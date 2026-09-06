<!-- GENERATED — DO NOT EDIT -->
<!-- Source: scripts/report-conformance.py -->
<!-- Regenerate: python3 scripts/report-conformance.py -->

# Conformance Baseline

Measurement date: 2026-09-06

This file is a measurement, not a contract: no figure below defines what the codebase is required to become, and no count in it gates a conformance check. Regenerating this file only ever fails on staleness -- committed bytes that no longer match a fresh run of `scripts/report-conformance.py` -- never on a count read here being high.

## Headline

| Reading | shared-examples | generated-twin | contract-surface |
|---|---|---|---|
| Files unreadable by `_slice_sections` | 0 of 14 | 0 of 14 | 0 of 1 |
| §6 conclusion claims (untraced) | 77 (2 untraced) | 77 (2 untraced) | 3 (3 untraced) |
| §6 untraced claims (marked / silent) | 2 untraced (2 marked, 0 silent) | 2 untraced (2 marked, 0 silent) | 3 untraced (0 marked, 3 silent) |
| §2 verdict cells (non-conforming) | 77 (0 non-conforming) | 77 (0 non-conforming) | 1 (1 non-conforming) |
| §4 `chain_blocks` (malformed) | 31 (0 malformed) | 31 (0 malformed) | 3 (1 malformed) |
| `### Conclusion` heading-swept blocks (malformed) | 31 (0 malformed) | 31 (0 malformed) | 1 (0 malformed) |
| Source-vs-twin agreement (D-04) | 14 of 14 pairs agree | | |

## Two chain-block censuses (D-05)

`detect_defects` and the `### Conclusion` heading sweep are both produced by the same frozen instrument, `scripts/check-quality-harness.py`, yet they read a different number of chain blocks. `detect_defects`'s §4-scoped `chain_blocks` / `malformed_chain_blocks` columns come from a section slice, so they cannot read the files `_slice_sections` rejects. The `### Conclusion` heading sweep -- `_render_example_chain_blocks` paired with `_chain_block_well_formed` -- is a heading scan, not a section parse, so it can read those same files. The two figures measure different things and are published as separately named columns rather than reconciled into one number.

## Column vocabulary

Three kinds of value appear in the per-artifact tables below. A number means the detector read the document and counted. The literal `n/a` means no `.jsonl` generation capture exists for this artifact -- true of all 29 artifacts, for the nine provenance columns, unconditionally. The literal `unreadable` means `_slice_sections` rejected the document, so the twelve measured schema fields were never computed. The nine provenance columns are emitted in full precisely so `n/a` and `0` are never printed as the same thing.

## Disclosed bounds

This phase publishes four disclosures in the same voice R7/R9/R10 use on the agent surface to state their own measured bounds, rather than leaving them to be discovered.

**1. Chain-form reach.** `heading_malformed_blocks == 0` means every scanned block conforms under `_chain_block_well_formed`'s measured reach -- the head and first hop, up to the second arrow of the first matching candidate. This is NOT the same claim as "no R7 violations remain in `shared/examples/`": a wrap or a GT-led hop after the second arrow is not detected. This phase fixes to the detector's bound, which is what CONF-04 states; fixing to R7 as published is a strictly larger job and is recorded as backlog, not as done.

**2. Marked-claim residual (derived) — a ratchet as of Phase 18 (CONF-GATE).** 4 claim(s) across shared-examples and generated-twin carry the `no chain — flagged assumption only` marker (shared-examples: 2, generated-twin: 2), computed from `rows` at render time, never hardcoded. This figure was established by Phase 18's exemplar-conformance pass rather than pre-declared, and it is now pinned by `scripts/check-conf-gate.py`'s `_MARKED_RATCHET`: the reading may fall, never rise. A marked caveat still scores untraced BY DESIGN (`R-CLAIM-CAVEAT-MARKED`): the marker discloses the gap, it does not discharge the claim. Driving the `untraced_claims` reading itself to zero would mean inventing citations, which is the failure mode the bound exists to prevent.

**3. `shared/spine/references/output-template.md` is measured but not gated.** It is the specification document whose §4 worked examples deliberately include non-conforming forms as labelled teaching contrasts, so a detector-conformance fix would require either mislabelling a deliberately-broken example or restructuring the document's own pedagogy. CONF-03..06 name the fourteen shipped analyses only. Phase 17 measured this surface and handed the scope question to Phase 18; Phase 18 declines it by this stated reason -- an accepted, disclosed exclusion, never a silent omission.

**4. The closure-ledger route has zero shipped exemplars.** `output-template.md` §6 blesses two citation routes; the exemplars use one -- the inline `(chain Cn)` form the template itself calls "the mechanically checkable form" (decision D-01). After this phase no shipped worked example demonstrates the `- "quoted claim" → chain Cn` closure-ledger row, because of backlog 999.24 (an unfenced in-section-6 ledger row counts itself as a claim) and `_slice_sections`'s section-6 rule, which ends §6 at the first ATX heading of any depth.

**5. The pre-commit conformance-drift gate fails on staleness, not on a lost catch (D-07).** `scripts/report-conformance.py --check` fails when the committed bytes of this file or `docs/data/conformance.json` no longer match a fresh run -- never when a count read here, including the adversarial-corpus false-negative rate below, is high. A detector change that moves a corpus reading fails `--check` as drift; regenerating the two artifacts makes it pass again. Nothing here raises an alarm that the *meaning* of a reading changed -- only that the committed bytes are out of date.

## shared-examples

| relpath | section_resolution | heading_chain_blocks | heading_malformed_blocks | marked_untraced_claims | silent_untraced_claims | analysis_id | conclusion_claims | untraced_claims | untraced_flag | verdict_cells | nonconforming_verdict_cells | verdict_flag | chain_blocks | malformed_chain_blocks | chain_flag | dependency_cycles | ungrounded_chains | selfaudit_disagreements | provenance_labels | unmatched_sources | unreadable_sources | literals_checked | unlocated_literals | misattributed_literals | zero_literal_gts | orphan_fetches | provenance_flag |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| shared/examples/composed-inversion-second-order.md | OK | 1 | 0 | 0 | 0 | composed-inversion-second-order | 2 | 0 | 0 | 8 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| shared/examples/decompose-irreducibility.md | OK | 1 | 0 | 2 | 0 | decompose-irreducibility | 7 | 2 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| shared/examples/estimate-fermi.md | OK | 1 | 0 | 0 | 0 | estimate-fermi | 5 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| shared/examples/ishikawa-fishbone.md | OK | 3 | 0 | 0 | 0 | ishikawa-fishbone | 4 | 0 | 0 | 8 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| shared/examples/personal-general-2.md | OK | 3 | 0 | 0 | 0 | personal-general-2 | 7 | 0 | 0 | 8 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| shared/examples/personal-general.md | OK | 2 | 0 | 0 | 0 | personal-general | 7 | 0 | 0 | 5 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| shared/examples/product-business-2.md | OK | 3 | 0 | 0 | 0 | product-business-2 | 4 | 0 | 0 | 7 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| shared/examples/product-business.md | OK | 3 | 0 | 0 | 0 | product-business | 3 | 0 | 0 | 7 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| shared/examples/science-engineering-2.md | OK | 2 | 0 | 0 | 0 | science-engineering-2 | 3 | 0 | 0 | 8 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| shared/examples/science-engineering.md | OK | 2 | 0 | 0 | 0 | science-engineering | 3 | 0 | 0 | 8 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| shared/examples/self-application.md | OK | 3 | 0 | 0 | 0 | self-application | 9 | 0 | 0 | 6 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| shared/examples/software-systems-2.md | OK | 3 | 0 | 0 | 0 | software-systems-2 | 10 | 0 | 0 | 6 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| shared/examples/software-systems.md | OK | 3 | 0 | 0 | 0 | software-systems | 8 | 0 | 0 | 6 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| shared/examples/theoretical-limit-carnot.md | OK | 1 | 0 | 0 | 0 | theoretical-limit-carnot | 5 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

## generated-twin

| relpath | section_resolution | heading_chain_blocks | heading_malformed_blocks | marked_untraced_claims | silent_untraced_claims | analysis_id | conclusion_claims | untraced_claims | untraced_flag | verdict_cells | nonconforming_verdict_cells | verdict_flag | chain_blocks | malformed_chain_blocks | chain_flag | dependency_cycles | ungrounded_chains | selfaudit_disagreements | provenance_labels | unmatched_sources | unreadable_sources | literals_checked | unlocated_literals | misattributed_literals | zero_literal_gts | orphan_fetches | provenance_flag |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| first-principles/agents/references/examples/composed-inversion-second-order.md | OK | 1 | 0 | 0 | 0 | composed-inversion-second-order | 2 | 0 | 0 | 8 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| first-principles/agents/references/examples/decompose-irreducibility.md | OK | 1 | 0 | 2 | 0 | decompose-irreducibility | 7 | 2 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| first-principles/agents/references/examples/estimate-fermi.md | OK | 1 | 0 | 0 | 0 | estimate-fermi | 5 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| first-principles/agents/references/examples/ishikawa-fishbone.md | OK | 3 | 0 | 0 | 0 | ishikawa-fishbone | 4 | 0 | 0 | 8 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| first-principles/agents/references/examples/personal-general-2.md | OK | 3 | 0 | 0 | 0 | personal-general-2 | 7 | 0 | 0 | 8 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| first-principles/agents/references/examples/personal-general.md | OK | 2 | 0 | 0 | 0 | personal-general | 7 | 0 | 0 | 5 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| first-principles/agents/references/examples/product-business-2.md | OK | 3 | 0 | 0 | 0 | product-business-2 | 4 | 0 | 0 | 7 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| first-principles/agents/references/examples/product-business.md | OK | 3 | 0 | 0 | 0 | product-business | 3 | 0 | 0 | 7 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| first-principles/agents/references/examples/science-engineering-2.md | OK | 2 | 0 | 0 | 0 | science-engineering-2 | 3 | 0 | 0 | 8 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| first-principles/agents/references/examples/science-engineering.md | OK | 2 | 0 | 0 | 0 | science-engineering | 3 | 0 | 0 | 8 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| first-principles/agents/references/examples/self-application.md | OK | 3 | 0 | 0 | 0 | self-application | 9 | 0 | 0 | 6 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| first-principles/agents/references/examples/software-systems-2.md | OK | 3 | 0 | 0 | 0 | software-systems-2 | 10 | 0 | 0 | 6 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| first-principles/agents/references/examples/software-systems.md | OK | 3 | 0 | 0 | 0 | software-systems | 8 | 0 | 0 | 6 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| first-principles/agents/references/examples/theoretical-limit-carnot.md | OK | 1 | 0 | 0 | 0 | theoretical-limit-carnot | 5 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

## contract-surface

| relpath | section_resolution | heading_chain_blocks | heading_malformed_blocks | marked_untraced_claims | silent_untraced_claims | analysis_id | conclusion_claims | untraced_claims | untraced_flag | verdict_cells | nonconforming_verdict_cells | verdict_flag | chain_blocks | malformed_chain_blocks | chain_flag | dependency_cycles | ungrounded_chains | selfaudit_disagreements | provenance_labels | unmatched_sources | unreadable_sources | literals_checked | unlocated_literals | misattributed_literals | zero_literal_gts | orphan_fetches | provenance_flag |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| shared/spine/references/output-template.md | OK | 1 | 0 | 0 | 3 | output-template | 3 | 3 | 1 | 1 | 1 | 1 | 3 | 1 | 1 | 0 | 0 | 0 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

## adversarial-corpus

**False-negative rate:** 10 of 13 corpus items' catalogued falsehood the unmodified, CONTRACT-06-frozen `detect_defects` did not catch -- despite every item being a stated, catalogued falsehood. Each of those 10 is a false negative: a substantively wrong analysis this instrument cannot distinguish from a sound one. Diagnostic: 9 of 13 items had no substantive `detect_defects` column fire on them at all; the difference between the two figures is exactly the items on which an unrelated column fired for a reason having nothing to do with the item's own catalogued falsehood.

- Stratum A: 2 of 5 catalogued target missed (1 of 5 no column fired)
- Stratum B1: 1 of 1 catalogued target missed (1 of 1 no column fired)
- Stratum B2: 7 of 7 catalogued target missed (7 of 7 no column fired)

**Backlog 999.4 gate input.** Stratum B2 -- reachable by nothing this project ships -- reads 7 of 7 catalogued target missed. Per `.planning/ROADMAP.md` Phase 999.4 (CONDITIONAL, gated on this measurement): a low B2 rate closes 999.4 unrun, with this measurement recorded as the reason; a high B2 rate promotes 999.4, with this corpus as its validation set.

**Stratum vocabulary.** Stratum A: a named `detect_defects` column (`dependency_cycles`, `ungrounded_chains` or `selfaudit_disagreements`) plausibly has reach over the item's wrongness. Stratum B1: out of `detect_defects`'s reach but reachable by another shipped instrument -- closed at PROV-GUARD only (`scripts/check-provenance.py`'s read-at-source join), since no other shipped instrument has a code path over an arbitrary analysis. Stratum B2: reachable by nothing this project ships.

**Fixtures, not artifacts.** This section measures deliberately wrong test fixtures, never shipped artifacts. A probe reading clean is never the same claim as an artifact conforming. A stratum-A item is a positive control ONLY when the column that fired is its own catalogued target -- proving the run genuinely reaches that column on shipped corpus bytes: `t03-composition-cycle`, `t04-chain-only-head-ungrounded`, `t05-selfaudit-overclaim-under-cycle`. An item on which a substantive column fired for an UNRELATED reason (`t13-grounded-alongside-cyclic-ref`) had its own catalogued target missed regardless -- it is a false negative, never a positive control, no matter which column fired. An item on which no substantive column fired at all (`t01-ledger-arbitrary-chain`, `t02-fabricated-read-at-source`, `t06-hidden-cycle-past-head`, `t07-non-sequitur-between-hops`, `t08-verdict-contradicts-its-type`, `t09-arithmetic-does-not-follow`, `t11-fabricated-ground-truth`, `t12-inline-citation-wrong-chain`, `t14-order-of-magnitude-conversion`) is a false negative under the same figure. Which item sits in which set is answered by the `target` / `target_hits` / `target_missed` columns of the table below, never by this prose. The false-negative rate above is a measurement no phase may target (D-06): the only lever that would move it is widening a frozen detector, which CONTRACT-06 forbids.

**No generated twin.** The corpus is a test fixture, not a shipped artifact: nothing under `shared/` produces it and `sync-content.py` never emits it, so it has no twin and carries no pair-agreement row.

| relpath | stratum | section_resolution | form_defects | dependency_cycles | ungrounded_chains | selfaudit_disagreements | target | target_hits | target_missed | no_column_fired | disposition |
|---|---|---|---|---|---|---|---|---|---|---|---|
| tests/adversarial-corpus-v9.0/t01-ledger-arbitrary-chain.md | B2 | OK | 0 | 0 | 0 | 0 | none | [] | True | True | accept-with-reason: LEDGER-01, the 999.2 seed case — no shipped rule reads citation semantics; B2 by construction. |
| tests/adversarial-corpus-v9.0/t02-fabricated-read-at-source.md | B1 | OK | 0 | 0 | 0 | 0 | none | [] | True | True | accept-with-reason: reachable only by PROV-GUARD, named per decision (c); B1. |
| tests/adversarial-corpus-v9.0/t03-composition-cycle.md | A | OK | 0 | 2 | 0 | 0 | dependency_cycles:c1,c2 | ['dependency_cycles:c1,c2'] | False | False | accept-with-reason: caught — positive control proving `dependency_cycles` reaches shipped corpus bytes; not a hole. |
| tests/adversarial-corpus-v9.0/t04-chain-only-head-ungrounded.md | A | OK | 0 | 0 | 2 | 0 | ungrounded_chains:c1,c2 | ['ungrounded_chains:c1,c2'] | False | False | accept-with-reason: caught — positive control proving `ungrounded_chains` fires without also cycling; not a hole. |
| tests/adversarial-corpus-v9.0/t05-selfaudit-overclaim-under-cycle.md | A | OK | 0 | 2 | 0 | 1 | selfaudit_disagreements:4 | ['selfaudit_disagreements:4'] | False | False | accept-with-reason: caught — positive control confirming the Criterion-4 contradiction wiring end to end; not a hole. |
| tests/adversarial-corpus-v9.0/t06-hidden-cycle-past-head.md | A | OK | 0 | 0 | 0 | 0 | dependency_cycles:c1,c2;ungrounded_chains:c1,c2 | [] | True | True | defer-with-owner: backlog 999.35 (`_chain_head_refs` cannot see a circularity stated past a chain's head line) — the detectors are frozen under CONTRACT-06 and this phase may not widen one. |
| tests/adversarial-corpus-v9.0/t07-non-sequitur-between-hops.md | B2 | OK | 0 | 0 | 0 | 0 | none | [] | True | True | accept-with-reason: invalid inference between well-formed hops; no shipped rule judges inferential validity; B2. |
| tests/adversarial-corpus-v9.0/t08-verdict-contradicts-its-type.md | B2 | OK | 0 | 0 | 0 | 0 | none | [] | True | True | accept-with-reason: verdict/Type coherence is outside `_verdict_conforms`' reach and outside Criterion 2's form scope; B2. |
| tests/adversarial-corpus-v9.0/t09-arithmetic-does-not-follow.md | B2 | OK | 0 | 0 | 0 | 0 | none | [] | True | True | accept-with-reason: no numeric-plausibility check exists in the harness; B2. |
| tests/adversarial-corpus-v9.0/t11-fabricated-ground-truth.md | B2 | OK | 0 | 0 | 0 | 0 | none | [] | True | True | accept-with-reason: unlabeled fabrication reachable by nothing shipped, including PROV-GUARD; B2. |
| tests/adversarial-corpus-v9.0/t12-inline-citation-wrong-chain.md | B2 | OK | 0 | 0 | 0 | 0 | none | [] | True | True | accept-with-reason: same LEDGER-01 family via the inline citation form, demonstrating the flaw is form-independent; B2. |
| tests/adversarial-corpus-v9.0/t13-grounded-alongside-cyclic-ref.md | A | OK | 0 | 2 | 2 | 0 | ungrounded_chains:c1 | [] | True | False | accept-with-reason: disclosed bound of `grounded()`'s own-ground-truth short-circuit; not treated as a fix target. |
| tests/adversarial-corpus-v9.0/t14-order-of-magnitude-conversion.md | B2 | OK | 0 | 0 | 0 | 0 | none | [] | True | True | accept-with-reason: no unit-conversion check exists in the harness; B2. |

All thirteen form columns and all nine always-`n/a` provenance columns for these items are carried in full in `docs/data/conformance.json` under `adversarial_corpus.rows`, and are omitted here for readability.

## live-conformance

**Live conformance rate:** 5 of 8 runs attempted scored zero form defects across the four counts this rate is defined on: `section_resolution` reading `"OK"` (readable), plus `heading_malformed_blocks`, `nonconforming_verdict_cells` and `silent_untraced_claims` all reading zero. N = 8 because CONF-10's rate is stated over every catalog row dispatched, whether or not the run went on to complete.

**Secondary rate, conditional on completion:** 5 of 8 runs whose outcome was `completed` scored the same four counts clean. Outcome breakdown: 8 `completed`.

**Noise discipline.** The K-of-5 governing record (`docs/v8.7-constraint-teardown.md` §2 item 3) established that noise equals effect for this project's live-measurement instruments at N=5. At N=8, this reading carries the identical caveat: it is a recorded observation, not a figure precise enough to detect a small true effect.

**Delegation-conditional bound (D-04).** Every run went through `--probe`'s frozen `_wrap_for_bypass` meta-instruction, which commands verbatim Agent-tool dispatch. This is therefore a conformance rate conditional on delegation having occurred, not an end-to-end user-path rate -- whether an unwrapped user prompt reaches DELEGATE at all is measured separately, by `check-routing.py` and `check-routing-battery.py`, neither of which this surface touches.

**Non-interactive-branch bound.** Every run went through `_run_prompt_to`'s Plan-36-locked `claude -p` transport, which is non-interactive, so AskUserQuestion was structurally unavailable in all of them. The Input Contract (`shared/agent/input-contract.md`) names two paths this forecloses, and NEITHER is measured by this surface: (a) the pre-analysis clarification path, where the agent asks and a human answers before the analysis starts -- the runs instead take the contract's documented fallback, stating the missing inputs at the top of the response and proceeding best-effort; and (b) the mid-run re-open, the Self-Audit-Gate-triggered re-entry edge the contract caps at once per analysis, which can never fire under this transport, so its own fallback (halt at the Absent verdict with a confidence caveat) is the only branch these captures can exercise. This is a scope bound on what the figure covers, never a defect and never a claim that the interactive branch would score the same -- it is unmeasured, not measured-and-equal. Of the 8 runs, 5 opened with this disclosure, firing in the runs whose prompts were underspecified and not in the runs carrying dense supporting figures -- a prompt-correlated pattern, not a session-wide one. This corpus's prior committed live fixtures (`tests/quality-provenance-v8.24`, `tests/quality-ledger-v8.26`) were produced through the same locked transport and carry the same disclosure, which is what keeps the PR-P1 longitudinal comparison like-for-like.

**False-negative backdrop.** A clean live reading means this instrument found nothing, exactly as `adversarial-corpus`'s own published false-negative rate means for that surface (10 of 13 catalogued falsehoods missed) -- never a claim that the analysis is correct.

**Provenance departure (D-06).** All nine provenance columns read `n/a` for these runs even though the `.jsonl` captures exist in-tree, because nothing joins them this phase. `n/a` means no join was performed, never "checked, found clean". Backlog 999.12 / MEAS-01 stays open, with its input now in-tree for the first time.

**Observation, not a gate.** This rate is a measurement no phase may target and no gate reads (`scripts/check-conf-gate.py`'s `_GATED_SURFACES` does not include this surface). It may inform a phase; it may not block one.

**No generated twin.** These captures are evidence, not shipped artifacts: nothing under `shared/` produces them and `sync-content.py` never emits them, so they carry no pair-agreement row.

| relpath | outcome | section_resolution | heading_malformed_blocks | nonconforming_verdict_cells | silent_untraced_claims | form_defects | clean | disposition |
|---|---|---|---|---|---|---|---|---|
| tests/live-conformance-v9.0/PR-N1.md | completed | OK | 0 | 1 | 0 | 1 | False | fix: 1 of 12 Assumptions Table Verdict cells (assumption A3) scores nonconforming — `Accept as necessary, Challenge as sufficient — it closes one of the three conditions in C1 and leaves the other two manual` inserts descriptive text between the leading token and the em-dash, a compound-verdict form the Verdict Vocabulary rule's three example bullets do not address either way. Filed against `shared/spine/references/output-template.md`'s Verdict Vocabulary section and `shared/spine/references/validation-rubric.md` Criterion 2's Rigorous descriptor. The analysis text itself is not edited. |
| tests/live-conformance-v9.0/PR-N2.md | completed | OK | 0 | 1 | 0 | 1 | False | fix: 1 of 19 Assumptions Table Verdict cells (assumption A4) scores nonconforming — `Accept provisionally — affects which price constants apply, not the structure` inserts an adverb between the leading token and the em-dash. Filed against the same two prescription sections as `PR-N1`'s disposition above: `shared/spine/references/output-template.md`'s Verdict Vocabulary section and `shared/spine/references/validation-rubric.md` Criterion 2's Rigorous descriptor. The analysis text itself is not edited. |
| tests/live-conformance-v9.0/PR-P1-R2.md | completed | OK | 0 | 0 | 0 | 0 | True | accept-with-reason: scored 0/0/0/0 across the four D-20-A counts (section_resolution OK, heading_malformed_blocks 0, nonconforming_verdict_cells 0, silent_untraced_claims 0). Against `adversarial-corpus`'s published 10-of-13 false-negative rate, a clean reading here means this instrument found nothing, not that the analysis is correct. This is the second half of the D-02 within-body-variance pair against `PR-P1` above — see the plan 20-03 SUMMARY and `tests/live-conformance-v9.0/README.md` for the reading. |
| tests/live-conformance-v9.0/PR-P1.md | completed | OK | 0 | 0 | 0 | 0 | True | accept-with-reason: scored 0/0/0/0 across the four D-20-A counts (section_resolution OK, heading_malformed_blocks 0, nonconforming_verdict_cells 0, silent_untraced_claims 0). Against `adversarial-corpus`'s published 10-of-13 false-negative rate, a clean reading here means this instrument found nothing, not that the analysis is correct. This row is also the D-02 within-body-variance / cross-body-longitudinal anchor for the PR-P1 / PR-P1-R2 pair and for the `tests/quality-provenance-v8.24/PR-P1.md` comparison — see the plan 20-03 SUMMARY and `tests/live-conformance-v9.0/README.md` for both readings. |
| tests/live-conformance-v9.0/PR-P2.md | completed | OK | 0 | 0 | 0 | 0 | True | accept-with-reason: scored 0/0/0/0 across the four D-20-A counts (section_resolution OK, heading_malformed_blocks 0, nonconforming_verdict_cells 0, silent_untraced_claims 0). Against `adversarial-corpus`'s published 10-of-13 false-negative rate, a clean reading here means this instrument found nothing, not that the analysis is correct. |
| tests/live-conformance-v9.0/Q-P1.md | completed | OK | 0 | 0 | 0 | 0 | True | accept-with-reason: scored 0/0/0/0 across the four D-20-A counts (section_resolution OK, heading_malformed_blocks 0, nonconforming_verdict_cells 0, silent_untraced_claims 0). Against `adversarial-corpus`'s published 10-of-13 false-negative rate, a clean reading here means this instrument found nothing, not that the analysis is correct. |
| tests/live-conformance-v9.0/Q-P2.md | completed | OK | 0 | 31 | 0 | 31 | False | fix: 31 of 31 Assumptions Table Verdict cells score nonconforming — the analysis wrote its own richer vocabulary (`Accepted as a modelling convention`, `Unverified — flagged`, `Challenged — rejected`, `Verified approximately true`, `Partially verified by construction`) instead of the exact leading token `Accept`/`Challenge`/`Discard` the Verdict Vocabulary rule prescribes. Filed against `shared/spine/references/output-template.md`'s Verdict Vocabulary section (its three example bullets show only conforming forms, with no counter-example of this drift) and `shared/spine/references/validation-rubric.md` Criterion 2's Rigorous descriptor, which states the identical token-plus-em-dash requirement. The analysis text itself is not edited. |
| tests/live-conformance-v9.0/Q-P3.md | completed | OK | 0 | 0 | 0 | 0 | True | accept-with-reason: scored 0/0/0/0 across the four D-20-A counts (section_resolution OK, heading_malformed_blocks 0, nonconforming_verdict_cells 0, silent_untraced_claims 0). Against `adversarial-corpus`'s published 10-of-13 false-negative rate, a clean reading here means this instrument found nothing, not that the analysis is correct. |

All thirteen form columns and all nine always-`n/a` provenance columns for these runs are carried in full in `docs/data/conformance.json` under `live_conformance.rows`, and are omitted here for readability.

## Source-vs-twin agreement (D-04)

Compared fields (17): `conclusion_claims`, `untraced_claims`, `untraced_flag`, `verdict_cells`, `nonconforming_verdict_cells`, `verdict_flag`, `chain_blocks`, `malformed_chain_blocks`, `chain_flag`, `dependency_cycles`, `ungrounded_chains`, `selfaudit_disagreements`, `section_resolution`, `heading_chain_blocks`, `heading_malformed_blocks`, `marked_untraced_claims`, `silent_untraced_claims`.

Excluded (ten, foreordained equal on both surfaces): `analysis_id`, `provenance_labels`, `unmatched_sources`, `unreadable_sources`, `literals_checked`, `unlocated_literals`, `misattributed_literals`, `zero_literal_gts`, `orphan_fetches`, `provenance_flag`.

Result: 14 of 14 pairs agree.

Prior readings: `git log --follow docs/conformance-baseline.md`.
