---
phase: 26-migration-apply-reconcile-generalize-enforce
plan: 06
subsystem: infra
tags: [gen-gate-docs, deferred-literal-ledger, ratchet, self-test, conf-13]

# Dependency graph
requires:
  - phase: 26-migration-apply-reconcile-generalize-enforce
    plan: 05
    provides: >-
      The reconciled deferred-containment ledger (26 -> 23) and its own
      RATCHET-02 scope sentence, plus the deliberately-left-unfixed
      ('CLAUDE.md', '43') containment entry whose twin literal-ledger key
      this plan reconciles
provides:
  - "The deferred-literal ledger reconciled 181 -> 180, with _DEFERRED_LEDGER_MAX and _DEFERRED_LEDGER_KEYS_DIGEST re-pinned in the same commit as the reconciliation"
  - "CLAUDE.md:39's stale hand-typed \"(43 controls)\" parenthetical replaced with a pointer to this file's own generated CONF-GATE gate-table row, with the CR-05-distinction argument recorded at the edit site (the constant's own comment block)"
  - "RATCHET-02's size-only scope sentence stated at _DEFERRED_LEDGER_MAX's own comment block, citing the concrete ('CLAUDE.md', '(43 controls)') instance"
  - "The deferred-containment ledger's own twin entry ('CLAUDE.md', '43'), whose underlying finding disappeared as a side effect of the same prose fix, reconciled in the same commit (23 -> 22), keeping plan 26-05's ratchet green"
  - "docs/gates/CONF-SURFACE.md's growth/shrink chain narrative extended with the 181 -> 180 hop, and a new disclosed bound (12) recording the .py-docstring-not-narrative-prose decision and the diagnosis-page-not-a-region-host decision"
  - "Backlog 999.41 annotated with the decision and its measured, dated cost (47 entries)"
affects: [26-07]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "A prose fix inside a fenced shell code block cannot be bracketed by a marker-pair region; the sanctioned fix is a pointer to a generated fact elsewhere on the same page, never a corrected digit restated in place"
    - "A fix that removes a hand-typed digit from a page can silently invalidate a SIBLING ledger's entry for the identical text (the deferred-literal and deferred-containment ledgers both key off exact prose), requiring both ledgers to be reconciled and re-pinned in the same commit even though only one is this plan's own named subject"
    - "A disclosed-bounds-anchor count change (or any other derived_counts field) can coincidentally corroborate -- or de-corroborate -- an unrelated bare digit elsewhere on the same page; verify against the real page via generate_all(), not an isolated draft-only test, before concluding a containment/literal-scan check is clean"

key-files:
  created: []
  modified:
    - scripts/gen-gate-docs.py
    - CLAUDE.md
    - docs/gates/CONF-SURFACE.md
    - docs/ARCHITECTURE.md

key-decisions:
  - "Combined Task 1 (the CLAUDE.md prose fix) and Task 2 (the literal-ledger reconciliation and re-pin) into a single commit, per the plan's own must_haves and the harness's explicit same-commit instruction -- landing the prose fix alone would have left literal_ledger_ratchet_problems() failing (an un-repinned shrink) at that exact commit."
  - "Also reconciled and re-pinned the deferred-CONTAINMENT ledger's twin entry ('CLAUDE.md', '43') in the SAME commit, even though this plan's own files_modified list does not name it: the prose fix that removes the digit '43' from CLAUDE.md necessarily removes the containment scanner's underlying finding for it too (the same digit, a different scanner), which plan 26-05 explicitly anticipated and deliberately deferred here. Leaving it unreconciled would have failed containment_ledger_staleness_problems() at the same commit."
  - "Used only ONE new disclosed-bounds anchor for Task 3's two decisions (not two), after discovering that raising disclosed_bounds_anchors from 12 to 14 coincidentally corroborated the frozen-historical '14' entries on CLAUDE.md and docs/ARCHITECTURE.md (an unrelated field happening to render '14' inside CLAUDE.md's own generated table cell). Raising it to 13 instead left every existing ledger entry's corroboration status unchanged, verified against the real page via generate_all()."

requirements-completed: [CONTAIN-04, RATCHET-02]

# Metrics
duration: ~50min
completed: 2026-09-10
---

# Phase 26 Plan 06: The deferred-literal ledger reconciled against re-checked live values Summary

**Reconciled the deferred-literal ledger 181 -> 180 by replacing CLAUDE.md's one stale "live-verified" hand-typed count with a pointer to a generated fact, re-pinned both ledgers (literal and its containment-ledger twin) in the same commit, and decided the `.py`-docstring and diagnosis-page scope questions D-06 left open.**

## Performance

- **Duration:** ~50 min
- **Tasks:** 3 (Tasks 1 and 2 combined into one commit per the plan's own same-commit requirement; Task 3 in its own commit)
- **Files modified:** 4 tracked (`scripts/gen-gate-docs.py`, `CLAUDE.md`, `docs/gates/CONF-SURFACE.md`, `docs/ARCHITECTURE.md` as the mechanical `--write` regeneration side effect) plus 3 gitignored (`.planning/STATE.md`, `.planning/ROADMAP.md`, `.planning/REQUIREMENTS.md`)

## Accomplishments

- Mechanically enumerated (by scanning `_DEFERRED_LITERAL_HITS`'s reason strings for `--describe` + `live-verified`, not by reading research's own example): exactly **2** ledger entries assert a live value from another gate's `--describe` output, both on `CLAUDE.md` — `'(33 controls)'` (reason: `check-provenance.py`'s `control_count`) and `'(43 controls)'` (reason: `check-conf-gate.py`'s `control_count`).
- Re-invoked both gates live in this session: `check-provenance.py --describe` → `control_count=33` (**matches** the reason and the prose — left untouched); `check-conf-gate.py --describe` → `control_count=44` (**mismatches** the reason's `43` and the prose's `43` — the entry that had gone stale, first found live by plan 26-05's own research a day earlier and deliberately left unfixed for this plan).
- Fixed the mismatch at its source: `CLAUDE.md:39`'s hand-typed `"(43 controls)"` parenthetical is replaced with `"(control count: see the CI gates table's CONF-GATE row below)"` — a pointer to `CLAUDE.md:171`'s own already-correct generated row (`control_count=44`), not a corrected `"(44 controls)"` digit. A marker-pair region cannot bracket that line (it sits inside a fenced ` ```sh ` block, outside `_generated_marker_pairs_for()`'s reach), so the pointer edit is the only NARR-02-consistent fix available. The CR-05 distinction is recorded at the edit site itself (`_DEFERRED_LEDGER_MAX`'s own comment block, in the same commit): CR-05 deleted a **true** literal and substituted an unfalsifiable hedge; this deletes a literal **already proven false** this session and substitutes a pointer to a generated value on the same page — strictly more checkable than what it replaced, not less.
- Re-ran the literal scan after the fix: `describe()`'s `literal_scan_hits` moved from **213** (pre-fix) to **212** (post-fix, ledger not yet reconciled) — confirming the hit genuinely disappeared rather than merely being re-exempted.
- `_DEFERRED_LEDGER_MAX` and `_DEFERRED_LEDGER_KEYS_DIGEST` re-pinned **181 -> 180** in the same commit as the ledger-key removal, with a new growth/shrink history entry and RATCHET-02's size-only scope sentence appended to the constant's own comment block, citing this concrete instance by key.
- **Side effect requiring its own reconciliation, in the same commit:** removing the digit `"43"` from `CLAUDE.md` also removed the deferred-**containment** ledger's twin entry `('CLAUDE.md', '43')` underlying finding (same digit, a different scanner) — exactly the coupling plan 26-05 anticipated and deliberately deferred ("fixing CLAUDE.md's own prose here would move that ledger too... its re-pin reserved for plan 26-06"). Reconciled `_CONTAINMENT_LEDGER_MAX`/`_CONTAINMENT_LEDGER_KEYS_DIGEST` **23 -> 22** in the same commit, keeping plan 26-05's own ratchet green.
- `docs/gates/CONF-SURFACE.md`'s growth/shrink chain narrative (bound (6)) is extended with the new `181 -> 180` hop so `chain_terminus_problems()` stays current on this page; the one touched self-test control (`_control_delta_chain_hops_confsurface_corrected`, a LIVE-TEXT-DRIVEN control by its own design) is updated to match (hop count 5 -> 6, terminus `('181',)` -> `('180',)`).
- Task 3 records D-06's `.py`-docstring decision as a new disclosed bound (12) on `docs/gates/CONF-SURFACE.md`: a Python module docstring is **not** "narrative prose" for NARR-02/criterion 3's region target, because `docs/PROCESS.md` section 2's product/apparatus cut draws the line by claim audience (a docstring's audience is inside the build loop) and NARR-02's own text already scopes its target to the six containment-unreachable Markdown surfaces — confirmed exhaustive rather than widened. The cost is stated honestly and dated: 47 `_DEFERRED_LITERAL_HITS` entries carry backlog `999.41` as of 2026-09-10, the largest unadjudicated share of the ledger, staying ledgered under its existing blanket permit — **not closed by this phase**. The same bound also records the decision **not** to make `docs/v9.1-claim-containment-diagnosis.md` a region host (a frozen diagnosis record; regionizing it would be the regression D-06 proviso 3 forbids). Backlog `999.41` in `.planning/ROADMAP.md` is annotated with the same decision.

## Task Commits

1. **Tasks 1+2 combined: fix CLAUDE.md's stale prose and reconcile/re-pin both ledgers** — `e49b6d5` (feat)
2. **Task 3: decide the `.py`-docstring and diagnosis-page scope calls (D-06)** — `d9ed155` (docs)

**Plan metadata:** this SUMMARY.md and the STATE.md/ROADMAP.md/REQUIREMENTS.md updates are committed together as the plan's closing metadata commit — `.planning/STATE.md`, `.planning/ROADMAP.md` and `.planning/REQUIREMENTS.md` stay gitignored per project convention (`commit_docs: false`) and are not part of that commit's file list beyond what the harness force-tracks (this SUMMARY.md).

## Files Created/Modified

- `scripts/gen-gate-docs.py` — removed `('CLAUDE.md', '(43 controls)')` from `_DEFERRED_LITERAL_HITS` and `('CLAUDE.md', '43')` from `_DEFERRED_CONTAINMENT_HITS`; re-pinned `_DEFERRED_LEDGER_MAX`/`_DEFERRED_LEDGER_KEYS_DIGEST` (181/180) and `_CONTAINMENT_LEDGER_MAX`/`_CONTAINMENT_LEDGER_KEYS_DIGEST` (23/22) with new growth/shrink history entries; added RATCHET-02's size-only scope sentence to `_DEFERRED_LEDGER_MAX`'s comment block; updated `_control_delta_chain_hops_confsurface_corrected`'s docstring and assertions to the new live text; added one new `LITERAL_SCAN_DISCLOSED_BOUNDS` anchor (`py-docstring-not-narrative-prose-scope`).
- `CLAUDE.md` — line 39's `"(43 controls)"` replaced with a pointer to its own generated CONF-GATE row; the CONF-SURFACE table row's own `disclosed_bounds_anchors` cell updated to 13 as the mechanical `--write` side effect.
- `docs/gates/CONF-SURFACE.md` — bound (6)'s growth/shrink chain narrative extended with the `181 -> 180` hop; new bound (12) records both D-06 decisions; Facts fence regenerated (`literal_scan_ledger_entries`/`max` 181->180, `containment_ledger_entries`/`max` 23->22, `disclosed_bounds_anchors` 12->13, `control_ids`/`control_count` unchanged at 109).
- `docs/ARCHITECTURE.md` — CONF-SURFACE's generated gate-table row cell updated to match, as the mechanical `--write` regeneration side effect; no other cell changed.
- `.planning/ROADMAP.md` (gitignored) — Phase 26 criterion 1 marked discharged; plan `26-06` checkbox ticked; backlog `999.41` annotated with the docstring-scope decision and its measured cost.
- `.planning/REQUIREMENTS.md` (gitignored) — `CONTAIN-04` and `RATCHET-02` marked complete, both halves (containment from plan 26-05, literal from this plan) recorded in place; status table rows updated to `Complete`.

## Decisions Made

See `key-decisions` in the frontmatter above (verbatim, not repeated here per `docs/PROCESS.md` §1's own citation-not-restatement rule).

## Deviations from Plan

**1. [Same-commit coupling, per the plan's own must_haves — not a Rule 1-4 fix] Tasks 1 and 2 landed as a single commit rather than two.**
- **Found during:** preparing to commit Task 1's own prose fix in isolation.
- **What happened:** the moment `CLAUDE.md:39`'s stale digit was removed, `literal_ledger_staleness_problems()` began reporting the now-orphaned ledger key, and the pre-commit hook's own gate 4 (`gen-gate-docs.py --self-test`) exercises `cmd_check()` against the real tree in several controls. A Task-1-only commit would have failed its own pre-commit hook.
- **Why:** this is exactly the scenario the plan's own must_haves and the harness's sequential-execution instructions anticipated for this plan ("both pins to move in the SAME commit as the reconciliation").
- **Impact:** one larger commit (`e49b6d5`) instead of two; every acceptance criterion from both tasks was independently verified before that single commit was made (see transcripts below).

**2. [Rule 1/3 — blocking, directly caused by this plan's own edit] The deferred-containment ledger's twin entry also required reconciliation, in the same commit.**
- **Found during:** re-running `--self-test` immediately after the CLAUDE.md prose fix, before the literal-ledger reconciliation had even landed.
- **Issue:** `containment_ledger_staleness_problems()` reported `('CLAUDE.md', '43')` as no longer matching any live finding — the digit `"43"` this plan's own fix removed was the exact text the deferred-CONTAINMENT ledger's own entry (a *different* scanner, keyed on bare digits rather than phrases) had permitted. This is the coupling plan 26-05 explicitly named and deliberately deferred to this plan.
- **Fix:** removed `('CLAUDE.md', '43')` from `_DEFERRED_CONTAINMENT_HITS` and re-pinned `_CONTAINMENT_LEDGER_MAX`/`_CONTAINMENT_LEDGER_KEYS_DIGEST` (23 -> 22) in the same commit as the literal-ledger reconciliation.
- **Files modified:** `scripts/gen-gate-docs.py` (containment ledger dict, its pin, its digest, its growth/shrink history comment).
- **Verification:** `containment_ledger_ratchet_problems()` and `containment_ledger_staleness_problems()` both `[]` after the fix; transcribed below.
- **Committed in:** `e49b6d5`.

**3. [Rule 1 — blocking, directly caused by this plan's own edit] `docs/gates/CONF-SURFACE.md`'s own chain-terminus narrative went stale the moment the pin moved, and required its own extension.**
- **Found during:** the first `--self-test` re-run after the ledger re-pin.
- **Issue:** `chain_terminus_problems()` reported `docs/gates/CONF-SURFACE.md`'s own growth-chain narrative (`134 -> 152 -> ... -> 183 -> 181`) as stale — its terminus (`181`) no longer matched the live `literal_scan_ledger_max` (now `180`).
- **Fix:** extended the chain narrative with a new `181 -> 180` hop, attributing it to this plan by name, and updated the one touched self-test control (`_control_delta_chain_hops_confsurface_corrected`) to the new hop count and terminus, per that control's own documented LIVE-TEXT-DRIVEN convention.
- **Committed in:** `e49b6d5`.

**4. [Rule 1 — blocking, exposed by Task 3's own edit] Raising `disclosed_bounds_anchors` from 12 to 14 (two new anchors) coincidentally corroborated the frozen-historical `'14'` entries on `CLAUDE.md` and `docs/ARCHITECTURE.md`.**
- **Found during:** `--self-test` after adding Task 3's new disclosed bound with two new anchor names.
- **Issue:** `CLAUDE.md`'s own generated CONF-SURFACE table cell renders `disclosed_bounds_anchors=14`; since `'14'` now appeared inside a generated fence, the containment scanner treated the *unrelated* frozen-historical `'14'` prose on `CLAUDE.md`/`docs/ARCHITECTURE.md` as newly corroborated, orphaning those two containment-ledger entries.
- **Fix:** used only one new disclosed-bounds anchor (bundling both Task 3 decisions under bound (12) with a single anchor name), raising the count to 13 instead of 14 — verified clean by regenerating the real page via `generate_all()` and re-running `--self-test`, not by an isolated draft-only test.
- **Committed in:** `d9ed155`.

---

**Total deviations:** 4, all Rule 1/3 auto-fixes directly caused by this plan's own edits (either explicitly anticipated by plan 26-05, or a mechanical consequence of the reconciliation this plan's own must_haves required). No scope creep; no architectural decision required.

## Issues Encountered

**Coincidental cross-ledger and cross-check corroboration is a real, recurring fragility, not a one-off.** Three separate times in this plan, a change to one part of the Facts fence or the page's own prose caused an *unrelated* bare digit elsewhere on the same page to flip its corroboration status (deviations 2 and 4 above; a third, transient occurrence during Task 1's isolated work — `docs/gates/CONF-SURFACE.md`'s own `'5'` — resolved itself once `--write` was re-run against the live harvest). Every instance was resolved by re-deriving against the real, on-disk page through `generate_all()` — never by trusting an isolated draft-only test — per the established pitfall discipline. None of these is newly introduced risk: `docs/gates/CONF-SURFACE.md`'s own bound (2) already discloses "the scanner proves a number is CURRENT, never that it describes the right thing," which is exactly this class of coincidence. Not fixed further here (out of this plan's own stated scope — CONTAIN-04/RATCHET-02, not a scanner-robustness hardening pass); left as a working pattern for future reconciliation plans, matching backlog `999.72`'s own class of latent containment-mechanism residuals.

## In-Process Verification Transcripts

**Mechanical enumeration of live-value ledger entries (Task 1), before any edit:**

| Key | Reason value | Live `--describe` invocation | Live value | Prose literal (`CLAUDE.md`) | Verdict |
|---|---|---|---|---|---|
| `('CLAUDE.md', '(33 controls)')` | 33 | `python3 scripts/check-provenance.py --describe` → `control_count` | 33 | `(33 controls)` (line 37) | **match** — left untouched |
| `('CLAUDE.md', '(43 controls)')` | 43 | `python3 scripts/check-conf-gate.py --describe` → `control_count` | 44 | `(43 controls)` (line 39) | **mismatch** — fixed |

**`literal_scan_hits` readings, both taken by module import:**

| Reading point | Value |
|---|---|
| Before this plan's edit | 213 |
| After the prose fix, before ledger reconciliation | 212 |

**Task 1 acceptance — pre-repin failure, transcribed verbatim (confirms the mechanism working, not a bug):**

```
CLAUDE.md: deferred-containment-ledger key no longer matches any live finding: '43' (remove this ledger entry -- its underlying prose was likely already fixed)
CLAUDE.md: deferred-literal-ledger key no longer matches any live hit: '(43 controls)' (remove this ledger entry -- its underlying prose was likely already fixed)
```
`python3 scripts/gen-gate-docs.py --self-test` at this point: **exit 1** (3 controls failing on the above), exactly as the plan's own acceptance criteria anticipated ("`--check` is expected to FAIL at this point... it is the mechanism working").

**Task 2 — ratchet re-pin, transcribed:**

```
_DEFERRED_LEDGER_MAX:              181 -> 180
_DEFERRED_LEDGER_KEYS_DIGEST:      sha256:200b241f... -> sha256:e76f58ee...
_CONTAINMENT_LEDGER_MAX:           23 -> 22
_CONTAINMENT_LEDGER_KEYS_DIGEST:   sha256:ac8790ce... -> sha256:847df3a5...
literal_ledger_ratchet_problems()       -> []
containment_ledger_ratchet_problems()   -> []
```

**Phase-opening endpoint, read from git (not from a planning document):**

```
$ git show f2073f3:scripts/gen-gate-docs.py | grep -n "_DEFERRED_LEDGER_MAX: int"
2967:_DEFERRED_LEDGER_MAX: int = 181
```

**Delta, both endpoints measured in this session:** `181` (phase-opening, `f2073f3`) `->` `180` (this plan's own commit `e49b6d5`) — one entry removed, no replacement, published on `docs/gates/CONF-SURFACE.md`'s bound (6).

**`/usr/bin/grep -rn "tens, not hundreds" docs/ scripts/ CLAUDE.md` → (no matches).**

**Final verify, all green (both after `e49b6d5` and after `d9ed155`):**

```
python3 scripts/gen-gate-docs.py --self-test         # SELF-TEST PASS -- 109 controls run
python3 scripts/gen-gate-docs.py --check              # exit 0; harvested 22/22 expected script-backed entries
sh .githooks/pre-commit                               # all five gates PASS, exit 0
bash scripts/check-firewall-battery.sh                # FIREWALL: GREEN (26/26)
```

**Ledger readings, both taken by module import, before this plan and after its final commit:**

| Reading point | `len(_DEFERRED_LITERAL_HITS)` | `_DEFERRED_LEDGER_MAX` | `len(_DEFERRED_CONTAINMENT_HITS)` | `_CONTAINMENT_LEDGER_MAX` |
|---|---|---|---|---|
| Before this plan | 181 | 181 | 23 | 23 |
| After this plan | 180 | 180 | 22 | 22 |

`git diff --diff-filter=D --name-only` on both commits returned empty — no unexpected deletions. `git status --porcelain` clean before the first edit and after each commit. `git diff --name-only` from this plan's base commit (`356b549`) to `HEAD` lists exactly `CLAUDE.md`, `docs/ARCHITECTURE.md`, `docs/gates/CONF-SURFACE.md`, `scripts/gen-gate-docs.py` — neither `.github/workflows/validation.yml` nor `scripts/check-firewall-battery.sh` appears; battery tally unchanged at 26/26.

## Assumption Drift (advisory)

None material. One color note: the plan's own task 1 anticipated ONLY the literal ledger's ratchet failing pre-repin ("a ledger ratchet finding, because the ledger has shrunk and the pins have not moved"); in practice, fixing the prose also broke the deferred-containment ledger's own staleness predicate simultaneously (a second, distinct finding), which the plan's own prior-wave note and 26-05's SUMMARY had already flagged as the expected coupling — so this is a confirmed prediction, not a drift, but the acceptance-criteria wording named only one of the two mechanisms that would actually fire.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- Plan 26-07 (RATCHET-01's four-arm mutation demonstration, criterion 3's published target and residue, criterion 6's invariance by direct count, phase close) can proceed directly: both ledgers are reconciled and re-pinned, `CONTAIN-04` and `RATCHET-02` are both marked complete in `.planning/REQUIREMENTS.md`, and the `.py`-docstring/diagnosis-page scope calls D-06 required are decided and recorded with their cost.
- Backlog `999.41` (the `.py`-docstring bucket, 47 entries) and `999.69`/`999.73` (the containment ledger's own remaining `cannot_reach`/`frozen_historical`/`not_a_count_claim` residue) are published and named, not closed in-phase — consistent with D-06 proviso 2 and D-05 proviso 4.
- No blockers. `FIREWALL: GREEN (26/26)`, tally unchanged; CI job count unchanged.

---
*Phase: 26-migration-apply-reconcile-generalize-enforce*
*Completed: 2026-09-10*

## Self-Check: PASSED

- FOUND: `scripts/gen-gate-docs.py`
- FOUND: `CLAUDE.md`
- FOUND: `docs/gates/CONF-SURFACE.md`
- FOUND: `docs/ARCHITECTURE.md`
- FOUND: `.planning/phases/26-migration-apply-reconcile-generalize-enforce/26-06-SUMMARY.md`
- FOUND: commit `e49b6d5` in `git log --oneline --all`
- FOUND: commit `d9ed155` in `git log --oneline --all`
