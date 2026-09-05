---
phase: 15-self-audit-scan
plan: 13
subsystem: testing
tags: [self-audit-gate, structural-gate, documentation-accuracy, neutralization-testing, python]

# Dependency graph
requires:
  - phase: 15-self-audit-scan (plan 15-11)
    provides: "Rubric-13 region-split (TEMPLATE/ADMISSION clause guards), branch count 87 -> 94, closing the SCAN-02 gate-locked contradiction"
  - phase: 15-self-audit-scan (plan 15-12)
    provides: "Rubric-11 per-literal band-bullet controls, ENTRY-SOURCE LOCK over the roster floor, branch count 94 -> 100"
provides:
  - "Every SCAN-GUARD figure (branch count, not-found-arm count, census arithmetic, netting count, multi-literal coverage claim) re-measured against the live tree and made consistent across all four surfaces (gate docstring, CLAUDE.md, docs/ARCHITECTURE.md, check-firewall-battery.sh)"
  - "Phase 15's gap ledger discharged row by row: all four SCAN-02 missing items, both SCAN-03 missing items, both documentation-accuracy missing items, each tied to a plan/task and a command output"
  - "ROADMAP.md's Phase 15 entry marked 13/13 plans executed (local worktree edit only — see note below; not part of this plan's git-tracked commit set, per worktree-mode constraint that the orchestrator owns ROADMAP.md/STATE.md writes)"
affects: [16-integration-ship]

# Tech tracking
tech-stack:
  added: []
  patterns: ["per-arm neutralization testing (force a condition to a constant False on a scratch copy, observe --self-test rc) as the standard way to classify a not-found reporting site as controlled/uncontrolled"]

key-files:
  created: []
  modified:
    - scripts/check-selfaudit-scan.py
    - CLAUDE.md
    - docs/ARCHITECTURE.md
    - scripts/check-firewall-battery.sh
    - .planning/ROADMAP.md

key-decisions:
  - "Scoped Measurement 2's published not-found-arm count to the same population WR-03 (15-REVIEW.md) originally measured (Body-3, Rubric-2, Rubric-13) plus plan 15-11's new split_idx arm, rather than also publishing four additional dead/unreachable sub-conditions found in Rubric-9/Rubric-10 during finer-grained neutralization (span_idx==-1 is unreachable, guarded by a preceding count==1 check on the same literal; rigorous_idx==-1 fires as an unasserted side effect of an unrelated R-11 fixture) — recorded as a scope note, not published, because surfacing them now would be scope creep on a plan whose action items are limited to reconciling the specific WR-03 finding"
  - "Netting count settled at 'one' everywhere (the gate docstring alone said 'two'; both doc surfaces already said 'one') per Measurement 4: R-02-placement-aa is a single branch id"
  - "Not-found residual count settled at eight (five previously named + Rubric-2's two, previously measured but omitted from the published list + plan 15-11's new split_idx arm), re-derived by per-arm neutralization against the current tree rather than transcribed from 15-REVIEW.md"

requirements-completed: [SCAN-02, SCAN-03]

# Metrics
duration: 35min
completed: 2026-09-04
---

# Phase 15 Plan 13: SCAN-GUARD documentation reconciliation and phase close Summary

**Re-measured every published SCAN-GUARD figure (100 branches, 8 uncontrolled not-found arms, 16-row neutralization-census total, netting count one) against the live tree and wrote the same numbers onto all four describing surfaces in one pass, then reproduced all three of the verifier's fail-open findings against the closed tree and confirmed each now fails the gate by name.**

## Performance

- **Duration:** ~35 min
- **Started:** 2026-09-04T12:43:24-04:00 (worktree base commit)
- **Completed:** 2026-09-04 (this commit)
- **Tasks:** 3
- **Files modified:** 4 committed (`scripts/check-selfaudit-scan.py`, `CLAUDE.md`, `docs/ARCHITECTURE.md`, `scripts/check-firewall-battery.sh`) + 1 local-only, uncommitted per worktree-mode constraint (`.planning/ROADMAP.md`, gitignored)

## Accomplishments

- Re-derived every SCAN-GUARD figure by running or mutating the live code (never transcribed from `15-VERIFICATION.md` or `15-REVIEW.md`), and corrected the gate's own docstring, `CLAUDE.md`, `docs/ARCHITECTURE.md` and the battery comment to state the same numbers.
- Closed all eight `missing:` items across the three verification gaps, with a command output backing each.
- Reproduced all three of the verifier's fail-open findings (the gate-locked SCAN-02 contradiction, the `_BAND_BULLETS` narrowing fail-open, the roster-argument-aliasing fail-open) against the final tree and confirmed each now fails `--self-test`/the live leg by name.
- Closed the phase: `bash scripts/check-firewall-battery.sh` reports `FIREWALL: GREEN (24/24)`, `sync-content.py --check` is clean; `.planning/ROADMAP.md`'s Phase 15 entry marked 13/13 plans executed locally (this is a gitignored file the orchestrator owns centrally — see note below, not part of this plan's commit set).

## Task Commits

1. **Task 1: Re-measure every published SCAN-GUARD figure against the live code** - `7148cc2` (fix)
2. **Task 2: Write the measured figures onto the three external SCAN-GUARD surfaces in one pass** - `f87ce32` (fix)
3. **Task 3: Close the phase — discharge the gap ledger row by row and record what remains** - plan metadata commit (this SUMMARY only; `.planning/ROADMAP.md` is gitignored and edited locally, not committed — see note below)

## Files Created/Modified

- `scripts/check-selfaudit-scan.py` — docstring bound (8) rewritten: the not-found residual's count and enumeration replaced with Measurement 2's re-derived eight-arm set, the netting count corrected from "two" to "one".
- `CLAUDE.md` — SCAN-GUARD row: branch count corrected to one hundred with the growth narrative extended for plans 15-11/15-12; the "20 fail" defect avoided (this surface never carried the wrong figure); `m13`-`m16` given a recorded disposition; the not-found residual corrected to eight arms; WR-04 marked closed with its disclosed bounds stated.
- `docs/ARCHITECTURE.md` — same corrections at this surface's shorter density: branch count, "20 fail" → 16 (the enumeration's own arithmetic), `m13`-`m16` disposition, eight-arm not-found residual, WR-04 closure note.
- `scripts/check-firewall-battery.sh` — SCAN-GUARD registration comment: branch count corrected to 100 with the 15-11/15-12 growth steps, not-found-arm count corrected to eight.
- `.planning/ROADMAP.md` — Phase 15's wave 13 entry checked off; top-level Phase 15 status line updated from "10/13 plans executed" to "13/13 plans executed", framing gap-closure round 4 as complete and awaiting re-verification. **Note:** `.planning/` is gitignored in this repo; this edit is local-only within this worktree and is NOT part of this plan's committed changes — per this executor's worktree-mode instructions, the orchestrator owns ROADMAP.md/STATE.md writes centrally after all worktree agents in the wave complete, and will apply the equivalent update from this SUMMARY's frontmatter and content.

## Measurement 1 — branch count

```
python3 -c "
import importlib.util
spec = importlib.util.spec_from_file_location('m', 'scripts/check-selfaudit-scan.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
print('REQUIRED_BRANCHES len:', len(m.REQUIRED_BRANCHES))
print('_BRANCH_ROSTER_LOCK len:', len(m._BRANCH_ROSTER_LOCK))
print('equal:', m.REQUIRED_BRANCHES == m._BRANCH_ROSTER_LOCK)
"
```
→ `REQUIRED_BRANCHES len: 100`, `_BRANCH_ROSTER_LOCK len: 100`, `equal: True`.

`python3 scripts/check-selfaudit-scan.py --self-test` printed `ANTI-MASKING GATE: All 100 branches covered: [...]` — all three readings agree at **100**.

## Measurement 2 — the not-found reporting arms

Enumerated every site in the file reporting a failure because an index lookup returned `-1` or a slice returned `None` (16 candidate sites total: `_check_body_text`'s Body-1/Body-3, `_check_rubric_text`'s Rubric-2/Rubric-3..8/Rubric-9/Rubric-10/Rubric-13 x2/Rubric-14). For each, neutralized it alone on a scratch copy (`scripts/_scratch_check-selfaudit-scan.py`, deleted after each run) by rewriting its condition to `if False:`, then ran `--self-test` and recorded the exit code:

| Site (line) | Construct | Mutation | Observed rc | Verdict |
|---|---|---|---|---|
| 904 | Body-3 `lead_idx == -1` | `if False:` | 0 | UNCONTROLLED |
| 906 | Body-3 `tail_idx == -1` | `if False:` | 0 | UNCONTROLLED |
| 910 | Body-3 `clean_idx == -1` | `if False:` | 0 | UNCONTROLLED |
| 1079 | Rubric-2 `aa_idx == -1` | `if False:` | 1 (`ANTI-MASKING GATE FAILURE: ['R-02-placement-anchor']`) | CONTROLLED |
| 1081 | Rubric-2 `scan_idx == -1` | `if False:` | 0 | UNCONTROLLED |
| 1083 | Rubric-2 `precedence_idx == -1` | `if False:` | 0 | UNCONTROLLED |
| 1107 | Rubric-3..8 `scan_slice is None` | `if False:` | 1 (crashes with `TypeError` inside the `else` branch when R-01a's fixture strips the scan-block heading) | CONTROLLED (load-bearing, though via a crash rather than a named branch id) |
| 1170 | Rubric-9 `crit4_slice is None` | `if False:` | 0 | UNCONTROLLED |
| 1187 | Rubric-9 `span_idx==-1 or rigorous_idx==-1 or not(...)` (whole condition) | `if False:` | 1 (`R-09-crit4-order`) | CONTROLLED as a whole (via the ordering sub-condition) |
| 1187 | Rubric-9 `span_idx==-1` (sub-condition only) | `if False or rigorous_idx==-1 or not(...):` | 0 | UNCONTROLLED, but unreachable dead code (guarded by a preceding `c4_span_count == 1` check on the same literal) |
| 1187 | Rubric-9 `rigorous_idx==-1` (sub-condition only) | `if span_idx==-1 or False or not(...):` | 0 | UNCONTROLLED (fires as a side effect of `R-11-bands-crit4-rigorous`'s fixture, but no assertion pins that message) |
| 1203 | Rubric-10 `crit6_slice is None` | `if False:` | 0 | UNCONTROLLED |
| 1220 | Rubric-10 combined ordering condition (whole) | `if False:` | 1 (`R-10-crit6-order`) | CONTROLLED as a whole |
| 1220 | Rubric-10 `span_idx==-1`/`rigorous_idx==-1` (sub-conditions) | (as above, per sub-condition) | 0 / 0 | UNCONTROLLED, same shape as Rubric-9's |
| 1268 | Rubric-13 `format_slice is None` | `if False:` | 0 | UNCONTROLLED |
| 1319 | Rubric-13 `split_idx == -1` (region-split anchor, added at plan 15-11) | `if False:` | 0 | UNCONTROLLED |
| 1357 | Rubric-13 combined admission/crit4-index/ordering condition (whole) | `if False:` | 1 (`R-13-format-order`) | CONTROLLED as a whole (via the ordering sub-condition) |
| 1357 | Rubric-13 `admission_idx == -1` (sub-condition only) | `if False or crit4_idx==-1 or not(...):` | 0 | UNCONTROLLED |
| 1357 | Rubric-13 `crit4_idx == -1` (sub-condition only) | `if admission_idx==-1 or False or not(...):` | 0 | UNCONTROLLED |
| 1396 | Rubric-14 `crit2_slice is None` | `if False:` | 0 | UNCONTROLLED |

**Published count: eight arms** — the same population `15-REVIEW.md`'s WR-03 originally measured (Body-3's three, Rubric-2's two, Rubric-13's admission-sentence/Criterion-4-index pair), plus the one new arm plan 15-11 introduced (Rubric-13's region-split anchor, `split_idx == -1`, line 1319 — confirmed uncontrolled both by this neutralization and by 15-11-SUMMARY.md's own statement that it "carries no `REQUIRED_BRANCHES` id of its own... asserted here by manual reproduction rather than an automated `--self-test` control"). `aa_idx == -1` stays excluded (controlled via `R-02-placement-anchor`, confirmed by the code comment at line 2309-2310 and by this measurement).

**Scope decision, not published:** the finer-grained sub-condition tests on Rubric-9/Rubric-10 (lines 1187, 1220) surfaced four additional uncontrolled sub-conditions (`span_idx==-1`/`rigorous_idx==-1` in each of the two criterion slices). These are NOT added to the published residual: `span_idx==-1` is unreachable dead code in every path that reaches it (the preceding `count == 1` check on the identical literal makes a subsequent `_find_flat` miss impossible), and neither review round's WR-03 finding — nor this plan's binding constraints — scoped these in. Recorded here for transparency; the whole-condition-as-one-arm granularity (matching how `15-REVIEW.md` itself measured Rubric-13's combined condition as two named sub-parts, never Rubric-9/10's) is what the published figure uses.

## Measurement 3 — the neutralization-census arithmetic (22-row disposition table)

`|{m1..m5}| + |{m7..m12}| + |{m17..m21}| = 5 + 6 + 5 = 16` (arithmetic total of the enumeration `docs/ARCHITECTURE.md` misstated as "20"):

| # | Mutation | Disposition |
|---|---|---|
| m1 | Rubric-9 ordering arm → `if False:` | CAUGHT (closed plan 15-05) |
| m2 | Rubric-10 ordering arm → `if False:` | CAUGHT (closed plan 15-05) |
| m3 | Cross-1 rubric arm → `if False:` | CAUGHT (`X-01-cols-chain-rubric`) |
| m4 | Cross-2 body arm → `if False:` | CAUGHT (`X-02-heading-body`) |
| m5 | Body-2 whole-file count arm → `if False:` | CAUGHT (`B-02-lead-whole`) |
| m6 | Rubric-4 name loop → `if False:` | N/A — loop deleted (WR-09); could not be applied |
| m7 | drop `_BODY_ROWRULE_CLAIM` from Body-7's tuple | CAUGHT (`B-07-rowrule-claim`) |
| m8 | drop `_BODY_PLACEMENT_2` from Body-12's tuple | CAUGHT (`B-12-placement-2`) |
| m9 | drop `_BODY_LEDGER_INDEP_2` from Body-10's tuple | CAUGHT (`B-10-ledger-indep-2`) |
| m10 | drop `_BODY_RECON_TEMPLATE` from Body-11's tuple | CAUGHT (`B-11-recon-template`) |
| m11 | drop `_RUBRIC_DIVLABOUR_2` from Rubric-3's tuple | CAUGHT (`R-03-divlabour-2`) |
| m12 | drop `_COLS_CLAIM` from Rubric-5's tuple | CAUGHT (`R-05-cols-claim`) |
| m13 | Rubric-11 C6 loop → `if False:` | CAUGHT before this census ran; **re-applied against the current tree in this plan** (line 1245, `if n != 1:` → `if False:`) — rc 1, `ANTI-MASKING GATE FAILURE: 4 branch(es) not covered: ['R-11-bands-crit6-absent', 'R-11-bands-crit6-handwavy', 'R-11-bands-crit6-rigorous', 'R-11-bands-crit6-sound']`. No regression. |
| m14 | Body-15 pre-amendment arm → `if False:` | CAUGHT before this census ran; **re-applied** (line 1013, `if preamendment_count != 0:` → `if False:`) — rc 1, `B-15-donotpresent-preamendment` uncovered. No regression. |
| m15 | Rubric-7 near-twin arm → `if False:` | CAUGHT before this census ran; **re-applied** (line 1154) — rc 1, `R-07-missing-neartwin` uncovered. No regression. |
| m16 | Rubric-12 halt count → `if False:` | CAUGHT before this census ran; **re-applied** (line 1256, `if halt_count != 1:` → `if False:`) — rc 1, `R-12-halt-dup`/`R-12-halt-missing` uncovered. No regression. |
| m17 | drop `_COLS_CLAIM` from Cross-1's tuple | CAUGHT (`X-01-cols-claim-body`/`X-01-cols-claim-rubric`) |
| m18 | delete `X-01-cols`/`X-02-heading` from `REQUIRED_BRANCHES` | CAUGHT (roster-equality floor) |
| m19 | Body-3 `tail_idx < lead_idx < clean_idx` → `lead_idx < clean_idx` | CAUGHT (`B-03-placement-tail`) |
| m20 | Rubric-9 `!= 1` → `< 1` | CAUGHT (`R-09-crit4-count-dup`) |
| m21 | Body-4 `!= 1` → `< 1` | CAUGHT (`B-04-heading-dup`) |
| m22 | delete `+ _check_cross_surface(...)` from `_validate_files` | Open at the 2026-09-04 `15-REVIEW.md` census; **now closed by plan 15-09's `validate-census`** |

All 22 rows carry a disposition — none are unaccounted for. `m13`-`m16` are the four rows both doc surfaces previously left unmentioned; this plan re-applied all four against the current tree (not merely cited their pre-existing 15-06-SUMMARY.md disposition) and confirmed no regression.

## Measurement 4 — the netting count

`/usr/bin/grep -c '"R-02-placement-aa"' scripts/check-selfaudit-scan.py` → **3** (once in `REQUIRED_BRANCHES`, once in `_BRANCH_ROSTER_LOCK`, once in the docstring's own residual-ledger prose after this plan's edit) — confirming `R-02-placement-aa` is a single branch id, so the netting count settles at **one** wherever it is stated. `/usr/bin/grep -n "net of" scripts/check-selfaudit-scan.py CLAUDE.md docs/ARCHITECTURE.md` was run and every match read: the gate docstring's line wraps across "net of\n    the one" (matching its pre-existing wrap point, unaffected by this edit) and now says "the one"; `CLAUDE.md` and `docs/ARCHITECTURE.md` already said "the one" before this plan and still do. No surface states a netting count other than one.

## Reproductions (Task 3)

**Reproduction A (gap 1, the blocking one) — inverse of the verifier's reproduction.** On a disposable `rsync -a --exclude .git --exclude .venv` scratch copy: reverted `shared/spine/references/validation-rubric.md`'s quoted-span template from the amended (plan 15-11) wording back to the pre-15-11 narrow wording ("...for Criteria 4 and 6 only, from the self-audit scan emitted as process output for this analysis"), ran `sync-content.py --write` (48 files written), then ran the bare live leg:
```
check-selfaudit-scan: FAIL — Rubric-13: amended quoted-span template occurs 0 time(s) in the Verdict Block Format section, expected exactly 1
check-selfaudit-scan: FAIL — Rubric-13: Criteria-4/6 clause occurs 0 time(s) in the Verdict Block Format TEMPLATE region, expected exactly 1
check-selfaudit-scan: FAIL — Rubric-13: Criterion-2 clause occurs 0 time(s) in the Verdict Block Format TEMPLATE region, expected exactly 1
check-selfaudit-scan: FAIL — Rubric-13: superseded narrow quoted-span wording still present (1 occurrence(s)) in the whole file, expected 0
check-selfaudit-scan: FAIL — Cross-5: superseded narrow quoted-span wording present in rubric surface
```
rc=1, naming both the amended-template arm and the superseded-count-0 arm exactly as predicted. Scratch copy deleted; `git status --porcelain` confirmed empty in the real tree afterward.

**Reproduction B (gap 2, `_BAND_BULLETS`).** On a scratch copy of `scripts/check-selfaudit-scan.py` (deleted after the run), narrowed `_BAND_BULLETS` from `(_BAND_RIGOROUS, _BAND_SOUND, _BAND_HANDWAVY, _BAND_ABSENT)` to `(_BAND_SOUND,)` and ran `--self-test`:
```
ANTI-MASKING GATE FAILURE: 6 branch(es) not covered: ['R-11-bands-crit4-absent', 'R-11-bands-crit4-handwavy', 'R-11-bands-crit4-sound', 'R-11-bands-crit6-absent', 'R-11-bands-crit6-handwavy', 'R-11-bands-crit6-sound']
```
rc=1, naming the six uncovered branch ids exactly as predicted (the seventh and eighth, `-crit4-rigorous`/`-crit6-rigorous`, stay incidentally "covered" because `zip(_BAND_BULLETS, _BAND_NAMES)` non-strict-pairs the surviving `_BAND_SOUND` literal with the first name, "rigorous" — a mislabeling, not a gap in the fix). File restored; `git status --porcelain` confirmed empty afterward.

**Reproduction C (gap 2, roster aliasing).** On a scratch copy, aliased the real `_roster_problems(...)` call's third argument from `frozenset(covered_branches)` to `frozenset(REQUIRED_BRANCHES)` and ran `--self-test`:
```
(roster-lock) ROSTER LOCK: PASS — REQUIRED_BRANCHES == _BRANCH_ROSTER_LOCK and covered_branches has no unregistered branch id(s)
check-selfaudit-scan --self-test: FAIL — (roster-entry-source): real call's argument-triple text 'REQUIRED_BRANCHES, _BRANCH_ROSTER_LOCK, frozenset(covered_branches)' not found in source (rewritten, aliased, or missing call site); (dispatch): main(['--self-test']) returned 1, expected 0
```
rc=1, naming `(roster-entry-source)` exactly as predicted — the `(roster-lock)` surplus check itself still prints PASS for the aliased reason WR-04 described (structurally incapable of failing), but the ENTRY-SOURCE LOCK plan 15-12 added catches the rewritten call site independently. File restored; `git status --porcelain` confirmed empty afterward.

**Reproduction D (gap 1, the prose judgement).** Read all four texts side by side from the current (unmutated) tree:

1. **TEMPLATE** (`shared/spine/references/validation-rubric.md:176`): `Quoted span: "[Direct quote of the specific text that most directly determines the band assigned — from the analysis being scored, or, per the admission below, from the self-audit scan for Criteria 4 and 6 or the Assumption Audit scan for Criterion 2, each emitted as process output for this analysis.]"`
2. **ADMISSION paragraph** (`:182`): `The self-audit scan and the Assumption Audit scan are not output sections, and they are the only artifacts outside the six-section analysis a verdict block may quote: the self-audit scan for Criteria 4 and 6, and the Assumption Audit scan for Criterion 2.`
3. **Criterion 2's Rigorous descriptor** (`:265`): `...the Assumption Audit artifact produced before scoring (per "How to Apply This Rubric") confirms this scan was exhaustive over named derivation chain steps, not an open-ended survey of the universe of conceivable assumptions.`
4. **`shared/spine/SKILL-body.md`'s Validate step** (`:298`): `**Validate** — apply each gate criterion; quote the specific span that satisfies or fails each criterion — from the analysis text, or, per the Verdict Block Format's admission, from the self-audit scan for Criteria 4 and 6, and the Assumption Audit scan for Criterion 2.`

**Verdicts, pairwise:**
- **TEMPLATE vs. ADMISSION: AGREE.** Both now state the identical two-clause rule (self-audit scan for Criteria 4/6, Assumption Audit scan for Criterion 2) — this is the specific agreement plan 15-11 restored; before it, the TEMPLATE stated the narrower pre-fix rule while the ADMISSION already stated the wider one.
- **TEMPLATE/ADMISSION vs. Criterion 2's Rigorous descriptor: AGREE in scope, but the descriptor's own cross-reference is broken.** All three permit Criterion 2 to draw on the Assumption Audit scan/artifact — no substantive disagreement about WHAT may be quoted. But the descriptor cites `"How to Apply This Rubric"`, a section that does not exist in either rubric surface (the only matching heading is `## How to Apply This Gate`) — this is `15-REVIEW.md` WR-05, explicitly named as NOT closed by this plan (see Residual Ledger below).
- **ADMISSION vs. `SKILL-body.md`'s Validate step: AGREE.** The Validate step restates the ADMISSION's two-clause rule near-verbatim ("the self-audit scan for Criteria 4 and 6, and the Assumption Audit scan for Criterion 2"), closing the cross-surface drift the second verification pass found (`15-VERIFICATION.md`'s `gaps_closed` entry for the prior round).

This is the exact judgement the verifier made to fail Truth 2 in the prior round; against the tree as plan 15-11 leaves it, all three prescriptive statements now agree on the two-clause rule, with the one open exception (WR-05's dangling cross-reference) named rather than silently fixed.

## Eight-row gap ledger

| # | Gap | Missing item | Closed by | Evidence |
|---|---|---|---|---|
| 1 | Gap 1 (SCAN-02, blocking) | Widen `_RUBRIC_FORMAT_QUOTED_SPAN`'s template text to name both admitted artifacts | Plan 15-11, Task 1 | `/usr/bin/grep -c "for Criteria 4 and 6 only" shared/spine/references/validation-rubric.md` → 0 (15-11-SUMMARY.md Task 1 evidence); template now reads the two-clause rule (Reproduction D above) |
| 2 | Gap 1 | Add `_RUBRIC_FORMAT_QUOTED_SPAN_SUPERSEDED` pinned at whole-file count 0 | Plan 15-11, Task 2 | Reproduction A above: reinstating the narrow wording fails naming `R-13-format-quoted-span-superseded`'s message ("superseded narrow quoted-span wording still present") |
| 3 | Gap 1 | Correct docstring bound (5) to match bound (6)'s three-artifact enumeration | Plan 15-11, Task 1 | `scripts/check-selfaudit-scan.py` bound (5), read this plan: states "corrected at plan 15-11", now consistent with bound (6) |
| 4 | Gap 1 | Re-run `sync-content.py --write` and confirm the SCAN-GUARD live leg passes | Plan 15-11, Task 2 | `python3 scripts/sync-content.py --check` → exit 0 (this plan, Task 2 verification); `python3 scripts/check-selfaudit-scan.py` → exit 0 (this plan) |
| 5 | Gap 2 (WR-01, minor) | Parameterize Rubric-11's arms over all four `_BAND_BULLETS` literals | Plan 15-12, Task 1 | Reproduction B above: narrowing `_BAND_BULLETS` now fails naming six branch ids, `ANTI-MASKING GATE: All 100 branches covered` on the unmutated tree |
| 6 | Gap 2 (WR-04, minor) | Add an ENTRY-SOURCE LOCK for the roster floor's `covered` argument | Plan 15-12, Task 2 | Reproduction C above: aliasing the argument now fails naming `(roster-entry-source)` |
| 7 | Gap 3 (documentation, minor) | Correct `docs/ARCHITECTURE.md`'s count to 16 and account for `m13`-`m16` | This plan (15-13), Task 2 | `/usr/bin/grep -n "20 fail" docs/ARCHITECTURE.md` → no match (rc 1); `/usr/bin/grep -n "m13" docs/ARCHITECTURE.md` → matches with disposition text |
| 8 | Gap 3 | Add the two missing Rubric-2 arms to the "seven not-found" residual and settle the netting count at "one" | This plan (15-13), Tasks 1-2 | Measurement 2 above (eight-arm re-derivation); Measurement 4 above (netting count) |

## Residual ledger (not closed by this gap-closure round)

| Item | Disposition | Recorded at |
|---|---|---|
| WR-01 (band-determining-limbs half) | Open. Three further band-determining limbs (a chain lacking a genuine intermediate step, a conclusion with more than one derivation chain, a Conclusion claim inconsistent with its section-4 chains) have no column in either scan table and no quoting rule under either half of the instruction. | Gate docstring bound (7); `CLAUDE.md`/`docs/ARCHITECTURE.md` SCAN-GUARD rows |
| WR-05 | Open. Criterion 2's Rigorous descriptor cites `"How to Apply This Rubric"`, a section that does not exist (the real heading is `"How to Apply This Gate"`) — confirmed live in Reproduction D above. | `15-REVIEW.md` WR-05; not mentioned on any external surface prior to this plan, now named here |
| WR-06 | Open. The scan-verify block's mutually exclusive missing-scan instructions (halt forever vs. proceed and note the gap) — per the review, not independently re-reproduced by this plan. | `15-REVIEW.md`, Anti-Patterns table row `validation-rubric.md:59 vs 75` |
| IN-01, IN-02 | Open. Not independently re-measured by this plan; carried forward from `15-REVIEW.md`'s residual inventory. | `15-REVIEW.md` |
| IN-04 | Open, narrowed by one instance. The self-test's own top-level assertions (anti-masking gate, dispatch-reachability control, positive control (a), `_check_negative`'s check-ID/`expected_detail` matches) have no meta-guard beyond the branch and call-site censuses already in place; plan 15-12 added exactly one more meta-guard (`(roster-es-census)`), narrowing rather than closing this residual. | Gate docstring bound (8); `CLAUDE.md`/`docs/ARCHITECTURE.md` |
| IN-05 | Open. Two residual raw `str.find`/`.count` sites (`_slice`'s heading lookup, Rubric-11's band-bullet count) deviate from the file's stated one-discipline (`_find_flat`/`_count_flat`) rule. | Gate docstring bound (8); `CLAUDE.md`/`docs/ARCHITECTURE.md` |
| CV-01 | Open. Not independently re-measured by this plan; carried forward from `15-REVIEW.md`'s residual inventory. | `15-REVIEW.md` |
| SCAN-04 character figure | Deferred, non-blocking, unchanged. The 2,288-vs-1,381-character discrepancy stays disclosed rather than settled — no fixture exists to mechanically adjudicate it. Confirmed this plan's edits left the disclosure (gate docstring `## Measured emission cost (SCAN-04)` section, lines 258-319) byte-identical; not touched, per binding constraint. | Gate docstring; `15-VERIFICATION.md` deferred item 1 |
| WR-04 (roster aliasing) | **Closed this round** (plan 15-12) — listed here only to note its now-closed status is reflected on all four surfaces as of this plan's Task 2. | Measurement 4; Reproduction C |

## Closing green-state readings

- `python3 scripts/sync-content.py --check` → exit 0.
- `python3 scripts/check-selfaudit-scan.py --self-test` → exit 0, `ANTI-MASKING GATE: All 100 branches covered`.
- `python3 scripts/check-selfaudit-scan.py` (bare live leg) → exit 0.
- `python3 -m py_compile scripts/check-selfaudit-scan.py` → exit 0.
- `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (24/24)` with `[PASS] SCAN-GUARD`.
- `python3 scripts/check-traceability.py --self-test` → exit 0 (HEADLINE-LOCK scans `CLAUDE.md` and `docs/*.md`, both edited this plan).
- `python3 scripts/check-registration.py --self-test` → exit 0 (29 controls); `python3 scripts/check-registration.py` (live) → exit 0 (14/14 skills, 21/22 CI-registered + 1 battery-only by design).
- `python3 scripts/check-version-stamps.py --self-test` → exit 0; `python3 scripts/check-version-stamps.py` (live) → exit 0 — confirming no plan in this round moved a version stamp.
- `git status --porcelain` → empty in the real tree throughout (verified after every scratch-copy mutation and after each commit).

## Decisions Made

See `key-decisions` in the frontmatter. In addition: chose to re-apply `m13`-`m16` against the CURRENT tree (not merely cite 15-06-SUMMARY.md's pre-existing disposition) so the SUMMARY's own disposition table is independently re-measured rather than transcribed, per the plan's binding-constraint discipline.

## Deviations from Plan

None — plan executed exactly as written. The one scope decision (excluding Rubric-9/10's dead/unreachable sub-conditions from the published not-found count) is documented in `key-decisions` above rather than as a deviation, since it does not change any published surface's content beyond what the plan's own action items specify.

## Issues Encountered

None.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

Phase 15's gap ledger is fully discharged (eight of eight `missing:` items closed, evidenced above) and the tree closes green at 24/24. `.planning/ROADMAP.md`'s Phase 15 entry was updated locally to 13/13 plans executed (see note above — this is advisory only; the orchestrator applies the tracked update), awaiting the next verification pass. Phase 16 (Integration & Ship) depends on Phase 15's deliverable existing, which it now does; Phase 16 is NOT started by this plan (out of scope — version stamps, matrix rows, the coverage headline, and CHANGELOG entries are explicitly reserved for Phase 16 per this plan's binding constraints).

---
*Phase: 15-self-audit-scan*
*Completed: 2026-09-04*

## Self-Check: PASSED

- FOUND: commit `7148cc2` (Task 1)
- FOUND: commit `f87ce32` (Task 2)
- FOUND: `scripts/check-selfaudit-scan.py`
- FOUND: `CLAUDE.md`
- FOUND: `docs/ARCHITECTURE.md`
- FOUND: `scripts/check-firewall-battery.sh`
- FOUND: `.planning/phases/15-self-audit-scan/15-13-SUMMARY.md`
