# PROV-ROLLUP: The provenance roll-up's enumeration must agree with the section 3 it summarises.

<!-- GENERATED:FACTS -->
## Facts

- `registered_surfaces` (2): `shared/spine/SKILL-body.md`, `shared/spine/references/output-template.md`
- `scan_globs` (1): `shared/references/*.md`
- `locked_constants` (3 entries): `shared/references/*.md`=0, `shared/spine/SKILL-body.md`=0, `shared/spine/references/output-template.md`=1
- `derived_counts` (10 entries): `fixtures`=11, `injections`=9, `line_format_paired_captures`=77, `line_format_present`=30, `line_format_unreadable`=4, `live_arm_rollup_subjects`=14, `template_only_surfaces`=3, `template_read_captures`=18, `template_read_dispatched`=17, `template_read_true`=10
- `disclosed_bounds_anchors` (12): `chain-head-window-is-head-line-only`, `exemplar-floor-gates-shipped-files-not-live-readings`, `ids-compared-question-mark-insensitively`, `line-format-pinned-on-frozen-captures-only`, `pre-check-line-is-not-a-rollup`, `presence-is-report-only`, `read-at-source-coverage-is-report-only`, `read-at-source-grammar-unprescribed`, `rollup-located-in-section-3-only`, `section-3-read-outside-fenced-code`, `template-read-pinned-on-frozen-captures-only`, `unreadable-document-is-named-not-failed`
- `control_ids` (20): `absent`, `agreeing`, `always-pass`, `backticked-and-suffixed`, `census-always-true`, `census-no-reads`, `count-disagrees`, `empty-ground-truths`, `enumerated-not-marked`, `exemplar-rollup-dropped`, `high-chain-covered`, `high-chain-uncovered`, `integer-not-a-list`, `kept-row-dropped`, `locator-everywhere`, `locator-never`, `marked-not-enumerated`, `pre-check-is-not-a-rollup`, `presence-is-agreement`, `range-form`
- `control_count`: `20`
<!-- END GENERATED:FACTS -->

<!-- GENERATED:HOW-TO-RUN -->
## How to run

```sh
python3 scripts/check-provenance-rollup.py --self-test && python3 scripts/check-provenance-rollup.py --dir shared/examples
```

CI job: `check-provenance-rollup`
<!-- END GENERATED:HOW-TO-RUN -->
