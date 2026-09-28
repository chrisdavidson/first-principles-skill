# Pre-Registration — Does stating the delivery rule at the top make every run use it?

**Id:** `delivery-fix-4` · **Registered:** 2026-09-28, before any run under this id. The
compliance work the maintainer chose when v3 was merged
([v3 reading](delivery-fix-3-reading.md)).

## 1. The one remaining failure, and the fix

v3's file handoff removed truncation wherever it was followed. The single remaining failure is
**compliance**: 2 of 12 runs never used the file, and both skipped the body's procedure outright —
no template read, and one made no tool calls. The rule sat about 250 lines into the body. v4
(`090bb9eb` on branch `delivery-fix-v4`) states it before the Methodology:

> **Deliver the analysis to a file — this binds every response, including one you write without
> using any tool.** Your deliverable is appended to `.first-principles/analysis-<UTC>.md`, one
> section per Bash call, and your final message is only a short pointer to that file; the steps
> are under *Deliver the analysis as a file* in Output format below. A document returned as your
> final message instead can be cut off by the output limit, and then the reader receives only its
> last part.

## 2. Design

As `delivery-fix-3`: `TB-02`, `TB-03`, `TB-04`, `TB-06`, 3 repeats each, **12 runs**, empty
working directory, persistence on, each run's stream, own transcript and file kept; routing misses
retried at most twice.

## 3. Delivered — `tests/delivery-fix-4/run_fix4.py`

A run is **delivered** when all four hold:

- **used** — a file exists under `.first-principles/`;
- **complete** — it carries all 6 contract sections;
- **read** — the main session read it;
- **provenance** — replaying every Bash command the agent issued against the file, in order, on an
  empty copy, reproduces it byte for byte. In-place revision is allowed; silent change is not. The
  replay now also executes the agent's own Python edits: every heredoc body is removed before the
  command words are checked, and any command outside the listed file-and-text set still fails the
  run.

**Calibrated before any run:** applied to the frozen `delivery-fix-3` runs, this rule marks 10 of
12 delivered, failing exactly `TB-04.r1` and `TB-04.r2`, the two that never used the file. It
therefore measures compliance, which is the thing v4 changes.

## 4. Success rule, fixed now

**Operational** if **all 12** scored runs are delivered. **Not operational** otherwise.
Reported: output-limit cut-offs, template reads, in-place revisions, the pointer's length.

## 5. What this cannot establish

- **Twelve runs, four prompts.** All 12 passing shows compliance on this set, not a rate.
- **A top-of-body statement did not reduce abandonment in `abandonment` Phase 1.** That was a
  different rule; whether position helps this one is exactly what this run tests.

## 6. Amendment 1 — `delivery-fix-4b`, registered mid-run for the runs not yet observed

`TB-02.r3` failed §3 on an instrument gap, not on delivery: its file equals the concatenated
appends exactly and was read in full, but the agent also ran `readlink`, a read-only utility my
replay's allowlist lacked, so the replay refused it and the run fails as registered. **By §4,
`delivery-fix-4` is therefore not operational**, and it is reported that way.

**`delivery-fix-4b`, prospective only:** it scores only the runs not yet in
`tests/delivery-fix-4/cells.json` at this amendment's commit — `TB-02.r1`, `TB-02.r2` and
`TB-02.r3` are excluded. **Provenance** holds when the file equals its appends exactly (no other
write can have left a trace) **or** the replay reproduces it byte for byte; the replay's allowlist
gains the read-only `readlink`, `date`, `file`, `which` and `env`. Everything else in §3 stands.
**Operational** if every run it scores is delivered, with at least 9 scored.
