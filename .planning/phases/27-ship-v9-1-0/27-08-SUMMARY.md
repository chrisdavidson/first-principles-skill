---
phase: 27-ship-v9-1-0
plan: 08
subsystem: release-act-three-changelog-entry
tags: [release, changelog, D-11, D-13, D-16, disclosed-limits, REL-08]

dependency-graph:
  requires:
    - "27-04: the pre-release recurrence reading, whose recurrence-reading surface this entry
      cites without stating a digit"
    - "27-05: release act one (17 stamps at 9.1.0)"
    - "27-06: release act two (matrix rows + headline sweep, the '18' CANNOT-REACH deviation this
      entry names in its Containment reach bullet)"
    - "27-07: REL-06's direct count and the D-15 fence adjudication (40/40 HELD, 0 exceptions --
      so no fence-break sentence is added to this entry)"
  provides:
    - "CHANGELOG.md's [9.1.0] entry, committed alone in one commit, citing
      docs/conformance-baseline.md's recurrence-reading section rather than stating a recurrence
      digit"
  affects:
    - "plan 27-09 (the post-arm reading) -- if the trip fires post-arm, a dated addendum is
      appended to this entry per D-16; this plan's commit is otherwise final"

tech-stack:
  added: []
  patterns:
    - "in-process test of drafted CHANGELOG prose against _scan_text_for_literal_hits() before
      writing to disk (Phase 26/27-01 precedent), plus a word-boundary regex check isolating the
      exact sentence carrying the recurrence-reading pointer for the no-digit/no-characterising-word
      acceptance criterion"

key-files:
  created: []
  modified:
    - CHANGELOG.md

decisions:
  - "The D-13 candidate list names CR-01, CR-03 and P-CR-01 (not CR-02) as v9.0.0's carried
    exceptions to disclose; CR-02 is still named in the Diagnosis bullet (it is one of the three
    dispositions PROSE-04 requires), but its own current-disposition text was already fully stated
    at [9.0.0] and needed no new disclosure beyond restating its (unchanged) routing-based
    disposition."
  - "CR-01's disposition is stated as CLOSED (not merely 'accepted with a bound') because Phase 25
    demonstrated the chain-terminus arm catching it by mutation -- a stronger, later fact than the
    diagnosis page's own 2026-09-09 dated reading, stated in the entry rather than on that page,
    which this milestone does not reopen as a region host."
  - "27-06's own deviation (the new '18' CANNOT-REACH containment-ledger entry) is disclosed by
    shape, not by digit -- 'a fresh entry... a currently-correct digit with no corroborating
    generated field' -- rather than restating the ledger's current count, per D-13's
    cite-don't-restate instruction for ledger deltas."
  - "No fence-break sentence was added: 27-07-SUMMARY.md's adjudication found 0
    HELD-WITH-DISCLOSED-EXCEPTION sites (40/40 HELD clean), so per this plan's own acceptance
    criterion ('if 27-07 recorded none, the summary states that and no fence sentence is added')
    that fact is recorded here, not fabricated into the CHANGELOG as an empty disclosure."

requirements-completed: []

metrics:
  duration: "~1h15m"
  completed: "2026-09-11"
---

# Phase 27 Plan 08: Release Act Three -- the [9.1.0] CHANGELOG Entry Summary

Drafted and committed the `[9.1.0]` CHANGELOG entry alone, in the `[9.0.0]` house form: a headline
paragraph naming the milestone and all five requirement groups (all 18 IDs), one `### Added` bullet
per group each carrying a `**Disclosed limits --**` clause where its own claim would otherwise read
wider than what was measured, and a release-act sentence citing
`docs/conformance-baseline.md`'s `recurrence-reading` section with no recurrence digit and no
characterising word. REL-08 is **not** ticked by this plan -- its own text names verification
measured against product recurrence, and the post-arm half of that measurement is plan 27-09's job.

## What was built

**Task 1 -- drafted and tested the entry before writing it to disk.** Read the `[9.0.0]` entry's
house form (headline paragraph, one `### Added` bullet per requirement group, a `**Disclosed
limits --**` clause per bullet), `docs/PROCESS.md`'s frozen-historical-count paragraph (lines
149-153, the D-11 exemption), `docs/conformance-baseline.md`'s `## recurrence-reading` section
(the pointer target), `docs/gates/CONF-SURFACE.md`'s bounds (13) and (14), plan 27-07's fence
adjudication table (40/40 HELD, 0 exceptions), plan 27-06's summary (the `18` CANNOT-REACH
deviation, current containment-ledger value 21), and `docs/v9.1-claim-containment-diagnosis.md`
section 3 (CR-01/CR-02/CR-03's dispositions as recorded 2026-09-09, before Phase 25's later
closure of CR-01).

Read the live coverage headline directly (`check-traceability.py --describe`'s `coverage_headline`
field: `217 reproducible / 106 audit-only / 0 gap / 323 total` / `217/106/0/323`) rather than
trusting the CONTEXT.md draft-time figure, and transcribed it byte-for-byte into the headline
paragraph. Confirmed the containment ledger's live value is `21` (`_CONTAINMENT_LEDGER_MAX` in
`scripts/gen-gate-docs.py`), not the `20` CONTEXT.md's D-13 text names -- CONTEXT.md was written
before plan 27-06's own deviation moved it, so the entry cites the ledger's page rather than
restating either figure, sidestepping the staleness rather than transcribing a value already known
to be about to move again.

Drafted the entry with five `### Added` bullets -- **Diagnosis** (PROSE-01..04), **Containment
reach** (CONTAIN-01..04), **The generalized rule and generated narrative regions** (NARR-01,
NARR-02), **The ratchets** (RATCHET-01..04), **The release act itself** (REL-05..08) -- each naming
its own requirement IDs by range (matching the `[9.0.0]` entry's own `CONF-11 through CONF-13`
precedent shape) and each carrying its own `**Disclosed limits --**` clause. Tested the full draft
in-process against `scripts/gen-gate-docs.py`'s `_scan_text_for_literal_hits("CHANGELOG.md",
text)` (correct `(relpath, text)` argument order, per the 27-06 near-miss precedent) before writing
anything to disk.

**Literal-scan hit classification (acceptance criterion: the recurrence-digit class must be
empty).**

| # | Hit text | Classification | Disposition |
|---|---|---|---|
| 1 | `one new entry` (containment-ledger deviation sentence) | restated moving count | **reworded** -- "one" removed, replaced with "a fresh entry", eliminating the spelled-out-number-adjacent-to-count-noun shape entirely |
| 2 | `mutation proof (two` (RATCHET-01's four-arm demonstration) | frozen historical | **kept** -- a closed, dated description of this milestone's own already-run mutation demonstration (four arms: two host surfaces + the census arm + the unmutated arm), matching the CHANGELOG's own established per-release convention (e.g. `[8.20.0]`'s "Three fault injections", `[8.18.0]`'s "three new gates") |
| 3 | `17 hand-maintained version stamps` | frozen historical | **kept** -- `17` is stated unfenced in this exact phrasing at nine other points across `CHANGELOG.md`'s history (`/usr/bin/grep -n "17 " CHANGELOG.md`, verified), including the file's own preamble two lines above the first entry; not a moving count for this milestone, a standing project constant restated in every release's own dated language |

**Recurrence-digit class: 0 members** (no hit is a recurrence-reading figure; the recurrence
sentence itself was never given to the scanner because it carries no digit-adjacent count noun in
the first place -- confirmed separately below).

**Recurrence-sentence check (acceptance criterion, checked directly rather than assumed).** Isolated
the exact sentence carrying the pointer to `docs/conformance-baseline.md`'s `recurrence-reading`
section:

> "both instruments' readings (a frozen-scanner arm and an independent two-reader prose arm), at
> both the pre-release and post-release timing, are published unreconciled in
> `docs/conformance-baseline.md`'s `recurrence-reading` section rather than restated here"

`re.findall(r'\d', sentence)` → `[]` (zero Arabic digits). `re.search(r'\b(clean|none|zero|low|reduced)\b', sentence, re.IGNORECASE)`
→ no match on any of the five banned words, word-boundary-checked (a naive substring check without
word boundaries had falsely flagged "low" inside "followed" on a first pass -- corrected before
being treated as a result).

**D-13 candidate disposition table** (every discretionary disclosure candidate the plan named,
whether it was included, and why):

| Candidate | Included? | Where | Reason |
|---|---|---|---|
| Bound (13)'s two cannot-reach residues (`tests/premise-rejection-catalog.md` G3 target, `docs/COMPONENT-DIAGRAM.md` Mermaid label) | **Yes** | Containment reach bullet AND the generalized-rule bullet | Mandatory per the plan's own rule: the generalized-rule bullet states "**zero** non-exempt hits" (a "driven to zero" claim), which would overstate without this residue; named a second time in Containment reach because that bullet's own reach claim is the residue's direct subject |
| Plan 27-06's disclosed bound (14) (HEADLINE-LOCK verifies five surfaces, `--write` produces three) | **Yes** | Release-act bullet | Mandatory per the plan's instruction; REL-07's own clause ("produced by HEADLINE-LOCK's sweep, not a hand edit") would read wider than the mechanism without it |
| Deferred-literal ledger delta (181 → 180) and containment ledger (26 → 20 → 21), with RATCHET-02's growth-only/size-only bound | **Yes, cited not restated** | Containment reach bullet | Included as instructed ("cited to `docs/gates/CONF-SURFACE.md`'s published section rather than restated") -- no digit for either ledger's current value appears in the entry; the containment ledger's own growth during this release is named by shape ("a fresh entry... a currently-correct digit with no corroborating generated field") rather than by count, since the count itself was mid-move at CONTEXT.md's own draft time (20 there, 21 live) and citing the page sidesteps stating a number this entry could go stale on |
| v9.0.0's carried exceptions (CR-01, CR-03, P-CR-01) and their current disposition | **Yes** | Diagnosis bullet | Included per the plan's explicit instruction; CR-01 is now stated CLOSED (Phase 25's mutation-demonstrated chain-terminus arm), a fact more recent than the diagnosis page's own 2026-09-09 dated reading; CR-03 remains accepted-with-bound (nothing changed); P-CR-01 (never named in the `[9.0.0]` entry itself, since it was found by a post-review after that entry shipped) is disclosed here for the first time, as CLOSED |
| Every `HELD-WITH-DISCLOSED-EXCEPTION` fence site from plan 27-07 | **No -- because there are none** | -- | Per this plan's own acceptance criterion: "if 27-07 recorded none, the summary states that and no fence sentence is added." 27-07-SUMMARY.md's adjudication table shows 40/40 sites HELD, 0 `HELD-WITH-DISCLOSED-EXCEPTION`, 0 misclassifications -- stated here, not fabricated into the CHANGELOG as a disclosure with nothing to disclose |

## Deviations from Plan

None -- plan executed exactly as written. No source file outside `CHANGELOG.md` was touched by
either task.

## Verification (observed this session)

- `/usr/bin/grep -n "^## \[9.1.0\]" CHANGELOG.md` → `14:## [9.1.0] — 2026-09-11`, exactly one
  match, positioned immediately above `## [9.0.0]` (observed).
- `/usr/bin/grep -n "recurrence-reading" CHANGELOG.md` → one match, inside the release-act bullet's
  pointer sentence (observed).
- `/usr/bin/grep -c "Disclosed limits" CHANGELOG.md` → `13` (9 pre-existing in `[9.0.0]` + 4 in
  `[9.1.0]` that do not wrap "Disclosed limits" across a physical line break; the fifth bullet's
  own Disclosed-limits clause wraps mid-phrase across two lines, matching an identical wrap
  already present in the shipped `[9.0.0]` entry at line 52 -- confirmed a pre-existing, accepted
  formatting convention in this file, not a defect) (observed).
- `check-traceability.py --describe`'s live `coverage_headline` → `{'slash': '217/106/0/323',
  'prose': '217 reproducible / 106 audit-only / 0 gap / 323 total'}`, transcribed byte-for-byte
  into the headline paragraph (observed, both before and after commit).
- `_CONTAINMENT_LEDGER_MAX` in `scripts/gen-gate-docs.py` → `21` (live, confirmed via direct grep
  before drafting the Containment reach bullet) (observed).
- In-process `_scan_text_for_literal_hits("CHANGELOG.md", draft_text)` → 3 hits before rewording,
  2 after (the "one new entry" hit reworded away); both survivors classified frozen-historical
  above; recurrence-digit class 0 members (observed, both readings transcribed above).
- Recurrence-pointer sentence isolated and checked: `re.findall(r'\d', sentence)` → `[]`;
  word-boundary regex for `clean|none|zero|low|reduced` → no match (observed, transcribed above).
- `git status --porcelain` before commit → ` M CHANGELOG.md`, nothing else (observed).
- `git diff --stat -- docs/conformance-baseline.md docs/data/conformance.json` → empty, both files
  untouched (observed).
- `python3 scripts/report-conformance.py --check` → `report-conformance: PASS — no drift`, exit 0,
  run before the commit against the state plan 27-04 already left current, no regeneration run in
  this plan (observed).
- `sh .githooks/pre-commit` → exit 0 (the printed `DRIFT: /tmp/.../artifact.md` block is Gate 2's
  own `report-conformance.py --self-test` exercising its mutation-detection control on a disposable
  scratch fixture, not a real failure -- confirmed by the hook's own exit code and by the
  subsequent `report-conformance: PASS` / `gen-gate-docs: SELF-TEST PASS` lines that follow it)
  (observed, both pre- and post-commit runs).
- Commit `de185245af7ec7192040f389d4385855fbb00b81` (`de18524`), without `--no-verify` (observed).
- `git show --stat --format= HEAD` → `CHANGELOG.md | 102 +++...`, exactly one file (observed).
- `git diff --diff-filter=D --name-only HEAD~1 HEAD` → empty, no unexpected deletions (observed).
- `git diff HEAD~1 HEAD -- docs/conformance-baseline.md docs/data/conformance.json` → empty
  (observed).
- `python3 scripts/gen-gate-docs.py --check` → `harvested 22/22 expected script-backed entries (22
  total)`, exit 0 (observed).
- `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (26/26)` (observed, run after the
  commit).
- `/usr/bin/grep -c "^- \[ \] \*\*REL-08\*\*" .planning/REQUIREMENTS.md` → `1` -- REL-08
  deliberately left unticked, per the plan's own instruction (observed).

## Self-Check: PASSED

- `CHANGELOG.md` contains `## [9.1.0] — 2026-09-11` — FOUND.
- Commit `de18524` — FOUND (`git log --oneline --all | grep de18524`).
- `.planning/phases/27-ship-v9-1-0/27-08-SUMMARY.md` — FOUND (this file).

## Requirements Note

`requirements: [REL-08]` is named in this plan's frontmatter, but **REL-08 is NOT marked complete
by this plan**, matching plan 27-01's and 27-04's own precedent. REL-08's own text names
verification measured against product recurrence at both timings; this plan ships only the
release-act half (the entry itself, citing the pre-arm reading already taken). Plan 27-09's
post-arm reading, and D-16's dated-addendum mechanism if the trip still fires, are what discharge
the requirement in full. `.planning/REQUIREMENTS.md`'s REL-08 checkbox is left unticked
deliberately.

## Next Phase Readiness

- Release act three (the `[9.1.0]` CHANGELOG entry) is complete and committed alone, touching no
  other tracked file.
- The entry cites, rather than states, every recurrence-reading figure -- D-16's circularity is
  closed. If plan 27-09's post-arm reading confirms the trip still fires, a dated addendum is
  appended to this same entry per D-16, rather than any digit being edited in place.
- `docs/conformance-baseline.md` and `docs/data/conformance.json` remain exactly as plan 27-04 left
  them; pre-commit gate 3 passed trivially, as D-27-06 predicted, with no regeneration in this plan.

---
*Phase: 27-ship-v9-1-0*
*Completed: 2026-09-11*
