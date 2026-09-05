---
phase: 19-false-negative-rate
plan: 08
subsystem: testing
tags: [adversarial-corpus, conformance, false-negative-rate, report-conformance, gap-closure]

# Dependency graph
requires:
  - phase: 19-false-negative-rate (plans 01-07, waves 1-5)
    provides: "the 13-item frozen corpus, catalog.md, README.md, report-conformance.py's
      fourth adversarial-corpus surface, and 19-VERIFICATION.md's Truth-2/Truth-3 gap
      finding this plan closes"
provides:
  - "tests/adversarial-corpus-v9.0/catalog.md: a closed-vocabulary Target column joined
    to detect_defects' own chain/criterion audit fields, and a self-consistent
    'Reading the strata' section"
  - "scripts/report-conformance.py: _parse_corpus_target, _corpus_target_hits, the
    renamed no_column_fired diagnostic, the target_missed-keyed headline, and derived
    (never hardcoded) render-time item enumerations"
  - "docs/conformance-baseline.md, docs/data/conformance.json: the false-negative figure
    now counts catalogued targets missed (10 of 13), with t13's divergence from
    no_column_fired (9 of 13) visible in both the table and the JSON"
affects: [19-09]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Chain-scoped join, never column-scoped: _corpus_target_hits compares specific
       chain ids / criterion numbers named in the catalog's Target cell against
       detect_defects' underscore-prefixed audit fields, rather than asking only
       whether a column fired at all -- this is what lets t13's own catalogued chain
       (C1) read missed even though an unrelated cycle on chains C2/C3 fires the same
       column."
    - "Private out-param channel (build_row's _audit_record_out) to reach a raw
       detect_defects record's audit-only fields from build_corpus_row without a second
       detect_defects call and without widening build_row's own return schema for the
       other three surfaces."
    - "Fail-closed target-cell grammar: any parse problem anywhere in a Target cell
       empties the whole cell's parsed pair list rather than partially trusting the
       well-formed terms -- a malformed cell is treated as 'nothing catalogued', never
       as 'some of it catalogued'."

key-files:
  created: []
  modified:
    - tests/adversarial-corpus-v9.0/catalog.md
    - tests/adversarial-corpus-v9.0/README.md
    - scripts/report-conformance.py
    - docs/conformance-baseline.md
    - docs/data/conformance.json

key-decisions:
  - "Followed the plan's D-19-08-A verbatim: renamed fully_clean to no_column_fired
     (demoted to a per-row diagnostic) AND wired the catalog's Target column into a new
     target_missed field that the published headline now keys on -- Option B with
     Option A's rename adopted as a mandatory sub-part, not a standalone alternative."
  - "Widened _corpus_disposition_problems' CONF-08 floor from checking no_column_fired
     alone to checking the UNION (target_missed is True or no_column_fired is True) --
     required by the second closes_gaps bullet's own text ('so the headline and the
     disposition floor key on catalogued falsehood missed'), even though this specific
     widening was not spelled out as its own numbered step in Task 2's <action>."
  - "Removed every literal occurrence of the string fully_clean from
     scripts/report-conformance.py, including inside docstrings/comments explaining the
     rename -- the acceptance criterion (grep -c fully_clean prints 0) is unconditional,
     so explanatory prose was reworded to avoid the identifier rather than quote it."

requirements-completed: [CONF-07, CONF-08]

# Metrics
duration: ~2h
completed: 2026-09-05
---

# Phase 19 Plan 08: False-Negative Figure Keyed on Catalogued Target, Not Column-Fired Summary

**The published false-negative rate now counts items whose catalogued falsehood
`detect_defects` failed to catch (10 of 13) rather than items on which no column merely
happened to fire (9 of 13, demoted to a `no_column_fired` diagnostic) — closing the
19-VERIFICATION.md gap where `t13-grounded-alongside-cyclic-ref`'s own catalogued target
(chain C1) was silently exempted from the count because an unrelated cycle on chains
C2/C3 fired the same column.**

## Performance

- **Duration:** ~2h
- **Completed:** 2026-09-05
- **Tasks:** 3 completed
- **Files modified:** 5 (`tests/adversarial-corpus-v9.0/catalog.md`,
  `tests/adversarial-corpus-v9.0/README.md`, `scripts/report-conformance.py`,
  `docs/conformance-baseline.md`, `docs/data/conformance.json`)

## Accomplishments

- Added a closed-vocabulary `Target` column to `catalog.md`'s catalog table (eighth
  column, after `Disposition`), a vocabulary paragraph explaining its scope and
  grammar, and rewrote `## Reading the strata` so it states `t13`'s status once,
  consistently, instead of contradicting itself.
- Added `_parse_corpus_target` (fail-closed grammar parser) and `_corpus_target_hits`
  (the chain-scoped join against `detect_defects`' `_dependency_cycles` /
  `_ungrounded_chains` / `_selfaudit_disagreements` audit fields) to
  `scripts/report-conformance.py`.
- Renamed `fully_clean` → `no_column_fired` everywhere (19 occurrences), demoted from
  headline to per-row diagnostic; added `target`, `target_hits`, `target_missed` to
  every corpus row.
- Re-keyed `compute_corpus_headline` on `target_missed` (renamed `clean` →
  `target_missed`/`no_column_fired`; renamed `clean_without_disposition` →
  `missed_without_disposition`, widened to the union of both predicates).
- Widened `_corpus_disposition_problems`' CONF-08 zero-silent-passes floor to the union
  `target_missed is True or no_column_fired is True`, so an item like `t13` can no
  longer escape the floor merely because an unrelated column fired on it.
- Replaced the hardcoded `t03, t04, t05` positive-control enumeration in
  `_render_adversarial_corpus_section` with three sets derived from `corpus_rows` at
  render time (caught / column-fired-but-target-missed / nothing-fired), and added a
  new self-test control (`corpus-render-no-hardcoded-stems`) that fails if any stem
  literal is reintroduced.
- Re-measured and corrected the false "0 structural ledger rows across all 13 items,
  measured" docstring claim in `_corpus_citation_mutation_site` (the true figure is 1).
- Grew `--self-test` from 43 to 51 controls (8 new/renamed: `corpus-render-no-hardcoded-stems`,
  `corpus-target-parse-vocabulary`, `corpus-target-hits-chain-scoped`,
  `corpus-target-hits-selfaudit-criterion`, `corpus-target-none-is-missed`,
  `corpus-target-missing-entry-is-missed`, `corpus-headline-keys-on-target-missed`,
  `corpus-disposition-target-missed-only-checked`).

## Task Commits

1. **Task 1: Add the closed-vocabulary Target column to catalog.md, fix its
   self-contradiction, and move the README sha256 rows in the same commit** —
   `d2fd0be` (feat)
2. **Task 2: Parse the Target column, join it to detect_defects' audit fields, rename
   fully_clean to no_column_fired, and key the headline on target_missed** — `11a0f95`
   (feat)
3. **Task 3: Derive every enumerated item set in the rendered corpus section, and
   replace the false "measured" ledger-row comment** — `d513553` (fix)

**Plan metadata:** this SUMMARY.md (docs commit follows).

## Step-1 audit-field measurement (re-measured before writing any Target value)

Loaded `scripts/check-quality-harness.py` via `importlib` and called the unmodified
`detect_defects(text, stem)` on each of the thirteen corpus items, verbatim:

```
t01-ledger-arbitrary-chain dependency_cycles= [] ungrounded_chains= [] selfaudit_disagreements= []
t02-fabricated-read-at-source dependency_cycles= [] ungrounded_chains= [] selfaudit_disagreements= []
t03-composition-cycle dependency_cycles= ['c1', 'c2'] ungrounded_chains= [] selfaudit_disagreements= []
t04-chain-only-head-ungrounded dependency_cycles= [] ungrounded_chains= ['c1', 'c2'] selfaudit_disagreements= []
t05-selfaudit-overclaim-under-cycle dependency_cycles= ['c1', 'c2'] ungrounded_chains= [] selfaudit_disagreements= [4]
t06-hidden-cycle-past-head dependency_cycles= [] ungrounded_chains= [] selfaudit_disagreements= []
t07-non-sequitur-between-hops dependency_cycles= [] ungrounded_chains= [] selfaudit_disagreements= []
t08-verdict-contradicts-its-type dependency_cycles= [] ungrounded_chains= [] selfaudit_disagreements= []
t09-arithmetic-does-not-follow dependency_cycles= [] ungrounded_chains= [] selfaudit_disagreements= []
t11-fabricated-ground-truth dependency_cycles= [] ungrounded_chains= [] selfaudit_disagreements= []
t12-inline-citation-wrong-chain dependency_cycles= [] ungrounded_chains= [] selfaudit_disagreements= []
t13-grounded-alongside-cyclic-ref dependency_cycles= ['c2', 'c3'] ungrounded_chains= ['c2', 'c3'] selfaudit_disagreements= []
t14-order-of-magnitude-conversion dependency_cycles= [] ungrounded_chains= [] selfaudit_disagreements= []
```

Every measured value matched the plan's prescribed per-item `Target` value AND the
existing `Rule that ought to catch it` prose for that row — no disagreement was found,
so no item required stopping to report a conflict. `T-13`'s measured
`ungrounded_chains=['c2','c3']` contains neither `c1` (its own catalogued target),
confirming the divergence live before writing `Target: ungrounded_chains:c1`.

## fully_clean rename blast-radius (Step 1, Task 2)

```
$ /usr/bin/grep -c fully_clean scripts/report-conformance.py
19
$ /usr/bin/grep -rln fully_clean --include=*.py --include=*.md --include=*.sh . \
    | grep -v '^\./\.planning' | grep -v '^\./docs/data'
./docs/conformance-baseline.md
./scripts/report-conformance.py
```

Confirmed: exactly the two surfaces D-19-08-A's cost assessment named, no other tracked
file. After the rename, `/usr/bin/grep -c fully_clean scripts/report-conformance.py`
prints `0` — including every docstring/comment mention (the acceptance criterion is
unconditional on the literal string, so explanatory prose describing the old identifier
was reworded rather than quoting it).

## Before/after `--self-test` control counts

- Before this plan (end of 19-06/19-07): **43 controls**.
- After Task 2 (`11a0f95`): **50 controls** (+7: `corpus-target-parse-vocabulary`,
  `corpus-target-hits-chain-scoped`, `corpus-target-hits-selfaudit-criterion`,
  `corpus-target-none-is-missed`, `corpus-target-missing-entry-is-missed`,
  `corpus-headline-keys-on-target-missed`,
  `corpus-disposition-target-missed-only-checked`; `corpus-clean-without-disposition`
  renamed to `corpus-missed-without-disposition` in place, net control count for that
  rename unchanged).
- After Task 3 (`d513553`): **51 controls** (+1: `corpus-render-no-hardcoded-stems`).

## New rendered headline sentence (verbatim, from the regenerated `docs/conformance-baseline.md`)

```
**False-negative rate:** 10 of 13 corpus items' catalogued falsehood the unmodified,
CONTRACT-06-frozen `detect_defects` did not catch -- despite every item being a stated,
catalogued falsehood. Each of those 10 is a false negative: a substantively wrong
analysis this instrument cannot distinguish from a sound one. Diagnostic: 9 of 13 items
had no substantive `detect_defects` column fire on them at all; the difference between
the two figures is exactly the items on which an unrelated column fired for a reason
having nothing to do with the item's own catalogued falsehood.
```

Per-stratum breakdown, verbatim:

```
- Stratum A: 2 of 5 catalogued target missed (1 of 5 no column fired)
- Stratum B1: 1 of 1 catalogued target missed (1 of 1 no column fired)
- Stratum B2: 7 of 7 catalogued target missed (7 of 7 no column fired)
```

Backlog 999.4 gate input (Stratum B2) reads **7 of 7 catalogued target missed** —
unchanged from the pre-fix `no_column_fired` reading of 7 of 7, since every stratum-B2
item's catalogued `Target` is `none` (no `detect_defects` column is scoped to reach
B1/B2 wrongness by construction), so this stratum's figure could not move under the
rename. Stratum A is where the movement is: 2 of 5 missed (up from 1 of 5 clean under
the old predicate) — the extra one is `t13`.

The `t01-ledger-arbitrary-chain.md` row (`no_column_fired: false`, `target_missed:
true`) confirms the t13 divergence live in the regenerated
`docs/data/conformance.json`:

```
$ python3 -c "import json;d=json.load(open('docs/data/conformance.json'));r=[x for x in d['adversarial_corpus']['rows'] if x['analysis_id'].startswith('t13')][0];assert r['no_column_fired'] is False and r['target_missed'] is True, r;print('T13 DIVERGENCE CONFIRMED')"
T13 DIVERGENCE CONFIRMED
```

## Re-measured ledger-row figure (Task 3, Step 5)

The prior docstring on `_corpus_citation_mutation_site` claimed "0 structural ledger
rows across all 13 items, measured" — this was false. Re-measurement command and
verbatim output:

```
$ python3 -c "
import importlib.util, sys
from pathlib import Path
REPO_ROOT = Path('.').resolve()
_HARNESS_PATH = REPO_ROOT / 'scripts' / 'check-quality-harness.py'
_spec = importlib.util.spec_from_file_location('_quality_harness', _HARNESS_PATH)
_mod = importlib.util.module_from_spec(_spec)
sys.modules['_quality_harness'] = _mod
_spec.loader.exec_module(_mod)
detect_defects = _mod.detect_defects

total = 0
for p in sorted(REPO_ROOT.glob('tests/adversarial-corpus-v9.0/t*.md')):
    stem = p.stem
    text = p.read_text(encoding='utf-8')
    r = detect_defects(text, stem)
    n = len(r['_closure_ledger_fragments'])
    if n:
        print(stem, n, r['_closure_ledger_fragments'])
    total += n
print('TOTAL', total)
"
t01-ledger-arbitrary-chain 1 ['Use the effective compensation figure (approximately $54,000) rather than the nominal figure in any financial planning']
TOTAL 1
```

Exactly **one** structural ledger row exists (`t01-ledger-arbitrary-chain`'s own 999.2
seed-case row). The docstring now states this figure and explains why the ledger
fallback branch in `_corpus_citation_mutation_site` is *still* never exercised against
real corpus bytes despite that row existing: `t01`'s section 6 also carries inline
`(chain Cn)` citations earlier in the body, and
`_INLINE_CHAIN_CITE_RE.search(section6)` matches the first inline occurrence anywhere
in the section regardless of where the structural ledger row sits, so the function
always returns from the inline branch before ever reaching the fallback — verified by
reading `t01`'s section 6 text directly (its first line already contains `(chain C2)`).

## Neutralizations performed (each applied alone, reverted, confirmed reverted)

**N1 — chain-scoped join weakened to bare column-fired truthiness** (Task 2 acceptance
criterion): changed `_corpus_target_hits`' membership test
`if any(s.lower() in audit_ids for s in selectors):` to `if bool(audit_ids):` in a
disposable `rsync --exclude .git` scratch copy under the scratchpad directory.

```
$ python3 scripts/report-conformance.py --self-test
report-conformance: SELF-TEST FAIL [corpus-target-hits-chain-scoped] — ['ungrounded_chains:c1']
```

Fires by name, naming the exact control the plan requires. Reverted; `--self-test`
back to PASS. `git status --porcelain` in the real worktree confirmed empty before and
after (the scratch copy never touched it).

**N2 — `compute_corpus_headline`'s `target_missed` aliased to `no_column_fired`** (Task
2 acceptance criterion): in the same scratch copy, replaced the independent
`target_missed = sum(...)` computation with `target_missed = no_column_fired`.

```
$ python3 scripts/report-conformance.py --self-test
report-conformance: SELF-TEST FAIL [corpus-headline-keys-on-target-missed] — {'total': 3, 'target_missed': 1, 'no_column_fired': 1, ...}
```

Fires by name, naming the anti-vacuity control for the whole rename. Reverted;
`--self-test` back to PASS. Real worktree confirmed clean before and after.

**N3 — reinstated a literal `(\`t03\`, \`t04\`, \`t05\`)` parenthetical in
`_render_adversarial_corpus_section`** (Task 3 acceptance criterion), in a second
disposable scratch copy:

```
$ python3 scripts/report-conformance.py --self-test
report-conformance: SELF-TEST FAIL [corpus-render-no-hardcoded-stems] — hardcoded stem literal 't03' found in rendered output
```

Fires by name. Reverted (scratch copy deleted); real worktree confirmed clean
(`git status --porcelain` showed only the intended Task 1/2/3 modifications, never the
neutralization's edits).

## Verification performed (all commands actually run, outputs recorded)

- `python3 scripts/report-conformance.py --self-test` (final state): `SELF-TEST PASS —
  51 controls run`.
- `python3 scripts/report-conformance.py --check` (final state): `PASS — no drift`.
- `python3 scripts/check-conf-gate.py --self-test`: `SELF-TEST PASS — 42 controls run`
  (unmodified by this plan).
- `python3 scripts/check-quality-harness.py --self-test`: all three CONTRACT-06 sub-checks
  (`chain_detector_pin`, `conclusion_claims_pin`, `slice_sections_pin`) PASSED; file
  byte-unchanged (`git diff --quiet -- scripts/check-quality-harness.py` exits 0 after
  every task, and `git diff --quiet HEAD~3 -- scripts/check-quality-harness.py
  scripts/check-conf-gate.py .github/workflows/validation.yml shared first-principles`
  exits 0 at the end of the plan).
- `bash scripts/check-firewall-battery.sh`: `FIREWALL: GREEN (25/25)` after every task's
  commit — battery TOTAL unchanged.
- `sha256sum tests/adversarial-corpus-v9.0/*.md` compared programmatically against
  `README.md`'s 14-row table: all 13 items + `catalog.md` match exactly; only
  `README.md` itself is (correctly, by its own documented convention) absent from the
  table.
- `detect_defects` call count for the corpus surface: instrumented `build_rows()` with
  a counting wrapper filtered to the 13 corpus stems — exactly **13** calls (one per
  item), confirmed no double-calling was introduced by the new `_audit_record_out`
  channel.
- `git status --porcelain`: empty after every task's commit.
- Post-commit deletion check (`git diff --diff-filter=D --name-only HEAD~1 HEAD`) on all
  three commits: no output, no files deleted.

## Assumption Drift (advisory)

**1. Disposition floor scope widened beyond Task 2's numbered steps, per the
closes_gaps text.** Task 2's `<action>` numbered steps (1-9) do not explicitly instruct
widening `_corpus_disposition_problems`' scope from `no_column_fired` to the union with
`target_missed`. However, the plan frontmatter's `closes_gaps` second bullet states the
gap closure as "wire that column in so the headline **and the disposition floor** key
on 'catalogued falsehood missed'" — the disposition floor is named explicitly there,
and 19-VERIFICATION.md's third `missing` item independently states the same
requirement ("Extend ... CONF-08's disposition floor so an item whose catalogued target
was missed cannot escape the zero-silent-passes check"). Treated this as in-scope for
Task 2 rather than out-of-scope, since the closes_gaps text is more authoritative than
the step-by-step's specific enumeration and the change is small, safe (widening only,
verified never narrower than the pre-existing scope), and directly closes a named gap.
Recorded here per the assumption-drift advisory rather than silently expanding scope
unremarked.

## Deviations from Plan

### Auto-fixed Issues

None — no bug, missing-critical-functionality, or blocking-issue auto-fix was required
beyond the scope-widening decision recorded above as assumption drift (which is a
scope interpretation, not a defect fix).

## Issues Encountered

None beyond the mechanical work of tracing which self-test controls held an inert
`fully_clean=...` override (unused by the function under test, safe to delete) versus a
load-bearing one (used by `_corpus_disposition_problems`, requiring semantic
translation to the new union predicate) — resolved by reading each control's target
function body before editing.

## User Setup Required

None — no external service configuration required. This worktree needed `uv sync`
(gitignored `.venv`) to satisfy the VAL-03 pytest prerequisite for the firewall
battery, the same already-documented remedy every prior plan in this phase applied
independently in its own worktree.

## Next Phase Readiness

- `scripts/report-conformance.py`'s adversarial-corpus surface now publishes a
  false-negative figure that means what CONF-08 requires: the catalogued falsehood was
  missed, not merely "some column happened not to fire".
- `t13-grounded-alongside-cyclic-ref` is now correctly counted as a false negative in
  the published `10 of 13` headline, and is no longer exempt from CONF-08's
  zero-silent-passes disposition floor.
- `catalog.md`, `docs/conformance-baseline.md` and `docs/data/conformance.json` agree
  with each other about which items are caught and which are missed — no remaining
  self-contradiction.
- Plan 19-09 (per the plan frontmatter's `depends_on`/wave note) can proceed against a
  corpus whose published rate is falsifiable rather than merely reported, closing both
  19-VERIFICATION.md gap-closure items named in this plan's `closes_gaps`.

---
*Phase: 19-false-negative-rate*
*Completed: 2026-09-05*

## Self-Check

- FOUND: `tests/adversarial-corpus-v9.0/catalog.md` (modified, present)
- FOUND: `tests/adversarial-corpus-v9.0/README.md` (modified, present)
- FOUND: `scripts/report-conformance.py` (modified, present)
- FOUND: `docs/conformance-baseline.md` (modified, present)
- FOUND: `docs/data/conformance.json` (modified, present)
- FOUND: commit `d2fd0be` (Task 1)
- FOUND: commit `11a0f95` (Task 2)
- FOUND: commit `d513553` (Task 3)

## Self-Check: PASSED
