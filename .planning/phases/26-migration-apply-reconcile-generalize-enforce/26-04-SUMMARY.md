---
phase: 26-migration-apply-reconcile-generalize-enforce
plan: 04
subsystem: infra
tags: [gen-gate-docs, narrative-region, cmd_check, literal-scan, self-test, ratchet]

# Dependency graph
requires:
  - phase: 26-migration-apply-reconcile-generalize-enforce
    plan: 03
    provides: >-
      The inert NARR-02 mechanism (_NARRATIVE_REGIONS roster, equality-floored
      lock, sentence renderer, harvest-free restatement census, and the
      generated-narrative-region exemption-class entry) with nine passing
      self-test controls, unwired to any host surface or to cmd_check()
  - phase: 26-migration-apply-reconcile-generalize-enforce
    plan: 02
    provides: >-
      docs/PROCESS.md §2's generalized digit-narrowing rule and the
      pre-migration census naming docs/README.md:20 and
      docs/MEASUREMENT-MAP.md:54 as the two NARR-02 region candidates
provides:
  - "Two bootstrapped generated regions on docs/README.md and docs/MEASUREMENT-MAP.md, registered in _generated_marker_pairs_for() -- the actual suppression mechanism -- and wired via two new _replace_or_bootstrap_region() call sites in generate_all()"
  - "The narrative-region roster's equality floor and the restatement census's 'finding'-class subset wired into cmd_check(), fed the surface-key set the generate_all() loop itself accumulates, never a table-derived default"
  - "Five new derived_counts fields (narrative_regions, narrative_restatement_finding/in_region/fenced/chain_hop) published on docs/gates/CONF-SURFACE.md's Facts fence"
  - "A new numbered disclosed bound (10) stating what the two regions now guarantee and what they do not"
  - "Two new --self-test controls (105 -> 107), each proven non-vacuous by induced failure, plus two pre-existing controls' hardcoded target counts updated (+3 -> +5) for the widened generate_all() target set"
affects: [26-05, 26-06, 26-07]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Widened a _NarrativeRegion template beyond its bare digit-bearing clause to the full swallowed span (surrounding blockquote paragraph, or a following horizontal rule) when no unique, non-fenced bootstrap anchor sits directly adjacent to the sentence -- reproduced whole, never truncated, per D-02's one-sentence rule"
    - "Monkeypatching generate_all/narrative_restatement_problems via _this_module to prove a cmd_check() call site is fed a genuinely-accumulated set, not a table-derived default (the established containment-loop precedent, reused for the narrative roster)"

key-files:
  created: []
  modified:
    - scripts/gen-gate-docs.py
    - docs/README.md
    - docs/MEASUREMENT-MAP.md
    - docs/gates/CONF-SURFACE.md
    - CLAUDE.md
    - docs/ARCHITECTURE.md

key-decisions:
  - "Widened both _NARRATIVE_REGIONS templates (built narrow by 26-03) to cover the full paragraph/rule span the bootstrap anchors necessarily swallow, rather than leaving the templates as the bare digit-bearing clause -- no unique, non-fenced anchor line sits directly adjacent to either sentence: docs/README.md's sentence sits inside a blockquote (splitting it would detach the coverage-headline clause from its own lead-in into a separate visual quote box), and docs/MEASUREMENT-MAP.md's nearest usable anchor is a heading two lines past a horizontal rule that repeats four times elsewhere on the page and cannot itself serve as an anchor. Verified byte-identical against the exact pre-migration span (not just the digit clause) before writing either template."
  - "Reworded _control_page_check_dispatch_wired's docstring to keep 'plan\" / \"21-08's Task 1' on the same line-break boundary as the original text, after a first draft's rewrap tripped CONF-13's own self-file docstring ratchet (a phrase that reads fine as prose only becomes a new hit when its physical line-wrapping changes which words sit adjacent)."
  - "Added disclosed bound (10) to docs/gates/CONF-SURFACE.md rather than folding its content into bound (9), since bound (9) is a published pre-migration finding (a structural gap) and bound (10) is a post-migration capability statement (what the two wired regions now guarantee and do not) -- different claims, kept as separate numbered entries."

requirements-completed: [NARR-02, RATCHET-01]

# Metrics
duration: ~90min
completed: 2026-09-10
---

# Phase 26 Plan 04: NARR-02/RATCHET-01 wired live Summary

**Registered docs/README.md and docs/MEASUREMENT-MAP.md's marker pairs in `_generated_marker_pairs_for()` (the actual suppression mechanism), bootstrapped both narrative regions live via `generate_all()`, and wired the roster equality floor plus the restatement census into `cmd_check()` -- proven by a scratch-copy mutation that a hand-typed restatement on either surface now blocks a commit.**

## Performance

- **Duration:** ~90 min
- **Tasks:** 2
- **Files modified:** 6 (`scripts/gen-gate-docs.py`; `docs/README.md`, `docs/MEASUREMENT-MAP.md` as the bootstrapped hosts; `docs/gates/CONF-SURFACE.md`, `CLAUDE.md`, `docs/ARCHITECTURE.md` as the mechanical `--write` regeneration side effect of the new derived-counts fields and disclosed bound)

## Accomplishments

- `docs/README.md` and `docs/MEASUREMENT-MAP.md` each carry a generated one-region span rendering the live coverage headline, registered in `_generated_marker_pairs_for()` and wired via two new `_replace_or_bootstrap_region()` call sites in `generate_all()`, following the CLAUDE.md/ARCHITECTURE.md/TESTING.md shape exactly.
- Both regions' templates were widened from the bare digit-bearing clause 26-03 built to the full swallowed span (docs/README.md's entire quoted blockquote paragraph; docs/MEASUREMENT-MAP.md's sentence plus its following horizontal rule), because no unique, non-fenced bootstrap anchor sits directly adjacent to either sentence. Byte comparison confirms the rendered content is identical to the exact pre-migration span; `git diff` on both hosts shows only inserted marker lines, zero removed or reworded prose.
- `python3 scripts/check-traceability.py --self-test` confirms HEADLINE-LOCK still finds the current, non-historical headline on both surfaces after the migration.
- `narrative_region_surface_roster_problems()` and `narrative_restatement_problems()`'s `'finding'`-class subset are now called from `cmd_check()`, fed the surface-key set the `generate_all()` loop itself accumulates from `pass1` (never `{r.surface for r in _NARRATIVE_REGIONS}`) -- the identical T-26-03 argument the containment loop's own roster floor already makes.
- `describe()`'s `derived_counts` gained five new fields (`narrative_regions=2`, `narrative_restatement_finding=0`, `narrative_restatement_in_region=4`, `narrative_restatement_fenced=0`, `narrative_restatement_chain_hop=0`), rendered into `docs/gates/CONF-SURFACE.md`'s Facts fence by `--write`.
- `docs/gates/CONF-SURFACE.md` gained numbered disclosed bound (10), stating what the two regions now guarantee (a rendered sentence's currency, plus no surviving hand-typed restatement on either roster surface) and what they do not (a third page's restatement; any other hand-typed count on either page) -- pointing at the generated `derived_counts` fields rather than restating their values. Bound (9)'s stale "region candidates for a later plan in this phase" phrasing was updated now that the wiring has landed.
- Two new `--self-test` controls (`control_count` 105 -> 107): one monkeypatches `generate_all` to drop `docs/README.md`'s target and confirms `cmd_check()` names it missing from the accumulated set; the other monkeypatches `narrative_restatement_problems` itself and confirms `cmd_check()`'s exit code and stderr genuinely reflect its return value in both directions. Both proven non-vacuous by induced failure (transcript below).
- The migration was measured, not estimated: the pre-migration census (26-02-SUMMARY.md) found both region candidates as bare hand-typed prose (`in-region=False`); the identical re-derived census now finds both `in-region=True`, while the structurally-unreachable `docs/COMPONENT-DIAGRAM.md` occurrence and the plan-26-05-scoped `CLAUDE.md` occurrence are unchanged (see the Before/After table below).
- Neither ledger moved (`_DEFERRED_LITERAL_HITS` 181/181, `_DEFERRED_CONTAINMENT_HITS` 26/26), confirmed by module import before Task 1 and after Task 2. `FIREWALL: GREEN (26/26)` held throughout; `git diff --name-only` never touched `.github/workflows/validation.yml` or `scripts/check-firewall-battery.sh`.

## Task Commits

1. **Task 1: Register the marker pairs and bootstrap the two regions** -- `1369236` (feat)
2. **Task 2: Wire the roster equality floor and the restatement census into cmd_check, and measure the migration** -- `ab28004` (feat)

**Plan metadata:** this SUMMARY.md and the STATE.md/ROADMAP.md/REQUIREMENTS.md updates are committed together as the plan's closing metadata commit -- `.planning/STATE.md`, `.planning/ROADMAP.md` and `.planning/REQUIREMENTS.md` stay gitignored per project convention (`commit_docs: false`) and are not part of that commit's file list beyond what the harness force-tracks (this SUMMARY.md).

## Files Created/Modified

- `scripts/gen-gate-docs.py` -- `README_MD`/`MEASUREMENT_MAP_MD` path constants, two bootstrap-anchor constant pairs, the two widened `_NARRATIVE_REGIONS` templates, two new `_generated_marker_pairs_for()` arms, two new `generate_all()` call sites, the `cmd_check()` narrative-roster/restatement wiring, five new `describe()` derived-counts fields, one new `LITERAL_SCAN_DISCLOSED_BOUNDS` anchor, two updated pre-existing self-test controls (target-count assertions and a docstring reword), and two new self-test controls.
- `docs/README.md`, `docs/MEASUREMENT-MAP.md` -- each now carries one generated region (marker lines only added; the coverage-headline sentence's bytes are unchanged).
- `docs/gates/CONF-SURFACE.md` -- Facts fence regenerated (`derived_counts` 30 -> 35 entries, `disclosed_bounds_anchors` 10 -> 11, `control_ids`/`control_count` 105 -> 107); new disclosed bound (10) and a wording update to bound (9).
- `CLAUDE.md`, `docs/ARCHITECTURE.md` -- CONF-SURFACE's generated gate-table row cell updated to match, as the mechanical `--write` regeneration side effect; no other cell on either row changed.

## Decisions Made

See `key-decisions` in the frontmatter above (verbatim, not repeated here per `docs/PROCESS.md` §1's own citation-not-restatement rule).

## Deviations from Plan

**1. [Rule 1 - Bug] Two pre-existing self-test controls hardcoded `generate_all()`'s prior target count (+3).**
- **Found during:** Task 1, first `--self-test` run after wiring the two new `generate_all()` call sites.
- **Issue:** `_control_page_per_entry` and `_control_page_check_dispatch_wired` both asserted `len(targets) == len(expected) + 3` (the three surface files this file's own history migrated before this plan). Adding two more `generate_all()` targets made both assertions fail.
- **Fix:** Updated both assertions to `+ 5`, added `README_MD`/`MEASUREMENT_MAP_MD` membership checks to `_control_page_per_entry`, and updated `_control_page_check_dispatch_wired`'s docstring to name the two new surfaces.
- **Files modified:** `scripts/gen-gate-docs.py`.
- **Verification:** `python3 scripts/gen-gate-docs.py --self-test` passes (107 controls).
- **Committed in:** `1369236` (Task 1 commit).

**2. [Rule 1 - Bug] A docstring rewrap tripped CONF-13's own self-file literal-scan ratchet.**
- **Found during:** Task 1, same self-test run.
- **Issue:** The first draft of `_control_page_check_dispatch_wired`'s widened docstring reflowed its line breaks, moving "As of plan" and "21-08's Task 1" onto the same physical line for the first time -- the scanner's count-noun-adjacent detection is line-scoped, and this reflow produced a new hit (`nonmodule-docstring self-file ratchet`, live 30 vs. pinned 29) that did not exist in the original wording.
- **Fix:** Rewrote the paragraph to preserve the original line-break boundary around that phrase while still naming the two new surfaces, re-scanned in-process (0 hits from this docstring beyond the pre-existing, already-ledgered "five surface" hit), then wrote to disk.
- **Files modified:** `scripts/gen-gate-docs.py`.
- **Verification:** `python3 scripts/gen-gate-docs.py --self-test` passes with the pin unmoved at 29.
- **Committed in:** `1369236` (Task 1 commit).

Both are Rule 1 (bug) fixes to the test suite's own bookkeeping made necessary by widening `generate_all()`'s target population -- neither changes product behavior beyond what the plan's own action items already specified.

## Issues Encountered

**Choosing bootstrap anchors that do not swallow unrelated prose.** Neither host page has a unique, non-fenced whole line directly adjacent to its coverage-headline sentence: `docs/README.md`'s sentence sits inside a blockquote (the line immediately after it, a bare `>` blockquote-continuation marker, repeats four times on the page), and `docs/MEASUREMENT-MAP.md`'s nearest candidate anchor is a horizontal rule (`---`) that repeats four times elsewhere on the page. Resolved per the plan's own action instruction ("have the template reproduce every byte between the anchors ... The unit of generation stays one whole sentence even when that sentence spans several quoted lines") by widening each region's template to reproduce the full swallowed span verbatim -- confirmed by direct byte comparison against the pre-migration text (see transcript below) rather than by inspection alone.

## In-Process Verification Transcripts

**Task 1 -- byte-identity comparison, rendered region body vs. the exact pre-migration span:**

```
README.md rendered:  '> **Current state — start here:** [`requirements-traceability.md`]
(requirements-traceability.md)\n> — the authoritative surface: active residuals,
dispositions, and the **current** coverage\n> headline of **208 reproducible / 97
audit-only / 0 gap / 305 total**.\n>'
README.md span (file lines 18-21, joined):  IDENTICAL

MEASUREMENT-MAP.md rendered:  'For the complete Active-Surface list and the coverage
headline (208 reproducible / 97 audit-only / 0 gap / 305 total), see
[requirements-traceability.md](requirements-traceability.md).\n\n---'
MEASUREMENT-MAP.md span (file lines 54-56, joined):  IDENTICAL
```

**Task 1 -- `END GENERATED` grep readings:**

| Surface | Before (26-02/26-03 dated reading) | After |
|---|---|---|
| `docs/README.md` | 0 | 1 |
| `docs/MEASUREMENT-MAP.md` | 0 | 1 |

**Task 1 -- `git diff docs/README.md docs/MEASUREMENT-MAP.md`:** both diffs contain `+` lines only (the two marker lines per host); zero `-` lines on either page.

**Task 1 -- automated verify, all green:**

```
python3 scripts/gen-gate-docs.py --check                # exit 0
python3 scripts/check-traceability.py --self-test        # PASS; HEADLINE-LOCK finds the
                                                           # current headline on both new surfaces
sh .githooks/pre-commit                                   # all five gates PASS, exit 0
```

**Task 1 -- registration check:**

```
_generated_marker_pairs_for("docs/README.md")           -> (README_HEADLINE_MARKERS,)
_generated_marker_pairs_for("docs/MEASUREMENT-MAP.md")  -> (MEASUREMENT_MAP_HEADLINE_MARKERS,)
_generated_marker_pairs_for("CLAUDE.md")                -> unchanged (CLAUDE_REGION_MARKERS,)
len(_DEFERRED_LITERAL_HITS) / _DEFERRED_LEDGER_MAX          -> 181 / 181 (before and after)
len(_DEFERRED_CONTAINMENT_HITS) / _CONTAINMENT_LEDGER_MAX   -> 26 / 26 (before and after)
```

**Task 2 -- `--describe` census fields, transcribed:**

```
narrative_regions = 2
narrative_restatement_finding = 0
narrative_restatement_in_region = 4
narrative_restatement_fenced = 0
narrative_restatement_chain_hop = 0
```

The `in_region=4` reading is expected, not a defect: both regions render the identical `coverage_headline.prose` value, and the census checks every roster surface for every region's own value, so each region's value is found "in-region" on both surfaces (2 regions x 2 surfaces = 4).

**Task 2 -- Before/After migration census (re-running 26-02-SUMMARY.md's exact enumeration):**

| Surface | Pre-migration (26-02) | Post-migration (this plan) | Class change |
|---|---|---|---|
| `docs/PROCESS.md` | (no occurrence) | (no occurrence) | unchanged |
| `docs/README.md` | line 20, `in-region=False` (region candidate) | line 21, `in-region=True` | **region candidate -> in-region** |
| `CONTRIBUTING.md` | (no occurrence) | (no occurrence) | unchanged |
| `docs/MEASUREMENT-MAP.md` | line 54, `in-region=False` (region candidate) | line 55, `in-region=True` | **region candidate -> in-region** |
| `docs/COMPONENT-DIAGRAM.md` | line 98, `fenced=True` (structurally unreachable, bound (9)) | line 98, `fenced=True` | unchanged (out of D-01's reach by construction) |
| `docs/DATA-FLOW.md` | (no occurrence) | (no occurrence) | unchanged |
| `CLAUDE.md` | line 312, `in-region=False` (plan 26-05's own target) | line 312, `in-region=False` | unchanged (deliberately out of this plan's scope) |

Delta: 2 of 2 region candidates the pre-migration census named are now generated regions (`in-region=True`); the one structurally-unreachable occurrence and the one plan-26-05-scoped occurrence are unchanged, as expected.

**Task 2 -- new self-test controls, induced-failure transcript:**

| Control id | Induced mutation | Failure observed |
|---|---|---|
| `narrative-roster-accumulated-not-table-derived` | monkeypatched `narrative_region_surface_roster_problems` to always return `[]` (simulating a table-derived no-op) | `AssertionError: cmd_check() returned 0, expected 1 with docs/README.md missing from pass1` |
| `narrative-restatement-wired-into-cmd-check` | monkeypatched `cmd_check` itself to always return 0 (simulating an un-wired dispatch) | `AssertionError: cmd_check() returned 0, expected 1 with a stubbed restatement finding` |

**Task 2 -- `control_count` readings:** before Task 2, `105`; after Task 2, `107` (grew by exactly the 2 controls added).

**Task 2 -- `narrative_region_surface_roster_problems` call-site check:**

```
$ /usr/bin/grep -n "narrative_region_surface_roster_problems" scripts/gen-gate-docs.py
1614: def narrative_region_surface_roster_problems(       # definition
4348:     problems += narrative_region_surface_roster_problems(narrative_reached)   # THE call site
6370, 6381, 6395: self-test controls (explicit synthetic sets, not the module's roster)
```

No call site passes a comprehension over `_NARRATIVE_REGIONS`.

**Task 2 -- scratch-copy mutation transcript (real repository never touched):**

```
$ git status --porcelain                    # (empty) -- before the first mutation
$ git rev-parse HEAD                        # ab28004c9aee4c4c2538432543f5ce7abf7be47f

$ SCRATCH=$(mktemp -d); rsync -a --exclude .git . "$SCRATCH"/

# Arm A -- mutate the scratch copy: append a hand-typed restatement of the
# coverage headline to docs/MEASUREMENT-MAP.md, OUTSIDE its own generated region.
$ echo "Stray restatement for testing: 208 reproducible / 97 audit-only / 0 gap / 305 total." \
    >> "$SCRATCH/docs/MEASUREMENT-MAP.md"

$ cd "$SCRATCH" && python3 scripts/gen-gate-docs.py --check
narrative-restatement: docs/MEASUREMENT-MAP.md:103 restates the value docs/README.md's own
  generated-narrative-region renders, outside any generated fence (NARR-02)
narrative-restatement: docs/MEASUREMENT-MAP.md:103 restates the value docs/MEASUREMENT-MAP.md's
  own generated-narrative-region renders, outside any generated fence (NARR-02)
harvested 22/22 expected script-backed entries (22 total)
CHECK EXIT: 1                                # non-zero, names the file and the exact line

# Arm B -- restore and confirm byte-identical
$ cp docs/MEASUREMENT-MAP.md "$SCRATCH/docs/MEASUREMENT-MAP.md"   # (from the real repo)
$ md5sum docs/MEASUREMENT-MAP.md "$SCRATCH/docs/MEASUREMENT-MAP.md"
b93fb0e52c0c8076ab3e8aa3a9e89f0b  docs/MEASUREMENT-MAP.md
b93fb0e52c0c8076ab3e8aa3a9e89f0b  /tmp/tmp.6STuV27TcU/docs/MEASUREMENT-MAP.md   # identical
$ cd "$SCRATCH" && python3 scripts/gen-gate-docs.py --check
CHECK EXIT: 0                                # restored, passes again

$ rm -rf "$SCRATCH"
$ git status --porcelain                     # (empty) -- after the last mutation
$ git rev-parse HEAD                         # ab28004c9aee4c4c2538432543f5ce7abf7be47f (unchanged)
```

**Final verify (this plan's own `<verification>` block, all green):**

```
python3 scripts/gen-gate-docs.py --self-test    # SELF-TEST PASS -- 107 controls run
python3 scripts/gen-gate-docs.py --check         # harvested 22/22 expected script-backed entries; exit 0
python3 scripts/check-traceability.py --self-test  # PASS
sh .githooks/pre-commit                           # all five gates PASS, exit 0 (run before each commit)
bash scripts/check-firewall-battery.sh            # FIREWALL: GREEN (26/26)
```

**Ledger readings, both taken by module import, before Task 1 and after Task 2:**

| Reading point | `len(_DEFERRED_LITERAL_HITS)` | `_DEFERRED_LEDGER_MAX` | `len(_DEFERRED_CONTAINMENT_HITS)` | `_CONTAINMENT_LEDGER_MAX` |
|---|---|---|---|---|
| Before Task 1 | 181 | 181 | 26 | 26 |
| After Task 2 | 181 | 181 | 26 | 26 |

`git diff --diff-filter=D --name-only` between every consecutive pair of commits in this plan returned empty -- no unexpected deletions. `git status --porcelain` was clean after each commit. `git diff --name-only` from this plan's base commit lists exactly `CLAUDE.md`, `docs/ARCHITECTURE.md`, `docs/MEASUREMENT-MAP.md`, `docs/README.md`, `docs/gates/CONF-SURFACE.md`, `scripts/gen-gate-docs.py` -- neither `.github/workflows/validation.yml` nor `scripts/check-firewall-battery.sh` appears.

## Assumption Drift (advisory)

None material. The plan's own `<interfaces>` block pre-named every identifier used here (`_NARRATIVE_REGIONS`, `_generated_marker_pairs_for`, `_replace_or_bootstrap_region`, `containment_surface_roster_problems`'s docstring precedent) and the two host surfaces exactly matched 26-02-SUMMARY.md's own measured region candidates -- no rediscovery or renaming was needed. One color note, not drift: the plan anticipated the bootstrap-anchor choice as a matter of "prefer anchors that are structural and unlikely to be reworded"; in practice neither host page offered such an anchor directly adjacent to the sentence, which the plan's own action text had already anticipated for `docs/README.md`'s blockquote case ("place the markers outside the blockquote... have the template reproduce every byte between the anchors") -- the same discipline was extended to `docs/MEASUREMENT-MAP.md`'s horizontal-rule case by the same reasoning, not a deviation from the plan's own instruction.

## User Setup Required

None -- no external service configuration required.

## Next Phase Readiness

- Plan 26-05 (CLAUDE.md's own third narrative region, together with the containment re-pin its region forces) can proceed directly: `CLAUDE.md`'s coverage-headline occurrence (line 312) was left untouched by this plan, exactly as this plan's own interfaces and `docs/gates/CONF-SURFACE.md`'s comment already scope it, and the two-surface roster lock (`_NARRATIVE_REGION_SURFACES_LOCK`) is explicitly NOT to be weakened to a subset test when the third surface is added -- it must be extended by equality, in the same commit as the containment re-pin, per the plan's own binding instruction.
- No blockers. Both ledgers confirmed unmoved (181/181, 26/26), which is the precondition the phase's own wave ordering (migrate first, re-pin last) depends on for the remaining waves.
- `pre-commit gate 5` (`gen-gate-docs.py --check`) now reaches a class of region it could not reach before this plan (RATCHET-01's substance), demonstrated live by the scratch-copy mutation above -- plan 26-07's own mutation demonstration can cite this transcript's shape rather than re-deriving it from scratch, though 26-07's own acceptance criteria may still require its own independent run per that plan's text.

---
*Phase: 26-migration-apply-reconcile-generalize-enforce*
*Completed: 2026-09-10*

## Self-Check: PASSED

- FOUND: `scripts/gen-gate-docs.py`
- FOUND: `docs/README.md`
- FOUND: `docs/MEASUREMENT-MAP.md`
- FOUND: `docs/gates/CONF-SURFACE.md`
- FOUND: `CLAUDE.md`
- FOUND: `docs/ARCHITECTURE.md`
- FOUND: commit `1369236` in `git log --oneline --all`
- FOUND: commit `ab28004` in `git log --oneline --all`
