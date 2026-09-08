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
being described: the review's own table collapsed two textually distinct edits — "about five live
entries" was hedged twice in the same paragraph — into a single row, and omitted a further
deletion ("while 16 gates stayed green" hedged to "while the whole battery stayed green"). Getting
a count of deleted falsifiable claims wrong by under-counting is the same failure mode one level
removed. Plan 22-04 restores all 17 rows verbatim.

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

