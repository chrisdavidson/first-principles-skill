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

## Task 4: Checkpoint Response and Render-Fidelity Fix

### The checkpoint and the human's response

Task 4 (`checkpoint:human-verify`, `gate="blocking"`) paused after commits `53bb85a`/`9ee3ae8`/
`8659dc3`/`5c07689` (Tasks 1-3 plus the plan-summary/self-check commits above), asking the
developer to read the four migrated/edited product surfaces. The developer's response:

> "fix the rendering, accept the bounds"

**Accepted as-is, not revisited:**
- Disclosed bound (12): Python module docstrings excluded from criterion 3's region target; 47
  entries stay ledgered under backlog `999.41`, published not closed.
- Disclosed bound (13): the cannot-reach residue (`tests/premise-rejection-catalog.md`'s second
  G3 target, `docs/COMPONENT-DIAGRAM.md`'s fenced Mermaid label).
- The decision that `docs/v9.1-claim-containment-diagnosis.md` is not a region host.

**To fix:** three rendering regressions found by diffing the migrated surfaces against the
phase-base commit `f2073f3` — the migration is byte-neutral in rendered TEXT (RATCHET-01's own
drift check compares text, never parsed block structure) but was not byte-neutral in rendered
BLOCK STRUCTURE. No gate in this repository caught this class before the checkpoint, because the
text bytes were, and remain, preserved.

### Root cause, per file, with the CommonMark rule that explains it

**1. `docs/README.md` — the blockquote was split.** At `f2073f3` the "Current state — start
here" paragraph and the "Historical terminal record" paragraph lived in ONE blockquote (base
lines 18-22: a continuous `>`-prefixed block with a bare `>` separator line between the two
paragraphs). The migration's markers were bare, column-0 HTML comments
(`<!-- GENERATED:README-COVERAGE-HEADLINE -->`, no leading `>`). A line that is not `>`-prefixed
is not eligible for blockquote lazy continuation when it itself opens a new block (an HTML
comment is CommonMark start-condition type 2, one of the six conditions that MAY interrupt an
open construct) — so each bare marker line terminated the enclosing blockquote rather than
continuing it, turning one blockquote into a sequence of disconnected blockquote/HTML-block
fragments (visually: two separate blockquotes, the invisible comments contributing no visible
box of their own).

**2. `CLAUDE.md` — the list item went from tight to loose, and worse.** At `f2073f3` the
`- **docs/requirements-traceability.md**` bullet was ONE contiguous paragraph (bullet head +
"Active residuals...findings." + "(Derived from..." + the historical-count narration, all on
2-space-indented continuation lines with zero blank lines anywhere in the span). The migration
put a blank line immediately before the START marker and immediately after the END marker
(making the item loose — CommonMark: "A list is loose if any of its constituent list items are
separated by blank lines, or if any of its constituent list items directly contain two
block-level elements with a blank line between them... paragraphs in a loose list are wrapped in
`<p>` tags, while paragraphs in a tight list are not"), AND placed both markers at column 0
inside a list item whose content column is 2 (set by the `"- "` bullet marker). A line that is
under-indented relative to a list item's content column is eligible for lazy continuation ONLY
if it would otherwise be ordinary paragraph continuation text; a line that itself opens an
interrupting block (our HTML comment, again start-condition type 2) does not qualify — so the
column-0 marker did not merely make the item loose, it fell OUT of the list item entirely,
silently ejecting everything physically after it (the sentence, and the historical-count
narration) into top-level, non-list content. This is the more severe of the two defects and was
flagged explicitly in the resume instructions as something to verify by reasoning through the
render, not assume.

**3. `docs/MEASUREMENT-MAP.md` — the region over-scoped.** The fence enclosed not only its
sentence but the trailing blank line AND the `---` thematic break beneath it (the original
bootstrap swallowed both because `"---"` repeats four times elsewhere on the page and could not
serve as a unique bootstrap anchor for a NARROWER region). Rendering was unaffected here (an
HTML comment either side of `sentence\n\n---` doesn't change what's visible), but the fence had
no rendering business owning a horizontal rule it could, in principle, rewrite on a future
regeneration.

### The fix

**Roster/marker literal changes (`scripts/gen-gate-docs.py`)** — engineered at the source of
truth, not by hand-editing the emitted files into shape:

- `README_HEADLINE_MARKERS` now carries a `"> "` blockquote-continuation prefix on BOTH marker
  lines: `"> <!-- GENERATED:README-COVERAGE-HEADLINE -->"` / `"> <!-- END GENERATED:... -->"`.
  `_replace_region`/`_generated_line_flags`/`_fenced_line_flags` all match markers on WHOLE-LINE
  content, so this is a complete, ordinary marker to every one of them — no mechanism change
  needed, only the literal.
- `CLAUDE_HEADLINE_MARKERS` now carries a two-space list-item-continuation prefix on BOTH marker
  lines, matching the item's own content column.
- `_NARRATIVE_REGIONS[1]` (docs/MEASUREMENT-MAP.md)'s `template` is narrowed to the bare
  sentence — the trailing `"\n\n---"` is dropped, and the blank line plus `"---"` now live
  OUTSIDE the end marker on disk.
- The surrounding rationale comments (which had described the swallowed shape as an intentional
  design, not a bug) are corrected to describe the fixed shape and to name the T-26-13 finding;
  the bootstrap-only path (`_replace_or_bootstrap_region`'s shared `"\n{start}\n{body}{end}\n\n"`
  block format) is explicitly left unchanged and its residual limitation documented in a comment
  — that path is provably dead for all three regions today (their markers already exist, so
  every `--write`/`--check` takes `_replace_region` instead), and re-engineering a bootstrap path
  that cannot itself be exercised was judged disproportionate to this fix.

**On-disk realignment (one-time hand edit, matching the new source of truth):**
- `docs/README.md`: both marker lines gained the `"> "` prefix; the stray blank line between the
  end marker and "Historical terminal record" was removed.
- `CLAUDE.md`: both marker lines gained the two-space prefix; the blank lines before the start
  marker and after the end marker were removed.
- `docs/MEASUREMENT-MAP.md`: the end marker was moved to sit immediately after the sentence,
  ahead of the blank line and `"---"`.

`python3 scripts/gen-gate-docs.py --check` confirmed **zero drift** against this new source of
truth immediately after the hand edits (before `--write` was ever run) — proof the edits are
exactly what the roster now generates, not merely plausible.

### Block-structure fidelity vs. `f2073f3`, by transcript

Text-diff against the phase base, restricted to the touched span (only the marker lines
inserted/moved; no other line altered — `f2073f3` here is a stand-in for the phase-base
comparison target used per the plan's `<interfaces>` block, i.e. `git show f2073f3:<path>`):

```
$ diff <(git show f2073f3:docs/README.md | sed -n '15,26p') <(sed -n '15,25p' docs/README.md)
3a4
> > <!-- GENERATED:README-COVERAGE-HEADLINE -->
7a9
> > <!-- END GENERATED:README-COVERAGE-HEADLINE -->
10,12d11
< [continuing historical-narration lines beyond the compared window]
```

Block-by-block classification (a narrow, purpose-built classifier applying only the CommonMark
rules this comparison needs — blockquote continuation/lazy-continuation, list-item paragraph
interruption by an HTML comment, blank-line breaks, thematic breaks, headings — built and run in
`/tmp/.../scratchpad/block_walk.py`, never shipped):

**`docs/README.md`** — BASE vs FIXED:

```
BASE                                              FIXED
BLOCKQUOTE-OPEN  > gate-load-bearing...           BLOCKQUOTE-OPEN  > gate-load-bearing...
  bq-paragraph-START                                bq-paragraph-START
  bq-paragraph-continuation ...kept.                bq-paragraph-continuation ...kept.
BLANK (real break)                                BLANK (real break)
BLOCKQUOTE-OPEN  > Current state...               BLOCKQUOTE-OPEN  > <!-- GENERATED:... -->
  bq-paragraph-START                                bq-html-comment (invisible, ends para)
  bq-paragraph-continuation                         bq-paragraph-START  > Current state...
  bq-paragraph-continuation                         bq-paragraph-continuation
  bq-blank-in-quote (para ends, quote OPEN)          bq-paragraph-continuation
  bq-paragraph-START  > Historical terminal...       bq-blank-in-quote (para ends, quote OPEN)
                                                      bq-html-comment (invisible, ends para)
                                                      bq-paragraph-START  > Historical terminal...
```

`BLOCKQUOTE-OPEN` fires exactly ONCE in each of the two container spans, both base and fixed —
the blockquote never closes and reopens; it stays a single container with the identical 2-paragraph
split base already had (the bare `>` line was already a paragraph break in the BASE commit, not
something this fix introduced), plus two additional invisible HTML-comment children. Rendered
result: one `<blockquote>` wrapping two `<p>` elements, identical to base, with two comments that
render nothing.

**`CLAUDE.md`** — BASE vs FIXED (list item, de-indented by its own 2-space content column):

```
BASE                                              FIXED
paragraph-START  the authoritative source...      paragraph-START  the authoritative source...
  paragraph-continuation  Active residuals...      HTML-COMMENT (invisible, interrupts para)
  paragraph-continuation  (Derived from...          paragraph-START  Active residuals...
                                                     paragraph-continuation
                                                     paragraph-continuation  findings.
                                                     HTML-COMMENT (invisible, interrupts para)
                                                     paragraph-START  (Derived from...
```

No blank line appears anywhere in either span, so per the CommonMark tight/loose rule quoted
above, the list stays TIGHT in both BASE and FIXED — meaning FIXED's three paragraph nodes each
render WITHOUT a wrapping `<p>` tag, exactly like BASE's one merged paragraph. In the tight-list
HTML rendering, adjacent bare inline-content blocks separated only by a source newline (no `<p>`,
no visible box for the invisible comments) collapse to a single flowing line when rendered by a
standard HTML client, because a bare newline between text nodes is ordinary collapsible
whitespace, not a block-level break. This is the mechanism that restores "one flowing
description": not a literal merge into one `<p>` node (the comments genuinely interrupt the
paragraph at the AST level), but the absence of any `<p>`-imposed visual break, which is what a
loose list's spacing would have introduced and what BASE never had.

**`docs/MEASUREMENT-MAP.md`** — BASE vs FIXED:

```
BASE                                              FIXED
paragraph-START  For the complete...              HTML-COMMENT (invisible)
BLANK (real break)                                paragraph-START  For the complete...
THEMATIC-BREAK (---)                              HTML-COMMENT (invisible)
BLANK (real break)                                BLANK (real break)
HEADING  ## Live thresholds...                    THEMATIC-BREAK (---)
                                                   BLANK (real break)
                                                   HEADING  ## Live thresholds...
```

Identical visible sequence (paragraph, break, thematic break, break, heading) with two invisible
comments flanking the paragraph and no longer enclosing the thematic break — the strongest match
of the three, since nothing here depends on tight/loose or lazy-continuation subtlety.

### Both ledger pins, confirmed unmoved by this continuation

```
$ python3 -c "... print(len(_DEFERRED_LITERAL_HITS), _DEFERRED_LEDGER_MAX,
                        len(_DEFERRED_CONTAINMENT_HITS), _CONTAINMENT_LEDGER_MAX)"
before this continuation's edits: 180 180 20 20
after this continuation's edits:  180 180 20 20
```

Both pins are byte-unchanged by this continuation's own work. Note: the resume instructions
stated `_CONTAINMENT_LEDGER_MAX` "must stay 22" — that figure predates this same plan's own Task
2 (commit `9ee3ae8`), which re-pinned it 22 → 20 as a documented, already-committed deviation
(the coincidental cross-check corroboration recorded above, under "Deviations from Plan").
20 is the value at the moment this checkpoint fired and the value this continuation is bound not
to move further; it has not moved, which is the operative guarantee the resume instructions were
asking for ("This continuation is not permitted to move a pin").

### The invisible-regression class: control added, not backlogged

**Decision: added a cheap, real control** — `narrative_region_marker_context_problems()`, wired
into `cmd_check()`'s aggregated problems (`scripts/gen-gate-docs.py`). For every registered
region: the START marker's own leading blockquote-`>`/list-indent prefix must equal its body's
first line's prefix, and the END marker's prefix must equal its body's last line's prefix. A
mismatch names the surface, both markers, and both observed prefixes.

**Why a control, not a backlog item:** a full CommonMark parser was considered and rejected —
this module already has three independent block-aware primitives (`_fenced_line_flags`,
`_generated_line_flags`, the containment loop's own number-adjacency heuristic) and none of them
is a general block parser; adding a fourth, heavier one to catch a single regression class would
repeat the "widened criterion" move this same phase's Task 2 already rejected once, for a
different check (D-06 proviso 2's synthetic-fixture/widened-criterion rejection, applied here by
the same reasoning). A narrow prefix-equality comparison is proportionate and sufficient because
every registered region host uses exactly one of two container idioms (blockquote `"> "`, or
list-item indentation) or neither (a plain paragraph) — a marker whose own leading container
prefix disagrees with its body's is a marker in the wrong container, full stop, regardless of
which idiom is in play. The comparison normalizes away the one legitimate cosmetic difference
within a shared container (a bare `">"` continuation line vs. a `"> "`-prefixed marker line,
both the same blockquote depth) by comparing only the leading run of bare `>` characters, not
the optional trailing space CommonMark allows after each one.

Proof the control works, not merely exists:
```
$ python3 -c "... print(m.narrative_region_marker_context_problems())"
real tree (fixed):    []
synthetic mismatch:   ["narrative-marker-context: fixtures/ctx.md start marker '<!-- GENERATED:CTX-TEST -->'
                        carries prefix '', but its own body's first line carries '>' -- the marker sits
                        in a different blockquote/list-item container than its body (NARR-02/T-26-13)",
                       "... end marker ... carries prefix '' ... body's last line carries '>' ..."]
```

Three new `--self-test` controls (109 → 112, cascading a `--write` refresh of CLAUDE.md's,
docs/ARCHITECTURE.md's and docs/gates/CONF-SURFACE.md's own generated CONF-SURFACE table
cell/Facts fence — no other cell changed): `narrative-marker-context-legs` (four fixture legs:
blockquote match, blockquote mismatch/T-26-13's own shape, list-indent match, plain-paragraph
match, plus the bare-`>`-vs-`"> "` non-mismatch case matching docs/README.md's own real shape),
`narrative-marker-context-live-tree-clean` (asserts the REAL, now-fixed three regions pass, not
just a fixture resembling them), and `narrative-marker-context-wired-into-cmd-check` (the same
monkeypatch-stub proof pattern `narrative-restatement-wired-into-cmd-check` already uses for its
sibling check).

### Full verification, all green

```
$ python3 scripts/gen-gate-docs.py --self-test
gen-gate-docs: SELF-TEST PASS — 112 controls run

$ python3 scripts/gen-gate-docs.py --check
harvested 22/22 expected script-backed entries (22 total)
$ echo $?
0

$ sh .githooks/pre-commit
report-conformance: SELF-TEST PASS — 102 controls run
report-conformance: PASS — no drift
gen-gate-docs: SELF-TEST PASS — 112 controls run
harvested 22/22 expected script-backed entries (22 total)
$ echo $?
0

$ bash scripts/check-firewall-battery.sh
[... 24 gate/gate_prereq PASS lines + 2 inline PASS + 1 INFO ...]
FIREWALL: GREEN (26/26)
$ echo $?
0
```

`git diff --diff-filter=D --name-only HEAD~1 HEAD` (after the fix commit) is empty — no
unexpected deletions. `git status --short` clean before the first edit of this continuation and
after the fix commit.

### Task Commits (Task 4, this continuation)

4. **Task 4: fix the three rendering regressions, add the T-26-13 control, close the phase** —
   `97fdceb` (fix). Touches `scripts/gen-gate-docs.py`, `docs/README.md`, `CLAUDE.md`,
   `docs/MEASUREMENT-MAP.md`, `docs/ARCHITECTURE.md`, `docs/gates/CONF-SURFACE.md`. One atomic
   commit rather than three: all three per-file marker/template changes and the new control live
   in the same generator file and are only jointly self-test/`--check`-consistent (the
   control_ids cascade into CLAUDE.md/ARCHITECTURE.md/CONF-SURFACE.md's own generated table cell
   depends on the control addition landing in the same pass as the marker/template fixes it
   documents) — splitting them into three commits would have required staging partial-file diffs
   with no clean boundary and no independent verifiable state in between.

### Deviations from Plan (Task 4)

**2. [Rule 1 — bug, directly caused by adding a new self-test control] Adding three new controls
raised `control_ids`/`control_count` (109 → 112), staling CLAUDE.md's/docs/ARCHITECTURE.md's own
generated CONF-SURFACE table cell and docs/gates/CONF-SURFACE.md's Facts fence.**
- **Found during:** first `--self-test`/`--check` run after wiring
  `narrative_region_marker_context_problems()` and its three controls.
- **Issue:** `--self-test` passed (112 controls) but the standalone "wired into cmd_check" control
  failed with a `DRIFT: CLAUDE.md` / `DRIFT: docs/ARCHITECTURE.md` finding — the CONF-SURFACE
  table row's own `control_ids=109; control_count=109` text was now stale against the freshly
  regenerated `112`.
- **Why:** the exact same self-referential cascade Task 2 of this plan (and plan 26-06 before it)
  already hit and named: CONF-SURFACE's own meta-facts (control count) are themselves rendered
  inside the generated surfaces it describes, so adding a control changes what those surfaces
  must say about themselves.
- **Fix:** ran `python3 scripts/gen-gate-docs.py --write`, which regenerated exactly
  `CLAUDE.md`'s and `docs/ARCHITECTURE.md`'s CONF-SURFACE table cell and
  `docs/gates/CONF-SURFACE.md`'s Facts fence (`control_ids`/`control_count` 109 → 112,
  `roster_arm_payload_assert_sites` 50 → 51 as an incidental side effect of the new asserts added)
  — no other cell changed, confirmed by `git diff` review before staging.
- **Files modified:** `CLAUDE.md`, `docs/ARCHITECTURE.md`, `docs/gates/CONF-SURFACE.md`.
- **Verification:** `--self-test` (112 controls), `--check`, `sh .githooks/pre-commit`, and
  `bash scripts/check-firewall-battery.sh` (`FIREWALL: GREEN (26/26)`) all pass after the `--write`.
- **Committed in:** `97fdceb` (Task 4 commit).

**Total deviations, this continuation:** 1, a Rule 1 auto-fix directly caused by this
continuation's own edit (the same self-referential-cascade class this plan's Task 2 and plan
26-06 already named once each). No scope creep; no architectural decision required.

### Phase close, reconfirmed after the fix

- All seven Phase 26 requirements remain ticked in `.planning/REQUIREMENTS.md` with their own
  evidence lines (unchanged by this continuation — the fix touched no requirement's own text).
- `.planning/ROADMAP.md`'s Phase 26 entry remains marked complete with all six success criteria's
  discharge evidence in place (`/usr/bin/grep -n "Phase 26" .planning/ROADMAP.md` shows the
  `- [x] **Phase 26: Migration**` roadmap-index line and the phase's own `### Phase 26:` section,
  unchanged by this continuation).
- `FIREWALL: GREEN (26/26)` holds after the fix, with the same 26/26 tally as before it (the new
  controls are counted inside CONF-SURFACE's own `control_ids`/`control_count`, not as a new
  battery registration — the battery/CI/exemption invariance Task 3 reconciled is unaffected).
- Both ledgers unmoved by this continuation (180/180, 20/20 — see above).

---
*Phase: 26-migration-apply-reconcile-generalize-enforce*
*Completed: 2026-09-10*

## Self-Check: PASSED

- FOUND: `docs/gates/CONF-SURFACE.md`
- FOUND: `scripts/gen-gate-docs.py`
- FOUND: `CLAUDE.md`
- FOUND: `docs/ARCHITECTURE.md`
- FOUND: commit `53bb85a` in `git log --oneline --all`
- FOUND: commit `9ee3ae8` in `git log --oneline --all`
- FOUND: commit `8659dc3` in `git log --oneline --all`

## Self-Check (Task 4 continuation): PASSED

- FOUND: `docs/README.md`
- FOUND: `docs/MEASUREMENT-MAP.md`
- FOUND: `CLAUDE.md`
- FOUND: `scripts/gen-gate-docs.py`
- FOUND: commit `97fdceb` in `git log --oneline --all`
- CONFIRMED: `python3 scripts/gen-gate-docs.py --self-test` — SELF-TEST PASS, 112 controls run
- CONFIRMED: `python3 scripts/gen-gate-docs.py --check` — exit 0
- CONFIRMED: `sh .githooks/pre-commit` — exit 0 (5 gates)
- CONFIRMED: `bash scripts/check-firewall-battery.sh` — FIREWALL: GREEN (26/26)
- CONFIRMED: `_DEFERRED_LEDGER_MAX` 180/180, `_CONTAINMENT_LEDGER_MAX` 20/20, both unmoved
- CONFIRMED: `narrative_region_marker_context_problems()` returns `[]` against the real tree
