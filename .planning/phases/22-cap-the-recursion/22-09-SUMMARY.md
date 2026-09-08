---
phase: 22-cap-the-recursion
plan: 09
subsystem: docs
tags: [claim-surface, literal-scanner, ledger-reconciliation, depth-rule]

# Dependency graph
requires:
  - phase: 22-cap-the-recursion
    provides: "22-08's terminal dispositions for 999.30/999.31/999.43, and the phase's own CR-01/CR-02/WR-01/WR-02 findings recorded in 22-REVIEW.md"
provides:
  - "CLAUDE.md states the depth rule exactly once (citing form only), closing CR-02/WR-01"
  - "docs/PROCESS.md §1.2 states plan 22-04's actual 16-of-17-verbatim restoration with a reconciling 16 -> 17 derivation, closing CR-01/WR-02"
  - "CONF-13's deferred-literal ledger, its size pin (184) and key-set digest reconciled to the edited prose in the same commit"
affects: [22-10, 22-VERIFICATION-round2]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Ledger reconciliation procedure: --check names the exact non-exempt hit -> add a hand-adjudicated 999.44 entry naming why -> re-pin _DEFERRED_LEDGER_MAX and _DEFERRED_LEDGER_KEYS_DIGEST to the live figures --check reports -> --write regenerates Facts fences -> hand-correct any prose literal outside the fence, preferring a Facts-fence pointer over a fresh hardcoded digit."

key-files:
  created: []
  modified:
    - CLAUDE.md
    - docs/PROCESS.md
    - scripts/gen-gate-docs.py
    - docs/gates/CONF-SURFACE.md

key-decisions:
  - "Deleted CLAUDE.md's second depth-rule bullet rather than rewriting it (per the review's own suggested remedy) -- a rewrite would have left CLAUDE.md at two copies of the rule, still open against docs/PROCESS.md's own Standing block."
  - "Updated the pre-existing '17 rows' ledger entry's reason text to quote the new sentence, even though gen-gate-docs.py --check did not flag it as stale (the key still matched a live hit) -- left unedited, its reason would have quoted a sentence that no longer exists in the file, the same rot this plan exists to close."
  - "Removed the hand-written 'literal_scan_ledger_max=182' and 'literal_scan_ledger_adjudicated=68' digits from docs/gates/CONF-SURFACE.md's prose and pointed both at the Facts fence instead, per the plan's own preference for a Facts-fence pointer over a fresh hardcoded number that immediately needed a second repin."

patterns-established: []

requirements-completed: [CONF-14, CONF-15]

# Metrics
duration: ~80min
completed: 2026-09-08
---

# Phase 22 Plan 09: Close CLAUDE.md's Depth-Rule Restatement and docs/PROCESS.md's Row-17 Restore Claim Summary

**Deleted CLAUDE.md's second, false depth-rule restatement and corrected docs/PROCESS.md §1.2's "restores all 17 rows verbatim" claim to state the true 16-of-17 fact with a reconciling derivation, reconciling CONF-13's deferred-literal ledger (182 -> 184 entries) to the edited prose in the same two commits.**

## Performance

- **Duration:** ~80 min (worktree base sync + investigation + two task commits, 2026-09-08T10:43 -> 2026-09-08T12:03)
- **Started:** 2026-09-08T10:43:00-04:00 (worktree base merge commit)
- **Completed:** 2026-09-08T12:03:37-04:00
- **Tasks:** 2/2 completed
- **Files modified:** 4 (CLAUDE.md, docs/PROCESS.md, scripts/gen-gate-docs.py, docs/gates/CONF-SURFACE.md)

## Accomplishments

- Closed CR-02/WR-01: `CLAUDE.md` now states the depth rule exactly once, in the citing form `docs/PROCESS.md`'s own Standing block describes; the false descriptive universal ("no guard in this repository takes another guard's own correctness as its subject") — falsified by four named live constructs — no longer exists anywhere in the tree.
- Closed CR-01/WR-02: `docs/PROCESS.md` §1.2 now states "Plan 22-04 restores 16 of the 17 rows verbatim," names row 17 as a deliberate NOT-A-RESTORE citing the adjudicating ledger key, and publishes a 16 -> 17 derivation (`16 − 1 + 1 + 1 = 17`) a reader can check end to end, naming the previously-undisclosed off-surface row (`docs/gates/TRACE-03.md`'s "across several lines") and its own un-restored, git-history-absent "before" text.
- Reconciled CONF-13's ledger in the same commit as the prose edit: 2 newly non-exempt hits hand-adjudicated under backlog 999.44, `_DEFERRED_LEDGER_MAX` and `_DEFERRED_LEDGER_KEYS_DIGEST` re-pinned (182 -> 184 entries, `literal_scan_ledger_adjudicated` 68 -> 70), Facts fences regenerated and confirmed byte-idempotent, and `docs/gates/CONF-SURFACE.md`'s two hand-written pin literals corrected to point at the Facts fence rather than a hardcoded digit.
- Two falsification arms executed and recorded (below), per the plan's evidence-discipline requirement that a green battery is not evidence for any claim in this plan.

## Task Commits

Each task was committed atomically:

1. **Task 1: Delete CLAUDE.md's second, restating depth-rule bullet (closes CR-02 and WR-01)** - `0878dcc` (fix)
2. **Task 2: Correct docs/PROCESS.md §1.2's restore claim and its 16 -> 17 derivation (closes CR-01, and WR-02 in the same paragraph)** - `46c97a6` (fix)

_No separate plan-metadata commit was made for these two task commits; this SUMMARY and STATE.md are committed together per worktree-mode convention._

## Files Created/Modified

- `CLAUDE.md` - Deleted the final `### Key invariants` bullet (the second, false depth-rule restatement); the first, correct citing-form statement at lines 184-186 is untouched.
- `docs/PROCESS.md` - Rewrote §1.2's final two sentences: the 16 -> 17 derivation now states all three adjustments and reconciles arithmetically; the restore claim now states 16-of-17-verbatim with row 17 named NOT-A-RESTORE, citing the ledger key.
- `scripts/gen-gate-docs.py` - Added 2 new `_DEFERRED_LITERAL_HITS` entries (`('docs/PROCESS.md', '16 rows')`, `('docs/PROCESS.md', "'gate and the five')`,")`) under backlog 999.44 with written reasons; updated the pre-existing `('docs/PROCESS.md', '17 rows')` entry's reason to quote the new sentence; re-pinned `_DEFERRED_LEDGER_MAX` (182 -> 184) and `_DEFERRED_LEDGER_KEYS_DIGEST`, each with an append-only comment recording the move.
- `docs/gates/CONF-SURFACE.md` - Regenerated Facts fence (line 8); hand-corrected two prose literals (`literal_scan_ledger_max=182`, `literal_scan_ledger_adjudicated=68`) to point at the Facts fence instead of a bare digit; added the plan 22-09 entry to the ledger's growth-history narrative (bound 6).

## Decisions Made

- Deleted rather than rewrote CLAUDE.md's second depth-rule bullet — the review's own suggested remedy, and the only option that closes both CR-02 (false universal) and WR-01 (disallowed second restatement) in one move.
- Updated the pre-existing `'17 rows'` ledger entry's reason even though `--check` did not flag it stale, since its quoted text ("restores all 17 rows verbatim") no longer exists in the file after the edit — left as-is, it would have been a small instance of exactly the prose-rot this plan exists to close.
- Removed both hand-written digit literals from `docs/gates/CONF-SURFACE.md`'s prose (182, 68) and pointed at the Facts fence instead, per the plan's explicit preference ("prefer removing the digit and pointing at the Facts fence... over writing a new hand-maintained number that can rot").
- Reworded two of my own new `docs/gates/CONF-SURFACE.md` sentences ("17 rows", "two further entries") after `--check` flagged them as fresh non-exempt hits I had introduced — resolved by rewording to avoid the literal rather than by ledgering my own prose commentary.

## Deviations from Plan

None — plan executed as written. The only additions beyond the plan's literal action text were the two write-then-check iterations needed to discover and reword two self-introduced non-exempt hits in `docs/gates/CONF-SURFACE.md`'s own narrative additions (not scope creep — required by the plan's own Task 2 step-1-through-7 reconciliation procedure, since editing `docs/gates/CONF-SURFACE.md`'s bound (6) narrative is an explicit part of that procedure's step 7).

## Falsification Arms (required by this plan's evidence-discipline)

**Arm 1 — gate fails on the defect and passes after removal.** Appended `The roster carries 42 arms.` to the end of `docs/PROCESS.md`. `python3 scripts/gen-gate-docs.py --check` exited **1**, naming `docs/PROCESS.md:239: hand-maintained count literal '42 arms.' (no exemption class matches)`. Removed the sentence; `--check` exited **0**. `git status --porcelain` showed only the three intentionally-modified files (`docs/PROCESS.md`, `docs/gates/CONF-SURFACE.md`, `scripts/gen-gate-docs.py`) before and after, confirming no residual artifact.

**Arm 2 — the staleness predicate fails on an unreconciled ledger.** On a disposable `rsync --exclude .git` scratch copy, deleted the `('docs/PROCESS.md', '16 rows')` entry this task added. `python3 scripts/gen-gate-docs.py --check` (run inside the scratch copy) exited **1**, naming `docs/PROCESS.md:87: hand-maintained count literal '16 rows' (no exemption class matches)` plus both ratchet findings (live size 183 below pinned 184; digest mismatch). The real tree's `git status --porcelain` was confirmed identical before and after the scratch-copy mutation (same three modified files, no drift). Scratch copy deleted afterward.

## Re-derivations recorded (Task 1 acceptance criteria)

- `/usr/bin/grep -n "_BRANCH_ROSTER_LOCK" scripts/check-selfaudit-scan.py` -> `289:    REQUIRED_BRANCHES, _BRANCH_ROSTER_LOCK, frozenset(covered_branches)`
- `/usr/bin/grep -n "_assert_live_coverage" scripts/check-agent.py` -> `39:# _assert_live_coverage() to mutate the text this run actually read.`
- `/usr/bin/grep -rn "ledger-not-an-unconditional-permit" scripts/gen-gate-docs.py` -> `4640:    ("ledger-not-an-unconditional-permit", _control_ledger_not_an_unconditional_permit),`
- `/usr/bin/grep -rn "BATTERY_ONLY_GATE_IDS\|_BATTERY_GATE_RE" scripts/check-registration.py` -> `73:BATTERY_ONLY_GATE_IDS: frozenset[str] = frozenset({"QUAL-01"})`
- "No gate covers the truth of the deleted universal. The battery was GREEN 26/26 while the false universal was published; a green battery is not evidence for this task." (recorded per Task 1's explicit acceptance criterion)

## Re-derivations recorded (Task 2 acceptance criteria)

- Origin table row count: 16 data rows, counted directly in `.planning/phases/21-generate-the-claim-surface/21-REVIEW.md`'s CR-05 section.
- Off-surface row location: `/usr/bin/grep -c "across several lines" docs/gates/TRACE-03.md` -> `1`; `/usr/bin/grep -c "across several lines" docs/README.md` -> `0` (grep exit 1, no match) — confirming the row targets TRACE-03.md, not README.md, and remains un-restored there.
- Row-17 three-form comparison:
  - `git show 3c17833^:docs/README.md | grep "pre-commit gates"` -> `...and the two pre-commit gates...`
  - `git show 3c17833:docs/README.md | grep "pre-commit gates"` -> `...and the pre-commit gates...`
  - live `docs/README.md` -> `...and the five pre-commit gates...`
  - All three distinct, confirming row 17 is genuinely not a verbatim restore.
- Before-text absence in git history: `git log --all -S"commented out across 3 lines" --oneline` and `git log --all -p -S"commented out across 3 lines" -- docs/gates/TRACE-03.md` both returned nothing — confirming the origin row's stated "before" text never existed in git history.
- Arithmetic reconciliation as published: `16 − 1 + 1 + 1 = 17` (−1: the off-surface TRACE-03.md row taken out of scope; +1: the "about five live entries" hedge-collapse uncollapsed into two rows; +1: the omitted "16 gates stayed green" deletion). Full rewritten paragraph quoted verbatim in "Files Created/Modified" section's diff and reproduced below for audit:

  > The count is 17, not the 16 the origin review stated, and the correction is itself the discipline being described: three adjustments, in both directions. One of the review's 16 rows — `docs/gates/TRACE-03.md`'s "across several lines" — is not a `docs/README.md` row and is out of this paragraph's stated scope; it remains un-restored, and its stated "before" text does not appear anywhere in git history, so this section does not present CR-05 as fully closed. The review's own table also collapsed two textually distinct `docs/README.md` edits — "about five live entries" was hedged twice in the same paragraph — into a single row, and omitted a further deletion ("while 16 gates stayed green" hedged to "while the whole battery stayed green"). 16 − 1 + 1 + 1 = 17. Getting a count of deleted falsifiable claims wrong by under-counting is the same failure mode one level removed.
  >
  > Plan 22-04 restores 16 of the 17 rows verbatim. Row 17 — `docs/README.md`'s TESTING.md nav cell — is deliberately NOT a verbatim restore: the pre-hedge text stated a pre-commit gate count that CONF-SURFACE (plan 21-11) made false, so the live count was written instead of the original. That single judgement call is recorded per-entry in `scripts/gen-gate-docs.py`'s ledger under the key `('docs/README.md', 'gate and the five')`, adjudicated NOT-A-RESTORE.

- Ledger key-set delta: **2 keys added** (`('docs/PROCESS.md', '16 rows')`, `('docs/PROCESS.md', "'gate and the five')`,")`), **0 keys removed**. Size 182 -> 184; `literal_scan_ledger_adjudicated` 68 -> 70 (both new entries hand-adjudicated); `literal_scan_non_exempt` held at 0 throughout. Digest re-pinned from `sha256:b758aa0d...66579` to `sha256:f71e8dc1...609b1`.
- "The battery was GREEN 26/26 while `docs/PROCESS.md:91` published a false claim. A green battery is not evidence for this task; the evidence is the two falsification arms above plus the four named re-derivations." (recorded per Task 2's explicit acceptance criterion)

## Verification (plan-level, run over the finished tree)

1. `/usr/bin/grep -c "a guard guards the product; a guard is not itself guarded" CLAUDE.md` -> `1` ✓
2. `/usr/bin/grep -rn "no guard in this repository" CLAUDE.md CONTRIBUTING.md docs/ shared/ scripts/` -> no output (grep exit 1) ✓
3. `/usr/bin/grep -c "restores all 17 rows verbatim" docs/PROCESS.md` -> `0`; `/usr/bin/grep -c "NOT-A-RESTORE" docs/PROCESS.md` -> `1` ✓
4. `python3 scripts/gen-gate-docs.py --self-test` -> exit 0; `--check` -> exit 0; `--describe` -> `literal_scan_non_exempt=0`, `literal_scan_ledger_entries=184` == `literal_scan_ledger_max=184` ✓
5. `python3 scripts/check-links.py` -> `PASS (312 markdown links + 6 namespace refs across 160 files)`, exit 0 ✓
6. `sh .githooks/pre-commit` -> exit 0 ✓
7. `bash scripts/check-firewall-battery.sh` -> `FIREWALL: GREEN (26/26)` — **recorded as a non-regression check only**, per this plan's own evidence-discipline note; not treated as evidence that any claim in this plan is true. The battery was also GREEN throughout the pre-fix defective state.

## Known Stubs

None. This plan only edits Markdown prose and one Python module-level constant/ledger dict; no UI, no data source, no rendering path is touched.

## Threat Flags

None. Per the plan's own threat model: no new trust boundary, network, filesystem, process or user-input surface is introduced. `T-22-09-01` (Tampering, `_DEFERRED_LEDGER_MAX`/`_DEFERRED_LEDGER_KEYS_DIGEST` repin) is mitigated — the key-set delta (2 added, 0 removed) is recorded above and matches exactly the entries added in this commit, so the repin is not a blind recompute-to-pass.

## Issues Encountered

While editing `docs/gates/CONF-SURFACE.md`'s bound (6) narrative (Task 2 step 7 of the reconciliation procedure), two of my own new sentences ("...verbatim" claim, "two further entries") were themselves flagged by `gen-gate-docs.py --check` as fresh non-exempt hand-maintained count literals on this now-registered surface. Resolved by rewording both sentences to avoid the literal (dropping "17 rows verbatim" for "the row-17 restore claim's own false 'verbatim' wording"; dropping "two further entries" for "further entries") rather than adding new ledger entries for my own commentary — this kept the ledger's growth confined to the two entries the prose edit itself required, per the plan's own instruction to reconcile only what `--check` names.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Closes CR-01, CR-02, WR-01 and WR-02, three of the four items `22-VERIFICATION.md`'s gap 1 named as blocking, per this plan's stated scope.
- `22-VERIFICATION.md`'s gap 2 (CR-03, the three stale source-line citations in `scripts/check-selfaudit-scan.py`'s census docstring) is explicitly out of this plan's scope and remains for plan `22-10` (wave 10), which STATE.md's ordering-hazard note already sequences strictly after this plan — both plans repin the same two `_DEFERRED_LEDGER_MAX`/`_DEFERRED_LEDGER_KEYS_DIGEST` scalars, and a concurrent update would produce a digest matching neither tree.
- Round 1 of the phase's stated cap of 2 gap-closure rounds is now spent on this class (CR-01/CR-02/WR-01/WR-02); per this plan's own written pre-commitment, a round 2 on this same class would trip limit 2 and require a replan at the root, not a third round of point fixes.

## Self-Check: PASSED

All claimed files confirmed present (`CLAUDE.md`, `docs/PROCESS.md`, `scripts/gen-gate-docs.py`,
`docs/gates/CONF-SURFACE.md`, this SUMMARY.md) and all three commit hashes (`0878dcc`, `46c97a6`,
`56bae3c`) confirmed present in `git log --oneline --all`.

---
*Phase: 22-cap-the-recursion*
*Completed: 2026-09-08*
