# PERSONA-GATE: Checks a reader-persona view against the analysis it was derived from and the contract in `shared/spine/references/persona-views.md` — the provenance header, the band against section 6, the role's word band, that every sentence and bullet carries a citation, that every cited chain, ground-truth (with matching `?` marking), assumption and dead-end id resolves in the source, and that every number appears in the source.

<!-- GENERATED:FACTS -->
## Facts

- `control_ids` (24): `P01`, `P02`, `P03`, `M-ID`, `M-AGREE`, `M-NUMBER`, `M-UNCITED`, `M-PSEUDO`, `M-BAND`, `M-HEADER`, `M-OVER`, `M-UNDER`, `M-SHAPE`, `M-DEADEND`, `G-NAME`, `G-WORDS`, `U01`, `U02`, `U03`, `U04`, `EX-REACH`, `EX-REACH-ID`, `EX-REACH-EMPTY`, `EX-REACH-ROSTER`
- `control_count`: `24`
- `registered_surfaces` (3): `shared/spine/references/how-to-read.md`, `shared/spine/references/output-template.md`, `shared/spine/references/persona-views.md`
- `checked_files` (12): `shared/examples/estimate-fermi.md`, `shared/examples/personal-general.md`, `shared/examples/product-business-2.md`, `shared/persona-examples/estimate-fermi-decision-owner.md`, `shared/persona-examples/estimate-fermi-skeptic.md`, `shared/persona-examples/product-business-2-decision-owner.md`, `shared/persona-examples/product-business-2-skeptic.md`, `tests/persona-views-v9.18/personal-general-risk.md`, `tests/persona-views-v9.18/product-business-2-decision-owner.md`, `tests/persona-views-v9.18/product-business-2-operator.md`, `tests/persona-views-v9.18/product-business-2-risk.md`, `tests/persona-views-v9.18/product-business-2-skeptic.md`
- `locked_constants` (3 entries): `guide_max_words`, `provenance_template`, `roster`
- `derived_counts` (4 entries): `finding_codes`=11, `fixtures`=5, `persona_examples`=4, `personas`=4
- `disclosed_bounds_anchors` (5): `absent-input-sentences-not-checked-for-truth`, `citation-presence-not-semantic-support`, `fixtures-are-worked-examples-not-live-analyses`, `guide-names-checked-against-output-template-only`, `numbers-matched-by-value-not-by-context`
<!-- END GENERATED:FACTS -->

<!-- GENERATED:HOW-TO-RUN -->
## How to run

```sh
python3 scripts/check-persona-view.py --self-test
```

CI job: `check-persona-view`
<!-- END GENERATED:HOW-TO-RUN -->
