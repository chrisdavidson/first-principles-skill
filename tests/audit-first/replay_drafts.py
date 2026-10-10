#!/usr/bin/env python3
"""Rebuild the held drafts as they stood at the first held-append attempt and replay rules on them.

    python3 tests/audit-first/replay_drafts.py [--rule candidate|strict] [--arm-dir DIR]
    python3 tests/audit-first/replay_drafts.py --body PATH [--compare-transcript]
    python3 tests/audit-first/replay_drafts.py --self-test

Each run's .s2/.s3/.s4 drafts are the bodies of the last `cat > "<X>.sN" <<'FP_EOF'` heredoc
issued before the run's first held-append call. The default mode reports how often the
candidate Type-cell rule fires on the reconstructed .s2; --body replays a body's whole
held-append call on them; --compare-transcript checks each replay against the outcome the
transcript recorded. A measurement tool, never a gate.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


ra = _load("run_audit", HERE / "run_audit.py")
cs = _load("check_snippet", HERE / "check_snippet.py")

# POSIX awk only. Prints "NR: row" for each offending Assumptions-table row and exits 0 if any
# offended, else 1, so `elif awk ... "<path>.s2"; then echo "NOT APPENDED: ..."` refuses on a hit.
# Type cell = field 3. Offending: names two or more of the four types, or contains "/".
CANDIDATE_TYPE_AWK = (
    '/^\\|/ { c = tolower($3); t = c; gsub(/^[ \\t]+|[ \\t]+$/, "", t); '
    'if (t == "type" || t ~ /^[ \\t:-]*$/) next; '
    'n = split(c, a, "physical law") + split(c, a, "current constraint") '
    '+ split(c, a, "convention") + split(c, a, "untested belief") - 4; '
    'if (n >= 2 || index(c, "/") > 0) { print NR ": " $0; bad = 1 } } '
    "END { if (bad) exit 0; exit 1 }"
)

# The D-10-literal form: offending unless the trimmed, lowercased Type cell is exactly one type.
STRICT_TYPE_AWK = (
    '/^\\|/ { c = tolower($3); t = c; gsub(/^[ \\t]+|[ \\t]+$/, "", t); '
    'if (t == "type" || t ~ /^[ \\t:-]*$/) next; '
    'if (t != "physical law" && t != "current constraint" && t != "convention" '
    '&& t != "untested belief") { print NR ": " $0; bad = 1 } } '
    "END { if (bad) exit 0; exit 1 }"
)

AWK_IMPLS = [
    "awk",
    "gawk",
    "gawk --posix",
    "mawk",
    "nawk",
    "original-awk",
    "busybox awk",
]
CLEAN = ["env", "-i", "PATH=/usr/bin:/bin"]
HEREDOC = re.compile(
    r"cat > \"([^\"\n]+\.s([234]))\" <<'FP_EOF'\n(.*?)\nFP_EOF", re.DOTALL
)


def available_impls() -> list[str]:
    out = []
    for impl in AWK_IMPLS:
        argv = shlex.split(impl)
        if not shutil.which(argv[0]):
            continue
        if (
            argv[0] == "busybox"
            and subprocess.run(
                ["busybox", "awk", "BEGIN{exit 0}"], capture_output=True, check=False
            ).returncode
            != 0
        ):
            continue
        out.append(impl)
    return out


def run_awk(impl: str, prog: str, text: str) -> tuple[bool, str]:
    """(fired, output): `<impl> -F'|' '<prog>' file` in a clean bash, in a temp dir."""
    assert "'" not in prog
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / "f").write_text(text)
        r = subprocess.run(
            [*CLEAN, "bash", "--noprofile", "--norc", "-c", f"{impl} -F'|' '{prog}' f"],
            cwd=d,
            capture_output=True,
            text=True,
            check=False,
        )
    return r.returncode == 0, r.stdout


def tool_results(agent_dir: Path) -> list[tuple[int, str, str]]:
    """(turn, command, result) for every Bash call, read independently of run_audit.bash_calls.
    A turn is one distinct assistant message id, as in run_audit.bash_cmds."""
    ids: list[str] = []
    uses: list[tuple[str, int, str]] = []
    res: dict[str, str] = {}
    for f in sorted(agent_dir.glob("agent-*.jsonl")):
        for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                o = json.loads(line)
            except ValueError:
                continue
            msg = o.get("message") or {}
            content = msg.get("content")
            if o.get("type") == "assistant":
                mid = msg.get("id") or f"{f.name}:{len(ids)}"
                if mid not in ids:
                    ids.append(mid)
                for b in content or []:
                    if (
                        isinstance(b, dict)
                        and b.get("type") == "tool_use"
                        and b.get("name") == "Bash"
                    ):
                        uses.append(
                            (
                                b.get("id", ""),
                                len(ids),
                                (b.get("input") or {}).get("command", ""),
                            )
                        )
            elif o.get("type") == "user" and isinstance(content, list):
                for b in content:
                    if isinstance(b, dict) and b.get("type") == "tool_result":
                        c = b.get("content")
                        if isinstance(c, list):
                            c = "\n".join(
                                x.get("text", "") for x in c if isinstance(x, dict)
                            )
                        res[b.get("tool_use_id", "")] = c if isinstance(c, str) else ""
    return [(t, c, res.get(i, "")) for i, t, c in uses]


def reconstruct(agent_dir: Path) -> dict:
    """Drafts at the first held-append attempt, plus the transcript's own outcome of that call."""
    calls = tool_results(agent_dir)
    first = next(((t, c, r) for t, c, r in calls if ra.is_held_append_cmd(c)), None)
    if first is None:
        return {"reconstructed": False, "why": "no held append"}
    turn, _, result = first
    drafts: dict[str, str] = {}
    for t, c, _ in calls:
        if t >= turn:
            break
        for m in HEREDOC.finditer(c):
            drafts[m.group(2)] = m.group(3) + "\n"
    missing = [n for n in "234" if n not in drafts]
    if missing:
        return {
            "reconstructed": False,
            "why": f"no heredoc for .s{','.join(missing)}",
            "turn": turn,
        }
    return {
        "reconstructed": True,
        "turn": turn,
        "drafts": drafts,
        "transcript_refused": "NOT APPENDED" in result,
    }


def arm_runs(arm_dir: Path) -> list[tuple[str, dict]]:
    out = []
    for d in sorted((arm_dir / "raw").glob("*.agent")):
        key = re.sub(r"\.a\d+\.agent$", "", d.name)
        out.append((key, reconstruct(d)))
    return out


def replay_call(snippet: str, drafts: dict[str, str]) -> tuple[bool, str]:
    files = {
        "": "## 1. Essence\n",
        ".s2": drafts["2"],
        ".s3": drafts["3"],
        ".s4": drafts["4"],
    }
    outs, _ = cs.run([cs.fill(snippet)], files)
    first = outs[0].splitlines()[0] if outs[0] else ""
    return "NOT APPENDED" in outs[0], first


def rule_mode(arm_dir: Path, prog: str, label: str) -> tuple[int, int, list[str]]:
    runs = arm_runs(arm_dir)
    usable = [(k, r) for k, r in runs if r["reconstructed"]]
    print(f"unreconstructed {len(runs) - len(usable)}")
    for k, r in runs:
        if not r["reconstructed"]:
            print(f"  {k}: {r['why']}")
    fired = []
    for k, r in usable:
        f, _ = run_awk("awk", prog, r["drafts"]["2"])
        print(f"{k} {'fire' if f else 'no-fire'}")
        if f:
            fired.append(k)
    print(f"{label}TYPE-CELL FIRES {len(fired)} of {len(usable)}")
    return len(fired), len(usable), fired


def body_mode(arm_dir: Path, body: Path, compare: bool) -> int:
    snippet = cs.extract(body.read_text())
    runs = arm_runs(arm_dir)
    usable = [(k, r) for k, r in runs if r["reconstructed"]]
    print(f"unreconstructed {len(runs) - len(usable)}")
    refused, mismatch = 0, 0
    for k, r in usable:
        ref, first = replay_call(snippet, r["drafts"])
        refused += ref
        note = ""
        if compare and ref != r["transcript_refused"]:
            mismatch += 1
            note = f"  MISMATCH transcript {'refused' if r['transcript_refused'] else 'appended'}"
        print(f"{k} {'refused' if ref else 'appended'} | {first[:90]}{note}")
    print(f"CALL REFUSES {refused} of {len(usable)}")
    if compare:
        print(f"TRANSCRIPT MISMATCHES {mismatch}")
    return 1 if mismatch else 0


def self_test() -> bool:
    ok = True

    def check(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  {'PASS' if cond else 'FAIL'}: {name}")
        ok = ok and cond

    hdr = "| Assumption | Type | Treatment | Verdict | Verification |\n|---|---|---|---|---|\n"

    def row(cell: str) -> str:
        return hdr + f"| A1 | {cell} | t | v | x |\n"

    # (text, candidate fires, strict fires)
    fixtures = [
        (
            "convention / untested belief",
            row("convention / untested belief"),
            True,
            True,
        ),
        (
            "physical law, current constraint",
            row("physical law, current constraint"),
            True,
            True,
        ),
        (
            "untested belief, load-bearing",
            row("untested belief, load-bearing"),
            False,
            True,
        ),
        ("convention", row("convention"), False, False),
        ("none of these", row("none of these"), False, True),
        ("header and separator only", hdr, False, False),
        ("two-column row", "| A1 | stated |\n", False, True),
        ("separator with colons", "|:--|:-:|--:|\n", False, False),
    ]
    impls = available_impls()
    print(f"awk impls run: {', '.join(impls)}")
    check("at least one awk implementation found", bool(impls))
    for impl in impls:
        bad = []
        for name, text, cand, strict in fixtures:
            if run_awk(impl, CANDIDATE_TYPE_AWK, text)[0] != cand:
                bad.append(f"candidate:{name}")
            if run_awk(impl, STRICT_TYPE_AWK, text)[0] != strict:
                bad.append(f"strict:{name}")
        check(
            f"fixtures under `{impl}`" + (f" disagree: {bad}" if bad else ""), not bad
        )

    check("candidate awk has no single quote", "'" not in CANDIDATE_TYPE_AWK)
    mutant = "{ } END { exit 1 }"
    dirty = fixtures[0][1]
    check(
        "must-fail: never-matching awk fails the dirty fixture",
        not run_awk("awk", mutant, dirty)[0],
    )

    with tempfile.TemporaryDirectory() as d:
        body = Path(d) / "b198.md"
        body.write_text(
            subprocess.run(
                ["git", "show", "cc37f771:first-principles/agents/first-principles.md"],
                cwd=HERE.parents[1],
                capture_output=True,
                text=True,
                check=True,
            ).stdout
        )
        snippet = cs.extract(body.read_text())
        runs = arm_runs(HERE)
        usable = [(k, r) for k, r in runs if r["reconstructed"]]
        check("24 runs reconstructed", len(usable) == 24 and len(runs) == 24)
        mism = [
            k
            for k, r in usable
            if replay_call(snippet, r["drafts"])[0] != r["transcript_refused"]
        ]
        check(
            f"replay equals transcript first-attempt outcome on every run {mism}",
            not mism,
        )
        k_cand, n, _ = rule_mode_quiet(usable, CANDIDATE_TYPE_AWK)
        check(f"candidate fires on {k_cand} of {n} (<= 10)", n == 24 and k_cand <= 10)
    print(f"replay_drafts --self-test: {'PASS' if ok else 'FAIL'}")
    return ok


def rule_mode_quiet(usable, prog):
    fired = [k for k, r in usable if run_awk("awk", prog, r["drafts"]["2"])[0]]
    return len(fired), len(usable), fired


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--arm-dir", type=Path, default=HERE)
    ap.add_argument("--rule", choices=("candidate", "strict"), default="candidate")
    ap.add_argument("--body", type=Path)
    ap.add_argument("--compare-transcript", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return 0 if self_test() else 1
    if a.body:
        return body_mode(a.arm_dir, a.body, a.compare_transcript)
    if a.rule == "strict":
        rule_mode(a.arm_dir, STRICT_TYPE_AWK, "STRICT ")
    else:
        rule_mode(a.arm_dir, CANDIDATE_TYPE_AWK, "")
    return 0


if __name__ == "__main__":
    sys.exit(main())
