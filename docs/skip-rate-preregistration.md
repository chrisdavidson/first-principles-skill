# Pre-Registration — How often does the agent skip its procedure, and does 9.19.3 stop it?

**Id:** `skip-rate` · **Registered:** 2026-10-09, before any run under this id.
**Origin:** backlog 999.196; [`delivery-guard-reading.md`](delivery-guard-reading.md) — two live runs
show the 9.19.3 guard works end to end, but no skip rate has been measured. Earlier counts disagree:
3 of 14 (`example-rerun-2`), 4 of 14 (`pointer-fix`), 0 full skips of 18 (`skip-paired`).

## 1. Question

1. **Baseline:** how often does 9.19.2 (no guard, `Skill` allowed) finish without delivering?
2. **Intrinsic rate on 9.19.3:** how often does 9.19.3's agent *first try to stop* without having
   delivered — the rate the guard has to catch? Comparing it with (1) says whether removing `Skill`
   changes how often the agent skips, rather than only which way it skips.
3. **Effect:** how often does 9.19.3 finish without delivering, after the guard has acted?
4. **Recovery:** of the 9.19.3 runs the guard blocked, how many then delivered?
5. **Cost:** what does a block add, in turns and wall-clock time?

## 2. Design

- **Arms.** `A` = the generated plugin tree at tag `v9.19.2`; `B` = the same at tag `v9.19.3`. Each is
  exported with `git archive` outside the repository before any run, so neither changes under the
  run.
- **Prompts.** All 14 worked-example prompts, `tests/example-rerun-2/prompts.json`, verbatim.
- **N.** Two repeats per prompt per arm: **28 runs per arm, 56 in all.** At the ~15% pooled base
  rate this expects about 4 skips in arm A.
- **Order.** Runs are interleaved — prompt by prompt, repeat by repeat, alternating which arm goes
  first — so time-of-day and service drift fall on both arms alike. Two runs execute at once, each in
  its own fresh empty working directory.
- **Transport.** `claude -p --model claude-sonnet-5 --plugin-dir <arm> --output-format stream-json
  --verbose --permission-mode bypassPermissions <prompt>`, CLI 2.1.289, the same transport as
  `example-rerun-2` and `pointer-fix`. `FP_GUARD_LOG` is set in both arms; only arm `B` has a hook
  to write it.
- **Routing misses** (the main session never dispatches `first-principles:first-principles`) are
  not skips by this agent: the run is retried, at most twice, and a run that misses three times is
  reported as exhausted and left out of every denominator.
- **Usage limits.** A run that ends on a usage-limit stub is discarded and re-run after a pause; it
  is not an outcome.

## 3. Instrument — `tests/skip-rate/run_skiprate.py read`

Per dispatched run, read from the final state of its working directory and its transcripts:

- **Delivered** — a `.first-principles/analysis-<UTC>.md` exists whose first `## ` heading is
  `## Answer`, and `report-<UTC>.md` exists beside it. This is the guard's own criterion, applied
  here by the reader to the files on disk, not to the guard's log.
- **Skipped** — dispatched and not delivered. The mode is read from the agent's transcript:
  `skill-first` (its first tool call is `Skill`), `zero-tool` (no tool call), `no-file` (tool calls,
  none creating the analysis file), `partial` (file created, not assembled or no report).
- **First-stop skip (arm `B`)** — the guard's log shows `decision: block` on the run's first
  `SubagentStop` event. For arm `A`, a first-stop skip is the same as a skip, since nothing stops
  the agent from stopping.
- **Recovered (arm `B`)** — blocked at least once and delivered.
- **Cost** — `num_turns` and `duration_ms` from the final `result` event.

## 4. Readings fixed in advance

- **Primary (Q3).** Arm `B`'s final skip rate against arm `A`'s, Fisher exact one-sided
  (B < A). The guard is **shown effective** if `B` has at most 1 skip in 28 **and** `A` has at
  least 3; if `A` has fewer than 3, the comparison is reported as **uninformative** (the baseline
  did not recur), whatever `B` shows.
- **Mechanism (Q2).** Arm `B`'s first-stop skip rate against arm `A`'s skip rate, Fisher two-sided.
  Reported, not verdict-bearing: N = 28 can detect only a large change.
- **Recovery (Q4).** Reported as k of n blocked runs; any blocked run that did not deliver is read by
  hand and its cause named.
- **Mode table.** Every skip, either arm, is listed with its mode.

## 5. What this cannot establish

One model, one CLI version, print mode, two repeats per prompt. The analyses' content is not judged.
A rate from 28 runs carries a wide interval (0 of 28 is compatible with a true rate up to ~10%).
