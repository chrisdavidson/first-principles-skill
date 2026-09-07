# PRECOMMIT:claim-surface-drift-gate: Blocks if `CLAUDE.md`'s/`docs/ARCHITECTURE.md`'s generated gate tables, `docs/TESTING.md`'s generated index, or any `docs/gates/<ID>.md` page no longer match a fresh `scripts/gen-gate-docs.py --write` run, or if CONF-13's standing literal scanner finds a non-exempt hand-maintained count literal — the same check as CONF-SURFACE, fired before commit rather than in CI/battery.

<!-- GENERATED:FACTS -->
## Facts

This gate carries no `--describe`-derived facts (nothing consumed yet).
<!-- END GENERATED:FACTS -->

<!-- GENERATED:HOW-TO-RUN -->
## How to run

```sh
python3 scripts/gen-gate-docs.py --check
```

CI job: — (not a CI job)
<!-- END GENERATED:HOW-TO-RUN -->
