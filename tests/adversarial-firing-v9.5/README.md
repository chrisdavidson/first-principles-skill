# v9.5 Adversarial-Pass Firing Fixture

**Status: live evidence, NOT registered in `_FROZEN_PATHS`.** Deliberately unfrozen for this
milestone — see "Why this is not frozen" below. Five real `claude -p` dispatches of the shipped
`first-principles:first-principles` agent against the **wired** body (Phase 47, HEAD `707923c`),
captured and committed as-is.

## Purpose

These captures answer the two readings Phase 47 left owing:

- **MEAS-03** — the adversarial pass's live firing rate, replacing the earlier N=1 observation.
- **MEAS-04** — whether `_battery_core.classify()` drifts now that an applicable analysis emits
  pre-mortem markers.

## Provenance

- **Catalog:** `tests/live-conformance-catalog.md`, the five distinct plan-shaped rows
  (`Q-P1`, `Q-P2`, `Q-P3`, `PR-P1`, `PR-P2`). `PR-P1-R2` is excluded — it is a deliberate duplicate
  of `PR-P1`'s prompt and would not add an independent trial.
- **Run date:** 2026-09-20, serialized one dispatch at a time.
- **Body measured:** the wired body at HEAD `707923c` (Phase 47's product-tier commit `4667c1c`
  plus the citation correction).
- **Transport:** `scripts/check-quality-harness.py --probe <ID> --catalog … --out … --plugin-dir
  ./first-principles`. The Plan-36-locked argv in `_run_prompt_to` was **not** modified.
- **Model pin (D-48-A):** requested via the `ANTHROPIC_MODEL` environment variable, never by
  editing the locked argv. **Observed** model read back from each capture's own metadata rather
  than assumed: every capture reports `claude-opus-5` on its `type=system` init event and on every
  `message.model`, and every capture's `result.modelUsage` is keyed by **two** models —
  `claude-opus-5` and `claude-haiku-4-5-20251001`. The pin held for the answering model; a second
  model was also billed. Recorded as a divergence rather than reconciled away.

## Why this is not frozen

`_FROZEN_PATHS` registration is deliberately withheld for this milestone, following the D-20-C
lesson recorded in `tests/live-conformance-catalog.md`: registering a directory before its readings
have been reviewed makes the first correction a frozen-evidence violation instead of a correction.
`tests/live-conformance-v9.0/` and `tests/live-conformance-catalog.md` **are** frozen and were
byte-unchanged throughout; FROZEN-EVIDENCE passed on every battery run in this phase.

## Extraction — read this before re-scoring

`--probe` **refused to persist an analysis for all five captures.** Its guardrail compares two
channels and declines when they disagree. That refusal is correct and the `.jsonl` files are intact;
each `.md` here was re-extracted from its own capture without paying for a second dispatch. Two
distinct disagreement modes were observed, and they need different handling:

| Mode | Captures | Shape | Correct channel |
|---|---|---|---|
| **Spill** | `Q-P1`, `Q-P2`, `Q-P3`, `PR-P1` | cross-check is a fixed **2,289-byte** `<persisted-output>` preview, because the harness spilled a >50KB output to a file | the primary channel (the full analysis) |
| **Wrapper** | `PR-P2` | cross-check is *larger* than primary (46,235 vs 44,853) because it carries a `[Subagent hand-back]` preamble and a `<usage>` trailer | `tool_use_result.content[*].text` — the clean analysis |

**Taking the longest text field is wrong.** It picks the harness-wrapped copy in Wrapper mode. One
`.md` here (`Q-P3`) was initially extracted that way and re-done; every file in this directory is
now verified unwrapped, carrying all six output sections and the
`## Adversarial pass (process output)` heading.

## Readings taken

**MEAS-03 — firing rate. N = 5. A recorded observation, not a gate.** All five captures carry an
adversarial-pass record, and all five records are shape-complete (past-tense premise, named
clusters, per-cluster disposition): **present 5/5, shape-complete 5/5**. Per
`docs/v8.7-constraint-teardown.md` §2 item 3 this value gates nothing — at N=5 noise equals effect,
and the S-P04 vector swung 2/5 → 0/5 → 2/5 with no source change. Read it as "the prescription
fired on every plan-shaped row in this sample", never as a rate that will hold.

**MEAS-04 — classifier drift: none.** All five classify `full-composer`. The prediction on record
was that the CR-02 `_COMPOSER_FOCUS_CEILING` would hold because a full-composer run carries ≥4
scaffold headers. **The outcome is as predicted; the mechanism is not.** For pre-mortem the ceiling
never had to act, because `pre-mortem` never fired as a technique at all: each capture matches
exactly **1 of 9** pre-mortem markers (`\bhas\s+failed\b`), below `MIN_HEADER_HITS=2`. The barrier
that prevents the over-route is therefore the anti-masking constant INVARIANT-CHECK pins, not the
ceiling. The ceiling *was* exercised — on `PR-P2`, where `fishbone` fired alone (n=1) at 13
composer hits, so the n==1 early return was correctly suppressed.

One incidental cause, worth naming because it was not designed for: the record is emitted under
`## Adversarial pass (process output)`, which does not contain the literal "pre-mortem", so the
`#\s*(focused\s+)?pre[-\s]?mortem\b` heading marker never matches. A Phase 2 naming choice made for
readability turns out to be part of why the classifier does not drift. That is luck, not design, and
a future rename of that heading could change the MEAS-04 answer.

## Chain of custody

| File | Bytes | Extracted | Six sections | Adversarial heading |
|---|---|---|---|---|
| `Q-P1.md` | 54,137 | spill mode, primary channel | yes | yes |
| `Q-P2.md` | 53,139 | spill mode, primary channel | yes | yes |
| `Q-P3.md` | 46,653 | spill mode, primary channel (re-done after an initial wrapped extraction) | yes | yes |
| `PR-P1.md` | 49,882 | spill mode, primary channel | yes | yes |
| `PR-P2.md` | 44,853 | wrapper mode, `tool_use_result` clean channel | yes | yes |

Each `.jsonl` is the unmodified transport log for its `.md`.
