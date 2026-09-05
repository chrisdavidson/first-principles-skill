# Adversarial corpus catalog — Phase 19 (false-negative rate)

Per-item metadata for `tests/adversarial-corpus-v9.0/`: analyses that are **form-clean under the
frozen `detect_defects`** (`malformed_chain_blocks`, `nonconforming_verdict_cells` and
`untraced_claims` all read zero on every item) and **substantively wrong** — the wrongness lives in
citation semantics, derivation validity, provenance, verdict/type coherence, or arithmetic, none of
which the form checks read. This table is the machine-parsed input plan 19-06's equality floor
compares against the discovered `.md` files, and the disposition floor that fails by name on any
clean-scoring item carrying no recorded disposition.

Every item is labelled into exactly one stratum:

- **A** — a named `detect_defects` column (`dependency_cycles`, `ungrounded_chains` or
  `selfaudit_disagreements`) plausibly has reach over this item's wrongness. A clean score here is a
  real detector defect, unless the item is a positive control deliberately proving the column fires.
- **B1** — out of `detect_defects`' reach, but reachable by another shipped instrument. A clean score
  is a pointer to that instrument, not a hole. This stratum is **closed at PROV-GUARD only**
  (decision (c), `19-01-PLAN.md`): SCAN-GUARD reads only the shipped agent/rubric files and has no
  code path over an arbitrary analysis, CONF-GATE's floors are locked by equality to the named
  fourteen-exemplar set, and the routing batteries score a live session's routing decision, never a
  static document. A single-member list is what stops the label being used to launder a stratum-B2
  item as reachable when nothing shipped actually reaches it.
- **B2** — reachable by nothing this project ships. A clean score is an acknowledged bound, and this
  stratum's composition is the honest decision input for backlog 999.4 (semantic claim-to-chain
  judging) — never a target this or any phase may drive toward zero, because the only lever that
  would move it is widening a frozen detector.

**`T-10` is deliberately absent.** CONF-07 pins `nonconforming_verdict_cells` and `untraced_claims`
to zero corpus-wide, so a criterion-2 or criterion-6 self-audit disagreement can never fire on a
corpus item that also satisfies CONF-07's form precondition — the only surviving self-audit route is
Criterion 4 via `_dependency_cycles`, which `T-05` already occupies. The gap in the numbering is a
recorded decision (`19-01-PLAN.md` decision (b)), not an omission.

## Catalog

| ID | File | Stratum | Source | What is false | Rule that ought to catch it | Disposition |
|---|---|---|---|---|---|---|
| T-01 | t01-ledger-arbitrary-chain | B2 | derived:personal-general | A closure-ledger row quotes the claim from item 3 verbatim but cites chain C2, when chain C1 is the chain that actually derives that claim — LEDGER-01's arbitrary-chain-citation flaw and the 999.2 seed case named by CONF-07. | None — LEDGER-01 is invisible to every shipped rule; the closest non-reaching rule is `_claim_is_traced` (checks that a citation exists, never that it supports). | accept-with-reason: LEDGER-01, the 999.2 seed case — no shipped rule reads citation semantics; B2 by construction. |
| T-02 | t02-fabricated-read-at-source | B1 | derived:science-engineering-2 | GT-4's stated source — a specific SKF bearing-catalogue table entry marked `Provenance: read-at-source.` — is fabricated; no such datasheet backs the 131,850-hour L10 bearing-life figure. | PROV-GUARD (scripts/check-provenance.py) read-at-source join. | accept-with-reason: reachable only by PROV-GUARD, named per decision (c); B1. |
| T-03 | t03-composition-cycle | A | hand-authored | Conclusion C1 and Conclusion C2 each cite the other as support inside their own composition heads, forming a genuine citation cycle dressed as a well-formed two-arrow chain on each side. | dependency_cycles (`_chain_dependency_defects` cycle DFS). | accept-with-reason: caught — positive control proving `dependency_cycles` reaches shipped corpus bytes; not a hole. |
| T-04 | t04-chain-only-head-ungrounded | A | hand-authored | Conclusion C1's head cites only Conclusion C2, and C2's head cites only an undefined chain C3, so the recommendation is derived entirely from chain-to-chain composition anchored to nothing stated as fact. | ungrounded_chains (`_chain_dependency_defects` `grounded()` reachability search). | accept-with-reason: caught — positive control proving `ungrounded_chains` fires without also cycling; not a hole. |
| T-05 | t05-selfaudit-overclaim-under-cycle | A | hand-authored | The same two-chain composition cycle as T-03 is paired with a Self-Audit Gate block claiming Criterion 4 Band Rigorous, even though the analysis's own chains are genuinely circular. | selfaudit_disagreements (`_selfaudit_calibration_defects`, Criterion 4 contradicted by `_dependency_cycles`). | accept-with-reason: caught — positive control confirming the Criterion-4 contradiction wiring end to end; not a hole. |
| T-06 | t06-hidden-cycle-past-head | A | hand-authored | Conclusion C1 and Conclusion C2 are genuinely circular in their prose — each conclusion's practical force depends on the other — but the circularity is stated only after each chain's two-arrow head line, past where the dependency check reads. | dependency_cycles / ungrounded_chains (`_chain_dependency_defects`) — reads only each chain's head line. | defer-with-owner: backlog 999.35 (`_chain_head_refs` cannot see a circularity stated past a chain's head line) — the detectors are frozen under CONTRACT-06 and this phase may not widen one. |
| T-07 | t07-non-sequitur-between-hops | B2 | derived:product-business | Chain C2's second hop inverts the force of its first hop, using an unmeasured, high-sensitivity variable to argue for immediate adoption rather than for gathering data first — a non-sequitur between well-formed hops. | None — no shipped rule judges inferential validity between hops; the closest non-reaching rule is `_chain_block_well_formed` (checks form only). | accept-with-reason: invalid inference between well-formed hops; no shipped rule judges inferential validity; B2. |
| T-08 | t08-verdict-contradicts-its-type | B2 | derived:personal-general-2 | The drawdown-tolerance row's Verdict reads Accept with a conforming justification that argues for acceptance precisely because the belief is untested — the opposite of what its own Type and Treatment prescribe. | None — `_verdict_conforms` checks token + em-dash + non-empty justification only, never cross-reads the Type column. | accept-with-reason: verdict/Type coherence is outside `_verdict_conforms`' reach and outside Criterion 2's form scope; B2. |
| T-09 | t09-arithmetic-does-not-follow | B2 | derived:science-engineering | Chain C1's panel-sizing arithmetic multiplies by the 0.80 derating factor where the energy path requires dividing by it, producing a wrong 250 W panel-array recommendation carried consistently through the document. | None — no numeric-plausibility check exists anywhere in the harness; the closest non-reaching rule is `_chain_block_well_formed` (form only). | accept-with-reason: no numeric-plausibility check exists in the harness; B2. |
| T-11 | t11-fabricated-ground-truth | B2 | derived:product-business-2 | GT-4's engineering-capacity figure and its attributed source, an invented internal workforce survey, are both fabricated, with no read-at-source label attached to either. | None — the fabrication carries no read-at-source label, so PROV-GUARD (the nearest instrument) has no join to check it against. | accept-with-reason: unlabeled fabrication reachable by nothing shipped, including PROV-GUARD; B2. |
| T-12 | t12-inline-citation-wrong-chain | B2 | derived:product-business | The same LEDGER-01 falsehood as T-01, expressed through the inline `(chain Cn)` citation form rather than a ledger row: the citation names chain C2 where chain C1 is the chain that actually supports the claim. | None — same as T-01; the closest non-reaching rule is `_claim_is_traced` (checks citation existence, never support). | accept-with-reason: same LEDGER-01 family via the inline citation form, demonstrating the flaw is form-independent; B2. |
| T-13 | t13-grounded-alongside-cyclic-ref | A | hand-authored | Conclusion C1's head composes on its own ground truth plus Conclusion C2, and C2 and C3 form a genuine citation cycle, yet C1 reads fully grounded because `grounded()` short-circuits on its own ground truth before inspecting what it co-cites. | ungrounded_chains (`_chain_dependency_defects`), specifically for the citing chain C1 — not flagged, due to `grounded()`'s own-ground-truth short-circuit. | accept-with-reason: disclosed bound of `grounded()`'s own-ground-truth short-circuit; not treated as a fix target. |
| T-14 | t14-order-of-magnitude-conversion | B2 | derived:software-systems | The profiling-duration figure carried through chain C3, the self-audit ledger, and section 6's plan is wrong by two orders of magnitude: about 14 minutes where the correct conversion of one engineering day is 1,440 minutes. | None — no unit-conversion or numeric-plausibility check exists anywhere in the harness. | accept-with-reason: no unit-conversion check exists in the harness; B2. |

## Reading the strata

A stratum-A item scoring **non-clean** (`T-03`, `T-04`, `T-05`) is a positive control — proof the
corpus run genuinely reaches `dependency_cycles`, `ungrounded_chains` and `selfaudit_disagreements`
on shipped corpus bytes — not a hole in the corpus. `T-06` and `T-13` are the stratum's honest
misses: a genuine detector miss and a disclosed grounding-short-circuit bound, respectively, each
recorded with `defer-with-owner` or `accept-with-reason` rather than closed, because the three
sha256-pinned detectors this phase measures against are frozen under CONTRACT-06 and no plan in this
phase may widen one. Stratum B2's composition is the decision input backlog 999.4 consumes when it
is next reviewed — a low B2 rate is a reason to close 999.4 unrun; a high one is a reason to promote
it, with this corpus as its validation set. The headline false-negative rate this catalog feeds is,
per decision D-06, **a measurement no phase may target**: the only lever that would move it is
widening a frozen detector, and `docs/conformance-baseline.md` — never this file — is the single
generated surface that carries the figure itself.
