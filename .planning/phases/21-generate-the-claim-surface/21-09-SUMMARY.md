---
phase: 21-generate-the-claim-surface
plan: 09
subsystem: tooling
tags: [conf-13, literal-scanner, drift-gate, generator, exemption-taxonomy, coverage-floor]
status: complete

# Dependency graph
requires:
  - phase: 21-generate-the-claim-surface
    plan: 08
    provides: "The landed claim surface: docs/gates/<GATE-ID>.md pages,
      CLAUDE.md's and docs/ARCHITECTURE.md's generated CI-gate tables, and
      the D-06 containment rule with its citation/identifier exemption
      vocabulary."
  - phase: 21-generate-the-claim-surface
    plan: 01
    provides: "21-CONF13-BASELINE.md: the measured, noise-filtered
      hand-maintained-count-literal figure (79 scanner-target / 15 exempt
      out of 250 raw hits), its detection vocabulary, and its exemption
      taxonomy with written reasons."
provides:
  - "scripts/gen-gate-docs.py's standing CONF-13 literal scanner:
    LITERAL_SCAN_SURFACES (8 Markdown globs + 20 derived .py
    module-docstring scripts), the generated-fence discriminator, seven
    named LITERAL_EXEMPTION_CLASSES, a read loop (run_literal_scan)
    recording read_relpaths, a coverage floor whose signature takes the
    read record itself, and literal_scan_problems() wired into cmd_check()
    alongside the existing drift and D-06 checks."
  - "The anticipatory CONF-SURFACE registry entry's own --describe is now
    harvested (generate_all()/cmd_check() pass the full ENTRIES list to
    harvest(), not just the non-anticipatory subset), so
    docs/gates/CONF-SURFACE.md's Facts fence carries real, derived counts
    instead of a placeholder."
  - "The post-generation live reading: 156 non-exempt residual hits across
    29 registered surfaces (56 files actually opened), handed to plan
    21-10 as its remediation target; the scanner was not weakened to
    reach exit 0."
  - "A recorded stale-figure survivor (docs/COMPONENT-DIAGRAM.md's
    hyphen-compound gate-count sentence) that the scanner is structurally
    blind to, for plan 21-10 to remediate by hand."
affects: [21-10, 21-11, 21-12]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "generated-fence discriminator reuse: the CONF-13 scanner's
      _generated_marker_pairs_for()/_literal_hits_outside_generated()
      reuse the SAME _generated_line_flags() helper and the SAME
      CLAUDE_REGION_MARKERS/ARCHITECTURE_REGION_MARKERS/_ALL_DETAIL_MARKER_PAIRS
      constants D-06's containment check and the region-replacement
      primitive already use — one implementation of 'is this line inside a
      generated fence', not a second."
    - "derived .py surface list, not hand-typed twice: _py_docstring_scan_scripts()
      calls the pre-existing _expected_harvest_scripts() rather than
      re-transcribing the baseline's 20-script PY_DOCSTRING_SURFACES list —
      closes 21-CONF13-BASELINE.md's own disclosed hand-transcription
      bound ('plan 21-09's standing scanner is expected to derive this set
      programmatically... rather than hand-list it a second time')."
    - "coverage-floor signature discipline (HEADLINE-LOCK block (m)):
      literal_scan_coverage_floor_problems(read: LiteralScanRead, ...)
      takes the LiteralScanRead record itself as its first parameter, never
      a glob-derived set[str] — asserted directly via
      inspect.signature(...).parameters['read'].annotation, so a
      glob-derived substitute is unexpressible at the call site."
    - "detection-time exclusions vs. exemption classes, kept distinct: the
      ordinal/label-adjacency exclusion, the exit-code-line exclusion, and
      section-reference blanking (ported verbatim from
      conf13_sweep.py::scan_text) identify text that never made a count
      claim at all, so they live in _scan_text_for_literal_hits() (what
      counts as a candidate hit); LITERAL_EXEMPTION_CLASSES permits a
      genuine count claim for a named, written reason. The two are not
      merged."
    - "the harvest() call sites in generate_all()/cmd_check() now pass
      _gate_registry.ENTRIES (the FULL list) rather than a non-anticipatory
      filter — CONF-SURFACE's own script exists now, so its own --describe
      is safe and correct to run; _ANTICIPATORY_KEYS still correctly
      excludes it from the D-01 battery-id floor and the live table
      row count, which is the invariant it was protecting."

key-files:
  created: []
  modified:
    - scripts/gen-gate-docs.py
    - scripts/_gate_registry.py
    - docs/gates/CONF-SURFACE.md

key-decisions:
  - "CONF-SURFACE was added to NARRATIVE_ENTRIES so its detail page can
    carry a hand-written 'Disclosed bounds' narrative that survives
    regeneration — matching the shape the plan's own action names ('the
    R7/R9/R10 voice'). Its Facts fence is populated from the SAME
    describe()-derived blob every other narrative page uses, via the
    existing render_detail_page() region-preservation branch; no new
    mechanism was introduced."
  - "The scanner's exemption taxonomy implements exactly the classes the
    baseline measured with real hits (version-stamp-count,
    headline-provenance-delta, plan-number-identifier, retired-body-budget)
    plus the three CLAUDE.md-invariant classes the baseline measured at
    zero hits today (maxturns-60-value, sha256-digest,
    commonmark-heading-depth) — kept for completeness against future
    prose, not deleted as dead weight, since none of the three overlaps
    with the ordinal/label/exit-code detection-time exclusions already
    baked into scan_text."
  - "Detection-time false-positive exclusions (ordinal-label-reference,
    adjacency-mistrack, enumerated-list-marker — the baseline classifier's
    OWN separate false-positive layer, distinct from its exemption
    taxonomy) were deliberately NOT ported into the standing scanner. The
    plan's action names only the exemption taxonomy and the two structural
    tightening passes already inside scan_text (exit-code lines,
    ordinal-adjacent labels, section references); it does not ask for a
    third false-positive filter layer. Not weakening the scanner to reach
    exit 0 (an explicit acceptance criterion) means these residual false
    positives from real narrative prose are reported honestly as part of
    the 156 non-exempt hits, not silently absorbed."
  - "harvest() at both call sites (generate_all(), cmd_check()) was widened
    from the non-anticipatory ENTRIES subset to the FULL ENTRIES list, so
    CONF-SURFACE's own script (which now exists) is actually invoked for
    --describe. _ANTICIPATORY_KEYS' exclusion from the D-01 battery-id
    equality floor and the live ARCHITECTURE.md row-count floor is
    unchanged — those are the invariants _ANTICIPATORY_KEYS exists to
    protect, not 'never run this script'."

requirements-completed: [CONF-13]

# Metrics
duration: ~3 hours (single session)
completed: 2026-09-06
---

# Phase 21 Plan 09: Generate the Claim Surface (Standing Scanner) Summary

**Built CONF-13's standing hand-maintained-count-literal scanner inside `scripts/gen-gate-docs.py`
from `21-CONF13-BASELINE.md`'s measured taxonomy: a generated-fence-aware read loop over 29
registered surfaces, seven named exemption classes, a coverage floor bound to the read loop's own
record, and ten new self-test controls (36 -> 46) including three anti-vacuity neutralization arms.
Live reading: 156 non-exempt residual hits — handed to plan 21-10, not silently absorbed. Proved the
standing property (reappearance fires, removal un-fires) by reintroduction on a scratch copy across
three surface kinds, and swept the tree by hand for the stale-figure blind spot the scanner cannot
see, finding the one known instance (`docs/COMPONENT-DIAGRAM.md`'s hyphen-compound gate count).**

## Status: COMPLETE

## Performance

- **Duration:** ~3 hours, single session
- **Files modified:** `scripts/gen-gate-docs.py`, `scripts/_gate_registry.py`,
  `docs/gates/CONF-SURFACE.md`
- **Commits:** `a438f51` (Task 1 — the scanner itself, its exemption taxonomy, its ten controls,
  and the disclosed-bounds narrative). Task 2 required no further code changes — see "Task 2" below.

## Accomplishments

### Task 1: Re-measure post-generation, then implement the scanner and its exemptions

**Post-generation re-measurement, beside the baseline's prediction:**

| Reading | Surfaces | Files opened | Total hits | Non-exempt |
|---|---|---|---|---|
| `21-CONF13-BASELINE.md` (pre-generation) | 28 candidates (`docs/gates/*.md` vacuous — dir did not exist) | n/a (raw sweep, not a read-loop record) | 250 raw | 79 scanner-target |
| This plan's standing scanner (post-generation, live) | 29 (28 candidates + `docs/gates/*.md` now populated) | 56 | 173 | **156** |

**Discrepancy against the baseline's prediction, explained, not silently adopted:** the standing
scanner's non-exempt count (156) is materially HIGHER than the baseline's scanner-target figure
(79), for two structural reasons, both real and both recorded rather than papered over:

1. **The four `NARRATIVE_ENTRIES` pages' migrated prose is entirely new surface** the baseline could
   not measure (`docs/gates/*.md` was "0 (directory does not exist yet)" in the baseline). Plan
   21-08's migration moved ~43k characters of dense, citation-heavy narrative into
   `docs/gates/QUAL-01.md`, `SCAN-GUARD.md`, `TRACE-03.md`, `CONF-GATE.md` — exactly the surface
   D-06's own containment rule needed a citation-exemption vocabulary to survive (21-08-SUMMARY.md
   deviation #3). CONF-13's standing scanner has no equivalent vocabulary; it flags the same class
   of ordinary-language small numbers and parenthetical enumerations ("two contract surfaces",
   "(1) worked-example extraction", "Criteria 4 and 6" split across a noun-adjacency window) that
   D-06 had to specifically learn to ignore.
2. **The standing scanner does not port the baseline's own `conf13_classify.py` false-positive
   layer** (ordinal-label-reference, adjacency-mistrack, enumerated-list-marker) — a deliberate
   choice (see key-decisions): the plan's action names the exemption taxonomy and the two
   structural tightening passes already inside `scan_text` (exit-code lines, ordinal-adjacent
   labels, section references), not a third filter layer. A residual of this shape (~15-20 hits,
   e.g. `docs/README.md`'s "1. The **sync-drift gate**") is expected and reported honestly.

Both effects are structural properties of running the scanner against REAL, DENSE, POST-GENERATION
prose for the first time — the same "synthetic fixtures don't predict real prose" lesson plan
21-08's own Assumption Drift note already recorded for D-06. **Per the plan's explicit instruction,
the scanner was not weakened to reach exit 0** — `--check` exits 1, naming all 156 residual hits by
file and line, which plan 21-10 inherits as its remediation target.

**Implementation** (`scripts/gen-gate-docs.py`):

- `LITERAL_SCAN_MD_GLOBS` (8 entries, each with an inline comment) + `_py_docstring_scan_scripts()`
  (derived from `_expected_harvest_scripts()`, never hand-listed a second time) =
  `LITERAL_SCAN_SURFACES` (29 total).
- `_scan_text_for_literal_hits()` ports `21-CONF13-BASELINE.md`'s `conf13_sweep.py::scan_text`
  verbatim: digit/spelled-out/range forms, the exit-code-line exclusion, the ordinal-adjacent-label
  exclusion, and `§`-token blanking.
- `_generated_marker_pairs_for()` / `_literal_hits_outside_generated()`: the generated-region
  discriminator, reusing the EXISTING `_generated_line_flags()` helper and the existing
  `CLAUDE_REGION_MARKERS` / `ARCHITECTURE_REGION_MARKERS` / `_ALL_DETAIL_MARKER_PAIRS` constants —
  one implementation, not a second.
- `LITERAL_EXEMPTION_CLASSES` (7 entries): `version-stamp-count`, `headline-provenance-delta`,
  `plan-number-identifier`, `retired-body-budget` (all measured with real hits: 3, 11, 2, 1
  respectively in the live reading) plus `maxturns-60-value`, `sha256-digest`,
  `commonmark-heading-depth` (all measuring 0 live hits today, kept per the baseline's own
  instruction not to delete a named class as dead weight).
- `run_literal_scan()` returns a `LiteralScanRead(read_relpaths, hits, declined)` record; every
  candidate the loop declines to open is a named `INFO:` line (none fired live — all 29 surfaces
  resolved).
- `literal_scan_coverage_floor_problems(read: LiteralScanRead, surfaces=...)`: the floor's first
  parameter is the read record itself (asserted by `scan-coverage-floor-signature-locked` via
  `inspect.signature`), never a glob-derived `set[str]`.
- `literal_scan_problems()` / `literal_scan_attributions()`: one named finding per non-exempt hit,
  one diagnostic line per exempt hit naming its class.
- Wired into `cmd_check()` alongside the drift comparison and the D-06 containment check, all
  findings collected and reported together.
- **The anticipatory `CONF-SURFACE` registry entry's own `--describe` is now harvested**: both
  `generate_all()` and `cmd_check()` were widened from `harvest(non_anticipatory)` to
  `harvest(_gate_registry.ENTRIES)` — the script exists now (it did not when `_ANTICIPATORY_KEYS`
  was written), so its own detail page gets the same real, harvested Facts every other gate's page
  gets. `_ANTICIPATORY_KEYS`'s exclusion from the D-01 battery-id floor and the live table row
  count is unchanged. `_gate_registry.py`'s `CONF-SURFACE` entry gained a `consumes` tuple
  (`registered_surfaces`, `checked_files`, `derived_counts`, `disclosed_bounds_anchors`,
  `control_ids`, `control_count`, `locked_constants`) matching `describe()`'s emitted fields
  exactly — confirmed by D-04's bidirectional field-resolution floor reporting zero problems.
- Four disclosed bounds published in `docs/gates/CONF-SURFACE.md`'s hand-written narrative, in the
  R7/R9/R10 voice: (1) line-scoped detection, (2) currency-not-correctness, (3) the closed
  spelled-out vocabulary, (4) `.py` coverage is module docstrings only.

**Ten named isolation arms, all present and passing** (verified individually, not just via
`--self-test`'s aggregate PASS):

| Control | Result |
|---|---|
| `scan-hit-outside-fence-fires` | PASS |
| `scan-hit-inside-fence-passes` | PASS |
| `scan-exempt-class-attributed` | PASS |
| `scan-unattributable-permit-fires` | PASS |
| `scan-spelled-out-detected` | PASS |
| `scan-docstring-only` | PASS |
| `scan-coverage-floor-fires` | PASS |
| `scan-glob-narrowing-fires` | PASS |
| `scan-coverage-floor-signature-locked` | PASS |
| `scan-neutralization-arms` (bundles all three anti-vacuity arms) | PASS |

**Three neutralization observations, each restoring the original function afterward:**

1. Disabling the generated-region discriminator (`_generated_marker_pairs_for` -> always `()`)
   breaks `scan-hit-inside-fence-passes`: the fenced `47 controls` fixture text is no longer
   exempted, `hits == []` fails.
2. Disabling spelled-out normalisation (`_literal_is_num_atom` -> digit-only) breaks
   `scan-spelled-out-detected`: `"forty-seven controls were measured."` produces zero hits instead
   of one.
3. Replacing exemption attribution with an unconditional permit (`_literal_hit_exemption` -> always
   returns a class name) breaks `scan-unattributable-permit-fires`: the `9 branches` fixture (which
   matches no real class) is wrongly permitted, so `literal_scan_problems` returns `[]` instead of
   one finding.

`python3 scripts/gen-gate-docs.py --self-test` exits 0 with **46 controls** (up from 36 after plan
21-08). `python3 scripts/gen-gate-docs.py --check` exits **1**, naming all 156 residual non-exempt
hits — recorded, not weakened away.

### Task 2: Live reading, the standing-zero record, and the reappearance proof

**Live per-surface reading published as derived fact** in `docs/gates/CONF-SURFACE.md`'s generated
Facts fence (landed in Task 1's commit, since `render_detail_page()`'s existing region-preservation
mechanism required no separate step): `registered_surfaces` (29, the declared surface set),
`checked_files` (56, every file actually opened this run), `derived_counts` (11 entries: the
aggregate hit/non-exempt counts plus one `literal_scan_exempt_<class-name>` entry per exemption
class), `disclosed_bounds_anchors` (4). `gen-gate-docs.py --check` is clean of any D-06 containment
violation on this page — confirmed by rewriting the hand-written narrative to cite the Facts fence
by name rather than restating any bare digit outside it (a first draft that cited `156`/`173`/`29`
directly outside the fence was caught by D-06's own containment check and corrected before commit).

**Stale-figure hand sweep**, run against every file `run_literal_scan()` actually opened (56 files,
`read_relpaths`) plus a targeted search for the four figure classes the plan names by name:

```sh
# per-file loop over the 56 real paths in read_relpaths (registered_surfaces expanded,
# #__doc__ suffix stripped for .py files), run from the repo root:
while IFS= read -r f; do grep -Hn "23 rows\|27 rows" "$f"; done < <(...)
while IFS= read -r f; do grep -Hn "14-gate\|14 gate" "$f"; done < <(...)
while IFS= read -r f; do grep -Hn "22,742\|22,630\|9,336\|9,307\|8,195\|8,160\|3,010\|3,001" "$f"; done < <(...)
```

**Survivor list (one entry, matching the plan's named prediction):**

- **`docs/COMPONENT-DIAGRAM.md:66`** — `"For the full 14-gate inventory (the 12 CI gates, VAL-01
  through TRACE-03, plus the two pre-commit gates) see..."` The `14-gate` figure is stale (the
  current gate count is materially higher) AND it is **structurally invisible to the standing
  scanner**: `_literal_tokenize()` splits on whitespace, so `14-gate` is ONE token, and
  `_literal_is_num_atom("14-gate")` fails (the cleaned token is not a pure digit/word-number run) —
  confirmed live: `run_literal_scan()`'s hit list for this file contains `'12 CI gates,'` and
  `'two pre-commit gates)'` (both already inside the 156 non-exempt count) but **no hit at all**
  citing `14-gate`. This is exactly the detection gap the plan's acceptance criteria named by path
  and line (D-21-G) — a hyphen directly joining a number to its noun, with no space, evades
  noun-adjacency tokenization entirely. Recorded here as a named detection gap for plan 21-10 to
  fix by hand, not a defect this plan's own scanner design closes.

**No other survivors found.** The pre-unification row-count figures (`23 rows`, `27 rows`) and the
pre-split narrative-cell character counts (`22,742` / `9,336` / `8,195` / `3,010` and their
plan-21-08-summary-estimate siblings) return zero hits across every registered surface — both were
eliminated structurally by plan 21-08's migration, confirming `21-CONF13-BASELINE.md`'s own
prediction that the structural class "reaches 0 by construction... the moment [generation] lands."
(One incidental, out-of-scope match: `scripts/check-traceability.py`'s own docstring and
`HEADLINE-LOCK` self-test both cite `"23 rows"` describing the FROZEN v8.18 historical matrix
block — a pre-existing, correct, unrelated historical fact this phase did not move, not a survivor
of this phase's own restructuring.)

**Battery total note** (per the plan's own instruction, not a finding): every registered surface
currently states `FIREWALL: GREEN (25/25)` accurately — this is CORRECT today and will become
stale the moment plan 21-11 registers `CONF-SURFACE` into the battery (25 -> 26). Recorded here as
a forward-looking note for plan 21-11, not as a current stale-figure finding.

**Reappearance proof**, on an `rsync -a --exclude .git` scratch copy (never the real tree), adding
one sentence — `"There are 47 controls newly claimed here for the reintroduction proof."` — in
unfenced prose to three different registered surfaces of three different kinds:

1. A plain Markdown doc: `docs/MEASUREMENT-MAP.md` (appended, landing at line 101).
2. A `docs/gates/` page: `docs/gates/CONF-GATE.md` (appended, landing at line 64 — a
   `NARRATIVE_ENTRIES` page, so this ALSO tripped a D-06 containment finding on the same line, an
   expected additional signal, not a defect).
3. A `.py` module docstring: `scripts/check-links.py`, inserted directly after the docstring's
   first line (landing at docstring line 3, confirmed via `ast.get_docstring`).

`python3 scripts/gen-gate-docs.py --check` in the scratch copy, first run — **three findings**,
verbatim, each citing the correct file and line:

```
docs/MEASUREMENT-MAP.md:101: hand-maintained count literal '47 controls' (no exemption class matches)
docs/gates/CONF-GATE.md:64: hand-maintained count literal '47 controls' (no exemption class matches)
scripts/check-links.py#__doc__:3: hand-maintained count literal '47 controls' (no exemption class matches)
```

(A fourth, unrelated line also printed — `containment: docs/gates/CONF-GATE.md states '47' outside
a generated fence with no matching literal inside one (D-06)` — the pre-existing D-06 mechanism
correctly firing on the same injected sentence; not part of CONF-13's own three-finding count.)

Removed the `docs/gates/CONF-GATE.md` addition (reverted its two appended lines), re-ran `--check`
in the scratch copy — **two findings**, verbatim:

```
docs/MEASUREMENT-MAP.md:101: hand-maintained count literal '47 controls' (no exemption class matches)
scripts/check-links.py#__doc__:3: hand-maintained count literal '47 controls' (no exemption class matches)
```

Scratch copy deleted after use (`rm -rf`); `git status --porcelain` confirmed empty in the real
repo both before creating the scratch copy and after deleting it.

`python3 scripts/gen-gate-docs.py --self-test` exits 0 (46 controls). `python3 scripts/check-links.py`
exits 0 (274 links + 6 namespace refs, 128 files — unchanged). `bash scripts/check-firewall-battery.sh`
reports **FIREWALL: GREEN (25/25)**. `python3 scripts/_gate_registry.py --self-test` exits 0 (16
controls, confirming the `consumes` tuple addition satisfies D-04's field-resolution floor).
`python3 scripts/check-registration.py` and `python3 scripts/report-conformance.py --check` both
still PASS.

**Task 2 required no additional code changes** beyond what Task 1's commit already landed (the
Facts-fence recording via `render_detail_page()`'s existing region-preservation mechanism) — its
deliverables are the verification results recorded above, per the plan's own `<output>` instruction
to record them in this SUMMARY.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking issue] `harvest()` excluded the anticipatory `CONF-SURFACE` entry's own
script, making its `consumes` tuple structurally unsatisfiable**
- **Found during:** Task 1, wiring `CONF-SURFACE`'s `consumes` tuple to match `describe()`'s new
  fields
- **Issue:** `generate_all()` and `cmd_check()` both called `harvest(non_anticipatory)`, a list that
  excludes `CONF-SURFACE` by construction (`_ANTICIPATORY_KEYS`). Once `CONF-SURFACE` gained a
  non-empty `consumes` tuple, `_gate_registry._requested_fields_by_script()` (which does NOT
  exclude anticipatory entries) added `scripts/gen-gate-docs.py` to `requested`, while `emitted`
  never contained that key at all (harvest never invoked it) — D-04's bidirectional
  `field_resolution_problems()` floor would report every requested field as missing, permanently
  failing `--check`.
- **Fix:** Widened both `harvest()` call sites to pass `_gate_registry.ENTRIES` (the full list).
  `_ANTICIPATORY_KEYS`'s exclusion from the D-01 battery-id equality floor and the live
  `docs/ARCHITECTURE.md` row-count floor is untouched — those are the invariants the constant
  exists to protect, and the docstring's original reasoning ("script does not exist yet") no
  longer applies now that `gen-gate-docs.py` exists.
- **Files modified:** `scripts/gen-gate-docs.py`
- **Verification:** `python3 scripts/_gate_registry.py --self-test` (16 controls) and
  `python3 scripts/gen-gate-docs.py --self-test`/`--check` all pass with zero D-04/vocabulary
  problems; `harvested 21/21 expected script-backed entries (22 total, including the anticipatory
  CONF-SURFACE)` confirms the widened harvest without breaking the "expected" floor.
- **Committed in:** `a438f51`

**2. [Rule 1 - Bug] First draft of `docs/gates/CONF-SURFACE.md`'s disclosed-bounds narrative
restated Facts-fence figures as bare digits outside the fence, tripping D-06's own containment
check on the page describing that same containment mechanism**
- **Found during:** Task 2, running `--check` after adding the narrative
- **Issue:** The first draft cited `156`/`173` (the live hit counts) directly in prose, outside any
  generated fence, with no matching literal inside one on the same page (the standard D-06
  violation shape) — an ironic self-inflicted instance on the page documenting the scanner that
  polices exactly this class of literal.
- **Fix:** Rewrote the closing paragraph to point at the Facts fence by name ("the total hits
  found... lives in the Facts fence above as `derived_counts`, never restated by hand here") rather
  than re-transcribing any figure, following the same "point back, don't restate" fork plan 21-08
  used for `estimate-detail.md`/`theoretical-limit-detail.md`'s chain-form citations.
- **Files modified:** `docs/gates/CONF-SURFACE.md`
- **Verification:** `python3 scripts/gen-gate-docs.py --check` reports zero containment violations
  on `docs/gates/CONF-SURFACE.md` after the fix; the residual 156 non-exempt count is unchanged
  (this was a page-content fix, not a scanner-logic change).
- **Committed in:** `a438f51`

**Total deviations:** 2 auto-fixed (Rule 3, Rule 1). Neither required a Rule 4 architectural-change
checkpoint — both are narrow, mechanical fixes surfaced by the plan's own required verification
steps (`--self-test`/`--check`), following the same shape as plan 21-08's own six Rule-1 fixes.
**Impact on plan:** Both fixes were necessary to land Task 1's `consumes` wiring and Task 2's
Facts-fence narrative at all; neither changes the plan's success criteria or scope.

## Assumption Drift (advisory)

- **Found during:** Task 1, the post-generation re-measurement
- **Planned assumption:** The plan's own action frames the post-generation re-measurement as
  confirming the baseline's prediction ("the structural elimination has happened; the number that
  matters... is what is left") — implicitly expecting a residual in the neighborhood of the
  baseline's 79 scanner-target figure, since D-06's citation-exemption vocabulary (plan 21-08) had
  already been proven against the same migrated narrative.
- **What turned out true:** The standing scanner's residual (156) is roughly double the baseline's
  79, because the standing scanner and D-06's containment check are TWO INDEPENDENT mechanisms with
  independently-scoped vocabularies — D-06 gained a citation-exemption vocabulary in plan 21-08
  specifically for the migrated narrative's false-positive shapes, but CONF-13's own scanner (built
  fresh in this plan, from the baseline's OLDER taxonomy) does not share that vocabulary. The two
  checkers police overlapping but non-identical claim shapes over the same text.
- **Why it matters:** A reader of plan 21-08's SUMMARY (which describes D-06 as "widened against
  real prose" and now fully passing) could reasonably expect CONF-13's own literal count to be
  similarly low. This is advisory, not a gate — the scanner is built exactly to the plan's own
  specification and was deliberately not widened with a second false-positive layer beyond what the
  baseline's taxonomy and detection-time exclusions already specify (see key-decisions) — but
  future work reconciling the two checkers' vocabularies (explicitly out of this plan's scope) would
  likely shrink this residual further before plan 21-10 even starts hand-fixing individual lines.

## Files Created/Modified

- `scripts/gen-gate-docs.py` (modified) — `LiteralHit`, `LiteralExemptionClass`,
  `LITERAL_EXEMPTION_CLASSES` (7 classes), `_scan_text_for_literal_hits()`,
  `_generated_marker_pairs_for()`/`_literal_hits_outside_generated()`, `LITERAL_SCAN_MD_GLOBS`,
  `_py_docstring_scan_scripts()`, `LITERAL_SCAN_SURFACES`, `LiteralScanRead`, `run_literal_scan()`,
  `literal_scan_coverage_floor_problems()`, `literal_scan_problems()`, `literal_scan_attributions()`,
  wired into `cmd_check()`; `describe()` extended with the live literal-scan reading;
  `NARRATIVE_ENTRIES` gained `CONF-SURFACE`; both `harvest()` call sites widened to the full
  `ENTRIES` list; ten new self-test controls (36 -> 46)
- `scripts/_gate_registry.py` (modified) — `CONF-SURFACE`'s `GateEntry` gained a `consumes` tuple
  matching `describe()`'s new fields
- `docs/gates/CONF-SURFACE.md` (modified) — Facts fence now carries real `--describe`-derived
  counts; a hand-written "Disclosed bounds" narrative section added (the four bounds, in the
  R7/R9/R10 voice)

## Decisions Made

See `key-decisions` in frontmatter — summarized: (1) `CONF-SURFACE` joined `NARRATIVE_ENTRIES` to
carry a hand-written narrative through regeneration; (2) the exemption taxonomy implements all
seven baseline-named classes, including three measuring zero live hits today, kept for completeness
rather than deleted as dead weight; (3) the baseline's own false-positive filter layer
(ordinal-label/adjacency-mistrack/enumerated-list-marker) was deliberately not ported — only its
exemption taxonomy and its two structural detection-time tightening passes were; (4) `harvest()`
was widened to the full `ENTRIES` list so the anticipatory `CONF-SURFACE` entry's own `--describe`
runs, while `_ANTICIPATORY_KEYS`'s other two exclusions (D-01 battery-id floor, live table row
count) are unchanged.

## Issues Encountered

None beyond the two deviations above, both resolved within this plan's own scope.

## Next Phase Readiness

- **This plan is COMPLETE.** All Task 1 work landed in commit `a438f51`. Task 2 required no
  additional code changes; its deliverables (the live reading, the stale-figure sweep, and the
  reintroduction proof) are recorded in this SUMMARY as instructed by the plan's `<output>` spec.
- `bash scripts/check-firewall-battery.sh` reports **GREEN (25/25)** against the committed state.
- **Handed to plan 21-10:** 156 non-exempt residual literal-scan hits (file:line list reproducible
  via `python3 scripts/gen-gate-docs.py --check`), plus the one stale-figure survivor
  (`docs/COMPONENT-DIAGRAM.md:66`'s `14-gate` hyphen-compound, invisible to the scanner by
  construction — a detection gap to close by hand, not a scanner defect).
- **Handed to plan 21-11:** the battery-total forward-looking note (registering `CONF-SURFACE` will
  move `FIREWALL: GREEN (25/25)` to `26/26`; every current mention of `25` is correct today and
  will need updating then).
- No blockers. Ready for plan 21-10.

## Known Stubs

None. The scanner is fully implemented and wired into `--check`; no placeholder logic remains. The
156 non-exempt residual is a MEASURED, HONEST reading (per the plan's explicit "do not weaken the
scanner to reach exit 0" instruction), not a stub.

---
*Phase: 21-generate-the-claim-surface*
*Completed: 2026-09-06*

## Self-Check: PASSED

- FOUND: commit `a438f51` (`git log --oneline --all`)
- FOUND: `bash scripts/check-firewall-battery.sh` reports FIREWALL: GREEN (25/25)
- FOUND: `python3 scripts/gen-gate-docs.py --self-test` exits 0 (46 controls)
- FOUND: `python3 scripts/gen-gate-docs.py --check` exits 1, printing `literal-scan: 156 non-exempt hit(s) found`
- FOUND: `python3 scripts/_gate_registry.py --self-test` exits 0 (16 controls)
- FOUND: `python3 scripts/check-links.py` exits 0 (274 links + 6 namespace refs, 128 files)
- FOUND: `docs/gates/CONF-SURFACE.md` carries the four disclosed bounds and a populated Facts fence
- FOUND: `git status --porcelain` empty in the real repo (verified before and after the scratch-copy
  reintroduction proof)
