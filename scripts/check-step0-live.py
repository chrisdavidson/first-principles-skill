#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Live Step 0 harness — K-of-N classification and baseline recorder (STEP0-06).

Runs the full 35-row Step 0 fixture catalog (`tests/step0-fixture-catalog.md`)
over the proven approach-② `_wrap_for_bypass` bypass channel, classifies each
run's MODE from the captured `.jsonl` stream using `_classify_mode` (with the
harness-side `none`→`full-composer` inference fix — D-01/D-02), and scores
K-of-N matching the routing-battery convention (`--repeat 5 --min-pass 3`).

Designed to be run from `/tmp` with an absolute `--plugin-dir` path, matching
the routing battery methodology and eliminating project-context enrichment:

    REPO=/path/to/first-principles-skills
    cd /tmp && python3 "$REPO/scripts/check-step0-live.py" \\
        --catalog "$REPO/tests/step0-fixture-catalog.md" \\
        --plugin-dir "$REPO/first-principles" \\
        --repeat 5 --min-pass 3 \\
        --out /tmp/step0-live-$(date -u +%Y%m%dT%H%M%SZ) \\
        --baseline "$REPO/tests/step0-baseline-v7.13.md"

Usage:
    python3 scripts/check-step0-live.py [OPTIONS]

Options:
    --catalog PATH      Path to step0-fixture-catalog.md (required)
    --plugin-dir PATH   Path to first-principles plugin dir (default: repo-relative)
    --out-dir PATH      Output directory for .jsonl captures (default: /tmp/check-step0-live-<ts>)
    --repeat INT        Number of runs per fixture (default: 5)
    --min-pass INT      Minimum passing runs to score a row PASS (default: 3)
    --baseline PATH     If supplied, write the v7.13 baseline .md to this path
    --quiet             Suppress per-row progress output
    --dry-run           Parse catalog and print planned run without invoking claude
    --self-test         Run offline deterministic self-test and exit (no claude invoked)

Exit codes:
    0  BATTERY PASS (all rows reached min_pass, or self-test passed)
    1  BATTERY FAIL (one or more rows below min_pass, or self-test failed)
    2  Usage/environment error (bad --repeat/--min-pass, missing claude, stale agent body)

Renamed in place from scripts/check-step0-live-spike.py (Phase 71 seed — D-04).
The none→full-composer inference in _classify_mode is the harness-side D-01 fix.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

# ---------------------------------------------------------------------------
# Module-level constants (verbatim-move-from: spike lines 48-49)
# ---------------------------------------------------------------------------

REPO_ROOT: Path = Path(__file__).resolve().parents[1]
DEFAULT_PLUGIN_DIR: Path = REPO_ROOT / "first-principles"
_BASELINE_VERSION: str = "v7.13"

# ---------------------------------------------------------------------------
# Load _battery_core.py via importlib
# MUST pre-register in sys.modules BEFORE exec_module — Pitfall 3
# (Python 3.13 @dataclass(frozen=True) compat)
# ---------------------------------------------------------------------------

_CORE: Path = Path(__file__).resolve().parent / "_battery_core.py"
_spec = importlib.util.spec_from_file_location("_battery_core", _CORE)
_mod = importlib.util.module_from_spec(_spec)  # type: ignore[arg-type]
sys.modules["_battery_core"] = _mod  # MUST precede exec_module (Pitfall 3)
_spec.loader.exec_module(_mod)  # type: ignore[union-attr]

detect_output_structure_from_file = _mod.detect_output_structure_from_file
_run_prompt_n_times_to_paths = _mod._run_prompt_n_times_to_paths
_validate_kn = _mod._validate_kn
DEFAULT_PLUGIN_DIR = _mod.DEFAULT_PLUGIN_DIR  # noqa: F811 — override with _battery_core value

# ---------------------------------------------------------------------------
# Catalog data types
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Step0Prompt:
    """One row from the step0-fixture-catalog.md catalog."""

    id: str
    text: str      # verbatim prompt text
    expected: str  # expected MODE string (e.g. "focused-pre-mortem")


@dataclass(frozen=True)
class WrappedPrompt:
    """Duck-typed prompt carrying wrapped text for _run_prompt_n_times_to_paths."""

    id: str
    text: str  # = _wrap_for_bypass(verbatim_text)


@dataclass
class PromptResult:
    """Per-row K-of-N result."""

    prompt: Step0Prompt
    modes: list[str]   # len == repeat
    match_count: int   # how many runs matched expected
    row_pass: bool     # match_count >= min_pass


# ---------------------------------------------------------------------------
# KNOWN_MODES allowlist (validated at catalog parse time — T-72-01)
# ---------------------------------------------------------------------------

KNOWN_MODES: frozenset[str] = frozenset(
    {"full-composer"}
    | {
        f"focused-{t}"
        for t in (
            "pre-mortem",
            "inversion",
            "fishbone",
            "five-whys",
            "trade-off",
            "second-order",
            "identify-essence",
            "challenge-assumptions",
            "ground-truths",
            "reason-upward",
            "validate",
            # v7.6 8-technique re-baseline (Phase 108→v7.6): estimate and
            # theoretical-limit remain active Tier-1 techniques. The ninth
            # technique was merged into five-whys in v7.5 and its slug removed.
            # S-P16 routes to focused-five-whys (slug already present above).
            "estimate",
            "theoretical-limit",
        )
    }
)

# ---------------------------------------------------------------------------
# Catalog reader
# Model: check-step0-emulator.py _read_catalog (lines 230-287)
# ---------------------------------------------------------------------------


def _read_step0_catalog(path: Path) -> list[Step0Prompt]:
    """Parse step0-fixture-catalog.md into a list of Step0Prompt objects.

    Catalog columns: | ID | Prompt | Expected MODE | Notes |

    Skips header and separator rows. Validates Expected MODE against
    KNOWN_MODES allowlist; exits non-zero on unknown value (T-72-01).
    Preserves file order — S-P01 is always index 0.
    """
    text = path.read_text(encoding="utf-8")
    prompts: list[Step0Prompt] = []
    in_table = False
    expecting_separator = False
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            in_table = False
            expecting_separator = False
            continue
        cells = [c.strip() for c in stripped.split("|")]
        cells = [c for c in cells if c != ""]
        if not cells:
            continue
        if not in_table:
            if len(cells) >= 2 and cells[0].strip().upper() in ("ID", ""):
                in_table = True
                expecting_separator = True
            continue
        if expecting_separator:
            expecting_separator = False
            if all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
                continue
        if len(cells) < 3:
            continue
        row_id = cells[0]
        prompt_text = cells[1]
        expected_mode = cells[2]
        if expected_mode not in KNOWN_MODES:
            sys.stderr.write(
                f"_read_step0_catalog: FAIL — row {row_id}: "
                f"unrecognized MODE {expected_mode!r}\n"
                f"  Known modes: {sorted(KNOWN_MODES)}\n"
            )
            sys.exit(1)
        prompts.append(Step0Prompt(id=row_id, text=prompt_text, expected=expected_mode))
    if not prompts:
        raise ValueError(f"Catalog {path}: no rows parsed")
    return prompts


# ---------------------------------------------------------------------------
# Harness-side MODE classification with none→full-composer inference (D-01/D-02)
# ---------------------------------------------------------------------------


def _agent_was_dispatched(jsonl_path: Path) -> bool:
    """Return True if the capture shows first-principles:first-principles was dispatched.

    Scans the .jsonl for an assistant tool_use block with
    input.subagent_type == "first-principles:first-principles" (case-insensitive).
    Returns False on malformed/partial JSON lines without raising.
    """
    raw = jsonl_path.read_text(encoding="utf-8", errors="replace")
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("type") != "assistant":
            continue
        msg = obj.get("message", {})
        content = msg.get("content", []) if isinstance(msg, dict) else []
        for c in content if isinstance(content, list) else []:
            if not isinstance(c, dict):
                continue
            if c.get("type") != "tool_use":
                continue
            inp = c.get("input", {})
            subagent_type = inp.get("subagent_type", "") if isinstance(inp, dict) else ""
            if subagent_type.lower() == "first-principles:first-principles":
                return True
    return False


def _classify_mode(jsonl_path: Path) -> str:
    """Classify MODE from a captured .jsonl with harness-side none→full-composer inference.

    When detect_output_structure_from_file returns 'none' AND the capture shows
    Agent(subagent_type='first-principles:first-principles') was dispatched,
    the sub-agent ran but produced a non-structured response (e.g. clarification
    request — confirmed root cause of D-01 / S-N01). The dispatch proves Step 0
    chose the full-composer path, so reclassify as 'full-composer'.

    The inference is harness-side only — _battery_core.py is never modified (D-02).
    """
    mode = detect_output_structure_from_file(jsonl_path)
    if mode == "none" and _agent_was_dispatched(jsonl_path):
        return "full-composer"
    return mode


# ---------------------------------------------------------------------------
# Runtime guard (verbatim from spike lines 94-100)
# ---------------------------------------------------------------------------


def _ensure_claude_available() -> None:
    if shutil.which("claude") is None:
        print(
            "error: `claude` CLI not found on PATH; cannot run the Step 0 harness",
            file=sys.stderr,
        )
        sys.exit(2)


# ---------------------------------------------------------------------------
# Approach ② bypass wrapper (verbatim from spike lines 108-127 — FROZEN 71/D-09)
# ---------------------------------------------------------------------------


def _wrap_for_bypass(verbatim_text: str) -> str:
    """Approach ②: meta-instruction commanding verbatim Agent-tool invocation.

    Instructs the orchestrator to invoke the first-principles:first-principles
    agent against the verbatim text with no interpretation, enrichment, or
    clarification. The wrapper itself contains NO Step 0 trigger phrases
    (no "pre-mortem", "inversion", "fishbone", "five-whys", "trade-off",
    "second-order", "nervous about plan", etc.) — see Pitfall 2.

    Only the interpolated {verbatim_text} slot carries trigger phrases.
    FROZEN — copy verbatim per 71/D-09. Never add technique keywords.
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
# Offline --self-test fixtures (D-06)
# ---------------------------------------------------------------------------


def _fixture_assistant_text(text: str) -> str:
    """Build a one-line stream-json blob with assistant text."""
    return json.dumps({"type": "assistant", "text": text})


def _fixture_agent_dispatch(subagent_type: str, prompt: str) -> str:
    """Build a stream-json line with an Agent tool_use dispatch."""
    return json.dumps({
        "type": "assistant",
        "message": {
            "content": [{
                "type": "tool_use",
                "name": "Agent",
                "input": {"subagent_type": subagent_type, "prompt": prompt},
            }]
        },
    })


# Fixture A: focused-pre-mortem (>=2 distinct pre-mortem markers)
_FIXTURE_ST_FOCUSED_PREMORTEM = "\n".join([
    _fixture_assistant_text(
        "Prospective-hindsight: the plan has already failed. What caused it?\n"
        "Working backward: what caused the rollout to stall?"
    ),
])

# Fixture B: full-composer via structural override (>=2 composer scaffold sections)
_FIXTURE_ST_FULL_COMPOSER = "\n".join([
    _fixture_assistant_text(
        "## Phase 1 — Ground Truths\nFact A.\n\n"
        "## Phase 2 — Assumption Audit\nUntested: B.\n\n"
        "## Phase 3 — Verdict\nProceed.\n"
    ),
])

# Fixture C: none + agent dispatch → _classify_mode returns full-composer
# LOAD-BEARING: this fixture guards the D-01 none→full-composer inference fix.
# Removing _classify_mode's inference logic causes this fixture to return 'none'
# and fail the self-test.
_FIXTURE_ST_NONE_WITH_DISPATCH = "\n".join([
    _fixture_agent_dispatch(
        "first-principles:first-principles",
        "The plan looks solid. Surface failure modes.",
    ),
    _fixture_assistant_text(
        "I need more information about the plan to run the analysis. "
        "Please share the plan details."
    ),
])

# Fixture D: none WITHOUT dispatch → _classify_mode returns none (inference does NOT fire)
_FIXTURE_ST_NONE_NO_DISPATCH = "\n".join([
    _fixture_assistant_text("Hello world. No methodology markers present."),
])


def _run_one_fixture_step0(name: str, body: str, expected: str) -> bool:
    """Run one self-test fixture and return True if _classify_mode matches expected."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".jsonl", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(body)
        tmp_path = Path(tmp.name)
    try:
        actual = _classify_mode(tmp_path)
        if actual != expected:
            print(
                f"self-test FAIL: {name!r} expected {expected!r}, got {actual!r}",
                file=sys.stderr,
            )
            return False
        return True
    finally:
        try:
            tmp_path.unlink()
        except OSError:
            pass


def self_test() -> int:
    """Run offline deterministic self-test. Returns 0 on full pass, 1 on any failure.

    No claude process is spawned and no network is used.
    Tests: 4 fixtures + K>N rejection + catalog parse.
    """
    all_passed = True

    # --- 4 classification fixtures ---
    for name, body, expected in [
        ("focused_premortem", _FIXTURE_ST_FOCUSED_PREMORTEM, "focused-pre-mortem"),
        ("full_composer_structural", _FIXTURE_ST_FULL_COMPOSER, "full-composer"),
        # LOAD-BEARING: removing the _classify_mode inference flips this to 'none'
        ("none_with_dispatch_LOAD_BEARING", _FIXTURE_ST_NONE_WITH_DISPATCH, "full-composer"),
        ("none_without_dispatch", _FIXTURE_ST_NONE_NO_DISPATCH, "none"),
    ]:
        if not _run_one_fixture_step0(name, body, expected):
            all_passed = False

    # --- K>N rejection sub-test ---
    # --repeat 2 --min-pass 3 is invalid (3 > 2); _validate_kn must return exit code 2
    try:
        rc = main(["--catalog", "/nonexistent", "--repeat", "2", "--min-pass", "3"])
    except SystemExit as e:
        rc = e.code if isinstance(e.code, int) else 2
    if rc != 2:
        print(
            f"self-test FAIL: K>N guard — expected exit 2 for --repeat 2 --min-pass 3, got {rc}",
            file=sys.stderr,
        )
        all_passed = False

    # --- Catalog parse sub-test ---
    # Valid rows: parse succeeds and returns correct objects
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, encoding="utf-8"
    ) as tf:
        tf.write(
            "| ID | Prompt | Expected MODE | Notes |\n"
            "|---|--------|--------------|-------|\n"
            "| S-P01 | run a pre-mortem on this launch | focused-pre-mortem | ok |\n"
            "| S-N01 | oblique full-composer prompt | full-composer | ok |\n"
        )
        cat_path = Path(tf.name)
    try:
        rows = _read_step0_catalog(cat_path)
        if len(rows) != 2 or rows[0].id != "S-P01" or rows[1].expected != "full-composer":
            print(
                f"self-test FAIL: catalog parse — expected 2 rows with S-P01 first, got {rows}",
                file=sys.stderr,
            )
            all_passed = False
    finally:
        try:
            cat_path.unlink()
        except OSError:
            pass

    # Verify unknown-mode detection causes sys.exit(non-zero)
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, encoding="utf-8"
    ) as tf:
        tf.write(
            "| ID | Prompt | Expected MODE | Notes |\n"
            "|---|--------|--------------|-------|\n"
            "| S-P99 | some prompt | unknown-xyzzy-mode | bad |\n"
        )
        bad_cat_path = Path(tf.name)
    try:
        try:
            _read_step0_catalog(bad_cat_path)
            print(
                "self-test FAIL: catalog parse — unknown mode should have exited non-zero",
                file=sys.stderr,
            )
            all_passed = False
        except SystemExit as e:
            if e.code == 0:
                print(
                    "self-test FAIL: catalog parse — unknown mode exit code was 0 (expected non-zero)",
                    file=sys.stderr,
                )
                all_passed = False
            # non-zero exit is correct
    finally:
        try:
            bad_cat_path.unlink()
        except OSError:
            pass

    # --- _apply_priority reorder sub-test (READY-03 / D-03) ---
    # Build four in-memory rows — IDs deliberately chosen from the 8-technique
    # canonical set so no scrubbed literal appears here.
    _prows = [
        Step0Prompt(id="S-P01", text="t1", expected="focused-pre-mortem"),
        Step0Prompt(id="S-P04", text="t4", expected="focused-five-whys"),
        Step0Prompt(id="S-P10", text="t10", expected="focused-estimate"),
        Step0Prompt(id="S-P16", text="t16", expected="focused-five-whys"),
    ]
    _prows_ids_before = [r.id for r in _prows]  # snapshot for immutability check
    # With [] (flag present, no value) → uses DEFAULT_PRIORITY_IDS = (S-P04, S-P16) first
    _reordered = _apply_priority(_prows, [])
    _expected_order = ["S-P04", "S-P16", "S-P01", "S-P10"]
    _actual_order = [r.id for r in _reordered]
    if _actual_order != _expected_order:
        print(
            f"self-test FAIL: priority-subset reorder — expected {_expected_order}, got {_actual_order}",
            file=sys.stderr,
        )
        all_passed = False
    # With None → passthrough (unchanged order)
    _passthrough = _apply_priority(_prows, None)
    _passthrough_order = [r.id for r in _passthrough]
    if _passthrough_order != _prows_ids_before:
        print(
            f"self-test FAIL: priority-subset None passthrough — expected {_prows_ids_before}, got {_passthrough_order}",
            file=sys.stderr,
        )
        all_passed = False
    # Input list must not be mutated by either call
    _prows_ids_after = [r.id for r in _prows]
    if _prows_ids_after != _prows_ids_before:
        print(
            f"self-test FAIL: priority-subset mutated input — before {_prows_ids_before}, after {_prows_ids_after}",
            file=sys.stderr,
        )
        all_passed = False

    # --- /8 tally drift guard (READY-03 / D-03) ---
    # Assert the 8-technique canonical tally count exactly, without naming any scrubbed ID.
    # A len mismatch means a technique was added or removed and this guard must be updated.
    if len(CANONICAL_TALLY_IDS) != 8:
        print(
            f"self-test FAIL: /8-tally drift — expected len(CANONICAL_TALLY_IDS)==8, got {len(CANONICAL_TALLY_IDS)}",
            file=sys.stderr,
        )
        all_passed = False

    # --- KNOWN_MODES size drift guard (READY-03 / D-03) ---
    # The 8-technique set produces exactly 14 KNOWN_MODES entries:
    #   1 × full-composer + 13 × focused-<technique> (including estimate + theoretical-limit,
    #   excluding the ninth technique removed in v7.5). If the count rises to 15 a scrubbed
    #   slug was re-introduced; if it falls below 14 an active technique was lost.
    if len(KNOWN_MODES) != 14:
        print(
            f"self-test FAIL: KNOWN_MODES size drift — expected 14, got {len(KNOWN_MODES)}",
            file=sys.stderr,
        )
        all_passed = False

    # --- D-01a firewall: failing S-P16 does not crash _write_baseline or flip battery ---
    # Build a synthetic results list: all 8 canonical rows PASS + S-P16 FAILS.
    # Assert (a) _write_baseline writes without raising (CR-01 regression guard),
    # and (b) _battery_gate returns battery_pass=True (WR-01 regression guard).
    _d01a_args = argparse.Namespace(repeat=5, min_pass=3)
    _d01a_canonical = [
        PromptResult(
            prompt=Step0Prompt(id=cid, text="t", expected="focused-pre-mortem"),
            modes=["focused-pre-mortem"] * 5,
            match_count=5,
            row_pass=True,
        )
        for cid in CANONICAL_TALLY_IDS
    ]
    _d01a_sp16 = PromptResult(
        prompt=Step0Prompt(id="S-P16", text="t16", expected="focused-five-whys"),
        modes=["full-composer"] * 5,
        match_count=0,
        row_pass=False,
    )
    _d01a_results = _d01a_canonical + [_d01a_sp16]
    # (a) _write_baseline must write without ValueError
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, encoding="utf-8"
    ) as _d01a_tf:
        _d01a_path = Path(_d01a_tf.name)
    try:
        try:
            _write_baseline(_d01a_results, _d01a_args, _d01a_path,
                            recorded_ts="2026-01-01T00:00:00Z")
        except ValueError as _e:
            print(
                f"self-test FAIL: D-01a failing-S-P16 firewall — "
                f"_write_baseline raised ValueError: {_e}",
                file=sys.stderr,
            )
            all_passed = False
        except Exception as _e:
            print(
                f"self-test FAIL: D-01a failing-S-P16 firewall — "
                f"_write_baseline raised unexpected exception: {_e}",
                file=sys.stderr,
            )
            all_passed = False
    finally:
        try:
            _d01a_path.unlink()
        except OSError:
            pass
    # (b) _battery_gate must return battery_pass=True with all canonical rows PASS + S-P16 FAIL
    _d01a_p_rows = [r for r in _d01a_results if r.prompt.id.startswith("S-P")]
    _d01a_n_rows = [r for r in _d01a_results if r.prompt.id.startswith("S-N")]
    _, _, _, _d01a_battery_pass = _battery_gate(_d01a_p_rows, _d01a_n_rows)
    if not _d01a_battery_pass:
        print(
            "self-test FAIL: D-01a failing-S-P16 firewall — "
            "_battery_gate returned battery_pass=False with all canonical rows passing "
            "(failing S-P16 must not flip the battery — WR-01)",
            file=sys.stderr,
        )
        all_passed = False

    # --- D-01a firewall: failing S-N row does not crash _write_baseline (WR-04) ---
    # Build a synthetic results list: all 8 canonical rows PASS + S-N01 FAILS.
    # Assert _write_baseline writes without raising (WR-04 regression guard).
    _d01a_sn01 = PromptResult(
        prompt=Step0Prompt(id="S-N01", text="oblique prompt", expected="full-composer"),
        modes=["focused-pre-mortem"] * 5,   # over-routes — fails
        match_count=0,
        row_pass=False,
    )
    _d01a_sn_results = _d01a_canonical + [_d01a_sn01]
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, encoding="utf-8"
    ) as _d01a_sn_tf:
        _d01a_sn_path = Path(_d01a_sn_tf.name)
    try:
        try:
            _write_baseline(_d01a_sn_results, _d01a_args, _d01a_sn_path,
                            recorded_ts="2026-01-01T00:00:00Z")
        except ValueError as _e:
            print(
                f"self-test FAIL: D-01a failing-S-N firewall — "
                f"_write_baseline raised ValueError on failing S-N01: {_e}",
                file=sys.stderr,
            )
            all_passed = False
        except Exception as _e:
            print(
                f"self-test FAIL: D-01a failing-S-N firewall — "
                f"_write_baseline raised unexpected exception on failing S-N01: {_e}",
                file=sys.stderr,
            )
            all_passed = False
    finally:
        try:
            _d01a_sn_path.unlink()
        except OSError:
            pass

    # --- NON-BLOCK-NEG: non-blocking negative semantics (D-16/D-17) ---
    # Assert (a) a synthetic results set with all 8 canonical positives PASS +
    # S-N04 FAILS returns battery_pass=True (S-N04 is non-blocking); and
    # (b) the same set with S-N01 FAILS instead returns battery_pass=False
    # (S-N01 is a blocking oblique negative).
    _nb_canonical = [
        PromptResult(
            prompt=Step0Prompt(id=cid, text="t", expected="focused-pre-mortem"),
            modes=["focused-pre-mortem"] * 5,
            match_count=5,
            row_pass=True,
        )
        for cid in CANONICAL_TALLY_IDS
    ]
    _nb_sn04_fail = PromptResult(
        prompt=Step0Prompt(id="S-N04", text="walk through failure modes", expected="full-composer"),
        modes=["focused-pre-mortem"] * 5,
        match_count=0,
        row_pass=False,
    )
    _nb_sn01_fail = PromptResult(
        prompt=Step0Prompt(id="S-N01", text="oblique prompt", expected="full-composer"),
        modes=["focused-pre-mortem"] * 5,
        match_count=0,
        row_pass=False,
    )
    # (a) Failing S-N04 must NOT flip battery (non-blocking)
    _, _, _, _nb_bp_sn04 = _battery_gate(_nb_canonical, [_nb_sn04_fail])
    if not _nb_bp_sn04:
        print(
            "self-test FAIL: NON-BLOCK-NEG — failing S-N04 flipped battery_pass=False "
            "(S-N04 must be excluded from the blocking negative bar via "
            "NON_BLOCKING_NEGATIVE_IDS; D-16/D-17)",
            file=sys.stderr,
        )
        all_passed = False
    # (b) Failing S-N01 MUST flip battery (blocking)
    _, _, _, _nb_bp_sn01 = _battery_gate(_nb_canonical, [_nb_sn01_fail])
    if _nb_bp_sn01:
        print(
            "self-test FAIL: NON-BLOCK-NEG — failing S-N01 did NOT flip battery_pass=False "
            "(S-N01 must remain a blocking negative; D-16/D-17)",
            file=sys.stderr,
        )
        all_passed = False

    # --- scrubbed-slug absence guard (READY-01 / D-02) ---
    # Reads this file's own source and asserts the three scrubbed slugs are absent.
    # Tokens built by fragment concatenation so no forbidden literal appears verbatim;
    # any re-introduction would trip this guard and turn STEP0-06 red.
    _dca_label = "de" + "compose-absence"
    _own_src = Path(__file__).read_text(encoding="utf-8")
    for _tok in [
        "de" + "com" + "pose",
        "S" + "-P" + "09",
        "focused-" + "de" + "com" + "pose",
    ]:
        if _tok in _own_src:
            print(
                f"self-test FAIL: {_dca_label} drift"
                f" — {_tok!r} reappeared in check-step0-live.py",
                file=sys.stderr,
            )
            all_passed = False

    # --- routing-count drift guard (READY-01 / D-02) ---
    # Asserts tests/routing-catalog.md parses to exactly 13 P / 20 N,
    # reusing the live check-routing.parse_catalog (no hand-rolled parser).
    _rcheck_path = Path(__file__).resolve().parent / "check-routing.py"
    _rcheck_spec = importlib.util.spec_from_file_location("_check_routing_module", _rcheck_path)
    _rcheck_mod = importlib.util.module_from_spec(_rcheck_spec)  # type: ignore[arg-type]
    sys.modules["_check_routing_module"] = _rcheck_mod
    _rcheck_spec.loader.exec_module(_rcheck_mod)  # type: ignore[union-attr]
    _rc_pos, _rc_neg = _rcheck_mod.parse_catalog(REPO_ROOT / "tests" / "routing-catalog.md")
    if len(_rc_pos) != 13 or len(_rc_neg) != 20:
        print(
            f"self-test FAIL: routing-count drift"
            f" — expected 13 P / 20 N, got {len(_rc_pos)}/{len(_rc_neg)}",
            file=sys.stderr,
        )
        all_passed = False

    # --- v7.13 emitter-target drift guard (D-06 / Phase 135) ---
    # Pins _BASELINE_VERSION == "v7.13" and asserts the three emitter-derived
    # strings contain "v7.13" and not "v7.6" / "v7.8" / "v7.11".  The not-stale
    # check is scoped to these three strings ONLY — the lineage prose legitimately
    # cites the prior v7.11 baseline as a comparison anchor, so a whole-file grep
    # for "v7.11" would produce false failures.
    _v713_label = "v7.13-emitter-target"
    if _BASELINE_VERSION != "v7.13":
        print(
            f"self-test FAIL: {_v713_label} — _BASELINE_VERSION is {_BASELINE_VERSION!r},"
            f" expected 'v7.13'",
            file=sys.stderr,
        )
        all_passed = False
    # Construct the three emitter-derived strings the same way _write_baseline does.
    _v713_header = f"# Step 0 Live Harness Baseline — {_BASELINE_VERSION}"
    _v713_out_dir = f"/tmp/step0-live-{_BASELINE_VERSION}-placeholder"
    _v713_baseline = f"step0-baseline-{_BASELINE_VERSION}.md"
    for _v713_label_str, _v713_s in [
        ("header", _v713_header),
        ("OUT_DIR", _v713_out_dir),
        ("--baseline", _v713_baseline),
    ]:
        if "v7.13" not in _v713_s:
            print(
                f"self-test FAIL: {_v713_label} — {_v713_label_str!r} string"
                f" does not contain 'v7.13': {_v713_s!r}",
                file=sys.stderr,
            )
            all_passed = False
        for _stale in ("v7.6", "v7.8", "v7.11"):
            if _stale in _v713_s:
                print(
                    f"self-test FAIL: {_v713_label} — {_v713_label_str!r} string"
                    f" contains stale {_stale!r}: {_v713_s!r}",
                    file=sys.stderr,
                )
                all_passed = False

    # --- routing-emitter-absence guard (READY-02 / D-05 confirm-only) ---
    # Asserts neither check-routing.py nor check-routing-battery.py contains a
    # version-driven emitter (i.e. the _BASELINE_VERSION token is absent from
    # both routing scripts). This makes "routing scripts stay emitter-free" a
    # CI-gated regression assertion — not a no-op edit (D-02) — and explicitly
    # does NOT add any emitter machinery to the routing scripts (D-03).
    # The guard searches the routing files only (naturally safe; no fragment
    # concatenation needed since check-step0-live.py itself is never searched here).
    _rea_label = "routing-emitter-absence"
    _routing_scripts = [
        Path(__file__).resolve().parent / "check-routing.py",
        Path(__file__).resolve().parent / "check-routing-battery.py",
    ]
    _emitter_token = "_BASELINE_VERSION"
    for _rscript in _routing_scripts:
        try:
            _rsrc = _rscript.read_text(encoding="utf-8")
        except OSError as _e:
            print(
                f"self-test FAIL: {_rea_label} — could not read {_rscript.name}: {_e}",
                file=sys.stderr,
            )
            all_passed = False
            continue
        if _emitter_token in _rsrc:
            print(
                f"self-test FAIL: {_rea_label} — {_emitter_token!r} appeared in"
                f" {_rscript.name} (routing scripts must stay emitter-free; D-05)",
                file=sys.stderr,
            )
            all_passed = False

    # --- rr-id-coverage drift guard (CR-01 structural hole-closer, STEP0-06) ---
    # Parse the live catalog and assert every residual-reachable row ID has a
    # non-None entry in _RR_ID_MAP. This prevents a catalog-grows-but-map-doesn't-update
    # regression from silently passing STEP0-06 while _write_baseline would crash
    # on a live run (the exact class of defect that CR-01 found in Phase 128).
    _rr_cov_label = "rr-id-coverage"
    _rr_cov_catalog_path = REPO_ROOT / "tests" / "step0-fixture-catalog.md"
    try:
        _rr_cov_catalog = _read_step0_catalog(_rr_cov_catalog_path)
        # Reachable = rows that the live invocation loop runs AND that reach the
        # generic else branch in _write_baseline's verdict loop. The live path
        # excludes S-A rows before invoking; CONTEXT_FREE_IDS and
        # MERGE_VALIDATION_IDS are handled by their own branches and never reach
        # residual_risk_rows. Any unmapped row that slips through would raise
        # ValueError in _write_baseline after 145 live invocations.
        _rr_cov_reachable = {
            row.id for row in _rr_cov_catalog
            if not row.id.startswith("S-A")
            and row.id not in CONTEXT_FREE_IDS
            and row.id not in MERGE_VALIDATION_IDS
        }
        _rr_cov_missing = sorted(
            rid for rid in _rr_cov_reachable if _RR_ID_MAP.get(rid) is None
        )
        if _rr_cov_missing:
            print(
                f"self-test FAIL: {_rr_cov_label} — catalog rows reachable by"
                f" _write_baseline but missing from _RR_ID_MAP: {_rr_cov_missing}."
                f" Add each ID to _RR_ID_MAP with an appropriate RR tracking ID.",
                file=sys.stderr,
            )
            all_passed = False
    except Exception as _rr_cov_err:
        print(
            f"self-test FAIL: {_rr_cov_label} — could not parse catalog"
            f" {_rr_cov_catalog_path}: {_rr_cov_err}",
            file=sys.stderr,
        )
        all_passed = False

    if all_passed:
        print(
            "self-test PASS (4 fixtures + K>N rejection + catalog parse + priority-subset"
            " + /8-tally + failing-S-P16 firewall + failing-S-N firewall"
            f" + non-blocking-S-N04 + {_dca_label} + routing-count"
            f" + {_v713_label} + {_rea_label} + {_rr_cov_label})"
        )
        return 0
    return 1


# ---------------------------------------------------------------------------
# Baseline emitter
# ---------------------------------------------------------------------------

# Context-free / alternation-falsifier fixtures: catalog rows that guard the
# offline pipe-split parser (an emulator concern), not live technique routing.
# They are MEASURED and RECORDED but EXCLUDED from the 8-technique tally (D-01a).
# v5.1 origin: S-P07/08 (context-free). v7.4 (Phase 108, D-01a): extended to the
# full 6-falsifier set so a falsifier failure never breaks the technique bar and
# never over-weights estimate (4 rows) / theoretical-limit (1 extra row).
CONTEXT_FREE_IDS = ("S-P07", "S-P08", "S-P11", "S-P12", "S-P13", "S-P15")

# Merge-validation row: tracked OUTSIDE the /8 canonical bar (D-01a).
# S-P16 answers "did the five-whys consolidation re-home the absorbed trigger?"
# It is reported via a dedicated _s_p16_result Summary line and must never reach
# residual_risk_rows or _battery_gate's p_context — it is neither a canonical
# technique row nor a context-free falsifier.
MERGE_VALIDATION_IDS = ("S-P16",)

# Non-blocking negative: S-N04 is MEASURED and RECORDED in every run but is
# EXCLUDED from the blocking negative bar. S-N04's prompt ("walk through how
# this could go badly — what failure modes should we prepare for?") is
# semantically a pre-mortem request; the live agent legitimately routes it to
# a focused pre-mortem (evidence from Phase 117 CONF-01: over-routes even with
# FIX-01 reverted, ~1/5 without the fix — genuine routing, not a detector
# artifact). Its v7.6 "3/5 PASS" was partly a detector false-negative (the
# weaker v7.6 detector failed to recognise the pre-mortem the agent was already
# running). The blocking oblique negatives are S-N01/S-N02/S-N03.
# S-N04 STAYS an emulator/phrase-table negative (STEP0-08 unchanged — it fires
# NO Step 0 trigger phrase); it is live non-blocking only (D-16/D-17).
# Phase 117 re-scope, D-16/D-17.
NON_BLOCKING_NEGATIVE_IDS = ("S-N04",)

# The 8 canonical positive rows — one per technique (D-01) — over which the
# v7.13 8-technique pass-rate is computed. The instrument emits this per-technique
# tally (D-01b, REBASE-02), it is not hand-assembled. All 8 techniques have a
# v7.8 prior K/N; there is no "newly-measured" subset in this re-measure.
CANONICAL_TALLY_IDS = (
    "S-P01",  # pre-mortem
    "S-P02",  # inversion
    "S-P03",  # fishbone
    "S-P04",  # five-whys
    "S-P05",  # trade-off
    "S-P06",  # second-order
    "S-P10",  # estimate
    "S-P14",  # theoretical-limit
)

# Default merge-validation priority subset (D-02): the two rows that answer
# "did the five-whys consolidation improve routing?". Running these first
# guarantees the core finding lands even if a spend cutoff hits mid-run.
# S-P04 = five-whys (the surviving technique); S-P16 = the absorbed trigger
# re-homed to focused-five-whys (merge-validation signal, outside /8).
DEFAULT_PRIORITY_IDS: tuple[str, ...] = ("S-P04", "S-P16")

# D-03/D-04 — _RR_ID_MAP carries the residual-tracking IDs for this v7.13
# re-measure of RR-130-01 fix + Step 0 deferred residuals (Phase 135-137, uncapped — no spend-limit
# constraint; all 29 S-P/S-N fixture rows measured, S-A excluded from live run).
# Residual state entering this run:
#   - RR-114-01 (S-P02 inversion): v7.6 live 1/5 < min-pass → CARRIED FORWARD.
#     RESOLVED-STRUCTURALLY-OFFLINE Phase 121 OCH-02: detector extended 9→13
#     markers; offline proof shows detector CAN read the new headers. Live
#     pass-rate re-measure is the deliverable of this v7.11 run. May be CLOSED
#     (≥3/5) or CARRIED FORWARD under a fresh Phase-129 RR ID (post-run mint).
#   - RR-108-04 (S-P10 estimate): v7.6 spend-limit-indeterminate (all 5 runs
#     truncated → `none`). This v7.11 run is uncapped — a clean measurement is
#     expected. May be CLOSED (≥3/5) or CARRIED FORWARD (fresh ID, post-run).
#   - RR-108-05 (S-P14 theoretical-limit): v7.6 spend-limit-indeterminate (all
#     5 runs truncated → `none`). Same — uncapped; clean measurement expected.
#     May be CLOSED or CARRIED FORWARD (fresh ID, post-run).
# RR-108-02 (S-P05 trade-off) is CLOSED (Phase 114, live 4/5 ≥ min-pass).
# No provisional placeholder survives. The falsifier rows still need a tracked
# ID for the invariant safety net (they are handled by the CONTEXT_FREE branch
# and never reach residual_risk_rows, but a non-None entry is required); they
# share the closest minted canonical-technique ID for their falsified technique.
# Module-level constant so both _write_baseline and self_test() reference the
# same object — drift-proofing against RR_ID_MAP growing stale (CR-01).
_RR_ID_MAP: dict[str, str] = {
    "S-P01": "RR-79-01", "S-P02": "RR-114-01", "S-P03": "RR-75-03",
    "S-P04": "RR-75-04", "S-P05": "RR-108-02", "S-P06": "RR-75-06",
    "S-N04": "RR-80-01",
    # Negative-control rows that dipped below min_pass on this run ONLY because
    # of spend-limit `none` truncation (no routing happened), NOT genuine
    # over-routing. They reach residual_risk_rows when failing, so they need a
    # tracked ID for the safety-net invariant. Mapped to a single infra ID
    # (RR-108-06) — they are NOT a routing residual.
    "S-N06": "RR-108-06",  # spend-limit truncation (infra), not a routing residual
    "S-N07": "RR-108-06",  # spend-limit truncation (infra), not a routing residual
    # Live negative-control over-routing rows (WR-04): S-N01/02/03/08 are
    # canonical oblique prompts. An over-route (row_pass=False) is a
    # high-signal result — they get a tracked infra ID so a failing row never
    # aborts the run. RR-108-08 = live negative-control over-routing signal.
    "S-N01": "RR-108-08",  # over-routing negative-control (live oblique prompt)
    "S-N02": "RR-108-08",  # over-routing negative-control (live oblique prompt)
    "S-N03": "RR-108-08",  # over-routing negative-control (live oblique prompt)
    "S-N08": "RR-108-08",  # over-routing negative-control (live oblique prompt)
    # Guard-suppressed / oblique pre-mortem-flavored negatives (molten-salt-TES
    # domain). Same class as S-N01/02/03/08 — an over-route is a high-signal
    # result; they get the same tracked infra ID (RR-108-08) so a failing row
    # never aborts the run.
    "S-N09": "RR-108-08",  # over-routing negative-control (guard-suppressed / oblique)
    "S-N10": "RR-108-08",  # over-routing negative-control (guard-suppressed / oblique)
    "S-N11": "RR-108-08",  # over-routing negative-control (guard-suppressed / oblique)
    "S-N12": "RR-108-08",  # over-routing negative-control (guard-suppressed / oblique)
    "S-N13": "RR-108-08",  # over-routing negative-control (guard-suppressed / oblique)
    "S-N14": "RR-108-08",  # over-routing negative-control (guard-suppressed / oblique)
    "S-N15": "RR-108-08",  # over-routing negative-control (guard-suppressed / oblique)
    # Canonical techniques with v7.6 spend-limit-indeterminate residuals. These CAN
    # reach the residual-risk branch if below min-pass in this v7.13 run.
    "S-P10": "RR-108-04",  # estimate          (v7.6 spend-limit-indeterminate)
    "S-P14": "RR-108-05",  # theoretical-limit (v7.6 spend-limit-indeterminate)
    # Falsifier rows (handled by the CONTEXT_FREE branch in the verdict loop;
    # never appended to residual_risk_rows) — share the minted ID of the
    # technique they falsify so no provisional placeholder survives.
    "S-P07": "RR-79-01",   # pre-mortem falsifier
    "S-P08": "RR-79-01",   # pre-mortem falsifier
    "S-P11": "RR-108-04",  # estimate falsifier
    "S-P12": "RR-108-04",  # estimate falsifier
    "S-P13": "RR-108-04",  # estimate falsifier
    "S-P15": "RR-108-05",  # theoretical-limit falsifier
}


def _apply_priority(
    catalog: list[Step0Prompt], priority: list[str] | None
) -> list[Step0Prompt]:
    """Return a NEW stably-reordered catalog with priority rows first.

    If priority is None, returns a copy of the catalog in unchanged order.
    Otherwise, computes priority_ids = priority (if non-empty) or
    DEFAULT_PRIORITY_IDS (if --priority flag was given with no value, so
    args.priority == []), builds a set, and returns front + rest where:
      front = rows whose id is in the priority set (file order preserved)
      rest  = remaining rows (file order preserved)

    Never mutates the input list. Safe to call with an empty priority list
    (falls back to DEFAULT_PRIORITY_IDS).
    """
    if priority is None:
        return list(catalog)
    priority_ids: set[str] = set(priority) if priority else set(DEFAULT_PRIORITY_IDS)
    front = [p for p in catalog if p.id in priority_ids]
    rest = [p for p in catalog if p.id not in priority_ids]
    return front + rest


def _battery_gate(
    p_rows: list[PromptResult], n_rows: list[PromptResult]
) -> tuple[list[PromptResult], int, int, bool]:
    """v5.1 split battery gate, shared by the baseline emitter and main()'s
    exit code so the two can never drift (CR-01). Three exclusion sets apply:
    - CONTEXT_FREE_IDS (6 rows: S-P07/08/11/12/13/15) — alternation-falsifier
      fixtures excluded from the technique bar.
    - MERGE_VALIDATION_IDS (S-P16) — merge-validation signal tracked outside
      the /8 canonical bar (D-01a).
    - NON_BLOCKING_NEGATIVE_IDS (S-N04) — semantically a pre-mortem request;
      the live agent legitimately routes it to a focused pre-mortem; MEASURED
      and RECORDED but excluded from the blocking negative bar (D-16/D-17).
      The blocking oblique negatives are S-N01/S-N02/S-N03.
    The gate is (all len(CANONICAL_TALLY_IDS)==8 canonical rows pass) AND
    (all blocking S-N pass). Returns (p_context, p_context_pass, n_pass,
    battery_pass) where n_pass counts only blocking negatives."""
    p_context = [
        r for r in p_rows
        if r.prompt.id not in CONTEXT_FREE_IDS
        and r.prompt.id not in MERGE_VALIDATION_IDS
    ]
    p_context_pass = sum(1 for r in p_context if r.row_pass)
    n_blocking = [r for r in n_rows if r.prompt.id not in NON_BLOCKING_NEGATIVE_IDS]
    n_pass = sum(1 for r in n_blocking if r.row_pass)
    battery_pass = (p_context_pass == len(p_context)) and (n_pass == len(n_blocking))
    return p_context, p_context_pass, n_pass, battery_pass


def _write_baseline(
    results: list[PromptResult],
    args: argparse.Namespace,
    path: Path,
    recorded_ts: str = "",
) -> None:
    """Write tests/step0-baseline-v7.13.md mirroring routing-battery-baseline-v4.3.md.

    Header block: recorded timestamp, versions, run flags, run cwd, verdict, summary.
    Per-prompt table: ID | Expected MODE | K/N | Verdict (falsifiable <n>/N PASS|FAIL).
    Methodology notes, scores.tsv block, lineage section.

    D-03 compliance: rows that did not reach min_pass are written with their TRUE
    K/N (e.g. 2/5 FAIL) and a residual-risk note — never a forced PASS.
    """
    repeat = args.repeat
    min_pass = args.min_pass

    def _git_sha7(rel_path: str) -> str:
        try:
            r = subprocess.run(
                ["git", "log", "-1", "--format=%h", "--", rel_path],
                capture_output=True, text=True, cwd=REPO_ROOT,
            )
            return r.stdout.strip() or "unknown"
        except Exception:
            return "unknown"

    script_sha = _git_sha7("scripts/check-step0-live.py")
    core_sha = _git_sha7("scripts/_battery_core.py")
    fixture_sha = _git_sha7("tests/step0-fixture-catalog.md")
    agent_sha = _git_sha7("first-principles/agents/first-principles.md")

    p_rows = [r for r in results if r.prompt.id.startswith("S-P")]
    n_rows = [r for r in results if r.prompt.id.startswith("S-N")]
    # Shared v5.1 split gate — the 6 falsifier rows (CONTEXT_FREE_IDS) are
    # excluded from the bar. With the D-01a extension, p_context == the 8
    # canonical rows.
    p_context, p_context_pass, n_pass, battery_pass = _battery_gate(p_rows, n_rows)
    battery_verdict = "PASS" if battery_pass else "FAIL"

    # D-01b — the 8-canonical-row per-technique tally surfaced at the human
    # checkpoint for the falsifiable criterion (REBASE-02/03).
    # Driven explicitly from CANONICAL_TALLY_IDS so the Summary always reads /8
    # even if the falsifier-exclusion set ever drifts from the canonical set.
    # All 8 techniques have a v7.8 prior K/N; no "newly-measured" subset exists
    # in this v7.13 re-measure.
    canonical_rows = [r for r in results if r.prompt.id in CANONICAL_TALLY_IDS]
    canonical_pass = sum(1 for r in canonical_rows if r.row_pass)
    canonical_n = len(CANONICAL_TALLY_IDS)
    # S-P16 merge-validation: tracked outside the /8 canonical bar (D-01a).
    _s_p16_result = next((r for r in results if r.prompt.id == "S-P16"), None)

    if not recorded_ts:
        recorded_ts = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    lines: list[str] = [
        f"# Step 0 Live Harness Baseline — {_BASELINE_VERSION}",
        "",
        f"**Recorded:** {recorded_ts} ({repeat * len(results)} live `claude` invocations: {len(results)} prompts × {repeat} repeats)",
        f"**Script version:** `scripts/check-step0-live.py` (commit `{script_sha}`)",
        f"**Core version:** `scripts/_battery_core.py` (commit `{core_sha}`)",
        f"**Fixture version:** `tests/step0-fixture-catalog.md` (commit `{fixture_sha}`)",
        f"**Agent version:** `first-principles/agents/first-principles.md` (commit `{agent_sha}`)",
        f"**Run flags:** `--repeat {repeat} --min-pass {min_pass}`",
        "**Run cwd:** `/tmp` (out-of-repo — see Methodology notes)",
        f"**Baseline verdict:** BATTERY: {battery_verdict}",
        f"**Summary:** P {canonical_pass}/{canonical_n} (8-technique canonical bar: "
        f"S-P01–06 + S-P10 estimate, S-P14 theoretical-limit) | "
        f"S-N {n_pass}/{len(n_rows)} | "
        f"S-P07/08/11/12/13/15 expected-FAIL (context-free / alternation falsifiers, excluded from the bar) | "
        f"S-P16 merge-validation (outside /8): "
        f"{(_s_p16_result.match_count if _s_p16_result else 'N/A')}/"
        f"{(args.repeat if _s_p16_result else 'N/A')} "
        f"({'PASS' if _s_p16_result and _s_p16_result.row_pass else ('FAIL' if _s_p16_result else 'not measured this run')})",
        "",
        "---",
        "",
        "## Per-prompt results",
        "",
        "| ID | Expected MODE | K/N | Verdict |",
        "|----|---------------|-----|---------|",
    ]

    residual_risk_rows: list[PromptResult] = []
    for r in results:
        kn_str = f"{r.match_count}/{repeat} {'PASS' if r.row_pass else 'FAIL'}"
        if r.prompt.id in CONTEXT_FREE_IDS:
            verdict_str = (
                f"FAIL (expected — context-free parser-robustness fixture, "
                f"not part of the {p_context_pass}/{len(p_context)} live-technique bar)"
            )
        elif r.prompt.id in MERGE_VALIDATION_IDS:
            # S-P16 merge-validation: reported via the dedicated _s_p16_result
            # Summary line (see header block above). Never appended to
            # residual_risk_rows and never written as expected-FAIL (CR-01/D-01a).
            verdict_str = (
                "PASS" if r.row_pass else
                "FAIL (merge-validation signal — outside /8 canonical bar; "
                "tracked via _s_p16_result line, not a residual-risk row)"
            )
        else:
            verdict_str = "PASS" if r.row_pass else "FAIL"
            if not r.row_pass:
                residual_risk_rows.append(r)
        lines.append(f"| {r.prompt.id} | {r.prompt.expected} | {kn_str} | {verdict_str} |")

    lines += [
        "",
        "### Verdict-cell schema",
        "",
        "Each row's K/N cell uses the falsifiable `<n>/N PASS|FAIL` format (matching the",
        "`routing-battery-baseline-v4.3.md` convention). A row showing `<n>/5 FAIL`",
        "does NOT satisfy the gate. `PASS` means `match_count >= min_pass`.",
        "`FAIL` means `match_count < min_pass`.",
        "",
        "---",
        "",
        "## How this baseline was produced",
        "",
        "```bash",
        "REPO=/path/to/first-principles-skills",
        f"OUT_DIR=/tmp/step0-live-{_BASELINE_VERSION}-$(date -u +%Y%m%dT%H%M%SZ)",
        "cd /tmp && python3 \"$REPO/scripts/check-step0-live.py\" \\",
        "  --catalog \"$REPO/tests/step0-fixture-catalog.md\" \\",
        "  --plugin-dir \"$REPO/first-principles\" \\",
        f"  --repeat {repeat} --min-pass {min_pass} \\",
        "  --out \"$OUT_DIR\" \\",
        f"  --baseline \"$REPO/tests/step0-baseline-{_BASELINE_VERSION}.md\"",
        "```",
        "",
        f"**Run date:** {recorded_ts}",
        "",
        "---",
        "",
        "## Methodology notes",
        "",
        "**Why run from `/tmp`.** Same rationale as the routing battery: when run from the",
        "project root, the orchestrator's sub-agent may discover `.planning/` and plugin context,",
        "enriching its response with project-specific artifacts. Running from `/tmp` ensures",
        "the full-composer mode responds to the verbatim prompt only, matching the routing",
        "battery baseline methodology (v4.3 Methodology notes).",
        "",
        "**Why `--plugin-dir` must be an absolute path.** The script is invoked from `/tmp`;",
        "a relative path would resolve against `/tmp`. Always pass an absolute path.",
        "",
        "**Why `_classify_mode` infers `full-composer` from `none` + dispatch evidence.**",
        "When `detect_output_structure_from_file` returns `none` but the capture shows",
        "`Agent(subagent_type=\"first-principles:first-principles\")` was dispatched, the",
        "sub-agent ran the full-composer path but produced a non-structured response",
        "(e.g., a clarification request when `AskUserQuestion` is unavailable). The",
        "dispatch itself proves Step 0 chose the full-composer path. This inference is",
        "applied only in the Step 0 harness; `_battery_core.py` is not modified (D-02).",
    ]

    if residual_risk_rows:
        lines += [
            "",
            "**Residual risk notes (D-03).** The following rows did not reach `min_pass`.",
            "Their true observed K/N is recorded below; a forced PASS is never written.",
            "",
        ]
        for r in residual_risk_rows:
            rr_id = _RR_ID_MAP.get(r.prompt.id)
            if rr_id is None:
                raise ValueError(
                    f"_write_baseline: failing row {r.prompt.id} has no RR ID in _RR_ID_MAP; "
                    f"allocate a tracked RR ID before recording this baseline (RR-75-NN is retired)."
                )
            lines.append(
                f"- `{r.prompt.id}`: {r.match_count}/{repeat} FAIL"
                f" — expected `{r.prompt.expected}`;"
                f" observed modes: {r.modes}."
                f" Residual-risk tracked as {rr_id}."
            )

    lines += [
        "",
        "---",
        "",
        "## Scores (scores.tsv)",
        "",
        "```",
        "id\trun\texpected\tactual\tmatch",
    ]
    for r in results:
        for run_idx, mode in enumerate(r.modes, 1):
            match = 1 if mode == r.prompt.expected else 0
            lines.append(f"{r.prompt.id}\t{run_idx}\t{r.prompt.expected}\t{mode}\t{match}")
    lines += [
        "```",
        "",
        "---",
        "",
        "## Lineage",
        "",
        "This baseline records the Phase 135-137 v7.13 **re-measure of RR-130-01 fix + Step 0 deferred residuals** of Step 0",
        "technique selection. This is a **measurement-only** re-measure: there is NO detector change",
        "and NO agent-body change this milestone. The agent body is measured **as-shipped (v7.12)**",
        "and the detector `scripts/_battery_core.py` is **frozen** (`_TECHNIQUE_CATEGORIES` unchanged —",
        "inversion 13 markers, trade-off 10 markers (post-Phase-121 OCH-02) — `MIN_HEADER_HITS=2`,",
        "`_COMPOSER_FOCUS_CEILING=4` byte-unchanged). This run uses the 8 canonical rows:",
        "S-P01 pre-mortem, S-P02 inversion, S-P03 fishbone, S-P04 five-whys, S-P05",
        "trade-off, S-P06 second-order, S-P10 estimate, S-P14 theoretical-limit. All 8",
        "techniques have a v7.8 prior K/N. S-P16 (the absorbed reduce-to-primitives prompt",
        "routing to focused-five-whys) is measured as a dedicated merge-validation signal",
        "outside the /8 canonical bar (D-01a). Honesty-not-score (D-01) governs the committed",
        "verdict; the falsifiable criterion is applied at a blocking human checkpoint, not forced.",
        "This run is uncapped (no spend-limit constraint); all 29 S-P/S-N fixture rows are measured",
        "(S-A semantic-ambiguity rows excluded from live run).",
        "",
        "Three carried residuals from v7.8 may be resolved-or-carried in this run: RR-114-01",
        "(S-P02 inversion, v7.6 live 1/5; RESOLVED-STRUCTURALLY-OFFLINE Phase 121 OCH-02;",
        "live pass-rate re-measure this run), RR-108-04 (S-P10 estimate, v7.6",
        "spend-limit-indeterminate), RR-108-05 (S-P14 theoretical-limit, v7.6",
        "spend-limit-indeterminate). Each is CLOSED at its observed K/N if it reaches",
        "min-pass (≥3/5), or CARRIED FORWARD under a freshly-minted superseding Phase-129",
        "RR ID otherwise (that mint is conditional and post-run — it is NOT pre-baked in",
        "the offline firewall commit).",
        "",
        "Prior baseline: tests/step0-baseline-v7.11.md (Phase 128-129 whole-system re-measure) — BATTERY: PASS,",
        "29 S-P/S-N rows measured (S-A excluded); residuals",
        "RR-114-01 (S-P02 inversion, CARRIED — structural offline resolution Phase 121),",
        "RR-108-04 (S-P10 estimate, CARRIED-indeterminate), RR-108-05 (S-P14 theoretical-limit,",
        "CARRIED-indeterminate) carried forward into this v7.13 run.",
    ]

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Baseline written: {path}")


# ---------------------------------------------------------------------------
# argparse
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Live Step 0 K-of-N classification harness (STEP0-06)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument(
        "--catalog",
        type=Path,
        required=False,
        help="Path to step0-fixture-catalog.md (required unless --self-test)",
    )
    p.add_argument(
        "--plugin-dir",
        dest="plugin_dir",
        type=Path,
        default=DEFAULT_PLUGIN_DIR,
        help=f"Path to first-principles plugin dir (default: {DEFAULT_PLUGIN_DIR})",
    )
    p.add_argument(
        "--out-dir",
        "--out",
        dest="out_dir",
        type=Path,
        default=None,
        help="Output directory for .jsonl captures (default: /tmp/check-step0-live-<UTC-timestamp>/)",
    )
    p.add_argument(
        "--repeat",
        type=int,
        default=5,
        help="Number of runs per fixture (default: 5)",
    )
    p.add_argument(
        "--min-pass",
        dest="min_pass",
        type=int,
        default=3,
        help="Minimum passing runs to score a row PASS (default: 3)",
    )
    p.add_argument(
        "--baseline",
        type=Path,
        default=None,
        help="If supplied, write the v7.13 baseline .md to this path after the run",
    )
    p.add_argument(
        "--priority",
        "--only",
        dest="priority",
        nargs="*",
        default=None,
        help=(
            "Run a named subset of row IDs first, then the full catalog. "
            "With no value, uses the default merge-validation subset "
            f"({' + '.join(DEFAULT_PRIORITY_IDS)}). "
            "Pass explicit IDs to override the default subset. "
            "Example: --priority S-P04 S-P16 S-P02"
        ),
    )
    p.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress per-row progress output",
    )
    p.add_argument(
        "--dry-run",
        dest="dry_run",
        action="store_true",
        help="Parse catalog and print planned run without invoking claude",
    )
    p.add_argument(
        "--self-test",
        dest="self_test",
        action="store_true",
        help="Run offline deterministic self-test and exit (no claude invoked)",
    )
    return p


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    """Entry point. Returns exit code (0=pass, 1=fail, 2=usage/env error)."""
    parser = build_parser()
    args = parser.parse_args(argv)

    # (1) --self-test: MUST return before any env guard or claude invocation (D-06)
    if args.self_test:
        rc = self_test()
        sys.exit(rc)

    # (2) K>N validation (D-05) — exits 2 if repeat=2 and min_pass=3
    kn_rc = _validate_kn(args)
    if kn_rc is not None:
        sys.exit(kn_rc)

    # (3) Catalog is required for all non-self-test modes
    if not args.catalog:
        parser.error("--catalog is required (unless --self-test)")

    # --dry-run: parse and print without calling claude
    if args.dry_run:
        catalog = _read_step0_catalog(args.catalog)
        # WR-02: apply the same S-A exclusion filter as the live path BEFORE
        # _apply_priority, so the preview count matches the actual run size
        # (29 rows / 145 invocations at --repeat 5, not 35/175).
        catalog = [p for p in catalog if not p.id.startswith("S-A")]
        # WR-03: validate explicit --priority IDs against the filtered catalog
        if args.priority:
            catalog_ids = {p.id for p in catalog}
            unknown = [pid for pid in args.priority if pid not in catalog_ids]
            if unknown:
                print(
                    f"warning: --priority IDs not found in catalog: {unknown}",
                    file=sys.stderr,
                )
        catalog = _apply_priority(catalog, args.priority)
        print(
            f"Dry run: {len(catalog)} rows × {args.repeat} repeats"
            f" = {len(catalog) * args.repeat} invocations"
        )
        print(f"  min-pass: {args.min_pass} / {args.repeat}")
        print(f"  plugin-dir: {args.plugin_dir}")
        if args.priority is not None:
            priority_ids = args.priority or list(DEFAULT_PRIORITY_IDS)
            print(f"  priority subset: {priority_ids} (first)")
        for row in catalog:
            truncated = row.text[:60] + ("..." if len(row.text) > 60 else "")
            print(f"  {row.id}: {row.expected!r}  {truncated!r}")
        return 0

    # (4) sync-content.py --check pre-flight (71/D-09 constraint #3, Pitfall 4, T-72-05)
    sync_check = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "sync-content.py"), "--check"],
        capture_output=True,
    )
    if sync_check.returncode != 0:
        print(
            "error: sync-content.py --check failed — agent body may be stale.\n"
            "  Run: python3 scripts/sync-content.py --write",
            file=sys.stderr,
        )
        sys.exit(2)

    # (5) Environment guards
    _ensure_claude_available()
    if not args.plugin_dir.exists():
        print(
            f"error: plugin dir not found: {args.plugin_dir}\n"
            "  Run: python3 scripts/sync-content.py --write",
            file=sys.stderr,
        )
        sys.exit(2)

    # (6) Resolve out_dir
    if args.out_dir is None:
        ts = _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        args.out_dir = Path(f"/tmp/check-step0-live-{ts}")
    args.out_dir.mkdir(parents=True, exist_ok=True)

    # (7) Load catalog and run K-of-N loop (S-P01-first order preserved)
    parsed_catalog = _read_step0_catalog(args.catalog)
    # D-02 — filter the 6 S-A semantic-ambiguity rows out of the LIVE run. They
    # are offline-emulator-only by Phase 107 design (deterministic intended-winner
    # disambiguation gated by STEP0-08/SEMGATE); the live agent's focused-output is
    # not what they assert, so a live run adds non-deterministic noise + cost with
    # no new signal. The catalog file keeps them (offline fixtures); only the live
    # invocation loop excludes them — the live run iterates exactly the 29 S-P/S-N
    # rows (145 invocations at --repeat 5).
    catalog = [p for p in parsed_catalog if not p.id.startswith("S-A")]
    # WR-03: validate explicit --priority IDs against the live catalog so a
    # typo'd ID (e.g. --priority S-P4 instead of S-P04) warns to stderr rather
    # than silently reordering nothing and defeating the budget-guard guarantee.
    if args.priority:
        catalog_ids = {p.id for p in catalog}
        unknown = [pid for pid in args.priority if pid not in catalog_ids]
        if unknown:
            print(
                f"warning: --priority IDs not found in catalog: {unknown}",
                file=sys.stderr,
            )
    catalog = _apply_priority(catalog, args.priority)
    repeat = args.repeat
    min_pass = args.min_pass
    plugin_dir = args.plugin_dir
    out_dir = args.out_dir

    print(f"Step 0 live harness — {len(catalog)} rows × {repeat} repeats "
          f"(S-A* excluded from live run; {len(parsed_catalog)} parsed)")
    print(f"  min-pass: {min_pass}/{repeat}")
    print(f"  plugin-dir: {plugin_dir}")
    print(f"  out-dir: {out_dir}")
    print()

    results: list[PromptResult] = []
    for prompt in catalog:
        # Wrap verbatim text at call site (RESEARCH §2 CRITICAL note)
        wrapped = WrappedPrompt(id=prompt.id, text=_wrap_for_bypass(prompt.text))
        paths = _run_prompt_n_times_to_paths(wrapped, plugin_dir, out_dir, repeat)
        modes = [_classify_mode(p) for p in paths]
        match_count = sum(1 for m in modes if m == prompt.expected)
        row_pass = match_count >= min_pass
        results.append(PromptResult(
            prompt=prompt,
            modes=modes,
            match_count=match_count,
            row_pass=row_pass,
        ))
        if not args.quiet:
            print(
                f"[{prompt.id}] {match_count}/{repeat} "
                f"{'PASS' if row_pass else 'FAIL'} "
                f"(expected {prompt.expected!r})"
            )
        # Warn if bypass gate (S-P01) fails — other results may not be trustworthy
        if prompt.id == "S-P01" and not row_pass:
            print(
                f"WARNING: S-P01 (bypass gate) reached only {match_count}/{repeat} — "
                f"approach-② may not be working. Inspect captures in {out_dir}.",
                file=sys.stderr,
            )

    # (8) Write baseline if requested
    if args.baseline:
        _write_baseline(results, args, args.baseline)

    # (9) Write scores.tsv
    scores_path = out_dir / "scores.tsv"
    with scores_path.open("w", encoding="utf-8") as sf:
        sf.write("id\trun\texpected\tactual\tmatch\n")
        for r in results:
            for run_idx, mode in enumerate(r.modes, 1):
                match = 1 if mode == r.prompt.expected else 0
                sf.write(f"{r.prompt.id}\t{run_idx}\t{r.prompt.expected}\t{mode}\t{match}\n")

    # (10) Battery verdict
    p_rows = [r for r in results if r.prompt.id.startswith("S-P")]
    n_rows = [r for r in results if r.prompt.id.startswith("S-N")]
    # Same v5.1 split gate as the baseline emitter (S-P07/08 excluded) so the
    # process exit code and the written baseline verdict can never disagree (CR-01).
    p_context, p_context_pass, n_pass, battery_pass = _battery_gate(p_rows, n_rows)

    print()
    print("=" * 60)
    print(f"BATTERY: {'PASS' if battery_pass else 'FAIL'}")
    print(
        f"  P: {p_context_pass}/{len(p_context)} rows passed "
        f"({len(CANONICAL_TALLY_IDS)}-technique canonical bar; "
        f"{len(CONTEXT_FREE_IDS)} CONTEXT_FREE_IDS excluded; "
        f"MERGE_VALIDATION_IDS excluded)"
    )
    n_blocking_count = len(n_rows) - sum(
        1 for r in n_rows if r.prompt.id in NON_BLOCKING_NEGATIVE_IDS
    )
    n_non_blocking = [r for r in n_rows if r.prompt.id in NON_BLOCKING_NEGATIVE_IDS]
    n_non_blocking_str = ", ".join(r.prompt.id for r in n_non_blocking) or "none"
    print(
        f"  N: {n_pass}/{n_blocking_count} blocking-negative rows passed; "
        f"{len(NON_BLOCKING_NEGATIVE_IDS)} NON_BLOCKING_NEGATIVE_IDS excluded "
        f"({n_non_blocking_str}, live non-blocking)"
    )
    print(f"  scores.tsv: {scores_path}")

    return 0 if battery_pass else 1


if __name__ == "__main__":
    sys.exit(main())
