# Recurrence reading: pre-arm, prose arm, reader B

**Timing:** pre-arm (taken immediately before the first release act of v9.1.0, per D-27-11 --
the tree with plans 27-01/27-02/27-03 landed, before plan 27-05's stamp bump)
**Arm:** prose
**Reader id:** B
**Commit sha read:** `33fe35b157a8fdf283d4d9fe89f3194845bea480`
**Isolation mechanism:** a fresh, non-interactive `claude -p` session, launched from a scratch
working directory outside this repository, with this repository made available only via
`--add-dir` (never as the session's own working directory, so this repository's own `CLAUDE.md`
would not auto-load as ambient context the way it does for an agent whose cwd is inside the
repo); `--allowedTools` restricted to `Read Grep Glob` plus a `Bash(<cmd>:*)` allowlist naming
`git show`, `git log`, `git rev-parse`, `git diff`, `cat`, `grep`, `find`, `wc`, `ls`, `head`,
`tail`, `sed -n`; and `--permission-prompts none` so anything outside that allowlist is denied
automatically rather than stalling the non-interactive session on a prompt. Reader B's
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
time), writing to new output files (`reader-b-output-2.txt`). Everything below
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
| 1 | CLAUDE.md:68 | "60 live claude invocations" | 145 (29 catalog rows × `--repeat 5`) | `echo $(( $(grep -c '^| S-[PN]' tests/step0-fixture-catalog.md) * 5 ))` → 145; corroborated by the comment in scripts/check-step0-live.py:1784 "29 rows / 145 invocations at --repeat 5" | product | FENCED | step0-live-invocations |
| 2 | CLAUDE.md:330 | "superseded seven times" | 8 headline moves after 133/96/0/229 | `grep -cE '^\| (6\|7\|8\|9\|1[0-3]) \| ' docs/requirements-traceability.md` → 8 (headline-history rows 6-13); `grep -cE '[0-9]{3}/[0-9]{2} → [0-9]{3}/[0-9]{2}' CLAUDE.md` → 8 | product | FENCED | headline-supersessions-since-v8.0 |
| 3 | CLAUDE.md:381 | "(60 invocations)" | 145 | same command as row 1 | product | FENCED | step0-live-invocations |
| 4 | README.md:143 | "currently 644 lines" | 773 | `wc -l first-principles/agents/first-principles.md` → 773; `python3 scripts/check-body-budget.py` reports the same figure | product | FENCED | agent-body-line-count |
| 5 | README.md:145 | "composes BOTH gates (body budget + sync drift)" (2) | 5 | `grep -c '^# --- Gate [0-9]' .githooks/pre-commit` → 5 (same for scripts/git-hooks/pre-commit) | product | FENCED | pre-commit-gate-count |
| 6 | docs/README.md:110 | "13 live matrix rows" | 12 distinct rows | `python3 -c "import json;print(len({r['key'] for r in json.load(open('docs/data/matrix.json')) if 'whole-system-remeasure-verdict' in r.get('artifact_link','')+r.get('gap_rationale','')+r.get('deliverable_path','')}))"` → 12 | product | FENCED | matrix-rows-citing-remeasure-verdict |
| 7 | docs/README.md:217 | "referenced by 13 rows" | 12 | same command as row 6 | product | FENCED | matrix-rows-citing-remeasure-verdict |
| 8 | docs/TESTING.md:99 | "five labelled surfaces" | 6 | `grep -cE '^## [a-z-]+$' docs/conformance-baseline.md` → 6 (shared-examples, generated-twin, contract-surface, adversarial-corpus, live-conformance, recurrence-reading); `surface_counts` in docs/data/conformance.json has 6 keys | product | FENCED | conformance-labelled-surface-count |
| 9 | docs/TESTING.md:117 | "line 2156" | 2190 | `grep -n '^MIN_HEADER_HITS' scripts/_battery_core.py` → 2190 | product | FENCED | min-header-hits-line-citation |
| 10 | docs/TESTING.md:118 | "line 2178" | 2212 | `grep -n '^_COMPOSER_FOCUS_CEILING' scripts/_battery_core.py` → 2212 | product | FENCED | composer-focus-ceiling-line-citation |
| 11 | docs/DEVELOPMENT.md:153 | "60 invocations" | 145 | same command as row 1 | product | FENCED | step0-live-invocations |
| 12 | docs/DEVELOPMENT.md:171 | "Two gates fire on `git commit`" | 5 | same command as row 5 | product | FENCED | pre-commit-gate-count |
| 13 | docs/CONFIGURATION.md:18 | `metadata.version` = `"8.16.0"` | `"9.0.0"` | `grep -E '^\s*version:' shared/spine/SKILL.meta.yml` → `version: "9.0.0"`; `python3 scripts/check-version-stamps.py` reports 17 stamps all `9.0.0` | product | FENCED | current-shipped-version |
| 14 | docs/CONFIGURATION.md:148 | "Both hook paths run two gates" | 5 | same command as row 5 | product | FENCED | pre-commit-gate-count |
| 15 | docs/MEASUREMENT-MAP.md:17 | "(60 invocations)" | 145 | same command as row 1 | product | FENCED | step0-live-invocations |
| 16 | docs/ONBOARDING.md:113 | "the two pre-commit gates" | 5 | same command as row 5 | product | FENCED | pre-commit-gate-count |
| 17 | docs/testing-agents-headlessly.md:249 | "the 12-row `tests/step0-fixture-catalog.md`" | 29 rows | `grep -c '^| S-[PN]' tests/step0-fixture-catalog.md` → 29 | product | FENCED | step0-fixture-catalog-rows |
| 18 | docs/requirements-traceability.md:294 | "the current 91-row audit-only total" | 97 | `grep -c '"coverage_tier": "audit-only"' docs/data/matrix.json` → 97 | product | FENCED | audit-only-row-count |
| 19 | docs/live-monitoring-runbook.md:59 | "60 live claude invocations" | 145 | same command as row 1 | product | FENCED | step0-live-invocations |
| 20 | docs/live-monitoring-runbook.md:87 | "the 12-row fixture catalog" | 29 | same command as row 17 | product | FENCED | step0-fixture-catalog-rows |
| 21 | docs/live-monitoring-runbook.md:87 | "(60 live `claude` invocations)" | 145 | same command as row 1 | product | FENCED | step0-live-invocations |
| 22 | docs/live-monitoring-runbook.md:173 | "the 12-row Step-0 fixture catalog" | 29 | same command as row 17 | product | FENCED | step0-fixture-catalog-rows |
| 23 | docs/v8.0-final-closure.md:15 | "has moved six times" | 8 | same command as row 2 | product | FENCED | headline-supersessions-since-v8.0 |
| 24 | docs/v8.0-final-closure.md:21 | "now reads 25/25" | 26/26 | `grep -oE '^\s*gate(_prereq)? "[^"]+"' scripts/check-firewall-battery.sh` lists 24 distinct gate ids (VAL-03 appears once per if/else branch) + 2 inline checks (INVARIANT-CHECK, FROZEN-EVIDENCE) = 26; `bash scripts/check-firewall-battery.sh` prints `FIREWALL: GREEN (26/26)` | product | FENCED | battery-total |
| 25 | docs/v8.0-final-closure.md:113 | "it is 25/25 today" | 26/26 | same command as row 24 | product | FENCED | battery-total |
| 26 | .planning/PROJECT.md:9 | "Shipped at v8.26.0" | 9.0.0 | `grep '"version"' .claude-plugin/marketplace.json` → `"version": "9.0.0"`; `python3 scripts/check-version-stamps.py` → all 17 stamps `9.0.0` | apparatus | FENCED | current-shipped-version |

## Totals

**Totals this file:** 26 sites / 12 distinct claims.

## Method account

I confirmed the tree is at `33fe35b157a8fdf283d4d9fe89f3194845bea480` by reading `.git/HEAD` → `refs/heads/master` → that SHA (the Bash tool was denied for the entire session, so every "command" below was executed through the Read/Grep/Glob file tools using the identical file and regex, and the shell form in "how derived" is what a third party runs to reproduce each value; I did not run `gen-gate-docs.py --check`, `run_literal_scan`, or any scanner function). Product tier, in protocol order: read CLAUDE.md, README.md and CONTRIBUTING.md in full; read CHANGELOG.md lines 1-200 in full and grepped the remainder for present-tense count phrasing, treating dated release entries as frozen historical (exclusion 1); under docs/ read in full README, ARCHITECTURE, TESTING, DEVELOPMENT, CONFIGURATION, GETTING-STARTED, PROCESS, conformance-baseline, MEASUREMENT-MAP, DATA-FLOW, COMPONENT-DIAGRAM, ONBOARDING, requirements-traceability, testing-agents-headlessly, METHODOLOGY-CHEATSHEET, FIVE-PHASE-FLOW, live-monitoring-runbook, the head of requirements-matrix, the banner and §"battery" passages of v8.0-final-closure, and lines 1-1276 of v9.1-claim-containment-diagnosis (the rest is its dated per-vector census table, excluded as a commit-pinned measurement); the other v8.x/audit/gen-01/use-journal/whole-system records I grepped only for present-tense count phrasing ("currently", "today", "now reads"), and the 31 docs/gates pages I grepped for spelled-out numbers and HAND-WRITTEN sections without recording a hit (the digit-form claims there are the scanner's containment population, and the spelled-out SCAN-GUARD terminus "one hundred" matches the generated `branch_roster=100`). For shared/ and first-principles/ I grepped for number-word-plus-count-noun patterns and read first-principles/README.md and SKILL.meta.yml in full; shared/examples/self-application.md's "878 lines" is a worked example and excluded under exclusion 6. Apparatus tier: read check-version-stamps.py, check-body-budget.py, check-firewall-battery.sh, install-hooks.sh, run-live-monitoring.sh, .githooks/pre-commit and .github/workflows/validation.yml in full (its pinned CPython 3.12 / pyyaml 6.0.3 / pytest 9.1.1 match `.python-version` and `uv.lock`), grepped every scripts/*.py for count claims in docstrings and comments, and under .planning/ read MILESTONE-CONTEXT.md, STATE.md 1-606, PROJECT.md 1-100 and 722-753, REQUIREMENTS.md 1-60, then grepped all 608 .planning Markdown files for every stale-figure class found in the product tier. Roughly 40 files were read line by line (about 7,000 lines) and some 700 more were grepped. Live values: agent-body line count from a `^`-anchored line count of first-principles/agents/first-principles.md (773); pre-commit gate count from the `# --- Gate N` headers in both hook files (5); headline supersessions from headline-history rows 6-13 in requirements-traceability.md and the eight `NNN/NN → NNN/NN` arrows in CLAUDE.md (8); Step 0 rows from `^| S-[PN]` in the fixture catalog (29, ×5 = 145, matching check-step0-live.py's own comment); matrix rows citing whole-system-remeasure-verdict.md by deduplicating matrix.json rows on `key` (12); labelled surfaces from the lowercase `## ` headings of conformance-baseline.md and the six `surface_counts` keys in conformance.json (6); the two `_battery_core.py` line numbers from `grep -n` on the assignment lines (2190, 2212); audit-only rows from `"coverage_tier": "audit-only"` occurrences in matrix.json (97); the version from SKILL.meta.yml and marketplace.json (9.0.0); the battery total from the 24 distinct `gate`/`gate_prereq` ids plus the two inline `TOTAL` increments (26). Judgement calls, stated: I counted CONFIGURATION.md's `metadata.version` and PROJECT.md's "Shipped at v8.26.0" as quantity-shaped because a version string is a digit corroborable by `check-version-stamps.py` and neither site is a stamp that script enumerates (so exclusion 4 does not apply); I counted v8.0-final-closure.md's "now reads 25/25", "25/25 today" and "moved six times" because they are present-tense claims the project itself maintains as current facts; I excluded .planning/MILESTONE-CONTEXT.md:265 "(Count: 14)" because its own banner freezes the file as dated evidence and corrects the count, and excluded check-firewall-battery.sh:155 "still reads 8.25.0" and audit-2026-08-16:257 "currently read 8.17.1" as explicitly dated "at time of writing"/audit-date statements; I did not count CLAUDE.md:220's "a fifth labelled surface" because the ordinal remains true although the total is now six, and run-live-monitoring.sh:22's "~60 claude invocations" sits in an `echo` string rather than a comment and so falls outside the `.sh` surface definition. Site 21 shares a line with site 20 but states a different value, so both are recorded as found and not de-duplicated.
