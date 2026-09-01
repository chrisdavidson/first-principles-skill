#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""TRACE-01..TRACE-03 / GAP-01 gate: traceability matrix emitter + consistency gate.

Emits a Markdown matrix table (MATRIX.md) and a structured JSON sidecar
(matrix.json) from an internal list of MatrixRow dataclass objects, then
validates the sidecar for consistency.

Usage:
    python3 scripts/check-traceability.py --self-test
    python3 scripts/check-traceability.py emit \\
        --md-output docs/requirements-matrix.md \\
        --json-output docs/data/matrix.json
    python3 scripts/check-traceability.py check \\
        --input docs/data/matrix.json

Exit codes:
    0  all fixtures pass (--self-test) or subcommand completes cleanly
    1  fixture mismatch or consistency failure
    2  environment error (Python <3.12) or path confinement violation

--self-test: runs the inline fixtures + named sentinels (no disk I/O beyond
             checking known-present repo files) and exits 0 only if all pass.
             This is the CI gate entry point (TRACE-03 + STEP0-08 pattern).

emit: writes MATRIX.md + matrix.json from build_matrix_rows(); both paths
      must be under .planning/ or docs/ (T-82-01 path-confinement guard).

check: reads matrix.json, validates every row has a valid capability and
       coverage_tier, and deep-resolves every reproducible artifact_link (D-08).
"""

import argparse
import json
import re
import sys
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path


REPO_ROOT: Path = Path(__file__).resolve().parents[1]

# Whitelist for CLI-tool artifact links that have no script file (Pitfall 6)
KNOWN_CLI_GATES: set[str] = {
    "claude plugin validate ./first-principles",
    "markdownlint-cli2",
}

# Valid values for capability and coverage_tier fields
VALID_CAPABILITIES: set[str] = {"Methodology", "Test-Network"}
VALID_TIERS: set[str] = {"reproducible", "audit-only", "gap", "scheduled"}

# Surfaces where the published coverage headline is asserted as a present-tense claim by
# _self_test_headline_lock(). This set is allowed to under-count without being wrong: it
# does not need to be exhaustive for correctness, only for the gate to stay green — a
# surface stating the headline but missing from this set is left for a tree-wide scan to
# catch loudly (a later phase's own mechanism), never silently accepted here. Treat this as
# a "known covered" record, not a trusted exhaustive inventory.
COVERED_HEADLINE_SURFACES: frozenset[str] = frozenset({
    "docs/requirements-traceability.md",  # line 7, prose form (already gated pre-Phase-10)
    "CLAUDE.md",                          # line 220, prose form
    "docs/README.md",                     # line 20, prose form
    "docs/MEASUREMENT-MAP.md",            # line 52, prose form
    "docs/COMPONENT-DIAGRAM.md",          # line 97, slash form ONLY — no prose form in this file
})

# Whole-file historical exemption for HEADLINE-03: files whose entire purpose is recording a
# frozen or dated coverage figure. A hit in one of these files is never "the current claim"
# even with no arrow on the line — each entry below is a deliberate editorial decision, not a
# default, and every entry must carry its own justification.
#
# Safe-failure direction: because the search target used against this set is always the
# *current* literal derived live from build_matrix_rows() (never a generic numeric pattern), a
# value that is superseded stops matching the search the moment the headline moves — no entry
# here ever needs retiring on that account. This set only needs to grow (a new milestone-closure
# doc), and a document that states the current literal without an arrow and is missing from this
# set is not silently accepted: it is loudly caught as an unregistered surface by the tree-wide
# scan (a later plan in this phase), never here.
HISTORICAL_EXEMPT_FILES: frozenset[str] = frozenset({
    "CHANGELOG.md",                 # dated log by definition; already covered by the arrow
                                     # layer at its one live occurrence (line 45), kept here too
                                     # because a dated log is definitionally historical narration
    "docs/v8.0-final-closure.md",   # frozen v8.0 terminal record; its "Superseded" callout
                                     # states both current renderings with NO arrow on that
                                     # line — the live proof that the arrow layer alone is
                                     # insufficient and the whole-file layer is load-bearing here
})

# Tree-wide scan scope for HEADLINE-05 (unregistered-surface detection): the same
# non-recursive, hand-curated glob idiom as check-links.py's DOCS_CHECK_GLOBS — Path.glob()
# only, with no tree-walking helper and no shell-out of any kind. Any tracked file matched
# here that states the current headline as a non-historical occurrence must also be a member
# of COVERED_HEADLINE_SURFACES, or the tree-wide scan in _self_test_headline_lock() fails,
# naming the file and line.
HEADLINE_SCAN_GLOBS: list[str] = [
    "docs/*.md",    # deliberately non-recursive: can never descend into docs/history/, which
                     # is git-ignored and untracked and must not be scanned
    "CLAUDE.md",     # already a registered current-fact surface (COVERED_HEADLINE_SURFACES)
    "CHANGELOG.md",  # whole-file historical exemption (HISTORICAL_EXEMPT_FILES)
    "README.md",     # repo root; matches zero occurrences today, included as forward
                     # protection against a future surface silently gaining a stale mention
]


# Arrow-layer tokens for _is_historical_headline_hit()'s figure-adjacency test (CR-03). Neither
# constant contains any digit from the coverage headline itself.
_ARROW_TOKENS: tuple[str, str] = ("→", "->")
_HTML_COMMENT_CLOSE: str = "-->"


def _is_historical_headline_hit(relpath: str, line: str) -> bool:
    """HEADLINE-03 two-layer historical classifier, shared by every consumer: the per-surface
    presence assertion, its positive controls, and the tree-wide unregistered-surface scan.

    A hit (a line already known to contain the current headline literal, in either rendering)
    is historical if EITHER layer applies, checked in this order:
      1. whole-file: relpath is a member of HISTORICAL_EXEMPT_FILES.
      2. figure-adjacent arrow: an arrow token (_ARROW_TOKENS) sits between two figures on the
         line — a superseded slash-form reading joined to its replacement by an arrow, e.g. a
         ledger row reading "<old slash reading> → <new slash reading>" — this is adjacency,
         not line membership. A mermaid edge ("A --> B"), an HTML comment terminator ("-->"),
         or an unrelated prose arrow elsewhere on the same line is NOT evidence that this
         line's headline mention is historical; only an arrow delimiting two figures is. The
         HTML comment terminator is stripped from the line before the arrow test runs, so it
         can never itself supply the arrow (it would otherwise falsely satisfy the ASCII "->"
         token, since "-->" contains "->" as a substring).

    Deliberately does not do any tense, marker-word, or surrounding-prose detection — this tree
    contains at least four distinct historical phrasings ("stayed X", "moved to X", "from X to
    Y", "the then-current X") and a marker list could never be proven exhaustive. The two
    structural layers above are what the live tree actually requires (see the
    <measured_classification_table> in this phase's plan) and nothing more.

    This narrowing was measured against the live tree during planning (Phase 10 Plan 04's
    <measured_live_baseline>): every one of the 11 headline-bearing lines in the current scan
    scope keeps the identical classification under this adjacency test that it had under the
    prior whole-line test — zero verdicts moved. The green self-test result after this change is
    therefore a checked property, not a hope.
    """
    if relpath in HISTORICAL_EXEMPT_FILES:
        return True
    _stripped = line.replace(_HTML_COMMENT_CLOSE, "")
    return any(
        re.search(rf"\d[\d\s/]*\s*{re.escape(_tok)}\s*[\d\s/]*\d", _stripped)
        for _tok in _ARROW_TOKENS
    )


def _headline_scan_files(globs: list[str]) -> list[Path]:
    """Expand a HEADLINE_SCAN_GLOBS-shaped glob list against REPO_ROOT with Path.glob,
    deduplicated by path, preserving sorted order per pattern (the check-links.py
    _collect_files idiom). Module level so block (j) and its non-vacuity control, block
    (l), call the identical function object — a control exercising a parallel copy would
    prove nothing (research Pitfall 4). No tree-walking helper, no shell-out.
    """
    _seen: set[Path] = set()
    _files: list[Path] = []
    for _glob_pattern in globs:
        for _candidate in sorted(REPO_ROOT.glob(_glob_pattern)):
            if _candidate not in _seen:
                _seen.add(_candidate)
                _files.append(_candidate)
    return _files


def _headline_scan_floor_breaches(
    scan_files: list[Path], accounted_hits: int
) -> list[str]:
    """Derived coverage floor and accounted-hit floor for the tree-wide scan (CR-01 fix).

    Returns a list of breach descriptions (empty when both floors hold), evaluated in this
    order — coverage first, since an unreachable surface makes the accounted-hit count
    meaningless. Both bounds are derived from COVERED_HEADLINE_SURFACES and
    HISTORICAL_EXEMPT_FILES, never a magic number, so a narrowing typo or an emptied glob
    list is caught proportionally rather than only on total absence. Module level so block
    (j) and its non-vacuity control, block (l), call the identical function object.
    """
    _scan_relpaths = {
        _p.relative_to(REPO_ROOT).as_posix() for _p in scan_files if _p.is_file()
    }
    _unreachable = sorted(
        (COVERED_HEADLINE_SURFACES | HISTORICAL_EXEMPT_FILES) - _scan_relpaths
    )
    if _unreachable:
        return [
            f"(j) coverage floor unmet: scan globs do not reach {_unreachable} — the "
            "tree-wide scan cannot be load-bearing for surfaces it never reads"
        ]
    if accounted_hits < len(COVERED_HEADLINE_SURFACES):
        return [
            f"(j) accounted-hit floor unmet: only {accounted_hits} non-historical hit(s) "
            f"seen, fewer than the {len(COVERED_HEADLINE_SURFACES)} registered surfaces — "
            "the scan is not reading what it claims to read"
        ]
    return []


# ---------------------------------------------------------------------------
# MatrixRow dataclass (D-12: single internal representation for dual output)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MatrixRow:
    key: str              # milestone-qualified: "v3.1/ROUTE-02"
    bare_id: str          # "ROUTE-02"
    milestone: str        # "v3.1"
    capability: str       # "Methodology" | "Test-Network"
    deliverable_path: str # live file path or "active-tail" sentinel
    coverage_tier: str    # "reproducible" | "audit-only" | "gap" | "scheduled"
    artifact_link: str    # resolves to real path/row/section or whitelist CLI
    gap_rationale: str    # non-empty when coverage_tier != "reproducible"


# ---------------------------------------------------------------------------
# Matrix row content — curated in Plan 02 (two inclusion paths per D-05)
# ---------------------------------------------------------------------------

# residual/ key prefix for non-milestone RR and S-N residuals.
# CONFIRMED at Task 3 checkpoint (82-02 Plan, 2026-06-14) — key scheme approved;
# no re-keying required. If scheme ever changes, update only this constant
# and re-run emit + check; the key form changes everywhere at once.
_RESIDUAL_KEY_PREFIX = "residual"


def _rows_methodology_agent() -> list[MatrixRow]:
    """v3.0 agent-body, sync, migrate, PKG, EVAL reqs — Methodology."""
    audit_rationale = "Validated by v3.0-MILESTONE-AUDIT; no re-runnable gate"
    return [
        MatrixRow("v3.0/AGENT-01", "AGENT-01", "v3.0", "Methodology",
                  "first-principles/agents/first-principles.md",
                  "audit-only", "", audit_rationale),
        MatrixRow("v3.0/AGENT-02", "AGENT-02", "v3.0", "Methodology",
                  "first-principles/agents/first-principles.md",
                  "audit-only", "", audit_rationale),
        MatrixRow("v3.0/AGENT-03", "AGENT-03", "v3.0", "Methodology",
                  "first-principles/agents/first-principles.md",
                  "audit-only", "", audit_rationale),
        MatrixRow("v3.0/AGENT-04", "AGENT-04", "v3.0", "Methodology",
                  "first-principles/agents/first-principles.md",
                  "audit-only", "", audit_rationale),
        MatrixRow("v3.0/AGENT-05", "AGENT-05", "v3.0", "Methodology",
                  "first-principles/agents/first-principles.md",
                  "audit-only", "", audit_rationale),
        MatrixRow("v3.0/AGENT-06", "AGENT-06", "v3.0", "Methodology",
                  "first-principles/agents/first-principles.md",
                  "audit-only", "", audit_rationale),
        MatrixRow("v3.0/SYNC-01", "SYNC-01", "v3.0", "Methodology",
                  "scripts/sync-content.py",
                  "audit-only", "", audit_rationale),
        MatrixRow("v3.0/SYNC-02", "SYNC-02", "v3.0", "Methodology",
                  "scripts/sync-content.py",
                  "audit-only", "", audit_rationale),
        MatrixRow("v3.0/SYNC-03", "SYNC-03", "v3.0", "Methodology",
                  "scripts/sync-content.py",
                  "audit-only", "", audit_rationale),
        MatrixRow("v3.0/SYNC-04", "SYNC-04", "v3.0", "Methodology",
                  "scripts/sync-content.py",
                  "audit-only", "", audit_rationale),
        MatrixRow("v3.0/PKG-01", "PKG-01", "v3.0", "Methodology",
                  "first-principles/agents/first-principles.md",
                  "audit-only", "", audit_rationale),
        MatrixRow("v3.0/PKG-02", "PKG-02", "v3.0", "Methodology",
                  "first-principles/agents/first-principles.md",
                  "audit-only", "", audit_rationale),
        MatrixRow("v3.0/EVAL-01", "EVAL-01", "v3.0", "Methodology",
                  "first-principles/agents/first-principles.md",
                  "audit-only", "", audit_rationale),
    ]


def _rows_methodology_agent_cont() -> list[MatrixRow]:
    """v3.0 MIGRATE/DEPR/GATE rows + v3.2 META rows — Methodology."""
    audit_v30 = "Validated by v3.0-MILESTONE-AUDIT; no re-runnable gate"
    audit_v32 = "Validated by v3.2-MILESTONE-AUDIT; no re-runnable gate"
    return [
        MatrixRow("v3.0/MIGRATE-01", "MIGRATE-01", "v3.0", "Methodology",
                  "first-principles/agents/first-principles.md",
                  "audit-only", "", audit_v30),
        MatrixRow("v3.0/MIGRATE-02", "MIGRATE-02", "v3.0", "Methodology",
                  "first-principles/agents/first-principles.md",
                  "audit-only", "", audit_v30),
        MatrixRow("v3.0/MIGRATE-03", "MIGRATE-03", "v3.0", "Methodology",
                  "first-principles/agents/first-principles.md",
                  "audit-only", "", audit_v30),
        MatrixRow("v3.0/MIGRATE-04", "MIGRATE-04", "v3.0", "Methodology",
                  "first-principles/agents/first-principles.md",
                  "audit-only", "", audit_v30),
        MatrixRow("v3.0/MIGRATE-05", "MIGRATE-05", "v3.0", "Methodology",
                  "first-principles/agents/first-principles.md",
                  "audit-only", "", audit_v30),
        MatrixRow("v3.0/MIGRATE-06", "MIGRATE-06", "v3.0", "Methodology",
                  "first-principles/agents/first-principles.md",
                  "audit-only", "", audit_v30),
        MatrixRow("v3.0/DEPR-01", "DEPR-01", "v3.0", "Methodology",
                  "first-principles/agents/first-principles.md",
                  "audit-only", "", audit_v30),
        MatrixRow("v3.0/DEPR-02", "DEPR-02", "v3.0", "Methodology",
                  "first-principles/agents/first-principles.md",
                  "audit-only", "", audit_v30),
        MatrixRow("v3.0/DEPR-03", "DEPR-03", "v3.0", "Methodology",
                  "first-principles/agents/first-principles.md",
                  "audit-only", "", audit_v30),
        # v3.2 — worked examples + rubric (META-*/META-Q-*)
        MatrixRow("v3.2/META-01", "META-01", "v3.2", "Methodology",
                  "first-principles/agents/references/examples",
                  "audit-only", "", audit_v32),
        MatrixRow("v3.2/META-02", "META-02", "v3.2", "Methodology",
                  "first-principles/agents/references/assumption-taxonomy.md",
                  "audit-only", "", audit_v32),
        MatrixRow("v3.2/META-03-SW", "META-03-SW", "v3.2", "Methodology",
                  "first-principles/agents/references/examples",
                  "audit-only", "", audit_v32),
        MatrixRow("v3.2/META-03-PB", "META-03-PB", "v3.2", "Methodology",
                  "first-principles/agents/references/examples",
                  "audit-only", "", audit_v32),
        MatrixRow("v3.2/META-03-PG", "META-03-PG", "v3.2", "Methodology",
                  "first-principles/agents/references/examples",
                  "audit-only", "", audit_v32),
        MatrixRow("v3.2/META-03-SE", "META-03-SE", "v3.2", "Methodology",
                  "first-principles/agents/references/examples",
                  "audit-only", "", audit_v32),
        MatrixRow("v3.2/META-Q1", "META-Q1", "v3.2", "Methodology",
                  "shared/spine/references/validation-rubric.md",
                  "audit-only", "", audit_v32),
        MatrixRow("v3.2/META-Q2", "META-Q2", "v3.2", "Methodology",
                  "first-principles/agents/first-principles.md",
                  "audit-only", "", audit_v32),
        MatrixRow("v3.2/META-Q3", "META-Q3", "v3.2", "Methodology",
                  "first-principles/agents/references/examples",
                  "audit-only", "", audit_v32),
        MatrixRow("v3.2/META-Q4", "META-Q4", "v3.2", "Methodology",
                  "scripts/check-body-budget.py",
                  "audit-only", "",
                  "TEARDOWN-01 (v8.7 Phase 163, docs/v8.7-constraint-teardown.md) retired the "
                  "body-budget pre-commit gate. scripts/check-body-budget.py is now report-only "
                  "(always exits 0) and scripts/git-hooks/pre-commit no longer invokes it — the "
                  "body line count is reported every firewall-battery run ([INFO] body-size) but "
                  "is not gated. META-Q4 is therefore audit-only (reported/inspectable), not "
                  "reproducibly enforced. Re-tiered reproducible -> audit-only in the v8.8 "
                  "post-close TEARDOWN-01 cleanup, replacing the prior vacuously-green tier."),
    ]


def _rows_methodology_rigor() -> list[MatrixRow]:
    """v3.7 RIGOR rows — Methodology (validation rubric).

    Rubric anchor strings must be substrings present in the rubric file
    (D-08 resolution: plain substring check after '#' split).
    These match the actual section headings in validation-rubric.md.
    """
    rubric = "shared/spine/references/validation-rubric.md"
    # Anchor text = literal substring expected in the rubric file
    crit1 = rubric + "#Criterion 1: Identify Essence"
    crit2 = rubric + "#Criterion 2: Challenge Assumptions"
    crit3 = rubric + "#Criterion 3: Establish Ground Truths"
    crit4 = rubric + "#Criterion 4: Reason Upward"
    crit5 = rubric + "#Criterion 5: Validate"
    crit6 = rubric + "#Criterion 6: Conclusion-to-Ground-Truth Traceability"
    r_link = rubric + "#How to Apply This Rubric"
    scoring = rubric + "#Scoring Model"
    return [
        MatrixRow("v3.7/RIGOR-01", "RIGOR-01", "v3.7", "Methodology",
                  rubric, "reproducible", crit1, ""),
        MatrixRow("v3.7/RIGOR-02", "RIGOR-02", "v3.7", "Methodology",
                  rubric, "reproducible", crit2, ""),
        MatrixRow("v3.7/RIGOR-03", "RIGOR-03", "v3.7", "Methodology",
                  rubric, "reproducible", crit3, ""),
        MatrixRow("v3.7/RIGOR-04", "RIGOR-04", "v3.7", "Methodology",
                  rubric, "reproducible", crit4, ""),
        MatrixRow("v3.7/RIGOR-05", "RIGOR-05", "v3.7", "Methodology",
                  rubric, "reproducible", crit5, ""),
        MatrixRow("v3.7/RIGOR-06", "RIGOR-06", "v3.7", "Methodology",
                  rubric, "reproducible", crit6, ""),
        MatrixRow("v3.7/RIGOR-07", "RIGOR-07", "v3.7", "Methodology",
                  rubric, "reproducible", r_link, ""),
        MatrixRow("v3.7/RIGOR-08", "RIGOR-08", "v3.7", "Methodology",
                  rubric, "reproducible", scoring, ""),
    ]


def _rows_methodology_focused_stubs() -> list[MatrixRow]:
    """v3.8 focused-mode stubs + v3.12 phase-level skills — Methodology."""
    audit_v38 = "Validated by v3.8-MILESTONE-AUDIT; no re-runnable gate"
    audit_v312 = "Validated by v3.12-MILESTONE-AUDIT; no re-runnable gate"
    fp_agent = "first-principles/agents/first-principles.md"
    fp_skills = "first-principles/skills"
    return [
        MatrixRow("v3.8/DISP-01", "DISP-01", "v3.8", "Methodology",
                  fp_agent, "audit-only", "", audit_v38),
        MatrixRow("v3.8/STUB-01", "STUB-01", "v3.8", "Methodology",
                  fp_skills, "audit-only", "", audit_v38),
        # EVAL-01's original deliverable, scripts/check-focused-output.py, was
        # retired at the 2026-08-16 audit (stream 2) after being superseded by
        # the merged check-routing-battery.py. The deliverable_path is repointed
        # at the successor rather than left dangling: deliverable_path is
        # reported, never existence-resolved (only artifact_link is), so a stale
        # path here would have failed silently and misled a matrix reader.
        MatrixRow("v3.8/EVAL-01", "EVAL-01", "v3.8", "Methodology",
                  "scripts/check-routing-battery.py",
                  "audit-only", "",
                  audit_v38 + ". Original deliverable scripts/check-focused-output.py"
                  " retired 2026-08-16 (superseded by the merged battery);"
                  " deliverable repointed to its successor."),
        MatrixRow("v3.12/PHASE-01", "PHASE-01", "v3.12", "Methodology",
                  fp_skills, "audit-only", "", audit_v312),
        MatrixRow("v3.12/PHASE-02", "PHASE-02", "v3.12", "Methodology",
                  fp_skills, "audit-only", "", audit_v312),
        MatrixRow("v3.12/PHASE-03", "PHASE-03", "v3.12", "Methodology",
                  fp_skills, "audit-only", "", audit_v312),
        MatrixRow("v3.12/PHASE-04", "PHASE-04", "v3.12", "Methodology",
                  fp_skills, "audit-only", "", audit_v312),
        MatrixRow("v3.12/PHASE-05", "PHASE-05", "v3.12", "Methodology",
                  fp_skills, "audit-only", "", audit_v312),
        MatrixRow("v3.12/PHASE-06", "PHASE-06", "v3.12", "Methodology",
                  fp_skills, "audit-only", "", audit_v312),
        MatrixRow("v3.12/PHASE-07", "PHASE-07", "v3.12", "Methodology",
                  fp_skills, "audit-only", "", audit_v312),
        MatrixRow("v3.12/PHASE-08", "PHASE-08", "v3.12", "Methodology",
                  fp_skills, "audit-only", "", audit_v312),
        MatrixRow("v3.12/PHASE-09", "PHASE-09", "v3.12", "Methodology",
                  fp_skills, "audit-only", "", audit_v312),
        MatrixRow("v3.12/PHASE-10", "PHASE-10", "v3.12", "Methodology",
                  fp_skills, "audit-only", "", audit_v312),
        MatrixRow("v3.13/TAX-01", "TAX-01", "v3.13", "Methodology",
                  "first-principles/agents/references/assumption-taxonomy.md",
                  "audit-only", "",
                  "Validated by v3.13-MILESTONE-AUDIT; no re-runnable gate"),
        MatrixRow("v3.13/TAX-02", "TAX-02", "v3.13", "Methodology",
                  "first-principles/agents/references/assumption-taxonomy.md",
                  "audit-only", "",
                  "Validated by v3.13-MILESTONE-AUDIT; no re-runnable gate"),
        MatrixRow("v3.13/WKEX-01", "WKEX-01", "v3.13", "Methodology",
                  "first-principles/agents/references/examples",
                  "audit-only", "",
                  "Validated by v3.13-MILESTONE-AUDIT; no re-runnable gate"),
        MatrixRow("v3.13/WKEX-02", "WKEX-02", "v3.13", "Methodology",
                  "first-principles/agents/references/examples",
                  "audit-only", "",
                  "Validated by v3.13-MILESTONE-AUDIT; no re-runnable gate"),
    ]


def _rows_testnet_ci_gates() -> list[MatrixRow]:
    """CI gate rows — Test-Network (VAL-01..05, DUAL-04, GATE-01..03, HOOK-*)."""
    hook = ".githooks/pre-commit"
    audit_v30 = "Validated by v3.0-MILESTONE-AUDIT; no re-runnable gate"
    audit_v33 = "Validated by v3.3-MILESTONE-AUDIT; no re-runnable gate"
    return [
        # VAL-01/02 via KNOWN_CLI_GATES whitelist (Pitfall 6)
        MatrixRow("v2.0/VAL-01", "VAL-01", "v2.0", "Test-Network",
                  "first-principles/agents/first-principles.md",
                  "reproducible", "claude plugin validate ./first-principles",
                  ""),
        MatrixRow("v2.0/VAL-02", "VAL-02", "v2.0", "Test-Network",
                  "first-principles/agents/first-principles.md",
                  "reproducible", "markdownlint-cli2", ""),
        MatrixRow("v2.0/VAL-03", "VAL-03", "v2.0", "Test-Network",
                  "scripts/check-links.py",
                  "reproducible", "scripts/check-links.py", ""),
        MatrixRow("v2.0/VAL-04", "VAL-04", "v2.0", "Test-Network",
                  "scripts/check-trigger-collisions.py",
                  "reproducible", "scripts/check-trigger-collisions.py", ""),
        MatrixRow("v2.0/VAL-05", "VAL-05", "v2.0", "Test-Network",
                  "scripts/check-description-budget.py",
                  "reproducible", "scripts/check-description-budget.py", ""),
        # v3.0 GATE rows
        MatrixRow("v3.0/GATE-01", "GATE-01", "v3.0", "Test-Network",
                  "scripts/check-agent.py",
                  "reproducible", "scripts/check-agent.py", ""),
        MatrixRow("v3.0/GATE-02", "GATE-02", "v3.0", "Test-Network",
                  "scripts/check-trigger-collisions.py",
                  "reproducible", "scripts/check-trigger-collisions.py", ""),
        MatrixRow("v3.0/GATE-03", "GATE-03", "v3.0", "Test-Network",
                  "scripts/sync-content.py",
                  "reproducible", "scripts/sync-content.py", ""),
        # DUAL-04 sync-check gate
        MatrixRow("v2.0/DUAL-04", "DUAL-04", "v2.0", "Test-Network",
                  "scripts/sync-content.py",
                  "audit-only", "",
                  "v2.0-MILESTONE-AUDIT passed; v2.0 DUAL-04 predates current --check flag"),
        # v3.3 body-budget pre-commit hook rows
        MatrixRow("v3.3/HOOK-01", "HOOK-01", "v3.3", "Test-Network",
                  hook, "audit-only", "", audit_v33),
        MatrixRow("v3.3/HOOK-02", "HOOK-02", "v3.3", "Test-Network",
                  hook, "audit-only", "", audit_v33),
        MatrixRow("v3.3/HOOK-03", "HOOK-03", "v3.3", "Test-Network",
                  hook, "audit-only", "", audit_v33),
        MatrixRow("v3.3/HOOK-04", "HOOK-04", "v3.3", "Test-Network",
                  hook, "reproducible", hook, ""),
        MatrixRow("v3.3/HOOK-05", "HOOK-05", "v3.3", "Test-Network",
                  hook, "reproducible", hook, ""),
        MatrixRow("v3.3/HOOK-06", "HOOK-06", "v3.3", "Test-Network",
                  hook, "audit-only", "", audit_v33),
        # v3.13 INFRA rows (CI extension)
        MatrixRow("v3.13/INFRA-01", "INFRA-01", "v3.13", "Test-Network",
                  "scripts/check-trigger-collisions.py",
                  "reproducible", "scripts/check-trigger-collisions.py", ""),
        MatrixRow("v3.13/INFRA-02", "INFRA-02", "v3.13", "Test-Network",
                  "scripts/check-description-budget.py",
                  "reproducible", "scripts/check-description-budget.py", ""),
        MatrixRow("v3.13/INFRA-03", "INFRA-03", "v3.13", "Test-Network",
                  "scripts/check-agent.py",
                  "reproducible", "scripts/check-agent.py", ""),
        MatrixRow("v3.13/INFRA-04", "INFRA-04", "v3.13", "Test-Network",
                  "scripts/check-links.py",
                  "reproducible", "scripts/check-links.py", ""),
        MatrixRow("v3.13/INFRA-05", "INFRA-05", "v3.13", "Test-Network",
                  "scripts/sync-content.py",
                  "reproducible", "scripts/sync-content.py", ""),
        MatrixRow("v3.13/INFRA-06", "INFRA-06", "v3.13", "Test-Network",
                  "scripts/check-trigger-collisions.py",
                  "reproducible", "scripts/check-trigger-collisions.py", ""),
    ]


def _rows_testnet_routing_battery() -> list[MatrixRow]:
    """Routing battery rows — Test-Network (v3.1 ROUTE + v3.4 NOISE + v3.5/3.6 CAT)."""
    cat = "tests/routing-catalog.md"
    audit_v31 = "Validated by v3.1-MILESTONE-AUDIT; no re-runnable gate"
    return [
        MatrixRow("v3.1/ROUTE-01", "ROUTE-01", "v3.1", "Test-Network",
                  "first-principles/agents/first-principles.md",
                  "audit-only", "", audit_v31),
        MatrixRow("v3.1/ROUTE-02", "ROUTE-02", "v3.1", "Test-Network",
                  "scripts/check-routing.py",
                  "reproducible", "scripts/check-routing.py", ""),
        MatrixRow("v3.1/ROUTE-03", "ROUTE-03", "v3.1", "Test-Network",
                  "docs/testing-agents-headlessly.md",
                  "audit-only", "", audit_v31),
        MatrixRow("v3.1/DOC-01", "DOC-01", "v3.1", "Test-Network",
                  "docs/testing-agents-headlessly.md",
                  "audit-only", "", audit_v31),
        MatrixRow("v3.4/NOISE-01", "NOISE-01", "v3.4", "Test-Network",
                  "scripts/check-routing.py",
                  "reproducible", "scripts/check-routing.py", ""),
        MatrixRow("v3.4/NOISE-02", "NOISE-02", "v3.4", "Test-Network",
                  "scripts/check-routing.py",
                  "reproducible", "scripts/check-routing.py", ""),
        MatrixRow("v3.4/NOISE-03", "NOISE-03", "v3.4", "Test-Network",
                  "scripts/check-routing.py",
                  "reproducible", "scripts/check-routing.py", ""),
        MatrixRow("v3.4/NOISE-04", "NOISE-04", "v3.4", "Test-Network",
                  "scripts/check-routing.py",
                  "reproducible", "scripts/check-routing.py", ""),
        MatrixRow("v3.4/NOISE-05", "NOISE-05", "v3.4", "Test-Network",
                  "scripts/check-routing.py",
                  "reproducible", "scripts/check-routing.py", ""),
        MatrixRow("v3.4/NOISE-06", "NOISE-06", "v3.4", "Test-Network",
                  "scripts/check-routing.py",
                  "reproducible", "scripts/check-routing.py", ""),
        MatrixRow("v3.5/FRAG-01", "FRAG-01", "v3.5", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.5/FRAG-02", "FRAG-02", "v3.5", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.5/FRAG-03", "FRAG-03", "v3.5", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.5/FRAG-04", "FRAG-04", "v3.5", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.5/FRAG-05", "FRAG-05", "v3.5", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.5/FRAG-06", "FRAG-06", "v3.5", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.5/FRAG-07", "FRAG-07", "v3.5", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.5/FRAG-08", "FRAG-08", "v3.5", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.5/FRAG-09", "FRAG-09", "v3.5", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.6/CAT-01", "CAT-01", "v3.6", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.6/CAT-02", "CAT-02", "v3.6", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.6/CAT-03", "CAT-03", "v3.6", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.6/CAT-04", "CAT-04", "v3.6", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.6/CAT-05", "CAT-05", "v3.6", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.6/CAT-06", "CAT-06", "v3.6", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.6/CAT-07", "CAT-07", "v3.6", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.6/CAT-08", "CAT-08", "v3.6", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.6/CAT-09", "CAT-09", "v3.6", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.6/CAT-10", "CAT-10", "v3.6", "Test-Network",
                  cat, "reproducible", cat, ""),
    ]


def _rows_testnet_routing_v38() -> list[MatrixRow]:
    """v3.8 FIXTURE/VERIFY/DOC-01 routing test rows — Test-Network."""
    audit_v38 = "Validated by v3.8-MILESTONE-AUDIT; no re-runnable gate"
    batt_script = "scripts/check-routing-battery.py"
    return [
        MatrixRow("v3.8/FIXTURE-01", "FIXTURE-01", "v3.8", "Test-Network",
                  "tests/step0-fixture-catalog.md",
                  "audit-only", "", audit_v38),
        MatrixRow("v3.8/FIXTURE-02", "FIXTURE-02", "v3.8", "Test-Network",
                  "tests/step0-fixture-catalog.md",
                  "audit-only", "", audit_v38),
        MatrixRow("v3.8/VERIFY-01", "VERIFY-01", "v3.8", "Test-Network",
                  batt_script, "reproducible", batt_script, ""),
        MatrixRow("v3.8/VERIFY-02", "VERIFY-02", "v3.8", "Test-Network",
                  batt_script, "reproducible", batt_script, ""),
        MatrixRow("v3.8/VERIFY-03", "VERIFY-03", "v3.8", "Test-Network",
                  batt_script, "reproducible", batt_script, ""),
        MatrixRow("v3.8/DOC-01", "DOC-01", "v3.8", "Test-Network",
                  "docs/testing-agents-headlessly.md",
                  "audit-only", "", audit_v38),
    ]


def _rows_testnet_routing_v39_plus() -> list[MatrixRow]:
    """v3.9 P8, v3.10 CONV, v3.11 MON, v3.13 META — Test-Network."""
    cat = "tests/routing-catalog.md"
    batt = "tests/routing-battery-catalog.md"
    audit_v39 = "Validated by v3.9-MILESTONE-AUDIT; no re-runnable gate"
    audit_v311 = "Validated by v3.11-MILESTONE-AUDIT; no re-runnable gate"
    return [
        # v3.9 P8 routing fix
        MatrixRow("v3.9/P8-01", "P8-01", "v3.9", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.9/P8-02", "P8-02", "v3.9", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.9/P8-03", "P8-03", "v3.9", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.9/P8-04", "P8-04", "v3.9", "Test-Network",
                  cat, "reproducible", cat, ""),
        # v3.10 CONV — convention files (test-network: new test gates)
        MatrixRow("v3.10/CONV-01", "CONV-01", "v3.10", "Test-Network",
                  ".planning/phases",
                  "audit-only", "",
                  "Validated by v3.10-MILESTONE-AUDIT; VERIFICATION.md convention files"),
        MatrixRow("v3.10/CONV-02", "CONV-02", "v3.10", "Test-Network",
                  ".planning/phases",
                  "audit-only", "",
                  "Validated by v3.10-MILESTONE-AUDIT; VALIDATION.md convention files"),
        # v3.11 MON — routing forward monitoring
        MatrixRow("v3.11/MON-01", "MON-01", "v3.11", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.11/MON-02", "MON-02", "v3.11", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.11/MON-03", "MON-03", "v3.11", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.11/MON-04", "MON-04", "v3.11", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.11/MON-05", "MON-05", "v3.11", "Test-Network",
                  cat, "audit-only", "", audit_v311),
        # v3.13 META-01/02 (routing-catalog content)
        MatrixRow("v3.13/META-01", "META-01", "v3.13", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.13/META-02", "META-02", "v3.13", "Test-Network",
                  cat, "reproducible", cat, ""),
    ]


def _rows_testnet_merged_battery() -> list[MatrixRow]:
    """v4.2 focused-output + v4.3 BATT merged-battery rows — Test-Network."""
    batt = "scripts/check-routing-battery.py"
    audit_v42 = "Validated by v4.2-MILESTONE-AUDIT; no re-runnable gate"
    audit_v43 = "Validated by v4.3-MILESTONE-AUDIT; no re-runnable gate"
    bcat = "tests/routing-battery-catalog.md"
    return [
        MatrixRow("v4.2/CAT-01", "CAT-01", "v4.2", "Test-Network",
                  bcat, "reproducible", batt, ""),
        MatrixRow("v4.2/CAT-02", "CAT-02", "v4.2", "Test-Network",
                  bcat, "reproducible", batt, ""),
        MatrixRow("v4.2/CAT-03", "CAT-03", "v4.2", "Test-Network",
                  bcat, "reproducible", batt, ""),
        MatrixRow("v4.2/CAT-04", "CAT-04", "v4.2", "Test-Network",
                  bcat, "reproducible", batt, ""),
        MatrixRow("v4.2/FOCUS-01", "FOCUS-01", "v4.2", "Test-Network",
                  batt, "reproducible", batt, ""),
        MatrixRow("v4.2/FOCUS-02", "FOCUS-02", "v4.2", "Test-Network",
                  batt, "reproducible", batt, ""),
        MatrixRow("v4.2/FOCUS-03", "FOCUS-03", "v4.2", "Test-Network",
                  batt, "reproducible", batt, ""),
        MatrixRow("v4.2/STRICT-01", "STRICT-01", "v4.2", "Test-Network",
                  batt, "reproducible", batt, ""),
        MatrixRow("v4.2/STRICT-02", "STRICT-02", "v4.2", "Test-Network",
                  batt, "reproducible", batt, ""),
        MatrixRow("v4.2/BASE-01", "BASE-01", "v4.2", "Test-Network",
                  "tests/routing-battery-baseline-v4.3.md",
                  "reproducible",
                  "tests/test_69_merged_baseline_invariants.py", ""),
        MatrixRow("v4.2/BASE-02", "BASE-02", "v4.2", "Test-Network",
                  "tests/routing-battery-baseline-v4.3.md",
                  "reproducible",
                  "tests/test_69_merged_baseline_invariants.py", ""),
        MatrixRow("v4.3/BATT-01", "BATT-01", "v4.3", "Test-Network",
                  batt, "reproducible", batt, ""),
        MatrixRow("v4.3/BATT-02", "BATT-02", "v4.3", "Test-Network",
                  batt, "reproducible", batt, ""),
        MatrixRow("v4.3/BATT-03", "BATT-03", "v4.3", "Test-Network",
                  batt, "reproducible", batt, ""),
        MatrixRow("v4.3/BATT-04", "BATT-04", "v4.3", "Test-Network",
                  batt, "reproducible", batt, ""),
        MatrixRow("v4.3/BATT-05", "BATT-05", "v4.3", "Test-Network",
                  batt, "reproducible", batt, ""),
        MatrixRow("v4.3/BATT-06", "BATT-06", "v4.3", "Test-Network",
                  batt, "reproducible", batt, ""),
        MatrixRow("v4.3/BATT-07", "BATT-07", "v4.3", "Test-Network",
                  "tests/routing-battery-baseline-v4.3.md",
                  "reproducible",
                  "tests/test_69_merged_baseline_invariants.py", ""),
        MatrixRow("v4.3/BATT-08", "BATT-08", "v4.3", "Test-Network",
                  "tests/routing-battery-baseline-v4.3.md",
                  "reproducible",
                  "tests/test_69_merged_baseline_invariants.py", ""),
    ]


def _rows_testnet_step0_harness() -> list[MatrixRow]:
    """v5.0 STEP0, v5.1 FIX/DET/SAFE/BASE — Test-Network."""
    emul = "scripts/check-step0-emulator.py"
    live = "scripts/check-step0-live.py"
    cat = "tests/step0-fixture-catalog.md"
    audit_v51 = "Validated by v5.1-MILESTONE-AUDIT; no re-runnable gate"
    return [
        # v5.0 Step 0 harness rows
        MatrixRow("v5.0/STEP0-01", "STEP0-01", "v5.0", "Test-Network",
                  emul, "reproducible", emul, ""),
        MatrixRow("v5.0/STEP0-02", "STEP0-02", "v5.0", "Test-Network",
                  live, "reproducible", live, ""),
        MatrixRow("v5.0/STEP0-03", "STEP0-03", "v5.0", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v5.0/STEP0-04", "STEP0-04", "v5.0", "Test-Network",
                  emul, "reproducible", emul, ""),
        MatrixRow("v5.0/STEP0-05", "STEP0-05", "v5.0", "Test-Network",
                  live, "reproducible", live, ""),
        MatrixRow("v5.0/STEP0-06", "STEP0-06", "v5.0", "Test-Network",
                  live, "reproducible", live, ""),
        MatrixRow("v5.0/STEP0-07", "STEP0-07", "v5.0", "Test-Network",
                  live, "reproducible", live, ""),
        MatrixRow("v5.0/STEP0-08", "STEP0-08", "v5.0", "Test-Network",
                  emul, "reproducible", emul, ""),
        MatrixRow("v5.0/STEP0-09", "STEP0-09", "v5.0", "Test-Network",
                  cat, "reproducible", cat, ""),
        # v5.1 detector fix + safe rows
        MatrixRow("v5.1/FIX-01", "FIX-01", "v5.1", "Test-Network",
                  emul, "reproducible", emul, ""),
        MatrixRow("v5.1/FIX-02", "FIX-02", "v5.1", "Test-Network",
                  emul, "reproducible", emul, ""),
        MatrixRow("v5.1/FIX-03", "FIX-03", "v5.1", "Test-Network",
                  emul, "reproducible", emul, ""),
        MatrixRow("v5.1/DET-01", "DET-01", "v5.1", "Test-Network",
                  emul, "reproducible", emul, ""),
        MatrixRow("v5.1/DET-02", "DET-02", "v5.1", "Test-Network",
                  emul, "reproducible", emul, ""),
        MatrixRow("v5.1/DET-03", "DET-03", "v5.1", "Test-Network",
                  emul, "reproducible", emul, ""),
        MatrixRow("v5.1/SAFE-01", "SAFE-01", "v5.1", "Test-Network",
                  emul, "reproducible", emul, ""),
        MatrixRow("v5.1/SAFE-02", "SAFE-02", "v5.1", "Test-Network",
                  emul, "reproducible", emul, ""),
        MatrixRow("v5.1/SAFE-03", "SAFE-03", "v5.1", "Test-Network",
                  emul, "reproducible", emul, ""),
        MatrixRow("v5.1/BASE-01", "BASE-01", "v5.1", "Test-Network",
                  "tests/step0-baseline-v5.1.md",
                  "audit-only", "", audit_v51),
        MatrixRow("v5.1/BASE-02", "BASE-02", "v5.1", "Test-Network",
                  "tests/step0-baseline-v5.1.md",
                  "audit-only", "", audit_v51),
        MatrixRow("v5.1/BASE-03", "BASE-03", "v5.1", "Test-Network",
                  "tests/step0-baseline-v5.1.md",
                  "audit-only", "", audit_v51),
        MatrixRow("v5.1/BASE-04", "BASE-04", "v5.1", "Test-Network",
                  "tests/step0-baseline-v5.1.md",
                  "audit-only", "", audit_v51),
    ]


def _rows_testnet_v52_v53() -> list[MatrixRow]:
    """v5.2 DIAG/DET/ROUTE-10/REBASE + v5.3 DET/SAFE/REBASE/TOOL-01 — Test-Network."""
    emul = "scripts/check-step0-emulator.py"
    live = "scripts/check-step0-live.py"
    audit_v52 = "Validated by v5.2-MILESTONE-AUDIT; no re-runnable gate"
    audit_v53 = "Validated by v5.3-MILESTONE-AUDIT; no re-runnable gate"
    agent = "first-principles/agents/first-principles.md"
    return [
        MatrixRow("v5.2/DIAG-01", "DIAG-01", "v5.2", "Test-Network",
                  emul, "audit-only", "", audit_v52),
        MatrixRow("v5.2/DIAG-02", "DIAG-02", "v5.2", "Test-Network",
                  emul, "audit-only", "", audit_v52),
        MatrixRow("v5.2/DIAG-03", "DIAG-03", "v5.2", "Test-Network",
                  emul, "audit-only", "", audit_v52),
        MatrixRow("v5.2/DET-10", "DET-10", "v5.2", "Test-Network",
                  emul, "reproducible", emul, ""),
        MatrixRow("v5.2/DET-11", "DET-11", "v5.2", "Test-Network",
                  emul, "reproducible", emul, ""),
        MatrixRow("v5.2/DET-12", "DET-12", "v5.2", "Test-Network",
                  emul, "reproducible", emul, ""),
        MatrixRow("v5.2/ROUTE-10", "ROUTE-10", "v5.2", "Methodology",
                  agent, "audit-only", "", audit_v52),
        MatrixRow("v5.2/REBASE-01", "REBASE-01", "v5.2", "Test-Network",
                  "tests/step0-baseline-v5.2.md",
                  "audit-only", "", audit_v52),
        MatrixRow("v5.2/REBASE-02", "REBASE-02", "v5.2", "Test-Network",
                  "tests/step0-baseline-v5.2.md",
                  "audit-only", "", audit_v52),
        MatrixRow("v5.2/REBASE-03", "REBASE-03", "v5.2", "Test-Network",
                  "tests/step0-baseline-v5.2.md",
                  "audit-only", "", audit_v52),
        MatrixRow("v5.3/DET-13", "DET-13", "v5.3", "Test-Network",
                  emul, "reproducible", emul, ""),
        MatrixRow("v5.3/DET-14", "DET-14", "v5.3", "Test-Network",
                  emul, "reproducible", emul, ""),
        MatrixRow("v5.3/DET-15", "DET-15", "v5.3", "Test-Network",
                  emul, "reproducible", emul, ""),
        MatrixRow("v5.3/SAFE-04", "SAFE-04", "v5.3", "Test-Network",
                  emul, "reproducible", emul, ""),
        MatrixRow("v5.3/REBASE-04", "REBASE-04", "v5.3", "Test-Network",
                  "tests/step0-baseline-v5.3.md",
                  "audit-only", "", audit_v53),
        MatrixRow("v5.3/REBASE-05", "REBASE-05", "v5.3", "Test-Network",
                  "tests/step0-baseline-v5.3.md",
                  "audit-only", "", audit_v53),
        # v5.3/TOOL-01: quick task closure for check-routing.py (Test-Network)
        MatrixRow("v5.3/TOOL-01", "TOOL-01", "v5.3", "Test-Network",
                  "scripts/check-routing.py",
                  "audit-only", "", audit_v53),
    ]



def _rows_active_tail() -> list[MatrixRow]:
    """D-05 path (b): active-tail rows — included unconditionally, mixed tiers.

    These residuals are exempt from the deliverable-existence gate. GEN-01 has
    been flipped from 'scheduled' to 'reproducible' (Phase 93, D-08) — the Step 0
    classifier capability is now reproducibly measured by the committed v7.6 live
    re-baseline (tests/step0-baseline-v7.6.md, Phase 114). Earned by the committed
    baseline, not a passing score (BATTERY: FAIL, P 3/8 REGRESSION — honest
    v7.6 measured state). GEN-02 has been converted to coverage_tier='reproducible'
    (runbook + wrapper script, Phase 89) and no longer belongs to the open-gap set.

    Key form: v5.3/GEN-01 and v5.3/GEN-02 carry the canonical v5.3 milestone
    prefix. RR-80-01, RR-79-01, RR-114-01, RR-108-02, and RR-77-08 are non-milestone
    residuals that use the _RESIDUAL_KEY_PREFIX (confirmed at Task 3 checkpoint,
    82-02). RR-114-01 supersedes RR-108-01 (Phase 114 v7.6 carry-forward, S-P02
    inversion CARRIED 1/5); RR-108-02 is CLOSED at 4/5 (Phase 114 v7.6 re-baseline,
    S-P05 trade-off cleared min-pass — the lone canonical improver; ID retained,
    sentinel present as regression guard). Full chains: RR-79-02 ->
    RR-92-01 -> RR-95-01 -> RR-108-01 -> RR-114-01 (S-P02); RR-79-03 -> RR-92-02 ->
    RR-95-02 -> RR-108-02 CLOSED (S-P05).
    """
    p = _RESIDUAL_KEY_PREFIX  # e.g. "residual" — confirmed Task 3 checkpoint
    tail_rationale_gen01 = (
        "Full Step 0 classifier rearchitecture (GEN-01-REARCH, Phases 91-93). "
        "GEN-01 is now reproducible: the Step 0 classifier capability is reproducibly "
        "measured by committed live re-baselines (latest: v7.13 residual-delta, Phase 137). "
        "Earned by the committed baseline, not a passing score (reproducible = measured, not passing). "
        "Phase 129 v7.11 8-technique BATTERY: FAIL, P 4/8 (S-P01 5/5, S-P03 4/5, S-P05 5/5, "
        "S-P06 4/5 PASS; S-P02 2/5, S-P04 2/5, S-P10 0/5, S-P14 0/5 FAIL) — honest measured "
        "state (honesty-not-score, D-01). Prior baselines frozen: v7.6 (Phase 114, FAIL), "
        "v7.7 (Phase 117 CONF-01, SHORT OF BAR), v7.8 (Phase 119 CONF-03, targeted 6-row PASS). "
        "v7.11 dispositions (Phase 129; see docs/whole-system-remeasure-verdict.md): "
        "RR-79-01 S-P01 CLOSE SUSTAINED 5/5; RR-117-01 S-P03 fishbone CLOSE SUSTAINED 4/5; "
        "RR-108-02 S-P05 trade-off CLOSE SUSTAINED 5/5; "
        "RR-114-01 S-P02 inversion CARRIED 2/5 (supersedes RR-108-01); "
        "RR-108-04 estimate CARRIED 0/5; RR-108-05 theoretical-limit CARRIED 0/5 "
        "(both first genuine live measurement, v7.4 was spend-limit-indeterminate); "
        "RR-108-03 decompose RESOLVED-BY-MERGE (v7.5; sentinel stays on frozen v7.4 evidence). "
        "v7.13 residual-delta re-measure (Phase 137, 3-row filtered catalog; "
        "tests/step0-baseline-v7.8.md remains the canonical full 8-technique baseline): "
        "S-P02 inversion 1/5 CARRIED (RR-114-01, ID kept, no successor); "
        "S-P10 estimate 0/5 CARRIED (RR-108-04, ID kept); "
        "S-P14 theoretical-limit 0/5 CARRIED (RR-108-05, ID kept). "
        "Confirming artifact: tests/step0-baseline-v7.13.md."
    )
    tail_rationale_gen02 = (
        "Runbook + wrapper script established (Phase 89). Cadence: milestone boundary + "
        "detector-surface changes. See docs/live-monitoring-runbook.md."
    )
    return [
        MatrixRow(f"{p}/RR-80-01", "RR-80-01", p, "Test-Network",
                  "active-tail", "reproducible", "scripts/_battery_core.py#self_test_boundary", ""),
        MatrixRow("v5.3/GEN-01", "GEN-01", "v5.3", "Test-Network",
                  "active-tail", "reproducible", "tests/step0-baseline-v7.13.md",
                  tail_rationale_gen01),
        MatrixRow("v5.3/GEN-02", "GEN-02", "v5.3", "Test-Network",
                  "active-tail", "reproducible", "docs/live-monitoring-runbook.md",
                  tail_rationale_gen02),
        MatrixRow(f"{p}/RR-79-01", "RR-79-01", p, "Test-Network",
                  "active-tail", "reproducible", "scripts/_battery_core.py#self_test_boundary", ""),
        # RR-114-01 supersedes RR-108-01 (Phase 114 v7.6 carry-forward, S-P02 inversion CARRIED 1/5)
        # Full chain: RR-79-02 -> RR-92-01 -> RR-95-01 -> RR-108-01 -> RR-114-01
        MatrixRow(f"{p}/RR-114-01", "RR-114-01", p, "Test-Network",
                  "active-tail", "reproducible", "scripts/_battery_core.py#self_test_boundary", ""),
        # RR-108-02 supersedes RR-95-02 (Phase 108 v7.4 carry-forward, S-P05 trade-off CARRIED 2/5)
        # Full chain: RR-79-03 -> RR-92-02 -> RR-95-02 -> RR-108-02 CLOSED
        # CLOSED at 4/5 ≥ min-pass at Phase 114 v7.6 re-baseline (lone canonical improver;
        # ID retained, sentinel in _battery_core.self_test_boundary() re-pointed to v7.6 vector)
        MatrixRow(f"{p}/RR-108-02", "RR-108-02", p, "Test-Network",
                  "active-tail", "reproducible", "scripts/_battery_core.py#self_test_boundary", ""),
        MatrixRow(f"{p}/RR-77-08", "RR-77-08", p, "Test-Network",
                  "active-tail", "reproducible", "scripts/_battery_core.py#self_test_boundary", ""),
        # RR-117-01: S-P03 fishbone CLOSED at 5/5 at Phase 117 CONF-01; CLOSE SUSTAINED 4/5 at v7.8 CONF-03.
        # First fishbone vector sentinel; RR-75-03 lineage; re-pointed to v7.8 in Phase 119 CONF-04.
        MatrixRow(f"{p}/RR-117-01", "RR-117-01", p, "Test-Network",
                  "active-tail", "reproducible", "scripts/_battery_core.py#self_test_boundary", ""),
        # RR-117-02: S-N03 precision sentinel; D-17 precision finding; re-pointed to v7.8 in Phase 119 CONF-04.
        MatrixRow(f"{p}/RR-117-02", "RR-117-02", p, "Test-Network",
                  "active-tail", "reproducible", "scripts/_battery_core.py#self_test_boundary", ""),
        # RR-119-01: S-N01 over-routing RESOLVED-OVER-BAR at Phase 119 CONF-03 (v7.8 vector [0,2,1,1,3]).
        # Under-count caveat documented; NOT a reclassification (D-4, Phase 119 CONF-04).
        MatrixRow(f"{p}/RR-119-01", "RR-119-01", p, "Test-Network",
                  "active-tail", "reproducible", "scripts/_battery_core.py#self_test_boundary", ""),
        # RR-119-02: S-N02 over-routing RESOLVED-OVER-BAR at Phase 119 CONF-03 (v7.8 vector [0,3,3,1,1]).
        # Under-count caveat documented; NOT a reclassification (D-4, Phase 119 CONF-04).
        MatrixRow(f"{p}/RR-119-02", "RR-119-02", p, "Test-Network",
                  "active-tail", "reproducible", "scripts/_battery_core.py#self_test_boundary", ""),
    ]


def _rows_v79() -> list[MatrixRow]:
    """v7.9 milestone rows — 8 reproducible requirements (D-01 / Phase 123).

    All rows carry milestone="v7.9", coverage_tier="reproducible", gap_rationale="".
    Keys use the milestone-qualified form "v7.9/<bare_id>".

    D-02 PROHIBITION: no coverage_tier="scheduled" row here; RR-114-01 / trade-off
    live re-measure is a documented residual handled as prose in 123-02 (not a
    matrix row).

    The 8 requirements and their V79-ROWS TRACE-03 sentinel lock are added here
    as the first milestone block since v5.3. Three fix phases produce them:
      Phase 120 (Fix #3): NEGCAT-01/02 — Step 0 negative-catalog expansion
      Phase 121 (Fix #4): OCH-01/02/03 — output-contract headers + detector
      Phase 122 (Fix #5): COLLIDE-01/02 — dual-install collision checker
      Phase 123 (RECON):  RECON-01 — traceability reconcile + battery green

    Artifact_link resolution notes:
      NEGCAT-01/02: scripts/check-step0-emulator.py (owns STEP0-08 NEGCAT assertions)
      OCH-01:       scripts/sync-content.py (DUAL-04 gate; agent body zero-drift proven)
      OCH-02:       scripts/check-routing-battery.py (BATT-06 owns inversion/trade-off
                    heading-anchored marker assertions)
      OCH-03:       scripts/_battery_core.py#self_test_boundary (anchor substring in file)
      COLLIDE-01/02: scripts/check-install-collisions.py (COLLIDE-01 CI gate)
      RECON-01:     scripts/check-traceability.py (TRACE-03 self-test, this file)
    """
    return [
        MatrixRow("v7.9/NEGCAT-01", "NEGCAT-01", "v7.9", "Test-Network",
                  "tests/step0-fixture-catalog.md",
                  "reproducible", "scripts/check-step0-emulator.py", ""),
        MatrixRow("v7.9/NEGCAT-02", "NEGCAT-02", "v7.9", "Test-Network",
                  "scripts/check-step0-emulator.py",
                  "reproducible", "scripts/check-step0-emulator.py", ""),
        MatrixRow("v7.9/OCH-01", "OCH-01", "v7.9", "Methodology",
                  "shared/references/inversion.md",
                  "reproducible", "scripts/sync-content.py", ""),
        MatrixRow("v7.9/OCH-02", "OCH-02", "v7.9", "Test-Network",
                  "scripts/_battery_core.py",
                  "reproducible", "scripts/check-routing-battery.py", ""),
        MatrixRow("v7.9/OCH-03", "OCH-03", "v7.9", "Test-Network",
                  "scripts/_battery_core.py",
                  "reproducible", "scripts/_battery_core.py#self_test_boundary", ""),
        MatrixRow("v7.9/COLLIDE-01", "COLLIDE-01", "v7.9", "Test-Network",
                  "scripts/check-install-collisions.py",
                  "reproducible", "scripts/check-install-collisions.py", ""),
        MatrixRow("v7.9/COLLIDE-02", "COLLIDE-02", "v7.9", "Test-Network",
                  ".github/workflows/validation.yml",
                  "reproducible", "scripts/check-install-collisions.py", ""),
        MatrixRow("v7.9/RECON-01", "RECON-01", "v7.9", "Test-Network",
                  "docs/requirements-traceability.md",
                  "reproducible", "scripts/check-traceability.py", ""),
    ]


def _rows_v711() -> list[MatrixRow]:
    """v7.11 milestone rows — 11 audit-only requirements (D-04 / Phase 131).

    The v7.11 milestone is a whole-system live re-measure. Its own requirements
    (harness-readiness firewall, the three live re-baselines, and the terminal
    reconcile) are verified by ONE-SHOT MANUAL LIVE RUNS, not deterministic offline
    CI gates — so they are tiered "audit-only" (they grow the audit-only count, not
    reproducible), with artifact_link="" and a non-empty gap_rationale (D-04).

    Keys use the milestone-qualified form "v7.11/<bare_id>" — the "v7.11/" prefix
    prevents collision with the existing "v7.9/RECON-01" row.

    RR-130-01 (the main-routing inline-answering regression) is a DOCUMENTED RESIDUAL
    with NO matrix row (v7.9 D-02 precedent) — it is recorded as prose in
    docs/requirements-traceability.md, not here.
    """
    audit_v711 = (
        "Validated by the v7.11 whole-system live re-baseline (Phases 128-131); "
        "one-shot manual live run, no re-runnable offline gate (D-04). "
        "See docs/whole-system-remeasure-verdict.md."
    )
    return [
        MatrixRow("v7.11/READY-01", "READY-01", "v7.11", "Test-Network",
                  "scripts/check-firewall-battery.sh", "audit-only", "", audit_v711),
        MatrixRow("v7.11/READY-02", "READY-02", "v7.11", "Test-Network",
                  "scripts/check-step0-live.py", "audit-only", "", audit_v711),
        MatrixRow("v7.11/READY-03", "READY-03", "v7.11", "Test-Network",
                  "scripts/check-firewall-battery.sh", "audit-only", "", audit_v711),
        MatrixRow("v7.11/STEP0L-01", "STEP0L-01", "v7.11", "Test-Network",
                  "tests/step0-baseline-v7.11.md", "audit-only", "", audit_v711),
        MatrixRow("v7.11/STEP0L-02", "STEP0L-02", "v7.11", "Test-Network",
                  "tests/step0-baseline-v7.11.md", "audit-only", "", audit_v711),
        MatrixRow("v7.11/STEP0L-03", "STEP0L-03", "v7.11", "Test-Network",
                  "tests/step0-baseline-v7.11.md", "audit-only", "", audit_v711),
        MatrixRow("v7.11/ROUTEL-01", "ROUTEL-01", "v7.11", "Test-Network",
                  "tests/routing-baseline-v7.11.md", "audit-only", "", audit_v711),
        MatrixRow("v7.11/ROUTEL-02", "ROUTEL-02", "v7.11", "Test-Network",
                  "tests/routing-battery-baseline-v7.11.md", "audit-only", "", audit_v711),
        MatrixRow("v7.11/RECON-01", "RECON-01", "v7.11", "Test-Network",
                  "docs/whole-system-remeasure-verdict.md", "audit-only", "", audit_v711),
        MatrixRow("v7.11/RECON-02", "RECON-02", "v7.11", "Test-Network",
                  "tests/step0-captures-v7.11", "audit-only", "", audit_v711),
        MatrixRow("v7.11/RECON-03", "RECON-03", "v7.11", "Test-Network",
                  "docs/requirements-matrix.md", "audit-only", "", audit_v711),
    ]


def _rows_v818() -> list[MatrixRow]:
    """v8.18 milestone rows — 23 requirements, 21 reproducible + 2 audit-only (D-05/D-06, Phase 4).

    All rows carry milestone="v8.18". Keys use the milestone-qualified form
    "v8.18/<bare_id>".

    D-05 departure from Phase 142 D-01: `docs/requirements-traceability.md:11` records that
    v7.12, v7.13 and v8.0 requirements are validated by their milestone audits rather than
    matrix rows, because those milestones were live-measure and audit work with no
    deterministic offline gate behind their requirements. No v8.x milestone has added a row
    since v7.9 (Phase 123) for that reason. v8.18's requirements are the first since v7.9 to
    pass headline-history row 2's test — "each backed by a deterministic offline gate" —
    because HARN-01/HARN-02/HARN-03 are deterministic, offline, and (per D-01/D-03) both
    battery- and CI-registered. This is an application of the existing rule, not an exception
    to it. See the dated addendum beside the Phase 142 D-01 note in
    docs/requirements-traceability.md (D-08: the original note stays byte-intact).

    Capability assignment: ACT-*/LOOP-*/PAR-* change the agent's methodology prose, so they
    are "Methodology"; HARN-01..04 and SHIP-01/02/03/06 are harness and release apparatus, so
    they are "Test-Network"; SHIP-04 and SHIP-05 are records of the methodology milestone, so
    they are "Methodology" too — which under _SEVERITY_LABEL gives them MEDIUM rather than
    HIGH if either is ever downgraded to a gap, matching the judgment that a missing
    changelog entry is not a verification-system gap.

    Tiering (D-06, decided per row against "does something re-run", not by block):
    SHIP-04 (CHANGELOG entry exists) and SHIP-05 (docs record exists) are audit-only, with
    artifact_link="" and a non-empty gap_rationale — no gate re-runs to check a changelog
    entry or a docs/ record. The other 21 are reproducible with a named artifact_link:
      ACT-*                -> scripts/check-act-limb.py
      LOOP-*                -> scripts/check-loop-closure.py
      PAR-* / HARN-03       -> scripts/check-focused-parity.py
      HARN-01               -> scripts/check-act-limb.py
      HARN-02               -> scripts/check-loop-closure.py
      HARN-04, SHIP-03, SHIP-06 -> scripts/check-firewall-battery.sh
      SHIP-01               -> scripts/sync-content.py
      SHIP-02               -> scripts/check-version-stamps.py
    Rejected: all 23 reproducible (would give SHIP-04/SHIP-05 an artifact_link that does not
    exist — the vacuous-green shape this project has flagged four times).
    """
    audit_v818 = (
        "Validated by inspecting the shipped record — the CHANGELOG.md milestone entry "
        "(SHIP-04) or the docs/v8.18-praor-loop-closure.md milestone record (SHIP-05) — "
        "not by a re-runnable offline gate (D-06). No gate re-runs to check a changelog "
        "entry or a docs/ narrative exists, or is proposed, for either requirement."
    )
    return [
        MatrixRow("v8.18/ACT-01", "ACT-01", "v8.18", "Methodology",
                  "shared/spine/SKILL-body.md",
                  "reproducible", "scripts/check-act-limb.py", ""),
        MatrixRow("v8.18/ACT-02", "ACT-02", "v8.18", "Methodology",
                  "shared/spine/SKILL-body.md",
                  "reproducible", "scripts/check-act-limb.py", ""),
        MatrixRow("v8.18/ACT-03", "ACT-03", "v8.18", "Methodology",
                  "shared/spine/SKILL-body.md",
                  "reproducible", "scripts/check-act-limb.py", ""),
        MatrixRow("v8.18/ACT-04", "ACT-04", "v8.18", "Methodology",
                  "shared/spine/SKILL-body.md",
                  "reproducible", "scripts/check-act-limb.py", ""),
        MatrixRow("v8.18/ACT-05", "ACT-05", "v8.18", "Methodology",
                  "shared/spine/references/validation-rubric.md",
                  "reproducible", "scripts/check-act-limb.py", ""),
        MatrixRow("v8.18/LOOP-01", "LOOP-01", "v8.18", "Methodology",
                  "shared/spine/SKILL-body.md",
                  "reproducible", "scripts/check-loop-closure.py", ""),
        MatrixRow("v8.18/LOOP-02", "LOOP-02", "v8.18", "Methodology",
                  "shared/agent/input-contract.md",
                  "reproducible", "scripts/check-loop-closure.py", ""),
        MatrixRow("v8.18/LOOP-03", "LOOP-03", "v8.18", "Methodology",
                  "shared/spine/references/validation-rubric.md",
                  "reproducible", "scripts/check-loop-closure.py", ""),
        MatrixRow("v8.18/LOOP-04", "LOOP-04", "v8.18", "Methodology",
                  "shared/spine/SKILL-body.md",
                  "reproducible", "scripts/check-loop-closure.py", ""),
        MatrixRow("v8.18/LOOP-05", "LOOP-05", "v8.18", "Methodology",
                  "shared/spine/SKILL-body.md",
                  "reproducible", "scripts/check-loop-closure.py", ""),
        MatrixRow("v8.18/PAR-01", "PAR-01", "v8.18", "Methodology",
                  "shared/spine/SKILL-body.md",
                  "reproducible", "scripts/check-focused-parity.py", ""),
        MatrixRow("v8.18/PAR-02", "PAR-02", "v8.18", "Methodology",
                  "shared/spine/focused-validation-step.md",
                  "reproducible", "scripts/check-focused-parity.py", ""),
        MatrixRow("v8.18/PAR-03", "PAR-03", "v8.18", "Methodology",
                  "shared/spine/SKILL-body.md",
                  "reproducible", "scripts/check-focused-parity.py", ""),
        MatrixRow("v8.18/HARN-01", "HARN-01", "v8.18", "Test-Network",
                  "scripts/check-act-limb.py",
                  "reproducible", "scripts/check-act-limb.py", ""),
        MatrixRow("v8.18/HARN-02", "HARN-02", "v8.18", "Test-Network",
                  "scripts/check-loop-closure.py",
                  "reproducible", "scripts/check-loop-closure.py", ""),
        MatrixRow("v8.18/HARN-03", "HARN-03", "v8.18", "Test-Network",
                  "scripts/check-focused-parity.py",
                  "reproducible", "scripts/check-focused-parity.py", ""),
        MatrixRow("v8.18/HARN-04", "HARN-04", "v8.18", "Test-Network",
                  "scripts/check-firewall-battery.sh",
                  "reproducible", "scripts/check-firewall-battery.sh", ""),
        MatrixRow("v8.18/SHIP-01", "SHIP-01", "v8.18", "Test-Network",
                  "scripts/sync-content.py",
                  "reproducible", "scripts/sync-content.py", ""),
        MatrixRow("v8.18/SHIP-02", "SHIP-02", "v8.18", "Test-Network",
                  "scripts/check-version-stamps.py",
                  "reproducible", "scripts/check-version-stamps.py", ""),
        MatrixRow("v8.18/SHIP-03", "SHIP-03", "v8.18", "Test-Network",
                  "scripts/check-firewall-battery.sh",
                  "reproducible", "scripts/check-firewall-battery.sh", ""),
        MatrixRow("v8.18/SHIP-06", "SHIP-06", "v8.18", "Test-Network",
                  "scripts/check-firewall-battery.sh",
                  "reproducible", "scripts/check-firewall-battery.sh", ""),
        MatrixRow("v8.18/SHIP-04", "SHIP-04", "v8.18", "Methodology",
                  "CHANGELOG.md", "audit-only", "", audit_v818),
        MatrixRow("v8.18/SHIP-05", "SHIP-05", "v8.18", "Methodology",
                  "docs/v8.18-praor-loop-closure.md", "audit-only", "", audit_v818),
    ]


def _rows_v824() -> list[MatrixRow]:
    """v8.24 milestone rows — 15 requirements, 14 reproducible + 1 audit-only (D-06/D-07, Phase 6).

    All rows carry milestone="v8.24". Keys use the milestone-qualified form
    "v8.24/<bare_id>".

    Capability assignment, and the departure it makes: v8.18's discriminator was "changes the
    agent's methodology prose -> Methodology; harness and release apparatus -> Test-Network".
    None of v8.24's 15 requirements change agent methodology prose -- every one is verification
    apparatus or release bookkeeping -- so all 14 reproducible rows are Test-Network. VAL-04 is
    Methodology, following the SHIP-04/SHIP-05 carve-out exactly: an audit-only docs-record
    requirement is Methodology so _SEVERITY_LABEL reads MEDIUM rather than HIGH, matching this
    project's own stated judgment that a missing docs record is not a verification-system gap.
    This departs from 06-RESEARCH.md's "Open Questions" item 1, which recommended CAP-*/PROV-*
    -> Methodology, because those requirements are properties of gate scripts and a test
    fixture, not of the agent's prose.

    Tiering (D-07, decided per row against "does something re-run", not by block): 14
    reproducible, VAL-04 audit-only. All 15 reproducible is rejected for the same reason
    _rows_v818() rejects it -- VAL-04 would get an artifact_link that does not exist, the
    vacuous-green shape.

    CAP-01/CAP-03 (CR-02, v8.24 code review): both rows deliver into
    scripts/check-quality-harness.py, and both originally pointed their artifact_link at
    scripts/check-quality-harness.py's sibling scripts/check-provenance.py -- a script that
    mentions neither requirement and touches neither deliverable, so _resolve_artifact()'s
    bare-path existence check resolved it while nothing re-ran the requirement. Deleting the
    two self-test items would have left both rows reporting "reproducible" against an artifact
    that exists: the same vacuously-green shape the paragraph above rejects, and the shape
    headline-history row 6 (META-Q4) records. They now point at the assertions that actually
    re-run them, by symbol anchor rather than by file, so the link binds to the assertion:
    QUAL-01's _selftest_analysis_persistence() ("Item 20 (v8.24.0 Phase 4, CAP-01)") and
    _selftest_capture_tool_reader() ("Item 19 (v8.24.0 Phase 4, CAP-03)"). CAP-02 keeps
    scripts/check-provenance.py -- its deliverable is the committed fixture, which that
    script's live leg genuinely reads.

    GATE-02 (WR-02, v8.24 code review): this row used to point at
    scripts/check-firewall-battery.sh with a docstring note conceding that no offline gate
    re-read .github/workflows/validation.yml -- which made "reproducible" a claim nothing
    could falsify, the vacuously-green shape this function's tiering paragraph above rejects
    for VAL-04. REG-GUARD now carries a real leg for it: verify_ci_job_registration() reads
    the battery's own `gate "<ID>"` registrations and every CI job's `name: <job> (<GATE-ID>)`
    field, and fails when a battery gate has no CI job (QUAL-01 is the single named
    battery-only exemption). Deleting the check-provenance job from validation.yml now turns
    REG-GUARD red -- measured as a live negative control -- so the artifact_link points at
    that assertion by symbol anchor, binding the row to the check rather than to a file's mere
    existence.
    """
    audit_v824 = (
        "Validated by inspecting the shipped record -- CLAUDE.md's CI gates table and this "
        "file's PROV-GUARD record -- not by a re-runnable offline gate. No gate re-runs to "
        "check that a docs record exists, and none is proposed (the v8.18 SHIP-04/SHIP-05 "
        "precedent, D-07)."
    )
    return [
        MatrixRow("v8.24/CAP-01", "CAP-01", "v8.24", "Test-Network",
                  "scripts/check-quality-harness.py",
                  "reproducible",
                  "scripts/check-quality-harness.py#_selftest_analysis_persistence", ""),
        MatrixRow("v8.24/CAP-02", "CAP-02", "v8.24", "Test-Network",
                  "tests/quality-provenance-v8.24/README.md",
                  "reproducible", "scripts/check-provenance.py", ""),
        MatrixRow("v8.24/CAP-03", "CAP-03", "v8.24", "Test-Network",
                  "scripts/check-quality-harness.py",
                  "reproducible",
                  "scripts/check-quality-harness.py#_selftest_capture_tool_reader", ""),
        MatrixRow("v8.24/PROV-01", "PROV-01", "v8.24", "Test-Network",
                  "scripts/check-provenance.py",
                  "reproducible", "scripts/check-provenance.py", ""),
        MatrixRow("v8.24/PROV-02", "PROV-02", "v8.24", "Test-Network",
                  "scripts/check-provenance.py",
                  "reproducible", "scripts/check-provenance.py", ""),
        MatrixRow("v8.24/PROV-03", "PROV-03", "v8.24", "Test-Network",
                  "scripts/check-provenance.py",
                  "reproducible", "scripts/check-provenance.py", ""),
        MatrixRow("v8.24/PROV-04", "PROV-04", "v8.24", "Test-Network",
                  "scripts/check-provenance.py",
                  "reproducible", "scripts/check-provenance.py", ""),
        MatrixRow("v8.24/PROV-05", "PROV-05", "v8.24", "Test-Network",
                  "scripts/check-quality-harness.py",
                  "reproducible", "scripts/check-provenance.py", ""),
        MatrixRow("v8.24/GATE-01", "GATE-01", "v8.24", "Test-Network",
                  "scripts/check-provenance.py",
                  "reproducible", "scripts/check-provenance.py", ""),
        MatrixRow("v8.24/GATE-02", "GATE-02", "v8.24", "Test-Network",
                  ".github/workflows/validation.yml",
                  "reproducible",
                  "scripts/check-registration.py#verify_ci_job_registration", ""),
        MatrixRow("v8.24/GATE-03", "GATE-03", "v8.24", "Test-Network",
                  "scripts/check-firewall-battery.sh",
                  "reproducible", "scripts/check-firewall-battery.sh", ""),
        MatrixRow("v8.24/VAL-01", "VAL-01", "v8.24", "Test-Network",
                  "scripts/check-firewall-battery.sh",
                  "reproducible", "scripts/check-firewall-battery.sh", ""),
        MatrixRow("v8.24/VAL-02", "VAL-02", "v8.24", "Test-Network",
                  "scripts/check-version-stamps.py",
                  "reproducible", "scripts/check-version-stamps.py", ""),
        MatrixRow("v8.24/VAL-03", "VAL-03", "v8.24", "Test-Network",
                  "scripts/sync-content.py",
                  "reproducible", "scripts/sync-content.py", ""),
        MatrixRow("v8.24/VAL-04", "VAL-04", "v8.24", "Methodology",
                  "CLAUDE.md", "audit-only", "", audit_v824),
    ]


def build_matrix_rows() -> list[MatrixRow]:
    """Return the curated list of MatrixRow objects (Plan 02 — fully populated).

    Six inclusion paths. (a)-(c) were enumerated per the original D-05; (d) has been in the
    body since Phase 131 RECON-03 but went undocumented here until 2026-08-29; (e) was added
    at v8.18 Phase 4; (f) was added at v8.24 Phase 6.
    (a) Live-shipping requirements — deliverable-gated (D-01/D-02/D-03).
        Grouped by capability (D-04): Methodology first, then Test-Network.
    (b) Active tail — included unconditionally (see `_rows_active_tail()`); all reproducible (D-05b):
        GEN-01 reproducible (Phase 93 flip, artifact bumped to v7.11 baseline Phase 131 RECON-03),
        GEN-02 + residuals reproducible. RR-114-01 supersedes RR-108-01 (Phase 114 v7.6);
        RR-108-02 CLOSED at 4/5 v7.6 (ID retained, sentinel present);
        RR-117-01/RR-117-02 added Phase 117 CONF-02; RR-119-01/RR-119-02 added Phase 119 CONF-04.
    (c) v7.9 milestone (8 rows) — first milestone block since v5.3; all reproducible
        (Phase 123, D-01). NEGCAT-01/02 (Phase 120), OCH-01/02/03 (Phase 121),
        COLLIDE-01/02 (Phase 122), RECON-01 (Phase 123).
    (d) v7.11 milestone (11 rows) — all audit-only (Phase 131 RECON-03, D-04): validated by
        one-shot manual live runs, not by deterministic offline CI gates, which is why they
        carry artifact_link="" and a shared gap_rationale. See `_rows_v711()`. This path was
        present in the body from Phase 131 but absent from this docstring until 2026-08-29;
        its absence is what made the "first block since v7.9" claim below look true.
    (e) v8.18 milestone (23 rows, 21 reproducible + 2 audit-only) — first **v8.x** milestone block
        since v7.9 (Phase 4/D-05; the v7.11 block at (d) is the last non-v8.x addition): the
        discriminator is headline-history row 2's phrase "each backed by a deterministic offline
        gate", which v7.12, v7.13 and v8.0 did not satisfy but HARN-01/02/03 do. See
        `_rows_v818()` for the full per-row rationale.
    (f) v8.24 milestone (15 rows, 14 reproducible + 1 audit-only) — Phase 6/D-06/D-07: the
        milestone's CAP-*/PROV-*/GATE-*/VAL-* requirements, all Test-Network apparatus except
        VAL-04 (Methodology, audit-only — a docs record, not a re-runnable gate). See
        `_rows_v824()` for the full per-row rationale.

    The 'residual/' key prefix for non-milestone residuals is confirmed
    (Task 3 checkpoint, 82-02). See _RESIDUAL_KEY_PREFIX for the change point.
    """
    rows: list[MatrixRow] = []
    # --- Methodology capability ---
    rows.extend(_rows_methodology_agent())
    rows.extend(_rows_methodology_agent_cont())
    rows.extend(_rows_methodology_rigor())
    rows.extend(_rows_methodology_focused_stubs())
    # --- Test-Network capability ---
    rows.extend(_rows_testnet_ci_gates())
    rows.extend(_rows_testnet_routing_battery())
    rows.extend(_rows_testnet_routing_v38())
    rows.extend(_rows_testnet_routing_v39_plus())
    rows.extend(_rows_testnet_merged_battery())
    rows.extend(_rows_testnet_step0_harness())
    rows.extend(_rows_testnet_v52_v53())
    # --- Active tail (D-05 path b) ---
    rows.extend(_rows_active_tail())
    # --- v7.9 milestone (D-01 / Phase 123) ---
    rows.extend(_rows_v79())
    # --- v7.11 milestone (D-04 / Phase 131) — 11 audit-only rows ---
    rows.extend(_rows_v711())
    # --- v8.18 milestone (D-05 / Phase 4) — 21 reproducible + 2 audit-only ---
    rows.extend(_rows_v818())
    # --- v8.24 milestone (D-06 / Phase 6) — 14 reproducible + 1 audit-only ---
    rows.extend(_rows_v824())
    return rows


# ---------------------------------------------------------------------------
# Python version guard
# ---------------------------------------------------------------------------


def _require_python_version() -> None:
    if sys.version_info < (3, 12):
        sys.stderr.write(
            f"scripts/check-traceability.py requires Python >=3.12 "
            f"(running {sys.version_info.major}.{sys.version_info.minor}).\n"
        )
        sys.exit(2)


# ---------------------------------------------------------------------------
# Path-confinement guard (T-82-01; loosened in Phase 83 to allow docs/)
# ---------------------------------------------------------------------------

ALLOWED_OUTPUT_ROOTS: tuple[Path, ...] = (
    (REPO_ROOT / ".planning").resolve(),
    (REPO_ROOT / "docs").resolve(),
)


def _resolve_confined_output(path: Path) -> Path:
    """Resolve path and enforce T-82-01: must be under REPO_ROOT/.planning/ or docs/.

    Returns the resolved absolute path if confined.
    Writes a stderr message and calls sys.exit(2) if the path escapes.
    """
    resolved = path.resolve()
    confined = any(
        resolved == root or str(resolved).startswith(str(root) + "/")
        for root in ALLOWED_OUTPUT_ROOTS
    )
    if not confined:
        sys.stderr.write(
            f"check-traceability: --output path must be under .planning/ or docs/ "
            f"(got: {resolved})\n"
        )
        sys.exit(2)
    return resolved


# ---------------------------------------------------------------------------
# Artifact resolution (D-08 deep check)
# ---------------------------------------------------------------------------


def _resolve_artifact(artifact_link: str) -> list[str]:
    """Deep-resolve an artifact_link; return a list of issue descriptions.

    Resolution rules per RESEARCH.md §Pattern 3:
      - CLI whitelist entry (KNOWN_CLI_GATES) → membership check
      - catalog-row anchor (path#ROW-ID) → file exists + row ID in file text
      - rubric anchor (path#anchor) → file exists + heading found in file
      - plain file path → file exists

    Returns empty list if the artifact resolves correctly.
    Empty artifact_link string is not dispatched here (callers check tier first).
    """
    if not artifact_link:
        return []

    # CLI whitelist check (Pitfall 6: VAL-01/VAL-02 have no script file)
    if artifact_link in KNOWN_CLI_GATES:
        return []

    # Anchor-based resolution (catalog rows and rubric sections)
    if "#" in artifact_link:
        file_part, anchor = artifact_link.split("#", 1)
        file_path = REPO_ROOT / file_part
        if not file_path.exists():
            return [f"artifact file not found: {file_part!r}"]
        content = file_path.read_text(encoding="utf-8")

        if file_part.endswith(".py"):
            # For .py files: require the anchor to match a real top-level symbol.
            # Arm 1: def/class (functions incl. `async def`, classes; indented
            #        methods also matched).
            # Arm 2: module constant / annotated assignment at column 0.
            # This prevents a comment-only substring from falsely resolving.
            #
            # Known, accepted limitation (WR-02): this is a line-anchored regex,
            # NOT an AST walk (D-03 — AST was intentionally rejected as
            # over-engineered for a CI gate whose only live anchor is
            # `#self_test_boundary`). A symbol-like line sitting at column 0
            # inside a triple-quoted string or docstring can therefore
            # false-positive. The self-test proves comment-only rejection +
            # substring non-vacuity; it does not claim string-literal rejection.
            escaped = re.escape(anchor)
            # Arm 1 allows an optional `async ` prefix so `async def <anchor>`
            # resolves (WR-03 — a bare `(def|class)` alternation misses it
            # because the line begins with `async`, not `def`).
            _def_class_pat = re.compile(
                r"^\s*(?:async\s+def|def|class)\s+" + escaped + r"\b", re.MULTILINE
            )
            _const_pat = re.compile(
                r"^" + escaped + r"\s*[=:]", re.MULTILINE
            )
            if not (_def_class_pat.search(content) or _const_pat.search(content)):
                return [
                    f"anchor {anchor!r} is not a def/class/module-level symbol in {file_part!r}"
                ]
            return []

        # Non-.py files: catalog-row form (row ID like B-P12, S-P01, etc.) and
        # rubric anchors (heading slugs). Use plain substring membership
        # (RESEARCH.md §Parenthetical gotcha: avoid pipe-table split over content
        # with | alternation characters).
        if anchor not in content:
            return [
                f"anchor {anchor!r} not found in {file_part!r}"
            ]
        return []

    # Plain file path resolution
    file_path = REPO_ROOT / artifact_link
    if not file_path.exists():
        return [f"artifact file not found: {artifact_link!r}"]
    return []


# ---------------------------------------------------------------------------
# Consistency gate
# ---------------------------------------------------------------------------


def check_consistency(rows: list[MatrixRow]) -> list[str]:
    """Validate each row; return list of issue descriptions (empty == consistent).

    Per-row checks:
      - capability must be in VALID_CAPABILITIES (TRACE-01)
      - coverage_tier must be in VALID_TIERS (TRACE-03)
      - for reproducible AND scheduled rows: artifact_link must resolve via
        _resolve_artifact (WR-02/D-02); a dangling scheduled artifact FAILS check
        the same as a dangling reproducible artifact
      - audit-only and gap rows with no artifact link are valid states (D-06)
    """
    issues: list[str] = []
    for row in rows:
        if row.capability not in VALID_CAPABILITIES:
            issues.append(
                f"{row.key}: invalid capability {row.capability!r} "
                f"(must be one of {sorted(VALID_CAPABILITIES)!r})"
            )
        if row.coverage_tier not in VALID_TIERS:
            issues.append(
                f"{row.key}: invalid coverage_tier {row.coverage_tier!r} "
                f"(must be one of {sorted(VALID_TIERS)!r})"
            )
        if row.coverage_tier in ("reproducible", "scheduled"):
            link_issues = _resolve_artifact(row.artifact_link)
            for issue in link_issues:
                issues.append(f"{row.key}: {issue}")
    return issues


# ---------------------------------------------------------------------------
# Emitter: dual output from one row list (D-12 anti-drift)
# ---------------------------------------------------------------------------

# Severity matrix per D-14: coverage-tier × capability-undermined
# gap+Test-Network=CRITICAL, gap+Methodology=HIGH,
# audit-only+Test-Network=HIGH, audit-only+Methodology=MEDIUM
_SEVERITY_LABEL: dict[tuple[str, str], str] = {
    ("gap", "Test-Network"): "CRITICAL",
    ("gap", "Methodology"): "HIGH",
    ("audit-only", "Test-Network"): "HIGH",
    ("audit-only", "Methodology"): "MEDIUM",
}

# Human-curated per-item severity overrides for the 7 active-tail gap rows.
# Approved at Task 3 checkpoint (82-02 Plan, 2026-06-14); rationale in
# 82-RESEARCH.md §Gap Prioritization Model lines 719-724.
# These override the pure D-14 2×2 formula for the named bare_ids only;
# all other rows continue to use the _SEVERITY_LABEL 2×2 map.
_ACTIVE_TAIL_SEVERITY: dict[str, str] = {
    "RR-80-01": "CRITICAL",   # negative-control regression in step0-baseline
    # GEN-01 removed — now "reproducible" (committed live re-baseline; flip Phase 93 on v6.3 Phase 92, now tracks v6.4 Phase 95)
    # GEN-02 removed — now "reproducible" (runbook + wrapper script, Phase 89)
    "RR-79-01": "HIGH",       # live S-P routing unresolved
    # RR-114-01 supersedes RR-108-01 (Phase 114 v7.6 carry-forward, S-P02 inversion CARRIED 1/5)
    # Full chain: RR-79-02 -> RR-92-01 -> RR-95-01 -> RR-108-01 -> RR-114-01
    "RR-114-01": "HIGH",      # live S-P routing unresolved (carried v7.6)
    # RR-108-02 supersedes RR-95-02 (Phase 108 v7.4 carry-forward, S-P05 trade-off CARRIED 2/5)
    # Full chain: RR-79-03 -> RR-92-02 -> RR-95-02 -> RR-108-02 CLOSED
    # CLOSED at 4/5 ≥ min-pass at Phase 114 v7.6 re-baseline (ID retained, sentinel present)
    "RR-108-02": "HIGH",      # CLOSED at 4/5 v7.6 (ID retained as regression guard)
    "RR-77-08": "MEDIUM",     # ceiling warning, non-blocking
}

# Sort rank keyed on final label (CRITICAL first → MEDIUM last).
# Using label→rank keeps sort correct even when override changes the label.
_SEVERITY_RANK: dict[str, int] = {
    "CRITICAL": 0,
    "HIGH":     1,
    "MEDIUM":   2,
    "UNKNOWN":  99,
}


def _gap_severity(row: MatrixRow) -> str:
    """Return the effective severity label for an audit-only or gap row.

    Checks the human-curated _ACTIVE_TAIL_SEVERITY override FIRST (approved
    at Task 3 checkpoint, 82-02, for the 7 active-tail rows). Falls back to
    the D-14 2×2 _SEVERITY_LABEL map for all other rows.

    CRITICAL: gap + Test-Network (or override). Verification system unverified.
    HIGH:     gap + Methodology OR audit-only + Test-Network (or override).
    MEDIUM:   audit-only + Methodology (or override).
    """
    if row.bare_id in _ACTIVE_TAIL_SEVERITY:
        return _ACTIVE_TAIL_SEVERITY[row.bare_id]
    return _SEVERITY_LABEL.get((row.coverage_tier, row.capability), "UNKNOWN")


def _render_gap_findings(uncovered: list[MatrixRow]) -> list[str]:
    """Render the severity-ordered Gap Findings + Candidate Work List sections.

    Implements GAP-01 (named gap findings) + GAP-02 (prioritized carry-forward).
    Uncovered rows = audit-only + gap rows, sorted CRITICAL -> HIGH -> MEDIUM.
    Sort is by final label rank (_SEVERITY_RANK) so override labels sort correctly.
    """
    # Sort by final severity label rank (ascending rank = descending severity)
    sorted_rows = sorted(
        uncovered,
        key=lambda r: _SEVERITY_RANK.get(_gap_severity(r), 99),
    )
    lines: list[str] = []
    lines.append("## Gap Findings (GAP-01)")
    lines.append("")
    lines.append(
        "> **D-15 honesty note:** A non-zero audit-only+gap count is the "
        "expected success state — an honest 'N requirements are uncovered' "
        "finding is the goal, not a zero-gap matrix."
    )
    lines.append("")
    current_sev = ""
    for r in sorted_rows:
        sev = _gap_severity(r)
        if sev != current_sev:
            lines.append(f"### {sev}")
            lines.append("")
            current_sev = sev
        lines.append(
            f"- **{r.bare_id}** ({r.key}) [{r.coverage_tier}] "
            f"[{r.capability}]: {r.gap_rationale}"
        )
    lines.append("")
    lines.append("## Future-Milestone Candidate Work List (GAP-02)")
    lines.append("")
    lines.append(
        "The following items are carried forward as candidate work for a "
        "future milestone. No new confirming tests are written this phase."
    )
    lines.append("")
    for r in sorted_rows:
        sev = _gap_severity(r)
        lines.append(
            f"- [{sev}] **{r.bare_id}** ({r.key}): Add a confirming "
            f"{r.capability} gate/test. Rationale: {r.gap_rationale[:80]}"
            f"{'...' if len(r.gap_rationale) > 80 else ''}"
        )
    lines.append("")
    return lines


def render_matrix_markdown(rows: list[MatrixRow]) -> str:
    """Render the matrix as a Markdown string (list[str] → join pattern).

    Coverage Distribution folds scheduled rows into the reproducible bucket
    (D-01/WR-01): the reproducible bullet shows len(reproducible)+len(scheduled)
    with an `(incl. N scheduled)` annotation when N > 0. No standalone scheduled
    bullet is emitted. uncovered = audit_only + gap only (scheduled is not
    uncovered and must not enter _render_gap_findings).
    """
    reproducible = [r for r in rows if r.coverage_tier == "reproducible"]
    audit_only = [r for r in rows if r.coverage_tier == "audit-only"]
    gap = [r for r in rows if r.coverage_tier == "gap"]
    scheduled = [r for r in rows if r.coverage_tier == "scheduled"]
    uncovered = audit_only + gap

    lines: list[str] = []
    lines.append("<!-- GENERATED — DO NOT EDIT -->")
    lines.append("<!-- Source: scripts/check-traceability.py build_matrix_rows() -->")
    lines.append(
        "<!-- Regenerate: python3 scripts/check-traceability.py emit"
        " --md-output docs/requirements-matrix.md"
        " --json-output docs/data/matrix.json -->"
    )
    lines.append("")
    lines.append("# Requirements Traceability Matrix")
    lines.append("")
    lines.append(
        "> Generated by: "
        "`python3 scripts/check-traceability.py emit"
        " --md-output docs/requirements-matrix.md ...`"
    )
    lines.append("")
    lines.append("## Coverage Distribution")
    _folded_reproducible = len(reproducible) + len(scheduled)
    if len(scheduled) > 0:
        lines.append(
            f"- reproducible: {_folded_reproducible} (incl. {len(scheduled)} scheduled)"
        )
    else:
        lines.append(f"- reproducible: {_folded_reproducible}")
    lines.append(f"- audit-only: {len(audit_only)}")
    lines.append(f"- gap: {len(gap)}")
    lines.append(f"- total: {len(rows)}")
    lines.append("")
    lines.append("## Matrix Table")
    lines.append(
        "| Key | Bare ID | Capability | Deliverable | Tier | "
        "Artifact | Gap Rationale |"
    )
    lines.append(
        "|-----|---------|------------|-------------|------|----------|---------------|"
    )
    for r in rows:
        lines.append(
            f"| {r.key} | {r.bare_id} | {r.capability} | "
            f"{r.deliverable_path} | {r.coverage_tier} | "
            f"{r.artifact_link} | {r.gap_rationale} |"
        )
    lines.append("")
    if uncovered:
        lines.extend(_render_gap_findings(uncovered))
    return "\n".join(lines)


def emit_matrix(
    rows: list[MatrixRow],
    md_path: Path,
    json_path: Path,
) -> None:
    """Write MATRIX.md + matrix.json from one row list (D-12 single repr).

    Both paths must pass _resolve_confined_output() first.
    Writes JSON sidecar first, then Markdown.
    """
    md_resolved = _resolve_confined_output(md_path)
    json_resolved = _resolve_confined_output(json_path)

    md_resolved.parent.mkdir(parents=True, exist_ok=True)
    json_resolved.parent.mkdir(parents=True, exist_ok=True)

    json_resolved.write_text(
        json.dumps([asdict(r) for r in rows], indent=2),
        encoding="utf-8",
    )
    md_resolved.write_text(
        render_matrix_markdown(rows),
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# load_rows: JSON sidecar → list[MatrixRow]
# ---------------------------------------------------------------------------


def load_rows(json_path: Path) -> list[MatrixRow]:
    """Load matrix.json → list[MatrixRow] via json.loads + dataclass constructor.

    The constructor catches missing fields (Don't-Hand-Roll: per RESEARCH.md).
    """
    raw = json.loads(json_path.read_text(encoding="utf-8"))
    return [MatrixRow(**item) for item in raw]


# ---------------------------------------------------------------------------
# Self-test fixtures
# ---------------------------------------------------------------------------


def _self_test_valid_rows_fixtures(wrong_results: list[str]) -> None:
    """Fixtures 1, 5, 6: valid rows that must pass check_consistency."""
    # Fixture (1): valid reproducible row with a real repo file
    row1 = MatrixRow(
        key="v5.0/STEP0-F1",
        bare_id="STEP0-F1",
        milestone="v5.0",
        capability="Test-Network",
        deliverable_path="scripts/check-step0-emulator.py",
        coverage_tier="reproducible",
        artifact_link="scripts/check-step0-emulator.py",
        gap_rationale="",
    )
    issues1 = check_consistency([row1])
    if issues1:
        print(f"check-traceability --self-test: fixture(1) FAIL — {issues1!r}")
        wrong_results.append("fixture(1) valid reproducible row flagged incorrectly")
    else:
        print("check-traceability --self-test: fixture(1) valid reproducible row PASS")

    # Fixture (5): audit-only row with no artifact link — valid state (D-06)
    row5 = MatrixRow(
        key="v3.1/ROUTE-02",
        bare_id="ROUTE-02",
        milestone="v3.1",
        capability="Test-Network",
        deliverable_path="scripts/check-routing.py",
        coverage_tier="audit-only",
        artifact_link="",
        gap_rationale="Validated by v3.1 milestone audit; no re-runnable gate",
    )
    issues5 = check_consistency([row5])
    if issues5:
        print(f"check-traceability --self-test: fixture(5) FAIL — {issues5!r}")
        wrong_results.append(
            "fixture(5) audit-only row with no artifact flagged (should be valid)"
        )
    else:
        print("check-traceability --self-test: fixture(5) audit-only no-artifact PASS")

    # Fixture (6): gap row with rationale, no artifact link — valid state (D-06)
    # Generic gap-row STRUCTURAL test; coverage_tier="gap" is still a valid tier.
    # NOT tied to the live GEN-01 state (GEN-01 is now "scheduled" after Phase 88).
    row6 = MatrixRow(
        key="v5.3/GEN-01",
        bare_id="GEN-01",
        milestone="v5.3",
        capability="Test-Network",
        deliverable_path="active-tail",
        coverage_tier="gap",
        artifact_link="",
        gap_rationale="Full Step 0 classifier rearchitecture; perpetually deferred",
    )
    issues6 = check_consistency([row6])
    if issues6:
        print(f"check-traceability --self-test: fixture(6) FAIL — {issues6!r}")
        wrong_results.append(
            "fixture(6) gap row with rationale flagged (should be valid)"
        )
    else:
        print("check-traceability --self-test: fixture(6) gap row with rationale PASS")

    # Fixture (9): scheduled row with resolvable artifact link — valid state (D-02/Phase 88)
    # Proves that coverage_tier="scheduled" is accepted by check_consistency() AND
    # that deep-resolve passes for a scheduled row with a real artifact (WR-02/Phase 90).
    # check_consistency() now deep-resolves artifact links for both "reproducible" AND
    # "scheduled" rows. Fixture passes because docs/gen-01-rearch-milestone.md exists.
    # The GEN-01-SCHEDULED sentinel (below) also verifies the file exists.
    row9 = MatrixRow(
        key="v5.3/GEN-01",
        bare_id="GEN-01",
        milestone="v5.3",
        capability="Test-Network",
        deliverable_path="active-tail",
        coverage_tier="scheduled",
        artifact_link="docs/gen-01-rearch-milestone.md",
        gap_rationale="Committed future milestone GEN-01-REARCH",
    )
    issues9 = check_consistency([row9])
    if issues9:
        print(f"check-traceability --self-test: fixture(9) FAIL — {issues9!r}")
        wrong_results.append("fixture(9) scheduled row flagged (should be valid)")
    else:
        print("check-traceability --self-test: fixture(9) scheduled row with artifact PASS")

    # ---------------------------------------------------------------------------
    # DISTRIBUTION-FOLD fixture (10) — WR-01 renderer fold lock (TRACE-03)
    # Calls render_matrix_markdown on a tiny SYNTHETIC row set (hardcoded, NOT
    # live build_matrix_rows) so the fixture can never go vacuous if live counts
    # shift. Asserts the three WR-01 regression conditions:
    #   (a) Sum guard: Coverage Distribution bullets sum to len(rows).
    #   (b) Annotation guard: "(incl. 1 scheduled)" appears in the rendered output.
    #   (c) Positive counter-check (non-vacuous): folded reproducible count
    #       strictly > bare reproducible count (mirrors GEN-01-SCHEDULED
    #       _gen01_was_gap and RR-77-08 composer_hits == CEILING-1 idioms).
    # Honesty-not-score: asserts renderer math, not any live pass-rate.
    # Any revert of the scheduled-fold in render_matrix_markdown fails this fixture.
    # ---------------------------------------------------------------------------
    _fold_repro1 = MatrixRow(
        key="fixture/FOLD-REPRO-01", bare_id="FOLD-REPRO-01", milestone="fixture",
        capability="Test-Network", deliverable_path="active-tail",
        coverage_tier="reproducible", artifact_link="", gap_rationale="",
    )
    _fold_repro2 = MatrixRow(
        key="fixture/FOLD-REPRO-02", bare_id="FOLD-REPRO-02", milestone="fixture",
        capability="Test-Network", deliverable_path="active-tail",
        coverage_tier="reproducible", artifact_link="", gap_rationale="",
    )
    _fold_sched1 = MatrixRow(
        key="fixture/FOLD-SCHED-01", bare_id="FOLD-SCHED-01", milestone="fixture",
        capability="Test-Network", deliverable_path="active-tail",
        coverage_tier="scheduled", artifact_link="",
        gap_rationale="Synthetic scheduled row for DISTRIBUTION-FOLD fixture",
    )
    _fold_rows = [_fold_repro1, _fold_repro2, _fold_sched1]  # 2 repro + 1 scheduled
    _fold_bare_reproducible = 2   # bare count (before fold)
    _fold_rendered = render_matrix_markdown(_fold_rows)
    _fold_dist = _fold_rendered.split("## Coverage Distribution")[1].split("## Matrix Table")[0]

    # (a) Sum guard: the total bullet must equal len(rows); reproducible+audit+gap
    # must equal len(rows) (the scheduled rows are folded into reproducible).
    # Parse the total bullet and the three tier bullets separately.
    import re as _re
    _fold_total_match = _re.search(r"^- total: (\d+)", _fold_dist, _re.MULTILINE)
    _fold_total_val = int(_fold_total_match.group(1)) if _fold_total_match else -1
    _fold_sum_ok = _fold_total_val == len(_fold_rows)
    if not _fold_sum_ok:
        print(
            f"check-traceability --self-test: fixture(10) DISTRIBUTION-FOLD FAIL "
            f"— total bullet is {_fold_total_val}, expected {len(_fold_rows)} "
            f"(scheduled row dropped, sum is wrong)"
        )
        wrong_results.append(
            "DISTRIBUTION-FOLD: total bullet does not equal len(rows) (scheduled row dropped)"
        )
    else:
        print(
            "check-traceability --self-test: fixture(10) DISTRIBUTION-FOLD sum guard PASS "
            f"(total={_fold_total_val} == {len(_fold_rows)})"
        )

    # (b) Annotation guard: "(incl. 1 scheduled)" must appear in the rendered output
    _fold_annotation_ok = "(incl. 1 scheduled)" in _fold_dist
    if not _fold_annotation_ok:
        print(
            "check-traceability --self-test: fixture(10) DISTRIBUTION-FOLD FAIL "
            "— annotation '(incl. 1 scheduled)' not found in Coverage Distribution"
        )
        wrong_results.append("DISTRIBUTION-FOLD: (incl. 1 scheduled) annotation missing")
    else:
        print(
            "check-traceability --self-test: fixture(10) DISTRIBUTION-FOLD annotation PASS"
        )

    # (c) Positive counter-check: folded reproducible count (3) > bare count (2)
    # Extract the reproducible bullet value from the rendered distribution
    _fold_repro_match = _re.search(r"^- reproducible: (\d+)", _fold_dist, _re.MULTILINE)
    _fold_folded_count = int(_fold_repro_match.group(1)) if _fold_repro_match else -1
    _fold_noop = _fold_folded_count <= _fold_bare_reproducible
    if _fold_noop or _fold_folded_count < 0:
        print(
            f"check-traceability --self-test: fixture(10) DISTRIBUTION-FOLD FAIL "
            f"— folded reproducible count ({_fold_folded_count}) not strictly > "
            f"bare reproducible count ({_fold_bare_reproducible}); fold is a no-op or missing"
        )
        wrong_results.append(
            "DISTRIBUTION-FOLD: folded count not strictly > bare reproducible count"
        )
    else:
        print(
            f"check-traceability --self-test: fixture(10) DISTRIBUTION-FOLD positive "
            f"counter-check PASS ({_fold_folded_count} > {_fold_bare_reproducible})"
        )

    # ---------------------------------------------------------------------------
    # GEN-01-REPRODUCIBLE named sentinel (D-09 / Phase 93)
    # Repurposed from GEN-01-SCHEDULED (Phase 88) — GEN-01 is now 'reproducible'
    # (Phase 93 flip, D-08) because the Step 0 classifier capability is reproducibly
    # measured by a committed live re-baseline. The flip was earned in Phase 93 on
    # tests/step0-baseline-v6.3.md (Phase 92); the artifact_link now tracks the current
    # authoritative re-baseline tests/step0-baseline-v7.13.md (Phase 137, residual-delta).
    # Artifact bump history: v7.6 (Phase 114) → v7.8 (Phase 119) → v7.11 (Phase 131 RECON-03, D-05)
    # → v7.13 (Phase 138 Plan 03, D-05). tests/step0-baseline-v7.8.md remains the canonical
    # full 8-technique baseline; v7.13 is a 3-row residual-delta re-measure.
    # The flip is earned by the committed baseline, not a passing score
    # (Phase 129 v7.11: BATTERY: FAIL P 4/8 — reproducible = measured, not passing, D-01).
    # Asserts:
    #   (a) GEN-01's tier is "reproducible" (not "scheduled", not "gap")
    #   (b) GEN-01's artifact_link is the committed v7.13 baseline (deep-resolved)
    #   (c) Exactly-one GEN-01 row drift guard
    #   (d) Not-scheduled counter-check (transition non-vacuous)
    # Mirrors the Phase 84/85 RR-80-01 idiom: hardcoded named assertion +
    # positive counter-check + drift guard. No live claude session required.
    # No gitignored-file dependency (.planning/ROADMAP.md removed — ABSENT in CI).
    # Honesty-not-score (D-01): asserts the documented reproducible state, not a
    # live pass-rate. Any future revert of the tier, deletion of the GEN-01 row,
    # or removal of the v7.13 baseline file fails CI.
    # ---------------------------------------------------------------------------

    # (1) Live-sourced tier read — call _rows_active_tail() directly (Pitfall 4:
    # do NOT hardcode a MatrixRow literal; the function is the source of truth).
    _gen01_rows = [r for r in _rows_active_tail() if r.bare_id == "GEN-01"]
    _gen01_count = len(_gen01_rows)
    _gen01_tier = _gen01_rows[0].coverage_tier if _gen01_rows else "MISSING"
    _gen01_artifact = _gen01_rows[0].artifact_link if _gen01_rows else ""

    # (c) Drift guard: GEN-01 must exist exactly once (not deleted, not duplicated).
    if _gen01_count != 1:
        print(
            f"  GEN-01-REPRODUCIBLE FAIL: expected exactly 1 GEN-01 row in "
            f"_rows_active_tail(), got {_gen01_count} — drift guard failed."
        )
        wrong_results.append("GEN-01-REPRODUCIBLE: row count drift")

    # (d) Not-scheduled counter-check: proves the scheduled→reproducible transition
    # is non-vacuous. _gen01_was_scheduled would have been True pre-Phase 93; asserting
    # NOT scheduled is meaningful (mirrors the old _gen01_was_gap idiom from Phase 88).
    _gen01_was_scheduled = _gen01_tier == "scheduled"
    _gen01_is_reproducible = _gen01_tier == "reproducible"

    if _gen01_is_reproducible and not _gen01_was_scheduled:
        print(
            f"  GEN-01-REPRODUCIBLE PASS: GEN-01 tier={_gen01_tier!r} "
            f"(not 'scheduled', not 'gap'); artifact_link={_gen01_artifact!r}"
        )
    else:
        print(
            f"  GEN-01-REPRODUCIBLE FAIL: GEN-01 tier={_gen01_tier!r} "
            f"(expected 'reproducible', not 'scheduled' or 'gap'). "
            f"Phase 93 flip not applied or tier reverted. "
            f"See D-08 in 93-02-PLAN.md."
        )
        wrong_results.append("GEN-01-REPRODUCIBLE: tier not 'reproducible'")

    # (b) Artifact deep-resolve (D-09): GEN-01's artifact_link must be the committed
    # v7.13 baseline (Phase 137 residual-delta — the latest authoritative re-baseline).
    # Deep-resolve via _resolve_artifact (git-tracked, present in CI).
    # Bump history: v7.6 (Phase 114) → v7.8 (Phase 119) → v7.11 (Phase 131 RECON-03, Plan 03, D-05)
    # → v7.13 (Phase 138 Plan 03, D-05). tests/step0-baseline-v7.8.md remains canonical full baseline.
    _gen01_expected_artifact = "tests/step0-baseline-v7.13.md"
    if _gen01_artifact != _gen01_expected_artifact:
        print(
            f"  GEN-01-REPRODUCIBLE FAIL: artifact_link={_gen01_artifact!r} "
            f"(expected {_gen01_expected_artifact!r})."
        )
        wrong_results.append("GEN-01-REPRODUCIBLE: artifact_link not v7.13 baseline")
    else:
        _gen01_resolve_issues = _resolve_artifact(_gen01_artifact)
        # Belt-and-suspenders: explicit path existence check
        _gen01_baseline_path = REPO_ROOT / "tests" / "step0-baseline-v7.13.md"
        if _gen01_resolve_issues or not _gen01_baseline_path.exists():
            print(
                f"  GEN-01-REPRODUCIBLE FAIL: artifact deep-resolve failed for "
                f"{_gen01_artifact!r}: {_gen01_resolve_issues}; "
                f"file exists={_gen01_baseline_path.exists()}"
            )
            wrong_results.append("GEN-01-REPRODUCIBLE: v7.13 baseline not resolvable")
        else:
            print(
                f"  GEN-01-REPRODUCIBLE PASS: artifact_link={_gen01_artifact!r} "
                f"deep-resolves OK (tests/step0-baseline-v7.13.md exists, git-tracked)."
            )

    # ---------------------------------------------------------------------------
    # GEN-02-RUNBOOK named sentinel (D-03 / Phase 89)
    # Asserts (a) GEN-02's tier is "reproducible" (not "gap") in _rows_active_tail()
    # and (b) dual artifact-existence: docs/live-monitoring-runbook.md exists AND
    # scripts/run-live-monitoring.sh exists.
    # Mirrors the Phase 88 GEN-01-SCHEDULED idiom: live _rows_active_tail() read +
    # positive counter-check + drift guard + existence checks. No live claude session.
    # Honesty-not-score (D-06): asserts the documented reproducible confirming state,
    # not a live pass-rate. Any future revert of the tier, deletion of the GEN-02 row,
    # or removal of the runbook/wrapper fails CI.
    # ---------------------------------------------------------------------------

    # (1) Live-sourced tier read — call _rows_active_tail() directly (Pitfall 1:
    # do NOT hardcode a MatrixRow literal; the function is the source of truth).
    _gen02_rows = [r for r in _rows_active_tail() if r.bare_id == "GEN-02"]
    _gen02_count = len(_gen02_rows)
    _gen02_tier = _gen02_rows[0].coverage_tier if _gen02_rows else "MISSING"
    _gen02_artifact = _gen02_rows[0].artifact_link if _gen02_rows else ""

    # (3) Drift guard: GEN-02 must exist exactly once (not deleted, not duplicated).
    if _gen02_count != 1:
        print(
            f"  GEN-02-RUNBOOK FAIL: expected exactly 1 GEN-02 row in "
            f"_rows_active_tail(), got {_gen02_count} — drift guard failed."
        )
        wrong_results.append("GEN-02-RUNBOOK: row count drift")

    # (2) Positive counter-check: _gen02_was_gap proves the transition is non-vacuous.
    # _gen02_was_gap would have been True pre-Phase 89; asserting NOT gap is meaningful.
    _gen02_was_gap = _gen02_tier == "gap"
    _gen02_is_reproducible = _gen02_tier == "reproducible"

    if _gen02_is_reproducible and not _gen02_was_gap:
        print(
            f"  GEN-02-RUNBOOK PASS: GEN-02 tier={_gen02_tier!r} (not 'gap'); "
            f"artifact_link={_gen02_artifact!r}"
        )
    else:
        print(
            f"  GEN-02-RUNBOOK FAIL: GEN-02 tier={_gen02_tier!r} "
            f"(expected 'reproducible', not 'gap'). "
            f"Runbook + wrapper not established or tier reverted. "
            f"See docs/live-monitoring-runbook.md."
        )
        wrong_results.append("GEN-02-RUNBOOK: tier not 'reproducible'")

    # (b) Dual artifact-existence check (D-03): runbook AND wrapper must both exist.
    _gen02_runbook_path = REPO_ROOT / "docs" / "live-monitoring-runbook.md"
    if _gen02_runbook_path.exists():
        print("  GEN-02-RUNBOOK PASS: docs/live-monitoring-runbook.md exists.")
    else:
        print(
            "  GEN-02-RUNBOOK FAIL: docs/live-monitoring-runbook.md does not exist "
            "— D-03 dual-artifact check (part 1) not satisfied."
        )
        wrong_results.append("GEN-02-RUNBOOK: docs/live-monitoring-runbook.md missing")

    _gen02_wrapper_path = REPO_ROOT / "scripts" / "run-live-monitoring.sh"
    if _gen02_wrapper_path.exists():
        print("  GEN-02-RUNBOOK PASS: scripts/run-live-monitoring.sh exists.")
    else:
        print(
            "  GEN-02-RUNBOOK FAIL: scripts/run-live-monitoring.sh does not exist "
            "— D-03 dual-artifact check (part 2) not satisfied."
        )
        wrong_results.append("GEN-02-RUNBOOK: scripts/run-live-monitoring.sh missing")


def _self_test_dangling_fixtures(wrong_results: list[str]) -> None:
    """Fixtures 2, 3, 4: dangling references that must flag non-zero."""
    # Fixture (2): reproducible row with dangling file path
    row2 = MatrixRow(
        key="test/DANGLE-01",
        bare_id="DANGLE-01",
        milestone="test",
        capability="Test-Network",
        deliverable_path="scripts/check-routing-battery.py",
        coverage_tier="reproducible",
        artifact_link="scripts/nonexistent-check-99.py",
        gap_rationale="",
    )
    issues2 = check_consistency([row2])
    if not issues2:
        print("check-traceability --self-test: fixture(2) FAIL — dangling path not detected")
        wrong_results.append(
            "fixture(2) dangling file path not flagged (nonexistent-check-99.py)"
        )
    else:
        print("check-traceability --self-test: fixture(2) dangling file path detected PASS")

    # Fixture (3): reproducible row with catalog row not in catalog
    row3 = MatrixRow(
        key="test/DANGLE-02",
        bare_id="DANGLE-02",
        milestone="test",
        capability="Test-Network",
        deliverable_path="scripts/check-routing-battery.py",
        coverage_tier="reproducible",
        artifact_link="tests/routing-battery-catalog.md#B-NONEXISTENT",
        gap_rationale="",
    )
    issues3 = check_consistency([row3])
    if not issues3:
        print("check-traceability --self-test: fixture(3) FAIL — dangling catalog row not detected")
        wrong_results.append(
            "fixture(3) dangling catalog row not flagged (B-NONEXISTENT)"
        )
    else:
        print(
            "check-traceability --self-test: fixture(3) dangling catalog row detected PASS"
        )

    # Fixture (4): reproducible row with missing rubric anchor
    row4 = MatrixRow(
        key="test/DANGLE-03",
        bare_id="DANGLE-03",
        milestone="test",
        capability="Methodology",
        deliverable_path="shared/spine/references/validation-rubric.md",
        coverage_tier="reproducible",
        artifact_link=(
            "shared/spine/references/validation-rubric.md"
            "#criterion-99-nonexistent"
        ),
        gap_rationale="",
    )
    issues4 = check_consistency([row4])
    if not issues4:
        print("check-traceability --self-test: fixture(4) FAIL — missing rubric anchor not detected")
        wrong_results.append(
            "fixture(4) missing rubric anchor not flagged (criterion-99-nonexistent)"
        )
    else:
        print(
            "check-traceability --self-test: fixture(4) missing rubric anchor detected PASS"
        )


def _self_test_schema_fixtures(wrong_results: list[str]) -> None:
    """Fixtures 7, 8: schema violations (missing capability or coverage_tier)."""
    # Fixture (7): row with empty capability
    row7 = MatrixRow(
        key="test/SCHEMA-01",
        bare_id="SCHEMA-01",
        milestone="test",
        capability="",
        deliverable_path="scripts/check-routing-battery.py",
        coverage_tier="audit-only",
        artifact_link="",
        gap_rationale="no capability assigned",
    )
    issues7 = check_consistency([row7])
    if not issues7:
        print("check-traceability --self-test: fixture(7) FAIL — missing capability not detected")
        wrong_results.append("fixture(7) empty capability not flagged")
    else:
        print("check-traceability --self-test: fixture(7) missing capability detected PASS")

    # Fixture (8): row with empty coverage_tier
    row8 = MatrixRow(
        key="test/SCHEMA-02",
        bare_id="SCHEMA-02",
        milestone="test",
        capability="Test-Network",
        deliverable_path="scripts/check-routing-battery.py",
        coverage_tier="",
        artifact_link="",
        gap_rationale="no tier assigned",
    )
    issues8 = check_consistency([row8])
    if not issues8:
        print("check-traceability --self-test: fixture(8) FAIL — missing coverage_tier not detected")
        wrong_results.append("fixture(8) empty coverage_tier not flagged")
    else:
        print("check-traceability --self-test: fixture(8) missing coverage_tier detected PASS")


def _self_test_pyanchor_resolver(wrong_results: list[str]) -> None:
    """pyanchor teeth: 3 positive controls + 1 comment-only negative control + non-vacuity check.

    Proves the extension-gated .py#anchor resolver is non-vacuous:
      (a) def-arm positive: scripts/_battery_core.py#self_test_boundary resolves (real def).
      (b) constant-arm positive: scripts/_battery_core.py#MIN_HEADER_HITS resolves (module const).
      (c) comment-only negative control: a .py file whose content mentions a token ONLY
          in a comment is rejected by the stricter resolver; the substring non-vacuity
          counter-check proves the OLD loose resolver would have falsely passed it
          (the name IS a substring).
      (d) async-def positive control (WR-03): `async def <anchor>` must resolve — guards
          the optional `async ` prefix in the def-arm against regression.

    Scope note (WR-02): these controls prove comment-only rejection + substring
    non-vacuity + async-def acceptance. They deliberately do NOT assert
    string-literal rejection, because the line-anchored regex (D-03, not AST)
    genuinely cannot reject a symbol-like line inside a docstring/string — that is
    a known, accepted limitation, not a defect this self-test claims to cover.
    """
    # (a) Positive control — def-arm: live OCH-03 anchor must still resolve.
    issues_a = _resolve_artifact("scripts/_battery_core.py#self_test_boundary")
    if issues_a:
        print(
            f"  PYANCHOR FAIL (a): def-arm regressed — "
            f"self_test_boundary not resolved: {issues_a}"
        )
        wrong_results.append(
            "PYANCHOR (a): scripts/_battery_core.py#self_test_boundary def-arm regressed"
        )
    else:
        print(
            "  PYANCHOR PASS (a): scripts/_battery_core.py#self_test_boundary def-arm resolves OK"
        )

    # (b) Positive control — constant-arm: MIN_HEADER_HITS is a module-level constant.
    issues_b = _resolve_artifact("scripts/_battery_core.py#MIN_HEADER_HITS")
    if issues_b:
        print(
            f"  PYANCHOR FAIL (b): constant-arm broken — "
            f"MIN_HEADER_HITS not resolved: {issues_b}"
        )
        wrong_results.append(
            "PYANCHOR (b): scripts/_battery_core.py#MIN_HEADER_HITS constant-arm broken"
        )
    else:
        print(
            "  PYANCHOR PASS (b): scripts/_battery_core.py#MIN_HEADER_HITS constant-arm resolves OK"
        )

    # (c) Negative control + substring non-vacuity counter-check.
    # Write a .py file with the token ONLY in a comment — no def/class/module-const.
    with tempfile.TemporaryDirectory() as _tmpdir:
        _fake_py = Path(_tmpdir) / "fake.py"
        _fake_py.write_text(
            "# comment_only_symbol mentioned here\nx = 1\n", encoding="utf-8"
        )
        _fake_content = _fake_py.read_text(encoding="utf-8")

        # Counter-check: the name IS a plain substring — proves the old loose resolver
        # would have falsely passed it, so the fix is non-vacuous.
        if "comment_only_symbol" not in _fake_content:
            print(
                "  PYANCHOR FAIL (c-counter): fixture not a substring — non-vacuity check invalid"
            )
            wrong_results.append(
                "PYANCHOR (c-counter): comment_only_symbol not a substring of fake.py"
            )
        else:
            print(
                "  PYANCHOR PASS (c-counter): comment_only_symbol IS a substring "
                "(old loose resolver would have falsely passed — fix is non-vacuous)"
            )

        # Negative control: the stricter resolver must REJECT this comment-only anchor.
        # The "#" form drives anchor resolution; pathlib absolute-path joining keeps the
        # absolute path (REPO_ROOT / absolute_path == absolute_path).
        issues_c = _resolve_artifact(f"{_fake_py}#comment_only_symbol")
        if not issues_c:
            print(
                "  PYANCHOR FAIL (c): stricter resolver did not reject comment-only anchor"
            )
            wrong_results.append(
                "PYANCHOR (c): comment_only_symbol in comment not rejected by .py resolver"
            )
        else:
            print(
                f"  PYANCHOR PASS (c): comment-only anchor correctly rejected: {issues_c}"
            )

    # (d) Positive control — async-def arm (WR-03): `async def <anchor>` must resolve.
    # Gives the optional `async ` prefix teeth — a bare `(def|class)` alternation
    # would FALSE-NEGATIVE here because the line begins with `async`, not `def`.
    with tempfile.TemporaryDirectory() as _tmpdir_d:
        _async_py = Path(_tmpdir_d) / "fake_async.py"
        _async_py.write_text(
            "async def some_async_anchor():\n    return 1\n", encoding="utf-8"
        )
        issues_d = _resolve_artifact(f"{_async_py}#some_async_anchor")
        if issues_d:
            print(
                f"  PYANCHOR FAIL (d): async-def arm did not resolve "
                f"`async def some_async_anchor`: {issues_d}"
            )
            wrong_results.append(
                "PYANCHOR (d): async def anchor not resolved by .py resolver (WR-03 regression)"
            )
        else:
            print(
                "  PYANCHOR PASS (d): async-def anchor `some_async_anchor` resolves OK"
            )


def _self_test_v79_rows_sentinel(wrong_results: list[str]) -> None:
    """V79-ROWS named sentinel (D-01 / Phase 123).

    Asserts the 8 v7.9 milestone rows registered in _rows_v79():
      (a) Exactly 8 rows (drift guard — not deleted, not duplicated).
      (b) bare_id set equals the canonical 8 IDs.
      (c) Every row's coverage_tier == "reproducible" (D-02: no "scheduled" rows).
      (d) Every artifact_link deep-resolves via _resolve_artifact (zero issues).
      (e) Positive counter-check: RECON-01 is present and reproducible, proving
          the assertion is non-vacuous (mirrors GEN-01-REPRODUCIBLE idiom).
      (f) milestone/key lock: every row has milestone == "v7.9" AND a key prefixed
          "v7.9/" (attribution guard — a mis-attributed row passes (a)-(e) silently).
      (g) capability lock: every row's capability is in VALID_CAPABILITIES (the same
          TRACE-01 whitelist check_consistency enforces; not re-run by --self-test).

    Called from _rows_v79() live — never hardcodes a MatrixRow literal (Pitfall 4).
    Honesty-not-score (D-01): asserts the documented reproducible registration,
    not a live pass-rate. Any deletion, tier revert, or dangling artifact_link fails CI.
    """
    # (a) Drift guard: read live, assert exactly 8 rows.
    _v79_rows = _rows_v79()
    _v79_count = len(_v79_rows)
    _EXPECTED_V79_IDS = {
        "NEGCAT-01", "NEGCAT-02", "OCH-01", "OCH-02", "OCH-03",
        "COLLIDE-01", "COLLIDE-02", "RECON-01",
    }
    if _v79_count != 8:
        print(
            f"  V79-ROWS FAIL: expected exactly 8 rows in _rows_v79(), "
            f"got {_v79_count} — drift guard failed."
        )
        wrong_results.append("V79-ROWS: row count drift (expected 8)")

    # (b) bare_id set assertion.
    _v79_ids = {r.bare_id for r in _v79_rows}
    if _v79_ids != _EXPECTED_V79_IDS:
        _missing = _EXPECTED_V79_IDS - _v79_ids
        _extra = _v79_ids - _EXPECTED_V79_IDS
        print(
            f"  V79-ROWS FAIL: bare_id set mismatch — "
            f"missing={sorted(_missing)!r}, extra={sorted(_extra)!r}"
        )
        wrong_results.append("V79-ROWS: bare_id set mismatch")
    else:
        print(f"  V79-ROWS PASS: bare_id set = {sorted(_v79_ids)!r}")

    # (c) Every row must be reproducible (D-02 prohibition on "scheduled" rows).
    _non_repro = [r for r in _v79_rows if r.coverage_tier != "reproducible"]
    if _non_repro:
        print(
            f"  V79-ROWS FAIL: {len(_non_repro)} row(s) are not 'reproducible': "
            f"{[r.bare_id for r in _non_repro]!r}"
        )
        wrong_results.append("V79-ROWS: non-reproducible row(s) found")
    else:
        print(f"  V79-ROWS PASS: all {_v79_count} rows are coverage_tier='reproducible'")

    # (d) Deep-resolve every artifact_link; assert zero issues.
    _link_issues: list[str] = []
    for _row in _v79_rows:
        for _issue in _resolve_artifact(_row.artifact_link):
            _link_issues.append(f"{_row.bare_id}: {_issue}")
    if _link_issues:
        for _issue in _link_issues:
            print(f"  V79-ROWS FAIL: artifact_link issue — {_issue}")
        wrong_results.append(f"V79-ROWS: {len(_link_issues)} artifact_link issue(s)")
    else:
        print(f"  V79-ROWS PASS: all {_v79_count} artifact_links deep-resolve OK")

    # (e) Positive counter-check: RECON-01 is present and reproducible.
    _recon01_rows = [r for r in _v79_rows if r.bare_id == "RECON-01"]
    _recon01_present = len(_recon01_rows) == 1
    _recon01_repro = _recon01_rows[0].coverage_tier == "reproducible" if _recon01_rows else False
    if _recon01_present and _recon01_repro:
        print(
            f"  V79-ROWS PASS: RECON-01 present and reproducible "
            f"(artifact_link={_recon01_rows[0].artifact_link!r}) — counter-check non-vacuous"
        )
    else:
        print(
            f"  V79-ROWS FAIL: RECON-01 positive counter-check failed "
            f"(present={_recon01_present}, reproducible={_recon01_repro})"
        )
        wrong_results.append("V79-ROWS: RECON-01 counter-check failed")

    # (f) milestone/key lock: every v7.9 row must carry milestone == "v7.9" AND a
    #     milestone-qualified key of the form "v7.9/<bare_id>". A mis-attributed row
    #     (e.g. key "v8.0/OCH-01" with milestone="v8.0") keeps bare_id/count/tier/link
    #     valid and would otherwise pass silently — this assertion is the attribution lock.
    _bad_ms = [
        r.key for r in _v79_rows
        if r.milestone != "v7.9" or not r.key.startswith("v7.9/")
    ]
    if _bad_ms:
        print(f"  V79-ROWS FAIL: milestone/key drift — {_bad_ms!r}")
        wrong_results.append(f"V79-ROWS: milestone/key drift {_bad_ms!r}")
    else:
        print(f"  V79-ROWS PASS: all {_v79_count} rows carry milestone='v7.9' and 'v7.9/' key prefix")

    # (g) capability lock: reuse the module-level VALID_CAPABILITIES whitelist (the same
    #     set check_consistency enforces, TRACE-01). A capability typo such as
    #     "methodology" (lowercase) is invalid and must fail here, since TRACE-03
    #     --self-test does not run check_consistency() over the live matrix.
    _bad_cap = [r.bare_id for r in _v79_rows if r.capability not in VALID_CAPABILITIES]
    if _bad_cap:
        print(f"  V79-ROWS FAIL: invalid capability on row(s) {_bad_cap!r}")
        wrong_results.append(f"V79-ROWS: invalid capability {_bad_cap!r}")
    else:
        print(
            f"  V79-ROWS PASS: all {_v79_count} rows carry a valid capability "
            f"(in {sorted(VALID_CAPABILITIES)!r})"
        )


def _self_test_v818_rows_sentinel(wrong_results: list[str]) -> None:
    """V818-ROWS named sentinel (D-07 / Phase 4).

    Asserts the 23 v8.18 milestone rows registered in _rows_v818():
      (a) Exactly 23 rows (drift guard — not deleted, not duplicated).
      (b) bare_id set equals the canonical 23 IDs.
      (c) Tier partition pinned by ID, not by count (D-07's first adaptation): the
          audit-only bare_id set is exactly {"SHIP-04", "SHIP-05"} AND the reproducible
          bare_id set is exactly the other 21, named. A blanket 21/2 count assert is
          explicitly rejected — swapping SHIP-04's tier with SHIP-01's would keep the
          counts right and pass silently, the same class of silent pass (f) closes below.
      (d) Deep-resolve artifact_link over the 21 reproducible rows only (D-07's second
          adaptation) — a straight copy of the v7.9 (d) iterates all rows, which is wrong
          here because 2 of the 23 rows are audit-only. Also asserts both audit-only rows
          carry artifact_link == "", so the skip cannot silently become a skip-everything.
      (e) Positive counter-check: HARN-04 is present exactly once, reproducible, and
          carries a non-empty artifact_link (mirrors the V79-ROWS RECON-01 idiom).
      (f) milestone/key lock: every row has milestone == "v8.18" AND a key prefixed
          "v8.18/" (attribution guard — a mis-attributed row passes (a)-(e) silently).
      (g) capability lock: every row's capability is in VALID_CAPABILITIES (the same
          TRACE-01 whitelist check_consistency enforces; not re-run by --self-test).

    Called from _rows_v818() live — never hardcodes a MatrixRow literal (Pitfall 4).
    Honesty-not-score (D-01 idiom): asserts the documented reproducible/audit-only
    registration, not a live pass-rate. Any deletion, tier swap, or dangling
    artifact_link fails CI.
    """
    # (a) Drift guard: read live, assert exactly 23 rows.
    _v818_rows = _rows_v818()
    _v818_count = len(_v818_rows)
    _EXPECTED_V818_IDS = {
        "ACT-01", "ACT-02", "ACT-03", "ACT-04", "ACT-05",
        "LOOP-01", "LOOP-02", "LOOP-03", "LOOP-04", "LOOP-05",
        "PAR-01", "PAR-02", "PAR-03",
        "HARN-01", "HARN-02", "HARN-03", "HARN-04",
        "SHIP-01", "SHIP-02", "SHIP-03", "SHIP-04", "SHIP-05", "SHIP-06",
    }
    _EXPECTED_V818_AUDIT_ONLY_IDS = {"SHIP-04", "SHIP-05"}
    _EXPECTED_V818_REPRODUCIBLE_IDS = _EXPECTED_V818_IDS - _EXPECTED_V818_AUDIT_ONLY_IDS
    if _v818_count != 23:
        print(
            f"  V818-ROWS FAIL: expected exactly 23 rows in _rows_v818(), "
            f"got {_v818_count} — drift guard failed."
        )
        wrong_results.append("V818-ROWS: row count drift (expected 23)")
    else:
        print(f"  V818-ROWS PASS: row count == 23")

    # (b) bare_id set assertion.
    _v818_ids = {r.bare_id for r in _v818_rows}
    if _v818_ids != _EXPECTED_V818_IDS:
        _missing = _EXPECTED_V818_IDS - _v818_ids
        _extra = _v818_ids - _EXPECTED_V818_IDS
        print(
            f"  V818-ROWS FAIL: bare_id set mismatch — "
            f"missing={sorted(_missing)!r}, extra={sorted(_extra)!r}"
        )
        wrong_results.append("V818-ROWS: bare_id set mismatch")
    else:
        print(f"  V818-ROWS PASS: bare_id set = {sorted(_v818_ids)!r}")

    # (c) Tier partition pinned by ID, not by count.
    _audit_only_ids = {r.bare_id for r in _v818_rows if r.coverage_tier == "audit-only"}
    _reproducible_ids = {r.bare_id for r in _v818_rows if r.coverage_tier == "reproducible"}
    if _audit_only_ids != _EXPECTED_V818_AUDIT_ONLY_IDS:
        print(
            f"  V818-ROWS FAIL: audit-only bare_id set mismatch — "
            f"expected={sorted(_EXPECTED_V818_AUDIT_ONLY_IDS)!r}, got={sorted(_audit_only_ids)!r}"
        )
        wrong_results.append("V818-ROWS: audit-only bare_id set mismatch")
    elif _reproducible_ids != _EXPECTED_V818_REPRODUCIBLE_IDS:
        print(
            f"  V818-ROWS FAIL: reproducible bare_id set mismatch — "
            f"expected={sorted(_EXPECTED_V818_REPRODUCIBLE_IDS)!r}, got={sorted(_reproducible_ids)!r}"
        )
        wrong_results.append("V818-ROWS: reproducible bare_id set mismatch")
    else:
        print(
            f"  V818-ROWS PASS: tier partition pinned by ID — audit-only={sorted(_audit_only_ids)!r}, "
            f"21 reproducible IDs confirmed by name"
        )

    # (d) Deep-resolve artifact_link over the 21 reproducible rows only; both audit-only
    #     rows must carry artifact_link == "" (so the skip cannot become a skip-everything).
    _v818_repro_rows = [r for r in _v818_rows if r.coverage_tier == "reproducible"]
    _v818_audit_rows = [r for r in _v818_rows if r.coverage_tier == "audit-only"]
    _link_issues: list[str] = []
    for _row in _v818_repro_rows:
        for _issue in _resolve_artifact(_row.artifact_link):
            _link_issues.append(f"{_row.bare_id}: {_issue}")
    _nonempty_audit_links = [r.bare_id for r in _v818_audit_rows if r.artifact_link != ""]
    if _link_issues:
        for _issue in _link_issues:
            print(f"  V818-ROWS FAIL: artifact_link issue — {_issue}")
        wrong_results.append(f"V818-ROWS: {len(_link_issues)} artifact_link issue(s)")
    elif _nonempty_audit_links:
        print(
            f"  V818-ROWS FAIL: audit-only row(s) with non-empty artifact_link — "
            f"{_nonempty_audit_links!r}"
        )
        wrong_results.append("V818-ROWS: audit-only row(s) with non-empty artifact_link")
    else:
        print(
            f"  V818-ROWS PASS: all {len(_v818_repro_rows)} reproducible artifact_links "
            f"deep-resolve OK, both audit-only rows carry artifact_link=''"
        )

    # (e) Positive counter-check: HARN-04 is present, reproducible, non-empty artifact_link.
    _harn04_rows = [r for r in _v818_rows if r.bare_id == "HARN-04"]
    _harn04_present = len(_harn04_rows) == 1
    _harn04_repro = _harn04_rows[0].coverage_tier == "reproducible" if _harn04_rows else False
    _harn04_link = _harn04_rows[0].artifact_link if _harn04_rows else ""
    if _harn04_present and _harn04_repro and _harn04_link:
        print(
            f"  V818-ROWS PASS: HARN-04 present and reproducible "
            f"(artifact_link={_harn04_link!r}) — counter-check non-vacuous"
        )
    else:
        print(
            f"  V818-ROWS FAIL: HARN-04 positive counter-check failed "
            f"(present={_harn04_present}, reproducible={_harn04_repro}, link={_harn04_link!r})"
        )
        wrong_results.append("V818-ROWS: HARN-04 counter-check failed")

    # (f) milestone/key lock.
    _bad_ms = [
        r.key for r in _v818_rows
        if r.milestone != "v8.18" or not r.key.startswith("v8.18/")
    ]
    if _bad_ms:
        print(f"  V818-ROWS FAIL: milestone/key drift — {_bad_ms!r}")
        wrong_results.append(f"V818-ROWS: milestone/key drift {_bad_ms!r}")
    else:
        print(f"  V818-ROWS PASS: all {_v818_count} rows carry milestone='v8.18' and 'v8.18/' key prefix")

    # (g) capability lock.
    _bad_cap = [r.bare_id for r in _v818_rows if r.capability not in VALID_CAPABILITIES]
    if _bad_cap:
        print(f"  V818-ROWS FAIL: invalid capability on row(s) {_bad_cap!r}")
        wrong_results.append(f"V818-ROWS: invalid capability {_bad_cap!r}")
    else:
        print(
            f"  V818-ROWS PASS: all {_v818_count} rows carry a valid capability "
            f"(in {sorted(VALID_CAPABILITIES)!r})"
        )


def _self_test_v824_rows_sentinel(wrong_results: list[str]) -> None:
    """V824-ROWS named sentinel (D-09 / Phase 6).

    Asserts the 15 v8.24 milestone rows registered in _rows_v824():
      (a) Exactly 15 rows (drift guard — not deleted, not duplicated).
      (b) bare_id set equals the canonical 15 IDs.
      (c) Tier partition pinned by ID, not by count (D-07): the audit-only bare_id set is
          exactly {"VAL-04"} AND the reproducible bare_id set is exactly the other 14, named.
          A blanket 14/1 count assert is explicitly rejected — swapping VAL-04's tier with a
          reproducible row's would keep the counts right and pass silently.
      (d) Deep-resolve artifact_link over the 14 reproducible rows only. Also asserts the
          audit-only row carries artifact_link == "", so the skip cannot silently become a
          skip-everything.
      (e) Positive counter-check: GATE-03 is present exactly once, reproducible, and carries a
          non-empty artifact_link (mirrors the V818-ROWS HARN-04 idiom).
      (f) milestone/key lock: every row has milestone == "v8.24" AND a key prefixed
          "v8.24/" (attribution guard — a mis-attributed row passes (a)-(e) silently).
      (g) capability lock: every row's capability is in VALID_CAPABILITIES (the same
          TRACE-01 whitelist check_consistency enforces; not re-run by --self-test).

    Called from _rows_v824() live — never hardcodes a MatrixRow literal (Pitfall 4).
    Honesty-not-score (D-01 idiom): asserts the documented reproducible/audit-only
    registration, not a live pass-rate. Any deletion, tier swap, or dangling
    artifact_link fails CI.
    """
    # (a) Drift guard: read live, assert exactly 15 rows.
    _v824_rows = _rows_v824()
    _v824_count = len(_v824_rows)
    _EXPECTED_V824_IDS = {
        "CAP-01", "CAP-02", "CAP-03",
        "PROV-01", "PROV-02", "PROV-03", "PROV-04", "PROV-05",
        "GATE-01", "GATE-02", "GATE-03",
        "VAL-01", "VAL-02", "VAL-03", "VAL-04",
    }
    _EXPECTED_V824_AUDIT_ONLY_IDS = {"VAL-04"}
    _EXPECTED_V824_REPRODUCIBLE_IDS = _EXPECTED_V824_IDS - _EXPECTED_V824_AUDIT_ONLY_IDS
    if _v824_count != 15:
        print(
            f"  V824-ROWS FAIL: expected exactly 15 rows in _rows_v824(), "
            f"got {_v824_count} — drift guard failed."
        )
        wrong_results.append("V824-ROWS: row count drift (expected 15)")
    else:
        print(f"  V824-ROWS PASS: row count == 15")

    # (b) bare_id set assertion.
    _v824_ids = {r.bare_id for r in _v824_rows}
    if _v824_ids != _EXPECTED_V824_IDS:
        _missing = _EXPECTED_V824_IDS - _v824_ids
        _extra = _v824_ids - _EXPECTED_V824_IDS
        print(
            f"  V824-ROWS FAIL: bare_id set mismatch — "
            f"missing={sorted(_missing)!r}, extra={sorted(_extra)!r}"
        )
        wrong_results.append("V824-ROWS: bare_id set mismatch")
    else:
        print(f"  V824-ROWS PASS: bare_id set = {sorted(_v824_ids)!r}")

    # (c) Tier partition pinned by ID, not by count.
    _audit_only_ids = {r.bare_id for r in _v824_rows if r.coverage_tier == "audit-only"}
    _reproducible_ids = {r.bare_id for r in _v824_rows if r.coverage_tier == "reproducible"}
    if _audit_only_ids != _EXPECTED_V824_AUDIT_ONLY_IDS:
        print(
            f"  V824-ROWS FAIL: audit-only bare_id set mismatch — "
            f"expected={sorted(_EXPECTED_V824_AUDIT_ONLY_IDS)!r}, got={sorted(_audit_only_ids)!r}"
        )
        wrong_results.append("V824-ROWS: audit-only bare_id set mismatch")
    elif _reproducible_ids != _EXPECTED_V824_REPRODUCIBLE_IDS:
        print(
            f"  V824-ROWS FAIL: reproducible bare_id set mismatch — "
            f"expected={sorted(_EXPECTED_V824_REPRODUCIBLE_IDS)!r}, got={sorted(_reproducible_ids)!r}"
        )
        wrong_results.append("V824-ROWS: reproducible bare_id set mismatch")
    else:
        print(
            f"  V824-ROWS PASS: tier partition pinned by ID — audit-only={sorted(_audit_only_ids)!r}, "
            f"14 reproducible IDs confirmed by name"
        )

    # (d) Deep-resolve artifact_link over the 14 reproducible rows only; the audit-only
    #     row must carry artifact_link == "" (so the skip cannot become a skip-everything).
    _v824_repro_rows = [r for r in _v824_rows if r.coverage_tier == "reproducible"]
    _v824_audit_rows = [r for r in _v824_rows if r.coverage_tier == "audit-only"]
    _link_issues: list[str] = []
    for _row in _v824_repro_rows:
        for _issue in _resolve_artifact(_row.artifact_link):
            _link_issues.append(f"{_row.bare_id}: {_issue}")
    _nonempty_audit_links = [r.bare_id for r in _v824_audit_rows if r.artifact_link != ""]
    if _link_issues:
        for _issue in _link_issues:
            print(f"  V824-ROWS FAIL: artifact_link issue — {_issue}")
        wrong_results.append(f"V824-ROWS: {len(_link_issues)} artifact_link issue(s)")
    elif _nonempty_audit_links:
        print(
            f"  V824-ROWS FAIL: audit-only row(s) with non-empty artifact_link — "
            f"{_nonempty_audit_links!r}"
        )
        wrong_results.append("V824-ROWS: audit-only row(s) with non-empty artifact_link")
    else:
        print(
            f"  V824-ROWS PASS: all {len(_v824_repro_rows)} reproducible artifact_links "
            f"deep-resolve OK, audit-only row carries artifact_link=''"
        )

    # (e) Positive counter-check: GATE-03 is present, reproducible, non-empty artifact_link.
    _gate03_rows = [r for r in _v824_rows if r.bare_id == "GATE-03"]
    _gate03_present = len(_gate03_rows) == 1
    _gate03_repro = _gate03_rows[0].coverage_tier == "reproducible" if _gate03_rows else False
    _gate03_link = _gate03_rows[0].artifact_link if _gate03_rows else ""
    if _gate03_present and _gate03_repro and _gate03_link:
        print(
            f"  V824-ROWS PASS: GATE-03 present and reproducible "
            f"(artifact_link={_gate03_link!r}) — counter-check non-vacuous"
        )
    else:
        print(
            f"  V824-ROWS FAIL: GATE-03 positive counter-check failed "
            f"(present={_gate03_present}, reproducible={_gate03_repro}, link={_gate03_link!r})"
        )
        wrong_results.append("V824-ROWS: GATE-03 counter-check failed")

    # (f) milestone/key lock.
    _bad_ms = [
        r.key for r in _v824_rows
        if r.milestone != "v8.24" or not r.key.startswith("v8.24/")
    ]
    if _bad_ms:
        print(f"  V824-ROWS FAIL: milestone/key drift — {_bad_ms!r}")
        wrong_results.append(f"V824-ROWS: milestone/key drift {_bad_ms!r}")
    else:
        print(f"  V824-ROWS PASS: all {_v824_count} rows carry milestone='v8.24' and 'v8.24/' key prefix")

    # (g) capability lock.
    _bad_cap = [r.bare_id for r in _v824_rows if r.capability not in VALID_CAPABILITIES]
    if _bad_cap:
        print(f"  V824-ROWS FAIL: invalid capability on row(s) {_bad_cap!r}")
        wrong_results.append(f"V824-ROWS: invalid capability {_bad_cap!r}")
    else:
        print(
            f"  V824-ROWS PASS: all {_v824_count} rows carry a valid capability "
            f"(in {sorted(VALID_CAPABILITIES)!r})"
        )


def _self_test_headline_lock(wrong_results: list[str]) -> None:
    """HEADLINE-LOCK named sentinel (WR-08 / v8.18 Phase 4 review).

    Ties the three published, hand-copied or generator-written coverage surfaces back to
    build_matrix_rows(), which nothing previously did. The v8.18 review measured the gap:
    no script anywhere contained the literal headline figure, and TRACE-03's --self-test
    never re-rendered the matrix to compare it against the tracked artifacts, because the
    `emit` subcommand is a manual regeneration step that CI does not run.

    That gap is not hypothetical. The same review's CR-01 was exactly this drift: an
    `88 audit-only` figure surviving in two places six and fifty lines from a headline the
    same commit had moved to 90. It was corrected by hand, closing the instance and leaving
    the mechanism intact, so the next headline move would have reopened it identically.

    Asserts:
      (a) Published-headline lock: docs/requirements-traceability.md states exactly the
          headline build_matrix_rows() produces. Every one of the four figures is derived
          live — including the gap count, which is NOT hardcoded to 0. Hardcoding it would
          mean that the first real gap row makes this sentinel fail while blaming the prose,
          which would be a correct document losing to a stale assertion.
      (b) Non-vacuity control for (a): the same predicate, run against a copy of the document
          with the reproducible count perturbed, must report a mismatch. Without this, a
          rewritten (a) that always passes is indistinguishable from a passing (a).
      (c) Markdown artifact freshness: docs/requirements-matrix.md on disk is byte-identical
          to render_matrix_markdown(rows). Deterministic — the renderer embeds no timestamp.
      (d) JSON artifact freshness: docs/data/matrix.json on disk is byte-identical to what
          emit_matrix writes, built through the same json.dumps(..., indent=2) over asdict.
      (e) Non-vacuity control for (c)/(d): perturbed copies of both artifacts must compare
          unequal, proving the comparison is a real comparison and not a tautology.
      (f) Per-surface headline presence: every surface named in COVERED_HEADLINE_SURFACES
          states the current headline in either rendering (prose or compact-slash),
          label-agnostic — this is what proves docs/COMPONENT-DIAGRAM.md is covered even
          though it only ever states the bare slash form and never the
          "**Coverage headline:**" label (a) is keyed to. Tightened in Phase 10 Plan 02
          (HEADLINE-03) to require at least one hit that
          `_is_historical_headline_hit()` does NOT call historical — a delta row or
          historical statement elsewhere in the same file must not be able to satisfy this
          on its own, so a surface whose only occurrence is a ledger delta (e.g. an arrow
          row) correctly fails here rather than passing on a technicality.
      (g) Non-vacuity control for (f): for each surface independently, perturbing its
          in-memory copy so that (f)'s tightened, non-historical-only predicate finds zero
          hits — holding every other surface's real text untouched. Sharpened in Phase 10
          Plan 02 to perturb ONLY the lines `_is_historical_headline_hit()` does NOT call
          historical, via `_perturb_non_historical_hits()`, leaving every historical/delta
          line (e.g. an arrow-marked ledger row) byte-correct in the mutated copy — this is
          a line-level, classifier-driven perturbation rather than a rendering-keyed guess
          (perturb "the prose form") because docs/requirements-traceability.md carries two
          non-historical hits in two different renderings (line 7 prose, line 99 slash
          narrative) and one historical hit in the slash rendering (line 80, arrow); a
          rendering guess cannot correctly single out just the historical line. For surfaces
          with a single, non-historical occurrence this has the same effect as plan 10-01's
          blanket perturbation. Each control's message names its own surface.
      (h) Positive controls (HEADLINE-03, ROADMAP criterion 3, CR-02 fix): layer
          attribution is asserted on SYNTHETIC lines carrying the current literal at the
          REAL surface relpath — docs/v8.0-final-closure.md and CHANGELOG.md must attribute
          a no-arrow line to the WHOLE-FILE layer, and docs/requirements-traceability.md
          must attribute a delta-shaped line to the ARROW layer specifically, inside a file
          that is NOT whole-file exempt (T-10-05 — if it were, assertion (a) would be
          defeated). None of the three needs the live file to still contain today's figure,
          because `_is_historical_headline_hit()` does not depend on the figure at all — a
          control bound to a live occurrence tested a strictly narrower, stronger
          precondition than the historicity property it claimed to prove, and broke on
          every legitimate headline move (CR-02). A discriminating arm (WR-06) evaluates the
          identical no-arrow line at a relpath that is NOT whole-file exempt and requires
          `""`, proving whole-file MEMBERSHIP — not the line's content — is what rescues the
          two whole-file cases. The one genuinely live-file claim that survives —
          docs/v8.0-final-closure.md still containing a no-arrow current-literal line today
          — is reported as INFO, never asserted, because it legitimately stops being true
          the moment the headline moves.
      (h2) Headline-move invariance control (T-10-05 continuation): for each (h) case,
          asserts `_headline_exempt_layer()` returns the SAME layer for the identical line
          built from `_prose`/`_slash` and from `_perturbed_prose`/`_perturbed_slash` — a
          cheap, deterministic, in-process stand-in for manually simulating a headline move,
          permanently asserting that the (h) controls stay figure-independent rather than
          leaving that property incidental. A second arm requires the two constructed lines
          to be non-byte-equal, so a future edit that made the perturbation a no-op cannot
          leave this passing vacuously forever.
      (i) Non-vacuity control for the classifier (T-10-04): feeds
          `_is_historical_headline_hit()` a synthetic, non-exempt path and a synthetic line
          containing the current literal with no arrow, and requires NOT historical.
          Prevents (h)'s positive controls from passing off a classifier rewritten to
          `return True` unconditionally.
      (i2) Adjacency-specific controls (CR-03, T-10-04-01): a mermaid edge and an HTML
          comment terminator sharing a line with the current headline must NOT exempt that
          line from `_unregistered_headline_finding()` (the fail-unsafe case CR-03 names),
          while a genuine delta line (a superseded figure, an arrow, then the current
          figure) still must be exempt — proving the narrowing did not simply disable the
          arrow layer. Every control drives through `_unregistered_headline_finding()`
          itself, never a parallel copy.
      (j) Tree-wide unregistered-surface scan (HEADLINE-05, T-10-07): files are collected
          through the shared `_headline_scan_files()` helper (also driven directly by block
          (l)'s non-vacuity control), every matched file is read, its hits fed through
          `_unregistered_headline_finding()` (which itself calls
          `_is_historical_headline_hit()` — the identical function object (h)/(i) exercise,
          so HEADLINE-05's documented dependency on HEADLINE-03 already holding is enforced
          by construction, not by convention), and any non-historical hit whose file is not
          in COVERED_HEADLINE_SURFACES is a FAIL naming the file and line. Before the PASS
          branch, `_headline_scan_floor_breaches()` (CR-01 fix) asserts a derived coverage
          floor — every path in COVERED_HEADLINE_SURFACES | HISTORICAL_EXEMPT_FILES must be
          reachable by the configured globs — and, if that holds, a derived accounted-hit
          floor — at least one non-historical hit per registered surface. Both are derived
          from the constants, never a magic number, so an emptied or narrowed
          HEADLINE_SCAN_GLOBS can no longer stay green while reading nothing; this is what
          lets COVERED_HEADLINE_SURFACES under-count without being silently wrong: an
          omission is caught loudly here rather than trusted. Never follows a symlink
          resolving outside REPO_ROOT and never descends into the git-ignored, untracked
          docs/history/ (the glob is non-recursive by construction).
      (k) Non-vacuity control for (j) (T-10-08): a synthetic path/line combination, driven
          through the SAME `_unregistered_headline_finding()` function object the real scan
          calls, proves three directions — the synthetic unregistered hit IS reported; the
          identical line attributed to a registered surface is NOT reported (else the
          function would simply flag everything); and the same synthetic path with an arrow
          appended is NOT reported (proving the scan is gated behind HEADLINE-03's
          classifier, not merely a membership test). Preconditions are asserted explicitly so
          the control cannot silently degrade into a tautology.

    Reads live files rather than fixtures (Pitfall 4 idiom, as V79-ROWS / V818-ROWS do), so
    it locks the shipped surfaces themselves and not a copy of them. Offline and deterministic:
    no live claude session, no network, no writes.
    """
    _rows = build_matrix_rows()
    _repro = sum(1 for r in _rows if r.coverage_tier == "reproducible")
    _audit = sum(1 for r in _rows if r.coverage_tier == "audit-only")
    _gap = sum(1 for r in _rows if r.coverage_tier == "gap")
    _expected = (
        f"{_repro} reproducible / {_audit} audit-only / {_gap} gap / {len(_rows)} total"
    )
    _headline = f"**Coverage headline:** {_expected}"

    # Label-agnostic literals: bare numbers, no "**Coverage headline:**" prefix and no bold
    # wrapping, so a match works regardless of a surface's own label wording. Built from the
    # same _repro/_audit/_gap/len(_rows) locals as _expected above — never a separate
    # literal, so a future headline move updates every assertion that uses these
    # automatically, including the ones added in this function below.
    _prose = f"{_repro} reproducible / {_audit} audit-only / {_gap} gap / {len(_rows)} total"
    _slash = f"{_repro}/{_audit}/{_gap}/{len(_rows)}"

    def _headline_hits(text: str) -> list[tuple[int, str]]:
        """Return every (1-based line number, line text) pair whose line contains either
        the current headline's prose or compact-slash rendering as a substring.

        Shared by every per-surface assertion below and its own non-vacuity control —
        never re-implemented in parallel — so a control that calls this function proves the
        real assertion's code path is non-vacuous, not a copy that could silently diverge.
        """
        return [
            (_i, _line)
            for _i, _line in enumerate(text.splitlines(), start=1)
            if _prose in _line or _slash in _line
        ]

    def _headline_matches(text: str) -> bool:
        """The (a) predicate, isolated so (b) can exercise the identical code path."""
        return _headline in text

    # (a) Published-headline lock.
    _trace_path = REPO_ROOT / "docs" / "requirements-traceability.md"
    if not _trace_path.is_file():
        print(f"  HEADLINE-LOCK FAIL: {_trace_path} not found")
        wrong_results.append("HEADLINE-LOCK: docs/requirements-traceability.md missing")
        return
    _trace = _trace_path.read_text(encoding="utf-8")
    if _headline_matches(_trace):
        print(f"  HEADLINE-LOCK PASS: published headline == {_expected}")
    else:
        print(
            f"  HEADLINE-LOCK FAIL: docs/requirements-traceability.md does not state "
            f"{_expected!r} — build_matrix_rows() and the published headline disagree"
        )
        wrong_results.append(
            f"HEADLINE-LOCK: published headline disagrees with build_matrix_rows() "
            f"(expected {_expected!r})"
        )

    # (b) Non-vacuity control for (a): perturb the reproducible count, expect a mismatch.
    _mutated_trace = _trace.replace(
        _headline, f"**Coverage headline:** {_repro + 1} reproducible / {_audit} "
        f"audit-only / {_gap} gap / {len(_rows)} total"
    )
    if _headline_matches(_mutated_trace):
        print("  HEADLINE-LOCK FAIL: (a) passed a perturbed headline — assertion is vacuous")
        wrong_results.append("HEADLINE-LOCK: (a) negative control did not fail")
    else:
        print("  HEADLINE-LOCK PASS: (a) rejects a perturbed headline — non-vacuous")

    # (c) Markdown artifact freshness.
    _md_path = REPO_ROOT / "docs" / "requirements-matrix.md"
    _md_live = render_matrix_markdown(_rows)
    if not _md_path.is_file():
        print(f"  HEADLINE-LOCK FAIL: {_md_path} not found")
        wrong_results.append("HEADLINE-LOCK: docs/requirements-matrix.md missing")
        return
    _md_disk = _md_path.read_text(encoding="utf-8")
    if _md_disk == _md_live:
        print(
            f"  HEADLINE-LOCK PASS: docs/requirements-matrix.md byte-identical to "
            f"render_matrix_markdown() ({len(_rows)} rows)"
        )
    else:
        print(
            "  HEADLINE-LOCK FAIL: docs/requirements-matrix.md is stale — "
            "re-run the emit subcommand"
        )
        wrong_results.append(
            "HEADLINE-LOCK: docs/requirements-matrix.md disagrees with build_matrix_rows()"
        )

    # (d) JSON artifact freshness — built exactly as emit_matrix writes it.
    _json_path = REPO_ROOT / "docs" / "data" / "matrix.json"
    _json_live = json.dumps([asdict(r) for r in _rows], indent=2)
    if not _json_path.is_file():
        print(f"  HEADLINE-LOCK FAIL: {_json_path} not found")
        wrong_results.append("HEADLINE-LOCK: docs/data/matrix.json missing")
        return
    _json_disk = _json_path.read_text(encoding="utf-8")
    if _json_disk == _json_live:
        print(
            f"  HEADLINE-LOCK PASS: docs/data/matrix.json byte-identical to emit output "
            f"({len(_rows)} rows)"
        )
    else:
        print(
            "  HEADLINE-LOCK FAIL: docs/data/matrix.json is stale — re-run the emit subcommand"
        )
        wrong_results.append(
            "HEADLINE-LOCK: docs/data/matrix.json disagrees with build_matrix_rows()"
        )

    # (e) Non-vacuity control for (c)/(d): perturbed artifacts must compare unequal.
    _md_vacuous = (_md_disk + "\n") == _md_live
    _json_vacuous = (_json_disk + "\n") == _json_live
    if _md_vacuous or _json_vacuous:
        print(
            f"  HEADLINE-LOCK FAIL: byte-comparison is vacuous "
            f"(md={_md_vacuous}, json={_json_vacuous})"
        )
        wrong_results.append("HEADLINE-LOCK: (c)/(d) negative control did not fail")
    else:
        print("  HEADLINE-LOCK PASS: (c)/(d) reject perturbed artifacts — non-vacuous")

    # (f) Per-surface headline presence across every currently covered surface (sorted for
    # deterministic output), including docs/requirements-traceability.md again via the
    # label-agnostic scanner — (a) above is specific to that file's own
    # "**Coverage headline:**" label wording, so (f) additionally proves the bare-literal
    # scanner every other surface relies on also covers it.
    _perturbed_prose = (
        f"{_repro + 1} reproducible / {_audit} audit-only / {_gap} gap / {len(_rows)} total"
    )
    _perturbed_slash = f"{_repro + 1}/{_audit}/{_gap}/{len(_rows)}"

    def _perturb_non_historical_hits(text: str, relpath: str) -> str:
        """Return a copy of text with the current headline literal replaced ONLY on lines
        that _is_historical_headline_hit() does not call historical, leaving every
        historical/delta line byte-unchanged. This is what makes (g) sharp: it perturbs
        exactly the lines (f) counts as evidence, via the SAME classifier, rather than a
        rendering-keyed guess at which occurrence is "the" current-fact line. A rendering
        guess (perturb only the prose form, say) is not sound here —
        docs/requirements-traceability.md carries two non-historical hits in two different
        renderings (line 7 prose, line 99 slash narrative — see the measured classification
        table, point 3) and one historical hit in the slash rendering (line 80, arrow), so
        "perturb the prose rendering only" would leave line 99's non-historical slash hit
        live in the mutated copy, silently defeating the control. Verified live against both
        docs/README.md (line 20 non-historical vs. line 100 historical/arrow) and
        docs/requirements-traceability.md (lines 7/99 non-historical vs. line 80
        historical/arrow) before adopting this approach over the rendering-keyed one.
        """
        return "\n".join(
            _line.replace(_prose, _perturbed_prose).replace(_slash, _perturbed_slash)
            if (_prose in _line or _slash in _line)
            and not _is_historical_headline_hit(relpath, _line)
            else _line
            for _line in text.splitlines()
        )

    for _surface in sorted(COVERED_HEADLINE_SURFACES):
        _surface_path = REPO_ROOT / _surface
        if not _surface_path.is_file():
            print(f"  HEADLINE-LOCK FAIL: (f) {_surface} not found")
            wrong_results.append(f"HEADLINE-LOCK: (f) {_surface} missing")
            continue
        _surface_text = _surface_path.read_text(encoding="utf-8")
        _hits = _headline_hits(_surface_text)
        _current_hits = [
            (_i, _line)
            for _i, _line in _hits
            if not _is_historical_headline_hit(_surface, _line)
        ]
        if _current_hits:
            _renderings = sorted(
                {"prose" if _prose in _line else "slash" for _, _line in _current_hits}
            )
            print(
                f"  HEADLINE-LOCK PASS: (f) {_surface} states the current, non-historical "
                f"headline (rendering(s): {', '.join(_renderings)})"
            )
        else:
            print(
                f"  HEADLINE-LOCK FAIL: (f) {_surface} does not state {_expected!r} as a "
                f"non-historical occurrence — build_matrix_rows() and {_surface} disagree, "
                f"or the only occurrence present is historical/delta"
            )
            wrong_results.append(
                f"HEADLINE-LOCK: (f) {_surface} does not state the current headline "
                f"(expected {_expected!r})"
            )

        # (g) Non-vacuity control for (f): perturb this surface's in-memory copy so that
        # (f)'s tightened, non-historical-only predicate finds zero hits. Only lines the
        # classifier does NOT call historical are perturbed — every historical/delta line
        # (e.g. an arrow-marked ledger row) is left byte-correct in the mutated copy, so the
        # control proves the classifier (not a blanket textual perturbation) is what does
        # the rejecting. For surfaces with a single, non-historical occurrence this has the
        # same effect as plan 10-01's blanket perturbation.
        _mutated_surface = _perturb_non_historical_hits(_surface_text, _surface)
        _mutated_current_hits = [
            (_i, _line)
            for _i, _line in _headline_hits(_mutated_surface)
            if not _is_historical_headline_hit(_surface, _line)
        ]
        if _mutated_current_hits:
            print(
                f"  HEADLINE-LOCK FAIL: (g) {_surface} still has a non-historical match "
                f"after its current-fact occurrence was perturbed — control is vacuous"
            )
            wrong_results.append(f"HEADLINE-LOCK: (g) {_surface} negative control did not fail")
        else:
            print(
                f"  HEADLINE-LOCK PASS: (g) {_surface} rejects a perturbed headline — "
                f"non-vacuous"
            )

    def _headline_exempt_layer(relpath: str, line: str) -> str:
        """Which layer of _is_historical_headline_hit() classifies (relpath, line) as
        historical: "whole-file" if relpath is a member of HISTORICAL_EXEMPT_FILES,
        "arrow" if the classifier accepted the line for any other reason, or "" if the
        classifier does not call it historical at all.

        Delegates to _is_historical_headline_hit() rather than re-deriving the arrow test,
        so this helper can never disagree with the classifier it attributes — a control
        exercising a parallel copy would prove nothing (research Pitfall 4, the same rule
        _unregistered_headline_finding() below already observes). If the classifier's arrow
        layer is narrowed or a third layer is ever added, this helper picks up the change
        automatically instead of silently keeping stale semantics while still printing PASS.
        """
        if not _is_historical_headline_hit(relpath, line):
            return ""
        # Whole-file is checked first by the classifier, so a member relpath is attributed
        # there regardless of the line; anything else the classifier accepted is arrow-layer.
        return "whole-file" if relpath in HISTORICAL_EXEMPT_FILES else "arrow"

    # (h) Positive controls (ROADMAP criterion 3, CR-02 fix): layer attribution is asserted
    # on SYNTHETIC lines carrying the current literal at the REAL surface relpath, never on
    # a line located by scanning the live file for today's figure. _is_historical_headline_
    # hit() does not depend on the figure at all, so binding the control to a live
    # occurrence of it made the precondition ("this line contains today's headline")
    # strictly stronger than the property under test ("this line is historical") — the next
    # legitimate headline move broke all three controls and could only be resolved by
    # editing CHANGELOG.md or docs/v8.0-final-closure.md, two records this repo designates
    # historical and frozen (CR-02). Every literal below is built from the in-scope
    # _prose/_slash locals; the delta row's superseded left-hand figure is a fixed,
    # non-current placeholder and is not the headline, so it may be typed.
    _synthetic_no_arrow_line = f"Superseded: the headline is now {_prose}."
    _synthetic_delta_line = f"| 9 | some milestone | 0/0/0/1 → {_slash} | ... |"
    for _relpath, _line, _want in (
        ("docs/v8.0-final-closure.md", _synthetic_no_arrow_line, "whole-file"),
        ("CHANGELOG.md", _synthetic_no_arrow_line, "whole-file"),
        ("docs/requirements-traceability.md", _synthetic_delta_line, "arrow"),
    ):
        if (
            _relpath == "docs/requirements-traceability.md"
            and _relpath in HISTORICAL_EXEMPT_FILES
        ):
            # Explicit precondition (T-10-05): if this file were ever added to the
            # whole-file exemption, assertion (a) (which requires this same file to state
            # the current headline as a present-tense claim) would be defeated. Say so
            # rather than silently attributing the delta row to the wrong layer.
            print(
                f"  HEADLINE-LOCK FAIL: (h) precondition violated — {_relpath} is in "
                "HISTORICAL_EXEMPT_FILES, which would defeat assertion (a)"
            )
            wrong_results.append(f"HEADLINE-LOCK: (h) {_relpath} precondition violated")
            continue
        _got = _headline_exempt_layer(_relpath, _line)
        if _got == _want:
            print(
                f"  HEADLINE-LOCK PASS: (h) {_relpath} attributes a synthetic "
                f"{'delta-shaped' if _want == 'arrow' else 'no-arrow'} line carrying the "
                f"current literal to the {_want.upper()} layer"
            )
        else:
            print(
                f"  HEADLINE-LOCK FAIL: (h) {_relpath} attributed a synthetic "
                f"{'delta-shaped' if _want == 'arrow' else 'no-arrow'} line to {_got!r}, "
                f"wanted {_want!r}"
            )
            wrong_results.append(f"HEADLINE-LOCK: (h) {_relpath} layer attribution failed")

    # Discriminating arm (WR-06 fix): the identical synthetic no-arrow line, evaluated at a
    # relpath that is NOT whole-file exempt, must attribute "" — proving it is whole-file
    # MEMBERSHIP, not the line's content, that rescues the two whole-file cases above. This
    # is what stops the CHANGELOG.md/v8.0-final-closure.md cases from being tautological:
    # the same line at a non-exempt path is correctly NOT rescued.
    _non_exempt_relpath = "docs/does-not-exist-synthetic-non-exempt-headline-check.md"
    if _non_exempt_relpath in HISTORICAL_EXEMPT_FILES:
        print(
            "  HEADLINE-LOCK FAIL: (h) precondition violated — the discriminating arm's "
            "synthetic path is in HISTORICAL_EXEMPT_FILES"
        )
        wrong_results.append("HEADLINE-LOCK: (h) discriminating-arm precondition violated")
    else:
        _got = _headline_exempt_layer(_non_exempt_relpath, _synthetic_no_arrow_line)
        if _got == "":
            print(
                "  HEADLINE-LOCK PASS: (h) the same no-arrow synthetic line attributes to "
                "'' at a non-whole-file-exempt relpath — whole-file MEMBERSHIP rescues the "
                "line, not its content"
            )
        else:
            print(
                f"  HEADLINE-LOCK FAIL: (h) the no-arrow synthetic line attributed to "
                f"{_got!r} at a non-exempt relpath — should be '' (content alone should "
                "not rescue it)"
            )
            wrong_results.append(
                "HEADLINE-LOCK: (h) discriminating arm did not attribute ''"
            )

    # Demoted live-file observation (CR-02): the whole-file layer's only live proof in this
    # tree — a no-arrow current-literal line genuinely present in docs/v8.0-final-closure.md
    # — is reported for visibility in diff review, never asserted, because it legitimately
    # stops being true the moment the headline moves; binding the gate to it is precisely
    # the defect CR-02 records. A missing docs/v8.0-final-closure.md is still a real
    # repository defect and stays a wrong_results finding.
    _v80_path = REPO_ROOT / "docs" / "v8.0-final-closure.md"
    if not _v80_path.is_file():
        print(f"  HEADLINE-LOCK FAIL: (h) {_v80_path} not found")
        wrong_results.append("HEADLINE-LOCK: (h) docs/v8.0-final-closure.md missing")
    else:
        _v80_text = _v80_path.read_text(encoding="utf-8")
        _v80_hit = next(
            (
                (_i, _line)
                for _i, _line in _headline_hits(_v80_text)
                if "→" not in _line and "->" not in _line
            ),
            None,
        )
        if _v80_hit is not None:
            print(
                "  HEADLINE-LOCK INFO: (h) docs/v8.0-final-closure.md still carries a live "
                f"no-arrow current-literal line (line {_v80_hit[0]}) — reported only, not "
                "asserted, because it is expected to stop being true on a headline move"
            )
        else:
            print(
                "  HEADLINE-LOCK INFO: (h) docs/v8.0-final-closure.md no longer carries a "
                "live no-arrow current-literal line — expected after a headline move, "
                "reported only, not asserted"
            )

    # (h2) Headline-move invariance control: Task 1's (h) rewrite makes the three controls
    # figure-independent, but nothing yet ASSERTS that they are — a future edit could rebind
    # one back to a live literal and every control would stay green, the defect one layer
    # down. For each (h) case, build the identical synthetic line twice — once from
    # _prose/_slash, once from _perturbed_prose/_perturbed_slash (already in scope for block
    # (g), reused rather than re-derived) — and require _headline_exempt_layer() to return
    # the SAME layer for both; it must, because the classifier never reads the figure. A
    # second arm asserts the two constructed lines are NOT byte-equal, so a future edit that
    # made the perturbation a no-op cannot leave this comparing a string to itself forever.
    _perturbed_no_arrow_line = f"Superseded: the headline is now {_perturbed_prose}."
    _perturbed_delta_line = f"| 9 | some milestone | 0/0/0/1 → {_perturbed_slash} | ... |"
    _h2_cases = (
        ("docs/v8.0-final-closure.md", _synthetic_no_arrow_line, _perturbed_no_arrow_line),
        ("CHANGELOG.md", _synthetic_no_arrow_line, _perturbed_no_arrow_line),
        ("docs/requirements-traceability.md", _synthetic_delta_line, _perturbed_delta_line),
    )
    _h2_precondition_failed = [
        _relpath for _relpath, _orig_line, _pert_line in _h2_cases if _orig_line == _pert_line
    ]
    if _h2_precondition_failed:
        print(
            f"  HEADLINE-LOCK FAIL: (h2) precondition violated for "
            f"{_h2_precondition_failed} — synthetic and perturbed lines are byte-equal, "
            "the perturbation did not change the line"
        )
        wrong_results.append(
            f"HEADLINE-LOCK: (h2) precondition violated for {_h2_precondition_failed}"
        )
    else:
        _h2_mismatches = [
            (_relpath, _headline_exempt_layer(_relpath, _orig_line),
             _headline_exempt_layer(_relpath, _pert_line))
            for _relpath, _orig_line, _pert_line in _h2_cases
        ]
        _h2_broken = [
            (_relpath, _layer_orig, _layer_pert)
            for _relpath, _layer_orig, _layer_pert in _h2_mismatches
            if _layer_orig != _layer_pert
        ]
        if _h2_broken:
            print(
                f"  HEADLINE-LOCK FAIL: (h2) layer attribution is NOT invariant under a "
                f"perturbed figure: {_h2_broken} — a consumer has been rebound to the "
                "current literal"
            )
            wrong_results.append(
                f"HEADLINE-LOCK: (h2) invariance broken for "
                f"{[r for r, _, _ in _h2_broken]}"
            )
        else:
            print(
                "  HEADLINE-LOCK PASS: (h2) all three (h) verdicts (docs/v8.0-final-"
                "closure.md, CHANGELOG.md, docs/requirements-traceability.md) are "
                "invariant under a perturbed figure"
            )

    # (i) Non-vacuity control for the classifier itself (T-10-04): prevents (h)'s positive
    # controls from passing off a classifier rewritten to always return "historical".
    # Preconditions are asserted explicitly so this control cannot silently degrade if a
    # future edit adds the synthetic path to HISTORICAL_EXEMPT_FILES.
    _synthetic_path = "docs/does-not-exist-synthetic-headline-check.md"
    _synthetic_line = f"This is a synthetic current-fact line: {_prose}"
    if _synthetic_path in HISTORICAL_EXEMPT_FILES:
        print(
            "  HEADLINE-LOCK FAIL: (i) precondition violated — synthetic path is in "
            "HISTORICAL_EXEMPT_FILES"
        )
        wrong_results.append("HEADLINE-LOCK: (i) precondition violated (whole-file)")
    elif "→" in _synthetic_line or "->" in _synthetic_line:
        print(
            "  HEADLINE-LOCK FAIL: (i) precondition violated — synthetic line contains an "
            "arrow"
        )
        wrong_results.append("HEADLINE-LOCK: (i) precondition violated (arrow)")
    elif _is_historical_headline_hit(_synthetic_path, _synthetic_line):
        print(
            "  HEADLINE-LOCK FAIL: (i) classifier called a non-exempt, no-arrow line "
            "historical — classifier is vacuous or over-broad"
        )
        wrong_results.append("HEADLINE-LOCK: (i) classifier non-vacuity control did not fail")
    else:
        print(
            "  HEADLINE-LOCK PASS: (i) classifier correctly rejects a non-exempt, no-arrow "
            "line as historical — non-vacuous"
        )

    def _unregistered_headline_finding(
        relpath: str, hit: tuple[int, str]
    ) -> tuple[bool, str]:
        """The (j) scan's per-hit decision, shared by the real scan below and its (k)
        non-vacuity control — a control exercising a parallel copy would prove nothing
        (research Pitfall 4). Returns (is_finding, message-or-empty-string).

        A hit is a finding only if BOTH of these hold: `_is_historical_headline_hit()`
        classifies it non-historical, AND `relpath` is absent from
        COVERED_HEADLINE_SURFACES. Gating the decision behind the classifier first is what
        proves the scan cannot false-positive on a correctly historical or delta statement
        (T-10-07) — HEADLINE-05's documented dependency on HEADLINE-03 is enforced by this
        function calling the classifier directly, not by convention.
        """
        _lineno, _line = hit
        if _is_historical_headline_hit(relpath, _line):
            return False, ""
        if relpath in COVERED_HEADLINE_SURFACES:
            return False, ""
        return True, (
            f"{relpath}:{_lineno} states the current headline as a non-historical "
            "occurrence but is not registered in COVERED_HEADLINE_SURFACES"
        )

    # (i2) Adjacency-specific controls (CR-03). A mermaid edge and an HTML comment
    # terminator sharing a line with the current headline must NOT exempt that line from
    # being reported as an unregistered-surface finding (the fail-unsafe case CR-03 names —
    # docs/COMPONENT-DIAGRAM.md is live proof mermaid-heavy docs and headline statements
    # coexist), while a genuine delta line still must be exempt, proving the narrowing did
    # not simply disable the arrow layer. Every control drives through
    # _unregistered_headline_finding(), the SAME decision function (j) and (k) call, never
    # a parallel copy. Writes nothing to disk.
    _i2_path = "docs/synthetic-adjacency-check.md"
    if _i2_path in COVERED_HEADLINE_SURFACES or _i2_path in HISTORICAL_EXEMPT_FILES:
        print(
            "  HEADLINE-LOCK FAIL: (i2) precondition violated — synthetic path is "
            "registered or whole-file exempt"
        )
        wrong_results.append("HEADLINE-LOCK: (i2) precondition violated")
    else:
        print(
            f"  HEADLINE-LOCK PASS: (i2) precondition — {_i2_path} is absent from both "
            "COVERED_HEADLINE_SURFACES and HISTORICAL_EXEMPT_FILES"
        )

        # 1. Mermaid edge is NOT exempt.
        _i2_mermaid_line = f"NODE_A --> NODE_B carrying {_prose}"
        _i2_mermaid_finding, _i2_mermaid_msg = _unregistered_headline_finding(
            _i2_path, (1, _i2_mermaid_line)
        )
        if _i2_mermaid_finding and _i2_path in _i2_mermaid_msg:
            print(
                "  HEADLINE-LOCK PASS: (i2) a mermaid edge sharing a line with the current "
                "headline is reported as a finding — not exempt"
            )
        else:
            print(
                "  HEADLINE-LOCK FAIL: (i2) a mermaid edge sharing a line with the current "
                "headline was NOT reported as a finding"
            )
            wrong_results.append("HEADLINE-LOCK: (i2) mermaid edge non-exemption failed")

        # 2. HTML comment terminator is NOT exempt — the exact CR-03 reproduction, promoted
        # into a permanent control.
        _i2_html_line = f"See -->  {_prose}"
        _i2_html_finding, _i2_html_msg = _unregistered_headline_finding(
            _i2_path, (1, _i2_html_line)
        )
        if _i2_html_finding and _i2_path in _i2_html_msg:
            print(
                "  HEADLINE-LOCK PASS: (i2) an HTML comment terminator sharing a line with "
                "the current headline is reported as a finding — not exempt"
            )
        else:
            print(
                "  HEADLINE-LOCK FAIL: (i2) an HTML comment terminator sharing a line with "
                "the current headline was NOT reported as a finding"
            )
            wrong_results.append(
                "HEADLINE-LOCK: (i2) HTML comment terminator non-exemption failed"
            )

        # 3. A genuine delta line IS exempt — without this arm, controls 1 and 2 would pass
        # against a classifier that returns False unconditionally.
        _i2_delta_line = f"0/0/0/1 → {_slash}"
        _i2_delta_finding, _ = _unregistered_headline_finding(_i2_path, (1, _i2_delta_line))
        if not _i2_delta_finding:
            print(
                "  HEADLINE-LOCK PASS: (i2) a genuine delta line (superseded figure → "
                "current figure) is NOT reported as a finding — exempt as expected"
            )
        else:
            print(
                "  HEADLINE-LOCK FAIL: (i2) a genuine delta line was reported as a finding "
                "— the narrowing over-disabled the arrow layer"
            )
            wrong_results.append("HEADLINE-LOCK: (i2) delta-line exemption failed")

    # (j) Tree-wide unregistered-surface scan (HEADLINE-05). Collect files through the
    # shared _headline_scan_files() helper (also driven directly by block (l)'s
    # non-vacuity control) so glob expansion is never a parallel copy.
    _scan_files: list[Path] = _headline_scan_files(HEADLINE_SCAN_GLOBS)

    _scanned_count = 0
    _accounted_hits = 0
    _scan_ok = True
    _repo_root_resolved = REPO_ROOT.resolve()
    for _scan_path in _scan_files:
        if not _scan_path.is_file():
            continue
        _resolved_scan_path = _scan_path.resolve()
        if not _resolved_scan_path.is_relative_to(_repo_root_resolved):
            continue  # never follow a symlink resolving outside the repository
        try:
            _scan_text = _scan_path.read_text(encoding="utf-8")
        except UnicodeDecodeError as _decode_exc:
            print(
                f"  HEADLINE-LOCK FAIL: (j) {_scan_path} could not be decoded as UTF-8: "
                f"{_decode_exc}"
            )
            wrong_results.append(f"HEADLINE-LOCK: (j) {_scan_path} decode error")
            _scan_ok = False
            continue
        _scanned_count += 1
        _scan_relpath = _scan_path.relative_to(REPO_ROOT).as_posix()
        for _hit in _headline_hits(_scan_text):
            _is_finding, _finding_msg = _unregistered_headline_finding(_scan_relpath, _hit)
            if _is_finding:
                print(f"  HEADLINE-LOCK FAIL: (j) {_finding_msg}")
                wrong_results.append(f"HEADLINE-LOCK: (j) {_finding_msg}")
                _scan_ok = False
            elif not _is_historical_headline_hit(_scan_relpath, _hit[1]):
                _accounted_hits += 1

    # (j-floor) Coverage floor and accounted-hit floor (CR-01 fix): the scan must have
    # actually reached every registered-plus-exempt surface and accounted for at least one
    # non-historical hit per registered surface, or the PASS line below is vacuous — a
    # narrowed or emptied HEADLINE_SCAN_GLOBS must be caught here, not stay silently green.
    # Evaluated through the shared _headline_scan_floor_breaches() helper, before the PASS
    # branch, so the PASS line can never be reached vacuously.
    if _scan_ok:
        for _breach in _headline_scan_floor_breaches(_scan_files, _accounted_hits):
            print(f"  HEADLINE-LOCK FAIL: {_breach}")
            wrong_results.append(f"HEADLINE-LOCK: {_breach}")
            _scan_ok = False

    if _scan_ok:
        _reachable_surfaces = COVERED_HEADLINE_SURFACES | HISTORICAL_EXEMPT_FILES
        _scan_relpaths = {
            _p.relative_to(REPO_ROOT).as_posix() for _p in _scan_files if _p.is_file()
        }
        _reached_count = len(_reachable_surfaces & _scan_relpaths)
        print(
            f"  HEADLINE-LOCK PASS: (j) tree-wide scan covered {_scanned_count} files, "
            f"{_accounted_hits} non-historical occurrence(s) accounted for by registered "
            f"surfaces, both floors evaluated, {_reached_count} of "
            f"{len(_reachable_surfaces)} registered-plus-exempt paths reached"
        )

    # (k) Non-vacuity control for (j) (T-10-08). Preconditions are asserted explicitly so
    # this control cannot silently degrade into a tautology if a future edit changes a
    # constant. Writes nothing to disk — no tempfile, no fixture file, no touch of the tree.
    _synth_path = "docs/synthetic-unregistered-surface.md"
    _synth_line = f"This document states the coverage headline: {_prose}."
    if _synth_path in COVERED_HEADLINE_SURFACES:
        print(
            "  HEADLINE-LOCK FAIL: (k) precondition violated — synthetic path is in "
            "COVERED_HEADLINE_SURFACES"
        )
        wrong_results.append("HEADLINE-LOCK: (k) precondition violated (covered)")
    elif _synth_path in HISTORICAL_EXEMPT_FILES:
        print(
            "  HEADLINE-LOCK FAIL: (k) precondition violated — synthetic path is in "
            "HISTORICAL_EXEMPT_FILES"
        )
        wrong_results.append("HEADLINE-LOCK: (k) precondition violated (whole-file)")
    elif "→" in _synth_line or "->" in _synth_line:
        print(
            "  HEADLINE-LOCK FAIL: (k) precondition violated — synthetic line contains an "
            "arrow"
        )
        wrong_results.append("HEADLINE-LOCK: (k) precondition violated (arrow)")
    else:
        # Direction 1: the synthetic unregistered hit IS reported as a finding, naming the
        # synthetic path.
        _unreg_finding, _unreg_msg = _unregistered_headline_finding(
            _synth_path, (1, _synth_line)
        )
        # Direction 2: the SAME synthetic line attributed to a REGISTERED path is NOT
        # reported — otherwise the decision function would simply flag everything and the
        # scan's greenness on the live tree would be luck, not correctness.
        _registered_path = sorted(COVERED_HEADLINE_SURFACES)[0]
        _reg_finding, _ = _unregistered_headline_finding(_registered_path, (1, _synth_line))
        # Direction 3 (T-10-08 / ROADMAP criterion 5's "gated behind HEADLINE-03" clause):
        # a genuinely delta-shaped line — a fixed superseded figure, an arrow, then the
        # current slash rendering (built from the in-scope _slash local, never typed) — at
        # the SAME unregistered synthetic path, is NOT reported. This proves the scan is
        # gated behind the historical classifier and not merely a registered-surface
        # membership test. The left-hand figure is a fixed non-current placeholder; it is
        # not the headline and does not fall under the no-literal rule.
        _superseded_figure = "0/0/0/1"
        _delta_line = f"{_superseded_figure} → {_slash}"
        if not _is_historical_headline_hit(_synth_path, _delta_line):
            print(
                "  HEADLINE-LOCK FAIL: (k) precondition violated — the delta-shaped line "
                "is not classified historical, so direction 3 would prove nothing"
            )
            wrong_results.append("HEADLINE-LOCK: (k) precondition violated (delta-shaped)")
        else:
            _delta_finding, _ = _unregistered_headline_finding(_synth_path, (1, _delta_line))
            if (
                _unreg_finding
                and _synth_path in _unreg_msg
                and not _reg_finding
                and not _delta_finding
            ):
                print(
                    f"  HEADLINE-LOCK PASS: (k) synthetic unregistered surface {_synth_path} "
                    f"is reported as a finding, the same line at a registered surface is "
                    f"not, and a delta-shaped line at the same synthetic path is not — "
                    f"non-vacuous and gated behind HEADLINE-03"
                )
            else:
                print(
                    f"  HEADLINE-LOCK FAIL: (k) non-vacuity control for the tree-wide scan "
                    f"did not behave as expected (unregistered finding={_unreg_finding}, "
                    f"registered finding={_reg_finding}, delta-shaped finding="
                    f"{_delta_finding})"
                )
                wrong_results.append(
                    "HEADLINE-LOCK: (k) non-vacuity control did not behave as expected"
                )


def _run_self_test() -> None:
    """Run the inline artifact-resolution / schema / sentinel fixtures — no .planning/ reads required.

    Fixtures per PATTERNS.md §Required fixtures:
      (1) valid reproducible row → PASS
      (2) reproducible row with dangling file path → flagged
      (3) reproducible row with dangling catalog row → flagged
      (4) reproducible row with missing rubric anchor → flagged
      (5) audit-only row, no artifact link → PASS (valid state)
      (6) gap row with rationale, no artifact link → PASS (valid state; generic structural test)
      (7) row missing capability → flagged
      (8) row missing coverage_tier → flagged
      (9) scheduled row with resolvable artifact link → PASS (WR-02/D-02/Phase 90)
      (10) DISTRIBUTION-FOLD: render_matrix_markdown on synthetic 2-repro+1-scheduled set;
           asserts bullets sum to len(rows), (incl. 1 scheduled) annotation present,
           folded count strictly > bare reproducible count (WR-01 fold lock / TRACE-03)

    Named sentinels:
      GEN-01-REPRODUCIBLE: live tier assertion (reproducible) + not-scheduled counter-check
                           + drift guard + deep-resolve of tests/step0-baseline-v7.6.md
                           (D-09/Phase 93; repurposed from GEN-01-SCHEDULED Phase 88;
                           artifact bumped v6.4->v7.4 Phase 108; bumped v7.4->v7.6 Phase 114)
      GEN-02-RUNBOOK: live tier assertion + counter-check + drift guard + dual-file existence
                      check (runbook + wrapper) (D-03/Phase 89)
      V79-ROWS: live row count + bare_id set + reproducible-tier + deep-resolve + RECON-01
                positive counter-check (D-01 / Phase 123); locks all 8 v7.9 milestone rows
                against silent drift; no live claude session required.
      V818-ROWS: live row count + bare_id set + ID-pinned 21/2 tier partition + deep-resolve
                 over reproducible rows only + HARN-04 positive counter-check + milestone/key
                 attribution lock + capability lock (D-07 / Phase 4); locks all 23 v8.18
                 milestone rows against silent drift, including a tier swap between two
                 named IDs that a blanket count assert would miss; no live claude session
                 required.
      V824-ROWS: live row count + bare_id set + ID-pinned 14/1 tier partition + deep-resolve
                 over reproducible rows only + GATE-03 positive counter-check + milestone/key
                 attribution lock + capability lock (D-09 / Phase 6); locks all 15 v8.24
                 milestone rows against silent drift, including a tier swap between two
                 named IDs that a blanket count assert would miss; no live claude session
                 required.
      HEADLINE-LOCK: ties the published coverage headline in
                 docs/requirements-traceability.md, and both tracked artifacts
                 (docs/requirements-matrix.md, docs/data/matrix.json), back to
                 build_matrix_rows() — with non-vacuity controls on both comparisons
                 (WR-08 / Phase 4 review). Closes the drift class that produced that
                 review's own CR-01, which was corrected by hand with the mechanism
                 left intact. All four headline figures are derived live, gap included.
    """
    wrong_results: list[str] = []
    _self_test_valid_rows_fixtures(wrong_results)
    _self_test_dangling_fixtures(wrong_results)
    _self_test_schema_fixtures(wrong_results)
    _self_test_pyanchor_resolver(wrong_results)
    _self_test_v79_rows_sentinel(wrong_results)
    _self_test_v818_rows_sentinel(wrong_results)
    _self_test_v824_rows_sentinel(wrong_results)
    _self_test_headline_lock(wrong_results)
    if wrong_results:
        sys.stderr.write(
            f"check-traceability --self-test: FAIL — {', '.join(wrong_results)}\n"
        )
        sys.exit(1)
    print("check-traceability --self-test: PASS")


# ---------------------------------------------------------------------------
# Subcommand handlers
# ---------------------------------------------------------------------------


def _run_emit(md_output: Path, json_output: Path) -> None:
    """Handler for the emit subcommand."""
    rows = build_matrix_rows()
    emit_matrix(rows, md_output, json_output)
    print(
        f"check-traceability emit: PASS — {len(rows)} rows written to "
        f"{md_output} + {json_output}"
    )


def _run_check(input_path: Path) -> None:
    """Handler for the check subcommand."""
    rows = load_rows(input_path)
    issues = check_consistency(rows)
    if issues:
        for issue in issues:
            sys.stderr.write(f"check-traceability check: ISSUE — {issue}\n")
        sys.exit(1)
    print(
        f"check-traceability check: PASS — {len(rows)} rows consistent"
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "TRACE-01..TRACE-03 / GAP-01 gate: traceability matrix emitter + "
            "consistency gate (stdlib-only)."
        )
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help=(
            "run the inline fixtures + named sentinels (no .planning/ reads required); "
            "exit 0 only if all pass (CI gate entry point)"
        ),
    )
    subparsers = parser.add_subparsers(dest="subcommand")

    emit_parser = subparsers.add_parser(
        "emit",
        help="Write MATRIX.md + matrix.json from build_matrix_rows()",
    )
    emit_parser.add_argument(
        "--md-output",
        type=Path,
        required=True,
        help="Path for requirements-matrix.md (must be under .planning/ or docs/; T-82-01)",
    )
    emit_parser.add_argument(
        "--json-output",
        type=Path,
        required=True,
        help="Path for matrix.json (must be under .planning/ or docs/; T-82-01)",
    )

    check_parser = subparsers.add_parser(
        "check",
        help="Validate matrix.json for consistency (D-08)",
    )
    check_parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Path to matrix.json to validate",
    )

    args = parser.parse_args()
    _require_python_version()

    if args.self_test:
        _run_self_test()
        return

    if args.subcommand == "emit":
        _run_emit(args.md_output, args.json_output)
    elif args.subcommand == "check":
        _run_check(args.input)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
