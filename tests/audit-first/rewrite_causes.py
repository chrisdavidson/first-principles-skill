#!/usr/bin/env python3
"""rewrite-causes -- which kind of in-place rewrite an agent made to its own analysis file.

    python3 tests/audit-first/rewrite_causes.py --self-test
    python3 tests/audit-first/rewrite_causes.py --against tests/audit-first/baseline-coding.tsv
    python3 tests/audit-first/rewrite_causes.py --dirs 'tests/audit-first/raw/*.agent'

A rewrite is a Bash command that edits the analysis file in place (the definition is
`phase_turns.is_rewrite`, imported unedited). Each one is assigned a category from text signals in
the command itself: AA, HOP, HEAD, BAND, QMARK, VERDICT, IDFMT, HEADINGS, PROC, S6, STRUCT,
CONTENT. The hand-coded table in baseline-coding.tsv grouped consecutive rewrites into episodes
(turn gap of at most 3) and named the cause of each by reading the transcripts; this module
reproduces the grouping and approximates the naming from text alone, so the category mix of a new
set of runs can be read without a person recoding it.

A reading aid, report-only, never a gate. Nothing imports it and nothing fails on what it prints.

Measured agreement (2026-10-10): 69 of 193 matched episodes agree (35.8%)
"""

from __future__ import annotations

import argparse
import glob
import importlib.util
import json
import re
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location(
    "phase_turns", REPO / "tests" / "skip-rate" / "phase_turns.py"
)
phase_turns = importlib.util.module_from_spec(_spec)
sys.modules["phase_turns"] = phase_turns
_spec.loader.exec_module(phase_turns)

CATEGORIES = (
    "AA",
    "HOP",
    "HEAD",
    "BAND",
    "QMARK",
    "VERDICT",
    "IDFMT",
    "HEADINGS",
    "CONTENT",
    "STRUCT",
    "PROC",
    "S6",
)

_PROC = re.compile(r"analysis-[^\s'\"]*\.process\b|\$F\.process\b|\.process['\"]")
_AA_ROW = re.compile(r"^\s*\|\s*A-\d+", re.MULTILINE)
_ASSUMES = re.compile(r"\[Assumes:")
_HOP_LINE = re.compile(r"^\s*→ (?:GT-|C\d)", re.MULTILINE)
_HEADINGS = re.compile(r"### Conclusion C|### Dead End:")
_VERDICT = re.compile(r"\b(?:Accept|Challenge|Discard)\b")
_QMARK = re.compile(r"GT-\d+\?")
_BAND = re.compile(
    r"\*\*(?:Confidence|Pre-check):\*\*[^\n]*?\b(?:HIGH|MEDIUM|LOW|ceiling)\b|\bceiling\b",
    re.IGNORECASE,
)
_HEAD = re.compile(r"\*\*Pre-check:\*\*|^\s*#+ .*\bChain\b|^\s*C\d+ head", re.MULTILINE)
_S6 = re.compile(r"^## 6\.", re.MULTILINE)

_PY_REPLACE = re.compile(
    r"\.replace\(\s*(?P<q1>'''|\"\"\"|'|\")(?P<old>.*?)(?<!\\)(?P=q1)\s*,\s*(?P<q2>'''|\"\"\"|'|\")(?P<new>.*?)(?<!\\)(?P=q2)",
    re.DOTALL,
)
_SED_SUB = re.compile(
    r"s(?P<d>[/|#,])(?P<old>(?:\\.|(?!(?P=d)).)*)(?P=d)(?P<new>(?:\\.|(?!(?P=d)).)*)(?P=d)"
)


def _pairs(cmd: str) -> list[tuple[str, str]]:
    """(old, new) text pairs the command applies; empty when none can be read."""
    out = [(m.group("old"), m.group("new")) for m in _PY_REPLACE.finditer(cmd)]
    if not out and "sed" in cmd:
        out = [(m.group("old"), m.group("new")) for m in _SED_SUB.finditer(cmd)]
    return out


def _count(rx: re.Pattern, text: str) -> int:
    return len(rx.findall(text))


def _changed(rx: re.Pattern, old: str, new: str) -> bool:
    return _count(rx, old) != _count(rx, new)


def classify_rewrite(cmd: str, context_text: str = "") -> str:
    """One category code for one rewrite command, checked in a fixed order."""
    if _PROC.search(cmd):
        return "PROC"
    pairs = _pairs(cmd) or [("", cmd)]
    old = "\n".join(p[0] for p in pairs)
    new = "\n".join(p[1] for p in pairs)
    if _changed(_AA_ROW, old, new) or _changed(_ASSUMES, old, new):
        return "AA"
    if (
        set(_HOP_LINE.findall(old)) != set(_HOP_LINE.findall(new))
        or _changed(_HOP_LINE, old, new)
        or (_HOP_LINE.search(old) and old != new)
    ):
        return "HOP"
    if _changed(_HEADINGS, old, new):
        return "HEADINGS"
    if old != new and (_VERDICT.search(old) or _VERDICT.search(new)):
        return "VERDICT"
    if (
        re.search(r"\bA\d+\b", old)
        and re.search(r"\bA-\d+\b", new)
        or re.search(r"GT-[A-Z]\b", old + new)
    ):
        return "IDFMT"
    if _changed(_QMARK, old, new):
        return "QMARK"
    if _BAND.search(old + new) and old != new:
        return "BAND"
    if _HEAD.search(old + new):
        return "HEAD"
    if _S6.search(cmd):
        return "S6"
    if (
        re.search(r"(?:>\s*\"?\$F\"?\b|write_text|open\([^)]*['\"]w['\"])", cmd)
        and ".part" in cmd
    ):
        return "STRUCT"
    return "CONTENT"


def rewrite_commands(agent_dir: Path) -> list[tuple[int, str]]:
    """(turn, command) for every rewrite in one run; turns counted as phase_turns.read_run counts them."""
    ids: list[str] = []
    out: list[tuple[int, str]] = []
    for f in sorted(Path(agent_dir).glob("agent-*.jsonl")):
        for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                o = json.loads(line)
            except ValueError:
                continue
            if o.get("type") != "assistant":
                continue
            msg = o.get("message") or {}
            mid = msg.get("id") or f"{f.name}:{len(ids)}"
            if mid not in ids:
                ids.append(mid)
            for b in msg.get("content") or []:
                if (
                    isinstance(b, dict)
                    and b.get("type") == "tool_use"
                    and b.get("name") == "Bash"
                ):
                    cmd = (b.get("input") or {}).get("command", "")
                    if phase_turns.is_rewrite(cmd):
                        out.append((len(ids), cmd))
    return out


def episodes(cmds: list[tuple[int, str]], gap: int = 3) -> list[list[tuple[int, str]]]:
    groups: list[list[tuple[int, str]]] = []
    for item in cmds:
        if groups and item[0] - groups[-1][-1][0] <= gap:
            groups[-1].append(item)
        else:
            groups.append([item])
    return groups


def classify_episode(ep: list[tuple[int, str]]) -> str:
    cats = [classify_rewrite(c) for _, c in ep]
    counts = Counter(cats)
    best = max(counts.values())
    return next(c for c in cats if counts[c] == best)


def baseline_runs() -> dict[tuple[str, str], Path]:
    out = {}
    for label, (rel, tag) in phase_turns.CORPORA.items():
        for d in sorted((REPO / rel).glob("*.agent")):
            if tag and tag not in d.name and not d.name.startswith(tag):
                continue
            out[(label, d.name[: -len(".agent")])] = d
    return out


def against(tsv: Path) -> int:
    rows = [ln.split("\t") for ln in tsv.read_text().splitlines()[1:] if ln.strip()]
    coded = {}
    for r in rows:
        coded[(r[1], r[2], int(r[5]))] = (r[8], int(r[7]))
    recon: dict[tuple[str, str, int], str] = {}
    n_cmds = 0
    for (label, run), d in baseline_runs().items():
        cmds = rewrite_commands(d)
        n_cmds += len(cmds)
        for ep in episodes(cmds):
            recon[(label, run, ep[0][0])] = classify_episode(ep)
    matched = [k for k in coded if k in recon]
    agree = sum(coded[k][0] == recon[k] for k in matched)
    print(
        f"coded episodes: {len(coded)}  reconstructed episodes: {len(recon)}  "
        f"difference: {len(recon) - len(coded)}"
    )
    print(
        f"rewrite commands: {n_cmds}  coded command total: {sum(v[1] for v in coded.values())}"
    )
    print(f"coded episodes matched by (corpus, run, turn_start): {len(matched)}")
    pct = 100 * agree / len(matched) if matched else 0.0
    print(f"{agree} of {len(matched)} matched episodes agree ({pct:.1f}%)")
    conf = Counter((coded[k][0], recon[k]) for k in matched)
    print("confusion (rows coded, columns classified):")
    print("          " + " ".join(f"{c[:5]:>5}" for c in CATEGORIES))
    for a in CATEGORIES:
        print(f"  {a:<8}" + " ".join(f"{conf.get((a, b), 0):>5}" for b in CATEGORIES))
    return 0


def mix(patterns: list[str]) -> int:
    dirs = sorted({Path(p) for pat in patterns for p in glob.glob(pat)})
    cats: Counter = Counter()
    total = 0
    for d in dirs:
        for _, c in rewrite_commands(d):
            cats[classify_rewrite(c)] += 1
            total += 1
    print(f"{len(dirs)} transcripts, {total} rewrite commands")
    for c in CATEGORIES:
        if cats[c]:
            print(f"  {c:<9}{cats[c]:>4}")
    return 0


def self_test() -> int:
    fails = []

    def check(name, got, want):
        if got != want:
            fails.append(f"{name}: got {got!r}, want {want!r}")

    py = "python3 - <<'X'\np='analysis-1.md'\ns=open(p).read()\ns=s.replace({!r},{!r})\nopen(p,'w').write(s)\nX"
    check(
        "AA",
        classify_rewrite(
            py.format("| A-3 | x |", "| A-3 | x |\n| A-4 | y [Assumes: A-4] |")
        ),
        "AA",
    )
    check(
        "HOP",
        classify_rewrite(
            py.format("→ GT-4's stated duty cycle", "→ the duty cycle stated in GT-4")
        ),
        "HOP",
    )
    check(
        "HEADINGS",
        classify_rewrite("sed -i '/^## 5/i ### Dead End: x' analysis-1.md"),
        "HEADINGS",
    )
    check("PROC", classify_rewrite("sed -i 's/a/b/' analysis-1.md.process"), "PROC")
    check("VERDICT", classify_rewrite(py.format("Accept: ", "Accept — ")), "VERDICT")
    check("QMARK", classify_rewrite(py.format("GT-3 holds", "GT-3? holds")), "QMARK")
    check("IDFMT", classify_rewrite(py.format("A1 says", "A-1 says")), "IDFMT")
    check(
        "CONTENT", classify_rewrite(py.format("the pump", "the compressor")), "CONTENT"
    )
    groups = episodes([(1, "a"), (4, "b"), (9, "c")])
    check("episodes gap<=3", [len(g) for g in groups], [2, 1])
    check(
        "tie goes to earliest",
        classify_episode(
            [(1, py.format("a", "a [Assumes: A-4]")), (2, py.format("x", "y"))]
        ),
        "AA",
    )

    runs = baseline_runs()
    if not runs:
        fails.append("no baseline runs found")
    else:
        total = sum(len(rewrite_commands(d)) for d in runs.values())
        tsv = REPO / "tests" / "audit-first" / "baseline-coding.tsv"
        want = sum(
            int(ln.split("\t")[7])
            for ln in tsv.read_text().splitlines()[1:]
            if ln.strip()
        )
        check("baseline command total", (total, want), (483, 483))
    for f in fails:
        print("FAIL", f)
    if not fails:
        print("rewrite_causes --self-test: PASS")
    return 1 if fails else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--against", type=Path)
    ap.add_argument("--dirs", nargs="+")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if a.against:
        return against(a.against)
    if a.dirs:
        return mix(a.dirs)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
