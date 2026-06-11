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
import re
import subprocess
import sys
from pathlib import Path


REPO_ROOT: Path = Path(__file__).resolve().parents[1]

# Canonical source — always read from shared/, never from the generated tree.
# Pitfall 1: do NOT read first-principles/agents/first-principles.md (generated output).
SKILL_BODY: Path = REPO_ROOT / "shared" / "spine" / "SKILL-body.md"
CATALOG_PATH: Path = REPO_ROOT / "tests" / "step0-fixture-catalog.md"

# D-06: hardcoded allowlist — intentional second source of truth.
# Do NOT derive this from the parsed table: the independence is what makes
# D-05.3 actually catch renames/typos in the table.
KNOWN_TECHNIQUES = ("pre-mortem", "inversion", "fishbone", "five-whys", "trade-off", "second-order")


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


def _parse_table_rows(lines: list[str]) -> list[list[str]]:
    """Parse markdown pipe-table data rows, skipping header and separator lines.

    Stops at the first non-pipe-prefixed line (table has ended).
    Returns a list of cell lists (one inner list per data row).
    """
    rows: list[list[str]] = []
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("|"):
            break  # table ended
        # Skip separator rows like |---|---|
        inner = stripped.replace("|", "").replace("-", "").replace(" ", "")
        if not inner or set(inner) <= set("-"):
            continue
        # Split on | and strip each cell; drop empty leading/trailing entries
        cells = [c.strip() for c in stripped.split("|")]
        cells = [c for c in cells if c != ""]
        if cells:
            rows.append(cells)
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
    for row in data_rows:
        if len(row) < 2:
            sys.stderr.write(
                "check-step0-emulator: FAIL — phrase detection table: "
                f"malformed row (expected 2 cells, got {len(row)}): {row!r}\n"
            )
            sys.exit(1)

        technique = row[0]
        cell = row[1]

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
    """
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
    for row in data_rows:
        if len(row) < 3:
            sys.stderr.write(
                f"check-step0-emulator: FAIL — malformed catalog row "
                f"(expected >=3 cells, got {len(row)}): {row!r}\n"
            )
            sys.exit(1)
        row_id, prompt, expected_mode = row[0], row[1], row[2]
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
        import tempfile
        import os
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
    # Final verdict
    # -----------------------------------------------------------------------

    if wrong:
        sys.stderr.write(
            f"check-step0-emulator --self-test: FAIL — "
            f"{', '.join(wrong)}\n"
        )
        sys.exit(1)

    print("check-step0-emulator --self-test: PASS")


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
