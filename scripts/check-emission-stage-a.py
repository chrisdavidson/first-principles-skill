#!/usr/bin/env python3
"""Stage A of the `emission-phase1` pre-registration.

Captures the *subagent's* own analysis document -- not the main session's summary of
it -- and reads it mechanically. No judge, no live `claude` call in `--self-test`.

The fault this exists to avoid is recorded in `docs/trackb-transport-erratum.md`: the
Track B run captured `claude -p` stdout, which under `--plugin-dir` is the orchestrator's
summary of the agent's document. Every arm-T reading in that run therefore describes a
summary. Here the capture is the assistant message carrying a non-empty
`parent_tool_use_id`, which is the subagent's own emission.

Protocol: `docs/emission-phase1-preregistration.md`.

    python3 scripts/check-emission-stage-a.py --self-test
    python3 scripts/check-emission-stage-a.py plan
    python3 scripts/check-emission-stage-a.py run --out-dir tests/emission-stage-a-v9.14
    python3 scripts/check-emission-stage-a.py read --out-dir tests/emission-stage-a-v9.14
"""
from __future__ import annotations

import argparse
import functools
import json
import os
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGIN_DIR = REPO_ROOT / "first-principles"
CATALOG = REPO_ROOT / "tests" / "trackb-catalog-v9.13.md"
PREREG = REPO_ROOT / "docs" / "emission-phase1-preregistration.md"

MODEL = "claude-sonnet-5"
MIN_WORDS = 120
MIN_SECTIONS = 4
N_PROMPTS = 10

SECTIONS = (
    "Problem Essence",
    "Assumptions Table",
    "Ground Truths",
    "Derivation Chains",
    "Abandoned Reasoning",
    "Conclusion",
)

# Retained verbatim from check-trackb-comparative.py's §7 check.
_RUBRIC_CONTAMINATION_MARKERS = (
    "TRACKB-SCORELINE-START",
    "Score the document on its own terms",
    "Format carries no marks",
)

_PRINT_BG_WAIT_ENV = {"CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS": "0"}


class StageAError(RuntimeError):
    pass


# ---------------------------------------------------------------------------
# Mechanical readings
# ---------------------------------------------------------------------------

_NUM = re.compile(r"\d[\d,]*(?:\.\d+)?")
_OPSYM = re.compile(
    r"[×÷]"
    r"|(?<=[\s\d)])[*x](?=[\s\d(])"
    r"|(?<=\d)\s*/\s*(?=\d)"
    r"|(?<=[\s\d)])[+](?=[\s\d(])"
)
_RESULT = re.compile(r"=|≈|→")
_URL = re.compile(r"https?://")
_GT = re.compile(r"\bGT-\d+")
_CHAIN_HOP = re.compile(r"^\s*→")
_UNGROUNDED = re.compile(r"\[(?:ungrounded|external[^\]]*|unverified[^\]]*)\]", re.IGNORECASE)
_WEIGHT_HEADER = re.compile(r"^\|.*\b(weight|score)\b.*\|", re.IGNORECASE)


def derivation_lines(text: str) -> list[str]:
    """Lines carrying a visible numeric derivation.

    Sensitivity is MEASURED and poor: 1 of 2 at document level on the only corpus
    where it has been hand-audited (the 20 frozen Track B captures). See
    `docs/emission-phase1-preregistration.md` §6. It is a reported secondary reading,
    never a gate.
    """
    out = []
    for line in text.splitlines():
        if (
            len(_NUM.findall(line)) >= 2
            and _OPSYM.search(line)
            and _RESULT.search(line)
        ):
            out.append(line.strip())
    return out


def sections_present(text: str) -> list[str]:
    return [s for s in SECTIONS if s.lower() in text.lower()]


def read_document(text: str) -> dict:
    return {
        "words": len(text.split()),
        "sections_present": sections_present(text),
        "section_count": len(sections_present(text)),
        "gt_identifiers": len(_GT.findall(text)),
        "chain_hops": sum(1 for l in text.splitlines() if _CHAIN_HOP.match(l)),
        "derivation_lines": len(derivation_lines(text)),
        "urls": len(_URL.findall(text)),
        "ungrounded_marks": len(_UNGROUNDED.findall(text)),
        "weight_table": any(_WEIGHT_HEADER.match(l) for l in text.splitlines()),
    }


def capture_problems(text: str, from_subagent: bool) -> list[str]:
    """The four §3 capture-integrity conditions. Condition 2 is what Track B lacked."""
    probs: list[str] = []
    if not from_subagent:
        probs.append("not-from-subagent")
    if len(sections_present(text)) < MIN_SECTIONS:
        probs.append(
            f"only {len(sections_present(text))} of 6 section headings "
            f"(need >= {MIN_SECTIONS}) -- looks like a summary, not the document"
        )
    for marker in _RUBRIC_CONTAMINATION_MARKERS:
        if marker in text:
            probs.append(f"rubric-contamination: {marker!r}")
    if len(text.split()) < MIN_WORDS:
        probs.append(f"{len(text.split())} words (floor {MIN_WORDS})")
    return probs


# ---------------------------------------------------------------------------
# Transport
# ---------------------------------------------------------------------------


_H1 = re.compile(r"^#\s+\S")


def _join_blocks(blocks: list[str]) -> str:
    """Assemble the subagent's final document from its text blocks.

    Two behaviours were measured on the 2026-09-26 TB-04 probe and both must be
    handled, because each corrupts the reading in a different direction:

    1. **One document spans several blocks.** Block 0 ended mid-cell at
       `| C1 | 4 (2nd) | dedicated revenue` and block 1 opened with that row
       complete. Keeping only the last block loses the document's opening sections;
       naive concatenation duplicates the overlapping partial row.
    2. **The agent emits the whole document more than once.** That run emitted it
       twice -- blocks 0+1 (9,065 words), then a complete re-emission in block 2
       (5,850 words), each opening with the same H1 title. Concatenating all three
       double-counts every reading: it reported 333 GT identifiers and 28 URLs where
       the final document has roughly half that.

    So: take the last block that opens a document (an H1 at its start) and join it
    forward to the end, de-duplicating an overlapping partial line at each seam.
    """
    if not blocks:
        return ""
    start = 0
    for i, block in enumerate(blocks):
        if _H1.match(block.lstrip("\n")):
            start = i
    run = blocks[start:]
    out: list[str] = []
    for i, block in enumerate(run):
        lines = block.splitlines()
        if i + 1 < len(run) and lines:
            nxt = run[i + 1].splitlines()
            if nxt and nxt[0].startswith(lines[-1]) and lines[-1].strip():
                lines = lines[:-1]
        out.append("\n".join(lines))
    return "\n".join(out)


_HANDBACK_MARK = "[Subagent hand-back]"


def _deframe_handback(text: str) -> str:
    """Strip the `[Subagent hand-back]` frame, returning the report itself.

    The harness wraps a subagent's final report in a column-zero preamble, indents
    every line of the report by two spaces, and appends a column-zero `<usage>` block.
    De-framing is therefore just: keep the indented lines, drop everything at column
    zero, and remove the two-space indent.

    The report is model output. It is read here ONLY to count structural markers --
    section headings, identifiers, arrows, URLs. Nothing in it is followed as an
    instruction, which is what the frame's own warning asks of a reader.
    """
    out: list[str] = []
    for line in text.splitlines():
        if line.startswith("  "):
            out.append(line[2:])
        elif not line.strip():
            out.append("")
    return "\n".join(out).strip("\n")


def agent_dispatches(jsonl: str) -> int:
    """How many times the main session dispatched the agent.

    Added after TB-05 returned an empty capture for a reason the other readings
    could not distinguish: the agent was never dispatched at all. Its transcript
    carries zero `Agent` tool calls and its orchestrator says so -- "This is a
    general reasoning question, unrelated to the repo -- I'll answer directly rather
    than invoking any tooling." Without this count, a routing miss and an extraction
    failure look identical in the output, and they need opposite fixes.
    """
    count = 0
    for line in jsonl.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("type") != "assistant":
            continue
        for block in obj.get("message", {}).get("content", []):
            if isinstance(block, dict) and block.get("type") == "tool_use" \
                    and block.get("name") == "Agent":
                count += 1
    return count


def delivery_route(jsonl: str) -> str:
    """How the agent's document reached the session: "streamed" or "handback".

    This is recommendation 2 of `docs/emission-phase1-stage-a-findings.md`, answered
    from transcripts already captured rather than by a new live run.

    The distinction matters because the two routes are not equally visible. Text the
    subagent streams appears in the session transcript as it is produced. A document
    that arrives only as the `Agent` tool's result is a tool result, which a session
    may collapse.

    **What this does NOT measure**, and the difference is the whole caveat: it reads
    what the transport carries, not what a UI renders. A streamed document is present
    in the transcript; whether a given interface displays it expanded, collapsed or at
    all is a rendering question no transcript can answer.
    """
    streamed = 0
    handback = 0
    for line in jsonl.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("type") == "assistant" and obj.get("parent_tool_use_id"):
            for block in obj.get("message", {}).get("content", []):
                if isinstance(block, dict) and block.get("type") == "text":
                    streamed += len(block.get("text", "").split())
        elif obj.get("type") == "user":
            for block in obj.get("message", {}).get("content", []) or []:
                if not isinstance(block, dict) or block.get("type") != "tool_result":
                    continue
                content = block.get("content")
                if isinstance(content, list):
                    content = "".join(
                        x.get("text", "") for x in content if isinstance(x, dict))
                if _HANDBACK_MARK in str(content):
                    handback += len(str(content).split())
    if streamed >= MIN_WORDS:
        return "streamed"
    if handback >= MIN_WORDS:
        return "handback"
    return "none"


def _handbacks(jsonl: str) -> list[str]:
    """Every subagent hand-back in the transcript, in order, de-framed."""
    found: list[str] = []
    for line in jsonl.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("type") != "user":
            continue
        for block in obj.get("message", {}).get("content", []) or []:
            if not isinstance(block, dict) or block.get("type") != "tool_result":
                continue
            content = block.get("content")
            if isinstance(content, list):
                content = "".join(
                    x.get("text", "") for x in content if isinstance(x, dict))
            content = str(content or "")
            if _HANDBACK_MARK in content:
                found.append(_deframe_handback(content))
    return found


def extract_subagent_text(jsonl: str) -> tuple[str, str]:
    """Return (subagent_document, orchestrator_final_text) from a stream-json run.

    The subagent's messages are those carrying a non-empty `parent_tool_use_id` -- the
    same threading `scripts/check-provenance.py` relies on. Every subagent text block
    is part of the document (see `_join_blocks`); only the orchestrator's *last*
    message is its summary.
    """
    sub: list[str] = []
    orch: list[str] = []
    for line in jsonl.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("type") != "assistant":
            continue
        content = obj.get("message", {}).get("content", [])
        if isinstance(content, str):
            blocks = [content]
        else:
            blocks = [
                b.get("text", "")
                for b in content
                if isinstance(b, dict) and b.get("type") == "text"
            ]
        target = sub if obj.get("parent_tool_use_id") else orch
        target.extend(t for t in blocks if t.strip())

    # A subagent does not always stream its document as assistant text: measured on
    # TB-03 and TB-05, where it emitted 12 tool calls and ZERO text blocks, and the
    # document arrived only as the Agent tool's hand-back. So the hand-backs are
    # candidates too, and the one that IS a document wins.
    candidates = _handbacks(jsonl)
    joined = _join_blocks(sub)
    if joined.strip():
        candidates.append(joined)

    document = ""
    for cand in candidates:                      # last candidate that is a document
        if len(sections_present(cand)) >= MIN_SECTIONS:
            document = cand
    if not document and candidates:              # none qualifies: keep the fullest,
        document = max(candidates, key=lambda c: len(c.split()))  # so `read` can say why
    return document, (orch[-1] if orch else "")


def parse_catalog(text: str) -> list[tuple[str, str, str]]:
    rows = []
    for line in text.splitlines():
        m = re.match(r"^\|\s*(TB-\d+)\s*\|\s*(\w+)\s*\|\s*(.+?)\s*\|\s*$", line)
        if m:
            rows.append((m.group(1), m.group(2), m.group(3)))
    return rows


def run_one(prompt_text: str, raw_path: Path) -> str:
    argv = [
        "claude", "-p", "--model", MODEL,
        "--plugin-dir", str(PLUGIN_DIR),
        "--output-format", "stream-json", "--verbose",
        "--no-session-persistence",
        "--permission-mode", "bypassPermissions",
        prompt_text,
    ]
    env = {**os.environ, **_PRINT_BG_WAIT_ENV}
    proc = subprocess.run(argv, capture_output=True, text=True, timeout=5400, env=env, check=False)
    raw_path.write_text(proc.stdout, encoding="utf-8")
    return proc.stdout


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


def cmd_plan() -> int:
    prompts = parse_catalog(CATALOG.read_text(encoding="utf-8"))
    print("emission-phase1 Stage A -- plan (no spend)")
    print(f"  prompts          : {len(prompts)}")
    print(f"  model            : {MODEL}")
    print(f"  live calls       : {len(prompts)} (generation only; no judge)")
    print("  capture          : subagent message (parent_tool_use_id), stream-json")
    print(f"  void unless      : >= {MIN_SECTIONS} of 6 sections, >= {MIN_WORDS} words,")
    print("                     no rubric contamination, from the subagent")
    print(f"  protocol         : {PREREG.relative_to(REPO_ROOT)}")
    return 0


def cmd_run(out_dir: Path) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_dir = out_dir / "raw"
    doc_dir = out_dir / "documents"
    raw_dir.mkdir(exist_ok=True)
    doc_dir.mkdir(exist_ok=True)

    prompts = parse_catalog(CATALOG.read_text(encoding="utf-8"))
    if len(prompts) != N_PROMPTS:
        raise StageAError(f"catalog holds {len(prompts)} prompts, expected {N_PROMPTS}")

    for pid, _domain, text in prompts:
        raw = raw_dir / f"{pid}.jsonl"
        doc = doc_dir / f"{pid}.md"
        if doc.is_file() and doc.read_text(encoding="utf-8").strip():
            print(f"[gen] {pid} (cached)", flush=True)
            continue
        if not raw.is_file() or not raw.read_text(encoding="utf-8").strip():
            print(f"[gen] {pid} ...", flush=True)
            run_one(text, raw)
        sub, orch = extract_subagent_text(raw.read_text(encoding="utf-8"))
        doc.write_text(sub, encoding="utf-8")
        (doc_dir / f"{pid}.orchestrator.md").write_text(orch, encoding="utf-8")
        print(f"[gen] {pid} subagent={len(sub.split())}w "
              f"orchestrator={len(orch.split())}w", flush=True)
    return cmd_read(out_dir)


# ---------------------------------------------------------------------------
# Live-output conformance -- a RECORDED READING, never a gate
# ---------------------------------------------------------------------------

_CONFORMANCE_FIELDS: tuple[tuple[str, str], ...] = (
    ("untraced_claims", "conclusion_claims"),
    ("malformed_chain_blocks", "chain_blocks"),
    ("nonconforming_verdict_cells", "verdict_cells"),
)


def _rel(path: Path) -> str:
    """Repo-relative POSIX path, tolerant of a relative --out-dir."""
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


@functools.lru_cache(maxsize=1)
def _load_qh():
    """Load `check-quality-harness.py` as a module, cached.

    The same `importlib.util.spec_from_file_location` pattern
    `conformance_reading` used inline before this helper was factored out of
    it (quick task 260929-tg9) -- both `conformance_reading` and C21
    (`_c21_answer_first_document_reads_like_the_bare_one`) load the harness
    through it now, so a 20k-line module is executed once per process, not
    once per caller.
    """
    import importlib.util as _ilu
    import sys as _sys

    spec = _ilu.spec_from_file_location(
        "_qh_for_stage_a", REPO_ROOT / "scripts" / "check-quality-harness.py")
    qh = _ilu.module_from_spec(spec)
    _sys.modules["_qh_for_stage_a"] = qh
    spec.loader.exec_module(qh)
    return qh


def conformance_reading(doc_dir: Path) -> dict:
    """Run the shipped defect detector over the frozen live corpus.

    **This is a reading, not a gate, and nothing here changes an exit code.**
    Emission rates are K-of-N live observations, and
    `docs/v8.7-constraint-teardown.md` section 2 item 3 bars those from gating. The
    reading is deterministic only because the corpus is frozen; re-running the AGENT
    would not reproduce it, which is exactly why it may not gate.

    The detector is `check-quality-harness.detect_defects` -- the same instrument
    `report-conformance.py` uses on the v9.0 surface, reused rather than
    reimplemented so the two readings are comparable.

    **Unreadable documents are counted, never dropped.** A document that abandons the
    output contract entirely raises `SectionResolutionError` and contributes to no
    numerator or denominator, so conformance rates are conditional on readability and
    a total abandonment cannot lower any of them. Reporting `unreadable` beside the
    rates is what stops that reading as a clean bill of health.
    """
    qh = _load_qh()

    totals: dict[str, int] = {}
    scored = 0
    unreadable: list[str] = []
    for doc in sorted(doc_dir.glob("TB-*.md")):
        if doc.name.endswith(".orchestrator.md"):
            continue
        text = doc.read_text(encoding="utf-8")
        if not text.strip():
            continue
        try:
            d = qh.detect_defects(text, doc.stem)
        except Exception:  # noqa: BLE001 -- any parse refusal is "unreadable"
            unreadable.append(doc.stem)
            continue
        scored += 1
        for num, den in _CONFORMANCE_FIELDS:
            for field in (num, den):
                v = d.get(field, 0)
                totals[field] = totals.get(field, 0) + (v if isinstance(v, int) else 0)

    rates = {}
    for num, den in _CONFORMANCE_FIELDS:
        n, m = totals.get(num, 0), totals.get(den, 0)
        rates[num] = {
            "numerator": n,
            "denominator": m,
            "rate_pct": (round(100.0 * n / m, 1) if m else None),
        }
    return {
        "corpus": _rel(doc_dir),
        "documents_scored": scored,
        "documents_unreadable": len(unreadable),
        "unreadable_ids": unreadable,
        "rates": rates,
        "is_a_gate": False,
    }


def cmd_conformance(out_dir: Path) -> int:
    r = conformance_reading(out_dir / "documents")
    n = r["documents_scored"]
    print(f"\nlive-output conformance reading -- {r['corpus']}")
    print(f"  N = {n} scored, {r['documents_unreadable']} unreadable "
          f"{r['unreadable_ids'] or ''}")
    print("  (a recorded reading with its N, never a gate)\n")
    for field, v in r["rates"].items():
        pct = "n/a" if v["rate_pct"] is None else f"{v['rate_pct']:5.1f}%"
        print(f"  {field:<30}{v['numerator']:>4}/{v['denominator']:<5} = {pct}")
    print("\n  Rates are conditional on readability: an unreadable document "
          "contributes to\n  no denominator, so contract abandonment cannot lower any "
          "rate above.")
    return 0


def cmd_reextract(out_dir: Path) -> int:
    """Re-derive documents/ from the cached raw/ transcripts. No live calls.

    Extraction rules have changed twice during this run as the transcripts revealed
    shapes the first rule did not handle (see `_join_blocks` and `_handbacks`). Raw
    transcripts are kept precisely so that a corrected rule costs nothing to apply:
    a reading is re-derivable, never re-spent. Note that `run.log` records what the
    runner saw at generation time and is NOT retroactively corrected -- the documents
    and `stage-a-result.json` this command writes are the authoritative readings.
    """
    raw_dir = out_dir / "raw"
    doc_dir = out_dir / "documents"
    if not raw_dir.is_dir():
        raise StageAError(f"no raw transcripts in {raw_dir}")
    doc_dir.mkdir(exist_ok=True)
    for raw in sorted(raw_dir.glob("TB-*.jsonl")):
        sub, orch = extract_subagent_text(raw.read_text(encoding="utf-8"))
        (doc_dir / f"{raw.stem}.md").write_text(sub, encoding="utf-8")
        (doc_dir / f"{raw.stem}.orchestrator.md").write_text(orch, encoding="utf-8")
        print(f"[re-extract] {raw.stem} subagent={len(sub.split())}w "
              f"orchestrator={len(orch.split())}w", flush=True)
    return cmd_read(out_dir)


def cmd_read(out_dir: Path) -> int:
    doc_dir = out_dir / "documents"
    if not doc_dir.is_dir():
        raise StageAError(f"no documents in {out_dir}")

    rows = {}
    voids = {}
    for doc in sorted(doc_dir.glob("TB-*.md")):
        if doc.name.endswith(".orchestrator.md"):
            continue
        text = doc.read_text(encoding="utf-8")
        pid = doc.stem
        probs = capture_problems(text, from_subagent=bool(text.strip()))
        rows[pid] = read_document(text)
        raw = out_dir / "raw" / f"{pid}.jsonl"
        rawtext = raw.read_text(encoding="utf-8") if raw.is_file() else None
        disp = agent_dispatches(rawtext) if rawtext is not None else None
        rows[pid]["agent_dispatches"] = disp
        rows[pid]["delivery_route"] = delivery_route(rawtext) if rawtext is not None else None
        if disp == 0:
            probs = [("agent never dispatched (0 Agent tool calls) -- routing miss, "
                     "not an extraction failure")] + probs
        if probs:
            voids[pid] = probs

    print(f"\nemission-phase1 Stage A -- mechanical reading ({len(rows)} documents)\n")
    hdr = (f"{'id':<8}{'words':>7}{'sec/6':>7}{'GT':>5}{'hops':>6}{'deriv':>7}"
           f"{'urls':>6}{'marks':>7}{'wtbl':>6}{'disp':>6}{'route':>10}")
    print(hdr)
    print("-" * len(hdr))
    for pid, r in rows.items():
        print(f"{pid:<8}{r['words']:>7}{r['section_count']:>7}{r['gt_identifiers']:>5}"
              f"{r['chain_hops']:>6}{r['derivation_lines']:>7}{r['urls']:>6}"
              f"{r['ungrounded_marks']:>7}{'yes' if r['weight_table'] else '-':>6}"
              f"{('?' if r['agent_dispatches'] is None else r['agent_dispatches']):>6}"
              f"{(r['delivery_route'] or '?'):>10}")

    n = len(rows) or 1
    p1 = sum(1 for r in rows.values() if r["section_count"] >= MIN_SECTIONS)
    p2 = sum(1 for r in rows.values() if r["urls"] > 0)
    p3 = sum(1 for r in rows.values() if r["derivation_lines"] > 0)
    def score(hits: int, need: int) -> str:
        """A prediction is scored only when it is decided.

        Scoring a /10 threshold against a partial run misreports it in BOTH
        directions: 4 of 5 against 'at least 8 of 10' is not REFUTED (five prompts
        remain, so 9 is still reachable), and an early run of hits is not HOLDS.
        A prediction is decided when the remaining prompts cannot change it.
        """
        remaining = N_PROMPTS - len(rows)
        if hits >= need:
            return "HOLDS"
        if hits + remaining < need:
            return "REFUTED"
        return f"PENDING ({remaining} prompt(s) unread; needs {need - hits} more)"

    routes = [r["delivery_route"] for r in rows.values() if r["delivery_route"]]
    if routes:
        s = routes.count("streamed"); h = routes.count("handback")
        print(f"\ndelivery route (recommendation 2): streamed {s}/{len(routes)}, "
              f"hand-back only {h}/{len(routes)}")
        print("  transport only -- says nothing about whether a UI renders it")

    print("\npre-registered predictions (§4):")
    print(f"  P1 >=4/6 sections in >=8 of 10 : {p1}/{len(rows)}  {score(p1, 8)}")
    print(f"  P2 >=1 URL in >=5 of 10        : {p2}/{len(rows)}  {score(p2, 5)}")
    print(f"  P3 derivations above 1 of 10   : {p3}/{len(rows)}  {score(p3, 2)}")
    if len(rows) < N_PROMPTS:
        print(f"  (partial run: {len(rows)} of {N_PROMPTS} prompts read)")
    if voids:
        print(f"\nVOID captures ({len(voids)}):")
        for pid, probs in voids.items():
            print(f"  {pid}: {probs}")
    record = {
        "complete": len(rows) == N_PROMPTS,
        "run_id": out_dir.name,
        "model": MODEL,
        "protocol": "emission-phase1",
        "documents": rows,
        "voids": voids,
        "predictions": {"P1": p1, "P2": p2, "P3": p3, "n": len(rows)},
    }
    (out_dir / "stage-a-result.json").write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


# ---------------------------------------------------------------------------
# Falsifiability controls
# ---------------------------------------------------------------------------


def _c01_summary_is_rejected_document_is_not() -> str | None:
    """The check Track B lacked: a well-formed summary must NOT pass as a document."""
    summary = (
        "Here's the analysis, distilled from the full first-principles breakdown:\n"
        + "The city should price congestion. " * 60
    )
    if len(summary.split()) < MIN_WORDS:
        return "C01 fixture is below the word floor; it would void for the wrong reason"
    if not capture_problems(summary, from_subagent=True):
        return "C01: a 300-word summary passed the capture check"
    document = (
        "## Problem Essence\nx\n## Assumptions Table\nx\n## Ground Truths\nx\n"
        "## Derivation Chains\nx\n## Abandoned Reasoning\nx\n## Conclusion\nx\n"
        + "word " * 200
    )
    if capture_problems(document, from_subagent=True):
        return f"C01: a real document was voided: {capture_problems(document, True)}"
    return None


def _c02_orchestrator_capture_is_rejected() -> str | None:
    """A capture not carrying parent_tool_use_id is void however good it looks."""
    good = "## Problem Essence\n## Assumptions Table\n## Ground Truths\n## Conclusion\n" + "word " * 200
    if "not-from-subagent" not in capture_problems(good, from_subagent=False):
        return "C02: an orchestrator-sourced capture was accepted"
    return None


def _c03_subagent_extraction_picks_the_right_message() -> str | None:
    """The whole erratum in one control: orchestrator text must not be returned."""
    lines = [
        json.dumps({"type": "assistant", "message": {"content": [
            {"type": "text", "text": "I'll delegate this."}]}}),
        json.dumps({"type": "assistant", "parent_tool_use_id": "toolu_1",
                    "message": {"content": [{"type": "text", "text": "THE DOCUMENT"}]}}),
        json.dumps({"type": "assistant", "message": {"content": [
            {"type": "text", "text": "Here's the analysis, distilled:"}]}}),
    ]
    sub, orch = extract_subagent_text("\n".join(lines))
    if sub != "THE DOCUMENT":
        return f"C03: subagent text was {sub!r}, expected 'THE DOCUMENT'"
    if orch != "Here's the analysis, distilled:":
        return f"C03: orchestrator text was {orch!r}"
    return None


def _c11_multiblock_document_is_joined_not_truncated() -> str | None:
    """A long document arrives as several subagent text blocks. Keeping only the last
    silently drops its opening sections -- measured on the TB-04 probe, where that
    rule returned 2,969 of 9,065 words and 3 of 6 section headings."""
    b0 = "## Problem Essence\nfirst part\n| C1 | 4 | dedicated revenue"
    b1 = "| C1 | 4 | dedicated revenue gives officials a stake |\n## Conclusion\nend"
    lines = [
        json.dumps({"type": "assistant", "parent_tool_use_id": "t",
                    "message": {"content": [{"type": "text", "text": b0}]}}),
        json.dumps({"type": "assistant", "parent_tool_use_id": "t",
                    "message": {"content": [{"type": "text", "text": b1}]}}),
    ]
    sub, _ = extract_subagent_text("\n".join(lines))
    if "Problem Essence" not in sub:
        return "C11: the first block was dropped -- document truncated"
    if "Conclusion" not in sub:
        return "C11: the last block was dropped"
    if sub.count("dedicated revenue") != 1:
        return (f"C11: the overlapping partial row was duplicated "
                f"({sub.count('dedicated revenue')} occurrences, expected 1)")
    return None


def _c12_re_emitted_document_is_not_double_counted() -> str | None:
    """The agent may emit the whole document twice. Concatenating both doubles every
    reading -- measured on the TB-04 probe as 333 GT identifiers and 28 URLs against a
    final document carrying about half that. Only the last emission is the document."""
    first = "# Analysis\n## Problem Essence\nGT-1 GT-2\nhttps://a.example\ndraft tail"
    second = "# Analysis\n## Problem Essence\nGT-1 GT-2\nhttps://a.example\nfinal tail"
    lines = [
        json.dumps({"type": "assistant", "parent_tool_use_id": "t",
                    "message": {"content": [{"type": "text", "text": t}]}})
        for t in (first, second)
    ]
    sub, _ = extract_subagent_text("\n".join(lines))
    r = read_document(sub)
    if r["gt_identifiers"] != 2:
        return (f"C12: {r['gt_identifiers']} GT identifiers from a re-emitted "
                f"document, expected 2 -- both emissions were counted")
    if r["urls"] != 1:
        return f"C12: {r['urls']} URLs, expected 1 -- both emissions were counted"
    if "draft tail" in sub:
        return "C12: the superseded first emission is still in the document"
    if "final tail" not in sub:
        return "C12: the final emission was dropped"
    return None


def _c04_extraction_survives_malformed_lines() -> str | None:
    blob = "not json\n\n" + json.dumps(
        {"type": "assistant", "parent_tool_use_id": "t",
         "message": {"content": [{"type": "text", "text": "D"}]}}) + "\n{bad"
    sub, _ = extract_subagent_text(blob)
    if sub != "D":
        return f"C04: malformed lines broke extraction, got {sub!r}"
    return None


def _c05_detector_finds_a_planted_derivation() -> str | None:
    if not derivation_lines("Totals: (5 × 5) + (3 × 4) = 37 points."):
        return "C05: detector missed a planted arithmetic line"
    return None


def _c06_detector_rejects_bare_numbers() -> str | None:
    text = "Pricing scores 82, cycle lanes 70, free transit 63, across 6 criteria."
    if derivation_lines(text):
        return "C06: detector fired on bare numbers with no operator or result"
    return None


def _c07_detector_blindness_is_still_what_is_published() -> str | None:
    """§6 publishes a 1-of-2 document-level sensitivity. If the detector is silently
    improved or degraded, the published figure is stale -- fail rather than mislead."""
    caught = "- **Demand:** ~6,250 kWh/person/year × 10M people ≈ **60 TWh/year** today"
    missed = "**Supported:** the runs showed higher yield (62%→71%, a 9-point / ~14.5% relative increase)"
    if not derivation_lines(caught):
        return "C07: the published 'caught' specimen is no longer caught"
    if derivation_lines(missed):
        return ("C07: the published 'missed' specimen is now caught -- detector improved, "
                "so §6's measured 1-of-2 sensitivity is stale and must be re-audited")
    return None


def _c08_frozen_trackb_captures_still_fail_the_check() -> str | None:
    """The erratum's claim, as an executable control against the frozen evidence."""
    gens = REPO_ROOT / "tests" / "trackb-run-v9.13" / "generations"
    if not gens.is_dir():
        return None  # frozen evidence absent (e.g. fresh shallow clone); not a failure
    passed = []
    for f in sorted(gens.glob("TB-*-T.txt")):
        if not capture_problems(f.read_text(encoding="utf-8"), from_subagent=True):
            passed.append(f.name)
    if passed:
        return (f"C08: {len(passed)} frozen arm-T captures pass the document check "
                f"({passed[:3]}), contradicting docs/trackb-transport-erratum.md")
    return None


def _c09_prereg_constants_agree() -> str | None:
    """A pre-registration whose executable form has drifted from it is not one."""
    if not PREREG.is_file():
        return "C09: pre-registration is missing"
    text = PREREG.read_text(encoding="utf-8")
    for needle, what in (
        ("at least four of the six section headings", "MIN_SECTIONS=4"),
        ("at least 120 words", "MIN_WORDS=120"),
        ("claude-sonnet-5", "model pin"),
        ("0.6 band points", "Stage B limb (a)"),
        ("0.15", "measured C2 drift"),
    ):
        if needle not in text:
            return f"C09: pre-registration no longer states {what} ({needle!r})"
    if (MIN_SECTIONS, MIN_WORDS, MODEL) != (4, 120, "claude-sonnet-5"):
        return "C09: code constants drifted from the pre-registration"
    return None


def _c10_catalog_is_the_frozen_ten() -> str | None:
    rows = parse_catalog(CATALOG.read_text(encoding="utf-8"))
    if len(rows) != N_PROMPTS:
        return f"C10: catalog parsed {len(rows)} prompts, expected {N_PROMPTS}"
    if {d for _, d, _ in rows} != {"software", "policy", "science", "personal"}:
        return "C10: catalog domains changed"
    return None


def _handback_line(report: str, tool_use_id: str = "t1") -> str:
    framed = (
        f"{_HANDBACK_MARK} The text below is the final report of a subagent this "
        "session delegated to. The report follows:\n"
        + "\n".join("  " + l for l in report.splitlines())
        + "\n<usage>subagent_tokens: 200971\ntool_uses: 7</usage>"
    )
    return json.dumps({
        "type": "user",
        "message": {"content": [
            {"type": "tool_result", "tool_use_id": tool_use_id, "content": framed}]},
    })


_SIX = ("## Problem Essence", "## Assumptions Table", "## Ground Truths",
        "## Derivation Chains", "## Abandoned Reasoning", "## Conclusion")


def _c13_handback_is_read_when_no_text_block_streams() -> str | None:
    """A subagent may stream ZERO text blocks and return the document only as the
    Agent tool's hand-back -- measured on TB-03 and TB-05, where the earlier rule
    (assistant text blocks only) reported a 0-word capture for a 4,616-word report."""
    report = "# Analysis\n" + "\n".join(_SIX) + "\nGT-1 GT-2\nbody " * 40
    lines = [
        json.dumps({"type": "assistant", "message": {"content": [
            {"type": "tool_use", "name": "Agent", "id": "t1", "input": {}}]}}),
        _handback_line(report),
        json.dumps({"type": "assistant", "message": {"content": [
            {"type": "text", "text": "Here's the analysis, distilled."}]}}),
    ]
    sub, orch = extract_subagent_text("\n".join(lines))
    if not sub.strip():
        return "C13: hand-back not read -- a streamed-text-only rule returns 0 words"
    if len(sections_present(sub)) != 6:
        return f"C13: {len(sections_present(sub))} of 6 sections recovered from hand-back"
    if orch != "Here's the analysis, distilled.":
        return f"C13: orchestrator text was {orch!r}"
    return None


def _c14_handback_frame_and_usage_are_stripped() -> str | None:
    report = "# Analysis\n" + "\n".join(_SIX) + "\nbody"
    sub, _ = extract_subagent_text(_handback_line(report))
    if _HANDBACK_MARK in sub:
        return "C14: the hand-back preamble survived into the document"
    if "subagent_tokens" in sub or "<usage>" in sub:
        return "C14: the trailing <usage> block survived into the document"
    if "# Analysis" not in sub:
        return "C14: de-framing removed the document's own first line"
    return None


def _c15_the_document_handback_wins_over_a_follow_up() -> str | None:
    """TB-03 dispatched two agents: a 4,616-word analysis and a 629-word follow-up.
    Taking the LAST hand-back would capture the follow-up; the document must win."""
    document = "# Analysis\n" + "\n".join(_SIX) + "\nGT-1\nbody " * 30
    follow_up = "Band: **Rigorous**\nJustification: a short self-audit note only."
    sub, _ = extract_subagent_text(
        _handback_line(document, "t1") + "\n" + _handback_line(follow_up, "t2"))
    if "Justification: a short self-audit note only." in sub and "GT-1" not in sub:
        return "C15: the short follow-up hand-back was captured instead of the document"
    if len(sections_present(sub)) != 6:
        return f"C15: recovered {len(sections_present(sub))} of 6 sections, expected the document"
    return None


def _c16_delivery_route_separates_streamed_from_handback() -> str | None:
    """Recommendation 2's reading. A document that only ever arrives as a tool result
    is not delivered the same way as one the subagent streams, and conflating them
    would answer the surfacing question wrongly in whichever direction the last
    transcript happened to fall."""
    body = "# A\n" + "word " * 200
    streamed = json.dumps({"type": "assistant", "parent_tool_use_id": "t",
                           "message": {"content": [{"type": "text", "text": body}]}})
    if delivery_route(streamed) != "streamed":
        return f"C16: streamed text read as {delivery_route(streamed)!r}"
    if delivery_route(_handback_line(body)) != "handback":
        return f"C16: a hand-back read as {delivery_route(_handback_line(body))!r}"
    if delivery_route("") != "none":
        return "C16: an empty transcript did not read as 'none'"
    # a short courtesy line must not count as the document having been streamed
    tiny = json.dumps({"type": "assistant", "parent_tool_use_id": "t",
                       "message": {"content": [{"type": "text", "text": "Done."}]}})
    if delivery_route(tiny + "\n" + _handback_line(body)) != "handback":
        return "C16: a one-line subagent aside outvoted the hand-back carrying the document"
    return None


def _c17_conformance_reading_is_computed_not_hardcoded() -> str | None:
    """The reading must come from the corpus. A hardcoded rate is the defect this
    whole workstream exists to close -- a number that cannot move is not a reading."""
    import tempfile
    six = ("## Problem Essence\nx\n## Assumptions Table\nx\n## Ground Truths\nx\n"
           "## Derivation Chains\nx\n## Abandoned Reasoning\nx\n## Conclusion\nx\n")
    with tempfile.TemporaryDirectory() as td:
        d = Path(td) / "documents"
        d.mkdir()
        (d / "TB-01.md").write_text(six + "word " * 200, encoding="utf-8")
        r = conformance_reading(d)
    if r["documents_scored"] + r["documents_unreadable"] != 1:
        return (f"C17: a one-document corpus produced "
                f"{r['documents_scored']}+{r['documents_unreadable']} documents")
    live = conformance_reading(REPO_ROOT / "tests" / "emission-stage-a-v9.14" / "documents")
    if live["documents_scored"] == r["documents_scored"]:
        return "C17: the reading did not change with the corpus -- it is not computed"
    return None


def _c18_unreadable_documents_are_counted_not_dropped() -> str | None:
    """A document abandoning the contract must be COUNTED, not silently excluded.

    Dropping it flatters every rate: total abandonment would leave the population
    instead of lowering anything. `TB-08` is the live instance -- dispatched, reasoned,
    and carrying 2 of 6 section headings with no traceable identifiers.
    """
    r = conformance_reading(REPO_ROOT / "tests" / "emission-stage-a-v9.14" / "documents")
    if r["documents_unreadable"] < 1:
        return ("C18: no unreadable document reported, but TB-08 abandons the contract "
                "-- unreadable documents are being dropped silently")
    if "TB-08" not in r["unreadable_ids"]:
        return f"C18: unreadable ids {r['unreadable_ids']} do not name TB-08"
    return None


def _c19_the_reading_is_not_a_gate() -> str | None:
    """Emission rates are K-of-N live readings, barred from gating by
    `docs/v8.7-constraint-teardown.md` section 2 item 3. If this ever gates, that bar
    has been crossed silently."""
    r = conformance_reading(REPO_ROOT / "tests" / "emission-stage-a-v9.14" / "documents")
    if r.get("is_a_gate") is not False:
        return "C19: the reading no longer declares itself a non-gate"
    src = (REPO_ROOT / "scripts" / "check-emission-stage-a.py").read_text(encoding="utf-8")
    body = src.split("def cmd_conformance", 1)[1].split("\ndef ", 1)[0]
    if "return 1" in body or "SystemExit" in body:
        return "C19: cmd_conformance can now return a failing exit code -- it gates"
    return None


def _c20_every_reported_rate_states_its_denominator() -> str | None:
    """A rate without its denominator is the shape this repository bars."""
    r = conformance_reading(REPO_ROOT / "tests" / "emission-stage-a-v9.14" / "documents")
    for field, v in r["rates"].items():
        if "denominator" not in v or "numerator" not in v:
            return f"C20: {field} reports a rate with no numerator/denominator"
        if v["denominator"] == 0 and v["rate_pct"] is not None:
            return f"C20: {field} reports a percentage over an empty denominator"
    return None


# ---------------------------------------------------------------------------
# C21 -- answer-first document reads like the bare one (quick task 260929-tg9)
# ---------------------------------------------------------------------------
#
# `check-quality-harness._slice_sections` ends section 6 at the first ATX
# heading of ANY depth after it, outside a fence -- so under the answer-first
# body (shared/spine/SKILL-body.md, D-E) the trailing `## Appendix -- process
# output` heading is what caps section 6, not a convention. This fixture set
# proves that capping works (positive) and that removing only the capping
# heading is visible to the detector (the anti-masking twin) -- so a
# regression that silently drops the heading, or a copy of this fixture that
# forgot it, is something this control can actually catch.

_C21_CHAIN_BLOCK = (
    "### Conclusion C1: The claim\n\n"
    "```text\n"
    "GT-1 (a fact)\n"
    "→ an intermediate claim\n"
    "→ the conclusion\n"
    "```\n\n"
    "**Confidence:** HIGH\n"
)

# Base fixture B: six sections in check-provenance-rollup.py's `_doc()`
# shape, one fenced chain C1, a single inline-cited §6 claim.
_C21_BASE_DOC = (
    "# 1. Problem Essence\n\nOne sentence.\n\n"
    "## 2. Assumptions Table\n\n| Assumption | Type |\n|---|---|\n| A1 | belief |\n\n"
    "## 3. Ground Truths\n\n- **GT-1** A fact. source: arithmetic; read-at-source: in-entry\n\n"
    "## 4. Derivation Chains\n\n" + _C21_CHAIN_BLOCK + "\n"
    "## 5. Abandoned Reasoning\n\nNothing abandoned.\n\n"
    "## 6. Conclusion\n\n**Recommended approach:** Do the thing (chain C1).\n"
)

# Content planted AFTER section 6 in both W and N -- a structural ledger row
# (`_STRUCTURAL_LEDGER_ROW_RE`, `"..." -> chain C1`) and a second, uncited
# `**Recommended approach:**` claim. Neither belongs to section 6 when the
# appendix is correctly capped; both are exactly the kind of content that
# would inflate `conclusion_claims`/`untraced_claims` if section 6 absorbed
# them instead.
_C21_PLANTED = (
    "- \"Do the thing\" -> chain C1\n\n"
    "**Recommended approach:** Adopt the alternative option instead.\n"
)

_C21_ANSWER_BLOCK = (
    "## Answer\n\n"
    "**Recommendation:** Do the thing (chain C1).\n"
    "**Band (from §6):** HIGH (chain C1).\n"
    "**Would change it:** No named evidence would move it (chain C1).\n\n"
)

# W: positive fixture -- Answer block + B + a correctly-capped appendix
# (the `## Appendix -- process output` heading, then a nested self-audit-scan
# heading) holding the same planted content.
_C21_W = (
    _C21_ANSWER_BLOCK
    + _C21_BASE_DOC
    + "\n## Appendix — process output\n\n"
    + "## Self-audit scan (process output)\n\n"
    + "| Chain | Band |\n|---|---|\n| C1 | HIGH |\n\n"
    + _C21_PLANTED
)

# N: the in-control anti-masking twin -- B plus the SAME planted content, but
# with NO heading at all separating it from section 6. `_slice_sections`
# then has nothing to stop section 6 at, and its body absorbs the planted
# lines.
_C21_N = _C21_BASE_DOC + "\n" + _C21_PLANTED

_C21_DEFECT_FIELDS = (
    "conclusion_claims",
    "untraced_claims",
    "chain_blocks",
    "malformed_chain_blocks",
    "verdict_cells",
    "nonconforming_verdict_cells",
    "_closure_ledger_fragments",
)


def _c21_answer_first_document_reads_like_the_bare_one() -> str | None:
    """C21: an answer-first document (Answer + six sections + capped
    appendix) reads identically to the bare six-section document on every
    defect field, and a twin missing only the capping heading reads
    differently -- so this control can fail, rather than passing on any
    document that merely contains the word "Appendix"."""
    qh = _load_qh()

    try:
        base_sections = qh._slice_sections(_C21_BASE_DOC)
    except Exception as exc:  # noqa: BLE001
        return f"C21: base fixture B does not resolve: {exc}"
    base_defects = qh.detect_defects(_C21_BASE_DOC, "C21-B")
    if base_defects["conclusion_claims"] < 1:
        return "C21: base fixture B has no conclusion claims -- precondition not met"
    if base_defects["untraced_claims"] != 0:
        return "C21: base fixture B has an untraced claim -- precondition not met"

    try:
        w_sections = qh._slice_sections(_C21_W)
    except Exception as exc:  # noqa: BLE001
        return f"C21: answer-first fixture W does not resolve: {exc}"
    w_defects = qh.detect_defects(_C21_W, "C21-W")
    for field in _C21_DEFECT_FIELDS:
        if w_defects[field] != base_defects[field]:
            return (
                f"C21: answer-first document W disagrees with the bare "
                f"document B on {field}: {w_defects[field]!r} != "
                f"{base_defects[field]!r}"
            )
    if w_sections[1] != base_sections[1]:
        return "C21: section 1 differs between W and B -- the Answer preamble leaked in"
    present = sections_present(_C21_W)
    if len(present) != len(SECTIONS):
        missing = set(SECTIONS) - set(present)
        return f"C21: sections_present(W) is missing {sorted(missing)!r}"

    n_defects = qh.detect_defects(_C21_N, "C21-N")
    if (
        n_defects["conclusion_claims"] == base_defects["conclusion_claims"]
        and n_defects["untraced_claims"] == base_defects["untraced_claims"]
    ):
        return (
            "C21: anti-masking twin N (headless appendix) reads identically "
            "to B -- the control cannot distinguish a mis-slice"
        )
    return None


_CONTROLS = (
    ("C01", _c01_summary_is_rejected_document_is_not),
    ("C02", _c02_orchestrator_capture_is_rejected),
    ("C03", _c03_subagent_extraction_picks_the_right_message),
    ("C04", _c04_extraction_survives_malformed_lines),
    ("C05", _c05_detector_finds_a_planted_derivation),
    ("C06", _c06_detector_rejects_bare_numbers),
    ("C07", _c07_detector_blindness_is_still_what_is_published),
    ("C08", _c08_frozen_trackb_captures_still_fail_the_check),
    ("C09", _c09_prereg_constants_agree),
    ("C10", _c10_catalog_is_the_frozen_ten),
    ("C11", _c11_multiblock_document_is_joined_not_truncated),
    ("C12", _c12_re_emitted_document_is_not_double_counted),
    ("C13", _c13_handback_is_read_when_no_text_block_streams),
    ("C14", _c14_handback_frame_and_usage_are_stripped),
    ("C15", _c15_the_document_handback_wins_over_a_follow_up),
    ("C16", _c16_delivery_route_separates_streamed_from_handback),
    ("C17", _c17_conformance_reading_is_computed_not_hardcoded),
    ("C18", _c18_unreadable_documents_are_counted_not_dropped),
    ("C19", _c19_the_reading_is_not_a_gate),
    ("C20", _c20_every_reported_rate_states_its_denominator),
    ("C21", _c21_answer_first_document_reads_like_the_bare_one),
)


def self_test() -> int:
    failures = []
    for cid, fn in _CONTROLS:
        try:
            msg = fn()
        except Exception as exc:  # noqa: BLE001
            msg = f"{type(exc).__name__}: {exc}"
        # Print every control's id on every run -- not only on failure -- so a passing
        # run's stdout still names which controls executed (quick task 260929-tg9: a
        # verify step that greps this output for a specific control id, e.g. C21, needs
        # the id to be present on a PASS, not only inside a failure message).
        print(f"  {'FAIL' if msg else 'PASS'}  [{cid}]")
        if msg:
            failures.append(f"  [{cid}] {msg}")
    if failures:
        print(f"STAGE-A SELF-TEST: FAIL ({len(failures)}/{len(_CONTROLS)})")
        print("\n".join(failures))
        return 1
    print(f"STAGE-A SELF-TEST: PASS ({len(_CONTROLS)}/{len(_CONTROLS)} controls)")
    return 0


def describe() -> dict:
    """Pure self-description backing EMIT-STAGE-A (D-03 shape).

    Every field is DERIVED from this module's own rosters. A hand-typed count on a
    generated doc page is the defect CONF-SURFACE exists to prevent.
    """
    return {
        "control_ids": [cid for cid, _fn in _CONTROLS],
        "control_count": len(_CONTROLS),
        "registered_surfaces": [
            str(PREREG.relative_to(REPO_ROOT)),
            str(CATALOG.relative_to(REPO_ROOT)),
        ],
        "checked_files": [
            "tests/emission-stage-a-v9.14/raw/*.jsonl",
            "tests/emission-stage-a-v9.14/documents/*.md",
        ],
        "locked_constants": {
            "MODEL": MODEL,
            "MIN_WORDS": MIN_WORDS,
            "MIN_SECTIONS": MIN_SECTIONS,
            "N_PROMPTS": N_PROMPTS,
        },
        "disclosed_bounds_anchors": [
            "derivation detector sensitivity is 1 of 2 at document level, hand-audited",
            "delivery_route reads the transport, never what a UI renders",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("command", nargs="?", default="plan",
                    choices=["plan", "run", "read", "reextract", "conformance"])
    ap.add_argument("--out-dir", type=Path,
                    default=REPO_ROOT / "tests" / "emission-stage-a-v9.14")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--describe", action="store_true")
    args = ap.parse_args(argv)

    if args.describe:
        print(json.dumps(describe(), indent=2, sort_keys=True))
        return 0
    if args.self_test:
        return self_test()
    try:
        if args.command == "plan":
            return cmd_plan()
        if args.command == "run":
            return cmd_run(args.out_dir)
        if args.command == "reextract":
            return cmd_reextract(args.out_dir)
        if args.command == "conformance":
            return cmd_conformance(args.out_dir)
        return cmd_read(args.out_dir)
    except StageAError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
