#!/usr/bin/env python3
"""Tests for Phase 64: --install flag behavior in main.py.

Tests:
- check_skill_happy_path: _install("skill", ..., install=True) copies candidate to shared/skills/<slug>/SKILL.md
- check_agent_happy_path: _install("agent", ..., install=True) copies candidate to shared/agent/<slug>.md
- check_conflict_abort: _install raises SystemExit(1) when dest already exists; no overwrite
- check_sync_failure_rollback: _install raises SystemExit(1) on sync failure; dest file is deleted
- check_validation_fail_blocks_install: _install raises SystemExit(1) when validation fails; no file written
- check_shared_tree_untouched: git status --porcelain shared/ is empty after all tests run

Run from repo root:
    python3 tests/test_64_01_install.py
"""

from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
import tempfile
import types
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MAIN_PY = REPO_ROOT / "main.py"

# Candidate file content for tests
_SKILL_CONTENT = """\
---
name: my-test-skill
description: "A test skill for Phase 64 install tests."
---

## When to reach for this

Use this skill during testing.
"""

_AGENT_CONTENT = """\
---
name: my-test-agent
description: "A test agent for Phase 64 install tests."
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


def _load_main() -> tuple[object | None, str]:
    """Import a fresh main.py module instance via importlib. Returns (mod, "") on success."""
    try:
        spec = importlib.util.spec_from_file_location("main", MAIN_PY)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod, ""
    except Exception as e:
        return None, f"Could not import main.py: {e}"


def check_skill_happy_path() -> tuple[bool, str]:
    """_install('skill', candidate, install=True) copies to shared/skills/<slug>/SKILL.md.

    Uses a tmpdir anchored under REPO_ROOT so dest_path.relative_to(REPO_ROOT) succeeds.
    Patches subprocess so sync-content.py is never actually invoked.
    """
    mod, err = _load_main()
    if mod is None:
        return False, err

    # Anchor tmpdir under REPO_ROOT so relative_to(REPO_ROOT) works
    anchor = Path(tempfile.mkdtemp(dir=REPO_ROOT))
    try:
        # Patch SHARED_SKILLS_DIR and SHARED_AGENT_DIR to tmpdir subdirs
        skills_dir = anchor / "shared" / "skills"
        agent_dir = anchor / "shared" / "agent"
        setattr(mod, "SHARED_SKILLS_DIR", skills_dir)
        setattr(mod, "SHARED_AGENT_DIR", agent_dir)

        # Patch subprocess so sync-content.py returns success (returncode=0)
        fake_subprocess = types.SimpleNamespace(
            run=lambda *a, **k: types.SimpleNamespace(returncode=0, stderr="", stdout="")
        )
        setattr(mod, "subprocess", fake_subprocess)

        # Patch _run_validation to return True (skip real checks)
        setattr(mod, "_run_validation", lambda *a, **k: True)

        # Write candidate file to a temp location inside REPO_ROOT
        cand_path = anchor / "my-test-skill.md"
        cand_path.write_text(_SKILL_CONTENT, encoding="utf-8")

        mod._install("skill", cand_path, install=True)

        dest = skills_dir / "my-test-skill" / "SKILL.md"
        if not dest.exists():
            return False, f"Expected dest {dest} to exist after install"
        installed_text = dest.read_text(encoding="utf-8")
        original_text = cand_path.read_text(encoding="utf-8")
        if installed_text != original_text:
            return False, "Installed content does not match candidate content"
        return True, f"skill happy path: {dest.relative_to(anchor)} created with correct content"
    except SystemExit as e:
        return False, f"Unexpected SystemExit({e.code}) in skill happy path"
    except Exception as e:
        return False, f"Unexpected exception: {e}"
    finally:
        shutil.rmtree(anchor, ignore_errors=True)


def check_agent_happy_path() -> tuple[bool, str]:
    """_install('agent', candidate, install=True) copies to shared/agent/<slug>.md.

    Uses a tmpdir anchored under REPO_ROOT so dest_path.relative_to(REPO_ROOT) succeeds.
    Patches subprocess so sync-content.py is never actually invoked.
    """
    mod, err = _load_main()
    if mod is None:
        return False, err

    anchor = Path(tempfile.mkdtemp(dir=REPO_ROOT))
    try:
        skills_dir = anchor / "shared" / "skills"
        agent_dir = anchor / "shared" / "agent"
        setattr(mod, "SHARED_SKILLS_DIR", skills_dir)
        setattr(mod, "SHARED_AGENT_DIR", agent_dir)

        fake_subprocess = types.SimpleNamespace(
            run=lambda *a, **k: types.SimpleNamespace(returncode=0, stderr="", stdout="")
        )
        setattr(mod, "subprocess", fake_subprocess)

        setattr(mod, "_run_validation", lambda *a, **k: True)

        cand_path = anchor / "my-test-agent.md"
        cand_path.write_text(_AGENT_CONTENT, encoding="utf-8")

        mod._install("agent", cand_path, install=True)

        dest = agent_dir / "my-test-agent.md"
        if not dest.exists():
            return False, f"Expected dest {dest} to exist after install"
        installed_text = dest.read_text(encoding="utf-8")
        original_text = cand_path.read_text(encoding="utf-8")
        if installed_text != original_text:
            return False, "Installed content does not match candidate content"
        return True, f"agent happy path: {dest.relative_to(anchor)} created with correct content"
    except SystemExit as e:
        return False, f"Unexpected SystemExit({e.code}) in agent happy path"
    except Exception as e:
        return False, f"Unexpected exception: {e}"
    finally:
        shutil.rmtree(anchor, ignore_errors=True)


def check_conflict_abort() -> tuple[bool, str]:
    """_install raises SystemExit(1) when dest already exists; pre-existing file is unchanged.

    Uses a tmpdir anchored under REPO_ROOT so dest_path.relative_to(REPO_ROOT) succeeds
    inside the conflict-abort error message in _install.
    """
    mod, err = _load_main()
    if mod is None:
        return False, err

    anchor = Path(tempfile.mkdtemp(dir=REPO_ROOT))
    try:
        skills_dir = anchor / "shared" / "skills"
        agent_dir = anchor / "shared" / "agent"
        setattr(mod, "SHARED_SKILLS_DIR", skills_dir)
        setattr(mod, "SHARED_AGENT_DIR", agent_dir)

        setattr(mod, "_run_validation", lambda *a, **k: True)

        # Pre-create the target file with sentinel content
        dest = skills_dir / "my-test-skill" / "SKILL.md"
        dest.parent.mkdir(parents=True, exist_ok=True)
        sentinel = "pre-existing content — must not be overwritten\n"
        dest.write_text(sentinel, encoding="utf-8")

        cand_path = anchor / "my-test-skill.md"
        cand_path.write_text(_SKILL_CONTENT, encoding="utf-8")

        try:
            mod._install("skill", cand_path, install=True)
            return False, "_install should have raised SystemExit(1) on conflict"
        except SystemExit as e:
            if e.code != 1:
                return False, f"Expected SystemExit(1), got SystemExit({e.code})"
            # Verify the pre-existing file was not overwritten
            after_content = dest.read_text(encoding="utf-8")
            if after_content != sentinel:
                return False, "Conflict-abort: pre-existing file content was modified"
            return True, "conflict abort: SystemExit(1) raised; pre-existing file unchanged"
        except Exception as e:
            return False, f"Unexpected exception: {e}"
    finally:
        shutil.rmtree(anchor, ignore_errors=True)


def check_sync_failure_rollback() -> tuple[bool, str]:
    """_install raises SystemExit(1) on sync failure; dest file is deleted (rollback).

    Uses a tmpdir anchored under REPO_ROOT so dest_path.relative_to(REPO_ROOT) succeeds
    inside the rollback notice in _sync_content.
    """
    mod, err = _load_main()
    if mod is None:
        return False, err

    anchor = Path(tempfile.mkdtemp(dir=REPO_ROOT))
    try:
        skills_dir = anchor / "shared" / "skills"
        agent_dir = anchor / "shared" / "agent"
        setattr(mod, "SHARED_SKILLS_DIR", skills_dir)
        setattr(mod, "SHARED_AGENT_DIR", agent_dir)

        setattr(mod, "_run_validation", lambda *a, **k: True)

        # Patch subprocess to simulate sync failure (non-zero returncode)
        class _FakeProc:
            returncode = 1
            stderr = "sync boom\n"
            stdout = ""

        fake_subprocess = types.SimpleNamespace(
            run=lambda *a, **k: _FakeProc()
        )
        setattr(mod, "subprocess", fake_subprocess)

        cand_path = anchor / "my-test-skill.md"
        cand_path.write_text(_SKILL_CONTENT, encoding="utf-8")
        dest = skills_dir / "my-test-skill" / "SKILL.md"

        try:
            mod._install("skill", cand_path, install=True)
            return False, "_install should have raised SystemExit(1) on sync failure"
        except SystemExit as e:
            if e.code != 1:
                return False, f"Expected SystemExit(1), got SystemExit({e.code})"
            # Verify rollback: dest should not exist
            if dest.exists():
                return False, f"Rollback failed: dest file still exists at {dest}"
            return True, "sync failure rollback: SystemExit(1) raised; dest file deleted"
        except Exception as e:
            return False, f"Unexpected exception: {e}"
    finally:
        shutil.rmtree(anchor, ignore_errors=True)


def check_validation_fail_blocks_install() -> tuple[bool, str]:
    """_install raises SystemExit(1) when validation fails; no file written to shared/.

    Uses a tmpdir anchored under REPO_ROOT so dest_path.relative_to(REPO_ROOT) succeeds
    if _install is ever refactored to compute dest_path before the validation gate.
    """
    mod, err = _load_main()
    if mod is None:
        return False, err

    anchor = Path(tempfile.mkdtemp(dir=REPO_ROOT))
    try:
        skills_dir = anchor / "shared" / "skills"
        agent_dir = anchor / "shared" / "agent"
        setattr(mod, "SHARED_SKILLS_DIR", skills_dir)
        setattr(mod, "SHARED_AGENT_DIR", agent_dir)

        # Patch _run_validation to return False (validation failure)
        setattr(mod, "_run_validation", lambda *a, **k: False)

        cand_path = anchor / "my-test-skill.md"
        cand_path.write_text(_SKILL_CONTENT, encoding="utf-8")
        dest = skills_dir / "my-test-skill" / "SKILL.md"

        try:
            mod._install("skill", cand_path, install=True)
            return False, "_install should have raised SystemExit(1) when validation fails"
        except SystemExit as e:
            if e.code != 1:
                return False, f"Expected SystemExit(1), got SystemExit({e.code})"
            # Verify no file was written
            if dest.exists():
                return False, f"Validation-fail guard: dest file was written at {dest}"
            return True, "validation fail blocks install: SystemExit(1) raised; no file written"
        except Exception as e:
            return False, f"Unexpected exception: {e}"
    finally:
        shutil.rmtree(anchor, ignore_errors=True)


def check_shared_tree_untouched() -> tuple[bool, str]:
    """After all test scenarios, shared/ must be no dirtier than before the suite ran."""
    result = subprocess.run(
        ["git", "status", "--porcelain", "shared/"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return False, f"git status failed: {result.stderr.strip()}"
    output = result.stdout.strip()
    if output:
        # Emit a warning rather than a hard fail when the dirty state is pre-existing
        return False, (
            f"shared/ has uncommitted changes (may be pre-existing, not caused by tests): "
            f"{output!r}"
        )
    return True, "git status --porcelain shared/ is empty — real shared/ tree untouched"


def main() -> None:
    checks = [
        ("skill happy path: copies candidate to shared/skills/<slug>/SKILL.md", check_skill_happy_path),
        ("agent happy path: copies candidate to shared/agent/<slug>.md", check_agent_happy_path),
        ("conflict abort: SystemExit(1) when dest exists; no overwrite", check_conflict_abort),
        ("sync failure rollback: SystemExit(1) and dest deleted on non-zero sync exit", check_sync_failure_rollback),
        ("validation fail blocks install: SystemExit(1); no file written", check_validation_fail_blocks_install),
        ("shared tree untouched: git status --porcelain shared/ is empty", check_shared_tree_untouched),
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
