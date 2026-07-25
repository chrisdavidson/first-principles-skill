# Use Journal

One line per **real** invocation of the first-principles agent or a companion skill — real
meaning it was reached for to think about an actual problem, not a harness run, not a test.

Started 2026-07-24, per the altitude check of the same date (`.planning/ALTITUDE.md`, verdict
PAUSE, after phase 177).

## What this is for

v8.11 closed the last measured defect line with no successor (`CGATE-BUILD-01` = WON'T-DO, the
DIVERGE line closed characterized-but-not-closable). There is currently **no legitimate scope
source for a v8.12**. This journal is the only one that would count: after about five entries,
either disappointment clusters somewhere — and that cluster is the scope — or it does not appear
at all, and v8.11 is the terminal state.

A journal of five entries with nothing in the "fell short" column is a **real result**, not a
failed experiment. Record that outcome as readily as the other one.

## Rules

- **One line, written right after the invocation**, while the intent is still fresh.
- **The "fell short" half is the whole point.** "Nothing" is a valid and informative entry —
  write it rather than skipping the line.
- **Do not promote this to an instrument.** No script, no detector, no counter, no CI gate, and
  no row in the traceability matrix. This project's characteristic failure is turning an
  observation into a measured harness and then spending milestones measuring the harness —
  v8.7 through v8.11 went that way. A plain file read by a human is the correct fidelity.
- **Do not tune the format.** If an entry does not fit the shape below, write prose and move on.

## Format

```text
- YYYY-MM-DD · <technique or `agent`> · asked: <the actual problem, ~10 words> · fell short: <where it disappointed, or "nothing">
```

## Entries

<!-- append below; newest at the bottom -->

## Read-back

At roughly five entries, read them in one sitting and answer one question: **does the
disappointment cluster?**

The expectation on record, written before the entries exist so it can be falsified by them: real
use is concentrated in the **5-phase composer**, which was dispatched **19 times in 30 days** —
12 of those in external work projects, on actual problems, outside this repo. Over the same 30
days the focused technique skills were slash-invoked **zero** times; their large lifetime
counters (`pre-mortem` 125, `inversion` 38) last incremented on 2026-07-20, the date of the
v8.5/v8.6 live re-measure runs, so they are best read as harness activity rather than use.
A cluster is therefore likely to point at the composer. **If it points at a focused technique
instead, that surprise is itself the finding.**

*Correction, 2026-07-24: an earlier version of this section asserted the opposite — that the
composer was near-unused and the focused techniques carried the load. That came from comparing a
lifetime skill counter against a 30-day transcript count, and from counting only Skill-tool
dispatches while the composer is invoked through the Agent tool. Both windows are now measured
the same way. The error is left visible here rather than quietly overwritten.*

Record the read-back as a new dated entry in the altitude log (`.planning/ALTITUDE.md`), not
here. This file stays raw observations; conclusions live in the append-only log.
