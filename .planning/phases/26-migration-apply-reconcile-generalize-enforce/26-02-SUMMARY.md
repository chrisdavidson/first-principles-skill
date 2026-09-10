---
phase: 26-migration-apply-reconcile-generalize-enforce
plan: 02
subsystem: docs
tags: [gen-gate-docs, containment, literal-scan, requirements-governance, narr-01]

# Dependency graph
requires:
  - phase: 26-migration-apply-reconcile-generalize-enforce
    plan: 01
    provides: >-
      RATCHET-04's forward REACH-or-LEVEL determination for NARR-01
      (docs/gates/CONF-SURFACE.md), citable rather than re-derived, and the
      requirement/roadmap texts with `cog` already amended out
provides:
  - "docs/PROCESS.md §2's standing constraint generalized from the gate-battery count to every restated moving count (NARR-01), frozen-historical-count exception preserved byte-for-byte"
  - "A measured, transcribed pre-migration census of the coverage-headline restatement across the six containment-unreachable narrative surfaces plus CLAUDE.md, classified by fenced/in-region/chain-hop status"
  - "A published, anchor-counted disclosed bound (9) on docs/gates/CONF-SURFACE.md naming the one structurally-unreachable occurrence (docs/COMPONENT-DIAGRAM.md's fenced Mermaid label)"
affects: [26-03, 26-04, 26-05, 26-06, 26-07]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "In-process _scan_text_for_literal_hits() dry-run on drafted prose before writing to disk, repeated for every new sentence this plan wrote"
    - "Disclosed bound published with an anchor string in LITERAL_SCAN_DISCLOSED_BOUNDS rather than a hand-typed population digit in prose"

key-files:
  created: []
  modified:
    - docs/PROCESS.md
    - docs/gates/CONF-SURFACE.md
    - scripts/gen-gate-docs.py
    - CLAUDE.md
    - docs/ARCHITECTURE.md

key-decisions:
  - "Kept the pre-existing 'moved from 15 to its current value' sentence verbatim inside the generalized first paragraph rather than removing it — it is not itself a live-count restatement (it names a closed, one-time historical starting point), it produced zero literal-scan hits in the in-process dry run, and removing it would have discarded a worked example the plan's own action explicitly asked to keep alongside the COMPONENT-DIAGRAM.md/ARCHITECTURE.md references."
  - "Named the anchor 'component-diagram-mermaid-fence-unreachable' rather than a more generic name, because the census found exactly one structurally-unreachable occurrence and it is specific to that page's Mermaid fence — a generic name would overstate what the bound covers if a second, differently-shaped unreachable site is found later."
  - "Recorded CLAUDE.md's own coverage-headline occurrence (line 312) separately from the six-surface count, per the plan's own <action> instruction that it is plan 26-05's target (containment-reached) rather than NARR-02's (containment-unreachable) — it is not folded into either the region-candidate or structurally-unreachable tallies for the six-surface set."

requirements-completed: [NARR-01]

# Metrics
duration: ~40min
completed: 2026-09-10
---

# Phase 26 Plan 02: NARR-01 generalization and the pre-migration restatement census Summary

**Widened `docs/PROCESS.md` §2's digit-narrowing rule from the gate-battery count to every restated moving count, then measured — by command, not estimate — the pre-migration population that widened rule newly names: 2 region candidates and 1 structurally-unreachable occurrence, the latter published as a numbered, anchor-counted disclosed bound.**

## Performance

- **Duration:** ~40 min
- **Tasks:** 2
- **Files modified:** 5 (docs/PROCESS.md; docs/gates/CONF-SURFACE.md; scripts/gen-gate-docs.py; CLAUDE.md and docs/ARCHITECTURE.md as the mechanical `--write` regeneration side effect of the anchor count moving)

## Accomplishments

- `docs/PROCESS.md` §2's standing-constraint opening paragraph now binds every restated moving
  count, not the gate-battery count alone — the battery total is kept as the rule's named worked
  example (with its COMPONENT-DIAGRAM.md/ARCHITECTURE.md citations intact) rather than the rule's
  whole subject. The paragraph names CONF-13's already-existing literal scanner as the enforcement
  rather than claiming new teeth, points at `docs/gates/CONF-SURFACE.md`'s generated
  `registered_surfaces` figure instead of a bare digit for "how many surfaces," and cites
  `docs/v9.1-claim-containment-diagnosis.md` §5a's REACH classification and its own one-sentence
  answer to test 3 (a widened scope clause is not a second rule governing whether the first was
  followed) rather than re-deriving either.
- The frozen-historical-count second paragraph is confirmed byte-unchanged: `git diff
  docs/PROCESS.md` shows it as unchanged context with zero `+`/`-` lines inside it.
- The pre-migration restatement population NARR-01 newly names was measured by command across the
  six containment-unreachable surfaces plus `CLAUDE.md`: 3 occurrences on the unreachable set (2
  region candidates, 1 structurally unreachable) and 1 separate occurrence on `CLAUDE.md`
  (containment-reached, plan 26-05's own target).
- The structurally-unreachable occurrence — `docs/COMPONENT-DIAGRAM.md`'s Mermaid node label,
  inside a fenced code block — is published as numbered bound (9) on `docs/gates/CONF-SURFACE.md`,
  with a matching `component-diagram-mermaid-fence-unreachable` anchor added to
  `LITERAL_SCAN_DISCLOSED_BOUNDS` (`disclosed_bounds_anchors` 9 → 10), explicitly rejecting both a
  synthetic fixture and a widened criterion by name.
- Neither ledger moved: `_DEFERRED_LITERAL_HITS` 181/181 and `_DEFERRED_CONTAINMENT_HITS` 26/26,
  confirmed by module import before and after both tasks.

## Task Commits

1. **Task 1: Generalize §2's standing constraint (NARR-01)** — `2162730` (docs)
2. **Task 2: Measure and record the pre-migration restatement baseline** — `b82092b` (docs)

**Plan metadata:** this SUMMARY.md and the STATE.md/ROADMAP.md/REQUIREMENTS.md updates are
committed together as the plan's closing metadata commit — `.planning/STATE.md`,
`.planning/ROADMAP.md` and `.planning/REQUIREMENTS.md` all stay gitignored per project convention
(`commit_docs: false`) and are not part of that commit's file list beyond what the harness
force-tracks (this SUMMARY.md).

## Files Created/Modified

- `docs/PROCESS.md` — §2's first standing-constraint paragraph rewritten to generalize the scope
  clause; second paragraph (frozen-historical-count exception) untouched.
- `docs/gates/CONF-SURFACE.md` — new numbered bound (9) added to `## Disclosed bounds`, naming the
  structurally-unreachable occurrence, its reason, and the two rejected alternatives; Facts fence
  `disclosed_bounds_anchors` regenerated from 9 to 10 entries by `--write`.
- `scripts/gen-gate-docs.py` — `LITERAL_SCAN_DISCLOSED_BOUNDS` gained one new anchor string,
  `component-diagram-mermaid-fence-unreachable`.
- `CLAUDE.md`, `docs/ARCHITECTURE.md` — CONF-SURFACE's generated gate-table row updated
  (`disclosed_bounds_anchors=9` → `=10`) as the mechanical `--write` regeneration side effect of
  the anchor count moving; no other cell on either row changed.

## Decisions Made

See `key-decisions` in the frontmatter above (verbatim, not repeated here per `docs/PROCESS.md`
§1's own citation-not-restatement rule).

## Deviations from Plan

None — plan executed exactly as written. No auto-fix was needed on either task; both drafted
paragraphs passed their in-process scans on the first attempt after minor pre-drafting rewording
(removing spelled-out count words like "six"/"one" adjacent to a count noun) done before any text
was written to disk, which is the plan's own mandated drafting discipline, not a deviation from
it.

## Issues Encountered

The first draft of bound (9)'s prose used "six containment-unreachable narrative surfaces" and
"...for the same reason bound (8) rejects one — a control..." — both tripped
`_scan_text_for_literal_hits()` in the in-process dry run (2 hits: `'six containment-unreachable
narrative surfaces'`, `'one — a control'`). Reworded to avoid the count-noun-adjacent spelled-out
numbers ("every containment-unreachable narrative surface named in NARR-02's scope", "...rejects a
control asserting its own presence — a control demonstrating..."), re-ran the scan, got zero hits,
then wrote to disk. This is the plan's own prescribed drafting discipline working as designed, not
an issue requiring a fix — recorded here because it is the concrete instance of "test draft prose
in-process before writing it to disk" the plan's `<read_first>` warns Phase 25 lost time on twice.

## In-Process Verification Transcripts

**Task 1 — `_scan_text_for_literal_hits()` over the exact final first-paragraph text, before
writing to disk:**

```
hits: 0
```

**Task 1 — ledger key-set readings, both taken by module import of `scripts/gen-gate-docs.py`:**

| Reading point | Sorted `_DEFERRED_LITERAL_HITS` keys where surface = `docs/PROCESS.md` | `len(_DEFERRED_LITERAL_HITS)` | `_DEFERRED_LEDGER_MAX` | `len(_DEFERRED_CONTAINMENT_HITS)` | `_CONTAINMENT_LEDGER_MAX` |
|---|---|---|---|---|---|
| Immediately before the edit | 30 keys (listed below) | 181 | 181 | 26 | 26 |
| Immediately after the edit | identical 30 keys, same order | 181 | 181 | 26 | 26 |

The 30 `docs/PROCESS.md` keys (identical both readings):
`"13 plans,"`, `'gate and the five')`,`, `(32 falsification arms,`, `(4 plans,`,
`**13 gap-closure plans`, `1 (4 plans,`, `13 gap-closure plans`, `13 plans,`, `16 gates`,
`16 rows`, `17 rows`, `2 gap-closure plans`, `2 plans`, `2 was plans`, `3 was plans`,
`4 was plans`, `Two plans,`, `four literals`, `four plans`, `item — one`, `literals to one`,
`literals — at two`, `one verification → plan`, `plans 21-17..21-20, four`, `plans across 4`,
`plans closed three`, `plans to three`, `plans," "4`, `plans," "4 rounds," "41%,"`, `two plans`.

`git diff docs/PROCESS.md` confirmed the edit is confined to the first standing-constraint
paragraph; the frozen-historical-count paragraph appears in the diff as unchanged context only.

**Task 2 — the full census, by command:**

```
$ python3 scripts/check-traceability.py --describe | ... coverage_headline
prose: "208 reproducible / 97 audit-only / 0 gap / 305 total"
slash: "208/97/0/305"
```

Per-surface grep for both live strings, followed by per-occurrence classification
(`_fenced_line_flags`, `_generated_marker_pairs_for`/`_generated_line_flags`,
`_delta_chain_hops`/`_link_delta_chains`, all via direct module import):

| Surface | Line | Kind | Fenced | In-region | Chain-hop | Class |
|---|---|---|---|---|---|---|
| docs/PROCESS.md | — | — | — | — | — | (no occurrence) |
| docs/README.md | 20 | prose | False | False | False | region candidate |
| CONTRIBUTING.md | — | — | — | — | — | (no occurrence) |
| docs/MEASUREMENT-MAP.md | 54 | prose | False | False | False | region candidate |
| docs/COMPONENT-DIAGRAM.md | 98 | slash | True | False | False | structurally unreachable |
| docs/DATA-FLOW.md | — | — | — | — | — | (no occurrence) |
| CLAUDE.md | 312 | prose | False | False | False | region candidate (plan 26-05's target, not NARR-02's) |

Chain-hop check: `_delta_chain_hops()` over `docs/README.md`, `docs/MEASUREMENT-MAP.md`,
`docs/COMPONENT-DIAGRAM.md` and `CLAUDE.md` found hop spans touching `208`/`97`/`305`
(`docs/README.md`: `'133/96 → 132/97'`, `'286 → 305'`; `CLAUDE.md`: `'133/96 → 132/97'`,
`'132/97 → 126/88,'`, `'192/94 → 208/97,'`, `'286 → 305'`), none of which match the coverage-
headline occurrence lines themselves (20/54/98/312 respectively) — confirming none of the four
occurrences is a chain hop.

**Arithmetic:** on the six-surface (NARR-02) set, 3 occurrences total = 2 region candidates + 1
structurally unreachable + 0 frozen historical (`2 + 1 + 0 = 3`). The `CLAUDE.md` occurrence is
recorded separately (1), per the plan's own instruction that it is plan 26-05's target.

**Task 2 — `_scan_text_for_literal_hits()` over the exact final bound-(9) text, before writing to
disk (after the reword described in "Issues Encountered"):**

```
literal scan hits: 0
```

**Task 2 — `detail_page_containment_problems()` over the same bound-(9) text**, run with the exact
`check_spelled_out=False` polarity `cmd_check()` actually uses for `docs/gates/CONF-SURFACE.md`
(its stem, `CONF-SURFACE`, is a `NARRATIVE_ENTRIES` member):

```
missing (check_spelled_out=False): []
```

**Task 2 — ledger readings, both taken by module import, before and after the bound edit and the
`--write` regeneration:**

| Reading point | `len(_DEFERRED_LITERAL_HITS)` | `_DEFERRED_LEDGER_MAX` | `len(_DEFERRED_CONTAINMENT_HITS)` | `_CONTAINMENT_LEDGER_MAX` |
|---|---|---|---|---|
| Before Task 2's edit | 181 | 181 | 26 | 26 |
| After Task 2's edit + `--write` | 181 | 181 | 26 | 26 |

**`disclosed_bounds_anchors` before/after**, from `docs/gates/CONF-SURFACE.md`'s regenerated Facts
fence: `9` → `10` (grew by exactly one, the new
`component-diagram-mermaid-fence-unreachable` anchor).

**Automated verify commands run, both tasks, both green:**

```
python3 scripts/gen-gate-docs.py --self-test   # SELF-TEST PASS — 96 controls run
python3 scripts/gen-gate-docs.py --check        # harvested 22/22 expected script-backed entries; exit 0
sh .githooks/pre-commit                          # all five gates PASS, exit 0 (run before each commit)
bash scripts/check-firewall-battery.sh           # FIREWALL: GREEN (26/26)
```

`git diff --diff-filter=D --name-only HEAD~1 HEAD` returned empty after each commit — no
unexpected deletions. `git status --porcelain` clean after each commit.

## Assumption Drift (advisory)

None material. The plan's own `<interfaces>` block pre-named the six containment-unreachable
surfaces, the live harvest field (`coverage_headline`), and the exact functions to import; all
matched what was found with no drift. One minor color note, not drift: the plan's `<read_first>`
pointed at `26-PATTERNS.md` for §2's verbatim quote, but that file does not exist in this phase
directory (only `26-CONTEXT.md` and `26-RESEARCH.md` do) — the verbatim quote was instead read
directly from `docs/PROCESS.md` itself, which is the authoritative source anyway, so this did not
affect the plan's execution.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- Plan 26-03 (NARR-02's mechanism landed inert: region roster, equality-floored lock, sentence
  renderer, restatement census, exemption-class entry, self-test controls) can proceed: the two
  region candidates this plan measured (`docs/README.md:20`, `docs/MEASUREMENT-MAP.md:54`) are the
  concrete targets 26-03/26-04 will wire regions onto, and the structurally-unreachable residue
  (`docs/COMPONENT-DIAGRAM.md:98`) is already published so 26-03/26-04 do not need to rediscover or
  re-justify excluding it.
- No blockers. Both ledgers confirmed unmoved (181/181, 26/26), which is the precondition the
  phase's own wave ordering (migrate first, re-pin last) depends on for waves 3-6.

---
*Phase: 26-migration-apply-reconcile-generalize-enforce*
*Completed: 2026-09-10*

## Self-Check: PASSED

- FOUND: `docs/PROCESS.md`
- FOUND: `docs/gates/CONF-SURFACE.md`
- FOUND: `scripts/gen-gate-docs.py`
- FOUND: `CLAUDE.md`
- FOUND: `docs/ARCHITECTURE.md`
- FOUND: `.planning/phases/26-migration-apply-reconcile-generalize-enforce/26-02-SUMMARY.md`
- FOUND: commit `2162730` in `git log --oneline --all`
- FOUND: commit `b82092b` in `git log --oneline --all`
