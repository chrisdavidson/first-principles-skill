---
phase: 26-migration-apply-reconcile-generalize-enforce
plan: 05
subsystem: infra
tags: [gen-gate-docs, narrative-region, containment-ledger, ratchet, self-test]

# Dependency graph
requires:
  - phase: 26-migration-apply-reconcile-generalize-enforce
    plan: 04
    provides: >-
      The two wired NARR-02/RATCHET-01 regions (docs/README.md,
      docs/MEASUREMENT-MAP.md) and the cmd_check() wiring (roster equality
      floor + restatement census) this plan extends to a third surface
  - phase: 26-migration-apply-reconcile-generalize-enforce
    plan: 03
    provides: >-
      The region mechanism's shape (_NarrativeRegion, marker-pair
      registration, _render_narrative_sentence, restatement census) this
      plan's third region reuses unmodified
provides:
  - "CLAUDE.md's own third narrative region (CLAUDE_HEADLINE_MARKERS), a second independent marker pair chained onto the same CLAUDE_MD target the CI-gate-table region already writes"
  - "The narrative-region roster and its lock extended from two surfaces to three (docs/README.md, docs/MEASUREMENT-MAP.md, CLAUDE.md), floored by equality against the surface-key set cmd_check()'s own loop accumulates"
  - "The deferred-containment ledger reconciled 26 -> 23 entries, re-pinned (_CONTAINMENT_LEDGER_MAX, _CONTAINMENT_LEDGER_KEYS_DIGEST) in the same commit as the reconciliation that moved it"
  - "A generated per-class breakdown of the containment ledger (containment_ledger_cannot_reach/_frozen_historical/_not_a_count_claim derived-counts fields, backed by _containment_ledger_class_counts()) published on docs/gates/CONF-SURFACE.md's disclosed bound (11)"
  - "RATCHET-02's size-only scope sentence, stated at _CONTAINMENT_LEDGER_MAX's own comment block, citing the concrete ('CLAUDE.md', '43') instance this plan found"
  - "A new backlog entry (999.73) for the 9 not-a-count-claim containment entries, split out of 999.69 so that class is separately schedulable"
  - "Two new --self-test controls (107 -> 109): claude-headline-region-chained-not-reread and containment-ledger-class-counts-cover-ledger"
affects: [26-06, 26-07]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "A second, independent _replace_or_bootstrap_region() call chained onto targets[CLAUDE_MD] (the text the FIRST call already produced), rather than a second independent read of CLAUDE.md -- the exact chaining shape the plan's own action text required"
    - "Bootstrap anchors created by a minimal, content-preserving line split (one glued physical line, 'findings. (Derived from...', split into two) rather than widening the swallowed region to reach a pre-existing anchor -- chosen specifically to keep the six frozen-historical digits in the following sentence OUTSIDE the new fence, since swallowing them would have shrunk the containment ledger inside this same task"
    - "A ledger reason's own leading tag (CANNOT-REACH / FROZEN HISTORICAL / NOT A COUNT CLAIM) doubling as the input to a generated per-class tally function, so the published breakdown is derived from the ledger itself rather than hand-typed and re-counted"

key-files:
  created: []
  modified:
    - scripts/gen-gate-docs.py
    - CLAUDE.md
    - docs/gates/CONF-SURFACE.md
    - .planning/ROADMAP.md
    - .planning/REQUIREMENTS.md

key-decisions:
  - "Combined this plan's Task 1 (land the region) and Task 2 (reconcile + re-pin the ledger) into a SINGLE commit, per the plan's own must_haves requirement that the re-pin land in the same commit as the reconciliation that moved it (D-05 proviso 1) -- landing the region alone, in its own commit, would have left the containment ledger's staleness predicate failing at that exact commit (three entries' underlying findings disappear the moment the region lands), which the pre-commit hook's own gen-gate-docs.py --self-test/--check gates would have blocked. Documented as a deviation from the plan's literal per-task commit shape, per the harness's own explicit instruction for this plan."
  - "Found the ('CLAUDE.md', '43') containment-ledger entry's reason factually wrong (live control_count is 44, not 43) but did NOT correct the underlying CLAUDE.md prose to fix it -- doing so would also move the deferred-LITERAL ledger's own twin entry for the identical text (('CLAUDE.md', '(43 controls)'), backlog 999.42), which this plan's own acceptance criteria hold untouched, reserved for plan 26-06. Left the entry ledgered with a corrected reason documenting the discovery, rather than silently fixing it out of scope."
  - "Split the 9 not-a-count-claim containment entries (identifier residue, quick-task ids, line-number citations, arithmetic-expression offsets, CLI flag values) to a new backlog entry (999.73) rather than leaving them inside 999.69's own CONTAIN-04 disposition, since they need a REACH move on containment's own citation-shape stripper -- a different, smaller fix than a generated region -- and D-06 proviso 2 requires this class published separately from the genuine cannot-reach residue, not folded into it."
  - "Left CONTAIN-04 and RATCHET-02 unchecked in .planning/REQUIREMENTS.md: both requirements' own literal text names the deferred-LITERAL ledger (_DEFERRED_LEDGER_MAX), which this plan does not touch by its own stated scope discipline. Annotated both items in place with the containment-half completion and the outstanding literal-ledger half, rather than ticking a box the requirement's own text does not yet support."

requirements-completed: []

# Metrics
duration: ~2h
completed: 2026-09-10
---

# Phase 26 Plan 05: CLAUDE.md's third narrative region and the containment ledger's reconciliation Summary

**Wired CLAUDE.md's own coverage-headline sentence into a second, independent generated region (chained onto the same CI-gate-table target), reconciled the deferred-containment ledger from 26 to 23 entries with the delta measured and published by class, and stated RATCHET-02's size-only scope at the constant -- citing a concrete stale-reason instance this plan found and deliberately left unfixed to protect the literal ledger's own out-of-scope boundary.**

## Performance

- **Duration:** ~2h
- **Tasks:** 3 (Tasks 1 and 2 combined into one commit per the plan's own same-commit requirement; Task 3 touches only gitignored planning docs, no commit)
- **Files modified:** 4 tracked (`scripts/gen-gate-docs.py`, `CLAUDE.md`, `docs/gates/CONF-SURFACE.md`, `docs/ARCHITECTURE.md` as the mechanical `--write` regeneration side effect) plus 2 gitignored (`.planning/ROADMAP.md`, `.planning/REQUIREMENTS.md`)

## Accomplishments

- `CLAUDE.md` hosts a third generated region (`CLAUDE_HEADLINE_MARKERS`), registered in `_generated_marker_pairs_for("CLAUDE.md")` as a two-element tuple alongside the pre-existing `CLAUDE_REGION_MARKERS` (the CI-gate table); `generate_all()`'s new call site chains onto `targets[CLAUDE_MD]` (the text the first call already produced), never a second independent read — proven by a new `--self-test` control (`claude-headline-region-chained-not-reread`) asserting both marker pairs survive in the same generated output.
- The bootstrap anchors were created by a minimal, content-preserving edit: one physical line ("findings. (Derived from regenerated matrix Phase 138 Plan 03; ...") was split in two, no words moved, so the region's swallowed span covers only the target sentence ("Active residuals, the current coverage headline (**208 reproducible / 97 audit-only / 0 gap / 305 total**), compact historical ledger, and gap findings.") and never touches the six frozen-historical digits (`14`, `15`×2, `20`, `266`) in the immediately-following sentence — verified: those six entries' own containment-ledger keys are unchanged, confirming Task 1's own "no ledger key moves" constraint held at the moment the region landed.
- The rendered region body is byte-identical to the pre-migration sentence (verified by direct string comparison, transcribed below); `_NARRATIVE_REGION_SURFACES_LOCK` and the roster's equality floor now cover three surfaces (`docs/README.md`, `docs/MEASUREMENT-MAP.md`, `CLAUDE.md`), and `cmd_check()`'s `_named_narrative_paths` dict (the loop-accumulated set the floor is fed) was extended with `CLAUDE_MD: "CLAUDE.md"`.
- The deferred-containment ledger was re-measured at the start of this plan's own session (26/26, matching every prior planning document's dated reading) and reconciled to 23 entries in the same commit as the region landing: the coverage-headline triple (`'208'`/`'97'`/`'305'`) disappeared outright once inside the new fence; every surviving entry was re-adjudicated against a fresh `--describe` invocation of its own naming gate in this session (never trusting the prior ledger's own reading), discovering that `('CLAUDE.md', '43')`'s "live-verified" reason had gone false (live `control_count` is now 44) — left ledgered, with a corrected reason, rather than fixed out of scope (see Deviations).
- `_CONTAINMENT_LEDGER_MAX` (26 → 23) and `_CONTAINMENT_LEDGER_KEYS_DIGEST` were re-pinned in the same commit; `containment_ledger_ratchet_problems()` and `containment_ledger_staleness_problems()` both return `[]` against the live state.
- A new `_containment_ledger_class_counts()` function classifies every surviving entry by the tag its own reason starts with (`CANNOT-REACH`=8, `FROZEN HISTORICAL`=6, `NOT A COUNT CLAIM`=9, summing to 23), published as three new `describe()` derived-counts fields and cited by `docs/gates/CONF-SURFACE.md`'s new disclosed bound (11) — pointing at the generated fields rather than hand-typing the counts, per the plan's own instruction.
- `RATCHET-02`'s size-only scope sentence was added to `_CONTAINMENT_LEDGER_MAX`'s own comment block, citing the concrete `('CLAUDE.md', '43')` instance as evidence rather than a hypothetical.
- Backlog `999.69` was updated to record the reconciliation with both endpoints and the per-class breakdown, and marked **still open** (not closed — the live ledger is not empty). A new backlog entry, `999.73`, was filed for the 9 not-a-count-claim entries, the next free `999.x` id, confirmed by listing existing ids.
- Two new `--self-test` controls (`control_count` 107 → 109): `claude-headline-region-chained-not-reread` and `containment-ledger-class-counts-cover-ledger` (the latter also asserts an unclassified reason raises rather than silently reading as zero).
- The literal ledger was confirmed untouched throughout: `len(_DEFERRED_LITERAL_HITS) == _DEFERRED_LEDGER_MAX` (181/181) held before, during, and after every edit in this plan.

## Task Commits

Per the plan's own must_haves ("the re-pin lands in the same commit as the reconciliation that moved it," D-05 proviso 1), Tasks 1 and 2 were landed as a single commit rather than two — see Deviations for the full reasoning.

1. **Tasks 1+2 combined: land CLAUDE.md's third narrative region and reconcile/re-pin the containment ledger** — `49bb351` (feat)

Task 3 (backlog updates) touches only `.planning/ROADMAP.md` and `.planning/REQUIREMENTS.md`, both gitignored (`commit_docs: false`) — no git commit produced, confirmed via `git check-ignore -v`.

**Plan metadata:** this SUMMARY.md and the STATE.md/ROADMAP.md/REQUIREMENTS.md updates are committed together as the plan's closing metadata commit — `.planning/STATE.md`, `.planning/ROADMAP.md` and `.planning/REQUIREMENTS.md` stay gitignored per project convention (`commit_docs: false`) and are not part of that commit's file list beyond what the harness force-tracks (this SUMMARY.md).

## Files Created/Modified

- `scripts/gen-gate-docs.py` — `CLAUDE_HEADLINE_MARKERS`, `_CLAUDE_HEADLINE_BOOTSTRAP_AFTER`/`_BEFORE`, the third `_NARRATIVE_REGIONS` entry, the extended `_NARRATIVE_REGION_SURFACES_LOCK`, the new `generate_all()` call site (chained onto `targets[CLAUDE_MD]`), the extended `_named_narrative_paths` dict in `cmd_check()`, the reconciled `_DEFERRED_CONTAINMENT_HITS` (26 → 23 entries, every surviving reason re-tagged by class), the re-pinned `_CONTAINMENT_LEDGER_MAX`/`_CONTAINMENT_LEDGER_KEYS_DIGEST` with RATCHET-02's scope sentence, `_containment_ledger_class_counts()` and its three new `describe()` fields, one new `LITERAL_SCAN_DISCLOSED_BOUNDS` anchor, an updated `_control_region_preserves_surrounding_prose` (accounting for the second chained region), and two new `--self-test` controls.
- `CLAUDE.md` — a second generated region (marker lines added around the coverage-headline sentence, one physical line split in two so the bootstrap anchors land cleanly outside the following frozen-historical sentence); the coverage-headline sentence's own bytes are unchanged.
- `docs/gates/CONF-SURFACE.md` — Facts fence regenerated (`derived_counts` 35 → 38 entries, `disclosed_bounds_anchors` 11 → 12, `control_ids`/`control_count` 107 → 109); bound (10) updated for the third roster surface, new disclosed bound (11) for the containment-ledger reconciliation delta.
- `docs/ARCHITECTURE.md` — CONF-SURFACE's generated gate-table row cell updated to match, as the mechanical `--write` regeneration side effect; no other cell changed.
- `.planning/ROADMAP.md` (gitignored) — backlog `999.69` updated with the reconciliation record, kept open; new backlog `999.73` filed for the not-a-count-claim class.
- `.planning/REQUIREMENTS.md` (gitignored) — `CONTAIN-04` and `RATCHET-02` annotated in place with the containment-half completion and the outstanding literal-ledger half; neither checkbox ticked.

## Decisions Made

See `key-decisions` in the frontmatter above (verbatim, not repeated here per `docs/PROCESS.md` §1's own citation-not-restatement rule).

## Deviations from Plan

**1. [Same-commit coupling, per the plan's own must_haves — not a Rule 1-4 fix] Tasks 1 and 2 landed as a single commit rather than two.**
- **Found during:** preparing Task 1's own commit, after landing the region in isolation.
- **What happened:** the moment CLAUDE.md's coverage-headline region landed, three containment-ledger entries (`'208'`, `'97'`, `'305'`) lost their underlying live finding, which `containment_ledger_staleness_problems()` reports as a `cmd_check()` failure — and the pre-commit hook's own gate 4 (`gen-gate-docs.py --self-test`) exercises `cmd_check()` against the real tree in several controls. A Task-1-only commit would therefore fail its own pre-commit hook.
- **Why:** this is exactly the scenario the plan's own must_haves anticipated ("`_CONTAINMENT_LEDGER_MAX` and `_CONTAINMENT_LEDGER_KEYS_DIGEST` are re-pinned to the live values in the same commit that moved them") and the harness's own sequential-execution instructions named explicitly for this plan.
- **Impact:** one larger commit (`49bb351`) instead of two; every acceptance criterion from both tasks was independently verified before that single commit was made (see the transcripts below).

**2. [Rule 4-adjacent scope decision, not architectural — resolved without a checkpoint] `('CLAUDE.md', '43')` was found factually wrong but deliberately left unfixed.**
- **Found during:** Task 2's re-derivation pass, re-invoking `check-conf-gate.py --describe` for every "live fact" reason.
- **Issue:** the ledger's own reason for `'43'` read "live-verified" against `check-conf-gate.py --describe`'s `control_count`; a fresh invocation in this session returns `44`, not `43` — the value went stale one day after the ledger entry was written (research's own finding, re-confirmed here). Fixing `CLAUDE.md`'s own line (`"(43 controls)"` → `"(44 controls)"`) would have closed this containment-ledger entry, but it also would have moved `_DEFERRED_LITERAL_HITS`' own twin entry for the identical text (`('CLAUDE.md', '(43 controls)')`, backlog `999.42`) — a same-size key substitution that this plan's own acceptance criteria explicitly hold out of scope ("the literal ledger is untouched in this plan... If the literal ledger moved, stop and report before committing").
- **Fix:** reverted the prose fix; left `('CLAUDE.md', '43')` ledgered under `999.69`, with its reason corrected to document the discovery (the value is now known-false, cited as RATCHET-02's own motivating example) rather than silently keeping a reason already known wrong.
- **Files modified:** `scripts/gen-gate-docs.py` (the ledger entry's reason text and the `_CONTAINMENT_LEDGER_MAX` comment's growth/shrink history).
- **Verification:** `containment_ledger_ratchet_problems()`/`staleness_problems()` both `[]`; `len(_DEFERRED_LITERAL_HITS) == _DEFERRED_LEDGER_MAX` (181/181) confirmed unchanged before and after this decision.
- **Committed in:** `49bb351`.

Both deviations are scope-discipline decisions the plan's own text and the harness's sequential-execution instructions anticipated; neither required a checkpoint.

## Issues Encountered

**A cross-invocation convergence gap in `--write`.** The first `--write` call computed `docs/gates/CONF-SURFACE.md`'s own Facts fence (via this module's own `--describe`, subprocess-invoked by `harvest()`) against CLAUDE.md's **pre-region** on-disk state, since `harvest()` runs before `generate_all()`'s in-memory targets are ever written back to disk — producing a transiently stale `chain_termini_*`/`narrative_restatement_*` reading baked into that first write. A second `--write` (against the now-updated on-disk `CLAUDE.md`) converged; a third confirmed idempotency. This matches Task 1's own acceptance criterion 4 ("`--write` run twice produces no diff on the second run") — resolved by running it twice, as that criterion anticipates, rather than treating the first pass's transient reading as a bug.

## In-Process Verification Transcripts

**Pre-migration readings, taken by module import before any edit in this plan (commit `ae32a6c`):**

```
len(_DEFERRED_LITERAL_HITS) / _DEFERRED_LEDGER_MAX          -> 181 / 181
len(_DEFERRED_CONTAINMENT_HITS) / _CONTAINMENT_LEDGER_MAX    -> 26 / 26
_CONTAINMENT_LEDGER_KEYS_DIGEST (before)                     -> sha256:67bc2d748bdb3330e701bc90c6b7660f1e849fcebdcf8fb36d0f44f589b78f94
_generated_marker_pairs_for("CLAUDE.md")                     -> (CLAUDE_REGION_MARKERS,)   [1-element]
control_count (before)                                        -> 107
disclosed_bounds_anchors (before)                              -> 11
/usr/bin/grep -c "END GENERATED" CLAUDE.md                    -> 1
```

**Task 1 -- END GENERATED grep readings:**

| Reading point | Count |
|---|---|
| Before this plan | 1 |
| After this plan | 2 |

**Task 1 -- byte comparison, rendered region body vs. the exact pre-migration sentence:**

```
pre      : 'Active residuals, the current coverage headline (**208 reproducible / 97 audit-only / 0 gap / 305 total**), compact historical ledger, and gap findings.'
rendered : 'Active residuals, the current coverage headline (**208 reproducible / 97 audit-only / 0 gap / 305 total**), compact historical ledger, and gap findings.'
IDENTICAL: True
```

**Task 1 -- marker-pair registration:**

```
_generated_marker_pairs_for("CLAUDE.md") -> (CLAUDE_REGION_MARKERS, CLAUDE_HEADLINE_MARKERS)   [2-element tuple]
4 marker strings, pairwise distinct: True
```

**Task 1 -- chaining proof (new control `claude-headline-region-chained-not-reread`):**

```
generate_all()[CLAUDE_MD] contains CLAUDE_REGION_MARKERS[0]/[1]     -> True / True (CI-gate table survived)
generate_all()[CLAUDE_MD] contains CLAUDE_HEADLINE_MARKERS[0]/[1]   -> True / True (new region present)
```

**Task 1 -- no ledger key moved (re-derived immediately after the region landed, before Task 2's reconciliation):**

```
len(_DEFERRED_LITERAL_HITS) / _DEFERRED_LEDGER_MAX          -> 181 / 181 (unchanged)
len(_DEFERRED_CONTAINMENT_HITS) / _CONTAINMENT_LEDGER_MAX    -> 26 / 26 (unchanged -- the DICT itself; the mechanism's own staleness predicate began reporting 3 stale keys, which is the finding Task 2 reconciles, not a change to the ledger dict)
```

**Task 2 -- `--emit-containment-ledger` diff, before and after the region:**

```
Before region: 26 keys (matches committed _DEFERRED_CONTAINMENT_HITS exactly)
After region:  23 keys ('208'/'97'/'305' gone; all else unchanged)
```

**Task 2 -- `--describe` invocations proving every cannot-reach classification, transcribed:**

```
$ python3 scripts/check-description-budget.py --describe
{"locked_constants": {"cap": 2000}}                                     # no field for '1024'

$ python3 scripts/check-version-stamps.py --describe
{"derived_counts": {"stamp_source_kind_count": 4},
 "registered_surfaces": [".claude-plugin/marketplace.json",
   "first-principles/.claude-plugin/plugin.json",
   "shared/skills/*/SKILL.md", "shared/spine/SKILL.meta.yml"]}          # no field for '17' or ARCHITECTURE.md's '14'

$ python3 scripts/check-step0-live.py --describe
{"control_count": 25, ...}                                              # no field for '60'

$ python3 scripts/check-routing-battery.py --describe
{"locked_constants": {"boundary_n_threshold": 2, "boundary_p_threshold": 2,
  "focused_n_threshold": 1, "focused_p_threshold": 4}}                  # no field for MIN_HEADER_HITS ('2') or _COMPOSER_FOCUS_CEILING ('4')

$ file scripts/check-firewall-battery.sh
scripts/check-firewall-battery.sh: Bourne-Again shell script            # no --describe leg at all; '24' cannot be harvested

$ python3 scripts/check-conf-gate.py --describe | python3 -c "import json,sys; print(json.load(sys.stdin)['control_count'])"
44                                                                       # '43' is STALE -- see Deviations
```

**Task 2 -- per-entry adjudication table (23 surviving entries, class and backlog id):**

| Surface | Key | Class | Backlog |
|---|---|---|---|
| CLAUDE.md | `03` | not-a-count-claim | 999.73 |
| CLAUDE.md | `1024` | cannot-reach | 999.69 |
| CLAUDE.md | `14` | frozen-historical | 999.69 |
| CLAUDE.md | `15` | frozen-historical | 999.69 |
| CLAUDE.md | `17` | cannot-reach | 999.69 |
| CLAUDE.md | `20` | frozen-historical | 999.69 |
| CLAUDE.md | `22` | not-a-count-claim | 999.73 |
| CLAUDE.md | `24` | cannot-reach | 999.69 |
| CLAUDE.md | `260728` | not-a-count-claim | 999.73 |
| CLAUDE.md | `266` | frozen-historical | 999.69 |
| CLAUDE.md | `43` | cannot-reach (found stale, left unfixed) | 999.69 |
| CLAUDE.md | `60` | cannot-reach | 999.69 |
| docs/ARCHITECTURE.md | `03` | not-a-count-claim | 999.73 |
| docs/ARCHITECTURE.md | `14` | cannot-reach | 999.69 |
| docs/ARCHITECTURE.md | `644` | frozen-historical | 999.69 |
| docs/TESTING.md | `1` | not-a-count-claim | 999.73 |
| docs/TESTING.md | `2` | cannot-reach | 999.69 |
| docs/TESTING.md | `2156` | not-a-count-claim | 999.73 |
| docs/TESTING.md | `2178` | not-a-count-claim | 999.73 |
| docs/TESTING.md | `3` | not-a-count-claim | 999.73 |
| docs/TESTING.md | `4` | cannot-reach | 999.69 |
| docs/TESTING.md | `5` | not-a-count-claim | 999.73 |
| docs/TESTING.md | `644` | frozen-historical | 999.69 |

**Arithmetic:** cannot-reach=8, frozen-historical=6, not-a-count-claim=9; `8 + 6 + 9 = 23`, matching the live ledger size exactly. `_containment_ledger_class_counts()` (generated, not hand-typed): `{'not_a_count_claim': 9, 'frozen_historical': 6, 'cannot_reach': 8}`.

**Task 2 -- ratchet re-pin, transcribed:**

```
_CONTAINMENT_LEDGER_MAX:            26 -> 23
_CONTAINMENT_LEDGER_KEYS_DIGEST:    sha256:67bc2d74... -> sha256:ac8790ce65be987c8714f7f0bc27fb02b1749d2c1b4e7f23a66f64a927a03ff8
containment_ledger_ratchet_problems()     -> []
containment_ledger_staleness_problems()   -> []
literal_ledger_ratchet_problems()         -> [] (literal ledger untouched: 181/181)
```

```
$ git show --stat 49bb351
 CLAUDE.md                  |   9 +-
 docs/ARCHITECTURE.md       |   2 +-
 docs/gates/CONF-SURFACE.md |  46 ++++--
 scripts/gen-gate-docs.py   | 337 +++++++++++++++++++++++++++++++++++++-------
 4 files changed, 328 insertions(+), 66 deletions(-)
```

Both the reconciliation (ledger dict, ratchet pin, key digest) and the region landing are in this one commit, confirming D-05 proviso 1.

**Task 2 -- literal-scan test on all new prose before writing to disk:**

```
_scan_text_for_literal_hits() over bound (10)'s updated text -> 0 hits
_scan_text_for_literal_hits() over bound (11)'s new text     -> 0 hits (first draft had 2 hits: 'three entries', 'one entry' -- reworded before writing, per Pitfall 3's own discipline)
/usr/bin/grep -rn "tens, not hundreds" docs/ scripts/ CLAUDE.md -> (no matches)
```

**Task 2 -- `LITERAL_SCAN_DISCLOSED_BOUNDS` anchor count:**

```
Before: 11 anchors, disclosed_bounds_anchors=11
After:  12 anchors, disclosed_bounds_anchors=12   (+1: "containment-ledger-reconciliation-delta")
```

**Final verify, all green:**

```
python3 scripts/gen-gate-docs.py --self-test        # SELF-TEST PASS -- 109 controls run
python3 scripts/gen-gate-docs.py --check             # exit 0; harvested 22/22 expected script-backed entries
python3 scripts/check-traceability.py --self-test    # PASS (HEADLINE-LOCK finds the current headline on all surfaces, including CLAUDE.md)
sh .githooks/pre-commit                              # all five gates PASS, exit 0
bash scripts/check-firewall-battery.sh               # FIREWALL: GREEN (26/26)
```

**Ledger readings, both taken by module import, before this plan and after its single commit:**

| Reading point | `len(_DEFERRED_LITERAL_HITS)` | `_DEFERRED_LEDGER_MAX` | `len(_DEFERRED_CONTAINMENT_HITS)` | `_CONTAINMENT_LEDGER_MAX` |
|---|---|---|---|---|
| Before this plan | 181 | 181 | 26 | 26 |
| After this plan | 181 | 181 | 23 | 23 |

`git diff --diff-filter=D --name-only` on the single commit returned empty — no unexpected deletions. `git status --porcelain` was clean before the first edit; `git diff --name-only` from this plan's base commit (`ae32a6c`) lists exactly `CLAUDE.md`, `docs/ARCHITECTURE.md`, `docs/gates/CONF-SURFACE.md`, `scripts/gen-gate-docs.py` — neither `.github/workflows/validation.yml` nor `scripts/check-firewall-battery.sh` appears; the battery tally is unchanged at 26/26.

## Assumption Drift (advisory)

None material. One color note: the plan's own action text anticipated the region and the reconciliation as two separate tasks with (implicitly) two commits; the plan's own must_haves and the harness's sequential-execution instructions both explicitly anticipated the same-commit coupling this plan actually required, so the single-commit shape is a documented, expected outcome of the plan's own stated constraint rather than a drift from it.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- Plan 26-06 (the deferred-**literal** ledger's own reconciliation and `_DEFERRED_LEDGER_MAX` re-pin, CONTAIN-04's other half) can proceed directly: the literal ledger is confirmed untouched throughout this plan (181/181, digest unchanged), and `('CLAUDE.md', '(43 controls)')`'s own twin entry (backlog 999.42) is an explicit, documented candidate for that plan's own reconciliation pass — its underlying prose ("43 controls") is still the CLAUDE.md hand-written line this plan deliberately left uncorrected.
- Backlog `999.73` (the not-a-count-claim shape-stripping class) is filed and ready for a future REACH-scoped plan; it does not block Phase 26's own closure since D-06 proviso 2 only requires it be published and named, not closed in-phase.
- No blockers. `FIREWALL: GREEN (26/26)`, tally unchanged; CI job count unchanged at 23 (unverified count claim by construction — not re-derived in this plan, since neither `.github/workflows/validation.yml` nor `scripts/check-firewall-battery.sh` appears in this plan's own `git diff --name-only`).

---
*Phase: 26-migration-apply-reconcile-generalize-enforce*
*Completed: 2026-09-10*

## Self-Check: PASSED

- FOUND: `scripts/gen-gate-docs.py`
- FOUND: `CLAUDE.md`
- FOUND: `docs/gates/CONF-SURFACE.md`
- FOUND: `docs/ARCHITECTURE.md`
- FOUND: commit `49bb351` in `git log --oneline --all`
