# FIG-GATE: Renders both figures of the typst library in `shared/spine/references/report-figures.md` (the shipped source) against the real-analysis fixture, a two-digit-id worst-case fixture and every worked example's structured-summary block, and asserts through `typst eval 'query(...)'` that drawn edges equal the total of every chain `rests_on` entry, conclusion edges equal `conclusion.rests_on`, the matrix total equals the assumption count, no label overflows its box and every SVG fits the text column.

<!-- GENERATED:FACTS -->
## Facts

- `control_ids` (12): `P01`, `M01`, `M02`, `M03`, `F01`, `F02`, `B01`, `U01`, `U02`, `U03`, `U04`, `U05`
- `control_count`: `12`
- `registered_surfaces` (2): `shared/spine/references/report-figures.md`, `first-principles/references/report-figures.md`
- `checked_files` (2): `tests/report-figures-v9.17/analysis-20261001T204943Z.json`, `tests/report-figures-v9.17/worst-case-labels.json`
- `locked_constants` (3 entries): `FONTS`, `MAX_WIDTH_PT`, `mutation_anchors`
- `derived_counts` (3 entries): `example_fixtures`=14, `finding_codes`=13, `mutations`=3
- `disclosed_bounds_anchors` (6): `battery-blocked-decided-by-command-v-not-exit-code`, `counts-read-from-library-metadata-not-svg-geometry`, `label-fit-proven-to-two-digit-ids`, `requires-noto-sans-or-liberation-sans`, `typst-absent-is-blocked-not-pass`, `visual-legibility-is-inspection-not-gate`
<!-- END GENERATED:FACTS -->

<!-- GENERATED:HOW-TO-RUN -->
## How to run

```sh
python3 scripts/check-report-figures.py --self-test
```

CI job: `check-report-figures`
<!-- END GENERATED:HOW-TO-RUN -->
