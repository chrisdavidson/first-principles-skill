#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Merged dual-signal routing battery entry point (D-07, BATT-02/03/04).

This script is the single battery that replaces the two separate batteries
(`check-sub-skill-routing.py` and `check-focused-output.py`). It:

  - Captures each prompt in `tests/routing-battery-catalog.md` EXACTLY ONCE
    per run (one .jsonl file per prompt, shared by both detectors — BATT-02).
  - Scores BOTH the boundary signal (detect_subskill) AND the focused-output
    classifier (detect_output_structure_from_file) from the SAME .jsonl file
    (BATT-03).
  - Applies a both-match verdict per prompt: a prompt passes only when BOTH
    signals match their respective expectations. `n-a` on either side
    auto-passes that side (D-02 reduce-to-single-signal behavior).
  - Emits TWO K-of-N tally sections (--- Boundary signal --- / --- Focused
    output ---) plus an --- Overall --- section in the locked format that
    Phase 69 invariant tests will parse (D-06).
  - Exposes FOUR namespaced threshold flags with defaults that reproduce the
    two source scripts' exact verdicts (BATT-04, D-04):
        --boundary-p-threshold  default 2  (from check-sub-skill-routing.py)
        --boundary-n-threshold  default 2  (from check-sub-skill-routing.py)
        --focused-p-threshold   default 4  (from check-focused-output.py)
        --focused-n-threshold   default 1  (from check-focused-output.py)

## D-04 Resolution (boundary n-threshold)

CONTEXT.md D-04 says "Boundary has no n-threshold (its catalog has no
inverted-expectation rows)." Resolved by reading check-sub-skill-routing.py:
  - `build_parser` defines `--n-threshold` with default 2.
  - `run_battery` gates with `n_pass >= n_threshold`.
  - The boundary catalog HAS N rows (B-N1, B-N2), both expecting `none-or-other`.
  - Removing the n-threshold gate would change verdicts for any run where an N
    row fails.
Decision: RETAIN `--boundary-n-threshold` with default 2. The verbatim-verdict
principle (CONTEXT.md) overrides D-04's literal wording. D-04's "no n-threshold"
means "no INVERTED-expectation N rows" (like focused N1's NOT-any-focused), NOT
that N rows or the gate are absent.

## Import convention

`scripts/` has NO `__init__.py`; `from scripts._battery_core import ...` fails.
We use the established repo convention (see tests/test_60_01_check_agent_candidate.py
and tests/test_64_01_install.py): insert the scripts/ dir at the front of sys.path,
then `import _battery_core`. This is identical to the test-convention used across
the repo for sibling-script loading.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Shared-module import — no-package convention for scripts/
# (scripts/ has no __init__.py; `from scripts._battery_core import ...` fails)
# This mirrors the established repo test convention:
#   tests/test_60_01_check_agent_candidate.py, tests/test_64_01_install.py
# ---------------------------------------------------------------------------
_SCRIPTS_DIR = str(Path(__file__).resolve().parent)
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

import _battery_core as _bc  # noqa: E402  (must follow sys.path surgery)

# Bind exported names for convenience and type-checker visibility
MergedPrompt = _bc.MergedPrompt
parse_merged_catalog = _bc.parse_merged_catalog
_run_prompt_n_times_to_paths = _bc._run_prompt_n_times_to_paths
detect_subskill = _bc.detect_subskill
detect_output_structure_from_file = _bc.detect_output_structure_from_file
_is_match = _bc._is_match
_verdict_matches = _bc._verdict_matches
_both_match = _bc._both_match
_ensure_claude_available = _bc._ensure_claude_available
_print = _bc._print
_validate_kn = _bc._validate_kn
self_test_boundary = _bc.self_test_boundary
self_test_focused = _bc.self_test_focused
DEFAULT_PLUGIN_DIR = _bc.DEFAULT_PLUGIN_DIR


# ---------------------------------------------------------------------------
# Battery driver
# ---------------------------------------------------------------------------


def run_battery(
    prompts_p: list[MergedPrompt],
    prompts_n: list[MergedPrompt],
    plugin_dir: Path,
    out_dir: Path,
    boundary_p_threshold: int,
    boundary_n_threshold: int,
    focused_p_threshold: int,
    focused_n_threshold: int,
    quiet: bool,
    repeat: int = 1,
    min_pass: int = 1,
) -> int:
    """Run the merged dual-signal battery, write outputs, return 0 (PASS) or 1 (FAIL).

    Each prompt is captured EXACTLY ONCE per run (one .jsonl per prompt). Both
    detect_subskill() and detect_output_structure_from_file() score the SAME
    .jsonl — no double capture. Per-prompt verdict passes only when BOTH signals
    meet their respective expectations; `n-a` auto-passes its side (D-02).

    Emits:
      - verdict.txt        (three sections: Boundary / Focused / Overall)
      - scores-boundary.tsv
      - scores-focused.tsv
      - per-prompt .jsonl files in out_dir

    Returns 0 if overall_pass (both boundary and focused pass), else 1.
    """
    _ensure_claude_available()
    out_dir.mkdir(parents=True, exist_ok=True)

    ordered: list[MergedPrompt] = list(prompts_p) + list(prompts_n)
    total = len(ordered)

    _print(
        f"check-routing-battery: catalog has {len(prompts_p)} P + "
        f"{len(prompts_n)} N (total {total})",
        quiet,
    )
    _print(f"  plugin-dir: {plugin_dir}", quiet)
    _print(f"  out:        {out_dir}", quiet)
    _print(
        f"  boundary thresholds: P >= {boundary_p_threshold}, "
        f"N >= {boundary_n_threshold}",
        quiet,
    )
    _print(
        f"  focused  thresholds: P >= {focused_p_threshold}, "
        f"N >= {focused_n_threshold}",
        quiet,
    )
    if repeat > 1:
        _print(f"  repeat:     {repeat} (K-of-N, min-pass={min_pass})", quiet)

    # Per-prompt result storage:
    # (prompt, paths, b_count, f_count, prompt_passed)
    results: list[tuple[MergedPrompt, int, int, bool]] = []

    # boundary and focused score rows for TSV output
    boundary_rows: list[tuple[MergedPrompt, list, list]] = []
    focused_rows: list[tuple[MergedPrompt, list, list]] = []

    for idx, prompt in enumerate(ordered, start=1):
        _print(
            f"[{idx}/{total}] {prompt.id}: boundary={prompt.expected_boundary} "
            f"output={prompt.expected_output} ...",
            quiet,
        )

        # ONE capture — both detectors score the same .jsonl files
        paths = _run_prompt_n_times_to_paths(prompt, plugin_dir, out_dir, repeat)

        b_verdicts = [detect_subskill(p) for p in paths]
        f_verdicts = [detect_output_structure_from_file(p) for p in paths]

        b_count, f_count, prompt_passed = _both_match(
            b_verdicts, f_verdicts,
            prompt.expected_boundary, prompt.expected_output,
            min_pass,
        )
        results.append((prompt, b_count, f_count, prompt_passed))
        boundary_rows.append((prompt, b_verdicts, paths))
        focused_rows.append((prompt, f_verdicts, paths))

        if repeat == 1:
            b_actual = b_verdicts[0]
            f_actual = f_verdicts[0]
            _print(
                f"    -> boundary={b_actual} output={f_actual} "
                f"{'PASS' if prompt_passed else 'FAIL'}",
                quiet,
            )
        else:
            _print(
                f"    -> boundary {b_count}/{repeat} output {f_count}/{repeat} "
                f"{'PASS' if prompt_passed else 'FAIL'}",
                quiet,
            )

    # P/N classification — strip a single leading de-collision prefix (B-/F-)
    # before reading the P/N marker.
    def _is_p_row(rid: str) -> bool:
        return re.sub(r"^[A-Z]-", "", rid).startswith("P")

    # ------------------------------------------------------------------
    # Tally: boundary signal
    # CR-01 fix: score ONLY rows that actually carry the boundary signal
    # (expected_boundary != "n-a"). Counting n-a rows would tally their
    # auto-pass (b_count == min_pass forced by _both_match) and permanently
    # defeat the gate — the boundary P/N thresholds must reproduce
    # check-sub-skill-routing.py's verdict over ITS rows (B-P12/B-P24 and
    # B-N1/B-N2) only, not the 4 focused P-rows that are n-a on this side.
    # ------------------------------------------------------------------
    boundary_results = [
        (prompt, b_count) for prompt, b_count, _f, _p in results
        if prompt.expected_boundary != "n-a"
    ]
    b_p_total = sum(1 for prompt, _ in boundary_results if _is_p_row(prompt.id))
    b_n_total = sum(1 for prompt, _ in boundary_results if not _is_p_row(prompt.id))
    b_p_pass = sum(
        1 for prompt, b_count in boundary_results
        if _is_p_row(prompt.id) and b_count >= min_pass
    )
    b_n_pass = sum(
        1 for prompt, b_count in boundary_results
        if not _is_p_row(prompt.id) and b_count >= min_pass
    )
    boundary_pass = b_p_pass >= boundary_p_threshold and b_n_pass >= boundary_n_threshold

    # ------------------------------------------------------------------
    # Tally: focused output
    # CR-02 fix: score ONLY rows that carry the focused signal
    # (expected_output != "n-a"). Otherwise the boundary N-rows (B-N1/B-N2,
    # n-a on this side) auto-pass and mask an F-N1 regression. Reproduces
    # check-focused-output.py's verdict over its rows (F-P12/24/25/26, F-N1).
    # ------------------------------------------------------------------
    focused_results = [
        (prompt, f_count) for prompt, _b, f_count, _p in results
        if prompt.expected_output != "n-a"
    ]
    fp_p_total = sum(1 for prompt, _ in focused_results if _is_p_row(prompt.id))
    fp_n_total = sum(1 for prompt, _ in focused_results if not _is_p_row(prompt.id))
    fp_p_pass = sum(
        1 for prompt, f_count in focused_results
        if _is_p_row(prompt.id) and f_count >= min_pass
    )
    fp_n_pass = sum(
        1 for prompt, f_count in focused_results
        if not _is_p_row(prompt.id) and f_count >= min_pass
    )
    focused_pass = fp_p_pass >= focused_p_threshold and fp_n_pass >= focused_n_threshold

    overall_pass = boundary_pass and focused_pass

    # ------------------------------------------------------------------
    # Build verdict.txt content — three sections in Phase 69 locked format
    # ------------------------------------------------------------------
    verdict_lines: list[str] = []

    # --- Boundary signal ---
    verdict_lines.append("--- Boundary signal ---")
    verdict_lines.append(f"BATTERY: {'PASS' if boundary_pass else 'FAIL'}")
    verdict_lines.append(f"P: {b_p_pass}/{b_p_total}  N: {b_n_pass}/{b_n_total}")
    if not boundary_pass:
        verdict_lines.append("")
        verdict_lines.append("Failed prompts:")
        for prompt, b_count, f_count, prompt_passed in results:
            if b_count < min_pass:
                if repeat == 1:
                    boundary_rows_map = {
                        p.id: bv for p, bv, _ in boundary_rows
                    }
                    actual_b = boundary_rows_map[prompt.id][0] if prompt.id in boundary_rows_map else "?"
                    verdict_lines.append(
                        f"  {prompt.id}: expected={prompt.expected_boundary} actual={actual_b}"
                    )
                else:
                    verdict_lines.append(
                        f"  {prompt.id}: expected={prompt.expected_boundary} "
                        f"{b_count}/{repeat} match"
                    )
    if repeat > 1:
        verdict_lines.append("")
        verdict_lines.append(f"Per-prompt K/N (best-of-{repeat}, K={min_pass}):")
        for prompt, b_count, f_count, _ in results:
            verdict_lines.append(
                f"  {prompt.id}: {b_count}/{repeat} "
                f"{'PASS' if b_count >= min_pass else 'FAIL'}"
            )

    verdict_lines.append("")

    # --- Focused output ---
    verdict_lines.append("--- Focused output ---")
    verdict_lines.append(f"BATTERY: {'PASS' if focused_pass else 'FAIL'}")
    verdict_lines.append(f"P: {fp_p_pass}/{fp_p_total}  N: {fp_n_pass}/{fp_n_total}")
    if not focused_pass:
        verdict_lines.append("")
        verdict_lines.append("Failed prompts:")
        for prompt, b_count, f_count, prompt_passed in results:
            if f_count < min_pass:
                if repeat == 1:
                    focused_rows_map = {
                        p.id: fv for p, fv, _ in focused_rows
                    }
                    actual_f = focused_rows_map[prompt.id][0] if prompt.id in focused_rows_map else "?"
                    verdict_lines.append(
                        f"  {prompt.id}: expected={prompt.expected_output} actual={actual_f}"
                    )
                else:
                    verdict_lines.append(
                        f"  {prompt.id}: expected={prompt.expected_output} "
                        f"{f_count}/{repeat} match"
                    )
    if repeat > 1:
        verdict_lines.append("")
        verdict_lines.append(f"Per-prompt K/N (best-of-{repeat}, K={min_pass}):")
        for prompt, b_count, f_count, _ in results:
            verdict_lines.append(
                f"  {prompt.id}: {f_count}/{repeat} "
                f"{'PASS' if f_count >= min_pass else 'FAIL'}"
            )

    verdict_lines.append("")

    # --- Overall ---
    verdict_lines.append("--- Overall ---")
    verdict_lines.append(f"BATTERY: {'PASS' if overall_pass else 'FAIL'}")
    verdict_lines.append("")

    verdict_text = "\n".join(verdict_lines)
    verdict_path = out_dir / "verdict.txt"
    verdict_path.write_text(verdict_text, encoding="utf-8")
    print(verdict_text, end="")

    # ------------------------------------------------------------------
    # Write scores-boundary.tsv
    # ------------------------------------------------------------------
    b_scores_path = out_dir / "scores-boundary.tsv"
    with b_scores_path.open("w", encoding="utf-8") as fh:
        if repeat == 1:
            fh.write("id\texpected\tactual\tpass\n")
            for prompt, b_verdicts, _ in boundary_rows:
                actual = b_verdicts[0]
                b_count_row = 1 if _is_match(actual, prompt.expected_boundary) or prompt.expected_boundary == "n-a" else 0  # type: ignore[arg-type]
                fh.write(
                    f"{prompt.id}\t{prompt.expected_boundary}\t{actual}\t"
                    f"{'pass' if b_count_row else 'fail'}\n"
                )
        else:
            fh.write("id\trun\texpected\tactual\tmatch\n")
            for prompt, b_verdicts, _ in boundary_rows:
                for run_idx, actual in enumerate(b_verdicts, start=1):
                    if prompt.expected_boundary == "n-a":
                        match_flag = 1
                    else:
                        match_flag = 1 if _is_match(actual, prompt.expected_boundary) else 0  # type: ignore[arg-type]
                    fh.write(
                        f"{prompt.id}\t{run_idx}\t{prompt.expected_boundary}\t"
                        f"{actual}\t{match_flag}\n"
                    )

    # ------------------------------------------------------------------
    # Write scores-focused.tsv
    # ------------------------------------------------------------------
    f_scores_path = out_dir / "scores-focused.tsv"
    with f_scores_path.open("w", encoding="utf-8") as fh:
        if repeat == 1:
            fh.write("id\texpected\tactual\tpass\n")
            for prompt, f_verdicts, _ in focused_rows:
                actual = f_verdicts[0]
                if prompt.expected_output == "n-a":
                    f_count_row = 1
                else:
                    f_count_row = 1 if _verdict_matches(actual, prompt.expected_output) else 0
                fh.write(
                    f"{prompt.id}\t{prompt.expected_output}\t{actual}\t"
                    f"{'pass' if f_count_row else 'fail'}\n"
                )
        else:
            fh.write("id\trun\texpected\tactual\tmatch\n")
            for prompt, f_verdicts, _ in focused_rows:
                for run_idx, actual in enumerate(f_verdicts, start=1):
                    if prompt.expected_output == "n-a":
                        match_flag = 1
                    else:
                        match_flag = 1 if _verdict_matches(actual, prompt.expected_output) else 0
                    fh.write(
                        f"{prompt.id}\t{run_idx}\t{prompt.expected_output}\t"
                        f"{actual}\t{match_flag}\n"
                    )

    return 0 if overall_pass else 1


# ---------------------------------------------------------------------------
# Self-test (merged — calls shared module fixtures + K>N rejection test here)
# ---------------------------------------------------------------------------


def self_test() -> int:
    """Validate detection logic against in-module fixtures. No claude invocation.

    Runs:
      1. self_test_boundary() — 8 boundary fixtures from _battery_core
      2. self_test_focused()  — 9 focused fixtures from _battery_core (Fixture 8 soft-skipped)
      3. K>N rejection sub-test — calls main() with repeat=2/min-pass=3 and asserts exit 2

    The K>N rejection sub-test is here (not in _battery_core) because main() is
    defined in this file (Coupling Risk 4 / Pitfall 5 in 67-PATTERNS.md).
    """
    all_passed = True

    rc_boundary = self_test_boundary()
    if rc_boundary != 0:
        all_passed = False

    rc_focused = self_test_focused()
    if rc_focused != 0:
        all_passed = False

    # K>N rejection sub-test (parallel to check-sub-skill-routing.py lines 840-868)
    try:
        rc_kn = main(
            [
                "--catalog",
                "/nonexistent/path/that/does/not/exist",
                "--repeat",
                "2",
                "--min-pass",
                "3",
            ]
        )
    except SystemExit as exc:
        rc_kn = exc.code if isinstance(exc.code, int) else 2
    if rc_kn != 2:
        print(
            f"self-test FAIL: 'kofn_invalid_kn_rejection' expected exit 2 "
            f"(K>N guard), got {rc_kn}",
            file=sys.stderr,
        )
        all_passed = False

    if all_passed:
        print("self-test PASS (boundary + focused + K>N rejection)")
        return 0
    return 1


# ---------------------------------------------------------------------------
# CLI scaffolding
# ---------------------------------------------------------------------------


def _default_out_dir() -> Path:
    """Return a timestamped /tmp directory unique to this battery run (D-07 / Pitfall 4)."""
    ts = _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return Path("/tmp") / f"check-routing-battery-{ts}"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="check-routing-battery.py",
        description=(
            "Merged dual-signal routing battery — captures each prompt once, "
            "scores boundary (detect_subskill) AND focused-output "
            "(detect_output_structure_from_file) from the same .jsonl, "
            "applies a both-match verdict (n-a auto-passes its side), "
            "and emits two K-of-N tally sections plus an Overall verdict."
        ),
    )
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--catalog",
        type=Path,
        help="Path to a merged routing-battery-catalog.md (BATT-01 format).",
    )
    mode.add_argument(
        "--self-test",
        dest="self_test",
        action="store_true",
        help=(
            "Validate detection logic against in-module fixtures and exit. "
            "Runs boundary fixtures, focused fixtures, and K>N rejection test."
        ),
    )
    p.add_argument(
        "--plugin-dir",
        type=Path,
        default=DEFAULT_PLUGIN_DIR,
        help=(
            f"Plugin directory passed to `claude --plugin-dir` "
            f"(default: {DEFAULT_PLUGIN_DIR})."
        ),
    )
    p.add_argument(
        "--out",
        type=Path,
        default=None,
        help=(
            "Output directory for .jsonl + verdict.txt + scores-*.tsv "
            "(default: /tmp/check-routing-battery-<UTC-timestamp>/)."
        ),
    )
    p.add_argument(
        "--boundary-p-threshold",
        type=int,
        default=2,
        dest="boundary_p_threshold",
        help=(
            "Min P-rows whose boundary verdict matches for boundary PASS "
            "(default: 2 — from check-sub-skill-routing.py --p-threshold)."
        ),
    )
    p.add_argument(
        "--boundary-n-threshold",
        type=int,
        default=2,
        dest="boundary_n_threshold",
        help=(
            "Min N-rows whose boundary verdict matches for boundary PASS "
            "(default: 2 — from check-sub-skill-routing.py --n-threshold; "
            "retained per D-04 resolution: N rows exist and the threshold "
            "gate is load-bearing for verdict parity)."
        ),
    )
    p.add_argument(
        "--focused-p-threshold",
        type=int,
        default=4,
        dest="focused_p_threshold",
        help=(
            "Min P-rows whose focused verdict matches for focused PASS "
            "(default: 4 — from check-focused-output.py --p-threshold)."
        ),
    )
    p.add_argument(
        "--focused-n-threshold",
        type=int,
        default=1,
        dest="focused_n_threshold",
        help=(
            "Min N-rows whose focused verdict matches for focused PASS "
            "(default: 1 — from check-focused-output.py --n-threshold)."
        ),
    )
    p.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress per-prompt progress lines (final verdict still printed).",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse the catalog and print counts; do not invoke claude.",
    )
    p.add_argument(
        "--repeat",
        type=int,
        default=5,
        metavar="N",
        help="Run each catalog prompt N times (default: 5).",
    )
    p.add_argument(
        "--min-pass",
        type=int,
        default=3,
        metavar="K",
        help="K-of-N runs must match expected for prompt to PASS (default: 3).",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()

    # K>N pre-flight guard — runs BEFORE any I/O (parallel to
    # check-sub-skill-routing.py lines 968-987, via shared _validate_kn helper)
    rc = _validate_kn(args)
    if rc is not None:
        return rc

    catalog_path: Path = args.catalog
    try:
        positives, negatives = parse_merged_catalog(catalog_path)
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except ValueError as exc:
        print(f"error: failed to parse catalog: {exc}", file=sys.stderr)
        return 2

    if args.dry_run:
        print(f"Catalog: {len(positives)} P-prompts, {len(negatives)} N-prompts")
        return 0

    out_dir: Path = args.out if args.out is not None else _default_out_dir()
    try:
        return run_battery(
            prompts_p=positives,
            prompts_n=negatives,
            plugin_dir=args.plugin_dir,
            out_dir=out_dir,
            boundary_p_threshold=args.boundary_p_threshold,
            boundary_n_threshold=args.boundary_n_threshold,
            focused_p_threshold=args.focused_p_threshold,
            focused_n_threshold=args.focused_n_threshold,
            quiet=args.quiet,
            repeat=args.repeat,
            min_pass=args.min_pass,
        )
    except OSError as exc:
        print(f"error: IO failure during battery run: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
