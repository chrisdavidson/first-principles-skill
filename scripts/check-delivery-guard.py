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
import os
import re
import shlex
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

AGENT_MD = PLUGIN / "agents" / "first-principles.md"
PHASE_TURNS = REPO_ROOT / "tests" / "skip-rate" / "phase_turns.py"
PROGRAM_SRC = PLUGIN / "references" / "replace-blocks.md"
_IDENTITY_ROOTS = (
    REPO_ROOT / "tests" / "audit-first" / "raw",
    REPO_ROOT / "tests" / "post-held-append" / "raw",
)
_IDENTITY_FLOOR = 40

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
    "P4-survivor-blocked",
    "M7-survivor-check-stubbed",
    "A01-plain-replace",
    "A02-unmatched-refuses",
    "A03-duplicate-refuses",
    "A04-h3-scope",
    "A05-fence-ignored",
    "A06-last-wins",
    "A07-chained",
    "A08-extent-sibling",
    "A09-level-mismatch-refuses",
    "A10-unclosed-fence-refuses",
    "A11-withdraw-recovers",
    "A12-withdraw-unmatched-warns",
    "A13-idempotent",
    "A14-identity-captures",
    "A22-malformed-then-withdraw-assembles",
    "A23-malformed-alone-refuses",
    "A24-unclosed-fence-recovery",
    "M8-fence-test-dropped",
    "M9-duplicate-refusal-removed",
    "M11-withdraw-skip-removed",
    "M12-unmatched-refusal-removed",
    "M13-deferred-validation-ignores-withdraw",
    "M14-unmatched-withdraw-refuses",
    "M15-unmatched-withdraw-survives",
    "A15-step4-assembles",
    "A16-step4-rerun-noop",
    "A17-step4-refusal-keeps-files",
    "A18-step4-empty-program-keeps-files",
    "A19-step4-misfiled-resolves",
    "A20-step4-not-rewrite",
    "A21-awk-dialects",
    "M10-size-guard-dropped",
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


def survivor_problems(guard) -> list[str]:
    """[] only when the guard blocks an assembled file that still carries a Replace line."""
    with tempfile.TemporaryDirectory() as td:
        cwd = Path(td)
        stamp = "20261009T120000Z"
        rel = f".first-principles/analysis-{stamp}.md"
        (cwd / ".first-principles").mkdir()
        (cwd / rel).write_text("## Answer\nx\n## Replace: X\n## X\n", encoding="utf-8")
        (cwd / ".first-principles" / f"report-{stamp}.md").write_text("# T\n")
        transcript = cwd / "t.jsonl"
        block = {"type": "tool_result", "content": rel}
        transcript.write_text(
            json.dumps({"type": "user", "message": {"role": "user", "content": [block]}})
            + "\n"
        )
        got = guard.delivery_problem(transcript, cwd)
    if isinstance(got, str) and "survives" in got:
        return []
    return ["SURVIVOR: guard passed a surviving ## Replace: line"]


# ----------------------------------------------------------- replacement-block applier


def extract_program(text: str) -> str:
    """The awk program exactly as step 4 extracts it: after the first line equal to
    "```awk", up to the next line equal to "```"."""
    out: list[str] = []
    inside = False
    for ln in text.split("\n"):
        if not inside:
            inside = ln == "```awk"
            continue
        if ln == "```":
            break
        out.append(ln)
    return "\n".join(out) + "\n" if out else ""


def shipped_program() -> str:
    return extract_program(PROGRAM_SRC.read_text(encoding="utf-8"))


def awk_dialects() -> list[tuple[str, list[str]]]:
    """(label, argv) for every awk implementation on PATH, first label per binary kept."""
    cands: list[tuple[str, list[str]]] = []
    for name in ("gawk", "mawk", "original-awk", "nawk"):
        if shutil.which(name):
            cands.append((name, [shutil.which(name)]))
    if shutil.which("busybox"):
        cands.append(("busybox awk", [shutil.which("busybox"), "awk"]))
    if shutil.which("gawk"):
        cands.append(("gawk --posix", [shutil.which("gawk"), "--posix"]))
    if shutil.which("awk"):
        cands.append(("awk", [shutil.which("awk")]))
    seen: set[tuple] = set()
    out: list[tuple[str, list[str]]] = []
    for label, argv in cands:
        key = (os.path.realpath(argv[0]), tuple(argv[1:]))
        if key not in seen:
            seen.add(key)
            out.append((label, argv))
    return out


def dialect_problems(labels: list[str], required: str) -> list[str]:
    problems: list[str] = []
    if not labels:
        problems.append("DIALECT-NONE: no awk implementation found on PATH")
    for want in [w.strip() for w in required.split(",") if w.strip()]:
        if want not in labels:
            problems.append(f"DIALECT-REQUIRED: {want!r} did not run (ran: {labels})")
    return problems


def apply(prog: Path, argv: list[str], text: str) -> tuple[int, str, str]:
    proc = subprocess.run(
        argv + ["-f", str(prog)],
        input=text.encode("utf-8", "surrogateescape"),
        capture_output=True,
        check=False,
    )
    return (
        proc.returncode,
        proc.stdout.decode("utf-8", "surrogateescape"),
        proc.stderr.decode("utf-8", "surrogateescape"),
    )


def _t(*lines: str) -> str:
    return "\n".join(lines) + "\n"


def _assembles(want: str):
    def chk(rc: int, out: str, err: str) -> list[str]:
        if rc == 0 and out == want:
            return []
        return [f"rc={rc} stdout={out!r} stderr={err!r}, wanted {want!r}"]

    return chk


def _refuses(*needles: str):
    def chk(rc: int, out: str, err: str) -> list[str]:
        if rc != 0 and out == "" and all(n in err for n in needles):
            return []
        return [f"rc={rc} stdout={out!r} stderr={err!r}, wanted refusal naming {needles}"]

    return chk


def _warns(want: str, line: str):
    def chk(rc: int, out: str, err: str) -> list[str]:
        if rc == 0 and out == want and line in err.split("\n"):
            return []
        return [f"rc={rc} stdout={out!r} stderr={err!r}, wanted {want!r} and {line!r}"]

    return chk


_FENCE = "`" * 3
_A24_BASE = (
    "## A",
    "old",
    "## B",
    "b",
    "## Replace: A",
    "## A",
    _FENCE,
    "## Replace: B",
    "## B",
    "b2",
)

_FIXTURES = [
    (
        "A01-plain-replace",
        _t("## A", "old", "## B", "keep", "## Replace: A", "## A", "new"),
        _assembles(_t("## A", "new", "## B", "keep")),
    ),
    (
        "A02-unmatched-refuses",
        _t("## A", "x", "## Replace: Nope", "## Nope", "y"),
        _refuses("NOT ASSEMBLED: no heading matches"),
    ),
    (
        "A03-duplicate-refuses",
        _t("## A", "x", "## A", "y", "## Replace: A", "## A", "z"),
        _refuses("2 headings match"),
    ),
    (
        "A04-h3-scope",
        _t("## 4", "### C1", "x", "### C2", "y", "## 5", "z", "## Replace: C1", "### C1", "x2"),
        _assembles(_t("## 4", "### C1", "x2", "### C2", "y", "## 5", "z")),
    ),
    (
        "A05-fence-ignored",
        _t(
            "## A", "old", "## B", _FENCE, "## A", "## Replace: A", _FENCE,
            "## Replace: A", "## A", "new",
        ),
        _assembles(_t("## A", "new", "## B", _FENCE, "## A", "## Replace: A", _FENCE)),
    ),
    (
        "A06-last-wins",
        _t("## A", "old", "## Replace: A", "## A", "n1", "## Replace: A", "## A", "n2"),
        _assembles(_t("## A", "n2")),
    ),
    (
        "A07-chained",
        _t("## A", "old", "## Replace: A", "## A2", "mid", "## Replace: A2", "## A2", "fin"),
        _assembles(_t("## A2", "fin")),
    ),
    (
        "A08-extent-sibling",
        _t(
            "## 4", "### C1", "x", "### C2", "y", "## Replace: C1", "### C1", "x2",
            "### C1b", "z",
        ),
        _assembles(_t("## 4", "### C1", "x2", "### C1b", "z", "### C2", "y")),
    ),
    (
        "A09-level-mismatch-refuses",
        _t("## A", "old", "## Replace: A", "### A", "new"),
        _refuses("opens a level-3 heading but the target is level 2"),
    ),
    (
        "A10-unclosed-fence-refuses",
        _t("## A", "old", _FENCE, "## Replace: A", "## A", "new"),
        _refuses("is never closed"),
    ),
    (
        "A11-withdraw-recovers",
        _t(
            "## A", "old", "## Replace: Z", "## Z", "q", "## Withdraw: Z",
            "## Replace: A", "## A", "new",
        ),
        _assembles(_t("## A", "new")),
    ),
    (
        "A12-withdraw-unmatched-warns",
        _t("## A", "x", "## Withdraw: Q"),
        _warns(_t("## A", "x"), "WARNING: withdraw matched nothing: Q"),
    ),
    (
        "A22-malformed-then-withdraw-assembles",
        _t(
            "## A", "old", "## Replace: A", "not a heading", "## Withdraw: A",
            "## Replace: A", "## A", "new",
        ),
        _assembles(_t("## A", "new")),
    ),
    (
        "A23-malformed-alone-refuses",
        _t("## A", "old", "## Replace: A", "not a heading"),
        _refuses("does not start with a ## or ### heading line"),
    ),
    (
        "A24-unclosed-fence-recovery",
        _t(*_A24_BASE),
        _refuses("is never closed"),
    ),
]

_A24_RECOVERED = _t(
    *_A24_BASE, _FENCE, "## Withdraw: A", "## Replace: B", "## B", "b2"
)
_A13_INPUT = dict((f[0], f[1]) for f in _FIXTURES)["A08-extent-sibling"]


def _lvl(s: str) -> int:
    c = 0
    while s[c : c + 1] == "#":
        c += 1
    if c < 1 or c > 6 or s[c : c + 1] != " ":
        return 0
    return c


def _htext(s: str) -> str:
    return s[_lvl(s) + 1 :].rstrip(" \t\r")


def identity_input(text: str) -> str | None:
    """text plus an identity replacement of every ##/### heading, or None to skip."""
    if "\r" in text or not text.strip():
        return None
    if not text.endswith("\n"):
        text += "\n"
    lines = text.split("\n")[:-1]
    heads: list[tuple[int, int, str]] = []
    fenced = False
    for i, ln in enumerate(lines):
        if ln.startswith(_FENCE):
            fenced = not fenced
        elif not fenced and _lvl(ln):
            heads.append((i, _lvl(ln), _htext(ln)))
    texts = [h[2] for h in heads]
    if fenced or len(set(texts)) != len(texts):
        return None
    if any(t.startswith(("Replace: ", "Withdraw: ")) for t in texts):
        return None
    out = list(lines)
    for k, (i, level, htxt) in enumerate(heads):
        if level not in (2, 3):
            continue
        end = len(lines)
        for i2, l2, _ in heads[k + 1 :]:
            if l2 <= level:
                end = i2
                break
        out.append("## Replace: " + htxt)
        out.extend(lines[i:end])
    return "\n".join(out) + "\n"


_IDENTITY_CACHE: list | None = None


def identity_cases() -> tuple[list[tuple[str, str]], int]:
    global _IDENTITY_CACHE
    if _IDENTITY_CACHE is None:
        cases: list[tuple[str, str]] = []
        skipped = 0
        for root in _IDENTITY_ROOTS:
            for f in sorted(root.glob("*.files/analysis-*.md")):
                text = f.read_text(encoding="utf-8", errors="surrogateescape")
                built = identity_input(text)
                if built is None:
                    skipped += 1
                    continue
                want = text if text.endswith("\n") else text + "\n"
                name = f"{root.parent.name}/{f.parent.name}"
                cases.append((name, built))
                _IDENTITY_WANT[name] = want
        _IDENTITY_CACHE = [cases, skipped]
    return _IDENTITY_CACHE[0], _IDENTITY_CACHE[1]


_IDENTITY_WANT: dict[str, str] = {}
_LAST_IDENTITY = {"files": 0, "skipped": 0, "mismatches": 0}


def applier_problems(
    program: str, only: set[str] | None = None, dialects=None
) -> dict[str, list[str]]:
    """{control id: problems}, each problem naming its dialect."""
    dialects = awk_dialects() if dialects is None else dialects
    ids = [f[0] for f in _FIXTURES] + ["A13-idempotent", "A14-identity-captures"]
    res: dict[str, list[str]] = {i: [] for i in ids if only is None or i in only}
    if not program.strip():
        for cid in res:
            res[cid].append("PROGRAM-EMPTY: no awk program extracted")
        return res
    with tempfile.TemporaryDirectory() as td:
        prog = Path(td) / "replace.awk"
        prog.write_text(program, encoding="utf-8")
        for label, argv in dialects:
            for cid, text, chk in _FIXTURES:
                if cid not in res:
                    continue
                res[cid] += [f"[{label}] {p}" for p in chk(*apply(prog, argv, text))]
            if "A24-unclosed-fence-recovery" in res:
                rc, out, err = apply(prog, argv, _A24_RECOVERED)
                want = _t("## A", "old", "## B", "b2")
                if rc != 0 or out != want:
                    res["A24-unclosed-fence-recovery"].append(
                        f"[{label}] recovery gave rc={rc} stdout={out!r} stderr={err!r}"
                    )
            if "A13-idempotent" in res:
                rc, out1, err = apply(prog, argv, _A13_INPUT)
                rc2, out2, err2 = apply(prog, argv, out1)
                if rc != 0 or rc2 != 0 or out1 != out2:
                    res["A13-idempotent"].append(
                        f"[{label}] re-run differs or failed (rc {rc}/{rc2})"
                    )
                if any(ln.startswith(("## Replace: ", "## Withdraw: ")) for ln in out1.split("\n")):
                    res["A13-idempotent"].append(f"[{label}] a marker survives")
            if "A14-identity-captures" in res:
                cases, skipped = identity_cases()
                bad = 0
                for name, built in cases:
                    rc, out, err = apply(prog, argv, built)
                    if rc != 0 or out != _IDENTITY_WANT[name]:
                        bad += 1
                        res["A14-identity-captures"].append(
                            f"[{label}] identity replacement changed {name} (rc={rc})"
                        )
                _LAST_IDENTITY.update(
                    files=len(cases),
                    skipped=skipped,
                    mismatches=(_LAST_IDENTITY['mismatches'] if label != dialects[0][0] else 0) + bad,
                )
                if len(cases) < _IDENTITY_FLOOR:
                    res["A14-identity-captures"].append(
                        f"IDENTITY-FLOOR: {len(cases)} files, floor {_IDENTITY_FLOOR}"
                    )
    return res


def _drop_line(program: str, needle: str) -> str:
    return "".join(ln for ln in program.splitlines(True) if needle not in ln)


_MUTATIONS = [
    (
        "M8-fence-test-dropped",
        "A05-fence-ignored",
        lambda p: _drop_line(p, "if (substr(C[i], 1, 3) == FENCE) { f = !f;"),
    ),
    (
        "M9-duplicate-refusal-removed",
        "A03-duplicate-refuses",
        lambda p: _drop_line(p, "if (cnt > 1) die("),
    ),
    (
        "M11-withdraw-skip-removed",
        "A11-withdraw-recovers",
        lambda p: _drop_line(p, "if (X[r]) continue"),
    ),
    (
        "M12-unmatched-refusal-removed",
        "A02-unmatched-refuses",
        lambda p: _drop_line(p, "if (cnt == 0) die("),
    ),
    (
        "M13-deferred-validation-ignores-withdraw",
        "A22-malformed-then-withdraw-assembles",
        lambda p: p.replace("!X[r] && BAD[r]", "BAD[r]", 1),
    ),
    (
        "M14-unmatched-withdraw-refuses",
        "A12-withdraw-unmatched-warns",
        lambda p: p.replace(
            'print "WARNING: withdraw matched nothing: " W > "/dev/stderr"',
            'die("withdraw matched nothing: " W)',
            1,
        ),
    ),
    (
        "M15-unmatched-withdraw-survives",
        "A12-withdraw-unmatched-warns",
        lambda p: p.replace("i += 1", "B[++nb] = C[i]; i += 1", 1),
    ),
]


def mutation_problems(mutate, target: str, program: str) -> list[str]:
    mutated = mutate(program)
    if mutated == program:
        return ["MUTATION-VACUOUS: the mutation left the program text unchanged"]
    return applier_problems(mutated, only={target}).get(target, [])


# ------------------------------------------------------------- step 4, end to end


def step4_command(text: str | None = None) -> str:
    """The one-line sh command of step 4, read from the shipped agent, never copied."""
    text = AGENT_MD.read_text(encoding="utf-8") if text is None else text
    m = re.search(
        r"^4\. \*\*Assemble once[^\n]*\n\s*```sh\n(.*?)\n\s*```", text, re.S | re.M
    )
    if not m:
        raise ValueError("STEP4-MISSING: no sh block after '4. **Assemble once'")
    lines = [ln.strip() for ln in m.group(1).split("\n")]
    if len(lines) != 1 or not lines[0]:
        raise ValueError(f"STEP4-SHAPE: expected one command line, found {len(lines)}")
    return lines[0]


def _snapshot(d: Path) -> dict[str, bytes]:
    fp = d / ".first-principles"
    return {f.name: f.read_bytes() for f in sorted(fp.iterdir())}


def _run_step4(cmd: str, d: Path, bindir: Path, plugin_root: Path):
    full = cmd.replace("<path>", ".first-principles/analysis-T.md")
    return subprocess.run(
        [
            "env", "-i", f"PATH={bindir}:/usr/bin:/bin",
            f"CLAUDE_PLUGIN_ROOT={plugin_root}", "bash", "-c", full,
        ],
        cwd=d,
        capture_output=True,
        text=True,
        check=False,
    )


def _has_marker(text: str) -> bool:
    fenced = False
    for ln in text.split("\n"):
        if ln.startswith(_FENCE):
            fenced = not fenced
        elif not fenced and ln.startswith(("## Replace: ", "## Withdraw: ")):
            return True
    return False


def step4_problems(cmd: str, label: str, argv: list[str]) -> dict[str, list[str]]:
    ids = (
        "A15-step4-assembles",
        "A16-step4-rerun-noop",
        "A17-step4-refusal-keeps-files",
        "A18-step4-empty-program-keeps-files",
        "A19-step4-misfiled-resolves",
    )
    res: dict[str, list[str]] = {i: [] for i in ids}
    leftovers = (".answer", ".process", ".apply", ".tmp")

    def fail(cid: str, msg: str) -> None:
        res[cid].append(f"[{label}] {msg}")

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        bindir = root / "bin"
        bindir.mkdir()
        wrapper = bindir / "awk"
        wrapper.write_text(
            "#!/bin/sh\nexec " + " ".join(shlex.quote(a) for a in argv) + ' "$@"\n'
        )
        wrapper.chmod(0o755)
        empty_root = root / "empty-plugin"
        (empty_root / "references").mkdir(parents=True)
        (empty_root / "references" / "replace-blocks.md").write_text("no program\n")

        def case(name: str, main: str, process: str, answer: str) -> Path:
            d = root / name
            (d / ".first-principles").mkdir(parents=True)
            base = d / ".first-principles" / "analysis-T.md"
            base.write_text(main)
            base.with_name("analysis-T.md.process").write_text(process)
            base.with_name("analysis-T.md.answer").write_text(answer)
            return d

        def stray(d: Path) -> list[str]:
            return [
                f.name
                for f in (d / ".first-principles").iterdir()
                if f.name.endswith(leftovers)
            ]

        # A15 / A16
        d = case(
            "a15",
            "## 1. Essence\ntext\n## Replace: 1. Essence\n## 1. Essence\nfixed\n",
            "## Appendix — process output\nfoo\n",
            "## Answer\nans\n",
        )
        proc = _run_step4(cmd, d, bindir, PLUGIN)
        out = (d / ".first-principles" / "analysis-T.md").read_text()
        if proc.returncode != 0 or not out.startswith("## Answer\n"):
            fail("A15-step4-assembles", f"rc={proc.returncode} err={proc.stderr!r} out={out!r}")
        elif "fixed" not in out or "text" in out or _has_marker(out):
            fail("A15-step4-assembles", f"replacement not applied cleanly: {out!r}")
        if stray(d):
            fail("A15-step4-assembles", f"working files left behind: {stray(d)}")
        before = _snapshot(d)
        proc = _run_step4(cmd, d, bindir, PLUGIN)
        if "already assembled" not in proc.stdout or _snapshot(d) != before:
            fail("A16-step4-rerun-noop", f"stdout={proc.stdout!r}, or files changed")

        # A17: a refusal keeps every file
        d = case(
            "a17",
            "## 1. Essence\ntext\n",
            "## Appendix\nfoo\n## Replace: Nope\n## Nope\nx\n",
            "## Answer\nans\n",
        )
        before = _snapshot(d)
        proc = _run_step4(cmd, d, bindir, PLUGIN)
        if "NOT ASSEMBLED:" not in proc.stdout + proc.stderr:
            fail("A17-step4-refusal-keeps-files", f"no refusal text: {proc.stderr!r}")
        if _snapshot(d) != before:
            fail("A17-step4-refusal-keeps-files", "files changed or working files left")

        # A18: an empty extracted program keeps every file
        d = case("a18", "## 1. Essence\ntext\n", "## Appendix\nfoo\n", "## Answer\nans\n")
        before = _snapshot(d)
        _run_step4(cmd, d, bindir, empty_root)
        if _snapshot(d) != before:
            fail("A18-step4-empty-program-keeps-files", "files changed or working files left")

        # A19: a replacement misfiled in .process still resolves
        d = case(
            "a19",
            "## 1. Essence\ntext\n## 2. Next\nn\n",
            "## Appendix\nfoo\n## Replace: 1. Essence\n## 1. Essence\nfixed\n",
            "## Answer\nans\n",
        )
        proc = _run_step4(cmd, d, bindir, PLUGIN)
        out = (d / ".first-principles" / "analysis-T.md").read_text()
        if proc.returncode != 0 or "fixed" not in out or "text" in out or _has_marker(out):
            fail("A19-step4-misfiled-resolves", f"rc={proc.returncode} out={out!r}")
    return res


def phase_turns_problems(cmd: str) -> list[str]:
    spec = importlib.util.spec_from_file_location("phase_turns", PHASE_TURNS)
    pt = importlib.util.module_from_spec(spec)
    sys.modules["phase_turns"] = pt
    spec.loader.exec_module(pt)
    real = cmd.replace("<path>", ".first-principles/analysis-20261009T120000Z.md")
    problems = []
    if pt.is_rewrite(real) is not False:
        problems.append("REWRITE: phase_turns counts step 4 as a rewrite")
    if "assemble" not in pt.classify(real):
        problems.append(f"CLASSIFY: step 4 is not classified assemble: {pt.classify(real)}")
    return problems


def step4_all(cmd: str, dialects) -> dict[str, list[str]]:
    merged: dict[str, list[str]] = {}
    for label, argv in dialects:
        for cid, probs in step4_problems(cmd, label, argv).items():
            merged.setdefault(cid, []).extend(probs)
    return merged


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

    control("P4-survivor-blocked", survivor_problems(guard), False)
    saved_sm = guard.surviving_marker
    guard.surviving_marker = lambda p: None
    try:
        stubbed = survivor_problems(guard)
    finally:
        guard.surviving_marker = saved_sm
    control("M7-survivor-check-stubbed", stubbed, True)

    labels = [lb for lb, _ in awk_dialects()]
    print(f"check-delivery-guard --self-test: awk dialects run: {', '.join(labels)}")
    program = shipped_program()
    got = applier_problems(program)
    for cid in _CONTROL_IDS:
        if cid in got and cid != "A14-identity-captures":
            control(cid, got[cid], False)
    control("A14-identity-captures", got["A14-identity-captures"], False)
    print(
        "check-delivery-guard --self-test: A14 identity files "
        f"{_LAST_IDENTITY['files']} (skipped {_LAST_IDENTITY['skipped']}, "
        f"mismatches {_LAST_IDENTITY['mismatches']})"
    )
    for mid, target, mutate in _MUTATIONS:
        control(mid, mutation_problems(mutate, target, program), True)

    dialects = awk_dialects()
    try:
        cmd = step4_command()
    except ValueError as exc:
        cmd = ""
        for cid in ("A15-step4-assembles", "A16-step4-rerun-noop",
                    "A17-step4-refusal-keeps-files", "A18-step4-empty-program-keeps-files",
                    "A19-step4-misfiled-resolves", "A20-step4-not-rewrite", "M10-size-guard-dropped"):
            control(cid, [str(exc)], False)
    if cmd:
        s4 = step4_all(cmd, dialects)
        for cid in (
            "A15-step4-assembles",
            "A16-step4-rerun-noop",
            "A17-step4-refusal-keeps-files",
            "A18-step4-empty-program-keeps-files",
            "A19-step4-misfiled-resolves",
        ):
            control(cid, s4[cid], False)
        control("A20-step4-not-rewrite", phase_turns_problems(cmd), False)
        required = os.environ.get("FP_REQUIRE_AWK_DIALECTS", "")
        a21 = dialect_problems(labels, required)
        if not dialect_problems(labels, "no-such-awk"):
            a21.append("A21 requirement path cannot fail")
        control("A21-awk-dialects", a21, False)
        mutated = cmd.replace(' && [ -s "$A" ]', "", 1)
        if mutated == cmd:
            m10 = ["MUTATION-VACUOUS: the mutation left the command unchanged"]
        else:
            m10 = step4_all(mutated, dialects)["A18-step4-empty-program-keeps-files"]
        control("M10-size-guard-dropped", m10, True)

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
            "first-principles/references/replace-blocks.md",
            "first-principles/agents/first-principles.md",
        ],
        "disclosed_bounds_anchors": [
            "decides delivery from the file on disk, never from the analysis's quality",
            "blocks at most twice per run, then lets the stop through",
            "whether a blocked agent then delivers is a live reading, never gated",
            "awk implementations absent from the machine are untested",
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
