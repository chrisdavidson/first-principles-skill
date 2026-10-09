#!/usr/bin/env python3
"""DELIVERY-GUARD -- the shipped SubagentStop delivery guard is wired and decides right.

Backlog 999.196. The plugin ships `first-principles/hooks/hooks.json`, which runs
`first-principles/hooks/delivery-guard.py` when the first-principles agent stops,
and refuses the stop (at most twice) until the analysis file is assembled and the
reader report exists. That guard is the only executable code in the plugin, so a
wiring slip -- a matcher that no longer names the agent, a command path that no
longer resolves -- would turn it off with every other gate green. This gate checks:

  1. Wiring: hooks.json's SubagentStop list holds only the guard's entry, its matcher is
     `<plugin.json name>:<agent name from shared/spine/SKILL.meta.yml>`, and its
     command runs `${CLAUDE_PLUGIN_ROOT}/hooks/delivery-guard.py`, which exists.
  2. The shipped guard's own `--self-test` passes, with its capture controls run.
  3. Corpus: the guard's decision on every current-body capture in
     tests/pointer-fix/raw, tests/example-rerun-2/raw and the `new` arm of
     tests/skip-paired/raw equals an independently transcribed verdict table --
     every recorded skip blocked, every delivered run passed.

Must-fail controls mutate the wiring and stub the guard's decision (always-allow,
always-block) and require each to turn this gate red.

What it cannot see: whether the live agent, once blocked, then delivers. That is
a live reading (docs/delivery-guard-reading.md), never gated here.
"""

from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGIN = REPO_ROOT / "first-principles"
HOOKS_JSON = PLUGIN / "hooks" / "hooks.json"
GUARD = PLUGIN / "hooks" / "delivery-guard.py"
PLUGIN_JSON = PLUGIN / ".claude-plugin" / "plugin.json"
SPINE_META = REPO_ROOT / "shared" / "spine" / "SKILL.meta.yml"
GUARD_COMMAND = 'python3 "${CLAUDE_PLUGIN_ROOT}/hooks/delivery-guard.py"'

# Independent transcription of each current-body capture's verdict, read from the
# transcripts and the readings (docs/pointer-fix-reading.md "Skips";
# docs/example-rerun-2-reading.md; docs/skip-paired-reading.md), not derived
# from the guard. True = the run delivered (the guard must let it stop).
# skip-paired's `old` arm ran v9.13.0, whose file is never assembled under
# `## Answer`, so it is outside this body's contract and not listed.
_SKIPS = {
    "pointer-fix": {
        "decompose-irreducibility.a1",  # web searches only
        "product-business.a1",  # no tool call
        "science-engineering-2.a1",  # Skill: the slash-only launcher
        "self-application.a1",  # Skill: claude-api
        "science-engineering-2.supp1.a1",  # working file only, report steps skipped
    },
    "example-rerun-2": {
        "decompose-irreducibility.a1",  # Skill that does not exist
        "personal-general-2.a2",  # two Bash calls, no file
        "product-business.a1",  # no tool call
    },
    "skip-paired": {
        "decompose-irreducibility.new.r3.a1",  # assembled, no reader report
    },
}
_CORPORA = {
    "pointer-fix": REPO_ROOT / "tests" / "pointer-fix" / "raw",
    "example-rerun-2": REPO_ROOT / "tests" / "example-rerun-2" / "raw",
    "skip-paired": REPO_ROOT / "tests" / "skip-paired" / "raw",
}
# Floor: the corpus must still hold at least this many current-body captures,
# so a deleted or renamed capture tree cannot shrink the check to nothing.
_CORPUS_FLOOR = 40

_CONTROL_IDS = (
    "P1-live-wiring",
    "P2-guard-self-test",
    "P3-corpus-verdicts",
    "M1-matcher-renamed",
    "M2-command-path-missing",
    "M3-second-subagentstop-entry",
    "M4-guard-always-allows",
    "M5-guard-always-blocks",
    "M6-corpus-floor",
)


def _load_guard():
    spec = importlib.util.spec_from_file_location("fp_delivery_guard", GUARD)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def expected_matcher() -> str:
    plugin = json.loads(PLUGIN_JSON.read_text(encoding="utf-8"))["name"]
    agent = yaml.safe_load(SPINE_META.read_text(encoding="utf-8"))["agent"]["name"]
    return f"{plugin}:{agent}"


def wiring_problems(hooks: dict, guard_exists: bool = True) -> list[str]:
    problems: list[str] = []
    entries = (hooks.get("hooks") or {}).get("SubagentStop")
    if not isinstance(entries, list) or len(entries) != 1:
        n = len(entries) if isinstance(entries, list) else 0
        return [f"WIRE-COUNT: expected exactly one SubagentStop entry, found {n}"]
    entry = entries[0]
    want = expected_matcher()
    if entry.get("matcher") != want:
        problems.append(
            f"WIRE-MATCHER: matcher is {entry.get('matcher')!r}, expected {want!r}"
        )
    commands = [
        h.get("command") for h in entry.get("hooks", []) if h.get("type") == "command"
    ]
    if commands != [GUARD_COMMAND]:
        problems.append(
            f"WIRE-COMMAND: commands are {commands!r}, expected [{GUARD_COMMAND!r}]"
        )
    if not guard_exists:
        problems.append(f"WIRE-TARGET: {GUARD.relative_to(REPO_ROOT)} does not exist")
    return problems


def guard_self_test_problems() -> list[str]:
    proc = subprocess.run(
        [sys.executable, str(GUARD), "--self-test"],
        capture_output=True,
        text=True,
        check=False,
    )
    problems = []
    if proc.returncode != 0:
        problems.append(
            f"GUARD-SELFTEST: exit {proc.returncode}\n{proc.stdout}{proc.stderr}"
        )
    if "C12 capture" not in proc.stdout:
        problems.append("GUARD-SELFTEST: capture controls C11/C12 did not run")
    return problems


def corpus_verdicts(decide_problem) -> tuple[dict[str, bool], list[str]]:
    """{corpus/capture: delivered?} as `decide_problem` judges it, plus problems."""
    verdicts: dict[str, bool] = {}
    with tempfile.TemporaryDirectory() as td:
        for corpus, raw in _CORPORA.items():
            if not raw.is_dir():
                return verdicts, [f"CORPUS-MISSING: {raw.relative_to(REPO_ROOT)}"]
            for agent_dir in sorted(raw.glob("*.agent")):
                name = agent_dir.name[: -len(".agent")]
                if corpus == "skip-paired" and ".new." not in name:
                    continue
                transcripts = sorted(agent_dir.glob("*.jsonl"))
                if len(transcripts) != 1:
                    return verdicts, [
                        f"CORPUS-SHAPE: {agent_dir} has {len(transcripts)} transcripts"
                    ]
                cwd = Path(td) / corpus / name
                files = raw / f"{name}.files"
                if files.is_dir():
                    shutil.copytree(files, cwd / ".first-principles")
                else:
                    cwd.mkdir(parents=True)
                verdicts[f"{corpus}/{name}"] = (
                    decide_problem(transcripts[0], cwd) is None
                )
    return verdicts, []


def corpus_problems(decide_problem) -> list[str]:
    verdicts, problems = corpus_verdicts(decide_problem)
    if problems:
        return problems
    if len(verdicts) < _CORPUS_FLOOR:
        return [f"CORPUS-FLOOR: {len(verdicts)} captures, floor {_CORPUS_FLOOR}"]
    for corpus, skips in _SKIPS.items():
        for name in skips:
            if f"{corpus}/{name}" not in verdicts:
                problems.append(
                    f"CORPUS-UNLISTED: {corpus}/{name} is in the verdict table but not on disk"
                )
    for key, delivered in sorted(verdicts.items()):
        corpus, name = key.split("/", 1)
        want = name not in _SKIPS[corpus]
        if delivered != want:
            kind = "passed a recorded skip" if delivered else "blocked a delivered run"
            problems.append(f"CORPUS-VERDICT: guard {kind}: {key}")
    return problems


def _hooks() -> dict:
    return json.loads(HOOKS_JSON.read_text(encoding="utf-8"))


def self_test() -> int:
    failures: list[str] = []
    guard = _load_guard()

    def control(cid: str, problems: list[str], must_fail: bool) -> None:
        ok = bool(problems) if must_fail else not problems
        print(f"check-delivery-guard --self-test: {cid} {'PASS' if ok else 'FAIL'}")
        if not ok:
            failures.append(cid)
            for p in problems or ["(expected a finding, got none)"]:
                print(f"    {p}")

    control("P1-live-wiring", wiring_problems(_hooks(), GUARD.is_file()), False)
    control("P2-guard-self-test", guard_self_test_problems(), False)
    control("P3-corpus-verdicts", corpus_problems(guard.delivery_problem), False)

    renamed = copy.deepcopy(_hooks())
    renamed["hooks"]["SubagentStop"][0]["matcher"] = "first-principles"
    control("M1-matcher-renamed", wiring_problems(renamed), True)
    control(
        "M2-command-path-missing", wiring_problems(_hooks(), guard_exists=False), True
    )
    doubled = copy.deepcopy(_hooks())
    doubled["hooks"]["SubagentStop"].append(doubled["hooks"]["SubagentStop"][0])
    control("M3-second-subagentstop-entry", wiring_problems(doubled), True)
    control("M4-guard-always-allows", corpus_problems(lambda t, c: None), True)
    control("M5-guard-always-blocks", corpus_problems(lambda t, c: "stub"), True)

    global _CORPUS_FLOOR
    saved = _CORPUS_FLOOR
    _CORPUS_FLOOR = 10_000
    try:
        problems = corpus_problems(guard.delivery_problem)
    finally:
        _CORPUS_FLOOR = saved
    control(
        "M6-corpus-floor", [p for p in problems if p.startswith("CORPUS-FLOOR")], True
    )

    if failures:
        print(
            f"check-delivery-guard --self-test: FAIL ({len(failures)} of {len(_CONTROL_IDS)})"
        )
        return 1
    print(f"check-delivery-guard --self-test: PASS ({len(_CONTROL_IDS)} controls)")
    return 0


def describe() -> dict:
    return {
        "control_ids": list(_CONTROL_IDS),
        "control_count": len(_CONTROL_IDS),
        "registered_surfaces": [
            "first-principles/hooks/delivery-guard.py",
            "first-principles/hooks/hooks.json",
        ],
        "disclosed_bounds_anchors": [
            "decides delivery from the file on disk, never from the analysis's quality",
            "blocks at most twice per run, then lets the stop through",
            "whether a blocked agent then delivers is a live reading, never gated",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--describe", action="store_true")
    args = ap.parse_args(argv)
    if args.describe:
        print(json.dumps(describe(), indent=2, sort_keys=True))
        return 0
    return self_test()


if __name__ == "__main__":
    sys.exit(main())
