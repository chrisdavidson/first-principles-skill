#!/usr/bin/env python3
"""answer-first -- the live confirmation pre-registered in docs/answer-first-protocol.md.

    python3 tests/answer-first/run.py probe --cwd <empty dir>
    python3 tests/answer-first/run.py run --cwd <empty dir outside the repo> [--only TB-NN]
    python3 tests/answer-first/run.py read
    python3 tests/answer-first/run.py --self-test

Confirms that a delivered analysis opens with a chain-cited `## Answer` block, keeps the six
contract sections unchanged and in order, and moves every process-output block to a trailing
`## Appendix -- process output` heading -- against criteria (a)-(e), the protocol's registered
definitions, verbatim. A measurement tool: N=3 on one model shows the rule working on these
runs, not a rate, and this script gates nothing on its own.

Modelled on tests/example-rerun/run_examples.py, which itself loads
tests/delivery-fix-3/run_fix3.py for `dl`/`stage_a`/`qh` -- the same chain is reused here so the
extraction, capture and dispatch-classification logic is not reimplemented a third time.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
RAW = HERE / "raw"
DOCS = HERE / "documents"
PLUGIN_DIR = REPO_ROOT / "first-principles"
AGENT_BODY = PLUGIN_DIR / "agents" / "first-principles.md"

spec = importlib.util.spec_from_file_location("_fxaf", REPO_ROOT / "tests/delivery-fix-3/run_fix3.py")
fx = importlib.util.module_from_spec(spec)
sys.modules["_fxaf"] = fx
spec.loader.exec_module(fx)
dl, stage_a, qh = fx.dl, fx.stage_a, fx.dl.p1.qh

# --- pre-registered protocol (docs/answer-first-protocol.md) -------------------------------
MODEL = "claude-sonnet-5"
CATALOG = "tests/trackb-catalog-v9.13.md"
PROMPTS = ("TB-01", "TB-04", "TB-08")   # software, policy, science -- TB-04 is the stage-A specimen
MAX_ATTEMPTS = 3

# D-G: acceptEdits plus an enumerated Bash-prefix allowlist, never bypassPermissions and never a
# bare `Bash` entry. The agent's own frontmatter already disallows Write/Edit/Agent/SendMessage/
# ListAgents; these are the Bash prefixes its own delivery mechanics need.
ALLOWED_TOOLS: tuple[str, ...] = (
    "Read", "Glob", "Grep", "WebFetch", "WebSearch",
    "Bash(mkdir:*)", "Bash(cat:*)", "Bash(printf:*)", "Bash(echo:*)",
    "Bash(date:*)", "Bash(grep:*)", "Bash(wc:*)", "Bash(mv:*)",
    "Bash(rm:*)", "Bash(ls:*)", "Bash(head:*)", "Bash(sed:*)",
)
# ---------------------------------------------------------------------------------------------

_CHAIN_TOKEN_RE = re.compile(r"\bC\d+\b")
_ANSWER_HEADING_RE = re.compile(r"^## Answer[ \t]*$", re.M)
_CRITERION_C_BAN_RE = re.compile(
    r"(?i)process output|assumption audit|adversarial pass|closure ledger|self-audit"
    r"|techniques not applied|appendix"
)
_TECHNIQUES_NOT_APPLIED_RE = re.compile(r"^\**Techniques not applied", re.I)
_INLINE_CODE_RE = re.compile(r"`([^`\n]+)`")


def live_argv(prompt: str, plugin_dir: Path) -> list[str]:
    """The argv a live run dispatches with -- D-G, refusing bypassPermissions by construction."""
    return [
        "claude", "-p", "--model", MODEL, "--plugin-dir", str(plugin_dir),
        "--output-format", "stream-json", "--verbose",
        "--permission-mode", "acceptEdits",
        "--allowedTools", " ".join(ALLOWED_TOOLS),
        prompt,
    ]


def _generate(argv: list[str], cwd: Path, raw_path: Path) -> str:
    assert "bypassPermissions" not in argv, "refusing to dispatch with bypassPermissions"
    assert "Bash" not in argv, "refusing a bare Bash entry in the allowlist"
    env = {**os.environ, "CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS": "0"}
    proc = subprocess.run(argv, capture_output=True, text=True, timeout=5400, env=env, cwd=cwd)
    raw_path.write_text(proc.stdout, encoding="utf-8")
    return proc.stdout


def _permission_denials(jsonl: str) -> list:
    """The last `result` event's `permission_denials` field (empty if none, or absent)."""
    denials: list = []
    for obj in dl.p0._events(jsonl):
        if obj.get("type") == "result":
            denials = obj.get("permission_denials") or []
    return denials


def _collect_all_files(cwd: Path, dest: Path) -> list[Path]:
    """Copy EVERY file under <cwd>/.first-principles/ (not just *.md) so a leftover
    .answer/.process/.tmp side file is preserved as evidence rather than silently swept by the
    next run's cleanup -- fx.collect_files globs *.md only, which would hide exactly the
    failure mode this protocol's `side files left` observation exists to catch."""
    src = cwd / ".first-principles"
    out: list[Path] = []
    if src.is_dir():
        dest.mkdir(parents=True, exist_ok=True)
        for f in sorted(src.iterdir()):
            if f.is_file():
                shutil.copy2(f, dest / f.name)
                out.append(dest / f.name)
        shutil.rmtree(src, ignore_errors=True)
    for leftover in cwd.iterdir():
        shutil.rmtree(leftover, ignore_errors=True) if leftover.is_dir() else leftover.unlink()
    return out


# ---------------------------------------------------------------------------------------------
# Criteria (a)-(e) -- the protocol's registered definitions, verbatim (docs/answer-first-protocol.md)
# ---------------------------------------------------------------------------------------------

def _first_heading_outside_fence(doc: str) -> str | None:
    lines = doc.splitlines()
    fenced = qh._fenced_code_flags(lines)
    for i, line in enumerate(lines):
        if fenced[i]:
            continue
        if re.match(r"^#{1,6}[ \t]+\S", line):
            return line.strip()
    return None


def _answer_body(doc: str) -> str | None:
    """From the `## Answer` heading line to the next heading (exclusive), or None if absent."""
    m = _ANSWER_HEADING_RE.search(doc)
    if not m:
        return None
    rest = doc[m.end():]
    m2 = re.search(r"^#{1,6}[ \t]", rest, re.M)
    return rest[: m2.start()] if m2 else rest


def criterion_a(doc: str) -> tuple[bool, str]:
    """(a) qh._slice_sections(doc) resolves."""
    try:
        qh._slice_sections(doc)
        return True, "resolves"
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def criterion_b(doc: str) -> tuple[bool, str]:
    """(b) the first line outside fences matching ^## is exactly `## Answer`."""
    first = _first_heading_outside_fence(doc)
    return first == "## Answer", f"first heading: {first!r}"


def criterion_c(doc: str) -> tuple[bool, str]:
    """(c) no heading before `## 6. Conclusion` matches the process-output vocabulary, and no
    line before it starts with (optionally bolded) 'Techniques not applied'."""
    lines = doc.splitlines()
    fenced = qh._fenced_code_flags(lines)
    concl_idx = None
    for i, line in enumerate(lines):
        if not fenced[i] and re.match(r"^#{1,6}[ \t]", line) and "6. Conclusion" in line:
            concl_idx = i
            break
    if concl_idx is None:
        return False, "no '## 6. Conclusion' heading found"
    for j in range(concl_idx):
        if fenced[j]:
            continue
        stripped = lines[j].strip()
        if re.match(r"^#{1,6}[ \t]", lines[j]) and _CRITERION_C_BAN_RE.search(lines[j]):
            return False, f"banned heading before section 6: {stripped!r}"
        if _TECHNIQUES_NOT_APPLIED_RE.match(stripped):
            return False, f"'Techniques not applied' line before section 6: {stripped!r}"
    return True, "clean"


def criterion_d(doc: str) -> tuple[bool, str]:
    """(d) the Answer body contains >=1 chain token, and every such token is in section 4's
    chain ids."""
    body = _answer_body(doc)
    if body is None:
        return False, "no '## Answer' heading"
    tokens = sorted(set(_CHAIN_TOKEN_RE.findall(body)))
    if not tokens:
        return False, "no chain token (Cn) cited in the Answer body"
    try:
        sections = qh._slice_sections(doc)
        # `qh._chain_ids` returns each id in its STORED form ("Conclusion C1", "Chain C1", or
        # a bare "C1") -- normalise both sides the same way `_cites_chain` does, so a bare
        # `(chain C1)` citation matches a "### Conclusion C1: ..." heading correctly.
        valid = {qh._normalize_chain_id(cid) for cid in qh._chain_ids(sections[4])}
    except Exception as exc:  # noqa: BLE001
        return False, f"could not resolve section 4 chain ids: {exc}"
    bad = sorted(t for t in tokens if qh._normalize_chain_id(t) not in valid)
    if bad:
        return False, f"Answer cites chain(s) absent from section 4: {bad}"
    return True, f"chains cited: {tokens}"


def criterion_e(doc: str) -> tuple[bool, str]:
    """(e) len(answer_body.split()) <= 150, heading line excluded."""
    body = _answer_body(doc)
    if body is None:
        return False, "no '## Answer' heading"
    n = len(body.split())
    return n <= 150, f"{n} words"


def score_document(doc: str) -> dict[str, tuple[bool, str]]:
    return {
        "a": criterion_a(doc), "b": criterion_b(doc), "c": criterion_c(doc),
        "d": criterion_d(doc), "e": criterion_e(doc),
    }


def observe(doc: str) -> dict:
    """Observations alongside the pass/fail criteria: total words, words before section 1,
    appendix word share, and whether every Answer chain is also cited in section 6."""
    total_words = len(doc.split())
    m1 = re.search(r"^#{1,3}[ \t]+1\.?[ \t]+Problem Essence", doc, re.M | re.I)
    words_before_1 = len(doc[: m1.start()].split()) if m1 else None
    appx = re.search(r"^## Appendix — process output[ \t]*$", doc, re.M)
    appendix_words = len(doc[appx.start():].split()) if appx else 0
    appendix_share = round((appendix_words / total_words), 3) if total_words else 0.0
    chains_in_6 = None
    body = _answer_body(doc)
    if body is not None:
        answer_chains = sorted(set(_CHAIN_TOKEN_RE.findall(body)))
        try:
            sections = qh._slice_sections(doc)
            chains_in_6 = (
                all(c in sections[6] for c in answer_chains) if answer_chains else None
            )
        except Exception:  # noqa: BLE001
            chains_in_6 = None
    return {
        "total_words": total_words,
        "words_before_section_1": words_before_1,
        "appendix_word_share": appendix_share,
        "answer_chains_all_cited_in_section_6": chains_in_6,
    }


# ---------------------------------------------------------------------------------------------
# run / probe / read
# ---------------------------------------------------------------------------------------------

def cmd_run(cwd: Path, only: str | None) -> int:
    if any(cwd.iterdir()):
        raise SystemExit(f"--cwd {cwd} is not empty")
    RAW.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    cells_path = HERE / "cells.json"
    cells = json.loads(cells_path.read_text()) if cells_path.is_file() else {}
    pids = [only] if only else list(PROMPTS)
    for pid in pids:
        if cells.get(pid, {}).get("outcome") == "scored":
            print(f"[gen] {pid} (recorded)", flush=True)
            continue
        prompt = dl.p1.prompt_text(pid, CATALOG)
        subdir = cwd / pid
        subdir.mkdir(parents=True, exist_ok=True)
        attempts: list[str] = []
        outcome = "exhausted"
        denials: list = []
        dispatched = None
        for n in range(1, MAX_ATTEMPTS + 1):
            raw = RAW / f"{pid}.a{n}.jsonl"
            argv = live_argv(prompt, PLUGIN_DIR)
            print(f"[gen] {pid} attempt {n} ...", flush=True)
            jsonl = _generate(argv, subdir, raw)
            dl.capture_agent_transcripts(jsonl, RAW / f"{pid}.a{n}.agent")
            files = _collect_all_files(subdir, RAW / f"{pid}.a{n}.files")
            attempts.append(raw.name)
            if dl.w4.is_limit_stub(jsonl):
                raw.rename(RAW / f"{pid}.a{n}.limit-stub.jsonl")
                print(f"[pause] {pid}: usage-limit stub; re-run to resume", flush=True)
                return 3
            loaded = dl.w4.loaded_body(jsonl)
            if loaded != [str(PLUGIN_DIR)]:
                print(f"[abort] {pid}: loaded {loaded}, not the working-tree plugin", flush=True)
                return 5
            denials = _permission_denials(jsonl)
            fp_denials = [d for d in denials if ".first-principles" in json.dumps(d)]
            if fp_denials:
                print(f"[void-permission] {pid} attempt {n}: {fp_denials}", flush=True)
                return 4
            r = dl.p1.classify(raw, "answer-first")
            dispatched = r.get("dispatched")
            if not dispatched:
                print(f"[miss] {pid} attempt {n}: not dispatched", flush=True)
                continue
            candidates = sorted((p for p in files if p.name.startswith("analysis-")
                                 and p.suffix == ".md"), key=lambda p: p.stat().st_size)
            if not candidates:
                print(f"[miss] {pid} attempt {n}: no assembled analysis-*.md file", flush=True)
                continue
            docfile = candidates[-1]
            (DOCS / f"{pid}.md").write_text(docfile.read_text(encoding="utf-8"), encoding="utf-8")
            outcome = "scored"
            break
        cells[pid] = {
            "outcome": outcome, "attempts": attempts,
            "loaded_body": loaded if attempts else None,
            "dispatched": dispatched, "permission_denials": denials,
        }
        cells_path.write_text(json.dumps(cells, indent=2) + "\n", encoding="utf-8")
        print(f"[gen] {pid} {outcome.upper()}", flush=True)
    return 0


def cmd_probe(cwd: Path) -> int:
    """One cheap transport check: no --plugin-dir, same permission flags, asks the model to run
    the body's own create and assemble commands verbatim on dummy files. Not a registered run."""
    if any(cwd.iterdir()):
        raise SystemExit(f"--cwd {cwd} is not empty")
    RAW.mkdir(parents=True, exist_ok=True)
    body_text = AGENT_BODY.read_text(encoding="utf-8")
    create_cmd = _extract_inline_command(body_text, ".first-principles/analysis-")
    assemble_cmd = _extract_inline_command(body_text, '"<path>.answer"')
    if not create_cmd or not assemble_cmd:
        raise SystemExit("probe: could not locate the create/assemble commands in the body")
    prompt = (
        "Run this Bash command verbatim: " + create_cmd + " -- then write the word 'dummy' "
        "into the file it printed and into that same path with '.answer' appended, then run "
        "this Bash command verbatim, substituting the printed path for every <path>: "
        + assemble_cmd + " Report the exact text of any permission denial you receive; do not "
        "ask me anything, just attempt the commands."
    )
    argv = [
        "claude", "-p", "--model", MODEL, "--output-format", "stream-json", "--verbose",
        "--permission-mode", "acceptEdits", "--allowedTools", " ".join(ALLOWED_TOOLS), prompt,
    ]
    assert "bypassPermissions" not in argv
    raw_path = RAW / "probe.jsonl"
    env = {**os.environ, "CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS": "0"}
    proc = subprocess.run(argv, capture_output=True, text=True, timeout=600, env=env, cwd=cwd)
    raw_path.write_text(proc.stdout, encoding="utf-8")
    denials = _permission_denials(proc.stdout)
    print(f"probe: permission_denials = {denials}")
    return 1 if denials else 0


def cmd_read() -> int:
    cells_path = HERE / "cells.json"
    cells = json.loads(cells_path.read_text()) if cells_path.is_file() else {}
    runs: dict[str, dict] = {}
    for pid in PROMPTS:
        doc_path = DOCS / f"{pid}.md"
        if not doc_path.is_file():
            continue
        doc = doc_path.read_text(encoding="utf-8")
        scores = score_document(doc)
        obs = observe(doc)
        side_files: list[str] = []
        for n in range(1, MAX_ATTEMPTS + 1):
            d = RAW / f"{pid}.a{n}.files"
            if d.is_dir():
                side_files = sorted(p.name for p in d.iterdir() if not p.name.endswith(".md"))
        obs["side_files_left"] = side_files
        passed = all(v[0] for v in scores.values())
        runs[pid] = {
            "scores": {k: {"pass": v[0], "evidence": v[1]} for k, v in scores.items()},
            "observations": obs, "pass": passed,
            "cell": cells.get(pid),
        }
    print(f"answer-first -- reading (N={len(runs)}, an observation against the registered rule, "
          f"never a gate)\n")
    for pid, r in runs.items():
        print(f"{pid}: pass={r['pass']}  " +
              "  ".join(f"{k}={v['pass']}" for k, v in r["scores"].items()))
    (HERE / "result.json").write_text(
        json.dumps({"runs": runs}, indent=2) + "\n", encoding="utf-8")
    return 0


# ---------------------------------------------------------------------------------------------
# --self-test -- S1-S7 (criteria scorer + argv) and M1 (mechanics replay, W2 idempotency)
# ---------------------------------------------------------------------------------------------

_FIXTURE_CHAIN = (
    "### Conclusion C1: The claim\n\n"
    "```text\n"
    "GT-1 (a fact)\n"
    "→ an intermediate claim\n"
    "→ the conclusion\n"
    "```\n\n"
    "**Confidence:** HIGH\n"
)

_FIXTURE_BASE = (
    "# 1. Problem Essence\n\nOne sentence.\n\n"
    "## 2. Assumptions Table\n\n| Assumption | Type |\n|---|---|\n| A1 | belief |\n\n"
    "## 3. Ground Truths\n\n- **GT-1** A fact. source: arithmetic; read-at-source: in-entry\n\n"
    "## 4. Derivation Chains\n\n" + _FIXTURE_CHAIN + "\n"
    "## 5. Abandoned Reasoning\n\nNothing abandoned.\n\n"
    "## 6. Conclusion\n\n**Recommended approach:** Do the thing (chain C1).\n"
)

_FIXTURE_ANSWER = (
    "## Answer\n\n"
    "**Recommendation:** Do the thing (chain C1).\n"
    "**Band (from §6):** HIGH (chain C1).\n"
    "**Would change it:** No named evidence would move it (chain C1).\n\n"
)

_FIXTURE_ANSWER_BAD_CHAIN = (
    "## Answer\n\n"
    "**Recommendation:** Do the thing (chain C9).\n"
    "**Band (from §6):** HIGH (chain C9).\n"
    "**Would change it:** No named evidence would move it (chain C9).\n\n"
)

_FIXTURE_APPENDIX = (
    "\n## Appendix — process output\n\n"
    "## Self-audit scan (process output)\n\n"
    "| Chain | Band |\n|---|---|\n| C1 | HIGH |\n"
)

_FIXTURE_PASS = _FIXTURE_ANSWER + _FIXTURE_BASE + _FIXTURE_APPENDIX
_FIXTURE_S5 = _FIXTURE_ANSWER_BAD_CHAIN + _FIXTURE_BASE + _FIXTURE_APPENDIX

_FIXTURE_S4 = (
    _FIXTURE_ANSWER
    + "# 1. Problem Essence\n\nOne sentence.\n\n"
    + "## 2. Assumptions Table\n\n| Assumption | Type |\n|---|---|\n| A1 | belief |\n\n"
    + "## 3. Ground Truths\n\n- **GT-1** A fact. source: arithmetic; read-at-source: in-entry\n\n"
    + "## 4. Derivation Chains\n\n" + _FIXTURE_CHAIN + "\n"
    + "## 5. Abandoned Reasoning\n\nNothing abandoned.\n\n"
    + "## Self-audit scan (process output)\n\nleaked before the verdict blocks\n\n"
    + "## 6. Conclusion\n\n**Recommended approach:** Do the thing (chain C1).\n"
    + _FIXTURE_APPENDIX
)


def _extract_inline_command(text: str, needle: str) -> str | None:
    """The LONGEST backticked span containing *needle*.

    More than one inline-code span can contain a short substring like
    `.first-principles/analysis-` -- the opening paragraph's own descriptive
    mention of the path shape is one, the actual multi-clause shell command
    is another and much longer. Longest-match is what picks the real
    command rather than a short cross-reference to it."""
    candidates = [m.group(1) for m in _INLINE_CODE_RE.finditer(text) if needle in m.group(1)]
    return max(candidates, key=len) if candidates else None


def _m1_check_final(text: str) -> list[str]:
    problems: list[str] = []
    first = _first_heading_outside_fence(text)
    if first != "## Answer":
        problems.append(f"first heading is {first!r}, not '## Answer'")
    positions = [m.start() for m in re.finditer(r"^## Appendix — process output[ \t]*$", text, re.M)]
    if len(positions) != 1:
        problems.append(f"'## Appendix — process output' occurs {len(positions)} times, expected 1")
    else:
        concl = re.search(r"^## 6\. Conclusion[ \t]*$", text, re.M)
        if not concl or positions[0] < concl.start():
            problems.append("appendix heading does not follow '## 6. Conclusion'")
    return problems


def _m1_replay() -> bool:
    """Extract the body's own create and assemble commands verbatim and replay them in a temp
    dir. Runs the assemble command TWICE -- the second call is the retry-after-success case the
    idempotency guard exists for -- and requires no stray .answer/.process/.tmp file survives
    either call."""
    body_text = AGENT_BODY.read_text(encoding="utf-8")
    create_cmd = _extract_inline_command(body_text, ".first-principles/analysis-")
    assemble_cmd = _extract_inline_command(body_text, '"<path>.answer"')
    if not create_cmd or not assemble_cmd:
        print("  M1: could not find the create/assemble command in the body text")
        return False
    with tempfile.TemporaryDirectory() as td:
        proc = subprocess.run(["bash", "-c", create_cmd], cwd=td, capture_output=True,
                               text=True, timeout=30)
        if proc.returncode != 0:
            print(f"  M1: create command failed: {proc.stderr.strip()}")
            return False
        rel = proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else ""
        path = (Path(td) / rel).resolve()
        if not rel or not path.is_file():
            print(f"  M1: create command did not produce a file (printed {rel!r})")
            return False
        path.write_text(_FIXTURE_BASE, encoding="utf-8")
        process_path = Path(str(path) + ".process")
        if not process_path.is_file():
            print("  M1: create command did not seed the .process side file")
            return False
        with process_path.open("a", encoding="utf-8") as fh:
            fh.write("## Self-audit scan (process output)\n\n| Chain | Band |\n|---|---|\n| C1 | HIGH |\n")
        answer_path = Path(str(path) + ".answer")
        answer_path.write_text(_FIXTURE_ANSWER, encoding="utf-8")
        tmp_path = Path(str(path) + ".tmp")

        substituted = assemble_cmd.replace("<path>", str(path))

        proc1 = subprocess.run(["bash", "-c", substituted], cwd=td, capture_output=True,
                                text=True, timeout=30)
        if proc1.returncode != 0:
            print(f"  M1: assemble command (first call) failed: {proc1.stderr.strip()}")
            return False
        problems = _m1_check_final(path.read_text(encoding="utf-8"))
        if answer_path.exists() or process_path.exists() or tmp_path.exists():
            problems.append("a side file (.answer/.process/.tmp) survives the first assemble call")
        if problems:
            for p in problems:
                print(f"  M1: {p}")
            return False
        first_text = path.read_text(encoding="utf-8")

        # W2: replay the SAME assemble command a second time -- a retry after a prior success.
        proc2 = subprocess.run(["bash", "-c", substituted], cwd=td, capture_output=True,
                                text=True, timeout=30)
        if proc2.returncode != 0:
            print(f"  M1: assemble command (retried call) failed: {proc2.stderr.strip()}")
            return False
        second_text = path.read_text(encoding="utf-8")
        if second_text != first_text:
            print("  M1: a retried assemble call after success changed the file -- not idempotent")
            return False
        if answer_path.exists() or process_path.exists() or tmp_path.exists():
            print("  M1: a side file survives after a retried assemble call")
            return False
        return True


def self_test() -> int:
    checks: dict[str, bool] = {}

    checks["S1 a passing fixture scores (a)-(e) all true"] = all(
        v[0] for v in score_document(_FIXTURE_PASS).values()
    )

    s2_doc = _FIXTURE_PASS.replace(
        "## 3. Ground Truths\n\n- **GT-1** A fact. source: arithmetic; read-at-source: in-entry\n\n",
        "",
    )
    checks["S2 a document missing section 3 fails (a)"] = not criterion_a(s2_doc)[0]

    checks["S3 section 1 first (no Answer) fails (b)"] = not criterion_b(_FIXTURE_BASE)[0]

    checks["S4 a process-output heading before section 6 fails (c)"] = not criterion_c(_FIXTURE_S4)[0]

    checks["S5 an Answer citing a chain absent from section 4 fails (d)"] = not criterion_d(_FIXTURE_S5)[0]

    long_answer = (
        "## Answer\n\n**Recommendation:** " + ("word " * 200) + "(chain C1).\n"
        "**Band (from §6):** HIGH (chain C1).\n**Would change it:** none (chain C1).\n\n"
    )
    s6_doc = long_answer + _FIXTURE_BASE + _FIXTURE_APPENDIX
    checks["S6 a 200-word Answer fails (e)"] = not criterion_e(s6_doc)[0]

    argv = live_argv("prompt", PLUGIN_DIR)
    checks["S7 the live argv carries acceptEdits/--allowedTools, never bypassPermissions or a bare Bash"] = (
        "acceptEdits" in argv and "--allowedTools" in argv
        and "bypassPermissions" not in argv and "Bash" not in argv
    )

    checks["M1 the body's own create+assemble commands replay to an answer-first file; a retried "
           "assemble call is a no-op with no stray side files"] = _m1_replay()

    ok = all(checks.values())
    for name, v in checks.items():
        print(f"  {'PASS' if v else 'FAIL'}  {name}")
    print(f"answer-first --self-test: {'PASS' if ok else 'FAIL'} ({len(checks)} controls)")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("command", nargs="?", choices=("run", "probe", "read"))
    ap.add_argument("--cwd", type=Path)
    ap.add_argument("--only")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if a.command == "read":
        return cmd_read()
    if a.command == "probe":
        if not a.cwd:
            ap.error("probe needs --cwd")
        return cmd_probe(a.cwd.resolve())
    if a.command == "run":
        if not a.cwd:
            ap.error("run needs --cwd")
        return cmd_run(a.cwd.resolve(), a.only)
    ap.error("a command or --self-test is required")


if __name__ == "__main__":
    sys.exit(main())
