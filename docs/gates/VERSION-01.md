# VERSION-01: Every hand-maintained version stamp carries the same value.

<!-- GENERATED:FACTS -->
## Facts

- `derived_counts` (1 entries): `stamp_source_kind_count`=4
- `registered_surfaces` (4): `.claude-plugin/marketplace.json`, `first-principles/.claude-plugin/plugin.json`, `shared/skills/*/SKILL.md`, `shared/spine/SKILL.meta.yml`
<!-- END GENERATED:FACTS -->

<!-- GENERATED:HOW-TO-RUN -->
## How to run

```sh
python3 scripts/check-version-stamps.py --self-test && python3 scripts/check-version-stamps.py
```

CI job: `check-version-stamps`
<!-- END GENERATED:HOW-TO-RUN -->

## How to run, in detail

The 4 hand-maintained stamp source kinds (`derived_counts.stamp_source_kind_count` above) are the
per-skill `shared/skills/*/SKILL.md` sources, `shared/spine/SKILL.meta.yml`,
`.claude-plugin/marketplace.json`, and `first-principles/.claude-plugin/plugin.json`.

Unlike most gates, both modes matter here: the invariant is a property of the working tree, so
the self-test alone would prove only that the detector works, not that the tree is consistent.

Why it exists: plugin installs are version-gated, not content-gated. An edit that ships without a
version bump never reaches an installed session, so a single missed stamp produces an inert
update while every other gate stays green. Nothing previously asserted *equality* —
`sync-content.py` copies `metadata.version` through per-file rather than propagating one source of
truth, and the version-string invariant in
[CONFIGURATION.md](../CONFIGURATION.md#key-invariants) checks a stamp's **format**, not its
agreement with the others.

The stamp count is reported, never asserted. Hardcoding it would recreate the drift the gate
exists to catch: a newly added skill is discovered by glob automatically, and one that forgets its
stamp fails on presence instead of on a magic number.

The 4 walked source kinds above are what `registered_surfaces` in the Facts fence names — the
surfaces `collect_stamps()`'s own four walk sites actually reach, floored against that roster in
both directions by `self_test()` (a fabricated roster entry nothing walks fails as an over-claim;
a walked source the roster fails to declare fails as an under-claim).

The generated tree under `first-principles/agents/**` and `first-principles/skills/**` is
deliberately EXCLUDED from that walk — not one of the four kinds `registered_surfaces` names —
because those stamps are produced by `sync-content.py` from the `shared/` sources above, and
DUAL-04 (`sync-content.py --check`) already fails on any divergence between them.
