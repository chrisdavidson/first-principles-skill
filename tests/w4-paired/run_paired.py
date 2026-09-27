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
            doc, orch = stage_a.extract_subagent_text(jsonl)
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
    (HERE / "result.json").write_text(json.dumps(
        {"summary": summary, "unreadable": unreadable, "void": void,
         "leading_gt_malformed": lead, "malformed": mal}, indent=2) + "\n", encoding="utf-8")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=("plan", "run", "read"))
    ap.add_argument("--old", type=Path)
    ap.add_argument("--new", type=Path)
    a = ap.parse_args()
    if a.command == "plan":
        return cmd_plan()
    if a.command == "read":
        return cmd_read()
    if not (a.old and a.new):
        ap.error("run needs --old and --new plugin directories")
    return cmd_run({"old": a.old.resolve(), "new": a.new.resolve()})


if __name__ == "__main__":
    sys.exit(main())
