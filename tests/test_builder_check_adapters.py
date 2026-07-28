"""Pytest adapter for the three builder check-suites that pytest never collected.

Why this file exists
--------------------
`tests/test_59_02_task1.py`, `tests/test_60_01_check_agent_candidate.py`, and
`tests/test_64_01_install.py` were written as standalone runners: their assertions
live in functions named `check_*` (not `test_*`), each returning a
`tuple[bool, str]` that the file's own `main()` tallies under
`if __name__ == "__main__"`.

pytest collects nothing from any of them — verified live during the 2026-07-28
technical-debt audit (`pytest <the three files> -v` -> `collected 0 items`). So
`main.py`, the v4.0-era builder those 19 checks exist to protect, was covered by
three files that *looked* like a regression suite and contributed zero assertions
to the suite. See docs/technical-debt-audit-2026-07-28.md.

Why an adapter instead of renaming `check_*` -> `test_*`
--------------------------------------------------------
A rename alone would be worse than the gap it closes. These functions signal
failure through a returned `False`, not through a raised assertion, so pytest
would collect them and report every one as PASSING regardless of the bool — a
silent false green. (pytest only warns about non-None returns; it does not fail
on them.) Rewriting all 19 to assert internally would also break each file's
`main()` runner, which consumes the `(ok, detail)` tuples to print its tally.

This adapter keeps both entry points working: the standalone runners are
untouched and still valid, while pytest now asserts on the same bools.

Adding a new check: name it `check_*` in one of the three modules and it is
picked up here automatically — no edit to this file required.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

TESTS_DIR = Path(__file__).resolve().parent

# The three standalone check-suites, each keyed by the module alias used to
# import it here. Aliases are deliberately distinct from the real filenames so
# this import cannot collide with pytest's own collection-time import of the
# same files.
CHECK_SUITES: dict[str, str] = {
    "_builder_checks_59_02": "test_59_02_task1.py",
    "_builder_checks_60_01": "test_60_01_check_agent_candidate.py",
    "_builder_checks_64_01": "test_64_01_install.py",
}


def _load(alias: str, filename: str) -> ModuleType:
    """Import a check-suite by file path under a private alias."""
    path = TESTS_DIR / filename
    spec = importlib.util.spec_from_file_location(alias, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot build import spec for {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[alias] = module
    spec.loader.exec_module(module)
    return module


def _discover() -> list[tuple[str, str]]:
    """Return (alias, check_function_name) for every check_* in every suite.

    Discovery is at import time so each check becomes its own parametrized case
    with a readable id, rather than one opaque aggregate test.
    """
    found: list[tuple[str, str]] = []
    for alias, filename in CHECK_SUITES.items():
        module = _load(alias, filename)
        for name in sorted(dir(module)):
            if name.startswith("check_") and callable(getattr(module, name)):
                found.append((alias, name))
    return found


DISCOVERED = _discover()


def test_discovery_is_non_vacuous() -> None:
    """Guard: the adapter must never silently adapt zero checks.

    Without this, a rename or a broken import would turn the whole adapter into
    a no-op that still reports green — reproducing the exact failure mode this
    file was written to fix.
    """
    assert DISCOVERED, "no check_* functions discovered — adapter is vacuous"
    suites_covered = {alias for alias, _ in DISCOVERED}
    assert suites_covered == set(CHECK_SUITES), (
        f"expected checks from all {len(CHECK_SUITES)} suites, "
        f"got {sorted(suites_covered)}"
    )


@pytest.mark.parametrize(
    ("alias", "check_name"),
    DISCOVERED,
    ids=[f"{alias.removeprefix('_builder_checks_')}::{name}" for alias, name in DISCOVERED],
)
def test_builder_check(alias: str, check_name: str) -> None:
    """Run one `check_*` function and assert on the bool it returns."""
    module = sys.modules[alias]
    ok, detail = getattr(module, check_name)()
    assert ok, f"{CHECK_SUITES[alias]}::{check_name} failed: {detail}"
