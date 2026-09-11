---
phase: 27-ship-v9-1-0
plan: 09
subsystem: post-release-recurrence-reading-and-phase-close
tags: [release, recurrence-reading, REL-08, same-class-trip, D-08, D-09, D-10, D-27-09, D-27-10]

dependency-graph:
  requires:
    - "27-04: the pre-release reading, its protocol freeze and its fired pre-arm trip verdict"
    - "27-07: the D-15 fence adjudication (every pre-arm site HELD), used for attribution"
    - "27-08: the [9.1.0] entry this plan's addendum extends"
  provides:
    - "the three post-arm record files and all six recurrence-reading cells published"
    - "the post-release trip verdict with its full union computation"
    - "backlog 999.77 (the reach map) and dated pointers on 999.54 / 999.57 / 999.58"
    - "REL-08 ticked; Phase 27 closed halted-for-root-replan; v9.1.0 SHIPPED"
  affects:
    - "the next milestone's planning: 999.77 is its root-replan input"

key-files:
  created:
    - tests/recurrence-reading-v9.1/post-arm-scanner.md
    - tests/recurrence-reading-v9.1/post-arm-reader-a.md
    - tests/recurrence-reading-v9.1/post-arm-reader-b.md
  modified:
    - tests/recurrence-reading-v9.1/README.md
    - docs/conformance-baseline.md
    - docs/data/conformance.json
    - CHANGELOG.md
    - .planning/REQUIREMENTS.md (gitignored)
    - .planning/ROADMAP.md (gitignored)
    - .planning/STATE.md (gitignored)

decisions:
  - "Reader B's completed second-attempt output from the interrupted session was transcribed
    rather than re-run: it met every isolation condition (fresh session, same prompt, no pre-arm
    record, transcript names no tests/recurrence-reading-v9.1/ path). Only reader A, whose second
    run the usage limit cut off, was re-run. That halved the re-run cost."
  - "Reader A was re-run on the account's new default model (claude-opus-5) rather than on
    claude-fable-5-1. protocol.md fixes no model; the pre-arm readers' model cannot be read back;
    a Fable re-run risked a third usage-limit stop. Disclosed as a bound, not normalised."
  - "Reader A was captured with --output-format json instead of text, so its run metadata
    (model, turns, token usage) survives. The transcribed result field is byte-identical plus a
    terminal newline."
  - "Reach-map groups were assigned by a stated mechanical precedence ((d), then (b), then (a),
    then (c)), evaluated against each timing's own commit."
  - "D-27-09 consolidation: groups (a), (b) and (d), and the unowned remainder of (c), have no open
    owner, so one new number (999.77) carries all of them; 999.54, 999.57 and 999.58 get dated
    pointers for the (c) sites they already own. One number, not one per group."

metrics:
  duration: "~70 min in this session, after two usage-limit stops in the interrupted session"
  completed: 2026-09-11
---

# Phase 27 Plan 09: The post-release reading, the trip verdict, and phase close — Summary

Took the post-release recurrence reading on `7d7c1d9` (the tree that ships), published all six
cells, decided the same-class trip by the predicate published before any reading, did the
bookkeeping the verdict requires, ticked REL-08, and closed Phase 27 halted-for-root-replan
while v9.1.0 ships in full.

## Task 1 — the post-arm reading

- **HEAD read:** `7d7c1d9a75ceecf4d76c840a3952ed34b01e2f77`, i.e. the `[9.1.0]` commit `de18524`
  plus its summary commit `7d7c1d9`.
- **Protocol freeze:** `git diff --stat 1846788 HEAD -- tests/recurrence-reading-v9.1/protocol.md`
  printed nothing. The protocol is byte-identical between timings.
- **Detector freeze:** `git log --oneline f189c99..HEAD -- scripts/gen-gate-docs.py` lists only
  `8f16db9` (plan 27-06). No detector changed after 27-06.
- **Scanner arm:** written by the interrupted session (`post-arm-scanner.md`); every instrument is
  clean. This session read it back and confirmed it parses.
- **Prose arm, invocation (verbatim, identical for both readers except cwd and output file):**

  ```sh
  ALLOWED="Read Grep Glob Bash(git show:*) Bash(git log:*) Bash(git rev-parse:*) Bash(git diff:*) Bash(cat:*) Bash(grep:*) Bash(find:*) Bash(wc:*) Bash(ls:*) Bash(head:*) Bash(tail:*) Bash(sed -n:*)"
  cd <fresh scratch cwd outside the repo>
  claude -p "$(cat reader-prompt.md)" --add-dir /home/chrisdavidson/Projects/first-principles-skill \
    --allowedTools $ALLOWED --permission-prompts none --output-format text   # reader A: json
  ```

  `reader-prompt.md` (sha256 `58f6796c…e8a1`) is the pre-arm prompt with only the commit sha
  changed. It carries the verbatim protocol and nothing else: no pre-arm record, no scanner
  reading, no expected figure, no mention of another reader.
- **Attempts, in order:**

  | Attempt | Time (EDT) | Model | Outcome |
  |---|---|---|---|
  | A1, B1 | 2026-09-11 01:52 | `claude-fable-5-1` | both stopped after ~25 s: "You've hit your monthly spend limit … resets 4:20am" |
  | A2, B2 | 05:24 | `claude-fable-5-1` | **B2 completed 05:36** (transcribed); A2 stopped 05:36: "… resets 10:20am" |
  | A3 | 10:24 → 10:48 | `claude-opus-5` | completed, 227 turns (transcribed) |

- **Neither post-arm reader was given either pre-arm record.** Both session transcripts were
  scanned afterwards: no tool call names a path under `tests/recurrence-reading-v9.1/`. **Disclosed
  bound:** both readers read `docs/conformance-baseline.md`. It is on the protocol's own surface
  list, and its pre-arm instrument-gap paragraph publishes the pre-arm union's `file:line` ids.
  Reader A disclosed this in its method account; reader B's account does not mention it. Recorded
  in both headers and in the README's new post-arm bound paragraph.
- **Method accounts:** each reader's own account is transcribed byte-for-byte in its record file's
  `## Method account` section. Both state that no scanner function and no `gen-gate-docs.py --check`
  was run. Reader B walked every top-level `docs/*.md` in full, all `docs/gates/*.md`, all of
  `CHANGELOG.md`, and the `.planning/` core files, grep-sweeping the rest. Reader A read the
  product-tier core in full, read gate-page narratives, and grep-triaged `scripts/`. It limited
  `.planning/` to git-indexed paths.
- **Fence classes:** all 44 + 59 rows are FENCED. No site lies in a real generated region
  (checked with an opener/closer-paired detector), none is HEADLINE-LOCK's headline statement, none
  is an enumerated stamp, and none is in a matrix file. This is consistent with pre-arm, where all
  rows were FENCED.
- **Publication:** `python3 scripts/report-conformance.py` regenerated the pair. The section names
  all six files with a sites/claims pair per tier, and carries `**Instrument gap (pre-arm).**`,
  `**Instrument gap (post-arm).**` and three `**Timing delta (…).**` paragraphs. It contains no
  `not yet recorded`.
- **Commit:** `9c2ed12` carries the three records, the README (three custody rows with real
  sha256s) and the regenerated pair. The `[9.1.0]` CHANGELOG commit is `de18524` and the addendum
  commit is `551a4f4`, so the records' commit is not the CHANGELOG commit.
- `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (26/26)`.

## Task 2 — the trip verdict

TRIP: fired

**The computation.** The union is built over both readers, both tiers and both timings, keyed by
`(timing, file:line)`. It contains 40 pre-arm sites, matching 27-07's independent count, and 73
post-arm sites. Every recording row's `how derived` command was re-run this session; the
transcript is below. Where Markdown's `\|` was ambiguous, both renderings were run. The four
commands the cell parser could not extract whole were re-derived by hand:

- headline moves: `grep -c -E '^\| (6|7|8|9|1[0-4]) \|' docs/requirements-traceability.md` → `9`
- CONF-GATE: `grep -o 'control_count`: `[0-9]*' docs/gates/CONF-GATE.md` → `44`
- conformance drift gate: the same command on `PRECOMMIT-conformance-baseline-drift-gate.md` → `110`
- labelled surfaces: `grep -cE '^## [a-z]+-[a-z]+$' docs/conformance-baseline.md` → `6`

Every site's live value still disagrees with its claim, so condition (a) holds throughout. No live
value has moved into agreement since it was recorded.

**The verdict does not rest on any disputed site.** At post-arm, 29 sites were recorded by both
readers; at pre-arm, 19 were. Among the corroborated sites that meet all three conditions at both
timings are `README.md:143` (claims 644 lines; `wc -l` → 773), `docs/CONFIGURATION.md:148`,
`docs/DEVELOPMENT.md:171` and `docs/ONBOARDING.md:113` (claim "two" pre-commit gates; live 5),
and `docs/TESTING.md:117`/`:118` (line citations 2156/2178; live 2190/2212).

**Attribution.** Every post-arm command was also re-run against a worktree of the pre-arm commit
`33fe35b`. Four post-arm sites were **true at pre-arm and made stale during the release block**:

| Site | Claim | Live at pre-arm | Live at post-arm |
|---|---|---|---|
| `CLAUDE.md:334` | "305-row matrix" | 305 | 323 |
| `docs/README.md:157` | "305-row matrix" | 305 | 323 |
| `docs/README.md:36` (disputed, B only) | chain terminus "286 → 305" | 305 | 323 |
| `docs/README.md:27` | "moved eight times" | 8 | 9 |

In each case plan 27-06's row registration moved the live value, in a file 27-06 touched. None of
the four sites' own bytes changed, which is why 27-07's fence check (every site HELD) could not
see them. Every other tracked post-arm site was already false at pre-arm, so it is residue. The
`.planning/` sites have no git history and are not attributable.

**Consequences (D-27-09 / D-27-10), all done:**

- **Consolidation.** Dated pointer paragraphs were appended to 999.54 (`docs/README.md:110`,
  `:217`), 999.57 (`CLAUDE.md:330`/`:332`) and 999.58 (`docs/README.md:110`, `:217`).
- **Group by group:**
  - (a) structural: no owner, carried to 999.77.
  - (b) population: no owner, carried to 999.77.
  - (c) shape: partly owned (the three pointers above); the remainder goes to 999.77.
  - (d) tier: no owner, carried to 999.77. 999.41 concerns over-firing, not this gap.
- **999.77** was filed after 999.76 in 999.49's form, with all nine D-27-09 sections in order.
  Empty sub-shapes are named as empty.
- **Addendum.** The `[9.1.0]` addendum is commit `551a4f4`, and `git show --stat` lists only
  `CHANGELOG.md`. It was tested in-process with `_scan_text_for_literal_hits`, which found 78
  hits both before and after, so the addendum adds none. After removing the date, the backlog
  numbers and the `file:line` line numbers, no digits remain, and it contains no count words.
- `.planning/ROADMAP.md` is gitignored (`git check-ignore -v` → `.gitignore:1:.planning/`), so no
  commit was made for the backlog edits.
- **No record-named site was edited.** The measurement was not repaired.

### Union computation

| # | timing | site | reader(s) | tier | reach group | (a) disagrees, re-run this session | (b) named re-runnable command | (c) not excluded | disputed | attribution |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | pre | `.planning/MILESTONE-CONTEXT.md:14` | A | apparatus | (d) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | pre-arm reading |
| 2 | pre | `.planning/MILESTONE-CONTEXT.md:265` | A | apparatus | (d) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | pre-arm reading |
| 3 | pre | `.planning/PROJECT.md:9` | B | apparatus | (d) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only B) | pre-arm reading |
| 4 | pre | `.planning/REQUIREMENTS.md:346` | A | apparatus | (d) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | pre-arm reading |
| 5 | pre | `CLAUDE.md:330` | B | product | (c) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only B) | pre-arm reading |
| 6 | pre | `CLAUDE.md:381` | AB | product | (c) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | pre-arm reading |
| 7 | pre | `CLAUDE.md:68` | AB | product | (a) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | pre-arm reading |
| 8 | pre | `README.md:143` | AB | product | (b) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | pre-arm reading |
| 9 | pre | `README.md:145` | B | product | (b) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only B) | pre-arm reading |
| 10 | pre | `docs/CONFIGURATION.md:148` | AB | product | (b) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | pre-arm reading |
| 11 | pre | `docs/CONFIGURATION.md:18` | AB | product | (b) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | pre-arm reading |
| 12 | pre | `docs/DEVELOPMENT.md:153` | AB | product | (b) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | pre-arm reading |
| 13 | pre | `docs/DEVELOPMENT.md:171` | AB | product | (b) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | pre-arm reading |
| 14 | pre | `docs/MEASUREMENT-MAP.md:17` | AB | product | (c) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | pre-arm reading |
| 15 | pre | `docs/ONBOARDING.md:113` | AB | product | (b) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | pre-arm reading |
| 16 | pre | `docs/README.md:110` | AB | product | (c) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | pre-arm reading |
| 17 | pre | `docs/README.md:217` | AB | product | (c) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | pre-arm reading |
| 18 | pre | `docs/TESTING.md:117` | AB | product | (a) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | pre-arm reading |
| 19 | pre | `docs/TESTING.md:118` | AB | product | (a) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | pre-arm reading |
| 20 | pre | `docs/TESTING.md:99` | B | product | (c) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only B) | pre-arm reading |
| 21 | pre | `docs/gates/CONF-GATE.md:42` | A | product | (c) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | pre-arm reading |
| 22 | pre | `docs/gates/QUAL-01.md:244` | A | product | (c) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | pre-arm reading |
| 23 | pre | `docs/gates/QUAL-01.md:246` | A | product | (c) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | pre-arm reading |
| 24 | pre | `docs/live-monitoring-runbook.md:173` | AB | product | (b) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | pre-arm reading |
| 25 | pre | `docs/live-monitoring-runbook.md:59` | AB | product | (b) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | pre-arm reading |
| 26 | pre | `docs/live-monitoring-runbook.md:87` | AB | product | (b) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | pre-arm reading |
| 27 | pre | `docs/requirements-traceability.md:294` | B | product | (b) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only B) | pre-arm reading |
| 28 | pre | `docs/testing-agents-headlessly.md:249` | AB | product | (b) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | pre-arm reading |
| 29 | pre | `docs/v8.0-final-closure.md:113` | AB | product | (b) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | pre-arm reading |
| 30 | pre | `docs/v8.0-final-closure.md:15` | B | product | (b) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only B) | pre-arm reading |
| 31 | pre | `docs/v8.0-final-closure.md:20` | A | product | (b) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | pre-arm reading |
| 32 | pre | `docs/v8.0-final-closure.md:21` | AB | product | (b) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | pre-arm reading |
| 33 | pre | `docs/v8.0-final-closure.md:98` | A | product | (b) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | pre-arm reading |
| 34 | pre | `scripts/_battery_core.py:2385` | A | apparatus | (d) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | pre-arm reading |
| 35 | pre | `scripts/check-quality-harness.py:4232` | A | apparatus | (d) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | pre-arm reading |
| 36 | pre | `scripts/check-quality-harness.py:9857` | A | apparatus | (d) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | pre-arm reading |
| 37 | pre | `scripts/check-step0-live.py:1784` | A | apparatus | (d) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | pre-arm reading |
| 38 | pre | `scripts/check-step0-live.py:8` | A | apparatus | (c) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | pre-arm reading |
| 39 | pre | `scripts/gen-gate-docs.py:3390` | A | apparatus | (d) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | pre-arm reading |
| 40 | pre | `scripts/sync-content.py:131` | A | apparatus | (d) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | pre-arm reading |
| 41 | post | `.planning/MILESTONE-CONTEXT.md:14` | B | apparatus | (d) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only B) | no git history (gitignored); not attributable |
| 42 | post | `.planning/MILESTONE-CONTEXT.md:4` | B | apparatus | (d) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only B) | no git history (gitignored); not attributable |
| 43 | post | `.planning/PROJECT.md:545` | B | apparatus | (d) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only B) | no git history (gitignored); not attributable |
| 44 | post | `.planning/PROJECT.md:550` | B | apparatus | (d) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only B) | no git history (gitignored); not attributable |
| 45 | post | `.planning/PROJECT.md:88` | B | apparatus | (d) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only B) | no git history (gitignored); not attributable |
| 46 | post | `.planning/PROJECT.md:9` | B | apparatus | (d) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only B) | no git history (gitignored); not attributable |
| 47 | post | `.planning/REQUIREMENTS.md:346` | B | apparatus | (d) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only B) | no git history (gitignored); not attributable |
| 48 | post | `CLAUDE.md:332` | AB | product | (c) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | residue: already false at pre-arm |
| 49 | post | `CLAUDE.md:334` | AB | product | (c) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | NEW at post-arm: true at pre-arm, made stale when plan 27-06 moved its live value; file touched by a release act |
| 50 | post | `CLAUDE.md:383` | AB | product | (c) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | residue: already false at pre-arm |
| 51 | post | `CLAUDE.md:68` | AB | product | (a) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | residue: already false at pre-arm |
| 52 | post | `README.md:143` | AB | product | (b) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | residue: already false at pre-arm |
| 53 | post | `README.md:145` | B | product | (b) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only B) | residue: already false at pre-arm |
| 54 | post | `docs/CONFIGURATION.md:148` | AB | product | (b) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | residue: already false at pre-arm |
| 55 | post | `docs/CONFIGURATION.md:18` | AB | product | (b) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | residue: already false at pre-arm |
| 56 | post | `docs/DEVELOPMENT.md:153` | AB | product | (b) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | residue: already false at pre-arm |
| 57 | post | `docs/DEVELOPMENT.md:171` | AB | product | (b) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | residue: already false at pre-arm |
| 58 | post | `docs/MEASUREMENT-MAP.md:17` | AB | product | (c) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | residue: already false at pre-arm |
| 59 | post | `docs/MEASUREMENT-MAP.md:64` | B | product | (c) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only B) | residue: already false at pre-arm |
| 60 | post | `docs/ONBOARDING.md:113` | AB | product | (b) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | residue: already false at pre-arm |
| 61 | post | `docs/README.md:105` | B | product | (c) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only B) | residue: already false at pre-arm |
| 62 | post | `docs/README.md:110` | B | product | (c) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only B) | residue: already false at pre-arm |
| 63 | post | `docs/README.md:157` | AB | product | (c) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | NEW at post-arm: true at pre-arm, made stale when plan 27-06 moved its live value; file touched by a release act |
| 64 | post | `docs/README.md:217` | AB | product | (c) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | residue: already false at pre-arm |
| 65 | post | `docs/README.md:27` | AB | product | (c) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | NEW at post-arm: true at pre-arm, made stale when plan 27-06 moved its live value; file touched by a release act |
| 66 | post | `docs/README.md:36` | B | product | (c) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only B) | NEW at post-arm: true at pre-arm, made stale when plan 27-06 moved its live value; file touched by a release act |
| 67 | post | `docs/TESTING.md:117` | AB | product | (a) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | residue: already false at pre-arm |
| 68 | post | `docs/TESTING.md:118` | AB | product | (a) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | residue: already false at pre-arm |
| 69 | post | `docs/TESTING.md:99` | AB | product | (c) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | residue: already false at pre-arm |
| 70 | post | `docs/gates/CONF-GATE.md:42` | AB | product | (c) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | residue: already false at pre-arm |
| 71 | post | `docs/gates/QUAL-01.md:244` | A | product | (c) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | residue: already false at pre-arm |
| 72 | post | `docs/gates/QUAL-01.md:246` | A | product | (c) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | residue: already false at pre-arm |
| 73 | post | `docs/gates/STEP0-08.md:28` | A | product | (c) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | residue: already false at pre-arm |
| 74 | post | `docs/live-monitoring-runbook.md:173` | AB | product | (b) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | residue: already false at pre-arm |
| 75 | post | `docs/live-monitoring-runbook.md:59` | AB | product | (b) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | residue: already false at pre-arm |
| 76 | post | `docs/live-monitoring-runbook.md:87` | AB | product | (b) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | residue: already false at pre-arm |
| 77 | post | `docs/requirements-traceability.md:296` | AB | product | (b) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | residue: already false at pre-arm |
| 78 | post | `docs/testing-agents-headlessly.md:249` | AB | product | (b) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | residue: already false at pre-arm |
| 79 | post | `docs/v8.0-final-closure.md:113` | AB | product | (b) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | residue: already false at pre-arm |
| 80 | post | `docs/v8.0-final-closure.md:15` | AB | product | (b) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | residue: already false at pre-arm |
| 81 | post | `docs/v8.0-final-closure.md:21` | AB | product | (b) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | residue: already false at pre-arm |
| 82 | post | `docs/v8.0-final-closure.md:85` | AB | product | (b) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | residue: already false at pre-arm |
| 83 | post | `docs/v8.0-final-closure.md:98` | AB | product | (b) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | residue: already false at pre-arm |
| 84 | post | `docs/v8.7-constraint-teardown.md:9` | B | product | (b) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only B) | residue: already false at pre-arm |
| 85 | post | `docs/v8.7-quality-baseline-freeze.md:8` | B | product | (b) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only B) | residue: already false at pre-arm |
| 86 | post | `first-principles/agents/references/assumption-taxonomy.md:391` | A | product | (b) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | residue: already false at pre-arm |
| 87 | post | `scripts/_gate_registry.py:1440` | A | apparatus | (d) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | residue: already false at pre-arm |
| 88 | post | `scripts/_gate_registry.py:1457` | A | apparatus | (d) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | residue: already false at pre-arm |
| 89 | post | `scripts/_gate_registry.py:1473` | A | apparatus | (d) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | residue: already false at pre-arm |
| 90 | post | `scripts/check-act-limb.py:369` | A | apparatus | (d) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | residue: already false at pre-arm |
| 91 | post | `scripts/check-conf-gate.py:352` | A | apparatus | (d) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | residue: already false at pre-arm |
| 92 | post | `scripts/check-firewall-battery.sh:196` | AB | apparatus | (d) | yes | yes | yes (recording reader's call; see disputed) | no (A and B) | residue: already false at pre-arm |
| 93 | post | `scripts/check-quality-harness.py:10866` | A | apparatus | (d) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | residue: already false at pre-arm |
| 94 | post | `scripts/check-quality-harness.py:8570` | A | apparatus | (d) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | residue: already false at pre-arm |
| 95 | post | `scripts/check-quality-harness.py:9358` | A | apparatus | (d) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | residue: already false at pre-arm |
| 96 | post | `scripts/check-quality-harness.py:9857` | A | apparatus | (d) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | residue: already false at pre-arm |
| 97 | post | `scripts/check-step0-emulator.py:1743` | A | apparatus | (d) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | residue: already false at pre-arm |
| 98 | post | `scripts/check-step0-emulator.py:424` | A | apparatus | (d) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | residue: already false at pre-arm |
| 99 | post | `scripts/check-step0-live.py:151` | A | apparatus | (d) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | residue: already false at pre-arm |
| 100 | post | `scripts/check-step0-live.py:1784` | A | apparatus | (d) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | residue: already false at pre-arm |
| 101 | post | `scripts/check-step0-live.py:1841` | A | apparatus | (d) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | residue: already false at pre-arm |
| 102 | post | `scripts/check-step0-live.py:8` | A | apparatus | (c) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | residue: already false at pre-arm |
| 103 | post | `scripts/check-traceability.py:1469` | A | apparatus | (d) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | residue: already false at pre-arm |
| 104 | post | `scripts/check-traceability.py:5832` | A | apparatus | (d) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | residue: already false at pre-arm |
| 105 | post | `scripts/gen-gate-docs.py:4327` | A | apparatus | (d) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | residue: already false at pre-arm |
| 106 | post | `scripts/gen-gate-docs.py:4917` | A | apparatus | (d) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | residue: already false at pre-arm |
| 107 | post | `scripts/sync-content.py:131` | A | apparatus | (d) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | residue: already false at pre-arm |
| 108 | post | `scripts/sync-content.py:1318` | A | apparatus | (d) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | residue: already false at pre-arm |
| 109 | post | `scripts/sync-content.py:1361` | A | apparatus | (d) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | residue: already false at pre-arm |
| 110 | post | `scripts/sync-content.py:1372` | A | apparatus | (d) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | residue: already false at pre-arm |
| 111 | post | `scripts/sync-content.py:1374` | A | apparatus | (d) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | residue: already false at pre-arm |
| 112 | post | `scripts/sync-content.py:1376` | A | apparatus | (d) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | residue: already false at pre-arm |
| 113 | post | `shared/spine/references/assumption-taxonomy.md:389` | A | product | (b) | yes | yes | yes (recording reader's call; see disputed) | **disputed** (only A) | residue: already false at pre-arm |

### Re-run transcript (this session, working tree at `7d7c1d9` plus this plan's uncommitted records)

| record | # | site | recorded live value | re-run, quoted form | re-run, GFM-rendered form |
|---|---|---|---|---|---|
| pre-arm-reader-a | 1 | `README.md:143` | 773 lines | 773 first-principles/agents/first-principles.md | 773 first-principles/agents/first-principles.md |
| pre-arm-reader-a | 2 | `docs/CONFIGURATION.md:18` | `"9.0.0"` | 6:    version: "9.1.0" | 6:    version: "9.1.0" |
| pre-arm-reader-a | 3 | `docs/CONFIGURATION.md:148` | 5 gates | 5 | 5 |
| pre-arm-reader-a | 4 | `docs/DEVELOPMENT.md:171` | 5 gates | 5 | 5 |
| pre-arm-reader-a | 5 | `docs/ONBOARDING.md:113` | 5 gates | 5 | 5 |
| pre-arm-reader-a | 6 | `docs/TESTING.md:117` | line 2190 | 2190:MIN_HEADER_HITS: int = 2 | 2190:MIN_HEADER_HITS: int = 2 |
| pre-arm-reader-a | 7 | `docs/TESTING.md:118` | line 2212 | 2212:_COMPOSER_FOCUS_CEILING: int = 4 | 2212:_COMPOSER_FOCUS_CEILING: int = 4 |
| pre-arm-reader-a | 8 | `CLAUDE.md:68` | 145 (29 non-S-A rows × 5) | 29 | 78 |
| pre-arm-reader-a | 9 | `CLAUDE.md:381` | 145 | 29 | 78 |
| pre-arm-reader-a | 10 | `docs/MEASUREMENT-MAP.md:17` | 145 | 29 | 78 |
| pre-arm-reader-a | 11 | `docs/DEVELOPMENT.md:153` | 145 | 29 | 78 |
| pre-arm-reader-a | 12 | `docs/live-monitoring-runbook.md:59` | 145 | 29 | 78 |
| pre-arm-reader-a | 13 | `docs/live-monitoring-runbook.md:87` | 145 | 29 | 78 |
| pre-arm-reader-a | 14 | `docs/live-monitoring-runbook.md:87` | 41 rows | 41 | 78 |
| pre-arm-reader-a | 15 | `docs/live-monitoring-runbook.md:173` | 41 rows | 41 | 78 |
| pre-arm-reader-a | 16 | `docs/testing-agents-headlessly.md:249` | 41 rows | 41 | 78 |
| pre-arm-reader-a | 17 | `docs/README.md:110` | 12 distinct rows | 1860:    "gap_rationale": "Full Step 0 classifier rearchitecture (GEN- | 1860:    "gap_rationale": "Full Step 0 classifier rearchitecture (GEN- |
| pre-arm-reader-a | 18 | `docs/README.md:217` | 12 distinct rows | 1860:    "gap_rationale": "Full Step 0 classifier rearchitecture (GEN- | 1860:    "gap_rationale": "Full Step 0 classifier rearchitecture (GEN- |
| pre-arm-reader-a | 19 | `docs/v8.0-final-closure.md:20` | 208/97/0/305 | "coverage_tier": "audit-only" ⏎ "coverage_tier": "audit-only" ⏎ "cover | "coverage_tier": "audit-only" ⏎ "coverage_tier": "audit-only" ⏎ "cover |
| pre-arm-reader-a | 20 | `docs/v8.0-final-closure.md:21` | 26 | 343:gate "DUAL-04" \ ⏎ 354:gate "GATE-02-v8.5" \ ⏎ 360:gate "STEP0-06" | 343:gate "DUAL-04" \ ⏎ 354:gate "GATE-02-v8.5" \ ⏎ 360:gate "STEP0-06" |
| pre-arm-reader-a | 21 | `docs/v8.0-final-closure.md:98` | 208/97/0/305 | "coverage_tier": "audit-only" ⏎ "coverage_tier": "audit-only" ⏎ "cover | "coverage_tier": "audit-only" ⏎ "coverage_tier": "audit-only" ⏎ "cover |
| pre-arm-reader-a | 22 | `docs/v8.0-final-closure.md:113` | 26 | 343:gate "DUAL-04" \ ⏎ 354:gate "GATE-02-v8.5" \ ⏎ 360:gate "STEP0-06" | 343:gate "DUAL-04" \ ⏎ 354:gate "GATE-02-v8.5" \ ⏎ 360:gate "STEP0-06" |
| pre-arm-reader-a | 23 | `docs/gates/QUAL-01.md:244` | 0 of 14 unreadable | 15:\| Files unreadable by `_slice_sections` \| 0 of 14 \| 0 of 14 \| 0 | 15:\| Files unreadable by `_slice_sections` \| 0 of 14 \| 0 of 14 \| 0 |
| pre-arm-reader-a | 24 | `docs/gates/QUAL-01.md:246` | 0 malformed of 31 | 19:\| §4 `chain_blocks` (malformed) \| 31 (0 malformed) \| 31 (0 malfo | 19:\| §4 `chain_blocks` (malformed) \| 31 (0 malformed) \| 31 (0 malfo |
| pre-arm-reader-a | 25 | `docs/gates/CONF-GATE.md:42` | 44 | control_count`: `44 | control_count`: `44 |
| pre-arm-reader-a | 26 | `scripts/check-step0-live.py:8` | 41 rows | 41 | 78 |
| pre-arm-reader-a | 27 | `scripts/check-step0-live.py:1784` | 41 rows / 205 invocations | 41 | 78 |
| pre-arm-reader-a | 28 | `scripts/sync-content.py:131` | 14 | shared/examples/composed-inversion-second-order.md ⏎ shared/examples/d | shared/examples/composed-inversion-second-order.md ⏎ shared/examples/d |
| pre-arm-reader-a | 29 | `scripts/gen-gate-docs.py:3390` | 111 | literal_scan_ledger_mechanical`=111 | literal_scan_ledger_mechanical`=111 |
| pre-arm-reader-a | 30 | `scripts/check-quality-harness.py:4232` | line 326 | 326:### Conclusion C1: [Conclusion text] | 326:### Conclusion C1: [Conclusion text] |
| pre-arm-reader-a | 31 | `scripts/check-quality-harness.py:9857` | line 316 | 316:Example: `GT-2 + GT-5 (criteria facts) → weighted totals: B=82 > A | 316:Example: `GT-2 + GT-5 (criteria facts) → weighted totals: B=82 > A |
| pre-arm-reader-a | 32 | `scripts/_battery_core.py:2385` | lines 47, 50, 103 | 47:   sharper the inverted form. ⏎ 50:   hold." Resist softening the i | 47:   sharper the inverted form. ⏎ 50:   hold." Resist softening the i |
| pre-arm-reader-a | 33 | `.planning/MILESTONE-CONTEXT.md:265` | 17 requirement boxes in that file (18 in `.planning/REQUIREMENTS.md`) | 17 | 17 |
| pre-arm-reader-a | 34 | `.planning/MILESTONE-CONTEXT.md:14` | line 265 | 14:> 4. **Line 243's "(Count: 14)" is wrong — the live population was  | 14:> 4. **Line 243's "(Count: 14)" is wrong — the live population was  |
| pre-arm-reader-a | 35 | `.planning/REQUIREMENTS.md:346` | line 265 | 14:> 4. **Line 243's "(Count: 14)" is wrong — the live population was  | 14:> 4. **Line 243's "(Count: 14)" is wrong — the live population was  |
| pre-arm-reader-b | 1 | `CLAUDE.md:68` | 145 (29 catalog rows × `--repeat 5`) | 145 | 145 |
| pre-arm-reader-b | 2 | `CLAUDE.md:330` | 8 headline moves after 133/96/0/229 | 0 | 362 |
| pre-arm-reader-b | 3 | `CLAUDE.md:381` | 145 | 145 | 145 |
| pre-arm-reader-b | 4 | `README.md:143` | 773 | 773 first-principles/agents/first-principles.md | 773 first-principles/agents/first-principles.md |
| pre-arm-reader-b | 5 | `README.md:145` | 5 | 5 | 5 |
| pre-arm-reader-b | 6 | `docs/README.md:110` | 12 distinct rows | 12 | 12 |
| pre-arm-reader-b | 7 | `docs/README.md:217` | 12 | 12 | 12 |
| pre-arm-reader-b | 8 | `docs/TESTING.md:99` | 6 | 6 | 6 |
| pre-arm-reader-b | 9 | `docs/TESTING.md:117` | 2190 | 2190:MIN_HEADER_HITS: int = 2 | 2190:MIN_HEADER_HITS: int = 2 |
| pre-arm-reader-b | 10 | `docs/TESTING.md:118` | 2212 | 2212:_COMPOSER_FOCUS_CEILING: int = 4 | 2212:_COMPOSER_FOCUS_CEILING: int = 4 |
| pre-arm-reader-b | 11 | `docs/DEVELOPMENT.md:153` | 145 | 145 | 145 |
| pre-arm-reader-b | 12 | `docs/DEVELOPMENT.md:171` | 5 | 5 | 5 |
| pre-arm-reader-b | 13 | `docs/CONFIGURATION.md:18` | `"9.0.0"` | version: "9.1.0" | version: "9.1.0" |
| pre-arm-reader-b | 14 | `docs/CONFIGURATION.md:148` | 5 | 5 | 5 |
| pre-arm-reader-b | 15 | `docs/MEASUREMENT-MAP.md:17` | 145 | 145 | 145 |
| pre-arm-reader-b | 16 | `docs/ONBOARDING.md:113` | 5 | 5 | 5 |
| pre-arm-reader-b | 17 | `docs/testing-agents-headlessly.md:249` | 29 rows | 29 | 29 |
| pre-arm-reader-b | 18 | `docs/requirements-traceability.md:294` | 97 | 106 | 106 |
| pre-arm-reader-b | 19 | `docs/live-monitoring-runbook.md:59` | 145 | 145 | 145 |
| pre-arm-reader-b | 20 | `docs/live-monitoring-runbook.md:87` | 29 | 29 | 29 |
| pre-arm-reader-b | 21 | `docs/live-monitoring-runbook.md:87` | 145 | 145 | 145 |
| pre-arm-reader-b | 22 | `docs/live-monitoring-runbook.md:173` | 29 | 29 | 29 |
| pre-arm-reader-b | 23 | `docs/v8.0-final-closure.md:15` | 8 | 0 | 362 |
| pre-arm-reader-b | 24 | `docs/v8.0-final-closure.md:21` | 26/26 | gate "DUAL-04" ⏎ gate "GATE-02-v8.5" ⏎ gate "STEP0-06" ⏎ gate "STEP0-0 | gate "DUAL-04" ⏎ gate "GATE-02-v8.5" ⏎ gate "STEP0-06" ⏎ gate "STEP0-0 |
| pre-arm-reader-b | 25 | `docs/v8.0-final-closure.md:113` | 26/26 | gate "DUAL-04" ⏎ gate "GATE-02-v8.5" ⏎ gate "STEP0-06" ⏎ gate "STEP0-0 | gate "DUAL-04" ⏎ gate "GATE-02-v8.5" ⏎ gate "STEP0-06" ⏎ gate "STEP0-0 |
| pre-arm-reader-b | 26 | `.planning/PROJECT.md:9` | 9.0.0 | "version": "9.1.0", | "version": "9.1.0", |
| post-arm-reader-a | 1 | `CLAUDE.md:68` | 145 (29 live rows × 5) | 29 | 29 |
| post-arm-reader-a | 2 | `CLAUDE.md:332` | 9 | 14 | 14 |
| post-arm-reader-a | 3 | `CLAUDE.md:334` | 323 | - reproducible: 217 ⏎ - audit-only: 106 ⏎ - gap: 0 | - reproducible: 217 ⏎ - audit-only: 106 ⏎ - gap: 0 |
| post-arm-reader-a | 4 | `CLAUDE.md:383` | 145 | 29 | 29 |
| post-arm-reader-a | 5 | `README.md:143` | 773 | 773 first-principles/agents/first-principles.md | 773 first-principles/agents/first-principles.md |
| post-arm-reader-a | 6 | `docs/CONFIGURATION.md:18` | "9.1.0" | 6:    version: "9.1.0" | 6:    version: "9.1.0" |
| post-arm-reader-a | 7 | `docs/CONFIGURATION.md:148` | 5 | 5 | 5 |
| post-arm-reader-a | 8 | `docs/DEVELOPMENT.md:153` | 145 | 29 | 29 |
| post-arm-reader-a | 9 | `docs/DEVELOPMENT.md:171` | 5 | 5 | 5 |
| post-arm-reader-a | 10 | `docs/MEASUREMENT-MAP.md:17` | 145 | 29 | 29 |
| post-arm-reader-a | 11 | `docs/ONBOARDING.md:113` | 5 | 5 | 5 |
| post-arm-reader-a | 12 | `docs/README.md:27` | 9 | 14 | 14 |
| post-arm-reader-a | 13 | `docs/README.md:157` | 323 | - reproducible: 217 ⏎ - audit-only: 106 ⏎ - gap: 0 | - reproducible: 217 ⏎ - audit-only: 106 ⏎ - gap: 0 |
| post-arm-reader-a | 14 | `docs/README.md:217` | 12 | 12 | 12 |
| post-arm-reader-a | 15 | `docs/TESTING.md:99` | 6 | 6 | 6 |
| post-arm-reader-a | 16 | `docs/TESTING.md:117` | line 2190 | 2190:MIN_HEADER_HITS: int = 2 | 2190:MIN_HEADER_HITS: int = 2 |
| post-arm-reader-a | 17 | `docs/TESTING.md:118` | line 2212 | 2212:_COMPOSER_FOCUS_CEILING: int = 4 | 2212:_COMPOSER_FOCUS_CEILING: int = 4 |
| post-arm-reader-a | 18 | `docs/gates/CONF-GATE.md:42` | 44 | 10:- `control_count`: `44` | 10:- `control_count`: `44` |
| post-arm-reader-a | 19 | `docs/gates/QUAL-01.md:244` | 0 unreadable of 14 | 15:\| Files unreadable by `_slice_sections` \| 0 of 14 \| 0 of 14 \| 0 | 15:\| Files unreadable by `_slice_sections` \| 0 of 14 \| 0 of 14 \| 0 |
| post-arm-reader-a | 20 | `docs/gates/QUAL-01.md:246` | 0 malformed (of 31) | 19:\| §4 `chain_blocks` (malformed) \| 31 (0 malformed) \| 31 (0 malfo | 19:\| §4 `chain_blocks` (malformed) \| 31 (0 malformed) \| 31 (0 malfo |
| post-arm-reader-a | 21 | `docs/gates/STEP0-08.md:28` | 8 | 446:    # Category 1: D-05 fault-injection fixtures (hardcoded malform | 446:    # Category 1: D-05 fault-injection fixtures (hardcoded malform |
| post-arm-reader-a | 22 | `docs/live-monitoring-runbook.md:59` | 145 | 29 | 29 |
| post-arm-reader-a | 23 | `docs/live-monitoring-runbook.md:87` | 41 rows; 145 invocations | 41 | 41 |
| post-arm-reader-a | 24 | `docs/live-monitoring-runbook.md:173` | 41 | 41 | 41 |
| post-arm-reader-a | 25 | `docs/requirements-traceability.md:296` | MEDIUM 67; audit-only 106; HIGH 39 | 67 | 67 |
| post-arm-reader-a | 26 | `docs/testing-agents-headlessly.md:249` | 41 | 41 | 41 |
| post-arm-reader-a | 27 | `docs/v8.0-final-closure.md:15` | 9 | 14 | 14 |
| post-arm-reader-a | 28 | `docs/v8.0-final-closure.md:21` | 26/26 | 26 tallied in the offline battery | 26 tallied in the offline battery |
| post-arm-reader-a | 29 | `docs/v8.0-final-closure.md:85` | 9 | 14 | 14 |
| post-arm-reader-a | 30 | `docs/v8.0-final-closure.md:98` | 217/106/0/323 | - reproducible: 217 ⏎ - audit-only: 106 ⏎ - gap: 0 | - reproducible: 217 ⏎ - audit-only: 106 ⏎ - gap: 0 |
| post-arm-reader-a | 31 | `docs/v8.0-final-closure.md:113` | 26/26 | 26 tallied in the offline battery | 26 tallied in the offline battery |
| post-arm-reader-a | 32 | `shared/spine/references/assumption-taxonomy.md:389` | 6 rows at lines 49–54 | 45:## 2. Assumptions Table | 45:## 2. Assumptions Table |
| post-arm-reader-a | 33 | `first-principles/agents/references/assumption-taxonomy.md:391` | 6 rows at lines 49–54 | 45:## 2. Assumptions Table | 45:## 2. Assumptions Table |
| post-arm-reader-a | 34 | `scripts/_gate_registry.py:1440` | line 1023 | 1009:                    raise ValueError( ⏎ 1016:                rais | 1009:                    raise ValueError( ⏎ 1016:                rais |
| post-arm-reader-a | 35 | `scripts/_gate_registry.py:1457` | line 1036 | 1009:                    raise ValueError( ⏎ 1016:                rais | 1009:                    raise ValueError( ⏎ 1016:                rais |
| post-arm-reader-a | 36 | `scripts/_gate_registry.py:1473` | line 1030 | 1009:                    raise ValueError( ⏎ 1016:                rais | 1009:                    raise ValueError( ⏎ 1016:                rais |
| post-arm-reader-a | 37 | `scripts/check-act-limb.py:369` | 78 | 9:- `control_count`: `78` | 9:- `control_count`: `78` |
| post-arm-reader-a | 38 | `scripts/check-conf-gate.py:352` | line 2498 | 2498:    _stripped_lines = [line.split("#", 1)[0] for line in _body.sp | 2498:    _stripped_lines = [line.split("#", 1)[0] for line in _body.sp |
| post-arm-reader-a | 39 | `scripts/check-quality-harness.py:8570` | line 488 | 488:def _assert_live_coverage(text: str, agent_path: Path) -> None: | 488:def _assert_live_coverage(text: str, agent_path: Path) -> None: |
| post-arm-reader-a | 40 | `scripts/check-quality-harness.py:9358` | line 488 | 488:def _assert_live_coverage(text: str, agent_path: Path) -> None: | 488:def _assert_live_coverage(text: str, agent_path: Path) -> None: |
| post-arm-reader-a | 41 | `scripts/check-quality-harness.py:9857` | line 316 | 316:Example: `GT-2 + GT-5 (criteria facts) → weighted totals: B=82 > A | 316:Example: `GT-2 + GT-5 (criteria facts) → weighted totals: B=82 > A |
| post-arm-reader-a | 42 | `scripts/check-quality-harness.py:10866` | line 488 | 488:def _assert_live_coverage(text: str, agent_path: Path) -> None: | 488:def _assert_live_coverage(text: str, agent_path: Path) -> None: |
| post-arm-reader-a | 43 | `scripts/check-step0-emulator.py:424` | 8 | 446:    # Category 1: D-05 fault-injection fixtures (hardcoded malform | 446:    # Category 1: D-05 fault-injection fixtures (hardcoded malform |
| post-arm-reader-a | 44 | `scripts/check-step0-emulator.py:1743` | lines 638–694 | 638:    # Category 3: RR-80-01 named emulator assertion (D-02 / D-04)  | 638:    # Category 3: RR-80-01 named emulator assertion (D-02 / D-04)  |
| post-arm-reader-a | 45 | `scripts/check-step0-live.py:8` | 41 | 41 | 41 |
| post-arm-reader-a | 46 | `scripts/check-step0-live.py:151` | line 359 | 359:def _read_catalog(path: Path) -> list[tuple[str, str, str]]: | 359:def _read_catalog(path: Path) -> list[tuple[str, str, str]]: |
| post-arm-reader-a | 47 | `scripts/check-step0-live.py:1784` | 41/205 | 41 | 41 |
| post-arm-reader-a | 48 | `scripts/check-step0-live.py:1841` | 12 | 12 | 12 |
| post-arm-reader-a | 49 | `scripts/check-traceability.py:1469` | line 16 | 16:> **v8.0 audit-validated-reqs note (D-02):** v7.12, v7.13, and v8.0 | 16:> **v8.0 audit-validated-reqs note (D-02):** v7.12, v7.13, and v8.0 |
| post-arm-reader-a | 50 | `scripts/check-traceability.py:5832` | line 196 | 196:(HARN-01, HARN-02, HARN-03). The offline battery moved **17 → 20** | 196:(HARN-01, HARN-02, HARN-03). The offline battery moved **17 → 20** |
| post-arm-reader-a | 51 | `scripts/gen-gate-docs.py:4327` | line 2098 | 2098:# surfaces cannot disagree with each other. | 2098:# surfaces cannot disagree with each other. |
| post-arm-reader-a | 52 | `scripts/gen-gate-docs.py:4917` | lines 5925 / 6183 / 6297 | 5925:_CONTROLS: tuple[tuple[str, object], ...] = ( ⏎ 6183:_CONTROL_IDS | 5925:_CONTROLS: tuple[tuple[str, object], ...] = ( ⏎ 6183:_CONTROL_IDS |
| post-arm-reader-a | 53 | `scripts/sync-content.py:131` | 29 files, 14 worked examples | first-principles/agents/references/assumption-taxonomy.md ⏎ first-prin | first-principles/agents/references/assumption-taxonomy.md ⏎ first-prin |
| post-arm-reader-a | 54 | `scripts/sync-content.py:1318` | 14 | composed-inversion-second-order.md ⏎ decompose-irreducibility.md ⏎ est | composed-inversion-second-order.md ⏎ decompose-irreducibility.md ⏎ est |
| post-arm-reader-a | 55 | `scripts/sync-content.py:1361` | 48 | 314:GENERATED_TARGET_COUNT = 48 | 314:GENERATED_TARGET_COUNT = 48 |
| post-arm-reader-a | 56 | `scripts/sync-content.py:1372` | 48 | 314:GENERATED_TARGET_COUNT = 48 | 314:GENERATED_TARGET_COUNT = 48 |
| post-arm-reader-a | 57 | `scripts/sync-content.py:1374` | 48 | 314:GENERATED_TARGET_COUNT = 48 | 314:GENERATED_TARGET_COUNT = 48 |
| post-arm-reader-a | 58 | `scripts/sync-content.py:1376` | 14 | SKILLS = ( ⏎     "pre-mortem", "inversion", "fishbone", "five-whys", " | SKILLS = ( ⏎     "pre-mortem", "inversion", "fishbone", "five-whys", " |
| post-arm-reader-a | 59 | `scripts/check-firewall-battery.sh:196` | 110 | 9:- `control_count`: `110` | 9:- `control_count`: `110` |
| post-arm-reader-b | 1 | `CLAUDE.md:68` | 205 (41 catalog rows × --repeat 5) | 41 | 78 |
| post-arm-reader-b | 2 | `CLAUDE.md:332` | 9 headline moves since v8.0 | 0 | 362 |
| post-arm-reader-b | 3 | `CLAUDE.md:334` | 323 | 323 | 323 |
| post-arm-reader-b | 4 | `CLAUDE.md:383` | 205 (41 × 5) | 41 | 78 |
| post-arm-reader-b | 5 | `README.md:143` | 773 | 773 first-principles/agents/first-principles.md | 773 first-principles/agents/first-principles.md |
| post-arm-reader-b | 6 | `README.md:145` | 5 | 0 | 5 |
| post-arm-reader-b | 7 | `docs/CONFIGURATION.md:18` | "9.1.0" | 6:    version: "9.1.0" | 6:    version: "9.1.0" |
| post-arm-reader-b | 8 | `docs/CONFIGURATION.md:148` | 5 | 0 | 5 |
| post-arm-reader-b | 9 | `docs/DEVELOPMENT.md:153` | 205 (41 × 5) | 41 | 78 |
| post-arm-reader-b | 10 | `docs/DEVELOPMENT.md:171` | 5 | 0 | 5 |
| post-arm-reader-b | 11 | `docs/MEASUREMENT-MAP.md:17` | 205 (41 × 5) | 41 | 78 |
| post-arm-reader-b | 12 | `docs/MEASUREMENT-MAP.md:64` | lines 860 and 866 | no backticked command | 860:        default=11, ⏎ 866:        default=18, |
| post-arm-reader-b | 13 | `docs/ONBOARDING.md:113` | 5 | 0 | 5 |
| post-arm-reader-b | 14 | `docs/README.md:27` | 9 | 0 | 362 |
| post-arm-reader-b | 15 | `docs/README.md:36` | 323 | 323 | 323 |
| post-arm-reader-b | 16 | `docs/README.md:105` | 29 files | 31 | 31 |
| post-arm-reader-b | 17 | `docs/README.md:110` | 12 | jq: error: syntax error, unexpected INVALID_CHARACTER, expecting '\|'  | 12 |
| post-arm-reader-b | 18 | `docs/README.md:157` | 323 | 323 | 323 |
| post-arm-reader-b | 19 | `docs/README.md:217` | 12 | jq: error: syntax error, unexpected INVALID_CHARACTER, expecting '\|'  | 12 |
| post-arm-reader-b | 20 | `docs/TESTING.md:99` | 6 | no backticked command | no backticked command |
| post-arm-reader-b | 21 | `docs/TESTING.md:117` | line 2190 | 2190:MIN_HEADER_HITS: int = 2 | 2190:MIN_HEADER_HITS: int = 2 |
| post-arm-reader-b | 22 | `docs/TESTING.md:118` | line 2212 | 2212:_COMPOSER_FOCUS_CEILING: int = 4 | 2212:_COMPOSER_FOCUS_CEILING: int = 4 |
| post-arm-reader-b | 23 | `docs/gates/CONF-GATE.md:42` | 44 | bash: -c: line 1: unexpected EOF while looking for matching `'' | bash: -c: line 1: unexpected EOF while looking for matching `'' |
| post-arm-reader-b | 24 | `docs/live-monitoring-runbook.md:59` | 205 (41 × 5) | 41 | 78 |
| post-arm-reader-b | 25 | `docs/live-monitoring-runbook.md:87` | 41 | 41 | 78 |
| post-arm-reader-b | 26 | `docs/live-monitoring-runbook.md:87` | 205 (41 × 5) | 41 | 78 |
| post-arm-reader-b | 27 | `docs/live-monitoring-runbook.md:173` | 41 | 41 | 78 |
| post-arm-reader-b | 28 | `docs/requirements-traceability.md:296` | 106 | jq: error: syntax error, unexpected INVALID_CHARACTER, expecting '\|'  | 106 |
| post-arm-reader-b | 29 | `docs/testing-agents-headlessly.md:249` | 41 | 41 | 78 |
| post-arm-reader-b | 30 | `docs/v8.0-final-closure.md:15` | 9 | 0 | 362 |
| post-arm-reader-b | 31 | `docs/v8.0-final-closure.md:21` | 26 (24 gate ids + 2 inline checks) | 0 | 24 |
| post-arm-reader-b | 32 | `docs/v8.0-final-closure.md:85` | 9 | 0 | 362 |
| post-arm-reader-b | 33 | `docs/v8.0-final-closure.md:98` | 217/106/0/323 | 11:- `coverage_headline` (2 entries): `prose`='217 reproducible / 106  | 11:- `coverage_headline` (2 entries): `prose`='217 reproducible / 106  |
| post-arm-reader-b | 34 | `docs/v8.0-final-closure.md:113` | 26 (24 gate ids + 2 inline checks) | 0 | 24 |
| post-arm-reader-b | 35 | `docs/v8.7-constraint-teardown.md:9` | 29 files | 31 | 31 |
| post-arm-reader-b | 36 | `docs/v8.7-quality-baseline-freeze.md:8` | 26 (24 gate ids + 2 inline checks) | 0 | 24 |
| post-arm-reader-b | 37 | `scripts/check-firewall-battery.sh:196` | 110 | bash: -c: line 1: unexpected EOF while looking for matching `'' | bash: -c: line 1: unexpected EOF while looking for matching `'' |
| post-arm-reader-b | 38 | `.planning/MILESTONE-CONTEXT.md:4` | line 265 | 14:> 4. **Line 243's "(Count: 14)" is wrong — the live population was  | 14:> 4. **Line 243's "(Count: 14)" is wrong — the live population was  |
| post-arm-reader-b | 39 | `.planning/MILESTONE-CONTEXT.md:14` | line 265 | 14:> 4. **Line 243's "(Count: 14)" is wrong — the live population was  | 14:> 4. **Line 243's "(Count: 14)" is wrong — the live population was  |
| post-arm-reader-b | 40 | `.planning/PROJECT.md:9` | 9.1.0 | 9.1.0 | 9.1.0 |
| post-arm-reader-b | 41 | `.planning/PROJECT.md:88` | line 265 | 14:> 4. **Line 243's "(Count: 14)" is wrong — the live population was  | 14:> 4. **Line 243's "(Count: 14)" is wrong — the live population was  |
| post-arm-reader-b | 42 | `.planning/PROJECT.md:545` | 26 (24 gate ids + 2 inline checks) | 0 | 24 |
| post-arm-reader-b | 43 | `.planning/PROJECT.md:550` | 25 (26 tallied minus PROV-GUARD) | 0 | 24 |
| post-arm-reader-b | 44 | `.planning/REQUIREMENTS.md:346` | line 265 | 14:> 4. **Line 243's "(Count: 14)" is wrong — the live population was  | 14:> 4. **Line 243's "(Count: 14)" is wrong — the live population was  |

## Task 3 — REL-08, invariants, phase close

- **REL-08 ticked** in `.planning/REQUIREMENTS.md`, and its traceability row now reads `Complete`.
  The evidence block is structural only: the heading is present, the section names all six
  files, the entry points at that section, the instruments are published separately with the gap
  stated, the readers stay unreconciled, and the protocol has both tiers plus its prohibition.
  It contains no threshold on a recurrence count. It states that the tick does not depend on the
  trip verdict.
- **All 18 boxes:** the plan's verify command printed `UNTICKED: []`.
- **D-08 structural check:** `git diff f189c99 HEAD` shows no added `sys.exit` / `raise` /
  `return 1` predicated on a sites or claims value. The only matches are
  `RecurrenceRecordParseError` raises, and each one guards parser integrity: a missing header,
  the cell count, an invalid tier or fence class, a missing totals line, or declared totals ≠
  parsed rows. The other match is the control's own negative-fixture string. The control
  `recurrence-no-exit-code-conditioned-on-count` was invoked directly and returned PASS.
- **Invariants, by command:**
  - `FIREWALL: GREEN (26/26)`.
  - `git diff --numstat f189c99 HEAD -- .github/workflows/validation.yml` → no output.
  - `git diff --numstat f189c99 HEAD -- scripts/check-firewall-battery.sh` → `1	0`.
  - `check-version-stamps.py` → 17 stamps, all `9.1.0`, PASS.
  - `check-traceability.py --self-test` → every `V91-ROWS` and `HEADLINE-LOCK` line PASS, overall
    PASS.
- **Planning surfaces (D-27-10), all gitignored, so no commit was made:**
  - `.planning/ROADMAP.md`: the Phase 27 row is `[x]`, carries per-criterion evidence, and ends
    `(halted-for-root-replan 2026-09-11)`. The 27-09 plan box is ticked. The v9.1.0 paragraph reads
    `**SHIPPED 2026-09-11**` and names the halt and 999.77.
  - `.planning/STATE.md`: frontmatter, Current focus and Current Position are updated, and a
    closing paragraph was added citing the Phase 22 precedent.
  - The only status strings used are `halted-for-root-replan`, `HALTED FOR ROOT REPLAN` (the
    Phase 22 record's own form), `shipped` and `SHIPPED`.

## Deviations from Plan

1. **Reader B came from a prior session, and reader A from this one.** The usage limit stopped the
   interrupted session twice during the reader-spawn step. B's valid second run was transcribed
   and A was re-run alone. Disclosed in both headers.
2. **Reader A ran on a different model and output format** (`claude-opus-5`, `--output-format
   json`). Disclosed as a bound. Model is not a protocol term.
3. **An anchoring channel the plan did not anticipate.** T-27-33's mitigation ("receive neither
   pre-arm record") holds literally, but the pre-arm union's site ids reached both readers through
   `docs/conformance-baseline.md`, which is a required surface. The design cannot close this
   without editing the frozen protocol or the surface under measurement, so it was disclosed
   (README, headers, 999.77) and not closed.
4. **Reader B's header was corrected before the commit.** Its first draft said the reader never
   saw a pre-arm site list, which was false. Reader A's own disclosure prompted a check, and the
   check showed the baseline page lists the sites. The committed header states the exposure
   correctly.

## Self-Check: PASSED

- All six record files exist and parse under `_read_recurrence_records`, with totals matching
  rows (35/20, 26/12, 0/0, 59/32, 44/19, 0/0).
- `report-conformance.py --self-test` (110 controls) and `--check` exit 0. `gen-gate-docs.py
  --check` exits 0. `sh .githooks/pre-commit` exited 0 on both commits; the printed `DRIFT:` block
  is the generator self-test's own mutation control.
- The commits exist: `9c2ed12` and `551a4f4`.
