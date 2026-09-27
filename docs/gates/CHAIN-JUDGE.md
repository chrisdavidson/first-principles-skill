# CHAIN-JUDGE: The offline control suite of the only instrument in this tree that judges whether a conclusion's claim is SEMANTICALLY supported by the chain it cites, rather than merely citing it.

<!-- GENERATED:FACTS -->
## Facts

- `control_ids` (7): `structure`, `harness`, `packet`, `parse`, `blinding`, `fixture`, `emission`
- `control_count`: `7`
- `registered_surfaces` (1): `scripts/check-claim-chain-judge.py`
- `disclosed_bounds_anchors` (5): `offline --self-test is gated; the live semantic reading is NOT`, `reach about 6 of 10, membership unstable across passes -- never a rate`, `no precision or false-positive figure exists, by design (999.118)`, `fabricated provenance is unreachable`, `anything outside sections 3/4/6 is outside the packet`
<!-- END GENERATED:FACTS -->

<!-- GENERATED:HOW-TO-RUN -->
## How to run

```sh
python3 scripts/check-claim-chain-judge.py --self-test
```

CI job: `check-claim-chain-judge`
<!-- END GENERATED:HOW-TO-RUN -->
