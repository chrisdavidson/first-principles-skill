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


def _slice_sections(text: str) -> dict[int, str]:
    """Locate the six numbered output-template sections; return num -> body text.

    Content before section 1 (preamble) is discarded. A section's body runs
    from its heading to the next resolved section heading, or — for section
    6 — to the next heading at the same or shallower hash depth (an
    appendix), or end of file. Raises `SectionResolutionError` if the six
    section numbers do not resolve, in ascending order, with no gaps —
    exactly the six shapes required, never a partial or out-of-order read.
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
            # Section 6: stop at the next heading of depth <= this one
            # (an appendix), else end of file.
            body_end = len(text)
            for hm in re.finditer(r"^(#{1,3})[ \t]+", text[body_start:], re.MULTILINE):
                if len(hm.group(1)) <= depth:
                    body_end = body_start + hm.start()
                    break
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
_FENCE_RE = re.compile(r"^\s*(?:```|~~~)")

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

    A ledger line is any line that BOTH quotes a span and cites a real
    chain id. Both halves are load-bearing: a quote citing nothing traces
    nothing, and a chain citation with no quote names which chain but not
    which claim. An id cited but absent from section 4 is not a chain id
    and yields no fragment — so a ledger cannot invent its own authority.
    """
    fragments: list[str] = []
    for line in section6.splitlines():
        if not _cites_chain(line, chain_ids):
            continue
        fragments.extend(m.group(1) for m in _LEDGER_QUOTE_RE.finditer(line))
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
    in_fence = False
    for line in section6.splitlines():
        stripped = line.strip()
        # LEDGER-01: a fenced block is verbatim structural content — a
        # closure ledger, a formula, a captured snippet — not section-6
        # prose. Mining it for claims counted a ledger's own rows as ten
        # additional claims on the live PR-P1 run.
        if _FENCE_RE.match(stripped):
            in_fence = not in_fence
            continue
        if in_fence or not stripped:
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
_RENDER_FIXTURE_SHAPE: dict[str, tuple[str, ...]] = {
    "R-CHAIN-CONFORMING": ("GT-1", "GT-6", "actual compute\n→ sustained"),
    "R-CHAIN-WRAPPED": ("GT-1", "GT-6", "\n  once idle-time billing"),
    "R-CHAIN-NUMBERED": ("GT-1", "GT-6", "\n2. "),
    "R-CITE-INLINE": ("(chain C1)",),
    "R-CITE-LEDGER": ("C1", '"'),
    "R-CITE-NONE": ("Fargate",),
    "R-VERDICT-EXPIRY": ("expires at",),
    "R-VERDICT-EXPIRY-BAD": ("expires at",),
}

# Substrings the extracted text for a fixture id must NOT contain.
# `R-CITE-NONE`'s entire point is that it names no chain; an extraction
# that accidentally captured a neighbouring line carrying `C1` would
# otherwise score `False` for the wrong reason.
_RENDER_FIXTURE_FORBIDDEN: dict[str, tuple[str, ...]] = {
    "R-CITE-NONE": ("C1",),
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


def _render_contract_fixtures() -> tuple[dict[str, str], list[str]]:
    """Read all eight Phase 11 rendering-contract fixtures from the shipped
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
_RENDER_RULE_SURFACES: tuple[str, ...] = (
    "shared/spine/references/output-template.md",
    "shared/spine/SKILL-body.md",
    "shared/spine/references/validation-rubric.md",
)

# Each value is a SHARED VERBATIM LITERAL, present byte for byte in BOTH
# `_RENDER_RULE_SURFACES` entries. Reconciliation is implemented as identity
# of this literal on both surfaces specifically so that contradicting one
# surface without the other is unexpressible without deleting the literal
# from it — copying the "shared bytes, not a restated paraphrase" discipline
# that keeps CONTRACT-05's head form from drifting silently.
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
    # R4: the citation rule (CONTRACT-02 reconciliation).
    "R4": (
        "Every Conclusion-section claim either names the chain that "
        "established it inline — `(chain C1)` — or is discharged by a "
        "§6→§4 closure ledger row that quotes the claim and names its "
        "chain. A claim doing neither is cut, not softened."
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
_RENDER_SURFACE_REQUIRED_RULES: dict[str, tuple[str, ...]] = {
    "shared/spine/references/output-template.md": (
        "R1", "R2", "R3", "R4", "R5", "R6",
    ),
    "shared/spine/SKILL-body.md": (
        "R1", "R2", "R3", "R4", "R5", "R6",
    ),
    "shared/spine/references/validation-rubric.md": ("R1", "R6"),
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

# The two doc-side QUAL-01 gate-description rows that must state the new
# coverage — see control (m) and Task 3.
_QUAL01_DOC_ROWS: tuple[str, ...] = (
    "CLAUDE.md",
    "docs/ARCHITECTURE.md",
)

# The tokens each registered `| QUAL-01 |` table row must carry (plan
# 11-10, WR-04/IN-02/IN-03). The second token is what makes the row's
# disclosure of the third scanned surface (validation-rubric.md)
# load-bearing rather than decorative — a row could name "emission
# rendering contract" while still describing only the two-surface world
# CR-01 closed.
_QUAL01_DOC_ROW_TOKENS: tuple[str, ...] = (
    "emission rendering contract",
    "validation-rubric.md",
)


@dataclass(frozen=True)
class _RenderRegistrySnapshot:
    """A by-value snapshot of the registries the rendering-contract
    mechanism depends on — one field per entry of
    `_RENDER_REGISTRY_FIELDS` (eleven today, ten registries: the
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
    itself — and `_RENDER_RULE_LITERAL_DIGEST`, a pin compared inside the
    `literals` arm. Nothing makes this scope self-maintaining: a NEW
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
)

# A `sha256:<hex>` pin over `_RENDER_RULE_LITERALS`, recomputed as
# `"\x00".join(f"{k}={v}" for k, v in sorted(literals.items()))` encoded
# UTF-8. Recompute ONLY with an explicit, reviewed contract change — a
# diff to this constant should always accompany a diff to the literals it
# pins. It sits beside the clause arm in `_render_registry_lock_problems`
# because the clause arm only proves ONE required substring survived per
# literal; the digest arm catches every other text change, including one
# that keeps the required clause and appends a permission the clause never
# excluded.
_RENDER_RULE_LITERAL_DIGEST = (
    "sha256:90093fc609847566fd55a60b861fe226315ede2c8365d15567e81fc3159275e3"
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
        "R-VERDICT-EXPIRY", "R-VERDICT-EXPIRY-BAD",
    ]

    # The AUTHORITATIVE extraction arm: all FOUR columns of every row, not
    # the `row[0]` id projection the snapshot used to carry (WR-03,
    # `11-REVIEW-gap-closure.md`). `source_file`, `habitat_mode` and
    # `anchor` are what determine WHAT THE GATE ACTUALLY READS, and they
    # sat outside the lock entirely: rebinding all eight rows'
    # `source_file` to `first-principles/agents/references/` — the
    # GENERATED copy — left the self-test GREEN while both `| QUAL-01 |`
    # doc rows told the reader the gate reads the canonical `shared/`
    # source. The id-only arm below is kept for its narrower failure
    # message and for its own (h2) cases, not as the authority.
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
        # ALL EIGHT ids carry a FULL-VALUE lock, not just a key-set lock.
        # The three R-CHAIN-* ids were promoted first (IN-04,
        # `11-REVIEW.md`); the five others followed at WR-01
        # (`11-REVIEW-gap-closure.md`), which reproduced setting each of
        # their needle tuples to `()` with every key still present and the
        # self-test still GREEN — that silently disables the mode-2 shape
        # guard for five of the eight fixtures, so an extraction that
        # returned a neighbouring block scores `False` for the wrong reason
        # and passes vacuously. There is no reason to keep two tiers: a
        # needle tuple is the whole content of the guard for its fixture.
        expected_fixture_shape = {
            "R-CHAIN-CONFORMING": ("GT-1", "GT-6", "actual compute\n→ sustained"),
            "R-CHAIN-WRAPPED": ("GT-1", "GT-6", "\n  once idle-time billing"),
            "R-CHAIN-NUMBERED": ("GT-1", "GT-6", "\n2. "),
            "R-CITE-INLINE": ("(chain C1)",),
            "R-CITE-LEDGER": ("C1", '"'),
            "R-CITE-NONE": ("Fargate",),
            "R-VERDICT-EXPIRY": ("expires at",),
            "R-VERDICT-EXPIRY-BAD": ("expires at",),
        }
        for fixture_id, expected_shape in expected_fixture_shape.items():
            actual_shape = snapshot.fixture_shape.get(fixture_id)
            if actual_shape != expected_shape:
                problems.append(
                    f"fixture_shape: {fixture_id} shape {actual_shape!r} "
                    f"!= expected discriminating shape {expected_shape!r}"
                )
    checked.add("fixture_shape")

    expected_forbidden = {"R-CITE-NONE": ("C1",)}
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
    )
    if snapshot.surfaces != expected_surfaces:
        problems.append(
            f"surfaces: {snapshot.surfaces!r} != expected "
            f"{expected_surfaces!r}"
        )
    checked.add("surfaces")

    expected_required_rules = {
        "shared/spine/references/output-template.md": (
            "R1", "R2", "R3", "R4", "R5", "R6",
        ),
        "shared/spine/SKILL-body.md": (
            "R1", "R2", "R3", "R4", "R5", "R6",
        ),
        "shared/spine/references/validation-rubric.md": ("R1", "R6"),
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

    # `literals` carries TWO arms under the single field name — both
    # required, both counted under "literals" so neither can be dropped
    # while the field still reads as covered.
    expected_literal_clauses = {
        "R1": "a hop is never broken across physical lines",
        "R2": "it is two hops — split it",
        "R3": "do not wrap it",
        "R4": "A claim doing neither is cut, not softened",
        "R5": "GT-1 ([brief fact label]) + GT-6",
        "R6": "a hop is split rather than continued on a second line",
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

    literal_digest = "sha256:" + hashlib.sha256(
        "\x00".join(
            f"{k}={v}" for k, v in sorted(snapshot.literals.items())
        ).encode("utf-8")
    ).hexdigest()
    if literal_digest != _RENDER_RULE_LITERAL_DIGEST:
        problems.append(
            f"literals: digest {literal_digest!r} != pinned "
            f"{_RENDER_RULE_LITERAL_DIGEST!r}"
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

    Controls (a)-(b) pin the eight measured verdicts. Control (c) pins
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
    not pass (b)/(e) by accident. Control (p), added by plan 11-09 (gap
    2's second half), is the CONSUMPTION FLOOR: `_get` records every id it
    is asked for, and the floor asserts that set against a locked eight-id
    set written inline — plus that `fixtures` matches the same locked set
    whenever `problems` is empty (the exact condition CR-02's reproduction
    left silent), plus that every locked id is either in `fixtures` or
    named in a reported problem. A fixture that is extracted but never
    requested, or requested but never scored or reported, now fails by
    name instead of being silently skipped by controls (b)-(f)'s
    `is not None` guards. Control (q), also added by plan 11-09, drives
    `_render_fixture_accounting_problems()` — the mode 3 replacement in
    `_render_contract_fixtures()` — directly with a clean case, a
    duplicated-id case and a count-mismatch case, proving WR-06's
    unreachable membership check has been replaced by something that can
    actually fire.

    Controls (h)-(l) close Case A (CONTRACT-03) and pin the reconciled
    multi-hop head form (CONTRACT-05) across THREE canonical surfaces, per
    D-04: a rule shipped uncontrolled lands in the exact defect class
    PROJECT.md's through-line names — a form stated in more places than
    anything checks. Plan 11-07 (CR-01, `11-VERIFICATION.md` gap 1) added
    the third surface, `shared/spine/references/validation-rubric.md`: it
    is canonical because it is the rubric the agent scores its own
    emission against at Phase 5 Criterion 4, and it shipped for one
    milestone stating one of this gate's own enumerated contradiction
    phrasings (`too long for one line wraps`) while sitting outside the
    gate's scan scope — CR-01's fix note is what closes that gap.

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
    both `_QUAL01_DOC_ROW_TOKENS` entries independently, reporting one
    problem per missing token by name rather than a single all-or-nothing
    verdict. `_QUAL01_DOC_ROW_TOKENS` is itself a ninth locked
    `_RenderRegistrySnapshot` field, so dropping either required token
    from the tuple is caught by control (h2)'s anti-masking floor even if
    every doc row still carries it. A NEGATIVE-CASE COUNT FLOOR derives
    the expected 4 (2 doc rows x 2 tokens) from the two registries rather
    than restating it.

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

    # (b) Chain verdicts.
    if conforming is not None and not _chain_block_well_formed(conforming):
        _fail(
            "(b) R-CHAIN-CONFORMING (doc label 'Conforming — head, then "
            "one hop per line:') scored malformed, expected well-formed"
        )
    if wrapped is not None and _chain_block_well_formed(wrapped):
        _fail(
            "(b) R-CHAIN-WRAPPED (doc label 'Non-conforming — a hop "
            "broken across physical lines:') scored well-formed, "
            "expected malformed"
        )
    if numbered is not None and _chain_block_well_formed(numbered):
        _fail(
            "(b) R-CHAIN-NUMBERED (doc label 'Non-conforming — the same "
            "hops rendered as a numbered list:') scored well-formed, "
            "expected malformed"
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
    if verdict_expiry is not None and not _verdict_conforms(verdict_expiry):
        _fail(
            "(e) R-VERDICT-EXPIRY (doc label 'Conforming — a current "
            "constraint recording its expiry:') scored non-conforming, "
            "expected conforming"
        )
    if verdict_bad is not None and _verdict_conforms(verdict_bad):
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
        if not _claim_is_traced(cite_inline, ["C1"], [conforming]):
            _fail(
                "(f) R-CITE-INLINE (doc label 'Conforming — inline chain "
                "citation:') scored untraced, expected traced"
            )
    if conforming is not None and cite_none is not None:
        if _claim_is_traced(cite_none, ["C1"], [conforming]):
            _fail(
                "(f) R-CITE-NONE (doc label 'Non-conforming — a claim "
                "naming no chain and quoted by no ledger row:') scored "
                "traced with no ledger fragments, expected untraced"
            )
    if cite_ledger is not None:
        ledger_fragments = _closure_ledger_fragments(cite_ledger, ["C1"])
        if not ledger_fragments:
            _fail(
                "(f) R-CITE-LEDGER (doc label 'Conforming — closure-ledger "
                "row:') yielded zero closure-ledger fragments"
            )
        elif conforming is not None and cite_none is not None:
            if not _claim_is_traced(
                cite_none, ["C1"], [conforming], ledger_fragments
            ):
                _fail(
                    "(f) R-CITE-NONE with R-CITE-LEDGER's fragments still "
                    "scored untraced — the ledger row does not discharge "
                    "the claim it quotes"
                )

    # (g) NON-VACUITY: the module's own long-standing base cases still
    #     hold from outside this item. A control that scored everything
    #     `True`, or everything `False`, would pass (b) and (e) only by
    #     accident.
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

    # (p) CONSUMPTION FLOOR. Plan 11-09, gap 2's second half
    #     (`11-VERIFICATION.md`): controls (b)-(f) above are all guarded by
    #     `is not None`, so a fixture id absent from `fixtures` is silently
    #     SKIPPED rather than reported — this is exactly the path the
    #     verifier's CR-02 reproduction relied on once
    #     `_RENDER_CONTRACT_EXTRACTION_TABLE` was emptied: `problems` stayed
    #     empty, every `_get(...)` returned `None`, and the sub-check still
    #     printed PASSED. The locked eight-id set below is written INLINE,
    #     matching plan 11-08's (h) lock literal, never read off a module
    #     constant, so this floor cannot be made tautologically green by
    #     comparing a constant against itself. This control proves every
    #     locked fixture was requested and either scored or reported; it
    #     does NOT prove the verdict each control asserted is the right
    #     verdict — that is controls (b)-(f)'s job, and control (g)'s
    #     non-vacuity pair is what keeps those honest.
    render_locked_fixture_ids = {
        "R-CHAIN-CONFORMING", "R-CHAIN-NUMBERED", "R-CHAIN-WRAPPED",
        "R-CITE-INLINE", "R-CITE-LEDGER", "R-CITE-NONE",
        "R-VERDICT-EXPIRY", "R-VERDICT-EXPIRY-BAD",
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
    # arm 2 above skipped by its own `if not problems` guard.
    render_unaccounted_fixture_ids = sorted(
        fid
        for fid in render_locked_fixture_ids
        if fid not in fixtures
        and not _render_fixture_id_accounted(fid, problems)
    )
    if render_unaccounted_fixture_ids:
        _fail(
            f"(p) CONSUMPTION FLOOR: fixture id(s) "
            f"{render_unaccounted_fixture_ids!r} are neither in fixtures "
            f"nor named in a reported problem — never scored, never "
            f"reported"
        )

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
    #     rule is deleted from any of the three canonical surfaces today,
    #     or if any surface currently contradicts the no-wrap rule.
    render_reads, render_read_problems = _read_render_surfaces()
    for problem in render_read_problems:
        _fail(f"(i) POSITIVE: could not read a registered surface: {problem}")
    for read in render_reads:
        for problem in _render_rule_report(read):
            _fail(f"(i) POSITIVE: {problem}")

    # (j) COVERAGE FLOOR. Phase 10 block (l)'s corrected shape: derived
    #     from the relpaths the read loop actually RETURNED, never from a
    #     re-glob or a restated list. A surface the read loop declined to
    #     open is named at (i) above rather than silently reducing
    #     coverage to whatever was read; this floor additionally proves no
    #     registered surface silently dropped out of the returned records.
    #     Compares a three-element set as of plan 11-07's rubric surface.
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
    #     _RENDER_SURFACE_REQUIRED_RULES.values()), 14 today
    #     (6 + 6 + 2), so shrinking the mapping fails the floor rather
    #     than silently reducing coverage.
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
    expected_missing_case_count = 14
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

    # NEGATIVE-CASE COUNT FLOOR: 2 doc rows x 2 required tokens = 4 cases
    # above, derived from the two registries rather than restated, and
    # floored against an inline expected total of 4 — a doc row or a
    # required token silently dropped shrinks the derived count.
    qual01_negative_case_count = len(_QUAL01_DOC_ROWS) * len(
        _QUAL01_DOC_ROW_TOKENS
    )
    if qual01_negative_case_count != 4:
        _fail(
            f"(m) NEGATIVE-CASE COUNT FLOOR: derived "
            f"{qual01_negative_case_count} (file, token) case(s) from "
            f"{len(_QUAL01_DOC_ROWS)} doc row(s) x "
            f"{len(_QUAL01_DOC_ROW_TOKENS)} token(s) != expected 4"
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
    base = REPO_ROOT / "tests" / "quality-baseline-v8.7" / "analyses"
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
