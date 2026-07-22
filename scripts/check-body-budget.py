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
    1  self-test fixture failure (counting/reporting logic bug)
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
import tempfile
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


def _run_self_test() -> int:
    """Run in-process fixtures pinning reporting correctness, not gating.

    Mostly independent of the real generated body — uses pure strings, and
    only substitutes a temp-file fixture for ``AGENT_FILE`` in the final
    ``_validate_body_file`` check below (restored before returning). Checks:
      - count arithmetic at the empty and single-line edges,
      - the splitlines() trailing-newline contract (644 either way),
      - no fail path at 643, 644, 645, and 1288 lines via ``_report_body_text``
        — the last two are load-bearing: under the retired gate they would
        have been failures,
      - no fail path in ``_validate_body_file`` itself (the function an
        actual caller reaches, not just the pure-string helper it calls) at
        1288 lines — a re-introduced ``sys.exit(1)`` there would otherwise go
        uncaught.

    Uses an accumulate-then-return-nonzero pattern rather than bare
    ``assert``. Under ``python3 -O`` the Python compiler strips every
    ``assert`` statement from the bytecode, so a bare-assert self-test would
    print every "— correct" line and ``PASS`` and exit 0 even if
    ``_count_lines`` (or the no-fail-path contract) were genuinely broken —
    the checks would be inert exactly when they are needed most. Accumulating
    failures into a list and returning a nonzero exit code does not depend on
    the ``assert`` statement to signal failure, so it fires identically under
    both ``python3`` and ``python3 -O``.
    """
    failures: list[str] = []

    def _expect(cond: bool, ok_msg: str, fail_msg: str) -> None:
        if cond:
            print(f"check-body-budget --self-test: {ok_msg} — correct")
        else:
            failures.append(fail_msg)

    # Count arithmetic at the empty and single-line edges.
    _expect(
        _count_lines("") == 0,
        "empty string counts 0",
        f'empty string: expected 0, got {_count_lines("")}',
    )
    _expect(
        _count_lines("x") == 1,
        'single line "x" counts 1',
        f'single line "x": expected 1, got {_count_lines("x")}',
    )

    # splitlines() trailing-newline contract: 644 lines, with and without a
    # trailing newline, both count 644. A newline-counting implementation
    # (text.count('\n')) would return 643 on the unterminated variant.
    terminated_644 = "x\n" * 644
    unterminated_644 = "\n".join(["x"] * 644)  # exactly 644 lines, no trailing newline

    _expect(
        _count_lines(terminated_644) == 644,
        "644-line fixture (trailing newline) counts 644",
        f"644-line fixture (trailing newline): expected 644, got {_count_lines(terminated_644)}",
    )
    _expect(
        _count_lines(unterminated_644) == 644,
        "644-line fixture (no trailing newline) counts 644",
        f"644-line fixture (no trailing newline): expected 644, got {_count_lines(unterminated_644)}",
    )

    # No fail path: fixtures at 643, 644, 645 and 1288 lines are each reported
    # with zero failures. 645 and 1288 are load-bearing — under the retired
    # gate they would have been failures.
    for n in (643, 644, 645, 1288):
        fixture = "x\n" * n
        report = _report_body_text(fixture)  # must return normally — no fail path exists
        actual_count = _count_lines(fixture)
        _expect(
            actual_count == n,
            f"{n}-line fixture reported with zero failures: {report}",
            f"{n}-line fixture: count mismatch, expected {n}, got {actual_count}",
        )

    # Exercise _validate_body_file itself — the function an actual caller
    # reaches — not just _report_body_text. A re-introduced sys.exit(1) tied
    # to the body's size in _validate_body_file would not be caught by the
    # checks above, since none of them call it.
    global AGENT_FILE
    _original_agent_file = AGENT_FILE
    with tempfile.TemporaryDirectory() as tmpdir:
        over_budget_file = Path(tmpdir) / "over-budget-fixture.md"
        over_budget_file.write_text("x\n" * 1288, encoding="utf-8")
        AGENT_FILE = over_budget_file
        try:
            _validate_body_file()
        except SystemExit as exc:
            failures.append(
                "_validate_body_file() on a 1288-line fixture unexpectedly called "
                f"sys.exit({exc.code}) — the retired gate must never fail on size"
            )
        else:
            print(
                "check-body-budget --self-test: _validate_body_file() on a "
                "1288-line fixture returned with zero failures — correct"
            )
        finally:
            AGENT_FILE = _original_agent_file

    if failures:
        for msg in failures:
            sys.stderr.write(f"check-body-budget --self-test FAIL: {msg}\n")
        return 1

    print("check-body-budget --self-test: PASS")
    return 0


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
        sys.exit(_run_self_test())

    _validate_body_file()


if __name__ == "__main__":
    main()
