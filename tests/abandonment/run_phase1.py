#!/usr/bin/env python3
"""abandonment Phase 1 -- the A/B pre-registered in docs/abandonment-preregistration.md section 5.

    python3 tests/abandonment/run_phase1.py plan
    python3 tests/abandonment/run_phase1.py run --control <wt>/first-principles \\
                                                --fix <wt>/first-principles --cwd <empty dir>
    python3 tests/abandonment/run_phase1.py read

Every protocol constant is the pre-registration's. `run` is resumable: a cell whose outcome is
already recorded is skipped. A measurement tool, never a gate.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
OUT = HERE / "phase1"
RAW = OUT / "raw"
DOCS = OUT / "documents"


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, REPO_ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


w4 = _load("_w4p1", "tests/w4-paired/run_paired.py")
p0 = _load("_p0p1", "tests/abandonment/phase0_reading.py")
stage_a, qh = w4.stage_a, w4.qh

# --- pre-registered protocol (section 5) ---------------------------------------------------
MODEL = "claude-sonnet-5"
ARMS = ("control", "fix")
PROMPTS = (
    [(f"TB-{i:02d}", "tests/trackb-catalog-v9.13.md") for i in range(1, 11)]
    + [(f"Q-N{i}", "tests/quality-catalog-v8.10-oos.md") for i in range(1, 7)]
    + [(f"Q-P{i}", "tests/quality-catalog-v8.7.md") for i in range(1, 4)]
    + [(f"QT-P{i}", "tests/quality-catalog-v9.12-technique.md") for i in range(1, 4)]
    + [(p, "tests/premise-rejection-catalog.md") for p in ("PR-P1", "PR-P2", "PR-N2")]
    + [(p, "tests/step0-fixture-catalog.md") for p in ("S-N02", "S-N04", "S-N07", "S-A08", "S-A12")]
)
MAX_ATTEMPTS = 3                 # a routing miss is retried at most twice
MAX_EXHAUSTED_PER_ARM = 5        # stop rule
DECISION_MAX_P = 0.10
GUARDRAIL_DOCS = 3
# -------------------------------------------------------------------------------------------


def prompt_text(pid: str, catalog: str) -> str:
    col = None
    for line in (REPO_ROOT / catalog).read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.split("|")]
        if col is None and len(cells) > 2 and cells[1] == "ID" and "Prompt" in cells:
            col = cells.index("Prompt")
        elif col is not None and len(cells) > col and cells[1] == pid:
            return cells[col]
    raise SystemExit(f"prompt {pid} not found in {catalog}")


def schedule() -> list[tuple[str, str]]:
    out = []
    for i, (pid, _) in enumerate(PROMPTS):
        order = ARMS if i % 2 == 0 else ARMS[::-1]
        out.extend((pid, arm) for arm in order)
    return out


def generate(text: str, plugin_dir: Path, cwd: Path, raw_path: Path) -> str:
    argv = ["claude", "-p", "--model", MODEL, "--plugin-dir", str(plugin_dir),
            "--output-format", "stream-json", "--verbose", "--no-session-persistence",
            "--permission-mode", "bypassPermissions", text]
    env = {**os.environ, "CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS": "0"}
    proc = subprocess.run(argv, capture_output=True, text=True, timeout=5400, env=env, cwd=cwd)
    raw_path.write_text(proc.stdout, encoding="utf-8")
    return proc.stdout


def classify(raw_path: Path, arm: str) -> dict:
    """One attempt, read with Phase 0's definitions (section 2)."""
    r = p0.read_attempt(raw_path, arm)
    jsonl = raw_path.read_text(encoding="utf-8")
    if r["dispatched"] and not r["transport"]:
        doc, _, _ = w4.extract(jsonl)
        if not doc.strip():
            doc = p0.legacy_handback(jsonl)
        r["words"] = len(doc.split())
        r["_doc"] = doc
    return r


def truncated_handback(raw_path: Path, doc: str) -> bool:
    """A document delivered only as its TAIL -- reported, never decisive.

    Seen first on TB-04.fix: the subagent used tools and read the template, streamed no text,
    and its hand-back began mid-section ("Speed is necessary but not sufficient.") with only
    Abandoned Reasoning and Conclusion present. The earlier part was written in a message the
    hand-back does not carry and the transcript does not stream. Mechanical and symmetric:
    no streamed subagent text, no Problem Essence, and the document's first non-blank line is
    not a heading -- it opens mid-flow. (A first draft tested for a SUFFIX of the six sections
    and missed TB-04.fix, whose tail mentions Ground Truths.) A reclassification here would
    favour the arm under test, so it feeds only a sensitivity reading, never the
    pre-registered decision.
    """
    streamed = False
    for obj in p0._events(raw_path.read_text(encoding="utf-8")):
        if obj.get("type") == "assistant" and obj.get("parent_tool_use_id"):
            for b in obj.get("message", {}).get("content", []) or []:
                if isinstance(b, dict) and b.get("type") == "text" and b.get("text", "").strip():
                    streamed = True
    first = next((ln.strip() for ln in doc.splitlines() if ln.strip()), "")
    opens_mid_flow = bool(first) and not first.startswith("#")
    no_opening = "Problem Essence" not in stage_a.sections_present(doc)
    return (not streamed) and no_opening and opens_mid_flow


def cmd_plan() -> int:
    s = schedule()
    print(f"abandonment Phase 1 -- plan (no spend): {len(PROMPTS)} prompts x {len(ARMS)} arms"
          f" = {len(s)} cells, model {MODEL}")
    for pid, cat in PROMPTS:
        print(f"  {pid:<7}{len(prompt_text(pid, cat).split()):>4} words  {cat}")
    return 0


def cmd_run(dirs: dict[str, Path], cwd: Path) -> int:
    if any(cwd.iterdir()):
        raise SystemExit(f"--cwd {cwd} is not empty (section 5 requires an empty directory)")
    RAW.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    texts = {pid: prompt_text(pid, cat) for pid, cat in PROMPTS}
    cells_path = OUT / "cells.json"
    cells = json.loads(cells_path.read_text()) if cells_path.is_file() else {}
    for pid, arm in schedule():
        key = f"{pid}.{arm}"
        if key in cells:
            print(f"[gen] {key} (recorded: {cells[key]['outcome']})", flush=True)
            continue
        attempts = []
        outcome = "exhausted"
        for n in range(1, MAX_ATTEMPTS + 1):
            raw = RAW / f"{key}.a{n}.jsonl"
            if not raw.is_file():
                print(f"[gen] {key} attempt {n} ...", flush=True)
                jsonl = generate(texts[pid], dirs[arm], cwd, raw)
                if w4.is_limit_stub(jsonl):
                    raw.rename(RAW / f"{key}.a{n}.limit-stub.jsonl")
                    print(f"[pause] {key}: usage-limit/transport stub; re-run to resume", flush=True)
                    return 3
                if w4.loaded_body(jsonl) != [str(dirs[arm])]:
                    print(f"[abort] {key}: loaded {w4.loaded_body(jsonl)}", flush=True)
                    return 5
            r = classify(raw, arm)
            attempts.append(raw.name)
            if not r["dispatched"]:
                print(f"[miss] {key} attempt {n}: never dispatched", flush=True)
                continue
            if r["transport"]:
                print(f"[transport] {key} attempt {n}", flush=True)
                continue
            outcome = "abandoned" if r["abandoned"] else "kept"
            (DOCS / f"{key}.md").write_text(r["_doc"], encoding="utf-8")
            break
        cells[key] = {"outcome": outcome, "attempts": attempts, "scored": attempts[-1]
                      if outcome != "exhausted" else None}
        cells_path.write_text(json.dumps(cells, indent=2) + "\n", encoding="utf-8")
        print(f"[gen] {key} {outcome.upper()}", flush=True)
        exhausted = sum(1 for k, v in cells.items()
                        if k.endswith("." + arm) and v["outcome"] == "exhausted")
        if exhausted > MAX_EXHAUSTED_PER_ARM:
            print(f"[stop] arm {arm}: {exhausted} cells exhausted their routing retries", flush=True)
            return 4
    return cmd_read()


def cmd_read() -> int:
    cells = json.loads((OUT / "cells.json").read_text())
    print("abandonment Phase 1 -- reading (a recorded reading with its N, never a gate)\n")
    stats = {}
    for arm in ARMS:
        mine = {k: v for k, v in cells.items() if k.endswith("." + arm)}
        scored = {k: v for k, v in mine.items() if v["outcome"] != "exhausted"}
        rows = {k: classify(RAW / v["scored"], arm) for k, v in scored.items()}
        misses = 0
        for v in mine.values():
            for a in v["attempts"]:
                misses += not p0.read_attempt(RAW / a, arm)["dispatched"]
        one = [k for k, r in rows.items() if r["one_shot"]]
        readable, a1, a2 = 0, 0, 0
        for k, v in scored.items():
            if v["outcome"] != "kept":
                continue
            try:
                d = qh.detect_defects((DOCS / f"{k}.md").read_text(encoding="utf-8"), k)
            except qh.SectionResolutionError:
                continue
            readable += 1
            a1 += d["malformed_chain_blocks"] > 0
            a2 += d["nonconforming_verdict_cells"] > 0
        stats[arm] = {
            "cells": len(mine), "scored": len(scored),
            "abandoned": sum(v["outcome"] == "abandoned" for v in scored.values()),
            "exhausted": len(mine) - len(scored), "routing_misses": misses,
            "one_shot": len(one),
            "abandoned_one_shot": sum(1 for k in one if scored[k]["outcome"] == "abandoned"),
            "template_read": sum(r["template_read"] for r in rows.values()),
            "readable": readable, "A1": a1, "A2": a2,
            "abandoned_cells": sorted(k for k, v in scored.items() if v["outcome"] == "abandoned"),
            # Amendment 3: a delivery failure is a truncated hand-back OR a run interrupted
            # before it wrote a document (under Stage A's word floor, e.g. the 7-word
            # "[Request interrupted by user for tool use]" of TB-08.fix). Sensitivity only.
            "truncated_cells": sorted(
                k for k, v in scored.items() if v["outcome"] == "abandoned"
                and (truncated_handback(RAW / v["scored"], rows[k].get("_doc", ""))
                     or len(rows[k].get("_doc", "").split()) < stage_a.MIN_WORDS)),
        }
    c, f = stats["control"], stats["fix"]
    p = w4.fisher_one_sided(f["abandoned"], f["scored"], c["abandoned"], c["scored"],
                            greater_first=False)
    reduces = f["scored"] and c["scored"] and \
        f["abandoned"] / f["scored"] < c["abandoned"] / c["scored"] and p <= DECISION_MAX_P
    reading = "fix reduces abandonment" if reduces else "no reduction detected at this N"
    guard_ok = (f["A1"] - c["A1"] < GUARDRAIL_DOCS) and (f["A2"] - c["A2"] < GUARDRAIL_DOCS)
    for arm in ARMS:
        s = stats[arm]
        print(f"{arm:<8} abandoned {s['abandoned']}/{s['scored']}  one-shot {s['one_shot']}"
              f"  abandoned|one-shot {s['abandoned_one_shot']}/{s['one_shot']}"
              f"  template-read {s['template_read']}  routing misses {s['routing_misses']}"
              f"  exhausted {s['exhausted']}  | A1 {s['A1']}/{s['readable']}"
              f"  A2 {s['A2']}/{s['readable']}")
        if s["abandoned_cells"]:
            print(f"         abandoned: {', '.join(s['abandoned_cells'])}")
    print(f"\nPRIMARY  abandonment fix {f['abandoned']}/{f['scored']} vs control "
          f"{c['abandoned']}/{c['scored']}  one-sided p={p:.3f}  -> {reading}")
    print(f"GUARDRAIL A1 {f['A1']} vs {c['A1']}, A2 {f['A2']} vs {c['A2']} "
          f"(fail at +{GUARDRAIL_DOCS})  -> {'PASS' if guard_ok else 'FAIL'}")
    tc, tf = len(c["truncated_cells"]), len(f["truncated_cells"])
    ps = w4.fisher_one_sided(f["abandoned"] - tf, f["scored"] - tf,
                             c["abandoned"] - tc, c["scored"] - tc, greater_first=False)
    print(f"SENSITIVITY (reported, never decisive) -- delivery failures (truncated or interrupted) excluded from both arms:"
          f" fix {f['abandoned'] - tf}/{f['scored'] - tf} vs control "
          f"{c['abandoned'] - tc}/{c['scored'] - tc}  p={ps:.3f}"
          f"  [delivery failures: fix {f['truncated_cells']}, control {c['truncated_cells']}]")
    ship = reduces and guard_ok
    print(f"PHASE 2  {'AUTHORISED' if ship else 'NOT AUTHORISED'}")
    (OUT / "result.json").write_text(json.dumps(
        {"stats": stats, "p_one_sided": round(p, 4), "reading": reading,
         "guardrail_pass": guard_ok, "phase2_authorised": bool(ship)}, indent=2) + "\n",
        encoding="utf-8")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=("plan", "run", "read"))
    ap.add_argument("--control", type=Path)
    ap.add_argument("--fix", type=Path)
    ap.add_argument("--cwd", type=Path)
    a = ap.parse_args()
    if a.command == "plan":
        return cmd_plan()
    if a.command == "read":
        return cmd_read()
    if not (a.control and a.fix and a.cwd):
        ap.error("run needs --control, --fix and --cwd")
    return cmd_run({"control": a.control.resolve(), "fix": a.fix.resolve()}, a.cwd.resolve())


if __name__ == "__main__":
    sys.exit(main())
