#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Report the generated agent body's line count (TEARDOWN-01 — retired gate).

The generated agent surface at ``first-principles/agents/first-principles.md``
is reported on every run for visibility. As of TEARDOWN-01
(``docs/v8.7-constraint-teardown.md``) this script is report-only: it never
fails on the body's size. ``MAX_LINES`` survives as a historical reference
figure only — see its provenance comment below.

Usage:
    python3 scripts/check-body-budget.py [--self-test]

Exit codes:
    0  successful report (or self-test passed) — this script has no fail path
       tied to the body's line count
    2  environment error (Python <3.12, agent body file not found)

--self-test: runs in-process fixtures pinning the reporting's counting
             correctness (splitlines() semantics) and proving no fail path
             exists at, one line past, or far past the historical MAX_LINES
             threshold. Independent of the real generated body's current
             size — uses pure strings, no disk I/O.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REPO_ROOT: Path = Path(__file__).resolve().parents[1]
AGENT_FILE: Path = REPO_ROOT / "first-principles" / "agents" / "first-principles.md"

# Historical reference figure only (TEARDOWN-01 — see docs/v8.7-constraint-teardown.md).
# This was previously an enforced budget; it no longer gates anything.
# Recalibrated for the 9th inlined technique procedure (theoretical-limit, v7.3 / D-10 redux):
# body grew 560→622 when theoretical-limit was wired; limit raised to 622 + 22 buffer.
# Full raise chain: 500 → 580 → 644, each raise made when the prior limit bound.
# Demoted under TEARDOWN-01 (docs/v8.7-constraint-teardown.md): the fitted-limit provenance
# above is itself the evidence the number was fitted to the body's incidental size, not to
# any measured quality effect — the retirement record cites this comment directly.
MAX_LINES: int = 644


def _count_lines(text: str) -> int:
    """Count lines using ``splitlines()`` semantics.

    Matches ``wc -l`` when the file ends in a trailing newline, and is
    well-defined for fixtures with or without a trailing newline. Using
    ``text.count('\\n')`` would be off-by-one when the trailing newline is
    missing, so it is deliberately avoided.
    """
    return len(text.splitlines())


def _report_body_text(text: str) -> str:
    """Return a report string for body text. Never fails — report-only.

    The report names the current line count and the historical reference
    figure (``MAX_LINES``) for context, but no branch here raises
    ``SystemExit`` or otherwise signals failure — the body's size cannot
    fail this function.
    """
    count = _count_lines(text)
    return f"body is {count} lines (historical reference figure {MAX_LINES}, gate retired — TEARDOWN-01)"


def _require_python_version() -> None:
    if sys.version_info < (3, 12):
        sys.stderr.write(
            f"scripts/check-body-budget.py requires Python >=3.12 "
            f"(running {sys.version_info.major}.{sys.version_info.minor}).\n"
        )
        sys.exit(2)


def _validate_body_file() -> None:
    """Report on the real generated agent body file.

    Always reaches the report print branch — the environment-error exit-2
    paths below are orthogonal to the retired gate/report distinction and
    stay: they signal the file is missing, not that it is too large.
    """
    if not AGENT_FILE.exists():
        sys.stderr.write(
            f"check-body-budget: agent body file not found: {AGENT_FILE}\n"
            f"  Run the sync pipeline to generate it before running this report.\n"
        )
        sys.exit(2)

    text = AGENT_FILE.read_text(encoding="utf-8")
    print(f"check-body-budget: REPORT — {_report_body_text(text)}")


def _run_self_test() -> None:
    """Run in-process fixtures pinning reporting correctness, not gating.

    Independent of the real generated body — uses pure strings, never reads
    AGENT_FILE. Asserts:
      - count arithmetic at the empty and single-line edges,
      - the splitlines() trailing-newline contract (644 either way),
      - no fail path at 643, 644, 645, and 1288 lines — the last two are
        load-bearing: under the retired gate they would have been failures.

    Uses plain ``assert`` for internal consistency checks rather than an
    accumulate-then-exit-nonzero pattern — this module has no fail path tied
    to the body's size, and these assertions can only trip on a genuine bug
    in the counting/reporting logic itself, never on the fixtures' sizes.
    """
    # Count arithmetic at the empty and single-line edges.
    assert _count_lines("") == 0, f'empty string: expected 0, got {_count_lines("")}'
    print("check-body-budget --self-test: empty string counts 0 — correct")

    assert _count_lines("x") == 1, f'single line "x": expected 1, got {_count_lines("x")}'
    print('check-body-budget --self-test: single line "x" counts 1 — correct')

    # splitlines() trailing-newline contract: 644 lines, with and without a
    # trailing newline, both count 644. A newline-counting implementation
    # (text.count('\n')) would return 643 on the unterminated variant.
    terminated_644 = "x\n" * 644
    unterminated_644 = "\n".join(["x"] * 644)  # exactly 644 lines, no trailing newline

    assert _count_lines(terminated_644) == 644, (
        f"644-line fixture (trailing newline): expected 644, got {_count_lines(terminated_644)}"
    )
    print(
        "check-body-budget --self-test: 644-line fixture (trailing newline) counts 644 — correct"
    )

    assert _count_lines(unterminated_644) == 644, (
        f"644-line fixture (no trailing newline): expected 644, got {_count_lines(unterminated_644)}"
    )
    print(
        "check-body-budget --self-test: 644-line fixture (no trailing newline) counts 644 — correct"
    )

    # No fail path: fixtures at 643, 644, 645 and 1288 lines are each reported
    # with zero failures. 645 and 1288 are load-bearing — under the retired
    # gate they would have been failures.
    for n in (643, 644, 645, 1288):
        fixture = "x\n" * n
        report = _report_body_text(fixture)  # must return normally — no fail path exists
        actual_count = _count_lines(fixture)
        assert actual_count == n, f"{n}-line fixture: count mismatch, expected {n}, got {actual_count}"
        print(f"check-body-budget --self-test: {n}-line fixture reported with zero failures: {report}")

    print("check-body-budget --self-test: PASS")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Reports the generated first-principles agent body's line count "
            f"(historical reference figure MAX_LINES={MAX_LINES}; gate retired "
            "under TEARDOWN-01, see docs/v8.7-constraint-teardown.md)."
        )
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run in-process fixtures pinning reporting correctness (no gating)",
    )
    args = parser.parse_args()

    _require_python_version()

    if args.self_test:
        _run_self_test()
        return

    _validate_body_file()


if __name__ == "__main__":
    main()
