#!/usr/bin/env python3
"""skip-paired -- does the current body skip its procedure more often than v9.13.0's?

    python3 tests/skip-paired/run_paired.py run --old <dir>/first-principles --new <dir>/first-principles --cwd <empty dir>
    python3 tests/skip-paired/run_paired.py read

Protocol: docs/skip-paired-preregistration.md. Transport and capture reuse
tests/example-rerun-2/run_examples.py unchanged; only the output paths and the schedule differ.
A measurement, never a gate.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
spec = importlib.util.spec_from_file_location("_er2p", REPO_ROOT / "tests/example-rerun-2/run_examples.py")
er = importlib.util.module_from_spec(spec)
sys.modules["_er2p"] = er
spec.loader.exec_module(er)
er.HERE, er.RAW, er.DOCS = HERE, HERE / "raw", HERE / "documents"

PROMPT_NAMES = ("decompose-irreducibility", "personal-general-2", "product-business")
REPEATS = (1, 2, 3)
ALL_PROMPTS = json.loads((REPO_ROOT / "tests/example-rerun-2/prompts.json").read_text(encoding="utf-8"))


def schedule() -> list[tuple[str, str]]:
    """(cell, arm) in run order: arm order alternates within each pair and flips per repeat."""
    out, flip = [], False
    for r in REPEATS:
        for name in PROMPT_NAMES:
            arms = ("new", "old") if flip else ("old", "new")
            out += [(f"{name}.{arm}.r{r}", arm) for arm in arms]
            flip = not flip
    return out


def run(bodies: dict[str, Path], cwd: Path) -> int:
    for cell, arm in schedule():
        er.PROMPTS = {cell: ALL_PROMPTS[cell.split(".")[0]]}
        rc = er.run(bodies[arm], cwd)
        if rc:
            return rc
    return 0


def _reads_template(agent_dir: Path) -> bool:
    for f in agent_dir.glob("agent-*.jsonl"):
        for line in f.read_text(encoding="utf-8").splitlines():
            o = json.loads(line)
            if o.get("type") != "assistant":
                continue
            for b in o["message"].get("content") or []:
                if (isinstance(b, dict) and b.get("type") == "tool_use" and b.get("name") == "Read"
                        and str(b.get("input", {}).get("file_path", "")).endswith("output-template.md")):
                    return True
    return False


def _fisher_one_sided(a_skip: int, a_n: int, b_skip: int, b_n: int) -> float:
    """P(new arm has >= b_skip skips | total skips fixed), hypergeometric."""
    k, n = a_skip + b_skip, a_n + b_n
    return sum(comb(b_n, x) * comb(a_n, k - x) for x in range(b_skip, min(k, b_n) + 1)) / comb(n, k)


def read() -> int:
    cells = json.loads((HERE / "cells.json").read_text())
    tally = {"old": [0, 0], "new": [0, 0]}
    print(f"{'cell':40} {'outcome':14} file  template  SKIP")
    for cell, arm in schedule():
        c = cells.get(cell)
        if not c or c["outcome"] == "exhausted":
            print(f"{cell:40} {'(not run)' if not c else 'exhausted':14}")
            continue
        last = c["attempts"][-1].removesuffix(".jsonl")
        has_file = c["outcome"] == "file"
        tmpl = _reads_template(HERE / "raw" / f"{last}.agent")
        skip = (not has_file) or (not tmpl)
        tally[arm][0] += skip
        tally[arm][1] += 1
        print(f"{cell:40} {c['outcome']:14} {'Y' if has_file else '-':5} {'Y' if tmpl else '-':9} {'SKIP' if skip else ''}")
    (o, on), (n, nn) = tally["old"], tally["new"]
    print(f"\nold (v9.13.0) skips {o}/{on}   new (2628e725) skips {n}/{nn}")
    if on and nn:
        print(f"Fisher one-sided p (new > old) = {_fisher_one_sided(o, on, n, nn):.3f}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=("run", "read"))
    ap.add_argument("--old", type=Path)
    ap.add_argument("--new", type=Path)
    ap.add_argument("--cwd", type=Path)
    a = ap.parse_args()
    if a.command == "read":
        return read()
    if not (a.old and a.new and a.cwd):
        ap.error("run needs --old, --new and --cwd")
    return run({"old": a.old.resolve(), "new": a.new.resolve()}, a.cwd.resolve())


if __name__ == "__main__":
    sys.exit(main())
