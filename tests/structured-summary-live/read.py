#!/usr/bin/env python3
"""structured-summary-live -- the reading side of the live confirmation pre-registered in
docs/structured-summary-live-protocol.md (id ``structured-summary-live``). Gates nothing on its
own: it computes every figure the protocol's criteria need from the captures ``run.py`` collects,
and leaves the pass/fail call to its own ``verdict`` subcommand and the falsifiers that call it.

    python3 tests/structured-summary-live/read.py check
    python3 tests/structured-summary-live/read.py crossread
    python3 tests/structured-summary-live/read.py table
    python3 tests/structured-summary-live/read.py verdict [--leg runs|blocks|gate|cost|all]
    python3 tests/structured-summary-live/read.py --self-test

``check`` runs the unchanged checker (default live mode, never ``--exemplar``/``--schema``) over
every collected report and records the gate reading, by the rule in ``gate_cleared_rule``.
``crossread`` compares each report's block against agent-router's own ``trace.py`` prose parser,
read-only, and records every disagreement with which field it is on. ``table`` renders the
before/after Markdown table. ``verdict`` prints PASS/FAIL per requested leg and exits non-zero
unless every requested leg passes. ``--self-test`` runs offline, no network, no ``claude``, no
subprocess call to the real checker.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import statistics
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent

# --- run.py's constants and helpers, loaded by file path, never copied -----------------------
_run_spec = importlib.util.spec_from_file_location("_ssl_run", HERE / "run.py")
assert _run_spec and _run_spec.loader
_ssl_run = importlib.util.module_from_spec(_run_spec)
_run_spec.loader.exec_module(_ssl_run)

REPO_ROOT = _ssl_run.REPO_ROOT
ID = _ssl_run.ID
FP_REPO = _ssl_run.FP_REPO
AR_DIR = _ssl_run.AR_DIR
RUNNER = _ssl_run.RUNNER
RUNNER_SHA256 = _ssl_run.RUNNER_SHA256
OUT = _ssl_run.OUT
BASELINE_DIR = _ssl_run.BASELINE_DIR
ENTRY = _ssl_run.ENTRY
JOBS = _ssl_run.JOBS
MAX_ATTEMPTS = _ssl_run.MAX_ATTEMPTS
BASELINE_MODEL = _ssl_run.BASELINE_MODEL
EXPECTED_PLUGIN = _ssl_run.EXPECTED_PLUGIN
RAW = _ssl_run.RAW
BASE = _ssl_run.BASE
MANIFEST = _ssl_run.MANIFEST
events = _ssl_run.events
is_limit_stub = _ssl_run.is_limit_stub
loaded_body = _ssl_run.loaded_body
init_event = _ssl_run.init_event
runner_argv = _ssl_run.runner_argv

# --- pinned constants, quoted verbatim by docs/structured-summary-live-protocol.md (R10) ------
CHECKER = "scripts/check-summary-block.py"
# The $2.73 baseline + 10%; the exact +10% of the raw median is 3.0078 and the stricter $3.00 is
# used instead.
COST_CEILING = 3.00
BASELINE_MEDIAN = 2.7343755
GATE_CODES = (
    "SB-GATE-CLEARED", "SB-GATE-RESULT", "SB-GATE-PASSES",
    "SB-GATE-BANDS", "SB-INVARIANT", "SB-REENTRY",
)
HEADING = "## Structured summary (process output)"


# ---------------------------------------------------------------------------
# Block extraction (R01), prose gate line (R02), gate-cleared rule (R03)
# ---------------------------------------------------------------------------

_FENCE_JSON_RE = re.compile(r"```json\s*\n(.*?)\n```", re.DOTALL)


def extract_block(text: str) -> dict | None:
    """The report's one ```json fence under HEADING, parsed. None when the heading is absent,
    no fence follows it, or the fence body is not a JSON object."""
    idx = text.find(HEADING)
    if idx == -1:
        return None
    m = _FENCE_JSON_RE.search(text, idx)
    if m is None:
        return None
    try:
        obj = json.loads(m.group(1))
    except json.JSONDecodeError:
        return None
    return obj if isinstance(obj, dict) else None


_GATE_RESULT_RE = re.compile(r"^\*\*Gate result:\*\*\s*(cleared|not cleared)\b.*$", re.MULTILINE)


def prose_gate_cleared(text: str) -> bool | None:
    """The LAST `**Gate result:**` line decides. None when absent."""
    matches = list(_GATE_RESULT_RE.finditer(text))
    if not matches:
        return None
    return matches[-1].group(1) == "cleared"


def gate_cleared_rule(block: dict | None, prose_cleared: bool | None, gate_findings_present: bool) -> bool:
    """Cleared only when the block's gate.cleared is true AND the prose's last Gate result line
    reads cleared AND the checker reported none of GATE_CODES. Anything else -> not cleared."""
    if not isinstance(block, dict):
        return False
    gate = block.get("gate")
    if not (isinstance(gate, dict) and gate.get("cleared") is True):
        return False
    if prose_cleared is not True:
        return False
    if gate_findings_present:
        return False
    return True


# ---------------------------------------------------------------------------
# Cost rule (R04)
# ---------------------------------------------------------------------------


def cost_leg(rows: list[dict]) -> tuple[bool, float | None]:
    """Median over raw cost_usd floats, <= COST_CEILING. A null cost_usd fails the leg outright
    -- unknown is not cheap."""
    if not rows or any(r.get("cost_usd") is None for r in rows):
        return False, None
    median = statistics.median(r["cost_usd"] for r in rows)
    return median <= COST_CEILING, median


# ---------------------------------------------------------------------------
# Verdict legs (R05)
# ---------------------------------------------------------------------------


def runs_leg(summary_rows: list[dict], checks: list[dict], expected_plugin: str) -> tuple[bool, str]:
    if len(summary_rows) != 14 or len(checks) != 14:
        return False, f"{len(summary_rows)}/14 summary rows, {len(checks)}/14 checks"
    complete = sum(1 for r in summary_rows if r.get("status") == "complete")
    by_name = {c.get("example"): c for c in checks}
    correct_body = sum(
        1 for r in summary_rows
        if by_name.get(r.get("example"), {}).get("loaded_body") == [expected_plugin]
    )
    ok = complete == 14 and correct_body == 14
    return ok, f"{complete}/14 complete, {correct_body}/14 correct body"


def blocks_leg(checks: list[dict]) -> tuple[bool, str]:
    n = sum(1 for c in checks if c.get("checker_exit") == 0 and not c.get("shortfall"))
    return (n == 14 and len(checks) == 14), f"{n}/14"


def gate_leg(checks: list[dict]) -> tuple[bool, str]:
    n = sum(1 for c in checks if c.get("gate_cleared") is True)
    return (n == 14 and len(checks) == 14), f"{n}/14"


def cmd_verdict(
    leg: str = "all",
    *,
    raw_dir: Path = RAW,
    checks_path: Path | None = None,
    expected_plugin: str = str(EXPECTED_PLUGIN),
) -> int:
    if checks_path is None:
        checks_path = HERE / "checks.json"
    summary_path = raw_dir / "summary.json"
    if not summary_path.is_file() or not checks_path.is_file():
        print("verdict: raw/summary.json or checks.json missing -- run `check` first", file=sys.stderr)
        return 2
    summary_rows = json.loads(summary_path.read_text())
    checks = json.loads(checks_path.read_text())
    legs = ("runs", "blocks", "gate", "cost") if leg == "all" else (leg,)
    all_pass = True
    for name in legs:
        if name == "runs":
            ok, detail = runs_leg(summary_rows, checks, expected_plugin)
        elif name == "blocks":
            ok, detail = blocks_leg(checks)
        elif name == "gate":
            ok, detail = gate_leg(checks)
        elif name == "cost":
            cost_ok, median = cost_leg(summary_rows)
            ok = cost_ok
            detail = f"median ${median:.4f}" if median is not None else "median unavailable (a null cost_usd)"
        else:
            continue
        print(f"LEG {name}: {'PASS' if ok else 'FAIL'} ({detail})")
        all_pass = all_pass and ok
    return 0 if all_pass else 1


# ---------------------------------------------------------------------------
# Checker invocation (R06, R07)
# ---------------------------------------------------------------------------


def checker_argv(report_path: str) -> list[str]:
    """[python3, CHECKER, --json, report] -- exactly; never --exemplar, never --schema."""
    return ["python3", CHECKER, "--json", report_path]


def checker_sha256(checker_path: Path) -> str:
    return hashlib.sha256(checker_path.read_bytes()).hexdigest()


# ---------------------------------------------------------------------------
# Report choice (R09)
# ---------------------------------------------------------------------------


def select_report(example_dir: Path) -> tuple[Path | None, list[str]]:
    """The collected report: `raw/<name>/report.md`, which `run.py`'s `collect()` already
    flattened from the longest `.first-principles/analysis-*.md` by character count (its own
    documented `max(texts, key=len)` rule) -- read.py never re-picks among candidates collect()
    has already resolved. Falls back to the longest `.first-principles/analysis-*.md` directly
    under `example_dir` when `report.md` is absent (an uncollected, OUT-style directory, as built
    by this module's own self-test fixtures)."""
    flattened = example_dir / "report.md"
    if flattened.is_file():
        return flattened, [flattened.name]
    analysis_dir = example_dir / ".first-principles"
    files = sorted(analysis_dir.glob("analysis-*.md")) if analysis_dir.is_dir() else []
    names = [f.name for f in files]
    if not files:
        return None, names
    longest = max(files, key=lambda p: len(p.read_text(errors="replace")))
    return longest, names


def determine_report(
    example_dir: Path, summary_row: dict, *, inline_writer=None,
) -> tuple[Path | None, list[str], str | None]:
    """select_report, plus the D-08 shortfall rule: zero analysis files is a shortfall whatever
    the row says, and an inline-only run's inline text is still checked (inline_writer writes it
    to raw/<name>/inline-report.md and returns its path), the shortfall label unchanged by
    whatever the checker then says of it."""
    report_path, names = select_report(example_dir)
    if report_path is not None:
        return report_path, names, None
    shortfall = "no delivered file (D-08)"
    if summary_row.get("analysis_inline") and inline_writer is not None:
        report_path = inline_writer(example_dir)
    return report_path, names, shortfall


def plugin_version(jsonl_text: str) -> str | None:
    for p in init_event(jsonl_text).get("plugins") or []:
        if p.get("name") == "first-principles":
            return p.get("version")
    return None


def _example_dirs(raw_dir: Path) -> list[str]:
    if not raw_dir.is_dir():
        return []
    return sorted(p.name for p in raw_dir.iterdir() if p.is_dir() and p.name != "state")


def _trace_cleared_after(raw_dir: Path, session: str | None) -> bool | None:
    """Informational: trace.py's stricter cleared (no Hand-wavy at all), read from
    raw/state/trace/<session>.jsonl's last run_end record, via run.py's own derive_gate."""
    if not session:
        return None
    trace_dir = raw_dir / "state" / "trace"
    gate = _ssl_run.derive_gate([{"example": "_probe", "session": session}], trace_dir)
    return gate.get("_probe")


# ---------------------------------------------------------------------------
# check -- checker pass per report, gate reading
# ---------------------------------------------------------------------------


def cmd_check(
    *,
    raw_dir: Path = RAW,
    manifest_path: Path = MANIFEST,
    checker_path: Path = REPO_ROOT / CHECKER,
    out_path: Path | None = None,
) -> int:
    if out_path is None:
        out_path = HERE / "checks.json"
    names = _example_dirs(raw_dir)
    if len(names) != 14:
        print(f"check: {raw_dir} holds {len(names)} example dir(s), expected 14", file=sys.stderr)
        return 2
    if not manifest_path.is_file():
        print(f"check: {manifest_path} absent", file=sys.stderr)
        return 2
    manifest = json.loads(manifest_path.read_text())
    actual_sha = checker_sha256(checker_path)
    if manifest.get("checker_sha256") != actual_sha:
        print(
            f"check: checker sha256 mismatch (manifest {manifest.get('checker_sha256')!r} != "
            f"actual {actual_sha!r}) -- refusing to read",
            file=sys.stderr,
        )
        return 2

    summary_path = raw_dir / "summary.json"
    summary_rows = json.loads(summary_path.read_text()) if summary_path.is_file() else []
    summary_by_name = {r["example"]: r for r in summary_rows}

    runner_mod = None

    def write_inline(example_dir: Path) -> Path | None:
        nonlocal runner_mod
        jsonl_path = example_dir / "run.jsonl"
        text = jsonl_path.read_text(errors="replace") if jsonl_path.is_file() else ""
        if runner_mod is None:
            runner_mod = _ssl_run.load_runner()
        inline_text = runner_mod.inline_report(events(text))
        if not inline_text:
            return None
        inline_path = example_dir / "inline-report.md"
        inline_path.write_text(inline_text)
        return inline_path

    checks: list[dict] = []
    for name in names:
        example_dir = raw_dir / name
        jsonl_path = example_dir / "run.jsonl"
        text = jsonl_path.read_text(errors="replace") if jsonl_path.is_file() else ""
        row = summary_by_name.get(name, {})
        report_path, candidate_names, shortfall = determine_report(example_dir, row, inline_writer=write_inline)

        entry: dict = {
            "example": name,
            "model": init_event(text).get("model"),
            "loaded_body": loaded_body(text),
            "plugin_version": plugin_version(text),
            "limit_stub": is_limit_stub(text),
            "report": str(report_path) if report_path else None,
            "report_candidates": candidate_names,
            "shortfall": shortfall,
            "read_own_example": bool(row.get("self_application")),
        }

        if report_path is not None:
            argv = checker_argv(str(report_path))
            proc = subprocess.run(argv, cwd=REPO_ROOT, capture_output=True, text=True)
            entry["checker_exit"] = proc.returncode
            try:
                doc = json.loads(proc.stdout)
                entry["checker_passed"] = doc.get("passed")
                reports = doc.get("reports") or []
                entry["checker_findings"] = reports[0].get("findings", []) if reports else []
            except json.JSONDecodeError:
                entry["checker_passed"] = False
                entry["checker_findings"] = []
            report_text = report_path.read_text(errors="replace")
            block = extract_block(report_text)
            entry["block_present"] = block is not None
            gate = block.get("gate") if isinstance(block, dict) else None
            entry["block_gate_cleared"] = gate.get("cleared") if isinstance(gate, dict) else None
            entry["block_gate_passes"] = (
                len(gate.get("passes") or []) if isinstance(gate, dict) and isinstance(gate.get("passes"), list) else None
            )
            re_entry = block.get("re_entry") if isinstance(block, dict) else None
            entry["block_re_entry_fired"] = re_entry.get("fired") if isinstance(re_entry, dict) else None
            conclusion = block.get("conclusion") if isinstance(block, dict) else None
            entry["block_conclusion_confidence"] = conclusion.get("confidence") if isinstance(conclusion, dict) else None
            entry["prose_gate_cleared"] = prose_gate_cleared(report_text)
            gate_findings_present = any(f.get("code") in GATE_CODES for f in entry["checker_findings"])
            entry["gate_cleared"] = gate_cleared_rule(block, entry["prose_gate_cleared"], gate_findings_present)
        else:
            entry.update({
                "checker_exit": None, "checker_passed": False, "checker_findings": [],
                "block_present": False, "block_gate_cleared": None, "block_gate_passes": None,
                "block_re_entry_fired": None, "block_conclusion_confidence": None,
                "prose_gate_cleared": None, "gate_cleared": False,
            })

        entry["trace_cleared_after"] = _trace_cleared_after(raw_dir, row.get("session"))
        checks.append(entry)

    out_path.write_text(json.dumps(checks, indent=2, sort_keys=True) + "\n")
    print(f"checked {len(checks)}/14")
    return 0


# ---------------------------------------------------------------------------
# crossread -- block vs agent-router's trace.py prose parser (R08)
# ---------------------------------------------------------------------------

_TRAILING_ELLIPSIS_RE = re.compile(r"(\.\.\.|…)\s*$")


def _strip_trailing_ellipsis(s: str) -> str:
    return _TRAILING_ELLIPSIS_RE.sub("", s)


def _gate_cleared_label(block: dict) -> str | None:
    """'parser_rule' when the block's final bands hold exactly one Hand-wavy and no Absent --
    trace.py's cleared rule rejects any Hand-wavy at all, stricter than the rubric."""
    gate = block.get("gate") if isinstance(block, dict) else None
    passes = gate.get("passes") if isinstance(gate, dict) else None
    if not isinstance(passes, list) or not passes:
        return None
    last = passes[-1]
    bands = last.get("bands") if isinstance(last, dict) else None
    if isinstance(bands, list) and bands.count("Hand-wavy") == 1 and "Absent" not in bands:
        return "parser_rule"
    return None


def crossread_example(block: dict, parsed: dict) -> list[dict]:
    """Every disagreement between the block and trace.py's parse_analysis(text) on the fields
    the protocol names, as {field, block, parser[, label]}. Equal values (including both sides
    absent) produce no entry."""
    out: list[dict] = []

    def cmp(field: str, b, p, label: str | None = None) -> None:
        if b is None and p is None:
            return
        if b != p:
            d = {"field": field, "block": b, "parser": p}
            if label:
                d["label"] = label
            out.append(d)

    cmp("run_mode", block.get("run_mode"), parsed.get("run_mode"))

    b_re = block.get("re_entry")
    p_re = parsed.get("re_entry")
    cmp(
        "re_entry.fired",
        b_re.get("fired") if isinstance(b_re, dict) else None,
        p_re.get("fired") if isinstance(p_re, dict) else None,
    )

    b_gate = block.get("gate") if isinstance(block.get("gate"), dict) else None
    p_gate = parsed.get("gate") if isinstance(parsed.get("gate"), dict) else None
    b_passes = (
        len(b_gate.get("passes") or []) if b_gate and isinstance(b_gate.get("passes"), list) else None
    )
    p_passes = p_gate.get("passes") if p_gate else None
    cmp("gate.passes", b_passes, p_passes)

    b_cleared = b_gate.get("cleared") if b_gate else None
    p_cleared = p_gate.get("cleared") if p_gate else None
    label = _gate_cleared_label(block) if b_cleared != p_cleared else None
    cmp("gate.cleared", b_cleared, p_cleared, label)

    b_chains = block.get("chains") if isinstance(block.get("chains"), list) else []
    p_chains = parsed.get("chains") if isinstance(parsed.get("chains"), list) else []
    p_chain_by_id = {c.get("id"): c for c in p_chains if isinstance(c, dict)}
    for c in b_chains:
        if not isinstance(c, dict):
            continue
        cid = c.get("id")
        pc = p_chain_by_id.get(cid)
        cmp(f"chains.{cid}.confidence", c.get("confidence"), pc.get("confidence") if pc else None)

    b_gts = block.get("ground_truths") if isinstance(block.get("ground_truths"), list) else None
    p_gts = parsed.get("ground_truths") if isinstance(parsed.get("ground_truths"), dict) else None
    if b_gts is not None or p_gts is not None:
        b_unverified = {
            g.get("id") for g in (b_gts or []) if isinstance(g, dict) and g.get("read_at_source") is False
        }
        p_unverified = {str(g).rstrip("?") for g in (p_gts or {}).get("unverified", [])}
        cmp("ground_truths.unverified", b_unverified, p_unverified)

    b_assumptions = block.get("assumptions")
    p_assumptions = parsed.get("assumptions")
    if b_assumptions is not None or p_assumptions is not None:
        b_count = len(b_assumptions) if isinstance(b_assumptions, list) else None
        p_count = p_assumptions.get("count") if isinstance(p_assumptions, dict) else None
        cmp("assumptions.count", b_count, p_count)

    b_conc = block.get("conclusion") if isinstance(block.get("conclusion"), dict) else {}
    p_conc = parsed.get("conclusion") if isinstance(parsed.get("conclusion"), dict) else {}
    cmp("conclusion.confidence", b_conc.get("confidence"), p_conc.get("confidence"))

    b_rec = b_conc.get("recommendation")
    p_rec = p_conc.get("recommended")
    if b_rec is not None or p_rec is not None:
        if b_rec != p_rec:
            rec_label = None
            if isinstance(b_rec, str) and isinstance(p_rec, str):
                stripped = _strip_trailing_ellipsis(p_rec)
                if len(stripped) < 400 and stripped != b_rec and b_rec.startswith(stripped):
                    rec_label = "parser_cut"
            entry = {"field": "conclusion.recommendation", "block": b_rec, "parser": p_rec}
            if rec_label:
                entry["label"] = rec_label
            out.append(entry)

    return out


def cmd_crossread(
    *,
    checks_path: Path | None = None,
    ar_trace_path: Path = AR_DIR / "trace.py",
    out_path: Path | None = None,
) -> int:
    if checks_path is None:
        checks_path = HERE / "checks.json"
    if out_path is None:
        out_path = HERE / "crossread.json"
    if not checks_path.is_file():
        print("crossread: checks.json missing -- run `check` first", file=sys.stderr)
        return 2
    checks = json.loads(checks_path.read_text())
    spec = importlib.util.spec_from_file_location("_ar_trace", ar_trace_path)
    assert spec and spec.loader
    ar_trace = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ar_trace)

    result: dict[str, list[dict]] = {}
    for entry in checks:
        name = entry["example"]
        report = entry.get("report")
        if not report:
            continue
        text = Path(report).read_text(errors="replace")
        block = extract_block(text) or {}
        parsed = ar_trace.parse_analysis(text)
        result[name] = crossread_example(block, parsed)

    out_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    total = sum(len(v) for v in result.values())
    print(f"crossread: {total} disagreement(s) across {len(result)} example(s)")
    return 0


# ---------------------------------------------------------------------------
# table -- before/after Markdown table
# ---------------------------------------------------------------------------


def cmd_table(
    *,
    raw_dir: Path = RAW,
    base_dir: Path = BASE,
    checks_path: Path | None = None,
    out_path: Path | None = None,
) -> int:
    if checks_path is None:
        checks_path = HERE / "checks.json"
    if out_path is None:
        out_path = HERE / "result.json"
    if not checks_path.is_file() or not (raw_dir / "summary.json").is_file():
        print("table: checks.json or raw/summary.json missing -- run `check` first", file=sys.stderr)
        return 2
    checks = {c["example"]: c for c in json.loads(checks_path.read_text())}
    after_rows = {r["example"]: r for r in json.loads((raw_dir / "summary.json").read_text())}
    before_summary = base_dir / "summary.json"
    before_rows = (
        {r["example"]: r for r in json.loads(before_summary.read_text())} if before_summary.is_file() else {}
    )
    before_gate: dict = {}
    gate_path = base_dir / "gate.json"
    if gate_path.is_file():
        before_gate = json.loads(gate_path.read_text()).get("cleared", {})

    names = sorted(set(after_rows) | set(checks))
    lines = [
        "| example | before: status · cost $ · words · turns · gate | "
        "after: status · block present · checker · cost $ · words · turns "
        "· gate · trace.py gate |",
        "|---|---|---|",
    ]
    rows_out = []
    after_costs: list[float] = []
    after_words: list[float] = []
    before_costs: list[float] = []
    before_words: list[float] = []
    for name in names:
        b = before_rows.get(name, {})
        a = after_rows.get(name, {})
        c = checks.get(name, {})
        mark = "†" if c.get("read_own_example") else ""
        before_gate_cell = "cleared" if before_gate.get(name) else ("not cleared" if name in before_gate else "—")
        before_cell = (
            f"{b.get('status', '—')} · ${b.get('cost_usd', 0):.4f} · "
            f"{b.get('words', '—')} · {b.get('turns', '—')} · {before_gate_cell}"
        )
        after_trace_cell = (
            "cleared" if c.get("trace_cleared_after") else ("not cleared" if c.get("trace_cleared_after") is False else "—")
        )
        after_cell = (
            f"{a.get('status', '—')} · {'yes' if c.get('block_present') else 'no'} · "
            f"{'PASS' if c.get('checker_exit') == 0 else 'FAIL'} · ${a.get('cost_usd', 0):.4f} · "
            f"{a.get('words', '—')} · {a.get('turns', '—')} · "
            f"{'cleared' if c.get('gate_cleared') else 'not cleared'} · {after_trace_cell}"
        )
        lines.append(f"| {name}{mark} | {before_cell} | {after_cell} |")
        rows_out.append({"example": name, "before": b, "after": a, "checks": c})
        if isinstance(a.get("cost_usd"), (int, float)):
            after_costs.append(a["cost_usd"])
        if isinstance(a.get("words"), (int, float)):
            after_words.append(a["words"])
        if isinstance(b.get("cost_usd"), (int, float)):
            before_costs.append(b["cost_usd"])
        if isinstance(b.get("words"), (int, float)):
            before_words.append(b["words"])

    print("\n".join(lines))
    if after_costs:
        print(f"\nafter median cost: ${statistics.median(after_costs):.4f} (n={len(after_costs)})")
    if before_costs:
        print(f"before median cost: ${statistics.median(before_costs):.4f} (n={len(before_costs)})")
    if after_words:
        print(f"after median words: {statistics.median(after_words):.4f} (n={len(after_words)})")
    if before_words:
        print(f"before median words: {statistics.median(before_words):.4f} (n={len(before_words)})")

    out_path.write_text(json.dumps(rows_out, indent=2, sort_keys=True) + "\n")
    return 0


# --- --self-test -- R01-R09, offline, no network, no `claude`, no real checker subprocess ------


def _r01() -> tuple[bool, str]:
    good = f"## Appendix — process output\n\n{HEADING}\n\n```json\n" + json.dumps({"schema_version": 1, "a": 1}) + "\n```\n"
    block = extract_block(good)
    if block != {"schema_version": 1, "a": 1}:
        return False, f"expected the parsed dict, got {block!r}"
    no_heading = "## Appendix — process output\n\nsome text\n```json\n{}\n```\n"
    if extract_block(no_heading) is not None:
        return False, "expected None with no heading"
    malformed = f"{HEADING}\n\n```json\n{{not valid json\n```\n"
    if extract_block(malformed) is not None:
        return False, "expected None on malformed JSON"
    return True, ""


def _r02() -> tuple[bool, str]:
    cleared = "intro\n**Gate result:** cleared · passes: 2 · Fix/Repeat fired: yes\n"
    if prose_gate_cleared(cleared) is not True:
        return False, "expected True for a 'cleared' line"
    not_cleared = "intro\n**Gate result:** not cleared · passes: 1 · Fix/Repeat fired: no\n"
    if prose_gate_cleared(not_cleared) is not False:
        return False, "expected False for a 'not cleared' line"
    absent = "no gate result line here\n"
    if prose_gate_cleared(absent) is not None:
        return False, "expected None when the line is absent"
    two_lines = (
        "**Gate result:** not cleared · passes: 1 · Fix/Repeat fired: no\n"
        "...\n"
        "**Gate result:** cleared · passes: 2 · Fix/Repeat fired: yes\n"
    )
    if prose_gate_cleared(two_lines) is not True:
        return False, "expected the LAST Gate result line to decide"
    return True, ""


def _r03() -> tuple[bool, str]:
    block_true = {"gate": {"cleared": True}}
    if gate_cleared_rule(block_true, True, False) is not True:
        return False, "block true + prose True + no finding -> expected cleared"
    if gate_cleared_rule(block_true, True, True) is not False:
        return False, "block true + prose True + a gate finding -> expected not cleared"
    if gate_cleared_rule(block_true, None, False) is not False:
        return False, "block true + prose None -> expected not cleared"
    if gate_cleared_rule(None, True, False) is not False:
        return False, "block missing -> expected not cleared"
    return True, ""


def _r04() -> tuple[bool, str]:
    rows_299 = [{"cost_usd": 2.99} for _ in range(14)]
    ok, median = cost_leg(rows_299)
    if not ok or median is None or abs(median - 2.99) > 1e-9:
        return False, f"2.99 median expected to pass, got ok={ok} median={median}"
    rows_300 = [{"cost_usd": 3.00} for _ in range(14)]
    ok, median = cost_leg(rows_300)
    if not ok:
        return False, "3.00 median expected to pass (<= the ceiling)"
    rows_30001 = [{"cost_usd": 3.0001} for _ in range(14)]
    ok, median = cost_leg(rows_30001)
    if ok:
        return False, "3.0001 median expected to FAIL"
    rows_null = [{"cost_usd": 2.0}] * 13 + [{"cost_usd": None}]
    ok, median = cost_leg(rows_null)
    if ok:
        return False, "a null cost_usd row must fail the cost leg outright"
    return True, ""


def _r05() -> tuple[bool, str]:
    checks_13 = [{"example": f"ex{i}", "checker_exit": 0, "shortfall": None} for i in range(13)] + [
        {"example": "ex13", "checker_exit": 1, "shortfall": None}
    ]
    ok, _ = blocks_leg(checks_13)
    if ok:
        return False, "13/14 checker passes must FAIL the blocks leg"
    checks_14 = [{"example": f"ex{i}", "checker_exit": 0, "shortfall": None} for i in range(14)]
    ok, _ = blocks_leg(checks_14)
    if not ok:
        return False, "14/14 checker passes must PASS the blocks leg"

    summary_bad = [{"example": f"ex{i}", "status": "complete"} for i in range(13)] + [
        {"example": "ex13", "status": "failed"}
    ]
    checks_bodies_ok = [{"example": f"ex{i}", "loaded_body": [str(EXPECTED_PLUGIN)]} for i in range(14)]
    ok, _ = runs_leg(summary_bad, checks_bodies_ok, str(EXPECTED_PLUGIN))
    if ok:
        return False, "a non-complete row must FAIL the runs leg"

    summary_ok = [{"example": f"ex{i}", "status": "complete"} for i in range(14)]
    checks_bodies_bad = [{"example": f"ex{i}", "loaded_body": [str(EXPECTED_PLUGIN)]} for i in range(13)] + [
        {"example": "ex13", "loaded_body": ["/wrong/path"]}
    ]
    ok, _ = runs_leg(summary_ok, checks_bodies_bad, str(EXPECTED_PLUGIN))
    if ok:
        return False, "a wrong loaded_body must FAIL the runs leg"
    ok, _ = runs_leg(summary_ok, checks_bodies_ok, str(EXPECTED_PLUGIN))
    if not ok:
        return False, "14 complete rows with correct bodies must PASS the runs leg"

    with tempfile.TemporaryDirectory() as tmp:
        tmp_raw = Path(tmp) / "raw"
        tmp_raw.mkdir()
        (tmp_raw / "summary.json").write_text(json.dumps(summary_ok))
        checks_path = Path(tmp) / "checks.json"
        checks_path.write_text(json.dumps(checks_13))
        rc = cmd_verdict("blocks", raw_dir=tmp_raw, checks_path=checks_path, expected_plugin=str(EXPECTED_PLUGIN))
        if rc != 1:
            return False, f"cmd_verdict blocks leg with 13/14 passes: expected exit 1, got {rc}"
        checks_path.write_text(json.dumps(checks_14))
        rc = cmd_verdict("blocks", raw_dir=tmp_raw, checks_path=checks_path, expected_plugin=str(EXPECTED_PLUGIN))
        if rc != 0:
            return False, f"cmd_verdict blocks leg with 14/14 passes: expected exit 0, got {rc}"
    return True, ""


def _r06() -> tuple[bool, str]:
    argv = checker_argv("path/to/report.md")
    if argv != ["python3", CHECKER, "--json", "path/to/report.md"]:
        return False, f"unexpected argv {argv!r}"
    if "--exemplar" in argv or "--schema" in argv:
        return False, "forbidden flag present in the constructed argv"
    return True, ""


def _r07() -> tuple[bool, str]:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        raw_dir = tmp_path / "raw"
        raw_dir.mkdir()
        for i in range(13):
            (raw_dir / f"ex{i}").mkdir()
        checker_path = tmp_path / "checker.py"
        checker_path.write_text("# fake checker\n")
        real_sha = checker_sha256(checker_path)
        manifest_path = tmp_path / "manifest.json"
        manifest_path.write_text(json.dumps({"checker_sha256": real_sha}))
        out_path = tmp_path / "checks.json"

        rc = cmd_check(raw_dir=raw_dir, manifest_path=manifest_path, checker_path=checker_path, out_path=out_path)
        if rc != 2:
            return False, f"expected exit 2 with 13 example dirs, got {rc}"

        (raw_dir / "ex13").mkdir()  # now 14 dirs; pin still correct
        manifest_path.write_text(json.dumps({"checker_sha256": "0" * 64}))  # now mismatched
        rc2 = cmd_check(raw_dir=raw_dir, manifest_path=manifest_path, checker_path=checker_path, out_path=out_path)
        if rc2 != 2:
            return False, f"expected exit 2 on checker sha256 mismatch, got {rc2}"
    return True, ""


def _r08() -> tuple[bool, str]:
    block1 = {"re_entry": {"fired": False}}
    parsed1 = {"re_entry": {"fired": True}}
    diffs1 = crossread_example(block1, parsed1)
    matches1 = [d for d in diffs1 if d["field"] == "re_entry.fired"]
    if matches1 != [{"field": "re_entry.fired", "block": False, "parser": True}]:
        return False, f"expected one re_entry.fired disagreement, got {diffs1!r}"

    block2 = {"gate": {"passes": [{}, {}]}}
    parsed2 = {"gate": {"passes": 1}}
    diffs2 = crossread_example(block2, parsed2)
    matches2 = [d for d in diffs2 if d["field"] == "gate.passes"]
    if len(matches2) != 1 or matches2[0]["block"] != 2 or matches2[0]["parser"] != 1:
        return False, f"expected one gate.passes disagreement (2 vs 1), got {diffs2!r}"

    long_rec = "Recommendation sentence one. " * 5 + "And a tail that keeps going well past the first line."
    cut_rec = long_rec.split(".")[0] + "."
    block3 = {"conclusion": {"recommendation": long_rec}}
    parsed3 = {"conclusion": {"recommended": cut_rec}}
    diffs3 = crossread_example(block3, parsed3)
    matches3 = [d for d in diffs3 if d["field"] == "conclusion.recommendation"]
    if len(matches3) != 1 or matches3[0].get("label") != "parser_cut":
        return False, f"expected conclusion.recommendation flagged parser_cut, got {diffs3!r}"

    block4 = {
        "run_mode": "full-composer",
        "re_entry": {"fired": False},
        "gate": {"passes": [{}], "cleared": True},
        "conclusion": {"confidence": "HIGH", "recommendation": "Do X."},
    }
    parsed4 = {
        "run_mode": "full-composer",
        "re_entry": {"fired": False},
        "gate": {"passes": 1, "cleared": True},
        "conclusion": {"confidence": "HIGH", "recommended": "Do X."},
    }
    diffs4 = crossread_example(block4, parsed4)
    if diffs4:
        return False, f"expected no disagreements on equal values, got {diffs4!r}"
    return True, ""


def _r09() -> tuple[bool, str]:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        example_dir = tmp_path / "ex-multi"
        d = example_dir / ".first-principles"
        d.mkdir(parents=True)
        (d / "analysis-a.md").write_text("short")
        (d / "analysis-b.md").write_text("a much longer report body text here")
        report, names = select_report(example_dir)
        if report is None or report.name != "analysis-b.md":
            return False, f"expected the longer file chosen, got {report!r}"
        if sorted(names) != ["analysis-a.md", "analysis-b.md"]:
            return False, f"expected both file names recorded, got {names!r}"

        none_dir = tmp_path / "ex-none"
        none_dir.mkdir()
        calls: list[Path] = []

        def fake_writer(ex_dir: Path) -> Path:
            calls.append(ex_dir)
            p = ex_dir / "inline-report.md"
            p.write_text("whatever the checker would say of this text")
            return p

        report2, _names2, shortfall2 = determine_report(none_dir, {"analysis_inline": True}, inline_writer=fake_writer)
        if shortfall2 != "no delivered file (D-08)":
            return False, f"expected the D-08 shortfall label, got {shortfall2!r}"
        if not calls or report2 is None:
            return False, "expected the inline writer to be invoked and its path returned"

        report3, _names3, shortfall3 = determine_report(none_dir, {"analysis_inline": False}, inline_writer=fake_writer)
        if shortfall3 != "no delivered file (D-08)":
            return False, f"expected the D-08 shortfall label without an inline capture, got {shortfall3!r}"
        if report3 is not None:
            return False, "no analysis file and no inline capture must leave the report absent"
    return True, ""


_PROTOCOL_PATH = REPO_ROOT / "docs" / "structured-summary-live-protocol.md"
_PHASE75_CLOSE_RE = re.compile(r"PHASE75_CLOSE\s*=\s*`?([0-9a-f]{40})`?")


def _r10() -> tuple[bool, str]:
    """Every constant the protocol quotes agrees with run.py/read.py's own constants, and
    PHASE75_CLOSE is a real, resolvable commit."""
    if not _PROTOCOL_PATH.is_file():
        return False, f"{_PROTOCOL_PATH} is absent"
    text = _PROTOCOL_PATH.read_text()
    required = [
        f"--entry {ENTRY} --jobs {JOBS} --fp-repo {FP_REPO}",
        "runs/structured-summary-live",
        "$3.00",
        "2.7343755",
        "at most 3",
        "**Id:** `structured-summary-live`",
    ]
    missing = [r for r in required if r not in text]
    if missing:
        return False, f"protocol missing verbatim literal(s): {missing!r}"
    m = _PHASE75_CLOSE_RE.search(text)
    if m is None:
        return False, "no 'PHASE75_CLOSE = <sha>' text found in the protocol"
    sha = m.group(1)
    if len(sha) != 40:
        return False, f"PHASE75_CLOSE {sha!r} is not a 40-hex SHA"
    check = subprocess.run(["git", "cat-file", "-e", sha], cwd=REPO_ROOT, capture_output=True)
    if check.returncode != 0:
        return False, f"git cat-file -e rejects PHASE75_CLOSE {sha!r}"
    return True, ""


_CONTROLS: list[tuple[str, object]] = [
    ("R01", _r01), ("R02", _r02), ("R03", _r03), ("R04", _r04), ("R05", _r05),
    ("R06", _r06), ("R07", _r07), ("R08", _r08), ("R09", _r09), ("R10", _r10),
]


def self_test() -> int:
    results = []
    for name, fn in _CONTROLS:
        try:
            ok, reason = fn()  # type: ignore[operator]
        except Exception as e:  # noqa: BLE001 -- a control's own assertion failure is a FAIL, not a crash
            ok, reason = False, f"{type(e).__name__}: {e}"
        results.append((name, ok))
        suffix = f" {reason}" if not ok and reason else ""
        print(f"  {'PASS' if ok else 'FAIL'}  [{name}]{suffix}")
    passed = sum(ok for _, ok in results)
    verdict = "PASS" if passed == len(results) else "FAIL"
    print(f"STRUCTURED-SUMMARY-LIVE READ SELF-TEST: {verdict} ({passed}/{len(results)} controls)")
    return 0 if passed == len(results) else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    sub = ap.add_subparsers(dest="command")
    sub.add_parser("check")
    sub.add_parser("crossread")
    sub.add_parser("table")
    verdict_p = sub.add_parser("verdict")
    verdict_p.add_argument("--leg", choices=("runs", "blocks", "gate", "cost", "all"), default="all")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if args.command == "check":
        return cmd_check()
    if args.command == "crossread":
        return cmd_crossread()
    if args.command == "table":
        return cmd_table()
    if args.command == "verdict":
        return cmd_verdict(getattr(args, "leg", "all"))
    ap.error("a command or --self-test is required")


if __name__ == "__main__":
    raise SystemExit(main())
