#!/usr/bin/env python3
"""A behavioural test of the prescribed held append and assembly, run by hand; not a gate.

    python3 tests/audit-first/check_snippet.py --self-test
    python3 tests/audit-first/check_snippet.py --body PATH --self-test

Extracts the held-append sh block (contains NOT APPENDED) and the step-4 assemble command from
the agent body, checks each equals its expected text, runs them in a clean bash against bad, clean
and missing drafts, and checks phase_turns does not count them as rewrites.

The shipped working tree carries the held-append snippet (the 999.198 body, re-applied for 999.200
and unreleased). Against a body without the snippet (for example the 9.19.4 body) the self-test
reports SKIP and exits 0.
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DEFAULT_BODY = REPO / "first-principles" / "agents" / "first-principles.md"

_spec = importlib.util.spec_from_file_location(
    "phase_turns", REPO / "tests" / "skip-rate" / "phase_turns.py"
)
phase_turns = importlib.util.module_from_spec(_spec)
sys.modules["phase_turns"] = phase_turns
_spec.loader.exec_module(phase_turns)

GREP_PATTERN = "'^→[[:space:]]*(\\[[^]]*\\])?[[:space:]]*GT-[0-9]'"

# Must equal replay_drafts.CANDIDATE_TYPE_AWK, so the measured fire rate is the shipped rule's.
TYPE_AWK = (
    '/^\\|/ { c = tolower($3); t = c; gsub(/^[ \\t]+|[ \\t]+$/, "", t); '
    'if (t == "type" || t ~ /^[ \\t:-]*$/) next; '
    'n = split(c, a, "physical law") + split(c, a, "current constraint") '
    '+ split(c, a, "convention") + split(c, a, "untested belief") - 4; '
    'if (n >= 2 || index(c, "/") > 0) { print NR ": " $0; bad = 1 } } '
    "END { if (bad) exit 0; exit 1 }"
)

EXPECTED_SNIPPET = (
    'if [ ! -f "<path>.s2" ] || [ ! -f "<path>.s3" ] || [ ! -f "<path>.s4" ]; then '
    'echo "NOT APPENDED: <path>.s2, .s3 or .s4 is missing '
    '(if this call already succeeded, all three are in the file)"; '
    f'elif grep -nE {GREP_PATTERN} "<path>.s4"; then '
    'echo "NOT APPENDED: a hop above begins with a GT-N identifier; '
    'reorder it and issue the §4 draft again"; '
    f"elif awk -F'|' '{TYPE_AWK}' \"<path>.s2\"; then "
    'echo "NOT APPENDED: a Type cell above names more than one assumption type; '
    "give each row exactly one of physical law, current constraint, convention or "
    'untested belief and issue the §2 draft again"; '
    'else cat "<path>.s2" "<path>.s3" "<path>.s4" >> "<path>" '
    '&& rm -f "<path>.s2" "<path>.s3" "<path>.s4"; fi'
)

GUARD_BRANCH = (
    'if ls "<path>".s[234] 2>/dev/null; then echo "NOT ASSEMBLED: the held drafts '
    'listed above are not in the file; run the held append in step 2 first"; el'
)
EXPECTED_ASSEMBLE = (
    GUARD_BRANCH
    + 'if [ -f "<path>.answer" ]; then cat "<path>.answer" "<path>" "<path>.process" '
    '> "<path>.tmp" && mv "<path>.tmp" "<path>" && rm -f "<path>.answer" '
    '"<path>.process" || rm -f "<path>.tmp"; else echo "already assembled"; fi'
)

CLEAN_ENV = ["env", "-i", "PATH=/usr/bin:/bin"]
REL = ".first-principles/analysis-20261010T000000Z.md"

S1 = "## 1. Essence\n\nThe essence.\n"
S2 = "## 2. Assumptions\n\n| A1 | stated |\n"
S2_HEAD = (
    "## 2. Assumptions\n\n"
    "| Assumption | Type | Treatment | Verdict | Verification |\n"
    "|---|---|---|---|---|\n"
)
S2_CLEAN = (
    S2_HEAD
    + "| A1 rates are flat | physical law | held | Hold | checked |\n"
    + "| A2 budget is fixed | Current constraint | held | Hold | checked |\n"
)
S2_SLASH = (
    S2_CLEAN + "| A3 users agree | convention / untested belief | held | Hold | x |\n"
)
S2_TWO = (
    S2_CLEAN
    + "| A3 users agree | physical law, current constraint | held | Hold | x |\n"
)
S3 = "## 3. Ground Truths\n\nGT-1: a figure\n"
HEAD = "## 4. Derivation Chains\n\n### Conclusion C1: example\n\nGT-1 (a) + GT-2? (b)\n"
BAD_FIRST = HEAD + "→ GT-1's value is the binding term\n→ the rate follows\n"
BAD_LATE = (
    HEAD
    + "→ the value stated in GT-1 is the binding term\n"
    + "→ the rate follows\n"
    + "→ [2nd] GT-3 caps the rate\n"
)
CN_LED = (
    HEAD
    + "→ the value stated in GT-1 is the binding term\n"
    + "→ C1's saving dominates the cost\n"
)
CLEAN = HEAD + "→ the value stated in GT-1 is the binding term\n→ the rate follows\n"


def extract(text: str) -> str:
    blocks = re.findall(
        r"^([ \t]*)```sh\n(.*?)^\1```[ \t]*$", text, re.DOTALL | re.MULTILINE
    )
    hits = [(ind, b) for ind, b in blocks if "NOT APPENDED" in b]
    if len(hits) != 1:
        raise ValueError(
            f"expected exactly one sh block with NOT APPENDED, found {len(hits)}"
        )
    return textwrap.dedent(hits[0][1]).rstrip("\n")


def extract_assemble(text: str) -> str:
    hits = re.findall(r"`(if [^`\n]*already assembled[^`\n]*)`", text)
    if len(hits) != 1:
        raise ValueError(f"expected exactly one assemble command, found {len(hits)}")
    return hits[0]


def fill(cmd: str) -> str:
    return cmd.replace("<path>", REL)


def run(cmds: list[str], files: dict[str, str]) -> tuple[list[str], dict[str, str]]:
    """Run each cmd in order in a clean bash in one fresh dir.

    files maps a suffix on REL ("" for the analysis file) to its initial content.
    Returns (stdout per cmd, suffix -> content of every file left behind).
    """
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / ".first-principles").mkdir()
        for suffix, content in files.items():
            (root / (REL + suffix)).write_text(content)
        outs = []
        for cmd in cmds:
            r = subprocess.run(
                [*CLEAN_ENV, "bash", "--noprofile", "--norc", "-c", cmd],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            outs.append(r.stdout)
        left = {
            p.name[len(Path(REL).name) :]: p.read_text()
            for p in (root / ".first-principles").iterdir()
        }
        return outs, left


def drafts(s4: str, s2: str = S2) -> dict[str, str]:
    return {"": S1, ".s2": s2, ".s3": S3, ".s4": s4}


def _load_replay():
    spec = importlib.util.spec_from_file_location(
        "replay_drafts", REPO / "tests" / "audit-first" / "replay_drafts.py"
    )
    mod = importlib.util.module_from_spec(spec)
    sys.modules["replay_drafts"] = mod
    spec.loader.exec_module(mod)
    return mod


def self_test(body: Path) -> bool:
    results: list[tuple[str, bool]] = []

    def check(name: str, ok: bool) -> None:
        results.append((name, ok))
        print(f"{'PASS' if ok else 'FAIL'}: {name}")

    text = body.read_text()
    if "NOT APPENDED" not in text:
        print(
            "SKIP: the body carries no held-append snippet (for example the 9.19.4 body); "
            "pass --body for the arm commit's body to run this test"
        )
        return True
    try:
        snippet = extract(text)
        assemble = extract_assemble(text)
    except ValueError as e:
        check(f"extract: {e}", False)
        print("check_snippet --self-test: FAIL")
        return False
    check("extract: exactly one sh block with NOT APPENDED", True)
    check("drift: body snippet equals EXPECTED_SNIPPET", snippet == EXPECTED_SNIPPET)
    check(
        "drift: body assemble equals EXPECTED_ASSEMBLE", assemble == EXPECTED_ASSEMBLE
    )

    cmd = fill(snippet)
    for name, s4, offending in (
        ("bad first hop refused", BAD_FIRST, "→ GT-1's value is the binding term"),
        ("late order-marked bad hop refused", BAD_LATE, "→ [2nd] GT-3 caps the rate"),
    ):
        outs, left = run([cmd], drafts(s4))
        check(
            name,
            left[""] == S1
            and {".s2", ".s3", ".s4"} <= left.keys()
            and "NOT APPENDED" in outs[0]
            and offending in outs[0],
        )

    for name, s4 in (
        ("Cn-led hop accepted", CN_LED),
        ("clean drafts appended in order", CLEAN),
    ):
        outs, left = run([cmd], drafts(s4))
        check(
            name,
            left == {"": S1 + S2 + S3 + s4} and "NOT APPENDED" not in outs[0],
        )

    for name, s2, offending in (
        ("slash Type cell refused", S2_SLASH, "convention / untested belief"),
        ("two-token Type cell refused", S2_TWO, "physical law, current constraint"),
    ):
        outs, left = run([cmd], drafts(CLEAN, s2))
        check(
            name,
            left[""] == S1
            and {".s2", ".s3", ".s4"} <= left.keys()
            and left[".s2"] == s2
            and left[".s3"] == S3
            and left[".s4"] == CLEAN
            and "NOT APPENDED: a Type cell above" in outs[0]
            and offending in outs[0],
        )
    outs, left = run([cmd], drafts(CLEAN, S2_CLEAN))
    check(
        "clean single-type S2 appended in order",
        left == {"": S1 + S2_CLEAN + S3 + CLEAN} and "NOT APPENDED" not in outs[0],
    )

    rd = _load_replay()
    check(
        "TYPE_AWK equals replay_drafts.CANDIDATE_TYPE_AWK",
        TYPE_AWK == rd.CANDIDATE_TYPE_AWK,
    )
    fixtures = [S2_CLEAN, S2_SLASH, S2_TWO, S2]
    ran = []
    agree = True
    with tempfile.TemporaryDirectory() as d:
        for i, fx in enumerate(fixtures):
            (Path(d) / f"fx{i}").write_text(fx)
        base_codes = None
        for impl in rd.available_impls():
            argv = impl.split()
            codes = [
                subprocess.run(
                    [*CLEAN_ENV, *argv, "-F|", TYPE_AWK, str(Path(d) / f"fx{i}")],
                    capture_output=True,
                    check=False,
                ).returncode
                for i in range(len(fixtures))
            ]
            ran.append(impl)
            if impl == "awk":
                base_codes = codes
            elif base_codes is not None and codes != base_codes:
                agree = False
                print(f"  disagrees: {impl} {codes} vs awk {base_codes}")
    print(f"awk impls run: {', '.join(ran)}")
    check(
        "TYPE_AWK decides every fixture alike under every awk on PATH",
        bool(ran) and "awk" in ran and agree and base_codes == [1, 0, 0, 1],
    )

    check(
        "Type-cell refusal: not a rewrite, classified nothing",
        not phase_turns.is_rewrite(cmd) and phase_turns.classify(cmd) == [],
    )

    files = drafts(CLEAN)
    del files[".s3"]
    outs, left = run([cmd], files)
    check(
        "missing .s3 refused, nothing appended",
        left == {"": S1, ".s2": S2, ".s4": CLEAN} and "NOT APPENDED" in outs[0],
    )

    outs, left = run([cmd, cmd], drafts(CLEAN))
    check(
        "idempotent: second run leaves the file byte-identical and refuses",
        left == {"": S1 + S2 + S3 + CLEAN}
        and "NOT APPENDED" not in outs[0]
        and "NOT APPENDED" in outs[1],
    )

    acmd = fill(assemble)
    base = {"": S1 + S2, ".answer": "## Answer\n", ".process": "## Appendix\n"}
    outs, left = run([acmd], {**base, ".s3": S3})
    check(
        "assembly refused while a held draft exists",
        "NOT ASSEMBLED" in outs[0]
        and Path(REL + ".s3").name in outs[0]
        and left == {**base, ".s3": S3},
    )
    outs, left = run([acmd, acmd], base)
    check(
        "assembly proceeds with no drafts, then reports already assembled",
        left == {"": "## Answer\n" + S1 + S2 + "## Appendix\n"}
        and "NOT ASSEMBLED" not in outs[0]
        and "already assembled" in outs[1],
    )

    sidecar = f"cat > \"{REL}.s2\" <<'FP_EOF'\n{S2}FP_EOF"
    check(
        "held append: not a rewrite, classified nothing",
        not phase_turns.is_rewrite(cmd) and phase_turns.classify(cmd) == [],
    )
    check(
        "assemble: not a rewrite, classified assemble",
        not phase_turns.is_rewrite(acmd) and "assemble" in phase_turns.classify(acmd),
    )
    check(
        "sidecar write and its re-issue: not rewrites, classified s2",
        not phase_turns.is_rewrite(sidecar) and phase_turns.classify(sidecar) == ["s2"],
    )

    mutant = snippet.replace(GREP_PATTERN, "'^NEVERMATCH'")
    outs, left = run([fill(mutant)], drafts(BAD_FIRST))
    check(
        "must-fail control: NEVERMATCH mutant fails the bad-draft case",
        not (left[""] == S1 and "NOT APPENDED" in outs[0]),
    )
    mutant = snippet.replace(TYPE_AWK, "BEGIN { exit 1 }")
    outs, left = run([fill(mutant)], drafts(CLEAN, S2_SLASH))
    check(
        "must-fail control: a never-matching Type awk fails the dirty-S2 case",
        not (left[""] == S1 and "NOT APPENDED" in outs[0]),
    )
    mutant = snippet.replace('|| [ ! -f "<path>.s3" ]', "")
    files = drafts(CLEAN)
    del files[".s3"]
    outs, left = run([fill(mutant)], files)
    check(
        "must-fail control: dropping the .s3 test fails the missing-draft case",
        not (left[""] == S1 and "NOT APPENDED" in outs[0]),
    )
    mutant = assemble.replace(GUARD_BRANCH, "")
    outs, left = run([fill(mutant)], {**base, ".s3": S3})
    check(
        "must-fail control: dropping the ls branch fails the assembly-guard case",
        not ("NOT ASSEMBLED" in outs[0] and left == {**base, ".s3": S3}),
    )

    ok = all(o for _, o in results)
    print(f"check_snippet --self-test: {'PASS' if ok else 'FAIL'}")
    return ok


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--body", type=Path, default=DEFAULT_BODY)
    args = ap.parse_args()
    if not args.self_test:
        ap.error("--self-test is required")
    return 0 if self_test(args.body) else 1


if __name__ == "__main__":
    sys.exit(main())
