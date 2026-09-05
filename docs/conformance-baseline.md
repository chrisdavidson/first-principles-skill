<!-- GENERATED — DO NOT EDIT -->
<!-- Source: scripts/report-conformance.py -->
<!-- Regenerate: python3 scripts/report-conformance.py -->

# Conformance Baseline

Measurement date: 2026-09-05

This file is a measurement, not a contract: no figure below defines what the codebase is required to become, and no count in it gates a conformance check. Regenerating this file only ever fails on staleness -- committed bytes that no longer match a fresh run of `scripts/report-conformance.py` -- never on a count read here being high.

## Headline

| Reading | shared-examples | generated-twin | contract-surface |
|---|---|---|---|
| Files unreadable by `_slice_sections` | 3 of 14 | 3 of 14 | 0 of 1 |
| §6 conclusion claims (untraced) | 60 (58 untraced) | 60 (58 untraced) | 3 (3 untraced) |
| §6 untraced claims (marked / silent) | 58 untraced (0 marked, 58 silent) | 58 untraced (0 marked, 58 silent) | 3 untraced (0 marked, 3 silent) |
| §2 verdict cells (non-conforming) | 77 (69 non-conforming) | 77 (69 non-conforming) | 1 (1 non-conforming) |
| §4 `chain_blocks` (malformed) | 28 (19 malformed) | 28 (19 malformed) | 3 (1 malformed) |
| `### Conclusion` heading-swept blocks (malformed) | 28 (19 malformed) | 28 (19 malformed) | 1 (0 malformed) |
| Source-vs-twin agreement (D-04) | 14 of 14 pairs agree | | |

## Two chain-block censuses (D-05)

`detect_defects` and the `### Conclusion` heading sweep are both produced by the same frozen instrument, `scripts/check-quality-harness.py`, yet they read a different number of chain blocks. `detect_defects`'s §4-scoped `chain_blocks` / `malformed_chain_blocks` columns come from a section slice, so they cannot read the files `_slice_sections` rejects. The `### Conclusion` heading sweep -- `_render_example_chain_blocks` paired with `_chain_block_well_formed` -- is a heading scan, not a section parse, so it can read those same files. The two figures measure different things and are published as separately named columns rather than reconciled into one number.

## Column vocabulary

Three kinds of value appear in the per-artifact tables below. A number means the detector read the document and counted. The literal `n/a` means no `.jsonl` generation capture exists for this artifact -- true of all 29 artifacts, for the nine provenance columns, unconditionally. The literal `unreadable` means `_slice_sections` rejected the document, so the twelve measured schema fields were never computed. The nine provenance columns are emitted in full precisely so `n/a` and `0` are never printed as the same thing.

## Disclosed bounds

This phase publishes four disclosures in the same voice R7/R9/R10 use on the agent surface to state their own measured bounds, rather than leaving them to be discovered.

**1. Chain-form reach.** `heading_malformed_blocks == 0` means every scanned block conforms under `_chain_block_well_formed`'s measured reach -- the head and first hop, up to the second arrow of the first matching candidate. This is NOT the same claim as "no R7 violations remain in `shared/examples/`": a wrap or a GT-led hop after the second arrow is not detected. This phase fixes to the detector's bound, which is what CONF-04 states; fixing to R7 as published is a strictly larger job and is recorded as backlog, not as done.

**2. Marked-claim residual (derived).** 0 claim(s) across shared-examples and generated-twin carry the `no chain — flagged assumption only` marker (shared-examples: 0, generated-twin: 0), computed from `rows` at render time, never hardcoded. A marked caveat still scores untraced BY DESIGN (`R-CLAIM-CAVEAT-MARKED`): the marker discloses the gap, it does not discharge the claim. Driving the `untraced_claims` reading itself to zero would mean inventing citations, which is the failure mode the bound exists to prevent.

**3. `shared/spine/references/output-template.md` is measured but not gated.** It is the specification document whose §4 worked examples deliberately include non-conforming forms as labelled teaching contrasts, so a detector-conformance fix would require either mislabelling a deliberately-broken example or restructuring the document's own pedagogy. CONF-03..06 name the fourteen shipped analyses only. Phase 17 measured this surface and handed the scope question to Phase 18; Phase 18 declines it by this stated reason -- an accepted, disclosed exclusion, never a silent omission.

**4. The closure-ledger route has zero shipped exemplars.** `output-template.md` §6 blesses two citation routes; the exemplars use one -- the inline `(chain Cn)` form the template itself calls "the mechanically checkable form" (decision D-01). After this phase no shipped worked example demonstrates the `- "quoted claim" → chain Cn` closure-ledger row, because of backlog 999.24 (an unfenced in-section-6 ledger row counts itself as a claim) and `_slice_sections`'s section-6 rule, which ends §6 at the first ATX heading of any depth.

## shared-examples

| relpath | section_resolution | heading_chain_blocks | heading_malformed_blocks | marked_untraced_claims | silent_untraced_claims | analysis_id | conclusion_claims | untraced_claims | untraced_flag | verdict_cells | nonconforming_verdict_cells | verdict_flag | chain_blocks | malformed_chain_blocks | chain_flag | dependency_cycles | ungrounded_chains | selfaudit_disagreements | provenance_labels | unmatched_sources | unreadable_sources | literals_checked | unlocated_literals | misattributed_literals | zero_literal_gts | orphan_fetches | provenance_flag |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| shared/examples/composed-inversion-second-order.md | OK | 1 | 0 | 0 | 0 | composed-inversion-second-order | 2 | 0 | 0 | 8 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| shared/examples/decompose-irreducibility.md | SectionResolutionError: expected sections 1-6 to resolve in order, resolved [] | 0 | 0 | unreadable | unreadable | decompose-irreducibility | unreadable | unreadable | unreadable | unreadable | unreadable | unreadable | unreadable | unreadable | unreadable | unreadable | unreadable | unreadable | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| shared/examples/estimate-fermi.md | SectionResolutionError: expected sections 1-6 to resolve in order, resolved [] | 0 | 0 | unreadable | unreadable | estimate-fermi | unreadable | unreadable | unreadable | unreadable | unreadable | unreadable | unreadable | unreadable | unreadable | unreadable | unreadable | unreadable | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| shared/examples/ishikawa-fishbone.md | OK | 3 | 0 | 0 | 4 | ishikawa-fishbone | 4 | 4 | 1 | 8 | 8 | 1 | 3 | 0 | 0 | 0 | 0 | 2 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| shared/examples/personal-general-2.md | OK | 3 | 3 | 0 | 7 | personal-general-2 | 7 | 7 | 1 | 8 | 8 | 1 | 3 | 3 | 1 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| shared/examples/personal-general.md | OK | 2 | 0 | 0 | 7 | personal-general | 7 | 7 | 1 | 5 | 5 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| shared/examples/product-business-2.md | OK | 3 | 3 | 0 | 4 | product-business-2 | 4 | 4 | 1 | 7 | 7 | 1 | 3 | 3 | 1 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| shared/examples/product-business.md | OK | 3 | 0 | 0 | 3 | product-business | 3 | 3 | 1 | 7 | 7 | 1 | 3 | 0 | 0 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| shared/examples/science-engineering-2.md | OK | 2 | 2 | 0 | 3 | science-engineering-2 | 3 | 3 | 1 | 8 | 8 | 1 | 2 | 2 | 1 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| shared/examples/science-engineering.md | OK | 2 | 2 | 0 | 3 | science-engineering | 3 | 3 | 1 | 8 | 8 | 1 | 2 | 2 | 1 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| shared/examples/self-application.md | OK | 3 | 3 | 0 | 9 | self-application | 9 | 9 | 1 | 6 | 6 | 1 | 3 | 3 | 1 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| shared/examples/software-systems-2.md | OK | 3 | 3 | 0 | 10 | software-systems-2 | 10 | 10 | 1 | 6 | 6 | 1 | 3 | 3 | 1 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| shared/examples/software-systems.md | OK | 3 | 3 | 0 | 8 | software-systems | 8 | 8 | 1 | 6 | 6 | 1 | 3 | 3 | 1 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| shared/examples/theoretical-limit-carnot.md | SectionResolutionError: expected sections 1-6 to resolve in order, resolved [] | 0 | 0 | unreadable | unreadable | theoretical-limit-carnot | unreadable | unreadable | unreadable | unreadable | unreadable | unreadable | unreadable | unreadable | unreadable | unreadable | unreadable | unreadable | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

## generated-twin

| relpath | section_resolution | heading_chain_blocks | heading_malformed_blocks | marked_untraced_claims | silent_untraced_claims | analysis_id | conclusion_claims | untraced_claims | untraced_flag | verdict_cells | nonconforming_verdict_cells | verdict_flag | chain_blocks | malformed_chain_blocks | chain_flag | dependency_cycles | ungrounded_chains | selfaudit_disagreements | provenance_labels | unmatched_sources | unreadable_sources | literals_checked | unlocated_literals | misattributed_literals | zero_literal_gts | orphan_fetches | provenance_flag |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| first-principles/agents/references/examples/composed-inversion-second-order.md | OK | 1 | 0 | 0 | 0 | composed-inversion-second-order | 2 | 0 | 0 | 8 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| first-principles/agents/references/examples/decompose-irreducibility.md | SectionResolutionError: expected sections 1-6 to resolve in order, resolved [] | 0 | 0 | unreadable | unreadable | decompose-irreducibility | unreadable | unreadable | unreadable | unreadable | unreadable | unreadable | unreadable | unreadable | unreadable | unreadable | unreadable | unreadable | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| first-principles/agents/references/examples/estimate-fermi.md | SectionResolutionError: expected sections 1-6 to resolve in order, resolved [] | 0 | 0 | unreadable | unreadable | estimate-fermi | unreadable | unreadable | unreadable | unreadable | unreadable | unreadable | unreadable | unreadable | unreadable | unreadable | unreadable | unreadable | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| first-principles/agents/references/examples/ishikawa-fishbone.md | OK | 3 | 0 | 0 | 4 | ishikawa-fishbone | 4 | 4 | 1 | 8 | 8 | 1 | 3 | 0 | 0 | 0 | 0 | 2 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| first-principles/agents/references/examples/personal-general-2.md | OK | 3 | 3 | 0 | 7 | personal-general-2 | 7 | 7 | 1 | 8 | 8 | 1 | 3 | 3 | 1 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| first-principles/agents/references/examples/personal-general.md | OK | 2 | 0 | 0 | 7 | personal-general | 7 | 7 | 1 | 5 | 5 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| first-principles/agents/references/examples/product-business-2.md | OK | 3 | 3 | 0 | 4 | product-business-2 | 4 | 4 | 1 | 7 | 7 | 1 | 3 | 3 | 1 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| first-principles/agents/references/examples/product-business.md | OK | 3 | 0 | 0 | 3 | product-business | 3 | 3 | 1 | 7 | 7 | 1 | 3 | 0 | 0 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| first-principles/agents/references/examples/science-engineering-2.md | OK | 2 | 2 | 0 | 3 | science-engineering-2 | 3 | 3 | 1 | 8 | 8 | 1 | 2 | 2 | 1 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| first-principles/agents/references/examples/science-engineering.md | OK | 2 | 2 | 0 | 3 | science-engineering | 3 | 3 | 1 | 8 | 8 | 1 | 2 | 2 | 1 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| first-principles/agents/references/examples/self-application.md | OK | 3 | 3 | 0 | 9 | self-application | 9 | 9 | 1 | 6 | 6 | 1 | 3 | 3 | 1 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| first-principles/agents/references/examples/software-systems-2.md | OK | 3 | 3 | 0 | 10 | software-systems-2 | 10 | 10 | 1 | 6 | 6 | 1 | 3 | 3 | 1 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| first-principles/agents/references/examples/software-systems.md | OK | 3 | 3 | 0 | 8 | software-systems | 8 | 8 | 1 | 6 | 6 | 1 | 3 | 3 | 1 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| first-principles/agents/references/examples/theoretical-limit-carnot.md | SectionResolutionError: expected sections 1-6 to resolve in order, resolved [] | 0 | 0 | unreadable | unreadable | theoretical-limit-carnot | unreadable | unreadable | unreadable | unreadable | unreadable | unreadable | unreadable | unreadable | unreadable | unreadable | unreadable | unreadable | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

## contract-surface

| relpath | section_resolution | heading_chain_blocks | heading_malformed_blocks | marked_untraced_claims | silent_untraced_claims | analysis_id | conclusion_claims | untraced_claims | untraced_flag | verdict_cells | nonconforming_verdict_cells | verdict_flag | chain_blocks | malformed_chain_blocks | chain_flag | dependency_cycles | ungrounded_chains | selfaudit_disagreements | provenance_labels | unmatched_sources | unreadable_sources | literals_checked | unlocated_literals | misattributed_literals | zero_literal_gts | orphan_fetches | provenance_flag |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| shared/spine/references/output-template.md | OK | 1 | 0 | 0 | 3 | output-template | 3 | 3 | 1 | 1 | 1 | 1 | 3 | 1 | 1 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

## Source-vs-twin agreement (D-04)

Compared fields (17): `conclusion_claims`, `untraced_claims`, `untraced_flag`, `verdict_cells`, `nonconforming_verdict_cells`, `verdict_flag`, `chain_blocks`, `malformed_chain_blocks`, `chain_flag`, `dependency_cycles`, `ungrounded_chains`, `selfaudit_disagreements`, `section_resolution`, `heading_chain_blocks`, `heading_malformed_blocks`, `marked_untraced_claims`, `silent_untraced_claims`.

Excluded (ten, foreordained equal on both surfaces): `analysis_id`, `provenance_labels`, `unmatched_sources`, `unreadable_sources`, `literals_checked`, `unlocated_literals`, `misattributed_literals`, `zero_literal_gts`, `orphan_fetches`, `provenance_flag`.

Result: 14 of 14 pairs agree.

Prior readings: `git log --follow docs/conformance-baseline.md`.
