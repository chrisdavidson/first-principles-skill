---
phase: 19-false-negative-rate
plan: 02
subsystem: testing
tags: [adversarial-corpus, conf-07, prov-guard, quality-harness, false-negative-rate]

# Dependency graph
requires:
  - phase: 19-false-negative-rate (plan 01, same wave)
    provides: "the corpus directory and the 999.2 seed case (t01); this plan writes disjoint filenames in parallel"
provides:
  - "tests/adversarial-corpus-v9.0/t02-fabricated-read-at-source.md — the corpus's single stratum-B1 item"
  - "tests/adversarial-corpus-v9.0/t08-verdict-contradicts-its-type.md — stratum-B2 verdict/type incoherence"
  - "tests/adversarial-corpus-v9.0/t11-fabricated-ground-truth.md — stratum-B2 fabricated GT with no read-at-source label"
  - "tests/adversarial-corpus-v9.0/t14-order-of-magnitude-conversion.md — stratum-B2 100x unit-conversion error"
affects: [19-04-catalog-and-readme, 19-05-surface-extension, 999.4-semantic-claim-to-chain-correspondence]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Adversarial corpus items derived by surgical single-passage edit from a Phase-18 exemplar that already measures 0/0/0, preserving inherited form-cleanliness rather than re-earning it"

key-files:
  created:
    - tests/adversarial-corpus-v9.0/t02-fabricated-read-at-source.md
    - tests/adversarial-corpus-v9.0/t08-verdict-contradicts-its-type.md
    - tests/adversarial-corpus-v9.0/t11-fabricated-ground-truth.md
    - tests/adversarial-corpus-v9.0/t14-order-of-magnitude-conversion.md
  modified: []

key-decisions:
  - "t02's fabricated citation targets GT-4 (the L10 bearing-life figure) in science-engineering-2.md, keeping the ~130,000-hour headline unchanged everywhere else in the document and only replacing the source clause with a fabricated catalogue citation carrying *Provenance: read-at-source.* — zero other lines needed editing, since the approximate figure already tolerates the fabricated citation's more precise 131,850-hour instantiation"
  - "t11's fabricated GT (GT-4, engineering capacity) changes both the source (an invented 'Meridian Workforce Analytics' internal survey) and the figure (3.2 to 4.1 engineer-quarters), with the one dependent Assumptions Table cross-reference updated to match; explicitly carries no read-at-source label so it stays out of PROV-GUARD's reach and does not converge with t02"
  - "t08 targets personal-general-2.md's drawdown-tolerance row (Type: untested belief — diagnostic), rewriting only the Verdict and Verification cells so the conforming Accept — em-dash — justification form argues for accepting the belief precisely because it is untested, contradicting the row's own Treatment (verify by ruling out alternative diagnoses)"
  - "t14 targets software-systems.md's profiling-duration figure, carried through chain C3's first hop, the self-audit ledger table, and section 6's numbered plan — rewritten from ~1 day to ~14 minutes (a 1,440÷100 conversion slip), with every GT citation and chain shape left untouched"

requirements-completed: [CONF-07]

# Metrics
duration: 25min
completed: 2026-09-05
---

# Phase 19 Plan 02: Adversarial Corpus — B1 Provenance Item and Three B2 Breadth Items Summary

**Authored the corpus's single stratum-B1 item (a fabricated read-at-source ground truth reachable only by PROV-GUARD) plus three stratum-B2 items broadening the falsehood families no shipped instrument reaches — all four derived by surgical single-passage edit from Phase-18 exemplars, zero code touched.**

## Performance

- **Duration:** 25 min
- **Started:** 2026-09-05T12:52:00Z (approx, after worktree base correction)
- **Completed:** 2026-09-05
- **Tasks:** 2 completed
- **Files modified:** 4 created, 0 modified

## Accomplishments

- t02 and t11 (Task 1): the corpus's only B1 item (t02, PROV-GUARD-reachable fabricated read-at-source GT) and a B2 fabrication with no read-at-source label (t11) that deliberately does not converge with it.
- t08 and t14 (Task 2): a B2 verdict/Type incoherence probe and a B2 order-of-magnitude conversion probe, both fully form-clean under the frozen detector.

## Task Commits

Each task was committed atomically:

1. **Task 1: Author t02 (fabricated read-at-source GT) and t11 (fabricated GT, no provenance label)** — `5b42e45` (feat)
2. **Task 2: Author t08 (verdict contradicts its Type) and t14 (order-of-magnitude conversion error)** — `2371e91` (feat)

**Plan metadata:** committed alongside this SUMMARY (see final commit).

_No TDD tasks in this plan — both are `type="auto"`, pure content authoring._

## Files Created/Modified

- `tests/adversarial-corpus-v9.0/t02-fabricated-read-at-source.md` — copy of `shared/examples/science-engineering-2.md` with GT-4's L10-life source clause replaced by a fabricated SKF catalogue citation carrying `*Provenance: read-at-source.*`
- `tests/adversarial-corpus-v9.0/t11-fabricated-ground-truth.md` — copy of `shared/examples/product-business-2.md` with GT-4's engineering-capacity figure and source replaced by an invented internal survey, no read-at-source label
- `tests/adversarial-corpus-v9.0/t08-verdict-contradicts-its-type.md` — copy of `shared/examples/personal-general-2.md` with the drawdown-tolerance row's Verdict/Verification cells rewritten to Accept the untested belief on grounds that contradict its own Treatment
- `tests/adversarial-corpus-v9.0/t14-order-of-magnitude-conversion.md` — copy of `shared/examples/software-systems.md` with the profiling-duration figure rewritten from ~1 day to ~14 minutes (a 100x conversion slip) in chain C3, the self-audit ledger, and section 6

## Measurement Output (verbatim)

Run via the scratchpad `measure-corpus.py` module (loads `scripts/check-quality-harness.py` directly, never committed) against the worktree at `/home/chrisdavidson/Projects/first-principles-skill/.claude/worktrees/agent-ac31b49d9f90b08e6`:

```
t02-fabricated-read-at-source.md {'conclusion_claims': 3, 'untraced_claims': 0, 'verdict_cells': 8, 'nonconforming_verdict_cells': 0, 'chain_blocks': 2, 'malformed_chain_blocks': 0, 'dependency_cycles': 0, 'ungrounded_chains': 0, 'selfaudit_disagreements': 0}
t11-fabricated-ground-truth.md {'conclusion_claims': 4, 'untraced_claims': 0, 'verdict_cells': 7, 'nonconforming_verdict_cells': 0, 'chain_blocks': 3, 'malformed_chain_blocks': 0, 'dependency_cycles': 0, 'ungrounded_chains': 0, 'selfaudit_disagreements': 0}
t08-verdict-contradicts-its-type.md {'conclusion_claims': 7, 'untraced_claims': 0, 'verdict_cells': 8, 'nonconforming_verdict_cells': 0, 'chain_blocks': 3, 'malformed_chain_blocks': 0, 'dependency_cycles': 0, 'ungrounded_chains': 0, 'selfaudit_disagreements': 0}
t14-order-of-magnitude-conversion.md {'conclusion_claims': 8, 'untraced_claims': 0, 'verdict_cells': 6, 'nonconforming_verdict_cells': 0, 'chain_blocks': 3, 'malformed_chain_blocks': 0, 'dependency_cycles': 0, 'ungrounded_chains': 0, 'selfaudit_disagreements': 0}
```

Every reading is byte-identical to the plan's required substrate figures (`science-engineering-2.md` claims 3/cells 8/blocks 2; `product-business-2.md` claims 4/cells 7/blocks 3; `personal-general-2.md` claims 7/cells 8/blocks 3; `software-systems.md` claims 8/cells 6/blocks 3), all nine substantive/form columns zero on every item. None printed `UNREADABLE`.

**`_verdict_conforms` on t08's rewritten cell** (`"Accept — this is an untested belief, so it is taken at face value pending future work"`): `True` — confirmed by direct call against the unmodified detector.

## Falsehood Statements (for plan 19-04's `catalog.md`)

- **t02** (stratum B1, disposition: accept-with-reason naming PROV-GUARD): GT-4's stated source — a specific SKF bearing-catalogue table entry — is fabricated; no such datasheet backs the 131,850-hour figure. `detect_defects` reads clean because its nine provenance columns are hardcoded `"n/a"`; `scripts/check-provenance.py` is the one instrument that could falsify a `*Provenance: read-at-source.*` label against a real capture, and no paired `.jsonl` capture is shipped for this item (declined under 19-01's decision (d)/D-02 — would need a written CONF-08 amendment, a second run path, and ~236KB per capture).
- **t11** (stratum B2, disposition: accept-with-reason): GT-4's engineering-capacity figure and its attributed source (`"Meridian Workforce Analytics"`) are both invented; the fabrication carries no `read-at-source` label, so no shipped instrument — including PROV-GUARD — has a join to check it against. Distinguishes from t02 by design: the same fabrication family, reachable by nothing, dressed the way surrounding ordinary GTs are dressed.
- **t08** (stratum B2, disposition: accept-with-reason): the drawdown-tolerance row's Verdict reads `Accept` with a conforming em-dash justification, but that justification argues for acceptance precisely because the assumption is untested — the opposite of what its own `untested belief` Type and `Verify by ruling out alternative diagnoses` Treatment prescribe. No rule reaches it: `_verdict_conforms` checks token + em-dash + non-empty justification only, never cross-reads the Type column, and Criterion 2 of the rubric governs Verdict form, not its coherence with Type.
- **t14** (stratum B2, disposition: accept-with-reason): the profiling-duration figure carried through chain C3, the self-audit ledger, and section 6's numbered plan is wrong by two orders of magnitude — `~14 minutes` where the correct conversion of "1 engineering day" is 1,440 minutes, a 1,440÷100 slip. No numeric-plausibility check exists anywhere in the harness, so the item is expected to read fully clean; that is the measurement, not a defect to correct.

## Decisions Made

- Kept every edit surgical and confined to the smallest coherent unit (one GT bullet, or one Verdict/Verification cell pair, or one duration figure repeated at its three points of appearance) rather than touching chain heads, arrows, or unrelated sections — matching 19-01's precedent and minimizing the risk of accidentally perturbing `_chain_block_well_formed` or `_conclusion_claims` counts.
- For t02, chose not to change the `~130,000 hours` headline figure anywhere in the document; the fabricated citation's more precise `131,850 hours` is presented as a specific instantiation of the existing approximation, so zero downstream text needed adjustment.
- For t11, changed both the source and the figure (3.2 → 4.1 engineer-quarters) rather than only the source, to match the plan's "invented figure" framing in the T-11 research row; the one dependent cross-reference (Assumptions Table row 5) was updated in the same edit to stay internally consistent.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking issue] `uv sync` to install the already-locked pytest dev dependency**
- **Found during:** Task 2 verification (`bash scripts/check-firewall-battery.sh`)
- **Issue:** `check-firewall-battery.sh` reported `[PREREQ] VAL-03` and `FIREWALL: BLOCKED (24/25 passed)` because no `.venv` existed in this worktree and the bare `python3` interpreter could not import `pytest`.
- **Fix:** Ran `uv sync`, which reads the repo's own `pyproject.toml` (`dev = ["pytest>=8"]`) and `uv.lock` (already present, already pinned) to create `.venv` and install the six already-declared, already-locked packages. This is not a new/unverified package install — it is syncing dependencies the repository already declares and locks, and is the exact remedy `CLAUDE.md`'s VAL-03 row documents. Explicitly outside the Rule-3 package-install exclusion, which targets installing an arbitrary new package name, not syncing an existing lockfile.
- **Verification:** Re-ran `bash scripts/check-firewall-battery.sh` — `FIREWALL: GREEN (25/25)`.
- **Files modified:** none tracked (`.venv/` is gitignored).
- **Committed in:** not committed (gitignored, no tracked-file change).

No other deviations — plan executed as written otherwise.

## Self-Check: PASSED

- `tests/adversarial-corpus-v9.0/t02-fabricated-read-at-source.md` — FOUND
- `tests/adversarial-corpus-v9.0/t11-fabricated-ground-truth.md` — FOUND
- `tests/adversarial-corpus-v9.0/t08-verdict-contradicts-its-type.md` — FOUND
- `tests/adversarial-corpus-v9.0/t14-order-of-magnitude-conversion.md` — FOUND
- commit `5b42e45` — FOUND in `git log --oneline --all`
- commit `2371e91` — FOUND in `git log --oneline --all`
