# Pre-Registration — Does the current agent body skip its procedure more often than v9.13.0's?

**Id:** `skip-paired` · **Registered:** 2026-10-08, before any run under this id.
**Origin:** [`example-rerun-2-reading.md`](example-rerun-2-reading.md) — 3 of 14 registered
re-runs on the body at `2628e725` skipped the procedure (no template read, no file), against 0 of
14 on v9.13.0 in [`example-rerun`](example-rerun-reading.md).

## 1. Question

Is the skip rate a property of the current body, or chance? The two bodies differ by 51 commits
to `shared/spine/` and `shared/agent/`; the current body is 19% longer (16,772 → 19,982 words),
mostly delivery machinery. This test can attribute a difference to *the body as a whole*, not to
any one change in it.

## 2. Design

- **Arms:** `old` = `git archive v9.13.0 first-principles`; `new` = `git archive 2628e725
  first-principles`. Both exported outside the repository.
- **Prompts:** the three whose registered example-rerun-2 runs skipped —
  `decompose-irreducibility`, `personal-general-2`, `product-business` — verbatim from
  `tests/example-rerun-2/prompts.json`.
- **Runs:** 3 prompts × 3 repeats × 2 arms = **18**, sequential, arm order alternating within
  each prompt-repeat pair and flipped between repeats, so neither arm systematically runs first.
- **Transport:** as `example-rerun-2` — `tests/delivery/run_delivery.py`'s `claude -p` call,
  `claude-sonnet-5`, empty working directory, persistence on, routing misses retried at most
  twice, the agent's own transcript kept.

## 3. Outcome — a run **skips** when it is dispatched and either holds

- no file exists under `.first-principles/` at the end of the run; or
- the agent issued no `Read` of `output-template.md`.

Both are read from the run's capture, not inferred. The two conditions are also reported
separately.

## 4. Reading

Reported as counts per arm and per prompt, with Fisher's exact one-sided p for `new` > `old`.
**No threshold is claimed as decisive at N = 9 per arm:** a 0-of-9 against 3-of-9 split gives
p ≈ 0.10. The reading states what the counts are consistent with; it does not convert them into
a verdict the N cannot carry.

## 5. Confounds, stated in advance

- **The v9.13.0 body ships its reference tree under `agents/`,** which `eabb3f12` later moved
  out because Claude Code registers each such file as a selectable agent. The `old` arm therefore
  presents extra agent types to the main session. This can change routing; it is not expected to
  change what the dispatched agent does once running, but this test cannot exclude it.
- One model, one CLI version (2.1.289), print mode, one day.

## 6. What this cannot establish

Which change in the body causes a difference, if one is found. A recorded reading, never a gate.
