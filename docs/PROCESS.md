# Process Contract

**Milestone:** v9.0.0 Conformance (Phase 22)
**Recorded:** 2026-09-08
**Status:** Standing governing record. Inherited by every future milestone — no expiry, no
v9.0.0-only scoping.

> **Standing — this is the project's single canonical statement of its own stopping rule.**
> `CLAUDE.md` and `CONTRIBUTING.md` each carry one sentence naming the depth rule plus a link to
> this page — they do not restate it. Cite `docs/PROCESS.md`; do not re-explain its rules on a
> second surface. Hand-transcribed dual-surface claims are this project's dominant defect class,
> measured at 41% of all review findings across Phases 13-15, and this page exists so Phase 22
> does not manufacture a fresh instance of the exact defect it is closing.

## 1. The depth rule

**a guard guards the product; a guard is not itself guarded**

This exact sentence, with this exact punctuation, is the rule. Do not paraphrase it, do not
change the semicolon, do not capitalise it.

The measured justification is the chain `999.27 → 999.28 → 999.30`. Phase 15's SCAN-GUARD gate
was built to catch a specific class of defect — a published claim about test coverage that the
tests themselves do not honour. Guarding SCAN-GUARD's own correctness turned out to reproduce the
identical defect class one level up, three times in a row:

- **999.27** — SCAN-GUARD's live leg could be reduced to an unconditional PASS: neutralising
  `if failures:` to `if False:` in `_validate_files` left `python3 scripts/check-selfaudit-scan.py`
  exiting 0 and the whole battery reporting green, because nothing controlled the live leg's own
  reporting path. Closed by plan 15-09, which added an anti-vacuity control on the live leg itself
  — the GATE-01 `_assert_live_coverage` precedent, mutating the surface the run actually read.
- **999.28** — the successor hole, inside SCAN-GUARD's own anti-masking floor: `_BAND_BULLETS`
  was narrowable from four literals to one with `--self-test` still reporting full coverage, and
  the roster floor's `covered` argument had no lock against its own required set, making the
  surplus check structurally incapable of failing. Closed by plans 15-12 and 15-13, which added a
  second, independently transcribed roster and an ENTRY-SOURCE LOCK.
- **999.30** — the successor to *that*, one level further removed: `_validate_leg_symbols` was
  itself an unlocked registry inside the anti-masking floor it patrols, and the ENTRY-SOURCE LOCK
  plan 15-12 had just added was itself unanchored and unfloored — the identical shape, still open
  when this phase began.

Three consecutive rounds, each closing the specifically-reproduced mutation while a structurally
identical hole one level removed stayed open. 999.30's terminal disposition under this rule is
**closed-by-decision**: the pattern, not the individual instance, is the finding, and this rule is
what that finding argues for. The entry is this rule's own worked justification for not chasing
the regress a fourth time.

### 1.1 REACH is not LEVEL

**REACH** — pointing an existing product-guard at another product surface is L1 work, always
allowed. **LEVEL** — adding a guard whose subject is another guard's own correctness stops at L3.

The distinction is load-bearing. Without it, "a guard is not itself guarded" degrades into "never
touch `scripts/`" and freezes legitimate coverage work — CONF-13's literal scanner, HARN-01
through HARN-03, PROV-GUARD and REG-GUARD are all guards implemented under `scripts/`, and a rule
that forbade touching that directory at all would freeze the exact coverage work Phase 21 did.

This phase's own REACH move: registering `docs/PROCESS.md` and `CONTRIBUTING.md` in CONF-13's
scanned Markdown population (the widening plan 22-07 performs) points an existing product-guard
— CONF-13, which already scans Markdown surfaces for unattributed literals — at two product
surfaces it did not previously reach. It does not add a guard whose subject is another guard's own
correctness, so it is REACH, not LEVEL.

The in-repo precedent for this exact argument already exists: `_py_docstring_scan_scripts()`'s own
docstring (`scripts/gen-gate-docs.py`) explains why CONF-13's `.py` population was widened from the
narrower `_expected_harvest_scripts()` registry set to every `.py` file directly under `scripts/`
— the narrower set made `scripts/_gate_registry.py`, the module that *defines* those entries,
structurally unable to ever be one of its own scanned surfaces. That widening pointed an existing
detector at more of the product surface it already claimed to cover; it did not build a second
detector to check the first one's correctness. This phase's widening is the same move.

### 1.2 The rule's own worked example: CR-05

CONF-13's non-exempt-literal zero (reached in Phase 21) was reached partly by deleting 17 true,
permanently-stable historical measurements from `docs/README.md` and substituting unfalsifiable
hedges — "several," "a handful," "many" — in their place, including one that is a gating
criterion on opening any post-v8.11 milestone, not narrative colour (the "about five live
entries" to "several more live entries" edit, in `docs/README.md`'s Post-v8.11 gate paragraph).

The generalisation this argues for, stated plainly: **a guard that is itself scored creates
pressure to make the product less falsifiable in order to satisfy it.** CONF-13 was not gamed by
adding a false claim — it was gamed by deleting true, checkable ones and writing something no
scanner can dispute in their place. That is the argument for the depth rule, in this project's own
measured terms, not an abstraction borrowed from elsewhere.

The count is 17, not the 16 the origin review stated, and the correction is itself the discipline
being described: three adjustments, in both directions. One of the review's 16 rows —
`docs/gates/TRACE-03.md`'s "across several lines" — is not a `docs/README.md` row and is out of
this paragraph's stated scope; it remains un-restored, and its stated "before" text does not
appear anywhere in git history, so this section does not present CR-05 as fully closed. The
review's own table also collapsed two textually distinct `docs/README.md` edits — "about five
live entries" was hedged twice in the same paragraph — into a single row, and omitted a further
deletion ("while 16 gates stayed green" hedged to "while the whole battery stayed green"). 16 − 1
+ 1 + 1 = 17. Getting a count of deleted falsifiable claims wrong by under-counting is the same
failure mode one level removed.

Plan 22-04 restores 16 of the 17 rows verbatim. Row 17 — `docs/README.md`'s TESTING.md nav cell —
is deliberately NOT a verbatim restore: the pre-hedge text stated a pre-commit gate count that
CONF-SURFACE (plan 21-11) made false, so the live count was written instead of the original. That
single judgement call is recorded per-entry in `scripts/gen-gate-docs.py`'s ledger under the key
`('docs/README.md', 'gate and the five')`, adjudicated NOT-A-RESTORE.

## 2. Product and apparatus

The cut is by **claim-audience**, not by directory and not by subject.

**Product** = anything asserting a fact to a reader outside the build loop: the shipped plugin
(`shared/`, `first-principles/`), `docs/`, `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, and
`CLAUDE.md`'s prose. **Apparatus** = the machinery that verifies claims: `scripts/`, `.github/`,
gate `--self-test` suites, `.planning/`.

The consequence: **Product findings block the phase.** Apparatus findings auto-file to backlog
and never block.

Two other cuts were considered and rejected. A **path-glob cut** (`shared/` and
`first-principles/` only) would have made all six of Phase 21's carried findings apparatus,
including CR-05's honesty regression — reading as an amnesty for the exact defect class that
caused four gap-closure rounds. A cut drawn by **"what a gate can see"** would require re-arguing
the boundary every time a new gate's reach changed, rather than applying one rule.

**Corollary:** tier follows audience, and findings split per item — one backlog entry may carry
two tiers. A false sentence in `CLAUDE.md` is a product defect regardless of whether its *subject*
is the apparatus, because the reader cannot audit it either way.

**Standing constraint for this whole file, and for any product surface stating a count over the
gate battery:** any mention of the number of gates the battery runs must point at the generated
fact — `CLAUDE.md`'s generated CI-gate table and its population-arithmetic sentence — rather than
state a bare digit. That total is not frozen; it has moved from 15 to its current value over the
project's history, and hardcoding it here would manufacture exactly the stale-count defect this
page exists to name. [COMPONENT-DIAGRAM.md](COMPONENT-DIAGRAM.md) already makes this move for the
same reason — pointing at the generated source instead of a bare, driftable digit — and
[ARCHITECTURE.md](ARCHITECTURE.md) carries the full CI-gate table this page's own claim about
"the battery" ultimately resolves to.

Frozen historical counts — "13 plans," "4 rounds," "41%," "17 figures" — are different in kind
from a moving total: they describe a specific, closed, immutable past state and will never change.
They are stated in this file as literals and attributed by ledger entry (plan 22-07, per this
phase's own D-22-A), never by a catch-all exemption. A moving count is never stated as a literal
at all.

## 3. The rework cap

Two limits, because Phase 21 recorded two distinct failure modes:

1. **Cap = 2 gap-closure ROUNDS.** A round is one verification → plan → execute cycle. A round
   may contain N plans provided each closes an independently-verified gap.
2. **Same-class trip** — a finding of a defect class already closed in this phase halts
   immediately and forces a replan at the root, regardless of round count. Applied retroactively
   to Phase 21: round 2 would have tripped this same-class rule and halted then.

The measured evidence, from Phase 21: **13 gap-closure plans across 4 rounds against a stated cap
of 2.** Each round closed the specifically-flagged instance while a structurally identical
instance of the same class appeared elsewhere. Applying the rule retroactively: round 1 (4 plans,
3 distinct independently-verified gaps) would be allowed under limit 1; round 2 would trip limit 2
and halt. The actual outcome was 4 rounds and 13 plans, with the class still recurring at close.

**Deviation from the wording in plans, stated explicitly, not applied silently.** `REQUIREMENTS.md`
CONF-15 and ROADMAP criterion 4 both state the cap as *"more than 2 gap-closure plans halts the
phase and forces a replan."* This page changes the unit from **plans** to **rounds**. Reason: a
per-phase plan *count* cannot distinguish round 1 of a genuine three-gap closure from round 4 of
point-fixing, and it did not fire at all when round 2 breached it silently — nothing outside the
exception record itself checked that the record existed. Neither `REQUIREMENTS.md` nor
`ROADMAP.md` is rewritten by this change; this page is the record.

### 3.1 Recorded exceptions (append-only)

An exception to the cap is taken by explicit developer decision, in writing, in this table, in
the same diff as the plans it authorises.

**Why the ledger moved here, per the measured cause of the round-2 breach:** `*-CONTEXT.md` files
are not git-tracked (`*-SUMMARY.md` files are force-tracked; `*-CONTEXT.md` is not), so Phase 21's
exception record lived where no gate, no CI job and no diff review could see it — which is how
round 2 breached the cap with no record written at the time. A tracked, public, CONF-13-scanned
surface makes enforcement ordinary code review: plans landing with no matching ledger row in the
same diff are visible in the diff.

A mechanical checker over `.planning/` was considered and rejected: `.planning/` is gitignored so
it can never run in CI, it would guard the process rather than the product, and it would be a new
guard in the phase that caps guards.

| Phase | Date | Rounds | Plans | Reason |
|---|---|---|---|---|
| Phase 21 | 2026-09-07 | round 1 | 21-13..21-16 (4) | Three blocking must-have failures sharing one root cause — a gate reporting GREEN while the claim it publishes is false — with zero gap-closure plans spent before this round. The alternatives were shipping known-wrong published claims or a Phase 21.1 rename that would honour the rule only by resetting its counter. |
| Phase 21 | 2026-09-07 | rounds 2 and 3 | 21-17..21-23 (7; running total 11) | Round 2's four plans closed three independently-verified blocking gaps, but **round 2 was executed with no exception recorded at the time — a fact discovered by the round-2 verifier, not self-reported.** Round 3 grew from two plans to three when plan-checking found a live twin of the same defect one requirement over. |
| Phase 21 | 2026-09-08 | round 4 | 21-24, 21-25 (2; running total 13) | The fourth consecutive round in which closing a flagged instance left or produced a new instance of the same class. Two plans, because the remediation had to land and commit before the census was widened to detect it, or every commit in the repo would block mid-execution. |

**Round 1, in full.** `21-VERIFICATION.md` failed 3 of 4 must-haves, all blocking: CONF-13's
standing scanner could not fail on `CLAUDE.md`, `docs/ARCHITECTURE.md` or `docs/TESTING.md` (a
whole-surface relpath permit; a live-wrong literal was detected then dropped); CONF-11's
`--describe` emissions were not derived from live constants on at least two scripts, with the
wrong figures already rendered onto the generated surface; CONF-12's generated `CLAUDE.md`
contradicted hand-written `CLAUDE.md` seventeen lines below it. The planner judged the set
uncompressible to 2 plans without dropping scope, and the plan-checker independently confirmed all
three gaps close if the four plans execute as written (32 falsification arms, no criterion
reducing to "the battery is green"). The cap's purpose is to stop endless point-fixing rounds;
Phase 21 had spent zero gap-closure plans before this round, so it was round 1 addressing three
blocking gaps sharing one root cause, not a fourth round of patches. The cap was NOT amended — it
stood at 2 for every other phase in the milestone, and Phase 19's own "cap of 2 now spent"
accounting was unaffected. This was a single named exception, not a new rule.

**Rounds 2 and 3, in full.** Round 2 was plans 21-17..21-20, four gap-closure plans against
`21-VERIFICATION.md` round 1's three blocking gaps, executed with **no exception recorded at the
time** — a fact discovered by the round-2 verifier, not self-reported. Round 3 was plans 21-21,
21-22 and 21-23: two against the single blocking gap the round-2 closure apparatus itself opened,
and a third added at plan-checking time when the same structural defect was found live one
requirement over — `_py_docstring_scan_scripts()` derived CONF-13's literal-scan population from
the identical set that caused the round-1 defect, so the same seven `.py` files were invisible to
CONF-13's standing scanner too. Running total: 4 (round 1) + 4 (round 2) + 3 (round 3) = 11
gap-closure plans against a stated cap of 2. The omission in round 2 was of the *record*, not of
the deliberation — round 2's four plans closed three independently-verified blocking gaps and were
confirmed to have genuinely closed them — and an undocumented breach is worse than a documented
one precisely because it cannot be reviewed. The cap was NOT amended. A cap exceeded without
halting the phase is evidence about the cap's own design: a cap stated as a per-phase plan count
cannot tell round 1 of a genuine multi-gap closure from round 4 of point-fixing, and it did not
fire at all when round 2 breached it, because nothing mechanically checked that the exception
record existed.

**Round 4, in full.** Round 4 was plans 21-24 and 21-25, against `21-VERIFICATION.md` round 3's
single blocking gap: a generated gate-documentation page published a universal about a census's
reach that was false against files inside the census's own population. Running total: 4 + 4 + 3 +
2 = 13 gap-closure plans against a stated cap of 2. This was the fourth consecutive round in which
closing a specifically-flagged instance of "a published claim that does not match what the code
verifies" left, or produced, a new instance of the same class — not a fourth round of point-fixing
but the first round to attack the recurrence itself, by binding the published claim to the live
roster it describes with an equality floor and an over-claim falsification arm. The cap was NOT
amended. A cap exceeded four times in one phase, with the fourth exception written by the same
process that failed to write the second one at the time, is evidence about the cap's design —
carried forward here rather than softened. This recurrence pattern — four rounds, same defect
class, a new location each time — is the concrete case against a cap stated as a per-phase plan
count, and it is this page's own reason for changing the unit to rounds.

Rows in this ledger are **appended, never edited and never removed.** A superseded row is
annotated in place, not deleted.

The cap's own standing is unchanged by any exception recorded here: it stands at **2 rounds** for
every phase.

