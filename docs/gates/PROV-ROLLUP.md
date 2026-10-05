# PROV-ROLLUP: The provenance roll-up's enumeration must agree with the section 3 it summarises.

<!-- GENERATED:FACTS -->
## Facts

- `registered_surfaces` (2): `shared/spine/SKILL-body.md`, `shared/spine/references/output-template.md`
- `scan_globs` (1): `shared/references/*.md`
- `locked_constants` (3 entries): `shared/references/*.md`=0, `shared/spine/SKILL-body.md`=0, `shared/spine/references/output-template.md`=1
- `derived_counts` (7 entries): `fixtures`=11, `injections`=5, `live_arm_rollup_subjects`=11, `template_only_surfaces`=3, `template_read_captures`=18, `template_read_dispatched`=17, `template_read_true`=10
- `disclosed_bounds_anchors` (10): `chain-head-window-is-head-line-only`, `ids-compared-question-mark-insensitively`, `pre-check-line-is-not-a-rollup`, `presence-is-report-only`, `read-at-source-coverage-is-report-only`, `read-at-source-grammar-unprescribed`, `rollup-located-in-section-3-only`, `section-3-read-outside-fenced-code`, `template-read-pinned-on-frozen-captures-only`, `unreadable-document-is-named-not-failed`
- `control_ids` (16): `absent`, `agreeing`, `always-pass`, `backticked-and-suffixed`, `census-always-true`, `census-no-reads`, `count-disagrees`, `empty-ground-truths`, `enumerated-not-marked`, `high-chain-covered`, `high-chain-uncovered`, `integer-not-a-list`, `marked-not-enumerated`, `pre-check-is-not-a-rollup`, `presence-is-agreement`, `range-form`
- `control_count`: `16`
<!-- END GENERATED:FACTS -->

<!-- GENERATED:HOW-TO-RUN -->
## How to run

```sh
python3 scripts/check-provenance-rollup.py --self-test && python3 scripts/check-provenance-rollup.py --dir shared/examples
```

CI job: `check-provenance-rollup`
<!-- END GENERATED:HOW-TO-RUN -->
