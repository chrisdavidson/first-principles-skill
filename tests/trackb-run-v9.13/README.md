# Track B comparative run — v9.13

**Frozen evidence. Do not edit any file in this directory.**
Registered in `_FROZEN_PATHS` (`scripts/check-firewall-battery.sh`), so any modification
turns FROZEN-EVIDENCE red.

**Run date:** 2026-09-25 · **Model:** `claude-sonnet-5` (pinned) · **Run id:** `trackb-run-v9.13`
**Protocol:** `docs/trackb-preregistration.md` · **Rubric:** `docs/trackb-neutral-rubric.md`
**Prompts:** `tests/trackb-catalog-v9.13.md`

---

## What this is

The first measurement in this project's history comparing the agent against **not using
the agent**. Every prior "A/B" here contrasted two versions of the same agent body.

- **Arm T** — plugin loaded (`--plugin-dir ./first-principles`)
- **Arm C** — same byte-identical prompt, same model, no plugin

Both arms were asked, in the same words, for a rigorous ground-up analysis. That is the
conservative framing, registered as primary: it measures whether routing through the
agent beats simply asking Claude carefully, not whether it beats a casual prompt.

## Result: null

Computed by `evaluate()` in `scripts/check-trackb-comparative.py` from the recorded
numbers. No code path permits a caller to assert a status (control C17).

| | |
|---|---|
| Agent arm (T) | 12.90 / 15 |
| Control arm (C) | 12.55 / 15 |
| Mean difference | +0.35 |
| p (exact paired permutation) | 0.564 |
| In-run judge drift | 0.90 (threshold 2× = 1.80) |
| Domains favouring agent | 2 of 4 (needed 3) |

All three pre-registered conditions failed. **The instrument is 2.6× noisier than the
effect it was asked to detect.**

Mechanics were clean: 20/20 generations, 60/60 judgings, 0 voided cells, 0 dispatch
failures, 0 unparseable scorelines.

## Contents

| Path | What it holds |
|---|---|
| `generations/TB-NN-{T,C}.txt` | 20 captured analyses, one per prompt per arm |
| `judgings/DNNN-j{1,2}.txt` | 40 blinded judgings, 2 independent judges per document |
| `judgings/DNNN-drift.txt` | 20 same-session re-judgings — the drift-control arm |
| `blinding-key.json` | opaque-id → cell mapping, written after generation |
| `result.json` | the computed result record, every per-prompt score and drift pair |
| `run.log` | the run's own stdout |

## Why it is here rather than published

The comparative claim is **not** published. `docs/EVIDENCE.md` carries its standing
disclaimer that no controlled comparison against an unaided baseline exists, enforced
mechanically by `gen-evidence-card.py` control C06.

That is deliberate and it is not the same as hiding the result. The evidence lives here,
in full, diff-reviewable. What is withheld is the *claim*, because a null does not
support one. `result.json` is stored in this directory rather than at
`docs/data/trackb-result.json` precisely so the publication path stays empty while the
record stays durable — the card's generator reads only the `docs/data/` location.

## Known limitations of this corpus

Stated here rather than left to be discovered.

- **N=10 paired prompts, 1 run per cell.** The pre-registration was amended from 2 runs
  per cell to 1 *before any data existed* (recorded in §4 of that document, with its
  cause and its cost). This sacrifices within-arm variance control, measured elsewhere
  in this repository at up to 3 band points.
- **Judge drift is large relative to the effect.** 9 of 20 documents scored differently
  on same-session re-read; one swung 5 points. Any future comparison on this rubric must
  clear its own in-run drift, not a number guessed in advance.
- **Blinding is passive non-exposure, not unreachability.** A judge subprocess retained
  filesystem access and could in principle have located the key. Same bound the existing
  quality harness discloses; not tightened for this run.
- **Length is a confound and was not controlled.** Agent mean 449 words, control 575.
- **Conditional on explicit dispatch.** Arm T invoked the plugin directly. Whether an
  ordinary user prompt reaches the agent at all is a separate, known-unreliable question.
- **This corpus cannot speak to the bare-prompt framing**, which is the comparison most
  users actually live in and which was deliberately not tested here.

## Downstream use

This is the **baseline for Phase 1** of the evidence-grounding evaluation
(`.planning/PIVOT-EVALUATION-evidence-grounding-2026-09-26.md`). Arm T's
evidence-grounding band distribution — Rigorous 2 / Sound 12 / Hand-wavy 6 across 20
judgings — is the figure a derivation-showing change must move.
