#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""PROV-GUARD gate: verify `*Provenance: read-at-source.*` ground truths against a
stored generation capture.

Parses an analysis's section 3 (Ground Truths), joins every read-at-source GT to the
real `WebFetch`/`Read` call in the run's `.jsonl` capture that fetched its cited
source, and requires every numeric/currency literal the GT states to appear verbatim
in that source's retrieved text (PROV-01, PROV-02, PROV-03). Findings land as named
`_DEFECT_RECORD_FIELDS` columns (PROV-05) via `provenance_defect_record`.

Usage:
    python3 scripts/check-provenance.py [--self-test]

Exit codes:
    0  all checks passed
    1  validation/content failure (a source is unmatched or unreadable, a literal is
       unlocated or misattributed, or a self-test control behaves wrongly)
    2  environment error (Python <3.12, the fixture files are missing)

--self-test: runs an offline control battery of positive, negative and anti-masking
             controls (D-16), fully in-memory or tempdir-scoped -- no network access
             and no live Claude session.

## What this gate does not assert

1. It verifies that a stated number appears in the retrieved text of the source the
   analysis names. It does not verify the number means what the analysis says it
   means, nor that the chain citing it is valid inference -- that is backlog 999.4.
2. The literal regex (D-01, locked) also matches digit runs that are the tail of an
   alphanumeric identifier: `x86` yields `86`, `EC2` yields `2`. These still verify,
   because the identifier appears verbatim in the retrieved text, but carry no
   independent evidentiary weight. This is expected behaviour, not a parser bug.
3. Whole-span (bold or quoted) matching was measured and rejected -- 4/11 bold spans
   and 4/8 quoted spans located, because bold spans are paraphrase envelopes and
   quotes carry the analyst's own elisions. Do not resurrect it as a "cleaner" rule.
4. PROV-04's no-network control blocks `socket`; it does not cover a `subprocess`
   shell-out. Stated residual (D-14).

Phase 6 note: `scripts/check-firewall-battery.sh:346-349` already registers a battery
gate literally named `GATE-01` (bound to `check-agent.py`), so this gate must be
registered under a distinct id such as `PROV-GUARD` when Phase 6 wires it in.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import socket
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


# Repo-anchored, not caller-supplied: check-agent.py's rationale reproduced here --
# a constant derived from __file__ keeps the gate cwd-independent and its target
# cannot be silently re-pointed by an argv/env override.
REPO_ROOT: Path = Path(__file__).resolve().parents[1]
_FIXTURE_CAPTURE: Path = REPO_ROOT / "tests" / "quality-provenance-v8.24" / "PR-P1.jsonl"
_FIXTURE_ANALYSIS: Path = REPO_ROOT / "tests" / "quality-provenance-v8.24" / "PR-P1.md"
_FIXTURE_SUBAGENT_TYPE: str = "first-principles:first-principles"

# D-02: hardcoded pins, not merely reflected from whatever the run computes -- the
# STEP0-08 pin-as-literal pattern. A silent drop in extraction must fail the live
# leg, not pass with a smaller number.
_EXPECTED_SOURCES: int = 7
_EXPECTED_LITERALS: int = 35

# Deliberately NOT derived from the fixture's own 532-char minimum retrieved-text
# length, which would make the floor fixture-shaped. 50 is clearly below any real
# fetched page and clearly above an empty or near-empty fetch.
_MIN_RETRIEVED_TEXT_CHARS: int = 50


# ---------------------------------------------------------------------------
# Harness import (one-way). check-quality-harness.py never imports this file.
# ---------------------------------------------------------------------------

_HARNESS_PATH: Path = REPO_ROOT / "scripts" / "check-quality-harness.py"
_spec = importlib.util.spec_from_file_location("_quality_harness", _HARNESS_PATH)
_mod = importlib.util.module_from_spec(_spec)  # type: ignore[arg-type]
sys.modules["_quality_harness"] = _mod  # Python 3.13+ dataclass compat -- must precede exec_module
_spec.loader.exec_module(_mod)  # type: ignore[union-attr]

_slice_sections = _mod._slice_sections
_capture_subagent_tool_calls = _mod._capture_subagent_tool_calls
detect_defects = _mod.detect_defects
read_defect_incidence = _mod.read_defect_incidence
_DEFECT_RECORD_FIELDS = _mod._DEFECT_RECORD_FIELDS


def _require_python_version() -> None:
    if sys.version_info < (3, 12):
        sys.stderr.write(
            f"scripts/check-provenance.py requires Python >=3.12 "
            f"(running {sys.version_info.major}.{sys.version_info.minor}).\n"
        )
        sys.exit(2)


# ---------------------------------------------------------------------------
# PROV-01: section-3 parsing
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class GroundTruth:
    """One `- **GT-n**` list item parsed from an analysis's section 3."""

    gt_id: str
    label: str
    claim_body: str
    source: str
    literals: tuple[str, ...]


# A section-3 list item: "- **GT-1** <rest of line>". `re.M` so `$` anchors each
# GT to its own line -- every GT in the fixture is single-line.
_GT_LINE_RE = re.compile(r"^\-\s+\*\*(GT-\d+\??)\*\*\s+(.*)$", re.M)

# The literal label FORM, never the bare "read-at-source" substring: the fixture's
# section 3 contains "read-at-source" 26 times total (7 in this label, 19 more
# inside each GT's own "read-at-source: <location>" clause), but the label form
# itself only 7 times.
_READ_AT_SOURCE_LABEL = "*Provenance: read-at-source.*"

_PROVENANCE_LABEL_RE = re.compile(r"\*Provenance:\s*([a-zA-Z][a-zA-Z\-]*)\.\*")

# D-01, locked verbatim. No word-boundary anchor: it deliberately also matches a
# digit run that is the tail of an alphanumeric identifier (see limit 2 above).
_LITERAL_RE = re.compile(r"\$?\d[\d,]*(?:\.\d+)?")


def _claim_body(line_body: str) -> str:
    """Return the claim substring preceding the '— source: ...' clause.

    Without this split, digits inside the 'read-at-source: <location>'
    description are scanned too and the literal count lands on 37, not 35.
    """
    return re.split(r"\s+—\s+source:", line_body)[0]


def _source_string(line_body: str) -> str:
    """Return the text between '— source:' and the following ';', or the
    '*Provenance:' label if the source clause carries no semicolon, stripped.
    """
    m = re.search(r"—\s+source:\s*(.*)", line_body)
    if not m:
        return ""
    rest = m.group(1)
    if ";" in rest:
        return rest.split(";", 1)[0].strip()
    return rest.split("*Provenance:", 1)[0].strip()


def _label(line_body: str) -> str:
    """Return the GT's provenance label word ("read-at-source", "unverified", ...).

    Checks the exact `_READ_AT_SOURCE_LABEL` form as a substring first -- see
    that constant's own comment for why the bare substring is rejected.
    """
    if _READ_AT_SOURCE_LABEL in line_body:
        return "read-at-source"
    m = _PROVENANCE_LABEL_RE.search(line_body)
    return m.group(1) if m else ""


def _parse_ground_truths(section3: str) -> list[GroundTruth]:
    """Parse every '- **GT-n**' list item in `section3` into a `GroundTruth`.

    Includes every GT regardless of its provenance label; callers filter on
    `label == "read-at-source"`.
    """
    out: list[GroundTruth] = []
    for m in _GT_LINE_RE.finditer(section3):
        gt_id = m.group(1)
        line_body = m.group(2)
        claim = _claim_body(line_body)
        out.append(
            GroundTruth(
                gt_id=gt_id,
                label=_label(line_body),
                claim_body=claim,
                source=_source_string(line_body),
                literals=tuple(_LITERAL_RE.findall(claim)),
            )
        )
    return out


def parse_analysis(analysis_text: str) -> list[GroundTruth]:
    """Slice section 3 (Ground Truths) out of an analysis and parse its GT list.

    Lets `SectionResolutionError` from `_slice_sections` propagate -- a document
    the parser cannot read must fail loudly, never report zero findings.
    """
    section3 = _slice_sections(analysis_text)[3]
    return _parse_ground_truths(section3)


def _run_self_test() -> None:
    """Stub. Plan 05-03 fills this with the full D-16 control battery."""
    print("check-provenance --self-test: stub -- plan 05-03 fills the control battery")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="PROV-GUARD: verify read-at-source provenance against a stored capture."
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run the offline control battery (positive, negative, anti-masking)",
    )
    args = parser.parse_args()

    _require_python_version()

    if args.self_test:
        _run_self_test()
        return

    _validate_live_fixture()


if __name__ == "__main__":
    main()
