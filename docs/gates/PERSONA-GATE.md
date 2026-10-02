# PERSONA-GATE: Checks a reader-persona view against the analysis it was derived from and the contract in `shared/spine/references/persona-views.md` — the memo header (To, Re, Basis, Band) and provenance sentence, the band against section 6, the role's word band, that every sentence carries a citation, that every cited chain, ground-truth (with matching `?` marking), assumption and dead-end id resolves in the source, that every number appears in the source, that the body is a memo — an In brief paragraph, then one paragraph per fixed question with no bullet, no label and no printed question (it counts paragraphs and cannot prove each answers its question), and that a lexical voice check (PV-DIRECTIVE) flags a denylisted imperative opener, second-person address, a verdict on the reader, or a six-word run of §6's recommended approach, over-reporting by design and never judging meaning.

<!-- GENERATED:FACTS -->
## Facts

- `control_ids` (40): `P01`, `P02`, `P03`, `P04`, `P05`, `M-ID`, `M-AGREE`, `M-NUMBER`, `M-UNCITED`, `M-PSEUDO`, `M-BAND`, `M-HEADER`, `M-OVER`, `M-UNDER`, `M-SHAPE`, `M-DEADEND`, `M-Q-BULLET`, `M-Q-BRIEF`, `M-Q-FEW`, `M-Q-MANY`, `M-Q-PRINT`, `M-H-TO`, `M-H-BREAK`, `M-H-BASIS`, `M-H-LINK`, `M-D-OPEN`, `M-D-YOU`, `M-D-RUN`, `G-NAME`, `G-WORDS`, `U01`, `U02`, `U03`, `U04`, `U05`, `D-PRE87`, `EX-REACH`, `EX-REACH-ID`, `EX-REACH-EMPTY`, `EX-REACH-ROSTER`
- `control_count`: `40`
- `registered_surfaces` (3): `shared/spine/references/how-to-read.md`, `shared/spine/references/output-template.md`, `shared/spine/references/persona-views.md`
- `checked_files` (13): `shared/examples/estimate-fermi.md`, `shared/examples/personal-general.md`, `shared/examples/product-business-2.md`, `shared/persona-examples/estimate-fermi-decision-owner.md`, `shared/persona-examples/estimate-fermi-skeptic.md`, `shared/persona-examples/product-business-2-decision-owner.md`, `shared/persona-examples/product-business-2-skeptic.md`, `tests/persona-views-v9.18/personal-general-risk.md`, `tests/persona-views-v9.18/pre87-product-business-2-decision-owner.md`, `tests/persona-views-v9.18/product-business-2-decision-owner.md`, `tests/persona-views-v9.18/product-business-2-operator.md`, `tests/persona-views-v9.18/product-business-2-risk.md`, `tests/persona-views-v9.18/product-business-2-skeptic.md`
- `locked_constants` (9 entries): `directive_openers`, `directive_phrase_openers`, `guide_max_words`, `in_brief_prefix`, `memo_fields`, `provenance_template`, `questions`, `roster`, `verbatim_run_words`
- `derived_counts` (4 entries): `finding_codes`=13, `fixtures`=5, `persona_examples`=4, `personas`=4
- `disclosed_bounds_anchors` (9): `absent-input-sentences-not-checked-for-truth`, `citation-presence-not-semantic-support`, `directive-check-is-lexical-not-semantic`, `fixtures-are-worked-examples-not-live-analyses`, `guide-names-checked-against-output-template-only`, `imperative-check-is-sentence-initial-only`, `memo-structure-counts-paragraphs-not-answers`, `numbers-matched-by-value-not-by-context`, `verbatim-run-checked-against-section6-recommended-approach-only`
<!-- END GENERATED:FACTS -->

<!-- GENERATED:HOW-TO-RUN -->
## How to run

```sh
python3 scripts/check-persona-view.py --self-test
```

CI job: `check-persona-view`
<!-- END GENERATED:HOW-TO-RUN -->
