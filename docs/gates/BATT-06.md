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

## How to run, in detail

Captures each prompt in `tests/routing-battery-catalog.md` once and scores both the
boundary-discipline signal and the focused-output signal. In CI only the offline `--self-test`
above runs; the full live battery is a developer tool — see `CLAUDE.md`'s "Routing battery
(requires a running Claude Code session)" section for the full live-run command with catalog and
threshold flags.

The `--self-test` mode exercises the boundary and focused-output fixture suites from
`scripts/_battery_core.py`, including the anti-masking sentinels (see
[docs/TESTING.md § Anti-masking measurement invariants](../TESTING.md#anti-masking-measurement-invariants)).
