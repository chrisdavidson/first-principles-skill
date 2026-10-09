#!/usr/bin/env python3
"""pointer-fix -- does the final pointer name the files where the shell actually wrote them?

    python3 tests/pointer-fix/run_pointer.py run --body <dir>/first-principles --cwd <empty dir>
    python3 tests/pointer-fix/run_pointer.py read [--dir tests/<capture dir>]

Protocol: docs/pointer-fix-preregistration.md. Transport and capture reuse
tests/example-rerun-2/run_examples.py unchanged. A measurement, never a gate.
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
spec = importlib.util.spec_from_file_location("_er2pf", REPO_ROOT / "tests/example-rerun-2/run_examples.py")
er = importlib.util.module_from_spec(spec)
sys.modules["_er2pf"] = er
spec.loader.exec_module(er)
EXAMPLE_PROMPTS = dict(er.PROMPTS)

_ANCHOR = ".first-principles/"
_STOP = set(" \t\n`'\"()<>*[]|,;")
_NAME = re.compile(r"[A-Za-z0-9._-]+")


def path_tokens(text: str) -> list[str]:
    """Every path token naming a delivered file: an optional absolute prefix, then
    `.first-principles/<name>`. Anchored on the literal, so it is linear in the text."""
    out, i = [], text.find(_ANCHOR)
    while i != -1:
        m = _NAME.match(text, i + len(_ANCHOR))
        if m:
            j = i
            while j > 0 and text[j - 1] not in _STOP:
                j -= 1
            prefix = text[j:i]
            out.append((prefix if prefix.startswith("/") else "") + _ANCHOR + m.group(0).rstrip("."))
        i = text.find(_ANCHOR, i + 1)
    return out


def _events(path: Path):
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            yield json.loads(line)


def final_pointer(agent_dir: Path) -> str:
    """Every path the agent asserts or uses: all its own assistant text, plus the file path of
    every Read it issues. Strict on purpose -- a wrong pointer in an earlier turn, or a Read of a
    location the shell never wrote, counts even if the last message is right."""
    parts = []
    for f in sorted(agent_dir.glob("agent-*.jsonl")):
        for o in _events(f):
            if o.get("type") != "assistant":
                continue
            for b in o["message"].get("content") or []:
                if not isinstance(b, dict):
                    continue
                if b.get("type") == "text":
                    parts.append(b.get("text", ""))
                elif b.get("type") == "tool_use" and b.get("name") == "Read":
                    parts.append("`" + str(b.get("input", {}).get("file_path", "")) + "`")
    return "\n".join(parts)


def run_cwd(jsonl: Path) -> str | None:
    for o in _events(jsonl):
        if o.get("type") == "system" and o.get("subtype") == "init":
            return o.get("cwd")
    return None


def judge(pointer: str, cwd: str, produced: set[str]) -> dict:
    """Classify every path token in the pointer.

    wrong    -- absolute but not under <cwd>/.first-principles/, or names no produced file
    relative -- `.first-principles/<name>` naming a produced file (right place, not absolute)
    correct  -- `<cwd>/.first-principles/<name>` naming a produced file
    """
    want = f"{cwd.rstrip('/')}/.first-principles/"
    out = {"correct": [], "relative": [], "wrong": []}
    for tok in dict.fromkeys(path_tokens(pointer)):
        name = tok.rsplit("/", 1)[-1]
        if name not in produced:
            out["wrong"].append(tok)
        elif tok.startswith("/"):
            (out["correct"] if tok.startswith(want) else out["wrong"]).append(tok)
        else:
            out["relative"].append(tok)
    return out


def printed_names(agent_dir: Path) -> set[str]:
    """Basenames of every `.first-principles/` file a Bash command printed in the agent's run."""
    names: set[str] = set()
    for f in sorted(agent_dir.glob("agent-*.jsonl")):
        for o in _events(f):
            for b in (o.get("message", {}).get("content") or []):
                if isinstance(b, dict) and b.get("type") == "tool_result":
                    c = b.get("content")
                    text = c if isinstance(c, str) else "\n".join(
                        x.get("text", "") for x in c or [] if isinstance(x, dict))
                    for tok in path_tokens(text):
                        names.add(tok.rsplit("/", 1)[-1])
    return names


def read(capture: Path) -> int:
    cells = json.loads((capture / "cells.json").read_text())
    tally = {"runs": 0, "with_paths": 0, "wrong": 0, "all_absolute": 0}
    print(f"{'cell':44} {'paths':>5} {'abs-ok':>6} {'rel':>4} {'wrong':>5}")
    for cell, c in cells.items():
        if c.get("outcome") != "file":
            continue
        last = c["attempts"][-1].removesuffix(".jsonl")
        files_dir = capture / "raw" / f"{last}.files"
        produced = {p.name for p in files_dir.rglob("*") if p.is_file()} if files_dir.is_dir() else set()
        produced |= printed_names(capture / "raw" / f"{last}.agent")
        cwd = run_cwd(capture / "raw" / f"{last}.jsonl") or ""
        j = judge(final_pointer(capture / "raw" / f"{last}.agent"), cwd, produced)
        n = sum(len(v) for v in j.values())
        tally["runs"] += 1
        tally["with_paths"] += n > 0
        tally["wrong"] += bool(j["wrong"])
        tally["all_absolute"] += n > 0 and not j["relative"] and not j["wrong"]
        flag = "  WRONG " + ", ".join(j["wrong"][:2]) if j["wrong"] else ""
        print(f"{cell:44} {n:>5} {len(j['correct']):>6} {len(j['relative']):>4} {len(j['wrong']):>5}{flag}")
    print(f"\nfile runs {tally['runs']}  pointer names a path {tally['with_paths']}  "
          f"WRONG pointer {tally['wrong']}  every path absolute and correct {tally['all_absolute']}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=("run", "supp", "read"))
    ap.add_argument("--body", type=Path)
    ap.add_argument("--cwd", type=Path)
    ap.add_argument("--dir", type=Path, default=HERE)
    a = ap.parse_args()
    if a.command == "read":
        return read(a.dir.resolve())
    if not (a.body and a.cwd):
        ap.error("run needs --body and --cwd")
    er.HERE, er.RAW, er.DOCS = HERE, HERE / "raw", HERE / "documents"
    if a.command == "run":
        er.PROMPTS = EXAMPLE_PROMPTS
        return er.run(a.body.resolve(), a.cwd.resolve())
    # Amendment 1: re-run each example whose registered run skipped, supp1 then supp2 only.
    cells = json.loads((HERE / "cells.json").read_text())
    skipped = [n for n in EXAMPLE_PROMPTS if cells.get(n, {}).get("outcome") == "final-message"]
    for name in skipped:
        for k in (1, 2):
            cell = f"{name}.supp{k}"
            er.PROMPTS = {cell: EXAMPLE_PROMPTS[name]}
            rc = er.run(a.body.resolve(), a.cwd.resolve())
            if rc:
                return rc
            if json.loads((HERE / "cells.json").read_text())[cell]["outcome"] == "file":
                break
    return 0


if __name__ == "__main__":
    sys.exit(main())
