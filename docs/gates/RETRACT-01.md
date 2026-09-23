# RETRACT-01: A claim a code review found false may never reappear on a published surface.

<!-- GENERATED:FACTS -->
## Facts

- `registered_surfaces` (9): `CHANGELOG.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `README.md`, `docs/**/*.md`, `docs/data/*.json`, `first-principles/**/*.md`, `scripts/*.py`, `shared/**/*.md`
- `derived_counts` (2 entries): `exemption_entries`=3, `registered_retracted_claims`=4
- `control_ids` (10): `C1-absent-passes`, `C10-self-exclusion-is-one-file`, `C2-present-fails`, `C3-exempt-at-count-passes`, `C4-exempt-above-count-fails`, `C5-exempt-below-count-fails`, `C6-empty-registry-fails`, `C7-empty-population-fails`, `C8-live-tree`, `C9-registry-literals-nonempty`
- `control_count`: `10`
<!-- END GENERATED:FACTS -->

<!-- GENERATED:HOW-TO-RUN -->
## How to run

```sh
python3 scripts/check-retracted-claims.py --self-test && python3 scripts/check-retracted-claims.py
```

CI job: `check-retracted-claims`
<!-- END GENERATED:HOW-TO-RUN -->
