#!/usr/bin/env python3
"""Reproducer for the post-87 live reading (docs/v9.18b-persona-live-reading.md).

Re-derives every figure published in that document's `## 9. Results` section from the
recorded, committed artifacts in `tests/persona-live-v9.18b/reading/` -- it never trusts
the document's own prose. A mismatch between a fresh run of this script and the
committed table means the table is wrong, not the reproduction (section 8 of the
pre-registration).

Copied from `tests/persona-live-v9.18/reproduce.py` (FROZEN, never edited) and adapted:
reading directory and doc moved to the `b` id; cell ids are S01-S12, not R01-R12; sources
are still read from the frozen `tests/persona-live-v9.18/sources/` directory (read-only
reuse -- that tree is FROZEN-EVIDENCE and is never copied); the verdict line additionally
carries PV-QUESTIONS and PV-DIRECTIVE cell counts, which this script also recomputes and
compares when the doc's verdict line states them.

Lives under tests/, not scripts/: it is not a gate and not CONF-13-scanned.

Checks, in order:
    1. Every results.tsv row with a persona file is re-checked with
       scripts/check-persona-view.py's own check_view() against the recorded source;
       its PASS/FAIL and distinct code set must equal the row. A row with no persona
       file (NO-FILE/SOURCE-MODIFIED/EXTRA-FILE) is re-derived from manifest.jsonl
       instead. Every persona's sha256 is recomputed and compared.
    2. The Results table in the pre-registration doc must equal results.tsv row for
       row: cell, source, role, result, codes.
    3. The doc's stated pass count, PV-ID cell count and PV-NUMBER cell count must
       equal the recomputed figures.
    4. The doc's stated bar outcome (met / not met / not evaluable) must equal the
       recomputed outcome.
    5. If the doc's verdict line states PV-QUESTIONS and/or PV-DIRECTIVE cell counts,
       those must equal the recomputed figures too.

Usage:
    python3 tests/persona-live-v9.18b/reproduce.py [--doc PATH] [--results-tsv PATH]
        [--manifest PATH]
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
READING_DIR = REPO_ROOT / "tests" / "persona-live-v9.18b" / "reading"
SOURCES_DIR = REPO_ROOT / "tests" / "persona-live-v9.18" / "sources"
DEFAULT_DOC = REPO_ROOT / "docs" / "v9.18b-persona-live-reading.md"
DEFAULT_RESULTS_TSV = READING_DIR / "results.tsv"
DEFAULT_MANIFEST = READING_DIR / "manifest.jsonl"
DEFAULT_OUT_DIR = READING_DIR / "out"

CELL_ORDER: tuple[tuple[str, str], ...] = tuple(
    (s, r)
    for s in (
        "analysis-20261002T015836Z.md",
        "analysis-20260101T000001Z.md",
        "analysis-20260101T000002Z.md",
    )
    for r in ("decision-owner", "operator", "risk", "skeptic")
)

_mismatches: list[str] = []


def fail(msg: str) -> None:
    _mismatches.append(msg)


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_check_persona_view():
    spec = importlib.util.spec_from_file_location(
        "_cpv_for_reproduce", REPO_ROOT / "scripts" / "check-persona-view.py"
    )
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_cpv_for_reproduce"] = mod
    spec.loader.exec_module(mod)
    return mod


def load_results_tsv(path: Path) -> list[dict]:
    rows = []
    lines = path.read_text().splitlines()
    header = lines[0].split("\t")
    for line in lines[1:]:
        if not line.strip():
            continue
        rows.append(dict(zip(header, line.split("\t"))))
    return rows


def load_manifest(path: Path) -> dict[str, dict]:
    out = {}
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        out[rec["cell"]] = rec
    return out


def recompute_row(cell: str, rec: dict, cpv, roster, out_dir: Path) -> tuple[str, list[str], str | None]:
    """Returns (result 'PASS'/'FAIL', sorted distinct codes, recomputed persona sha256 or None)."""
    codes: set[str] = set()
    status = rec.get("status")
    source_unchanged = rec.get("source_unchanged")
    extra_files = rec.get("extra_files") or []

    if status != "complete":
        codes.add("NO-FILE")

    if source_unchanged is False:
        codes.add("SOURCE-MODIFIED")

    if extra_files:
        codes.add("EXTRA-FILE")

    persona_sha256 = None
    if status == "complete":
        persona_name = rec.get("persona")
        persona_path = out_dir / persona_name
        if not persona_path.is_file():
            fail(f"{cell}: persona file recorded in manifest is missing on disk: {persona_path}")
        else:
            persona_sha256 = sha256_of(persona_path)
            source_name = rec["source"]
            source_path = SOURCES_DIR / source_name
            persona_text = persona_path.read_text()
            source_text = source_path.read_text()
            findings = cpv.check_view(persona_text, source_text, source_name, roster)
            codes |= {f.code for f in findings}

    pv_codes_present = {c for c in codes if c.startswith("PV-")}
    is_pass = status == "complete" and source_unchanged is True and not extra_files and not pv_codes_present
    result = "PASS" if is_pass else "FAIL"
    return result, sorted(codes), persona_sha256


# ---------------------------------------------------------------------------
# Doc parsing
# ---------------------------------------------------------------------------

_RESULTS_SECTION_RE = re.compile(r"^## 9\. Results\n(.*?)(?=^## 10\.|\Z)", re.MULTILINE | re.DOTALL)
_TABLE_ROW_RE = re.compile(r"^\|\s*(?P<cell>S\d+)\s*\|(?P<rest>.*)\|\s*$", re.MULTILINE)
_VERDICT_RE = re.compile(
    r"Observed:\s*(?P<pass_count>\d+)/(?P<n_declared>\d+)\s*pass\s*\(N\s*=\s*(?P<n>\d+)\);\s*"
    r"PV-ID cells:\s*(?P<pv_id>\d+);\s*PV-NUMBER cells:\s*(?P<pv_number>\d+)\s*"
    r"[-—]\s*bar\s*(?P<outcome>met|not met|not evaluable)"
    r"(?:;\s*PV-QUESTIONS cells:\s*(?P<pv_questions>\d+))?"
    r"(?:;\s*PV-DIRECTIVE cells:\s*(?P<pv_directive>\d+))?"
)


def parse_doc(doc_text: str) -> tuple[list[dict], dict]:
    m = _RESULTS_SECTION_RE.search(doc_text)
    if not m:
        fail("could not find '## 9. Results' section in the doc")
        return [], {}
    section = m.group(1)

    vm = _VERDICT_RE.search(section)
    if not vm:
        fail("could not find the 'Observed: K/12 pass ...' verdict line in ## 9. Results")
        verdict = {}
    else:
        verdict = {
            "pass_count": int(vm.group("pass_count")),
            "n": int(vm.group("n")),
            "pv_id": int(vm.group("pv_id")),
            "pv_number": int(vm.group("pv_number")),
            "outcome": vm.group("outcome"),
        }
        if vm.group("pv_questions") is not None:
            verdict["pv_questions"] = int(vm.group("pv_questions"))
        if vm.group("pv_directive") is not None:
            verdict["pv_directive"] = int(vm.group("pv_directive"))

    rows = []
    for rm in _TABLE_ROW_RE.finditer(section):
        cell = rm.group("cell")
        cols = [c.strip() for c in rm.group("rest").split("|")]
        if len(cols) < 4:
            continue
        source, role, result, codes = cols[0], cols[1], cols[2], cols[3]
        rows.append({
            "cell": cell, "source": source, "role": role,
            "status": result, "codes": codes,
        })
    return rows, verdict


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    ap.add_argument("--results-tsv", type=Path, default=DEFAULT_RESULTS_TSV)
    ap.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    ap.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    args = ap.parse_args(argv)

    cpv = _load_check_persona_view()
    roster = cpv._load_roster_from_contract()

    tsv_rows = load_results_tsv(args.results_tsv)
    manifest = load_manifest(args.manifest)

    if len(tsv_rows) != 12:
        fail(f"results.tsv has {len(tsv_rows)} rows, expected 12")

    expected_order = [(s, r) for s, r in CELL_ORDER]
    actual_order = [(r["source"], r["role"]) for r in tsv_rows]
    if actual_order != expected_order:
        fail(f"results.tsv row order {actual_order} does not match the pre-registered cell order {expected_order}")

    recomputed: dict[str, dict] = {}
    for row in tsv_rows:
        cell = row["cell"]
        rec = manifest.get(cell)
        if rec is None:
            fail(f"{cell}: no manifest entry found")
            continue
        result, codes, persona_sha256 = recompute_row(cell, rec, cpv, roster, args.out_dir)
        codes_str = "-" if not codes else ",".join(codes)
        recomputed[cell] = {
            "cell": cell, "source": row["source"], "role": row["role"],
            "status": result, "codes": codes_str, "persona_sha256": persona_sha256,
        }

        if row.get("status") != result:
            fail(f"{cell}: results.tsv says {row.get('status')!r}, recomputed {result!r}")
        if row.get("codes") != codes_str:
            fail(f"{cell}: results.tsv codes {row.get('codes')!r}, recomputed {codes_str!r}")
        row_sha = row.get("persona_sha256")
        if persona_sha256 is not None and row_sha != persona_sha256:
            fail(f"{cell}: results.tsv persona_sha256 {row_sha!r}, recomputed {persona_sha256!r}")
        elif persona_sha256 is None and row_sha not in (None, "-"):
            fail(f"{cell}: results.tsv records a persona_sha256 {row_sha!r} but no persona file exists")

    doc_text = args.doc.read_text()
    doc_rows, verdict = parse_doc(doc_text)

    if len(doc_rows) != 12:
        fail(f"doc Results table has {len(doc_rows)} rows, expected 12")

    for drow in doc_rows:
        cell = drow["cell"]
        rrow = recomputed.get(cell)
        if rrow is None:
            fail(f"{cell}: doc table cites a cell with no recomputed row")
            continue
        for field in ("source", "role", "status", "codes"):
            if drow[field] != rrow[field]:
                fail(
                    f"{cell}: doc table field {field!r} is {drow[field]!r}, "
                    f"recomputed {rrow[field]!r}"
                )

    pass_count = sum(1 for r in recomputed.values() if r["status"] == "PASS")
    pv_id_count = sum(1 for r in recomputed.values() if "PV-ID" in r["codes"].split(","))
    pv_number_count = sum(1 for r in recomputed.values() if "PV-NUMBER" in r["codes"].split(","))
    pv_questions_count = sum(1 for r in recomputed.values() if "PV-QUESTIONS" in r["codes"].split(","))
    pv_directive_count = sum(1 for r in recomputed.values() if "PV-DIRECTIVE" in r["codes"].split(","))
    completed = sum(1 for rec in manifest.values() if rec.get("status") != "limit_stub")

    if completed < 12:
        bar_outcome = "not evaluable"
    elif pass_count >= 11 and pv_id_count == 0 and pv_number_count == 0:
        bar_outcome = "met"
    else:
        bar_outcome = "not met"

    if verdict:
        if verdict.get("pass_count") != pass_count:
            fail(f"doc verdict pass_count {verdict.get('pass_count')} != recomputed {pass_count}")
        if verdict.get("n") != 12:
            fail(f"doc verdict N {verdict.get('n')} != 12")
        if verdict.get("pv_id") != pv_id_count:
            fail(f"doc verdict PV-ID cells {verdict.get('pv_id')} != recomputed {pv_id_count}")
        if verdict.get("pv_number") != pv_number_count:
            fail(f"doc verdict PV-NUMBER cells {verdict.get('pv_number')} != recomputed {pv_number_count}")
        if verdict.get("outcome") != bar_outcome:
            fail(f"doc verdict bar outcome {verdict.get('outcome')!r} != recomputed {bar_outcome!r}")
        if "pv_questions" in verdict and verdict["pv_questions"] != pv_questions_count:
            fail(f"doc verdict PV-QUESTIONS cells {verdict['pv_questions']} != recomputed {pv_questions_count}")
        if "pv_directive" in verdict and verdict["pv_directive"] != pv_directive_count:
            fail(f"doc verdict PV-DIRECTIVE cells {verdict['pv_directive']} != recomputed {pv_directive_count}")

    if _mismatches:
        print("REPRODUCE: FAIL")
        for m in _mismatches:
            print(f"  - {m}")
        return 1

    print(
        f"REPRODUCE: PASS ({pass_count}/12 pass, PV-ID cells: {pv_id_count}, "
        f"PV-NUMBER cells: {pv_number_count}, PV-QUESTIONS cells: {pv_questions_count}, "
        f"PV-DIRECTIVE cells: {pv_directive_count}, bar {bar_outcome})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
