---
phase: 26-migration-apply-reconcile-generalize-enforce
plan: 03
subsystem: docs
tags: [gen-gate-docs, narrative-region, literal-scan, exemption-class, self-test]

# Dependency graph
requires:
  - phase: 26-migration-apply-reconcile-generalize-enforce
    plan: 02
    provides: >-
      docs/PROCESS.md §2's generalized digit-narrowing rule and the
      pre-migration census naming docs/README.md:20 and
      docs/MEASUREMENT-MAP.md:54 as the two NARR-02 region candidates
provides:
  - "_NarrativeRegion roster (_NARRATIVE_REGIONS, two entries) with a second independently transcribed _NARRATIVE_REGION_SURFACES_LOCK and a required-argument set-equality floor (narrative_region_surface_roster_problems)"
  - "The sentence renderer (_render_narrative_sentence, raising NarrativeFieldNotFoundError on an absent field_path) and the harvest-free on-disk value recovery (_narrative_region_value_on_disk)"
  - "The restatement census (_narrative_restatement_findings / narrative_restatement_counts / narrative_restatement_problems), classifying every occurrence of a region's own value as finding / in-region / fenced / chain-hop"
  - "The generated-narrative-region entry in LITERAL_EXEMPTION_CLASSES, a named declaration whose matcher always returns False"
  - "Nine new --self-test controls (96 -> 105), each proven non-vacuous by induced failure"
affects: [26-04, 26-05, 26-06, 26-07]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "In-memory surface_texts substitution parameter on the census functions so --self-test controls never touch the real tree (FROZEN-EVIDENCE discipline)"
    - "Second, independently typed frozenset lock over a two-entry roster, mirroring _CONTAINMENT_SURFACES_LOCK exactly"

key-files:
  created: []
  modified:
    - scripts/gen-gate-docs.py
    - docs/gates/CONF-SURFACE.md
    - CLAUDE.md
    - docs/ARCHITECTURE.md

key-decisions:
  - "Named the two marker pairs README_HEADLINE_MARKERS / MEASUREMENT_MAP_HEADLINE_MARKERS with page-qualified strings (rather than reusing a shared name across pages) so the four literals are pairwise distinct on first read, even though _replace_region's per-file matching would not itself collide on identical marker text across different pages -- distinctness was explicit in the plan's own acceptance criterion."
  - "Reworded two new control docstrings (narrative-roster-missing-and-extra-named, narrative-restatement-four-legs) after CONF-13's own self-file docstring ratchet flagged new count-noun-adjacent literals ('surface removed, one', 'Four legs, one control') introduced by the first draft -- done before either wording reached disk, per the plan's own drafting discipline and Pitfall 3."
  - "Committed Task 1's roster/lock/floor together with the renderer and restatement census in a single commit, rather than splitting the renderer/census into Task 2's commit -- both pieces were already correct and interdependent (the census calls the renderer's sibling _narrative_region_value_on_disk) by the time Task 1's acceptance criteria were being verified; Task 2's own commit then carries only the exemption-class entry, which is genuinely separable and has its own --write side effect. Recorded as a deviation from the plan's literal task-to-commit mapping below."

requirements-completed: []

# Metrics
duration: ~50min
completed: 2026-09-10
---

# Phase 26 Plan 03: NARR-02's mechanism landed inert Summary

**Built the whole NARR-02 narrative-region mechanism inside `scripts/gen-gate-docs.py` -- a two-entry region roster with an equality-floored lock, a sentence renderer, a harvest-free restatement census, and a named exemption-class declaration -- proven correct by byte-identical rendering against the live harvest and nine non-vacuous self-test controls, and left completely unwired to any host surface or to `cmd_check()`.**

## Performance

- **Duration:** ~50 min
- **Tasks:** 3
- **Files modified:** 4 (`scripts/gen-gate-docs.py`; `docs/gates/CONF-SURFACE.md`, `CLAUDE.md`, `docs/ARCHITECTURE.md` as the mechanical `--write` regeneration side effect of the new exemption class and the new control count)

## Accomplishments

- `_NarrativeRegion` (surface, markers, source_script, field_path, template), `_NARRATIVE_REGIONS` (two entries: `docs/README.md`, `docs/MEASUREMENT-MAP.md`, both naming `scripts/check-traceability.py`'s `coverage_headline.prose` field), a second independently transcribed `_NARRATIVE_REGION_SURFACES_LOCK`, and `narrative_region_surface_roster_problems` (a required-`reached_keys`, no-default, set-equality comparator reporting `missing=`/`extra=`) -- exactly mirroring `_CONTAINMENT_SURFACES`/`_CONTAINMENT_SURFACES_LOCK`'s own shape.
- `_render_narrative_sentence` resolves a dotted `field_path` against a live `--describe` blob and renders the whole sentence via `template.format(value=...)`, raising the named `NarrativeFieldNotFoundError` (never `KeyError`, never `None`) when the field is absent.
- `_narrative_region_value_on_disk` recovers a region's live value straight from its own on-disk body with no subprocess and no importable-module escape hatch, failing closed (returning `None`) when the marker pair is absent -- proven at this stage to do exactly that, since neither host file carries the markers yet.
- `_narrative_restatement_findings` / `narrative_restatement_counts` / `narrative_restatement_problems` classify every occurrence of a recoverable region's value across the roster's surfaces as `finding` / `in-region` / `fenced` / `chain-hop`, reusing `_fenced_line_flags`, `_generated_line_flags` and `_link_delta_chains`/`_delta_chain_hops` rather than reimplementing any of them; accepts an in-memory `surface_texts` override so `--self-test` never touches the real tree.
- The `generated-narrative-region` entry in `LITERAL_EXEMPTION_CLASSES`, whose matcher (`_match_generated_narrative_region`) always returns `False` -- a named, auditable declaration of the class rather than the suppression mechanism (which is entirely `_generated_marker_pairs_for()`'s job, per D-04's mechanism correction). The only observable effect of adding it is the new zero-valued `literal_scan_exempt_generated-narrative-region` derived count.
- Nine new `--self-test` controls (`control_count` 96 -> 105), each proven non-vacuous by inducing its own failure via monkeypatch (see transcript below) rather than merely asserting a symbol's presence.
- No call site was added inside `generate_all`, `cmd_check`, `describe`, or `_generated_marker_pairs_for` -- confirmed by `grep` after every task. No document sentence and no ledger entry moved: `_DEFERRED_LITERAL_HITS` stayed 181/181 and `_DEFERRED_CONTAINMENT_HITS` stayed 26/26 across all three tasks.
- No new script, CI job, or REG-GUARD exemption: `FIREWALL: GREEN (26/26)` and `check-registration.py --self-test` PASS (29 controls) held throughout; `git diff --name-only` from the phase's base commit touches only `CLAUDE.md`, `docs/ARCHITECTURE.md`, `docs/gates/CONF-SURFACE.md`, and `scripts/gen-gate-docs.py`.

## Task Commits

1. **Task 1: Declare the narrative-region roster, its lock, and its equality floor (inert)** -- `d4d3893` (feat) -- also carries the renderer and restatement census (see key-decisions for why)
2. **Task 2: Add the sentence renderer, the exemption-class entry, and the harvest-free restatement census (inert)** -- `d98d8ca` (feat) -- the exemption-class entry and its `--write` regeneration side effect
3. **Task 3: Register --self-test controls for every new mechanism** -- `6d5909b` (test)

**Plan metadata:** this SUMMARY.md and the STATE.md/ROADMAP.md/REQUIREMENTS.md updates are committed together as the plan's closing metadata commit -- `.planning/STATE.md`, `.planning/ROADMAP.md` and `.planning/REQUIREMENTS.md` stay gitignored per project convention (`commit_docs: false`) and are not part of that commit's file list beyond what the harness force-tracks (this SUMMARY.md).

## Files Created/Modified

- `scripts/gen-gate-docs.py` -- the full narrative-region mechanism (roster, lock, floor, renderer, on-disk recovery, restatement census, exemption-class entry and matcher, nine self-test controls), landed entirely unwired.
- `docs/gates/CONF-SURFACE.md` -- Facts fence regenerated by `--write`: `derived_counts` gained `literal_scan_exempt_generated-narrative-region`=0 (29 -> 30 entries), and `control_ids`/`control_count` grew 96 -> 105.
- `CLAUDE.md`, `docs/ARCHITECTURE.md` -- CONF-SURFACE's generated gate-table row cell updated (`derived_counts=29 entries` -> `=30 entries`, `control_ids=96; control_count=96` -> `=105; control_count=105`) as the mechanical `--write` regeneration side effect; no other cell on either row changed.

## Decisions Made

See `key-decisions` in the frontmatter above (verbatim, not repeated here per `docs/PROCESS.md` §1's own citation-not-restatement rule).

## Deviations from Plan

**1. [Task-boundary conflation, not a Rule 1-4 fix] Task 1's commit also carries the renderer and restatement census.**
- **Found during:** preparing Task 1's commit.
- **What happened:** the renderer (`_render_narrative_sentence`), the on-disk value recovery (`_narrative_region_value_on_disk`), and the restatement census (`_narrative_restatement_findings`/`narrative_restatement_counts`/`narrative_restatement_problems`) were written and verified alongside the roster/lock/floor before the first commit was made, rather than held back for a separate Task 2 commit.
- **Why:** these functions are read-only siblings of the roster (they consume `_NarrativeRegion`/`_NARRATIVE_REGIONS` directly) and required no changes to `LITERAL_EXEMPTION_CLASSES` or any `--write` regeneration of their own -- unlike the exemption-class entry, which does force a Facts-fence regeneration and therefore genuinely earns its own commit.
- **Impact:** none on correctness or on the plan's stated acceptance criteria -- every criterion for both Task 1 and Task 2 was independently verified against the actual commits (see In-Process Verification Transcripts below), and the commit history still shows three atomic, buildable-and-testable commits in the plan's own task order. No rule 1-4 applied; this is an accounting note, not a functional deviation.

No auto-fix was needed on any task beyond the drafting-stage docstring reword recorded below (which is itself the plan's own prescribed drafting discipline, not a defect in the shipped mechanism).

## Issues Encountered

The first draft of two Task 3 control docstrings tripped CONF-13's own self-file docstring ratchet (`scripts/gen-gate-docs.py`'s live non-module-docstring hit count exceeded its pin, 32 vs 29): `_control_narrative_roster_missing_and_extra_named`'s docstring said "one locked surface removed, one fabricated surface added" (hit: `'surface removed, one'`), and `_control_narrative_restatement_four_legs`'s said "Four legs, one control." (hits: `'Four legs,'`, `'legs, one'`). Both were reworded before writing -- "the lock's own docs/README.md surface removed, a fabricated surface added" and "...each yield nothing -- covering every classified outcome" -- re-ran `--self-test`, got a clean pass, then proceeded. This is `26-RESEARCH.md`'s own Pitfall 3 firing exactly as documented, caught by the standing gate rather than requiring a second round-trip.

## In-Process Verification Transcripts

**Task 1 -- roster/lock/floor, verified by direct module import:**

```
len(_NARRATIVE_REGIONS) == 2                                            -> True
_NARRATIVE_REGION_SURFACES_LOCK == {"docs/README.md", "docs/MEASUREMENT-MAP.md"} -> True
narrative_region_surface_roster_problems()                              -> TypeError (no reached_keys)
narrative_region_surface_roster_problems(frozenset(LOCK))               -> []
narrative_region_surface_roster_problems(skewed: -README +BOGUS)        -> ["...missing=['docs/README.md'] extra=['docs/BOGUS.md']..."]
len({s for pair in (README_HEADLINE_MARKERS, MEASUREMENT_MAP_HEADLINE_MARKERS) for s in pair}) -> 4
every _NARRATIVE_REGIONS entry: template.count("{value}")               -> 1
```

`/usr/bin/grep -n "_NARRATIVE_REGIONS\|narrative_region_surface_roster_problems" scripts/gen-gate-docs.py` showed no call site inside `generate_all`, `cmd_check`, or `_generated_marker_pairs_for` (only the definitions themselves and their own docstring cross-references). `git diff --stat` for this task listed `scripts/gen-gate-docs.py` only.

**Task 1 -- byte-identity comparison, rendered vs. on-disk (live `--describe` blob from `scripts/check-traceability.py`):**

| Region | Rendered | On-disk line (stripped) | Byte-identical |
|---|---|---|---|
| `docs/README.md` | `> headline of **208 reproducible / 97 audit-only / 0 gap / 305 total**.` | same | True |
| `docs/MEASUREMENT-MAP.md` | `For the complete Active-Surface list and the coverage headline (208 reproducible / 97 audit-only / 0 gap / 305 total), see [requirements-traceability.md](requirements-traceability.md).` | same | True |

**Task 2 -- exemption entry and inertness, verified by direct module import:**

```
_render_narrative_sentence(region_with_absent_field, blob) -> NarrativeFieldNotFoundError (named, not KeyError/None)
generated-narrative-region matcher on a live-shaped hit      -> False
run_literal_scan().hits matched by that matcher              -> 0 of 213
describe()["derived_counts"]["literal_scan_exempt_generated-narrative-region"] -> 0
_narrative_region_value_on_disk(region, real on-disk text)  -> None (both regions -- no markers exist yet)
narrative_restatement_problems()                             -> [] (vacuous, for the same reason -- stated explicitly, not reported as a pass)
```

`--check` before `--write`: `DRIFT: docs/gates/CONF-SURFACE.md`, the diff limited to `derived_counts` gaining one entry (29 -> 30), the new `literal_scan_exempt_generated-narrative-region`=0 key -- no other line changed. After `--write`: `--check` exit 0; `git diff --stat` limited to `docs/gates/CONF-SURFACE.md`, `CLAUDE.md`, `docs/ARCHITECTURE.md` (the CONF-SURFACE table-row cell), plus `scripts/gen-gate-docs.py`.

**Task 3 -- control-count readings, transcribed:**

| Reading point | `control_count` |
|---|---|
| Before Task 3 | 96 |
| After Task 3 | 105 |

**Task 3 -- induced-failure transcript, every new control, by its own id:**

| Control id | Induced mutation | Failure observed |
|---|---|---|
| `narrative-region-roster-equals-lock` | handed a reached set missing `docs/MEASUREMENT-MAP.md` | `AssertionError: ({'docs/README.md'}, frozenset({'docs/MEASUREMENT-MAP.md', 'docs/README.md'}))` |
| `narrative-roster-no-default-raises` | forced a call that supplies `reached_keys` and then asserts a `TypeError` still occurs | `AssertionError: expected TypeError for missing reached_keys` |
| `narrative-roster-missing-and-extra-named` | monkeypatched the comparator to omit the `extra=` clause | `ValueError: _roster_arm_clauses: message lacks 'missing=' or ' extra=' marker: "narrative-region-surface-roster: missing=['docs/README.md']"` |
| `narrative-marker-pairs-distinct` | monkeypatched `MEASUREMENT_MAP_HEADLINE_MARKERS` to duplicate `README_HEADLINE_MARKERS` | `AssertionError: [...four strings collapsed to two, both repeated...]` |
| `narrative-region-templates-single-value-slot` | monkeypatched `_NARRATIVE_REGIONS` to a region whose template carries zero `{value}` slots | `AssertionError: _NarrativeRegion(..., template='no placeholder here')` |
| `narrative-render-raises-on-absent-field` | monkeypatched `_render_narrative_sentence` to never raise | `AssertionError: expected NarrativeFieldNotFoundError` |
| `narrative-render-round-trips-through-disk-value` | monkeypatched `_narrative_region_value_on_disk` to return a wrong value | `AssertionError: ('WRONG VALUE', 'Coverage stands at 1 reproducible / 2 audit-only / 0 gap / 3 total today.')` |
| `narrative-exemption-matcher-never-suppresses` | monkeypatched the matcher to return `True` | `AssertionError: LiteralHit(relpath='docs/README.md', line=20, text='208 reproducible / 97 audit-only / 0 gap / 305 total')` |
| `narrative-restatement-four-legs` | monkeypatched `_fenced_line_flags` to always report unfenced | `AssertionError: [...the fenced-line occurrence reclassified as 'finding', collapsing the four-way tally...]` |

All nine mutations were applied to a freshly `importlib`-loaded module instance, in-memory only (no `tempfile`, no real file ever touched, per FROZEN-EVIDENCE discipline); the real tree's `git status --porcelain` was empty both before and after this transcript was produced.

**Automated verify commands run, all three tasks, all green (final readings):**

```
python3 scripts/gen-gate-docs.py --self-test           # SELF-TEST PASS -- 105 controls run
python3 scripts/gen-gate-docs.py --check                # exit 0; harvested 22/22 expected script-backed entries
sh .githooks/pre-commit                                 # all five gates PASS, exit 0
python3 scripts/check-registration.py --self-test        # PASS (29 controls)
bash scripts/check-firewall-battery.sh                   # FIREWALL: GREEN (26/26)
```

**Ledger readings, both taken by module import, before Task 1 and after Task 3:**

| Reading point | `len(_DEFERRED_LITERAL_HITS)` | `_DEFERRED_LEDGER_MAX` | `len(_DEFERRED_CONTAINMENT_HITS)` | `_CONTAINMENT_LEDGER_MAX` |
|---|---|---|---|---|
| Before Task 1 | 181 | 181 | 26 | 26 |
| After Task 3 | 181 | 181 | 26 | 26 |

`git diff --diff-filter=D --name-only` between every consecutive pair of commits in this plan returned empty -- no unexpected deletions. `git status --porcelain` was clean after each commit. `git diff --name-only fe3e26e..HEAD` (the phase's prior commit) lists exactly `CLAUDE.md`, `docs/ARCHITECTURE.md`, `docs/gates/CONF-SURFACE.md`, `scripts/gen-gate-docs.py` -- neither `.github/workflows/validation.yml` nor `scripts/check-firewall-battery.sh` appears.

## Assumption Drift (advisory)

None material. The plan's own `<interfaces>` block pre-named every identifier used here (`_NarrativeRegion`, `_NARRATIVE_REGIONS`, `_NARRATIVE_REGION_SURFACES_LOCK`, `narrative_region_surface_roster_problems`, `_render_narrative_sentence`, `_narrative_region_value_on_disk`, `narrative_restatement_problems`/`_counts`, `generated-narrative-region`) and the two host surfaces (`docs/README.md`, `docs/MEASUREMENT-MAP.md`) exactly matched 26-02-SUMMARY.md's own measured region candidates -- no rediscovery or renaming was needed.

## User Setup Required

None -- no external service configuration required.

## Next Phase Readiness

- Plan 26-04 (wiring the mechanism: registering the two marker pairs in `_generated_marker_pairs_for()`, bootstrapping the regions into `docs/README.md`/`docs/MEASUREMENT-MAP.md` via `generate_all()`, and letting `cmd_check()`'s existing drift diff cover them) can proceed directly against this plan's roster, renderer, and census -- all proven correct while inert.
- No blockers. Both ledgers confirmed unmoved (181/181, 26/26), which is the precondition the phase's own wave ordering (migrate first, re-pin last) depends on for the remaining waves.

---
*Phase: 26-migration-apply-reconcile-generalize-enforce*
*Completed: 2026-09-10*

## Self-Check: PASSED

- FOUND: `scripts/gen-gate-docs.py`
- FOUND: `docs/gates/CONF-SURFACE.md`
- FOUND: `CLAUDE.md`
- FOUND: `docs/ARCHITECTURE.md`
- FOUND: commit `d4d3893` in `git log --oneline --all`
- FOUND: commit `d98d8ca` in `git log --oneline --all`
- FOUND: commit `6d5909b` in `git log --oneline --all`
