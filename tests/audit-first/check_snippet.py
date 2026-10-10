#!/usr/bin/env python3
"""A behavioural test of the prescribed §4 append, run by hand; not a gate.

    python3 tests/audit-first/check_snippet.py --self-test
    python3 tests/audit-first/check_snippet.py --body PATH --self-test

Extracts the fenced sh block containing NOT APPENDED from the agent body, checks it equals
EXPECTED_SNIPPET, runs it in a clean bash against bad and clean section-4 blocks, and checks the
filled command is not counted as a rewrite by phase_turns.is_rewrite and classifies as s4.
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
    "cat > \"<path>.s4\" <<'FP_EOF'\n"
    "<the §4 block>\n"
    "FP_EOF\n"
    f'if grep -nE {GREP_PATTERN} "<path>.s4"; then '
    'echo "NOT APPENDED: a hop above begins with a GT-N identifier; '
    'reorder it and re-issue this whole block"; '
    'else cat "<path>.s4" >> "<path>" && rm -f "<path>.s4"; fi'
)

CLEAN_ENV = ["env", "-i", "PATH=/usr/bin:/bin"]
REL = ".first-principles/analysis-20261010T000000Z.md"

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


def fill(snippet: str, block: str) -> str:
    return snippet.replace("<the §4 block>", block.rstrip("\n")).replace("<path>", REL)


def run(cmd: str) -> tuple[str, str, str | None]:
    """Run cmd in a clean bash in a fresh dir; return (stdout, analysis content, sidecar or None)."""
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / ".first-principles").mkdir()
        (root / REL).write_text("")
        r = subprocess.run(
            [
                *CLEAN_ENV,
                "bash",
                "--noprofile",
                "--norc",
                "-c",
                cmd,
            ],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
        )
        side = root / (REL + ".s4")
        return (
            r.stdout,
            (root / REL).read_text(),
            side.read_text() if side.exists() else None,
        )


def self_test(body: Path) -> bool:
    results: list[tuple[str, bool]] = []

    def check(name: str, ok: bool) -> None:
        results.append((name, ok))
        print(f"{'PASS' if ok else 'FAIL'}: {name}")

    try:
        snippet = extract(body.read_text())
    except ValueError as e:
        check(f"extract: {e}", False)
        print("check_snippet --self-test: FAIL")
        return False
    check("extract: exactly one sh block with NOT APPENDED", True)
    check("drift: body snippet equals EXPECTED_SNIPPET", snippet == EXPECTED_SNIPPET)

    for name, blk, offending in (
        ("bad first hop refused", BAD_FIRST, "→ GT-1's value is the binding term"),
        ("late order-marked bad hop refused", BAD_LATE, "→ [2nd] GT-3 caps the rate"),
    ):
        out, content, side = run(fill(snippet, blk))
        check(
            name,
            content == ""
            and "NOT APPENDED" in out
            and offending in out
            and side is not None,
        )

    for name, blk in (("Cn-led hop accepted", CN_LED), ("clean block appended", CLEAN)):
        out, content, side = run(fill(snippet, blk))
        check(
            name, content == blk + "\n" and side is None and "NOT APPENDED" not in out
        )

    for name, blk in (("bad", BAD_FIRST), ("clean", CLEAN)):
        cmd = fill(snippet, blk)
        check(
            f"{name} fill: not a rewrite, classified s4",
            not phase_turns.is_rewrite(cmd) and phase_turns.classify(cmd) == ["s4"],
        )

    mutant = snippet.replace(GREP_PATTERN, "'^NEVERMATCH'")
    out, content, _ = run(fill(mutant, BAD_FIRST))
    still_refuses = content == "" and "NOT APPENDED" in out
    check(
        "must-fail control: NEVERMATCH mutant fails the bad-block case",
        not still_refuses,
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
