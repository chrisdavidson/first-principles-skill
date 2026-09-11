---
phase: 27-ship-v9-1-0
plan: 04
subsystem: recurrence-reading-instrument
tags: [measurement, evidence-freeze, pre-arm, two-instruments, two-readers, REL-08]

dependency-graph:
  requires:
    - phase: 27-ship-v9-1-0 (plan 01)
      provides: "tests/recurrence-reading-v9.1/protocol.md, README.md (the sweep protocol and frozen-evidence discipline this plan executes)"
    - phase: 27-ship-v9-1-0 (plan 03)
      provides: "scripts/report-conformance.py's recurrence-reading surface (reader/render/headline), inert until this plan's record files exist"
  provides:
    - "tests/recurrence-reading-v9.1/pre-arm-scanner.md (scanner arm, 0 sites / 0 distinct claims -- every frozen instrument reads clean)"
    - "tests/recurrence-reading-v9.1/pre-arm-reader-a.md (prose arm, reader A, 35 sites / 20 distinct claims)"
    - "tests/recurrence-reading-v9.1/pre-arm-reader-b.md (prose arm, reader B, 26 sites / 12 distinct claims)"
    - "docs/conformance-baseline.md / docs/data/conformance.json publishing the pre-arm figures through the recurrence-reading surface"
    - "the trip predicate's pre-arm verdict: TRIP: fired"
  affects:
    - "plan 27-09 (post-arm reading; acts on this plan's TRIP: fired verdict)"
    - "any future replan informed by the 60 combined pre-arm sites this plan surfaced"

tech-stack:
  added: []
  patterns:
    - "two non-communicating claude -p reader sessions, spawned from a scratch cwd outside the repo, repo added only via --add-dir, read-only tool allowlist, non-interactive permission-prompts none"
    - "single-backtick-code-span-aware Markdown table-row splitter, mirroring GFM's own pipe-inside-code-span rendering rule"

key-files:
  created:
    - tests/recurrence-reading-v9.1/pre-arm-scanner.md
    - tests/recurrence-reading-v9.1/pre-arm-reader-a.md
    - tests/recurrence-reading-v9.1/pre-arm-reader-b.md
  modified:
    - tests/recurrence-reading-v9.1/README.md
    - docs/conformance-baseline.md
    - docs/data/conformance.json
    - scripts/report-conformance.py

decisions:
  - "All 61 combined pre-arm sites (35 + 26) are FENCED; none is RELEASE-OWNED -- D-15's fence therefore applies to every found site with zero collision against the release acts (open interaction #1 does not arise for this reading)."
  - "TRIP: fired -- the union trip predicate fires on multiple sites cross-corroborated identically by both independent readers, so the verdict does not rest on any single reader's disputed judgement."
  - "Fixed a genuine parser bug in report-conformance.py (Rule 1), the one file outside tests/recurrence-reading-v9.1/ this plan touches -- see Deviations."

requirements-completed: []

metrics:
  duration: "~2h10m across two sessions (spend-limit interruption at the reader-spawn step)"
  completed: "2026-09-11"
---

# Phase 27 Plan 04: The Pre-Release Recurrence Reading Summary

Took the pre-release half of D-03's two-timing recurrence measurement: the scanner arm (four frozen `gen-gate-docs.py` instruments) reads clean, and two independent, non-communicating prose readers swept the tree freely and found 35 and 26 sites respectively -- 38 combined sites the scanner cannot see by construction -- confirming the prose arm is a genuine independent read, not a scanner echo. Every found site is FENCED. The union trip predicate fires (`TRIP: fired`), recorded here for plan 27-09 to act on; nothing in this plan halts on it (D-08/D-10).

## What was built

**Task 1 -- the scanner arm's pre-release reading.** Imported `scripts/gen-gate-docs.py` in-process (the `sys.modules` pre-registration pattern from `27-RESEARCH.md`) and ran, in order: `run_literal_scan()` -> `literal_scan_problems()` (its non-exempt hits), `narrative_restatement_problems()` (its own `'finding'`-class subset), and `detail_page_containment_problems()` + `chain_terminus_problems()` over the four registered containment surfaces (`CLAUDE.md`, `docs/ARCHITECTURE.md`, `docs/TESTING.md`, `docs/gates/*.md`), replicating `cmd_check()`'s own per-surface loop exactly (same `marker_pairs`/`check_spelled_out` derivation, confirmed by reading `cmd_check()`'s source directly rather than approximating it). Every instrument read clean -- `tests/recurrence-reading-v9.1/pre-arm-scanner.md` records `0 sites / 0 distinct claims`, matching what `python3 scripts/gen-gate-docs.py --check` reports at this commit exactly (a legitimate scanner-arm outcome per `protocol.md`'s own note). `git diff f189c99 -- scripts/gen-gate-docs.py` confirmed empty both before and after this plan -- no detector was touched.

**Task 2 -- the prose arm, two independent readers.** Spawned Reader A and Reader B as separate, non-interactive `claude -p` sessions (the transport this repo's own `check-step0-live.py` already uses as precedent, adapted for a general-purpose read rather than the plugin harness), each launched from its own scratch working directory *outside* this repository, with this repository made available only via `--add-dir` (never as the session's own cwd, so this repository's `CLAUDE.md` would not auto-load as ambient context), `--allowedTools` restricted to `Read Grep Glob` plus a read-only `Bash` allowlist, and `--permission-prompts none` so anything outside the allowlist is denied rather than stalling the session. Each reader received exactly: the verbatim contents of `protocol.md`, the repository path, and the commit sha `33fe35b157a8fdf283d4d9fe89f3194845bea480` -- nothing else. Neither reader was told the other exists, shown the scanner arm's reading, or given any expected figure.

Reader A found **35 sites / 20 distinct claims** (25 product / 10 apparatus sites); Reader B found **26 sites / 12 distinct claims** (25 product / 1 apparatus site). Both totals lines are self-corroborated by `_read_recurrence_records`'s own re-derivation from the parsed rows (`--self-test` passes; see Verification). Both readers' own method-account paragraphs are transcribed verbatim in their record files' `## Method account` sections.

**Task 3 -- fence classes, the trip predicate, and publication.** Assigned a fence class to every one of the 61 combined rows against `protocol.md`'s mechanical rule, checked programmatically against the live rosters (generated-marker line ranges in `CLAUDE.md`/`docs/ARCHITECTURE.md`/`docs/TESTING.md`/`docs/README.md`/`docs/MEASUREMENT-MAP.md`/`docs/gates/QUAL-01.md`/`docs/gates/CONF-GATE.md`, the five `COVERED_HEADLINE_SURFACES`, the 17 version-stamp sites, and `docs/requirements-matrix.md`/`docs/data/matrix.json`) rather than by eyeballing -- every row landed **FENCED**; none is `RELEASE-OWNED`. Filled the README's three pre-arm chain-of-custody rows (commit sha, isolation mechanism, `sha256sum` computed after each file's final byte) and added the D-27-12 non-communicating-bound paragraph in the `live-conformance` surface's own disclosed-bound voice. Regenerated `docs/conformance-baseline.md` + `docs/data/conformance.json`; confirmed `--check` passes (byte-reproduced) and that the rendered `## recurrence-reading` section names all three pre-arm files with their real figures, names the three post-arm files as not yet recorded, and states the instrument gap (38 sites prose-not-scanner, 0 scanner-not-prose).

## The trip predicate

**TRIP: fired.**

The union predicate (`protocol.md`'s `## The trip predicate`) fires because multiple sites in the union of both readers' records satisfy all three conjunctive conditions (claimed value disagrees with the live value; the live value was obtained by a re-runnable named command; the site is not excluded under the protocol's own exclusion list) -- and it does not rest on any single reader's disputed judgement, because the following representative firing sites were found **identically by both readers**, independently:

- `README.md:143` -- agent body "currently 644 lines" vs. live `773` (`wc -l first-principles/agents/first-principles.md`) -- found by Reader A (row 1) and Reader B (row 4).
- `docs/DEVELOPMENT.md:171` -- "Two gates fire on `git commit`" vs. live `5` (`grep -cE '^(exec )?\$PY scripts/' .githooks/pre-commit`) -- found by Reader A (row 4) and Reader B (row 12).
- `CLAUDE.md:68` and `CLAUDE.md:381` -- "60 live claude invocations" / "(60 invocations)" vs. live `145` (`29 non-S-A catalog rows x 5`) -- found by both readers at both lines.
- `docs/v8.0-final-closure.md:21` -- battery "now reads 25/25" vs. live `26` (`FIREWALL: GREEN (26/26)`) -- found by both readers.

No cited firing site is a disputed site (one reader hit, the other not); the predicate's firing is corroborated, not resting on one reader's unique call. Per D-08/D-10, **nothing in this plan halts on this verdict** -- it is recorded here and acted on in plan 27-09 (the post-arm reading and, per D-10, the milestone-bookkeeping consequence if the trip still holds after the release acts).

## Falsifiability tripwire (27-VALIDATION.md), checked directly

The concrete symptom of a prose arm secretly measuring convention-compliance would be: the prose arm's findings are exactly the scanner arm's findings, with no site the scanner could not see. Observed instead: the scanner arm found **0** sites; the prose arm found **38 combined distinct sites** the scanner arm cannot see by construction (`docs/conformance-baseline.md`'s own rendered "Instrument gap (pre-arm)" line: "Sites the scanner arm recorded that the prose arm did not: none."). Both readers' method-account paragraphs (transcribed verbatim in their record files) describe a free walk across both the product and apparatus tiers in the protocol's own order, not a re-run of `gen-gate-docs.py --check`. This is the existence-proof shape `docs/PROCESS.md` §3 itself relies on for its four prior recurrences.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed `_read_recurrence_records`'s naive pipe-splitting parser -- the one file outside `tests/recurrence-reading-v9.1/` this plan touches**
- **Found during:** Task 3, first `python3 scripts/report-conformance.py` regenerate attempt.
- **Issue:** `_read_recurrence_records` split each table row with a naive `stripped.strip("|").split("|")`. Both readers' `how derived` cells legitimately quote `grep` patterns containing a literal `|` inside backticks (regex alternation, e.g. `` `grep -cE '^\| (6\|7\|8\|9\|1[0-3]) \| '` ``, or a Markdown table-row anchor like `` `^\| *S-[PN][0-9]+` ``) -- exactly the kind of concrete, re-runnable command the protocol's own record format requires. The naive split shredded 11 of the 61 combined rows into 9-16 cells instead of 8, raising `RecurrenceRecordParseError` and blocking the entire regenerate step.
- **Fix:** Added `_split_recurrence_table_row()`, a single-backtick-code-span-aware splitter (a pipe inside an open code span does not start a new cell, mirroring how GFM itself renders table pipes inside inline code), and used it at both split sites inside `_read_recurrence_records`. Left the module's other, unrelated table parser (line 477, a different function) untouched.
- **Why this is judged a bug fix rather than a fence violation, given Task 3's own acceptance criterion literally reads "No source file outside `tests/recurrence-reading-v9.1/` was edited by this plan":** the STRIDE threat register's only two Tampering entries in this plan are T-27-12 (editing *reader findings* during transcription) and T-27-13 (widening the *frozen scanner detectors*, `scripts/gen-gate-docs.py` by name). Neither names `report-conformance.py`'s own record-format parser, which is this same milestone's own newly-written apparatus (landed in plan 27-03, not one of the pre-existing "frozen instruments"). The alternative to this fix was rewriting the reader's own quoted regex text to avoid a literal `|` character, which *would* have violated the explicit, threat-registered, load-bearing constraint that a reader's six columns stay byte-verbatim (T-27-12) -- a strictly worse violation of a co-equal, more central guarantee. Between an acceptance-criterion sentence written before this exact failure mode was known to exist, and a STRIDE-registered tampering mitigation this plan is built around, the latter took precedence.
- **Scope discipline confirmed:** `control_count` unchanged at `110` (no new self-test control added); `git diff f189c99 -- scripts/gen-gate-docs.py` empty; `report-conformance.py --self-test` passes 110 controls; the fix is 32 inserted / 2 changed lines, isolated to the recurrence-reading reader.
- **Verification:** before the fix, regenerating raised `RecurrenceRecordParseError` naming the exact malformed row; after the fix, all three record files parse with `derived == declared` totals (`35,20`; `26,12`; `0,0`), `--self-test` passes 110 controls, `--check` passes with no drift.
- **Files modified:** `scripts/report-conformance.py`.
- **Commit:** `1846788`.

### Non-code events, disclosed rather than silently absorbed

**2. First reader-spawn attempt hit a monthly spend-limit 429.** Both Reader A and Reader B's first launch (same prompt, same flags, same commit sha, output files `reader-a-output.txt`/`reader-b-output.txt` under the session scratchpad) returned only `You've hit your monthly spend limit ... your session limit resets 11:20pm (America/New_York)` (158 bytes each). Those two files were **not transcribed** into any record file -- no finding in either committed record originates from that attempt. Both readers were re-launched, identically, after the stated reset (confirmed via `date`: 23:28 EDT, past 23:20), against the same confirmed-unchanged commit sha, writing to new output files (`reader-a-output-2.txt`/`reader-b-output-2.txt`). Everything in the committed record files is from that second, successful attempt. This event is recorded here per the coordinator's explicit instruction, not editorialized into either reader's findings.

---

**Total deviations:** 1 auto-fixed (Rule 1 bug, disclosed above with its scope tension named explicitly), plus 1 disclosed non-code event (the spend-limit retry). No scope creep beyond what was necessary to land a working pre-arm reading from genuine, unedited reader output.

## Verification (observed this session)

- `test -f tests/recurrence-reading-v9.1/pre-arm-scanner.md && grep -q "Totals this file:" ...` -> present, `SCANNER-ARM-PARSES` (observed).
- `python3 scripts/report-conformance.py --self-test` -> `SELF-TEST PASS — 110 controls run` (unchanged from before this plan -- no new control added).
- In-process reproduction of the scanner arm (transcribed verbatim in `pre-arm-scanner.md`'s own `## Reproduction` section): `run_literal_scan()`, `narrative_restatement_problems()`, `detail_page_containment_problems()`, `chain_terminus_problems()` all return `[]`; `reached == {'CLAUDE.md', 'docs/ARCHITECTURE.md', 'docs/TESTING.md', 'docs/gates/*.md'}` (observed).
- `git diff f189c99 -- scripts/gen-gate-docs.py` -> empty, both before and after this plan (observed twice).
- Both prose readers' record files parse under `_read_recurrence_records` with `derived == declared`: reader A `(35, 20)`, reader B `(26, 12)`, scanner `(0, 0)` (observed via direct in-process call).
- Byte-verbatim transcription proof: `diff <(sed 's/FENCED/TBD/' pre-arm-reader-{a,b}.md | tail -n +51) reader-{a,b}-output-2.txt` -> empty diff for both files (observed) -- the only edit from raw reader output to committed record is the header block plus the `TBD` -> `FENCED` fence-class substitution.
- Fence-class assignment verified programmatically (not by eyeballing): all 61 combined `file:line` sites checked against the live generated-marker ranges of every registered surface, the five `COVERED_HEADLINE_SURFACES`, the 17 version-stamp sites, and the two matrix files -- zero fall inside any of them; all 61 read `FENCED` (observed, transcript in this plan's own working notes).
- `sha256sum` of all three committed record files matches the README's chain-of-custody table exactly, re-run after commit (observed).
- Mutation demonstration (acceptance criterion): on a disposable `rsync`-copied scratch tree, inserting one fake row into `pre-arm-scanner.md` and regenerating moved the rendered `**pre-arm, scanner**` line from `0 sites / 0 distinct claims` to `1 sites / 1 distinct claims`; the real, committed tree's own rendering was re-confirmed unmoved (`0 sites / 0 distinct claims`) immediately after (observed, both readings transcribed above).
- `python3 scripts/report-conformance.py --check` -> `PASS — no drift` (observed, post-commit).
- `python3 scripts/gen-gate-docs.py --check` -> `harvested 22/22 expected script-backed entries` (observed, post-commit).
- `python3 scripts/gen-gate-docs.py --self-test` -> `SELF-TEST PASS — 112 controls run` (unchanged, observed).
- `sh .githooks/pre-commit` -> exit 0 (observed, both pre- and post-commit).
- `bash scripts/check-firewall-battery.sh` -> `FIREWALL: GREEN (26/26)`, `FROZEN-EVIDENCE` passing (observed, post-commit).
- `git diff --diff-filter=D --name-only HEAD~1 HEAD` -> empty (no unexpected deletions, observed).
- `git status --short` -> clean after commit (observed).
- `git diff --name-only HEAD~1 HEAD` -> `docs/conformance-baseline.md`, `docs/data/conformance.json`, `scripts/report-conformance.py`, `tests/recurrence-reading-v9.1/README.md`, `tests/recurrence-reading-v9.1/pre-arm-reader-a.md`, `tests/recurrence-reading-v9.1/pre-arm-reader-b.md`, `tests/recurrence-reading-v9.1/pre-arm-scanner.md` -- seven files, six of the plan's declared `files_modified` plus `scripts/report-conformance.py` (the disclosed Deviation #1 above); this is why the plan's own "exactly the six files" acceptance criterion is **not met literally**, and is recorded as such rather than glossed.

### Category B structural check (27-VALIDATION.md)

- The figure is present with its own stated N and cites its protocol (`docs/conformance-baseline.md`'s `## recurrence-reading` section header sentence names `tests/recurrence-reading-v9.1/protocol.md`) -- confirmed.
- No script's exit code is conditioned on the recurrence count: `git diff -- scripts/report-conformance.py` (this plan's own change) contains no new `sys.exit`/`raise`/`return 1` predicated on a recurrence figure -- the only new code is the table-row splitter, unconditional on any count (observed).
- Both readers' figures are present and unreconciled (not averaged, not merged) -- confirmed by direct read of the rendered section (separate `**pre-arm, prose, reader a**` / `**pre-arm, prose, reader b**` lines).
- Both instruments' figures are present separately and never summed, and the gap between them is stated -- confirmed (the `**Instrument gap (pre-arm)**` paragraph).

## Self-Check: PASSED

- `tests/recurrence-reading-v9.1/pre-arm-scanner.md` — FOUND
- `tests/recurrence-reading-v9.1/pre-arm-reader-a.md` — FOUND
- `tests/recurrence-reading-v9.1/pre-arm-reader-b.md` — FOUND
- `tests/recurrence-reading-v9.1/README.md` contains the three pre-arm chain-of-custody rows filled — FOUND
- `docs/conformance-baseline.md` contains `## recurrence-reading` with the pre-arm figures — FOUND
- `scripts/report-conformance.py` contains `_split_recurrence_table_row` — FOUND
- Commit `1846788` — FOUND (`git log --oneline --all | grep 1846788`)

## Requirements Note

`requirements: [REL-08]` is named in this plan's frontmatter, but **REL-08 is NOT marked complete by this plan**, matching plan 27-01's own precedent. REL-08's own text names the `[9.1.0]` CHANGELOG entry and product-recurrence verification as the requirement's discharge -- this plan ships only the pre-release half of the two-timing measurement (D-03); the post-arm reading (plan 27-09) and the CHANGELOG entry (a later release-act plan) are still outstanding. `.planning/REQUIREMENTS.md`'s REL-08 checkbox is left unticked deliberately.

## User Setup Required

None — no external service configuration required. (Two `claude -p` reader sessions were spawned and consumed normal usage quota; the first attempt hit the account's monthly spend limit, as disclosed above, and succeeded on retry after the stated reset with no user action needed beyond the coordinator's resume instruction.)

## Next Phase Readiness

- The pre-arm reading is fully published, fenced, and reproducible from its frozen records.
- Plan 27-09 (post-arm reading) can proceed once the intervening release acts (stamps, matrix rows, headline sweep, CHANGELOG) land; D-15's fence — every FENCED site here must stay byte-unchanged through those acts — is the concrete thing plan 27-09 must re-verify against this plan's own 61 sites.
- The `TRIP: fired` verdict is on the record for plan 27-09 to carry forward per D-09/D-10; no blocker to this plan's own completion.

---
*Phase: 27-ship-v9-1-0*
*Completed: 2026-09-11*
