---
phase: 27-ship-v9-1-0
plan: 07
subsystem: release-verification-battery-total-and-fence-adjudication
tags: [release, REL-06, direct-count, D-15, fence-adjudication, recurrence-reading]

dependency-graph:
  requires:
    - "27-05: release act one (all 17 version stamps at 9.1.0)"
    - "27-06: release act two (matrix rows + headline sweep), whose own deviation (the new '18'
      CANNOT-REACH containment-ledger entry) this plan's fence adjudication and cross-cutting note
      both examine"
    - "27-04: the pre-arm recurrence reading, whose 40 distinct FENCED sites this plan re-checks
      byte-for-byte against HEAD"
  provides:
    - "REL-06 ticked in .planning/REQUIREMENTS.md on a direct count at both the phase base
      (f189c99) and HEAD, with the battery's own tally line demoted to corroboration"
    - "The D-15 fence adjudication table: 40/40 distinct FENCED sites HELD, 0
      HELD-WITH-DISCLOSED-EXCEPTION, 0 misclassifications"
    - "A cross-cutting note on 27-06's own CANNOT-REACH deviation, for plan 27-08's CHANGELOG
      disclosure and plan 27-09's post-arm reading to act on"
  affects:
    - "plan 27-08 (the [9.1.0] CHANGELOG entry) -- must disclose the containment ledger's current
      value (21, not 20) and this plan's own observation about the '18' entry's shape"
    - "plan 27-09 (the post-arm reading) -- the '18' entry did not exist at pre-arm time, so it is
      not one of the 40 FENCED sites; a fresh full sweep may find it as a NEW site, not a held one"

tech-stack:
  added: []
  patterns:
    - "distinct file:line union across three record files (not row union), matching the
      acceptance criterion's own unit; content compared by git show <pre-arm-sha>:<path> against
      the working tree, located by content when a line number shifted rather than assumed broken"

key-files:
  created:
    - .planning/phases/27-ship-v9-1-0/27-07-SUMMARY.md
  modified:
    - .planning/REQUIREMENTS.md

decisions:
  - "The phase base for the direct count is f189c99 (parent of 442fd01, the first Phase 27
    commit) and the pre-arm commit for the fence adjudication is 1846788 (the commit that landed
    plan 27-04's three record files) -- distinct commits for distinct purposes, both identified by
    command rather than assumed."
  - "All 40 distinct FENCED file:line sites read HELD -- every apparent line-number shift (7 of
    the 40 sites sit in files a release act touched) traced to content inserted ABOVE the site by
    an unrelated release-act edit, never to the site's own bytes; the four frozen scanner
    functions in scripts/gen-gate-docs.py are confirmed byte-identical function-body-for-
    function-body between the pre-arm commit and HEAD, independently of the file-level diff."
  - "The misclassification check (would a FENCED site touched by a release act have actually
    qualified as RELEASE-OWNED) returns none: the three CLAUDE.md sites this plan traced sit
    outside both of CLAUDE.md's own generated-marker ranges (144-182, 311-315)."

requirements-completed: [REL-06]

metrics:
  duration: "~1h"
  completed: "2026-09-11"
---

# Phase 27 Plan 07: Battery-Total Direct Count and D-15 Fence Adjudication Summary

Established REL-06 by direct count at both the phase base and HEAD (26 at both endpoints,
`FIREWALL: GREEN (26/26)` cited only as corroboration), and adjudicated D-15's fence against the
release acts that have actually run: all 40 distinct FENCED sites from plan 27-04's pre-arm
reading are **HELD**, with zero disclosed exceptions and zero misclassifications. A cross-cutting
note records that plan 27-06's own release act introduced a new, structurally-relevant containment
entry that this plan's fence check does not cover by construction, and names why.

## What was done

### Task 1 — REL-06 by direct count

Phase base identified as `f189c99` (`git log -1 442fd01~1`, confirmed the parent of `442fd01`, the
first Phase 27 commit). At both `f189c99` and `HEAD`, applied `check-registration.py`'s own
`_BATTERY_GATE_RE` (`^[ \t]*gate(?:_prereq)?[ \t]+"([^"]+)"`) against `git show
<ref>:scripts/check-firewall-battery.sh`: 25 regex matches reduce to **24 distinct gate IDs**
(`VAL-03` is the sole ID with two matches, its if/else branches counted once, per Phases 25/26's
own precedent) at both endpoints, byte-identical set. 24 + 2 inline checks (`INVARIANT-CHECK` at
line 618/622, `FROZEN-EVIDENCE` at line 758/762/766, each incrementing `TOTAL` once via its own
literal `TOTAL=$((TOTAL + 1))` line at lines 616 and 756 — distinct from the two `TOTAL`
increments inside the `gate`/`gate_prereq` function bodies themselves, lines 252/288) = **26 at
both endpoints.**

CI job count: every indented `name: <job> (<GATE-ID>)` line under `jobs:` in
`.github/workflows/validation.yml` — **23 at `f189c99`, 23 at `HEAD`**, identical 23-item list at
both endpoints (including the two non-conforming-shape names, `check-trigger-collisions
(VAL-04/GATE-02)` and the bare `GATE-02-v8.5`, present unchanged at both). `BATTERY_ONLY_GATE_IDS`
read directly at `HEAD` (`frozenset({'QUAL-01'})`) and at `f189c99` (`grep` of the module source:
`frozenset[str] = frozenset({"QUAL-01"})`) — the single-member set holding `QUAL-01` at both.

Byte comparisons: `git diff --numstat f189c99 HEAD -- .github/workflows/validation.yml` → empty.
`git diff --numstat f189c99 HEAD -- scripts/check-firewall-battery.sh` → `1	0
scripts/check-firewall-battery.sh`; the diff body shows exactly one added line —
`'tests/recurrence-reading-v9.1'` inserted into `_FROZEN_PATHS` — and zero removed lines.

Corroboration run after the direct count, never before: `bash scripts/check-firewall-battery.sh`
→ `FIREWALL: GREEN (26/26)`. `python3 scripts/check-registration.py --self-test` → `PASS (29
controls: …)`, exit 0.

REL-06 ticked in `.planning/REQUIREMENTS.md` with the full evidence block transcribed above,
closing with the sentence that `FIREWALL: GREEN` is not itself the evidence, per `docs/PROCESS.md`
section 3's record that it held through every prior recurrence of this milestone's own defect
class. Traceability table row updated `Pending` → `Complete`.

### Task 2 — D-15 fence adjudication

**Pre-arm commit identified:** `1846788` (`feat(27-04): take v9.1.0's pre-release recurrence
reading` — the commit that landed `tests/recurrence-reading-v9.1/pre-arm-{scanner,reader-a,
reader-b}.md`). Confirmed `33fe35b` (the sha readers were actually given) is an ancestor of
`1846788`, and the diff between them touches only `tests/recurrence-reading-v9.1/`,
`docs/conformance-baseline.md`, `docs/data/conformance.json` and `scripts/report-conformance.py`
— none of which is a site any reader cited — so using `1846788` as the before-state for every
site's content is equivalent to using `33fe35b`.

**Union, by distinct `file:line`** (not by row — several sites carry two rows with different
claimed values on the same line, e.g. `docs/live-monitoring-runbook.md:87`, and the acceptance
criterion's own unit is the site): a mechanical extraction of every row across
`pre-arm-scanner.md` (0 rows), `pre-arm-reader-a.md` (35 rows), `pre-arm-reader-b.md` (26 rows)
produces **40 distinct `file:line` sites**, all classified `FENCED` in their source row (0
`RELEASE-OWNED` — confirmed independently, matching plan 27-04's own determination).

**Byte comparison, per site.** First isolated which of the 40 sites live in a file any release act
touched at all, via `git diff --name-only 1846788 HEAD` (23 files changed, from plans 27-05 and
27-06). Intersection: 7 of the 40 sites sit in a touched file (`CLAUDE.md` ×3, `docs/README.md`
×2, `docs/MEASUREMENT-MAP.md` ×1, `docs/requirements-traceability.md` ×1,
`scripts/gen-gate-docs.py` ×1). The remaining 33 sites sit in files absent from that diff, so they
are HELD by construction (the whole file is byte-unchanged) — including
`.planning/MILESTONE-CONTEXT.md`, `.planning/PROJECT.md` and `.planning/REQUIREMENTS.md`, which
are gitignored and so cannot be `git diff`'d at all; for those three, HELD was confirmed instead
by direct re-read of the exact cited line against the reader's transcribed claimed-value text
(all three match verbatim, at the same line number, in `.planning/REQUIREMENTS.md`'s case even
though that same file gained REL-05/06/07 evidence blocks elsewhere — those insertions sit at
lines 650+, well below line 346).

For the 7 sites in touched files, compared `git show 1846788:<path>` against the working tree at
and around the cited line, locating the site by content when the line number moved (per the plan's
own instruction, rather than calling a shift a break):

| file:line (pre-arm) | now at | shift | content |
|---|---|---|---|
| `CLAUDE.md:68` | 68 | 0 | byte-identical |
| `CLAUDE.md:330` | 332 | +2 | byte-identical |
| `CLAUDE.md:381` | 383 | +2 | byte-identical |
| `docs/README.md:110` | 110 | 0 | byte-identical |
| `docs/README.md:217` | 217 | 0 | byte-identical |
| `docs/MEASUREMENT-MAP.md:17` | 17 | 0 | byte-identical |
| `docs/requirements-traceability.md:294` | 296 | +2 | byte-identical |
| `scripts/gen-gate-docs.py:3390` | 3405 | +15 | byte-identical |

Every shift traces to release-act content inserted **above** the cited line elsewhere in the same
file (CLAUDE.md's requirements-ledger v9.1 hop and headline-history additions; the new v9.1
headline-history row and recount sentence in `docs/requirements-traceability.md`; the new
`_DEFERRED_CONTAINMENT_HITS` entry and its comment block in `scripts/gen-gate-docs.py`) — never to
an edit at the site itself. All 7 are **HELD**.

**Independent confirmation for the scanner arm's own instruments:** the four frozen functions
`run_literal_scan`, `narrative_restatement_problems`, `detail_page_containment_problems`,
`chain_terminus_problems` in `scripts/gen-gate-docs.py` were diffed function-body-for-function-body
between `1846788` and `HEAD` (not merely file-level) — all four **byte-identical**, confirming the
scanner arm's own reading mechanism, not just the measured prose sites, survived the release
bracket untouched.

## The adjudication table (all 40 sites)

Every distinct FENCED `file:line` from the union of the three pre-arm record files, its verdict,
and its bound. `-` in the "release act / sha" and "bound" columns means no act touched the site
(file absent from the `1846788..HEAD` diff, or — for the three gitignored `.planning/` files —
confirmed unchanged by direct re-read since no git history exists to diff).

| # | file:line | fence class | verdict | release act / sha | bound |
|---|---|---|---|---|---|
| 1 | `.planning/MILESTONE-CONTEXT.md:14` | FENCED | HELD | - | - |
| 2 | `.planning/MILESTONE-CONTEXT.md:265` | FENCED | HELD | - | - |
| 3 | `.planning/PROJECT.md:9` | FENCED | HELD | - | - |
| 4 | `.planning/REQUIREMENTS.md:346` | FENCED | HELD | - | - |
| 5 | `CLAUDE.md:68` | FENCED | HELD | - | - |
| 6 | `CLAUDE.md:330` (now 332) | FENCED | HELD | plan 27-06, `8f16db9`/`e67f878` (line-shift only, content unchanged) | shifted +2 lines by unrelated insertion above it |
| 7 | `CLAUDE.md:381` (now 383) | FENCED | HELD | plan 27-06, `8f16db9`/`e67f878` (line-shift only) | shifted +2 lines |
| 8 | `README.md:143` | FENCED | HELD | - | - |
| 9 | `README.md:145` | FENCED | HELD | - | - |
| 10 | `docs/CONFIGURATION.md:18` | FENCED | HELD | - | - |
| 11 | `docs/CONFIGURATION.md:148` | FENCED | HELD | - | - |
| 12 | `docs/DEVELOPMENT.md:153` | FENCED | HELD | - | - |
| 13 | `docs/DEVELOPMENT.md:171` | FENCED | HELD | - | - |
| 14 | `docs/MEASUREMENT-MAP.md:17` | FENCED | HELD | plan 27-06, `8f16db9` (file touched elsewhere; this line unmoved and unchanged) | - |
| 15 | `docs/ONBOARDING.md:113` | FENCED | HELD | - | - |
| 16 | `docs/README.md:110` | FENCED | HELD | plan 27-06, `8f16db9` (file touched elsewhere; this line unmoved and unchanged) | - |
| 17 | `docs/README.md:217` | FENCED | HELD | plan 27-06, `8f16db9` (file touched elsewhere; this line unmoved and unchanged) | - |
| 18 | `docs/TESTING.md:99` | FENCED | HELD | - | - |
| 19 | `docs/TESTING.md:117` | FENCED | HELD | - | - |
| 20 | `docs/TESTING.md:118` | FENCED | HELD | - | - |
| 21 | `docs/gates/CONF-GATE.md:42` | FENCED | HELD | - | - |
| 22 | `docs/gates/QUAL-01.md:244` | FENCED | HELD | - | - |
| 23 | `docs/gates/QUAL-01.md:246` | FENCED | HELD | - | - |
| 24 | `docs/live-monitoring-runbook.md:59` | FENCED | HELD | - | - |
| 25 | `docs/live-monitoring-runbook.md:87` | FENCED | HELD | - | - |
| 26 | `docs/live-monitoring-runbook.md:173` | FENCED | HELD | - | - |
| 27 | `docs/requirements-traceability.md:294` (now 296) | FENCED | HELD | plan 27-06, `8f16db9`/`e67f878` (line-shift only) | shifted +2 lines |
| 28 | `docs/testing-agents-headlessly.md:249` | FENCED | HELD | - | - |
| 29 | `docs/v8.0-final-closure.md:15` | FENCED | HELD | - | - |
| 30 | `docs/v8.0-final-closure.md:20` | FENCED | HELD | - | - |
| 31 | `docs/v8.0-final-closure.md:21` | FENCED | HELD | - | - |
| 32 | `docs/v8.0-final-closure.md:98` | FENCED | HELD | - | - |
| 33 | `docs/v8.0-final-closure.md:113` | FENCED | HELD | - | - |
| 34 | `scripts/_battery_core.py:2385` | FENCED | HELD | - | - |
| 35 | `scripts/check-quality-harness.py:4232` | FENCED | HELD | - | - |
| 36 | `scripts/check-quality-harness.py:9857` | FENCED | HELD | - | - |
| 37 | `scripts/check-step0-live.py:8` | FENCED | HELD | - | - |
| 38 | `scripts/check-step0-live.py:1784` | FENCED | HELD | - | - |
| 39 | `scripts/gen-gate-docs.py:3390` (now 3405) | FENCED | HELD | plan 27-06, `8f16db9` (containment-ledger CANNOT-REACH entry and re-pin inserted above it; this comment's own text unchanged) | shifted +15 lines |
| 40 | `scripts/sync-content.py:131` | FENCED | HELD | - | - |

**Tally:** 40 HELD, 0 HELD-WITH-DISCLOSED-EXCEPTION, 0 misclassified.

**RELEASE-OWNED sites:** none — plan 27-04 found zero, confirmed again here by the same
mechanical check against the live generated-marker ranges, the five `COVERED_HEADLINE_SURFACES`,
the 17 version-stamp sites and the two matrix files. No post-act state to record for this class.

**Misclassification check, performed:** for each of the 7 sites sitting in a file a release act
touched, checked whether any of `protocol.md`'s four `RELEASE-OWNED` sub-classes would, on
inspection, have covered it: (a) a `<!-- GENERATED -->` region — `CLAUDE.md`'s two generated
regions are lines 144-182 (CI gate table) and 311-315 (coverage headline); sites at 68/332/383 sit
outside both. (b) a coverage-headline statement on a `COVERED_HEADLINE_SURFACES` member — none of
the 7 sites is the headline sentence itself. (c) a version-stamp site — none of the 7 is one of the
17 enumerated stamps. (d) `docs/requirements-matrix.md`/`docs/data/matrix.json` — none of the 7 is
either file. **Result: no misclassification found** — every FENCED classification the pre-arm
reading assigned to these 7 sites was correct in advance.

## Cross-cutting notes for plans 27-08 and 27-09

**(a) On 27-06's own deviation — the new `('CLAUDE.md', '18')` CANNOT-REACH entry.** Stated
plainly, as the orchestrator's brief asked: **yes, this is a release act introducing a fresh
instance of the shape this milestone exists to reduce** — a new, hand-written, quantity-shaped
prose claim (the v9.1 milestone's own row count, "18") on a product surface, with no
`check-traceability.py --describe` field a containment check can corroborate it against. It is
**not** a recurrence of the CR-01/02/03 shape (a value that is currently wrong) — "18" is correct
today — but it is a new addition to the population of claims a gate cannot dispute, which is the
raw material the four prior recurrences (`docs/PROCESS.md` §3) were all drawn from. Plan 27-06
resolved it the only way the existing mechanism allows without inventing a new one (D-D forbids
a new gate): admission to `_DEFERRED_CONTAINMENT_HITS` as `CANNOT-REACH`, growing
`_CONTAINMENT_LEDGER_MAX` 20 → 21 in the same commit. This is RATCHET-02's own documented
size-only bound working as designed (growth is permitted, tracked, and re-pinned — never silent),
not a violation of it; but it does mean the ledger this milestone's own work is supposed to be
driving toward zero grew by one during the milestone's own release bracket.

**Bearing on D-15:** none, directly — the "18" entry did not exist at the pre-arm commit
(`1846788`/`33fe35b`), so it is not one of the 40 sites this plan's fence covers, and D-15's fence
protocol only ever protected sites that already existed at pre-arm time. It is simply outside this
plan's scope by construction, not a fence break.

**Bearing on plan 27-09 (the post-arm reading):** the "18" hop is now live prose on `CLAUDE.md`
with no corroborating generated field — exactly the shape `protocol.md`'s trip predicate looks
for. A fresh, full sweep (which D-03/D-05 require of both post-arm readers) may find it as a **new**
site not present in the pre-arm reading — it would not count as a "held" or "broken" fence site,
but it would be a legitimate new entry in the post-arm sites/claims figure, and worth naming
explicitly as "new since pre-arm, introduced by the release bracket itself" rather than folding it
silently into whatever the post-arm total reads.

**Bearing on plan 27-08 (the `[9.1.0]` CHANGELOG entry):** if the entry cites the deferred-
containment ledger figure (D-13's discretionary disclosure, following the `999.69`/`20` precedent
named in D-13's own text), the correct current figure is **21**, not 20 — plan 27-06 moved it in
the same session this note was written. The entry should also state, if it discloses the ledger at
all, that the milestone's own release act added one CANNOT-REACH entry to it — the shape this note
records above — rather than presenting a static count with no acknowledgment that the milestone's
own last-mile work is part of what moved it.

**(b) On 27-04's own deviation — the `report-conformance.py` parser fix landing in the same commit
as the pre-arm reading.** Reviewed against this plan's own fence-adjudication lens: the fix is to
`_read_recurrence_records`'s table-row splitter, a piece of this milestone's own newly-written
apparatus (landed at plan 27-03), not one of the four STRIDE-registered frozen scanner functions
(`run_literal_scan`, `narrative_restatement_problems`, `detail_page_containment_problems`,
`chain_terminus_problems` — all four independently confirmed byte-identical above, function body
for function body, between the pre-arm commit and HEAD) and not the subject of any FENCED site (no
reader cited `scripts/report-conformance.py`). D-15's fence protects the 40 measured **sites** and
the STRIDE register's frozen-instrument guarantee protects the four **scanner functions**; this
fix is outside both perimeters, so it raises no fence-adjudication concern from this plan's vantage
point. This confirms, independently, plan 27-04's own contemporaneous judgment that it was a Rule
1 bug fix rather than a fence violation.

## Verification (observed this session)

- `git log -1 442fd01~1` → `f189c99 …` (phase base, observed).
- Direct count: 24 distinct gate IDs + 2 inline checks = 26, at both `f189c99` and `HEAD`
  (observed, transcribed above).
- `git diff --numstat f189c99 HEAD -- .github/workflows/validation.yml` → empty (observed).
- `git diff --numstat f189c99 HEAD -- scripts/check-firewall-battery.sh` → `1	0
  scripts/check-firewall-battery.sh` (observed); diff body shows the single added
  `'tests/recurrence-reading-v9.1'` line (observed).
- 23 CI job-name lines, identical set, at both endpoints (observed).
- `BATTERY_ONLY_GATE_IDS` = `frozenset({'QUAL-01'})` at both endpoints (observed).
- `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (26/26)` (observed, run after the
  direct count, cited as corroboration only).
- `python3 scripts/check-registration.py --self-test` → `PASS (29 controls: …)` (observed).
- `/usr/bin/grep -c "^- \[x\] \*\*REL-06\*\*" .planning/REQUIREMENTS.md` → `1` (observed).
- 40 distinct FENCED `file:line` sites extracted mechanically from the three record files
  (observed; command and output transcribed above) — matches the manual union used for the
  adjudication table exactly.
- All 40 sites' content compared `1846788` vs `HEAD` (33 via whole-file-untouched inference from
  `git diff --name-only`, 3 via gitignored-file direct re-read, 7 via explicit `git show`/working-
  tree line comparison with content-based relocation where the line shifted) — **0** byte
  differences found at any site (observed, per-site transcript above).
- The four frozen scanner functions in `scripts/gen-gate-docs.py` diffed function-body-for-
  function-body between `1846788` and `HEAD` — all four `IDENTICAL` (observed).
- `git status --porcelain -- ':!.planning'` → empty (no tracked file outside `.planning/` was
  edited or reverted by this plan's own work; the only edit this plan makes is to the gitignored
  `.planning/REQUIREMENTS.md`) (observed).

## Deviations from Plan

None — plan executed exactly as written. No site was reverted to change a verdict; every finding
above is as-measured.

## Self-Check: PASSED

- `.planning/phases/27-ship-v9-1-0/27-07-SUMMARY.md` — FOUND (this file).
- `.planning/REQUIREMENTS.md` REL-06 checkbox reads `[x]` — FOUND (`grep -c` above returned 1).
- `.planning/REQUIREMENTS.md` Traceability REL-06 row reads `Complete` — FOUND (verified by direct
  read after edit).
- Adjudication table contains all 40 distinct FENCED sites with a `HELD` verdict, 0
  `HELD-WITH-DISCLOSED-EXCEPTION` — FOUND (transcribed above).

## Requirements Note

`requirements: [REL-06]` is fully discharged by this plan: the battery total is established by
direct count at both the phase base and HEAD, both constrained files are proven byte-unchanged
except the one permitted `_FROZEN_PATHS` line, and `FIREWALL: GREEN` is explicitly demoted to
corroboration in the evidence block itself.

## Next Phase Readiness

- REL-06 is complete. The only remaining requirement in this phase is REL-08 (the `[9.1.0]`
  CHANGELOG entry and the post-arm recurrence reading).
- D-15's fence held clean through both release acts that have run so far (27-05, 27-06) — 40/40,
  zero exceptions, zero misclassifications. If further release acts land before the CHANGELOG
  entry (per D-14's ordering), this adjudication should be re-run against the new HEAD before
  plan 27-09's post-arm reading is taken, since a HELD verdict here is a statement about the tree
  as of this plan's own HEAD, not a standing guarantee.
- The cross-cutting notes above (on 27-06's new CANNOT-REACH entry and 27-04's parser fix) are
  carried forward for plans 27-08 and 27-09 to act on; neither blocks this plan's own completion.

---
*Phase: 27-ship-v9-1-0*
*Completed: 2026-09-11*
