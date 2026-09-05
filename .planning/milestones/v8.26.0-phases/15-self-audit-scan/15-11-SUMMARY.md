---
phase: 15-self-audit-scan
plan: 11
subsystem: testing
tags: [rubric, verdict-block-format, scan-guard, quality-harness, region-split]

# Dependency graph
requires:
  - phase: 15-self-audit-scan
    provides: "plan 15-08's widened admission paragraph and Rubric-13/14 clause guards; 15-VERIFICATION.md gap 1 (SCAN-02) and 15-REVIEW.md context this plan closes"
provides:
  - "Verdict Block Format quoted-span template widened to name both admitted artifacts, byte-agreeing with the admission paragraph it governs"
  - "Region-split Rubric-13 clause guards (TEMPLATE region vs ADMISSION region), each independently falsifiable, closing the fix-one-statement-not-the-other failure mode that shipped twice"
  - "_RUBRIC_FORMAT_QUOTED_SPAN_SUPERSEDED count-0 pin plus Cross-5 per-surface arm, preventing silent reinstatement of the narrow wording on either prescriptive surface"
  - "Corrected SCAN-GUARD docstring bound (5)/(6)/(10), one scope stated rather than two contradictory ones"
affects: [16-ship-hardening]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Region-scoped mechanical-agreement guard: split a slice at a stable lead anchor (not the full literal being asserted) so a mutation to the asserted clause cannot also break the split point that locates it"

key-files:
  created: []
  modified:
    - shared/spine/references/validation-rubric.md
    - first-principles/agents/references/validation-rubric.md
    - scripts/check-selfaudit-scan.py

key-decisions:
  - "Split the TEMPLATE/ADMISSION boundary using a new _RUBRIC_FORMAT_ADMISSION_LEAD anchor (the admission sentence's prefix up to its colon) instead of the plan's originally suggested full _RUBRIC_FORMAT_ADMISSION literal, because the full-sentence literal is corrupted by any mutation that drops or duplicates a clause from within it — which made split_idx resolve to -1 and masked the specific admission-region arm behind a generic not-found failure"
  - "Ran `uv sync` to resolve VAL-03's pytest prerequisite before the firewall battery — a locked project dev-dependency declared in the repo's own pyproject.toml/uv.lock and documented in CLAUDE.md as the remedy, not an ad hoc package install"

requirements-completed: [SCAN-02]

# Metrics
duration: 45min
completed: 2026-09-04
---

# Phase 15 Plan 11: Verdict Block Format template/admission agreement Summary

**Widened the Verdict Block Format's quoted-span template to name both admitted artifacts in the admission paragraph's own words, then region-split `Rubric-13`'s clause guards so the two statements are mechanically asserted to agree, closing the third-round SCAN-02 contradiction between the template and the paragraph two lines below it.**

## Performance

- **Duration:** 45 min
- **Started:** 2026-09-04T15:33:00Z (approx.)
- **Completed:** 2026-09-04T16:18:15Z
- **Tasks:** 3/3 completed
- **Files modified:** 3

## Accomplishments

- The fenced quoted-span TEMPLATE in `shared/spine/references/validation-rubric.md` now reads "...or, per the admission below, from the self-audit scan for Criteria 4 and 6 or the Assumption Audit scan for Criterion 2, each emitted as process output for this analysis" — Criterion 2 is no longer forbidden by its own template from quoting the Assumption Audit artifact its Rigorous descriptor bands on.
- `Rubric-13`'s per-clause count guards are region-split into four independently falsifiable checks (Criteria-4/6 in TEMPLATE, Criterion-2 in TEMPLATE, Criteria-4/6 in ADMISSION, Criterion-2 in ADMISSION), so a clause dropped from one prescriptive statement while the other still states it fails by name — the exact failure mode rounds 1 (plan 15-07) and 2 (plan 15-08) shipped.
- The narrow "for Criteria 4 and 6 only, from the self-audit scan" wording is now a registered superseded literal, pinned at whole-file count 0 in `Rubric-13` plus a new `Cross-5` arm covering the agent body's Validate step, so it cannot be silently reinstated on either prescriptive surface.
- The bare SCAN-GUARD live leg (`python3 scripts/check-selfaudit-scan.py`, no flags) now exits 0 against the corrected emitted tree — this is the exact behaviour `15-VERIFICATION.md` reproduced as FAILED.
- `bash scripts/check-firewall-battery.sh` reports `FIREWALL: GREEN (24/24)`.

## Task Commits

Each task was committed atomically:

1. **Task 1: Census every surface that states the quoting rule, then widen the rubric template and its pinned literal together** - `e232962` (fix)
2. **Task 2: Make Rubric-13's clause guards region-aware and pin the superseded wording on both surfaces, with one controlled branch per new arm** - `80a4803` (fix)
3. **Task 3: Correct docstring bound (5) to the three-artifact enumeration and close green** - `462bddc` (docs)

**Plan metadata:** committed alongside this SUMMARY (worktree mode — orchestrator finalizes on merge)

_Note: this plan carried no TDD tasks._

## Files Created/Modified

- `shared/spine/references/validation-rubric.md` — widened the `Quoted span:` template (line 177) to name both admitted artifacts in the admission's own words
- `first-principles/agents/references/validation-rubric.md` — regenerated twin (line 179), via `sync-content.py --write`
- `scripts/check-selfaudit-scan.py` — widened `_RUBRIC_FORMAT_QUOTED_SPAN`, added `_RUBRIC_FORMAT_QUOTED_SPAN_SUPERSEDED` and `_RUBRIC_FORMAT_ADMISSION_LEAD`, region-split `Rubric-13`'s clause guards, added a `Cross-5` arm, registered 7 new branches (87 → 94), corrected docstring bounds (5)/(6) and added bound (10)

## Step A census (task 1, run before any edit)

`/usr/bin/grep -rn "Criteria 4 and 6" shared/ scripts/ docs/ first-principles/ CLAUDE.md --exclude-dir=__pycache__` returned **19 lines** (matching the plan's planning-time prediction exactly), classified:

| File | Line | Classification | Notes |
|---|---|---|---|
| `shared/spine/references/validation-rubric.md` | 177 | PRESCRIPTIVE — **the defect** | narrow template, widened by this task |
| `shared/spine/references/validation-rubric.md` | 183 | PRESCRIPTIVE (correct, unchanged) | admission paragraph, already widened by plan 15-08 |
| `shared/spine/SKILL-body.md` | 280 | PRESCRIPTIVE (correct, unchanged) | closure-ledger inadmissibility sentence |
| `shared/spine/SKILL-body.md` | 288 | PRESCRIPTIVE (correct, unchanged) | scan-placement sentence |
| `shared/spine/SKILL-body.md` | 298 | PRESCRIPTIVE (correct, unchanged) | Validate step, already two-clause per plan 15-08 |
| `scripts/check-selfaudit-scan.py` | 98 | GATE DOCSTRING — **the defect** | bound (5), corrected by task 3 |
| `scripts/check-selfaudit-scan.py` | 120 | GATE DOCSTRING (correct, unchanged) | bound (6) |
| `scripts/check-selfaudit-scan.py` | 280, 298, 323 | GATE LITERAL (correct, unchanged) | body-surface pinned literals |
| `scripts/check-selfaudit-scan.py` | 403 | GATE LITERAL — **the defect** | `_RUBRIC_FORMAT_QUOTED_SPAN`, widened by this task |
| `scripts/check-selfaudit-scan.py` | 415, 424 | GATE LITERAL (correct, unchanged) | `_RUBRIC_FORMAT_ADMISSION`, `_ADMISSION_SCOPE_C46` |
| `first-principles/agents/references/validation-rubric.md` | 179, 185 | GENERATED TWIN | regenerated by `sync-content.py --write`, tracks the shared/ source |
| `first-principles/agents/first-principles.md` | 325, 333, 343 | GENERATED TWIN (correct, unchanged) | regenerated body twin |
| `CLAUDE.md` | 169 | HISTORICAL — **not edited (out of scope, plan 15-13)** | describes plan 15-07's addition using the narrow phrase; the SCAN-GUARD row's own prose, not a rubric/gate assertion |

The narrower census, `/usr/bin/grep -rn "Criteria 4 and 6 only" shared/ scripts/ docs/ CLAUDE.md`, isolated exactly the four predicted hits: `shared/spine/references/validation-rubric.md:177`, `scripts/check-selfaudit-scan.py:98`, `scripts/check-selfaudit-scan.py:403`, `CLAUDE.md:169`. **No fifth prescriptive surface was found.** The `"Criterion 2"` census over `shared/spine/` found no additional prescriptive surface stating the quoting rule beyond the four already enumerated (the other hits are `assumption-taxonomy.md`'s references to Criterion 2 as a scoring mechanism, unrelated to the quoting-scope defect).

## Task 1 verification evidence

- `python3 scripts/sync-content.py --check` → exit 0.
- `/usr/bin/grep -c "for Criteria 4 and 6 only" shared/spine/references/validation-rubric.md` → **0**; same command against `first-principles/agents/references/validation-rubric.md` → **0**.
- `/usr/bin/grep -n "the Assumption Audit scan for Criterion 2" shared/spine/references/validation-rubric.md` → lines **177** (template) and **183** (admission) — count 2, as required.
- Python one-liner: `_flat(_RUBRIC_FORMAT_QUOTED_SPAN)` occurs **1** time in `_flat(RUBRIC_FILE.read_text())`; `_flat(_RUBRIC_FORMAT_QUOTED_SPAN_SUPERSEDED)` occurs **0** times in both `RUBRIC_FILE.read_text()` and `AGENT_FILE.read_text()`.
- `python3 -m py_compile scripts/check-selfaudit-scan.py` → exit 0.
- **Predicted intermediate RED state, reproduced exactly:** after task 1's edit and regeneration, `python3 scripts/check-selfaudit-scan.py` (bare live leg) exited 1 with:
  ```
  check-selfaudit-scan: FAIL — Rubric-13: admission's Criteria-4/6 clause occurs 2 time(s) in the Verdict Block Format section, expected exactly 1
  check-selfaudit-scan: FAIL — Rubric-13: admission's Criterion-2 clause occurs 2 time(s) in the Verdict Block Format section, expected exactly 1
  ```
  This is the measured evidence that the pre-15-11 clause guards were union-scoped over the whole section and needed to become region-aware — closed by task 2.

## Task 2: region split and neutralization evidence

**Measured `len(REQUIRED_BRANCHES)` = 94** (predicted 87 + 7 = 94, confirmed exactly; `_BRANCH_ROSTER_LOCK` is equal, `ROSTER LOCK: PASS`).

**Design note (deviation from the plan's literal suggestion, Rule 1 — bug fix):** the plan's Step A prescribed `split_idx = _find_flat(format_slice, _RUBRIC_FORMAT_ADMISSION)`. Implementing it literally and then constructing the required ADMISSION-region neutralization controls exposed a real defect: `_ADMISSION_SCOPE_C46`/`_ADMISSION_SCOPE_C2` are substrings of `_RUBRIC_FORMAT_ADMISSION`, so any mutation that strips or duplicates a clause from within the admission sentence also breaks the exact-match lookup used to compute `split_idx`, which resolved to `-1` and masked the intended `R-13-format-admission-*` message behind the generic "cannot region-split" failure — observed live (see below). Fixed by introducing `_RUBRIC_FORMAT_ADMISSION_LEAD` (the admission sentence's stable prefix up to its colon, which precedes both clauses) as the split anchor instead. This keeps the fail-closed discipline intact (an admission sentence with its LEAD entirely missing still fails closed) while letting the per-clause region counts fire correctly when only one clause is mutated.

### Automated self-test evidence (7 new branch ids)

All seven fire correctly via `--self-test`'s in-memory mutations; `ANTI-MASKING GATE: All 94 branches covered` confirms none is silently uncovered.

| Branch id | Mutation | Observed `--self-test` result |
|---|---|---|
| `R-13-format-template-c46-missing` | strip Criteria-4/6 clause from TEMPLATE region only | `(R-13l) correctly failed` — message contains "Criteria-4/6 clause occurs 0 time(s) in the Verdict Block Format TEMPLATE region" |
| `R-13-format-template-c46-dup` | duplicate Criteria-4/6 clause within TEMPLATE region | `(R-13m) correctly failed` — "...occurs 2 time(s)... TEMPLATE region" |
| `R-13-format-template-c2-missing` | strip Criterion-2 clause from TEMPLATE region only | `(R-13n) correctly failed` — "Criterion-2 clause occurs 0 time(s)... TEMPLATE region" |
| `R-13-format-template-c2-dup` | duplicate Criterion-2 clause within TEMPLATE region | `(R-13o) correctly failed` — "...occurs 2 time(s)... TEMPLATE region" |
| `R-13-format-quoted-span-superseded` | append narrow "for Criteria 4 and 6 only, from the self-audit scan" to rubric text | `(R-13p) correctly failed` — "superseded narrow quoted-span wording still present" |
| `X-05-superseded-body` | append narrow wording to agent-body text only | `(X-05a) correctly failed` — "Cross-5: superseded narrow quoted-span wording present in agent-body surface" |
| `X-05-superseded-rubric` | append narrow wording to rubric text only | `(X-05b) correctly failed` — "Cross-5: superseded narrow quoted-span wording present in rubric surface" |

The four pre-existing admission-region ids (`R-13-format-admission-c46-missing`/`-dup`, `-c2-missing`/`-dup`) were re-pointed to mutate within `[_RUBRIC_FORMAT_ADMISSION, _RUBRIC_CRITERIA_START)` instead of the whole section, and all four still fire correctly (`(R-13g)`-`(R-13j) correctly failed`), each now naming the ADMISSION region explicitly in its message.

### Manual scratch-copy reproduction (binding-constraint discipline)

Per binding constraints, ran isolated mutations on a disposable `rsync -a --exclude .git` scratch copy under the scratchpad directory, restoring between runs, with `git status --porcelain` confirmed to show only the intended `scripts/check-selfaudit-scan.py` change in the real tree before and after (verified empty except that one file at every restore point).

1. **Strip Criterion-2 clause from TEMPLATE region alone** (scratch emitted rubric, live gate):
   ```
   check-selfaudit-scan: FAIL — Rubric-13: amended quoted-span template occurs 0 time(s) in the Verdict Block Format section, expected exactly 1
   check-selfaudit-scan: FAIL — Rubric-13: Criterion-2 clause occurs 0 time(s) in the Verdict Block Format TEMPLATE region, expected exactly 1
   ```
   rc=1. No ADMISSION-region message fired — the ADMISSION arm stayed silent. Restored; live leg confirmed exit 0 (rc=0).

2. **Strip Criterion-2 clause from ADMISSION region alone** (scratch emitted rubric, live gate):
   ```
   check-selfaudit-scan: FAIL — Rubric-13: admission sentence occurs 0 time(s) in the Verdict Block Format section, expected exactly 1
   check-selfaudit-scan: FAIL — Rubric-13: admission's Criterion-2 clause occurs 0 time(s) in the Verdict Block Format ADMISSION region, expected exactly 1
   check-selfaudit-scan: FAIL — Rubric-13: admission sentence does not precede the Criterion 4 heading (placement violated)
   ```
   rc=1. No TEMPLATE-region message fired — the TEMPLATE arm stayed silent. This pair (rows 1 and 2) is the proof the split is real: each mutation fires only its own region's arm. Restored; live leg confirmed exit 0 (rc=0).

3. **Fail-closed `split_idx == -1` arm** — stripped the entire `_RUBRIC_FORMAT_ADMISSION_LEAD` text (scratch emitted rubric, live gate):
   ```
   check-selfaudit-scan: FAIL — Rubric-13: admission sentence occurs 0 time(s) in the Verdict Block Format section, expected exactly 1
   check-selfaudit-scan: FAIL — Rubric-13: admission sentence not found inside the Verdict Block Format section — cannot region-split the clause guards
   check-selfaudit-scan: FAIL — Rubric-13: admission sentence does not precede the Criterion 4 heading (placement violated)
   ```
   rc=1, confirming the fail-closed message fires as designed. This arm carries no `REQUIRED_BRANCHES` id of its own, matching the existing convention for not-found reporting arms (docstring bound (8): Body-3's scan-lead/ledger-fence-tail/ledger-clean, and Rubric-13's admission-sentence/Criterion-4-index not-found guards) — asserted here by manual reproduction rather than an automated `--self-test` control.

Scratch copy deleted after use; `git status --porcelain` in the real tree showed only `scripts/check-selfaudit-scan.py` modified throughout, confirmed empty of any other change at each restore point.

### Task 2 verification evidence

- `python3 scripts/check-selfaudit-scan.py --self-test` → exit 0, `ANTI-MASKING GATE: All 94 branches covered`, `ROSTER LOCK: PASS`.
- `python3 scripts/check-selfaudit-scan.py` (bare live leg) → exit 0 — **the gate now ACCEPTS the corrected template**, closing gap 1 from `15-VERIFICATION.md` (which reproduced `Rubric-13: amended quoted-span template occurs 0 time(s)... expected exactly 1` as a FAIL).
- `python3 -m py_compile scripts/check-selfaudit-scan.py` → exit 0.
- `git status --porcelain` in the real tree: only `scripts/check-selfaudit-scan.py` modified, before and after every scratch-copy mutation.

## Task 3: docstring correction and green close

`/usr/bin/grep -c "scan for Criteria 4 and 6 only" scripts/check-selfaudit-scan.py` → **0**.

`/usr/bin/grep -n "Criteria 4 and 6" scripts/check-selfaudit-scan.py` — every match classified, none states the narrow scope as current fact:

| Line | Content | Classification |
|---|---|---|
| 102, 108 | docstring bound (5), widened prose ("Criteria 4 and 6 AND the Assumption Audit scan for Criterion 2", "each of Criteria 4 and 6's quoted-span") | docstring prose, current — widened, not narrow |
| 130 | docstring bound (6), names the three-artifact enumeration | docstring prose, current — widened, not narrow |
| 314, 332 | body-surface pinned literal fragments (unrelated to the quoting-scope defect — closure-ledger inadmissibility and scan-placement sentences) | gate literal, current, unrelated |
| 357 | `_RUBRIC_FORMAT_ADMISSION` constant continuation | gate literal, current — widened (both clauses), not narrow |
| 445 | `_RUBRIC_FORMAT_QUOTED_SPAN_SUPERSEDED` constant | gate literal — **the superseded literal itself**, correctly pinned at count 0, not a current-fact claim |
| 456 | `_RUBRIC_FORMAT_ADMISSION` constant continuation | gate literal, current — widened, not narrow |
| 479 | `_ADMISSION_SCOPE_C46` constant | gate literal, current — correctly scoped (no "only"), not narrow |
| 1301 | comment describing the superseded literal | docstring/comment prose, describes history, not a current-fact claim |

No match leaves the narrow "for Criteria 4 and 6 only" scope stated as a current fact.

**Direct prose judgement (as the acceptance criteria requires — the exact judgement the verifier made to fail the truth, stated explicitly):**

- Template (widened, `shared/spine/references/validation-rubric.md:177`): `"...from the analysis being scored, or, per the admission below, from the self-audit scan for Criteria 4 and 6 or the Assumption Audit scan for Criterion 2, each emitted as process output for this analysis.]"`
- Admission (`shared/spine/references/validation-rubric.md:183`): `"...the only artifacts outside the six-section analysis a verdict block may quote: the self-audit scan for Criteria 4 and 6, and the Assumption Audit scan for Criterion 2."`

Both statements now name the same two admitted artifacts — the self-audit scan for Criteria 4 and 6, and the Assumption Audit scan for Criterion 2 — and neither forbids what the other permits. **Yes, the template and the admission now state the same rule.**

- Agent body Validate step (`shared/spine/SKILL-body.md:298`, unchanged by this plan — already amended by plan 15-08): `"...quote the specific span that satisfies or fails each criterion — from the analysis text, or, per the Verdict Block Format's admission, from the self-audit scan for Criteria 4 and 6, and the Assumption Audit scan for Criterion 2."` This agrees with both the widened template and the admission on the same two clauses. **Yes, the agent body's Validate step agrees with both.**

### Task 3 verification evidence

- `python3 scripts/check-selfaudit-scan.py --self-test` → exit 0.
- `python3 scripts/check-selfaudit-scan.py` (bare live leg) → exit 0 — the docstring-only edit did not move gate behaviour.
- `python3 scripts/sync-content.py --check` → exit 0.
- **`uv sync`** was run first to create `.venv` (pytest 9.1.1 installed per the repo's own `pyproject.toml`/`uv.lock` — a locked dev-dependency, not an ad hoc install; this is CLAUDE.md's documented remedy for VAL-03's pytest prerequisite). `bash scripts/check-firewall-battery.sh` → **`FIREWALL: GREEN (24/24)`**, with `[PASS] SCAN-GUARD check-selfaudit-scan.py --self-test + live`.
- `python3 scripts/check-registration.py --self-test` → exit 0 (29 controls, `PASS`).
- `python3 scripts/check-registration.py` (live) → exit 0 (`PASS (discovered 14 skills, agent present, manifest parsed, 14/14 names verified, 21/22 battery gates CI-registered + 1 battery-only by design)`).
- `python3 scripts/check-traceability.py --self-test` → exit 0 (`PASS`, including `HEADLINE-LOCK` and all fixture arms).
- **Measured `len(REQUIRED_BRANCHES)` = 94** — the value plan 15-13 must reconcile the four external doc surfaces (`CLAUDE.md`, `docs/ARCHITECTURE.md`, `scripts/check-firewall-battery.sh`, and any other branch-count-stating surface) against. This plan left those surfaces stale by design, per the binding constraints scoping that reconciliation to plan 15-13.

## Decisions Made

- Used `_RUBRIC_FORMAT_ADMISSION_LEAD` (a stable sentence-prefix anchor) rather than the plan's originally suggested full `_RUBRIC_FORMAT_ADMISSION` literal to compute the TEMPLATE/ADMISSION split point — necessary for the per-clause region arms to fire correctly rather than being masked behind a generic not-found failure. See "Design note" under Task 2 above.
- Ran `uv sync` to resolve the VAL-03 pytest prerequisite before running the firewall battery, per CLAUDE.md's own documented remedy; this installs only the repo's locked dev-dependencies (pytest, and its own transitive deps), not an arbitrary package.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] The plan's suggested `split_idx` anchor (`_RUBRIC_FORMAT_ADMISSION`, the full admission sentence) does not survive the exact mutations its own region-split arms are required to apply**
- **Found during:** Task 2, while wiring the `R-13-format-admission-*` neutralization controls
- **Issue:** `_ADMISSION_SCOPE_C46`/`_ADMISSION_SCOPE_C2` are substrings of `_RUBRIC_FORMAT_ADMISSION`; stripping or duplicating either clause from within the admission sentence also breaks the exact-match lookup the plan specified for locating the split point, causing `split_idx == -1` and masking the intended `R-13-format-admission-c46-missing`/`-c2-missing` (etc.) messages behind a generic "cannot region-split" failure — observed live via `--self-test`: `(R-13g) failed for the WRONG reason`.
- **Fix:** Introduced `_RUBRIC_FORMAT_ADMISSION_LEAD` (the admission sentence's prefix up to its colon, which precedes both clauses) as the split anchor instead of the full sentence. The whole-sentence `admission_count` guard still independently catches the same corruption via its own count-0 message; the LEAD-based split additionally lets the specific per-clause message fire.
- **Files modified:** `scripts/check-selfaudit-scan.py`
- **Verification:** `--self-test` shows all four re-pointed admission-region arms and all four new template-region arms `correctly failed`; manual scratch-copy reproduction (Task 2 section above) confirms the isolated pairwise behaviour the acceptance criteria requires.
- **Committed in:** `80a4803` (part of task 2 commit)

---

**Total deviations:** 1 auto-fixed (Rule 1 — bug fix in the plan's own suggested implementation detail, discovered while satisfying the plan's own acceptance criteria)
**Impact on plan:** Necessary for the region-split mechanism to actually deliver the falsifiability the plan's acceptance criteria requires (the ADMISSION-region arms firing by name, not masked by a generic not-found failure). No scope creep — the fix stays within `scripts/check-selfaudit-scan.py`, does not touch `shared/`, and does not weaken any existing guard.

## Issues Encountered

None beyond the deviation above.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

`15-VERIFICATION.md` gap 1 (SCAN-02, the Verdict Block Format template/admission contradiction) is closed: the bare SCAN-GUARD live leg exits 0, the template and admission state one rule, and `Rubric-13`'s region split makes a future one-sided edit fail by name. The tree closes green at 24/24.

Left open by design, owned by later plans in this wave chain per the binding constraints:
- Plan 15-12: `_BAND_BULLETS` parameterization and the roster floor's entry-source lock.
- Plan 15-13: reconciling the branch count (measured 94, up from 87), not-found-arm count, and census arithmetic on `CLAUDE.md`, `docs/ARCHITECTURE.md` and `scripts/check-firewall-battery.sh` — all of which this plan deliberately left stale.
- `15-REVIEW.md` WR-01 (three further band-determining limbs with no scan-table column) remains open and was not in this plan's scope.

---
*Phase: 15-self-audit-scan*
*Completed: 2026-09-04*

## Self-Check: PASSED

All created/modified files found on disk; all three task commits (e232962, 80a4803, 462bddc) confirmed present in git log.
