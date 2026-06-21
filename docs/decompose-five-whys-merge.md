# Decompose → Five-Whys Merge — v7.5

**Artifact type:** Decision / merge-execution record
**Date:** 2026-06-21
**Phase:** 112-trace-decision-artifact-traceability-reconciliation (Plan 01)
**Requirement:** TRACE-01
**Status:** DECIDED

---

## Decision

The `decompose` technique (reduce-to-primitives / irreducibility drill) was **absorbed** into
the `five-whys` technique as a co-equal dual mode; the standalone `decompose` surface was
**retired**. This is the absorb-and-retire merge shape.

The merge was executed across Phases 110-111 of the v7.5 milestone (the first
CONSOLIDATION milestone, reversing the v7.x expansion arc). The driving evidence was the
v7.4 live 9-technique Step 0 re-baseline: decompose (S-P09) scored **0/5 FAIL on clean
evidence** — all five runs routed to full-composer, with zero spend-limit truncations. The
conceptual overlap was well-established before the measurement: both techniques operate on
a reduce-to-root-cause intent. The 0/5 clean fail confirmed that maintaining a standalone
`decompose` surface added trigger-crowding cost without result-breadth benefit.

This artifact closes the VERDICT-01 forward pointer. See
[Closure of the VERDICT-01 forward pointer](#closure-of-the-verdict-01-forward-pointer)
below, and the source verdict doc:
[expansion-measurement-verdict.md#forward-pointer-the-technique-merge-execution-milestone](expansion-measurement-verdict.md#forward-pointer-the-technique-merge-execution-milestone).

---

## Merge Shape

The merge followed the **absorb-and-retire** pattern:

- **Absorb:** decompose's reduce-to-primitives / irreducibility content was folded into
  `shared/references/five-whys.md` as a **co-equal second mode** of the five-whys
  technique. The two modes — causal recursion and structural reduction — are now united
  under a single technique, a single trigger vocabulary, and a single `shared/references/`
  entry. Neither mode is subordinated to the other; the H1 of the merged file names both
  equally.

- **Retire:** The standalone `decompose` surface — its `shared/references/` entry, its
  skill registration, its token binding, its Step 0 trigger row, its agent-body Phase 3
  handoff — was deleted. No renamed alias was introduced; reduce-to-primitives mode is
  reached through the unified five-whys entry.

**Why this shape?** The absorb-and-retire pattern concentrates routing signal. A user
who formerly needed to know which of two similar technique names to invoke now reaches both
modes through a single entry with explicit mode-selection guidance. The trigger vocabulary
for reduce-to-primitives mode is preserved verbatim inside the merged reference file, so
the router still fires on phrases like *"reduce to primitives"*, *"irreducibility drill"*,
or *"break X into constituent facts"* — but through the five-whys entry, not a standalone
decompose entry.

This is the same structural rationale cited in the verdict doc's Merge Recommendation
section: "merging overlapping techniques reduces the trigger target count and concentrates
routing signal onto the remaining technique."

---

## What Folded

The following reduce-to-primitives / irreducibility content now lives in
`shared/references/five-whys.md` as part of the merged technique:

- **Co-equal dual-mode H1:** The file's top-level heading is now
  `# 5-Whys & Decompose (Root-Cause & Reduce-to-Primitives)`, naming both modes in the
  title. The introductory blockquote describes both causal recursion and structural reduction
  as co-equal recursive drills.

- **Merged `## Procedure` section:** The procedure now contains two named subsections:
  `### Causal mode (root-cause drill)` (the original five-whys procedure) and
  `### Reduce-to-primitives mode (irreducibility drill)` (the absorbed decompose procedure).
  Both are fully detailed step-by-step instructions with stop-test integration.

- **Decompose's stop test in the non-inlining `## Stop test` section:** The irreducibility
  stop test — the three irreducible anchors (physical law, definition, direct measurement)
  — was placed in a standalone `## Stop test` section. This section is **not** inlined into
  the agent body via `{{TOOL:five-whys}}` substitution; it is present in the reference file
  for human readers and focused-mode invocations, but intentionally excluded from the body
  token to preserve the agent-body line budget.

- **Combined decision rule in `## When to reach for this`:** This section now contains the
  mode-selection rule for both causal mode and reduce-to-primitives mode, the trigger
  vocabulary for reduce-to-primitives (D-01a), the "not a good fit" guidance, and the
  intra-technique vs. external-boundary distinction (causal vs. reduce-to-primitives is
  intra-technique; fishbone is the external cross-technique boundary).

- **Merged `## Handoff` section:** The handoff now documents both modes' outputs — causal
  mode hands off causal root causes; reduce-to-primitives mode hands off verified primitives.
  Both hand off to different rows of the Ground Truths list in Phase 3.

- **Merged `## Failure modes` section:** Two subsections cover the failure modes specific
  to each mode, including the confuse-the-modes failure (drifting from structural reduction
  into causal tracing) that is unique to the merged-technique context.

---

## What Was Retired

The following standalone `decompose` surfaces were deleted or decremented as part of the
merge:

- **`shared/references/decompose.md`** — deleted. Its content (reduce-to-primitives
  procedure, stop test, when-to-reach-for-this, failure modes, handoff) was absorbed into
  `shared/references/five-whys.md`. The standalone reference file no longer exists.

- **`shared/skills/decompose/`** — the entire directory was deleted. The skill registration
  (slash command), its `SKILL.md`, and the corresponding `first-principles/skills/decompose/`
  generated output are gone. The focused-mode decompose skill is not replaced; reduce-to-
  primitives mode is now reached through the five-whys focused skill or the orchestrating
  agent body.

- **`tool-map.yml` entry** — the `decompose` entry in `shared/spine/tool-map.yml` was
  deleted. There is no `{{TOOL:decompose}}` token binding remaining; reduce-to-primitives
  mode is inlined via `{{TOOL:five-whys}}`.

- **Both `{{TOOL:decompose}}` token sites** — the two occurrences in
  `shared/spine/SKILL-body.md` (Phase 3's primary decompose invocation and its parenthetical
  handoff reference) were replaced. Phase 3 now points to `{{TOOL:five-whys}}` in
  reduce-to-primitives mode; the parenthetical was reframed as an intra-technique mode
  distinction within the five-whys entry.

- **`focused-decompose` Step 0 phrase row** — the trigger phrase row for `focused-decompose`
  mode was removed from the `**Phrase detection rules**` table in `shared/spine/SKILL-body.md`.
  The eight remaining techniques now occupy the phrase table; reduce-to-primitives trigger
  vocabulary is captured in the `## When to reach for this` combined decision rule.

- **Standalone worked example at `shared/examples/decompose-irreducibility.md`** — this file
  was **not deleted** (per Phase 110 decision D-04: kept and rebranded in-place). The in-text
  source label was rebranded to attribute the example to five-whys (reduce-to-primitives
  mode) rather than the former standalone decompose skill. The file's content (the molten-salt
  reactor irreducibility drill) is retained as a worked example for reduce-to-primitives mode.

- **Nine-to-eight technique count decrements** — all count-bearing strings that previously
  named nine techniques were decremented to eight:
  - `KNOWN_TECHNIQUES` in `scripts/check-step0-emulator.py` (9→8 elements; `decompose`
    removed).
  - Technique counts in `shared/spine/SKILL-body.md` and generated agent body.
  - Fixture catalog counts in `tests/step0-fixture-catalog.md` (S-P09 / S-N05 rows removed;
    Category-4 hardcoded decompose assertion retired; S-P16/S-N08 re-homed per Phase 111
    reconcile).
  - Count references in `sync-content.py`'s target-count assertions.
  - VAL-05 skill-listing budget: from 1991/2000 (9-technique, 9-char slack) to 1950/2000
    (8-technique, 50-char slack) after the `decompose` skill listing was removed.
  - Agent body lines: from 622/644 before Phase 110 to 598/644 after regeneration (the
    removal of `{{TOOL:decompose}}` content freed 24 lines without requiring the body ceiling
    to be raised).

---

## Verification Decision

**Offline gates only.** No live `claude` re-baseline was performed for this merge. This was
a deliberate decision, not an oversight — the spend-limit reality documented in the v7.5
milestone (STATE.md) makes a fresh 8-technique live run impractical in the same budget
window. The offline gate suite was the verification criterion for this milestone.

All offline gates were green after the merge landed (Phase 111 completion):

| Gate | Script | Result |
|------|--------|--------|
| DUAL-04 | `sync-content.py --check` | Green — zero shared/generated-tree drift |
| STEP0-06 | `check-step0-live.py --self-test` | Green — offline harness self-test passes |
| **STEP0-08** | `check-step0-emulator.py --self-test` | **Flipped red→green in Phase 111** — `decompose` removed from `KNOWN_TECHNIQUES` |
| VAL-01 | `claude plugin validate` | Green |
| VAL-02 | `markdownlint-cli2` | Green |
| VAL-03 | `check-links.py` | Green |
| VAL-04 | `check-trigger-collisions.py` | Green |
| VAL-05 | `check-description-budget.py` | Green (1950/2000, 50-char slack) |
| GATE-01 | `check-agent.py` | Green |
| BATT-06 | `check-routing-battery.py --self-test` | Green |
| TRACE-03 | `check-traceability.py --self-test` | Green |

**STEP0-08 was intentionally left red at the end of Phase 110** (the `shared/` fold and
surface deletion phase) as a documented hand-off to Phase 111. Phase 111 completed the
battery reconciliation: removing `decompose` from `KNOWN_TECHNIQUES`, retiring the S-P09
and S-N05 fixtures, and retiring the Category-4 hardcoded decompose assertion flipped
STEP0-08 from red to green.

**Deferred tooling pass — `scripts/check-step0-live.py` dormant refs (D-04):** The live
harness `scripts/check-step0-live.py` retains dormant references to decompose: the S-P09
row in `CANONICAL_TALLY_IDS`, `focused-decompose` in `KNOWN_MODES`, and the S-P09 entry
in `RR_ID_MAP`. These were **not scrubbed this phase**. The decisive rationale: the frozen
v7.4 baseline (`tests/step0-baseline-v7.4.md`) legitimately measured a 9-technique set
including decompose (Phase 108, 110 live `claude` invocations). Scrubbing S-P09 from the
live harness would retroactively alter the semantics of that historical tally artifact —
a tally that is cited in the verdict doc and the traceability surface. STEP0-06
(`check-step0-live.py --self-test`) is green because the dormant refs are non-exercised
by the offline self-test. These refs are a future tooling-pass candidate: they should be
reconciled when a budget-fresh 8-technique live re-baseline is run and the v7.4 baseline
is formally superseded.

---

## Deferred Live Re-Baseline

A live re-baseline of the now-8-technique set is **deferred to a future budget-fresh
milestone**. This is the honest state: the v7.4 baseline (`tests/step0-baseline-v7.4.md`,
Phase 108) is the last authoritative live measurement. It measured 9 techniques including
decompose. After the v7.5 merge, the live routing picture for the 8-technique set is
unknown (but the offline emulator, STEP0-08, is green — the phrase-detection emulator
confirms the merge is correctly reflected in the agent body).

The still-deferred merge pairs from the verdict doc remain open:

- **`theoretical-limit` → `inversion` (SECOND recommendation):** Gated on a clean S-P14
  live re-measurement (the v7.4 S-P14 tally was spend-limit-indeterminate, not a confirmed
  misroute). Tracked as TLINV-01 in future-milestone deferred items.

- **`estimate` → partner unscoped (FLAG):** `estimate` (S-P10) scored 0/5 FAIL on clean
  evidence in v7.4. Its merge partner has not been identified; scoping requires behavioral
  analysis before pair selection. Tracked as ESTPART-01 in future-milestone deferred items.

Neither of these pairs was in scope for the v7.5 milestone, which was gated specifically
on VERDICT-01 (the PRIMARY recommendation: `decompose`↔`five-whys`) and executed only
that merge.

---

## Closure of the VERDICT-01 Forward Pointer

This artifact **closes VERDICT-01** — the forward pointer named in the verdict doc's
`### Forward pointer: the technique-merge-execution milestone` section of
[expansion-measurement-verdict.md](expansion-measurement-verdict.md).

The verdict doc (authored in Phase 109 / v7.4) named the technique-merge-execution
milestone as the designated follow-up: "The technique-merge-execution milestone must not
begin until VERDICT-01 is closed (i.e., until this verdict artifact is committed and the
traceability surface reconciled)." That condition was met: the verdict artifact was
committed and the traceability surface reconciled at v7.4 close. The v7.5 milestone then
executed the PRIMARY merge recommendation (decompose→five-whys) across Phases 110-112.

**VERDICT-01 is now CLOSED.** The technique-merge-execution milestone designated in the
verdict doc has been executed as the v7.5 milestone. This artifact is the durable
merge-execution record that closes that pointer.

The verdict doc's Forward-pointer section has been annotated with a bidirectional closure
note (see [expansion-measurement-verdict.md](expansion-measurement-verdict.md)). Both
directions of the pointer are now closed: this artifact references the verdict doc, and
the verdict doc's Forward-pointer section references this artifact.

---

## Out of Scope

The following were explicitly deferred and did NOT occur in this artifact, in Phases
110-112, or in the v7.5 milestone:

- **`theoretical-limit`↔`inversion` merge execution** — not this milestone; gated on a
  clean S-P14 live re-measurement.
- **`estimate` merge partner identification and execution** — not this milestone; partner
  needs behavioral scoping.
- **Live re-baseline of the 8-technique set** — deferred to a future budget-fresh
  milestone; the v7.4 9-technique baseline is the last authoritative live measurement.
- **Scrubbing dormant decompose refs in `scripts/check-step0-live.py`** — deferred per
  D-04; the frozen v7.4 baseline legitimately measured /9 including decompose.
- **Agent-body trim** — body ended at 598/644 after Phase 110 regeneration; the ceiling
  was not raised and no trim was needed.

---

*Decision recorded: 2026-06-21*
*Authored in: Phase 112-trace-decision-artifact-traceability-reconciliation, Plan 01*
*Supersedes: nothing (first v7.5 merge-execution decision artifact)*
*Closes: VERDICT-01 forward pointer in expansion-measurement-verdict.md*
