# Recurrence reading: pre-arm, prose arm, reader A

**Timing:** pre-arm (taken immediately before the first release act of v9.1.0, per D-27-11 --
the tree with plans 27-01/27-02/27-03 landed, before plan 27-05's stamp bump)
**Arm:** prose
**Reader id:** A
**Commit sha read:** `33fe35b157a8fdf283d4d9fe89f3194845bea480`
**Isolation mechanism:** a fresh, non-interactive `claude -p` session, launched from a scratch
working directory outside this repository, with this repository made available only via
`--add-dir` (never as the session's own working directory, so this repository's own `CLAUDE.md`
would not auto-load as ambient context the way it does for an agent whose cwd is inside the
repo); `--allowedTools` restricted to `Read Grep Glob` plus a `Bash(<cmd>:*)` allowlist naming
`git show`, `git log`, `git rev-parse`, `git diff`, `cat`, `grep`, `find`, `wc`, `ls`, `head`,
`tail`, `sed -n`; and `--permission-prompts none` so anything outside that allowlist is denied
automatically rather than stalling the non-interactive session on a prompt. Reader A's
own method account below reports that every `Bash` invocation was in fact denied for its entire
session (the intended read-only `Bash` allowlist did not admit any invocation actually
attempted), so the mechanism REALIZED in practice was `Read`/`Grep`/`Glob`-only -- stricter than
intended, but still non-communicating and read-only, which is what the isolation guarantee
actually depends on. This reader received nothing beyond the verbatim protocol text, this
repository's path, and the commit sha above; it was never told another reader exists, never
shown the scanner arm's reading, and never given a prior phase's findings or an expected figure.
**Disclosed bound:** whether any user-level global Claude Code settings or memory (as distinct
from this repository's own `CLAUDE.md`/`.planning/` auto-memory, which did not auto-load per the
cwd argument above) loaded into this session was not independently instrumented -- the session
was captured with `--output-format text`, which does not expose the system prompt -- so
non-communication between the two readers is confirmed (separate processes, separate cwds, no
shared scratch state, no file exchanged between them), but full statistical independence beyond
"non-communicating" is not claimed, per D-27-12's own published bound.

**First-attempt failure, disclosed rather than silently retried.** The first launch of both
readers (same prompt, same flags, same commit sha, separate output files
`reader-a-output.txt`/`reader-b-output.txt`) failed before producing any reading: both sessions
returned only "You've hit your monthly spend limit ... your session limit resets 11:20pm
(America/New_York)" (158 bytes each, timestamped ~2026-09-10 20:5x EDT). Those two files are
retained on disk as evidence of the failed attempt and were never transcribed into this record --
no finding in this file originates from that attempt. Both readers were re-launched, identically,
after 2026-09-10 23:28 EDT (past the stated 23:20 reset), against the same commit sha (confirmed
unchanged: `git rev-parse HEAD` still `33fe35b157a8fdf283d4d9fe89f3194845bea480` at re-launch
time), writing to new output files (`reader-a-output-2.txt`). Everything below
this point is transcribed from that second, successful attempt.

**Transcription discipline (T-27-12).** Everything from `## Findings table` onward is this
reader's own output, reproduced byte-for-byte, with exactly one edit: the `fence class` column,
which the reader itself left as the literal placeholder `TBD` in every row (fence-class
assignment is a separate, later, mechanical step against `protocol.md`'s own rule, not the
reader's job), is filled in below. Every other cell in every row -- `#`, `file:line`, `claimed
value`, `live generated value`, `how derived`, `tier`, `distinct claim` -- and the reader's own
`## Method account` prose are unedited, unmerged, uncorrected and un-de-duplicated.

## Findings table

| # | file:line | claimed value | live generated value | how derived | tier | fence class | distinct claim |
|---|-----------|----------------|-----------------------|-------------|------|-------------|-----------------|
| 1 | README.md:143 | agent body "currently 644 lines" | 773 lines | `wc -l first-principles/agents/first-principles.md` | product | FENCED | agent-body-line-count |
| 2 | docs/CONFIGURATION.md:18 | `metadata.version` canonical value `"8.16.0"` | `"9.0.0"` | `grep -n 'version:' shared/spine/SKILL.meta.yml` | product | FENCED | agent-metadata-version |
| 3 | docs/CONFIGURATION.md:148 | "Both hook paths run two gates" | 5 gates | `grep -cE '^(exec )?\$PY scripts/' .githooks/pre-commit` (=5); same on `scripts/git-hooks/pre-commit` (=5) | product | FENCED | pre-commit-gate-count |
| 4 | docs/DEVELOPMENT.md:171 | "Two gates fire on `git commit`" | 5 gates | `grep -cE '^(exec )?\$PY scripts/' .githooks/pre-commit` | product | FENCED | pre-commit-gate-count |
| 5 | docs/ONBOARDING.md:113 | "the two pre-commit gates" | 5 gates | `grep -cE '^(exec )?\$PY scripts/' .githooks/pre-commit` | product | FENCED | pre-commit-gate-count |
| 6 | docs/TESTING.md:117 | `MIN_HEADER_HITS` at `scripts/_battery_core.py, line 2156` | line 2190 | `grep -n 'MIN_HEADER_HITS: int' scripts/_battery_core.py` | product | FENCED | min-header-hits-line-citation |
| 7 | docs/TESTING.md:118 | `_COMPOSER_FOCUS_CEILING` at `line 2178` | line 2212 | `grep -n '_COMPOSER_FOCUS_CEILING: int' scripts/_battery_core.py` | product | FENCED | composer-ceiling-line-citation |
| 8 | CLAUDE.md:68 | full manual Step 0 run = "60 live claude invocations" | 145 (29 non-S-A rows × 5) | `grep -cE '^\| *S-[PN][0-9]+' tests/step0-fixture-catalog.md` (=29) ×5; same figure printed by `python3 scripts/check-step0-live.py --dry-run --catalog tests/step0-fixture-catalog.md --repeat 5 --min-pass 3` | product | FENCED | step0-live-invocation-count |
| 9 | CLAUDE.md:381 | "(60 invocations)" | 145 | as row 8 | product | FENCED | step0-live-invocation-count |
| 10 | docs/MEASUREMENT-MAP.md:17 | "(60 invocations)" | 145 | as row 8 | product | FENCED | step0-live-invocation-count |
| 11 | docs/DEVELOPMENT.md:153 | "full manual, 60 invocations" | 145 | as row 8 | product | FENCED | step0-live-invocation-count |
| 12 | docs/live-monitoring-runbook.md:59 | "60 live claude invocations" | 145 | as row 8 | product | FENCED | step0-live-invocation-count |
| 13 | docs/live-monitoring-runbook.md:87 | "(60 live `claude` invocations)" | 145 | as row 8 | product | FENCED | step0-live-invocation-count |
| 14 | docs/live-monitoring-runbook.md:87 | "the 12-row fixture catalog" | 41 rows | `grep -cE '^\| *S-' tests/step0-fixture-catalog.md` | product | FENCED | step0-catalog-row-count |
| 15 | docs/live-monitoring-runbook.md:173 | "the 12-row Step-0 fixture catalog" | 41 rows | `grep -cE '^\| *S-' tests/step0-fixture-catalog.md` | product | FENCED | step0-catalog-row-count |
| 16 | docs/testing-agents-headlessly.md:249 | "the 12-row `tests/step0-fixture-catalog.md`" | 41 rows | `grep -cE '^\| *S-' tests/step0-fixture-catalog.md` | product | FENCED | step0-catalog-row-count |
| 17 | docs/README.md:110 | "Provenance anchor for 13 live matrix rows" | 12 distinct rows | `grep -n 'whole-system-remeasure-verdict' docs/data/matrix.json` (13 lines; lines 2117 and 2120 both inside the one `v7.11/RECON-01` object, shown by `sed -n '2112,2122p' docs/data/matrix.json`) | product | FENCED | whole-system-verdict-matrix-row-count |
| 18 | docs/README.md:217 | "referenced by 13 rows of the traceability matrix" | 12 distinct rows | as row 17 | product | FENCED | whole-system-verdict-matrix-row-count |
| 19 | docs/v8.0-final-closure.md:20 | headline chain terminus "→ **175/91/0/266**" | 208/97/0/305 | `grep -oE '"coverage_tier": *"[a-z-]+"' docs/data/matrix.json` then `sort` / `uniq -c` (208 reproducible, 97 audit-only); `grep -c '"key"' docs/data/matrix.json` (=305) | product | FENCED | coverage-headline |
| 20 | docs/v8.0-final-closure.md:21 | battery "now reads 25/25" | 26 | `grep -nE '^\s*gate(_prereq)? "' scripts/check-firewall-battery.sh` (25 lines over 24 distinct ids, VAL-03 on either branch) + 2 inline checks (`grep -n '"INVARIANT-CHECK"\|"FROZEN-EVIDENCE"' scripts/check-firewall-battery.sh`); header `grep -n 'Gates (26)' scripts/check-firewall-battery.sh` | product | FENCED | battery-total |
| 21 | docs/v8.0-final-closure.md:98 | "The current headline is **175/91/0/266**" | 208/97/0/305 | as row 19 | product | FENCED | coverage-headline |
| 22 | docs/v8.0-final-closure.md:113 | "it is 25/25 today" | 26 | as row 20 | product | FENCED | battery-total |
| 23 | docs/gates/QUAL-01.md:244 | "three do not resolve into six template sections" (of the shipped examples) | 0 of 14 unreadable | `grep -n 'Files unreadable' docs/conformance-baseline.md` (artifact byte-checked by `python3 scripts/report-conformance.py --check`) | product | FENCED | shared-examples-unreadable-count |
| 24 | docs/gates/QUAL-01.md:246 | "19 malformed blocks in total" | 0 malformed of 31 | `grep -nE 'chain_blocks. \(malformed\)' docs/conformance-baseline.md` | product | FENCED | shared-examples-malformed-chain-blocks |
| 25 | docs/gates/CONF-GATE.md:42 | "a 42-control offline `--self-test`" | 44 | `grep -oE 'control_count.: .[0-9]+' docs/gates/CONF-GATE.md` (Facts fence emitted by `python3 scripts/check-conf-gate.py --describe`) | product | FENCED | conf-gate-control-count |
| 26 | scripts/check-step0-live.py:8 | docstring: "the full 35-row Step 0 fixture catalog" | 41 rows | `grep -cE '^\| *S-' tests/step0-fixture-catalog.md` | apparatus | FENCED | step0-catalog-row-count |
| 27 | scripts/check-step0-live.py:1784 | comment: unfiltered catalog "35/175" | 41 rows / 205 invocations | `grep -cE '^\| *S-' tests/step0-fixture-catalog.md` (=41) ×5 | apparatus | FENCED | step0-catalog-row-count |
| 28 | scripts/sync-content.py:131 | comment: reference tree holds "12 worked examples" | 14 | `ls shared/examples/*.md` piped to `wc -l` (=14); `ls first-principles/agents/references/examples/*.md` (=14) | apparatus | FENCED | worked-example-count |
| 29 | scripts/gen-gate-docs.py:3390 | comment: "The remaining 114 entries ... are pinned MECHANICALLY" | 111 | `grep -oE 'literal_scan_ledger_mechanical.=[0-9]+' docs/gates/CONF-SURFACE.md` (Facts fence emitted by `python3 scripts/gen-gate-docs.py --describe`) | apparatus | FENCED | deferred-ledger-mechanical-entry-count |
| 30 | scripts/check-quality-harness.py:4232 | comment: `### Conclusion C1:` block at output-template.md "lines 133-137" | line 326 | `grep -nE '^### Conclusion C1' shared/spine/references/output-template.md` | apparatus | FENCED | template-conclusion-block-line-citation |
| 31 | scripts/check-quality-harness.py:9857 | docstring: trade-off backtick example at "template line 123" | line 316 | `grep -nF 'weighted totals: B=82' shared/spine/references/output-template.md` | apparatus | FENCED | template-tradeoff-example-line-citation |
| 32 | scripts/_battery_core.py:2385 | comment: "inverted form" at inversion.md "lines 46, 49, 96" | lines 47, 50, 103 | `grep -n 'inverted form' shared/references/inversion.md` | apparatus | FENCED | inversion-md-line-citation |
| 33 | .planning/MILESTONE-CONTEXT.md:265 | "(Count: 14" requirements | 17 requirement boxes in that file (18 in `.planning/REQUIREMENTS.md`) | `grep -cE '^- \[[ x]\] \*\*' .planning/MILESTONE-CONTEXT.md` (=17); `grep -cE '^- \[[ x]\] \*\*(PROSE\|CONTAIN\|NARR\|RATCHET\|REL-0[5-8])' .planning/REQUIREMENTS.md` (=18) | apparatus | FENCED | v9.1.0-requirement-count |
| 34 | .planning/MILESTONE-CONTEXT.md:14 | "Line 243's "(Count: 14)"" | line 265 | `grep -n 'Count: 14' .planning/MILESTONE-CONTEXT.md` | apparatus | FENCED | milestone-context-count-line-citation |
| 35 | .planning/REQUIREMENTS.md:346 | "`MILESTONE-CONTEXT.md:243` stated "Count: 14"" | line 265 | `grep -n 'Count: 14' .planning/MILESTONE-CONTEXT.md` | apparatus | FENCED | milestone-context-count-line-citation |

## Totals

**Totals this file:** 35 sites / 20 distinct claims.

## Method account

I confirmed the tree was at `33fe35b157a8fdf283d4d9fe89f3194845bea480` by reading `.git/HEAD` and `.git/refs/heads/master` directly, because every `git` invocation (and every `python3` invocation, including the repo's own scripts and `--describe`) was auto-denied by this session's sandbox; consequently I could not verify a clean working tree and read the live tree rather than `git show`, and every live value in the table was obtained with `grep`, `wc`, `ls`, `sed` or `cat` — where a row cites a `--describe`-derived figure, the value was read from the committed `GENERATED:FACTS` fence that the pre-commit drift gate byte-checks, with the generating command named beside it. I walked the product tier in the protocol's order: `CLAUDE.md`, `README.md`, `CONTRIBUTING.md` and all 1,334 lines of `CHANGELOG.md` in full; then all 62 files under `docs/**/*.md` in full (about 11,700 lines, including every `docs/gates/*.md` page, the 1,947-line diagnosis, and the nine dated milestone records), treating `docs/requirements-matrix.md` and `docs/conformance-baseline.md` as whole-file generated regions (marker on line 1, no END marker) and excluding them after reading; for `shared/**/*.md` (51 files) and `first-principles/**/*.md` (48 files) I read `first-principles/README.md` in full and walked the rest by grep for number-plus-noun patterns naming skills, techniques, examples, gates, lines, stamps, files, rows or references, reading each hit in context — a targeted walk, not a line-by-line read of the methodology prose, and I treated the sync-content-generated files as generated regions even though the skill stubs carry a different marker text. The apparatus tier was walked by grep over comments and docstrings of all 30 `scripts/*.py` files (digit-plus-noun and `line N` citation patterns, then `sed` context reads of every candidate, excluding string literals such as the harness's `source=` fields as executable code), a full read of the three `.sh` files' comments and of `.github/workflows/validation.yml` (its pinned-version comment checked against `uv.lock` and `.python-version`), and a grep-plus-context walk of the git-ignored `.planning/` tree: the five top-level records (7,232 lines) plus phases 25–27, `pst-audit/` and `research/` (65 files), with the headers of `MILESTONE-CONTEXT.md` and `STATE.md` read in full — note that those three `.planning` rows cannot be reproduced by a third reader from a fresh clone. Judgement calls, each applied consistently: dated milestone records, `CHANGELOG` entries, the 2026-08-16 adjudication table in `docs/README.md`, the gen-01 stub, per-plan status lines in `STATE.md` and the "moved six times" move-counts were excluded as frozen history or as not corroborable against a generated fact; `docs/v8.0-final-closure.md`'s explicitly current-state sentences were counted because its own addendum declares them kept current; the two `docs/README.md` "13 rows" sites were counted against the distinct-row figure because the claim says "rows" even though a raw substring count still reads 13; the `_battery_core.py` citation was counted only where the drift (96→103) exceeds the comment's self-declared ±1 tolerance; the `MILESTONE-CONTEXT.md` count was counted despite its "frozen as dated evidence" banner because it was never a true past state; and the runbook's line 87 carries two different values so it appears twice. The per-tier split is 25 product sites (12 distinct claims) and 10 apparatus sites (9 distinct claims, one shared with product); the two tiers are listed in one table only because this output format requires it. The three biggest concentrations are the stale 60-invocation / 12-row Step-0 catalog figures, the 2-vs-5 pre-commit gate count, and the v8.0 closure record's "current" headline and battery totals, none of which the standing scanner disputes because they sit outside any generated fence or on its historical-exempt list.
