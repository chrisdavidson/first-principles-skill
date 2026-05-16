# Architecture Research

**Domain:** Content-heavy pure-Markdown Claude Code skill (first-principles thinking methodology)
**Researched:** 2026-05-16
**Confidence:** HIGH

## Standard Architecture

A Claude Code skill is a directory with `SKILL.md` as the required entrypoint plus
optional supporting files. It is not a runtime system — it is a *context-loading*
system. The "architecture" is an information architecture: deciding which content
loads always, which loads on demand, and how Claude navigates between the two.

### The three-layer loading model

```
┌─────────────────────────────────────────────────────────────┐
│  LAYER 1 — Metadata (always in context, ~100 tokens)         │
│  YAML frontmatter: name + description                        │
│  Loaded at session startup for EVERY skill installed.        │
│  Job: let Claude decide whether the skill is relevant.       │
├─────────────────────────────────────────────────────────────┤
│  LAYER 2 — SKILL.md body (loaded when skill triggers)        │
│  The methodology, output format, navigation map.             │
│  Stays in context for the rest of the session.              │
│  Job: be the complete operating procedure + table of        │
│       contents to deeper material. Target < 500 lines.       │
├─────────────────────────────────────────────────────────────┤
│  LAYER 3 — Supporting files (loaded on demand, per-file)     │
│  references/*.md  — depth Claude reads when a task needs it  │
│  examples/*.md    — worked analyses Claude reads to pattern- │
│                     match output quality                    │
│  Zero token cost until Claude runs Read on the specific file.│
└─────────────────────────────────────────────────────────────┘
```

The mechanism that makes this work: skill files live on the filesystem. Claude reads
them with the Read tool only when it decides they are needed. A 5,000-line
`references/` file costs nothing until the moment Claude opens it. This is
"progressive disclosure" — the architectural primitive the whole design is built on.

### Component Responsibilities

| Component | Responsibility | What lives here |
|-----------|----------------|-----------------|
| `SKILL.md` frontmatter | Discovery — make Claude trigger the skill at the right time | `name`, `description` (with trigger phrases), `version` |
| `SKILL.md` body | The always-on operating procedure: the sharpened 5-phase methodology, the output format/template, the navigation map to Layer 3, and a quick-reference checklist | Core methodology, output template, "Additional resources" pointers |
| `references/` | On-demand depth: companion thinking tools, the validation rubric, domain-specific guidance that is too long or too situational to keep always-loaded | 5-Whys, pre-mortem, trade-off analysis, validation rubric |
| `examples/` | On-demand worked analyses: complete first-principles analyses Claude reads to calibrate output quality and format | One worked example per domain |

## Recommended Project Structure

```
first-principles-skill/                 # the skill directory (v1 deliverable)
├── SKILL.md                            # Layer 1 + 2: methodology, format, nav map
├── README.md                           # human-facing install/usage docs (not loaded by Claude)
├── LICENSE                             # MIT, carried from the original
├── references/                         # Layer 3: on-demand depth
│   ├── validation-rubric.md            # the self-check scoring rubric
│   ├── five-whys.md                    # companion tool: root-cause drill-down
│   ├── pre-mortem.md                   # companion tool: failure-first analysis
│   ├── trade-off-analysis.md           # companion tool: structured option comparison
│   └── methodology-deep-dive.md        # OPTIONAL: overflow depth for the 5 phases
└── examples/                           # Layer 3: on-demand worked analyses
    ├── software-systems.md             # domain 1: software/systems
    ├── product-business.md             # domain 2: product/business
    ├── personal-general.md             # domain 3: personal/general decisions
    └── science-engineering.md          # domain 4: science/engineering
```

### Structure Rationale

- **`SKILL.md` stays lean (target 250–400 lines, hard ceiling 500).** It holds the
  methodology because the methodology must be in context for the *entire* analysis —
  it is standing instruction, not lookup material. Everything that is consulted
  *situationally* moves to Layer 3.
- **`references/` = "things Claude applies."** The validation rubric and the three
  companion tools are procedures invoked at specific moments (rubric at the validate
  phase; companion tools when a sub-problem calls for them). They do not need to be
  resident the whole session, so they belong on demand.
- **`examples/` = "things Claude reads to imitate."** Worked analyses are calibration
  material. Claude opens the one matching the current domain to see what "good"
  looks like, then closes the loop. Keeping four separate domain files (rather than
  one mega-file) means Claude loads only the ~1 relevant example, not all four.
- **One file per companion tool, one file per domain example.** Grouping (e.g. all
  three tools in `companion-tools.md`) would force Claude to load all three when it
  needs one — the opposite of progressive disclosure. Splitting by the natural unit
  of use keeps each on-demand load minimal and focused.
- **`methodology-deep-dive.md` is optional and a judgment call.** If the sharpened
  5-phase methodology fits comfortably under ~400 lines in `SKILL.md`, do not create
  it. If sharpening adds enough depth (per-phase worked micro-examples, expanded
  assumption taxonomy) to push `SKILL.md` past 500 lines, split the *elaboration*
  into this file and keep the *procedure* in `SKILL.md`. The procedure must always
  stay in Layer 2; only the elaboration moves.
- **`README.md` is for humans, not Claude.** Claude Code does not load `README.md`
  into context. It documents installation (copy/symlink) and usage. Keep it separate
  from `SKILL.md` so the skill body carries zero install boilerplate.

## Architectural Patterns

### Pattern 1: SKILL.md as table of contents (high-level guide with references)

**What:** `SKILL.md` contains the complete core procedure plus a clearly labelled
"Additional resources" section that names each Layer 3 file and states *when* to
open it. Claude treats this like a table of contents.

**When to use:** Always, for this skill. It is the canonical progressive-disclosure
pattern from Anthropic's skill-authoring guidance.

**Trade-offs:** Requires discipline to keep `SKILL.md` from absorbing reference
content. The payoff is a lean always-on context and unbounded depth on demand.

**Example (the navigation section of SKILL.md):**
```markdown
## Companion thinking tools

Bring in a companion tool when the analysis needs it:

- Stuck on *why* something is true → see [references/five-whys.md](references/five-whys.md)
- Pressure-testing a proposed solution → see [references/pre-mortem.md](references/pre-mortem.md)
- Choosing between viable options → see [references/trade-off-analysis.md](references/trade-off-analysis.md)

## Validating the analysis

Before presenting conclusions, score the analysis against the rubric in
[references/validation-rubric.md](references/validation-rubric.md).

## Worked examples

Match the domain, then read the relevant example for format and rigor:

- Software/systems → [examples/software-systems.md](examples/software-systems.md)
- Product/business → [examples/product-business.md](examples/product-business.md)
- Personal/general → [examples/personal-general.md](examples/personal-general.md)
- Science/engineering → [examples/science-engineering.md](examples/science-engineering.md)
```

### Pattern 2: References one level deep (flat navigation)

**What:** Every Layer 3 file links *directly* from `SKILL.md`. No reference file
links to another reference file as a required next step.

**When to use:** Always. Anthropic's guidance is explicit: nested references cause
Claude to partially read files (`head -100` previews) and miss content.

**Trade-offs:** Cross-references between Layer 3 files are allowed for *context*
("the pre-mortem pairs well with trade-off analysis"), but never as a required
read-this-next chain. If file A genuinely needs file B's content, the path to B
must also be reachable directly from `SKILL.md`.

**Example:**
```
GOOD:  SKILL.md → references/five-whys.md
       SKILL.md → references/pre-mortem.md
       SKILL.md → references/validation-rubric.md

BAD:   SKILL.md → references/methodology-deep-dive.md
                     → references/five-whys.md
                        → references/validation-rubric.md
```

### Pattern 3: Table of contents in long reference files

**What:** Any Layer 3 file longer than ~100 lines opens with a `## Contents`
section listing its internal sections.

**When to use:** For the validation rubric and any worked example that runs long.
Worked examples across four domains will likely each exceed 100 lines.

**Trade-offs:** Small duplication (the TOC restates section headings). The payoff:
when Claude previews a file with a partial read, it still sees the full scope.

**Example:**
```markdown
# Validation Rubric

## Contents
- Scoring dimensions (5 criteria)
- Per-dimension scoring guide (0–2 each)
- Pass threshold and interpretation
- Worked scoring example
- Failure-mode quick reference

## Scoring dimensions
...
```

### Pattern 4: Reference content vs. task content (frontmatter intent)

**What:** This skill is *reference content* — knowledge Claude applies to the user's
current work — not *task content* with side effects. It should therefore stay
model-invocable (no `disable-model-invocation`) so Claude triggers it automatically
when the user asks to reason from first principles, and also remain user-invocable
via `/first-principles`.

**When to use:** Set neither `disable-model-invocation` nor `user-invocable: false`.
Both invocation paths are wanted.

**Trade-offs:** None for v1. The default (both you and Claude can invoke) is correct.

## Data Flow

### How Claude moves through the skill during one analysis

```
User: "analyze this design from first principles"
        ↓
[Layer 1] Claude matches the request to the skill's `description`
        ↓
[Layer 2] Claude loads SKILL.md — methodology + output format now resident
        ↓
Claude works the 5 phases:
   Identify Essence → Challenge Assumptions → Establish Ground Truths
        ↓                    ↓
        │            (assumption needs root-cause drilling?)
        │                    ↓
        │            [Layer 3] Read references/five-whys.md
        ↓
   Reason Upward
        ↓
   (comparing options?) → [Layer 3] Read references/trade-off-analysis.md
   (stress-testing?)    → [Layer 3] Read references/pre-mortem.md
        ↓
   Validate
        ↓
   [Layer 3] Read references/validation-rubric.md → score the analysis
        ↓
   (unsure of output shape?) → [Layer 3] Read examples/<matching-domain>.md
        ↓
Claude emits the analysis in the SKILL.md output format
```

### Key data flows

1. **Discovery flow:** `description` frontmatter → Claude's skill-selection decision.
   The trigger phrases (English + Chinese, carried from the original) live here and
   are the single most important factor in whether the skill activates at all.
2. **Methodology flow:** `SKILL.md` body → resident standing instruction for the
   whole analysis. Written as *what to do*, not *one-time steps*, because skill
   content stays in context across turns and is not re-read.
3. **On-demand depth flow:** `SKILL.md` "Additional resources" pointer → Claude's
   Read tool → one specific Layer 3 file. Each load is independent and minimal.
4. **Calibration flow:** worked example in `examples/` → Claude pattern-matches the
   output format and rigor level, then produces its own analysis in that shape.

### State management

There is no runtime state. The only "state" is what is currently in the context
window. The architecture's entire job is to manage that: keep Layer 2 small so it
does not crowd the conversation, and push everything situational to Layer 3 so it
costs zero tokens until the moment of need.

## Scaling Considerations

"Scale" here means content growth and the future multi-skill milestone, not users.

| Scale | Architecture adjustments |
|-------|--------------------------|
| v1 — single skill, ~8 supporting files | Flat `references/` and `examples/`. One file per tool, one per domain. SKILL.md under 500 lines. No further structure needed. |
| Content growth within v1 | If `SKILL.md` nears 500 lines, split *elaboration* (not the procedure) into `references/methodology-deep-dive.md`. If a domain example exceeds ~300 lines, that is fine — it is Layer 3 and loads only when its domain matches. |
| Milestone 2 — collection of skills | Each thinking method becomes its own skill directory (`first-principles/`, `five-whys/`, `pre-mortem/`, `trade-off-analysis/`), all under one `skills/` parent or one plugin. See "Future-milestone compatibility" below. |

### Scaling priorities

1. **First thing that breaks: SKILL.md bloat.** Sharpening the methodology and adding
   the rubric is the most likely cause of crossing 500 lines. Mitigation: the rubric
   is *already* a separate `references/` file by design; keep the methodology
   procedure tight and push elaboration to `methodology-deep-dive.md` only if needed.
2. **Second: example sprawl.** Four domain examples that each grow large are not a
   problem *individually* (on-demand load), but if examples start cross-referencing
   each other they violate the one-level-deep rule. Mitigation: keep every example
   self-contained and linked only from `SKILL.md`.

## Future-Milestone Compatibility

The v1 single-skill structure must not block milestone 2 ("collection of related
thinking skills") or milestone 3 (Python builder). It does not, if these rules hold:

- **The companion tools are written as self-contained units now.** `five-whys.md`,
  `pre-mortem.md`, and `trade-off-analysis.md` each describe a complete method with
  its own purpose, process, and output shape. In milestone 2 each becomes the body of
  its own `SKILL.md` with minimal rewriting — the content is already
  promotion-ready. Writing them as half-methods that only make sense embedded in
  first-principles would force a rewrite later.
- **`SKILL.md` references companion tools by relative path within the skill
  directory.** This is correct for v1. In milestone 2, when each tool is its own
  skill, the in-body links become "see the `five-whys` skill" instead of a file path.
  This is a small, localized edit to one section of `SKILL.md` — not a restructuring.
- **No content duplication across files.** Each fact lives in exactly one file.
  When a companion tool is promoted to its own skill in milestone 2, there is one
  source of truth to move, not several copies to reconcile.
- **The directory is already named and shaped like one skill among many.** The repo
  working directory is `first-principles-skills` (plural) and the skill directory
  itself can sit at the repo root in v1; in milestone 2 it moves under a `skills/`
  parent alongside siblings. Because v1's skill is a clean self-contained directory
  (`SKILL.md` + `references/` + `examples/`), relocating it is a `mv`, not a refactor.
- **The `uv` scaffold stays untouched.** It is the milestone-3 builder foundation.
  v1 adds no Python and no executable scripts (pure-Markdown constraint), so there is
  nothing for the future builder to have to unwind.

The single design decision that protects all three milestones: **treat each companion
tool and each worked example as an independently meaningful, self-contained file.**
Progressive disclosure already demands this for token reasons; it also happens to be
exactly what makes future extraction into separate skills a move-not-rewrite.

## Build Order

Components have real dependencies. Build foundational pieces first so dependent
pieces can reference a stable target.

```
1. Sharpen the 5-phase methodology  ──┐
   (the core procedure + output       │  foundational — everything
    format, tightened from original)  │  else calibrates against this
                                      │
2. SKILL.md skeleton  ────────────────┤
   (frontmatter + methodology + the   │  the navigation map; needs the
    "Additional resources" nav map)   │  sharpened methodology to exist
                                      │
            ┌─────────────────────────┴──────────────────┐
            ↓                          ↓                 ↓
3. Validation rubric        4. Companion tools     5. Worked examples
   (references/                (references/           (examples/*.md ×4)
    validation-rubric.md)        five-whys.md,         depend on 1, 2 AND 3:
   depends on 1 — it scores      pre-mortem.md,        a good example shows
   whether an analysis           trade-off-           the methodology applied
   followed the methodology      analysis.md)         AND scores well on the
                                depend on 1 — they     rubric
                                slot into the
                                methodology's phases
            └─────────────────────────┬──────────────────┘
                                      ↓
6. SKILL.md final pass + README
   (wire every Layer 3 file into the nav map; verify
    one-level-deep links; write human-facing install docs)
```

### Build order rationale

1. **Sharpen the methodology first.** It is the single dependency of everything else.
   The rubric scores against it, the companion tools slot into its phases, the worked
   examples demonstrate it. Sharpening last would invalidate everything built on a
   loose version.
2. **SKILL.md skeleton second.** Establishes the frontmatter, the resident
   methodology, and — critically — the navigation map's *shape*. Later components
   fill named slots in that map rather than the map being retrofitted.
3. **Validation rubric third, before examples.** The rubric must exist before the
   worked examples because a good worked example should itself pass the rubric.
   Building examples first risks producing examples that the later rubric flags.
4. **Companion tools (parallelizable with the rubric).** Each is independent of the
   others and of the rubric. They depend only on the sharpened methodology, to know
   which phase they support. Three separate files, buildable concurrently.
5. **Worked examples last among content.** They depend on items 1, 2, and 3 — an
   example is the methodology applied, in the SKILL.md output format, at a quality
   that passes the rubric. Four domains, each self-contained, buildable concurrently
   once 1–3 are stable.
6. **Final SKILL.md pass + README.** Wire every Layer 3 file into "Additional
   resources," verify all links are one level deep, and write the human-facing
   `README.md` (install by copy/symlink, usage).

**Roadmap implication:** items 3, 4, and 5 are largely parallelizable once 1 and 2
are done — natural candidates for separate phases or parallel work within a phase.
Items 1 and 2 are a strict sequential foundation and should be one early phase. The
methodology-deep-dive split (if needed) is decided during item 2 and executed then,
not deferred.

## Anti-Patterns

### Anti-Pattern 1: Everything in SKILL.md

**What people do:** Put the methodology, all three companion tools, the full rubric,
and worked examples into one large `SKILL.md`.

**Why it's wrong:** The entire file becomes resident context for the whole session
and competes with the conversation. The rubric and examples are consulted at *one
moment*, not continuously — paying their token cost every turn is pure waste. It also
blows past the 500-line guidance.

**Do this instead:** `SKILL.md` holds only what must be resident the whole analysis —
the methodology procedure and output format. Rubric, tools, and examples go to
Layer 3.

### Anti-Pattern 2: Grouping on-demand files by type instead of by use

**What people do:** One `companion-tools.md` holding all three tools; one
`all-examples.md` holding all four domains.

**Why it's wrong:** It defeats progressive disclosure. Needing the 5-Whys tool forces
Claude to load pre-mortem and trade-off analysis too. Needing the software example
forces loading three irrelevant domains.

**Do this instead:** One file per natural unit of use — one file per tool, one file
per domain example.

### Anti-Pattern 3: Nested references

**What people do:** `SKILL.md` → `methodology-deep-dive.md` → `five-whys.md` →
`validation-rubric.md`, a chain of files each linking to the next.

**Why it's wrong:** Anthropic's guidance is explicit — Claude partially reads
files reached through nested links (previewing with `head`), missing content.

**Do this instead:** Every Layer 3 file links directly from `SKILL.md`. Cross-links
between Layer 3 files are allowed only as context notes, never as a required
read-this-next chain.

### Anti-Pattern 4: Duplicating content across files

**What people do:** Restate the 5-phase methodology inside each worked example, or
copy the rubric criteria into `SKILL.md`.

**Why it's wrong:** Multiple sources of truth drift apart on edit, and — specific to
this project — duplication makes the milestone-2 extraction of tools into separate
skills a reconciliation job instead of a clean move.

**Do this instead:** Each fact lives in exactly one file. Examples *apply* the
methodology and reference it; they do not restate it.

### Anti-Pattern 5: Procedural ("one-time step") phrasing in SKILL.md

**What people do:** Write the methodology as "First, do X. Then do Y." as if it runs
once at load time.

**Why it's wrong:** Skill content is injected once and stays resident; Claude does
not re-read it each turn. One-time-step phrasing reads as already-done by later turns.

**Do this instead:** Write the methodology as standing instructions — *what to do
throughout the analysis* — so it keeps applying across turns.

## Integration Points

### External / installation

| Integration | Pattern | Notes |
|-------------|---------|-------|
| Claude Code skills directory | Copy or symlink the skill directory into `~/.claude/skills/` (personal) or `.claude/skills/` (project) | Matches the original repo's install model; the constraint in PROJECT.md |
| Skill discovery | `description` frontmatter, ≤1024 chars, third person, key trigger phrases first | The combined description budget is truncated at 1,536 chars in the skill listing — front-load triggers |

### Internal boundaries

| Boundary | Communication | Notes |
|----------|---------------|-------|
| frontmatter ↔ SKILL.md body | YAML metadata vs. markdown content, same file | `description` drives triggering; body drives execution |
| SKILL.md ↔ references/ | Relative-path links in an "Additional resources" / per-section nav block | One level deep; each link names *when* to open the file |
| SKILL.md ↔ examples/ | Relative-path links, domain-matched | Claude loads the one example matching the analysis domain |
| references/ ↔ references/ | Context-only cross-mentions, never required chains | Keeps navigation flat for complete reads |
| skill ↔ future sibling skills (milestone 2) | Each companion tool file is promotion-ready as a standalone SKILL.md | The compatibility guarantee — written self-contained now |

## Sources

- [Extend Claude with skills — Claude Code Docs](https://code.claude.com/docs/en/skills) — HIGH: official, current. Three-layer loading model, frontmatter reference, skill content lifecycle, the 500-line guidance.
- [Skill authoring best practices — Claude Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) — HIGH: official, current. Progressive-disclosure patterns 1–3, one-level-deep rule, TOC-in-long-files, naming conventions, anti-patterns, evaluation-driven development.
- [anthropics/claude-code — plugin-dev skill-development SKILL.md](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/skill-development/SKILL.md) — HIGH: official reference skill. references/ vs examples/ vs scripts/ boundaries, third-person description rule, no-duplication rule.
- [chrisdavidson/first-principles-skill](https://github.com/chrisdavidson/first-principles-skill) — HIGH: the source repo. Existing structure (SKILL.md ~450 lines, 2 references files, 1 example), 5-phase methodology, frontmatter shape.

---
*Architecture research for: content-heavy pure-Markdown Claude Code skill*
*Researched: 2026-05-16*
