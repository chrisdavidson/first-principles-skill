# Track B comparative run — v9.15 (trackb-2, superseding)

**Frozen evidence. Do not edit any file in this directory.**
Registered in `_FROZEN_PATHS` (`scripts/check-firewall-battery.sh`), so any modification
turns FROZEN-EVIDENCE red.

**Run date:** 2026-09-30 · **Model:** `claude-sonnet-5` (pinned) · **Run id:** `trackb-run-v9.15`
**Protocol:** [`docs/trackb-2-preregistration.md`](../../docs/trackb-2-preregistration.md)
(id `trackb-2`) · **Rubric:** `docs/trackb-neutral-rubric.md`
**Prompts:** `tests/trackb-catalog-v9.13.md` (unchanged from v9.13)

---

## What this is

The superseding run of [`tests/trackb-run-v9.13/`](../trackb-run-v9.13/README.md), registered
because that run's arm-T captures were the main session's *summaries* of the agent's analysis,
not the agent's own document
([`docs/trackb-transport-erratum.md`](../../docs/trackb-transport-erratum.md)). This run scores
arm T on the agent's own delivered `.first-principles/analysis-*.md` file, captured via
`--output-format stream-json` with dispatch recorded per cell from the transcript, dispatched via
the documented slash-launcher form (`/first-principles:first-principles-analysis `).

- **Arm T** — the agent's delivered document, dispatched via
  `--plugin-dir <repo>/first-principles`
- **Arm C** — the byte-identical prompt, same model, no plugin, with the same isolation
  settings and transport as arm T (the only manipulated variable is the plugin)

## Result: cleared

Computed by `evaluate()` in `scripts/check-trackb-comparative.py` from the recorded numbers. No
code path permits a caller to assert a status (control C17).

| | |
|---|---|
| Agent arm (T), mean | 14.70 / 15 (per-prompt: 15, 15, 13.5, 15, 15, 15, 15, 15, 13.5, 15) |
| Control arm (C), mean | 11.30 / 15 (per-prompt: 13.5, 12, 12.5, 12.5, 9, 8, 11.5, 14, 9.5, 10.5) |
| Mean difference (T − C) | **+3.40** |
| *p* (exact paired permutation) | **0.001953** (< 0.05 ✓) |
| In-run judge drift | 0.35 (threshold 2× = 0.70; effect 3.40 ≫ 0.70 ✓) |
| Domains favouring agent | **4 of 4** (needed ≥ 3 ✓) |

All three pre-registered conditions held. **Format-tell caveat (part of the result, not a
footnote):** the scored arm-T document is identifiable by its own contract format with near
certainty, so this result cannot separate reasoning quality from a format or halo effect. See
`docs/trackb-2-reading.md` for the full §7 reading, including the non-gating secondary figure
(arm T's orchestrator summary scores 0.60 points lower than its own delivered file, on the same
blinded rubric).

Mechanics were clean: 20/20 primary generations scored, 0 voided cells, 0 unparseable
scorelines, 60/60 primary+drift judgings, 20/20 secondary judgings. Two usage-limit pauses
occurred mid-run (recorded in `manifest.json`'s `resumed_utc`); neither counted as an attempt or
altered any recorded score. One mid-run mechanics correction is recorded in
`docs/trackb-2-preregistration.md`'s "Pre-run amendments" section: `is_limit_stub()`'s regex
fallback misclassified `TB-01-C`'s attempt 1 (a genuine, complete, non-error answer) as a stub;
fixed, and that attempt adopted as `TB-01-C`'s scored capture (see `cells.json`'s
`reclassified_by` field on that cell).

## Contents

| Path | What it holds |
|---|---|
| `manifest.json` | protocol id, start/resume timestamps, HEAD sha, agent-body sha256, argv templates, isolation settings, blinding seed |
| `cells.json` | per-cell outcome, attempts, dispatch flag, delivered filename, word count (and `reclassified_by` for `TB-01-C`) |
| `probe/probe.json`, `probe/probe-{c,t}.jsonl` | the pre-run transport probe (arm-C isolation + arm-T dispatch), not scored |
| `raw/TB-NN-{T,C}.a{n}.jsonl` | every stream-json generation attempt, including the two usage-limit-pause specimens (`TB-06-T.a1.limit-stub.jsonl`) |
| `raw/TB-NN-T.a{n}.files/` | every file collected from that attempt's `.first-principles/` scratch directory |
| `generations/TB-NN-T.md` | the agent's delivered analysis document (primary, scored) |
| `generations/TB-NN-T.orchestrator.txt` | the main session's final message for that cell (secondary, non-gating) |
| `generations/TB-NN-C.txt` | the unaided control's answer (primary, scored) |
| `blinding-key.json` | opaque-id → (kind, cell) mapping, written after generation |
| `judgings/DNNN-j{1,2}.txt` | 40 blinded primary judgings, 2 independent judges per document |
| `judgings/DNNN-drift.txt` | 20 same-session re-judgings of primary documents — the drift-control arm |
| `judgings/DNNN-j{1,2}.txt` (secondary ids) | 20 blinded judgings of the 10 secondary (orchestrator-message) documents |
| `result.json` | the computed result record (identical to `docs/data/trackb-result.json`) |
| `run.log` | the run's own stdout across both launches |

## Why it is published

Unlike v9.13, this result is `cleared` and is therefore published on `docs/EVIDENCE.md`
(mechanically enforced by `gen-evidence-card.py` controls C06/C07/C12/C13) — but always with the
format-tell caveat rendered alongside it, per the pre-registration's §2 item 8.

## Known limitations of this corpus

Stated here rather than left to be discovered.

- **N=10 paired prompts, 1 run per cell.** Carried unchanged from v9.13's own amendment (§4 of
  `docs/trackb-preregistration.md`).
- **Not separable from a format/halo effect.** The scored arm-T document carries the agent's own
  contract structure (`## Answer`, six named sections, `GT-` ids, appendix); the scored arm-C
  document carries none of that. This is a stronger, disclosed confound than v9.13's registered
  length/structure difference.
- **Length is a confound and was not controlled.** Arm T mean 8,785.6 words; arm C mean 656.5
  words — a roughly 13× difference, far larger than v9.13's own (449 vs 575).
- **Blinding is passive non-exposure, not unreachability.** Same bound as v9.13; not tightened.
- **Conditional on explicit dispatch.** Arm T is dispatched via the documented slash-launcher
  form. Whether an ordinary user prompt reaches the agent at all is a separate, known-unreliable
  question measured elsewhere.
- **Not a correctness claim.** The rubric scores the quality of the reasoning as presented, not
  its arithmetic.
- **Not transferable to another model.** The model is pinned to `claude-sonnet-5`.

## Downstream use

Supersedes `tests/trackb-run-v9.13/` as the registered answer to "does the agent beat an unaided
answer?" — see `docs/trackb-2-reading.md` for the full reading.
