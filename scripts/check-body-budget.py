#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""META-Q4 / HOOK-01 + HOOK-02 gate: enforce the generated agent body line budget.

The generated agent surface at ``first-principles/agents/first-principles.md`` must
stay at or below ``MAX_LINES`` lines so the agent description budget and overall
context cost remain predictable. This script is the enforcement primitive invoked
by the pre-commit hook (Plan 35-02).

Usage:
    python3 scripts/check-body-budget.py [--self-test]

Exit codes:
    0  body line count is within budget (or self-test passed)
    1  validation failure (body exceeds MAX_LINES, or a self-test fixture
       classified incorrectly)
    2  environment error (Python <3.12, agent body file not found)

--self-test: runs two in-process fixtures (one at exactly MAX_LINES, one at
             MAX_LINES + 1) and verifies each classifies correctly. Independent
             of the real generated body's current size — uses pure strings, no
             disk I/O.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REPO_ROOT: Path = Path(__file__).resolve().parents[1]
AGENT_FILE: Path = REPO_ROOT / "first-principles" / "agents" / "first-principles.md"

# Hard-coded per D-03: the line budget is a code constant, not a CLI flag, env
# var, or config-file value. Changing the budget requires a code edit + commit
# so the change is reviewed, attributed, and traceable in git history.
MAX_LINES: int = 500


def _count_lines(text: str) -> int:
    """Count lines using ``splitlines()`` semantics.

    Matches ``wc -l`` when the file ends in a trailing newline, and is
    well-defined for fixtures with or without a trailing newline. Using
    ``text.count('\\n')`` would be off-by-one when the trailing newline is
    missing, so it is deliberately avoided.
    """
    return len(text.splitlines())


def _check_body_text(text: str) -> list[str]:
    """Validate body text against the line budget.

    Returns a list of failure-message strings (empty list == valid). The exact
    substring ``"exceeds MAX_LINES=500"`` appears in the failure message so the
    self-test can pin on a wrong-reason failure.
    """
    count = _count_lines(text)
    if count <= MAX_LINES:
        return []
    return [f"body is {count} lines, exceeds MAX_LINES={MAX_LINES}"]


def _require_python_version() -> None:
    if sys.version_info < (3, 12):
        sys.stderr.write(
            f"scripts/check-body-budget.py requires Python >=3.12 "
            f"(running {sys.version_info.major}.{sys.version_info.minor}).\n"
        )
        sys.exit(2)


def _validate_body_file() -> None:
    """Validate the real generated agent body file. Exits non-zero on failure."""
    if not AGENT_FILE.exists():
        sys.stderr.write(
            f"check-body-budget: agent body file not found: {AGENT_FILE}\n"
            f"  Run the sync pipeline to generate it before running this gate.\n"
        )
        sys.exit(2)

    text = AGENT_FILE.read_text(encoding="utf-8")
    failures = _check_body_text(text)

    if failures:
        for msg in failures:
            sys.stderr.write(f"check-body-budget: FAIL — {msg}\n")
        sys.exit(1)

    count = _count_lines(text)
    print(f"check-body-budget: PASS — body is {count} lines (limit {MAX_LINES})")


def _run_self_test() -> None:
    """Run in-process PASS+FAIL fixtures, verifying each classifies correctly.

    Independent of the real generated body — uses pure strings, never reads
    AGENT_FILE. Pins failure on a specific substring so a wrong-reason pass
    cannot slip through.
    """
    pass_fixture = "x\n" * MAX_LINES
    fail_fixture = "x\n" * (MAX_LINES + 1)
    expected_fail_substring = f"exceeds MAX_LINES={MAX_LINES}"

    wrong_results: list[str] = []

    # PASS fixture: exactly MAX_LINES lines → must produce zero failures.
    pass_failures = _check_body_text(pass_fixture)
    if pass_failures:
        print(
            f"check-body-budget --self-test: pass-fixture ({MAX_LINES} lines) "
            f"WRONGLY FAILED: {'; '.join(pass_failures)}"
        )
        wrong_results.append(f"pass-fixture wrongly failed ({len(pass_failures)} failure(s))")
    else:
        print(
            f"check-body-budget --self-test: pass-fixture ({MAX_LINES} lines) "
            f"correctly passed"
        )

    # FAIL fixture: MAX_LINES + 1 lines → must produce exactly one failure
    # whose message contains the expected substring.
    fail_failures = _check_body_text(fail_fixture)
    if not fail_failures:
        print(
            f"check-body-budget --self-test: fail-fixture ({MAX_LINES + 1} lines) "
            f"WRONGLY PASSED (expected failure)"
        )
        wrong_results.append("fail-fixture wrongly passed")
    elif len(fail_failures) != 1:
        print(
            f"check-body-budget --self-test: fail-fixture produced "
            f"{len(fail_failures)} failures (expected exactly 1): "
            f"{'; '.join(fail_failures)}"
        )
        wrong_results.append(f"fail-fixture produced {len(fail_failures)} failures, expected 1")
    elif expected_fail_substring not in fail_failures[0]:
        print(
            f"check-body-budget --self-test: fail-fixture failed for the WRONG reason "
            f"(expected substring '{expected_fail_substring}', got: {fail_failures[0]})"
        )
        wrong_results.append(f"fail-fixture wrong reason (expected '{expected_fail_substring}')")
    else:
        print(
            f"check-body-budget --self-test: fail-fixture ({MAX_LINES + 1} lines) "
            f"correctly failed with expected substring"
        )

    if wrong_results:
        sys.stderr.write(
            f"check-body-budget --self-test: FAIL — {', '.join(wrong_results)}\n"
        )
        sys.exit(1)

    print("check-body-budget --self-test: PASS")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "HOOK-01/HOOK-02: enforce the generated first-principles agent body "
            f"line budget (MAX_LINES={MAX_LINES})."
        )
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run in-process PASS+FAIL fixtures and verify each classifies correctly",
    )
    args = parser.parse_args()

    _require_python_version()

    if args.self_test:
        _run_self_test()
        return

    _validate_body_file()


if __name__ == "__main__":
    main()
