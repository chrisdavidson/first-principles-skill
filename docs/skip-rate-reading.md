# How often the agent skips its procedure, 9.19.2 vs 9.19.3 — the skip-rate reading

**A recorded reading with its N. Not a gate.**
**Protocol:** [`docs/skip-rate-preregistration.md`](skip-rate-preregistration.md), registered before
any run. **Captures:** `tests/skip-rate/` — `cells.json`, `readings.json`, and per run under `raw/`:
the main session's stream, the agent's own transcript (`.agent/`), the delivered files (`.files/`)
and, for 9.19.3, the guard's log (`.guard.jsonl`). **Re-derive:**
`python3 tests/skip-rate/run_skiprate.py read`

---

## The answer in one paragraph

**On 9.19.2, 5 of 28 runs finished without delivering. On 9.19.3, 0 of 27 did**
(Fisher one-sided p = 0.028). The pre-registered verdict is **shown effective**: 9.19.2 skipped at
least 3 times and 9.19.3 at most once. **What changed is the outcome, not the impulse to stop.**
9.19.3's agent still tried to stop without delivering in 3 of 27 runs, against 5 of 28 on 9.19.2
(two-sided p = 0.71). The guard blocked all 3, and all 3 then delivered. `Skill` was called in no
run on either version, so it was never the driver at this sample size. **The transcripts show that
a "skip" is several different failures.** The original one, the agent answering at once without the
procedure, recurs at about the same rate on both versions; the guard is what removes it. Two other
failures sit outside the agent's decision to skip. In one, the agent runs out of its 60-turn budget
mid-procedure and the main session then tells it to drop the file. In the other, the agent delivers
in full but to the wrong directory.

## Result, as registered

| | 9.19.2 (`A`) | 9.19.3 (`B`) |
|---|---|---|
| Runs scored | 28 | 27 |
| **Finished without delivering** (§3) | **5** | **0** |
| Tried to stop without delivering (first stop) | 5 | 3 |
| Blocked by the guard, then delivered | — | 3 of 3 |
| Runs calling `Skill` | 0 | 0 |
| Median agent wall-clock, tool calls, cost | 21.9 min, 46, $3.60 | 21.1 min, 42, $3.29 |

- **Excluded run.** `B.science-engineering.r2` missed routing on all three attempts and was excluded
  from both denominators, as registered.
- **Usage limits.** Seven attempts ended on a usage-limit stub. They were discarded and re-run, not
  scored; they are kept in `raw/` as `*.limit-stub.*`. No scored run ends on an error result.
- **Cost of a block.** The three blocked runs took 21–31 min, 63–75 tool calls and $4.08–$5.33,
  against the 9.19.3 median of 21.1 min, 42 calls and $3.29.

## What a "skip" actually is — mechanisms read from the transcripts

| Mechanism | 9.19.2 | 9.19.3 | Guard catches it? |
|---|---|---|---|
| **1. Early skip** — the agent answers at once: no tool call, or a few web searches then chat | 3, all failed (`estimate-fermi.r1`, `product-business.r1`, `product-business-2.r1`) | 2, both blocked within ~5 min and delivered (`product-business-2.r1`, `science-engineering-2.r2`) | Yes |
| **2. Turn budget, then told to cut the delivery** — the agent hits `maxTurns: 60` mid-procedure; the main session resumes it with `SendMessage` ("You hit the 60-turn limit…", "Stop producing PDFs/documents — I need plain text only, no files") | 1 failed (`product-business.r2`, partial file) | 1 stopped without its report, blocked, delivered (`estimate-fermi.r2`) | Yes |
| **3. Wrong directory** — the agent decodes a repository path from the scratch directory's name, `cd`s there, and delivers in full, to the wrong place | 1 (`self-application.r2`) | 0 | **No** — any existing assembled file the transcript names passes |
| **4. Routing miss** — the main session answers the question itself and never dispatches the agent | 3 attempts | 7 attempts, 1 run exhausted | **No** — the agent never runs |

**Mechanism 1 is the original known issue, and it did not go away on 9.19.3.** The agent tried an
early skip in 3 of 28 runs on 9.19.2 and 2 of 27 on 9.19.3. Removing `Skill` did not visibly change
how often the agent declines the procedure; no early skip on either version called `Skill`. What
changed is that on 9.19.3 the guard blocked each attempt within about five minutes (transcript
lines 14 and 35), and both runs then delivered. The order is read from the agent's own transcript:
the guard's "Do not stop yet" feedback comes well before any main-session message.

**Mechanism 2 lives outside the agent body.**

- **How often.** The main session sent the agent a mid-run message in 10 of 55 scored runs, across
  both versions, nearly always after the agent's 60-turn cap. It caused a failed or blocked stop
  in 2 of them; in the other 8 the agent delivered anyway.
- **What the messages said.** They were not the user's words. The main session reacted to a
  truncated hand-back and asked for "plain text only" or "skip figures". When the agent complied,
  the delivery was cut short.
- **Why the turn cap is close.** A delivered run uses a median of 42–46 tool calls, so the 60-turn
  cap leaves little room for a run that researches heavily before writing.

**Mechanism 3 is a sibling of the 9.19.2 pointer defect.** The pointer fix (`docs/pointer-fix-reading.md`)
made the *final message's* paths come from the shell. It does not stop the agent choosing a
different *working directory* for its writes. `self-application`'s prompt concerns this repository,
and the scratch path encodes the repository's name. This run's files were found in this
repository's (git-ignored) `.first-principles/` folder and moved into
`tests/skip-rate/raw/A.self-application.r2.misplaced-files/`. The analysis there is complete and
assembled.

## Where the turns go — mechanism 2, read without re-running

`python3 tests/skip-rate/phase_turns.py` reads every current-body agent transcript already captured
(99: this measurement, `pointer-fix`, `example-rerun-2`, `skip-paired`'s `new` arm). It marks the
turn at which each prescribed delivery step happens. A turn is one distinct assistant message, the
unit `maxTurns` counts. The main session's "you hit the turn limit" message arrives at exactly turn
60.

| Step reached | Median turn | 90th percentile | Max |
|---|---|---|---|
| File created | 2 | 12 | 44 |
| All six sections written | 15 | 24 | 54 |
| Self-Audit Gate | 28 | 48 | 63 |
| Answer | 32 | 54 | 74 |
| Final pointer (delivery done) | 40 | 59 | 82 |

**Research is not what uses up the budget.** In runs that hit the cap, the six sections are written
by turn 7–36. The overrun is between the last section and the Self-Audit Gate. There, capped runs
spend about 26 tool calls re-reading their own file and rewriting it in place through the shell:
splitting it with `sed -n … > part1`, splicing it back with `cat … && mv`, or running a `python3`
find-and-replace. Other runs spend about 6. The self-audit finds something to correct in a section
already appended, and with no `Write`/`Edit` tool and an append-only file, each correction costs
several turns.

| In-place rewrites of its own file | Runs | Hit the 60 cap | Median turns |
|---|---|---|---|
| 0 | 20 | 0 | 15 |
| 1–2 | 21 | 0 | 33 |
| 3–5 | 22 | 0 | 41 |
| 6 or more | 36 | 16 (44%) | 58 |

**Response.** 9.19.4 raises `maxTurns` from 60 to 90 as headroom, which treats the symptom. Backlog
999.198 tried to remove the cause by running the self-audit checks before a section is appended; it
was measured and not shown effective (verdict `not-shown-effective`, below), so it was not released
and the shipped body is the 9.19.4 body. Backlog 999.199 holds the alternative: correct by appending
replacement blocks that assembly applies. The 999.198 body is preserved on branch `audit-first-999.198`.

### After 999.198 (measured, not released)

One arm, 28 runs scheduled, 4 excluded as routing misses (never dispatched), 24 dispatched, all assembled and delivered, against the pooled
99-transcript baseline above. Verdict: `not-shown-effective`. Every figure is re-derived by
`python3 tests/audit-first/run_audit.py read`; the pre-registered rule is in
`docs/audit-first-preregistration.md`.

| | Baseline | 999.198 arm |
|---|---|---|
| Assembled runs | -- | 24 of 24 |
| Runs with 6 or more in-place rewrites | 34 of 87 | 3 of 24 (critical value 5; met) |
| Median rewrites | 4 | 2 |
| Median gate turn | -- | 26 |
| Max turns | -- | 90 (theoretical-limit-carnot.r2, 22 rewrites, gate at turn 73) |

The primary and secondary readings were met on their thresholds, but the no-regression condition
failed on max turns, so the verdict is not-shown-effective. Reported only: 2 of 75 in-place rewrite
commands came before the held append (`decompose-irreducibility.r1` and `personal-general-2.r1`),
both python patches to a held draft sidecar; all three runs with 6 or more rewrites (ishikawa-fishbone.r2 9,
software-systems.r1 9, theoretical-limit-carnot.r2 22) churned after the held append, the residual
the design disclosed (closure Step 0 and the adversarial pass editing sections 3 and 4 already in
the file). `NOT APPENDED` printed 4 times in 4 runs. `held_append_turn` in `readings.json` counts a
refused `NOT APPENDED` call as the held append (`software-systems.r1`: 14, real append 17), which
moves no rewrite in `software-systems.r1`; but one rewrite in `software-systems.r2` (a patch to the
`.s4` draft, turn 16) falls between its refusal (13) and its append (18), so a refusal-aware reading
finds 3 of 75 before the held append where `readings.json` finds 2. Falsifiers:
`python3 tests/audit-first/run_audit.py held` for the attempts and the pre-append commands,
`python3 tests/audit-first/run_audit.py read` for the per-run split. Spend $81.11. Excluded routing misses:
estimate-fermi.r2, science-engineering.r1, science-engineering.r2, theoretical-limit-carnot.r1.

## Sensitivity

| Reading | 9.19.2 | 9.19.3 | p (one-sided) | Verdict |
|---|---|---|---|---|
| As registered | 5/28 | 0/27 | 0.028 | shown effective |
| Misplaced delivery counted as delivered | 4/28 | 0/27 | 0.060 | shown effective (rule: A ≥ 3, B ≤ 1) |
| Early-skip attempts (mechanism 1, first stop) | 3/28 | 2/27 | — | not a verdict reading; the guard, not a lower rate, removes them |

## Instrument defects found during the run, and their effect

- **Retry attempts overwrote each other's raw streams.** `Path.with_suffix` treated `.a1` as a
  suffix, so all attempts of one run wrote to `<run>.jsonl`. The scored attempt is always the last,
  so every score reads the right stream. What was lost is the raw stream of the 10 routing-miss
  attempts, which is why the miss counts above come from `cells.json` and the log.
- **The timing reading first used the last `result` event.** That event is the short follow-up turn
  after the agent's completion notice, not the run. It was fixed before this reading: agent minutes
  now come from the agent's own transcript timestamps. Session totals are kept in `readings.json`
  but not reported, because on many runs the main session's `result` events do not cover the agent.
- **The runner was restarted once** (2026-10-09 21:31), after a usage-limit reset, while both
  workers were idle. No run was in flight, and recorded runs are never re-run.

## What this suggests next (not decided here)

1. **Mechanism 1: why does the agent decline at all?** The rate (~10%) is unchanged by removing
   `Skill`. The guard makes it harmless at a cost of a few minutes; the cause is still unexplained.
2. **Mechanism 2: give the procedure room, and stop the main session undoing it.** Measure turns
   used per phase, then either raise `maxTurns` (GATE-01 pins 60) or make the agent create the file
   earlier, so a truncated hand-back still leaves an assembled draft. Separately, the agent
   description or launcher could tell the caller not to ask a truncated agent for plain text.
3. **Mechanism 3: tighten the guard and the body.** The guard could require the analysis file to lie
   under the stop event's `cwd`, which would have caught `self-application.r2`. The body could forbid
   `cd` out of the working directory before writing.
4. **Mechanism 4: a routing measurement.** It concentrates in two prompts (`theoretical-limit-carnot`
   4 attempts, `science-engineering` 3). The routing battery is the right instrument for it.

## What limits this reading

One model (`claude-sonnet-5`), one CLI version (2.1.289), print mode, two repeats per prompt, and two
runs at a time across four usage-limit pauses. Mechanism counts come from reading each transcript by
hand and are small. The analyses' content is not judged.
