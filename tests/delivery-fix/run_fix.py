#!/usr/bin/env python3
"""delivery-fix -- the re-run pre-registered in docs/delivery-fix-preregistration.md.

    python3 tests/delivery-fix/run_fix.py run --body <wt>/first-principles --cwd <empty dir>
    python3 tests/delivery-fix/run_fix.py read
    python3 tests/delivery-fix/run_fix.py --self-test

Reuses the delivery runner's transport, capture and caller-channel reader; adds cut-off
detection (stop_reason=max_tokens in the agent's own transcript) and a fidelity ratio
against the document's first rendering. A measurement tool, never a gate.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
RAW = HERE / "raw"

spec = importlib.util.spec_from_file_location("_dlfx", REPO_ROOT / "tests/delivery/run_delivery.py")
dl = importlib.util.module_from_spec(spec)
sys.modules["_dlfx"] = dl
spec.loader.exec_module(dl)
p1, w4, p0, stage_a = dl.p1, dl.w4, dl.p0, dl.stage_a

# --- pre-registered protocol --------------------------------------------------------------
PROMPTS = ["TB-02", "TB-03", "TB-04", "TB-06"]
PASS1, PASS2 = (1, 2, 3), (4, 5, 6)
MIN_EVENTS = 3
FIDELITY = 0.90
# ------------------------------------------------------------------------------------------


def agent_turns(agent_dir: Path) -> list[dict]:
    """The agent's transcript as turns: assistant {text, tools, stop} and injected user text."""
    out = []
    for f in sorted(agent_dir.glob("agent-*.jsonl")):
        for obj in p0._events(f.read_text(encoding="utf-8")):
            msg = obj.get("message", {})
            content = msg.get("content")
            if obj.get("type") == "assistant":
                text = "\n".join(b.get("text", "") for b in content or []
                                 if isinstance(b, dict) and b.get("type") == "text").strip()
                tools = [b.get("name") for b in content or []
                         if isinstance(b, dict) and b.get("type") == "tool_use"]
                if text or tools:
                    out.append({"role": "agent", "text": text, "tools": tools,
                                "stop": msg.get("stop_reason")})
            elif obj.get("type") == "user":
                if isinstance(content, str) and content.strip():
                    out.append({"role": "user", "text": content})
                elif isinstance(content, list) and any(
                        isinstance(b, dict) and b.get("type") == "text" for b in content):
                    out.append({"role": "user", "text": " ".join(
                        b.get("text", "") for b in content if isinstance(b, dict))})
    return out


def first_rendering(turns: list[dict]) -> tuple[bool, str]:
    """(cut_off?, text of the document as first written across its continuation)."""
    idx = next((i for i, t in enumerate(turns) if t["role"] == "agent" and t.get("stop") == "max_tokens"), None)
    if idx is None:
        return False, ""
    parts = [turns[idx]["text"]]
    for t in turns[idx + 1:]:
        if t["role"] == "user":
            if t["text"].startswith("Output token limit hit"):
                continue                      # the harness's own resume prompt
            break                             # anything else sent to the agent ends it
        if t["tools"]:
            break
        parts.append(t["text"])
        if t.get("stop") != "max_tokens":
            break
    return True, "\n".join(p for p in parts if p)


def judge(received: str, turns: list[dict]) -> dict:
    cut, first = first_rendering(turns)
    fw, rw = len(first.split()), len(received.split())
    fs = set(stage_a.sections_present(first))
    rs = set(stage_a.sections_present(received))
    fidelity = (rw / fw) if fw else None
    return {
        "cut_off": cut,
        "first_words": fw, "received_words": rw,
        "fidelity": round(fidelity, 3) if fidelity is not None else None,
        "sections_first": len(fs), "sections_received": len(rs),
        "whole_with_fidelity": (not cut) or (fs <= rs and fidelity is not None and fidelity >= FIDELITY),
        "resend_cut_off": sum(1 for t in turns if t["role"] == "agent" and t.get("stop") == "max_tokens") > 1,
    }


def run_pass(repeats, body: Path, cwd: Path, cells: dict) -> int:
    texts = {pid: p1.prompt_text(pid, dl.CATALOG) for pid in PROMPTS}
    for pid in PROMPTS:
        for r in repeats:
            key = f"{pid}.r{r}"
            if key in cells:
                print(f"[gen] {key} (recorded)", flush=True)
                continue
            attempts, outcome = [], "exhausted"
            for n in range(1, dl.MAX_ATTEMPTS + 1):
                raw = RAW / f"{key}.a{n}.jsonl"
                if not raw.is_file():
                    print(f"[gen] {key} attempt {n} ...", flush=True)
                    jsonl = dl.generate(texts[pid], body, cwd, raw)
                    if w4.is_limit_stub(jsonl):
                        raw.rename(RAW / f"{key}.a{n}.limit-stub.jsonl")
                        print(f"[pause] {key}: usage-limit stub; re-run to resume", flush=True)
                        return 3
                    if w4.loaded_body(jsonl) != [str(body)]:
                        print(f"[abort] {key}: loaded {w4.loaded_body(jsonl)}", flush=True)
                        return 5
                    dl.capture_agent_transcripts(jsonl, RAW / f"{key}.a{n}.agent")
                attempts.append(raw.name)
                r1 = p1.classify(raw, "fix")
                if not r1["dispatched"]:
                    print(f"[miss] {key} attempt {n}", flush=True)
                    continue
                if r1["transport"]:
                    print(f"[transport] {key} attempt {n}", flush=True)
                    continue
                outcome = "scored"
                break
            cells[key] = {"outcome": outcome, "attempts": attempts,
                          "scored": attempts[-1] if outcome == "scored" else None}
            (HERE / "cells.json").write_text(json.dumps(cells, indent=2) + "\n", encoding="utf-8")
            if outcome == "scored":
                j = row(key, cells[key])
                tag = ("CUT-OFF " + ("WHOLE" if j["whole_with_fidelity"] else "LOST")) if j["cut_off"] else "NO-CUT"
                print(f"[gen] {key} {tag} fidelity={j['fidelity']}", flush=True)
            else:
                print(f"[gen] {key} EXHAUSTED", flush=True)
    return 0


def row(key: str, cell: dict) -> dict:
    raw = RAW / cell["scored"]
    turns = agent_turns(RAW / cell["scored"].replace(".jsonl", ".agent"))
    received, channel = dl.received_by_caller(raw.read_text(encoding="utf-8"))
    j = judge(received, turns)
    msgs = [{"text": t["text"], "tools": t.get("tools", [])} for t in turns if t["role"] == "agent"]
    j.update(dl.classify_caller(received, msgs), channel=channel, transcript=bool(turns))
    return j


def cmd_run(body: Path, cwd: Path) -> int:
    if any(cwd.iterdir()):
        raise SystemExit(f"--cwd {cwd} is not empty")
    RAW.mkdir(parents=True, exist_ok=True)
    cells_path = HERE / "cells.json"
    cells = json.loads(cells_path.read_text()) if cells_path.is_file() else {}
    rc = run_pass(PASS1, body, cwd, cells)
    if rc:
        return rc
    events = sum(row(k, v)["cut_off"] for k, v in cells.items() if v["outcome"] == "scored")
    if events < MIN_EVENTS:
        print(f"[pass2] only {events} cut-off events in pass 1 -- running pass 2", flush=True)
        rc = run_pass(PASS2, body, cwd, cells)
        if rc:
            return rc
    return cmd_read()


def cmd_read() -> int:
    cells = json.loads((HERE / "cells.json").read_text())
    rows = {k: row(k, v) for k, v in cells.items() if v["outcome"] == "scored"}
    print("delivery-fix -- reading (a recorded reading with its N, never a gate)\n")
    print(f"{'run':<9}{'cut-off':>8}{'first w':>9}{'recv w':>8}{'fidelity':>9}{'sec 1st':>8}"
          f"{'sec recv':>9}  verdict")
    for k, r in rows.items():
        v = ("WHOLE" if r["whole_with_fidelity"] else "LOST") if r["cut_off"] else \
            ("no cut-off, caller LOST sections" if r["caller_status"] == "lost" else "no cut-off, whole")
        print(f"{k:<9}{str(r['cut_off']):>8}{r['first_words']:>9}{r['received_words']:>8}"
              f"{str(r['fidelity']):>9}{r['sections_first']:>8}{r['sections_received']:>9}  {v}"
              f"{'  (re-send also cut off)' if r['resend_cut_off'] else ''}")
    events = [k for k, r in rows.items() if r["cut_off"]]
    good = [k for k in events if rows[k]["whole_with_fidelity"]]
    regress = [k for k, r in rows.items() if not r["cut_off"] and r["caller_status"] == "lost"]
    if len(events) < MIN_EVENTS:
        verdict = f"INCONCLUSIVE -- {len(events)} cut-off events (< {MIN_EVENTS}); the fix was not exercised"
    elif len(good) == len(events):
        verdict = "OPERATIONAL -- every cut-off event reached the caller whole, with fidelity"
    else:
        verdict = "NOT OPERATIONAL -- a cut-off event still lost the document"
    print(f"\ncut-off events {len(events)}/{len(rows)}; whole with fidelity {len(good)}/{len(events)}"
          f"   reference (pre-fix, same prompts, same judge): 0 of 6 whole")
    print(f"no-cut-off runs where the caller lost sections: {len(regress)} {regress or ''}")
    print(f"exhausted cells: {sum(v['outcome'] == 'exhausted' for v in cells.values())}"
          f"   runs missing the agent transcript: {[k for k, r in rows.items() if not r['transcript']] or 0}")
    print(f"VERDICT  {verdict}")
    (HERE / "result.json").write_text(json.dumps(
        {"rows": rows, "events": events, "whole": good, "regressions": regress,
         "verdict": verdict}, indent=2) + "\n", encoding="utf-8")
    return 0


def self_test() -> int:
    head = "## 1. Problem Essence\n" + " w" * 900 + "\n## 2. Assumptions Table\n" + " w" * 900
    tail = "## 3. Ground Truths\n" + " w" * 900 + "\n## 6. Conclusion\n" + " w" * 900
    full = head + "\n" + tail
    cut = [{"role": "agent", "text": head, "tools": [], "stop": "max_tokens"},
           {"role": "user", "text": "Output token limit hit. Resume directly"},
           {"role": "agent", "text": tail, "tools": [], "stop": "end_turn"}]
    checks = {
        "first rendering joins the cut message and its continuation":
            first_rendering(cut) == (True, head + "\n" + tail),
        "a tail-only delivery after a cut-off is LOST":
            not judge(tail, cut)["whole_with_fidelity"],
        "a verbatim re-send after a cut-off is WHOLE":
            judge(full, cut + [{"role": "agent", "text": full, "tools": [], "stop": "end_turn"}])["whole_with_fidelity"],
        "a summarised re-send (under 90% of the words) is LOST even with every section":
            not judge("## 1. Problem Essence\nx\n## 2. Assumptions Table\nx\n## 3. Ground Truths\nx\n## 6. Conclusion\nx",
                      cut)["whole_with_fidelity"],
        "a coordinator message ends the first rendering":
            first_rendering([cut[0], {"role": "user", "text": "The coordinator sent a message"}, cut[2]])
            == (True, head),
        "no max_tokens means no cut-off event":
            first_rendering([{"role": "agent", "text": full, "tools": [], "stop": "end_turn"}]) == (False, ""),
    }
    for name, ok in checks.items():
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    ok = all(checks.values())
    print(f"delivery-fix --self-test: {'PASS' if ok else 'FAIL'} ({len(checks)} controls)")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("command", nargs="?", choices=("run", "read"))
    ap.add_argument("--body", type=Path)
    ap.add_argument("--cwd", type=Path)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if a.command == "read":
        return cmd_read()
    if a.command == "run":
        if not (a.body and a.cwd):
            ap.error("run needs --body and --cwd")
        return cmd_run(a.body.resolve(), a.cwd.resolve())
    ap.error("a command or --self-test is required")


if __name__ == "__main__":
    sys.exit(main())
