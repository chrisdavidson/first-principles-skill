#!/usr/bin/env python3
"""TDD RED phase: tests for Task 1 of Phase 59 Plan 02.

Tests:
- _render_and_write returns a Path on success and None on abort
- _check_description_budget returns (True, "N/2000 chars") for short descriptions
- _check_description_budget returns (False, "description N chars; over by M chars") for long descriptions
- _check_trigger_collisions returns (True, "no 4-gram collisions") for non-colliding description
- main.py PEP 723 header contains pyyaml>=6.0

Run from repo root:
    python3 tests/test_59_02_task1.py
"""

from __future__ import annotations

import sys
import ast
from pathlib import Path
import tempfile
import textwrap

REPO_ROOT = Path(__file__).resolve().parents[1]
MAIN_PY = REPO_ROOT / "main.py"


def check_pep723_header() -> tuple[bool, str]:
    """Check that main.py PEP 723 header contains pyyaml>=6.0."""
    text = MAIN_PY.read_text(encoding="utf-8")
    if "pyyaml>=6.0" in text:
        return True, "pyyaml>=6.0 found in header"
    return False, "pyyaml>=6.0 NOT found in header"


def check_parses() -> tuple[bool, str]:
    """Check that main.py is syntactically valid Python."""
    try:
        ast.parse(MAIN_PY.read_text(encoding="utf-8"))
        return True, "AST parse OK"
    except SyntaxError as e:
        return False, f"SyntaxError: {e}"


def check_function_definitions() -> tuple[bool, str]:
    """Check that all required functions are defined in main.py."""
    text = MAIN_PY.read_text(encoding="utf-8")
    required = [
        "def _check_description_budget",
        "def _check_trigger_collisions",
        "def _tokens(",
        "def _ngrams(",
        "_DESCRIPTION_BUDGET_CAP",
        "PLUGIN_SKILLS_DIR",
        "return out_path",
    ]
    missing = [r for r in required if r not in text]
    if missing:
        return False, f"Missing: {missing}"
    return True, "All required symbols found"


def check_render_and_write_signature() -> tuple[bool, str]:
    """Check that _render_and_write has the right return annotation."""
    text = MAIN_PY.read_text(encoding="utf-8")
    if "-> Path | None:" in text:
        return True, "_render_and_write returns Path | None"
    return False, "_render_and_write does NOT return Path | None"


def check_description_budget_behavior() -> tuple[bool, str]:
    """Behaviorally test _check_description_budget by importing main.py."""
    sys.path.insert(0, str(REPO_ROOT))
    try:
        import importlib
        import importlib.util
        spec = importlib.util.spec_from_file_location("main", MAIN_PY)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    except Exception as e:
        return False, f"Could not import main.py: {e}"

    # Create a temp skill file with a short description
    short_desc = "A short description for testing."
    skill_content = textwrap.dedent(f"""\
        ---
        name: test-skill
        description: "{short_desc}"
        ---
        # Body
    """)
    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False) as f:
        f.write(skill_content)
        tmp = Path(f.name)

    try:
        ok, detail = mod._check_description_budget(tmp)
        if not ok:
            return False, f"Short description: expected PASS, got FAIL: {detail}"
        if not detail.endswith("/2000 chars"):
            return False, f"Short description: detail format wrong: {detail}"

        # Now test with an over-budget description
        long_desc = "x" * 2001
        long_content = textwrap.dedent(f"""\
            ---
            name: test-skill
            description: "{long_desc}"
            ---
            # Body
        """)
        tmp.write_text(long_content, encoding="utf-8")
        ok2, detail2 = mod._check_description_budget(tmp)
        if ok2:
            return False, f"Over-budget description: expected FAIL, got PASS"
        if "over by" not in detail2:
            return False, f"Over-budget description: detail format wrong: {detail2}"
    finally:
        tmp.unlink(missing_ok=True)

    return True, "Budget check behavior correct (PASS and FAIL cases)"


def check_trigger_collisions_behavior() -> tuple[bool, str]:
    """Behaviorally test _check_trigger_collisions with a non-colliding description."""
    sys.path.insert(0, str(REPO_ROOT))
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("main", MAIN_PY)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    except Exception as e:
        return False, f"Could not import main.py: {e}"

    # A completely unique description unlikely to collide with any installed skill
    unique_desc = "a completely unique description for xyzzy blargh test that should never collide"
    skill_content = textwrap.dedent(f"""\
        ---
        name: unique-test-skill
        description: "{unique_desc}"
        ---
        # Body
    """)
    with tempfile.NamedTemporaryFile(suffix=".md", mode="w", delete=False) as f:
        f.write(skill_content)
        tmp = Path(f.name)

    try:
        ok, detail = mod._check_trigger_collisions(tmp)
        if not ok:
            return False, f"Non-colliding description: expected PASS, got FAIL: {detail}"
        if detail != "no 4-gram collisions":
            return False, f"Non-colliding description: unexpected detail: {detail}"
    finally:
        tmp.unlink(missing_ok=True)

    return True, "Collision check behavior correct (PASS case)"


def main() -> None:
    checks = [
        ("PEP 723 header has pyyaml", check_pep723_header),
        ("main.py parses as valid Python", check_parses),
        ("Required function definitions exist", check_function_definitions),
        ("_render_and_write signature", check_render_and_write_signature),
        ("_check_description_budget behavior", check_description_budget_behavior),
        ("_check_trigger_collisions behavior", check_trigger_collisions_behavior),
    ]

    failures = []
    for name, fn in checks:
        try:
            ok, detail = fn()
        except Exception as e:
            ok, detail = False, f"Exception: {e}"
        status = "PASS" if ok else "FAIL"
        print(f"  {status}: {name} ({detail})")
        if not ok:
            failures.append(name)

    print()
    if failures:
        print(f"RESULT: FAIL — {len(failures)}/{len(checks)} checks failed")
        sys.exit(1)
    else:
        print(f"RESULT: PASS — {len(checks)}/{len(checks)} checks passed")
        sys.exit(0)


if __name__ == "__main__":
    main()
