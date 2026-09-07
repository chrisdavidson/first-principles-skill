# VAL-02: MD style across `first-principles/**/*.md` via `markdownlint-cli2`.

<!-- GENERATED:FACTS -->
## Facts

This gate carries no `--describe`-derived facts (no script backs it).
<!-- END GENERATED:FACTS -->

<!-- GENERATED:HOW-TO-RUN -->
## How to run

```sh
markdownlint-cli2 --config .markdownlint.jsonc 'first-principles/**/*.md'
```

CI job: `markdownlint`
<!-- END GENERATED:HOW-TO-RUN -->

## How to run, in detail

CI uses the `markdownlint-cli2-action`; the command above is how to run the identical check
locally.

## Disclosed bounds

<!-- HAND-WRITTEN: preserved verbatim across regeneration. -->

**This gate is deliberately not widened to `docs/gates/*.md` (D-21-H).** `markdownlint-cli2`
reaches no `docs/` file today — its configured glob is `first-principles/**/*.md` only. Widening
it to cover the generated `docs/gates/` pages would give them lint coverage that
`docs/ARCHITECTURE.md`, `docs/TESTING.md` and every other hand-written `docs/*.md` file still
lack, an inconsistent scope this plan declines to introduce as a side effect of an unrelated
migration. If `docs/` linting is ever wanted, it should be added as its own deliberate decision
covering the whole tree, not smuggled in for one directory. Contrast with VAL-03
([`docs/gates/VAL-03.md`](VAL-03.md)), which WAS widened this phase — the two gates made opposite
calls for a stated reason, not by oversight.
