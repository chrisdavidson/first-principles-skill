#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Quality-measurement harness — promoted blind A/B rig (HARNESS-01).

Promotes the throwaway blind judging rig that produced
`docs/v8.6-quality-ab-experiment.md` into a permanent, self-testing instrument.
The instrument runs generate -> extract -> blind -> judge -> tabulate end to
end as `claude -p` subprocesses (D-01) and encodes both documented extraction
traps (the orchestrator-summary substitution and the multi-block/multi-dispatch
concatenation) as firing assertions with negative fixtures.

**Task 1 scope: catalog parsing, the environment guard, the verbatim-dispatch
bypass wrapper, the live-generation transport, and a non-vacuous
`--self-test`.** **Task 3 scope: the extraction pipeline
(`extract_agent_analysis`, `extract_judge_verdict`), the sealed judge packet
builder, the judge prompt and scoreline parser, PASS/FAIL derivation, one-row
tabulation, and the `--single` tracer path.** The extraction channel is fixed
by the D-22 live probe — see `tests/quality-probe-v8.7/README.md` for the
probe's observed shape (and its one contradiction of the archived async-task
evidence) and `164-CONTEXT.md` D-22 for the full record.

**Plan 04 Task 1 scope: `--run`, `--rejudge`, `--dry-run`, `--resume`, and
`write_run_manifest`** — composes the pieces above into the full
generate->extract->blind->judge->score->tabulate->detect chain (`--run`), a
byte-faithful re-judge of an existing analyses directory (`--rejudge`), a
zero-side-effect invocation enumerator (`--dry-run`), and resumable
re-dispatch that never repeats a completed invocation (`--resume`), per
`classify_invocation_outcome`'s PARSING of each capture's terminal `result`
event (never a bare `grep 'api_error_status'` — see that function's
docstring for why the naive idiom is wrong and dangerous).

Usage:
    python3 scripts/check-quality-harness.py --self-test
    python3 scripts/check-quality-harness.py --probe Q-P1 \\
        --catalog tests/quality-catalog-v8.7.md --out /tmp/qh-probe
    python3 scripts/check-quality-harness.py --single \\
        tests/quality-probe-v8.7/probe-P1.jsonl
    python3 scripts/check-quality-harness.py --detect-defects \\
        tests/quality-baseline-v8.7/analyses --out /tmp/qh-detect.tsv
    python3 scripts/check-quality-harness.py --compare /tmp/qh-postfix \\
        --baseline tests/quality-baseline-v8.7-regenerated
    python3 scripts/check-quality-harness.py --dry-run --run \\
        --rejudge tests/quality-baseline-v8.7/analyses \\
        --catalog tests/quality-catalog-v8.7.md --out /tmp/qh-dry
    python3 scripts/check-quality-harness.py --run \\
        --rejudge tests/quality-baseline-v8.7/analyses \\
        --catalog tests/quality-catalog-v8.7.md --repeat 2 --out /tmp/qh-run
    python3 scripts/check-quality-harness.py --resume --run \\
        --rejudge tests/quality-baseline-v8.7/analyses \\
        --catalog tests/quality-catalog-v8.7.md --repeat 2 --out /tmp/qh-run

Options:
    --self-test         Run the offline deterministic self-test and exit (no
                         `claude` invoked).
    --catalog PATH      Path to tests/quality-catalog-v8.7.md (required for
                         --probe and --run).
    --out PATH          Output directory for `.jsonl` captures (--probe,
                         --run, --rejudge, --dry-run) or output TSV path
                         (--detect-defects).
    --repeat INT        Per-prompt repeat count (default: DEFAULT_REPEAT).
    --plugin-dir PATH   Path to the first-principles plugin dir (default:
                         repo-relative `first-principles/`).
    --probe [ID]        Dispatch exactly one live generation for the named
                         catalog row (default: Q-P1) and write the capture to
                         --out.
    --single JSONL      Run the whole extract->blind->judge->parse->tabulate
                         path for one already-captured generation .jsonl and
                         print one tabulated row. Dispatches exactly one live
                         judge invocation.
    --detect-defects DIR
                         Run the D-18 mechanical defect detector (offline, no
                         `claude` invoked) over a directory of analysis .md
                         files and write the ten-column TSV to --out.
    --compare POST_DIR   Diff POST_DIR against --baseline BASE_DIR (offline,
                         no `claude` invoked) and print the band/pass-split/
                         defect-incidence delta report plus a computed
                         GOODHART_FLAG line (D-04). Requires --baseline.
    --baseline BASE_DIR  Baseline run directory for --compare.
    --run               Run the full generate->extract->blind->judge->
                         score->tabulate->detect chain over --catalog,
                         writing scorelines.tsv, defect-incidence.tsv, a
                         blinding key, and a manifest under --out.
    --rejudge DIR       Re-judge an existing directory of analysis .md files
                         through the same judge channel, with a byte-
                         unchanged packet passthrough (T-164-19), writing
                         rejudge-scorelines.tsv under --out. Composes with
                         --run.
    --dry-run           Enumerate every invocation --run/--rejudge would
                         dispatch (kind, source id, run index, destination
                         path) and a total count; spends nothing, makes no
                         subprocess call, and creates no capture file.
    --resume            Continue into an existing --out directory, skipping
                         every invocation whose destination already holds a
                         completed record and re-dispatching only those that
                         are absent or hold a transport-error or rate-limit
                         stub (never a completed record, regardless of how
                         its content looks — T-164-18).

Exit codes:
    0  Self-test passed, or a run/probe/single/run-layer path completed
       successfully.
    1  Self-test failed, or a run failed.
    2  Usage/environment error (missing `claude` on PATH, bad arguments).
"""

from __future__ import annotations

import argparse
import contextlib
import fnmatch
import hashlib
import inspect
import io
import json
import random
import re
import shutil
import subprocess
import sys
import tempfile
import time
from collections.abc import Callable
from dataclasses import dataclass, fields, replace
from pathlib import Path

# ---------------------------------------------------------------------------
# Module-level constants
# ---------------------------------------------------------------------------

REPO_ROOT: Path = Path(__file__).resolve().parents[1]
DEFAULT_PLUGIN_DIR: Path = REPO_ROOT / "first-principles"
DEFAULT_CATALOG: Path = REPO_ROOT / "tests" / "quality-catalog-v8.7.md"
# Plan 02 real-capture guardrail fixtures (D-15 items 1-2). Built from whole
# donor lines under tests/step0-captures-v8.6/ — see
# tests/quality-fixtures-v8.7/README.md for per-fixture provenance.
FIXTURES_DIR: Path = REPO_ROOT / "tests" / "quality-fixtures-v8.7"
SCORELINE_BLOCKS_DIR: Path = FIXTURES_DIR / "scoreline-blocks"
BASELINE_DIR: Path = REPO_ROOT / "tests" / "quality-baseline-v8.7"
# Plan 04 Task 3: the regenerated pre-fix baseline this harness's own --run/
# --rejudge produced (D-02/D-07/D-08). check_baseline_integrity covers this
# directory too, with its D-02 re-judge arm checked against BASELINE_DIR's
# analyses/ (the frozen corpus it re-judged), not its own.
REGEN_DIR: Path = REPO_ROOT / "tests" / "quality-baseline-v8.7-regenerated"
# Phase 166 Plan 02 Task 3: the post-fix baseline this harness's own --run/
# --rejudge produced against the post-165 agent body (D-05). check_baseline_
# integrity covers this directory too, with its D-02 re-judge arm checked
# against REGEN_DIR's analyses/ (the frozen pre-fix analyses it re-judged
# same-day), not its own.
POSTFIX_DIR: Path = REPO_ROOT / "tests" / "quality-baseline-v8.7-postfix"
# Phase 4 (v8.24.0), CAP-02/CAP-03: the committed PR-P1 capture — the only
# fixture in the repo carrying real subagent WebFetch/Read tool calls,
# recovered from a reaping-vulnerable scratchpad and not reproducible
# without a paid live run. See tests/quality-provenance-v8.24/README.md.
PROVENANCE_FIXTURE_DIR: Path = REPO_ROOT / "tests" / "quality-provenance-v8.24"
# Phase 999.5 (WR-B): the frozen-path write guard reads its pathspec list from
# the battery script rather than restating it, so the two cannot drift. The
# review that filed WR-B named the absence of exactly this shared source as the
# reason the frozen half of the guard was left undone. Reading the shell array
# has precedent: `scripts/check-registration.py` already parses this same file
# for its `gate`/`gate_prereq` registrations (WR-02, v8.24 Phase 6).
BATTERY_PATH: Path = REPO_ROOT / "scripts" / "check-firewall-battery.sh"

# D-08 noise-floor rationale, in this harness's own words: three problems at
# two runs each buys a within-condition noise floor. The source experiment
# (docs/v8.6-quality-ab-experiment.md) ran one run per cell and its own authors
# called the exact 35/35 tie "partly luck" — without a repeat, a two-band
# post-fix movement (Phase 166) cannot be told apart from run-to-run variance.
DEFAULT_REPEAT = 2

# ---------------------------------------------------------------------------
# Catalog data types
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class QualityPrompt:
    """One row from tests/quality-catalog-v8.7.md."""

    id: str
    text: str
    notes: str


# ---------------------------------------------------------------------------
# Pipe-table cell primitives
# verbatim-move-from: scripts/_battery_core.py lines 86-103
# (reused rather than a bare `line.split("|")`, which shreds any cell holding
# alternation syntax like "(my|the|this)" — see repo memory
# step0-pipe-table-parser-gotcha.md)
# ---------------------------------------------------------------------------


def _split_row(line: str) -> list[str]:
    """Split a Markdown table row on `|`, returning trimmed cells.

    Leading/trailing `|` produce empty cells which we drop.
    """
    parts = [c.strip() for c in line.split("|")]
    if parts and parts[0] == "":
        parts = parts[1:]
    if parts and parts[-1] == "":
        parts = parts[:-1]
    return parts


def _is_separator_row(cells: list[str]) -> bool:
    """A separator row in a Markdown table is all dashes (with optional colons)."""
    if not cells:
        return False
    return all(re.fullmatch(r":?-{3,}:?", c) is not None for c in cells)


# ---------------------------------------------------------------------------
# Catalog reader
# Model: scripts/check-step0-live.py::_read_step0_catalog (lines 155-202)
# ---------------------------------------------------------------------------

# A catalog id becomes a filesystem path (<id>.jsonl and its .md sibling —
# see _extract_and_persist_analysis clause (d)), so it is validated at this
# boundary rather than at each of the places it is later used. `/` and `..`
# are rejected because they let an id write outside --out.
_CATALOG_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


def _read_quality_catalog(path: Path) -> list[QualityPrompt]:
    """Parse tests/quality-catalog-v8.7.md into a list of QualityPrompt rows.

    Catalog columns: | ID | Prompt | Notes |.

    Unlike `_read_step0_catalog` (which exits non-zero on an unrecognized MODE
    value — a live-run-time failure), this parser raises `ValueError` naming
    the offending line number for a malformed header, a missing separator row,
    or a row missing its ID or prompt text. Those are authoring bugs in the
    catalog file itself, not something to skip past silently.
    """
    text = path.read_text(encoding="utf-8")
    prompts: list[QualityPrompt] = []
    in_table = False
    expecting_separator = False
    header_seen = False
    for lineno, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped.startswith("|"):
            in_table = False
            expecting_separator = False
            continue
        cells = _split_row(stripped)
        if not cells:
            continue
        if not in_table:
            if cells == ["ID", "Prompt", "Notes"]:
                in_table = True
                expecting_separator = True
                header_seen = True
            else:
                raise ValueError(
                    f"{path}:{lineno}: expected header '| ID | Prompt | Notes |', "
                    f"got {cells!r}"
                )
            continue
        if expecting_separator:
            expecting_separator = False
            if _is_separator_row(cells):
                continue
            raise ValueError(
                f"{path}:{lineno}: expected a separator row after the header, "
                f"got {cells!r}"
            )
        if len(cells) < 2 or not cells[0].strip() or not cells[1].strip():
            raise ValueError(f"{path}:{lineno}: row missing ID or prompt text: {cells!r}")
        row_id = cells[0]
        if not _CATALOG_ID_RE.match(row_id):
            raise ValueError(
                f"{path}:{lineno}: catalog id {row_id!r} is not a safe filename "
                f"stem — ids become output paths ({row_id}.jsonl and its .md "
                f"sibling), so an id containing '/' or '..' writes outside --out"
            )
        prompt_text = cells[1]
        notes = cells[2] if len(cells) > 2 else ""
        prompts.append(QualityPrompt(id=row_id, text=prompt_text, notes=notes))
    if not header_seen:
        raise ValueError(f"{path}: no catalog header found (expected '| ID | Prompt | Notes |')")
    if not prompts:
        raise ValueError(f"{path}: no data rows parsed")
    return prompts


# ---------------------------------------------------------------------------
# Runtime guard
# verbatim-move-from: scripts/check-step0-live.py lines 267-273
# ---------------------------------------------------------------------------


def _ensure_claude_available() -> None:
    if shutil.which("claude") is None:
        print(
            "error: `claude` CLI not found on PATH; cannot run the quality harness",
            file=sys.stderr,
        )
        sys.exit(2)


# ---------------------------------------------------------------------------
# Approach ② bypass wrapper
# verbatim-move-from: scripts/check-step0-live.py lines 281-302 (FROZEN 71/D-09)
# Also matches the original v8.6 A/B experiment's own methodology
# (tests/quality-baseline-v8.7/README.md Provenance row: "claude -p
# --plugin-dir over the approach-② bypass wrapper") — this harness's live
# dispatch continues that same discipline for a deterministic Agent dispatch.
# ---------------------------------------------------------------------------


def _wrap_for_bypass(verbatim_text: str) -> str:
    """Approach ②: meta-instruction commanding verbatim Agent-tool invocation.

    Instructs the orchestrator to invoke the first-principles:first-principles
    agent against the verbatim text with no interpretation, enrichment, or
    clarification. The wrapper itself contains NO Step 0 trigger phrases
    (no "pre-mortem", "inversion", "fishbone", "five-whys", "trade-off",
    "second-order", "nervous about plan", etc.) — see Pitfall 2.

    Only the interpolated {verbatim_text} slot carries trigger phrases.
    FROZEN — copy verbatim per 71/D-09. Never add technique keywords.
    """
    return (
        "Invoke the first-principles:first-principles agent with exactly this "
        "prompt, verbatim, without any modification, enrichment, or clarification:"
        "\n\n"
        '"""\n'
        f"{verbatim_text}\n"
        '"""\n\n'
        "Do not interpret or enrich the prompt. Pass it exactly as written to the agent."
    )


# ---------------------------------------------------------------------------
# Plan-36-locked transport
# verbatim-move-from: scripts/_battery_core.py lines 173-204 (_run_prompt_to)
# Widened per this task's action: plain prompt string, out path, optional cwd,
# and an optional plugin_dir that — when None — omits --plugin-dir entirely.
# The judge invocation (Task 3) needs cwd set to a sealed packet dir and needs
# --plugin-dir omitted so the judge has no agent-dispatch surface; this task
# only builds the capability, it does not call it that way yet.
# ---------------------------------------------------------------------------


def _run_prompt_to(
    prompt_text: str,
    out_path: Path,
    plugin_dir: Path | None,
    cwd: Path | None = None,
) -> Path:
    """Issue one prompt via `claude -p` and capture the stream-json log to out_path.

    Transport (Plan-36-locked, verbatim, do not modify this argv list):
        claude -p [--plugin-dir <path>] --no-session-persistence \
          --output-format stream-json --verbose \
          --permission-mode bypassPermissions <prompt>

    When `plugin_dir` is None, `--plugin-dir` is omitted entirely — the judge
    invocation must have no agent-dispatch surface (D-05 Assumption A3).

    Returns out_path (combined stdout + stderr written there).
    """
    # Plan-36-locked — do not modify this argv list's flags/order/values
    argv = ["claude", "-p"]
    if plugin_dir is not None:
        argv += ["--plugin-dir", str(plugin_dir)]
    argv += [
        "--no-session-persistence",
        "--output-format",
        "stream-json",
        "--verbose",
        "--permission-mode",
        "bypassPermissions",
        prompt_text,
    ]
    proc = subprocess.run(
        argv,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        cwd=cwd,
    )
    out_path.write_bytes(proc.stdout or b"")
    return out_path


# ---------------------------------------------------------------------------
# Extraction pipeline (Task 3, D-22)
#
# The channel is fixed by the live probe committed in the prior commit
# (tests/quality-probe-v8.7/README.md), NOT by D-15's original wording, which
# described a different (synchronous, interactive-session) transport — the one
# the v8.6 A/B experiment's own tool_result-based extraction contract
# (tests/quality-baseline-v8.7/README.md) was correct for, but this harness's
# headless `claude -p` subprocess transport is not.
# ---------------------------------------------------------------------------


class MultipleAgentDispatchError(ValueError):
    """Raised when a capture holds != 1 Agent dispatch of the target subagent_type.

    Guardrail B (D-15 item 2, amended per D-22): the reject condition is the
    Agent-dispatch count, never a `tool_result` count — a subagent that calls
    even one internal tool (Read, a skill) legitimately produces additional,
    unrelated `tool_result` events in the same capture.
    """


class AgentAnalysisExtractionError(ValueError):
    """Raised when the verbatim analysis cannot be reliably read from a capture.

    Covers: no completed task_notification.summary found for the single
    dispatch, and the A4 cross-check divergence (primary and secondary
    channels both non-empty but disagree) — RESEARCH.md Assumption A4 names
    this untested-truncation risk; a loud failure is the correct response to a
    divergence this project has never measured.
    """


class AnalysisWriteRefused(ValueError):
    """Raised when the analysis extracted fine but its destination is unsafe to write.

    Phase 999.5 (WR-B). Deliberately NOT `AgentAnalysisExtractionError`, and
    the reason is the same one clause (c) of `_extract_and_persist_analysis`'s
    docstring already states for the None/raise split: these are different
    failures and collapsing them destroys information. An extraction error
    means the capture cannot be read; this means the capture read perfectly
    and the *destination* was refused. A caller that wants to retry into a
    different directory can act on the second and not the first.

    Two refusal conditions, both preventive rather than after-the-fact:
    (a) the destination is a symlink — the write would follow it out of the
        directory the caller chose;
    (b) the destination is inside a FROZEN-EVIDENCE pathspec — the write
        would dirty committed evidence in the worktree, which the battery
        would then report RED on its *next* run, after the damage.
    """


# The trailing transport-metadata tail observed on the tool_result channel in
# tests/quality-probe-v8.7/probe-P1.jsonl (README.md "What the matching
# tool_result actually contained") — an `agentId:` clause directly appended
# with NO separating newline (confirmed byte-for-byte against the probe:
# "...technically right.agentId: ab69e34256a1365ec (use SendMessage...")
# followed by a `\n<usage>...</usage>` block. Stripped only when tool_result
# is read as the cross-check candidate; never applied to
# task_notification.summary, which the probe showed carries no such tail.
_TRANSPORT_TAIL_RE = re.compile(
    r"agentId: [^\n]*\n<usage>.*?</usage>\s*\Z",
    re.DOTALL,
)

# Known launch-acknowledgement substring from the archived async-task evidence
# (37 committed captures under tests/step0-captures-v*/, per
# tests/quality-probe-v8.7/README.md) — this probe itself did not exhibit it
# (occurrence count 0), but the tracer_path self-test still guards against a
# future run leaking it into the extracted analysis.
_LAUNCH_ACK_PHRASE = "Async agent launched"


def _iter_jsonl_objects(jsonl_path: Path) -> list[dict]:
    """Parse a .jsonl capture into decoded objects, skipping undecodable lines.

    Never raises on a malformed line — matches the no-raise discipline of
    scripts/check-step0-live.py::_agent_was_dispatched.
    """
    raw = jsonl_path.read_text(encoding="utf-8", errors="replace")
    objs: list[dict] = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            objs.append(obj)
    return objs


def _find_agent_dispatch_ids(objs: list[dict], subagent_type: str) -> list[str]:
    """Collect every Agent tool_use id dispatching subagent_type (Guardrail B input)."""
    target = subagent_type.lower()
    dispatch_ids: list[str] = []
    for obj in objs:
        if obj.get("type") != "assistant":
            continue
        msg = obj.get("message", {})
        content = msg.get("content", []) if isinstance(msg, dict) else []
        for c in content if isinstance(content, list) else []:
            if not isinstance(c, dict) or c.get("type") != "tool_use":
                continue
            if c.get("name") != "Agent":
                continue
            inp = c.get("input", {})
            # D-01 (Phase 141) lesson, reused here: null-coalesce before
            # lowering — dict.get(key, default) returns None (not the
            # default) when the key is present with a JSON-null value.
            candidate = (
                (inp.get("subagent_type") or "").lower() if isinstance(inp, dict) else ""
            )
            if candidate == target:
                tool_use_id = c.get("id")
                if tool_use_id:
                    dispatch_ids.append(tool_use_id)
    return dispatch_ids


def _tool_result_text(content) -> str:
    """Normalize a tool_result's `content` field (str or content-block list) to text."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(b.get("text", "") for b in content if isinstance(b, dict))
    return ""


_CAPTURE_TOOL_TARGET_KEYS = {"WebFetch": "url", "Read": "file_path"}


def _iter_capture_tool_calls(
    jsonl_path: Path,
    tool_names: tuple[str, ...] = ("WebFetch", "Read"),
    dispatch_ids: frozenset[str] | None = None,
) -> list[tuple[str, str, str]]:
    """Yield (tool_name, target, retrieved_text) triples for the named tools.

    (a) Deliberately does NOT depend on _find_agent_dispatch_ids for its own
    traversal -- that function is hard-filtered to name == "Agent" plus a
    subagent_type match and returns bare ids with no path to input.url or
    input.file_path, so folding this reader's traversal into it would return
    an empty list on every capture. _capture_subagent_tool_calls (below)
    composes the two functions instead of merging their traversals, so this
    reader still never calls _find_agent_dispatch_ids itself and a defect
    here cannot reach Guardrail B's dispatch-counting logic.

    (b) It never opens the path a Read call names. retrieved_text comes
    exclusively from the capture's own tool_result block. Turning this into
    an actual filesystem read would make a capture's contents drive a file
    open, and would break replayability besides.

    (c) An empty return is the correct, non-exceptional result for a capture
    holding none of the target tools. This is a reader, not a verifier;
    reporting an unmatched label as a defect is a later verifier's job, not
    this function's.

    (d) It makes no judgement about Guardrail A or B and calls no function
    that does.

    (e) dispatch_ids=None (the default) is unfiltered: it returns every
    matching tool call in the capture, parent-session and dispatched-subagent
    alike, and the caller owns the distinction. Passing a frozenset scopes
    the result to only the tool_use blocks whose enclosing assistant event's
    parent_tool_use_id is a member of that set -- i.e. only a named
    subagent's own calls. _capture_subagent_tool_calls is the filtered,
    one-call entry point built for this; it is what Phase 5's
    check-provenance.py is documented to consume.

    (f) Measured 2026-08-31: no committed fixture holds a parent-session
    WebFetch/Read. tests/quality-provenance-v8.24/README.md lines 126-129
    describe tests/quality-fixtures-v8.7/gen-internal-tools.jsonl's tools as
    "the parent's tools"; measured, they are the subagent's, attributed to
    that file's own Agent dispatch id. The README is frozen evidence and is
    deliberately not corrected in place -- the correction is pinned instead
    by a synthesised mutation in self-test item 19 control 9, the only
    committed control with teeth on the parent/subagent attribution axis.
    """
    unmapped = [n for n in tool_names if n not in _CAPTURE_TOOL_TARGET_KEYS]
    if unmapped:
        raise ValueError(
            f"_iter_capture_tool_calls: no target key registered in "
            f"_CAPTURE_TOOL_TARGET_KEYS for {unmapped!r}; register a target "
            f"key rather than accept a blank target"
        )

    objs = _iter_jsonl_objects(jsonl_path)

    calls: list[tuple[str, str, str]] = []  # (tool_use_id, tool_name, target)
    for obj in objs:
        if obj.get("type") != "assistant":
            continue
        parent_id = obj.get("parent_tool_use_id")
        if dispatch_ids is not None and parent_id not in dispatch_ids:
            continue
        msg = obj.get("message", {})
        content = msg.get("content", []) if isinstance(msg, dict) else []
        for c in content if isinstance(content, list) else []:
            if not isinstance(c, dict) or c.get("type") != "tool_use":
                continue
            name = c.get("name")
            if name not in tool_names:
                continue
            inp = c.get("input")
            inp = inp if isinstance(inp, dict) else {}
            target = inp.get(_CAPTURE_TOOL_TARGET_KEYS[name], "")
            tool_use_id = c.get("id")
            if tool_use_id:
                calls.append((tool_use_id, name, target))

    results: dict[str, str] = {}
    for obj in objs:
        if obj.get("type") != "user":
            continue
        msg = obj.get("message", {})
        content = msg.get("content", []) if isinstance(msg, dict) else []
        for c in content if isinstance(content, list) else []:
            if not isinstance(c, dict) or c.get("type") != "tool_result":
                continue
            tool_use_id = c.get("tool_use_id")
            if not tool_use_id:
                continue
            results[tool_use_id] = _tool_result_text(c.get("content"))

    return [
        (name, target, results.get(tool_use_id, ""))
        for tool_use_id, name, target in calls
    ]


def _capture_subagent_tool_calls(
    jsonl_path: Path,
    subagent_type: str,
    tool_names: tuple[str, ...] = ("WebFetch", "Read"),
) -> list[tuple[str, str, str]]:
    """Return only the named subagent's own (tool_name, target, retrieved_text) triples.

    Composes _find_agent_dispatch_ids (read-only, never edited) with
    _iter_capture_tool_calls's dispatch_ids filter, so a caller gets
    subagent-scoped triples in one call rather than having to thread the
    dispatch-id lookup through by hand. Raises ValueError, rather than
    returning [], when subagent_type never dispatched in this capture --
    returning [] here would reintroduce the exact conflation this wrapper
    exists to close: an empty result would be indistinguishable between
    "this subagent issued no tool calls" and "there is no such subagent in
    this capture." Phase 5's check-provenance.py is the named consumer this
    wrapper is built for.
    """
    objs = _iter_jsonl_objects(jsonl_path)
    ids = _find_agent_dispatch_ids(objs, subagent_type)
    if not ids:
        raise ValueError(
            f"_capture_subagent_tool_calls: subagent_type {subagent_type!r} "
            f"never dispatched in {jsonl_path}"
        )
    return _iter_capture_tool_calls(
        jsonl_path, tool_names=tool_names, dispatch_ids=frozenset(ids)
    )


def _read_top_level_result(jsonl_path: Path) -> str:
    """Return a capture's top-level `result`/`result` field text (Guardrail A fixture helper).

    Used only by the guardrail_a self-test item to prove the extracted
    analysis is decisively longer than — and never equal to — the
    orchestrator-paraphrase channel Guardrail A must never read from. If a
    capture holds more than one terminal `result` event (an artifact seen in
    some archived donor captures), the last one is used.
    """
    value = ""
    for obj in _iter_jsonl_objects(jsonl_path):
        if obj.get("type") == "result":
            value = obj.get("result") or value
    return value


def extract_agent_analysis(jsonl_path: Path, subagent_type: str) -> str:
    """Extract the verbatim subagent analysis from a claude -p stream-json capture.

    Primary channel (probe-fixed, D-22): the `system`/`task_notification`
    event's `summary` field, matched by `tool_use_id` against the single
    Agent dispatch's `tool_use.id`. Confirmed on the committed probe to carry
    the clean, tail-free verbatim text.

    Cross-check channel: the `tool_result` block matched by the same
    `tool_use_id`, with the trailing `agentId:`/`<usage>` transport tail
    stripped. The probe showed this channel is unreliable in both
    directions — a ~200-char launch stub in 37 other committed captures, the
    full text plus a tail in the probe capture — so it is read only as an
    independent cross-check (RESEARCH.md Assumption A4), never as the primary
    source.

    Guardrail B: raises MultipleAgentDispatchError if the dispatch count for
    subagent_type is not exactly one — never concatenates, never guesses.

    Guardrail A: this function has no code path that reads the stream's
    top-level `result` field.
    """
    objs = _iter_jsonl_objects(jsonl_path)

    dispatch_ids = _find_agent_dispatch_ids(objs, subagent_type)
    if len(dispatch_ids) != 1:
        raise MultipleAgentDispatchError(
            f"expected exactly 1 {subagent_type!r} dispatch, found "
            f"{len(dispatch_ids)} in {jsonl_path}"
        )
    target_id = dispatch_ids[0]

    primary: str | None = None
    for obj in objs:
        if (
            obj.get("type") == "system"
            and obj.get("subtype") == "task_notification"
            and obj.get("tool_use_id") == target_id
            and obj.get("status") == "completed"
        ):
            primary = obj.get("summary")
            break

    if not primary:
        raise AgentAnalysisExtractionError(
            f"no completed task_notification.summary found for "
            f"tool_use_id={target_id} in {jsonl_path}"
        )

    secondary: str | None = None
    for obj in objs:
        if obj.get("type") != "user":
            continue
        msg = obj.get("message", {})
        content = msg.get("content", []) if isinstance(msg, dict) else []
        for c in content if isinstance(content, list) else []:
            if not isinstance(c, dict) or c.get("type") != "tool_result":
                continue
            if c.get("tool_use_id") != target_id:
                continue
            secondary = _TRANSPORT_TAIL_RE.sub("", _tool_result_text(c.get("content")))
            break
        if secondary is not None:
            break

    # A4 cross-check: when both channels are non-empty and disagree, raise
    # rather than silently trusting one. A launch-acknowledgement stub is NOT
    # an independent copy of the analysis to cross-check against — it is the
    # exact short-circuit Guardrail A must ignore (D-15 item 1: "a fixture
    # where the launch stub is present, proving the harness does not extract
    # it"). Real donor evidence under tests/step0-captures-v8.6/ shows this
    # stub shape is the tool_result's actual content for this dispatch id in
    # a different call site's transport (check-step0-live.py), distinct from
    # the D-22 probe's own full-text-plus-tail shape; treating the stub as a
    # disagreement source would raise on the ordinary case Guardrail A exists
    # to survive, not the anomalous one A4 exists to catch.
    if secondary and _LAUNCH_ACK_PHRASE not in secondary and secondary != primary:
        raise AgentAnalysisExtractionError(
            "primary (task_notification.summary) and cross-check "
            "(tail-stripped tool_result) channels disagree for "
            f"tool_use_id={target_id} in {jsonl_path} "
            f"(primary len={len(primary)}, cross-check len={len(secondary)})"
        )

    return primary


# ---------------------------------------------------------------------------
# Phase 999.5 (WR-B): destination guards for the analysis persistence write
# ---------------------------------------------------------------------------

# `_FROZEN_PATHS=(` ... `)` in scripts/check-firewall-battery.sh. Anchored to a
# line-start `)` so a `)` inside an entry cannot terminate the match early.
_FROZEN_PATHS_ARRAY_RE = re.compile(
    r"^_FROZEN_PATHS=\(\n(.*?)^\)$", re.MULTILINE | re.DOTALL
)
# One single-quoted entry per line, which is the array's only observed form.
_FROZEN_PATHS_ENTRY_RE = re.compile(r"^[ \t]*'([^']+)'[ \t]*$", re.MULTILINE)


def read_frozen_pathspecs(battery_text: str) -> list[str]:
    """Return the pathspecs `_FROZEN_PATHS` names in the battery script text.

    Fails CLOSED: an unparseable or empty array raises rather than returning
    an empty list. An empty list would silently disable the guard, which is
    the failure direction this whole phase exists to remove — a guard that
    reports "nothing is frozen" because it could not read the list is
    indistinguishable, at the call site, from one that read the list and
    found no match.
    """
    match = _FROZEN_PATHS_ARRAY_RE.search(battery_text)
    if match is None:
        raise AnalysisWriteRefused(
            f"cannot locate the _FROZEN_PATHS array in {BATTERY_PATH} — the "
            "frozen-path write guard cannot be evaluated, so the write is "
            "refused rather than allowed"
        )
    entries = _FROZEN_PATHS_ENTRY_RE.findall(match.group(1))
    if not entries:
        raise AnalysisWriteRefused(
            f"the _FROZEN_PATHS array in {BATTERY_PATH} parsed to zero "
            "entries — the frozen-path write guard cannot be evaluated, so "
            "the write is refused rather than allowed"
        )
    return entries


def _frozen_spec_matches(rel_posix: str, spec: str) -> bool:
    """Does one `_FROZEN_PATHS` pathspec cover this repo-relative path?

    Mirrors git's DEFAULT pathspec matching, which is what the battery's
    `git diff` / `git status` legs actually apply: a `*` is fnmatch without
    FNM_PATHNAME, so it crosses `/`, and a bare directory name covers
    everything beneath it. The second arm supplies that directory-prefix
    semantics for both the literal entries (`tests/quality-provenance-v8.24`)
    and the globbed ones (`tests/step0-captures-v*`).

    `fnmatchcase` rather than `fnmatch`: the latter applies
    `os.path.normcase`, which would make the result platform-dependent.
    """
    return fnmatch.fnmatchcase(rel_posix, spec) or fnmatch.fnmatchcase(
        rel_posix, f"{spec}/*"
    )


def is_frozen_destination(dest: Path, battery_text: str | None = None) -> bool:
    """Is `dest` inside a FROZEN-EVIDENCE pathspec?

    The parent is resolved but the leaf is not joined through `resolve()`, so
    a symlinked *parent* pointing into a frozen directory is caught here while
    a symlinked *leaf* stays visible to the separate symlink guard — the two
    conditions stay independently diagnosable rather than one masking the
    other.

    A destination outside the repository is never frozen; the battery's
    pathspecs are repo-relative and have no meaning elsewhere.
    """
    if battery_text is None:
        try:
            battery_text = BATTERY_PATH.read_text(encoding="utf-8")
        except OSError as exc:
            # Same fail-closed reasoning as `read_frozen_pathspecs`: an
            # unreadable list is not an empty list.
            raise AnalysisWriteRefused(
                f"cannot read {BATTERY_PATH} ({exc}) — the frozen-path write "
                "guard cannot be evaluated, so the write is refused rather "
                "than allowed"
            ) from exc
    resolved = dest.parent.resolve() / dest.name
    if not resolved.is_relative_to(REPO_ROOT):
        return False
    rel_posix = resolved.relative_to(REPO_ROOT).as_posix()
    return any(
        _frozen_spec_matches(rel_posix, spec)
        for spec in read_frozen_pathspecs(battery_text)
    )


def _guard_analysis_destination(dest: Path) -> None:
    """Refuse an unsafe persistence destination, or return silently.

    Order is deliberate: the symlink check runs first and does no filesystem
    resolution of its own, so a symlink is always reported as a symlink even
    when it also points into a frozen path. The reverse order would report
    the frozen condition for a link whose real defect is that it is a link.
    """
    if dest.is_symlink():
        raise AnalysisWriteRefused(
            f"refusing to write the extracted analysis through a symlink at "
            f"{dest} — the write would land wherever the link points, not in "
            f"the directory the caller named"
        )
    if is_frozen_destination(dest):
        raise AnalysisWriteRefused(
            f"refusing to write the extracted analysis to {dest} — it is "
            f"inside a FROZEN-EVIDENCE pathspec (see _FROZEN_PATHS in "
            f"{BATTERY_PATH}). Writing there dirties committed evidence in "
            f"the worktree; re-run against a copy outside tests/ instead"
        )


def _extract_and_persist_analysis(jsonl_path: Path, subagent_type: str) -> Path | None:
    """Extract the analysis from `jsonl_path` and write it beside its source.

    (a) Adds no extraction logic of its own — Guardrails A and B and the A4
    cross-check apply in full because `extract_agent_analysis` is called
    here unmodified, with no try/except around it.
    (b) The `completed` gate is checked first, via `classify_invocation_outcome`
    (defined far below this point in the file — the forward reference
    resolves at call time and is correct, but the distance is surprising
    enough to deserve this note), matching the skip condition
    `run_generation_arm` already applies before writing its own sibling
    `analyses/` copy.
    (c) `None` means "capture did not complete" (no `.md` is written); a
    raised exception means "completed but unextractable" — a
    `MultipleAgentDispatchError` or `AgentAnalysisExtractionError` from
    Guardrail A/B or the A4 cross-check. These are two different failures
    and must never be collapsed into one.
    (d) The destination is `jsonl_path.with_suffix(".md")`, so whatever
    shaped `jsonl_path` also shapes this write. On the `--probe` path that
    shape comes from a catalog id, validated at the catalog boundary by
    `_CATALOG_ID_RE` before it ever reaches a filesystem path. On the
    `--single` path it comes from a path the operator typed directly.
    (e) Phase 999.5 (WR-B): that destination is now guarded before it is
    written, raising `AnalysisWriteRefused` for a symlink or a
    FROZEN-EVIDENCE path. This is a THIRD outcome, not a variant of the two
    in clause (c): `None` means the capture did not complete, a guardrail
    error means it completed but could not be read, and this means it was
    read fine and the destination was refused. The guard is preventive —
    FROZEN-EVIDENCE catches the same damage, but only on the battery's next
    run, by which time the worktree is already dirty.

    Returns the written `.md` path, or `None` if the capture did not
    complete.
    """
    if classify_invocation_outcome(jsonl_path) != "completed":
        return None
    analysis = extract_agent_analysis(jsonl_path, subagent_type=subagent_type)
    dest = jsonl_path.with_suffix(".md")
    _guard_analysis_destination(dest)
    dest.write_text(analysis, encoding="utf-8")
    return dest


def _persist_or_refuse_analysis(
    jsonl_path: Path, subagent_type: str
) -> tuple[Path | None, str]:
    """Decide whether `--single` may proceed to a paid live judge invocation.

    (a) This is the `--single` call site's decision helper, extracted as a
    function precisely because the phase-04 verification found a correct
    helper (`_extract_and_persist_analysis`) behind an incorrect call site
    (CR-02): a decision that lives inline in `main()` cannot be self-tested
    without a live `claude`, so the decision itself is pulled out here where
    it can be exercised on a path alone.
    (b) The empty string in the success tuple `(path, "")` is not a message
    — callers must branch on the path being `None`, never on the message
    being falsy.
    (c) `MultipleAgentDispatchError` and `AgentAnalysisExtractionError`
    propagate through this wrapper untouched. A completed-but-unextractable
    capture is a different failure from a capture that did not complete,
    and collapsing the two into a single refusal would be the exact defect
    clause (c) of the wrapped helper's docstring exists to prevent.
    (d) `AnalysisWriteRefused` is the one exception this wrapper DOES
    convert into a refusal tuple, and the asymmetry with (c) is the point:
    a guardrail error is a statement about the capture's contents that the
    caller must be able to act on, whereas a refused destination is already
    a refusal — the exact thing this helper exists to express. Converting
    it loses nothing and keeps `--single tests/quality-provenance-v8.24/
    PR-P1.jsonl` (WR-B's own worked example) from ending in a traceback.
    """
    try:
        path = _extract_and_persist_analysis(jsonl_path, subagent_type=subagent_type)
    except AnalysisWriteRefused as exc:
        return (None, f"Refusing to judge {jsonl_path}: {exc}")
    if path is not None:
        return (path, "")
    outcome = classify_invocation_outcome(jsonl_path)
    message = (
        f"Refusing to judge {jsonl_path}: analysis not persisted — outcome "
        f"was {outcome!r}, not 'completed'. A judged score with no retained "
        f"analysis has no provenance."
    )
    return (None, message)


def _persist_or_diagnose_analysis(
    jsonl_path: Path, subagent_type: str
) -> tuple[Path | None, str, int]:
    """Decide what `--probe` reports after a paid live run, and with what status.

    Phase 999.5 (WR-A). The `--probe` call site had no `try`/`except` at all,
    so a capture that completed but could not be extracted ended a *paid*
    invocation in a bare traceback that never mentioned the one fact the
    operator most needs — that the `.jsonl` is intact and re-extractable
    without paying again.

    (a) This is a function rather than an inline `try` in `main()` for the
    reason `_persist_or_refuse_analysis`'s clause (a) records about CR-02: a
    decision that lives inline in `main()` cannot be self-tested without a
    live `claude`. The `--probe` block is the least testable code in this
    file precisely because everything above it costs money.
    (b) The three-outcome return mirrors the wrapped helper's three
    outcomes exactly, and the exit code is what distinguishes them where a
    message alone would not: `0` for "written" and for "the capture never
    completed" (nothing was owed), `1` for "completed but not persisted"
    (something was owed and not delivered). A diagnosis printed with a `0`
    exit is a diagnosis a script cannot see.
    (c) `AnalysisWriteRefused` is caught alongside the two guardrail errors
    rather than separately: from `--probe`'s perspective all three mean the
    same actionable thing — the capture survived, the analysis did not, and
    no second live run is required to try again.

    Returns `(path_or_None, message, exit_code)`. The message is always
    non-empty; the caller decides only which stream it goes to.
    """
    try:
        path = _extract_and_persist_analysis(jsonl_path, subagent_type=subagent_type)
    except (
        MultipleAgentDispatchError,
        AgentAnalysisExtractionError,
        AnalysisWriteRefused,
    ) as exc:
        return (
            None,
            f"Probe analysis NOT written — the capture completed but its "
            f"analysis could not be persisted: {exc}. The raw capture is "
            f"intact at {jsonl_path} and can be re-extracted without another "
            f"live run.",
            1,
        )
    if path is not None:
        return (path, f"Probe analysis written: {path}", 0)
    outcome = classify_invocation_outcome(jsonl_path)
    return (None, f"Probe analysis not written — outcome was {outcome!r}", 0)


def extract_judge_verdict(jsonl_path: Path) -> str:
    """Extract the judge's own verdict text from a claude -p judge-invocation capture.

    Deliberately the OPPOSITE of extract_agent_analysis (Common Pitfalls
    Pitfall 2, 164-RESEARCH.md) and must not be merged with it: the judge
    invocation dispatches no subagent (D-05 Assumption A3 — no --plugin-dir,
    the sealed packet dir as cwd), so the top-level model's own final output
    IS the judgment. Reading task_notification.summary here would find
    nothing (no subagent runs); reading the final assistant text / top-level
    `result` field here is correct, not a bug, because there is no subagent
    output to distinguish it from.

    Raises ValueError if the capture shows ANY Agent dispatch at all — a
    judge invocation must never delegate to a subagent.
    """
    objs = _iter_jsonl_objects(jsonl_path)

    for obj in objs:
        if obj.get("type") != "assistant":
            continue
        msg = obj.get("message", {})
        content = msg.get("content", []) if isinstance(msg, dict) else []
        for c in content if isinstance(content, list) else []:
            if isinstance(c, dict) and c.get("type") == "tool_use" and c.get("name") == "Agent":
                raise ValueError(
                    f"judge capture {jsonl_path} contains an Agent dispatch; "
                    "judging must not delegate to a subagent"
                )

    final_text: str | None = None
    for obj in objs:
        if obj.get("type") != "assistant":
            continue
        msg = obj.get("message", {})
        content = msg.get("content", []) if isinstance(msg, dict) else []
        texts = [
            c.get("text", "")
            for c in content
            if isinstance(c, dict) and c.get("type") == "text"
        ]
        if texts:
            final_text = "".join(texts)

    if final_text:
        return final_text

    # Fallback: the top-level result field — correct here, since there is no
    # subagent output for it to be a paraphrase of (Pattern 2, opposite of
    # extract_agent_analysis's Guardrail A).
    for obj in objs:
        if obj.get("type") == "result":
            value = obj.get("result")
            if value:
                return value

    raise ValueError(f"no judge verdict text found in {jsonl_path}")


def build_judge_packet(
    analysis: str | bytes, packet_root: Path | None = None
) -> Path:
    """Create a sealed judge packet dir outside the repository (D-05).

    Writes exactly two files: `analysis.md` (the passed-in, already-anonymised
    analysis) and `validation-rubric.md` (copied verbatim from
    shared/spine/references/validation-rubric.md). Verifies exactly two
    entries exist and the resolved path has no repository-root ancestor
    before returning; raises ValueError on either failure. Never writes a
    blinding key here — the key belongs to the run output directory (D-05),
    never inside or beside a packet directory.

    `analysis` accepts either `str` (the `--run` fresh-generation path,
    where the text was already decoded by `extract_agent_analysis`) or
    `bytes` (the `--rejudge` path — see `_build_rejudge_packet` below, which
    always passes bytes so the frozen corpus's trailing transport-metadata
    tail reaches the packet byte-for-byte, never re-encoded through a
    decode/encode round-trip that a str parameter would risk).

    `packet_root`, when given, overrides the parent directory the fresh
    packet dir is created under (still verified outside the repo); when
    None, the OS default temp root is used.
    """
    packet_dir = Path(tempfile.mkdtemp(prefix="qh-packet-", dir=packet_root))
    resolved = packet_dir.resolve()
    repo_root_resolved = REPO_ROOT.resolve()
    if resolved == repo_root_resolved or repo_root_resolved in resolved.parents:
        raise ValueError(f"judge packet dir {resolved} is inside the repository root")

    analysis_path = packet_dir / "analysis.md"
    if isinstance(analysis, bytes):
        analysis_path.write_bytes(analysis)
    else:
        analysis_path.write_text(analysis, encoding="utf-8")
    rubric_src = REPO_ROOT / "shared" / "spine" / "references" / "validation-rubric.md"
    shutil.copy(rubric_src, packet_dir / "validation-rubric.md")

    entries = sorted(p.name for p in packet_dir.iterdir())
    if entries != ["analysis.md", "validation-rubric.md"]:
        raise ValueError(
            f"judge packet dir {resolved} does not hold exactly the two "
            f"expected files: {entries!r}"
        )

    return packet_dir


# ---------------------------------------------------------------------------
# Judge prompt and D-05 blinding check
# ---------------------------------------------------------------------------

_SCORELINE_START = "=== QUALITY-HARNESS-SCORELINE-START ==="
_SCORELINE_END = "=== QUALITY-HARNESS-SCORELINE-END ==="

JUDGE_PROMPT = (
    "You are scoring exactly one first-principles analysis document, "
    "`analysis.md`, found in your current working directory, against the "
    "rubric in `validation-rubric.md`, also in your current working "
    "directory. Read both files in full, then apply every criterion in the "
    "rubric exactly as its own \"How to Apply This Rubric\" section "
    "instructs: complete the Assumption Audit first, then produce one "
    "verdict block per criterion using the rubric's prescribed Verdict "
    "Block Format.\n\n"
    "Score this document entirely on its own terms, as the only analysis "
    "you have ever been given to evaluate. Once your six verdict blocks are "
    "complete, close your response with exactly this fixed block and "
    "nothing else following it:\n\n"
    f"{_SCORELINE_START}\n"
    "C1: <Rigorous|Sound|Hand-wavy|Absent>\n"
    "C2: <Rigorous|Sound|Hand-wavy|Absent>\n"
    "C3: <Rigorous|Sound|Hand-wavy|Absent>\n"
    "C4: <Rigorous|Sound|Hand-wavy|Absent>\n"
    "C5: <Rigorous|Sound|Hand-wavy|Absent>\n"
    "C6: <Rigorous|Sound|Hand-wavy|Absent>\n"
    "Verdict: <PASS|FAIL>\n"
    f"{_SCORELINE_END}\n\n"
    "Replace each placeholder with exactly one value drawn from its listed "
    "vocabulary. Do not add, omit, reorder, or rename any line inside the "
    "block."
)

# D-05 / T-164-03: forbidden substrings that would leak that a comparison,
# prior result, or another arm/condition exists. Checked against JUDGE_PROMPT
# at import time via _check_judge_prompt_unblinded(), which the self-test
# also calls.
_FORBIDDEN_JUDGE_PROMPT_SUBSTRINGS = (
    "compare",
    "comparison",
    "condition a",
    "condition b",
    "arm a",
    "arm b",
    "baseline",
    "regression",
    "improvement",
    "prior analysis",
    "previous analysis",
    "other analysis",
    "second analysis",
    "another analysis",
    "pre-fix",
    "post-fix",
    "before the fix",
    "after the fix",
    "v8.6",
    "v8.7",
    "experiment",
    "a/b test",
    "versus",
    " vs ",
)


def _check_judge_prompt_unblinded(prompt: str = JUDGE_PROMPT) -> bool:
    """Return True if prompt contains none of the comparison-leaking substrings."""
    lowered = prompt.lower()
    return not any(s in lowered for s in _FORBIDDEN_JUDGE_PROMPT_SUBSTRINGS)


if not _check_judge_prompt_unblinded():
    raise RuntimeError(
        "JUDGE_PROMPT contains a forbidden comparison-leaking substring; "
        "fix the prompt text (T-164-03) before this module can be imported"
    )


# ---------------------------------------------------------------------------
# Scoreline parser (D-12/D-13) and PASS/FAIL derivation (D-14)
# ---------------------------------------------------------------------------

UNPARSEABLE = "UNPARSEABLE"

_BAND_VOCAB = ("Rigorous", "Sound", "Hand-wavy", "Absent")
_CRITERIA = ("C1", "C2", "C3", "C4", "C5", "C6")

_SCORELINE_BLOCK_RE = re.compile(
    re.escape(_SCORELINE_START) + r"\n(?P<body>.*?)\n" + re.escape(_SCORELINE_END),
    re.DOTALL,
)


def parse_scoreline(text: str) -> tuple[list[str], str] | str:
    """Strict D-12 terminal-block parse. Returns (bands, verdict) or UNPARSEABLE.

    Finds the LAST occurrence of the delimited terminal block — the judge's
    free-text rationale is never scanned for band names (the
    `_composer_structure_hits` incidental-match failure mode this repo has
    already been bitten by, RR-77-08). A well-formed block holds exactly six
    `C1:`..`C6:` lines in order, each an exact band-vocabulary match, then one
    `Verdict:` line reading exactly `PASS` or `FAIL`, and nothing else inside
    the block. Anything else returns UNPARSEABLE (D-13) — never raises, never
    partially scores, never retries.
    """
    matches = list(_SCORELINE_BLOCK_RE.finditer(text))
    if not matches:
        return UNPARSEABLE

    body = matches[-1].group("body")
    lines = [ln for ln in body.split("\n") if ln.strip() != ""]
    if len(lines) != len(_CRITERIA) + 1:
        return UNPARSEABLE

    bands: list[str] = []
    for idx, crit in enumerate(_CRITERIA):
        line = lines[idx]
        prefix = f"{crit}: "
        if not line.startswith(prefix):
            return UNPARSEABLE
        band = line[len(prefix) :].strip()
        if band not in _BAND_VOCAB:
            return UNPARSEABLE
        bands.append(band)

    verdict_line = lines[len(_CRITERIA)]
    verdict_prefix = "Verdict: "
    if not verdict_line.startswith(verdict_prefix):
        return UNPARSEABLE
    verdict = verdict_line[len(verdict_prefix) :].strip()
    if verdict not in ("PASS", "FAIL"):
        return UNPARSEABLE

    return bands, verdict


def derive_pass_fail(bands: list[str]) -> str:
    """Independently re-encode validation-rubric.md's own pass semantics (D-14).

    Duplicated in code from shared/spine/references/validation-rubric.md's
    "Gate" and "Hand-wavy cap" rules: a fail if any band is Absent (the gate),
    a fail if two or more bands are Hand-wavy (the cap), a pass otherwise.
    This duplication must be kept in sync with validation-rubric.md by hand —
    there is no single source of truth enforced in code (D-14 consequence).
    """
    if "Absent" in bands:
        return "FAIL"
    if bands.count("Hand-wavy") >= 2:
        return "FAIL"
    return "PASS"


def read_scorelines(path: Path | str) -> list[dict]:
    """Tolerant scoreline TSV reader (D-14 cross-check input).

    Accepts both the legacy 8-column shape used by
    tests/quality-baseline-v8.7/scorelines.tsv (`judge_id  C1  C2  C3  C4  C5
    C6  Verdict`) and the wider shape `tabulate_rows` emits (`packet_id  C1
    .. C6  judge_verdict  derived_verdict  agreement`, 10 columns as
    currently implemented). Column 8 (index 7) is the judge-stated verdict
    in both shapes — any columns beyond it (derived_verdict, agreement) are
    ignored, so this reader tolerates either width without needing to know
    which one it was given.

    Returns one dict per data row: {"id", "bands" (list[str], length 6),
    "judge_verdict"}. Raises ValueError naming the offending line for a row
    with fewer than 8 tab-separated columns — a truncated or malformed
    scoreline file is a loud failure, not a silently-shorter comparison.

    Skips `tabulate_rows`'s own header line (`packet_id\tC1\t...`) when it is
    the first line — a real packet ID is a shuffled identifier (`P01`, `X7`,
    ...) and is never literally the string `"packet_id"`, so this detection
    cannot mistake a genuine data row for a header (Plan 04 Task 3: the
    regenerated baseline's `scorelines.tsv`/`rejudge-scorelines.tsv` are the
    first committed files this reader parses that actually carry the header
    `tabulate_rows` writes; the legacy frozen baseline's file has none).
    """
    path = Path(path)
    rows: list[dict] = []
    text = path.read_text(encoding="utf-8")
    for lineno, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        cells = line.split("\t")
        if lineno == 1 and cells[0] == "packet_id" and len(cells) > 1 and cells[1] == "C1":
            continue
        if len(cells) < 1 + len(_CRITERIA) + 1:
            raise ValueError(
                f"{path}:{lineno}: expected at least {1 + len(_CRITERIA) + 1} "
                f"tab-separated columns, got {len(cells)}: {cells!r}"
            )
        rows.append(
            {
                "id": cells[0],
                "bands": cells[1 : 1 + len(_CRITERIA)],
                "judge_verdict": cells[1 + len(_CRITERIA)],
            }
        )
    return rows


_BAND_WEIGHTS = {"Rigorous": 3, "Sound": 2, "Hand-wavy": 1, "Absent": 0}


def compute_tabulation_summary(rows: list[dict]) -> dict:
    """D-15 item 5: aggregate tabulation arithmetic over `read_scorelines`-shaped rows.

    Each row must carry "bands" (list[str], one of `_BAND_VOCAB` or
    `UNPARSEABLE`) and "judge_verdict" ("PASS"/"FAIL"/`UNPARSEABLE`).

    Returns a dict:
      - per_row_totals: list[int | None], one per row — the sum of that
        row's 6 band weights, or None if any cell in the row is
        `UNPARSEABLE` (a row with an unparseable cell contributes no numeric
        total, but see `denominator` below — it is never dropped silently).
      - per_criterion_sums: list[int], one per C1-C6, summed only over rows
        with no unparseable cell.
      - unparseable_cell_count: int, total UNPARSEABLE band cells across all
        rows.
      - aggregate_band_total: int, sum of the non-None per_row_totals —
        equal to sum(per_criterion_sums) by construction.
      - pass_count / fail_count / unparseable_verdict_count: int tallies of
        each row's judge_verdict.
      - denominator: int, always `len(rows)` — T-164-12: an UNPARSEABLE cell
        must never be silently excluded from the row-count denominator, even
        though it is excluded from the numeric sums above.
      - mean: float, aggregate_band_total divided by the count of rows that
        contributed a numeric total (0.0 if none did).
    """
    per_row_totals: list[int | None] = []
    per_criterion_sums = [0] * len(_CRITERIA)
    unparseable_cell_count = 0
    pass_count = 0
    fail_count = 0
    unparseable_verdict_count = 0

    for row in rows:
        bands = row["bands"]
        if any(b == UNPARSEABLE for b in bands):
            per_row_totals.append(None)
            unparseable_cell_count += sum(1 for b in bands if b == UNPARSEABLE)
        else:
            per_row_totals.append(sum(_BAND_WEIGHTS[b] for b in bands))
            for idx, b in enumerate(bands):
                per_criterion_sums[idx] += _BAND_WEIGHTS[b]

        verdict = row["judge_verdict"]
        if verdict == "PASS":
            pass_count += 1
        elif verdict == "FAIL":
            fail_count += 1
        else:
            unparseable_verdict_count += 1

    numeric_totals = [t for t in per_row_totals if t is not None]
    aggregate_band_total = sum(numeric_totals)
    mean = aggregate_band_total / len(numeric_totals) if numeric_totals else 0.0

    return {
        "per_row_totals": per_row_totals,
        "per_criterion_sums": per_criterion_sums,
        "unparseable_cell_count": unparseable_cell_count,
        "aggregate_band_total": aggregate_band_total,
        "pass_count": pass_count,
        "fail_count": fail_count,
        "unparseable_verdict_count": unparseable_verdict_count,
        "denominator": len(rows),
        "mean": mean,
    }


def tabulate_rows(rows: list[dict]) -> str:
    """Emit tab-separated rows: packet_id, C1..C6, judge_verdict, derived_verdict, agreement.

    `agreement` is one of AGREE, DISAGREE, or UNPARSEABLE (D-14) — a
    disagreement between the judge's own stated verdict and the
    independently-derived one is reported, never resolved toward either side.
    """
    header = "\t".join(["packet_id", *_CRITERIA, "judge_verdict", "derived_verdict", "agreement"])
    lines = [header]
    for row in rows:
        lines.append(
            "\t".join(
                [
                    row["packet_id"],
                    *row["bands"],
                    row["judge_verdict"],
                    row["derived_verdict"],
                    row["agreement"],
                ]
            )
        )
    return "\n".join(lines)


def _build_scoreline_row(packet_id: str, judge_text: str) -> dict:
    """Parse a judge's raw response text into one tabulate_rows()-ready row."""
    parsed = parse_scoreline(judge_text)
    if parsed == UNPARSEABLE:
        return {
            "packet_id": packet_id,
            "bands": [UNPARSEABLE] * len(_CRITERIA),
            "judge_verdict": UNPARSEABLE,
            "derived_verdict": UNPARSEABLE,
            "agreement": UNPARSEABLE,
        }
    bands, judge_verdict = parsed
    derived = derive_pass_fail(bands)
    agreement = "AGREE" if derived == judge_verdict else "DISAGREE"
    return {
        "packet_id": packet_id,
        "bands": bands,
        "judge_verdict": judge_verdict,
        "derived_verdict": derived,
        "agreement": agreement,
    }


# Offline fixture for the tracer_path self-test sub-check — a well-formed
# judge response with a rationale preamble and the terminal block. One
# Hand-wavy (C5), no Absent -> derive_pass_fail == PASS, matching the fixture's
# own stated Verdict, so the tracer path exercises the AGREE branch.
_FIXTURE_SCORELINE_TEXT = (
    "**Criterion 1: Identify Essence**\n"
    "Quoted span: \"[offline fixture — rationale text omitted for brevity]\"\n"
    "Band: **Rigorous**\n"
    "Justification: Fixture stands in for a full judge rationale; only the "
    "terminal block below is parsed.\n\n"
    f"{_SCORELINE_START}\n"
    "C1: Rigorous\n"
    "C2: Sound\n"
    "C3: Rigorous\n"
    "C4: Sound\n"
    "C5: Hand-wavy\n"
    "C6: Rigorous\n"
    "Verdict: PASS\n"
    f"{_SCORELINE_END}\n"
)


# ---------------------------------------------------------------------------
# Offline --self-test
# Self-test discipline (D-16): accumulate-and-exit-nonzero, never a bare
# `assert` anywhere in this path — a bare assert is compiled away under
# `python3 -O`, which would make this gate silently vacuous under the
# optimized interpreter (repo memory bare-assert-selftest-vacuous-under-O.md).
# ---------------------------------------------------------------------------

_MALFORMED_CATALOG_FIXTURE = "\n".join(
    [
        "# Bad Catalog",
        "",
        "| ID | Prompt | Expected MODE | Notes |",
        "|---|---|---|---|",
        "| Q-P1 | some prompt | full-composer | note |",
        "",
    ]
)

_TRAVERSAL_ID_CATALOG_FIXTURE = "\n".join(
    [
        "# Traversal-Id Catalog",
        "",
        "| ID | Prompt | Notes |",
        "|---|---|---|",
        "| ../../scripts/check-agent | some prompt | note |",
        "",
    ]
)


def _self_test_catalog_parse_positive() -> bool:
    """Positive: the real catalog parses to exactly the three expected IDs."""
    try:
        rows = _read_quality_catalog(DEFAULT_CATALOG)
    except Exception as exc:  # noqa: BLE001 — self-test must report, not crash
        print(
            f"self-test FAIL: catalog_parse_positive raised unexpectedly: {exc!r}",
            file=sys.stderr,
        )
        return False
    ids = [row.id for row in rows]
    expected = ["Q-P1", "Q-P2", "Q-P3"]
    if ids != expected:
        print(
            f"self-test FAIL: catalog_parse_positive expected {expected!r}, got {ids!r}",
            file=sys.stderr,
        )
        return False
    return True


def _self_test_catalog_parse_negative() -> bool:
    """Negative: a catalog with a bad header, or with an unsafe id, must raise."""
    ok = True

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(_MALFORMED_CATALOG_FIXTURE)
        tmp_path = Path(tmp.name)
    try:
        try:
            _read_quality_catalog(tmp_path)
            print(
                "self-test FAIL: catalog_parse_negative did not raise on a "
                "malformed header",
                file=sys.stderr,
            )
            ok = False
        except ValueError:
            pass
        except Exception as exc:  # noqa: BLE001
            print(
                f"self-test FAIL: catalog_parse_negative raised the wrong "
                f"exception type: {exc!r}",
                file=sys.stderr,
            )
            ok = False
    finally:
        try:
            tmp_path.unlink()
        except OSError:
            pass

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(_TRAVERSAL_ID_CATALOG_FIXTURE)
        traversal_path = Path(tmp.name)
    try:
        try:
            _read_quality_catalog(traversal_path)
            print(
                "self-test FAIL: catalog_parse_negative did not raise on a "
                "traversal catalog id",
                file=sys.stderr,
            )
            ok = False
        except ValueError as exc:
            msg = str(exc)
            if "../../scripts/check-agent" not in msg:
                print(
                    f"self-test FAIL: catalog_parse_negative traversal-id "
                    f"error does not name the offending id: {msg!r}",
                    file=sys.stderr,
                )
                ok = False
            if f"{traversal_path}:5" not in msg:
                print(
                    f"self-test FAIL: catalog_parse_negative traversal-id "
                    f"error does not name the source line number: {msg!r}",
                    file=sys.stderr,
                )
                ok = False
        except Exception as exc:  # noqa: BLE001
            print(
                f"self-test FAIL: catalog_parse_negative traversal-id "
                f"raised the wrong exception type: {exc!r}",
                file=sys.stderr,
            )
            ok = False
    finally:
        try:
            traversal_path.unlink()
        except OSError:
            pass

    return ok


def _selftest_guardrail_a() -> bool:
    """D-15 item 1 (Guardrail A): real-capture positive + negative fixtures.

    Positive (`gen-single-dispatch.jsonl`, donor
    tests/step0-captures-v8.6/S-P04-run4.jsonl, retaining that donor's
    launch-acknowledgement `tool_result` line verbatim): extraction succeeds,
    the returned text is long, does not itself contain the launch-
    acknowledgement stub phrase, and is decisively longer than (never equal
    to) the stream's top-level `result` field — the orchestrator-paraphrase
    channel Guardrail A must never read from.

    Negative (`gen-stub-only.jsonl`, the same donor lines minus the completed
    `task_notification` line): with no completed notification for the
    dispatch, the only payload reachable is the launch-acknowledgement stub
    itself — extraction must raise, never silently fall back to returning
    the stub text as if it were the analysis.
    """
    ok = True
    single_path = FIXTURES_DIR / "gen-single-dispatch.jsonl"
    stub_path = FIXTURES_DIR / "gen-stub-only.jsonl"

    try:
        analysis = extract_agent_analysis(
            single_path, subagent_type="first-principles:first-principles"
        )
    except Exception as exc:  # noqa: BLE001 — self-test must report, not crash
        print(
            f"self-test FAIL: guardrail_a positive extraction raised "
            f"unexpectedly: {exc!r}",
            file=sys.stderr,
        )
        return False

    if len(analysis) <= 2000:
        print(
            f"self-test FAIL: guardrail_a positive analysis is too short "
            f"({len(analysis)} chars, expected > 2000)",
            file=sys.stderr,
        )
        ok = False
    if _LAUNCH_ACK_PHRASE in analysis:
        print(
            "self-test FAIL: guardrail_a positive analysis contains the "
            f"launch-acknowledgement phrase {_LAUNCH_ACK_PHRASE!r}",
            file=sys.stderr,
        )
        ok = False

    result_field = _read_top_level_result(single_path)
    if analysis == result_field or len(analysis) <= 2 * len(result_field):
        print(
            "self-test FAIL: guardrail_a positive analysis is not "
            "decisively longer than the stream's top-level result field "
            f"(analysis len={len(analysis)}, result field len={len(result_field)})",
            file=sys.stderr,
        )
        ok = False

    try:
        extract_agent_analysis(stub_path, subagent_type="first-principles:first-principles")
        print(
            "self-test FAIL: guardrail_a negative (gen-stub-only.jsonl) did "
            "not raise — a capture with no completed task_notification "
            "must never return the launch-acknowledgement stub as the "
            "analysis",
            file=sys.stderr,
        )
        ok = False
    except AgentAnalysisExtractionError:
        pass
    except Exception as exc:  # noqa: BLE001
        print(
            f"self-test FAIL: guardrail_a negative raised the wrong "
            f"exception type: {exc!r}",
            file=sys.stderr,
        )
        ok = False

    return ok


def _selftest_guardrail_b() -> bool:
    """D-15 item 2 (Guardrail B): dispatch-count rejection, tool_result-count boundary.

    Negative (`gen-multi-dispatch.jsonl` — the donor lines of
    tests/step0-captures-v8.6/S-P04-run4.jsonl followed by the donor lines
    of tests/step0-captures-v8.6/S-P04-run5.jsonl, two distinct Agent
    tool_use ids): extraction must raise naming the dispatch count found,
    never concatenate or guess which dispatch is the real one.

    Boundary (`gen-internal-tools.jsonl`, donor
    tests/step0-captures-v8.6/S-P03-run1.jsonl): one dispatch plus several
    unrelated `tool_result` events produced by the subagent's own internal
    tool calls (a Skill dispatch, a file Read, two Bash calls) — these must
    NOT cause rejection. Rejecting on `tool_result` count rather than
    Agent-dispatch count is exactly the false-rejection failure this item
    exists to catch.
    """
    ok = True
    multi_path = FIXTURES_DIR / "gen-multi-dispatch.jsonl"
    internal_path = FIXTURES_DIR / "gen-internal-tools.jsonl"

    try:
        extract_agent_analysis(multi_path, subagent_type="first-principles:first-principles")
        print(
            "self-test FAIL: guardrail_b negative (gen-multi-dispatch.jsonl) "
            "did not raise on two distinct Agent dispatches",
            file=sys.stderr,
        )
        ok = False
    except MultipleAgentDispatchError as exc:
        if "2" not in str(exc):
            print(
                f"self-test FAIL: guardrail_b negative raised but did not "
                f"name the dispatch count found: {exc!r}",
                file=sys.stderr,
            )
            ok = False
    except Exception as exc:  # noqa: BLE001
        print(
            f"self-test FAIL: guardrail_b negative raised the wrong "
            f"exception type: {exc!r}",
            file=sys.stderr,
        )
        ok = False

    try:
        boundary_analysis = extract_agent_analysis(
            internal_path, subagent_type="first-principles:first-principles"
        )
    except Exception as exc:  # noqa: BLE001
        print(
            "self-test FAIL: guardrail_b boundary (gen-internal-tools.jsonl) "
            "raised unexpectedly — unrelated tool_result events from the "
            f"subagent's own internal tool calls must not cause rejection: {exc!r}",
            file=sys.stderr,
        )
        return False
    if len(boundary_analysis) <= 2000:
        print(
            f"self-test FAIL: guardrail_b boundary analysis is too short "
            f"({len(boundary_analysis)} chars, expected > 2000)",
            file=sys.stderr,
        )
        ok = False

    return ok


def _selftest_capture_tool_reader() -> bool:
    """Item 19 (v8.24.0 Phase 4, CAP-03): _iter_capture_tool_calls proves the
    committed PR-P1 fixture's event inventory in code, not only in prose.

    Thirteen independently-failable controls:

    1. POSITIVE reader output — _iter_capture_tool_calls on the committed
       fixture returns exactly 9 triples: 7 WebFetch, 2 Read. Every target
       and retrieved_text is non-empty. The 7 WebFetch targets all start
       with "https://". The 2 Read targets end with the two named
       reference filenames.
    2. POSITIVE asserted event inventory — counting tool_use blocks by name
       and tool_result blocks directly over _iter_jsonl_objects of the
       committed fixture yields Agent 1, ToolSearch 1, WebFetch 7, Read 2,
       tool_result 11.
    3. ANTI-MASKING — no Agent and no ToolSearch triple appears in the
       reader's output, even though control 2 proves both blocks exist in
       the same file. A reader that returned every tool_use would fail
       this and pass control 2.
    4. ANTI-VACUITY (the 7 is measured, not constant) — a mutated copy of
       the fixture with every "WebFetch" tool-use name replaced by a name
       not in the default tuple must return exactly 2 triples, both Read.
       A hardcoded 7, or a loop that never actually matched, cannot
       survive this.
    5. ANTI-VACUITY (the id-join is real) — a mutated copy with every
       tool_result block removed must still return 9 triples with
       non-empty targets, but every retrieved_text must be empty —
       proving the non-empty-text assertion in control 1 is load-bearing
       rather than trivially satisfied.
    6. NEGATIVE graceful degradation — _iter_capture_tool_calls on
       tests/quality-probe-v8.7/probe-P1.jsonl (zero external tool calls)
       returns [] and does not raise.
    7. GUARDRAIL NON-INTERFERENCE — on the same committed fixture, with
       the extraction code unchanged: _find_agent_dispatch_ids returns
       exactly 1 id; extract_agent_analysis does not raise and returns
       34,943 chars, more than twice the length of (and not equal to)
       _read_top_level_result on the same file (2,636 chars). Re-proves
       Guardrails A and B on the new fixture without touching their own
       self-test items.
    8. POSITIVE, anti-masking for the dispatch_ids filter — pins the
       literal PR-P1 dispatch id and proves filtering by it does not
       simply reject everything: the filtered result equals the
       unfiltered 9 triples.
    9. DISCRIMINATION — the only control in the suite with teeth on the
       parent/subagent attribution axis. On a tempdir copy of PR-P1 with
       every assistant envelope carrying a "Read" tool_use rewritten to
       parent_tool_use_id=None (a synthesised parent-session Read — no
       committed fixture holds one; measured 2026-08-31, every non-Agent
       tool call in every committed capture carries its own file's Agent
       dispatch id as parent_tool_use_id), filtering by PR-P1's dispatch
       id must drop both rewritten Read triples and keep exactly the 7
       WebFetch triples. An implementation that ignores
       parent_tool_use_id returns 9 in both the unfiltered and the
       filtered case and fails here.
    10. CROSS-CAPTURE — filtering tests/quality-fixtures-v8.7/
        gen-internal-tools.jsonl by PR-P1's dispatch id returns []. This
        leg alone is satisfiable by any filter whatsoever (a filter that
        rejects everything also passes it); control 9, not this one, is
        what makes the attribution axis failable.
    11. ANTI-OVER-REJECTION — filtering gen-internal-tools.jsonl by its
        OWN dispatch id (not PR-P1's) returns exactly one Read triple
        ending svg-precision/references/spec.md, 6,309 chars. This is the
        review-corrected value: tests/quality-provenance-v8.24/README.md
        lines 126-129 describe this fixture's tools as "the parent's
        tools"; measured, the Read is the SUBAGENT's own, attributed to
        this file's own Agent dispatch id
        (toolu_01TQ6wqRTxaExMFGutr8Rj5Y). The README is frozen evidence
        and is not edited; this control is where the correction is
        pinned by a test rather than merely restated in prose. A `== []`
        result here means the filter over-rejects a subagent's own call.
    12. WR-04 — tool_names=("Agent",) and tool_names=("WebFetch", "Bash")
        both raise ValueError naming the offending value and
        _CAPTURE_TOOL_TARGET_KEYS; one bad name in an otherwise-valid
        tuple is enough to raise.
    13. WRAPPER — _capture_subagent_tool_calls(PR-P1, subagent_type)
        equals control 8's filtered result; called with a subagent_type
        that never dispatched, it raises ValueError naming the
        subagent_type rather than returning [].

    Both mutated copies (controls 4 and 5) and control 9's mutated copy are
    written only into a tempfile.TemporaryDirectory() — never into tests/,
    which is now inside the FROZEN-EVIDENCE pathspec.
    """
    ok = True
    fixture_path = PROVENANCE_FIXTURE_DIR / "PR-P1.jsonl"
    probe_path = REPO_ROOT / "tests" / "quality-probe-v8.7" / "probe-P1.jsonl"

    # Control 1: positive reader output.
    triples = _iter_capture_tool_calls(fixture_path)
    webfetch_triples = [t for t in triples if t[0] == "WebFetch"]
    read_triples = [t for t in triples if t[0] == "Read"]
    if len(webfetch_triples) != 7 or len(read_triples) != 2:
        print(
            f"self-test FAIL: capture_tool_reader control 1 (positive) — "
            f"expected 7 WebFetch + 2 Read, got {len(webfetch_triples)} "
            f"WebFetch + {len(read_triples)} Read",
            file=sys.stderr,
        )
        ok = False
    if not all(target and text for _, target, text in triples):
        print(
            "self-test FAIL: capture_tool_reader control 1 (positive) — "
            "an empty target or retrieved_text was found among the "
            "reader's triples",
            file=sys.stderr,
        )
        ok = False
    if not all(target.startswith("https://") for _, target, _ in webfetch_triples):
        print(
            "self-test FAIL: capture_tool_reader control 1 (positive) — "
            "not every WebFetch target starts with https://",
            file=sys.stderr,
        )
        ok = False
    read_targets = {target for _, target, _ in read_triples}
    if not any(t.endswith("agents/references/validation-rubric.md") for t in read_targets) or not any(
        t.endswith("agents/references/output-template.md") for t in read_targets
    ):
        print(
            f"self-test FAIL: capture_tool_reader control 1 (positive) — "
            f"Read targets do not match the expected pair: {sorted(read_targets)!r}",
            file=sys.stderr,
        )
        ok = False

    # Control 2: asserted event inventory, counted directly over
    # _iter_jsonl_objects (not via the reader under test).
    objs = _iter_jsonl_objects(fixture_path)
    tool_use_counts: dict[str, int] = {}
    tool_result_count = 0
    for obj in objs:
        if obj.get("type") == "assistant":
            msg = obj.get("message", {})
            content = msg.get("content", []) if isinstance(msg, dict) else []
            for c in content if isinstance(content, list) else []:
                if isinstance(c, dict) and c.get("type") == "tool_use":
                    name = c.get("name")
                    tool_use_counts[name] = tool_use_counts.get(name, 0) + 1
        elif obj.get("type") == "user":
            msg = obj.get("message", {})
            content = msg.get("content", []) if isinstance(msg, dict) else []
            for c in content if isinstance(content, list) else []:
                if isinstance(c, dict) and c.get("type") == "tool_result":
                    tool_result_count += 1
    expected_inventory = {"Agent": 1, "ToolSearch": 1, "WebFetch": 7, "Read": 2}
    if tool_use_counts != expected_inventory or tool_result_count != 11:
        print(
            f"self-test FAIL: capture_tool_reader control 2 (event "
            f"inventory) — expected {expected_inventory} tool_use and 11 "
            f"tool_result, got {tool_use_counts} tool_use and "
            f"{tool_result_count} tool_result",
            file=sys.stderr,
        )
        ok = False

    # Control 3: anti-masking — the filter is real, not decorative.
    if any(name in ("Agent", "ToolSearch") for name, _, _ in triples):
        print(
            "self-test FAIL: capture_tool_reader control 3 (anti-masking) "
            "— an Agent or ToolSearch triple leaked into the reader's "
            "output",
            file=sys.stderr,
        )
        ok = False

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        # Control 4: anti-vacuity — rename every WebFetch tool-use so the
        # default tuple no longer matches it.
        renamed_objs = []
        for obj in objs:
            obj_copy = json.loads(json.dumps(obj))
            if obj_copy.get("type") == "assistant":
                msg = obj_copy.get("message")
                content = msg.get("content") if isinstance(msg, dict) else None
                if isinstance(content, list):
                    for c in content:
                        if isinstance(c, dict) and c.get("type") == "tool_use" and c.get(
                            "name"
                        ) == "WebFetch":
                            c["name"] = "NotAWebFetchTool"
            renamed_objs.append(obj_copy)
        renamed_path = tmp_path / "renamed.jsonl"
        renamed_path.write_text(
            "\n".join(json.dumps(o) for o in renamed_objs), encoding="utf-8"
        )
        renamed_triples = _iter_capture_tool_calls(renamed_path)
        if len(renamed_triples) != 2 or any(name != "Read" for name, _, _ in renamed_triples):
            print(
                f"self-test FAIL: capture_tool_reader control 4 "
                f"(anti-vacuity, rename) — expected exactly 2 Read "
                f"triples after renaming every WebFetch, got "
                f"{renamed_triples!r}",
                file=sys.stderr,
            )
            ok = False

        # Control 5: anti-vacuity — strip every tool_result block so the
        # id-join has nothing to match.
        stripped_objs = []
        for obj in objs:
            obj_copy = json.loads(json.dumps(obj))
            if obj_copy.get("type") == "user":
                msg = obj_copy.get("message")
                content = msg.get("content") if isinstance(msg, dict) else None
                if isinstance(content, list):
                    msg["content"] = [
                        c
                        for c in content
                        if not (isinstance(c, dict) and c.get("type") == "tool_result")
                    ]
            stripped_objs.append(obj_copy)
        stripped_path = tmp_path / "stripped.jsonl"
        stripped_path.write_text(
            "\n".join(json.dumps(o) for o in stripped_objs), encoding="utf-8"
        )
        stripped_triples = _iter_capture_tool_calls(stripped_path)
        if len(stripped_triples) != 9 or not all(target for _, target, _ in stripped_triples):
            print(
                f"self-test FAIL: capture_tool_reader control 5 "
                f"(anti-vacuity, id-join) — expected 9 triples with "
                f"non-empty targets after stripping tool_result blocks, "
                f"got {stripped_triples!r}",
                file=sys.stderr,
            )
            ok = False
        elif any(text for _, _, text in stripped_triples):
            print(
                "self-test FAIL: capture_tool_reader control 5 "
                "(anti-vacuity, id-join) — retrieved_text was non-empty "
                "after stripping every tool_result block; the "
                "non-empty-text assertion in control 1 is not load-bearing",
                file=sys.stderr,
            )
            ok = False

    # Control 6: negative — graceful degradation on a capture with zero
    # matching tool calls.
    try:
        probe_triples = _iter_capture_tool_calls(probe_path)
    except Exception as exc:  # noqa: BLE001 — self-test must report, not crash
        print(
            f"self-test FAIL: capture_tool_reader control 6 (negative) — "
            f"raised unexpectedly on probe-P1.jsonl: {exc!r}",
            file=sys.stderr,
        )
        ok = False
    else:
        if probe_triples != []:
            print(
                f"self-test FAIL: capture_tool_reader control 6 (negative) "
                f"— expected [] on probe-P1.jsonl, got {probe_triples!r}",
                file=sys.stderr,
            )
            ok = False

    # Control 7: guardrail non-interference — re-prove Guardrails A and B
    # on the new fixture without touching their own self-test items.
    dispatch_ids = _find_agent_dispatch_ids(objs, "first-principles:first-principles")
    if len(dispatch_ids) != 1:
        print(
            f"self-test FAIL: capture_tool_reader control 7 (guardrail "
            f"non-interference) — expected exactly 1 Agent dispatch id, "
            f"got {len(dispatch_ids)}",
            file=sys.stderr,
        )
        ok = False
    try:
        analysis = extract_agent_analysis(
            fixture_path, subagent_type="first-principles:first-principles"
        )
    except Exception as exc:  # noqa: BLE001
        print(
            f"self-test FAIL: capture_tool_reader control 7 (guardrail "
            f"non-interference) — extract_agent_analysis raised "
            f"unexpectedly: {exc!r}",
            file=sys.stderr,
        )
        ok = False
    else:
        result_field = _read_top_level_result(fixture_path)
        if len(analysis) != 34943:
            print(
                f"self-test FAIL: capture_tool_reader control 7 (guardrail "
                f"non-interference) — expected 34943-char analysis, got "
                f"{len(analysis)}",
                file=sys.stderr,
            )
            ok = False
        if len(result_field) != 2636:
            print(
                f"self-test FAIL: capture_tool_reader control 7 (guardrail "
                f"non-interference) — expected 2636-char top-level result "
                f"field, got {len(result_field)}",
                file=sys.stderr,
            )
            ok = False
        if analysis == result_field or len(analysis) <= 2 * len(result_field):
            print(
                "self-test FAIL: capture_tool_reader control 7 (guardrail "
                "non-interference) — extracted analysis is not decisively "
                "longer than the top-level result field",
                file=sys.stderr,
            )
            ok = False

    # Control 8: POSITIVE, anti-masking for the dispatch_ids filter — pin
    # the literal dispatch id and prove filtering by it does not simply
    # reject everything.
    pr_p1_dispatch_ids = _find_agent_dispatch_ids(
        objs, "first-principles:first-principles"
    )
    if pr_p1_dispatch_ids != ["toolu_01WdhFJm9dSLjMurLvtpo3MX"]:
        print(
            f"self-test FAIL: capture_tool_reader control 8 (positive, "
            f"anti-masking) — expected dispatch id "
            f"['toolu_01WdhFJm9dSLjMurLvtpo3MX'], got {pr_p1_dispatch_ids!r}",
            file=sys.stderr,
        )
        ok = False
    pr_p1_dispatch_set = frozenset(pr_p1_dispatch_ids)
    filtered_triples = _iter_capture_tool_calls(
        fixture_path, dispatch_ids=pr_p1_dispatch_set
    )
    if filtered_triples != triples:
        print(
            f"self-test FAIL: capture_tool_reader control 8 (positive, "
            f"anti-masking) — filtering by PR-P1's own dispatch id changed "
            f"the result: expected the same {len(triples)} triples, got "
            f"{len(filtered_triples)}",
            file=sys.stderr,
        )
        ok = False

    # Control 9: DISCRIMINATION — the only control with teeth on the
    # parent/subagent attribution axis. Synthesise a parent-session Read by
    # rewriting parent_tool_use_id=None on every assistant envelope whose
    # tool_use block is named "Read". No committed fixture supplies this
    # case (measured 2026-08-31: every non-Agent tool call in every
    # committed capture carries its own file's Agent dispatch id).
    read_mutated_objs = []
    read_mutation_count = 0
    for obj in objs:
        obj_copy = json.loads(json.dumps(obj))
        if obj_copy.get("type") == "assistant":
            msg = obj_copy.get("message")
            content = msg.get("content") if isinstance(msg, dict) else None
            is_read_envelope = isinstance(content, list) and any(
                isinstance(c, dict)
                and c.get("type") == "tool_use"
                and c.get("name") == "Read"
                for c in content
            )
            if is_read_envelope:
                obj_copy["parent_tool_use_id"] = None
                read_mutation_count += 1
        read_mutated_objs.append(obj_copy)

    if read_mutation_count != 2:
        print(
            f"self-test FAIL: capture_tool_reader control 9 "
            f"(discrimination) — mutation setup failed: expected exactly "
            f"2 Read-bearing assistant envelopes rewritten, got "
            f"{read_mutation_count}; the mutation predicate matched "
            f"nothing (or too much), so the control below would be "
            f"vacuous",
            file=sys.stderr,
        )
        ok = False
    else:
        with tempfile.TemporaryDirectory() as tmpdir9:
            read_mutated_path = Path(tmpdir9) / "read-mutated.jsonl"
            read_mutated_path.write_text(
                "\n".join(json.dumps(o) for o in read_mutated_objs),
                encoding="utf-8",
            )
            unfiltered_mutated = _iter_capture_tool_calls(read_mutated_path)
            filtered_mutated = _iter_capture_tool_calls(
                read_mutated_path, dispatch_ids=pr_p1_dispatch_set
            )
            if len(unfiltered_mutated) != 9:
                print(
                    f"self-test FAIL: capture_tool_reader control 9 "
                    f"(discrimination) — unfiltered call on the mutated "
                    f"copy should still see 9 triples, got "
                    f"{len(unfiltered_mutated)}",
                    file=sys.stderr,
                )
                ok = False
            if len(filtered_mutated) != 7 or any(
                name != "WebFetch" for name, _, _ in filtered_mutated
            ):
                print(
                    f"self-test FAIL: capture_tool_reader control 9 "
                    f"(discrimination) — filtering by PR-P1's dispatch id "
                    f"on the mutated copy should drop both synthesised "
                    f"parent-session Read triples and keep exactly 7 "
                    f"WebFetch triples, got {filtered_mutated!r}. An "
                    f"implementation that ignores parent_tool_use_id "
                    f"returns 9 in both the unfiltered and filtered case.",
                    file=sys.stderr,
                )
                ok = False

    # Control 10: CROSS-CAPTURE — the weak leg. Satisfiable by any filter
    # whatsoever; control 9, not this one, is what makes the attribution
    # axis failable.
    internal_path = FIXTURES_DIR / "gen-internal-tools.jsonl"
    cross_capture_triples = _iter_capture_tool_calls(
        internal_path, dispatch_ids=pr_p1_dispatch_set
    )
    if cross_capture_triples != []:
        print(
            f"self-test FAIL: capture_tool_reader control 10 "
            f"(cross-capture) — filtering gen-internal-tools.jsonl by "
            f"PR-P1's dispatch id should return [], got "
            f"{cross_capture_triples!r}",
            file=sys.stderr,
        )
        ok = False

    # Control 11: ANTI-OVER-REJECTION + the README correction. Measured
    # 2026-08-31: gen-internal-tools.jsonl's Read is the SUBAGENT's own,
    # attributed to toolu_01TQ6wqRTxaExMFGutr8Rj5Y, contradicting
    # tests/quality-provenance-v8.24/README.md lines 126-129 (which the
    # README is frozen evidence and is not edited to correct — the
    # correction is asserted here instead). A "== []" result here would
    # mean the filter over-rejects a subagent's own call.
    internal_objs = _iter_jsonl_objects(internal_path)
    internal_dispatch_ids = _find_agent_dispatch_ids(
        internal_objs, "first-principles:first-principles"
    )
    internal_own_triples = _iter_capture_tool_calls(
        internal_path, dispatch_ids=frozenset(internal_dispatch_ids)
    )
    if (
        len(internal_own_triples) != 1
        or internal_own_triples[0][0] != "Read"
        or not internal_own_triples[0][1].endswith(
            "svg-precision/references/spec.md"
        )
        or len(internal_own_triples[0][2]) != 6309
    ):
        print(
            f"self-test FAIL: capture_tool_reader control 11 "
            f"(anti-over-rejection) — expected exactly one Read triple "
            f"ending svg-precision/references/spec.md with 6309 chars "
            f"when filtering gen-internal-tools.jsonl by its own dispatch "
            f"id, got {internal_own_triples!r}",
            file=sys.stderr,
        )
        ok = False

    # Control 12: WR-04 — an unmapped tool_names value raises rather than
    # returning a blank target.
    try:
        _iter_capture_tool_calls(fixture_path, tool_names=("Agent",))
    except ValueError as exc:
        if "Agent" not in str(exc) or "_CAPTURE_TOOL_TARGET_KEYS" not in str(exc):
            print(
                f"self-test FAIL: capture_tool_reader control 12 (WR-04) "
                f"— ValueError message does not name Agent and "
                f"_CAPTURE_TOOL_TARGET_KEYS: {exc!r}",
                file=sys.stderr,
            )
            ok = False
    else:
        print(
            "self-test FAIL: capture_tool_reader control 12 (WR-04) — "
            "tool_names=('Agent',) did not raise ValueError",
            file=sys.stderr,
        )
        ok = False
    try:
        _iter_capture_tool_calls(fixture_path, tool_names=("WebFetch", "Bash"))
    except ValueError as exc:
        if "Bash" not in str(exc) or "_CAPTURE_TOOL_TARGET_KEYS" not in str(exc):
            print(
                f"self-test FAIL: capture_tool_reader control 12 (WR-04) "
                f"— ValueError message does not name Bash and "
                f"_CAPTURE_TOOL_TARGET_KEYS: {exc!r}",
                file=sys.stderr,
            )
            ok = False
    else:
        print(
            "self-test FAIL: capture_tool_reader control 12 (WR-04) — "
            "tool_names=('WebFetch', 'Bash') did not raise ValueError, "
            "even though 'Bash' is unmapped",
            file=sys.stderr,
        )
        ok = False

    # Control 13: WRAPPER — _capture_subagent_tool_calls composes the
    # filter correctly, and raises rather than returning [] when the named
    # subagent never dispatched.
    wrapper_triples = _capture_subagent_tool_calls(
        fixture_path, "first-principles:first-principles"
    )
    if wrapper_triples != filtered_triples:
        print(
            f"self-test FAIL: capture_tool_reader control 13 (wrapper) — "
            f"_capture_subagent_tool_calls does not equal control 8's "
            f"filtered result",
            file=sys.stderr,
        )
        ok = False
    try:
        _capture_subagent_tool_calls(fixture_path, "no-such:agent")
    except ValueError as exc:
        if "no-such:agent" not in str(exc):
            print(
                f"self-test FAIL: capture_tool_reader control 13 "
                f"(wrapper) — ValueError message does not name the "
                f"subagent_type: {exc!r}",
                file=sys.stderr,
            )
            ok = False
    else:
        print(
            "self-test FAIL: capture_tool_reader control 13 (wrapper) — "
            "a never-dispatched subagent_type did not raise ValueError",
            file=sys.stderr,
        )
        ok = False

    return ok


def _selftest_analysis_persistence() -> bool:
    """Item 20 (v8.24.0 Phase 4, CAP-01): _extract_and_persist_analysis proves
    it leaves the extracted analysis beside its source .jsonl, in code, with
    the completed-gate and both extraction guardrails carried through.

    Six independently-failable controls, each on a fixture copied into a
    tempfile.TemporaryDirectory() before the helper touches it — never on a
    committed fixture path directly, since the helper writes beside its
    source and a committed tests/ path is inside the FROZEN-EVIDENCE
    pathspec:

    1. POSITIVE round trip — a tempdir copy of PROVENANCE_FIXTURE_DIR's
       PR-P1.jsonl produces a `.md` sibling at exactly `<tmp>/PR-P1.md`,
       byte-identical to the committed PR-P1.md, 34,943 chars.
    2. POSITIVE second capture — a tempdir copy of FIXTURES_DIR's
       gen-single-dispatch.jsonl produces an 8,739-char `.md` sibling,
       matching the length _selftest_guardrail_a already pins.
    3. GUARDRAIL A CARRIED THROUGH — for the gen-single-dispatch case, the
       written text does not contain _LAUNCH_ACK_PHRASE and is decisively
       longer than (never equal to) _read_top_level_result on the same
       capture.
    4. NEGATIVE — a tempdir copy of gen-internal-tools.jsonl
       (no_terminal_result) returns None, and no `.md` sibling exists on
       disk.
    5. ANTI-MASKING (extraction failure not swallowed) — a tempdir copy of
       gen-stub-only.jsonl (completed, but raises on extraction) makes the
       helper raise, not return None, and leaves no `.md` sibling.
    6. ANTI-MASKING (multi-dispatch reaches the caller) — a tempdir copy of
       gen-multi-dispatch.jsonl raises MultipleAgentDispatchError with the
       dispatch count "2" in the message, and leaves no `.md` sibling.
    """
    ok = True

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        # Control 1: positive round trip against real evidence.
        pr_p1_src = PROVENANCE_FIXTURE_DIR / "PR-P1.jsonl"
        pr_p1_copy = tmp_path / "PR-P1.jsonl"
        pr_p1_copy.write_bytes(pr_p1_src.read_bytes())
        result1 = _extract_and_persist_analysis(
            pr_p1_copy, subagent_type="first-principles:first-principles"
        )
        expected_md_path = tmp_path / "PR-P1.md"
        if result1 != expected_md_path:
            print(
                f"self-test FAIL: analysis_persistence control 1 (positive "
                f"round trip) — expected return {expected_md_path}, got {result1}",
                file=sys.stderr,
            )
            ok = False
        else:
            written_text = expected_md_path.read_text(encoding="utf-8")
            committed_text = (PROVENANCE_FIXTURE_DIR / "PR-P1.md").read_text(encoding="utf-8")
            if written_text != committed_text:
                print(
                    "self-test FAIL: analysis_persistence control 1 (positive "
                    "round trip) — written .md is not byte-identical to the "
                    "committed PR-P1.md",
                    file=sys.stderr,
                )
                ok = False
            if len(written_text) != 34943:
                print(
                    f"self-test FAIL: analysis_persistence control 1 (positive "
                    f"round trip) — expected 34943 chars, got {len(written_text)}",
                    file=sys.stderr,
                )
                ok = False

        # Control 2 + 3: second capture, different donor; Guardrail A carried
        # through the wrapper.
        single_src = FIXTURES_DIR / "gen-single-dispatch.jsonl"
        single_copy = tmp_path / "gen-single-dispatch.jsonl"
        single_copy.write_bytes(single_src.read_bytes())
        result2 = _extract_and_persist_analysis(
            single_copy, subagent_type="first-principles:first-principles"
        )
        expected_single_md = tmp_path / "gen-single-dispatch.md"
        if result2 != expected_single_md:
            print(
                f"self-test FAIL: analysis_persistence control 2 (positive "
                f"second capture) — expected return {expected_single_md}, "
                f"got {result2}",
                file=sys.stderr,
            )
            ok = False
        else:
            single_text = expected_single_md.read_text(encoding="utf-8")
            if len(single_text) != 8739:
                print(
                    f"self-test FAIL: analysis_persistence control 2 (positive "
                    f"second capture) — expected 8739 chars, got {len(single_text)}",
                    file=sys.stderr,
                )
                ok = False
            if _LAUNCH_ACK_PHRASE in single_text:
                print(
                    "self-test FAIL: analysis_persistence control 3 (guardrail "
                    "A carried through) — written text contains "
                    f"_LAUNCH_ACK_PHRASE {_LAUNCH_ACK_PHRASE!r}",
                    file=sys.stderr,
                )
                ok = False
            result_field = _read_top_level_result(single_copy)
            if single_text == result_field or len(single_text) <= 2 * len(result_field):
                print(
                    "self-test FAIL: analysis_persistence control 3 (guardrail "
                    "A carried through) — written text is not decisively "
                    f"longer than the top-level result field (written "
                    f"len={len(single_text)}, result field len={len(result_field)})",
                    file=sys.stderr,
                )
                ok = False

        # Control 4: negative — not completed means no file.
        internal_src = FIXTURES_DIR / "gen-internal-tools.jsonl"
        internal_copy = tmp_path / "gen-internal-tools.jsonl"
        internal_copy.write_bytes(internal_src.read_bytes())
        result4 = _extract_and_persist_analysis(
            internal_copy, subagent_type="first-principles:first-principles"
        )
        if result4 is not None:
            print(
                f"self-test FAIL: analysis_persistence control 4 (negative) "
                f"— expected None for a non-completed capture, got {result4}",
                file=sys.stderr,
            )
            ok = False
        if internal_copy.with_suffix(".md").exists():
            print(
                "self-test FAIL: analysis_persistence control 4 (negative) "
                "— a .md sibling was written for a non-completed capture",
                file=sys.stderr,
            )
            ok = False

        # Control 5: anti-masking — a guardrail failure is not swallowed.
        stub_src = FIXTURES_DIR / "gen-stub-only.jsonl"
        stub_copy = tmp_path / "gen-stub-only.jsonl"
        stub_copy.write_bytes(stub_src.read_bytes())
        try:
            _extract_and_persist_analysis(
                stub_copy, subagent_type="first-principles:first-principles"
            )
            print(
                "self-test FAIL: analysis_persistence control 5 (anti-masking, "
                "extraction failure) — gen-stub-only.jsonl (completed, "
                "unextractable) did not raise",
                file=sys.stderr,
            )
            ok = False
        except AgentAnalysisExtractionError:
            pass
        except Exception as exc:  # noqa: BLE001
            print(
                f"self-test FAIL: analysis_persistence control 5 (anti-masking, "
                f"extraction failure) — raised the wrong exception type: {exc!r}",
                file=sys.stderr,
            )
            ok = False
        if stub_copy.with_suffix(".md").exists():
            print(
                "self-test FAIL: analysis_persistence control 5 (anti-masking, "
                "extraction failure) — a .md sibling was written despite the "
                "raise",
                file=sys.stderr,
            )
            ok = False

        # Control 6: anti-masking — the multi-dispatch guardrail still
        # reaches the caller.
        multi_src = FIXTURES_DIR / "gen-multi-dispatch.jsonl"
        multi_copy = tmp_path / "gen-multi-dispatch.jsonl"
        multi_copy.write_bytes(multi_src.read_bytes())
        try:
            _extract_and_persist_analysis(
                multi_copy, subagent_type="first-principles:first-principles"
            )
            print(
                "self-test FAIL: analysis_persistence control 6 (anti-masking, "
                "multi-dispatch) — gen-multi-dispatch.jsonl did not raise",
                file=sys.stderr,
            )
            ok = False
        except MultipleAgentDispatchError as exc:
            if "2" not in str(exc):
                print(
                    f"self-test FAIL: analysis_persistence control 6 "
                    f"(anti-masking, multi-dispatch) — raised but did not "
                    f"name the dispatch count found: {exc!r}",
                    file=sys.stderr,
                )
                ok = False
        except Exception as exc:  # noqa: BLE001
            print(
                f"self-test FAIL: analysis_persistence control 6 (anti-masking, "
                f"multi-dispatch) — raised the wrong exception type: {exc!r}",
                file=sys.stderr,
            )
            ok = False
        if multi_copy.with_suffix(".md").exists():
            print(
                "self-test FAIL: analysis_persistence control 6 (anti-masking, "
                "multi-dispatch) — a .md sibling was written despite the raise",
                file=sys.stderr,
            )
            ok = False

    return ok


def _selftest_single_refusal() -> bool:
    """Item 21 (v8.24.0 Phase 4, CAP-01 closure): the `--single` CALL SITE
    refuses to reach `build_judge_packet` when the analysis was not
    persisted. Item 20's six controls all passed while the call site
    consuming `_extract_and_persist_analysis` was defective (CR-02), so
    this item asserts the call site, not the helper — control 4 is the
    reason this is its own item rather than a seventh control on item 20.

    Five independently-failable controls, plus a tempdir-copy discipline
    identical to item 20's (fixtures copied before the helper touches
    them; a committed `tests/` path is never passed directly):

    1. POSITIVE — a tempdir copy of PR-P1.jsonl through
       `_persist_or_refuse_analysis` returns `(<tmp>/PR-P1.md, "")`; the
       file exists and is byte-identical to the committed PR-P1.md.
    2. NEGATIVE (the CR-02 class) — a tempdir copy of
       gen-internal-tools.jsonl returns `(None, msg)` naming
       `no_terminal_result` and `Refusing`; no `.md` sibling exists.
    3. ANTI-VACUITY / reachability — on that same tempdir copy,
       `extract_agent_analysis` still returns exactly 2,769 chars, proving
       control 2's refusal fires on a capture whose analysis extracts
       perfectly, not on a degenerate unextractable one.
    4. CALL-SITE STRUCTURE — `main()`'s `--single` source block is sliced
       between two literal anchors and asserted to call
       `_persist_or_refuse_analysis(`, contain `return 1` before
       `build_judge_packet(`, never call `extract_agent_analysis(`
       directly, and read the judged text back via
       `analysis_path.read_text(`. A missing anchor is itself a FAILURE
       naming the drift, never a traceback and never a silent skip.
    5. ANTI-MASKING (guardrail pass-through) — a tempdir copy of
       gen-multi-dispatch.jsonl makes the wrapper raise
       `MultipleAgentDispatchError`, and a tempdir copy of
       gen-stub-only.jsonl makes it raise `AgentAnalysisExtractionError`;
       neither collapses into `(None, msg)`.
    """
    ok = True

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        # Control 1: positive round trip against real evidence.
        pr_p1_src = PROVENANCE_FIXTURE_DIR / "PR-P1.jsonl"
        pr_p1_copy = tmp_path / "PR-P1.jsonl"
        pr_p1_copy.write_bytes(pr_p1_src.read_bytes())
        result1_path, result1_msg = _persist_or_refuse_analysis(
            pr_p1_copy, subagent_type="first-principles:first-principles"
        )
        expected_md_path = tmp_path / "PR-P1.md"
        if result1_path != expected_md_path or result1_msg != "":
            print(
                f"self-test FAIL: single_refusal control 1 (positive) — "
                f"expected ({expected_md_path}, ''), got "
                f"({result1_path}, {result1_msg!r})",
                file=sys.stderr,
            )
            ok = False
        elif not expected_md_path.exists():
            print(
                "self-test FAIL: single_refusal control 1 (positive) — "
                f"{expected_md_path} does not exist on disk",
                file=sys.stderr,
            )
            ok = False
        else:
            written_text = expected_md_path.read_text(encoding="utf-8")
            committed_text = (PROVENANCE_FIXTURE_DIR / "PR-P1.md").read_text(encoding="utf-8")
            if written_text != committed_text:
                print(
                    "self-test FAIL: single_refusal control 1 (positive) — "
                    "written .md is not byte-identical to the committed "
                    "PR-P1.md",
                    file=sys.stderr,
                )
                ok = False

        # Control 2 + 3: negative refusal (the CR-02 class) and the
        # anti-vacuity reachability check that gives it meaning.
        internal_src = FIXTURES_DIR / "gen-internal-tools.jsonl"
        internal_copy = tmp_path / "gen-internal-tools.jsonl"
        internal_copy.write_bytes(internal_src.read_bytes())
        result2_path, result2_msg = _persist_or_refuse_analysis(
            internal_copy, subagent_type="first-principles:first-principles"
        )
        if result2_path is not None:
            print(
                f"self-test FAIL: single_refusal control 2 (negative) — "
                f"expected a None path for a non-completed capture, got "
                f"{result2_path}",
                file=sys.stderr,
            )
            ok = False
        else:
            if "no_terminal_result" not in result2_msg:
                print(
                    f"self-test FAIL: single_refusal control 2 (negative) — "
                    f"refusal message does not name the classified outcome: "
                    f"{result2_msg!r}",
                    file=sys.stderr,
                )
                ok = False
            if "Refusing" not in result2_msg:
                print(
                    f"self-test FAIL: single_refusal control 2 (negative) — "
                    f"refusal message does not read as a refusal: "
                    f"{result2_msg!r}",
                    file=sys.stderr,
                )
                ok = False
        if internal_copy.with_suffix(".md").exists():
            print(
                "self-test FAIL: single_refusal control 2 (negative) — a "
                ".md sibling was written despite the refusal",
                file=sys.stderr,
            )
            ok = False

        internal_analysis = extract_agent_analysis(
            internal_copy, subagent_type="first-principles:first-principles"
        )
        if len(internal_analysis) != 2769:
            print(
                f"self-test FAIL: single_refusal control 3 (anti-vacuity) — "
                f"expected 2769 chars from a capture that extracts "
                f"perfectly, got {len(internal_analysis)}",
                file=sys.stderr,
            )
            ok = False

        # Control 5: anti-masking — a guardrail failure must never collapse
        # into a refusal tuple.
        multi_src = FIXTURES_DIR / "gen-multi-dispatch.jsonl"
        multi_copy = tmp_path / "gen-multi-dispatch.jsonl"
        multi_copy.write_bytes(multi_src.read_bytes())
        try:
            _persist_or_refuse_analysis(
                multi_copy, subagent_type="first-principles:first-principles"
            )
            print(
                "self-test FAIL: single_refusal control 5 (anti-masking, "
                "multi-dispatch) — gen-multi-dispatch.jsonl did not raise",
                file=sys.stderr,
            )
            ok = False
        except MultipleAgentDispatchError:
            pass
        except Exception as exc:  # noqa: BLE001
            print(
                f"self-test FAIL: single_refusal control 5 (anti-masking, "
                f"multi-dispatch) — raised the wrong exception type: {exc!r}",
                file=sys.stderr,
            )
            ok = False

        stub_src = FIXTURES_DIR / "gen-stub-only.jsonl"
        stub_copy = tmp_path / "gen-stub-only.jsonl"
        stub_copy.write_bytes(stub_src.read_bytes())
        try:
            _persist_or_refuse_analysis(
                stub_copy, subagent_type="first-principles:first-principles"
            )
            print(
                "self-test FAIL: single_refusal control 5 (anti-masking, "
                "extraction failure) — gen-stub-only.jsonl (completed, "
                "unextractable) did not raise",
                file=sys.stderr,
            )
            ok = False
        except AgentAnalysisExtractionError:
            pass
        except Exception as exc:  # noqa: BLE001
            print(
                f"self-test FAIL: single_refusal control 5 (anti-masking, "
                f"extraction failure) — raised the wrong exception type: "
                f"{exc!r}",
                file=sys.stderr,
            )
            ok = False

    # Control 4: the --single call site's structure, sliced from main()'s
    # own source so a regression cannot land un-noticed.
    src = inspect.getsource(main)
    start_anchor = "\n    if args.single is not None:"
    end_anchor = "\n    if args.detect_defects is not None:"
    start_idx = src.find(start_anchor)
    end_idx = src.find(end_anchor)
    if start_idx == -1 or end_idx == -1:
        print(
            "self-test FAIL: single_refusal control 4 (call-site structure) "
            "— the --single/--detect-defects anchors have moved; this "
            "control cannot locate the block it must inspect",
            file=sys.stderr,
        )
        ok = False
    else:
        block = src[start_idx:end_idx]
        if "_persist_or_refuse_analysis(" not in block:
            print(
                "self-test FAIL: single_refusal control 4 (call-site "
                "structure) — _persist_or_refuse_analysis( not called in "
                "the --single block",
                file=sys.stderr,
            )
            ok = False
        if "return 1" not in block:
            print(
                "self-test FAIL: single_refusal control 4 (call-site "
                "structure) — no 'return 1' in the --single block",
                file=sys.stderr,
            )
            ok = False
        if "build_judge_packet(" not in block:
            print(
                "self-test FAIL: single_refusal control 4 (call-site "
                "structure) — build_judge_packet( not called in the "
                "--single block",
                file=sys.stderr,
            )
            ok = False
        if (
            "return 1" in block
            and "build_judge_packet(" in block
            and block.index("return 1") >= block.index("build_judge_packet(")
        ):
            print(
                "self-test FAIL: single_refusal control 4 (call-site "
                "structure) — 'return 1' does not precede "
                "build_judge_packet( — the refusal does not gate the judge",
                file=sys.stderr,
            )
            ok = False
        if "extract_agent_analysis(" in block:
            print(
                "self-test FAIL: single_refusal control 4 (call-site "
                "structure) — extract_agent_analysis( is still called "
                "directly in the --single block (WR-03)",
                file=sys.stderr,
            )
            ok = False
        if "analysis_path.read_text(" not in block:
            print(
                "self-test FAIL: single_refusal control 4 (call-site "
                "structure) — analysis_path.read_text( not found; the "
                "judged text is not read back from the persisted path",
                file=sys.stderr,
            )
            ok = False

    return ok


def _selftest_persistence_write_guards() -> bool:
    """Item 23 (Phase 999.5, WR-A + WR-B): the persistence write refuses an
    unsafe destination, and `--probe` diagnoses a failed persist instead of
    ending a paid live run in a bare traceback.

    Both findings are about the same call chain and are asserted together
    because the WR-A helper's own refusal path is reached through the WR-B
    guard — splitting them would leave that join untested from either side.

    Thirteen independently-failable controls. Every write-driving control uses
    a tempdir copy, with the single deliberate exception of control 5, whose
    whole point is the committed path (see its note):

    WR-B, the destination guard
      1. POSITIVE (symlink) — a tempdir `PR-P1.md` symlinked at a decoy makes
         `_extract_and_persist_analysis` raise `AnalysisWriteRefused` naming
         "symlink"; the decoy's bytes are unchanged and the link is still a
         link, so nothing was written through it.
      2. NON-VACUITY for control 1 — the same tempdir copy with no symlink at
         the destination writes normally and returns the `.md` path, proving
         control 1's refusal is caused by the link and not by the fixture.
      3. PATHSPEC PARSE — `read_frozen_pathspecs` over the live battery text
         returns a non-empty list containing `tests/quality-provenance-v8.24`
         and `tests/step0-baseline-v*.md`, i.e. both a literal directory entry
         and a globbed one.
      4. FAIL-CLOSED — battery text with the array renamed, battery text with
         an emptied array, and an unreadable battery path each raise
         `AnalysisWriteRefused` rather than yielding an empty pathspec list.
         An empty list would silently disable the guard, and "I could not
         read the list" is not "nothing is frozen".
      5. POSITIVE (frozen path, on the committed tree) — calling the helper
         directly on `PROVENANCE_FIXTURE_DIR / "PR-P1.jsonl"` — WR-B's own
         worked example — raises `AnalysisWriteRefused` naming
         "FROZEN-EVIDENCE", and the committed `PR-P1.md` is byte-unchanged.
         This is the one control that names a committed path on purpose: the
         guard is only meaningful if it fires on the real frozen tree. It is
         safe to run even if the guard is broken, because item 20 control 1
         pins that this extraction reproduces `PR-P1.md` byte-identically —
         a failed guard would rewrite identical content, so FROZEN-EVIDENCE
         cannot be tripped by this control either way.
      6. ANTI-OVERREACH — `is_frozen_destination` is False for a repo path
         outside every pathspec (`tests/routing-catalog.md`) and for a path
         outside the repo entirely, and True for a nested path under a
         globbed directory entry. Without this, a guard that answered True
         unconditionally would pass controls 1-5.

    WR-A, the probe diagnosis
      7. POSITIVE — a tempdir PR-P1 copy through `_persist_or_diagnose_
         analysis` returns `(<tmp>/PR-P1.md, "Probe analysis written: ...", 0)`.
      8. NOT-COMPLETED — a tempdir `gen-internal-tools.jsonl` returns
         `(None, msg, 0)` naming `no_terminal_result`; status 0 because
         nothing was owed.
      9. THE WR-A CASE — a tempdir `gen-stub-only.jsonl` (completed,
         unextractable: the exact capture the review reproduced against)
         returns `(None, msg, 1)`, does NOT raise, and the message names both
         the intact `.jsonl` path and that no second live run is needed.
     10. MULTI-DISPATCH — a tempdir `gen-multi-dispatch.jsonl` likewise
         returns status 1 rather than raising.
     11. ANTI-COSMETIC — controls 9 and 10 must carry a NON-ZERO status. A
         diagnosis printed on a 0 exit is invisible to any caller that
         branches on the status, which would restore WR-A's damage with
         better prose. Asserted separately so a status regression names
         itself rather than hiding inside control 9's tuple comparison.
     12. CALL-SITE STRUCTURE — `main()`'s `--probe` block is sliced between
         two literal anchors and asserted to call
         `_persist_or_diagnose_analysis(`, to never call
         `_extract_and_persist_analysis(` directly, and to return the helper's
         status rather than a literal `return 0`. A missing anchor is itself a
         FAILURE naming the drift, never a traceback and never a silent skip.
         Item 21 control 4 is the precedent: item 20's six controls all passed
         while the call site consuming the helper was defective.

    WR-B's other consumer
     13. SINGLE REFUSAL ASYMMETRY — `_persist_or_refuse_analysis` converts
         `AnalysisWriteRefused` into a `(None, msg)` refusal naming
         "Refusing", so `--single` against a frozen capture exits on a
         refusal rather than a traceback; and it still RAISES for both
         guardrail errors, so item 21 control 5's invariant is intact. The
         second half is what makes the first half a considered asymmetry
         rather than a blanket `except`.
    """
    ok = True
    subagent = "first-principles:first-principles"

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        pr_p1_src = PROVENANCE_FIXTURE_DIR / "PR-P1.jsonl"

        # Control 1: symlink destination is refused, and nothing is written
        # through the link.
        link_dir = tmp_path / "symlink-case"
        link_dir.mkdir()
        link_copy = link_dir / "PR-P1.jsonl"
        link_copy.write_bytes(pr_p1_src.read_bytes())
        decoy = link_dir / "decoy.md"
        decoy.write_text("DECOY", encoding="utf-8")
        (link_dir / "PR-P1.md").symlink_to(decoy)
        try:
            _extract_and_persist_analysis(link_copy, subagent_type=subagent)
            print(
                "self-test FAIL: persistence_write_guards control 1 (symlink) "
                "— writing through a symlinked destination did not raise",
                file=sys.stderr,
            )
            ok = False
        except AnalysisWriteRefused as exc:
            if "symlink" not in str(exc):
                print(
                    f"self-test FAIL: persistence_write_guards control 1 "
                    f"(symlink) — refusal does not name the condition: {exc!r}",
                    file=sys.stderr,
                )
                ok = False
        except Exception as exc:  # noqa: BLE001
            print(
                f"self-test FAIL: persistence_write_guards control 1 (symlink) "
                f"— raised the wrong exception type: {exc!r}",
                file=sys.stderr,
            )
            ok = False
        if decoy.read_text(encoding="utf-8") != "DECOY":
            print(
                "self-test FAIL: persistence_write_guards control 1 (symlink) "
                "— the analysis was written through the link into the decoy",
                file=sys.stderr,
            )
            ok = False
        if not (link_dir / "PR-P1.md").is_symlink():
            print(
                "self-test FAIL: persistence_write_guards control 1 (symlink) "
                "— the destination is no longer a symlink; it was replaced",
                file=sys.stderr,
            )
            ok = False

        # Control 2: non-vacuity — same fixture, no symlink, writes fine.
        clean_dir = tmp_path / "clean-case"
        clean_dir.mkdir()
        clean_copy = clean_dir / "PR-P1.jsonl"
        clean_copy.write_bytes(pr_p1_src.read_bytes())
        clean_result = _extract_and_persist_analysis(clean_copy, subagent_type=subagent)
        if clean_result != clean_dir / "PR-P1.md" or not clean_result.exists():
            print(
                f"self-test FAIL: persistence_write_guards control 2 "
                f"(non-vacuity) — an unguarded destination did not receive the "
                f"write; got {clean_result}",
                file=sys.stderr,
            )
            ok = False

        # Control 3: the pathspec list parses off the live battery script.
        battery_text = BATTERY_PATH.read_text(encoding="utf-8")
        specs = read_frozen_pathspecs(battery_text)
        for expected_spec in ("tests/quality-provenance-v8.24", "tests/step0-baseline-v*.md"):
            if expected_spec not in specs:
                print(
                    f"self-test FAIL: persistence_write_guards control 3 "
                    f"(pathspec parse) — {expected_spec!r} not among the "
                    f"{len(specs)} parsed entries",
                    file=sys.stderr,
                )
                ok = False

        # Control 4: fail-closed on an unparseable or empty array.
        renamed = battery_text.replace("_FROZEN_PATHS=(", "_THAWED_PATHS=(", 1)
        emptied = _FROZEN_PATHS_ARRAY_RE.sub("_FROZEN_PATHS=(\n)", battery_text, count=1)
        for label, mutated in (("renamed array", renamed), ("emptied array", emptied)):
            try:
                read_frozen_pathspecs(mutated)
                print(
                    f"self-test FAIL: persistence_write_guards control 4 "
                    f"(fail-closed, {label}) — returned instead of raising; a "
                    f"guard that cannot read its list must refuse, not allow",
                    file=sys.stderr,
                )
                ok = False
            except AnalysisWriteRefused:
                pass
            except Exception as exc:  # noqa: BLE001
                print(
                    f"self-test FAIL: persistence_write_guards control 4 "
                    f"(fail-closed, {label}) — wrong exception type: {exc!r}",
                    file=sys.stderr,
                )
                ok = False

        # Control 4 (third case): an UNREADABLE battery script is also
        # fail-closed. This is a different branch from an unparseable one —
        # the read raises before the parser is ever reached — and it is the
        # branch a harness copied out of the repo would hit.
        saved_battery_path = globals()["BATTERY_PATH"]
        globals()["BATTERY_PATH"] = tmp_path / "no-such-battery.sh"
        try:
            is_frozen_destination(REPO_ROOT / "tests" / "probe.md")
            print(
                "self-test FAIL: persistence_write_guards control 4 "
                "(fail-closed, unreadable battery) — an unreadable pathspec "
                "source returned instead of raising",
                file=sys.stderr,
            )
            ok = False
        except AnalysisWriteRefused:
            pass
        except Exception as exc:  # noqa: BLE001
            print(
                f"self-test FAIL: persistence_write_guards control 4 "
                f"(fail-closed, unreadable battery) — wrong exception type: "
                f"{exc!r}",
                file=sys.stderr,
            )
            ok = False
        finally:
            globals()["BATTERY_PATH"] = saved_battery_path

        # Control 5: the frozen tree itself — WR-B's worked example.
        committed_md = PROVENANCE_FIXTURE_DIR / "PR-P1.md"
        before = committed_md.read_bytes()
        try:
            _extract_and_persist_analysis(pr_p1_src, subagent_type=subagent)
            print(
                "self-test FAIL: persistence_write_guards control 5 (frozen "
                "path) — writing into tests/quality-provenance-v8.24/ did not "
                "raise",
                file=sys.stderr,
            )
            ok = False
        except AnalysisWriteRefused as exc:
            if "FROZEN-EVIDENCE" not in str(exc):
                print(
                    f"self-test FAIL: persistence_write_guards control 5 "
                    f"(frozen path) — refusal does not name the condition: "
                    f"{exc!r}",
                    file=sys.stderr,
                )
                ok = False
        except Exception as exc:  # noqa: BLE001
            print(
                f"self-test FAIL: persistence_write_guards control 5 (frozen "
                f"path) — raised the wrong exception type: {exc!r}",
                file=sys.stderr,
            )
            ok = False
        if committed_md.read_bytes() != before:
            print(
                "self-test FAIL: persistence_write_guards control 5 (frozen "
                "path) — the committed PR-P1.md changed on disk",
                file=sys.stderr,
            )
            ok = False

        # Control 6: anti-overreach — the guard must discriminate.
        overreach_cases = (
            (REPO_ROOT / "tests" / "routing-catalog.md", False, "unfrozen repo path"),
            (tmp_path / "anywhere.md", False, "path outside the repository"),
            (
                REPO_ROOT / "tests" / "step0-captures-v8.6" / "nested" / "x.md",
                True,
                "nested path under a globbed directory entry",
            ),
        )
        for candidate, expected, label in overreach_cases:
            actual = is_frozen_destination(candidate, battery_text=battery_text)
            if actual is not expected:
                print(
                    f"self-test FAIL: persistence_write_guards control 6 "
                    f"(anti-overreach, {label}) — expected {expected}, got "
                    f"{actual} for {candidate}",
                    file=sys.stderr,
                )
                ok = False

        # Controls 7-11: the --probe decision helper.
        probe_dir = tmp_path / "probe-case"
        probe_dir.mkdir()

        def _probe_copy(name: str) -> Path:
            src = (
                PROVENANCE_FIXTURE_DIR / name
                if (PROVENANCE_FIXTURE_DIR / name).exists()
                else FIXTURES_DIR / name
            )
            dst = probe_dir / name
            dst.write_bytes(src.read_bytes())
            return dst

        # Control 7: positive.
        p7 = _probe_copy("PR-P1.jsonl")
        path7, msg7, status7 = _persist_or_diagnose_analysis(p7, subagent_type=subagent)
        if path7 != probe_dir / "PR-P1.md" or status7 != 0 or "written" not in msg7:
            print(
                f"self-test FAIL: persistence_write_guards control 7 (probe "
                f"positive) — got ({path7}, {msg7!r}, {status7})",
                file=sys.stderr,
            )
            ok = False

        # Control 8: not completed — nothing was owed, so status 0.
        p8 = _probe_copy("gen-internal-tools.jsonl")
        path8, msg8, status8 = _persist_or_diagnose_analysis(p8, subagent_type=subagent)
        if path8 is not None or status8 != 0 or "no_terminal_result" not in msg8:
            print(
                f"self-test FAIL: persistence_write_guards control 8 (probe "
                f"not-completed) — got ({path8}, {msg8!r}, {status8})",
                file=sys.stderr,
            )
            ok = False

        # Controls 9 + 10: the two failure captures must be diagnosed, never
        # raised, out of the probe helper.
        failure_statuses: dict[str, int] = {}
        for control_no, name in ((9, "gen-stub-only.jsonl"), (10, "gen-multi-dispatch.jsonl")):
            fixture = _probe_copy(name)
            try:
                fpath, fmsg, fstatus = _persist_or_diagnose_analysis(
                    fixture, subagent_type=subagent
                )
            except Exception as exc:  # noqa: BLE001
                print(
                    f"self-test FAIL: persistence_write_guards control "
                    f"{control_no} (probe {name}) — the helper raised instead "
                    f"of diagnosing: {exc!r}",
                    file=sys.stderr,
                )
                ok = False
                continue
            failure_statuses[name] = fstatus
            if fpath is not None:
                print(
                    f"self-test FAIL: persistence_write_guards control "
                    f"{control_no} (probe {name}) — expected no path, got {fpath}",
                    file=sys.stderr,
                )
                ok = False
            if str(fixture) not in fmsg or "without another" not in fmsg:
                print(
                    f"self-test FAIL: persistence_write_guards control "
                    f"{control_no} (probe {name}) — the diagnosis does not "
                    f"tell the operator the capture is intact and re-usable: "
                    f"{fmsg!r}",
                    file=sys.stderr,
                )
                ok = False
            if fixture.with_suffix(".md").exists():
                print(
                    f"self-test FAIL: persistence_write_guards control "
                    f"{control_no} (probe {name}) — a .md sibling was written "
                    f"for an unpersistable capture",
                    file=sys.stderr,
                )
                ok = False

        # Control 11: anti-cosmetic — the diagnosis must carry a non-zero
        # status or no caller can act on it.
        for name, fstatus in failure_statuses.items():
            if fstatus == 0:
                print(
                    f"self-test FAIL: persistence_write_guards control 11 "
                    f"(anti-cosmetic) — {name} was diagnosed with exit status "
                    f"0; a caller branching on the status cannot see it",
                    file=sys.stderr,
                )
                ok = False
        if len(failure_statuses) != 2:
            print(
                f"self-test FAIL: persistence_write_guards control 11 "
                f"(anti-cosmetic) — expected 2 recorded failure statuses, got "
                f"{len(failure_statuses)}; controls 9/10 did not both run",
                file=sys.stderr,
            )
            ok = False

        # Control 13: --single's wrapper converts a write refusal but still
        # raises for the two guardrail errors.
        try:
            refuse_path, refuse_msg = _persist_or_refuse_analysis(
                pr_p1_src, subagent_type=subagent
            )
        except Exception as exc:  # noqa: BLE001
            print(
                f"self-test FAIL: persistence_write_guards control 13 (single "
                f"refusal asymmetry) — a frozen destination raised out of the "
                f"refusal wrapper instead of becoming a refusal tuple: {exc!r}",
                file=sys.stderr,
            )
            ok = False
            refuse_path, refuse_msg = None, "Refusing"  # keep the next checks readable
        if refuse_path is not None or "Refusing" not in refuse_msg:
            print(
                f"self-test FAIL: persistence_write_guards control 13 (single "
                f"refusal asymmetry) — a frozen destination did not become a "
                f"refusal tuple; got ({refuse_path}, {refuse_msg!r})",
                file=sys.stderr,
            )
            ok = False
        if committed_md.read_bytes() != before:
            print(
                "self-test FAIL: persistence_write_guards control 13 (single "
                "refusal asymmetry) — the committed PR-P1.md changed on disk",
                file=sys.stderr,
            )
            ok = False
        for exc_type, name in (
            (MultipleAgentDispatchError, "gen-multi-dispatch.jsonl"),
            (AgentAnalysisExtractionError, "gen-stub-only.jsonl"),
        ):
            guard_copy = tmp_path / f"asym-{name}"
            guard_copy.write_bytes((FIXTURES_DIR / name).read_bytes())
            try:
                _persist_or_refuse_analysis(guard_copy, subagent_type=subagent)
                print(
                    f"self-test FAIL: persistence_write_guards control 13 "
                    f"(single refusal asymmetry) — {name} was collapsed into a "
                    f"refusal tuple; guardrail errors must still reach the "
                    f"caller (item 21 control 5)",
                    file=sys.stderr,
                )
                ok = False
            except exc_type:
                pass
            except Exception as exc:  # noqa: BLE001
                print(
                    f"self-test FAIL: persistence_write_guards control 13 "
                    f"(single refusal asymmetry) — {name} raised the wrong "
                    f"exception type: {exc!r}",
                    file=sys.stderr,
                )
                ok = False

    # Control 12: the --probe call site's structure, sliced from main()'s own
    # source so a regression cannot land un-noticed.
    src = inspect.getsource(main)
    start_anchor = "\n    if args.probe is not None:"
    end_anchor = "\n    if args.single is not None:"
    start_idx = src.find(start_anchor)
    end_idx = src.find(end_anchor)
    if start_idx == -1 or end_idx == -1 or end_idx <= start_idx:
        print(
            "self-test FAIL: persistence_write_guards control 12 (call-site "
            "structure) — the --probe/--single anchors have moved; this "
            "control cannot locate the block it must inspect",
            file=sys.stderr,
        )
        ok = False
    else:
        block = src[start_idx:end_idx]
        if "_persist_or_diagnose_analysis(" not in block:
            print(
                "self-test FAIL: persistence_write_guards control 12 "
                "(call-site structure) — _persist_or_diagnose_analysis( not "
                "called in the --probe block (WR-A)",
                file=sys.stderr,
            )
            ok = False
        if "_extract_and_persist_analysis(" in block:
            print(
                "self-test FAIL: persistence_write_guards control 12 "
                "(call-site structure) — _extract_and_persist_analysis( is "
                "called directly in the --probe block, bypassing the "
                "diagnosis (WR-A)",
                file=sys.stderr,
            )
            ok = False
        if "return probe_status" not in block:
            print(
                "self-test FAIL: persistence_write_guards control 12 "
                "(call-site structure) — the --probe block does not return "
                "the helper's status; a diagnosed failure would still exit 0",
                file=sys.stderr,
            )
            ok = False

    return ok


def _selftest_scoreline() -> bool:
    """D-15 item 3: strict D-12/D-13 terminal-block parsing.

    Two well-formed fixtures (one plain, one whose rationale prose above the
    block contains all four band-vocabulary names) must parse to the exact
    same (bands, verdict) pair — proving the parser reads only inside the
    delimited block and never scans the rationale (the `_composer_structure_
    hits` incidental-match failure mode this repo has already been bitten by,
    RR-77-08). Every other fixture in tests/quality-fixtures-v8.7/scoreline-
    blocks/ is a documented malformation and must record UNPARSEABLE, never a
    plausible-looking score. A D-13 no-retry proof closes the item: a
    malformed input must cause exactly one `parse_scoreline` invocation, and
    the caller must never re-invoke anything after UNPARSEABLE.
    """
    ok = True
    expected_bands = ["Rigorous", "Sound", "Rigorous", "Sound", "Sound", "Rigorous"]
    expected_verdict = "PASS"

    for well_formed_name in ("well-formed.txt", "well-formed-prose-mentions-bands.txt"):
        path = SCORELINE_BLOCKS_DIR / well_formed_name
        parsed = parse_scoreline(path.read_text(encoding="utf-8"))
        if parsed == UNPARSEABLE:
            print(
                f"self-test FAIL: scoreline well-formed fixture {well_formed_name!r} "
                "failed to parse",
                file=sys.stderr,
            )
            ok = False
            continue
        bands, verdict = parsed
        if bands != expected_bands or verdict != expected_verdict:
            print(
                f"self-test FAIL: scoreline well-formed fixture {well_formed_name!r} "
                f"parsed to unexpected bands/verdict: {bands!r}/{verdict!r}",
                file=sys.stderr,
            )
            ok = False

    malformed_names = (
        "five-criteria.txt",
        "seven-criteria.txt",
        "invalid-band-vocab.txt",
        "missing-verdict.txt",
        "extra-line-in-block.txt",
        "no-terminal-block.txt",
    )
    for malformed_name in malformed_names:
        path = SCORELINE_BLOCKS_DIR / malformed_name
        try:
            result = parse_scoreline(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001 — a relaxed/broken parser must
            # still be reported by name, never crash the self-test uncontrolled
            print(
                f"self-test FAIL: scoreline malformed fixture {malformed_name!r} "
                f"raised instead of recording UNPARSEABLE: {exc!r}",
                file=sys.stderr,
            )
            ok = False
            continue
        if result != UNPARSEABLE:
            print(
                f"self-test FAIL: scoreline malformed fixture {malformed_name!r} "
                f"did not record UNPARSEABLE — got {result!r} instead",
                file=sys.stderr,
            )
            ok = False

    # D-13 no-retry proof: exactly one parse_scoreline invocation for one
    # malformed input, and the caller (_build_scoreline_row) records
    # UNPARSEABLE across every field rather than a partial score.
    counter = {"n": 0}
    real_parse_scoreline = globals()["parse_scoreline"]

    def _counting_parse_scoreline(text: str):
        counter["n"] += 1
        return real_parse_scoreline(text)

    globals()["parse_scoreline"] = _counting_parse_scoreline
    try:
        row = _build_scoreline_row("d13-check", "no terminal block anywhere in this text")
    finally:
        globals()["parse_scoreline"] = real_parse_scoreline

    if counter["n"] != 1:
        print(
            f"self-test FAIL: scoreline D-13 no-retry check — parse_scoreline "
            f"was invoked {counter['n']} times for one malformed input, expected exactly 1",
            file=sys.stderr,
        )
        ok = False
    if row["bands"] != [UNPARSEABLE] * len(_CRITERIA) or row["judge_verdict"] != UNPARSEABLE:
        print(
            f"self-test FAIL: scoreline D-13 no-retry check — malformed row "
            f"did not fully record UNPARSEABLE: {row!r}",
            file=sys.stderr,
        )
        ok = False

    return ok


def check_blinding(analysis_text: str) -> list[str]:
    """D-15 item 4 body: build a judge packet and return a list of findings.

    An empty list means the packet is well-formed: it holds exactly the two
    expected files, has no repository-root ancestor, and — walking up the
    packet dir's own ancestor chain, the only relative-traversal surface
    reachable from a cwd of the packet dir without external knowledge of the
    repo's absolute path — never surfaces the committed blinding key or
    scoreline file by name or resolved path. The copied rubric must be
    byte-identical to its source, and `JUDGE_PROMPT` must carry none of the
    forbidden comparison-revealing substrings.

    Mirrors `check_baseline_integrity`'s findings-list shape rather than
    raising, so a caller (self-test or a future CLI surface) can report every
    defect found in one pass instead of stopping at the first one.
    """
    findings: list[str] = []

    try:
        packet_dir = build_judge_packet(analysis_text)
    except Exception as exc:  # noqa: BLE001 — never propagate; findings only
        findings.append(f"build_judge_packet raised: {exc!r}")
        return findings

    entries = sorted(p.name for p in packet_dir.iterdir())
    if entries != ["analysis.md", "validation-rubric.md"]:
        findings.append(f"packet dir {packet_dir} does not hold exactly the two expected files: {entries!r}")

    resolved = packet_dir.resolve()
    repo_root_resolved = REPO_ROOT.resolve()
    if resolved == repo_root_resolved or repo_root_resolved in resolved.parents:
        findings.append(f"packet dir {resolved} has the repository root as an ancestor")

    blinding_key = BASELINE_DIR / "blinding-key.tsv"
    scorelines_path = BASELINE_DIR / "scorelines.tsv"
    forbidden_names = {"blinding-key.tsv", "scorelines.tsv"}
    forbidden_resolved = {blinding_key.resolve(), scorelines_path.resolve()}

    probe = resolved
    for _ in range(12):
        try:
            entries_here = list(probe.iterdir())
        except (PermissionError, NotADirectoryError, FileNotFoundError):
            entries_here = []
        names_here = {p.name for p in entries_here}
        resolved_here = {p.resolve() for p in entries_here}
        if names_here & forbidden_names or resolved_here & forbidden_resolved:
            findings.append(
                f"the committed blinding key or scoreline file is reachable by "
                f"walking up from packet dir {resolved} to {probe}"
            )
            break
        if probe.parent == probe:
            break
        probe = probe.parent

    rubric_src = REPO_ROOT / "shared" / "spine" / "references" / "validation-rubric.md"
    if (packet_dir / "validation-rubric.md").read_bytes() != rubric_src.read_bytes():
        findings.append("copied rubric is not byte-identical to its source")

    if not _check_judge_prompt_unblinded():
        findings.append("JUDGE_PROMPT contains a forbidden comparison-leaking substring")

    return findings


def _selftest_blinding() -> bool:
    """D-15 item 4: D-05 blinding integrity (`check_blinding`), plus the D-14
    real-data cross-check.

    D-14 cross-check: `derive_pass_fail` over the six real frozen
    `tests/quality-baseline-v8.7/scorelines.tsv` rows agrees with all six
    judge-stated verdicts (hand-checked at plan time, 164-02-PLAN.md).
    A synthetic disagreement row proves the DISAGREE branch is reachable —
    without it, that branch would never fire and the item would be vacuous.
    """
    ok = True

    fixture_analysis = (
        "# Fixture analysis\n\nOffline fixture text for the blinding self-test.\n"
    )
    findings = check_blinding(fixture_analysis)
    if findings:
        print(
            f"self-test FAIL: blinding — check_blinding reported: {findings!r}",
            file=sys.stderr,
        )
        ok = False

    # D-14 cross-check over the six real frozen scorelines.
    scorelines_path = BASELINE_DIR / "scorelines.tsv"
    try:
        rows = read_scorelines(scorelines_path)
    except Exception as exc:  # noqa: BLE001
        print(
            f"self-test FAIL: blinding read_scorelines raised unexpectedly: {exc!r}",
            file=sys.stderr,
        )
        return False
    if len(rows) != 6:
        print(
            f"self-test FAIL: blinding expected 6 rows from {scorelines_path}, "
            f"got {len(rows)}",
            file=sys.stderr,
        )
        ok = False
    for row in rows:
        derived = derive_pass_fail(row["bands"])
        if derived != row["judge_verdict"]:
            print(
                f"self-test FAIL: blinding D-14 cross-check — row {row['id']!r} "
                f"derived {derived!r} but judge stated {row['judge_verdict']!r}",
                file=sys.stderr,
            )
            ok = False

    # Synthetic disagreement row: without this, the DISAGREE branch is
    # unreachable over the six real rows (which all agree) and this item
    # would be vacuous.
    disagree_bands = ["Rigorous"] * len(_CRITERIA)
    disagree_judge_verdict = "FAIL"
    disagree_derived = derive_pass_fail(disagree_bands)
    disagree_agreement = "AGREE" if disagree_derived == disagree_judge_verdict else "DISAGREE"
    if disagree_agreement != "DISAGREE":
        print(
            "self-test FAIL: blinding D-14 synthetic disagreement row did not "
            f"disagree (derived={disagree_derived!r}, judge stated="
            f"{disagree_judge_verdict!r})",
            file=sys.stderr,
        )
        ok = False

    return ok


def _selftest_tabulation() -> bool:
    """D-15 item 5: tabulation arithmetic, pinned to hand-checked values.

    Values below were hand-checked at plan time (164-02-PLAN.md) from
    `tests/quality-baseline-v8.7/scorelines.tsv` using the rubric's band
    weights (Rigorous=3, Sound=2, Hand-wavy=1, Absent=0), and independently
    re-verified against the real file during this task's implementation.
    The per-criterion sums must add back to the aggregate total, so a future
    edit cannot move one figure without moving the other (T-164-12).

    A synthetic seventh row carrying one UNPARSEABLE cell proves the
    denominator counts it (7, not 6) rather than silently excluding it —
    T-164-12's Repudiation mitigation.
    """
    ok = True
    try:
        rows = read_scorelines(BASELINE_DIR / "scorelines.tsv")
    except Exception as exc:  # noqa: BLE001
        print(
            f"self-test FAIL: tabulation read_scorelines raised unexpectedly: {exc!r}",
            file=sys.stderr,
        )
        return False

    summary = compute_tabulation_summary(rows)

    expected_per_row = [10, 12, 12, 13, 11, 12]
    if summary["per_row_totals"] != expected_per_row:
        print(
            f"self-test FAIL: tabulation per-row totals expected {expected_per_row!r}, "
            f"got {summary['per_row_totals']!r}",
            file=sys.stderr,
        )
        ok = False

    if summary["aggregate_band_total"] != 70:
        print(
            f"self-test FAIL: tabulation aggregate band total expected 70, "
            f"got {summary['aggregate_band_total']!r}",
            file=sys.stderr,
        )
        ok = False

    expected_per_criterion = [18, 9, 12, 8, 11, 12]
    if summary["per_criterion_sums"] != expected_per_criterion:
        print(
            f"self-test FAIL: tabulation per-criterion sums expected "
            f"{expected_per_criterion!r}, got {summary['per_criterion_sums']!r}",
            file=sys.stderr,
        )
        ok = False

    if sum(summary["per_criterion_sums"]) != summary["aggregate_band_total"]:
        print(
            "self-test FAIL: tabulation per-criterion sums do not add back to "
            "the aggregate band total",
            file=sys.stderr,
        )
        ok = False

    if (summary["pass_count"], summary["fail_count"]) != (4, 2):
        print(
            f"self-test FAIL: tabulation pass split expected (4, 2), got "
            f"{(summary['pass_count'], summary['fail_count'])!r}",
            file=sys.stderr,
        )
        ok = False

    mean_rounded = round(summary["mean"], 2)
    if mean_rounded != 11.67:
        print(
            f"self-test FAIL: tabulation mean expected 11.67, got {mean_rounded!r}",
            file=sys.stderr,
        )
        ok = False

    # Synthetic seventh row carrying an UNPARSEABLE cell (T-164-12): the
    # denominator must be seven, not six, and the aggregate band total must
    # stay 70 (the unparseable row contributes no numeric total but is never
    # dropped from the row-count denominator).
    synthetic_row = {
        "id": "synthetic-unparseable",
        "bands": ["Rigorous", "Sound", UNPARSEABLE, "Sound", "Sound", "Rigorous"],
        "judge_verdict": UNPARSEABLE,
    }
    summary_plus = compute_tabulation_summary(rows + [synthetic_row])
    if summary_plus["denominator"] != 7:
        print(
            f"self-test FAIL: tabulation denominator with the synthetic "
            f"UNPARSEABLE row expected 7, got {summary_plus['denominator']!r}",
            file=sys.stderr,
        )
        ok = False
    if summary_plus["unparseable_cell_count"] != 1:
        print(
            f"self-test FAIL: tabulation unparseable_cell_count expected 1, "
            f"got {summary_plus['unparseable_cell_count']!r}",
            file=sys.stderr,
        )
        ok = False
    if summary_plus["aggregate_band_total"] != 70:
        print(
            "self-test FAIL: tabulation aggregate band total changed when an "
            "UNPARSEABLE row was added — it must be excluded from the numeric "
            "sum while still counted in the denominator",
            file=sys.stderr,
        )
        ok = False

    return ok


def check_baseline_integrity(
    baseline_dir: Path | str,
    *,
    rejudge_source_dir: Path | str | None = None,
) -> list[str]:
    """D-15 item 6 body: structural integrity check for a frozen quality baseline.

    Returns a list of human-readable findings; an empty list means the
    baseline is present and well-formed. A non-empty list is a loud failure
    (T-164-12 discipline: never a silently-shorter comparison). Checks:
      1. `baseline_dir` exists and is a directory holding an `analyses/`
         subdirectory.
      2. Every `analyses/*.md` file is non-empty and larger than 2,000 bytes.
      3. `scorelines.tsv` exists and its data-row count equals the analysis
         file count; every row's band cells are drawn from the four-name
         vocabulary or the `UNPARSEABLE` sentinel.
      4. `blinding-key.tsv` exists and its row count equals the analysis file
         count; every row names an analysis file (by stem) that exists in
         `analyses/`.

    When `rejudge_source_dir` is given (Plan 04's regenerated baseline, whose
    D-02 re-judge arm scores the *frozen corpus*, not this directory's own
    `analyses/`), two more checks run:
      5. `rejudge-scorelines.tsv` exists and its data-row count equals this
         directory's own analysis file count (D-08 fixes both arms at the
         same cardinality — one re-judged scoreline per fresh-arm cell) and
         every row's bands are drawn from the same vocabulary.
      6. `rejudge-blinding-key.tsv` exists, its row count equals the analysis
         file count, and every row names a file (by stem) that exists in
         `rejudge_source_dir` — the frozen corpus this arm re-judged.
    """
    baseline_dir = Path(baseline_dir)
    findings: list[str] = []

    if not baseline_dir.is_dir():
        findings.append(f"{baseline_dir}: baseline directory does not exist")
        return findings

    analyses_dir = baseline_dir / "analyses"
    if not analyses_dir.is_dir():
        findings.append(f"{baseline_dir}: analyses/ subdirectory does not exist")
        return findings

    analysis_files = sorted(analyses_dir.glob("*.md"))
    analysis_stems = {p.stem for p in analysis_files}
    analysis_count = len(analysis_files)

    for p in analysis_files:
        size = p.stat().st_size
        if size == 0:
            findings.append(f"{p}: analysis file is empty")
        elif size <= 2000:
            findings.append(f"{p}: analysis file is only {size} bytes, expected > 2000")

    scorelines_path = baseline_dir / "scorelines.tsv"
    if not scorelines_path.is_file():
        findings.append(f"{scorelines_path}: does not exist")
    else:
        try:
            score_rows = read_scorelines(scorelines_path)
        except ValueError as exc:
            findings.append(f"{scorelines_path}: failed to parse — {exc}")
            score_rows = []
        if len(score_rows) != analysis_count:
            findings.append(
                f"{scorelines_path}: {len(score_rows)} data rows but "
                f"{analysis_count} analysis files in {analyses_dir} — counts must match"
            )
        for row in score_rows:
            for idx, band in enumerate(row["bands"]):
                if band not in _BAND_VOCAB and band != UNPARSEABLE:
                    findings.append(
                        f"{scorelines_path}: row {row['id']!r} column "
                        f"C{idx + 1} has band {band!r}, not in the four-name "
                        f"vocabulary or {UNPARSEABLE!r}"
                    )

    blinding_key_path = baseline_dir / "blinding-key.tsv"
    if not blinding_key_path.is_file():
        findings.append(f"{blinding_key_path}: does not exist")
    else:
        key_rows: list[tuple[str, str]] = []
        text = blinding_key_path.read_text(encoding="utf-8")
        for lineno, line in enumerate(text.splitlines(), start=1):
            if not line.strip():
                continue
            cells = line.split("\t")
            if len(cells) < 2:
                findings.append(
                    f"{blinding_key_path}:{lineno}: expected 2 tab-separated "
                    f"columns, got {len(cells)}"
                )
                continue
            key_rows.append((cells[0], cells[1]))
        if len(key_rows) != analysis_count:
            findings.append(
                f"{blinding_key_path}: {len(key_rows)} rows but "
                f"{analysis_count} analysis files in {analyses_dir} — counts must match"
            )
        for judge_id, stem in key_rows:
            if stem not in analysis_stems:
                findings.append(
                    f"{blinding_key_path}: row {judge_id!r} names analysis "
                    f"{stem!r}, which does not exist in {analyses_dir}"
                )

    if rejudge_source_dir is not None:
        rejudge_source_dir = Path(rejudge_source_dir)

        rejudge_scorelines_path = baseline_dir / "rejudge-scorelines.tsv"
        if not rejudge_scorelines_path.is_file():
            findings.append(f"{rejudge_scorelines_path}: does not exist")
        else:
            try:
                rejudge_rows = read_scorelines(rejudge_scorelines_path)
            except ValueError as exc:
                findings.append(f"{rejudge_scorelines_path}: failed to parse — {exc}")
                rejudge_rows = []
            if len(rejudge_rows) != analysis_count:
                findings.append(
                    f"{rejudge_scorelines_path}: {len(rejudge_rows)} data rows but "
                    f"{analysis_count} analysis files in {analyses_dir} — counts must match"
                )
            for row in rejudge_rows:
                for idx, band in enumerate(row["bands"]):
                    if band not in _BAND_VOCAB and band != UNPARSEABLE:
                        findings.append(
                            f"{rejudge_scorelines_path}: row {row['id']!r} column "
                            f"C{idx + 1} has band {band!r}, not in the four-name "
                            f"vocabulary or {UNPARSEABLE!r}"
                        )

        rejudge_key_path = baseline_dir / "rejudge-blinding-key.tsv"
        if not rejudge_key_path.is_file():
            findings.append(f"{rejudge_key_path}: does not exist")
        else:
            rejudge_source_stems = {p.stem for p in rejudge_source_dir.glob("*.md")}
            rejudge_key_rows: list[tuple[str, str]] = []
            rejudge_text = rejudge_key_path.read_text(encoding="utf-8")
            for lineno, line in enumerate(rejudge_text.splitlines(), start=1):
                if not line.strip():
                    continue
                cells = line.split("\t")
                if len(cells) < 2:
                    findings.append(
                        f"{rejudge_key_path}:{lineno}: expected 2 tab-separated "
                        f"columns, got {len(cells)}"
                    )
                    continue
                rejudge_key_rows.append((cells[0], cells[1]))
            if len(rejudge_key_rows) != analysis_count:
                findings.append(
                    f"{rejudge_key_path}: {len(rejudge_key_rows)} rows but "
                    f"{analysis_count} analysis files in {analyses_dir} — counts must match"
                )
            for judge_id, stem in rejudge_key_rows:
                if stem not in rejudge_source_stems:
                    findings.append(
                        f"{rejudge_key_path}: row {judge_id!r} names source "
                        f"{stem!r}, which does not exist in {rejudge_source_dir}"
                    )

    return findings


def _selftest_baseline() -> bool:
    """D-15 item 6: baseline-fixture integrity on all three real baselines and a negative.

    The real frozen `tests/quality-baseline-v8.7/` must report zero findings
    — it is present, complete, and well-formed. Plan 04's regenerated
    `tests/quality-baseline-v8.7-regenerated/` must also report zero
    findings, including its D-02 re-judge arm (`rejudge-scorelines.tsv` /
    `rejudge-blinding-key.tsv`) checked against `BASELINE_DIR`'s `analyses/`
    — the frozen corpus that arm re-judged. Phase 166 Plan 02 Task 3 extends
    this item a third time: the post-fix `tests/quality-baseline-v8.7-postfix/`
    must also report zero findings, including its own D-02 re-judge arm
    checked against `REGEN_DIR`'s `analyses/` — the frozen pre-fix analyses
    that arm re-judged same-day (not `POSTFIX_DIR`'s own analyses). The
    deliberately truncated `tests/quality-fixtures-v8.7/baseline-truncated/`
    (4 analyses, but the frozen corpus's original 6-row `scorelines.tsv` left
    in place) must report at least one finding naming the row-count-versus-
    file-count mismatch — a truncated or partially-committed baseline must
    fail loudly rather than produce a short comparison.
    """
    ok = True

    real_findings = check_baseline_integrity(BASELINE_DIR)
    if real_findings:
        print(
            f"self-test FAIL: baseline integrity on the real frozen baseline "
            f"({BASELINE_DIR}) found unexpected findings: {real_findings!r}",
            file=sys.stderr,
        )
        ok = False

    regen_findings = check_baseline_integrity(
        REGEN_DIR, rejudge_source_dir=BASELINE_DIR / "analyses"
    )
    if regen_findings:
        print(
            f"self-test FAIL: baseline integrity on the regenerated baseline "
            f"({REGEN_DIR}) found unexpected findings: {regen_findings!r}",
            file=sys.stderr,
        )
        ok = False

    postfix_findings = check_baseline_integrity(
        POSTFIX_DIR, rejudge_source_dir=REGEN_DIR / "analyses"
    )
    if postfix_findings:
        print(
            f"self-test FAIL: baseline integrity on the post-fix baseline "
            f"({POSTFIX_DIR}) found unexpected findings: {postfix_findings!r}",
            file=sys.stderr,
        )
        ok = False

    truncated_dir = FIXTURES_DIR / "baseline-truncated"
    truncated_findings = check_baseline_integrity(truncated_dir)
    if not truncated_findings:
        print(
            "self-test FAIL: baseline integrity on the deliberately truncated "
            "fixture found no findings — expected the row-count-versus-file-"
            "count mismatch to be reported",
            file=sys.stderr,
        )
        ok = False
    elif not any("data rows but" in f and "analysis files" in f for f in truncated_findings):
        print(
            f"self-test FAIL: baseline integrity on the truncated fixture "
            f"reported findings, but none names the count mismatch: "
            f"{truncated_findings!r}",
            file=sys.stderr,
        )
        ok = False

    return ok


# ---------------------------------------------------------------------------
# Mechanical defect detector (D-18/D-19/D-20/D-21)
#
# Parses each analysis structurally against the six numbered output-template
# sections and reports three defect families: untraced Conclusion claims
# (D-20, per-claim with a document-level rollup), non-conforming Verdict
# cells, and malformed Derivation Chains blocks. Every check below reads a
# located section slice; none scans the whole document — a whole-document
# keyword scan is the incidental-match failure mode this repo has already
# shipped once (RR-77-08, `_composer_structure_hits`).
# ---------------------------------------------------------------------------


class SectionResolutionError(ValueError):
    """Raised when fewer than six sections resolve, in order, in an analysis.

    A parser that silently fails to resolve a section and returns an empty
    slice would report zero defects for that family — a false-clean result
    (T-164-14). A document the parser cannot read must fail loudly instead.
    """


_SECTION_NAMES: dict[int, str] = {
    1: "problem essence",
    2: "assumptions table",
    3: "ground truths",
    4: "derivation chains",
    5: "abandoned reasoning",
    6: "conclusion",
}

# One to three hash characters, the section number with an optional trailing
# dot, then the section name from output-template.md, matched
# case-insensitively (the .lower() comparison below, not an inline flag,
# since the hashes/number half of the pattern is case-invariant already).
_SECTION_HEADING_RE = re.compile(
    r"^(?P<hashes>#{1,3})[ \t]+(?P<num>\d+)\.?[ \t]+(?P<name>.+?)[ \t]*$",
    re.MULTILINE,
)

# Defined here rather than beside its other consumer
# (`_conclusion_claims`, far below) purely for READING order: this is the
# first use in the file. Module globals resolve at call time, so the
# placement is not load-bearing — an earlier revision of this comment
# claimed it was, which was false, and also described the position
# backwards.
_FENCE_RE = re.compile(r"^\s*(?:```|~~~)")

# An ATX heading at any depth CommonMark recognises, including the up-to-
# three leading spaces it permits — four or more makes an indented code
# block, not a heading, which is why the bound is `{0,3}` and not `*`.
# Seven or more hashes is likewise not a heading, and the `[ \t]+` is what
# rejects it: `#{1,6}` can match only six of the seven, and the seventh is
# not a space or tab.
_APPENDIX_HEADING_RE = re.compile(r"^ {0,3}#{1,6}[ \t]+")

# A CommonMark fenced-code-block delimiter: up to three leading spaces, then
# three or more backticks or tildes, then the info string.
_FENCE_DELIM_RE = re.compile(r"^ {0,3}(?P<fence>`{3,}|~{3,})(?P<info>.*)$")


def _fenced_code_flags(lines: list[str]) -> list[bool]:
    """Per line: is it inside a fenced code block (delimiters included)?

    Implements CommonMark's actual closing rule rather than a parity toggle,
    because parity is wrong in three ways this file has already been bitten
    by. A fence closes only on the SAME character (``` cannot close ~~~, so a
    tilde block may quote an unclosed backtick example), at least as long as
    the opener, and carrying no info string of its own. A backtick opener may
    not have a backtick in its info string. An unterminated fence runs to end
    of input, which is what CommonMark specifies and also the safe reading.

    A parity toggle got this wrong on ordinary content — a ~~~ block quoting
    a ``` example inverted the state for the rest of the document.
    """
    inside = [False] * len(lines)
    open_char: str | None = None
    open_len = 0
    for i, raw in enumerate(lines):
        m = _FENCE_DELIM_RE.match(raw.rstrip("\r"))
        if open_char is None:
            if m is not None:
                char = m.group("fence")[0]
                if not (char == "`" and "`" in m.group("info")):
                    open_char, open_len = char, len(m.group("fence"))
                    inside[i] = True
            continue
        inside[i] = True
        if (
            m is not None
            and m.group("fence")[0] == open_char
            and len(m.group("fence")) >= open_len
            and not m.group("info").strip()
        ):
            open_char, open_len = None, 0
    return inside


def _slice_sections(text: str) -> dict[int, str]:
    """Locate the six numbered output-template sections; return num -> body text.

    Content before section 1 (preamble) is discarded. A section's body runs
    from its heading to the next resolved section heading, or — for section
    6 — to the first ATX heading of any depth (an appendix) that is not
    inside a fenced code block, capped independently at the Self-Audit
    Gate, or end of file.
    Raises `SectionResolutionError` if the six section numbers do not
    resolve, in ascending order, with no gaps — exactly the six shapes
    required, never a partial or out-of-order read.
    """
    candidates: list[tuple[int, int, re.Match]] = []
    for m in _SECTION_HEADING_RE.finditer(text):
        num = int(m.group("num"))
        expected = _SECTION_NAMES.get(num)
        if expected is not None and m.group("name").strip().lower() == expected:
            candidates.append((m.start(), num, m))

    anchors: list[tuple[int, int, int, re.Match]] = []  # (start, num, depth, match)
    seen: set[int] = set()
    for start, num, m in sorted(candidates, key=lambda c: c[0]):
        if num in seen:
            continue
        seen.add(num)
        anchors.append((start, num, len(m.group("hashes")), m))

    resolved_nums = [a[1] for a in anchors]
    if resolved_nums != [1, 2, 3, 4, 5, 6]:
        raise SectionResolutionError(
            f"expected sections 1-6 to resolve in order, resolved {resolved_nums!r}"
        )

    sections: dict[int, str] = {}
    for idx, (start, num, depth, m) in enumerate(anchors):
        body_start = m.end()
        if idx + 1 < len(anchors):
            body_end = anchors[idx + 1][0]
        else:
            # Section 6: stop at the next heading of ANY depth (an
            # appendix), else end of file.
            #
            # Plan 14-01 / D-02: the prior guard (`if len(hm.group(1)) <=
            # depth`) required the following heading to be at the same or
            # shallower hash depth before it counted as an appendix
            # boundary. Measured on the 2026-09-02 capture (`# 6.
            # Conclusion` followed by `## Assumption Audit scan (process
            # output)`): the `##` appendix heading is DEEPER than the `#`
            # section-6 heading, so the guard never fired and section 6's
            # body absorbed the Assumption Audit scan and the Self-Audit
            # Gate that follow it. The Gate's own `Quoted span:` lines then
            # became ledger rows discharging the claims the Gate was
            # grading, and `**Residual disclosed:**` — a Gate line —
            # became an 8th "section 6" claim. Removing the depth
            # comparison entirely (break at the FIRST heading match,
            # regardless of depth) fixes this: section 6 now means the
            # Conclusion section on an emission that uses `#` for sections
            # and `##` for process-output appendices. Measured cost
            # against the frozen v8.7 corpus: zero — all six analyses
            # carry no headings inside section 6, so their
            # `conclusion_claims`/`untraced_claims` readings are
            # byte-identical before and after (see control (i) in
            # `_selftest_ledger_traceability`). `_slice_sections` carries
            # no digest pin (only `_chain_block_well_formed` and
            # `_RENDER_RULE_LITERALS` do), so CONTRACT-06 is untouched.
            # Two corrections landed after the D-02 fix above, both
            # live-reproduced against `tests/quality-ledger-v8.26/PR-P1.md`
            # before being fixed (CR-01/CR-02, phase 14 review):
            #
            # CR-01: the scan used `#{1,3}`, so a depth-4-or-deeper heading
            # did not stop section 6 at all — the fix claimed "ANY depth"
            # while the pattern could not express it, and rewriting this
            # fixture's two `##` appendix headings to `####` restored the
            # exact pre-fix reading (7 claims -> 8, the 8th being
            # `**Residual disclosed:**`, a Self-Audit Gate line).
            # `_APPENDIX_HEADING_RE` spans the full 1-6 depth CommonMark
            # recognises, so the claim and the pattern now agree.
            #
            # CR-02: the scan had no fence tracking, so every `#`-shaped
            # line INSIDE a fenced block counted as an appendix boundary.
            # A single fenced `## ...` line in section 6 truncated the body
            # to nothing and collapsed the whole inventory to 0 claims / 0
            # fragments / 0 untraced with no error raised anywhere — a
            # false-clean, and reachable through the very shape R4
            # recommends (a heading-introduced closure ledger).
            # `_conclusion_claims` now shares `_fenced_code_flags` with this
            # walk, so the two cannot disagree about where a line starts or
            # what counts as fenced — they did disagree while one used
            # `splitlines()` and the other `re.MULTILINE`.
            # Section 6 ends at the first ATX heading that is not inside
            # a fenced code block — and, independently of any fence
            # reasoning at all, never later than the Self-Audit Gate.
            #
            # The second condition is not redundant, and the history here is
            # the argument for it. Three successive fence rules were tried
            # and each was defeated by ordinary content:
            #
            #   * No fence tracking: a `## ...` line inside a fenced closure
            #     ledger truncated section 6 to nothing, reading 0/0/0 —
            #     a silent false-clean (CR-02).
            #   * Parity toggle: a balanced fence opening in section 6 and
            #     closing after the appendix headings hid both, so section 6
            #     absorbed the Self-Audit Gate and `**Residual disclosed:**`
            #     returned as an 8th claim — the D-02 defect, restored by
            #     its own fix.
            #   * "Hidden only if the fence closes before the next heading":
            #     a fenced block containing TWO heading-shaped lines (a bash
            #     snippet with two `# ` comments is enough) made the second
            #     one the "next heading", so nothing was hidden and the
            #     reading collapsed to 0/0/0 again.
            #
            # `fence / ## a / ## b / fence` is the same token shape whether
            # it is a legitimate two-line fenced ledger or a fence swallowing
            # two appendix headings, so NO rule reading fence and heading
            # positions alone can separate them. The fence scan is therefore
            # made correct (real CommonMark closing rules, not parity) and
            # then backstopped by a signal that does not depend on fences:
            # `_SELFAUDIT_CRITERION_RE` locates the Gate's own verdict blocks
            # in the whole analysis text, exactly as
            # `_selfaudit_calibration_defects` does. Whatever a fence does,
            # section 6 stops at or before the Gate.
            #
            # DISCLOSED BOUND: the cap can only fire on an emission that
            # actually renders `**Criterion N: ...**` blocks. An emission
            # with no Self-Audit Gate at all has no Gate to absorb, so the
            # fence scan alone governs, and an unterminated fence there
            # leaves section 6 running to end of file.
            #
            # Lines are split on "\n" alone, matching the `re.MULTILINE`
            # semantics of the `re.finditer` scan this replaced.
            # `str.splitlines()` also splits on `\x0b`, `\x0c`, `\x1c`-`\x1e`,
            # `\x85`, `\u2028` and `\u2029`, so a bare form feed created a
            # phantom line whose tail could match as a heading.
            lines = text[body_start:].split("\n")
            fenced = _fenced_code_flags(lines)

            body_end = len(text)
            offset = body_start
            for idx, raw_line in enumerate(lines):
                if not fenced[idx] and _APPENDIX_HEADING_RE.match(raw_line):
                    body_end = offset
                    break
                offset += len(raw_line) + 1

            gate = _SELFAUDIT_CRITERION_RE.search(text, body_start)
            if gate is not None:
                body_end = min(body_end, gate.start())
        sections[num] = text[body_start:body_end]
    return sections


def _verdict_cells(section2: str) -> list[str]:
    """Locate the assumption table's Verdict column by header name and return its cells.

    Uses the hardened row splitter (`_split_row`/`_is_separator_row`) rather
    than a bare pipe-split. The column index comes from the header alone,
    never a constant — the frozen corpus contains both five-column and
    six-column assumption tables with the Verdict column in different
    positions.
    """
    lines = section2.splitlines()
    header_idx: int | None = None
    verdict_col: int | None = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = _split_row(stripped)
        if _is_separator_row(cells):
            continue
        for j, c in enumerate(cells):
            if c.strip().lower() == "verdict":
                header_idx = i
                verdict_col = j
                break
        if header_idx is not None:
            break

    if header_idx is None or verdict_col is None:
        return []

    out: list[str] = []
    i = header_idx + 1
    if i < len(lines):
        sep_cells = _split_row(lines[i].strip())
        if _is_separator_row(sep_cells):
            i += 1
    while i < len(lines):
        stripped = lines[i].strip()
        if not stripped.startswith("|"):
            break
        cells = _split_row(stripped)
        if verdict_col < len(cells):
            out.append(cells[verdict_col])
        i += 1
    return out


# Deterministic order (a tuple, not a set — regex alternation order must
# stay stable regardless of PYTHONHASHSEED / hash randomization) of the
# three vocabulary tokens a Verdict cell's leading word may be.
_VERDICT_VOCAB = ("accept", "challenge", "discard")

# DETECT-02 (P183-D1/P183-D2, Phase 183): the Verdict cell contract is a
# leading vocabulary token, optionally wrapped in `*`/`_` emphasis, followed
# by U+2014 EM DASH and at least one non-whitespace justification character.
#
# Separator policy (P183-D1): U+2014 EM DASH is the ONLY accepted separator.
# U+2013 EN DASH and U+002D HYPHEN-MINUS are rejected. Both
# `output-template.md`'s Verdict Vocabulary bullet and
# `validation-rubric.md` Criterion 2's Rigorous descriptor name only
# "em-dash"; a codepoint dump of `output-template.md` lines 69-71 confirms
# all six separator occurrences there are U+2014; and a 267-cell census
# across all four frozen analysis corpora found zero en-dash and zero
# ASCII-hyphen separators in use, so this strict reading moves no recorded
# figure either way — it is a forward-looking documentation choice, not a
# retroactive correction.
#
# Empty-justification policy (P183-D2): a cell carrying the token and the
# separator but no non-whitespace character after it does not conform.
# Criterion 1 requires a "non-empty justification" and the rubric requires
# "a specific justification" — an empty remainder carries no reasoning,
# which is the whole purpose of the em-dash clause.
#
# The literal separator is written as the \u2014 escape below, never the
# raw glyph, so the character is unambiguous in a diff.
_VERDICT_FORM_RE = re.compile(
    r"^[*_]*\s*(" + "|".join(_VERDICT_VOCAB) + r")\s*[*_]*\s*\u2014\s*(.*)$",
    re.IGNORECASE,
)


def _verdict_conforms(cell: str) -> bool:
    """Whether a Verdict cell is the token-prefix + em-dash + justification
    form `output-template.md` and `validation-rubric.md` Criterion 2
    prescribe, rather than the bare vocabulary token alone.

    This function was previously inverted: an earlier implementation
    accepted the bare token alone and rejected the prescribed em-dash form —
    the exact opposite of what both canonical sources require. The
    correction (DETECT-02, Phase 183) is deliberately strict: only U+2014 EM
    DASH separates the token from the justification (see the comment above
    `_VERDICT_FORM_RE` for the separator and empty-justification policy and
    its rationale), and punctuation between the token and the separator (the
    old implementation's `rstrip(".,;:!")` behaviour) is not carried
    forward — a cell reading `Accept.` with no em-dash still does not
    conform.
    """
    m = _VERDICT_FORM_RE.match(cell.strip())
    if not m:
        return False
    return bool(m.group(2).strip())


# Chain-label families the frozen corpus actually uses: a two-letter prefix
# followed by a hyphen and a number (DC-1), the word "Chain" OR "Conclusion"
# followed by a letter or a number (Chain A, Chain 1, Conclusion C1 — the
# last being the form output-template.md §4 prescribes; see GAP-5 in
# `_selftest_gap5_conclusion_heading`), and — FIX-CONTRACT-01 limitation 1
# — a document's own bare single-letter convention (C1, A, E5: one
# uppercase letter optionally followed by digits) when used consistently as
# a §4 lead-in family (see _MIN_BARE_LABEL_FAMILY_SIZE below). The bare form
# is listed last in the alternation so the two more specific forms above it
# always win when they also match (e.g. "Chain A" matches the "Chain "
# alternative and never falls through to the bare one).
_CHAIN_LABEL_PATTERN = r"(?:[A-Z]{2}-\d+|(?:Chain|Conclusion)\s+[A-Za-z0-9]+)"
_CHAIN_LABEL_PATTERN_BARE = r"[A-Z]\d*"
_CHAIN_LABEL_PATTERN_ANY = r"(?:" + _CHAIN_LABEL_PATTERN + r"|" + _CHAIN_LABEL_PATTERN_BARE + r")"

# A bare single-letter label is only accepted as a chain-label family when
# it is used consistently (repeated/sequenced) as a §4 lead-in — a lone
# incidental bold lead-in that happens to match the bare shape (e.g. a
# single "**A/B test:**") must not be mistaken for a one-chain family. Two
# is the minimum "used consistently" reading: a single hit is definitionally
# not a repeated convention.
_MIN_BARE_LABEL_FAMILY_SIZE = 2
_BARE_LABEL_ONLY_RE = re.compile(r"^" + _CHAIN_LABEL_PATTERN_BARE + r"$")

# Headed form: a heading line whose text begins with the label followed by a
# separator (colon, em dash, en dash, or hyphen).
_CHAIN_HEADING_RE = re.compile(
    r"^#{1,6}[ \t]*(?P<label>" + _CHAIN_LABEL_PATTERN_ANY + r")[ \t]*[:—–-]",
    re.MULTILINE,
)
# Bolded lead-in form: a line beginning with bold markers whose text begins
# with the label (no heading hashes).
_CHAIN_BOLD_RE = re.compile(
    r"^\*\*(?P<label>" + _CHAIN_LABEL_PATTERN_ANY + r")\b[^\n]*?\*\*",
    re.MULTILINE,
)


def _iter_chain_id_matches(section4: str) -> list[re.Match]:
    matches = list(_CHAIN_HEADING_RE.finditer(section4)) + list(
        _CHAIN_BOLD_RE.finditer(section4)
    )
    matches.sort(key=lambda m: m.start())
    # FIX-CONTRACT-01 limitation 1's family guard: a bare single-letter
    # label only counts when the document uses it >= _MIN_BARE_LABEL_
    # FAMILY_SIZE times. The two-letter-hyphen and "Chain "-prefixed forms
    # are already specific enough that they need no such guard.
    bare_matches = [m for m in matches if _BARE_LABEL_ONLY_RE.match(m.group("label"))]
    if 0 < len(bare_matches) < _MIN_BARE_LABEL_FAMILY_SIZE:
        excluded_ids = {id(m) for m in bare_matches}
        matches = [m for m in matches if id(m) not in excluded_ids]
    return matches


def _chain_ids(section4: str) -> list[str]:
    """Return the chain identifiers present in section 4, in document order, deduplicated."""
    ids: list[str] = []
    for m in _iter_chain_id_matches(section4):
        label = m.group("label")
        if label not in ids:
            ids.append(label)
    return ids


def _chain_blocks(section4: str) -> list[str]:
    """Return the text belonging to each chain identifier.

    When no identifier is found, returns the whole section as a single
    block rather than an empty list, so a chains-without-labels document
    reports one block, not zero.
    """
    matches = _iter_chain_id_matches(section4)
    if not matches:
        return [section4]
    blocks: list[str] = []
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(section4)
        blocks.append(section4[start:end])
    return blocks


# Prescribed chain form (output-template.md § 4): one or more GT identifiers
# (optionally `?`-suffixed for an unverified ground truth, optionally
# followed by a parenthetical label), joined by `+`, then an arrow,
# non-empty intermediate text, a second arrow, and non-empty conclusion
# text. Both the unicode rightwards arrow and the two-character ASCII arrow
# are accepted. Phase 184 (DETECT-03) corrected the match from per-physical-
# line to block-level: the form is now matched across a whole chain block,
# joining a GT-head line with the arrow-led lines that follow it, because
# the template's own canonical worked example (the `### Conclusion C1:`
# block, lines 133-137) spans three physical lines and the earlier
# per-line reading rejected it outright. D-02 asymmetry, stated explicitly:
# `_GT_MENTION_RE` below is the deliberately un-widened sibling of the GT
# token here — it stays digit-only (`GT-\d+\??`) because it is
# DETECT-04/untraced-claims-owned, not DETECT-03-owned, and this widening
# must not reach it. D-04 accepted cost: because the GT token below now
# accepts any alphanumeric identifier rather than digits only, a real
# analysis that leaks unfilled template placeholders (`GT-N`, `GT-M`) now
# scores clean on this chain axis, and no other check in this file covers
# that gap — accepted because this predicate checks chain SHAPE, not
# identifier vocabulary.
_ARROW = r"(?:→|->)"
_GT_TOKEN_WIDE = r"GT-[A-Za-z0-9]+\??"

# GAP-6: a chain head may cite a prior CONCLUSION alongside (or instead of)
# ground truths — `GT-5 (label) + C6 (label) -> ... -> ...`. Before this,
# `_CHAIN_FORM_LINE_RE` accepted GT-only heads, so every composing chain
# scored malformed however well-formed its arrows were. Two shapes the
# output template itself produces are compositions: the trade-off matrix
# collapse, whose criteria rest on earlier conclusions, and the
# second-order order-marked extension.
#
# GT-only heads were acyclic by construction — a ground truth is an axiom
# and cannot depend on a chain. Admitting chain refs admits cycles (C1
# citing C2 citing C1) and chains that never reach a ground truth at all,
# neither of which any shape-level predicate can see. That is why this
# widening ships WITH `_chain_dependency_defects` below rather than alone:
# without it the change trades a false positive (composition scored
# malformed) for a false negative (circular reasoning scored clean), and
# circular reasoning is the more serious defect — the validation rubric
# names it an abandonment reason in its own right.
_CHAIN_REF_TOKEN = r"C\d+"
_CHAIN_HEAD_TOKEN = r"(?:" + _GT_TOKEN_WIDE + r"|" + _CHAIN_REF_TOKEN + r")"
_CHAIN_FORM_LINE_RE = re.compile(
    _CHAIN_HEAD_TOKEN + r"(?:[ \t]*\([^)\n]*\))?"
    r"(?:[ \t]*\+[ \t]*" + _CHAIN_HEAD_TOKEN + r"(?:[ \t]*\([^)\n]*\))?)*"
    r"[ \t]*" + _ARROW + r"[ \t]*\S[^\n]*?"
    r"[ \t]*" + _ARROW + r"[ \t]*\S[^\n]*"
)

# GT-head candidate test for the bounded block-level join (D-06): matches
# any line carrying a GT token, using the same widened token as
# _CHAIN_FORM_LINE_RE above. A separate symbol from _CHAIN_FORM_LINE_RE and
# _GT_MENTION_RE — this one is used with `.search` against a single
# stripped line to test candidacy, not to match a whole chain form.
#
# Deliberately UNANCHORED (Phase 184-04, reverting the Phase 184-03 `^`
# anchor). The anchor added a precondition — "the stripped line must
# BEGIN with a bare GT- token" — that never existed before Phase 184-03,
# and it is the SOLE cause of that revision's regression, measured against
# the pre-phase base `1f71211` in `184-04-PLAN.md` M-1/M-2: it rejected
# `shared/spine/references/output-template.md`'s own canonical `Example:`
# lines, every backtick/bold/blockquote/list-item/prose-embedded rendering
# the frozen corpus actually uses, and moved `malformed_chain_blocks` from
# `[2, 2, 2, 2, 3, 3]` to `[5, 2, 3, 3, 3, 5]` — seven false positives —
# while being pinned by ZERO of the 20 contract fixtures on file at the
# time (`184-VERIFICATION.md`, `184-REVIEW.md` CR-01/WR-02). The anchor's
# own stated rationale — an unanchored search matching a GT- token inside
# a prose sentence, e.g. "As discussed, GT-1 was already covered above." —
# does not reproduce: that prose-head probe measures False at the
# pre-phase base, at every intermediate revision, and under every
# candidate rule considered in `184-04-PLAN.md` M-2, because
# `_CHAIN_FORM_LINE_RE` already requires the arrow to follow the GT token
# (and its optional parenthetical) directly, so a bare mid-sentence
# mention can never complete a two-arrow match on its own. Candidacy stays
# unanchored because a well-formed chain legitimately sits inside
# backticks, bold spans, blockquotes, list items, numbered items and
# prose. INJ-1 (`184-04-PLAN.md` M-4) is the injection that now pins this
# reversion: re-anchoring flips six named fixtures (`C-RENDER-BACKTICK`,
# `C-RENDER-BLOCKQUOTE-BOLD`, `C-RENDER-EXAMPLE-PREFIX`,
# `C-RENDER-LIST-ITEM`, `C-RENDER-SECONDORDER-PREFIX`, `C-WRAP-BULLETED`)
# plus the `_CALIBRATION_MALFORMED_CHAIN_BLOCKS` self-test assertion.
# Widened with `_CHAIN_HEAD_TOKEN` (GAP-6) so a chain-headed composition
# line is a candidate at all. Measured against the frozen corpus before
# and after: `_CALIBRATION_MALFORMED_CHAIN_BLOCKS` stays [2, 2, 2, 2, 3,
# 3] under both this widening and the narrower "+ continuation only"
# variant, so neither introduces a false positive there.
_GT_HEAD_RE = re.compile(_CHAIN_HEAD_TOKEN)
# Readable alias for GAP-6 call sites that test head candidacy rather
# than GT presence; same compiled pattern, clearer at the use site.
_CHAIN_HEAD_TOKEN_RE = _GT_HEAD_RE

# Bounded-join continuation test (D-06): a stripped line continues the
# current candidate segment only while it itself begins with an arrow. A
# separate symbol from _ARROW (which it wraps) and from
# _CHAIN_FORM_LINE_RE — this one is anchored to the start of an
# already-stripped line.
_LEADING_ARROW_RE = re.compile(r"^" + _ARROW)

# Three named continuation-refusal regexes (Phase 184-04), replacing the
# Phase 184-03 head-arrow guard that `184-REVIEW.md` CR-03 and
# `184-VERIFICATION.md` gap 1 showed keyed on WHERE the line break fell
# rather than on whether the absorbed line is relevant to the SAME claim:
# moving a malformed chain's first arrow onto its own line defeated the
# old guard while leaving the malformation unchanged. Each regex below is
# evaluated against a continuation line already known to be arrow-led
# (`_LEADING_ARROW_RE` has matched); any one of the three refusing the
# line is the join's boundary, exactly like an unmatched
# `_LEADING_ARROW_RE`.

# A continuation line that itself LEADS WITH a GT identifier — optionally
# behind a bracketed order mark (`[2nd]`, `[3rd]`) with no intervening
# space, the template's own second-order extension form — is the head of
# a NEW claim, not a wrap of the current one. Deliberately "leads with",
# not "contains": a contains-test was measured and rejected
# (`184-04-PLAN.md` M-2 candidate C) because the template's own
# `C-TEMPLATE-C1` intermediate placeholder — "→ [intermediate claim — a
# new inference statable from combining GT-N and GT-M but from neither
# alone]" — CONTAINS `GT-N`/`GT-M` mid-line without being a new claim; a
# leads-with test accepts it while a contains test rejects the template's
# own canonical example. Pins `C-JOIN-ARROW-NEWGT` and
# `C-JOIN-ARROW-NEWGT-WRAPPED` (INJ-3); the optional order-mark bracket
# group is separately pinned by `C-JOIN-ORDERMARK-NEWGT` (INJ-5), which
# fires when the bracket group alone is removed.
_ARROW_LED_GT_RE = re.compile(
    r"^" + _ARROW + r"(?:\[[^\]\n]*\])?[ \t]*" + _GT_TOKEN_WIDE
)

# A continuation line that is a markdown table row is not a chain segment,
# regardless of its leading arrow. Pins `C-JOIN-ARROW-TABLEROW` and
# `C-JOIN-ARROW-TABLEROW-WRAPPED` (INJ-4).
_ARROW_LED_TABLE_ROW_RE = re.compile(r"^" + _ARROW + r"[ \t]*\|")

# A segment (the head line, or the last absorbed continuation) that has
# already closed its sentence has finished its claim, so a FOLLOWING
# arrow-led line starts a new statement rather than continuing this one.
# Tested at end-of-string against the already-stripped segment text and
# tracked across iterations, seeded from the head line: the head-level
# check is what closes CE1 (`C-JOIN-ARROW-BULLET`) and the
# continuation-level check is what closes R1
# (`C-JOIN-ARROW-BULLET-WRAPPED`) — both are required (measured,
# `184-04-PLAN.md` M-2). Defined as its own DETECT-03-owned symbol rather
# than reusing the equivalent inline pattern inside `_is_assertive_claim`
# — that pattern is FIX-CONTRACT-01-owned, and this phase keeps the two
# requirements' owned symbols separate. Pins `C-JOIN-ARROW-BULLET` and
# `C-JOIN-ARROW-BULLET-WRAPPED` (INJ-2).
_SEGMENT_SENTENCE_END_RE = re.compile(r"[.!?][\"'’”]*$")

# Markdown emphasis/code closers that may legitimately trail a sentence's
# terminal punctuation in this project's own corpus (`**bold.**`,
# `` `code.` ``, `*em.*`, `__strong.__`, `~~strike.~~`). Stripped before
# the sentence-end test — see `_segment_sentence_closed`.
_MD_TRAILING_CLOSER_RE = re.compile(r"(?:\*\*|__|[*_`~])+$")

# A GT identifier carries its OWN optional `?` (the unverified marker,
# `GT-5?`). That `?` is not sentence-terminal punctuation, but is
# indistinguishable from it at end-of-string. Masked before the
# sentence-end test — see `_segment_sentence_closed`. Same pattern as
# `_GT_HEAD_RE`, kept as its own named symbol because the two have
# distinct purposes (candidacy vs. normalisation).
_GT_TOKEN_MASK_RE = re.compile(_GT_TOKEN_WIDE)


def _segment_sentence_closed(seg: str) -> bool:
    """Has this segment finished its claim? Normalise, THEN test (D-20).

    Phase 184-06. `_SEGMENT_SENTENCE_END_RE` alone tests RAW rendered
    markdown, which made the refusal evadable in two opposite directions —
    both found by this phase's own code review AFTER every gate was green,
    because no fixture exercised either shape:

    - OVER-acceptance (`184-REVIEW.md` CR-01, pinned by
      `C-JOIN-ARROW-BOLDCLOSE`): a finished one-hop claim wearing a
      markdown closer (`**GT-1 → conclusion is finished here.**`) did not
      read as sentence-closed, so an unrelated following arrow-led line
      fused into a fake two-hop chain and scored well-formed. This is the
      blanket-pass class ROADMAP criterion 3 names by name.
    - UNDER-acceptance (`184-REVIEW.md` CR-02, pinned by
      `C-WRAP-GT-QMARK`): a legitimate wrapped chain whose head ends in a
      GT token's own unverified marker (`GT-2 + GT-5?`) read as
      sentence-closed on that `?`, so its real continuations were refused.

    Both are one root: the test ran on raw text without normalising
    decoration or tokenising GT markers first. Fixing the LAYERING —
    mask GT tokens, strip trailing markdown closers, then apply the
    unchanged `_SEGMENT_SENTENCE_END_RE` — closes both and, measured
    against the full grid, moves nothing else: all 32 contract fixtures
    still agree, the six-analysis corpus vector stays
    `[2, 2, 2, 2, 3, 3]`, and the template's own `Example:` lines stay
    True.

    ACCEPTED LIMITATION (D-21, honesty-not-score D-01). This does NOT
    close ROADMAP criterion 3 as a class, and Phase 184 stops here by
    decision rather than by exhaustion. Criterion 3 is an unbounded
    negative ("the matcher does not become a blanket pass") verified by a
    finite fixture table; finite examples cannot discharge a universal
    claim. Three rounds each closed the shape then known and each was
    defeated by a shape outside the table — line-break position (184-03),
    reformatted first arrow (184-04), markdown-decorated sentence close
    (184-06) — with every CI gate green throughout, because the gates
    assert only the table. Closing the class would require a GENERATOR
    (property-based testing over a grammar of renderings: bold x backtick
    x blockquote x list x table x order mark x arrow position x sentence
    closer), not more fixtures. That is deliberately not built. Treat a
    green chain axis as "no KNOWN shape regresses", never as "no shape
    passes".
    """
    text = _GT_TOKEN_MASK_RE.sub("\x01", seg).rstrip()
    previous = None
    while previous != text:
        previous = text
        text = _MD_TRAILING_CLOSER_RE.sub("", text).rstrip()
    return bool(_SEGMENT_SENTENCE_END_RE.search(text))


def _chain_block_well_formed(block: str) -> bool:
    """Match the prescribed chain form across a block (D-05, D-06).

    Tries every line carrying a GT head as a candidate chain start. The
    stripped head line seeds the candidate segment, and the head's own
    sentence-closed state (see `_SEGMENT_SENTENCE_END_RE` below) is
    tracked from that first line onward. A following stripped line is
    absorbed into the candidate only while ALL of these hold: the line
    begins with an arrow (`_LEADING_ARROW_RE`, D-06's necessary
    condition — a line that is not arrow-led is always the boundary); the
    previously accepted segment (the head, or the last absorbed
    continuation) had not already closed its sentence; the line does not
    itself lead with a GT identifier (`_ARROW_LED_GT_RE`); the line is
    not a markdown table row (`_ARROW_LED_TABLE_ROW_RE`). The first line
    that fails any of these is the boundary. The bounded, space-joined
    candidate is matched against the same `_CHAIN_FORM_LINE_RE` used
    before this phase — the regex stays load-bearing, only the caller
    changed, so a one-line block still joins to itself and matches
    (criterion 4 preserved by construction).

    No arrow-count cap is applied to the head line or to the joined
    candidate. A cap was measured in both directions (`184-04-PLAN.md`
    M-2, candidate F-full and the two cap-removal injections in its
    fault-injection matrix) and found behaviourally inert — both
    injections flip zero fixtures — so it is not implemented: shipping a
    rule no fixture can observe is the defect this phase exists to close.

    Phase 184-04 correction (closing `184-VERIFICATION.md` gap-closure
    items (a)-(d), reversing the `37fea87` regression that shipped BELOW
    the pre-phase base `1f71211`): two independent defects in the prior
    revision are both fixed here.

    First, `_GT_HEAD_RE`'s line-start `^` anchor is reverted — see that
    symbol's own comment for the measured cause-and-effect. Candidacy is
    unanchored again, so a chain sitting inside backticks, bold spans,
    blockquotes, list items, numbered items or prose is recognised, as it
    was before Phase 184-03.

    Second, the prior revision's head-arrow guard — which refused
    absorption only when the HEAD line already carried an arrow anywhere
    — keyed on WHERE the line break fell, not on whether the absorbed
    line continues the SAME claim: moving a malformed one-hop chain's
    first arrow onto its own line defeated the guard while the
    malformation stayed identical (`184-REVIEW.md` CR-03,
    `184-VERIFICATION.md` gap 1). It is replaced here with the three
    named, relevance-based continuation refusals defined above
    (`_ARROW_LED_GT_RE`, `_ARROW_LED_TABLE_ROW_RE`,
    `_SEGMENT_SENTENCE_END_RE`), evaluated at every continuation step
    rather than once against the head. Each refusal is proven
    load-bearing by its own fault injection under both `python3` and
    `python3 -O` (`184-04-PLAN.md` M-4): INJ-1 (the anchor reversion
    above), INJ-2 (sentence-closed), INJ-3 (arrow-led-GT), INJ-4
    (table-row), INJ-5 (the arrow-led-GT rule's optional order-mark
    bracket), INJ-6 (restoring the retired head-arrow guard).

    Measured limitations, stated honestly rather than tuned away (M-3):
    this rule set fails exactly three probes, and NONE is a regression
    against the pre-phase base `1f71211` — all three are already False
    there. RISK-A (a wrapped chain whose intermediate closes its own
    sentence before the second arrow) is structurally INDISTINGUISHABLE
    from the pinned negative `C-JOIN-ARROW-BULLET`: both are a GT head,
    one arrow, a sentence-terminating period, then an arrow-led line —
    they differ only in what the words MEAN, which no shape-based rule
    can read, so this phase rejects both and records the false negative
    rather than relaxing the sentence-closed refusal `C-JOIN-ARROW-BULLET`
    requires. RISK-B (the head closes its sentence BEFORE its first
    arrow) and RISK-C (a blockquote whose continuation lines keep their
    `>` prefix after stripping, so `_LEADING_ARROW_RE` never matches them)
    are both pre-existing limitations, constant across every revision and
    every candidate rule measured in `184-04-PLAN.md` M-2/M-3 — neither is
    introduced or worsened here.

    Phase 184-06 correction and STOP decision. The residual list above was
    incomplete when written: this phase's own code review, run AFTER
    184-04 and 184-05 committed and after every gate was green, found two
    further live shapes — `184-REVIEW.md` CR-01 (over-acceptance, a
    REGRESSION against the pre-phase base) and CR-02 (under-acceptance,
    not a base regression but undisclosed). Both had one root — the
    sentence-close test ran on raw rendered markdown — and both are closed
    by `_segment_sentence_closed` above and pinned by
    `C-JOIN-ARROW-BOLDCLOSE` and `C-WRAP-GT-QMARK`.

    ROADMAP criterion 3 is NOT closed as a class and is recorded as an
    ACCEPTED LIMITATION rather than pursued further (D-21; see
    `_segment_sentence_closed` for the full statement, and
    `docs/requirements-traceability.md` for the tracked disposition).
    Three rounds each closed the then-known shape and were each defeated
    by a shape outside the fixture table; a finite table cannot discharge
    an unbounded negative. Known shapes are pinned; the class stays open
    by decision.

    Deferred, out of this phase's scope (WR-03): this function's `any()`
    semantic over candidates, combined with `_chain_blocks`'s
    whole-section fallback for an un-headered block, means one matching
    candidate anywhere in the block suppresses detection of every other
    malformed fragment in that same block. Pre-dates this phase; both the
    code reviewer and the verifier scoped it out of Phase 184. Not
    changed here.
    """
    lines = block.splitlines()
    for i, ln in enumerate(lines):
        head = ln.strip()
        if not _GT_HEAD_RE.search(head):
            continue
        seg = [head]
        segment_closed = _segment_sentence_closed(head)
        for nxt in lines[i + 1 :]:
            s = nxt.strip()
            if not _LEADING_ARROW_RE.match(s):
                break
            if segment_closed:
                break
            if _ARROW_LED_GT_RE.match(s):
                break
            if _ARROW_LED_TABLE_ROW_RE.match(s):
                break
            seg.append(s)
            segment_closed = _segment_sentence_closed(s)
        if _CHAIN_FORM_LINE_RE.search(" ".join(seg)):
            return True
    return False


def _chain_detector_source() -> str:
    """The single call site naming the frozen `_chain_block_well_formed`.

    Exists so nothing else in this module — including the pin below and its
    self-test controls — has to call `inspect.getsource()` against the
    function directly; there is exactly one place that names it for hashing.
    """
    return inspect.getsource(_chain_block_well_formed)


# A `sha256:<hex>` pin over `_chain_block_well_formed`'s own source bytes
# (Phase 13, CHAINHEAD-07) — a DIFFERENT mechanism from the
# `_RENDER_RULE_LITERALS` digest pin above: that pin hashes a dict of prose
# strings, this one hashes a function's `inspect.getsource()`.
#
# `.rstrip("\n")` is applied because `inspect.getsource()` always returns
# source text ending in exactly one trailing newline; hashing it un-stripped
# yields a DIFFERENT digest than the one already recorded by hand in
# `.planning/STATE.md` and `.planning/PROJECT.md` as this function's
# v8.24.0-identical blob. A future reader who "simplifies" the strip away
# silently changes the pinned value against three already-committed
# documents — do not remove it.
#
# Recompute discipline: a diff to this literal must always accompany a
# WRITTEN AMENDMENT to the milestone goal, landed FIRST, per STATE.md's
# standing pre-commitment that changing `_chain_block_well_formed` requires
# that amendment before any recompute. Never the reverse order.
#
# Phase 13's own rationale for adding this pin now, not earlier or later: R7
# and R8 (`_RENDER_RULE_LITERALS`, above) now state on four canonical
# surfaces the exact grammar this function has enforced since GAP-6 — this
# pin freezes an implementation whose contract is, for the first time,
# written down. That rationale lives HERE, in this comment, and never inside
# the function's own docstring (D-09): the function stays byte-unchanged,
# and the first thing its pin records must not be the phase that edited the
# thing it froze.
_CHAIN_DETECTOR_PINNED_DIGEST = (
    "sha256:d7d42d7a0bd781bdb01f073d2929f7277c33c86c92f49bb63a48055ad15f13c3"
)


def _chain_detector_pin_problems(source: str) -> list[str]:
    """Compare *source* against the pinned `_chain_block_well_formed` digest.

    Takes the source text as a parameter rather than reading the function
    itself, so a self-test control can drive it with perturbed bytes —
    appended to, or stripped from, the real source in memory — without
    monkeypatching the module or editing the frozen function on disk.
    Returns a one-element problem list naming both digests and the standing
    written-amendment pre-commitment on a mismatch, or an empty list when
    *source* still hashes to the pinned value.
    """
    digest = "sha256:" + hashlib.sha256(
        source.rstrip("\n").encode("utf-8")
    ).hexdigest()
    if digest == _CHAIN_DETECTOR_PINNED_DIGEST:
        return []
    return [
        f"chain-detector: source digest {digest!r} != pinned "
        f"{_CHAIN_DETECTOR_PINNED_DIGEST!r} — _chain_block_well_formed is "
        "frozen under CONTRACT-06. If this change is intended, amend the "
        "milestone goal in writing FIRST (STATE.md's standing "
        "pre-commitment), then recompute. Do not recompute to make this "
        "pass."
    ]


# Bold lead-in ending in a colon (e.g. "**Key insight:** ..."); the colon
# must sit immediately before the closing bold markers, distinguishing a
# labelled claim from a bold phrase (e.g. "**Confidence: HIGH**") whose
# colon sits mid-span.
_BOLD_LEADIN_COLON_RE = re.compile(r"^\s*\*\*([^*\n]+:)\*\*")
_LIST_ITEM_RE = re.compile(r"^\s*(?:\d+[.)]|[-*])\s+(.+)$")

_GT_MENTION_RE = re.compile(r"GT-\d+\??")

# FIX-CONTRACT-01 limitation 2: a stored chain id (e.g. "Chain C1") is
# reduced to a bare, comparable form ("c1") by stripping a leading
# "Chain "/"chain " token and case-folding, so an abbreviated citation
# ("(C1)"), a lowercase-bolded one ("chain **C1**"), or a pluralized
# multi-id one ("(Chains C2, C3)") all substring-match the same underlying
# chain — without needing to change how the id is stored or how citations
# are written.
_CHAIN_PREFIX_RE = re.compile(r"^(?:chain|conclusion)\s+", re.IGNORECASE)


def _normalize_chain_id(chain_id: str) -> str:
    """Case-fold and strip a leading 'Chain '/'Conclusion ' token."""
    return _CHAIN_PREFIX_RE.sub("", chain_id.strip()).casefold()


def _normalized_id_safe_for_loose_match(normalized: str) -> bool:
    """Whether a normalized chain id is specific enough to substring-match
    loosely against arbitrary prose.

    Requires BOTH a digit AND a total length of at least two characters.
    The digit requirement rules out a bare letter with no digit (e.g. "a"
    from "Chain A" — the letter "a" appears in nearly every English
    sentence). The length requirement additionally rules out a bare DIGIT
    with no letter (e.g. "1" from "Chain 1") — a single digit is just as
    generic a substring, since it matches inside any other number in the
    prose (e.g. "1" inside "GT-13", "100mm", "$310k"). Only multi-character,
    digit-suffixed forms like "c1" or "dc-1" are safe.
    """
    return len(normalized) >= 2 and bool(re.search(r"\d", normalized))


def _label_has_any_citation(text: str, chain_ids: list[str]) -> bool:
    """Whether `text` references ANY chain id (exact stored form or the
    normalized abbreviated/pluralized form, limitation 2) or any Ground
    Truth id at all.

    This is a laxer PRESENCE check than `_claim_is_traced`'s full D-20
    tracing rule (no >=2-co-occurrence requirement) — used only to decide
    whether a section-intro label or restatement/corollary candidate
    carries "substantive claim content" of its own (limitation 3).
    """
    if any(cid in text for cid in chain_ids):
        return True
    folded = text.casefold()
    for cid in chain_ids:
        normalized = _normalize_chain_id(cid)
        if _normalized_id_safe_for_loose_match(normalized) and normalized in folded:
            return True
    return bool(_GT_MENTION_RE.search(text))


# --- LEDGER-01: closure-ledger traceability --------------------------------
#
# Observed 2026-08-31 on a live PR-P1 run: an analysis that traced its
# Conclusion claims through an explicit "§6→§4 closure ledger" rather than
# inline parentheticals scored WORSE on both halves of the traceability
# signal than one that cited inline. The ledger's own lines were mined as
# ten extra claims (denominator inflated 7 -> 14) while the three prose
# claims they discharged stayed counted as untraced (numerator 0 -> 3).
# `selfaudit_disagreements` then escalated that into a charge that the
# agent over-claimed Criterion 6.
#
# The rubric does not support that charge. Criterion 6 requires only that
# every Conclusion claim "traces to a specific named derivation chain in
# section 4" — it does not prescribe WHERE the citation sits — and
# output-template.md's section 6 prescribes three prose blocks with no
# inline-citation instruction at all. A ledger discharges the same
# obligation an inline parenthetical does. The detector was the defect,
# not the verdict.
#
# Plan 14-01 / D-03 (2026-09-03): the mechanism above credited ANY line
# that both quoted a span and cited a chain id, with no requirement that
# the line take the ledger's own prescribed row shape
# (`- "quote" -> chain Cn`). Measured across all six frozen v8.7 baseline
# analyses: LOAD_BEARING = 0 — removing the ledger scanner entirely
# changes no untraced count. Every fragment it has ever produced on
# tracked bytes is an inert false positive: a bold-lead-in tail
# (`:** involuntary churn is small (<0.5 pts)...`), a quoted customer
# verbatim (`didn't feel I was getting enough for the price,`), and —
# surviving D-02's slicer fix but not this narrowing — three capture
# fragments all under the 4-token floor (`serverless is cheaper than
# containers`, `serverless is the cheap option`, `fastest path`). The
# fix: `_closure_ledger_fragments` now credits a line only when it
# matches `_STRUCTURAL_LEDGER_ROW_RE` — the structural row shape
# output-template.md already prescribes and shows as its conforming
# example — before `_cites_chain` is even consulted. This is a
# NARROWING, the safe direction (nothing load-bearing to lose); widening
# to whole-document scope, the obvious alternative, is explicitly the
# wrong fix (999.3 Case A's treadmill) because it would pull MORE
# Self-Audit Gate quotes into ledger scope, not fewer.
# `_FENCE_RE` and the `_fenced_code_flags` scanner that uses it live beside
# `_APPENDIX_HEADING_RE`, further up, where `_slice_sections` first needs
# them. Placement is reading order only; module globals resolve at call time.

# The structural closure-ledger row shape output-template.md prescribes
# and shows as its conforming example: optional leading whitespace, a `-`
# or `*` list marker, a quoted span of at least 8 characters (straight or
# curly quotes, matching `_LEDGER_QUOTE_RE`'s own quote-character set), an
# arrow (Unicode `→` or ASCII `->` — the capture emits `→`, the existing
# self-test fixture emits `->`), then an optional literal `chain `
# followed by a `C<digits>` identifier. Anchored at the start of the
# stripped line only (never at the end), so a trailing `✓` or trailing
# prose does not prevent a match.
_STRUCTURAL_LEDGER_ROW_RE = re.compile(
    r'^[-*]\s*["“]([^"”\n]{8,})["”]\s*(?:→|->)\s*(?:chain\s+)?(C\d+)',
    re.IGNORECASE,
)

# A ledger entry pairs a quoted claim fragment with a named chain on one
# line:  - "Lambda is 2.10x more expensive per unit of compute"  -> chain C1
_LEDGER_QUOTE_RE = re.compile(r"[\"\u201c]([^\"\u201d\n]{8,})[\"\u201d]")

_TOKEN_RE = re.compile(r"[a-z0-9]+(?:\.[0-9]+)?")

_TRACE_STOPWORDS = frozenset(
    "a an and are as at be by do does for from in is it its of on or "
    "that the to with not no was were this these those".split()
)

# A fragment below this many content tokens is too generic to discharge a
# claim by overlap — a quoted "serverless is cheaper" would otherwise match
# any claim that happens to use those words.
_MIN_LEDGER_FRAGMENT_TOKENS = 4

# Fraction of the FRAGMENT's content tokens that must appear in the claim.
# Measured against the fragment and never against the claim: a long claim
# must not earn credit merely by being long enough to contain a short
# unrelated quote.
_LEDGER_COVERAGE_THRESHOLD = 0.7


def _content_tokens(text: str) -> set[str]:
    """Case-folded alphanumeric tokens with stopwords dropped."""
    return {t for t in _TOKEN_RE.findall(text.casefold()) if t not in _TRACE_STOPWORDS}


def _cites_chain(text: str, chain_ids: list[str]) -> bool:
    """Whether `text` names a chain id — exact stored form, or the
    normalized abbreviated/pluralized form (FIX-CONTRACT-01 limitation 2).

    Lifted verbatim out of `_claim_is_traced`'s first two clauses so the
    ledger scanner can require a CHAIN citation specifically, where
    `_label_has_any_citation` would also accept a bare GT mention.
    """
    if any(cid in text for cid in chain_ids):
        return True
    folded = text.casefold()
    for cid in chain_ids:
        normalized = _normalize_chain_id(cid)
        if _normalized_id_safe_for_loose_match(normalized) and normalized in folded:
            return True
    return False


def _closure_ledger_fragments(section6: str, chain_ids: list[str]) -> list[str]:
    """Quoted claim fragments from closure-ledger lines in section 6.

    A ledger line is now the structural row form output-template.md
    prescribes (`- "quote" -> chain Cn`, accepting both `→` and `->`) —
    not, as before plan 14-01 / D-03, any line that BOTH quotes a span and
    cites a real chain id. `_cites_chain` still runs AFTER the structural
    match: an id cited but absent from section 4 is not a chain id and
    still yields no fragment, so a ledger still cannot invent its own
    authority. Both halves remain load-bearing: a quote citing nothing
    traces nothing, and a chain citation with no quote names which chain
    but not which claim.
    """
    fragments: list[str] = []
    for line in section6.splitlines():
        stripped = line.strip()
        if not _STRUCTURAL_LEDGER_ROW_RE.match(stripped):
            continue
        if not _cites_chain(stripped, chain_ids):
            continue
        fragments.extend(m.group(1) for m in _LEDGER_QUOTE_RE.finditer(stripped))
    return fragments


def _ledger_fragment_covers(fragment: str, claim_text: str) -> bool:
    """Whether a ledger fragment quotes substantially the content of a claim.

    Overlap rather than substring: a ledger paraphrases lightly (`"Lambda
    is 2.10x more expensive ..."` against a claim reading `"... it is
    2.10x more expensive ..."`), so an exact-substring rule would credit
    almost nothing. The two guards above — a minimum fragment size and a
    coverage fraction taken over the fragment — are what keep the overlap
    from degenerating into "any long claim matches any short quote".
    """
    frag = _content_tokens(fragment)
    if len(frag) < _MIN_LEDGER_FRAGMENT_TOKENS:
        return False
    covered = len(frag & _content_tokens(claim_text))
    return covered / len(frag) >= _LEDGER_COVERAGE_THRESHOLD


def _is_assertive_claim(text: str) -> bool:
    """Keep only items with sentence-ending punctuation or over forty characters.

    Excludes bare labels (e.g. a short intro line ending in a colon with no
    trailing sentence) from being counted as Conclusion claims.
    """
    stripped = text.strip()
    if not stripped:
        return False
    if re.search(r"[.!?][\'\")”’]*$", stripped):
        return True
    return len(stripped) > 40


# FIX-CONTRACT-01 limitation 3(b)/(c): a narrow, closed set of restatement/
# summary lead-in cues, and a dual-negation corollary shape ("**X — no**,
# and **Y — no**:"). Both are bounded by `_is_excluded_restatement` below,
# which requires the candidate to carry no citation of its own AND an
# earlier claim in the same section to already be cited — "a near-paraphrase
# ... of an already-extracted, already-cited claim EARLIER in the same
# section" (the plan's own framing), not a blanket "drop short bullets."
_RESTATEMENT_LEADIN_RE = re.compile(
    r"^\*\*(?:bottom line|in short|in summary|to summarize|overall)\b[^*\n]*:\*\*",
    re.IGNORECASE,
)
_DUAL_NEGATION_COROLLARY_RE = re.compile(r"^\*\*[^*\n]+\*\*,?\s+and\s+\*\*[^*\n]+\*\*:")


def _is_excluded_restatement(candidate: str, chain_ids: list[str], prior_claims: list[str]) -> bool:
    """FIX-CONTRACT-01 limitation 3(c): near-paraphrase restatement / direct
    logical entailment of an already-extracted, already-cited claim earlier
    in the same section.

    Self-limiting: fires ONLY when (1) the candidate itself carries no
    citation, (2) it matches one of the two narrow restatement/corollary
    shapes above, AND (3) an earlier claim in the same claims list can
    actually be located that already carries a citation — i.e. the
    "already-cited antecedent" this exclusion depends on must be found, not
    assumed.
    """
    if _label_has_any_citation(candidate, chain_ids):
        return False
    if not (
        _RESTATEMENT_LEADIN_RE.match(candidate) or _DUAL_NEGATION_COROLLARY_RE.match(candidate)
    ):
        return False
    return any(_label_has_any_citation(c, chain_ids) for c in prior_claims)


def _conclusion_claims(section6: str, chain_ids: list[str] | None = None) -> list[str]:
    """Return the assertive claims in section 6: bold colon-lead-ins and list items.

    Returns the claim text (not just a count) so the detector output can be
    audited.

    FIX-CONTRACT-01 limitation 3 excludes two further non-claim shapes when
    `chain_ids` is supplied:
      (b) a colon-terminated bold lead-in that IS the entire physical line
          (nothing follows the closing `**` on the same line) and carries
          no citation of its own — a pure section-intro label, not a claim
          (e.g. "Before revisiting the decision, close the four unverified
          preconditions cheaply:").
      (c) a near-paraphrase restatement or direct logical entailment of an
          already-cited claim earlier in the same section
          (`_is_excluded_restatement`).
    Genuinely-uncited imperative recommendations that are neither of these
    two shapes (e.g. "Confirm there is an SLO...", "Measure your own
    p99...") are NOT excluded — they remain counted and, if truly uncited,
    remain flagged as the honest residual (honesty-not-score, D-01).
    """
    chain_ids = chain_ids or []
    claims: list[str] = []
    # LEDGER-01: a fenced block is verbatim structural content — a closure
    # ledger, a formula, a captured snippet — not section-6 prose. Mining
    # it for claims counted a ledger's own rows as ten additional claims on
    # the live PR-P1 run.
    #
    # Uses `_fenced_code_flags` (real CommonMark closing rules) rather than
    # the parity toggle this line held until the phase-14 review. Parity
    # inverted permanently on ordinary content — a ~~~ block quoting a ```
    # example, or any unterminated fence — after which every remaining
    # line read as fenced and the whole section returned ZERO claims. That
    # is a silent false-clean, and it was reachable without touching
    # `_slice_sections` at all. Splitting on "\n" (not `splitlines()`)
    # keeps this walk's line boundaries identical to the slicer's.
    lines = section6.split("\n")
    fenced = _fenced_code_flags(lines)
    for idx, line in enumerate(lines):
        if fenced[idx]:
            continue
        stripped = line.strip()
        if not stripped:
            continue
        m_bold = _BOLD_LEADIN_COLON_RE.match(stripped)
        if m_bold:
            if m_bold.end() == len(stripped) and not _label_has_any_citation(stripped, chain_ids):
                # limitation 3(b): pure section-intro label, no substantive
                # claim content of its own.
                continue
            if _is_assertive_claim(stripped) and not _is_excluded_restatement(
                stripped, chain_ids, claims
            ):
                claims.append(stripped)
            continue
        m_list = _LIST_ITEM_RE.match(stripped)
        if m_list:
            candidate = m_list.group(1).strip()
            if _is_assertive_claim(candidate) and not _is_excluded_restatement(
                candidate, chain_ids, claims
            ):
                claims.append(candidate)
    return claims


def _claim_is_traced(
    claim_text: str,
    chain_ids: list[str],
    chain_blocks: list[str],
    ledger_fragments: tuple[str, ...] | list[str] = (),
) -> bool:
    """A claim is traced if it names a chain identifier — either the exact
    stored form (e.g. "Chain C1") or a normalized abbreviated/pluralized
    citation of it (e.g. "(C1)", "chain **C1**", "(Chains C2, C3)" —
    FIX-CONTRACT-01 limitation 2) — or names >=2 GT ids that also appear
    together inside a single chain block (D-20) — or is quoted by a
    closure-ledger entry that cites a real chain (LEDGER-01).

    `ledger_fragments` defaults to empty, so every call site that predates
    LEDGER-01 keeps its exact prior behaviour.
    """
    if _cites_chain(claim_text, chain_ids):
        return True
    gt_mentions = {m.group(0).rstrip("?") for m in _GT_MENTION_RE.finditer(claim_text)}
    if len(gt_mentions) >= 2:
        for block in chain_blocks:
            block_gts = {m.group(0).rstrip("?") for m in _GT_MENTION_RE.finditer(block)}
            if gt_mentions <= block_gts:
                return True
    return any(_ledger_fragment_covers(f, claim_text) for f in ledger_fragments)


_DEFECT_RECORD_FIELDS = (
    "analysis_id",
    "conclusion_claims",
    "untraced_claims",
    "untraced_flag",
    "verdict_cells",
    "nonconforming_verdict_cells",
    "verdict_flag",
    "chain_blocks",
    "malformed_chain_blocks",
    "chain_flag",
    # Appended (not inserted) so that every committed ten-column
    # defect-incidence TSV keeps its existing column ORDER. `read_defect_
    # incidence` maps by header name, so a ten-column file and a
    # thirteen-column file both parse; appending keeps positional readers
    # outside this file working too.
    "dependency_cycles",
    "ungrounded_chains",
    "selfaudit_disagreements",
    # Phase 5 (PROV-05, D-11): nine more appended, same discipline as above —
    # every committed thirteen-column file keeps its order; `read_defect_
    # incidence` maps by header name so both old and new widths parse.
    "provenance_labels",
    "unmatched_sources",
    "unreadable_sources",
    "literals_checked",
    "unlocated_literals",
    "misattributed_literals",
    "zero_literal_gts",
    "orphan_fetches",
    "provenance_flag",
)


_HEAD_ARROW_SPLIT_RE = re.compile(_ARROW)
_CHAIN_REF_WORD_RE = re.compile(r"\b" + _CHAIN_REF_TOKEN + r"\b")


def _chain_head_refs(block: str) -> tuple[set[str], set[str]]:
    """Return `(gt_refs, chain_refs)` cited in a block's head line.

    The head is the portion of the first candidate line preceding its first
    arrow. GT tokens are stripped before the chain-ref scan so that
    `GT-C1` — a ground truth whose identifier happens to start with `C` —
    is never miscounted as a reference to chain `C1`.
    """
    for idx, ln in enumerate(block.splitlines()):
        s = ln.strip()
        # Skip the block's own markdown heading. `_chain_blocks` starts each
        # block at its heading line, and that line carries the chain's OWN
        # id (`### Conclusion C1:`) — reading it as a head would make every
        # composing chain self-referential and report the whole section as
        # one cycle.
        if s.startswith("#"):
            continue
        # GAP-8: the same hazard, via the OTHER label form. `_chain_ids` and
        # `_chain_blocks` recognise two shapes — `_CHAIN_HEADING_RE`
        # (hash-led) and `_CHAIN_BOLD_RE` (bold-led, no hashes) — and start a
        # block at whichever matched, but the guard above keys on markdown
        # heading SYNTAX rather than on "is this the block's own label line".
        # A bold-labelled analysis therefore reproduced the exact failure the
        # comment above predicts: PR-P1 run 4 labelled its chains
        # `**C1 — …**` and every one of its eight chains was reported both
        # self-cyclic and ungrounded, all artifact.
        #
        # Restricted to `idx == 0` deliberately, NOT applied to every line.
        # `_CHAIN_BOLD_RE`'s label alternation includes `[A-Z]{2}-\d+`, so a
        # fully-bolded HEAD line — `**GT-1 + GT-2 (label) → … → …**` — also
        # matches it (label `GT-1`); a blanket skip would swallow that head
        # and turn a well-formed grounded chain into an ungrounded one. The
        # block's own label is guaranteed to sit at line 0 because
        # `_chain_blocks` slices from the label match's own `start()`, so the
        # narrow form fixes the defect and cannot reach a head line further
        # down. Pinned by `_selftest_gap8_bold_chain_labels` control (d).
        if idx == 0 and _CHAIN_BOLD_RE.match(s):
            continue
        if not _CHAIN_HEAD_TOKEN_RE.search(s):
            continue
        head = _HEAD_ARROW_SPLIT_RE.split(s, 1)[0]
        gts = set(re.findall(_GT_TOKEN_WIDE, head))
        chains = set(_CHAIN_REF_WORD_RE.findall(re.sub(_GT_TOKEN_WIDE, " ", head)))
        if gts or chains:
            return gts, chains
    return set(), set()


def _chain_dependency_defects(section4: str) -> dict:
    """GAP-6 safety net: cycles and ungrounded chains among composition heads.

    Widening `_CHAIN_FORM_LINE_RE` to accept `GT-5 + C6` heads removed the
    property that made GT-only heads safe — a ground truth is an axiom, so a
    GT-only dependency graph cannot cycle. This reports the two defects the
    widening admits:

    - **cycles** — `C1` citing `C2` citing `C1`, or a chain citing itself.
      Circular reasoning, which the validation rubric names as an
      abandonment reason in its own right.
    - **ungrounded** — a chain with no ground truth in its own head and no
      path through its dependencies to one. Its conclusion rests on nothing
      verified, however well-formed its arrows are.

    Returns `{"cycles": [...], "ungrounded": [...]}` with normalized ids, in
    document order. A section whose chains cannot be paired with ids (no
    labels, or a block/id count mismatch) returns both lists empty rather
    than guessing — the shape checks already cover an unlabelled section.

    Reported through `detect_defects`'s audit-only underscore fields. It is
    deliberately NOT a `_DEFECT_RECORD_FIELDS` column: that schema is
    compared column-by-column against the committed calibration corpus, and
    a new column there is a separate decision from this one.
    """
    ids = _chain_ids(section4)
    blocks = _chain_blocks(section4)
    if not ids or len(ids) != len(blocks):
        return {"cycles": [], "ungrounded": []}

    norm = [_normalize_chain_id(i) for i in ids]
    known = set(norm)
    deps: dict[str, set[str]] = {}
    own_gt: dict[str, bool] = {}
    headed: dict[str, bool] = {}
    for name, block in zip(norm, blocks):
        gts, chain_refs = _chain_head_refs(block)
        deps[name] = {c.casefold() for c in chain_refs} & known
        own_gt[name] = bool(gts)
        # A block citing NOTHING has no head this function can read. That is
        # a SHAPE defect and `_chain_block_well_formed` already owns it —
        # reporting it here too would count one defect twice and would make
        # this signal a noisier duplicate of the malformed-block count
        # rather than an orthogonal one. Measured on the frozen corpus:
        # condA-P3 "Chain C" and condB-P2 "Chain D" are head-less
        # second-order effect lists, already inside the pinned
        # `_CALIBRATION_MALFORMED_CHAIN_BLOCKS` counts.
        headed[name] = bool(gts or chain_refs)

    # Cycle detection: white/grey/black DFS. A grey re-entry is a back edge.
    WHITE, GREY, BLACK = 0, 1, 2
    colour = dict.fromkeys(norm, WHITE)
    in_cycle: set[str] = set()

    def visit(node: str, stack: list[str]) -> None:
        colour[node] = GREY
        stack.append(node)
        for dep in sorted(deps.get(node, ())):
            if colour.get(dep) == GREY:
                in_cycle.update(stack[stack.index(dep):])
            elif colour.get(dep) == WHITE:
                visit(dep, stack)
        stack.pop()
        colour[node] = BLACK

    for name in norm:
        if colour[name] == WHITE:
            visit(name, [])

    # Grounding: reachable to a ground truth through the dependency graph.
    memo: dict[str, bool] = {}

    def grounded(node: str, seen: frozenset[str] = frozenset()) -> bool:
        if node in memo:
            return memo[node]
        if node in seen:
            return False  # cycle: contributes no grounding of its own
        if own_gt.get(node):
            memo[node] = True
            return True
        result = any(
            grounded(dep, seen | {node}) for dep in sorted(deps.get(node, ()))
        )
        if not seen:
            memo[node] = result
        return result

    return {
        "cycles": [n for n in norm if n in in_cycle],
        "ungrounded": [n for n in norm if headed[n] and not grounded(n)],
    }


# Self-Audit Gate verdict blocks, emitted as PROCESS output rather than as one
# of the six template sections, so these are matched against the whole
# analysis text and not against a slice.
_SELFAUDIT_CRITERION_RE = re.compile(
    r"^\*\*Criterion[ \t]+(?P<num>[1-6])[ \t]*:[^\n]*\*\*[ \t]*$", re.MULTILINE
)
_SELFAUDIT_BAND_RE = re.compile(
    r"^\**Band:\**[ \t]*\*\*(?P<band>Rigorous|Sound|Hand-wavy|Absent)\*\*",
    re.MULTILINE,
)

# Which measured field contradicts a claimed **Rigorous** on which criterion.
# Only Rigorous is contradicted: Sound, Hand-wavy and Absent already concede a
# defect, and under the Criterion 4 Sound band ("chains render their hops as an
# ordered list ... instead of the prescribed arrow-led form") a Sound verdict
# alongside malformed chains is the CORRECT self-report, not a disagreement.
_SELFAUDIT_CONTRADICTIONS: dict[int, tuple[str, ...]] = {
    2: ("nonconforming_verdict_cells",),
    4: ("malformed_chain_blocks", "_dependency_cycles"),
    6: ("untraced_claims",),
}


def _selfaudit_bands(analysis_text: str) -> dict[int, str]:
    """Map criterion number -> claimed band, from the emitted verdict blocks.

    A criterion block runs from its `**Criterion N: ...**` line to the next
    such line (or end of text); the first `Band: **X**` inside it is the
    claim. A criterion with no band line is omitted rather than defaulted —
    an unstated band is not a claim, and must not be scored as one.
    """
    heads = list(_SELFAUDIT_CRITERION_RE.finditer(analysis_text))
    bands: dict[int, str] = {}
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(analysis_text)
        block = analysis_text[m.end() : end]
        bm = _SELFAUDIT_BAND_RE.search(block)
        if bm:
            bands.setdefault(int(m.group("num")), bm.group("band"))
    return bands


def _selfaudit_calibration_defects(analysis_text: str, record: dict) -> list[dict]:
    """Disagreements between the Self-Audit Gate's claimed bands and measurement.

    The Self-Audit Gate is self-reported and nothing reconciled it against the
    mechanical record. Observed 2026-08-30: an analysis scored itself
    **Criterion 4: Reason Upward — Rigorous** and returned **Gate: PASS** while
    every one of its six chains was mechanically malformed.

    That run was NOT lying, which is the point of this check. Criterion 4's
    band descriptors scored only semantics — names its GT-IDs, carries an
    intermediate, reaches a conclusion — all of which those chains did. The
    prescribed rendering appeared in the criterion's preamble and in no band,
    so a Rigorous verdict was defensible on the rubric as written. The rubric
    now names the form in the Rigorous and Sound bands; this function is what
    makes the resulting claim falsifiable rather than merely stated.

    Returns one record per disagreement, in criterion order. An analysis with
    no verdict blocks returns `[]` — absence of a self-audit is a separate
    defect, owned by the agent body's "say so explicitly at the top of the
    response" disclosure rule, and is not silently recoded as agreement here.
    """
    bands = _selfaudit_bands(analysis_text)
    out: list[dict] = []
    for num in sorted(_SELFAUDIT_CONTRADICTIONS):
        if bands.get(num) != "Rigorous":
            continue
        for field in _SELFAUDIT_CONTRADICTIONS[num]:
            value = record.get(field)
            count = len(value) if isinstance(value, list) else (value or 0)
            if count:
                out.append(
                    {
                        "criterion": num,
                        "claimed": "Rigorous",
                        "contradicted_by": field,
                        "measured": count,
                    }
                )
    return out


def detect_defects(analysis_text: str, analysis_id: str) -> dict:
    """D-18: parse `analysis_text` structurally and report the three defect families.

    Raises `SectionResolutionError` (propagated from `_slice_sections`) if
    the six output-template sections do not resolve — a document the parser
    cannot read must fail loudly, never report zero defects.

    Returns a record with the ten fields in `_DEFECT_RECORD_FIELDS` order,
    plus underscore-prefixed audit-only fields (claim/cell text) that are
    never emitted to the TSV.
    """
    sections = _slice_sections(analysis_text)
    section2 = sections[2]
    section4 = sections[4]
    section6 = sections[6]

    verdicts = _verdict_cells(section2)
    nonconforming_verdicts = [c for c in verdicts if not _verdict_conforms(c)]

    chain_ids = _chain_ids(section4)
    blocks = _chain_blocks(section4)
    malformed_blocks = [b for b in blocks if not _chain_block_well_formed(b)]

    dependency = _chain_dependency_defects(section4)
    claims = _conclusion_claims(section6, chain_ids)
    ledger = _closure_ledger_fragments(section6, chain_ids)
    untraced = [
        c for c in claims if not _claim_is_traced(c, chain_ids, blocks, ledger)
    ]

    record = {
        "analysis_id": analysis_id,
        "conclusion_claims": len(claims),
        "untraced_claims": len(untraced),
        "untraced_flag": 1 if untraced else 0,
        "verdict_cells": len(verdicts),
        "nonconforming_verdict_cells": len(nonconforming_verdicts),
        "verdict_flag": 1 if nonconforming_verdicts else 0,
        "chain_blocks": len(blocks),
        "malformed_chain_blocks": len(malformed_blocks),
        "chain_flag": 1 if malformed_blocks else 0,
        "_claims_text": claims,
        "_untraced_claims_text": untraced,
        "_nonconforming_verdict_text": nonconforming_verdicts,
        "_malformed_chain_blocks_text": malformed_blocks,
        "_closure_ledger_fragments": ledger,
        "dependency_cycles": len(dependency["cycles"]),
        "ungrounded_chains": len(dependency["ungrounded"]),
        # Placeholder: the reconciliation needs the finished record, so it
        # is computed immediately below and this value replaced. It is
        # declared here so the key order matches _DEFECT_RECORD_FIELDS.
        "selfaudit_disagreements": 0,
        "_dependency_cycles": dependency["cycles"],
        "_ungrounded_chains": dependency["ungrounded"],
    }
    # Phase 5 (PROV-05, D-10): the harness owns only the default. The
    # sentinel is the string "n/a", never 0 — "no capture available" and
    # "checked, found clean" must not print the same value, and
    # `read_defect_incidence` `int()`s only the three `*_flag` columns, so a
    # string round-trips safely through every other column. A capture-aware
    # caller (e.g. check-provenance.py) overwrites these keys with real
    # values; `detect_defects` itself gains no capture argument.
    record.update({
        "provenance_labels": "n/a",
        "unmatched_sources": "n/a",
        "unreadable_sources": "n/a",
        "literals_checked": "n/a",
        "unlocated_literals": "n/a",
        "misattributed_literals": "n/a",
        "zero_literal_gts": "n/a",
        "orphan_fetches": "n/a",
        "provenance_flag": "n/a",
    })
    disagreements = _selfaudit_calibration_defects(analysis_text, record)
    record["selfaudit_disagreements"] = len(disagreements)
    record["_selfaudit_disagreements"] = disagreements
    return record


def run_detect_defects(analyses_dir: Path, out_path: Path) -> None:
    """`--detect-defects` CLI body: run `detect_defects` over a directory, write a TSV.

    Records are written in filename order with a header row, ten columns
    per `_DEFECT_RECORD_FIELDS`.
    """
    files = sorted(Path(analyses_dir).glob("*.md"))
    lines = ["\t".join(_DEFECT_RECORD_FIELDS)]
    for f in files:
        record = detect_defects(f.read_text(encoding="utf-8"), f.stem)
        lines.append("\t".join(str(record[field]) for field in _DEFECT_RECORD_FIELDS))
    Path(out_path).write_text("\n".join(lines) + "\n", encoding="utf-8")


_DEFECT_FIXTURE_CONFORMANT = FIXTURES_DIR / "analyses-conformant.md"
_DEFECT_FIXTURE_DEFECTIVE = FIXTURES_DIR / "analyses-defective.md"

# Expected records (all nine numeric fields, not just the three flags — a
# flags-only assertion would pass while the per-claim counts D-20 depends on
# drifted silently).
_EXPECTED_CONFORMANT_RECORD = {
    "conclusion_claims": 3,
    "untraced_claims": 0,
    "untraced_flag": 0,
    "verdict_cells": 3,
    "nonconforming_verdict_cells": 0,
    "verdict_flag": 0,
    "chain_blocks": 2,
    "malformed_chain_blocks": 0,
    "chain_flag": 0,
    "dependency_cycles": 0,
    "ungrounded_chains": 0,
    "selfaudit_disagreements": 0,
}
_EXPECTED_DEFECTIVE_RECORD = {
    "conclusion_claims": 3,
    "untraced_claims": 1,
    "untraced_flag": 1,
    "verdict_cells": 3,
    "nonconforming_verdict_cells": 1,
    "verdict_flag": 1,
    "chain_blocks": 2,
    "malformed_chain_blocks": 1,
    "chain_flag": 1,
    "dependency_cycles": 0,
    "ungrounded_chains": 0,
    "selfaudit_disagreements": 0,
}

# D-19 pinned observed calibration vector: the detector's OBSERVED per-
# document output over the six frozen analyses in
# tests/quality-baseline-v8.7/analyses/, in filename order, produced
# 2026-07-22 by `--detect-defects tests/quality-baseline-v8.7/analyses`
# and committed unedited to
# tests/quality-fixtures-v8.7/calibration-v8.6-corpus.tsv (see
# calibration-v8.6-corpus.md for the full finding). These are the values
# the detector actually produced, NOT the judge-reported figures (6/6, 6/6,
# 4/6) — pinning the observed vector makes a future change to the
# detector's definitions move it loudly rather than silently.
#
# Staleness caveat (Phase 183, DETECT-02): the committed
# tests/quality-fixtures-v8.7/calibration-v8.6-corpus.tsv file's
# `nonconforming_verdict_cells` column was produced under the pre-DETECT-02
# (inverted) Verdict check and no longer reproduces against the corrected
# detector — the `condB-P3` row is the clearest instance, moving from `4`
# to `15` nonconforming verdict cells (out of 15 total) once re-scored. The
# binary flags below are unaffected (verified stable, see the vectors
# immediately below this comment), so this staleness does not move any
# pinned value in this file; it is noted here purely for documentation
# honesty. The TSV is read by no runtime code path in this script and
# asserted by no self-test item. DETECT-05 (Phase 186) owns any correction
# to the TSV itself; this comment records the fact without editing it.
#
# Chain-axis staleness (Phase 184-05, DETECT-03, re-measured 2026-07-27
# against the tree as it stands after Phase 184-04, re-run over the six
# analyses in tests/quality-baseline-v8.7/analyses/ in
# _CALIBRATION_ANALYSIS_ORDER and compared column-by-column against the
# committed tests/quality-fixtures-v8.7/calibration-v8.6-corpus.tsv). This
# paragraph SUPERSEDES the Phase 184-03 version of itself, which shipped a
# false attribution in tracked source (184-VERIFICATION.md gap 5) — see
# the correction below.
#   - `chain_blocks`            TSV [5, 5, 3, 4, 4, 5]  -> unchanged
#   - `malformed_chain_blocks`  TSV [2, 2, 2, 2, 3, 3]  -> reproduces the
#     TSV column exactly, [2, 2, 2, 2, 3, 3], on all six rows. The chain
#     axis is consequently NO LONGER STALE as of Phase 184-04.
#   - `chain_flag`              TSV [1, 1, 1, 1, 1, 1]  -> unchanged
#
# Measured attribution (re-executed against three revisions plus two fault
# injections this session, not asserted): `1f71211` (pre-phase base)
# produces [2, 2, 2, 2, 3, 3]; `b50e8e4` (Phase 184-01, the block-level
# correction) ALSO produces [2, 2, 2, 2, 3, 3] — 184-01 moved this column
# by ZERO on all six rows. The [5, 2, 3, 3, 3, 5] excursion existed only at
# `37fea87` (Phase 184-03) and was caused entirely by the `^` line-start
# anchor then placed on `_GT_HEAD_RE`, not by the head-arrow guard added in
# the same commit: removing ONLY the head-arrow guard from `37fea87`
# (INJ-A) leaves [5, 2, 3, 3, 3, 5] unchanged; reverting ONLY the `^`
# anchor from `37fea87` (INJ-B) restores [2, 2, 2, 2, 3, 3] exactly. The
# anchor is the entire cause; the guard is not.
#
# The seven blocks that flipped at `37fea87`, named and classified — every
# one is a false positive, not tightened detection, because each carries a
# complete two-arrow chain sitting behind a backtick, a bold marker or a
# blockquote prefix, which the `^` anchor rejected for its punctuation, not
# its logic:
#   - condA-P1 "### DC-1: Estimate — how much latency can serialization
#     actually return? (Fermi)" — false positive (backtick-wrapped
#     `GT-2 + GT-5 + GT-1 → ... → ...` chain line inside the block).
#   - condA-P1 "### DC-2: Theoretical limit — the ceiling on this entire
#     program" — false positive (backtick-wrapped
#     `GT-1 (Amdahl) + GT-4 ... → ... → ...` chain line).
#   - condA-P1 "### DC-3: The benefit is misattributed" — false positive
#     (backtick-wrapped `GT-3 + GT-11 → ... → ...` chain line).
#   - condA-P3 "### Chain A — Energy saved per unit spent" — false
#     positive (blockquote + bold `GT-1 + GT-2 + GT-4 → ... → ...` chain
#     line).
#   - condB-P1 "**Chain B — the tail-latency exception:**" — false
#     positive (blockquote + backtick `GT-7 + GT-8? → ... → ...` chain
#     line).
#   - condB-P3 "### Chain 1 — Conductive saving per option (Fermi
#     estimate, unit-bracketed)" — false positive (backtick-wrapped
#     `GT-1 + GT-3 + GT-7? → ... → ...` chain line with a bracketed
#     assumption clause).
#   - condB-P3 "### Chain 3 — The draught symptom is not addressed by
#     either option" — false positive (backtick-wrapped
#     `GT-13 + GT-9 + GT-2 → ... → ...` chain line with a bracketed
#     assumption clause).
#
# Mechanical corroboration, not editorial judgement: the post-fix
# malformed-block SETS — not merely their counts — are identical to
# `1f71211` on all six analyses (re-verified by set diff this session). A
# judgment call could produce matching counts over a different set of
# blocks; set identity could not survive that.
#
# This paragraph corrects a false claim the Phase 184-03 version of this
# same comment shipped in tracked source: it attributed the +7 movement to
# Phase 184-01 (which moved the column by zero, measured above) and to the
# head-arrow guard (which INJ-A proves is not the cause), and it
# characterised the seven added detections as "genuinely tightened-
# boundary counts" when all seven are false positives on well-formed
# chains, including the project's own template. That attribution was false
# and is corrected here on measurement — the same discipline that prior
# paragraph invoked while getting it wrong the first time (honesty-not-
# score, D-01) — so the correction history stays legible rather than being
# tidied away, the same way the paragraph above already records its own
# Phase-183-era correction.
#
# The flags do not move, so `_CALIBRATION_CHAIN_FLAGS` below is still left
# exactly as it is under D-09's leave-alone branch. This comment records
# the measured truth; it is never an edit to the TSV itself — DETECT-05
# (Phase 186) owns any correction to the TSV. Phase 185 (DETECT-04) still
# owns full re-derivation of all `_CALIBRATION_*` constants — the four
# `_CALIBRATION_ANALYSIS_ORDER`-indexed vectors above plus
# `_CALIBRATION_MALFORMED_CHAIN_BLOCKS` below (added by Phase 184-04, a
# fifth constant Phase 185's re-derivation scope must now also cover) —
# treating this comment as an input to verify, not a result to trust.
#
# Verdict-axis re-derivation (Phase 185, DETECT-04, measured 2026-07-27
# against base commit 846ff2e, re-run over the six analyses in
# tests/quality-baseline-v8.7/analyses/ in _CALIBRATION_ANALYSIS_ORDER via
# `--detect-defects` and compared column-by-column against the committed
# tests/quality-fixtures-v8.7/calibration-v8.6-corpus.tsv):
#   - `nonconforming_verdict_cells`  TSV [13, 8, 10, 8, 7, 4]  -> recomputed
#     [13, 8, 10, 8, 7, 15]. MOVED on condB-P3 only (4 -> 15, out of 15
#     total), once the corrected `_verdict_conforms` (DETECT-02, Phase 183)
#     is applied. This is the OLD value the new sixth constant
#     `_CALIBRATION_NONCONFORMING_VERDICT_CELLS` below replaces.
#   - `_CALIBRATION_VERDICT_FLAGS`   TSV [1, 1, 1, 1, 1, 1]  -> recomputed
#     [1, 1, 1, 1, 1, 1]. NO MOVE — but this no-move is uninformative, not
#     reassuring: `verdict_flag` on condB-P3 was already saturated at 1
#     before the correction (4-of-15 nonconforming was already nonzero),
#     so the binary is structurally incapable of registering the 4-to-15
#     movement above. The direction measured is that the binary and the
#     numeric vector genuinely disagree in sensitivity, not that nothing
#     changed; no per-cell mechanism beyond `_verdict_conforms`'s own
#     corrected predicate is asserted here, because none beyond that was
#     confirmed against the documents themselves this phase.
#
# Full re-derivation, remaining constants (Phase 185, DETECT-04, measured
# 2026-07-27 against base commit 846ff2e, each recomputed independently by
# re-running `--detect-defects tests/quality-baseline-v8.7/analyses` and
# comparing to the committed
# tests/quality-fixtures-v8.7/calibration-v8.6-corpus.tsv column, verified
# by the author before writing the value below — a no-move recorded as a
# bare "unchanged" is indistinguishable from a value that was never
# re-checked, which is why every one of the six constants gets an explicit
# OLD/NEW/reason record here, moved or not):
#   - `_CALIBRATION_ANALYSIS_ORDER`  OLD and NEW both ("condA-P1",
#     "condA-P2", "condA-P3", "condB-P1", "condB-P2", "condB-P3"). NO MOVE.
#     Reason: `sorted(glob("*.md"))` over
#     tests/quality-baseline-v8.7/analyses/ still yields exactly these six
#     stems in this order — the corpus file set did not change.
#   - `_CALIBRATION_UNTRACED_FLAGS`  TSV [1, 1, 1, 1, 1, 1]  -> recomputed
#     [1, 1, 1, 1, 1, 1]. NO MOVE. Reason: every document retains at least
#     one untraced conclusion claim, so the binary saturates.
#   - `_CALIBRATION_VERDICT_FLAGS` — see the Verdict-axis re-derivation
#     paragraph immediately above: NO MOVE, and structurally incapable of
#     registering the condB-P3 4-to-15 movement pinned by the new sixth
#     constant.
#   - `_CALIBRATION_CHAIN_FLAGS`  TSV [1, 1, 1, 1, 1, 1]  -> recomputed
#     [1, 1, 1, 1, 1, 1]. NO MOVE. Reason: every document retains at least
#     one malformed block after DETECT-03's block-level correction, so the
#     binary saturates — the same blindness class the chain axis already
#     documents in the Chain-axis staleness paragraph above, now stated
#     explicitly for this flag too.
#   - `_CALIBRATION_MALFORMED_CHAIN_BLOCKS`  TSV [2, 2, 2, 2, 3, 3]  ->
#     recomputed [2, 2, 2, 2, 3, 3]. NO MOVE, RE-CONFIRMED this phase by
#     independent recomputation at 846ff2e, consistent with the
#     Chain-axis-staleness (Phase 184-05) measurement recorded above it in
#     this same comment block.
#
# One honest finding, recorded unattributed (Phase 185, DETECT-04):
# comparing the committed pre-DETECT-02 TSV against the HEAD recomputation
# shows `conclusion_claims` moving 10 -> 9 on condA-P2 and 9 -> 8 on
# condA-P3, and `untraced_claims` moving 6 -> 5 and 7 -> 6 on the same two
# rows — while `untraced_flag` stayed saturated at [1, 1, 1, 1, 1, 1]
# throughout. That is a THIRD instance of the saturation-blindness class
# documented in this file, on an axis with no pinned numeric vector. Its
# cause was NOT measured in this phase: DETECT-02 and DETECT-03 touched
# `_verdict_conforms` and `_chain_block_well_formed`, neither of which is
# called by `_conclusion_claims` or `_claim_is_traced`, so the movement is
# not attributable to either of them on the evidence in hand, and the TSV
# predates other changes as well. This is written down as
# observed-and-unattributed, explicitly, because the paragraph above this
# whole block already records the correction of a false attribution that a
# prior version of this same comment shipped in tracked source over an
# analogous finding — that correction history is the reason no cause is
# assigned here.
_CALIBRATION_ANALYSIS_ORDER = (
    "condA-P1",
    "condA-P2",
    "condA-P3",
    "condB-P1",
    "condB-P2",
    "condB-P3",
)
_CALIBRATION_UNTRACED_FLAGS = [1, 1, 1, 1, 1, 1]

# LEDGER-01: `_CALIBRATION_UNTRACED_FLAGS` is saturated at 1 across all six
# analyses and is therefore structurally blind to ANY movement in the counts
# beneath it — the same blindness 184-REVIEW.md WR-01 found in
# `_CALIBRATION_CHAIN_FLAGS`, which stayed green through a +7 false-positive
# regression. The two vectors below pin what the flags cannot see. Measured
# on tests/quality-baseline-v8.7/analyses/ in _CALIBRATION_ANALYSIS_ORDER
# immediately BEFORE the LEDGER-01 claim-extraction change, and re-measured
# byte-identical after it — which is the evidence that widening traceability
# to closure ledgers moved nothing on the frozen corpus.
_CALIBRATION_CONCLUSION_CLAIMS = [9, 9, 8, 5, 6, 4]
_CALIBRATION_UNTRACED_CLAIMS = [4, 5, 6, 3, 3, 4]
_CALIBRATION_VERDICT_FLAGS = [1, 1, 1, 1, 1, 1]
_CALIBRATION_CHAIN_FLAGS = [1, 1, 1, 1, 1, 1]

# _CALIBRATION_MALFORMED_CHAIN_BLOCKS (Phase 184-04, DETECT-03): a fifth
# _CALIBRATION_* constant — Phase 185 (DETECT-04) is scoped to re-derive
# the four above; this one is added here because 184-VERIFICATION.md gap
# 4 and 184-REVIEW.md WR-01 found `_CALIBRATION_CHAIN_FLAGS` above
# STRUCTURALLY BLIND to a +7 false-positive movement: every one of the
# six analyses already had at least one malformed block both before and
# after the 37fea87 regression, so the binary flag stayed saturated at 1
# throughout and `--self-test` stayed green over a regression that
# rejected the project's own template. The value below is NOT re-derived
# here — it is the committed tests/quality-fixtures-v8.7/
# calibration-v8.6-corpus.tsv `malformed_chain_blocks` column, which is
# also exactly what the pre-phase base 1f71211 produces (measured,
# 184-04-PLAN.md M-1), so this pins an EXISTING measured value rather
# than deriving a new one. Asserted below alongside the three flag
# vectors, with the same named-quantity failure-message shape (not a
# bare `assert`, which `python3 -O` strips) — INJ-1 in
# 184-04-PLAN.md M-4 is the injection that proves it load-bearing:
# re-anchoring `_GT_HEAD_RE` fires this assertion in addition to the six
# fixture mismatches it also causes. `_CALIBRATION_CHAIN_FLAGS` above is
# left exactly as it is under D-09's leave-alone branch: the corrected
# predicate reproduces `[1, 1, 1, 1, 1, 1]` exactly, the flag vector did
# not move, only the numeric vector needed a more sensitive assertion.
# Phase 185 (DETECT-04) must treat this constant as an input to verify
# against its own full re-derivation, not a result to trust — the same
# standing instruction the other four constants carry.
_CALIBRATION_MALFORMED_CHAIN_BLOCKS = [2, 2, 2, 2, 3, 3]

# Verdict-axis re-derivation (Phase 185, DETECT-04, measured 2026-07-27
# against commit 846ff2e): `_CALIBRATION_NONCONFORMING_VERDICT_CELLS` is a
# sixth `_CALIBRATION_*` constant, added by user decision D-01. It is the
# corrected-check recomputation measured this phase — re-run
# `--detect-defects tests/quality-baseline-v8.7/analyses` over the six
# frozen analyses and read column 6 (`nonconforming_verdict_cells`) in
# `_CALIBRATION_ANALYSIS_ORDER`; the result reproduces [13, 8, 10, 8, 7,
# 15] exactly. The OLD value it replaces is the pre-DETECT-02 column
# [13, 8, 10, 8, 7, 4] committed in
# tests/quality-fixtures-v8.7/calibration-v8.6-corpus.tsv — MOVED on
# condB-P3 only, 4 to 15 nonconforming Verdict cells out of 15 total, once
# the corrected `_verdict_conforms` (DETECT-02) is applied.
#
# `_CALIBRATION_VERDICT_FLAGS` below is STRUCTURALLY BLIND to this
# movement: `verdict_flag` on condB-P3 stayed saturated at 1 both before
# and after, because 4-of-15 nonconforming was already nonzero and cannot
# register a change to a already-tripped binary. This is the same
# blindness class that 184-VERIFICATION.md gap 4 and 184-REVIEW.md WR-01
# found on the chain axis (see `_CALIBRATION_MALFORMED_CHAIN_BLOCKS`
# above) and fixed the same way: pin a numeric sibling constant next to
# the saturated binary flag, asserted below alongside the other four
# vectors with the same named-quantity failure-message shape (not a bare
# `assert`, which `python3 -O` strips — this file contains zero live
# ones and must continue to). Load-bearing proof: splicing the
# pre-DETECT-02 `_verdict_conforms` body (recovered from `git show
# a30746d~1`) into HEAD fires this assertion (expected [13, 8, 10, 8, 7,
# 15], got [13, 8, 10, 8, 7, 4]) under both `python3` and `python3 -O`,
# while `_CALIBRATION_VERDICT_FLAGS` stays green throughout — that
# asymmetry is the proof the binary alone could not have caught the
# inversion (INJ-V-HIST, recorded in 185-01-SUMMARY.md).
_CALIBRATION_NONCONFORMING_VERDICT_CELLS = [13, 8, 10, 8, 7, 15]


def _defect_numeric_fields(record: dict) -> dict:
    return {k: record[k] for k in _EXPECTED_CONFORMANT_RECORD}


def _selftest_defects() -> bool:
    """D-18 item 7: fixtures, structural edges, and the pinned D-19 corpus vector.

    A conformant fixture must report zero on all three families; a
    deliberately defective fixture must report non-zero on all three, with
    every one of the nine numeric fields pinned. Three structural
    sub-assertions pin the corpus shapes most likely to break under a
    future edit: one-hash heading depth, an appendix after section 6, and a
    document missing section 4 raising rather than scoring clean. Finally,
    the detector's observed per-document rollups over the six frozen
    analyses are pinned against the committed calibration TSV (D-19).
    """
    ok = True

    conformant_text = _DEFECT_FIXTURE_CONFORMANT.read_text(encoding="utf-8")
    defective_text = _DEFECT_FIXTURE_DEFECTIVE.read_text(encoding="utf-8")

    try:
        conformant_record = detect_defects(conformant_text, "analyses-conformant")
    except Exception as exc:  # noqa: BLE001
        print(
            f"self-test FAIL: defects conformant fixture raised unexpectedly: {exc!r}",
            file=sys.stderr,
        )
        return False
    got = _defect_numeric_fields(conformant_record)
    if got != _EXPECTED_CONFORMANT_RECORD:
        print(
            f"self-test FAIL: defects conformant record expected "
            f"{_EXPECTED_CONFORMANT_RECORD!r}, got {got!r}",
            file=sys.stderr,
        )
        ok = False

    try:
        defective_record = detect_defects(defective_text, "analyses-defective")
    except Exception as exc:  # noqa: BLE001
        print(
            f"self-test FAIL: defects defective fixture raised unexpectedly: {exc!r}",
            file=sys.stderr,
        )
        return False
    got_d = _defect_numeric_fields(defective_record)
    if got_d != _EXPECTED_DEFECTIVE_RECORD:
        print(
            f"self-test FAIL: defects defective record expected "
            f"{_EXPECTED_DEFECTIVE_RECORD!r}, got {got_d!r}",
            file=sys.stderr,
        )
        ok = False

    # Structural sub-assertion: one-hash heading depth resolves identically.
    one_hash_text = re.sub(r"^## (\d+\.)", r"# \1", conformant_text, flags=re.MULTILINE)
    try:
        one_hash_record = detect_defects(one_hash_text, "analyses-conformant-one-hash")
    except Exception as exc:  # noqa: BLE001
        print(
            f"self-test FAIL: defects one-hash-depth variant raised unexpectedly: {exc!r}",
            file=sys.stderr,
        )
        ok = False
    else:
        if _defect_numeric_fields(one_hash_record) != _EXPECTED_CONFORMANT_RECORD:
            print(
                "self-test FAIL: defects one-hash-depth variant record differs from "
                "the two-hash original",
                file=sys.stderr,
            )
            ok = False

    # Structural sub-assertion: an appendix after section 6 does not change the record.
    appendix_text = (
        conformant_text
        + "\n\n## Appendix: Fixture Appendix\n\n"
        + "Fixture appendix content that must not affect the record.\n"
    )
    try:
        appendix_record = detect_defects(appendix_text, "analyses-conformant-appendix")
    except Exception as exc:  # noqa: BLE001
        print(
            f"self-test FAIL: defects appendix variant raised unexpectedly: {exc!r}",
            file=sys.stderr,
        )
        ok = False
    else:
        if _defect_numeric_fields(appendix_record) != _EXPECTED_CONFORMANT_RECORD:
            print(
                "self-test FAIL: defects appendix variant record differs from the "
                "no-appendix original",
                file=sys.stderr,
            )
            ok = False

    # Structural sub-assertion: a document missing section 4 entirely raises
    # the named section-resolution exception rather than reporting zero
    # malformed chains.
    section4_start = defective_text.index("## 4. Derivation Chains")
    section5_start = defective_text.index("## 5. Abandoned Reasoning")
    missing_section4_text = defective_text[:section4_start] + defective_text[section5_start:]
    try:
        detect_defects(missing_section4_text, "analyses-defective-missing-section4")
    except SectionResolutionError:
        pass
    except Exception as exc:  # noqa: BLE001
        print(
            f"self-test FAIL: defects missing-section-4 variant raised the wrong "
            f"exception type: {exc!r}",
            file=sys.stderr,
        )
        ok = False
    else:
        print(
            "self-test FAIL: defects missing-section-4 variant did not raise — a "
            "document the parser cannot read must fail loudly, never score clean",
            file=sys.stderr,
        )
        ok = False

    # D-19: the pinned observed calibration vector over the six frozen
    # analyses, reproducing the three document-level rollups committed in
    # tests/quality-fixtures-v8.7/calibration-v8.6-corpus.tsv.
    corpus_dir = BASELINE_DIR / "analyses"
    corpus_files = sorted(corpus_dir.glob("*.md"))
    corpus_ids = [f.stem for f in corpus_files]
    if corpus_ids != list(_CALIBRATION_ANALYSIS_ORDER):
        print(
            f"self-test FAIL: defects calibration corpus file set changed — "
            f"expected {_CALIBRATION_ANALYSIS_ORDER!r}, got {corpus_ids!r}",
            file=sys.stderr,
        )
        ok = False
    else:
        untraced_flags: list[int] = []
        verdict_flags: list[int] = []
        chain_flags: list[int] = []
        malformed_chain_blocks: list[int] = []
        nonconforming_verdict_cells: list[int] = []
        calibration_crashed = False
        for f in corpus_files:
            try:
                rec = detect_defects(f.read_text(encoding="utf-8"), f.stem)
            except Exception as exc:  # noqa: BLE001
                print(
                    f"self-test FAIL: defects calibration corpus raised "
                    f"unexpectedly on {f}: {exc!r}",
                    file=sys.stderr,
                )
                ok = False
                calibration_crashed = True
                break
            untraced_flags.append(rec["untraced_flag"])
            verdict_flags.append(rec["verdict_flag"])
            chain_flags.append(rec["chain_flag"])
            malformed_chain_blocks.append(rec["malformed_chain_blocks"])
            nonconforming_verdict_cells.append(rec["nonconforming_verdict_cells"])
        if not calibration_crashed:
            if untraced_flags != _CALIBRATION_UNTRACED_FLAGS:
                print(
                    f"self-test FAIL: defects calibration untraced_flag vector "
                    f"expected {_CALIBRATION_UNTRACED_FLAGS!r}, got {untraced_flags!r}",
                    file=sys.stderr,
                )
                ok = False
            if verdict_flags != _CALIBRATION_VERDICT_FLAGS:
                print(
                    f"self-test FAIL: defects calibration verdict_flag vector "
                    f"expected {_CALIBRATION_VERDICT_FLAGS!r}, got {verdict_flags!r}",
                    file=sys.stderr,
                )
                ok = False
            if chain_flags != _CALIBRATION_CHAIN_FLAGS:
                print(
                    f"self-test FAIL: defects calibration chain_flag vector "
                    f"expected {_CALIBRATION_CHAIN_FLAGS!r}, got {chain_flags!r}",
                    file=sys.stderr,
                )
                ok = False
            if malformed_chain_blocks != _CALIBRATION_MALFORMED_CHAIN_BLOCKS:
                print(
                    f"self-test FAIL: defects calibration malformed_chain_blocks "
                    f"vector expected {_CALIBRATION_MALFORMED_CHAIN_BLOCKS!r}, "
                    f"got {malformed_chain_blocks!r}",
                    file=sys.stderr,
                )
                ok = False
            if nonconforming_verdict_cells != _CALIBRATION_NONCONFORMING_VERDICT_CELLS:
                print(
                    f"self-test FAIL: defects calibration nonconforming_verdict_cells vector "
                    f"expected {_CALIBRATION_NONCONFORMING_VERDICT_CELLS!r}, "
                    f"got {nonconforming_verdict_cells!r}",
                    file=sys.stderr,
                )
                ok = False

    return ok


# ---------------------------------------------------------------------------
# DETECT-01 (Phase 182): the D-18 contract-pin red-carry mechanism.
#
# `_verdict_conforms` and `_chain_block_well_formed` are inverted relative to
# `shared/spine/references/output-template.md` and
# `shared/spine/references/validation-rubric.md` (settled at v8.13 milestone
# open, PROJECT.md Key Decisions 2026-07-27 — the templates are canonical,
# the detector is the outlier). This phase pins that mismatch as fixtures and
# a self-test item BEFORE either production function changes, so a later fix
# is provably a fix and not a number-chasing edit. See
# `.planning/phases/182-pin-the-defect-in-failing-tests/182-01-PLAN.md` for
# the full pre-registered expectation table.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ContractFixture:
    """A single pre-registered D-18 contract fixture (DETECT-01, Phase 182).

    ``expected`` is the contract-prescribed result (``True``/``False``), or
    ``None`` when the fixture is observation-only and Phase 182 deliberately
    does not assert a contract expectation (DETECT-02 must decide and
    document that treatment). ``owner`` names the requirement that owns the
    current mismatch, or ``None`` for a GREEN-GUARD row today's code already
    gets right. ``verbatim_from`` is a repo-relative path whose content must
    literally contain ``text`` — proven by Guard A in
    `_selftest_contract_pin`. DETECT-06 (Phase 187) replaces this literal-copy
    check with runtime extraction from the same file.
    """

    id: str
    kind: str  # "verdict" or "chain"
    text: str
    expected: bool | None
    owner: str | None
    source: str
    verbatim_from: str | None


_CONTRACT_FIXTURES: tuple[ContractFixture, ...] = (
    ContractFixture(
        id="V-ACCEPT-EMDASH",
        kind="verdict",
        text="Accept — survives P2 challenge; physical-law backed by GT-1",
        expected=True,
        owner="DETECT-02",
        source=(
            "output-template.md line 69, verbatim — the parenthesised Accept "
            "example in the Verdict Vocabulary bullet. Guarded by DETECT-06 "
            "(Phase 187) runtime extraction (habitat mode quoted-eg), which "
            "checks this literal against the live template at self-test time "
            "rather than trusting it as a static copy."
        ),
        verbatim_from="shared/spine/references/output-template.md",
    ),
    ContractFixture(
        id="V-ACCEPT-EMDASH-BOLD",
        kind="verdict",
        text="**Accept — survives P2 challenge; physical-law backed by GT-1**",
        expected=True,
        owner="DETECT-02",
        source=(
            "output-template.md line 69's parenthesised example wrapped in "
            "double asterisks — criterion 1 requires the bold form."
        ),
        verbatim_from=None,
    ),
    ContractFixture(
        id="V-CHALLENGE-EMDASH",
        kind="verdict",
        text="Challenge — vendor benchmark unverified, flagged GT-5?",
        expected=True,
        owner="DETECT-02",
        source=(
            "output-template.md line 70, verbatim — the parenthesised "
            "Challenge example. Guarded by DETECT-06 (Phase 187) runtime "
            "extraction (habitat mode quoted-eg), which checks this literal "
            "against the live template at self-test time rather than "
            "trusting it as a static copy."
        ),
        verbatim_from="shared/spine/references/output-template.md",
    ),
    ContractFixture(
        id="V-DISCARD-EMDASH-BOLD",
        kind="verdict",
        text="**Discard — contradicted by GT-2, no longer load-bearing**",
        expected=True,
        owner="DETECT-02",
        source="output-template.md line 71's parenthesised example wrapped in double asterisks",
        verbatim_from=None,
    ),
    ContractFixture(
        id="V-BARE-TOKEN",
        kind="verdict",
        text="Accept",
        expected=False,
        owner="DETECT-02",
        source=(
            "validation-rubric.md Criterion 2 Rigorous names the bare token "
            "alone as the defect; this is the Q-P2-run1 cell shape."
        ),
        verbatim_from=None,
    ),
    ContractFixture(
        id="V-BARE-TOKEN-BOLD",
        kind="verdict",
        text="**Challenge**",
        expected=False,
        owner="DETECT-02",
        source=(
            "validation-rubric.md Criterion 2 Rigorous's named defect, the "
            "bolded Q-P2-run1 cell shape."
        ),
        verbatim_from=None,
    ),
    ContractFixture(
        id="C-SINGLE-LINE",
        kind="chain",
        text=(
            "GT-1 + GT-2 → admission control, not worker count, is the "
            "binding limit → adding workers will not raise throughput"
        ),
        expected=True,
        owner=None,
        source="constructed; Phase 184 criterion 4 (single-line form must survive)",
        verbatim_from=None,
    ),
    ContractFixture(
        id="C-TEMPLATE-C1",
        kind="chain",
        text=(
            "### Conclusion C1: [Conclusion text]\n"
            "\n"
            "GT-N ([brief fact label, source]) + GT-M ([brief fact label, source])\n"
            "→ [intermediate claim — a new inference statable from combining "
            "GT-N and GT-M but from neither alone]\n"
            "→ [conclusion — the claim this chain establishes]"
        ),
        expected=True,
        owner="DETECT-03",
        source=(
            "output-template.md lines 133-137, verbatim — the template's own "
            "canonical worked example (criterion 3). Guarded by DETECT-06 "
            "(Phase 187) runtime extraction (habitat mode heading-block), "
            "which checks this literal against the live template at "
            "self-test time rather than trusting it as a static copy."
        ),
        verbatim_from="shared/spine/references/output-template.md",
    ),
    ContractFixture(
        id="C-TEMPLATE-FORMAT",
        kind="chain",
        text="GT-N + GT-M → [intermediate claim] → [conclusion]",
        expected=True,
        owner="DETECT-03",
        source=(
            "output-template.md line 108, verbatim — the fenced chain-format "
            "block. Its single-line form is deliberate: it isolates the "
            "placeholder-identifier axis from the multi-line axis. Guarded "
            "by DETECT-06 (Phase 187) runtime extraction (habitat mode "
            "fenced-block), which checks this literal against the live "
            "template at self-test time rather than trusting it as a static "
            "copy."
        ),
        verbatim_from="shared/spine/references/output-template.md",
    ),
    ContractFixture(
        id="C-MULTILINE-DIGITS",
        kind="chain",
        text=(
            "GT-1 (measured throughput, bench log) + GT-2 (queue depth, spec)\n"
            "→ admission control, not worker count, is the binding limit\n"
            "→ adding workers will not raise throughput"
        ),
        expected=True,
        owner="DETECT-03",
        source="constructed three-line chain in the template's shape",
        verbatim_from=None,
    ),
    ContractFixture(
        id="C-TEMPLATE-TRADEOFF",
        kind="chain",
        text=(
            "GT-2 + GT-5 (criteria facts) → weighted totals: B=82 > A=64, "
            "driven by reliability×warranty → recommend B"
        ),
        expected=True,
        owner=None,
        source=(
            "output-template.md line 123, verbatim — the backtick-quoted "
            "trade-off example. Guarded by DETECT-06 (Phase 187) runtime "
            "extraction (habitat mode backtick-span), which checks this "
            "literal against the live template at self-test time rather "
            "than trusting it as a static copy."
        ),
        verbatim_from="shared/spine/references/output-template.md",
    ),
    ContractFixture(
        id="C-NO-INTERMEDIATE",
        kind="chain",
        text="GT-1 + GT-2 → adding workers will not raise throughput",
        expected=False,
        owner=None,
        source=(
            "constructed negative; Phase 184 criterion 3 — this fix must not "
            "become a blanket pass."
        ),
        verbatim_from=None,
    ),
    ContractFixture(
        id="C-NO-INTERMEDIATE-MULTILINE",
        kind="chain",
        text=(
            "GT-1 (measured throughput, bench log) + GT-2 (queue depth, spec)\n"
            "→ adding workers will not raise throughput"
        ),
        expected=False,
        owner=None,
        source=(
            "constructed negative; the sentinel a block-level matcher is "
            "most likely to break."
        ),
        verbatim_from=None,
    ),
    ContractFixture(
        id="C-JOIN-FALSE-FUSE",
        kind="chain",
        text="GT-1 → conclusion A\nGT-2 → conclusion B",
        expected=False,
        owner=None,
        source=(
            "constructed negative; Phase 184 criterion 3 — two unrelated "
            "single-arrow chains fused into one block by an unbounded join "
            "must not wrongly score as one two-arrow chain (D-12)."
        ),
        verbatim_from=None,
    ),
    ContractFixture(
        id="C-JOIN-PROSE-ARROW",
        kind="chain",
        text="GT-1 → conclusion A\n**Confidence:** rises → HIGH once verified",
        expected=False,
        owner=None,
        source=(
            "constructed negative; Phase 184 criterion 3 — a defective "
            "one-arrow chain followed by a prose line that itself contains "
            "an arrow must not be absorbed into the join (D-12)."
        ),
        verbatim_from=None,
    ),
    ContractFixture(
        id="C-JOIN-ARROW-BULLET",
        kind="chain",
        text=(
            "GT-1 (single fact) -> this is the only hop, no second arrow to "
            "close the claim.\n-> Next steps: verify assumption before "
            "deploying."
        ),
        expected=False,
        owner=None,
        source=(
            "constructed negative from 184-REVIEW.md CR-01 counter-example "
            "1; its second line DOES begin with an arrow, the absorption "
            "branch neither C-JOIN-FALSE-FUSE nor C-JOIN-PROSE-ARROW "
            "reaches (WR-01); pinned by the head-arrow guard — removing "
            "that guard flips it."
        ),
        verbatim_from=None,
    ),
    ContractFixture(
        id="C-JOIN-ARROW-NEWGT",
        kind="chain",
        text=(
            "GT-1 (bench numbers) -> partial claim about GT-1 only, no "
            "second hop here\n-> GT-9 (unrelated fact) is what actually "
            "explains the real conclusion"
        ),
        expected=False,
        owner=None,
        source=(
            "constructed negative from 184-REVIEW.md CR-01 counter-example "
            "3; its second line DOES begin with an arrow, the absorption "
            "branch neither C-JOIN-FALSE-FUSE nor C-JOIN-PROSE-ARROW "
            "reaches (WR-01); pinned by the head-arrow guard — removing "
            "that guard flips it."
        ),
        verbatim_from=None,
    ),
    ContractFixture(
        id="C-RENDER-EXAMPLE-PREFIX",
        kind="chain",
        text=(
            'Example: `GT-2 + GT-5 (criteria facts) → weighted totals: B=82 > A=64, '
            'driven by reliability×warranty → recommend B`. The full matrix stays in '
            "the technique's own output — this subsection carries only the single "
            'collapsed chain, never the matrix re-expressed row-by-row (that would '
            'violate the one-chain-per-conclusion rule above). An exact tie between '
            'weighted totals still resolves to a single named recommended option; a '
            'tie must not produce a multi-option chain endpoint. **Exact-tie tiebreak '
            '(deterministic):** on an exact tie, prefer the option with fewer `GT-N?` '
            '(unverified) inputs among its winning criteria; if still tied, name both '
            'totals in the chain intermediate but select the first-listed option as '
            'the chain endpoint, and flag the tie explicitly in the Conclusion '
            "section's confidence line."
        ),
        expected=True,
        owner="DETECT-03",
        source=(
            "output-template.md line 123, the WHOLE stripped physical line — "
            "Example: lead-in and both backticks intact, not the "
            "de-contextualised substring C-TEMPLATE-TRADEOFF lifts. Certifies "
            "ROADMAP criterion 2 and DETECT-03 acceptance clause A against the "
            "template as it actually reads (184-VERIFICATION.md gap 2, "
            "184-REVIEW.md WR-03); this row and Guard A's substring check now "
            "cover the same characters, superseding C-TEMPLATE-TRADEOFF for "
            "behavioural purposes without editing it. False at 37fea87 (the `^` "
            "anchor rejected it), True at 1f71211 and after this plan; pinned by "
            "INJ-1. Guarded by DETECT-06 (Phase 187) runtime extraction "
            "(habitat mode whole-physical-line), which checks this literal "
            "against the live template at self-test time rather than "
            "trusting it as a static copy."
        ),
        verbatim_from="shared/spine/references/output-template.md",
    ),
    ContractFixture(
        id="C-RENDER-SECONDORDER-PREFIX",
        kind="chain",
        text=(
            'Example: `GT-1 → first-order conclusion →[2nd] flag-config surface grows '
            '→[3rd] flag debt accumulates (contradicts GT-4 → back to P2)`. The order '
            "marks (`[2nd]`, `[3rd]`) make the extension's sequence legible. A "
            'contradicting effect routes the conclusion back to Phase 2 — never '
            'directly to Phase 3 or past Phase 2. A pass that surfaces no '
            'non-contradicting downstream effect leaves the parent chain unextended — '
            'a clean no-op, not an error.'
        ),
        expected=True,
        owner="DETECT-03",
        source=(
            "output-template.md's second-order-extension Example: line, the "
            "WHOLE stripped physical line — same ownership and treatment as "
            "C-RENDER-EXAMPLE-PREFIX above (ROADMAP criterion 2, DETECT-03 "
            "acceptance clause A). False at 37fea87, True at 1f71211 and after "
            "this plan; pinned by INJ-1. Guarded by DETECT-06 (Phase 187) "
            "runtime extraction (habitat mode whole-physical-line), which "
            "checks this literal against the live template at self-test "
            "time rather than trusting it as a static copy."
        ),
        verbatim_from="shared/spine/references/output-template.md",
    ),
    ContractFixture(
        id="C-RENDER-BACKTICK",
        kind="chain",
        text=(
            '`GT-1 (Amdahl) + GT-4 (RTT is encoding-invariant) → the law-permitted '
            'ceiling on latency improvement from any transport change is exactly the '
            'fraction of the latency budget currently spent on encoding and connection '
            'management → everything else (RTT, queuing, DB, downstream fan-out, cold '
            'starts, GC pauses) is untouched by gRPC.`'
        ),
        expected=True,
        owner=None,
        source=(
            "tests/quality-baseline-v8.7/analyses/condA-P1.md line 93, the "
            "backtick-wrapped condA-P1 DC-2 rendering the frozen corpus actually "
            "uses (184-VERIFICATION.md gap 4, 184-REVIEW.md CR-01). False at "
            "37fea87, True at 1f71211 and after this plan; pinned by INJ-1."
        ),
        verbatim_from="tests/quality-baseline-v8.7/analyses/condA-P1.md",
    ),
    ContractFixture(
        id="C-RENDER-BLOCKQUOTE-BOLD",
        kind="chain",
        text=(
            '> **GT-1 + GT-2 + GT-4 → attic saves ≈ 107 W/K → GT-5 (attic ≈ '
            '£500–1,000) → ≈ 3–6 W/K per £100 spent**'
        ),
        expected=True,
        owner=None,
        source=(
            "tests/quality-baseline-v8.7/analyses/condA-P3.md line 71, the "
            "blockquote+bold condA-P3 rendering the frozen corpus actually uses "
            "(184-VERIFICATION.md gap 4, 184-REVIEW.md CR-01). False at 37fea87, "
            "True at 1f71211 and after this plan; pinned by INJ-1."
        ),
        verbatim_from="tests/quality-baseline-v8.7/analyses/condA-P3.md",
    ),
    ContractFixture(
        id="C-RENDER-LIST-ITEM",
        kind="chain",
        text="- GT-1 (bench) -> intermediate -> conclusion",
        expected=True,
        owner=None,
        source=(
            "constructed list-item rendering, one of the CR-01 table's "
            "renderings the pre-existing 11 chain fixtures structurally cannot "
            "see (every one begins at column 0 with a bare GT- token). False at "
            "37fea87, True at 1f71211 and after this plan; pinned by INJ-1."
        ),
        verbatim_from=None,
    ),
    ContractFixture(
        id="C-WRAP-HEAD-ARROW",
        kind="chain",
        text="GT-1 (fact) → intermediate claim\n→ therefore the conclusion holds",
        expected=True,
        owner=None,
        source=(
            "184-REVIEW.md WR-04: a legitimate line-wrapped chain whose head "
            "carries the first arrow and whose continuation carries the second "
            "— a normal rendering of the template's own `### Conclusion C1:` "
            "form. Unpinned in either direction before this plan. False / True "
            "/ False across 1f71211 / b50e8e4 / 37fea87 (184-01 fixed it, "
            "184-03's head-arrow guard re-broke it); True after this plan, "
            "pinned by INJ-6 (restoring the retired guard flips this fixture "
            "and only this one)."
        ),
        verbatim_from=None,
    ),
    ContractFixture(
        id="C-WRAP-BULLETED",
        kind="chain",
        text="- GT-1 + GT-2\n  -> intermediate\n  -> conclusion",
        expected=True,
        owner=None,
        source=(
            "the bulleted, indented canonical multi-line form — a literal "
            "instance of ROADMAP criterion 1's own wording (GT inputs joined "
            "by +, two arrow-led segments, line breaks between them). False / "
            "True / False across 1f71211 / b50e8e4 / 37fea87; True after this "
            "plan, pinned by INJ-1."
        ),
        verbatim_from=None,
    ),
    ContractFixture(
        id="C-JOIN-ARROW-BULLET-WRAPPED",
        kind="chain",
        text=(
            "GT-1 (single fact)\n"
            "-> this is the only hop, no second arrow to close the claim.\n"
            "-> Next steps: verify assumption before deploying."
        ),
        expected=False,
        owner=None,
        source=(
            "C-JOIN-ARROW-BULLET (CE1) reformatted — the first arrow moved from "
            "the head onto its own line, identical content and malformation. "
            "184-REVIEW.md CR-03/184-VERIFICATION.md gap 1: the 184-03 "
            "head-arrow guard was defeated by this reformatting alone (True at "
            "37fea87). False at 1f71211 and after this plan; pinned by INJ-2 "
            "(the sentence-closed refusal, tracked at the continuation level)."
        ),
        verbatim_from=None,
    ),
    ContractFixture(
        id="C-JOIN-ARROW-NEWGT-WRAPPED",
        kind="chain",
        text=(
            "GT-1 (bench numbers)\n"
            "-> partial claim about GT-1 only, no second hop here\n"
            "-> GT-9 (unrelated fact) is what actually explains the real "
            "conclusion"
        ),
        expected=False,
        owner=None,
        source=(
            "C-JOIN-ARROW-NEWGT (CE3) reformatted — the first arrow moved off "
            "the head. True at 37fea87 (blanket pass survives the "
            "reformatting); False at 1f71211 and after this plan; pinned by "
            "INJ-3 (the arrow-led-GT refusal)."
        ),
        verbatim_from=None,
    ),
    ContractFixture(
        id="C-JOIN-ARROW-TABLEROW",
        kind="chain",
        text=(
            "GT-1 -> intermediate only, single hop\n"
            "-> | some other column | another column |"
        ),
        expected=False,
        owner=None,
        source=(
            "the fourth original CR-01 counter-example as written "
            "(184-REVIEW-preclosure.md): a markdown table row absorbed through "
            "the arrow-led rule. True at b50e8e4 (never pinned, WR-02); False "
            "at 1f71211, at 37fea87 (the head-arrow guard incidentally closed "
            "it) and after this plan; pinned by INJ-4 (the table-row refusal)."
        ),
        verbatim_from=None,
    ),
    ContractFixture(
        id="C-JOIN-ARROW-TABLEROW-WRAPPED",
        kind="chain",
        text=(
            "GT-1\n"
            "-> intermediate only, single hop\n"
            "-> | some other column | another column |"
        ),
        expected=False,
        owner=None,
        source=(
            "the fourth counter-example reformatted — the first arrow moved "
            "off the head. True at b50e8e4 and at 37fea87 (the head-arrow "
            "guard does not reach a headless-of-arrow candidate, so this "
            "reformatting defeats it too); False at 1f71211 and after this "
            "plan; pinned by INJ-4."
        ),
        verbatim_from=None,
    ),
    ContractFixture(
        id="C-JOIN-ORDERMARK-NEWGT",
        kind="chain",
        text=(
            "GT-1 → first-order conclusion\n"
            "→[2nd] GT-9 (another fact) drives the rest"
        ),
        expected=False,
        owner=None,
        source=(
            "an order-marked continuation that leads with its own GT "
            "identifier — the single row that pins the optional bracket group "
            "inside _ARROW_LED_GT_RE (as opposed to the legitimate "
            "`→[2nd] flag-config surface grows` template shape, which the same "
            "refusal must NOT reject). True at b50e8e4; False at 1f71211, at "
            "37fea87 and after this plan; pinned by INJ-3 (the whole refusal) "
            "and INJ-5 (the bracket group specifically — removing only the "
            "bracket group flips this fixture and only this one)."
        ),
        verbatim_from=None,
    ),
    ContractFixture(
        id="C-JOIN-ARROW-BOLDCLOSE",
        kind="chain",
        text=(
            "**GT-1 → conclusion one is finished right here.**\n"
            "→ this note is actually a totally separate topic and should "
            "never fuse in"
        ),
        expected=False,
        owner="DETECT-03",
        source=(
            "184-REVIEW.md CR-01 — a one-hop claim whose sentence-terminal "
            "period sits BEHIND a markdown bold closer. True at b50e8e4 and "
            "after 184-04 (the raw sentence-end test cannot see the close "
            "through the `**`, so the unrelated next line fuses into a fake "
            "two-hop chain); False at 1f71211, at 37fea87 and after "
            "184-06. The unwrapped control returns False at every revision, "
            "isolating the closers as the entire cause. Pinned by INJ-7 "
            "(removing the trailing-closer strip)."
        ),
        verbatim_from=None,
    ),
    ContractFixture(
        id="C-WRAP-GT-QMARK",
        kind="chain",
        text=(
            "GT-2 + GT-5?\n"
            "→ intermediate claim here\n"
            "→ final conclusion here"
        ),
        expected=True,
        owner="DETECT-03",
        source=(
            "184-REVIEW.md CR-02 — a legitimate wrapped chain whose head "
            "ends in a GT token's OWN `?` unverified marker, which the raw "
            "sentence-end test read as sentence-terminal and so refused the "
            "real continuations. False at 1f71211 and after 184-04, True at "
            "b50e8e4, at 37fea87 and after 184-06. NOT a regression against "
            "the pre-phase base (False there too) but previously undisclosed "
            "— it was not among the RISK-A/B/C residuals. Pinned by INJ-8 "
            "(removing the GT-token mask)."
        ),
        verbatim_from=None,
    ),
    ContractFixture(
        id="V-OBS-ENDASH",
        kind="verdict",
        text="Accept – survives challenge",
        expected=False,
        owner="DETECT-02",
        source=(
            "en-dash separator — decided by P183-D1 (Phase 183): only "
            "U+2014 EM DASH separates the token from the justification, "
            "because both canonical sources name only the em-dash and a "
            "267-cell census of the frozen corpora found zero en-dash "
            "separators in use, so this treatment costs no recorded figure."
        ),
        verbatim_from=None,
    ),
    ContractFixture(
        id="V-OBS-HYPHEN",
        kind="verdict",
        text="Accept - survives challenge",
        expected=False,
        owner="DETECT-02",
        source=(
            "ASCII hyphen separator — decided by P183-D1 (Phase 183): only "
            "U+2014 EM DASH separates the token from the justification, "
            "because both canonical sources name only the em-dash and a "
            "267-cell census of the frozen corpora found zero hyphen "
            "separators in use, so this treatment costs no recorded figure."
        ),
        verbatim_from=None,
    ),
    ContractFixture(
        id="V-OBS-EMPTY-AFTER-DASH",
        kind="verdict",
        text="Accept — ",
        expected=False,
        owner="DETECT-02",
        source=(
            "justification empty after the em-dash — decided by P183-D2 "
            "(Phase 183): a cell carrying the token and the separator but "
            "no non-whitespace character after it does not conform, "
            "because an empty remainder carries no reasoning, which is the "
            "whole purpose of the em-dash clause."
        ),
        verbatim_from=None,
    ),
    ContractFixture(
        id="V-RUBRIC-CRIT2-EMDASH",
        kind="verdict",
        text="Accept \u2014 rubric-derived vocabulary, not transcribed",
        expected=True,
        owner=None,
        source=(
            "constructed from validation-rubric.md Criterion 2's derived "
            "Verdict vocabulary (DETECT-06, Phase 187): the leading token, "
            "capitalised, followed by the em-dash-plus-justification form "
            "Criterion 2 prescribes. verbatim_from is None because this "
            "cell is built from a runtime derivation, not lifted verbatim "
            "— the same reason V-BARE-TOKEN and V-BARE-TOKEN-BOLD already "
            "carry None."
        ),
        verbatim_from=None,
    ),
    ContractFixture(
        id="V-RUBRIC-CRIT2-BARE",
        kind="verdict",
        text="Accept",
        expected=False,
        owner=None,
        source=(
            "constructed negative sibling of V-RUBRIC-CRIT2-EMDASH: the "
            "same derived leading token alone, with no em-dash and no "
            "justification. Mandatory, not optional — a positive-only "
            "fixture is satisfiable by a blanket-pass _verdict_conforms, "
            "the failure class this repo hit three separate times across "
            "Phase 184's rounds, each time by a different mechanism. "
            "verbatim_from is None for the same reason as its positive "
            "sibling."
        ),
        verbatim_from=None,
    ),
)


# (i) This registry carries DETECT-01's deliberate red state across the phase
#     boundary; each entry is deleted by the requirement named in its value;
#     when the dict is empty DETECT-01's carry job is done and the fixtures
#     become ordinary assertions.
# (ii) The recorded red run this registry corresponds to lives at
#      tests/detect01-red-run-v8.13.md.
# (iii) The STALE PIN failure detects a COMPLETE fix, not a partial one. It
#      fires only when a pinned fixture's result flips to match its
#      `expected` value. A partial correction leaves the not-yet-flipped
#      entries validly pinned, no STALE PIN fires, and QUAL-01 stays green on
#      a half-corrected check — for example a `_verdict_conforms` that starts
#      accepting "Accept — justification" while still accepting the bare
#      token leaves `V-BARE-TOKEN` (expected False) legitimately pinned; and a
#      `_chain_block_well_formed` that gains the block-level match without a
#      decision on placeholder GT identifiers leaves `C-TEMPLATE-C1`
#      legitimately pinned, the direct consequence of the
#      necessary-but-not-sufficient finding recorded in this plan's
#      pre-registration.
# (iv) Therefore the completeness check for DETECT-02 and DETECT-03 is
#      `contract_pin_strict_report()` exiting 0 — that is the only signal
#      that says an owner's red is fully gone, and Phase 183 and Phase 184
#      must run it, not rely on a green gate.
# (v) A green QUAL-01 while this dict is non-empty means "the carried red is
#     still carried", never "the contract holds".
_DETECT01_PINNED_RED: dict[str, str] = {}


_GT_LETTER_RE = re.compile(r"GT-([A-Z])\b")


def _chain_failure_axes(text: str) -> list[str]:
    """Axis tags explaining why a chain block fails `_chain_block_well_formed`.

    MULTILINE tags a chain spread across several physical lines that would
    match `_CHAIN_FORM_LINE_RE` if joined onto one line — the reason
    `_chain_block_well_formed` moved to a block-level, bounded arrow-led
    join (D-05, D-06).

    This function used to carry a second, independent axis,
    NON-NUMERIC-GT, tagging a chain that only fails because it uses a
    placeholder GT identifier (`GT-N`/`GT-M`) rather than a digit-suffixed
    one. Phase 184 (DETECT-03) decided that question on shape-not-vocabulary
    grounds (D-01): the GT token inside `_CHAIN_FORM_LINE_RE` itself widened
    to accept any alphanumeric identifier, so a placeholder id no longer
    makes a chain fail on its own and the axis is retired — its detection
    branch is removed here, decided away rather than left pending or
    silently deleted, not merely made unreachable.
    """

    def per_line(t: str) -> bool:
        return any(_CHAIN_FORM_LINE_RE.search(line) for line in t.splitlines())

    def joined(t: str) -> bool:
        j = " ".join(line.strip() for line in t.splitlines() if line.strip())
        return bool(_CHAIN_FORM_LINE_RE.search(j))

    def digit_substituted(t: str) -> str:
        seen: list[str] = []

        def repl(m: re.Match) -> str:
            letter = m.group(1)
            if letter not in seen:
                seen.append(letter)
            return f"GT-{seen.index(letter) + 1}"

        return _GT_LETTER_RE.sub(repl, t)

    ds_text = digit_substituted(text)
    ds_per_line = per_line(ds_text)
    ds_joined = joined(ds_text)

    axes: list[str] = []
    if not ds_per_line and ds_joined:
        axes.append("MULTILINE")
    return axes


class _ContractAnchorError(Exception):
    """Raised by `_extract_contract_example` when an anchor in
    `_CONTRACT_EXTRACTION_TABLE` does not resolve to exactly one location in
    its source file — absent, or ambiguous (more than one match) (D-10).
    Carries the anchor, the source file, and a detail string so Guard A's
    mode-1 FAIL can name both the anchor and the file without re-parsing a
    message string.
    """

    def __init__(self, anchor: str, source_file: str, detail: str) -> None:
        self.anchor = anchor
        self.source_file = source_file
        self.detail = detail
        super().__init__(f"anchor {anchor!r} in {source_file}: {detail}")


# D-04: this table's coverage is enumerated, not swept, and the limit is
# real, not hypothetical. It covers exactly the fixtures listed below
# because those are the ones found by importing the module and reading
# `_CONTRACT_FIXTURES` live (D-01) — NOT because every
# `verbatim_from="shared/..."` fixture is guaranteed a row here. An example
# added to `output-template.md` later, with its own new fixture, is NOT
# automatically covered by this table: a new row must be added by hand.
# This has already happened once — `C-RENDER-EXAMPLE-PREFIX` and
# `C-RENDER-SECONDORDER-PREFIX` were added to `_CONTRACT_FIXTURES` after
# `tests/detect01-red-run-v8.13.md` §10 pre-registered a list of five
# template-sourced fixtures, and nothing noticed until 187-CONTEXT.md's D-01
# caught it by re-enumerating live rather than trusting §10's count.
_CONTRACT_EXTRACTION_TABLE: tuple[tuple[str, str, str, str], ...] = (
    (
        "V-ACCEPT-EMDASH",
        "shared/spine/references/output-template.md",
        "quoted-eg",
        "- **Accept**",
    ),
    (
        "V-CHALLENGE-EMDASH",
        "shared/spine/references/output-template.md",
        "quoted-eg",
        "- **Challenge**",
    ),
    (
        "C-TEMPLATE-C1",
        "shared/spine/references/output-template.md",
        "heading-block",
        "### Conclusion C1:",
    ),
    (
        "C-TEMPLATE-FORMAT",
        "shared/spine/references/output-template.md",
        "fenced-block",
        "**Chain format:**",
    ),
    (
        "C-TEMPLATE-TRADEOFF",
        "shared/spine/references/output-template.md",
        "backtick-span",
        "Example: `GT-2",
    ),
    (
        "C-RENDER-EXAMPLE-PREFIX",
        "shared/spine/references/output-template.md",
        "whole-physical-line",
        "Example: `GT-2",
    ),
    (
        "C-RENDER-SECONDORDER-PREFIX",
        "shared/spine/references/output-template.md",
        "whole-physical-line",
        "Example: `GT-1",
    ),
)


# Phase 11 (CONTRACT-01, CONTRACT-02, CONTRACT-04) self-test-only fixtures
# for the emission rendering contract's own worked examples in
# `output-template.md` §4 (chain form), §6 (citation form) and the Verdict
# Vocabulary (current-constraint expiry). These are DELIBERATELY NOT rows
# of `_CONTRACT_EXTRACTION_TABLE` above: that table is the D-18 / DETECT-01
# red-carry surface, paired one-to-one with `_CONTRACT_FIXTURES` and its
# `expected`/`owner` semantics — Item 24's fixtures are new and are not
# red-carry-tracked, so they get their own table rather than being folded
# into that one. The anchors are the bold labels Plan 01 (11-01) authored;
# every row reuses the same `_extract_contract_example` dispatcher above
# (habitat mode `fenced-block`), read at self-test time, never restated as
# a Python literal, so the doc and the control cannot drift (D-04).
_RENDER_CONTRACT_EXTRACTION_TABLE: tuple[tuple[str, str, str, str], ...] = (
    (
        "R-CHAIN-CONFORMING",
        "shared/spine/references/output-template.md",
        "fenced-block",
        "**Conforming — head, then one hop per line:**",
    ),
    (
        "R-CHAIN-WRAPPED",
        "shared/spine/references/output-template.md",
        "fenced-block",
        "**Non-conforming — a hop broken across physical lines:**",
    ),
    (
        "R-CHAIN-NUMBERED",
        "shared/spine/references/output-template.md",
        "fenced-block",
        "**Non-conforming — the same hops rendered as a numbered list:**",
    ),
    (
        "R-CITE-INLINE",
        "shared/spine/references/output-template.md",
        "fenced-block",
        "**Conforming — inline chain citation:**",
    ),
    (
        "R-CITE-LEDGER",
        "shared/spine/references/output-template.md",
        "fenced-block",
        "**Conforming — closure-ledger row:**",
    ),
    (
        "R-CITE-NONE",
        "shared/spine/references/output-template.md",
        "fenced-block",
        "**Non-conforming — a claim naming no chain and quoted by no ledger row:**",
    ),
    (
        "R-VERDICT-EXPIRY",
        "shared/spine/references/output-template.md",
        "fenced-block",
        "**Conforming — a current constraint recording its expiry:**",
    ),
    (
        "R-VERDICT-EXPIRY-BAD",
        "shared/spine/references/output-template.md",
        "fenced-block",
        "**Non-conforming — the expiry hoisted into the token slot:**",
    ),
    (
        "R-HEAD-PROSE-BAD",
        "shared/spine/references/output-template.md",
        "fenced-block",
        "**Non-conforming — an input carrying unparenthesized prose:**",
    ),
    (
        "R-HEAD-CHAINREF",
        "shared/spine/references/output-template.md",
        "fenced-block",
        "**Conforming — the same head with the upstream chain as an input:**",
    ),
    (
        "R-HEAD-ALLCHAIN",
        "shared/spine/references/output-template.md",
        "fenced-block",
        "**Conforming — a chain consuming only upstream conclusions:**",
    ),
    (
        "R-HEAD-PROSE-MID",
        "shared/spine/references/output-template.md",
        "fenced-block",
        "**Non-conforming, and undetected by the form check — the same prose input in a non-final position:**",
    ),
    (
        "R-HEAD-GTHOP-BAD",
        "shared/spine/references/output-template.md",
        "fenced-block",
        "**Non-conforming — a hop beginning with a GT-N identifier:**",
    ),
    (
        "R-HEAD-GTHOP-OK",
        "shared/spine/references/output-template.md",
        "fenced-block",
        "**Conforming — the same hop with the identifier moved off the front:**",
    ),
    (
        "R-HEAD-GTHOP-LATE",
        "shared/spine/references/output-template.md",
        "fenced-block",
        "**Non-conforming, and undetected by the form check — the GT-led hop in a later position:**",
    ),
    (
        "R-HEAD-PERIOD-BAD",
        "shared/spine/references/output-template.md",
        "fenced-block",
        "**Non-conforming — the first hop closing its own sentence:**",
    ),
    (
        "R-HEAD-PERIOD-OK",
        "shared/spine/references/output-template.md",
        "fenced-block",
        "**Conforming — the same chain with the first hop's terminal period removed:**",
    ),
    (
        "R-HEAD-PERIOD-LATE",
        "shared/spine/references/output-template.md",
        "fenced-block",
        "**Non-conforming, and undetected by the form check — the same period moved to a later hop:**",
    ),
    # Phase 14 (LEDGER-03, LEDGER-04): R11's three claim-extraction bounds
    # and R12's caveat-marker rule, pinned as nine worked-example blocks
    # plan 14-02 rendered in output-template.md §6 after `**Caveats.**`.
    (
        "R-CLAIM-LABEL-BARE",
        "shared/spine/references/output-template.md",
        "fenced-block",
        "**Not a claim — a bold lead-in alone on its line, carrying no citation:**",
    ),
    (
        "R-CLAIM-LABEL-INLINE",
        "shared/spine/references/output-template.md",
        "fenced-block",
        "**A claim — the same lead-in carrying its assertion on the same line:**",
    ),
    (
        "R-CLAIM-LABEL-CITED",
        "shared/spine/references/output-template.md",
        "fenced-block",
        "**A claim — the lead-in alone on its line, but carrying its own citation:**",
    ),
    (
        "R-CLAIM-COLON-MID",
        "shared/spine/references/output-template.md",
        "fenced-block",
        "**Not matched at all — a bold span whose colon sits inside it:**",
    ),
    (
        "R-CLAIM-COLON-END",
        "shared/spine/references/output-template.md",
        "fenced-block",
        "**A claim — the same statement with the colon closing the bold span:**",
    ),
    (
        "R-CLAIM-TERSE-DROP",
        "shared/spine/references/output-template.md",
        "fenced-block",
        "**Not a claim — a short list item with no sentence-ending punctuation:**",
    ),
    (
        "R-CLAIM-TERSE-KEEP",
        "shared/spine/references/output-template.md",
        "fenced-block",
        "**A claim — a short list item closing its own sentence:**",
    ),
    (
        "R-CLAIM-CAVEAT-MARKED",
        "shared/spine/references/output-template.md",
        "fenced-block",
        "**Conformant but still untraced — a caveat carrying the flagged-assumption marker:**",
    ),
    (
        "R-CLAIM-CAVEAT-CITED",
        "shared/spine/references/output-template.md",
        "fenced-block",
        "**Conformant and traced — the same caveat citing the chain it qualifies:**",
    ),
)

# Substrings the extracted text for each fixture id MUST contain before any
# detector is consulted (a mode-2 shape guard, mirroring Guard A's split):
# an extraction that silently returned a neighbouring block would otherwise
# risk scoring `False` for the wrong reason and passing vacuously.
#
# The three R-CHAIN-* entries carry a discriminating third needle each
# (IN-04, `11-REVIEW.md`): before this fix all three declared the same
# undiscriminating pair (`"GT-1", "GT-6"`), so a mis-anchored extraction of
# any one into any other still satisfied the guard. Each third needle is
# verified, not eyeballed (extracted fixture text, self-test run 2026-09-01):
# CONFORMING's own three lines join with no inserted line between the
# second and third hop, so `"actual compute\n→ sustained"` spans that exact
# transition and breaks the moment WRAPPED's inserted continuation line
# lands between them — `"\n→ "` alone was tried and rejected here because
# WRAPPED's text ALSO contains two arrow-led lines and therefore also
# contains `"\n→ "`, so it did not discriminate CONFORMING from WRAPPED.
#
# `R-CITE-INLINE` carries the same treatment for the citation pair
# (WR-02, `11-REVIEW-gap-closure.md`): its only needle used to be `"C1"`,
# which is also present in `R-CITE-LEDGER`'s block
# (`- "Move sustained workloads to Fargate" → chain C1 ✓`), so repointing
# its anchor at the ledger block left the self-test GREEN and control
# (f)'s "both accepted forms are proven" proved the ledger form twice and
# the inline form never. `"(chain C1)"` is the inline form's structural
# signature — verified by extraction, not eyeballed (2026-09-01): present
# in the inline block, absent from both the ledger block and the
# no-citation block. The reverse direction was already caught by
# `R-CITE-LEDGER`'s extra `'\"'` needle and `R-CITE-NONE`'s
# `_RENDER_FIXTURE_FORBIDDEN` entry.
#
# `R-HEAD-PROSE-BAD` and `R-HEAD-PROSE-MID` (plan 13-08, BL-01) are the
# same violation in two head positions — trailing and middle — and need to
# discriminate in BOTH directions: `R-HEAD-PROSE-MID`'s needle
# `"+ C2's threshold + GT-12?"` is unique to the middle-position block
# (`R-HEAD-PROSE-BAD` ends its head with `+ C2's threshold` and
# `R-HEAD-CHAINREF` carries `C2 (threshold)`, neither of which contains
# this substring), and `R-HEAD-PROSE-BAD`'s new third needle
# `"+ C2's threshold\n→"` is unique to the trailing-position block — without
# it a mis-anchored extraction returning the new middle-position block
# still satisfies `R-HEAD-PROSE-BAD`'s shape guard, because that block also
# contains the pair's first two needles.
#
# `R-HEAD-GTHOP-BAD` and `R-HEAD-GTHOP-OK` (plan 13-09, BL-02) are the same
# hop differing only in whether it leads with `GT-4`: `"→ GT-4's stated
# duty cycle"` and `"→ the duty cycle stated in GT-4"` each discriminate
# their own block from the other, because a mis-anchored extraction would
# carry the wrong ordering of that clause.
#
# `R-HEAD-GTHOP-BAD` and `R-HEAD-GTHOP-LATE` (plan 13-19, CR-02 fixture
# half) are the same offending hop in two positions — first and last —
# and need to discriminate in BOTH directions, the same shape 13-08 gave
# the PROSE pair. 13-19's original two-needle tuple named neither the hop
# nor its position: round 6 (`13-VERIFICATION-round6.md`, CR-01)
# reproduced its vacuity by deleting the GT-led hop from the fixture
# block entirely, leaving a plainly conforming chain, and `--self-test`
# stayed GREEN — the fixture demonstrated nothing and R9's published
# positional disclosure lost its only evidence. Plan 13-22 (CR-01) is the
# fix: `R-HEAD-GTHOP-LATE`'s new third needle, `"binding one\n→ GT-4's
# stated duty cycle"`, pins the offending hop by the hop that must
# PRECEDE it — the whole measured bound R9 discloses, that two arrow-led
# hops must already have matched before the identifier appears — and is
# unique to the late-position block, and `R-HEAD-GTHOP-BAD`'s third
# needle, `"threshold)\n→ GT-4's stated duty cycle"`, is unique to the
# first-position block. The pair now discriminates in both directions:
# without either needle a mis-anchored extraction returning the wrong
# block would still satisfy the other's shape guard, because both blocks
# share the same head and the same offending hop text.
_RENDER_FIXTURE_SHAPE: dict[str, tuple[str, ...]] = {
    "R-CHAIN-CONFORMING": ("GT-1", "GT-6", "actual compute\n→ sustained"),
    "R-CHAIN-WRAPPED": ("GT-1", "GT-6", "\n  once idle-time billing"),
    "R-CHAIN-NUMBERED": ("GT-1", "GT-6", "\n2. "),
    "R-CITE-INLINE": ("(chain C1)",),
    "R-CITE-LEDGER": ("C1", '"'),
    "R-CITE-NONE": ("Fargate",),
    # Discriminating needles (13-27, IN-03, `13-REVIEW.md`): before this,
    # both declared the identical single-element shape `("expires at",)`,
    # a substring both blocks share, so a mis-anchored extraction of
    # either into the other's slot satisfied both guards — only the
    # opposed verdicts (`True` vs `False`) happened to catch it. Each
    # needle below is a substring unique to its own block, verified
    # unique by grep across the whole template file.
    "R-VERDICT-EXPIRY": ("Accept — expires at",),
    "R-VERDICT-EXPIRY-BAD": ("Current constraint (expires",),
    "R-HEAD-PROSE-BAD": (
        "C2's threshold", "bill composition unknown", "+ C2's threshold\n→",
    ),
    "R-HEAD-CHAINREF": ("C2 (threshold)", "bill composition unknown"),
    "R-HEAD-ALLCHAIN": ("C5 (~73% ceiling", "C2's saving"),
    "R-HEAD-PROSE-MID": (
        "+ C2's threshold + GT-12?", "bill composition unknown",
    ),
    # `R-HEAD-GTHOP-BAD` / `R-HEAD-GTHOP-OK` (plan 13-09, BL-02) are the
    # same hop differing only in whether it leads with `GT-4`: each first
    # needle is unique to its own block and absent from the other and from
    # `R-HEAD-ALLCHAIN`; the shared second needle catches an extraction
    # landing outside the C1/C2 family entirely.
    "R-HEAD-GTHOP-BAD": (
        "→ GT-4's stated duty cycle", "2.20× at full duty",
        "threshold)\n→ GT-4's stated duty cycle",
    ),
    "R-HEAD-GTHOP-OK": (
        "→ the duty cycle stated in GT-4", "2.20× at full duty",
    ),
    "R-HEAD-GTHOP-LATE": (
        "the second reading is the binding one", "2.20× at full duty",
        "binding one\n→ GT-4's stated duty cycle",
    ),
    # `R-HEAD-PERIOD-BAD` / `R-HEAD-PERIOD-OK` / `R-HEAD-PERIOD-LATE`
    # (plan 13-26, CR-05 fixture half) pin R10's disclosed over-rejection
    # bound in all three measured directions, applying the GTHOP triple's
    # lesson from the start rather than repeating the two-needle mistake
    # 13-19 originally shipped: BAD's third needle,
    # `"workload shape.\n→ C2's saving"`, pins the terminal period IN
    # POSITION — the first hop's tail, the newline, and the opening of the
    # hop it wrongly closes the chain before — and is absent from both OK
    # (no period there) and LATE (the period sits three hops later).
    # OK's needle, `"workload shape\n→ C2's saving"`, is the same
    # transition with the period removed and is absent from BAD (whose
    # period breaks the match) and from LATE (whose second hop is a
    # different sentence, not `"C2's saving"` — a third hop was inserted
    # for exactly this reason: PERIOD-OK's full text would otherwise be a
    # literal prefix of PERIOD-LATE's, and no substring needle can
    # discriminate a text from its own prefix). LATE's third needle,
    # `"alone\n→ C2's saving is real only above the duty-cycle threshold
    # this estimate assumes."`, pins the period at its late position the
    # same way BAD's pins the early one — the inserted second hop's tail,
    # the newline, and the closing hop the check never re-tests once its
    # two-arrow requirement is already satisfied.
    "R-HEAD-PERIOD-BAD": (
        "C1's saving is unconditional", "2.20× at full duty",
        "workload shape.\n→ C2's saving",
    ),
    "R-HEAD-PERIOD-OK": (
        "C1's saving is unconditional", "2.20× at full duty",
        "workload shape\n→ C2's saving",
    ),
    "R-HEAD-PERIOD-LATE": (
        "does not rest on C1 alone", "2.20× at full duty",
        "alone\n→ C2's saving is real only above the duty-cycle threshold this estimate assumes.",
    ),
    # Phase 14 (LEDGER-03, LEDGER-04, Task 1's needle-uniqueness discipline,
    # `14-PATTERNS.md` Pattern 3): each needle below is verified unique by
    # a whole-file grep before being committed to. `R-CLAIM-COLON-MID` and
    # `R-CLAIM-COLON-END` share the prefix `**Overall confidence:`, so each
    # needle is anchored ACROSS the divergence point (the colon's position
    # relative to the closing `**`) rather than on the shared head, which
    # would discriminate neither block from the other.
    # `R-CLAIM-CAVEAT-MARKED` and `R-CLAIM-CAVEAT-CITED` share a long
    # common prefix and diverge only in their tails, which is exactly
    # where both needles sit. `R-CLAIM-TERSE-DROP` and `R-CLAIM-TERSE-KEEP`
    # are deliberately worded DIFFERENTLY, not a one-character minimal
    # pair: a true minimal pair (the same list item with only its
    # terminal period differing) would make one block's text a literal
    # prefix of the other's, which no substring needle can discriminate
    # (the `R-HEAD-PERIOD-*` lesson above) — Task 2's punctuation-toggle
    # re-score is what recovers the minimal-pair property mechanically,
    # in memory, rather than at the fixture-text level.
    "R-CLAIM-LABEL-BARE": ("**Recommended approach — three steps, in this order:**",),
    "R-CLAIM-LABEL-INLINE": (
        "Move sustained workloads to Fargate before evaluating Lambda",
    ),
    "R-CLAIM-LABEL-CITED": (
        "**Recommended approach, established in chain C1:**",
    ),
    "R-CLAIM-COLON-MID": ("confidence: HIGH.**",),
    "R-CLAIM-COLON-END": ("confidence:** HIGH —",),
    "R-CLAIM-TERSE-DROP": ("- Measure duty cycle first",),
    "R-CLAIM-TERSE-KEEP": ("- Size the Savings Plan after cleanup.",),
    "R-CLAIM-CAVEAT-MARKED": ("lower — no chain — flagged assumption only.",),
    "R-CLAIM-CAVEAT-CITED": ("lower (chain C5).",),
}

# Substrings the extracted text for a fixture id must NOT contain.
# `R-CITE-NONE`'s entire point is that it names no chain; an extraction
# that accidentally captured a neighbouring line carrying `C1` would
# otherwise score `False` for the wrong reason. `R-CLAIM-LABEL-BARE`
# (Phase 14) carries the same guard: an extraction that drifted onto
# `R-CLAIM-LABEL-CITED`'s block would otherwise still score `False` for
# the wrong reason, since both blocks are short bold-label lines.
# `R-CLAIM-CAVEAT-MARKED` carries the mirror guard against `C5` for the
# same reason — its whole point is that it names no chain.
_RENDER_FIXTURE_FORBIDDEN: dict[str, tuple[str, ...]] = {
    "R-CITE-NONE": ("C1",),
    "R-CLAIM-LABEL-BARE": ("C1",),
    "R-CLAIM-CAVEAT-MARKED": ("C5",),
}


def _render_fixture_id_token(fixture_id: str) -> str:
    """The DELIMITER-SCOPED token identifying *fixture_id* inside a per-id
    fixture problem: `] <id>: `.

    Exists because bare containment does not discriminate one fixture id
    from another (WR-07, `11-REVIEW-gap-closure.md`):
    `"R-VERDICT-EXPIRY"` is a proper prefix of `"R-VERDICT-EXPIRY-BAD"`,
    so a problem naming only the BAD fixture satisfied `fid in problem`
    for the good one, and control (p)'s accounting arm treated a fixture
    that was never scored and never reported as accounted for. The
    trailing `": "` is what breaks the prefix relation — `"-BAD: "` does
    not contain `": "` at that offset. This is the same loose-substring
    idiom that made the old mode 3 membership check unreachable (WR-06,
    `11-REVIEW.md`), so the token is defined ONCE and shared by the
    emitter (`_render_fixture_problem`) and the matcher
    (`_render_fixture_id_accounted`) rather than restated at either end.
    """
    return f"] {fixture_id}: "


def _render_fixture_problem(mode: str, fixture_id: str, detail: str) -> str:
    """Compose a per-id fixture problem: `[<mode>] <id>: <detail>`.

    The ONE place that form is written, built on `_render_fixture_id_token`
    so the accounting matcher cannot drift away from the emitter.
    """
    return f"[{mode}{_render_fixture_id_token(fixture_id)}{detail}"


def _render_fixture_id_accounted(fixture_id: str, problems: list[str]) -> bool:
    """True when *problems* carries a per-id problem naming *fixture_id*,
    matched on `_render_fixture_id_token` rather than on containment.
    """
    token = _render_fixture_id_token(fixture_id)
    return any(token in problem for problem in problems)


def _render_unscored_fixture_ids(
    locked_ids: set[str], scored_id_set: set[str], problems: list[str]
) -> list[str]:
    """Every id in *locked_ids* that is absent from *scored_id_set* and not
    accounted for by `_render_fixture_id_accounted(fid, problems)`, sorted.

    Membership in *scored_id_set* means a scoring wrapper actually called a
    scorer on that fixture's text — strictly stronger than the extraction
    test this helper replaces, which asked only whether the id was absent
    from the extracted-fixtures mapping. A fixture that fails to extract
    is still discharged, not through scoring but through the
    `problems` accounting arm, matching `_render_fixture_id_accounted`'s
    existing delimiter-scoped matching (never bare containment). Pure: it
    takes all three inputs as parameters and reads no module constant, so a
    self-test control can drive it with synthetic literals without
    touching `_RENDER_CONTRACT_EXTRACTION_TABLE` — the same purity contract
    `scripts/check-registration.py`'s `verify_ci_job_registration` states
    for the REG-GUARD axis.
    """
    return sorted(
        fid
        for fid in locked_ids
        if fid not in scored_id_set
        and not _render_fixture_id_accounted(fid, problems)
    )


def _render_chain_family_ids(
    locked_ids: set[str], prefixes: tuple[str, ...]
) -> set[str]:
    """Every id in *locked_ids* starting with any entry of *prefixes*.

    The chain family is a PROXY for "scored by the single-argument
    `_chain_block_well_formed`" (see `_RENDER_CHAIN_FAMILY_PREFIXES`'s
    own comment for the disclosure) — this helper is deliberately not a
    membership test against a hand-written id list, so a fourteenth
    `R-CHAIN-*`/`R-HEAD-*` fixture added to the locked set is picked up
    the next time this runs rather than requiring a second edit here.
    Pure: takes both inputs as parameters and reads no module constant
    (`_RENDER_CHAIN_FAMILY_PREFIXES` is passed in by the caller, never
    read directly), matching `_render_unscored_fixture_ids`'s purity
    contract — this is what lets control (x)'s x5 arm drive it with
    synthetic literals instead of the real locked set.
    """
    return {
        fid for fid in locked_ids if fid.startswith(tuple(prefixes))
    }


def _render_coverage_floor_problems(
    entries: tuple[tuple[str, frozenset[str], frozenset[str]], ...],
) -> list[str]:
    """For each `(arm_name, actual, required)` entry whose `actual !=
    required`, emit one problem naming the arm and the sorted symmetric
    difference (`required - actual` reported as MISSING, `actual -
    required` reported as UNEXPECTED). Sorted.

    This is an EQUALITY helper, deliberately, not a union or subset
    helper (CR-03, WR-04, `13-REVIEW-plans-08-11.md`):

    - A UNION over two sets is satisfied by whichever set is the
      superset, so narrowing the OTHER set is invisible to it — this is
      exactly how arm 4a's own coverage table could be shrunk from nine
      entries to one while the battery stayed green: arm 4b's table is
      a strict superset of arm 4a's, so the union check never noticed
      arm 4a narrowing underneath it.
    - A SUBSET test (`required - observed`) cannot see an observed set
      that grew past its requirement, and — the shape that matters here
      — when the REQUIREMENT itself is narrowed it cannot see that the
      arm now checks less than it claims to.

    Each entry is floored on its own, independently: a whole sibling
    entry passing cannot discharge a narrowed one, which is what makes
    this helper closed against the CR-03 shape rather than merely a
    relocation of it. Pure: takes all inputs as one parameter and reads
    no module constant.
    """
    problems_out: list[str] = []
    for arm_name, actual, required in entries:
        if actual != required:
            missing = sorted(required - actual)
            unexpected = sorted(actual - required)
            problems_out.append(
                f"{arm_name}: actual {sorted(actual)!r} != required "
                f"{sorted(required)!r} — MISSING {missing!r}, "
                f"UNEXPECTED {unexpected!r}"
            )
    return sorted(problems_out)


def _render_chain_form_surface_problems(
    texts: dict[str, str],
    signature: "re.Pattern[str]",
    registered: frozenset[str],
    exempt: tuple[tuple[str, str], ...],
) -> list[str]:
    """Every relpath in *texts* whose whitespace-normalized text
    (`" ".join(text.split())`, matching `_render_example_claiming_relpaths`'s
    own normalization discipline) matches *signature* and is neither in
    *registered* nor named by *exempt*, one problem per relpath, sorted;
    plus one REASONLESS EXEMPTION problem per *exempt* entry whose written
    reason is blank (an exemption without a written reason is the same
    undisclosed-scoping-decision defect an unregistered surface is, one
    register over); plus one NON-VACUITY problem if *signature* matches
    zero relpaths in *texts* at all — a signature that matches nothing is
    a broken sweep, not a clean tree.

    Pure: takes all four inputs as parameters and reads no module
    constant, matching the purity contract `_render_unscored_fixture_ids`
    and `_render_chain_family_ids` state in their own docstrings — what
    lets an isolation control drive this helper with synthetic `texts`
    and a synthetic *signature* without touching `shared/` or
    `_RENDER_CHAIN_FORM_GLOB`.
    """
    problems_out: list[str] = []

    for relpath, reason in exempt:
        if not reason.strip():
            problems_out.append(
                f"{relpath}: REASONLESS EXEMPTION — exempted from the "
                f"chain-form surface sweep with no written reason"
            )

    exempt_relpaths = {relpath for relpath, _reason in exempt}
    candidates = {
        relpath
        for relpath, text in texts.items()
        if signature.search(" ".join(text.split()))
    }
    for relpath in sorted(candidates - registered - exempt_relpaths):
        problems_out.append(
            f"{relpath}: states the chain form as a template rendering "
            f"(matches the chain-form signature) but is registered in "
            f"neither _RENDER_RULE_SURFACES nor _RENDER_CHAIN_FORM_EXEMPT"
        )

    if not candidates:
        problems_out.append(
            "NON-VACUITY: the chain-form signature matched zero relpaths "
            "— a signature that matches nothing is a broken sweep, not a "
            "clean tree"
        )

    return sorted(problems_out)


def _render_entry_source_problems(
    entries: tuple[tuple[str, frozenset[str], frozenset[str]], ...],
    expected_required_by_name: dict[str, frozenset[str]],
) -> list[str]:
    """For each `(arm_name, actual, required)` entry in *entries*, assert
    that `required` is the value *expected_required_by_name* independently
    names for that arm — never merely that some value is present under
    that name (R4-CR-02, `13-VERIFICATION-round4.md`). Four problem
    shapes, all sorted together:

    - UNREGISTERED: an entry name absent from *expected_required_by_name*.
    - WRONG SOURCE: an entry whose `required` side is not equal to its
      registered expectation, reported as sorted MISSING / UNEXPECTED,
      following `_render_coverage_floor_problems`'s own reporting shape.
    - ALIASED: an entry whose `required` side `is` the SAME OBJECT as its
      `actual` side. Kept separate from WRONG SOURCE on purpose: in the
      passing state EVERY entry's two sides are EQUAL BY VALUE — that is
      what passing means — so a value check alone can never discriminate
      a required side rebound to its own actual side from a correctly
      independent one. Only object identity can. MUTATION M3 exercises
      this arm in isolation, on the arm-4a entry, with no narrowing
      anywhere.
    - MISSING ENTRY: a name registered in *expected_required_by_name* with
      no matching entry in *entries* — so deleting an entry AND its
      expectation together stays loud.

    DISCLOSED LIMITATION: this helper compares `required` against the
    expectation the CALLER supplies — it is the caller's re-derivation
    from primary sources, not this helper, that carries the independence
    property. A rebind of a registry entry's required side to an
    expression of EQUAL value is harmless by construction and therefore
    invisible to the WRONG SOURCE shape — only a rebind that changes what
    the entry actually requires, or aliases it to its own actual side, is
    caught. Pure: takes all inputs as parameters and reads no module
    constant, which is what lets the isolation arms drive it with
    synthetic literals.
    """
    problems_out: list[str] = []
    entry_names = {name for name, _, _ in entries}
    for name, actual, required in entries:
        if name not in expected_required_by_name:
            problems_out.append(
                f"{name}: UNREGISTERED — no entry-source expectation is "
                f"registered for this arm name"
            )
            continue
        expected = expected_required_by_name[name]
        if required is actual:
            problems_out.append(
                f"{name}: ALIASED — the required side is bound to the "
                f"SAME OBJECT as the actual side, so this entry cannot "
                f"report a coverage-floor problem"
            )
        if required != expected:
            missing = sorted(expected - required)
            unexpected = sorted(required - expected)
            problems_out.append(
                f"{name}: WRONG SOURCE — required {sorted(required)!r} != "
                f"expected {sorted(expected)!r} — MISSING {missing!r}, "
                f"UNEXPECTED {unexpected!r}"
            )
    for name in expected_required_by_name:
        if name not in entry_names:
            problems_out.append(
                f"{name}: MISSING ENTRY — an entry-source expectation is "
                f"registered but no matching coverage-floor entry exists"
            )
    return sorted(problems_out)


def _render_verdict_floor_problems(
    expected: dict[str, list[bool]],
    scored_verdicts: dict[str, list[bool]],
    problems: list[str],
) -> list[str]:
    """Every id in *expected* whose recorded verdict sequence in
    *scored_verdicts* is absent or unequal to `expected[fid]`, skipping any
    id already discharged by `_render_fixture_id_accounted(fid, problems)` —
    matching `_render_unscored_fixture_ids`'s existing discharge semantics
    exactly. Sorted.

    This proves a scoring wrapper recorded the VERDICT `expected[fid]`
    states for *fid* — and therefore that SOME code path actually wrote it,
    strictly stronger than mere membership in a set. It does NOT prove the
    fixture's text really scores that way; that is
    `_render_chain_verdict_floor_problems` below's job, which re-derives
    from the text itself and consults no recorder. Pure: takes all three
    inputs as parameters and reads no module constant, matching
    `_render_unscored_fixture_ids`'s purity contract.
    """
    problems_out: list[str] = []
    for fid in sorted(expected):
        if _render_fixture_id_accounted(fid, problems):
            continue
        recorded = scored_verdicts.get(fid)
        if recorded != expected[fid]:
            problems_out.append(
                _render_fixture_problem(
                    "EXPECTED-VERDICT MISMATCH",
                    fid,
                    f"recorded verdict sequence {recorded!r} != expected "
                    f"sequence {expected[fid]!r}",
                )
            )
    return sorted(problems_out)


def _render_chain_verdict_floor_problems(
    expected: dict[str, bool],
    fixtures: dict[str, str],
    scorer: Callable[[str], bool],
    problems: list[str],
) -> list[str]:
    """Every id in *expected* whose text in *fixtures*, scored by *scorer*,
    differs from `expected[fid]`, skipping any id discharged by
    `_render_fixture_id_accounted(fid, problems)`, and REPORTING — never
    silently skipping — an id that is expected but absent from *fixtures*.
    Sorted.

    Reads `fixtures` and calls `scorer` directly: it consults no recorder
    of any shape, so it proves the fixture's text really scores as expected
    under the scorer passed in, and holds regardless of what any recorder
    contains. Taking the scorer as a PARAMETER, rather than hardcoding a
    call to `_chain_block_well_formed`, is deliberate: it is what lets
    control (w) drive this helper with a synthetic predicate without
    monkeypatching the module, and it is why this arm cannot be made
    tautological by comparing a constant with itself.
    """
    problems_out: list[str] = []
    for fid in sorted(expected):
        if _render_fixture_id_accounted(fid, problems):
            continue
        if fid not in fixtures:
            problems_out.append(
                _render_fixture_problem(
                    "CHAIN VERDICT FLOOR",
                    fid,
                    "expected but absent from fixtures",
                )
            )
            continue
        actual = scorer(fixtures[fid])
        if actual != expected[fid]:
            problems_out.append(
                _render_fixture_problem(
                    "CHAIN VERDICT FLOOR",
                    fid,
                    f"scored {actual!r} != expected {expected[fid]!r}",
                )
            )
    return sorted(problems_out)


def _render_example_claiming_relpaths(
    texts: dict[str, str], claim: str
) -> tuple[str, ...]:
    """Sorted relpaths in *texts* whose value, after whitespace
    normalization (`" ".join(text.split())`), contains *claim*.

    Pure: takes the already-read texts and the claim literal as
    parameters and performs no I/O, so an isolation control can drive it
    with synthetic literals without touching `_RENDER_EXAMPLE_GLOB` or the
    real `shared/examples/` tree. Whitespace normalization is
    load-bearing, not decorative (plan 13-14, CR-01
    `13-VERIFICATION-round3.md`): the claim is hard-wrapped across two
    physical lines in `composed-inversion-second-order.md`, so a
    line-scoped containment test would silently exempt that file — the
    same line-scoped blind spot `HEADLINE-LOCK` records for a headline
    wrapped across two physical lines.
    """
    return tuple(
        sorted(
            relpath
            for relpath, text in texts.items()
            if claim in " ".join(text.split())
        )
    )


_RENDER_EXAMPLE_HEADING_RE = re.compile(r"^### Conclusion", re.MULTILINE)
_RENDER_EXAMPLE_BOUND_RE = re.compile(r"^(?:#{1,6} |---\s*$)", re.MULTILINE)


def _render_example_chain_blocks(text: str) -> tuple[tuple[int, str], ...]:
    """Every `### Conclusion`-headed chain block in *text*, bounded, as
    `(1-based heading line number, block text)` pairs.

    A block starts at a line matching `_RENDER_EXAMPLE_HEADING_RE` and ends
    at the next line matching `_RENDER_EXAMPLE_BOUND_RE` after the heading,
    or at end of text. The bound exists because `_chain_block_well_formed`
    is an `any()` over candidates (its own docstring's deferred WR-03
    note): an unbounded block running to end of text would let one
    conforming chain anywhere later in the file mask a malformed one
    earlier in the same block.
    """
    blocks: list[tuple[int, str]] = []
    for heading in _RENDER_EXAMPLE_HEADING_RE.finditer(text):
        bound = _RENDER_EXAMPLE_BOUND_RE.search(text, heading.end())
        end = bound.start() if bound is not None else len(text)
        line_number = text.count("\n", 0, heading.start()) + 1
        blocks.append((line_number, text[heading.start() : end]))
    return tuple(blocks)


def _render_example_conformance_problems(
    texts: dict[str, str],
    claim: str,
    scorer: Callable[[str], bool],
) -> list[str]:
    """For every relpath in *texts* whose whitespace-normalized text
    contains *claim* (derived via `_render_example_claiming_relpaths`),
    score every `### Conclusion` chain block
    (`_render_example_chain_blocks`) with *scorer*, and emit one problem
    per block scoring falsy, naming the relpath, the heading's 1-based
    line number, the heading itself, and the first 60 characters of the
    first line after it that looks like a chain-head candidate (an empty
    string if none is found). A claiming file that yields ZERO blocks
    also emits one problem — a claim with nothing to check is a defect,
    not a pass. Sorted.

    Takes the scorer as a PARAMETER rather than hardcoding a call to
    `_chain_block_well_formed`, copying the parameter-scorer design one
    layer down in this same block: it is what lets an isolation control
    drive this helper with a synthetic predicate without monkeypatching
    the module.

    WR-02 (`13-VERIFICATION-round5.md`): the malformed-block problem used
    to call `block_text.splitlines()[0]` "the head", but `block_text`
    always begins at the `### Conclusion` heading
    (`_render_example_chain_blocks` bounds the block starting at
    `heading.start()`), so that line is the heading, never the chain
    head — `head` is R7/R8/R9's own load-bearing vocabulary, and a
    message calling the heading the head sends a maintainer to the wrong
    line. The heading is still reported (it is what locates the block)
    but is now named as a heading; the first line after it that matches
    `_CHAIN_HEAD_TOKEN_RE` is reported separately as the head candidate.
    Only the message text changed — the signature, return shape, sort
    order and problem count are unchanged.
    """
    problems_out: list[str] = []
    for relpath in _render_example_claiming_relpaths(texts, claim):
        blocks = _render_example_chain_blocks(texts[relpath])
        if not blocks:
            problems_out.append(
                f"{relpath}: asserts {claim!r} but contains zero "
                f"'### Conclusion' chain blocks to check"
            )
            continue
        for line_number, block_text in blocks:
            if not scorer(block_text):
                block_lines = block_text.splitlines()
                heading_line = block_lines[0] if block_lines else ""
                head_candidate = ""
                for candidate_line in block_lines[1:]:
                    stripped_candidate = candidate_line.strip()
                    if _CHAIN_HEAD_TOKEN_RE.search(stripped_candidate):
                        head_candidate = stripped_candidate
                        break
                problems_out.append(
                    f"{relpath}:{line_number}: chain block scored "
                    f"malformed under the frozen detector — heading "
                    f"{heading_line[:60]!r}, head candidate "
                    f"{head_candidate[:60]!r}"
                )
    return sorted(problems_out)


def _read_render_example_texts() -> tuple[dict[str, str], list[str]]:
    """Read every `_RENDER_EXAMPLE_GLOB` match under `shared/examples/`
    into a `relpath -> text` mapping, plus a problems list — never raise,
    never silently skip, matching `_read_qual01_doc_rows`'s discipline
    (`_read_text_or_problem`).
    """
    texts: dict[str, str] = {}
    problems: list[str] = []
    for path in sorted(REPO_ROOT.glob(_RENDER_EXAMPLE_GLOB)):
        relpath = path.relative_to(REPO_ROOT).as_posix()
        text, problem = _read_text_or_problem(path, relpath)
        if problem is not None:
            problems.append(problem)
            continue
        texts[relpath] = text
    return texts, problems


def _render_contract_fixtures() -> tuple[dict[str, str], list[str]]:
    """Read all twenty-seven Phase 11/13/14 rendering-contract fixtures from the shipped
    `shared/` canonical bytes at call time, via the same
    `_extract_contract_example` dispatcher `_CONTRACT_EXTRACTION_TABLE`
    uses above (D-04).

    Returns `(fixtures_by_id, problems)`. `problems` is empty on a clean
    read; every failure to read or shape-validate a fixture is a NAMED
    problem string, never a silent skip or an empty fixture — a broken
    anchor must not degrade into a fixture that satisfies a "must be
    False" assertion for the wrong reason (T-11-08). Three named failure
    modes, mirroring Guard A's mode split:

      mode 1: `_ContractAnchorError` — the anchor did not resolve. Reports
      the anchor, the source file and `exc.detail`, with the remedy
      "re-anchor the guard".

      mode 2: the extracted text is empty, is missing a
      `_RENDER_FIXTURE_SHAPE` substring, or contains a
      `_RENDER_FIXTURE_FORBIDDEN` substring. Reports which fixture and
      which substring.

      mode 3: `_render_fixture_accounting_problems()` — a duplicated row
      id (which `fixtures_by_id`, a dict, would otherwise silently dedup)
      and a count mismatch between `len(fixtures_by_id) + len(problems)`
      and the table's row count. This does NOT answer "does every row's
      id appear somewhere" — an earlier version of this docstring claimed
      that and the code did not keep the promise (WR-06,
      `11-VERIFICATION.md`/`11-REVIEW.md`): the membership question is
      answered by control (h)'s registry lock and control (p)'s
      consumption floor in `_selftest_render_contract`, not here.
    """
    fixtures_by_id: dict[str, str] = {}
    problems: list[str] = []

    for row in _RENDER_CONTRACT_EXTRACTION_TABLE:
        fixture_id = row[0]
        try:
            extracted = _extract_contract_example(row)
        except _ContractAnchorError as exc:
            problems.append(
                _render_fixture_problem(
                    "mode 1: anchor unresolved",
                    fixture_id,
                    f"anchor {exc.anchor!r} in {exc.source_file} did not "
                    f"resolve ({exc.detail}) — remedy: re-anchor the guard",
                )
            )
            continue

        if not extracted:
            problems.append(
                _render_fixture_problem(
                    "mode 2: empty extraction",
                    fixture_id,
                    "extracted text was empty",
                )
            )
            continue

        missing = [
            needle
            for needle in _RENDER_FIXTURE_SHAPE.get(fixture_id, ())
            if needle not in extracted
        ]
        if missing:
            problems.append(
                _render_fixture_problem(
                    "mode 2: shape mismatch",
                    fixture_id,
                    f"extracted text is missing required substring(s) "
                    f"{missing!r}",
                )
            )
            continue

        present_forbidden = [
            needle
            for needle in _RENDER_FIXTURE_FORBIDDEN.get(fixture_id, ())
            if needle in extracted
        ]
        if present_forbidden:
            problems.append(
                _render_fixture_problem(
                    "mode 2: forbidden substring present",
                    fixture_id,
                    f"extracted text unexpectedly contains "
                    f"{present_forbidden!r}",
                )
            )
            continue

        fixtures_by_id[fixture_id] = extracted

    # mode 3: pure reconciliation, driven by parameters rather than by
    # reading the module constant directly, so a self-test control can
    # drive it with a duplicated-id table without editing the constant.
    problems.extend(
        _render_fixture_accounting_problems(
            tuple(row[0] for row in _RENDER_CONTRACT_EXTRACTION_TABLE),
            set(fixtures_by_id),
            problems,
        )
    )

    return fixtures_by_id, problems


def _render_fixture_accounting_problems(
    row_ids: tuple[str, ...],
    extracted_ids: set[str],
    problems: list[str],
) -> list[str]:
    """Plan 11-09's replacement for the mode 3 block WR-06
    (`11-REVIEW.md`) found unreachable by construction: the old condition
    — `fixture_id not in accounted_ids and not any(fixture_id in p for p
    in problems)` — could never be true, because every one of
    `_render_contract_fixtures()`'s five loop exits either inserts the id
    into `fixtures_by_id` or appends a problem string naming it verbatim.

    Reports two things a pure per-id membership check cannot catch:

      - a duplicated row id in *row_ids* — `fixtures_by_id` is a dict, so
        a duplicate silently dedups rather than surfacing as a count
        mismatch;
      - a mismatch between `len(extracted_ids) + len(problems)` and
        `len(row_ids)` — the count reconciliation WR-06's fix note
        proposed.

    Takes its inputs as parameters, never reads
    `_RENDER_CONTRACT_EXTRACTION_TABLE` (or any other module constant)
    directly, so control (q) in `_selftest_render_contract` can drive it
    with a constructed duplicated-id table without touching the module
    constant it guards in production.
    """
    accounting_problems: list[str] = []

    seen_counts: dict[str, int] = {}
    for row_id in row_ids:
        seen_counts[row_id] = seen_counts.get(row_id, 0) + 1
    duplicated_ids = sorted(
        row_id for row_id, count in seen_counts.items() if count > 1
    )
    if duplicated_ids:
        accounting_problems.append(
            f"[mode 3: duplicated row id] {duplicated_ids!r} appear more "
            f"than once in the extraction table"
        )

    if len(extracted_ids) + len(problems) != len(row_ids):
        accounting_problems.append(
            f"[mode 3: count mismatch] {len(extracted_ids)} extracted + "
            f"{len(problems)} problems != {len(row_ids)} registered rows"
        )

    return accounting_problems


def _render_claim_bound_problems(
    expected: dict[str, list[bool]],
    fixtures: dict[str, str],
    claim_scorer: Callable[[str, list[str]], list[str]],
    traced_scorer: Callable[[str, list[str], list[str]], bool],
) -> tuple[list[str], dict[str, list[bool]]]:
    """Phase 14 (LEDGER-03, LEDGER-04, D-07, D-09): score every fixture id
    in *expected* against *claim_scorer* (R11's three claim-extraction
    bounds) or *traced_scorer* (R12's caveat-marker rule), and compare
    each recorded verdict sequence to *expected*.

    Copies `_render_fixture_accounting_problems`'s purity discipline:
    *expected*, *fixtures* and both scorer callables are the ONLY inputs
    — nothing here reads `_RENDER_FIXTURE_SHAPE`, `_conclusion_claims`,
    `_claim_is_traced` or any other module-level name, so a call site
    that wires the wrong table or the wrong scorer becomes unexpressible
    rather than merely untested.

    Two fixed per-id groups, matching the two distinct questions R11 and
    R12 ask of a fixture's text:

      - the two caveat ids (R12) — *claim_scorer* first extracts the
        caveat's own claim text (against chain id `"C5"`), then
        *traced_scorer* decides whether that extracted claim is traced.
        A caveat fixture yielding no claim to trace is a NAMED problem,
        not a silent `False`.
      - every other id (R11) — *claim_scorer* decides, against chain id
        `"C1"`, whether the fixture's text yields any claim at all. An id
        whose *expected* verdict list has length 2 is scored TWICE: once
        on its extracted text, once with its own trailing period toggled
        in memory (stripped if present, appended if absent). This is the
        mechanical proof that the assertiveness bound's axis is
        punctuation, not the wording difference Task 1's needle-
        uniqueness discipline forced `R-CLAIM-TERSE-DROP`/`R-CLAIM-TERSE-
        KEEP` to give up at the text level (a true one-character minimal
        pair would make one block's text a literal prefix of the
        other's, which no substring needle can discriminate — the
        `R-HEAD-PERIOD-*` lesson). `R-CITE-NONE`'s existing `[False,
        True]` is the precedent for a fixture scored more than once with
        different inputs.

    Returns `(problems, verdicts)`. `verdicts` maps every fixture id in
    *expected* to the ordered list of booleans this call produced, so the
    caller can merge it into `scored_verdicts` and the consumption floor
    picks every id up automatically. A fixture id named in *expected* but
    absent from *fixtures*, a caveat fixture yielding no claim to trace, a
    verdict-sequence mismatch against *expected*, and an EMPTY *expected*
    table are each a NAMED problem — never a silent skip and never a
    vacuous pass.
    """
    problems: list[str] = []
    verdicts: dict[str, list[bool]] = {}

    if not expected:
        problems.append(
            "NON-VACUITY: the claim-bound expectation table is empty — "
            "an empty table cannot pin anything and must not pass"
        )
        return problems, verdicts

    traced_ids = {"R-CLAIM-CAVEAT-MARKED", "R-CLAIM-CAVEAT-CITED"}

    for fixture_id, expected_verdicts in expected.items():
        text = fixtures.get(fixture_id)
        if text is None:
            problems.append(
                _render_fixture_problem(
                    "claim-bound: fixture missing",
                    fixture_id,
                    "expected but absent from the extracted fixtures mapping",
                )
            )
            continue

        chain_ids = ["C5"] if fixture_id in traced_ids else ["C1"]

        if fixture_id in traced_ids:
            claims = claim_scorer(text, chain_ids)
            if not claims:
                problems.append(
                    _render_fixture_problem(
                        "claim-bound: no claim to trace",
                        fixture_id,
                        "expected exactly one extracted claim to trace, got none",
                    )
                )
                verdicts[fixture_id] = []
                continue
            recorded = [traced_scorer(claims[0], chain_ids, [])]
        elif len(expected_verdicts) == 2:
            toggled = text[:-1] if text.endswith(".") else text + "."
            recorded = [
                bool(claim_scorer(text, chain_ids)),
                bool(claim_scorer(toggled, chain_ids)),
            ]
        else:
            recorded = [bool(claim_scorer(text, chain_ids))]

        verdicts[fixture_id] = recorded
        if recorded != expected_verdicts:
            problems.append(
                _render_fixture_problem(
                    "claim-bound: verdict mismatch",
                    fixture_id,
                    f"got {recorded!r}, expected {expected_verdicts!r}",
                )
            )

    return problems, verdicts


# Phase 11 (CONTRACT-03, CONTRACT-05, D-04) reconciliation controls. Case A's
# no-wrap rule, the brevity rule and its TELL diagnostic, the citation rule,
# and the reconciled multi-hop head form must each be stated, byte for byte,
# on BOTH canonical surfaces below — not merely each surface's own worked
# examples, which Item 24 above already scores. A rule shipped uncontrolled
# lands in the exact defect class PROJECT.md's through-line names: a form
# stated in more places than anything checks (D-04). D-02 is unaffected:
# nothing here touches `_chain_block_well_formed`.
#
# Plan 11-07 (CR-01, gap 1 of 11-VERIFICATION.md) adds a third surface:
# `shared/spine/references/validation-rubric.md` is the rubric the agent
# scores its own emission against at Phase 5 Criterion 4, so a wrap-
# permitting phrasing there grades the exact defect GAP-9 names as
# Rigorous — the rubric is canonical for the same reason the two contract
# surfaces are, and CR-01's fix note is what put it here. Each surface now
# declares which rule literals it must carry via
# `_RENDER_SURFACE_REQUIRED_RULES` below, rather than every surface being
# required to state all five (later six) rules.
#
# Plan 13-20 (CR-03, `13-VERIFICATION.md` gap 2) adds a fourth surface:
# `shared/references/reason-upward.md` states the chain form
# (`GT-N + GT-M → [intermediate claim] → [conclusion]`) and is the SOLE
# source of the shipped, slash-invocable `first-principles/skills/reason-
# upward/SKILL.md` via the `{{PROCEDURE:reason-upward}}` substitution in
# `sync-content.py` — model-facing at slash-invoke time with no companion
# surface beside it to carry the head-input rule for it. Before this plan
# it carried none of R6-R9 and its own R6 restatement was hard-wrapped
# across three physical lines, so it was not even a substring of the
# registered literal. CR-03's own text is that the requirement reads
# "every canonical surface that states the chain form" — registering this
# surface, rather than deleting the chain form from it, is the same fork
# plan 11-07 took for the rubric one gap earlier.
#
# This tuple is a hand-maintained list, not the enforcement mechanism for
# "every canonical surface that states the chain form" — round 6
# (`13-VERIFICATION-round6.md` gap 3, CR-04) found two more unregistered
# surfaces (`shared/references/estimate-detail.md` and
# `shared/references/theoretical-limit-detail.md`) the round after this
# comment last presented the four-surface set as a completed closure, which
# is exactly what a hand-maintained list cannot see happening to itself.
# What makes the requirement checkable is
# `_render_chain_form_surface_problems` (plan 13-24) — a sweep that derives
# its candidate surface set from the tree via `_RENDER_CHAIN_FORM_SIGNATURE`
# and compares it by equality against this tuple plus
# `_RENDER_CHAIN_FORM_EXEMPT`, not the count of entries here. The two
# CR-04 files were resolved by the point-back fork, not the register fork:
# both Handoff paragraphs now name their technique-specific content in prose
# and point back to `output-template.md`'s own "Converting
# structured-technique outputs into chains" subsection, which already
# declares itself the single source of truth for the conversion and
# instructs per-technique Handoff sections to point back rather than
# restate — registering them here would instead have propagated the four
# `_RENDER_RULE_LITERALS` into every technique appendix that mentions a
# chain, the duplication that produced this defect twice. See plan 13-24's
# SUMMARY and `13-VERIFICATION-round6.md` gap 3 for the full rationale.
_RENDER_RULE_SURFACES: tuple[str, ...] = (
    "shared/spine/references/output-template.md",
    "shared/spine/SKILL-body.md",
    "shared/spine/references/validation-rubric.md",
    "shared/references/reason-upward.md",
)

# Each value is a SHARED VERBATIM LITERAL, present byte for byte on every
# `_RENDER_RULE_SURFACES` entry that requires it (per
# `_RENDER_SURFACE_REQUIRED_RULES` below — not every surface is required to
# carry every key). Reconciliation is implemented as identity of this
# literal across every surface that requires it, so that contradicting one
# required surface without another is unexpressible without deleting the
# literal from it — copying the "shared bytes, not a restated paraphrase"
# discipline that keeps CONTRACT-05's head form from drifting silently.
_RENDER_RULE_LITERALS: dict[str, str] = {
    # R1: the no-wrap rule (CONTRACT-03).
    "R1": (
        "A hop occupies exactly one physical line. Every line after the "
        "head begins with `→` and carries exactly one complete hop; a hop "
        "is never broken across physical lines."
    ),
    # R2: the brevity rule, structural half (D-03).
    "R2": (
        "A hop states exactly ONE inference. If a hop joins two claims "
        "with \"and\", or carries a parenthetical that could stand as its "
        "own claim, it is two hops — split it."
    ),
    # R3: the brevity rule's `TELL (not the rule):` diagnostic (D-03).
    "R3": (
        "TELL (not the rule): a hop past ~200 characters is almost always "
        "two hops. Measure the hop, then split — do not wrap it, and do "
        "not trim words to hit a number."
    ),
    # R4: the citation rule (CONTRACT-02 reconciliation). Amended by plan
    # 14-03 (D-01, D-03): the ledger-discharge half now carries the
    # structural-row residual D-03's narrowing of
    # `_closure_ledger_fragments` leaves behind (a list marker, then the
    # quoted claim, then an arrow, then the chain id — a prose sentence
    # that only quotes and cites is not a ledger row) and the
    # section-6-visibility bound D-01 discloses (a ledger row is detected
    # only when it sits inside section 6; the pre-analysis process-output
    # ledger `output-template.md` also describes is not visible to the
    # check, so inline citation is the mechanically checkable form). Both
    # additions follow R7/R9/R10's own shape: state the rule positively,
    # then disclose the measured bound rather than widen the detector.
    "R4": (
        "Every Conclusion-section claim either names the chain that "
        "established it inline — `(chain C1)` — or is discharged by a "
        "§6→§4 closure ledger row that quotes the claim and names its "
        "chain. A claim doing neither is cut, not softened. Ledger "
        "discharge requires the structural row form the closure-ledger "
        "example below shows — a list marker, then the quoted claim, "
        "then an arrow, then the chain id — and a prose sentence that "
        "merely quotes something and names a chain is not a ledger row. "
        "This is detected only when the row sits inside section 6: the "
        "ledger emitted as process output before the analysis is not "
        "visible to the check, and inline citation is therefore the "
        "mechanically checkable form."
    ),
    # R5: the reconciled multi-hop head form (CONTRACT-05).
    "R5": "GT-1 ([brief fact label]) + GT-6 ([brief fact label])",
    # R6: the one-line-form-is-degenerate-case reconciliation (WR-03,
    # authored by plan 11-06) — ties the one-line chain form to the
    # head-plus-arrow-led multi-hop form so the two are not read as
    # competing shapes.
    "R6": (
        "The one-line form is the degenerate case, used only when the "
        "whole chain fits on one physical line; a chain that does not fit "
        "uses the head-plus-arrow-led form, and a hop is split rather than "
        "continued on a second line."
    ),
    # R7: the head-input rule, its negative, and its disclosed positional
    # bound in one literal (CHAINHEAD-01/CHAINHEAD-02, D-02; the bound
    # sentence added by plan 13-08, BL-01).
    "R7": (
        "The head line lists the inputs the chain consumes: each is a "
        "`GT-N` identifier (`GT-N?` when the ground truth is unverified) "
        "or a `Cn` identifier, optionally followed by a parenthesized "
        "gloss, joined to the next by `+`. The first `→` closes the head. "
        "An input carrying unparenthesized prose — `C2's threshold` — is "
        "not an identifier and does not parse; write `C2 (threshold)` in "
        "every position. The mechanical form check detects that violation "
        "only when the prose input is the last one before the first `→`; "
        "in an earlier position the check matches the well-formed "
        "remainder and scores the head conforming, so the rule binds in "
        "positions the check does not reach."
    ),
    # R8: the rendered head form showing GT-N? and chain-as-input
    # (CHAINHEAD-01, D-03).
    "R8": "GT-1? ([brief fact label]) + C2 ([brief fact label])",
    # R9: the head-only scope note and its GT-leading-hop refusal
    # (CHAINHEAD-01/CHAINHEAD-03/CHAINHEAD-04/CHAINHEAD-05, BL-02). This
    # literal was unregistered prose, byte-identical on three surfaces by
    # discipline alone, until plan 13-09. The `One exception:` clause exists
    # because `_ARROW_LED_GT_RE` refuses continuation for a hop that leads
    # with a `GT-N` identifier — it reads that hop as the head of a new
    # chain and ends the current one there. The trailing disclosure
    # sentence was added by plan 13-18 (13-VERIFICATION.md gap 1, CR-02):
    # R9 shipped as an unconditional refusal one plan after R7 was fixed
    # for the identical defect class (plan 13-08, BL-01) — the form check
    # detects the GT-led-hop violation only while fewer than two hops
    # precede it, measured directly against the live, unmutated
    # `_chain_block_well_formed` (False/False/True/True at 0/1/2/3
    # preceding hops).
    "R9": (
        "The head grammar governs the head line only. A hop is prose: "
        "`C2's saving` is fine after the first `→`, and is not an input "
        "reference. One exception: a hop must not begin with a `GT-N` "
        "identifier, which the form check reads as the head of a new "
        "chain and which therefore ends this one — write `→ the duty "
        "cycle stated in GT-4 is the binding term`, not `→ GT-4's stated "
        "duty cycle is the binding term`. The form check detects that "
        "violation only while fewer than two hops precede it; in a later "
        "position the check matches the preceding hops and scores the "
        "chain conforming, so the rule binds in positions the check does "
        "not reach."
    ),
    # R10: the detector's over-rejection bound, the mirror image of R7's and
    # R9's under-detection bounds (CHAINHEAD-01, `13-VERIFICATION-round6.md`
    # gap 4 / CR-05, plan 13-25). Measured directly against the live,
    # unmutated `_chain_block_well_formed`: closing the head's or the first
    # hop's own sentence rejects the chain at every hop count tested
    # (2/3/4 hops), while the identical closure from the second hop onward
    # leaves the verdict unchanged at every hop count tested — positional,
    # exactly like R7's and R9's bounds. This is why plan 13-13 stripped
    # terminal periods from intermediate hops in the shipped worked
    # examples: naming the practice and its reason here discloses that
    # choice without editing the example files themselves.
    "R10": (
        "The mechanical form check additionally rejects a chain whose "
        "head or first hop closes its own sentence before the next "
        "`→`: it reads the following arrow-led line as a new statement "
        "and ends the chain there, so a chain satisfying every rule "
        "above is scored malformed for that reason alone. The check "
        "reaches only that position — a hop that closes its own "
        "sentence from the second hop onward does not change the "
        "verdict — which is why intermediate hops carry no terminal "
        "punctuation in this project's worked examples."
    ),
    # R11: the closure-ledger claim-extraction rule (LEDGER-01/LEDGER-02,
    # D-05/D-07, plan 14-03). States positively what `_conclusion_claims`
    # extracts — a bold lead-in whose colon closes the bold span, or a
    # list item — names all three prescribed lead-ins (including
    # `**Trade-offs acknowledged:**`, LEDGER-02's own instance) as always
    # claims, and states the fenced-block and restatement/entailment
    # exclusions as RULE (not disclosed bound), per D-07 — mining a fenced
    # ledger's own rows as claims was the 2026-08-31 defect this rule
    # exists to prevent. Three bounds are then disclosed as MEASURED,
    # following R7/R9/R10's shape: (1) a whole-line, uncited bold lead-in
    # is a section-intro label, not a claim itself — the hinge of
    # "detectable from the emission alone" an author can exploit; (2) a
    # bold span whose closing `**` is not immediately preceded by a colon
    # is not matched at all; (3) a list item counts only past the
    # assertiveness floor (`_is_assertive_claim`). Each bound is pinned by
    # a worked-example fixture in section 6 below.
    "R11": (
        "A Conclusion-section claim is a bold lead-in whose colon closes "
        "the bold span, or a numbered or bulleted list item, and the "
        "three lead-ins this template prescribes — "
        "`**Recommended approach:**`, `**Key insight:**`, "
        "`**Trade-offs acknowledged:**` — are always claims and each "
        "must cite a chain; nothing inside a fenced block is ever a "
        "claim whatever its shape, a near-paraphrase restatement or "
        "direct entailment of an already-cited claim earlier in the "
        "same section is not a second claim, and prose carrying neither "
        "a bold colon lead-in nor a list marker is not a claim at all. "
        "Three bounds are measured, not assumed: a bold lead-in whose "
        "colon-terminated span is the entire physical line and carries "
        "no citation of its own is a section-intro label, and the "
        "citation obligation then falls to the list items beneath it; a "
        "bold span whose closing `**` is not immediately preceded by "
        "the colon is not matched at all — write `**Label:** text` to "
        "match, not `**Label: text**`; and a list item counts only "
        "when it closes its own sentence or runs past forty characters. "
        "Enumerate by this rule, not by recollection — the rule is the "
        "contract and the extractor is a partial instrument for it."
    ),
    # R12: the caveat rule (LEDGER-03, D-05/D-08/D-09, plan 14-03). A
    # marked caveat still scores untraced by design — the marker is a
    # disclosure, not a discharge, and neither `_conclusion_claims` nor
    # `_claim_is_traced` is taught the marker: LEDGER-03 forbids answering
    # the caveat sub-question by loosening the extractor, and teaching the
    # tracer would be the same loosening one function over. An author who
    # reads the marker as a discharge silences exactly the signal this
    # phase exists to preserve, so R12 must state the non-discharge in
    # terms that cannot be misread.
    "R12": (
        "A caveat qualifying an existing Conclusion-section claim "
        "either names the chain it qualifies inline or carries the "
        "marker `no chain — flagged assumption only` (em dash, lower "
        "case, no trailing punctuation inside the marker), and a "
        "marked caveat still scores untraced: the marker discloses the "
        "gap, it does not discharge the claim, because it is honest "
        "labelling rather than a citation and the extractor is "
        "deliberately not taught to recognise it. A caveat doing "
        "neither is cut, not softened."
    ),
}

# Which `_RENDER_RULE_LITERALS` keys each `_RENDER_RULE_SURFACES` entry must
# carry. Registration in `_RENDER_RULE_SURFACES` no longer means "this
# surface must state every rule" — the rubric is a scoring instrument, not a
# spec, and has no business stating the citation rule (R4) or the brevity
# TELL (R3). The contradiction scan below is deliberately NOT scoped by this
# mapping: `_RENDER_CONTRADICTION_PHRASES` applies to every registered
# surface regardless of which literals it must carry, because a wrap
# permission is wrong everywhere it appears, not just on the two surfaces
# that also state the positive rule.
#
# `shared/references/reason-upward.md` (plan 13-20, CR-03) gets the same
# four keys as the rubric and for the same reason: this surface states the
# chain form and the head grammar, not the citation rule (R4), the brevity
# TELL (R3) or the reconciled multi-hop head form's R5 rendering — it is a
# focused-mode procedure reference, not the output spec. It still gets the
# unscoped contradiction scan below regardless of this narrower required
# set, which is half the point of registering it.
_RENDER_SURFACE_REQUIRED_RULES: dict[str, tuple[str, ...]] = {
    "shared/spine/references/output-template.md": (
        "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10",
        "R11", "R12",
    ),
    "shared/spine/SKILL-body.md": (
        "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10",
        "R11", "R12",
    ),
    # R4 is deliberately NOT added here — plan 14-02 declined that
    # extension (D-06): the rubric is a scoring instrument, not the
    # output spec, and has no business stating the citation rule. R11
    # and R12 land here because D-06 registers the rubric as one of the
    # three surfaces the claim-inventory and caveat rules must carry
    # (it grades the construct these rules govern).
    "shared/spine/references/validation-rubric.md": (
        "R1", "R6", "R7", "R8", "R9", "R10", "R11", "R12",
    ),
    "shared/references/reason-upward.md": (
        "R6", "R7", "R8", "R9", "R10",
    ),
}

# Phrasings that must appear on NEITHER canonical surface — the enumerated
# ways the no-wrap rule (R1) can be contradicted. The first three are the
# phrasings present in the tree before Phase 11 Plans 01/02 landed; the last
# two are the natural ways a future edit would reintroduce the permission.
# DISCLOSED LIMITATION: this leg detects these ENUMERATED phrasings, not
# arbitrary contradiction of R1 — it is load-bearing rather than decorative
# because the first three were live findings, not hypotheticals.
_RENDER_CONTRADICTION_PHRASES: tuple[str, ...] = (
    "wraps with arrow-led continuation",
    "wrap with arrow-led continuation",
    "too long for one line wraps",
    "a hop may be broken",
    "may wrap across physical lines",
)

# Real wrap-permitting wordings this tree actually shipped before the
# rendering contract landed, byte-recovered with `git show` (plan 11-09,
# WR-07, `11-REVIEW.md`) rather than retyped — each entry is commented
# with its source file and the commit it was read from. Control (l1) in
# `_selftest_render_contract` appends each of these to a real record's
# text and requires `_render_rule_report` to catch it: this pins
# `_RENDER_CONTRADICTION_PHRASES` against wordings that were really in
# this tree, so narrowing the phrase list past one of them goes RED.
_RENDER_PRE_CONTRACT_WORDINGS: tuple[str, ...] = (
    # shared/spine/SKILL-body.md, pre-Phase-11, commit 54cad62
    # ("fix(chain-form): teach arrow-led continuation wrap in both spine
    # surfaces"). Verified via `git show 54cad62~1:shared/spine/SKILL-body.md`
    # showing no wrap wording, then `git show 54cad62:shared/spine/SKILL-body.md`
    # carrying this sentence.
    "**A chain too long for one line wraps with arrow-led continuation "
    "lines — never numbered steps.**",
    # shared/spine/references/output-template.md, pre-Phase-11, the same
    # commit 54cad62 — a differently-worded twin added to the second
    # surface in the same commit.
    "**Multi-hop chains wrap with arrow-led continuation lines — never "
    "numbered steps.**",
    # shared/spine/references/validation-rubric.md, removed by plan 11-06
    # commit e4ff9c0 ("fix(11-06): reword validation-rubric.md Criterion 4
    # to the split-not-wrap form") — CR-01's own finding
    # (`11-REVIEW.md`/`11-VERIFICATION.md`): this wording shipped for a
    # full milestone inside the tree while sitting outside this gate's
    # pre-Plan-11-07 scan scope.
    "a chain too long for one line wraps with `→`-led continuation "
    "lines, never as an ordered list",
)

# Real fabricated-example wordings this tree actually shipped — the
# rendered-example claim floor's own non-vacuity registry, copying
# `_RENDER_PRE_CONTRACT_WORDINGS`'s byte-recovered-not-retyped discipline
# (plan 13-23, `13-VERIFICATION-round6.md` gap 2 / CR-02). The first entry
# is the exact sentence plan 13-20 shipped on `shared/references/
# reason-upward.md`, byte-recovered via `git show
# 8289490:shared/references/reason-upward.md` rather than retyped, where
# it claimed a rendered example the file contained zero of, on a live,
# slash-invocable, model-facing surface. The remaining two are the
# natural re-introduction frames a future paraphrase would use.
# DISCLOSED LIMITATION: this leg detects an ENUMERATED frame set pinned
# against a wording this tree really shipped, not arbitrary fabrication.
_RENDER_FABRICATED_EXAMPLE_WORDINGS: tuple[str, ...] = (
    "Rendered examples follow the prescribed head form (`GT-1? "
    "([brief fact label]) + C2 ([brief fact label])`).",
    "Rendered examples follow",
    "examples follow the prescribed head form",
)

# The chain family is the subset of the locked fixture ids whose scorer
# is the single-argument `_chain_block_well_formed` — every id whose
# independent re-score (arm 4a) can call that scorer directly, rather
# than one of the five `R-CITE-*` / `R-VERDICT-*` fixtures whose scorers
# take extra arguments (chain ids, chain text, ledger fragments). The
# prefix test below is a PROXY for that scorer-arity property, chosen
# because the ids were named for it — the proxy relationship is
# disclosed here rather than left implicit, and control (x)'s x5
# DERIVATION arm proves the derivation discriminates rather than merely
# echoing its input.
_RENDER_CHAIN_FAMILY_PREFIXES: tuple[str, ...] = ("R-CHAIN-", "R-HEAD-")

# The two doc-side QUAL-01 gate-description rows that must state the new
# coverage — see control (m) and Task 3.
_QUAL01_DOC_ROWS: tuple[str, ...] = (
    "CLAUDE.md",
    "docs/ARCHITECTURE.md",
)

# The tokens each registered `| QUAL-01 |` table row must carry (plan
# 11-10, WR-04/IN-02/IN-03; third entry added by plan 13-05, CR-01;
# fourth entry added by plan 13-06, CR-02; fifth entry added by plan
# 13-08, BL-01). The second token is what
# makes the row's disclosure of the third scanned surface
# (validation-rubric.md) load-bearing rather than decorative — a row
# could name "emission rendering contract" while still describing only
# the two-surface world CR-01 closed. The third token pins the corrected
# consumption-floor guarantee: before plan 13-05 both rows stated that
# the floor fails if a fixture is not "scored or reported", but the
# floor tested extraction, not scoring — the row was a true statement
# about a wrong claim. Pinning the corrected phrase is what stops the
# row drifting back to the weaker claim while the gate stays green. The
# fourth token pins the dispatch-reachability leg plan 13-06 added:
# without it, removing the new leg's mention from either doc row would
# leave the gate green while the published claim silently narrowed back
# to what CR-02 found unfalsifiable. The fifth token, `R-HEAD-PROSE-MID`,
# pins the positional-bound disclosure plan 13-08 added: without it
# either row can revert to the unconditional "would fail the pair rather
# than pass it" claim while the gate stays green, which is BL-01 exactly.
# The sixth token, `R-HEAD-GTHOP-OK`, is deliberately the `-OK` id rather
# than the `-BAD` one, added by plan 13-09 (BL-02): the remedy half is
# the claim a future edit is likeliest to drop, because a row can state
# a refusal without stating that the prescribed rewrite was ever
# checked — without this token either row can state the GT-leading-hop
# refusal alone while silently dropping the claim that the rewrite it
# prescribes was ever verified to score well-formed. The seventh token,
# `expected-verdict floor`, added by plan 13-10 (BL-03): without it a row
# reverts to plan 13-05's membership-based claim ("scored by a control,
# not merely extracted"), which `13-VERIFICATION.md` independently showed
# was a true statement about a wrong guarantee — a control could satisfy
# it by calling a scorer and discarding the result, or by writing the
# recorder directly, while scoring nothing. This token pins the
# strengthened claim: the recorded verdict must equal an inline
# expectation, not merely exist. The eighth token, `chain-family
# coverage floor`, added by plan 13-12 (CR-03): without it a row can
# keep stating that the thirteen chain-family fixtures are independently
# re-scored while the arm deciding WHICH thirteen is narrowed to one,
# because the only floor over that arm's own coverage table was a union
# a sibling table already satisfied — CR-03 exactly, and the third time
# in this phase a floor reported PASS while unable to fail. The ninth
# token, `worked-example conformance`, added by plan 13-14 (CR-01,
# `13-VERIFICATION-round3.md`): without it a row can describe a
# four-leg gate while the surface that shipped CR-01 — a false
# conformance claim in a model-facing worked example, inside a GREEN
# battery — goes back to being reachable by no gate at all.
# The tenth token, `call-site census`, added by plan 13-16 (R4-CR-01): without
# it a row can keep describing three forgery-proof floors while the census that
# makes deleting any floor's single real call site loud is silently dropped.
# The eleventh token, `entry-source lock`, added by plan 13-17 (R4-CR-02):
# without it a row can describe a coverage floor whose required side may be
# rebound to its own actual side with the battery green.
# The twelfth token, `R-HEAD-GTHOP-LATE`, added by plan 13-21 (round 5
# closure, `13-VERIFICATION-round5.md`): the sixth token pins the
# GT-leading-hop refusal's prescribed remedy, but neither token states that
# the pair's coverage is positional — without this token a row can claim the
# pair pins R9's refusal "as measured" while silently dropping the fixture
# that pins the position the form check does not reach.
# The thirteenth token, `reason-upward.md`, added by plan 13-21 (round 5
# closure, CR-03's doc half): pins the fourth scanned surface exactly as the
# second token pins the third — without it a row can describe the scan while
# silently reverting to naming three surfaces instead of four.
# The fourteenth token, `over-rejection bound`, added by plan 13-28 (round 6
# closure, gap-4/WR-02 disclosure): without it a row can describe R7's and
# R9's under-detection bounds while silently dropping R10's over-rejection
# bound, leaving the published disclosure one-sided.
# The fifteenth token, `R-HEAD-PERIOD-BAD`, added by plan 13-28: pins the
# fixture triple (plan 13-26) that proves R10's bound in all three measured
# directions — without it a row can state R10's bound in prose with no
# fixture behind it, the same undischarged-claim shape BL-01/BL-02 closed
# for R9.
# The sixteenth token, `chain-form surface sweep`, added by plan 13-28:
# pins the tree-derived sweep (plan 13-24) that replaced the registry's own
# entry count as the "every canonical surface that states the chain form"
# enforcement mechanism — without it a row can claim that guarantee while
# silently reverting to the un-derived count the sweep replaced.
# The seventeenth token, `rendered-example claim floor`, added by plan
# 13-28: pins the leg (plan 13-23) that catches a registered surface
# fabricating a claim that its examples follow the head form — without it
# a row can describe four rendering-contract legs while the fifth, the one
# that closed a real fabricated claim shipped for a full milestone, goes
# unmentioned.
# The following six tokens were all added by plan 14-06 (D-12, the user's
# explicit decision to register this phase's new mechanism rather than
# leave it stated-nowhere): without them a doc row can describe five
# rendering-contract legs while the sixth — the closure-ledger
# claim-inventory leg this phase built across plans 14-01..14-05 — goes
# unmentioned, the inverse of the defect this milestone exists to close.
# The eighteenth token, `closure-ledger claim inventory`, names the leg
# itself; without it a reader of either row cannot tell the leg exists at
# all.
# The nineteenth token, `structural ledger row`, pins D-03's narrowing of
# `_closure_ledger_fragments` to the prescribed row shape — without it a
# row can describe the leg while silently reverting to the pre-D-03
# "any line that quotes and cites" description that made the mechanism's
# only discharge path unconditionally false-positive.
# The twentieth token, `section-intro label`, pins R11's bound-1 clause —
# the hinge of detectable-from-the-emission-alone (CONTEXT.md D-07) —
# without it a row can state R11 exists while dropping its one positional
# bound.
# The twenty-first token, `R-CLAIM-LABEL-BARE`, names the fixture that
# pins that bound, the way the existing `R-HEAD-*` tokens name theirs —
# without it the bound is stated in prose with no fixture behind it, the
# undischarged-claim shape BL-01/BL-02 closed for R9.
# The twenty-second token, `R-CLAIM-CAVEAT-MARKED`, pins D-09's teeth —
# without it a future edit teaching the tracer the flagged-assumption
# marker (making it a silent discharge rather than a disclosure) could
# land while the row still describes the caveat rule's original,
# stricter behaviour.
# The twenty-third token, `quality-ledger-v8.26`, pins D-04's committed
# fixture, following the PROV-GUARD row's own precedent of naming the
# fixture directory a live leg reads — without it a row can claim a live
# leg exists while never naming what it reads.
_QUAL01_DOC_ROW_TOKENS: tuple[str, ...] = (
    "emission rendering contract",
    "validation-rubric.md",
    "scored by a control, not merely extracted",
    "dispatch reachability",
    "R-HEAD-PROSE-MID",
    "R-HEAD-GTHOP-OK",
    "expected-verdict floor",
    "chain-family coverage floor",
    "worked-example conformance",
    "call-site census",
    "entry-source lock",
    "R-HEAD-GTHOP-LATE",
    "reason-upward.md",
    "over-rejection bound",
    "R-HEAD-PERIOD-BAD",
    "chain-form surface sweep",
    "rendered-example claim floor",
    "closure-ledger claim inventory",
    "structural ledger row",
    "section-intro label",
    "R-CLAIM-LABEL-BARE",
    "R-CLAIM-CAVEAT-MARKED",
    "quality-ledger-v8.26",
    "fenced pseudo-heading",
    "boundary regression",
    "silent false-clean",
    "Gate cap",
    "CommonMark closing rules",
    "fence shape battery",
    "direct boundary arms",
)

# A shipped worked example may not assert a conformance property it does
# not have (plan 13-14, CR-01, `13-VERIFICATION-round3.md`) — the
# invariant QUAL-01 leg 5, control (y) below, enforces.

_RENDER_EXAMPLE_CLAIM_LITERAL: str = "in the prescribed head form"
# The assertion whose presence brings a `shared/examples/*.md` file into
# leg 5's scope. Containment is tested against WHITESPACE-NORMALIZED file
# text (`" ".join(text.split())`), never a per-line test: the literal is
# hard-wrapped across two physical lines in
# `composed-inversion-second-order.md` (measured), so a line-scoped test
# would silently exempt that file from the leg entirely — the same
# line-scoped blind spot `HEADLINE-LOCK` records ("detection is
# line-scoped, so a headline hard-wrapped across two physical lines is
# invisible to it", CLAUDE.md's TRACE-03 row), a defect class this
# project has already paid for once.

_RENDER_EXAMPLE_GLOB: str = "shared/examples/*.md"
# The canonical surface leg 5 reads, never the generated
# verbatim-copy mirror under the shipped plugin tree — the same
# source-of-truth discipline the extraction table's own comment records
# as a live past defect (rebinding `source_file` to the generated tree
# left a self-test GREEN while both doc rows told the reader the gate
# reads canonical bytes).

_RENDER_EXAMPLE_CLAIMING_FILES: tuple[str, ...] = (
    "shared/examples/composed-inversion-second-order.md",
    "shared/examples/ishikawa-fishbone.md",
)
# The locked relpath set the DERIVED claiming-file set
# (`_render_example_claiming_relpaths`) is floored against by EQUALITY.
# This is not the list the leg iterates — the leg iterates what it
# derives from the claim literal — it exists so a derivation returning
# fewer (or more) files than this locked set is a loud failure rather
# than a quiet narrowing of scope.

_RENDER_CHAIN_FORM_SIGNATURE: "re.Pattern[str]" = re.compile(
    _CHAIN_HEAD_TOKEN + r".*?" + _ARROW + r"[ \t]*\[[a-z]"
)
# Matches a chain-form TEMPLATE rendering: a GT-N/GT-1/Cn/C1-shaped head
# token (`_CHAIN_HEAD_TOKEN`, the same token `_CHAIN_HEAD_TOKEN_RE` tests
# candidacy with) followed, within the same rendering, by an arrow
# immediately preceding a bracketed PLACEHOLDER (`→ [intermediate claim]`,
# never a filled-in value) — the trailing `[a-z]` requires the bracket's
# first character to be lowercase, which is what a generic placeholder
# noun phrase (`[intermediate claim]`, `[conclusion]`, `[unit-factor
# product]`, `[bracketed magnitude]`, `[governing law]`,
# `[law-permitted ceiling]`, `[gap to convention]`) always is and a
# rendered value never is. Matched against WHITESPACE-NORMALIZED text
# (`" ".join(text.split())`, the same normalization
# `_render_example_claiming_relpaths` applies), never raw text with
# newlines — both CR-04 files hard-wrap the template across two physical
# lines, so a line-scoped pattern would silently exempt them
# (`13-VERIFICATION-round6.md` gap 3).
#
# The `[a-z]` narrowing is load-bearing, not decorative — measured, not
# assumed. Without it, this signature also matches two GENUINE worked
# examples that were live in the tree throughout this plan:
# `shared/examples/estimate-fermi.md` (`→ installed-capital bracket:
# [Lower: ~$15/kWh | Central: ~$30/kWh | Upper: ~$42/kWh]`) and
# `shared/examples/theoretical-limit-carnot.md` (`→ [Conclusion:
# Molten-salt TES is cost-competitive...]`) — both render a real,
# filled-in value inside the bracket, and both happen to start that
# bracket with an uppercase letter. Measured against the live tree with
# `[a-z]` in place: matches exactly the four `_RENDER_RULE_SURFACES`
# entries — zero worked examples, zero other false positives — and
# against the pre-task-1 CR-04 text, on both `estimate-detail.md` and
# `theoretical-limit-detail.md`, proving the narrowing does not cost the
# defect this sweep exists to catch. DISCLOSED LIMITATION: a future
# template rendering whose placeholder noun phrase happens to start with
# an uppercase letter (`[Conclusion]` rather than `[conclusion]`) would
# not match this signature — the same class of bound this file's other
# frozen-detector signatures already disclose (R7, R9) rather than
# silently carry.

_RENDER_CHAIN_FORM_GLOB: str = "shared/**/*.md"
# Recursive, tree-wide — deliberately wider than `_RENDER_EXAMPLE_GLOB`
# (`shared/examples/*.md`, non-recursive): this sweep's whole purpose is
# to derive its candidate surface set from the TREE rather than trust a
# hand-maintained list, so it must reach every file under `shared/`, not
# just the examples directory.

_RENDER_CHAIN_FORM_EXEMPT: tuple[tuple[str, str], ...] = ()
# `(relpath, written reason)` pairs exempted from the sweep without being
# added to `_RENDER_RULE_SURFACES` — empty after plan 13-24, and REQUIRED
# to stay empty unless a future edit writes a reason:
# `_render_chain_form_surface_problems` fails the self-test on any entry
# whose reason is blank, because an unreasoned exemption is the same
# undisclosed-scoping-decision defect round 6's gap 3 named for an
# unregistered surface, one register over.


@dataclass(frozen=True)
class _RenderRegistrySnapshot:
    """A by-value snapshot of the registries the rendering-contract
    mechanism depends on — one field per entry of
    `_RENDER_REGISTRY_FIELDS` (nineteen today, eighteen registries: the
    extraction table contributes both `extraction_rows`, the
    authoritative all-four-column arm, and the derived `extraction_ids`).

    The count is stated once, here, and DERIVED everywhere it is asserted:
    control (h2)'s anti-masking floor compares the dataclass's own field
    names against `_RENDER_REGISTRY_FIELDS`, so a field added without
    being registered fails rather than making a hand-typed number stale.
    A hard number in prose went stale within one plan (WR-06,
    `11-REVIEW-gap-closure.md`: two present-tense descriptions still said
    "eight" after the ninth field landed).

    SCOPE: every module-level rendering-contract registry is a field here
    as of CR-01 (`_RENDER_PRE_CONTRACT_WORDINGS`) and WR-03 (the
    extraction table's non-id columns). The two module constants that are
    deliberately NOT fields are `_RENDER_REGISTRY_FIELDS` itself — the
    field roster this snapshot is asserted against, which cannot lock
    itself. Nothing makes this scope self-maintaining: a NEW
    registry added to the mechanism without a matching field is invisible
    to (h2)'s floor, which asserts field/roster agreement, not
    registry/field agreement.

    Exists so `_render_registry_lock_problems` cannot be handed a loose
    tuple or a hand-built dict on the positive arm: `.live()` is the ONLY
    producer that reads the real module constants, so a caller wanting the
    real registries must go through it. The negative arms control (h2)
    exercises are produced by `dataclasses.replace` on a `.live()`
    snapshot rather than by constructing a synthetic one — a mutation is
    provably a perturbation of the real thing, not a stand-in for it.
    Copies Phase 10 block (m)'s discipline
    (`scripts/check-agent.py:334`, `_assert_live_coverage`): make wrong
    wiring unexpressible, not merely asserted.
    """

    extraction_rows: tuple[tuple[str, str, str, str], ...]
    extraction_ids: tuple[str, ...]
    fixture_shape: dict[str, tuple[str, ...]]
    fixture_forbidden: dict[str, tuple[str, ...]]
    surfaces: tuple[str, ...]
    required_rules: dict[str, tuple[str, ...]]
    literals: dict[str, str]
    contradiction_phrases: tuple[str, ...]
    qual01_doc_rows: tuple[str, ...]
    qual01_doc_row_tokens: tuple[str, ...]
    pre_contract_wordings: tuple[str, ...]
    chain_family_prefixes: tuple[str, ...]
    example_claim_literal: str
    example_glob: str
    example_claiming_files: tuple[str, ...]
    fabricated_example_wordings: tuple[str, ...]
    chain_form_signature: str
    chain_form_glob: str
    chain_form_exempt: tuple[tuple[str, str], ...]

    @classmethod
    def live(cls) -> "_RenderRegistrySnapshot":
        """The only producer that reads the real module constants."""
        return cls(
            extraction_rows=_RENDER_CONTRACT_EXTRACTION_TABLE,
            extraction_ids=tuple(
                row[0] for row in _RENDER_CONTRACT_EXTRACTION_TABLE
            ),
            fixture_shape=_RENDER_FIXTURE_SHAPE,
            fixture_forbidden=_RENDER_FIXTURE_FORBIDDEN,
            surfaces=_RENDER_RULE_SURFACES,
            required_rules=_RENDER_SURFACE_REQUIRED_RULES,
            literals=_RENDER_RULE_LITERALS,
            contradiction_phrases=_RENDER_CONTRADICTION_PHRASES,
            qual01_doc_rows=_QUAL01_DOC_ROWS,
            qual01_doc_row_tokens=_QUAL01_DOC_ROW_TOKENS,
            pre_contract_wordings=_RENDER_PRE_CONTRACT_WORDINGS,
            chain_family_prefixes=_RENDER_CHAIN_FAMILY_PREFIXES,
            example_claim_literal=_RENDER_EXAMPLE_CLAIM_LITERAL,
            example_glob=_RENDER_EXAMPLE_GLOB,
            example_claiming_files=_RENDER_EXAMPLE_CLAIMING_FILES,
            fabricated_example_wordings=_RENDER_FABRICATED_EXAMPLE_WORDINGS,
            chain_form_signature=_RENDER_CHAIN_FORM_SIGNATURE.pattern,
            chain_form_glob=_RENDER_CHAIN_FORM_GLOB,
            chain_form_exempt=_RENDER_CHAIN_FORM_EXEMPT,
        )


# Declaration-order field names of `_RenderRegistrySnapshot` — the
# anti-masking spine control (h2) asserts against. A field added to the
# snapshot without being registered here fails (h2)'s own floor; a
# registry added to the lock without a matching negative case in (h2)'s
# table also fails that floor. See `_render_registry_lock_problems`.
_RENDER_REGISTRY_FIELDS: tuple[str, ...] = (
    "extraction_rows",
    "extraction_ids",
    "fixture_shape",
    "fixture_forbidden",
    "surfaces",
    "required_rules",
    "literals",
    "contradiction_phrases",
    "qual01_doc_rows",
    "qual01_doc_row_tokens",
    "pre_contract_wordings",
    "chain_family_prefixes",
    "example_claim_literal",
    "example_glob",
    "example_claiming_files",
    "fabricated_example_wordings",
    "chain_form_signature",
    "chain_form_glob",
    "chain_form_exempt",
)

def _render_registry_lock_problems(
    snapshot: "_RenderRegistrySnapshot",
) -> tuple[list[str], set[str]]:
    """Compare *snapshot* field by field against literals written INLINE
    here — never against the module constant each field mirrors, so the
    lock cannot be made tautologically green by comparing a constant
    against itself.

    Returns `(problems, checked_fields)`. `checked_fields` is the set of
    field names this call actually compared, returned rather than
    inferred — control (h2)'s `checked_fields` floor asserts it equals
    `set(_RENDER_REGISTRY_FIELDS)`, so a field silently skipped by this
    function (a return before reaching its comparison) is caught rather
    than passing by omission — the exact failure mode (h) had before this
    plan.

    ORDERING DISCIPLINE (WR-05, `11-REVIEW-gap-closure.md`): every
    `checked.add("<field>")` sits AFTER the comparison it records, never
    before it. Written the other way round — which is how this function
    shipped until that finding — the set records fields the function
    *intended* to compare rather than comparisons it actually ran, so a
    `return`, a `continue`, or a deleted comparison body between the
    `add` and the comparison still reported the field as checked and the
    floor still passed. Keep every `add` at the bottom of its own block.
    """
    problems: list[str] = []
    checked: set[str] = set()

    expected_ids = [
        "R-CHAIN-CONFORMING", "R-CHAIN-NUMBERED", "R-CHAIN-WRAPPED",
        "R-CITE-INLINE", "R-CITE-LEDGER", "R-CITE-NONE",
        "R-CLAIM-CAVEAT-CITED", "R-CLAIM-CAVEAT-MARKED",
        "R-CLAIM-COLON-END", "R-CLAIM-COLON-MID",
        "R-CLAIM-LABEL-BARE", "R-CLAIM-LABEL-CITED", "R-CLAIM-LABEL-INLINE",
        "R-CLAIM-TERSE-DROP", "R-CLAIM-TERSE-KEEP",
        "R-HEAD-ALLCHAIN", "R-HEAD-CHAINREF", "R-HEAD-GTHOP-BAD",
        "R-HEAD-GTHOP-LATE", "R-HEAD-GTHOP-OK",
        "R-HEAD-PERIOD-BAD", "R-HEAD-PERIOD-LATE", "R-HEAD-PERIOD-OK",
        "R-HEAD-PROSE-BAD", "R-HEAD-PROSE-MID",
        "R-VERDICT-EXPIRY", "R-VERDICT-EXPIRY-BAD",
    ]

    # The AUTHORITATIVE extraction arm: all FOUR columns of every row, not
    # the `row[0]` id projection the snapshot used to carry (WR-03,
    # `11-REVIEW-gap-closure.md`). `source_file`, `habitat_mode` and
    # `anchor` are what determine WHAT THE GATE ACTUALLY READS, and they
    # sat outside the lock entirely: rebinding all eleven rows'
    # `source_file` to `first-principles/agents/references/` — the
    # GENERATED copy — left the self-test GREEN while both `| QUAL-01 |`
    # doc rows told the reader the gate reads the canonical `shared/`
    # source. (Eleven was the table's size at Phase 11, when this was
    # found; the table now carries twenty-seven rows.) The id-only arm below
    # is kept for its narrower failure message and for its own (h2)
    # cases, not as the authority.
    expected_extraction_rows = (
        (
            'R-CHAIN-CONFORMING',
            'shared/spine/references/output-template.md',
            'fenced-block',
            '**Conforming — head, then one hop per line:**',
        ),
        (
            'R-CHAIN-WRAPPED',
            'shared/spine/references/output-template.md',
            'fenced-block',
            '**Non-conforming — a hop broken across physical lines:**',
        ),
        (
            'R-CHAIN-NUMBERED',
            'shared/spine/references/output-template.md',
            'fenced-block',
            '**Non-conforming — the same hops rendered as a numbered list:**',
        ),
        (
            'R-CITE-INLINE',
            'shared/spine/references/output-template.md',
            'fenced-block',
            '**Conforming — inline chain citation:**',
        ),
        (
            'R-CITE-LEDGER',
            'shared/spine/references/output-template.md',
            'fenced-block',
            '**Conforming — closure-ledger row:**',
        ),
        (
            'R-CITE-NONE',
            'shared/spine/references/output-template.md',
            'fenced-block',
            '**Non-conforming — a claim naming no chain and quoted by no ledger row:**',
        ),
        (
            'R-VERDICT-EXPIRY',
            'shared/spine/references/output-template.md',
            'fenced-block',
            '**Conforming — a current constraint recording its expiry:**',
        ),
        (
            'R-VERDICT-EXPIRY-BAD',
            'shared/spine/references/output-template.md',
            'fenced-block',
            '**Non-conforming — the expiry hoisted into the token slot:**',
        ),
        (
            'R-HEAD-PROSE-BAD',
            'shared/spine/references/output-template.md',
            'fenced-block',
            '**Non-conforming — an input carrying unparenthesized prose:**',
        ),
        (
            'R-HEAD-CHAINREF',
            'shared/spine/references/output-template.md',
            'fenced-block',
            '**Conforming — the same head with the upstream chain as an input:**',
        ),
        (
            'R-HEAD-ALLCHAIN',
            'shared/spine/references/output-template.md',
            'fenced-block',
            '**Conforming — a chain consuming only upstream conclusions:**',
        ),
        (
            'R-HEAD-PROSE-MID',
            'shared/spine/references/output-template.md',
            'fenced-block',
            '**Non-conforming, and undetected by the form check — the same prose input in a non-final position:**',
        ),
        (
            'R-HEAD-GTHOP-BAD',
            'shared/spine/references/output-template.md',
            'fenced-block',
            '**Non-conforming — a hop beginning with a GT-N identifier:**',
        ),
        (
            'R-HEAD-GTHOP-OK',
            'shared/spine/references/output-template.md',
            'fenced-block',
            '**Conforming — the same hop with the identifier moved off the front:**',
        ),
        (
            'R-HEAD-GTHOP-LATE',
            'shared/spine/references/output-template.md',
            'fenced-block',
            '**Non-conforming, and undetected by the form check — the GT-led hop in a later position:**',
        ),
        (
            'R-HEAD-PERIOD-BAD',
            'shared/spine/references/output-template.md',
            'fenced-block',
            '**Non-conforming — the first hop closing its own sentence:**',
        ),
        (
            'R-HEAD-PERIOD-OK',
            'shared/spine/references/output-template.md',
            'fenced-block',
            "**Conforming — the same chain with the first hop's terminal period removed:**",
        ),
        (
            'R-HEAD-PERIOD-LATE',
            'shared/spine/references/output-template.md',
            'fenced-block',
            '**Non-conforming, and undetected by the form check — the same period moved to a later hop:**',
        ),
        (
            'R-CLAIM-LABEL-BARE',
            'shared/spine/references/output-template.md',
            'fenced-block',
            '**Not a claim — a bold lead-in alone on its line, carrying no citation:**',
        ),
        (
            'R-CLAIM-LABEL-INLINE',
            'shared/spine/references/output-template.md',
            'fenced-block',
            '**A claim — the same lead-in carrying its assertion on the same line:**',
        ),
        (
            'R-CLAIM-LABEL-CITED',
            'shared/spine/references/output-template.md',
            'fenced-block',
            '**A claim — the lead-in alone on its line, but carrying its own citation:**',
        ),
        (
            'R-CLAIM-COLON-MID',
            'shared/spine/references/output-template.md',
            'fenced-block',
            '**Not matched at all — a bold span whose colon sits inside it:**',
        ),
        (
            'R-CLAIM-COLON-END',
            'shared/spine/references/output-template.md',
            'fenced-block',
            '**A claim — the same statement with the colon closing the bold span:**',
        ),
        (
            'R-CLAIM-TERSE-DROP',
            'shared/spine/references/output-template.md',
            'fenced-block',
            '**Not a claim — a short list item with no sentence-ending punctuation:**',
        ),
        (
            'R-CLAIM-TERSE-KEEP',
            'shared/spine/references/output-template.md',
            'fenced-block',
            '**A claim — a short list item closing its own sentence:**',
        ),
        (
            'R-CLAIM-CAVEAT-MARKED',
            'shared/spine/references/output-template.md',
            'fenced-block',
            '**Conformant but still untraced — a caveat carrying the flagged-assumption marker:**',
        ),
        (
            'R-CLAIM-CAVEAT-CITED',
            'shared/spine/references/output-template.md',
            'fenced-block',
            '**Conformant and traced — the same caveat citing the chain it qualifies:**',
        ),
    )
    if snapshot.extraction_rows != expected_extraction_rows:
        if len(snapshot.extraction_rows) != len(expected_extraction_rows):
            problems.append(
                f"extraction_rows: {len(snapshot.extraction_rows)} row(s) "
                f"!= expected {len(expected_extraction_rows)}"
            )
        for row_index, expected_row in enumerate(expected_extraction_rows):
            actual_row = (
                snapshot.extraction_rows[row_index]
                if row_index < len(snapshot.extraction_rows)
                else None
            )
            if actual_row != expected_row:
                problems.append(
                    f"extraction_rows: row {row_index} "
                    f"({expected_row[0]}) {actual_row!r} != expected "
                    f"{expected_row!r}"
                )
    checked.add("extraction_rows")

    if sorted(snapshot.extraction_ids) != expected_ids:
        problems.append(
            f"extraction_ids: sorted ids {sorted(snapshot.extraction_ids)!r} "
            f"!= expected {expected_ids!r}"
        )
    checked.add("extraction_ids")

    if sorted(snapshot.fixture_shape) != expected_ids:
        problems.append(
            f"fixture_shape: sorted keys {sorted(snapshot.fixture_shape)!r} "
            f"!= expected {expected_ids!r}"
        )
    else:
        # ALL ids carry a FULL-VALUE lock, not just a key-set lock (the
        # equality check above already pins the id count against
        # `expected_ids`, so the count is not restated here). The three
        # R-CHAIN-* ids were promoted first (IN-04, `11-REVIEW.md`); the
        # five others followed at WR-01 (`11-REVIEW-gap-closure.md`),
        # which reproduced setting each of their needle tuples to `()`
        # with every key still present and the self-test still GREEN —
        # that silently disables the mode-2 shape guard for five of the
        # eighteen fixtures, so an extraction that returned a
        # neighbouring block scores `False` for the wrong reason and
        # passes vacuously. The R-HEAD-* ids (ALLCHAIN, CHAINREF,
        # GTHOP-BAD, GTHOP-OK, PROSE-BAD, PROSE-MID) added at Phase 13
        # carry their discriminating needles from the start, the same
        # treatment the R-CHAIN-* ids received. There is no reason to keep
        # two tiers: a needle tuple is the whole content of the guard for
        # its fixture.
        expected_fixture_shape = {
            "R-CHAIN-CONFORMING": ("GT-1", "GT-6", "actual compute\n→ sustained"),
            "R-CHAIN-WRAPPED": ("GT-1", "GT-6", "\n  once idle-time billing"),
            "R-CHAIN-NUMBERED": ("GT-1", "GT-6", "\n2. "),
            "R-CITE-INLINE": ("(chain C1)",),
            "R-CITE-LEDGER": ("C1", '"'),
            "R-CITE-NONE": ("Fargate",),
            "R-VERDICT-EXPIRY": ("Accept — expires at",),
            "R-VERDICT-EXPIRY-BAD": ("Current constraint (expires",),
            "R-HEAD-PROSE-BAD": (
                "C2's threshold", "bill composition unknown", "+ C2's threshold\n→",
            ),
            "R-HEAD-CHAINREF": ("C2 (threshold)", "bill composition unknown"),
            "R-HEAD-ALLCHAIN": ("C5 (~73% ceiling", "C2's saving"),
            "R-HEAD-PROSE-MID": (
                "+ C2's threshold + GT-12?", "bill composition unknown",
            ),
            "R-HEAD-GTHOP-BAD": (
                "→ GT-4's stated duty cycle", "2.20× at full duty",
                "threshold)\n→ GT-4's stated duty cycle",
            ),
            "R-HEAD-GTHOP-OK": (
                "→ the duty cycle stated in GT-4", "2.20× at full duty",
            ),
            "R-HEAD-GTHOP-LATE": (
                "the second reading is the binding one", "2.20× at full duty",
                "binding one\n→ GT-4's stated duty cycle",
            ),
            "R-HEAD-PERIOD-BAD": (
                "C1's saving is unconditional", "2.20× at full duty",
                "workload shape.\n→ C2's saving",
            ),
            "R-HEAD-PERIOD-OK": (
                "C1's saving is unconditional", "2.20× at full duty",
                "workload shape\n→ C2's saving",
            ),
            "R-HEAD-PERIOD-LATE": (
                "does not rest on C1 alone", "2.20× at full duty",
                "alone\n→ C2's saving is real only above the duty-cycle threshold this estimate assumes.",
            ),
            # Phase 14 (LEDGER-03, LEDGER-04): the nine R-CLAIM-* ids carry
            # their discriminating needles from the start, the same
            # treatment every fixture added since WR-01 has received.
            "R-CLAIM-LABEL-BARE": ("**Recommended approach — three steps, in this order:**",),
            "R-CLAIM-LABEL-INLINE": (
                "Move sustained workloads to Fargate before evaluating Lambda",
            ),
            "R-CLAIM-LABEL-CITED": (
                "**Recommended approach, established in chain C1:**",
            ),
            "R-CLAIM-COLON-MID": ("confidence: HIGH.**",),
            "R-CLAIM-COLON-END": ("confidence:** HIGH —",),
            "R-CLAIM-TERSE-DROP": ("- Measure duty cycle first",),
            "R-CLAIM-TERSE-KEEP": ("- Size the Savings Plan after cleanup.",),
            "R-CLAIM-CAVEAT-MARKED": ("lower — no chain — flagged assumption only.",),
            "R-CLAIM-CAVEAT-CITED": ("lower (chain C5).",),
        }
        for fixture_id, expected_shape in expected_fixture_shape.items():
            actual_shape = snapshot.fixture_shape.get(fixture_id)
            if actual_shape != expected_shape:
                problems.append(
                    f"fixture_shape: {fixture_id} shape {actual_shape!r} "
                    f"!= expected discriminating shape {expected_shape!r}"
                )
    checked.add("fixture_shape")

    expected_forbidden = {
        "R-CITE-NONE": ("C1",),
        "R-CLAIM-LABEL-BARE": ("C1",),
        "R-CLAIM-CAVEAT-MARKED": ("C5",),
    }
    if snapshot.fixture_forbidden != expected_forbidden:
        problems.append(
            f"fixture_forbidden: {snapshot.fixture_forbidden!r} != "
            f"expected {expected_forbidden!r}"
        )
    checked.add("fixture_forbidden")

    expected_surfaces = (
        "shared/spine/references/output-template.md",
        "shared/spine/SKILL-body.md",
        "shared/spine/references/validation-rubric.md",
        "shared/references/reason-upward.md",
    )
    if snapshot.surfaces != expected_surfaces:
        problems.append(
            f"surfaces: {snapshot.surfaces!r} != expected "
            f"{expected_surfaces!r}"
        )
    checked.add("surfaces")

    expected_required_rules = {
        "shared/spine/references/output-template.md": (
            "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10",
            "R11", "R12",
        ),
        "shared/spine/SKILL-body.md": (
            "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10",
            "R11", "R12",
        ),
        "shared/spine/references/validation-rubric.md": (
            "R1", "R6", "R7", "R8", "R9", "R10", "R11", "R12",
        ),
        "shared/references/reason-upward.md": (
            "R6", "R7", "R8", "R9", "R10",
        ),
    }
    if snapshot.required_rules != expected_required_rules:
        problems.append(
            f"required_rules: {snapshot.required_rules!r} != expected "
            f"{expected_required_rules!r}"
        )
    checked.add("required_rules")

    expected_contradiction_phrases = (
        "wraps with arrow-led continuation",
        "wrap with arrow-led continuation",
        "too long for one line wraps",
        "a hop may be broken",
        "may wrap across physical lines",
    )
    if snapshot.contradiction_phrases != expected_contradiction_phrases:
        problems.append(
            f"contradiction_phrases: {snapshot.contradiction_phrases!r} != "
            f"expected {expected_contradiction_phrases!r}"
        )
    checked.add("contradiction_phrases")

    expected_qual01_doc_rows = ("CLAUDE.md", "docs/ARCHITECTURE.md")
    if snapshot.qual01_doc_rows != expected_qual01_doc_rows:
        problems.append(
            f"qual01_doc_rows: {snapshot.qual01_doc_rows!r} != expected "
            f"{expected_qual01_doc_rows!r}"
        )
    checked.add("qual01_doc_rows")

    expected_qual01_doc_row_tokens = (
        "emission rendering contract",
        "validation-rubric.md",
        "scored by a control, not merely extracted",
        "dispatch reachability",
        "R-HEAD-PROSE-MID",
        "R-HEAD-GTHOP-OK",
        "expected-verdict floor",
        "chain-family coverage floor",
        "worked-example conformance",
        "call-site census",
        "entry-source lock",
        "R-HEAD-GTHOP-LATE",
        "reason-upward.md",
        "over-rejection bound",
        "R-HEAD-PERIOD-BAD",
        "chain-form surface sweep",
        "rendered-example claim floor",
        "closure-ledger claim inventory",
        "structural ledger row",
        "section-intro label",
        "R-CLAIM-LABEL-BARE",
        "R-CLAIM-CAVEAT-MARKED",
        "quality-ledger-v8.26",
        # CR-01/CR-02 (phase-14 review): the two boundary defects in the
        # D-02 fix as first shipped. Registered here for the same reason
        # every token above is — the rows' prose about them is otherwise
        # unchecked, and "stated in more places than anything checks" is
        # the defect class this milestone exists to close. The rows made
        # exactly that mistake once already: they published "ANY depth"
        # against a pattern (`#{1,3}`) that could not express it.
        "fenced pseudo-heading",
        "boundary regression",
        "silent false-clean",
        # The review of the CR-01/CR-02 fix found its replacement rule
        # published on both rows with nothing checking it — "stated in more
        # places than anything checks", one plan after closing that exact
        # shape. These four cover the design the rows now describe.
        "Gate cap",
        "CommonMark closing rules",
        "fence shape battery",
        "direct boundary arms",
    )
    if snapshot.qual01_doc_row_tokens != expected_qual01_doc_row_tokens:
        problems.append(
            f"qual01_doc_row_tokens: {snapshot.qual01_doc_row_tokens!r} != "
            f"expected {expected_qual01_doc_row_tokens!r}"
        )
    checked.add("qual01_doc_row_tokens")

    # `_RENDER_PRE_CONTRACT_WORDINGS` is the ONLY thing making control
    # (l1) non-tautological — it detects the phrase list against wordings
    # this tree really shipped. Until CR-01
    # (`11-REVIEW-gap-closure.md`) it was the one rendering-contract
    # registry outside this lock: emptying it, or replacing an entry with
    # a bare `_RENDER_CONTRADICTION_PHRASES` member, left the self-test
    # GREEN with (l1) running zero real cases. Locked by value here; the
    # non-tautology and case-count floors live beside (l1) itself.
    expected_pre_contract_wordings = (
        "**A chain too long for one line wraps with arrow-led continuation "
        "lines — never numbered steps.**",
        "**Multi-hop chains wrap with arrow-led continuation lines — never "
        "numbered steps.**",
        "a chain too long for one line wraps with `→`-led continuation "
        "lines, never as an ordered list",
    )
    if snapshot.pre_contract_wordings != expected_pre_contract_wordings:
        problems.append(
            f"pre_contract_wordings: {snapshot.pre_contract_wordings!r} != "
            f"expected {expected_pre_contract_wordings!r}"
        )
    checked.add("pre_contract_wordings")

    # `chain_family_prefixes` (plan 13-12, CR-03): the prefix pair
    # `_render_chain_family_ids` derives arm 4a's coverage from. Locked
    # here by value, never against the module constant it mirrors.
    expected_chain_family_prefixes = ("R-CHAIN-", "R-HEAD-")
    if snapshot.chain_family_prefixes != expected_chain_family_prefixes:
        problems.append(
            f"chain_family_prefixes: {snapshot.chain_family_prefixes!r} != "
            f"expected {expected_chain_family_prefixes!r}"
        )
    checked.add("chain_family_prefixes")

    # `example_claim_literal`, `example_glob`, `example_claiming_files`
    # (plan 13-14, CR-01, `13-VERIFICATION-round3.md`): the claim literal
    # leg 5 (control (y)) derives its scope from, the canonical-only glob
    # it reads, and the locked two-file set the derivation is floored
    # against by equality. Locked here by value, never against the module
    # constant each mirrors.
    expected_example_claim_literal = "in the prescribed head form"
    if snapshot.example_claim_literal != expected_example_claim_literal:
        problems.append(
            f"example_claim_literal: {snapshot.example_claim_literal!r} "
            f"!= expected {expected_example_claim_literal!r}"
        )
    checked.add("example_claim_literal")

    expected_example_glob = "shared/examples/*.md"
    if snapshot.example_glob != expected_example_glob:
        problems.append(
            f"example_glob: {snapshot.example_glob!r} != expected "
            f"{expected_example_glob!r}"
        )
    checked.add("example_glob")

    expected_example_claiming_files = (
        "shared/examples/composed-inversion-second-order.md",
        "shared/examples/ishikawa-fishbone.md",
    )
    if snapshot.example_claiming_files != expected_example_claiming_files:
        problems.append(
            f"example_claiming_files: {snapshot.example_claiming_files!r} "
            f"!= expected {expected_example_claiming_files!r}"
        )
    checked.add("example_claiming_files")

    # `fabricated_example_wordings` (plan 13-23, CR-02
    # `13-VERIFICATION-round6.md` gap 2): the byte-recovered-not-retyped
    # wordings the rendered-example claim floor scans every registered
    # surface for. Locked here by value, never against the module
    # constant it mirrors.
    expected_fabricated_example_wordings = (
        "Rendered examples follow the prescribed head form (`GT-1? "
        "([brief fact label]) + C2 ([brief fact label])`).",
        "Rendered examples follow",
        "examples follow the prescribed head form",
    )
    if (
        snapshot.fabricated_example_wordings
        != expected_fabricated_example_wordings
    ):
        problems.append(
            f"fabricated_example_wordings: "
            f"{snapshot.fabricated_example_wordings!r} != expected "
            f"{expected_fabricated_example_wordings!r}"
        )
    checked.add("fabricated_example_wordings")

    # `chain_form_signature`, `chain_form_glob`, `chain_form_exempt`
    # (plan 13-24, CR-04, `13-VERIFICATION-round6.md` gap 3): the
    # tree-derived chain-form-surface sweep's own registries — the
    # signature pattern the sweep matches candidate relpaths against, the
    # recursive glob it reads the tree through, and the locked
    # (relpath, reason) exemption set. Locked here by value, never against
    # the module constant each mirrors.
    expected_chain_form_signature = (
        r"(?:GT-[A-Za-z0-9]+\??|C\d+).*?(?:→|->)[ \t]*\[[a-z]"
    )
    if snapshot.chain_form_signature != expected_chain_form_signature:
        problems.append(
            f"chain_form_signature: {snapshot.chain_form_signature!r} != "
            f"expected {expected_chain_form_signature!r}"
        )
    checked.add("chain_form_signature")

    expected_chain_form_glob = "shared/**/*.md"
    if snapshot.chain_form_glob != expected_chain_form_glob:
        problems.append(
            f"chain_form_glob: {snapshot.chain_form_glob!r} != expected "
            f"{expected_chain_form_glob!r}"
        )
    checked.add("chain_form_glob")

    expected_chain_form_exempt: tuple[tuple[str, str], ...] = ()
    if snapshot.chain_form_exempt != expected_chain_form_exempt:
        problems.append(
            f"chain_form_exempt: {snapshot.chain_form_exempt!r} != "
            f"expected {expected_chain_form_exempt!r}"
        )
    checked.add("chain_form_exempt")

    # `literals` carries TWO arms under the single field name — both
    # required, both counted under "literals" so neither can be dropped
    # while the field still reads as covered.
    expected_literal_clauses = {
        "R1": "a hop is never broken across physical lines",
        "R2": "it is two hops — split it",
        "R3": "do not wrap it",
        # R4's clause pin is repointed by plan 14-03 (D-01), following
        # R7/R9/R10's own stated rationale (plans 13-08, 13-18, 13-25):
        # the clause arm proves one substring per rule and the digest arm
        # covers the rest, so the clause should pin the half a future edit
        # is most likely to quietly drop — which after plan 14-03 is the
        # section-6-scope disclosure D-01 adds, not the "cut, not
        # softened" rule half, which was already covered before the
        # amendment and is in no more danger of quiet removal now than it
        # was then.
        "R4": "detected only when the row sits inside section 6",
        "R5": "GT-1 ([brief fact label]) + GT-6",
        "R6": "a hop is split rather than continued on a second line",
        # R7's clause pins the disclosed positional bound rather than the
        # negative-rule half: the clause arm proves one substring per rule
        # and the digest arm covers the rest, so the clause should pin the
        # half a future edit is most likely to quietly drop — which is now
        # the disclosure, not the negative rule (plan 13-08, BL-01).
        "R7": "detects that violation only when the prose input is the last one before the first",
        "R8": "GT-1? ([brief fact label]) + C2",
        # R9's clause pins the disclosed positional bound rather than the
        # negative-rule half: the clause arm proves one substring per rule
        # and the digest arm covers the rest, so the clause should pin the
        # half a future edit is most likely to quietly drop — which is now
        # the disclosure, not the refusal (plan 13-18, mirroring plan
        # 13-08's identical re-point for R7).
        "R9": "detects that violation only while fewer than two hops precede it",
        # R10's clause pins the POSITIONAL half rather than the rejection
        # half, following R7's and R9's own rationale: the clause arm
        # proves one substring per rule, so it must pin the half a future
        # edit is likeliest to quietly drop, which is the disclosure that
        # the over-rejection bound does not reach hop 2 onward (plan
        # 13-25, gap 4 / CR-05).
        "R10": "from the second hop onward does not change the verdict",
        # R11's clause pins bound 1 (the whole-line, uncited section-intro
        # label) rather than the positive extraction rule: CONTEXT.md D-07
        # names this bound "the hinge of detectable-from-the-emission-
        # alone" and it is the bound an author can exploit to dodge
        # extraction — the half a future edit is likeliest to quietly
        # soften or drop.
        "R11": "is the entire physical line and carries no citation of its own is a section-intro label",
        # R12's clause pins D-09's non-discharge half rather than the
        # marker's own bytes: an author who reads the marker as a
        # discharge silences exactly the signal this phase preserves, so
        # this is the sentence a future "helpful" edit would soften
        # first.
        "R12": "the marker discloses the gap, it does not discharge the claim",
    }
    if sorted(snapshot.literals) != sorted(expected_literal_clauses):
        problems.append(
            f"literals: key set {sorted(snapshot.literals)!r} != expected "
            f"{sorted(expected_literal_clauses)!r}"
        )
    else:
        for key, clause in expected_literal_clauses.items():
            if clause not in snapshot.literals[key]:
                problems.append(
                    f"literals: {key} is missing its required clause "
                    f"{clause!r}"
                )

    # A `sha256:<hex>` pin over `_RENDER_RULE_LITERALS`, recomputed as
    # `"\x00".join(f"{k}={v}" for k, v in sorted(literals.items()))`
    # encoded UTF-8. Recompute ONLY with an explicit, reviewed contract
    # change — a diff to this literal should always accompany a diff to the
    # literals it pins. It sits beside the clause arm because the clause arm
    # only proves ONE required substring survived per literal; the digest
    # arm catches every other text change, including one that keeps the
    # required clause and appends a permission the clause never excluded.
    #
    # Written INLINE here, like every other expectation in this function
    # (CR-02/IN-01, `11-REVIEW-gap-closure.md`). It used to be the module
    # constant `_RENDER_RULE_LITERAL_DIGEST`, which was the one arm
    # breaking this function's own stated discipline — not tautological
    # (the pin is hand-written, not derived at runtime) but an invitation
    # to relax the rule elsewhere, and the reason the published
    # `| QUAL-01 |` rows' "locked by value against inline expectations"
    # was not literally true of every arm.
    expected_literal_digest = (
        "sha256:7834b5c5b51136e2403d41ad94bb126eaec785eddb2df4e0950f69654edbdd49"
    )
    literal_digest = "sha256:" + hashlib.sha256(
        "\x00".join(
            f"{k}={v}" for k, v in sorted(snapshot.literals.items())
        ).encode("utf-8")
    ).hexdigest()
    if literal_digest != expected_literal_digest:
        problems.append(
            f"literals: digest {literal_digest!r} != pinned "
            f"{expected_literal_digest!r}"
        )
    checked.add("literals")

    return problems, checked


def _read_text_or_problem(path: Path, relpath: str) -> tuple[str | None, str | None]:
    """Read *path* as UTF-8 text, returning `(text, None)` on success and
    `(None, named_problem)` on failure — never an uncaught exception.

    Catches `(OSError, ValueError)`: `UnicodeDecodeError` is a `ValueError`
    subclass, not an `OSError`, so a readable-but-non-UTF-8 file used to
    propagate out of `_selftest_render_contract` and out of `self_test()`
    entirely — QUAL-01 died with a traceback and no finding, which is
    strictly worse for triage than the named problem the surface readers'
    docstrings promise (WR-08, `11-REVIEW.md`). The problem string carries
    *relpath* and the exception `repr()`, matching the shape both readers
    already reported for the narrower `OSError`-only case.

    Takes a `Path` parameter deliberately: it is what makes the failure
    path drivable by a control (isolation control (r)) with a tempdir
    fixture, without touching the repo tree.
    """
    try:
        return path.read_text(encoding="utf-8"), None
    except (OSError, ValueError) as exc:
        return None, f"could not read {relpath}: {exc!r}"


@dataclass(frozen=True)
class _RenderSurfaceRead:
    """One canonical surface's relpath and the text actually read from it.

    Exists so `_render_rule_report` cannot be handed a synthetic string: its
    sole parameter is this record type, produced only by
    `_read_render_surfaces()`, which reads the file and carries both the
    relpath and the text it actually read. A caller therefore cannot pass a
    hand-built string or a glob-derived path set — the type refuses it.
    Copies Phase 10 block (m)'s shape (`scripts/check-agent.py:334`,
    `_assert_live_coverage`): make wrong wiring unexpressible, not merely
    asserted.
    """

    relpath: str
    text: str


def _read_render_surfaces() -> tuple[tuple[_RenderSurfaceRead, ...], list[str]]:
    """Read every `_RENDER_RULE_SURFACES` entry into a typed record.

    Returns `(reads, problems)`. A path that cannot be opened OR decoded is
    a NAMED problem carrying the relpath and the exception repr, never a
    silent skip and never an uncaught traceback — routed through
    `_read_text_or_problem`, which catches `(OSError, ValueError)` (WR-08),
    mirroring `_render_contract_fixtures()`'s fail-closed shape above.
    """
    reads: list[_RenderSurfaceRead] = []
    problems: list[str] = []
    for relpath in _RENDER_RULE_SURFACES:
        text, problem = _read_text_or_problem(REPO_ROOT / relpath, relpath)
        if problem is not None:
            problems.append(problem)
            continue
        reads.append(_RenderSurfaceRead(relpath=relpath, text=text))
    return tuple(reads), problems


def _render_required_rule_problems(
    relpath: str,
    text: str,
    required_rules: dict[str, tuple[str, ...]] | None = None,
    literals: dict[str, str] | None = None,
) -> list[str]:
    """Report every missing REQUIRED rule literal for *relpath*/*text*
    against *required_rules* and *literals*.

    Extracted from `_render_rule_report` so the two fail-closed branches
    below are independently testable by passing a copied mapping — control
    (o) drives the unknown-key branch this way, without mutating either
    module constant in place. `_render_rule_report` calls this with both
    defaults, so its own behavior is unchanged; the two module constants
    remain the single source of truth for every real caller.

    Fails CLOSED on two degenerate cases, each a NAMED problem carrying the
    relpath, never a silent skip:
      - *relpath* has no entry in *required_rules* — the surface is
        registered but its required rule set was never declared.
      - a declared required key has no entry in *literals* — the surface
        requires a rule that no longer has a literal.
    """
    if required_rules is None:
        required_rules = _RENDER_SURFACE_REQUIRED_RULES
    if literals is None:
        literals = _RENDER_RULE_LITERALS

    problems: list[str] = []

    required_keys = required_rules.get(relpath)
    if required_keys is None:
        problems.append(
            f"{relpath}: is registered in _RENDER_RULE_SURFACES but "
            f"has no declared rule set — declare its required rules in "
            f"_RENDER_SURFACE_REQUIRED_RULES"
        )
    else:
        for key in required_keys:
            literal = literals.get(key)
            if literal is None:
                problems.append(
                    f"{relpath}: requires rule {key}, which no "
                    f"longer has a literal in _RENDER_RULE_LITERALS — the "
                    f"surface requires a rule that no longer has a literal"
                )
                continue
            if literal not in text:
                problems.append(
                    f"{relpath}: rule {key} is missing — deleted from "
                    f"this surface"
                )
    return problems


def _render_rule_report(read: _RenderSurfaceRead) -> list[str]:
    """Report every missing REQUIRED rule literal and every contradicting
    phrasing found in *read*'s text.

    Takes the `_RenderSurfaceRead` record itself, never a `str` or a `Path`
    — see the record's docstring. Which literals are required is looked up
    per surface via `_RENDER_SURFACE_REQUIRED_RULES`, not every entry of
    `_RENDER_RULE_LITERALS` — registering a surface means "it must state
    these rules and contradict none", not "it must state all of them".
    Delegates to `_render_required_rule_problems` with both module
    constants as defaults — see that function's docstring for the two
    fail-closed branches.

    One problem per missing required literal, naming the relpath, the
    literal key and that the rule was deleted from that surface; one
    problem per present `_RENDER_CONTRADICTION_PHRASES` entry, naming the
    relpath and the phrase. The contradiction scan is UNSCOPED — it runs
    the full phrase list against every surface regardless of that
    surface's required-rule set.
    """
    problems = _render_required_rule_problems(read.relpath, read.text)

    for phrase in _RENDER_CONTRADICTION_PHRASES:
        if phrase in read.text:
            problems.append(
                f"{read.relpath}: contradicts the no-wrap rule with the "
                f"phrase {phrase!r}"
            )
    return problems


# Matches a ` ``` `-delimited span on WHITESPACE-NORMALIZED text (no
# newlines survive normalization, so this is deliberately not `re.DOTALL`
# and deliberately not anchored to a language tag — a claiming surface may
# fence with ` ```text ` or bare ` ``` `). Non-greedy so back-to-back
# fenced blocks are read as separate spans, not one span swallowing the
# prose between them.
_RENDER_CLAIM_FLOOR_FENCE_RE = re.compile(r"```.*?```")


def _render_example_claim_floor_problems(
    texts: dict[str, str],
    wordings: tuple[str, ...],
    head_literal: str,
) -> list[str]:
    """Report one sorted problem per relpath in *texts* that CLAIMS its
    examples follow the head form while not actually rendering that form.

    For each `(relpath, text)` in *texts* whose WHITESPACE-NORMALIZED text
    (`" ".join(text.split())`) contains any entry of *wordings*, requires
    that same normalized text to also contain *head_literal* inside a
    fenced block (a ` ``` `-delimited span) — i.e. the file must actually
    render the head it claims its examples follow, the way `output-
    template.md` and `SKILL-body.md` do. A claiming file whose fenced span
    contains the literal is left alone: the claim is true of it. A
    claiming file with no such span, or whose fenced spans do not contain
    the literal, gets exactly one problem naming the relpath and the
    matched frame.

    Pure: takes all three inputs as parameters and reads no module
    constant — matching the purity contract `_render_unscored_fixture_ids`
    and `_render_chain_family_ids` state in their own docstrings — so a
    control can drive it with synthetic literals without touching the
    real registered surfaces (plan 13-23, CR-02 `13-VERIFICATION-round6.md`
    gap 2).

    Whitespace normalization is load-bearing, not decorative, for the SAME
    reason `_render_example_claiming_relpaths` states it is: a claim or a
    rendered head hard-wrapped across physical lines must not be silently
    exempted by a line-scoped test.
    """
    problems: list[str] = []
    for relpath in sorted(texts):
        normalized = " ".join(texts[relpath].split())
        matched_wording = next(
            (wording for wording in wordings if wording in normalized), None
        )
        if matched_wording is None:
            continue
        fenced_spans = _RENDER_CLAIM_FLOOR_FENCE_RE.findall(normalized)
        if any(head_literal in span for span in fenced_spans):
            continue
        problems.append(
            f"{relpath}: claims its examples follow the head form "
            f"({matched_wording!r}) but does not render {head_literal!r} "
            f"inside a fenced block"
        )
    return sorted(problems)


def _qual01_row_problem(read: _RenderSurfaceRead) -> list[str]:
    """Report every `_QUAL01_DOC_ROW_TOKENS` entry missing from *read*'s
    `| QUAL-01 |` table row — one problem per missing token, naming the
    relpath and the token, never a single all-or-nothing verdict (plan
    11-10, IN-02/IN-03).

    Takes the `_RenderSurfaceRead` record itself, never a loose
    `(relpath, text)` pair — mirrors `_render_rule_report`'s discipline.
    ROW-SCOPED (IN-03): only a physical line whose `lstrip()` starts with
    the exact prefix `| QUAL-01 |` is inspected. A file may mention
    "QUAL-01" on other lines (`CLAUDE.md` has three: the commands block,
    the CI-gates intro paragraph, and the battery-tally paragraph) — a
    claim stated on one of those does not satisfy this check; only the
    table row itself does.
    """
    qual01_row_lines = [
        line
        for line in read.text.splitlines()
        if line.lstrip().startswith("| QUAL-01 |")
    ]
    problems: list[str] = []
    for token in _QUAL01_DOC_ROW_TOKENS:
        if not any(token in line for line in qual01_row_lines):
            problems.append(
                f"{read.relpath}: the '| QUAL-01 |' row is missing "
                f"required token {token!r}"
            )
    return problems


def _read_qual01_doc_rows() -> tuple[tuple[_RenderSurfaceRead, ...], list[str]]:
    """Read every `_QUAL01_DOC_ROWS` entry into a typed record, mirroring
    `_read_render_surfaces()` exactly: a path that cannot be opened OR
    decoded is a NAMED problem carrying the relpath and the exception
    repr, never a silent skip and never an uncaught traceback — routed
    through `_read_text_or_problem` (WR-08).
    """
    reads: list[_RenderSurfaceRead] = []
    problems: list[str] = []
    for relpath in _QUAL01_DOC_ROWS:
        text, problem = _read_text_or_problem(REPO_ROOT / relpath, relpath)
        if problem is not None:
            problems.append(problem)
            continue
        reads.append(_RenderSurfaceRead(relpath=relpath, text=text))
    return tuple(reads), problems


_MATRIX_SELFTEST_ANCHOR_RE = re.compile(
    r"scripts/check-quality-harness\.py#(_self_?test_\w+)"
)


def _matrix_named_selftest_symbols() -> tuple[tuple[str, ...], list[str]]:
    """Read `scripts/check-traceability.py`'s source and return the sorted
    tuple of `_selftest_*`/`_self_test_*` anchors any `MatrixRow.
    artifact_link` names in THIS file (`scripts/check-quality-harness.py`),
    plus a problems list rather than raising (unreadable file, decode
    error — same `_read_text_or_problem` discipline as
    `_read_qual01_doc_rows`).

    Derives the symbol set from the sibling script's source rather than
    restating a hand-typed list here: a new matrix row naming a new
    sub-check is picked up automatically the next time this runs, and a
    restated list would go stale silently the moment a row's anchor
    changed and this file's copy did not (WR-06 idiom).

    Matches BOTH self-test-anchor naming conventions this repository
    uses (`_selftest_*` and `_self_test_*`, WR-04, plan 13-12), mirroring
    the widening `check-traceability.py`'s own dispatch-reachability leg
    got at plan 13-11 for exactly the same reason. Measured against the
    live tree at plan 13-12 (A-02): the derived set is unchanged today —
    `('_selftest_analysis_persistence', '_selftest_capture_tool_reader',
    '_selftest_chain_detector_pin', '_selftest_render_contract')` —
    because no `scripts/check-quality-harness.py#...` matrix row names a
    `_self_test_*` anchor. This widening is a future-narrowing guard, not
    a present behaviour change.
    """
    text, problem = _read_text_or_problem(
        REPO_ROOT / "scripts/check-traceability.py",
        "scripts/check-traceability.py",
    )
    if problem is not None:
        return (), [problem]
    symbols = sorted(set(_MATRIX_SELFTEST_ANCHOR_RE.findall(text)))
    return tuple(symbols), []


def _dispatch_reachability_problems(
    symbols: tuple[str, ...], self_test_source: str
) -> list[str]:
    """For each *symbols* entry, report a problem naming it when it is
    never called from *self_test_source* — an INDEPENDENT re-implementation
    of the same property `scripts/check-traceability.py`'s
    `_selftest_dispatch_problems` checks (CR-02 / criterion 5).

    Pure: takes the dispatcher's already-extracted source as a parameter,
    does no I/O and no `inspect` call itself. Comments are stripped line
    by line (drop from the first `#`) before each symbol is searched for,
    so a commented-out dispatch does not satisfy the check — matching the
    sibling detector's own tradeoff (a `#` inside a string literal can
    only over-strip, producing a false positive, never a false negative).

    The duplication with `scripts/check-traceability.py` is deliberate,
    not accidental: two independent detectors in two different scripts
    mean that hiding a deleted dispatch requires editing both gates, not
    one.
    """
    stripped_lines = [line.split("#", 1)[0] for line in self_test_source.splitlines()]
    stripped_source = "\n".join(stripped_lines)
    problems: list[str] = []
    for symbol in symbols:
        if (symbol + "(") not in stripped_source:
            problems.append(
                f"{symbol!r} is never dispatched from self_test() — a "
                f"matrix artifact_link naming it is unenforced"
            )
    return problems


def _extract_whole_physical_line(source_text: str, anchor: str, source_file: str) -> str:
    """Habitat mode `whole-physical-line`: return the anchor's own physical
    line, stripped — lead-in text and all, not a de-contextualised
    substring.
    """
    matches = [line for line in source_text.splitlines() if anchor in line]
    if len(matches) != 1:
        raise _ContractAnchorError(
            anchor, source_file,
            f"matched {len(matches)} physical lines (need exactly 1)",
        )
    return matches[0].strip()


_QUOTED_EG_RE = re.compile(r'\(e\.g\.,\s*"(.*?)"\)')


def _extract_quoted_eg(source_text: str, anchor: str, source_file: str) -> str:
    """Habitat mode `quoted-eg`: locate the bullet line by its unique
    bullet-lead `anchor` (e.g. ``- **Accept**``, count 1), then return the
    contents of the ``(e.g., "...")`` parenthetical on that line via a
    group capture.
    """
    matches = [line for line in source_text.splitlines() if anchor in line]
    if len(matches) != 1:
        raise _ContractAnchorError(
            anchor, source_file,
            f"matched {len(matches)} physical lines (need exactly 1)",
        )
    m = _QUOTED_EG_RE.search(matches[0])
    if m is None:
        raise _ContractAnchorError(
            anchor, source_file,
            'bullet line resolved but no (e.g., "...") parenthetical found on it',
        )
    return m.group(1)


def _extract_heading_block(source_text: str, anchor: str, source_file: str) -> str:
    """Habitat mode `heading-block`: locate the LINE-START heading matching
    `anchor` — never a mid-sentence substring mention. The plain substring
    ``### Conclusion C1:`` occurs twice in the template (an earlier
    mid-sentence, backtick-quoted mention in the chain-numbering prose, and
    the line-start heading itself); a naive first-occurrence match hits the
    wrong one, so this walker line-start-anchors the regex instead. Walks
    forward to, but not including, the ``**Confidence:**`` terminator line,
    trims the blank line before it, and joins with newlines.
    """
    heading_re = re.compile(r"(?m)^" + re.escape(anchor) + r".*$")
    matches = list(heading_re.finditer(source_text))
    if len(matches) != 1:
        raise _ContractAnchorError(
            anchor, source_file,
            f"line-start heading matched {len(matches)} times (need exactly 1)",
        )
    start = matches[0].start()
    terminator = "**Confidence:**"
    term_idx = source_text.find(terminator, start)
    if term_idx == -1:
        raise _ContractAnchorError(
            anchor, source_file,
            f"heading resolved but no {terminator!r} terminator found after it",
        )
    block = source_text[start:term_idx]
    block_lines = block.split("\n")
    while block_lines and block_lines[-1].strip() == "":
        block_lines.pop()
    return "\n".join(block_lines)


_FENCED_TEXT_BLOCK_RE = re.compile(r"```text\n(.*?)\n```", re.S)


def _extract_fenced_block(source_text: str, anchor: str, source_file: str) -> str:
    """Habitat mode `fenced-block`: locate the unique preceding label
    `anchor` (e.g. ``**Chain format:**``, count 1), then return the
    contents of the next fenced ` ```text ` block after it. Deliberately
    NOT disambiguated by fence ordinal — the ` ```text ` opener occurs
    three times in the template, and an ordinal rule would silently
    retarget if a fence were ever added earlier in the document.
    """
    label_count = source_text.count(anchor)
    if label_count != 1:
        raise _ContractAnchorError(
            anchor, source_file,
            f"label matched {label_count} times (need exactly 1)",
        )
    label_idx = source_text.index(anchor)
    after = source_text[label_idx:]
    m = _FENCED_TEXT_BLOCK_RE.search(after)
    if m is None:
        raise _ContractAnchorError(
            anchor, source_file,
            'label resolved but no fenced ```text block found after it',
        )
    return m.group(1)


def _extract_backtick_span(source_text: str, anchor: str, source_file: str) -> str:
    """Habitat mode `backtick-span`: locate the anchor's own physical line,
    then return the FIRST backtick-delimited span on it whose content
    starts with the same GT-token prefix the anchor itself names (e.g.
    anchor ``Example: `GT-2`` names prefix ``GT-2``) — an explicit,
    deliberate requirement, not incidental first-span selection. The line
    this shares with `C-RENDER-EXAMPLE-PREFIX` carries two backtick spans;
    if a future template edit inserted a new span earlier on the line, the
    prefix requirement surfaces it as a mode-2 mismatch rather than
    silently extracting the wrong span.
    """
    matches = [line for line in source_text.splitlines() if anchor in line]
    if len(matches) != 1:
        raise _ContractAnchorError(
            anchor, source_file,
            f"matched {len(matches)} physical lines (need exactly 1)",
        )
    line = matches[0]
    spans = re.findall(r"`([^`]*)`", line)
    if not spans:
        raise _ContractAnchorError(
            anchor, source_file, "anchor line resolved but carries no backtick span"
        )
    prefix = anchor.split("`", 1)[1] if "`" in anchor else anchor
    for span in spans:
        if span.startswith(prefix):
            return span
    raise _ContractAnchorError(
        anchor, source_file,
        f"no backtick span on the anchor line starts with {prefix!r}",
    )


def _extract_contract_example(row: tuple[str, str, str, str]) -> str:
    """Resolve one `_CONTRACT_EXTRACTION_TABLE` row against the live source
    file and return the extracted example text (D-02, D-03, D-05) — this
    file is read at self-test time, not at import time, so an unresolvable
    anchor becomes a named FAIL rather than an import-time traceback.

    Dispatches on habitat mode; raises `_ContractAnchorError` when the
    row's anchor does not resolve to exactly one location. There is no
    fallback and no silent empty-string return (D-10). Locate and extract
    are two independent steps in every mode, so the two rows sharing
    template line 123 (`C-TEMPLATE-TRADEOFF`, `backtick-span`, and
    `C-RENDER-EXAMPLE-PREFIX`, `whole-physical-line`) cannot interfere with
    each other in either evaluation order.
    """
    fixture_id, source_file, habitat_mode, anchor = row
    source_path = REPO_ROOT / source_file
    try:
        source_text = source_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise _ContractAnchorError(
            anchor, source_file, f"could not read source file: {exc!r}"
        ) from exc

    if habitat_mode == "whole-physical-line":
        return _extract_whole_physical_line(source_text, anchor, source_file)
    if habitat_mode == "quoted-eg":
        return _extract_quoted_eg(source_text, anchor, source_file)
    if habitat_mode == "heading-block":
        return _extract_heading_block(source_text, anchor, source_file)
    if habitat_mode == "fenced-block":
        return _extract_fenced_block(source_text, anchor, source_file)
    if habitat_mode == "backtick-span":
        return _extract_backtick_span(source_text, anchor, source_file)
    raise _ContractAnchorError(anchor, source_file, f"unknown habitat mode {habitat_mode!r}")


# D-09: the qualification behind ROADMAP criterion 2, recorded in-source
# rather than glossed.
# (i) ROADMAP criterion 2 asked for the rubric's Verdict form "sourced the
#     same way" as the template examples extracted above -- read from
#     validation-rubric.md at runtime, not transcribed.
# (ii) validation-rubric.md Criterion 2's Rigorous descriptor carries prose,
#      not an example: "the Verdict cell records Accept, Challenge, or
#      Discard as a leading token followed by an em-dash and a specific
#      justification -- not the bare token alone." There is nothing to lift
#      verbatim, so only the vocabulary -- the three named tokens -- is
#      derivable from this sentence; the promise is half available (D-06).
# (iii) Measured at plan time: the rubric's own text spells the separator
#       by its English name, "em-dash", using U+002D HYPHEN-MINUS, and
#       contains no literal instance of U+2014 EM DASH anywhere in
#       Criterion 2 -- while output-template.md's Verdict Vocabulary
#       bullets DO carry the real character, both as the bullet separator
#       and inside their quoted `(e.g., "...")` examples. There is a form
#       to derive in the template; there is none to derive in the rubric.
# (iv) Therefore the em-dash-plus-justification *form* stays stated in the
#      harness (see the comment above `_VERDICT_FORM_RE`), where the
#      P183-D1 separator policy and P183-D2 empty-justification policy
#      already carry their own evidence -- and the *vocabulary* alone is
#      derived here, at self-test time, and asserted equal to
#      `_VERDICT_VOCAB` (D-07). This closes a real by-product gap:
#      `_VERDICT_VOCAB` was itself an unguarded hand-maintained
#      transcription of the rubric's wording before this guard existed.
# (v) The criterion is recorded qualified, not softened: this guard proves
#     the vocabulary tracks the rubric; it does not and cannot prove the
#     separator form does, because the rubric supplies no separator
#     example to check against.
_RUBRIC_SOURCE_FILE = "shared/spine/references/validation-rubric.md"

# The anchor here is a regex, not a literal string like every row in
# `_CONTRACT_EXTRACTION_TABLE` above, because the three vocabulary tokens
# are themselves the variable part being derived. The two FIXED phrases
# bounding the capture -- "records " and " as a leading token" -- are the
# real anchor; the pattern deliberately stops there rather than spanning
# the rest of the sentence ("followed by an em-dash and a specific
# justification"), so a harmless reword of the justification clause
# elsewhere in the same sentence does not trip it (D-07). Asserting on
# that wider prose was considered and rejected for exactly this reason.
_RUBRIC_VOCAB_RE = re.compile(r"records (\w+), (\w+), or (\w+) as a leading token")
_RUBRIC_VOCAB_ANCHOR_DESC = "records <token>, <token>, or <token> as a leading token"


def _derive_verdict_vocab_from_rubric(rubric_text: str) -> tuple[str, str, str]:
    """Derive the three Criterion 2 Verdict vocabulary tokens from the live
    `validation-rubric.md` text (D-07), lower-cased, in the order the
    rubric's own sentence lists them.

    Raises `_ContractAnchorError` -- reusing plan 01's exception so the
    guard has one catch shape, not two -- when the anchor does not resolve
    to exactly one match: absent, or ambiguous (D-10). There is no
    fallback and no silent default; an unresolvable anchor becomes a named
    FAIL in Guard A, never an uncaught exception.
    """
    matches = _RUBRIC_VOCAB_RE.findall(rubric_text)
    if len(matches) != 1:
        raise _ContractAnchorError(
            _RUBRIC_VOCAB_ANCHOR_DESC,
            _RUBRIC_SOURCE_FILE,
            f"matched {len(matches)} times (need exactly 1)",
        )
    a, b, c = matches[0]
    return (a.lower(), b.lower(), c.lower())


def _contract_fixture_result(fx: ContractFixture, text: str | None = None) -> bool:
    """Dispatch a fixture to the production function its kind exercises.

    ``text`` overrides `fx.text` as the payload under test when given —
    the seam DETECT-06's runtime-extracted string rides on (D-11). Every
    pre-existing call site keeps its current single-argument call and its
    current behaviour, because ``text=None`` defaults the payload to
    `fx.text`.
    """
    payload = fx.text if text is None else text
    if fx.kind == "verdict":
        return _verdict_conforms(payload)
    if fx.kind == "chain":
        return _chain_block_well_formed(payload)
    raise ValueError(f"unknown ContractFixture kind: {fx.kind!r}")


def _selftest_contract_pin(strict: bool = False) -> bool:
    """DETECT-01 item 13: the red-carry mechanism over `_CONTRACT_FIXTURES`.

    In default mode (``strict=False``), a mismatch against a fixture's
    ``expected`` value is tolerated — printed as `PINNED-RED` — only when the
    fixture's id is registered in `_DETECT01_PINNED_RED`; an unregistered
    mismatch fails the self-test. A fixture registered in
    `_DETECT01_PINNED_RED` whose result no longer mismatches is a STALE PIN
    and also fails — the mechanical forcing function that makes Phase 183 and
    Phase 184 remove what they own (see the registry's own block comment for
    this failure's documented limit: it fires only on a fixture that has
    flipped, so a partial correction leaves other pinned fixtures validly
    pinned).

    In strict mode (``strict=True``, used by `contract_pin_strict_report`),
    `_DETECT01_PINNED_RED` is ignored entirely: any mismatch fails, unpinned
    or not. This is the DETECT-01 red run.

    Contains no `assert` statement — `python3 -O` strips assertions, and a
    self-test whose only failure path is a stripped statement prints PASS and
    exits 0.
    """
    ok = True
    fixtures_by_id = {fx.id: fx for fx in _CONTRACT_FIXTURES}
    asserted_count = 0
    observed_count = 0

    # Guard D — fixture-table sanity (both modes): duplicate/empty id, empty
    # text, or a kind outside verdict/chain. This runs BEFORE the evaluation
    # loop below on purpose: `_contract_fixture_result` raises ValueError on an
    # unknown kind, so a kind check placed after the loop could never fire, and
    # a malformed table would surface as an uncaught traceback rather than a
    # named FAIL line. Fixtures Guard D rejects are skipped below rather than
    # dispatched. On a clean table every branch here is silent, so this
    # ordering leaves the recorded self-test output byte-unchanged.
    seen_ids: set[str] = set()
    bad_kind_ids: set[str] = set()
    for fx in _CONTRACT_FIXTURES:
        if not fx.id:
            print("self-test FAIL: contract_pin Guard D empty fixture id", file=sys.stderr)
            ok = False
        elif fx.id in seen_ids:
            print(
                f"self-test FAIL: contract_pin Guard D duplicate fixture id {fx.id}",
                file=sys.stderr,
            )
            ok = False
        else:
            seen_ids.add(fx.id)
        if not fx.text:
            print(
                f"self-test FAIL: contract_pin Guard D empty text for {fx.id}",
                file=sys.stderr,
            )
            ok = False
        if fx.kind not in ("verdict", "chain"):
            print(
                f"self-test FAIL: contract_pin Guard D unknown kind {fx.kind!r} "
                f"for {fx.id}",
                file=sys.stderr,
            )
            ok = False
            bad_kind_ids.add(fx.id)

    for fx in _CONTRACT_FIXTURES:
        if fx.id in bad_kind_ids:
            # Already reported by Guard D; dispatching would raise ValueError.
            continue
        if fx.expected is None:
            observed_count += 1
            observed_value = _contract_fixture_result(fx)
            print(
                f"contract_pin OBSERVED [DETECT-02 undecided] {fx.id}: "
                f"current code returns {observed_value} — no contract "
                f"expectation asserted; DETECT-02 must decide and document",
                file=sys.stderr,
            )
            continue

        asserted_count += 1
        observed_value = _contract_fixture_result(fx)
        mismatched = observed_value != fx.expected
        pinned = fx.id in _DETECT01_PINNED_RED

        if fx.kind == "chain" and mismatched:
            axes = _chain_failure_axes(fx.text)
            print(f"contract_pin AXES {fx.id}: {', '.join(axes)}", file=sys.stderr)

        if strict:
            if mismatched:
                print(
                    f"contract_pin STRICT-FAIL [{fx.owner}] {fx.id}: "
                    f"contract expects {fx.expected}, current code returns "
                    f"{observed_value} — carried until {fx.owner}",
                    file=sys.stderr,
                )
                ok = False
            continue

        if mismatched:
            if pinned:
                print(
                    f"contract_pin PINNED-RED [{fx.owner}] {fx.id}: contract "
                    f"expects {fx.expected}, current code returns "
                    f"{observed_value} — carried until {fx.owner}\n"
                    f"{_DETECT01_PINNED_RED[fx.id]}",
                    file=sys.stderr,
                )
            else:
                print(
                    f"self-test FAIL: contract_pin unregistered mismatch "
                    f"{fx.id}: contract expects {fx.expected}, current code "
                    f"returns {observed_value}",
                    file=sys.stderr,
                )
                ok = False
        else:
            if pinned:
                print(
                    f"self-test FAIL: contract_pin STALE PIN {fx.id} — "
                    f"{fx.owner} has corrected the check; delete this entry "
                    f"from _DETECT01_PINNED_RED and let the fixture assert "
                    f"normally",
                    file=sys.stderr,
                )
                ok = False

    # Guard A — verbatim drift (both modes), strengthened by DETECT-06
    # (Phase 187, D-13). Two paths, split by whether the fixture's id has a
    # row in `_CONTRACT_EXTRACTION_TABLE`:
    #   - A fixture WITH a row takes the strengthened path: resolve the
    #     anchor against the live source file, assert byte equality against
    #     the pinned literal, and run the detector on the EXTRACTED text
    #     (D-11). Three named failure modes (D-12), no fallback to the
    #     substring check on any of them (D-10) — a guard that quietly
    #     degrades to the copy it replaces is the silent-drift mode this
    #     phase exists to close.
    #   - A fixture WITHOUT a row (the two frozen-corpus fixtures
    #     `C-RENDER-BACKTICK` and `C-RENDER-BLOCKQUOTE-BOLD`, whose sources
    #     are frozen analyses where anchor extraction does not apply) keeps
    #     the original substring check, unchanged (D-13).
    _extraction_by_id = {row[0]: row for row in _CONTRACT_EXTRACTION_TABLE}
    for fx in _CONTRACT_FIXTURES:
        if fx.verbatim_from is None:
            continue

        row = _extraction_by_id.get(fx.id)
        if row is None:
            source_path = REPO_ROOT / fx.verbatim_from
            try:
                source_text = source_path.read_text(encoding="utf-8")
            except OSError as exc:
                print(
                    f"self-test FAIL: contract_pin Guard A could not read "
                    f"{fx.verbatim_from} for {fx.id}: {exc!r}",
                    file=sys.stderr,
                )
                ok = False
                continue
            if fx.text not in source_text:
                print(
                    f"self-test FAIL: contract_pin Guard A {fx.id} text is not a "
                    f"literal substring of {fx.verbatim_from} — verbatim lift drifted",
                    file=sys.stderr,
                )
                ok = False
            continue

        # Strengthened path (D-11, D-12).
        try:
            extracted = _extract_contract_example(row)
        except _ContractAnchorError as exc:
            print(
                f"self-test FAIL: contract_pin Guard A [mode 1: anchor "
                f"unresolved] {fx.id}: anchor {exc.anchor!r} in "
                f"{exc.source_file} did not resolve ({exc.detail}) — "
                f"remedy: re-anchor the guard",
                file=sys.stderr,
            )
            ok = False
            continue

        if extracted != fx.text:
            print(
                f"self-test FAIL: contract_pin Guard A [mode 2: extraction "
                f"mismatch] {fx.id}: the template's example changed and the "
                f"fixture literal needs updating\n"
                f"  extracted: {extracted!r}\n"
                f"  literal:   {fx.text!r}",
                file=sys.stderr,
            )
            ok = False
            continue

        observed = _contract_fixture_result(fx, extracted)
        if observed != fx.expected:
            print(
                f"self-test FAIL: contract_pin Guard A [mode 3: DETECTOR "
                f"REGRESSION against the canonical contract] {fx.id} — the "
                f"extracted text equals the pinned literal, but the "
                f"detector no longer agrees with the canonical contract: "
                f"expected {fx.expected}, observed {observed}",
                file=sys.stderr,
            )
            ok = False

    # Guard A (rubric branch) — DETECT-06 (Phase 187, D-07/D-09/D-13). Runs
    # once per call, in BOTH modes — placed outside `if not strict:` below,
    # same as the template branch above, so no edit to
    # `contract_pin_strict_report` is needed to inherit coverage. The three
    # Criterion 2 Verdict vocabulary tokens are derived from the live
    # rubric at self-test time and asserted EQUAL to `_VERDICT_VOCAB` —
    # order matters (D-07): a reordering that changed which token leads
    # would be a genuine rubric change worth surfacing, so this is `==`,
    # not set membership.
    try:
        rubric_text: str | None = (REPO_ROOT / _RUBRIC_SOURCE_FILE).read_text(
            encoding="utf-8"
        )
    except OSError as exc:
        print(
            f"self-test FAIL: contract_pin Guard A [rubric anchor "
            f"unresolved] could not read {_RUBRIC_SOURCE_FILE}: {exc!r} — "
            f"remedy: re-anchor the guard",
            file=sys.stderr,
        )
        ok = False
        rubric_text = None

    derived_vocab: tuple[str, str, str] | None = None
    if rubric_text is not None:
        try:
            derived_vocab = _derive_verdict_vocab_from_rubric(rubric_text)
        except _ContractAnchorError as exc:
            print(
                f"self-test FAIL: contract_pin Guard A [rubric anchor "
                f"unresolved] anchor {exc.anchor!r} in {exc.source_file} "
                f"did not resolve ({exc.detail}) — remedy: re-anchor the "
                f"guard",
                file=sys.stderr,
            )
            ok = False

    if derived_vocab is not None and derived_vocab != _VERDICT_VOCAB:
        print(
            f"self-test FAIL: contract_pin Guard A [rubric vocabulary "
            f"mismatch] validation-rubric.md Criterion 2's derived "
            f"vocabulary {derived_vocab!r} and _VERDICT_VOCAB "
            f"{_VERDICT_VOCAB!r} have diverged",
            file=sys.stderr,
        )
        ok = False
        # A divergent vocabulary means there is nothing sound to build the
        # two derived-fixture checks on below; do not cascade a second,
        # confusing FAIL from comparing against an already-known-bad value.
        derived_vocab = None

    if derived_vocab is not None:
        # Both halves of the rubric's Criterion 2 clause become fixtures
        # (D-08): construct the em-dash and bare cell strings from the
        # DERIVED tokens — never hard-coded — so a rubric vocabulary
        # change surfaces as a mismatch here rather than leaving a stale
        # literal silently in place (D-11). `leading` is the first derived
        # token, matching the order-sensitive comparison above.
        leading = derived_vocab[0].capitalize()
        constructed_emdash = f"{leading} \u2014 rubric-derived vocabulary, not transcribed"
        constructed_bare = leading

        emdash_fx = fixtures_by_id.get("V-RUBRIC-CRIT2-EMDASH")
        bare_fx = fixtures_by_id.get("V-RUBRIC-CRIT2-BARE")

        if emdash_fx is not None and bare_fx is not None:
            if constructed_emdash != emdash_fx.text or constructed_bare != bare_fx.text:
                # Mirrors mode 2 (extraction mismatch) above: the literal
                # is retained as the diff-reviewable record; the live
                # assertion runs on what the rubric says today (D-11).
                print(
                    f"self-test FAIL: contract_pin Guard A [rubric mode 2: "
                    f"extraction mismatch] the rubric's derived vocabulary "
                    f"moved and a fixture literal needs updating\n"
                    f"  constructed emdash: {constructed_emdash!r}\n"
                    f"  literal emdash:     {emdash_fx.text!r}\n"
                    f"  constructed bare:   {constructed_bare!r}\n"
                    f"  literal bare:       {bare_fx.text!r}",
                    file=sys.stderr,
                )
                ok = False
            else:
                # Mode 3 (detector regression) — the phase's whole reason
                # for existing, so it carries its own distinctly-worded
                # message rather than sharing the extraction-plumbing text
                # above.
                emdash_observed = _contract_fixture_result(emdash_fx, constructed_emdash)
                bare_observed = _contract_fixture_result(bare_fx, constructed_bare)
                if emdash_observed != emdash_fx.expected or bare_observed != bare_fx.expected:
                    print(
                        f"self-test FAIL: contract_pin Guard A [rubric "
                        f"mode 3: DETECTOR REGRESSION against the "
                        f"canonical contract] the constructed cells equal "
                        f"their pinned literals, but the detector no "
                        f"longer agrees with the canonical contract: "
                        f"emdash expected {emdash_fx.expected} observed "
                        f"{emdash_observed}, bare expected "
                        f"{bare_fx.expected} observed {bare_observed}",
                        file=sys.stderr,
                    )
                    ok = False

        # Anti-blanket-pass sweep (D-08): each of the three derived tokens,
        # independently, in both directions — six checks total, so a
        # blanket-pass predicate cannot satisfy the guard on one token's
        # evidence alone. These checks add no fixture and no labelled
        # result line — they are branches inside this thirteenth self-test
        # item — so self_test()'s exactly-thirteen contract is preserved
        # (D-13).
        for token in derived_vocab:
            token_cap = token.capitalize()
            emdash_form = f"{token_cap} \u2014 justification"
            bare_form = token_cap
            if not _verdict_conforms(emdash_form):
                print(
                    f"self-test FAIL: contract_pin Guard A [rubric "
                    f"anti-blanket-pass] token {token_cap!r} em-dash form "
                    f"{emdash_form!r} does not conform but must",
                    file=sys.stderr,
                )
                ok = False
            if _verdict_conforms(bare_form):
                print(
                    f"self-test FAIL: contract_pin Guard A [rubric "
                    f"anti-blanket-pass] token {token_cap!r} bare form "
                    f"{bare_form!r} conforms but must not",
                    file=sys.stderr,
                )
                ok = False

    if not strict:
        # Guard B — registry drift (default mode): every _DETECT01_PINNED_RED
        # id must name a real fixture in _CONTRACT_FIXTURES.
        for pinned_id in _DETECT01_PINNED_RED:
            if pinned_id not in fixtures_by_id:
                print(
                    f"self-test FAIL: contract_pin Guard B unregistered "
                    f"fixture id in _DETECT01_PINNED_RED: {pinned_id}",
                    file=sys.stderr,
                )
                ok = False

        # Guard C — owner whitelist (default mode): every registry reason
        # string must mention DETECT-02 or DETECT-03, bounding the registry to
        # the two requirements that close it, so an unrelated future
        # regression cannot be silenced without a visibly false ownership
        # claim in a reviewed diff.
        for pinned_id, reason in _DETECT01_PINNED_RED.items():
            if "DETECT-02" not in reason and "DETECT-03" not in reason:
                print(
                    f"self-test FAIL: contract_pin Guard C reason for "
                    f"{pinned_id} names neither DETECT-02 nor DETECT-03",
                    file=sys.stderr,
                )
                ok = False

    pinned_red_ids = list(_DETECT01_PINNED_RED.keys())
    n_pinned_red = len(pinned_red_ids)
    # Look up by `.get`, not `[]`: a registry id naming no fixture is exactly
    # the drift Guard B reports, and subscripting here would turn that named
    # FAIL into an uncaught KeyError traceback that buries it. Such an id is
    # counted in `n_pinned_red` (it IS a registry entry) but belongs to no
    # owner tally, so the two per-owner counts can legitimately sum to less
    # than `n_pinned_red` while Guard B is failing.
    n_detect02 = sum(
        1 for i in pinned_red_ids
        if (fx := fixtures_by_id.get(i)) is not None and fx.owner == "DETECT-02"
    )
    n_detect03 = sum(
        1 for i in pinned_red_ids
        if (fx := fixtures_by_id.get(i)) is not None and fx.owner == "DETECT-03"
    )

    print(
        f"contract_pin: {asserted_count} asserted fixtures, {observed_count} "
        f"observation-only, {n_pinned_red} PINNED-RED carried (DETECT-02: "
        f"{n_detect02}, DETECT-03: {n_detect03}) — this red state is the "
        f"DETECT-01 deliverable, not a passing invariant"
    )

    return ok


def contract_pin_strict_report() -> int:
    """The DETECT-01 red run: the same fixtures, `_DETECT01_PINNED_RED` ignored.

    Its exiting 0 is the completeness check for DETECT-02 and DETECT-03 —
    because the default-mode STALE PIN failure only detects a fixture that
    has flipped and is therefore blind to a partial correction that leaves
    other pinned fixtures validly pinned. Phase 183 and Phase 184 must run
    this, not rely on a green `--self-test`.

    Reproduce with:
        python3 -c "import importlib.util as u, sys; \\
s = u.spec_from_file_location('qh', 'scripts/check-quality-harness.py'); \\
mm = u.module_from_spec(s); sys.modules['qh'] = mm; s.loader.exec_module(mm); \\
sys.exit(mm.contract_pin_strict_report())"
    """
    return 0 if _selftest_contract_pin(strict=True) else 1


def _selftest_limitation1_chainlabels() -> bool:
    """FIX-CONTRACT-01 limitation 1: `_chain_ids()` recognizes a document's
    own bare single-letter §4 lead-in convention (e.g. "C1", "C2") when used
    consistently (>= _MIN_BARE_LABEL_FAMILY_SIZE times), but a single
    incidental bold lead-in that happens to match the bare shape is not
    mistaken for a one-chain family (quick task 260724-bq3 Task 1).
    """
    ok = True

    family_section4 = (
        "**C1 — first chain:**\n"
        "GT-1 -> intermediate claim -> conclusion one.\n\n"
        "**C2 — second chain:**\n"
        "GT-2 -> intermediate claim -> conclusion two.\n"
    )
    family_ids = _chain_ids(family_section4)
    if family_ids != ["C1", "C2"]:
        print(
            f"self-test FAIL: limitation1 bare-letter chain-label family "
            f"expected ['C1', 'C2'], got {family_ids!r}",
            file=sys.stderr,
        )
        ok = False

    lone_section4 = (
        "**A/B test:** a single incidental bold lead-in that happens to "
        "match the bare single-letter shape but is not a chain family.\n\n"
        "GT-1 -> intermediate claim -> conclusion.\n"
    )
    lone_ids = _chain_ids(lone_section4)
    if lone_ids:
        print(
            f"self-test FAIL: limitation1 lone incidental bold lead-in "
            f"spuriously produced a bare-letter chain id: {lone_ids!r} — "
            f"the family-size guard did not fire",
            file=sys.stderr,
        )
        ok = False

    return ok


def _selftest_gap5_conclusion_heading() -> bool:
    """GAP-5: the `### Conclusion C1:` heading form is recognized end-to-end.

    `output-template.md` §4 prescribes this form verbatim — "Number each
    `### Conclusion:` block in this section `C1`, `C2`, ... in document order
    (e.g., `### Conclusion C1: [Conclusion text]`)" — but `_CHAIN_HEADING_RE`
    anchored its label immediately after the hashes, so only the "Chain "
    prefixed and bare forms parsed. The prescribed form produced zero ids.

    **The failure direction is silently green, which is why this fixture pins
    the whole path (ids -> blocks -> defect record) rather than the regex
    alone.** With zero ids, `_chain_blocks()` falls back to returning the whole
    section as ONE block; that block contains at least one well-formed chain
    somewhere, so `any()` matches and `malformed_chain_blocks` reports 0 on a
    document with genuinely malformed chains. Observed 2026-08-30 on a live
    agent run: raw score `chain_blocks: 1, malformed: 0, untraced: 7 of 7`;
    the same document with headings normalized scored `chain_blocks: 7,
    malformed: 2, untraced: 0`.

    Controls: (a) positive, colon separator; (b) positive, em-dash separator;
    (c) id normalization, so an abbreviated "(C1)" citation still traces;
    (d) anti-vacuity end-to-end — a two-chain section with exactly one
    malformed chain must report 2 blocks and 1 malformed, which is precisely
    what the pre-fix fallback could not do; (e) negative, a bare
    "**Conclusion:**" lead-in carries no label and must not mint an id;
    (f) negative, a heading with no label and no separator likewise.
    """
    ok = True

    def _fail(msg: str) -> None:
        nonlocal ok
        print(f"self-test FAIL: gap5_conclusion_heading {msg}", file=sys.stderr)
        ok = False

    well_formed = "GT-1 (a) + GT-2 (b)\n-> intermediate claim\n-> the conclusion"
    malformed = "GT-3 (c) + GT-4 (d) -> lone hop with no intermediate"

    # (a) colon separator — the exact prescribed form.
    colon = (
        f"### Conclusion C1: first\n\n{well_formed}\n\n"
        f"### Conclusion C2: second\n\n{well_formed}\n"
    )
    if _chain_ids(colon) != ["Conclusion C1", "Conclusion C2"]:
        _fail(f"(a) colon form expected two ids, got {_chain_ids(colon)!r}")

    # (b) em-dash separator.
    dash = (
        f"### Conclusion C1 - first\n\n{well_formed}\n\n"
        f"### Conclusion C2 - second\n\n{well_formed}\n"
    ).replace(" - ", " \u2014 ")
    if _chain_ids(dash) != ["Conclusion C1", "Conclusion C2"]:
        _fail(f"(b) em-dash form expected two ids, got {_chain_ids(dash)!r}")

    # (c) normalization, so "(C1)" in section 6 traces to a stored
    #     "Conclusion C1".
    if _normalize_chain_id("Conclusion C1") != "c1":
        _fail(
            f"(c) expected 'Conclusion C1' to normalize to 'c1', got "
            f"{_normalize_chain_id('Conclusion C1')!r}"
        )

    # (d) anti-vacuity: one well-formed chain and one malformed chain must
    #     report as two blocks with exactly one malformed. Pre-fix this
    #     collapsed to one block and zero malformed — a green verdict
    #     produced by not looking.
    mixed = (
        f"### Conclusion C1: sound\n\n{well_formed}\n\n"
        f"### Conclusion C2: broken\n\n{malformed}\n"
    )
    blocks = _chain_blocks(mixed)
    if len(blocks) != 2:
        _fail(f"(d) expected 2 chain blocks, got {len(blocks)}")
    else:
        bad = [b for b in blocks if not _chain_block_well_formed(b)]
        if len(bad) != 1:
            _fail(
                f"(d) expected exactly 1 malformed block, got {len(bad)} — "
                f"the whole-section fallback may have masked it"
            )

    # (e) negative: a bare bold "Conclusion:" lead-in carries no label.
    if _chain_ids("**Conclusion:** the analysis recommends option B.\n"):
        _fail("(e) bare '**Conclusion:**' lead-in spuriously minted a chain id")

    # (f) negative: a heading with no label and no separator.
    if _chain_ids("### Conclusion\n\nsome prose\n"):
        _fail("(f) label-less '### Conclusion' heading spuriously minted an id")

    return ok


def _selftest_gap6_composition_heads() -> bool:
    """GAP-6: a chain may compose on a prior conclusion, and the cycles that
    admits are detected.

    Observed 2026-08-30: a live analysis scored 2 of 7 chains malformed, both
    of them compositions — a trade-off collapse headed `GT-5 (...) + C1 + C2
    + C3 (...)` and a second-order extension headed `GT-5 (...) + C6 (...)`.
    Isolated, `GT-5 (label) + GT-2 (label)` measured well-formed while
    `GT-5 (label) + C6 (label)` measured malformed, whatever the arrow form.

    Controls (a)-(c) pin the widening, including the GT-only base case so the
    change cannot silently stop checking the shape it always checked.
    Controls (d)-(g) pin `_chain_dependency_defects`, which is the price of
    the widening: GT-only heads were acyclic by construction, and chain refs
    remove that guarantee.
    """
    ok = True

    def _fail(msg: str) -> None:
        nonlocal ok
        print(f"self-test FAIL: gap6_composition_heads {msg}", file=sys.stderr)
        ok = False

    tail = "\n-> intermediate claim\n-> the conclusion"

    # (a) GT + chain composition head — the shape that regressed.
    if not _chain_block_well_formed("GT-5 (label) + C6 (buy first)" + tail):
        _fail("(a) 'GT-5 (label) + C6 (label)' head scored malformed")

    # (b) chain-only head.
    if not _chain_block_well_formed("C1 + C2" + tail):
        _fail("(b) chain-only head 'C1 + C2' scored malformed")

    # (c) NON-VACUITY: the GT-only base case must still be well-formed, and a
    #     one-hop chain must still be malformed. A widening that accepted
    #     everything would pass (a) and (b) while checking nothing.
    if not _chain_block_well_formed("GT-1 (a) + GT-2 (b)" + tail):
        _fail("(c) GT-only head regressed to malformed")
    if _chain_block_well_formed("GT-1 (a) + GT-2 (b) -> lone hop"):
        _fail("(c) one-hop chain wrongly scored well-formed — widening is vacuous")

    def _section(*pairs: tuple[str, str]) -> str:
        return "\n\n".join(
            f"### Conclusion {cid}: t\n\n{head}{tail}" for cid, head in pairs)

    # (d) clean DAG: C2 composes on C1, which is GT-headed.
    clean = _section(("C1", "GT-1 (a) + GT-2 (b)"), ("C2", "GT-3 (c) + C1 (d)"))
    dep = _chain_dependency_defects(clean)
    if dep["cycles"] or dep["ungrounded"]:
        _fail(f"(d) clean DAG reported defects: {dep!r}")

    # (e) two-node cycle.
    cyc = _section(("C1", "GT-1 (a) + C2 (b)"), ("C2", "GT-2 (c) + C1 (d)"))
    if sorted(_chain_dependency_defects(cyc)["cycles"]) != ["c1", "c2"]:
        _fail(
            f"(e) two-node cycle not reported: "
            f"{_chain_dependency_defects(cyc)!r}"
        )

    # (f) self-loop.
    selfloop = _section(("C1", "GT-1 (a) + C1 (b)"))
    if _chain_dependency_defects(selfloop)["cycles"] != ["c1"]:
        _fail(
            f"(f) self-loop not reported: "
            f"{_chain_dependency_defects(selfloop)!r}"
        )

    # (h) scope guard: a head-less block is a SHAPE defect owned by
    #     `_chain_block_well_formed`, not a grounding defect. Reporting it
    #     here too would double-count. Pinned because the frozen corpus
    #     contains exactly this shape (condA-P3, condB-P2).
    headless = _section(("C1", "GT-1 (a) + GT-2 (b)")) + (
        "\n\n### Conclusion C2: t\n\n1. **2nd order:** an effect with no "
        "chain head at all\n")
    dep = _chain_dependency_defects(headless)
    if "c2" in dep["ungrounded"]:
        _fail(f"(h) head-less block wrongly reported ungrounded: {dep!r}")

    # (g) ungrounded: C2 reaches no ground truth by any path.
    ungrounded = _section(("C1", "GT-1 (a) + GT-2 (b)"), ("C2", "C8 + C9"))
    dep = _chain_dependency_defects(ungrounded)
    if dep["ungrounded"] != ["c2"]:
        _fail(f"(g) ungrounded chain not reported: {dep!r}")
    if dep["cycles"]:
        _fail(f"(g) ungrounded chain spuriously reported as a cycle: {dep!r}")

    return ok


def _selftest_gap8_bold_chain_labels() -> bool:
    """GAP-8: a bold-labelled chain is not read as citing itself.

    Observed 2026-08-31 on PR-P1 run 4 (v8.24.0 verified body): an analysis
    labelling its chains `**C1 — …**` rather than `### Conclusion C1:` scored
    all eight chains BOTH self-cyclic and ungrounded — every finding artifact.

    `_chain_ids` / `_chain_blocks` recognise two label shapes,
    `_CHAIN_HEADING_RE` (hash-led) and `_CHAIN_BOLD_RE` (bold-led), and start
    a block at whichever matched. `_chain_head_refs`'s skip guard covered only
    the first, so the bold label stayed inside the block and was read as the
    head — reproducing verbatim the failure that guard's own comment predicts.

    Controls (a)-(c) pin the fix. Control (d) is the anti-overreach control
    that forces the `idx == 0` restriction: `_CHAIN_BOLD_RE`'s label
    alternation includes `[A-Z]{2}-\\d+`, so a fully-bolded HEAD line matches
    it too, and a blanket "skip any bold-label line" guard would swallow that
    head. Controls (e)-(f) are non-vacuity: the widening must not neuter the
    cycle and grounding checks it operates on, nor the heading form.

    Fault injections, each failing the control that owns it:

    - reverting the guard entirely          -> (a), (b), (c), (d), (f)
    - widening `idx == 0` to every line     -> (d) ALONE
    - neutering `_chain_dependency_defects` -> (e), (f)

    Injection 2 failing (d) and nothing else is the load-bearing measurement:
    it proves (d) is the only control holding the `idx == 0` restriction, so
    the restriction cannot be relaxed back to a blanket skip silently.
    """
    ok = True

    def _fail(msg: str) -> None:
        nonlocal ok
        print(f"self-test FAIL: gap8_bold_chain_labels {msg}", file=sys.stderr)
        ok = False

    tail = "\n-> intermediate claim\n-> the conclusion"

    def _section(*pairs: tuple[str, str]) -> str:
        return "\n\n".join(
            f"**{cid} — t**\n\n{head}{tail}" for cid, head in pairs)

    # (a) the regressing shape: a bold label above a GT head. The label must
    #     be skipped and the GTs read — NOT `(set(), {'C1'})`.
    if _chain_head_refs(f"**C1 — t**\n\nGT-1 (a) + GT-2 (b){tail}") != (
        {"GT-1", "GT-2"}, set()
    ):
        _fail("(a) bold-labelled GT head not read as its own head")

    # (b) a bold-labelled COMPOSING chain still reports its real chain ref,
    #     so the skip did not cost the composition signal GAP-6 added.
    if _chain_head_refs(f"**C2 — t**\n\nGT-3 (c) + C1 (d){tail}") != (
        {"GT-3"}, {"C1"}
    ):
        _fail("(b) bold-labelled composing head lost its chain ref")

    # (c) end-to-end on the run-4 shape: a clean two-chain DAG under bold
    #     labels reports neither cycles nor ungrounded chains.
    dep = _chain_dependency_defects(
        _section(("C1", "GT-1 (a) + GT-2 (b)"), ("C2", "GT-3 (c) + C1 (d)")))
    if dep["cycles"] or dep["ungrounded"]:
        _fail(f"(c) clean bold-labelled DAG reported defects: {dep!r}")

    # (d) ANTI-OVERREACH: a bolded HEAD line below the label is still read.
    #     Pins `idx == 0`; a blanket bold skip returns `(set(), set())` here
    #     and turns a well-formed grounded chain into a head-less one.
    if _chain_head_refs(f"**C1 — t**\n\n**GT-1 (a) + GT-2 (b)**{tail}") != (
        {"GT-1", "GT-2"}, set()
    ):
        _fail("(d) bolded head line below the label was wrongly skipped")

    # (e) NON-VACUITY: a real cycle under bold labels is still detected, and
    #     the heading form is untouched. A guard that skipped everything
    #     would pass (a)-(d) while detecting nothing.
    cyc = _chain_dependency_defects(
        _section(("C1", "GT-1 (a) + C2 (b)"), ("C2", "GT-2 (c) + C1 (d)")))
    if sorted(cyc["cycles"]) != ["c1", "c2"]:
        _fail(f"(e) bold-labelled two-node cycle not reported: {cyc!r}")
    if _chain_head_refs(f"### Conclusion C1: t\n\nGT-1 (a) + GT-2 (b){tail}") != (
        {"GT-1", "GT-2"}, set()
    ):
        _fail("(e) heading-form head regressed")

    # (f) NON-VACUITY: a genuinely ungrounded bold-labelled chain is still
    #     reported, and does not come back as a cycle.
    ung = _chain_dependency_defects(
        _section(("C1", "GT-1 (a) + GT-2 (b)"), ("C2", "C8 + C9")))
    if ung["ungrounded"] != ["c2"]:
        _fail(f"(f) bold-labelled ungrounded chain not reported: {ung!r}")
    if ung["cycles"]:
        _fail(f"(f) ungrounded chain spuriously reported as a cycle: {ung!r}")

    return ok


def _selftest_render_contract() -> bool:
    """Phase 11 (CONTRACT-01, CONTRACT-02, CONTRACT-04): the emission
    rendering contract's own worked examples in `output-template.md` §4
    (chain form), §6 (citation form) and the Verdict Vocabulary
    (current-constraint expiry) are scored by the unmodified detectors
    with the expected verdicts, sourced from the shipped canonical bytes.

    Observed 2026-08-31 on run 4 (v8.24.0 verified body): GAP-9's hop
    broken mid-bracket across physical lines, and GAP-10's expiry
    qualifier hoisted into the verdict token slot, both rendered
    non-conformingly while the template gave no worked counter-example to
    check against. Phase 11 Plan 01 (11-01) closed that gap by authoring
    one conforming and one or two non-conforming examples for each shape
    directly in `output-template.md`, behind unique fenced-block anchors.

    D-02 keeps `_chain_block_well_formed` byte-unchanged — every control
    here calls it from outside; none of them, nor anything in this file,
    modifies it.

    Controls (a)-(b) pin the eighteen measured verdicts. Control (c) pins
    minimality of the wrap counter-example: it must differ from the
    conforming example by exactly the inserted continuation line, so the
    counter-example demonstrably teaches the wrap rule and nothing else.
    Control (d) pins the same-hops property of the numbered
    counter-example: it renders THE SAME hops as the conforming example,
    not a different chain that happens to fail. Control (e) pins the
    Case B verdict pair. Control (f) pins citation credit for both
    accepted forms — inline and closure-ledger — and proves the same
    otherwise-untraced claim becomes traced purely because the ledger row
    is present. Control (g) is NON-VACUITY: it re-asserts two
    long-standing base cases from outside this item, so a widened
    detector that scored everything `True` (or everything `False`) could
    not pass (b)/(e) by accident. Plan 13-02 (CHAINHEAD-05/CHAINHEAD-06)
    added three more (b) controls scoring `R-HEAD-PROSE-BAD`,
    `R-HEAD-CHAINREF` and `R-HEAD-ALLCHAIN`: the first two are the
    same bytes but for one token (`C2's threshold` vs `C2 (threshold)`)
    scored in opposite directions — a detector accepting both would fail
    this pair by design, which is why widening `_chain_block_well_formed`
    is the wrong fix; the third covers the all-`Cn` head shape GAP-6
    widened `_CHAIN_REF_TOKEN` for. Plan 13-08 (BL-01) added a fourth,
    `R-HEAD-PROSE-MID`: the same possessive-prose violation as
    `R-HEAD-PROSE-BAD` but in a non-final head position, pinning the
    measured bound R7 now discloses — the mechanical check reaches only
    the last input before the first arrow, so this fixture is expected
    WELL-FORMED even though R7 forbids the violation everywhere. Plan
    13-09 (BL-02) added a fifth and sixth, `R-HEAD-GTHOP-BAD` and
    `R-HEAD-GTHOP-OK`: the same hop differing only in whether it leads
    with a `GT-N` identifier, scored in opposite directions — this pins
    both halves of R9, the head-only scope note's GT-leading-hop refusal
    and the rewrite it prescribes. Plan 13-19 (CR-02 fixture half) added
    a seventh, `R-HEAD-GTHOP-LATE`: the same offending hop as
    `R-HEAD-GTHOP-BAD` moved from first position to last, scored
    WELL-FORMED even though R9 forbids the violation everywhere — R9's
    exact analogue of `R-HEAD-PROSE-MID`, pinning the position the check
    does not reach rather than merely stating it. Control
    (p), added by plan 11-09 (gap 2's second half), is the CONSUMPTION
    FLOOR: `_get` records every id it is asked for, and the floor asserts
    that set against a locked twenty-seven-id set written inline — plus that
    `fixtures` matches the same
    locked set whenever `problems` is empty (the exact condition CR-02's
    reproduction left silent), plus that every locked id is either
    scored by a control or named in a reported problem. A fixture that is
    extracted but never requested, or requested but never scored or
    reported, now fails by name instead of being silently skipped by
    controls (b)-(f)'s `is not None` guards. Plan 13-05 (CR-01,
    `13-VERIFICATION.md`) replaced the third arm's extraction test —
    absence from the extracted-fixtures mapping — with membership in a
    plain `set[str]` recorder written only by the `_score_chain` /
    `_score_verdict` / `_score_traced` / `_score_ledger` wrappers controls
    (b), (e) and (f) route through — the reproduction that motivated this
    was deleting the three (b) chain-head verdict-assertion blocks
    entirely: the fixtures still extracted cleanly, so the old
    extraction-only floor stayed green with zero scoring behaviour left.
    Control (s), added by the same plan, drives the new floor's pure helper
    (`_render_unscored_fixture_ids`) directly with synthetic
    locked/scored/problem inputs. Plan 13-10 (BL-03, `13-VERIFICATION.md`)
    found that membership-set recorder itself forgeable two ways — a bare
    `.update({...})` writing ids with no scorer ever called, and a wrapper
    genuinely called but its verdict discarded — both left this sub-check
    PASSED. The wrappers now record each scorer's boolean VERDICT into
    `scored_verdicts: dict[str, list[bool]]`, a fourth arm
    (`_render_verdict_floor_problems`) compares every locked id's recorded
    sequence against an inline expected-verdict table, and a fifth arm
    (`_render_chain_verdict_floor_problems`) independently re-scores the
    thirteen chain-family fixtures from `fixtures` with the frozen detector,
    consulting no recorder at all. Control (v) proves each wrapper's return
    equals its raw scorer's return AND the recorder holds that same value,
    so a fabricated verdict fails by name. Control (w) mirrors (s) for both
    new helpers. Control (t) survives as a source-level diff-review
    backstop over the recorder's write idioms — it is explicitly NOT what
    closes the fail-OPEN shape; that is arms 4a/4b and control (v). Control
    (q),
    also added by plan 11-09, drives `_render_fixture_accounting_problems()`
    — the mode 3 replacement in `_render_contract_fixtures()` — directly
    with a clean case, a duplicated-id case and a count-mismatch case,
    proving WR-06's unreachable membership check has been replaced by
    something that can actually fire. Control (u), added by plan 13-06
    (CR-02, criterion 5), is an INDEPENDENT second detector of the same
    dispatch-reachability property `scripts/check-traceability.py`'s
    `_selftest_dispatch_problems` checks — every `_selftest_*` symbol a
    matrix `artifact_link` names must be called from `self_test()`, not
    merely defined. It derives the symbol set from the sibling script's
    source (`_matrix_named_selftest_symbols`), asserts a non-vacuity floor
    over that set, then checks `self_test()`'s own comment-stripped source
    with `_dispatch_reachability_problems` — the arm that goes red when
    Item 25's `_selftest_chain_detector_pin` dispatch is deleted, run from
    Item 24 (still dispatched at that moment) precisely so the guard
    cannot be defeated by the same mutation it guards.

    Controls (h)-(l) close Case A (CONTRACT-03) and pin the reconciled
    multi-hop head form (CONTRACT-05) across FOUR canonical surfaces, per
    D-04: a rule shipped uncontrolled lands in the exact defect class
    PROJECT.md's through-line names — a form stated in more places than
    anything checks. Plan 11-07 (CR-01, `11-VERIFICATION.md` gap 1) added
    the third surface, `shared/spine/references/validation-rubric.md`: it
    is canonical because it is the rubric the agent scores its own
    emission against at Phase 5 Criterion 4, and it shipped for one
    milestone stating one of this gate's own enumerated contradiction
    phrasings (`too long for one line wraps`) while sitting outside the
    gate's scan scope — CR-01's fix note is what closes that gap. Plan
    13-20 (CR-03, `13-VERIFICATION.md` gap 2) added the fourth surface,
    `shared/references/reason-upward.md`: it is canonical because it is
    the sole source of the shipped, slash-invocable `first-principles/
    skills/reason-upward/SKILL.md`, and it shipped stating the chain form
    with none of R6-R9 present, invisible to this gate's contradiction
    scan — CR-03's fix note is what closes that gap.

    Plan 11-08 (CR-02/WR-01, `11-VERIFICATION.md` gap 2) widened control
    (h) from a two-registry MEMBERSHIP LOCK to a by-value lock over every
    registry the rendering-contract mechanism depends on — one field per
    entry of `_RENDER_REGISTRY_FIELDS`, the count stated once on
    `_RenderRegistrySnapshot` and derived here (WR-06) — and added
    control (h2). The verifier reproduced, on a scratch copy, that
    replacing `_RENDER_CONTRACT_EXTRACTION_TABLE` with an empty tuple made
    the extraction loop run zero times — `problems` stayed empty, every
    `_get(...)` returned `None`, controls (b)-(f) were skipped by their
    `is not None` guards, and the sub-check still printed
    `render_contract sub-check PASSED`, exit 0, with zero doc-derived
    assertions executed. Separately, gutting `_RENDER_RULE_LITERALS["R1"]`
    down to its harmless first sentence also left the sub-check PASSED — a
    one-line edit silently disabling the mechanism that makes ROADMAP
    success criteria 1 and 2 true. Control (h) now compares a LIVE
    `_RenderRegistrySnapshot` (`.live()` is the only producer reading the
    real module constants) against literals written inline inside
    `_render_registry_lock_problems`, never against the module constant
    each field mirrors; the CR-02 and WR-01 reproductions are both named
    cases in control (h2)'s table. Control (h2) is the ANTI-MASKING floor,
    copying HARN-01's shape (`scripts/check-act-limb.py`): every
    `_RENDER_REGISTRY_FIELDS` entry has at least one `dataclasses.replace`
    -derived negative case proving it load-bearing, the case table's field
    coverage is asserted against `_RENDER_REGISTRY_FIELDS` itself, and the
    `checked_fields` the positive call actually compared is asserted
    against that same set — a field silently skipped by
    `_render_registry_lock_problems` (the exact failure mode (h) had
    before this plan) is caught here rather than passing by omission. The
    `literals` field's two arms — a required-clause substring and a
    `sha256:` digest pin — are each BOUND TO A CASE by the required
    problem substring that case must see, not merely named in a case
    title (WR-04, `11-REVIEW-gap-closure.md`): the digest is a hash over
    the whole dict and therefore subsumes the clause arm, so while a case
    only had to yield some problem containing "literals", the clause arm
    could be deleted outright with both cases still green. Deleting
    either arm now fails the case bound to it, by name. DISCLOSED RESIDUAL: the lock proves the registries have not
    shrunk, been reordered, or lost a required literal clause against a
    PINNED expectation; it does not prove the pinned expectations are
    themselves the right ones — that question is answered by the fixture
    legs above and by plan 11-09's consumption floor, not here.

    Control (i) is POSITIVE — it goes RED if a rule is deleted from a
    shipped surface today. Control (j) is the COVERAGE FLOOR, Phase 10
    block (l)'s corrected shape: derived from the records
    `_read_render_surfaces()` actually returned, never a re-glob. Control
    (k) is the NEGATIVE leg for a missing rule, mutating an in-memory copy
    of the real bytes, never the file on disk (Phase 10 block (m)'s shape,
    `scripts/check-agent.py:334` `_assert_live_coverage`). Controls (n)
    and (o), added by plan 11-07, prove `_render_rule_report`'s two
    fail-closed branches — an unregistered surface and a required key
    with no literal — are load-bearing by mutating an in-memory copy and
    requiring the specific problem to fire.

    Control (m) checks the two doc-side QUAL-01 gate-description rows
    themselves, closing WR-04/IN-02/IN-03 (`11-REVIEW.md`) together: the
    two rows fused two independent mechanisms into one inaccurate sentence
    and omitted this item's third scanned surface, and the control that
    policed them was loose enough not to notice. Plan 11-10 rebuilt it to
    read through the same `_RenderSurfaceRead` discipline every other leg
    uses (`_read_qual01_doc_rows()` is the only producer;
    `_qual01_row_problem` cannot be handed a hand-built `(relpath, text)`
    pair — IN-02), to check only the physical line whose `lstrip()` starts
    with `| QUAL-01 |` rather than any line mentioning "QUAL-01" — IN-03,
    proven by a dedicated ANTI-MASKING arm that puts the token on a
    non-row line and requires the problem to still fire — and to require
    every `_QUAL01_DOC_ROW_TOKENS` entry independently, reporting one
    problem per missing token by name rather than a single all-or-nothing
    verdict. `_QUAL01_DOC_ROW_TOKENS` is itself a ninth locked
    `_RenderRegistrySnapshot` field, so dropping any required token
    from the tuple is caught by control (h2)'s anti-masking floor even if
    every doc row still carries it. Plan 13-05 (CR-01) added a third
    token pinning the corrected consumption-floor guarantee; plan 13-06
    (CR-02) added a fourth pinning the dispatch-reachability leg; plan
    13-08 (BL-01) added a fifth pinning the disclosed positional bound;
    plan 13-09 (BL-02) added a sixth pinning the GT-leading-hop refusal's
    remedy claim; plan 13-10 (BL-03) added a seventh pinning the
    strengthened expected-verdict consumption-floor claim; plan 13-12
    (CR-03) added an eighth pinning the chain-family coverage floor; plan
    13-14 (CR-01) added a ninth pinning the worked-example conformance
    leg. Plan 13-17 (WR-02, `13-VERIFICATION-round4.md`) added a tenth
    and an eleventh, pinning the three-helper call-site census (covering
    `_render_coverage_floor_problems`, `_render_example_conformance_problems`
    and `_render_entry_source_problems`, the last landed by plan 13-16 for
    R4-CR-02) and the entry-source lock, respectively. Plan 13-21 (round 5
    closure) added a twelfth and a thirteenth, pinning the GTHOP pair's
    positional coverage (`R-HEAD-GTHOP-LATE` pins the position the form
    check does not reach) and the fourth scanned surface
    (`reason-upward.md`), respectively. Plan 13-28 (round 6 closure) added
    a fourteenth through a seventeenth, pinning R10's over-rejection
    bound, the `R-HEAD-PERIOD-BAD` fixture that proves it, the
    tree-derived chain-form surface sweep, and the rendered-example claim
    floor, respectively. Plan 14-06 (D-12, the user's explicit decision
    to register this phase's mechanism rather than leave it unstated)
    added an eighteenth through a twenty-third, pinning the closure-ledger
    claim-inventory leg itself, D-03's structural-ledger-row narrowing,
    R11's section-intro-label bound and its `R-CLAIM-LABEL-BARE` fixture,
    D-09's `R-CLAIM-CAVEAT-MARKED` non-discharge teeth, and the
    `quality-ledger-v8.26` fixture D-04's live leg reads.
    A NEGATIVE-CASE COUNT FLOOR derives the expected 60 (2 doc rows x 30
    tokens) from the two registries rather than restating it, and a
    DOCSTRING COUNT LOCK (plan 13-17) asserts this very sentence's
    transcribed total — both factors, not only the product — against that
    same derivation, closing the drift channel: the count has now drifted
    stale in two consecutive plans (round 3's WR-02 on the registry-lock
    comment counts; round 4's WR-02 on this docstring sentence) because
    three surfaces restate one number and nothing compared them. Plan
    13-21 is the first count move since 13-17 built this floor and its
    docstring lock, exercised here rather than left theoretical; plan
    14-06 is the second.
    DISCLOSED LIMITATION: the lock checks this count sentence's
    transcription only, not the rest of this docstring's prose — the same
    bound control (m) states for the doc rows.

    Plan 11-09 (WR-07, `11-REVIEW.md`) rebuilt the contradiction leg,
    formerly a single control (l), into three explicitly-labelled arms
    after finding it tautological: it built `read.text + " " + phrase`
    and asserted the phrase was reported, which is `x in (y + x)` — true
    for every string, so it verified message formatting, not detection.
    Control (l1) DETECTION is the falsifiable replacement: it appends each
    of the real, `git show`-recovered pre-contract wordings in
    `_RENDER_PRE_CONTRACT_WORDINGS` to a real record and requires a
    contradiction problem, going RED if `_RENDER_CONTRADICTION_PHRASES` is
    narrowed past a wording that was actually shipped. Control (l2)
    MESSAGE FORM keeps the original per-phrase loop, relabelled as what it
    is — a check on the reported problem's shape, which controls (i) and
    (k) match on, not a detection test. Control (l3) is the
    negative-of-the-negative: appending R1's own correct literal must
    produce NO contradiction problem, closing the gap an
    always-reports-a-contradiction `_render_rule_report` would leave in
    (l1) alone.

    DISCLOSED LIMITATION: (l1)/(l2) together detect the ENUMERATED
    phrasings in `_RENDER_CONTRADICTION_PHRASES`, not arbitrary
    contradiction of R1 — the enumeration is now pinned against the real
    historical wordings recovered in `_RENDER_PRE_CONTRACT_WORDINGS`
    rather than merely asserted tautologically, but the residual is
    unchanged: contradiction of R1 in wording nobody has written yet is
    still undetected. That is a stated limitation, not a bug — three of
    the enumerated phrasings were live findings in this tree, not
    hypotheticals.

    Plan 11-11 (WR-08/IN-04, `11-REVIEW.md`) closed two remaining
    convention-level findings. `_read_render_surfaces` and
    `_read_qual01_doc_rows` previously caught `except OSError` only; a
    readable-but-invalid-UTF-8 file raised `UnicodeDecodeError` (a
    `ValueError` subclass) uncaught, killing `self_test()` with a
    traceback instead of the named problem both docstrings promised. Both
    readers now route through the module-level `_read_text_or_problem`,
    which catches `(OSError, ValueError)`; control (r) proves both
    branches fire, with the failure converted to a named `_fail` rather
    than an uncaught exception even if the widened catch is reverted.
    DISCLOSED RESIDUAL: `_extract_contract_example` (used by controls
    (a)-(g) above) keeps its own narrower `except OSError` — it is shared
    with the older D-18 red-carry extraction surface
    (`_CONTRACT_EXTRACTION_TABLE`), so widening it is out of this plan's
    scope; a non-UTF-8 `output-template.md` would still crash `self_test`
    via that path. Separately, `_RENDER_FIXTURE_SHAPE`'s three
    `R-CHAIN-*` entries previously declared the identical undiscriminating
    pair `("GT-1", "GT-6")`, so a mis-anchored extraction of any one chain
    fixture into another's slot passed the guard whose stated job was to
    catch exactly that. Each now carries its own discriminating third
    needle, and control (h)'s `fixture_shape` arm full-value-locks ALL
    EIGHT ids — the five non-chain ids were promoted off the key-set tier
    at WR-01 (`11-REVIEW-gap-closure.md`), which reproduced emptying their
    needle tuples with every key still present and the self-test still
    GREEN — with two (h2) cases that degrade a needle tuple rather than
    only dropping a key (one chain, one non-chain), so the arm has its own
    load-bearing negative case on both tiers it replaced.
    """
    ok = True

    def _fail(msg: str) -> None:
        nonlocal ok
        print(f"self-test FAIL: render_contract {msg}", file=sys.stderr)
        ok = False

    # (a) Extraction. A problem here means the fixture id below is absent
    #     from `fixtures`, so every later control that touches it is
    #     skipped, never run against an empty string.
    fixtures, problems = _render_contract_fixtures()
    for problem in problems:
        _fail(f"(a) extraction {problem}")

    # `requested_ids` backs control (p) below: every id `_get` is asked
    # for, regardless of whether the lookup finds it. Controls (b)-(f) are
    # all guarded by `is not None`, so a fixture id that is never requested
    # here would otherwise be a silent skip, not a reported problem.
    requested_ids: set[str] = set()

    def _get(fixture_id: str) -> str | None:
        requested_ids.add(fixture_id)
        return fixtures.get(fixture_id)

    conforming = _get("R-CHAIN-CONFORMING")
    wrapped = _get("R-CHAIN-WRAPPED")
    numbered = _get("R-CHAIN-NUMBERED")
    cite_inline = _get("R-CITE-INLINE")
    cite_ledger = _get("R-CITE-LEDGER")
    cite_none = _get("R-CITE-NONE")
    verdict_expiry = _get("R-VERDICT-EXPIRY")
    verdict_bad = _get("R-VERDICT-EXPIRY-BAD")
    head_prose_bad = _get("R-HEAD-PROSE-BAD")
    head_chainref = _get("R-HEAD-CHAINREF")
    head_allchain = _get("R-HEAD-ALLCHAIN")
    head_prose_mid = _get("R-HEAD-PROSE-MID")
    head_gthop_bad = _get("R-HEAD-GTHOP-BAD")
    head_gthop_ok = _get("R-HEAD-GTHOP-OK")
    head_gthop_late = _get("R-HEAD-GTHOP-LATE")
    head_period_bad = _get("R-HEAD-PERIOD-BAD")
    head_period_ok = _get("R-HEAD-PERIOD-OK")
    head_period_late = _get("R-HEAD-PERIOD-LATE")
    claim_label_bare = _get("R-CLAIM-LABEL-BARE")
    claim_label_inline = _get("R-CLAIM-LABEL-INLINE")
    claim_label_cited = _get("R-CLAIM-LABEL-CITED")
    claim_colon_mid = _get("R-CLAIM-COLON-MID")
    claim_colon_end = _get("R-CLAIM-COLON-END")
    claim_terse_drop = _get("R-CLAIM-TERSE-DROP")
    claim_terse_keep = _get("R-CLAIM-TERSE-KEEP")
    claim_caveat_marked = _get("R-CLAIM-CAVEAT-MARKED")
    claim_caveat_cited = _get("R-CLAIM-CAVEAT-CITED")

    # `scored_verdicts` backs the (p) CONSUMPTION FLOOR's fourth arm below:
    # for every id one of the four wrappers records, the boolean VERDICT
    # summary of the scorer it actually called — not merely that the id was
    # touched. Plan 13-10 (BL-03, `13-VERIFICATION.md`) replaced the prior
    # `scored_ids: set[str]` membership recorder with this verdict-sequence
    # dict because membership alone does not prove a scorer ran: both
    # `scored_ids.update({...})` with no scorer called, and a wrapper called
    # with its return value discarded, satisfied the old membership floor.
    # There is no separately writable `scored_ids` name any more — bypass
    # 1's write target no longer exists. Each wrapper records AFTER calling
    # its scorer, never before, so a wrapper that records first and raises
    # second cannot leave a verdict with no scorer behind it. A sequence,
    # not a single value, is stored because `R-CITE-NONE` is scored TWICE
    # by design (control (f)) and a last-write-wins dict would silently
    # lose the first (untraced) call.
    scored_verdicts: dict[str, list[bool]] = {}

    def _score_chain(fixture_id: str, text: str) -> bool:
        verdict = _chain_block_well_formed(text)
        scored_verdicts.setdefault(fixture_id, []).append(verdict)
        return verdict

    def _score_verdict(fixture_id: str, cell: str) -> bool:
        verdict = _verdict_conforms(cell)
        scored_verdicts.setdefault(fixture_id, []).append(verdict)
        return verdict

    def _score_traced(
        fixture_id: str,
        claim: str,
        chain_ids: list[str],
        chains: list[str],
        ledger_fragments: tuple[str, ...] | list[str] | None = None,
    ) -> bool:
        if ledger_fragments is None:
            verdict = _claim_is_traced(claim, chain_ids, chains)
        else:
            verdict = _claim_is_traced(claim, chain_ids, chains, ledger_fragments)
        scored_verdicts.setdefault(fixture_id, []).append(verdict)
        return verdict

    def _score_ledger(
        fixture_id: str, section6: str, chain_ids: list[str]
    ) -> list[str]:
        fragments = _closure_ledger_fragments(section6, chain_ids)
        scored_verdicts.setdefault(fixture_id, []).append(bool(fragments))
        return fragments

    # (b) Chain verdicts.
    if conforming is not None and not _score_chain(
        "R-CHAIN-CONFORMING", conforming
    ):
        _fail(
            "(b) R-CHAIN-CONFORMING (doc label 'Conforming — head, then "
            "one hop per line:') scored malformed, expected well-formed"
        )
    if wrapped is not None and _score_chain("R-CHAIN-WRAPPED", wrapped):
        _fail(
            "(b) R-CHAIN-WRAPPED (doc label 'Non-conforming — a hop "
            "broken across physical lines:') scored well-formed, "
            "expected malformed"
        )
    if numbered is not None and _score_chain("R-CHAIN-NUMBERED", numbered):
        _fail(
            "(b) R-CHAIN-NUMBERED (doc label 'Non-conforming — the same "
            "hops rendered as a numbered list:') scored well-formed, "
            "expected malformed"
        )

    # (b) Chain-head grammar verdicts (CHAINHEAD-05/CHAINHEAD-06). These
    #     two fixtures — R-HEAD-PROSE-BAD and R-HEAD-CHAINREF — are the
    #     SAME BYTES except for one token (`C2's threshold` vs
    #     `C2 (threshold)`, D-06), scored in both directions by the
    #     unmodified `_chain_block_well_formed`: a detector widened to
    #     accept the possessive form would fail this pair rather than pass
    #     it, which is why widening the detector is the wrong fix (the
    #     widening treadmill 999.3 Case A warns about) — the fix is the
    #     stated contract (R7/R8), not the code. R-HEAD-ALLCHAIN covers the
    #     all-`Cn` shape GAP-6 widened `_CHAIN_REF_TOKEN` for; without it a
    #     future narrowing of that token breaks this shape with every
    #     other gate green.
    if head_prose_bad is not None and _score_chain(
        "R-HEAD-PROSE-BAD", head_prose_bad
    ):
        _fail(
            "(b) R-HEAD-PROSE-BAD (doc label 'Non-conforming — an input "
            "carrying unparenthesized prose:') scored well-formed, "
            "expected malformed"
        )
    if head_chainref is not None and not _score_chain(
        "R-HEAD-CHAINREF", head_chainref
    ):
        _fail(
            "(b) R-HEAD-CHAINREF (doc label 'Conforming — the same head "
            "with the upstream chain as an input:') scored malformed, "
            "expected well-formed"
        )
    if head_allchain is not None and not _score_chain(
        "R-HEAD-ALLCHAIN", head_allchain
    ):
        _fail(
            "(b) R-HEAD-ALLCHAIN (doc label 'Conforming — a chain "
            "consuming only upstream conclusions:') scored malformed, "
            "expected well-formed"
        )

    # (b) R-HEAD-PROSE-MID (plan 13-08, BL-01): this fixture and
    #     R-HEAD-PROSE-BAD are the SAME violation in two head positions —
    #     trailing and middle — scored in OPPOSITE directions by the
    #     unmodified `_chain_block_well_formed`: with a well-formed input
    #     still to its right the check matches from `GT-12?` onward and
    #     never reaches `C2's threshold`, so this fixture is expected
    #     WELL-FORMED even though R7 forbids the same input everywhere.
    #     This pins the measured bound R7 now discloses, not an
    #     endorsement of the head — so a future anchoring of
    #     `_CHAIN_FORM_LINE_RE` fails this control rather than passing
    #     silently, which is the point.
    if head_prose_mid is not None and not _score_chain(
        "R-HEAD-PROSE-MID", head_prose_mid
    ):
        _fail(
            "(b) R-HEAD-PROSE-MID (doc label 'Non-conforming, and undetected by the form check "
            "— the same prose input in a non-final position:') scored "
            "malformed, expected well-formed (measured bound)"
        )

    # (b) R-HEAD-GTHOP-BAD / R-HEAD-GTHOP-OK (plan 13-09, BL-02): the same
    #     two hops differing only in whether the hop leads with `GT-4`,
    #     scored in opposite directions by the unmodified detector, so they
    #     pin BOTH halves of R9 — the refusal and the rewrite it prescribes.
    #     A relaxation of `_ARROW_LED_GT_RE` fails the first; a narrowing
    #     that also rejected the rewrite fails the second.
    if head_gthop_bad is not None and _score_chain(
        "R-HEAD-GTHOP-BAD", head_gthop_bad
    ):
        _fail(
            "(b) R-HEAD-GTHOP-BAD (doc label 'Non-conforming — a hop "
            "beginning with a GT-N identifier:') scored well-formed, "
            "expected malformed"
        )
    if head_gthop_ok is not None and not _score_chain(
        "R-HEAD-GTHOP-OK", head_gthop_ok
    ):
        _fail(
            "(b) R-HEAD-GTHOP-OK (doc label 'Conforming — the same hop "
            "with the identifier moved off the front:') scored malformed, "
            "expected well-formed"
        )

    # (b) R-HEAD-GTHOP-LATE (plan 13-19, CR-02 fixture half): the same
    #     offending hop as R-HEAD-GTHOP-BAD, moved from first position to
    #     last with two ordinary hops ahead of it, scored WELL-FORMED by
    #     the unmodified detector — with two hops already matched before
    #     it, the check has satisfied its arrow requirement and never
    #     evaluates the leading identifier. This pins the measured bound
    #     R9 now discloses — the check detects the violation only while
    #     fewer than two hops precede it — not an endorsement of the hop,
    #     so a future anchoring of `_CHAIN_FORM_LINE_RE` fails this
    #     control rather than passing silently, which is the point.
    if head_gthop_late is not None and not _score_chain(
        "R-HEAD-GTHOP-LATE", head_gthop_late
    ):
        _fail(
            "(b) R-HEAD-GTHOP-LATE (doc label 'Non-conforming, and "
            "undetected by the form check — the GT-led hop in a later "
            "position:') scored malformed, expected well-formed "
            "(measured bound)"
        )

    # (b) R-HEAD-PERIOD-BAD / R-HEAD-PERIOD-OK / R-HEAD-PERIOD-LATE
    #     (plan 13-26, CR-05 fixture half): pin R10's disclosed
    #     over-rejection bound in all three measured directions. BAD and
    #     OK are a minimal pair differing by exactly one character (the
    #     first hop's terminal period) and are scored in opposite
    #     directions by the unmodified detector — the check ends the
    #     chain at the sentence-closing first hop before its two-arrow
    #     requirement is satisfied, so BAD is malformed even though it
    #     violates none of R1-R9, and removing the period restores the
    #     match. LATE moves the identical period past the point where the
    #     check's two-arrow requirement is already satisfied — the check
    #     never re-tests a closed sentence for a line that does not
    #     follow it — and is scored WELL-FORMED, pinning the bound's
    #     undetected half.
    if head_period_bad is not None and _score_chain(
        "R-HEAD-PERIOD-BAD", head_period_bad
    ):
        _fail(
            "(b) R-HEAD-PERIOD-BAD (doc label 'Non-conforming — the "
            "first hop closing its own sentence:') scored well-formed, "
            "expected malformed"
        )
    if head_period_ok is not None and not _score_chain(
        "R-HEAD-PERIOD-OK", head_period_ok
    ):
        _fail(
            "(b) R-HEAD-PERIOD-OK (doc label 'Conforming — the same "
            "chain with the first hop's terminal period removed:') "
            "scored malformed, expected well-formed"
        )
    if head_period_late is not None and not _score_chain(
        "R-HEAD-PERIOD-LATE", head_period_late
    ):
        _fail(
            "(b) R-HEAD-PERIOD-LATE (doc label 'Non-conforming, and "
            "undetected by the form check — the same period moved to a "
            "later hop:') scored malformed, expected well-formed "
            "(measured bound)"
        )

    # (c) Minimality of the wrap counter-example: dropping the single line
    #     that is neither the first line nor begins (after .strip()) with
    #     `→` must reproduce R-CHAIN-CONFORMING byte for byte. This proves
    #     the doc's Case A counter-example differs from its conforming
    #     twin by exactly the wrap and nothing else.
    if wrapped is not None and conforming is not None:
        wrapped_lines = wrapped.split("\n")
        kept = [
            line
            for i, line in enumerate(wrapped_lines)
            if i == 0 or line.strip().startswith("→")
        ]
        dropped = [
            line
            for i, line in enumerate(wrapped_lines)
            if not (i == 0 or line.strip().startswith("→"))
        ]
        rebuilt = "\n".join(kept)
        if len(dropped) != 1:
            _fail(
                f"(c) R-CHAIN-WRAPPED does not differ from its conforming "
                f"twin by exactly one non-arrow-led continuation line: "
                f"{len(dropped)} such lines found"
            )
        elif rebuilt != conforming:
            _fail(
                "(c) dropping R-CHAIN-WRAPPED's single non-arrow-led "
                "continuation line did not reproduce R-CHAIN-CONFORMING "
                "byte for byte"
            )

    # (d) Same-hops property of the numbered counter-example: every line
    #     of R-CHAIN-CONFORMING, with any leading `→ ` removed, must
    #     appear as a substring of R-CHAIN-NUMBERED — proving the
    #     numbered example renders THE SAME hops, not a different chain
    #     that happens to fail.
    if conforming is not None and numbered is not None:
        for line in conforming.split("\n"):
            bare = line[2:] if line.startswith("→ ") else line
            if bare not in numbered:
                _fail(
                    f"(d) R-CHAIN-CONFORMING hop {bare!r} does not appear "
                    f"in R-CHAIN-NUMBERED — the numbered example may "
                    f"render different hops, not just a different form"
                )

    # (e) Verdict cells. CONTRACT-04 needed no schema change: this pair is
    #     the evidence — `_VERDICT_VOCAB` and `_VERDICT_FORM_RE` are
    #     untouched.
    if verdict_expiry is not None and not _score_verdict(
        "R-VERDICT-EXPIRY", verdict_expiry
    ):
        _fail(
            "(e) R-VERDICT-EXPIRY (doc label 'Conforming — a current "
            "constraint recording its expiry:') scored non-conforming, "
            "expected conforming"
        )
    if verdict_bad is not None and _score_verdict(
        "R-VERDICT-EXPIRY-BAD", verdict_bad
    ):
        _fail(
            "(e) R-VERDICT-EXPIRY-BAD (doc label 'Non-conforming — the "
            "expiry hoisted into the token slot:') scored conforming, "
            "expected non-conforming"
        )

    # (f) Citation credit. Both accepted forms — inline and
    #     closure-ledger — are proven, and the closure-ledger leg proves
    #     the SAME otherwise-untraced claim (R-CITE-NONE) flips from
    #     untraced to traced purely because the ledger row is present.
    if conforming is not None and cite_inline is not None:
        if not _score_traced("R-CITE-INLINE", cite_inline, ["C1"], [conforming]):
            _fail(
                "(f) R-CITE-INLINE (doc label 'Conforming — inline chain "
                "citation:') scored untraced, expected traced"
            )
    if conforming is not None and cite_none is not None:
        if _score_traced("R-CITE-NONE", cite_none, ["C1"], [conforming]):
            _fail(
                "(f) R-CITE-NONE (doc label 'Non-conforming — a claim "
                "naming no chain and quoted by no ledger row:') scored "
                "traced with no ledger fragments, expected untraced"
            )
    if cite_ledger is not None:
        ledger_fragments = _score_ledger("R-CITE-LEDGER", cite_ledger, ["C1"])
        if not ledger_fragments:
            _fail(
                "(f) R-CITE-LEDGER (doc label 'Conforming — closure-ledger "
                "row:') yielded zero closure-ledger fragments"
            )
        elif conforming is not None and cite_none is not None:
            if not _score_traced(
                "R-CITE-NONE", cite_none, ["C1"], [conforming], ledger_fragments
            ):
                _fail(
                    "(f) R-CITE-NONE with R-CITE-LEDGER's fragments still "
                    "scored untraced — the ledger row does not discharge "
                    "the claim it quotes"
                )

    # (g) NON-VACUITY: the module's own long-standing base cases still
    #     hold from outside this item. A control that scored everything
    #     `True`, or everything `False`, would pass (b) and (e) only by
    #     accident. These two calls stay RAW — string literals with no
    #     fixture id — deliberately: routing them through a `_score_*`
    #     wrapper would inject a non-fixture key into `scored_verdicts`. A
    #     future reader sweeping "all raw scorer calls" onto the wrappers
    #     would break the (p) floor below.
    if _chain_block_well_formed("GT-1 (a) + GT-2 (b) -> lone hop"):
        _fail(
            "(g) NON-VACUITY: the one-hop base case "
            "'GT-1 (a) + GT-2 (b) -> lone hop' wrongly scored well-formed"
        )
    if _verdict_conforms("Accept"):
        _fail(
            "(g) NON-VACUITY: the bare-token base case 'Accept' (no "
            "em-dash, no justification) wrongly scored conforming"
        )

    # (aa) CLAIM-BOUND VERDICTS. Plan 14-04 (D-07, D-09, LEDGER-04): R11's
    #      three disclosed bounds and R12's caveat-marker rule, scored by
    #      the unmodified `_conclusion_claims` and `_claim_is_traced`
    #      through `_render_claim_bound_problems` — a parameterised helper
    #      copying `_render_fixture_accounting_problems`'s purity
    #      discipline, so a call site wiring the wrong table or the wrong
    #      scorer becomes unexpressible rather than merely untested.
    #      `R-CLAIM-TERSE-DROP`/`R-CLAIM-TERSE-KEEP` are each scored TWICE
    #      by the helper — once as extracted, once with the terminal
    #      period toggled in memory — proving the axis Task 1's needle-
    #      uniqueness discipline forced the pair to give up at the text
    #      level (a true minimal pair would make one block's text a
    #      literal prefix of the other's, which no substring needle can
    #      discriminate) is punctuation, not wording. `R-CLAIM-CAVEAT-
    #      MARKED`/`R-CLAIM-CAVEAT-CITED` are scored by `_claim_is_traced`,
    #      proving the flagged-assumption marker really does not discharge
    #      the claim — a future edit teaching the tracer the marker fails
    #      this the moment it starts recognising it.
    render_claim_doc_labels = {
        "R-CLAIM-LABEL-BARE": "Not a claim — a bold lead-in alone on its line, carrying no citation:",
        "R-CLAIM-LABEL-INLINE": "A claim — the same lead-in carrying its assertion on the same line:",
        "R-CLAIM-LABEL-CITED": "A claim — the lead-in alone on its line, but carrying its own citation:",
        "R-CLAIM-COLON-MID": "Not matched at all — a bold span whose colon sits inside it:",
        "R-CLAIM-COLON-END": "A claim — the same statement with the colon closing the bold span:",
        "R-CLAIM-TERSE-DROP": "Not a claim — a short list item with no sentence-ending punctuation:",
        "R-CLAIM-TERSE-KEEP": "A claim — a short list item closing its own sentence:",
        "R-CLAIM-CAVEAT-MARKED": "Conformant but still untraced — a caveat carrying the flagged-assumption marker:",
        "R-CLAIM-CAVEAT-CITED": "Conformant and traced — the same caveat citing the chain it qualifies:",
    }
    render_claim_expected: dict[str, list[bool]] = {
        "R-CLAIM-LABEL-BARE": [False],
        "R-CLAIM-LABEL-INLINE": [True],
        "R-CLAIM-LABEL-CITED": [True],
        "R-CLAIM-COLON-MID": [False],
        "R-CLAIM-COLON-END": [True],
        "R-CLAIM-TERSE-DROP": [False, True],
        "R-CLAIM-TERSE-KEEP": [True, False],
        "R-CLAIM-CAVEAT-MARKED": [False],
        "R-CLAIM-CAVEAT-CITED": [True],
    }
    render_claim_fixtures = {
        fid: text
        for fid, text in (
            ("R-CLAIM-LABEL-BARE", claim_label_bare),
            ("R-CLAIM-LABEL-INLINE", claim_label_inline),
            ("R-CLAIM-LABEL-CITED", claim_label_cited),
            ("R-CLAIM-COLON-MID", claim_colon_mid),
            ("R-CLAIM-COLON-END", claim_colon_end),
            ("R-CLAIM-TERSE-DROP", claim_terse_drop),
            ("R-CLAIM-TERSE-KEEP", claim_terse_keep),
            ("R-CLAIM-CAVEAT-MARKED", claim_caveat_marked),
            ("R-CLAIM-CAVEAT-CITED", claim_caveat_cited),
        )
        if text is not None
    }
    render_claim_problems, render_claim_verdicts = _render_claim_bound_problems(
        render_claim_expected,
        render_claim_fixtures,
        _conclusion_claims,
        _claim_is_traced,
    )
    for render_claim_fid, render_claim_vlist in render_claim_verdicts.items():
        scored_verdicts.setdefault(render_claim_fid, []).extend(render_claim_vlist)
    for render_claim_problem in render_claim_problems:
        render_claim_problem_fid = next(
            (
                fid
                for fid in render_claim_expected
                if _render_fixture_id_token(fid) in render_claim_problem
            ),
            None,
        )
        render_claim_label = render_claim_doc_labels.get(render_claim_problem_fid, "?")
        _fail(f"(aa) {render_claim_problem} (doc label {render_claim_label!r})")

    # (p) CONSUMPTION FLOOR. Plan 11-09, gap 2's second half
    #     (`11-VERIFICATION.md`): controls (b)-(f) above are all guarded by
    #     `is not None`, so a fixture id absent from `fixtures` is silently
    #     SKIPPED rather than reported — this is exactly the path the
    #     verifier's CR-02 reproduction relied on once
    #     `_RENDER_CONTRACT_EXTRACTION_TABLE` was emptied: `problems` stayed
    #     empty, every `_get(...)` returned `None`, and the sub-check still
    #     printed PASSED. The locked twenty-seven-id set below is written INLINE,
    #     matching plan 11-08's (h) lock literal, never read off a module
    #     constant, so this floor cannot be made tautologically green by
    #     comparing a constant against itself. This control proves every
    #     locked fixture was requested and either scored or reported; it
    #     does NOT prove the verdict each control asserted is the right
    #     verdict — that is controls (b)-(f)'s job, and control (g)'s
    #     non-vacuity pair is what keeps those honest.
    #
    #     Plan 13-05 (CR-01, `13-VERIFICATION.md`) replaced this arm's
    #     extraction test — absence from the extracted-fixtures mapping —
    #     with membership in `scored_ids`, written only by the
    #     `_score_chain` / `_score_verdict` / `_score_traced` /
    #     `_score_ledger` wrappers above: deleting the
    #     three (b) chain-head verdict-assertion blocks used to leave this
    #     floor green because those fixtures still extracted cleanly even
    #     though no control ever scored them. The residual bypass — a
    #     control calling a raw detector instead of a wrapper — is
    #     fail-CLOSED: the fixture never enters the recorder, so this floor
    #     goes red.
    #
    #     Plan 13-10 (BL-03, `13-VERIFICATION.md`) found the ORIGINAL
    #     in-code claim here false: it asserted that control (t) below,
    #     by locking the wrapper/recorder site count, fully closed the
    #     fail-OPEN shape — a control marking a fixture scored without
    #     scoring it. The verification independently
    #     reproduced two bypasses that both satisfied or evaded that count
    #     while leaving this sub-check green: (1) `scored_ids.update({...})`
    #     writing the three chain-head ids directly, with no scorer ever
    #     called (`.update(` is not `.add(`, so the old count was unmoved);
    #     and (2) calling a `_score_*` wrapper genuinely (satisfying the old
    #     count exactly) but discarding its boolean return, so no verdict
    #     assertion existed anywhere. Control (t) alone never closed that
    #     shape — it counted source text, not behaviour. The actual fix is
    #     below, in arms 4a and 4b: arm 4b (`_render_verdict_floor_problems`)
    #     compares every locked id's RECORDED VERDICT sequence in
    #     `scored_verdicts` against an inline expected-verdict table, so a
    #     fabricated or omitted verdict is caught by value, not by count;
    #     arm 4a (`_render_chain_verdict_floor_problems`) additionally
    #     re-scores the thirteen chain-family fixtures independently, by
    #     calling the unmodified `_chain_block_well_formed` on `fixtures`
    #     itself, reading no recorder at all — so no forgery of the
    #     recorder, of any shape, can discharge those thirteen. Control (v)
    #     below proves each of the four wrappers actually delegates to its
    #     scorer rather than fabricating a verdict. Control (t) is retained
    #     as a diff-review
    #     backstop over the recorder's write idioms; it is explicitly NOT
    #     the thing that closes the fail-OPEN shape.
    render_locked_fixture_ids = {
        "R-CHAIN-CONFORMING", "R-CHAIN-NUMBERED", "R-CHAIN-WRAPPED",
        "R-CITE-INLINE", "R-CITE-LEDGER", "R-CITE-NONE",
        "R-VERDICT-EXPIRY", "R-VERDICT-EXPIRY-BAD",
        "R-HEAD-ALLCHAIN", "R-HEAD-CHAINREF", "R-HEAD-PROSE-BAD",
        "R-HEAD-PROSE-MID", "R-HEAD-GTHOP-BAD", "R-HEAD-GTHOP-OK",
        "R-HEAD-GTHOP-LATE",
        "R-HEAD-PERIOD-BAD", "R-HEAD-PERIOD-OK", "R-HEAD-PERIOD-LATE",
        "R-CLAIM-LABEL-BARE", "R-CLAIM-LABEL-INLINE", "R-CLAIM-LABEL-CITED",
        "R-CLAIM-COLON-MID", "R-CLAIM-COLON-END",
        "R-CLAIM-TERSE-DROP", "R-CLAIM-TERSE-KEEP",
        "R-CLAIM-CAVEAT-MARKED", "R-CLAIM-CAVEAT-CITED",
    }
    if requested_ids != render_locked_fixture_ids:
        _fail(
            f"(p) CONSUMPTION FLOOR: requested_ids {sorted(requested_ids)!r} "
            f"!= locked fixture ids {sorted(render_locked_fixture_ids)!r} — "
            f"a scoring control stopped asking for a fixture"
        )
    if not problems and set(fixtures) != render_locked_fixture_ids:
        _fail(
            f"(p) CONSUMPTION FLOOR: problems is empty but fixtures "
            f"{sorted(fixtures)!r} != locked fixture ids "
            f"{sorted(render_locked_fixture_ids)!r} — an emptied "
            f"extraction table leaves both problems and fixtures empty, "
            f"which is precisely the condition nothing used to notice"
        )
    # The accounting arm matches on `_render_fixture_id_token` — the
    # delimiter-scoped `] <id>: ` form the emitter itself composes — not on
    # bare containment (WR-07, `11-REVIEW-gap-closure.md`).
    # `"R-VERDICT-EXPIRY"` is a proper prefix of `"R-VERDICT-EXPIRY-BAD"`,
    # so under `fid in p` a problem naming only the BAD fixture accounted
    # for the good one too: drop the good row while the BAD one reports a
    # problem and this arm called the missing fixture accounted for, with
    # arm 2 above skipped by its own `if not problems` guard. As of plan
    # 13-05 this arm floors on SCORING, not extraction — `_render_
    # unscored_fixture_ids` returns a locked id only when it is absent from
    # `scored_verdicts` (derived here as `set(scored_verdicts)`, never a
    # separately writable name) AND not accounted for by a reported
    # problem.
    render_unscored_fixture_ids = _render_unscored_fixture_ids(
        render_locked_fixture_ids, set(scored_verdicts), problems
    )
    if render_unscored_fixture_ids:
        _fail(
            f"(p) CONSUMPTION FLOOR: fixture id(s) "
            f"{render_unscored_fixture_ids!r} are never scored by any "
            f"control and not named in a reported problem"
        )

    # (p) CHAIN VERDICT FLOOR — arm 4a. Plan 13-10 (BL-03,
    #     `13-VERIFICATION.md`): this arm reads `fixtures` and calls the
    #     frozen `_chain_block_well_formed` directly on the thirteen
    #     chain-family fixtures' extracted text — it consults NO recorder
    #     of any shape, so no forgery of `scored_verdicts` (a `.update(`,
    #     a bare subscript write, a wrapper that fabricates its return)
    #     can discharge these thirteen ids. This is the arm that makes
    #     "the mutation removes the entire behavioural content while the
    #     gate stays green" false rather than merely harder — deleting the
    #     (b) verdict-assertion blocks above no longer matters because this
    #     arm re-derives the verdict independently every run.
    render_chain_verdict_expected: dict[str, bool] = {
        "R-CHAIN-CONFORMING": True,
        "R-CHAIN-WRAPPED": False,
        "R-CHAIN-NUMBERED": False,
        "R-HEAD-PROSE-BAD": False,
        "R-HEAD-CHAINREF": True,
        "R-HEAD-ALLCHAIN": True,
        "R-HEAD-PROSE-MID": True,
        "R-HEAD-GTHOP-BAD": False,
        "R-HEAD-GTHOP-OK": True,
        "R-HEAD-GTHOP-LATE": True,
        "R-HEAD-PERIOD-BAD": False,
        "R-HEAD-PERIOD-OK": True,
        "R-HEAD-PERIOD-LATE": True,
    }
    for render_chain_problem in _render_chain_verdict_floor_problems(
        render_chain_verdict_expected, fixtures, _chain_block_well_formed, problems
    ):
        _fail(f"(p) CHAIN VERDICT FLOOR: {render_chain_problem}")

    # (p) EXPECTED-VERDICT FLOOR — arm 4b. Plan 13-10 (BL-03): covers all
    #     TWENTY-SEVEN locked ids, including the five `R-CITE-*` /
    #     `R-VERDICT-*` fixtures whose scorers take extra arguments (chain
    #     ids, chain text, ledger fragments) that arm 4a's single-argument
    #     shape cannot restate without duplicating control (f)'s wiring —
    #     for those five the guarantee is the recorded verdict plus control
    #     (v)'s delegation probe plus control (t)'s source-level lock, not
    #     an independent re-score (A-02, disclosed in both `| QUAL-01 |`
    #     doc rows). This arm also pins `R-CITE-NONE`'s two-call flip
    #     (`[False, True]`): scored once without ledger fragments
    #     (untraced) and once with them (traced) — a last-write-wins
    #     single-value recorder would lose the first call and silently
    #     record only `True`. Plan 14-04 (LEDGER-04) adds the nine
    #     `R-CLAIM-*` ids, scored by `_render_claim_bound_problems` (a
    #     separate re-score, not a recorder-only guarantee like the five
    #     `R-CITE-*`/`R-VERDICT-*` fixtures above).
    render_verdict_expected: dict[str, list[bool]] = {
        "R-CHAIN-CONFORMING": [True],
        "R-CHAIN-WRAPPED": [False],
        "R-CHAIN-NUMBERED": [False],
        "R-HEAD-PROSE-BAD": [False],
        "R-HEAD-CHAINREF": [True],
        "R-HEAD-ALLCHAIN": [True],
        "R-HEAD-PROSE-MID": [True],
        "R-HEAD-GTHOP-BAD": [False],
        "R-HEAD-GTHOP-OK": [True],
        "R-HEAD-GTHOP-LATE": [True],
        "R-HEAD-PERIOD-BAD": [False],
        "R-HEAD-PERIOD-OK": [True],
        "R-HEAD-PERIOD-LATE": [True],
        "R-VERDICT-EXPIRY": [True],
        "R-VERDICT-EXPIRY-BAD": [False],
        "R-CITE-INLINE": [True],
        "R-CITE-LEDGER": [True],
        "R-CITE-NONE": [False, True],
        "R-CLAIM-LABEL-BARE": [False],
        "R-CLAIM-LABEL-INLINE": [True],
        "R-CLAIM-LABEL-CITED": [True],
        "R-CLAIM-COLON-MID": [False],
        "R-CLAIM-COLON-END": [True],
        "R-CLAIM-TERSE-DROP": [False, True],
        "R-CLAIM-TERSE-KEEP": [True, False],
        "R-CLAIM-CAVEAT-MARKED": [False],
        "R-CLAIM-CAVEAT-CITED": [True],
    }
    for render_verdict_problem in _render_verdict_floor_problems(
        render_verdict_expected, scored_verdicts, problems
    ):
        _fail(f"(p) EXPECTED-VERDICT FLOOR: {render_verdict_problem}")

    # Coverage of BOTH expected-verdict tables above, plus control (u)'s
    # dispatch-reachability symbol set below, is floored by EQUALITY in
    # control (x) further down this function — not here, and not by a
    # union. A prior version of this comment described a union check
    # whose purpose was "a fifteenth fixture added later — covered by
    # neither table — would be silently unfloored by both arm 4a and arm
    # 4b." That case is subsumed by arm 4b's equality floor against
    # `render_locked_fixture_ids` in control (x). The case the union
    # could not see — arm 4a narrowing while arm 4b stays whole, so the
    # union (arm 4b alone) stays satisfied regardless of what arm 4a
    # contains — is CR-03, the gap control (x) exists to close
    # (`13-REVIEW-plans-08-11.md`).

    # (p) ISOLATION, prefix discrimination. Drives the accounting
    # predicate directly with a problem composed by the EMITTER's own
    # `_render_fixture_problem`, never a hand-typed string, over the one
    # id pair in the locked set where one id is a proper prefix of the
    # other. Both arms are load-bearing: the first fails if the matcher
    # reverts to containment, the second if the token form drifts apart
    # from the emitter so that NO id is ever accounted for (which would
    # make the arm above fail-closed but permanently unfalsifiable here).
    render_prefix_probe = [
        _render_fixture_problem(
            "mode 2: shape mismatch",
            "R-VERDICT-EXPIRY-BAD",
            "extracted text is missing required substring(s) ['expires at']",
        )
    ]
    if _render_fixture_id_accounted("R-VERDICT-EXPIRY", render_prefix_probe):
        _fail(
            f"(p) ISOLATION prefix discrimination: a problem naming only "
            f"'R-VERDICT-EXPIRY-BAD' wrongly accounted for the proper "
            f"prefix 'R-VERDICT-EXPIRY' — {render_prefix_probe!r}"
        )
    if not _render_fixture_id_accounted(
        "R-VERDICT-EXPIRY-BAD", render_prefix_probe
    ):
        _fail(
            f"(p) ISOLATION prefix discrimination: a problem naming "
            f"'R-VERDICT-EXPIRY-BAD' did not account for it — the "
            f"matcher's token has drifted from the emitter's form, so the "
            f"accounting arm can never report an accounted fixture: "
            f"{render_prefix_probe!r}"
        )

    # (s) ISOLATION, scoring floor. Plan 13-05: drives
    # `_render_unscored_fixture_ids` directly with synthetic literals —
    # never `render_locked_fixture_ids`, never `scored_verdicts`, never
    # `fixtures` — so the new floor's own predicate is proven falsifiable
    # in-process, mirroring (p) ISOLATION's discipline one arm up.
    render_s_clean = _render_unscored_fixture_ids({"A", "B"}, {"A", "B"}, [])
    if render_s_clean != []:
        _fail(
            f"(s) ISOLATION CLEAN: a fully scored locked set wrongly "
            f"reported a problem: {render_s_clean!r}"
        )

    render_s_unscored = _render_unscored_fixture_ids({"A", "B"}, {"A"}, [])
    if render_s_unscored != ["B"]:
        _fail(
            f"(s) ISOLATION UNSCORED: expected ['B'], got "
            f"{render_s_unscored!r} — this is the arm that would have "
            f"caught CR-01"
        )

    render_s_accounted_problems = [
        _render_fixture_problem(
            "mode 2: shape mismatch",
            "B",
            "extracted text is missing required substring(s) ['x']",
        )
    ]
    render_s_accounted = _render_unscored_fixture_ids(
        {"A", "B"}, {"A"}, render_s_accounted_problems
    )
    if render_s_accounted != []:
        _fail(
            f"(s) ISOLATION ACCOUNTED: an unscored fixture accounted for "
            f"by a reported problem wrongly stayed unaccounted: "
            f"{render_s_accounted!r} — without this arm the helper could "
            f"fail-closed on every unextractable fixture and nothing "
            f"would notice"
        )

    render_s_antimask_problems = [
        _render_fixture_problem(
            "mode 2: shape mismatch",
            "R-VERDICT-EXPIRY-BAD",
            "extracted text is missing required substring(s) ['expires at']",
        )
    ]
    render_s_antimask = _render_unscored_fixture_ids(
        {"R-VERDICT-EXPIRY", "R-VERDICT-EXPIRY-BAD"},
        set(),
        render_s_antimask_problems,
    )
    if render_s_antimask != ["R-VERDICT-EXPIRY"]:
        _fail(
            f"(s) ISOLATION ANTI-MASKING: expected only "
            f"['R-VERDICT-EXPIRY'] unscored, got {render_s_antimask!r} — "
            f"a helper reverted to bare `in` containment would let a "
            f"problem naming only the BAD proper-prefix fixture wrongly "
            f"discharge the good one too"
        )

    # (t) SCORING RECORDER LOCK. Plan 13-05 added this as a source-level
    # backstop over the recorder's write idioms. Plan 13-10 (BL-03,
    # `13-VERIFICATION.md`) REWROTE it: the ORIGINAL version here counted
    # `scored_ids.add(` / `def _score_` sites and its own comment falsely
    # claimed this control, by itself, fully closed the fail-OPEN shape —
    # a control marking a fixture scored without actually scoring it. It
    # did not: the verification independently reproduced two bypasses that
    # both left the old count satisfied or unmoved while the fail-OPEN
    # shape stayed wide open — (1) `scored_ids.update({...})` writing ids
    # directly with no scorer ever called (`.update(` is not `.add(`, so
    # the old count was unmoved); and (2) a `_score_*` wrapper genuinely
    # called (satisfying the old count exactly) but its boolean return
    # discarded, so no verdict assertion existed anywhere. The ACTUAL
    # close is arm 4a (`_render_chain_verdict_floor_problems`, an
    # independent re-score of the chain family from `fixtures`, reading no
    # recorder) plus arm 4b (`_render_verdict_floor_problems`, a recorded-
    # verdict comparison against an inline expectation) above, plus
    # control (v) below control (u) (proves each wrapper's return equals
    # its raw scorer's return and that the recorder holds that same
    # value). Control (t) is explicitly NOT what closes the fail-OPEN
    # shape; it is retained as a diff-review backstop, because for the
    # five non-chain-family fixtures (which have no independent
    # re-derivation arm — see plan 13-10's A-02) a hand-written recorder
    # entry with correct values would satisfy arm 4b, and this control
    # plus control (v) are the only things standing against that narrower
    # residual risk.
    #
    # Reads `inspect.getsource(_selftest_render_contract)` and asserts,
    # over that source TEXT — never behaviour: exactly five sites where the
    # recorder is mutated via its dict-of-lists append idiom (the four
    # `_score_*` wrappers' own `.setdefault(...).append(...)` calls, plus
    # plan 14-04's own control (aa) merging `_render_claim_bound_problems`'s
    # returned verdicts in via `.setdefault(...).extend(...)` — a fifth,
    # deliberately different call shape, so this census cannot be satisfied
    # by four wrapper-shaped calls alone if the merge step were ever
    # deleted), and exactly four `_score_*` wrapper definitions; exactly six call sites for the
    # recorded-verdict floor helper and exactly six call sites for the
    # independent chain-rescoring helper (one real floor-arm call each,
    # plus control (w)'s isolation-driving calls — five for the chain
    # helper as of plan 13-12's IN-03 anti-masking arm, matching the
    # verdict helper's own five — so deleting either floor arm's real
    # call, or any of control (w)'s isolation calls, moves the count and
    # fails here by name); and ZERO occurrences of the two bypasses' forgery
    # idioms — a bare dict `.update(` call on the recorder, and a
    # bare-subscript assignment into it (the recorder name immediately
    # followed by `[`, with `] = ` present on the SAME source line — this
    # is a textual heuristic over source lines, not a parse, and is stated
    # as such).
    #
    # R4-CR-01 (`13-VERIFICATION-round4.md`): the two floors plans 13-12
    # and 13-14 built specifically to make criterion 3's guarantee
    # forgery-proof — the coverage-floor-registry helper (control (x)'s
    # THE FLOOR ITSELF) and the worked-example-conformance helper (leg
    # 5's THE LEG ITSELF) — were never registered here, so each floor's
    # WHOLE enforcement rested on one real, source-text-uncounted call;
    # deleting it restored the exact defect the floor exists to catch
    # with the battery green. Three more counters below close that:
    #
    #   - the coverage-floor-registry helper: 7 call sites (1 real — THE
    #     FLOOR ITSELF — plus the x1-x4 isolation arms, 4, plus leg 5's
    #     own reuse of the same helper for its NON-VACUITY floor, 1, plus
    #     plan 13-24's chain-form surface sweep's own reuse for its
    #     EQUALITY floor, 1);
    #   - the worked-example-conformance helper: 6 call sites (1 real —
    #     THE LEG ITSELF — plus the z5-z9 isolation arms, 5);
    #   - the entry-source helper (this plan's own Task 1 fix): 5 call
    #     sites (1 real — the ENTRY-SOURCE LOCK — plus the x6-x9
    #     isolation arms, 4). This plan's own fix is registered in the
    #     same census it extends, so it does not reproduce the defect it
    #     closes (MUTATION M9).
    #   - the chain-form-surface-sweep helper (plan 13-24, CR-04,
    #     `13-VERIFICATION-round6.md` gap 3, Q2): 6 call sites (1 real —
    #     THE SWEEP ITSELF — plus the cf-iso i-v isolation arms, 5). This
    #     plan's own leg is registered in the same census it extends, for
    #     the identical reason the entry-source helper's own fix was: an
    #     unregistered helper's call site is deletable with the battery
    #     green (Q2's own reproduction target).
    #
    # Every search pattern below is built by concatenation rather than as
    # a single literal, and every pattern's NAME is referred to only in
    # prose above (never spelled out here contiguous with its trailing
    # punctuation), so this control's own comment and source do not
    # inflate the counts it takes over the function it lives inside.
    # DISCLOSED LIMITATION: this arm counts source text and observes no
    # behaviour — a call whose returned problems are discarded rather
    # than passed to `_fail` still counts, so it catches deletion of a
    # call, not neutering of its consumption; it does not by itself prove
    # a fixture's verdict is correct — arms 4a/4b and control (v) do
    # that.
    render_contract_src = inspect.getsource(_selftest_render_contract)
    render_t_setdefault_pattern = "scored_verdicts" + ".setdefault("
    render_t_def_pattern = "    def " + "_score_"
    render_t_verdict_call_pattern = "_render_verdict_floor_problems" + "("
    render_t_chain_call_pattern = "_render_chain_verdict_floor_problems" + "("
    render_t_update_pattern = "scored_verdicts" + ".update("
    render_t_coverage_call_pattern = "_render_coverage_floor_problems" + "("
    render_t_example_call_pattern = "_render_example_conformance_problems" + "("
    render_t_entry_source_call_pattern = "_render_entry_source_problems" + "("
    render_t_chain_form_call_pattern = "_render_chain_form_surface_problems" + "("
    render_t_setdefault_count = render_contract_src.count(render_t_setdefault_pattern)
    render_t_def_count = render_contract_src.count(render_t_def_pattern)
    render_t_verdict_call_count = render_contract_src.count(
        render_t_verdict_call_pattern
    )
    render_t_chain_call_count = render_contract_src.count(
        render_t_chain_call_pattern
    )
    render_t_update_count = render_contract_src.count(render_t_update_pattern)
    render_t_coverage_call_count = render_contract_src.count(
        render_t_coverage_call_pattern
    )
    render_t_example_call_count = render_contract_src.count(
        render_t_example_call_pattern
    )
    render_t_entry_source_call_count = render_contract_src.count(
        render_t_entry_source_call_pattern
    )
    render_t_chain_form_call_count = render_contract_src.count(
        render_t_chain_form_call_pattern
    )
    render_t_subscript_pattern = "scored_verdicts" + "["
    render_t_subscript_assign_count = sum(
        1
        for render_t_line in render_contract_src.splitlines()
        if render_t_subscript_pattern in render_t_line and "] = " in render_t_line
    )
    if (
        render_t_setdefault_count != 5
        or render_t_def_count != 4
        or render_t_verdict_call_count != 6
        or render_t_chain_call_count != 6
        or render_t_update_count != 0
        or render_t_subscript_assign_count != 0
        or render_t_coverage_call_count != 7
        or render_t_example_call_count != 6
        or render_t_entry_source_call_count != 5
        or render_t_chain_form_call_count != 6
    ):
        _fail(
            f"(t) SCORING RECORDER LOCK: observed {render_t_setdefault_count} "
            f"recorder-mutation site(s) (expected 5), "
            f"{render_t_def_count} scoring-wrapper definition(s) "
            f"(expected 4), {render_t_verdict_call_count} "
            f"verdict-floor-helper call site(s) (expected 6), "
            f"{render_t_chain_call_count} "
            f"chain-verdict-floor-helper call site(s) "
            f"(expected 6), {render_t_update_count} forbidden recorder "
            f"dict-update occurrence(s) (expected 0), "
            f"{render_t_subscript_assign_count} forbidden bare-subscript "
            f"assignment occurrence(s) (expected 0), "
            f"{render_t_coverage_call_count} coverage-floor-registry "
            f"helper call site(s) (expected 7), "
            f"{render_t_example_call_count} worked-example-conformance "
            f"helper call site(s) (expected 6), and "
            f"{render_t_entry_source_call_count} entry-source helper "
            f"call site(s) (expected 5), and "
            f"{render_t_chain_form_call_count} chain-form-surface-sweep "
            f"helper call site(s) (expected 6)"
        )

    # (u) DISPATCH REACHABILITY. Plan 13-06 (CR-02 / criterion 5): an
    # INDEPENDENT second detector of the same property
    # `scripts/check-traceability.py`'s `_selftest_dispatch_problems`
    # checks, living in a different script so hiding a deleted dispatch
    # requires editing both gates, not one.
    #
    # 1. READ: derive the matrix-named `_selftest_*` symbol set from the
    #    sibling script's source.
    render_u_symbols, render_u_read_problems = _matrix_named_selftest_symbols()
    for render_u_problem in render_u_read_problems:
        _fail(f"(u) DISPATCH REACHABILITY READ: {render_u_problem}")

    # 2. The locked anchor set this derived symbol set is floored
    #    against. As of plan 13-12 (WR-04) the floor itself is EQUALITY,
    #    not a subset test: a subset test (`required - observed`) cannot
    #    see the derived set NARROWING past what it used to cover, only
    #    an anchor going missing entirely — the same "narrowing is
    #    invisible" shape CR-03 showed one level up. The equality
    #    assertion for this set is control (x)'s registry (h) below, not
    #    here: `render_u_required` is a restated locked set rather than a
    #    derived one, by design, because there is no locked set upstream
    #    of it to derive from — narrowing it is intended to be the loud
    #    event, and the LIVE POSITIVE step below is what proves the four
    #    anchors are really dispatched.
    render_u_required = {
        "_selftest_analysis_persistence",
        "_selftest_capture_tool_reader",
        "_selftest_chain_detector_pin",
        "_selftest_render_contract",
    }

    # 3. LIVE POSITIVE: this is the arm that goes red when Item 25's
    #    dispatch is deleted — and it runs from Item 24, which is still
    #    dispatched at that moment, which is why this control lives here
    #    and not inside `_selftest_chain_detector_pin` (the mutation that
    #    threatens it deletes the call to the sub-check that control would
    #    have to live inside, so an arm placed there would never run).
    #    This is the single most likely thing for a future reader to
    #    "simplify" back into the callee — don't.
    render_u_self_test_src = inspect.getsource(self_test)
    render_u_live_problems = _dispatch_reachability_problems(
        render_u_symbols, render_u_self_test_src
    )
    if render_u_live_problems:
        _fail(
            f"(u) DISPATCH REACHABILITY LIVE POSITIVE: "
            f"{render_u_live_problems!r}"
        )

    # 4. SYNTHETIC NEGATIVES: drive `_dispatch_reachability_problems` with
    #    two in-memory sources — never the live tree.
    render_u_neg_uncalled = _dispatch_reachability_problems(
        ("_selftest_x",), "def self_test():\n    pass\n"
    )
    if not (len(render_u_neg_uncalled) == 1 and "_selftest_x" in render_u_neg_uncalled[0]):
        _fail(
            f"(u) DISPATCH REACHABILITY SYNTHETIC NEGATIVE (uncalled): "
            f"expected one problem naming '_selftest_x', got "
            f"{render_u_neg_uncalled!r}"
        )

    render_u_neg_commented = _dispatch_reachability_problems(
        ("_selftest_x",), "def self_test():\n    # _selftest_x()\n"
    )
    if not (len(render_u_neg_commented) == 1 and "_selftest_x" in render_u_neg_commented[0]):
        _fail(
            f"(u) DISPATCH REACHABILITY SYNTHETIC NEGATIVE (commented): "
            f"expected one problem naming '_selftest_x', got "
            f"{render_u_neg_commented!r}"
        )

    # (x) COVERAGE FLOOR REGISTRY. Plan 13-12 (CR-03, WR-04,
    #     `13-REVIEW-plans-08-11.md`): a coverage set that decides WHICH
    #     locked fixtures an arm covers must be DERIVED from the locked
    #     set and floored by EQUALITY — never by a union, a subset test,
    #     or a membership test that a sibling set can satisfy. Round 1
    #     found the original extraction-only floor forgeable (CR-01,
    #     `13-VERIFICATION-plans-01-04.md`); round 2 found the
    #     `scored_ids` floor forgeable two new ways (BL-03,
    #     `13-VERIFICATION.md`); round 3 found the 13-10 rebuild
    #     forgeable a third way (CR-03, this control's namesake). This is
    #     the general property those three rounds are instances of.
    #
    #     Three sets floored here, all by equality against a locked or
    #     derived set: arm 4a's chain re-score table (against the
    #     DERIVED chain family, not the locked set itself — the whole
    #     point is that arm 4a covers a proper SUBSET of the locked ids);
    #     arm 4b's recorded-verdict table (against all twenty-seven locked
    #     ids); and control (u)'s dispatch-reachability symbol set
    #     (against the four locked anchors, replacing WR-04's subset
    #     test, which could not see the required side itself narrowing).
    #
    #     DISCLOSED LIMITS: this registry is hand-registered, so a FOURTH
    #     coverage set added later without an entry here is invisible to
    #     this floor — the same limitation `_RenderRegistrySnapshot`'s
    #     own SCOPE paragraph states for its roster. And
    #     `render_u_required` is a restated locked set rather than a
    #     derived one, by design: there is no locked set upstream of it
    #     to derive from, so narrowing it is intended to be the loud
    #     event, with control (u)'s LIVE POSITIVE step being what proves
    #     the four anchors it names are really dispatched.
    render_chain_family_ids = _render_chain_family_ids(
        render_locked_fixture_ids, _RENDER_CHAIN_FAMILY_PREFIXES
    )

    # DERIVATION NON-VACUITY arm. Both halves are load-bearing: an EMPTY
    # family would let arm 4a shrink to nothing while the equality floor
    # below still passed (MUTATION D's first half — an empty required
    # side is trivially satisfied by an empty actual side only if arm 4a
    # were also emptied, which is exactly the unguarded state this arm
    # exists to forbid); a family equal to the WHOLE locked set would
    # mean the prefix predicate stopped discriminating and had silently
    # promoted the five extra-argument `R-CITE-*`/`R-VERDICT-*` fixtures
    # into an arm whose single-argument scorer cannot score them
    # (MUTATION D's second half).
    if not render_chain_family_ids or not (
        render_chain_family_ids < render_locked_fixture_ids
    ):
        _fail(
            f"(x) DERIVATION NON-VACUITY: chain family "
            f"{sorted(render_chain_family_ids)!r} must be non-empty and a "
            f"PROPER subset of locked fixture ids "
            f"{sorted(render_locked_fixture_ids)!r}"
        )

    render_coverage_floor_entries: tuple[
        tuple[str, frozenset[str], frozenset[str]], ...
    ] = (
        (
            "arm 4a chain re-score table",
            frozenset(render_chain_verdict_expected),
            frozenset(render_chain_family_ids),
        ),
        (
            "arm 4b recorded-verdict table",
            frozenset(render_verdict_expected),
            frozenset(render_locked_fixture_ids),
        ),
        (
            "(u) dispatch-reachability symbol set",
            frozenset(render_u_symbols),
            frozenset(render_u_required),
        ),
    )

    # REGISTRY MEMBERSHIP LOCK, copying control (m)'s `_QUAL01_DOC_ROWS`
    # membership-lock shape: what makes deleting an entry from the
    # registry above LOUD instead of silently shrinking coverage.
    render_x_entry_names = tuple(
        name for name, _, _ in render_coverage_floor_entries
    )
    render_x_expected_entry_names = (
        "arm 4a chain re-score table",
        "arm 4b recorded-verdict table",
        "(u) dispatch-reachability symbol set",
    )
    if render_x_entry_names != render_x_expected_entry_names:
        _fail(
            f"(x) REGISTRY MEMBERSHIP LOCK: coverage-floor entry names "
            f"{render_x_entry_names!r} != expected "
            f"{render_x_expected_entry_names!r}"
        )

    # (x) ENTRY-SOURCE LOCK. R4-CR-02 (`13-VERIFICATION-round4.md`): the
    #     REGISTRY MEMBERSHIP LOCK above compares entry NAMES only —
    #     nothing asserted that an entry's `required` side is the
    #     independently-derived value it claims to be, so rebinding arm
    #     4a's `required` binding above to its own `actual` side made
    #     that entry `x != x`, structurally incapable of reporting a
    #     problem, while every name and every isolation arm still passed.
    #     This arm RE-DERIVES each entry's required side from PRIMARY
    #     SOURCES at lock time — never by reading the registry's own
    #     binding above and never by reusing the local variable the
    #     registry was built from — and rejects an entry whose two sides
    #     are bound to one object.
    #
    #     `render_x_entry_source_expected`'s arm-4a value is a FRESH call
    #     to `_render_chain_family_ids`, not the `render_chain_family_ids`
    #     local above: comparing against that local would be defeated by
    #     rebinding the local itself before the registry is constructed
    #     (MUTATION M2). Arm 4b's expectation (13-27, WR-03, `13-REVIEW.md`)
    #     is a SECOND, independent transcription of the twenty-seven locked
    #     fixture ids, matching what `"(u) dispatch-reachability symbol
    #     set"`'s expectation already does with its four anchors below —
    #     before this transcription, arm 4b's entry here read
    #     `frozenset(render_locked_fixture_ids)`, the SAME local the
    #     registry entry above was built from, which is exactly the
    #     "never by reusing the local variable the registry was built
    #     from" violation this arm's own docstring paragraph forbids: a
    #     rebind of that one local — narrowing it together with both
    #     expected-verdict tables in the same edit — would have been
    #     invisible to this lock. `"(u) dispatch-reachability symbol
    #     set"`'s expectation is a SECOND, independent transcription of
    #     control (u)'s `render_u_required` anchor set — naming a fifth
    #     anchor is deliberately a two-place edit, matching the reason
    #     control (u) already gives for that set being restated rather
    #     than derived.
    #
    #     DISCLOSED LIMITATION: a rebind of a registry entry's required
    #     side to an expression of EQUAL value is harmless by
    #     construction and therefore invisible to this arm's WRONG SOURCE
    #     shape — only a rebind that changes what the entry actually
    #     requires, or aliases it to its own actual side, is caught.
    render_x_entry_source_expected: dict[str, frozenset[str]] = {
        "arm 4a chain re-score table": frozenset(
            _render_chain_family_ids(
                render_locked_fixture_ids, _RENDER_CHAIN_FAMILY_PREFIXES
            )
        ),
        "arm 4b recorded-verdict table": frozenset(
            {
                "R-CHAIN-CONFORMING", "R-CHAIN-NUMBERED", "R-CHAIN-WRAPPED",
                "R-CITE-INLINE", "R-CITE-LEDGER", "R-CITE-NONE",
                "R-VERDICT-EXPIRY", "R-VERDICT-EXPIRY-BAD",
                "R-HEAD-ALLCHAIN", "R-HEAD-CHAINREF", "R-HEAD-PROSE-BAD",
                "R-HEAD-PROSE-MID", "R-HEAD-GTHOP-BAD", "R-HEAD-GTHOP-OK",
                "R-HEAD-GTHOP-LATE",
                "R-HEAD-PERIOD-BAD", "R-HEAD-PERIOD-OK", "R-HEAD-PERIOD-LATE",
                "R-CLAIM-LABEL-BARE", "R-CLAIM-LABEL-INLINE",
                "R-CLAIM-LABEL-CITED", "R-CLAIM-COLON-MID", "R-CLAIM-COLON-END",
                "R-CLAIM-TERSE-DROP", "R-CLAIM-TERSE-KEEP",
                "R-CLAIM-CAVEAT-MARKED", "R-CLAIM-CAVEAT-CITED",
            }
        ),
        "(u) dispatch-reachability symbol set": frozenset(
            {
                "_selftest_analysis_persistence",
                "_selftest_capture_tool_reader",
                "_selftest_chain_detector_pin",
                "_selftest_render_contract",
            }
        ),
    }
    for render_x_entry_source_problem in _render_entry_source_problems(
        render_coverage_floor_entries, render_x_entry_source_expected
    ):
        _fail(f"(x) ENTRY-SOURCE LOCK: {render_x_entry_source_problem}")

    # THE FLOOR ITSELF.
    for render_x_problem in _render_coverage_floor_problems(
        render_coverage_floor_entries
    ):
        _fail(f"(x) COVERAGE FLOOR: {render_x_problem}")

    # (x) ISOLATION arms. Drive the two new pure helpers with SYNTHETIC
    # literals only — never `render_locked_fixture_ids`, never
    # `_RENDER_CHAIN_FAMILY_PREFIXES`, never either expected-verdict
    # table — mirroring controls (p)/(s)'s existing discipline.
    render_x1_problems = _render_coverage_floor_problems(
        (("x1 CLEAN", frozenset({"A", "B"}), frozenset({"A", "B"})),)
    )
    if render_x1_problems != []:
        _fail(
            f"(x) ISOLATION x1 CLEAN: a matching entry wrongly reported a "
            f"problem: {render_x1_problems!r}"
        )

    render_x2_problems = _render_coverage_floor_problems(
        (("x2 NARROWED", frozenset({"A"}), frozenset({"A", "B"})),)
    )
    if (
        len(render_x2_problems) != 1
        or "x2 NARROWED" not in render_x2_problems[0]
        or "B" not in render_x2_problems[0]
    ):
        _fail(
            f"(x) ISOLATION x2 NARROWED: expected exactly one problem "
            f"naming 'x2 NARROWED' and the missing id 'B', got "
            f"{render_x2_problems!r}"
        )

    render_x3_problems = _render_coverage_floor_problems(
        (("x3 UNEXPECTED", frozenset({"A", "C"}), frozenset({"A"})),)
    )
    if (
        len(render_x3_problems) != 1
        or "x3 UNEXPECTED" not in render_x3_problems[0]
        or "C" not in render_x3_problems[0]
    ):
        _fail(
            f"(x) ISOLATION x3 UNEXPECTED: expected exactly one problem "
            f"naming 'x3 UNEXPECTED' and the unexpected id 'C', got "
            f"{render_x3_problems!r}"
        )

    # x4 ANTI-MASKING — the CR-03 reproduction in miniature: this is the
    # property the deleted union check did not have — a WHOLE sibling
    # entry cannot discharge a NARROWED one. A third, independently
    # narrowed entry is included (rather than the minimal two) so this
    # arm also discriminates an accumulating loop from one that returns
    # after the first problem it finds: with only two entries the
    # single real problem always sits last, so a first-entry-wins helper
    # is indistinguishable from a correct one — with two SEPARATE
    # narrowed entries after the whole sibling, a first-entry-wins
    # helper reports only one of them while the correct helper reports
    # both.
    render_x4_problems = _render_coverage_floor_problems(
        (
            ("x4 WHOLE SIBLING", frozenset({"A", "B"}), frozenset({"A", "B"})),
            ("x4 NARROWED FIRST", frozenset({"A"}), frozenset({"A", "B"})),
            ("x4 NARROWED SECOND", frozenset({"C"}), frozenset({"C", "D"})),
        )
    )
    if (
        len(render_x4_problems) != 2
        or not any("x4 NARROWED FIRST" in p for p in render_x4_problems)
        or not any("x4 NARROWED SECOND" in p for p in render_x4_problems)
        or any("x4 WHOLE SIBLING" in p for p in render_x4_problems)
    ):
        _fail(
            f"(x) ISOLATION x4 ANTI-MASKING: expected exactly two "
            f"problems, naming 'x4 NARROWED FIRST' and 'x4 NARROWED "
            f"SECOND', and none naming 'x4 WHOLE SIBLING', got "
            f"{render_x4_problems!r}"
        )

    # x5 DERIVATION: `_render_chain_family_ids` proven to discriminate
    # rather than to echo its input.
    render_x5_chain_ids = _render_chain_family_ids(
        {"P-ONE-A", "P-ONE-B", "Q-TWO-A", "Q-TWO-B"}, ("P-ONE-",)
    )
    if render_x5_chain_ids != {"P-ONE-A", "P-ONE-B"}:
        _fail(
            f"(x) ISOLATION x5 DERIVATION: expected "
            f"{{'P-ONE-A', 'P-ONE-B'}}, got {render_x5_chain_ids!r}"
        )
    render_x5_chain_ids_none = _render_chain_family_ids(
        {"P-ONE-A", "P-ONE-B", "Q-TWO-A", "Q-TWO-B"}, ("Z-NOSUCH-",)
    )
    if render_x5_chain_ids_none != set():
        _fail(
            f"(x) ISOLATION x5 DERIVATION (no match): expected empty set, "
            f"got {render_x5_chain_ids_none!r}"
        )

    # x6-x9 ISOLATION: the ENTRY-SOURCE LOCK's own falsifiability. Every
    # arm drives `_render_entry_source_problems` with SYNTHETIC literals
    # only — never `render_locked_fixture_ids`, never
    # `_RENDER_CHAIN_FAMILY_PREFIXES`, never either expected-verdict
    # table, never the live registry — copying the x1-x5 arms' existing
    # discipline exactly.
    render_x6_problems = _render_entry_source_problems(
        (("x6 CLEAN", frozenset({"A"}), frozenset({"B"})),),
        {"x6 CLEAN": frozenset({"B"})},
    )
    if render_x6_problems != []:
        _fail(
            f"(x) ISOLATION x6 CLEAN: a matching entry wrongly reported a "
            f"problem: {render_x6_problems!r}"
        )

    render_x7_problems = _render_entry_source_problems(
        (("x7 WRONG SOURCE", frozenset({"A"}), frozenset({"A", "B"})),),
        {"x7 WRONG SOURCE": frozenset({"A"})},
    )
    if (
        len(render_x7_problems) != 1
        or "x7 WRONG SOURCE" not in render_x7_problems[0]
        or "B" not in render_x7_problems[0]
    ):
        _fail(
            f"(x) ISOLATION x7 WRONG SOURCE: expected exactly one problem "
            f"naming 'x7 WRONG SOURCE' and the differing id 'B', got "
            f"{render_x7_problems!r}"
        )

    render_x8_problems = _render_entry_source_problems(
        (("x8 UNREGISTERED", frozenset({"A"}), frozenset({"A"})),),
        {},
    )
    if (
        len(render_x8_problems) != 1
        or "x8 UNREGISTERED" not in render_x8_problems[0]
    ):
        _fail(
            f"(x) ISOLATION x8 UNREGISTERED: expected exactly one problem "
            f"naming 'x8 UNREGISTERED', got {render_x8_problems!r}"
        )

    render_x9_shared = frozenset({"A"})
    render_x9_problems = _render_entry_source_problems(
        (("x9 ALIASED", render_x9_shared, render_x9_shared),),
        {"x9 ALIASED": frozenset({"A"})},
    )
    if (
        len(render_x9_problems) != 1
        or "x9 ALIASED" not in render_x9_problems[0]
        or "ALIASED" not in render_x9_problems[0]
    ):
        _fail(
            f"(x) ISOLATION x9 ALIASED: expected exactly one problem "
            f"naming 'x9 ALIASED' and identifying the aliasing, got "
            f"{render_x9_problems!r}"
        )

    # (y) EXAMPLE CONFORMANCE. Plan 13-14 closes CR-01
    #     (`13-VERIFICATION-round3.md`): a shipped worked example may not
    #     ASSERT a conformance property it does not have. Scope is
    #     DERIVED from the assertion itself — every `shared/examples/*.md`
    #     file whose text, after whitespace normalization, contains
    #     `_RENDER_EXAMPLE_CLAIM_LITERAL` — so a THIRD example adopting
    #     the claim is covered the moment it does, with no gate edit. This
    #     is the same derived-not-restated rule control (x) installed one
    #     layer down, applied here to worked-example content.
    #
    #     DISCLOSED LIMITS: this leg checks only files that make the
    #     claim, not all fourteen `shared/examples/*.md` files — a
    #     whole-tree sweep was measured and rejected as out of this
    #     plan's scope (see `13-14-SUMMARY.md`: the other twelve files'
    #     section-4 slices are mostly not even in the shape this leg's
    #     block extraction expects). It checks chain FORM via the frozen
    #     detector, not whether the chain's reasoning is sound. Block
    #     boundaries are a heading/rule heuristic, not a markdown parse.
    #     And it detects a chain rendered in the already-malformed form;
    #     it does not detect every re-wrap of an already-conforming head,
    #     because the form check requires only two arrows in the truncated
    #     candidate, so a wrap or a GT-led hop after the second arrow is
    #     scored conforming, and a head split across two physical lines is
    #     scored conforming with its first input dropped — a property of
    #     the detector frozen under CONTRACT-06 and therefore an accepted
    #     limitation, not a defect this plan closed (13-21's measured
    #     attribution, matching both `| QUAL-01 |` doc rows; the prior
    #     `any()`-over-candidates masking attribution this comment carried
    #     was retracted there — WR-01, `13-REVIEW.md`).
    render_y_texts, render_y_read_problems = _read_render_example_texts()
    for render_y_problem in render_y_read_problems:
        _fail(f"(y) EXAMPLE CONFORMANCE READ: {render_y_problem}")

    render_y_claiming_relpaths = _render_example_claiming_relpaths(
        render_y_texts, _RENDER_EXAMPLE_CLAIM_LITERAL
    )

    # NON-VACUITY FLOOR, by EQUALITY, reusing control (x)'s own
    # `_render_coverage_floor_problems` primitive rather than restating an
    # ad hoc equality test. Deliberately NOT folded into control (x)'s own
    # `render_coverage_floor_entries` registry above: that registry is
    # built and locked before these example texts are read, and its own
    # scope is the dispatch/chain-family mechanism, not worked-example
    # content — mixing the two would blur what a REGISTRY MEMBERSHIP LOCK
    # failure is actually reporting. The equality-floor HELPER is shared;
    # the registry is not.
    for render_y_problem in _render_coverage_floor_problems(
        (
            (
                "(y) example claiming-file set",
                frozenset(render_y_claiming_relpaths),
                frozenset(_RENDER_EXAMPLE_CLAIMING_FILES),
            ),
        )
    ):
        _fail(f"(y) EXAMPLE CONFORMANCE NON-VACUITY: {render_y_problem}")
    if not render_y_texts:
        _fail(
            f"(y) EXAMPLE CONFORMANCE NON-VACUITY: {_RENDER_EXAMPLE_GLOB!r} "
            f"yielded an empty text mapping"
        )

    # BLOCK-COUNT FLOOR: the total blocks derived across the claiming
    # files must be non-zero and equal a derived-and-floored count
    # (measured: 1 + 3 = 4), following control (m)'s NEGATIVE-CASE COUNT
    # FLOOR shape — the derived number is reported so a future change is
    # diagnosed, not merely rejected.
    render_y_block_count = sum(
        len(_render_example_chain_blocks(render_y_texts[relpath]))
        for relpath in render_y_claiming_relpaths
    )
    if render_y_block_count != 4:
        _fail(
            f"(y) EXAMPLE CONFORMANCE BLOCK-COUNT FLOOR: derived "
            f"{render_y_block_count} chain block(s) across "
            f"{len(render_y_claiming_relpaths)} claiming file(s) != "
            f"expected 4"
        )

    # THE LEG ITSELF: every derived block, scored by the unmodified frozen
    # detector.
    for render_y_problem in _render_example_conformance_problems(
        render_y_texts,
        _RENDER_EXAMPLE_CLAIM_LITERAL,
        _chain_block_well_formed,
    ):
        _fail(f"(y) EXAMPLE CONFORMANCE: {render_y_problem}")

    # (z) ISOLATION, leg 5's own falsifiability. Every arm drives the
    #     Task-1 helpers with SYNTHETIC literals and a local synthetic
    #     scorer — never the real example texts, never
    #     `_RENDER_EXAMPLE_CLAIM_LITERAL`, never the frozen detector.
    render_z_claim = "in the synthetic head form"

    def render_z_scorer(block_text: str) -> bool:
        return "GOOD" in block_text

    # z1 DERIVATION CLEAN.
    render_z1_relpaths = _render_example_claiming_relpaths(
        {
            "synthetic/claims.md": f"Some prose. {render_z_claim} More prose.",
            "synthetic/silent.md": "Some prose with no assertion at all.",
        },
        render_z_claim,
    )
    if render_z1_relpaths != ("synthetic/claims.md",):
        _fail(
            f"(z1) DERIVATION CLEAN: expected "
            f"('synthetic/claims.md',), got {render_z1_relpaths!r}"
        )

    # z2 DERIVATION WRAPPED-CLAIM (the A-02 property, asserted in-process:
    # a per-line implementation fails here).
    render_z2_relpaths = _render_example_claiming_relpaths(
        {
            "synthetic/wrapped.md": (
                "Some prose asserting the property in\n"
                "the synthetic head form, more prose."
            ),
        },
        render_z_claim,
    )
    if render_z2_relpaths != ("synthetic/wrapped.md",):
        _fail(
            f"(z2) DERIVATION WRAPPED-CLAIM: expected "
            f"('synthetic/wrapped.md',), got {render_z2_relpaths!r}"
        )

    # z3 BLOCK BOUND: two headings separated by a `---` rule must yield
    # exactly two blocks, and the first must not contain the second
    # heading's content. A splitter that runs to end of text fails here.
    render_z3_text = (
        "intro\n"
        "### Conclusion: first block heading\n"
        "GT-1 (a) + GT-2 (b)\n"
        "-> claim one\n"
        "---\n"
        "### Conclusion: second block heading\n"
        "GT-3 (c) + GT-4 (d)\n"
        "-> claim two\n"
    )
    render_z3_blocks = _render_example_chain_blocks(render_z3_text)
    if len(render_z3_blocks) != 2:
        _fail(
            f"(z3) BLOCK BOUND: expected 2 blocks, got "
            f"{len(render_z3_blocks)}"
        )
    elif "second block heading" in render_z3_blocks[0][1]:
        _fail(
            "(z3) BLOCK BOUND: the first block's text "
            "contains the second heading's content — the bound is not "
            "load-bearing"
        )

    # z4 BLOCK LINE NUMBERS: each reported line number must equal the
    # 1-based line of its own heading in the synthetic text.
    if len(render_z3_blocks) == 2 and (
        render_z3_blocks[0][0] != 2 or render_z3_blocks[1][0] != 6
    ):
        _fail(
            f"(z4) BLOCK LINE NUMBERS: expected (2, 6), got "
            f"{(render_z3_blocks[0][0], render_z3_blocks[1][0])!r}"
        )

    # z5 CONFORMANCE CLEAN.
    render_z5_problems = _render_example_conformance_problems(
        {
            "synthetic/clean.md": (
                f"{render_z_claim} appears here.\n"
                "### Conclusion: ok\nGOOD content\n"
            ),
        },
        render_z_claim,
        render_z_scorer,
    )
    if render_z5_problems != []:
        _fail(
            f"(z5) CONFORMANCE CLEAN: expected [], got "
            f"{render_z5_problems!r}"
        )

    # z6 CONFORMANCE FAILING: exactly one problem naming the relpath and
    # the block's heading line number.
    render_z6_problems = _render_example_conformance_problems(
        {
            "synthetic/failing.md": (
                f"{render_z_claim} appears here.\n"
                "### Conclusion: bad\nBAD content\n"
            ),
        },
        render_z_claim,
        render_z_scorer,
    )
    if (
        len(render_z6_problems) != 1
        or "synthetic/failing.md" not in render_z6_problems[0]
        or ":2:" not in render_z6_problems[0]
    ):
        _fail(
            f"(z6) CONFORMANCE FAILING: expected exactly one "
            f"problem naming 'synthetic/failing.md' and line 2, got "
            f"{render_z6_problems!r}"
        )

    # z7 CLAIM WITHOUT BLOCKS: a claim with nothing to check is a defect,
    # not a pass.
    render_z7_problems = _render_example_conformance_problems(
        {"synthetic/noblocks.md": f"{render_z_claim} but no chain heading anywhere."},
        render_z_claim,
        render_z_scorer,
    )
    if (
        len(render_z7_problems) != 1
        or "synthetic/noblocks.md" not in render_z7_problems[0]
    ):
        _fail(
            f"(z7) CLAIM WITHOUT BLOCKS: expected exactly one "
            f"problem naming 'synthetic/noblocks.md', got "
            f"{render_z7_problems!r}"
        )

    # z8 NON-CLAIMING FILE IGNORED: proves the leg is scoped by the
    # assertion and does not silently become a whole-tree sweep.
    render_z8_problems = _render_example_conformance_problems(
        {
            "synthetic/unclaimed.md": (
                "no assertion here.\n### Conclusion: bad\nBAD content\n"
            ),
        },
        render_z_claim,
        render_z_scorer,
    )
    if render_z8_problems != []:
        _fail(
            f"(z8) NON-CLAIMING FILE IGNORED: expected [], "
            f"got {render_z8_problems!r}"
        )

    # z9 ANTI-MASKING, multi-file: the same property control (x)'s x4
    # asserts one layer down — a whole clean sibling cannot discharge a
    # narrowed (here, failing) one. Three entries, not the minimal two
    # (mirroring x4's own plan-13-12 redesign after MUTATION H showed a
    # two-entry case cannot discriminate an accumulating loop from one
    # that returns after its first problem): with only ONE failing entry,
    # a first-problem-wins helper produces the identical single-problem
    # output a correct accumulating helper does, so it cannot be caught.
    # With two INDEPENDENT failing entries after the clean sibling, an
    # accumulating helper reports both and a first-problem-wins helper
    # reports only one.
    render_z9_problems = _render_example_conformance_problems(
        {
            "synthetic/a-clean.md": (
                f"{render_z_claim}\n### Conclusion: ok\nGOOD stuff\n"
            ),
            "synthetic/b-failing.md": (
                f"{render_z_claim}\n### Conclusion: bad one\nBAD stuff\n"
            ),
            "synthetic/c-failing.md": (
                f"{render_z_claim}\n### Conclusion: bad two\nBAD stuff\n"
            ),
        },
        render_z_claim,
        render_z_scorer,
    )
    if (
        len(render_z9_problems) != 2
        or not any("synthetic/b-failing.md" in p for p in render_z9_problems)
        or not any("synthetic/c-failing.md" in p for p in render_z9_problems)
        or any("synthetic/a-clean.md" in p for p in render_z9_problems)
    ):
        _fail(
            f"(z9) ANTI-MASKING: expected exactly two "
            f"problems, naming 'synthetic/b-failing.md' and "
            f"'synthetic/c-failing.md', and none naming "
            f"'synthetic/a-clean.md', got {render_z9_problems!r}"
        )

    # (v) RECORDER DELEGATION PROBE. Plan 13-10 (BL-03, `13-VERIFICATION.md`):
    #     proves each of the four wrappers actually delegates to its own
    #     scorer, rather than fabricating a verdict — the shape BL-03's
    #     second reproduced bypass exploited (a wrapper genuinely called,
    #     its real return discarded, with nothing anywhere asserting what
    #     it returned). Probe ids are deliberately outside
    #     `render_locked_fixture_ids` and are not a proper prefix of any
    #     locked id, so the extra recorder keys they add are harmless to
    #     arms 4a/4b above, which iterate only the locked set.
    render_v_chain_false_text = "GT-1 (a) + GT-2 (b) -> lone hop"
    render_v_chain_true_text = (
        "GT-1 (a) + GT-2 (b)\n-> intermediate claim\n-> the conclusion"
    )
    render_v_chain_raw_false = _chain_block_well_formed(render_v_chain_false_text)
    render_v_chain_raw_true = _chain_block_well_formed(render_v_chain_true_text)
    render_v_chain_wrapped_false = _score_chain(
        "PROBE-SCORE-CHAIN", render_v_chain_false_text
    )
    render_v_chain_wrapped_true = _score_chain(
        "PROBE-SCORE-CHAIN", render_v_chain_true_text
    )
    if render_v_chain_wrapped_false != render_v_chain_raw_false:
        _fail(
            f"(v) RECORDER DELEGATION PROBE: _score_chain false-direction "
            f"probe returned {render_v_chain_wrapped_false!r}, raw "
            f"_chain_block_well_formed returned {render_v_chain_raw_false!r}"
        )
    if render_v_chain_wrapped_true != render_v_chain_raw_true:
        _fail(
            f"(v) RECORDER DELEGATION PROBE: _score_chain true-direction "
            f"probe returned {render_v_chain_wrapped_true!r}, raw "
            f"_chain_block_well_formed returned {render_v_chain_raw_true!r}"
        )
    if render_v_chain_wrapped_false == render_v_chain_wrapped_true:
        _fail(
            f"(v) RECORDER DELEGATION PROBE: _score_chain's two probe "
            f"results did not differ ({render_v_chain_wrapped_false!r} == "
            f"{render_v_chain_wrapped_true!r}) — a wrapper returning a "
            f"constant would otherwise satisfy the equality arms above "
            f"against a constant raw comparison"
        )
    render_v_chain_recorded = scored_verdicts.get("PROBE-SCORE-CHAIN")
    render_v_chain_expected_recorded = [
        render_v_chain_raw_false, render_v_chain_raw_true
    ]
    if render_v_chain_recorded != render_v_chain_expected_recorded:
        _fail(
            f"(v) RECORDER DELEGATION PROBE: recorder holds "
            f"{render_v_chain_recorded!r} for 'PROBE-SCORE-CHAIN', "
            f"expected {render_v_chain_expected_recorded!r}"
        )

    render_v_verdict_text = "Accept — measured against GT-1"
    render_v_verdict_raw = _verdict_conforms(render_v_verdict_text)
    render_v_verdict_wrapped = _score_verdict(
        "PROBE-SCORE-VERDICT", render_v_verdict_text
    )
    if render_v_verdict_wrapped != render_v_verdict_raw:
        _fail(
            f"(v) RECORDER DELEGATION PROBE: _score_verdict returned "
            f"{render_v_verdict_wrapped!r}, raw _verdict_conforms returned "
            f"{render_v_verdict_raw!r}"
        )
    if scored_verdicts.get("PROBE-SCORE-VERDICT") != [render_v_verdict_raw]:
        _fail(
            f"(v) RECORDER DELEGATION PROBE: recorder holds "
            f"{scored_verdicts.get('PROBE-SCORE-VERDICT')!r} for "
            f"'PROBE-SCORE-VERDICT', expected {[render_v_verdict_raw]!r}"
        )

    render_v_traced_claim = "a probe claim naming no chain"
    render_v_traced_raw = _claim_is_traced(
        render_v_traced_claim, ["C1"], [render_v_chain_true_text]
    )
    render_v_traced_wrapped = _score_traced(
        "PROBE-SCORE-TRACED",
        render_v_traced_claim,
        ["C1"],
        [render_v_chain_true_text],
    )
    if render_v_traced_wrapped != render_v_traced_raw:
        _fail(
            f"(v) RECORDER DELEGATION PROBE: _score_traced returned "
            f"{render_v_traced_wrapped!r}, raw _claim_is_traced returned "
            f"{render_v_traced_raw!r}"
        )
    if scored_verdicts.get("PROBE-SCORE-TRACED") != [render_v_traced_raw]:
        _fail(
            f"(v) RECORDER DELEGATION PROBE: recorder holds "
            f"{scored_verdicts.get('PROBE-SCORE-TRACED')!r} for "
            f"'PROBE-SCORE-TRACED', expected {[render_v_traced_raw]!r}"
        )

    render_v_ledger_section6 = "no closure ledger content here"
    render_v_ledger_raw = _closure_ledger_fragments(render_v_ledger_section6, ["C1"])
    render_v_ledger_wrapped = _score_ledger(
        "PROBE-SCORE-LEDGER", render_v_ledger_section6, ["C1"]
    )
    if render_v_ledger_wrapped != render_v_ledger_raw:
        _fail(
            f"(v) RECORDER DELEGATION PROBE: _score_ledger returned "
            f"{render_v_ledger_wrapped!r}, raw _closure_ledger_fragments "
            f"returned {render_v_ledger_raw!r}"
        )
    if scored_verdicts.get("PROBE-SCORE-LEDGER") != [bool(render_v_ledger_raw)]:
        _fail(
            f"(v) RECORDER DELEGATION PROBE: recorder holds "
            f"{scored_verdicts.get('PROBE-SCORE-LEDGER')!r} for "
            f"'PROBE-SCORE-LEDGER', expected {[bool(render_v_ledger_raw)]!r}"
        )

    # (w) FLOOR HELPER ISOLATION. Plan 13-10 (BL-03): mirrors control (s)'s
    #     discipline for the two new pure helpers, driven with synthetic
    #     literals only — never `render_locked_fixture_ids`, never
    #     `scored_verdicts`, never `fixtures` — proving both helpers
    #     falsifiable in-process rather than merely satisfied by the live
    #     registries.
    render_w_verdict_clean = _render_verdict_floor_problems(
        {"X": [True]}, {"X": [True]}, []
    )
    if render_w_verdict_clean != []:
        _fail(
            f"(w) FLOOR HELPER ISOLATION verdict CLEAN: a recorded "
            f"sequence matching its expectation wrongly reported a "
            f"problem: {render_w_verdict_clean!r}"
        )

    render_w_verdict_wrong = _render_verdict_floor_problems(
        {"X": [False]}, {"X": [True]}, []
    )
    if len(render_w_verdict_wrong) != 1 or _render_fixture_id_token(
        "X"
    ) not in render_w_verdict_wrong[0]:
        _fail(
            f"(w) FLOOR HELPER ISOLATION verdict WRONG-VERDICT: expected "
            f"exactly one problem naming 'X', got {render_w_verdict_wrong!r}"
        )

    render_w_verdict_missing = _render_verdict_floor_problems(
        {"X": [True]}, {}, []
    )
    if len(render_w_verdict_missing) != 1 or _render_fixture_id_token(
        "X"
    ) not in render_w_verdict_missing[0]:
        _fail(
            f"(w) FLOOR HELPER ISOLATION verdict MISSING: expected exactly "
            f"one problem naming 'X', got {render_w_verdict_missing!r}"
        )

    render_w_verdict_accounted_problems = [
        _render_fixture_problem(
            "mode 2: shape mismatch",
            "X",
            "extracted text is missing required substring(s) ['y']",
        )
    ]
    render_w_verdict_accounted = _render_verdict_floor_problems(
        {"X": [True]}, {}, render_w_verdict_accounted_problems
    )
    if render_w_verdict_accounted != []:
        _fail(
            f"(w) FLOOR HELPER ISOLATION verdict ACCOUNTED: an unrecorded "
            f"id accounted for by a reported problem wrongly stayed "
            f"unaccounted: {render_w_verdict_accounted!r}"
        )

    render_w_verdict_antimask_problems = [
        _render_fixture_problem(
            "mode 2: shape mismatch",
            "X-BAD",
            "extracted text is missing required substring(s) ['y']",
        )
    ]
    render_w_verdict_antimask = _render_verdict_floor_problems(
        {"X": [True], "X-BAD": [True]}, {}, render_w_verdict_antimask_problems
    )
    if len(render_w_verdict_antimask) != 1 or _render_fixture_id_token(
        "X"
    ) not in render_w_verdict_antimask[0]:
        _fail(
            f"(w) FLOOR HELPER ISOLATION verdict ANTI-MASKING: expected "
            f"exactly one problem naming the proper prefix 'X' (not "
            f"'X-BAD'), got {render_w_verdict_antimask!r} — a helper "
            f"reverted to bare `in` containment would let a problem "
            f"naming only 'X-BAD' wrongly discharge 'X' too"
        )

    def render_w_chain_scorer(text: str) -> bool:
        return "ok" in text

    render_w_chain_clean = _render_chain_verdict_floor_problems(
        {"X": True}, {"X": "this text is ok"}, render_w_chain_scorer, []
    )
    if render_w_chain_clean != []:
        _fail(
            f"(w) FLOOR HELPER ISOLATION chain CLEAN: a matching synthetic "
            f"score wrongly reported a problem: {render_w_chain_clean!r}"
        )

    render_w_chain_wrong = _render_chain_verdict_floor_problems(
        {"X": False}, {"X": "this text is ok"}, render_w_chain_scorer, []
    )
    if len(render_w_chain_wrong) != 1 or _render_fixture_id_token(
        "X"
    ) not in render_w_chain_wrong[0]:
        _fail(
            f"(w) FLOOR HELPER ISOLATION chain WRONG-VERDICT: expected "
            f"exactly one problem naming 'X', got {render_w_chain_wrong!r}"
        )

    render_w_chain_absent = _render_chain_verdict_floor_problems(
        {"X": True}, {}, render_w_chain_scorer, []
    )
    if len(render_w_chain_absent) != 1 or _render_fixture_id_token(
        "X"
    ) not in render_w_chain_absent[0]:
        _fail(
            f"(w) FLOOR HELPER ISOLATION chain FIXTURE-ABSENT: expected "
            f"exactly one problem REPORTING (not skipping) 'X', got "
            f"{render_w_chain_absent!r}"
        )

    render_w_chain_accounted_problems = [
        _render_fixture_problem(
            "mode 2: shape mismatch",
            "X",
            "extracted text is missing required substring(s) ['ok']",
        )
    ]
    render_w_chain_accounted = _render_chain_verdict_floor_problems(
        {"X": True}, {}, render_w_chain_scorer, render_w_chain_accounted_problems
    )
    if render_w_chain_accounted != []:
        _fail(
            f"(w) FLOOR HELPER ISOLATION chain ACCOUNTED: an absent-fixture "
            f"id accounted for by a reported problem wrongly stayed "
            f"unaccounted: {render_w_chain_accounted!r}"
        )

    # IN-03 (`13-REVIEW-plans-08-11.md`): the chain helper's own
    # ANTI-MASKING arm, mirroring `render_w_verdict_antimask` above — the
    # property is transitively covered by the shared
    # `_render_fixture_id_accounted` prefix logic, but this proves it
    # directly for the chain helper rather than leaving a reader to infer
    # it from the verdict helper's twin.
    render_w_chain_antimask_problems = [
        _render_fixture_problem(
            "mode 2: shape mismatch",
            "X-BAD",
            "extracted text is missing required substring(s) ['ok']",
        )
    ]
    render_w_chain_antimask = _render_chain_verdict_floor_problems(
        {"X": True, "X-BAD": True},
        {},
        render_w_chain_scorer,
        render_w_chain_antimask_problems,
    )
    if len(render_w_chain_antimask) != 1 or _render_fixture_id_token(
        "X"
    ) not in render_w_chain_antimask[0]:
        _fail(
            f"(w) FLOOR HELPER ISOLATION chain ANTI-MASKING: expected "
            f"exactly one problem naming the proper prefix 'X' (not "
            f"'X-BAD'), got {render_w_chain_antimask!r} — a helper "
            f"reverted to bare `in` containment would let the 'X-BAD' "
            f"problem wrongly discharge 'X' too"
        )

    # (q) ISOLATION, fixture accounting. Plan 11-09's replacement for the
    #     old unreachable mode 3 block (WR-06, `11-REVIEW.md`): drives
    #     `_render_fixture_accounting_problems` directly with three
    #     constructed inputs, never touching
    #     `_RENDER_CONTRACT_EXTRACTION_TABLE`. A clean case must report no
    #     problem, a duplicated-id case must name the duplicate, and a
    #     count-mismatch case must name both counts — each assertion fails
    #     when its own branch alone is neutralized.
    render_accounting_clean = _render_fixture_accounting_problems(
        ("A", "B", "C"), {"A", "B", "C"}, []
    )
    if render_accounting_clean:
        _fail(
            f"(q) ISOLATION clean case wrongly reported a problem: "
            f"{render_accounting_clean!r}"
        )

    render_accounting_dup = _render_fixture_accounting_problems(
        ("A", "A", "B"), {"A", "B"}, []
    )
    if not any(
        "duplicated row id" in p and "'A'" in p for p in render_accounting_dup
    ):
        _fail(
            f"(q) ISOLATION duplicated-id case did not name the "
            f"duplicate: {render_accounting_dup!r}"
        )

    render_accounting_mismatch = _render_fixture_accounting_problems(
        ("A", "B", "C"), {"A"}, []
    )
    if not any(
        "1 extracted" in p and "0 problems" in p and "3 registered" in p
        for p in render_accounting_mismatch
    ):
        _fail(
            f"(q) ISOLATION count-mismatch case did not name both "
            f"counts: {render_accounting_mismatch!r}"
        )

    # (h) MEMBERSHIP LOCK. Copies the `_TRACE03_DOC_ROWS` precedent (Phase
    #     10, commit `6d3c131`), widened by plan 11-08 (CR-02/WR-01) to
    #     cover every registry the rendering-contract mechanism depends
    #     on — one field per entry of `_RENDER_REGISTRY_FIELDS`, never a
    #     number restated here (WR-06) — not just two: dropping, shrinking, reordering or
    #     text-gutting any of them must not silently stop checking it.
    #     `_render_registry_lock_problems` compares the LIVE snapshot
    #     against literals written inline inside that function, never
    #     against the module constant each field mirrors — see its
    #     docstring. `render_lock_checked` is threaded to control (h2)'s
    #     `checked_fields` floor below.
    render_lock_problems, render_lock_checked = _render_registry_lock_problems(
        _RenderRegistrySnapshot.live()
    )
    for problem in render_lock_problems:
        _fail(f"(h) MEMBERSHIP LOCK: {problem}")

    # (h2) LOCK NEGATIVES. Every case is a `dataclasses.replace` on
    #     `_RenderRegistrySnapshot.live()` — a perturbation of the REAL
    #     registries, never a synthetic snapshot — reproducing the
    #     verifier's own degradation shapes named in
    #     `11-VERIFICATION.md` gap 2: emptying a tuple, emptying a dict,
    #     dropping one entry, or reordering. A case producing no problem
    #     naming its field is a failure naming that field. The first case
    #     is CR-02's exact reproduction; the eleventh is WR-01's.
    render_live_snapshot = _RenderRegistrySnapshot.live()
    # (name, field, required_problem_substring, mutated snapshot). The third
    # element is what makes a case bind to ONE ARM of its field rather than
    # to the field name alone (WR-04, `11-REVIEW-gap-closure.md`): the
    # `literals` field carries two arms, and the digest arm strictly
    # subsumes the clause arm (a hash over the whole dict changes whenever a
    # required clause is gutted), so a field-name-only assertion left the
    # clause arm deletable with both cases still green.
    render_lock_negative_cases: list[
        tuple[str, str, str, _RenderRegistrySnapshot]
    ] = [
        (
            "extraction_rows with every source_file repointed at the "
            "generated tree (WR-03 reproduction)",
            "extraction_rows",
            "!= expected",
            replace(
                render_live_snapshot,
                extraction_rows=tuple(
                    (
                        row[0],
                        "first-principles/agents/references/"
                        "output-template.md",
                        row[2],
                        row[3],
                    )
                    for row in render_live_snapshot.extraction_rows
                ),
            ),
        ),
        (
            "extraction_rows with one anchor repointed at a sibling "
            "block (WR-03 reproduction)",
            "extraction_rows",
            "!= expected",
            replace(
                render_live_snapshot,
                extraction_rows=tuple(
                    (
                        row[0],
                        row[1],
                        row[2],
                        "**Conforming — closure-ledger row:**",
                    )
                    if row[0] == "R-CITE-INLINE"
                    else row
                    for row in render_live_snapshot.extraction_rows
                ),
            ),
        ),
        (
            "extraction_ids emptied (CR-02 reproduction)",
            "extraction_ids",
            'sorted ids',
            replace(render_live_snapshot, extraction_ids=()),
        ),
        (
            "extraction_ids with one id dropped",
            "extraction_ids",
            'sorted ids',
            replace(
                render_live_snapshot,
                extraction_ids=render_live_snapshot.extraction_ids[1:],
            ),
        ),
        (
            "fixture_shape with a chain needle tuple degraded to the "
            "undiscriminating pair (IN-04 reproduction)",
            "fixture_shape",
            'expected discriminating shape',
            replace(
                render_live_snapshot,
                fixture_shape={
                    **render_live_snapshot.fixture_shape,
                    "R-CHAIN-CONFORMING": ("GT-1", "GT-6"),
                },
            ),
        ),
        (
            "fixture_shape with a non-chain needle tuple emptied "
            "(WR-01 reproduction)",
            "fixture_shape",
            "expected discriminating shape",
            replace(
                render_live_snapshot,
                fixture_shape={
                    **render_live_snapshot.fixture_shape,
                    "R-CITE-NONE": (),
                },
            ),
        ),
        (
            "fixture_forbidden emptied",
            "fixture_forbidden",
            '!= expected',
            replace(render_live_snapshot, fixture_forbidden={}),
        ),
        (
            "surfaces with the rubric entry dropped",
            "surfaces",
            '!= expected',
            replace(
                render_live_snapshot,
                surfaces=tuple(
                    s
                    for s in render_live_snapshot.surfaces
                    if s != "shared/spine/references/validation-rubric.md"
                ),
            ),
        ),
        (
            "surfaces reordered",
            "surfaces",
            '!= expected',
            replace(
                render_live_snapshot,
                surfaces=tuple(reversed(render_live_snapshot.surfaces)),
            ),
        ),
        (
            "required_rules with the rubric key dropped",
            "required_rules",
            '!= expected',
            replace(
                render_live_snapshot,
                required_rules={
                    k: v
                    for k, v in render_live_snapshot.required_rules.items()
                    if k != "shared/spine/references/validation-rubric.md"
                },
            ),
        ),
        (
            "contradiction_phrases emptied",
            "contradiction_phrases",
            '!= expected',
            replace(render_live_snapshot, contradiction_phrases=()),
        ),
        (
            "contradiction_phrases with the CR-01 live phrase dropped",
            "contradiction_phrases",
            '!= expected',
            replace(
                render_live_snapshot,
                contradiction_phrases=tuple(
                    p
                    for p in render_live_snapshot.contradiction_phrases
                    if p != "too long for one line wraps"
                ),
            ),
        ),
        (
            "qual01_doc_rows with one entry dropped",
            "qual01_doc_rows",
            '!= expected',
            replace(
                render_live_snapshot,
                qual01_doc_rows=render_live_snapshot.qual01_doc_rows[1:],
            ),
        ),
        (
            "qual01_doc_row_tokens with one token dropped",
            "qual01_doc_row_tokens",
            '!= expected',
            replace(
                render_live_snapshot,
                qual01_doc_row_tokens=render_live_snapshot.qual01_doc_row_tokens[1:],
            ),
        ),
        (
            "pre_contract_wordings emptied (CR-01 reproduction)",
            "pre_contract_wordings",
            "!= expected",
            replace(render_live_snapshot, pre_contract_wordings=()),
        ),
        (
            "pre_contract_wordings with an entry replaced by a bare "
            "contradiction phrase (CR-01's tautology reproduction)",
            "pre_contract_wordings",
            "!= expected",
            replace(
                render_live_snapshot,
                pre_contract_wordings=(
                    "wraps with arrow-led continuation",
                )
                + render_live_snapshot.pre_contract_wordings[1:],
            ),
        ),
        (
            "literals clause arm: R1 gutted (WR-01 reproduction)",
            "literals",
            'is missing its required clause',
            replace(
                render_live_snapshot,
                literals={
                    **render_live_snapshot.literals,
                    "R1": "A hop occupies exactly one physical line.",
                },
            ),
        ),
        (
            "literals digest arm: R1 clause kept, benign sentence appended",
            "literals",
            'digest',
            replace(
                render_live_snapshot,
                literals={
                    **render_live_snapshot.literals,
                    "R1": render_live_snapshot.literals["R1"]
                    + " A trailing continuation is permitted for readability.",
                },
            ),
        ),
        (
            "chain_family_prefixes emptied",
            "chain_family_prefixes",
            "!= expected",
            replace(render_live_snapshot, chain_family_prefixes=()),
        ),
        (
            "example_claim_literal replaced with a different string "
            "(plan 13-14)",
            "example_claim_literal",
            "!= expected",
            replace(
                render_live_snapshot,
                example_claim_literal="a different assertion entirely",
            ),
        ),
        (
            "example_glob emptied (plan 13-14)",
            "example_glob",
            "!= expected",
            replace(render_live_snapshot, example_glob=""),
        ),
        (
            "example_claiming_files with one entry dropped (plan 13-14)",
            "example_claiming_files",
            "!= expected",
            replace(
                render_live_snapshot,
                example_claiming_files=render_live_snapshot.example_claiming_files[
                    1:
                ],
            ),
        ),
        (
            "fabricated_example_wordings emptied (plan 13-23, CR-02 "
            "reproduction)",
            "fabricated_example_wordings",
            "!= expected",
            replace(render_live_snapshot, fabricated_example_wordings=()),
        ),
        (
            "chain_form_signature replaced with a different pattern "
            "(plan 13-24)",
            "chain_form_signature",
            "!= expected",
            replace(
                render_live_snapshot,
                chain_form_signature="a different pattern entirely",
            ),
        ),
        (
            "chain_form_glob emptied (plan 13-24)",
            "chain_form_glob",
            "!= expected",
            replace(render_live_snapshot, chain_form_glob=""),
        ),
        (
            "chain_form_exempt with an entry added (plan 13-24)",
            "chain_form_exempt",
            "!= expected",
            replace(
                render_live_snapshot,
                chain_form_exempt=(("shared/some-file.md", "a reason"),),
            ),
        ),
    ]

    render_lock_negative_fields_exercised: set[str] = set()
    render_lock_negative_arms_exercised: set[tuple[str, str]] = set()
    for (
        case_name,
        case_field,
        case_required_msg,
        mutated_snapshot,
    ) in render_lock_negative_cases:
        render_lock_negative_fields_exercised.add(case_field)
        render_lock_negative_arms_exercised.add((case_field, case_required_msg))
        case_problems, _ = _render_registry_lock_problems(mutated_snapshot)
        if not any(
            case_field in problem and case_required_msg in problem
            for problem in case_problems
        ):
            _fail(
                f"(h2) LOCK NEGATIVE: case {case_name!r} produced no "
                f"problem naming field {case_field!r} AND matching this "
                f"case's arm {case_required_msg!r} — {case_problems!r}"
            )

    # (h2) ANTI-MASKING FLOOR, copying HARN-01's shape
    #     (`scripts/check-act-limb.py`): a case table failing to cover the
    #     full field set, or the lock itself failing to check a field, is
    #     caught here rather than leaving either uncovered.
    render_snapshot_field_names = tuple(
        f.name for f in fields(_RenderRegistrySnapshot)
    )
    if render_snapshot_field_names != _RENDER_REGISTRY_FIELDS:
        _fail(
            f"(h2) ANTI-MASKING FLOOR: _RenderRegistrySnapshot field names "
            f"{render_snapshot_field_names!r} != _RENDER_REGISTRY_FIELDS "
            f"{_RENDER_REGISTRY_FIELDS!r} — a field was added to the "
            f"snapshot without being registered in _RENDER_REGISTRY_FIELDS"
        )
    if render_lock_negative_fields_exercised != set(_RENDER_REGISTRY_FIELDS):
        render_missing_case_fields = (
            set(_RENDER_REGISTRY_FIELDS) - render_lock_negative_fields_exercised
        )
        _fail(
            f"(h2) ANTI-MASKING FLOOR: the case table exercises "
            f"{sorted(render_lock_negative_fields_exercised)!r}, missing a "
            f"negative case for {sorted(render_missing_case_fields)!r} — a "
            f"registry added to the lock without a negative case is "
            f"unfalsifiable"
        )
    if render_lock_checked != set(_RENDER_REGISTRY_FIELDS):
        render_skipped_fields = set(_RENDER_REGISTRY_FIELDS) - render_lock_checked
        _fail(
            f"(h2) ANTI-MASKING FLOOR: the positive lock call at (h) only "
            f"compared {sorted(render_lock_checked)!r}, silently skipping "
            f"{sorted(render_skipped_fields)!r}"
        )
    # ARM FLOOR (WR-04, `11-REVIEW-gap-closure.md`). The predecessor of
    # this block matched on the case table's NAME strings (`"clause" in
    # name`), which asserted only that somebody had typed the word — the
    # clause arm itself could be deleted from
    # `_render_registry_lock_problems` and both literals cases stayed green,
    # because the digest arm subsumes it and each case only had to yield
    # SOME problem containing "literals". The floor now ranges over the
    # (field, required-substring) pairs the loop above actually bound, so
    # each named arm has a case that fails when THAT arm is deleted.
    render_literals_arms = {
        required_msg
        for field, required_msg in render_lock_negative_arms_exercised
        if field == "literals"
    }
    render_required_literals_arms = {
        "is missing its required clause",
        "digest",
    }
    if not render_required_literals_arms <= render_literals_arms:
        _fail(
            f"(h2) ANTI-MASKING FLOOR: the literals field's two arms "
            f"(clause, digest) are not both bound to a case by required "
            f"message substring — bound arms {sorted(render_literals_arms)!r}, "
            f"missing "
            f"{sorted(render_required_literals_arms - render_literals_arms)!r} "
            f"— an unbound arm can be deleted while the other keeps the "
            f"field 'covered'"
        )

    # (r) ISOLATION, decode-error fail-closed (WR-08, `11-REVIEW.md`).
    #     `_read_text_or_problem` is the module-level reader both
    #     `_read_render_surfaces` (control (i) below) and
    #     `_read_qual01_doc_rows` (control (m)) route through as of plan
    #     11-11 — neither keeps its own `try`/`except`. Drives it directly
    #     against a `tempfile.TemporaryDirectory()` fixture, never a repo
    #     path, so the battery's FROZEN-EVIDENCE and frozen-path write
    #     guard stay unaffected. Two arms, both branches of the widened
    #     `except (OSError, ValueError)`: a readable-but-invalid-UTF-8 file
    #     (`UnicodeDecodeError` is a `ValueError`) and a nonexistent path
    #     (`OSError`). The call is wrapped in `try`/`except Exception` at
    #     THIS level so that neutralizing the widened catch back to
    #     `except OSError` alone converts the escaped `UnicodeDecodeError`
    #     into a named `_fail`, not an uncaught traceback — the same
    #     graceful-red shape every other control here already has.
    with tempfile.TemporaryDirectory() as render_tmp_dir:
        render_bad_utf8_path = Path(render_tmp_dir) / "not-utf8.md"
        render_bad_utf8_path.write_bytes(b"\xff\xfe\x00 not valid utf-8")
        try:
            render_bad_text, render_bad_problem = _read_text_or_problem(
                render_bad_utf8_path, "not-utf8.md"
            )
        except Exception as exc:
            _fail(
                "(r) ISOLATION decode-error case: _read_text_or_problem "
                f"raised {exc!r} instead of returning a named problem — a "
                f"decode error must not escape as an uncaught exception"
            )
        else:
            if render_bad_text is not None:
                _fail(
                    "(r) ISOLATION decode-error case: "
                    f"_read_text_or_problem returned text "
                    f"{render_bad_text!r} for an invalid-UTF-8 file "
                    f"instead of a named problem"
                )
            if render_bad_problem is None or "not-utf8.md" not in render_bad_problem:
                _fail(
                    "(r) ISOLATION decode-error case: problem "
                    f"{render_bad_problem!r} does not name the relpath "
                    f"'not-utf8.md'"
                )

        render_missing_path = Path(render_tmp_dir) / "does-not-exist.md"
        try:
            render_missing_text, render_missing_problem = _read_text_or_problem(
                render_missing_path, "does-not-exist.md"
            )
        except Exception as exc:
            _fail(
                "(r) ISOLATION missing-file case: _read_text_or_problem "
                f"raised {exc!r} instead of returning a named problem"
            )
        else:
            if render_missing_text is not None:
                _fail(
                    "(r) ISOLATION missing-file case: "
                    f"_read_text_or_problem returned text "
                    f"{render_missing_text!r} for a nonexistent path "
                    f"instead of a named problem"
                )
            if (
                render_missing_problem is None
                or "does-not-exist.md" not in render_missing_problem
            ):
                _fail(
                    "(r) ISOLATION missing-file case: problem "
                    f"{render_missing_problem!r} does not name the "
                    f"relpath 'does-not-exist.md'"
                )

    # (i) POSITIVE. Reads the real shipped bytes; goes RED if a REQUIRED
    #     rule is deleted from any of the four canonical surfaces today,
    #     or if any surface currently contradicts the no-wrap rule.
    render_reads, render_read_problems = _read_render_surfaces()
    for problem in render_read_problems:
        _fail(f"(i) POSITIVE: could not read a registered surface: {problem}")
    for read in render_reads:
        for problem in _render_rule_report(read):
            _fail(f"(i) POSITIVE: {problem}")

    # (i2) POSITIVE, rendered-example claim floor (plan 13-23, CR-02
    #     `13-VERIFICATION-round6.md` gap 2). Reads the same per-surface
    #     reads the unscoped contradiction scan above already consumes and
    #     runs `_render_example_claim_floor_problems` over ALL of them at
    #     once — UNSCOPED like the contradiction scan, applying to EVERY
    #     entry of `_RENDER_RULE_SURFACES` regardless of that surface's
    #     required-rule set, because a fabricated claim is wrong wherever
    #     it appears. Goes RED if a registered surface currently claims
    #     its examples follow the head form without actually rendering
    #     that form in a fenced block.
    render_claim_texts = {read.relpath: read.text for read in render_reads}
    for problem in _render_example_claim_floor_problems(
        render_claim_texts,
        _RENDER_FABRICATED_EXAMPLE_WORDINGS,
        _RENDER_RULE_LITERALS["R8"],
    ):
        _fail(f"(i2) POSITIVE: {problem}")

    # (i3) NEGATIVE, fabricated-example wording — DETECTION, falsifiable
    #     (plan 13-23, copying control (l1)'s shape). `shared/spine/
    #     references/validation-rubric.md` discharges R8 with an INLINE
    #     backtick span, not a fenced block (the read_first pointer at
    #     that file's line 340) — it is the one registered surface whose
    #     real text does NOT already render R8's head literal inside a
    #     fence, so appending a fabricated wording to ITS real text is a
    #     genuine fabrication, unlike appending one to `output-
    #     template.md` or `SKILL-body.md`, which already carry a real
    #     fenced head and would make the appended sentence TRUE of them —
    #     exactly the property task 3's P2 mutation proves on the real
    #     tree. For each wording, appends it to the rubric's real read
    #     text — never mutating the file on disk — and requires
    #     `_render_example_claim_floor_problems` to report that relpath.
    render_i3_base_relpath = "shared/spine/references/validation-rubric.md"
    render_i3_base_read = next(
        (r for r in render_reads if r.relpath == render_i3_base_relpath), None
    )
    if render_i3_base_read is None:
        _fail(
            f"(i3) NEGATIVE setup: {render_i3_base_relpath!r} was not "
            f"among the surfaces read at (i) — cannot drive the "
            f"non-vacuity control"
        )
    else:
        render_i3_unfired: list[str] = []
        for wording in _RENDER_FABRICATED_EXAMPLE_WORDINGS:
            mutated_texts = {
                render_i3_base_relpath: render_i3_base_read.text + "\n" + wording
            }
            mutated_problems = _render_example_claim_floor_problems(
                mutated_texts,
                _RENDER_FABRICATED_EXAMPLE_WORDINGS,
                _RENDER_RULE_LITERALS["R8"],
            )
            if not any(render_i3_base_relpath in p for p in mutated_problems):
                render_i3_unfired.append(wording[:40])
        if render_i3_unfired:
            _fail(
                f"(i3) NEGATIVE: {len(render_i3_unfired)} wording(s) did "
                f"not fire when appended in memory to "
                f"{render_i3_base_relpath!r}: {render_i3_unfired!r}"
            )

    # (i3) CASE-COUNT FLOOR. Floors the wording count so emptying
    #     `_RENDER_FABRICATED_EXAMPLE_WORDINGS` fails by name rather than
    #     degenerating to zero cases — the CR-01
    #     (`11-REVIEW-gap-closure.md`) shape applied to this registry.
    if len(_RENDER_FABRICATED_EXAMPLE_WORDINGS) != 3:
        _fail(
            f"(i3) CASE-COUNT FLOOR: expected 3 pinned fabricated-example "
            f"wordings, got {len(_RENDER_FABRICATED_EXAMPLE_WORDINGS)}"
        )

    # (i4) ISOLATION. Drives `_render_example_claim_floor_problems` with a
    #     synthetic `texts` map, never a real surface — proves the helper
    #     itself discriminates a claiming file WITH a fenced head from one
    #     WITHOUT, independent of any registered surface's real content.
    render_i4_head_literal = _RENDER_RULE_LITERALS["R8"]
    render_i4_with_fence = (
        "Rendered examples follow the prescribed head form "
        "(`GT-1? ([brief fact label]) + C2 ([brief fact label])`).\n\n"
        "```text\n"
        f"{render_i4_head_literal}\n"
        "→ [intermediate claim]\n"
        "→ [conclusion]\n"
        "```\n"
    )
    render_i4_without_fence = (
        "Rendered examples follow the prescribed head form "
        "(`GT-1? ([brief fact label]) + C2 ([brief fact label])`).\n"
    )
    render_i4_texts = {
        "synthetic/with-fence.md": render_i4_with_fence,
        "synthetic/without-fence.md": render_i4_without_fence,
    }
    render_i4_problems = _render_example_claim_floor_problems(
        render_i4_texts,
        _RENDER_FABRICATED_EXAMPLE_WORDINGS,
        render_i4_head_literal,
    )
    if any("synthetic/with-fence.md" in p for p in render_i4_problems):
        _fail(
            "(i4) ISOLATION: the claiming file WITH a fenced head "
            f"produced a problem: {render_i4_problems!r}"
        )
    if not any("synthetic/without-fence.md" in p for p in render_i4_problems):
        _fail(
            "(i4) ISOLATION: the claiming file WITHOUT a fenced head "
            f"produced no problem: {render_i4_problems!r}"
        )
    if len(render_i4_problems) != 1:
        _fail(
            f"(i4) ISOLATION: expected exactly one problem, got "
            f"{len(render_i4_problems)}: {render_i4_problems!r}"
        )

    # (j) COVERAGE FLOOR. Phase 10 block (l)'s corrected shape: derived
    #     from the relpaths the read loop actually RETURNED, never from a
    #     re-glob or a restated list. A surface the read loop declined to
    #     open is named at (i) above rather than silently reducing
    #     coverage to whatever was read; this floor additionally proves no
    #     registered surface silently dropped out of the returned records.
    #     Compares a four-element set as of plan 13-20's reason-upward
    #     surface (previously a three-element set as of plan 11-07's
    #     rubric surface).
    read_relpaths = {read.relpath for read in render_reads}
    if read_relpaths != set(_RENDER_RULE_SURFACES):
        _fail(
            f"(j) COVERAGE FLOOR: relpaths actually read {read_relpaths!r} "
            f"do not equal the registered surfaces "
            f"{set(_RENDER_RULE_SURFACES)!r}"
        )

    # (k) NEGATIVE, missing. For each real record and each of that
    #     surface's REQUIRED literal keys (sourced from
    #     _RENDER_SURFACE_REQUIRED_RULES[read.relpath], the same view
    #     _render_rule_report itself uses — not every entry of
    #     _RENDER_RULE_LITERALS), build a NEW _RenderSurfaceRead from that
    #     record's real text with every occurrence of the literal replaced
    #     by the empty string — never mutating the file on disk — and
    #     require _render_rule_report to report a problem naming that
    #     relpath and that key. The case count follows the mapping rather
    #     than a restated number: a floor immediately below requires it to
    #     equal sum(len(keys) for keys in
    #     _RENDER_SURFACE_REQUIRED_RULES.values()), 37 today
    #     (12 + 12 + 8 + 5, three surfaces gaining R11 and R12 at plan
    #     14-03), so shrinking the mapping fails the floor rather than
    #     silently reducing coverage.
    missing_cases_unfired: list[str] = []
    missing_cases_run = 0
    for read in render_reads:
        required_keys = _RENDER_SURFACE_REQUIRED_RULES.get(read.relpath, ())
        for key in required_keys:
            literal = _RENDER_RULE_LITERALS.get(key)
            if literal is None:
                continue
            missing_cases_run += 1
            stripped_text = read.text.replace(literal, "")
            stripped = _RenderSurfaceRead(relpath=read.relpath, text=stripped_text)
            stripped_problems = _render_rule_report(stripped)
            if not any(
                read.relpath in p and key in p for p in stripped_problems
            ):
                missing_cases_unfired.append(f"{read.relpath}/{key}")
    if missing_cases_unfired:
        _fail(
            f"(k) NEGATIVE missing: {len(missing_cases_unfired)} case(s) "
            f"did not fire when the literal was stripped in memory: "
            f"{missing_cases_unfired!r}"
        )
    expected_missing_case_count = 37
    derived_missing_case_count = sum(
        len(keys) for keys in _RENDER_SURFACE_REQUIRED_RULES.values()
    )
    if (
        missing_cases_run != derived_missing_case_count
        or derived_missing_case_count != expected_missing_case_count
    ):
        _fail(
            f"(k) CASE-COUNT FLOOR: expected {expected_missing_case_count} "
            f"cases (derived sum {derived_missing_case_count}), ran "
            f"{missing_cases_run}"
        )

    # (l1) NEGATIVE, contradiction — DETECTION, falsifiable. Plan 11-09
    #     (WR-07, `11-REVIEW.md`): for each real record and each of the
    #     real pre-contract historical wordings in
    #     `_RENDER_PRE_CONTRACT_WORDINGS` (byte-recovered via `git show`,
    #     never retyped), build a NEW `_RenderSurfaceRead` from that
    #     record's real text with the wording appended — never mutating
    #     the file on disk — and require `_render_rule_report` to report a
    #     contradiction problem. This is the arm that carries the real
    #     risk: it goes RED if `_RENDER_CONTRADICTION_PHRASES` is narrowed
    #     past a wording that was actually shipped in this tree.
    render_l1_unfired: list[str] = []
    render_l1_cases_run = 0
    for read in render_reads:
        for wording in _RENDER_PRE_CONTRACT_WORDINGS:
            render_l1_cases_run += 1
            historical = _RenderSurfaceRead(
                relpath=read.relpath, text=read.text + "\n" + wording
            )
            historical_problems = _render_rule_report(historical)
            if not any(
                read.relpath in p and "contradicts the no-wrap rule" in p
                for p in historical_problems
            ):
                render_l1_unfired.append(f"{read.relpath}/{wording[:40]!r}")
    if render_l1_unfired:
        _fail(
            f"(l1) DETECTION: {len(render_l1_unfired)} case(s) did not "
            f"fire when a real pre-contract historical wording was "
            f"appended in memory: {render_l1_unfired!r}"
        )

    # (l1) CASE-COUNT FLOOR (CR-01, `11-REVIEW-gap-closure.md`). The loop
    # above is driven by a registry, so emptying that registry ran it zero
    # times and printed PASSED — byte for byte the degradation shape the
    # verifier ruled blocking for `_RENDER_CONTRACT_EXTRACTION_TABLE`. The
    # wording count is floored against an INLINE 3, and the case count is
    # DERIVED from the records the read loop returned rather than restated,
    # so a surface dropping out of (i)/(j) cannot quietly shrink this leg
    # either.
    if len(_RENDER_PRE_CONTRACT_WORDINGS) != 3:
        _fail(
            f"(l1) CASE-COUNT FLOOR: expected 3 pinned historical "
            f"wordings, got {len(_RENDER_PRE_CONTRACT_WORDINGS)}"
        )
    render_l1_expected_cases = len(render_reads) * len(
        _RENDER_PRE_CONTRACT_WORDINGS
    )
    if (
        render_l1_cases_run != render_l1_expected_cases
        or render_l1_cases_run == 0
    ):
        _fail(
            f"(l1) CASE-COUNT FLOOR: ran {render_l1_cases_run} case(s), "
            f"expected {render_l1_expected_cases} "
            f"({len(render_reads)} surface(s) x "
            f"{len(_RENDER_PRE_CONTRACT_WORDINGS)} wording(s)) and more "
            f"than zero — an emptied registry runs this leg zero times "
            f"and reports PASSED"
        )

    # (l1) NON-TAUTOLOGY FLOOR (CR-01). Nothing else requires a pinned
    # wording to differ from the phrase literals it is supposed to
    # independently confirm: with an entry set to a bare
    # `_RENDER_CONTRADICTION_PHRASES` member, the detection arm degenerates
    # to `x in (y + x)` — the exact tautology WR-07 (`11-REVIEW.md`)
    # removed — inside the registry created to prevent it.
    for wording in _RENDER_PRE_CONTRACT_WORDINGS:
        if wording.strip() in _RENDER_CONTRADICTION_PHRASES:
            _fail(
                f"(l1) NON-TAUTOLOGY FLOOR: pinned wording {wording!r} is "
                f"itself a contradiction phrase — appending it and "
                f"finding it proves nothing about the phrase list"
            )

    # (l2) NEGATIVE, contradiction — MESSAGE FORM, disclosed as such. For
    #     each real record and each contradiction phrasing, build a NEW
    #     `_RenderSurfaceRead` with the phrase appended and require a
    #     problem naming that relpath and that phrase. This is NOT a
    #     detection test — `_render_rule_report` tests `phrase in
    #     read.text`, and `phrase in (text + phrase)` holds for every
    #     string — it checks the reported problem's SHAPE (it names the
    #     relpath and the phrase), which controls (i) and (k) match on.
    #     Kept for that reason, not deleted; the real detection risk is
    #     (l1)'s job.
    contradiction_cases_unfired: list[str] = []
    for read in render_reads:
        for phrase in _RENDER_CONTRADICTION_PHRASES:
            contradicted_text = read.text + " " + phrase
            contradicted = _RenderSurfaceRead(
                relpath=read.relpath, text=contradicted_text
            )
            contradicted_problems = _render_rule_report(contradicted)
            if not any(
                read.relpath in p and phrase in p
                for p in contradicted_problems
            ):
                contradiction_cases_unfired.append(f"{read.relpath}/{phrase}")
    if contradiction_cases_unfired:
        _fail(
            f"(l2) MESSAGE FORM: "
            f"{len(contradiction_cases_unfired)} case(s) did not fire when "
            f"the phrase was appended in memory: "
            f"{contradiction_cases_unfired!r}"
        )

    # (l3) NEGATIVE-of-the-negative. Without this, a `_render_rule_report`
    #     that reported a contradiction for EVERY input would satisfy
    #     (l1) vacuously. Append a benign sentence that states R1
    #     correctly — the R1 literal itself — and require NO contradiction
    #     problem is reported.
    render_l3_wrongly_fired: list[str] = []
    for read in render_reads:
        benign = _RenderSurfaceRead(
            relpath=read.relpath,
            text=read.text + "\n" + _RENDER_RULE_LITERALS["R1"],
        )
        benign_problems = _render_rule_report(benign)
        if any(
            read.relpath in p and "contradicts the no-wrap rule" in p
            for p in benign_problems
        ):
            render_l3_wrongly_fired.append(read.relpath)
    if render_l3_wrongly_fired:
        _fail(
            f"(l3) NEGATIVE-of-the-negative: appending R1's own correct "
            f"literal wrongly triggered a contradiction problem for "
            f"{render_l3_wrongly_fired!r}"
        )

    # (m) QUAL-01 doc-row honesty. STATE.md records that the rest of the
    #     TRACE-03 doc rows' prose is asserted by nothing — a gate
    #     description that over-claims what the gate covers is the same
    #     defect class this milestone exists to close, one layer up.
    #     Reads through the same typed-record discipline as (i)-(l):
    #     `_qual01_row_problem` can only be handed a `_RenderSurfaceRead`
    #     produced by `_read_qual01_doc_rows()`, never a hand-built
    #     `(relpath, text)` pair (plan 11-10, IN-02).
    #     DISCLOSED LIMITATION: asserts the required tokens' presence on
    #     the `| QUAL-01 |` table row only, not the rest of either row's
    #     prose — the row can still over-claim in words no token covers.
    expected_doc_rows = ("CLAUDE.md", "docs/ARCHITECTURE.md")
    if _QUAL01_DOC_ROWS != expected_doc_rows:
        _fail(
            f"(m) MEMBERSHIP LOCK: _QUAL01_DOC_ROWS shrank or reordered — "
            f"expected {expected_doc_rows!r}, got {_QUAL01_DOC_ROWS!r}"
        )

    qual01_reads, qual01_read_problems = _read_qual01_doc_rows()
    for problem in qual01_read_problems:
        _fail(f"(m) could not read a registered doc row: {problem}")

    qual01_read_relpaths: set[str] = set()
    for read in qual01_reads:
        qual01_read_relpaths.add(read.relpath)

        # POSITIVE: every registered doc row carries every required token
        # on its `| QUAL-01 |` row.
        for problem in _qual01_row_problem(read):
            _fail(f"(m) POSITIVE: {problem}")

        for token in _QUAL01_DOC_ROW_TOKENS:
            # NEGATIVE, per (file, token): strip that ONE token from the
            # `| QUAL-01 |` row in an in-memory copy — never the file on
            # disk — and require the same checker to report the defect
            # naming that file and that token.
            stripped_lines = [
                line.replace(token, "")
                if line.lstrip().startswith("| QUAL-01 |")
                else line
                for line in read.text.splitlines()
            ]
            stripped_read = _RenderSurfaceRead(
                relpath=read.relpath, text="\n".join(stripped_lines)
            )
            stripped_problems = _qual01_row_problem(stripped_read)
            if not any(
                read.relpath in p and token in p for p in stripped_problems
            ):
                _fail(
                    f"(m) NEGATIVE: stripping {token!r} from "
                    f"{read.relpath}'s '| QUAL-01 |' row did not produce "
                    f"a problem naming that file and that token"
                )

            # ANTI-MASKING, the IN-03 arm made explicit: build an
            # in-memory copy where the `| QUAL-01 |` row has lost the
            # token but a NON-row line elsewhere in the file gains it.
            # Without this arm the row-scoping is asserted by nothing.
            masked_lines = list(stripped_lines)
            masked_lines.append(f"<!-- non-row QUAL-01 mention: {token} -->")
            masked_read = _RenderSurfaceRead(
                relpath=read.relpath, text="\n".join(masked_lines)
            )
            masked_problems = _qual01_row_problem(masked_read)
            if not any(
                read.relpath in p and token in p for p in masked_problems
            ):
                _fail(
                    f"(m) ANTI-MASKING: {read.relpath}'s '| QUAL-01 |' "
                    f"row lost {token!r} while a non-row line gained it, "
                    f"and no problem was reported — the row-scoping is "
                    f"not being enforced"
                )

    # COVERAGE FLOOR: the relpaths actually read must equal
    # `set(_QUAL01_DOC_ROWS)`, derived from the records the read loop
    # itself returned — never a re-glob (copies control (j)'s shape).
    if qual01_read_relpaths != set(_QUAL01_DOC_ROWS):
        _fail(
            f"(m) COVERAGE FLOOR: read relpaths "
            f"{sorted(qual01_read_relpaths)!r} != registered "
            f"{sorted(_QUAL01_DOC_ROWS)!r}"
        )

    # NEGATIVE-CASE COUNT FLOOR: 2 doc rows x 30 required tokens = 60 cases
    # above, derived from the two registries rather than restated, and
    # floored against an inline expected total of 60 — a doc row or a
    # required token silently dropped shrinks the derived count. Plan
    # 13-17 (WR-02, `13-VERIFICATION-round4.md`) added the tenth and
    # eleventh tokens (`call-site census`, `entry-source lock`), moving
    # this floor from 18 (9 tokens) to 22 (11 tokens). Plan 13-21 (round 5
    # closure) added the twelfth and thirteenth tokens (`R-HEAD-GTHOP-LATE`,
    # `reason-upward.md`), moving this floor from 22 (11 tokens) to 26
    # (13 tokens). Plan 13-28 (round 6 closure) added the fourteenth
    # through seventeenth tokens (`over-rejection bound`,
    # `R-HEAD-PERIOD-BAD`, `chain-form surface sweep`, `rendered-example
    # claim floor`), moving this floor from 26 (13 tokens) to 34
    # (17 tokens). Plan 14-06 added the eighteenth through twenty-third
    # tokens (`closure-ledger claim inventory`, `structural ledger row`,
    # `section-intro label`, `R-CLAIM-LABEL-BARE`, `R-CLAIM-CAVEAT-MARKED`,
    # `quality-ledger-v8.26`), moving this floor from 34 (17 tokens) to 46
    # (23 tokens). The phase-14 review's CR-01/CR-02 fix added the
    # twenty-fourth through twenty-sixth (`fenced pseudo-heading`,
    # `boundary regression`, `silent false-clean`), moving it from 46
    # (23 tokens) to 52 (26 tokens).
    qual01_negative_case_count = len(_QUAL01_DOC_ROWS) * len(
        _QUAL01_DOC_ROW_TOKENS
    )
    if qual01_negative_case_count != 60:
        _fail(
            f"(m) NEGATIVE-CASE COUNT FLOOR: derived "
            f"{qual01_negative_case_count} (file, token) case(s) from "
            f"{len(_QUAL01_DOC_ROWS)} doc row(s) x "
            f"{len(_QUAL01_DOC_ROW_TOKENS)} token(s) != expected 60"
        )

    # (m2) DOCSTRING COUNT LOCK (WR-02, `13-VERIFICATION-round4.md`,
    # closed at 13-17): the count above has now drifted stale in two
    # consecutive plans — round 3's WR-02 (the registry-lock comment
    # counts) and round 4's WR-02 (this function's OWN docstring, which
    # still said 16 (2 doc rows x 8 tokens) while the code above said 18)
    # — because three surfaces restate one number and nothing ever
    # compared them. This closes the drift CHANNEL, not just the stale
    # instance: it reads this function's own docstring at runtime, via
    # the same `inspect` API already imported for control (t)'s
    # source-text census, and derives the expected total from the SAME
    # two live registries the floor above uses — never from a restated
    # literal — asserting BOTH factors (the doc-row count and the token
    # count), not only their product, are present together in the
    # docstring's own sentence shape, so a partial update that fixes one
    # number and not the other is still caught. Compared with whitespace
    # normalized on both sides (the docstring's own sentence wraps across
    # a line break at this exact point), matching the same idiom
    # `_RENDER_EXAMPLE_CLAIM_LITERAL`'s leg 5 containment check uses for a
    # hard-wrapped claim, rather than a line-scoped test that a wrap could
    # silently defeat.
    # DISCLOSED LIMITATION: this locks the count sentence's transcription
    # only, not the rest of this docstring's prose — the same bound
    # control (m) states for the doc rows themselves.
    render_m2_doc = inspect.getdoc(_selftest_render_contract) or ""
    render_m2_doc_normalized = " ".join(render_m2_doc.split())
    render_m2_expected_sentence = (
        f"derives the expected {qual01_negative_case_count} "
        f"({len(_QUAL01_DOC_ROWS)} doc rows x "
        f"{len(_QUAL01_DOC_ROW_TOKENS)} tokens)"
    )
    if render_m2_expected_sentence not in render_m2_doc_normalized:
        render_m2_found_match = re.search(
            r"derives the expected \d+ \(\d+ doc rows x \d+ tokens\)",
            render_m2_doc_normalized,
        )
        render_m2_found = (
            render_m2_found_match.group(0)
            if render_m2_found_match
            else "<no matching sentence found in the docstring at all>"
        )
        _fail(
            f"(m2) DOCSTRING COUNT LOCK: the docstring's transcription "
            f"reads {render_m2_found!r} but the live registries derive "
            f"{render_m2_expected_sentence!r} — the NEGATIVE-CASE COUNT "
            f"FLOOR sentence has drifted from the value the code actually "
            f"derives"
        )

    # (n) ISOLATION, unregistered surface. Plan 11-07's first fail-closed
    #     branch: a `_RenderSurfaceRead` whose relpath is a sentinel that
    #     is NOT a key of `_RENDER_SURFACE_REQUIRED_RULES` (a real
    #     registered surface's text is reused, only the relpath is fake)
    #     must produce a problem naming that relpath and the "no declared
    #     rule set" phrase. An empty result here means the branch is not
    #     load-bearing.
    sentinel_relpath = "shared/spine/references/NOT-A-REGISTERED-SURFACE.md"
    if sentinel_relpath in _RENDER_SURFACE_REQUIRED_RULES:
        _fail(
            "(n) ISOLATION setup: sentinel relpath collides with a real "
            "registered surface — pick a different sentinel"
        )
    elif render_reads:
        unregistered_read = _RenderSurfaceRead(
            relpath=sentinel_relpath, text=render_reads[0].text
        )
        unregistered_problems = _render_rule_report(unregistered_read)
        if not any(
            sentinel_relpath in p and "no declared rule set" in p
            for p in unregistered_problems
        ):
            _fail(
                "(n) ISOLATION unregistered-surface: the unregistered-"
                "surface branch did not fire — "
                f"{unregistered_problems!r}"
            )

    # (o) ISOLATION, unknown key. Plan 11-07's second fail-closed branch:
    #     drive `_render_required_rule_problems` directly with a COPIED
    #     required-rules mapping — never editing `_RENDER_RULE_LITERALS`
    #     or `_RENDER_SURFACE_REQUIRED_RULES` in place — whose sole entry
    #     for a real surface names a key that is not in
    #     `_RENDER_RULE_LITERALS`. The public signature of
    #     `_render_rule_report`, `(_RenderSurfaceRead) -> list[str]`, is
    #     untouched; only the extracted helper takes the injected mapping.
    if render_reads:
        real_relpath = render_reads[0].relpath
        unknown_key_rules = {real_relpath: ("R-DOES-NOT-EXIST",)}
        unknown_key_problems = _render_required_rule_problems(
            real_relpath, render_reads[0].text, required_rules=unknown_key_rules
        )
        if not any(
            real_relpath in p and "R-DOES-NOT-EXIST" in p
            for p in unknown_key_problems
        ):
            _fail(
                "(o) ISOLATION unknown-key: the unknown-required-key "
                "branch did not fire — "
                f"{unknown_key_problems!r}"
            )

    # (cf) CHAIN-FORM SURFACE SWEEP (plan 13-24, CR-04
    #     `13-VERIFICATION-round6.md` gap 3): reads the live tree through
    #     `_RENDER_CHAIN_FORM_GLOB` and derives its candidate surface set
    #     from what the tree actually states, rather than trusting
    #     `_RENDER_RULE_SURFACES` — the hand-maintained list that failed
    #     to catch `estimate-detail.md` and `theoretical-limit-detail.md`
    #     stating the chain form as a template one round after
    #     `reason-upward.md` was fixed for the identical defect (CR-03,
    #     plan 13-20). Reads canonical `shared/` bytes only, matching
    #     `_RENDER_EXAMPLE_GLOB`'s source-of-truth discipline.
    render_cf_texts: dict[str, str] = {}
    render_cf_read_problems: list[str] = []
    for render_cf_path in sorted(REPO_ROOT.glob(_RENDER_CHAIN_FORM_GLOB)):
        render_cf_relpath = render_cf_path.relative_to(REPO_ROOT).as_posix()
        render_cf_text, render_cf_read_problem = _read_text_or_problem(
            render_cf_path, render_cf_relpath
        )
        if render_cf_read_problem is not None:
            render_cf_read_problems.append(render_cf_read_problem)
            continue
        render_cf_texts[render_cf_relpath] = render_cf_text  # type: ignore[assignment]
    for render_cf_read_problem in render_cf_read_problems:
        _fail(f"(cf) CHAIN-FORM SURFACE SWEEP READ: {render_cf_read_problem}")

    # EQUALITY FLOOR (CR-03/WR-04 shape via `_render_coverage_floor_problems`):
    # the derived candidate set must equal the registered surfaces plus
    # every written exemption — equality, not subset, so a signature
    # narrowed until it matches only the registered surfaces fails by
    # name rather than passing silently (the same shape the chain-family
    # coverage floor and the dispatch-reachability floor already pay for
    # above).
    render_cf_candidates = frozenset(
        relpath
        for relpath, text in render_cf_texts.items()
        if _RENDER_CHAIN_FORM_SIGNATURE.search(" ".join(text.split()))
    )
    render_cf_required = frozenset(_RENDER_RULE_SURFACES) | {
        relpath for relpath, _reason in _RENDER_CHAIN_FORM_EXEMPT
    }
    for render_cf_problem in _render_coverage_floor_problems(
        (
            (
                "(cf) chain-form candidate set",
                render_cf_candidates,
                render_cf_required,
            ),
        )
    ):
        _fail(f"(cf) CHAIN-FORM SURFACE SWEEP EQUALITY: {render_cf_problem}")

    # THE SWEEP ITSELF — the unmodified helper, called on the live tree.
    for render_cf_problem in _render_chain_form_surface_problems(
        render_cf_texts,
        _RENDER_CHAIN_FORM_SIGNATURE,
        frozenset(_RENDER_RULE_SURFACES),
        _RENDER_CHAIN_FORM_EXEMPT,
    ):
        _fail(f"(cf) CHAIN-FORM SURFACE SWEEP: {render_cf_problem}")

    # (cf-iso) ISOLATION, `_render_chain_form_surface_problems`'s own
    #     falsifiability. Every arm drives the helper with a SYNTHETIC
    #     signature and synthetic `texts` — never the real tree, never
    #     `_RENDER_CHAIN_FORM_SIGNATURE`. Each arm is neutralizable:
    #     reverting the helper's own fix makes exactly that arm fail.
    render_cf_synth_sig = re.compile(r"XSIG")

    # (i) a matching unregistered relpath yields exactly one problem
    #     naming it.
    render_cf_i = _render_chain_form_surface_problems(
        {"synthetic/unregistered.md": "before XSIG after"},
        render_cf_synth_sig,
        frozenset(),
        (),
    )
    if not (
        len(render_cf_i) == 1
        and "synthetic/unregistered.md" in render_cf_i[0]
    ):
        _fail(
            f"(cf-iso i) UNREGISTERED MATCH: expected exactly one problem "
            f"naming synthetic/unregistered.md, got {render_cf_i!r}"
        )

    # (ii) the same relpath in `registered` yields zero.
    render_cf_ii = _render_chain_form_surface_problems(
        {"synthetic/registered.md": "before XSIG after"},
        render_cf_synth_sig,
        frozenset({"synthetic/registered.md"}),
        (),
    )
    if render_cf_ii:
        _fail(
            f"(cf-iso ii) REGISTERED: expected zero problems, got "
            f"{render_cf_ii!r}"
        )

    # (iii) the same relpath in `exempt`, with a written reason, yields
    #     zero.
    render_cf_iii = _render_chain_form_surface_problems(
        {"synthetic/exempt.md": "before XSIG after"},
        render_cf_synth_sig,
        frozenset(),
        (("synthetic/exempt.md", "a written reason"),),
    )
    if render_cf_iii:
        _fail(
            f"(cf-iso iii) EXEMPT: expected zero problems, got "
            f"{render_cf_iii!r}"
        )

    # (iv) an empty candidate set yields the NON-VACUITY problem.
    render_cf_iv = _render_chain_form_surface_problems(
        {"synthetic/clean.md": "no signature here"},
        render_cf_synth_sig,
        frozenset(),
        (),
    )
    if not any("NON-VACUITY" in p for p in render_cf_iv):
        _fail(
            f"(cf-iso iv) NON-VACUITY: expected a NON-VACUITY problem, "
            f"got {render_cf_iv!r}"
        )

    # (v) an exempt entry with an EMPTY written reason yields a
    #     REASONLESS EXEMPTION problem naming it (Q3, `13-24-PLAN.md`
    #     task 3) — an exemption without a written reason must be caught
    #     regardless of whether the exempted relpath matches the
    #     signature at all.
    render_cf_v = _render_chain_form_surface_problems(
        {},
        render_cf_synth_sig,
        frozenset(),
        (("synthetic/reasonless.md", ""),),
    )
    if not any(
        "REASONLESS EXEMPTION" in p and "synthetic/reasonless.md" in p
        for p in render_cf_v
    ):
        _fail(
            f"(cf-iso v) REASONLESS EXEMPTION: expected a problem naming "
            f"synthetic/reasonless.md, got {render_cf_v!r}"
        )

    return ok


def _selftest_chain_detector_pin() -> bool:
    """Phase 13 (CHAINHEAD-07): the sha256 pin over
    `_chain_block_well_formed`'s source (`_chain_detector_pin_problems`,
    defined beside the frozen function) re-runs on every QUAL-01 self-test
    and fails on any byte change to that function, including whitespace.

    Four controls:

    (a) POSITIVE. The real, unmodified source hashes to the pinned value —
        the arm that goes red the moment anyone edits the frozen function.

    (b) NEGATIVE, anti-vacuity. The source the run actually read is
        perturbed in memory two ways — a comment line appended, and a line
        stripped from its middle — and each perturbation must produce
        exactly one problem. A pin that reported green on perturbed bytes
        would be vacuous; this is what proves it is not. Neither
        perturbation is ever written to disk or monkeypatched onto the
        module — the helper takes source as a parameter precisely so this
        control needs neither.

    (c) FORMULA CONTROL. The naive, un-stripped hash of the real source is
        NOT the pinned value, while the `.rstrip("\\n")` form IS — the arm
        that fails if a future reader "simplifies" the strip away, encoding
        this phase's highest-risk finding as a standing assertion rather
        than a comment.

    (d) MESSAGE CONTROL. The problem text produced by (b) carries all four
        load-bearing substrings D-10 specifies: the function name,
        `CONTRACT-06`, the written-amendment instruction, and the
        do-not-recompute instruction. A pin whose message degraded to a
        bare digest diff would still pass (a)-(c); this arm is why it
        cannot.
    """
    ok = True

    def _fail(msg: str) -> None:
        nonlocal ok
        print(f"self-test FAIL: chain_detector_pin {msg}", file=sys.stderr)
        ok = False

    real_source = _chain_detector_source()

    # (a) POSITIVE.
    positive_problems = _chain_detector_pin_problems(real_source)
    if positive_problems:
        _fail(
            "(a) POSITIVE: unmodified source reported problems: "
            f"{positive_problems!r}"
        )

    # (b) NEGATIVE, anti-vacuity: two independent perturbations, each must
    # produce exactly one problem.
    appended = real_source + "# perturbation appended by the self-test\n"
    appended_problems = _chain_detector_pin_problems(appended)
    if len(appended_problems) != 1:
        _fail(
            "(b) NEGATIVE anti-vacuity: appending a comment line did not "
            f"produce exactly one problem: {appended_problems!r}"
        )

    real_lines = real_source.splitlines(keepends=True)
    middle = len(real_lines) // 2
    stripped_lines = real_lines[:middle] + real_lines[middle + 1 :]
    stripped = "".join(stripped_lines)
    stripped_problems = _chain_detector_pin_problems(stripped)
    if len(stripped_problems) != 1:
        _fail(
            "(b) NEGATIVE anti-vacuity: stripping a middle line did not "
            f"produce exactly one problem: {stripped_problems!r}"
        )

    # (c) FORMULA CONTROL.
    naive_digest = "sha256:" + hashlib.sha256(
        real_source.encode("utf-8")
    ).hexdigest()
    stripped_digest = "sha256:" + hashlib.sha256(
        real_source.rstrip("\n").encode("utf-8")
    ).hexdigest()
    if naive_digest == _CHAIN_DETECTOR_PINNED_DIGEST:
        _fail(
            "(c) FORMULA CONTROL: the naive un-stripped digest unexpectedly "
            "equals the pinned value — the trailing-newline strip is no "
            "longer discriminating"
        )
    if stripped_digest != _CHAIN_DETECTOR_PINNED_DIGEST:
        _fail(
            "(c) FORMULA CONTROL: the .rstrip('\\n') digest does not equal "
            f"the pinned value: {stripped_digest!r} != "
            f"{_CHAIN_DETECTOR_PINNED_DIGEST!r}"
        )

    # (d) MESSAGE CONTROL.
    if appended_problems:
        message = appended_problems[0]
        required_substrings = (
            "_chain_block_well_formed",
            "CONTRACT-06",
            "amend the milestone goal in writing",
            "Do not recompute to make this pass",
        )
        missing = [s for s in required_substrings if s not in message]
        if missing:
            _fail(
                "(d) MESSAGE CONTROL: problem text is missing required "
                f"substring(s) {missing!r}: {message!r}"
            )

    return ok


def _selftest_selfaudit_calibration() -> bool:
    """The Self-Audit Gate's claimed bands are reconciled against measurement.

    Observed 2026-08-30: a live analysis scored itself **Criterion 4 —
    Rigorous** and **Gate: PASS** with 6 of 6 chains mechanically malformed.
    Nothing compared the two, so the disagreement was invisible.

    Controls (a)-(d) pin the disagreement firing per criterion. Controls
    (e)-(h) are the anti-overreach half: a correct self-report, a conceded
    band, a missing self-audit, and an unstated band must each produce NO
    finding. Without those, a check that simply always fired would pass the
    positives — honesty-not-score, D-01.
    """
    ok = True

    def _fail(msg: str) -> None:
        nonlocal ok
        print(f"self-test FAIL: selfaudit_calibration {msg}", file=sys.stderr)
        ok = False

    def _audit(**bands: str) -> str:
        names = {
            2: "Challenge Assumptions", 4: "Reason Upward",
            6: "Conclusion-to-Ground-Truth Traceability",
        }
        return "\n\n".join(
            f"**Criterion {n}: {names[n]}**\nQuoted span: *\"x\"*\n"
            f"Band: **{b}**\nJustification: y."
            for n, b in ((int(k[1:]), v) for k, v in bands.items()))

    clean = {"malformed_chain_blocks": 0, "untraced_claims": 0,
             "nonconforming_verdict_cells": 0, "_dependency_cycles": []}

    # (a) Criterion 4 Rigorous vs malformed chains — the observed case.
    d = _selfaudit_calibration_defects(
        _audit(c4="Rigorous"), {**clean, "malformed_chain_blocks": 6})
    if [x["criterion"] for x in d] != [4] or d[0]["measured"] != 6:
        _fail(f"(a) C4 Rigorous vs 6 malformed chains not reported: {d!r}")

    # (b) Criterion 6 Rigorous vs untraced claims.
    d = _selfaudit_calibration_defects(
        _audit(c6="Rigorous"), {**clean, "untraced_claims": 1})
    if [x["criterion"] for x in d] != [6]:
        _fail(f"(b) C6 Rigorous vs untraced claim not reported: {d!r}")

    # (c) Criterion 2 Rigorous vs non-conforming verdict cells.
    d = _selfaudit_calibration_defects(
        _audit(c2="Rigorous"), {**clean, "nonconforming_verdict_cells": 3})
    if [x["criterion"] for x in d] != [2]:
        _fail(f"(c) C2 Rigorous vs nonconforming verdicts not reported: {d!r}")

    # (d) Criterion 4 Rigorous vs a dependency cycle (GAP-6's defect).
    d = _selfaudit_calibration_defects(
        _audit(c4="Rigorous"), {**clean, "_dependency_cycles": ["c1", "c2"]})
    if not d or d[0]["contradicted_by"] != "_dependency_cycles":
        _fail(f"(d) C4 Rigorous vs dependency cycle not reported: {d!r}")

    # (e) ANTI-OVERREACH: a correct Rigorous claim on a clean record.
    if _selfaudit_calibration_defects(_audit(c2="Rigorous", c4="Rigorous",
                                             c6="Rigorous"), clean):
        _fail("(e) clean record with Rigorous claims spuriously reported")

    # (f) ANTI-OVERREACH: Sound alongside malformed chains is the CORRECT
    #     self-report under the Criterion 4 Sound band, not a disagreement.
    if _selfaudit_calibration_defects(
            _audit(c4="Sound"), {**clean, "malformed_chain_blocks": 6}):
        _fail("(f) conceded Sound band wrongly reported as a disagreement")

    # (g) ANTI-OVERREACH: no self-audit at all yields no finding — absence is
    #     a disclosure defect owned elsewhere, not silent agreement here.
    if _selfaudit_calibration_defects(
            "no verdict blocks here", {**clean, "malformed_chain_blocks": 6}):
        _fail("(g) missing self-audit wrongly produced a calibration finding")

    # (h) ANTI-OVERREACH: a criterion block with no Band line states no claim.
    noband = "**Criterion 4: Reason Upward**\nQuoted span: *\"x\"*\nJustification: y."
    if _selfaudit_calibration_defects(
            noband, {**clean, "malformed_chain_blocks": 6}):
        _fail("(h) unstated band wrongly scored as a Rigorous claim")

    return ok


def _selftest_ledger_traceability() -> bool:
    """A closure ledger discharges the claims it quotes, and its own rows
    are not counted as additional claims.

    Observed 2026-08-31 on a live PR-P1 run scored with this detector: an
    analysis that traced its Conclusion through an explicit "closure
    ledger" instead of inline parentheticals was penalised on BOTH halves
    of the signal — ten ledger rows mined as extra claims (7 -> 14) while
    the three claims they discharged stayed flagged untraced (0 -> 3) —
    and `selfaudit_calibration` then escalated that into a Criterion 6
    over-claim finding against an agent that had done nothing wrong.

    Controls (a)-(c) pin the fix. Controls (d)-(g) are the anti-overreach
    half: a ledger citing a chain that does not exist, a fragment too
    generic to identify a claim, and a fragment that quotes something else
    must each discharge NOTHING. Without them a rule that credited any
    ledger-shaped line would pass the positives — honesty-not-score, D-01.
    Control (h) discriminates the fence rule from the claim filter, and
    (i) pins the frozen corpus against movement.

    Plan 14-05 / D-04, D-10: (j) is QUAL-01's live leg over the committed
    `tests/quality-ledger-v8.26/PR-P1.md` fixture (a leg of this existing
    `--self-test`, never a new gate, CI job or CLI flag — the battery tally
    stays 23). It reads that fixture unconditionally, exactly as (i) already
    reads the frozen v8.7 corpus, and asserts its measured reading —
    `conclusion_claims == 7`, zero `_closure_ledger_fragments`,
    `untraced_claims == 1` — plus the IDENTITY of the single untraced claim
    (the `**Trade-offs acknowledged:**` paragraph), not just its count: a
    count catches a later loosening that silently discharges the claim
    (LEDGER-04's own words); the identity survives if a count ever
    legitimately moves. Three anti-vacuity mutation arms, one per pinned
    number, each mutate the text the run actually read (never a re-read of
    the file) and require the specific predicted change, so a leg that
    reads the fixture but cannot fail on it does not ship (T-14-14).
    DISCLOSED BOUNDS: (j) asserts a `detect_defects` reading over one
    committed analysis; it does not assert the analysis is correct, does
    not measure whether the agent complies with R11 or R12 at emission time
    (that needs a live run — 999.12/999.13), and does not assert a
    Criterion 6 band, which is assigned by a model and which no gate in
    this tree checks (D-10).

    Plan 14-01 / D-11: (i) compares PER ANALYSIS, not just vector-to-vector
    — a mismatch names the analysis, the field and both values — behind a
    LENGTH FLOOR that fails rather than vacuously passing if any of the
    three calibration vectors is emptied or resized. This is the mechanical
    proof that D-02 (`_slice_sections`) and D-03
    (`_closure_ledger_fragments`) left the v8.7 baseline (HARNESS-01)
    unmoved. Disclosed bound: (i) pins `conclusion_claims` and
    `untraced_claims` only, never `_closure_ledger_fragments` (D-03
    deliberately drives this to zero across the corpus) or any other
    `detect_defects` field.
    """
    ok = True

    def _fail(msg: str) -> None:
        nonlocal ok
        print(f"self-test FAIL: ledger_traceability {msg}", file=sys.stderr)
        ok = False

    chain_ids = ["Chain C1", "Chain C2", "Chain C3"]
    prose = (
        "**Recommended approach:** Do not start with Lambda. Measure bill "
        "composition and duty cycle first, then purchase Compute Savings "
        "Plan coverage sized to the post-cleanup baseline.\n\n"
        "**Key insight:** Lambda's advantage is not that it is cheap - it is "
        "2.10 times more expensive per unit of actual compute than Fargate. "
        "Its advantage is that it bills nothing for idle.\n\n"
        "**Trade-offs acknowledged:** A Savings Plan commits you to an hourly "
        "floor for three years and is not reversible, so cleanup moves ahead "
        "of sizing it.\n"
    )
    rows = "\n".join(
        (
            '- "Do not start with Lambda; measure bill composition and duty '
            'cycle first" -> chain C1',
            '- "Lambda is 2.10 times more expensive per unit of actual '
            'compute than Fargate" -> chain C2',
            '- "A Savings Plan commits you to an hourly floor for three '
            'years" -> chain C3',
        )
    ) + "\n"
    ledgered = prose + "\n## Closure ledger\n\n" + '```' + "text\n" + rows + '```' + "\n"

    # (a) POSITIVE: every prose claim is discharged by the ledger.
    claims = _conclusion_claims(ledgered, chain_ids)
    frags = _closure_ledger_fragments(ledgered, chain_ids)
    untraced = [c for c in claims if not _claim_is_traced(c, chain_ids, [], frags)]
    if untraced:
        _fail(f"(a) ledgered claims still reported untraced: {untraced!r}")

    # (b) DENOMINATOR: the ledger's own rows are not extra claims.
    if len(claims) != 3:
        _fail(f"(b) expected 3 prose claims, got {len(claims)}: {claims!r}")

    # (c) FAULT INJECTION: strip the ledger and the same three claims must
    #     go back to untraced — proving (a) is the ledger's doing and not a
    #     weakened claim extractor.
    bare_claims = _conclusion_claims(prose, chain_ids)
    bare_untraced = [
        c for c in bare_claims
        if not _claim_is_traced(c, chain_ids, [], _closure_ledger_fragments(prose, chain_ids))
    ]
    if len(bare_untraced) != 3:
        _fail(f"(c) ledger-free section did not report 3 untraced: {bare_untraced!r}")

    # (d) ANTI-OVERREACH: a ledger citing a chain absent from section 4 has
    #     no authority to discharge anything.
    bogus = prose + "\n" + '```' + "text\n" + rows.replace("C1", "C9").replace(
        "C2", "C8").replace("C3", "C7") + '```' + "\n"
    if _closure_ledger_fragments(bogus, chain_ids):
        _fail("(d) ledger citing non-existent chains yielded fragments")

    # (e) ANTI-OVERREACH: a fragment below the minimum size identifies no
    #     particular claim and must not discharge one.
    generic_claim = (
        "**Key insight:** The convention that serverless is cheaper does not "
        "survive contact with the duty cycle."
    )
    generic_frags = _closure_ledger_fragments(
        '- "serverless is cheaper" -> chain C1\n', chain_ids)
    if not generic_frags:
        _fail("(e) precondition: generic ledger line yielded no fragment to reject")
    elif _claim_is_traced(generic_claim, chain_ids, [], generic_frags):
        _fail("(e) sub-minimum fragment wrongly discharged a claim")

    # (f) ANTI-OVERREACH: a well-formed ledger entry quoting SOMETHING ELSE
    #     discharges nothing.
    other_frags = _closure_ledger_fragments(
        '- "the migration raises network and observability lines" -> chain C1\n',
        chain_ids)
    savings_claim = [c for c in claims if "Savings Plan commits" in c]
    if not (other_frags and savings_claim):
        _fail("(f) precondition: unrelated-fragment control not constructed")
    elif _claim_is_traced(savings_claim[0], chain_ids, [], other_frags):
        _fail("(f) unrelated fragment wrongly discharged a claim")

    # (g) ANTI-OVERREACH: coverage is measured over the FRAGMENT, so a long
    #     claim cannot absorb a short quote it never made.
    if _ledger_fragment_covers("alpha beta gamma delta epsilon zeta",
                               " ".join(["padding"] * 400)):
        _fail("(g) coverage credited a claim that contains none of the fragment")

    # (h) The fence rule, not `_is_assertive_claim`, is what excludes the
    #     ledger rows: unfenced, the same rows ARE claims (each self-cited).
    unfenced = prose + "\n## Closure ledger\n\n" + rows
    if len(_conclusion_claims(unfenced, chain_ids)) != 6:
        _fail("(h) unfenced ledger rows were excluded by something other "
              "than the fence rule")

    # (i) The frozen calibration corpus does not move. The saturated
    #     `_CALIBRATION_UNTRACED_FLAGS` cannot see this axis at all.
    #
    #     Plan 14-01 / D-11 (2026-09-03): this control is the mechanical
    #     assertion that D-02 (`_slice_sections`' section-6 boundary) and
    #     D-03 (`_closure_ledger_fragments`' structural narrowing) did not
    #     move the v8.7 baseline this detector protects (HARNESS-01,
    #     docs/v8.7-quality-baseline-freeze.md). It was rewritten from a
    #     whole-vector comparison to compare PER ANALYSIS, so a future
    #     change to `_slice_sections`, `_closure_ledger_fragments`,
    #     `_conclusion_claims` or `_claim_is_traced` that moves the record
    #     fails naming the analysis, the field, the measured value and the
    #     pinned value — not just "the vectors differ".
    #
    #     A LENGTH FLOOR runs first: without it, emptying
    #     `_CALIBRATION_ANALYSIS_ORDER` makes the per-analysis loop below
    #     run zero times and pass vacuously. The whole-vector comparison is
    #     kept alongside the per-analysis loop — it is what catches a
    #     length/order change that a per-element loop over a shortened list
    #     would silently skip.
    #
    #     DISCLOSED BOUND: this control pins `conclusion_claims` and
    #     `untraced_claims` only. It does not pin `_closure_ledger_fragments`
    #     (D-03 deliberately drives this to zero across the corpus — see
    #     the LEDGER-01 comment block above `_closure_ledger_fragments`),
    #     and it does not observe any other `detect_defects` field.
    base = REPO_ROOT / "tests" / "quality-baseline-v8.7" / "analyses"

    lengths = {
        "_CALIBRATION_ANALYSIS_ORDER": len(_CALIBRATION_ANALYSIS_ORDER),
        "_CALIBRATION_CONCLUSION_CLAIMS": len(_CALIBRATION_CONCLUSION_CLAIMS),
        "_CALIBRATION_UNTRACED_CLAIMS": len(_CALIBRATION_UNTRACED_CLAIMS),
    }
    if len(set(lengths.values())) != 1 or lengths["_CALIBRATION_ANALYSIS_ORDER"] != 6:
        _fail(f"(i) LENGTH FLOOR: calibration vectors are not all length 6: "
              f"{lengths!r}")
    else:
        measured_claims, measured_untraced = [], []
        for name in _CALIBRATION_ANALYSIS_ORDER:
            rec = detect_defects((base / f"{name}.md").read_text(encoding="utf-8"), name)
            measured_claims.append(rec["conclusion_claims"])
            measured_untraced.append(rec["untraced_claims"])

        if measured_claims != _CALIBRATION_CONCLUSION_CLAIMS:
            _fail(f"(i) conclusion_claims moved: {measured_claims} != "
                  f"{_CALIBRATION_CONCLUSION_CLAIMS}")
        if measured_untraced != _CALIBRATION_UNTRACED_CLAIMS:
            _fail(f"(i) untraced_claims moved: {measured_untraced} != "
                  f"{_CALIBRATION_UNTRACED_CLAIMS}")

        for name, m_claims, p_claims, m_untraced, p_untraced in zip(
            _CALIBRATION_ANALYSIS_ORDER, measured_claims,
            _CALIBRATION_CONCLUSION_CLAIMS, measured_untraced,
            _CALIBRATION_UNTRACED_CLAIMS,
        ):
            if m_claims != p_claims:
                _fail(f"(i) {name}: conclusion_claims moved: "
                      f"measured {m_claims} != pinned {p_claims}")
            if m_untraced != p_untraced:
                _fail(f"(i) {name}: untraced_claims moved: "
                      f"measured {m_untraced} != pinned {p_untraced}")

    # (j) THE LIVE LEG (D-04, plan 14-05): a committed, tracked fixture the
    #     v8.7 corpus cannot substitute for — see
    #     tests/quality-ledger-v8.26/README.md — asserts its own measured
    #     reading. `.planning/captures/` (the fixture's own source) is
    #     gitignored and unreachable by any gate; this is why the fixture
    #     was copied into `tests/` at all.
    ledger_fixture_path = REPO_ROOT / "tests" / "quality-ledger-v8.26" / "PR-P1.md"
    ledger_fixture_text = ledger_fixture_path.read_text(encoding="utf-8")
    fixture_rec = detect_defects(ledger_fixture_text, "PR-P1-ledger-v8.26")

    if fixture_rec["conclusion_claims"] != 7:
        _fail(f"(j) conclusion_claims: measured "
              f"{fixture_rec['conclusion_claims']} != pinned 7")
    if len(fixture_rec["_closure_ledger_fragments"]) != 0:
        _fail(f"(j) closure_ledger_fragments: measured "
              f"{len(fixture_rec['_closure_ledger_fragments'])} != pinned 0")
    if fixture_rec["untraced_claims"] != 1:
        _fail(f"(j) untraced_claims: measured "
              f"{fixture_rec['untraced_claims']} != pinned 1")

    # IDENTITY, not just count (D-10): a count can move for an innocent
    # reason (a legitimate emission change); the identity of the untraced
    # claim is what proves it is still the SAME residual, not a different
    # one that happens to share a count.
    untraced_text = fixture_rec["_untraced_claims_text"]
    expected_prefix = (
        "**Trade-offs acknowledged:** step 2's ~73% is a ceiling requiring "
        "a long-term, all-upfront commitment"
    )
    if len(untraced_text) != 1 or not untraced_text[0].startswith(expected_prefix):
        _fail(f"(j) untraced claim identity moved: {untraced_text!r} does "
              f"not start with {expected_prefix!r}")

    # ANTI-VACUITY (T-14-14): one mutation arm per pinned number, each
    # derived from `ledger_fixture_text` — the bytes this control actually
    # read — and applied in memory only. A live leg that reads a fixture
    # but cannot fail on it is worse than no leg at all.
    if len(untraced_text) == 1:
        trade_offs_line = untraced_text[0]

        # Arm 1 (untraced axis): citing a real chain inline must discharge
        # the claim.
        mutated_1 = ledger_fixture_text.replace(
            trade_offs_line, trade_offs_line + " (chain C5).", 1
        )
        if mutated_1 == ledger_fixture_text:
            _fail("(j) arm 1 precondition: trade-offs line not found in "
                  "the fixture text for mutation")
        else:
            rec_1 = detect_defects(mutated_1, "PR-P1-ledger-v8.26-arm1")
            if rec_1["untraced_claims"] != 0:
                _fail(f"(j) arm 1 ANTI-VACUITY: appending an inline chain "
                      f"C5 citation to the trade-offs claim did not "
                      f"discharge it — untraced_claims measured "
                      f"{rec_1['untraced_claims']}, expected 0; the "
                      f"untraced-axis assertion is passing vacuously")

        # Arm 3 (ledger axis): a structural ledger row inside section 6,
        # quoting a span of the trade-offs claim and naming a real chain id
        # from section 4, must produce a fragment AND discharge the claim.
        # Derived from the same `trade_offs_line` so the quoted span is
        # guaranteed to be a real substring of the claim it discharges.
        quoted_span = trade_offs_line[
            len("**Trade-offs acknowledged:** "):
        ].split(";", 1)[0]
        ledger_row = f'```text\n- "{quoted_span}" -> chain C5\n```\n\n'
        mutated_3 = ledger_fixture_text.replace(
            trade_offs_line, ledger_row + trade_offs_line, 1
        )
        if mutated_3 == ledger_fixture_text:
            _fail("(j) arm 3 precondition: trade-offs line not found in "
                  "the fixture text for mutation")
        else:
            rec_3 = detect_defects(mutated_3, "PR-P1-ledger-v8.26-arm3")
            if not rec_3["_closure_ledger_fragments"]:
                _fail("(j) arm 3 ANTI-VACUITY: inserting a structural "
                      "ledger row inside section 6 yielded zero "
                      "closure-ledger fragments; the ledger-axis assertion "
                      "is passing vacuously")
            elif rec_3["untraced_claims"] != 0:
                _fail(f"(j) arm 3 ANTI-VACUITY: the inserted ledger row's "
                      f"fragment did not discharge the trade-offs claim — "
                      f"untraced_claims measured {rec_3['untraced_claims']}, "
                      f"expected 0; the ledger-axis assertion is passing "
                      f"vacuously")
    else:
        _fail("(j) arm 1/3 precondition: expected exactly one untraced "
              "claim to derive the mutation from")

    # Arm 2 (claims axis): deleting the Key Insight claim must drop
    # conclusion_claims by exactly one. Derived from `_claims_text` itself
    # (never hand-transcribed) so the mutation is guaranteed to match the
    # bytes the control actually read.
    key_insight_claims = [
        c for c in fixture_rec["_claims_text"] if c.startswith("**Key insight")
    ]
    if len(key_insight_claims) != 1:
        _fail(f"(j) arm 2 precondition: expected exactly one Key Insight "
              f"claim to mutate, found {len(key_insight_claims)}")
    else:
        key_insight_line = key_insight_claims[0]
        mutated_2 = ledger_fixture_text.replace(key_insight_line + "\n\n", "", 1)
        if mutated_2 == ledger_fixture_text:
            _fail("(j) arm 2 precondition: Key Insight line deletion "
                  "produced no change to the fixture text")
        else:
            rec_2 = detect_defects(mutated_2, "PR-P1-ledger-v8.26-arm2")
            if rec_2["conclusion_claims"] != 6:
                _fail(f"(j) arm 2 ANTI-VACUITY: deleting the Key Insight "
                      f"claim did not drop conclusion_claims to 6 — "
                      f"measured {rec_2['conclusion_claims']}; the "
                      f"claims-axis assertion is passing vacuously")


    # Arms 4-5 (BOUNDARY REGRESSIONS, CR-01/CR-02): the two defects the
    # phase-14 review found in the D-02 slicer fix. Both were live-
    # reproduced against THIS fixture before being fixed, and both are
    # invisible to arms 1-3 and to control (i) — the frozen v8.7 corpus
    # carries no heading inside section 6 at all, so no analysis in it
    # exercises either shape. They are pinned here, on the bytes the
    # control actually read, because a boundary defect that only review can
    # see is exactly the failure mode this gate exists to prevent.
    #
    # Both arms assert INVARIANCE, not a moved number: the reading must be
    # the same 7/0/1 the fixture pins above. Pre-fix, arm 4 measured 8
    # claims (the 8th being `**Residual disclosed:**`, a Self-Audit Gate
    # line the deeper heading failed to fence off) and arm 5 measured
    # 0/0/0 — a silent false-clean, worse than a wrong count.
    baseline_reading = (
        fixture_rec["conclusion_claims"],
        len(fixture_rec["_closure_ledger_fragments"]),
        fixture_rec["untraced_claims"],
    )

    # Arm 4 (CR-01, appendix depth): deepening the fixture's own appendix
    # headings past `###` must not change what section 6 contains. The
    # headings are located by pattern rather than transcribed, so the arm
    # follows the fixture if its appendix is ever retitled.
    section6_at = ledger_fixture_text.find("# 6. Conclusion")
    if section6_at < 0:
        _fail("(j) arm 4 precondition: section 6 heading not found in the "
              "fixture text")
    else:
        # Every depth 1-6, not just 4. Flooring depth 4 alone left
        # `#{1,4}`, `#{2,6}` and `#{2,4}` all passing while both doc rows
        # published "depth 1-6" — the arm was narrower than the claim it
        # was supposed to back.
        #
        # SCOPE, measured: with the Self-Audit Gate cap in `_slice_sections`
        # in place, this arm no longer DISCRIMINATES the depth bound on this
        # fixture — the cap rescues the reading, so narrowing the pattern
        # leaves this arm silent. Arm 11 is what floors the depth bound, on
        # synthetic documents carrying no Gate. What this arm still asserts
        # is end-to-end invariance of the shipped reading, which is real but
        # weaker than it looks. The distinction is stated here because a
        # safety net that masks the defect it catches is exactly how a
        # control becomes vacuous without anyone noticing. Three leading spaces are covered too:
        # CommonMark permits up to three before an ATX marker, and the
        # fence test one statement away strips whitespace while the
        # heading test does not, so the two disagreed until `{0,3}` was
        # added to `_APPENDIX_HEADING_RE`.
        # The precondition is loop-invariant, so it is checked ONCE here
        # rather than inside the sweep, where a `break` left the outer loop
        # running and reported one structural failure six times.
        if re.search(r"(?m)^##(?=[ \t]+\S)", ledger_fixture_text[section6_at:]) is None:
            _fail("(j) arm 4 precondition: no `##` appendix heading found "
                  "after section 6 to rewrite")
        else:
          for depth in range(1, 7):
            for indent in ("", "   "):
                deepened, n_deepened = re.subn(
                    r"(?m)^##(?=[ \t]+\S)",
                    indent + "#" * depth,
                    ledger_fixture_text[section6_at:],
                )
                mutated_4 = ledger_fixture_text[:section6_at] + deepened
                rec_4 = detect_defects(
                    mutated_4, f"PR-P1-ledger-v8.26-arm4-d{depth}i{len(indent)}"
                )
                reading_4 = (
                    rec_4["conclusion_claims"],
                    len(rec_4["_closure_ledger_fragments"]),
                    rec_4["untraced_claims"],
                )
                if reading_4 != baseline_reading:
                    _fail(f"(j) arm 4 BOUNDARY REGRESSION (CR-01): rewriting "
                          f"{n_deepened} appendix heading(s) to depth "
                          f"{depth} with {len(indent)} leading space(s) "
                          f"moved the reading to {reading_4} from "
                          f"{baseline_reading}; section 6 must stop at an "
                          f"appendix heading of ANY depth CommonMark "
                          f"recognises, which is what both `| QUAL-01 |` "
                          f"doc rows publish")

    # Arm 5 (CR-02, fenced pseudo-heading): a `#`-shaped line inside a
    # fenced block is verbatim content, not an appendix boundary. This is
    # reachable through the shape R4 recommends — a heading-introduced
    # closure ledger rendered inside a fence.
    if section6_at >= 0:
        s6_line_end = ledger_fixture_text.find("\n", section6_at)
        if s6_line_end < 0:
            _fail("(j) arm 5 precondition: section 6 heading is not "
                  "newline-terminated")
        else:
            mutated_5 = (
                ledger_fixture_text[: s6_line_end + 1]
                + "\n```text\n## §6→§4 closure ledger\n```\n"
                + ledger_fixture_text[s6_line_end + 1 :]
            )
            # No `mutated_5 == ledger_fixture_text` precondition here: a
            # pure insertion cannot equal the original, so that branch was
            # unreachable and its `_fail` could never fire.
            if True:  # noqa: SIM103 - kept to preserve the block's indentation
                rec_5 = detect_defects(mutated_5, "PR-P1-ledger-v8.26-arm5")
                reading_5 = (
                    rec_5["conclusion_claims"],
                    len(rec_5["_closure_ledger_fragments"]),
                    rec_5["untraced_claims"],
                )
                if reading_5 != baseline_reading:
                    _fail(f"(j) arm 5 BOUNDARY REGRESSION (CR-02): a fenced "
                          f"`## ...` line inside section 6 moved the reading "
                          f"to {reading_5} from {baseline_reading}; a "
                          f"pseudo-heading inside a fence is verbatim "
                          f"content, never a section boundary. A reading of "
                          f"(0, 0, 0) here is the false-clean this arm "
                          f"exists to catch.")

    # Arms 10-11 (DIRECT BOUNDARY ARMS). The Gate cap above is a safety
    # net, and a safety net MASKS the thing it catches: with the cap in
    # place, narrowing the heading-depth bound or breaking the CommonMark
    # closing rules no longer changes the fixture's reading at all, because
    # the cap rescues it. Measured — every such mutation left arms 4-9
    # silent. Arms 4-9 therefore prove the pipeline's OUTCOME; these two
    # prove the boundary logic itself, on synthetic documents that carry no
    # Self-Audit Gate, so nothing can mask a defect.
    def _synthetic(section6_body: str) -> str:
        head = "".join(
            f"# {n}. {name.title()}\n\nbody {n}\n\n"
            for n, name in sorted(_SECTION_NAMES.items()) if n != 6
        )
        return head + "# 6. Conclusion\n\n" + section6_body

    # Arm 10: `_fenced_code_flags` implements CommonMark's closing rules,
    # not a parity toggle. Each case names the rule it pins.
    flag_cases: tuple[tuple[str, str, tuple[bool, ...]], ...] = (
        ("plain fence", "```\nx\n```\nout",
         (True, True, True, False)),
        ("``` cannot close ~~~", "~~~\n```\nstill inside\n~~~\nout",
         (True, True, True, True, False)),
        ("closer must be >= opener", "````\n```\ninside\n````\nout",
         (True, True, True, True, False)),
        ("closer carries no info string", "```\n``` js\ninside\n```\nout",
         (True, True, True, True, False)),
        ("backtick info bars the opener", "``` a`b\nnot a fence\n",
         (False, False, False)),
        ("unterminated runs to end", "```\na\nb",
         (True, True, True)),
    )
    for label, body, expected_flags in flag_cases:
        measured = tuple(_fenced_code_flags(body.split("\n")))
        if measured != expected_flags:
            _fail(f"(j) arm 10 FENCE SEMANTICS [{label}]: "
                  f"_fenced_code_flags returned {measured}, expected "
                  f"{expected_flags}; a parity toggle passes several of "
                  f"these and is wrong on all of them")

    # Arm 11: section 6's boundary on documents with NO Self-Audit Gate, so
    # the cap cannot mask a wrong answer. `hidden` means the appendix
    # heading must NOT end section 6; `boundary` means it must.
    boundary_cases: tuple[tuple[str, str, bool], ...] = tuple(
        [(f"depth {d} appendix heading", "keep\n\n" + "#" * d + " Appendix\n\nappendix\n", True)
         for d in range(1, 7)]
        + [("3-space indented heading", "keep\n\n   ## Appendix\n\nappendix\n", True),
           ("4-space indent is code, not a heading", "keep\n\n    ## Appendix\n\nmore\n", False),
           ("heading inside a fence", "keep\n\n```\n## Appendix\n```\n\nmore\n", False),
           ("two headings inside one fence", "keep\n\n```\n## A\n## B\n```\n\nmore\n", False),
           ("heading inside a ~~~ quoting ```", "keep\n\n~~~\n## A\n```\n~~~\n\nmore\n", False)]
    )
    for label, body, expect_boundary in boundary_cases:
        try:
            measured_s6 = _slice_sections(_synthetic(body))[6]
        except SectionResolutionError as exc:  # pragma: no cover - guard
            _fail(f"(j) arm 11 precondition [{label}]: synthetic document "
                  f"did not resolve: {exc}")
            continue
        ended_early = "appendix" not in measured_s6 and "more" not in measured_s6
        if ended_early != expect_boundary:
            _fail(f"(j) arm 11 BOUNDARY [{label}]: section 6 "
                  f"{'ended at' if ended_early else 'ran past'} the heading, "
                  f"expected it to {'end at' if expect_boundary else 'run past'} "
                  f"it. Sliced body: {measured_s6!r}")

    # Arms 6-9 (FENCE SHAPE BATTERY). Every entry is a shape that a
    # previous cut of this boundary logic got WRONG, each found by review
    # rather than by any gate. They are table-driven so a newly discovered
    # shape is one row, not another bespoke arm.
    #
    #   arm 6  a balanced fence opening in section 6 and closing after the
    #          appendix headings. Parity tracking hid both headings, section
    #          6 absorbed the Self-Audit Gate, and `**Residual disclosed:**`
    #          came back as an 8th claim — the D-02 defect restored by its
    #          own fix. The Gate cap is what closes it.
    #   arm 7  a fenced block holding TWO heading-shaped lines — an ordinary
    #          bash snippet with two `# ` comments is enough. The
    #          "hidden only if the fence closes before the next heading"
    #          rule made the second one the next heading, hid nothing, and
    #          collapsed the reading to 0/0/0.
    #   arm 8  a `~~~` block quoting an UNCLOSED ``` example. Legal
    #          CommonMark; a parity toggle inverted on it and read the whole
    #          remainder of the section as code, returning zero claims.
    #   arm 9  the disclosed bound, pinned rather than left to be
    #          rediscovered: an unterminated fence at the top of section 6
    #          reads as code to end of document, so the section returns
    #          nothing. Measured identical at 4d3b5ca, at e1459ac and here —
    #          long-standing behaviour, not introduced by this phase, and
    #          the conservative direction (too short, never absorbing the
    #          Gate). It is asserted as 0/0/0 so that a change to it must be
    #          deliberate.
    s6_body_at = ledger_fixture_text.find("\n", section6_at) + 1 if section6_at >= 0 else -1
    first_appendix = ledger_fixture_text.find("\n## ", section6_at) if section6_at >= 0 else -1
    last_appendix = ledger_fixture_text.rfind("\n## ")
    if s6_body_at <= 0 or first_appendix < 0 or last_appendix <= first_appendix:
        _fail("(j) arms 6-9 precondition: could not locate section 6's body "
              "and two following `## ` appendix headings in the fixture")
    else:
        heading_end = ledger_fixture_text.find("\n", last_appendix + 1)
        spanning = (
            ledger_fixture_text[:first_appendix]
            + "\n\n```text\nfence opens before the appendix headings\n"
            + ledger_fixture_text[first_appendix:heading_end]
            + "\n```\n"
            + ledger_fixture_text[heading_end:]
        )
        def _insert_into_s6(block: str) -> str:
            return (
                ledger_fixture_text[:s6_body_at] + block
                + ledger_fixture_text[s6_body_at:]
            )
        fence_shapes: tuple[tuple[str, str, str, tuple[int, int, int]], ...] = (
            ("arm 6", "fence spanning the appendix headings",
             spanning, baseline_reading),
            ("arm 7", "fenced block holding two heading-shaped lines",
             _insert_into_s6("\n```bash\n# step one\n# step two\nls\n```\n"),
             baseline_reading),
            ("arm 8", "`~~~` block quoting an unclosed ``` example",
             _insert_into_s6("\n~~~text\n## x\n```python\nnever closed\n~~~\n"),
             baseline_reading),
            ("arm 9", "unterminated fence at the top of section 6 "
                      "(DISCLOSED BOUND: reads as code to end of document)",
             _insert_into_s6("\n```text\nnever closed\n"),
             (0, 0, 0)),
        )
        for arm, description, mutated, expected in fence_shapes:
            if mutated == ledger_fixture_text:
                _fail(f"(j) {arm} precondition: {description} produced no "
                      f"change to the fixture text")
                continue
            rec_f = detect_defects(mutated, f"PR-P1-ledger-v8.26-{arm.replace(' ', '')}")
            reading_f = (
                rec_f["conclusion_claims"],
                len(rec_f["_closure_ledger_fragments"]),
                rec_f["untraced_claims"],
            )
            absorbed = [
                c for c in rec_f["_claims_text"]
                if c.startswith("**Residual disclosed:")
            ]
            if reading_f != expected or absorbed:
                _fail(f"(j) {arm} FENCE SHAPE: {description} read "
                      f"{reading_f}, expected {expected}"
                      + (f"; and pulled {len(absorbed)} Self-Audit Gate "
                         f"line(s) in as section-6 claim(s): {absorbed!r}"
                         if absorbed else "")
                      + ". Section 6 must never absorb the Gate that "
                        "grades it, and a legitimate fenced block must "
                        "never truncate it.")

    return ok


def _selftest_incidence_schema_compat() -> bool:
    """`read_defect_incidence` maps by header name, so widening the schema
    does not orphan the files already committed.

    Three columns were appended to `_DEFECT_RECORD_FIELDS` at the v8.18
    widening (`dependency_cycles`, `ungrounded_chains`,
    `selfaudit_disagreements`) so that findings previously visible only to
    an importing caller reach the emitted TSV. Nine more were appended for
    PROV-05 (D-11): `provenance_labels`, `unmatched_sources`,
    `unreadable_sources`, `literals_checked`, `unlocated_literals`,
    `misattributed_literals`, `zero_literal_gts`, `orphan_fetches`,
    `provenance_flag`. The file now pins three widths — ten (the twelve
    committed files), thirteen (the v8.18-era shape) and twenty-two (the
    current shape) — all parsing to identical `untraced`/`verdict`/`chain`
    sums. The nine provenance columns are read as bare strings by design
    (`read_defect_incidence` `int()`s only the three `*_flag` columns), so
    the `"n/a"` sentinel (D-10) round-trips safely.

    Controls (a)-(c) pin the compatibility, (d)-(e) pin loudness, (i)-(k)
    extend both to the twenty-two-column width (D-12): (i) all three widths
    agree, (j) the `n/a` sentinel perturbs no int-summed flag, and (k) the
    ragged-row and missing-`chain_flag` failures stay loud at the new width
    while a renamed `provenance_flag` column does not — it is deliberately
    not in `_REQUIRED`.
    """
    ok = True

    def _fail(msg: str) -> None:
        nonlocal ok
        print(f"self-test FAIL: incidence_schema_compat {msg}", file=sys.stderr)
        ok = False

    import tempfile

    narrow_header = "\t".join(_DEFECT_RECORD_FIELDS[:10])
    narrow_row = "condA-P1\t9\t4\t1\t13\t13\t1\t5\t2\t1"
    # Pinned to the v8.18-era thirteen-column shape, matching how
    # narrow_header is pinned to [:10] — _DEFECT_RECORD_FIELDS itself is now
    # 22 names (PROV-05, D-11), so an unsliced join here would silently
    # widen wide_header out from under wide_row's 13 cells.
    wide_header = "\t".join(_DEFECT_RECORD_FIELDS[:13])
    wide_row = narrow_row + "\t0\t0\t2"
    # Phase 5 (PROV-05, D-11/D-12): the current full-width shape, twenty-two
    # names, with the nine new provenance cells filled with the "n/a"
    # sentinel (D-10) — proves the sentinel perturbs none of the int-summed
    # flags.
    widest_header = "\t".join(_DEFECT_RECORD_FIELDS)
    widest_row = wide_row + "\tn/a" * 9

    with tempfile.TemporaryDirectory() as d:
        def _w(name: str, text: str) -> Path:
            f = Path(d) / name
            f.write_text(text, encoding="utf-8")
            return f

        # (a) a real committed ten-column file still parses.
        committed = FIXTURES_DIR / "calibration-v8.6-corpus.tsv"
        try:
            got = read_defect_incidence(committed)
        except Exception as exc:  # noqa: BLE001
            _fail(f"(a) committed ten-column corpus no longer parses: {exc}")
        else:
            if got["n"] != 6:
                _fail(f"(a) committed corpus row count changed: {got!r}")

        # (b) a widened file parses, with identical flag sums.
        a = read_defect_incidence(_w("narrow.tsv", f"{narrow_header}\n{narrow_row}\n"))
        b = read_defect_incidence(_w("wide.tsv", f"{wide_header}\n{wide_row}\n"))
        if a != b:
            _fail(f"(b) narrow and wide files disagree: {a!r} vs {b!r}")

        # (c) a headerless file falls back to positional mapping, read
        # against the current 22-name _DEFECT_RECORD_FIELDS tuple.
        c = read_defect_incidence(_w("nohdr.tsv", widest_row + "\n"))
        if c["n"] != 1 or c["chain"] != 1:
            _fail(f"(c) headerless positional fallback wrong: {c!r}")

        # (d) LOUDNESS: a data row narrower than its own header still raises.
        try:
            read_defect_incidence(_w("ragged.tsv", f"{wide_header}\n{narrow_row}\n"))
        except ValueError:
            pass
        else:
            _fail("(d) ragged row (13-col header, 10-col row) did not raise")

        # (e) LOUDNESS: a header missing a required flag column raises.
        bad = narrow_header.replace("chain_flag", "chain_flagg")
        try:
            read_defect_incidence(_w("badhdr.tsv", f"{bad}\n{narrow_row}\n"))
        except ValueError:
            pass
        else:
            _fail("(e) header missing 'chain_flag' did not raise")

        # (i) three widths agree: ten-, thirteen- and twenty-two-column
        # files all parse to the identical {"untraced","verdict","chain","n"}
        # dict (D-12).
        i_narrow = read_defect_incidence(_w("i-narrow.tsv", f"{narrow_header}\n{narrow_row}\n"))
        i_wide = read_defect_incidence(_w("i-wide.tsv", f"{wide_header}\n{wide_row}\n"))
        i_widest = read_defect_incidence(_w("i-widest.tsv", f"{widest_header}\n{widest_row}\n"))
        if i_narrow != i_wide:
            _fail(f"(i) narrow and wide disagree: {i_narrow!r} vs {i_wide!r}")
        if i_narrow != i_widest:
            _fail(f"(i) narrow and widest disagree: {i_narrow!r} vs {i_widest!r}")
        if i_wide != i_widest:
            _fail(f"(i) wide and widest disagree: {i_wide!r} vs {i_widest!r}")

        # (j) the "n/a" sentinel perturbs nothing: the twenty-two-column
        # result's untraced/verdict/chain sums equal the ten-column result's
        # — nine "n/a" provenance cells changed no int-summed flag. This is
        # what makes D-10's string sentinel safe: `_REQUIRED` covers only
        # untraced_flag/verdict_flag/chain_flag.
        for key in ("untraced", "verdict", "chain"):
            if i_widest[key] != i_narrow[key]:
                _fail(
                    f"(j) n/a sentinel perturbed {key!r}: "
                    f"widest={i_widest[key]!r} narrow={i_narrow[key]!r}"
                )

        # (k) LOUDNESS survives the widening.
        # (k-1) a 22-column header paired with the 13-cell wide_row raises.
        try:
            read_defect_incidence(_w("k-ragged.tsv", f"{widest_header}\n{wide_row}\n"))
        except ValueError:
            pass
        else:
            _fail("(k) 22-col header with 13-cell row did not raise")

        # (k-2) a 22-column header with provenance_flag renamed still
        # parses cleanly — proving the new column is deliberately NOT in
        # `_REQUIRED`.
        k_renamed = widest_header.replace("provenance_flag", "provenance_flagg")
        try:
            read_defect_incidence(_w("k-renamed-prov.tsv", f"{k_renamed}\n{widest_row}\n"))
        except ValueError as exc:
            _fail(
                f"(k) 22-col header with provenance_flag renamed "
                f"unexpectedly raised: {exc}"
            )

        # (k-3) the same header with chain_flag renamed still raises —
        # chain_flag stays required at the new width too.
        k_bad_required = widest_header.replace("chain_flag", "chain_flagg")
        try:
            read_defect_incidence(_w("k-badreq.tsv", f"{k_bad_required}\n{widest_row}\n"))
        except ValueError:
            pass
        else:
            _fail("(k) 22-col header missing 'chain_flag' did not raise")

    # (f)-(h) NON-VACUITY: the three appended columns must actually CARRY the
    # findings. Pinning them only at zero — which every fixture in this file
    # otherwise reports — would pass with the columns hardcoded to a constant,
    # which is precisely the failure this control exists to make impossible.
    # The document below is built to score non-zero on all three at once:
    # C1 and C2 cite each other (a cycle), C3 cites chains that do not exist
    # (ungrounded), and the Self-Audit Gate claims Criterion 4 Rigorous over
    # the top of the cycle (a disagreement).
    doc = """# 1. Problem Essence

**Core problem:** whether the appended columns carry their findings.

# 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| An assumption | convention | Challenge before use | Accept — survives challenge | source |

# 3. Ground Truths

- **GT-1** a fact — source: a source; read-at-source: a location

# 4. Derivation Chains

### Conclusion C1: first

GT-1 (a) + C2 (b)
-> an intermediate claim
-> the first conclusion

### Conclusion C2: second

GT-1 (a) + C1 (b)
-> an intermediate claim
-> the second conclusion

### Conclusion C3: third

C8 (a) + C9 (b)
-> an intermediate claim
-> the third conclusion

# 5. Abandoned Reasoning

Nothing material here - the fixture exists to exercise the dependency graph.

# 6. Conclusion

**Recommended approach:** the first conclusion (C1).

## Process output

**Criterion 4: Reason Upward**
Quoted span: *"GT-1 (a) + C2 (b)"*
Band: **Rigorous**
Justification: every chain names its GT-IDs.
"""
    rec = detect_defects(doc, "schema-nonvacuity")
    for field, want in (("dependency_cycles", 2),
                        ("ungrounded_chains", 1),
                        ("selfaudit_disagreements", 1)):
        if rec[field] != want:
            _fail(f"(f-h) emitted {field}: expected {want}, got {rec[field]!r}")

    # The emitted count must track the audit list, not be computed twice.
    for scalar, listed in (("dependency_cycles", "_dependency_cycles"),
                           ("ungrounded_chains", "_ungrounded_chains"),
                           ("selfaudit_disagreements", "_selfaudit_disagreements")):
        if rec[scalar] != len(rec[listed]):
            _fail(
                f"(f-h) {scalar}={rec[scalar]!r} disagrees with "
                f"len({listed})={len(rec[listed])}"
            )

    return ok


def _selftest_limitation2_citationnorm() -> bool:
    """FIX-CONTRACT-01 limitation 2: `_claim_is_traced()` normalizes stored
    chain ids AND claim text so abbreviated ("(C1)"), lowercase-bolded
    ("chain **C1**"), and pluralized ("(Chains C2, C3)") citations trace —
    plus two regression guards against the loose-match safety bounds
    (quick task 260724-bq3 Task 2).
    """
    ok = True

    positive_cases = [
        (
            "abbreviated (C1)",
            "**Some claim.** gRPC cannot move the median (C1), full stop.",
            ["Chain C1"],
        ),
        (
            "lowercase-bolded chain **C1**",
            '"Some claim text" → chain **C1** ✓',
            ["Chain C1"],
        ),
        (
            "pluralized (Chains C2, C3)",
            "**Insulation — yes** (Chains C2, C3): the strictly better option.",
            ["Chain C2", "Chain C3"],
        ),
    ]
    for label, claim_text, chain_ids in positive_cases:
        if not _claim_is_traced(claim_text, chain_ids, []):
            print(
                f"self-test FAIL: limitation2 {label} case did not trace "
                f"against chain_ids={chain_ids!r}: {claim_text!r}",
                file=sys.stderr,
            )
            ok = False

    # Regression guard: a bare single LETTER with no digit (e.g. "a" from
    # "Chain A") must not loosely substring-match ordinary prose that
    # merely contains the letter "a" — this is the crux residual the whole
    # detector must keep honest (Q-P1-run2's genuinely-uncited claim).
    letter_only_claim = (
        "Establish whether latency is a binding constraint at all — tie it "
        "to an SLO, a user-facing metric, or revenue."
    )
    if _claim_is_traced(letter_only_claim, ["Chain A"], []):
        print(
            "self-test FAIL: limitation2 bare-letter-with-no-digit "
            "regression guard fired — 'Chain A' loosely matched ordinary "
            "prose containing the letter 'a'",
            file=sys.stderr,
        )
        ok = False

    # Regression guard: a bare DIGIT with no letter (e.g. "1" from
    # "Chain 1") must not loosely substring-match ordinary prose that
    # merely contains the digit "1" (e.g. inside "GT-13" or "$310k").
    digit_only_claim = (
        "Insulate over the loft hatch and seal its perimeter — this is "
        "simultaneously the biggest single leakage path (GT-13) and the "
        "largest thermal bypass in the ceiling plane."
    )
    if _claim_is_traced(digit_only_claim, ["Chain 1"], []):
        print(
            "self-test FAIL: limitation2 bare-digit-with-no-letter "
            "regression guard fired — 'Chain 1' loosely matched the digit "
            "'1' inside 'GT-13'",
            file=sys.stderr,
        )
        ok = False

    return ok


def _selftest_limitation3_extractionscope() -> bool:
    """FIX-CONTRACT-01 limitation 3: `_conclusion_claims()` excludes a
    colon-terminated section-intro label with no citation of its own (b),
    and a restatement/corollary of an already-cited claim earlier in the
    same section (c) — while leaving a genuinely-uncited imperative
    recommendation counted and untraced (the honesty-not-score anti-
    overreach guard) (quick task 260724-bq3 Task 2).
    """
    ok = True

    cited_lead = "**The benefit is unquantified:** gRPC cannot move the median (C1)."
    chain_ids = ["C1"]

    # (b) pure section-intro label, no citation of its own -> excluded.
    label_section6 = (
        f"{cited_lead}\n\n"
        "**Before revisiting the decision, close the four unverified "
        "preconditions cheaply:**\n"
        "1. **Measure your own p99** on the six candidate services.\n"
    )
    label_claims = _conclusion_claims(label_section6, chain_ids)
    if any("close the four unverified preconditions" in c for c in label_claims):
        print(
            "self-test FAIL: limitation3(b) section-intro label was not "
            "excluded from conclusion_claims",
            file=sys.stderr,
        )
        ok = False

    # (c) restatement lead-in of an already-cited claim -> excluded.
    restatement_section6 = (
        f"{cited_lead}\n\n"
        "**Bottom line:** the benefit is unquantified, full stop, no "
        "further evidence offered here.\n"
    )
    restatement_claims = _conclusion_claims(restatement_section6, chain_ids)
    if any(c.startswith("**Bottom line:**") for c in restatement_claims):
        print(
            "self-test FAIL: limitation3(c) restatement lead-in was not "
            "excluded from conclusion_claims",
            file=sys.stderr,
        )
        ok = False

    # (c) dual-negation corollary of two already-cited claims -> excluded.
    corollary_section6 = (
        f"{cited_lead}\n\n"
        "**The cost and risk are concrete and front-loaded.** (C1)\n\n"
        "- **Both — no**, and **neither — no**: the two options are not a "
        "bundle; one clears the bar and one doesn't.\n"
    )
    corollary_claims = _conclusion_claims(corollary_section6, chain_ids)
    if any(c.startswith("**Both — no**") for c in corollary_claims):
        print(
            "self-test FAIL: limitation3(c) dual-negation corollary was "
            "not excluded from conclusion_claims",
            file=sys.stderr,
        )
        ok = False

    # Honesty-not-score anti-overreach guard: a genuinely-uncited imperative
    # recommendation with real trailing content is NEITHER a pure label NOR
    # a restatement/corollary shape — it must remain counted as a claim and
    # remain untraced, never silently excluded to force a cleaner tally.
    imperative_section6 = (
        f"{cited_lead}\n\n"
        "1. **Confirm there is an SLO the tail actually threatens** (A2). "
        "If nothing user-facing is at risk at p99, the entire premise "
        "weakens considerably.\n"
    )
    imperative_claims = _conclusion_claims(imperative_section6, chain_ids)
    imperative_claim = next(
        (c for c in imperative_claims if "Confirm there is an SLO" in c), None
    )
    if imperative_claim is None:
        print(
            "self-test FAIL: honesty-not-score anti-overreach guard — a "
            "genuinely-uncited imperative recommendation was incorrectly "
            "excluded from conclusion_claims (must remain counted)",
            file=sys.stderr,
        )
        ok = False
    elif _claim_is_traced(imperative_claim, chain_ids, []):
        print(
            "self-test FAIL: honesty-not-score anti-overreach guard — the "
            "genuinely-uncited imperative recommendation traced when it "
            "should not have (the fixture cites only an out-of-vocabulary "
            "Assumption id, 'A2', not a chain or >=2 GT ids)",
            file=sys.stderr,
        )
        ok = False

    return ok


# ---------------------------------------------------------------------------
# Run layer: --run / --rejudge / --dry-run / --resume (Plan 04 Task 1)
#
# Composes the catalog reader, the live-generation transport, the extraction
# pipeline, the sealed judge packet builder, the scoreline parser and the
# defect detector into three run modes plus a per-invocation manifest.
# `--run` spends 6 generations + 6 judgings; `--rejudge` spends 6 judgings of
# an existing analyses directory with a byte-unchanged packet passthrough
# (T-164-19); `--dry-run` composes with either and spends nothing, making no
# subprocess call at all; `--resume` continues into an existing --out
# directory, re-dispatching only invocations that are absent or hold a
# transport-error/rate-limit stub (T-164-18).
# ---------------------------------------------------------------------------


def classify_invocation_outcome(jsonl_path: Path) -> str:
    """Classify a captured `.jsonl` by PARSING its terminal `result` event —
    never by a bare `grep 'api_error_status'`.

    164-04-PLAN.md's Task 2 checkpoint step 4 originally suggested finding
    rate-limit stubs with `grep -l 'api_error_status' .../*.jsonl`. That idiom
    is wrong and dangerous: `api_error_status` is present — usually `null` —
    on EVERY terminal `result` event, including a fully successful run (the
    committed `tests/quality-probe-v8.7/probe-P1.jsonl` genuine completed
    capture literally contains the substring `"api_error_status":null`). A
    grep for the key's mere presence would match every healthy capture and
    drive `--resume` to re-dispatch all eighteen successful invocations —
    precisely the T-164-18 tampering threat this harness exists to prevent
    ("re-rolling a completed invocation would manufacture a baseline"). This
    function instead parses the terminal event's `is_error` and
    `api_error_status` *values*.

    Returns one of:
      "completed"            — terminal result present, `is_error` is
                                `False` AND `api_error_status` is `None`.
      "rate_limit_stub"      — terminal result present, `api_error_status`
                                is `429`.
      "transport_error_stub" — terminal result present with `is_error` true
                                or any other non-null `api_error_status`.
      "no_terminal_result"   — no terminal `result` event found in the
                                capture at all (treated the same as a stub
                                for `--resume` purposes: not "completed", so
                                eligible for re-dispatch).
    """
    terminal: dict | None = None
    for obj in _iter_jsonl_objects(jsonl_path):
        if obj.get("type") == "result":
            terminal = obj
    if terminal is None:
        return "no_terminal_result"
    is_error = terminal.get("is_error")
    api_error_status = terminal.get("api_error_status")
    if is_error is False and api_error_status is None:
        return "completed"
    if api_error_status == 429:
        return "rate_limit_stub"
    return "transport_error_stub"


def _build_rejudge_packet(source_path: Path, packet_root: Path | None = None) -> Path:
    """`--rejudge` packet builder (T-164-19): pass the source file's bytes
    through unchanged into the packet's analysis file.

    The frozen corpus files carry a trailing transport-metadata tail that the
    ORIGINAL judges scored as part of the document (164-CONTEXT.md's
    `flagged_assumptions`). Stripping or normalising it here — even a
    seemingly harmless whitespace trim — would make the re-judge score a
    different document than the one under measurement, turning a
    reproducibility measurement into a comparison of two different texts.
    Reading via `read_bytes()` and writing via `build_judge_packet`'s bytes
    branch means no decode/encode round-trip and no newline normalisation
    happen anywhere on this path: raw bytes in, raw bytes out.
    """
    return build_judge_packet(source_path.read_bytes(), packet_root=packet_root)


def plan_invocations(
    prompts: list[QualityPrompt],
    repeat: int,
    out_dir: Path,
    rejudge_dir: Path | None,
) -> list[dict]:
    """Enumerate every invocation `--run`/`--rejudge` would dispatch, with no
    subprocess call anywhere in this function.

    Order: one generation + one judge invocation per catalog row per run
    index (1-indexed, matching `scripts/_battery_core.py`'s
    `_run_prompt_n_times_to_paths` naming convention), then one rejudge
    invocation per `.md` file in `rejudge_dir` (when given). Over the real
    three-row catalog at the default repeat of 2, with a 6-file rejudge
    directory, this enumerates 3*2 generations + 3*2 judgings + 6 rejudgings
    = 18 total.

    Each planned invocation dict carries: "index" (1-indexed across the
    whole plan), "kind" ("generation" | "judge" | "rejudge"), "source_id",
    "run_index", and "dest" (the `.jsonl` capture path that invocation would
    write).
    """
    plans: list[dict] = []
    idx = 0
    for prompt in prompts:
        for run_idx in range(1, repeat + 1):
            idx += 1
            plans.append(
                {
                    "index": idx,
                    "kind": "generation",
                    "source_id": prompt.id,
                    "run_index": run_idx,
                    "dest": out_dir / "captures" / f"{prompt.id}-run{run_idx}.jsonl",
                }
            )
            idx += 1
            plans.append(
                {
                    "index": idx,
                    "kind": "judge",
                    "source_id": prompt.id,
                    "run_index": run_idx,
                    "dest": out_dir / "judgments" / f"{prompt.id}-run{run_idx}-judge.jsonl",
                }
            )
    if rejudge_dir is not None:
        for f in sorted(Path(rejudge_dir).glob("*.md")):
            idx += 1
            plans.append(
                {
                    "index": idx,
                    "kind": "rejudge",
                    "source_id": f.stem,
                    "run_index": 1,
                    "dest": out_dir / "rejudge-judgments" / f"{f.stem}-judge.jsonl",
                }
            )
    return plans


def run_dry_run(args: argparse.Namespace) -> int:
    """`--dry-run` CLI body.

    Structural guard, not a conditional inside the transport function: this
    function calls only `_read_quality_catalog` and `plan_invocations`,
    neither of which ever calls `_run_prompt_to` — the dry-run path simply
    does not contain a code path that reaches the transport function, so no
    subprocess is spawned and no capture file is created. Prints one line per
    planned invocation (kind, source id, run index, destination path),
    followed by a total count.
    """
    prompts = _read_quality_catalog(args.catalog or DEFAULT_CATALOG) if args.run else []
    plans = plan_invocations(
        prompts, args.repeat, args.out, args.rejudge if args.rejudge else None
    )
    for p in plans:
        print(f"{p['kind']}\t{p['source_id']}\t{p['run_index']}\t{p['dest']}")
    print(f"Total planned invocations: {len(plans)}")
    return 0


def run_generation_arm(
    prompts: list[QualityPrompt],
    repeat: int,
    out_dir: Path,
    plugin_dir: Path,
    manifest_rows: list[dict],
    resume: bool = False,
) -> dict[str, str]:
    """D-01/D-08: dispatch `repeat` live generations per catalog row, extract
    each through `extract_agent_analysis` (Guardrails A and B apply to every
    one of the six), write the extracted analyses to `out_dir/analyses/`, and
    append one manifest row per invocation to `manifest_rows`.

    `source_id` naming is `<catalog_id>-run<n>` (1-indexed), matching
    `scripts/_battery_core.py::_run_prompt_n_times_to_paths`'s convention.

    `resume` (T-164-18): an existing capture whose terminal result classifies
    "completed" (`classify_invocation_outcome`) is never re-dispatched —
    its analysis is instead re-extracted from the existing capture file.
    Anything else (absent, transport-error stub, rate-limit stub) is
    (re-)dispatched exactly once.

    Returns `{source_id: analysis_text}` for `run_judging_arm`.
    """
    captures_dir = out_dir / "captures"
    analyses_dir = out_dir / "analyses"
    captures_dir.mkdir(parents=True, exist_ok=True)
    analyses_dir.mkdir(parents=True, exist_ok=True)

    analyses: dict[str, str] = {}
    idx = len(manifest_rows)
    for prompt in prompts:
        for run_idx in range(1, repeat + 1):
            idx += 1
            source_id = f"{prompt.id}-run{run_idx}"
            cap_path = captures_dir / f"{source_id}.jsonl"
            duration = 0.0
            redispatch_reason = ""
            already_completed = (
                resume
                and cap_path.is_file()
                and classify_invocation_outcome(cap_path) == "completed"
            )
            if not already_completed:
                if resume and cap_path.is_file():
                    redispatch_reason = "prior capture was a transport-error or rate-limit stub"
                start = time.monotonic()
                wrapped = _wrap_for_bypass(prompt.text)
                _run_prompt_to(wrapped, cap_path, plugin_dir=plugin_dir)
                duration = time.monotonic() - start
            outcome = classify_invocation_outcome(cap_path)
            manifest_rows.append(
                {
                    "index": idx,
                    "kind": "generation",
                    "source_id": prompt.id,
                    "run_index": run_idx,
                    "dest_path": str(cap_path),
                    "duration_s": f"{duration:.1f}",
                    "outcome": outcome,
                    "redispatch_reason": redispatch_reason,
                }
            )
            if outcome != "completed":
                continue
            analysis_text = extract_agent_analysis(
                cap_path, subagent_type="first-principles:first-principles"
            )
            (analyses_dir / f"{source_id}.md").write_text(analysis_text, encoding="utf-8")
            analyses[source_id] = analysis_text
    return analyses


def _write_blinding_key(rows: list[tuple[str, str]], path: Path) -> None:
    """Write `packet_id \\t source_id` rows to the run's blinding key.

    Lives in the output directory root (D-05) — never inside or beside a
    packet directory, so the mapping is not visible from a judge's cwd.

    SCOPE OF THIS GUARANTEE (narrowed at the Phase 164 code review, WR-02).
    This prevents PASSIVE discovery: a judge placed in a sealed packet dir
    never encounters the key by listing its own directory or walking up from
    it, and `check_blinding`'s ancestor-walk asserts exactly that. It does
    NOT prevent ACTIVE search. The judge is dispatched through
    `_run_prompt_to` with `--permission-mode bypassPermissions` and no
    `--allowedTools` restriction, so the subprocess retains full filesystem
    tool access and could in principle locate the committed
    `blinding-key.tsv`, `scorelines.tsv`, or the v8.6 answer table by
    searching for them. Do not describe this mechanism as blinding "enforced
    by unreachability" — it is enforced by non-exposure, and an actively
    searching judge is outside its threat model.

    The transport argv is deliberately NOT tightened here: it is Plan-36-
    locked and byte-shared with the frozen baseline, so adding
    `--allowedTools` would make future runs non-comparable with the evidence
    this phase froze. Tightening it is a future-phase change that must
    re-baseline, not a drive-by edit.
    """
    lines = [f"{packet_id}\t{source_id}" for packet_id, source_id in rows]
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def run_judging_arm(
    items: list[tuple[str, "str | Path"]],
    out_dir: Path,
    dest_subdir: str,
    kind: str,
    manifest_rows: list[dict],
    blinding_key_path: Path,
    plugin_dir: Path | None = None,
    resume: bool = False,
) -> list[dict]:
    """Build one sealed packet and dispatch one judge invocation per item.

    `items` is a list of `(source_id, analysis)` pairs. When `analysis` is a
    `str` (the `--run` fresh-generation path), the packet is built through
    `build_judge_packet`'s text branch. When it is a `Path` (the `--rejudge`
    path), the packet is built through `_build_rejudge_packet`'s
    byte-unchanged passthrough (T-164-19) — the two paths are never
    conflated.

    Packet identifiers are shuffled (`random.shuffle`) so the mapping from
    identifier to source analysis is not recoverable from ordering (D-05);
    that mapping is written to `blinding_key_path` in the output directory
    root, never inside or beside a packet. `plugin_dir=None` (D-05
    Assumption A3): the judge invocation must have no agent-dispatch
    surface, so `--plugin-dir` is omitted from its transport call entirely.

    `resume` mirrors `run_generation_arm`'s discipline: a judge capture that
    already classifies "completed" is never re-dispatched.

    Returns one `tabulate_rows()`-shaped row dict per item, each carrying an
    additional `"source_id"` field, in the shuffled packet order.
    """
    judgments_dir = out_dir / dest_subdir
    judgments_dir.mkdir(parents=True, exist_ok=True)

    packet_ids = [f"P{i + 1:02d}" for i in range(len(items))]
    random.shuffle(packet_ids)

    rows: list[dict] = []
    blinding_rows: list[tuple[str, str]] = []
    idx = len(manifest_rows)
    for (source_id, analysis), packet_id in zip(items, packet_ids):
        idx += 1
        blinding_rows.append((packet_id, source_id))
        judge_capture = judgments_dir / f"{packet_id}-judge.jsonl"
        duration = 0.0
        redispatch_reason = ""
        already_completed = (
            resume
            and judge_capture.is_file()
            and classify_invocation_outcome(judge_capture) == "completed"
        )
        if not already_completed:
            if resume and judge_capture.is_file():
                redispatch_reason = "prior judge capture was a transport-error or rate-limit stub"
            packet_dir = (
                _build_rejudge_packet(analysis)
                if isinstance(analysis, Path)
                else build_judge_packet(analysis)
            )
            start = time.monotonic()
            _run_prompt_to(JUDGE_PROMPT, judge_capture, plugin_dir=plugin_dir, cwd=packet_dir)
            duration = time.monotonic() - start
        outcome = classify_invocation_outcome(judge_capture)
        manifest_rows.append(
            {
                "index": idx,
                "kind": kind,
                "source_id": source_id,
                "run_index": 1,
                "dest_path": str(judge_capture),
                "duration_s": f"{duration:.1f}",
                "outcome": outcome,
                "redispatch_reason": redispatch_reason,
            }
        )
        if outcome != "completed":
            rows.append(
                {
                    "source_id": source_id,
                    "packet_id": packet_id,
                    "bands": [UNPARSEABLE] * len(_CRITERIA),
                    "judge_verdict": UNPARSEABLE,
                    "derived_verdict": UNPARSEABLE,
                    "agreement": UNPARSEABLE,
                }
            )
            continue
        judge_text = extract_judge_verdict(judge_capture)
        # The rationale is evidence, never a score (D-12) — captured verbatim
        # to a sidecar file alongside the parsed row.
        (judgments_dir / f"{packet_id}-rationale.md").write_text(judge_text, encoding="utf-8")
        row = _build_scoreline_row(packet_id=packet_id, judge_text=judge_text)
        row["source_id"] = source_id
        rows.append(row)

    _write_blinding_key(blinding_rows, blinding_key_path)
    return rows


# Column order matches the legacy 8-column shape (`packet_id`, C1..C6,
# `judge_verdict`) for its first 8 columns, so `read_scorelines` — which
# reads column 0 as "id", columns 1-6 as bands, and column 7 as the judge's
# stated verdict, ignoring anything beyond — can read this eleven-column
# file without modification. `derived_verdict`, `agreement`, and `source_id`
# are the three additional columns D-08's regenerated baseline needs.
_RUN_SCORELINE_FIELDS = (
    "packet_id",
    *_CRITERIA,
    "judge_verdict",
    "derived_verdict",
    "agreement",
    "source_id",
)


def write_run_scorelines(rows: list[dict], out_path: Path) -> None:
    """Write the eleven-column `--run`/`--rejudge` scoreline TSV.

    Each row must carry "packet_id", "bands" (list[str], length 6),
    "judge_verdict", "derived_verdict", "agreement", and "source_id" — the
    shape `run_judging_arm` returns.
    """
    lines = ["\t".join(_RUN_SCORELINE_FIELDS)]
    for row in rows:
        lines.append(
            "\t".join(
                [
                    row["packet_id"],
                    *row["bands"],
                    row["judge_verdict"],
                    row["derived_verdict"],
                    row["agreement"],
                    row["source_id"],
                ]
            )
        )
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


_MANIFEST_FIELDS = (
    "index",
    "kind",
    "source_id",
    "run_index",
    "dest_path",
    "duration_s",
    "outcome",
    "redispatch_reason",
)


def write_run_manifest(rows: list[dict], out_path: Path) -> None:
    """T-164-18/T-164-22: write one manifest row per invocation.

    This is what makes the eighteen live invocations auditable — the record
    Task 3's acceptance criteria count. `outcome` is one of "completed",
    "transport_error_stub", "rate_limit_stub", or "no_terminal_result"
    (`classify_invocation_outcome`); `redispatch_reason` is non-empty only
    when `--resume` actually re-dispatched a prior stub.
    """
    lines = ["\t".join(_MANIFEST_FIELDS)]
    for row in rows:
        lines.append("\t".join(str(row.get(field, "")) for field in _MANIFEST_FIELDS))
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _selftest_resume_classification() -> bool:
    """Part of D-15/D-08 item 8: `classify_invocation_outcome` classifies by
    PARSING the terminal `result` event, never by grepping the
    `api_error_status` key.

    Four synthetic fixtures pin the four return values. A fifth check reads
    the real committed `tests/quality-probe-v8.7/probe-P1.jsonl` — a genuine
    completed run — and confirms two things at once: the literal substring
    `"api_error_status"` IS present in its text (so a bare grep for the key
    would wrongly flag this healthy capture as a stub), and
    `classify_invocation_outcome` nonetheless correctly classifies it
    "completed" by reading the value, not the key's presence.
    """
    ok = True

    def _fixture_path(events: list[dict]) -> Path:
        tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".jsonl", delete=False, encoding="utf-8"
        )
        for e in events:
            tmp.write(json.dumps(e) + "\n")
        tmp.close()
        return Path(tmp.name)

    cases = [
        (
            "completed",
            [{"type": "result", "subtype": "success", "is_error": False, "api_error_status": None}],
            "completed",
        ),
        (
            "transport_error",
            [{"type": "result", "subtype": "error", "is_error": True, "api_error_status": None}],
            "transport_error_stub",
        ),
        (
            "rate_limited",
            [{"type": "result", "subtype": "error", "is_error": True, "api_error_status": 429}],
            "rate_limit_stub",
        ),
        (
            "no_terminal",
            [{"type": "assistant", "message": {"content": []}}],
            "no_terminal_result",
        ),
    ]
    for name, events, expected in cases:
        path = _fixture_path(events)
        try:
            got = classify_invocation_outcome(path)
        finally:
            try:
                path.unlink()
            except OSError:
                pass
        if got != expected:
            print(
                f"self-test FAIL: run_layer resume classification fixture "
                f"{name!r} expected {expected!r}, got {got!r}",
                file=sys.stderr,
            )
            ok = False

    # Real-evidence proof that the rejected `grep 'api_error_status'` idiom
    # (164-04-PLAN.md's Task 2 checkpoint step 4) is wrong: the committed
    # probe capture is a genuine completed run, yet the literal key
    # `"api_error_status"` IS present in its text (value null) — a grep for
    # the key alone would misclassify it as a stub and drive --resume to
    # re-dispatch an already-successful invocation (T-164-18).
    probe_path = REPO_ROOT / "tests" / "quality-probe-v8.7" / "probe-P1.jsonl"
    probe_text = probe_path.read_text(encoding="utf-8")
    if '"api_error_status"' not in probe_text:
        print(
            "self-test FAIL: run_layer resume classification — expected the "
            "committed probe capture to contain the literal "
            '\'"api_error_status"\' key (demonstrating why a bare grep for '
            "that key is wrong), but it was absent",
            file=sys.stderr,
        )
        ok = False
    if classify_invocation_outcome(probe_path) != "completed":
        print(
            "self-test FAIL: run_layer resume classification — the committed "
            "probe capture is a genuine completed run and must classify "
            "'completed', proving the parser (not a grep) is what the "
            "harness relies on",
            file=sys.stderr,
        )
        ok = False

    return ok


def _selftest_run_layer() -> bool:
    """D-15/D-08 item 8: the run layer — offline, no `claude` invoked.

    1. A dry-run over the real catalog at the default repeat, with the
       frozen corpus as the rejudge source, must print a total of eighteen
       planned invocations (six generations + six judgings + six
       rejudgings) and must make ZERO calls to `_run_prompt_to` — proven by
       a counting monkeypatch of `_run_prompt_to` around a real invocation
       of `run_dry_run`, not merely by trusting the printed total — and must
       create zero capture files under a fresh temp `--out` directory
       (fault injection L).
    2. `_build_rejudge_packet`'s packet analysis file must be byte-identical
       to its source file, checked against a real frozen-corpus fixture
       (fault injection M).
    3. `write_run_manifest` emits one row per planned invocation with the
       required eight columns.
    4. `classify_invocation_outcome` classifies by PARSING, never by
       grepping `api_error_status` (`_selftest_resume_classification`).
    """
    ok = True

    # --- 1. dry-run count + zero-side-effect ---
    tmp_root = Path(tempfile.mkdtemp(prefix="qh-selftest-dryrun-"))
    try:
        plans = plan_invocations(
            _read_quality_catalog(DEFAULT_CATALOG),
            DEFAULT_REPEAT,
            tmp_root,
            BASELINE_DIR / "analyses",
        )
        if len(plans) != 18:
            print(
                f"self-test FAIL: run_layer plan_invocations expected 18 "
                f"planned invocations, got {len(plans)}",
                file=sys.stderr,
            )
            ok = False

        # Never delegates to the real `_run_prompt_to` — this must remain
        # true even under a deliberately fault-injected `run_dry_run` (Fault
        # injection L), so the self-test can prove the zero-call count
        # without ever spawning a real `claude` subprocess.
        call_count = {"n": 0}
        real_run_prompt_to = globals()["_run_prompt_to"]

        def _counting_run_prompt_to(*a, **kw):
            call_count["n"] += 1
            out_path = a[1] if len(a) > 1 else kw.get("out_path")
            return out_path

        dry_args = argparse.Namespace(
            out=tmp_root,
            run=True,
            rejudge=BASELINE_DIR / "analyses",
            catalog=DEFAULT_CATALOG,
            repeat=DEFAULT_REPEAT,
        )
        globals()["_run_prompt_to"] = _counting_run_prompt_to
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                run_dry_run(dry_args)
        finally:
            globals()["_run_prompt_to"] = real_run_prompt_to

        printed = buf.getvalue()
        if "Total planned invocations: 18" not in printed:
            print(
                "self-test FAIL: run_layer dry-run did not print a total of "
                f"18 planned invocations: {printed!r}",
                file=sys.stderr,
            )
            ok = False
        if call_count["n"] != 0:
            print(
                f"self-test FAIL: run_layer dry-run called _run_prompt_to "
                f"{call_count['n']} times — expected 0 (zero-side-effect)",
                file=sys.stderr,
            )
            ok = False
        jsonl_after = list(tmp_root.rglob("*.jsonl"))
        if jsonl_after:
            print(
                f"self-test FAIL: run_layer dry-run created capture files: "
                f"{jsonl_after!r}",
                file=sys.stderr,
            )
            ok = False
    finally:
        shutil.rmtree(tmp_root, ignore_errors=True)

    # --- 2. rejudge byte-identity passthrough ---
    fixture_source = BASELINE_DIR / "analyses" / "condA-P1.md"
    fixture_bytes = fixture_source.read_bytes()
    try:
        packet_dir = _build_rejudge_packet(fixture_source)
    except Exception as exc:  # noqa: BLE001
        print(
            f"self-test FAIL: run_layer rejudge packet build raised "
            f"unexpectedly: {exc!r}",
            file=sys.stderr,
        )
        return False
    packet_bytes = (packet_dir / "analysis.md").read_bytes()
    if packet_bytes != fixture_bytes:
        print(
            "self-test FAIL: run_layer rejudge byte-identity — packet "
            f"analysis.md differs from its source (source len="
            f"{len(fixture_bytes)}, packet len={len(packet_bytes)})",
            file=sys.stderr,
        )
        ok = False

    # --- 3. manifest writer ---
    manifest_fixture_rows = [
        {
            "index": 1,
            "kind": "generation",
            "source_id": "Q-P1",
            "run_index": 1,
            "dest_path": "/tmp/x/captures/Q-P1-run1.jsonl",
            "duration_s": "12.3",
            "outcome": "completed",
            "redispatch_reason": "",
        },
        {
            "index": 2,
            "kind": "judge",
            "source_id": "Q-P1",
            "run_index": 1,
            "dest_path": "/tmp/x/judgments/P01-judge.jsonl",
            "duration_s": "8.1",
            "outcome": "transport_error_stub",
            "redispatch_reason": "",
        },
    ]
    manifest_tmp_dir = Path(tempfile.mkdtemp(prefix="qh-selftest-manifest-"))
    try:
        manifest_path = manifest_tmp_dir / "manifest.tsv"
        write_run_manifest(manifest_fixture_rows, manifest_path)
        lines = manifest_path.read_text(encoding="utf-8").splitlines()
        if not lines or lines[0].split("\t") != list(_MANIFEST_FIELDS):
            print(
                f"self-test FAIL: run_layer manifest header expected "
                f"{_MANIFEST_FIELDS!r}, got "
                f"{lines[0].split(chr(9)) if lines else None!r}",
                file=sys.stderr,
            )
            ok = False
        if len(lines) != 1 + len(manifest_fixture_rows):
            print(
                f"self-test FAIL: run_layer manifest expected "
                f"{1 + len(manifest_fixture_rows)} lines (header + one per "
                f"planned invocation), got {len(lines)}",
                file=sys.stderr,
            )
            ok = False
    finally:
        shutil.rmtree(manifest_tmp_dir, ignore_errors=True)

    # --- 4. resume classification by PARSING, never by grepping the key ---
    if not _selftest_resume_classification():
        ok = False

    return ok


def _self_test_tracer_path() -> bool:
    """Tracer edge (D-15 item 6 lineage): the whole offline chain, no live call.

    Extracts the real committed probe capture, builds a sealed packet from it,
    parses a fixture judge scoreline, derives PASS/FAIL, and tabulates one row
    — proving the path this plan wires end to end is actually reachable and
    non-vacuous, under both `python3` and `python3 -O`.
    """
    ok = True

    probe_path = REPO_ROOT / "tests" / "quality-probe-v8.7" / "probe-P1.jsonl"
    try:
        analysis = extract_agent_analysis(
            probe_path, subagent_type="first-principles:first-principles"
        )
    except Exception as exc:  # noqa: BLE001 — self-test must report, not crash
        print(
            f"self-test FAIL: tracer_path extraction raised unexpectedly: {exc!r}",
            file=sys.stderr,
        )
        return False

    if len(analysis) <= 2000:
        print(
            f"self-test FAIL: tracer_path extracted analysis is too short "
            f"({len(analysis)} chars, expected > 2000)",
            file=sys.stderr,
        )
        ok = False
    if _LAUNCH_ACK_PHRASE in analysis:
        print(
            "self-test FAIL: tracer_path extracted analysis contains the "
            f"launch-acknowledgement phrase {_LAUNCH_ACK_PHRASE!r}",
            file=sys.stderr,
        )
        ok = False

    try:
        packet_dir = build_judge_packet(analysis)
    except Exception as exc:  # noqa: BLE001
        print(
            f"self-test FAIL: tracer_path build_judge_packet raised unexpectedly: {exc!r}",
            file=sys.stderr,
        )
        return False

    entries = sorted(p.name for p in packet_dir.iterdir())
    if entries != ["analysis.md", "validation-rubric.md"]:
        print(
            f"self-test FAIL: tracer_path packet dir has wrong entries: {entries!r}",
            file=sys.stderr,
        )
        ok = False
    resolved = packet_dir.resolve()
    repo_root_resolved = REPO_ROOT.resolve()
    if resolved == repo_root_resolved or repo_root_resolved in resolved.parents:
        print(
            f"self-test FAIL: tracer_path packet dir {resolved} is inside the repo root",
            file=sys.stderr,
        )
        ok = False

    parsed = parse_scoreline(_FIXTURE_SCORELINE_TEXT)
    if parsed == UNPARSEABLE:
        print(
            "self-test FAIL: tracer_path fixture scoreline failed to parse",
            file=sys.stderr,
        )
        return False
    bands, judge_verdict = parsed
    derived = derive_pass_fail(bands)
    agreement = "AGREE" if derived == judge_verdict else "DISAGREE"
    row = {
        "packet_id": "tracer-fixture",
        "bands": bands,
        "judge_verdict": judge_verdict,
        "derived_verdict": derived,
        "agreement": agreement,
    }
    table = tabulate_rows([row])
    if "tracer-fixture" not in table or agreement != "AGREE":
        print(
            f"self-test FAIL: tracer_path tabulation did not emit the expected "
            f"AGREE row (agreement={agreement!r}, table={table!r})",
            file=sys.stderr,
        )
        ok = False

    return ok


# ---------------------------------------------------------------------------
# Compare (D-04) — offline post-fix-vs-baseline delta tabulation.
#
# `--compare POST_DIR --baseline BASE_DIR` diffs two run directories
# (each shaped like tests/quality-baseline-v8.7-regenerated/: a
# scorelines.tsv plus a defect-incidence.tsv) and reports band, pass-split,
# and defect-incidence deltas plus a computed Goodhart flag. Fully offline —
# same class as --detect-defects, reaching no `_run_prompt_to`.
# ---------------------------------------------------------------------------

# C2 (verdict vocab), C4 (chain rigor), and C6 (conclusion traceability) are
# the Goodhart-guard bands named in 166-CONTEXT.md D-03.3 — zero-indexed
# positions 1, 3, 5 in `_CRITERIA`.
_GOODHART_GUARD_INDICES = (1, 3, 5)


def read_defect_incidence(path: Path | str) -> dict:
    """Parse a `run_detect_defects`-shaped defect-incidence.tsv into per-family sums.

    Reads a `_DEFECT_RECORD_FIELDS`-shaped file (header row plus one data row
    per analysis). **Columns are mapped by HEADER NAME when a header is
    present**, so a file written before a column was appended parses
    unchanged: every committed defect-incidence TSV in `tests/` is the
    original ten-column shape, and widening the schema must not orphan them.
    A headerless file falls back to positional mapping against the current
    `_DEFECT_RECORD_FIELDS`, which is the only reading available for it.

    The header is recognised by `cells[0] == "analysis_id"` — a real analysis
    id is never literally that string.

    Returns {"untraced": int, "verdict": int, "chain": int, "n": int} — the
    summed `untraced_flag`/`verdict_flag`/`chain_flag` columns across every
    data row, and `n` the row (analysis) count.

    Raises ValueError naming the path on a missing file or a data row whose
    column count differs from `len(_DEFECT_RECORD_FIELDS)` — a truncated or
    malformed defect-incidence file is a loud failure, never a
    silently-shorter comparison (T-164-12 discipline).
    """
    path = Path(path)
    if not path.is_file():
        raise ValueError(f"{path}: defect-incidence file not found")

    _REQUIRED = ("untraced_flag", "verdict_flag", "chain_flag")

    untraced = 0
    verdict = 0
    chain = 0
    n = 0
    header: tuple[str, ...] | None = None
    text = path.read_text(encoding="utf-8")
    for lineno, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        cells = line.split("\t")
        if lineno == 1 and cells[0] == "analysis_id":
            header = tuple(c.strip() for c in cells)
            missing = [c for c in _REQUIRED if c not in header]
            if missing:
                raise ValueError(
                    f"{path}:{lineno}: header is missing required "
                    f"column(s) {missing}: {list(header)!r}"
                )
            continue
        fields = header if header is not None else _DEFECT_RECORD_FIELDS
        if len(cells) != len(fields):
            raise ValueError(
                f"{path}:{lineno}: expected {len(fields)} "
                f"tab-separated columns, got {len(cells)}: {cells!r}"
            )
        record = dict(zip(fields, cells))
        try:
            untraced += int(record["untraced_flag"])
            verdict += int(record["verdict_flag"])
            chain += int(record["chain_flag"])
        except ValueError as exc:
            raise ValueError(
                f"{path}:{lineno}: non-integer flag value in "
                f"defect-incidence row: {exc}"
            ) from exc
        n += 1

    return {"untraced": untraced, "verdict": verdict, "chain": chain, "n": n}


def compute_compare(baseline_dir: Path | str, post_dir: Path | str) -> dict:
    """D-04: diff a post-fix run directory against a named baseline directory.

    Comparison is over AGGREGATES only (sums and N/analyses tallies) —
    packet IDs are shuffled and unmatched by design (each run's own
    blinding key maps its own packet IDs to its own source files
    independently), so no per-packet pairing is attempted here.

    Reads `scorelines.tsv` from each directory via `read_scorelines` +
    `compute_tabulation_summary`, and `defect-incidence.tsv` from each via
    `read_defect_incidence`.

    Returns a dict:
      - per_criterion: {crit: {"baseline", "post", "delta"}} for C1..C6.
      - aggregate: {"baseline_total", "post_total", "delta",
        "baseline_mean", "post_mean"}.
      - pass_split: {"baseline_pass", "baseline_fail", "post_pass",
        "post_fail", "delta_pass", "delta_fail"}.
      - defects: {"untraced"|"verdict"|"chain": {"baseline", "post",
        "delta", "baseline_n", "post_n"}}.
      - goodhart_fired: bool — True iff at least one defect family fell
        (post incidence < baseline incidence for untraced, verdict, OR
        chain) AND the C2, C4, AND C6 baseline-vs-post band-sums are ALL
        unchanged (166-CONTEXT.md D-03.3) — the reported
        "form-without-substance" signature, never an auto pass/fail gate.

    Raises ValueError (propagated from `read_scorelines` /
    `read_defect_incidence`, or from a missing scorelines.tsv) on a missing
    or malformed input file — never a silently-shorter comparison.
    """
    baseline_dir = Path(baseline_dir)
    post_dir = Path(post_dir)

    baseline_scorelines_path = baseline_dir / "scorelines.tsv"
    post_scorelines_path = post_dir / "scorelines.tsv"
    if not baseline_scorelines_path.is_file():
        raise ValueError(f"{baseline_scorelines_path}: scorelines file not found")
    if not post_scorelines_path.is_file():
        raise ValueError(f"{post_scorelines_path}: scorelines file not found")

    baseline_summary = compute_tabulation_summary(
        read_scorelines(baseline_scorelines_path)
    )
    post_summary = compute_tabulation_summary(read_scorelines(post_scorelines_path))

    per_criterion: dict[str, dict] = {}
    for idx, crit in enumerate(_CRITERIA):
        b = baseline_summary["per_criterion_sums"][idx]
        p = post_summary["per_criterion_sums"][idx]
        per_criterion[crit] = {"baseline": b, "post": p, "delta": p - b}

    aggregate = {
        "baseline_total": baseline_summary["aggregate_band_total"],
        "post_total": post_summary["aggregate_band_total"],
        "delta": post_summary["aggregate_band_total"]
        - baseline_summary["aggregate_band_total"],
        "baseline_mean": baseline_summary["mean"],
        "post_mean": post_summary["mean"],
    }

    pass_split = {
        "baseline_pass": baseline_summary["pass_count"],
        "baseline_fail": baseline_summary["fail_count"],
        "post_pass": post_summary["pass_count"],
        "post_fail": post_summary["fail_count"],
        "delta_pass": post_summary["pass_count"] - baseline_summary["pass_count"],
        "delta_fail": post_summary["fail_count"] - baseline_summary["fail_count"],
    }

    baseline_defects = read_defect_incidence(baseline_dir / "defect-incidence.tsv")
    post_defects = read_defect_incidence(post_dir / "defect-incidence.tsv")

    defects: dict[str, dict] = {}
    any_family_fell = False
    for family in ("untraced", "verdict", "chain"):
        b = baseline_defects[family]
        p = post_defects[family]
        if p < b:
            any_family_fell = True
        defects[family] = {
            "baseline": b,
            "post": p,
            "delta": p - b,
            "baseline_n": baseline_defects["n"],
            "post_n": post_defects["n"],
        }

    guard_unchanged = all(
        per_criterion[_CRITERIA[idx]]["delta"] == 0 for idx in _GOODHART_GUARD_INDICES
    )
    goodhart_fired = any_family_fell and guard_unchanged

    return {
        "per_criterion": per_criterion,
        "aggregate": aggregate,
        "pass_split": pass_split,
        "defects": defects,
        "goodhart_fired": goodhart_fired,
    }


def format_compare_report(result: dict) -> str:
    """D-04: render `compute_compare`'s result dict to a labelled text report.

    Sections: `[BANDS]` (per-criterion baseline -> post (delta) rows, an
    aggregate band-total row, and a mean/analysis row), `[PASS SPLIT]`
    (PASS and FAIL baseline -> post rows), `[DEFECT INCIDENCE]`
    (untraced/verdict/chain baseline N/n -> post N/n (delta) rows), and a
    final `GOODHART_FLAG:` line reading `FIRED` or `clear`.

    This is a REPORTER — it renders whatever `result` says and never
    adjusts phrasing for a favourable or unfavourable reading
    (honesty-not-score, D-01 global).
    """
    lines: list[str] = []

    lines.append("[BANDS]")
    for crit in _CRITERIA:
        row = result["per_criterion"][crit]
        lines.append(f"  {crit}: {row['baseline']} -> {row['post']} ({row['delta']:+d})")
    agg = result["aggregate"]
    lines.append(
        f"  aggregate: {agg['baseline_total']}/108 -> {agg['post_total']}/108 "
        f"({agg['delta']:+d})"
    )
    lines.append(f"  mean/analysis: {agg['baseline_mean']:.2f} -> {agg['post_mean']:.2f}")
    lines.append("")

    lines.append("[PASS SPLIT]")
    ps = result["pass_split"]
    lines.append(f"  PASS: {ps['baseline_pass']} -> {ps['post_pass']} ({ps['delta_pass']:+d})")
    lines.append(f"  FAIL: {ps['baseline_fail']} -> {ps['post_fail']} ({ps['delta_fail']:+d})")
    lines.append("")

    lines.append("[DEFECT INCIDENCE]")
    for family in ("untraced", "verdict", "chain"):
        d = result["defects"][family]
        lines.append(
            f"  {family}: {d['baseline']}/{d['baseline_n']} -> "
            f"{d['post']}/{d['post_n']} ({d['delta']:+d})"
        )
    lines.append("")

    lines.append(f"GOODHART_FLAG: {'FIRED' if result['goodhart_fired'] else 'clear'}")

    return "\n".join(lines)


def run_compare(baseline_dir: Path | str, post_dir: Path | str) -> int:
    """`--compare`/`--baseline` CLI body (D-04).

    Fully offline — no `claude` process is spawned and no function reaching
    `_run_prompt_to` is called; this branch sits in `main()` before the
    live `--run`/`--rejudge` dispatch and before `_ensure_claude_available()`
    is ever invoked.

    Prints the four-section delta report and the computed Goodhart flag.
    This is a REPORTER: it returns 0 on a well-formed comparison and 2 on a
    missing/malformed input directory — it never returns non-zero merely
    because the comparison itself reads unfavourably (honesty-not-score,
    D-01 global).
    """
    try:
        result = compute_compare(baseline_dir, post_dir)
    except (ValueError, OSError) as exc:
        print(f"--compare: {exc}", file=sys.stderr)
        return 2

    print(format_compare_report(result))
    return 0


_COMPARE_FIXTURES_DIR = FIXTURES_DIR / "compare"
_COMPARE_FIXTURE_POSITIVE = _COMPARE_FIXTURES_DIR / "positive"
_COMPARE_FIXTURE_GOODHART = _COMPARE_FIXTURES_DIR / "goodhart"

# Hand-checked expected `compute_compare` output for the positive/ pair
# (post moves C2/C4/C6 bands up AND lowers the `untraced` defect family
# while `verdict`/`chain` stay unchanged — Goodhart flag must read clear,
# substance is present). See tests/quality-fixtures-v8.7/compare/ fixture
# files themselves for the raw TSVs these figures are hand-derived from.
_EXPECTED_POSITIVE_PER_CRITERION = {
    "C1": {"baseline": 4, "post": 4, "delta": 0},
    "C2": {"baseline": 2, "post": 4, "delta": 2},
    "C3": {"baseline": 4, "post": 4, "delta": 0},
    "C4": {"baseline": 2, "post": 4, "delta": 2},
    "C5": {"baseline": 4, "post": 4, "delta": 0},
    "C6": {"baseline": 2, "post": 4, "delta": 2},
}
_EXPECTED_POSITIVE_AGGREGATE = {
    "baseline_total": 18,
    "post_total": 24,
    "delta": 6,
    "baseline_mean": 9.0,
    "post_mean": 12.0,
}
_EXPECTED_POSITIVE_PASS_SPLIT = {
    "baseline_pass": 0,
    "baseline_fail": 2,
    "post_pass": 2,
    "post_fail": 0,
    "delta_pass": 2,
    "delta_fail": -2,
}
_EXPECTED_POSITIVE_DEFECTS = {
    "untraced": {"baseline": 2, "post": 0, "delta": -2, "baseline_n": 2, "post_n": 2},
    "verdict": {"baseline": 2, "post": 2, "delta": 0, "baseline_n": 2, "post_n": 2},
    "chain": {"baseline": 2, "post": 2, "delta": 0, "baseline_n": 2, "post_n": 2},
}


def _selftest_compare() -> bool:
    """9th self-test item (D-04/D-16): non-vacuous `--compare` coverage.

    Accumulates failures into a local flag rather than a bare `assert`
    (D-16 — a bare `assert` prints PASS under `python3 -O`) and NEVER
    short-circuits on the first failure, so a fault-injection proof against
    any single check surfaces on its own labelled failure line.

    Runs `compute_compare` over the `positive/` fixture pair and checks
    every per-criterion delta, the aggregate delta, the pass-split deltas,
    and the per-defect deltas against the hand-checked literals above, and
    that its `goodhart_fired` is False (substance present, flag clear).
    Then runs `compute_compare` over the `goodhart/` fixture pair and
    checks its `goodhart_fired` is True (a defect family fell while C2/C4/
    C6 stayed flat — the form-without-substance signature must fire).
    """
    ok = True

    try:
        positive = compute_compare(
            _COMPARE_FIXTURE_POSITIVE / "baseline", _COMPARE_FIXTURE_POSITIVE / "post"
        )
    except Exception as exc:  # noqa: BLE001 — self-test must report, not crash
        print(
            f"self-test FAIL: compare positive fixture raised unexpectedly: {exc!r}",
            file=sys.stderr,
        )
        return False

    if positive["per_criterion"] != _EXPECTED_POSITIVE_PER_CRITERION:
        print(
            f"self-test FAIL: compare positive per_criterion expected "
            f"{_EXPECTED_POSITIVE_PER_CRITERION!r}, got {positive['per_criterion']!r}",
            file=sys.stderr,
        )
        ok = False

    if positive["aggregate"] != _EXPECTED_POSITIVE_AGGREGATE:
        print(
            f"self-test FAIL: compare positive aggregate expected "
            f"{_EXPECTED_POSITIVE_AGGREGATE!r}, got {positive['aggregate']!r}",
            file=sys.stderr,
        )
        ok = False

    if positive["pass_split"] != _EXPECTED_POSITIVE_PASS_SPLIT:
        print(
            f"self-test FAIL: compare positive pass_split expected "
            f"{_EXPECTED_POSITIVE_PASS_SPLIT!r}, got {positive['pass_split']!r}",
            file=sys.stderr,
        )
        ok = False

    if positive["defects"] != _EXPECTED_POSITIVE_DEFECTS:
        print(
            f"self-test FAIL: compare positive defects expected "
            f"{_EXPECTED_POSITIVE_DEFECTS!r}, got {positive['defects']!r}",
            file=sys.stderr,
        )
        ok = False

    if positive["goodhart_fired"] is not False:
        print(
            f"self-test FAIL: compare positive goodhart_fired expected False, "
            f"got {positive['goodhart_fired']!r}",
            file=sys.stderr,
        )
        ok = False

    try:
        goodhart = compute_compare(
            _COMPARE_FIXTURE_GOODHART / "baseline", _COMPARE_FIXTURE_GOODHART / "post"
        )
    except Exception as exc:  # noqa: BLE001
        print(
            f"self-test FAIL: compare goodhart fixture raised unexpectedly: {exc!r}",
            file=sys.stderr,
        )
        return False

    if goodhart["goodhart_fired"] is not True:
        print(
            f"self-test FAIL: compare goodhart goodhart_fired expected True, "
            f"got {goodhart['goodhart_fired']!r}",
            file=sys.stderr,
        )
        ok = False

    # Extra structural counter-check (T-164-12 discipline): the goodhart
    # fixture's own defect families must have actually fallen and its C2/
    # C4/C6 bands must have actually stayed flat, so the True verdict above
    # is non-vacuous rather than an accident of a mis-built fixture.
    if not any(goodhart["defects"][f]["delta"] < 0 for f in ("untraced", "verdict", "chain")):
        print(
            "self-test FAIL: compare goodhart fixture defect deltas did not "
            "fall on any family — fixture does not exercise the condition "
            "it claims to",
            file=sys.stderr,
        )
        ok = False
    if any(
        goodhart["per_criterion"][_CRITERIA[idx]]["delta"] != 0
        for idx in _GOODHART_GUARD_INDICES
    ):
        print(
            "self-test FAIL: compare goodhart fixture C2/C4/C6 band deltas "
            "are not all zero — fixture does not exercise the condition it "
            "claims to",
            file=sys.stderr,
        )
        ok = False

    return ok


def self_test() -> int:
    """Run the offline deterministic self-test. Returns 0 on pass, 1 on failure.

    No `claude` process is spawned and no network is used. Task 1 (Plan 01)
    seeded two background sub-checks (catalog parse positive/negative) and
    Plan 01 Task 3 added a background tracer_path end-to-end offline chain
    check; both still run and gate `all_passed`, but — matching the
    catalog-check style — print only on failure, so they do not inflate the
    labelled result-line count below. Plan 02 Task 1 wired D-15 items 1-2
    (guardrail_a, guardrail_b); Task 2 wired D-15 items 3-4 (scoreline,
    blinding — which now also owns the judge-prompt-unblinded check a prior
    revision ran as its own background sub-check); Task 3 added D-15 items
    5-6 (tabulation, baseline). Plan 03 added item 7 (defects — the D-18
    mechanical defect detector, D-19 calibration). Plan 04 Task 1 adds item
    8 (run_layer — the `--run`/`--rejudge`/`--dry-run`/`--resume` composition
    and `write_run_manifest`). Phase 166 Plan 01 Task 2 adds item 9 (compare
    — the offline `--compare`/`--baseline` band/pass-split/defect-incidence
    delta tabulation and the computed Goodhart flag, D-04). Quick task
    260724-bq3 (FIX-CONTRACT-01, the offline §4/§6 traceability-detector
    correction) Task 1 adds item 10 (limitation1_chainlabels — a document's
    own bare single-letter §4 chain-label convention, family-size-guarded).
    Task 2 adds item 11 (limitation2_citationnorm — abbreviated/lowercase/
    pluralized chain-citation normalization, plus the bare-letter and
    bare-digit loose-match regression guards) and item 12
    (limitation3_extractionscope — the section-intro-label and restatement/
    corollary exclusions, plus the honesty-not-score anti-overreach guard
    proving a genuinely-uncited imperative recommendation is never silently
    excluded). Phase 182 Plan 01 (DETECT-01) adds item 13 (contract_pin — the
    D-18 contract-pin red-carry mechanism over a pre-registered fixture set
    naming DETECT-02/DETECT-03 as owners of the current inverted-detector
    mismatch); its PASSED line coexists with a carried red state reported on
    the `contract_pin:` summary line, printed on every run so the carry is
    never silent. Item 14 (GAP-5) parses the `### Conclusion C1:` heading
    form output-template.md §4 prescribes end-to-end. Item 15 (GAP-6) admits
    composition chain heads (`GT-5 + C6`, `C1 + C2`) plus their acyclicity/
    grounding checks. Item 16 (self-audit calibration) reconciles the
    Self-Audit Gate's claimed bands against the mechanical record. Item 17
    (ledger traceability, LEDGER-01) proves a closure ledger discharges the
    claims it quotes without its own rows being mined as extra claims. Item
    18 (schema widening) proves `read_defect_incidence` keeps parsing the
    committed defect-incidence TSVs by header name after column widening.
    Item 19 (v8.24.0 Phase 4, CAP-03) proves `_iter_capture_tool_calls`
    asserts the committed PR-P1 fixture's event inventory (1 Agent, 7
    WebFetch, 2 Read, 11 tool_result) in code, not only in the fixture's
    README. Item 20 (v8.24.0 Phase 4, CAP-01) proves
    `_extract_and_persist_analysis` leaves the extracted analysis beside its
    source `.jsonl`, with the completed-gate and both extraction guardrails
    carried through the new write path. Item 21 (v8.24.0 Phase 4, CAP-01
    closure) proves the `--single` CALL SITE — not the helper — refuses to
    reach `build_judge_packet` when the analysis was not persisted (CR-02):
    item 20's six controls all passed while the call site consuming that
    helper was defective, so this item asserts the consumer. Each of the
    twenty-one items prints its own labelled PASS/FAILED result line —
    exactly twenty-one such lines, always, per run (D-16: the
    fault-injection proof for each item is recorded in the corresponding
    plan's SUMMARY.md).
    """
    all_passed = True

    if not _self_test_catalog_parse_positive():
        all_passed = False
    if not _self_test_catalog_parse_negative():
        all_passed = False
    if not _self_test_tracer_path():
        all_passed = False

    # D-15 item 1: Extraction guardrail A (never the top-level result field).
    if not _selftest_guardrail_a():
        all_passed = False
        print("self-test: guardrail_a sub-check FAILED", file=sys.stderr)
    else:
        print("self-test: guardrail_a sub-check PASSED")

    # D-15 item 2: Extraction guardrail B (dispatch count, not tool_result count).
    if not _selftest_guardrail_b():
        all_passed = False
        print("self-test: guardrail_b sub-check FAILED", file=sys.stderr)
    else:
        print("self-test: guardrail_b sub-check PASSED")

    # D-15 item 3: Strict D-12/D-13 scoreline terminal-block parsing.
    if not _selftest_scoreline():
        all_passed = False
        print("self-test: scoreline sub-check FAILED", file=sys.stderr)
    else:
        print("self-test: scoreline sub-check PASSED")

    # D-15 item 4: D-05 blinding integrity + D-14 real-data cross-check.
    if not _selftest_blinding():
        all_passed = False
        print("self-test: blinding sub-check FAILED", file=sys.stderr)
    else:
        print("self-test: blinding sub-check PASSED")

    # D-15 item 5: tabulation arithmetic pinned to hand-checked real values.
    if not _selftest_tabulation():
        all_passed = False
        print("self-test: tabulation sub-check FAILED", file=sys.stderr)
    else:
        print("self-test: tabulation sub-check PASSED")

    # D-15 item 6: baseline-fixture integrity (frozen corpus + regenerated
    # baseline + post-fix baseline + truncated negative). Plan 04 Task 3
    # extended this item to also cover REGEN_DIR (D-15's own text: "now
    # covers the regenerated baseline directory as well as the frozen
    # corpus"); Phase 166 Plan 02 Task 3 extends it a third time to also
    # cover POSTFIX_DIR, the post-fix baseline (D-05) — coverage change
    # named here, not silent (Phase 163 D-02).
    if not _selftest_baseline():
        all_passed = False
        print("self-test: baseline sub-check FAILED", file=sys.stderr)
    else:
        print(
            f"self-test: baseline sub-check PASSED "
            f"({BASELINE_DIR.name}, {REGEN_DIR.name}, {POSTFIX_DIR.name})"
        )

    # D-18 item 7: mechanical defect detector (fixtures, structural edges,
    # and the pinned D-19 calibration vector).
    if not _selftest_defects():
        all_passed = False
        print("self-test: defects sub-check FAILED", file=sys.stderr)
    else:
        print("self-test: defects sub-check PASSED")

    # Item 8 (Plan 04 Task 1): the run layer — dry-run enumeration and
    # zero-side-effect proof, the rejudge byte-identity passthrough, the
    # manifest writer, and resume classification by PARSING (never grepping
    # api_error_status).
    if not _selftest_run_layer():
        all_passed = False
        print("self-test: run_layer sub-check FAILED", file=sys.stderr)
    else:
        print("self-test: run_layer sub-check PASSED")

    # Item 9 (Phase 166 Plan 01 Task 2, D-04): the offline `--compare`
    # band/pass-split/defect-incidence delta tabulation and the computed
    # Goodhart flag — the positive/ fixture pair proves the arithmetic
    # against hand-checked literals and a clear flag; the goodhart/ pair
    # proves the flag fires when it should.
    if not _selftest_compare():
        all_passed = False
        print("self-test: compare sub-check FAILED", file=sys.stderr)
    else:
        print("self-test: compare sub-check PASSED")

    # Item 10 (quick task 260724-bq3 Task 1, FIX-CONTRACT-01 limitation 1):
    # a document's own bare single-letter §4 chain-label convention (C1,
    # C2, ...) is recognized when used consistently, family-size-guarded
    # against a single incidental bold lead-in.
    if not _selftest_limitation1_chainlabels():
        all_passed = False
        print("self-test: limitation1_chainlabels sub-check FAILED", file=sys.stderr)
    else:
        print("self-test: limitation1_chainlabels sub-check PASSED")

    # Item 11 (quick task 260724-bq3 Task 2, FIX-CONTRACT-01 limitation 2):
    # abbreviated/lowercase-bolded/pluralized chain-citation normalization,
    # plus the bare-letter and bare-digit loose-match regression guards.
    if not _selftest_limitation2_citationnorm():
        all_passed = False
        print("self-test: limitation2_citationnorm sub-check FAILED", file=sys.stderr)
    else:
        print("self-test: limitation2_citationnorm sub-check PASSED")

    # Item 12 (quick task 260724-bq3 Task 2, FIX-CONTRACT-01 limitation 3):
    # the section-intro-label (b) and restatement/corollary (c) exclusions,
    # plus the honesty-not-score anti-overreach guard.
    if not _selftest_limitation3_extractionscope():
        all_passed = False
        print("self-test: limitation3_extractionscope sub-check FAILED", file=sys.stderr)
    else:
        print("self-test: limitation3_extractionscope sub-check PASSED")

    # Item 13 (Phase 182 Plan 01, DETECT-01): the D-18 contract-pin red-carry
    # mechanism — `_CONTRACT_FIXTURES` compared against `_DETECT01_PINNED_RED`.
    # Its PASSED line coexists with a carried red state reported on the
    # `contract_pin:` summary line printed above, never silently suppressed
    # (honesty-not-score, D-01).
    if not _selftest_contract_pin():
        all_passed = False
        print("self-test: contract_pin sub-check FAILED", file=sys.stderr)
    else:
        print("self-test: contract_pin sub-check PASSED")

    # Item 14 (GAP-5): the `### Conclusion C1:` heading form prescribed by
    # output-template.md §4 parses end-to-end. Pins ids -> blocks -> malformed
    # count, because the pre-fix failure was silently GREEN: zero ids made
    # `_chain_blocks` fall back to one whole-section block whose single
    # well-formed chain suppressed every malformed one in the same section.
    if not _selftest_gap5_conclusion_heading():
        all_passed = False
        print("self-test: gap5_conclusion_heading sub-check FAILED", file=sys.stderr)
    else:
        print("self-test: gap5_conclusion_heading sub-check PASSED")

    # Item 15 (GAP-6): composition chain heads (`GT-5 + C6`, `C1 + C2`) are
    # well-formed, the GT-only base case and the one-hop negative still hold,
    # and `_chain_dependency_defects` reports the cycles and ungrounded chains
    # that admitting chain refs makes possible.
    if not _selftest_gap6_composition_heads():
        all_passed = False
        print("self-test: gap6_composition_heads sub-check FAILED", file=sys.stderr)
    else:
        print("self-test: gap6_composition_heads sub-check PASSED")

    # Item 16 (self-audit calibration): the Self-Audit Gate's claimed bands are
    # reconciled against the mechanical record, so a Rigorous verdict cannot
    # sit unchallenged on top of measured defects. Four positive controls, four
    # anti-overreach controls (correct claim, conceded band, absent self-audit,
    # unstated band).
    if not _selftest_selfaudit_calibration():
        all_passed = False
        print("self-test: selfaudit_calibration sub-check FAILED", file=sys.stderr)
    else:
        print("self-test: selfaudit_calibration sub-check PASSED")

    # Item 17 (ledger traceability, LEDGER-01): a closure ledger discharges the
    # claims it quotes, and its own rows are not mined as extra claims. Three
    # positive/fault-injection controls, four anti-overreach controls (bogus
    # chain, sub-minimum fragment, unrelated fragment, long-claim absorption),
    # one fence-vs-filter discriminator, and a frozen-corpus movement pin.
    if not _selftest_ledger_traceability():
        all_passed = False
        print("self-test: ledger_traceability sub-check FAILED", file=sys.stderr)
    else:
        print("self-test: ledger_traceability sub-check PASSED")

    # Item 18 (schema widening): `read_defect_incidence` maps by header name,
    # so the twelve committed ten-column defect-incidence TSVs keep parsing
    # after three columns were appended — and still fails loudly on a ragged
    # row or a header missing a required flag column.
    if not _selftest_incidence_schema_compat():
        all_passed = False
        print("self-test: incidence_schema_compat sub-check FAILED", file=sys.stderr)
    else:
        print("self-test: incidence_schema_compat sub-check PASSED")

    # Item 19 (v8.24.0 Phase 4, CAP-03; Plan 04-04 gap closure): asserts
    # the committed PR-P1 fixture's event inventory (1 Agent, 7 WebFetch,
    # 2 Read, 11 tool_result) in code, not only in the fixture's README,
    # and that _iter_capture_tool_calls's dispatch_ids filter genuinely
    # distinguishes a dispatched subagent's tool calls from the parent
    # session's own. Thirteen controls: positive reader output, positive
    # event inventory, anti-masking, two anti-vacuity mutation controls
    # (rename, id-join strip), negative graceful degradation, guardrail
    # non-interference, positive dispatch_ids anti-masking, the
    # discrimination control (a synthesised parent-session Read — the
    # only control with teeth on the attribution axis), a cross-capture
    # weak leg, anti-over-rejection (with the README correction), WR-04's
    # unmapped-tool-name rejection, and the _capture_subagent_tool_calls
    # wrapper.
    if not _selftest_capture_tool_reader():
        all_passed = False
        print("self-test: capture_tool_reader sub-check FAILED", file=sys.stderr)
    else:
        print("self-test: capture_tool_reader sub-check PASSED")

    # Item 20 (v8.24.0 Phase 4, CAP-01): _extract_and_persist_analysis
    # leaves the extracted analysis beside its source .jsonl. Six controls:
    # positive round trip (PR-P1), positive second capture
    # (gen-single-dispatch), guardrail A carried through the wrapper,
    # negative not-completed-means-no-file (gen-internal-tools), and two
    # anti-masking controls (gen-stub-only, gen-multi-dispatch) proving a
    # guardrail failure is never swallowed into a None.
    if not _selftest_analysis_persistence():
        all_passed = False
        print("self-test: analysis_persistence sub-check FAILED", file=sys.stderr)
    else:
        print("self-test: analysis_persistence sub-check PASSED")

    # Item 21 (v8.24.0 Phase 4, CAP-01 closure): _selftest_single_refusal
    # proves the --single CALL SITE refuses to reach build_judge_packet
    # when the analysis was not persisted (CR-02). Five controls:
    # positive, negative refusal (no_terminal_result), anti-vacuity
    # reachability, call-site structure, and anti-masking guardrail
    # pass-through (multi-dispatch, stub-only).
    if not _selftest_single_refusal():
        all_passed = False
        print("self-test: single_refusal sub-check FAILED", file=sys.stderr)
    else:
        print("self-test: single_refusal sub-check PASSED")

    # Item 22 (GAP-8): a bold-labelled chain is not read as citing itself.
    # `_chain_ids`/`_chain_blocks` accept two label shapes; `_chain_head_refs`
    # guarded only the hash-led one, so PR-P1 run 4's `**C1 — …**` labels made
    # all eight of its chains self-cyclic AND ungrounded, every finding
    # artifact. Six controls: three positive, one anti-overreach forcing the
    # `idx == 0` restriction (a fully-bolded HEAD line also matches
    # `_CHAIN_BOLD_RE`), two non-vacuity holding the cycle, grounding and
    # heading-form checks in place.
    if not _selftest_gap8_bold_chain_labels():
        all_passed = False
        print("self-test: gap8_bold_chain_labels sub-check FAILED", file=sys.stderr)
    else:
        print("self-test: gap8_bold_chain_labels sub-check PASSED")

    # Item 23 (Phase 999.5): the persistence write refuses an unsafe
    # destination (WR-B: symlink, FROZEN-EVIDENCE path), and --probe
    # diagnoses a failed persist rather than ending a paid live run in a bare
    # traceback (WR-A). Thirteen controls: two on the symlink guard (positive
    # plus non-vacuity), two on the pathspec source (parse, fail-closed), one
    # driving the real frozen tree, one anti-overreach, four on the probe
    # helper's three outcomes, one anti-cosmetic status assertion, and one
    # call-site structure control in the shape item 21 control 4 established,
    # and one asserting --single's refusal asymmetry.
    if not _selftest_persistence_write_guards():
        all_passed = False
        print("self-test: persistence_write_guards sub-check FAILED", file=sys.stderr)
    else:
        print("self-test: persistence_write_guards sub-check PASSED")

    # Item 24 (Phase 11, CONTRACT-01/02/04): the emission rendering
    # contract's own worked examples in `output-template.md` §4 (chain
    # form), §6 (citation form) and the Verdict Vocabulary
    # (current-constraint expiry) are scored by the unmodified detectors
    # with the expected verdicts. Its fixtures are extracted from
    # `shared/spine/references/output-template.md` at self-test time, via
    # the same `_extract_contract_example` dispatcher DETECT-06 uses, so
    # the doc and the control cannot drift. `_chain_block_well_formed` is
    # called and never modified (D-02). See `_selftest_render_contract`'s
    # own docstring for the full, current enumeration of its lettered
    # controls — restating the count here a second time is stale by
    # construction (IN-01, `11-REVIEW.md`; the same reasoning CLAUDE.md
    # already applies to the gate inventory).
    if not _selftest_render_contract():
        all_passed = False
        print("self-test: render_contract sub-check FAILED", file=sys.stderr)
    else:
        print("self-test: render_contract sub-check PASSED")

    # Item 25 (Phase 13, CHAINHEAD-07): a sha256 pin over
    # `_chain_block_well_formed`'s source bytes, freezing the function under
    # CONTRACT-06. The digest is computed over the `.rstrip("\n")` form of
    # `inspect.getsource()`'s output, because that call always appends
    # exactly one trailing newline and the pinned value already recorded by
    # hand in `.planning/STATE.md`/`.planning/PROJECT.md` is only reproduced
    # once that newline is stripped. This is the gate CONTRACT-06's
    # `reproducible` tier points its `artifact_link` at — deleting this
    # sub-check silently downgrades that coverage claim back to unenforced.
    # See `_selftest_chain_detector_pin`'s own docstring for the full,
    # current enumeration of its lettered controls.
    if not _selftest_chain_detector_pin():
        all_passed = False
        print("self-test: chain_detector_pin sub-check FAILED", file=sys.stderr)
    else:
        print("self-test: chain_detector_pin sub-check PASSED")

    return 0 if all_passed else 1


# ---------------------------------------------------------------------------
# argparse
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Quality-measurement harness — promoted blind A/B rig (HARNESS-01)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument(
        "--self-test",
        dest="self_test",
        action="store_true",
        help="Run the offline deterministic self-test and exit (no claude invoked)",
    )
    p.add_argument(
        "--catalog",
        type=Path,
        default=None,
        help=f"Path to the prompt catalog (default when omitted: {DEFAULT_CATALOG})",
    )
    p.add_argument(
        "--out",
        "--out-dir",
        dest="out",
        type=Path,
        default=None,
        help="Output directory for .jsonl captures",
    )
    p.add_argument(
        "--repeat",
        type=int,
        default=DEFAULT_REPEAT,
        help=f"Per-prompt repeat count (default: {DEFAULT_REPEAT})",
    )
    p.add_argument(
        "--plugin-dir",
        dest="plugin_dir",
        type=Path,
        default=DEFAULT_PLUGIN_DIR,
        help=f"Path to the first-principles plugin dir (default: {DEFAULT_PLUGIN_DIR})",
    )
    p.add_argument(
        "--probe",
        nargs="?",
        const="Q-P1",
        default=None,
        metavar="ID",
        help=(
            "Dispatch exactly one live generation for the named catalog row "
            "(default: Q-P1) and write the capture to --out"
        ),
    )
    p.add_argument(
        "--single",
        type=Path,
        default=None,
        metavar="JSONL",
        help=(
            "Run the whole extract->blind->judge->parse->tabulate path for "
            "one already-captured generation .jsonl and print one tabulated "
            "row. Dispatches exactly one live judge invocation."
        ),
    )
    p.add_argument(
        "--detect-defects",
        dest="detect_defects",
        type=Path,
        default=None,
        metavar="ANALYSES_DIR",
        help=(
            "Run the D-18 mechanical defect detector over a directory of "
            "analysis .md files and write the ten-column TSV to --out. "
            "Fully offline — no `claude` invoked."
        ),
    )
    p.add_argument(
        "--compare",
        type=Path,
        default=None,
        metavar="POST_DIR",
        help=(
            "Diff a post-fix run directory against --baseline and print the "
            "band/pass-split/defect-incidence deltas plus a computed "
            "GOODHART_FLAG line (D-04). Fully offline — no `claude` "
            "invoked. Requires --baseline."
        ),
    )
    p.add_argument(
        "--baseline",
        type=Path,
        default=None,
        metavar="BASE_DIR",
        help="Baseline run directory for --compare (offline, required with --compare).",
    )
    p.add_argument(
        "--run",
        action="store_true",
        help=(
            "Run the full generate->extract->blind->judge->score->tabulate->"
            "detect chain over --catalog, writing scorelines.tsv, "
            "defect-incidence.tsv, a blinding key, and a manifest under --out."
        ),
    )
    p.add_argument(
        "--rejudge",
        type=Path,
        default=None,
        metavar="ANALYSES_DIR",
        help=(
            "Re-judge an existing directory of analysis .md files through "
            "the same judge channel, with a byte-unchanged packet "
            "passthrough (T-164-19), writing rejudge-scorelines.tsv under "
            "--out. Composes with --run."
        ),
    )
    p.add_argument(
        "--dry-run",
        dest="dry_run",
        action="store_true",
        help=(
            "Enumerate every invocation --run/--rejudge would dispatch and a "
            "total count; spends nothing, makes no subprocess call, and "
            "creates no capture file."
        ),
    )
    p.add_argument(
        "--resume",
        action="store_true",
        help=(
            "Continue into an existing --out directory, skipping every "
            "invocation whose destination already holds a completed record "
            "and re-dispatching only those that are absent or hold a "
            "transport-error or rate-limit stub."
        ),
    )
    return p


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    """Entry point. Returns exit code (0=pass, 1=fail, 2=usage/env error)."""
    parser = build_parser()
    args = parser.parse_args(argv)

    # --self-test MUST return before any environment guard or live path (D-16).
    if args.self_test:
        sys.exit(self_test())

    # --dry-run MUST be checked before any live-path branch, and its own body
    # (run_dry_run) must never call a function that reaches _run_prompt_to —
    # a structural guard, not a conditional inside the transport function
    # (see Fault injection L in _selftest_run_layer).
    if args.dry_run:
        if not args.out:
            parser.error("--out is required with --dry-run")
        if not (args.run or args.rejudge):
            parser.error("--dry-run requires --run and/or --rejudge")
        return run_dry_run(args)

    # --compare MUST be checked before any live-path branch and calls no
    # function reaching `_run_prompt_to` — same offline class as
    # --detect-defects, mirrored here so it sits ahead of
    # `_ensure_claude_available()` entirely (D-04).
    if args.compare is not None:
        if not args.baseline:
            parser.error("--baseline is required with --compare")
        return run_compare(args.baseline, args.compare)

    if args.run or args.rejudge:
        _ensure_claude_available()
        if not args.out:
            parser.error("--out is required with --run/--rejudge")
        out_dir = args.out
        out_dir.mkdir(parents=True, exist_ok=True)
        manifest_rows: list[dict] = []

        if args.run:
            catalog_path = args.catalog or DEFAULT_CATALOG
            prompts = _read_quality_catalog(catalog_path)
            analyses = run_generation_arm(
                prompts,
                args.repeat,
                out_dir,
                args.plugin_dir,
                manifest_rows,
                resume=args.resume,
            )
            fresh_items = sorted(analyses.items())
            # D-05 Assumption A3: plugin_dir=None omits --plugin-dir entirely
            # from the judge invocation, which must have no agent-dispatch
            # surface.
            fresh_rows = run_judging_arm(
                fresh_items,
                out_dir,
                "judgments",
                "judge",
                manifest_rows,
                out_dir / "blinding-key.tsv",
                plugin_dir=None,
                resume=args.resume,
            )
            write_run_scorelines(fresh_rows, out_dir / "scorelines.tsv")
            run_detect_defects(out_dir / "analyses", out_dir / "defect-incidence.tsv")

        if args.rejudge:
            rejudge_items = [
                (f.stem, f) for f in sorted(Path(args.rejudge).glob("*.md"))
            ]
            rejudge_rows = run_judging_arm(
                rejudge_items,
                out_dir,
                "rejudge-judgments",
                "rejudge",
                manifest_rows,
                out_dir / "rejudge-blinding-key.tsv",
                plugin_dir=None,
                resume=args.resume,
            )
            write_run_scorelines(rejudge_rows, out_dir / "rejudge-scorelines.tsv")

        write_run_manifest(manifest_rows, out_dir / "manifest.tsv")
        print(
            f"Run complete: {len(manifest_rows)} invocations recorded in "
            f"{out_dir / 'manifest.tsv'}"
        )
        return 0

    if args.probe is not None:
        _ensure_claude_available()
        catalog_path = args.catalog or DEFAULT_CATALOG
        if not args.out:
            parser.error("--out is required with --probe")
        prompts = _read_quality_catalog(catalog_path)
        row = next((p for p in prompts if p.id == args.probe), None)
        if row is None:
            parser.error(f"--probe {args.probe!r} not found in catalog {catalog_path}")
            return 2  # unreachable — parser.error exits
        args.out.mkdir(parents=True, exist_ok=True)
        out_path = args.out / f"{row.id}.jsonl"
        wrapped_prompt = _wrap_for_bypass(row.text)
        _run_prompt_to(wrapped_prompt, out_path, plugin_dir=args.plugin_dir)
        print(f"Probe capture written: {out_path}")
        # Phase 999.5 (WR-A): the decision lives in a helper so it can be
        # self-tested without a live `claude`; this block only routes the
        # message to the stream the status code implies.
        _analysis_path, probe_message, probe_status = _persist_or_diagnose_analysis(
            out_path, subagent_type="first-principles:first-principles"
        )
        print(probe_message, file=sys.stderr if probe_status else sys.stdout)
        return probe_status

    if args.single is not None:
        _ensure_claude_available()
        analysis_path, refusal = _persist_or_refuse_analysis(
            args.single, subagent_type="first-principles:first-principles"
        )
        if analysis_path is None:
            print(refusal, file=sys.stderr)
            return 1
        print(f"Analysis written: {analysis_path}")
        analysis = analysis_path.read_text(encoding="utf-8")
        packet_dir = build_judge_packet(analysis)
        judge_capture = packet_dir / "judge-capture.jsonl"
        # D-05 Assumption A3: plugin_dir=None omits --plugin-dir entirely, so
        # the judge invocation has no agent-dispatch surface.
        _run_prompt_to(JUDGE_PROMPT, judge_capture, plugin_dir=None, cwd=packet_dir)
        judge_text = extract_judge_verdict(judge_capture)
        # The rationale is evidence, never a score (D-12) — captured verbatim
        # to a sidecar file alongside the parsed row.
        (packet_dir / "rationale.md").write_text(judge_text, encoding="utf-8")
        row = _build_scoreline_row(packet_id=args.single.stem, judge_text=judge_text)
        print(tabulate_rows([row]))
        print(f"Judge packet dir: {packet_dir}", file=sys.stderr)
        return 0

    if args.detect_defects is not None:
        if not args.out:
            parser.error("--out is required with --detect-defects")
        run_detect_defects(args.detect_defects, args.out)
        print(f"Defect-detection TSV written: {args.out}")
        return 0

    parser.error(
        "no action specified — pass --self-test, --probe, --single, "
        "--detect-defects, --compare, --run, --rejudge, or --dry-run"
    )
    return 2  # unreachable — parser.error exits


if __name__ == "__main__":
    sys.exit(main())
