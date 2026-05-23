# Changelog

All notable changes to this project are documented in this file.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [3.0.0] - 2026-05-23

### Removed

- Standalone monolith skill at `first-principles-thinking/`. Users who copied this to `~/.claude/skills/` should remove that local copy manually:
  `rm -rf ~/.claude/skills/first-principles-thinking`
- 7 namespaced plugin skills at `first-principles/skills/{thinking,five-whys,pre-mortem,trade-off,fishbone,inversion,second-order}/`. The Phase 26 forwarding language ("still installable") is superseded — these surfaces no longer exist.

### Added

- First-principles agent surface at `first-principles/agents/first-principles.md` (initially shipped Phase 23 in the v3.0-alpha series; now the sole installable interface).
- 6 on-demand companion-tool reference siblings under `first-principles/agents/references/{five-whys,fishbone,inversion,pre-mortem,trade-off,second-order}.md`.
- 6 worked-example siblings under `first-principles/agents/references/examples/` (migrated from the deleted monolith examples directory).

### Upgrade path

- Install: `claude --plugin-dir ./first-principles` for dev, or via the marketplace (`/plugin marketplace add chrisdavidson/first-principles-skill` then `/plugin install first-principles@first-principles-skill`).
- Invoke: `@agent-first-principles:first-principles` (auto-routing) or `/first-principles:first-principles` (explicit).
- If you previously copied `first-principles-thinking/` into `~/.claude/skills/`, delete that local copy manually — Claude Code does not auto-remove it.

### Reference

- Per-technique deep procedures now ship as agent-loaded reference files (`first-principles/agents/references/`).
- The 5-phase methodology text formerly carried by the monolith body is inlined in the agent body itself.
