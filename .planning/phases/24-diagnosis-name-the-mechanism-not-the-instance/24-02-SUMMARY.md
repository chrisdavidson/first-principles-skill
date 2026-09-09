---
phase: 24-diagnosis-name-the-mechanism-not-the-instance
plan: 02
subsystem: docs
tags: [claim-containment, prose-01, gen-gate-docs, diagnosis]
dependency_graph:
  requires: []
  provides:
    - "docs/v9.1-claim-containment-diagnosis.md § banner, self-discipline, method, section skeleton"
    - "docs/v9.1-claim-containment-diagnosis.md § 1. The mechanism"
  affects:
    - "24-03 (Appendix A), 24-04 (§2), 24-05 (§3), 24-06 (§§4-6) — all append into the same file's fixed section skeleton"
tech_stack:
  added: []
  patterns:
    - "Symbol-anchor citation + re-derivation command, never bare file:line (CR-03's own defect class)"
    - "Live invocation via importlib.util.spec_from_file_location, registered in sys.modules before exec_module"
key_files:
  created:
    - docs/v9.1-claim-containment-diagnosis.md
  modified: []
decisions: []
metrics:
  duration_minutes: null
  completed: 2026-09-09
---

# Phase 24 Plan 02: Diagnosis page — banner, discipline, method, and the mechanism Summary

One-liner: Created `docs/v9.1-claim-containment-diagnosis.md` and wrote its section 1, deriving —
by live invocation, not assertion — why `_CITATION_SHAPE_RES`'s measured-transition-vector
exemption makes a stale chain terminus indistinguishable from a current one to containment.

## What was built

**Task 1 — page skeleton.** `docs/v9.1-claim-containment-diagnosis.md` was created with:

- A banner naming the page a dated diagnosis (not a standing governing record — deliberately does
  not copy `docs/v8.7-constraint-teardown.md`'s "no expiry" wording).
- `## How this page disciplines its own quantity claims` — states, in writing, the four-part
  discipline this page follows (frozen dated measurements; point at generated facts, never
  restate; the disclosed no-gate bound, re-derived live rather than assumed; the two rejected
  fix-options named per D-02). The disclosed bound was re-derived at write time:
  `/usr/bin/grep -n "v9.1-claim-containment-diagnosis" scripts/gen-gate-docs.py` exits 1 (no
  match — this page is not a `LITERAL_SCAN_MD_GLOBS` member), and
  `_generated_marker_pairs_for("docs/v9.1-claim-containment-diagnosis.md")` returns `()`.
- `## Method` — records the date (2026-09-09), the commit read against (`b937b3c`, working tree
  clean), the four re-derivation tools used across the page, and the citation convention (symbol
  anchor + re-derivation command, never bare `file:line`).
- The seven fixed section headings (`## 1. The mechanism` through `## Appendix A`), each carrying
  a one-line placeholder naming the plan that fills it, so plans 24-03 through 24-06 append
  without collision.

**Task 2 — section 1, the mechanism (PROSE-01).** Filled `## 1. The mechanism` with five
sub-sections:

- **1.1** Quotes `_CITATION_SHAPE_RES`'s measured-transition vector pattern verbatim
  (`re.compile(r"\d[\d,]*\s*(?:→|-->|->)\s*\d[\d,]*")`) with its re-derivation grep, and states the
  exemption is correct in intent (prose must narrate a quantity's history) and wrong in extent.
- **1.2** Names `_strip_citation_shaped_numbers` as the span-deletion site — the whole `N → M` run,
  arrow and both operands, replaced by a single space before `_normalise_numbers` runs — and
  derives that a stated history is a chain of hop matches consuming every number including the
  terminus. Names `detail_page_containment_problems`'s sole call site (`DETAIL_PAGE_DIR in
  path.parents`, `cmd_check()`), which scopes containment to `docs/gates/*.md` only.
- **1.3** States the destroyed distinction: a chain whose final value has gone stale is
  bit-for-bit indistinguishable, to this scanner, from one whose final value is current.
- **1.4** Proves the blindness on the live tree by direct invocation (not by reading), recorded
  below and matched verbatim on the page.
- **1.5** Accounts for all four recorded self-instances of the defect class, none linked into
  `.planning/` (described in prose instead, since VAL-03 link-checks the page against a fresh
  clone that does not contain `.planning/`).

## Live invocation output (recorded on the page, reproduced here)

Run 2026-09-09 against commit `b937b3c`, working tree clean:

```
path.stem='CONF-SURFACE' in NARRATIVE_ENTRIES=True check_spelled_out=False
CONF-SURFACE.md containment problems: []
all-gates sweep: 31 pages scanned, 0 containment problems found
```

`python3 scripts/gen-gate-docs.py --check` exited `0`. This confirms containment reports zero
problems on `docs/gates/CONF-SURFACE.md` despite its live `182 → 184` deferred-ledger growth
narrative sitting against the actual `_DEFERRED_LEDGER_MAX = 181` (`scripts/gen-gate-docs.py`) —
the stale terminus escapes detection exactly as section 1 derives.

## Verification performed (observed, not assumed)

- `python3 scripts/check-links.py` — ran twice (after each task): `check-links: PASS (314
  markdown links + 6 namespace refs across 161 files)`, exit 0 both times.
- `python3 scripts/gen-gate-docs.py --check` — ran twice: `harvested 22/22 expected script-backed
  entries (22 total)`, exit 0 both times.
- `/usr/bin/grep -c "^## 1\. The mechanism\|^## 2\. The sibling census\|^## 3\. Dispositions\|^##
  4\. Out of scope\|^## 5\. The four self-referential tests\|^## 6\. Verdicts on RATCHET\|^##
  Appendix A" docs/v9.1-claim-containment-diagnosis.md` → `7`.
- `/usr/bin/grep -c "_CITATION_SHAPE_RES\|_strip_citation_shaped_numbers\|_normalise_numbers\|detail_page_containment_problems"
  docs/v9.1-claim-containment-diagnosis.md` → `8` (≥ 4 required).
- `/usr/bin/grep -c "](\.\./\.planning\|](\.planning" docs/v9.1-claim-containment-diagnosis.md` →
  `0`.
- `wc -l docs/v9.1-claim-containment-diagnosis.md` → `262` (≥ 90 required).
- `git diff --stat` for task 2 touched `docs/v9.1-claim-containment-diagnosis.md` only.
- `git diff --name-only b937b3c HEAD` (whole plan) → `docs/v9.1-claim-containment-diagnosis.md`
  only.
- `bash scripts/check-firewall-battery.sh` → `FIREWALL: BLOCKED (1 prerequisite(s) unmet; 25/26
  passed)`. The single non-passing row is `[PREREQ] VAL-03 — no pytest-capable interpreter found`
  (no `.venv`, `python3` cannot `import pytest`), a pre-existing environment condition unrelated
  to this plan's changes and distinct from a genuine gate failure per `CLAUDE.md`'s SHIP-06
  convention (`BLOCKED`, exit 2, vs. `RED`, exit 1). All 25 gates that did run, including
  CONF-SURFACE (`gen-gate-docs.py --self-test + --check`), reported `[PASS]`.

## Deviations from Plan

None — plan executed exactly as written. Both tasks' `<verify>` and `<acceptance_criteria>` blocks
were run and matched.

## Assumption Drift (advisory)

None material. The plan's action text described the section-2..6/Appendix-A placeholders only as
"a one-line placeholder naming the plan that fills it" without specifying which plan number fills
which heading; the actual plan-to-section mapping was derived from reading each of 24-03 through
24-06's own `<objective>` blocks (24-03 → Appendix A, 24-04 → §2, 24-05 → §3, 24-06 → §§4-6) rather
than assumed, and recorded in the placeholders exactly as derived.

## Self-Check: PASSED

- `docs/v9.1-claim-containment-diagnosis.md` — FOUND (created, 262 lines).
- Commit `19ada6d` (task 1) — FOUND in `git log --oneline`.
- Commit `f4b7200` (task 2) — FOUND in `git log --oneline`.
- Post-commit deletion check (`git diff --diff-filter=D --name-only`) — no deletions on either
  commit.
- `git status --short` — clean after both commits.
