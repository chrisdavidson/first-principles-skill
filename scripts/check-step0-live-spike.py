#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Phase 71 spike: proves one bypass approach for STEP0-05.

Runs TWO fixtures (S-P01 + S-N01) once each over the Plan-36-locked transport.
Prints MODE for each and exits 0 if S-P01 classifies as focused-pre-mortem
(bypass confirmed), 1 otherwise.

DO NOT HARDEN — Phase 72 consumes this as a seed.

Usage:
    python3 scripts/check-step0-live-spike.py

Exit codes:
    0  bypass confirmed (S-P01 → focused-pre-mortem)
    1  bypass not confirmed (S-P01 did not produce focused-pre-mortem)
    2  environment error (claude CLI missing, plugin dir absent)

Approach: ② explicit Agent-tool invocation via meta-instruction wrapper.
The wrapper instructs the orchestrator to invoke the
first-principles:first-principles agent against the verbatim text with no
enrichment or interpretation. S-P01 ("run a pre-mortem on this launch") is
the unambiguous bypass discriminator — focused-pre-mortem can ONLY arise if
Step 0 saw the verbatim phrase, not an orchestrator-enriched restatement.

Captures: /tmp/step0-spike-S-P01.jsonl and /tmp/step0-spike-S-N01.jsonl
(transient, NOT committed).

Extension point for Phase 72: add --out-dir, --repeat (K-of-N), and full
fixture catalog coverage.
"""

from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Module-level constants (verbatim-move-from: _battery_core.py lines 64-65)
# ---------------------------------------------------------------------------

REPO_ROOT: Path = Path(__file__).resolve().parents[1]
DEFAULT_PLUGIN_DIR: Path = REPO_ROOT / "first-principles"

# ---------------------------------------------------------------------------
# Load detect_output_structure_from_file from _battery_core.py
# (importlib.util pattern; MUST pre-register in sys.modules — Pitfall 3)
# ---------------------------------------------------------------------------

_CORE: Path = Path(__file__).resolve().parent / "_battery_core.py"
_spec = importlib.util.spec_from_file_location("_battery_core", _CORE)
_mod = importlib.util.module_from_spec(_spec)  # type: ignore[arg-type]
sys.modules["_battery_core"] = _mod  # MUST precede exec_module (Pitfall 3)
_spec.loader.exec_module(_mod)  # type: ignore[union-attr]
detect_output_structure_from_file = _mod.detect_output_structure_from_file

# ---------------------------------------------------------------------------
# Spike fixtures — hardcoded from tests/step0-fixture-catalog.md rows 38, 44
# Run S-P01 FIRST (Pitfall 1 / S-P01-first execution order)
# ---------------------------------------------------------------------------

SPIKE_FIXTURES: list[dict[str, str]] = [
    {
        "id": "S-P01",
        "text": "run a pre-mortem on this launch",
        "expected": "focused-pre-mortem",
        "role": "focused-positive discriminating control — the bypass proof gate",
        "capture": "/tmp/step0-spike-S-P01.jsonl",
    },
    {
        "id": "S-N01",
        "text": (
            "The plan looks solid and the team is excited, but I am nervous. "
            "Before we lock it in, I want to surface every way this could blow up."
        ),
        "expected": "full-composer",
        "role": "oblique negative — interpretable ONLY if S-P01 passes",
        "capture": "/tmp/step0-spike-S-N01.jsonl",
    },
]


# ---------------------------------------------------------------------------
# Runtime guard (verbatim-copy-from: _battery_core.py lines 129-135)
# ---------------------------------------------------------------------------


def _ensure_claude_available() -> None:
    if shutil.which("claude") is None:
        print(
            "error: `claude` CLI not found on PATH; cannot run the sub-skill routing battery",
            file=sys.stderr,
        )
        sys.exit(2)


# ---------------------------------------------------------------------------
# Approach ② wrapper — the ONLY genuinely new logic in this seed
# ---------------------------------------------------------------------------


def _wrap_for_bypass(verbatim_text: str) -> str:
    """Approach ②: meta-instruction commanding verbatim Agent-tool invocation.

    Instructs the orchestrator to invoke the first-principles:first-principles
    agent against the verbatim text with no interpretation, enrichment, or
    clarification. The wrapper itself contains NO Step 0 trigger phrases
    (no "pre-mortem", "inversion", "fishbone", "five-whys", "trade-off",
    "second-order", "nervous about plan", etc.) — see Pitfall 2.

    Only the interpolated {verbatim_text} slot carries trigger phrases.
    """
    return (
        "Invoke the first-principles:first-principles agent with exactly this "
        "prompt, verbatim, without any modification, enrichment, or clarification:"
        "\n\n"
        '"""\n'
        f"{verbatim_text}\n"
        '"""\n\n'
        "Do not interpret or enrich the prompt. Pass it exactly as written to the agent."
    )


# ---------------------------------------------------------------------------
# Transport runner — Plan-36-locked argv (VERBATIM from _battery_core.py
# lines 159-172); only the final positional arg changes to _wrap_for_bypass(...)
# ---------------------------------------------------------------------------


def _run_prompt(verbatim_text: str, out_path: Path) -> Path:
    """Issue one prompt via claude -p and capture the stream-json log to out_path.

    Transport per D-10 (verbatim, copied from _battery_core.py _run_prompt_to):
        claude -p --plugin-dir <path> --no-session-persistence \\
          --output-format stream-json --verbose \\
          --permission-mode bypassPermissions <prompt>

    The final positional arg is _wrap_for_bypass(verbatim_text) (approach ②).
    Returns out_path.
    """
    plugin_dir: Path = DEFAULT_PLUGIN_DIR
    # Plan-36-locked — do not modify this argv list
    argv = [
        "claude",
        "-p",
        "--plugin-dir",
        str(plugin_dir),
        "--no-session-persistence",
        "--output-format",
        "stream-json",
        "--verbose",
        "--permission-mode",
        "bypassPermissions",
        _wrap_for_bypass(verbatim_text),
    ]
    proc = subprocess.run(
        argv,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    out_path.write_bytes(proc.stdout or b"")
    return out_path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    _ensure_claude_available()

    if not DEFAULT_PLUGIN_DIR.exists():
        print(
            f"error: plugin dir not found: {DEFAULT_PLUGIN_DIR}\n"
            "  Run: python3 scripts/sync-content.py --write",
            file=sys.stderr,
        )
        sys.exit(2)

    print(f"Plugin dir: {DEFAULT_PLUGIN_DIR}")
    print(f"Running {len(SPIKE_FIXTURES)} spike fixtures (S-P01 first — bypass gate)\n")

    results: dict[str, str] = {}

    for fixture in SPIKE_FIXTURES:
        fid = fixture["id"]
        text = fixture["text"]
        expected = fixture["expected"]
        role = fixture["role"]
        capture_path = Path(fixture["capture"])

        print(f"[{fid}] {role}")
        print(f"  prompt : {text!r}")
        print(f"  expected: {expected}")
        print(f"  capture : {capture_path}")
        print("  running...", flush=True)

        _run_prompt(text, capture_path)

        mode = detect_output_structure_from_file(capture_path)
        results[fid] = mode

        match_marker = "PASS" if mode == expected else "MISMATCH"
        print(f"  MODE    : {mode}  [{match_marker}]")
        print()

    # S-P01 is the bypass gate
    sp01_mode = results.get("S-P01", "none")
    sn01_mode = results.get("S-N01", "none")

    print("=" * 60)
    print(f"S-P01 MODE: {sp01_mode}")
    print(f"S-N01 MODE: {sn01_mode}")

    if sp01_mode == "focused-pre-mortem":
        print("\nRESULT: BYPASS CONFIRMED — approach ② proven (D-01)")
        print("  S-P01 produced focused-pre-mortem → verbatim prompt reached Step 0")
        print(f"  S-N01 produced {sn01_mode!r} (interpretable because S-P01 passed)")
        print("\nCaptures:")
        print(f"  {SPIKE_FIXTURES[0]['capture']}")
        print(f"  {SPIKE_FIXTURES[1]['capture']}")
        sys.exit(0)
    else:
        print(f"\nRESULT: BYPASS NOT CONFIRMED — S-P01 produced {sp01_mode!r} (expected focused-pre-mortem)")
        print("  approach ② did not bypass orchestrator enrichment")
        print("  Escalation: investigate candidate ① (synthesized stream-json envelope)")
        print("  See RESEARCH.md §'Failure / Escalation Path'")
        print("\nCaptures for inspection:")
        print(f"  {SPIKE_FIXTURES[0]['capture']}")
        print(f"  {SPIKE_FIXTURES[1]['capture']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
