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
from dataclasses import dataclass, asdict
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


def extraction_problems(doc_text: str, min_words: int = 120) -> list[str]:
    """Void-the-cell checks applied BEFORE a document reaches a judge.

    This harness family has twice nearly fabricated a decisive result through
    extraction faults -- once by paraphrasing an analysis down to ~15% of itself,
    once by concatenating the rubric onto an arm's output. Both would have
    produced confident, false verdicts, in OPPOSITE directions.
    """
    problems: list[str] = []
    for marker in _RUBRIC_CONTAMINATION_MARKERS:
        if marker in doc_text:
            problems.append(f"rubric contamination: capture contains {marker!r}")
    words = len(doc_text.split())
    if words < min_words:
        problems.append(f"implausibly short capture: {words} words < {min_words}")
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
) -> dict:
    """Apply the pre-registered threshold. Returns the result record.

    `per_prompt` maps prompt_id -> {"domain": str, "T": float, "C": float}.

    There is deliberately no argument by which a caller can assert a status: it
    is computed here from the recorded numbers, and `cmd_run` writes whatever
    this returns. That is what makes "publish only if non-null" a protocol rather
    than a preference.
    """
    prompt_ids = sorted(per_prompt)
    diffs = [per_prompt[p]["T"] - per_prompt[p]["C"] for p in prompt_ids]
    mean_diff = statistics.fmean(diffs) if diffs else 0.0

    # Mechanics first: a broken run is inconclusive, never null.
    if dispatch_failures or unparseable_fraction > MAX_UNPARSEABLE_FRACTION:
        return {
            "status": "inconclusive",
            "reason": (
                f"run mechanics failed: {dispatch_failures} dispatch failure(s), "
                f"{unparseable_fraction:.1%} unparseable (cap "
                f"{MAX_UNPARSEABLE_FRACTION:.0%})"
            ),
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
        argv, capture_output=True, text=True, timeout=5400, env=env
    )
    out_path.write_text(proc.stdout + proc.stderr, encoding="utf-8")
    return out_path


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
    print(f"  arms                 : 2 (T=plugin, C=unaided)")
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
        argv, capture_output=True, text=True, timeout=1800, cwd=packet, env=env
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
            probs = extraction_problems(text)
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


def _write_result(record: dict, extra: dict) -> None:
    payload = {**record, **extra}
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


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
)


def self_test() -> int:
    failures: list[str] = []
    for name, fn in _CONTROLS:
        try:
            problem = fn()  # type: ignore[operator]
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
    parser.add_argument("--out", type=Path, help="capture directory for --run")
    parser.add_argument("--model", default="claude-sonnet-5", help="pinned model")
    args = parser.parse_args(argv)

    try:
        if args.describe:
            print(json.dumps(describe(), indent=2, sort_keys=True))
            return 0
        if args.self_test:
            return self_test()
        if args.plan:
            return cmd_plan()
        if args.run:
            if not args.out:
                sys.stderr.write("[trackb] --run requires --out DIR\n")
                return 1
            return cmd_run(args.out, args.model)
        parser.print_help()
        return 0
    except TrackBError as exc:
        sys.stderr.write(f"[trackb] {exc}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
