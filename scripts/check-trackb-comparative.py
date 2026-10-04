#!/usr/bin/env python3
"""Track B comparative harness -- agent vs. unaided control, pre-registered.

Implements `docs/trackb-preregistration.md` exactly. That document is LOCKED and
this script is its executable form: the arms, the sample, the analysis plan and
the decision threshold are read from constants pinned here and cross-checked
against the pre-registration's own text at `--self-test` time, so the code and the
registered protocol cannot silently diverge.

What makes this different from every prior arm/arm run in this repo
-------------------------------------------------------------------
Every previous "A/B" here contrasted two versions of the SAME agent body. This is
the project's first comparison against NOT USING THE AGENT. Arm C is the same
model, the same prompt, no plugin.

The one-sided-drift hazard, and the answer to it
------------------------------------------------
`docs/v8.7-quality-baseline-freeze.md` measured this instrument family drifting
+7/108 upward on BYTE-IDENTICAL documents re-scored a day apart -- five of six
documents up, none down. A favourable-looking result is therefore what noise
produces here. Two consequences, both structural rather than advisory:

 1. The decision threshold is SELF-CALIBRATING: the effect must exceed twice the
    drift measured inside this same run (`--drift-control`), not a number guessed
    beforehand. A run with no drift arm cannot reach `cleared` at all.
 2. The threshold is evaluated by `evaluate()` from the recorded numbers, and the
    emitted status is whatever that function returns. There is no path in this
    file that lets a human set `status` by hand.

Why the rubric is not the Self-Audit Gate
------------------------------------------
Scoring against the agent's own output contract would score arm C `Absent` for not
being in the agent's format, producing a large and meaningless result. The neutral
rubric (`docs/trackb-neutral-rubric.md`) names no format, and
`_c01_rubric_is_format_neutral` FAILS this script if any format token appears in
it. That control is the integrity of the whole comparison.

Usage:
    python3 scripts/check-trackb-comparative.py --self-test
    python3 scripts/check-trackb-comparative.py --plan          # cost, no spend
    python3 scripts/check-trackb-comparative.py --rig-test      # 4 live calls
    python3 scripts/check-trackb-comparative.py --run --out DIR # the registered run
    python3 scripts/check-trackb-comparative.py --score DIR     # re-score captures

Exit codes:
    0  success (self-test passed / plan printed / run completed and recorded)
    1  a control failed, a precondition was violated, or the run was voided
"""

from __future__ import annotations

import argparse
import itertools
import json
import re
import statistics
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT: Path = Path(__file__).resolve().parents[1]
PREREG: Path = REPO_ROOT / "docs" / "trackb-preregistration.md"
RUBRIC: Path = REPO_ROOT / "docs" / "trackb-neutral-rubric.md"
CATALOG: Path = REPO_ROOT / "tests" / "trackb-catalog-v9.13.md"
RESULT_PATH: Path = REPO_ROOT / "docs" / "data" / "trackb-result.json"
PLUGIN_DIR: Path = REPO_ROOT / "first-principles"

# --- Pinned protocol constants (must match the pre-registration) ------------
RUNS_PER_CELL = 1
JUDGES_PER_DOC = 2
DRIFT_ARM_SIZE = 20
ALPHA = 0.05
DRIFT_MULTIPLE = 2.0
MIN_DOMAINS_IN_DIRECTION = 3
MAX_UNPARSEABLE_FRACTION = 0.10

# --- trackb-2 protocol constants (docs/trackb-2-preregistration.md) --------
#
# trackb-2 supersedes trackb (v9.13): arm T is scored on the agent's OWN
# delivered document, captured via stream-json, with dispatch recorded per
# cell -- not on `claude -p` stdout, which under `--plugin-dir` is the main
# session's SUMMARY of that document (docs/trackb-transport-erratum.md).
PREREG_2: Path = REPO_ROOT / "docs" / "trackb-2-preregistration.md"
RUN_ID_2 = "trackb-run-v9.15"
# The documented user path: the launcher skill's own slash form, prefixed onto
# the byte-identical prompt text. A pre-run amendment (recorded in the
# pre-registration, before any registered cell) may replace this with the
# explicit-frame fallback if a transport probe shows the slash form does not
# dispatch under `-p`.
ARM_T_INVOCATION = "/first-principles:first-principles-analysis "
ALLOWED_TOOLS: tuple[str, ...] = ("Read", "Glob", "Grep", "WebFetch", "WebSearch", "Bash(*)")
JUDGE_ALLOWED_TOOLS: tuple[str, ...] = ("Read", "Glob", "Grep")
# Confirmed live 2026-09-29 (read-only) against ~/.claude/settings.json's own
# schema: `enabledPlugins` maps a marketplace-qualified plugin id to a bool.
# Disabling both here keeps arm C free of the user-scope install and keeps
# every call (including arm T and the judges) on a symmetric transport.
ISOLATION_SETTINGS = json.dumps(
    {
        "enabledPlugins": {
            "first-principles@first-principles-skill": False,
            "bm@buildomator": False,
        }
    }
)
# Pre-declared fallback (Task 2 probe) if --settings does not isolate arm C.
ISOLATION_SETTING_SOURCES_FALLBACK = "project,local"
MAX_ATTEMPTS = 3
MAX_VOID_FRACTION = 0.10
BLINDING_SEED_2 = 20260929
# 10 prompts x JUDGES_PER_DOC judgings of arm T's orchestrator final message
# (secondary, non-gating -- quantifies what a user sees without opening the
# delivered file).
SECONDARY_JUDGINGS = 20
FORMAT_TELL_CAVEAT = (
    "The scored arm-T document is identifiable by its format with near certainty, "
    "so this result cannot separate reasoning quality from a format or halo effect."
)


def total_live_2() -> int:
    """20 generations + 40 primary judgings + 20 drift + 20 secondary judgings.

    Derived from the pinned constants -- never typed -- so C20 fails if a
    constant changes without the pre-registration's own literal changing with
    it (docs/trackb-2-preregistration.md 'Total live invocations').
    """
    prompts = parse_catalog(CATALOG.read_text(encoding="utf-8"))
    generations = len(prompts) * 2 * RUNS_PER_CELL
    primary_judgings = generations * JUDGES_PER_DOC
    return generations + primary_judgings + DRIFT_ARM_SIZE + SECONDARY_JUDGINGS


_BAND_WEIGHTS = {"Rigorous": 3, "Sound": 2, "Hand-wavy": 1, "Absent": 0}
_CRITERIA = ("C1", "C2", "C3", "C4", "C5")
_MAX_DOC_SCORE = len(_CRITERIA) * 3

_SCORELINE_START = "=== TRACKB-SCORELINE-START ==="
_SCORELINE_END = "=== TRACKB-SCORELINE-END ==="

# Format tokens that must NOT appear in the neutral rubric. Their presence would
# mean the rubric rewards the agent's output shape, which rigs the comparison.
_FORMAT_TOKENS = (
    "derivation chain",
    "verdict cell",
    "assumption table",
    "ground truth",
    "self-audit",
    "six sections",
    "output section",
    "numbered section",
    "chain block",
    "gt-",
)

# Substrings that would leak to a judge that a comparison exists.
_FORBIDDEN_JUDGE_SUBSTRINGS = (
    "compare", "comparison", "arm a", "arm b", "treatment", "control",
    "baseline", "plugin", "agent", "unaided", "versus", " vs ",
    "first-principles", "better", "worse", "improvement", "experiment",
)


class TrackBError(RuntimeError):
    """A protocol precondition was violated. The run is void."""


class TrackBPause(TrackBError):
    """A usage-limit stub was hit; the caller must stop without further calls
    and resume later against the same --out/--scratch (exit 3)."""


class TrackBAbort(TrackBError):
    """An isolation breach or a body-sha drift was detected mid-run; the
    caller must stop without further calls (exit 5)."""


# ---------------------------------------------------------------------------
# Judge transport (mirrors check-quality-harness.py's locked argv shape)
# ---------------------------------------------------------------------------

JUDGE_PROMPT = (
    "You are scoring exactly one analysis document, `analysis.md`, found in your "
    "current working directory, against the rubric in `rubric.md`, also in your "
    "current working directory. Read both files in full, then score the document "
    "on each of the rubric's five criteria exactly as it instructs, writing one "
    "short paragraph per criterion before your final block.\n\n"
    "Score this document entirely on its own terms, as the only document you have "
    "ever been given to evaluate. Close your response with exactly the fixed block "
    "the rubric specifies and nothing after it."
)


def judge_prompt_leaks() -> list[str]:
    lowered = JUDGE_PROMPT.lower()
    return [s for s in _FORBIDDEN_JUDGE_SUBSTRINGS if s in lowered]


# ---------------------------------------------------------------------------
# Data shapes
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Prompt:
    prompt_id: str
    domain: str
    text: str


@dataclass
class DocScore:
    """One judge's reading of one document."""

    doc_id: str
    prompt_id: str
    arm: str           # "T" or "C"
    judge: int
    bands: dict        # criterion -> band
    total: int


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------


def parse_catalog(text: str) -> tuple[Prompt, ...]:
    """Read the frozen catalog's pipe table into Prompt records."""
    prompts: list[Prompt] = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("| TB-"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 3:
            continue
        prompts.append(Prompt(prompt_id=cells[0], domain=cells[1], text=cells[2]))
    return tuple(prompts)


def parse_scoreline(text: str) -> dict | None:
    """Extract the fixed scoreline block. Returns None if absent/malformed.

    Returning None rather than raising is deliberate: an unparseable judgement is
    a COUNTED outcome under the pre-registration (§5), not an exception that
    silently drops the row from a denominator.
    """
    if _SCORELINE_START not in text or _SCORELINE_END not in text:
        return None
    block = text.split(_SCORELINE_START, 1)[1].split(_SCORELINE_END, 1)[0]
    bands: dict[str, str] = {}
    for crit in _CRITERIA:
        m = re.search(rf"^\s*{crit}:\s*(\w[\w-]*)\s*$", block, re.MULTILINE)
        if not m:
            return None
        band = m.group(1)
        if band not in _BAND_WEIGHTS:
            return None
        bands[crit] = band
    return bands


def score_total(bands: dict) -> int:
    return sum(_BAND_WEIGHTS[bands[c]] for c in _CRITERIA)


# ---------------------------------------------------------------------------
# Extraction integrity (pre-registration §7)
# ---------------------------------------------------------------------------

_RUBRIC_CONTAMINATION_MARKERS = (
    _SCORELINE_START,
    "Track B Neutral Rubric",
    "Format carries no marks",
)


# The agent's output contract. A plugin-arm capture that carries none of these is
# not the agent's document -- see AGENT_CONTRACT_MIN_SECTIONS below.
_AGENT_CONTRACT_SECTIONS = (
    "Problem Essence",
    "Assumptions Table",
    "Ground Truths",
    "Derivation Chains",
    "Abandoned Reasoning",
    "Conclusion",
)
AGENT_CONTRACT_MIN_SECTIONS = 4


def extraction_problems(
    doc_text: str, min_words: int = 120, *, plugin_arm: bool = False
) -> list[str]:
    """Void-the-cell checks applied BEFORE a document reaches a judge.

    This harness family has twice nearly fabricated a decisive result through
    extraction faults -- once by paraphrasing an analysis down to ~15% of itself,
    once by concatenating the rubric onto an arm's output. Both would have
    produced confident, false verdicts, in OPPOSITE directions.

    A THIRD fault of the same family was found on 2026-09-26 and is what
    `plugin_arm` closes (`docs/trackb-transport-erratum.md`). Under `--plugin-dir`,
    `claude -p` stdout is the main session's SUMMARY of the agent's document, not
    the document. All ten arm-T captures of the v9.13 run were summaries; every
    reading taken from them describes a summary. The two checks above could not
    see it: a summary carries no rubric text and runs 282-699 words, far above the
    floor. Length distinguishes a truncation, and this is a SUBSTITUTION of one
    well-formed document for another.

    `plugin_arm=True` therefore additionally requires the agent's own output
    contract. It is opt-in per arm and MUST stay that way: the control arm is
    unaided and will never carry the contract, so applying this to it would void
    every control cell and destroy the comparison it exists to protect.
    """
    problems: list[str] = []
    for marker in _RUBRIC_CONTAMINATION_MARKERS:
        if marker in doc_text:
            problems.append(f"rubric contamination: capture contains {marker!r}")
    words = len(doc_text.split())
    if words < min_words:
        problems.append(f"implausibly short capture: {words} words < {min_words}")
    if plugin_arm:
        lowered = doc_text.lower()
        found = [s for s in _AGENT_CONTRACT_SECTIONS if s.lower() in lowered]
        if len(found) < AGENT_CONTRACT_MIN_SECTIONS:
            problems.append(
                f"not the agent's document: {len(found)} of "
                f"{len(_AGENT_CONTRACT_SECTIONS)} contract sections present "
                f"(need >= {AGENT_CONTRACT_MIN_SECTIONS}) -- under --plugin-dir, "
                f"`claude -p` stdout is the orchestrator's summary; capture the "
                f"subagent message instead (docs/trackb-transport-erratum.md)"
            )
    return problems


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------


def paired_permutation_p(diffs: list[float]) -> float:
    """Exact two-tailed paired permutation (sign-flip) test.

    With n pairs there are 2**n sign assignments; for n <= 20 that is at most
    ~1e6 and is enumerated EXACTLY rather than sampled, so the p-value carries no
    seed and no sampling error. The pre-registration's mention of a sampled test
    with a seed is the fallback for larger n, which this catalog does not reach.
    """
    n = len(diffs)
    if n == 0:
        return 1.0
    if all(d == 0 for d in diffs):
        return 1.0
    observed = abs(statistics.fmean(diffs))
    if n > 20:  # pragma: no cover - catalog is 10
        raise TrackBError(f"exact test refuses n={n}; use the sampled fallback")
    at_least_as_extreme = 0
    total = 0
    for signs in itertools.product((1, -1), repeat=n):
        total += 1
        m = abs(statistics.fmean([s * d for s, d in zip(signs, diffs)]))
        if m >= observed - 1e-12:
            at_least_as_extreme += 1
    return at_least_as_extreme / total


def mean_absolute_drift(pairs: list[tuple[int, int]]) -> float:
    """Mean |rescore - original| over the drift-control arm."""
    if not pairs:
        return 0.0
    return statistics.fmean([abs(b - a) for a, b in pairs])


# ---------------------------------------------------------------------------
# The decision -- the only place status is determined
# ---------------------------------------------------------------------------


def evaluate(
    per_prompt: dict,
    drift_pairs: list[tuple[int, int]],
    unparseable_fraction: float,
    dispatch_failures: int,
    *,
    void_fraction: float = 0.0,
) -> dict:
    """Apply the pre-registered threshold. Returns the result record.

    `per_prompt` maps prompt_id -> {"domain": str, "T": float, "C": float}.

    There is deliberately no argument by which a caller can assert a status: it
    is computed here from the recorded numbers, and `cmd_run` writes whatever
    this returns. That is what makes "publish only if non-null" a protocol rather
    than a preference.

    `void_fraction` is trackb-2's addition (docs/trackb-2-preregistration.md):
    a mechanical-failure cell (no dispatch, no delivered file, a failing
    extraction check, a non-zero exit or a timeout, exhausted after
    MAX_ATTEMPTS) drops its prompt from the paired analysis. Exceeding
    MAX_VOID_FRACTION of the 20 cells is mechanics, not a disappointing
    result, so it routes to `inconclusive` exactly like a dispatch failure or
    an unparseable-scoreline rate above MAX_UNPARSEABLE_FRACTION -- never to
    `null`. The default of 0.0 keeps every pre-existing trackb (v9.13) call
    site and control unaffected.
    """
    prompt_ids = sorted(per_prompt)
    diffs = [per_prompt[p]["T"] - per_prompt[p]["C"] for p in prompt_ids]
    mean_diff = statistics.fmean(diffs) if diffs else 0.0

    # Mechanics first: a broken run is inconclusive, never null.
    if (
        dispatch_failures
        or unparseable_fraction > MAX_UNPARSEABLE_FRACTION
        or void_fraction > MAX_VOID_FRACTION
    ):
        reason_parts = [
            f"{dispatch_failures} dispatch failure(s)",
            f"{unparseable_fraction:.1%} unparseable (cap {MAX_UNPARSEABLE_FRACTION:.0%})",
        ]
        if void_fraction > MAX_VOID_FRACTION:
            reason_parts.append(
                f"{void_fraction:.1%} voided cells (cap {MAX_VOID_FRACTION:.0%})"
            )
        return {
            "status": "inconclusive",
            "reason": "run mechanics failed: " + ", ".join(reason_parts),
            "mean_difference": round(mean_diff, 4),
            "n_prompts": len(prompt_ids),
        }

    p_value = paired_permutation_p(diffs)
    drift = mean_absolute_drift(drift_pairs)
    drift_bar = DRIFT_MULTIPLE * drift

    by_domain: dict[str, list[float]] = {}
    for pid in prompt_ids:
        by_domain.setdefault(per_prompt[pid]["domain"], []).append(
            per_prompt[pid]["T"] - per_prompt[pid]["C"]
        )
    domains_in_direction = sum(
        1
        for d, vals in by_domain.items()
        if statistics.fmean(vals) > 0
    )

    cond_stat = p_value < ALPHA
    cond_drift = bool(drift_pairs) and mean_diff > drift_bar
    cond_domain = domains_in_direction >= MIN_DOMAINS_IN_DIRECTION

    cleared = cond_stat and cond_drift and cond_domain

    unmet = []
    if not cond_stat:
        unmet.append(f"p={p_value:.4f} not < {ALPHA}")
    if not drift_pairs:
        unmet.append("no drift-control arm recorded; threshold 2 unreachable")
    elif not cond_drift:
        unmet.append(
            f"effect {mean_diff:.3f} does not exceed {DRIFT_MULTIPLE}x in-run "
            f"drift ({drift_bar:.3f})"
        )
    if not cond_domain:
        unmet.append(
            f"only {domains_in_direction} of {len(by_domain)} domains in direction "
            f"(need {MIN_DOMAINS_IN_DIRECTION})"
        )

    return {
        "status": "cleared" if cleared else "null",
        "reason": "all three pre-registered conditions met" if cleared else "; ".join(unmet),
        "mean_difference": round(mean_diff, 4),
        "p_value": round(p_value, 6),
        "in_run_drift": round(drift, 4),
        "drift_threshold": round(drift_bar, 4),
        "domains_in_direction": domains_in_direction,
        "domain_count": len(by_domain),
        "n_prompts": len(prompt_ids),
        "conditions": {
            "statistical": cond_stat,
            "exceeds_drift": cond_drift,
            "domain_spread": cond_domain,
        },
        "per_prompt_differences": {p: round(d, 3) for p, d in zip(prompt_ids, diffs)},
    }


# ---------------------------------------------------------------------------
# Live transport
# ---------------------------------------------------------------------------


# The treatment arm MUST carry this. Measured 2026-09-25, before any registered
# run: with the plugin loaded, `claude -p` dispatches the agent as a BACKGROUND
# task and print mode terminates at a 600s ceiling, emitting
#
#   "Background tasks still running after 600s; terminating."
#
# followed by a ~54-word stub ("I've delegated this to the first-principles
# agent ... I'll share the full analysis once it completes") INSTEAD OF the
# analysis, at exit code 0. A run on that transport would have scored arm T
# near-zero on every criterion and produced a large, confident, and entirely
# false result in the direction of "the plugin makes analysis much worse."
#
# Setting the ceiling to 0 waits indefinitely. Re-measured on the same prompt:
# 598 words, 11m48s, a real analysis. `extraction_problems()` rejected the
# broken capture and accepted the repaired one, which is the fault class
# pre-registration section 7 exists for -- it fired on the very first live
# invocation, before any registered data existed.
_PRINT_BG_WAIT_ENV = {"CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS": "0"}


def run_prompt(prompt_text: str, out_path: Path, plugin: bool, model: str) -> Path:
    import os

    argv = ["claude", "-p", "--model", model]
    if plugin:
        argv += ["--plugin-dir", str(PLUGIN_DIR)]
    argv += [
        "--no-session-persistence",
        "--permission-mode", "bypassPermissions",
        prompt_text,
    ]
    env = {**os.environ, **_PRINT_BG_WAIT_ENV}
    proc = subprocess.run(
        argv, capture_output=True, text=True, timeout=5400, env=env, check=False
    )
    out_path.write_text(proc.stdout + proc.stderr, encoding="utf-8")
    return out_path


# ---------------------------------------------------------------------------
# trackb-2 stream-json helpers (stdlib-only; NOT imported from tests/ modules
# -- gate scripts stay independent of test-only helper modules)
# ---------------------------------------------------------------------------


def events(jsonl: str):
    """Yield each parsed JSON object from a stream-json capture, skipping any
    blank or malformed line rather than raising -- a truncated tail must not
    crash the harness mid-run."""
    for line in jsonl.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            yield json.loads(line)
        except json.JSONDecodeError:
            continue


def init_plugins(jsonl: str) -> list[dict]:
    """The init event's `plugins` array, or [] if no init event is present."""
    for obj in events(jsonl):
        if obj.get("type") == "system" and obj.get("subtype") == "init":
            return list(obj.get("plugins") or [])
    return []


def init_check(jsonl: str, arm: str) -> list[str]:
    """Isolation problems in the init event, for the named arm ('T' or 'C').

    Arm C must load no `first-principles` plugin at all. Arm T must load
    EXACTLY one, at PLUGIN_DIR -- the repository's working-tree copy, not the
    user-scope installed one (planner finding F4: `--plugin-dir` shadows the
    installed plugin, so the inline copy is what must be confirmed present).

    Path comparison is relative to repository root to work across different
    checkout locations (local vs. CI).
    """
    plugins = init_plugins(jsonl)
    fp = [p for p in plugins if p.get("name") == "first-principles"]
    if arm == "C":
        if fp:
            return [f"arm C init event lists a first-principles plugin: {fp!r}"]
        return []
    if arm == "T":
        if len(fp) != 1:
            return [
                (f"arm T init event lists {len(fp)} first-principles plugin(s), "
                f"expected exactly 1: {fp!r}")
            ]
        # Compare relative paths from repository root to work across checkout locations
        plugin_path_str = fp[0].get("path") or ""
        plugin_path = Path(plugin_path_str)
        try:
            plugin_relative = plugin_path.relative_to(REPO_ROOT)
        except ValueError:
            # If the path is not relative to REPO_ROOT, compare it as-is
            plugin_relative = plugin_path.name if plugin_path.name == PLUGIN_DIR.name else plugin_path

        try:
            expected_relative = PLUGIN_DIR.relative_to(REPO_ROOT)
        except ValueError:
            expected_relative = PLUGIN_DIR.name

        if plugin_relative != expected_relative:
            return [
                (f"arm T first-principles plugin path is {fp[0].get('path')!r}, "
                f"expected {str(PLUGIN_DIR)!r}")
            ]
        return []
    raise TrackBError(f"init_check: unknown arm {arm!r}")


def dispatched(jsonl: str) -> bool:
    """True iff the stream carries a tool_use dispatching the first-principles
    agent specifically (not any subagent)."""
    for obj in events(jsonl):
        if obj.get("type") != "assistant":
            continue
        for block in (obj.get("message") or {}).get("content") or []:
            if not isinstance(block, dict):
                continue
            if block.get("type") != "tool_use" or block.get("name") not in ("Agent", "Task"):
                continue
            if block.get("input", {}).get("subagent_type") == "first-principles:first-principles":
                return True
    return False


def final_message(jsonl: str) -> str:
    """The LAST `result` event's `result` field.

    A dispatched run emits an early stub `result` event (planner finding F5: a
    356-char "I've kicked off..." message) before the real final message. The
    FIRST result event is therefore the wrong one to treat as the answer.
    """
    last = ""
    for obj in events(jsonl):
        if obj.get("type") == "result":
            last = obj.get("result", "") or ""
    return last


def is_limit_stub(jsonl: str) -> bool:
    """Reimplemented from tests/w4-paired/run_paired.py (not imported): gate
    scripts stay stdlib-only and independent of test-only modules.

    Corrected 2026-09-30 (docs/trackb-2-preregistration.md's pre-run
    amendment): a stream carrying a genuine final `result` event with
    `is_error` false and a non-empty `result` text is a complete answer and
    is NEVER a stub, regardless of what words that answer happens to
    contain -- measured false positive: TB-01-C's attempt 1 (arm C, no
    plugin, so no `parent_tool_use_id` ever appears in its stream) was a
    complete, `is_error: false` answer discussing GraphQL rate limiting,
    and the regex fallback below misfired on that prose. `is_error` (and the
    equivalent `api_error_status == 429`) is checked FIRST and still catches
    every real spend-limit stub, including the frozen 429 specimen this
    module's own self-test reads. The regex fallback now runs only when
    there is NO final `result` event at all (a genuinely truncated or killed
    capture), or one with `is_error` false but an empty `result` text --
    the case the fallback actually exists for."""
    last_result: dict | None = None
    for obj in events(jsonl):
        if obj.get("type") == "result":
            last_result = obj
    if last_result is not None:
        if last_result.get("is_error") or last_result.get("api_error_status") == 429:
            return True
        if (last_result.get("result") or "").strip():
            return False
    return (
        bool(re.search(r"usage limit|rate limit", jsonl[-4000:], re.IGNORECASE))
        and '"parent_tool_use_id":"' not in jsonl
    )


def _assert_argv_safe(argv: list[str]) -> None:
    if "bypassPermissions" in argv:
        raise TrackBError("refusing to dispatch with bypassPermissions")
    if "Bash" in argv:
        raise TrackBError("refusing a bare Bash entry in the allowlist")
    allowed = [a for a in argv if isinstance(a, str) and a.startswith("--allowedTools=")]
    if len(allowed) != 1:
        raise TrackBError(f"argv must carry exactly one --allowedTools= token, got {allowed!r}")


def argv_t(prompt: str, model: str) -> list[str]:
    """Arm T: --plugin-dir <repo>/first-principles, the ARM_T_INVOCATION
    prefix, acceptEdits, and the isolation settings -- kept on for transport
    symmetry with arm C even though they are inert against an ephemeral
    --plugin-dir load (the only manipulated variable stays the plugin)."""
    argv = [
        "claude", "-p", "--model", model,
        "--plugin-dir", str(PLUGIN_DIR),
        "--output-format", "stream-json", "--verbose",
        "--permission-mode", "acceptEdits",
        "--allowedTools=" + ",".join(ALLOWED_TOOLS),
        "--settings", ISOLATION_SETTINGS,
        ARM_T_INVOCATION + prompt,
    ]
    _assert_argv_safe(argv)
    return argv


def argv_c(prompt: str, model: str) -> list[str]:
    """Arm C: no --plugin-dir; otherwise the same transport as arm T (§2
    point 5 of the pre-registration: the control is not denied any tool arm T
    has)."""
    argv = [
        "claude", "-p", "--model", model,
        "--output-format", "stream-json", "--verbose",
        "--permission-mode", "acceptEdits",
        "--allowedTools=" + ",".join(ALLOWED_TOOLS),
        "--settings", ISOLATION_SETTINGS,
        prompt,
    ]
    _assert_argv_safe(argv)
    return argv


def argv_judge(model: str) -> list[str]:
    """Judge transport: plain `-p` (the scoreline text is parsed directly from
    stdout, as in the v9.13 judge), never bypassPermissions, isolation
    settings applied for the same reason as the generation arms."""
    argv = [
        "claude", "-p", "--model", model,
        "--permission-mode", "acceptEdits",
        "--allowedTools=" + ",".join(JUDGE_ALLOWED_TOOLS),
        "--settings", ISOLATION_SETTINGS,
        JUDGE_PROMPT,
    ]
    _assert_argv_safe(argv)
    return argv


def _fresh_scratch_dir(scratch_root: Path, name: str) -> Path:
    resolved_root = scratch_root.resolve()
    if resolved_root == REPO_ROOT.resolve() or REPO_ROOT.resolve() in resolved_root.parents:
        raise TrackBError(f"scratch root {resolved_root} resolves inside the repository")
    d = resolved_root / name
    d.mkdir(parents=True, exist_ok=True)
    return d


def _collect_first_principles_files(cwd: Path, dest: Path) -> list[Path]:
    """Copy every file under <cwd>/.first-principles/ to `dest`, then clear the
    scratch subdir entirely (mirrors tests/answer-first/run.py's
    `_collect_all_files`, reimplemented here to stay independent of tests/)."""
    import shutil

    src = cwd / ".first-principles"
    out: list[Path] = []
    if src.is_dir():
        dest.mkdir(parents=True, exist_ok=True)
        for f in sorted(src.iterdir()):
            if f.is_file():
                shutil.copy2(f, dest / f.name)
                out.append(dest / f.name)
        shutil.rmtree(src, ignore_errors=True)
    for leftover in cwd.iterdir():
        if leftover.is_dir():
            shutil.rmtree(leftover, ignore_errors=True)
        else:
            leftover.unlink()
    return out


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


def cmd_plan() -> int:
    prompts = parse_catalog(CATALOG.read_text(encoding="utf-8"))
    gens = len(prompts) * 2 * RUNS_PER_CELL
    judgings = gens * JUDGES_PER_DOC
    total = gens + judgings + DRIFT_ARM_SIZE
    print("Track B registered run plan (no spend)")
    print(f"  prompts              : {len(prompts)}")
    domains = sorted({p.domain for p in prompts})
    print(f"  domains              : {', '.join(domains)}")
    print("  arms                 : 2 (T=plugin, C=unaided)")
    print(f"  runs per cell        : {RUNS_PER_CELL}")
    print(f"  generations          : {gens}")
    print(f"  judgings             : {judgings} ({JUDGES_PER_DOC} judges/doc)")
    print(f"  drift-control arm    : {DRIFT_ARM_SIZE}")
    print(f"  TOTAL live calls     : {total}")
    print()
    print("  threshold (all three must hold):")
    print(f"    1. paired permutation p < {ALPHA} (exact, 2^n enumeration)")
    print(f"    2. effect > {DRIFT_MULTIPLE}x in-run measured judge drift")
    print(f"    3. direction holds in >= {MIN_DOMAINS_IN_DIRECTION} of 4 domains")
    print()
    print("  on null: nothing is published; docs/EVIDENCE.md keeps its standing")
    print("           no-comparison disclaimer (enforced by gen-evidence-card C06).")
    return 0


def _judge_once(doc_text: str, out_path: Path, model: str) -> dict | None:
    """One blinded judging. Packet holds exactly analysis.md + rubric.md."""
    import os
    import shutil
    import tempfile

    packet = Path(tempfile.mkdtemp(prefix="tb-packet-"))
    resolved = packet.resolve()
    if resolved == REPO_ROOT.resolve() or REPO_ROOT.resolve() in resolved.parents:
        raise TrackBError(f"judge packet {resolved} is inside the repository")
    (packet / "analysis.md").write_text(doc_text, encoding="utf-8")
    shutil.copy(RUBRIC, packet / "rubric.md")
    entries = sorted(x.name for x in packet.iterdir())
    if entries != ["analysis.md", "rubric.md"]:
        raise TrackBError(f"judge packet holds unexpected files: {entries!r}")

    if judge_prompt_leaks():
        raise TrackBError("JUDGE_PROMPT leaks comparison terms; run void")

    env = {**os.environ, **_PRINT_BG_WAIT_ENV}
    argv = [
        "claude", "-p", "--model", model,
        "--no-session-persistence",
        "--permission-mode", "bypassPermissions",
        JUDGE_PROMPT,
    ]
    proc = subprocess.run(
        argv, capture_output=True, text=True, timeout=1800, cwd=packet, env=env, check=False
    )
    out = proc.stdout + proc.stderr
    out_path.write_text(out, encoding="utf-8")
    shutil.rmtree(packet, ignore_errors=True)
    return parse_scoreline(out)


def cmd_run(out_dir: Path, model: str) -> int:
    """The single registered run. Resumable: an existing capture is reused, so
    an interrupted session does not burn the one permitted attempt."""
    import random

    out_dir.mkdir(parents=True, exist_ok=True)
    gen_dir = out_dir / "generations"
    judge_dir = out_dir / "judgings"
    gen_dir.mkdir(exist_ok=True)
    judge_dir.mkdir(exist_ok=True)

    prompts = parse_catalog(CATALOG.read_text(encoding="utf-8"))
    if len(prompts) != 10:
        raise TrackBError(f"catalog holds {len(prompts)} prompts, expected 10")

    # --- Phase 1: generate -------------------------------------------------
    dispatch_failures = 0
    voided: list[str] = []
    docs: dict[str, str] = {}
    for pr in prompts:
        for arm in ("T", "C"):
            cell = f"{pr.prompt_id}-{arm}"
            cap = gen_dir / f"{cell}.txt"
            if not cap.is_file() or not cap.read_text(encoding="utf-8").strip():
                print(f"[gen] {cell} ...", flush=True)
                try:
                    run_prompt(pr.text, cap, plugin=(arm == "T"), model=model)
                except Exception as exc:  # noqa: BLE001
                    print(f"[gen] {cell} DISPATCH FAILURE: {exc}", flush=True)
                    dispatch_failures += 1
                    continue
            text = cap.read_text(encoding="utf-8")
            probs = extraction_problems(text, plugin_arm=(arm == "T"))
            if probs:
                print(f"[gen] {cell} VOIDED: {probs}", flush=True)
                voided.append(cell)
                continue
            docs[cell] = text
    print(f"[gen] captured {len(docs)}, voided {len(voided)}, "
          f"dispatch failures {dispatch_failures}", flush=True)

    # --- Phase 2: blind ----------------------------------------------------
    cells = sorted(docs)
    rng = random.Random(20260925)
    opaque = [f"D{i:03d}" for i in range(len(cells))]
    rng.shuffle(opaque)
    key = dict(zip(cells, opaque))
    (out_dir / "blinding-key.json").write_text(
        json.dumps(key, indent=2, sort_keys=True), encoding="utf-8")

    # --- Phase 3 + 4: judge, then drift-control re-judge -------------------
    unparseable = 0
    attempted = 0
    scores: dict[str, list[int]] = {c: [] for c in cells}
    drift_pairs: list[tuple[int, int]] = []
    for cell in cells:
        for j in (1, 2):
            jp = judge_dir / f"{key[cell]}-j{j}.txt"
            attempted += 1
            if jp.is_file() and jp.read_text(encoding="utf-8").strip():
                bands = parse_scoreline(jp.read_text(encoding="utf-8"))
            else:
                print(f"[judge] {key[cell]} j{j} ...", flush=True)
                bands = _judge_once(docs[cell], jp, model)
            if bands is None:
                unparseable += 1
                continue
            scores[cell].append(score_total(bands))
        # drift arm: one extra judging of the same document, same session
        dp = judge_dir / f"{key[cell]}-drift.txt"
        attempted += 1
        if dp.is_file() and dp.read_text(encoding="utf-8").strip():
            dbands = parse_scoreline(dp.read_text(encoding="utf-8"))
        else:
            print(f"[judge] {key[cell]} drift ...", flush=True)
            dbands = _judge_once(docs[cell], dp, model)
        if dbands is not None and scores[cell]:
            drift_pairs.append((scores[cell][0], score_total(dbands)))
        elif dbands is None:
            unparseable += 1

    # --- Phase 5: evaluate -------------------------------------------------
    per_prompt: dict = {}
    domain_of = {p.prompt_id: p.domain for p in prompts}
    for pr in prompts:
        tc, cc = f"{pr.prompt_id}-T", f"{pr.prompt_id}-C"
        if not scores.get(tc) or not scores.get(cc):
            continue
        per_prompt[pr.prompt_id] = {
            "domain": domain_of[pr.prompt_id],
            "T": statistics.fmean(scores[tc]),
            "C": statistics.fmean(scores[cc]),
        }

    frac = (unparseable / attempted) if attempted else 1.0
    record = evaluate(per_prompt, drift_pairs, frac, dispatch_failures)
    extra = {
        "preregistered_threshold": (
            f"paired permutation p < {ALPHA}; effect > {DRIFT_MULTIPLE}x in-run "
            f"drift; direction holds in >= {MIN_DOMAINS_IN_DIRECTION} of 4 domains"
        ),
        "observed_effect": (
            f"agent arm scored {record.get('mean_difference', 0):+.2f} points "
            f"higher on a 15-point rubric across {record.get('n_prompts', 0)} "
            f"paired problems"
        ),
        "n_per_arm": len(per_prompt),
        "measured": "2026-09-25",
        "run_id": out_dir.name,
        "model": model,
        "voided_cells": voided,
        "unparseable_fraction": round(frac, 4),
        "per_prompt_scores": per_prompt,
        "drift_pairs": drift_pairs,
    }
    _write_result(record, extra)
    print(json.dumps({**record, **{k: extra[k] for k in ("n_per_arm", "voided_cells")}},
                     indent=2, sort_keys=True))
    print(f"\nstatus: {record['status']} -- {record['reason']}")
    return 0


def _write_result(record: dict, extra: dict, *, extra_paths: tuple[Path, ...] = ()) -> None:
    payload = {**record, **extra}
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(text, encoding="utf-8")
    for p in extra_paths:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")


# ---------------------------------------------------------------------------
# trackb-2 -- the superseding registered run
# ---------------------------------------------------------------------------


def cmd_plan_2() -> int:
    prompts = parse_catalog(CATALOG.read_text(encoding="utf-8"))
    total = total_live_2()
    print("Track B (trackb-2, superseding) registered run plan (no spend)")
    print(f"  prompts              : {len(prompts)}")
    domains = sorted({p.domain for p in prompts})
    print(f"  domains              : {', '.join(domains)}")
    print("  arms                 : 2 (T=agent's delivered document, C=unaided)")
    print(f"  runs per cell        : {RUNS_PER_CELL}")
    print(f"  generations          : {len(prompts) * 2 * RUNS_PER_CELL}")
    print(f"  primary judgings     : {len(prompts) * 2 * RUNS_PER_CELL * JUDGES_PER_DOC}")
    print(f"  drift-control arm    : {DRIFT_ARM_SIZE}")
    print(f"  secondary judgings   : {SECONDARY_JUDGINGS} (orchestrator message, non-gating)")
    print(f"  TOTAL live calls     : {total}")
    print(f"  max attempts/cell    : {MAX_ATTEMPTS}")
    print(f"  void cap             : {MAX_VOID_FRACTION:.0%} of 20 cells")
    print()
    print("  threshold (all three must hold, identical to trackb):")
    print(f"    1. paired permutation p < {ALPHA} (exact, 2^n enumeration)")
    print(f"    2. effect > {DRIFT_MULTIPLE}x in-run measured judge drift")
    print(f"    3. direction holds in >= {MIN_DOMAINS_IN_DIRECTION} of 4 domains")
    print()
    print("  format-tell caveat (always reported, whatever the outcome):")
    print(f"    {FORMAT_TELL_CAVEAT}")
    print()
    print("  on null: nothing is published; docs/EVIDENCE.md keeps its standing")
    print("           no-comparison disclaimer (enforced by gen-evidence-card C06).")
    return 0


def _judge_call_2(doc_text: str, out_path: Path, model: str) -> str:
    """One blinded trackb-2 judging. Packet holds exactly analysis.md +
    rubric.md, outside the repository -- same discipline as `_judge_once`."""
    import os as _os
    import shutil
    import tempfile

    packet = Path(tempfile.mkdtemp(prefix="tb2-packet-"))
    resolved = packet.resolve()
    if resolved == REPO_ROOT.resolve() or REPO_ROOT.resolve() in resolved.parents:
        raise TrackBError(f"judge packet {resolved} is inside the repository")
    (packet / "analysis.md").write_text(doc_text, encoding="utf-8")
    shutil.copy(RUBRIC, packet / "rubric.md")
    entries = sorted(x.name for x in packet.iterdir())
    if entries != ["analysis.md", "rubric.md"]:
        raise TrackBError(f"judge packet holds unexpected files: {entries!r}")
    if judge_prompt_leaks():
        raise TrackBError("JUDGE_PROMPT leaks comparison terms; run void")
    env = {**_os.environ, **_PRINT_BG_WAIT_ENV}
    argv = argv_judge(model)
    proc = subprocess.run(argv, capture_output=True, text=True, timeout=1800, cwd=packet, env=env, check=False)
    out = proc.stdout + proc.stderr
    out_path.write_text(out, encoding="utf-8")
    shutil.rmtree(packet, ignore_errors=True)
    return out


def _judge_pool_2(out_dir: Path, prompts: tuple, model: str, *, live: bool) -> dict:
    """Blind and judge the primary + secondary pool. `live=False` (recompute)
    raises if any judging is missing rather than spending a live call."""
    import random

    gen_dir = out_dir / "generations"
    judge_dir = out_dir / "judgings"
    judge_dir.mkdir(parents=True, exist_ok=True)
    cells_path = out_dir / "cells.json"
    cells = json.loads(cells_path.read_text(encoding="utf-8")) if cells_path.is_file() else {}

    scored_prompts = sorted(
        pr.prompt_id
        for pr in prompts
        if cells.get(f"{pr.prompt_id}-T", {}).get("outcome") == "scored"
        and cells.get(f"{pr.prompt_id}-C", {}).get("outcome") == "scored"
    )
    primary_cells = sorted(f"{pid}-{arm}" for pid in scored_prompts for arm in ("T", "C"))
    secondary_candidates = sorted(scored_prompts)

    blinding_path = out_dir / "blinding-key.json"
    if blinding_path.is_file():
        key = json.loads(blinding_path.read_text(encoding="utf-8"))
    elif live:
        rng = random.Random(BLINDING_SEED_2)
        pool_ids = [f"primary:{c}" for c in primary_cells] + [
            f"secondary:{p}" for p in secondary_candidates
        ]
        opaque = [f"D{i:03d}" for i in range(len(pool_ids))]
        rng.shuffle(opaque)
        key = dict(zip(pool_ids, opaque))
        blinding_path.write_text(
            json.dumps(key, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    else:
        raise TrackBError(f"{blinding_path} missing; --recompute needs a complete capture")

    def _text(kind: str, ident: str) -> str:
        if kind == "primary":
            _pid, arm = ident.rsplit("-", 1)
            suffix = "md" if arm == "T" else "txt"
            return (gen_dir / f"{ident}.{suffix}").read_text(encoding="utf-8")
        return (gen_dir / f"{ident}-T.orchestrator.txt").read_text(encoding="utf-8")

    doc_bands: dict[str, list[dict]] = {}
    drift_pairs: list[tuple[int, int]] = []
    secondary_bands: dict[str, list[dict]] = {}
    secondary_voided: list[str] = []
    unparseable_primary = 0
    attempted_primary = 0

    pool = [("primary", c) for c in primary_cells] + [
        ("secondary", p) for p in secondary_candidates
    ]
    for kind, ident in pool:
        opaque = key[f"{kind}:{ident}"]
        text = _text(kind, ident)
        if kind == "secondary" and extraction_problems(text, plugin_arm=False):
            secondary_voided.append(ident)
            continue
        for j in (1, 2):
            jp = judge_dir / f"{opaque}-j{j}.txt"
            if kind == "primary":
                attempted_primary += 1
            if jp.is_file() and jp.read_text(encoding="utf-8").strip():
                raw = jp.read_text(encoding="utf-8")
            elif live:
                print(f"[judge] {opaque} j{j} ...", flush=True)
                raw = _judge_call_2(text, jp, model)
            else:
                raise TrackBError(f"{jp} missing; --recompute needs a complete capture")
            if is_limit_stub(raw):
                raise TrackBPause(f"usage-limit stub at {jp}")
            bands = parse_scoreline(raw)
            if bands is None:
                if kind == "primary":
                    unparseable_primary += 1
                continue
            if kind == "primary":
                doc_bands.setdefault(ident, []).append(bands)
            else:
                secondary_bands.setdefault(ident, []).append(bands)
        if kind == "primary":
            dp = judge_dir / f"{opaque}-drift.txt"
            attempted_primary += 1
            if dp.is_file() and dp.read_text(encoding="utf-8").strip():
                draw = dp.read_text(encoding="utf-8")
            elif live:
                print(f"[judge] {opaque} drift ...", flush=True)
                draw = _judge_call_2(text, dp, model)
            else:
                raise TrackBError(f"{dp} missing; --recompute needs a complete capture")
            if is_limit_stub(draw):
                raise TrackBPause(f"usage-limit stub at {dp}")
            dbands = parse_scoreline(draw)
            if dbands is None:
                unparseable_primary += 1
            elif doc_bands.get(ident):
                drift_pairs.append((score_total(doc_bands[ident][0]), score_total(dbands)))

    return {
        "scored_prompts": scored_prompts,
        "primary_cells": primary_cells,
        "doc_bands": doc_bands,
        "drift_pairs": drift_pairs,
        "secondary_bands": secondary_bands,
        "secondary_voided": secondary_voided,
        "unparseable_primary": unparseable_primary,
        "attempted_primary": attempted_primary,
    }


def _build_record_2(
    prompts: tuple, domain_of: dict, pool: dict, cells: dict, voided_cells: list,
    *, model: str, measured_date: str,
) -> tuple[dict, dict]:
    per_prompt: dict = {}
    for pid in pool["scored_prompts"]:
        tband = pool["doc_bands"].get(f"{pid}-T")
        cband = pool["doc_bands"].get(f"{pid}-C")
        if not tband or not cband:
            continue
        per_prompt[pid] = {
            "domain": domain_of[pid],
            "T": statistics.fmean(score_total(b) for b in tband),
            "C": statistics.fmean(score_total(b) for b in cband),
        }

    frac = (
        (pool["unparseable_primary"] / pool["attempted_primary"])
        if pool["attempted_primary"]
        else 1.0
    )
    void_fraction = round(len(voided_cells) / 20, 4)
    record = evaluate(per_prompt, pool["drift_pairs"], frac, 0, void_fraction=void_fraction)

    per_crit: dict[str, dict[str, list[int]]] = {arm: {c: [] for c in _CRITERIA} for arm in ("T", "C")}
    for pid in pool["scored_prompts"]:
        for arm in ("T", "C"):
            for bands in pool["doc_bands"].get(f"{pid}-{arm}", []):
                for c in _CRITERIA:
                    per_crit[arm][c].append(_BAND_WEIGHTS[bands[c]])
    per_criterion_means = {
        arm: {
            c: (round(statistics.fmean(vals), 3) if vals else None)
            for c, vals in crits.items()
        }
        for arm, crits in per_crit.items()
    }

    words: dict[str, list[int]] = {"T": [], "C": []}
    for pid in pool["scored_prompts"]:
        for arm in ("T", "C"):
            w = cells.get(f"{pid}-{arm}", {}).get("words")
            if w is not None:
                words[arm].append(w)
    words_summary = {
        arm: {
            "mean": round(statistics.fmean(ws), 1) if ws else None,
            "median": statistics.median(ws) if ws else None,
            "min": min(ws) if ws else None,
            "max": max(ws) if ws else None,
        }
        for arm, ws in words.items()
    }

    agree_hits = 0
    agree_total = 0
    abs_diffs: list[int] = []
    per_crit_diffs: dict[str, list[int]] = {c: [] for c in _CRITERIA}
    for pid in pool["scored_prompts"]:
        for arm in ("T", "C"):
            bl = pool["doc_bands"].get(f"{pid}-{arm}", [])
            if len(bl) < 2:
                continue
            j1, j2 = bl[0], bl[1]
            agree_total += 1
            if j1 == j2:
                agree_hits += 1
            abs_diffs.append(abs(score_total(j1) - score_total(j2)))
            for c in _CRITERIA:
                per_crit_diffs[c].append(abs(_BAND_WEIGHTS[j1[c]] - _BAND_WEIGHTS[j2[c]]))
    agreement = {
        "exact_band_agreement_rate": round(agree_hits / agree_total, 4) if agree_total else None,
        "mean_abs_diff_total": round(statistics.fmean(abs_diffs), 3) if abs_diffs else None,
        "mean_abs_diff_per_criterion": {
            c: (round(statistics.fmean(vals), 3) if vals else None)
            for c, vals in per_crit_diffs.items()
        },
        "n_pairs": agree_total,
    }

    secondary_means: dict[str, float] = {}
    for pid in pool["scored_prompts"]:
        bl = pool["secondary_bands"].get(pid, [])
        if bl:
            secondary_means[pid] = round(statistics.fmean(score_total(b) for b in bl), 3)
    secondary_summary_gap = None
    common = [pid for pid in per_prompt if pid in secondary_means]
    if common:
        gaps = [per_prompt[pid]["T"] - secondary_means[pid] for pid in common]
        secondary_summary_gap = round(statistics.fmean(gaps), 3)

    directional = {
        "prediction": (
            "largest on Assumption Surfacing (C3) and Falsifiability (C5), "
            "smallest on Decision Usefulness (C1)"
        ),
        "observed_diff_by_criterion": {
            c: (
                round(per_criterion_means["T"][c] - per_criterion_means["C"][c], 3)
                if per_criterion_means["T"][c] is not None
                and per_criterion_means["C"][c] is not None
                else None
            )
            for c in _CRITERIA
        },
    }

    extra = {
        "preregistered_threshold": (
            f"paired permutation p < {ALPHA}; effect > {DRIFT_MULTIPLE}x in-run drift; "
            f"direction holds in >= {MIN_DOMAINS_IN_DIRECTION} of 4 domains"
        ),
        "observed_effect": (
            f"agent arm scored {record.get('mean_difference', 0):+.2f} points higher on a "
            f"15-point rubric across {record.get('n_prompts', 0)} paired problems"
        ),
        "n_per_arm": len(per_prompt),
        "measured": measured_date,
        "run_id": RUN_ID_2,
        "model": model,
        "preregistration": "docs/trackb-2-preregistration.md",
        "supersedes": "trackb",
        "caveat": FORMAT_TELL_CAVEAT,
        "secondary_summary_gap": secondary_summary_gap,
        "voided_cells": sorted(voided_cells),
        "unparseable_fraction": round(frac, 4),
        "void_fraction": void_fraction,
        "per_prompt_scores": per_prompt,
        "drift_pairs": pool["drift_pairs"],
        "per_criterion_means": per_criterion_means,
        "directional_prediction": directional,
        "words_per_arm": words_summary,
        "inter_rater_agreement": agreement,
        "secondary_means": secondary_means,
        "counts": {
            "voided_cells": len(voided_cells),
            "extraction_voids_secondary": len(pool["secondary_voided"]),
            "unparseable_primary": pool["unparseable_primary"],
            "attempted_primary": pool["attempted_primary"],
        },
    }
    return record, extra


def cmd_run_2(out_dir: Path, scratch_root: Path, model: str) -> int:
    """The single trackb-2 registered run. Resumable: a recorded attempt or
    judging is reused rather than re-spent; a usage-limit pause leaves the
    partial capture untouched and exits 3 for the caller to resume later."""
    import datetime
    import hashlib
    import os

    out_dir.mkdir(parents=True, exist_ok=True)
    result_path = out_dir / "result.json"
    if result_path.is_file():
        sys.stderr.write(f"[trackb-2] {result_path} already exists; this run is complete\n")
        return 1

    resolved_scratch = scratch_root.resolve()
    if resolved_scratch == REPO_ROOT.resolve() or REPO_ROOT.resolve() in resolved_scratch.parents:
        raise TrackBError(f"--scratch {resolved_scratch} resolves inside the repository")
    resolved_scratch.mkdir(parents=True, exist_ok=True)

    raw_dir = out_dir / "raw"
    gen_dir = out_dir / "generations"
    judge_dir = out_dir / "judgings"
    for d in (raw_dir, gen_dir, judge_dir):
        d.mkdir(parents=True, exist_ok=True)

    head_sha = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True
    ).strip()
    body_path = PLUGIN_DIR / "agents" / "first-principles.md"
    body_sha256 = hashlib.sha256(body_path.read_bytes()).hexdigest()

    manifest_path = out_dir / "manifest.json"
    now = datetime.datetime.now(datetime.UTC).isoformat().replace("+00:00", "Z")
    if manifest_path.is_file():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("body_sha256") != body_sha256:
            manifest_path.write_text(
                json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
            )
            raise TrackBAbort(
                "first-principles.md sha256 changed since the run started "
                f"({manifest.get('body_sha256')} -> {body_sha256})"
            )
        manifest.setdefault("resumed_utc", []).append(now)
    else:
        manifest = {
            "protocol": "trackb-2",
            "run_id": RUN_ID_2,
            "started_utc": now,
            "head_sha": head_sha,
            "body_sha256": body_sha256,
            "model": model,
            "argv_t_template": argv_t("<prompt>", model),
            "argv_c_template": argv_c("<prompt>", model),
            "argv_judge_template": argv_judge(model),
            "isolation_settings": json.loads(ISOLATION_SETTINGS),
            "blinding_seed": BLINDING_SEED_2,
            "resumed_utc": [],
        }
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    prompts = parse_catalog(CATALOG.read_text(encoding="utf-8"))
    if len(prompts) != 10:
        raise TrackBError(f"catalog holds {len(prompts)} prompts, expected 10")
    domain_of = {p.prompt_id: p.domain for p in prompts}

    cells_path = out_dir / "cells.json"
    cells: dict = json.loads(cells_path.read_text(encoding="utf-8")) if cells_path.is_file() else {}

    def _save_cells() -> None:
        cells_path.write_text(
            json.dumps(cells, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )

    resume_cmd = (
        "python3 scripts/check-trackb-comparative.py --run --protocol trackb-2 "
        f"--out {out_dir} --scratch {scratch_root} --model {model}"
    )

    def _run_cell(pr: Prompt, arm: str) -> None:
        cell = f"{pr.prompt_id}-{arm}"
        rec = cells.get(cell, {"outcome": "pending", "attempts": []})
        if rec.get("outcome") in ("scored", "void"):
            return
        subdir = _fresh_scratch_dir(resolved_scratch, cell)
        attempts: list[str] = list(rec.get("attempts", []))
        void_reason = None
        env = {**os.environ, "CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS": "0"}
        for n in range(len(attempts) + 1, MAX_ATTEMPTS + 1):
            argv = argv_t(pr.text, model) if arm == "T" else argv_c(pr.text, model)
            print(f"[gen] {cell} attempt {n} ...", flush=True)
            proc = subprocess.run(
                argv, capture_output=True, text=True, timeout=5400, env=env, cwd=subdir, check=False
            )
            jsonl = proc.stdout
            raw_path = raw_dir / f"{cell}.a{n}.jsonl"
            raw_path.write_text(jsonl, encoding="utf-8")
            files = _collect_first_principles_files(subdir, raw_dir / f"{cell}.a{n}.files")
            attempts.append(raw_path.name)
            if is_limit_stub(jsonl):
                stub_path = raw_dir / f"{cell}.a{n}.limit-stub.jsonl"
                raw_path.rename(stub_path)
                attempts[-1] = stub_path.name
                rec.update({"outcome": "pending", "attempts": attempts})
                cells[cell] = rec
                _save_cells()
                print(f"[pause] {cell}: usage-limit stub. Resume with:\n  {resume_cmd}", flush=True)
                raise TrackBPause(f"usage-limit stub at {stub_path}")
            problems = init_check(jsonl, arm)
            if problems:
                rec.update({"outcome": "aborted", "attempts": attempts, "abort_reason": problems})
                cells[cell] = rec
                _save_cells()
                raise TrackBAbort(f"{cell}: " + "; ".join(problems))
            if arm == "T":
                disp = dispatched(jsonl)
                candidates = sorted(
                    (p for p in files if p.name.startswith("analysis-") and p.suffix == ".md"),
                    key=lambda p: p.stat().st_size,
                )
                if not disp or not candidates:
                    void_reason = "not dispatched" if not disp else "no delivered analysis-*.md file"
                    print(f"[miss] {cell} attempt {n}: {void_reason}", flush=True)
                    rec.update({"outcome": "pending", "attempts": attempts, "dispatched": disp})
                    cells[cell] = rec
                    _save_cells()
                    continue
                docfile = candidates[-1]
                text = docfile.read_text(encoding="utf-8")
                probs = extraction_problems(text, plugin_arm=True)
                if probs:
                    void_reason = "; ".join(probs)
                    print(f"[miss] {cell} attempt {n}: {void_reason}", flush=True)
                    rec.update({"outcome": "pending", "attempts": attempts, "dispatched": disp})
                    cells[cell] = rec
                    _save_cells()
                    continue
                (gen_dir / f"{pr.prompt_id}-T.md").write_text(text, encoding="utf-8")
                (gen_dir / f"{pr.prompt_id}-T.orchestrator.txt").write_text(
                    final_message(jsonl), encoding="utf-8"
                )
                rec.update(
                    {
                        "outcome": "scored", "attempts": attempts, "dispatched": True,
                        "delivered": docfile.name, "words": len(text.split()),
                    }
                )
                cells[cell] = rec
                _save_cells()
                return
            else:
                text = final_message(jsonl)
                probs = extraction_problems(text, plugin_arm=False)
                if probs:
                    void_reason = "; ".join(probs)
                    print(f"[miss] {cell} attempt {n}: {void_reason}", flush=True)
                    rec.update({"outcome": "pending", "attempts": attempts})
                    cells[cell] = rec
                    _save_cells()
                    continue
                (gen_dir / f"{pr.prompt_id}-C.txt").write_text(text, encoding="utf-8")
                rec.update({"outcome": "scored", "attempts": attempts, "words": len(text.split())})
                cells[cell] = rec
                _save_cells()
                return
        rec.update({"outcome": "void", "attempts": attempts, "void_reason": void_reason})
        cells[cell] = rec
        _save_cells()
        print(f"[gen] {cell} VOID after {len(attempts)} attempts: {void_reason}", flush=True)

    try:
        for pr in prompts:
            _run_cell(pr, "T")
        for pr in prompts:
            _run_cell(pr, "C")

        voided_cells = [c for c, r in cells.items() if r.get("outcome") == "void"]
        pool = _judge_pool_2(out_dir, prompts, model, live=True)
        record, extra = _build_record_2(
            prompts, domain_of, pool, cells, voided_cells,
            model=model, measured_date=manifest["started_utc"][:10],
        )
    except TrackBPause as exc:
        sys.stderr.write(f"[pause] {exc}\n")
        print(f"Resume with:\n  {resume_cmd}", flush=True)
        return 3
    except TrackBAbort as exc:
        sys.stderr.write(f"[abort] {exc}\n")
        return 5

    _write_result(record, extra, extra_paths=(result_path,))
    print(json.dumps({**record, **extra}, indent=2, sort_keys=True))
    print(f"\nstatus: {record['status']} -- {record['reason']}")
    return 0


def cmd_recompute_2(out_dir: Path) -> int:
    """Recompute the trackb-2 result from frozen captures only (no subprocess)
    and confirm it reproduces the recorded result.json exactly."""
    manifest_path = out_dir / "manifest.json"
    cells_path = out_dir / "cells.json"
    if not manifest_path.is_file() or not cells_path.is_file():
        raise TrackBError(f"{out_dir} holds no manifest.json/cells.json to recompute from")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    cells = json.loads(cells_path.read_text(encoding="utf-8"))
    prompts = parse_catalog(CATALOG.read_text(encoding="utf-8"))
    domain_of = {p.prompt_id: p.domain for p in prompts}
    voided_cells = [c for c, r in cells.items() if r.get("outcome") == "void"]

    pool = _judge_pool_2(out_dir, prompts, manifest["model"], live=False)
    record, extra = _build_record_2(
        prompts, domain_of, pool, cells, voided_cells,
        model=manifest["model"], measured_date=manifest["started_utc"][:10],
    )
    # Round-trip through JSON before comparing: the live record holds Python
    # tuples (e.g. drift_pairs) that a JSON list will never `==` even when
    # every element matches -- comparing both sides post-serialisation is
    # what "reproduces result.json" actually means.
    fresh = json.loads(json.dumps({**record, **extra}))

    existing_path = out_dir / "result.json"
    if not existing_path.is_file():
        raise TrackBError(f"{existing_path} missing; nothing to recompute against")
    existing = json.loads(existing_path.read_text(encoding="utf-8"))
    mismatches = {k: (existing.get(k), v) for k, v in fresh.items() if existing.get(k) != v}
    if mismatches:
        for k, (old, new) in mismatches.items():
            sys.stderr.write(f"[recompute] mismatch on {k!r}: recorded={old!r} recomputed={new!r}\n")
        return 1
    print(f"recompute: {existing_path} reproduced exactly ({len(fresh)} fields)")
    return 0


def _run_streaming_until_dispatch_or_result(argv: list[str], cwd: Path, timeout: int) -> str:
    """Popen + line-by-line read, terminating as soon as a dispatch tool_use or
    a `result` event is seen -- saves most of a 10-20 minute generation when
    used for a cheap pre-run probe, which is the only caller."""
    import os
    import time

    env = {**os.environ, "CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS": "0"}
    proc = subprocess.Popen(
        argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, cwd=cwd, env=env
    )
    lines: list[str] = []
    start = time.time()
    try:
        assert proc.stdout is not None
        for line in proc.stdout:
            lines.append(line)
            stripped = line.strip()
            if stripped:
                try:
                    obj = json.loads(stripped)
                except json.JSONDecodeError:
                    obj = None
                if obj is not None:
                    if obj.get("type") == "result":
                        break
                    if obj.get("type") == "assistant":
                        content = (obj.get("message") or {}).get("content") or []
                        if any(
                            isinstance(b, dict)
                            and b.get("type") == "tool_use"
                            and b.get("name") in ("Agent", "Task")
                            for b in content
                        ):
                            break
            if time.time() - start > timeout:
                break
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
    return "".join(lines)


def cmd_probe_2(out_dir: Path, scratch_root: Path, model: str) -> int:
    """Pre-run mechanics probe (not scored): confirms arm C isolation and arm
    T dispatch via ARM_T_INVOCATION, terminated at first dispatch/result."""
    probe_dir = out_dir / "probe"
    probe_dir.mkdir(parents=True, exist_ok=True)
    resolved_scratch = scratch_root.resolve()
    if resolved_scratch == REPO_ROOT.resolve() or REPO_ROOT.resolve() in resolved_scratch.parents:
        raise TrackBError(f"--scratch {resolved_scratch} resolves inside the repository")
    resolved_scratch.mkdir(parents=True, exist_ok=True)

    c_dir = _fresh_scratch_dir(resolved_scratch, "probe-c")
    argv_c_probe = argv_c("Reply with the single word OK.", model)
    out_c = _run_streaming_until_dispatch_or_result(argv_c_probe, c_dir, timeout=180)
    (probe_dir / "probe-c.jsonl").write_text(out_c, encoding="utf-8")
    c_problems = init_check(out_c, "C")

    # A non-catalog problem, so this probe can never be reused as a registered
    # cell (§Transport probe, docs/trackb-2-preregistration.md).
    probe_prompt = (
        "As a quick sanity check unrelated to any catalog problem: what is the single "
        "most load-bearing assumption in deciding whether to switch a small team from "
        "weekly to daily deploys?"
    )
    t_dir = _fresh_scratch_dir(resolved_scratch, "probe-t")
    argv_t_probe = argv_t(probe_prompt, model)
    out_t = _run_streaming_until_dispatch_or_result(argv_t_probe, t_dir, timeout=1200)
    (probe_dir / "probe-t.jsonl").write_text(out_t, encoding="utf-8")
    t_problems = init_check(out_t, "T")
    t_dispatched = dispatched(out_t)
    _collect_first_principles_files(t_dir, probe_dir / "probe-t.files")

    result = {
        "arm_c_init_ok": not c_problems,
        "arm_t_init_ok": not t_problems,
        "arm_t_dispatched": t_dispatched,
        "plugins": {"arm_c": init_plugins(out_c), "arm_t": init_plugins(out_t)},
        "problems": {"arm_c": c_problems, "arm_t": t_problems},
    }
    (probe_dir / "probe.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    ok = result["arm_c_init_ok"] and result["arm_t_init_ok"] and result["arm_t_dispatched"]
    return 0 if ok else 1


# ---------------------------------------------------------------------------
# Self-test controls
# ---------------------------------------------------------------------------


def _c01_rubric_is_format_neutral() -> str | None:
    """THE integrity control for this whole comparison."""
    if not RUBRIC.is_file():
        return f"{RUBRIC} missing"
    text = RUBRIC.read_text(encoding="utf-8").lower()
    hits = [t for t in _FORMAT_TOKENS if t in text]
    if hits:
        return (
            "neutral rubric contains format token(s) "
            f"{hits!r} — it would reward the agent's output shape and rig the run"
        )
    return None


def _c02_rubric_declares_format_carries_no_marks() -> str | None:
    text = RUBRIC.read_text(encoding="utf-8")
    if "Format carries no marks" not in text:
        return "rubric does not state that format carries no marks"
    if "Length carries no marks" not in text:
        return "rubric does not neutralise length"
    return None


def _c03_judge_prompt_does_not_leak() -> str | None:
    leaks = judge_prompt_leaks()
    if leaks:
        return f"JUDGE_PROMPT leaks comparison terms: {leaks!r}"
    return None


def _c04_catalog_parses_and_is_balanced() -> str | None:
    prompts = parse_catalog(CATALOG.read_text(encoding="utf-8"))
    if len(prompts) != 10:
        return f"catalog parsed {len(prompts)} prompts, expected 10"
    domains = {p.domain for p in prompts}
    if len(domains) != 4:
        return f"catalog covers {len(domains)} domains, expected 4"
    for p in prompts:
        if len(p.text.split()) < 15:
            return f"{p.prompt_id}: prompt text implausibly short"
    return None


def _c05_scoreline_roundtrip() -> str | None:
    good = (
        f"blah\n{_SCORELINE_START}\nC1: Rigorous\nC2: Sound\nC3: Hand-wavy\n"
        f"C4: Absent\nC5: Sound\n{_SCORELINE_END}\n"
    )
    bands = parse_scoreline(good)
    if bands is None:
        return "a well-formed scoreline failed to parse"
    if score_total(bands) != 3 + 2 + 1 + 0 + 2:
        return f"score_total wrong: {score_total(bands)}"
    return None


def _c06_malformed_scorelines_rejected() -> str | None:
    cases = {
        "missing block": "no block here",
        "missing criterion": f"{_SCORELINE_START}\nC1: Sound\n{_SCORELINE_END}",
        "off-vocabulary band": (
            f"{_SCORELINE_START}\nC1: Excellent\nC2: Sound\nC3: Sound\n"
            f"C4: Sound\nC5: Sound\n{_SCORELINE_END}"
        ),
    }
    for name, text in cases.items():
        if parse_scoreline(text) is not None:
            return f"malformed scoreline accepted: {name}"
    return None


def _c07_permutation_test_is_calibrated() -> str | None:
    """Known inputs, known answers. A test that cannot fail measures nothing."""
    if paired_permutation_p([0.0] * 10) != 1.0:
        return "all-zero differences did not return p=1.0"
    # A maximally consistent effect over 10 pairs: only the all-positive and
    # all-negative sign assignments reach the observed mean => 2/1024.
    p_strong = paired_permutation_p([2.0] * 10)
    if abs(p_strong - 2 / 1024) > 1e-9:
        return f"uniform effect p={p_strong}, expected {2/1024}"
    # A symmetric split must be far from significant.
    p_null = paired_permutation_p([1.0, -1.0] * 5)
    if p_null < 0.5:
        return f"symmetric differences gave p={p_null}, expected >= 0.5"
    return None


def _c08_drift_threshold_blocks_a_noise_sized_effect() -> str | None:
    """The anti-masking control: a statistically clean but noise-sized effect
    must NOT clear, because that is exactly what one-sided judge drift produces."""
    per_prompt = {
        f"TB-{i:02d}": {
            "domain": ["software", "policy", "science", "personal"][i % 4],
            "T": 10.0,
            "C": 9.0,
        }
        for i in range(1, 11)
    }
    # Drift of 1.0 means the bar is 2.0; the effect is 1.0 and must fail.
    res = evaluate(per_prompt, [(10, 11)] * 20, 0.0, 0)
    if res["status"] == "cleared":
        return "an effect smaller than 2x drift was cleared"
    if "does not exceed" not in res["reason"]:
        return f"wrong reason for rejection: {res['reason']}"
    return None


def _c09_missing_drift_arm_cannot_clear() -> str | None:
    per_prompt = {
        f"TB-{i:02d}": {
            "domain": ["software", "policy", "science", "personal"][i % 4],
            "T": 14.0,
            "C": 4.0,
        }
        for i in range(1, 11)
    }
    res = evaluate(per_prompt, [], 0.0, 0)
    if res["status"] == "cleared":
        return "a run with no drift-control arm reached cleared"
    return None


def _c10_a_real_effect_does_clear() -> str | None:
    """Positive control: the threshold must be reachable, or it measures nothing."""
    per_prompt = {
        f"TB-{i:02d}": {
            "domain": ["software", "policy", "science", "personal"][i % 4],
            "T": 13.0,
            "C": 8.0,
        }
        for i in range(1, 11)
    }
    res = evaluate(per_prompt, [(10, 10)] * 18 + [(10, 11)] * 2, 0.0, 0)
    if res["status"] != "cleared":
        return f"a large, consistent, low-drift effect did not clear: {res['reason']}"
    return None


def _c11_broken_mechanics_is_inconclusive_not_null() -> str | None:
    per_prompt = {
        "TB-01": {"domain": "software", "T": 10.0, "C": 9.0},
    }
    res = evaluate(per_prompt, [(10, 10)], 0.0, dispatch_failures=3)
    if res["status"] != "inconclusive":
        return f"dispatch failures produced {res['status']!r}, expected inconclusive"
    res2 = evaluate(per_prompt, [(10, 10)], 0.5, 0)
    if res2["status"] != "inconclusive":
        return f"high unparseable rate produced {res2['status']!r}"
    return None


def _c12_extraction_integrity_detects_both_faults() -> str | None:
    contaminated = "word " * 200 + _SCORELINE_START
    if not any("contamination" in p for p in extraction_problems(contaminated)):
        return "rubric contamination not detected"
    if not any("short" in p for p in extraction_problems("too short")):
        return "implausibly short capture not detected"
    clean = "word " * 400
    if extraction_problems(clean):
        return "a clean capture was flagged"
    return None


def _c18_plugin_arm_rejects_an_orchestrator_summary() -> str | None:
    """The v9.13 defect, as a standing control (docs/trackb-transport-erratum.md).

    A 400-word summary with no contract sections must void on the plugin arm and
    must NOT void on the control arm -- the control is unaided and never carries the
    contract, so a symmetric check would void every control cell.
    """
    summary = ("Here's the analysis, distilled from the full first-principles "
               "breakdown: " + "the city should price congestion. " * 80)
    if len(summary.split()) < 120:
        return "C18 fixture is under the word floor; it would void for the wrong reason"
    plugin = extraction_problems(summary, plugin_arm=True)
    if not any("not the agent's document" in x for x in plugin):
        return "C18: a plugin-arm summary was accepted -- the v9.13 defect can recur"
    if extraction_problems(summary, plugin_arm=False):
        return ("C18: the same text voided on the CONTROL arm; that would void every "
                "control cell and destroy the comparison")
    document = ("# Analysis\n## Problem Essence\n## Assumptions Table\n"
                "## Ground Truths\n## Derivation Chains\n## Abandoned Reasoning\n"
                "## Conclusion\n" + "word " * 300)
    if extraction_problems(document, plugin_arm=True):
        return f"C18: a real agent document voided: {extraction_problems(document, plugin_arm=True)}"
    return None


def _c19_the_frozen_arm_t_captures_would_now_void() -> str | None:
    """Re-run against the evidence: every one of the ten frozen arm-T captures must
    fail the guard. If any passes, the guard does not cover the case it was built for."""
    gens = REPO_ROOT / "tests" / "trackb-run-v9.13" / "generations"
    if not gens.is_dir():
        return None  # frozen evidence absent (shallow clone); not a failure
    passed = [f.name for f in sorted(gens.glob("TB-*-T.txt"))
              if not extraction_problems(f.read_text(encoding="utf-8"), plugin_arm=True)]
    if passed:
        return (f"C19: {len(passed)} frozen arm-T summaries still pass the plugin-arm "
                f"guard ({passed[:3]})")
    controls = [f.name for f in sorted(gens.glob("TB-*-C.txt"))
                if extraction_problems(f.read_text(encoding="utf-8"), plugin_arm=False)]
    if controls:
        return f"C19: {len(controls)} frozen CONTROL captures void under the unchanged check ({controls[:3]})"
    return None


def _c13_prereg_and_code_constants_agree() -> str | None:
    """The code is the pre-registration's executable form; drift between them
    would let the run follow a protocol nobody registered."""
    if not PREREG.is_file():
        return f"{PREREG} missing"
    # Whitespace-normalised so a literal hard-wrapped across lines is still
    # found -- the same discipline score-technique-adoption.py applies, and for
    # the same reason: a reflowed paragraph is not a changed claim.
    text = " ".join(PREREG.read_text(encoding="utf-8").split())
    required = {
        "runs per cell": "**Runs per cell:** 1",
        "judges": "2 independent blinded judges",
        "drift arm": "20 documents re-judged",
        "alpha": "*p* < 0.05",
        "drift multiple": "twice the in-run measured judge drift",
        "domains": "at least three of the four domains",
        "total calls": "**Total live invocations: 80.**",
    }
    for name, literal in required.items():
        if literal not in text:
            return f"pre-registration no longer states {name}: {literal!r}"
    prompts = parse_catalog(CATALOG.read_text(encoding="utf-8"))
    expected_total = (
        len(prompts) * 2 * RUNS_PER_CELL
        + len(prompts) * 2 * RUNS_PER_CELL * JUDGES_PER_DOC
        + DRIFT_ARM_SIZE
    )
    if expected_total != 80:
        return (
            f"code constants imply {expected_total} calls but the "
            "pre-registration states 80"
        )
    return None


def _c15_transport_carries_the_bg_wait_fix() -> str | None:
    """Without this env var the treatment arm captures a delegation stub instead
    of an analysis, and the run produces a confident, false negative result.
    Measured before any registered run; see `_PRINT_BG_WAIT_ENV`'s comment."""
    if _PRINT_BG_WAIT_ENV.get("CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS") != "0":
        return "the print-mode background-wait ceiling is not disabled"
    src = Path(__file__).read_text(encoding="utf-8")
    if "env=env" not in src:
        return "run_prompt() does not pass the patched environment to the subprocess"
    text = " ".join(PREREG.read_text(encoding="utf-8").split())
    if "CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS" not in text:
        return "the pre-registration does not pin the corrected transport"
    return None


def _c16_a_delegation_stub_would_be_rejected() -> str | None:
    """The exact broken capture, verbatim, must not reach a judge."""
    stub = (
        "Background tasks still running after 600s; terminating. "
        "I've delegated this to the first-principles agent, which will decompose "
        "the decision into ground truths, challenge the usual assumptions, and "
        "reason upward to a validated conclusion. It's running in the background "
        "- I'll share the full analysis once it completes."
    )
    if not extraction_problems(stub):
        return "the measured delegation-stub capture was accepted for scoring"
    return None


def _c17_status_cannot_be_asserted_by_a_caller() -> str | None:
    """The module docstring claims there is no path by which a human sets
    `status`. That claim was untested until now.

    `evaluate()` must derive the verdict from the recorded numbers alone, so a
    caller cannot pass a favourable status in alongside disappointing data. This
    is the structural half of "publish only if non-null": the decision rule is
    only honest if the decision is computed, and an untested claim that it is
    computed is not a guarantee.
    """
    import inspect

    sig = inspect.signature(evaluate)
    forbidden = {"status", "verdict", "cleared", "result", "publish"}
    offending = forbidden.intersection(sig.parameters)
    if offending:
        return (
            f"evaluate() accepts caller-supplied verdict parameter(s) {sorted(offending)} "
            "— status must be derived, never asserted"
        )
    # A disappointing dataset must reach `null` no matter how it is presented.
    flat = {
        f"TB-{i:02d}": {
            "domain": ["software", "policy", "science", "personal"][i % 4],
            "T": 9.0,
            "C": 9.0,
        }
        for i in range(1, 11)
    }
    if evaluate(flat, [(10, 10)] * 20, 0.0, 0)["status"] != "null":
        return "a zero-effect dataset did not evaluate to null"
    return None


def _c14_status_vocabulary_matches_the_card() -> str | None:
    """Only `cleared` may publish. The card enforces this too; asserted on both
    sides so a rename on either surface is caught."""
    produced = set()
    per = {"TB-01": {"domain": "software", "T": 10.0, "C": 9.0}}
    produced.add(evaluate(per, [(10, 10)], 0.0, 1)["status"])
    produced.add(evaluate(per, [(10, 10)], 0.0, 0)["status"])
    per_big = {
        f"TB-{i:02d}": {
            "domain": ["software", "policy", "science", "personal"][i % 4],
            "T": 13.0, "C": 8.0,
        }
        for i in range(1, 11)
    }
    produced.add(evaluate(per_big, [(10, 10)] * 20, 0.0, 0)["status"])
    allowed = {"cleared", "null", "inconclusive"}
    if not produced <= allowed:
        return f"evaluate() produced status outside the vocabulary: {produced - allowed}"
    if "cleared" not in produced:
        return "no input reached 'cleared'; the threshold is unreachable"
    return None


# ---------------------------------------------------------------------------
# trackb-2 self-test controls
# ---------------------------------------------------------------------------

# Whitespace-normalised leading-'>' strip, shared with docs/trackb-2-preregistration.md's
# own §Unchanged block extraction.
_UNCHANGED_HEADING_RE = re.compile(r"(?ms)^## [^\n]*Unchanged[^\n]*\n(.*?)(?=^## )")
_BLOCKQUOTE_RE = re.compile(r"(?m)(?:^[ \t]*>.*(?:\n|\Z))+")
_LEADING_QUOTE_RE = re.compile(r"(?m)^[ \t]*(>[ \t]?)+")


def _norm_quote(s: str) -> str:
    return " ".join(_LEADING_QUOTE_RE.sub("", s).split())


def _c20_prereg2_code_agree() -> str | None:
    """The code is trackb-2's executable form; drift between the doc and the
    pinned constants would let the superseding run follow a protocol nobody
    registered -- same discipline as C13, extended to the new constants."""
    if not PREREG_2.is_file():
        return f"{PREREG_2} missing"
    # Leading '>' blockquote markers are stripped before whitespace-joining, so
    # a phrase that happens to wrap across two quoted lines (leaving a bare
    # '>' mid-phrase after a naive join) is still found.
    text = _norm_quote(PREREG_2.read_text(encoding="utf-8"))
    checks = {
        "runs per cell 1": "**Runs per cell:** 1" in text,
        "2 independent blinded judges": "2 independent blinded judges" in text,
        "20 documents re-judged": "20 documents re-judged" in text,
        "p < 0.05": "*p* < 0.05" in text,
        "twice the in-run measured judge drift": "twice the in-run measured judge drift" in text,
        "at least three of the four domains": "at least three of the four domains" in text,
        "max 3 attempts": "up to 3 attempts" in text,
        "10% void cap": "10% of the 20 cells" in text,
        "model claude-sonnet-5": "claude-sonnet-5" in text,
        "ARM_T_INVOCATION prefix": ARM_T_INVOCATION.strip() in text,
        "blinding seed": str(BLINDING_SEED_2) in text,
        "FORMAT_TELL_CAVEAT sentence": " ".join(FORMAT_TELL_CAVEAT.split()) in text,
        "resume-continues-same-run sentence": (
            "never regenerated" in text and "same single run" in text
        ),
        "Supersedes + both cited paths": (
            "Supersedes" in text
            and "docs/trackb-preregistration.md" in text
            and "tests/trackb-run-v9.13" in text
        ),
    }
    missing = [k for k, ok in checks.items() if not ok]
    if missing:
        return f"pre-registration no longer states: {missing}"
    total = total_live_2()
    if str(total) not in text:
        return f"code implies total live invocations {total}, not found in doc text"
    return None


def _c21_void_cap_blocks_and_default_preserves_old_controls() -> str | None:
    per_prompt = {
        f"TB-{i:02d}": {
            "domain": ["software", "policy", "science", "personal"][i % 4],
            "T": 13.0,
            "C": 8.0,
        }
        for i in range(1, 11)
    }
    drift_pairs = [(10, 10)] * 18 + [(10, 11)] * 2
    res_high = evaluate(per_prompt, drift_pairs, 0.0, 0, void_fraction=3 / 20)
    if res_high["status"] != "inconclusive":
        return f"void_fraction 3/20 did not produce inconclusive: {res_high['status']}"
    res_ok = evaluate(per_prompt, drift_pairs, 0.0, 0, void_fraction=2 / 20)
    if res_ok["status"] == "inconclusive":
        return "void_fraction 2/20 with clean mechanics produced inconclusive"
    preserved = {"C08", "C09", "C10", "C11", "C14", "C17"}
    for name, fn in _CONTROLS:
        if name.split("-")[0] in preserved:
            problem = fn()
            if problem:
                return f"{name} regressed after adding void_fraction: {problem}"
    return None


def _c22_dispatch_detection() -> str | None:
    p1 = REPO_ROOT / "tests/answer-first/raw/TB-01.a1.jsonl"
    p2 = REPO_ROOT / "tests/emission-stage-a-v9.14/raw-attempt1/TB-05.jsonl"
    p3 = REPO_ROOT / "tests/emission-stage-a-v9.14/raw/TB-03.jsonl"
    if not (p1.is_file() and p2.is_file() and p3.is_file()):
        return None  # frozen evidence absent (shallow clone); not a failure
    if not dispatched(p1.read_text(encoding="utf-8")):
        return f"{p1} expected dispatched=True"
    if dispatched(p2.read_text(encoding="utf-8")):
        return f"{p2} expected dispatched=False"
    if not dispatched(p3.read_text(encoding="utf-8")):
        return f"{p3} expected dispatched=True"
    fm = final_message(p1.read_text(encoding="utf-8"))
    if len(fm) != 5420:
        return f"final_message length {len(fm)}, expected 5420"
    return None


def _c23_arm_isolation() -> str | None:
    at = argv_t("PROMPT", "claude-sonnet-5")
    ac = argv_c("PROMPT", "claude-sonnet-5")
    aj = argv_judge("claude-sonnet-5")
    if "--plugin-dir" in ac:
        return "arm C argv carries --plugin-dir"
    if "--plugin-dir" not in at or str(PLUGIN_DIR) not in at:
        return "arm T argv missing --plugin-dir <repo>/first-principles"
    if not any(isinstance(a, str) and a.startswith(ARM_T_INVOCATION) for a in at):
        return "arm T prompt does not start with ARM_T_INVOCATION"
    for argv in (at, ac, aj):
        if ISOLATION_SETTINGS not in argv:
            return "an argv is missing the isolation settings"
        if "acceptEdits" not in argv:
            return "an argv is missing acceptEdits"
        if "bypassPermissions" in argv:
            return "an argv contains bypassPermissions"
    p1 = REPO_ROOT / "tests/answer-first/raw/TB-01.a1.jsonl"
    if p1.is_file():
        jsonl = p1.read_text(encoding="utf-8")
        # The frozen capture records the absolute plugin path of the machine
        # it was taken on; a checkout elsewhere (CI) has a different
        # PLUGIN_DIR. Re-anchor the recorded path to this checkout so the
        # control tests init_check's logic, not where the repo happens to live.
        recorded = [
            p.get("path") for p in init_plugins(jsonl) if p.get("name") == "first-principles"
        ]
        if len(recorded) != 1 or not recorded[0]:
            return f"answer-first fixture lists {len(recorded)} first-principles plugin path(s)"
        jsonl = jsonl.replace(json.dumps(recorded[0])[1:-1], json.dumps(str(PLUGIN_DIR))[1:-1])
        if init_check(jsonl, "C") == []:
            return "init_check(arm='C') accepted an init event listing first-principles"
        problems_t = init_check(jsonl, "T")
        if problems_t:
            return f"init_check(arm='T') rejected the answer-first init event: {problems_t}"
        altered = jsonl.replace(str(PLUGIN_DIR), str(PLUGIN_DIR) + "-ALTERED")
        if not init_check(altered, "T"):
            return "init_check(arm='T') accepted an altered first-principles path"
    return None


def _c24_delivered_file_accepted() -> str | None:
    doc_path = REPO_ROOT / "tests/answer-first/documents/TB-01.md"
    if not doc_path.is_file():
        return None
    if extraction_problems(doc_path.read_text(encoding="utf-8"), plugin_arm=True):
        return "the delivered answer-first TB-01.md failed extraction_problems(plugin_arm=True)"
    old = REPO_ROOT / "tests/trackb-run-v9.13/generations/TB-04-T.txt"
    if old.is_file() and not extraction_problems(old.read_text(encoding="utf-8"), plugin_arm=True):
        return "a frozen v9.13 TB-04-T summary passed the plugin-arm guard"
    return None


def _c25_spent_protocol_refuses(tmp_root: Path) -> str | None:
    out_dir = tmp_root / "spent-check"
    rc = main(["--run", "--protocol", "trackb", "--out", str(out_dir)])
    if rc == 0:
        return "--run --protocol trackb (v9.13) returned 0; it must refuse"
    if out_dir.exists() and any(out_dir.rglob("*")):
        return "--run --protocol trackb produced output despite refusing"
    return None


def _c26_unchanged_is_verbatim() -> str | None:
    if not PREREG_2.is_file():
        return f"{PREREG_2} missing"
    src = _norm_quote(PREREG.read_text(encoding="utf-8"))
    doc = PREREG_2.read_text(encoding="utf-8")
    m = _UNCHANGED_HEADING_RE.search(doc)
    if not m:
        return "no '## ...Unchanged' section followed by another '##' section"
    blocks = _BLOCKQUOTE_RE.findall(m.group(1))
    if len(blocks) < 8:
        return f"too few verbatim blockquote blocks: {len(blocks)}"
    bad = [b[:80] for b in blocks if _norm_quote(b) not in src]
    if bad:
        return f"paraphrased or non-source passage(s): {bad}"
    words = _norm_quote(blocks[0]).split()
    if len(words) < 2:
        return "first block too short to mutate"
    i = len(words) // 2
    words[i] = words[i] + "zq"
    if " ".join(words) in src:
        return "anti-masking: a mutated passage still matched verbatim (comparator broken)"
    return None


def _c27_is_limit_stub_false_positive_fixed() -> str | None:
    """2026-09-30 amendment: a complete, non-error answer that happens to
    mention "rate limit" in its own prose (TB-01-C's real specimen) must
    never be misclassified as a usage-limit stub, while a genuine 429
    spend-limit stub must still be caught. Mutation leg: flipping the good
    fixture's `is_error` to true and giving it the real limit message must
    flip the verdict, so the check is not vacuously returning one constant."""
    good = json.dumps(
        {
            "type": "result",
            "is_error": False,
            "api_error_status": None,
            "result": (
                "Discussing GraphQL vs REST: one driver is reducing round trips and "
                "avoiding client-side rate limiting concerns. " + "word " * 200
            ),
        }
    )
    if is_limit_stub(good):
        return (
            "a complete non-error answer mentioning 'rate limiting' was misclassified "
            "as a usage-limit stub (the TB-01-C false-positive class)"
        )
    real_stub_path = REPO_ROOT / "tests/trackb-run-v9.15/raw/TB-06-T.a1.limit-stub.jsonl"
    if real_stub_path.is_file() and not is_limit_stub(
        real_stub_path.read_text(encoding="utf-8")
    ):
        return f"{real_stub_path} (a genuine 429 spend-limit stub) was not detected"
    mutated = json.dumps(
        {
            "type": "result",
            "is_error": True,
            "api_error_status": 429,
            "result": "You've hit your monthly spend limit",
        }
    )
    if not is_limit_stub(mutated):
        return "mutation check: an is_error=true/429 result was not detected as a stub"
    return None


_CONTROLS: tuple[tuple[str, object], ...] = (
    ("C01-rubric-format-neutral", _c01_rubric_is_format_neutral),
    ("C02-rubric-neutralises-format-and-length", _c02_rubric_declares_format_carries_no_marks),
    ("C03-judge-prompt-no-leak", _c03_judge_prompt_does_not_leak),
    ("C04-catalog-parses-balanced", _c04_catalog_parses_and_is_balanced),
    ("C05-scoreline-roundtrip", _c05_scoreline_roundtrip),
    ("C06-malformed-scorelines-rejected", _c06_malformed_scorelines_rejected),
    ("C07-permutation-calibrated", _c07_permutation_test_is_calibrated),
    ("C08-drift-blocks-noise-sized-effect", _c08_drift_threshold_blocks_a_noise_sized_effect),
    ("C09-no-drift-arm-cannot-clear", _c09_missing_drift_arm_cannot_clear),
    ("C10-real-effect-does-clear", _c10_a_real_effect_does_clear),
    ("C11-broken-mechanics-inconclusive", _c11_broken_mechanics_is_inconclusive_not_null),
    ("C12-extraction-integrity", _c12_extraction_integrity_detects_both_faults),
    ("C13-prereg-code-agree", _c13_prereg_and_code_constants_agree),
    ("C14-status-vocabulary", _c14_status_vocabulary_matches_the_card),
    ("C15-transport-bg-wait-fix", _c15_transport_carries_the_bg_wait_fix),
    ("C16-delegation-stub-rejected", _c16_a_delegation_stub_would_be_rejected),
    ("C17-status-is-derived-not-asserted", _c17_status_cannot_be_asserted_by_a_caller),
    ("C18-plugin-arm-rejects-orchestrator-summary", _c18_plugin_arm_rejects_an_orchestrator_summary),
    ("C19-frozen-arm-t-captures-would-void", _c19_the_frozen_arm_t_captures_would_now_void),
    ("C20-prereg2-code-agree", _c20_prereg2_code_agree),
    ("C21-void-cap", _c21_void_cap_blocks_and_default_preserves_old_controls),
    ("C22-dispatch-detection", _c22_dispatch_detection),
    ("C23-arm-isolation", _c23_arm_isolation),
    ("C24-delivered-file-accepted", _c24_delivered_file_accepted),
    ("C25-spent-protocol-refuses", _c25_spent_protocol_refuses),
    ("C26-unchanged-is-verbatim", _c26_unchanged_is_verbatim),
    ("C27-limit-stub-false-positive-fixed", _c27_is_limit_stub_false_positive_fixed),
)


def self_test() -> int:
    import inspect
    import tempfile

    failures: list[str] = []
    with tempfile.TemporaryDirectory(prefix="trackb-self-test-") as td:
        tmp_root = Path(td)
        for name, fn in _CONTROLS:
            try:
                sig = inspect.signature(fn)  # type: ignore[arg-type]
                problem = fn(tmp_root) if sig.parameters else fn()  # type: ignore[operator]
            except Exception as exc:  # noqa: BLE001
                problem = f"raised {type(exc).__name__}: {exc}"
            if problem:
                failures.append(f"{name}: {problem}")
    if failures:
        for f in failures:
            sys.stderr.write(f"[trackb self-test] FAIL {f}\n")
        sys.stderr.write(
            f"[trackb self-test] {len(failures)} of {len(_CONTROLS)} controls failed\n"
        )
        return 1
    print(f"trackb self-test: {len(_CONTROLS)}/{len(_CONTROLS)} controls passed")
    return 0


def describe() -> dict:
    return {
        "registered_surfaces": [
            "docs/trackb-preregistration.md",
            "docs/trackb-neutral-rubric.md",
            "tests/trackb-catalog-v9.13.md",
            "docs/trackb-2-preregistration.md",
        ],
        "control_ids": sorted(c[0] for c in _CONTROLS),
        "control_count": len(_CONTROLS),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Track B comparative harness.")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--plan", action="store_true", help="print the run plan; no spend")
    parser.add_argument("--describe", action="store_true")
    parser.add_argument("--run", action="store_true", help="execute the registered run")
    parser.add_argument("--probe", action="store_true", help="trackb-2 pre-run mechanics probe")
    parser.add_argument(
        "--recompute", action="store_true", help="recompute trackb-2 from frozen captures"
    )
    parser.add_argument("--protocol", choices=("trackb", "trackb-2"), default="trackb")
    parser.add_argument("--out", type=Path, help="capture directory")
    parser.add_argument(
        "--scratch", type=Path, help="scratch root for trackb-2 live cells (outside the repo)"
    )
    parser.add_argument("--model", default="claude-sonnet-5", help="pinned model")
    args = parser.parse_args(argv)

    try:
        if args.describe:
            print(json.dumps(describe(), indent=2, sort_keys=True))
            return 0
        if args.self_test:
            return self_test()
        if args.plan:
            return cmd_plan_2() if args.protocol == "trackb-2" else cmd_plan()
        if args.run:
            if not args.out:
                sys.stderr.write("[trackb] --run requires --out DIR\n")
                return 1
            if args.protocol == "trackb":
                sys.stderr.write(
                    "[trackb] --run under protocol 'trackb' (v9.13) is spent; superseded by "
                    "docs/trackb-2-preregistration.md -- refusing to run\n"
                )
                return 1
            if not args.scratch:
                sys.stderr.write("[trackb] --run --protocol trackb-2 requires --scratch DIR\n")
                return 1
            return cmd_run_2(args.out, args.scratch, args.model)
        if args.probe:
            if args.protocol != "trackb-2":
                sys.stderr.write("[trackb] --probe is only defined for --protocol trackb-2\n")
                return 1
            if not args.out or not args.scratch:
                sys.stderr.write("[trackb] --probe requires --out DIR and --scratch DIR\n")
                return 1
            return cmd_probe_2(args.out, args.scratch, args.model)
        if args.recompute:
            if args.protocol != "trackb-2":
                sys.stderr.write("[trackb] --recompute is only defined for --protocol trackb-2\n")
                return 1
            if not args.out:
                sys.stderr.write("[trackb] --recompute requires --out DIR\n")
                return 1
            return cmd_recompute_2(args.out)
        parser.print_help()
        return 0
    except TrackBError as exc:
        sys.stderr.write(f"[trackb] {exc}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
