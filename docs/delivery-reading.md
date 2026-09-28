# Delivery — what reaches the caller

**A recorded reading with its N. Not a gate.**
**Protocol:** [`docs/delivery-preregistration.md`](delivery-preregistration.md), with
Amendment 1 (§6).
**Captures:** `tests/delivery/` (frozen; each run's own agent transcript is under
`raw/<run>.agent/`) · **Re-derive:** `python3 tests/delivery/run_delivery.py read`

---

## The answer

**On the body with self-delegation blocked, the caller received an incomplete document in 5 of 20
runs.** Every one of the five is a **length continuation**: the agent wrote its document across
consecutive messages with no tool call between, and only the last message reaches the caller.

| | Result |
|---|---|
| **Caller received fewer contract sections than the agent wrote** | **5 of 20** |
| Runs whose document spanned consecutive messages (length continuation) | 6 of 20 |
| … of those, the caller lost sections | 5 of 6 — the sixth re-sent the whole document last |
| Self-delegation calls | 0 (the `749da354` block holds) |
| Runs missing the agent's own transcript | 0 |
| Pre-registered figure, from streamed text the caller never receives | 0 of 20 — see Amendment 1 |

| Run | Sections the agent wrote | Sections the caller received |
|---|---|---|
| `TB-02.r1` | 6 | 3 |
| `TB-02.r2` | 6 | 5 |
| `TB-03.r1` | 6 | 4 |
| `TB-04.r2` | 5 | 0 |
| `TB-06.r2` | 6 | 4 |

## The mechanism, established twice

1. **In isolation.** A probe told the agent to write `ALPHA`, call a tool, then write `OMEGA`.
   The caller received `OMEGA` alone.
2. **In this run.** In all 20 runs, what the caller received is exactly the agent's final text
   message. Where the document ran past one message, the earlier part was lost; where the agent
   happened to re-send the complete document last (`TB-10.r2`), nothing was.

`TB-06.r2` is the clearest case: three consecutive messages of 3,050, 927 and 2,741 words, the
second opening mid-table and the third at `# 4. Derivation Chains`. The caller received the third.

## Against Phase 1

Phase 1 counted 4 of 20 delivery failures before self-delegation was blocked, but measured the
delivered document from streamed text, the definition this run found wanting. The two figures
are not comparable. What this run adds is the cause of the failures that remain: **none
involved delegation; all involved length continuation.**

## What this points at

A fix that makes the **final message the complete document** — or keeps the document short
enough to fit in one — should remove this failure class. Whether it does is a separate,
pre-registered test; nothing here edits the body.

## Limits

- **Twenty runs, one prompt family (TB), one model, today.**
- **Asynchronous dispatch only.** Every run here delivered through `task_notification`. A
  synchronous hand-back is also the final message (the probe), but its rate is not measured here.
- **Sections are a coarse unit.** A loss inside a section is not counted.

## Falsifiers

```sh
python3 tests/delivery/run_delivery.py --self-test
python3 tests/delivery/run_delivery.py read | grep -q 'CALLER DELIVERY FAILURE RATE  5/20'
python3 tests/delivery/run_delivery.py read | grep -q 'length continuation in 6/20; lost among them 5/6'
python3 tests/delivery/run_delivery.py read | grep -q 'self-delegation calls: 0'
python3 tests/delivery/run_delivery.py read | grep -q 'pre-registered rate (streamed text, which the caller never receives)  0/20'
git diff --quiet HEAD -- tests/delivery
```
