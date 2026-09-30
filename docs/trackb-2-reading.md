# Track B (trackb-2) reading — the superseding agent-vs-unaided comparison

**Status: cleared.** Computed by `evaluate()` from the recorded numbers
(`docs/data/trackb-result.json`); reason as recorded: *"all three pre-registered conditions
met."* Run id `trackb-run-v9.15`, model `claude-sonnet-5`, measured 2026-09-30. Protocol:
[`docs/trackb-2-preregistration.md`](trackb-2-preregistration.md), superseding `trackb`
(`docs/trackb-preregistration.md` / `tests/trackb-run-v9.13/`).

Every figure below is copied from `docs/data/trackb-result.json`; no rounding beyond what that
file already holds.

---

## 1. The effect, against the pre-registered threshold

All three §5 conditions held:

1. **Statistical:** exact paired permutation *p* = **0.001953** (< 0.05).
2. **Exceeds in-run drift:** mean difference **+3.40** exceeds twice the in-run measured judge
   drift (drift = 0.35, threshold = 0.70; 3.40 ≫ 0.70).
3. **Not carried by one domain:** the effect holds in direction in **4 of 4** domains (software,
   policy, science, personal), not merely the required ≥ 3.

`observed_effect` as recorded: *"agent arm scored +3.40 points higher on a 15-point rubric
across 10 paired problems."*

## 2. Per-criterion means, both arms, and the §1 directional prediction scored

| Criterion | Arm T mean | Arm C mean | T − C |
|---|---|---|---|
| C1 Decision usefulness | 3.00 | 2.70 | +0.30 |
| C2 Evidence grounding | 2.80 | 1.75 | +1.05 |
| C3 Assumption surfacing | 3.00 | 2.65 | +0.35 |
| C4 Calibration | 2.90 | 2.05 | +0.85 |
| C5 Falsifiability | 3.00 | 2.15 | +0.85 |

**The §1 directional prediction was registered as:** the effect should be largest on Assumption
surfacing and Falsifiability, and smallest on Decision usefulness.

**Scored against the outcome: partially held, and this is reported precisely rather than
rounded up to "held".**

- **Smallest — held.** Decision usefulness (C1, +0.30) is indeed the smallest gap of the five,
  exactly as predicted.
- **Largest — did not hold as stated.** The predicted-largest criteria, Assumption surfacing
  (C3, +0.35) and Falsifiability (C5, +0.85), were NOT jointly the largest. C3's gap is the
  second-smallest of the five (only Decision usefulness is smaller), not among the largest.
  Falsifiability (C5, +0.85) does tie for the largest gap — but it ties with Calibration (C4,
  +0.85), a criterion the prediction did not name, and the single largest-named criterion,
  Evidence grounding (C2, +1.05), was not one the §1 prediction called out at all.

So: one of the two registered claims (smallest-on-C1) held exactly; the other
(largest-on-C3-and-C5) held for C5 only in a three-way tie and did not hold for C3 at all. This
is recorded as a partial, mixed result rather than smoothed into "the prediction held."

## 3. Length (words per arm) — registered covariate, no normalisation

| Arm | Mean | Median | Min | Max |
|---|---|---|---|---|
| T (agent, delivered file) | 8,785.6 | 8,617.0 | 6,061 | 13,287 |
| C (unaided) | 656.5 | 699.5 | 402 | 871 |

Arm T's documents run roughly **13× longer** than arm C's — a substantially larger length
confound than v9.13's registered 449-vs-575-word difference, and expected given arm T's document
carries the agent's full six-section contract plus a process-output appendix while arm C's is an
unstructured direct answer.

## 4. Inter-rater agreement (primary judgings, both raw and per-criterion)

- **Exact-band agreement rate:** 0.55 (11 of 20 primary document pairs, the two judges assigned
  the identical band on every one of the five criteria).
- **Mean absolute score difference (0–15 scale), overall:** 0.50.
- **Mean absolute difference, per criterion (band-point scale, 0–3):**

  | C1 | C2 | C3 | C4 | C5 |
  |---|---|---|---|---|
  | 0.10 | 0.15 | 0.05 | 0.25 | 0.05 |

  C4 (Calibration) shows the most judge-to-judge disagreement; C3 and C5 the least.

## 5. In-run judge drift

Measured as the mean absolute score change across the 20 primary documents, each re-judged once
in the same session: **0.35** (on the 0–15 total scale). Twice this figure, 0.70, is the §5
threshold-2 bar; the observed effect (3.40) clears it by roughly 4.9×. This is markedly tighter
drift than v9.13 measured on the same rubric (0.90), though the two runs scored different
document types (v9.13 scored orchestrator summaries; this run scores the agent's delivered
files and unaided answers) and are not compared as an effect.

## 6. Mechanics: dispatch, extraction, voids, unparseable, attempts

- **Dispatch misses:** 0. Every one of the 10 arm-T cells recorded `dispatched: true` from its
  stream-json transcript.
- **Extraction-integrity voids:** 0 primary cells voided (0 of 20), 0 secondary documents voided
  (`extraction_voids_secondary: 0`).
- **Voided cells overall:** 0 of 20 (`void_fraction: 0.0`).
- **Unparseable scorelines:** 0 of 60 primary+drift judgings attempted
  (`unparseable_primary: 0`, `attempted_primary: 60`).
- **Attempts per cell:** every cell scored within its first counted attempt, except `TB-06-T`
  (2 attempts — the first hit a genuine usage-limit stub, 429, not counted against the cap) and
  `TB-01-C` (1 attempt, initially misclassified as a usage-limit stub by a detector false
  positive, corrected and adopted as scored — see §8 below and
  `docs/trackb-2-preregistration.md`'s "Pre-run amendments").
- **Live invocations spent:** 20 generations + 40 primary judgings + 20 drift judgings + 20
  secondary judgings = 100, plus the two pre-run transport-probe calls (not scored, not counted
  in the 100).

## 7. Secondary measure: arm T's orchestrator message (non-gating)

Arm T's orchestrator final message — what a user sees without opening the delivered file — was
judged in the same blinded pool, 2 judges each, 10 documents. Mean score: **14.10 / 15**, against
the delivered file's own mean of **14.70 / 15** on the same 10 prompts.

**Secondary summary gap: −0.60** (`secondary_summary_gap` in the result record; the delivered
file scores 0.60 points higher than the orchestrator's own summary of it, on the identical
blinded rubric). This never enters `evaluate()` and does not affect the `cleared` status — it is
reported because it quantifies, for the first time on this instrument, how much a user loses by
reading only the chat response rather than the delivered file: a real but modest tax, an order
of magnitude smaller than the +3.40 agent-vs-unaided effect itself.

## 8. Format-tell caveat — part of the result, not a footnote

Quoted verbatim from the result record's `caveat` field (identical to
`docs/trackb-2-preregistration.md` §2 item 8 and to `FORMAT_TELL_CAVEAT` in
`scripts/check-trackb-comparative.py`):

> The scored arm-T document is identifiable by its format with near certainty, so this result cannot separate reasoning quality from a format or halo effect.

This is published alongside the effect on `docs/EVIDENCE.md` (control C13 requires it on any
cleared trackb-2 render) and restated here rather than left to the pre-registration alone,
because a reader of this specific reading document should see it in the same place as the
number it qualifies.

## 9. What this run does establish, and what it still cannot

**Establishes:** on this rubric, this model, and these 10 prompts, the agent's own delivered
document scores measurably and significantly higher than an unaided answer to the
byte-identical prompt — a real, clean, mechanically clean result, not an artifact of the v9.13
extraction fault (arm T here is the agent's own document, dispatch-confirmed per cell).

**Still cannot establish** (unchanged from `docs/trackb-2-preregistration.md` §6):

- **Not a general quality claim.** Ten prompts across four domains is a spread, not a domain
  sample.
- **Not a claim about ordinary use.** Arm T was dispatched via the documented slash-launcher
  form; whether an undirected user prompt reaches the agent at all is a separate,
  known-unreliable question measured elsewhere.
- **Not a correctness claim.** The rubric scores the reasoning as presented, not its arithmetic.
- **Not transferable to another model.** The model is pinned to `claude-sonnet-5`.
- **Not separable from the format/halo effect** named in §8 above — this is the sharpest new
  limit this run adds relative to v9.13, precisely because this run fixed v9.13's extraction
  fault by scoring the contract-structured document.

## 10. Relation to v9.13 — not compared as an effect

v9.13 measured a *summary* of the agent's analysis against an unaided answer and returned
`null` (`docs/trackb-transport-erratum.md`). This run measures the agent's own *delivered
document* and returns `cleared`. The two runs answer different, narrower and broader questions
respectively; no v9.13-vs-v9.15 delta is computed or implied anywhere in this reading, per the
pre-registration's own instruction not to treat this as a before/after comparison of the same
measurement.

## 11. Mid-run mechanics, disclosed

Two usage-limit pauses occurred during generation (recorded in `manifest.json`'s `resumed_utc`
array and in `run.log`); neither altered any score or counted as an attempt. One detector false
positive was found and fixed mid-run: `is_limit_stub()`'s regex fallback misclassified
`TB-01-C`'s attempt 1 — a genuine, complete, non-error answer whose own prose mentioned "rate
limiting" in a GraphQL discussion — as a usage-limit stub. Fixed (a final `result` event with
`is_error: false` and non-empty text is now never treated as a stub), and that attempt adopted
as `TB-01-C`'s scored capture rather than re-generated, recorded in `cells.json`'s
`reclassified_by` field and in `docs/trackb-2-preregistration.md`'s dated "Pre-run amendments"
correction. Nothing decision-relevant in the protocol changed.
