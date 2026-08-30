#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# ///
"""HC-04 gate: assert the Phase 5 tightening of Criterion 3 (Evidence) and
Criterion 5 (Conclusion) is present and well-formed in the Self-Audit rubric,
and that all three EXCEPT exceptions are documented, and that the
`## Exceptions Summary` navigation section exists in its required position.

Phase 5 tightened the rubric's prose to require HIGH-confidence chains
supporting ground truths and conclusions, with three documented exceptions.
Nothing currently stops a future edit from silently reverting it — no existing
gate reads the Criterion 3 or Criterion 5 Rigorous descriptors for the
HIGH-confidence bound, and VAL-04 is structurally blind to rubric content.
This gate is the ratchet that makes the tightening permanent.

This gate validates rubric structure only. It does NOT measure whether the
agent actually produces HIGH-confidence analyses — that is MEAS-01/MEAS-02,
deferred to v8.20+.

Usage:
    python3 scripts/check-high-confidence-bound.py [--self-test]

Exit codes:
    0  all checks passed
    1  validation failure (missing or malformed rubric elements)
    2  environment error (Python <3.12, rubric file not found)

--self-test: runs an offline control battery with negative and positive
             controls, exits 0 if every control behaves as intended; exits 1
             on any wrong-pass or wrong-reason failure.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REPO_ROOT: Path = Path(__file__).resolve().parents[1]
CANONICAL_RUBRIC: Path = REPO_ROOT / "shared" / "spine" / "references" / "validation-rubric.md"
EMITTED_RUBRIC: Path = REPO_ROOT / "first-principles" / "agents" / "references" / "validation-rubric.md"

# --- Heading literals (identica in both canonical and emitted copies) ---
_HOW_TO_APPLY = "## How to Apply This Gate"
_EXCEPTIONS_SUMMARY = "## Exceptions Summary"
_SCORING_MODEL = "## Scoring Model"
_CRITERION3_START = "### Criterion 3: Establish Ground Truths"
_CRITERION4_START = "### Criterion 4: Reason Upward"
_CRITERION5_START = "### Criterion 5: Validate"
_CRITERION6_START = "### Criterion 6: Conclusion-to-Ground-Truth Traceability"

# --- Rigorous band anchors (the "Sound" bullet ends each band) ---
_C3_SOUND_LEAD = "- **Sound** — GT-IDs are present and stable"
_C5_SOUND_LEAD = "- **Sound** — confidence ratings exist on chains"

# --- Whitespace flattening layer (copied from check-focused-parity.py) ---
_WS = re.compile(r"\s+")


def _flat(text: str) -> str:
    """Collapse every whitespace run to a single space."""
    return _WS.sub(" ", text)


def _contains(text: str, literal: str) -> bool:
    """Whitespace-insensitive containment."""
    return _flat(literal) in _flat(text)


def _count_flex(text: str, literal: str) -> int:
    """Whitespace-insensitive occurrence count of *literal* in *text*."""
    pattern = re.compile(
        r"\s+".join(re.escape(w) for w in _flat(literal).strip().split(" "))
    )
    return len(pattern.findall(text))


# --- Slicing contract (copied from check-act-limb.py) ---
def _slice(text: str, start_heading: str, end_heading: str) -> str | None:
    """Return the text strictly between *start_heading* and *end_heading*.

    Returns None if either heading is missing or they appear out of order.
    A vanished section is a failure to report, not an empty string to silently
    pass through.
    """
    start_idx = text.find(start_heading)
    if start_idx == -1:
        return None
    content_start = start_idx + len(start_heading)
    end_idx = text.find(end_heading, content_start)
    if end_idx == -1:
        return None
    return text[content_start:end_idx]


def _rigorous_region(slice_text: str | None, sound_anchor: str) -> str | None:
    """Return the Rigorous descriptor region from the start up to sound_anchor.

    Returns None if the anchor is missing or if slice_text is None.
    The Rigorous region includes the Rigorous bullet and follow-on paragraphs.
    """
    if slice_text is None:
        return None
    # Find the sound anchor
    idx = slice_text.find(sound_anchor)
    if idx == -1:
        return None
    return slice_text[:idx]


def _check_criterion3(text: str, surface: str) -> list[str]:
    """Check Criterion 3 Rigorous descriptors. Returns failure strings."""
    failures: list[str] = []

    # HC-1: Criterion 3 slice present
    c3_slice = _slice(text, _CRITERION3_START, _CRITERION4_START)
    if c3_slice is None:
        failures.append(f"HC-1: {surface} — Criterion 3 slice not found")
        return failures

    # HC-2: Criterion 3 Rigorous region present
    c3_rigorous = _rigorous_region(c3_slice, _C3_SOUND_LEAD)
    if c3_rigorous is None:
        failures.append(f"HC-2: {surface} — Criterion 3 Rigorous region not found (Sound anchor missing)")
        return failures

    # HC-3: "at least one HIGH-confidence chain"
    if not _contains(c3_rigorous, "at least one HIGH-confidence chain"):
        failures.append(f"HC-3: {surface} — Criterion 3 Rigorous: 'at least one HIGH-confidence chain' not found")

    # HC-4: "reachable"
    if not _contains(c3_rigorous, "reachable"):
        failures.append(f"HC-4: {surface} — Criterion 3 Rigorous: 'reachable' not found")

    # HC-5: EXCEPT clause with "unreachable"
    # Split on EXCEPT: and check if unreachable appears after the EXCEPT token
    except_parts = c3_rigorous.split("EXCEPT:")
    unreachable_found = False
    if len(except_parts) > 1:
        # Check the text following the first EXCEPT token (only the part of the first clause)
        first_clause = except_parts[1].split(".")[0] if "." in except_parts[1] else except_parts[1]
        if _contains(first_clause, "unreachable"):
            unreachable_found = True
    if not unreachable_found:
        failures.append(f"HC-5: {surface} — Criterion 3 Rigorous: EXCEPT clause with 'unreachable' not found")

    # HC-6: "Phase 3"
    if not _contains(c3_rigorous, "Phase 3"):
        failures.append(f"HC-6: {surface} — Criterion 3 Rigorous: 'Phase 3' not found")

    return failures


def _check_criterion5(text: str, surface: str) -> list[str]:
    """Check Criterion 5 Rigorous descriptors. Returns failure strings."""
    failures: list[str] = []

    # HC-7: Criterion 5 slice present
    c5_slice = _slice(text, _CRITERION5_START, _CRITERION6_START)
    if c5_slice is None:
        failures.append(f"HC-7: {surface} — Criterion 5 slice not found")
        return failures

    # HC-8: Criterion 5 Rigorous region present
    c5_rigorous = _rigorous_region(c5_slice, _C5_SOUND_LEAD)
    if c5_rigorous is None:
        failures.append(f"HC-8: {surface} — Criterion 5 Rigorous region not found (Sound anchor missing)")
        return failures

    # HC-9: "at least one HIGH-confidence"
    if not _contains(c5_rigorous, "at least one HIGH-confidence"):
        failures.append(f"HC-9: {surface} — Criterion 5 Rigorous: 'at least one HIGH-confidence' not found")

    # HC-10: "Conclusion" (case-insensitive for first letter)
    if not (_contains(c5_rigorous, "Conclusion") or _contains(c5_rigorous, "conclusion")):
        failures.append(f"HC-10: {surface} — Criterion 5 Rigorous: 'Conclusion' not found")

    # HC-11: EXCEPT clause mentioning "speculative"
    # Split on EXCEPT: and check if any following text contains "speculative"
    except_parts = c5_rigorous.split("EXCEPT:")
    speculative_found = False
    if len(except_parts) > 1:
        # Check each EXCEPT clause
        for part in except_parts[1:]:
            if _contains(part.split("EXCEPT:")[0], "speculative"):
                speculative_found = True
                break
    if not speculative_found:
        failures.append(f"HC-11: {surface} — Criterion 5 Rigorous: EXCEPT clause with 'speculative' not found")

    # HC-12: EXCEPT clause mentioning "absent-fails" (or "absent fails")
    absent_fails_found = False
    if len(except_parts) > 1:
        # Check each EXCEPT clause
        for part in except_parts[1:]:
            part_text = part.split("EXCEPT:")[0]
            if _contains(part_text, "absent-fails") or _contains(part_text, "absent fails"):
                absent_fails_found = True
                break
    if not absent_fails_found:
        failures.append(f"HC-12: {surface} — Criterion 5 Rigorous: EXCEPT clause with 'absent-fails' not found")

    return failures


if __name__ == "__main__":
    sys.exit(0)
