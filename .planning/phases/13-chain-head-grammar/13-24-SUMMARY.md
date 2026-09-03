---
phase: 13-chain-head-grammar
plan: 24
subsystem: testing
tags: [python, regex, self-test, quality-harness, chain-form, sync-content]

# Dependency graph
requires:
  - phase: 13-chain-head-grammar
    provides: "13-23's registered chain-form-rule mechanism (_RENDER_RULE_SURFACES, _RENDER_RULE_LITERALS) that this plan makes tree-derived rather than hand-maintained"
provides:
  - "Point-back Handoff paragraphs on estimate-detail.md and theoretical-limit-detail.md that name technique-specific content in prose and cite output-template.md §4 instead of restating the chain-form template"
  - "_render_chain_form_surface_problems — a pure, tree-derived sweep that flags any shared/**/*.md file stating the chain form as a template rendering while absent from _RENDER_RULE_SURFACES or a written exemption"
  - "A call-site census entry for the sweep's own helper, closing the unwired-detectable-only-by-diff-review gap the mutation reproduction (Q2) found in this plan's own first draft"
affects: [13-25, 13-26, 13-27, 13-28]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Tree-derived registry sweep: compare a signature-matched candidate set against a hand-maintained registry by EQUALITY (not subset), following the CR-03/WR-04 shape already used by the chain-family coverage floor and the dispatch-reachability floor"
    - "Lowercase-first-character bracket discriminator to distinguish a template placeholder ([intermediate claim]) from a worked example's filled-in value ([Lower: ~$15/kWh ...])"

key-files:
  created: []
  modified:
    - shared/references/estimate-detail.md
    - shared/references/theoretical-limit-detail.md
    - first-principles/agents/references/estimate-detail.md
    - first-principles/agents/references/theoretical-limit-detail.md
    - first-principles/skills/estimate/references/estimate-detail.md
    - first-principles/skills/theoretical-limit/references/theoretical-limit-detail.md
    - scripts/check-quality-harness.py

key-decisions:
  - "Took the point-back fork (not the register fork) for both -detail.md files: output-template.md's own 'Converting structured-technique outputs into chains' subsection already declares itself the single source of truth and instructs per-technique Handoff sections to point back rather than restate, so restating the form there contradicts a convention this tree already publishes."
  - "Narrowed the chain-form signature to require a lowercase first character inside the bracket after the arrow (`→ [a-z`), because the unrestricted signature false-positived on two genuine worked examples (estimate-fermi.md, theoretical-limit-carnot.md) that render real filled-in values inside brackets — measured against the live tree, not assumed from the plan's stated (and, it turned out, inaccurate) claim that the unrestricted form already excluded all worked examples."
  - "Added a call-site census for the sweep's own helper (_render_chain_form_surface_problems) beyond what the plan's task 2 specified, after Q2's mutation reproduction showed the leg's wiring could be deleted entirely with the battery still green — the same forgeability class R4-CR-01 closed for the coverage-floor-registry and worked-example-conformance helpers one plan earlier."

requirements-completed: [CHAINHEAD-03, CHAINHEAD-04]

# Metrics
duration: 55min
completed: 2026-09-03
---

# Phase 13 Plan 24: Chain-form point-back fork and tree-derived surface sweep Summary

**Rewrote estimate/theoretical-limit Handoff sections to point at the output template instead of restating the chain form, then closed the underlying defect class with a tree-derived sweep (`_render_chain_form_surface_problems`) that catches any `shared/**/*.md` file stating the chain form as a template while unregistered — verified by three scratch-copy mutations (Q1 reproduces the fixed defect, Q2 reproduces an unwired-but-defined sweep, Q3 reproduces a reasonless exemption), all now caught with the sweep in place.**

## Performance

- **Duration:** 55 min
- **Started:** 2026-09-03T11:00:00Z (approx, worktree base correction preceded task work)
- **Completed:** 2026-09-03T11:56:00Z
- **Tasks:** 3
- **Files modified:** 7 (2 canonical + 4 generated copies + 1 script)

## Accomplishments
- Closed round-6 gap 3 (CR-04): `estimate-detail.md` and `theoretical-limit-detail.md` no longer restate the chain-form template; both point back to `output-template.md` §4 for the form and head grammar while keeping their technique-specific prose (unit-factor product / bracketed magnitude for estimate; governing law / law-permitted ceiling / gap to convention for theoretical-limit) and every required verbatim sentence
- Added a tree-derived sweep that makes "every canonical surface that states the chain form" a checkable property instead of a hand-maintained list nobody checks against the tree — the exact mechanism gap that let the same defect class recur one round after `reason-upward.md` was fixed for it (CR-03, plan 13-20)
- Found and fixed a genuine measurement gap in the plan's own stated signature design: two live worked examples (`estimate-fermi.md`, `theoretical-limit-carnot.md`) false-positived against the plan-specified signature; narrowed the signature with a measured, disclosed discriminator rather than exempting the files
- Found and fixed a second gap during the plan's own Q2 mutation-reproduction step: the sweep's wiring itself had no call-site census, so deleting it entirely left the battery green — added the missing census entry before declaring the leg closed

## Task Commits

Each task was committed atomically:

1. **Task 1: Take the point-back fork on both -detail.md Handoff sections, with the rationale recorded** - `48f6576` (fix)
2. **Task 2: Add the tree-derived unregistered-chain-form-surface sweep** - `d264419` (feat)
3. **Task 3: Mutation reproduction and closing evidence** - `be0db88` (fix)

_Note: Task 3's commit is the closing-evidence fix (the census gap Q2 found), not a separate metadata-only commit — the mutation reproduction itself was run and verified on scratch copies, never committed._

## Files Created/Modified
- `shared/references/estimate-detail.md` - Handoff paragraph rewritten to name unit-factor product/bracketed magnitude in prose and point at output-template.md §4
- `shared/references/theoretical-limit-detail.md` - Handoff paragraph rewritten to name governing law/law-permitted ceiling/gap to convention in prose and point at output-template.md §4
- `first-principles/agents/references/estimate-detail.md`, `first-principles/agents/references/theoretical-limit-detail.md`, `first-principles/skills/estimate/references/estimate-detail.md`, `first-principles/skills/theoretical-limit/references/theoretical-limit-detail.md` - regenerated via `sync-content.py --write`
- `scripts/check-quality-harness.py` - `_RENDER_CHAIN_FORM_SIGNATURE`/`_GLOB`/`_EXEMPT`, the pure `_render_chain_form_surface_problems` helper, the `(cf)` leg with its EQUALITY floor and five isolation controls in `_selftest_render_contract`, three new `_RenderRegistrySnapshot` fields with matching `(h2)` lock negatives, an updated `_RENDER_RULE_SURFACES` closing comment recording the fork rationale, and a `(t)` census entry for the sweep helper's own call sites

## Decisions Made
- Point-back fork over register fork (see `key-decisions` above) — recorded in the `_RENDER_RULE_SURFACES` comment block itself, per the plan's task 1 instruction, plus restated here and in this SUMMARY per the threat model's T-13-24-01 mitigation (full doc-row restatement deferred to plan 13-28 as the threat model specifies).
- Lowercase-first-character bracket discriminator (`[a-z]`) — see `key-decisions` above.
- Census the sweep's own helper beyond the plan's literal task 2 scope — see `key-decisions` above.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Chain-form signature false-positived on two genuine worked examples**
- **Found during:** Task 2 (first self-test run after wiring the sweep)
- **Issue:** The plan's task 2 action specified a signature matching "a GT-N/GT-1/Cn/C1-shaped head token followed... by an arrow immediately preceding a bracketed placeholder (`→ [`)" and stated this "deliberately does NOT match the fourteen `shared/examples/*.md` worked examples." Measured against the live tree, the unrestricted signature also matched `shared/examples/estimate-fermi.md` (`→ installed-capital bracket: [Lower: ~$15/kWh | Central: ~$30/kWh | Upper: ~$42/kWh]`) and `shared/examples/theoretical-limit-carnot.md` (`→ [Conclusion: Molten-salt TES is cost-competitive...]`) — both genuine worked examples rendering real filled-in values, not template placeholders, that predate this plan by many phases (git history: Phase 103/105).
- **Fix:** Added a `[a-z]` requirement on the bracket's first character — every true template placeholder in the four registered surfaces (`[intermediate claim]`, `[conclusion]`, and the CR-04 files' own `[unit-factor product]`, `[bracketed magnitude]`, `[governing law]`, `[law-permitted ceiling]`, `[gap to convention]`) starts lowercase, while both false-positive worked examples' filled-in brackets start uppercase (`[Lower`, `[Conclusion`). Verified against the full `shared/**/*.md` tree: the narrowed signature matches exactly the four registered surfaces on the clean tree, and still matches both pre-task-1 CR-04 texts (proven via scratch-copy replay of the original wording), so the narrowing does not cost the defect this sweep exists to catch. Disclosed as a measured limitation in the constant's own comment: a future placeholder rendered with an uppercase-led bracket (`[Conclusion]` rather than `[conclusion]`) would not match.
- **Files modified:** scripts/check-quality-harness.py
- **Verification:** `python3 scripts/check-quality-harness.py --self-test` exits 0 on the real tree; scratch-copy sweep over `shared/**/*.md` with the narrowed signature returns exactly the four registered surfaces; scratch-copy replay of the pre-task-1 CR-04 text still matches.
- **Committed in:** d264419 (Task 2 commit)

**2. [Rule 2 - Missing Critical] The sweep's own wiring had no call-site census, reproducing the exact forgeability class R4-CR-01 closed one plan earlier**
- **Found during:** Task 3, Q2 mutation reproduction (as specified by the plan's own task 3 action)
- **Issue:** Deleting the entire `(cf)` leg from `_selftest_render_contract` (helper left defined, zero calls) left the self-test GREEN except for the EQUALITY floor's own reused `_render_coverage_floor_problems` call dropping the shared census count from 7 to 6 — but nothing named the sweep helper's OWN wiring as missing. This is precisely the "unregistered helper's call site is deletable with the battery green" shape `13-VERIFICATION-round4.md`'s R4-CR-01 finding closed for the coverage-floor-registry and worked-example-conformance helpers.
- **Fix:** Added a sixth census pattern (`_render_chain_form_surface_problems(`) to control (t)'s source-text call-site count, expecting 6 sites (1 real — THE SWEEP ITSELF — plus the five `cf-iso` isolation arms), following the exact shape the existing coverage/example/entry-source censuses already use.
- **Files modified:** scripts/check-quality-harness.py
- **Verification:** On a fresh scratch copy with the `(cf)` block entirely removed, `--self-test` now exits non-zero naming `0 chain-form-surface-sweep helper call site(s) (expected 6)`. Real-tree self-test still exits 0 after the fix; `bash scripts/check-firewall-battery.sh` prints `FIREWALL: GREEN (23/23)`.
- **Committed in:** be0db88 (Task 3 commit)

---

**Total deviations:** 2 auto-fixed (1 bug, 1 missing critical)
**Impact on plan:** Both fixes were necessary for the sweep to actually deliver what the plan's must-haves require ("Adding a chain-form template rendering to any unregistered file... makes `--self-test` exit non-zero naming that file" — a sweep with false positives on real worked examples, or one that is silently unwired, does not satisfy that truth). No scope creep beyond what the plan's own verification steps (Q1/Q2/Q3) were designed to surface.

## Mutation Reproduction Evidence (Q1/Q2/Q3, Task 3)

All three run on a disposable `rsync -a --exclude .git --exclude .venv --exclude .planning` scratch copy, never on the tracked tree. `git status --porcelain` on the real tree was empty immediately before Task 1 began and is empty now (0 lines) after Task 3's own real-tree edit (the census fix) was committed; each Q's own mutation lived only in its scratch copy and was discarded with the copy.

**Q1** — reverted both `-detail.md` files to their pre-task-1 text on a scratch copy, regenerated (`sync-content.py --write`), ran `--self-test`:
```
self-test FAIL: render_contract (cf) CHAIN-FORM SURFACE SWEEP EQUALITY: (cf) chain-form candidate set: actual [...,'shared/references/estimate-detail.md', ..., 'shared/references/theoretical-limit-detail.md', ...] != required [...] — MISSING [], UNEXPECTED ['shared/references/estimate-detail.md', 'shared/references/theoretical-limit-detail.md']
self-test FAIL: render_contract (cf) CHAIN-FORM SURFACE SWEEP: shared/references/estimate-detail.md: states the chain form as a template rendering (matches the chain-form signature) but is registered in neither _RENDER_RULE_SURFACES nor _RENDER_CHAIN_FORM_EXEMPT
self-test FAIL: render_contract (cf) CHAIN-FORM SURFACE SWEEP: shared/references/theoretical-limit-detail.md: states the chain form as a template rendering (matches the chain-form signature) but is registered in neither _RENDER_RULE_SURFACES nor _RENDER_CHAIN_FORM_EXEMPT
```
Exit 1. Before this plan the identical tree state was GREEN (no mechanism reached these two files) — that delta is this plan's evidence. Restored.

**Q2** — deleted the sweep's entire `(cf)` wiring block from the self-test (helper left defined, zero calls), on a scratch copy that also carried Q1's revert, ran `--self-test`:
```
self-test FAIL: render_contract (t) SCORING RECORDER LOCK: ... 6 coverage-floor-registry helper call site(s) (expected 7), ... and 0 chain-form-surface-sweep helper call site(s) (expected 6)
```
Exit 1 — on the sweep's own registration/anti-masking floor (the census added as this task's own closing fix), not passing silently. Restored (fresh scratch copy for Q3).

**Q3** — added `("shared/references/trade-off.md", "")` (empty reason) to `_RENDER_CHAIN_FORM_EXEMPT` on a scratch copy, ran `--self-test`:
```
self-test FAIL: render_contract (h) MEMBERSHIP LOCK: chain_form_exempt: (('shared/references/trade-off.md', ''),) != expected ()
self-test FAIL: render_contract (cf) CHAIN-FORM SURFACE SWEEP EQUALITY: ... MISSING ['shared/references/trade-off.md'], UNEXPECTED []
self-test FAIL: render_contract (cf) CHAIN-FORM SURFACE SWEEP: shared/references/trade-off.md: REASONLESS EXEMPTION — exempted from the chain-form surface sweep with no written reason
```
Exit 1, naming the reasonless exemption. Restored (scratch directory deleted).

**Fork taken and where its rationale is recorded:** the point-back fork (not the register fork), for the reason stated under `key-decisions` above. Recorded in `scripts/check-quality-harness.py`'s `_RENDER_RULE_SURFACES` comment block (the rewritten closing paragraph, Task 1) and in this SUMMARY. Full `| QUAL-01 |` doc-row restatement on `CLAUDE.md`/`docs/ARCHITECTURE.md` is deferred to plan 13-28 per the threat model's T-13-24-01 mitigation plan.

## Issues Encountered
None beyond the two deviations documented above, both discovered by the plan's own prescribed verification steps (a self-test run in Task 2; the Q2 mutation reproduction the plan's Task 3 explicitly prescribes) and fixed inline before the task they were found in was considered complete.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- CHAINHEAD-03 and CHAINHEAD-04 requirements closed for this plan's scope: the chain-form rule is now enforced by a tree-derived sweep rather than a hand-maintained registry, and both CR-04 files no longer restate the template.
- `_chain_block_well_formed` remains byte-unchanged (`contract_pin` self-test: 0 PINNED-RED); the frozen detector was not touched by this plan.
- Plan 13-28 still owns restating this plan's fork rationale on the `| QUAL-01 |` CLAUDE.md/docs/ARCHITECTURE.md doc rows, per the threat model's own deferral.

---
*Phase: 13-chain-head-grammar*
*Completed: 2026-09-03*

## Self-Check: PASSED

- FOUND: .planning/phases/13-chain-head-grammar/13-24-SUMMARY.md
- FOUND: shared/references/estimate-detail.md
- FOUND: shared/references/theoretical-limit-detail.md
- FOUND: scripts/check-quality-harness.py
- FOUND commit: 48f6576 (Task 1)
- FOUND commit: d264419 (Task 2)
- FOUND commit: be0db88 (Task 3)
- FOUND commit: ac00cb6 (SUMMARY)
