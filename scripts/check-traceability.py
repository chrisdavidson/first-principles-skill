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
        --json-output .planning/phases/82-traceability-matrix-and-gap-findings/matrix.json
    python3 scripts/check-traceability.py check \\
        --input .planning/phases/82-.../matrix.json

Exit codes:
    0  all fixtures pass (--self-test) or subcommand completes cleanly
    1  fixture mismatch or consistency failure
    2  environment error (Python <3.12) or path confinement violation

--self-test: runs 10 in-process fixtures + named sentinels (no disk I/O beyond
             checking known-present repo files) and exits 0 only if all pass.
             This is the CI gate entry point (TRACE-03 + STEP0-08 pattern).

emit: writes MATRIX.md + matrix.json from build_matrix_rows(); both paths
      must be under .planning/ or docs/ (T-82-01 path-confinement guard).

check: reads matrix.json, validates every row has a valid capability and
       coverage_tier, and deep-resolves every reproducible artifact_link (D-08).
"""

import argparse
import json
import sys
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
                  "reproducible",
                  "scripts/git-hooks/pre-commit", ""),
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
        MatrixRow("v3.8/EVAL-01", "EVAL-01", "v3.8", "Methodology",
                  "scripts/check-focused-output.py",
                  "audit-only", "", audit_v38),
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


def _rows_methodology_builder() -> list[MatrixRow]:
    """v4.0 CLI + v4.1 INST builder rows — Methodology."""
    audit_v40 = "Validated by v4.0-MILESTONE-AUDIT; no re-runnable gate"
    audit_v41 = "Validated by v4.1-MILESTONE-AUDIT; no re-runnable gate"
    return [
        MatrixRow("v4.0/CLI-01", "CLI-01", "v4.0", "Methodology",
                  "main.py", "audit-only", "", audit_v40),
        MatrixRow("v4.0/CLI-02", "CLI-02", "v4.0", "Methodology",
                  "main.py", "audit-only", "", audit_v40),
        MatrixRow("v4.0/CLI-03", "CLI-03", "v4.0", "Methodology",
                  "main.py", "audit-only", "", audit_v40),
        MatrixRow("v4.0/CLI-04", "CLI-04", "v4.0", "Methodology",
                  "main.py", "audit-only", "", audit_v40),
        MatrixRow("v4.0/CLI-05", "CLI-05", "v4.0", "Methodology",
                  "main.py", "audit-only", "", audit_v40),
        MatrixRow("v4.0/CLI-06", "CLI-06", "v4.0", "Methodology",
                  "main.py", "audit-only", "", audit_v40),
        MatrixRow("v4.0/CLI-07", "CLI-07", "v4.0", "Methodology",
                  "main.py", "audit-only", "", audit_v40),
        MatrixRow("v4.0/CLI-08", "CLI-08", "v4.0", "Methodology",
                  "main.py", "audit-only", "", audit_v40),
        MatrixRow("v4.1/INST-01", "INST-01", "v4.1", "Methodology",
                  "main.py",
                  "reproducible", "tests/test_64_01_install.py", ""),
        MatrixRow("v4.1/INST-02", "INST-02", "v4.1", "Methodology",
                  "main.py",
                  "reproducible", "tests/test_64_01_install.py", ""),
        MatrixRow("v4.1/INST-03", "INST-03", "v4.1", "Methodology",
                  "main.py",
                  "reproducible", "tests/test_64_01_install.py", ""),
        MatrixRow("v4.1/INST-04", "INST-04", "v4.1", "Methodology",
                  "main.py",
                  "reproducible", "tests/test_64_01_install.py", ""),
        MatrixRow("v4.1/INST-05", "INST-05", "v4.1", "Methodology",
                  "main.py",
                  "reproducible", "tests/test_64_01_install.py", ""),
        MatrixRow("v4.1/INST-06", "INST-06", "v4.1", "Methodology",
                  "main.py", "audit-only", "",
                  "Validated by v4.1-MILESTONE-AUDIT; README documented; no re-runnable gate"),
        MatrixRow("v4.1/INST-07", "INST-07", "v4.1", "Methodology",
                  "main.py",
                  "reproducible", "tests/test_64_01_install.py", ""),
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
    classifier capability is now reproducibly measured by the committed v6.3 live
    re-baseline (tests/step0-baseline-v6.3.md, Phase 92). Earned by the committed
    baseline, not a passing score (BATTERY: FAIL, 2/4 residuals carried — honest
    v6.3 success state). GEN-02 has been converted to coverage_tier='reproducible'
    (runbook + wrapper script, Phase 89) and no longer belongs to the open-gap set.

    Key form: v5.3/GEN-01 and v5.3/GEN-02 carry the canonical v5.3 milestone
    prefix. RR-80-01, RR-79-01, RR-92-01, RR-92-02, and RR-77-08 are non-milestone
    residuals that use the _RESIDUAL_KEY_PREFIX (confirmed at Task 3 checkpoint,
    82-02). RR-92-01 supersedes RR-79-02 (Phase 92 v6.3 carry-forward, S-P02
    inversion); RR-92-02 supersedes RR-79-03 (Phase 92 v6.3 carry-forward, S-P05
    trade-off).
    """
    p = _RESIDUAL_KEY_PREFIX  # e.g. "residual" — confirmed Task 3 checkpoint
    tail_rationale_gen01 = (
        "Full Step 0 classifier rearchitecture (GEN-01-REARCH, Phases 91-93). "
        "GEN-01 is now reproducible: the Step 0 classifier capability is reproducibly "
        "measured by the committed v6.3 live re-baseline (Phase 92). Earned by the "
        "committed baseline, not a passing score (BATTERY: FAIL, 2/4 residuals carried "
        "— legitimate v6.3 success state). Confirming artifact: tests/step0-baseline-v6.3.md."
    )
    tail_rationale_gen02 = (
        "Runbook + wrapper script established (Phase 89). Cadence: milestone boundary + "
        "detector-surface changes. See docs/live-monitoring-runbook.md."
    )
    return [
        MatrixRow(f"{p}/RR-80-01", "RR-80-01", p, "Test-Network",
                  "active-tail", "reproducible", "scripts/_battery_core.py#self_test_boundary", ""),
        MatrixRow("v5.3/GEN-01", "GEN-01", "v5.3", "Test-Network",
                  "active-tail", "reproducible", "tests/step0-baseline-v6.3.md",
                  tail_rationale_gen01),
        MatrixRow("v5.3/GEN-02", "GEN-02", "v5.3", "Test-Network",
                  "active-tail", "reproducible", "docs/live-monitoring-runbook.md",
                  tail_rationale_gen02),
        MatrixRow(f"{p}/RR-79-01", "RR-79-01", p, "Test-Network",
                  "active-tail", "reproducible", "scripts/_battery_core.py#self_test_boundary", ""),
        # RR-92-01 supersedes RR-79-02 (Phase 92 v6.3 carry-forward, S-P02 inversion CARRIED 0/5)
        MatrixRow(f"{p}/RR-92-01", "RR-92-01", p, "Test-Network",
                  "active-tail", "reproducible", "scripts/_battery_core.py#self_test_boundary", ""),
        # RR-92-02 supersedes RR-79-03 (Phase 92 v6.3 carry-forward, S-P05 trade-off CARRIED 1/5)
        MatrixRow(f"{p}/RR-92-02", "RR-92-02", p, "Test-Network",
                  "active-tail", "reproducible", "scripts/_battery_core.py#self_test_boundary", ""),
        MatrixRow(f"{p}/RR-77-08", "RR-77-08", p, "Test-Network",
                  "active-tail", "reproducible", "scripts/_battery_core.py#self_test_boundary", ""),
    ]


def build_matrix_rows() -> list[MatrixRow]:
    """Return the curated list of MatrixRow objects (Plan 02 — fully populated).

    Two inclusion paths per D-05:
    (a) Live-shipping requirements — deliverable-gated (D-01/D-02/D-03).
        Grouped by capability (D-04): Methodology first, then Test-Network.
    (b) Active tail (7 rows) — included unconditionally; all reproducible (D-05b):
        GEN-01 reproducible (Phase 93 flip, v6.3 baseline earned), GEN-02 + 5
        residuals reproducible. RR-92-01/02 supersede RR-79-02/03 (Phase 92).

    The 'residual/' key prefix for non-milestone residuals is confirmed
    (Task 3 checkpoint, 82-02). See _RESIDUAL_KEY_PREFIX for the change point.
    """
    rows: list[MatrixRow] = []
    # --- Methodology capability ---
    rows.extend(_rows_methodology_agent())
    rows.extend(_rows_methodology_agent_cont())
    rows.extend(_rows_methodology_rigor())
    rows.extend(_rows_methodology_focused_stubs())
    rows.extend(_rows_methodology_builder())
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
        # Catalog-row form: anchor is a row ID like B-P12, S-P01, etc.
        # Rubric anchor: anchor is a slug like criterion-1-identify-essence.
        # Use plain substring membership (RESEARCH.md §Parenthetical gotcha:
        # avoid pipe-table split over content with | alternation characters).
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
    # GEN-01 removed — now "reproducible" (committed v6.3 live re-baseline, Phase 92)
    # GEN-02 removed — now "reproducible" (runbook + wrapper script, Phase 89)
    "RR-79-01": "HIGH",       # live S-P routing unresolved
    # RR-92-01 supersedes RR-79-02 (Phase 92 v6.3 carry-forward, S-P02 inversion CARRIED 0/5)
    "RR-92-01": "HIGH",       # live S-P routing unresolved
    # RR-92-02 supersedes RR-79-03 (Phase 92 v6.3 carry-forward, S-P05 trade-off CARRIED 1/5)
    "RR-92-02": "HIGH",       # live S-P routing unresolved
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
        " --json-output .planning/phases/82-traceability-matrix-and-gap-findings/matrix.json -->"
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
    # measured by the committed v6.3 live re-baseline (tests/step0-baseline-v6.3.md,
    # Phase 92). The flip is earned by the committed baseline, not a passing score
    # (BATTERY: FAIL, 2/4 residuals carried — legitimate v6.3 success state).
    # Asserts:
    #   (a) GEN-01's tier is "reproducible" (not "scheduled", not "gap")
    #   (b) GEN-01's artifact_link is the committed v6.3 baseline (deep-resolved)
    #   (c) Exactly-one GEN-01 row drift guard
    #   (d) Not-scheduled counter-check (transition non-vacuous)
    # Mirrors the Phase 84/85 RR-80-01 idiom: hardcoded named assertion +
    # positive counter-check + drift guard. No live claude session required.
    # No gitignored-file dependency (.planning/ROADMAP.md removed — ABSENT in CI).
    # Honesty-not-score (D-01): asserts the documented reproducible state, not a
    # live pass-rate. Any future revert of the tier, deletion of the GEN-01 row,
    # or removal of the v6.3 baseline file fails CI.
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
    # v6.3 baseline. Deep-resolve via _resolve_artifact (git-tracked, present in CI).
    _gen01_expected_artifact = "tests/step0-baseline-v6.3.md"
    if _gen01_artifact != _gen01_expected_artifact:
        print(
            f"  GEN-01-REPRODUCIBLE FAIL: artifact_link={_gen01_artifact!r} "
            f"(expected {_gen01_expected_artifact!r})."
        )
        wrong_results.append("GEN-01-REPRODUCIBLE: artifact_link not v6.3 baseline")
    else:
        _gen01_resolve_issues = _resolve_artifact(_gen01_artifact)
        # Belt-and-suspenders: explicit path existence check
        _gen01_baseline_path = REPO_ROOT / "tests" / "step0-baseline-v6.3.md"
        if _gen01_resolve_issues or not _gen01_baseline_path.exists():
            print(
                f"  GEN-01-REPRODUCIBLE FAIL: artifact deep-resolve failed for "
                f"{_gen01_artifact!r}: {_gen01_resolve_issues}; "
                f"file exists={_gen01_baseline_path.exists()}"
            )
            wrong_results.append("GEN-01-REPRODUCIBLE: v6.3 baseline not resolvable")
        else:
            print(
                f"  GEN-01-REPRODUCIBLE PASS: artifact_link={_gen01_artifact!r} "
                f"deep-resolves OK (tests/step0-baseline-v6.3.md exists, git-tracked)."
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


def _run_self_test() -> None:
    """Run 10 inline fixtures — no .planning/ reads required.

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
                           + drift guard + deep-resolve of tests/step0-baseline-v6.3.md
                           (D-09/Phase 93; repurposed from GEN-01-SCHEDULED Phase 88)
      GEN-02-RUNBOOK: live tier assertion + counter-check + drift guard + dual-file existence
                      check (runbook + wrapper) (D-03/Phase 89)
    """
    wrong_results: list[str] = []
    _self_test_valid_rows_fixtures(wrong_results)
    _self_test_dangling_fixtures(wrong_results)
    _self_test_schema_fixtures(wrong_results)
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
            "run 10 inline fixtures + named sentinels (no .planning/ reads required); "
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
