# EVIDENCE-01: Every figure published on `docs/EVIDENCE.md` — the project's public, general-audience measurement record — is re-read from its cited source at generation time, and the committed page must reproduce a fresh render byte-for-byte.

<!-- GENERATED:FACTS -->
## Facts

- `registered_surfaces` (1): `docs/EVIDENCE.md`
- `checked_files` (5): `docs/conformance-baseline.md`, `docs/use-journal.md`, `docs/v8.6-quality-ab-experiment.md`, `docs/v8.7-correctness-spot-check.md`, `docs/v8.7-quality-baseline-freeze.md`
- `population_floors` (1 entries): `facts`=8
- `control_ids` (13): `C01-literals-located`, `C02-corrupted-literal-caught`, `C03-empty-registry-fails`, `C04-render-deterministic`, `C05-trackb-absent-renders-nothing`, `C06-trackb-null-renders-nothing`, `C07-trackb-cleared-renders`, `C08-trackb-malformed-rejected`, `C09-trackb-bad-status-rejected`, `C10-every-fact-states-a-bound`, `C11-no-composite-score`, `C12-trackb2-links-correct-prereg`, `C13-trackb2-requires-and-renders-caveat`
- `control_count`: `13`
<!-- END GENERATED:FACTS -->

<!-- GENERATED:HOW-TO-RUN -->
## How to run

```sh
python3 scripts/gen-evidence-card.py --self-test && python3 scripts/gen-evidence-card.py --check
```

CI job: `gen-evidence-card`
<!-- END GENERATED:HOW-TO-RUN -->
