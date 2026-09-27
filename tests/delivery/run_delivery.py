#!/usr/bin/env python3
"""delivery -- the measurement pre-registered in docs/delivery-preregistration.md.

    python3 tests/delivery/run_delivery.py plan
    python3 tests/delivery/run_delivery.py run --body <wt>/first-principles --cwd <empty dir>
    python3 tests/delivery/run_delivery.py read
    python3 tests/delivery/run_delivery.py --self-test

Unlike every earlier live capture here, runs keep session persistence so the AGENT'S OWN
transcript survives; it is copied to raw/<key>.agent/ beside the stream-json capture. The
delivery failure rate is reported as its own number. A measurement tool, never a gate.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
RAW = HERE / "raw"
DOCS = HERE / "documents"


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, REPO_ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


p1 = _load("_p1dl", "tests/abandonment/run_phase1.py")
w4, p0, stage_a = p1.w4, p1.p0, p1.stage_a

# --- pre-registered protocol (section 2 and 3) ---------------------------------------------
MODEL = "claude-sonnet-5"
PROMPTS = [f"TB-{i:02d}" for i in range(1, 11)]
CATALOG = "tests/trackb-catalog-v9.13.md"
REPEATS = 2
MAX_ATTEMPTS = 3
MIN_WORDS = stage_a.MIN_WORDS            # 120
MIN_SECTIONS = stage_a.MIN_SECTIONS      # 4
DELEGATION = {"Agent", "SendMessage", "ListAgents"}
# ------------------------------------------------------------------------------------------


def schedule() -> list[str]:
    return [f"{pid}.r{r}" for pid in PROMPTS for r in range(1, REPEATS + 1)]


def generate(text: str, body: Path, cwd: Path, raw_path: Path) -> str:
    argv = ["claude", "-p", "--model", MODEL, "--plugin-dir", str(body),
            "--output-format", "stream-json", "--verbose",
            "--permission-mode", "bypassPermissions", text]      # persistence deliberately ON
    env = {**os.environ, "CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS": "0"}
    proc = subprocess.run(argv, capture_output=True, text=True, timeout=5400, env=env, cwd=cwd)
    raw_path.write_text(proc.stdout, encoding="utf-8")
    return proc.stdout


def session_of(jsonl: str) -> tuple[str | None, str | None]:
    for obj in p0._events(jsonl):
        if obj.get("type") == "system" and obj.get("subtype") == "init":
            return obj.get("session_id"), obj.get("cwd")
    return None, None


def capture_agent_transcripts(jsonl: str, dest: Path) -> int:
    """Copy the session's subagents/*.jsonl (and .meta.json) beside the raw capture."""
    sid, cwd = session_of(jsonl)
    if not (sid and cwd):
        return 0
    key = cwd.replace("/", "-").replace(".", "-")
    src = Path.home() / ".claude" / "projects" / key / sid / "subagents"
    if not src.is_dir():
        return 0
    dest.mkdir(parents=True, exist_ok=True)
    n = 0
    for f in sorted(src.iterdir()):
        shutil.copy2(f, dest / f.name)
        n += f.suffix == ".jsonl"
    return n


def agent_messages(agent_dir: Path) -> list[dict]:
    """The agent's own assistant messages, in order: [{'text': str, 'tools': [names]}]."""
    out = []
    for f in sorted(agent_dir.glob("agent-*.jsonl")):
        for obj in p0._events(f.read_text(encoding="utf-8")):
            if obj.get("type") != "assistant":
                continue
            text, tools = [], []
            for b in obj.get("message", {}).get("content", []) or []:
                if not isinstance(b, dict):
                    continue
                if b.get("type") == "text" and b.get("text", "").strip():
                    text.append(b["text"])
                elif b.get("type") == "tool_use":
                    tools.append(b.get("name"))
            if text or tools:
                out.append({"text": "\n".join(text), "tools": tools})
    return out


def classify_delivery(delivered: str, msgs: list[dict]) -> dict:
    """Section 3's definitions, first match wins: interrupted, split, whole."""
    texts = [m["text"] for m in msgs if m["text"]]
    emitted = "\n".join(texts)
    stranded = sum(len(t.split()) for t in texts[:-1]) if texts else 0
    sec_emitted = len(stage_a.sections_present(emitted))
    sec_delivered = len(stage_a.sections_present(delivered))
    if len(delivered.split()) < MIN_WORDS:
        status = "interrupted"
    elif stranded >= MIN_WORDS and sec_emitted >= MIN_SECTIONS and sec_delivered < MIN_SECTIONS:
        status = "split"
    else:
        status = "whole"
    between = []                       # tool calls that separate the document's text messages
    seen_text = False
    for m in msgs:
        if m["text"]:
            seen_text = True
        if seen_text and m["tools"]:
            between.extend(m["tools"])
    return {
        "status": status,
        "text_messages": len(texts),
        "stranded_words": stranded,
        "sections_emitted": sec_emitted,
        "sections_delivered": sec_delivered,
        "abandoned": sec_emitted < MIN_SECTIONS,
        "delegation_calls": sorted(t for m in msgs for t in m["tools"] if t in DELEGATION),
        "tools_between_text": between[-6:],
    }


def cmd_plan() -> int:
    print(f"delivery -- plan (no spend): {len(schedule())} runs, model {MODEL}, persistence ON")
    for key in schedule():
        print(f"  {key}")
    return 0


def cmd_run(body: Path, cwd: Path) -> int:
    if any(cwd.iterdir()):
        raise SystemExit(f"--cwd {cwd} is not empty")
    RAW.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    texts = {pid: p1.prompt_text(pid, CATALOG) for pid in PROMPTS}
    cells_path = HERE / "cells.json"
    cells = json.loads(cells_path.read_text()) if cells_path.is_file() else {}
    for key in schedule():
        if key in cells:
            print(f"[gen] {key} (recorded: {cells[key]['outcome']})", flush=True)
            continue
        pid = key.split(".")[0]
        attempts, outcome = [], "exhausted"
        for n in range(1, MAX_ATTEMPTS + 1):
            raw = RAW / f"{key}.a{n}.jsonl"
            if not raw.is_file():
                print(f"[gen] {key} attempt {n} ...", flush=True)
                jsonl = generate(texts[pid], body, cwd, raw)
                if w4.is_limit_stub(jsonl):
                    raw.rename(RAW / f"{key}.a{n}.limit-stub.jsonl")
                    print(f"[pause] {key}: usage-limit stub; re-run to resume", flush=True)
                    return 3
                if w4.loaded_body(jsonl) != [str(body)]:
                    print(f"[abort] {key}: loaded {w4.loaded_body(jsonl)}", flush=True)
                    return 5
                got = capture_agent_transcripts(jsonl, RAW / f"{key}.a{n}.agent")
                print(f"[capture] {key} attempt {n}: {got} agent transcript(s)", flush=True)
            attempts.append(raw.name)
            r = p1.classify(raw, "body")
            if not r["dispatched"]:
                print(f"[miss] {key} attempt {n}", flush=True)
                continue
            if r["transport"]:
                print(f"[transport] {key} attempt {n}", flush=True)
                continue
            (DOCS / f"{key}.md").write_text(r["_doc"], encoding="utf-8")
            outcome = "scored"
            break
        cells[key] = {"outcome": outcome, "attempts": attempts,
                      "scored": attempts[-1] if outcome == "scored" else None}
        cells_path.write_text(json.dumps(cells, indent=2) + "\n", encoding="utf-8")
        if outcome == "scored":
            d = classify_delivery((DOCS / f"{key}.md").read_text(encoding="utf-8"),
                                  agent_messages(RAW / attempts[-1].replace(".jsonl", ".agent")))
            print(f"[gen] {key} {d['status'].upper()}", flush=True)
        else:
            print(f"[gen] {key} EXHAUSTED", flush=True)
    return cmd_read()


def cmd_read() -> int:
    cells = json.loads((HERE / "cells.json").read_text())
    rows = {}
    for key, v in cells.items():
        if v["outcome"] != "scored":
            continue
        agent_dir = RAW / v["scored"].replace(".jsonl", ".agent")
        msgs = agent_messages(agent_dir) if agent_dir.is_dir() else []
        rows[key] = classify_delivery((DOCS / f"{key}.md").read_text(encoding="utf-8"), msgs)
        rows[key]["agent_transcript"] = bool(msgs)
    print("delivery -- reading (a recorded reading with its N, never a gate)\n")
    print(f"{'run':<10}{'status':<13}{'msgs':>5}{'stranded':>9}{'sec emit':>9}{'sec dlvr':>9}"
          f"  delegation / tools between text")
    for k, r in rows.items():
        print(f"{k:<10}{r['status']:<13}{r['text_messages']:>5}{r['stranded_words']:>9}"
              f"{r['sections_emitted']:>9}{r['sections_delivered']:>9}  "
              f"{r['delegation_calls'] or ''} {r['tools_between_text'] if r['status'] != 'whole' else ''}")
    n = len(rows)
    count = lambda s: sum(r["status"] == s for r in rows.values())
    fail = count("split") + count("interrupted")
    missing = [k for k, r in rows.items() if not r["agent_transcript"]]
    print(f"\nDELIVERY FAILURE RATE  {fail}/{n}  (split {count('split')}, interrupted "
          f"{count('interrupted')}, whole {count('whole')})   reference: Phase 1, 4/20, pre-fix")
    print(f"abandoned (no contract even in the agent's own text): "
          f"{sum(r['abandoned'] for r in rows.values())}/{n}")
    print(f"self-delegation calls: {sum(len(r['delegation_calls']) for r in rows.values())}"
          f"   exhausted cells: {sum(v['outcome'] == 'exhausted' for v in cells.values())}"
          f"   runs missing the agent transcript: {missing or 0}")
    (HERE / "result.json").write_text(json.dumps(
        {"rows": rows, "delivery_failures": fail, "n": n, "split": count("split"),
         "interrupted": count("interrupted"), "missing_agent_transcript": missing},
        indent=2) + "\n", encoding="utf-8")
    return 0


def self_test() -> int:
    """Offline controls on the classifier -- each must hold before any live run."""
    doc = "\n".join(f"## {i}. {s}\nbody text " * 1 for i, s in enumerate(stage_a.SECTIONS, 1))
    long = " word" * 200
    head = "## 1. Problem Essence\n" + long + "\n## 2. Assumptions Table\n" + long + \
        "\n## 3. Ground Truths\n" + long + "\n## 4. Derivation Chains\n" + long
    tail = "## 5. Abandoned Reasoning\n" + long + "\n## 6. Conclusion\n" + long
    checks = {
        "whole: one message carrying the document":
            classify_delivery(head + "\n" + tail, [{"text": head + "\n" + tail, "tools": []}])["status"] == "whole",
        "split: head stranded behind a tool call, only the tail delivered":
            classify_delivery(tail, [{"text": head, "tools": ["WebSearch"]},
                                     {"text": tail, "tools": []}])["status"] == "split",
        "interrupted: a 7-word hand-back":
            classify_delivery("[Request interrupted by user for tool use]",
                              [{"text": head, "tools": ["Read"]}])["status"] == "interrupted",
        "not split: short process chatter before a whole final document":
            classify_delivery(head + "\n" + tail, [{"text": "Reading the template now.", "tools": ["Read"]},
                                                   {"text": head + "\n" + tail, "tools": []}])["status"] == "whole",
        "abandoned is not split: no contract in the agent's own text either":
            (lambda r: r["status"] == "whole" and r["abandoned"])(
                classify_delivery("# My outline\n" + long, [{"text": "# My outline\n" + long, "tools": []}])),
        "delegation calls are counted":
            classify_delivery(tail, [{"text": "", "tools": ["Agent", "SendMessage"]},
                                     {"text": tail, "tools": []}])["delegation_calls"] == ["Agent", "SendMessage"],
    }
    ok = all(checks.values())
    for name, v in checks.items():
        print(f"  {'PASS' if v else 'FAIL'}  {name}")
    print(f"delivery --self-test: {'PASS' if ok else 'FAIL'} ({len(checks)} controls)")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("command", nargs="?", choices=("plan", "run", "read"))
    ap.add_argument("--body", type=Path)
    ap.add_argument("--cwd", type=Path)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if a.command == "plan":
        return cmd_plan()
    if a.command == "read":
        return cmd_read()
    if a.command == "run":
        if not (a.body and a.cwd):
            ap.error("run needs --body and --cwd")
        return cmd_run(a.body.resolve(), a.cwd.resolve())
    ap.error("a command or --self-test is required")


if __name__ == "__main__":
    sys.exit(main())
