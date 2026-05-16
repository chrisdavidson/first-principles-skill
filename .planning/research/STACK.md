# Stack Research

**Domain:** Authoring a pure-Markdown Claude Code skill (Agent Skill) — `SKILL.md` + `references/` + `examples/`
**Researched:** 2026-05-16
**Confidence:** HIGH (verified against current official Anthropic / Claude Code docs and the Agent Skills open standard)

## Executive Summary

A Claude Code skill in 2026 is **not a code project** — it is a directory with one required
file (`SKILL.md`) plus optional supporting files. The "stack" is therefore: the **Agent Skills
file format** (an open standard, originally from Anthropic), **Markdown + YAML frontmatter**,
and a thin layer of **optional validation/lint tooling**. There is no build step, no runtime,
no dependency manifest for a pure-Markdown skill. This matches the project's pure-Markdown
constraint perfectly.

Two specs govern this skill, and they differ slightly. The skill must satisfy **both**:

1. **Agent Skills open standard** ([agentskills.io/specification](https://agentskills.io/specification)) — the portable, cross-tool format.
2. **Claude Code's extensions** ([code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills)) — Claude Code adds optional fields and reads the same file.

The safe approach for this project: **author to the open standard's required schema** (`name` + `description`), keep all Claude-Code-specific fields optional, and the skill works everywhere.

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| Agent Skills file format | Current open standard (agentskills.io) | The skill *is* a folder with `SKILL.md` | The single authoritative format. Anthropic-originated, now an open standard adopted across Claude Code, Cursor, Copilot, Gemini CLI, etc. A skill authored to it is portable. |
| Markdown (CommonMark) | n/a | `SKILL.md` body + all `references/` and `examples/` files | The format mandates Markdown body content. No format restrictions on the body — plain CommonMark with fenced code blocks and `<details>` is sufficient and universally rendered. |
| YAML frontmatter | YAML 1.2 | The metadata block between `---` markers at the top of `SKILL.md` | Required by the spec. Only the frontmatter is schema-constrained; everything below it is free-form Markdown. |
| UTF-8, LF line endings, forward-slash paths | n/a | File encoding + path style throughout | Official best practices: always use forward slashes (`references/guide.md`) even on Windows — backslashes break on Unix. |

### Supporting Libraries

This is a pure-Markdown skill, so there are **no runtime libraries**. The "supporting"
tools below are *optional dev-time* aids — none ship inside the skill, none are required
to author or install it.

| Tool | Version | Purpose | When to Use |
|------|---------|---------|-------------|
| `skills-ref` (agentskills/agentskills) | Current | Official reference validator for the open standard. `skills-ref validate ./my-skill` checks frontmatter validity and naming conventions. | Run before each commit / before shipping. The closest thing to an "official linter." Confidence: HIGH (named directly in the spec). |
| `anthropics/skills` repo — `skill-creator` skill | Current | Anthropic's meta-skill: structure guidance, `package_skill.py` (produces a `.skill` bundle), eval scaffolding. | Useful as a *reference example* of a well-built skill. Its packaging script targets Claude.ai distribution — not needed when installing by copy/symlink. |
| `markdownlint` (DavidAnson/markdownlint or markdownlint-cli2) | Current | Generic Markdown style/consistency linting for `SKILL.md` + `references/` + `examples/`. | Optional. Use to enforce consistent heading style and catch broken structure across the repo. See "Development Tools" for config guidance. |

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| `skills-ref validate` | Schema/convention validation of `SKILL.md` | Treat as the gate. Validates: `name` 1-64 chars lowercase-alnum-hyphen, no leading/trailing/consecutive hyphens, **name must match parent directory name**; `description` 1-1024 chars non-empty. |
| `markdownlint-cli2` + `.markdownlint.jsonc` | Repo-wide Markdown consistency | Recommended config below. **Disable `MD013` (line length)** — skill prose is naturally long-line; line-length limits fight readability. **Keep `MD003` (consistent ATX headings)**, `MD040` (fenced code language), `MD041` (first line heading). Optionally relax `MD033` if you use `<details>` for "old patterns" sections. |
| `claude` CLI + `/doctor` | Live diagnosis inside Claude Code | `/doctor` reports whether the skill-listing description budget is overflowing and whether your skill's description is being truncated. There is **no dedicated `claude skill validate` command** — validation is `skills-ref` + live testing. |
| Git | Version control / distribution | The skill ships *as* a git repo. Installation is `git clone` then copy or symlink into a skills directory (see Installation). |

## Installation

This skill is **authored**, not `npm install`-ed. There is no package to install to *build*
it. "Installation" means placing the finished skill folder where Claude Code discovers it.

```bash
# --- Optional dev tooling (host machine, never bundled in the skill) ---

# Official spec validator (run before shipping)
#   Repo: https://github.com/agentskills/agentskills/tree/main/skills-ref
#   Install per that repo's instructions, then:
skills-ref validate ./first-principles-thinking

# Generic Markdown linting (optional)
npm install -D markdownlint-cli2

# --- Installing the finished skill for use (the user-facing model) ---

# Personal skill — available across all the user's projects:
cp -r ./first-principles-thinking ~/.claude/skills/
#   or symlink (keeps the repo as source of truth, edits picked up live):
ln -s "$(pwd)/first-principles-thinking" ~/.claude/skills/first-principles-thinking

# Project skill — committed to a repo, scoped to that project:
cp -r ./first-principles-thinking <project>/.claude/skills/
```

**Critical install rule:** the skill *directory name* must equal the frontmatter `name`
field (open standard requirement) — and the directory name becomes the `/command`.
So the repo's skill folder should be named `first-principles-thinking` (or whatever the
final `name` is), not `first-principles-skill` or `src/`.

## Where Skills Live (Claude Code discovery scopes)

| Scope | Path | Applies to | Use for this project? |
|-------|------|------------|------------------------|
| Personal | `~/.claude/skills/<name>/SKILL.md` | All the user's projects | **Primary install target** — matches the original repo's "copy or symlink into a skills directory" model. |
| Project | `.claude/skills/<name>/SKILL.md` | One project (commit to VCS) | Alternative for teams sharing the skill via a repo. |
| Plugin | `<plugin>/skills/<name>/SKILL.md` | Wherever the plugin is enabled | Out of scope for v1 (single skill, not a plugin/collection). |
| Enterprise | Managed settings | Whole org | Out of scope. |

Claude Code watches `~/.claude/skills/` and project `.claude/skills/` for **live changes**
within a session — edits to an existing skill take effect without restart. This makes
**symlink installs ideal during development**.

## SKILL.md Frontmatter Schema (field-by-field, prescriptive)

The skill must satisfy the open standard's required fields. Claude-Code-specific fields are
all optional and should be used sparingly.

### Required (open standard)

| Field | Constraint | Guidance for this project |
|-------|-----------|----------------------------|
| `name` | 1-64 chars; lowercase letters, numbers, hyphens only; no leading/trailing hyphen; no consecutive hyphens; **must match parent directory name**. | Use a gerund or noun-phrase, e.g. `first-principles-thinking`. Avoid `helper`/`utils`. Do **not** use reserved words `anthropic`/`claude` (Claude Code rejects them). |
| `description` | 1-1024 chars; non-empty; no XML tags; **third person**. | Single most important field — it is the *trigger*. Must state **what it does + when to use it**, front-loading the key use case. See "Description as trigger" below. |

### Optional — open standard (safe, portable)

| Field | Use it? | Notes |
|-------|---------|-------|
| `license` | Optional | Set `license: MIT` to match the original repo's license. Short string or a bundled `LICENSE` filename. |
| `metadata` | **Recommended for versioning** | Free-form key-value map. Put `version: "2.0"` here — see Versioning section. |
| `compatibility` | Skip | Only for skills with environment requirements (system packages, network). A pure-Markdown methodology skill has none. |
| `allowed-tools` | Skip for v1 | Experimental in the open standard. A pure-Markdown thinking skill issues no tool calls of its own; no pre-approval needed. |

### Optional — Claude Code extensions (use deliberately, or not at all)

| Field | Use it? | Notes |
|-------|---------|-------|
| `when_to_use` | Optional | Appends extra trigger phrases/examples to `description`. Counts toward the combined **1,536-char** listing cap. Use only if `description` alone can't carry the triggers. |
| `disable-model-invocation` | **No** | Setting `true` means *only the user* can invoke via `/name` and Claude never auto-loads it. A thinking methodology should trigger automatically when relevant — keep the default (`false`). |
| `user-invocable` | **No** (keep default `true`) | `false` hides it from the `/` menu. Users *should* be able to type `/first-principles-thinking` deliberately. |
| `argument-hint` / `arguments` | Skip for v1 | Useful for skills that take positional arguments. The methodology applies to the conversation context; no structured args needed. |
| `model`, `effort` | Skip | These override the session model/effort. Not appropriate to hard-code in a reusable methodology skill. |
| `context: fork`, `agent` | Skip | Forking into a subagent loses conversation context — wrong for a methodology meant to reason *about the current conversation*. |
| `paths` | Skip | Glob-scoping to file types; this skill is domain-agnostic (software, business, personal, science). |
| `hooks`, `shell` | Skip | No executable behavior in a pure-Markdown skill. |

**Recommended frontmatter for this project:**

```yaml
---
name: first-principles-thinking
description: >-
  Decomposes complex problems into fundamental, verified truths and reasons
  upward from them instead of by analogy. Use when the user wants to evaluate
  a design, challenge assumptions, justify a decision from first principles,
  run a pre-mortem or 5-Whys, or asks "why do we actually do it this way?".
license: MIT
metadata:
  version: "2.0"
---
```

## The `description` Field as a Trigger (the highest-leverage decision)

The `description` is the *only* part of the skill loaded into context at startup. Claude
selects among potentially 100+ skills using `name` + `description` alone. Get this wrong
and the skill never fires.

**Rules (all HIGH confidence, from official best-practices docs):**

- **Third person, always.** The description is injected into the system prompt.
  Good: `"Decomposes problems into fundamental truths..."`.
  Avoid: `"I can help you..."` / `"You can use this to..."`.
- **State what + when.** Pattern: `<what it does>. Use when <concrete triggers>.`
- **Front-load the key use case.** The combined `description` + `when_to_use` is truncated
  at **1,536 characters** in the skill listing; the most important trigger must come first.
- **Include the literal words users say.** "first principles", "challenge assumptions",
  "pre-mortem", "5-whys", "trade-off analysis", "reason from scratch". Skills are matched
  on keyword overlap with the user's request.
- **Be "pushy" against under-triggering.** Anthropic's own `skill-creator` advises wording
  like *"Make sure to use this skill whenever the user mentions X, even if they don't
  explicitly ask for it."* A methodology skill is prone to under-triggering — lean pushy.
- **Multilingual triggers:** the original skill carries English + Chinese triggers. There
  is **no dedicated multilingual field** — multilingual triggers simply live as additional
  phrases inside the one `description` (or `when_to_use`). They consume the same 1,024 /
  1,536-char budget, so keep each language's phrasing tight. Confidence: MEDIUM (no field
  exists; this is the only mechanism the format provides).

**Do NOT:** write vague descriptions (`"Helps with thinking"`, `"Does analysis"`). These
are the #1 cause of a skill never triggering.

## Progressive Disclosure & Size Budget

Skills load in three stages (the core architecture):

1. **Metadata (~100 tokens)** — `name` + `description`, always in context.
2. **`SKILL.md` body** — loaded *in full* the moment the skill triggers; stays in context
   for the rest of the session (recurring token cost every turn).
3. **`references/` and `examples/` files** — loaded **only when SKILL.md points Claude to
   them and the task needs them**. Zero context cost until read.

**Size budgets (HIGH confidence, official):**

| Target | Budget | Source |
|--------|--------|--------|
| `SKILL.md` body | **Under 500 lines** ("for optimal performance"; split when approaching it) | Claude Code docs + best-practices |
| `SKILL.md` body | **< ~5,000 tokens recommended** | Agent Skills spec |
| `description` | ≤ 1,024 chars (hard); ≤ 1,536 chars combined with `when_to_use` (truncation) | Frontmatter reference |
| Reference files | No hard cap — but keep each **focused**; add a table of contents if **> ~100 lines** (so partial reads still reveal scope) | Best-practices |

**When content belongs inline (in SKILL.md) vs in a reference file:**

| Put it in `SKILL.md` | Put it in a `references/` or `examples/` file |
|----------------------|------------------------------------------------|
| The 5-phase methodology steps themselves (the core procedure) | Long worked examples (SpaceX/Tesla, microservices review) |
| The output format / template | Detailed per-domain example walkthroughs |
| The validation rubric checklist (if concise) | The full companion-tool guides (5-Whys, pre-mortem, trade-off) if each is long |
| A short navigation map: "for X see references/x.md" | Reference material the model needs only sometimes |

**Critical structural rule — keep references one level deep.** Every `references/` and
`examples/` file must link **directly from `SKILL.md`**. Do **not** chain
`SKILL.md → a.md → b.md` — Claude often only *previews* (e.g. `head -100`) nested files
and gets incomplete information. For this project: `SKILL.md` links to each companion-tool
file and each example file directly; companion files do not link to each other.

## Directory Conventions

```
first-principles-thinking/
├── SKILL.md          # Required. Methodology + output format + rubric + navigation map.
├── references/       # Knowledge loaded on demand. Companion tools, deep guides.
│   ├── five-whys.md
│   ├── pre-mortem.md
│   ├── trade-off-analysis.md
│   └── validation-rubric.md   # if too long to keep inline
├── examples/         # Worked examples showing the methodology applied end-to-end.
│   ├── software-microservices-review.md
│   ├── product-business.md
│   ├── personal-general.md
│   └── science-engineering.md
└── LICENSE           # MIT, matching the source repo
```

| Directory | Per the open standard, holds | This project's use |
|-----------|------------------------------|--------------------|
| `references/` | "Additional documentation agents read when needed" — technical reference, domain files | Companion thinking tools (5-Whys, pre-mortem, trade-off) and any long-form rubric. |
| `examples/` | (Not a named spec directory, but a documented convention — `examples.md` / `examples/`) | Worked first-principles analyses across the four target domains. |
| `scripts/` | Executable code | **Do not create.** v1 is pure-Markdown; an empty `scripts/` would be misleading. |
| `assets/` | Static resources — templates, images, data files | Not needed. A Markdown output template lives inline in `SKILL.md` or as a `references/` file, not as an `asset`. |

## Versioning Conventions

There is **no first-class `version` frontmatter field** in either the open standard or
Claude Code's frontmatter reference (verified — HIGH confidence). Options:

| Approach | Verdict |
|----------|---------|
| `metadata: { version: "2.0" }` in frontmatter | **Recommended.** `metadata` is the spec-sanctioned home for arbitrary keys; Anthropic's own examples use exactly `version: "1.0"` there. Quote the value so YAML treats it as a string. |
| Git tags (e.g. `v2.0.0`) on the repo | **Recommended, in addition.** The skill ships as a git repo; tags are the real release record. |
| A top-level `version:` frontmatter key | Avoid — not in the schema; some validators/clients may ignore or flag it. |

Use **semantic versioning** semantics informally: this milestone (enhanced single skill)
is a **2.0** relative to the original 1.x. When updating an installed skill, the
`skill-creator` guidance is explicit: **keep the same `name` and directory name** — never
rename to `first-principles-thinking-v2`.

## Validation

| Layer | Tool | What it catches |
|-------|------|-----------------|
| Schema/convention | `skills-ref validate ./first-principles-thinking` | Invalid `name`/`description`, naming-convention violations, name≠dirname. The official validator for the open standard. |
| Markdown style | `markdownlint-cli2` (optional) | Inconsistent headings, missing code-fence languages, structural issues across `SKILL.md` + references + examples. |
| Behavioral | Live testing in Claude Code (`/doctor`, real prompts) | Whether the skill *triggers*, whether the description is being truncated, whether Claude follows references. There is **no automated behavioral validator** — Anthropic's recommended method is eval-driven iteration (test with vs without the skill). |
| Domain rubric | The skill's own Markdown validation rubric | Project-specific: the self-check the model applies to verify an analysis followed first-principles rigor. This is a *skill feature*, not authoring tooling. |

**Recommended `.markdownlint.jsonc` for this pure-Markdown repo:**

```jsonc
{
  "default": true,
  "MD013": false,   // line length — off; skill prose has long lines by design
  "MD033": false,   // allow inline HTML (<details> for "old patterns" sections)
  "MD041": true,    // first line must be a top-level heading
  "MD040": true,    // fenced code blocks must declare a language
  "MD003": { "style": "atx" }  // consistent "# " headings
}
```

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|--------------------------|
| Author to the Agent Skills **open standard** schema | Author to Claude-Code-only frontmatter | Only if the skill will *never* be used outside Claude Code. The open standard is a strict subset for required fields, so authoring to it costs nothing and keeps the skill portable (Cursor, Copilot, Gemini CLI, etc.). |
| `metadata.version` for versioning | Top-level `version:` key | Never — not in the schema. |
| Personal skill install (`~/.claude/skills/`) | Project skill (`.claude/skills/`) | When a team wants the skill version-controlled inside a specific repo. |
| Copy/symlink install | Plugin packaging / `.skill` bundle | Plugin/`.skill` distribution suits a *collection* or marketplace publishing — explicitly milestone 2/3, out of scope for v1. |
| `skills-ref` for validation | `claude` CLI | There is no `claude skill validate` command; `/doctor` only diagnoses description-budget issues, not schema correctness. |
| Plain CommonMark Markdown | Heavy MDX / custom components | The body has "no format restrictions" but must be readable by the model and by humans on GitHub — keep it plain. |

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| `scripts/` directory or any executable code | Violates the v1 pure-Markdown constraint; an empty/placeholder `scripts/` misleads readers | Express the validation rubric as a Markdown checklist the model applies |
| `disable-model-invocation: true` | Stops Claude from auto-loading the skill when a problem calls for first-principles reasoning — defeats the purpose | Default (`false`): both `/`-invocation and automatic triggering |
| `context: fork` | Runs the skill in an isolated subagent with no conversation history; a methodology must reason about *the current* discussion | Default inline execution |
| Top-level `version:` frontmatter key | Not in the open standard or Claude Code schema; may be ignored or flagged | `metadata: { version: "2.0" }` + git tags |
| Vague `description` (`"Helps with thinking"`) | #1 cause of a skill never triggering | Specific what+when description with literal trigger keywords |
| First-person description (`"I help you..."`) | Injected into the system prompt; inconsistent POV harms discovery | Third person (`"Decomposes problems into..."`) |
| Deeply nested references (`SKILL.md → a.md → b.md`) | Claude previews nested files with partial reads → incomplete info | All references one level deep, linked directly from `SKILL.md` |
| Windows-style backslash paths in references | Break on Unix; skills are cross-platform | Forward slashes always (`references/five-whys.md`) |
| Reserved words `anthropic` / `claude` in `name` | Rejected by Claude Code's `name` validation | A descriptive gerund/noun-phrase name |
| Time-sensitive content ("after August 2025, use...") | Becomes wrong; bloats the skill | A `<details>`-wrapped "old patterns" section, or omit entirely |
| `SKILL.md` over ~500 lines | Recurring token cost every turn once loaded; degrades performance | Split into `references/` files, leave a navigation map in `SKILL.md` |

## Stack Patterns by Variant

**If the skill stays a single skill (v1 — this milestone):**
- Single directory, install by copy/symlink into `~/.claude/skills/`.
- Companion tools (5-Whys, pre-mortem, trade-off) are `references/` files, not separate skills.
- No plugin manifest, no marketplace metadata.

**If it later becomes a collection (milestone 2):**
- Each skill is its own directory; consider a Claude Code **plugin** (`<plugin>/skills/<name>/`) to distribute them together with a `plugin-name:skill-name` namespace.
- `skillListingBudgetFraction` may need raising if many skills crowd the description budget.

**If a programmatic builder is added (milestone 3):**
- The `uv` Python scaffold becomes relevant; it could generate `SKILL.md` + reference files.
- Adopt `skills-ref validate` as a CI gate on generated output.

## Version Compatibility

| Component | Compatible With | Notes |
|-----------|-----------------|-------|
| Agent Skills open standard | Claude Code, Claude.ai, Cursor, Copilot, Gemini CLI, OpenCode, Goose, and more | A skill authored to the open-standard required schema is portable across all listed clients. |
| Claude Code frontmatter extensions | Claude Code only | Optional fields like `when_to_use`, `disable-model-invocation`, `context` are read by Claude Code; other clients ignore them. Keeping them unused maximizes portability. |
| `skills-ref validate` | Open standard | Validates the standard's schema; will not check Claude-Code-specific fields. |
| Markdown body | Universal | No format restrictions; plain CommonMark renders correctly in Claude Code, on GitHub, and in every skills-compatible client. |

## Sources

- [Extend Claude with skills — Claude Code Docs](https://code.claude.com/docs/en/skills) — full frontmatter reference, skill locations, invocation control, `<500 line` budget, live change detection, `/doctor`, 1,536-char listing cap. **HIGH confidence (official, current).**
- [Skill authoring best practices — Claude Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) — description writing (third person, what+when), progressive disclosure patterns, one-level-deep references, 500-line budget, ~5,000-token guidance, anti-patterns, evaluation-driven development. **HIGH confidence (official, current).**
- [Agent Skills Specification — agentskills.io](https://agentskills.io/specification) — the open-standard schema: required `name`/`description` with exact constraints, optional `license`/`compatibility`/`metadata`/`allowed-tools`, directory conventions (`scripts/`, `references/`, `assets/`), `skills-ref validate` tooling. **HIGH confidence (authoritative open standard).**
- [Agent Skills Overview — agentskills.io](https://agentskills.io) — three-stage progressive disclosure, cross-client adoption list. **HIGH confidence.**
- [anthropics/skills — skill-creator/SKILL.md](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) — Anthropic's meta-skill: "pushy" descriptions, packaging, preserve-name-on-update rule, metadata.version example. **HIGH confidence (official Anthropic repo).**
- [DavidAnson/markdownlint](https://github.com/DavidAnson/markdownlint) and [markdownlint Rules](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md) — Markdown linting rules and config (MD013, MD003, MD040, MD041, MD033). **MEDIUM confidence (current, not skill-specific — generic Markdown tooling).**

---
*Stack research for: pure-Markdown Claude Code skill authoring*
*Researched: 2026-05-16*
