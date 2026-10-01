#!/usr/bin/env python3
"""structured-summary-live -- the dispatch side of the live confirmation pre-registered in
docs/structured-summary-live-protocol.md (id ``structured-summary-live``).

A measurement tool that gates nothing on its own. It never modifies agent-router: it only
invokes ``run_examples.py`` as a subprocess and imports two of its functions
(``write_summary``, ``write_decisions``) by file path, read-only.

    python3 tests/structured-summary-live/run.py probe
    python3 tests/structured-summary-live/run.py baseline
    python3 tests/structured-summary-live/run.py run --phase75-close SHA
    python3 tests/structured-summary-live/run.py collect
    python3 tests/structured-summary-live/run.py --self-test

``probe`` makes one cheap ``claude -p`` call to check headroom before any dispatch. ``baseline``
copies the 2026-09-29 baseline's figures into this repo (no ``claude`` call). ``run`` dispatches
(or resumes) the 14-example run against agent-router's ``run_examples.py``, pausing on a
usage/spend-limit stub rather than sleeping or looping, and merges rows across invocations so a
resume never loses an earlier invocation's results. ``collect`` copies the finished run's
artifacts into this repo under ``raw/``. ``--self-test`` runs offline, no network, no ``claude``.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# --- pinned constants ---------------------------------------------------------------------
HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent

ID = "structured-summary-live"
FP_REPO = "/home/chrisdavidson/Projects/first-principles-skill"
AR_DIR = Path.home() / "Projects" / "agent-router" / "integrations" / "first-principles"
RUNNER = AR_DIR / "run_examples.py"
# Read at plan time (77-runner.sha256); tests/ must not read .planning/, so the hex is a literal.
RUNNER_SHA256 = "1b9194802e482559028689c4a17f5d8cdff10d96746e7245b1c15b0e03006bf5"
# Outside this repo, beside the baseline, so each `claude` cwd matches the baseline's -- a cwd
# inside this repo would load this repo's CLAUDE.md and expose the answer keys.
OUT = AR_DIR / "runs" / "structured-summary-live"
BASELINE_DIR = AR_DIR / "runs" / "2026-09-29-examples-latest"
ENTRY = "launcher"
JOBS = 3
MAX_ATTEMPTS = 3
BASELINE_MODEL = "claude-opus-5-5"
EXPECTED_PLUGIN = REPO_ROOT / "first-principles"

RAW = HERE / "raw"
BASE = HERE / "baseline"
MANIFEST = HERE / "manifest.json"


class IdentityChanged(Exception):
    """Raised by check_identity when a resume's tested body no longer matches the manifest."""


class CollectError(Exception):
    """Raised by collect() when OUT does not hold exactly 14 example dirs."""


# --- run.jsonl readers (reimplemented, not imported -- stdlib-only, independent of test-only
# modules, per scripts/check-trackb-comparative.py's own convention) ------------------------


def events(jsonl: str) -> list[dict]:
    out = []
    for line in jsonl.splitlines():
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def is_limit_stub(jsonl: str) -> bool:
    """Corrected 2026-09-30 logic (scripts/check-trackb-comparative.py): the final `result`
    event's `is_error`/`api_error_status` decides first; the trailing-text regex fallback runs
    only when there is no final result event, or one with an empty result text."""
    last_result: dict | None = None
    for obj in events(jsonl):
        if obj.get("type") == "result":
            last_result = obj
    if last_result is not None:
        if last_result.get("is_error") or last_result.get("api_error_status") == 429:
            return True
        if (last_result.get("result") or "").strip():
            return False
    return (
        bool(re.search(r"usage limit|rate limit", jsonl[-4000:], re.I))
        and '"parent_tool_use_id":"' not in jsonl
    )


def init_event(jsonl: str) -> dict:
    """The first `type=system, subtype=init` event's model and plugins, or {} if none."""
    for obj in events(jsonl):
        if obj.get("type") == "system" and obj.get("subtype") == "init":
            return {"model": obj.get("model"), "plugins": obj.get("plugins") or []}
    return {}


def loaded_body(jsonl: str) -> list[str]:
    """Paths of every `first-principles` plugin the run's init event reports loading
    (tests/w4-paired/run_paired.py:109's idiom)."""
    return [p.get("path", "") for p in init_event(jsonl).get("plugins") or [] if p.get("name") == "first-principles"]


# --- example/attempt bookkeeping ------------------------------------------------------------


def analysis_files(out: Path, name: str) -> list[Path]:
    return sorted((out / name / ".first-principles").glob("analysis-*.md"))


def _attempt_files(out: Path, name: str) -> list[Path]:
    """Every run.jsonl this example has produced across invocations: the live one (if present)
    plus any voided-by-resume captures, oldest first."""
    d = out / name
    files = []
    if (d / "run.jsonl").is_file():
        files.append(d / "run.jsonl")
    files += sorted(d.glob("run.void-*.jsonl"))
    return files


def relaunch_targets(out: Path, manifest: dict) -> list[str]:
    """Examples with zero analysis file, below MAX_ATTEMPTS *counted* attempts. An attempt whose
    run.jsonl is a limit stub (void, not a scored attempt) is not counted."""
    del manifest  # reserved for parity with the resume call site; not needed for this derivation
    names = sorted(p.name for p in out.iterdir() if p.is_dir() and p.name != "state") if out.is_dir() else []
    targets = []
    for name in names:
        if analysis_files(out, name):
            continue
        attempts = _attempt_files(out, name)
        counted = sum(not is_limit_stub(f.read_text(errors="replace")) for f in attempts)
        if counted < MAX_ATTEMPTS:
            targets.append(name)
    return sorted(targets)


def merge_rows(invocation_row_lists: list[list[dict]]) -> list[dict]:
    """Fold invocation row-lists in order; a later invocation's row for the same example
    overrides an earlier one. Sorted by example name."""
    merged: dict[str, dict] = {}
    for rows in invocation_row_lists:
        for row in rows:
            merged[row["example"]] = row
    return [merged[k] for k in sorted(merged)]


def runner_argv(only: list[str] | None) -> list[str]:
    argv = [
        "python3", str(RUNNER),
        "--entry", ENTRY,
        "--jobs", str(JOBS),
        "--fp-repo", FP_REPO,
        "--out", str(OUT),
    ]
    if only:
        argv += ["--only", ",".join(only)]
    return argv


def load_runner():
    """agent-router's run_examples.py, loaded by file path (never imported as a package --
    agent-router is a separate project)."""
    spec = importlib.util.spec_from_file_location("_ar_run_examples", RUNNER)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# --- identity (resume safety) ---------------------------------------------------------------


def _git(*args: str, cwd: Path | None = None) -> str:
    return subprocess.run(
        ["git", *args], cwd=cwd or REPO_ROOT, capture_output=True, text=True, check=True
    ).stdout.strip()


def identity() -> dict:
    return {
        "head_sha": _git("rev-parse", "HEAD"),
        "fp_tree": _git("rev-parse", "HEAD:first-principles"),
        "shared_tree": _git("rev-parse", "HEAD:shared"),
        "checker_sha256": hashlib.sha256(
            (REPO_ROOT / "scripts" / "check-summary-block.py").read_bytes()
        ).hexdigest(),
        "runner_sha256": hashlib.sha256(RUNNER.read_bytes()).hexdigest(),
        "agent_router_head": _git("rev-parse", "HEAD", cwd=AR_DIR),
    }


_IDENTITY_KEYS = ("fp_tree", "shared_tree", "checker_sha256", "runner_sha256")


def check_identity(manifest: dict, now: str, current: dict | None = None) -> None:
    """Raises IdentityChanged if the tested plugin tree, shared/ tree, checker or runner changed
    since the run started; otherwise appends one resumed_utc entry to manifest (in place)."""
    current = current if current is not None else identity()
    changed = [k for k in _IDENTITY_KEYS if manifest.get(k) != current.get(k)]
    if changed:
        raise IdentityChanged(f"identity changed since the run started: {changed}")
    manifest.setdefault("resumed_utc", []).append(now)


# --- baseline gate derivation (state/trace run_end records, never trace.py's own `cleared`) --


def derive_gate(rows: list[dict], trace_dir: Path) -> dict:
    """{example: True|False|None} from each row's `session` mapped to the LAST run_end record's
    `decisions.gate.cleared` in that session's trace file. No trace file, or a trace file with
    no run_end record, both map to None -- never fabricated True."""
    cleared_by_session: dict[str, bool | None] = {}
    if trace_dir.is_dir():
        for trace_file in sorted(trace_dir.glob("*.jsonl")):
            cleared: bool | None = None
            for line in trace_file.read_text(errors="replace").splitlines():
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if rec.get("kind") == "run_end":
                    cleared = bool(((rec.get("decisions") or {}).get("gate") or {}).get("cleared"))
            cleared_by_session[trace_file.stem] = cleared
    return {row["example"]: cleared_by_session.get(row.get("session"), None) for row in rows}


# --- subcommands -----------------------------------------------------------------------------


def cmd_probe() -> int:
    """One cheap call before any dispatch: no --plugin-dir, no permission flag, fresh scratch
    cwd. Never retried, never slept on."""
    cwd = Path(tempfile.mkdtemp())
    argv = [
        "claude", "-p",
        "--no-session-persistence",
        "--output-format", "stream-json",
        "--verbose",
        "Reply with the single word OK.",
    ]
    assert "--plugin-dir" not in argv and "--permission-mode" not in argv
    proc = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=300)
    stdout = proc.stdout
    stub = is_limit_stub(stdout)
    last_result = next((e for e in reversed(events(stdout)) if e.get("type") == "result"), {})
    result_text = (last_result or {}).get("result") or ""
    HERE.mkdir(parents=True, exist_ok=True)
    probe = {
        "utc": dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z"),
        "limit_stub": stub,
        "result_head": result_text[:200],
        "cost_usd": (last_result or {}).get("total_cost_usd"),
        "model": init_event(stdout).get("model"),
    }
    (HERE / "probe.json").write_text(json.dumps(probe, indent=2) + "\n")
    if stub:
        print("PAUSED: usage/spend limit")
        return 3
    if result_text.strip():
        return 0
    return 1


def cmd_baseline() -> int:
    """Copy the 2026-09-29 baseline's figures into this repo. No `claude` call."""
    new_summary = json.loads((BASELINE_DIR / "summary.json").read_text())
    existing = BASE / "summary.json"
    if existing.is_file():
        old = json.loads(existing.read_text())
        if old != new_summary:
            print(f"baseline: {BASE} already holds a different summary.json", file=sys.stderr)
            return 2
    BASE.mkdir(parents=True, exist_ok=True)
    shutil.copy2(BASELINE_DIR / "summary.json", BASE / "summary.json")
    shutil.copy2(BASELINE_DIR / "summary.md", BASE / "summary.md")
    prompts_dir = BASE / "prompts"
    prompts_dir.mkdir(exist_ok=True)
    for row in new_summary:
        name = row["example"]
        src = BASELINE_DIR / name / "prompt.txt"
        if src.is_file():
            shutil.copy2(src, prompts_dir / f"{name}.txt")
    trace_dir = BASELINE_DIR / "state" / "trace"
    sha256s = {
        p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(trace_dir.glob("*.jsonl"))
    } if trace_dir.is_dir() else {}
    gate = {
        "source": "state/trace run_end records, trace.py rule (no Absent, no Hand-wavy)",
        "sha256": sha256s,
        "cleared": derive_gate(new_summary, trace_dir),
    }
    (BASE / "gate.json").write_text(json.dumps(gate, indent=2, sort_keys=True) + "\n")
    print(f"baseline copied -> {BASE}")
    return 0


def _preflight() -> str | None:
    """None if clear to dispatch; else the reason."""
    runner_hash = hashlib.sha256(RUNNER.read_bytes()).hexdigest()
    if runner_hash != RUNNER_SHA256:
        return f"runner sha256 changed ({runner_hash})"
    sync_check = subprocess.run(["python3", "scripts/sync-content.py", "--check"], cwd=REPO_ROOT)
    if sync_check.returncode != 0:
        return "sync-content.py --check failed"
    status = subprocess.run(
        ["git", "status", "--porcelain", "--", "shared", "first-principles", "scripts/check-summary-block.py"],
        cwd=REPO_ROOT, capture_output=True, text=True,
    ).stdout
    if status.strip():
        return f"working tree dirty:\n{status}"
    tracked = subprocess.run(
        ["git", "cat-file", "-e", "HEAD:docs/structured-summary-live-protocol.md"], cwd=REPO_ROOT
    ).returncode == 0
    if not tracked:
        return "docs/structured-summary-live-protocol.md not tracked at HEAD"
    protocol_status = subprocess.run(
        ["git", "status", "--porcelain", "--", "docs/structured-summary-live-protocol.md"],
        cwd=REPO_ROOT, capture_output=True, text=True,
    ).stdout
    if protocol_status.strip():
        return "docs/structured-summary-live-protocol.md modified"
    return None


def cmd_run(phase75_close: str) -> int:
    reason = _preflight()
    if reason is not None:
        print(f"preflight: {reason}", file=sys.stderr)
        return 2

    now = dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")
    OUT.mkdir(parents=True, exist_ok=True)
    log_path = OUT.parent / "structured-summary-live.log"

    only: list[str] | None
    if not MANIFEST.is_file():
        manifest = {
            "id": ID,
            **identity(),
            "phase75_close": phase75_close,
            "out": str(OUT),
            "started_utc": now,
            "resumed_utc": [],
            "invocations": [],
        }
        only = None
    else:
        manifest = json.loads(MANIFEST.read_text())
        check_identity(manifest, now)
        targets = relaunch_targets(OUT, manifest)
        if not targets:
            print("NOTHING TO RELAUNCH")
            return 0
        k_prev = len(manifest["invocations"])
        for name in targets:
            src = OUT / name / "run.jsonl"
            if src.is_file():
                src.rename(OUT / name / f"run.void-{k_prev}.jsonl")
        only = targets

    k = len(manifest["invocations"]) + 1
    argv = runner_argv(only)
    with log_path.open("a") as log:
        proc = subprocess.run(argv, cwd=REPO_ROOT, stdout=log, stderr=subprocess.STDOUT)
    runner_exit = proc.returncode

    shutil.copy2(OUT / "summary.json", OUT / f"summary.inv{k}.json")
    invocation_rows = [
        json.loads((OUT / f"summary.inv{i}.json").read_text())
        for i in range(1, k + 1)
        if (OUT / f"summary.inv{i}.json").is_file()
    ]
    merged = merge_rows(invocation_rows)

    runner_mod = load_runner()
    runner_mod.write_summary(OUT, merged)
    runner_mod.write_decisions(OUT, merged)

    stubs, zero_file = [], []
    for row in merged:
        if analysis_files(OUT, row["example"]):
            continue
        jsonl_path = OUT / row["example"] / "run.jsonl"
        text = jsonl_path.read_text(errors="replace") if jsonl_path.is_file() else ""
        (stubs if is_limit_stub(text) else zero_file).append(row["example"])

    manifest["invocations"].append(
        {"k": k, "utc": now, "targets": only or [], "runner_exit": runner_exit, "stubs": stubs, "zero_file": zero_file}
    )
    MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

    if stubs:
        print(f"PAUSED: usage/spend limit — {', '.join(stubs)}")
        return 3
    if zero_file:
        relaunchable = [n for n in zero_file if len(_attempt_files(OUT, n)) < MAX_ATTEMPTS]
        if relaunchable:
            print(f"RELAUNCHABLE: {', '.join(relaunchable)}")
            return 4
        print(f"FINAL: {', '.join(zero_file)} have no analysis file after {MAX_ATTEMPTS} attempts")
        return 0
    print("COMPLETE")
    return 0


def collect(out: Path, raw: Path) -> dict:
    """Copy a finished OUT into raw/; flatten each example's longest analysis-*.md (by character
    count) to raw/<name>/report.md. A missing report is recorded absent, never fabricated."""
    example_dirs = sorted(p for p in out.iterdir() if p.is_dir() and p.name != "state") if out.is_dir() else []
    if len(example_dirs) != 14:
        raise CollectError(f"{out} holds {len(example_dirs)} example dirs, expected 14")
    raw.mkdir(parents=True, exist_ok=True)
    for name in ("summary.json", "summary.md", "decisions.json", "decisions.md"):
        src = out / name
        if src.is_file():
            shutil.copy2(src, raw / name)
    for inv in sorted(out.glob("summary.inv*.json")):
        shutil.copy2(inv, raw / inv.name)
    for sub in ("state/trace", "state/audit"):
        src = out / sub
        if src.is_dir():
            dest = raw / sub
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(src, dest)
    copied, missing = [], []
    for d in example_dirs:
        name = d.name
        dest = raw / name
        dest.mkdir(parents=True, exist_ok=True)
        if (d / "prompt.txt").is_file():
            shutil.copy2(d / "prompt.txt", dest / "prompt.txt")
        if (d / "run.jsonl").is_file():
            shutil.copy2(d / "run.jsonl", dest / "run.jsonl")
        for v in sorted(d.glob("run.void-*.jsonl")):
            shutil.copy2(v, dest / v.name)
        files = analysis_files(out, name)
        if files:
            longest = max(files, key=lambda p: len(p.read_text(errors="replace")))
            shutil.copy2(longest, dest / "report.md")
            copied.append(name)
        else:
            missing.append(name)
    return {"copied": copied, "missing": missing}


def cmd_collect() -> int:
    try:
        result = collect(OUT, RAW)
    except CollectError as e:
        print(f"collect: {e}", file=sys.stderr)
        return 2
    print(f"collected {len(result['copied'])}/14; missing: {result['missing'] or 'none'}")
    return 0


# --- --self-test -- D01-D08, offline, no network, no `claude` --------------------------------


def _line(obj: dict) -> str:
    return json.dumps(obj)


def _make_analysis_dir(ex_dir: Path, text: str = "placeholder analysis") -> None:
    d = ex_dir / ".first-principles"
    d.mkdir(parents=True, exist_ok=True)
    (d / "analysis-20260101T000000Z.md").write_text(text)


def _d01() -> tuple[bool, str]:
    cases = [
        (_line({"type": "result", "is_error": True, "result": ""}), True, "is_error true"),
        (_line({"type": "result", "is_error": False, "api_error_status": 429}), True, "429"),
        (
            _line({"type": "result", "is_error": False, "result": "Let's discuss GraphQL rate limiting."}),
            False,
            "complete non-stub answer that merely discusses rate limiting",
        ),
        (
            "preamble\nYou've hit your usage limit for this period.",
            True,
            "no result event, tail usage limit, no parent_tool_use_id",
        ),
        (
            'preamble usage limit tail\n"parent_tool_use_id":"x"',
            False,
            "no result event, tail mentions usage limit but parent_tool_use_id present",
        ),
    ]
    for jsonl, expected, label in cases:
        got = is_limit_stub(jsonl)
        if got != expected:
            return False, f"{label}: expected {expected} got {got}"
    return True, ""


def _d02() -> tuple[bool, str]:
    jsonl = _line(
        {
            "type": "system",
            "subtype": "init",
            "model": "m",
            "plugins": [
                {"name": "first-principles", "path": "/P"},
                {"name": "agent-router-fp", "path": "/Q"},
            ],
        }
    )
    got = loaded_body(jsonl)
    if got != ["/P"]:
        return False, f"expected ['/P'] got {got}"
    if loaded_body("no init event here") != []:
        return False, "expected [] with no init event"
    return True, ""


def _d03() -> tuple[bool, str]:
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        for i in range(11):
            name = f"ex-complete-{i:02d}"
            (out / name).mkdir()
            _make_analysis_dir(out / name)
        for name in ("miss1", "miss2"):
            (out / name).mkdir()
            (out / name / "run.jsonl").write_text(
                _line({"type": "result", "is_error": False, "result": "partial output"})
            )
        name = "miss3"
        (out / name).mkdir()
        (out / name / "run.jsonl").write_text(_line({"type": "result", "is_error": False, "result": "c"}))
        (out / name / "run.void-1.jsonl").write_text(
            _line({"type": "result", "is_error": False, "result": "a"})
        )
        (out / name / "run.void-2.jsonl").write_text(
            _line({"type": "result", "is_error": False, "result": "b"})
        )
        targets = relaunch_targets(out, {})
        if targets != ["miss1", "miss2"]:
            return False, f"expected [miss1, miss2], got {targets}"
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        (out / "stubonly").mkdir()
        (out / "stubonly" / "run.jsonl").write_text(
            _line({"type": "result", "is_error": True, "result": ""})
        )
        targets = relaunch_targets(out, {})
        if targets != ["stubonly"]:
            return False, f"stub-only case: expected [stubonly], got {targets}"
    return True, ""


def _d04() -> tuple[bool, str]:
    inv1 = [{"example": f"ex{i}", "status": "complete" if i not in (2, 5) else "failed", "v": i} for i in range(14)]
    inv2 = [{"example": "ex2", "status": "complete", "v": 99}, {"example": "ex5", "status": "complete", "v": 98}]
    merged = merge_rows([inv1, inv2])
    if len(merged) != 14:
        return False, f"expected 14 rows got {len(merged)}"
    if sorted(r["example"] for r in merged) != sorted(r["example"] for r in inv1):
        return False, "example set changed"
    if [r["example"] for r in merged] != sorted(r["example"] for r in merged):
        return False, "rows not sorted by example"
    by_name = {r["example"]: r for r in merged}
    if by_name["ex2"]["v"] != 99 or by_name["ex5"]["v"] != 98:
        return False, "resumed rows did not override"
    for i in range(14):
        if i in (2, 5):
            continue
        if by_name[f"ex{i}"] != inv1[i]:
            return False, f"row ex{i} not byte-equal to invocation 1"
    return True, ""


def _d05() -> tuple[bool, str]:
    base_identity = {
        "fp_tree": "aaa", "shared_tree": "bbb", "checker_sha256": "ccc",
        "runner_sha256": "ddd", "head_sha": "eee", "agent_router_head": "fff",
    }
    manifest = {**base_identity, "resumed_utc": []}
    try:
        check_identity(manifest, "2026-01-01T00:00:00Z", current={**base_identity, "fp_tree": "changed"})
        return False, "expected IdentityChanged on a different fp_tree"
    except IdentityChanged:
        pass
    manifest2 = {**base_identity, "resumed_utc": []}
    check_identity(manifest2, "2026-01-01T00:00:00Z", current=base_identity)
    if manifest2["resumed_utc"] != ["2026-01-01T00:00:00Z"]:
        return False, f"expected one resumed_utc entry, got {manifest2['resumed_utc']}"
    return True, ""


def _d06() -> tuple[bool, str]:
    a1 = runner_argv(None)
    a2 = runner_argv(["x", "y"])
    for a in (a1, a2):
        forbidden = {"--model", "--permission-mode", "bypassPermissions"} & set(a)
        if forbidden:
            return False, f"forbidden flag(s) present: {forbidden} in {a}"
    if a1[a1.index("--jobs") + 1] != str(JOBS):
        return False, "jobs mismatch"
    if a1[a1.index("--entry") + 1] != ENTRY:
        return False, "entry mismatch"
    if a1[a1.index("--fp-repo") + 1] != FP_REPO:
        return False, "fp-repo mismatch"
    if "--only" in a1:
        return False, "unexpected --only in first-invocation argv"
    if a2[a2.index("--only") + 1] != "x,y":
        return False, "resume --only value mismatch"
    return True, ""


def _d07() -> tuple[bool, str]:
    with tempfile.TemporaryDirectory() as tmp:
        trace_dir = Path(tmp)
        (trace_dir / "sess-a.jsonl").write_text(
            _line({"kind": "run_end", "decisions": {"gate": {"cleared": True}}}) + "\n"
        )
        (trace_dir / "sess-b.jsonl").write_text(
            _line({"kind": "run_end", "decisions": {"gate": {"cleared": False}}}) + "\n"
        )
        rows = [
            {"example": "ex-a", "session": "sess-a"},
            {"example": "ex-b", "session": "sess-b"},
            {"example": "ex-c", "session": "sess-c"},  # no trace file at all
        ]
        cleared = derive_gate(rows, trace_dir)
        if cleared != {"ex-a": True, "ex-b": False, "ex-c": None}:
            return False, f"got {cleared}"
        (trace_dir / "sess-d.jsonl").write_text(_line({"kind": "other"}) + "\n")
        cleared2 = derive_gate([{"example": "ex-d", "session": "sess-d"}], trace_dir)
        if cleared2 != {"ex-d": None}:
            return False, f"trace file with no run_end: got {cleared2}, expected null"
    return True, ""


def _d08() -> tuple[bool, str]:
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "out"
        raw = Path(tmp) / "raw"
        out.mkdir()
        for i in range(12):
            name = f"ex{i:02d}"
            (out / name).mkdir()
            _make_analysis_dir(out / name, text="x" * (10 + i))
        multi = "ex-multi"
        d = out / multi / ".first-principles"
        d.mkdir(parents=True)
        (d / "analysis-a.md").write_text("short")
        (d / "analysis-b.md").write_text("a much longer report body here")
        none_name = "ex-none"
        (out / none_name).mkdir()
        result = collect(out, raw)
        if none_name not in result["missing"]:
            return False, "missing example not recorded as absent"
        if (raw / none_name / "report.md").exists():
            return False, "fabricated a report for a missing example"
        report = raw / multi / "report.md"
        if not report.is_file() or report.read_text() != "a much longer report body here":
            return False, "did not flatten the longest analysis file by character count"
    with tempfile.TemporaryDirectory() as tmp:
        out13 = Path(tmp) / "out13"
        out13.mkdir()
        for i in range(13):
            (out13 / f"ex{i}").mkdir()
        try:
            collect(out13, Path(tmp) / "raw13")
            return False, "expected CollectError for 13 example dirs"
        except CollectError:
            pass
    return True, ""


def self_test() -> int:
    controls = [
        ("D01", _d01), ("D02", _d02), ("D03", _d03), ("D04", _d04),
        ("D05", _d05), ("D06", _d06), ("D07", _d07), ("D08", _d08),
    ]
    results = []
    for name, fn in controls:
        try:
            ok, reason = fn()
        except Exception as e:  # noqa: BLE001 -- a control's own assertion failure is a FAIL, not a crash
            ok, reason = False, f"{type(e).__name__}: {e}"
        results.append((name, ok))
        suffix = f" {reason}" if not ok and reason else ""
        print(f"  {'PASS' if ok else 'FAIL'}  [{name}]{suffix}")
    passed = sum(ok for _, ok in results)
    verdict = "PASS" if passed == len(results) else "FAIL"
    print(f"STRUCTURED-SUMMARY-LIVE RUN SELF-TEST: {verdict} ({passed}/{len(results)} controls)")
    return 0 if passed == len(results) else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("command", nargs="?", choices=("probe", "baseline", "run", "collect"))
    ap.add_argument("--phase75-close")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if a.command == "probe":
        return cmd_probe()
    if a.command == "baseline":
        return cmd_baseline()
    if a.command == "run":
        if not a.phase75_close:
            ap.error("run needs --phase75-close")
        return cmd_run(a.phase75_close)
    if a.command == "collect":
        return cmd_collect()
    ap.error("a command or --self-test is required")


if __name__ == "__main__":
    raise SystemExit(main())
