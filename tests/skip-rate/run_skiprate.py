#!/usr/bin/env python3
"""skip-rate -- the measurement pre-registered in docs/skip-rate-preregistration.md.

    python3 tests/skip-rate/run_skiprate.py run --bodies <dir> --work <dir> [--workers 2]
    python3 tests/skip-rate/run_skiprate.py read
    python3 tests/skip-rate/run_skiprate.py --self-test

<bodies>/A/first-principles is the v9.19.2 plugin tree, <bodies>/B/first-principles v9.19.3's,
each exported with `git archive`. Resumable: a run already recorded in cells.json is not re-run.
A measurement tool, never a gate.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
RAW = HERE / "raw"
CELLS = HERE / "cells.json"
PROMPTS_FILE = REPO_ROOT / "tests" / "example-rerun-2" / "prompts.json"

# --- pre-registered protocol --------------------------------------------------------------
MODEL = "claude-sonnet-5"
ARMS = ("A", "B")  # A = v9.19.2, B = v9.19.3
REPEATS = (1, 2)
MAX_ATTEMPTS = 3  # first try + two routing-miss retries
AGENT_TYPE = "first-principles:first-principles"
LIMIT_PAUSE_S = 1800
# ------------------------------------------------------------------------------------------

_lock = threading.Lock()


def schedule(prompts: list[str]) -> list[tuple[str, str, int]]:
    """Interleaved: prompt by prompt, repeat by repeat, alternating which arm goes first."""
    order, flip = [], False
    for r in REPEATS:
        for pid in prompts:
            arms = ARMS[::-1] if flip else ARMS
            order += [(arm, pid, r) for arm in arms]
            flip = not flip
    return order


def events(text: str):
    for line in text.splitlines():
        try:
            yield json.loads(line)
        except ValueError:
            continue


def init_event(text: str) -> dict:
    return next((o for o in events(text) if o.get("type") == "system" and o.get("subtype") == "init"), {})


def result_events(text: str) -> list[dict]:
    """Every `result` event, in order. A run usually has two: the session's main turn, then
    a short follow-up turn after the background agent's completion notice -- so the LAST
    one alone measures seconds, not the run (fixed 2026-10-09, before the reading)."""
    return [o for o in events(text) if o.get("type") == "result"]


def agent_minutes(agent_dir: Path) -> float | None:
    """Wall-clock minutes of the first-principles agent, first to last transcript timestamp."""
    from datetime import datetime

    stamps = []
    for f in sorted(agent_dir.glob("agent-*.jsonl")):
        for o in events(f.read_text(encoding="utf-8", errors="replace")):
            t = o.get("timestamp")
            if t:
                stamps.append(datetime.fromisoformat(t.replace("Z", "+00:00")))
    return round((max(stamps) - min(stamps)).total_seconds() / 60, 1) if stamps else None


def result_event(text: str) -> dict:
    last = {}
    for o in events(text):
        if o.get("type") == "result":
            last = o
    return last


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
    """The first-principles agent's own tool calls, in order. Picks the transcript whose
    meta names the agent type; falls back to every agent-*.jsonl in the directory."""
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
    """(delivered, state) from the files on disk -- the pre-registered criterion."""
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


def guard_log(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    return [json.loads(ln) for ln in path.read_text().splitlines() if ln.strip()]


def score(key: str, cell: dict) -> dict:
    base = RAW / cell["scored"]
    text = (base.with_suffix(".jsonl")).read_text(encoding="utf-8", errors="replace")
    delivered, state = delivery(base.with_suffix(".files"))
    calls = agent_tool_calls(base.with_suffix(".agent"))
    log = guard_log(base.with_suffix(".guard.jsonl"))
    decisions = [(e.get("reply") or {}).get("decision") == "block" for e in log]
    results = result_events(text)
    return {
        "key": key,
        "arm": cell["arm"],
        "prompt": cell["prompt"],
        "delivered": delivered,
        "state": state,
        "mode": None if delivered else skip_mode(calls, state),
        "first_call": calls[0][0] if calls else None,
        "skill_calls": sum(1 for n, _ in calls if n == "Skill"),
        "tool_calls": len(calls),
        "stops": len(log),
        "blocks": sum(decisions),
        "first_stop_skip": (decisions[0] if decisions else False) if cell["arm"] == "B" else not delivered,
        "agent_min": agent_minutes(base.with_suffix(".agent")),
        "session_min": round(sum(r.get("duration_ms") or 0 for r in results) / 60000, 1),
        "cost_usd": max((r.get("total_cost_usd") or 0 for r in results), default=0),
        "attempts": len(cell["attempts"]),
    }


# --- running -----------------------------------------------------------------------------


def generate(text: str, body: Path, cwd: Path, base: Path) -> str:
    argv = [
        "claude", "-p", "--model", MODEL, "--plugin-dir", str(body),
        "--output-format", "stream-json", "--verbose",
        "--permission-mode", "bypassPermissions", text,
    ]  # fmt: skip
    env = {**os.environ, "CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS": "0",
           "FP_GUARD_LOG": str(base.with_suffix(".guard.jsonl"))}  # fmt: skip
    proc = subprocess.run(argv, capture_output=True, text=True, timeout=5400, env=env, cwd=cwd, check=False)
    base.with_suffix(".jsonl").write_text(proc.stdout, encoding="utf-8")
    if proc.stderr.strip():
        base.with_suffix(".stderr").write_text(proc.stderr, encoding="utf-8")
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
        base.with_suffix(".guard.jsonl").unlink(missing_ok=True)
        print(f"[run] {key} attempt {n} ...", flush=True)
        text = generate(prompt, body, cwd, base)
        if is_limit_stub(text):
            for suf in (".jsonl", ".guard.jsonl", ".stderr"):
                p = base.with_suffix(suf)
                if p.exists():
                    p.rename(RAW / f"{key}.a{n}.limit-stub{suf}")
            print(f"[pause] {key}: usage-limit stub; sleeping {LIMIT_PAUSE_S}s", flush=True)
            time.sleep(LIMIT_PAUSE_S)
            n -= 1
            continue
        plugins = [p.get("path") for p in init_event(text).get("plugins") or [] if p.get("name") == "first-principles"]
        if plugins != [str(body)]:
            raise SystemExit(f"[abort] {key}: loaded {plugins}, expected {body}")
        capture_agent(text, base.with_suffix(".agent"))
        src = cwd / ".first-principles"
        if src.is_dir():
            shutil.copytree(src, base.with_suffix(".files"), dirs_exist_ok=True)
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
                f"blocks={s['blocks']} first={s['first_call']} agent_min={s['agent_min']}",
                flush=True,
            )
        else:
            print(f"[done] {key} EXHAUSTED", flush=True)


def cmd_run(bodies: Path, work: Path, workers: int) -> int:
    prompts = json.loads(PROMPTS_FILE.read_text())
    for arm in ARMS:
        if not (bodies / arm / "first-principles" / "agents" / "first-principles.md").is_file():
            raise SystemExit(f"missing body for arm {arm} under {bodies}")
    RAW.mkdir(parents=True, exist_ok=True)
    done = json.loads(CELLS.read_text()) if CELLS.is_file() else {}
    todo = [(a, p, r) for a, p, r in schedule(list(prompts)) if f"{a}.{p}.r{r}" not in done]
    print(f"[plan] {len(todo)} runs to go, {workers} at a time", flush=True)
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = [ex.submit(run_one, a, p, r, prompts[p], bodies, work) for a, p, r in todo]
        for f in futures:
            f.result()
    return cmd_read()


# --- reading -----------------------------------------------------------------------------


def fisher_one_sided(a_k: int, a_n: int, b_k: int, b_n: int) -> float:
    """P(B skips <= b_k | margins): one-sided test that B's rate is lower than A's."""
    total_k, total_n = a_k + b_k, a_n + b_n
    denom = comb(total_n, total_k)
    return sum(
        comb(b_n, x) * comb(a_n, total_k - x)
        for x in range(0, b_k + 1)
        if 0 <= total_k - x <= a_n
    ) / denom


def fisher_two_sided(a_k: int, a_n: int, b_k: int, b_n: int) -> float:
    total_k, total_n = a_k + b_k, a_n + b_n
    denom = comb(total_n, total_k)

    def p(x: int) -> float:
        return comb(b_n, x) * comb(a_n, total_k - x) / denom

    obs = p(b_k)
    return min(1.0, sum(p(x) for x in range(0, min(b_n, total_k) + 1)
                        if 0 <= total_k - x <= a_n and p(x) <= obs * (1 + 1e-9)))  # fmt: skip


def cmd_read() -> int:
    cells = json.loads(CELLS.read_text()) if CELLS.is_file() else {}
    rows = [score(k, c) for k, c in sorted(cells.items()) if c["outcome"] == "scored"]
    exhausted = sorted(k for k, c in cells.items() if c["outcome"] != "scored")
    by = {arm: [r for r in rows if r["arm"] == arm] for arm in ARMS}
    print("skip-rate -- 9.19.2 (A) vs 9.19.3 (B)\n")
    for arm in ARMS:
        rs = by[arm]
        n = len(rs)
        sk = sum(not r["delivered"] for r in rs)
        fs = sum(r["first_stop_skip"] for r in rs)
        print(f"arm {arm}: scored {n}, skipped {sk}, first-stop skips {fs}, "
              f"Skill calls in {sum(r['skill_calls'] > 0 for r in rs)} runs")  # fmt: skip
    a, b = by["A"], by["B"]
    a_k, b_k = sum(not r["delivered"] for r in a), sum(not r["delivered"] for r in b)
    b_fs = sum(r["first_stop_skip"] for r in b)
    if a and b:
        print(f"\nQ3 final skips: A {a_k}/{len(a)} vs B {b_k}/{len(b)}; "
              f"Fisher one-sided (B<A) p = {fisher_one_sided(a_k, len(a), b_k, len(b)):.3f}")  # fmt: skip
        verdict = (
            "UNINFORMATIVE (baseline did not recur: A < 3 skips)" if a_k < 3
            else "SHOWN EFFECTIVE" if b_k <= 1 else "NOT SHOWN EFFECTIVE"
        )  # fmt: skip
        print(f"    pre-registered verdict: {verdict}")
        print(f"Q2 first-stop skips: A {a_k}/{len(a)} vs B {b_fs}/{len(b)}; "
              f"Fisher two-sided p = {fisher_two_sided(a_k, len(a), b_fs, len(b)):.3f}")  # fmt: skip
        blocked = [r for r in b if r["blocks"]]
        print(f"Q4 recovery: {sum(r['delivered'] for r in blocked)} of {len(blocked)} blocked B runs delivered")
        def med(xs):
            xs = sorted(x for x in xs if x is not None)
            return xs[len(xs) // 2] if xs else None

        for arm in ARMS:
            for label, rs in (("delivered", [r for r in by[arm] if r["delivered"]]), ("all", by[arm])):
                if rs:
                    print(f"Q5 arm {arm} ({label}, n={len(rs)}): median agent {med(r['agent_min'] for r in rs)} min, "
                                                    f"{med(r['tool_calls'] for r in rs)} agent tool calls, ${med(r['cost_usd'] for r in rs):.2f}")  # fmt: skip
        for r in blocked:
            print(f"    blocked: {r['key']} blocks={r['blocks']} delivered={r['delivered']} "
                  f"agent_min={r['agent_min']} tool_calls={r['tool_calls']} cost=${r['cost_usd']:.2f}")  # fmt: skip
    print("\nskips / first-stop skips:")
    for r in rows:
        if not r["delivered"] or r["first_stop_skip"]:
            print(f"  {r['key']}: delivered={r['delivered']} mode={r['mode']} first_call={r['first_call']} "
                  f"tools={r['tool_calls']} blocks={r['blocks']} attempts={r['attempts']}")  # fmt: skip
    if exhausted:
        print(f"\nexhausted (routing misses, excluded): {exhausted}")
    (HERE / "readings.json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    return 0


def self_test() -> int:
    ok = True

    def check(label, cond):
        nonlocal ok
        print(f"skip-rate --self-test: {label} {'PASS' if cond else 'FAIL'}")
        ok &= bool(cond)

    sched = schedule(["p1", "p2"])
    check("schedule 2 prompts x 2 repeats x 2 arms = 8, balanced", len(sched) == 8
          and sum(a == "A" for a, _, _ in sched) == 4 and sched[0][0] != sched[2][0])  # fmt: skip
    check("fisher 0/28 vs 4/28 one-sided", abs(fisher_one_sided(4, 28, 0, 28) - 0.0558) < 0.002)
    check("fisher equal counts two-sided = 1", abs(fisher_two_sided(3, 28, 3, 28) - 1.0) < 1e-9)
    fg = REPO_ROOT / "tests" / "delivery-guard" / "raw"
    if fg.is_dir():
        d, s = delivery(fg / "forced-skip.files")
        check("forced-skip capture delivered", d and s == "delivered")
        log = guard_log(fg / "forced-skip.guard.jsonl")
        check("forced-skip guard log first stop blocked", (log[0]["reply"] or {}).get("decision") == "block")
        txt = (fg / "forced-skip.jsonl").read_text()
        check("forced-skip dispatched", dispatched(txt) and not is_limit_stub(txt))
    pf = REPO_ROOT / "tests" / "pointer-fix" / "raw"
    if pf.is_dir():
        calls = agent_tool_calls(pf / "science-engineering-2.a1.agent")
        d, s = delivery(pf / "science-engineering-2.a1.files")
        check("Skill-first skip classified", not d and skip_mode(calls, s) == "skill-first")
        calls = agent_tool_calls(pf / "product-business.a1.agent")
        d, s = delivery(pf / "product-business.a1.files")
        check("zero-tool skip classified", not d and skip_mode(calls, s) == "zero-tool")
        d, s = delivery(pf / "science-engineering-2.supp1.a1.files")
        check("partial delivery classified", not d and s == "partial")
        d, _ = delivery(pf / "estimate-fermi.a1.files")
        check("delivered capture classified", d)
    if fg.is_dir():
        txt = (fg / "forced-skip.jsonl").read_text()
        am = agent_minutes(fg / "forced-skip.agent")
        sm = sum(r.get("duration_ms") or 0 for r in result_events(txt)) / 60000
        check("timing: agent minutes read from its transcript, > 5", am is not None and am > 5)
        # session_min is kept in readings.json but never printed: in this capture the
        # result events do cover the agent, but on live runs they often do not (B's median
        # read 1.6 min against 23 min of agent time), so it is not a measure of the run.
        check("timing: session total recorded", sm > 0)
    print(f"skip-rate --self-test: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", nargs="?", choices=["run", "read"])
    ap.add_argument("--bodies", type=Path)
    ap.add_argument("--work", type=Path)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if a.cmd == "run":
        if not (a.bodies and a.work):
            ap.error("run needs --bodies and --work")
        return cmd_run(a.bodies.resolve(), a.work.resolve(), a.workers)
    if a.cmd == "read":
        return cmd_read()
    ap.error("give run, read or --self-test")
    return 2


if __name__ == "__main__":
    sys.exit(main())
