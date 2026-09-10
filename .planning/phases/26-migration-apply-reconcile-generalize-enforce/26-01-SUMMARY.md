---
phase: 26-migration-apply-reconcile-generalize-enforce
plan: 01
subsystem: docs
tags: [gen-gate-docs, containment, literal-scan, requirements-governance]

# Dependency graph
requires:
  - phase: 25-mechanism-design-containment-reach-and-the-terminus-arm
    provides: >-
      CONTAIN-01/02/03's REACH-or-LEVEL determinations section on
      docs/gates/CONF-SURFACE.md (the precedent this plan extends rather than
      duplicates), and the settled 181/26 ledger baselines this plan does not move
provides:
  - "Phase 26's written REACH-or-LEVEL determinations for NARR-01, NARR-02, RATCHET-01, RATCHET-02, RATCHET-03, landed before any of the mechanisms exists (RATCHET-04)"
  - "The written answer to STACK.md's cogapp recommendation: ARCHITECTURE.md's rejection adopted (D-01), STACK.md's strongest point conceded by name, a superseded-by pointer added"
  - "RATCHET-03's DROP verdict recorded at both its roadmap landing sites (criterion 4's pointer, criterion 5's drop slot)"
  - "NARR-02 and RATCHET-01 requirement texts, and roadmap criteria 3/4, amended to name generated-narrative-region / scripts/gen-gate-docs.py --check rather than cog/cogapp"
affects: [26-02, 26-03, 26-04, 26-05, 26-06, 26-07]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "REACH-or-LEVEL determination written before the mechanism it judges exists (RATCHET-04's ordering requirement), landed as a sibling `##` section on the same gate page rather than renaming the Phase 25 section"
    - "Requirement/roadmap amendment recorded in an amendment note (D-04 shape), citing the rejecting research doc rather than re-deriving the argument"

key-files:
  created: []
  modified:
    - docs/gates/CONF-SURFACE.md
    - .planning/research/STACK.md
    - .planning/REQUIREMENTS.md
    - .planning/ROADMAP.md

key-decisions:
  - "D-01 (cog): adopt ARCHITECTURE.md's rejection of cogapp; the repo's own _replace_region/_replace_or_bootstrap_region/_generated_marker_pairs_for primitives already reproduce cog's marked-span granularity without a second templating language or CLI dependency"
  - "RATCHET-03's DROP is landed at both roadmap sites: criterion 4's third clause becomes a pointer to criterion 5, and criterion 5 carries the verdict, its reason, and the citation"
  - "NARR-02's requirement text corrected on a second axis beyond the cog/cogapp naming: the suppression mechanism is a marker-pair registration in _generated_marker_pairs_for(), not the LITERAL_EXEMPTION_CLASSES entry, which is a named declaration only"

requirements-completed: []

# Metrics
duration: ~30min
completed: 2026-09-10
---

# Phase 26 Plan 01: RATCHET-04's determinations, the cog answer, and D-04's amendments Summary

**Wrote Phase 26's REACH-or-LEVEL determinations for NARR-01/NARR-02/RATCHET-01/02/03 before any of those mechanisms exists, answered STACK.md's cogapp recommendation in writing (D-01: rejected, ARCHITECTURE.md's side taken), and amended NARR-02/RATCHET-01/roadmap criteria 3-4-5 to name the mechanism actually being built instead of `cog`.**

## Performance

- **Duration:** ~30 min (STATE.md's phase-start timestamp `2026-09-10T11:20:55Z` to plan close `~11:52Z`)
- **Tasks:** 2
- **Files modified:** 4 (1 git-tracked, 3 under the gitignored `.planning/` tree)

## Accomplishments

- `docs/gates/CONF-SURFACE.md` carries a new `## REACH-or-LEVEL determinations (Phase 26, NARR-01, NARR-02, RATCHET-01, RATCHET-02, RATCHET-03)` section with all six required sub-parts: the cog answer, the three RATCHET verdicts (cited from `docs/v9.1-claim-containment-diagnosis.md` §6, not restated), the meta-guard-regress argument, forward determinations for NARR-01/NARR-02/the roster floor/the restatement census, the capability statement, and the D-04 requirement-amendment record.
- `.planning/research/STACK.md`'s cogapp section gained a superseded-by note naming `26-CONTEXT.md` D-01 and `docs/gates/CONF-SURFACE.md` as where the written answer lives, without deleting or rewording the original recommendation.
- `.planning/REQUIREMENTS.md`'s NARR-02 and RATCHET-01 texts, and `.planning/ROADMAP.md`'s Phase 26 success criteria 3, 4 and 5, no longer name `cog`/`cogapp`/`cog --check`/`cog-generated-region` as the mechanism being built; every surviving `cog` occurrence sits in a sentence stating it is not adopted.
- RATCHET-03's DROP verdict is recorded at both landing sites: a pointer in criterion 4 (replacing the struck hedge-word-scan clause) and the verdict, its reason, and the diagnosis citation in criterion 5's own drop slot.

## Task Commits

1. **Task 1: Write Phase 26's REACH-or-LEVEL determinations and the cog answer** — `78b45a9` (docs)
2. **Task 2: Amend the requirement and roadmap texts (D-04, plus the suppression-mechanism correction, plus RATCHET-03's DROP)** — no commit. `.planning/REQUIREMENTS.md` and `.planning/ROADMAP.md` are both gitignored (`.gitignore:1: .planning/` with no force-track exception for these two files — verified via `git check-ignore -v`), and `commit_docs: false` in `.planning/config.json` confirms this is the intended project convention, not an oversight. The edits are on disk and verified (see below); there is nothing to stage.

**Plan metadata:** this SUMMARY.md and the STATE.md/ROADMAP.md-progress update are committed together as the plan's closing metadata commit (see `<final_commit>`), per project convention — `.planning/ROADMAP.md` itself stays gitignored and is not part of that commit's file list beyond what the harness force-tracks.

## Files Created/Modified

- `docs/gates/CONF-SURFACE.md` — new hand-written section (95 lines) with the six required sub-parts, placed after the existing Phase 25 REACH-or-LEVEL section, outside both generated fences.
- `.planning/research/STACK.md` — superseded-by note appended to the cogapp section (gitignored, not git-tracked).
- `.planning/REQUIREMENTS.md` — NARR-02 and RATCHET-01 texts amended (gitignored).
- `.planning/ROADMAP.md` — Phase 26 success criteria 3, 4, 5 amended; two backlog cross-references (Phase 999.69, Phase 999.70) that named "NARR-02's `cog` regions/territory" also corrected to `generated-narrative-region` for consistency with the amended requirement text (gitignored).

## Decisions Made

- Extended the existing `## REACH-or-LEVEL determinations (v9.1.0, CONTAIN-01, CONTAIN-02, CONTAIN-03)` section's *pattern* with a new sibling `##` heading for Phase 26's own determinations, rather than renaming the existing heading — both were acceptable per the plan; a sibling heading keeps Phase 25's and Phase 26's determinations independently addressable.
- Cited `docs/v9.1-claim-containment-diagnosis.md` §6 as "section 6" (spelled out) rather than "§6" in the new prose, after the draft's `§6` form tripped `detail_page_containment_problems()`'s bare-number check (`_strip_citation_shaped_numbers`'s citation-shape vocabulary recognizes the word "section" but not the `§` symbol). This is a wording choice with no loss of accuracy — [Rule 1 — Bug] fix, verified by re-running the containment check in-process before writing to disk.
- Fixed the RATCHET-01 requirement text's wrapped line break that had separated `cog --check` from the `not adopted` disclosure onto two physical lines, after the plan's own automated verify command (`grep -v "not adopted"`, line-scoped) flagged it as a surviving unqualified `cog` mention. Reworded onto one physical line — [Rule 1 — Bug] fix, since the substance (cogapp is not adopted) was already present, just not co-located on the line the verify command reads.
- Also corrected two Phase 26 backlog entries (999.69, 999.70) elsewhere in `.planning/ROADMAP.md` that referred to "NARR-02's `cog` regions/territory" — outside Task 2's literal `<action>` scope (which named only NARR-02/RATCHET-01/criteria 3-4), but within the plan's own stated truth ("No requirement text, roadmap criterion or gate page names `cog`... as the mechanism this phase builds") and acceptance criterion (`grep -n "cog" .planning/REQUIREMENTS.md .planning/ROADMAP.md` must show only not-adopted-qualified occurrences). Left `.planning/ROADMAP.md:986`'s Plans-list mention of "the written answer to STACK.md's cog recommendation" untouched — it names STACK.md's own historical recommendation, not the mechanism being built.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] `§6` citation form tripped the containment scanner's bare-number check**
- **Found during:** Task 1, drafting the RATCHET-verdicts subsection
- **Issue:** Citing `docs/v9.1-claim-containment-diagnosis.md` as `§6` (four occurrences) left a bare `6` outside any generated fence with no matching harvested literal, which `detail_page_containment_problems()` flags as a D-06 finding — this would have failed `--check` on commit.
- **Fix:** Reworded all four occurrences to "section 6", which `_strip_citation_shaped_numbers`'s named-thing-ordinal-reference pattern recognizes and strips before the bare-number count runs.
- **Files modified:** `docs/gates/CONF-SURFACE.md`
- **Verification:** Re-ran `detail_page_containment_problems()` in-process on the edited text; only the pre-existing, already-tolerated `'20'` finding remained (confirmed present and unchanged on the unedited original text too, via `git show HEAD:...`).
- **Committed in:** `78b45a9` (Task 1 commit)

**2. [Rule 1 - Bug] RATCHET-01's `not adopted` qualifier was wrapped onto a different physical line than `cog --check`**
- **Found during:** Task 2, running the plan's own automated verify command
- **Issue:** `grep -nE "cog(app)? " .planning/REQUIREMENTS.md | grep -v "not adopted"` is line-scoped; the initial edit's Markdown line-wrap put `` `cog --check` `` on one physical line and `` `cogapp` is not adopted `` on the next, so the negated verify failed even though the substance was correct.
- **Fix:** Rewrote the RATCHET-01 line so `` `cogapp` is not adopted `` sits on the same physical line as `` `cog --check` ``.
- **Files modified:** `.planning/REQUIREMENTS.md` (gitignored, not committed)
- **Verification:** Re-ran the exact verify command; exit 0.

---

**Total deviations:** 2 auto-fixed (both Rule 1 — bugs discovered by running the plan's own verification commands before considering either task done, not scope creep).
**Impact on plan:** Both fixes are wording-only corrections needed to satisfy this same plan's own stated acceptance criteria; no scope change.

## In-Process Verification Transcripts

**`_scan_text_for_literal_hits()` over the exact final text of Task 1's new section** (isolated by slicing the file from the new `## REACH-or-LEVEL determinations (Phase 26...` heading to end-of-file, relpath `docs/gates/CONF-SURFACE.md`):
```
hits in new section only: 0
```

**Ledger readings, both taken by module import of `scripts/gen-gate-docs.py`:**

| Reading point | `len(_DEFERRED_LITERAL_HITS)` | `_DEFERRED_LEDGER_MAX` | `len(_DEFERRED_CONTAINMENT_HITS)` | `_CONTAINMENT_LEDGER_MAX` |
|---|---|---|---|---|
| Plan start (before any edit, matches `26-RESEARCH.md`'s dated reading) | 181 | 181 | 26 | 26 |
| Plan end (after both tasks, `--write` + `--check` run) | 181 | 181 | 26 | 26 |

No re-pin happened in this plan, as required — both figures are byte-unchanged from start to end.

**Every surviving `cog` occurrence, quoted with its surrounding sentence, in `.planning/REQUIREMENTS.md` and `.planning/ROADMAP.md` after Task 2:**

- `.planning/REQUIREMENTS.md:390` — "...marker-region machinery (`_replace_region`/`_replace_or_bootstrap_region`, not `cogapp` — amended by D-04, ...)" — states non-adoption.
- `.planning/REQUIREMENTS.md:402` — "**RATCHET-01**: `scripts/gen-gate-docs.py --check` (`cogapp` is not adopted; amended by D-04 from `cog --check`, same citations as NARR-02 above) runs as **pre-commit gate 5**..." — states non-adoption.
- `.planning/ROADMAP.md:953-954` — "A `generated-narrative-region` entry exists in `LITERAL_EXEMPTION_CLASSES` (amended from `cog-generated-region` — D-04, ...; `cogapp` is not adopted)..." — states non-adoption.
- `.planning/ROADMAP.md:958` — "`scripts/gen-gate-docs.py --check` (amended from `cog --check`, same citations as criterion 3 above)..." — amendment note, no bare unqualified `cog` mechanism claim.
- `.planning/ROADMAP.md:986` — Plans-list bullet: "26-01-PLAN.md — RATCHET-04's determinations, the written answer to STACK.md's cog recommendation, ..." — refers to STACK.md's own historical recommendation (the thing being answered), not the mechanism built; left as-is deliberately.
- `.planning/ROADMAP.md:4030-4031, 4057` — two backlog entries (999.69, 999.70) corrected from "NARR-02's `cog` regions/territory" to "NARR-02's generated narrative regions... not `cog` regions — `cogapp` is not adopted" / "generated-narrative-region territory... not `cog` territory".

**Automated verify commands run, both green:**
```
python3 scripts/gen-gate-docs.py --self-test   # SELF-TEST PASS — 96 controls run
python3 scripts/gen-gate-docs.py --check       # harvested 22/22 expected script-backed entries (22 total); exit 0
! /usr/bin/grep -nE "cog(app)? " .planning/REQUIREMENTS.md | /usr/bin/grep -v "not adopted"   # exit 0
bash scripts/check-firewall-battery.sh          # FIREWALL: GREEN (26/26)
```

`git diff --name-only` from the phase's own base commit (`f2073f3`, the tip before this phase started) to `HEAD` lists exactly one file: `docs/gates/CONF-SURFACE.md`. No file under `scripts/`, `shared/`, `first-principles/` or `.github/` was touched by this plan.

## Issues Encountered

None beyond the two auto-fixed items above, both caught by running the plan's own prescribed verification commands rather than by inspection.

## Assumption Drift (advisory)

None material. The plan's own `<interfaces>` block pre-specified the exemption-class id (`generated-narrative-region`), the pre-commit landing site (gate 5), and the three existing hand-written host sections to read first; all three matched what was found in `docs/gates/CONF-SURFACE.md` with no drift.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- Plan 26-02 (NARR-01: generalize `docs/PROCESS.md` §2's digit-narrowing rule) can proceed: RATCHET-04's ordering requirement is now discharged for NARR-01 (its forward REACH-or-LEVEL determination is written and citable) and the requirement/roadmap texts 26-02 and later plans will read no longer name a tool that isn't being built.
- No blockers. The ledger baselines (181/181, 26/26) are confirmed unmoved, which is the precondition the phase's own wave ordering (migrate first, re-pin last) depends on for waves 2-4.

---
*Phase: 26-migration-apply-reconcile-generalize-enforce*
*Completed: 2026-09-10*

## Self-Check: PASSED

- FOUND: `docs/gates/CONF-SURFACE.md`
- FOUND: `.planning/research/STACK.md`
- FOUND: `.planning/REQUIREMENTS.md`
- FOUND: `.planning/ROADMAP.md`
- FOUND: `.planning/phases/26-migration-apply-reconcile-generalize-enforce/26-01-SUMMARY.md`
- FOUND: commit `78b45a9` in `git log --oneline --all`
