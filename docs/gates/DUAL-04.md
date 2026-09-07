# DUAL-04: `shared/` and the generated `first-principles/` tree are in sync.

<!-- GENERATED:FACTS -->
## Facts

- `derived_counts` (1 entries): `generated_target_count`=48
- `registered_surfaces` (4): `estimate`, `fishbone`, `five-whys`, `theoretical-limit`
- `locked_constants` (1 entries): `generated_marker`='<!-- GENERATED — DO NOT EDIT. Source: shared/{source_rel}. Regenerate via: scripts/sync-content.py --write. -->\n'
- `control_ids` (11): `a`, `b`, `c`, `d`, `e`, `f`, `g`, `h`, `i`, `j`, `k`
- `control_count`: `11`
<!-- END GENERATED:FACTS -->

<!-- GENERATED:HOW-TO-RUN -->
## How to run

```sh
python3 scripts/sync-content.py --check
```

CI job: `sync-check`
<!-- END GENERATED:HOW-TO-RUN -->

## How to run, in detail

Exit 1 on any drift. This is the same check as the pre-commit sync-drift gate — it fires before a
commit locally, and again in CI on push/PR. To fix drift:

```sh
python3 scripts/sync-content.py --write && git add -u
```
