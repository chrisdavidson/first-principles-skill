---
phase: 13-chain-head-grammar
plan: 25
subsystem: quality-harness
tags: [chain-head-grammar, render-contract, quality-harness, sha256-pin, disclosure]

# Dependency graph
requires:
  - phase: 13-chain-head-grammar
    provides: "plans 13-01..13-24 established the four-surface registered-literal mechanism (R1-R9) and CONTRACT-06's sha256 pin over `_chain_block_well_formed`"
provides:
  - "R10 — a tenth registered literal disclosing the detector's over-rejection bound (head or first hop closing its own sentence), byte-identical on all four registered grammar surfaces"
  - "a measured grid proving the bound is positional (head/hop-1 reject, hop-2-onward does not), reproduced live against the unmutated `_chain_block_well_formed`"
  - "recomputed `expected_literal_digest`, updated registry-lock copies, and an updated (surface, rule) pair-count floor (27 -> 31)"
affects: [13-26]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Positional-bound disclosure literal (R7/R9/R10 shape): state the mechanism's rejection, then the exact position where detection stops, in one physical line, pinned by a clause-substring plus a digest over the whole literal set."

key-files:
  created: []
  modified:
    - scripts/check-quality-harness.py
    - shared/spine/references/output-template.md
    - shared/spine/SKILL-body.md
    - shared/spine/references/validation-rubric.md
    - shared/references/reason-upward.md
    - first-principles/agents/first-principles.md
    - first-principles/agents/references/output-template.md
    - first-principles/agents/references/validation-rubric.md
    - first-principles/skills/reason-upward/SKILL.md

key-decisions:
  - "Wording derived from live measurement, not from the review's draft literal — the draft's unconditional 'a chain whose intermediate hop closes its own sentence' phrasing was wrong in the same direction round 5 blocked R9 for; the shipped R10 states the bound positionally (head or first hop only)."
  - "R10's registered clause pins the POSITIONAL half ('from the second hop onward does not change the verdict'), not the rejection half, following R7's and R9's own established rationale — the clause proves the substring most likely to be quietly dropped."
  - "The frozen `_chain_block_well_formed` and `_CHAIN_DETECTOR_PINNED_DIGEST` are untouched — this is a disclosure-only fork, confirmed byte-identical against `git show HEAD:`."

patterns-established: []

requirements-completed: [CHAINHEAD-01, CHAINHEAD-03]

# Metrics
duration: ~55min
completed: 2026-09-03
---

# Phase 13 Plan 25: Register R10 (the chain-rendering over-rejection bound) Summary

**Added a tenth registered literal disclosing that the mechanical chain-form check rejects a chain whose head or first hop closes its own sentence, while a sentence-closing hop from the second hop onward leaves the verdict unchanged — measured directly against the live, unmutated `_chain_block_well_formed` before a word of R10 was written, and proven falsifiable per surface, per byte, and per clause.**

## Performance

- **Duration:** ~55 min
- **Completed:** 2026-09-03
- **Tasks:** 3/3 completed
- **Files modified:** 9 (1 script, 4 canonical `shared/` surfaces, 4 generated tree files)

## Accomplishments

- Measured the over-rejection bound live, before writing any wording, via `importlib` against the unmutated `_chain_block_well_formed` — confirmed it is positional (head or first hop only), matching the plan's predicted grid exactly.
- Registered `R10` in `_RENDER_RULE_LITERALS`, required it on all four canonical surfaces in `_RENDER_SURFACE_REQUIRED_RULES`, and wrote it byte-identically on all four `shared/` surfaces.
- Recomputed `expected_literal_digest` as an explicit, controlled step and updated the registry-lock `expected_required_rules` / `expected_literal_clauses` copies and the `(surface, rule)` pair-count floor (27 → 31).
- Proved R10's registration falsifiable: four independent scratch-copy deletions (one per surface), a single-word byte alteration on one surface, and a positional-clause strip on the module literal — every mutation produced the expected named failure. Re-confirmed every clause of R10 as shipped against the measured grid (no mutation).
- `_chain_block_well_formed` and `_CHAIN_DETECTOR_PINNED_DIGEST` confirmed byte-identical to `git show HEAD:scripts/check-quality-harness.py` throughout.
- Closed with `python3 scripts/check-quality-harness.py --self-test` exit 0 (`chain_detector_pin` and `render_contract` both PASSED), `python3 scripts/sync-content.py --check` exit 0, and `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (23/23)`.

## Task Commits

1. **Task 1: Measure the over-rejection bound before writing a single word of R10** — no commit (measurement-only; `scripts/check-quality-harness.py` unmodified, `git status --porcelain` empty, per the task's own acceptance criteria).
2. **Task 2: Register R10 and state it byte-identically on all four grammar surfaces** — `6930e19` (feat)
3. **Task 3: Prove R10's registration falsifiable and its wording honest** — no commit (all mutations ran on disposable `rsync --exclude .git --exclude .venv --exclude .planning` scratch copies; the real tree was never modified — `git status --porcelain` confirmed empty before the first mutation and after the last).

**Plan metadata:** this commit (docs: complete plan)

## Files Created/Modified

- `scripts/check-quality-harness.py` — added `R10` to `_RENDER_RULE_LITERALS`, added `"R10"` to every surface's tuple in `_RENDER_SURFACE_REQUIRED_RULES` and the registry-lock `expected_required_rules` copy, added the `expected_literal_clauses["R10"]` entry, recomputed `expected_literal_digest`, and updated the `(surface, rule)` pair-count floor (`27` → `31`, comment `9+9+5+4` → `10+10+6+5`).
- `shared/spine/references/output-template.md`, `shared/spine/SKILL-body.md`, `shared/spine/references/validation-rubric.md`, `shared/references/reason-upward.md` — each received the byte-identical R10 sentence, placed immediately after R9's existing paragraph (or, on `validation-rubric.md`, inline in the same flowing paragraph, matching how R7/R8/R9 already sit there).
- `first-principles/agents/first-principles.md`, `first-principles/agents/references/output-template.md`, `first-principles/agents/references/validation-rubric.md`, `first-principles/skills/reason-upward/SKILL.md` — regenerated via `python3 scripts/sync-content.py --write`.

## Task 1 — Measured Grid

Called the live, unmutated `_chain_block_well_formed` directly via `importlib.util.spec_from_file_location` (registered under an explicit `sys.modules` name, per the plan's own guidance for this file's frozen dataclasses). Built chains with a fixed `GT-2 (a) + GT-3 (b)` head and 2, 3, or 4 arrow-led hops, sweeping which single position (the head, or hop N) carried a terminal period, plus a fully-open baseline for each hop count:

| hop count | closed position | verdict |
|---|---|---|
| 2 | none (baseline) | True |
| 3 | none (baseline) | True |
| 4 | none (baseline) | True |
| 2 | head | False |
| 3 | head | False |
| 4 | head | False |
| 2 | hop 1 | False |
| 2 | hop 2 | True |
| 3 | hop 1 | False |
| 3 | hop 2 | True |
| 3 | hop 3 | True |
| 4 | hop 1 | False |
| 4 | hop 2 | True |
| 4 | hop 3 | True |
| 4 | hop 4 | True |

**Result:** the over-rejection bound is exactly as the plan predicted and exactly as round 6's verification stated — rejection occurs when the head closes its sentence, and when the FIRST hop does; a sentence-closing hop from the second hop onward leaves the verdict unchanged at every hop count tested (2, 3, 4). No divergence from the plan's stated grid. `git status --porcelain` was empty before and after; `scripts/check-quality-harness.py` was unmodified by this task (confirmed via `git diff --stat`).

**Mechanism (read, not edited):** `_chain_block_well_formed` checks `segment_closed` (set from `_segment_sentence_closed`) *before* absorbing each candidate next line, using the state left by the *previously absorbed* segment. Closing the head means `segment_closed` is already `True` before the loop starts, so hop 1 is never absorbed — the candidate stays head-only, which can never satisfy `_CHAIN_FORM_LINE_RE`'s two-arrow minimum. Closing hop 1 means the loop absorbs hop 1 (already open when checked), computes `segment_closed = True` afterward, then refuses to absorb hop 2 on the next iteration — again leaving only 1 arrow, below the two-arrow minimum. Closing hop 2 or later means at least 2 hops (2 arrows) are already absorbed by the time the closure blocks further absorption, which already satisfies the two-arrow minimum — so the truncated candidate still matches.

## Task 2 — R10 Registration

**R10 literal (identical on all four surfaces and in the module):**

> The mechanical form check additionally rejects a chain whose head or first hop closes its own sentence before the next `→`: it reads the following arrow-led line as a new statement and ends the chain there, so a chain satisfying every rule above is scored malformed for that reason alone. The check reaches only that position — a hop that closes its own sentence from the second hop onward does not change the verdict — which is why intermediate hops carry no terminal punctuation in this project's worked examples.

Verified byte-identical across all four `shared/` surfaces with a Python script counting exact-substring occurrences (1 each) rather than visual inspection.

**Digest recompute (explicit, controlled step):**
- Old `expected_literal_digest`: `sha256:1990944390d22d07dcace92290262159bdfa8c09a2686534c6e300f621aebe00`
- New `expected_literal_digest`: `sha256:301ef5ff8ebe97b8163800e9f9cc2b0daec1ac1b48a97a64ac1adc23ccf6e8f3`
- Computed as `"sha256:" + sha256("\x00".join(f"{k}={v}" for k, v in sorted(_RENDER_RULE_LITERALS.items())).encode("utf-8")).hexdigest()`, matching the module's own formula exactly.

**Pair-count floor:** `expected_missing_case_count` moved `27` → `31` (each of the four surfaces gained one required rule, `10 + 10 + 6 + 5`), derived from `sum(len(keys) for keys in _RENDER_SURFACE_REQUIRED_RULES.values())` per the plan's instruction rather than hand-typed.

**`_chain_block_well_formed` / `_CHAIN_DETECTOR_PINNED_DIGEST` byte-identity confirmed** against `git show HEAD:scripts/check-quality-harness.py` via direct regex extraction and comparison — both identical. Only a disclosure literal and its registry scaffolding changed; the frozen detector was not touched.

**Gate results after task 2:**
- `python3 scripts/check-quality-harness.py --self-test` → exit 0, `render_contract` and `chain_detector_pin` both PASSED.
- `python3 scripts/sync-content.py --check` → exit 0.
- `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (23/23)` (required `uv sync` first to provision a pytest-capable `.venv` for VAL-03's third leg — the battery reported `BLOCKED` beforehand due to the missing external prerequisite, not a gate failure; `.venv/` is gitignored).

## Task 3 — Falsifiability Proofs

All mutations ran on a disposable `rsync -a --exclude .git --exclude .venv --exclude .planning` scratch copy per mutation (a fresh copy for each of R1's four surfaces, R2, and R3), with `git status --porcelain` on the real tracked tree confirmed empty before the first mutation and after the last.

**R1 — per-surface deletion (4 mutations, 4 named failures):**

| Surface mutated | `--self-test` exit | Failure message |
|---|---|---|
| `shared/spine/references/validation-rubric.md` | 1 | `render_contract (i) POSITIVE: shared/spine/references/validation-rubric.md: rule R10 is missing — deleted from this surface` |
| `shared/spine/references/output-template.md` | 1 | `render_contract (i) POSITIVE: shared/spine/references/output-template.md: rule R10 is missing — deleted from this surface` |
| `shared/spine/SKILL-body.md` | 1 | `render_contract (i) POSITIVE: shared/spine/SKILL-body.md: rule R10 is missing — deleted from this surface` |
| `shared/references/reason-upward.md` | 1 | `render_contract (i) POSITIVE: shared/references/reason-upward.md: rule R10 is missing — deleted from this surface` |

Each mutation deleted R10's sentence from exactly one `shared/` surface, regenerated with `sync-content.py --write`, then ran `--self-test` — each named the mutated relpath and `R10`.

**R2 — single-word byte alteration (1 mutation, 1 named failure):** altered `output-template.md`'s R10 text from "additionally rejects" to "also rejects" (leaving the other three surfaces and the module literal untouched), regenerated, and ran `--self-test`: exit 1, `render_contract (i) POSITIVE: shared/spine/references/output-template.md: rule R10 is missing — deleted from this surface`. The exact-substring identity check reports byte-altered text the same way it reports absent text — presence, not merely a "contains some of the words" fuzzy match, is what the mechanism guarantees, confirming identity across surfaces (not mere partial presence) is enforced.

**R3 — positional-clause strip on the module literal only (no recompute):** stripped `"sentence from the second hop onward does not change the "` / `"verdict — which is why..."` down to a shortened form that dropped the positional clause, from `_RENDER_RULE_LITERALS["R10"]` in the module only (no `sync-content.py --write`, no digest recompute — the four `shared/` surfaces were left with the full, original R10 text). `--self-test` exit 1 with BOTH:
- `render_contract (h) MEMBERSHIP LOCK: literals: R10 is missing its required clause 'from the second hop onward does not change the verdict'`
- `render_contract (h) MEMBERSHIP LOCK: literals: digest 'sha256:c1e7a8fda9afe55b078734519322d9106b311171daeac0c3dad46948fa96a354' != pinned 'sha256:301ef5ff8ebe97b8163800e9f9cc2b0daec1ac1b48a97a64ac1adc23ccf6e8f3'`

(plus four cascading `(i) POSITIVE` failures on the four now-unmatched surfaces, since the shortened module literal no longer appears verbatim in any of them — expected, not a defect.) This proves the clause table pins the disclosure rather than the rejection half, so R10 cannot silently revert to an unconditional statement without both the clause arm and the digest arm going red — the exact regression class round 5 blocked R9 for.

**R4 — honesty check, no mutation:** re-ran task 1's measurement grid against the real tracked tree (post-task-2 commit) and confirmed it is unchanged (identical to task 1's grid, since `_chain_block_well_formed` was never touched). Checked R10 as shipped, clause by clause, against that grid:

- *"additionally rejects a chain whose head or first hop closes its own sentence before the next `→`"* — TRUE: head-closed → `False` at hop counts 2/3/4; hop-1-closed → `False` at hop counts 2/3/4.
- *"it reads the following arrow-led line as a new statement and ends the chain there"* — accurate description of the mechanism read in task 1 (segment-closed state checked before absorbing the next candidate line).
- *"a chain satisfying every rule above is scored malformed for that reason alone"* — TRUE: every test chain in the grid used well-formed heads/hops satisfying R1-R9; only the closure position changed the verdict.
- *"The check reaches only that position"* — TRUE: no closure position beyond hop 1 changed the verdict, at any hop count tested.
- *"a hop that closes its own sentence from the second hop onward does not change the verdict"* — TRUE: hop-2/hop-3/hop-4 closures all verdict `True`, matching the fully-open baseline, at every hop count tested (2, 3, 4).
- *"which is why intermediate hops carry no terminal punctuation in this project's worked examples"* — a statement of project practice (plan 13-13's period-stripping), not a detector-behavior claim the grid can confirm or deny directly; consistent with the review's own account of why plan 13-13 made that edit.

No clause over-claims; no correction was needed.

**Real tree confirmed clean and closed:** `git status --porcelain` empty before the first mutation and after the last; scratch directories deleted after every R1/R2/R3 mutation. Real tree re-run: `python3 scripts/check-quality-harness.py --self-test` exit 0; `python3 scripts/sync-content.py --check` exit 0; `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (23/23)`.

## Deviations from Plan

None — plan executed exactly as written. Task 1's measured grid matched the plan's predicted grid with zero divergence, so no wording correction was needed.

## Verification

- `python3 scripts/sync-content.py --check` — exit 0. **Observed**, not assumed.
- `python3 scripts/check-quality-harness.py --self-test` — exit 0, `chain_detector_pin` PASSED. **Observed**, not assumed.
- `bash scripts/check-firewall-battery.sh` — `FIREWALL: GREEN (23/23)`. **Observed**, not assumed (required a one-time `uv sync` to provision a pytest-capable `.venv`, since none pre-existed in this fresh worktree; this is an environment-provisioning step, not a code change, and `.venv/` is gitignored).
- Deleting R10 from any one of the four surfaces exits non-zero naming that surface — **observed** directly for all four surfaces via scratch-copy mutation (task 3, R1).

## Self-Check

- `scripts/check-quality-harness.py` — FOUND (modified, tracked)
- `shared/spine/references/output-template.md` — FOUND (modified, tracked)
- `shared/spine/SKILL-body.md` — FOUND (modified, tracked)
- `shared/spine/references/validation-rubric.md` — FOUND (modified, tracked)
- `shared/references/reason-upward.md` — FOUND (modified, tracked)
- `first-principles/agents/first-principles.md` — FOUND (regenerated, tracked)
- `first-principles/agents/references/output-template.md` — FOUND (regenerated, tracked)
- `first-principles/agents/references/validation-rubric.md` — FOUND (regenerated, tracked)
- `first-principles/skills/reason-upward/SKILL.md` — FOUND (regenerated, tracked)
- Commit `6930e19` — FOUND in `git log --oneline`

## Self-Check: PASSED
