---
phase: 26-migration-apply-reconcile-generalize-enforce
plan: 07
subsystem: infra
tags: [gen-gate-docs, mutation-demonstration, ratchet, literal-scan, containment-ledger, phase-close]

# Dependency graph
requires:
  - phase: 26-migration-apply-reconcile-generalize-enforce
    plan: 06
    provides: >-
      Both ledgers reconciled and re-pinned (literal 180/180, containment
      22/22), D-06's .py-docstring and diagnosis-page scope calls decided,
      CONTAIN-04 and RATCHET-02 both marked complete
  - phase: 26-migration-apply-reconcile-generalize-enforce
    plan: 04
    provides: >-
      The two wired NARR-02/RATCHET-01 regions (docs/README.md,
      docs/MEASUREMENT-MAP.md) this plan mutates in Arm B and the census arm
  - phase: 26-migration-apply-reconcile-generalize-enforce
    plan: 05
    provides: >-
      CLAUDE.md's third narrative region this plan mutates in Arm C
provides:
  - "RATCHET-01 proved by mutation, not by reading: four arms (unmutated control, a mutated docs/README.md region, an independently mutated CLAUDE.md region on a different host surface, and a census-arm hand-typed restatement on docs/MEASUREMENT-MAP.md), all on a disposable rsync scratch copy, all restored and md5sum-confirmed, with the real repository verified clean before the first mutation and after the last"
  - "Criterion 3's published target: the count of hand-typed non-exempt count literals in narrative prose across the NARR-02-scoped surfaces (six containment-unreachable surfaces plus CLAUDE.md) is driven to zero, measured by filtering a fresh run_literal_scan() to that named set"
  - "Criterion 3's cannot-reach residue consolidated into one new disclosed bound (13), citing the two sites already on record (bounds (8), (9)) rather than absorbing them into the target"
  - "The capability statement plan 26-01 wrote as a pre-commitment restated as a demonstrated fact citing this plan's own mutation transcripts, and all four self-referential tests answered with dated evidence"
  - "Criterion 6's invariance reconciled by direct artifact count against the phase base commit (f2073f3), never by the battery's own self-report: battery gate/gate_prereq registrations plus inline checks, CI job count, and the REG-GUARD exemption set are each byte-identical at both endpoints"
  - "All seven Phase 26 requirements (CONTAIN-04, NARR-01, NARR-02, RATCHET-01..04) ticked in .planning/REQUIREMENTS.md with their own command-and-reading evidence lines; Phase 26 marked complete in .planning/ROADMAP.md with per-criterion evidence, including a closing note that FIREWALL: GREEN is not itself the evidence for any criterion"
affects: [27]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Mutation demonstration on a disposable rsync --exclude .git scratch copy, never the real tree: Arm A (unmutated control) establishes a baseline, Arm B/Arm C mutate two different regions on two different host surfaces to prove the check is general rather than fitted to one target, and a census arm proves the sibling restatement-outside-region check independently — every arm restored and md5sum-confirmed before the next runs"
    - "A generated derived_counts field growing by exactly one new disclosed-bounds anchor can coincidentally corroborate an unrelated frozen-historical or cannot-reach digit already stated elsewhere on the same page (the same trap plan 26-06 Task 3 hit); when the resulting total cannot be chosen to avoid the collision (only one anchor is being added), the correct fix is to reconcile the containment ledger's now-stale entries in the same commit, not to leave them ledgered against a corroboration that only happened because an unrelated field rendered the same digit"
    - "Criterion 6's invariance is reconciled by reading each of the three source files directly at the phase base commit (git show <base>:<path>) and at HEAD, never by trusting a script's own printed tally alone -- the battery's report is then checked for AGREEMENT with the direct count, not substituted for it"

key-files:
  created: []
  modified:
    - docs/gates/CONF-SURFACE.md
    - scripts/gen-gate-docs.py
    - CLAUDE.md
    - docs/ARCHITECTURE.md
    - .planning/REQUIREMENTS.md
    - .planning/ROADMAP.md

key-decisions:
  - "Chose docs/README.md for Arm B and CLAUDE.md for Arm C (rather than, e.g., docs/MEASUREMENT-MAP.md for both mutation arms), and docs/MEASUREMENT-MAP.md for the census arm, so all three narrative-region host surfaces registered by this phase (docs/README.md, docs/MEASUREMENT-MAP.md, CLAUDE.md) are individually exercised across the four arms, rather than reusing one surface twice."
  - "When adding the one new disclosed-bounds anchor for criterion 3's residue moved disclosed_bounds_anchors 13 -> 14 and coincidentally corroborated two unrelated frozen/cannot-reach '14' containment-ledger entries (CLAUDE.md, docs/ARCHITECTURE.md) -- the same trap plan 26-06 Task 3 hit -- reconciled the containment ledger in the same commit (22 -> 20) rather than searching for a non-colliding anchor-count choice, because only one anchor was being added this time (unlike 26-06, which had two candidate bounds to bundle under one anchor and could choose a non-colliding total)."
  - "Consolidated criterion 3's cannot-reach residue into exactly one new disclosed bound citing the two sites already published individually (bounds (8), (9)) rather than writing new prose re-deriving either -- following this phase's own citation-not-restatement discipline (docs/PROCESS.md §1)."
  - "Enhanced RATCHET-01's and criterion 4's already-ticked/discharged text with this plan's own mutation-demonstration evidence, rather than treating the prior tick as already sufficient -- D-06 proviso 1's own words are 'reading the code is not proof', and the prior tick (from plan 26-04) predates this plan's own four-arm demonstration."

requirements-completed: [CONTAIN-04, NARR-01, NARR-02, RATCHET-01, RATCHET-02, RATCHET-03, RATCHET-04]

# Metrics
duration: ~45min
completed: 2026-09-10
---

# Phase 26 Plan 07: RATCHET-01 proved by mutation, criterion 3's target and residue published, criterion 6 reconciled by direct count, phase closed Summary

**Proved RATCHET-01 by a four-arm mutation demonstration on a disposable scratch copy (unmutated control, two independently mutated narrative regions on two host surfaces, and a census-arm restatement), published criterion 3's target (zero non-exempt hand-typed count literals across the NARR-02-scoped surfaces) and its consolidated cannot-reach residue, reconciled criterion 6's battery/CI/exemption invariance by direct artifact count against the phase base commit, and closed Phase 26 with all seven requirements ticked and their own evidence.**

## Performance

- **Duration:** ~45 min
- **Tasks:** 3 (Task 3 touches only gitignored `.planning/REQUIREMENTS.md`/`.planning/ROADMAP.md`, no commit)
- **Files modified:** 4 tracked (`docs/gates/CONF-SURFACE.md`, `scripts/gen-gate-docs.py`, `CLAUDE.md`, `docs/ARCHITECTURE.md` as the mechanical `--write` regeneration side effect) plus 2 gitignored (`.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`)

## Accomplishments

- **RATCHET-01 proved by mutation, not by reading.** On a disposable `rsync --exclude .git` scratch copy, with the real repository confirmed clean (`git status --porcelain` empty, `HEAD` recorded) before the first mutation and after the last: Arm A (unmutated control) passed `--check` exit 0; Arm B (`docs/README.md`'s own coverage-headline region mutated in place, no constant touched) failed `--check` exit 1 with a `DRIFT:` line naming that exact file, and `--self-test` also failed (two controls that exercise `cmd_check()` against the real tree, exactly the mechanism working as designed, matching plan 26-04's own precedent); Arm C (`CLAUDE.md`'s independent coverage-headline region mutated, a different host surface from Arm B) failed `--check` exit 1 with an independent `DRIFT:` line naming that second file, proving the check is general rather than fitted to Arm B's own target; the census arm (a hand-typed restatement of the coverage headline appended to `docs/MEASUREMENT-MAP.md`, outside any generated fence) failed `--check` exit 1, naming the file and the exact line (`docs/MEASUREMENT-MAP.md:103`) three times, once per roster region it restates. Every mutation was restored from the real repository and confirmed byte-identical via `md5sum` before the next arm ran, and `--check` passed exit 0 again after each restore.
- A short paragraph recording all four arms and their outcomes was added to `docs/gates/CONF-SURFACE.md` ("RATCHET-01, demonstrated by mutation"), stating explicitly that no sixth pre-commit gate, CI job, or battery registration was added — the demonstration runs entirely through pre-commit gate 5, which already existed.
- **Criterion 3's target published**: re-invoking `run_literal_scan()` and filtering its hits to exactly the NARR-02-scoped surface set (`docs/PROCESS.md`, `docs/README.md`, `CONTRIBUTING.md`, `docs/MEASUREMENT-MAP.md`, `docs/COMPONENT-DIAGRAM.md`, `docs/DATA-FLOW.md`, `CLAUDE.md`) finds 80 total hits, all of which already carry a matching exemption class — the non-exempt count on that named set is **zero**, published on a new "Criterion 3's published target" section on `docs/gates/CONF-SURFACE.md`, pointing at the same `literal_scan_non_exempt` field the Facts fence already publishes globally (also zero) rather than restating a bare digit.
- **Criterion 3's cannot-reach residue consolidated into one new disclosed bound (13)**, citing the two sites already published individually by earlier plans in this phase (`tests/premise-rejection-catalog.md`'s second G3 target, bound (8); `docs/COMPONENT-DIAGRAM.md`'s fenced Mermaid label, bound (9)) rather than re-deriving either or absorbing them into the target — `disclosed_bounds_anchors` grew from 13 to 14, exactly one new anchor (`criterion-3-cannot-reach-residue`).
- **Coincidental cross-check corroboration, found and fixed in the same commit**: raising `disclosed_bounds_anchors` to 14 made `CLAUDE.md`'s own generated CI-gate table cell render `14`, which coincided with two unrelated, already-ledgered containment findings — the frozen-historical `('CLAUDE.md', '14')` and the cannot-reach `('docs/ARCHITECTURE.md', '14')` — both keyed on the digit "14" appearing outside any fence on their own page with (now) a same-page in-fence match. `containment_ledger_staleness_problems()` reported both as no longer matching any live finding; removed and re-pinned in the same commit (`_CONTAINMENT_LEDGER_MAX` 22 → 20, key digest re-derived), following the identical discipline plan 26-06 Task 2 used for `('CLAUDE.md', '43')`.
- **The capability statement, demonstrated**: plan 26-01's pre-commitment ("a contributor will no longer be able to hand-type the live coverage headline on CLAUDE.md... and reach HEAD") is restated as a fact on `docs/gates/CONF-SURFACE.md`, citing this plan's own Arm C and census-arm transcripts as the demonstration, naming `HEADLINE-LOCK`'s own disclosed bound as the prior gap this closes, and stating plainly what remains open (the residue bound (13), and any narrative page outside the roster's fixed population).
- **All four self-referential tests answered** in a new "The four self-referential tests, answered for this phase" section: test 1 (capability, not correction) points at the demonstrated statement above; test 2 (sibling site named first) cites `26-02-SUMMARY.md`'s pre-migration census; test 3 (REACH-or-LEVEL in writing) cites plan 26-01's determinations section, dated before any mechanism existed; test 4 (recurrence, not compliance) names `REL-08` as where product-recurrence verification actually lands.
- **Criterion 6's invariance reconciled by direct artifact count**, never by the battery's own self-report: `scripts/check-firewall-battery.sh`'s `gate`/`gate_prereq` call sites (VAL-03's if/else pair counted once) plus its two inline checks, `.github/workflows/validation.yml`'s job `name:` entries, and `check-registration.py`'s `BATTERY_ONLY_GATE_IDS` were each read directly at the phase base commit (`f2073f3`) and at `HEAD` and found byte-identical at both endpoints (24 gate/gate_prereq registrations + 2 inline checks = 26; 23 CI jobs; `{"QUAL-01"}` unchanged). `bash scripts/check-firewall-battery.sh` then reports `FIREWALL: GREEN (26/26)`, agreeing with — not substituting for — the direct count.
- **All seven Phase 26 requirements ticked** in `.planning/REQUIREMENTS.md` with their own command-and-reading evidence lines (RATCHET-01 and criterion 4 enhanced with this plan's own mutation transcript; RATCHET-03 and RATCHET-04, previously unticked, now ticked with their DROP-verdict and dated-determination evidence respectively). `.planning/ROADMAP.md`'s Phase 26 entry marked complete, all six success criteria carrying their own discharge evidence, and a closing note stating explicitly that `FIREWALL: GREEN` is not itself the evidence for any criterion.

## Task Commits

1. **Task 1: The three-arm (plus census) mutation demonstration** — `53bb85a` (docs)
2. **Task 2: Publish criterion 3's target and the demonstrated capability statement** — `9ee3ae8` (docs)
3. **Task 3: Reconcile criterion 6's invariance and close the phase** — no commit; `.planning/REQUIREMENTS.md` and `.planning/ROADMAP.md` are both gitignored (`commit_docs: false`), verified via `git check-ignore -v`. Edits are on disk and verified below.

**Plan metadata:** this SUMMARY.md and the STATE.md/ROADMAP.md/REQUIREMENTS.md updates are committed together as the plan's closing metadata commit — `.planning/STATE.md`, `.planning/ROADMAP.md` and `.planning/REQUIREMENTS.md` stay gitignored per project convention (`commit_docs: false`) and are not part of that commit's file list beyond what the harness force-tracks (this SUMMARY.md).

## Files Created/Modified

- `docs/gates/CONF-SURFACE.md` — new "RATCHET-01, demonstrated by mutation" subsection; new "Criterion 3's published target" section and new disclosed bound (13) for the consolidated cannot-reach residue; new "The capability statement, demonstrated" and "The four self-referential tests, answered for this phase" subsections; Facts fence regenerated (`disclosed_bounds_anchors` 13 → 14, `containment_ledger_entries`/`max` 22 → 20, `containment_ledger_cannot_reach` 7 → 6, `containment_ledger_frozen_historical` 6 → 5, `control_ids`/`control_count` unchanged at 109).
- `scripts/gen-gate-docs.py` — one new `LITERAL_SCAN_DISCLOSED_BOUNDS` anchor (`criterion-3-cannot-reach-residue`); removed `('CLAUDE.md', '14')` and `('docs/ARCHITECTURE.md', '14')` from `_DEFERRED_CONTAINMENT_HITS`; re-pinned `_CONTAINMENT_LEDGER_MAX` (22 → 20) and `_CONTAINMENT_LEDGER_KEYS_DIGEST` with a new growth/shrink history comment explaining the coincidental-corroboration trap and why no non-colliding anchor-count choice was available this time.
- `CLAUDE.md`, `docs/ARCHITECTURE.md` — CONF-SURFACE's generated gate-table row cell updated to match, as the mechanical `--write` regeneration side effect; no other cell changed.
- `.planning/REQUIREMENTS.md` (gitignored) — RATCHET-01 and criterion 4's ticks enhanced with the mutation-demonstration evidence; RATCHET-03 and RATCHET-04 ticked with their own evidence lines; status table rows for both updated to `Complete`.
- `.planning/ROADMAP.md` (gitignored) — Phase 26 marked complete; success criteria 3, 4 and 6 given discharge notes with their own evidence; a closing note added stating `FIREWALL: GREEN` is not itself the evidence for any criterion; plan `26-07` checkbox ticked.

## Decisions Made

See `key-decisions` in the frontmatter above (verbatim, not repeated here per `docs/PROCESS.md` §1's own citation-not-restatement rule).

## Deviations from Plan

**1. [Rule 1 — blocking, directly caused by this plan's own edit] Adding the one new disclosed-bounds anchor coincidentally corroborated two unrelated frozen/cannot-reach containment-ledger entries.**
- **Found during:** Task 2, first `--self-test` run after adding bound (13)'s anchor.
- **Issue:** `disclosed_bounds_anchors` moved 13 → 14; `CLAUDE.md`'s own generated CI-gate table cell renders that count, and the digit "14" happened to already be the subject of two ledgered, unrelated containment findings — the frozen-historical `('CLAUDE.md', '14')` (a past milestone's requirement count) and the cannot-reach `('docs/ARCHITECTURE.md', '14')` (a skill-stub version-stamp sub-count). `containment_ledger_staleness_problems()` reported both keys as no longer matching any live finding.
- **Why:** the exact same trap plan 26-06 Task 3 hit when its own anchor-count change corroborated a frozen `'14'` entry — but unlike that plan (which had two new bounds to bundle under one anchor and could choose a non-colliding total, landing at 13), this plan adds exactly one new anchor, so the resulting total (14) was arithmetically forced and could not be chosen to avoid the collision.
- **Fix:** removed both now-stale ledger entries and re-pinned `_CONTAINMENT_LEDGER_MAX` (22 → 20) and `_CONTAINMENT_LEDGER_KEYS_DIGEST` in the same commit, with a comment explaining the trap and why reconciliation (rather than anchor-count avoidance) was the correct move this time.
- **Files modified:** `scripts/gen-gate-docs.py`.
- **Verification:** `containment_ledger_ratchet_problems()`/`staleness_problems()` both `[]`; `--self-test` (109 controls) and `--check` both pass; transcribed below.
- **Committed in:** `9ee3ae8` (Task 2 commit).

---

**Total deviations:** 1, a Rule 1 auto-fix directly caused by this plan's own edit (the same class of coincidental corroboration plan 26-06 already named and fixed once). No scope creep; no architectural decision required.

## Issues Encountered

None beyond the one auto-fixed item above, caught by running the plan's own prescribed verification commands (`--self-test`) rather than by inspection.

## Mutation Transcript

**Before the first mutation, on the real repository:**

```
$ git status --porcelain
(empty)
$ git rev-parse HEAD
dcbc3b436832602d6a35a97b8bd192b969e830ef
$ /usr/bin/grep -c "gen-gate-docs.py --check" .githooks/pre-commit
2
$ /usr/bin/grep -c "gen-gate-docs.py --check" scripts/git-hooks/pre-commit
2
```

**Scratch copy:**

```
$ SCRATCH=$(mktemp -d)
$ rsync -a --exclude .git . "$SCRATCH"/
```

**Arm A — unmutated control:**

```
$ cd "$SCRATCH" && python3 scripts/gen-gate-docs.py --check
harvested 22/22 expected script-backed entries (22 total)
EXIT: 0
```

**Arm B — mutate docs/README.md's own coverage-headline region (208 -> 999, no constant touched):**

```
$ sed -i 's/208 reproducible \/ 97 audit-only \/ 0 gap \/ 305 total/999 reproducible \/ 97 audit-only \/ 0 gap \/ 305 total/' docs/README.md
$ python3 scripts/gen-gate-docs.py --check
DRIFT: docs/README.md
--- a/docs/README.md
+++ b/docs/README.md
@@ -18,7 +18,7 @@
 <!-- GENERATED:README-COVERAGE-HEADLINE -->
 > **Current state — start here:** [`requirements-traceability.md`](requirements-traceability.md)
 > — the authoritative surface: active residuals, dispositions, and the **current** coverage
-> headline of **999 reproducible / 97 audit-only / 0 gap / 305 total**.
+> headline of **208 reproducible / 97 audit-only / 0 gap / 305 total**.
 >
 <!-- END GENERATED:README-COVERAGE-HEADLINE -->

DRIFT: docs/gates/CONF-SURFACE.md
[... Facts-fence derived_counts diff omitted here, transcribed in full in the executor's tool log ...]

Run: python3 scripts/gen-gate-docs.py --write && git add -u
harvested 22/22 expected script-backed entries (22 total)
EXIT: 1
```

`--self-test` on the same mutated scratch copy also failed (two controls that exercise `cmd_check()` against the real on-disk tree — `check-dispatch-wired` and `narrative-restatement-wired-into-cmd-check` — both report the same `DRIFT: docs/README.md` finding), exactly as plan 26-04's own mutation hit the identical shape: `gen-gate-docs: SELF-TEST FAIL [check-dispatch-wired] — DRIFT: docs/README.md ...`, exit 1.

**Arm B — restore and confirm:**

```
$ cp docs/README.md "$SCRATCH/docs/README.md"    # from the real repo
$ md5sum docs/README.md "$SCRATCH/docs/README.md"
cf12fb36a68862741f18835b971b97d6  docs/README.md
cf12fb36a68862741f18835b971b97d6  /tmp/tmp.GvzpUTs38p/docs/README.md
$ cd "$SCRATCH" && python3 scripts/gen-gate-docs.py --check
harvested 22/22 expected script-backed entries (22 total)
EXIT: 0
```

**Arm C — mutate CLAUDE.md's own coverage-headline region (208 -> 777, a different host surface from Arm B):**

```
$ sed -i 's/(\*\*208 reproducible \/ 97 audit-only \/ 0 gap \/ 305 total\*\*), compact historical ledger, and gap/(\*\*777 reproducible \/ 97 audit-only \/ 0 gap \/ 305 total\*\*), compact historical ledger, and gap/' CLAUDE.md
$ python3 scripts/gen-gate-docs.py --check > armC_check.txt 2>&1
$ echo "EXIT: $?"
EXIT: 1
$ /usr/bin/grep -n "^DRIFT:" armC_check.txt
1:DRIFT: CLAUDE.md
14:DRIFT: docs/gates/CONF-SURFACE.md
```

`DRIFT: CLAUDE.md` — a different file from Arm B's `docs/README.md`, proving the check is not fitted to Arm B's own target.

**Arm C — restore and confirm:**

```
$ cp CLAUDE.md "$SCRATCH/CLAUDE.md"
$ md5sum CLAUDE.md "$SCRATCH/CLAUDE.md"
c24d4a12b2d9f3f35e995a2c72386c4c  CLAUDE.md
c24d4a12b2d9f3f35e995a2c72386c4c  /tmp/tmp.GvzpUTs38p/CLAUDE.md
$ cd "$SCRATCH" && python3 scripts/gen-gate-docs.py --check
harvested 22/22 expected script-backed entries (22 total)
EXIT: 0
```

**Census arm — append a hand-typed restatement of the coverage headline to docs/MEASUREMENT-MAP.md, outside any generated fence:**

```
$ echo "" >> docs/MEASUREMENT-MAP.md
$ echo "Census-arm test line: 208 reproducible / 97 audit-only / 0 gap / 305 total." >> docs/MEASUREMENT-MAP.md
$ python3 scripts/gen-gate-docs.py --check > census_check.txt 2>&1
$ echo "EXIT: $?"
EXIT: 1
$ /usr/bin/grep -n "narrative-restatement" census_check.txt
1:narrative-restatement: docs/MEASUREMENT-MAP.md:103 restates the value docs/README.md's own generated-narrative-region renders, outside any generated fence (NARR-02)
2:narrative-restatement: docs/MEASUREMENT-MAP.md:103 restates the value docs/MEASUREMENT-MAP.md's own generated-narrative-region renders, outside any generated fence (NARR-02)
3:narrative-restatement: docs/MEASUREMENT-MAP.md:103 restates the value CLAUDE.md's own generated-narrative-region renders, outside any generated fence (NARR-02)
```

Names the file (`docs/MEASUREMENT-MAP.md`) and the exact line (`:103`), three times — once per roster region whose rendered value it restates.

**Census arm — restore and confirm:**

```
$ cp docs/MEASUREMENT-MAP.md "$SCRATCH/docs/MEASUREMENT-MAP.md"
$ md5sum docs/MEASUREMENT-MAP.md "$SCRATCH/docs/MEASUREMENT-MAP.md"
b93fb0e52c0c8076ab3e8aa3a9e89f0b  docs/MEASUREMENT-MAP.md
b93fb0e52c0c8076ab3e8aa3a9e89f0b  /tmp/tmp.GvzpUTs38p/docs/MEASUREMENT-MAP.md
$ cd "$SCRATCH" && python3 scripts/gen-gate-docs.py --check
harvested 22/22 expected script-backed entries (22 total)
EXIT: 0
```

**Cleanup and final real-repository confirmation:**

```
$ rm -rf "$SCRATCH"
$ git status --porcelain
(empty)
$ git rev-parse HEAD
dcbc3b436832602d6a35a97b8bd192b969e830ef   (unchanged)
$ git diff --name-only
(empty)
```

**Hook-file grep readings, both before and after the mutation work (unchanged):**

```
$ /usr/bin/grep -c "gen-gate-docs.py --check" .githooks/pre-commit
2
$ /usr/bin/grep -c "gen-gate-docs.py --check" scripts/git-hooks/pre-commit
2
$ git diff f2073f3..HEAD -- .githooks/pre-commit scripts/git-hooks/pre-commit
(empty)
```

## In-Process Verification Transcripts

**Task 2 — criterion 3's target, re-derived by module import:**

```python
target_surfaces = {"docs/PROCESS.md", "docs/README.md", "CONTRIBUTING.md",
                    "docs/MEASUREMENT-MAP.md", "docs/COMPONENT-DIAGRAM.md",
                    "docs/DATA-FLOW.md", "CLAUDE.md"}
read = run_literal_scan()
hits_on_target = [h for h in read.hits if h.relpath in target_surfaces]
non_exempt_on_target = [h for h in hits_on_target if _literal_hit_exemption(h) is None]
```

```
hits on 7 target surfaces: 80
non-exempt on 7 target surfaces: 0
literal_scan_non_exempt (global, unfiltered): 0
narrative_restatement_finding: 0
```

Breakdown of the 80 hits by exemption class: `deferred-literal-ledger`=64, `headline-provenance-delta`=13, `version-stamp-count`=2, `plan-number-identifier`=1.

**Task 2 — frozen-historical figures confirmed byte-unchanged, phase base vs. HEAD (content match, not fragile line-offset diff):**

```
'229 → 214 rows'      -> base(CLAUDE=1, README=0) head(CLAUDE=1, README=0)
'214 → 237 rows'      -> base(CLAUDE=1, README=0) head(CLAUDE=1, README=0)
'237 → 252 rows'      -> base(CLAUDE=1, README=0) head(CLAUDE=1, README=0)
'row count 252 → 266' -> base(CLAUDE=1, README=1) head(CLAUDE=1, README=1)
'row count 266'       -> base(CLAUDE=1, README=0) head(CLAUDE=1, README=0)
'row count 286'       -> base(CLAUDE=1, README=1) head(CLAUDE=1, README=1)
'row count 229'       -> base(CLAUDE=0, README=1) head(CLAUDE=0, README=1)
'row count 237'       -> base(CLAUDE=0, README=1) head(CLAUDE=0, README=1)
```

All eight readings identical at both endpoints.

**Task 2 — bound (13) anchor growth and ledger reconciliation:**

```
disclosed_bounds_anchors: 13 -> 14 (+1: criterion-3-cannot-reach-residue)
_CONTAINMENT_LEDGER_MAX: 22 -> 20
_CONTAINMENT_LEDGER_KEYS_DIGEST: sha256:847df3a5... -> sha256:3bf6da23...
containment_ledger_ratchet_problems()   -> []
containment_ledger_staleness_problems() -> []
```

**Task 2 — final verify, all green:**

```
python3 scripts/gen-gate-docs.py --self-test   # SELF-TEST PASS -- 109 controls run
python3 scripts/gen-gate-docs.py --check        # exit 0; harvested 22/22 expected script-backed entries
sh .githooks/pre-commit                          # all five gates PASS, exit 0
bash scripts/check-firewall-battery.sh           # FIREWALL: GREEN (26/26)
```

**Task 3 — criterion 6's invariance, direct count at the phase base commit vs. HEAD:**

```
$ git show f2073f3:scripts/check-firewall-battery.sh | /usr/bin/grep -nE '^\s*gate "|^\s*gate_prereq "'
[24 lines: DUAL-04, GATE-02-v8.5, STEP0-06, STEP0-08, VAL-01, VAL-02, VAL-03 (gate),
 VAL-03 (gate_prereq, counted once), VAL-04, VAL-05, VERSION-01, REG-GUARD, GATE-01,
 BATT-06, TRACE-03, COLLIDE-01, QUAL-01, PROV-GUARD, HARN-01, HARN-02, HARN-03,
 SCAN-GUARD, HC-BOUND, CONF-GATE, CONF-SURFACE]
$ /usr/bin/grep -nE '^\s*gate "|^\s*gate_prereq "' scripts/check-firewall-battery.sh
[identical 24 lines at HEAD]

$ git show f2073f3:.github/workflows/validation.yml | /usr/bin/grep -n "^\s*name:"
[24 lines: the workflow's own top-level "name: validation" + 23 job names]
$ /usr/bin/grep -n "^\s*name:" .github/workflows/validation.yml
[identical 24 lines at HEAD -- 23 CI jobs]

$ git show f2073f3:scripts/check-registration.py | /usr/bin/grep -n "BATTERY_ONLY_GATE_IDS: frozenset"
BATTERY_ONLY_GATE_IDS: frozenset[str] = frozenset({"QUAL-01"})
$ /usr/bin/grep -n "BATTERY_ONLY_GATE_IDS: frozenset" scripts/check-registration.py
BATTERY_ONLY_GATE_IDS: frozenset[str] = frozenset({"QUAL-01"})   [identical]
```

24 gate/gate_prereq registrations + 2 inline checks (INVARIANT-CHECK, FROZEN-EVIDENCE) = 26, byte-identical at both endpoints. 23 CI jobs, byte-identical. Exemption set `{"QUAL-01"}`, byte-identical.

```
$ bash scripts/check-firewall-battery.sh
...
FIREWALL: GREEN (26/26)
```

Battery's own report (26/26) agrees with the direct count (26) — the direct count is the evidence; the battery's agreement is corroboration, not substitution.

```
$ git diff --name-only f2073f3..HEAD | sort
CLAUDE.md
docs/ARCHITECTURE.md
docs/gates/CONF-SURFACE.md
docs/MEASUREMENT-MAP.md
docs/PROCESS.md
docs/README.md
.planning/phases/26-migration-apply-reconcile-generalize-enforce/26-01-SUMMARY.md
.planning/phases/26-migration-apply-reconcile-generalize-enforce/26-02-SUMMARY.md
.planning/phases/26-migration-apply-reconcile-generalize-enforce/26-03-SUMMARY.md
.planning/phases/26-migration-apply-reconcile-generalize-enforce/26-04-SUMMARY.md
.planning/phases/26-migration-apply-reconcile-generalize-enforce/26-05-SUMMARY.md
.planning/phases/26-migration-apply-reconcile-generalize-enforce/26-06-SUMMARY.md
scripts/gen-gate-docs.py
```

Neither `scripts/check-firewall-battery.sh` nor `.github/workflows/validation.yml` appears.

```
$ python3 scripts/check-registration.py --self-test
check-registration --self-test: PASS (29 controls: ...)
EXIT: 0
```

**Ledger readings, both taken by module import, before this plan and after its final commit:**

| Reading point | `len(_DEFERRED_LITERAL_HITS)` | `_DEFERRED_LEDGER_MAX` | `len(_DEFERRED_CONTAINMENT_HITS)` | `_CONTAINMENT_LEDGER_MAX` |
|---|---|---|---|---|
| Before this plan | 180 | 180 | 22 | 22 |
| After this plan | 180 | 180 | 20 | 20 |

The literal ledger is untouched by this plan (180/180 throughout); the containment ledger moved 22 → 20 as the direct, documented consequence of the coincidental-corroboration fix above (Deviation 1), not a new reconciliation pass.

`git diff --diff-filter=D --name-only` on both task commits returned empty — no unexpected deletions. `git status --porcelain` clean before the first edit and after each commit.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- Phase 27 (Ship v9.1.0, REL-05..08) can proceed directly: Phase 26 is complete, all seven of its requirements are ticked with their own evidence, `FIREWALL: GREEN (26/26)` holds (unchanged battery total, unchanged CI job count, unchanged REG-GUARD exemption set, all confirmed by direct count against the phase base), and both ledgers are reconciled (literal 180/180 untouched this plan; containment 20/20 after this plan's own fix).
- Backlog `999.41` (the `.py`-docstring bucket), `999.70` (the second G3 target), and the containment ledger's own remaining `cannot_reach`/`frozen_historical`/`not_a_count_claim` residue (now 20 entries: 6 cannot-reach, 5 frozen-historical, 9 not-a-count-claim) are published and named, not closed in-phase — consistent with D-06 proviso 2 and D-05 proviso 4, and explicitly not required for Phase 26's own closure.
- No blockers. `FIREWALL: GREEN (26/26)`, tally unchanged; CI job count unchanged at 23.

---
*Phase: 26-migration-apply-reconcile-generalize-enforce*
*Completed: 2026-09-10*
