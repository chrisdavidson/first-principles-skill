# FIG-GATE: Renders both figures of the typst library in `shared/spine/references/report-figures.md` (the shipped source) against the real-analysis fixture, a two-digit-id worst-case fixture and every worked example's structured-summary block, and asserts through `typst eval 'query(...)'` that drawn edges equal the total of every chain `rests_on` entry, conclusion edges equal `conclusion.rests_on`, the matrix total equals the assumption count, no label overflows its box and every SVG fits the text column.

<!-- GENERATED:FACTS -->
## Facts

- `control_ids` (16): `P01`, `M01`, `M02`, `M03`, `M04`, `F01`, `F02`, `B01`, `U01`, `U02`, `U03`, `U04`, `U05`, `L01`, `L02`, `L03`
- `control_count`: `16`
- `registered_surfaces` (4): `shared/spine/references/report-figures.md`, `first-principles/references/report-figures.md`, `shared/spine/references/report-layout.md`, `first-principles/references/report-layout.md`
- `checked_files` (5): `tests/report-figures-v9.17/analysis-20261001T204943Z.json`, `tests/report-figures-v9.17/worst-case-labels.json`, `tests/report-layout-v9.20/report-layout-45f6244a.md`, `shared/examples/product-business-2.md`, `shared/spine/references/how-to-read.md`
- `locked_constants` (3 entries): `FONTS`, `MAX_WIDTH_PT`, `mutation_anchors`
- `derived_counts` (3 entries): `example_fixtures`=14, `finding_codes`=14, `mutations`=4
- `disclosed_bounds_anchors` (8): `battery-blocked-decided-by-command-v-not-exit-code`, `counts-read-from-library-metadata-not-svg-geometry`, `label-fit-proven-to-two-digit-ids`, `page-template-proven-to-compile-not-to-look-right`, `pandoc-absent-is-blocked-not-pass`, `requires-noto-sans-or-liberation-sans`, `typst-absent-is-blocked-not-pass`, `visual-legibility-is-inspection-not-gate`
<!-- END GENERATED:FACTS -->

<!-- GENERATED:HOW-TO-RUN -->
## How to run

```sh
python3 scripts/check-report-figures.py --self-test
```

CI job: `check-report-figures`
<!-- END GENERATED:HOW-TO-RUN -->
