# v9.6 Baseline-Reading Fresh Set

**Status: live evidence, NOT registered in `_FROZEN_PATHS`.** Deliberately unfrozen for this
milestone — see "Why this is not frozen" below. Five real `claude -p` dispatches of the shipped
`first-principles:first-principles` agent against the pre-edit body (Phase 50, HEAD `d1c64d5`),
captured and committed as-is.

**Frozen 2026-09-22 (Phase 54, D-08):** registered in `_FROZEN_PATHS` once BASE-02's reading
(`docs/v9.6-rebaseline-reading.md`) was reviewed. Both the before- and after-readings now exist.

## Purpose

This directory is the BASE-01 fresh set. BASE-01 requires the milestone's baseline reading to
cover "the existing captures plus a fresh set" before any `shared/` edit lands in v9.6.0. Every
existing capture in `tests/*` predates the shipped Phase 50 instrument (`selfaudit_bands_parsed`/
`selfaudit_offvocab_bands` parse-accounting, the three composition counts, the Criterion 5
contradiction entry, and the `--reference-reads` four-state census) — this is the first live
evidence taken against the body as it stands before any v9.6 `shared/` edit. It is read, together
with the existing captures, by `docs/v9.6-baseline-reading.md` (plan 51-02); no reading or
detector figure is transcribed into this README.

## Provenance

- **Catalog:** `tests/live-conformance-catalog.md`, the five distinct plan-shaped rows
  (`Q-P1`, `Q-P2`, `Q-P3`, `PR-P1`, `PR-P2`). `PR-P1-R2` is excluded — it is a documented
  byte-duplicate of `PR-P1`'s prompt and would not add an independent trial.
- **This set repeats prior scenarios rather than sampling new ones.** All five prompts were also
  used by `tests/adversarial-firing-v9.5/` and, before that, `tests/live-conformance-v9.0/`. This
  is a disclosure, not a defect (RESEARCH.md Open Decision 1): reusing the catalog's known-good
  rows keeps this set comparable with the most recent prior body and reuses the only committed
  transport precedent, at the cost of not sampling a genuinely new scenario.
- **Run date:** 2026-09-21, serialized one dispatch at a time, each awaited before the next began.
- **Body measured:** the pre-edit body at HEAD `d1c64d5` (Phase 50's last commit; zero `shared/`
  commits between phase base `30b5971` and this HEAD, confirmed live before dispatch).
- **Transport:** `scripts/check-quality-harness.py --probe <ID> --catalog
  tests/live-conformance-catalog.md --plugin-dir ./first-principles --out
  tests/baseline-reading-v9.6/`. The Plan-36-locked argv in `_run_prompt_to` (`claude -p
  --plugin-dir <path> --no-session-persistence --output-format stream-json --verbose
  --permission-mode bypassPermissions <prompt>`) was **not** modified.
- **`claude` CLI version:** `2.1.278 (Claude Code)`.
- **Model pin (D-48-A):** requested via the `ANTHROPIC_MODEL=claude-opus-5` environment variable,
  never by editing the locked argv. **Observed** model read back from each capture's own metadata
  rather than assumed: all five captures report `claude-opus-5` on the `type=system`/`subtype=init`
  event and on every `message.model`. Four captures (`Q-P1`, `Q-P2`, `Q-P3`, `PR-P2`) bill only
  `claude-opus-5` in `result.modelUsage`. `PR-P1` bills **two** models —
  `claude-opus-5` and `claude-haiku-4-5-20251001`. The pin held for the answering model on every
  capture; `PR-P1`'s second billed model is recorded as a divergence, not reconciled away, matching
  the precedent in `tests/adversarial-firing-v9.5/README.md`.

## Why this is not frozen

`_FROZEN_PATHS` registration is deliberately withheld for this milestone, following the D-20-C
lesson recorded in `tests/live-conformance-catalog.md`: registering a directory before its
readings have been reviewed makes the first correction a frozen-evidence violation instead of a
correction. `tests/live-conformance-v9.0/` and `tests/live-conformance-catalog.md` **are** frozen
and were byte-unchanged throughout dispatch; FROZEN-EVIDENCE passed on every battery run touching
this phase. The plausible freeze point is Phase 54 (BASE-02), once both a before- and an after-
reading exist and neither is expected to need correction.

## Dispatch record

All five rows were dispatched one at a time, each background run awaited before the next began; no
two dispatches overlapped.

- **Q-P1** — outcome `completed`. `--probe` refused to persist an analysis (primary/cross-check
  disagreement, primary len=25,470, cross-check len=26,520). No re-dispatch — handled by
  re-extraction below (Wrapper mode).
- **Q-P2** — outcome `completed`. `--probe` refused to persist (primary len=24,172, cross-check
  len=25,258). No re-dispatch — re-extracted (Wrapper mode).
- **Q-P3** — outcome `completed`. `--probe` refused to persist (primary len=24,391, cross-check
  len=25,527). No re-dispatch — re-extracted (Wrapper mode).
- **PR-P1** — outcome `completed`. `--probe` refused to persist (primary len=27,979, cross-check
  len=29,115). No re-dispatch — re-extracted (Wrapper mode).
- **PR-P2** — outcome `completed`. `--probe` refused to persist (primary len=27,184, cross-check
  len=28,306). No re-dispatch — re-extracted (Wrapper mode).

No capture stubbed (`rate_limit_stub`, `transport_error_stub`, `no_terminal_result`) and no
`superseded/` directory was needed — every row completed on its first and only dispatch.

## Extraction — read this before re-scoring

`--probe` **refused to persist an analysis for all five captures.** Its guardrail compares two
channels — the `task_notification.summary` primary channel and a tail-stripped `tool_result`
cross-check — and declines when they disagree. That refusal is correct and every `.jsonl` here is
the intact, unmodified transport log; each `.md` was re-extracted from its own capture without
paying for a second dispatch.

All five captures disagree in the **same** mode:

| Mode | Captures | Shape | Correct channel |
|---|---|---|---|
| **Wrapper** | `Q-P1`, `Q-P2`, `Q-P3`, `PR-P1`, `PR-P2` | cross-check is *larger* than primary in every case (by roughly 1,050-1,140 characters) because it carries a `[Subagent hand-back]` preamble and an `<usage>` trailer | the primary channel (`task_notification.summary`) — independently confirmed character-for-character identical to the capture's own top-level `tool_use_result.content[*].text` field, the clean channel named in the precedent's Wrapper row |

Unlike `tests/adversarial-firing-v9.5/` (four Spill-mode captures plus one Wrapper-mode capture),
every row in this set disagreed in Wrapper mode. **Taking the longest text field is wrong** — it
would pick the `[Subagent hand-back]`-wrapped copy in every one of the five. Each `.md` in this
directory was verified, before commit, to (a) not start with `[Subagent hand-back]`, (b) contain
no `<persisted-output>` or `<usage>` trailer, and (c) carry all six numbered output-template
sections (`^#{1,2} [1-6]\. `).

## A note on local absolute paths

Every `.jsonl` in this directory contains local absolute paths from the donor machine (5-7
occurrences of `/home/` per file, confirmed by grep) — this is expected transport-log content, not
a defect, and matches the precedent in `tests/reference-reads-v9.2.1/README.md`. These paths are
**not** rewritten or "fixed" to remove them; frozen and unfrozen fixture content alike is left as
the donor machine produced it.

## Chain of custody

| File | Bytes | sha256 |
|---|---|---|
| `Q-P1.jsonl` | 230,095 | `afbb4ce687a4e0c7fcedca8a172e1c0182bb99a57faa4b4b9c5dd764097c7905` |
| `Q-P1.md` | 25,725 | `204470fa8fe0a0b69abf072faed31f3ede62c51d239fc5f31db1fc9e63d9d9f1` |
| `Q-P2.jsonl` | 222,611 | `555abf444b3b6b86a2f83ee6797492019acec160a6a1a7ebebb09d73b67e0c1d` |
| `Q-P2.md` | 24,452 | `fd4a0f1dce8ba3d92b01d1cf77f21c6d29f203aaa0f2c36c289e13f0b09dc818` |
| `Q-P3.jsonl` | 226,171 | `84214f882f058d19eb57764e6e60de221a86c685105371176008ccebfe9a44fa` |
| `Q-P3.md` | 24,727 | `93ac36a3f84dd86f165af4c7c05b42b86ec328ee29f7a79b171979292664e734` |
| `PR-P1.jsonl` | 284,100 | `b32991434ea25c3a70586ed13cceceab95da0948839142d6f3e0583da2253539` |
| `PR-P1.md` | 28,169 | `79bfa9792b4d3b745494194154cf48c901851383b0202b2ed8e7648ac30d3c58` |
| `PR-P2.jsonl` | 234,479 | `5e1c60d2b3b17d3d431263b1a561d9225093876739c7e59cf5d63b6f02eb57d5` |
| `PR-P2.md` | 27,333 | `9d0ba8c482344d2509f7eea27dff2222ad0d64a85383d2e8da1c5cb365e6aa37` |

Each `.jsonl` is the unmodified transport log for its sibling `.md`.
