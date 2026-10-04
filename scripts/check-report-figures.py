#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""FIG-GATE: offline self-test for the typst report-figures library.

Extracts the one fenced ```typst block from the SHIPPED source
(`shared/spine/references/report-figures.md`, never a copy) using the exact
awk one-liner the agent body itself runs, renders both figures
(`evidence-trace` and `assumption-verdict-matrix`) against the two tracked
fixtures under `tests/report-figures-v9.17/` plus every structured-summary
block in `shared/examples/*.md`, and asserts the typst `#metadata` counts
each figure stamps against counts independently re-derived straight from the
fixture JSON -- never from the drawn SVG geometry. FIG-01 through FIG-05 name
the requirements this mechanises; this module's own finding codes are
FIG-EXTRACT, FIG-FIXTURE, FIG-COMPILE, FIG-METADATA, FIG-GTS, FIG-CHAINS,
FIG-EDGES, FIG-CONCL-EDGES, FIG-CELLS, FIG-OVERFLOW, FIG-SVG, FIG-FONT and
FIG-ANCHOR.

Two-layer BLOCKED design (see Pitfall 1 in the phase research): this script's
own `--self-test`/`--render` exit with code 1 (RED, since Phase 89 plan 01;
previously 2) and print BLOCKED the moment typst is absent from PATH, before
any other work -- a directly self-testable contract (control B01). The battery's own [PREREQ] verdict is a SEPARATE
bash-level decision (`command -v typst`) made by the caller, not derived from
this exit code; `--describe` is typst-independent so it still answers when
typst is absent.

Usage:
    python3 scripts/check-report-figures.py --self-test
    python3 scripts/check-report-figures.py --describe
    python3 scripts/check-report-figures.py --render DIR
"""
from __future__ import annotations

import argparse
import copy
import glob
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LIBRARY = REPO_ROOT / "shared" / "spine" / "references" / "report-figures.md"
TWIN = REPO_ROOT / "first-principles" / "references" / "report-figures.md"
FIXTURE_DIR = REPO_ROOT / "tests" / "report-figures-v9.17"
FIXTURES: tuple[str, ...] = ("analysis-20261001T204943Z.json", "worst-case-labels.json")
EXAMPLES_GLOB = str(REPO_ROOT / "shared" / "examples" / "*.md")
MAX_WIDTH_PT = 470
FONTS: tuple[str, ...] = ("Noto Sans", "Liberation Sans")

# Closed set of finding codes. FIG-EXTRACT/FIG-FIXTURE/FIG-COMPILE/FIG-FONT
# are the four U04 exempts from the "must be observed by some control" rule
# -- each one fires only on a defect in the shipped source, a fixture, a
# typst invocation, or the local font install, none of which this self-test
# mutates on a healthy run (observing them would mean the shipped tree is
# already broken).
FINDING_CODES: tuple[str, ...] = (
    "FIG-EXTRACT",
    "FIG-FIXTURE",
    "FIG-COMPILE",
    "FIG-METADATA",
    "FIG-GTS",
    "FIG-CHAINS",
    "FIG-EDGES",
    "FIG-CONCL-EDGES",
    "FIG-CELLS",
    "FIG-OVERFLOW",
    "FIG-SVG",
    "FIG-FONT",
    "FIG-ANCHOR",
)

_EXEMPT_FROM_OBSERVATION = frozenset({"FIG-EXTRACT", "FIG-FIXTURE", "FIG-COMPILE", "FIG-FONT"})

_REQUIRED_METADATA_KEYS: dict[str, tuple[str, ...]] = {
    "trace": ("gts", "chains", "edges", "conclusion_edges", "overflow", "width"),
    "verdicts": ("cells", "total", "untyped", "grid", "overflow", "width"),
}

_AWK_PROGRAM = '/^```typst$/ { f = 1; next } f && /^```$/ { exit } f'
_WIDTH_RE = re.compile(r"^([0-9.]+)pt$")


@dataclass(frozen=True)
class Finding:
    code: str
    subject: str
    detail: str


# ---------------------------------------------------------------------------
# check-summary-block.py loader (importlib precedent: check-summary-block.py
# _load_qh) -- reused for find_blocks/load_schema/validate_report, never
# re-implemented.
# ---------------------------------------------------------------------------

_SB = None


def sb():
    global _SB
    if _SB is None:
        spec = importlib.util.spec_from_file_location(
            "_sb_for_report_figures", REPO_ROOT / "scripts" / "check-summary-block.py")
        mod = importlib.util.module_from_spec(spec)
        sys.modules["_sb_for_report_figures"] = mod
        spec.loader.exec_module(mod)
        _SB = mod
    return _SB


_SCHEMA = None


def _schema() -> dict:
    global _SCHEMA
    if _SCHEMA is None:
        _SCHEMA = sb().load_schema(sb().DEFAULT_SCHEMA)
    return _SCHEMA


def _types() -> tuple[str, ...]:
    return tuple(_schema()["fields"]["assumptions"]["items"]["fields"]["type"]["enum"])


def _verdicts() -> tuple[str, ...]:
    return tuple(_schema()["fields"]["assumptions"]["items"]["fields"]["verdict"]["enum"])


def _relpath(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _safe_name(label: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", label)


def require_typst() -> str | None:
    return shutil.which("typst")


# ---------------------------------------------------------------------------
# Extraction
# ---------------------------------------------------------------------------

def _awk_extract(path: Path) -> str:
    result = subprocess.run(
        ["awk", _AWK_PROGRAM, str(path)],
        capture_output=True, text=True, check=True,
    )
    return result.stdout


def extract_library(path: Path) -> tuple[str, list[Finding]]:
    """Extract the fenced ```typst block via the identical awk one-liner the
    agent body itself runs. FIG-EXTRACT if the source does not hold exactly
    one `^```typst$` line, or if the twin's extracted bytes differ from the
    source's."""
    findings: list[Finding] = []
    text = path.read_text()
    fence_count = sum(1 for line in text.split("\n") if line == "```typst")
    extracted = _awk_extract(path)
    if fence_count != 1:
        findings.append(Finding(
            "FIG-EXTRACT", _relpath(path),
            f"expected exactly one ```typst fence line, found {fence_count}"))
    if path == LIBRARY and TWIN.exists():
        twin_extracted = _awk_extract(TWIN)
        if twin_extracted != extracted:
            findings.append(Finding(
                "FIG-EXTRACT", _relpath(TWIN),
                "twin's extracted typst block differs from the shipped source's"))
    return extracted, findings


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def load_fixtures() -> tuple[list[tuple[str, dict]], list[Finding]]:
    """Returns (label, summary) pairs: the two tracked JSON fixtures, then
    every shared/examples/*.md structured-summary block (sorted by
    filename). A fixture that fails to parse or fails schema validation is
    FIG-FIXTURE, not silently skipped."""
    findings: list[Finding] = []
    pairs: list[tuple[str, dict]] = []
    schema = _schema()

    for name in FIXTURES:
        path = FIXTURE_DIR / name
        label = _relpath(path)
        try:
            val = json.loads(path.read_text())
        except (OSError, json.JSONDecodeError) as exc:
            findings.append(Finding("FIG-FIXTURE", label, f"cannot read/parse: {exc}"))
            continue
        violations = sb().validate_report(val, schema, exemplar=False)
        if violations:
            findings.append(Finding(
                "FIG-FIXTURE", label,
                f"schema violations: {[v.code for v in violations]}"))
            continue
        pairs.append((label, val))

    for path_str in sorted(glob.glob(EXAMPLES_GLOB)):
        path = Path(path_str)
        label = _relpath(path)
        text = path.read_text()
        blocks = sb().find_blocks(text)
        if len(blocks) != 1:
            findings.append(Finding(
                "FIG-FIXTURE", label,
                f"expected exactly one structured-summary block, found {len(blocks)}"))
            continue
        try:
            val = json.loads(blocks[0].body)
        except json.JSONDecodeError as exc:
            findings.append(Finding("FIG-FIXTURE", label, f"malformed JSON: {exc}"))
            continue
        violations = sb().validate_report(val, schema, exemplar=True)
        if violations:
            findings.append(Finding(
                "FIG-FIXTURE", label,
                f"schema violations: {[v.code for v in violations]}"))
            continue
        pairs.append((label, val))

    return pairs, findings


def _real_fixture() -> tuple[str, dict]:
    path = FIXTURE_DIR / FIXTURES[0]
    return _relpath(path), json.loads(path.read_text())


# ---------------------------------------------------------------------------
# Fonts
# ---------------------------------------------------------------------------

def font_findings(typst_bin: str) -> list[Finding]:
    result = subprocess.run([typst_bin, "fonts"], capture_output=True, text=True, check=False)
    lines = {line.strip() for line in result.stdout.split("\n")}
    if not any(font in lines for font in FONTS):
        return [Finding("FIG-FONT", "typst fonts", f"none of {FONTS} found in `typst fonts` output")]
    return []


# ---------------------------------------------------------------------------
# Render and metadata readback
# ---------------------------------------------------------------------------

def render(
    lib_text: str, summary: dict, figure: str, workdir: Path, *,
    fmt: str = "svg", extra_args: list[str] | None = None,
) -> tuple[Path | None, list[Finding]]:
    lib_path = workdir / "figures.typ"
    lib_path.write_text(lib_text)
    out_path = workdir / f"out.{fmt}"
    argv = (
        ["typst", "compile", "--format", fmt]
        + (extra_args or [])
        + ["--input", f"figure={figure}", "--input", f"summary={json.dumps(summary)}",
           str(lib_path), str(out_path)]
    )
    result = subprocess.run(argv, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        first_line = next(iter(result.stderr.strip().split("\n")), "")
        return None, [Finding("FIG-COMPILE", figure, first_line)]
    return out_path, []


def _parse_metadata_output(stdout: str, figure: str) -> tuple[dict | None, list[Finding]]:
    """Pure parsing/validation of a `typst eval 'query(...)'` readback,
    split out of read_metadata so control U02 can exercise it directly with
    fabricated stdout, with no typst subprocess involved."""
    try:
        data = json.loads(stdout)
    except json.JSONDecodeError as exc:
        return None, [Finding("FIG-METADATA", figure, f"non-JSON metadata output: {exc}")]
    if not isinstance(data, dict):
        return None, [Finding("FIG-METADATA", figure, f"metadata is not an object: {type(data).__name__}")]
    findings: list[Finding] = []
    for key in _REQUIRED_METADATA_KEYS[figure]:
        if key not in data:
            findings.append(Finding("FIG-METADATA", figure, f"missing required key: {key}"))
            continue
        if key == "grid":
            if not (isinstance(data[key], list)
                    and all(isinstance(x, int) and not isinstance(x, bool) for x in data[key])):
                findings.append(Finding("FIG-METADATA", figure, "grid is not a list of ints"))
        elif not isinstance(data[key], int) or isinstance(data[key], bool):
            findings.append(Finding("FIG-METADATA", figure, f"{key} is not an int: {data[key]!r}"))
    if findings:
        return None, findings
    return data, []


def read_metadata(lib_path: Path, summary: dict, figure: str) -> tuple[dict | None, list[Finding]]:
    label = "<fig-trace>" if figure == "trace" else "<fig-verdicts>"
    argv = [
        "typst", "eval", f"query({label}).first().value", "--in", str(lib_path),
        "--input", f"summary={json.dumps(summary)}", "--input", f"figure={figure}",
    ]
    result = subprocess.run(argv, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        first_line = next(iter(result.stderr.strip().split("\n")), "")
        return None, [Finding("FIG-METADATA", figure, f"typst eval failed: {first_line}")]
    return _parse_metadata_output(result.stdout.strip(), figure)


# ---------------------------------------------------------------------------
# Independent expectations and comparisons
# ---------------------------------------------------------------------------

def expected_trace(summary: dict) -> dict:
    gts = summary.get("ground_truths") or []
    chains = summary.get("chains") or []
    # The library draws an edge only for a citation that resolves to a declared
    # ground truth or chain (a trailing ? marks an unverified GT, not another id);
    # count the same set, so a dangling citation is not expected as a drawn edge
    # (81-REVIEW WR-01).
    known = {g.get("id") for g in gts} | {c.get("id") for c in chains}

    def _resolves(ref: str) -> bool:
        return (ref.removesuffix("?")) in known

    edges = sum(1 for c in chains for r in (c.get("rests_on") or []) if _resolves(r))
    concl = summary.get("conclusion") or {}
    conclusion_edges = sum(1 for r in (concl.get("rests_on") or []) if _resolves(r))
    return {"gts": len(gts), "chains": len(chains), "edges": edges, "conclusion_edges": conclusion_edges}


def expected_verdicts(summary: dict) -> dict:
    types = _types()
    verdicts = _verdicts()
    assumptions = summary.get("assumptions") or []
    grid = [
        sum(1 for a in assumptions if a.get("type") == t and a.get("verdict") == v)
        for t in types for v in verdicts
    ]
    untyped = sum(1 for a in assumptions if a.get("type") is None)
    return {"cells": 12, "total": len(assumptions), "untyped": untyped, "grid": grid}


def compare_trace(actual: dict, expected: dict) -> list[Finding]:
    findings: list[Finding] = []
    for key, code in (
        ("gts", "FIG-GTS"), ("chains", "FIG-CHAINS"),
        ("edges", "FIG-EDGES"), ("conclusion_edges", "FIG-CONCL-EDGES"),
    ):
        if actual.get(key) != expected.get(key):
            findings.append(Finding(code, key, f"expected {expected.get(key)}, got {actual.get(key)}"))
    if actual.get("overflow", 0) > 0:
        findings.append(Finding("FIG-OVERFLOW", "trace", f"overflow={actual.get('overflow')}"))
    return findings


def compare_verdicts(actual: dict, expected: dict) -> list[Finding]:
    findings: list[Finding] = []
    mismatched = [
        key for key in ("total", "untyped", "grid")
        if actual.get(key) != expected.get(key)
    ]
    if actual.get("cells") != 12:
        mismatched.append("cells")
    if mismatched:
        findings.append(Finding("FIG-CELLS", "verdicts", f"mismatched dimensions: {mismatched}"))
    if actual.get("overflow", 0) > 0:
        findings.append(Finding("FIG-OVERFLOW", "verdicts", f"overflow={actual.get('overflow')}"))
    return findings


# typst's `#set page(margin: 6pt)` in the library adds this on each side.
PAGE_MARGIN_PT = 6


def check_svg(text: str, declared_width: int | None = None) -> list[Finding]:
    try:
        root = ET.fromstring(text)
    except ET.ParseError as exc:
        return [Finding("FIG-SVG", "svg", f"malformed XML: {exc}")]
    if not root.tag.endswith("svg"):
        return [Finding("FIG-SVG", "svg", f"root element is not <svg>: {root.tag}")]
    if "viewBox" not in root.attrib:
        return [Finding("FIG-SVG", "svg", "missing viewBox attribute")]
    width = root.attrib.get("width", "")
    m = _WIDTH_RE.match(width)
    if not m:
        return [Finding("FIG-SVG", "svg", f"width attribute not in Npt form: {width!r}")]
    if float(m.group(1)) > MAX_WIDTH_PT:
        return [Finding("FIG-SVG", "svg", f"width {width} exceeds {MAX_WIDTH_PT}pt ceiling")]
    # The canvas must be the figure's own declared width plus the page margin: anything
    # wider means some element (a legend, a label) spilled past the figure (81-REVIEW CR-01).
    if declared_width is not None:
        want = declared_width + 2 * PAGE_MARGIN_PT
        if abs(float(m.group(1)) - want) > 1.0:
            return [Finding(
                "FIG-SVG", "svg",
                f"width {width} is not the declared {declared_width}pt plus {2 * PAGE_MARGIN_PT}pt margin ({want}pt)")]
    return []


def _with_subject(findings: list[Finding], label: str, figure: str) -> list[Finding]:
    return [Finding(f.code, f"{label}:{figure}:{f.subject}", f.detail) for f in findings]


def check_all(lib_text: str, fixtures: list[tuple[str, dict]], workdir: Path) -> list[Finding]:
    findings: list[Finding] = []
    for label, summary in fixtures:
        for figure in ("trace", "verdicts"):
            fig_dir = workdir / _safe_name(label) / figure
            fig_dir.mkdir(parents=True, exist_ok=True)
            lib_path = fig_dir / "figures.typ"
            out_path, compile_findings = render(lib_text, summary, figure, fig_dir, fmt="svg")
            findings.extend(_with_subject(compile_findings, label, figure))
            metadata, meta_findings = read_metadata(lib_path, summary, figure)
            findings.extend(_with_subject(meta_findings, label, figure))
            if metadata is not None:
                if figure == "trace":
                    findings.extend(_with_subject(
                        compare_trace(metadata, expected_trace(summary)), label, figure))
                else:
                    findings.extend(_with_subject(
                        compare_verdicts(metadata, expected_verdicts(summary)), label, figure))
            if out_path is not None:
                declared = metadata.get("width") if metadata is not None else None
                findings.extend(_with_subject(
                    check_svg(out_path.read_text(), declared), label, figure))
    return findings


# ---------------------------------------------------------------------------
# Mutation anchors (D-05 must-fail controls a/b/c)
# ---------------------------------------------------------------------------

def apply_mutation(
    lib_text: str, anchor: str, build_replacement: Callable[[str], str],
) -> tuple[str | None, list[Finding]]:
    """Find the single line starting with `anchor` and replace it via
    build_replacement(stripped_line). FIG-ANCHOR if zero or more than one
    line matches -- a mutation that changes nothing must never pass."""
    lines = lib_text.split("\n")
    matches = [i for i, line in enumerate(lines) if line.strip().startswith(anchor)]
    if len(matches) != 1:
        return None, [Finding(
            "FIG-ANCHOR", anchor,
            f"expected exactly one matching line, found {len(matches)}")]
    i = matches[0]
    stripped = lines[i].strip()
    indent = lines[i][: len(lines[i]) - len(lines[i].lstrip())]
    lines[i] = indent + build_replacement(stripped)
    return "\n".join(lines), []


_MUTATIONS: tuple[tuple[str, str, Callable[[str], str], frozenset[str]], ...] = (
    ("M01", "let drawn-edges = edges",
     lambda _line: "let drawn-edges = edges.slice(1)",
     frozenset({"FIG-EDGES"})),
    ("M02", "let n = cell-count(t, v)",
     lambda _line: (
         "let n = cell-count(t, v) + "
         "(if t == types.at(0) and v == verdicts.at(0) { 1 } else { 0 })"),
     frozenset({"FIG-CELLS"})),
    ("M03", "let node-w = ",
     lambda _line: "let node-w = 20pt",
     frozenset({"FIG-OVERFLOW"})),
    # 81-REVIEW CR-01: a matrix legend line wider than the matrix must be caught.
    ("M04", "let legend-lines = (",
     lambda line: line.replace(
         '("Shading darkens with count."',
         '("Shading darkens with count, from no assumptions in a cell to the most assumptions in any single cell."', 1),
     frozenset({"FIG-OVERFLOW"})),
)


def _make_mutation_control(
    anchor: str, build_replacement: Callable[[str], str], expected_codes: frozenset[str],
) -> Callable[[], str | None]:
    def _control() -> str | None:
        lib_text, extract_findings = extract_library(LIBRARY)
        if extract_findings:
            return f"extraction findings before mutation: {extract_findings}"
        mutated, anchor_findings = apply_mutation(lib_text, anchor, build_replacement)
        if anchor_findings:
            return anchor_findings[0].detail
        label, summary = _real_fixture()
        with tempfile.TemporaryDirectory() as td:
            findings = check_all(mutated, [(label, summary)], Path(td))
        codes = {f.code for f in findings}
        if codes != expected_codes:
            return f"expected codes {sorted(expected_codes)}, got {sorted(codes)} ({findings})"
        return None
    return _control


# ---------------------------------------------------------------------------
# Controls
# ---------------------------------------------------------------------------

def _p01_shipped_library_all_fixtures_clean() -> str | None:
    lib_text, extract_findings = extract_library(LIBRARY)
    if extract_findings:
        return f"extraction findings: {extract_findings}"
    fixtures, fixture_findings = load_fixtures()
    if fixture_findings:
        return f"fixture-loading findings: {fixture_findings}"
    typst_bin = require_typst()
    if typst_bin is None:
        return "typst not found on PATH (should have been caught by main() already)"
    f_findings = font_findings(typst_bin)
    if f_findings:
        return f"font findings: {f_findings}"
    with tempfile.TemporaryDirectory() as td:
        findings = check_all(lib_text, fixtures, Path(td))
    if findings:
        return f"expected zero findings across {len(fixtures)} fixtures, got {len(findings)}: {findings[:5]}"
    return None


def _f01_drop_chain_edge() -> str | None:
    label, summary = _real_fixture()
    original_expected = expected_trace(summary)
    modified = copy.deepcopy(summary)
    for chain in modified.get("chains", []):
        if chain.get("rests_on"):
            chain["rests_on"] = chain["rests_on"][:-1]
            break
    else:
        return "no chain with a non-empty rests_on found in the real fixture"
    lib_text, extract_findings = extract_library(LIBRARY)
    if extract_findings:
        return f"extraction findings: {extract_findings}"
    with tempfile.TemporaryDirectory() as td:
        workdir = Path(td)
        _out, compile_findings = render(lib_text, modified, "trace", workdir, fmt="svg")
        if compile_findings:
            return f"compile failed: {compile_findings}"
        metadata, meta_findings = read_metadata(workdir / "figures.typ", modified, "trace")
    if meta_findings:
        return f"metadata findings: {meta_findings}"
    codes = {f.code for f in compare_trace(metadata, original_expected)}
    if codes != {"FIG-EDGES"}:
        return f"expected {{'FIG-EDGES'}}, got {codes}"
    return None


def _f02_drop_conclusion_edge() -> str | None:
    label, summary = _real_fixture()
    original_expected = expected_trace(summary)
    if not (summary.get("conclusion") or {}).get("rests_on"):
        return f"{label}: conclusion.rests_on is empty or null -- nothing to drop (81-REVIEW WR-02)"
    modified = copy.deepcopy(summary)
    modified["conclusion"]["rests_on"] = modified["conclusion"]["rests_on"][:-1]
    lib_text, extract_findings = extract_library(LIBRARY)
    if extract_findings:
        return f"extraction findings: {extract_findings}"
    with tempfile.TemporaryDirectory() as td:
        workdir = Path(td)
        _out, compile_findings = render(lib_text, modified, "trace", workdir, fmt="svg")
        if compile_findings:
            return f"compile failed: {compile_findings}"
        metadata, meta_findings = read_metadata(workdir / "figures.typ", modified, "trace")
    if meta_findings:
        return f"metadata findings: {meta_findings}"
    codes = {f.code for f in compare_trace(metadata, original_expected)}
    if codes != {"FIG-CONCL-EDGES"}:
        return f"expected {{'FIG-CONCL-EDGES'}}, got {codes}"
    return None


def _b01_typst_absent_is_blocked() -> str | None:
    with tempfile.TemporaryDirectory() as empty_path_dir:
        env = {"PATH": empty_path_dir, "HOME": os.environ.get("HOME", "")}
        result = subprocess.run(
            [sys.executable, str(Path(__file__).resolve()), "--self-test"],
            env=env, capture_output=True, text=True, check=False,
        )
    if result.returncode != 1:
        return f"expected exit 1, got {result.returncode} (stdout={result.stdout!r})"
    if "BLOCKED" not in result.stdout:
        return f"expected BLOCKED in stdout, got {result.stdout!r}"
    if "PASS" in result.stdout:
        return f"PASS must not appear in stdout, got {result.stdout!r}"
    return None


def _u01_svg_checks() -> str | None:
    bad_cases = {
        "malformed": "<svg><unclosed>",
        "non-svg-root": '<drawing viewBox="0 0 10 10" width="10pt"/>',
        "no-viewbox": '<svg width="10pt"/>',
        "overwide": '<svg viewBox="0 0 500 10" width="500pt"/>',
    }
    for name, xml_text in bad_cases.items():
        codes = {f.code for f in check_svg(xml_text)}
        if codes != {"FIG-SVG"}:
            return f"{name}: expected {{'FIG-SVG'}}, got {codes}"
    good = '<svg viewBox="0 0 400 10" width="400pt" xmlns="http://www.w3.org/2000/svg"/>'
    good_findings = check_svg(good)
    if good_findings:
        return f"well-formed 400pt SVG: expected no findings, got {good_findings}"
    # declared width: 272pt canvas for a 260pt figure is right; 334.76pt (the CR-01
    # canvas, widened by an unboxed legend) is not.
    if check_svg('<svg viewBox="0 0 272 10" width="272pt"/>', 260):
        return "272pt canvas for a declared 260pt figure: expected no findings"
    codes = {f.code for f in check_svg('<svg viewBox="0 0 334.76 10" width="334.76pt"/>', 260)}
    if codes != {"FIG-SVG"}:
        return f"334.76pt canvas for a declared 260pt figure: expected {{'FIG-SVG'}}, got {codes}"
    return None


def _u02_metadata_checks() -> str | None:
    bad_cases = {
        "non-json": "not json",
        "list": "[1,2,3]",
        "missing-key": json.dumps({"gts": 1, "chains": 1, "edges": 1}),
    }
    for name, stdout in bad_cases.items():
        data, findings = _parse_metadata_output(stdout, "trace")
        codes = {f.code for f in findings}
        if data is not None or codes != {"FIG-METADATA"}:
            return f"{name}: expected (None, {{'FIG-METADATA'}}), got ({data}, {codes})"
    good = json.dumps({"gts": 1, "chains": 1, "edges": 1, "conclusion_edges": 0, "overflow": 0, "width": 458})
    data, findings = _parse_metadata_output(good, "trace")
    if findings or data is None:
        return f"well-formed trace metadata: expected a clean parse, got {findings}"
    return None


def _u03_expected_trace_null_absent() -> str | None:
    base = {"ground_truths": [], "chains": []}
    with_null = dict(base, conclusion={"rests_on": None})
    without_key = dict(base, conclusion={})
    e1 = expected_trace(with_null)["conclusion_edges"]
    e2 = expected_trace(without_key)["conclusion_edges"]
    if e1 != 0 or e2 != 0:
        return f"expected both 0, got null={e1} absent={e2}"
    dangling = {
        "ground_truths": [{"id": "GT-1", "read_at_source": True}],
        "chains": [{"id": "C1", "confidence": "HIGH", "rests_on": ["GT-1", "GT-9", "C7"]}],
        "conclusion": {"rests_on": ["C1", "GT-1?", "C9"]},
    }
    e3 = expected_trace(dangling)
    if (e3["edges"], e3["conclusion_edges"]) != (1, 2):
        return f"dangling citations must not be expected as edges: got edges={e3['edges']} conclusion_edges={e3['conclusion_edges']}"
    return None


def _u04_code_registry_complete() -> str | None:
    observed: set[str] = set()
    for _cid, _anchor, _build, expected_codes in _MUTATIONS:
        observed |= set(expected_codes)
    observed |= {"FIG-EDGES", "FIG-CONCL-EDGES"}  # F01, F02
    observed |= {"FIG-SVG"}  # U01
    observed |= {"FIG-METADATA"}  # U02
    observed |= {"FIG-GTS", "FIG-CHAINS", "FIG-EDGES", "FIG-CONCL-EDGES", "FIG-CELLS", "FIG-OVERFLOW"}  # U05

    lib_text, _extract_findings = extract_library(LIBRARY)
    _mutated, anchor_findings = apply_mutation(lib_text, "no-such-anchor-in-the-library", lambda line: line)
    observed |= {f.code for f in anchor_findings}  # exercises FIG-ANCHOR directly, no typst needed

    unknown = observed - set(FINDING_CODES)
    if unknown:
        return f"observed codes outside FINDING_CODES: {sorted(unknown)}"
    missing = (set(FINDING_CODES) - _EXEMPT_FROM_OBSERVATION) - observed
    if missing:
        return f"codes never observed by any control: {sorted(missing)}"
    return None


def _u05_single_dimension_mismatches() -> str | None:
    summary = {
        "ground_truths": [{"id": "GT-1", "read_at_source": True}],
        "chains": [{"id": "C1", "confidence": "HIGH", "rests_on": ["GT-1"]}],
        "conclusion": {"confidence": "HIGH", "rests_on": ["C1"]},
    }
    expected = expected_trace(summary)
    for key, code in (
        ("gts", "FIG-GTS"), ("chains", "FIG-CHAINS"),
        ("edges", "FIG-EDGES"), ("conclusion_edges", "FIG-CONCL-EDGES"),
    ):
        actual = dict(expected, overflow=0)
        actual[key] = actual[key] + 1
        codes = {f.code for f in compare_trace(actual, expected)}
        if codes != {code}:
            return f"trace {key}: expected {{{code!r}}}, got {codes}"
    overflow_actual = dict(expected, overflow=1)
    codes = {f.code for f in compare_trace(overflow_actual, expected)}
    if codes != {"FIG-OVERFLOW"}:
        return f"trace overflow: expected {{'FIG-OVERFLOW'}}, got {codes}"

    vsummary = {"assumptions": [{"type": "physical law", "verdict": "Accept"}]}
    vexpected = expected_verdicts(vsummary)
    for key in ("total", "untyped", "grid", "cells"):
        actual = dict(vexpected, overflow=0)
        if key == "grid":
            actual["grid"] = list(actual["grid"])
            actual["grid"][0] += 1
        elif key == "cells":
            actual["cells"] = 13
        else:
            actual[key] = actual[key] + 1
        codes = {f.code for f in compare_verdicts(actual, vexpected)}
        if codes != {"FIG-CELLS"}:
            return f"verdicts {key}: expected {{'FIG-CELLS'}}, got {codes}"
    overflow_actual = dict(vexpected, overflow=1)
    codes = {f.code for f in compare_verdicts(overflow_actual, vexpected)}
    if codes != {"FIG-OVERFLOW"}:
        return f"verdicts overflow: expected {{'FIG-OVERFLOW'}}, got {codes}"
    return None


_CONTROLS: tuple[tuple[str, Callable[[], str | None]], ...] = (
    ("P01", _p01_shipped_library_all_fixtures_clean),
) + tuple(
    (cid, _make_mutation_control(anchor, build, expected))
    for cid, anchor, build, expected in _MUTATIONS
) + (
    ("F01", _f01_drop_chain_edge),
    ("F02", _f02_drop_conclusion_edge),
    ("B01", _b01_typst_absent_is_blocked),
    ("U01", _u01_svg_checks),
    ("U02", _u02_metadata_checks),
    ("U03", _u03_expected_trace_null_absent),
    ("U04", _u04_code_registry_complete),
    ("U05", _u05_single_dimension_mismatches),
)


def self_test() -> int:
    failures: list[str] = []
    for cid, fn in _CONTROLS:
        try:
            msg = fn()
        except Exception as exc:  # noqa: BLE001
            msg = f"{type(exc).__name__}: {exc}"
        if msg:
            print(f"[FAIL] {cid}: {msg}")
            failures.append(cid)
        else:
            print(f"[PASS] {cid}")
    if failures:
        print(f"FIG-GATE: FAIL ({len(failures)}/{len(_CONTROLS)} failed: {failures})")
        return 1
    print(f"FIG-GATE: PASS ({len(_CONTROLS)}/{len(_CONTROLS)} controls)")
    return 0


# ---------------------------------------------------------------------------
# --describe (typst-independent -- gen-gate-docs and the battery's PREREQ
# branch both run this with no typst on PATH)
# ---------------------------------------------------------------------------

def describe() -> dict:
    """Pure self-description. Every value is derived from this module's own
    data, never hand-typed."""
    return {
        "control_ids": [cid for cid, _fn in _CONTROLS],
        "control_count": len(_CONTROLS),
        "registered_surfaces": [_relpath(LIBRARY), _relpath(TWIN)],
        "checked_files": [_relpath(FIXTURE_DIR / name) for name in FIXTURES],
        "locked_constants": {
            "MAX_WIDTH_PT": MAX_WIDTH_PT,
            "FONTS": list(FONTS),
            "mutation_anchors": [anchor for _cid, anchor, _build, _expected in _MUTATIONS],
        },
        "derived_counts": {
            "finding_codes": len(FINDING_CODES),
            "mutations": len(_MUTATIONS),
            "example_fixtures": len(glob.glob(EXAMPLES_GLOB)),
        },
        "disclosed_bounds_anchors": sorted([
            "counts-read-from-library-metadata-not-svg-geometry",
            "label-fit-proven-to-two-digit-ids",
            "typst-absent-is-blocked-not-pass",
            "battery-blocked-decided-by-command-v-not-exit-code",
            "visual-legibility-is-inspection-not-gate",
            "requires-noto-sans-or-liberation-sans",
        ]),
    }


# ---------------------------------------------------------------------------
# --render (Plan 03 inspects these as images)
# ---------------------------------------------------------------------------

def _do_render(out_dir: Path) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    lib_text, extract_findings = extract_library(LIBRARY)
    if extract_findings:
        for f in extract_findings:
            print(f"{f.code}: {f.subject}: {f.detail}")
        return 1
    fixtures, fixture_findings = load_fixtures()
    if fixture_findings:
        for f in fixture_findings:
            print(f"{f.code}: {f.subject}: {f.detail}")
        return 1

    had_findings = False
    for label, summary in fixtures:
        safe = _safe_name(label)
        for figure in ("trace", "verdicts"):
            with tempfile.TemporaryDirectory() as td:
                workdir = Path(td)
                svg_path, svg_findings = render(lib_text, summary, figure, workdir, fmt="svg")
                if svg_findings:
                    had_findings = True
                    for f in svg_findings:
                        print(f"{f.code}: {label}:{figure}: {f.detail}")
                    continue
                dest_svg = out_dir / f"{safe}-{figure}.svg"
                dest_svg.write_bytes(svg_path.read_bytes())
                print(dest_svg)

                png_path, png_findings = render(
                    lib_text, summary, figure, workdir, fmt="png", extra_args=["--ppi", "144"])
                if png_findings:
                    had_findings = True
                    for f in png_findings:
                        print(f"{f.code}: {label}:{figure}: {f.detail}")
                    continue
                dest_png = out_dir / f"{safe}-{figure}.png"
                dest_png.write_bytes(png_path.read_bytes())
                print(dest_png)
    return 1 if had_findings else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--describe", action="store_true")
    ap.add_argument("--render", metavar="DIR", default=None)
    args = ap.parse_args(argv)

    if args.describe:
        print(json.dumps(describe(), indent=2, sort_keys=True))
        return 0

    if require_typst() is None:
        print("FIG-GATE: BLOCKED — typst not found on PATH; figures were not rendered (this is not a pass)")
        return 1

    if args.render is not None:
        return _do_render(Path(args.render))

    if args.self_test:
        return self_test()

    ap.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
