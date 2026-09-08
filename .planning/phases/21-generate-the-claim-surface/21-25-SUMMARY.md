---
phase: 21-generate-the-claim-surface
plan: 25
subsystem: gate-registry-claim-surface
tags: [roster-arm-census, conf-surface, narrative-join, over-claim-pin, gen-gate-docs]
dependency-graph:
  requires: ["21-24"]
  provides: []
  affects: ["scripts/gen-gate-docs.py", "docs/gates/CONF-SURFACE.md", "CLAUDE.md", "docs/ARCHITECTURE.md"]
tech-stack:
  added: []
  patterns: ["RosterArmShape/RosterArmUnreached NamedTuple rosters", "confsurface_census_narrative_problems (version01_narrative_problems precedent)", "_CENSUS_OVERCLAIM_PHRASES whitespace-normalized pin"]
key-files:
  created: []
  modified:
    - scripts/gen-gate-docs.py
    - docs/gates/CONF-SURFACE.md
    - CLAUDE.md
    - docs/ARCHITECTURE.md
key-decisions:
  - "Both moves the round-3 verifier offered, not one: widen the census to include the demonstrated value-bearing spelling AND rewrite the published claim as a spelling-level scan over a named, enumerated shape set — narrowing alone would leave a detected spelling undetected, widening alone cannot make a universal true."
  - "The over-claim pin (_CENSUS_OVERCLAIM_PHRASES) is seeded with four entries, not two — the page's sentence and its bare fragment, plus both docstring twins Task 1 corrected — because a pin seeded only from the page's wording would never fire on either docstring regressing."
  - "The narrative-join control is --self-test only, matching version01_narrative_problems' verified live placement, not wired into cmd_check() — a property of hand-written prose against live code, not of generated-output drift, and --self-test already runs in the battery, CI and both pre-commit hooks."
  - "No guard-of-guard control added; the depth rule is Phase 22's (CONF-14) and 21-CONTEXT.md's <deferred> section forbids pre-empting it here."
requirements-completed: [CONF-11, CONF-12, CONF-13]
metrics:
  duration: "~40min"
  completed: 2026-09-07
---

# Phase 21 Plan 25: Close CR-01's fourth recurrence — narrow the census's claim to what it verifies, widen it to what round 3 demonstrated Summary

Replaced `roster_arm_shape_census_problems()`'s two loose regexes with a named, enumerated
`_ROSTER_ARM_SHAPES` roster (three spellings, including the value-bearing clause-marker spelling
`21-VERIFICATION.md` round 3 demonstrated live), named the four escape routes it cannot reach in
`_ROSTER_ARM_UNREACHED` with the largest published as a read-only measurement, corrected both
docstring twins of the false shape-universal, rewrote `docs/gates/CONF-SURFACE.md`'s census
paragraph to state what the mechanism actually is, and added a registered narrative-join control
(`confsurface-census-narrative-joined`) binding every named id to the live rosters by set equality
in both directions plus a locked over-claim pin so the superseded sentence cannot return to any of
the three surfaces it lived on. Also silenced the false `NON-DETERMINISTIC` diagnostic that printed
on every clean self-test run, fixed two stale self-descriptions in the generator's own source, and
regenerated the claim surface — `bash scripts/check-firewall-battery.sh` reports `FIREWALL: GREEN
(26/26)`.

## What was done

### Task 1 — Name the census's shapes and unreached routes, add the value-bearing spelling

**Precondition (measured before any edit):** in-process scan of `_roster_arm_census_sources()`
(29-file population) for the value-bearing spelling returned **0** hits — plan 21-24 had already
landed, confirming it was safe to widen.

Replaced the two loose module-level regexes with `RosterArmShape` (a `NamedTuple`: `shape_id`,
`pattern`, `clause_identifier_exempt`, `finding_text`) and a single roster, `_ROSTER_ARM_SHAPES`,
registering three spellings:
- `roster-arm-synthetic-id-membership` (existing wave-15 shape)
- `roster-arm-bare-clause-marker` (existing check-version-stamps.py pre-21-17 shape)
- `roster-arm-value-bearing-clause-marker` — **new**: `r'"(?:missing=|extra=)[^"]+"' r"\s+in\s+([A-Za-z_][A-Za-z0-9_]*)\b"`, a one-or-more quantifier (not zero-or-more) keeping it
  disjoint from the bare shape. Written split across two adjacent string literals so the pattern's
  own on-disk source cannot self-match the shape it defines.

Added `RosterArmUnreached` (`route_id`, `reason`) and a roster of four named escape routes:
`roster-arm-unreached-payload-substring`, `roster-arm-unreached-other-spellings`,
`roster-arm-unreached-outside-scripts`, `roster-arm-unreached-semantic-correctness`. The first is
published as a read-only measurement, `_roster_arm_payload_assert_site_count()` /
`roster_arm_payload_assert_sites` in `describe()`'s `derived_counts` — never fed into any findings
list, never turns `--check` red.

Rewrote the scan loop to iterate `_ROSTER_ARM_SHAPES`, so every finding names its `shape_id`.

**Corrected both docstring twins of the false universal:**
- `_control_roster_arm_shape_census` no longer says the population "carries none of the defective
  roster-arm shapes"; it now states that no member matches any spelling in `_ROSTER_ARM_SHAPES`,
  the population equals the live glob, and the scan is spelling-level with named unreached routes.
- `roster_arm_shape_census_problems` no longer says it scans for "the two defective roster-arm
  shapes above"; it now describes a spelling-level match against `_ROSTER_ARM_SHAPES`.

**SOURCE — the vacuous-grep demonstration (run before either docstring was edited):**

| Check | Method | Result |
|---|---|---|
| `_control_roster_arm_shape_census` docstring contains "carries none of the defective roster-arm shapes" | `/usr/bin/grep -c` on the unmodified file | `0` — VACUOUS (wraps after "carries none of the") |
| `roster_arm_shape_census_problems` docstring contains "the two defective roster-arm shapes" | `/usr/bin/grep -c` on the unmodified file | `0` — VACUOUS (wraps after "the two defective") |
| Same two checks | whitespace-collapsed `__doc__` substring test | `True` / `True` |

This is the concrete proof that a single-line grep over a hard-wrapped docstring is a vacuous
criterion — it reports `0` whether or not the defect is present. **After the edit**, the identical
collapsed-`__doc__` check returns `False` / `False` for both.

Extended `_control_roster_arm_shape_census_vacuity` with a fourth fixture (the value-bearing
spelling) and a fifth (its clause-split fixed form), assembled across physical source lines per
the file's own self-match convention; asserts three fixtures fire and two fixed forms do not.

**Lowered the self-file non-module-docstring ratchet pin 30 → 29** (`_SELF_FILE_NONMODULE_DOCSTRING_HITS`):
rewording the vacuity control's docstring removed its one pre-existing hit ("two fixture strings")
without adding a replacement — a genuine shrink, re-pinned in the same commit per the ratchet's own
rule.

**Verification (in-process, this task's own changes):**

```
BEHAVIOR: roster_arm_shape_census_problems() over the real 29-file population -> []
FALSIFICATION 1 (new shape fires): fed synthetic source with the value-bearing spelling
  BEFORE (original code): []
  AFTER  (new code):      ['scripts/fixture-valuebearing-demo.py:1: value-bearing clause-marker
                            membership test against a whole message
                            [roster-arm-value-bearing-clause-marker]: ...']
FALSIFICATION 2 (fixed form not caught): clause-split "'c' in extra_clause" -> []
FALSIFICATION 3 (no self-match): scripts/gen-gate-docs.py confirmed IN the population (True);
  live census over the whole population -> []
FALSIFICATION 4 (measurement is derived): monkeypatched population with 3 known payload-assert
  lines -> derived_counts['roster_arm_payload_assert_sites'] moved from the live figure to 3
FALSIFICATION 5 (measurement never gates): same synthetic population -> roster_arm_shape_census_
  problems() still [] — the payload-assert count is read-only and does not feed any finding
```

Known transient state at the end of this task: `--self-test` failed exactly 2 pre-existing controls
(`check-dispatch-wired`, `check-reports-full-drift-count`) — both due to expected `DRIFT: CLAUDE.md`
(the CI-gate-table cell hadn't been regenerated yet). All 73 controls executed; isolated to those
two, both resolved by Task 3's `--write`.

Commit: `fed00de`.

### Task 2 — Replace the false universal on CONF-SURFACE.md, bind it with a narrative-join control

**Before (superseded sentence, on disk before this task):**
> "A separate, permanent self-test control — distinct from the literal-scan taxonomy above —
> proves that every `.py` file directly under `scripts/` asserts a roster-mismatch finding against
> an extracted clause, never against a whole message."

**After (full replacement paragraph set), quoted in full:**
> "**The roster-arm shape census.** A separate, permanent self-test control — distinct from the
> literal-scan taxonomy above — scans for an enumerated, NAMED set of defective spellings:
> `roster-arm-synthetic-id-membership`, `roster-arm-bare-clause-marker`, and
> `roster-arm-value-bearing-clause-marker`. This is a spelling-level scan for named spellings, **not
> a guarantee about assertion SHAPE in general** — a whole-message assertion written in any spelling
> outside this named set passes the scan clean. The `roster_arm_census_population` and
> `roster_arm_census_shapes` fields in the Facts fence above are the live, derived population size
> and shape-roster size; neither is restated by hand here.
>
> The routes this scan cannot reach are named too, rather than left an unbounded admission:
> `roster-arm-unreached-payload-substring` (a whole-message assertion against `problems[0]`, or any
> other joined finding — its live population size is published, read-only and gating nothing, as
> `roster_arm_payload_assert_sites` in the Facts fence above), `roster-arm-unreached-other-spellings`
> (any other way of writing a whole-message membership test; the spelling set named above is
> closed), `roster-arm-unreached-outside-scripts` (`.py` files not directly under `scripts/`), and
> `roster-arm-unreached-semantic-correctness` (whether a roster arm is semantically right, which no
> source-shape scan can see). `roster_arm_census_unreached` in the Facts fence above is the live,
> derived size of this unreached-route roster.
>
> **This paragraph previously stated an unscoped universal** about assertion SHAPE, and live
> counterexamples inside the census's own scanned population — confirmed live during this phase's
> round-three verification — falsified it. The correction above is a spelling-level scan over a
> named, enumerated set, never a claim about assertion shape in general.
>
> **The join itself is disclosed, not assumed.** Every shape id and route id named above is held to
> the live `_ROSTER_ARM_SHAPES` / `_ROSTER_ARM_UNREACHED` rosters by a registered self-test control
> (`confsurface-census-narrative-joined`) asserting SET EQUALITY in both directions — a shape added
> in code and not named here is a finding, and an id named here that does not exist in code is a
> finding too — and the superseded sentence above is pinned so it cannot return to this page or to
> the census docstrings it also lived on. This is an equality join plus a spelling-level pin on a
> single superseded sentence; it does not prove this page's narrative is honest in general, only
> that these named ids and that superseded sentence stay in sync with the live code.
>
> Its population was previously derived from the gate registry's own `ENTRIES`, which made
> `scripts/_gate_registry.py` — the module that DEFINES those entries — structurally unable to ever
> appear in its own census; that gap is closed by widening the population to a live directory glob,
> recorded during this phase's round-two verification."

Added `confsurface_census_narrative_problems(page_text=None, shape_ids=None, route_ids=None) ->
list[str]`, modelled on `version01_narrative_problems`: isolates hand-written text via
`_generated_line_flags`, collapses whitespace before matching (the page is hard-wrapped), extracts
every backticked `roster-arm-[a-z0-9-]+` token and requires SET EQUALITY with the union of live
shape/route ids (both directions — a live id missing from the page, or a page id not in code, is a
finding), reports an empty extracted set as a finding, and rejects any occurrence of a phrase in a
locked module-level tuple `_CENSUS_OVERCLAIM_PHRASES` (four entries, whitespace-normalized) on the
isolated page text AND on the two corrected census docstrings — never on this module's own
`__doc__` or whole source text.

**Registered where:** `confsurface-census-narrative-joined` in BOTH `_CONTROLS` and `_CONTROL_IDS`,
grep-confirmed present at both locations and called from NO line inside `cmd_check()` (only from
`_control_confsurface_census_narrative_joined`, itself `--self-test`-only) — matching
`version01_narrative_problems`' verified live placement (defined once, called only from
`_control_version01_narrative_control_ids_live`, never from `cmd_check()`). **This does NOT give
the join `--check` coverage.** What is still load-bearing: `gen-gate-docs.py --self-test` is gate 4
of five pre-commit gates in both hook mechanisms, a CI job (`gen-gate-docs (CONF-SURFACE)`), and a
registered battery gate — a control that fails there blocks the commit, the push and the battery. A
bare `--check` invocation on its own (nothing in this repo's gate set does that in isolation) would
not re-evaluate this join.

**Verification:**

```
SOURCE: /usr/bin/grep -c 'never against a whole message' docs/gates/CONF-SURFACE.md -> 0 (was 1)
BEHAVIOR: confsurface_census_narrative_problems() against the real page and real rosters -> []
Self-test control count: 73 -> 74
```

**Eleven falsification arms, run against fresh `rsync -a --exclude .git` scratch copies (real tree
`git status --porcelain` confirmed empty before and after every one):**

| # | What | Command / mutation | Result | Exit |
|---|------|---------------------|--------|------|
| 1 | New shape fires (before/after pair) | in-process, identical fixture | before `[]`, after named finding with `roster-arm-value-bearing-clause-marker` | n/a |
| 2 | Fixed form not caught | in-process | `[]` | n/a |
| 3 | No self-match | in-process on live population | `[]`, self file confirmed a member | n/a |
| 4 | Measurement derived | monkeypatch population | count moved to injected value | n/a |
| 5 | Measurement never gates | same monkeypatch | census findings unaffected | n/a |
| 6 | Over-claim rejected, wrapped then reflowed one line | synthetic page text | finding naming `never against a whole message`, both wrap forms | n/a (in-process) |
| 7 | Equality floor, code→prose | scratch copy: added `roster-arm-fake-extra-shape` to `_ROSTER_ARM_SHAPES`, page untouched | `--self-test` failed `confsurface-census-narrative-joined` naming the unnamed id | **1** |
| 8 | Equality floor, prose→code | scratch copy: added `` `roster-arm-something-invented` `` to the page | `--self-test` failed naming that id | **1** |
| 9 | Vacuity | scratch copy: stripped all `roster-arm-*` backticks from the page | `--self-test` failed with the vacuity finding | **1** |
| 10a | Superseded phrase restored — page docstring twin 1 | scratch copy: restored "never against a whole message" into `_control_roster_arm_shape_census`'s docstring | `--self-test` failed naming that phrase and `_control_roster_arm_shape_census`'s docstring | **1** |
| 10b | Superseded phrase restored, wrapped — docstring twin 1 | scratch copy: restored "carries none of the defective roster-arm shapes" wrapped exactly as it sat on disk (break after "carries none of the") | `--self-test` failed naming the phrase; paired `/usr/bin/grep -c` on the docstring text returns `0` (the one grep hit found is the pin's own module-level literal, not the docstring) | **1** |
| 10c | Superseded phrase restored, wrapped — docstring twin 2 | scratch copy: restored "the two defective roster-arm shapes" wrapped (break after "the two defective") in `roster_arm_shape_census_problems`'s docstring | `--self-test` failed naming the phrase; same paired grep-0 fact recorded | **1** |

**Deviation (Rule 1 — self-caused, auto-fixed inline):** this task's own new prose introduced two
CONF-13 count-noun-adjacent literals on the page ("pin on one", "ids and that one") and three in
the new control's docstring ("Four lettered legs:", "one live id,", "id — the two") — both caught
live by `--check`/the self-file docstring ratchet before commit and reworded (never exempted) to
avoid the count-noun adjacency; `literal_scan_non_exempt` stayed `0` and the self-file ratchet's
pin (29, set in Task 1) held unchanged, confirmed by re-running the checks after each reword.

Commit: `b9c3248`.

### Task 3 — Fix the four remaining source-level claims, regenerate, re-gate

**(i) False failure signal.** `_control_nondeterminism_exit_2` now wraps its `cmd_check()` call in
`contextlib.redirect_stdout`/`redirect_stderr` over `io.StringIO` (the `_control_check_dispatch_wired`
idiom) and additionally asserts the captured stderr contains `NON-DETERMINISTIC`, proving the
diagnostic actually fires rather than only that the return code is 2.

FALSIFICATION 11 (strengthened control still fires): on a scratch copy, silenced the diagnostic
write in `cmd_check()` while leaving the non-deterministic detection and `return 2` intact.
`--self-test` failed naming `nondeterminism-exit-2` with message `"cmd_check() returned 2 without
writing the NON-DETERMINISTIC diagnostic"` — **exit 1**. Real tree confirmed clean before and after.

**(ii) Stale `#` comment.** `"docs/gates/*.md",  # the 28 generated detail pages` (live count 31,
`/usr/bin/grep -n '28 generated detail pages'` found it at the old line 1988) replaced with a
comment naming the live source (`literal_scan_read_files`), no re-typed digit. `/usr/bin/grep -n
'28 generated detail pages' scripts/gen-gate-docs.py` now returns nothing. This literal was
invisible to CONF-13's own scanner by construction (`ast.get_docstring` does not see `#` comments)
— the second live demonstration of that disclosed bound (round 2 fixed three docstring literals;
this one sat one syntactic form outside that fix's reach).

**(iii) Stale block comment.** The comment above `LITERAL_SCAN_SURFACES`, which still described the
`.py` half as "every script-backed registry entry's module docstring" (the pre-21-23 shape),
rewritten to state the current live-glob-over-`scripts/*.py` fact and name plan 21-23 as the change
that made it so.

**(iv) Misattributed population size.** Added `literal_scan_py_population =
len(_py_docstring_scan_scripts())` to `describe()`'s `derived_counts`. Confirmed
`literal_scan_py_population == len(_py_docstring_scan_scripts()) == 29`, all three agree.
Repointed the page's `.py`-population paragraph — previously citing `literal_scan_surfaces` (37)
and `literal_scan_read_files` (67) as the population size, neither of which held it against the
real population of 29 — at `literal_scan_py_population`.

**Bound (4) verification (recorded, not edited into a widening):** read the live sentence first;
it already named "a comment or an in-code string constant" as out of reach, so **no widening of
that sentence was required** to close this round's second live demonstration. Added the one
genuinely missing sentence instead — the PUBLISHED SIZE of the blind spot
(`literal_scan_nonmodule_docstring_hits` / `literal_scan_nonmodule_docstring_surfaces`) measures
non-module DOCSTRINGS only, not `#` comments, so the published figure UNDERSTATES this bound's true
reach.

**Regeneration.** `python3 scripts/gen-gate-docs.py --write` regenerated exactly the predicted
cells across three files — `CLAUDE.md`, `docs/ARCHITECTURE.md`, `docs/gates/CONF-SURFACE.md`
(`git diff --stat` confirms only these three files moved; `docs/TESTING.md` and every other
`docs/gates/*.md` page unchanged). `CLAUDE.md`'s and `docs/ARCHITECTURE.md`'s CONF-SURFACE cell
moved `derived_counts=19 entries` → `23 entries`, `disclosed_bounds_anchors=7` → `8`,
`control_ids=73; control_count=73` → `control_ids=74; control_count=74` — nothing else in either
cell moved.

**Post-write verification, all green:**

```
python3 scripts/gen-gate-docs.py --self-test  -> "gen-gate-docs: SELF-TEST PASS — 74 controls run" (was 73), EMPTY stderr
python3 scripts/gen-gate-docs.py --check      -> exit 0, "harvested 22/22 expected script-backed entries (22 total)", zero DRIFT:, zero literal-scan:
sh .githooks/pre-commit                        -> exit 0, no NON-DETERMINISTIC line
sh scripts/git-hooks/pre-commit                -> exit 0, no NON-DETERMINISTIC line
python3 scripts/check-links.py --self-test              -> exit 0
python3 scripts/check-registration.py --self-test       -> exit 0 (29 controls)
python3 scripts/check-quality-harness.py --self-test    -> exit 0, all four contract sub-checks PASSED
python3 scripts/report-conformance.py --check           -> "PASS — no drift"
bash scripts/check-firewall-battery.sh                   -> FIREWALL: GREEN (26/26)
```

`literal_scan_non_exempt` = `0` (unchanged); `len(_DEFERRED_LITERAL_HITS)` = `135` (unchanged from
its pre-plan value — the same 135 the Facts fence carried before any edit in this plan). All three
CONTRACT-06 sha256 pins (`_chain_block_well_formed`, `_conclusion_claims`, `_slice_sections`)
verified byte-unchanged via `check-quality-harness.py --self-test`'s pin sub-checks. Battery total
unchanged at 26; no new CI job; no new battery gate; no new REG-GUARD exemption; no detector
threshold loosened; no exemption class or ledger entry touched; no guard-of-guard control added.

Commit: `95d377f`.

## Final derived-counts snapshot (all `len()`-derived, none hand-typed)

| Field | Value | Checked against |
|---|---|---|
| `roster_arm_census_population` | 29 | live glob of `scripts/*.py` |
| `roster_arm_census_shapes` | 3 | `len(_ROSTER_ARM_SHAPES)` |
| `roster_arm_census_unreached` | 4 | `len(_ROSTER_ARM_UNREACHED)` |
| `roster_arm_payload_assert_sites` | 40 | line-count of `_ROSTER_ARM_PAYLOAD_ASSERT_RE` matches across the population (read-only; moved during development as the value-bearing vacuity fixture's own `in problems[0]` line was added — a genuine new source line, not a hand-typed number) |
| `literal_scan_py_population` | 29 | `len(_py_docstring_scan_scripts())`, and matches the shell count of `scripts/*.py` |
| `disclosed_bounds_anchors` | 8 (was 7) | `LITERAL_SCAN_DISCLOSED_BOUNDS` |
| `control_ids` / `control_count` | 74 (was 73) | `_CONTROL_IDS` |

## Explicit statements required by this plan's `<output>`

- **No producer function's message text changed.** The three roster-drift message formats
  (`D-07 ROSTER DRIFT: ...`, `D-04 CORPUS ROSTER DRIFT: ...`, `D-20 LIVE ROSTER DRIFT: ...`) from
  plan 21-24 are untouched by this plan; this plan only widened the SCANNER that reads those and
  other files' source text.
- **No exemption class, ledger entry, or CONTRACT-06 pin was touched.** Confirmed via
  `literal_scan_non_exempt = 0`, `len(_DEFERRED_LITERAL_HITS) = 135` (unchanged), and
  `check-quality-harness.py --self-test`'s pin sub-checks all PASSED.
- **No guard-of-guard control was added.** `confsurface-census-narrative-joined` guards the claim
  surface; nothing guards it in turn — that is Phase 22's (CONF-14) per `21-CONTEXT.md`'s
  `<deferred>` section.
- **Battery total unchanged at 26**; no new CI job; no new battery gate; no new REG-GUARD exemption.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 — Bug, self-caused] New prose introduced CONF-13 count-noun-adjacent literals**
- **Found during:** Task 2, first `--check` run after rewriting the page and adding the control.
- **Issue:** Two phrases on `docs/gates/CONF-SURFACE.md` ("pin on one", "ids and that one") and
  three in `_control_confsurface_census_narrative_joined`'s new docstring ("Four lettered legs:",
  "one live id,", "id — the two") were caught as new hand-maintained count literals by CONF-13's
  standing scanner and the self-file non-module-docstring ratchet.
- **Fix:** Reworded both surfaces to remove the count-noun adjacency without changing meaning
  ("a single superseded sentence" / "that superseded sentence"; "Lettered legs (a)-(d)" / "a live
  id" / "both directions").
- **Files modified:** `docs/gates/CONF-SURFACE.md`, `scripts/gen-gate-docs.py`.
- **Verification:** `--check` returned to zero `literal-scan:` findings; the self-file ratchet held
  at its Task-1 pin (29) with no further change needed.
- **Committed in:** `b9c3248` (Task 2 commit — fixed inline before that commit landed).

**2. [Rule 1 — Bug, self-caused] Task 1's own docstring wording tripped the self-file ratchet**
- **Found during:** Task 1, first `--self-test` run after adding the new regex/roster comments.
- **Issue:** A new docstring sentence for `_roster_arm_payload_assert_site_count` literally
  contained the phrase "in problems[0]", moving `literal_scan_nonmodule_docstring_hits` and
  tripping no floor directly, but a separate rewording of `_control_roster_arm_shape_census_
  vacuity`'s docstring (needed to add the new fixtures) removed a pre-existing count-noun hit,
  taking the self-file ratchet from 30 to 29 live hits against its 30 pin.
- **Fix:** Reworded the `_roster_arm_payload_assert_site_count` docstring to reference the regex by
  name rather than spell out the literal shape; re-pinned `_SELF_FILE_NONMODULE_DOCSTRING_HITS`
  30 → 29 in the same commit, per the ratchet's own repin-on-shrink rule, with a written reason.
- **Files modified:** `scripts/gen-gate-docs.py`.
- **Verification:** `nonmodule_docstring_selffile_ratchet_problems()` returns `[]` at 29/29;
  `--self-test`'s `selffile-docstring-ratchet-fires` / `-requires-repin-on-shrink` controls both
  passed.
- **Committed in:** `fed00de` (Task 1 commit — fixed inline before that commit landed).

---

**Total deviations:** 2 auto-fixed (both Rule 1, both self-caused by this plan's own new prose
tripping the exact CONF-13/self-file-ratchet machinery this milestone exists to keep honest).
**Impact on plan:** Both fixes are wording-only, necessary for CONF-13 correctness, and were caught
and closed before their respective task's commit landed — no scope creep, no exemption widened.

## Issues Encountered

None beyond the two self-caused deviations above, both anticipated in kind by the plan's own
"Line-wrap discrimination audit" table (a hard-wrapped docstring is invisible to a single-line
grep) and resolved the same way that audit prescribes: reword the artifact, never widen the check.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

`21-VERIFICATION.md` round 3's single BLOCKING gap is closed: the census now scans a named,
enumerated spelling set including the demonstrated value-bearing spelling, the page states exactly
that (never a shape universal), and a registered control fails in both directions the moment prose
and code disagree — with the superseded over-claim locked out of the page and both docstrings it
lived on. This is round 4 of gap-closure, following the same recorded-exception pattern as rounds
1-3; the exact `.planning/` edits this worktree cannot reach (a fourth `21-CONTEXT.md` `RECORDED
EXCEPTION` block, `.planning/ROADMAP.md`'s exception paragraph, `.planning/STATE.md`'s position
refresh) are the orchestrator's to apply post-merge — see the note below.

### For the orchestrator: `.planning/` edits this worktree could not make

`.planning/` is gitignored in this repo except for force-tracked `*-SUMMARY.md` files, so
`21-CONTEXT.md`, `ROADMAP.md` and `STATE.md` are absent from this worktree (confirmed:
`.planning/phases/21-generate-the-claim-surface/` here holds only `*-SUMMARY.md` and
`21-CONF13-BASELINE.md`). Per the orchestrator's own note, plan 21-24's round-4 `RECORDED
EXCEPTION` block, the ROADMAP "Four recorded exceptions" paragraph, and part of the STATE.md
position refresh have already been applied after 21-24 merged. What is still needed once 21-25
also merges:

1. **`.planning/phases/21-generate-the-claim-surface/21-CONTEXT.md`** — the round-4 `RECORDED
   EXCEPTION` block plan 21-24 specified (verbatim text is in `21-24-SUMMARY.md`) should already be
   present from that merge; no further edit is needed there for 21-25 specifically, since 21-25 is
   itself the second (and final) plan of round 4, already accounted for in that block's "2 more
   gap-closure plans (21-24, 21-25)" wording.
2. **`.planning/ROADMAP.md`** — the Phase 21 checklist line's parenthetical, which 21-24-SUMMARY.md
   flagged as deferred pending 21-25's completion, should now read reflecting **25 of 25** plans
   executed across 4 gap-closure rounds, round 4 complete (21-24 and 21-25 both landed), and the
   round-3 blocking gap (CR-01's recurrence) closed.
3. **`.planning/STATE.md`** — `## Current Position` should read `Plan: 25 of 25`, with
   `progress.completed_plans` incremented by 1 from wherever 21-24's merge left it, and
   `last_activity`/`last_updated` refreshed to this plan's completion timestamp.

## Self-Check: PASSED

- FOUND: `scripts/gen-gate-docs.py` (modified, contains `RosterArmShape`, `RosterArmUnreached`,
  `_ROSTER_ARM_SHAPES`, `_ROSTER_ARM_UNREACHED`, `confsurface_census_narrative_problems`,
  `_CENSUS_OVERCLAIM_PHRASES`, `_control_confsurface_census_narrative_joined`)
- FOUND: `docs/gates/CONF-SURFACE.md` (modified, contains the rewritten census paragraph with all
  seven `roster-arm-*` ids in backticks)
- FOUND: `CLAUDE.md`, `docs/ARCHITECTURE.md` (both regenerated, CONF-SURFACE cell shows
  `derived_counts=23 entries; disclosed_bounds_anchors=8; control_ids=74; control_count=74`)
- Commit `fed00de` (Task 1) — `git log --oneline --all | grep fed00de` → found
- Commit `b9c3248` (Task 2) — `git log --oneline --all | grep b9c3248` → found
- Commit `95d377f` (Task 3) — `git log --oneline --all | grep 95d377f` → found

---
*Phase: 21-generate-the-claim-surface*
*Completed: 2026-09-07*
