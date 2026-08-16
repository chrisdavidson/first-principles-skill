# First Principles Thinking — Claude Code Plugin

A Claude Code plugin packaging the 5-phase first-principles methodology as an agent, with
companion thinking techniques loaded on demand rather than carried in every context.

## What this plugin ships

- **One agent** at `agents/first-principles.md` — the methodology spine, all five phases inlined.
- **Eight companion-technique references** under `agents/references/` — Five Whys, fishbone,
  inversion, pre-mortem, trade-off analysis, second-order thinking, estimate, and
  theoretical-limit. The agent loads each on demand when the relevant trigger fires, so a
  technique that is not being used costs no context. Four of them carry a further `-detail.md`
  appendix, loaded only on a named trigger.
- **Two spine references** — `agents/references/output-template.md` (the output document's
  section shape) and `agents/references/validation-rubric.md` (the self-audit gate), plus
  `assumption-taxonomy.md` for within-type assumption subtypes.
- **Fourteen worked examples** under `agents/references/examples/` — spread across
  software/systems, product/business, personal/general, and science/engineering, each showing a
  real dead-end and a complete validation pass. Pulled in when an in-context illustration helps.
- **Fourteen slash-invocable skills** under `skills/` — a full-analysis launcher plus thirteen
  focused modes (the eight techniques above and five phase skills: identify-essence,
  challenge-assumptions, ground-truths, reason-upward, validate). All are registered
  slash-only (`disable-model-invocation: true`); the agent never auto-routes to them.

## Install

```sh
/plugin marketplace add chrisdavidson/first-principles-skill
/plugin install first-principles@first-principles-skill
```

For a local development install instead:

```bash
claude --plugin-dir ./first-principles
```

## Invoke

```text
@agent-first-principles:first-principles   # auto-routed
/first-principles:first-principles         # explicit
/first-principles:five-whys                # a focused mode, by name
```

Verify with `/doctor` inside Claude Code; the `first-principles` agent should appear in the listing.

Automatic delegation is not reliable in every session — prefer the explicit slash form when it
matters.

## More

- [Getting started](https://github.com/chrisdavidson/first-principles-skill/blob/master/docs/GETTING-STARTED.md)
  — install options, verification, invoking each skill, common issues.
- [Repo README](https://github.com/chrisdavidson/first-principles-skill/blob/master/README.md)
  — what the methodology is and when to reach for it.
- [CHANGELOG](https://github.com/chrisdavidson/first-principles-skill/blob/master/CHANGELOG.md)
  — release history, including the v2.x → v3.0.0 upgrade path.

Links here are absolute on purpose: `docs/` and the repo root are not part of an installed
plugin, so a relative link out of this directory would be dead for anyone who installed rather
than cloned.
