# REG-GUARD: Registration completeness over two surfaces: (a) every skill directory and the main agent carry a frontmatter `name:` matching their own basename; (b) every gate this file's own battery registers has a matching `name: <job> (<GATE-ID>)` job in `.github/workflows/validation.yml`, QUAL-01 the one named battery-only exemption.

<!-- GENERATED:FACTS -->
## Facts

- `control_ids` (29): `c1`, `c10`, `c11`, `c12`, `c13`, `c14`, `c15`, `c16`, `c17`, `c18`, `c19`, `c2`, `c20`, `c21`, `c22`, `c23`, `c24`, `c25`, `c26`, `c27`, `c28`, `c29`, `c3`, `c4`, `c5`, `c6`, `c7`, `c8`, `c9`
- `control_count`: `29`
- `registered_surfaces` (2): `plugin axis (skill/agent frontmatter name: matches directory/file basename)`, `CI-job axis (every battery gate id has a matching name: <job> (<GATE-ID>) job)`
- `checked_files` (4): `.github/workflows/validation.yml`, `first-principles/.claude-plugin/plugin.json`, `first-principles/agents/first-principles.md`, `scripts/check-firewall-battery.sh`
- `locked_constants` (1 entries): `battery_only_gate_ids`
<!-- END GENERATED:FACTS -->

<!-- GENERATED:HOW-TO-RUN -->
## How to run

```sh
python3 scripts/check-registration.py --self-test && python3 scripts/check-registration.py
```

CI job: `check-registration`
<!-- END GENERATED:HOW-TO-RUN -->
