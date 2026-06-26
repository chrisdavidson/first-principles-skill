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
# Phase 110 merged decompose into five-whys; Phase 111 removes it here (9→8).
KNOWN_TECHNIQUES = ("pre-mortem", "inversion", "fishbone", "five-whys", "trade-off", "second-order", "estimate", "theoretical-limit")


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


def _parse_phrase_table(path: Path) -> list[tuple[str, list[re.Pattern[str]], list[re.Pattern[str]]]]:
    """Parse the phrase-detection table from the canonical SKILL-body.md source.

    Returns a list of ``(technique, [compiled_trigger_regex, ...], [compiled_guard_regex, ...])``
    3-tuples in declaration order (first-row-wins precedence, D-04).  The third
    element is an empty list when the guard cell is absent or empty (no-guard default).

    Exits non-zero with a loud error message on any of the D-05 modes:
      D-05.1 — anchor ``**Phrase detection rules**`` not found
      D-05.2 — zero technique rows parsed, or a row has an empty trigger cell
      D-05.3 — a technique name is not in KNOWN_TECHNIQUES
      D-05.4 — a quoted phrase fails re.compile (caught at load time)
      D-05.5 — guard cell has an unbalanced quote (WR-03 applied to guard cell too)
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

    rules: list[tuple[str, list[re.Pattern[str]], list[re.Pattern[str]]]] = []
    for technique, remainder in data_rows:
        # Split remainder into trigger cell and guard cell.
        # _parse_table_rows strips the leading '|' and splits on the FIRST interior
        # pipe, so remainder is: " trigger_cell | guard_cell |"  (3-column row)
        # or just: " trigger_cell |" (ragged 2-column row, older format).
        # Use rsplit("|", 2) to split off the trailing empty part and the guard cell:
        #   3-column: [trigger, guard, ""]  (3 parts)
        #   2-column ragged: [trigger, ""]  (2 parts — D-G: graceful no-guard)
        # D-G: a ragged row missing the guard column is treated as no-guard (graceful
        # default) rather than a loud failure. This is intentional: the guard column
        # is additive and a 2-column table is a valid older format.  Loud failure is
        # reserved for the guard cell *content* being malformed (D-05.5 unbalanced
        # quote), not for the column being absent.
        parts = remainder.rsplit("|", 2)
        if len(parts) >= 3:
            trigger_cell = parts[0]
            guard_cell = parts[1]
        else:
            # Ragged row: no guard column — treat as empty guard (D-G default)
            trigger_cell = parts[0] if parts else remainder
            guard_cell = ""

        cell = trigger_cell  # alias for backward-compat error messages below

        # WR-03: balanced-quote guard on trigger cell — an odd number of '"' means
        # the cell has an unterminated quoted phrase (D-05-class corruption).
        # Fail loudly rather than silently extracting a partial phrase list.
        if cell.count('"') % 2 != 0:
            sys.stderr.write(
                f"check-step0-emulator: FAIL — technique '{technique}' phrase cell "
                f"has an unbalanced quote (possible pipe-split corruption): {cell!r}\n"
            )
            sys.exit(1)

        # D-05.2: empty trigger pattern cell
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

        # D-05.4: uncompilable regex in trigger cell — caught at load time, not per-prompt
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

        # D-05.5: WR-03 balanced-quote guard on guard cell
        if guard_cell.count('"') % 2 != 0:
            sys.stderr.write(
                f"check-step0-emulator: FAIL — technique '{technique}' guard cell "
                f"has an unbalanced quote (possible pipe-split corruption): {guard_cell!r}\n"
            )
            sys.exit(1)

        # Compile guard phrases (empty cell → empty list = no guard)
        guard_phrases = _extract_phrases(guard_cell)
        compiled_guard: list[re.Pattern[str]] = []
        for phrase in guard_phrases:
            try:
                compiled_guard.append(re.compile(phrase, re.IGNORECASE))
            except re.error as exc:
                sys.stderr.write(
                    f"check-step0-emulator: FAIL — technique '{technique}' "
                    f"guard phrase {phrase!r} is not a valid Python regex: {exc}\n"
                )
                sys.exit(1)

        rules.append((technique, compiled, compiled_guard))

    return rules


# ---------------------------------------------------------------------------
# Classifier
# ---------------------------------------------------------------------------

def classify(prompt: str, rules: list[tuple[str, list[re.Pattern[str]], list[re.Pattern[str]]]]) -> str:
    """Classify a prompt string to a MODE.

    Iterates rules in declaration order (D-04, first-row-wins). Returns
    ``f"focused-{technique}"`` for the first technique whose any compiled
    trigger pattern fires AND no guard phrase fires. Returns ``"full-composer"``
    if no unguarded trigger fires (D-04 default).

    Guard suppression (D-B/FIX-03): when a trigger fires but any guard phrase
    also matches, the trigger is suppressed via ``break`` (drops to the next
    technique in declaration order without returning).  This preserves
    first-trigger-wins and the full-composer default — later techniques can
    still fire if the guard only suppresses this one.
    """
    for technique, patterns, guard_patterns in rules:
        for pattern in patterns:
            if pattern.search(prompt):
                # Guard suppression: if any guard phrase matches, skip this technique
                if any(g.search(prompt) for g in guard_patterns):
                    break  # trigger fired but guard suppresses — try next technique
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
        # D-05.5: guard cell with unbalanced quote (D-G / WR-03 applied to guard cell)
        # A 3-column row where the guard cell has an odd number of '"' → loud failure.
        (
            "D-05.5 guard-unbalanced-quote",
            "**Phrase detection rules** (case-insensitive)\n"
            "\n"
            "| Technique | Trigger phrases (any one fires) | Guard phrases (suppress if any fires) |\n"
            "|---|---|---|\n"
            '| pre-mortem | "pre-mortem" | "unmatched quote |\n',
            "unbalanced quote",
        ),
        # D-05.6: ragged row missing the guard cell in a 3-column table (D-G)
        # A 2-cell row where the table has a 3-column header → graceful no-guard parse
        # (the D-G locked behavior: treat as empty guard, not a loud failure).
        # This fixture must NOT appear in the fault_fixtures list (which expects non-zero exit).
        # It is tested separately below as a graceful-parse assertion.
    ]

    # D-05.6: ragged-row-no-guard — a 2-cell row in a 3-column table must parse
    # gracefully as no-guard (D-G locked behavior: graceful, not loud failure).
    # Unlike D-05.1–D-05.5, D-05.6 expects exit 0 (graceful), so it is NOT in
    # fault_fixtures (which expects non-zero exit).  It is tested via a subprocess
    # parse that must succeed and produce a rules list.
    _dg_ragged_text = (
        "**Phrase detection rules** (case-insensitive)\n"
        "\n"
        "| Technique | Trigger phrases (any one fires) | Guard phrases (suppress if any fires) |\n"
        "|---|---|---|\n"
        '| pre-mortem | "pre-mortem" |\n'  # only 2 cells — ragged row, no guard cell
    )
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(_dg_ragged_text)
        _dg_ragged_path = tmp.name

    try:
        _dg_result = subprocess.run(
            [
                sys.executable,
                str(Path(__file__).resolve()),
                "--_parse-table-test",
                _dg_ragged_path,
            ],
            capture_output=True,
            text=True,
        )
        _dg_exit_code = _dg_result.returncode
    finally:
        os.unlink(_dg_ragged_path)

    if _dg_exit_code == 0:
        print(
            "check-step0-emulator --self-test: D-05.6 ragged-row-no-guard PASS "
            "(2-cell row in 3-column table parsed gracefully as no-guard)"
        )
    else:
        print(
            f"check-step0-emulator --self-test: D-05.6 ragged-row-no-guard FAIL "
            f"(expected exit 0 / graceful no-guard, got exit {_dg_exit_code}; "
            f"stderr: {_dg_result.stderr.strip()!r})"
        )
        wrong.append("D-05.6 ragged-row-no-guard (expected graceful parse, got non-zero exit)")

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
    # Category 4: FIVEWHYS-ABSORB named emulator assertions (D-02 / D-04)
    #
    # Phase 110 merged the decompose technique into five-whys; Phase 111
    # renamed this block from the prior decompose-named block to FIVEWHYS-ABSORB
    # to reflect that these assertions now verify absorbed-phrase routing to
    # five-whys, not a standalone decompose technique.
    #
    # Two catalog-independent hardcoded assertions that lock in absorbed-phrase
    # routing behavior:
    #   (a) A positive prompt fires the absorbed reduce-to-primitives trigger
    #       (decompose (this )?(claim|into primitives)) → focused-five-whys.
    #       The prompt contains the generic verb "decompose" but the trigger
    #       is now owned by the merged five-whys row in the phrase table.
    #   (b) The WR-01 mis-route framing ("decompose this problem from first
    #       principles: …") does NOT fire any trigger → full-composer.
    #       This is the CI-invisible WR-01 guard: check-trigger-collisions.py
    #       scans only skill descriptions, never the Step 0 phrase table, so
    #       this hardcoded assertion is the only CI gate that catches a
    #       mis-route regression. The absorbed phrase requires "claim" or
    #       "into primitives", not "problem from first principles".
    # Both literals are catalog-independent (D-04): deleting S-P16 or S-N08
    # from step0-fixture-catalog.md cannot silently drop these gates.
    # -----------------------------------------------------------------------

    _FIVEWHYS_ABSORB_POS_PROMPT = (
        "decompose this claim: a molten-salt thermal storage system achieves "
        "85% round-trip electricity efficiency when paired with a combined-cycle "
        "gas turbine — the vendor has published test data from a pilot plant in "
        "the Atacama Desert"
    )
    _FIVEWHYS_ABSORB_POS_EXPECTED = "focused-five-whys"

    _FIVEWHYS_ABSORB_NEG_PROMPT = (
        "decompose this problem from first principles: a molten-salt thermal "
        "storage system achieves 85% round-trip electricity efficiency — "
        "walk me through how to approach this"
    )
    _FIVEWHYS_ABSORB_NEG_EXPECTED = "full-composer"

    # Drift guard: hardcoded positive literal must still match the live catalog
    # S-P16 row, OR the row must be absent.
    _sp16_catalog_prompt = next(
        (p for rid, p, _ in fixtures if rid == "S-P16"), None
    )
    if _sp16_catalog_prompt is not None and _sp16_catalog_prompt != _FIVEWHYS_ABSORB_POS_PROMPT:
        print(
            "check-step0-emulator --self-test: FIVEWHYS-ABSORB S-P16 FAIL "
            "(hardcoded positive literal drifted from the live catalog S-P16 row — re-sync "
            "the literal or update the gate)"
        )
        wrong.append(
            f"FIVEWHYS-ABSORB S-P16 (literal drifted from catalog row "
            f"{_sp16_catalog_prompt!r} != {_FIVEWHYS_ABSORB_POS_PROMPT!r})"
        )

    # Drift guard: hardcoded negative literal must still match the live catalog
    # S-N08 row, OR the row must be absent.
    _sn08_catalog_prompt = next(
        (p for rid, p, _ in fixtures if rid == "S-N08"), None
    )
    if _sn08_catalog_prompt is not None and _sn08_catalog_prompt != _FIVEWHYS_ABSORB_NEG_PROMPT:
        print(
            "check-step0-emulator --self-test: FIVEWHYS-ABSORB S-N08 FAIL "
            "(hardcoded negative literal drifted from the live catalog S-N08 row — re-sync "
            "the literal or update the gate)"
        )
        wrong.append(
            f"FIVEWHYS-ABSORB S-N08 (literal drifted from catalog row "
            f"{_sn08_catalog_prompt!r} != {_FIVEWHYS_ABSORB_NEG_PROMPT!r})"
        )

    fivewhys_absorb_pos_computed = classify(_FIVEWHYS_ABSORB_POS_PROMPT, rules)
    if fivewhys_absorb_pos_computed == _FIVEWHYS_ABSORB_POS_EXPECTED:
        print(
            "check-step0-emulator --self-test: FIVEWHYS-ABSORB S-P16 PASS "
            f"(absorbed reduce-to-primitives trigger → {fivewhys_absorb_pos_computed})"
        )
    else:
        print(
            f"check-step0-emulator --self-test: FIVEWHYS-ABSORB S-P16 FAIL "
            f"(expected {_FIVEWHYS_ABSORB_POS_EXPECTED!r}, got {fivewhys_absorb_pos_computed!r})"
        )
        wrong.append(
            f"FIVEWHYS-ABSORB S-P16 (expected {_FIVEWHYS_ABSORB_POS_EXPECTED!r}, got {fivewhys_absorb_pos_computed!r})"
        )

    fivewhys_absorb_neg_computed = classify(_FIVEWHYS_ABSORB_NEG_PROMPT, rules)
    if fivewhys_absorb_neg_computed == _FIVEWHYS_ABSORB_NEG_EXPECTED:
        print(
            "check-step0-emulator --self-test: FIVEWHYS-ABSORB S-N08 PASS "
            f"(WR-01 mis-route guard → {fivewhys_absorb_neg_computed})"
        )
    else:
        print(
            f"check-step0-emulator --self-test: FIVEWHYS-ABSORB S-N08 FAIL "
            f"(expected {_FIVEWHYS_ABSORB_NEG_EXPECTED!r}, got {fivewhys_absorb_neg_computed!r}; "
            f"WR-01 regression: mis-route prompt now fires a trigger)"
        )
        wrong.append(
            f"FIVEWHYS-ABSORB S-N08 (expected {_FIVEWHYS_ABSORB_NEG_EXPECTED!r}, got {fivewhys_absorb_neg_computed!r})"
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
    # (Plan 107-01 moved theoretical-limit above inversion; Phase 110 merged
    # decompose into five-whys — the formerly-separate decompose row no longer
    # exists; its absorbed triggers are now part of the five-whys row).
    # check-trigger-collisions.py (VAL-04) is structurally blind to this
    # disambiguation — it scans only skill description text, never the Step 0
    # phrase table — so this Category 7 block is the only CI gate that locks the
    # post-reorder intended winner for each pair (VAL-04 complementarity, GT-6).
    #
    # Pair 1: absorbed-decompose phrase vs. five-whys native phrase (S-A01)
    #   Both triggers fire within the merged five-whys row: the absorbed
    #   "decompose (this )?(claim|into primitives)" phrase fires on "decompose
    #   this claim"; the native "root cause" phrase fires on "root cause of the
    #   performance gap".  Since both are now owned by the same merged five-whys
    #   row, the co-fire resolves to focused-five-whys (first-row-wins within
    #   the same row is not applicable — the whole merged row routes to one
    #   technique).  This is an intra-merged-technique co-fire, not a
    #   cross-technique disambiguation.
    #   VAL-04 complementarity: a 4-gram collision scan on the SKILL-body text
    #   cannot detect this case — the classifier is phrase-table-aware, VAL-04
    #   is not.
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
    _SEMGATE07_DECOMP_FW_EXPECTED = "focused-five-whys"

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

    # Drift guard: hardcoded absorbed-decompose↔five-whys literal must still match
    # the live catalog S-A01 row, OR the row must be absent (deletion is the
    # survivable case — the hardcoded literal is what gets classified below).
    _sa01_catalog_prompt = next(
        (p for rid, p, _ in fixtures if rid == "S-A01"), None
    )
    if _sa01_catalog_prompt is not None and _sa01_catalog_prompt != _SEMGATE07_DECOMP_FW_PROMPT:
        print(
            "check-step0-emulator --self-test: SEMGATE-07 S-A01 FAIL "
            "(hardcoded absorbed-decompose-phrase literal drifted from the live catalog S-A01 row — "
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
            f"(absorbed-decompose-phrase + five-whys intra-merged co-fire → {semgate07_decomp_fw_computed})"
        )
    else:
        print(
            f"check-step0-emulator --self-test: SEMGATE-07 S-A01 FAIL "
            f"(expected {_SEMGATE07_DECOMP_FW_EXPECTED!r}, got {semgate07_decomp_fw_computed!r}; "
            f"absorbed-decompose-phrase and root-cause both owned by merged five-whys row — "
            f"regression: phrase table may have drifted from Phase 110 merge state)"
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
    # Category 7 (continued): All-8-coverage assertion (D-09)
    #
    # Confirms that every technique in KNOWN_TECHNIQUES has at least one positive
    # catalog fixture (expected_mode == f"focused-{technique}") so the live
    # re-baseline harness (check-step0-live.py --catalog) is re-baseline-ready
    # across all 8 surviving techniques (decompose removed in Phase 110/111).
    # This is a confirm-don't-expand check (D-09):
    # we verify the existing catalog covers all 8, not author new fixtures.
    # -----------------------------------------------------------------------

    covered_techniques = {
        mode.removeprefix("focused-")
        for _, _, mode in fixtures
        if mode.startswith("focused-")
    }
    for technique in KNOWN_TECHNIQUES:
        if technique not in covered_techniques:
            print(
                f"check-step0-emulator --self-test: SEMGATE-07 all-8-coverage FAIL "
                f"(technique '{technique}' has no positive catalog fixture with "
                f"expected_mode='focused-{technique}' — catalog is not re-baseline-ready "
                f"for this technique)"
            )
            wrong.append(
                f"SEMGATE-07 all-8-coverage (technique '{technique}' uncovered)"
            )
        else:
            print(
                f"check-step0-emulator --self-test: SEMGATE-07 all-8-coverage PASS "
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
    # Assertion: the S-A01 co-fire literal (absorbed-decompose-phrase + five-whys
    # native phrase) classifies to focused-five-whys — a semantic-overlap case
    # that VAL-04 cannot detect because: (a) VAL-04 scans description text, not
    # phrase-table rows, and (b) even if it found a collision, it would not know
    # which row-ORDER wins (or, after the Phase 110 merge, that both phrases are
    # now owned by the same row).
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
    # above: the co-fire literal was classified to focused-five-whys by classify()
    # using the post-Phase-110-merge phrase table.  The classify() call uses
    # SKILL-body.md row order — information VAL-04 never accesses.  No additional
    # runtime check is needed here; the assertion is already recorded in the
    # wrong[] list if it failed.  The comment above satisfies the GT-6
    # documentation requirement.

    # -----------------------------------------------------------------------
    # Category 8: FIX01-LOCK named emulator assertions (FIX-01 / D-04 / D-11)
    #
    # Two catalog-independent hardcoded positive-lock assertions (modelled on
    # FIVEWHYS-ABSORB) that prove the augmented phrase table (Phase 117 FIX-01)
    # still routes S-P01 and S-P03 to their focused modes via the phrase
    # classifier.
    #
    # Motivation: FIX-01 added new trigger phrases to pre-mortem (row 30:
    # "structural weakness", "failure chain") and fishbone (row 33:
    # "candidate causes"). These additions make the _battery_core.py detector
    # more sensitive, but the STEP0-08 phrase-table classifier must still
    # route the *original* S-P01 and S-P03 prompts correctly — they contain
    # literal primary triggers ("pre-mortem" and "fishbone") so the expected
    # outcomes are unchanged. These assertions lock that invariant.
    #
    # Both literals are catalog-independent (D-04): deleting S-P01 or S-P03
    # from step0-fixture-catalog.md cannot silently drop these gates. Any
    # silent edit to a catalog row fails loudly via the drift guard below.
    # -----------------------------------------------------------------------

    _FIX01_LOCK_SP01_PROMPT = (
        "run a pre-mortem on this launch — we are shipping the payments-rewrite "
        "service to all EU customers next Friday, replacing the legacy stripe "
        "integration, with no staged rollout"
    )
    _FIX01_LOCK_SP01_EXPECTED = "focused-pre-mortem"

    _FIX01_LOCK_SP03_PROMPT = (
        "draw a fishbone diagram on the production incident — our checkout API "
        "returned 503 errors for 40 minutes starting 14:10 UTC yesterday, "
        "affecting all users; we have ruled out the database layer"
    )
    _FIX01_LOCK_SP03_EXPECTED = "focused-fishbone"

    # Drift guard: hardcoded S-P01 literal must still match the live catalog
    # S-P01 row, OR the row must be absent (deletion is the survivable case).
    _sp01_catalog_prompt = next(
        (p for rid, p, _ in fixtures if rid == "S-P01"), None
    )
    if _sp01_catalog_prompt is not None and _sp01_catalog_prompt != _FIX01_LOCK_SP01_PROMPT:
        print(
            "check-step0-emulator --self-test: FIX01-LOCK S-P01 FAIL "
            "(hardcoded S-P01 literal drifted from the live catalog S-P01 row — "
            "re-sync the literal or update the gate)"
        )
        wrong.append(
            f"FIX01-LOCK S-P01 (literal drifted from catalog row "
            f"{_sp01_catalog_prompt!r} != {_FIX01_LOCK_SP01_PROMPT!r})"
        )

    # Drift guard: hardcoded S-P03 literal must still match the live catalog
    # S-P03 row, OR the row must be absent.
    _sp03_catalog_prompt = next(
        (p for rid, p, _ in fixtures if rid == "S-P03"), None
    )
    if _sp03_catalog_prompt is not None and _sp03_catalog_prompt != _FIX01_LOCK_SP03_PROMPT:
        print(
            "check-step0-emulator --self-test: FIX01-LOCK S-P03 FAIL "
            "(hardcoded S-P03 literal drifted from the live catalog S-P03 row — "
            "re-sync the literal or update the gate)"
        )
        wrong.append(
            f"FIX01-LOCK S-P03 (literal drifted from catalog row "
            f"{_sp03_catalog_prompt!r} != {_FIX01_LOCK_SP03_PROMPT!r})"
        )

    fix01_lock_sp01_computed = classify(_FIX01_LOCK_SP01_PROMPT, rules)
    if fix01_lock_sp01_computed == _FIX01_LOCK_SP01_EXPECTED:
        print(
            "check-step0-emulator --self-test: FIX01-LOCK S-P01 PASS "
            f"(augmented pre-mortem trigger → {fix01_lock_sp01_computed})"
        )
    else:
        print(
            f"check-step0-emulator --self-test: FIX01-LOCK S-P01 FAIL "
            f"(expected {_FIX01_LOCK_SP01_EXPECTED!r}, got {fix01_lock_sp01_computed!r}; "
            f"FIX-01 regression: augmented pre-mortem row 30 no longer routes the "
            f"primary S-P01 trigger to focused-pre-mortem)"
        )
        wrong.append(
            f"FIX01-LOCK S-P01 (expected {_FIX01_LOCK_SP01_EXPECTED!r}, got {fix01_lock_sp01_computed!r})"
        )

    fix01_lock_sp03_computed = classify(_FIX01_LOCK_SP03_PROMPT, rules)
    if fix01_lock_sp03_computed == _FIX01_LOCK_SP03_EXPECTED:
        print(
            "check-step0-emulator --self-test: FIX01-LOCK S-P03 PASS "
            f"(augmented fishbone trigger → {fix01_lock_sp03_computed})"
        )
    else:
        print(
            f"check-step0-emulator --self-test: FIX01-LOCK S-P03 FAIL "
            f"(expected {_FIX01_LOCK_SP03_EXPECTED!r}, got {fix01_lock_sp03_computed!r}; "
            f"FIX-01 regression: augmented fishbone row 33 no longer routes the "
            f"primary S-P03 trigger to focused-fishbone)"
        )
        wrong.append(
            f"FIX01-LOCK S-P03 (expected {_FIX01_LOCK_SP03_EXPECTED!r}, got {fix01_lock_sp03_computed!r})"
        )

    # -----------------------------------------------------------------------
    # Category 6: PREMORTEM-GUARD + TIEBREAK-OBLIQUE + TIEBREAK-DECISIVE
    #   named emulator assertions (FIX-03 / FIX-04 / D-B / D-C / D-D)
    #
    # These three assertions lock the guard-suppression mechanism and the
    # stay-in-composer tiebreaker behavior introduced in Phase 118.
    #
    # PREMORTEM-GUARD (D-B / D-C):
    #   A synthetic prompt containing BOTH a literal pre-mortem trigger phrase
    #   AND an oblique guard phrase → expect full-composer (trigger suppressed).
    #   This is a catalog-INDEPENDENT synthetic fixture (no drift guard against
    #   catalog needed — no catalog row exists for this synthetic combo).
    #   Mirrors the RR-77-08 / Category-N synthetic-fixture idiom in _battery_core.py.
    #
    # TIEBREAK-OBLIQUE (D-D / FIX-04 prose lock):
    #   An oblique prompt with no trigger → full-composer.
    #   Confirms the tiebreaker prose: oblique worry-phrasing without a decisive
    #   trigger stays in full-composer at the emulator layer.
    #
    # TIEBREAK-DECISIVE (D-D / FIX-04 prose lock):
    #   A decisive trigger prompt → focused-<technique>.
    #   Confirms the tiebreaker does NOT suppress legitimate focused routes.
    # -----------------------------------------------------------------------

    # PREMORTEM-GUARD: trigger fires ("pre-mortem" literal) AND guard fires
    # ("before we lock it in" from the pre-mortem guard cell) → full-composer suppressed.
    _PREMORTEM_GUARD_PROMPT = (
        "run a pre-mortem on our API gateway redesign — before we lock it in, "
        "let's surface every risk the team might have missed"
    )
    _PREMORTEM_GUARD_EXPECTED = "full-composer"  # trigger fired, guard suppressed

    premortem_guard_computed = classify(_PREMORTEM_GUARD_PROMPT, rules)
    if premortem_guard_computed == _PREMORTEM_GUARD_EXPECTED:
        print(
            "check-step0-emulator --self-test: PREMORTEM-GUARD PASS "
            f"(pre-mortem trigger + guard phrase → {premortem_guard_computed})"
        )
    else:
        print(
            f"check-step0-emulator --self-test: PREMORTEM-GUARD FAIL "
            f"(expected {_PREMORTEM_GUARD_EXPECTED!r}, got {premortem_guard_computed!r}; "
            f"guard suppression not working: trigger fired but guard phrase did not suppress it)"
        )
        wrong.append(
            f"PREMORTEM-GUARD (expected {_PREMORTEM_GUARD_EXPECTED!r}, got {premortem_guard_computed!r})"
        )

    # TIEBREAK-OBLIQUE: oblique prompt, no trigger phrase → full-composer.
    # Uses the S-N01 oblique worry-phrasing (no literal trigger fires).
    _TIEBREAK_OBLIQUE_PROMPT = (
        "The plan looks solid and the team is excited, but I am nervous. "
        "Before we lock it in, I want to surface every way this could blow up."
    )
    _TIEBREAK_OBLIQUE_EXPECTED = "full-composer"

    tiebreak_oblique_computed = classify(_TIEBREAK_OBLIQUE_PROMPT, rules)
    if tiebreak_oblique_computed == _TIEBREAK_OBLIQUE_EXPECTED:
        print(
            "check-step0-emulator --self-test: TIEBREAK-OBLIQUE PASS "
            f"(oblique no-trigger prompt → {tiebreak_oblique_computed})"
        )
    else:
        print(
            f"check-step0-emulator --self-test: TIEBREAK-OBLIQUE FAIL "
            f"(expected {_TIEBREAK_OBLIQUE_EXPECTED!r}, got {tiebreak_oblique_computed!r}; "
            f"oblique worry-phrasing should not route to any focused mode)"
        )
        wrong.append(
            f"TIEBREAK-OBLIQUE (expected {_TIEBREAK_OBLIQUE_EXPECTED!r}, got {tiebreak_oblique_computed!r})"
        )

    # TIEBREAK-DECISIVE: decisive trigger prompt → focused-inversion.
    # Confirms the tiebreaker does NOT suppress legitimate focused routes:
    # a prompt with a clear decisive trigger ("invert this claim") must still route correctly.
    _TIEBREAK_DECISIVE_PROMPT = (
        "invert this claim: our deployment pipeline is reliable enough for daily releases"
    )
    _TIEBREAK_DECISIVE_EXPECTED = "focused-inversion"

    tiebreak_decisive_computed = classify(_TIEBREAK_DECISIVE_PROMPT, rules)
    if tiebreak_decisive_computed == _TIEBREAK_DECISIVE_EXPECTED:
        print(
            "check-step0-emulator --self-test: TIEBREAK-DECISIVE PASS "
            f"(decisive inversion trigger → {tiebreak_decisive_computed})"
        )
    else:
        print(
            f"check-step0-emulator --self-test: TIEBREAK-DECISIVE FAIL "
            f"(expected {_TIEBREAK_DECISIVE_EXPECTED!r}, got {tiebreak_decisive_computed!r}; "
            f"decisive triggers must still route to focused mode)"
        )
        wrong.append(
            f"TIEBREAK-DECISIVE (expected {_TIEBREAK_DECISIVE_EXPECTED!r}, got {tiebreak_decisive_computed!r})"
        )

    # -----------------------------------------------------------------------
    # Category 7: NEGCAT — guard-suppressed + no-decisive-trigger named assertions
    #
    # Phase 120 Fix #3: broaden the oblique-negative boundary coverage by adding
    # four individually-named guard-suppressed assertions (one per unexercised
    # pre-mortem guard phrase) and one catalog-coupled no-decisive-trigger
    # assertion.  These lock the v7.8 Fix #1 guard-suppression mechanism and
    # Fix #2 stay-in-composer tiebreaker against novel boundary prompts.
    #
    # NEGCAT-GUARD-1..4 (inline-synthetic, catalog-independent, D-04):
    #   Each assertion pairs a literal pre-mortem trigger with exactly one of
    #   the four previously-unexercised guard phrases, expects full-composer
    #   (guard suppresses the trigger), and includes an anti-vacuity counter-
    #   check (same trigger WITHOUT the guard phrase must route to focused-pre-
    #   mortem — proving the trigger is genuine and the full-composer result is
    #   caused by the guard, not by a missing trigger).
    #
    # NEGCAT-OBLIQUE (catalog-coupled, drift-guarded, RR-80-01/S-N04 idiom):
    #   Locks the no-decisive-trigger oblique catalog row S-N13. Hardcodes the
    #   literal and adds a drift guard so a silent catalog edit fails loudly.
    # -----------------------------------------------------------------------

    # NEGCAT-GUARD-1: trigger fires ("prospective-hindsight") AND guard fires
    # ("surface every way this could blow up") → full-composer suppressed.
    _NEGCAT_GUARD1_PROMPT = (
        "I need a prospective-hindsight on this deployment — "
        "surface every way this could blow up before we flip the switch"
    )
    _NEGCAT_GUARD1_EXPECTED = "full-composer"  # trigger fired, guard suppressed

    negcat_guard1_computed = classify(_NEGCAT_GUARD1_PROMPT, rules)
    if negcat_guard1_computed == _NEGCAT_GUARD1_EXPECTED:
        print(
            "check-step0-emulator --self-test: NEGCAT-GUARD-1 PASS "
            f"(pre-mortem trigger + guard 'surface every way this could blow up' → {negcat_guard1_computed})"
        )
    else:
        print(
            f"check-step0-emulator --self-test: NEGCAT-GUARD-1 FAIL "
            f"(expected {_NEGCAT_GUARD1_EXPECTED!r}, got {negcat_guard1_computed!r}; "
            f"guard suppression not working: guard phrase 'surface every way this could blow up' "
            f"did not suppress the pre-mortem trigger)"
        )
        wrong.append(
            f"NEGCAT-GUARD-1 (expected {_NEGCAT_GUARD1_EXPECTED!r}, got {negcat_guard1_computed!r})"
        )

    # Anti-vacuity counter-check: same trigger WITHOUT the guard phrase → focused-pre-mortem
    _NEGCAT_GUARD1_POSITIVE_PROMPT = (
        "I need a prospective-hindsight on this deployment — "
        "please enumerate the risks before we flip the switch"
    )
    negcat_guard1_positive_computed = classify(_NEGCAT_GUARD1_POSITIVE_PROMPT, rules)
    if negcat_guard1_positive_computed == "focused-pre-mortem":
        print(
            "check-step0-emulator --self-test: NEGCAT-GUARD-1-positive PASS "
            f"(pre-mortem trigger without guard phrase → {negcat_guard1_positive_computed})"
        )
    else:
        print(
            f"check-step0-emulator --self-test: NEGCAT-GUARD-1-positive FAIL "
            f"(expected 'focused-pre-mortem', got {negcat_guard1_positive_computed!r}; "
            f"anti-vacuity: the pre-mortem trigger must fire when guard phrase is absent)"
        )
        wrong.append(
            f"NEGCAT-GUARD-1-positive (expected 'focused-pre-mortem', got {negcat_guard1_positive_computed!r})"
        )

    # NEGCAT-GUARD-2: trigger fires (plan-nervousness alternation: "I'm nervous about this plan")
    # AND guard fires ("everything that would make it go wrong") → full-composer suppressed.
    _NEGCAT_GUARD2_PROMPT = (
        "I'm nervous about this plan to expand the data center — "
        "walk me through everything that would make it go wrong"
    )
    _NEGCAT_GUARD2_EXPECTED = "full-composer"  # trigger fired, guard suppressed

    negcat_guard2_computed = classify(_NEGCAT_GUARD2_PROMPT, rules)
    if negcat_guard2_computed == _NEGCAT_GUARD2_EXPECTED:
        print(
            "check-step0-emulator --self-test: NEGCAT-GUARD-2 PASS "
            f"(pre-mortem trigger + guard 'everything that would make it go wrong' → {negcat_guard2_computed})"
        )
    else:
        print(
            f"check-step0-emulator --self-test: NEGCAT-GUARD-2 FAIL "
            f"(expected {_NEGCAT_GUARD2_EXPECTED!r}, got {negcat_guard2_computed!r}; "
            f"guard suppression not working: guard phrase 'everything that would make it go wrong' "
            f"did not suppress the pre-mortem trigger)"
        )
        wrong.append(
            f"NEGCAT-GUARD-2 (expected {_NEGCAT_GUARD2_EXPECTED!r}, got {negcat_guard2_computed!r})"
        )

    # Anti-vacuity counter-check
    _NEGCAT_GUARD2_POSITIVE_PROMPT = (
        "I'm nervous about this plan to expand the data center — "
        "walk me through the main risk factors"
    )
    negcat_guard2_positive_computed = classify(_NEGCAT_GUARD2_POSITIVE_PROMPT, rules)
    if negcat_guard2_positive_computed == "focused-pre-mortem":
        print(
            "check-step0-emulator --self-test: NEGCAT-GUARD-2-positive PASS "
            f"(pre-mortem trigger without guard phrase → {negcat_guard2_positive_computed})"
        )
    else:
        print(
            f"check-step0-emulator --self-test: NEGCAT-GUARD-2-positive FAIL "
            f"(expected 'focused-pre-mortem', got {negcat_guard2_positive_computed!r}; "
            f"anti-vacuity: the pre-mortem trigger must fire when guard phrase is absent)"
        )
        wrong.append(
            f"NEGCAT-GUARD-2-positive (expected 'focused-pre-mortem', got {negcat_guard2_positive_computed!r})"
        )

    # NEGCAT-GUARD-3: trigger fires ("pre-mortem" literal) AND guard fires
    # ("what failure modes should we prepare for") → full-composer suppressed.
    _NEGCAT_GUARD3_PROMPT = (
        "run a pre-mortem on the new CI pipeline — "
        "what failure modes should we prepare for before we enable auto-merge"
    )
    _NEGCAT_GUARD3_EXPECTED = "full-composer"  # trigger fired, guard suppressed

    negcat_guard3_computed = classify(_NEGCAT_GUARD3_PROMPT, rules)
    if negcat_guard3_computed == _NEGCAT_GUARD3_EXPECTED:
        print(
            "check-step0-emulator --self-test: NEGCAT-GUARD-3 PASS "
            f"(pre-mortem trigger + guard 'what failure modes should we prepare for' → {negcat_guard3_computed})"
        )
    else:
        print(
            f"check-step0-emulator --self-test: NEGCAT-GUARD-3 FAIL "
            f"(expected {_NEGCAT_GUARD3_EXPECTED!r}, got {negcat_guard3_computed!r}; "
            f"guard suppression not working: guard phrase 'what failure modes should we prepare for' "
            f"did not suppress the pre-mortem trigger)"
        )
        wrong.append(
            f"NEGCAT-GUARD-3 (expected {_NEGCAT_GUARD3_EXPECTED!r}, got {negcat_guard3_computed!r})"
        )

    # Anti-vacuity counter-check
    _NEGCAT_GUARD3_POSITIVE_PROMPT = (
        "run a pre-mortem on the new CI pipeline before we enable auto-merge"
    )
    negcat_guard3_positive_computed = classify(_NEGCAT_GUARD3_POSITIVE_PROMPT, rules)
    if negcat_guard3_positive_computed == "focused-pre-mortem":
        print(
            "check-step0-emulator --self-test: NEGCAT-GUARD-3-positive PASS "
            f"(pre-mortem trigger without guard phrase → {negcat_guard3_positive_computed})"
        )
    else:
        print(
            f"check-step0-emulator --self-test: NEGCAT-GUARD-3-positive FAIL "
            f"(expected 'focused-pre-mortem', got {negcat_guard3_positive_computed!r}; "
            f"anti-vacuity: the pre-mortem trigger must fire when guard phrase is absent)"
        )
        wrong.append(
            f"NEGCAT-GUARD-3-positive (expected 'focused-pre-mortem', got {negcat_guard3_positive_computed!r})"
        )

    # NEGCAT-GUARD-4: trigger fires ("failure chain") AND guard fires
    # ("how this could go badly") → full-composer suppressed.
    _NEGCAT_GUARD4_PROMPT = (
        "there is a failure chain risk in the handoff protocol — "
        "walk me through how this could go badly in the production environment"
    )
    _NEGCAT_GUARD4_EXPECTED = "full-composer"  # trigger fired, guard suppressed

    negcat_guard4_computed = classify(_NEGCAT_GUARD4_PROMPT, rules)
    if negcat_guard4_computed == _NEGCAT_GUARD4_EXPECTED:
        print(
            "check-step0-emulator --self-test: NEGCAT-GUARD-4 PASS "
            f"(pre-mortem trigger + guard 'how this could go badly' → {negcat_guard4_computed})"
        )
    else:
        print(
            f"check-step0-emulator --self-test: NEGCAT-GUARD-4 FAIL "
            f"(expected {_NEGCAT_GUARD4_EXPECTED!r}, got {negcat_guard4_computed!r}; "
            f"guard suppression not working: guard phrase 'how this could go badly' "
            f"did not suppress the pre-mortem trigger)"
        )
        wrong.append(
            f"NEGCAT-GUARD-4 (expected {_NEGCAT_GUARD4_EXPECTED!r}, got {negcat_guard4_computed!r})"
        )

    # Anti-vacuity counter-check
    _NEGCAT_GUARD4_POSITIVE_PROMPT = (
        "there is a failure chain risk in the handoff protocol — "
        "walk me through the main concerns for production"
    )
    negcat_guard4_positive_computed = classify(_NEGCAT_GUARD4_POSITIVE_PROMPT, rules)
    if negcat_guard4_positive_computed == "focused-pre-mortem":
        print(
            "check-step0-emulator --self-test: NEGCAT-GUARD-4-positive PASS "
            f"(pre-mortem trigger without guard phrase → {negcat_guard4_positive_computed})"
        )
    else:
        print(
            f"check-step0-emulator --self-test: NEGCAT-GUARD-4-positive FAIL "
            f"(expected 'focused-pre-mortem', got {negcat_guard4_positive_computed!r}; "
            f"anti-vacuity: the pre-mortem trigger must fire when guard phrase is absent)"
        )
        wrong.append(
            f"NEGCAT-GUARD-4-positive (expected 'focused-pre-mortem', got {negcat_guard4_positive_computed!r})"
        )

    # NEGCAT-OBLIQUE: catalog-coupled drift-guarded no-decisive-trigger assertion.
    # Hardcodes the S-N13 literal (oblique worry-phrasing, no trigger phrase fires).
    # Mirrors the RR-80-01/S-N04 idiom (Category 3, lines 559–613): the hardcoded
    # literal is what gets classified (catalog-independent per D-04), while the drift
    # guard ensures a silent catalog edit fails loudly instead of leaving the gate
    # testing a stale prompt.
    _NEGCAT_OBLIQUE_PROMPT = (
        "I have a nagging feeling the molten-salt thermal storage upgrade might unravel "
        "— can we do a sanity check on the project assumptions before the design review?"
    )
    _NEGCAT_OBLIQUE_EXPECTED = "full-composer"

    # Drift guard: hardcoded literal must still match the live S-N13 catalog row (or be absent)
    _sn13_catalog_prompt = next(
        (p for rid, p, _ in fixtures if rid == "S-N13"), None
    )
    if _sn13_catalog_prompt is not None and _sn13_catalog_prompt != _NEGCAT_OBLIQUE_PROMPT:
        print(
            "check-step0-emulator --self-test: NEGCAT-OBLIQUE FAIL "
            "(hardcoded literal drifted from the live catalog S-N13 row — re-sync "
            "the literal or update the gate)"
        )
        wrong.append(
            "NEGCAT-OBLIQUE S-N13 (literal drifted from catalog row "
            f"{_sn13_catalog_prompt!r} != {_NEGCAT_OBLIQUE_PROMPT!r})"
        )

    negcat_oblique_computed = classify(_NEGCAT_OBLIQUE_PROMPT, rules)
    if negcat_oblique_computed == _NEGCAT_OBLIQUE_EXPECTED:
        print(
            "check-step0-emulator --self-test: NEGCAT-OBLIQUE PASS "
            f"(oblique no-trigger worry-phrasing S-N13 → {negcat_oblique_computed})"
        )
    else:
        print(
            f"check-step0-emulator --self-test: NEGCAT-OBLIQUE FAIL "
            f"(expected {_NEGCAT_OBLIQUE_EXPECTED!r}, got {negcat_oblique_computed!r}; "
            f"oblique no-trigger prompt should not route to any focused mode)"
        )
        wrong.append(
            f"NEGCAT-OBLIQUE (expected {_NEGCAT_OBLIQUE_EXPECTED!r}, got {negcat_oblique_computed!r})"
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

    print(f"check-step0-emulator --self-test: PASS — {len(fixtures)} fixtures + RR-80-01 + FIVEWHYS-ABSORB + ESTIMATE-07 + TLIMIT-07 + SEMGATE-07 + FIX01-LOCK + PREMORTEM-GUARD + TIEBREAK-OBLIQUE + TIEBREAK-DECISIVE + NEGCAT-GUARD-1 + NEGCAT-GUARD-2 + NEGCAT-GUARD-3 + NEGCAT-GUARD-4 + NEGCAT-OBLIQUE named assertions")


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
