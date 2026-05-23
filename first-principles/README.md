# First Principles Thinking — Claude Code Plugin

> **v3.0.0 — Plugin contents removed.** The 7 namespaced skills (`first-principles:thinking`, `:five-whys`, `:pre-mortem`, `:trade-off`, `:fishbone`, `:inversion`, `:second-order`) and the root monolith have been removed. The recommended (and only shipped) interface is the **first-principles agent** — invoke `@agent-first-principles:first-principles` or `/first-principles:first-principles`. See [/CHANGELOG.md](../CHANGELOG.md) for the upgrade path.

A Claude Code plugin packaging the 5-phase first-principles methodology as a single agent, with six on-demand companion thinking tools loaded as agent reference siblings.

## What this plugin ships

- **One agent** at `agents/first-principles.md` — the methodology spine with all five phases inlined.
- **Six on-demand reference siblings** under `agents/references/` — Five Whys, fishbone, inversion, pre-mortem, trade-off analysis, second-order thinking. The agent loads each on demand when the relevant trigger fires; no recurring token cost from technique procedures that aren't being used.
- **Six worked examples** under `agents/references/examples/` — software/systems, product/business, personal/general, science/engineering, ishikawa fishbone, and composed inversion + second-order. Pulled in by the agent when an in-context illustration helps.

## Install (dev)

```bash
claude --plugin-dir ./first-principles
```

## Invoke

```text
@agent-first-principles:first-principles   # auto-routed
/first-principles:first-principles         # explicit
```

Verify with `/doctor` inside Claude Code; the `first-principles` agent should appear in the listing.

For marketplace install and the full upgrade path from v2.x, see the repo-root [README](../README.md) and [CHANGELOG.md](../CHANGELOG.md).
