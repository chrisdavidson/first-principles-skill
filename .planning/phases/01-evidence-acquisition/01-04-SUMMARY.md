---
phase: 01-evidence-acquisition
plan: 04
subsystem: agent-body
tags: [prompt-engineering, markdown, self-audit-gate, provenance, sync-content, gate, offline-harness, act-limb, harn-01, gap-closure]

# Dependency graph
requires:
  - phase: 01-evidence-acquisition (plan 01)
    provides: "Phase 3 Operation verification-step paragraph and Criterion 3 Fix note"
  - phase: 01-evidence-acquisition (plan 02)
    provides: "scripts/check-act-limb.py — HARN-01 offline gate"
  - phase: 01-evidence-acquisition (plan 03)
    provides: "Repaired population selector and assignment-verb failure branch (ACT-02/ACT-03 gaps 1-2), 19-control self-test battery"
provides:
  - "Exhaustive three-branch partition of the Phase 3 acquisition step's outcomes (success / not-found / unreachable) in shared/spine/SKILL-body.md, with a narrowed resolved-state exclusion and a widened provenance-table unverified row"
  - "Rubric Criterion 3 Fix note whose downgrade branch covers both failure modes (source unreachable, source reachable but unsupporting)"
  - "scripts/check-act-limb.py re-anchored onto the exhaustive partition, extended from 19 to 24 self-test controls (a)-(x), closing CR-02 and WR-08"
affects: [01-evidence-acquisition (Phase 4 / HARN-04 registration), Phase 4 (Ship)]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Outcome-branch exhaustiveness demonstrated by explicit case enumeration (population selector x source-opens x figure-located) rather than inferred from presence checks — the anti-recurrence discipline this plan itself was commissioned to add after 01-03 passed every presence check it was given and still shipped an unhandled branch"
    - "Fixture-mutation helper generalized from whole-file replace to a region-anchored splice (find start heading, find end heading, assert block uniqueness inside that byte range, splice head+mutated-region+tail) — closes a class of vacuous-control risk where a block's text collision outside its intended region silently mutates the wrong occurrence"
    - "Shared reason token as cross-file coherence anchor: `citation does not support the claim` is asserted present, byte-identical, in both the body slice (Body-6) and the rubric Fix-note paragraph (Rubric-6) — the same two-sided binding pattern Body-10/Rubric-5 established for pointer names in 01-03"
    - "Block-scoped rubric checks (Rubric-3/5/6) share one located Fix-note paragraph rather than each independently searching the whole Criterion 3 slice — a gutted-but-relocated note can no longer scatter required phrases past a slice-wide search"

key-files:
  created: []
  modified:
    - shared/spine/SKILL-body.md
    - shared/spine/references/validation-rubric.md
    - first-principles/agents/first-principles.md
    - first-principles/agents/references/validation-rubric.md
    - scripts/check-act-limb.py

key-decisions:
  - "The not-found branch references the Phase 3 failure record artifact in its PLAIN (unbolded) form rather than redefining it — Body-10 asserts the bold form occurs exactly once in the Phase 3 slice, and the unreachable branch already owns that definition site; a second bold occurrence would fail Body-10 on this task's own final run. Measured before writing prose (GATE-COUPLING SWEEP in the plan's <interfaces>), not discovered after."
  - "Task 3 (body gate) and Task 4 (rubric gate) were split from what the plan's previous revision bundled as one task, so each reaches an independent green checkpoint and Body-10's exact-count coupling — the thing that made the previous revision self-defeating — is isolated to one task's blast radius."
  - "CR-02 (Rubric-3/Rubric-5 slice-scoped, not Fix-note-scoped) is closed in this plan rather than deferred again, because Task 2 edits the exact paragraph CR-02 is about and Task 4 adds a paragraph-scoped Rubric-6 neighbour — leaving Rubric-3/5 slice-scoped next to a paragraph-scoped check would be an inconsistency inviting the next editor to widen Rubric-6 back."
  - "WR-08 (_mutate_body_removing_from_block replaces the first whole-file occurrence) is closed here because control (v) is a brand-new call site against a brand-new block (the provenance table) — an unanchored helper would make that control vacuous by construction, the exact failure mode this plan exists to eliminate."

patterns-established:
  - "A gate-coupling sweep — enumerating every count-bearing assertion in the gate file from its COUNTING LOGIC, not its constant block — performed BEFORE prose is finalized, and re-derived AFTER the gate is edited, catches a self-defeating repair before it ships (this is what caught the previous plan revision's second bolded artifact name, which would have driven Body-10 from 1 to 2 and failed the gate on its own closing run)."

requirements-completed: [ACT-02, ACT-03, ACT-05, HARN-01]

# Metrics
duration: ~50min
completed: 2026-08-27
---

# Phase 1 Plan 4: Evidence Acquisition — Branch-Exhaustiveness Gap Closure (CR-01) Summary

**Closed the second gap of the same defect class that 01-03 closed: a ground truth whose cited source opens but whose asserted figure or wording is not located satisfied none of the acquisition step's three outcome branches and was permanently barred from a later read by 01-03's own exclusion clause — added a third outcome branch, narrowed the exclusion to a resolved-state qualifier, widened the provenance table and the rubric's downgrade branch to match, and re-anchored HARN-01 from 19 to 24 self-test controls, closing CR-02 and WR-08 along the way.**

## Performance

- **Duration:** ~50 min
- **Started:** worktree branch-check reset to `b765d76` (this plan's expected base)
- **Completed:** this commit
- **Tasks:** 5/5 completed (Task 5 is a verification-only sweep, no files modified)
- **Files modified:** 5 (`shared/spine/SKILL-body.md`, `shared/spine/references/validation-rubric.md`, `first-principles/agents/first-principles.md`, `first-principles/agents/references/validation-rubric.md`, `scripts/check-act-limb.py`)

## Accomplishments

- The Phase 3 acquisition step in `shared/spine/SKILL-body.md` now has a third outcome branch: when the cited source opens but the asserted figure or wording is not located in it, the step writes a Phase 3 failure record with the reason `citation does not support the claim`, marks the ground truth `?` (assigning the suffix if it did not already carry one), and lands it on the `unverified` label — closing ROADMAP Phase 1's derived truth #6 (the failed truth in `01-VERIFICATION.md`).
- The exclusion clause 01-03 added is narrowed from "already opened" to "already opened **and in which the asserted figure or wording was located**" — it now bars only a ground truth that reached a resolved state, so it can no longer swallow the new not-found branch.
- The provenance table's `unverified` row is widened to admit "the cited source was opened and the asserted figure or wording was not found in it" alongside its original "no source was located at all" — the not-found branch's label is now a label the table actually defines.
- The rubric's Criterion 3 Fix note downgrade branch is widened from "taken only when the source cannot be opened" to also cover "or opens without containing the asserted figure or wording," and its failure-record requirement now admits `citation does not support the claim` as a reason alongside "which source and why unreachable" — the same token the body writes, asserted byte-identical in both emitted files.
- `scripts/check-act-limb.py` is re-anchored: four new body constants (`_B12_NOT_FOUND_BRANCH`, `_B12B_NOT_FOUND_ASSIGN`, `_B13_EXCLUSION_RESOLVED`, `_B14_TABLE_NOT_FOUND`) fold into Body-5/Body-6, and a new Body-12 asserts the provenance table's coverage. Two new rubric constants (`_R6_DOWNGRADE_SCOPE`, `_R6B_SHARED_REASON`) back a new, paragraph-scoped Rubric-6.
- WR-08 is closed: `_mutate_body_removing_from_block` is rebuilt to splice its mutation into the exact byte range between `_PHASE3_START` and `_PHASE4_START`, asserting block uniqueness *inside that region* rather than searching-and-replacing against the whole file.
- CR-02 is closed: Rubric-3 and Rubric-5 are narrowed from whole-Criterion-3-slice scope to the same Fix-note paragraph block Rubric-6 locates, so a gutted-but-relocated Fix note (the verifier's own documented CR-02 fixture) can no longer pass.
- The self-test battery grew from 19 controls (a)-(s) to 24 controls (a)-(x); all 24 behave as intended. Every new control was demonstrated non-vacuous by scratch-process execution against the real emitted files, not merely asserted from a code reading.
- Full offline gate sweep after all four repairs: `FIREWALL: RED (1 gate(s) failed; 16/17 passed)`, VAL-03 the sole failure, confirmed to be the pre-existing missing-`pytest` environment gap (byte-identical to the baseline recorded across `01-01-SUMMARY.md`, `01-02-SUMMARY.md`, `01-03-SUMMARY.md` and `01-VERIFICATION.md`) — no new failure, no version stamp moved (all 17 at `8.17.5`).

## Task Commits

1. **Task 1: Add the not-found outcome branch, narrow the exclusion, widen the provenance table, and demonstrate the partition** — `00d9993` (feat)
2. **Task 2: Widen the rubric's Criterion 3 downgrade branch to cover both failure modes** — `7d76886` (feat)
3. **Task 3: Re-anchor HARN-01's BODY checks onto the exhaustive partition, and close WR-08** — `20cc0c5` (feat)
4. **Task 4: Re-anchor HARN-01's RUBRIC checks onto the widened downgrade branch, and close CR-02** — `03fa674` (feat)
5. **Task 5: Regenerate, run the full offline battery, and record the closing evidence** — no commit (verification-only, no files modified, per task's own `<files>` spec)

**Plan metadata:** (this commit, below)

## Files Created/Modified

- `shared/spine/SKILL-body.md` — added the not-found outcome branch, narrowed the exclusion, widened the provenance table's `unverified` row.
- `shared/spine/references/validation-rubric.md` — widened Criterion 3's Fix note downgrade branch and failure-record reason list.
- `first-principles/agents/first-principles.md` — regenerated via `sync-content.py --write`; carries both body repairs verbatim, zero drift.
- `first-principles/agents/references/validation-rubric.md` — regenerated via `sync-content.py --write`; carries the rubric repair verbatim, zero drift.
- `scripts/check-act-limb.py` — added `_B12_NOT_FOUND_BRANCH`, `_B12B_NOT_FOUND_ASSIGN`, `_B13_EXCLUSION_RESOLVED`, `_B14_TABLE_NOT_FOUND`, `_R6_DOWNGRADE_SCOPE`, `_R6B_SHARED_REASON`; extended Body-5/Body-6; added Body-12 and Rubric-6; closed WR-08 (region-anchored `_mutate_body_removing_from_block`) and CR-02 (paragraph-scoped Rubric-3/5); added self-test controls (t)-(x).

## 1. Verbatim Before/After

### The acquisition paragraph

**Before (shipped by 01-03, the two-branch form `01-VERIFICATION.md` failed on):**

```
**Acquire the evidence — attempt the read before assigning the label.** This is the **Phase 3 verification step**: for every ground truth that will feed a HIGH-confidence derivation chain and whose cited source this analysis has not yet opened — whether or not it currently carries the `?` — attempt to open the cited source directly, with Read for a local path or repository file, Grep to locate the asserted figure or wording within it, or WebFetch for a URL, before recording the provenance label the table above assigns. The read is what decides the suffix, so the suffix cannot decide what earns a read: both halves of this population are decidable before the provenance table assigns anything — whether this feeds a HIGH-confidence chain is a fact about the analysis's intent, whether this analysis has opened the source is a fact about what it did. A ground truth whose cited source this analysis has already opened, and a ground truth feeding only a MEDIUM- or LOW-confidence chain, do not earn a read: verification reads compete with the Self-Audit Gate for the same turn budget, and the gate runs last. When the source opens and the asserted figure or wording is located, the ground truth becomes `read-at-source`, drops the `?` if it carried one, and its read-location — the page, table, section, or quoted passage — is recorded; a well-formed citation this analysis did not open stays `reported-by-delegate` and keeps the `?` the provenance table requires, because the read is what moves the label, not the citation's quality. When the source cannot be opened, the step writes the **Phase 3 failure record**: which source and why unreachable — 404, paywall, no network, path not found, ambiguous citation — and mark that ground truth `?`, assigning the suffix if it did not already carry one: no silent fallback to an unmarked ground truth. [...]
```

**After (this plan's repair, mirrored verbatim in `first-principles/agents/first-principles.md`):**

```
**Acquire the evidence — attempt the read before assigning the label.** This is the **Phase 3 verification step**: for every ground truth that will feed a HIGH-confidence derivation chain and whose cited source this analysis has not yet opened — whether or not it currently carries the `?` — attempt to open the cited source directly, with Read for a local path or repository file, Grep to locate the asserted figure or wording within it, or WebFetch for a URL, before recording the provenance label the table above assigns. The read is what decides the suffix, so the suffix cannot decide what earns a read: both halves of this population are decidable before the provenance table assigns anything — whether this feeds a HIGH-confidence chain is a fact about the analysis's intent, whether this analysis has opened the source is a fact about what it did. A ground truth whose cited source this analysis has already opened and in which the asserted figure or wording was located, and a ground truth feeding only a MEDIUM- or LOW-confidence chain, do not earn a read: verification reads compete with the Self-Audit Gate for the same turn budget, and the gate runs last. When the source opens and the asserted figure or wording is located, the ground truth becomes `read-at-source`, drops the `?` if it carried one, and its read-location — the page, table, section, or quoted passage — is recorded; a well-formed citation this analysis did not open stays `reported-by-delegate` and keeps the `?` the provenance table requires, because the read is what moves the label, not the citation's quality. When the source opens but the asserted figure or wording is not located in it, the step writes a Phase 3 failure record with the reason `citation does not support the claim` and marks that ground truth `?`, assigning the suffix if it did not already carry one, so it lands on the `unverified` label. When the source cannot be opened, the step writes the **Phase 3 failure record**: which source and why unreachable — 404, paywall, no network, path not found, ambiguous citation — and mark that ground truth `?`, assigning the suffix if it did not already carry one: no silent fallback to an unmarked ground truth. [...]
```

Two changes: the exclusion clause gained `and in which the asserted figure or wording was located`, and one new sentence was inserted between the success/no-read sentence and the "cannot be opened" sentence.

### The `unverified` provenance-table row

**Before:** `| **unverified** | No source was located at all. | **`?` required** |`

**After:** `| **unverified** | No source was located at all, or the cited source was opened and the asserted figure or wording was not found in it. | **`?` required** |`

### The rubric's Fix note (Criterion 3)

**Before:**

```
**Fix — acquire before you downgrade.** Branch one, preferred: acquire the evidence — open
  the cited source, per the Phase 3 verification step, and let the read move the provenance
  label. Branch two: downgrade the confidence — carry the `?` and drop the chain from HIGH,
  taken only when the source cannot be opened. The preference, explicitly: acquisition is preferred when the source is reachable, because a gate whose only available Fix weakens the output resolves every failure toward less claim rather than more evidence. The unreachable case is not a free pass — the downgrade branch still requires the Phase 3 failure record, which source and why unreachable, so a reader can tell a downgrade from a skipped attempt.
```

**After:**

```
**Fix — acquire before you downgrade.** Branch one, preferred: acquire the evidence — open
  the cited source, per the Phase 3 verification step, and let the read move the provenance
  label. Branch two: downgrade the confidence — carry the `?` and drop the chain from HIGH,
  taken only when the source cannot be opened or opens without containing the asserted figure or wording. The preference, explicitly: acquisition is preferred when the source is reachable, because a gate whose only available Fix weakens the output resolves every failure toward less claim rather than more evidence. The unreachable case is not a free pass — the downgrade branch still requires the Phase 3 failure record, which source and why unreachable, or `citation does not support the claim`, so a reader can tell a downgrade from a skipped attempt.
```

## 2. Branch-Exhaustiveness Demonstration (Task 1, action step 5)

Read against the EMITTED paragraph in `first-principles/agents/first-principles.md` (quoted in full above under "After").

| Case | Admitted by the population selector? | Excluded? | Branch that fires | End state |
|---|---|---|---|---|
| 1. In population; source opens; asserted figure located | Yes — feeds a HIGH-confidence chain and source not yet opened | No — not yet opened, so not excluded | Success branch: "When the source opens and the asserted figure or wording is located, the ground truth becomes `read-at-source`" | `read-at-source`, `?` dropped, read-location recorded |
| 2. In population; source opens; asserted figure NOT located ← **the gap** | Yes — same as case 1 (population is decided before the read happens) | No — the exclusion requires the figure to have been *located*; this case did not locate it, so the exclusion's first limb does not match | Not-found branch: "When the source opens but the asserted figure or wording is not located in it, the step writes a Phase 3 failure record with the reason `citation does not support the claim` and marks that ground truth `?`... so it lands on the `unverified` label" | Phase 3 failure record + `?`, labelled `unverified` |
| 3. In population; source cannot be opened | Yes — same as case 1 | No — the exclusion is about sources already opened; an unopenable source was never opened | Unreachable branch: "When the source cannot be opened, the step writes the **Phase 3 failure record**: which source and why unreachable ... and mark that ground truth `?`" | Phase 3 failure record + `?` |
| 4. Not in population (MEDIUM/LOW-confidence chain, or the read was simply not attempted) | No — population requires "will feed a HIGH-confidence derivation chain" | Excluded via the second limb ("a ground truth feeding only a MEDIUM- or LOW-confidence chain, do not earn a read") for the MEDIUM/LOW sub-case; simply outside the population selector for the "not attempted" sub-case | No-read branch: "a well-formed citation this analysis did not open stays `reported-by-delegate` and keeps the `?` the provenance table requires" | `reported-by-delegate`, `?` retained |
| 5. Already opened and located on an earlier pass | No — population requires "whose cited source this analysis has not yet opened"; already opened, so outside the population by construction | Also excluded by the (narrowed) exclusion's first limb, redundantly | No branch fires — the ground truth is not re-processed by this step at all; it already carries `read-at-source` from the pass that located the figure | `read-at-source` (unchanged, from the earlier successful pass) |

### (a) Coverage — cases 1/2/3 are exhaustive over the population by construction

The source either opens or it does not (case 3 vs. cases 1/2). If it opens, the asserted figure either is or is not located (case 1 vs. case 2). There is no third state for "did the source open" and no third state for "was the figure located" — these are each binary facts about what happened during the read attempt, so the three cases partition every possible read outcome for a ground truth inside the population.

Additional candidate outcomes considered and folded:
- *"Source opens and states a DIFFERENT figure than asserted"* — folds into case 2, because the *asserted* figure was not located; the branch's trigger ("the asserted figure or wording is not located in it") does not distinguish "absent" from "present but different," and it does not need to — both are "not located."
- *"Ambiguous citation (unclear which of several sources is meant)"* — folds into case 3 via the existing why-unreachable list, which already names "ambiguous citation" as one of the "cannot be opened" reasons (404, paywall, no network, path not found, ambiguous citation).
- *"Source opens, figure located, but the analysis mis-transcribes it"* — out of scope for this step: the acquisition step's job is to attempt the read and record what was found; transcription accuracy is a property of the analysis's own diligence, not a fourth outcome of the acquisition step itself. Not folded into any of the three branches because it is not a branch of *this* step — it is a hypothetical failure of a later step (recording).

### (b) No unresolved exit — every case ends in a labelled, recorded state

Case 1 ends `read-at-source` (drops the `?` per the success sentence: "the ground truth becomes `read-at-source`, drops the `?` if it carried one, and its read-location ... is recorded"). Case 2 ends with a Phase 3 failure record and the `?`, labelled `unverified` (per the not-found sentence, quoted above). Case 3 ends with a Phase 3 failure record and the `?` (per the unreachable sentence: "the step writes the **Phase 3 failure record**: which source and why unreachable ... and mark that ground truth `?`"). Case 4 ends `reported-by-delegate` + `?` via the no-read branch — confirmed: a ground truth in the population whose read is never attempted is, by the population selector's own wording, "whose cited source this analysis has **not yet opened**"; if the step runs and no read happens for it (because it's excluded by the MEDIUM/LOW limb, or because the population simply doesn't reach it in this pass), it retains whatever label it already carried, which for a never-opened citation is `reported-by-delegate` + `?` by the no-read branch's own definition ("a well-formed citation this analysis did not open stays `reported-by-delegate` and keeps the `?`") — it does not fall through to an unlabelled state. Case 5's end state is `read-at-source`, unchanged, because it was already resolved on the earlier pass this step is not re-litigating.

Every end state names a label the provenance table defines: `read-at-source`, `reported-by-delegate`, and `unverified` are exactly the table's three rows.

### (c) No case barred from resolution by an exclusion

After the narrowing (`and in which the asserted figure or wording was located`), the exclusion's first limb reads: "A ground truth whose cited source this analysis has already opened and in which the asserted figure or wording was located ... do not earn a read." Case 2 (source opened, figure NOT located) does not satisfy this limb — the "and in which ... was located" clause is false for case 2 — so case 2 is **not** barred by the exclusion. It also is not barred by the second limb (MEDIUM/LOW-confidence), since case 2 is defined as being in the HIGH-confidence population.

The relationship between the exclusion and the population selector: the population selector *itself* already excludes any already-opened source ("whose cited source this analysis has **not yet opened**"), so a ground truth that has already been opened (whether or not the figure was located) is outside the population this step processes at all — it never reaches the branches in a later pass. This makes the exclusion clause's practical effect, after the population selector, **redundant for the purpose of blocking a re-read**: the population selector alone already prevents re-reading anything already opened. I did find this redundancy while tracing case 5 through both the selector and the exclusion. The narrowing is still required, though, for a reason independent of read-blocking: the exclusion clause is also read as a *reader-facing instruction about what "do not earn a read" is for* — the verification report's `missing:` item 2 explicitly requires the exclusion be narrowed so it "does not swallow the new branch," and that requirement is about what the sentence *asserts*, not only about what the population selector *does*. An un-narrowed exclusion sentence, read on its own, tells a reader "a ground truth whose source is already opened does not earn a further read" without qualifying that the source's content was ever confirmed — which invites exactly the misreading CR-01 named: that an opened-but-unresolved ground truth is done and needs no failure record. The narrowing closes that misreading at the prose level even though the population selector already closes it at the mechanism level. Both the item-2 requirement and the misreading-prevention argument hold regardless of the selector redundancy, so the narrowing is required either way.

## 3. Three-Surface Coherence Table (Task 2, action step 4)

Every cell is a verbatim quote from the corresponding EMITTED file.

| Outcome | Body branch (`first-principles/agents/first-principles.md`) | Provenance table row | Rubric Fix branch (`first-principles/agents/references/validation-rubric.md`) |
|---|---|---|---|
| Source opens, figure located | "the ground truth becomes `read-at-source`, drops the `?` if it carried one, and its read-location — the page, table, section, or quoted passage — is recorded" | `read-at-source` row: "The specific figure, table, passage, or clause was located and read..." | (implicit — this is the acquisition branch's success path; the Fix note's "Branch one, preferred: acquire the evidence" leads here) |
| Source opens, figure NOT located | "the step writes a Phase 3 failure record with the reason `citation does not support the claim` and marks that ground truth `?`, assigning the suffix if it did not already carry one, so it lands on the `unverified` label" | `unverified` row: "No source was located at all, or the cited source was opened and the asserted figure or wording was not found in it." | "taken only when the source cannot be opened **or opens without containing the asserted figure or wording**" / "the downgrade branch still requires the Phase 3 failure record, which source and why unreachable, or `citation does not support the claim`" |
| Source cannot be opened | "the step writes the **Phase 3 failure record**: which source and why unreachable — 404, paywall, no network, path not found, ambiguous citation — and mark that ground truth `?`, assigning the suffix if it did not already carry one" | `unverified` row (same row as above — "no source was located at all" is the unreachable case) | "taken only when the source cannot be opened" / "the downgrade branch still requires the Phase 3 failure record, which source and why unreachable" |

All three cells are filled for all three outcomes; no cell is blank.

## 4. Control Roster and Non-Vacuity Evidence

### Final roster (a)-(x), 24 controls, live run after Task 4

```
(a) positive control — body: PASS (0 failures)
(b) positive control — rubric: PASS (0 failures)
(c) correctly failed (3 failure(s))
(d) correctly failed (2 failure(s))
(e) correctly failed (1 failure(s))
(f) correctly failed (1 failure(s))
(g) correctly failed (1 failure(s))
(h) correctly failed (2 failure(s))
(i) correctly failed (3 failure(s))
(j) correctly failed (1 failure(s))
(k) correctly failed (3 failure(s))
(l) correctly failed (1 failure(s))
(n) correctly failed (1 failure(s))
(o) correctly failed (1 failure(s))
(p) correctly failed (1 failure(s))
(q) correctly failed (1 failure(s))
(r) correctly failed (1 failure(s))
(s) correctly failed (1 failure(s))
(t) correctly failed (1 failure(s))
(u) correctly failed (1 failure(s))
(v) correctly failed (1 failure(s))
(w) correctly failed (1 failure(s))
(x) correctly failed (3 failure(s))
(m) dispatch control: PASS — main(['--self-test']) reaches this block end-to-end
check-act-limb --self-test: PASS
```

24 unique control labels; zero occurrences of `WRONGLY PASSED` or `WRONG reason` (confirmed by `grep -E "WRONG|FAIL"` over captured output finding nothing). Note control (k)'s failure count rose from 2 to 3 at Task 4's checkpoint — expected, see below.

### Intermediate roster: end of Task 3 (22 controls, (a)-(v))

```
(a) positive control — body: PASS (0 failures)
(b) positive control — rubric: PASS (0 failures)
(c) correctly failed (3 failure(s))  ... (d)-(s) unchanged from 01-03's 19-control roster ...
(t) correctly failed (1 failure(s))
(u) correctly failed (1 failure(s))
(v) correctly failed (1 failure(s))
(m) dispatch control: PASS
check-act-limb --self-test: PASS
```

### Intermediate roster: end of Task 4 (24 controls, (a)-(x))

Identical to the final roster above (Task 4 is the last code-editing task; Task 5 makes no further changes).

### Raw non-vacuity output — Task 3 controls (t), (u), (v)

```
=== real body (unmutated) ===
failures on real body: []

=== (t) fixture: strip _B12_NOT_FOUND_BRANCH ===
failures: ['Body-6 (ACT-03, failure path): step paragraph missing not-found branch']
contains not-found branch: True

=== (u) fixture: strip _B13_EXCLUSION_RESOLVED ===
failures: ['Body-5 (ACT-04, the bound): step paragraph missing resolved-state exclusion']
contains resolved-state exclusion: True

=== (v) fixture: strip _B14_TABLE_NOT_FOUND from table block ===
failures: ["Body-12 (ACT-02/ACT-03, table coverage): provenance table's `unverified` row is missing the not-found test"]
contains Body-12: True
```

### Raw non-vacuity output — Task 4 controls (w), (x)

```
=== real rubric (unmutated) ===
failures: []

=== (w) fixture: strip _R6_DOWNGRADE_SCOPE ===
failures: ['Rubric-6 (ACT-05, downgrade scope): Fix note paragraph missing downgrade scope']
contains Rubric-6: True

=== (x) fixture: gutted-but-relocated Fix note (CR-02) ===
AFTER (Task 4, block-scoped) failures: ['Rubric-3 (ACT-05, branches and preference): Fix note paragraph missing acquire branch, downgrade branch, stated preference', 'Rubric-5 (CR-05, pointer use): Fix note paragraph missing step pointer, failure-record pointer', 'Rubric-6 (ACT-05, downgrade scope): Fix note paragraph missing downgrade scope, shared reason token']
contains Rubric-3: True

BEFORE (pre-Task-4, slice-scoped) failures on the SAME fixture: []
```

**The `[]` → `Rubric-3` contrast** is the direct proof that CR-02 is closed rather than restated: the identical gutted-but-relocated fixture — built the same way the verifier's own `01-VERIFICATION.md` reproduction built it (replace the Fix-note block with a stub keeping only its lead, scatter the five required phrases as noise elsewhere in the Criterion 3 slice) — passed cleanly under the pre-Task-4 slice-scoped logic and now fails naming `Rubric-3` under the paragraph-scoped logic.

### PRE-01-04 REGRESSION FIXTURE (proves the whole re-anchoring is a genuine backstop)

Built by removing the not-found sentence entirely and reverting the exclusion to its un-narrowed (X4) form, against the real emitted body:

```
pre-01-04 regression fixture failures:
 - Body-5 (ACT-04, the bound): step paragraph missing resolved-state exclusion
 - Body-6 (ACT-03, failure path): step paragraph missing not-found branch, not-found assignment verb

names not-found branch: True
names resolved-state exclusion: True
```

A gate that passes the prose the verifier found broken has not closed the gap; this fixture confirms `_check_body_text()` FAILS on the exact pre-01-04 shape, naming both stripped properties by name.

### Anchor separation, proven in the gate

```
control (o) strip _B6B_ASSIGNMENT failures: ['Body-6 (ACT-03, failure path): step paragraph missing assignment verb']
strip _B12B_NOT_FOUND_ASSIGN failures: ['Body-6 (ACT-03, failure path): step paragraph missing not-found assignment verb']
```

Stripping `_B6B_ASSIGNMENT` alone (control (o)) produces `assignment verb` and never `not-found assignment verb`; stripping `_B12B_NOT_FOUND_ASSIGN` alone produces `not-found assignment verb` and never the bare `assignment verb`. The two failure branches remain independently testable — the A6/A14 anchor separation (`mark` vs `marks`) holds in the gate, not just in the prose.

### Existing rubric controls survive the CR-02 scope narrowing

```
(k) strip _R1_FIX_LEAD entirely:
  failures: ['Rubric-2 (ACT-05): Fix note lead occurs 0 time(s) in the Criterion 3 slice, expected exactly 1',
             'Rubric-2 (ACT-05): Fix note lead occurs 0 time(s) in the whole file, expected exactly 1',
             'Rubric-3/5/6 (CR-02, block scope): Fix note paragraph occurs 0 time(s) in the Criterion 3 slice, expected exactly 1 — cannot check branches, preference, pointers, or downgrade scope']
  contains 'Fix note lead': True   (control (k) still correctly fails, does NOT raise — the zero-block path)

(l) strip _R4_PREFERENCE whole-file:
  failures: ['Rubric-3 (ACT-05, branches and preference): Fix note paragraph missing stated preference']
  contains 'stated preference': True

(s) strip _R5_STEP_POINTER whole-file:
  failures: ['Rubric-5 (CR-05, pointer use): Fix note paragraph missing step pointer']
  contains 'Rubric-5': True
```

All three confirmed by running, not reading. Control (k)'s failure count moved from 2 to 3 (the new zero-block Rubric-3/5/6 failure joined Rubric-2's two pre-existing ones) — an expected, not a wrong-reason, change.

## 5. WR-08 Closure and the Re-Run Gate-Coupling Sweep

### WR-08 duplicate-block demonstration

Two complementary scratch demonstrations, neither touching a repository file:

**Test A — the literal WR-08 defect scenario** (a block's text also appears in an *earlier* phase): duplicated the provenance-table block into the region before `### Phase 3: Establish Ground Truths` and ran `_mutate_body_removing_from_block`. Result: the earlier-phase copy survives untouched (`_B14_TABLE_NOT_FOUND` still present in it) and the Phase-3 copy has the target correctly removed (`_B14_TABLE_NOT_FOUND` absent from the Phase 3 slice afterward) — confirming the region-anchored splice mutates the *correct* occurrence even when a textual duplicate exists outside the region, which the old whole-file-`replace` implementation could not guarantee.

**Test B — the uniqueness guard** (a block duplicated *inside* the Phase 3 region, making it non-unique where the helper is required to anchor): duplicated the provenance-table block a second time inside the Phase 3 slice. Result:

```
Test B (duplicate within Phase 3 region): AssertionError raised as expected:
expected exactly one block containing '| **unverified** |' inside the Phase 3 region
while building a fixture, found 2
```

Confirms `_mutate_body_removing_from_block` raises `AssertionError` when the located block is not unique inside the Phase 3 region, matching the file's existing fixture-guard idiom rather than silently mutating an arbitrary match.

### Re-run gate-coupling sweep (Task 3 step G), live measured values

| # | Assertion | Live measured value | Disturbed by this repair? |
|---|-----------|---------------------|---------------------------|
| Body-2/3 | step lead count, slice and whole-file | 1, 1 | No |
| Body-4..9 | step paragraph block count | 1 | No — new sentence stayed inside the single-line block |
| Body-10 | `**Phase 3 verification step**` slice count | 1 | No |
| Body-10 | `**Phase 3 failure record**` slice count | **1** | No — satisfied without widening, because the not-found branch references the artifact in plain form (A10B) |
| Body-9 | `HIGH-confidence derivation chain` slice count | 2 | No — floor check, monotone-safe under addition |
| Body-12 (NEW) | provenance-table block count | 1 | New assertion, recorded here as the sweep requires — this is the one new count-bearing coupling this repair introduces |
| Rubric-2 | Fix-note lead count, slice and whole-file | 1, 1 | No |
| `_mutate_body_removing_from_block` (fixture helper) | block count inside its located region | 1 (existing constraint, now region-scoped rather than whole-file-scoped) | Strengthened, not newly introduced — same category as before |

Measurement confirming Body-10 needed no widening:

```
Body-2/3 step lead in slice: 1
Body-2/3 step lead whole file: 1
Body-4..9 paragraphs (block count): 1
Body-10 step name slice count: 1
Body-10 failure record slice count: 1
Body-9 shared population count: 2
Body-12 table blocks count: 1
Rubric-2 Fix lead in slice: 1
Rubric-2 Fix lead whole file: 1
```

**Conclusion:** no new count-bearing coupling was introduced beyond Body-12's block-count guard, exactly as the plan's `<interfaces>` GATE-COUPLING SWEEP predicted before any prose was written.

## 6. Battery Verdict and Environment-vs-Real Discrimination

```
FIREWALL: RED (1 gate(s) failed; 16/17 passed)
```

Full gate list from this run: `DUAL-04` PASS, `GATE-02-v8.5` PASS, `STEP0-06` PASS, `STEP0-08` PASS, `VAL-01` PASS, `VAL-02` PASS, `VAL-03` **FAIL**, `VAL-04` PASS, `VAL-05` PASS, `VERSION-01` PASS, `GATE-01` PASS, `BATT-06` PASS, `TRACE-03` PASS, `COLLIDE-01` PASS, `QUAL-01` PASS, plus the two report-only inline checks `INVARIANT-CHECK` and `FROZEN-EVIDENCE`, both PASS. Byte-identical to the baseline recorded in `01-VERIFICATION.md`'s Behavioral Spot-Checks table and reconfirmed unchanged by `01-03-SUMMARY.md`.

**Environment-vs-real discrimination, performed not assumed:**

- `python3 scripts/check-links.py --self-test` → exit 0
- `python3 scripts/check-links.py` → exit 0, `check-links: PASS (237 markdown links + 6 namespace refs across 125 files)`
- `python3 -m pytest scripts/check-links_anchors_test.py -q` → exit 1, `/usr/bin/python3: No module named pytest`
- `uv run --with pytest python3 -m pytest scripts/check-links_anchors_test.py -q` → exit 0, `8 passed in 0.08s`

Only the bare `python3 -m pytest` invocation fails, and only for a missing-module reason; the identical anchor suite passes under the documented workaround. This is the known, pre-existing SHIP-06 environment gap (system `python3` lacks `pytest`), not a content defect — confirmed by discrimination, not assumed from the verdict line alone.

## 7. `git diff --stat` for the Whole Plan

```
 first-principles/agents/first-principles.md        |   4 +-
 .../agents/references/validation-rubric.md         |   2 +-
 scripts/check-act-limb.py                          | 253 +++++++++++++++++----
 shared/spine/SKILL-body.md                         |   4 +-
 shared/spine/references/validation-rubric.md       |   2 +-
 5 files changed, 221 insertions(+), 44 deletions(-)
```

Exactly the five files named in the plan's `files_modified` frontmatter — no more, no less. `python3 scripts/check-version-stamps.py` reports 17 stamps, all `8.17.5`, unchanged from before this plan. `git diff --stat -- .claude-plugin/ shared/spine/SKILL.meta.yml shared/skills/` is empty (VERSION-01, hard constraint 2). `git diff --quiet scripts/check-firewall-battery.sh` exits 0 and `grep -c "check-act-limb" scripts/check-firewall-battery.sh` is 0 (hard constraint 3 — HARN-01 stays unregistered).

## 8. `<deferred>` Dispositions (carried forward with owners)

**Closed in this plan, against an earlier deferral:**
- **CR-02** (`_check_rubric_text`'s Rubric-3/Rubric-5 slice-scoped, false PASS on a gutted-but-relocated Fix note) — closed by Task 4, reproducing the verifier's own fixture and inverting its `[]` result.
- **WR-08** (`_mutate_body_removing_from_block` replaces the first whole-file occurrence, not the anchored one) — closed by Task 3, region-anchoring the helper to the Phase 3 byte range.

**Deferred — owner: Phase 4 (Ship) / HARN-04** (unchanged by this plan):
- **WR-01** — the HIGH-confidence trigger is a self-declared property. Design question about literal-anchor gates, inherited verbatim from ROADMAP/ACT-04, both VERIFIED.
- **WR-02** — eight HARN-01 assertion sites have no negative control. This plan adds no new uncontrolled assertions; every new check (Body-5's fourth item, Body-6's two new items, Body-12, Rubric-6) ships with its own control.
- **WR-03** — inverting the step's operative clause is a false PASS. Known literal-anchor-gate limitation shared with `check-agent.py`.
- **CR-01 of the pre-01-03 review** (self-test `_check_negative` matches a generic substring) — this plan's five new controls (t)-(x) are locally immune (unique substrings); the audit of the pre-existing controls stays deferred as a single coherent piece of work.
- **WR-06** — HARN-01 registered nowhere (no CI job, absent from the battery and `CLAUDE.md`'s gate inventory). Not a defect; ROADMAP scopes registration to HARN-04/Phase 4; hard constraint 3 forbids doing it here.
- **WR-10** — `Rubric-4` can never be the sole failure and silently vacates when a heading moves. Untouched by this plan.
- **IN-01..IN-06** — cosmetic/convention-level findings (constant numbering vs check numbering, live-derived vs `tempfile` fixtures, a stale `_run_self_test` docstring — still says "controls a-s", deliberately left unchanged per this plan's own scope discipline — the rubric's missing `SKILL.md` attribution, the Fix note's long line against a ~95-column file — now marginally longer after Task 2's edits, accepted deliberately so the diff stays legible — bare `AssertionError` in fixture builders).

**Accepted — no owner, no task** (unchanged by this plan):
- **WR-07** — the Fix note is a what-to-fix instruction in a file whose scope block says remediation lives in `SKILL.md`. Resolving it requires a scope decision above a gap-closure plan; Task 2 added no new remediation prose.
- **WR-09** — reviewer-facing rationale shipped into the agent's executable instructions (the "verification reads compete with the Self-Audit Gate" sentence, from 01-03). Accepted; hard constraint 5 capped this plan's addition at one operative sentence with no rationale prose, so the paragraph did not grow further in the direction WR-09 objects to.
- **SHIP-06 / VAL-03's missing `pytest`** — a real, tracked requirement owned by Phase 4. This plan discriminates it (proves it is the environment gap, not a content defect) per Task 5, never fixes it (would violate hard constraint 3 and pre-empt SHIP-06).

## Decisions Made

- The not-found branch's assignment verb is deliberately `marks` (plural), not `mark`, so it never collides with the unreachable branch's `mark that ground truth `?`` — control (o) keeps testing the unreachable branch alone and the new control (t) keeps testing the not-found branch alone, confirmed by direct execution (Section 4, "Anchor separation").
- The not-found branch references the Phase 3 failure record artifact in its plain, unbolded form (A10B) rather than redefining it — Body-10 requires the bold form to occur exactly once in the Phase 3 slice, and this task's own final run would fail on a second bold occurrence. Confirmed by direct measurement (`**Phase 3 failure record**` count = 1) rather than by code inspection.
- Tasks 3 and 4 were kept as the plan specified — one gate-editing task per `_check_*_text()` function — so each reaches an independent green checkpoint and no single task carries the Body-10 exact-count coupling risk that made the previous plan revision self-defeating.

## Deviations from Plan

None — plan executed exactly as written. All anchors (A1-A16), all deleted strings (X4, X5), all new gate checks (Body-5's fourth item, Body-6's two new items, Body-12, Rubric-6, and the CR-02 narrowing of Rubric-3/5), and all five new self-test controls (t)-(x) match the plan's `<interfaces>` and each task's `<action>` specification verbatim, confirmed by direct grep/execution against both `shared/` and the emitted tree at every acceptance-criteria checkpoint before each task's commit.

## Issues Encountered

None beyond the pre-existing, out-of-scope `pytest`-missing environment gap already documented in `01-01-SUMMARY.md`, `01-02-SUMMARY.md` and `01-03-SUMMARY.md` (VAL-03's sole sub-check failure) — reconfirmed unchanged by Task 5's discrimination sweep, per hard constraint 6.

## Known Stubs

None — no UI, no data-fetching components; this plan edits Markdown prompt specification files and a stdlib-only Python validation script, and regenerates the derived tree.

## Threat Flags

None beyond this plan's own `<threat_model>` (T-01-01, T-01-02, T-01-05, T-01-06, T-01-07, T-01-08, T-01-09, T-01-10, T-01-11, T-01-SC, T-01-INFO), all mitigated as designed:
- T-01-01 (prompt injection via WebFetch/Read) — anchor A8 and the injection-containment tail survive byte-unchanged (confirmed present exactly once in both files); the not-found branch is written as a recording action only, prescribing no action derived from the source's contents.
- T-01-02 (turn-budget DoS) — the selector (A2/A3) is byte-unchanged; the exclusion is narrowed, not widened; rationale A11 retained verbatim; no numeric read cap introduced (confirmed by regex sweep over the Phase 3 slice).
- T-01-05 (hand edit to the emitted tree) — `shared/` edited only; `sync-content.py --write` produced no further change on Task 5's re-run; every prose acceptance criterion asserted against both `shared/` and the emitted mirror.
- T-01-06 (gate assertion-set vacuity) — controls (t)-(x) each demonstrated non-vacuous by execution against the real emitted file (Section 4); the pre-01-04 regression fixture fails naming both stripped properties.
- T-01-07 (fixture mutation landing in the wrong region, WR-08) — closed; demonstrated by both Test A (correct-region mutation despite an outside duplicate) and Test B (raise on an inside duplicate).
- T-01-08 (gutted-but-relocated rubric Fix note passing the gate, CR-02) — closed; control (x) reproduces the verifier's exact fixture and now fails, with the `[]` → `Rubric-3` contrast recorded.
- T-01-09 (repudiation — an opened-but-unsupporting citation leaves no trace) — this was the substance of the gap; A13/A14/A10B/A16 together give the outcome a named reason, an assignment, an artifact reference, and a table-defined label.
- T-01-10 (VERSION-01 stamp drift) — `check-version-stamps.py` confirms all 17 stamps unchanged at `8.17.5`; scoped `git diff --stat` empty under the three protected paths.
- T-01-11 (environment RED misread as content RED or vice versa) — Section 6's discrimination performed the required sub-command isolation and `uv run` cross-check rather than assuming the verdict line's meaning.
- T-01-SC (package installs) — not applicable; no packages installed. `uv run --with pytest` is a diagnostic of an already-in-CI dependency, run in a throwaway environment, changing no lockfile.
- T-01-INFO — not applicable; no credential, secret, PII, or user data touched.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- The failed derived truth #6 from `01-VERIFICATION.md` is now TRUE and demonstrated (Section 2): the Phase 3 acquisition step's outcome branches partition its declared population — every ground truth the step admits reaches a provenance-label change or a Phase 3 failure record plus the `?`, none falls through, none is barred from resolution by the exclusion.
- ROADMAP Phase 1 Success Criteria 1-5 are all still TRUE: ACT-01 (unchanged, non-regressed), ACT-02/ACT-03 (repaired again, now exhaustive), ACT-04 (unchanged, non-regressed), ACT-05 (widened to cover both failure modes), HARN-01 (green live and in self-test with 24 controls).
- CR-02 and WR-08 are closed with recorded before/after evidence (Sections 4 and 5). WR-01, WR-02, WR-03, WR-06, WR-10, IN-01..IN-06, and the pre-01-03 review's generic-substring finding remain open with Phase 4/HARN-04 as stated owner. WR-07, WR-09, and SHIP-06 are accepted with stated reasoning (Section 8).
- `scripts/check-act-limb.py` stays unregistered in `scripts/check-firewall-battery.sh` (confirmed: `grep -c "check-act-limb" scripts/check-firewall-battery.sh` = 0, file untouched) — Phase 4/HARN-04 owns registration and the tally bump from 17.
- Phase 1 (Evidence Acquisition) is closed pending the phase-level re-verification this SUMMARY feeds: all four plans (01-01, 01-02, 01-03, 01-04) executed and committed; the derived truth that was FAILED in `01-VERIFICATION.md` is now backed by repaired, gate-locked, non-vacuously-tested prose.

---
*Phase: 01-evidence-acquisition*
*Completed: 2026-08-27*

Note: `.planning/` is gitignored per CLAUDE.md — this summary is not published to the public repo.

## Self-Check: PASSED

- FOUND: shared/spine/SKILL-body.md
- FOUND: shared/spine/references/validation-rubric.md
- FOUND: first-principles/agents/first-principles.md
- FOUND: first-principles/agents/references/validation-rubric.md
- FOUND: scripts/check-act-limb.py
- FOUND: .planning/phases/01-evidence-acquisition/01-04-SUMMARY.md
- FOUND commit: 00d9993 (Task 1)
- FOUND commit: 7d76886 (Task 2)
- FOUND commit: 20cc0c5 (Task 3)
- FOUND commit: 03fa674 (Task 4)
