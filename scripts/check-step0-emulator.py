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
KNOWN_TECHNIQUES = ("pre-mortem", "inversion", "fishbone", "five-whys", "trade-off", "second-order", "decompose")


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
    # Final verdict
    # -----------------------------------------------------------------------

    if wrong:
        sys.stderr.write(
            f"check-step0-emulator --self-test: FAIL — "
            f"{', '.join(wrong)}\n"
        )
        sys.exit(1)

    print(f"check-step0-emulator --self-test: PASS — {len(fixtures)} fixtures + RR-80-01 + DECOMP-07 named assertions")


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
