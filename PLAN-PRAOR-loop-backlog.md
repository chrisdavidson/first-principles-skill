# Working plan: making Perceive → Reason → Act → Observe → React the real control loop

**Status.** Planning summary only. Nothing in `shared/`, `first-principles/`, `docs/`,
`.planning/` or any script was modified to produce this file, and no backlog item below has been
filed. Proposed IDs are reservations, not registrations.

**Inputs compared**

| Doc | What it is | Vantage |
|---|---|---|
| `grok-proar-recommends-code-review.md` | External review arguing PRAOR should be the explicit outer control loop the five phases implement | Structural / architectural. Reads the shipped design and the v8.18 record; does not audit a run |
| `REVIEW-technique-improvement-analysis.md` | Line-level audit of the eight companion techniques, Phase 4 and the Phase 5 validation layer, read against `shared/` sources | Content / methodology. Recomputed the worked examples; does not use PRAOR vocabulary at all |

**Also consulted**, because both documents lean on them: `REVIEW-agent-improvement-opportunities.md`
(the single demo-run audit: R1, P1–P6, H1–H5) and `grok-recommendation-confidence-levels.md`
(a deep-dive on P1's confidence-propagation failure). These are the empirical layer under the
two primary inputs.

---

## 1. What the two documents each establish

### 1.1 The PRAOR doc's claims

1. The structural holes are closed (v8.18: Act limb, Observe→Perceive edges, focused parity,
   HARN-01/02/03). Remaining problems are **semantic drift, structural-vs-live enforcement, and
   incomplete React semantics**.
2. **Act** exists in prose and is gated structurally, but nothing measures whether a run
   actually opens a source. MEAS-01/MEAS-02 stay deferred; that is "the largest consistency gap".
3. **React is distributed and under-named.** The four bounded re-entry edges plus the
   degrade-to-caveat rule *are* React, but no surface labels them as one mechanism.
4. **Turn-budget pressure truncates the loop-closing limbs first** (Observe and React run last).
5. **No loop-state artefact** records which edges fired, whether Act was attempted, or the
   current confidence band — so state is silently lost across a Fix/Repeat.
6. Six ordered recommendations; the cheapest (an explicit Control-loop section) is ranked highest.

### 1.2 The technique doc's claims

1. **Two worked examples model the error their own technique warns against** — the estimate
   example is off by ~38,000× and labels it "the right order of magnitude"; theoretical-limit uses
   Carnot (the loosest bound) and overstates headroom against Curzon–Ahlborn (~39% vs 40–42%
   observed).
2. **Wiring gaps** — pre-mortem is invoked from zero phases, trade-off from none; Step 0's
   "Phase 4 enumerates all eight" contradicts the phase text and forces padding.
3. **Validation checks form, not reasoning** — no criterion asks whether a hop follows, whether
   the arithmetic is right, or whether a rival conclusion was considered.
4. **The confidence model rewards HIGH and never defines it** — Criterion 5 Rigorous requires
   every conclusion to rest on a HIGH chain, and HIGH/MEDIUM/LOW are only ever defined as caps.
5. Eight prioritised changes, all tiered **product**, none needing a new gate.
6. Two stub-drift findings (`/reason-upward` "ALL THREE" vs the body's "ALL FOUR";
   `/validate` invoking a retired rubric name at the wrong step) that HARN-03 does not catch.

---

## 2. How they relate: convergence, divergence, and the gap each leaves

### 2.1 Where they converge (these are the load-bearing items)

| Convergent finding | PRAOR doc | Technique doc | Reading |
|---|---|---|---|
| Green structural gate ≠ correct behaviour | Root cause 1; rec 6 | §D1 (gate scores form, not reasoning) | Same defect at two altitudes: the *gate* checks form and the *harness* checks prose. Both need a semantic limb |
| Observe is weak where it matters | "strong inside the document; weak on real-world outcomes" | §D1–D3: no method, no rival, undefined HIGH | The technique doc supplies the missing *content* of the limb the PRAOR doc only names |
| Focused mode diverges | Root cause 2 (disclosed but real) | §D4 (no substantive validation at all) | Agree on the fact, differ on the fix — see 2.2 |
| Turn budget crowds out the loop's tail | Root cause 4; rec 4 | §A2 (mandatory padding), §C6 (parser-workaround prose) | Complementary: the technique doc names *what to cut* to pay for what the PRAOR doc wants *protected* |

### 2.2 Where they pull in different directions

- **Focused mode.** PRAOR rec 3 says keep the residual, make it a mandatory disclosure, add an
  escalation rule. Technique §D4 says add a cheap per-technique semantic check. These are
  reconcilable and should be taken together — the escalation rule is React's exit from focused
  mode, the semantic check is the Observe limb that makes escalation decidable. Taking only the
  disclosure leaves focused mode with a documented hole and no detector.
- **Body length.** PRAOR rec 1 and rec 5 both *add* prose to `SKILL-body.md` (a Control-loop
  section and a loop-state block). Technique §C6 observes the body is already carrying
  measuring-tool caveats that cost the model attention. Net-add to the body is a real cost under
  root cause 4, the PRAOR doc's own concern. Any Control-loop section should be paid for by the
  §A2 padding cut and the §C6 relocation, not stacked on top.
- **"Structural work is solid; only consistency remains."** The PRAOR doc asserts this. The demo
  review falsifies the strong form of it: the run emitted a complete six-criterion gate having
  opened **zero** reference files, in a verdict vocabulary that does not exist. That is not
  drift — Observe fired against invented criteria. Treat the PRAOR doc's premise as *structurally*
  true and *behaviourally* unproven.

### 2.3 What each document does not cover

- The PRAOR doc has **nothing on confidence propagation**, which the demo review (P1, P2) and
  `grok-recommendation-confidence-levels.md` identify as the concrete mechanism by which Observe
  reports a false pass. Without D-07 transitivity and a positive definition of HIGH, a named
  Observe limb still signs off on false certainty.
- The technique doc has **no loop vocabulary and no live-measurement proposal**. Its eight items
  land entirely in `shared/`, which per the demo review's ordering caution is exactly where you
  can destroy your own before-reading.

**Synthesis.** The PRAOR doc supplies the *frame* (name the loop, close it live). The technique
doc supplies the *substance* of the two weakest limbs (Act's inputs, Observe's method). Neither
alone yields a reliable loop. The backlog below interleaves them.

---

## 3. Current state, checked in the tree (2026-09-19)

Stated because two of the input documents' recommendations are already partly satisfied, and one
sequencing constraint is repo-specific.

- **Demo-review item 1 has landed.** `shared/spine/SKILL-body.md:313` now carries
  *"Open the Self-Audit Gate's rubric once, before scoring the first criterion"*, with an explicit
  "do not score from recollection" fallback that forbids emitting verdict blocks on a failed read.
  Phase 5's Operation (`:175`) points at it. So R1's fix exists in source; **nothing has measured
  whether it works live.** That measurement is the first real PRAOR deliverable, not a new edit.
- **PRAOR is named in `docs/` but nowhere in the shipped body.** `docs/v8.18-praor-loop-closure.md`,
  `docs/ARCHITECTURE.md`, `docs/README.md` and `docs/gates/HARN-02.md` use the vocabulary;
  `shared/spine/SKILL-body.md` uses "re-entry edge" and "Turn discipline" and never names the loop.
  The PRAOR doc's rec 1 is therefore genuinely unfilled.
- **MEAS-01/MEAS-02 exist as backlog 999.12/999.13**, promoted to v9.0.0 Phase 20 and carried with
  an explicit note (`ROADMAP.md:1082`) that MEAS-01 may be **materially smaller than filed**
  because stored captures already answer part of it. Re-derive scope before scoping work.
- **Backlog numbering** currently runs to `999.127`. Proposed items below start at `999.128`.
- **The milestone is held.** v9.4.0 close was attempted twice and held; Phase 37 closed
  `halted-for-root-replan` with a standing PRE-2 STOP (D-04) and open findings carried to
  `999.127`. Battery is GREEN 23/23 at `66e6d24`. **This work is a next-milestone candidate
  (v9.5.0 "PRAOR live consistency"), not an insertion into v9.4.0** — the STOP decision governs.

---

## 4. Target state: what "the loop is closed" would mean

Falsifiable definition, so the milestone can be audited rather than asserted:

1. **Named.** One surface the model actually reads states the five limbs and the React rule
   (one pass, then degrade + caveat, never spin, never silently drop a fired edge).
2. **Act is observed, not asserted.** A recorded census says, per captured run, whether the
   reference reads and source reads happened — with its N, as an observation, never a gate
   (K-of-5 discipline, `docs/v8.7-constraint-teardown.md` §2 item 3).
3. **Observe has a method and a semantic limb.** Recompute → sensitivity → rival → adversarial
   technique → falsification condition, and a Criterion 4 clause that can fail a well-formed
   non-sequitur.
4. **Confidence is calibrated, not maximised.** HIGH/MEDIUM/LOW defined positively; D-07 made
   transitive; Criterion 5 Rigorous re-based on calibration so an honest MEDIUM can be Rigorous.
5. **React has a state record.** Edges fired, Act attempted y/n, per-chain band — in a form the
   existing detector can parse.
6. **Focused mode has a disclosed residual and a cheap check**, plus one escalation rule out of it.

---

## 5. Proposed backlog

Five workstreams. Tier per `docs/PROCESS.md` §2 (product = changes the shipped methodology the
agent executes; apparatus = changes the instrument). Effort is relative, not estimated in time.

### A — Instrument first (apparatus). Proposed 999.128–999.131

The demo review's ordering caution applies at milestone scale: every item in workstreams B–D
edits `shared/`, and editing the body first destroys the artifact that demonstrates the gap.

| ID | Item | Closes | Effort |
|---|---|---|---|
| A1 / 999.128 | `reference_reads` census over captures — did the run open the rubric, the template, any technique file? | Demo H5; PRAOR root cause 1 (Act half); partially answers 999.12/MEAS-01 offline | ~20 lines + fixtures |
| A2 / 999.129 | `detect_defects` confidence columns: `high_conf_chains`, `high_conf_unverified_head`, `confidence_inversions` | Demo H1; makes P1/P2 mechanically visible; technique §D3 | one function + 3 columns + self-test fixtures |
| A3 / 999.130 | `selfaudit_bands_parsed` column; widen the criterion-head regex; non-vocabulary verdict counts as a finding | Demo H3 (anti-masking: `0 disagreements` currently indistinguishable from `0 parsed`) | small, same module |
| A4 / 999.131 | `5:` entry in `_SELFAUDIT_CONTRADICTIONS` pointing at A2's fields | Demo H2 (Criterion 5 structurally invisible today) | one line, after A2 |

**Then take a baseline reading** on the existing captures plus a fresh set, before any `shared/`
edit in B–D. All four are offline; they add no live gate and no CI job beyond QUAL-01's existing
self-test. A3 is a prerequisite for trusting anything A2 reports.

### B — Name the loop and pay for it (product). Proposed 999.132–999.134

| ID | Item | Source | Note |
|---|---|---|---|
| B1 / 999.132 | Control-loop section in `shared/spine/SKILL-body.md`: five limbs, the phases as implementation, the React rule stated once | PRAOR rec 1 | Cheapest high-leverage item, but see B2 — do not net-add |
| B2 / 999.133 | Pay for B1: replace Step 0's "enumerate all eight in Phase 4" with "consider each technique at the phase that owns it, apply where its trigger fires, record one-line *not applicable — reason* for the rest"; relocate the parser-workaround prose to `docs/` leaving one sentence | Technique §A2, §C6 | Removes mandatory padding; frees the turns root cause 4 needs |
| B3 / 999.134 | Turn-discipline priority order: Phase 1–4 artefacts → Act limb (if a HIGH chain needs it) → Self-Audit Gate → React edges; on exhaustion emit partial artefacts + explicit "Observe incomplete — residual caveat", never a silent truncation | PRAOR rec 4 | Makes the degrade path explicit rather than emergent |

### C — Make Observe actually observe (product). Proposed 999.135–999.138

This is where the two documents combine, and where the demo review says the real defect is.

| ID | Item | Source | Note |
|---|---|---|---|
| C1 / 999.135 | Confidence pre-check immediately before every `**Confidence:**` line: list the head's identifiers, contains `GT-N?` y/n, label forced accordingly | `grok-recommendation-confidence-levels.md` tip 1; demo P1 | Local just-in-time checklist beats a distant global rule; this is the single highest-ROI product item |
| C2 / 999.136 | D-07 transitivity clause in `output-template.md` + Criterion 5 Rigorous descriptor: a chain is capped by the lowest band in its head, chains included | Demo P2; technique §D3 | Specification gap, not a slip — P2 is currently *legal* under the written rule |
| C3 / 999.137 | Define HIGH/MEDIUM/LOW positively in `output-template.md`; re-base Criterion 5 Rigorous on **calibration** ("each rating is the highest its inputs and hops license, and no higher"), keeping the caps | Technique §D3 | Removes the structural incentive to inflate. An honest MEDIUM becomes Rigorous |
| C4 / 999.138 | Phase 5 method: recompute → sensitivity (which GT flips it, is it `?`) → rival conclusion → adversarial technique → falsification condition; plus a **hop-validity + arithmetic** limb on Criterion 4 | Technique §D1–D2; PRAOR "Observe" | Gives Criterion 5's Absent band something observable to score. Needs no new tooling — scored like Criterion 6's Key-Insight limb |

Also in scope here and cheap: add the D-07 compliance column to the existing self-audit scan
table (`Contains GT-N? | label | D-07 compliant?`) — reuses an existing artefact rather than
inventing one, and is the natural carrier for the PRAOR doc's **loop-state marker** (rec 5):
edges fired, Act attempted y/n, per-chain band, in one block A2/A3 can parse.

### D — Fix the inputs Act and Reason consume (product). Proposed 999.139–999.143

The PRAOR doc does not see these; they are what the Reason limb is actually made of.

| ID | Item | Source | Effort |
|---|---|---|---|
| D1 / 999.139 | Rebuild the estimate worked example in one consistent unit; flag the balance-of-system multiplier as `Assumed` with a range; convert to kWh_e before the Li-ion comparison | Technique §B7 | small — **highest priority in D**: an LLM copies examples more readily than prose |
| D2 / 999.140 | Theoretical-limit: require the **tightest** applicable bound; three-tier bracket (ideal → practical/demonstrated → conventional); generalise "physical law" to "governing hard constraint"; rewrite the CSP example and add a software example (speed-of-light latency floor) | Technique §B8 | small–medium |
| D3 / 999.141 | Wire pre-mortem + inversion-of-headline into Phase 5's Operation; wire trade-off into Phase 4's | Technique §A1 | small — Phase 5 currently has *no* adversarial technique attached |
| D4 / 999.142 | Trade-off hardening: must-have knock-outs, 1-and-5 scoring anchors, scores cite GT-IDs (a `GT-N?` score caps the chain at MEDIUM), always report the smallest weight flip, include the status-quo option | Technique §B5 | small |
| D5 / 999.143 | Per-technique gaps: five-whys counterfactual + depth guard + verdict format; fishbone discriminating observation + measurement category; inversion step-4 rewrite + verdict + `load-bearing` tag; pre-mortem triage/tripwires/output contract; second-order actor + time lenses and success-criteria contradiction check; quotas → coverage lenses | Technique §A4, §B1–B4, §B6 | medium, splittable per technique |

D4 and D5's pre-mortem output contract touch the BATT-06 header-hit anti-masking constants
(`pre-mortem=9`, …) that INVARIANT-CHECK asserts — a deliberate, recorded change, not a side effect.

### E — Focused mode and stub parity (product + apparatus). Proposed 999.144–999.146

| ID | Item | Source |
|---|---|---|
| E1 / 999.144 | Make the focused-mode residual a **required disclosure** in the stub output template and Step 0, same sentence on both surfaces | PRAOR rec 3 |
| E2 / 999.145 | One-line escalation rule: escalate to full-composer if any `?` ground truth becomes load-bearing — React's exit from focused mode — plus a cheap per-technique semantic check | PRAOR rec 3; technique §D4 |
| E3 / 999.146 | Reconcile the `/reason-upward` ("ALL THREE", no Assumption Audit) and `/validate` (retired rubric name, wrong step) stubs with the body; better, generate the phase stubs' Procedure and Exit criterion from `SKILL-body.md` via the existing `{{PROCEDURE:slug}}` mechanism so they cannot drift again | Technique §A3 |

E3 is the only item that changes `scripts/sync-content.py` behaviour, and it is the one that makes
HARN-03's parity claim mean what readers assume it means.

### F — Live evidence (observational, never a gate). Proposed 999.147, and 999.12/999.13

Last, per the PRAOR doc's own milestone shape item 5 and the ROADMAP's constraint-5 ordering.

- **999.147** — 5–10 live captures deliberately exercising evidence acquisition, a Criterion 1
  Absent verdict, and a second-order contradiction; score with A1–A4's columns; record whether the
  loop was followed. **Recorded observation with its N, not a gate**; K-of-5 noise discipline.
- **999.12 (MEAS-01)** — re-derive scope after A1 lands; the offline census may already answer most
  of it, leaving only the genuinely uncovered case (the agent silently *not* acquiring).
- **999.13 (MEAS-02)** — genuinely last. It asks whether the Act limb was *worth* shipping, and
  cannot be answered through an instrument still being repaired.

---

## 6. Sequencing

```
A1..A4  (instrument, offline)        ──► BASELINE READING on existing + fresh captures
   │
   ├─► B1..B3  (name the loop, pay for it from padding)
   ├─► C1..C4  (Observe method + confidence calibration)   ← the substantive core
   ├─► D1..D5  (technique/example fixes; D1 first)
   └─► E1..E3  (focused mode + stub parity; E3 touches sync)
                                     ──► RE-READING, same columns
                                     ──► F/999.147 live captures, then 999.12, then 999.13
```

Three ordering constraints, each with a reason rather than a preference:

1. **A before B–E.** Fixing the body first removes the artifact that demonstrates the gap, and the
   next run is a different prompt — there would be nothing to measure the fix against.
2. **A3 before A2's results are trusted.** `0 disagreements` and `0 parsed` are currently the same
   reading; until they are distinguishable, A2's columns can report clean because they see nothing.
3. **C2/C3 before F.** Measuring confidence compliance against a rule that still permits P2 measures
   the wrong thing.

Within B–E the workstreams are independent and can run in parallel. If only one thing ships,
ship **C1** (the confidence pre-check): it is one paragraph, it sits at the moment of decision,
and it targets the defect that makes Observe report a false pass.

---

## 7. Blast radius and risks

- **Rubric/body wording is asserted verbatim by gates.** SCAN-GUARD, HC-BOUND and HARN-01/02
  pin prescription text; CONF-GATE pins source-literal conformance targets; CONF-SURFACE and the
  claim-surface drift gate regenerate the doc tables. Run `bash scripts/check-firewall-battery.sh`
  after any `shared/spine/` or rubric edit, and expect fixture updates in the same commit.
- **Every `shared/` edit needs `python3 scripts/sync-content.py --write`**; the pre-commit
  sync-drift gate enforces it.
- **D4/D5 move BATT-06 header-hit constants** that INVARIANT-CHECK asserts by value.
- **B1's net-add risk is real.** If B2 does not land, B1 makes root cause 4 worse, not better.
- **The milestone is held.** v9.4.0 carries a standing PRE-2 STOP and an unstarted Phase 44. This
  backlog is a v9.5.0 candidate; filing it does not resolve the STOP, and starting it before the
  STOP is resolved would repeat the pattern the STOP exists to interrupt.
- **Self-grading remains self-grading.** C1–C4 raise the floor; none of them adds a second grader.
  The honest ceiling of this milestone is "the gate can now fail a well-formed non-sequitur and a
  miscalibrated HIGH", not "the gate is adversarial".

---

## 8. Open questions, not decided here

1. **Does the landed Phase 5 read imperative actually fire?** Unmeasured. A1 + one live capture
   answers it, and the answer changes whether B/C get a prose fix or a mechanism fix.
2. **Is the loop-state marker its own block or a column set on the existing self-audit scan?**
   This plan assumes the latter (cheaper, parseable, reuses an artefact). The PRAOR doc implies
   a new block.
3. **Does E3 generate the phase stubs from `SKILL-body.md`, or hand-reconcile them once?**
   Generation costs more now and ends the drift class; reconciliation is a one-off that will
   drift again.
4. **Milestone scope.** All of A–F is large. A defensible smaller cut is A + C + D1, which buys
   the instrument, the confidence contract and the worst worked example, and defers the naming.
