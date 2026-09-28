# Delivery compliance — the delivery-fix-4 reading

**A recorded reading with its N. Not a gate.**
**Protocol:** [`docs/delivery-fix-4-preregistration.md`](delivery-fix-4-preregistration.md) and its
Amendment 1 (`delivery-fix-4b`). **Captures:** `tests/delivery-fix-4/` (frozen). **Re-derive:**
`python3 tests/delivery-fix-4/run_fix4.py read` (its `VERDICT` line is inherited from v3's runner
and says "verbatim"; v4 scores the provenance definition of its §3).

---

## The verdicts, as registered

| Registration | Delivered | Verdict |
|---|---|---|
| `delivery-fix-4` — all 12 runs; file used, 6 sections, read, replay under v4's allowlist | 11 of 12 | **not operational** |
| `delivery-fix-4b` — the 9 runs unobserved at its registration; provenance = equal to the appends, or replay | **9 of 9** | **operational** |

`delivery-fix-4`'s one failure, `TB-02.r3`, is an instrument gap and is reported as a failure
anyway: its file equals its appends exactly and was read in full, but the agent also ran
`readlink`, which v4's replay allowlist lacked. `delivery-fix-4b` was registered after that run
and before any other was observed, and scores only those later runs.

## What changed

v4 states the file-delivery rule at the top of the body, before the Methodology. Across 12 runs of
the four prompts that lost sections before any fix:

| | v3 (rule 250 lines in) | v4 (rule at the top) |
|---|---|---|
| Runs that used the file | 10 of 12 | **12 of 12** |
| … `TB-04`, the prompt whose runs ignored it | 1 of 3 | **3 of 3** |
| Output-limit cut-offs | 0 | 0 |
| File length | 7,719 – 10,147 words | 7,610 – 11,573 words |
| Revised in place during self-audit, replaying byte for byte | 3 of 4 revisers | **5 of 5** |

**Every v4 run delivered the complete analysis to the caller**: a six-section file, read in full
by the main session, whose every byte replays from the agent's own recorded writes. Where the agent
revised its file — five runs — the revisions are its own commands, reproduced exactly. The final
message was a short pointer of 119 to 295 words, far below any output limit.

## Against where this started

| | Before any fix (`delivery`) | v4 |
|---|---|---|
| Caller received fewer sections than the agent wrote | 5 of 20 | **0 of 12** |
| Output-limit cut-offs | 6 of 20 | 0 of 12 |

## Limits

- **Twelve runs, four prompts, one model, print mode.** 12 of 12 shows compliance on this set, not
  a rate; a run that skips the procedure entirely remains possible.
- **The before-and-after comparison is not paired.** `delivery` ran the ten TB prompts twice on a
  different day; the fix runs used four of them three times.
- **Provenance proves nothing was changed between writing and delivery** — not that each section
  was complete when first written.

## Falsifiers

```sh
python3 tests/delivery-fix-4/run_fix4.py --self-test
python3 tests/delivery-fix-4/run_fix4.py read | grep -q 'delivered 11/12   runs with a cut-off 0'
python3 tests/delivery-fix-4/run_fix4.py read | grep -q '4b (prospective, Amendment 1)  delivered 9/9  VERDICT-4B  OPERATIONAL'
git diff --quiet HEAD -- tests/delivery-fix-4
```
