#!/usr/bin/env python3
"""w4-paired -- the paired re-run pre-registered in docs/w4-paired-preregistration.md.

Same five prompts, two bodies (v9.0.0 and v9.12.0), three repeats each. Every protocol
constant below is fixed by that document; change it there under a new id, not here.

A measurement tool, never a gate: the reading is K-of-N live observation and
docs/v8.7-constraint-teardown.md section 2 item 3 bars such readings from gating.

    python3 tests/w4-paired/run_paired.py plan
    python3 tests/w4-paired/run_paired.py run  --old <wt-v9.0.0>/first-principles \\
                                               --new <wt-v9.12.0>/first-principles
    python3 tests/w4-paired/run_paired.py read

`run` is resumable: a generation whose document already exists is skipped, so a usage-limit
pause is recovered by re-running the same command.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
RAW = HERE / "raw"
DOCS = HERE / "documents"

# --- pre-registered protocol (docs/w4-paired-preregistration.md) -------------------
MODEL = "claude-sonnet-5"
PROMPTS = (  # (id, catalog, prompt column index after splitting the row on "|")
    ("TB-02", "tests/trackb-catalog-v9.13.md", 3),
    ("TB-06", "tests/trackb-catalog-v9.13.md", 3),
    ("TB-10", "tests/trackb-catalog-v9.13.md", 3),
    ("Q-P2", "tests/live-conformance-catalog.md", 2),
    ("PR-N1", "tests/live-conformance-catalog.md", 2),
)
ARMS = ("old", "new")
REPEATS = 3
MAX_VOIDS_PER_ARM = 3
SUPPORT_MIN_DOCS = 3
SUPPORT_MAX_P = 0.10
NO_DIFF_MAX_DOCS = 1
# ------------------------------------------------------------------------------------


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, REPO_ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


stage_a = _load("_stage_a", "scripts/check-emission-stage-a.py")
qh = _load("_qh", "scripts/check-quality-harness.py")


def prompt_text(pid: str, catalog: str, col: int) -> str:
    for line in (REPO_ROOT / catalog).read_text(encoding="utf-8").splitlines():
        cells = line.split("|")
        if len(cells) > col and cells[1].strip() == pid:
            return cells[col].strip()
    raise SystemExit(f"prompt {pid} not found in {catalog}")


def schedule() -> list[tuple[str, str, int]]:
    """Prompt by prompt; within a repeat both arms back to back, first arm alternating."""
    out = []
    for pid, _, _ in PROMPTS:
        for rep in range(1, REPEATS + 1):
            order = ARMS if rep % 2 else ARMS[::-1]
            out.extend((pid, arm, rep) for arm in order)
    return out


def stem(pid: str, arm: str, rep: int) -> str:
    return f"{pid}.{arm}.r{rep}"


def is_limit_stub(jsonl: str) -> bool:
    for line in jsonl.splitlines():
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("type") == "result" and obj.get("is_error"):
            return True
    return bool(re.search(r"usage limit|rate limit", jsonl[-4000:], re.I)) and '"parent_tool_use_id":"' not in jsonl


def generate(text: str, plugin_dir: Path, raw_path: Path) -> str:
    argv = ["claude", "-p", "--model", MODEL, "--plugin-dir", str(plugin_dir),
            "--output-format", "stream-json", "--verbose", "--no-session-persistence",
            "--permission-mode", "bypassPermissions", text]
    env = {**os.environ, "CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS": "0"}
    proc = subprocess.run(argv, capture_output=True, text=True, timeout=5400, env=env,
                          cwd=REPO_ROOT)
    raw_path.write_text(proc.stdout, encoding="utf-8")
    return proc.stdout


def loaded_body(jsonl: str) -> list[str]:
    """Paths of every `first-principles` plugin the run's init event reports loading."""
    for line in jsonl.splitlines():
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("type") == "system" and obj.get("subtype") == "init":
            return [p.get("path", "") for p in obj.get("plugins") or []
                    if p.get("name") == "first-principles"]
    return []


_PERSISTED = "<persisted-output>"


def _tool_result_text(block: dict) -> str:
    c = block.get("content")
    if isinstance(c, str):
        return c
    return "".join(x.get("text", "") for x in c or [] if isinstance(x, dict))


def recover_persisted(jsonl: str) -> str | None:
    """Rebuild a hand-back the harness persisted to disk instead of inlining.

    Amendment 1 (docs/w4-paired-preregistration.md section 10). Over ~50 KB the Agent
    tool's result is stored as `<persisted-output>` and the transcript keeps a 2 KB
    preview, which `extract_subagent_text` then reads as the document. The orchestrator
    Read that file in the same run, so its full text is in the transcript as a
    line-numbered JSON array; this re-assembles it. Returns None when the report was
    persisted and never read back -- a transport failure, never a void.
    """
    persisted, reads = False, []
    for line in jsonl.splitlines():
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("type") != "user":
            continue
        for b in obj.get("message", {}).get("content", []) or []:
            if not (isinstance(b, dict) and b.get("type") == "tool_result"):
                continue
            s = _tool_result_text(b)
            if stage_a._HANDBACK_MARK not in s:
                continue
            if _PERSISTED in s:
                persisted = True
            else:
                reads.append(s)
    if not persisted:
        return None
    for s in reads:
        body = "\n".join(re.sub(r"^\s*\d+\t", "", ln) for ln in s.splitlines())
        try:
            arr = json.loads(body)
        except json.JSONDecodeError:
            continue
        text = "".join(x.get("text", "") for x in arr
                       if isinstance(x, dict) and x.get("type") == "text")
        if stage_a._HANDBACK_MARK in text:
            return stage_a._deframe_handback(text)
    return ""


def extract(jsonl: str) -> tuple[str, str, str]:
    """(document, orchestrator, status) -- status is 'ok', 'recovered' or 'transport'."""
    doc, orch = stage_a.extract_subagent_text(jsonl)
    rec = recover_persisted(jsonl)
    if rec is None:
        return doc, orch, "ok"
    if rec:
        return rec, orch, "recovered"
    return doc, orch, "transport"


def void_problems(doc: str, jsonl: str) -> list[str]:
    probs = stage_a.capture_problems(doc, from_subagent=bool(doc.strip()))
    if stage_a.agent_dispatches(jsonl) == 0:
        probs.insert(0, "agent never dispatched")
    return probs


def cmd_plan() -> int:
    s = schedule()
    print(f"w4-paired -- plan (no spend): {len(s)} generations, model {MODEL}")
    for pid, arm, rep in s:
        print(f"  {stem(pid, arm, rep)}")
    return 0


def cmd_run(dirs: dict[str, Path]) -> int:
    RAW.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    texts = {pid: prompt_text(pid, cat, col) for pid, cat, col in PROMPTS}
    voids = {a: 0 for a in ARMS}
    for pid, arm, rep in schedule():
        s = stem(pid, arm, rep)
        doc_path = DOCS / f"{s}.md"
        if doc_path.is_file():
            if (DOCS / f"{s}.void").is_file():
                voids[arm] += 1
            print(f"[gen] {s} (cached)", flush=True)
            continue
        for attempt in (1, 2):
            raw_path = RAW / f"{s}.jsonl"
            print(f"[gen] {s} attempt {attempt} ...", flush=True)
            jsonl = generate(texts[pid], dirs[arm], raw_path)
            if is_limit_stub(jsonl):
                raw_path.rename(RAW / f"{s}.limit-stub.jsonl")
                print(f"[pause] {s}: usage-limit/transport stub kept; re-run to resume",
                      flush=True)
                return 3
            # Transport integrity, not a void: a run on the wrong body must never be scored.
            if loaded_body(jsonl) != [str(dirs[arm])]:
                print(f"[abort] {s}: loaded {loaded_body(jsonl)}, expected {dirs[arm]}",
                      flush=True)
                return 5
            doc, orch, _status = extract(jsonl)
            probs = void_problems(doc, jsonl)
            if not probs:
                break
            print(f"[void] {s} attempt {attempt}: {probs}", flush=True)
            if attempt == 1:
                raw_path.rename(RAW / f"{s}.attempt1.jsonl")
        doc_path.write_text(doc, encoding="utf-8")
        (DOCS / f"{s}.orchestrator.md").write_text(orch, encoding="utf-8")
        if probs:
            (DOCS / f"{s}.void").write_text("\n".join(probs) + "\n", encoding="utf-8")
            voids[arm] += 1
            if voids[arm] > MAX_VOIDS_PER_ARM:
                print(f"[stop] arm {arm} exceeded {MAX_VOIDS_PER_ARM} voids", flush=True)
                return 4
        print(f"[gen] {s} {len(doc.split())}w {'VOID' if probs else 'ok'}", flush=True)
    return cmd_read()


def cmd_reextract() -> int:
    """Rebuild every cell's document from `raw/`, under Amendment 1's cell rule.

    A cell's document is its FIRST attempt (`.attempt1.jsonl`, then `.jsonl`) that is
    neither a transport failure nor a void. If every attempt voids, the cell is void.
    The rule is fixed before any defect is read, so choosing an attempt can never
    depend on what the detector would say about it.
    """
    log = []
    for pid, arm, rep in schedule():
        s = stem(pid, arm, rep)
        attempts = [p for p in (RAW / f"{s}.attempt1.jsonl", RAW / f"{s}.jsonl") if p.is_file()]
        if not attempts:
            continue
        chosen = None
        for p in attempts:
            jsonl = p.read_text(encoding="utf-8")
            doc, orch, status = extract(jsonl)
            probs = [] if status == "transport" else void_problems(doc, jsonl)
            log.append({"cell": s, "attempt": p.name, "status": status, "void": probs})
            if status != "transport" and not probs:
                chosen = (doc, orch, [])
                break
            if status != "transport":
                chosen = (doc, orch, probs)          # void; a later attempt may replace it
        if chosen is None:
            continue
        doc, orch, probs = chosen
        (DOCS / f"{s}.md").write_text(doc, encoding="utf-8")
        (DOCS / f"{s}.orchestrator.md").write_text(orch, encoding="utf-8")
        void_marker = DOCS / f"{s}.void"
        if probs:
            void_marker.write_text("\n".join(probs) + "\n", encoding="utf-8")
        elif void_marker.exists():
            void_marker.unlink()
    (HERE / "attempts.json").write_text(json.dumps(log, indent=2) + "\n", encoding="utf-8")
    for e in log:
        print(f"{e['cell']:<16}{e['attempt']:<32}{e['status']:<11}"
              f"{'VOID ' + e['void'][0][:40] if e['void'] else 'ok'}")
    return 0


# --- reading ------------------------------------------------------------------------

_LEAD_GT = re.compile(r"^\s*(?:→|->)\s*GT-", re.M)


def fisher_one_sided(a: int, n1: int, b: int, n2: int, greater_first: bool) -> float:
    """P(X >= a) (or <= a) for X ~ Hypergeom: a of n1 in arm 1, b of n2 in arm 2."""
    k, n = a + b, n1 + n2
    def pmf(x: int) -> float:
        return math.comb(n1, x) * math.comb(n2, k - x) / math.comb(n, k)
    lo, hi = max(0, k - n2), min(k, n1)
    xs = range(a, hi + 1) if greater_first else range(lo, a + 1)
    return sum(pmf(x) for x in xs)


def verdict(new_k: int, new_n: int, old_k: int, old_n: int) -> tuple[str, float]:
    d = new_k - old_k
    if new_n == 0 or old_n == 0:
        return "inconclusive (an arm has no readable documents)", 1.0
    p = fisher_one_sided(new_k, new_n, old_k, old_n, greater_first=d >= 0)
    if abs(d) >= SUPPORT_MIN_DOCS and p <= SUPPORT_MAX_P:
        return f"body difference supported ({'new worse' if d > 0 else 'new better'})", p
    if abs(d) <= NO_DIFF_MAX_DOCS:
        return "no difference detected at this N", p
    return "inconclusive", p


def cmd_read() -> int:
    per = {a: {} for a in ARMS}
    unreadable = {a: [] for a in ARMS}
    void = {a: [] for a in ARMS}
    for pid, arm, rep in schedule():
        s = stem(pid, arm, rep)
        path = DOCS / f"{s}.md"
        if not path.is_file():
            continue
        if (DOCS / f"{s}.void").is_file():
            void[arm].append(s)
            continue
        try:
            per[arm][s] = qh.detect_defects(path.read_text(encoding="utf-8"), s)
        except qh.SectionResolutionError:
            unreadable[arm].append(s)

    print("w4-paired -- reading (a recorded reading with its N, never a gate)\n")
    print(f"{'doc':<16}{'blocks':>7}{'mal':>5}{'leadGT':>7}{'cells':>7}{'noncf':>7}"
          f"{'claims':>7}{'untr':>6}")
    for arm in ARMS:
        for s, r in per[arm].items():
            lead = sum(1 for b in r["_malformed_chain_blocks_text"] if _LEAD_GT.search(b))
            print(f"{s:<16}{r['chain_blocks']:>7}{r['malformed_chain_blocks']:>5}{lead:>7}"
                  f"{r['verdict_cells']:>7}{r['nonconforming_verdict_cells']:>7}"
                  f"{r['conclusion_claims']:>7}{r['untraced_claims']:>6}")
    print()
    for arm in ARMS:
        print(f"arm {arm}: readable {len(per[arm])}, unreadable {unreadable[arm]}, "
              f"void {void[arm]}")
    print()
    summary = {}
    for axis, field in (("A1 malformed chain block", "malformed_chain_blocks"),
                        ("A2 nonconforming verdict cell", "nonconforming_verdict_cells")):
        k = {a: sum(1 for r in per[a].values() if r[field] > 0) for a in ARMS}
        n = {a: len(per[a]) for a in ARMS}
        v, p = verdict(k["new"], n["new"], k["old"], n["old"])
        summary[axis] = {"old": [k["old"], n["old"]], "new": [k["new"], n["new"]],
                         "p_one_sided": round(p, 4), "reading": v}
        print(f"{axis:<32} old {k['old']}/{n['old']}  new {k['new']}/{n['new']}  "
              f"p={p:.3f}  -> {v}")
    lead = {a: sum(1 for r in per[a].values() for b in r["_malformed_chain_blocks_text"]
                   if _LEAD_GT.search(b)) for a in ARMS}
    mal = {a: sum(r["malformed_chain_blocks"] for r in per[a].values()) for a in ARMS}
    print(f"\nmalformed blocks whose cause is a leading-GT hop: old {lead['old']}/{mal['old']}"
          f"  new {lead['new']}/{mal['new']}")
    for field, den in (("untraced_claims", "conclusion_claims"),
                       ("malformed_chain_blocks", "chain_blocks"),
                       ("nonconforming_verdict_cells", "verdict_cells")):
        parts = []
        for a in ARMS:
            x = sum(r[field] for r in per[a].values())
            y = sum(r[den] for r in per[a].values())
            parts.append(f"{a} {x}/{y}")
        tag = "  (reported only: contracts differ)" if field == "untraced_claims" else ""
        print(f"{field:<30} " + "  ".join(parts) + tag)
    # Contract abandonment is counted over ATTEMPTS, not cells: a void retried into a
    # readable document still happened, and the cell rule would otherwise hide it.
    # Two different failures, never pooled: a ROUTING MISS (the main session answered
    # without dispatching the agent) says nothing about the body's output contract; an
    # ABANDONMENT (dispatched, contract not emitted) does.
    abandon = {a: [0, 0] for a in ARMS}       # [abandoned, dispatched attempts]
    routing = {a: [0, 0] for a in ARMS}       # [never dispatched, attempts]
    attempts_path = HERE / "attempts.json"
    if attempts_path.is_file():
        for e in json.loads(attempts_path.read_text(encoding="utf-8")):
            if e["status"] == "transport":
                continue
            arm = e["cell"].split(".")[1]
            routing[arm][1] += 1
            if e["void"] and e["void"][0] == "agent never dispatched":
                routing[arm][0] += 1
                continue
            abandon[arm][1] += 1
            abandon[arm][0] += bool(e["void"])
        print("routing misses (never dispatched / attempts):       "
              + "  ".join(f"{a} {routing[a][0]}/{routing[a][1]}" for a in ARMS))
        print("contract abandonment (void / dispatched attempts):  "
              + "  ".join(f"{a} {abandon[a][0]}/{abandon[a][1]}" for a in ARMS))
        p = fisher_one_sided(abandon["new"][0], abandon["new"][1],
                             abandon["old"][0], abandon["old"][1], greater_first=True)
        print(f"  (reported only, not a pre-registered outcome: one-sided p={p:.3f})")
    (HERE / "result.json").write_text(json.dumps(
        {"summary": summary, "unreadable": unreadable, "void": void,
         "abandonment_attempts": abandon, "routing_miss_attempts": routing,
         "leading_gt_malformed": lead, "malformed": mal}, indent=2) + "\n", encoding="utf-8")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=("plan", "run", "reextract", "read"))
    ap.add_argument("--old", type=Path)
    ap.add_argument("--new", type=Path)
    a = ap.parse_args()
    if a.command == "plan":
        return cmd_plan()
    if a.command == "read":
        return cmd_read()
    if a.command == "reextract":
        return cmd_reextract()
    if not (a.old and a.new):
        ap.error("run needs --old and --new plugin directories")
    return cmd_run({"old": a.old.resolve(), "new": a.new.resolve()})


if __name__ == "__main__":
    sys.exit(main())
