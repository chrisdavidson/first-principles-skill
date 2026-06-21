#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Live Step 0 harness — K-of-N classification and baseline recorder (STEP0-06).

Runs the full 12-row Step 0 fixture catalog (`tests/step0-fixture-catalog.md`)
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
        --baseline "$REPO/tests/step0-baseline-v7.6.md"

Usage:
    python3 scripts/check-step0-live.py [OPTIONS]

Options:
    --catalog PATH      Path to step0-fixture-catalog.md (required)
    --plugin-dir PATH   Path to first-principles plugin dir (default: repo-relative)
    --out-dir PATH      Output directory for .jsonl captures (default: /tmp/check-step0-live-<ts>)
    --repeat INT        Number of runs per fixture (default: 5)
    --min-pass INT      Minimum passing runs to score a row PASS (default: 3)
    --baseline PATH     If supplied, write the v7.6 baseline .md to this path
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
_BASELINE_VERSION: str = "v7.6"

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

    if all_passed:
        print("self-test PASS (4 fixtures + K>N rejection + catalog parse)")
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

# The 8 canonical positive rows — one per technique (D-01) — over which the
# v7.6 8-technique pass-rate is computed. The instrument emits this per-technique
# tally (D-01b, REBASE-02), it is not hand-assembled. All 8 techniques have a
# v7.4 prior K/N; there is no "newly-measured" subset in this re-baseline.
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
    exit code so the two can never drift (CR-01). Context-free fixtures
    (S-P07/08) are excluded from the S-P bar: the gate is
    (all S-P01–06 pass) AND (all S-N pass). Returns
    (p_context, p_context_pass, n_pass, battery_pass)."""
    p_context = [r for r in p_rows if r.prompt.id not in CONTEXT_FREE_IDS]
    p_context_pass = sum(1 for r in p_context if r.row_pass)
    n_pass = sum(1 for r in n_rows if r.row_pass)
    battery_pass = (p_context_pass == len(p_context)) and (n_pass == len(n_rows))
    return p_context, p_context_pass, n_pass, battery_pass


def _write_baseline(
    results: list[PromptResult],
    args: argparse.Namespace,
    path: Path,
    recorded_ts: str = "",
) -> None:
    """Write tests/step0-baseline-v7.6.md mirroring routing-battery-baseline-v4.3.md.

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
    # All 8 techniques have a v7.4 prior K/N; no "newly-measured" subset exists
    # in this v7.6 re-baseline.
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

    # D-03/D-03a — RR_ID_MAP RESOLVED at the Phase-108 finalize (Commit 2,
    # plan 108-02). The 108-01 provisional placeholders are replaced with the
    # real RR-108-NN IDs per the human-approved close-vs-carry verdict surfaced
    # at the Task 1 blocking checkpoint:
    #   - S-P02 inversion live 1/5 < min-pass → CARRY FORWARD as RR-108-01
    #     (supersedes RR-95-01; chain RR-79-02 → RR-92-01 → RR-95-01 → RR-108-01).
    #   - S-P05 trade-off live 2/5 < min-pass → CARRY FORWARD as RR-108-02
    #     (supersedes RR-95-02; chain RR-79-03 → RR-92-02 → RR-95-02 → RR-108-02).
    #   - The ninth technique (v7.4): removed in v7.5 (absorbed into five-whys,
    #     RR-108-03 resolved-by-merge). Not present in the v7.6 8-technique run.
    #   - S-P10 estimate  live 0/5 → RR-108-04 (v7.4 carry-forward).
    #   - S-P14 theoretical-limit live 0/5 → RR-108-05 (v7.4 carry-forward).
    # No RR-95-NN was CLOSED (both S-P02 and S-P05 stayed below the ≥3/5 bar).
    # No provisional placeholder survives. The falsifier rows still need a tracked
    # ID for the invariant safety net (they are handled by the CONTEXT_FREE branch
    # and never reach residual_risk_rows, but a non-None entry is required); they
    # share the closest minted canonical-technique ID for their falsified technique.
    RR_ID_MAP = {
        "S-P01": "RR-79-01", "S-P02": "RR-108-01", "S-P03": "RR-75-03",
        "S-P04": "RR-75-04", "S-P05": "RR-108-02", "S-P06": "RR-75-06",
        "S-N04": "RR-80-01",
        # Negative-control rows that dipped below min_pass on this run ONLY because
        # of spend-limit `none` truncation (no routing happened), NOT genuine
        # over-routing. They reach residual_risk_rows when failing, so they need a
        # tracked ID for the safety-net invariant. Mapped to a single infra ID
        # (RR-108-06) — they are NOT a routing residual.
        "S-N06": "RR-108-06",  # spend-limit truncation (infra), not a routing residual
        "S-N07": "RR-108-06",  # spend-limit truncation (infra), not a routing residual
        # Canonical techniques with v7.4 carry-forward residuals. These CAN
        # reach the residual-risk branch if below min-pass in this v7.6 run.
        "S-P10": "RR-108-04",  # estimate          (v7.4 carry-forward)
        "S-P14": "RR-108-05",  # theoretical-limit (v7.4 carry-forward)
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
    if residual_risk_rows:
        lines += [
            "",
            "**Residual risk notes (D-03).** The following rows did not reach `min_pass`.",
            "Their true observed K/N is recorded below; a forced PASS is never written.",
            "",
        ]
        for r in residual_risk_rows:
            rr_id = RR_ID_MAP.get(r.prompt.id)
            if rr_id is None:
                raise ValueError(
                    f"_write_baseline: failing row {r.prompt.id} has no RR ID in RR_ID_MAP; "
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
        "This baseline records the Phase 113-114 v7.6 **8-technique live re-baseline** of Step 0",
        "technique selection. This is a **measurement-only** re-baseline following the v7.5",
        "five-whys consolidation merge: there is NO detector change and NO agent-body change this",
        "milestone. The agent body is measured **as-shipped (v7.5)** and the detector",
        "`scripts/_battery_core.py` is **frozen** (`_TECHNIQUE_CATEGORIES` unchanged —",
        "inversion 9 markers, trade-off 6 markers — `MIN_HEADER_HITS=2`,",
        "`_COMPOSER_FOCUS_CEILING=4` byte-unchanged). This run uses the 8 canonical rows:",
        "S-P01 pre-mortem, S-P02 inversion, S-P03 fishbone, S-P04 five-whys, S-P05",
        "trade-off, S-P06 second-order, S-P10 estimate, S-P14 theoretical-limit. All 8",
        "techniques have a v7.4 prior K/N. S-P16 (the absorbed reduce-to-primitives prompt",
        "routing to focused-five-whys) is measured as a dedicated merge-validation signal",
        "outside the /8 canonical bar (D-01a). Honesty-not-score (D-01) governs the committed",
        "verdict; the falsifiable criterion is applied at a blocking human checkpoint, not forced.",
        "",
        "Four carried residuals from v7.4 may be resolved-or-carried in this run: RR-108-01",
        "(S-P02 inversion, v7.4 live 1/5), RR-108-02 (S-P05 trade-off, v7.4 live 2/5),",
        "RR-108-04 (S-P10 estimate, v7.4 live 0/5), RR-108-05 (S-P14 theoretical-limit,",
        "v7.4 spend-limit-indeterminate). Each is CLOSED at its observed K/N if it reaches",
        "min-pass (≥3/5), or CARRIED FORWARD under a freshly-minted superseding Phase-114",
        "RR ID otherwise (that mint is conditional and post-run — it is NOT pre-baked in",
        "the offline firewall commit).",
        "",
        "Prior baseline: tests/step0-baseline-v7.4.md (Phase 108) — BATTERY: FAIL,",
        "P 4/9 (S-P01-06 + three expanded techniques), S-N 4/4; residuals RR-108-01 (S-P02 inversion, CARRIED 1/5),",
        "RR-108-02 (S-P05 trade-off, CARRIED 2/5), RR-108-04 (S-P10 estimate, CARRIED 0/5),",
        "RR-108-05 (S-P14 theoretical-limit, spend-limit-indeterminate) carried forward.",
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
        help="If supplied, write the v7.6 baseline .md to this path after the run",
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
    # invocation loop excludes them — the live run iterates exactly the 22 S-P/S-N
    # rows (~110 invocations at --repeat 5).
    catalog = [p for p in parsed_catalog if not p.id.startswith("S-A")]
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
    print(f"  P: {p_context_pass}/{len(p_context)} rows passed (S-P01–06; S-P07/08 context-free, excluded)")
    print(f"  N: {n_pass}/{len(n_rows)} rows passed")
    print(f"  scores.tsv: {scores_path}")

    return 0 if battery_pass else 1


if __name__ == "__main__":
    sys.exit(main())
