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
        --md-output .planning/phases/82-.../MATRIX.md \\
        --json-output .planning/phases/82-.../matrix.json
    python3 scripts/check-traceability.py check \\
        --input .planning/phases/82-.../matrix.json

Exit codes:
    0  all fixtures pass (--self-test) or subcommand completes cleanly
    1  fixture mismatch or consistency failure
    2  environment error (Python <3.12) or path confinement violation

--self-test: runs 8 in-process fixtures (no disk I/O beyond checking that
             known-present repo files exist) and exits 0 only if all pass.
             This is the CI gate entry point (TRACE-03 + STEP0-08 pattern).

emit: writes MATRIX.md + matrix.json from build_matrix_rows(); both paths
      must be under .planning/ (T-82-01 path-confinement guard).

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
VALID_TIERS: set[str] = {"reproducible", "audit-only", "gap"}


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
    coverage_tier: str    # "reproducible" | "audit-only" | "gap"
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
    """D-05 path (b): 7 active-tail gap rows — included unconditionally.

    These 7 residuals are exempt from the deliverable-existence gate. They
    use deliverable_path='active-tail' and coverage_tier='gap'. They are the
    primary GAP-01 findings.

    Key form: v5.3/GEN-01 and v5.3/GEN-02 carry the canonical v5.3 milestone
    prefix. S-N04, RR-79-01/02/03, and RR-77-08 are non-milestone residuals
    that use the _RESIDUAL_KEY_PREFIX (confirmed at Task 3 checkpoint, 82-02).
    """
    p = _RESIDUAL_KEY_PREFIX  # e.g. "residual" — confirmed Task 3 checkpoint
    tail_rationale_sn04 = (
        "Negative-control over-routing dip recorded in tests/step0-baseline-v5.3.md "
        "(S-N04 2/5 pass rate); no RR-ID assigned; no owning phase; not in any "
        "milestone REQUIREMENTS checkbox. Synthetic residual/ qualifier confirmed "
        "at Task 3 checkpoint (82-02, 2026-06-14)."
    )
    tail_rationale_gen01 = (
        "Full Step 0 classifier rearchitecture; perpetually deferred "
        "(v5.1->v5.2->v5.3->v6.0+); no confirming phase. "
        "STATE.md carry_forward to v6.0+."
    )
    tail_rationale_gen02 = (
        "Periodic live monitoring cadence; perpetually deferred; no confirming phase. "
        "STATE.md carry_forward to v6.0+."
    )
    tail_rationale_rr7901 = (
        "S-P01 honest carry-forward (Phase 79): no false-positive-safe marker "
        "cleared D-08 evidence bar across 5 v5.2 captures; "
        "'Bottom line' framing has zero technique markers. RETROSPECTIVE.md Phase 79."
    )
    tail_rationale_rr7902 = (
        "S-P02 honest carry-forward (Phase 79): zero canonical inversion vocabulary "
        "in all five v5.2 captures. RETROSPECTIVE.md Phase 79."
    )
    tail_rationale_rr7903 = (
        "S-P05 honest carry-forward (Phase 79): only 'trade-off analysis' cleared "
        "D-08 but D-04 requires two distinct markers. RETROSPECTIVE.md Phase 79."
    )
    tail_rationale_rr7708 = (
        "Warning residual: CEILING=4 vs expected=3 deviation caused by incidental "
        "\\bVerdict\\b IGNORECASE match in composer_hits. Not a blocking defect but "
        "not resolved. RETROSPECTIVE.md Phase 77 (RR-77-08)."
    )
    return [
        MatrixRow(f"{p}/S-N04", "S-N04", p, "Test-Network",
                  "active-tail", "gap", "", tail_rationale_sn04),
        MatrixRow("v5.3/GEN-01", "GEN-01", "v5.3", "Test-Network",
                  "active-tail", "gap", "", tail_rationale_gen01),
        MatrixRow("v5.3/GEN-02", "GEN-02", "v5.3", "Test-Network",
                  "active-tail", "gap", "", tail_rationale_gen02),
        MatrixRow(f"{p}/RR-79-01", "RR-79-01", p, "Test-Network",
                  "active-tail", "gap", "", tail_rationale_rr7901),
        MatrixRow(f"{p}/RR-79-02", "RR-79-02", p, "Test-Network",
                  "active-tail", "gap", "", tail_rationale_rr7902),
        MatrixRow(f"{p}/RR-79-03", "RR-79-03", p, "Test-Network",
                  "active-tail", "gap", "", tail_rationale_rr7903),
        MatrixRow(f"{p}/RR-77-08", "RR-77-08", p, "Test-Network",
                  "active-tail", "gap", "", tail_rationale_rr7708),
    ]


def build_matrix_rows() -> list[MatrixRow]:
    """Return the curated list of MatrixRow objects (Plan 02 — fully populated).

    Two inclusion paths per D-05:
    (a) Live-shipping requirements — deliverable-gated (D-01/D-02/D-03).
        Grouped by capability (D-04): Methodology first, then Test-Network.
    (b) Active tail (7 rows) — included unconditionally, tagged gap (D-05b).

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
# Path-confinement guard (T-82-01; reused verbatim from check-inventory.py)
# ---------------------------------------------------------------------------


def _resolve_confined_output(path: Path) -> Path:
    """Resolve path and enforce T-82-01: must be under REPO_ROOT/.planning/.

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
            f"check-traceability: --output path must be under .planning/ "
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
      - for reproducible rows: artifact_link must resolve via _resolve_artifact
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
        if row.coverage_tier == "reproducible":
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
    "S-N04":    "CRITICAL",   # negative-control regression in step0-baseline
    "GEN-01":   "CRITICAL",   # Test-Network integrity (classifier rearchitecture)
    "GEN-02":   "HIGH",       # measurement cadence unestablished (periodic live)
    "RR-79-01": "HIGH",       # live S-P routing unresolved
    "RR-79-02": "HIGH",       # live S-P routing unresolved
    "RR-79-03": "HIGH",       # live S-P routing unresolved
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
    """Render the matrix as a Markdown string (list[str] → join pattern)."""
    reproducible = [r for r in rows if r.coverage_tier == "reproducible"]
    audit_only = [r for r in rows if r.coverage_tier == "audit-only"]
    gap = [r for r in rows if r.coverage_tier == "gap"]
    uncovered = audit_only + gap

    lines: list[str] = []
    lines.append("# Traceability Matrix — Phase 82")
    lines.append("")
    lines.append(
        "> Generated by: "
        "`python3 scripts/check-traceability.py emit --md-output ... --json-output ...`"
    )
    lines.append("")
    lines.append("## Coverage Distribution")
    lines.append(f"- reproducible: {len(reproducible)}")
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
    """Run 8 inline fixtures — no .planning/ reads required.

    Fixtures per PATTERNS.md §Required fixtures:
      (1) valid reproducible row → PASS
      (2) reproducible row with dangling file path → flagged
      (3) reproducible row with dangling catalog row → flagged
      (4) reproducible row with missing rubric anchor → flagged
      (5) audit-only row, no artifact link → PASS (valid state)
      (6) gap row with rationale, no artifact link → PASS (valid state)
      (7) row missing capability → flagged
      (8) row missing coverage_tier → flagged
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
            "run 8 inline fixtures (no .planning/ reads); "
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
        help="Path for MATRIX.md (must be under .planning/; T-82-01)",
    )
    emit_parser.add_argument(
        "--json-output",
        type=Path,
        required=True,
        help="Path for matrix.json (must be under .planning/; T-82-01)",
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
