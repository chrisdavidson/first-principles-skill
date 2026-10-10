#!/usr/bin/env python3
"""A behavioural test of the prescribed held append and assembly, run by hand; not a gate.

    python3 tests/audit-first/check_snippet.py --self-test
    python3 tests/audit-first/check_snippet.py --body PATH --self-test

Extracts the held-append sh block (contains NOT APPENDED) and the step-4 assemble command from
the agent body, checks each equals its expected text, runs them in a clean bash against bad, clean
and missing drafts, and checks phase_turns does not count them as rewrites.

The body under test was not released (999.198 verdict: not-shown-effective). Its snippet lives at
e5b1ef5d151d; re-test with --body <(git show e5b1ef5d151d:first-principles/agents/first-principles.md).
Against the shipped body, which lacks the snippet, the self-test reports SKIP and exits 0.
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

EXPECTED_SNIPPET = (
    'if [ ! -f "<path>.s2" ] || [ ! -f "<path>.s3" ] || [ ! -f "<path>.s4" ]; then '
    'echo "NOT APPENDED: <path>.s2, .s3 or .s4 is missing '
    '(if this call already succeeded, all three are in the file)"; '
    f'elif grep -nE {GREP_PATTERN} "<path>.s4"; then '
    'echo "NOT APPENDED: a hop above begins with a GT-N identifier; '
    'reorder it and issue the §4 draft again"; '
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


def drafts(s4: str) -> dict[str, str]:
    return {"": S1, ".s2": S2, ".s3": S3, ".s4": s4}


def self_test(body: Path) -> bool:
    results: list[tuple[str, bool]] = []

    def check(name: str, ok: bool) -> None:
        results.append((name, ok))
        print(f"{'PASS' if ok else 'FAIL'}: {name}")

    text = body.read_text()
    if "NOT APPENDED" not in text:
        print(
            "SKIP: the body carries no held-append snippet (999.198 was not released); "
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
