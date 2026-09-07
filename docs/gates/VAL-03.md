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

## Disclosed bounds

<!-- HAND-WRITTEN: preserved verbatim across regeneration. -->

**`docs/gates/*.md` is inside `DOCS_CHECK_GLOBS` as of plan 21-10 (D-21-H).** The generated pages
are a claim surface and the CI-gate tables link into them; leaving them unchecked would be
inherited coverage assumed rather than granted. See `scripts/check-links.py`'s own module
docstring for the derived glob list this gate actually reaches. Widening proved non-vacuous by a
two-direction mutation on a scratch copy: a broken relative link introduced into one
`docs/gates/*.md` page is reported citing that file with the glob present, and goes unreported
with it removed.

**A `docs/gates/*.md` page's own `../`-prefixed links (back up to `docs/`) are not validated at
all** — `_check_docs_file`'s fourth validation rule skips any `../`-relative target unconditionally, a pre-existing
behavior this widening inherits rather than changes. Contrast with VAL-02
([`docs/gates/VAL-02.md`](VAL-02.md)), which was deliberately NOT widened.
