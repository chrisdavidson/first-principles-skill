# Agent-Goal Alignment Audit — v7.10

**Artifact type:** Agent-goal alignment audit / evaluation inventory
**Date:** 2026-06-27
**Phase:** 124-agent-goal-alignment-audit
**Requirement:** ALIGN-01, ALIGN-02, ALIGN-03
**Status:** DECIDED / inventory complete

---

## Decision up front

The `first-principles` agent's goal is **faithful first-principles reasoning plus trustworthy
gates** — every conclusion traces to a verified ground truth, every assumption is explicitly
challenged, and every gate can be independently re-run to prove correctness.

This audit evaluates every open method-fidelity gap and accumulated technical-debt item that
misaligns the shipped agent from that goal. Phase 124 **audits and forward-commits only**: it
authors no new companion technique, runs no live `claude` invocation, edits no `shared/` or
generated surface, and leaves all detector markers (`pre-mortem` 9 / `fishbone` 7 /
`inversion` 13 / `trade-off` 10), `MIN_HEADER_HITS==2`, and `_COMPOSER_FOCUS_CEILING==4`
byte-frozen. The actual fixes land in Phases 125-127; method-fidelity technique-adds
(calibrate / reference-class / argument-map / steelman) are forward-committed as named
follow-up milestones, not authored here.

---

## Scoring Rubrics

### D-04 Goal-Threat Severity (1-3)

Severity is anchored to **how badly the item misaligns the agent from its goal**, not a
generic Critical/High/Med/Low scale. A severity-3 item either lets the agent reason
confidently-wrong or directly undermines a trustworthy gate; a severity-1 item has no
reasoning or gate impact at all.

| Score | Definition |
|-------|-----------|
| 3 | Lets the agent reason confidently-wrong, OR undermines a trustworthy gate (method-fidelity guard; gate/detector correctness) |
| 2 | Degrades trust or maintainability of the verification surface without directly misleading reasoning (stale tooling/tests that could mask real drift) |
| 1 | Cosmetic / hygiene with no reasoning or gate impact (empty dirs, docstring drift, process ceremony) |

### D-01 Leverage and Offline-Fixability (1-3 each)

| Factor | Score 3 | Score 2 | Score 1 |
|--------|---------|---------|---------|
| **Leverage** | Unblocks many downstream items or a core capability | One subsystem | Isolated / self-contained |
| **Offline-fixability** | Fully fixable offline this milestone via deterministic doc/test/dir change | Offline-fixable but multi-step | NOT offline-fixable this milestone — needs a full technique-authoring milestone or fresh live budget |

**Composite = Severity × Leverage × Offline-fixability** (range 1..27, sorted descending in
the ALIGN-03 ranking table). This formula makes every row's rank reproducible from its three
factor scores.

---

## ALIGN-01: Method-Fidelity Gap Table

Four gaps remain open after the Tier-1 set shipped (`decompose` absorbed into `five-whys`,
`estimate`, `theoretical-limit`). Each is scored severity 3: all four let the agent reason
without a critical guard, which is the definition of goal-threat-3 under D-04.

| Gap | Technique | Severity | In-repo evidence | Threatened agent-goal | Forward-commit ID |
|-----|-----------|----------|------------------|-----------------------|-------------------|
| #3 Uncalibrated confidence | `calibrate` | 3 | `first-principles-portfolio-assessment.md` §"The honest gaps" #3; agent Phase 5 HIGH/MED/LOW confidence caveats (qualitative, no principled evidence-update procedure) | Trustworthy confidence — the method feels rigorous without being calibrated; HIGH/MED/LOW confidence labels carry no evidence weight | METHFID-CALIB |
| #4 No outside-view / base-rate guard | `reference-class` | 3 | `first-principles-portfolio-assessment.md` §"The honest gaps" #4; "No guard against first-principles' own failure mode" | The classic first-principles failure mode — reconstructing from pure reason while ignoring empirical base rates (reason confidently-wrong against what actually happens to projects like this) | METHFID-REFCLASS |
| #5 Inference validity unchecked | `argument-map` | 3 | `first-principles-portfolio-assessment.md` §"The honest gaps" #5; "Inference *validity* isn't checked" | Valid inference — Phase 4-5 derivation chains trust their chain structure, not the logic of each step; equivocation, affirming-the-consequent, and smuggled premises are uncaught | METHFID-ARGMAP |
| Tier-3 strongest-opposing-case | `steelman` | 3 | `first-principles-portfolio-assessment.md` §"Tier 3"; "construct the strongest opposing case before concluding" | Adversarial validation breadth — inversion attacks a claim; nothing constructs the best counter-thesis; the agent can conclude without ever encountering the strongest opposing argument | METHFID-STEELMAN |

All four IDs (`METHFID-CALIB`, `METHFID-REFCLASS`, `METHFID-ARGMAP`, `METHFID-STEELMAN`) are
used verbatim from `.planning/REQUIREMENTS.md` §"Method-Fidelity Technique-Adds" (D-05). No
new IDs are minted.

---

## ALIGN-02: Technical-Debt Inventory

### Debt Table

Evidence pointers were re-confirmed in-repo before citing (D-02 bounded-sweep protocol).

| Item | Source | Severity | Evidence (file / line) | Disposition |
|------|--------|----------|------------------------|-------------|
| Stray empty skill dirs `shared/skills/rollback-test/` and `shared/skills/testing/` | STATE.md ledger (carry_forward); `first-principles-portfolio-assessment.md` §"Housekeeping" | 1 | Both dirs contain no `SKILL.md`, generate nothing, and are git-tracked stubs; verified via `ls shared/skills/{rollback-test,testing}/` (empty) | fix-now → DEBT-01 (Phase 125) |
| `sync-content.py` generator target-count contradiction | STATE.md ledger (code_review_deferred P105 WR-03) + bounded sweep | 1 | `scripts/sync-content.py:23` ("12 focused-mode stubs" — stale); `:679` ("SKILLS to 12" — stale pre-v7.5 history note); `:681` ("SKILLS to 13" — correct); `:689` ("13 slash-invocable focused-mode stubs" — correct). Module-level docstring (line 23) contradicts the `generate_all()` docstring (lines 681-689) and the actual on-disk count of 13 skill dirs | fix-now → DEBT-02 (Phase 125) |
| Stale traceability-tooling docstrings (WR-01/WR-02) and `.py#anchor` whole-file-substring resolver (WR-03) | STATE.md ledger (carry_forward WR-01/WR-02, WR-03) | 2 | `scripts/check-traceability.py` — WR-01/WR-02: stale generate_all/related row-count claims in internal function docstrings (v6.1 Phase 86 code review; counts became stale as the matrix grew); WR-03: plain-substring anchor resolver at lines ~200-205 (`_rows_methodology_rigor` D-08 note) and ~971-980 (`if anchor not in content:` — resolves `.py#funcname` anchors by checking if the anchor string is any substring of the file, not a true symbol anchor) | fix-now → DEBT-03 (Phase 126) |
| Stale-count pytest fixtures | STATE.md ledger (carry_forward, future_milestone) | 2 | `tests/test_81_inventory.py:127,131-132` — asserts 26 `vX.Y-REQUIREMENTS.md` files; actual on-disk count is 40 (verified: `ls .planning/milestones/v*-REQUIREMENTS.md | wc -l`); `tests/test_step0_live_task1.py:49-56` — asserts 28 catalog rows; actual count is 35 after v7.9 NEGCAT fixtures (verified: `grep -c "^| S-\|^| B-" tests/step0-fixture-catalog.md`). Both failures confirmed by running pytest | fix-now → DEBT-04 (Phase 126) |
| Nyquist `XX-VALIDATION.md` ceremony gap for Phases 94-119 | STATE.md ledger (nyquist_gap) | 1 | Ceremony present only for Phases 88, 89, 91 (`.planning/phases/88-gen-01-execution/88-VALIDATION.md`, etc.). Phases 94-119 have `VERIFICATION.md` files but no `VALIDATION.md`; gap confirmed by scanning `.planning/phases/9*/` and `1{0..9}*/` dirs | fix-now → DEBT-05 (Phase 127) |
| RR-114-01: S-P02 inversion live pass-rate re-measure | STATE.md ledger (carry_forward) | 3 | Structural resolution shipped in Phase 121 (OCH-02/OCH-03): output-contract headers + detector extended inversion 9→13 markers; offline confirming gate in `scripts/_battery_core.py#self_test_boundary`. Live re-measure against post-Phase-121 detector fidelity remains forward-committed (v7.6 captures predate the new headers; honesty-not-score D-01) | deferred → LIVE-RR114 (needs live budget) |
| S-P10 (`estimate`) + S-P14 (`theoretical-limit`) clean live re-measure | STATE.md ledger (carry_forward) | 2 | `tests/step0-baseline-v7.6.md` — both rows spent-limit-INDETERMINATE at v7.6; RR-108-04 (estimate 0/5 clean, first measurement) and RR-108-05 (theoretical-limit 0/5 spend-limit-indeterminate) carried forward; no clean re-measure since v7.4 | deferred → LIVE-SP10SP14 (needs fresh live budget) |
| `check-step0-live.py` generator round-trip (P95 WR-02) | STATE.md ledger (carry_forward) | 1 | `scripts/check-step0-live.py` — live-harness generator round-trip was deferred at Phase 95; pre-existing carry-forward with low tooling impact; not in the v7.10 fix subset | deferred (low tooling impact; not in v7.10 scope) |
| P105 code-review deferrals (IN-01 Carnot `+273` vs `+273.15`, IN-02 reference vs example framing) | STATE.md ledger (code_review_deferred) | 1 | Phase 105 code review SUMMARY — IN-01/IN-02 informational items; phase passed; advisory only | deferred (advisory; phase passed) |
| P121 code-review deferrals (WR-01 inversion teeth verify 1/4 new markers; WR-02 aggregate-only assertion; IN-01/IN-02/IN-03 leniency/comment notes) | STATE.md ledger (code_review_deferred) | 1 | Phase 121 code review SUMMARY — 0C/2W/3I advisory; markers are present and correct; drift guard catches removal; not a current defect | deferred (advisory; phase passed) |
| v7.4 Phase 108/109 code-review INFOs (5 informational items) | STATE.md ledger (future_milestone) | 1 | Phase 108/109 code review SUMMARY — 5 INFO items; pre-existing non-blocking; tracker ref: "5 v7.4 code-review INFOs" | deferred (pre-existing non-blocking informational items) |
| `theoretical-limit`↔`inversion` merge (TLINV-01) | STATE.md ledger (future_milestone) | 1 | `docs/expansion-measurement-verdict.md` §"Second candidate pair" — gated on a clean S-P14 live re-measurement; merge pair confirmed by prior overlap analysis but S-P14 is spend-limit-INDETERMINATE | deferred (gated on clean S-P14 re-measure; TLINV-01) |
| `estimate` merge partner scoping (ESTPART-01) | STATE.md ledger (future_milestone) | 1 | `docs/expansion-measurement-verdict.md` §"Newly-evidenced candidate" — `estimate` scored 0/5 FAIL on clean evidence; no pre-named merge partner; behavioral scoping needed | deferred (no pre-named partner; ESTPART-01) |

### Sweep Boundary

**What was combed:** The complete STATE.md §"Deferred Items" ledger (all 14 rows across
carry_forward, code_review_deferred, future_milestone, and nyquist_gap categories) plus a
targeted pass over the named debt classes: stray empty `shared/skills/` dirs, the
`sync-content.py` module-level vs `generate_all()` docstring count contradiction,
stale-docstring counts and the `.py#anchor` resolver in `check-traceability.py`, and the
stale-count pytest fixture assertions. Each item was re-confirmed as reproducing in the
current repo before being cited with file/line evidence (D-02).

**What was not combed:** No exhaustive tree walk of the full repo, no scan of the generated
`first-principles/` tree, no third-party dependency audit, no git-history archaeology, no
live `claude` session. This is an offline static inspection of the ledger plus the bounded
debt classes. Unknown debt outside those classes is not in scope for this audit.

---

## ALIGN-03: Prioritized Ranking Table

One sortable table per D-01. Composite = Severity × Leverage × Offline-fixability (range
1..27). The composite drives sort order (descending); the Disposition column records the
v7.10-scope decision: the fix-now subset is exactly the offline-provable hygiene items with a
DEBT-* requirement (all Offline-fixability 3), chosen for v7.10 scope. The remaining items are
deferred for a **mix** of reasons — *not* uniformly because they are un-fixable offline: the
method-fidelity gaps (METHFID-*) need a full technique-authoring milestone, the live
re-measures (LIVE-RR114 / LIVE-SP10SP14) need fresh live budget, the merge candidates
(TLINV-01 / ESTPART-01) are gated on a future re-measure, and the advisory / low-impact
code-review residuals are deferred for being non-blocking and out of v7.10 scope (even where
their Offline-fixability is 2-3). Offline-fixability 3 is therefore necessary but not
sufficient for fix-now — several deferred rows also carry Offline-fixability 2-3.

| Item | Severity | Leverage | Offline-fixability | Composite | Disposition |
|------|----------|----------|--------------------|-----------|-------------|
| Stale traceability-tooling docstrings + `.py#anchor` resolver (WR-01/WR-02/WR-03) | 2 | 3 | 3 | 18 | fix-now → DEBT-03 (Phase 126) |
| Stale-count pytest fixtures (`test_81_inventory` 26→40; `test_step0_live_task1` 28→35) | 2 | 3 | 3 | 18 | fix-now → DEBT-04 (Phase 126) |
| Gap #4 No outside-view / base-rate guard (`reference-class`) | 3 | 3 | 1 | 9 | deferred → METHFID-REFCLASS |
| Gap #3 Uncalibrated confidence (`calibrate`) | 3 | 2 | 1 | 6 | deferred → METHFID-CALIB |
| Gap #5 Inference validity unchecked (`argument-map`) | 3 | 2 | 1 | 6 | deferred → METHFID-ARGMAP |
| `sync-content.py` generator-count contradiction (module docstring 12 vs `generate_all()` 13) | 1 | 2 | 3 | 6 | fix-now → DEBT-02 (Phase 125) |
| RR-114-01: S-P02 inversion live pass-rate re-measure | 3 | 2 | 1 | 6 | deferred → LIVE-RR114 |
| S-P10 (`estimate`) + S-P14 (`theoretical-limit`) clean live re-measure | 2 | 2 | 1 | 4 | deferred → LIVE-SP10SP14 |
| Tier-3 strongest-opposing-case (`steelman`) | 3 | 1 | 1 | 3 | deferred → METHFID-STEELMAN |
| Stray empty skill dirs `shared/skills/rollback-test/` + `shared/skills/testing/` | 1 | 1 | 3 | 3 | fix-now → DEBT-01 (Phase 125) |
| Nyquist `XX-VALIDATION.md` ceremony gap Phases 94-119 | 1 | 1 | 3 | 3 | fix-now → DEBT-05 (Phase 127) |
| P105/P121 code-review deferrals (advisory; phases passed) | 1 | 1 | 3 | 3 | deferred (advisory) |
| `check-step0-live.py` generator round-trip (P95 WR-02) | 1 | 1 | 2 | 2 | deferred (low tooling impact) |
| v7.4 code-review INFOs (5 informational items, Phase 108/109) | 1 | 1 | 3 | 3 | deferred (pre-existing non-blocking) |
| `theoretical-limit`↔`inversion` merge (TLINV-01) | 1 | 1 | 1 | 1 | deferred (gated on S-P14 re-measure; TLINV-01) |
| `estimate` merge partner scoping (ESTPART-01) | 1 | 1 | 1 | 1 | deferred (no pre-named partner; ESTPART-01) |

**Fix-now subset (v7.10 scope):** exactly {DEBT-01, DEBT-02, DEBT-03, DEBT-04, DEBT-05}
mapped to Phases 125-127. These are the five offline-provable hygiene items; all five score
Offline-fixability 3. Every method-fidelity gap is deferred to its verbatim METHFID-* ID;
every live re-measure is deferred to LIVE-RR114 / LIVE-SP10SP14; all other deferred rows
carry a reason or a named milestone ID.

---

## Artifacts This Phase Produces

| Artifact | Status |
|----------|--------|
| `docs/agent-goal-alignment-audit.md` | **New** — this file; the authoritative evaluation inventory for v7.10 |
| `docs/requirements-traceability.md` | **Edited** — cross-reference link to this audit added in Plan 02 (D-03) |

---

*Decision recorded: 2026-06-27*
*Authored in: Phase 124-agent-goal-alignment-audit, Plan 01*
*Supersedes: nothing (first agent-goal alignment audit artifact)*
