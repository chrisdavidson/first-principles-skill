#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""STEP0-01/02/03/08 gate: offline emulator for the Step 0 phrase-detection classifier.

Parses the ``**Phrase detection rules**`` table from the canonical source
``shared/spine/SKILL-body.md`` into a deterministic prompt → MODE classifier.
Fails loudly (non-zero exit + explicit error) on any of the four D-05 corruption
modes so table edits can never silently produce wrong classifications.

Usage:
    python3 scripts/check-step0-emulator.py --self-test
    python3 scripts/check-step0-emulator.py --prompt "run a pre-mortem on this"

Exit codes:
    0  self-test passed, or --prompt printed a MODE
    1  self-test failure, or --prompt produced a loud parse failure
    2  environment error (Python <3.12, canonical source not found)

--self-test: runs TWO fixture categories offline with no live claude session:
  1. Fault-injection fixtures (D-05) — four hardcoded malformed table strings,
     each pinning a required error substring in the expected failure message.
  2. Classification fixtures — loads the real table from shared/spine/SKILL-body.md
     and the real catalog from tests/step0-fixture-catalog.md; classifies every
     row and asserts expected MODE.

--prompt: classify a single prompt string and print the MODE (convenience flag
          for manual checks and Phase 72 live-harness development).
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


REPO_ROOT: Path = Path(__file__).resolve().parents[1]

# Canonical source — always read from shared/, never from the generated tree.
# Pitfall 1: do NOT read first-principles/agents/first-principles.md (generated output).
SKILL_BODY: Path = REPO_ROOT / "shared" / "spine" / "SKILL-body.md"
CATALOG_PATH: Path = REPO_ROOT / "tests" / "step0-fixture-catalog.md"

# D-06: hardcoded allowlist — intentional second source of truth.
# Do NOT derive this from the parsed table: the independence is what makes
# D-05.3 actually catch renames/typos in the table.
KNOWN_TECHNIQUES = ("pre-mortem", "inversion", "fishbone", "five-whys", "trade-off", "second-order", "decompose", "estimate", "theoretical-limit")


# ---------------------------------------------------------------------------
# Table parsing helpers
# ---------------------------------------------------------------------------

def _extract_phrases(cell: str) -> list[str]:
    """Extract quoted trigger phrases from a table cell.

    Uses quoted-substring extraction rather than naive comma-split (D-03),
    so commas inside a pattern string are safe.

    Example:
        '"pre-mortem", "nervous about (my|the|this) plan"'
        → ['pre-mortem', 'nervous about (my|the|this) plan']
    """
    return re.findall(r'"([^"]+)"', cell)


def _parse_table_rows(lines: list[str]) -> list[tuple[str, str]]:
    """Parse markdown pipe-table data rows, pipe-safe, skipping separator lines.

    Stops at the first non-pipe-prefixed line (table has ended).
    Returns a list of (first_cell, remainder) tuples per data row.

    CR-01 / WR-02 fix: splits only on the FIRST interior pipe so that embedded
    ``|`` characters inside quoted phrases (e.g. ``(my|the|this)``) are preserved
    in the remainder. GFM colon-alignment separators (``| :--- | ---: |``) are
    recognized by including ``:`` in the stripped character set.
    """
    rows: list[tuple[str, str]] = []
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("|"):
            break  # table ended
        body = stripped[1:]  # drop the leading pipe
        # Skip separator rows like |---|---| and | :--- | ---: |
        # WR-02: include ':' so colon-aligned GFM separators are recognized.
        # IN-01: use a single fullmatch — the old ``set(inner) <= set("-")``
        # disjunct was unreachable dead code after the replace("-") had already
        # stripped all dashes.
        if re.fullmatch(r"[\s\-:|]+", body):
            continue
        # technique = text up to the first unquoted pipe; remainder = rest of line
        first_pipe = body.index("|")
        first_cell = body[:first_pipe].strip()
        remainder = body[first_pipe + 1:]
        rows.append((first_cell, remainder))
    return rows


def _parse_phrase_table(path: Path) -> list[tuple[str, list[re.Pattern[str]]]]:
    """Parse the phrase-detection table from the canonical SKILL-body.md source.

    Returns a list of ``(technique, [compiled_regex, ...])`` pairs in declaration
    order (first-row-wins precedence, D-04).

    Exits non-zero with a loud error message on any of the four D-05 modes:
      D-05.1 — anchor ``**Phrase detection rules**`` not found
      D-05.2 — zero technique rows parsed, or a row has an empty pattern cell
      D-05.3 — a technique name is not in KNOWN_TECHNIQUES
      D-05.4 — a quoted phrase fails re.compile (caught at load time)
    """
    text = path.read_text(encoding="utf-8")

    # D-05.1: anchor missing
    anchor = "**Phrase detection rules**"
    if anchor not in text:
        sys.stderr.write(
            "check-step0-emulator: FAIL — phrase detection anchor "
            f"'{anchor}' not found in {path.name}\n"
        )
        sys.exit(1)

    # Locate the anchor and find the markdown table that follows it
    anchor_pos = text.index(anchor)
    after_anchor = text[anchor_pos:]
    lines = after_anchor.splitlines()

    # Find the header row of the table (first line starting with '|' after anchor)
    table_start: int | None = None
    for i, line in enumerate(lines):
        if line.strip().startswith("|"):
            table_start = i
            break

    if table_start is None:
        sys.stderr.write(
            "check-step0-emulator: FAIL — phrase detection table: "
            "zero technique rows found (no table after anchor)\n"
        )
        sys.exit(1)

    all_rows = _parse_table_rows(lines[table_start:])

    # Skip the header row (first row) to get data rows
    data_rows = all_rows[1:] if all_rows else []

    # D-05.2: zero rows
    if not data_rows:
        sys.stderr.write(
            "check-step0-emulator: FAIL — phrase detection table: "
            "zero technique rows parsed\n"
        )
        sys.exit(1)

    rules: list[tuple[str, list[re.Pattern[str]]]] = []
    for technique, cell in data_rows:
        # WR-03: balanced-quote guard — an odd number of '"' means the cell has
        # an unterminated quoted phrase (D-05-class corruption).  Fail loudly
        # rather than silently extracting a partial phrase list.
        if cell.count('"') % 2 != 0:
            sys.stderr.write(
                f"check-step0-emulator: FAIL — technique '{technique}' phrase cell "
                f"has an unbalanced quote (possible pipe-split corruption): {cell!r}\n"
            )
            sys.exit(1)

        # D-05.2: empty pattern cell
        phrases = _extract_phrases(cell)
        if not phrases:
            sys.stderr.write(
                f"check-step0-emulator: FAIL — technique '{technique}' "
                f"has empty pattern cell\n"
            )
            sys.exit(1)

        # D-05.3: unknown technique name
        if technique not in KNOWN_TECHNIQUES:
            sys.stderr.write(
                f"check-step0-emulator: FAIL — unknown technique '{technique}' "
                f"(not in KNOWN_TECHNIQUES)\n"
            )
            sys.exit(1)

        # D-05.4: uncompilable regex — caught at load time, not per-prompt
        compiled: list[re.Pattern[str]] = []
        for phrase in phrases:
            try:
                compiled.append(re.compile(phrase, re.IGNORECASE))
            except re.error as exc:
                sys.stderr.write(
                    f"check-step0-emulator: FAIL — technique '{technique}' "
                    f"phrase {phrase!r} is not a valid Python regex: {exc}\n"
                )
                sys.exit(1)

        rules.append((technique, compiled))

    return rules


# ---------------------------------------------------------------------------
# Classifier
# ---------------------------------------------------------------------------

def classify(prompt: str, rules: list[tuple[str, list[re.Pattern[str]]]]) -> str:
    """Classify a prompt string to a MODE.

    Iterates rules in declaration order (D-04, first-row-wins). Returns
    ``f"focused-{technique}"`` for the first technique whose any compiled
    pattern fires via ``re.search``. Returns ``"full-composer"`` if no
    pattern fires (D-04 default).
    """
    for technique, patterns in rules:
        for pattern in patterns:
            if pattern.search(prompt):
                return f"focused-{technique}"
    return "full-composer"


# ---------------------------------------------------------------------------
# Catalog reader
# ---------------------------------------------------------------------------

def _read_catalog(path: Path) -> list[tuple[str, str, str]]:
    """Parse the fixture catalog at ``path`` into ``(id, prompt, expected_mode)`` tuples.

    Expects a markdown pipe-table with columns: ID | Prompt | Expected MODE | Notes.
    Skips the header row and separator row automatically.

    WR-01: validates ``expected_mode`` against the known MODE allowlist and
    exits non-zero if the value is unrecognized — a column-shift (e.g. from a
    prompt cell containing a bare ``|``) must never pass silently.
    """
    valid_modes = {"full-composer"} | {f"focused-{t}" for t in KNOWN_TECHNIQUES}

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    # Find the catalog table (first line starting with '|')
    table_start: int | None = None
    for i, line in enumerate(lines):
        if line.strip().startswith("|"):
            table_start = i
            break

    if table_start is None:
        sys.stderr.write(
            f"check-step0-emulator: FAIL — no table found in catalog {path}\n"
        )
        sys.exit(1)

    all_rows = _parse_table_rows(lines[table_start:])
    # Skip the header row
    data_rows = all_rows[1:] if all_rows else []

    result: list[tuple[str, str, str]] = []
    for row_id, remainder in data_rows:
        # Catalog columns: ID | Prompt | Expected MODE | Notes
        # remainder contains " Prompt | Expected MODE | Notes |" after the ID cell.
        # Split on the first two pipes to extract prompt and expected_mode.
        parts = remainder.split("|")
        if len(parts) < 2:
            sys.stderr.write(
                f"check-step0-emulator: FAIL — malformed catalog row "
                f"(expected >=3 columns, got fewer after ID '{row_id}'): "
                f"{remainder!r}\n"
            )
            sys.exit(1)
        prompt = parts[0].strip()
        expected_mode = parts[1].strip()
        # WR-01: validate against the known MODE allowlist
        if expected_mode not in valid_modes:
            sys.stderr.write(
                f"check-step0-emulator: FAIL — catalog row {row_id}: "
                f"unrecognized MODE {expected_mode!r} "
                f"(not in KNOWN_TECHNIQUES allowlist; possible column-shift)\n"
            )
            sys.exit(1)
        result.append((row_id, prompt, expected_mode))

    return result


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

def _run_self_test() -> None:
    """Run TWO fixture categories and exit non-zero if any produces the wrong verdict.

    Category 1: Fault-injection fixtures (D-05) — hardcoded malformed table strings.
      Each fixture expects the parser to exit non-zero with a specific error substring.
      Uses subprocess to capture exit code + stderr so a non-zero exit + expected
      substring counts as a correct fail; a missing substring is a wrong-reason failure.

    Category 2: Classification fixtures — loads the real table from SKILL-body.md and
      the real catalog from step0-fixture-catalog.md; classifies every row and asserts
      the computed MODE matches the expected MODE.

    Pitfall 3: fault-injection fixtures use hardcoded malformed strings, NOT the live file.
    """
    wrong: list[str] = []

    # -----------------------------------------------------------------------
    # Category 1: D-05 fault-injection fixtures (hardcoded malformed strings)
    # -----------------------------------------------------------------------

    # Each tuple: (label, malformed_table_text, expected_error_substring)
    fault_fixtures = [
        # D-05.1: anchor missing — no "**Phrase detection rules**" in text
        (
            "D-05.1 anchor-missing",
            "| Technique | Trigger phrases (any one fires) |\n"
            "|---|---|\n"
            '| pre-mortem | "pre-mortem" |\n',
            "anchor",
        ),
        # D-05.2: zero rows — anchor present but table has only a header + separator
        (
            "D-05.2 zero-rows",
            "**Phrase detection rules** (case-insensitive)\n"
            "\n"
            "| Technique | Trigger phrases (any one fires) |\n"
            "|---|---|\n",
            "zero",
        ),
        # D-05.3: unknown technique — row with name "unknown-technique"
        (
            "D-05.3 unknown-technique",
            "**Phrase detection rules** (case-insensitive)\n"
            "\n"
            "| Technique | Trigger phrases (any one fires) |\n"
            "|---|---|\n"
            '| unknown-technique | "trigger phrase" |\n',
            "unknown technique",
        ),
        # D-05.4: uncompilable regex — quoted cell contains "[" (invalid regex)
        (
            "D-05.4 bad-regex",
            "**Phrase detection rules** (case-insensitive)\n"
            "\n"
            "| Technique | Trigger phrases (any one fires) |\n"
            "|---|---|\n"
            '| pre-mortem | "[" |\n',
            "not a valid Python regex",
        ),
    ]

    for label, table_text, expected_substring in fault_fixtures:
        # Write the malformed table to a temporary file and run the parser
        # via subprocess so we can capture exit code + stderr
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as tmp:
            tmp.write(table_text)
            tmp_path = tmp.name

        try:
            result = subprocess.run(
                [
                    sys.executable,
                    str(Path(__file__).resolve()),
                    "--_parse-table-test",
                    tmp_path,
                ],
                capture_output=True,
                text=True,
            )
            exit_code = result.returncode
            stderr_text = result.stderr
        finally:
            os.unlink(tmp_path)

        if exit_code == 0:
            print(
                f"check-step0-emulator --self-test: {label} WRONGLY PASSED "
                f"(expected non-zero exit)"
            )
            wrong.append(f"{label} (wrongly passed)")
        elif expected_substring not in stderr_text:
            print(
                f"check-step0-emulator --self-test: {label} failed for WRONG reason "
                f"(expected '{expected_substring}' in stderr, got: {stderr_text.strip()!r})"
            )
            wrong.append(f"{label} (wrong reason, expected '{expected_substring}')")
        else:
            print(
                f"check-step0-emulator --self-test: {label} correctly failed "
                f"(exit {exit_code}, found '{expected_substring}')"
            )

    # -----------------------------------------------------------------------
    # Category 2: classification fixtures (real table + real catalog)
    # -----------------------------------------------------------------------

    # Load the real normalized phrase table
    if not SKILL_BODY.exists():
        sys.stderr.write(
            f"check-step0-emulator: FAIL — canonical source not found: {SKILL_BODY}\n"
        )
        sys.exit(2)

    rules = _parse_phrase_table(SKILL_BODY)

    # Load the real fixture catalog
    if not CATALOG_PATH.exists():
        sys.stderr.write(
            f"check-step0-emulator: FAIL — fixture catalog not found: {CATALOG_PATH}\n"
        )
        sys.exit(2)

    fixtures = _read_catalog(CATALOG_PATH)

    for row_id, prompt, expected_mode in fixtures:
        computed = classify(prompt, rules)
        if computed == expected_mode:
            print(
                f"check-step0-emulator --self-test: {row_id} PASS "
                f"('{prompt[:50]}...' → {computed})"
                if len(prompt) > 50
                else f"check-step0-emulator --self-test: {row_id} PASS "
                f"('{prompt}' → {computed})"
            )
        else:
            print(
                f"check-step0-emulator --self-test: {row_id} FAIL "
                f"(expected {expected_mode!r}, got {computed!r}, "
                f"prompt: {prompt[:60]!r})"
            )
            wrong.append(
                f"{row_id} (expected {expected_mode!r}, got {computed!r})"
            )

    # -----------------------------------------------------------------------
    # Category 3: RR-80-01 named emulator assertion (D-02 / D-04)
    #
    # RR-80-01 is the S-N04 negative-control over-routing residual recorded at
    # 2/5 FAIL in tests/step0-baseline-v5.3.md (live agent over-routes to
    # focused-pre-mortem on oblique pre-mortem-adjacent prompts).  This
    # assertion confirms the INTENDED emulator classification (full-composer —
    # no trigger phrase fires), not the live pass rate (honesty-not-score
    # principle). The assertion hardcodes the literal RR-80-01 ID and the
    # verbatim S-N04 prompt so RR-80-01 coverage is catalog-independent (D-04):
    # deleting the S-N04 row from tests/step0-fixture-catalog.md cannot
    # silently drop this gate.
    # -----------------------------------------------------------------------

    _RR80_01_PROMPT = (
        "We have a written plan to roll out the new authentication system across "
        "all teams next quarter. Before we lock the timeline, "
        "walk through how this could go badly — what failure modes should we prepare for?"
    )
    _RR80_01_EXPECTED = "full-composer"

    # Drift guard (WR-02): the hardcoded literal must still match the live catalog
    # S-N04 row, OR the row must be absent.  Deletion is the survivable case D-04
    # targets (the literal — not the catalog — is what gets classified below, so the
    # gate keeps running catalog-independently).  But a silent *edit* to the catalog
    # row (e.g. the fragile em-dash mangled to `--` or a different dash codepoint)
    # now fails loudly here instead of leaving the gate testing a stale prompt.
    _sn04_catalog_prompt = next(
        (p for rid, p, _ in fixtures if rid == "S-N04"), None
    )
    if _sn04_catalog_prompt is not None and _sn04_catalog_prompt != _RR80_01_PROMPT:
        print(
            "check-step0-emulator --self-test: RR-80-01 S-N04 FAIL "
            "(hardcoded literal drifted from the live catalog S-N04 row — re-sync "
            "the literal or update the gate)"
        )
        wrong.append(
            "RR-80-01 S-N04 (literal drifted from catalog row "
            f"{_sn04_catalog_prompt!r} != {_RR80_01_PROMPT!r})"
        )

    rr80_01_computed = classify(_RR80_01_PROMPT, rules)
    if rr80_01_computed == _RR80_01_EXPECTED:
        print(
            "check-step0-emulator --self-test: RR-80-01 S-N04 PASS "
            f"(oblique pre-mortem-adjacent prompt → {rr80_01_computed})"
        )
    else:
        print(
            f"check-step0-emulator --self-test: RR-80-01 S-N04 FAIL "
            f"(expected {_RR80_01_EXPECTED!r}, got {rr80_01_computed!r}; "
            f"a trigger phrase fired on the S-N04 oblique prompt)"
        )
        wrong.append(
            f"RR-80-01 S-N04 (expected {_RR80_01_EXPECTED!r}, got {rr80_01_computed!r})"
        )

    # -----------------------------------------------------------------------
    # Category 4: DECOMP-07 named emulator assertions (D-02 / D-04)
    #
    # Two catalog-independent hardcoded assertions that lock in decompose
    # phrase-detection behavior:
    #   (a) A positive prompt fires the decompose trigger → focused-decompose.
    #   (b) The WR-01 mis-route prompt ("decompose this problem from first
    #       principles: …") does NOT fire any decompose trigger → full-composer.
    #       This is the CI-invisible WR-01 guard: check-trigger-collisions.py
    #       scans only skill descriptions, never the Step 0 phrase table, so
    #       this hardcoded assertion is the only CI gate that catches a
    #       mis-route regression.
    # Both literals are catalog-independent (D-04): deleting S-P09 or S-N05
    # from step0-fixture-catalog.md cannot silently drop these gates.
    # -----------------------------------------------------------------------

    _DECOMP07_POS_PROMPT = (
        "decompose this claim: a molten-salt thermal storage system achieves "
        "85% round-trip electricity efficiency when paired with a combined-cycle "
        "gas turbine — the vendor has published test data from a pilot plant in "
        "the Atacama Desert"
    )
    _DECOMP07_POS_EXPECTED = "focused-decompose"

    _DECOMP07_NEG_PROMPT = (
        "decompose this problem from first principles: a molten-salt thermal "
        "storage system achieves 85% round-trip electricity efficiency — "
        "walk me through how to approach this"
    )
    _DECOMP07_NEG_EXPECTED = "full-composer"

    # Drift guard: hardcoded positive literal must still match the live catalog
    # S-P09 row, OR the row must be absent.
    _sp09_catalog_prompt = next(
        (p for rid, p, _ in fixtures if rid == "S-P09"), None
    )
    if _sp09_catalog_prompt is not None and _sp09_catalog_prompt != _DECOMP07_POS_PROMPT:
        print(
            "check-step0-emulator --self-test: DECOMP-07 S-P09 FAIL "
            "(hardcoded positive literal drifted from the live catalog S-P09 row — re-sync "
            "the literal or update the gate)"
        )
        wrong.append(
            f"DECOMP-07 S-P09 (literal drifted from catalog row "
            f"{_sp09_catalog_prompt!r} != {_DECOMP07_POS_PROMPT!r})"
        )

    # Drift guard: hardcoded negative literal must still match the live catalog
    # S-N05 row, OR the row must be absent.
    _sn05_catalog_prompt = next(
        (p for rid, p, _ in fixtures if rid == "S-N05"), None
    )
    if _sn05_catalog_prompt is not None and _sn05_catalog_prompt != _DECOMP07_NEG_PROMPT:
        print(
            "check-step0-emulator --self-test: DECOMP-07 S-N05 FAIL "
            "(hardcoded negative literal drifted from the live catalog S-N05 row — re-sync "
            "the literal or update the gate)"
        )
        wrong.append(
            f"DECOMP-07 S-N05 (literal drifted from catalog row "
            f"{_sn05_catalog_prompt!r} != {_DECOMP07_NEG_PROMPT!r})"
        )

    decomp07_pos_computed = classify(_DECOMP07_POS_PROMPT, rules)
    if decomp07_pos_computed == _DECOMP07_POS_EXPECTED:
        print(
            "check-step0-emulator --self-test: DECOMP-07 S-P09 PASS "
            f"(decompose trigger prompt → {decomp07_pos_computed})"
        )
    else:
        print(
            f"check-step0-emulator --self-test: DECOMP-07 S-P09 FAIL "
            f"(expected {_DECOMP07_POS_EXPECTED!r}, got {decomp07_pos_computed!r})"
        )
        wrong.append(
            f"DECOMP-07 S-P09 (expected {_DECOMP07_POS_EXPECTED!r}, got {decomp07_pos_computed!r})"
        )

    decomp07_neg_computed = classify(_DECOMP07_NEG_PROMPT, rules)
    if decomp07_neg_computed == _DECOMP07_NEG_EXPECTED:
        print(
            "check-step0-emulator --self-test: DECOMP-07 S-N05 PASS "
            f"(WR-01 mis-route prompt → {decomp07_neg_computed})"
        )
    else:
        print(
            f"check-step0-emulator --self-test: DECOMP-07 S-N05 FAIL "
            f"(expected {_DECOMP07_NEG_EXPECTED!r}, got {decomp07_neg_computed!r}; "
            f"WR-01 regression: mis-route prompt now fires a trigger)"
        )
        wrong.append(
            f"DECOMP-07 S-N05 (expected {_DECOMP07_NEG_EXPECTED!r}, got {decomp07_neg_computed!r})"
        )

    # -----------------------------------------------------------------------
    # Category 5: ESTIMATE-07 named emulator assertions (D-02 / D-04)
    #
    # Two catalog-independent hardcoded assertions that lock in estimate
    # phrase-detection behavior:
    #   (a) A positive prompt fires the estimate trigger → focused-estimate.
    #   (b) The S-N06 over-firing prompt ("estimate the impact of …") does NOT
    #       fire any estimate trigger → full-composer.
    #       This is the only CI gate catching an estimate over-firing regression:
    #       check-trigger-collisions.py scans only skill descriptions, never the
    #       Step 0 phrase table, so this hardcoded assertion is the only CI gate
    #       that catches a phrase over-firing regression on 'estimate the impact
    #       of' vs 'estimate the (size|number|magnitude|cost) of'.
    # Both literals are catalog-independent (D-04): deleting S-P10 or S-N06
    # from step0-fixture-catalog.md cannot silently drop these gates.
    # -----------------------------------------------------------------------

    _ESTIMATE07_POS_PROMPT = (
        "roughly how much does a molten-salt thermal storage system cost per kWh "
        "of usable capacity for a 200 MWh utility-scale installation — assume a "
        "30-year plant lifetime, a charging cycle once per day, and that the salt "
        "tanks are pre-commissioned"
    )
    _ESTIMATE07_POS_EXPECTED = "focused-estimate"

    _ESTIMATE07_NEG_PROMPT = (
        "estimate the impact of migrating our monolith to microservices next "
        "quarter — the platform team is planning a phased decomposition over six "
        "sprints and we want to understand the downstream effects on developer "
        "velocity and incident rate"
    )
    _ESTIMATE07_NEG_EXPECTED = "full-composer"

    # Drift guard: hardcoded positive literal must still match the live catalog
    # S-P10 row, OR the row must be absent.
    _sp10_catalog_prompt = next(
        (p for rid, p, _ in fixtures if rid == "S-P10"), None
    )
    if _sp10_catalog_prompt is not None and _sp10_catalog_prompt != _ESTIMATE07_POS_PROMPT:
        print(
            "check-step0-emulator --self-test: ESTIMATE-07 S-P10 FAIL "
            "(hardcoded positive literal drifted from the live catalog S-P10 row — re-sync "
            "the literal or update the gate)"
        )
        wrong.append(
            f"ESTIMATE-07 S-P10 (literal drifted from catalog row "
            f"{_sp10_catalog_prompt!r} != {_ESTIMATE07_POS_PROMPT!r})"
        )

    # Drift guard: hardcoded negative literal must still match the live catalog
    # S-N06 row, OR the row must be absent.
    _sn06_catalog_prompt = next(
        (p for rid, p, _ in fixtures if rid == "S-N06"), None
    )
    if _sn06_catalog_prompt is not None and _sn06_catalog_prompt != _ESTIMATE07_NEG_PROMPT:
        print(
            "check-step0-emulator --self-test: ESTIMATE-07 S-N06 FAIL "
            "(hardcoded negative literal drifted from the live catalog S-N06 row — re-sync "
            "the literal or update the gate)"
        )
        wrong.append(
            f"ESTIMATE-07 S-N06 (literal drifted from catalog row "
            f"{_sn06_catalog_prompt!r} != {_ESTIMATE07_NEG_PROMPT!r})"
        )

    estimate07_pos_computed = classify(_ESTIMATE07_POS_PROMPT, rules)
    if estimate07_pos_computed == _ESTIMATE07_POS_EXPECTED:
        print(
            "check-step0-emulator --self-test: ESTIMATE-07 S-P10 PASS "
            f"(estimate trigger prompt → {estimate07_pos_computed})"
        )
    else:
        print(
            f"check-step0-emulator --self-test: ESTIMATE-07 S-P10 FAIL "
            f"(expected {_ESTIMATE07_POS_EXPECTED!r}, got {estimate07_pos_computed!r})"
        )
        wrong.append(
            f"ESTIMATE-07 S-P10 (expected {_ESTIMATE07_POS_EXPECTED!r}, got {estimate07_pos_computed!r})"
        )

    estimate07_neg_computed = classify(_ESTIMATE07_NEG_PROMPT, rules)
    if estimate07_neg_computed == _ESTIMATE07_NEG_EXPECTED:
        print(
            "check-step0-emulator --self-test: ESTIMATE-07 S-N06 PASS "
            f"(over-firing boundary prompt → {estimate07_neg_computed})"
        )
    else:
        print(
            f"check-step0-emulator --self-test: ESTIMATE-07 S-N06 FAIL "
            f"(expected {_ESTIMATE07_NEG_EXPECTED!r}, got {estimate07_neg_computed!r}; "
            f"over-firing regression: 'estimate the impact of' now fires a trigger "
            f"(estimate the (size/number/magnitude/cost) of must not match 'impact'))"
        )
        wrong.append(
            f"ESTIMATE-07 S-N06 (expected {_ESTIMATE07_NEG_EXPECTED!r}, got {estimate07_neg_computed!r})"
        )

    # -----------------------------------------------------------------------
    # Category 6: TLIMIT-07 named emulator assertions (D-02 / D-03 / D-04)
    #
    # Two catalog-independent hardcoded assertions that lock in theoretical-limit
    # phrase-detection behavior:
    #   (a) A positive prompt fires the theoretical-limit trigger → focused-theoretical-limit.
    #   (b) The S-N07 WR-01 regression boundary prompt ("upper bound on our Q3 cloud
    #       spend") does NOT fire any theoretical-limit trigger → full-composer.
    #       This is the ONLY CI guard for the WR-01 'upper bound on' narrowing boundary
    #       (the Phase-105 over-firing fix narrowed 'upper bound on |.*' to
    #       'upper bound on what.?s achievable' in commit 57bf737):
    #       check-trigger-collisions.py scans only skill descriptions, never the
    #       Step 0 phrase table, so this hardcoded assertion is the only CI gate
    #       that catches a WR-01 regression where the narrowed phrase re-broadens
    #       to match a generic 'upper bound on [other]' prompt.
    #       This makes S-N07 analogous to decompose's S-N05 (a real mis-route guard),
    #       not estimate's S-N06 (mere over-firing guard).
    # Both literals are catalog-independent (D-04): deleting S-P14 or S-N07
    # from step0-fixture-catalog.md cannot silently drop these gates.
    # -----------------------------------------------------------------------

    _TLIMIT07_POS_PROMPT = (
        "For a molten-salt thermal-storage plant, what's the theoretical limit on "
        "thermodynamic conversion efficiency, setting aside current engineering "
        "practice — what do the laws actually permit?"
    )
    _TLIMIT07_POS_EXPECTED = "focused-theoretical-limit"

    _TLIMIT07_NEG_PROMPT = (
        "We're forecasting infrastructure costs for next year and need the upper "
        "bound on our Q3 cloud spend given current usage trends and committed-use "
        "discounts — what's the most it could realistically reach?"
    )
    _TLIMIT07_NEG_EXPECTED = "full-composer"

    # Drift guard: hardcoded positive literal must still match the live catalog
    # S-P14 row, OR the row must be absent.
    _sp14_catalog_prompt = next(
        (p for rid, p, _ in fixtures if rid == "S-P14"), None
    )
    if _sp14_catalog_prompt is not None and _sp14_catalog_prompt != _TLIMIT07_POS_PROMPT:
        print(
            "check-step0-emulator --self-test: TLIMIT-07 S-P14 FAIL "
            "(hardcoded positive literal drifted from the live catalog S-P14 row — re-sync "
            "the literal or update the gate)"
        )
        wrong.append(
            f"TLIMIT-07 S-P14 (literal drifted from catalog row "
            f"{_sp14_catalog_prompt!r} != {_TLIMIT07_POS_PROMPT!r})"
        )

    # Drift guard: hardcoded negative literal must still match the live catalog
    # S-N07 row, OR the row must be absent.
    _sn07_catalog_prompt = next(
        (p for rid, p, _ in fixtures if rid == "S-N07"), None
    )
    if _sn07_catalog_prompt is not None and _sn07_catalog_prompt != _TLIMIT07_NEG_PROMPT:
        print(
            "check-step0-emulator --self-test: TLIMIT-07 S-N07 FAIL "
            "(hardcoded negative literal drifted from the live catalog S-N07 row — re-sync "
            "the literal or update the gate)"
        )
        wrong.append(
            f"TLIMIT-07 S-N07 (literal drifted from catalog row "
            f"{_sn07_catalog_prompt!r} != {_TLIMIT07_NEG_PROMPT!r})"
        )

    tlimit07_pos_computed = classify(_TLIMIT07_POS_PROMPT, rules)
    if tlimit07_pos_computed == _TLIMIT07_POS_EXPECTED:
        print(
            "check-step0-emulator --self-test: TLIMIT-07 S-P14 PASS "
            f"(theoretical-limit trigger prompt → {tlimit07_pos_computed})"
        )
    else:
        print(
            f"check-step0-emulator --self-test: TLIMIT-07 S-P14 FAIL "
            f"(expected {_TLIMIT07_POS_EXPECTED!r}, got {tlimit07_pos_computed!r})"
        )
        wrong.append(
            f"TLIMIT-07 S-P14 (expected {_TLIMIT07_POS_EXPECTED!r}, got {tlimit07_pos_computed!r})"
        )

    tlimit07_neg_computed = classify(_TLIMIT07_NEG_PROMPT, rules)
    if tlimit07_neg_computed == _TLIMIT07_NEG_EXPECTED:
        print(
            "check-step0-emulator --self-test: TLIMIT-07 S-N07 PASS "
            f"(WR-01 boundary prompt → {tlimit07_neg_computed})"
        )
    else:
        print(
            f"check-step0-emulator --self-test: TLIMIT-07 S-N07 FAIL "
            f"(expected {_TLIMIT07_NEG_EXPECTED!r}, got {tlimit07_neg_computed!r}; "
            f"WR-01 regression: narrowed phrase 'upper bound on what's achievable' now matches "
            f"a generic cloud-spend prompt (must NOT match without 'what's achievable' phrasing))"
        )
        wrong.append(
            f"TLIMIT-07 S-N07 (expected {_TLIMIT07_NEG_EXPECTED!r}, got {tlimit07_neg_computed!r})"
        )

    # -----------------------------------------------------------------------
    # Category 7: SEMGATE named emulator assertions (D-02 / D-03 / D-04)
    #
    # Three catalog-independent hardcoded assertions that lock the intended winner
    # for each documented semantic-overlap pair (SEMGATE-01 / SEMGATE-02).
    #
    # Motivation (D-04 catalog-independence): the S-A catalog rows added in Plan
    # 107-02 can be silently deleted without breaking these assertions — the
    # hardcoded literals below, not the catalog rows, are what get classified.
    # Any silent edit to a catalog row fails loudly via the drift guard.
    #
    # This also makes GT-6 demonstrable: each co-fire literal fires BOTH triggers
    # of an overlap pair simultaneously, but classify() returns exactly ONE winner
    # via first-row-wins precedence on the post-reorder SKILL-body phrase table
    # (Plan 107-01 moved decompose above five-whys and theoretical-limit above
    # inversion).  check-trigger-collisions.py (VAL-04) is structurally blind to
    # this disambiguation — it scans only skill description text, never the Step 0
    # phrase table — so this Category 7 block is the only CI gate that locks the
    # post-reorder intended winner for each pair (VAL-04 complementarity, GT-6).
    #
    # Pair 1: decompose vs. five-whys (S-A01)
    #   Both triggers fire: "decompose this claim" fires phrase 1 of decompose;
    #   "root cause" fires the five-whys trigger.
    #   Post-reorder winner: decompose (row 5 beats row 6 under first-row-wins).
    #   VAL-04 complementarity: a 4-gram collision scan on the SKILL-body text
    #   cannot detect this precedence — the same phrase fires two independent rows
    #   and only the row ORDER determines the winner.
    #
    # Pair 2: theoretical-limit vs. inversion (S-A03)
    #   Both triggers fire: "theoretical limit" fires theoretical-limit; the
    #   inversion trigger "what would guarantee .* fail(ure)?" fires on
    #   "what would guarantee that a planned storage upgrade fails".
    #   Post-reorder winner: theoretical-limit (row 2 beats row 3 under first-row-wins).
    #
    # Pair 3: inversion vs. pre-mortem (S-A05)
    #   Both triggers fire: "I'm nervous about this plan" fires pre-mortem;
    #   "invert" fires inversion.
    #   Intended winner: pre-mortem (row 1 beats row 3 — already correct, no reorder
    #   needed, D-05 flagship-first kept intentionally).
    # -----------------------------------------------------------------------

    _SEMGATE07_DECOMP_FW_PROMPT = (
        "decompose this claim into its constituent parts: for a molten-salt thermal "
        "storage system, why did the round-trip electricity efficiency drop below "
        "projections — what is the root cause of the performance gap?"
    )
    _SEMGATE07_DECOMP_FW_EXPECTED = "focused-decompose"

    _SEMGATE07_TL_INV_PROMPT = (
        "For a molten-salt thermal storage system, what is the theoretical limit on "
        "round-trip efficiency given thermodynamic laws — and separately, what would "
        "guarantee that a planned storage upgrade fails to meet its performance targets?"
    )
    _SEMGATE07_TL_INV_EXPECTED = "focused-theoretical-limit"

    _SEMGATE07_INV_PM_PROMPT = (
        "I'm nervous about this plan to expand our molten-salt thermal storage system "
        "to a second site — before we finalize, invert the assumptions: what would "
        "have to be true for this expansion to go badly?"
    )
    _SEMGATE07_INV_PM_EXPECTED = "focused-pre-mortem"

    # Drift guard: hardcoded decompose↔five-whys literal must still match the live
    # catalog S-A01 row, OR the row must be absent (deletion is the survivable case).
    _sa01_catalog_prompt = next(
        (p for rid, p, _ in fixtures if rid == "S-A01"), None
    )
    if _sa01_catalog_prompt is not None and _sa01_catalog_prompt != _SEMGATE07_DECOMP_FW_PROMPT:
        print(
            "check-step0-emulator --self-test: SEMGATE-07 S-A01 FAIL "
            "(hardcoded decompose↔five-whys literal drifted from the live catalog S-A01 row — "
            "re-sync the literal or update the gate)"
        )
        wrong.append(
            f"SEMGATE-07 S-A01 (literal drifted from catalog row "
            f"{_sa01_catalog_prompt!r} != {_SEMGATE07_DECOMP_FW_PROMPT!r})"
        )

    # Drift guard: hardcoded theoretical-limit↔inversion literal must still match
    # the live catalog S-A03 row, OR the row must be absent.
    _sa03_catalog_prompt = next(
        (p for rid, p, _ in fixtures if rid == "S-A03"), None
    )
    if _sa03_catalog_prompt is not None and _sa03_catalog_prompt != _SEMGATE07_TL_INV_PROMPT:
        print(
            "check-step0-emulator --self-test: SEMGATE-07 S-A03 FAIL "
            "(hardcoded theoretical-limit↔inversion literal drifted from the live catalog S-A03 row — "
            "re-sync the literal or update the gate)"
        )
        wrong.append(
            f"SEMGATE-07 S-A03 (literal drifted from catalog row "
            f"{_sa03_catalog_prompt!r} != {_SEMGATE07_TL_INV_PROMPT!r})"
        )

    # Drift guard: hardcoded inversion↔pre-mortem literal must still match the live
    # catalog S-A05 row, OR the row must be absent.
    _sa05_catalog_prompt = next(
        (p for rid, p, _ in fixtures if rid == "S-A05"), None
    )
    if _sa05_catalog_prompt is not None and _sa05_catalog_prompt != _SEMGATE07_INV_PM_PROMPT:
        print(
            "check-step0-emulator --self-test: SEMGATE-07 S-A05 FAIL "
            "(hardcoded inversion↔pre-mortem literal drifted from the live catalog S-A05 row — "
            "re-sync the literal or update the gate)"
        )
        wrong.append(
            f"SEMGATE-07 S-A05 (literal drifted from catalog row "
            f"{_sa05_catalog_prompt!r} != {_SEMGATE07_INV_PM_PROMPT!r})"
        )

    semgate07_decomp_fw_computed = classify(_SEMGATE07_DECOMP_FW_PROMPT, rules)
    if semgate07_decomp_fw_computed == _SEMGATE07_DECOMP_FW_EXPECTED:
        print(
            "check-step0-emulator --self-test: SEMGATE-07 S-A01 PASS "
            f"(decompose↔five-whys co-fire → {semgate07_decomp_fw_computed})"
        )
    else:
        print(
            f"check-step0-emulator --self-test: SEMGATE-07 S-A01 FAIL "
            f"(expected {_SEMGATE07_DECOMP_FW_EXPECTED!r}, got {semgate07_decomp_fw_computed!r}; "
            f"pair: decompose↔five-whys; regression: five-whys may be above decompose in row order)"
        )
        wrong.append(
            f"SEMGATE-07 S-A01 (expected {_SEMGATE07_DECOMP_FW_EXPECTED!r}, got {semgate07_decomp_fw_computed!r})"
        )

    semgate07_tl_inv_computed = classify(_SEMGATE07_TL_INV_PROMPT, rules)
    if semgate07_tl_inv_computed == _SEMGATE07_TL_INV_EXPECTED:
        print(
            "check-step0-emulator --self-test: SEMGATE-07 S-A03 PASS "
            f"(theoretical-limit↔inversion co-fire → {semgate07_tl_inv_computed})"
        )
    else:
        print(
            f"check-step0-emulator --self-test: SEMGATE-07 S-A03 FAIL "
            f"(expected {_SEMGATE07_TL_INV_EXPECTED!r}, got {semgate07_tl_inv_computed!r}; "
            f"pair: theoretical-limit↔inversion; regression: inversion may be above theoretical-limit in row order)"
        )
        wrong.append(
            f"SEMGATE-07 S-A03 (expected {_SEMGATE07_TL_INV_EXPECTED!r}, got {semgate07_tl_inv_computed!r})"
        )

    semgate07_inv_pm_computed = classify(_SEMGATE07_INV_PM_PROMPT, rules)
    if semgate07_inv_pm_computed == _SEMGATE07_INV_PM_EXPECTED:
        print(
            "check-step0-emulator --self-test: SEMGATE-07 S-A05 PASS "
            f"(inversion↔pre-mortem co-fire → {semgate07_inv_pm_computed})"
        )
    else:
        print(
            f"check-step0-emulator --self-test: SEMGATE-07 S-A05 FAIL "
            f"(expected {_SEMGATE07_INV_PM_EXPECTED!r}, got {semgate07_inv_pm_computed!r}; "
            f"pair: inversion↔pre-mortem; regression: pre-mortem may have moved below inversion in row order)"
        )
        wrong.append(
            f"SEMGATE-07 S-A05 (expected {_SEMGATE07_INV_PM_EXPECTED!r}, got {semgate07_inv_pm_computed!r})"
        )

    # -----------------------------------------------------------------------
    # Category 7 (continued): All-9-coverage assertion (D-09)
    #
    # Confirms that every technique in KNOWN_TECHNIQUES has at least one positive
    # catalog fixture (expected_mode == f"focused-{technique}") so the Phase 108
    # live re-baseline harness (check-step0-live.py --catalog) is re-baseline-ready
    # across all 9 techniques.  This is a confirm-don't-expand check (D-09):
    # we verify the existing catalog covers all 9, not author new fixtures.
    # -----------------------------------------------------------------------

    covered_techniques = {
        mode.removeprefix("focused-")
        for _, _, mode in fixtures
        if mode.startswith("focused-")
    }
    for technique in KNOWN_TECHNIQUES:
        if technique not in covered_techniques:
            print(
                f"check-step0-emulator --self-test: SEMGATE-07 all-9-coverage FAIL "
                f"(technique '{technique}' has no positive catalog fixture with "
                f"expected_mode='focused-{technique}' — catalog is not re-baseline-ready "
                f"for this technique)"
            )
            wrong.append(
                f"SEMGATE-07 all-9-coverage (technique '{technique}' uncovered)"
            )
        else:
            print(
                f"check-step0-emulator --self-test: SEMGATE-07 all-9-coverage PASS "
                f"(technique '{technique}' has >=1 positive catalog fixture)"
            )

    # -----------------------------------------------------------------------
    # Category 7 (continued): VAL-04 complementarity assertion (GT-6)
    #
    # GT-6: check-trigger-collisions.py (VAL-04) scans skill description text
    # for lexical 4-gram collisions between skill names.  It is structurally
    # blind to the Step 0 phrase table: it never reads SKILL-body.md and cannot
    # detect that two technique rows share a common trigger phrase.  SEMGATE
    # fills this gap.
    #
    # Assertion: the S-A01 co-fire literal (decompose↔five-whys) classifies
    # to focused-decompose — a semantic-overlap case that VAL-04 cannot detect
    # because: (a) VAL-04 scans description text, not phrase-table rows, and
    # (b) even if it found a collision, it would not know which row-ORDER wins.
    # The assertion above (SEMGATE-07 S-A01) already proved this.  The comment
    # below makes the GT-6 complementarity explicit and findable.
    #
    # Complementarity summary:
    #   VAL-04 asks: "do two skills share a 4-gram in their descriptions?"
    #   SEMGATE asks: "when two phrase-table rows BOTH fire on the same prompt,
    #                  does first-row-wins return the INTENDED winner?"
    # These are orthogonal checks — VAL-04 never reads the phrase table, so a
    # row-order regression is CI-invisible to VAL-04.  SEMGATE-07 is the only
    # CI gate that catches it.
    # -----------------------------------------------------------------------

    # VAL-04 complementarity is demonstrated by the SEMGATE-07 S-A01 assertion
    # above: the co-fire literal was classified to focused-decompose by classify()
    # using the post-reorder phrase table.  The classify() call uses SKILL-body.md
    # row order — information VAL-04 never accesses.  No additional runtime check
    # is needed here; the assertion is already recorded in the wrong[] list if it
    # failed.  The comment above satisfies the GT-6 documentation requirement.

    # -----------------------------------------------------------------------
    # Final verdict
    # -----------------------------------------------------------------------

    if wrong:
        sys.stderr.write(
            f"check-step0-emulator --self-test: FAIL — "
            f"{', '.join(wrong)}\n"
        )
        sys.exit(1)

    print(f"check-step0-emulator --self-test: PASS — {len(fixtures)} fixtures + RR-80-01 + DECOMP-07 + ESTIMATE-07 + TLIMIT-07 + SEMGATE-07 named assertions")


def _require_python_version() -> None:
    if sys.version_info < (3, 12):
        sys.stderr.write(
            f"scripts/check-step0-emulator.py requires Python >=3.12 "
            f"(running {sys.version_info.major}.{sys.version_info.minor}).\n"
        )
        sys.exit(2)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "STEP0-01/02/03 offline emulator: classify prompt → MODE using the "
            "phrase-detection table from shared/spine/SKILL-body.md."
        )
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help=(
            "run fault-injection fixtures (D-05) and catalog classification fixtures; "
            "exits 0 if all pass, 1 on any failure. No live claude session required."
        ),
    )
    parser.add_argument(
        "--prompt",
        metavar="TEXT",
        default=None,
        help="classify a single prompt string and print the MODE",
    )
    # Internal flag used by --self-test subprocess: parse a given table file and exit
    parser.add_argument(
        "--_parse-table-test",
        metavar="PATH",
        default=None,
        dest="parse_table_test",
        help=argparse.SUPPRESS,
    )
    args = parser.parse_args()

    _require_python_version()

    if args.parse_table_test:
        # Used internally by _run_self_test fault-injection subprocess calls
        _parse_phrase_table(Path(args.parse_table_test))
        sys.exit(0)

    if args.self_test:
        _run_self_test()
        return

    if args.prompt is not None:
        if not SKILL_BODY.exists():
            sys.stderr.write(
                f"check-step0-emulator: canonical source not found: {SKILL_BODY}\n"
            )
            sys.exit(2)
        rules = _parse_phrase_table(SKILL_BODY)
        mode = classify(args.prompt, rules)
        print(mode)
        return

    parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
