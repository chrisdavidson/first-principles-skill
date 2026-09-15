# REG-GUARD: Registration completeness over two surfaces: (a) every skill directory and the main agent carry a frontmatter `name:` matching their own basename, and every skill stub's `disable-model-invocation` is `true` -- the property VAL-04's 4-gram collision scan was a proxy for (999.104); (b) every gate this file's own battery registers has a matching `name: <job> (<GATE-ID>)` job in `.github/workflows/validation.yml`, the gates named in `BATTERY_ONLY_GATE_IDS` exempt.

<!-- GENERATED:FACTS -->
## Facts

- `control_ids` (32): `c1`, `c10`, `c11`, `c12`, `c13`, `c14`, `c15`, `c16`, `c17`, `c18`, `c19`, `c2`, `c20`, `c21`, `c22`, `c23`, `c24`, `c25`, `c26`, `c27`, `c28`, `c29`, `c3`, `c30`, `c31`, `c32`, `c4`, `c5`, `c6`, `c7`, `c8`, `c9`
- `control_count`: `32`
- `registered_surfaces` (2): `plugin axis (skill/agent frontmatter name: matches directory/file basename; every skill stub's disable-model-invocation is true)`, `CI-job axis (every battery gate id has a matching name: <job> (<GATE-ID>) job)`
- `checked_files` (4): `.github/workflows/validation.yml`, `first-principles/.claude-plugin/plugin.json`, `first-principles/agents/first-principles.md`, `scripts/check-firewall-battery.sh`
- `locked_constants` (2 entries): `battery_only_gate_ids`, `required_disable_model_invocation`
<!-- END GENERATED:FACTS -->

<!-- GENERATED:HOW-TO-RUN -->
## How to run

```sh
python3 scripts/check-registration.py --self-test && python3 scripts/check-registration.py
```

CI job: `check-registration`
<!-- END GENERATED:HOW-TO-RUN -->
