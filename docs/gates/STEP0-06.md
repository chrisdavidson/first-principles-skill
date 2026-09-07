# STEP0-06: Offline Step 0 live-harness scoring/parsing logic self-test.

<!-- GENERATED:FACTS -->
## Facts

- `locked_constants` (2 entries): `baseline_version`='v8.5', `transport_command`='claude -p --plugin-dir <plugin_dir> --no-session-persistence --output-format stream-json --verbose --permission-mode bypassPermissions <prompt>'
- `checked_files` (2): `tests/step0-baseline-v8.5.md`, `tests/step0-fixture-catalog.md`
- `control_ids` (23): `fixture-focused_premortem`, `fixture-full_composer_structural`, `fixture-none_with_dispatch_LOAD_BEARING`, `fixture-none_without_dispatch`, `kn-rejection`, `catalog-parse-valid`, `catalog-parse-unknown-mode`, `priority-subset-reorder`, `priority-subset-none-passthrough`, `priority-subset-no-mutate`, `tally-8-drift`, `known-modes-size-drift`, `d01a-failing-sp16-firewall`, `d01a-failing-sn-firewall`, `non-block-neg`, `scrubbed-slug-absence`, `routing-count-drift`, `v85-emitter-target`, `routing-emitter-absence`, `rr-id-coverage`, `null-subagent-no-raise`, `reduced-run-denominator`, `describe`
- `control_count`: `23`
<!-- END GENERATED:FACTS -->

<!-- GENERATED:HOW-TO-RUN -->
## How to run

```sh
python3 scripts/check-step0-live.py --self-test
```

CI job: `check-step0-live`
<!-- END GENERATED:HOW-TO-RUN -->

## How to run, in detail

Forces invocation of the agent body via the approach-② bypass channel against a running `claude`
session. Classifies each run's `MODE` from the captured stream. The offline `--self-test` above
asserts the scoring and parsing logic without invoking Claude — see `CLAUDE.md`'s measurement
harness section for the full live-run command with catalog and threshold flags.

The full live run against `tests/step0-fixture-catalog.md` is the canonical manual baseline (see
`tests/step0-baseline-v7.8.md`).

A K-of-N result from the full live run is a recorded observation, never a gate — see `CLAUDE.md`'s
"K-of-5 is a recorded observation, not a gate" note for the full disclosure, including why the
tool's own invocation and pass-threshold flag stay unchanged.
