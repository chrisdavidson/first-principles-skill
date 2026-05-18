# Phase 6: Final SKILL.md Wiring, README, and Validation - Pattern Map

**Mapped:** 2026-05-18
**Files analyzed:** 4 (1 modify, 2 create, 1 optional create)
**Analogs found:** 3 / 4 (`.markdownlint.jsonc` has no meaningful analog — config file)

---

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `first-principles-thinking/SKILL.md` | Layer-2 always-on methodology body + nav index | request-response (loaded on trigger → model reads nav map and follows links to Layer 3) | `first-principles-thinking/SKILL.md` itself (current state) | exact — restructuring in place |
| `README.md` | human-facing documentation (repo front door) | none — static document | `CLAUDE.md` (repo root long-form Markdown) | partial-match — similar document length and structure conventions; different audience |
| `.markdownlint.jsonc` | dev config file | none — consumed by linting tool | none in this repo | no analog |
| `dev/check-links.sh` (optional) | host-side validation utility | batch (scan files → assert targets exist) | none in this repo | no analog — throwaway script; RESEARCH.md Pattern 2 provides the exact implementation |

---

## Pattern Assignments

### `first-principles-thinking/SKILL.md` (Layer-2 nav restructure, D-07/D-08/D-09)

**Analog:** The file itself — this is an in-place restructure, not a new file. The patterns to preserve are derived from how the current file is structured; the patterns to apply are defined in RESEARCH.md Pattern 1.

**What changes:** The two terminal sections `## Companion thinking tools` and `## Worked examples` (lines 161–177) are replaced with a single consolidated `## Skill files` section with three subsections. The inline functional links at lines 144 and 151 remain in place (D-09).

**Existing sections to preserve** (lines 1–159 — do not touch):

- Frontmatter block (lines 1–16): `name`, `description`, `license`, `metadata.version` — no changes.
- All five phase sections (`### Phase 1` through `### Phase 5`) — locked from Phases 1–4.
- `## Output format` section (lines 117–144) — locked; keep inline link to `references/output-template.md` at line 144.
- `## Before presenting conclusions` section (lines 148–158) — locked; keep inline link to `references/validation-rubric.md` at lines 151–152.

**Section divider pattern** (throughout current SKILL.md):
```markdown
---

### Phase N: [Name]
```
Use `---` between every major section. This is the established rhythm.

**Current nav sections to replace** (lines 160–177):
```markdown
## Companion thinking tools

Reach for a companion tool when the analysis needs it:

- **Stuck on why something is true** → [references/five-whys.md](references/five-whys.md) — root-cause drill-down procedure
- **Stress-testing a proposed solution** → [references/pre-mortem.md](references/pre-mortem.md) — prospective-hindsight failure analysis
- **Choosing between viable options** → [references/trade-off-analysis.md](references/trade-off-analysis.md) — weighted trade-off procedure

## Worked examples

Match the domain, then read the relevant example to calibrate format and rigor:

- Software and systems → [examples/software-systems.md](examples/software-systems.md)
- Product and business → [examples/product-business.md](examples/product-business.md)
- Personal and general → [examples/personal-general.md](examples/personal-general.md)
- Science and engineering → [examples/science-engineering.md](examples/science-engineering.md)
```

**Target structure (D-07/D-08)** — copy this directly from RESEARCH.md Pattern 1:
```markdown
## Skill files

### Companion tools

**[Five Whys](references/five-whys.md)** — Root-cause drill-down procedure. Use when an
analysis is stuck on *why* something is true and the surface explanation feels insufficient.
The tool branches causal chains iteratively until a root cause passes a testability check,
then hands back to Phase 3 (Establish Ground Truths) with a verified causal fact.

**[Pre-mortem](references/pre-mortem.md)** — Prospective-hindsight failure analysis. Use
during Phase 5 (Validate) to stress-test a proposed solution by imagining it has already
failed and working backward to find the failure modes. Findings surface as weak-link flags
or confidence caveats in the signed-off analysis.

**[Trade-off Analysis](references/trade-off-analysis.md)** — Weighted-criteria decision
procedure. Use during Phase 4 (Reason Upward) when multiple viable options remain after
ground truths are established. Criteria are weighted before scoring to prevent
post-hoc rationalization, and the result feeds back as a derivation chain step.

### Worked examples

- Software and systems → [examples/software-systems.md](examples/software-systems.md)
- Product and business → [examples/product-business.md](examples/product-business.md)
- Personal and general → [examples/personal-general.md](examples/personal-general.md)
- Science and engineering → [examples/science-engineering.md](examples/science-engineering.md)

### Reference docs

- Output format template → [references/output-template.md](references/output-template.md)
- Validation rubric → [references/validation-rubric.md](references/validation-rubric.md)
```

**Companion tool blurb pattern (D-08):** Each blurb follows the schema: `**[Link Text](path)** — [one-line role]. [When-to-use sentence naming the relevant phase.] [How-it-hands-back sentence naming the artifact and destination phase.]` The blurb starts bold-linked, uses an em-dash after the link, and spans 2–3 sentences. No H3 or H4 nested under the companion tool name — bold link inline is the established style from `references/validation-rubric.md` and `references/five-whys.md` header patterns.

**MD040 fix — line 136:** The derivation chain format block at line 136 currently has no language specifier. Add `text`:
```markdown
Before (line 136):
```
GT-N + GT-M → [intermediate claim] → [conclusion]
```

After:
```text
GT-N + GT-M → [intermediate claim] → [conclusion]
```
```

**Line budget:** Current file is 177 lines. The replacement adds approximately 15 net lines (three 3-sentence blurbs replacing three 1-line bullets, plus a new subsection heading and "Reference docs" subsection). Projected total ≈ 192 lines — well within the 500-line budget.

**Forward-slash paths:** All 9 link paths in the consolidated map must use forward slashes (e.g., `references/five-whys.md`, not `references\five-whys.md`). The current file already uses forward slashes — maintain this.

---

### `README.md` (human-facing documentation, create from scratch)

**Analog:** `CLAUDE.md` — the closest long-form Markdown document in this repo. It serves a different audience (contributor/dev rather than user), but establishes structural conventions: H2 top-level sections, H3 sub-sections for details, tables for structured reference data, code blocks for shell commands, and a tone that is direct and precise without being academic.

**CLAUDE.md structure conventions to carry over** (from reading CLAUDE.md):

```markdown
## Section Heading     ← H2 for top-level sections
### Sub-section        ← H3 when a section has distinct sub-topics
| Col | Col |          ← tables for structured reference (e.g., install scope options)
```bash               ← fenced code with `bash` language for shell commands
```

**README-specific structure (D-01 to D-03, D-10/D-11):**

The file opens with an H1 title matching the skill's human name. Sections in order:

1. **Opening pitch** (2–4 sentences under H1, no heading): What the skill is and what problem it solves. Must include the words "first principles" and "Claude Code" for discoverability.

2. **`## When to use it`** (or equivalent heading at Claude's discretion): Trigger situations in bullet-list form — match the concrete trigger phrases from the `description` frontmatter field (challenge assumptions, is this the right approach, why are we doing this, evaluate an architectural decision, etc.). Not a prose restatement of the methodology.

3. **`## The methodology`** (or equivalent): Readable prose summary of the 5-phase methodology with phase names and what each produces. Per D-02, this section ends with an explicit pointer to `first-principles-thinking/SKILL.md` as the authoritative spec. Must NOT re-specify the methodology in full — summarize, then defer.

4. **`## Companion tools`** (or equivalent): Three tools named, one sentence each on what each is for. Link to `first-principles-thinking/references/five-whys.md`, `pre-mortem.md`, `trade-off-analysis.md`. Not a duplicate of the SKILL.md blurbs — just a named list.

5. **`## Worked examples`** (or equivalent): Four examples listed by domain with links to `first-principles-thinking/examples/`. One sentence each describing the scenario.

6. **`## Relationship to the original`** (D-03 — exact section required): Names the fork lineage (`github.com/chrisdavidson/first-principles-skill`, MIT, same author) and what v2.0 adds over the original: validation rubric, three companion tools, four domain-spread worked examples, sharpened 5-phase methodology with entry/exit criteria and named artifacts. Must be concrete, not vague — this is the project's premise.

7. **`## Installation`** (D-10): Both install modes (`cp` copy and `ln -s` symlink), both scopes (personal `~/.claude/skills/` and project `.claude/skills/`), personal marked as recommended default. Must call out that the installed directory must be named `first-principles-thinking`. Concrete shell commands with bash code blocks.

**Installation section shell command pattern** (from CLAUDE.md §Installation conventions and D-10):
```bash
# Personal install (recommended) — available across all your projects
git clone https://github.com/chrisdavidson/first-principles-skills.git
cp -r first-principles-skills/first-principles-thinking ~/.claude/skills/first-principles-thinking

# Or symlink (keeps repo as live source of truth — edits picked up without re-copying):
ln -s /path/to/first-principles-skills/first-principles-thinking ~/.claude/skills/first-principles-thinking

# Project install — scoped to one repo, committed to VCS
cp -r first-principles-skills/first-principles-thinking /path/to/your-project/.claude/skills/first-principles-thinking
```

Key constraint: the installed directory **must be named `first-principles-thinking`** — it must match the frontmatter `name` field.

**Tone pattern** (from `CLAUDE.md` prose sections): Direct declarative sentences. No hedging ("might," "could"). Descriptions name what something does, not how the author feels about it. The "Relationship to the original" section is factual and concrete — it lists additions, not emotional marketing language.

**No contributing or dev-tooling section** (D-11): `skills-ref`, `markdownlint`, and dev workflow stay in `CLAUDE.md`. README ends after Installation.

**MD041 compliance:** The very first line of README.md must be the H1 title. No blank line, no preamble before `# First Principles Thinking`.

---

### `.markdownlint.jsonc` (dev config, create at repo root)

**No analog in this repo.** This is a configuration file type new to the project.

**Pattern:** Copy directly from RESEARCH.md Pattern 3 (verified against current skill files during research):

```jsonc
{
  "default": false,
  "MD003": true,
  "MD040": true,
  "MD041": true
}
```

**Notes:**
- `"default": false` means only the explicitly listed rules are enabled.
- `MD013` (line length) is intentionally omitted — CLAUDE.md prescribes it off.
- `MD033` (inline HTML) is intentionally omitted — no HTML in skill files.
- The file extension is `.jsonc` (JSON with Comments). The content above has no actual comments but the extension is conventional for markdownlint config and allows future annotation.
- Placement: repo root (same level as `README.md`, `CLAUDE.md`, `first-principles-thinking/`).

**Invocation command** (not in the config file itself, but needed for the plan's validation task):
```bash
npx markdownlint-cli2 "first-principles-thinking/**/*.md" --config .markdownlint.jsonc
```

---

### `dev/check-links.sh` (optional host-side utility)

**No meaningful analog in this repo.** This is a discretionary throwaway script.

**Pattern:** Copy directly from RESEARCH.md Pattern 2 (verified working against this repo during research):

```bash
#!/usr/bin/env bash
# Host-side link-resolution check for first-principles-thinking skill.
# Run from repo root. NOT part of the skill — pure dev tooling.
SKILL_DIR="./first-principles-thinking"
cd "$SKILL_DIR" || exit 1
BROKEN=0
while IFS=: read -r source_file link_target; do
  src_dir=$(dirname "$source_file")
  resolved="$src_dir/$link_target"
  if [ ! -f "$resolved" ]; then
    echo "BROKEN: $source_file -> $link_target"
    BROKEN=$((BROKEN+1))
  fi
done < <(grep -oP '\[.*?\]\(\K[^)#]+' SKILL.md references/*.md examples/*.md | grep -v '^http')
[ "$BROKEN" -eq 0 ] && echo "All links resolve OK" || echo "$BROKEN broken link(s)"
```

**Decision:** Whether to commit this file is at Claude's discretion (CONTEXT.md §Discretion). If committed, place at `dev/check-links.sh` with execute permission (`chmod +x`). If run ad-hoc only, do not create the file — run the inline commands directly in bash. Either choice is valid. The script must NOT be placed inside `first-principles-thinking/` — that would violate the pure-Markdown v1 constraint.

---

## MD040 Fixes (prerequisite for `markdownlint` gate)

Five fenced code blocks across skill files currently lack language specifiers. These must be fixed before the markdownlint gate can pass. They are not a new-file concern — they are fixes to existing files.

| File | Line | Current | Fix |
|------|------|---------|-----|
| `first-principles-thinking/SKILL.md` | 136 | ` ``` ` (no lang) | ` ```text ` |
| `first-principles-thinking/references/output-template.md` | 99 | ` ``` ` (no lang) | ` ```text ` or ` ```markdown ` |
| `first-principles-thinking/references/validation-rubric.md` | 95 | ` ``` ` (no lang) | ` ```text ` or ` ```markdown ` |
| `first-principles-thinking/references/validation-rubric.md` | 108 | ` ``` ` (no lang) | ` ```text ` or ` ```markdown ` |
| `first-principles-thinking/examples/software-systems.md` | 162 | ` ``` ` (no lang) | ` ```text ` |

**Constraint:** Do NOT add YAML frontmatter to any of these files when fixing them. The fix is only adding a language specifier to the opening fence of the code block — nothing else changes (Phase 2 D-08).

---

## Shared Patterns

### Markdown heading conventions
**Source:** `first-principles-thinking/SKILL.md` throughout; `first-principles-thinking/references/validation-rubric.md` throughout
**Apply to:** Both `SKILL.md` (restructured sections) and `README.md`
- H1 (`#`) for document title — appears exactly once, as the first line of the file (MD041)
- H2 (`##`) for top-level sections
- H3 (`###`) for subsections within a top-level section
- No H4 or deeper in files under ~200 lines

### Section dividers
**Source:** `first-principles-thinking/SKILL.md` (between every H2/H3 section); `first-principles-thinking/references/five-whys.md` (between every H2)
**Apply to:** SKILL.md restructured sections only (README does not use `---` dividers — standard GitHub README convention omits them)
```markdown
---

## Next Section
```

### Forward-slash relative paths in links
**Source:** `first-principles-thinking/SKILL.md` lines 144, 151–152, 165–167, 171–176 — every internal link uses forward slashes
**Apply to:** All links in both SKILL.md and README.md — never backslashes.

### Fenced code block language specifiers
**Source:** `first-principles-thinking/SKILL.md` line 127 (` ```markdown `), RESEARCH.md §Code Examples
**Apply to:** Every fenced block in every file touched in this phase. Use:
- `bash` for shell commands
- `text` for format-string examples and placeholder content
- `markdown` for Markdown syntax examples
- `jsonc` for the `.markdownlint.jsonc` content in README documentation

### No YAML frontmatter on Layer-3 files
**Source:** `first-principles-thinking/references/output-template.md` line 1; `first-principles-thinking/references/validation-rubric.md` line 1; `first-principles-thinking/references/five-whys.md` line 1
**Apply to:** All MD040 fix targets — do not add frontmatter when fixing code fences.

---

## No Analog Found

| File | Role | Reason |
|------|------|--------|
| `.markdownlint.jsonc` | dev config | No linting config files exist in this repo. Pattern is fully specified in RESEARCH.md Pattern 3 — copy directly. |
| `dev/check-links.sh` | optional host-side script | No shell scripts exist in this repo. Pattern is fully specified in RESEARCH.md Pattern 2 — copy directly. No analog search needed. |

---

## Metadata

**Analog search scope:** `first-principles-thinking/` (all Markdown files), `CLAUDE.md`, `.planning/phases/` (prior PATTERNS.md files for format conventions)
**Files scanned:** 11 (`SKILL.md`, `references/` ×5, `examples/` ×4, `CLAUDE.md`, prior `04-PATTERNS.md` for format reference)
**Pattern extraction date:** 2026-05-18
