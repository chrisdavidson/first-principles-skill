#!/usr/bin/env python3
"""example-rerun -- re-run every worked example on v9.13.0 and compare it with the committed one.

    python3 tests/example-rerun/run_examples.py run --body <wt>/first-principles --cwd <empty dir>
    python3 tests/example-rerun/run_examples.py compare

Protocol: docs/example-rerun-protocol.md. Each example's prompt (prompts.json) carries the problem
and the user-supplied facts the committed example started from. A re-run's document is the file
the agent delivered (v9.13.0's file handoff), or its final message if it wrote none. `compare`
reads both documents with the repo's own instruments. A measurement, never a gate.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
RAW = HERE / "raw"
DOCS = HERE / "documents"
EXAMPLES = REPO_ROOT / "shared" / "examples"

spec = importlib.util.spec_from_file_location("_fx3er", REPO_ROOT / "tests/delivery-fix-3/run_fix3.py")
fx = importlib.util.module_from_spec(spec)
sys.modules["_fx3er"] = fx
spec.loader.exec_module(fx)
dl, stage_a, qh = fx.dl, fx.stage_a, fx.dl.p1.qh

PROMPTS = json.loads((HERE / "prompts.json").read_text(encoding="utf-8"))
MAX_ATTEMPTS = 3


def run(body: Path, cwd: Path) -> int:
    if any(cwd.iterdir()):
        raise SystemExit(f"--cwd {cwd} is not empty")
    RAW.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    cells_path = HERE / "cells.json"
    cells = json.loads(cells_path.read_text()) if cells_path.is_file() else {}
    for name, prompt in PROMPTS.items():
        if name in cells:
            print(f"[gen] {name} (recorded)", flush=True)
            continue
        outcome, attempts = "exhausted", []
        for n in range(1, MAX_ATTEMPTS + 1):
            raw = RAW / f"{name}.a{n}.jsonl"
            print(f"[gen] {name} attempt {n} ...", flush=True)
            jsonl = dl.generate(prompt, body, cwd, raw)
            dl.capture_agent_transcripts(jsonl, RAW / f"{name}.a{n}.agent")
            files = fx.collect_files(cwd, RAW / f"{name}.a{n}.files")
            if dl.w4.is_limit_stub(jsonl):
                raw.rename(RAW / f"{name}.a{n}.limit-stub.jsonl")
                print(f"[pause] {name}: usage-limit stub; re-run to resume", flush=True)
                return 3
            if dl.w4.loaded_body(jsonl) != [str(body)]:
                print(f"[abort] {name}: loaded {dl.w4.loaded_body(jsonl)}", flush=True)
                return 5
            attempts.append(raw.name)
            if not dl.p1.classify(raw, "rerun")["dispatched"]:
                print(f"[miss] {name} attempt {n}", flush=True)
                continue
            if files:
                doc, source = max(files, key=lambda p: p.stat().st_size).read_text(encoding="utf-8"), "file"
            else:
                doc, source = dl.received_by_caller(jsonl)[0], "final-message"
            (DOCS / f"{name}.md").write_text(doc, encoding="utf-8")
            outcome = source
            break
        cells[name] = {"outcome": outcome, "attempts": attempts}
        cells_path.write_text(json.dumps(cells, indent=2) + "\n", encoding="utf-8")
        print(f"[gen] {name} {outcome.upper()} "
              f"{len((DOCS / f'{name}.md').read_text().split()) if outcome != 'exhausted' else 0}w",
              flush=True)
    return 0


# ------------------------------------------------------------------ reading both documents

_GT = re.compile(r"\bGT-\d+\??")
_URL = re.compile(r"https?://")
_CONF = re.compile(r"\*\*Confidence:?\**:?\s*(?:\([^)]*\)\s*)?\**\s*(HIGH|MEDIUM|LOW)\b")


def metrics(doc: str) -> dict:
    m = {"words": len(doc.split()), "sections": len(stage_a.sections_present(doc)),
         "gt_ids": len({g.rstrip("?") for g in _GT.findall(doc)}),
         "gt_unverified": len({g for g in _GT.findall(doc) if g.endswith("?")}),
         "urls": len(_URL.findall(doc))}
    try:
        secs = qh._slice_sections(doc)
        d = qh.detect_defects(doc, "x")
        confs = _CONF.findall(secs[6])
        m.update(readable=True, chains=len(qh._chain_ids(secs[4])),
                 dead_ends=len(re.findall(r"^#{2,4}\s", secs[5], re.M)),
                 conclusion_confidence=(confs[-1].upper() if confs else None),
                 claims=d["conclusion_claims"], untraced=d["untraced_claims"],
                 chain_blocks=d["chain_blocks"], malformed=d["malformed_chain_blocks"],
                 verdict_cells=d["verdict_cells"], nonconforming=d["nonconforming_verdict_cells"],
                 confidence_inversions=d["confidence_inversions"],
                 precheck_disagreements=d["precheck_disagreements"])
    except qh.SectionResolutionError:
        m.update(readable=False)
    return m


def compare() -> int:
    cells = json.loads((HERE / "cells.json").read_text())
    rows = {}
    for name in PROMPTS:
        old = metrics((EXAMPLES / f"{name}.md").read_text(encoding="utf-8"))
        new = (metrics((DOCS / f"{name}.md").read_text(encoding="utf-8"))
               if cells.get(name, {}).get("outcome") in ("file", "final-message") else None)
        rows[name] = {"example": old, "rerun": new, "source": cells.get(name, {}).get("outcome")}
    keys = ("words", "sections", "gt_ids", "gt_unverified", "chains", "dead_ends", "urls",
            "untraced", "malformed", "nonconforming", "confidence_inversions", "conclusion_confidence")
    print("example-rerun -- committed example (old) vs v9.13.0 re-run (new)\n")
    for name, r in rows.items():
        o, n = r["example"], r["rerun"]
        print(f"== {name}  [{r['source']}]")
        if n is None:
            print("   no re-run document")
            continue
        for k in keys:
            if k in o or k in n:
                print(f"   {k:<24}{str(o.get(k, '-')):>10} -> {str(n.get(k, '-')):<10}")
        if not n.get("readable", True) or not o.get("readable", True):
            print(f"   readable: example={o.get('readable')} rerun={n.get('readable')}")
    tot = lambda side, k: sum((r[side] or {}).get(k, 0) or 0 for r in rows.values() if r["rerun"])
    print("\nTOTALS (examples with a re-run)")
    for k, den in (("untraced", "claims"), ("malformed", "chain_blocks"), ("nonconforming", "verdict_cells")):
        print(f"   {k:<14} old {tot('example', k)}/{tot('example', den)}   new {tot('rerun', k)}/{tot('rerun', den)}")
    (HERE / "comparison.json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=("run", "compare"))
    ap.add_argument("--body", type=Path)
    ap.add_argument("--cwd", type=Path)
    a = ap.parse_args()
    if a.command == "compare":
        return compare()
    if not (a.body and a.cwd):
        ap.error("run needs --body and --cwd")
    return run(a.body.resolve(), a.cwd.resolve())


if __name__ == "__main__":
    sys.exit(main())
