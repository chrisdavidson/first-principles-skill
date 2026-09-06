# BATT-06: Offline merged dual-signal routing-battery self-test (boundary + focused-output); owns the honest-state and anti-masking sentinels.

<!-- GENERATED:FACTS -->
## Facts

- `locked_constants` (4 entries): `boundary_n_threshold`=2, `boundary_p_threshold`=2, `focused_n_threshold`=1, `focused_p_threshold`=4
- `disclosed_bounds_anchors` (11): `RR-108-02`, `RR-108-04`, `RR-108-05`, `RR-114-01`, `RR-117-01`, `RR-117-02`, `RR-119-01`, `RR-119-02`, `RR-77-08`, `RR-79-01`, `RR-80-01`
- `derived_counts` (1 entries): `rr_sentinel_count`=11
- `checked_files` (1): `first-principles`
<!-- END GENERATED:FACTS -->

<!-- GENERATED:HOW-TO-RUN -->
## How to run

```sh
python3 scripts/check-routing-battery.py --self-test
```

CI job: `check-routing-battery`
<!-- END GENERATED:HOW-TO-RUN -->
