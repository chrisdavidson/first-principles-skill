# SUMM-BLOCK: Finds exactly one structured-summary block at the end of a report's appendix, validates it against `shared/spine/references/summary-schema.json` with a stdlib validator driven by that file, and cross-checks every id and value against the report's own prose.

<!-- GENERATED:FACTS -->
## Facts

- `control_ids` (52): `C01`, `C02`, `C03`, `C04`, `C05`, `C06`, `C07`, `C08`, `C09`, `C10`, `C11`, `C12`, `C13`, `C14`, `C15`, `C15b`, `C15c`, `C16`, `C17`, `C18`, `C19`, `C20`, `C21`, `C22`, `C23`, `C24`, `C25`, `C26-precheck-clean`, `C27-precheck-field-mutations`, `C28-precheck-decoys`, `C29-precheck-missing`, `C30-precheck-head-shapes`, `C31-section6-same-line`, `P1-personal-general`, `P2-software-systems`, `P3-science-engineering`, `P4-tb-01`, `P5-precheck-real-fixtures`, `M1-missing-block`, `M2-two-blocks`, `M3-malformed-json`, `M4-chain-confidence`, `M5-reentry-fired-personal-general`, `M6-reentry-not-fired-software-systems`, `M7-single-pass-before-fix`, `M8-conclusion-cut`, `M9-two-hand-wavy-cleared`, `M10-precheck-real-fixture-mutation`, `X1-extraction-floor`, `X2-cross-check-ablation`, `X3-precheck-comparator-stub`, `X4-exemplar-precheck-floor`
- `control_count`: `52`
- `registered_surfaces` (4): `shared/spine/references/summary-schema.json`, `tests/summary-block-v9.16`, `shared/examples`, `first-principles/references/examples`
- `checked_files` (4): `tests/summary-block-v9.16/personal-general.md`, `tests/summary-block-v9.16/software-systems.md`, `tests/summary-block-v9.16/science-engineering.md`, `tests/summary-block-v9.16/tb-01.md`
- `locked_constants` (3 entries): `BLOCK_HEADING`='## Structured summary (process output)', `DEFAULT_SCHEMA`='shared/spine/references/summary-schema.json', `SCHEMA_VERSION`=1
- `derived_counts` (2 entries): `cross_checks`=17, `finding_codes`=32
- `disclosed_bounds_anchors` (14): `not-applied-phase-only-where-stated`, `precheck-band-raised-to-ceiling-undetectable`, `precheck-cited-band-reader-not-fence-aware`, `precheck-missing-fails-in-exemplar-mode-only`, `precheck-overlaps-qual01-precheck-defects`, `precheck-section6-head-completeness-not-checked`, `precheck-x3-passes-by-construction-under-a-comparator-stub`, `precheck-x4-chain-count-shares-the-site-chain-id-reader`, `recommendation-bold-markers-ignored`, `reentry-read-from-gate-span-and-disclosure-only`, `rests_on-order-not-compared`, `run-mode-only-where-stated`, `second-order-and-input-reopen-edges-need-a-disclosed-paragraph`, `techniques-applied-vocabulary-only`
<!-- END GENERATED:FACTS -->

<!-- GENERATED:HOW-TO-RUN -->
## How to run

```sh
python3 scripts/check-summary-block.py --self-test && python3 scripts/check-summary-block.py --exemplar shared/examples/*.md && python3 scripts/check-summary-block.py --exemplar first-principles/references/examples/*.md
```

CI job: `check-summary-block`
<!-- END GENERATED:HOW-TO-RUN -->
