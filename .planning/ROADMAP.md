# Roadmap: first-principles-skill

## Milestones

- ✅ **v8.21.0 — REG-GUARD Registration Completeness Gate** — Phases 1-3 (shipped 2026-08-30)
- ✅ **v8.22.0 / v8.23.0** — shipped outside the GSD milestone machinery (direct commits; no `.planning/` record)
- ✅ **v8.24.0 — Capture-Based Provenance Verification** — Phases 4-6 (shipped 2026-08-31)
- ✅ **v8.25.0 — Rendering Contract & Surface Coverage** — Phases 10-12 (shipped 2026-09-02)
- ✅ **v8.26.0 — Self-Audit Falsifiability** — Phases 13-16 (shipped 2026-09-04)
- 🚧 **v9.0.0 — Conformance** — Phases 17-23 (in progress)

---

## Phases

<details>
<summary>✅ v8.21.0 — REG-GUARD Registration Completeness Gate (Phases 1-3) — SHIPPED 2026-08-30</summary>

- [x] Phase 1: Discovery & Audit (1/1 plans) — completed 2026-08-30
- [x] Phase 2: Gate Implementation (2/2 plans) — completed 2026-08-30
- [x] Phase 3: Integration & Ship (1/1 plan) — completed 2026-08-30

Full detail: `.planning/milestones/v8.21.0-ROADMAP.md`

</details>

<details>
<summary>✅ v8.24.0 — Capture-Based Provenance Verification (Phases 4-6) — SHIPPED 2026-08-31</summary>

Turned `*Provenance: read-at-source*` from an unfalsifiable self-report into a verified fact.
PROV-GUARD joins every read-at-source ground truth to a real `WebFetch`/`Read` in the run's stored
capture and locates every stated literal in that source's retrieved text — offline, against the
capture rather than the live web, so the check stays deterministic and replayable.

- [x] Phase 4: Capture Retention & Fixture Foundation (4/4 plans) — completed 2026-08-31
- [x] Phase 5: Provenance Verifier & Gate (3/3 plans) — completed 2026-08-31
- [x] Phase 6: Integration & Ship (5/5 plans) — completed 2026-08-31

**Shipped:** `scripts/check-provenance.py` (PROV-GUARD) as a CI job and the 23rd firewall-battery
gate; the git-tracked PR-P1 capture fixture; `--probe`/`--single` analysis retention;
`_DEFECT_RECORD_FIELDS` widened 13 → 22 columns. Live result against the committed fixture:
**7/7 sources matched, 35/35 literals located**. `FIREWALL: GREEN (23/23)`.
Coverage headline **147/90/0/237 → 161/91/0/252**.

Full detail: `.planning/milestones/v8.24.0-ROADMAP.md`

</details>

<details>
<summary>✅ v8.25.0 — Rendering Contract & Surface Coverage (Phases 10-12) — SHIPPED 2026-09-02</summary>

Stopped fixing form drift by hand. Both halves are the same defect shape — *a form is stated in
more places than anything checks* — and both are closed at the mechanism rather than the
instance. `HEADLINE-LOCK` went from one gated surface to seven, in both published renderings,
with a tree-wide scan that fails on any unregistered surface stating the headline as current
fact and a two-layer classifier that lets frozen historical documents keep their superseded
counts. The emission rendering contract is now prescriptive on three canonical surfaces, with
both open cases closed (hop wrapping, verdict expiry) by a stated rule plus a control.

- [x] Phase 10: Headline Surface Coverage (11/11 plans) — completed 2026-09-01
- [x] Phase 11: Emission Rendering Contract (11/11 plans) — completed 2026-09-01
- [x] Phase 12: Integration & Ship (5/5 plans) — completed 2026-09-02

**Shipped:** `COVERED_HEADLINE_SURFACES` / `HEADLINE_SCAN_GLOBS` and the widened `HEADLINE-LOCK`
sentinel in `check-traceability.py`; the R1-R6 rendering contract stated byte-identically across
`output-template.md`, `SKILL-body.md` and `validation-rubric.md`; QUAL-01 self-test Item 24 (eight
extracted fixtures, cross-surface literal reconciliation, by-value registry lock). CONTRACT-06
held — `_chain_block_well_formed` is sha256-identical to its v8.24.0 blob, so the detector was
**not** widened. `FIREWALL: GREEN (23/23)`.
Coverage headline **161/91/0/252 → 174/92/0/266**, swept by this milestone's own gate.

Full detail: `.planning/milestones/v8.25.0-ROADMAP.md`

</details>

---
<details>
<summary>✅ v8.26.0 — Self-Audit Falsifiability (Phases 13-16) — SHIPPED 2026-09-04</summary>

Made the check able to fail. v8.25.0 specified the emitted form; the first run measured against it
scored two self-audit disagreements — Criterion 4 Rigorous with a malformed chain block present,
Criterion 6 Rigorous with an untraced claim present — and neither was a detector artifact. Both
holes are closed by *stating the form* (R7-R12, byte-identical across four canonical surfaces,
each rule published with its measured positional bound rather than as an unconditional claim), and
Phase 5 now emits a chain-form and claim-inventory scan that Criteria 4 and 6 must quote rather
than assert against.

- [x] Phase 13: Chain-Head Grammar (28/28 plans) — completed 2026-09-03
- [x] Phase 14: Closure-Ledger Claim Inventory (6/6 plans) — completed 2026-09-03
- [x] Phase 15: Self-Audit Scan (13/13 plans) — completed 2026-09-04
- [x] Phase 16: Integration & Ship (5/5 plans) — completed 2026-09-04

**Shipped:** the §4 head-line grammar (R7-R10) with a sha256 pin over `_chain_block_well_formed`;
the closure-ledger claim-extraction and caveat rules (R11-R12) with `tests/quality-ledger-v8.26/`
pinned at its measured reading; the Phase 5 self-audit scan and SCAN-GUARD's 100 clause-level
named branches; and SHIP-05's exemplar-conformance disclosure (4/14 unreadable, 69/69 verdict
cells non-conforming, 56/58 claims untraced, 19/28 chain blocks malformed — v9.0.0 closes it).
`FIREWALL: GREEN (24/24)`. Coverage headline **175/91/0/266 → 192/94/0/286**, swept by
`HEADLINE-LOCK` rather than by hand.

Full detail: `.planning/milestones/v8.26.0-ROADMAP.md`

</details>

---

### v9.0.0 — Conformance

**Promoted from:** `.planning/PROPOSAL-L1-first-milestone-2026-09-04.md` (fully approved
2026-09-04), with companions `ANALYSIS-rework-root-cause-2026-09-04.md` and
`ANALYSIS-where-the-rigour-points-2026-09-04.md`. Phase numbering continues from Phase 16 — the
next free integer is **17**.

**Milestone goal:** Drive the shipped artifacts into conformance with the rules the apparatus
already enforces, then generate the claim surface and cap the meta-recursion — **L1 before L2
before L3.** Phases 17-20 are strictly L1 and must ALL complete before Phases 21-22 (L2, L3)
begin; Phase 21 depending on Phase 20 is the explicit ordering commitment of this milestone.

**The revised Definition of Done** (clause 1 is new, is first, and is the blocking one):

1. **(L1 — the gate)** Every shipped artifact governed by the rule scores conforming under the
   unmodified detector, and a standing check fails if that count regresses.

2. **(L2)** The rule is stated on every canonical surface that carries it — generated from the
   checker, never hand-transcribed.

3. **(L3)** One control proves the L1 check fails when the artifact is broken. Depth stops
   here — a guard guards the product; a guard is not itself guarded.

**Standing instruction for every plan and discussion this milestone** (REQUIREMENTS.md §
"Standing instruction for this milestone"):

> A success criterion is acceptable only if it names a count over shipped artifacts that can be
> driven to a target and then declared done. A criterion of the form *"the gate fails when X is
> broken"* is an L3 control — it belongs in the plan's verification section, never in the phase's
> exit condition.

Two guardrails, restated because they are the ones most likely to erode under pressure:
**(1) the detectors are frozen** — if an artifact cannot be made to conform, the *artifact*
changes, never the detector (the widening treadmill 999.2 documents); **(2) the rework cap is 2**
— more than two gap-closure plans in a phase halts it and forces a replan.

**Absorbed into this milestone from the backlog:** 999.2 becomes Phase 19; 999.12/999.13
(MEAS-01/MEAS-02) become Phase 20; 999.30/999.31 are terminally disposed by Phase 22.

- [x] **Phase 17: Conformance Baseline** - publish, as a committed and regenerable artifact, the (completed 2026-09-05)
      L1 conformance reading of every shipped surface under the unmodified frozen detectors; fix
      nothing

- [x] **Phase 18: Exemplar Conformance** - drive the shipped worked examples to full conformance (14/14 plans executed 2026-09-05; round-3 verification: 6/7, criteria 1-5 verified and unregressed, BL-01..BL-04 and WR-08 closed; criterion-6 durability gap PARKED by decision 2026-09-05 as backlog 999.34, shipping with the exit-code exposure documented) (completed 2026-09-05)
      with R1-R12 and make the zero standing (the core L1 phase)

- [ ] **Phase 19: False-Negative Rate** - establish whether the detector catches a
      structurally-impeccable, substantively-wrong analysis (promotes backlog 999.2)

- [ ] **Phase 20: Live Conformance** - answer whether the agent's own output conforms, not just
      the prose about it (promotes backlog 999.12/999.13, MEAS-01/MEAS-02)

- [ ] **Phase 21: Generate the Claim Surface** - eliminate hand-transcribed gate documentation
      via `--describe` and generated docs

- [ ] **Phase 22: Cap the Recursion** - write the depth rule, terminally dispose 999.30/999.31,
      split product findings from apparatus findings, set the rework cap at 2 plans

- [ ] **Phase 23: Ship v9.0.0** - 17 stamps in lockstep, battery GREEN, `[9.0.0]` CHANGELOG entry
      closing the SHIP-05 disclosure by name

### Phase 17: Conformance Baseline

**Goal**: Publish, as a committed and regenerable artifact, the L1 conformance reading of every
shipped surface under the unmodified frozen detectors. Fix nothing. This milestone cannot be
scoped, and its completion cannot be claimed, without a number that does not currently exist —
today the readings live in a throwaway shell invocation and one parenthetical in `CLAUDE.md`
describing them as "a known out-of-scope surface."

**Depends on**: none

**Dependency rationale**: Nothing in this milestone; Phase 16 already shipped.

**Requirements**: CONF-01, CONF-02

**Success Criteria** (observable, mechanically checkable):

  1. `scripts/report-conformance.py` emits a per-artifact table of every `_DEFECT_RECORD_FIELDS`
     reading for all 14 `shared/examples/*.md`, and separately for
     `shared/spine/references/output-template.md`, naming files the detector cannot read rather
     than skipping them.

  2. `docs/conformance-baseline.md` and `docs/data/conformance.json` are committed, generated by
     that command, and carry the six headline figures measured 2026-09-04.

  3. Re-running the command against an unchanged tree reproduces the committed artifacts byte for
     byte (`--check` mode, exit 1 on drift).

  4. The baseline is read-only about the future: it states no target, blocks no gate, and its
     numbers are dated. It is a measurement, not a contract.
**Plans**: 3 plans

Plans:
**Wave 1**

- [x] 17-01-PLAN.md — build `scripts/report-conformance.py`: frozen-harness import, glob discovery under named count floors, partial rows, both chain censuses, twin agreement, dual renderers, `--check`, inline `--self-test`

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 17-02-PLAN.md — generate and commit `docs/conformance-baseline.md` + `docs/data/conformance.json`, verify the six 2026-09-04 figures against two witnesses, run validation mutations 1-6 and 8 on a scratch copy

**Wave 3** *(blocked on Wave 2 completion)*

- [x] 17-03-PLAN.md — wire `--check` into both mirrored pre-commit hooks (D-06), sweep the five doc surfaces stating the gate count, prove mutation 7 on both install paths, confirm the battery is unmoved at 24/24

### Phase 18: Exemplar Conformance

**Goal**: Drive the shipped worked examples to full conformance with R1-R12 and make the zero
standing. The agent imitates these files; every violation they carry is a violation they teach.
This is the core L1 phase.

**Depends on**: 17

**Dependency rationale**: The baseline defines the work.

**Requirements**: CONF-03, CONF-04, CONF-05, CONF-06

**Success Criteria** (observable, mechanically checkable — every one a bounded count):

  1. All 14 `shared/examples/*.md` resolve into six template sections under `_slice_sections` —
     `SectionResolutionError` count **4 → 0**.

  2. Malformed chain blocks across every `### Conclusion` heading in `shared/examples/`, scored
     by the unmodified `_chain_block_well_formed`: **19 → 0** (of 28).

  3. Non-conforming §2 verdict cells under the unmodified `_verdict_conforms`: **69 → 0**.
  4. Untraced claims are closed to a stated bound, not to zero (decision D-2). Every §6
     conclusion claim in every shipped example either (a) names its chain inline, or (b) carries
     the `no chain — flagged assumption only` marker already prescribed by
     `output-template.md:397`, `validation-rubric.md:486` and `SKILL-body.md:260`.

       - **Silent untraced — cited by neither route: 56 → 0.** This is the falsifiable zero.
       - The `untraced_claims` reading **will not reach zero and must not be expected to**: a
         marked caveat still scores untraced by design (`R-CLAIM-CAVEAT-MARKED`) — the marker
         discloses the gap, it does not discharge the claim. Driving the reading itself to zero
         would mean inventing citations, which is the failure mode this bound exists to prevent.

       - The residual — the count of legitimately marked claims — is established by this phase,
         not pre-declared, published as a figure in `docs/conformance-baseline.md`, and pinned by
         the gate as a **ratchet: it may fall, never rise.**

       - Correctness of a citation is explicitly out of scope and remains backlog 999.4. The
         tracer is a substring test; this criterion proves citations are present or honestly
         absent, never that they are right.

  5. The generated tree (`first-principles/agents/references/examples/`) carries the same zeros —
     asserted against the emitted bytes, not the source.

  6. **One** new battery gate (`CONF-GATE`) fails if any count in criteria 1-4 rises above its
     target on either surface. It is registered in `check-firewall-battery.sh` and in
     `.github/workflows/validation.yml`, moving the battery 24 → 25.

**Explicit non-goal**: the detectors are frozen (CONTRACT-06). If an example cannot be made to
conform, the example changes — never the detector. Any proposal to widen a detector in this phase
is rejected by construction and filed as a separate finding.
**Plans**: 14 plans (8 executed + 6 gap-closure)

Plans:

**Wave 1**

- [x] 18-01-PLAN.md — add the `marked_untraced_claims` / `silent_untraced_claims` columns (D-06a),
      publish the phase's four written disclosures in the baseline, and C-number the 27 chain
      headings in the ten section-readable examples

**Wave 2** *(blocked on Wave 1)*

- [x] 18-02-PLAN.md — make `composed-inversion-second-order.md`, `estimate-fermi.md` and
      `theoretical-limit-carnot.md` resolve and conform, by heading renumber and transcription only
      (zero chains authored)

**Wave 3** *(blocked on Wave 2)*

- [x] 18-03-PLAN.md — `decompose-irreducibility.md`: six-section wrapper plus exactly ONE
      transcribed chain, closing `SectionResolutionError` 4 → 0

**Wave 4** *(blocked on Wave 3)*

- [x] 18-04-PLAN.md — de-wrap, verdict cells and citations for `self-application.md`,
      `software-systems.md`, `personal-general.md`

**Wave 5** *(blocked on Wave 4)*

- [x] 18-05-PLAN.md — de-wrap, verdict cells and citations for `software-systems-2.md`,
      `product-business-2.md`, `personal-general-2.md`

**Wave 6** *(blocked on Wave 5)*

- [x] 18-06-PLAN.md — verdict cells and citations for `ishikawa-fishbone.md`,
      `product-business.md`, plus de-wrap for `science-engineering.md` and
      `science-engineering-2.md`; closes criteria 2, 3, 4 and 5 corpus-wide

**Wave 7** *(blocked on Wave 6)*

- [x] 18-07-PLAN.md — build `scripts/check-conf-gate.py`: source-literal targets, claim floors under
      a D-07 equality lock, the marked-claim ratchet, the D-03 rule, the D-08 live anti-vacuity arm
      and a floored `--self-test`

**Wave 8** *(blocked on Wave 7)*

- [x] 18-08-PLAN.md — register CONF-GATE in the battery and CI (24 → 25), sweep the five
      current-fact doc surfaces, and prove all six success criteria by mutation on scratch copies

**Wave 9** *(gap closure — 18-VERIFICATION.md, blocking gap)*

- [x] 18-09-PLAN.md — floor CONF-GATE's own live-leg enforcement wiring: a source-text call-site
      census and call-form lock over `run_live()`'s six comparator calls (CR-01), plus independent
      literal locks for `_CLAIM_FLOORS`, `_MARKED_RATCHET` and `_PRESCRIBED_LEAD_INS` and the
      missing `CAVEAT_MARKER` negative control (CR-02); 18 → 31 controls, proved by neutralization

**Wave 10** *(blocked on Wave 9)*

- [x] 18-10-PLAN.md — reconcile the marked-claim ratchet to the corpus-wide quantity the baseline
      publishes (WR-02), repair `check-firewall-battery.sh`'s stale 24-gate header and add
      CONF-GATE's Composition-change paragraph, and clear the last stale current-fact battery
      count in `CLAUDE.md` plus both CONF-GATE doc rows' control count

**Wave 11** *(gap closure — 18-VERIFICATION.md re-verification, blocking gap BL-01/BL-02)*

- [x] 18-11-PLAN.md — strip `#` line comments before the call-site census counts and before the
      form lock matches (BL-01), and floor both census roster tables by set equality against
      `_LIVE_CALL_SITES_LOCK`, a second independent transcription (BL-02); 32 → 34 controls,
      proved by neutralization

**Wave 12** *(blocked on Wave 11)*

- [x] 18-12-PLAN.md — add per-surface denominator floors for `verdict_cells` and
      `heading_chain_blocks` (`_POPULATION_FLOORS`), wired into `run_live()` as a seventh
      floored call site, so a zero achieved by deleting the measured population fails (BL-03);
      folds in WR-07's uncontrolled heading-sum scope; 34 → 38 controls

**Wave 13** *(blocked on Wave 12)*

- [x] 18-13-PLAN.md — refactor the D-08 live anti-vacuity arm to return `(problems, lines)`
      instead of calling `sys.exit()` (WR-06) and control all four of its internal predicates
      with tempdir-driven fixtures (BL-04); 38 → 42 controls

**Wave 14** *(blocked on Wave 13)*

- [x] 18-14-PLAN.md — clear the three stale-figure residuals (`CLAUDE.md:39`, both pre-commit
      hook mirrors), reconcile both CONF-GATE doc rows with the shipped enforcement and its
      disclosed bounds, re-sweep with a predicate wider than 18-10's on both axes, and record the
      nineteen-row WR/IN residual ledger

### Phase 19: False-Negative Rate

**Goal**: Establish the one number that makes every other check meaningful — does this detector
catch an analysis that is structurally impeccable and substantively wrong? Until this exists, no
one can distinguish a gate that protects the product from a gate that only protects the prose.
Promotes backlog 999.2.

**Depends on**: 18

**Dependency rationale**: File overlap is the forcing constraint: both phases write
`docs/conformance-baseline.md`, and both edit `scripts/check-firewall-battery.sh` (18 registers
`CONF-GATE`; 19 registers a `_FROZEN_PATHS` entry, which also lands in
`scripts/check-quality-harness.py`). Secondarily, a conforming corpus is the control group — you
cannot measure false negatives against exemplars that already fail on form.

**Requirements**: CONF-07, CONF-08

**Success Criteria**:

  1. `tests/adversarial-corpus-v9.0/` ships at least 12 analyses that pass every form check
     (0 malformed blocks, 0 non-conforming verdicts, 0 untraced claims) while being substantively
     wrong, each with a written statement of what is false about it and which rule ought to have
     caught it. The seed case named in 999.2 — a closure ledger citing arbitrary chains — is one
     of them.

  2. `detect_defects` is run over the whole corpus and the false-negative rate is published as a
     single figure in `docs/conformance-baseline.md`, next to Phase 17's readings.

  3. Every corpus item scoring fully clean is filed as a named hole with an explicit disposition:
     fix, accept-with-reason, or defer-with-owner. Zero silent passes.

  4. The corpus is registered under `_FROZEN_PATHS` so FROZEN-EVIDENCE catches tampering.

**Plans**: 7 plans in 5 waves. Author-first / wire-last: waves 1-2 land the corpus and its two
sidecars with **zero** code touched (inert to every gate); wave 3 lands the surface extension and
the regenerated baseline in ONE commit; wave 5 registers `_FROZEN_PATHS` last, because
FROZEN-EVIDENCE's untracked-file leg would otherwise fire on corpus files before they are committed.

**Wave 1** *(three parallel authoring plans, disjoint filenames, no code touched)*

- [x] 19-01-PLAN.md — the 999.2 seed case (closure ledger citing a real but non-supporting chain)
      plus three stratum-B2 derivations; carries the phase's `<decision_record>` for all six
      "Claude's Discretion" questions and both open research questions
- [x] 19-02-PLAN.md — the corpus's single stratum-B1 item (fabricated read-at-source → PROV-GUARD)
      plus three further stratum-B2 derivations
- [x] 19-03-PLAN.md — five hand-authored stratum-A micro-documents: three positive controls making
      `dependency_cycles`, `ungrounded_chains` and `selfaudit_disagreements` fire, one genuine-miss
      probe past the chain head, one disclosed-bound probe

**Wave 2** *(blocked on Wave 1)*

- [x] 19-04-PLAN.md — `catalog.md` (seven columns, one row per item, keyed by stem) and the
      hand-written `README.md` (custody, sha256s, no-twin statement, frozen-evidence residual)

**Wave 3** *(blocked on Wave 2)*

- [x] 19-05-PLAN.md — the fourth `report-conformance.py` surface: discovery with a floor of 12,
      catalog join, corpus headline, the `## adversarial-corpus` markdown section publishing the
      rate as a single figure, the `adversarial_corpus` JSON key, and the regenerated baseline —
      all in one commit

**Wave 4** *(blocked on Wave 3)*

- [x] 19-06-PLAN.md — the D-04 catalog⇄discovery equality floor, the disposition floor (CONF-08's
      zero silent passes), the per-item and corpus-wide population floors, and the D-03 per-item
      in-memory perturbation floor, each with a named neutralization proving it fires

**Wave 5** *(blocked on Wave 4)*

- [x] 19-07-PLAN.md — register `tests/adversarial-corpus-v9.0` in `_FROZEN_PATHS` (battery stays
      at 25), prove BOTH FROZEN-EVIDENCE legs by mutation, amend the corpus README so its
      sequencing note is not the 999.25 shape, and record the phase's three exit counts

### Phase 20: Live Conformance

**Goal**: Answer the question this project has never answered: does the agent's own output
conform? Every gate to date scores prose about the agent. This scores the agent. Promotes
backlog 999.12/999.13 (MEAS-01/MEAS-02).

**Depends on**: 19

**Dependency rationale**: A false-negative rate is needed to interpret a clean live reading;
without it, "the run scored clean" is unfalsifiable. Note: the capture work alone (criterion 1)
needs no artifact from 18 or 19 and runs against the already-shipped v8.26.0 body; it is held
serial by the shared `docs/conformance-baseline.md` and by this milestone's L1-ordering
commitment, not by the captures themselves.

**Requirements**: CONF-09, CONF-10

**Success Criteria**:

  1. At least 5 live runs are captured on the shipped v8.26.0 body across the fixture set, and
     each capture's full `detect_defects` reading is committed under
     `tests/live-conformance-v9.0/`.

  2. A conformance rate — runs with zero form defects, over runs attempted — is published in
     `docs/conformance-baseline.md`.

  3. Every defect the live runs expose is filed against the artifact or the prescription, never
     closed by widening a detector.

  4. The reading is reported as an observation with its N stated, subject to the same noise
     discipline the K-of-5 record already establishes ("at N=5, noise equals effect") — a rate,
     not a gate. It may inform a phase; it may not block one.
**Plans**: TBD

### Phase 21: Generate the Claim Surface

**Goal**: Eliminate hand-transcribed gate documentation, which produced 41% of all review
findings across Phases 13-15. Every branch count, surface list and disclosed bound is currently
copied by hand into up to five places with nothing checking they agree.

**Depends on**: 17, 18, 19, 20

**Dependency rationale**: L1 closes first; this is the explicit ordering commitment of this
milestone. The direct edge to 18 is independently forced by `CLAUDE.md`'s CI-gate table (18 moves
the battery 24 → 25 and adds the `CONF-GATE` row; 21 regenerates that table) and by `CONF-GATE`
itself needing a `--describe` limb.

**Requirements**: CONF-11, CONF-12, CONF-13

**Success Criteria**:

  1. Every registered gate script supports `--describe`, emitting its own documentation row from
     its live constants (branch counts, registered surfaces, disclosed bounds).

  2. `CLAUDE.md`'s CI-gate table and `docs/ARCHITECTURE.md`'s inventory are generated from those
     emissions; a gate fails when committed text ≠ emitted text.

  3. Per-gate detail moves to `docs/gates/<GATE-ID>.md`. No table cell exceeds 2,000 characters —
     today QUAL-01's is 22,626 on a single line, which git cannot diff and no reviewer can read.

  4. Hand-maintained branch-count literals in prose → 0, verified by a check that fails if one
     reappears. A deliberately partial pattern sweep finds 9 across `CLAUDE.md`,
     `docs/ARCHITECTURE.md` and `check-selfaudit-scan.py`'s docstring; spelled-out forms
     ("fifty-eight to seventy-two", "eighty-six", "ninety-four") are not covered by that sweep, so
     the true count is higher. Establishing the real figure is this criterion's first task.
**Plans**: TBD

### Phase 22: Cap the Recursion

**Goal**: Give the project a written stopping rule, and dispose of the accumulated meta-guard
backlog by decision rather than a fifth round of point fixes — which is what the Phase 15
verifier explicitly recommended and no one was empowered to do.

**Depends on**: 21

**Dependency rationale**: This phase hand-writes the depth rule into `CLAUDE.md`, which Phase 21
generates; reversing the order would have the generator clobber it.

**Requirements**: CONF-14, CONF-15

**Success Criteria**:

  1. The depth rule — "a guard guards the product; a guard is not itself guarded" — is stated in
     `CLAUDE.md` and `CONTRIBUTING.md`, with the `999.27 → 999.28 → 999.30` chain cited as the
     measured justification.

  2. Backlog 999.30 and 999.31 each carry a recorded terminal disposition: closed-by-decision
     under the depth rule, or promoted with a written bound. Neither remains open-and-unowned.

  3. The review protocol distinguishes product findings (block the phase) from apparatus findings
     (auto-file to backlog, never block), and `/bm:code-review`'s output reflects the split.

  4. A phase-level rework cap is written down: more than 2 gap-closure plans halts the phase and
     forces a replan. Phase 13 would have stopped at plan 6 rather than 28.
**Plans**: TBD

### Phase 23: Ship v9.0.0

**Goal**: Release the milestone in lockstep, the way every prior ship phase has — and discharge
the disclosure `SHIP-05` made on this milestone's behalf in the `[8.26.0]` entry.

**Depends on**: 22

**Dependency rationale**: Total order upstream; REL-02 additionally requires `CONF-GATE` (from
Phase 18) and every Phase 21/22 control registered.

**Requirements**: REL-01, REL-02, REL-03, REL-04

**Success Criteria** (observable, mechanically checkable):

  1. All 17 hand-maintained version stamps read `9.0.0`; VERSION-01 green; `sync-content.py
     --check` clean.

  2. `check-firewall-battery.sh` reports GREEN with `CONF-GATE` and every Phase 21/22 control
     registered, and every surface stating the gate count agrees with what it runs.

  3. This milestone's requirements are registered as matrix rows and the coverage-headline move
     is produced by `HEADLINE-LOCK`'s sweep, not a hand edit.

  4. `CHANGELOG.md` carries a `[9.0.0]` entry that closes the SHIP-05 disclosure by name: it
     restates the v8.26.0 figures and gives the post-fix reading beside each, so the two entries
     read as one before/after pair rather than two unrelated snapshots.

  5. `docs/conformance-baseline.md` carries its final post-milestone reading, and the
     marked-claim residual is stated as the ratchet's standing value.
**Plans**: TBD

---

## Active Milestone

**v9.0.0 — Conformance** — Phases 17-23, in progress. Started 2026-09-04, roadmap approved the
same day from `.planning/PROPOSAL-L1-first-milestone-2026-09-04.md` §2. L1 (Phases 17-20) must
complete before L2 (Phase 21) and L3 (Phase 22) begin. Next: `/bm:discuss-phase 17` →
`/bm:plan-phase 17`.

---

## Backlog

Unsequenced parking lot. 999.2-999.4 come from the 2026-08-31 traceability-hardening review,
which found that **every column `detect_defects` emits scores form, not fact**: `untraced_claims`
tests whether a claim contains the substring `C1` and never opens the chain, and
`build_judge_packet` writes exactly two files, so the blind judge never sees the run's tool calls.
Ordered P1 → P4 by value-to-cost against the stated goal: trace claims from fact, not
hallucination.

(P0 of that review — documenting what each TSV column actually tests — is not filed here; it is
a docs task, not a phase.)

**999.1 (P1) shipped as milestone v8.24.0, Phases 4-6** (promoted 2026-08-31, archived the same
day). The clause "nothing in the stack can falsify a `*Provenance: read-at-source*` label" that
motivated this whole review is **no longer true** — PROV-GUARD falsifies it. 999.2-999.4 remain
parked and were explicitly out of that milestone's scope.

**999.6 and 999.3 shipped as milestone v8.25.0, Phases 10-12** (promoted 2026-08-31, archived
2026-09-02). Constraint 3 held: 999.6 landed as Phase 10 and then swept v8.25.0's own
`161/91/0/252 → 174/92/0/266` headline move, so the fourth hand-sweep never happened. Constraint
4 is now satisfied — 999.3 shipped, so a 999.2 corpus built from here on is no longer stale in
its rendering the moment the contract lands. **Wave 3 is next.**

999.5 and 999.6 were filed *during* v8.24.0, from its own code reviews: 999.5 by phase 4's review
(two pre-existing warnings neither gap-closure plan was scoped to touch), 999.6 by phase 6's
(the coverage headline has now been fixed by hand three times — v8.18 `07520b8`, v8.24 `c2da6e2`
and `b034005` — because no gate covers it).

999.7-999.10 were filed *after* v8.24.0 shipped, from the first matched-pair comparison in the
PR-P1 series: run 4 on a verified 8.24.0 body against run 3 on 8.23.0, written up as GAP-8 through
GAP-11 in `tests/premise-rejection-catalog.md`. The premise axis passed a fourth time and every
other column moved the wrong way — **three of the four causes are instrument defects, not analysis
defects.** 999.7 is the priority: it is the only one in a shipped CI gate and the only one that
fails green. 999.9 and 999.10 overlap 999.3 by construction and were folded into it at
`/bm:review-backlog` 2026-08-31 — they are no longer separately schedulable.

999.11 was filed by 999.7's own work — the reach widening let PROV-GUARD read an analysis that
renders currency differently from the committed fixture, exposing a literal-matching policy that
had never been measured. 999.12 and 999.13 are not new findings at all: they are MEAS-01 and
MEAS-02, deferred v2 requirements carried in `PROJECT.md`'s candidate prose since v8.18.0 and
given numbered entries here on 2026-08-31 so they sit inside the resolution order rather than
beside it. Neither has a matrix row, so promoting either moves the coverage headline.

**999.18-999.21 were filed 2026-09-02 from the first v8.25.0 PR-P1 run** — the first measurement
taken *after* 999.3 shipped, capture and scores staged at
`.planning/captures/pr-p1-v8.25.0-2026-09-02/`. They are **unsequenced**: the resolution order
above was determined across twelve entries and has not been re-run over these four. Three of them
(999.18, 999.19, 999.20) are one causal chain — two contract holes and the scan that would have
caught both — and 999.20 is explicitly gated on the other two. 999.21 is a sibling of 999.11 and
belongs beside it. Sequencing them is `/bm:review-backlog`'s job, not this note's.

**Reviewed `/bm:review-backlog` 2026-09-02 — three decisions settled, nothing promoted** (there is
still no active milestone; opening one belongs to `/bm:new-milestone`). (1) **Proposed scope for the
next milestone: 999.18, 999.19, 999.20, in that order** — one causal chain, two contract holes plus
the scan that would have caught both, with 999.20 already gated on the other two and 999.17's pin
folded into 999.18's close. This takes precedence over the previously-ordered wave 3; the reasoning
is that 999.3 proved the contract branch works and these three are its unenumerated cases, measured
rather than predicted. (2) 999.21 merged into 999.11 as Case B. (3) 999.17 merged into 999.18 as its
closing step. Two entries also had ROADMAP rows but no phase directory — 999.16 and 999.17 — which
would have failed `/bm:discuss-phase`; both created, and 999.17's removed again on merge.

### Resolution order (determined 2026-08-31 across nine; revised same day to twelve; reviewed 2026-08-31)

Twelve items, **five shipped** (999.5, 999.7, 999.8, and — at v8.25.0 — 999.6 and 999.3), leaving **five units of work** across seven
open entries — 999.9 and 999.10 are now formally absorbed into 999.3, and 999.4 is conditional
rather than scheduled. Ordered by what unblocks or protects what, not by severity alone; the five
dependencies below are the only hard constraints, and everything else is value-to-cost within them.

*Revision note: the original order covered 999.2-999.10. 999.11 was filed by 999.7's own work and
999.12/999.13 promote the long-deferred MEAS-01/MEAS-02 out of `PROJECT.md`'s candidate prose into
numbered entries; all three are placed below rather than left outside the ordering.*

*Review note (`/bm:review-backlog`, 2026-08-31): nothing was promoted — there is no active
milestone to promote into, and opening one belongs to `/bm:new-milestone`. Three decisions were
settled and are now recorded in the entries themselves rather than left as open questions in this
prose: (1) 999.9 and 999.10 merge into 999.3 as its two worked cases; (2) 999.4 is CONDITIONAL,
gated on 999.2's measured false-negative rate, with "close unrun" an accepted outcome; (3) the
stale records were corrected — 999.5's Wave 1 row now reads DONE, and the shipped 999.7/999.8
phase directories were removed to match 999.5's precedent. **Proposed scope for the next
milestone: 999.6, then the merged 999.3.** That pairing is forced, not preferred — 999.6 is
constraint 3 and 999.3 is the first work that registers matrix rows.*

**Hard constraints, each one non-obvious:**

1. **999.8 before any measurement.** While the bold-label guard is wrong, `_dependency_cycles` and
   `_ungrounded_chains` are unreadable on any bold-labelled analysis — so every reading taken
   before it is fixed may be contaminated, including 999.2's corpus scoring.

2. **999.5 before any phase that dispatches paid live runs.** `--probe`'s
   `_extract_and_persist_analysis` call has no `try/except`, so a completed-but-unextractable
   capture ends a *paid* run in a bare traceback. 999.3's verification and 999.2's corpus build
   are both live-run-heavy.

3. **999.6 before the next milestone that moves the coverage headline.** Every wave below
   registers matrix rows and therefore moves it. Landing the gate afterwards is the fourth
   hand-sweep of a class already swept three times.

4. **999.3 before 999.2.** 999.3 changes what the agent emits; a corpus built first is stale in
   its rendering the moment 999.3 lands.

5. **999.3 and 999.2 before 999.13 (MEAS-02).** Not a sequencing preference — an instrument-trust
   prerequisite. MEAS-02 scores the quality harness's defect columns, and GAP-8..GAP-11 measured
   those columns reading *form rather than substance*. An A/B run through an instrument that
   scores rendering would attribute a rendering difference to the intervention. 999.3 stabilises
   the form; 999.2 measures what the detector still misses.

**Wave 1 — clear and protect the instrument.** All four are small, and each one protects the work
that follows rather than delivering user-visible value itself.

| # | Phase | Why here |
|---|---|---|
| 1 | ~~**999.8** Chain-label guard~~ **DONE** | Smallest item in the backlog; fix is prototyped and measured non-moving on run 3 and the frozen corpus. Only the controls remain. Constraint 1. |
| 2 | ~~**999.7** PROV-GUARD floor~~ **DONE** | Highest severity in the backlog — the only item in a shipped CI gate and the only one that fails **green**. Every green build is partly meaningless while it stands. Its own internal order (floor, then regex reach) is in its entry. |
| 3 | ~~**999.5** Probe hardening~~ **DONE** | Constraint 2. Cheap insurance bought before the waves that spend money. |
| 4 | ~~**999.6** Headline gate~~ **DONE** | Constraint 3. Shipped as v8.25.0 Phase 10, and it swept that milestone's own headline move — the constraint was satisfied by the milestone that would otherwise have violated it. |

**Wave 2 — fix the cause.**

| # | Phase | Why here |
|---|---|---|
| 5 | ~~**999.3** Rendering contract~~ **DONE** *(absorbed 999.9 + 999.10)* | The highest-leverage item in the backlog: the under-specified emission form is the upstream cause of GAP-5, GAP-6, GAP-7, GAP-9 **and** GAP-10. 999.9 and 999.10 supply the two worked cases that make 999.3 concrete and give it acceptance tests; running 999.3 without them means re-deriving both. |

**Wave 3 — measure what is left.**

| # | Phase | Why here |
|---|---|---|
| 6 | **999.2** Adversarial corpus | Constraint 4. Also the decision input for whether 999.4 is worth building at all. **Displaced by the 2026-09-02 review** — the contract chain 999.18-999.20 is proposed ahead of this wave. |
| 7 | **999.11** Matching policy *(absorbed 999.21)* | Directly after 999.2, as its own entry sequences it: neither case carries a recorded measurement, and the corpus is the instrument for measuring whether loosening costs a real detection. The 2026-09-02 run showed Case A's failure is nondeterministic per fetch, which makes the corpus a hard prerequisite rather than a convenience. |
| 8 | **999.4** Semantic judging *(CONDITIONAL)* | Not scheduled — gated on 999.2's measured false-negative rate, decided 2026-08-31. Sequenced here only for the case where the gate opens. See the caveat below. |

**Wave 4 — measure the behaviour, not the form.** The standing answer to "structural gates are not
behavioural gates". Both were deferred at v8.18.0 for reasons that have since changed, and both
are subject to the standing rule that a live K-of-N verdict is a recorded observation and never a
gate.

| # | Phase | Why here |
|---|---|---|
| 9 | **999.12** MEAS-01, live acquisition harness | Its v8.18.0 deferral reason — no consumer for a fresh baseline — is weaker now that PROV-GUARD reads captures. **Re-derive the scope before scoping the work**: part of the original question may already be answered from stored captures, which would make this materially smaller than filed. |
| 10 | **999.13** MEAS-02, quality A/B | Constraint 5. Its original blocker (the behaviour had not shipped) is gone; instrument trust replaced it. Genuinely last: it is the only item that asks whether the v8.18.0 Act limb was *worth* shipping, and it cannot be answered through an instrument that is still being repaired. |

**999.4 may never be worth running, and that is a legitimate outcome — now recorded as its entry's CONDITIONAL gate rather than left as advice here.** It is the only
non-deterministic item in the backlog and the most expensive. 999.2 measures the false-negative
rate mechanically; if that rate is low, the case for an LLM judge over claim-to-chain
correspondence largely evaporates. Treat 999.2's result as the gate on 999.4 rather than
scheduling 999.4 unconditionally.

**One open decision remains inside wave 2, and the merge did not settle it.** 999.3's Case A (was
999.9) admits two resolutions: (a) state the no-wrap rule on both surfaces, or (b) teach
`_chain_block_well_formed`'s join bracket-awareness. Option (b) is the detector widening 999.3 was
filed to resist — so if the phase resolves toward (b), 999.3's goal statement must be amended
rather than quietly contradicted. This is a phase-scoping question, deliberately left open at
`/bm:review-backlog` 2026-08-31 rather than pre-decided here: it should be answered by
`/bm:discuss-phase` with the code in front of it, and whoever answers it must first read
`_chain_block_well_formed`'s Phase 184-03/184-04 history, where a head-arrow guard was tried and
reverted for keying on where the line break fell rather than on whether the absorbed line belonged
to the same claim.

### Phase 999.2: Adversarial corpus of well-formed but false analyses (PROMOTED 2026-09-04 to v9.0.0 Phase 19)

**Goal:** Measure the detector's false-negative rate. Build a corpus of analyses that are
structurally impeccable and substantively wrong, score them, and treat everything that passes
clean as a hole.

**Why:** three live runs produced five instrument-level defects, three fixed by *widening* the
detector to accept what the agent did. Widening only ever loosens, and nobody has measured
whether this detector still catches a bad analysis. First case to seed: a closure ledger that
quotes each claim while citing arbitrary chains — LEDGER-01 credits a cited chain for *existing*,
never for *supporting* the claim.

**Requirements:** TBD
**Plans:** 0 plans

Plans:

- [ ] TBD (promote with /bm:review-backlog when ready)

---

### Phase 999.3: Tighten the output template instead of widening the detector (SHIPPED 2026-09-02 as v8.25.0, Phase 11 — absorbed 999.9 and 999.10)

**Goal:** Stop the widening treadmill at its source. Make `output-template.md` §4 and §6
prescriptive enough to be mechanically checkable — the exact chain rendering, the exact citation
form, and what is non-conforming — so the agent stops varying and the detector stops guessing.

**Why:** the treadmill exists because the form is under-specified, so every legitimate variation
the agent produces reads as a defect. v8.22's arrow-led wrap fix is the proof this works: the
agent complied once told, and that fix held on run 3.

**Merge settled at `/bm:review-backlog` 2026-08-31.** 999.9 and 999.10 are absorbed as this
phase's two worked cases; they are no longer separately schedulable. They supply the concrete
acceptance tests without which 999.3 is an abstract "be more prescriptive" — running the contract
work alone would mean re-deriving both from GAP-9 and GAP-10. Their full findings stay in their
own entries below rather than being duplicated here.

- **Case A — chain hop wrapping** (was 999.9, GAP-9). May a single derivation hop wrap across
  physical lines? Both surfaces state the rule as *every line after the head begins with `→`*,
  satisfiable only by never breaking a hop. Neither says so. **This case still carries the one
  open design decision — see the note under the wave tables.**

- **Case B — verdict expiry form** (was 999.10, GAP-10). A worked example showing a
  `current constraint` row recording its expiry at the point of use. Run 3 already demonstrated
  the vocabulary adequate, so this is an example, not a schema change.

Acceptance: each case is closed by a stated rule on both canonical surfaces **plus** a control
that fails if the rule is dropped — not by widening a detector to accept what run 4 happened
to emit.

**Requirements:** TBD
**Plans:** 0 plans

Plans:

- [ ] TBD (promote with /bm:review-backlog when ready)

---

### Phase 999.4: Semantic claim-to-chain correspondence judging (BACKLOG — CONDITIONAL)

**Goal:** The real version of `untraced_claims` — does the chain a claim cites actually support
it? Needs an LLM judge given the derivation chains alongside the claim, not the citation-presence
substring test that ships today.

**Why last:** expensive and non-deterministic, and 999.1 (now v8.24.0) removes the more damaging failure mode
far more cheaply. Fabricated facts beat invalid inference on both damage and detection cost.

**CONDITIONAL — decided at `/bm:review-backlog` 2026-08-31.** This phase is not scheduled; it is
*gated on 999.2's measured result*, and closing it unrun is an accepted outcome, not an
abandonment.

- **Gate:** the false-negative rate 999.2 measures mechanically over the adversarial corpus.
- **Low rate → close unrun.** Record the measurement as the reason. If a mechanical detector
  already catches structurally-impeccable-but-false analyses at an acceptable rate, the case for
  an LLM judge over claim-to-chain correspondence largely evaporates, and the only remaining
  argument for it is that it is the *theoretically* right check — which does not by itself buy a
  non-deterministic, expensive instrument.

- **High rate → promote**, with the corpus doubling as its validation set.

Do not schedule this before 999.2 reports. The point of the gate is that the decision input does
not exist yet.

**Requirements:** TBD
**Plans:** 0 plans

Plans:

- [ ] TBD (promote with /bm:review-backlog when ready)

---

### Phase 999.5: Harden `_extract_and_persist_analysis`'s failure and write paths (DONE 2026-08-31)

**Goal:** Close the two pre-existing warnings phase 4's code review reproduced but neither
gap-closure plan was scoped to touch (`04-REVIEW.md`, 2026-08-31).

**Why:** both are silent-cost defects in verification infrastructure, not style. (a) `--probe`'s
call to `_extract_and_persist_analysis` has no `try/except`, so a completed-but-unextractable
capture ends a *paid live run* in a bare traceback — reproduced against `gen-stub-only.jsonl`.
(b) the persistence write has no symlink/frozen-path guard; the WR-01 untracked-file sweep
mitigates the silent half, but the write itself is still unguarded. Neither was named in either
phase-4 gap's `missing:` list, neither contradicts a phase-4 success criterion, and both leave
the raw `.jsonl` safely on disk in every failure case they describe — which is why phase 4
verified `passed` at 7/7 with these open.

**Shipped 2026-08-31**, both halves, direct to master (not promoted through
`/bm:review-backlog` — the review had already reproduced both defects and prescribed both
fixes; same disposition as 999.7 and 999.8). Commit `003d047`. Battery GREEN 23/23.

(a) WR-A — the decision now lives in `_persist_or_diagnose_analysis`, a function rather than
an inline `try`, for the reason `_persist_or_refuse_analysis`'s clause (a) records about
CR-02: a decision inline in `main()` cannot be self-tested without a live `claude`, and
`--probe` is the least testable block in the file precisely because everything above it costs
money. It returns `(path, message, status)`; the non-zero status on a failed persist is what
makes the diagnosis actionable, since a diagnosis printed on a `0` exit is invisible to any
caller that branches on the status.

(b) WR-B — both guards, not just the symlink half the review called "the cheap,
self-contained part". The review left the frozen half undone because a shared `_FROZEN_PATHS`
source did not exist on the Python side; rather than restate the list and create a drift
hazard, the guard **parses it out of `scripts/check-firewall-battery.sh`** — the same file
`check-registration.py` already parses for its gate registrations. It fails closed on every
read or parse failure, because "I could not read the list" is not "nothing is frozen".

**Two deviations from the review's prescribed fixes, both deliberate.** The review's snippet
raised `AgentAnalysisExtractionError` for the symlink refusal; this ships a new
`AnalysisWriteRefused` instead, on the same reasoning clause (c) of the wrapped helper's
docstring already states — an extraction error means the capture cannot be read, a write
refusal means it read perfectly and the *destination* was refused, and collapsing them
destroys the information a caller would act on. Reusing the existing type would also have made
the new failure indistinguishable from a guardrail failure at both call sites. Second: the
review scoped WR-A to `--probe`, but `--single` reaches the same new refusal, so
`_persist_or_refuse_analysis` converts `AnalysisWriteRefused` into a refusal tuple while
still propagating both guardrail errors untouched. That asymmetry is asserted in both
directions (control 13) so it cannot decay into a blanket `except`.

**Control 5 drives the real committed tree on purpose** and is safe either way: item 20
control 1 already pins that this extraction reproduces `PR-P1.md` byte-identically, so a
broken guard rewrites identical content and cannot trip FROZEN-EVIDENCE. Confirmed — `tests/`
stayed clean across all 11 injected faults.

**Requirements:** covered by QUAL-01 Item 23 (13 controls, 11 fault injections)
**Plans:** shipped without a plan document

---

### Phase 999.6: Gate the coverage headline on every surface that states it (SHIPPED 2026-09-02 as v8.25.0, Phase 10)

**Goal:** Make a gate — not a manual sweep — keep the published coverage headline consistent
across every file that states it.

**Why:** phase 6's CR-01 shipped `CLAUDE.md` self-contradictory about the headline
(`147/90/0/237` vs the authoritative `161/91/0/252`) with the battery GREEN at 23/23, because
`HEADLINE-LOCK` scans only `docs/requirements-traceability.md` and the two tracked artifacts.
The fix pass swept five surfaces by hand, and phase 6's own residual-drift sweep had already
reported `SWEEP CLEAN` over the surface it missed. Nothing gates `CLAUDE.md`'s headline today,
so the identical defect recurs at the next milestone that moves the number — this is the third
time this class has been fixed by sweeping (v8.18 `07520b8`, v8.24 `c2da6e2`/`b034005`).

**Fix:** widen `_self_test_headline_lock`'s scanned surfaces to every file that states the
headline (`CLAUDE.md`'s Requirements-surface section at minimum), with a non-vacuity control
per surface. Sweeping is the symptom fix; the gate is the cause fix.

**Requirements:** TBD
**Plans:** 0 plans

Plans:

- [ ] TBD (promote with /bm:review-backlog when ready)

---

### Phase 999.7: Zero-coverage floor for PROV-GUARD (DONE 2026-08-31)

**Goal:** Make it impossible for `check-provenance.py` to return PASS having read nothing. An
analysis yielding zero parsed ground truths — or zero provenance labels against a capture that
contains fetches — must fail, not pass. Then widen `_GT_LINE_RE`, `_READ_AT_SOURCE_LABEL` and
`_source_string` to reach renderings the committed fixture does not use.

**Why (highest priority of 999.7-999.10):** this is a defect in a **shipped CI gate**, and it
fails green. Measured on PR-P1 run 4 (GAP-11): the gate returned `provenance_labels 0,
literals_checked 0, provenance_flag 0` — PASS — on a section 3 holding sixteen ground truths,
twelve of them `read-at-source` labelled and every cited source actually fetched. Three
independent form dependencies caused it: `_GT_LINE_RE` requires a `- ` bullet (run 4 used `1. `),
`_READ_AT_SOURCE_LABEL` requires the period *inside* the emphasis, and `_source_string` expects
the fixture's `— source: <url>; read-at-source: <location>` clause shape. Neither leg can observe
any of them — the live leg reads one fixture in one rendering, and all 24 self-test controls are
built by `_gt_line`, which emits that same rendering for positive and negative controls alike.

The floor is deliberately ordered **before** the regex widening: it is independent of how many
renderings the parser accepts, and it converts every future rendering surprise from a silent pass
into a loud failure. Widening without it just moves the blind spot.

Same failure direction as GAP-5 (silently green), and it partially undercuts the claim in
`CLAUDE.md` and `tests/quality-provenance-v8.24/README.md` that PROV-GUARD "can falsify a
`read-at-source` label" — true only for analyses rendered like the fixture. Worth re-stating that
claim's scope as part of this phase.

Full finding: `tests/premise-rejection-catalog.md`, GAP-11 — FIXED.

**Shipped 2026-08-31**, both halves, floor first. `coverage_floor_breach` feeds `provenance_flag`
on two conditions (zero parsed GTs; zero labels AND at least one retrieved source), and the three
form dependencies are widened. Controls 24 -> 32, eight fault injections. Committed fixture
unchanged at 7/7 sources and 35/35 literals. Battery GREEN 23/23.

Run 4 moves from `provenance_flag=0` (PASS, having read nothing) to `flag=1` with 12 labels read,
15 literals checked, 5 named unbindable citations and 2 unlocated literals. One of the five —
GT-12, `accounting identity; irreducible by definition` — is a genuine agent defect: a definitional
identity labelled `read-at-source` when nothing was read.

Two things came out of the work that were not in its scope, both recorded rather than absorbed:
a redundant `_READ_AT_SOURCE_LABEL` branch that made the period widening unfalsifiable (removed,
`_PROVENANCE_LABEL_RE` is now the single authority), and the currency-sigil false positive now
filed as **999.11**.

**Requirements:** covered by PROV-GUARD controls FLOOR-* and REACH-*
**Plans:** shipped without a plan document

---

### Phase 999.8: Chain-label self-reference guard covers bold labels (DONE 2026-08-31)

**Goal:** Widen `_chain_head_refs`'s label-skip guard from `s.startswith("#")` to also skip a
`_CHAIN_BOLD_RE` match, so a bold-labelled chain is not read as citing itself.

**Why:** smallest item in this group and already measured. `_chain_ids`/`_chain_blocks` accept
**two** label forms — `_CHAIN_HEADING_RE` (hash-led) and `_CHAIN_BOLD_RE` (bold-led) — while the
guard covers only the first. The guard's own comment predicts the resulting symptom verbatim:
*"reading it as a head would make every composing chain self-referential and report the whole
section as one cycle."* PR-P1 run 4 labelled its chains `**C1 — …**` and produced exactly that:
`_dependency_cycles` and `_ungrounded_chains` both reported all eight chains, all artifact.
Correct reasoning keyed to the wrong property — markdown heading *syntax* rather than *is this the
block's own label line*.

The one-line widening was prototyped and measured: run 4 cycles 8→0, ungrounded 8→0, self-audit
disagreements 3→2 (the survivor is 999.9's, correctly); run 3 unchanged; all six frozen v8.7
analyses unchanged on every column, `malformed [2, 2, 2, 2, 3, 3]` still matching
`_CALIBRATION_MALFORMED_CHAIN_BLOCKS`. **The missing work is the controls, not the line** — a
positive control on a bold-labelled composing chain, and an anti-overreach control proving a
genuinely bold-led *head* line is not swallowed.

Failure direction is false-positive, so this hides nothing and is not urgent — but it is cheap and
it currently makes run 4's dependency columns unreadable.

Full finding: `tests/premise-rejection-catalog.md`, GAP-8.

**Shipped 2026-08-31**, direct to master (not promoted through `/bm:review-backlog` — the fix
was already measured and the phase was one guard plus its controls). `_chain_head_refs` skips the
bold label at the block's own first line; QUAL-01 self-test Item 22
(`_selftest_gap8_bold_chain_labels`) carries six controls and three fault injections. Battery
GREEN 23/23.

**The recorded fix direction was wrong and the anti-overreach control is what caught it.** The
blanket `_CHAIN_BOLD_RE.match(s)` widening measured in the finding would have swallowed a
fully-bolded *head* line, since `_CHAIN_BOLD_RE`'s label alternation matches `GT-1`. Shipped
narrowed to `idx == 0`. Full record in `tests/premise-rejection-catalog.md`, GAP-8 — FIXED.

**Requirements:** covered by QUAL-01 Item 22
**Plans:** shipped without a plan document

---

### Phase 999.9: Chain hop wrapping contract (MERGED INTO 999.3 — 2026-08-31)

**Not separately schedulable.** Absorbed as Phase 999.3's Case A at `/bm:review-backlog`
2026-08-31. The finding below is retained in full because 999.3 references it rather than
duplicating it — including the open (a)/(b) decision and the Phase 184-03/184-04 warning, both
of which the merged phase must read before touching `_chain_block_well_formed`.

**Goal:** Decide and document whether a single derivation hop may wrap across physical lines, and
make the detector and both canonical surfaces agree with the decision. Either (a) state the
no-wrap rule explicitly in `SKILL-body.md` §4 and `output-template.md` §4, or (b) teach
`_chain_block_well_formed`'s bounded join to absorb a continuation inside an unclosed `[`.

**Why:** the rule as written is unimplementable for a long intermediate, and which runs pass is
currently decided by an undocumented rendering preference. `_chain_block_well_formed` absorbs a
following line only while it is arrow-led, and `_CHAIN_FORM_LINE_RE` then requires two arrows in
the joined candidate — so a wrapped hop emits a non-arrow-led continuation, the join stops, and
the candidate keeps one arrow. Both surfaces state the rule as *every line after the head begins
with `→`*, which is literally true and satisfiable only by never breaking a hop across lines.
Neither says so.

Measured: crossing head form against wrap over four minimal probes, **both** prescribed head forms
pass unwrapped and fail wrapped — so the `SKILL-body.md:208` / `output-template.md:131` head-form
difference is real but is **not** the cause here (it should still be reconciled on its own
merits). PR-P1 run 3 passed with 0/5 malformed by emitting 479-character unwrapped lines; run 4
failed 8/8 by wrapping near 90 columns. Neither was told which to do, and that is the entire delta
on this axis.

**Cross-reference: this is the concrete seed case Phase 999.3 was filed for** ("tighten the output
template instead of widening the detector"). Option (a) is squarely 999.3's thesis; option (b) is
the widening 999.3 exists to resist. Consider merging this into 999.3 at `/bm:review-backlog`
rather than running both. If (b) is attempted, read `_chain_block_well_formed`'s Phase
184-03/184-04 history first — a head-arrow guard was tried and reverted for keying on *where the
line break fell* rather than on whether the absorbed line belonged to the same claim.

Full finding: `tests/premise-rejection-catalog.md`, GAP-9.

**Requirements:** TBD
**Plans:** 0 plans

Plans:

- [ ] TBD (promote with /bm:review-backlog when ready)

---

### Phase 999.10: Verdict expiry form for `current constraint` rows (MERGED INTO 999.3 — 2026-08-31)

**Not separately schedulable.** Absorbed as Phase 999.3's Case B at `/bm:review-backlog`
2026-08-31. The finding below is retained in full because 999.3 references it rather than
duplicating it — in particular the run-3 evidence that the vocabulary is already adequate, which
is what makes this a worked example rather than a `_VERDICT_VOCAB` widening.

**Goal:** Give the Verdict Vocabulary a worked example showing how a `current constraint` row
records its expiry — `Accept — expires at <condition>` — at the point of use.

**Why:** the only one of GAP-8..GAP-11 that is an **agent deviation rather than an instrument
defect**, and the cheapest to close. PR-P1 run 4 wrote `**Accept with expiry** — …` on all three
of its `current constraint` rows, a fourth token `_VERDICT_VOCAB` does not define, so all three
cells are non-conforming and Criterion 2's **Rigorous** self-audit was correctly contradicted (its
justification asserts *"Verdicts lead with Accept/Challenge/Discard"*, false for three of its own
24 rows).

It first reads as a hole in the contract — `current constraint`'s prescribed treatment is *"record
the expiry conditions"* and no verdict token names that. **Run 3 refutes that reading:** on the
same prompt it carried four `current constraint` rows and rendered every one conformingly, putting
the expiry in the justification (`**Accept** — expires at term end (1 or 3 years)`). The
vocabulary is adequate and was demonstrated adequate one milestone earlier; run 4 moved the
qualifier into the token slot, three times.

So the fix is a worked example, not a schema change. Widening `_VERDICT_VOCAB` is the more
expensive option — it moves the 267-cell census `_VERDICT_FORM_RE`'s separator policy is
calibrated against — and run 3 is the evidence it is unnecessary.

**Cross-reference: overlaps Phase 999.3** (template prescriptiveness) and is small enough to fold
into it. Also worth pairing with 999.9 — both are "the emitted rendering contract is
under-specified at the point of use."

Full finding: `tests/premise-rejection-catalog.md`, GAP-10.

**Requirements:** TBD
**Plans:** 0 plans

Plans:

- [ ] TBD (promote with /bm:review-backlog when ready)

### Phase 999.11: Decide PROV-GUARD's matching policy — sigil and anaphoric source (BACKLOG — absorbed 999.21)

**Merge settled at `/bm:review-backlog` 2026-09-02.** 999.21 is absorbed as this phase's second
worked case; it is no longer separately schedulable. Both cases are the same question on the same
gate — an unmeasured matching policy meeting a rendering the contract never forbade — and both must
name explicitly whether they resolved on the **contract** branch (state the rule, 999.3's lineage)
or the **detector** branch (loosen the join, the widening 999.3 was filed to resist). 999.21's full
finding stays in its own entry below rather than being duplicated here.

- **Case A — currency sigil** (the original entry, GAP-12). Below.
- **Case B — anaphoric source** (was 999.21). `*Provenance: read-at-source* — same page` on 3 of 10
  labels in the 2026-09-02 run; `_join_key`/`_bind` cannot resolve it, so `provenance_flag` raises
  to 1 on a run scoring 11/11 literals located.

**Goal (Case A):** Decide whether `verify`'s literal comparison should normalize a leading `$` the
way it normalizes commas, and pin the decision with a control either way.

**Goal (Case B):** Decide whether an anaphoric source string (`same page` and equivalents) is legal
in a `read-at-source` label — require a resolvable source per GT, or teach the joiner to resolve the
reference against the nearest preceding labelled GT — and pin the decision with a control either
way. Full evidence in the 999.21 entry below.

**Why:** currently it does not — *"'$' is never stripped"* — and that produces false positives on
real output. Measured on PR-P1 run 4 (GAP-12): `$0.000011244` and `$0.000001235` both report
unlocated, and both appear in the retrieved `aws.amazon.com/fargate/pricing` text as
`"0.000011244 per vCPU second"` and `"0.000001235 per GB per second"`. The numbers were read at
source exactly as claimed; only the sigil differs.

**Why it is a decision and not a fix:** normalizing loosens the check symmetrically — a bare `42`
would then match `$42`, and a misattribution between a count and a price gets harder to see. The
current policy is the stricter of the two and its cost was invisible until the 999.7 reach
widening let the gate read an analysis that renders currency differently from the fixture.

**Why it needs 999.2 first:** unlike the whole-span matching rejected in the module docstring's
limitation 3, this policy carries **no recorded measurement** — it is stated in `verify`'s
docstring, pinned by no control, and every literal in the committed fixture matches under either
rule. The adversarial corpus is the instrument for measuring whether a loosening costs a real
detection. Sequence this after 999.2, not before.

Full finding: `tests/premise-rejection-catalog.md`, GAP-12.

**New evidence, 2026-09-02 (v8.25.0 PR-P1 run) — the failure mode is nondeterministic per fetch,
not per analysis.** GAP-12's two literals (`$0.000011244`, `$0.000001235`) scored **located** in
this run: the bound `aws.amazon.com/fargate/pricing` fetch returned them *with* the sigil. The same
run fetched that same URL a second time and got the sigil-less rendering GAP-12 describes
(`"0.000011244 per vCPU second"`). One run, one URL, both renderings. Consequence for scoping: a
fix cannot be validated against a fresh capture — whether it fires depends on which rendering the
page returned that minute — so this needs a pinned fixture or the 999.2 corpus to be testable at
all. That strengthens the existing "sequence after 999.2" rather than changing it. Capture:
`.planning/captures/pr-p1-v8.25.0-2026-09-02/`.

**Requirements:** TBD
**Plans:** 0 plans

Plans:

- [ ] TBD (promote with /bm:review-backlog when ready)

---

### Phase 999.12: MEAS-01 — live harness for evidence acquisition (PROMOTED 2026-09-04 to v9.0.0 Phase 20)

**Goal:** Measure whether the agent *actually performs* the Phase 3 read when a source is
reachable, as opposed to HARN-01's structural question of whether the step exists in the emitted
tree.

**Why:** this is half of the standing answer to "structural gates are not behavioural gates".
HARN-01, HC-BOUND and the rest of the battery assert that named prose is present, well-formed and
cannot be silently stripped. None of them observes a run. The v8.18.0 record states the
distinction in its own words and defers this deliberately, not by oversight
(`docs/v8.18-praor-loop-closure.md` §3 and §7).

**Why it was deferred, and what has changed since.** The recorded reason (v8.18.0, 2026-08-2x)
was that K-of-5 live results are recorded observations and never gates — the standing governing
record, §2 item 3 of `docs/v8.7-constraint-teardown.md` — so building the harness then would have
meant a fresh baseline freeze with **no immediate consumer**. That premise is now weaker: v8.24.0
shipped PROV-GUARD, which reads a stored `.jsonl` capture and joins each `*Provenance:
read-at-source*` label to a real `WebFetch`/`Read` of that source, and 999.7 added a coverage
floor that fires when an analysis carries zero labels against a capture that *does* hold fetches.
Between them they already answer part of MEAS-01's question on any captured run, without a live
K-of-N at all.

**So the scope needs re-deriving before this is promoted, not just scheduling.** A defensible
reading is that PROV-GUARD covers the *claimed-read* direction (a label that names a source the
run never fetched) and 999.7's floor covers the *no-labels-despite-fetches* direction, leaving
MEAS-01 responsible for the genuinely uncovered case: the agent silently **not** acquiring
evidence when a source was reachable and it made no claim either way — a false negative that
leaves no artifact in the analysis for any capture-based check to catch. That reading is this
entry's proposal, **not** a settled finding; confirm it against `check-provenance.py` at
`/bm:review-backlog` before scoping. If it holds, MEAS-01 is materially smaller than it was at
v8.18.0 and should be re-titled accordingly.

**Standing constraint:** whatever this measures, a K-of-5 verdict from it is an observation a
phase records and may not be a gate. Any new gate this phase ships must be offline and
deterministic, like every other member of the battery.

**Requirements:** MEAS-01 — a deferred v2 requirement named in prose only; it has **no matrix
row** (confirmed absent from `docs/requirements-traceability.md` and `docs/requirements-matrix.md`
2026-08-31), so promoting it registers a new row and therefore moves the coverage headline —
constraint 3 applies.
**Plans:** 0 plans

Plans:

- [ ] TBD (promote with /bm:review-backlog when ready)

---

### Phase 999.13: MEAS-02 — quality A/B for evidence acquisition (PROMOTED 2026-09-04 to v9.0.0 Phase 20)

**Goal:** Measure whether evidence acquisition actually changes analysis quality, relative to the
alternative the rubric already permits — downgrading confidence instead of acquiring the evidence.

**Why:** the other half of the structural-vs-behavioural answer, and the one that asks whether the
v8.18.0 Act limb was *worth* shipping rather than whether it is present. HC-BOUND asserts the
HIGH-confidence bound's prose exists in both rubric surfaces; nothing measures whether an agent
that reads a reachable source produces a better analysis than one that flags the input unverified.

**Why it was deferred, and what has changed since.** The recorded reason was that the behaviour
had not shipped yet — v8.18.0 was "the first to make it possible rather than the one that measures
it". **That condition is now met.** The behaviour shipped, and the PR-P1 series has produced the
first matched-pair evidence (run 4 on a verified 8.24.0 body against run 3 on 8.23.0,
`tests/premise-rejection-catalog.md`). The original blocker is gone; a different one has taken its
place.

**The new blocker is instrument trust, and it is why this sits behind wave 2 and 999.2.** The
quality harness's defect columns are what MEAS-02 would score, and GAP-8 through GAP-11 measured
those columns reading **form rather than substance** — run 4's dependency columns were entirely
artifact until 999.8, and PROV-GUARD returned a clean bill on sixteen ground truths until 999.7.
An A/B run through an instrument that scores rendering would attribute a rendering difference to
the intervention. 999.3 stabilises the form; 999.2 measures what the detector still misses. Both
are prerequisites in substance, not merely in sequence.

**Standing constraint:** same as 999.12 — a live K-of-N result is a recorded observation, never a
gate.

**Requirements:** MEAS-02 — like MEAS-01, a deferred v2 requirement with **no matrix row**;
promoting it registers one and moves the coverage headline (constraint 3).
**Plans:** 0 plans

Plans:

- [ ] TBD (promote with /bm:review-backlog when ready)

---

### Phase 999.14: Lock the meta-guards Phase 11 introduced (CLOSED 2026-09-01 by /bm:code-review 11 --fix)

**Goal:** Close the vacuity defect class where it migrated — into the registries and anchors
Phase 11's gap-closure round added to close it elsewhere.

**Why:** Phase 11 closed both of its blocking gaps, and the primary scoring path
(real file read → real detector → real assertion) is intact and exercised against the real doc
content today. What is unlocked is the *secondary* guard against a future careless edit to the
guard's own plumbing. Three reproductions, each confirmed independently by the phase's code review
and again by its verifier on disposable copies:

1. `_RENDER_PRE_CONTRACT_WORDINGS` (`scripts/check-quality-harness.py`, ~line 6708) is the only
   registry the mechanism depends on that is **not** a `_RenderRegistrySnapshot` field. It is the
   sole thing making control (l1) non-tautological — it is what plan 11-09 added to fix WR-07's
   `x in (y + x)`. Emptying it, or replacing its three entries with a one-element tautology,
   leaves `_selftest_render_contract()` returning True.

2. `_RenderRegistrySnapshot.live()` (~line 6782) projects `_RENDER_CONTRACT_EXTRACTION_TABLE` down
   to `row[0]` (the id) only. `source_file`, `habitat_mode` and `anchor` are outside the by-value
   lock: repointing `R-CITE-INLINE`'s anchor at `R-CITE-LEDGER`'s own block leaves `--self-test`
   PASSED, so control (f) would prove the ledger form twice and never prove the inline form.
   `_RENDER_FIXTURE_SHAPE`'s five non-chain ids are key-set-locked but not value-locked.

3. Consequently both `| QUAL-01 |` gate-description rows (`CLAUDE.md:165`, byte-identical in
   `docs/ARCHITECTURE.md:146`) state two guarantees the gate does not enforce — that the examples
   are extracted from `shared/spine/references/output-template.md` (nothing constrains which file
   is read, since `source_file` is unlocked) and that the registries backing legs (1) and (2) are
   membership-locked by value (item 1 above is not).

**Why it is filed rather than fixed in place:** these are durability residuals against a
hypothetical future edit, not present-tense defects. On the shipped tree today every ROADMAP
Phase 11 success criterion holds under direct inspection *and* under mutation of the primary
mechanisms — re-inserting a real contradiction phrase into `shared/spine/SKILL-body.md` is still
caught by control (i). That is the line the phase's verifier drew between this and the two
original blocking gaps, which defeated the primary path itself.

**Fix notes are already written.** `11-REVIEW-gap-closure.md`'s CR-01-new, WR-01 and WR-03 carry
directly implementable fix notes; its CR-02-new gives exact replacement prose for the doc rows.
Either close items 1-2 so the rows' claims become true, or narrow the rows to disclose which
registries remain unlocked — not both.

**CLOSED before promotion.** Filed 2026-09-01 when Phase 11's verifier parked these as minor
residuals; closed the same day when `/bm:code-review 11 --fix` was run instead of parking. All
three numbered items above are fixed on `master` (commits `3be21ff`, `ce52cf0`, `bb877a5`,
`49b2d85`): `_RENDER_PRE_CONTRACT_WORDINGS` is now the eleventh `_RenderRegistrySnapshot` field
with case-count and non-tautology floors; the extraction table is locked across all four columns
and `_RENDER_FIXTURE_SHAPE` across all eight full-value needle tuples; and item 3 was resolved by
*enforcing* the two `| QUAL-01 |` claims rather than narrowing them, so both rows are byte
unchanged. Every previously-GREEN mutation in `11-REVIEW-gap-closure.md`'s table now goes RED.
Retained as a record, not as work. See `11-REVIEW-FIX.md`.

**One residual survives, and it is a scope decision rather than a defect** — tracked as 999.16.

**Requirements:** none — closed unpromoted
**Plans:** 0 plans

Plans:

- [x] Closed by /bm:code-review 11 --fix (2026-09-01), no plan needed

---

### Phase 999.15: Give a wrapped hop a landing band in the validation rubric (CLOSED 2026-09-01 by /bm:code-review 11 --fix)

**Goal:** Make `validation-rubric.md`'s Criterion 4 bands self-consistent, so an emission with a
hop broken across physical lines has a named lower band to fall to.

**Why:** Phase 11 fixed the Rigorous descriptor to state R1 (no-wrap) correctly — that closed the
original CR-01 defect, where a wrapped hop scored **Rigorous** in words verbatim from the rule it
violated. But the Sound band's form clause still names only the ordered-list defect, and Hand-wavy
names only missing chains, unknown GT-IDs and analogy misuse. Neither enumerates the wrap defect,
so an agent applying the rubric mechanically — band-matching on the defects each band actually
lists — has no trigger to demote to, and could in principle land back on Rigorous.

**Why it is minor:** this is a live-behaviour concern (how an agent applies the rubric), not a
static-content defect a gate can falsify, and it is outside the literal text of Phase 11's
success criteria SC1-5, which name `output-template.md` and `SKILL-body.md` rather than the
rubric's band completeness. The third-surface work went beyond what SC1-5 required and is a net
improvement on the prior state — just not yet fully self-consistent.

**Fix (applied):** the Sound band's form clause now names the hop-wrap defect explicitly, so a
wrapped hop has a band to fall to. Landed as commit `e58b7fc` in `shared/`, regenerated with
`python3 scripts/sync-content.py --write`. Filed and closed the same day (2026-09-01) — the
verifier parked it as minor, then `/bm:code-review 11 --fix` was run instead of parking.

**Requirements:** none — closed unpromoted
**Plans:** 0 plans

Plans:

- [x] Closed by /bm:code-review 11 --fix (2026-09-01), no plan needed

---

### Phase 999.16: Decide whether focused-mode skills are in rendering-contract scope (BACKLOG)

**Goal:** Settle one scope question Phase 11 never asked: does the emission rendering contract
bind the focused-mode skill surfaces, or only the three canonical surfaces the agent assembles
from?

**Why it exists:** `/bm:code-review 11 --fix` fixed WR-09 halfway and stopped, correctly.
`shared/references/reason-upward.md` stated the one-line chain form unqualified; the R6 qualifier
sentence now lands there and in its generated skill stub (commit `e42118d`), so the focused-mode
surface no longer contradicts the contract. But it was deliberately **not** added to
`_RENDER_RULE_SURFACES` — so the rule is *stated* there, not *enforced* there.

**Why the fixer stopped rather than finishing.** Registering a fourth surface would make both
`| QUAL-01 |` rows' phrase *"no registered surface among all three — [three named files]"* false,
reopening CR-02's wording one commit after CR-02 was closed by the opposite branch (enforce the
claims rather than narrow them). Finishing the fix mechanically would have undone the fix beside
it. That is a decision, not a defect.

**The actual question, stated plainly:** thirteen companion skills ship as slash-invocable
surfaces that restate parts of the method. If the contract binds them, the registered-surface set
grows from three to some larger number and every one of them needs per-surface required rules —
a real cost, and it changes what "canonical surface" means. If it does not bind them, the current
state is already correct and this entry closes unrun, with the reason recorded.

**Entry condition:** answer the scope question first, in `/bm:discuss-phase`, with
`_RENDER_SURFACE_REQUIRED_RULES` and the thirteen skill sources in front of you. Do not open this
as an implementation phase before that answer exists — the implementation is small either way and
the answer is the whole work.

**Requirements:** TBD
**Plans:** 0 plans

Plans:

- [ ] TBD (promote with /bm:review-backlog when ready)

---

### Phase 999.17: sha256-pin `_chain_block_well_formed` for a reproducible CONTRACT-06 (MERGED INTO 999.18 — 2026-09-02; 999.18 PROMOTED 2026-09-02 to v8.26.0 Phase 13)

**Merged at `/bm:review-backlog` 2026-09-02** as 999.18's closing step. 999.18 re-specifies the
contract this function enforces, so pinning first would freeze the wrong bytes — the ordering
constraint is now internal to one phase instead of a cross-entry dependency someone has to notice,
and the function is touched once rather than twice. The scope below is unchanged; only its owner
moved.

**Goal:** Make CONTRACT-06 genuinely reproducible by adding a sha256 digest pin over
`_chain_block_well_formed`'s source in `scripts/check-quality-harness.py`, precedented by the
existing `_RENDER_RULE_LITERALS` sha256 pin at `scripts/check-quality-harness.py:7193`.

**Why:** Phase 12 tiered CONTRACT-06 audit-only (A1) because nothing in the tree currently pins
that function byte-unchanged; the docstring's claim that it stays byte-unchanged
(`scripts/check-quality-harness.py:8395-8397`) is a claim about author discipline, not a
mechanical assertion.

**Why deferred rather than done in Phase 12:** this is new verification-mechanism work inside
`check-quality-harness.py` with no requirement in this milestone authorizing it; Phase 12's
stated goal is to ship this milestone's deliverables and let the headline gate sweep, not to add
new detector machinery.

**Entry condition:** if picked up, the fix is: add a `sha256:` digest pin over
`_chain_block_well_formed`'s source (mirroring `_RENDER_RULE_LITERALS`'s pin), re-tier CONTRACT-06
`reproducible`, and point its `artifact_link` at the new pin/control (a matrix-row edit + a small
detector addition, not a milestone).

**Requirements:** none — closed unpromoted / TBD
**Plans:** 0 plans

Plans:

- [ ] TBD (promote with /bm:review-backlog when ready)

---

### Phase 999.18: State the chain-head grammar, including chain-as-input (PROMOTED 2026-09-02 to v8.26.0 Phase 13 — absorbed 999.17)

**Goal:** Make the section-4 head line's grammar explicit on both canonical surfaces — consumed
inputs are `GT-N` **or** `Cn` identifiers, each optionally glossed in parentheses, joined by `+`,
with the first `→` closing the head — and show the possessive/prose form as non-conforming.

**Why (measured, not inferred):** the 2026-09-02 v8.25.0 PR-P1 run scored C6 malformed on exactly
this. Its head reads `GT-13? (…) + GT-12? (…) + C2's threshold`; the possessive puts unparenthesized
prose where `_CHAIN_FORM_LINE_RE` expects a delimiter, so the whole block fails to parse. C7's head
in the same analysis — `C1 (2.20× at full duty) + C2 (…) + C4 (…)` — parses fine. The detector has
accepted `C\d+` with an optional parenthesized gloss all along; **no surface states it.**
`output-template.md`'s chain-format section says only *"The head line carries the GT identifiers and
their brief fact labels"*, which does not describe a chain consuming an upstream chain at all. The
agent complied by luck in one place and improvised in the other.

**Why it belongs to 999.3's lineage:** this is the same under-specification 999.3 was filed to
close, in a case 999.3's two worked cases (hop wrapping, verdict expiry) did not enumerate. The fix
is the contract, **not** widening the regex to accept possessives — record that explicitly if the
phase resolves the other way, per the standing note on 999.3's Case A.

**Acceptance:** the head-grammar rule stated on both canonical surfaces and registered in QUAL-01's
cross-surface literal set with a control that fails if it is dropped; a conforming and a
non-conforming worked example in `output-template.md`, extracted at self-test time and scored by
the **unmodified** `_chain_block_well_formed` (the CONTRACT-03 worked-example leg); C6's head
re-rendered under the new rule scores well-formed.

**Absorbed 999.17 at `/bm:review-backlog` 2026-09-02.** This phase closes with 999.17's work: add
the sha256 digest pin over `_chain_block_well_formed`'s source (mirroring the `_RENDER_RULE_LITERALS`
pin at `scripts/check-quality-harness.py:7193`), re-tier CONTRACT-06 `reproducible`, and point its
`artifact_link` at the new pin. **Order is the reason for the merge:** the pin lands *after* the
grammar rule and its controls, never before — pinning first freezes the bytes this phase exists to
change. Note this moves a matrix row, so the coverage headline moves with it and HEADLINE-LOCK will
sweep the surfaces.

**Requirements:** TBD
**Plans:** 0 plans

Plans:

- [ ] TBD (promote with /bm:review-backlog when ready)

---

### Phase 999.19: Make the §6→§4 closure ledger's claim inventory mechanical (PROMOTED 2026-09-02 to v8.26.0 Phase 14)

**Goal:** The ledger must enumerate section-6 claims by a **stated extraction rule** — matching what
`_conclusion_claims` extracts (bold colon lead-ins and list items, minus the documented exclusions)
— rather than by whatever the agent remembers having claimed.

**Why (measured, not inferred):** in the 2026-09-02 v8.25.0 PR-P1 run the ledger listed 8 claims and
8 chains, "clean — no cuts". The detector found a ninth: the `**Trade-offs acknowledged:**`
paragraph, which cites assumption IDs (A19, A20, A12, A13, A15, A16) and no chain, and which
asserts material absent from section 4 (a 1-year no-upfront plan realizes materially less; Lambda's
non-cost benefits). That paragraph is **prescribed** by `output-template.md:253` and **named** by
Criterion 6's Rigorous band as a claim class that must trace — *"every claim in the Conclusion
section (recommended approach, key insight, trade-offs acknowledged) traces to a specific named
derivation chain"*. By the rubric's own wording the run's Criterion 6 was **Sound**, not Rigorous.

**The structural defect, stated plainly:** the gate's Criterion 6 justification cites the ledger's
own completeness as evidence. The ledger is written by the same pass that writes the claims, so a
claim never entered is invisible to the audit that reads it — **the inventory is self-selected and
the check cannot fail.** That is a stronger finding than the missed paragraph itself.

**Open sub-question, to be answered in `/bm:discuss-phase`, not here:** must a caveat that qualifies
an existing claim cite the chain it qualifies, or carry an explicit *no chain — flagged assumption
only* marker? Both are contract answers. Do not answer it by loosening `_conclusion_claims`'s
bold-lead-in extraction — that is the widening treadmill, and FIX-CONTRACT-01 limitation 3 already
records where its exclusions stop.

**Acceptance:** the extraction rule stated on both canonical surfaces; a section-6 claim absent from
the ledger detectable from the emission alone; re-scoring
`.planning/captures/pr-p1-v8.25.0-2026-09-02/PR-P1.md` under the rule yields Criterion 6 **Sound**.

**Requirements:** TBD
**Plans:** 0 plans

Plans:

- [ ] TBD (promote with /bm:review-backlog when ready)

---

### Phase 999.20: Give Criteria 4 and 6 a mechanical scan to quote (PROMOTED 2026-09-02 to v8.26.0 Phase 15)

**Goal:** Extend the Phase 5 Self-Audit Gate with a chain-form and claim-inventory scan emitted as
process output, mirroring the Assumption Audit scan that already ships.

**Why (measured, not inferred):** both self-audit disagreements in the 2026-09-02 v8.25.0 PR-P1 run
are the gate rating **itself** Rigorous against defects sitting in its own text — Criterion 4
Rigorous with 1 malformed chain block, Criterion 6 Rigorous with 1 untraced claim. The assumption
axis has a per-chain-per-step scan table (44 rows in that run) the gate can quote and a reader can
check. Criteria 4 and 6 have no equivalent, so their bands rest on assertion, and the analysis
asserted correctly on neither.

**Why it is the general fix:** 999.18 and 999.19 each close one contract hole. This closes the class
— it moves the reconciliation `_selfaudit_calibration_defects` performs *after* the fact into the
emission itself, so the agent reaches the finding before the detector does. Every future contract
rule gets checked by the same scan for free.

**Sequencing:** after 999.18 and 999.19. A scan can only cite rules that exist; running this first
would ship a scan with nothing to scan for.

**Watch for:** the gate already runs last under a `maxTurns: 60` budget and owns the re-perception
edge. A scan that costs more than it catches is a real risk — size it against the Assumption Audit
scan's measured cost on this same capture, not in the abstract.

**Requirements:** TBD
**Plans:** 0 plans

Plans:

- [ ] TBD (promote with /bm:review-backlog when ready)

---

### Phase 999.21: Decide the anaphoric-source policy for read-at-source labels (MERGED INTO 999.11 — 2026-09-02)

**Merged at `/bm:review-backlog` 2026-09-02** as 999.11's Case B, on the 999.9/999.10 → 999.3
precedent: same gate, same class of question, same instrument needed to answer it. The finding
below is retained in full because it is this entry's evidence, not 999.11's. Do not schedule this
entry — schedule 999.11.

**Goal:** Settle whether `*Provenance: read-at-source* — same page` is a legal provenance source
string, and make the answer mechanical.

**Why (measured, not inferred):** running `check-provenance.verify()` against the 2026-09-02
v8.25.0 PR-P1 capture reports **3 unmatched sources of 10 labels** — GT-2, GT-4 and GT-7, every one
of them citing *"same page"* instead of repeating the URL its predecessor named. `provenance_flag`
raises to 1 on a run whose literals score 11/11 located, 0 misattributed, 0 unreadable. The flag is
real (the join genuinely cannot resolve the reference) but it is a **citation-style** defect
reported at the same weight as a fabricated source.

**Sibling of 999.11.** Same gate, same class of question: a matching policy carrying no recorded
measurement, meeting a rendering the contract never forbade. Sequence with or after it; whoever
takes one should read `_join_key` and `_bind` for both.

**Two resolutions, and the phase must name which it took:**

- **(a) Contract.** Require every `read-at-source` label to name a resolvable source. 999.3's
  lineage; costs the agent a repeated URL per GT.

- **(b) Detector.** Teach the joiner to resolve intra-section anaphora against the nearest preceding
  labelled GT. Cheaper for the agent, but it is a widening of the one gate in the stack that records
  fact rather than form — if chosen, say so in the goal statement rather than letting it pass as a
  bug fix.

**Requirements:** TBD
**Plans:** 0 plans

Plans:

- [ ] TBD (promote with /bm:review-backlog when ready)

---

---

## Progress

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. Discovery & Audit | v8.21.0 | 1/1 | Complete | 2026-08-30 |
| 2. Gate Implementation | v8.21.0 | 2/2 | Complete | 2026-08-30 |
| 3. Integration & Ship | v8.21.0 | 1/1 | Complete | 2026-08-30 |
| 4. Capture Retention & Fixture Foundation | v8.24.0 | 4/4 | Complete | 2026-08-31 |
| 5. Provenance Verifier & Gate | v8.24.0 | 3/3 | Complete | 2026-08-31 |
| 6. Integration & Ship | v8.24.0 | 5/5 | Complete | 2026-08-31 |
| 10. Headline Surface Coverage | v8.25.0 | 11/11 | Complete | 2026-09-01 |
| 11. Emission Rendering Contract | v8.25.0 | 11/11 | Complete   | 2026-09-01 |
| 12. Integration & Ship | v8.25.0 | 5/5 | Complete    | 2026-09-02 |
| 13. Chain-Head Grammar | v8.26.0 | 28/28 | Complete    | 2026-09-03 |
| 14. Closure-Ledger Claim Inventory | v8.26.0 | 6/6 | Complete    | 2026-09-03 |
| 15. Self-Audit Scan | v8.26.0 | 13/13 | Complete    | 2026-09-04 |
| 16. Integration & Ship | v8.26.0 | 5/5 | Complete    | 2026-09-04 |
| 17. Conformance Baseline | v9.0.0 | 3/3 | Complete    | 2026-09-05 |
| 18. Exemplar Conformance | v9.0.0 | 14/14 | Complete   | 2026-09-05 |
| 19. False-Negative Rate | v9.0.0 | 6/7 | In Progress|  |
| 20. Live Conformance | v9.0.0 | 0/TBD | Not started | - |
| 21. Generate the Claim Surface | v9.0.0 | 0/TBD | Not started | - |
| 22. Cap the Recursion | v9.0.0 | 0/TBD | Not started | - |
| 23. Ship v9.0.0 | v9.0.0 | 0/TBD | Not started | - |

---

*Roadmap updated: 2026-09-02 — milestone v8.26.0 (Self-Audit Falsifiability) opened, promoted from backlog 999.18 (absorbing 999.17), 999.19 and 999.20. Phases 13-16 added (Chain-Head Grammar; Closure-Ledger Claim Inventory; Self-Audit Scan; Integration & Ship), 19/19 requirements mapped, 0 plans yet (roadmap stage). Backlog entries 999.17-999.20 marked PROMOTED; Backlog section otherwise unchanged.*

*Roadmap updated: 2026-09-04 — SHIP-05 added to Phase 16 (exemplar-conformance disclosure in the `[8.26.0]` CHANGELOG entry); milestone requirement count 19 → 20, and criterion 3's literal updated to match. Approved from `.planning/PROPOSAL-L1-first-milestone-2026-09-04.md` §4. The v9.0.0 "Conformance" milestone (Phases 17-22) is proposed in that same document and is NOT yet written here — it lands via `/bm:new-milestone` after Phase 16 ships.*

*Roadmap updated: 2026-09-04 — milestone v9.0.0 (Conformance) opened, promoted from `.planning/PROPOSAL-L1-first-milestone-2026-09-04.md` §2 (fully approved 2026-09-04). Phases 17-23 added (Conformance Baseline; Exemplar Conformance; False-Negative Rate; Live Conformance; Generate the Claim Surface; Cap the Recursion; Ship v9.0.0), 19/19 requirements mapped, 0 plans yet (roadmap stage). L1 (Phases 17-20) gates L2/L3 (Phases 21-22) by an explicit Depends-on chain. Backlog entries 999.2, 999.12 and 999.13 marked PROMOTED into Phases 19/20/20 respectively; 999.30/999.31 noted for terminal disposition by Phase 22. Backlog section otherwise unchanged.*

*Prior entry: 2026-09-02 — backlog reviewed: 999.21 merged into 999.11, 999.17 merged into 999.18, next-milestone scope proposed as 999.18-999.20. Earlier same day: four backlog entries added (999.18-999.21) from the first post-999.3 PR-P1 measurement; see the note above the resolution order. Prior entry: 2026-08-31 — milestone v8.25.0 (Rendering Contract & Surface Coverage) opened, promoted from backlog 999.6 and 999.3 (the latter absorbing 999.9/999.10). Phases 10-12 added (Headline Surface Coverage; Emission Rendering Contract; Integration & Ship), 14/14 requirements mapped, 0 plans yet (roadmap stage). Backlog section otherwise unchanged from the prior review pass.*

For detailed milestone information, see `.planning/milestones/v8.24.0-ROADMAP.md` and
`.planning/milestones/v8.21.0-ROADMAP.md`.

### Phase 999.22: One ledger row must discharge one claim, not every span on its line

**Parked from Phase 14 verification, 2026-09-03** (`14-VERIFICATION.md` gap 1; originally
`14-REVIEW.md` WR-01). Severity minor — no Phase 14 Success Criterion fails today, because the
shipped PR-P1 fixture has no multi-quote row. The defect is live and reproducible.

**Goal:** `_closure_ledger_fragments` matches the structural row shape via
`_STRUCTURAL_LEDGER_ROW_RE`, then discards that match's own capture group and re-scans the whole
stripped line with `_LEDGER_QUOTE_RE.finditer`, crediting every quoted span on the line rather than
the one the structural shape names. One row can therefore discharge N unrelated section-6 claims,
against R4's singular "quotes the claim". Verified by direct call: a row quoting two spans returns
both as fragments.

This is the failure direction Phase 14's own goal statement warns against — an unrelated ledger row
can make a genuinely uncited claim invisible to the audit that reads the ledger.

**Fix:** use the structural match's own `group(1)` as the sole fragment for a matched row, plus a
control asserting a two-quote line yields exactly one fragment.

---

### Phase 999.23: R11 says three lead-ins; the template prescribes four

**Parked from Phase 14 verification, 2026-09-03** (`14-VERIFICATION.md` gap 2; originally
`14-REVIEW.md` WR-03). Severity minor — SC1's narrow "matches what `_conclusion_claims` extracts"
contract still holds, because R11's general bold-lead-in clause predicts the extraction correctly.

**Goal:** R11 states "the three lead-ins this template prescribes — `**Recommended approach:**`,
`**Key insight:**`, `**Trade-offs acknowledged:**`". The same template prescribes a fourth eleven
lines above the rule, `**Confidence:**`, and instructs that a MEDIUM/LOW confidence line carry
explanatory prose — prose that clears `_is_assertive_claim` and is mined as a claim. Reproduced:
inserting a template-conforming MEDIUM Confidence line moved the fixture from 7 claims / 1 untraced
to 8 / 2, with the Confidence line as the new untraced claim.

A false statement of fact about the very document it sits in, byte-identical across all six
surfaces, and no surface tells an author the Confidence line needs a citation to satisfy the rule it
is extracted under.

---

### Phase 999.24: An unfenced in-section-6 ledger row counts itself as a claim

**Parked from Phase 14 verification, 2026-09-03** (`14-VERIFICATION.md` gap 3;
`14-REVIEW.md` WR-07). Severity minor.

**Goal:** A closure-ledger row rendered in section 6 without a fence inflates `conclusion_claims`
by counting itself. Verified: 7 → 8, with the untraced count unaffected. R4 recommends a
heading-introduced ledger, so the unfenced rendering is a shape the contract invites.

---

### Phase 999.25: `quality-ledger-v8.26/README.md` still calls `_FROZEN_PATHS` registration pending

**Parked from Phase 14 verification, 2026-09-03** (`14-VERIFICATION.md` gap 4;
`14-REVIEW.md` WR-05). Severity minor, cosmetic, in a tracked file.

**Goal:** The README's sequencing note describes plan 14-06's `_FROZEN_PATHS` registration as not
yet done, while an earlier line in the same file says it is. 14-06 landed; the note is false.

---

### Phase 999.26: Parameterise `_render_claim_bound_problems`' dispatch and floor it

**Parked from Phase 14 verification, 2026-09-03** (`14-VERIFICATION.md` gap 5;
`14-REVIEW.md` WR-02/WR-06). Severity minor.

**Goal:** The punctuation-toggle dispatch is triggered solely by `len(expected_verdicts) == 2` and
the caveat-id routing is a function-local literal set, both shape-dispatched rather than
parameterised and floored. Editing both hand-maintained tables deletes the mechanical proof the doc
rows publish while the self-test still exits 0.

---

### Phase 999.27: SCAN-GUARD's live leg can be reduced to an unconditional PASS (RESOLVED 2026-09-04 by Phase 15 plan 15-09)

**Parked from Phase 15 re-verification, 2026-09-04** (`15-REVIEW.md` WR-05, which widens and
subsumes the earlier WR-03/`m22` residual the 15-06 executor disclosed as out of scope).
Severity minor — the defect is latent, not active: the live leg reports correctly today.

**Goal:** Neutralizing `if failures:` to `if False:` in `_validate_files`
(`scripts/check-selfaudit-scan.py`) leaves `python3 scripts/check-selfaudit-scan.py` exiting 0
and `bash scripts/check-firewall-battery.sh` reporting `FIREWALL: GREEN` — the live leg can be
turned into an unconditional PASS with every offline gate still green, because nothing controls
the live leg's own reporting path. The `--self-test` fixtures are in-memory and never read the
shipped tree, so they are structurally blind to this.

The fix shape is the one GATE-01 already uses: an anti-vacuity control on the **live** leg that
mutates the surface this run actually read (strip a literal the gate must catch) and fails unless
the checker reports that specific defect. GATE-01's `_assert_live_coverage` is the precedent;
PROV-GUARD and REG-GUARD's live legs are the other registered examples to compare against.

**Not to be confused with** Phase 15's two blocking gaps (the Criterion 2 admission-sentence
contradiction and the missing `R-02-placement-aa` control), which are in scope for the next
gap-closure round rather than parked here.

**RESOLVED 2026-09-04 by plan 15-09.** `_live_exit_code` was extracted with isolation arms in the
`_roster_problems` idiom, three call-site censuses (`validate-census`, `live-census`,
`live-dispatch-census`) were added, and the live leg is now registered in both
`scripts/check-firewall-battery.sh` (two-command form) and the `check-selfaudit-scan` CI job.
The Phase 15 verifier reproduced the closure live: reducing `_validate_files` to an unconditional
PASS is no longer silent, and deleting any of its three legs fails `--self-test` by name.
`R-02-placement-aa` — the other item this entry disclaimed — was also closed by 15-09.

---

### Phase 999.28: SCAN-GUARD's own anti-masking floor is narrowable and unlensed (RESOLVED 2026-09-04 by Phase 15 plans 15-12 and 15-13)

**Parked from Phase 15 third verification, 2026-09-04** (`15-VERIFICATION.md` gap 2;
`15-REVIEW.md` WR-01 and WR-04). Severity minor — it narrows confidence in the floor's own
robustness, one level up from Phase 15's stated success criteria. The 87-branch anti-masking
floor as a whole is real and was reproduced.

**Goal:** Two shapes let SCAN-GUARD's coverage claim be weakened with `--self-test` still green.

  1. **`_BAND_BULLETS` is narrowable 4 -> 1 undetected** (reproduced live by the verifier).
     Narrowing `(_BAND_RIGOROUS, _BAND_SOUND, _BAND_HANDWAVY, _BAND_ABSENT)` to `(_BAND_SOUND,)`
     leaves `--self-test` at rc=0 reporting "All 87 branches covered" — three of four
     band-descriptor literals have no arm in either criterion slice. This falsifies the
     "every multi-literal tuple has one arm per literal" coverage claim published on three
     surfaces: `CLAUDE.md`, `docs/ARCHITECTURE.md`, and the gate's own battery-registration
     comment. Fix: parameterise Rubric-11's arms over all four literals, registering the new ids
     in both `REQUIRED_BRANCHES` and `_BRANCH_ROSTER_LOCK`.

  2. **The roster floor's `covered` argument has no entry-source lock**
     (`scripts/check-selfaudit-scan.py:2764-2766`). Aliasing it to `REQUIRED_BRANCHES` makes
     `covered - required` empty by construction, so the surplus check becomes structurally
     incapable of failing — and the call-site census cannot see it, because the call is still
     there. This is the same `x != x` shape `check-quality-harness.py`'s ENTRY-SOURCE LOCK
     (plan 13-16 / R4-CR-02) exists to catch, and it is not in SCAN-GUARD's disclosed residual
     ledger. Fix: add an ENTRY-SOURCE LOCK matching that precedent. Taken from the review's
     measured claim and consistent with the code as read; not independently re-reproduced.

---

### Phase 999.29: SCAN-GUARD's published coverage figures disagree with their own enumerations (RESOLVED 2026-09-04 by Phase 15 plan 15-13)

**Parked from Phase 15 third verification, 2026-09-04** (`15-VERIFICATION.md` gap 3;
`15-REVIEW.md` WR-02 and WR-03). Severity minor — a documentation-accuracy defect, not a
functional gate hole beyond 999.28's. Plausible against the cited line numbers; not re-verified
character-by-character.

**Goal:** Three published figures do not match what they enumerate. This is the same
"a claim the machinery does not honour" shape Phase 15 exists to close, one level up — which is
why it is worth fixing rather than living with.

  1. `docs/ARCHITECTURE.md:150` states "20 fail" beside an enumeration (`m1`-`m5`, `m7`-`m12`,
     `m17`-`m21`) that arithmetically totals 16. Census rows `m13`-`m16` carry no recorded
     disposition on either `CLAUDE.md` or `docs/ARCHITECTURE.md`.

  2. The "seven not-found reporting arms" residual (gate docstring and `CLAUDE.md`) names only
     five, omitting Rubric-2's `scan_idx == -1` and `precedence_idx == -1` reports — both
     measured rc=0.

  3. The netting count disagrees with itself: the gate docstring says "net of the **two** closed"
     while `CLAUDE.md` and `docs/ARCHITECTURE.md` say "net of the **one**". `R-02-placement-aa`
     is a single branch id, so "one" is correct.

Fix: correct the count to 16 and account for `m13`-`m16`; add the two missing Rubric-2 arms to
the residual list on all three surfaces; settle the netting count at "one".

---

### Phase 999.30: SCAN-GUARD's anti-masking meta-guards are themselves unlocked (terminal disposition due by v9.0.0 Phase 22)

**Parked from Phase 15 fourth verification, 2026-09-04** (`15-VERIFICATION.round2.md` gap 1;
`15-REVIEW.round2.md` CR-01 and CR-02). Severity minor — reproduced live by the verifier on an
isolated scratch tree, but it narrows confidence in the mechanisms that prove the floor is
exhaustive, one level further removed from Phase 15's success criteria than 999.28 was. The
100-branch floor itself is real and green against the shipped tree.

**Goal:** The successor to 999.28. Waves 11-13 closed 999.28's two specific reproduced
mutations; both fixes have a fail-open one edit wide, of the same shape.

  1. **`_validate_leg_symbols` is an unlocked registry inside an anti-masking floor**
     (`scripts/check-selfaudit-scan.py:~3368`). Dropping `"_check_cross_surface"` from the tuple
     AND deleting the real `_check_cross_surface(...)` call from `_validate_files` together leave
     `--self-test` at rc 0, "All 100 branches covered", while `(validate-census)` prints
     `CALL-SITE CENSUS: PASS (all four legs ... present exactly once)` — a false claim, since the
     live leg no longer runs the cross-surface check. This restores `m22`, the exact defect plan
     15-09 registered the census to close. Fix: lock the tuple against a second, independently
     transcribed roster (the `_BRANCH_ROSTER_LOCK` idiom already in this file), and derive the
     PASS message's leg count and names from the tuple rather than a hardcoded "all four legs".

  2. **The ENTRY-SOURCE LOCK added by plan 15-12 is unanchored and unfloored**
     (`scripts/check-selfaudit-scan.py:~1710`, `~3251`). `_entry_source_problems` does a free-text
     `_contains(inspect.getsource(_run_self_test), expected)` over the whole function rather than
     anchoring to the `_roster_problems(` call site, so aliasing the real call's third argument to
     `frozenset(REQUIRED_BRANCHES)` while leaving the expected triple in an inert comment still
     prints `ENTRY-SOURCE LOCK: PASS` at rc 0. Separately `roster_entry_source_expected` has no
     second transcription, so narrowing it makes the lock vacuous in a one-place edit. The
     `check-quality-harness.py` R4-CR-02 precedent this file cites as its model re-derives its
     required side from an independent transcription; that half is missing. Fix: anchor the search
     to the call site, and add the second transcription.

**Pattern worth naming at triage:** this is the third consecutive round where a fix closes the
specific reproduced mutation while a structurally identical hole one level removed stays open.
The verifier's recommendation is a general "lock every anti-masking registry with a second,
independently transcribed roster" pass rather than a fourth round of point fixes.

---

### Phase 999.31: SCAN-GUARD's multi-literal census and residual ledger overstate their own coverage (terminal disposition due by v9.0.0 Phase 22)

**Parked from Phase 15 fourth verification, 2026-09-04** (`15-VERIFICATION.round2.md` gap 2;
`15-REVIEW.round2.md` WR-01/WR-03/WR-05/WR-06). Severity minor — a documentation-accuracy defect
on surfaces presenting themselves as measured fact, not a functional hole beyond 999.30's.
The successor to 999.29, which waves 11-13 closed.

**Goal:** Four claims do not match what they enumerate or what the code does.

  1. The multi-literal census published as "nine found in total ... no named exceptions" (gate
     docstring bound (11), restated verbatim in `CLAUDE.md` and `docs/ARCHITECTURE.md`) recounts
     to ten — Rubric-13's region loop and clause loop are two constructs, not one — and
     `_validate_leg_symbols` is itself an undisclosed exception, a four-literal tuple driving a
     check with no per-literal arm. Fix: recount, and either name the exception or close it per
     999.30 item 1 and state the claim as genuinely true.

  2. The comment at `~line 2610` says the Rubric-11 loop is driven `via zip(..., strict=True)`
     while the code at line 2623 uses plain `zip` — and the module docstring and the `_BAND_NAMES`
     comment both correctly explain that `strict=True` was deliberately rejected. One comment
     contradicts the rest of the file's own disclosure. Fix: correct the comment.

  3. `_BAND_BULLETS` has no membership floor (no `_BAND_BULLET_LOCK` symbol exists), so a
     same-cardinality proper subset — duplicating one literal to replace another — plausibly still
     reports full coverage, and reordering mislabels all eight ids. Fix: float it behind a
     membership lock, or narrow the published claim to name the open direction.

  4. The published "eight not-found reporting arms" figure may undercount by at least four:
     Rubric-9's Criterion-4-slice, Rubric-10's Criterion-6-slice, Rubric-13's
     Verdict-Block-Format-slice and Rubric-14's Criterion-2-slice not-found call sites all exist
     (grep-confirmed) but were not neutralized to determine whether they are controlled. Fix:
     neutralize each and correct the count.

---

### Phase 999.32: `report-conformance.py`'s provenance sentinel is structurally incapable of failing

Filed 2026-09-05 by Phase 17's code review (CR-01) and independently reproduced by its verifier.
Severity minor — the published reading is correct today; what is missing is regression protection
for the invariant, not the invariant itself.

**Goal:** `_control_render_provenance_sentinel` (`scripts/report-conformance.py`, ~lines 806-816)
is the only control guarding the must-have truth "the nine provenance columns render the literal
`n/a`, never `0`" — the distinction `docs/conformance-baseline.md` devotes a whole "Column
vocabulary" section to. It cannot fail:

  1. `assert "n/a" in md` is satisfied by static prose `render_markdown` emits unconditionally, so
     it passes with zero rows rendered.
  2. The loop asserts `row[field] == "n/a"` against the INPUT rows, which `_synthetic_row` set to
     `"n/a"` two lines earlier — expected and actual are the same expression, and `md` is never
     re-read after being built.
  3. The in-code comment claims the opposite of what the code does.

Measured: three separate neutralizations — a renderer coercing every provenance cell to `0`, a
renderer emitting zero rows, and `build_row` collapsing `n/a` to `"unreadable"` — each left
`--self-test` at rc 0 printing `SELF-TEST PASS — 14 controls run`.

Verified separately, and why this is minor: the committed artifacts are correct — 0 of 261
provenance cells across the 29 rows of `docs/data/conformance.json` are non-`n/a`, and
`docs/conformance-baseline.md` renders `n/a` 30 times and `| 0 |` zero times.

**Entry condition:** re-implement the control to parse cells back out of the RENDERED Markdown
table (or JSON) and assert on that, plus a negative control proving a coercing renderer is
rejected. The review's suggested fix at `17-REVIEW.md` CR-01 is directly usable. Consider also
WR-01 (`PROVENANCE_FIELDS = _DEFECT_RECORD_FIELDS[13:]` is a magic offset that silently
misclassifies any appended measured field) and WR-04 (`--self-test` has no runner in the battery,
CI, either hook, or `docs/TESTING.md`) from the same review.

**Requirements:** none — closed unpromoted / TBD
**Plans:** 0 plans

Plans:

- [ ] TBD (promote with /bm:review-backlog when ready)

---

### Phase 999.33: Phase 17's pre-commit gate-count doc sweep missed three surfaces

Filed 2026-09-05 by Phase 17's verifier, which caught it by direct grep rather than by trusting
`17-03-SUMMARY.md`'s own `SWEEP-CLEAN` claim. Severity minor — documentation accuracy, not a
functional hole.

**Goal:** Phase 17 wired a second pre-commit gate (`report-conformance.py --check`) and swept the
surfaces stating the gate count. Three were missed, one of them self-contradicting:

  1. `CLAUDE.md` lines 86 and 88 still read `# sync-drift gate in .git/hooks/pre-commit` and
     `# same sync-drift gate via .githooks/pre-commit` — directly contradicting lines 189-190 of
     the same file, which correctly name both gates. This is the file read into every session.
  2. `CONTRIBUTING.md:40` still states that one gate fires on `git commit`, the sync-drift gate.
  3. `scripts/install-hooks.sh:57` still refers to manually adding the sync-drift check, singular.

Root cause, and the more valuable half: the sweep's own verify command never included
`CONTRIBUTING.md` or `scripts/install-hooks.sh` in its file list, and none of its four literal
patterns match `CLAUDE.md`'s actual stale phrasing. The sweep passed while missing three live
contradictions — a verify command that cannot see the defect it exists to catch.

**Entry condition:** update the three surfaces to name both gates, matching the shape already
applied to `docs/ARCHITECTURE.md`, `docs/CONFIGURATION.md`, `docs/DATA-FLOW.md`,
`docs/TESTING.md` and `docs/DEVELOPMENT.md`; then widen the sweep command itself to cover
`CONTRIBUTING.md` and `scripts/install-hooks.sh` and to match the real phrasing, so a re-run
would actually catch a recurrence.

**Requirements:** none — closed unpromoted / TBD
**Plans:** 0 plans

Plans:

- [ ] TBD (promote with /bm:review-backlog when ready)

### Phase 999.34: CONF-GATE's `run_live()` control flow is outside its own hardened layer

Filed 2026-09-05 as the accepted residual of Phase 18's gap-closure round 3. The phase's blocking
gap on criterion 6 ("make the zero standing") is **parked here by explicit decision, not closed** —
shipping with the exit-code exposure documented. Severity: blocking-as-verified, accepted.

**Goal:** Phase 18 rounds 1-3 hardened CONF-GATE's comparator layer until every mutation to a
comparator predicate, a pinned constant, a lock table, or a registered call-site's *text* fails
`--self-test` by name. That layer now holds. `run_live()`'s own control flow was never in it, and
two vectors there were independently reproduced by both the code reviewer and the verifier on
disposable scratch copies:

  1. **CR-01 — the verdict lies while the diagnosis is correct.** `run_live()`'s two `return 1`
     branches (`scripts/check-conf-gate.py:747` and `:753`) are unasserted by any control. Flip
     either to `return 0` with a real corpus defect present: the gate computes the problems and
     *prints* `check-conf-gate: FAIL — TARGET EXCEEDED …` to stderr, then exits 0. Both
     `.github/workflows/validation.yml` and `scripts/check-firewall-battery.sh` read only the exit
     code, so this class of regression ships inside a green CI job and a `FIREWALL: GREEN` run.
     This is **not** the census's disclosed "problems computed then discarded" residual — the
     mutation is downstream of every registered call site's text, so no source-text census can
     reach it.

  2. **CR-02 — the one loop-carried comparator.** `_d03_rule_problems_from_text` is the only
     registered enforcement symbol invoked from inside a loop rather than at statement level. The
     census and form lock match call-site *text*, which is byte-identical whether the loop body
     ever executes. Guard the loop with `if True: continue` and an isolated D-03 violation —
     verified caught in isolation first, so the reproduction is single-vector — ships with zero
     output on both legs, rc 0.

Root cause, and the more valuable half: three consecutive rounds each closed their named findings
while the same must-have failed through adjacent vectors *in the machinery the round had just
built*. The hardening mechanism was always aimed one level below where the exposure sat.

**Why this is not the declined fourth-level meta-gate.** `18-CONTEXT.md` D-08 declines a separate
gate watching CONF-GATE from outside. This is inside CONF-GATE's own `--self-test`, and the
in-repo precedent is exact: `scripts/check-selfaudit-scan.py:1460` already carries a pure
`_live_exit_code(failures)` helper with two isolation arms *and* its own call-site census, for
the identical shape. Round 2 deferred the adjacent finding as "a repo-wide accepted bound
SCAN-GUARD discloses for itself"; that rationale is factually inverted — SCAN-GUARD is the
counter-example, not the precedent.

**Entry condition:** extract `run_live()`'s verdict into a pure `_live_exit_code(problems,
d08_problems) -> int`, and extract the D-03 loop's row filter and disk read into a pure
`_d03_rule_problems(rows, read_text)` drivable from `--self-test` with synthetic rows and an
injected reader. Register both in the census/roster/form-lock tables and add isolation arms
proving both truth values. Adjacent and lower-severity, same shape: `main()`'s dispatch is
unasserted (swapping its two branches leaves the battery green) and the documented exit code 2 is
unreachable for any real import failure.

**Also parked from the same review:** `_strip_line_comments`' DISCLOSED BOUND at
`scripts/check-conf-gate.py:357-361` is overstated. It claims it cannot manufacture a false PASS
by hiding a real call site behind an in-string `#`; because the census tests equality against 1
rather than a `>= 1` floor, it can. The exploit is contrived, but this repo treats an overstated
bound as a real defect (the `reason-upward.md` fabricated-claim precedent).

**Full record:** `.planning/phases/18-exemplar-conformance/18-VERIFICATION-round3.md` (both
reproductions, with the isolation proof for CR-02) and `18-REVIEW-round3.md` (2 blocker,
5 warning, 6 convention). Both are preserved alongside the round-2 originals, which every Phase 18
SUMMARY ledger cites by name.

**Requirements:** TBD
**Plans:** 0 plans

Plans:
- [ ] TBD (promote with /bm:review-backlog when ready)

---

### Phase 999.35: `_chain_head_refs` cannot see a circularity stated past a chain's head line

Filed 2026-09-05 as Phase 19's one genuine stratum-A miss:
`tests/adversarial-corpus-v9.0/t06-hidden-cycle-past-head.md`, catalog row `T-06`, disposition
`defer-with-owner`.

**Goal:** an analysis whose two conclusions are genuinely circular — each conclusion's practical
force depends on the other, stated explicitly in the paragraph that follows the two-arrow
derivation rather than in the derivation itself — currently reads `dependency_cycles == 0` and
`ungrounded_chains == 0` when both chain heads cite only their own `GT-n` token. The circularity is
real; the detector's reading is clean.

**Mechanical reason:** `_chain_head_refs` returns on the first head-matching line of a
`### Conclusion` block and never reads further into it, so a citation stated later in the same
block's prose — after the two-arrow head line the function actually reads — is structurally
invisible to the dependency graph `_chain_dependency_defects` builds from those returned refs.

**Why Phase 19 could not close it:** `_chain_head_refs` sits inside CONTRACT-06's frozen detector
surface (alongside `_chain_block_well_formed`, `_conclusion_claims` and `_slice_sections`).
Widening its read window is exactly the kind of mid-measurement detector change 999.2 exists to
forbid, and any such change requires a written amendment to the milestone goal before the diff,
never after. Phase 19's own scope explicitly excludes it (`19-CONTEXT.md`, "Explicit non-goal").

**Disposition, restated from the catalog:** `defer-with-owner` — this entry is the named owner.
`tests/adversarial-corpus-v9.0/catalog.md`'s `T-06` row cites this number in plain text, and
`docs/conformance-baseline.md`'s stratum-A reading (1 of 5 clean) is the measured context.

**Requirements:** TBD
**Plans:** 0 plans

Plans:
- [ ] TBD (promote with /bm:review-backlog when ready)

---
