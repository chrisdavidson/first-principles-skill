#!/usr/bin/env python3
"""phase-turns -- where the agent's 60-turn budget goes, read from captured transcripts.

    python3 tests/skip-rate/phase_turns.py            # table over every capture set
    python3 tests/skip-rate/phase_turns.py --runs     # one line per run

No run is made. A turn is one distinct assistant message (`message.id`) in the agent's own
transcript -- the unit `maxTurns` counts: the main session's "you hit the turn limit" message
arrives at exactly the 60th. Phase milestones are read from the Bash calls the delivery steps
prescribe: the file's creation, each heredoc append (named by its first heading), the assembly,
the reader report, the PDF, the figures and the final `pwd -P` pointer. A measurement tool,
never a gate.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from statistics import median

REPO = Path(__file__).resolve().parents[2]
CAP = 60
CORPORA = {
    "skip-rate A (9.19.2)": ("tests/skip-rate/raw", "A."),
    "skip-rate B (9.19.3)": ("tests/skip-rate/raw", "B."),
    "pointer-fix": ("tests/pointer-fix/raw", ""),
    "example-rerun-2": ("tests/example-rerun-2/raw", ""),
    "skip-paired new": ("tests/skip-paired/raw", ".new."),
}
# Milestones in the order the body prescribes them.
MILESTONES = (
    "create",
    "s1", "s2", "s3", "s4", "s5", "s6",
    "gate", "answer", "assemble", "report", "pdf", "figures", "pointer",
)  # fmt: skip
_HEREDOC = re.compile(r"<<\s*'FP_EOF'\n(.*)", re.S)
_SECTION = re.compile(r"^## ([1-6])\. ", re.M)
# A rewrite: the agent editing its own analysis file in place through the shell (it holds no
# Write/Edit tool) -- splitting and re-splicing it, `sed -i`, or a python find-and-replace.
# The prescribed appends and the prescribed assembly are not rewrites.
_REWRITE = re.compile(
    r"sed -i|sed -n[^|]*>\s*\"?\$F|\.part\d|\$F\.p\d|\$F\.[ab]\b|open\([^)]*['\"]w['\"]|write_text"
    r"|mv \"\$F\.tmp\" \"\$F\""
)


def is_rewrite(cmd: str) -> bool:
    if "FP_EOF" in cmd and "cat >>" in cmd:
        return False
    if ".answer" in cmd and ".process" in cmd:
        return False
    return bool(_REWRITE.search(cmd)) and "analysis-" in cmd + "$F"


def classify(cmd: str) -> list[str]:
    hits = []
    if "mkdir -p .first-principles" in cmd and "analysis-$(date" in cmd:
        hits.append("create")
    m = _HEREDOC.search(cmd)
    if m:
        body = m.group(1)
        first = next((ln for ln in body.splitlines() if ln.startswith("#")), "")
        s = _SECTION.match(first)
        if s:
            hits.append(f"s{s.group(1)}")
        elif first.startswith("## Self-Audit Gate"):
            hits.append("gate")
        elif first.startswith("## Answer") or (".answer" in cmd.split("<<")[0] and "cat >" in cmd):
            hits.append("answer")
    if ".answer" in cmd and "mv " in cmd and ".tmp" in cmd:
        hits.append("assemble")
    if "report-${F##*/analysis-}" in cmd or ("report-" in cmd and "Executive Summary" in cmd):
        hits.append("report")
    if "pandoc" in cmd and ".pdf" in cmd:
        hits.append("pdf")
    if "typst compile" in cmd and "fig" in cmd:
        hits.append("figures")
    if "pwd -P" in cmd:
        hits.append("pointer")
    return hits


def read_run(agent_dir: Path) -> dict | None:
    files = sorted(agent_dir.glob("agent-*.jsonl"))
    if not files:
        return None
    ids: list[str] = []
    first: dict[str, int] = {}
    coordinator = guard = None
    rewrites = 0
    for f in files:
        for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                o = json.loads(line)
            except ValueError:
                continue
            msg = o.get("message") or {}
            if o.get("type") == "assistant":
                mid = msg.get("id") or f"{f.name}:{len(ids)}"
                if mid not in ids:
                    ids.append(mid)
                for b in msg.get("content") or []:
                    if isinstance(b, dict) and b.get("type") == "tool_use" and b.get("name") == "Bash":
                        rewrites += is_rewrite((b.get("input") or {}).get("command", ""))
                        for h in classify((b.get("input") or {}).get("command", "")):
                            # `pwd -P` also appears in early exploration; the pointer is the
                            # one printed after the reader report exists.
                            if h == "pointer" and "report" not in first:
                                continue
                            first.setdefault(h, len(ids))
            elif o.get("type") == "user":
                c = msg.get("content")
                text = c if isinstance(c, str) else " ".join(
                    b.get("text", "") for b in c or [] if isinstance(b, dict) and b.get("type") == "text"
                )  # fmt: skip
                if coordinator is None and "coordinator sent a message" in text:
                    coordinator = len(ids)
                if guard is None and "Stop hook feedback" in text and "delivery guard" in text:
                    guard = len(ids)
    return {"turns": len(ids), "first": first, "coordinator": coordinator, "guard": guard, "rewrites": rewrites}


def runs():
    for label, (rel, tag) in CORPORA.items():
        for agent_dir in sorted((REPO / rel).glob("*.agent")):
            if tag and tag not in agent_dir.name and not agent_dir.name.startswith(tag):
                continue
            r = read_run(agent_dir)
            if r:
                r["corpus"], r["run"] = label, agent_dir.name[: -len(".agent")]
                yield r


def main() -> int:
    rows = list(runs())
    if "--runs" in sys.argv:
        for r in rows:
            ms = " ".join(f"{m}={r['first'][m]}" for m in MILESTONES if m in r["first"])
            print(f"{r['corpus']:<22} {r['run']:<42} turns={r['turns']:<4} {ms}"
                  f"{' coord=' + str(r['coordinator']) if r['coordinator'] else ''}"
                  f"{' guard=' + str(r['guard']) if r['guard'] else ''}")  # fmt: skip
        return 0
    full = [r for r in rows if "pointer" in r["first"] or "figures" in r["first"]]
    print(f"phase-turns: {len(rows)} agent transcripts, {len(full)} reached the end of delivery\n")
    print("Turn at which each milestone is first reached (runs that reached it):")
    print(f"  {'milestone':<10} {'n':>3} {'median':>7} {'p75':>5} {'p90':>5} {'max':>5}  past cap")
    for m in MILESTONES:
        xs = sorted(r["first"][m] for r in rows if m in r["first"])
        if not xs:
            continue
        q = lambda p: xs[min(len(xs) - 1, int(p * len(xs)))]  # noqa: E731
        past = sum(x > CAP for x in xs)
        print(f"  {m:<10} {len(xs):>3} {median(xs):>7.0f} {q(0.75):>5} {q(0.9):>5} {xs[-1]:>5}  {past}")
    print("\nPhase widths (turns between milestones, runs with both ends):")
    spans = (
        ("research before the file", None, "create"),
        ("six sections", "create", "s6"),
        ("process blocks + Self-Audit Gate", "s6", "gate"),
        ("gate -> Answer", "gate", "answer"),
        ("Answer -> end of delivery", "answer", "pointer"),
    )
    for label, a, b in spans:
        xs = [r["first"][b] - (r["first"][a] if a else 0) for r in rows if b in r["first"] and (a is None or a in r["first"])]
        if xs:
            print(f"  {label:<34} n={len(xs):<3} median {median(xs):.0f}  max {max(xs)}")
    over = [r for r in rows if r["turns"] > CAP]
    coord = [r for r in rows if r["coordinator"]]
    print(f"\nRuns using more than {CAP} turns in all: {len(over)} of {len(rows)}")
    print(f"Runs the main session messaged mid-run: {len(coord)}; at turn {sorted(r['coordinator'] for r in coord)}")
    stuck = {}
    for r in coord:
        reached = [m for m in MILESTONES if m in r["first"] and r["first"][m] <= r["coordinator"]]
        stuck[r["run"]] = reached[-1] if reached else "before create"
    print(f"\nIn-place rewrites of the analysis file vs hitting the {CAP}-turn cap:")
    for lo, hi in ((0, 0), (1, 2), (3, 5), (6, 999)):
        g = [r for r in rows if lo <= r["rewrites"] <= hi]
        if g:
            capped = sum(bool(r["coordinator"] and r["coordinator"] >= CAP - 5) for r in g)
            print(f"  {lo}-{hi if hi < 999 else '+'} rewrites: {len(g):>3} runs, {capped:>2} capped "
                  f"({100 * capped / len(g):.0f}%), median turns {median(r['turns'] for r in g):.0f}")  # fmt: skip
    print("Last milestone reached when the main session stepped in:")
    for run, m in sorted(stuck.items()):
        print(f"  {run:<42} {m}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
