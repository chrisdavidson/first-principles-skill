# EMIT-STAGE-A: Offline controls for the capture protocol that reads the AGENT'S OWN document rather than the main session's summary of it.

<!-- GENERATED:FACTS -->
## Facts

- `control_ids` (21): `C01`, `C02`, `C03`, `C04`, `C05`, `C06`, `C07`, `C08`, `C09`, `C10`, `C11`, `C12`, `C13`, `C14`, `C15`, `C16`, `C17`, `C18`, `C19`, `C20`, `C21`
- `control_count`: `21`
- `registered_surfaces` (2): `docs/emission-phase1-preregistration.md`, `tests/trackb-catalog-v9.13.md`
- `checked_files` (2): `tests/emission-stage-a-v9.14/raw/*.jsonl`, `tests/emission-stage-a-v9.14/documents/*.md`
- `locked_constants` (4 entries): `MIN_SECTIONS`=4, `MIN_WORDS`=120, `MODEL`='claude-sonnet-5', `N_PROMPTS`=10
- `disclosed_bounds_anchors` (2): `derivation detector sensitivity is 1 of 2 at document level, hand-audited`, `delivery_route reads the transport, never what a UI renders`
<!-- END GENERATED:FACTS -->

<!-- GENERATED:HOW-TO-RUN -->
## How to run

```sh
python3 scripts/check-emission-stage-a.py --self-test
```

CI job: `check-emission-stage-a`
<!-- END GENERATED:HOW-TO-RUN -->
