# PROV-GUARD: The self-test is an offline regression test of the verifier's own parsing, join and literal-location logic (D-16 positive/negative/anti-masking controls), not a product guard.

<!-- GENERATED:FACTS -->
## Facts

- `control_ids` (33): `D03-zeroliteral-negative`, `D03-zeroliteral-positive`, `D04-misattributed-negative`, `D04-misattributed-positive`, `D06-orphan-negative`, `D06-orphan-positive`, `D08-unreadable-negative`, `D08-unreadable-positive`, `FLOOR-covered-negative`, `FLOOR-nofetch-negative`, `FLOOR-zerogt-positive`, `FLOOR-zerolabel-positive`, `GATE01-antimask-selfproof`, `PROV01-labelform-negative`, `PROV01-labelform-positive`, `PROV02-ambiguous-negative`, `PROV02-ambiguous-positive`, `PROV02-anchor-negative`, `PROV02-bind-positive`, `PROV02-dispatch-raises`, `PROV02-readarm-negative`, `PROV02-readarm-positive`, `PROV02-unmatched-negative`, `PROV03-located-positive`, `PROV03-unlocated-negative`, `PROV04-network-armed-proof`, `PROV04-network-blocked`, `PROV05-record-roundtrip`, `REACH-labelform-negative`, `REACH-labelled-source-positive`, `REACH-labelperiod-positive`, `REACH-marker-positive`, `describe`
- `control_count`: `33`
- `registered_surfaces` (2): `tests/quality-provenance-v8.24/PR-P1.jsonl`, `tests/quality-provenance-v8.24/PR-P1.md`
- `locked_constants` (1 entries): `no_network_control`='PROV04-network-blocked'
<!-- END GENERATED:FACTS -->

<!-- GENERATED:HOW-TO-RUN -->
## How to run

```sh
python3 scripts/check-provenance.py --self-test
```

CI job: — (not a CI job)
<!-- END GENERATED:HOW-TO-RUN -->
