# Project Research Summary

**Project:** First Principles Thinking Skill (Enhanced)
**Domain:** Content-heavy pure-Markdown Claude Code skill (a structured reasoning/methodology skill)
**Researched:** 2026-05-16
**Confidence:** HIGH

## Executive Summary

This project is not a software build — it is an *information-architecture* exercise. A Claude Code skill in 2026 is a directory with one required file (`SKILL.md`) plus optional `references/` and `examples/`. There is no runtime, no dependency manifest, no build step. The "stack" is the Agent Skills open standard, CommonMark Markdown, and YAML frontmatter. Experts author skills around one principle — **progressive disclosure**: a tiny always-loaded metadata layer, a lean always-resident `SKILL.md` body (target under 500 lines), and on-demand `references/`/`examples/` files that cost zero tokens until Claude reads them. The v1 deliverable is the *enhanced* single skill, forked in spirit from the existing `first-principles-skill` repo, expanding four known gaps: more worked examples, a sharper 5-phase methodology, a Markdown validation rubric, and fully-built companion tools (5-Whys, pre-mortem, trade-off analysis).

The recommended approach is to author to the Agent Skills open-standard schema (`name` + `description` required), keep all Claude-Code-specific frontmatter fields unused for portability, and treat `SKILL.md` as a *table of contents* rather than a document. The methodology procedure and output format stay resident in `SKILL.md`; the rubric, the three companion tools, and four domain examples each become a separate file linked one level deep. Build order is dependency-driven and unambiguous: sharpen the 5-phase methodology and harden the output format first (everything calibrates against it), then build the rubric, companion tools, and examples — three streams that parallelize once the foundation is stable.

The dominant risk is not technical but *content-quality*: a methodology skill can fail in two opposite directions. Too abstract, and the 5 phases become inspiring labels that produce reasoning-by-analogy in disguise; too prescriptive, and Claude box-ticks a five-heading template where the headings are filled but no real reasoning happened. Both failures violate the project's Core Value ("reasoning a skeptic cannot dismiss as hand-waving"). The mitigation is to give each phase a concrete operation with a named artifact, keep one phase deliberately high-freedom, make the validation rubric falsifiable and evidence-quoting (test it against a deliberately weak analysis), and ensure each of the four examples exercises the method *differently* with a real false-assumption pivot. Secondary risks — `SKILL.md` bloat, a description that never triggers, and scope creep toward a skill collection or executable code — are all preventable with disciplined structure and the `uv` scaffold left untouched.

## Key Findings

### Recommended Stack

A pure-Markdown skill has no runtime libraries and no package to install to *build* it. The skill *is* a folder; "installation" means placing it where Claude Code discovers it (`~/.claude/skills/<name>/` for personal use — the primary target — or `.claude/skills/<name>/` for project scope). Author to the **Agent Skills open standard** required schema and the skill stays portable across Claude Code, Cursor, Copilot, and Gemini CLI. Versioning goes in `metadata: { version: "2.0" }` (there is no first-class `version` frontmatter key) plus git tags. The critical install rule: the skill *directory name* must equal the frontmatter `name` — so the directory is `first-principles-thinking`.

**Core technologies:**
- Agent Skills open standard (agentskills.io) — the skill *is* a `SKILL.md` + folder — the single authoritative, portable format
- Markdown (CommonMark) + YAML 1.2 frontmatter — `SKILL.md` body and all `references/`/`examples/` content — mandated by the format; only the frontmatter is schema-constrained
- `skills-ref validate` — official spec validator (schema + naming conventions) — run as a pre-ship gate; the closest thing to an official linter
- `markdownlint-cli2` (optional dev tool) — repo-wide Markdown consistency — disable `MD013` (line length), keep `MD003`/`MD040`/`MD041`

**Avoid:** a `scripts/` directory or any executable code (violates the pure-Markdown constraint), `disable-model-invocation: true` (kills auto-triggering), `context: fork` (loses the conversation the methodology must reason about), a top-level `version:` key, vague/first-person descriptions, and deeply nested references.

### Expected Features

The "features" of a methodology skill are content-and-structure properties, not runtime capabilities. The four PROJECT.md gaps map directly onto the differentiators below.

**Must have (table stakes):**
- Valid `SKILL.md` frontmatter — `name`, `description`, `metadata.version` — or the skill will not load
- Trigger-rich `description` — third person, "what it does + when to use it", explicit phrases, multilingual EN+ZH — the only thing pre-loaded for skill selection
- The 5-phase methodology as the spine, with a standardized output format/template — the skill's reason to exist
- Progressive disclosure — lean `SKILL.md`, all depth in `references/`/`examples/`, every reference one level deep
- Installable by copy/symlink, no time-sensitive content, consistent imperative voice and terminology

**Should have (competitive — these are the four v1 gaps):**
- Self-check validation rubric (Gap 3) — analytic (not holistic), ~6-8 falsifiable criteria, 3-4 discrete levels, gate scoring, applied as a validator->fix->repeat loop — the single biggest rigor multiplier
- Companion tool reference components (Gap 4) — 5-Whys, pre-mortem, trade-off analysis, each a self-contained `references/` file with when-to-use, procedure, mini-example, failure modes, and a named handoff back to the 5-phase spine
- Domain-spread worked examples (Gap 1) — exactly 4, one each for software/systems, product/business, personal/general, science/engineering — each showing the whole method including a dead-end
- Tightened 5-phase process with entry/exit criteria and explicit traceability (Gap 2) — fuzzy phase boundaries are where reasoning-by-analogy leaks in

**Defer (v1.x / v2+):**
- Self-application / dogfooding reference — cheap, add if v1 examples feel thin on meta-credibility
- Splitting into a collection of thinking skills — explicitly milestone 2
- Executable validation script — explicitly a later milestone; needs the rubric stable first
- Python skill-builder — explicitly milestone 3

### Architecture Approach

A skill is a *context-loading* system, organized in three layers: Layer 1 metadata (`name` + `description`, ~100 tokens, always loaded for skill selection); Layer 2 the `SKILL.md` body (loaded when the skill triggers, resident for the whole session — target 250-400 lines, hard ceiling 500); Layer 3 `references/` and `examples/` files (loaded only when Claude runs `Read` on the specific file, zero cost until then). The architectural primitive is progressive disclosure; the design discipline is keeping `SKILL.md` a lean table-of-contents and pushing everything *situational* to Layer 3. Critically, every Layer 3 file links directly from `SKILL.md` (one level deep) — nested references cause Claude to partial-read and miss content — and each companion tool / domain example is a self-contained file (one per natural unit of use), which is also what makes the milestone-2 extraction into separate skills a `mv`, not a rewrite.

**Major components:**
1. `SKILL.md` frontmatter — discovery; make Claude trigger the skill at the right time
2. `SKILL.md` body — always-on operating procedure: the sharpened 5-phase methodology, the output format, and the navigation map to Layer 3
3. `references/` — on-demand depth Claude *applies*: the validation rubric and the three companion tools (5-Whys, pre-mortem, trade-off analysis)
4. `examples/` — on-demand worked analyses Claude reads to *imitate*: one self-contained file per domain

### Critical Pitfalls

1. **Methodology too abstract to act on** — the 5 phases become inspiring labels; "identify the essence" produces a restated problem, not a decomposition. Avoid by giving each phase a concrete operation with a named output artifact, matching degrees of freedom to the step, and making companion tools the operational engines of the abstract phases.
2. **Methodology too prescriptive — box-ticking** — the opposite failure: Claude mechanically fills every section and the output *looks* rigorous while hand-waving. Avoid with a strict template *shape* but flexible content *depth*, allowing justified "nothing material here", and keeping Reason Upward explicitly high-freedom.
3. **Validation rubric that is vague, unfalsifiable, or gameable** — "is this rigorous?" certifies hand-waving as rigorous, worse than no rubric. Avoid by writing every item as a falsifiable, evidence-quoting question, testing for traceability not presence, including negative anti-rigor criteria, and verifying the rubric against a deliberately weak analysis.
4. **`SKILL.md` bloat** — examples, rubric, and three companion tools pull toward one big always-resident file that taxes every turn and risks truncation after compaction. Avoid by keeping the body under 500 lines and confirming examples/rubric/tools live in separate files.
5. **Description that never triggers (or triggers on everything)** — narrow literal triggers users never type verbatim, or broad ones that fire on routine design questions. Avoid with a "`<what>`. Use when `<concrete situations>`" pattern, enumerating intents not exact phrases, and testing 8-10 realistic phrasings across all four domains plus phrasings that should *not* trigger.
6. **Scope creep — single skill drifting toward a collection or toward code** — companion tools growing their own frontmatter/triggers, or a "quick" scripted rubric using the idle `uv` scaffold. Avoid by treating PROJECT.md's Out-of-Scope list as a hard gate and leaving `main.py`/`pyproject.toml` untouched.

## Implications for Roadmap

Build order is dependency-driven and the research is unusually clear on it: the sharpened methodology is the single dependency of everything else. The suggested phase structure follows the architecture research's build order directly.

### Phase 1: Sharpen the Methodology and Harden the Output Format
**Rationale:** The methodology is the single dependency of every other component — the rubric scores against it, companion tools slot into its phases, examples demonstrate it. Sharpening it last would invalidate everything built on a loose version. PROJECT.md explicitly flags the original methodology as "loose."
**Delivers:** A tightened 5-phase process (Identify Essence -> Challenge Assumptions -> Establish Ground Truths -> Reason Upward -> Validate) with entry/exit criteria per phase, each phase naming a concrete operation and a named output artifact; a hardened standardized output format with an explicit conclusion->ground-truth traceability section; an assumption-classification scheme.
**Addresses:** Gap 2 (tightened 5-phase process, hardened output format + traceability).
**Avoids:** Pitfall 1 (too abstract — every phase gets an operation + artifact) and Pitfall 2 (too prescriptive — strict shape, flexible depth, one deliberately high-freedom phase).

### Phase 2: SKILL.md Skeleton and Frontmatter
**Rationale:** Establishes the frontmatter, the resident methodology, and the *shape* of the navigation map so later components fill named slots rather than the map being retrofitted. The methodology-deep-dive split decision is made here.
**Delivers:** `SKILL.md` with valid open-standard frontmatter (trigger-rich multilingual `description`, `metadata.version: "2.0"`, `license: MIT`), the resident sharpened methodology and output format as standing instructions, and an "Additional resources" navigation map naming each Layer 3 file and when to open it.
**Uses:** Agent Skills open standard schema; CommonMark + YAML frontmatter (from STACK.md).
**Implements:** Components 1 and 2 (frontmatter, `SKILL.md` body).
**Avoids:** Pitfall 4 (`SKILL.md` bloat — body kept under 500 lines, written as standing instructions) and Pitfall 5 (description never/over triggers).

### Phase 3: Validation Rubric
**Rationale:** Must exist before the worked examples, because a good worked example should itself pass the rubric — building examples first risks producing examples the later rubric flags. Depends only on Phase 1.
**Delivers:** `references/validation-rubric.md` — analytic scoring, ~6-8 falsifiable evidence-quoting criteria, 3-4 discrete named levels, gate scoring model, with a "how to apply" preamble framing it as a validator->fix->repeat feedback loop.
**Addresses:** Gap 3 (self-check validation rubric).
**Avoids:** Pitfall 3 (vague/gameable rubric — falsifiable items, negative criteria, verified against a deliberately weak analysis).

### Phase 4: Companion Tool References
**Rationale:** Parallelizable with Phase 3 — each tool is independent of the others and of the rubric; they depend only on the sharpened methodology to know which phase they support. Three separate files, buildable concurrently.
**Delivers:** `references/five-whys.md`, `references/pre-mortem.md`, `references/trade-off-analysis.md` — each a self-contained, milestone-2-promotion-ready component with when-to-use, step-by-step procedure, a worked mini-example, failure modes, and an explicit handoff back to the 5-phase spine. No independent frontmatter or triggers.
**Addresses:** Gap 4 (companion tools as fully usable reference components).
**Avoids:** Pitfall 6 (scope creep — tools stay `references/` components, not skills).

### Phase 5: Domain-Spread Worked Examples
**Rationale:** Depends on Phases 1, 2, and 3 — an example is the methodology applied, in the `SKILL.md` output format, at a quality that passes the rubric. Four domains, each self-contained, buildable concurrently once the foundation is stable.
**Delivers:** `examples/software-systems.md`, `examples/product-business.md`, `examples/personal-general.md`, `examples/science-engineering.md` — each exercising the methodology *differently*, each including a false-assumption pivot, ideally each demonstrating one companion tool.
**Addresses:** Gap 1 (domain-spread worked examples).
**Avoids:** Pitfall 2 / "examples filler or domain-uniform" — deliberate per-domain variety, not one skeleton with nouns swapped.

### Phase 6: Final SKILL.md Pass, README, and Validation
**Rationale:** Wiring and verification can only happen once all Layer 3 files exist.
**Delivers:** Every Layer 3 file wired into the `SKILL.md` navigation map; all links verified forward-slash and one level deep; a human-facing `README.md` documenting copy/symlink install; `skills-ref validate` passing; activation testing across all four domains.
**Avoids:** Maintenance/version drift, broken cross-references, install breakage.

### Phase Ordering Rationale

- **Strict sequential foundation:** Phases 1 and 2 must come first and in order — the methodology is the single dependency of everything; the `SKILL.md` skeleton establishes the navigation map's shape that later phases fill.
- **Parallelizable middle:** Phases 3, 4, and 5 are largely independent once 1 and 2 are stable (the architecture research explicitly flags items 3-5 as parallel candidates). Phase 3 (rubric) should still *complete* before Phase 5 (examples) so examples can be authored to pass it.
- **Avoids the dominant content-quality risk:** putting methodology-sharpening first and rubric-before-examples directly defends against the two-way failure (too abstract / box-ticking) and prevents producing examples a later rubric would reject.
- **Future-milestone safe:** writing each companion tool and example as a self-contained file (Phases 4-5) keeps the milestone-2 split a move, not a rewrite, and the `uv` scaffold stays untouched throughout.

### Research Flags

Phases likely needing deeper research during planning:
- **Phase 1 (methodology-sharpening):** This is the highest-risk requirement — operationalizing first-principles reasoning into concrete per-phase operations is genuinely hard. A `--research-phase` pass should look at how other reasoning frameworks define falsifiable phase exit-criteria, and may benefit from drafting the methodology *using* the methodology (the dogfooding goal).
- **Phase 3 (validation rubric):** Falsifiable LLM self-evaluation is a researched but unsettled area. Worth a research pass on analytic-rubric design and self-grading leniency mitigations before authoring.

Phases with standard patterns (skip research-phase):
- **Phase 2 (SKILL.md skeleton):** Frontmatter schema, description rules, and progressive-disclosure structure are fully documented in official Anthropic sources — STACK.md and ARCHITECTURE.md already give prescriptive guidance.
- **Phase 6 (final pass / README / validation):** Mechanical wiring and validation against documented rules; no research needed.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Verified against current official Anthropic / Claude Code docs and the Agent Skills open standard; no ambiguity in the file format. |
| Features | HIGH | Skill-mechanics from official docs; reasoning-tool guidance (5-Whys, pre-mortem, trade-off) from established, multiply-corroborated practitioner sources. |
| Architecture | HIGH | Three-layer loading model and progressive-disclosure patterns are official, current, and prescriptive; build order is dependency-derived. |
| Pitfalls | HIGH overall | Skill-authoring pitfalls are HIGH (authoritative official docs); methodology-content and rubric-design pitfalls are MEDIUM (docs plus reasoning/LLM-evaluation research). |

**Overall confidence:** HIGH

### Gaps to Address

- **Operationalizing the 5 phases:** Research gives the *principle* (concrete operation + named artifact per phase, degrees-of-freedom matching) but not the finished phase definitions — that is genuine design work for Phase 1. Handle by dogfooding the methodology on the design itself and testing each phase against the Core Value (a worked run must show a full ground-truth trace).
- **Rubric falsifiability vs. self-grading leniency:** The mechanism is known (falsifiable, evidence-quoting items; negative criteria; gate scoring) but its effectiveness depends on execution. Handle in Phase 3 by validating the rubric against a deliberately weak analysis — it must catch it — before considering the rubric done.
- **Multilingual triggers have no dedicated field:** EN+ZH triggers must share the single `description`/`when_to_use` budget (1,024 / 1,536-char caps). MEDIUM confidence this is the only mechanism. Handle in Phase 2 by keeping each language's phrasing tight and checking `/doctor` for truncation.
- **Methodology-deep-dive split is a judgment call:** Whether `references/methodology-deep-dive.md` is needed depends on the sharpened methodology's final size. Decide during Phase 2; only the elaboration moves, never the procedure.

## Sources

### Primary (HIGH confidence)
- [Extend Claude with skills — Claude Code Docs](https://code.claude.com/docs/en/skills) — frontmatter reference, three-layer loading model, 500-line budget, description truncation/budget, /doctor, troubleshooting triggering
- [Skill authoring best practices — Claude Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) — descriptions (third person, what+when), progressive disclosure, one-level-deep references, degrees of freedom, anti-patterns, evaluation-driven development
- [Agent Skills Specification — agentskills.io](https://agentskills.io/specification) — open-standard schema, required/optional fields, directory conventions, skills-ref validate
- [anthropics/skills — skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) and [anthropics/claude-code skill-development](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/skill-development/SKILL.md) — pushy descriptions, packaging, preserve-name-on-update, references/examples boundaries
- [Premortem — Gary Klein](https://www.gary-klein.com/premortem) and [Performing a Project Premortem — HBR/ResearchGate](https://www.researchgate.net/publication/3229642_Performing_a_Project_Premortem) — pre-mortem technique originator
- `.planning/PROJECT.md` — project scope, constraints, Out-of-Scope boundaries, Core Value

### Secondary (MEDIUM confidence)
- [Five whys — Wikipedia](https://en.wikipedia.org/wiki/Five_whys), [5 Whys — MindTools](https://www.mindtools.com/a3mi00v/5-whys/), [5 Whys Root Cause Analysis — ReliaMag](https://reliamag.com/articles/5-whys-root-cause-analysis-maintenance/) — 5-Whys procedure and pitfalls (linear thinking, stop criteria)
- [LLM-Rubric — arXiv](https://arxiv.org/html/2501.00274v1) and [Rubric-Based Evals & LLM-as-a-Judge — Adnan Masood](https://medium.com/@adnanmasood/rubric-based-evals-llm-as-a-judge-methodologies-and-empirical-validation-in-domain-context-71936b989e80) — analytic vs holistic rubrics, level granularity, self-grading leniency
- [TICKing All the Boxes — arXiv 2410.03608](https://arxiv.org/abs/2410.03608) — checklists improve evaluation but can be gamed as a proxy
- [Skill Authoring Patterns — generativeprogrammer.com](https://generativeprogrammer.com/p/skill-authoring-patterns-from-anthropics) — corroborates official skill-authoring docs
- [First principles — Untools](https://untools.co/first-principles/) and [fs.blog](https://fs.blog/first-principles/) — methodology framing

### Tertiary (LOW confidence)
- [DavidAnson/markdownlint](https://github.com/DavidAnson/markdownlint) — generic Markdown linting config (not skill-specific; optional dev tooling only)

---
*Research completed: 2026-05-16*
*Ready for roadmap: yes*
