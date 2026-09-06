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
