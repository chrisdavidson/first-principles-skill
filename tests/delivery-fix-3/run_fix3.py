#!/usr/bin/env python3
"""delivery-fix-3 -- the re-run pre-registered in docs/delivery-fix-3-preregistration.md.

    python3 tests/delivery-fix-3/run_fix3.py run --body <wt>/first-principles --cwd <empty dir>
    python3 tests/delivery-fix-3/run_fix3.py read
    python3 tests/delivery-fix-3/run_fix3.py --self-test

v3 delivers the analysis as a file the agent appends to, one section per Bash call. Per run
this reads: the file (moved out of the working directory into raw/<run>.files/), the heredoc
payloads the agent issued (from its own transcript), and whether the main session read the
file. Transport and capture reuse the delivery runner. A measurement tool, never a gate.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
RAW = HERE / "raw"

spec = importlib.util.spec_from_file_location("_dlf3", REPO_ROOT / "tests/delivery/run_delivery.py")
dl = importlib.util.module_from_spec(spec)
sys.modules["_dlf3"] = dl
spec.loader.exec_module(dl)
p1, w4, p0, stage_a = dl.p1, dl.w4, dl.p0, dl.stage_a

# --- pre-registered protocol --------------------------------------------------------------
PROMPTS = ["TB-02", "TB-03", "TB-04", "TB-06"]
REPEATS = (1, 2, 3)
CONTRACT = len(stage_a.SECTIONS)          # 6
# ------------------------------------------------------------------------------------------

_APPEND = re.compile(r"cat\s+>>\s*\"?([^\"\s]+)\"?\s*<<\s*'FP_EOF'\n(.*?)\nFP_EOF", re.S)


def appended_payloads(agent_dir: Path) -> tuple[list[str], int]:
    """(heredoc bodies of every executed append, in order; max_tokens stops in the transcript)."""
    bodies, cutoffs = [], 0
    for f in sorted(agent_dir.glob("agent-*.jsonl")):
        for obj in p0._events(f.read_text(encoding="utf-8")):
            msg = obj.get("message", {})
            if obj.get("type") != "assistant":
                continue
            cutoffs += msg.get("stop_reason") == "max_tokens"
            for b in msg.get("content", []) or []:
                if isinstance(b, dict) and b.get("type") == "tool_use" and b.get("name") == "Bash":
                    for m in _APPEND.finditer(str(b.get("input", {}).get("command", ""))):
                        bodies.append(m.group(2))
    return bodies, cutoffs


def caller_read(jsonl: str, filename: str) -> tuple[bool, int]:
    """(did the MAIN session read the file?, words it received from that read)."""
    ids, words = set(), 0
    for obj in p0._events(jsonl):
        if obj.get("parent_tool_use_id"):
            continue
        for b in obj.get("message", {}).get("content", []) or []:
            if not isinstance(b, dict):
                continue
            if obj.get("type") == "assistant" and b.get("type") == "tool_use":
                inp = json.dumps(b.get("input", {}))
                if filename in inp and b.get("name") in ("Read", "Bash"):
                    ids.add(b.get("id"))
            if obj.get("type") == "user" and b.get("type") == "tool_result" and b.get("tool_use_id") in ids:
                c = b.get("content")
                text = c if isinstance(c, str) else " ".join(
                    x.get("text", "") for x in c or [] if isinstance(x, dict))
                words += len(text.split())
    return bool(ids), words


def judge(file_text: str | None, bodies: list[str], read: bool) -> dict:
    if file_text is None:
        return {"file": False, "sections": 0, "verbatim": False, "caller_read": read,
                "delivered": False}
    joined = "\n".join(bodies)
    norm = lambda s: re.sub(r"\s+", " ", s).strip()
    sections = len(stage_a.sections_present(file_text))
    verbatim = bool(bodies) and norm(joined) == norm(file_text)
    return {"file": True, "sections": sections, "verbatim": verbatim, "caller_read": read,
            "file_words": len(file_text.split()), "appends": len(bodies),
            "delivered": sections >= CONTRACT and verbatim and read}


def collect_files(cwd: Path, dest: Path) -> list[Path]:
    src = cwd / ".first-principles"
    out = []
    if src.is_dir():
        dest.mkdir(parents=True, exist_ok=True)
        for f in sorted(src.glob("*.md")):
            shutil.move(str(f), dest / f.name)
            out.append(dest / f.name)
        shutil.rmtree(src, ignore_errors=True)
    for leftover in cwd.iterdir():                  # keep the next run's cwd empty
        shutil.rmtree(leftover, ignore_errors=True) if leftover.is_dir() else leftover.unlink()
    return out


def row(key: str, cell: dict) -> dict:
    base = RAW / cell["scored"].replace(".jsonl", "")
    files = sorted(Path(str(base) + ".files").glob("*.md"))
    f = max(files, key=lambda p: p.stat().st_size) if files else None
    bodies, cutoffs = appended_payloads(Path(str(base) + ".agent"))
    read, read_words = caller_read((RAW / cell["scored"]).read_text(encoding="utf-8"),
                                   f.name if f else "\0")
    j = judge(f.read_text(encoding="utf-8") if f else None, bodies, read)
    received, _ = dl.received_by_caller((RAW / cell["scored"]).read_text(encoding="utf-8"))
    j.update(cutoffs=cutoffs, files=len(files), read_words=read_words,
             pointer_words=len(received.split()),
             fallback_sections=len(stage_a.sections_present(received)))
    return j


def cmd_run(body: Path, cwd: Path) -> int:
    if any(cwd.iterdir()):
        raise SystemExit(f"--cwd {cwd} is not empty")
    RAW.mkdir(parents=True, exist_ok=True)
    cells_path = HERE / "cells.json"
    cells = json.loads(cells_path.read_text()) if cells_path.is_file() else {}
    texts = {pid: p1.prompt_text(pid, dl.CATALOG) for pid in PROMPTS}
    for pid in PROMPTS:
        for r in REPEATS:
            key = f"{pid}.r{r}"
            if key in cells:
                print(f"[gen] {key} (recorded)", flush=True)
                continue
            attempts, outcome = [], "exhausted"
            for n in range(1, dl.MAX_ATTEMPTS + 1):
                raw = RAW / f"{key}.a{n}.jsonl"
                print(f"[gen] {key} attempt {n} ...", flush=True)
                jsonl = dl.generate(texts[pid], body, cwd, raw)
                dl.capture_agent_transcripts(jsonl, RAW / f"{key}.a{n}.agent")
                collect_files(cwd, RAW / f"{key}.a{n}.files")
                if w4.is_limit_stub(jsonl):
                    raw.rename(RAW / f"{key}.a{n}.limit-stub.jsonl")
                    print(f"[pause] {key}: usage-limit stub; re-run to resume", flush=True)
                    return 3
                if w4.loaded_body(jsonl) != [str(body)]:
                    print(f"[abort] {key}: loaded {w4.loaded_body(jsonl)}", flush=True)
                    return 5
                attempts.append(raw.name)
                r1 = p1.classify(raw, "fix")
                if not r1["dispatched"]:
                    print(f"[miss] {key} attempt {n}", flush=True)
                    continue
                outcome = "scored"
                break
            cells[key] = {"outcome": outcome, "attempts": attempts,
                          "scored": attempts[-1] if outcome == "scored" else None}
            cells_path.write_text(json.dumps(cells, indent=2) + "\n", encoding="utf-8")
            if outcome == "scored":
                j = row(key, cells[key])
                print(f"[gen] {key} {'DELIVERED' if j['delivered'] else 'NOT-DELIVERED'} "
                      f"file={j['file']} sections={j['sections']} verbatim={j['verbatim']} "
                      f"read={j['caller_read']} cutoffs={j['cutoffs']}", flush=True)
            else:
                print(f"[gen] {key} EXHAUSTED", flush=True)
    return cmd_read()


def cmd_read() -> int:
    cells = json.loads((HERE / "cells.json").read_text())
    rows = {k: row(k, v) for k, v in cells.items() if v["outcome"] == "scored"}
    print("delivery-fix-3 -- reading (a recorded reading with its N, never a gate)\n")
    print(f"{'run':<9}{'file':>6}{'sections':>9}{'verbatim':>9}{'read':>6}{'words':>7}{'appends':>8}"
          f"{'cutoffs':>8}{'pointer w':>10}  verdict")
    for k, r in rows.items():
        print(f"{k:<9}{str(r['file']):>6}{r['sections']:>9}{str(r['verbatim']):>9}"
              f"{str(r['caller_read']):>6}{r.get('file_words', 0):>7}{r.get('appends', 0):>8}"
              f"{r['cutoffs']:>8}{r['pointer_words']:>10}  {'DELIVERED' if r['delivered'] else 'NOT DELIVERED'}")
    ok = [k for k, r in rows.items() if r["delivered"]]
    cut = [k for k, r in rows.items() if r["cutoffs"]]
    verdict = ("OPERATIONAL -- every run delivered the complete, verbatim file to the caller"
               if rows and len(ok) == len(rows) else
               "NOT OPERATIONAL -- a run did not deliver the complete, verbatim file to the caller")
    print(f"\ndelivered {len(ok)}/{len(rows)}   runs with a cut-off {len(cut)} {cut or ''}"
          f"   exhausted {sum(v['outcome'] == 'exhausted' for v in cells.values())}")
    print(f"VERDICT  {verdict}")
    (HERE / "result.json").write_text(json.dumps(
        {"rows": rows, "delivered": ok, "cutoffs": cut, "verdict": verdict}, indent=2) + "\n",
        encoding="utf-8")
    return 0


def self_test() -> int:
    doc = "\n".join(f"## {i}. {s}\ntext {i}" for i, s in enumerate(stage_a.SECTIONS, 1))
    parts = doc.split("\n## ")
    bodies = [parts[0]] + ["## " + p for p in parts[1:]]
    cmd = lambda b: f"cat >> \".first-principles/a.md\" <<'FP_EOF'\n{b}\nFP_EOF"
    checks = {
        "heredoc payloads are extracted in order":
            [m.group(2) for c in map(cmd, bodies) for m in _APPEND.finditer(c)] == bodies,
        "a complete, verbatim, read file is DELIVERED":
            judge(doc, bodies, True)["delivered"],
        "an unread file is NOT delivered":
            not judge(doc, bodies, False)["delivered"],
        "a file that differs from what was appended is NOT verbatim":
            not judge(doc.replace("text 3", "rewritten"), bodies, True)["verbatim"],
        "a file missing a section is NOT delivered":
            not judge("\n".join(bodies[:-1]), bodies[:-1], True)["delivered"],
        "no file is NOT delivered":
            not judge(None, [], True)["delivered"],
    }
    for name, v in checks.items():
        print(f"  {'PASS' if v else 'FAIL'}  {name}")
    ok = all(checks.values())
    print(f"delivery-fix-3 --self-test: {'PASS' if ok else 'FAIL'} ({len(checks)} controls)")
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
