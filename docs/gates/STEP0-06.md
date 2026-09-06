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
