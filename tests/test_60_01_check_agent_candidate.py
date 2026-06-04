#!/usr/bin/env python3
"""Tests for Phase 60.1: check-agent.py --skip-name-check and _check_agent_subprocess flag.

Tests:
- _check_agent_text(skip_name_check=True): structurally valid candidate with any name passes
- _check_agent_text(skip_name_check=True): structurally invalid candidate (missing name key) fails
- _check_agent_text(skip_name_check=False): production agent passes
- _check_agent_text(skip_name_check=False): wrong-name agent fails (identity check fires)
- _check_agent_subprocess source contains --skip-name-check in command list
- CI regression guard: production check-agent call in validation.yml has no --skip-name-check

Run from repo root:
    python3 tests/test_60_01_check_agent_candidate.py
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CHECK_AGENT_PY = REPO_ROOT / "scripts" / "check-agent.py"
MAIN_PY = REPO_ROOT / "main.py"
AGENT_FILE = REPO_ROOT / "first-principles" / "agents" / "first-principles.md"
VALIDATION_YML = REPO_ROOT / ".github" / "workflows" / "validation.yml"

# Structurally valid candidate agent with a non-first-principles name
# and no required trigger phrases — used with skip_name_check=True
VALID_CANDIDATE_TEXT = """\
---
name: my-builder-agent
description: A candidate agent for testing builder output.
license: MIT
metadata:
  version: "1.0.0"
disallowedTools:
  - Write
  - Edit
maxTurns: 30
AskUserQuestion: permitted
---
## Body

Non-empty body content for the candidate agent fixture.
"""

# Same as above but with the `name:` and `disallowedTools:` keys removed —
# missing disallowedTools is a structural failure that fires even with skip_name_check=True
INVALID_CANDIDATE_TEXT = """\
---
description: A candidate agent for testing builder output.
license: MIT
metadata:
  version: "1.0.0"
maxTurns: 30
AskUserQuestion: permitted
---
## Body

Non-empty body content for the candidate agent fixture.
"""

# Same as VALID_CANDIDATE_TEXT but with a wrong name value
WRONG_NAME_TEXT = """\
---
name: wrong-agent-name
description: A candidate agent for testing builder output.
license: MIT
metadata:
  version: "1.0.0"
disallowedTools:
  - Write
  - Edit
maxTurns: 30
AskUserQuestion: permitted
---
## Body

Non-empty body content for the candidate agent fixture.
"""


def _load_check_agent() -> tuple[object | None, str]:
    """Import check-agent.py module dynamically. Returns (mod, "") on success or (None, err)."""
    try:
        spec = importlib.util.spec_from_file_location("check_agent", CHECK_AGENT_PY)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod, ""
    except Exception as e:
        return None, f"Could not import check-agent.py: {e}"


def check_check_agent_text_candidate_pass() -> tuple[bool, str]:
    """_check_agent_text(VALID_CANDIDATE_TEXT, skip_name_check=True) returns []."""
    mod, err = _load_check_agent()
    if mod is None:
        return False, err
    result = mod._check_agent_text(VALID_CANDIDATE_TEXT, skip_name_check=True)
    if result == []:
        return True, "valid candidate passes with skip_name_check=True"
    return False, f"expected [], got: {result}"


def check_check_agent_text_candidate_fail_missing_key() -> tuple[bool, str]:
    """_check_agent_text(INVALID_CANDIDATE_TEXT, skip_name_check=True) returns non-empty list.

    INVALID_CANDIDATE_TEXT is missing disallowedTools (a structural check that runs
    regardless of skip_name_check). This verifies that skip_name_check=True only skips
    identity checks, not all structural checks.
    """
    mod, err = _load_check_agent()
    if mod is None:
        return False, err
    result = mod._check_agent_text(INVALID_CANDIDATE_TEXT, skip_name_check=True)
    if not result:
        return False, "expected failures list, got empty list"
    # Check that the missing-disallowedTools failure is reported
    combined = " ".join(result)
    if "disallowedTools" not in combined:
        return False, f"expected error mentioning 'disallowedTools', got: {result}"
    return True, f"invalid candidate (missing disallowedTools) correctly fails: {result[0][:60]}"


def check_check_agent_text_production_pass() -> tuple[bool, str]:
    """_check_agent_text(production agent text, skip_name_check=False) returns []."""
    mod, err = _load_check_agent()
    if mod is None:
        return False, err
    try:
        text = AGENT_FILE.read_text(encoding="utf-8")
    except Exception as e:
        return False, f"Could not read {AGENT_FILE}: {e}"
    result = mod._check_agent_text(text, skip_name_check=False)
    if result == []:
        return True, "production agent passes with skip_name_check=False"
    return False, f"production agent unexpected failures: {result}"


def check_check_agent_text_wrong_name_fails() -> tuple[bool, str]:
    """_check_agent_text(WRONG_NAME_TEXT, skip_name_check=False) returns non-empty list."""
    mod, err = _load_check_agent()
    if mod is None:
        return False, err
    result = mod._check_agent_text(WRONG_NAME_TEXT, skip_name_check=False)
    if not result:
        return False, "expected name-identity failure, got empty list"
    combined = " ".join(result)
    if "first-principles" not in combined:
        return False, f"expected error mentioning 'first-principles', got: {result}"
    return True, f"wrong-name agent fails identity check: {result[0][:60]}"


def check_subprocess_args_contain_skip_name_check() -> tuple[bool, str]:
    """_check_agent_subprocess in main.py has '--skip-name-check' in command list."""
    try:
        text = MAIN_PY.read_text(encoding="utf-8")
    except Exception as e:
        return False, f"Could not read main.py: {e}"
    idx = text.find("def _check_agent_subprocess")
    if idx == -1:
        return False, "_check_agent_subprocess not found in main.py"
    snippet = text[idx : idx + 600]
    if '"--skip-name-check"' in snippet:
        return True, '"--skip-name-check" found in _check_agent_subprocess body'
    return False, f'"--skip-name-check" NOT found in first 600 chars of _check_agent_subprocess'


def check_ci_no_skip_name_check_on_production() -> tuple[bool, str]:
    """Production check-agent.py call in validation.yml does not include --skip-name-check."""
    try:
        text = VALIDATION_YML.read_text(encoding="utf-8")
    except Exception as e:
        return False, f"Could not read {VALIDATION_YML}: {e}"
    lines = text.splitlines()
    production_lines = [
        line for line in lines
        if "check-agent.py --file first-principles" in line
    ]
    if not production_lines:
        return False, "No line with 'check-agent.py --file first-principles' found in validation.yml"
    offending = [line for line in production_lines if "--skip-name-check" in line]
    if offending:
        return False, f"Production CI call contains --skip-name-check: {offending[0].strip()}"
    return True, f"Production CI call is clean ({len(production_lines)} matching line(s) checked)"


def main() -> None:
    checks = [
        ("_check_agent_text: valid candidate passes with skip_name_check=True", check_check_agent_text_candidate_pass),
        ("_check_agent_text: invalid candidate (missing disallowedTools) fails with skip_name_check=True", check_check_agent_text_candidate_fail_missing_key),
        ("_check_agent_text: production agent passes with skip_name_check=False", check_check_agent_text_production_pass),
        ("_check_agent_text: wrong-name agent fails with skip_name_check=False", check_check_agent_text_wrong_name_fails),
        ("_check_agent_subprocess: command list contains --skip-name-check", check_subprocess_args_contain_skip_name_check),
        ("CI regression guard: production CI call has no --skip-name-check", check_ci_no_skip_name_check_on_production),
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
