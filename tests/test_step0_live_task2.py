"""RED test — Task 2 (72-01): offline --self-test with LOAD-BEARING none_with_dispatch.

These assertions document the TDD requirements for the self_test() function:
  - 4 fixture assertions including the LOAD-BEARING none_with_dispatch
  - K>N rejection sub-test (--repeat 2 --min-pass 3 exits 2)
  - Catalog parse sub-test
  - Fully offline (no claude, no network)
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
HARNESS = REPO_ROOT / "scripts" / "check-step0-live.py"


def _load_harness():
    spec = importlib.util.spec_from_file_location("check_step0_live_t2", HARNESS)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["check_step0_live_t2"] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def harness():
    return _load_harness()


def test_self_test_exits_0_offline():
    """--self-test must exit 0 offline without spawning claude."""
    result = subprocess.run(
        [sys.executable, str(HARNESS), "--self-test"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"--self-test exited {result.returncode}\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )


def test_self_test_prints_pass_anchor():
    """--self-test must print a line containing 'self-test PASS'."""
    result = subprocess.run(
        [sys.executable, str(HARNESS), "--self-test"],
        capture_output=True,
        text=True,
    )
    assert "self-test PASS" in result.stdout, (
        f"'self-test PASS' not found in stdout:\n{result.stdout}"
    )


def test_self_test_function_returns_0(harness):
    """self_test() function must return 0."""
    rc = harness.self_test()
    assert rc == 0, f"self_test() returned {rc}"


def test_self_test_does_not_invoke_claude():
    """--self-test must NOT spawn a claude process (offline boundary D-06).

    Verified by asserting --self-test succeeds even when 'claude' is patched
    to not be on PATH. Uses a wrapper script to avoid __file__ issues with exec.
    """
    wrapper = f"""
import importlib.util, sys, shutil
# Patch shutil.which so 'claude' appears absent
_orig_which = shutil.which
shutil.which = lambda n: None if n == 'claude' else _orig_which(n)

spec = importlib.util.spec_from_file_location("h", {str(HARNESS)!r})
mod = importlib.util.module_from_spec(spec)
sys.modules["h"] = mod
spec.loader.exec_module(mod)
# self_test must still pass even with no claude on PATH
sys.exit(mod.self_test())
"""
    result = subprocess.run(
        [sys.executable, "-c", wrapper],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"self_test() failed when claude was unavailable (not offline-safe!):\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )


def test_load_bearing_fixture_inference_guard(harness):
    """LOAD-BEARING: breaking the _classify_mode inference must flip none_with_dispatch to 'none'."""
    import json
    import tempfile

    # Build the none_with_dispatch fixture body
    dispatch_line = json.dumps({
        "type": "assistant",
        "message": {
            "content": [{
                "type": "tool_use",
                "name": "Agent",
                "input": {"subagent_type": "first-principles:first-principles", "prompt": "test"}
            }]
        }
    })
    clarification_line = json.dumps({
        "type": "assistant",
        "text": "I need more information to run the analysis."
    })

    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
        f.write(dispatch_line + "\n" + clarification_line + "\n")
        p = Path(f.name)

    try:
        # _classify_mode WITH inference: should return full-composer
        result_with_inference = harness._classify_mode(p)
        assert result_with_inference == "full-composer", (
            f"LOAD-BEARING fixture failed: expected 'full-composer', got {result_with_inference!r}"
        )

        # _agent_was_dispatched: must return True for this fixture
        dispatched = harness._agent_was_dispatched(p)
        assert dispatched is True, "LOAD-BEARING: _agent_was_dispatched must be True for dispatch fixture"

        # detect_output_structure_from_file alone (WITHOUT inference): returns 'none'
        raw_mode = harness.detect_output_structure_from_file(p)
        assert raw_mode == "none", (
            f"LOAD-BEARING: detect_output_structure_from_file should return 'none' "
            f"(inference is harness-side wrapper), got {raw_mode!r}"
        )
    finally:
        p.unlink(missing_ok=True)
