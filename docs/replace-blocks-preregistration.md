# Replace-blocks — pre-registered measurement

Registered 2026-10-11, before any run.

## Question

Does correcting by appending replacement blocks (backlog 999.199: the 9.19.4 body, the replace-blocks
applier in `first-principles/references/replace-blocks.md`, and the rule that an appended block is
never rewritten in place) reduce in-place rewrites of the analysis file without costing turns?

## Arm

One arm: the generated `first-principles/` tree at the commit recorded on the line below, exported
with `git archive` to `$HOME/.cache/fp-replace-blocks/` outside the repository before any run.

**Arm commit:** 81552f6fb80d (exported with git archive 2026-10-11T13:55:47Z)

The arm is built on the 9.19.4 body (D-01), not on the 999.198 or 999.200 bodies. There is no concurrent
control arm. Arm directory `tests/replace-blocks/`, rule `replace-v1` selected by its `rule.json`; the
frozen arms `tests/audit-first/` and `tests/post-held-append/` are read, never written, by this rule.

### Mechanism

- Marker syntax: a correction is appended as `## Replace: <heading text>`, the existing heading exactly
  as written without its leading `#` characters, followed by the corrected heading line and its full
  corrected content.
- Target scope: the named heading through the next heading of the same or higher level. Only `##` and
  `###` headings are targets, and the replacement opens a heading of the same level.
- Sibling extent: a replacement runs to the next `#` or `##` heading line, so a `###` replacement may
  carry further `###` blocks, which is how a chain is added.
- Last wins: replacements apply in file order, a later one for the same heading winning.
- Batching: several blocks may share one heredoc, so the corrections one check finds go in one call.
- One pass: step 4 of delivery runs the awk applier over `<path>.answer`, the main file and
  `<path>.process` in that order, and consumes every marker.
- Fail loud: assembly that cannot proceed prints `NOT ASSEMBLED:` on stderr, writes nothing and exits
  non-zero. The four refusals a block causes (no matching heading, more than one match, a level
  mismatch, a marker not followed by a heading) are each decided after Withdraw processing.
- Withdraw (D-18, `999.199-CONTEXT.md`): `## Withdraw: <text>` cancels every earlier `## Replace: <text>`
  block with that text. The reason is that a mistyped target otherwise has no appended fix, the working
  files being append-only, so the agent would be pushed back to an in-place edit. Because every
  block-caused refusal is decided after Withdraw processing, a Withdraw clears it. A Withdraw naming no
  earlier replacement is a no-op that prints `WARNING: withdraw matched nothing:` and is consumed (D-18 as
  amended), so a mistyped Withdraw cannot dead-end assembly. A refusal for a code fence left unclosed
  above a marker is cleared by appending a closing fence line, not by a Withdraw, since a Withdraw
  under an unclosed fence is itself fenced text.
- Awk dialects: the applier uses only POSIX constructs. The DELIVERY-GUARD controls ran locally under
  `awk dialects run: gawk, mawk, original-awk, busybox awk, gawk --posix` (mawk 1.3.4, BWK awk 20260426
  and busybox 1.36.1 fetched outside the package manager; 43 controls PASS). The CI job installs and
  requires mawk, original-awk and busybox awk (`FP_REQUIRE_AWK_DIALECTS`), but CI's own run has not been
  observed. Any other awk is untested.

## Runs

The 14 prompts of `tests/example-rerun-2/prompts.json`, two repeats, 28 runs scheduled. Stage 1 is
repeat 1 of every prompt, stage 2 is repeat 2. Model `claude-sonnet-5`, CLI version re-checked before the
run, the same `claude -p --plugin-dir` transport and retry policy as the earlier arms: at most two runs at
a time, routing misses retried at most twice and then excluded, usage-limit stubs discarded and re-run.
The denominator is the runs reaching `assemble`.

## Primary

The number of assembled runs with six or more `phase_turns.is_rewrite` rewrites is at most the critical
value of the exact one-sided binomial at p0 = 34/87 (alpha 0.05; the critical value is 5 at n = 24). The
comparator is the pooled 87-run 9.19.2/9.19.3 baseline, run at `maxTurns: 60`.

`primary` here is this binomial test, not the permutation test of the 999.200 arm (999.201 IN-05): the
word names a different test in each arm's `verdict.json`. It is also mechanical. `is_rewrite` is unedited
and exempts `cat >> ... FP_EOF` appends, so a replacement append is not a rewrite and the count falls
whether or not any turn is saved. The primary alone cannot show the change helped, which is why the turn
must-holds below carry the claim.

## Must-hold secondaries

- Median rewrites among assembled runs at most 2.
- No run at or over 90 turns (D-16).
- Median total turns among assembled runs at most 39, the 999.198 arm's median
  (`tests/audit-first/verdict.json`), so that a drop in rewrites is not bought by relabelling
  corrections as appends that cost the same turns (D-16).

## No regression

Every dispatched run assembled and delivered (D-10); no `## Replace:` or `## Withdraw:` line surviving
outside a code fence in any delivered file; no leftover sidecar and no missing section; median first
Self-Audit Gate turn at most 28 (the 999.198 arm's was 26); median total turns at most 43.

## Decision

`shown-effective` only if the primary, every must-hold secondary and every no-regression condition hold
and at least 18 runs assembled. After stage 1, 5 or more assembled runs with six or more rewrites stops
the measurement (`futility-stop`). Fewer than 18 assembled after both stages is `uninformative`. Any
other outcome is `not-shown-effective`. Only `shown-effective` releases 9.19.5.

## Reader definitions

`phase_turns.is_rewrite` and `phase_turns.classify` are unedited. Per run, as implemented in
`tests/audit-first/run_audit.py`:

- `replace_blocks`, `withdraw_blocks`: marker lines outside code fences in the run's `cat >>` heredoc
  commands.
- `replace_calls`: commands carrying at least one of those markers.
- `not_assembled`: step-4 assembly calls whose result contains `NOT ASSEMBLED:`.
- `surviving_replace`: unfenced marker lines left in the delivered `analysis-*.md` (not `.process` or
  `.answer`). A run with any is not complete.
- `corrections = rewrites + replace_calls`.

## Reported, not verdict-bearing

- Mean and median of each reading above per run.
- Median turns against the 999.198 arm (39) and the 999.200 arm (37.5).
- Cost, and the category mix of the remaining rewrites from `tests/audit-first/rewrite_causes.py`.

## Cost

About $97 for 28 runs (28 x $3.48, the 999.200 arm's mean over 24 runs, $83.53 in all); $85 to $110
expected, up to about $140 if two runs reach the cap. Stage 1 alone is about $49 and is `uninformative`
by itself.

## What this cannot establish

One model, one CLI version, print mode, and no judgement of analysis quality.

- The primary is mechanical (see Primary), so the turn must-holds carry the claim.
- There is no concurrent 9.19.4-body arm, and the baseline was truncated at 60 turns, which biases
  against the new arm.
- The no-run-at-90 condition is a tail event. At the 999.198 arm's rate of 1 run in 24, an unchanged body
  passes it about 36% of the time (0.958^24, an estimate from one observation). One run
  (`theoretical-limit-carnot.r2`, 90 and 99 turns) decided both prior verdicts.
- A run over 90 turns was observed in the 999.200 arm (99) and not investigated, so it is not a clean cap
  signal.
- A Replace has no row-level form: a fix to one row of the section 2 Assumptions Table re-emits the whole
  `## 2.` section (26% of baseline episodes were such fixes; median scope 21 lines), so output per
  correction rises.
- Replacements save turns only when batched; one command per replacement is turn-neutral against one
  rewrite (RESEARCH finding 3).

## Constants

Each line below is machine-checked against `tests/audit-first/run_audit.py`.

- Rule: replace-v1
- Alpha: 0.05
- Baseline heavy share: 34/87
- Rewrite-heavy threshold: 6
- Secondary median ceiling: 2
- Median gate turn ceiling: 28
- Median turns ceiling: 39
- Turn cap: 90
- Undelivered runs allowed: 0
- Futility threshold: 5
- Minimum assembled: 18

## Falsifiers

- `python3 tests/audit-first/run_audit.py --self-test`
- `python3 tests/audit-first/run_audit.py read --arm-dir tests/replace-blocks`
- `python3 scripts/check-delivery-guard.py --self-test`

None is a verdict gate for this measurement: the first two are measurement tools registered in no
battery, CI job or gate registry; the third is the DELIVERY-GUARD gate that proves the applier.
