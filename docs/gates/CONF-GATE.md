# CONF-GATE: Standing exemplar-conformance comparator: the four conformance counts on both gated example surfaces against source-literal targets, a 14-entry claim floor locked by equality to the live-discovered `shared-examples` ids, the D-03 prescribed-lead-in rule, and the marked-claim ratchet (may fall, never rise).

<!-- GENERATED:FACTS -->
## Facts

- `registered_surfaces` (2): `shared-examples`, `generated-twin`
- `population_floors` (2 entries): `heading_chain_blocks`=31, `verdict_cells`=77
- `call_site_census` (7 entries): `_claim_floor_problems`=1, `_claim_floor_roster_problems`=1, `_d03_rule_problems_from_text`=1, `_population_floor_problems`=1, `_ratchet_problems`=1, `_run_d08_arm`=1, `_targets_problems`=1
- `control_ids` (44): `target-unreadable-fires`, `target-unreadable-passes-at-zero`, `target-heading-malformed-fires`, `target-nonconforming-verdict-fires`, `target-silent-untraced-fires`, `targets-pass-on-generated-twin-too`, `target-fires-on-generated-twin`, `d07-missing-named`, `d07-extra-named`, `d07-roster-arm-shape-guard`, `d07-equal-passes`, `d04-floor-fires`, `d04-floor-passes-at-floor`, `population-floor-passes-at-floor`, `population-floor-fires`, `population-floor-values-locked`, `target-heading-malformed-counted-when-unreadable`, `claim-floor-values-locked`, `d03-leadin-set-locked`, `d03-fires-on-leadin-recommended-approach`, `d03-fires-on-leadin-key-insight`, `d03-fires-on-leadin-trade-offs-acknowledged`, `d03-passes-on-nonprescribed-leadin`, `d03-passes-on-unmarked-prescribed-leadin`, `ratchet-fires-above`, `ratchet-passes-at-pin`, `ratchet-passes-below`, `ratchet-value-locked`, `ratchet-fires-across-both-surfaces`, `contract-surface-excluded`, `live-call-site-census`, `live-call-form-lock`, `census-x1-clean`, `census-x2-missing`, `census-x3-duplicated`, `form-lock-x1-clean`, `form-lock-x2-rewritten`, `census-x4-commented`, `live-call-site-roster-locked`, `d08-missing-target-row-reported`, `d08-missing-sites-reported`, `d08-increments-not-produced-reported`, `d08-needle-not-unique-reported`, `describe`
- `control_count`: `44`
- `locked_constants` (2 entries): `marked_claim_ratchet`=4, `prescribed_lead_ins`='**Recommended approach:** | **Key insight:** | **Trade-offs acknowledged:**'
<!-- END GENERATED:FACTS -->

<!-- GENERATED:HOW-TO-RUN -->
## How to run

```sh
python3 scripts/check-conf-gate.py --self-test && python3 scripts/check-conf-gate.py
```

CI job: `check-conf-gate`
<!-- END GENERATED:HOW-TO-RUN -->

<!-- HAND-WRITTEN: preserved verbatim across regeneration. -->

## What it asserts

Registered — CI job `check-conf-gate (CONF-GATE)` plus battery registration, both running
`--self-test` **and** the live leg, matching SCAN-GUARD's shape (and PROV-GUARD's, until v9.4.0
Phase 40). Measures the
fourteen shipped worked examples through `report-conformance.py`'s discovery/measurement surface and
asserts the four conformance counts (`unreadable`, `heading_malformed_blocks`,
`nonconforming_verdict_cells`, `silent_untraced_claims`) are zero on both gated surfaces
(`shared-examples`, `generated-twin`) against source-literal targets — never against the regenerated
baseline — with the D-03 prescribed-lead-in rule, a 14-entry claim floor locked by equality to the
live-discovered `shared-examples` ids (D-07), and the marked-claim ratchet (may fall, never rise) —
corpus-wide over both gated surfaces and pinned at 4, matching `docs/conformance-baseline.md`'s
published figure. Backed by a D-08 live anti-vacuity arm (three in-memory mutations of
`personal-general.md`, each confirmed to increment its target count by exactly 1), a source-text
call-site census plus call-form lock over `run_live()`'s seven enforcement call sites (plan 18-09,
closing the 18-VERIFICATION.md blocking gap where a one-line deletion left both `--self-test` and
the live leg reporting PASS; plan 18-12 adds `_population_floor_problems` as the seventh), a
42-control offline `--self-test` floored by equality against a second, independently transcribed
control-id lock, the census reading `run_live()`'s source with `#` line comments STRIPPED so a
commented-out enforcement call is caught (plan 18-11, BL-01), both census tables floored by set
equality against `_LIVE_CALL_SITES_LOCK`, a second independent transcription, so narrowing either
fails by name (plan 18-11, BL-02), per-surface DENOMINATOR floors (`_POPULATION_FLOORS`) over the
two previously numerator-only zero targets (`nonconforming_verdict_cells`,
`heading_malformed_blocks`) so a zero achieved by deleting the measured population fails (plan
18-12, BL-03), and the D-08 live anti-vacuity arm returning problems instead of exiting, with
offline controls over each of its four internal predicates (plan 18-13, BL-04/WR-06).

## Disclosed bounds

**What it does not assert:** citation correctness (backlog 999.4); `heading_malformed_blocks == 0`
is conformance under this detector's measured reach, not a claim that no R7 violation remains
anywhere in the corpus; the population floors detect population SHRINKAGE below a pinned figure, not
substitution; the D-08 controls prove the arm reports and each internal predicate is falsifiable,
not that the three mutations are meaningful against the real corpus; and, in the same voice
QUAL-01's and SCAN-GUARD's own censuses carry, the call-site census and call-form lock — now
including the commented-out case, which plan 18-11 moved onto the CAUGHT side — catch a deleted,
commented-out, or rewritten enforcement call site, not a call whose returned problems are computed
and then discarded.
