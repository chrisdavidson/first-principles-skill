---
phase: 23-ship-v9-0-0
plan: 05
subsystem: release-changelog
tags: [changelog, release, ship-05, conformance-baseline, no-fix-fence, requirements-closure]

# Dependency graph
requires:
  - phase: 23-ship-v9-0-0
    plan: 04
    provides: "FIREWALL: GREEN (26/26) reading, battery/registry/CI id-set reconciliation, carried-forward CONF-SURFACE.md finding"
  - phase: 24-diagnosis-name-the-mechanism-not-the-instance
    provides: "Dispositions for CR-01, CR-02, CR-03 (docs/v9.1-claim-containment-diagnosis.md § 3), discharging D-06 and releasing v9.0.0's D-05 hold"
provides:
  - "CHANGELOG.md [9.0.0] entry (commit 6e4af7e) closing the SHIP-05 disclosure by name as an honest before/after pair with all three moved denominators stated"
  - "CHANGELOG.md [9.0.0] entry disclosing CR-01, CR-02, CR-03 by name per D-14, each citing its own site path plus docs/v9.1-claim-containment-diagnosis.md section 3"
  - "docs/conformance-baseline.md re-confirmed with no drift; MEASUREMENT_DATE deliberately not bumped"
  - "REL-01 through REL-04 all ticked in .planning/REQUIREMENTS.md with inline command-and-reading evidence"
  - "ROADMAP.md and STATE.md reconciled: Phase 23 marked complete, v9.0.0 marked SHIPPED, halt block and HELD heading preserved verbatim"
  - "Explicit, disclosed adjudication of the CR-01/docs/gates/CONF-SURFACE.md phase-wide fence exception carried forward from 23-04-SUMMARY.md"
affects: []

tech-stack:
  added: []
  patterns: ["phase-wide no-fix fence evaluated against PHASE_BASE_SHA rather than HEAD~1", "explicit HELD-WITH-DISCLOSED-EXCEPTION adjudication rather than silent resolution or a blanket halt"]

key-files:
  created:
    - ".planning/phases/23-ship-v9-0-0/23-05-SUMMARY.md"
  modified:
    - "CHANGELOG.md"
    - ".planning/REQUIREMENTS.md"
    - ".planning/ROADMAP.md"
    - ".planning/STATE.md"

key-decisions:
  - "MEASUREMENT_DATE in scripts/report-conformance.py was NOT bumped. report-conformance.py --check reported no drift against the committed 2026-09-06 reading, meaning nothing measured moved; the plan's own rule says bumping the date in that case would assert a new measurement event the identical bytes disprove. The re-confirmation is recorded as re-confirmed-on-ship-date rather than re-dated."
  - "The [9.0.0] entry additionally publishes the adversarial-corpus false-negative rate (10 of 13) and the live-conformance rate (5 of 8, with its N and its empty-heading-population vacuity bound), beyond REL-04's stated minimum (the SHIP-05 before/after pair and the CR-01/02/03 disclosures). Reasoning: both are the milestone's own honest counter-readings, and publishing the conformance zeros while omitting them would be the selective-disclosure move this project's own threat model (T-23-09) flags."
  - "The CR-01 / docs/gates/CONF-SURFACE.md phase-wide no-fix fence is adjudicated HELD-WITH-DISCLOSED-EXCEPTION rather than treated as a fresh halt. The file differs from PHASE_BASE_SHA (commit ed73189, plan 23-02) but only in three unrelated derived_counts values, a mechanical side effect of gen-gate-docs.py --write regenerating the page after 23-02's headline sweep; the CR-01 sentence itself (line 219) is byte-identical, no fix was written, and a revert is unavailable because CONF-SURFACE's own drift gate requires the regenerated counts. This is disclosed explicitly here rather than silently absorbed or papered over, per this milestone's own stated purpose."

requirements-completed: [REL-01, REL-02, REL-03, REL-04]

# Metrics
duration: ~70min
completed: 2026-09-09
---

# Phase 23 Plan 05: Publish [9.0.0] — SHIP-05 Closure, CR-01/02/03 Disclosure, Phase Closure Summary

**`CHANGELOG.md` now carries a `[9.0.0]` entry (commit `6e4af7e`) that closes the SHIP-05
disclosure by name as an honest before/after pair with all three moved denominators stated
(`69→77`, `58→77`, `28→31`) and discloses CR-01, CR-02 and CR-03 live and uncorrected per D-14;
`docs/conformance-baseline.md` was re-confirmed with zero drift; REL-01 through REL-04 are all
ticked on their own commands and readings; and the phase-wide no-fix fence is reported honestly —
HELD for CR-02/CR-03, HELD-WITH-DISCLOSED-EXCEPTION for CR-01's `docs/gates/CONF-SURFACE.md`
(a mechanical derived-count regeneration in commit `ed73189`, not a fix).**

## Performance

- **Duration:** ~70 min
- **Started:** 2026-09-09 (session start, before any read)
- **Completed:** 2026-09-09T17:59:54Z
- **Tasks:** 3 completed (task 1: conformance-baseline re-confirmation, no commit — no drift found;
  task 2: `[9.0.0]` CHANGELOG entry, commit `6e4af7e`; task 3: REL box ticks and phase closure,
  no commit — all three edited files are gitignored)
- **Files modified:** 4 (`CHANGELOG.md` committed; `.planning/REQUIREMENTS.md`,
  `.planning/ROADMAP.md`, `.planning/STATE.md` gitignored, not committed)

## Task 1 — Final conformance-baseline reading, `_FROZEN_PATHS` sweep, `MEASUREMENT_DATE` decision

**Verify command run in full:**

```
$ python3 scripts/report-conformance.py --self-test
report-conformance: SELF-TEST PASS — 102 controls run
$ python3 scripts/report-conformance.py --check
report-conformance: PASS — no drift
$ python3 scripts/check-conf-gate.py --self-test
check-conf-gate: SELF-TEST PASS — 44 controls run
$ python3 scripts/check-conf-gate.py
check-conf-gate: COVERAGE — measured 28 artifacts across shared-examples, generated-twin
check-conf-gate: D-08(a)/(b)/(c) falsification arms fired and recovered
check-conf-gate: PASS
```

**Final headline readings, verbatim from `docs/conformance-baseline.md` (measurement date
2026-09-06, re-run and confirmed byte-identical this session):**

| Reading | shared-examples | generated-twin | contract-surface |
|---|---|---|---|
| Files unreadable by `_slice_sections` | 0 of 14 | 0 of 14 | 0 of 1 |
| §6 conclusion claims (untraced) | 77 (2 untraced) | 77 (2 untraced) | 3 (3 untraced) |
| §6 untraced claims (marked / silent) | 2 untraced (2 marked, 0 silent) | 2 untraced (2 marked, 0 silent) | 3 untraced (0 marked, 3 silent) |
| §2 verdict cells (non-conforming) | 77 (0 non-conforming) | 77 (0 non-conforming) | 1 (1 non-conforming) |
| §4 `chain_blocks` (malformed) | 31 (0 malformed) | 31 (0 malformed) | 3 (1 malformed) |
| `### Conclusion` heading-swept blocks (malformed) | 31 (0 malformed) | 31 (0 malformed) | 1 (0 malformed) |
| Source-vs-twin agreement (D-04) | 14 of 14 pairs agree | | |

- **adversarial-corpus false-negative rate:** 10 of 13 (Stratum A 2 of 5, Stratum B1 1 of 1,
  Stratum B2 7 of 7); diagnostic 9 of 13 no column fired.
- **live-conformance rate:** 5 of 8 (primary and secondary conditional rate agree; 8 of 8
  attempted runs completed). Vacuity bound (CR-01, disclosed in the artifact's own prose): the
  `### Conclusion` heading sweep found 6 blocks total across the 8 resolved runs and none at all
  in 7 of them, so `heading_malformed_blocks == 0` — one of the four counts the rate is defined
  on — is vacuous on those 7 runs; a quarter of the clean verdict's four counts is carried by a
  single run.

**`MEASUREMENT_DATE` decision, recorded explicitly:** `--check` reported no drift, meaning the
committed bytes are byte-identical to a fresh run — nothing measured moved since 2026-09-06.
Per the plan's own rule, `MEASUREMENT_DATE` (`scripts/report-conformance.py:59`,
`"2026-09-06"`) was **NOT bumped** — bumping it would assert a new measurement event that the
identical bytes disprove. The reading is recorded as **re-confirmed on the ship date
(2026-09-09) against the stated measurement date (2026-09-06)**, not re-dated.

**Marked-claim residual confirmation:** `docs/conformance-baseline.md` "Disclosed bounds" bound 2
already states the marked-claim residual as 4 (2 shared-examples + 2 generated-twin) and frames it
as a ratchet ("may fall, never rise") equal to `scripts/check-conf-gate.py`'s `_MARKED_RATCHET`.
Live confirmation this session: `/usr/bin/grep -n "_MARKED_RATCHET: int" scripts/check-conf-gate.py`
→ `223:_MARKED_RATCHET: int = 4`. The two agree; no edit was needed to the generated artifact.

**CONTRACT-06 pins byte-unchanged:** `git log --oneline -- scripts/check-quality-harness.py`
shows no commit from Phase 23 (most recent touch: `b83d23d`, Phase 21) — the three sha256 pins
are untouched by this phase.

**`_FROZEN_PATHS` sweep.** Read directly out of `scripts/check-firewall-battery.sh` (not
transcribed from prose) — **22 entries**:

```
tests/step0-baseline-v*.md
tests/step0-captures-v*
tests/routing-baseline-v3.*.md
tests/routing-battery-baseline-v4.3.md
tests/routing-baseline-v7.11.md
tests/routing-battery-baseline-v7.11.md
tests/routing-baseline-v7.13.md
tests/routing-battery-baseline-v8.5.md
tests/focused-output-baseline-v*.md
tests/sub-skill-routing-baseline-v*.md
tests/quality-catalog-v8.7.md
tests/quality-probe-v8.7
tests/quality-baseline-v8.7-regenerated
tests/quality-baseline-v8.7
tests/quality-baseline-v8.7-postfix
tests/quality-baseline-v8.10-oos
tests/defrobust-v8.11
tests/quality-provenance-v8.24
tests/quality-ledger-v8.26
tests/adversarial-corpus-v9.0
tests/live-conformance-v9.0
tests/live-conformance-catalog.md
```

Both legs run against `PHASE_BASE_SHA` (`40064eeaaad2ad9a0fbe407dfc875dff631c3b82`, from
`23-01-SUMMARY.md`), spanning the whole phase rather than the last commit:

```
$ git diff --stat 40064eeaaad2ad9a0fbe407dfc875dff631c3b82 HEAD -- <22 pathspecs>
(empty) exit 0

$ git status --porcelain --untracked-files=all -- <22 pathspecs>
(empty) exit 0
```

Both readings clean — the frozen-evidence invariant holds phase-wide. No file changed in Task 1;
no commit made.

## Task 2 — The `[9.0.0]` CHANGELOG entry

**Phase-wide no-fix fence, run before drafting and re-run after committing** (base:
`PHASE_BASE_SHA = 40064eeaaad2ad9a0fbe407dfc875dff631c3b82`, recorded in `23-01-SUMMARY.md`, used
verbatim — not derived):

| Finding | Site | Fence check | Result |
|---|---|---|---|
| CR-01 | `docs/gates/CONF-SURFACE.md` | `git diff --name-only "$PHASE_BASE_SHA"..HEAD -- docs/gates/CONF-SURFACE.md` | **NON-EMPTY** — file changed. See adjudication below. |
| CR-02 | `CLAUDE.md` § "Review protocol" | Section-scoped diff, `git show "$PHASE_BASE_SHA":CLAUDE.md` vs. working tree, `awk` extractor `index($0,h)==1{f=1;print;next} f&&/^#+ /{exit} f{print}` with `h='### Review protocol'` | **EMPTY diff, 37 lines both sides (non-vacuous).** HELD. |
| CR-03 | `docs/README.md` § "Standing of the nine milestone documents" | Same extractor, `h='## Standing of the nine milestone documents'` (the heading is `##`, not `###` — corrected after an initial vacuous 0-line extraction with the wrong heading level, caught immediately by the non-vacuity requirement) | **EMPTY diff, 42 lines both sides (non-vacuous).** HELD. |

**CR-01 adjudication — HELD-WITH-DISCLOSED-EXCEPTION, not a fresh halt.** This finding was
carried forward, unresolved, from `23-04-SUMMARY.md`. Verified independently in this plan's own
session:

- `git diff "$PHASE_BASE_SHA"..HEAD -- docs/gates/CONF-SURFACE.md` shows exactly one changed line
  (the `derived_counts` line inside the "Facts fence"), introduced in commit `ed73189` (plan
  23-02, `git log -p` confirms), with three values moved:
  `literal_scan_exempt_headline-provenance-delta` 11→13, `literal_scan_hits` 211→213,
  `literal_scan_nonmodule_docstring_hits` 383→398. No other line in the file differs.
- The CR-01 narrative sentence itself, line 219 ("plan 22-09 grew it a third time, 182 → 184..."),
  is **byte-identical** between `PHASE_BASE_SHA` and `HEAD` — confirmed by grepping both revisions
  directly. The stale terminus this finding is about was never touched.
- The change is a **mechanical side effect**: plan 23-02's headline sweep added two more `N → M`
  headline-provenance-delta instances elsewhere in the tree, and `gen-gate-docs.py --write`
  regenerated `docs/gates/CONF-SURFACE.md`'s derived-counts line as a consequence — not a
  targeted edit to CR-01's own sentence, and no fix or correction was written for CR-01 anywhere
  in Phase 23's commit history.
- **A revert is unavailable.** `docs/gates/CONF-SURFACE.md`'s own drift gate
  (`gen-gate-docs.py --check`, part of both pre-commit hooks) requires the regenerated counts to
  match a fresh run; reverting the three values to their pre-23-02 state would itself fail that
  gate on the very next commit.

**Adjudication, stated plainly:** the *spirit* of D-09/D-14's no-fix clause holds — Phase 23
wrote no fix for CR-01 — but the plan's own must_have truth as literally written ("No commit
anywhere in Phase 23 changed... `docs/gates/CONF-SURFACE.md`") is **FALSE** and is **not**
restated here as satisfied. The fence is recorded as **HELD-WITH-DISCLOSED-EXCEPTION**: the file
changed (commit `ed73189`), the change is unrelated to CR-01's own claim, the change is mechanical
and unavoidable given the drift gate's own requirement, and no fix was written. This plan did not
hand-edit `docs/gates/CONF-SURFACE.md` to try to force the absolute claim true, and does not
proceed past this without disclosing it. This adjudication is carried into `.planning/STATE.md`
and `.planning/ROADMAP.md` (Task 3) as well — see below. **This plan's own commits touch none of
the three sites** (`CHANGELOG.md` only) — the CR-01 exception predates this plan entirely.

**Figure-by-figure re-verification against fresh command output, run in this session
immediately before committing:**

| Figure in entry | Fresh command | Result | Match |
|---|---|---|---|
| Coverage headline `192/94/0/286` → `208/97/0/305` | `check-traceability.py --self-test` | `HEADLINE-LOCK PASS: published headline == 208 reproducible / 97 audit-only / 0 gap / 305 total` | ✓ |
| 19 rows, 16 reproducible + 3 audit-only | `check-traceability.py --self-test` | `V9-ROWS PASS: row count == 19`; `tier partition ... audit-only=['CONF-14','CONF-15','REL-04'], 16 reproducible` | ✓ |
| Battery 24/24 → 26/26; CONF-GATE 24→25; CONF-SURFACE 25→26 | `bash scripts/check-firewall-battery.sh`; `CLAUDE.md`'s own narration | `FIREWALL: GREEN (26/26)`; narration sentence present verbatim | ✓ |
| CONF-03..06 figures (0 of 14, 0 of 77, 0 of 31, 2/2/0, `_MARKED_RATCHET=4`) | `report-conformance.py --check`; `check-conf-gate.py --self-test`/live; grep | No drift; SELF-TEST PASS; PASS; `_MARKED_RATCHET: int = 4` | ✓ |
| CONF-07/08 (10 of 13; Stratum A 2/5, B1 1/1, B2 7/7) | `report-conformance.py --check` (confirms committed bytes current) | No drift | ✓ |
| CONF-09/10 (5 of 8; 6 blocks/8 runs, 0 in 7) | `report-conformance.py --check` | No drift | ✓ |
| CONF-11/12/13 (`--self-test` 74 controls; `--check` 22/22; `literal_scan_non_exempt=0`) | `gen-gate-docs.py --self-test`; `--check` | `SELF-TEST PASS — 74 controls run`; `harvested 22/22 expected script-backed entries (22 total)` | ✓ |
| CONF-14/15 (depth-rule quote; "No script, control or CI job enforces any of this") | grep | `docs/PROCESS.md:17` quote present; `CLAUDE.md:280` sentence present | ✓ |
| CR-01 stale terminus (`182 → 184` vs. live `181`) | grep | `docs/gates/CONF-SURFACE.md:219` "182 → 184"; `scripts/gen-gate-docs.py:2093` `_DEFERRED_LEDGER_MAX: int = 181` | ✓ |
| CR-02 (`CLAUDE.md`'s CR-05 characterization vs. CR-05's own `File:` field) | grep | `CLAUDE.md:282` "an edit made in `scripts/`..."; `21-REVIEW.md:271-274` `### CR-05`, `File:` names only `docs/README.md`, `docs/MEASUREMENT-MAP.md`, `docs/COMPONENT-DIAGRAM.md` | ✓ |
| CR-03 (13 stated vs. 12 distinct rows) | python one-liner over `docs/data/matrix.json` (this session, not copied from the diagnosis doc) | `distinct rows: 12`; `grep -c` raw substring count: `13` | ✓ |
| Backlog 999.54 (CR-03), 999.55 (CR-02) exist | grep `.planning/ROADMAP.md` | Both headers present | ✓ |

**Entry shape and prohibitions verified:**

- `git diff HEAD~1 -- CHANGELOG.md` → 118 insertions, 0 deletions; the sole `-` line in the diff
  output is the `--- c/CHANGELOG.md` header line, not a content deletion. Additions only, above
  `## [8.26.0]`.
- Inside the `[9.0.0]` section: no mention of the rework cap firing, of a halted phase, or of
  999.49 (grepped for all three; zero hits).
- `/usr/bin/grep -q "^## \[9.0.0\]" CHANGELOG.md && for t in SHIP-05 CR-01 CR-02 CR-03
  v9.1-claim-containment-diagnosis; do grep -q "$t" CHANGELOG.md; done` → all present.
- `python3 scripts/gen-gate-docs.py --self-test` → `SELF-TEST PASS — 74 controls run`; `--check`
  → `harvested 22/22 expected script-backed entries (22 total)`, exit 0.
- `sh .githooks/pre-commit` → exit 0 (the `DRIFT: /tmp/.../artifact.md` line in the output is
  `report-conformance.py --self-test`'s own internal mutated-fixture noise, the same expected
  signal `23-04-SUMMARY.md` recorded — not a real drift finding against this repository).

**Discretion exercised, recorded per the plan's own instruction:** the entry additionally
publishes the adversarial-corpus false-negative rate (10 of 13) and the live-conformance rate
(5 of 8, with its N and its empty-heading-population vacuity bound), beyond REL-04's stated
minimum. Reasoning: both are the milestone's own honest counter-readings; publishing the
conformance zeros while omitting them would be the selective-disclosure move this project's own
threat model (T-23-09) explicitly flags. `output-template.md`'s disclosed exclusion and the
closure-ledger route's zero-shipped-exemplars fact are published as `**Disclosed limits —**`
clauses on the exemplar-conformance bullet.

**Commit:** `git add CHANGELOG.md` → `git commit` → `6e4af7e` (`docs(23-05): publish [9.0.0]
CHANGELOG entry closing SHIP-05 and disclosing CR-01/02/03`). Post-commit deletion check:
`git diff --diff-filter=D --name-only HEAD~1 HEAD` → empty.

## Task 3 — REL box ticks, ROADMAP and STATE reconciliation

**REL-01 through REL-04, each ticked with its own inline evidence line (command + literal
reading + date), never a plan number or a summary file as ground:**

- **REL-01** (already `[x]` from plan 23-03): evidence line already present, unchanged.
- **REL-02** (was `[x]` with no inline evidence — added one this pass): cites
  `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (26/26)`, the battery/registry
  strict-equality reconciliation (26==26), the CI-job axis scoped to REG-GUARD's own
  `_BATTERY_GATE_RE` (24 call-site ids, `A′ minus C = {QUAL-01}`), and the three scratch-copy
  mutations proving the registration floor fires by name — restating `23-04-SUMMARY.md`'s
  findings as REL-02's own recorded evidence rather than leaving it implicit.
- **REL-03** (already `[x]` from plan 23-02): evidence line already present, unchanged.
- **REL-04** (ticked `[ ]` → `[x]` this pass): cites the grep/diff checks from Task 2's verify
  command, the four SHIP-05 before/after pairs with denominators named, the CR-01/02/03
  disclosure with both citations each, and the re-confirmed `docs/conformance-baseline.md`
  reading with the marked-claim residual matching `_MARKED_RATCHET`, commit `6e4af7e`.

`/usr/bin/grep -c "^- \[ \] \*\*REL-0[1-4]\*\*" .planning/REQUIREMENTS.md` → **0** (all four
v9.0.0 REL boxes ticked). **Note on the plan's literal acceptance-criterion grep**
(`grep -c "^- \[ \] \*\*REL-0"`, without the `[1-4]` bound): this returns **4**, not 0 — but
those four hits are **REL-05 through REL-08**, v9.1.0's own release requirements mapped to
Phase 27 (not yet planned), which are correctly `Pending` per the Traceability table. This is a
pattern-scope artifact of the plan's grep (both milestones' release requirements share the
`REL-0` prefix), not an unticked v9.0.0 box; confirmed by naming all four hits explicitly above.
The Traceability table's Status column was updated to `Complete` for REL-01 through REL-04, and
the file's `*Last updated*` footer and its top-line milestone-status header (`v9.0.0 (open,
release held)` → `v9.0.0 (shipped)`) were both corrected.

**ROADMAP.md:**

- Phase 23 bullet: `[ ]` → `[x]`, with a dated completion annotation in the shape other phase
  bullets use, naming what shipped (5/5 plans, all six criteria, both commit hashes) and the
  date (2026-09-09), plus the phase-wide fence result (CR-02/CR-03 HELD, CR-01
  HELD-WITH-DISCLOSED-EXCEPTION, named in full).
- `**Plans**:` line updated with the actual 5-plan list; wave-5 plan checkbox ticked.
- `## Active Milestone` v9.0.0 summary paragraph (the second, independent "HELD" assertion
  outside the Phase 23 bullet, per D-01's misalignment class) rewritten in place to state
  SHIPPED 2026-09-09, all four REL boxes ticked, and Phase 22's halt correctly re-stated as a
  rework-axis halt (D-04) whose own requirements (CONF-14/15) re-derived clean and are ticked.
- `/usr/bin/grep -n "HELD" .planning/ROADMAP.md` → the only remaining hits are the ones this
  plan itself wrote (the fence-status prose "HELD clean" / "HELD-WITH-DISCLOSED-EXCEPTION"),
  confirmed by reading — no stale HELD assertion survives.

**Six ROADMAP success criteria, discharged one by one:**

| # | Criterion | Evidence |
|---|---|---|
| 1 | 17 stamps `9.0.0`; VERSION-01 green; `sync-content.py --check` clean | `check-version-stamps.py` → PASS (re-run this session); `sync-content.py --check` → exit 0; commit `a27a308` (plan 23-03) |
| 2 | Battery GREEN with `CONF-GATE`/Phase 21-22 controls registered, gate-count surfaces agree | `FIREWALL: GREEN (26/26)` re-confirmed this session; battery/registry/CI reconciliation by equality (plan 23-04, no commit — read/record only) |
| 3 | Matrix rows registered, headline move via `HEADLINE-LOCK` | `_rows_v9()`, 19 rows; headline `192/94/0/286`→`208/97/0/305` confirmed live this session; commit `ed73189` (plan 23-02) |
| 4 | `[9.0.0]` entry closes SHIP-05 by name, honest before/after pair | Commit `6e4af7e`; all four figures restated with three moved denominators named (this plan, Task 2) |
| 5 | `docs/conformance-baseline.md` final reading; marked-claim residual as ratchet's standing value | Re-confirmed no-drift this session (Task 1); bound 2 already states residual=4=`_MARKED_RATCHET` |
| 6 | `[9.0.0]` entry discloses CR-01/CR-02/CR-03 by name, each citing its disposition path | Commit `6e4af7e`; each of the three cited with both its own site path and `docs/v9.1-claim-containment-diagnosis.md` § 3 (this plan, Task 2) |

**STATE.md:**

- Pre-edit copy taken (`/tmp/state_pre_edit_copy.md`) before any edit, for the byte-verbatim
  diff below.
- `## Current Position`, the "Current focus" line, and the frontmatter (`completed_phases` 7→8,
  `completed_plans` 77→78, `percent` 11→12, `last_updated`, `last_activity`) all updated to
  reflect Phase 23 COMPLETE / v9.0.0 SHIPPED and the next focus (Phase 25, not yet planned).
  **Counters derived by counting, not incrementing**: `total_phases` (66, unchanged — 11 real
  `### Phase N` headers [17-27] + 55 backlog `### Phase 999.x` headers, no new backlog entries
  filed this plan) and `total_plans`/`completed_plans` (78/78 — counted directly via
  `grep -c "^- \[.\] [0-9][0-9]-[0-9][0-9]-PLAN\.md" .planning/ROADMAP.md` for total, and the
  `[x]`-only variant for completed, both re-run after the edit).
- `### v9.0.0 is OPEN and its release is HELD` heading: confirmed **byte-unchanged** — grepped
  directly, matches the pre-edit copy word for word.
- A further dated supersession note was **appended** beneath the existing D-13/D-14 notes
  (never deleting or rewording them), recording that v9.0.0 SHIPPED 2026-09-09, naming both
  commits, restating the phase-wide fence result, and stating the release ordering is now
  realised.
- `#### The Phase 22 halt record, verbatim` through the section's closing `---`: confirmed
  **byte-identical** to the pre-edit copy via `diff` (exit 0).
- A new dated narrative note for "Phase 23 plan 05" was appended after the existing "Phase 23
  plan 04" note (never editing it), carrying the same fence adjudication as above.
- `## Operator Next Steps`: a further dated supersession note was appended above the existing
  D-13 note (kept verbatim beneath it, per D-07), stating both `/bm:plan-phase 24` and
  `/bm:plan-phase 23` are now fully discharged and the actual next step is `/bm:plan-phase 25`.

**Tracking status of Task 3's three files, stated explicitly so this is not mistaken for a
commit that does not exist:** `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`, and
`.planning/STATE.md` are all **gitignored** (`git check-ignore -v` confirms all three against
`.gitignore:1:.planning/`), consistent with `commit_docs: false` and with plans 23-01 and 23-04's
identical pattern. `git status --short .planning/` is empty. **No commit was made for Task 3.**

## Verification Results

```
$ bash scripts/check-firewall-battery.sh ; echo EXIT:$?
FIREWALL: GREEN (26/26)
EXIT:0

$ python3 scripts/check-version-stamps.py ; echo EXIT:$?
check-version-stamps: PASS
EXIT:0

$ python3 scripts/check-traceability.py --self-test ; echo EXIT:$?
check-traceability --self-test: PASS
EXIT:0

$ python3 scripts/report-conformance.py --self-test ; echo EXIT:$?
report-conformance: SELF-TEST PASS — 102 controls run
EXIT:0

$ python3 scripts/report-conformance.py --check ; echo EXIT:$?
report-conformance: PASS — no drift
EXIT:0

$ python3 scripts/gen-gate-docs.py --self-test ; echo EXIT:$?
gen-gate-docs: SELF-TEST PASS — 74 controls run
EXIT:0

$ python3 scripts/gen-gate-docs.py --check ; echo EXIT:$?
harvested 22/22 expected script-backed entries (22 total)
EXIT:0

$ sh .githooks/pre-commit ; echo EXIT:$?
(report-conformance --self-test's own internal mutated-fixture DRIFT line, expected noise)
report-conformance: SELF-TEST PASS — 102 controls run
report-conformance: PASS — no drift
gen-gate-docs: SELF-TEST PASS — 74 controls run
harvested 22/22 expected script-backed entries (22 total)
EXIT:0

$ /usr/bin/grep -c "^- \[ \] \*\*REL-0[1-4]\*\*" .planning/REQUIREMENTS.md
0

$ git log --oneline -3
6e4af7e docs(23-05): publish [9.0.0] CHANGELOG entry closing SHIP-05 and disclosing CR-01/02/03
24bd55c docs(23-04): complete REL-02 battery reconciliation plan
413d5c5 docs(23-03): complete REL-01 version-stamp lockstep bump plan

$ git diff --diff-filter=D --name-only HEAD~1 HEAD
(empty)

$ git status --short .planning/
(empty — all three edited planning files are gitignored)
```

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] CR-03's `awk` section extractor initially used the wrong heading level**
- **Found during:** Task 2, running the phase-wide no-fix fence for CR-03.
- **Issue:** The plan's own extractor template used `h='### Standing of the nine milestone
  documents'` (a level-3 heading marker), but the actual heading in `docs/README.md` is
  `## Standing of the nine milestone documents` (level 2). The mismatched marker produced a
  vacuous 0-line extraction on both sides, which the plan's own non-vacuity requirement caught
  immediately (both sides read 0 lines, tripping the "guard the vacuous case" rule rather than
  passing silently).
- **Fix:** Re-ran the extraction with the correct `##` heading level, producing a non-vacuous
  42-line extraction on both sides with an empty diff.
- **Files modified:** None (read-only verification step; no product file touched).
- **Verification:** `wc -l` on both extractions showing 42 lines each; `diff` exit 0.
- **Committed in:** N/A — this was a verification-script correction, not a product change.

**2. [Rule 1 - Bug] `.planning/REQUIREMENTS.md`'s top-line milestone-status header was stale**
- **Found during:** Task 3, while reviewing REQUIREMENTS.md for phase-closure edits beyond the
  three explicitly named files in the plan's own header (which named `.planning/REQUIREMENTS.md`
  as a file this plan modifies, but the plan's action text focused on the REL boxes and the
  Traceability table, not the file's own title/header line).
- **Issue:** Line 1 read "v9.0.0 (open, release held)" and line 4 read "Phases 17-23 — release
  HELD" — both now false now that v9.0.0 has shipped in this same plan.
- **Fix:** Corrected in place to "v9.0.0 (shipped)" and "Phases 17-23 — SHIPPED 2026-09-09".
  This header carries no verbatim-preservation constraint (unlike STATE.md's halt block and HELD
  heading), so it was corrected directly rather than superseded by addition.
- **Files modified:** `.planning/REQUIREMENTS.md`.
- **Verification:** Re-read the header lines after the edit.
- **Committed in:** N/A — `.planning/REQUIREMENTS.md` is gitignored, no commit exists for this
  file.

---

**Total deviations:** 2 auto-fixed (1 bug in a verification step, 1 stale-claim bug in a
gitignored planning artifact). **Impact on plan:** Neither touched any of the three no-fix-fenced
sites or the shipped `CHANGELOG.md`. No scope creep.

## Assumption Drift (advisory)

None material. One thing worth naming explicitly rather than letting it pass silently: this
plan's own must_have truth #8 ("No commit anywhere in Phase 23 changed... `docs/gates/
CONF-SURFACE.md`") was planned as an absolute claim and turned out to be false in its literal
form — see the CR-01 adjudication above under Task 2. This is not drift in the sense of a
changed working assumption during execution; it is a pre-existing, carried-forward finding from
plan 23-04 that this plan was explicitly tasked with adjudicating, and it is adjudicated in full
above rather than restated as satisfied.

## Known Stubs

None. This plan writes one CHANGELOG entry (`CHANGELOG.md`) and edits three gitignored
planning-state files (`REQUIREMENTS.md`, `ROADMAP.md`, `STATE.md`); no shipped product surface,
UI, or data-rendering path is touched.

## Threat Flags

None new. Per the plan's own threat model, all five threats (T-23-08 through T-23-13, excluding
T-23-SC which is n/a) were `mitigate`-dispositioned and are discharged as follows:

- **T-23-08** (a stale figure at publish time): every figure in the entry was matched against a
  fresh command run in this session (table above); none was carried over from an earlier phase's
  reading without re-verification.
- **T-23-09** (selective disclosure): the entry additionally publishes the adversarial-corpus and
  live-conformance rates beyond REL-04's minimum, with the choice recorded (Decisions section).
- **T-23-10** (editing a frozen historical CHANGELOG figure): `git diff HEAD~1 -- CHANGELOG.md`
  shows additions only, above `## [8.26.0]`; confirmed by counting `-` lines in the diff (only
  the header line, no content deletion).
- **T-23-12** (a fix written for CR-01/02/03 anywhere in Phase 23's history): the phase-wide
  fence against `PHASE_BASE_SHA` was run and its result reported honestly, including the one
  place it does NOT hold clean (CR-01/`CONF-SURFACE.md`) — adjudicated as a disclosed, mechanical
  exception rather than silently passed or hidden.
- **T-23-13** (an edit or injected untracked file inside `_FROZEN_PATHS`): both legs run clean
  against `PHASE_BASE_SHA`, pathspecs read from the battery script itself, entry count (22)
  recorded.

## Next Steps

- v9.0.0 is fully shipped and closed. There is no further work on this milestone.
- v9.1.0 continues at **Phase 25 (mechanism design — CONTAIN-01..03)**, not yet planned. Next
  operator command: `/bm:plan-phase 25`.
- Standing backlog carried forward, unaffected by this plan: **999.54** (CR-03's provenance-anchor
  gap), **999.55** (CR-02's routing to the consistency-shaped class), **999.50/999.51/999.52**
  (the consistency-shaped class generally), and the pre-existing longer list in
  `.planning/STATE.md` § Operator Next Steps.

## Self-Check: PASSED

- `test -f CHANGELOG.md && grep -q "^## \[9.0.0\]" CHANGELOG.md` → FOUND
- `git log --oneline --all | grep -q 6e4af7e` → FOUND (`6e4af7e docs(23-05): publish [9.0.0]
  CHANGELOG entry closing SHIP-05 and disclosing CR-01/02/03`)
- `test -f .planning/REQUIREMENTS.md && grep -c "^- \[ \] \*\*REL-0[1-4]\*\*"` → `0` → FOUND
  (zero unticked v9.0.0 REL boxes)
- `test -f .planning/ROADMAP.md && grep -q "^\- \[x\] \*\*Phase 23"` → FOUND
- `test -f .planning/STATE.md && grep -A 12 "^### v9.0.0 is OPEN"` byte-matches the pre-edit
  copy → CONFIRMED (diff exit 0 against `/tmp/state_pre_edit_copy.md` for both the heading block
  and the full halt-record block)
- `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (26/26)` → CONFIRMED (re-run, same
  result as plan 23-04's own reading)
- `test -f .planning/phases/23-ship-v9-0-0/23-05-SUMMARY.md` → FOUND (this file)
