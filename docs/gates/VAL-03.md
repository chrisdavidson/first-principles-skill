# VAL-03: Relative Markdown link validity across the plugin, `shared/`, and `docs/` trees; `docs/` anchors validated with a github-slugger rule.

<!-- GENERATED:FACTS -->
## Facts

- `scan_globs` (3 entries): `docs_check`, `full_check`, `namespace_only`
- `locked_constants` (2 entries): `plugin_root_token`='${CLAUDE_PLUGIN_ROOT}', `plugin_root_token_target`='first-principles'
<!-- END GENERATED:FACTS -->

<!-- GENERATED:HOW-TO-RUN -->
## How to run

```sh
python3 scripts/check-links.py --self-test && python3 scripts/check-links.py && <pytest-capable interpreter> -m pytest scripts/check-links_anchors_test.py -q
```

CI job: `check-links`
<!-- END GENERATED:HOW-TO-RUN -->

## How to run, in detail

Em-dash headings produce double-hyphen anchors, which the anchor-validation rule accounts for.
`docs/-prefixed` links inside `docs/` are flagged as CF-04 violations. `docs/history/**` is
excluded from the scan (frozen archives).
