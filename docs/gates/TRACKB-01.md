# TRACKB-01: Offline controls for the pre-registered agent-vs-unaided comparative harness — the project's first measurement against NOT using its own agent, every prior 'A/B' here having contrasted two versions of the same agent body.

<!-- GENERATED:FACTS -->
## Facts

- `registered_surfaces` (3): `docs/trackb-preregistration.md`, `docs/trackb-neutral-rubric.md`, `tests/trackb-catalog-v9.13.md`
- `control_ids` (17): `C01-rubric-format-neutral`, `C02-rubric-neutralises-format-and-length`, `C03-judge-prompt-no-leak`, `C04-catalog-parses-balanced`, `C05-scoreline-roundtrip`, `C06-malformed-scorelines-rejected`, `C07-permutation-calibrated`, `C08-drift-blocks-noise-sized-effect`, `C09-no-drift-arm-cannot-clear`, `C10-real-effect-does-clear`, `C11-broken-mechanics-inconclusive`, `C12-extraction-integrity`, `C13-prereg-code-agree`, `C14-status-vocabulary`, `C15-transport-bg-wait-fix`, `C16-delegation-stub-rejected`, `C17-status-is-derived-not-asserted`
- `control_count`: `17`
<!-- END GENERATED:FACTS -->

<!-- GENERATED:HOW-TO-RUN -->
## How to run

```sh
python3 scripts/check-trackb-comparative.py --self-test
```

CI job: `check-trackb-comparative`
<!-- END GENERATED:HOW-TO-RUN -->
