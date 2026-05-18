# Phase 6: Final SKILL.md Wiring, README, and Validation - Research

**Researched:** 2026-05-18
**Domain:** Agent Skills authoring finalization — nav-map restructure, README authoring, schema validation tooling
**Confidence:** HIGH

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**README depth & audience**
- D-01: `README.md` is comprehensive — covers what the skill is, the 5-phase methodology summary, companion tools, worked-examples list, when to use it, fork lineage, and installation.
- D-02: README summarizes methodology in readable prose, then explicitly points to `SKILL.md` and `first-principles-thinking/references/output-template.md` as authoritative/canonical spec. No drift between README and SKILL.md.
- D-03: README has a dedicated "Relationship to the original" section (fork of `github.com/chrisdavidson/first-principles-skill`, MIT, same author). Names what v2.0 adds: validation rubric, three companion tools (5-Whys, pre-mortem, trade-off), four domain-spread worked examples, sharpened 5-phase methodology with entry/exit criteria and named artifacts.

**Schema validation gate**
- D-04: "Passes Agent Skills schema validation" = install `skills-ref` and run `agentskills validate ./first-principles-thinking`, capture pass output as evidence. Contingency: if install fails, flag task `autonomous: false` and document manual conformance check as fallback — do NOT silently pass.
- D-05: PKG-02 verified by one-time host-side link-resolution check — grep/script extracts every relative Markdown link and asserts each target exists. NOT bundled into the skill.
- D-06: Repo-wide `markdownlint` pass using CLAUDE.md-recommended config: MD013 off; MD003/MD040/MD041 on. Host-side tooling only, not bundled.

**SKILL.md wiring scope**
- D-07: Nav map restructured into single consolidated "Skill files" section with grouped subsections: Companion tools, Worked examples, Reference docs.
- D-08: Each companion tool expanded to 2-3 sentence blurb (what it does, when to reach for it, how it hands back to the 5-phase spine).
- D-09: Inline links to `references/output-template.md` and `references/validation-rubric.md` kept at functional body locations AND also listed in the consolidated map. Minor duplication intentional.

**README install coverage**
- D-10: Documents both `cp` and `ln -s` installation into personal (`~/.claude/skills/`) and project (`.claude/skills/`) scopes. Must call out that installed directory must be named `first-principles-thinking`. Personal scope is recommended default.
- D-11: README is user-facing only. Dev/validation tooling (`skills-ref`, `markdownlint`) stays in CLAUDE.md — no contributing section in README.

### Claude's Discretion
- Exact prose wording of all README sections.
- Exact heading text for the consolidated "Skill files" section and ordering of its three subsections.
- Implementation of the one-time link-resolution check (bash/grep/node) and where it lives (throwaway host-side tooling; committing to repo is acceptable but optional).
- Whether `skills-ref` is installed via npm or by cloning the `agentskills` repo — follow that repo's current install instructions.
- Concrete shell command snippets in the README install section.
- Wording of the methodology summary in the README (prose form, links to canonical).

### Deferred Ideas (OUT OF SCOPE)
None — discussion stayed within phase scope. v2 requirements (META-01/02/03) and milestones 2-3 remain out of scope.
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| FOUND-04 | Every `references/` and `examples/` file links one level deep directly from `SKILL.md` | Current SKILL.md links all 9 files; D-07 restructures how they appear — confirmed already wired. |
| FOUND-05 | The skill installs by copy or symlink into a Claude Code skills directory with no build step | README D-10 documents both install modes; skill directory is pure Markdown, no build step. |
| TOOL-04 | `SKILL.md` briefly describes each companion tool, says when to reach for it, and links to its reference file | D-08: companion tools get 2-3 sentence blurbs replacing the current one-liner entries. |
| PKG-01 | `README.md` describes the skill, its methodology, and installation for human readers | D-01/D-02/D-03/D-10: comprehensive README written from scratch. |
| PKG-02 | All cross-references between `SKILL.md`, `references/`, and `examples/` resolve correctly | D-05: host-side link-resolution check. All 9 links already verified to resolve. |
| PKG-03 | The skill passes Agent Skills schema validation | D-04: `agentskills validate ./first-principles-thinking`. Already passes — confirmed during research. |
</phase_requirements>

---

## Summary

Phase 6 is a finalization phase, not construction. Phases 1-5 have produced all 9 Layer-3 files and the SKILL.md body (176 lines, well within the 500-line budget). The skill already passes Agent Skills schema validation (`agentskills validate` returns "Valid skill"). All 9 cross-references already resolve. The structural work remaining is: (1) restructure the SKILL.md nav map into a consolidated "Skill files" section with 2-3 sentence companion-tool blurbs, (2) write a comprehensive human-facing README.md from scratch, and (3) run and clear three validation gates (schema, link-resolution, markdownlint).

The most important operational finding from research is the correct install method for `skills-ref`. The PyPI package installs via `uv tool install skills-ref` and exposes the binary as `agentskills`, not `skills-ref`. The CLAUDE.md references "skills-ref validate" as the command, but the actual installed binary is `agentskills validate`. This distinction must be correct in the plan's task commands. The package is already installed on this machine and the current skill passes validation.

The second critical finding is that the CLAUDE.md-recommended markdownlint config (MD003/MD040/MD041 on, MD013 off) currently produces 5 MD040 failures — five fenced code blocks without language specifiers, spread across SKILL.md, references/output-template.md, references/validation-rubric.md, and examples/software-systems.md. The markdownlint pass is not already clean; fixing these 5 blocks is an explicit task.

**Primary recommendation:** Install `markdownlint-cli2` via `npm install -g markdownlint-cli2` (or npx), fix the 5 MD040 code-fence violations, confirm the markdownlint pass is clean, and gate the phase close on all three validators reporting green.

---

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| SKILL.md nav map restructure | Skill content (Layer 2) | — | SKILL.md body is the always-on layer; the nav map is its index into Layer 3 files |
| Companion tool blurbs (D-08) | Skill content (Layer 2) | — | Inline in SKILL.md body, not in references/ |
| Inline functional links (D-09) | Skill content (Layer 2) | — | Links at functional locations remain in SKILL.md body |
| README.md | Repo root (human-facing) | — | Not part of the skill package; consumed by GitHub readers, not the AI client |
| Schema validation (`agentskills validate`) | Host-side tooling | — | Validates frontmatter; output is evidence, not bundled into skill |
| Link-resolution check (D-05) | Host-side tooling | — | Throwaway bash/grep; NOT committed to skill |
| Markdownlint pass (D-06) | Host-side tooling | — | Host dev tool; NOT committed to skill |

---

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| `skills-ref` (PyPI) | 0.1.1 | Agent Skills schema validator — `agentskills validate` | Authoritative validator named in CLAUDE.md and the agentskills.io spec [VERIFIED: PyPI registry, agentskills/agentskills repo] |
| `markdownlint-cli2` (npm) | 0.22.1 | Markdown linting with configurable rules | CLAUDE.md-recommended; fast, flexible, supports jsonc config files [VERIFIED: npm registry] |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `uv` (already installed) | 0.11.11 | Install `skills-ref` on this externally-managed system | Use instead of raw `pip install` — avoids externally-managed-environment error |
| bash + grep | builtin | Link-resolution check (D-05) | One-time throwaway verification; no install needed |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| `uv tool install skills-ref` | `pip install skills-ref --break-system-packages` | uv is cleaner on Debian-managed Python; avoids polluting system Python |
| `npx markdownlint-cli2` | `npm install -g markdownlint-cli2` | npx avoids a global install but re-downloads each run; global is faster for repeated use |

**Installation:**
```bash
# skills-ref (already installed on this machine via uv tool install)
uv tool install skills-ref

# markdownlint-cli2 (not yet installed — use npx or global install)
npm install -g markdownlint-cli2
# OR: use npx markdownlint-cli2 <args> with no install
```

---

## Package Legitimacy Audit

| Package | Registry | Age | Downloads | Source Repo | slopcheck | Disposition |
|---------|----------|-----|-----------|-------------|-----------|-------------|
| `skills-ref` | PyPI | Released Jan 2026 | N/A (new) | github.com/agentskills/agentskills | [OK] | Approved — confirmed as the official agentskills validator [VERIFIED: PyPI registry + official repo] |
| `markdownlint-cli2` | npm | Created Jul 2020 | ~226 KB unpacked, widely used | github.com/DavidAnson/markdownlint-cli2 | N/A (npm, not PyPI — slopcheck tested wrong registry) | Approved — 5+ year track record, official DavidAnson repo [VERIFIED: npm registry] |

**Packages removed due to slopcheck [SLOP] verdict:** none

**Packages flagged as suspicious [SUS]:** none

**Note on npm `skills-ref`:** There is a separate npm package also called `skills-ref` (v0.1.5, published December 2025, no source repository, different maintainer). This npm package is NOT the agentskills/agentskills validator. The correct package is the PyPI `skills-ref`. The npm package should not be used. [VERIFIED: npm registry investigation]

---

## Architecture Patterns

### System Architecture Diagram

```
Phase 6 work flow:

SKILL.md (Layer 2)             README.md (repo root)
   │                                │
   │ D-07: restructure nav map      │ D-01/02/03/10: write from scratch
   │ D-08: expand companion blurbs  │
   │ D-09: keep inline links        │
   └──────┬────────────────────────┘
          │
          ▼
   Three validation gates (host-side only, not bundled into skill)
          │
          ├─── Gate 1: agentskills validate ./first-principles-thinking
          │    (schema check: name, description, dirname match)
          │
          ├─── Gate 2: bash link-resolution check
          │    (extract relative links → assert each target exists)
          │
          └─── Gate 3: markdownlint-cli2 pass
               (MD003/MD040/MD041 on, MD013 off)
               → 5 MD040 failures to fix before this gates green
```

### Recommended Project Structure

The skill directory structure is already complete. No new files added to the skill itself.

```
first-principles-thinking/         ← skill package (pure Markdown, no build step)
├── SKILL.md                       ← edit: restructure nav map (D-07/08/09)
├── references/
│   ├── output-template.md         ← no change
│   ├── validation-rubric.md       ← fix: add language to 2 fenced blocks (MD040)
│   ├── five-whys.md               ← no change
│   ├── pre-mortem.md              ← no change
│   └── trade-off-analysis.md      ← no change
└── examples/
    ├── software-systems.md        ← fix: add language to 1 fenced block (MD040)
    ├── product-business.md        ← no change
    ├── personal-general.md        ← no change
    └── science-engineering.md     ← no change

README.md                          ← create: comprehensive human-facing (D-01 to D-03, D-10/11)
```

### Pattern 1: Consolidated "Skill files" Navigation Section

**What:** A single `## Skill files` (or similar heading) in SKILL.md that groups all Layer-3 links into three subsections: Companion tools (with 2-3 sentence blurbs), Worked examples (one line per domain), and Reference docs. Replaces the current two-section split (Companion thinking tools / Worked examples) and resolves inline links being scattered.

**When to use:** Always — this is the mandatory D-07 restructure.

**Current structure (to replace):**

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

**Target structure (D-07/D-08):**

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

*Note: The inline functional links at the "Output format" and "Before presenting conclusions" sections are KEPT in addition to the map (D-09). The above is the nav section only.*

### Pattern 2: Host-Side Link Resolution Check

**What:** A bash one-liner that extracts all relative Markdown links from the skill files and verifies each target exists. Throwaway — can be run ad-hoc or committed to a dev script.

```bash
# Source: verified working against this repo (research step)
SKILL_DIR="./first-principles-thinking"
cd "$SKILL_DIR"
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

*All 9 current links already pass this check — confirmed during research.*

### Pattern 3: markdownlint Config (.markdownlint.jsonc)

**What:** Minimal config per CLAUDE.md recommendations. Place at repo root or pass with `--config`.

```jsonc
// Source: CLAUDE.md §"Development Tools" + verified against current skill files
{
  "default": false,
  "MD003": true,
  "MD040": true,
  "MD041": true
}
```

**Invocation:**
```bash
npx markdownlint-cli2 "first-principles-thinking/**/*.md" --config .markdownlint.jsonc
```

### Anti-Patterns to Avoid

- **Running `pip install skills-ref` directly:** Debian marks the system Python as externally managed. Use `uv tool install skills-ref` instead.
- **Using the npm `skills-ref` package:** A different package with no source repo. The correct package is PyPI `skills-ref`.
- **Calling `skills-ref validate`:** The PyPI `skills-ref` package installs the binary as `agentskills`, not `skills-ref`. The correct command is `agentskills validate <path>`.
- **Bundling the link-check script into the skill directory:** Violates the pure-Markdown v1 constraint (no executable code in the skill).
- **Adding frontmatter to Layer-3 files:** Phase 2 D-08 locked no YAML frontmatter on references/ and examples/ files — do not add frontmatter when fixing MD040 issues.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Agent Skills schema validation | Manual frontmatter inspection | `agentskills validate` | Tests name constraints, description non-empty, dirname match — edge cases invisible to visual inspection |
| Markdown linting | Read-and-check by eye | `markdownlint-cli2` | 40+ rules, rule interdependencies; manual review misses subtle issues |
| Link resolution | Mental model of file structure | bash grep check | Files can be renamed independently; only a programmatic check catches drift |

---

## Common Pitfalls

### Pitfall 1: Wrong Binary Name for skills-ref

**What goes wrong:** Plan tasks call `skills-ref validate` but the command is not found.

**Why it happens:** The PyPI package name is `skills-ref` but the installed binary is `agentskills`. The CLAUDE.md documentation says "skills-ref validate" — this is the conceptual command name from before the binary was renamed.

**How to avoid:** Always use `agentskills validate <path>` in task shell commands.

**Warning signs:** `command not found: skills-ref` after a successful `uv tool install skills-ref`.

### Pitfall 2: markdownlint MD040 Violations Already Exist

**What goes wrong:** Plan assumes `markdownlint` pass is a simple "run and confirm green." It produces 5 errors before any edits.

**Why it happens:** Five fenced code blocks in the existing skill files lack language specifiers. This was not caught during Phases 3-5 because markdownlint was not run until now.

**How to avoid:** Plan must include an explicit fix task for the 5 MD040 violations, separate from the "run markdownlint" task.

**The 5 violations (verified):**
- `SKILL.md:136` — the derivation chain format block (add language `text` or ``)
- `references/output-template.md:99` — one fenced block (add language specifier)
- `references/validation-rubric.md:95` — one fenced block
- `references/validation-rubric.md:108` — one fenced block
- `examples/software-systems.md:162` — one fenced block

### Pitfall 3: Externally-Managed Python Environment

**What goes wrong:** `pip install skills-ref` fails with "externally-managed-environment" error.

**Why it happens:** Debian/Ubuntu systems mark system Python as managed by apt. Direct pip installs are blocked.

**How to avoid:** Use `uv tool install skills-ref`. `uv` is already installed at `/usr/bin/uv` (v0.11.11). `skills-ref` is already installed via uv tool on this machine.

**Warning signs:** `error: externally-managed-environment` from pip.

### Pitfall 4: SKILL.md Line Budget Tracking

**What goes wrong:** Nav restructure expands SKILL.md beyond the 500-line budget.

**Why it happens:** D-08 companion-tool blurbs expand each from ~1 line to ~4-5 lines (three tools = +9-12 lines). Risk is low given current count is 176, but must be confirmed after edits.

**How to avoid:** After editing SKILL.md, run `wc -l first-principles-thinking/SKILL.md` before committing. Budget is 500 lines; current headroom is ~324 lines — no real risk, but verify.

### Pitfall 5: README Drift from SKILL.md

**What goes wrong:** README describes the methodology in prose that contradicts or omits a phase-level detail in SKILL.md.

**Why it happens:** Writing prose summaries of structured content produces paraphrasing drift.

**How to avoid:** D-02 mandates that README "summarizes… then explicitly points to SKILL.md as authoritative/canonical spec." After drafting README, do a single cross-reference read against SKILL.md. Any descriptive statement in README must be traceable to SKILL.md or a Layer-3 file.

---

## Code Examples

### agentskills validate — Pass and Fail Output

```bash
# Pass (exit 0):
$ agentskills validate ./first-principles-thinking
Valid skill: /path/to/first-principles-thinking

# Fail (exit 1):
$ agentskills validate ./bad-skill
Validation failed for /path/to/bad-skill:
  - Skill name 'Bad Skill' must be lowercase
  - Field 'description' must be a non-empty string
```
*Source: verified by running agentskills 0.1.1 against a test case during research.*

### markdownlint-cli2 with recommended config

```bash
# Create config at repo root:
# .markdownlint.jsonc
{
  "default": false,
  "MD003": true,
  "MD040": true,
  "MD041": true
}

# Run:
npx markdownlint-cli2 "first-principles-thinking/**/*.md" --config .markdownlint.jsonc

# Clean pass output:
# markdownlint-cli2 v0.22.1 (markdownlint v0.40.0)
# Finding: first-principles-thinking/**/*.md
# Linting: 10 file(s)
# Summary: 0 error(s)
```
*Source: verified against current skill files during research.*

### Fixing MD040 — Adding language specifier to fenced blocks

The derivation-chain format block in SKILL.md (line 136) uses a format string that is not any programming language. Use `text` as the language specifier:

```markdown
Before:
```
GT-N + GT-M → [intermediate claim] → [conclusion]
```

After:
```text
GT-N + GT-M → [intermediate claim] → [conclusion]
```
```

For fenced blocks containing template/placeholder content (as in output-template.md and validation-rubric.md), use `text` or `markdown` as appropriate.

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `skills-ref validate` binary name | `agentskills validate` binary name | PyPI 0.1.x (Jan 2026) | CLAUDE.md doc says "skills-ref validate" — actual command is `agentskills` |
| `pip install skills-ref` | `uv tool install skills-ref` on Debian | Debian managed-env policy | Direct pip blocked on this system; uv tool is the correct path |

---

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | The 5 MD040 violations are the only markdownlint failures with the recommended config (default:false, MD003/040/041 on) | Common Pitfalls §2 | Low — verified by running the exact config against all 10 skill files during research. If new violations appear, fix them in the same task. |
| A2 | `agentskills 0.1.1` validates the same schema rules as the agentskills.io specification (name constraints, description non-empty, dirname match) | Code Examples | Low — verified pass/fail behavior matches the spec's stated constraints. |

---

## Open Questions

1. **README heading conventions**
   - What we know: D-01 to D-03 define content sections; Claude has discretion on exact headings.
   - What's unclear: Whether to use a "Quick start" top-level section before methodology vs. a single "Installation" section after methodology.
   - Recommendation: Mirror GitHub README conventions — quick pitch + install visible above the fold, methodology detail below.

2. **Companion tool blurb tone**
   - What we know: D-08 requires 2-3 sentences: what it does, when to reach for it, how it hands back to the 5-phase spine.
   - What's unclear: Whether each blurb should begin with the tool name as bold or as a heading.
   - Recommendation: Bold name on a definition-list-style entry (as shown in the Pattern 1 code example above) — maintains visual consistency without adding heading nesting depth.

---

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| `agentskills` (uv tool) | D-04 schema validation | Already installed | 0.1.1 | Manual conformance check per D-04 contingency |
| `uv` | skills-ref install | Already installed | 0.11.11 | `pip install skills-ref --break-system-packages` (risky on Debian) |
| `npx` / `markdownlint-cli2` | D-06 markdownlint | `npx` available (node 22.22.2) | cli2 v0.22.1 | `npm install -g markdownlint-cli2` |
| `bash` + `grep` | D-05 link check | Available (system) | builtin | No fallback needed |
| Python 3 | skills-ref runtime | 3.11.14 | — | — |
| Node.js | npx/markdownlint | 22.22.2 | — | — |

**Missing dependencies with no fallback:** None.

**Missing dependencies with fallback:** None — all dependencies are available.

---

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | Three host-side gates (no unit test framework — pure Markdown skill) |
| Config file | `.markdownlint.jsonc` (create in Wave 0) |
| Quick run command | `agentskills validate ./first-principles-thinking` |
| Full suite command | `agentskills validate ./first-principles-thinking && npx markdownlint-cli2 "first-principles-thinking/**/*.md" --config .markdownlint.jsonc` |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| FOUND-04 | All 9 Layer-3 files linked one level deep from SKILL.md | Link resolution | bash link-check script | ❌ Wave 0 |
| FOUND-05 | Installs by copy/symlink, no build step | Manual verify | — (manual-only: no build artifact to check) | N/A |
| TOOL-04 | SKILL.md describes each companion tool with when+link | Schema + visual | `agentskills validate` + human review | — |
| PKG-01 | README.md covers skill, methodology, installation | Human review | — (manual-only: prose content) | ❌ Wave 0 |
| PKG-02 | All cross-references resolve | Link resolution | bash link-check script | ❌ Wave 0 |
| PKG-03 | Passes Agent Skills schema validation | Schema | `agentskills validate ./first-principles-thinking` | — |

### Sampling Rate
- **Per task commit:** `agentskills validate ./first-principles-thinking`
- **Per wave merge:** `agentskills validate ./first-principles-thinking && npx markdownlint-cli2 "first-principles-thinking/**/*.md" --config .markdownlint.jsonc`
- **Phase gate:** All three validators green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `.markdownlint.jsonc` — repo root config file; covers MD003/MD040/MD041 on, MD013 off
- [ ] `dev/check-links.sh` (optional) — committing the link-resolution script is discretionary per D-05

---

## Security Domain

No authentication, no user input, no network calls, no secrets. This phase edits Markdown files and runs local CLI validators. ASVS categories V2, V3, V4, V5, V6 do not apply.

---

## Sources

### Primary (HIGH confidence)
- CLAUDE.md §"Technology Stack", §"Validation", §"Development Tools", §"Installation", §"Where Skills Live" — authoritative authoring spec for this project
- `agentskills validate ./first-principles-thinking` — live validation run during research; confirmed pass output "Valid skill"
- `pip index versions skills-ref` — confirmed versions 0.1.0 and 0.1.1 available on PyPI [VERIFIED: PyPI registry]
- `npm view markdownlint-cli2` — confirmed version 0.22.1, npm since 2020 [VERIFIED: npm registry]
- `npx markdownlint-cli2 "first-principles-thinking/**/*.md"` — live run during research; confirmed 5 MD040 violations before fix
- `agentskills validate` failure-mode test — tested against a deliberately invalid skill during research; confirmed error message format

### Secondary (MEDIUM confidence)
- [agentskills/agentskills skills-ref README](https://github.com/agentskills/agentskills/tree/main/skills-ref) — install via `uv sync` or `pip install -e .` from clone; confirms PyPI package; binary is `agentskills` (fetched during research)
- [PyPI skills-ref 0.1.1](https://pypi.org/project/skills-ref/) — install command `pip install skills-ref`, release Jan 2026

### Tertiary (LOW confidence)
None.

---

## Metadata

**Confidence breakdown:**
- Validation tooling (skills-ref, markdownlint): HIGH — live runs verified on actual skill files
- SKILL.md nav restructure structure: HIGH — all 9 files confirmed present; current SKILL.md read in full
- README content requirements: HIGH — all locked from CONTEXT.md decisions
- MD040 violation locations: HIGH — verified by running exact config during research

**Research date:** 2026-05-18
**Valid until:** 2026-06-18 (stable tooling; PyPI/npm versions unlikely to change materially in 30 days)
