---
phase: 19-false-negative-rate
plan: 05
subsystem: measurement-instrumentation
tags: [conformance-baseline, adversarial-corpus, false-negative-rate, report-conformance]
dependency-graph:
  requires: [19-01, 19-02, 19-03, 19-04]
  provides: [adversarial-corpus-fourth-surface, published-false-negative-rate]
  affects: [19-06, 19-07]
tech-stack:
  added: []
  patterns:
    - "discovery-with-count-floor idiom reused for a fourth surface (D-02)"
    - "compute_corpus_headline as a sibling of compute_headline, not a fourth per_surface entry"
    - "build_corpus_row as a thin wrapper over build_row -- one detect_defects call per item"
key-files:
  created: []
  modified:
    - scripts/report-conformance.py
    - docs/conformance-baseline.md
    - docs/data/conformance.json
decisions: []
metrics:
  duration: "~45 minutes"
  completed: 2026-09-05
---

# Phase 19 Plan 05: Publish the adversarial-corpus false-negative rate Summary

`scripts/report-conformance.py` gains a fourth discovered surface (`adversarial-corpus`, floor 12)
that joins `tests/adversarial-corpus-v9.0/catalog.md` metadata onto each item's existing
`detect_defects` reading, and `docs/conformance-baseline.md` now publishes the measured
false-negative rate (9 of 13) as a single figure next to Phase 17's readings.

## What was built

**Task 1 — discovery, catalog parsing, joined rows.**
- `ADVERSARIAL_CORPUS_GLOB`, `ADVERSARIAL_CORPUS_CATALOG`, `ADVERSARIAL_CORPUS_README` and
  `MIN_CORPUS_ITEMS = 12` added beside the three existing surface constants.
- `Artifact.surface`'s `Literal` widened with `"adversarial-corpus"`; `discover_artifacts` gained a
  fourth `sorted(...)` glob block excluding `catalog.md`/`README.md` by resolved path, with the same
  `COUNT FLOOR FAIL` idiom as the three existing surfaces. Corpus artifacts are emitted last, so
  discovery order stays `shared-examples`, `generated-twin`, `contract-surface`,
  `adversarial-corpus`.
- `parse_corpus_catalog(repo_root)` reads the `## Catalog` table by locating the header row naming
  all seven columns, then maps each data row **by header name** (never by position), returning
  `(entries, problems)`. A row with an empty `File` cell or a `Stratum` outside `{A, B1, B2}`
  becomes a named problem rather than being silently dropped.
- `build_corpus_row(artifact, catalog_entry)` is a thin wrapper: calls `build_row(artifact)`
  verbatim, then merges `stratum`/`source`/`disposition` (or the literal `"MISSING"` if no catalog
  entry exists) plus computed `fully_clean` (True iff `section_resolution == "OK"` and every field
  in `_CORPUS_FORM_FIELDS` and `_CORPUS_SUBSTANTIVE_FIELDS` reads `0`) and `form_defects` (summed
  form-field count, or the literal `"unreadable"` when unreadable).
- `build_rows` now parses the catalog once per call and routes `adversarial-corpus` artifacts
  through `build_corpus_row`, the other three surfaces through the unmodified `build_row`.
- `_make_minimum_tree` (the `--self-test` fixture builder) was extended to also populate the
  corpus's own 12-item minimum plus its two sidecars, and `_control_floor_passes_at_minimum`'s
  expected count now includes `MIN_CORPUS_ITEMS` — both needed so the three pre-existing floor
  controls kept passing against the widened four-floor `discover_artifacts`.

**Task 2 — headline, rendering, regeneration.**
- `compute_corpus_headline(corpus_rows)` — a sibling of `compute_headline`, not a fourth
  `per_surface` entry — returns `total`, `clean`, `unreadable`, `form_defects`, `by_stratum`
  (A/B1/B2, plus `MISSING` if present) and `clean_without_disposition`.
- `render_markdown` gained a `## adversarial-corpus` section (via the new
  `_render_adversarial_corpus_section` helper) after the three-surface loop and before
  `## Source-vs-twin agreement (D-04)`: the headline as a single figure, the three per-stratum
  rates, the backlog-999.4 gate-input sentence (stated in 999.4's own CONDITIONAL terms), the
  stratum vocabulary paragraph, the fixtures-vs-artifacts distinction paragraph (D-06: a
  measurement no phase may target), the no-generated-twin statement, and the narrower nine-column
  per-item table with a pointer to the full 22-column JSON. A fifth Disclosed-bounds point (D-07)
  was also added: the pre-commit gate fails on staleness, never on a high reading.
- `render_json` gained one new top-level key `adversarial_corpus: {headline, rows}` (never folded
  into the flat `rows` list or into `pair_agreement`) plus a fourth `surface_counts` entry;
  `pair_agreement`/`AGREEMENT_FIELDS` were left untouched.
- One `--self-test` control added: `corpus-clean-without-disposition`, asserting a synthetic
  two-row fixture reads `clean_without_disposition == 1` when one clean row's disposition is
  `"MISSING"`, and `== 0` once that same row's disposition is perturbed to a real string.
- Both artifacts regenerated and committed together with the code change, in the single commit
  the plan's SEQUENCING section requires.

## Sequencing deviation from the plan's task-commit boundary (not a plan deviation)

The plan's Task 1 acceptance criteria describe an intermediate state where only
`scripts/report-conformance.py` is dirty and the two docs artifacts are "NOT yet regenerated."
Verified empirically that committing at that checkpoint is not possible: `build_rows` already
discovers and measures the fourth surface after Task 1 alone, so the flat `rows` list `render_json`
serializes already differs from the committed `docs/data/conformance.json` — `--check` reports
drift and the pre-commit conformance-drift hook blocks the commit, even though `render_markdown`/
`render_json` had not yet been touched. This is exactly the failure mode the plan's own SEQUENCING
paragraph warns about ("The code change and the regenerated artifacts land in ONE commit ...
Splitting them blocks every subsequent commit"). Per that explicit instruction, both tasks' file
changes were implemented in full and then landed together in the single commit below, rather than
attempting (and having git reject) a Task-1-only commit. No task content was skipped; Task 1's
acceptance criteria were all verified against the working tree before Task 2's code was added.

## Verification performed (all commands actually run, outputs recorded)

- `python3 scripts/report-conformance.py --self-test` after Task 1's code only: `SELF-TEST PASS —
  17 controls run` (unchanged from pre-plan; Task 1 adds no control, matching its acceptance
  criteria).
- Corpus discovery + catalog parse one-liner: `corpus artifacts 13`, `catalog entries 13 parse
  problems []`; none of the 13 relpaths is `catalog.md` or `README.md`.
- `/usr/bin/grep -c 'detect_defects(' scripts/report-conformance.py` → `1`, unchanged from the
  pre-plan count — confirmed `build_corpus_row` never calls `detect_defects` a second time.
- Unreadable-is-never-clean in-memory check: an artifact that raises `SectionResolutionError`
  produces `section_resolution` starting `SectionResolutionError:`, `fully_clean == False`,
  `form_defects == "unreadable"`.
- Scratch-copy floor-fires behavior assertion (`rsync -a --exclude .git`, deleted two corpus items
  to leave 11): `python3 scripts/report-conformance.py --check` exited **1** with
  `report-conformance: COUNT FLOOR FAIL — expected >= 12 files matching
  tests/adversarial-corpus-v9.0/*.md (excluding catalog.md and README.md), found 11`. Real tree
  `git status --porcelain` was empty before and after; scratch copy discarded.
- After Task 2: `python3 scripts/report-conformance.py --self-test` → `SELF-TEST PASS — 18 controls
  run` (17 → 18, the one control Task 2 adds).
- `python3 scripts/report-conformance.py` then `--check` twice in a row: both exits **0**,
  `report-conformance: PASS — no drift` both times (idempotency confirmed, no pass1/pass2
  non-determinism).
- `/usr/bin/grep -c '^## adversarial-corpus' docs/conformance-baseline.md` → `1`.
- JSON assertion one-liner: top-level keys
  `['adversarial_corpus', 'artifact_count', 'generator', 'headline', 'measurement_date',
  'pair_agreement', 'rows', 'surface_counts']`; `adversarial_corpus.headline` =
  `{'total': 13, 'clean': 9, 'unreadable': 0, 'form_defects': 0, 'by_stratum': {'B2': {'clean': 7,
  'total': 7}, 'B1': {'clean': 1, 'total': 1}, 'A': {'clean': 1, 'total': 5}},
  'clean_without_disposition': 0}` — `form_defects == 0` and `clean_without_disposition == 0`
  both hold, as CONF-07/CONF-08 require.
- Published-rate-equals-JSON check: the rendered markdown reads **"9 of 13 corpus items score
  fully clean"**, matching `adversarial_corpus.headline.clean == 9` of
  `adversarial_corpus.headline.total == 13` exactly.
- Anti-vacuity check on a disposable scratch copy: emptied `T-01`'s `Disposition` cell in
  `catalog.md`, regenerated — `clean_without_disposition` rose from `0` to `1`, and the rendered
  `t01-ledger-arbitrary-chain.md` table row showed an empty disposition cell. Real tree
  `git status --porcelain` was empty before and after; scratch copy discarded.
- `bash scripts/check-firewall-battery.sh` initially reported `FIREWALL: BLOCKED (24/25)` — VAL-03's
  pytest-capable interpreter was missing in this worktree. Per CLAUDE.md's documented remedy for
  this exact condition, ran `uv sync` (created the gitignored `.venv`, installed `pytest==9.1.1`).
  Re-ran: `FIREWALL: GREEN (25/25)`.
- `git diff --stat scripts/check-quality-harness.py` and `git diff --stat scripts/check-conf-gate.py`
  both produced no output — neither frozen detector file was touched.
- `git diff --stat HEAD~1 HEAD -- shared/ first-principles/ .github/` produced no output.
- `git status --porcelain` after `git add`: exactly `docs/conformance-baseline.md`,
  `docs/data/conformance.json`, `scripts/report-conformance.py` — the three files the plan names.
- Post-commit deletion check: `git diff --diff-filter=D --name-only HEAD~1 HEAD` — no output, no
  files deleted.
- `git status --porcelain --untracked-files=all` after the commit — no output, nothing left
  untracked.

## Per-stratum reading (recorded verbatim)

- **Stratum A: 1 of 5 clean.** `T-03`, `T-04`, `T-05` score non-clean (positive controls proving
  `dependency_cycles`/`ungrounded_chains`/`selfaudit_disagreements` reach shipped corpus bytes).
  `T-06` (the genuine miss, per `19-03-SUMMARY.md`) and `T-13` (the disclosed `grounded()`
  short-circuit) are the two clean items — but `T-13` measured `dependency_cycles == 2` and
  `ungrounded_chains == 2` non-clean here, so only `T-06` reads clean at the fully_clean predicate.
- **Stratum B1: 1 of 1 clean** (`T-02`, the fabricated read-at-source item, reachable only by
  PROV-GUARD).
- **Stratum B2: 7 of 7 clean** (`T-01`, `T-07`, `T-08`, `T-09`, `T-11`, `T-12`, `T-14` — reachable
  by nothing this project ships).
- **Overall: 9 of 13 clean** — the published false-negative rate.

## Commit

Single commit `502829d` — `feat(19-05): add adversarial-corpus as report-conformance.py's fourth
surface` — contains exactly the three files the plan names:

```
docs/conformance-baseline.md  |  36 ++
docs/data/conformance.json    | 968 +++++++++++++++++++++++++++++++++++++++++-
scripts/report-conformance.py | 414 +++++++++++++++++-
3 files changed, 1407 insertions(+), 11 deletions(-)
```

## Deviations from Plan

### Auto-fixed Issues

None — no bug, missing-critical-functionality, or blocking-issue auto-fix was required beyond the
sequencing accommodation documented above (which is a task-commit-boundary adjustment, not a
content deviation from the plan's specified code).

### Assumption Drift (advisory)

None material. The plan's stated behaviors (constants, discover_artifacts extension, catalog
parser, thin build_corpus_row wrapper, compute_corpus_headline as a sibling function, the markdown
section's seven required elements, the JSON key shape, the single self-test control) were all
implemented as specified and verified against the interfaces block.

## Self-Check: PASSED

- FOUND: `scripts/report-conformance.py` (modified, present)
- FOUND: `docs/conformance-baseline.md` (modified, present, contains `## adversarial-corpus`)
- FOUND: `docs/data/conformance.json` (modified, present, contains `adversarial_corpus` key)
- FOUND: commit `502829d` in `git log --oneline -3`
