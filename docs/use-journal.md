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

## Capture — writing a line while away from this repo

- **Where the line goes.** The fixed local inbox is `use-journal-inbox.md`, at the top of `$HOME`.
  Append to it right after the run, wherever the author happens to be working; it is always
  available and needs no tooling. Transcription into the `## Entries` section of this journal
  happens later, in batch.
- **Every inbox line carries the date it was written.** Not the date of the run — the date the line
  was typed. Both dates end up in the transcribed entry.
- **A line captured materially later than the run is discarded, not transcribed.** Reconstructing
  an entry from memory days afterwards produces something that looks like evidence and is not.
  Missing runs stay missing, and that absence is itself data — it is what the read-back denominator
  measures.
- **The inbox is local-only and never committed.** Raw detail can go in it, including material that
  could not be written in this public file; the abstraction happens at transcription, under the
  Privacy rules in the next section.

## Privacy — how to be detailed in public

This file is in a public repo, and most real runs are on client work. The scheme separates
**who** from **what**, so the "what" can be as detailed as you like.

**Identity lives in a private key, never here.** `.planning/use-journal-key.md` (gitignored, local
only) maps each stable label to the real project. This file uses labels only:

| Label | Meaning |
|-------|---------|
| `project-a`, `project-b`, … | External work projects — assigned in first-use order, never reused, never explained here |
| `repo` | This repository |
| `personal` | Own non-client problems |

Labels are permanent: once `project-b` means something, it always means that, so patterns across
months stay traceable without the key ever being published.

**Content rule — the operative test:** *would this entry identify the client to someone who knows
the sector?* If yes, abstract it further. In practice:

- **No proper nouns** — no client, person, product, place, or system names.
- **No verbatim quotes** from the source material, and no distinctive figures. Round them
  (`~£2m`, `low hundreds of staff`) or drop them.
- **Describe the analysis, not the case.** "Stress-tested a pricing assumption I'd already
  committed to" is detailed and safe. "Reviewed the Q3 repricing for <client>" is neither.
- **The `fell short` half needs no redaction at all** — it is about the tool's behaviour, not the
  client's business. That is the half this journal exists for, so be blunt there.

Anything too specific to abstract goes in the private key against the same label, not here.

## Format

```text
- YYYY-MM-DD · <label> · <technique or `agent`> · asked: <abstracted problem shape> · fell short: <where it disappointed, or "nothing">
```

Two worked examples of the right altitude — detailed about the work, silent about the client:

```text
- 2026-07-01 · project-b · agent · asked: whether a staffing model I'd already priced survived a demand drop · fell short: gave me the 5 phases but Ground Truths were restatements of my own inputs, not verified facts — I had to supply every number it "grounded" on
- 2026-07-16 · project-c · agent · asked: second-order effects of moving a contract from fixed-fee to time-and-materials · fell short: nothing — the inversion section found a failure mode I'd missed
```

## Entries

<!-- live entries below; newest at the bottom. Written at the time, unlike the baseline above. -->

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

One structural fact from those 19, worth carrying into the read-back: **every real run invoked the
full 5-phase composer** — not one focused technique. And one working session ran the composer eight
times with the prompt growing monotonically (2.6k → 8.0k chars). That growth is either re-prompting
to repair unsatisfying answers — a disappointment signal that fired eight times unrecorded — or
ordinary iteration across successive problems. Transcript metadata cannot tell them apart. It is
the first thing a live entry should settle.

*Correction, 2026-07-24: an earlier version of this section asserted the opposite — that the
composer was near-unused and the focused techniques carried the load. That came from comparing a
lifetime skill counter against a 30-day transcript count, and from counting only Skill-tool
dispatches while the composer is invoked through the Agent tool. Both windows are now measured
the same way. The error is left visible here rather than quietly overwritten.*

Record the read-back as a new dated entry in the altitude log (`.planning/ALTITUDE.md`), not
here. This file stays raw observations; conclusions live in the append-only log.
