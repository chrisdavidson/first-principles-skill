#!/usr/bin/env python3
"""audit-first -- the measurement pre-registered in docs/audit-first-preregistration.md.

    python3 tests/audit-first/run_audit.py run --bodies <dir> --work <dir> [--workers 2] [--stage 1|2]
    python3 tests/audit-first/run_audit.py read
    python3 tests/audit-first/run_audit.py --self-test

<bodies>/N/first-principles is the arm tree, exported with `git archive`. Resumable: a run
already recorded in cells.json is not re-run. The outcome is read with the unedited
tests/skip-rate/phase_turns.py. A measurement tool, never a gate.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from math import comb
from pathlib import Path
from statistics import mean, median

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
RAW = HERE / "raw"
CELLS = HERE / "cells.json"
VERDICT = HERE / "verdict.json"
READINGS = HERE / "readings.json"
PROMPTS_FILE = REPO_ROOT / "tests" / "example-rerun-2" / "prompts.json"

# --- pre-registered protocol --------------------------------------------------------------
MODEL = "claude-sonnet-5"
ARMS = ("N",)
REPEATS = (1, 2)
MAX_ATTEMPTS = 3  # first try + two routing-miss retries
AGENT_TYPE = "first-principles:first-principles"
LIMIT_PAUSE_S = 1800
P0 = 34 / 87  # baseline share of assembled runs with six or more rewrites, treated as exact
ALPHA = 0.05
REWRITE_HEAVY = 6  # "six or more rewrites"
MIN_ASSEMBLED = 18  # fewer than this after both stages is uninformative
FUTILITY_K = 5  # stage 1: this many heavy-rewrite assembled runs stops the measurement
SECONDARY_MEDIAN = 2
ASSEMBLY_RATE_MIN = 0.90
GATE_TURN_MAX = 28
TURNS_MEDIAN_MAX = 43
TURN_CEILING = 90
# ------------------------------------------------------------------------------------------

_spec = importlib.util.spec_from_file_location("phase_turns", REPO_ROOT / "tests" / "skip-rate" / "phase_turns.py")
pt = importlib.util.module_from_spec(_spec)
sys.modules["phase_turns"] = pt
_spec.loader.exec_module(pt)

_lock = threading.Lock()
_SECTION_RE = re.compile(r"^s[1-6]$")


def sib(base: Path, suffix: str) -> Path:
    """A sibling path by string concatenation. `Path.with_suffix` would replace the attempt
    marker (`.a1`) because the key itself contains dots."""
    return base.with_name(base.name + suffix)


def schedule(prompts: list[str], stage: int | None = None) -> list[tuple[str, str, int]]:
    """Stage 1 = every prompt at repeat 1, stage 2 = every prompt at repeat 2."""
    reps = REPEATS if stage is None else (REPEATS[stage - 1],)
    return [(arm, pid, r) for r in reps for pid in prompts for arm in ARMS]


def events(text: str):
    for line in text.splitlines():
        try:
            yield json.loads(line)
        except ValueError:
            continue


def init_event(text: str) -> dict:
    return next((o for o in events(text) if o.get("type") == "system" and o.get("subtype") == "init"), {})


def result_events(text: str) -> list[dict]:
    """Every `result` event, in order."""
    return [o for o in events(text) if o.get("type") == "result"]


def result_event(text: str) -> dict:
    last = {}
    for o in events(text):
        if o.get("type") == "result":
            last = o
    return last


def agent_minutes(agent_dir: Path) -> float | None:
    """Wall-clock minutes of the first-principles agent, first to last transcript timestamp."""
    from datetime import datetime

    stamps = []
    for f in sorted(agent_dir.glob("agent-*.jsonl")):
        for o in events(f.read_text(encoding="utf-8", errors="replace")):
            t = o.get("timestamp")
            if t:
                stamps.append(datetime.fromisoformat(t))
    return round((max(stamps) - min(stamps)).total_seconds() / 60, 1) if stamps else None


def dispatched(text: str) -> bool:
    for o in events(text):
        if o.get("type") != "assistant" or o.get("parent_tool_use_id"):
            continue
        for b in o.get("message", {}).get("content", []) or []:
            if (
                isinstance(b, dict)
                and b.get("type") == "tool_use"
                and b.get("name") in ("Agent", "Task")
                and (b.get("input") or {}).get("subagent_type") == AGENT_TYPE
            ):
                return True
    return False


def is_limit_stub(text: str) -> bool:
    res = result_event(text)
    if res.get("api_error_status") == 429:
        return True
    if res.get("is_error") and not dispatched(text):
        return True
    return not res and "limit" in text[-4000:].lower() and not dispatched(text)


def capture_agent(text: str, dest: Path) -> list[Path]:
    init = init_event(text)
    sid, cwd = init.get("session_id"), init.get("cwd")
    if not (sid and cwd):
        return []
    key = cwd.replace("/", "-").replace(".", "-")
    src = Path.home() / ".claude" / "projects" / key / sid / "subagents"
    out = []
    if src.is_dir():
        dest.mkdir(parents=True, exist_ok=True)
        for f in sorted(src.iterdir()):
            shutil.copy2(f, dest / f.name)
            if f.suffix == ".jsonl":
                out.append(dest / f.name)
    return out


def agent_tool_calls(agent_dir: Path) -> list[tuple[str, dict]]:
    """The first-principles agent's own tool calls, in order."""
    files = []
    for meta in sorted(agent_dir.glob("agent-*.meta.json")):
        try:
            m = json.loads(meta.read_text())
        except ValueError:
            continue
        if AGENT_TYPE in json.dumps(m) or m.get("agentType") == "first-principles":
            files.append(meta.with_name(meta.name.replace(".meta.json", ".jsonl")))
    if not files:
        files = sorted(agent_dir.glob("agent-*.jsonl"))
    calls = []
    for f in files:
        if not f.is_file():
            continue
        for o in events(f.read_text(encoding="utf-8", errors="replace")):
            if o.get("type") != "assistant":
                continue
            for b in o.get("message", {}).get("content", []) or []:
                if isinstance(b, dict) and b.get("type") == "tool_use":
                    calls.append((b.get("name"), b.get("input") or {}))
    return calls


def delivery(files_dir: Path) -> tuple[bool, str]:
    """(delivered, state) from the files on disk."""
    analyses = sorted(files_dir.glob("analysis-*.md")) if files_dir.is_dir() else []
    analyses = [a for a in analyses if a.name.count(".") == 1]  # not .process/.answer
    if not analyses:
        return False, "no-file"
    for a in reversed(analyses):
        first = next((ln.rstrip("\n") for ln in a.open(errors="replace") if ln.startswith("## ")), None)
        report = a.with_name(a.name.replace("analysis-", "report-", 1))
        if first == "## Answer" and report.is_file():
            return True, "delivered"
    return False, "partial"


def skip_mode(calls: list[tuple[str, dict]], state: str) -> str:
    if state == "partial":
        return "partial"
    if not calls:
        return "zero-tool"
    if calls[0][0] == "Skill":
        return "skill-first"
    return "no-file"


# --- reading: the outcome measure ---------------------------------------------------------


def critical(n: int, p0: float = P0, alpha: float = ALPHA) -> int | None:
    """Largest k with P(X <= k) <= alpha for X ~ Binomial(n, p0); None if even k = 0 exceeds it."""
    best, cum = None, 0.0
    for k in range(n + 1):
        cum += comb(n, k) * p0**k * (1 - p0) ** (n - k)
        if cum <= alpha:
            best = k
        else:
            break
    return best


def bash_cmds(agent_dir: Path) -> list[tuple[int, str]]:
    """(turn, command) for every Bash call, walking assistant messages exactly as
    phase_turns.read_run does: a turn is one distinct assistant message id."""
    out: list[tuple[int, str]] = []
    ids: list[str] = []
    for f in sorted(agent_dir.glob("agent-*.jsonl")):
        for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                o = json.loads(line)
            except ValueError:
                continue
            if o.get("type") != "assistant":
                continue
            msg = o.get("message") or {}
            mid = msg.get("id") or f"{f.name}:{len(ids)}"
            if mid not in ids:
                ids.append(mid)
            for b in msg.get("content") or []:
                if isinstance(b, dict) and b.get("type") == "tool_use" and b.get("name") == "Bash":
                    out.append((len(ids), (b.get("input") or {}).get("command", "")))
    return out


def rewrite_turns(cmds: list[tuple[int, str]]) -> list[int]:
    return [t for t, c in cmds if pt.is_rewrite(c)]


def turn_rewrites(agent_dir: Path) -> list[int]:
    """Turn indices at which the unedited is_rewrite is true."""
    return rewrite_turns(bash_cmds(agent_dir))


def dup_sections(cmds: list[tuple[int, str]]) -> int:
    """Heredoc commands that write a section (s1..s6) already written earlier in the run."""
    seen: set[str] = set()
    dup = 0
    for _, c in cmds:
        for h in pt.classify(c):
            if _SECTION_RE.match(h):
                if h in seen:
                    dup += 1
                seen.add(h)
    return dup


def dup_section_writes(agent_dir: Path) -> int:
    return dup_sections(bash_cmds(agent_dir))


def held_append(cmds: list[tuple[int, str]]) -> int | None:
    """Turn of the first command that appends the held .s2, .s3 and .s4 sidecars with `>>`."""
    for t, c in cmds:
        if ">>" in c and all(s in c for s in (".s2", ".s3", ".s4")):
            return t
    return None


def held_append_turn(agent_dir: Path) -> int | None:
    return held_append(bash_cmds(agent_dir))


def gate_turn(cmds: list[tuple[int, str]]) -> int | None:
    for t, c in cmds:
        if "gate" in pt.classify(c):
            return t
    return None


def split_rewrites(cmds: list[tuple[int, str]]) -> dict[str, int]:
    """Rewrites before the held append, after it but before the first gate append, after the gate.
    With no held append, every pre-gate rewrite is counted before it."""
    held, gate = held_append(cmds), gate_turn(cmds)
    out = {"pre_held": 0, "post_held_pre_gate": 0, "post_gate": 0}
    for t in rewrite_turns(cmds):
        if gate is not None and t >= gate:
            out["post_gate"] += 1
        elif held is None or t < held:
            out["pre_held"] += 1
        else:
            out["post_held_pre_gate"] += 1
    return out


def leftover_sidecars(files_dir: Path) -> list[str]:
    if not files_dir.is_dir():
        return []
    pats = ("*.s2", "*.s3", "*.s4", "*.draft")
    return sorted({str(p.relative_to(files_dir)) for pat in pats for p in files_dir.rglob(pat)})


def missing_sections(files_dir: Path) -> list[int]:
    """Section numbers 1..6 whose `## N. ` heading is absent from the delivered analysis."""
    analyses = sorted(files_dir.glob("analysis-*.md")) if files_dir.is_dir() else []
    analyses = [a for a in analyses if a.name.count(".") == 1]
    if not analyses:
        return list(range(1, 7))
    text = analyses[-1].read_text(encoding="utf-8", errors="replace")
    return [n for n in range(1, 7) if not re.search(rf"^## {n}\. ", text, re.MULTILINE)]


def baseline_dirs() -> list[Path]:
    out = []
    for rel, tag in pt.CORPORA.values():
        for agent_dir in sorted((REPO_ROOT / rel).glob("*.agent")):
            if tag and tag not in agent_dir.name and not agent_dir.name.startswith(tag):
                continue
            if pt.read_run(agent_dir):
                out.append(agent_dir)
    return out


def baseline() -> dict:
    rows = list(pt.runs())
    asm = [r for r in rows if "assemble" in r["first"]]
    gates = [r["first"]["gate"] for r in asm if "gate" in r["first"]]
    return {
        "runs": len(rows),
        "assembled": len(asm),
        "k_ge6": sum(r["rewrites"] >= REWRITE_HEAVY for r in asm),
        "median_rewrites": median(r["rewrites"] for r in asm),
        "median_gate_turn": median(gates),
        "median_turns": median(r["turns"] for r in asm),
        "over_60": sum(r["turns"] > 60 for r in asm),
        "max_turns": max(r["turns"] for r in rows),
    }


# --- the verdict --------------------------------------------------------------------------


def futility(asm_stage1: list[dict]) -> str:
    return "STOP" if sum(r["rewrites"] >= REWRITE_HEAVY for r in asm_stage1) >= FUTILITY_K else "CONTINUE"


def no_regression(n_dispatched: int, asm: list[dict]) -> dict:
    gates = [r["gate_turn"] for r in asm if r.get("gate_turn") is not None]
    rate = len(asm) / n_dispatched if n_dispatched else 0.0
    med_gate = median(gates) if gates else None
    med_turns = median(r["turns"] for r in asm) if asm else None
    incomplete = sum(1 for r in asm if not r["complete"])
    conds = {
        "assembly_rate": rate >= ASSEMBLY_RATE_MIN,
        "median_gate_turn": med_gate is not None and med_gate <= GATE_TURN_MAX,
        "median_turns": med_turns is not None and med_turns <= TURNS_MEDIAN_MAX,
        "max_turns": all(r["turns"] < TURN_CEILING for r in asm),
        "complete": incomplete == 0,
    }
    return {"conditions": conds, "ok": all(conds.values()), "rate": rate, "incomplete": incomplete}


def decide(
    n_dispatched: int,
    asm: list[dict],
    *,
    stage_complete: bool,
    stage2_started: bool,
    stage1_complete: bool,
    asm_stage1: list[dict],
) -> dict:
    n = len(asm)
    k = sum(r["rewrites"] >= REWRITE_HEAVY for r in asm)
    crit = critical(n) if n else None
    med_rw = median(r["rewrites"] for r in asm) if asm else None
    primary = crit is not None and k <= crit
    secondary = med_rw is not None and med_rw <= SECONDARY_MEDIAN
    nr = no_regression(n_dispatched, asm)
    fut = futility(asm_stage1) if (stage1_complete and not stage2_started) else None
    gates = [r["gate_turn"] for r in asm if r.get("gate_turn") is not None]
    if not stage_complete:
        verdict = "futility-stop" if fut == "STOP" else "in-progress"
    elif n < MIN_ASSEMBLED:
        verdict = "uninformative"
    elif primary and secondary and nr["ok"]:
        verdict = "shown-effective"
    else:
        verdict = "not-shown-effective"
    return {
        "stage_complete": stage_complete,
        "dispatched": n_dispatched,
        "assembled": n,
        "k_ge6": k,
        "critical": crit,
        "primary": primary,
        "median_rewrites": med_rw,
        "secondary": secondary,
        "assembly_rate": nr["rate"],
        "median_gate_turn": median(gates) if gates else None,
        "median_turns": median(r["turns"] for r in asm) if asm else None,
        "max_turns": max((r["turns"] for r in asm), default=None),
        "incomplete_runs": nr["incomplete"],
        "no_regression": nr["ok"],
        "no_regression_conditions": nr["conditions"],
        "futility": fut,
        "verdict": verdict,
    }


# --- scoring one captured run -------------------------------------------------------------


def score(key: str, cell: dict) -> dict:
    base = RAW / cell["scored"]
    text = sib(base, ".jsonl").read_text(encoding="utf-8", errors="replace")
    files_dir, agent_dir = sib(base, ".files"), sib(base, ".agent")
    delivered, state = delivery(files_dir)
    calls = agent_tool_calls(agent_dir)
    run = pt.read_run(agent_dir)
    cmds = bash_cmds(agent_dir)
    results = result_events(text)
    assembled = bool(run and "assemble" in run["first"])
    left = leftover_sidecars(files_dir)
    miss = missing_sections(files_dir)
    return {
        "key": key,
        "prompt": cell["prompt"],
        "repeat": cell["repeat"],
        "delivered": delivered,
        "state": state,
        "mode": None if delivered else skip_mode(calls, state),
        "assembled": assembled,
        "turns": run["turns"] if run else 0,
        "rewrites": run["rewrites"] if run else 0,
        "rewrite_split": split_rewrites(cmds),
        "dup_section_writes": dup_sections(cmds),
        "gate_turn": run["first"].get("gate") if run else None,
        "held_append_turn": held_append(cmds),
        "leftover_sidecars": left,
        "missing_sections": miss,
        "complete": not left and not miss,
        "cost_usd": max((r.get("total_cost_usd") or 0 for r in results), default=0),
        "agent_min": agent_minutes(agent_dir),
        "attempts": len(cell["attempts"]),
    }


# --- running ------------------------------------------------------------------------------


def generate(text: str, body: Path, cwd: Path, base: Path) -> str:
    argv = [
        "claude", "-p", "--model", MODEL, "--plugin-dir", str(body),
        "--output-format", "stream-json", "--verbose",
        "--permission-mode", "bypassPermissions", text,
    ]  # fmt: skip
    env = {**os.environ, "CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS": "0",
           "FP_GUARD_LOG": str(sib(base, ".guard.jsonl"))}  # fmt: skip
    proc = subprocess.run(argv, capture_output=True, text=True, timeout=5400, env=env, cwd=cwd, check=False)
    sib(base, ".jsonl").write_text(proc.stdout, encoding="utf-8")
    if proc.stderr.strip():
        sib(base, ".stderr").write_text(proc.stderr, encoding="utf-8")
    return proc.stdout


def run_one(arm: str, pid: str, r: int, prompt: str, bodies: Path, work: Path) -> None:
    key = f"{arm}.{pid}.r{r}"
    body = (bodies / arm / "first-principles").resolve()
    attempts, outcome, n = [], "exhausted", 0
    while n < MAX_ATTEMPTS:
        n += 1
        cwd = work / f"{key}.a{n}"
        shutil.rmtree(cwd, ignore_errors=True)
        cwd.mkdir(parents=True)
        base = RAW / f"{key}.a{n}"
        sib(base, ".guard.jsonl").unlink(missing_ok=True)
        print(f"[run] {key} attempt {n} ...", flush=True)
        text = generate(prompt, body, cwd, base)
        if is_limit_stub(text):
            for suf in (".jsonl", ".guard.jsonl", ".stderr"):
                p = sib(base, suf)
                if p.exists():
                    p.rename(RAW / f"{key}.a{n}.limit-stub{suf}")
            print(f"[pause] {key}: usage-limit stub; sleeping {LIMIT_PAUSE_S}s", flush=True)
            time.sleep(LIMIT_PAUSE_S)
            n -= 1
            continue
        plugins = [p.get("path") for p in init_event(text).get("plugins") or [] if p.get("name") == "first-principles"]
        if plugins != [str(body)]:
            raise SystemExit(f"[abort] {key}: loaded {plugins}, expected {body}")
        capture_agent(text, sib(base, ".agent"))
        src = cwd / ".first-principles"
        if src.is_dir():
            shutil.copytree(src, sib(base, ".files"), dirs_exist_ok=True)
        shutil.rmtree(cwd, ignore_errors=True)
        attempts.append(base.name)
        if dispatched(text):
            outcome = "scored"
            break
        print(f"[miss] {key} attempt {n}", flush=True)
    with _lock:
        cells = json.loads(CELLS.read_text()) if CELLS.is_file() else {}
        cells[key] = {
            "arm": arm, "prompt": pid, "repeat": r, "outcome": outcome,
            "attempts": attempts, "scored": attempts[-1] if outcome == "scored" else None,
        }  # fmt: skip
        CELLS.write_text(json.dumps(cells, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        if outcome == "scored":
            s = score(key, cells[key])
            print(
                f"[done] {key} {'DELIVERED' if s['delivered'] else 'SKIP:' + str(s['mode'])} "
                f"assembled={s['assembled']} turns={s['turns']} rewrites={s['rewrites']} "
                f"agent_min={s['agent_min']}",
                flush=True,
            )
        else:
            print(f"[done] {key} EXHAUSTED", flush=True)


def _run_stage(prompts: dict, stage: int, bodies: Path, work: Path, workers: int) -> None:
    done = json.loads(CELLS.read_text()) if CELLS.is_file() else {}
    todo = [(a, p, r) for a, p, r in schedule(list(prompts), stage) if f"{a}.{p}.r{r}" not in done]
    print(f"[plan] stage {stage}: {len(todo)} runs to go, {workers} at a time", flush=True)
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = [ex.submit(run_one, a, p, r, prompts[p], bodies, work) for a, p, r in todo]
        for f in futures:
            f.result()


def cmd_run(bodies: Path, work: Path, workers: int, stage: int | None) -> int:
    prompts = json.loads(PROMPTS_FILE.read_text())
    for arm in ARMS:
        if not (bodies / arm / "first-principles" / "agents" / "first-principles.md").is_file():
            raise SystemExit(f"missing body for arm {arm} under {bodies}")
    RAW.mkdir(parents=True, exist_ok=True)
    stages = (1, 2) if stage is None else (stage,)
    for st in stages:
        _run_stage(prompts, st, bodies, work, workers)
        if st == 1 and stage is None:
            v = build_verdict(write=False)
            if v and v["futility"] == "STOP":
                print("[futility] stage 1 hit the futility stop; stage 2 is not run", flush=True)
                break
    return cmd_read()


# --- read ---------------------------------------------------------------------------------


def build_verdict(write: bool = True, echo: bool = False) -> dict | None:
    cells = json.loads(CELLS.read_text()) if CELLS.is_file() else {}
    if not cells:
        return None
    n_prompts = len(json.loads(PROMPTS_FILE.read_text()))
    rows = [score(k, c) for k, c in sorted(cells.items()) if c["outcome"] == "scored"]
    exhausted = sorted(k for k, c in cells.items() if c["outcome"] != "scored")
    asm = [r for r in rows if r["assembled"]]
    stage1 = {k for k in cells if k.endswith(".r1")}
    stage2_started = any(k.endswith(".r2") for k in cells)
    v = decide(
        len(rows),
        asm,
        stage_complete=len(cells) >= n_prompts * len(REPEATS) * len(ARMS),
        stage2_started=stage2_started,
        stage1_complete=len(stage1) >= n_prompts * len(ARMS),
        asm_stage1=[r for r in asm if r["repeat"] == 1],
    )
    if echo:
        for r in rows:
            sp = r["rewrite_split"]
            print(
                f"{r['key']}: delivered={r['delivered']} assembled={r['assembled']} turns={r['turns']} "
                f"rewrites={r['rewrites']} (pre-held {sp['pre_held']}, held-to-gate {sp['post_held_pre_gate']}, "
                f"post-gate {sp['post_gate']}) dup-section-writes={r['dup_section_writes']} "
                f"gate-turn={r['gate_turn']} leftover={r['leftover_sidecars']} "
                f"missing={r['missing_sections']} cost=${r['cost_usd']:.2f} agent-min={r['agent_min']}"
            )
        if exhausted:
            print(f"exhausted (routing misses, excluded): {exhausted}")
        if asm:
            print(
                f"reported: mean rewrites {mean(r['rewrites'] for r in asm):.2f}; "
                f"duplicate-section writes {sum(r['dup_section_writes'] for r in asm)}; "
                f"cost ${sum(r['cost_usd'] for r in rows):.2f}; "
                f"agent minutes {sum(r['agent_min'] or 0 for r in rows):.1f}"
            )
        print("\nverdict:")
        for k, val in v.items():
            print(f"  {k}: {val}")
    if write:
        READINGS.write_text(json.dumps(rows, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        VERDICT.write_text(json.dumps(v, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return v


def cmd_read() -> int:
    if build_verdict(write=True, echo=True) is None:
        print("audit-first: no cells recorded yet")
    return 0


# --- self-test ----------------------------------------------------------------------------

_REWRITE_CMD = "sed -i 's/a/b/' analysis-X.md"
_APPEND = "cat >> \"$F\" <<'FP_EOF'\n{}\nFP_EOF"
_EXPECTED_CRIT = {12: 1, 13: 1, 14: 2, 15: 2, 16: 2, 17: 2, 18: 3, 19: 3, 20: 3, 21: 4, 22: 4,
                  23: 4, 24: 5, 25: 5, 26: 5, 27: 5, 28: 6}  # fmt: skip


def _row(rewrites=0, turns=40, gate=25, complete=True, repeat=1):
    return {"rewrites": rewrites, "turns": turns, "gate_turn": gate, "complete": complete, "repeat": repeat}


def _decide(rows, dispatched_n=None, **kw):
    kw.setdefault("stage_complete", True)
    kw.setdefault("stage2_started", True)
    kw.setdefault("stage1_complete", True)
    kw.setdefault("asm_stage1", [])
    return decide(len(rows) if dispatched_n is None else dispatched_n, rows, **kw)


def self_test() -> int:
    ok = True

    def check(label, cond):
        nonlocal ok
        print(f"audit-first --self-test: {label} {'PASS' if cond else 'FAIL'}")
        ok &= bool(cond)

    # baseline, from the unedited instrument
    b = baseline()
    check("baseline 99 runs, 87 assembled", b["runs"] == 99 and b["assembled"] == 87)
    check("baseline 34 of 87 with >= 6 rewrites", b["k_ge6"] == 34)
    check("baseline median rewrites 4, median gate turn 28", b["median_rewrites"] == 4 and b["median_gate_turn"] == 28)
    check("baseline median total turns 43", b["median_turns"] == 43)
    check("baseline 14 assembled runs over 60 turns, none over 90", b["over_60"] == 14 and b["max_turns"] < TURN_CEILING)
    check("critical table n=12..28", all(critical(n) == k for n, k in _EXPECTED_CRIT.items()))

    # verdict rules on synthetic runs
    def with_heavy(n, k):
        return [_row(rewrites=REWRITE_HEAVY if i < k else 0) for i in range(n)]

    v = _decide(with_heavy(26, 5))
    check("n=26 k=5 primary PASS", v["primary"] and v["verdict"] == "shown-effective")
    v = _decide(with_heavy(26, 6))
    check("n=26 k=6 primary FAIL", not v["primary"] and v["verdict"] == "not-shown-effective")
    check("n=17 uninformative", _decide(with_heavy(17, 0))["verdict"] == "uninformative")
    check("futility 5 of 13 STOP", futility(with_heavy(13, 5)) == "STOP")
    check("futility 4 of 13 CONTINUE", futility(with_heavy(13, 4)) == "CONTINUE")
    v = _decide(with_heavy(13, 5), stage_complete=False, stage2_started=False, asm_stage1=with_heavy(13, 5))
    check("stage-1 futility STOP gives futility-stop", v["verdict"] == "futility-stop")
    v = _decide(with_heavy(13, 4), stage_complete=False, stage2_started=False, asm_stage1=with_heavy(13, 4))
    check("stage-1 futility CONTINUE gives in-progress", v["verdict"] == "in-progress")
    check("secondary median 2 passes", _decide([_row(2)] * 26)["secondary"])
    check("secondary median 3 fails", not _decide([_row(3)] * 26)["secondary"])
    check("median total turns 43 passes", _decide([_row(2, turns=43)] * 26)["no_regression"])
    check("median total turns 44 fails", not _decide([_row(2, turns=44)] * 26)["no_regression"])
    check("a run at 90 turns fails no-regression",
          not _decide([_row(2, turns=40)] * 25 + [_row(2, turns=90)])["no_regression"])  # fmt: skip
    check("median gate turn 29 fails no-regression", not _decide([_row(2, gate=29)] * 26)["no_regression"])
    check("assembly rate under 90% fails no-regression", not _decide([_row(2)] * 26, dispatched_n=30)["no_regression"])
    check("one incomplete assembled run fails no-regression",
          not _decide([_row(2)] * 25 + [_row(2, complete=False)])["no_regression"])  # fmt: skip

    # completeness on disk
    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        good = d / "good"
        good.mkdir()
        (good / "analysis-X.md").write_text("".join(f"## {n}. Title\n\nbody\n" for n in range(1, 7)))
        check("complete delivered analysis, no sidecar", not leftover_sidecars(good) and not missing_sections(good))
        side = d / "side"
        side.mkdir()
        (side / "analysis-X.md").write_text((good / "analysis-X.md").read_text())
        (side / "analysis-X.md.s3").write_text("held\n")
        check("leftover .s3 sidecar detected", leftover_sidecars(side) == ["analysis-X.md.s3"])
        short = d / "short"
        short.mkdir()
        (short / "analysis-X.md").write_text("".join(f"## {n}. Title\n" for n in (1, 2, 3, 5, 6)))
        check("missing `## 4. ` heading detected", missing_sections(short) == [4])
        check("completeness feeds no-regression",
              not no_regression(2, [_row(complete=not leftover_sidecars(side)) | {"turns": 40}] * 2)["ok"])  # fmt: skip

    # post-held-append rewrites
    cmds = [
        (18, _REWRITE_CMD),
        (20, "cat F.s2 F.s3 F.s4 >> \"$F\""),
        (25, _REWRITE_CMD),
        (35, _APPEND.format("## Self-Audit Gate")),
        (40, _REWRITE_CMD),
    ]
    sp = split_rewrites(cmds)
    check("held append at turn 20 found", held_append(cmds) == 20 and gate_turn(cmds) == 35)
    check("rewrite split pre-held 1, held-to-gate 1, post-gate 1",
          (sp["pre_held"], sp["post_held_pre_gate"], sp["post_gate"]) == (1, 1, 1))  # fmt: skip

    # duplicate-section writes
    once = [(i, _APPEND.format(f"## {i}. T")) for i in range(1, 7)]
    check("one write per section: 0 duplicates", dup_sections(once) == 0)
    twice = once + [(9, "cat > \"$F.p\" <<'FP_EOF'\n## 4. T again\nFP_EOF")]
    check("`## 4. ` heredoc twice: 1 duplicate", dup_sections(twice) == 1)

    # the walker counts with the unedited is_rewrite, run by run
    dirs = baseline_dirs()
    same = all(len(turn_rewrites(d)) == pt.read_run(d)["rewrites"] for d in dirs)
    check(f"per-turn rewrite walker equals read_run on all {len(dirs)} baseline runs", same and len(dirs) == 99)

    # copied delivery fixtures
    fg = REPO_ROOT / "tests" / "delivery-guard" / "raw"
    if fg.is_dir():
        d, s = delivery(fg / "forced-skip.files")
        check("forced-skip capture delivered", d and s == "delivered")
        txt = (fg / "forced-skip.jsonl").read_text()
        check("forced-skip dispatched", dispatched(txt) and not is_limit_stub(txt))
        am = agent_minutes(fg / "forced-skip.agent")
        check("agent minutes read from the transcript, > 5", am is not None and am > 5)
    pf = REPO_ROOT / "tests" / "pointer-fix" / "raw"
    if pf.is_dir():
        calls = agent_tool_calls(pf / "science-engineering-2.a1.agent")
        d, s = delivery(pf / "science-engineering-2.a1.files")
        check("Skill-first skip classified", not d and skip_mode(calls, s) == "skill-first")
        d, s = delivery(pf / "science-engineering-2.supp1.a1.files")
        check("partial delivery classified", not d and s == "partial")
        d, _ = delivery(pf / "estimate-fermi.a1.files")
        check("delivered capture classified", d)

    sched = schedule(["p1", "p2"])
    check("schedule 2 prompts x 2 repeats x 1 arm = 4, stage 1 first",
          len(sched) == 4 and [r for _, _, r in sched] == [1, 1, 2, 2])  # fmt: skip
    check("sib keeps the attempt marker", sib(Path("N.x.r1.a1"), ".jsonl").name == "N.x.r1.a1.jsonl")
    print(f"audit-first --self-test: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", nargs="?", choices=["run", "read"])
    ap.add_argument("--bodies", type=Path)
    ap.add_argument("--work", type=Path)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--stage", type=int, choices=[1, 2])
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if a.cmd == "run":
        if not (a.bodies and a.work):
            ap.error("run needs --bodies and --work")
        return cmd_run(a.bodies.resolve(), a.work.resolve(), a.workers, a.stage)
    if a.cmd == "read":
        return cmd_read()
    ap.error("give run, read or --self-test")
    return 2


if __name__ == "__main__":
    sys.exit(main())
