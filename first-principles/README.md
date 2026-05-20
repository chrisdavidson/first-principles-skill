# First Principles Thinking — Claude Code Plugin

A Claude Code plugin packaging the 5-phase first-principles methodology and
six companion thinking tools as namespaced skills.

> **Status:** v2.0.0-alpha — Phase 15 scaffolding only. Full spine and
> companion-tool skills land in Phases 16–17. See the repo root for the
> shippable v1.2 single-skill install.

## Install (dev)

```bash
claude --plugin-dir ./first-principles
```

## Performance tip

This plugin ships 7 skills (the spine plus six companion tools), whose
`description:` fields together occupy a non-trivial share of Claude Code's
default 1% skill-listing budget. Users who run this plugin alongside many
other skills may want to raise that budget so all 7 descriptions stay
visible to the model during skill routing. Set `skillListingBudgetFraction`
to `0.02` in Claude Code user settings (`~/.claude/settings.json`) to
double the listing budget to 2%. This is a per-user preference — the
plugin manifest is unchanged.

For the marketplace install path and the v1.2 single-skill install path, see
the repo root README (updated in Phase 18).
