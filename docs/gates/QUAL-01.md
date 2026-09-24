# QUAL-01: Offline blind A/B quality-measurement harness self-test — extraction guardrails, scoreline parsing, blinding, tabulation, baseline-fixture integrity, the mechanical defect detector, and the emission rendering contract's six legs.

<!-- GENERATED:FACTS -->
## Facts

- `control_ids` (27): `R-CHAIN-CONFORMING`, `R-CHAIN-NUMBERED`, `R-CHAIN-WRAPPED`, `R-CITE-INLINE`, `R-CITE-LEDGER`, `R-CITE-NONE`, `R-CLAIM-CAVEAT-CITED`, `R-CLAIM-CAVEAT-MARKED`, `R-CLAIM-COLON-END`, `R-CLAIM-COLON-MID`, `R-CLAIM-LABEL-BARE`, `R-CLAIM-LABEL-CITED`, `R-CLAIM-LABEL-INLINE`, `R-CLAIM-TERSE-DROP`, `R-CLAIM-TERSE-KEEP`, `R-HEAD-ALLCHAIN`, `R-HEAD-CHAINREF`, `R-HEAD-GTHOP-BAD`, `R-HEAD-GTHOP-LATE`, `R-HEAD-GTHOP-OK`, `R-HEAD-PERIOD-BAD`, `R-HEAD-PERIOD-LATE`, `R-HEAD-PERIOD-OK`, `R-HEAD-PROSE-BAD`, `R-HEAD-PROSE-MID`, `R-VERDICT-EXPIRY`, `R-VERDICT-EXPIRY-BAD`
- `control_count`: `27`
- `registered_surfaces` (4): `shared/references/reason-upward.md`, `shared/spine/SKILL-body.md`, `shared/spine/references/output-template.md`, `shared/spine/references/validation-rubric.md`
- `disclosed_bounds_anchors` (30): `CommonMark closing rules`, `Gate cap`, `R-CLAIM-CAVEAT-MARKED`, `R-CLAIM-LABEL-BARE`, `R-HEAD-GTHOP-LATE`, `R-HEAD-GTHOP-OK`, `R-HEAD-PERIOD-BAD`, `R-HEAD-PROSE-MID`, `boundary regression`, `call-site census`, `chain-family coverage floor`, `chain-form surface sweep`, `closure-ledger claim inventory`, `direct boundary arms`, `dispatch reachability`, `emission rendering contract`, `entry-source lock`, `expected-verdict floor`, `fence shape battery`, `fenced pseudo-heading`, `over-rejection bound`, `quality-ledger-v8.26`, `reason-upward.md`, `rendered-example claim floor`, `scored by a control, not merely extracted`, `section-intro label`, `silent false-clean`, `structural ledger row`, `validation-rubric.md`, `worked-example conformance`
- `derived_counts` (4 entries): `qual01_doc_row_count`=1, `qual01_doc_row_token_count`=30, `render_surface_count`=4, `rule_count`=13
- `locked_constants` (3 entries): `qual01_doc_rows`='docs/gates/QUAL-01.md', `render_surface_required_rules`='shared/spine/references/output-template.md: R1,R2,R3,R4,R5,R6,R7,R8,R9,R10,R11,R12,R13; shared/spine/SKILL-body.md: R1,R2,R3,R4,R5,R6,R7,R8,R9,R10,R11,R12,R13; shared/spine/references/validation-rubric.md: R1,R6,R7,R8,R9,R10,R11,R12; shared/references/reason-upward.md: R6,R7,R8,R9,R10', `rule_ids`='R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 | R11 | R12 | R13'
- `contract_pins` (3 entries): `_chain_block_well_formed` (digest=sha256:d7d42d7a0bd781bdb01f073d2929f7277c33c86c92f49bb63a48055ad15f13c3, line_count=121); `_conclusion_claims` (digest=sha256:8b0cc1f1d2d32215e284f0276afbdbd63e761bcef573ec3723f6e6205405d394, line_count=63); `_slice_sections` (digest=sha256:485ffe356a6782657709bc55ffaa1b474b1af2024398bcc00d2c799eb41c848e, line_count=149)
<!-- END GENERATED:FACTS -->

<!-- GENERATED:HOW-TO-RUN -->
## How to run

```sh
python3 scripts/check-quality-harness.py --self-test
```

CI job: — (not a CI job)
<!-- END GENERATED:HOW-TO-RUN -->

<!-- HAND-WRITTEN: preserved verbatim across regeneration. -->

## How to run, in detail

Added at v8.7 Phase 164; moved `scripts/check-firewall-battery.sh`'s offline gate count from 15
to 16.

## What it asserts

Offline blind A/B quality-measurement harness self-test (deterministic, no live session) —
extraction guardrails A/B, scoreline parser, blinding integrity, tabulation arithmetic,
baseline-fixture integrity, the mechanical defect detector (including chain-heading parsing,
chain-dependency acyclicity/grounding, and Self-Audit-Gate reconciliation against the measured
record), and defect-incidence schema compatibility; the promoted instrument behind the pre/post-fix
quality baseline (HARNESS-01, `docs/v8.7-quality-baseline-freeze.md`). As of Phase 11
(CONTRACT-03/CONTRACT-05), also covers the emission rendering contract as six separate legs: (1)
worked-example extraction — twenty-seven worked examples (the chain conforming/wrapped/numbered
trio, the section 6 citation trio, the current-constraint expiry pair, the chain-head grammar set:
the C6 head as emitted, the same head re-rendered with `C2 (threshold)`, C7's all-`Cn` head, the
same prose input moved to a non-final position (`R-HEAD-PROSE-MID`), which the frozen detector
scores well-formed, a hop beginning with a `GT-N` identifier, which the frozen detector scores
malformed, the same hop with the identifier moved off the front, which it scores well-formed, and
the same offending hop moved to a later position (`R-HEAD-GTHOP-LATE`), which the frozen detector
also scores well-formed, and R10's disclosed over-rejection bound
(`R-HEAD-PERIOD-BAD`/`R-HEAD-PERIOD-OK`/`R-HEAD-PERIOD-LATE`): a chain whose head or first hop
closes its own sentence before the next arrow is scored malformed even though it violates none of
R1-R9 (`R-HEAD-PERIOD-BAD`, scored malformed, against its one-character minimal pair
`R-HEAD-PERIOD-OK`, scored well-formed), while the identical closure from the second hop onward does
not change the verdict (`R-HEAD-PERIOD-LATE`, scored well-formed)) are extracted from
`shared/spine/references/output-template.md` at self-test time and scored by the unmodified
detectors (`_chain_block_well_formed`, `_verdict_conforms`, `_claim_is_traced`), never compared to
any other surface, with a consumption floor failing the gate if any of the twenty-seven is not
requested and either scored by a control, not merely extracted, or reported. The
scored-not-extracted consumption floor was itself strengthened (plan 13-10, BL-03): each locked
fixture's recorded verdict must equal an inline expected-verdict floor, and the thirteen
chain-family fixtures are additionally re-scored by the floor itself, by calling the unmodified
`_chain_block_well_formed` on the extracted text, so a control that calls a scorer and discards its
result, or writes the recorder directly, no longer discharges the floor. Which fixtures that
re-score arm covers is not restated but derived, as of plan 13-12 (CR-03) — a **chain-family
coverage floor** computes the family from the locked fixture-id set by prefix (`R-CHAIN-` /
`R-HEAD-`) and asserts EQUALITY, so narrowing the re-score table while the recorded-verdict table
stays whole fails the gate naming the arm and the dropped ids, replacing a union-of-both-tables
check that could not see that narrowing because the recorded-verdict table is a superset of the
re-score table (CR-03). The same floor covers the recorded-verdict table by equality against all
twenty-seven locked ids, and the dispatch-reachability symbol set (leg 4 below) by equality against
the five locked anchors, the latter replacing a subset test that could not see the anchor set itself
narrowing (WR-04). Plan 13-16 (R4-CR-01, `13-VERIFICATION-round4.md`) extended control (t)'s
source-text call-site census to all three floor helpers that make this guarantee forgery-proof: the
coverage-floor-registry helper (6 call sites: 1 real THE FLOOR ITSELF call plus the x1-x4 isolation
arms plus leg 5's own reuse for its NON-VACUITY floor), the worked-example-conformance helper (6
call sites: 1 real THE LEG ITSELF call plus the z5-z9 isolation arms), and the entry-source helper
(5 call sites: 1 real ENTRY-SOURCE LOCK call plus the x6-x9 isolation arms) — each floored against
its own per-helper expected count, so deleting a floor's single real call site now fails the gate by
name rather than only in diff review; before plan 13-16, deleting either of the first two floors'
single real call left the battery green with the exact defect the floor exists to catch restored
(R4-CR-01). The same plan (R4-CR-02) added an ENTRY-SOURCE LOCK to control (x): each coverage-floor
registry entry's required side is RE-DERIVED at lock time from the primary locked constants — a
fresh chain-family derivation for arm 4a, the locked fixture-id set for arm 4b, and an independent
second transcription of the five dispatch anchors — and an entry whose required and actual sides are
bound to the same object is rejected, so a required side rebound to its own actual side (`x != x`,
structurally incapable of failing) is caught rather than passing every name-based check; before this
plan, a one-token rebind of one entry's required side restored the chain-family coverage floor's
pre-13-12 narrowing defect with the battery green (R4-CR-02). The C6 pair is scored in both
directions by the unmodified `_chain_block_well_formed`, so the pair discriminates the possessive
form in trailing head position; `R-HEAD-PROSE-MID` pins the measured bound that the same violation
in an earlier position is scored well-formed, so R7 as published states the bound rather than an
unconditional claim; (2) cross-surface literal reconciliation — twelve hand-transcribed rule
literals (R1-R12) must be present byte for byte on the surfaces that declare them, and no registered
surface among all four — `shared/spine/references/output-template.md`, `shared/spine/SKILL-body.md`,
`shared/spine/references/validation-rubric.md`, and `shared/references/reason-upward.md` — may carry
one of five enumerated wrap-permitting phrasings, with required literals scoped per surface (the
rubric declares R1, R6, R7, R8, R9, R10, R11 and R12; `reason-upward.md` declares R6, R7, R8, R9 and
R10 — it is canonical because it is the sole source of the shipped, slash-invocable `/reason-upward`
stub via `{{PROCEDURE:reason-upward}}`; the two contract surfaces declare all twelve); a chain-form
surface sweep (`_render_chain_form_surface_problems`, plan 13-24) separately derives its own
candidate set from a tree-wide chain-form-template signature — a chain-head token followed by an
arrow into a lowercase placeholder bracket — and asserts EQUALITY against the four registered
surfaces plus a written-reason exemption list, so a fifth surface stating the chain form is caught
by the sweep rather than by trusting the registry's own entry count;
`shared/references/estimate-detail.md` and `shared/references/theoretical-limit-detail.md` took the
point-back fork instead of registration (plan 13-24) — both now cite `output-template.md` §4 for the
chain form rather than restating it, so the sweep's candidate set excludes them by construction, not
by a silent registry omission; (3) registry lock — the registries backing (1) and (2) are
membership-locked by value against inline expectations, with a per-field negative case and an
anti-masking floor; a rendered-example claim floor (plan 13-23) separately asserts, unscoped across
every registered surface regardless of that surface's required-rule set, that a surface currently
claiming its examples follow the head form actually renders R8's literal inside a fenced block —
closing the fabricated-claim shape `shared/references/reason-upward.md` shipped for a full milestone
before this floor existed; (4) dispatch reachability (Phase 13, CR-02) — every
`_selftest_*`/`_self_test_*` symbol a `check-traceability.py` matrix `artifact_link` names, pointing
at this file, is asserted to be called from `self_test()`, not merely defined, with the symbol set
derived from that sibling script's source rather than restated here, an independent detector from
the one `check-traceability.py` itself runs (two scripts, so hiding a deleted dispatch requires
editing both), a live positive proving the derived anchors are dispatched, an EQUALITY floor over
the derived symbol set against a locked five-anchor set (plan 13-12, WR-04 — one of the three
entries in the same chain-family coverage floor, replacing a non-vacuity subset test that could not
see the anchor set itself narrowing), the anchor regex accepting both `_selftest_*` and
`_self_test_*` naming conventions (the derived set is unchanged today because no
`scripts/check-quality-harness.py#...` matrix row names a `_self_test_*` anchor), and synthetic
negative cases for an uncalled and a commented-out dispatch. This file's own detector stays scoped
to anchors this file's own `artifact_link`s name (A-02, 13-11; naming-convention widened at 13-12):
`check-traceability.py`'s widened leg additionally covers its OWN `_self_test_*` anchors and
`_run_self_test()` dispatcher (including `async def`), so the two-scripts independence property this
leg provides covers only the anchors this file's `artifact_link`s name — it does not extend to
`check-traceability.py`'s own `_self_test_*` anchors (e.g. SHIP-03's `_self_test_headline_lock`),
which are covered by one detector, not two. (5) **worked-example conformance** (plan 13-14, CR-01,
`13-VERIFICATION-round3.md`) — every `shared/examples/*.md` file whose text, after whitespace
normalization, asserts `in the prescribed head form` has every one of its `### Conclusion` chain
blocks scored by the unmodified `_chain_block_well_formed`, with the claiming-file set DERIVED from
the claim literal rather than restated as a filename list and floored by equality against a locked
set, and with a claiming file that yields zero blocks reported rather than passed. This closes
CR-01, where two shipped examples asserted a head form all four of their chains violated and no gate
reached the file. (6) **closure-ledger claim inventory** (Phase 14, LEDGER-01..04) — R11 (claim
extraction) and R12 (caveat) are new registered literals on all three D-06 surfaces
(`output-template.md`, `SKILL-body.md`, `validation-rubric.md`), and R4 (citation) is amended with
D-01's section-6-visibility disclosure and D-03's structural-row residual; the fixture population
these legs score moved from eighteen to twenty-seven, adding nine `R-CLAIM-*` fixtures pinning R11's
three bounds and R12's marker. Two detector corrections ship alongside: `_slice_sections`' section 6
now stops at the first ATX heading of any depth CommonMark recognises (1-6 hashes, with the
up-to-three leading spaces it permits) that is not inside a fenced code block — a **fenced
pseudo-heading** is verbatim content, never a boundary — and, independently of any fence reasoning,
never later than the Self-Audit Gate, located by `_SELFAUDIT_CRITERION_RE` over the whole analysis
text. That second condition is a **Gate cap**, not a redundancy: `fence / ## a / ## b / fence` is
the same token shape whether it is a legitimate two-line fenced ledger or a fence swallowing two
appendix headings, so no rule reading fence and heading positions alone can separate them — three
successive attempts each shipped a measured defect (no tracking → 0/0/0 false-clean; parity →
section 6 absorbed the Gate and returned an 8th claim; closes-before-next-heading → an ordinary bash
block with two `# ` comments read 0/0/0). Fence extent uses **CommonMark closing rules** — same
delimiter character, at least the opening length, no info string on the closer, no backtick in a
backtick opener's info string — never a parity toggle, which inverts permanently on a legal `~~~`
block quoting an unclosed ``` example.

## Disclosed bounds

DISCLOSED BOUND: an unterminated fence runs to end of document per CommonMark, so a section 6
opening one returns nothing; measured identical before this milestone and after, and the
conservative direction — too short, never absorbing the Gate (D-02), and `_closure_ledger_fragments`
requires the line to match a **structural ledger row** shape before a citation is even consulted
(D-03) — both asserted per-analysis by name against the frozen v8.7 corpus. SCOPE, matching control
(i)'s own DISCLOSED BOUND rather than overstating it: that control pins `conclusion_claims` and
`untraced_claims` only, and those two fields are what is unmoved under either change.
`_closure_ledger_fragments` is NOT pinned and did move — D-03 deliberately drives it toward zero,
measured 2 → 0 (condA-P2) and 1 → 0 (condB-P1) — and no other `detect_defects` field is observed at
all. A new committed fixture, `quality-ledger-v8.26` (the 2026-09-02 PR-P1 analysis, `.planning/`
being gitignored and therefore unreachable by any command), backs a live leg reading
`detect_defects` against it directly: 7 claims / 0 ledger fragments / 1 untraced, with the untraced
claim's identity pinned and three independently-neutralization-tested anti-vacuity arms, plus two
**boundary regression** arms (4-5) pinning the two defects the phase-14 review found in the D-02 fix
as first shipped, each live-reproduced against that fixture before being fixed and each
neutralization-tested to fire alone: a depth-4 appendix heading read 8 claims where the eighth was a
Self-Audit Gate line, and a fenced `## …` line inside section 6 collapsed the reading to 0 claims /
0 fragments / 0 untraced — a **silent false-clean**, which is why the arms assert invariance of the
whole 7/0/1 reading rather than any single moved number. Arms 6-9 are a table-driven **fence shape
battery**, one row per shape a previous cut got wrong (fence spanning the appendix headings; a
fenced block holding two heading-shaped lines; a `~~~` block quoting an unclosed ``` example; and
the unterminated-fence bound, pinned at 0/0/0 so a change to it must be deliberate). Arms 10-11 are
**direct boundary arms** over `_fenced_code_flags` and `_slice_sections` on synthetic documents
carrying no Gate, and they exist because the Gate cap MASKS what it catches: with the cap in place,
narrowing the depth bound or breaking a CommonMark closing rule leaves arms 4-9 silent (measured).
Arm 11, not arm 4, is what floors the depth and indent bounds; arm 4 asserts end-to-end invariance
only. Eleven mutations — each rule of the fence scanner, each half of the heading pattern, the cap,
and the fence check in either scan — were each verified to fire at least one arm. Neither shape
occurs anywhere in the frozen v8.7 corpus, so control (i) is structurally blind to both and these
arms are the only thing covering them. DISCLOSED BOUNDS, in the same voice as R7/R9/R10: R11's three
bounds are measured properties of `_conclusion_claims`, not prescriptions — a bold lead-in alone on
its line with no citation of its own is a **section-intro label** and escapes the claim obligation
(pinned by `R-CLAIM-LABEL-BARE`), a bold span whose closing `**` does not immediately follow a colon
is never matched, and a list item under the assertiveness floor (forty characters, no terminal
punctuation) is not a claim; a caveat carrying the `no chain — flagged assumption only` marker still
scores untraced BY DESIGN (`R-CLAIM-CAVEAT-MARKED`) — the marker discloses the gap, it does not
discharge the claim, and the extractor and tracer are deliberately not taught to recognise it; the
pre-analysis process-output ledger is invisible to `_closure_ledger_fragments` by construction, so
inline citation is the only mechanically checkable discharge form; `R-CLAIM-TERSE-DROP`/`-KEEP` are
worded differently rather than a one-character minimal pair, with an in-memory punctuation-toggle
re-score recovering the minimal-pair property the fixture text itself could not keep; and the leg
asserts a `detect_defects` reading only, never a Criterion 6 band, which a model assigns and no gate
here checks.) DISCLOSED LIMITATIONS: the contradiction leg detects an enumerated phrase set pinned
against wordings this tree really shipped, not arbitrary contradiction of R1, and the doc-row check
asserts required tokens in this page's hand-written narrative only (fence-excluded, T-21-08-02), not
the rest of the narrative's prose — repointed at plan 21-08 (CONF-12) from the two `| QUAL-01 |`
table-row surfaces this page replaced. The
chain-head grammar's presence and scoring controls assert that the grammar is stated and that the
fixtures score as measured — they do not measure whether the agent complies with the grammar at
emission time, which needs a live run (999.12/999.13). The chain-head fixtures pin what the detector
measurably does, not what R7 prescribes — R7 binds in every input position while the form check
reaches only the last, and that asymmetry is stated on all four canonical surfaces rather than
closed in code (the detector is frozen under CONTRACT-06). The head-only scope note (R9) carries an
exception the form check imposes rather than the grammar — a hop leading with a `GT-N` identifier
ends the chain — and `R-HEAD-GTHOP-BAD`/`R-HEAD-GTHOP-OK` pin both directions of that behaviour at
hop position 1, which is the only position the form check reaches, and `R-HEAD-GTHOP-LATE` pins the
measured non-detection with two hops preceding, so R9 as published states the bound rather than an
unconditional refusal — the same disclosure shape `R-HEAD-PROSE-MID` gives R7. R10 discloses the
mirror-image bound: the detector also over-rejects — a chain whose head or first hop closes its own
sentence before the next arrow is scored malformed even though it violates none of R1-R9 — and that
rejection is itself positional, reaching only the head and the first hop;
`R-HEAD-PERIOD-BAD`/`R-HEAD-PERIOD-OK`/`R-HEAD-PERIOD-LATE` pin the rejecting, conforming and
undetected-position cases respectively, so the published bounds now cover both under-detection
(R7/R9) and over-rejection (R10). Separately, disclosed but not required: zero of the fourteen
shipped worked examples in `shared/examples/` instantiate the `Cn`-as-head-input half of R7/R8 —
`output-template.md`'s own `R-HEAD-ALLCHAIN` fixture does, which is what CHAINHEAD-06 literally
requires; broadening `shared/examples/` to also exercise it is a deliberate, non-blocking extension,
not a gap. The strengthened consumption floor's independent re-score (arm 4a) covers only the chain
family; for the five `R-CITE-*` / `R-VERDICT-*` fixtures the guarantee is the recorded verdict (arm
4b) plus control (v)'s delegation probe plus control (t)'s source-level idiom lock, and a
hand-written recorder entry with correct values would satisfy the recorded-verdict arm for those
five. The chain-family coverage floor's own registry is hand-registered (plan 13-12): a fourth
coverage set added later without an entry in it is invisible to this floor, the same limitation
`_RenderRegistrySnapshot`'s own SCOPE paragraph states for its roster. And the dispatch-reachability
entry's required side is a locked set with a second, independent transcription in the entry-source
lock (plan 13-17), which makes narrowing it a two-place edit rather than the single-place edit it
was before; a required side rebound to an expression of EQUAL value is harmless by construction and
therefore invisible to the entry-source lock's WRONG SOURCE arm — only a rebind that changes what
the entry actually requires, or aliases it to its own actual side, is caught, with control (u)'s
live positive proving the five anchors it names are really dispatched. The call-site census counts
source text and observes no behaviour: it catches DELETION of a real call, not a call whose returned
problems are discarded instead of being passed to the failure reporter. The worked-example
conformance leg checks only files that make the claim, not all fourteen worked examples; block
boundaries are a heading-and-rule heuristic, not a parse; whitespace normalization is what makes the
hard-wrapped claim in `composed-inversion-second-order.md` visible, and a line-scoped test would
exempt it; the other twelve example files were measured and are a known out-of-scope surface (three
do not resolve into six template sections at all; seven of the nine that do carry at least one
malformed section-4 chain, 19 malformed blocks in total), recorded here rather than silently
omitted; and the leg detects a chain rendered in the malformed form — it does not detect every
re-wrap of an already-conforming head, because the form check requires only two arrows in the
truncated candidate, so a wrap or a GT-led hop after the second arrow is scored conforming, and a
head split across two physical lines is scored conforming with its first input dropped — a property
of the detector frozen under CONTRACT-06 and therefore an accepted limitation, not a defect this
phase closed. The operative property: the first chain-start candidate in each of those blocks
already satisfies the form check's two-arrow requirement on its truncated segment, so the block
scores conforming regardless of what follows.

## Provenance

**CONTRACT-06 source pins — three, as of the Phase 15 SCAN-04 validation audit.** The `sha256:<hex>`
source-digest mechanism (hash `inspect.getsource()`'s output after `.rstrip("\n")`, with exactly one
named helper per function so nothing else in the module calls `getsource` on it) now covers
`_chain_block_well_formed` (Phase 13, CHAINHEAD-07), `_conclusion_claims` and `_slice_sections` —
the latter two added by the SCAN-04 audit. `15-04-SUMMARY.md` recorded all three as proved
byte-identical across Phase 15 by a one-off hand-run hash comparison, but only the first carried a
standing gate, so the other two were the "proved once, never re-run" shape SCAN-04's own validation
left uncovered; the two new pins freeze the digests **and** line counts that summary measured (63
and 149 respectively), so they re-assert the recorded state rather than whatever happened to sit in
the tree at audit time. Each carries the same four lettered controls as the original — (a) positive,
(b) anti-vacuity perturbation, (c) `.rstrip` formula control, (d) message control — and the same
recompute discipline: a diff to a pinned literal must FOLLOW a written amendment to the milestone
goal, never precede it, and is never recomputed to make a failing self-test pass. This is a
different mechanism from `_RENDER_RULE_LITERALS`' membership lock, which is not a source digest.

## Residuals and open items

**Known staleness, disclosed rather than fixed:** `_slice_sections`' own body carries a Phase-14
comment stating it "carries no digest pin (only `_chain_block_well_formed` and
`_RENDER_RULE_LITERALS` do), so CONTRACT-06 is untouched" — true when written, false now. It cannot
be corrected without recomputing the pin that freezes those exact bytes, which the recompute
discipline forbids absent a written amendment, so it is recorded in the pin's own comment block
instead.
