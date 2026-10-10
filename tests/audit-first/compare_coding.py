#!/usr/bin/env python3
"""Compare the tracked rewrite coding with readings.json's rewrite_split.

    python3 tests/audit-first/compare_coding.py [--tsv PATH] [--readings PATH]
    python3 tests/audit-first/compare_coding.py --self-test

Sums rewrite_cmds by (run, position) and requires each run's three sums to equal that run's
readings.json rewrite_split. Exits 1 on any difference or on a run readings.json does not know.
A measurement tool, never a gate.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
TSV = HERE / "postheld-coding.tsv"
READINGS = HERE / "readings.json"
POS = {"pre-held": "pre_held", "held-to-gate": "post_held_pre_gate", "post-gate": "post_gate"}


def load_tsv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def compare(tsv: Path, readings: Path, quiet: bool = False) -> int:
    rows = load_tsv(tsv)
    known = {r["key"]: r["rewrite_split"] for r in json.loads(readings.read_text())}
    sums: dict[str, Counter] = defaultdict(Counter)
    tot: Counter = Counter()
    hand: Counter = Counter()
    bad = 0
    for r in rows:
        n = int(r["rewrite_cmds"])
        pos = r["position"]
        if r["run"] not in known or pos not in POS:
            if not quiet:
                print(f"UNKNOWN run/position: {r['run']} {pos}")
            bad += 1
            continue
        sums[r["run"]][POS[pos]] += n
        tot[pos] += n
        if r["coder"] == "hand":
            hand[r["trigger"]] += n
    for key, split in sorted(known.items()):
        got = {k: sums[key].get(k, 0) for k in POS.values()}
        if got != split:
            bad += 1
            if not quiet:
                print(f"DIFF {key}: tsv {got} readings {split}")
    if not quiet:
        print(
            f"TOTAL {sum(tot.values())} pre-held {tot['pre-held']} "
            f"held-to-gate {tot['held-to-gate']} post-gate {tot['post-gate']}"
        )
        for t, n in hand.most_common():
            print(f"  hand {t}: {n}")
        print(f"HAND {sum(hand.values())}")
    return 1 if bad else 0


def self_test() -> bool:
    ok = True

    def check(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  {'PASS' if cond else 'FAIL'}: {name}")
        ok = ok and cond

    check("tracked files: 0 diffs", compare(TSV, READINGS, quiet=True) == 0)
    rows = load_tsv(TSV)
    check("total 75", sum(int(r["rewrite_cmds"]) for r in rows) == 75)
    split = Counter()
    hand = 0
    for r in rows:
        split[r["position"]] += int(r["rewrite_cmds"])
        hand += int(r["rewrite_cmds"]) if r["coder"] == "hand" else 0
    check("split 2/58/15", (split["pre-held"], split["held-to-gate"], split["post-gate"]) == (2, 58, 15))
    check("HAND 40", hand == 40)
    header = TSV.read_text().splitlines()[0].split("\t")
    with tempfile.TemporaryDirectory() as d:
        base = TSV.read_text().splitlines()

        def mutated(edit) -> Path:
            lines = [ln.split("\t") for ln in base]
            edit(lines)
            p = Path(d) / "m.tsv"
            p.write_text("\n".join("\t".join(x) for x in lines) + "\n")
            return p

        i = header.index("rewrite_cmds")

        def plus(lines):
            lines[1][i] = str(int(lines[1][i]) + 1)

        def unknown(lines):
            lines[1][header.index("run")] = "N.no-such-run.r9"

        check("mutation +1 exits 1", compare(mutated(plus), READINGS, quiet=True) == 1)
        check("mutation unknown run exits 1", compare(mutated(unknown), READINGS, quiet=True) == 1)
    print(f"compare_coding --self-test: {'PASS' if ok else 'FAIL'}")
    return ok


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tsv", type=Path, default=TSV)
    ap.add_argument("--readings", type=Path, default=READINGS)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return 0 if self_test() else 1
    return compare(a.tsv, a.readings)


if __name__ == "__main__":
    sys.exit(main())
