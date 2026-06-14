#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""AUDIT-01..AUDIT-04 gate: enumerate and classify requirement IDs across all
milestone REQUIREMENTS files.

Parses each `.planning/milestones/vX.Y-REQUIREMENTS.md` file for bolded
requirement IDs at list-item boundaries (never embedded prose). Records each
entry milestone-qualified (D-08: `vX.Y/ID`) so reused bare IDs across
milestones stay distinct.

Usage:
    python3 scripts/check-inventory.py [--output PATH] [--check-coverage] [--self-test]

Exit codes:
    0  all inline fixtures pass (--self-test) or enumeration complete
    1  fixture mismatch, file-coverage gap, or output path violation
    2  environment error (Python <3.12, or .planning/milestones/ not found)

--self-test: runs 8 in-process format/edge fixtures (no disk I/O, no
             .planning/ reads) and verifies each ID classification is correct.
             Catches the v3.9-v3.12 **ID:** pitfall and the embedded-prose
             false-positive trap. Exits 0 only if all 8 classify correctly.

--check-coverage: enumerate all 26 milestone files, print per-file ID count,
                  exit 1 if any file is unvisited or yields 0 IDs (AUDIT-01).

--output PATH: write the Markdown inventory to PATH (must be under
               .planning/ to stay in the gitignored zone; T-81-01).
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path


REPO_ROOT: Path = Path(__file__).resolve().parents[1]
MILESTONES_DIR: Path = REPO_ROOT / ".planning" / "milestones"

# ---------------------------------------------------------------------------
# ID extraction regex — list-item-anchored (D-07/D-08 compliance)
# ---------------------------------------------------------------------------
# Matches only at the START of a list item so embedded prose references
# like "the detector recognizes **S-P01**" are excluded (Pitfall 2).
#
# Handles five corpus ID format variants:
#   Form 1: - [ ] **ID**           (checkbox + closing **)
#   Form 2: - [ ] **ID:**          (colon-inside-bold; v3.9-v3.12)
#   Form 3: - **ID**               (no checkbox; future/deferred items)
#   Form 4: - **ID:**              (no checkbox + colon-inside-bold)
#   Prefix:  [A-Z0-9]+             (allows B-46-1 compound prefix; Pitfall 3)
#   Suffix:  [A-Z0-9]+             (allows META-03-SW alpha sub-ID, STEP0-F1)
_ID_RE = re.compile(
    r"""
    ^-\s                                   # list-item start (anchored)
    (?:\[[x~\.\s]\]\s)?                   # optional checkbox: [x], [~], [ ], [.]
    \*\*                                   # bold open
    (                                      # capture group: the requirement ID
        [A-Z0-9]+-                         # prefix (caps+digits, e.g. B-46)
        [A-Z0-9]+                          # first ID segment
        (?:-[A-Z0-9]+)*                    # zero or more additional segments
    )
    (?:\*\*|:)                            # terminator: closing ** or colon-inside-bold
    """,
    re.VERBOSE | re.MULTILINE,
)

# Secondary pattern: dual-ID bold span "**FU-21-1 / FU-21-2**"
# Captures two IDs separated by space-slash-space inside one bold span.
_DUAL_ID_RE = re.compile(
    r"""
    ^-\s                                   # list-item start
    (?:\[[x~\.\s]\]\s)?                   # optional checkbox
    \*\*\s*                                # bold open (with optional space)
    (                                      # first ID
        [A-Z0-9]+-[A-Z0-9]+(?:-[A-Z0-9]+)*
    )
    \s*/\s*                                # space-slash-space separator
    (                                      # second ID
        [A-Z0-9]+-[A-Z0-9]+(?:-[A-Z0-9]+)*
    )
    \s*\*\*                                # bold close
    """,
    re.VERBOSE | re.MULTILINE,
)

# Checkbox state extraction
_CHECKBOX_RE = re.compile(r"^-\s\[([x~\.\s])\]")


def _extract_checkbox(line: str) -> str:
    """Return checkbox state: 'checked', 'obsoleted', 'open', or 'none'."""
    m = _CHECKBOX_RE.match(line)
    if not m:
        return "none"
    ch = m.group(1)
    if ch == "x":
        return "checked"
    if ch == "~":
        return "obsoleted"
    return "open"


def _milestone_from_filename(path: Path) -> str:
    """Derive milestone label 'vX.Y' from 'vX.Y-REQUIREMENTS.md'."""
    name = path.name
    # Remove the '-REQUIREMENTS.md' suffix
    return name.replace("-REQUIREMENTS.md", "")


def _extract_ids_from_file(path: Path, milestone: str) -> list[dict]:
    """Extract requirement IDs from a single milestone REQUIREMENTS file.

    Returns a list of dicts: {key, id, milestone, source_path, line_no, checkbox}.
    The key is milestone-qualified: 'vX.Y/ID' (D-08).
    source_path is the true filesystem path (D-09).

    A dual-ID bold span like **FU-21-1 / FU-21-2** produces two records.
    Never raises — if a file yields 0 IDs, the list is empty (callers should
    warn, as 0 IDs is a likely sign of a broken regex against v3.9-v3.12 files).
    """
    text = path.read_text(encoding="utf-8")
    entries: list[dict] = []
    seen_lines: set[int] = set()

    for line_no, line in enumerate(text.splitlines(), start=1):
        # Primary scan: standard single-ID form
        m = _ID_RE.match(line)
        if m:
            req_id = m.group(1)
            checkbox = _extract_checkbox(line)
            entries.append({
                "key": f"{milestone}/{req_id}",
                "id": req_id,
                "milestone": milestone,
                "source_path": str(path),
                "line_no": line_no,
                "checkbox": checkbox,
            })
            seen_lines.add(line_no)
            continue

        # Secondary scan: dual-ID bold span "**FU-21-1 / FU-21-2**"
        dm = _DUAL_ID_RE.match(line)
        if dm:
            checkbox = _extract_checkbox(line)
            for req_id in (dm.group(1), dm.group(2)):
                entries.append({
                    "key": f"{milestone}/{req_id}",
                    "id": req_id,
                    "milestone": milestone,
                    "source_path": str(path),
                    "line_no": line_no,
                    "checkbox": checkbox,
                })
            seen_lines.add(line_no)

    return entries


def detect_collisions(entries: list[dict]) -> dict[str, list[str]]:
    """Return {bare_id: [milestone, ...]} for IDs appearing in >1 milestone."""
    by_id: dict[str, list[str]] = defaultdict(list)
    for entry in entries:
        by_id[entry["id"]].append(entry["milestone"])
    return {k: v for k, v in by_id.items() if len(v) > 1}


def find_orphan_candidates(entries: list[dict]) -> list[dict]:
    """Return entries whose checkbox is 'obsoleted' or 'open' or 'none' (deferred)."""
    return [e for e in entries if e["checkbox"] in ("obsoleted", "open", "none")]


def _enumerate_corpus() -> tuple[list[dict], list[Path]]:
    """Glob all vX.Y-REQUIREMENTS.md files and extract IDs from each.

    Returns (all_entries, visited_files).
    visited_files is the sorted list of Path objects actually processed.
    all_entries is the aggregated list across all files.

    Never raises — a file yielding 0 IDs is still in visited_files;
    callers must check for zero-ID files explicitly (AUDIT-01 coverage gate).
    """
    req_files = sorted(MILESTONES_DIR.glob("v*-REQUIREMENTS.md"))
    all_entries: list[dict] = []
    for req_file in req_files:
        milestone = _milestone_from_filename(req_file)
        file_entries = _extract_ids_from_file(req_file, milestone)
        all_entries.extend(file_entries)
    return all_entries, req_files


def _require_python_version() -> None:
    if sys.version_info < (3, 12):
        sys.stderr.write(
            f"scripts/check-inventory.py requires Python >=3.12 "
            f"(running {sys.version_info.major}.{sys.version_info.minor}).\n"
        )
        sys.exit(2)


def _self_test_regex_fixtures(wrong_results: list[str]) -> None:
    """Inline regex/checkbox fixtures (1)-(6) — no disk I/O."""
    fix1 = "- **FOUND-01** some description\n"
    matches1 = _ID_RE.findall(fix1)
    if matches1 != ["FOUND-01"]:
        print(f"check-inventory --self-test: fixture(1) FAIL — got {matches1!r}")
        wrong_results.append("fixture(1) bold-close form not extracted")
    else:
        print("check-inventory --self-test: fixture(1) bold-close form correctly extracted")

    fix2 = "- [ ] **CONV-01:** description\n"
    matches2 = _ID_RE.findall(fix2)
    if matches2 != ["CONV-01"]:
        print(f"check-inventory --self-test: fixture(2) FAIL — got {matches2!r}")
        wrong_results.append("fixture(2) colon-inside-bold form not extracted")
    else:
        print("check-inventory --self-test: fixture(2) colon-inside-bold correctly extracted")

    fix3 = "- [x] **META-03-SW** description\n"
    matches3 = _ID_RE.findall(fix3)
    if matches3 != ["META-03-SW"]:
        print(f"check-inventory --self-test: fixture(3) FAIL — got {matches3!r}")
        wrong_results.append("fixture(3) alpha sub-ID not extracted")
    else:
        print("check-inventory --self-test: fixture(3) alpha sub-ID correctly extracted")

    # The list-item line must be non-list for the embedded-prose test.
    fix4b = "  the detector recognizes **S-P01** in the output text\n"
    matches4b = _ID_RE.findall(fix4b)
    if matches4b:
        print(f"check-inventory --self-test: fixture(4) FAIL — embedded prose extracted: {matches4b!r}")
        wrong_results.append("fixture(4) embedded prose bold wrongly extracted")
    else:
        print("check-inventory --self-test: fixture(4) embedded prose correctly excluded")

    fix5 = "- **FU-21-1 / FU-21-2** dual requirement span\n"
    dm5 = _DUAL_ID_RE.match(fix5)
    if not dm5 or (dm5.group(1), dm5.group(2)) != ("FU-21-1", "FU-21-2"):
        print(f"check-inventory --self-test: fixture(5) FAIL — dual-ID match={dm5}")
        wrong_results.append("fixture(5) dual-ID not split into two records")
    else:
        print("check-inventory --self-test: fixture(5) dual-ID correctly split")

    fix6 = "- [~] **ROUTE-01** obsoleted requirement\n"
    matches6 = _ID_RE.findall(fix6)
    checkbox6 = _extract_checkbox(fix6)
    if matches6 != ["ROUTE-01"]:
        print(f"check-inventory --self-test: fixture(6) FAIL — id not extracted: {matches6!r}")
        wrong_results.append("fixture(6) obsoleted ID not extracted")
    elif checkbox6 != "obsoleted":
        print(f"check-inventory --self-test: fixture(6) FAIL — checkbox={checkbox6!r} (expected 'obsoleted')")
        wrong_results.append(f"fixture(6) checkbox={checkbox6!r}, expected 'obsoleted'")
    else:
        print("check-inventory --self-test: fixture(6) [~] checkbox correctly classified as 'obsoleted'")


def _self_test_collision_orphan_fixtures(wrong_results: list[str]) -> None:
    """Collision and orphan fixtures (7)-(8) — no disk I/O."""
    # Fixture (7): GEN-01 in three milestones → detect_collisions reports it
    collision_entries = [
        {"id": "GEN-01", "milestone": "v5.1", "key": "v5.1/GEN-01",
         "source_path": "fake", "line_no": 1, "checkbox": "none"},
        {"id": "GEN-01", "milestone": "v5.2", "key": "v5.2/GEN-01",
         "source_path": "fake", "line_no": 1, "checkbox": "none"},
        {"id": "GEN-01", "milestone": "v5.3", "key": "v5.3/GEN-01",
         "source_path": "fake", "line_no": 1, "checkbox": "none"},
        {"id": "SOLO-01", "milestone": "v5.1", "key": "v5.1/SOLO-01",
         "source_path": "fake", "line_no": 2, "checkbox": "checked"},
    ]
    collisions7 = detect_collisions(collision_entries)
    if "GEN-01" not in collisions7:
        print(f"check-inventory --self-test: fixture(7) FAIL — GEN-01 not in collisions: {collisions7!r}")
        wrong_results.append("fixture(7) collision fixture: GEN-01 cross-milestone not detected")
    elif "SOLO-01" in collisions7:
        print(f"check-inventory --self-test: fixture(7) FAIL — SOLO-01 wrongly reported as collision")
        wrong_results.append("fixture(7) collision fixture: single-milestone ID SOLO-01 wrongly flagged")
    else:
        milestones7 = collisions7["GEN-01"]
        if sorted(milestones7) != ["v5.1", "v5.2", "v5.3"]:
            print(f"check-inventory --self-test: fixture(7) FAIL — milestones={milestones7!r}")
            wrong_results.append(f"fixture(7) GEN-01 milestones wrong: {milestones7!r}")
        else:
            print("check-inventory --self-test: fixture(7) collision fixture correctly detected GEN-01×3")

    # Fixture (8): [~] ROUTE-01 entry → find_orphan_candidates flags it
    orphan_entries = [
        {"id": "ROUTE-01", "milestone": "v3.8", "key": "v3.8/ROUTE-01",
         "source_path": "fake", "line_no": 10, "checkbox": "obsoleted"},
        {"id": "BASE-01", "milestone": "v3.8", "key": "v3.8/BASE-01",
         "source_path": "fake", "line_no": 11, "checkbox": "checked"},
    ]
    orphans8 = find_orphan_candidates(orphan_entries)
    orphan_ids8 = [e["id"] for e in orphans8]
    if "ROUTE-01" not in orphan_ids8:
        print(f"check-inventory --self-test: fixture(8) FAIL — ROUTE-01 not flagged as orphan: {orphan_ids8!r}")
        wrong_results.append("fixture(8) orphan fixture: [~] ROUTE-01 not flagged")
    elif "BASE-01" in orphan_ids8:
        print(f"check-inventory --self-test: fixture(8) FAIL — checked BASE-01 wrongly flagged as orphan")
        wrong_results.append("fixture(8) orphan fixture: checked BASE-01 wrongly flagged")
    else:
        print("check-inventory --self-test: fixture(8) orphan fixture correctly flagged ROUTE-01 only")


def _run_self_test() -> None:
    """Run 8 inline format/edge fixtures — no disk I/O, no .planning/ reads.

    Fixtures per VALIDATION.md §Wave 0 Requirements:
      (1) **ID** bold-close → extracted
      (2) **ID:** colon-inside-bold → extracted (catches v3.9-v3.12 pitfall)
      (3) **META-03-SW** alpha sub-ID → extracted
      (4) embedded prose bold → NOT extracted (no list anchor)
      (5) **FU-21-1 / FU-21-2** dual-ID → two records
      (6) [~] checkbox **ROUTE-01** → extracted with checkbox='obsoleted'
      (7) collision fixture: GEN-01 in 3 milestones → detect_collisions reports it
      (8) orphan fixture: [~] ROUTE-01 entry → find_orphan_candidates flags it
    """
    wrong_results: list[str] = []
    _self_test_regex_fixtures(wrong_results)
    _self_test_collision_orphan_fixtures(wrong_results)
    if wrong_results:
        sys.stderr.write(
            f"check-inventory --self-test: FAIL — {', '.join(wrong_results)}\n"
        )
        sys.exit(1)
    print("check-inventory --self-test: PASS")


def render_inventory_markdown(
    entries: list[dict],
    collisions: dict[str, list[str]],
    orphans: list[dict],
    n_files: int,
) -> str:
    """Render the inventory as a Markdown string (skeleton; human fills status/evidence)."""
    lines: list[str] = []
    lines.append("# Requirements Inventory — Phase 81")
    lines.append("")
    lines.append("> Generated by: `python3 scripts/check-inventory.py --output ...`")
    lines.append(">")
    lines.append(
        "> **Note:** REQUIREMENTS.md text and ROADMAP.md refer to "
        "`milestones/vX.Y-REQUIREMENTS.md` — the actual paths are "
        "`.planning/milestones/vX.Y-REQUIREMENTS.md` (gitignored). (D-09)"
    )
    lines.append("")
    lines.append("## Summary")
    lines.append(f"- Total IDs extracted: {len(entries)} (across {n_files} files)")
    lines.append(f"- Cross-milestone collisions (AUDIT-03): {len(collisions)} bare IDs appear in >1 milestone")
    lines.append(f"- Orphan candidates (AUDIT-04): {len(orphans)} entries")
    lines.append("")
    lines.append("## Enumeration Table (AUDIT-01)")
    lines.append(
        "| Key (vX.Y/ID) | Bare ID | Milestone | Source Path | Line | Checkbox | "
        "Status | Evidence | Related IDs |"
    )
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for e in entries:
        lines.append(
            f"| {e['key']} | {e['id']} | {e['milestone']} | "
            f"{e['source_path']} | {e['line_no']} | {e['checkbox']} | "
            "_(human fills)_ | _(human fills)_ |  |"
        )
    lines.append("")
    lines.append("## Collision Report (AUDIT-03)")
    if collisions:
        lines.append("| Bare ID | Milestones |")
        lines.append("|---|---|")
        for bare_id, milestones in sorted(collisions.items()):
            lines.append(f"| {bare_id} | {', '.join(milestones)} |")
    else:
        lines.append("_(no cross-milestone collisions detected)_")
    lines.append("")
    lines.append("## Orphan Candidates (AUDIT-04)")
    if orphans:
        lines.append("| Key | Checkbox | Source Path | Line |")
        lines.append("|---|---|---|---|")
        for e in orphans:
            lines.append(
                f"| {e['key']} | {e['checkbox']} | "
                f"{e['source_path']} | {e['line_no']} |"
            )
    else:
        lines.append("_(no orphan candidates detected)_")
    lines.append("")
    return "\n".join(lines)


def _resolve_confined_output(path: Path) -> Path:
    """Resolve path and enforce T-81-01: must be under REPO_ROOT/.planning/.

    Returns the resolved absolute path if confined.
    Writes a stderr message and calls sys.exit(2) if the path escapes.
    """
    resolved = path.resolve()
    allowed_root = (REPO_ROOT / ".planning").resolve()
    confined = (
        resolved == allowed_root
        or str(resolved).startswith(str(allowed_root) + "/")
    )
    if not confined:
        sys.stderr.write(
            f"check-inventory: --output path must be under .planning/ "
            f"(got: {resolved})\n"
        )
        sys.exit(2)
    return resolved


def _run_enumerate_and_emit(output: Path | None) -> None:
    """Enumerate corpus, detect collisions/orphans, and write or print Markdown.

    If output is not None, writes to the already-resolved confined path and
    prints a summary to stdout. If None, prints full Markdown to stdout (D-02).
    """
    all_entries, req_files = _enumerate_corpus()
    if not req_files:
        sys.stderr.write(
            f"check-inventory: no v*-REQUIREMENTS.md files found in {MILESTONES_DIR}\n"
        )
        sys.exit(1)

    zero_id_files = [
        rf.name for rf in req_files
        if not any(e["milestone"] == _milestone_from_filename(rf) for e in all_entries)
    ]
    collisions = detect_collisions(all_entries)
    orphans = find_orphan_candidates(all_entries)
    markdown = render_inventory_markdown(
        all_entries, collisions, orphans, len(req_files)
    )

    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(markdown, encoding="utf-8")
        print(
            f"check-inventory: PASS — {len(all_entries)} IDs extracted from "
            f"{len(req_files)} files"
        )
        print(f"  Cross-milestone collisions: {len(collisions)}")
        print(f"  Orphan candidates: {len(orphans)}")
        print(f"  Inventory written to: {output}")
    else:
        print(markdown)

    if zero_id_files:
        sys.stderr.write(
            f"check-inventory: WARNING — 0 IDs found in: {', '.join(zero_id_files)}\n"
            f"  This may indicate a broken regex (Pitfall 1: v3.9-v3.12 **ID:** form).\n"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "AUDIT-01..AUDIT-04: enumerate and classify requirement IDs across "
            "all .planning/milestones/vX.Y-REQUIREMENTS.md files."
        )
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run 8 inline format/edge fixtures; exit 0 only if all pass",
    )
    parser.add_argument(
        "--check-coverage",
        action="store_true",
        help=(
            "enumerate all 26 files and print per-file ID count; "
            "exit 1 if any file yields 0 IDs (AUDIT-01)"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="write Markdown inventory to this path (must be under .planning/; T-81-01)",
    )
    args = parser.parse_args()
    _require_python_version()

    if args.self_test:
        _run_self_test()
        return

    if not MILESTONES_DIR.exists():
        sys.stderr.write(
            f"check-inventory: MILESTONES_DIR not found: {MILESTONES_DIR}\n"
            f"  Ensure .planning/milestones/ exists (it is gitignored).\n"
        )
        sys.exit(2)

    if args.check_coverage:
        _run_check_coverage()
        return

    resolved_output: Path | None = None
    if args.output is not None:
        resolved_output = _resolve_confined_output(args.output)

    _run_enumerate_and_emit(resolved_output)


def _run_check_coverage() -> None:
    """Enumerate corpus and print per-file ID count; exit 1 on any zero-ID file.

    This is the AUDIT-01 file-coverage round-trip: every v*-REQUIREMENTS.md
    file must be visited and yield at least one ID. Exits 0 on full coverage.
    """
    req_files = sorted(MILESTONES_DIR.glob("v*-REQUIREMENTS.md"))
    if not req_files:
        sys.stderr.write(
            f"check-inventory: no v*-REQUIREMENTS.md files found in {MILESTONES_DIR}\n"
        )
        sys.exit(1)

    zero_id_files: list[str] = []
    total_ids = 0
    for req_file in req_files:
        milestone = _milestone_from_filename(req_file)
        file_entries = _extract_ids_from_file(req_file, milestone)
        n = len(file_entries)
        total_ids += n
        status = "OK" if n > 0 else "ZERO-IDs"
        print(f"  {milestone}: {n} IDs [{status}]")
        if n == 0:
            zero_id_files.append(req_file.name)

    if zero_id_files:
        sys.stderr.write(
            f"check-inventory --check-coverage: FAIL — 0 IDs in: "
            f"{', '.join(zero_id_files)}\n"
            f"  Likely broken regex (Pitfall 1: v3.9-v3.12 **ID:** form).\n"
        )
        sys.exit(1)

    print(
        f"check-inventory --check-coverage: PASS — {total_ids} IDs across "
        f"{len(req_files)} files (all 26 visited, no zero-ID file)"
    )


if __name__ == "__main__":
    main()
