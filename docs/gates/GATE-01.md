# GATE-01: Agent structural checks — 8 frontmatter/body assertions on the shipped agent, including the exact `maxTurns` value (60), not merely its presence.

<!-- GENERATED:FACTS -->
## Facts

- `branch_roster` (8): `Check 1: file begins with a frontmatter fence and splits into exactly 3 parts`, `Check 2: 'name' key present and equals the locked identity (skipped under --skip-name-check)`, `Check 3: 'description' is a non-empty string within the max-length budget`, `Check 4: 'disallowedTools' key is present`, `Check 5: 'maxTurns' key is present; for the canonical identity only, also carries the locked value (value clause skipped under --skip-name-check)`, `Check 6: body is non-empty after stripping whitespace`, `Check 7: body contains no unresolved sync markers`, `Check 8: 'description' contains all mandatory trigger phrases (skipped under --skip-name-check)`
- `branch_count`: `8`
- `scoped_branches` (3): `Check 2: 'name' key present and equals the locked identity (skipped under --skip-name-check)`, `Check 5: 'maxTurns' key is present; for the canonical identity only, also carries the locked value (value clause skipped under --skip-name-check)`, `Check 8: 'description' contains all mandatory trigger phrases (skipped under --skip-name-check)`
- `locked_constants` (3 entries): `expected_max_turns`=60, `expected_name`='first-principles', `max_description_len`=1024
- `checked_files` (1): `first-principles/agents/first-principles.md`
- `disclosed_bounds_anchors` (1): `live-coverage-anti-vacuity`
<!-- END GENERATED:FACTS -->

<!-- GENERATED:HOW-TO-RUN -->
## How to run

```sh
python3 scripts/check-agent.py --self-test && python3 scripts/check-agent.py
```

CI job: `check-agent`
<!-- END GENERATED:HOW-TO-RUN -->

## How to run, in detail

Structural integrity check for the assembled agent: frontmatter schema, required fields,
`disallowedTools`, version format, and description constraints. The run command above already
sequences the offline `--self-test` fixture before the live file check.
