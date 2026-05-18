---
phase: 05-domain-spread-worked-examples
plan: "07"
subsystem: examples
tags: [gap-closure, IN-03, GAP-02, personal-general, figure-consistency]
dependency_graph:
  requires: []
  provides: [EX-03-consistent-figure-confidence]
  affects: [first-principles-thinking/examples/personal-general.md]
tech_stack:
  added: []
  patterns: []
key_files:
  created: []
  modified:
    - first-principles-thinking/examples/personal-general.md
decisions:
  - "Carried Chain 1 caveat phrasing into Section 6 rather than removing it from Chain 1 — the $18,000 is accurately a rent+tax partial accounting and Section 6 must not overstate it"
metrics:
  duration_minutes: 5
  completed_date: "2026-05-18"
---

# Phase 05 Plan 07: Personal-General Figure-Confidence Consistency Summary

**One-liner:** Closed IN-03 by carrying Chain 1's "before accounting for other SF cost differences" qualifier into both Section 6 references to the ~$18,000 cost differential in personal-general.md.

## What Was Done

Resolved the figure-confidence inconsistency (IN-03) in `examples/personal-general.md`:

- **Chain 1 (Section 4, line 60)** stated the ~$18,000 differential as "roughly $18,000/year before accounting for other SF cost differences (transportation, food, services)" — correctly hedged because the figure covers rent and California/Oregon tax delta only.
- **Section 6 step 3** previously stated "The ~$18,000 annual cost differential" as a firm operative figure with no caveat.
- **Section 6 Trade-offs paragraph** previously stated "accepting a ~$18,000/year effective cost-of-living increase" — also without qualifier.

Both Section 6 references were updated to attach the same qualifier Chain 1 uses, making the confidence level consistent across the document.

Confirmed GAP-02: the two `### Conclusion:` headings remain in the bare template form (`### Conclusion: [text]`) — no letters, no numbers.

## Tasks

| # | Name | Commit | Files |
|---|------|--------|-------|
| 1 | Make ~$18,000 phrasing consistent between Chain 1 and Section 6 (IN-03); confirm GAP-02 heading conformance | 2fe0dc8 | first-principles-thinking/examples/personal-general.md |

## Verification Results

- `grep -c "^### Conclusion: " personal-general.md` returns **2** — confirmed.
- `grep -n "Conclusion A\|Conclusion B" personal-general.md` returns nothing — confirmed.
- Six `## 1.` through `## 6.` headings present in order — confirmed.
- All three occurrences of `18,000` in the file: Chain 1 (line 60) retains its caveat; Section 6 step 3 (line 97) and Trade-offs paragraph (line 103) now each carry the matching qualifier.

## Deviations from Plan

None — plan executed exactly as written. The two-edit minimal fix matched the prescribed approach.

## Known Stubs

None.

## Threat Flags

None — pure Markdown content change with no network endpoints, auth paths, or schema changes.

## Self-Check: PASSED

- `first-principles-thinking/examples/personal-general.md` exists and contains the qualifier in Section 6.
- Commit 2fe0dc8 verified in git log.
- No unexpected file deletions.
