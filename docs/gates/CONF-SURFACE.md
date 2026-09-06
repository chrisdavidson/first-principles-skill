# CONF-SURFACE: The claim-surface drift gate itself: regenerates `CLAUDE.md`'s and docs/ARCHITECTURE.md's gate tables and docs/gates/<ID>.md pages from this registry's ENTRIES and every gate's --describe emission, and fails on drift.

<!-- GENERATED:FACTS -->
## Facts

This gate carries no `--describe`-derived facts (nothing consumed yet).
<!-- END GENERATED:FACTS -->

<!-- GENERATED:HOW-TO-RUN -->
## How to run

```sh
python3 scripts/gen-gate-docs.py --self-test && python3 scripts/gen-gate-docs.py --check
```

CI job: `gen-gate-docs`
<!-- END GENERATED:HOW-TO-RUN -->
