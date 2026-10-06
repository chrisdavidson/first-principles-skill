# CONF-DRIFT: `docs/conformance-baseline.md` and `docs/data/conformance.json` reproduce byte-for-byte a fresh `report-conformance.py` run.

<!-- GENERATED:FACTS -->
## Facts

- `registered_surfaces` (5): `first-principles/references/examples/*.md`, `shared/examples/*.md`, `shared/spine/references/output-template.md`, `tests/adversarial-corpus-v9.0/*.md`, `tests/live-conformance-v9.0/*.jsonl`
- `checked_files` (2): `docs/conformance-baseline.md`, `docs/data/conformance.json`
- `locked_constants` (1 entries): `surface_names`='adversarial-corpus | contract-surface | generated-twin | live-conformance | recurrence-reading | shared-examples'
<!-- END GENERATED:FACTS -->

<!-- GENERATED:HOW-TO-RUN -->
## How to run

```sh
python3 scripts/report-conformance.py --check
```

CI job: — (not a CI job)
<!-- END GENERATED:HOW-TO-RUN -->
