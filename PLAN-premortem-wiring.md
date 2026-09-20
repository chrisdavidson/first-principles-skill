# Phased plan: make the pre-mortem technique actually execute

**Status.** Phases 0-4 executed 2026-09-20 in `shared/`, synced, battery re-run. Phase 5's live
re-measurement is the remaining leg. Per-phase execution notes are recorded inline below under
each phase heading. Originally drafted as plan only; Derived from `PLAN-PRAOR-loop-backlog.md` item
**D3 / 999.141** ("Wire pre-mortem + inversion-of-headline into Phase 5's Operation; wire trade-off
into Phase 4's"), which that document sizes as *small* and ranks inside workstream D. This plan
promotes it to its own sequence because it is the one item that both closes a wiring gap **and**
delivers the requested increase in the agent's output verbosity — the missing content *is* the
verbose content.

**Backlog numbering.** `.planning/ROADMAP.md` currently runs to `999.129`. IDs proposed here start
at `999.130`. Reservations, not registrations.

**Milestone context.** v9.4.0 shipped 2026-09-20 at `172db6e`; `.planning/STATE.md` reports
`status: shipped`, no milestone open, battery `FIREWALL: GREEN (23/23)`, coverage `228/167/0/395`.
This is therefore new-milestone work (v9.5.0 candidate), not an insertion.

---

## 1. The defect, stated precisely

`PLAN-PRAOR-loop-backlog.md` §5 D3 and `REVIEW-technique-improvement-analysis.md` §A1 both say
pre-mortem "is invoked from zero phases". Checked in the tree on 2026-09-20, that is exactly right
about the *prescription* and slightly wrong about the *behaviour*. Both halves matter.

### 1.1 The prescription gap (confirmed)

`{{TOOL:pre-mortem}}` appears **twice** in `shared/spine/SKILL-body.md`:

| Line | Context | Is it an instruction? |
|---|---|---|
| `:64` | Step 0 routing table — the phrase list that routes a *user prompt* to `/pre-mortem` | No. Routes away from the composer, never into a phase |
| `:401` | `## Companion tools` summary — "Use during Phase 5 (Validate) to stress-test…" | No. A description of when it *would* apply |

No phase Operation, no phase exit criterion, and no rubric criterion names it. Compare
second-order, which is prescribed in Phase 4's Operation *and* made mandatory by exit condition
(3) of the ALL FOUR clause at `:165`. That is the shape a wired technique has; pre-mortem has
none of it.

**Consequence:** Phase 5 — the phase whose own "Why this phase exists" calls it *"the adversarial
pass"* — has no adversarial technique attached. Its Operation (`:175`) prescribes free-form
weakest-link inspection by the same model that wrote the chains, and nothing else.

### 1.2 The behaviour (measured, and the reason this is worth fixing rather than filing)

Pre-mortem is not absent from output. It is **discretionary and shapeless**:

| Surface | Runs with some pre-mortem content | Runs with none |
|---|---|---|
| `tests/live-conformance-v9.0/*.md` (8 captures) | 4 (`PR-P1`, `PR-P1-R2`, `Q-P1`, `Q-P2`) | 4 (`PR-N1`, `PR-N2`, `PR-P2`, `Q-P3`) |
| Root demos (2) | 2 (`DEMO-…-multiregion-latency.md:394`, `DEMO-…-ticket-triage.md:591`) | 0 |

Where it appears, its shape varies from a full sub-section with premise, causes, clusters and
per-cluster dispositions (`DEMO-…-multiregion-latency.md:394-420`) down to a single italic
sentence folded into another paragraph (`Q-P1.md:230`). Nothing requires either form, so nothing
distinguishes them.

**Erratum, 2026-09-20, found by Phase 48 research.** The row above originally read *"(9 captures)"*
and *"5 … plus a citation in `PR-P1`'s Criterion 4 justification"*. Both were wrong. There are **8**
`.md` captures under `tests/live-conformance-v9.0/` (`ls` excluding `README.md`; the catalog states 8
rows), and the "5" double-counted `PR-P1` — once as a capture carrying a pre-mortem, and again as a
citation *inside that same file*. The correct split is 4 present / 4 absent.

The headline is unaffected and was independently correct: **6/10 present** is 4 captures plus the 2
root demos, over a population of 8 + 2 = 10, which is the `N = 10` the baseline table in §3 states
and the number MEAS-05's like-for-like check re-asserts. What was wrong was the breakdown offered in
support of it — a defect in the evidence, not in the reading. It is recorded rather than silently
corrected because a miscount inside a document arguing for better provenance is the same class of
error this milestone exists to fix.

**This is the sharpest statement of the defect:** the agent is currently *rewarded identically*
for a rigorous pre-mortem, a one-line gesture at one, and silence. Criterion 5's `Absent` band
fires only when "no weak-link identification or chain inspection was performed at all" — a
free-form weakest-link paragraph satisfies it. An omitted pre-mortem is invisible; a thorough one
is unscored.

### 1.3 Why this is the verbosity lever

The output the wiring adds is substantial and structured, not filler: a restated past-tense
premise, an unfiltered cause list, clustered structural weaknesses, and a named plan change or an
explicitly accepted risk per cluster — roughly 25-40 lines of process output per analysis, in the
shape `DEMO-…-multiregion-latency.md:394-420` already demonstrates. It lands as process output
before the Phase 5 verdict blocks, following the precedent already set by the Phase 4 Assumption
Audit scan table (`SKILL-body.md:161`), the §6→§4 closure ledger and the self-audit scan
(`:260ff`). No new output section is created; the fixed six-section template shape is unchanged.

### 1.4 The twin gap, in scope because it is the same edit

Trade-off has the identical defect one phase earlier: one mention in Phase 4's Operation, and it
is inside a decision-rule parenthesis (*"trade-off = qualitative weighted scoring"*), never an
instruction. `trade-off.md:118-121` already defines the collapse-into-a-chain form the wiring
needs. Doing it in the same sequence costs one extra sentence and one extra rubric clause.

---

## 2. Target state (falsifiable)

1. Phase 5's Operation prescribes an adversarial technique with a stated applicability test, and an
   honest `not applicable — [reason]` record when the test does not fire.
2. Phase 5's exit criterion will not admit a silently-skipped adversarial pass, in the same words
   Phase 4's exit condition (3) uses for second-order.
3. The pre-mortem emits a **named artifact** with a required shape, as process output before the
   verdict blocks.
4. Criterion 5 can tell the three cases apart: contract satisfied, gesture, absent.
5. The baseline rate from §1.2 is re-measured after the change, with its N, as an observation and
   never a gate (K-of-5 discipline, `docs/v8.7-constraint-teardown.md` §2 item 3).
6. `FIREWALL: GREEN` at the same 23/23, with every fixture update in the same commit as the source
   edit that required it.

---

## 3. Phases

### Phase 0 — Baseline before touching `shared/` (apparatus). 999.130

`PLAN-PRAOR-loop-backlog.md` §6 ordering constraint 1: editing the body first destroys the artifact
that demonstrates the gap, and the next run is a different prompt.

- Write a deterministic extractor over the 9 `tests/live-conformance-v9.0/*.md` captures and the 2
  root demos scoring each for: premise restated in past tense y/n; cause count; clusters named y/n;
  per-cluster disposition (plan change **or** named accepted risk) y/n.
- Record the reading with its N in the plan record. §1.2's 5/9 is the headline; the shape columns
  are what Phase 4 re-reads.
- **No `shared/` edit in this phase.** Captures under `tests/live-conformance-v9.0/` are registered
  `_FROZEN_PATHS` entries — FROZEN-EVIDENCE asserts they are unmodified relative to HEAD. Read
  them; do not regenerate them.

**Baseline reading, taken 2026-09-20 (N = 10):**

| file | present | premise | causes | clusters | disposition |
|---|---|---|---|---|---|
| `PR-N1.md` | no | - | - | - | - |
| `PR-N2.md` | no | - | - | - | - |
| `PR-P1-R2.md` | yes | yes | 3 | yes | yes |
| `PR-P1.md` | yes | yes | 9 | yes | yes |
| `PR-P2.md` | no | - | - | - | - |
| `Q-P1.md` | yes | yes | 6 | yes | **no** |
| `Q-P2.md` | yes | **no** | 0 | yes | yes |
| `Q-P3.md` | no | - | - | - | - |
| `DEMO-…-multiregion-latency.md` | yes | yes | 15 | yes | yes |
| `DEMO-…-ticket-triage.md` | yes | yes | 9 | **no** | yes |

- **pre-mortem content present: 6/10**
- **all three shape columns satisfied: 3/10**
- cause count where present: 0, 3, 6, 9, 9, 15 *(six values, one per present row)*

**Erratum, 2026-09-20, found by Phase 48 planning.** The bullet above originally read
*"0, 0, 3, 6, 9, 9, 15"* — **seven** values for **six** present rows, with a spurious extra `0`. The
table's own cells are the authority and read 3, 9, 6, 0, 15, 9; the `6/10` and `3/10` aggregates
derive from the table, not from this bullet, and §1.2's erratum independently corroborates them, so
MEAS-05's like-for-like check is unaffected. Recorded rather than silently rewritten, in the same
form §1.2 uses: this is the second miscount found in this document's own evidence, both in summaries
of a table that was itself correct.

`Q-P2`'s `causes = 0` is a true reading, not an extractor miss: its clusters are written inline as
`**(i)** … **(v)**` inside a single italic paragraph, with no enumerated cause list before the
grouping — the compression the contract in Phase 2 is meant to stop. The step the technique calls
load-bearing (`pre-mortem.md:37-39`, write the full list *before* reviewing it) did not happen
there.

**One instrument note, because it changes the reading.** The extractor's first cut anchored on the
first `pre-mortem` match in each file and scored both root demos `no` on every column. That was the
instrument failing: in both demos the first mention is meta-discussion of the technique
(`DEMO-…-multiregion-latency.md:241`, `DEMO-…-ticket-triage.md:83`) and the pre-mortem itself is
hundreds of lines later under its own heading, whose body blocks never repeat the word. Anchoring
on *every* match with a 30-line window fixed it, and the strongest capture in the set then scored
strongest. A baseline that had been taken with the first-anchor version would have understated the
present rate as 4/10 and the shape rate as 1/10.

**MEAS-05 like-for-like reading, taken 2026-09-20 (Phase 48 plan 48-01), instrument:
`scripts/measure-adversarial-pass.py --score`.** The extractor above existed only as prose in this
document until now; `scripts/measure-adversarial-pass.py` is a tracked, re-runnable script
implementing both corrections named above (anchor on every match, not the first; anchor on both
`pre-mortem` and the `Adversarial pass` heading). Re-scoring the same ten named files:

| file | present | premise | causes | clusters | disposition |
|---|---|---|---|---|---|
| `PR-N1.md` | no | - | - | - | - |
| `PR-N2.md` | no | - | - | - | - |
| `PR-P1.md` | yes | yes | 9 | yes | yes |
| `PR-P1-R2.md` | yes | yes | 3 | yes | yes |
| `PR-P2.md` | no | - | - | - | - |
| `Q-P1.md` | yes | yes | **0** | yes | no |
| `Q-P2.md` | yes | no | 0 | yes | yes |
| `Q-P3.md` | no | - | - | - | - |
| `DEMO-…-multiregion-latency.md` | yes | yes | **5** | yes | yes |
| `DEMO-…-ticket-triage.md` | yes | yes | **4** | no | yes |

- **present: 6/10** — reproduces the table above row for row on this column.
- **all three shape columns satisfied: 3/10** — the same three rows (`PR-P1.md`, `PR-P1-R2.md`,
  `DEMO-…-multiregion-latency.md`) satisfy premise AND clusters AND disposition, and every
  present/premise/clusters/disposition cell above reproduces the corresponding cell in the Phase 0
  table exactly.

**Differing `causes` cells, recorded rather than tuned away.** `causes` is a count, not a shape
column — it feeds neither aggregate above — and three of the six present rows differ from the
hand-read table:

- `Q-P1.md`: table reads 6, instrument reads **0**. The instrument's window carries no literal
  `cause`/`causes`/`caused` token at all — the file's pre-mortem sentence names "three clusters" by
  label (`deferral-without-a-deadline`, `ownership vacuum`, `political cost`) without using the
  word "cause" anywhere nearby, so the instrument's cause-keyword anchor never fires. Zero is an
  honest miss, not a tuned answer.
- `DEMO-…-multiregion-latency.md`: table reads 15, instrument reads **5**. The instrument counts
  the first enumerated list immediately following the first `cause`/`caused` mention in its 30-line
  window — the five "Plan A … What caused it?" bullets — and does not also fold in the four
  numbered structural-weakness labels, the three Plan B causes, or the three nested `Mitigation:`
  lines a human reader evidently also counted toward 15.
- `DEMO-…-ticket-triage.md`: table reads 9, instrument reads **4** — the four `Pre-mortem findings`
  bullets, each already paired with its own disposition; the table's 9 counted a wider span than
  this instrument's window reaches.

**Assessment of those three, added 2026-09-20 after independent re-reading.** The record above is
accurate on the mechanism and slightly too hard on the new instrument. Two corrections:

**`Q-P1`'s `0` is correct, not "an honest miss."** That file's pre-mortem is a single italic
sentence naming three clusters by label; it enumerates **no** causes at all. Zero is the right
reading of "enumerated causes written before grouping". What needs explaining is not the new `0` but
the **old `6`** — and the explanation is window bleed: the original instrument counted line-start
bullets in a fixed 30-line window after the anchor, and the 30 lines following `Q-P1`'s pre-mortem
sentence contain 12 bullets belonging to **section 6's Conclusion**, not to the pre-mortem. Verified
by direct read of `Q-P1.md:230-260`.

**The old counts conflated categories the contract separates.** `DEMO-…-multiregion-latency.md`'s
`15` is 5 Plan A causes + 4 structural weaknesses + 3 Plan B causes + 3 `Mitigation:` lines — that is
causes *plus clusters plus dispositions*, three of the contract's four parts summed into one number.
The new instrument's `5` counts causes only. So the corrected range is **0 to 9**, and the old
"0 to 15" was never a range of cause counts.

**What this strengthens, and it is worth being explicit.** Every boolean column — `present`,
`premise`, `clusters`, `disposition` — and both aggregates (`6/10`, `3/10`) now agree across **two
independently written instruments**, one of which bled its window and one of which does not. That
agreement is stronger evidence for the baseline than the original single reading was. The column
that diverged is the one no aggregate depends on, and it diverged because the first instrument was
measuring something looser than it claimed.

None of these three differences moves `present` or `shape-complete`, which is what MEAS-05
requires. They are recorded, per this plan's own governing rule, because tuning the extractor until
the `causes` numbers matched the hand-read table would be exactly the failure mode this requirement
exists to prevent — an instrument corrected against its target reading is not a correction.

**Reproducibility bound.** Two of these ten files — `DEMO-first-principles-multiregion-latency.md`
and `DEMO-first-principles-ticket-triage.md` — are untracked at the repository root by deliberate
decision (`.planning/STATE.md`; neither EVID-01 nor the roadmap's Phase 47 Success Criterion 5
names them). This reading therefore re-runs on this working tree but not on a fresh clone; D-48-C
accepts and discloses that bound rather than closing it by tracking the two files.

**Exit:** a recorded baseline table, N stated, nothing in `shared/` modified.

### Phase 1 — Wire the invocation (product). 999.131

**Executed.** `shared/spine/SKILL-body.md` Phase 5 Operation gained the **Run the adversarial pass** block and the exit criterion became ALL THREE. One deviation from the plan as written, and it is the deviation that matters: the wiring does **not** use the `{{TOOL:pre-mortem}}` token the other prescribed techniques use. That token substitutes the phrase *"the inlined pre-mortem procedure"* (`shared/spine/tool-map.yml:8`), and the procedure is not inlined — it ships as a reference sibling. Telling an agent to apply an inlined procedure that is not inlined is an instruction to work from recollection, which is precisely the failure this phase exists to fix, and is the same class of defect `CLAUDE.md` warns about under Token substitution. The wiring therefore uses an explicit Read imperative against the `${CLAUDE_PLUGIN_ROOT}`-anchored path, following the precedent the rubric read and the output-template read already set, with a stated fallback when the read fails.

`shared/spine/SKILL-body.md`, Phase 5 Operation (`:175`) and exit criterion (`:179`).

- Operation gains, after the weakest-link sentence: when the analysis's conclusion is a **plan or
  recommendation**, apply the pre-mortem procedure to it; when it is a **claim**, invert the
  headline conclusion using the inversion procedure. The decision rule already exists and is
  already written down — `inversion.md:28-31` ("inversion stress-tests a **claim**; pre-mortem
  stress-tests a **plan**") — so this wiring cites an existing rule rather than inventing one.
- Each structural weakness found becomes a named weak link or a confidence caveat, which is the
  handoff `pre-mortem.md:105-110` already specifies and nothing currently consumes.
- Exit criterion gains a third condition in Phase 4's own words: a silently-skipped adversarial
  pass does not satisfy this criterion and does not exit this phase.
- Honest-depth escape: an analysis whose conclusion is neither a plan nor a claim records one line
  `adversarial pass not applicable — [reason]`. This is what keeps the change from becoming the
  mandatory padding `REVIEW-technique-improvement-analysis.md` §A2 objects to elsewhere.

**Correction, 2026-09-20, found by Phase 47 research.** PASS-01's parenthetical originally read
*"The two procedures state this same rule themselves; it is cited here, not re-authored."* That was
false: `shared/references/inversion.md:28-31` and `:146` state the rule, and
`shared/references/pre-mortem.md` contains **zero** occurrences of "inversion". The plural claim was
wrong, and it was wrong inside the clause asserting the rule was cited rather than authored — the
same construction as v9.4.0's RF-01. Corrected to name the one procedure that carries the rule and
to state that pre-mortem names trade-off and five-whys as its neighbours and not inversion. The
residual the correction exposed — pre-mortem.md's missing inversion boundary — is filed as backlog
**999.130** rather than fixed here, because it edits a file outside this milestone's four and
changes a `{{PROCEDURE:pre-mortem}}` surface the `/pre-mortem` stub renders. Battery re-run after
the correction: `FIREWALL: GREEN (23/23)`.

**Gate blast radius:** `SKILL-body.md` edits regenerate the whole agent tree. SCAN-GUARD pins the
Phase-4 scan-table sentence and 100 clause-level branches; HARN-01 pins the Phase 3 verification
step; HARN-02 pins the re-entry edges. None of those slices is touched by a Phase 5 Operation
edit, but all three read the emitted tree — run the battery, expect fixture work.

### Phase 2 — Give it an output contract (product). 999.132

**Executed.** `shared/references/pre-mortem.md` gained an `## Output contract` section (premise / causes / clusters / disposition), and step 2 gained the three-viewpoint generation rule while step 3's "would I have suppressed this in a group?" became a single-analyst test — look for the softened items, not the missing ones. The contract reaches three surfaces from that one edit: the agent reference sibling, the `/pre-mortem` skill stub via `{{PROCEDURE:pre-mortem}}`, and the emission instruction in the body.

This is the phase that delivers the verbosity.

- `shared/references/pre-mortem.md`: add an **Output contract** section after the Procedure —
  premise line, the unfiltered cause list, the clusters, and per cluster a named plan change or an
  explicitly accepted risk with a named mitigation. The exit criterion at `:57-62` already requires
  all four; it simply never says what they look like on the page.
- `shared/spine/SKILL-body.md`: name the artifact and place it — emitted as process output before
  the Phase 5 verdict blocks, on the Assumption Audit scan table's precedent, **not** a seventh
  output section.
- Each cluster cites the chain ids (`Cn`) or ground-truth ids (`GT-N`) it bears on, so the
  pre-mortem joins the existing traceability surface instead of floating beside it. The demo
  already does this unprompted (`DEMO-…-multiregion-latency.md:398-401`, clusters citing C5/C6,
  C1/C2, C3/C8, C9) — the contract makes it required.
- While here, `REVIEW-technique-improvement-analysis.md` §A5's cheap fix: pre-mortem step 3's
  *"Would I have suppressed this in a group?"* is guidance for facilitated human sessions and does
  nothing for a single model. Replace with perspective rotation across at least three named
  stakeholders. This is what actually makes the cause list longer and less generic.

**Gate blast radius:** `pre-mortem.md` feeds three surfaces — the agent reference sibling, the
`/pre-mortem` skill stub via `{{PROCEDURE:pre-mortem}}`, and HARN-03's parity token set. Adding
headers to it does **not** touch `_TECHNIQUE_CATEGORIES['pre-mortem']` (9 markers, asserted by
INVARIANT-CHECK) — those are prompt/transcript phrase markers in `scripts/_battery_core.py`, not
document headers. See Phase 5 for the one real interaction.

### Phase 3 — Make it scoreable (product). 999.133

**Executed.** Criterion 5 gained clauses on three bands: Rigorous (record complete, every weakness landed), Hand-wavy (record present, no cluster carries a disposition — the gesture case — or clusters without the cause list they came from), Absent (neither a record nor the not-applicable line anywhere). The Absent clause states explicitly that it is a separate reading from the existing stress-test clause, because a free-form weakest-link paragraph satisfies that one and is exactly what the new clause is meant to catch. The predicted gate interaction did not fire: both HC-BOUND and HARN-01's Criterion 5 scope guard passed unchanged, and no fixture needed updating. The guard HARN-01 enforces is that the literal `**Fix — acquire before you downgrade.**` stays Criterion-3-local; the added clauses do not contain it.

Without this, the gate still cannot tell §1.2's three cases apart and the wiring is unenforced.

`shared/spine/references/validation-rubric.md`, Criterion 5 (`:413`):

- `Absent` gains a clause: no adversarial-pass artifact and no `not applicable` record.
- `Hand-wavy` gains: an adversarial pass whose clusters carry no disposition — the gesture case.
- `Rigorous` gains: every cluster carries a named plan change or an explicitly accepted risk with a
  named mitigation, and cites the chain or ground truth it bears on.

**Gate blast radius — the sharp one.** HC-BOUND (`scripts/check-high-confidence-bound.py:66`,
`_CRITERION5_START`) reads the Criterion 5 slice and asserts the Rigorous descriptor's
HIGH-confidence bound plus all three documented EXCEPT exceptions. `check-act-limb.py:84`
(`_CRIT5_START`) uses the same slice as a **scope boundary**, with negative controls (`ar`, `bv`)
asserting that Criterion-3-local text does *not* appear in it. Additive clauses that do not
mention the HIGH bound or the Fix-note lead should clear both, but this phase lands with its
fixture updates in the same commit or it does not land.

### Phase 4 — Trade-off, the same edit one phase earlier (product). 999.134

**Executed.** Phase 4's Operation now opens the trade-off procedure by anchored path when two or more viable options survive the ground truths, and collapses the result into a chain per the output template's §4 conversion rule. Exit criterion deliberately unchanged — surviving options are conditional in a way an adversarial pass is not.

`SKILL-body.md` Phase 4 Operation: when two or more viable options remain after ground truths are
established, apply the trade-off procedure and collapse the result into a chain per
`output-template.md` §4. The collapse form exists at `trade-off.md:118-121`. Exit criterion
unchanged — options are conditional in a way the adversarial pass is not, so this is a prescribed
technique, not a mandatory one.

### Phase 5 — Re-measure and reconcile the gates (apparatus). 999.135

**Executed, with one measurement retracted and re-taken.**

**Gates.** `sync-content.py --write` then `check-firewall-battery.sh` → `FIREWALL: GREEN (23/23)`,
run twice: once after Phases 1-2 and again after Phases 3-4. HC-BOUND and HARN-01, the two gates
that read the Criterion 5 slice, passed unchanged with no fixture updates. The risk this plan
recorded for Phase 3 did not fire, and the reason is that HARN-01's Criterion 5 guard is narrower
than the plan assumed: it enforces that the literal `**Fix — acquire before you downgrade.**`
stays Criterion-3-local, which additive band clauses do not touch.

**The first live reading was inconclusive and is retracted.** A `claude -p --plugin-dir
./first-principles` run on a plan-shaped prompt returned an analysis that mentioned trade-off
scoring with weights locked before scoring, and a pre-mortem producing clusters with plan-change
dispositions. Neither is evidence: the outer session *delegated*, so only its summary of the
sub-agent reached the capture, and both constructs already exist in the v8.24.0 body's Companion
tools summary and in `pre-mortem.md`'s original exit criterion. The run distinguishes nothing.

**What made a decisive reading possible.** The installed plugin cache is `v8.24.0` and contains
zero occurrences of `Run the adversarial pass`, `Weighting the criteria before scoring`,
`Trade-off procedure` and `ALL THREE conditions`; the working tree contains one of each. A
cache run and a `--plugin-dir` run are therefore cleanly separable by inspection of the output.

**The decisive reading.** Re-taken through the repo's own `--probe` transport
(`check-quality-harness.py --probe Q-P3 --catalog tests/live-conformance-catalog.md
--plugin-dir ./first-principles`), which extracts the *sub-agent's* analysis rather than the
parent's summary. `Q-P3` was chosen because its frozen baseline capture contains **no pre-mortem
at all** — same prompt, same transport, old body produced nothing.

| | present | premise | causes | clusters | disposition |
|---|---|---|---|---|---|
| `Q-P3` baseline (old body, frozen) | **no** | - | - | - | - |
| `Q-P3` re-run (wired body) | **yes** | yes | 16 | yes (5) | yes (5/5) |

The emitted record carries the prescribed heading `## Adversarial pass (process output)`, a
past-tense premise, 16 causes written before grouping from five named viewpoints (homeowner,
installer, payer, a future buyer's inspector, the window contractor who lost the job), an
adversarial-interrogation paragraph in the single-analyst form Phase 2 introduced, and five
clusters in a table whose columns are `Cluster | Causes | Bears on | Disposition` — every cluster
citing GT/chain ids, every one carrying a plan change or an accepted risk with a named mitigation.

**The rubric clause is live and did not rubber-stamp.** The run's own Criterion 5 verdict block
cites the pass — "the adversarial pass ran with a past-tense premise, a 16-cause unfiltered list
from five viewpoints written before grouping, and five clusters each citing chain/GT ids and each
carrying a plan change or an accepted risk with a named mitigation" — and then bands the criterion
**below Rigorous anyway**, on the pre-existing no-HIGH-chain clause. The new clause is being
evaluated as one input among several rather than read as a pass.

**SUPERSEDED 2026-09-20 by the Phase 48 K-of-5 reading — the paragraph below stands as the honest
statement it was at the time, and its own caveat was correct.** MEAS-03 has since taken the reading
it called for: **N = 5, present 5/5, shape-complete 5/5**, over the five distinct plan-shaped catalog
rows (`Q-P1`, `Q-P2`, `Q-P3`, `PR-P1`, `PR-P2`) against the committed wired body, captured under
`tests/adversarial-firing-v9.5/` with its own provenance README. It remains a recorded observation
and gates nothing. MEAS-04's companion reading found **no classifier drift** — all five classify
`full-composer` — but found the *mechanism* differs from the prediction: `pre-mortem` never fires as
a technique at all (1 of 9 markers, below `MIN_HEADER_HITS=2`), so the CR-02 ceiling never had to
act for it, though it was exercised on `PR-P2`'s lone `fishbone` hit.

**A third instrument correction, found by that reading rather than by inspection.** `Q-P3`'s fresh
record scored `disposition: no` — a false negative on a record carrying 15 causes, 6 clusters and 6
dispositions, verified by reading it. Cause: `WINDOW_LINES = 30`. The same arbitrary constant caused
both of this instrument's failures in opposite directions — too long it bled into output section 6
(the spurious baseline `6` for `Q-P1`), too short it missed a dispositions block beginning ~40 lines
past the anchor. The window is now bounded by the next top-level heading, the boundary the output
contract itself defines. The ten frozen baseline files still return **6/10 present and 3/10
shape-complete** under it — the same aggregates two earlier, differently-windowed instruments
produced, which makes those aggregates considerably better evidenced than a single reading could.

**N = 1.** This is a recorded observation, not a rate, and it is subject to the same K-of-5 noise
discipline as every other live reading in this repository (`docs/v8.7-constraint-teardown.md` §2
item 3). It establishes that the wiring *can* fire and what it emits when it does. It does not
establish how often. A K-of-5 reading across the plan-shaped catalog rows is the honest next
measurement, and it is not taken here.

**A second instrument correction, same class as Phase 0's.** The baseline extractor anchored on
the literal `pre-mortem`, and the wired body emits the record under `## Adversarial pass` — so it
scored the new capture `premise=no, disposition=no` against text that plainly carried both. The
anchor was widened to `pre-mortem|adversarial pass`. Re-scoring the ten baseline captures with the
widened anchor returns **6/10 and 3/10 unchanged**: the old captures never use the new phrase, so
the widening is a no-op on them and the before/after comparison is like-for-like. Had the reading
been taken without this correction, the wiring's own output would have scored worse than the
baseline it improves on.

**The baseline side of the MEAS-04 classifier reading, taken 2026-09-20 (Phase 48 plan 48-01),
instrument: `scripts/measure-adversarial-pass.py --classify`.** Before any live usage is spent on a
fresh capture, the same frozen chain (`_battery_core._technique_hits` →
`MIN_HEADER_HITS`-derived `fired` → `_composer_structure_hits` → `classify`) is run over the same
ten named baseline files, proving the feeder works on real capture text and putting the "before"
column of the drift reading on the record. Same reproducibility bound as the MEAS-05 reading in
Phase 0: two of these ten files are untracked at the repository root by deliberate decision, so
this reading re-runs on this working tree but not on a fresh clone.

| file | fired | len(fired) | composer_structure_hits | verdict |
|---|---|---|---|---|
| `PR-N1.md` | `[]` | 0 | 13 | `full-composer` |
| `PR-N2.md` | `['fishbone', 'trade-off']` | 2 | 11 | `full-composer` |
| `PR-P1.md` | `['fishbone', 'inversion', 'trade-off']` | 3 | 14 | `full-composer` |
| `PR-P1-R2.md` | `['fishbone']` | 1 | 11 | `full-composer` |
| `PR-P2.md` | `[]` | 0 | 20 | `full-composer` |
| `Q-P1.md` | `['fishbone']` | 1 | 17 | `full-composer` |
| `Q-P2.md` | `[]` | 0 | 16 | `full-composer` |
| `Q-P3.md` | `[]` | 0 | 10 | `full-composer` |
| `DEMO-…-multiregion-latency.md` | `['pre-mortem', 'trade-off']` | 2 | 26 | `full-composer` |
| `DEMO-…-ticket-triage.md` | `['trade-off']` | 1 | 25 | `full-composer` |

All ten verdicts are `full-composer`, at `composer_structure_hits` ranging 10-26 against
`_COMPOSER_FOCUS_CEILING = 4` — the frozen composer-structure override wins every row, including
the two rows where `len(fired) == 1` (`PR-P1-R2.md`, `Q-P1.md`), because both carry
`composer_structure_hits` far above the ceiling. This is the "before" reading a fresh wired-body
capture's verdict is compared against once plan 48-03 takes the "after" side.

**Not done: the routing-classifier drift check.** `_battery_core.classify()`'s `n == 1` /
`_COMPOSER_FOCUS_CEILING` interaction remains a prediction. BATT-06 and INVARIANT-CHECK pass, and
the frozen sentinels are byte-frozen and unaffected, but no fresh live routing-battery run has
been taken against a body that now emits pre-mortem markers on every applicable analysis. That
check belongs with the K-of-5 reading above.


- `python3 scripts/sync-content.py --write`, then `bash scripts/check-firewall-battery.sh`.
  Target: `FIREWALL: GREEN (23/23)`.
- Re-run Phase 0's extractor over **fresh** captures. Recorded observation with its N; K-of-5 noise
  discipline; never a gate.
- **Check the routing classifier for drift.** `_battery_core.classify()` resolves `n == 1` to
  `focused-<technique>` unless `composer_structure_hits >= _COMPOSER_FOCUS_CEILING` (4). A body
  that now emits a pre-mortem on every applicable full-composer run fires ≥2 of the 9 pre-mortem
  markers — "has already failed", "structural weakness(es)", "failure causes" all match, and the
  demo output at `:394-420` would score 3. The CR-02 ceiling exists precisely for this case and
  should hold, because a full-composer run carries all four scaffold headers. **It should hold** is
  a prediction, not a measurement: verify it against fresh captures before trusting it. Frozen
  sentinel excerpts are unaffected — they are byte-frozen and do not re-run.

---

## 4. Sequencing and why

```
Phase 0 (baseline, offline, no shared/ edit)
   └─► Phase 1 (wire) ─► Phase 2 (contract) ─► Phase 3 (score)
                                             └─► Phase 4 (trade-off, independent)
                                                    └─► Phase 5 (re-measure + gates)
```

1. **Phase 0 before everything.** Constraint 1 from `PLAN-PRAOR-loop-backlog.md` §6.
2. **Phase 2 before Phase 3.** A rubric clause can only score a contract that exists; scoring a
   shape the body does not prescribe is how Criterion 5 got its current blind spot.
3. **Phase 4 anywhere after Phase 0**, but bundling it with 1-3 pays one sync + battery cycle
   instead of two.
4. **Phase 5 last**, and its gate reconciliation is not optional: Phase 3 touches a slice two
   separate gates read.

**If only one phase ships:** Phases 1 + 2 together. Phase 1 alone makes the agent run a technique
with no required shape, which reproduces §1.2's variance under a mandate. Phase 2 alone documents a
shape nothing invokes.

---

## 5. Risks

- **Padding.** A mandatory adversarial pass on an analysis with no plan and no claim is filler the
  rubric cannot distinguish from analysis — the exact failure `REVIEW-technique-improvement-analysis.md`
  §A2 identifies in Step 0's "enumerate all eight". The `not applicable — [reason]` escape in
  Phase 1 is the mitigation, and it is load-bearing, not decorative.
- **Turn budget.** `SKILL-body.md:20-22` states the gate runs last and is what gets dropped when
  the budget runs out. This plan **net-adds** prescribed work to Phase 5, immediately upstream of
  the gate. `PLAN-PRAOR-loop-backlog.md` B2/999.133 proposes paying for such additions by cutting
  Step 0's "enumerate all eight" padding; this plan does not include that cut, so the addition is
  unpaid. Flagged, not resolved — if Phase 5 measurement shows gate truncation rising, B2 becomes a
  prerequisite rather than a neighbour.
- **Two gates read the Criterion 5 slice** (Phase 3). Fixtures in the same commit.
- **Self-grading remains self-grading.** The same model runs the pre-mortem and scores it. This
  raises the floor — the gate can now tell an omitted adversarial pass from a performed one — and
  does not make the gate adversarial.
