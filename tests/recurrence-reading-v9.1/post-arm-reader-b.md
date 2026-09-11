# Recurrence reading: post-arm, prose arm, reader B

**Timing:** post-arm (taken on the tree that actually ships -- the `[9.1.0]` commit from plan
27-08 plus its plan-summary commit, i.e. HEAD at reading time)
**Arm:** prose
**Reader id:** B
**Commit sha read:** `7d7c1d9a75ceecf4d76c840a3952ed34b01e2f77`
**Isolation mechanism:** a fresh, non-interactive `claude -p` session, launched from a scratch
working directory outside this repository, with this repository made available only via
`--add-dir`; `--allowedTools` given the same `Read Grep Glob` plus `Bash(<cmd>:*)` allowlist the
pre-arm readers were given, and `--permission-prompts none`. The allowlist was passed as one
unquoted shell word list, so every multi-word rule (`Bash(git show:*)` and the other `git` rules,
`Bash(sed -n:*)`) was split and rejected by the CLI with an `Ignoring --allowedTools rule`
warning on stderr; this reader's own method account below reports `git`, `python3` and `awk`
denied and `wc`, `grep`, `find`, `ls` and `jq` usable. The session ran on `claude-fable-5-1`
(the account's default model at launch, read from the session's own transcript). This reader
received nothing beyond the verbatim protocol text, this repository's path and the commit sha
above; it was never told another reader exists, never shown the scanner arm's reading, and never
given either reader's pre-arm record. Its session transcript was checked after the fact: none of
its tool calls names a path under `tests/recurrence-reading-v9.1/`.
**Disclosed bound -- the pre-arm site list was reachable through a surface the protocol requires.**
`docs/conformance-baseline.md` is on the protocol's own product-tier surface list (`docs/**/*.md`),
and this reader read it. That page's `recurrence-reading` section publishes the pre-arm per-reader
sites/claims figures and, in its `**Instrument gap (pre-arm).**` paragraph, the full `file:line`
list of the pre-arm prose union. So "received neither reader's pre-arm record" holds literally --
no record file was given or opened -- but the pre-arm union's site ids were in front of this
reader, not attributed to a reader and without claimed or live values. The design cannot close
this channel without editing either the frozen protocol or the surface under measurement, and it
was not closed. Reader A, separately, disclosed the same exposure in its own words; this reader's
method account does not mention it. D-27-12's non-communicating-not-statistically-independent
bound applies to this timing as it did to the first, and the post-arm/pre-arm delta mixes tree
change with reader-to-reader variance and with this anchoring channel.

**Earlier attempts, disclosed rather than silently retried.** The first post-arm launch of both
readers (2026-09-11 ~01:52 EDT; output files `reader-a-output.txt`/`reader-b-output.txt`) returned
only "You've hit your monthly spend limit ... your session limit resets 4:20am
(America/New_York)" before producing any reading; nothing from it was transcribed. Both readers
were re-launched identically at 2026-09-11 05:24 EDT against the same unchanged commit, writing
`reader-a-output-2.txt`/`reader-b-output-2.txt`. This reader's second run completed at 05:36 EDT
and is the reading transcribed below (source file sha256
`904de5fc28eed499434f87e936b658d7291e8f27a78e85582ae295120ad4c8bb`). Reader A's second run was cut
off by the same limit and was re-run separately; see `post-arm-reader-a.md`.

**Transcription discipline (T-27-12).** Everything from `## Findings table` onward is this
reader's own output, reproduced byte-for-byte, with exactly one edit: the `fence class` column,
which the reader left as the literal placeholder `TBD` in every row, is filled in by
`protocol.md`'s mechanical rule. Every row is **FENCED**: no site lies inside a
`<!-- GENERATED ... -->` region (sub-class a); none is the coverage-headline statement
HEADLINE-LOCK locks on a `COVERED_HEADLINE_SURFACES` member (sub-class b -- the history chains in
`CLAUDE.md` and `docs/README.md` are not that statement, as at pre-arm); none is a stamp
`check-version-stamps.py` enumerates (sub-class c); and none lies in `docs/requirements-matrix.md`
or `docs/data/matrix.json` (sub-class d). Every other cell and the reader's own
`## Method account` prose are unedited, unmerged, uncorrected and un-de-duplicated.

## Findings table

| # | file:line | claimed value | live generated value | how derived | tier | fence class | distinct claim |
|---|-----------|----------------|-----------------------|-------------|------|-------------|-----------------|
| 1 | CLAUDE.md:68 | 60 live claude invocations | 205 (41 catalog rows × --repeat 5) | `grep -c -E '^\| S-' tests/step0-fixture-catalog.md` → 41 | product | FENCED | step0-live-invocation-count |
| 2 | CLAUDE.md:332 | superseded seven times | 9 headline moves since v8.0 | `grep -c -E '^\| (6\|7\|8\|9\|1[0-4]) \|' docs/requirements-traceability.md` → 9 | product | FENCED | headline-moves-since-v8.0 |
| 3 | CLAUDE.md:334 | generated 305-row matrix | 323 | `jq length docs/data/matrix.json` → 323 | product | FENCED | matrix-row-count |
| 4 | CLAUDE.md:383 | (60 invocations) | 205 (41 × 5) | `grep -c -E '^\| S-' tests/step0-fixture-catalog.md` → 41 | product | FENCED | step0-live-invocation-count |
| 5 | README.md:143 | currently 644 lines | 773 | `wc -l first-principles/agents/first-principles.md` → 773 | product | FENCED | agent-body-line-count |
| 6 | README.md:145 | composes BOTH gates (two) into pre-commit | 5 | `grep -c -E '^(\$PY\|exec \$PY) scripts/' .githooks/pre-commit` → 5 | product | FENCED | precommit-gate-count |
| 7 | docs/CONFIGURATION.md:18 | metadata.version "8.16.0" | "9.1.0" | `grep -n -E '^\s*version:' shared/spine/SKILL.meta.yml` → 9.1.0 | product | FENCED | version-stamp-value |
| 8 | docs/CONFIGURATION.md:148 | Both hook paths run two gates | 5 | `grep -c -E '^(\$PY\|exec \$PY) scripts/' .githooks/pre-commit` → 5 | product | FENCED | precommit-gate-count |
| 9 | docs/DEVELOPMENT.md:153 | full manual, 60 invocations | 205 (41 × 5) | `grep -c -E '^\| S-' tests/step0-fixture-catalog.md` → 41 | product | FENCED | step0-live-invocation-count |
| 10 | docs/DEVELOPMENT.md:171 | Two gates fire on git commit | 5 | `grep -c -E '^(\$PY\|exec \$PY) scripts/' .githooks/pre-commit` → 5 | product | FENCED | precommit-gate-count |
| 11 | docs/MEASUREMENT-MAP.md:17 | (60 invocations) | 205 (41 × 5) | `grep -c -E '^\| S-' tests/step0-fixture-catalog.md` → 41 | product | FENCED | step0-live-invocation-count |
| 12 | docs/MEASUREMENT-MAP.md:64 | argparse defaults (lines 41–42) | lines 860 and 866 | `grep -n -E 'default=(11\|18),' scripts/check-routing.py` → 860, 866 | product | FENCED | check-routing-defaults-line |
| 13 | docs/ONBOARDING.md:113 | the two pre-commit gates | 5 | `grep -c -E '^(\$PY\|exec \$PY) scripts/' .githooks/pre-commit` → 5 | product | FENCED | precommit-gate-count |
| 14 | docs/README.md:27 | headline has moved eight times | 9 | `grep -c -E '^\| (6\|7\|8\|9\|1[0-4]) \|' docs/requirements-traceability.md` → 9 | product | FENCED | headline-moves-since-v8.0 |
| 15 | docs/README.md:36 | chain terminus row count 286 → 305 | 323 | `jq length docs/data/matrix.json` → 323 | product | FENCED | matrix-row-count |
| 16 | docs/README.md:105 | 16 surfaces cite it | 29 files | `grep -rl 'v8.7-constraint-teardown' --exclude-dir=.git --exclude-dir=.planning --exclude-dir=__pycache__ --exclude-dir=.venv . \| wc -l` → 29 | product | FENCED | constraint-teardown-citing-files |
| 17 | docs/README.md:110 | 13 live matrix rows | 12 | `jq '[.[] \| select(tostring \| test("whole-system-remeasure-verdict"))] \| length' docs/data/matrix.json` → 12 | product | FENCED | remeasure-verdict-matrix-row-citations |
| 18 | docs/README.md:157 | Generated 305-row matrix | 323 | `jq length docs/data/matrix.json` → 323 | product | FENCED | matrix-row-count |
| 19 | docs/README.md:217 | referenced by 13 rows | 12 | `jq '[.[] \| select(tostring \| test("whole-system-remeasure-verdict"))] \| length' docs/data/matrix.json` → 12 | product | FENCED | remeasure-verdict-matrix-row-citations |
| 20 | docs/TESTING.md:99 | publishes five labelled surfaces | 6 | `grep -o "surface_names='[^']*'" docs/gates/PRECOMMIT-conformance-baseline-drift-gate.md` → 6 names | product | FENCED | conformance-baseline-surface-count |
| 21 | docs/TESTING.md:117 | MIN_HEADER_HITS at line 2156 | line 2190 | `grep -n -E '^MIN_HEADER_HITS:' scripts/_battery_core.py` → 2190 | product | FENCED | battery-core-min-header-hits-line |
| 22 | docs/TESTING.md:118 | _COMPOSER_FOCUS_CEILING at line 2178 | line 2212 | `grep -n -E '^_COMPOSER_FOCUS_CEILING:' scripts/_battery_core.py` → 2212 | product | FENCED | battery-core-composer-ceiling-line |
| 23 | docs/gates/CONF-GATE.md:42 | 42-control offline --self-test | 44 | `grep -o 'control_count`: `[0-9]*' docs/gates/CONF-GATE.md` → 44 | product | FENCED | conf-gate-control-count |
| 24 | docs/live-monitoring-runbook.md:59 | 60 live claude invocations | 205 (41 × 5) | `grep -c -E '^\| S-' tests/step0-fixture-catalog.md` → 41 | product | FENCED | step0-live-invocation-count |
| 25 | docs/live-monitoring-runbook.md:87 | 12-row fixture catalog | 41 | `grep -c -E '^\| S-' tests/step0-fixture-catalog.md` → 41 | product | FENCED | step0-catalog-row-count |
| 26 | docs/live-monitoring-runbook.md:87 | (60 live claude invocations) | 205 (41 × 5) | `grep -c -E '^\| S-' tests/step0-fixture-catalog.md` → 41 | product | FENCED | step0-live-invocation-count |
| 27 | docs/live-monitoring-runbook.md:173 | 12-row Step-0 fixture catalog | 41 | `grep -c -E '^\| S-' tests/step0-fixture-catalog.md` → 41 | product | FENCED | step0-catalog-row-count |
| 28 | docs/requirements-traceability.md:296 | current 91-row audit-only total | 106 | `jq '[.[] \| select(.coverage_tier=="audit-only")] \| length' docs/data/matrix.json` → 106 | product | FENCED | audit-only-row-total |
| 29 | docs/testing-agents-headlessly.md:249 | 12-row tests/step0-fixture-catalog.md | 41 | `grep -c -E '^\| S-' tests/step0-fixture-catalog.md` → 41 | product | FENCED | step0-catalog-row-count |
| 30 | docs/v8.0-final-closure.md:15 | headline has moved six times | 9 | `grep -c -E '^\| (6\|7\|8\|9\|1[0-4]) \|' docs/requirements-traceability.md` → 9 | product | FENCED | headline-moves-since-v8.0 |
| 31 | docs/v8.0-final-closure.md:21 | battery now reads 25/25 | 26 (24 gate ids + 2 inline checks) | `grep -o -E '^\s*(gate\|gate_prereq) "[A-Za-z0-9.-]+"' scripts/check-firewall-battery.sh \| grep -o '"[A-Za-z0-9.-]*"' \| sort -u \| wc -l` → 24 | product | FENCED | battery-total |
| 32 | docs/v8.0-final-closure.md:85 | the headline moved six times | 9 | `grep -c -E '^\| (6\|7\|8\|9\|1[0-4]) \|' docs/requirements-traceability.md` → 9 | product | FENCED | headline-moves-since-v8.0 |
| 33 | docs/v8.0-final-closure.md:98 | current headline is 175/91/0/266 | 217/106/0/323 | `grep -n 'coverage_headline' docs/gates/TRACE-03.md` → 217 reproducible / 106 audit-only / 0 gap / 323 total | product | FENCED | current-coverage-headline |
| 34 | docs/v8.0-final-closure.md:113 | it is 25/25 today | 26 (24 gate ids + 2 inline checks) | `grep -o -E '^\s*(gate\|gate_prereq) "[A-Za-z0-9.-]+"' scripts/check-firewall-battery.sh \| grep -o '"[A-Za-z0-9.-]*"' \| sort -u \| wc -l` → 24 | product | FENCED | battery-total |
| 35 | docs/v8.7-constraint-teardown.md:9 | sixteen files cite it | 29 files | `grep -rl 'v8.7-constraint-teardown' --exclude-dir=.git --exclude-dir=.planning --exclude-dir=__pycache__ --exclude-dir=.venv . \| wc -l` → 29 | product | FENCED | constraint-teardown-citing-files |
| 36 | docs/v8.7-quality-baseline-freeze.md:8 | battery 15 → 16, now 17 | 26 (24 gate ids + 2 inline checks) | `grep -o -E '^\s*(gate\|gate_prereq) "[A-Za-z0-9.-]+"' scripts/check-firewall-battery.sh \| grep -o '"[A-Za-z0-9.-]*"' \| sort -u \| wc -l` → 24 | product | FENCED | battery-total |
| 37 | scripts/check-firewall-battery.sh:196 | ~98-control --self-test battery | 110 | `grep -o 'control_count`: `[0-9]*' docs/gates/PRECOMMIT-conformance-baseline-drift-gate.md` → 110 | apparatus | FENCED | report-conformance-control-count |
| 38 | .planning/MILESTONE-CONTEXT.md:4 | cites line 243 below | line 265 | `grep -n 'Count: 14' .planning/MILESTONE-CONTEXT.md` → 265 | apparatus | FENCED | milestone-context-count-line-citation |
| 39 | .planning/MILESTONE-CONTEXT.md:14 | Line 243's "(Count: 14)" | line 265 | `grep -n 'Count: 14' .planning/MILESTONE-CONTEXT.md` → 265 | apparatus | FENCED | milestone-context-count-line-citation |
| 40 | .planning/PROJECT.md:9 | Shipped at v8.26.0 | 9.1.0 | `jq -r .version first-principles/.claude-plugin/plugin.json` → 9.1.0 | apparatus | FENCED | version-stamp-value |
| 41 | .planning/PROJECT.md:88 | MILESTONE-CONTEXT.md:243 | line 265 | `grep -n 'Count: 14' .planning/MILESTONE-CONTEXT.md` → 265 | apparatus | FENCED | milestone-context-count-line-citation |
| 42 | .planning/PROJECT.md:545 | runs 24 offline gates | 26 (24 gate ids + 2 inline checks) | `grep -o -E '^\s*(gate\|gate_prereq) "[A-Za-z0-9.-]+"' scripts/check-firewall-battery.sh \| grep -o '"[A-Za-z0-9.-]*"' \| sort -u \| wc -l` → 24 | apparatus | FENCED | battery-total |
| 43 | .planning/PROJECT.md:550 | the 23 that score form | 25 (26 tallied minus PROV-GUARD) | `grep -o -E '^\s*(gate\|gate_prereq) "[A-Za-z0-9.-]+"' scripts/check-firewall-battery.sh \| grep -o '"[A-Za-z0-9.-]*"' \| sort -u \| wc -l` → 24 | apparatus | FENCED | battery-total |
| 44 | .planning/REQUIREMENTS.md:346 | MILESTONE-CONTEXT.md:243 | line 265 | `grep -n 'Count: 14' .planning/MILESTONE-CONTEXT.md` → 265 | apparatus | FENCED | milestone-context-count-line-citation |

## Totals

**Totals this file:** 44 sites / 19 distinct claims.

## Method account

I confirmed HEAD by reading `.git/HEAD` and `.git/refs/heads/master` directly (git itself, python3, and awk were denied in this session, so every live value comes from `wc`, `grep`, `find`, `ls`, or `jq` run against the working tree, which I could not diff against the commit; I assumed the tree matches 7d7c1d9). I walked the product tier in the protocol's order: CLAUDE.md, README.md, CONTRIBUTING.md and all 1,436 lines of CHANGELOG.md in full; every one of the 31 top-level `docs/*.md` files in full (except the 1,948-line v9.1 diagnosis, read to line ~1,540 with its remaining per-vector census table judged frozen by that page's own commit-pinned discipline), plus all 31 `docs/gates/*.md` pages; `first-principles/README.md` in full, with the rest of `first-principles/` treated as excluded under exclusion 2 since every file opens with a whole-file `<!-- GENERATED — DO NOT EDIT -->` marker; and for `shared/` I read `shared/agent/input-contract.md` in full and swept the spine, references, skill stubs and examples by grep for number words and repository-state digits, finding only methodology content (the examples are illustrative under exclusion 6). For the apparatus tier I read the CI workflow in full, all comment lines of the three `scripts/*.sh` files (the battery script's 600-line header in full), grep-swept comments and docstrings across all 32 `scripts/*.py` files for current-state count patterns and read the contexts of every hit, and for `.planning/` read PROJECT.md, MILESTONE-CONTEXT.md, MILESTONES.md, the first 420 lines of STATE.md, the v9.1 half of REQUIREMENTS.md and ROADMAP.md's milestone overview and Phase 24–27 sections in full, grep-sweeping the remaining ~600 files (archived milestones and phase records) for present-tense count claims and treating dated plan/summary records as frozen. For each candidate I obtained the live value with the command quoted in its row: `wc -l` on the agent body (773); `grep -c` over the pre-commit hook's gate invocations (5); `jq length` and `jq select` over docs/data/matrix.json (323 rows, 106 audit-only, 12 rows citing the remeasure verdict); `grep -c '^| S-'` over the Step 0 fixture catalog (41 rows, hence 205 invocations at --repeat 5); `grep -n` for the two battery-core constants (2190, 2212), the check-routing.py defaults (860, 866), the stamp value in SKILL.meta.yml and plugin.json (9.1.0), the "Count: 14" line (265), and the generated Facts fences for CONF-GATE (44), the conformance drift gate (110 controls, 6 surface names) and TRACE-03's headline; `grep -rl … | wc -l` for files citing the teardown record (29); a `sort -u` count of distinct battery gate ids (24, plus the two inline checks I read in the script = 26); and a `grep -c` over rows 6–14 of the traceability headline-history table (9 moves since v8.0). Judgement calls I made and record here: I counted version stamps on non-enumerated surfaces (CONFIGURATION.md, PROJECT.md) as quantity-shaped ordinals; I counted "BOTH gates" as a spelled-out two; I counted the dated-but-present-tense "N files cite it" and "now 17/25" banner claims as live because the same 2026-08-16 adjudication banners were demonstrably updated after their date; I counted stale `file:line` citations as ordinals over live state; I excluded the dated census figures in the v9.1 diagnosis, the whole of MILESTONE-CONTEXT.md's body (self-labelled frozen), CHANGELOG entries, milestone-dated PROJECT.md "shipped state" paragraphs, and STATE.md's tool-maintained frontmatter (no named command reproduces its derivation). I did not run `gen-gate-docs.py --check` or any scanner function.
