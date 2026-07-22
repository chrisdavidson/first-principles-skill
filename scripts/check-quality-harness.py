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
`--self-test`.** **Task 3 scope (this commit): the extraction pipeline
(`extract_agent_analysis`, `extract_judge_verdict`), the sealed judge packet
builder, the judge prompt and scoreline parser, PASS/FAIL derivation, one-row
tabulation, and the `--single` tracer path.** The extraction channel is fixed
by the D-22 live probe committed in the prior commit — see
`tests/quality-probe-v8.7/README.md` for the probe's observed shape (and its
one contradiction of the archived async-task evidence) and `164-CONTEXT.md`
D-22 for the full record. Guardrail fixtures for Plan 02's remaining
`--self-test` items (blinding integrity, tabulation arithmetic,
baseline-fixture integrity, the guardrail negative fixtures themselves) are
out of this commit's scope.

Usage:
    python3 scripts/check-quality-harness.py --self-test
    python3 scripts/check-quality-harness.py --probe Q-P1 \\
        --catalog tests/quality-catalog-v8.7.md --out /tmp/qh-probe
    python3 scripts/check-quality-harness.py --single \\
        tests/quality-probe-v8.7/probe-P1.jsonl

Options:
    --self-test         Run the offline deterministic self-test and exit (no
                         `claude` invoked).
    --catalog PATH      Path to tests/quality-catalog-v8.7.md (required for
                         --probe).
    --out PATH          Output directory for `.jsonl` captures (required for
                         --probe).
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

Exit codes:
    0  Self-test passed, or a run/probe/single-path completed successfully.
    1  Self-test failed, or a run failed.
    2  Usage/environment error (missing `claude` on PATH, bad arguments).
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
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


def build_judge_packet(analysis_text: str, packet_root: Path | None = None) -> Path:
    """Create a sealed judge packet dir outside the repository (D-05).

    Writes exactly two files: `analysis.md` (the passed-in, already-anonymised
    analysis text) and `validation-rubric.md` (copied verbatim from
    shared/spine/references/validation-rubric.md). Verifies exactly two
    entries exist and the resolved path has no repository-root ancestor
    before returning; raises ValueError on either failure. Never writes a
    blinding key here — the key belongs to the run output directory (D-05),
    never inside or beside a packet directory.

    `packet_root`, when given, overrides the parent directory the fresh
    packet dir is created under (still verified outside the repo); when
    None, the OS default temp root is used.
    """
    packet_dir = Path(tempfile.mkdtemp(prefix="qh-packet-", dir=packet_root))
    resolved = packet_dir.resolve()
    repo_root_resolved = REPO_ROOT.resolve()
    if resolved == repo_root_resolved or repo_root_resolved in resolved.parents:
        raise ValueError(f"judge packet dir {resolved} is inside the repository root")

    (packet_dir / "analysis.md").write_text(analysis_text, encoding="utf-8")
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


def _self_test_judge_prompt_unblinded() -> bool:
    """D-05/T-164-03: JUDGE_PROMPT itself must carry no comparison-leaking language."""
    if not _check_judge_prompt_unblinded():
        print(
            "self-test FAIL: judge_prompt_unblinded — JUDGE_PROMPT contains a "
            "forbidden comparison-leaking substring",
            file=sys.stderr,
        )
        return False
    return True


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


def self_test() -> int:
    """Run the offline deterministic self-test. Returns 0 on pass, 1 on failure.

    No `claude` process is spawned and no network is used. Task 1 seeded two
    sub-checks (catalog parse positive/negative); Task 3 adds the judge-prompt
    blinding check and the tracer_path end-to-end offline chain. Plan 02 adds
    the remaining D-15 sub-checks (guardrail negative fixtures, scoreline
    parser positive/negative, tabulation arithmetic, baseline-fixture
    integrity) to this function.
    """
    all_passed = True

    if not _self_test_catalog_parse_positive():
        all_passed = False
    if not _self_test_catalog_parse_negative():
        all_passed = False
    if not _self_test_judge_prompt_unblinded():
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

    if not _self_test_tracer_path():
        all_passed = False
        print("self-test: tracer_path sub-check FAILED", file=sys.stderr)
    else:
        print("self-test: tracer_path sub-check PASSED")

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

    parser.error("no action specified — pass --self-test, --probe, or --single")
    return 2  # unreachable — parser.error exits


if __name__ == "__main__":
    sys.exit(main())
