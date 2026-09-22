# v9.6 Re-Baseline-Reading Fresh Set

**Status: live evidence, NOT registered in `_FROZEN_PATHS`.** Deliberately unfrozen for this
milestone — see "Why this is not frozen yet" below. Five real `claude -p` dispatches of the
shipped `first-principles:first-principles` agent against the post-OBS-01..03 body (Phases 52 and
53, HEAD `5a86e0b`), captured and committed as-is.

**Frozen 2026-09-22 (Phase 54, D-08):** registered in `_FROZEN_PATHS` once BASE-02's reading
(`docs/v9.6-rebaseline-reading.md`) was reviewed. Both the before- and after-readings now exist.

## Purpose

This directory is the BASE-02 fresh set. BASE-02 closes the loop opened at Phase 51: the same five
catalog prompts `tests/baseline-reading-v9.6/` used, dispatched again after OBS-01..03 landed. Same
prompts, same transport, same model pin, different body — the only intended difference is the body
(D-01). Together with `tests/baseline-reading-v9.6/`, this is the milestone's only before/after on
agent behaviour (N=5 per arm). Plan 54-02 reads both sets in `docs/v9.6-rebaseline-reading.md`; no
reading or detector figure is transcribed into this README.

## Provenance

- **Catalog:** `tests/live-conformance-catalog.md`, the same five distinct plan-shaped rows as
  `tests/baseline-reading-v9.6/` (`Q-P1`, `Q-P2`, `Q-P3`, `PR-P1`, `PR-P2`). `PR-P1-R2` stays
  excluded — it is a documented byte-duplicate of `PR-P1`'s prompt and would not add an independent
  trial (D-01).
- **Run date:** 2026-09-22, serialized one dispatch at a time, each awaited before the next began.
  No two dispatches overlapped.
- **Body measured:** HEAD `5a86e0b`. `git status --porcelain` was empty (clean tree) immediately
  before the first dispatch — confirmed identical to the HEAD recorded at the Task 1 pre-flight and
  the Task 2 checkpoint, so no re-log of the `shared/` commit list was needed at dispatch time.
  `git log --oneline a866971..5a86e0b -- shared/` (BASE-01's reading commit `a866971` through this
  HEAD) is nonempty — 9 commits — confirming the Phase 52 (OBS-01) and Phase 53 (OBS-03, plus the
  WR-01..WR-07 review fixes) `shared/` changes are in the body measured here:

  ```
  5a86e0b fix(53): fold WR-03's Phase 5 addition back under the D-10 net-growth bound (WR-03, 999.133)
  b9e91b2 fix(53): scope the adversarial-pass not-applicable line to the technique step (WR-03)
  1a93387 fix(53): name the band for a depended-on hop whose only gap is an undeclared premise (WR-02)
  8bdb80f fix(53): make Criterion 4's Sound and Hand-wavy hop clauses exclusive (WR-01)
  61e66cc feat(53-02): prescribe Phase 5's five-step falsification procedure and add Criterion 4's hop-validity and arithmetic limb (OBS-03 SC1/SC2/SC4, D-06..D-15)
  d250539 fix(52-11): ground product-business-2's C1 downgrade in a stated A3 hop, name C2's rival, restore C3's GT-5? verification, count the cost cause once in §6 (OBS-01, WR-01..WR-03, IN-04)
  b0fdbd2 fix(52-08): carry the full pre-check prescription and a parse-verified example into focused-mode reason-upward (OBS-01, WR-03)
  3e53b92 fix(52-07): make product-business-2's pre-checks agree with their Confidence lines (OBS-01, WR-01/WR-02)
  a9c1232 feat(52-02): emit a confidence pre-check before every Confidence line (OBS-01)
  ```

- **Transport (D-02):** `scripts/check-quality-harness.py --probe <ID> --catalog
  tests/live-conformance-catalog.md --plugin-dir ./first-principles --out
  tests/rebaseline-reading-v9.6/`. The Plan-36-locked argv in `_run_prompt_to` (`claude -p
  --plugin-dir <path> --no-session-persistence --output-format stream-json --verbose
  --permission-mode bypassPermissions <prompt>`) was **not** modified — confirmed by
  `git diff --quiet -- scripts/` after all five dispatches.
- **`claude` CLI version:** `2.1.278 (Claude Code)` — same as `tests/baseline-reading-v9.6/`.
- **Model pin:** requested via the `ANTHROPIC_MODEL=claude-opus-5` environment variable, never by
  editing the locked argv. **Observed** model read back from each capture's own metadata rather than
  assumed: all five captures report `claude-opus-5` on the `type=system`/`subtype=init` event and on
  every `message.model`. Three captures (`Q-P1`, `Q-P2`, `PR-P2`) bill only `claude-opus-5` in
  `result.modelUsage`. **Two captures bill a second model** — `Q-P3` and `PR-P1` both bill
  `claude-opus-5` **and** `claude-haiku-4-5-20251001`. The pin held for the answering model on every
  capture; the second billed model on `Q-P3`/`PR-P1` is recorded as a divergence, not reconciled
  away, matching the precedent in `tests/baseline-reading-v9.6/README.md` (where `PR-P1` alone
  billed a second model) and `tests/adversarial-firing-v9.5/README.md`.

## Why this is not frozen yet

`_FROZEN_PATHS` registration is deliberately withheld for this milestone, following the D-20-C
lesson recorded in `tests/live-conformance-catalog.md` and repeated in
`tests/baseline-reading-v9.6/README.md`: registering a directory before its readings have been
reviewed makes the first correction a frozen-evidence violation instead of a correction. Plan 54-02
(D-08) registers **both** `tests/baseline-reading-v9.6/` and `tests/rebaseline-reading-v9.6/` in
`_FROZEN_PATHS` together, once the re-reading (`docs/v9.6-rebaseline-reading.md`) is written and
reviewed and neither fresh set is expected to need correction.

## Dispatch record

All five rows were dispatched one at a time, each background run awaited before the next began; no
two dispatches overlapped. Total elapsed wall-clock across the five serial dispatches was
approximately 20 minutes.

- **Q-P1** — outcome `completed`. `--probe` refused to persist an analysis (primary/cross-check
  disagreement, primary len=20,747, cross-check len=21,707). No re-dispatch — handled by
  re-extraction below (Wrapper mode). `total_cost_usd` **$1.8311**, `duration_ms` 199,039 (~3.3 min).
- **Q-P2** — outcome `completed`. `--probe` refused to persist (primary len=23,643, cross-check
  len=24,753). No re-dispatch — re-extracted (Wrapper mode). `total_cost_usd` **$1.8560**,
  `duration_ms` 244,012 (~4.1 min).
- **Q-P3** — outcome `completed`. `--probe` refused to persist (primary len=27,178, cross-check
  len=28,276). No re-dispatch — re-extracted (Wrapper mode). `total_cost_usd` **$2.3276**,
  `duration_ms` 290,643 (~4.8 min). Bills two models (see Provenance).
- **PR-P1** — outcome `completed`. `--probe` refused to persist (primary len=24,401, cross-check
  len=25,477). No re-dispatch — re-extracted (Wrapper mode). `total_cost_usd` **$2.1345**,
  `duration_ms` 254,271 (~4.2 min). Bills two models (see Provenance).
- **PR-P2** — outcome `completed`. `--probe` refused to persist (primary len=18,943, cross-check
  len=19,889). No re-dispatch — re-extracted (Wrapper mode). `total_cost_usd` **$1.5312**,
  `duration_ms` 166,858 (~2.8 min).

**TOTAL: `total_cost_usd` $9.6806, `duration_ms` sum ~19.2 min serial processing time** (summed from
each capture's own `result` event, the same method the Task 1 pre-flight used to reproduce the
`tests/baseline-reading-v9.6/` and `tests/adversarial-firing-v9.5/` precedent totals). This lands
just under the Task 1 pre-flight's approved $10-$25 range and within its ~25-70 min wall-clock
range.

No capture stubbed (`rate_limit_stub`, `transport_error_stub`, `no_terminal_result`) and no
`superseded/` directory was needed — every row completed on its first and only dispatch. N=5, full
row set, no reduction.

## Extraction — read this before re-scoring

`--probe` **refused to persist an analysis for all five captures**, the same outcome as
`tests/baseline-reading-v9.6/`. Its guardrail compares two channels — the
`task_notification.summary` primary channel and a tail-stripped `tool_result` cross-check — and
declines when they disagree. That refusal is correct and every `.jsonl` here is the intact,
unmodified transport log; each `.md` was re-extracted from its own capture without paying for a
second dispatch.

All five captures disagree in the **same** mode:

| Mode | Captures | Shape | Correct channel |
|---|---|---|---|
| **Wrapper** | `Q-P1`, `Q-P2`, `Q-P3`, `PR-P1`, `PR-P2` | `--probe`'s own tail-stripped cross-check is *larger* than the primary channel in every case (by roughly 960-1,100 characters), carrying wrapper artifact the tail-strip does not remove | the primary channel (`task_notification.summary`) — for every row, independently re-verified character-for-character identical to the capture's own top-level `tool_use_result.content[*].text` field via a scratchpad extraction script, the clean channel named in the precedent's Wrapper row |

Every row in this set disagreed in Wrapper mode, matching `tests/baseline-reading-v9.6/` exactly
(no Spill-mode row, unlike `tests/adversarial-firing-v9.5/`). **Taking the longest text field is
wrong** — it would pick the wrapper-carrying copy in every one of the five. Each `.md` in this
directory was verified, before commit, to (a) not start with `[Subagent hand-back]`, (b) contain no
`<persisted-output>` or `<usage>` trailer, and (c) carry all six numbered output-template sections
(`^#{1,2} [1-6]\. `).

## A note on local absolute paths

Every `.jsonl` in this directory contains local absolute paths from the donor machine (`/home/`
occurrences, confirmed present by grep) — this is expected transport-log content, not a defect, and
matches the precedent in `tests/baseline-reading-v9.6/README.md` and
`tests/reference-reads-v9.2.1/README.md`. These paths are **not** rewritten or "fixed" to remove
them; live evidence is left as the donor machine produced it.

## Chain of custody

| File | Bytes | sha256 |
|---|---|---|
| `Q-P1.jsonl` | 218,198 | `a6bcc0595bb092d26d57f448e585ed928ef75c19efb56916a7c3121a9c870c78` |
| `Q-P1.md` | 20,977 | `609f5eceaea4f3a68e3c33cfd049c75d35f5ca4b752bce294271d0912437a845` |
| `Q-P2.jsonl` | 233,709 | `039a1826c5f0ac96c2845e5b7274ec9f745f5ec4203aa3082bd3e7a0cfe1347a` |
| `Q-P2.md` | 23,842 | `9609af687b3f2f0d759b04232adf7adb4d49cb281db5b82c90cbb3a2f7ed0d8d` |
| `Q-P3.jsonl` | 248,945 | `05a999b7639c79cebdba903ba128fd3614213b2810d08f012efe81a7c967020a` |
| `Q-P3.md` | 27,457 | `0c1e9a6a9abed073f93d0519dab09923d1b2f560ec64309c0363116b6508f078` |
| `PR-P1.jsonl` | 244,283 | `914a076f2c1ae40fa38c2b4b0c85a404b7ee896063624c9a659315c2081e25cd` |
| `PR-P1.md` | 24,675 | `0ae0d42b87558b6ceb6e62fca58be1bc71113f6b02d956aa9d756d1e42982571` |
| `PR-P2.jsonl` | 204,967 | `b660c433606d96e58faec01877c10aef0df6c284a39ba6b79f7e9428dca17374` |
| `PR-P2.md` | 19,052 | `0f490ecb0f665e04ca549583d9c1eeac2644807fad61f3284c2564bec231dd7b` |

Each `.jsonl` is the unmodified transport log for its sibling `.md`.
