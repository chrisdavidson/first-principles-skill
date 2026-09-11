# Recurrence reading: post-arm, prose arm, reader A

**Timing:** post-arm (taken on the tree that actually ships -- the `[9.1.0]` commit from plan
27-08 plus its plan-summary commit, i.e. HEAD at reading time)
**Arm:** prose
**Reader id:** A
**Commit sha read:** `7d7c1d9a75ceecf4d76c840a3952ed34b01e2f77`
**Isolation mechanism:** a fresh, non-interactive `claude -p` session (session id
`2af084b3-84d2-45f4-9e13-30778b3f9e4f`), launched from a scratch working directory outside this
repository, with this repository made available only via `--add-dir`; the same verbatim prompt
file reader B received (sha256
`58f6796c4922a7c274eef2cb2011202c2f391f841f112bdf141d77bc59d5e8a1`), the same `--allowedTools`
list passed the same way (so the same multi-word rules were rejected on stderr), and
`--permission-prompts none`. The session reported every `git` and `python3` invocation, and one
attempted `Write`, as permission denials; nothing was written to the repository. Two differences
from reader B's run, both disclosed rather than normalised: (1) this session ran on
`claude-opus-5` with a 1M context window, because the account's default model had been changed
before this re-run, while reader B's post-arm run (and both earlier post-arm launches) ran on
`claude-fable-5-1`; the pre-arm readers' model cannot now be read back, since their session
transcripts no longer exist. (2) The session was captured with `--output-format json` rather than
`text`, so its run metadata survives; the reader's `result` field is transcribed below
byte-for-byte (source file sha256
`24460e9a95cedfd5e5a6786fef4e90b84486527d4123991a108bf97a8833dc87`). The run started
2026-09-11T14:24:46Z, ended 14:48:42Z, and reported 227 turns. This reader received nothing
beyond the verbatim protocol text, this repository's path and the commit sha above; it was never
told another reader exists, never shown the scanner arm's reading, and never given either
reader's pre-arm record. Its session transcript was checked after the fact: none of its tool
calls names a path under `tests/recurrence-reading-v9.1/`.
**Disclosed bound -- the pre-arm site list was reachable through a surface the protocol requires.**
`docs/conformance-baseline.md` is on the protocol's own product-tier surface list, and its
`**Instrument gap (pre-arm).**` paragraph publishes the full `file:line` list of the pre-arm prose
union. This reader read it mid-sweep and disclosed that in its own method account below, naming
which of its hits it had found before that point and which pre-arm sites it did not record. So
"received neither reader's pre-arm record" holds literally -- no record file was given or opened
-- but the pre-arm union's site ids were in front of this reader. The model difference above adds
a third term to what the post-arm/pre-arm delta mixes, alongside tree change and
reader-to-reader variance; D-27-12's non-communicating-not-statistically-independent bound
applies unchanged.

**Earlier attempts, disclosed rather than silently retried.** The first post-arm launch
(2026-09-11 ~01:52 EDT) returned only "You've hit your monthly spend limit ... your session limit
resets 4:20am (America/New_York)". The second launch (05:24 EDT, `reader-a-output-2.txt`) was cut
off at 05:36 EDT by the same limit, "resets 10:20am (America/New_York)", before producing any
reading. Nothing from either attempt was transcribed. This third run was launched at 10:24 EDT
from a separate session, against the same unchanged commit (`git rev-parse HEAD` confirmed
`7d7c1d9a75ceecf4d76c840a3952ed34b01e2f77` immediately before launch).

**Transcription discipline (T-27-12).** Everything from `## Findings table` onward is this
reader's own output, reproduced byte-for-byte, with exactly one edit: the `fence class` column,
which the reader left as the literal placeholder `TBD` in every row, is filled in by
`protocol.md`'s mechanical rule (plus the terminal newline the JSON `result` string lacks). Every
row is **FENCED**: no site lies inside a `<!-- GENERATED ... -->` region (sub-class a -- `first-principles/agents/references/assumption-taxonomy.md`
carries a whole-file `sync-content.py` stamp, which is not a `gen-gate-docs.py --write` region);
none is the coverage-headline statement HEADLINE-LOCK locks on a `COVERED_HEADLINE_SURFACES`
member (sub-class b); none is a stamp `check-version-stamps.py` enumerates (sub-class c); and none
lies in `docs/requirements-matrix.md` or `docs/data/matrix.json` (sub-class d). Every other cell
and the reader's own `## Method account` prose are unedited, unmerged, uncorrected and
un-de-duplicated.

## Findings table

| # | file:line | claimed value | live generated value | how derived | tier | fence class | distinct claim |
|---|-----------|----------------|-----------------------|-------------|------|-------------|-----------------|
| 1 | CLAUDE.md:68 | 60 live claude invocations | 145 (29 live rows × 5) | `grep -cE '^. S-[PN][0-9]' tests/step0-fixture-catalog.md` → 29 (S-A rows are filtered out at scripts/check-step0-live.py:1848) × `--repeat 5` = 145 | product | FENCED | Step 0 live-run size (12-row catalog / 60 invocations) |
| 2 | CLAUDE.md:332 | superseded seven times | 9 | `grep -cE '^. [0-9]+ . .* [0-9/]+ → [0-9/]+' docs/requirements-traceability.md` → 14 headline-history rows; rows 6–14 come after 133/96/0/229 = 9 | product | FENCED | Coverage-headline moves since v8.0 |
| 3 | CLAUDE.md:334 | generated 305-row matrix | 323 | `sed -n '10,12p' docs/requirements-matrix.md` → 217 + 106 + 0 = 323 | product | FENCED | Requirements-matrix row count |
| 4 | CLAUDE.md:383 | (60 invocations) | 145 | same as row 1 | product | FENCED | Step 0 live-run size (12-row catalog / 60 invocations) |
| 5 | README.md:143 | currently 644 lines | 773 | `wc -l first-principles/agents/first-principles.md` → 773 | product | FENCED | Agent body line count |
| 6 | docs/CONFIGURATION.md:18 | metadata.version "8.16.0" | "9.1.0" | `grep -n 'version:' shared/spine/SKILL.meta.yml` → "9.1.0" | product | FENCED | Agent metadata.version |
| 7 | docs/CONFIGURATION.md:148 | Both hook paths run two gates | 5 | `grep -cE '^(exec )?.PY scripts/' .githooks/pre-commit` → 5 (also 5 for scripts/git-hooks/pre-commit) | product | FENCED | Pre-commit gate count |
| 8 | docs/DEVELOPMENT.md:153 | full manual, 60 invocations | 145 | same as row 1 | product | FENCED | Step 0 live-run size (12-row catalog / 60 invocations) |
| 9 | docs/DEVELOPMENT.md:171 | Two gates fire on git commit | 5 | same as row 7 | product | FENCED | Pre-commit gate count |
| 10 | docs/MEASUREMENT-MAP.md:17 | (60 invocations) | 145 | same as row 1 | product | FENCED | Step 0 live-run size (12-row catalog / 60 invocations) |
| 11 | docs/ONBOARDING.md:113 | the two pre-commit gates | 5 | same as row 7 | product | FENCED | Pre-commit gate count |
| 12 | docs/README.md:27 | headline has moved eight times since | 9 | same as row 2 | product | FENCED | Coverage-headline moves since v8.0 |
| 13 | docs/README.md:157 | Generated 305-row matrix | 323 | same as row 3 | product | FENCED | Requirements-matrix row count |
| 14 | docs/README.md:217 | referenced by 13 rows of the traceability matrix | 12 | `grep -c '^. v[0-9].*whole-system-remeasure-verdict' docs/requirements-matrix.md` → 12 | product | FENCED | Matrix rows citing whole-system-remeasure-verdict.md |
| 15 | docs/TESTING.md:99 | publishes five labelled surfaces | 6 | `grep -cE '^## [a-z]+-[a-z]+$' docs/conformance-baseline.md` → 6 (matches the 6-member `Artifact.surface` Literal at scripts/report-conformance.py:211-218) | product | FENCED | conformance-baseline labelled-surface count |
| 16 | docs/TESTING.md:117 | MIN_HEADER_HITS at _battery_core.py line 2156 | line 2190 | `grep -n '^MIN_HEADER_HITS' scripts/_battery_core.py` → 2190 | product | FENCED | _battery_core.py anti-masking constant line numbers |
| 17 | docs/TESTING.md:118 | _COMPOSER_FOCUS_CEILING at line 2178 | line 2212 | `grep -n '^_COMPOSER_FOCUS_CEILING' scripts/_battery_core.py` → 2212 | product | FENCED | _battery_core.py anti-masking constant line numbers |
| 18 | docs/gates/CONF-GATE.md:42 | a 42-control offline --self-test | 44 | `grep -n 'control_count' docs/gates/CONF-GATE.md` → 44 (the 44-entry `_CONTROL_IDS` at scripts/check-conf-gate.py:1526-1571) | product | FENCED | CONF-GATE self-test control count |
| 19 | docs/gates/QUAL-01.md:244 | three [example files] do not resolve into six template sections | 0 unreadable of 14 | `grep -n 'Files unreadable' docs/conformance-baseline.md` → "0 of 14" | product | FENCED | shared-examples conformance state (unreadable / malformed) |
| 20 | docs/gates/QUAL-01.md:246 | 19 malformed blocks in total | 0 malformed (of 31) | `grep -n 'chain_blocks. (malformed)' docs/conformance-baseline.md` → "31 (0 malformed)" | product | FENCED | shared-examples conformance state (unreadable / malformed) |
| 21 | docs/gates/STEP0-08.md:28 | --self-test runs two fixture categories | 8 | `grep -nE '^    # Category [0-9]+:' scripts/check-step0-emulator.py` → Categories 1–8 | product | FENCED | STEP0-08 self-test fixture-category count |
| 22 | docs/live-monitoring-runbook.md:59 | 60 live claude invocations | 145 | same as row 1 | product | FENCED | Step 0 live-run size (12-row catalog / 60 invocations) |
| 23 | docs/live-monitoring-runbook.md:87 | 12-row fixture catalog; 60 live claude invocations | 41 rows; 145 invocations | `grep -cE '^. S-' tests/step0-fixture-catalog.md` → 41; invocations as in row 1 | product | FENCED | Step 0 live-run size (12-row catalog / 60 invocations) |
| 24 | docs/live-monitoring-runbook.md:173 | the 12-row Step-0 fixture catalog | 41 | `grep -cE '^. S-' tests/step0-fixture-catalog.md` → 41 | product | FENCED | Step 0 live-run size (12-row catalog / 60 invocations) |
| 25 | docs/requirements-traceability.md:296 | MEDIUM audit-only 53; current 91-row audit-only total; HIGH 38 | MEDIUM 67; audit-only 106; HIGH 39 | `grep -c '^- .MEDIUM.' docs/requirements-matrix.md` → 67; `grep -c '^- .HIGH.' docs/requirements-matrix.md` → 39; `sed -n '11p' docs/requirements-matrix.md` → audit-only: 106 | product | FENCED | GAP-02 audit-only severity split and total |
| 26 | docs/testing-agents-headlessly.md:249 | the 12-row tests/step0-fixture-catalog.md | 41 | `grep -cE '^. S-' tests/step0-fixture-catalog.md` → 41 | product | FENCED | Step 0 live-run size (12-row catalog / 60 invocations) |
| 27 | docs/v8.0-final-closure.md:15 | has moved six times | 9 | same as row 2 | product | FENCED | Coverage-headline moves since v8.0 |
| 28 | docs/v8.0-final-closure.md:21 | battery "now reads 25/25" | 26/26 | `grep -oE '[0-9]+ tallied in the offline battery' CLAUDE.md` → 26 (the generated population-arithmetic sentence) | product | FENCED | Firewall battery total |
| 29 | docs/v8.0-final-closure.md:85 | the headline moved six times | 9 | same as row 2 | product | FENCED | Coverage-headline moves since v8.0 |
| 30 | docs/v8.0-final-closure.md:98 | current headline 175/91/0/266 | 217/106/0/323 | `sed -n '10,12p' docs/requirements-matrix.md` → reproducible 217, audit-only 106, gap 0 (323 total) | product | FENCED | Current coverage headline |
| 31 | docs/v8.0-final-closure.md:113 | it is 25/25 today | 26/26 | same as row 28 | product | FENCED | Firewall battery total |
| 32 | shared/spine/references/assumption-taxonomy.md:389 | five assumption rows (table at lines 47–51) | 6 rows at lines 49–54 | `grep -n '^## 2. Assumptions Table' first-principles/agents/references/examples/software-systems.md` → 45; `sed -n '49,54p'` on the same file → 6 assumption rows | product | FENCED | software-systems example assumption-row count/location |
| 33 | first-principles/agents/references/assumption-taxonomy.md:391 | five assumption rows (table at lines 47–51) | 6 rows at lines 49–54 | same as row 32 | product | FENCED | software-systems example assumption-row count/location |
| 34 | scripts/_gate_registry.py:1440 | extra= duplicate: "line 1006's raise site" | line 1023 | `grep -n 'raise ValueError' scripts/_gate_registry.py` → 1009, 1016, 1023, 1030, 1036, 1043 | apparatus | FENCED | _hook_roster_arm_clauses raise-site line numbers |
| 35 | scripts/_gate_registry.py:1457 | hook-divergence: "line 1019's raise site" | line 1036 | same as row 34 | apparatus | FENCED | _hook_roster_arm_clauses raise-site line numbers |
| 36 | scripts/_gate_registry.py:1473 | extra-branch both-markers: "line 1013's raise site" | line 1030 | same as row 34 | apparatus | FENCED | _hook_roster_arm_clauses raise-site line numbers |
| 37 | scripts/check-act-limb.py:369 | "58 controls" the HARN-01 published row "states today" | 78 | `grep -n 'control_count' docs/gates/HARN-01.md` → 78 (CLAUDE.md HARN-01 row: control_count=78) | apparatus | FENCED | HARN-01 published control count |
| 38 | scripts/check-conf-gate.py:352 | comment-stripping site at check-traceability.py "~line 2152" | line 2498 | `grep -n 'split("#", 1)' scripts/check-traceability.py` → 2498 | apparatus | FENCED | check-traceability comment-stripping site line |
| 39 | scripts/check-quality-harness.py:8570 | scripts/check-agent.py:334 (_assert_live_coverage) | line 488 | `grep -n 'def _assert_live_coverage' scripts/check-agent.py` → 488 | apparatus | FENCED | check-agent.py _assert_live_coverage line |
| 40 | scripts/check-quality-harness.py:9358 | scripts/check-agent.py:334 | line 488 | same as row 39 | apparatus | FENCED | check-agent.py _assert_live_coverage line |
| 41 | scripts/check-quality-harness.py:9857 | two rows sharing template line 123 | line 316 | `grep -n 'Example: .GT-2' shared/spine/references/output-template.md` → 316 | apparatus | FENCED | output-template "Example: GT-2" anchor line |
| 42 | scripts/check-quality-harness.py:10866 | scripts/check-agent.py:334 | line 488 | same as row 39 | apparatus | FENCED | check-agent.py _assert_live_coverage line |
| 43 | scripts/check-step0-emulator.py:424 | "Run TWO fixture categories" | 8 | same as row 21 | apparatus | FENCED | STEP0-08 self-test fixture-category count |
| 44 | scripts/check-step0-emulator.py:1743 | Category 3, lines 559–613 | lines 638–694 | `grep -nE '^    # Category [34]:' scripts/check-step0-emulator.py` → 638, 695 | apparatus | FENCED | Emulator Category 3 line range |
| 45 | scripts/check-step0-live.py:8 | full 35-row Step 0 fixture catalog | 41 | `grep -cE '^. S-' tests/step0-fixture-catalog.md` → 41 | apparatus | FENCED | Step 0 fixture-catalog row counts (total / S-A) |
| 46 | scripts/check-step0-live.py:151 | _read_catalog (lines 230-287) | line 359 | `grep -n 'def _read_catalog' scripts/check-step0-emulator.py` → 359 | apparatus | FENCED | Emulator _read_catalog line range |
| 47 | scripts/check-step0-live.py:1784 | unfiltered "35/175" | 41/205 | `grep -cE '^. S-' tests/step0-fixture-catalog.md` → 41; × `--repeat 5` = 205 | apparatus | FENCED | Step 0 fixture-catalog row counts (total / S-A) |
| 48 | scripts/check-step0-live.py:1841 | the 6 S-A semantic-ambiguity rows | 12 | `grep -cE '^. S-A[0-9]' tests/step0-fixture-catalog.md` → 12 | apparatus | FENCED | Step 0 fixture-catalog row counts (total / S-A) |
| 49 | scripts/check-traceability.py:1469 | docs/requirements-traceability.md:11 records the D-02 note | line 16 | `grep -n 'v8.0 audit-validated-reqs note' docs/requirements-traceability.md` → 16 | apparatus | FENCED | requirements-traceability D-02 note line |
| 50 | scripts/check-traceability.py:5832 | sentence shape lifted from docs/README.md:187 | line 196 | `grep -n 'The offline battery moved' docs/README.md` → 196 | apparatus | FENCED | docs/README.md battery-move sentence line |
| 51 | scripts/gen-gate-docs.py:4327 | report-conformance.py:2636-2646's "cannot disagree with each other" | line 2098 | `grep -n 'cannot disagree with each other' scripts/report-conformance.py` → 2098 | apparatus | FENCED | report-conformance "cannot disagree" discipline line |
| 52 | scripts/gen-gate-docs.py:4917 | report-conformance.py:5226-5361 (_CONTROLS/_CONTROL_IDS/self_test) | lines 5925 / 6183 / 6297 | `grep -n '^_CONTROL' scripts/report-conformance.py` → 5925, 6183; `grep -n '^def self_test' scripts/report-conformance.py` → 6297 | apparatus | FENCED | report-conformance self-test house-style line range |
| 53 | scripts/sync-content.py:131 | agent reference tree = 22 files, 12 worked examples | 29 files, 14 worked examples | `find first-principles/agents/references -type f` → 29 paths; `ls shared/examples` → 14 files | apparatus | FENCED | Agent worked-example / reference-tree count |
| 54 | scripts/sync-content.py:1318 | for the 12 worked examples | 14 | `ls shared/examples` → 14 files | apparatus | FENCED | Agent worked-example / reference-tree count |
| 55 | scripts/sync-content.py:1361 | Current target count: 47 total | 48 | `grep -n '^GENERATED_TARGET_COUNT' scripts/sync-content.py` → 48 | apparatus | FENCED | sync-content generated target count |
| 56 | scripts/sync-content.py:1372 | Total: 1 + 11 + 4 + 14 + 13 + 4 = 47 | 48 | same as row 55 | apparatus | FENCED | sync-content generated target count |
| 57 | scripts/sync-content.py:1374 | the total count (47) | 48 | same as row 55 | apparatus | FENCED | sync-content generated target count |
| 58 | scripts/sync-content.py:1376 | 13 SKILLS | 14 | `sed -n '117,122p' scripts/sync-content.py` → SKILLS tuple lists 14 slugs | apparatus | FENCED | sync-content SKILLS count |
| 59 | scripts/check-firewall-battery.sh:196 | report-conformance.py's ~98-control --self-test | 110 | `grep -n 'control_count' docs/gates/PRECOMMIT-conformance-baseline-drift-gate.md` → 110 | apparatus | FENCED | report-conformance self-test control count |

## Totals

**Totals this file:** 59 sites / 32 distinct claims.

## Method account

**Commit check.** `git` commands were denied in this session, so I confirmed the commit by reading the ref files directly. `.git/HEAD` points to `refs/heads/master`, and that file reads `7d7c1d9a75ceecf4d76c840a3952ed34b01e2f77`. I read the live tree. `git status` was also blocked, so I could not confirm the tree was clean. No `python3` script execution was allowed, so I never ran `gen-gate-docs.py` or any other repo script. Every live value came from `grep`, `sed`, `wc`, `find` and `ls`. One read-only `cd` into the repo happened as a side effect of a command; nothing was written.

**Product tier, in protocol order.**
- **Read in full:** `CLAUDE.md` (417 lines), `README.md`, `CONTRIBUTING.md`, and `docs/PROCESS.md`, `ARCHITECTURE.md`, `CONFIGURATION.md`, `DEVELOPMENT.md`, `TESTING.md`, `MEASUREMENT-MAP.md`, `COMPONENT-DIAGRAM.md`, `DATA-FLOW.md`, `ONBOARDING.md`, `GETTING-STARTED.md`, `METHODOLOGY-CHEATSHEET.md`, `FIVE-PHASE-FLOW.md`, `docs/README.md`, `requirements-traceability.md`, `v8.0-final-closure.md`, `testing-agents-headlessly.md`, `live-monitoring-runbook.md` and `conformance-baseline.md`.
- **Gate pages:** I read the non-generated narrative of every `docs/gates/*.md` page; the short, fully generated ones I checked with a digit grep.
- **`CHANGELOG.md`:** I read the preamble and lines 1–200 plus the heading and tag tables. I treated dated release entries as frozen.
- **Other dated `docs/` records:** For the v8.x records, the audit, whole-system and `v9.1-claim-containment-diagnosis.md`, I read the status banners and grep-triaged the bodies. All are declared frozen or dated.
- **`shared/` and `first-principles/`:** I read `first-principles/README.md` in full and grep-triaged the rest for repo-state counts. I excluded the worked examples under exclusion 6.

**Apparatus tier.**
- **Scripts:** All 30 `scripts/*.py` files (about 75k lines) were too large to read line by line. I ran targeted greps over comments and docstrings for number-plus-count-noun patterns and for line-number citations, then read the context of each candidate.
- **Shell files:** I read the whole comment header of `check-firewall-battery.sh`, plus `install-hooks.sh`, `run-live-monitoring.sh` and the comment grep of `git-hooks/pre-commit`.
- **`.github`:** I read the comments in `validation.yml`; its version comment matches `uv.lock` and `.python-version`.
- **`.planning`:** It is gitignored, so I limited it to the 136 paths present in `.git/index`: plan summaries, `21-CONF13-BASELINE.md` and `deferred-items.md`. I opened only `27-08-SUMMARY.md` and `deferred-items.md`. I treated the unread tracked summaries as frozen dated plan records without opening them, and recorded no `.planning` hits.

**Judgement calls.**
- A version string counts as quantity-shaped, because exclusion 4 only covers the stamps themselves.
- A line-number citation counts as an ordinal over live state. The exceptions are `verbatim-move-from` records, citations of retired files, explicitly dated or plan-narrated notes, and self-declared approximations such as the `_battery_core.py` ±1 block.
- Dated standing banners (adjudicated 2026-08-16) and the `docs/README.md` adjudication table are frozen. The exception is `v8.0-final-closure.md`, whose own 2026-08-29 addendum says its current-headline statements are kept current.
- Past-tense plan narration is frozen, for example `QUAL-01.md` line 73's "6 call sites" (live: 7). So are ledger-size snapshots attributed to a plan.
- I excluded `echo` strings in `.sh` files as code rather than comments.
- I dropped claims I could not re-derive with a command. One example is `check-firewall-battery.sh:540`'s "eight not-found arms".
- The sync-generated `first-principles/` copy is recorded as its own site, because it is not a `gen-gate-docs` region.

**Disclosure.** `docs/conformance-baseline.md`, which I read mid-sweep, lists the earlier pre-arm prose readers' sites. By then I had already found most of my product-tier hits: `CLAUDE.md` lines 68, 332, 334 and 383, `README.md:143`, `CONFIGURATION.md` lines 18 and 148, `DEVELOPMENT.md`, `MEASUREMENT-MAP.md`, `ONBOARDING.md`, `TESTING.md`, `CONF-GATE.md`, and `check-step0-live.py` lines 1784 and 1841. After that I kept making my own calls. I did not record their `README.md:145`, `docs/README.md:110` or `.planning` sites, and I added sites absent from their list, such as `sync-content.py` lines 1318, 1361, 1372, 1374 and 1376, `_gate_registry.py`, and `assumption-taxonomy.md`. A verifier should still weigh that exposure.
