# SCAN-GUARD: Self-audit scan structural gate: the Phase 15 self-audit scan prescription, its rubric verify block, and the Criterion-2-widened Verdict Block Format admission are present, correctly placed and internally coherent in the emitted tree, with one hundred clause-level named branches floored by an independent transcription (`_BRANCH_ROSTER_LOCK`).

<!-- GENERATED:FACTS -->
## Facts

- `branch_roster` (100): `B-01-slice-count`, `B-01-slice-noheading`, `B-02-lead-dup`, `B-02-lead-slice`, `B-02-lead-whole`, `B-03-placement-clean`, `B-03-placement-tail`, `B-04-heading-dup`, `B-04-heading-missing`, `B-05-cols-chain-dup`, `B-05-cols-chain-missing`, `B-06-cols-claim-dup`, `B-06-cols-claim-missing`, `B-07-rowrule-chain`, `B-07-rowrule-claim`, `B-08-rejected`, `B-09-cleanpass`, `B-10-ledger-indep-1`, `B-10-ledger-indep-2`, `B-11-recon-lead`, `B-11-recon-template`, `B-12-placement-1`, `B-12-placement-2`, `B-13-refix`, `B-14-bound`, `B-15-donotpresent-amended`, `B-15-donotpresent-dup`, `B-15-donotpresent-preamendment`, `B-16-coverage-bound-dup`, `B-16-coverage-bound-missing`, `B-17-validate-dup`, `B-17-validate-missing`, `B-17-validate-preamendment`, `R-01-block-dup`, `R-01-block-missing`, `R-01-no-mask`, `R-02-placement-aa`, `R-02-placement-anchor`, `R-02-placement-order`, `R-03-divlabour-1`, `R-03-divlabour-2`, `R-04-two-criteria`, `R-05-cols-chain`, `R-05-cols-claim`, `R-06-ledger`, `R-07-missing-absent`, `R-07-missing-neartwin`, `R-08-bound`, `R-09-crit4-count-dup`, `R-09-crit4-count-missing`, `R-09-crit4-direct-dup`, `R-09-crit4-direct-missing`, `R-09-crit4-order`, `R-10-crit6-count-dup`, `R-10-crit6-count-missing`, `R-10-crit6-direct-dup`, `R-10-crit6-direct-missing`, `R-10-crit6-order`, `R-11-bands-crit4-absent`, `R-11-bands-crit4-handwavy`, `R-11-bands-crit4-rigorous`, `R-11-bands-crit4-sound`, `R-11-bands-crit6-absent`, `R-11-bands-crit6-handwavy`, `R-11-bands-crit6-rigorous`, `R-11-bands-crit6-sound`, `R-12-halt-dup`, `R-12-halt-missing`, `R-13-format-admission-c2-dup`, `R-13-format-admission-c2-missing`, `R-13-format-admission-c46-dup`, `R-13-format-admission-c46-missing`, `R-13-format-admission-dup`, `R-13-format-admission-missing`, `R-13-format-admission-superseded`, `R-13-format-amended-dup`, `R-13-format-amended-missing`, `R-13-format-order`, `R-13-format-preamendment`, `R-13-format-quoted-span-superseded`, `R-13-format-template-c2-dup`, `R-13-format-template-c2-missing`, `R-13-format-template-c46-dup`, `R-13-format-template-c46-missing`, `R-14-c2-descriptor-dup`, `R-14-c2-descriptor-missing`, `X-01-cols-chain-body`, `X-01-cols-chain-rubric`, `X-01-cols-claim-body`, `X-01-cols-claim-rubric`, `X-02-heading-body`, `X-02-heading-rubric`, `X-03-bound-body`, `X-03-bound-rubric`, `X-04-admission-c2-body`, `X-04-admission-c2-rubric`, `X-04-admission-c46-body`, `X-04-admission-c46-rubric`, `X-05-superseded-body`, `X-05-superseded-rubric`
- `branch_count`: `100`
- `registered_surfaces` (2): `first-principles/agents/first-principles.md`, `first-principles/agents/references/validation-rubric.md`
- `call_site_census` (4 entries): `_check_body_text`=1, `_check_cross_surface`=1, `_check_rubric_text`=1, `_live_exit_code`=1
- `control_ids` (12): `roster-census`, `roster-lock`, `roster-entry-source`, `roster-es-census`, `validate-census`, `live-census`, `dispatch`, `live-dispatch`, `live-dispatch-census`, `describe`, `roster-floor-missing`, `roster-floor-extra`
- `control_count`: `12`
- `locked_constants` (1 entries): `band_bullets`='- **Rigorous** | - **Sound** | - **Hand-wavy** | - **Absent**'
<!-- END GENERATED:FACTS -->

<!-- GENERATED:HOW-TO-RUN -->
## How to run

```sh
python3 scripts/check-selfaudit-scan.py --self-test && python3 scripts/check-selfaudit-scan.py
```

CI job: `check-selfaudit-scan`
<!-- END GENERATED:HOW-TO-RUN -->

<!-- HAND-WRITTEN: preserved verbatim across regeneration. -->

## What it asserts

Registered — CI job `check-selfaudit-scan (SCAN-GUARD)` plus battery registration, both running
`--self-test` **and** the live leg against the shipped `AGENT_FILE`/`RUBRIC_FILE`, matching
REG-GUARD's shape (and PROV-GUARD's, until v9.4.0 Phase 40) (plan 15-09, closing
`15-VERIFICATION.md` gap 2's WR-05 finding); the
battery tally is unchanged because `gate()` increments its total once per gate id regardless of how
many commands run under it. Asserts the Phase 15 self-audit scan prescription (agent body) and the
`**Self-audit scan (verify before scoring)**` block plus the Criterion 4 / Criterion 6 quote-source
sentences (rubric reference) are present, correctly placed and internally coherent in the
**emitted** tree. Carries one hundred clause-level named branches (plan 15-06 split thirty-one
check-level branches to fifty-eight clause-level ids — every `!= 1` count guard now has a MISSING
and a DUPLICATE arm, every multi-literal tuple has one arm per literal, and every cross-surface arm
is split by surface; plan 15-07 added fourteen more, 58 to 72, closing CR-02/CR-03: the amended
Verdict Block Format's admission of the self-audit scan for Criteria 4 and 6 only (`Rubric-13`, six
branches — the amended template, the admission sentence, the pre-amendment template's absence, and
their ordering), the direct-quotation half of each of Criterion 4's and Criterion 6's quoted-span
instructions for the band-determining limbs neither scan table carries a column for
(`Rubric-9`/`Rubric-10`, four branches), the shared table-coverage-bound sentence inside the agent
body's scan prescription (`Body-16`, two branches), and that same sentence's cross-surface presence
(`Cross-3`, two branches); plan 15-08 added fourteen more, 72 to 86, widening the Verdict Block
Format admission to cover Criterion 2's Assumption Audit artifact alongside Criteria 4/6 —
Rubric-13's per-clause count guards (the Criteria-4/6 half, the Criterion-2 half, each missing+dup)
plus a whole-file count-0 guard on the superseded pre-15-08 clause, a new Rubric-14 pinning
Criterion 2's Assumption-Audit-artifact descriptor sentence, a new Body-17 pinning the amended
agent-body Validate step (and the pre-amendment restriction's absence), and Cross-4's four
single-surface arms asserting both admission clauses on both surfaces; plan 15-09 added one more,
eighty-six to eighty-seven, `R-02-placement-aa`, closing the fail-open where Rubric-2's combined
placement predicate (`aa_idx < scan_idx < precedence_idx`) had only its Precedence half controlled —
a scan block relocated BEFORE the Assumption Audit block previously passed `--self-test` undetected;
the predicate is now split into two independently falsifiable per-half guards); plan 15-11 added
seven more, eighty-seven to ninety-four, region-splitting `Rubric-13`'s clause guards so the
quoted-span TEMPLATE and the admission paragraph are each independently required to state both
admitted-artifact clauses (`R-13-format-template-c46-missing`/`-dup`,
`R-13-format-template-c2-missing`/`-dup`, `R-13-format-quoted-span-superseded`, and `Cross-5`'s two
per-surface arms) — closing the gate-locked contradiction the pre-15-11 template shipped with: the
TEMPLATE pinned the narrow "Criteria 4 and 6 only" wording at exactly-once while the admission
paragraph two lines below it already admitted Criterion 2, so `Rubric-13` REJECTED the correct fix
until the template itself was widened to name both admitted artifacts (`15-VERIFICATION.md`'s
SCAN-02 gap); plan 15-12 added six more, ninety-four to one hundred, replacing `Rubric-11`'s two
hand-written `_BAND_SOUND`-only ids with eight ids parameterized over every `_BAND_BULLETS` literal
(`R-11-bands-{crit4,crit6}-{rigorous,sound,handwavy,absent}`), closing the fail-open where narrowing
`_BAND_BULLETS` to one literal left `--self-test` at rc 0 reporting full coverage — each with its
own per-source negative control and an anti-masking assertion derived from the branch set; the
registry itself is floored by equality against a second, independently transcribed roster
(`_BRANCH_ROSTER_LOCK`), so narrowing `REQUIRED_BRANCHES` fails `--self-test` by name rather than
silently shrinking coverage (plan 15-05, closing WR-02). Every ordering lookup (Body-3, Rubric-2,
Rubric-9, Rubric-10, Rubric-13) resolves through a shared normalized-index helper (`_find_flat`) and
fails closed on a not-found anchor, closing the CR-01 defect where a hard-wrapped-and-relocated
sentence passed with no signal. Rubric-1's early return no longer masks the Criterion 4/6 findings
(WR-10: a duplicated scan-block heading and a stripped Criterion 4 quoted-span sentence now both
surface in one run, control `R-01-no-mask`), and Rubric-4's information-free two-criteria name loop
(WR-09, confirmed uncontrollable since three sibling sentences already name both criteria) was
deleted rather than kept as an unfalsifiable arm. The live CLI leg (`_validate_files`) is floored by
a source-text call-site census over its four legs (`_check_body_text`, `_check_rubric_text`,
`_check_cross_surface`, `_live_exit_code`) plus a pure `_live_exit_code(failures)` helper with two
synthetic isolation arms and an in-process dispatch control driving `main([])` — every census counts
source text and observes no behaviour, so each catches DELETION of a real call, not a call whose
returned result is discarded (plan 15-09). `

## Residuals and open items

15-REVIEW.md` (measured 2026-09-04 against the pre-15-08 tree) re-ran the prior gap-closure census
of 22 targeted neutralizations: 16 of them (`m1`-`m5`, `m7`-`m12` and `m17`-`m21`) failed
`--self-test` as expected — the arithmetic total of that enumeration, not the "20" an earlier
version of this row stated; `m6`'s target (Rubric-4's information-free name loop) had been deleted
rather than controlled, so it could not be applied at all; `m22` (the live leg's
`_check_cross_surface` wiring into `_validate_files` going unfloored) was open at that review and is
now closed by plan 15-09's `validate-census`; `m13`-`m16` (Rubric-11's C6 loop, Body-15's
pre-amendment arm, Rubric-7's near-twin arm and Rubric-12's halt count, each already controlled
before that census ran) were re-applied against the current tree in plan 15-13 and remain CAUGHT,
with no regression. **Coverage claim, narrowed to what is measured** (`15-REVIEW.md` WR-03):
clause-level ids cover every `!= N` count guard, every multi-literal tuple and every cross-surface
arm — not, as an earlier version of this row claimed, "one id per independently neutralizable
assertion arm"; plan 15-12's own full census of every multi-literal construct in the file found
nine and confirmed the claim held for the whole file, disclosing no exception. Plan 22-05
re-derived that census by direct enumeration against the live file and superseded it: eleven
multi-literal constructs, ten of which each carry a hand-written arm per literal, with
`_VALIDATE_LEG_SYMBOLS` the one NAMED EXCEPTION — a four-literal tuple driving the validate-census
check through a single aggregate pass/fail message with no per-leg id and no membership lock,
disclosed rather than closed under the depth rule (`docs/PROCESS.md` §1), because adding the
missing lock or a per-leg arm to make the claim true of all eleven would be the LEVEL move the
rule stops. Not-found reporting arms across `_check_body_text` and `_check_rubric_text` were
re-censused by plan 22-06 through per-site neutralization on disposable scratch copies, superseding
this row's prior WR-03-scoped eight-arm figure: of a nineteen-arm roster, CONTROLLED are three (one
via `R-02-placement-anchor`'s own branch id, two — Body-1's and Rubric-3..8's slice guards — via an
uncaught crash rather than a named check), SIBLING-ONLY are zero, and UNCONTROLLED are sixteen —
three plus zero plus sixteen sums to the full nineteen-arm roster. The sixteen-arm UNCONTROLLED
residual, including the four sites a backlog review (999.31 item 4) named as never independently
neutralized, is a published measured limitation, disclosed rather than closed under the depth rule
(`docs/PROCESS.md` §1) rather than fixed.

## Disclosed bounds

**Does not assert** that a scan row's content is correct, and does not assert a live run complied
with the prescription (999.12/999.13 own that layer); does not assert that the widened Verdict Block
Format admission's three-artifact enumeration (plan 15-08) or the enumerated band-determining limbs
neither scan table covers are the COMPLETE set against every future descriptor edit — both are
semantic properties of the descriptor prose no mechanical check reads, guarded only procedurally
(the gate docstring's disclosed bounds); `15-REVIEW.md` WR-01 — three further band-determining limbs
(a chain lacking a genuine intermediate step, a conclusion with more than one derivation chain, a
Conclusion claim inconsistent with its section-4 chains) with no column in either scan table and no
quoting rule under either half of the instruction — remains open and is not closed by plan 15-10;
SCAN-03's "skill-stub surfaces" wording is a recorded deviation because no focused-mode stub carries
Criterion 4 or 6 at all (`shared/spine/focused-validation-step.md` disclaims the six-criterion
gate), with backlog 999.16 left open; and the SCAN-04 emission-cost character figure (2,288 vs. an
independent 1,381 reconstruction) is disclosed as unfalsifiable rather than settled — see the gate's
own docstring for the full residual ledger. WR-04 (the roster floor's `covered` argument aliasable
to `REQUIRED_BRANCHES`, making the surplus check structurally incapable of failing) is now closed by
plan 15-12's ENTRY-SOURCE LOCK: it proves the real `_roster_problems(...)` call's own
argument-triple text matches the expected literal, whitespace-normalized — it does NOT observe
behaviour (it catches an argument triple that was rewritten, not a floor whose returned problems are
discarded before reaching `problems`), and an argument rebound to an expression of equal value is
invisible to it by construction. IN-04 and IN-05 stay open and stay named.
