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
import io
import json
import random
import re
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
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
    """Negative: a catalog with the wrong header columns must raise."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(_MALFORMED_CATALOG_FIXTURE)
        tmp_path = Path(tmp.name)
    try:
        try:
            _read_quality_catalog(tmp_path)
        except ValueError:
            return True
        except Exception as exc:  # noqa: BLE001
            print(
                f"self-test FAIL: catalog_parse_negative raised the wrong "
                f"exception type: {exc!r}",
                file=sys.stderr,
            )
            return False
        print(
            "self-test FAIL: catalog_parse_negative did not raise on a "
            "malformed header",
            file=sys.stderr,
        )
        return False
    finally:
        try:
            tmp_path.unlink()
        except OSError:
            pass


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


_VERDICT_VOCAB = {"accept", "challenge", "discard"}


def _verdict_conforms(cell: str) -> bool:
    """A Verdict cell conforms after stripping emphasis, whitespace, and trailing punctuation."""
    s = cell.strip()
    s = re.sub(r"^[*_]+", "", s)
    s = re.sub(r"[*_]+$", "", s)
    s = s.strip().rstrip(".,;:!").strip()
    return s.lower() in _VERDICT_VOCAB


# Chain-label families the frozen corpus actually uses: a two-letter prefix
# followed by a hyphen and a number (DC-1), and the word "Chain" followed by
# a letter or a number (Chain A, Chain 1).
_CHAIN_LABEL_PATTERN = r"(?:[A-Z]{2}-\d+|Chain\s+[A-Za-z0-9]+)"

# Headed form: a heading line whose text begins with the label followed by a
# separator (colon, em dash, en dash, or hyphen).
_CHAIN_HEADING_RE = re.compile(
    r"^#{1,6}[ \t]*(?P<label>" + _CHAIN_LABEL_PATTERN + r")[ \t]*[:—–-]",
    re.MULTILINE,
)
# Bolded lead-in form: a line beginning with bold markers whose text begins
# with the label (no heading hashes).
_CHAIN_BOLD_RE = re.compile(
    r"^\*\*(?P<label>" + _CHAIN_LABEL_PATTERN + r")\b[^\n]*?\*\*",
    re.MULTILINE,
)


def _iter_chain_id_matches(section4: str) -> list[re.Match]:
    matches = list(_CHAIN_HEADING_RE.finditer(section4)) + list(
        _CHAIN_BOLD_RE.finditer(section4)
    )
    matches.sort(key=lambda m: m.start())
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
# are accepted. Matched per physical line — the prescribed form names one
# line, not a claim spread across several.
_ARROW = r"(?:→|->)"
_CHAIN_FORM_LINE_RE = re.compile(
    r"GT-\d+\??(?:[ \t]*\([^)\n]*\))?"
    r"(?:[ \t]*\+[ \t]*GT-\d+\??(?:[ \t]*\([^)\n]*\))?)*"
    r"[ \t]*" + _ARROW + r"[ \t]*\S[^\n]*?"
    r"[ \t]*" + _ARROW + r"[ \t]*\S[^\n]*"
)


def _chain_block_well_formed(block: str) -> bool:
    return any(_CHAIN_FORM_LINE_RE.search(line) for line in block.splitlines())


# Bold lead-in ending in a colon (e.g. "**Key insight:** ..."); the colon
# must sit immediately before the closing bold markers, distinguishing a
# labelled claim from a bold phrase (e.g. "**Confidence: HIGH**") whose
# colon sits mid-span.
_BOLD_LEADIN_COLON_RE = re.compile(r"^\s*\*\*([^*\n]+:)\*\*")
_LIST_ITEM_RE = re.compile(r"^\s*(?:\d+[.)]|[-*])\s+(.+)$")

_GT_MENTION_RE = re.compile(r"GT-\d+\??")


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


def _conclusion_claims(section6: str) -> list[str]:
    """Return the assertive claims in section 6: bold colon-lead-ins and list items.

    Returns the claim text (not just a count) so the detector output can be
    audited.
    """
    claims: list[str] = []
    for line in section6.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        m_bold = _BOLD_LEADIN_COLON_RE.match(stripped)
        if m_bold:
            if _is_assertive_claim(stripped):
                claims.append(stripped)
            continue
        m_list = _LIST_ITEM_RE.match(stripped)
        if m_list:
            candidate = m_list.group(1).strip()
            if _is_assertive_claim(candidate):
                claims.append(candidate)
    return claims


def _claim_is_traced(claim_text: str, chain_ids: list[str], chain_blocks: list[str]) -> bool:
    """A claim is traced if it names a chain identifier, or names >=2 GT ids
    that also appear together inside a single chain block (D-20)."""
    if any(cid in claim_text for cid in chain_ids):
        return True
    gt_mentions = {m.group(0).rstrip("?") for m in _GT_MENTION_RE.finditer(claim_text)}
    if len(gt_mentions) >= 2:
        for block in chain_blocks:
            block_gts = {m.group(0).rstrip("?") for m in _GT_MENTION_RE.finditer(block)}
            if gt_mentions <= block_gts:
                return True
    return False


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
)


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

    claims = _conclusion_claims(section6)
    untraced = [c for c in claims if not _claim_is_traced(c, chain_ids, blocks)]

    return {
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
    }


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
_CALIBRATION_ANALYSIS_ORDER = (
    "condA-P1",
    "condA-P2",
    "condA-P3",
    "condB-P1",
    "condB-P2",
    "condB-P3",
)
_CALIBRATION_UNTRACED_FLAGS = [1, 1, 1, 1, 1, 1]
_CALIBRATION_VERDICT_FLAGS = [1, 1, 1, 1, 1, 1]
_CALIBRATION_CHAIN_FLAGS = [1, 1, 1, 1, 1, 1]


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

    Reads the ten-column `_DEFECT_RECORD_FIELDS` shape (header row plus one
    data row per analysis). Skips the header row when it is the first line
    (`cells[0] == "analysis_id"`) — a real analysis id is never literally
    that string.

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

    untraced = 0
    verdict = 0
    chain = 0
    n = 0
    text = path.read_text(encoding="utf-8")
    for lineno, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        cells = line.split("\t")
        if lineno == 1 and cells[0] == "analysis_id":
            continue
        if len(cells) != len(_DEFECT_RECORD_FIELDS):
            raise ValueError(
                f"{path}:{lineno}: expected {len(_DEFECT_RECORD_FIELDS)} "
                f"tab-separated columns, got {len(cells)}: {cells!r}"
            )
        record = dict(zip(_DEFECT_RECORD_FIELDS, cells))
        untraced += int(record["untraced_flag"])
        verdict += int(record["verdict_flag"])
        chain += int(record["chain_flag"])
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
    delta tabulation and the computed Goodhart flag, D-04). Each of the nine
    items prints its own labelled PASS/FAILED result line — exactly nine
    such lines, always, per run (D-16: the fault-injection proof for each
    item is recorded in the corresponding plan's SUMMARY.md).
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
        return 0

    if args.single is not None:
        _ensure_claude_available()
        analysis = extract_agent_analysis(
            args.single, subagent_type="first-principles:first-principles"
        )
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
