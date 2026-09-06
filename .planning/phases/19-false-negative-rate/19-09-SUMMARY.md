---
phase: 19-false-negative-rate
plan: 09
subsystem: testing
tags: [adversarial-corpus, conformance, false-negative-rate, report-conformance, gap-closure, checkpoint-decision]

# Dependency graph
requires:
  - phase: 19-false-negative-rate (plans 01-08, waves 1-7)
    provides: "the 13-item frozen corpus, catalog.md's closed-vocabulary Target column,
      report-conformance.py's target_missed/no_column_fired split, and
      19-VERIFICATION.md's remaining two gap-closure items this plan closes"
provides:
  - "scripts/report-conformance.py: _corpus_target_problems (vacuity / stratum-consistency
    / caught-set-drift layers), _CORPUS_TARGET_CAUGHT_LOCK, differentiated SILENT PASS
    messages, a 5th censused call site, and 7 new self-test controls (51 -> 58)"
  - "tests/adversarial-corpus-v9.0/*.md (13 items) + README.md: an in-file
    'ADVERSARIAL FIXTURE — DELIBERATELY FALSE' marker on every item, a recorded
    add-marker decision, and a moved 13-row sha256 chain-of-custody table"
affects: []

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Symmetric source-literal lock, not a ratchet (D-19-09-B): _CORPUS_TARGET_CAUGHT_LOCK
       fails --check on a catch gained as loudly as a catch lost, closing 19-CONTEXT.md
       D-07's disclosed 'the drift gate fails on staleness, not on a catch being lost'
       residual without registering a new gate."
    - "Union-widened disposition floor, never re-scoped (D-19-09-A): a row is inside
       CONF-08's zero-silent-passes floor if EITHER target_missed OR no_column_fired is
       True, so the floor can never be narrower than either predicate's own scope alone."
    - "Identical marker text on all thirteen corpus items, not just the eight
       near-byte-identical ones, so the marker's presence does not itself become a signal
       distinguishing 'close copy' from 'hand-authored' falsified content."

key-files:
  created: []
  modified:
    - scripts/report-conformance.py
    - tests/adversarial-corpus-v9.0/README.md
    - tests/adversarial-corpus-v9.0/t01-ledger-arbitrary-chain.md
    - tests/adversarial-corpus-v9.0/t02-fabricated-read-at-source.md
    - tests/adversarial-corpus-v9.0/t03-composition-cycle.md
    - tests/adversarial-corpus-v9.0/t04-chain-only-head-ungrounded.md
    - tests/adversarial-corpus-v9.0/t05-selfaudit-overclaim-under-cycle.md
    - tests/adversarial-corpus-v9.0/t06-hidden-cycle-past-head.md
    - tests/adversarial-corpus-v9.0/t07-non-sequitur-between-hops.md
    - tests/adversarial-corpus-v9.0/t08-verdict-contradicts-its-type.md
    - tests/adversarial-corpus-v9.0/t09-arithmetic-does-not-follow.md
    - tests/adversarial-corpus-v9.0/t11-fabricated-ground-truth.md
    - tests/adversarial-corpus-v9.0/t12-inline-citation-wrong-chain.md
    - tests/adversarial-corpus-v9.0/t13-grounded-alongside-cyclic-ref.md
    - tests/adversarial-corpus-v9.0/t14-order-of-magnitude-conversion.md

key-decisions:
  - "Checkpoint (Task 2, plan D-19-09-C): selected option id `add-marker`, date
     2026-09-05, decider Christopher Davidson. Recorded verbatim in this SUMMARY before
     Task 3 began, per the plan's own acceptance criterion."
  - "Executed the add-marker branch exactly as specified: identical two-line blockquote
     prepended to all thirteen items, thirteen sha256 rows moved, catalog.md left
     byte-unchanged, all fifteen -- actually fourteen, see Deviations -- changed files
     landed in one commit alongside the moved sha256 table so FROZEN-EVIDENCE never saw
     an intermediate untracked-drift state."
  - "Re-proved measurement neutrality across all thirteen items by measurement (diffing
     regenerated docs/conformance-baseline.md and docs/data/conformance.json against
     pre-edit scratch copies), rather than trusting 19-REVIEW.md's single-item (t01)
     check."

requirements-completed: [CONF-07, CONF-08]

# Metrics
duration: ~1h
completed: 2026-09-05
---

# Phase 19 Plan 09: Catalogued-Target Join Floors + Adversarial-Corpus Falsity Marker Summary

**CONF-08's zero-silent-passes floor now carries a vacuity arm, a stratum-consistency
check, and a symmetric caught-set lock over the catalogued-target join (closing
19-VERIFICATION.md's third gap-closure item), and all thirteen adversarial-corpus items
now carry an identical in-file "ADVERSARIAL FIXTURE — DELIBERATELY FALSE" marker per a
human decision made at this plan's Task 2 checkpoint — closing the CR-02 blocker
19-REVIEW.md raised over eight near-byte-identical falsified twins of shipped exemplars.**

## Performance

- **Duration:** ~1h
- **Completed:** 2026-09-05
- **Tasks:** 3 completed (Task 1 auto, Task 2 checkpoint:decision, Task 3 auto)
- **Files modified:** 16 total across two commits (1: `scripts/report-conformance.py`;
  14: 13 corpus items + `README.md`)

## Task 2 Checkpoint Decision (recorded before Task 3 began)

**Selected option id:** `add-marker`
**Date:** 2026-09-05
**Decider:** Christopher Davidson

Presented per D-19-09-C: `19-VERIFICATION.md` did not score the missing in-file marker as
a requirement failure (CONF-07/CONF-08 as literally written are satisfied by the
`catalog.md` sidecar); `19-REVIEW.md` (CR-02) rated it a blocker. The concrete fact shown
at the checkpoint — the first ten lines of `tests/adversarial-corpus-v9.0/
t12-inline-citation-wrong-chain.md` and `shared/examples/product-business.md` are
byte-identical, and `grep -rl "ADVERSARIAL FIXTURE\|DELIBERATELY FALSE"
tests/adversarial-corpus-v9.0/*.md` returned zero matches before this plan — was resolved
by the human selecting `add-marker`.

## Accomplishments

- Added `_corpus_target_problems` to `scripts/report-conformance.py`: a vacuity layer
  (fails `TARGET JOIN VACUOUS` if every corpus row reads `target_missed=True`), a
  stratum-consistency layer (`TARGET/STRATUM CONTRADICTION` for stratum A + target
  `none`, or non-A + a named `detect_defects` column; `TARGET FORM` for a `MISSING`
  stratum or target), and a caught-set-drift layer against the new
  `_CORPUS_TARGET_CAUGHT_LOCK` (fails `TARGET CAUGHT-SET DRIFT` on movement in EITHER
  direction).
- Differentiated `_corpus_disposition_problems`' `SILENT PASS` message so a reader can
  tell, without opening the code, which condition (catalogued target missed vs. no
  column fired) put a row inside CONF-08's floor.
- Widened `_CORPUS_CALL_SITES` / `_CORPUS_CALL_FORMS` / `_CORPUS_CALL_SITES_LOCK` from 4
  to 5 entries, adding `_corpus_target_problems`, and wired it into `cmd_check()` between
  `_corpus_disposition_problems` and `_corpus_population_problems`.
- Added 7 new self-test controls (51 -> 58): `corpus-disposition-target-missed-covered`,
  `corpus-disposition-union-not-narrower`, `corpus-disposition-caught-and-fired-skipped`,
  `corpus-target-vacuity-detected`, `corpus-target-stratum-contradiction-detected`,
  `corpus-target-caught-set-drift-detected`, `corpus-target-caught-lock-values-locked`.
- Prepended an identical two-line "ADVERSARIAL FIXTURE — DELIBERATELY FALSE" blockquote
  marker, above the title line, to all thirteen `tests/adversarial-corpus-v9.0/t*.md`
  items.
- Moved all thirteen item rows of `README.md`'s sha256 chain-of-custody table in the same
  commit as the marker edits (`catalog.md`'s row is unchanged — not edited by this
  branch), and added a new `## Why every item carries an in-file marker` section
  recording the decision, its date, decider, and the risk it closes.
- Re-proved measurement neutrality by measurement, across all thirteen items: regenerated
  `docs/conformance-baseline.md` and `docs/data/conformance.json` are byte-identical to
  copies captured before the marker edit.

## Task Commits

1. **Task 1: Key CONF-08's disposition floor on the union, add the target-consistency
   floor, and widen the call-site census** — `10d6747` (feat)
2. **Task 2: CHECKPOINT — decide whether the 13 corpus items carry an in-file
   "deliberately false" marker** — no commit (decision-only; recorded above and in the
   coordinator's relayed message)
3. **Task 3: Execute the selected branch (add-marker), then record the phase's closing
   evidence** — `f0f7c31` (feat)

**Plan metadata:** this SUMMARY.md (docs commit follows).

## Step 1 evidence: before/after disposition-floor row sets (Task 1)

Commands run against the live tree before any Task-1 code change (the union widening
itself was already shipped by plan 19-08, per its own recorded assumption-drift note; this
plan's Step 1 re-measured the current reach before adding the new floors):

```
no_column_fired=True (9): t01-ledger-arbitrary-chain, t02-fabricated-read-at-source,
  t06-hidden-cycle-past-head, t07-non-sequitur-between-hops,
  t08-verdict-contradicts-its-type, t09-arithmetic-does-not-follow,
  t11-fabricated-ground-truth, t12-inline-citation-wrong-chain,
  t14-order-of-magnitude-conversion

target_missed=True (10): the same 9, plus t13-grounded-alongside-cyclic-ref

union (10): identical to the target_missed=True set — the union is a strict superset of
  the no_column_fired-alone set (delta = {t13-grounded-alongside-cyclic-ref}), proving the
  widening cannot have narrowed the floor's reach.

caught (target_missed=False, 3): t03-composition-cycle, t04-chain-only-head-ungrounded,
  t05-selfaudit-overclaim-under-cycle
```

## Before/after `--self-test` control counts

- Before this plan (end of 19-08): **51 controls**.
- After Task 1 (`10d6747`): **58 controls** (+7, exactly the plan's acceptance floor).
- After Task 3 (`f0f7c31`): **58 controls** (unchanged — Task 3 touches corpus content and
  `README.md`, not the self-test battery).

## Named neutralizations performed (Task 1, each applied alone, reverted, confirmed reverted)

**N1 — reverted `_corpus_disposition_problems`' gate to the old single-predicate check**
(`if r["no_column_fired"] is not True: continue`), applied in place then restored:

```
report-conformance: SELF-TEST FAIL [corpus-disposition-target-missed-only-checked] — []
report-conformance: SELF-TEST FAIL [corpus-disposition-target-missed-covered] — []
```

Fired by name against both the pre-existing (19-08) and the new (19-09) control for this
exact shape. Reverted; `--self-test` back to `PASS — 58 controls run`.

**N2 — deleted `problems += _corpus_target_problems(corpus_rows)` from `cmd_check`:**

```
report-conformance: SELF-TEST FAIL [corpus-call-site-census-positive] — ["CALL-SITE
CENSUS: _corpus_target_problems occurs 0 time(s) in cmd_check's source, expected 1",
"CALL-FORM LOCK: _corpus_target_problems's expected call form not found in cmd_check's
source: 'problems += _corpus_target_problems(corpus_rows)'"]
```

Fired by name, naming the exact symbol. Reverted; `--self-test` back to PASS.

**N3 — commented out the same line with a leading `#`:**

```
report-conformance: SELF-TEST FAIL [corpus-call-site-census-positive] — ["CALL-SITE
CENSUS: _corpus_target_problems occurs 0 time(s) in cmd_check's source, expected 1",
"CALL-FORM LOCK: ..."]
```

`_strip_line_comments` makes the commented-out call indistinguishable from a deleted one,
exactly as required. Restored; `--self-test` back to PASS.

**N4 — removed `t05-selfaudit-overclaim-under-cycle` from `_CORPUS_TARGET_CAUGHT_LOCK`,
ran `--check` against the LIVE tree:**

```
report-conformance: FAIL — TARGET CAUGHT-SET DRIFT: gained=['t05-selfaudit-overclaim-under-cycle'] lost=[]
```

Fired by name, naming that exact stem under `gained=`. Restored; re-confirmed
`report-conformance: PASS — no drift`.

## Pinned `_CORPUS_TARGET_CAUGHT_LOCK` value (Task 1)

Derivation command and verbatim output:

```
$ python3 -c "
import json
data = json.load(open('docs/data/conformance.json'))
rows = data['adversarial_corpus']['rows']
print(sorted(r['analysis_id'] for r in rows if r['target_missed'] is False))
"
['t03-composition-cycle', 't04-chain-only-head-ungrounded', 't05-selfaudit-overclaim-under-cycle']
```

Pinned as `_CORPUS_TARGET_CAUGHT_LOCK = frozenset({"t03-composition-cycle",
"t04-chain-only-head-ungrounded", "t05-selfaudit-overclaim-under-cycle"})`, unchanged by
Task 3 (the marker branch adds no corpus item and removes none).

## Task 3 (add-marker branch): measurement-neutrality proof

Baseline captured before any corpus edit, `--check` confirmed clean first:

```
$ python3 scripts/report-conformance.py --check
report-conformance: PASS — no drift
```

`docs/conformance-baseline.md` and `docs/data/conformance.json` copied to a scratch
location outside the repo. All thirteen items marked (verified: `grep -rl "ADVERSARIAL
FIXTURE" tests/adversarial-corpus-v9.0/t*.md | wc -l` → `13`; `catalog.md` untouched, its
sha256 unchanged at `e4a355eaad300cf10cfd0e55bc674f1f8950b4872708aa0653d4ba7799d33766`).

Re-ran the generator and diffed both regenerated artifacts against the pre-edit scratch
copies:

```
$ python3 scripts/report-conformance.py
report-conformance: PASS — wrote .../docs/conformance-baseline.md +
  .../docs/data/conformance.json (42 rows)

$ diff <scratch>/conformance-baseline.md.orig docs/conformance-baseline.md
(no output, exit 0)

$ diff <scratch>/conformance.json.orig docs/data/conformance.json
(no output, exit 0)
```

Both diffs empty across **all thirteen** items, not just `t01` as `19-REVIEW.md` measured
— the marker moved no reading. Neither the marker branch's own criterion, nor any
`docs/`-artifact regeneration, was needed to absorb a moved figure.

## sha256 chain-of-custody: recomputed as the last edit, moved into `README.md`

```
$ sha256sum tests/adversarial-corpus-v9.0/*.md
e4a355eaad300cf10cfd0e55bc674f1f8950b4872708aa0653d4ba7799d33766  catalog.md            (unchanged)
74b4c1ee9572654ea49ea16047eb1b65f807dfa931fe3cfdc8640655e68af1cc  README.md             (not in table, self-hash)
ad47ae04633eb299582cf2095f8df4e3a10136f3a65edf03ad99ac6de436d2aa  t01-ledger-arbitrary-chain.md
fbc26f04ecc4a3ca8e2285fda44c732f188e394e7cbf109fa0b489b501c520fe  t02-fabricated-read-at-source.md
fc8cbc6fd0ed0593008163a3987ef7d4bd50a9ff80b36efb613396e9956f4c1e  t03-composition-cycle.md
56771927a22386766f4ed5bc55b1d78302d6030e2fb206be3cbf2cfcb1cd9bf5  t04-chain-only-head-ungrounded.md
1cf70bff52bbd478338bdee2037de1dc8fdecac0d2db73e04db4aa099fc51cd4  t05-selfaudit-overclaim-under-cycle.md
2c645182d70d9a4d1d31786c0439a9d9633312e1a65f1c735e8c9bc181c431e3  t06-hidden-cycle-past-head.md
05d5665c23fb5d416dd60f7708c443331ce484929554ff4f1f09b3c28a00f075  t07-non-sequitur-between-hops.md
38e44ca028a48753d303ac1d42f5087a10690360574d08fb648d1505e4f5fc17  t08-verdict-contradicts-its-type.md
87ce22ee4390727ba389ff521a7ec6f3a8c7a2edbcc55e1a3597d06a3be46f0b  t09-arithmetic-does-not-follow.md
ac6a733356a790816156d55a0515b8d0e1036e7d58adc437d4ba30f5069e7f9e  t11-fabricated-ground-truth.md
dc5ba58a4d1b43d471325b169849c011fcff257352fdbcc0e95b316ed4406e19  t12-inline-citation-wrong-chain.md
687959d6aba90e601d3c46b7e2e55d164751ac1d9fb64b42bf79ab2e2204b6b5  t13-grounded-alongside-cyclic-ref.md
1aa929a3bd3334b8e5ad38158b3343e2b3ab82b725cb0bfaeab7fcc6c606f4c8  t14-order-of-magnitude-conversion.md
```

All thirteen new hashes moved into `README.md`'s table in the same commit (`f0f7c31`) as
the marker edits, so FROZEN-EVIDENCE never observed an intermediate drift state.

## Verification performed after Task 3's commit (both branches' shared checklist)

- `bash scripts/check-firewall-battery.sh`: `FIREWALL: GREEN (25/25)` — TOTAL unchanged.
- `python3 scripts/report-conformance.py --check`: `PASS — no drift`.
- `git status --porcelain`: empty.
- `python3 scripts/check-quality-harness.py --self-test`: all three CONTRACT-06
  sub-checks (`chain_detector_pin`, `conclusion_claims_pin`, `slice_sections_pin`)
  PASSED; file byte-unchanged.
- `python3 scripts/check-conf-gate.py --self-test`: unaffected (not modified by this
  plan).

## Re-recorded D-06 exit counts (from `docs/data/conformance.json`, read fresh after the
Task 3 commit)

```
$ python3 -c "
import json
data = json.load(open('docs/data/conformance.json'))
rows = data['adversarial_corpus']['rows']
print('corpus items                                >= 12   actual:', len(rows))
print('corpus form-defect count across all items   == 0    actual:',
      sum(r['form_defects'] for r in rows if r['section_resolution'] == 'OK'))
print('missed/no-column-fired items w/ no disposition == 0 actual:',
      sum(1 for r in rows
          if (r['target_missed'] is True or r['no_column_fired'] is True)
          and (not r.get('disposition') or r['disposition'] == 'MISSING')))
"
corpus items                                >= 12   actual: 13
corpus form-defect count across all items   == 0    actual: 0
missed/no-column-fired items w/ no disposition == 0 actual: 0
```

All three counts are unchanged from `19-07-SUMMARY.md`'s recorded values (13, 0, 0) — the
marker branch's prose-only, whitespace-only-above-the-title edit moved no measured
reading, confirmed rather than assumed.

## Final published false-negative figure (verbatim, `docs/conformance-baseline.md`)

```
**False-negative rate:** 10 of 13 corpus items' catalogued falsehood the unmodified,
CONTRACT-06-frozen `detect_defects` did not catch -- despite every item being a stated,
catalogued falsehood. Each of those 10 is a false negative: a substantively wrong
analysis this instrument cannot distinguish from a sound one. Diagnostic: 9 of 13 items
had no substantive `detect_defects` column fire on them at all; the difference between
the two figures is exactly the items on which an unrelated column fired for a reason
having nothing to do with the item's own catalogued falsehood.
```

Per-stratum breakdown, verbatim:

```
- Stratum A: 2 of 5 catalogued target missed (1 of 5 no column fired)
- Stratum B1: 1 of 1 catalogued target missed (1 of 1 no column fired)
- Stratum B2: 7 of 7 catalogued target missed (7 of 7 no column fired)
```

Both readings unchanged from 19-08's regenerated headline — this plan's floors report on
the existing figures, they do not move them, and the marker branch is measurement-neutral
by proof (above), not by assumption.

## Assumption Drift (advisory)

**1. Task 3's acceptance criterion literally says "fifteen files"; the actual file list
in the same sentence is thirteen items + `README.md` = fourteen.** The plan's own action
text states: "Commit all fifteen files (thirteen items + `README.md`, and nothing else)
in ONE commit." 13 + 1 = 14, not 15 — the numeral and the enumeration it labels
contradict each other within the same sentence. Followed the explicit enumeration (13
items + README.md, nothing else) rather than the numeral, since `catalog.md` is expressly
excluded elsewhere in the same task ("`catalog.md`'s row must be unchanged (this branch
does not edit it)") and no other file is named anywhere in the branch's steps. `git show
--stat HEAD` on commit `f0f7c31` names exactly 14 files, matching the enumeration. This is
recorded as advisory drift, not a deviation requiring a fix, since acting on the literal
numeral would have required inventing a 15th file the plan never names.

## Deviations from Plan

### Auto-fixed Issues

None — no bug, missing-critical-functionality, or blocking-issue auto-fix was required
beyond the arithmetic-literal interpretation recorded above as assumption drift (a
plan-text reading choice, not a code defect).

## Issues Encountered

None. All four named neutralizations in Task 1 fired exactly as the plan specified, and
the add-marker branch's measurement-neutrality proof came back clean on the first attempt
across all thirteen items — no STOP-and-restore path was triggered.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- `scripts/report-conformance.py`'s CONF-08 disposition floor now has no structural blind
  spot over the catalogued-target join: a vacuity arm, a stratum-consistency check, and a
  symmetric caught-set lock all run in `cmd_check()`, censused and roster-locked.
- All thirteen adversarial-corpus items now self-identify as deliberately false content
  in-file, closing 19-REVIEW.md's CR-02 blocker with a human-made, dated, recorded
  decision rather than a planner default.
- Both of `19-VERIFICATION.md`'s remaining `missing` items and its one `human_verification`
  item are closed: the disposition floor's union scope is extended (not merely
  re-scoped), and the marker decision is made and recorded.
- Battery GREEN 25/25, TOTAL unchanged; `--check` PASS; all three CONTRACT-06 pins
  byte-unchanged; the phase's published false-negative figure (10 of 13) is unmoved by
  this plan's work.
- Rework count for this phase: this was the phase's SECOND gap-closure plan (19-CONTEXT.md's
  cap is 2) — the phase's gap-closure budget is now fully spent; any further gap found
  against Phase 19 requires a replan, per D-19-09-D.

---
*Phase: 19-false-negative-rate*
*Completed: 2026-09-05*

## Self-Check

- FOUND: `scripts/report-conformance.py` (modified, present)
- FOUND: `tests/adversarial-corpus-v9.0/README.md` (modified, present)
- FOUND: `tests/adversarial-corpus-v9.0/t01-ledger-arbitrary-chain.md` (modified, present)
- FOUND: `tests/adversarial-corpus-v9.0/t02-fabricated-read-at-source.md` (modified, present)
- FOUND: `tests/adversarial-corpus-v9.0/t03-composition-cycle.md` (modified, present)
- FOUND: `tests/adversarial-corpus-v9.0/t04-chain-only-head-ungrounded.md` (modified, present)
- FOUND: `tests/adversarial-corpus-v9.0/t05-selfaudit-overclaim-under-cycle.md` (modified, present)
- FOUND: `tests/adversarial-corpus-v9.0/t06-hidden-cycle-past-head.md` (modified, present)
- FOUND: `tests/adversarial-corpus-v9.0/t07-non-sequitur-between-hops.md` (modified, present)
- FOUND: `tests/adversarial-corpus-v9.0/t08-verdict-contradicts-its-type.md` (modified, present)
- FOUND: `tests/adversarial-corpus-v9.0/t09-arithmetic-does-not-follow.md` (modified, present)
- FOUND: `tests/adversarial-corpus-v9.0/t11-fabricated-ground-truth.md` (modified, present)
- FOUND: `tests/adversarial-corpus-v9.0/t12-inline-citation-wrong-chain.md` (modified, present)
- FOUND: `tests/adversarial-corpus-v9.0/t13-grounded-alongside-cyclic-ref.md` (modified, present)
- FOUND: `tests/adversarial-corpus-v9.0/t14-order-of-magnitude-conversion.md` (modified, present)
- FOUND: commit `10d6747` (Task 1)
- FOUND: commit `f0f7c31` (Task 3)

## Self-Check: PASSED
