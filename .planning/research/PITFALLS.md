# Pitfalls Research

**Domain:** Authoring a pure-Markdown Claude Code skill that delivers a structured first-principles-thinking (reasoning/methodology) skill
**Researched:** 2026-05-16
**Confidence:** HIGH (official Anthropic skill-authoring docs are authoritative and current; methodology-content and rubric pitfalls are MEDIUM, grounded in docs plus reasoning research)

## Scope note

This is a **methodology skill** (reference content that shapes how Claude reasons), not a tool skill (executable scripts that do work). Most published skill-authoring guidance assumes tool skills — the highest-value pitfalls here are the ones that are *specific to reasoning/methodology content* and to *pure-Markdown* skills. Generic advice ("write tests", "handle errors in scripts") mostly does not apply: v1 ships no code.

## Critical Pitfalls

### Pitfall 1: Description that never triggers (or triggers on everything)

**What goes wrong:**
The skill either never activates when a user wants first-principles analysis, or it activates on almost every analytical request and crowds out normal responses. The original skill's description leans on phrases like "analyze from first principles" and "challenge assumptions" — narrow literal triggers that users rarely type verbatim, while "is this the right approach" is broad enough to fire on routine design questions.

**Why it happens:**
At startup only the `name` + `description` (combined `description` + `when_to_use`, capped at 1,536 chars) are loaded into context. Claude selects skills purely from that text. Authors write descriptions as a *label* ("First principles thinking methodology") instead of as a *selection instruction* ("...Use when the user asks to challenge assumptions, evaluate a design's fundamentals, question whether an approach is sound, or asks for reasoning from scratch"). The official guidance is explicit: the description must state **both what the skill does and when to use it**, in **third person**, with the key use case first.

**How to avoid:**
- Write the description as: `<what it does>. Use when <concrete trigger situations>.` Lead with the single most common trigger.
- Enumerate *situations and intents*, not just exact phrases — users say "I'm not sure this design is right", not "challenge assumptions".
- Use `when_to_use` frontmatter for additional trigger phrases/example requests rather than bloating `description`.
- Decide invocation mode deliberately. A reasoning methodology is partly *reference content* (Claude should apply it when relevant) and partly *invokable* (`/first-principles`). Keep model invocation **on**, but make the description specific enough that it does not fire on every "review this code" request.
- Test activation on 8-10 realistic phrasings across all four domains (software, product, personal, science) before shipping — and test phrasings that should *not* trigger it.

**Warning signs:**
- The description is a noun phrase with no "Use when..." clause.
- Trigger phrases are all exact quotes a user would have to know in advance.
- During testing, asking "is this a good design?" always pulls the skill, even for trivial questions.

**Phase to address:** Methodology/SKILL.md authoring phase; verified in a dedicated activation-testing phase or gate.

---

### Pitfall 2: SKILL.md bloat — always-resident content burning the context budget

**What goes wrong:**
The whole methodology — 5 phases, output template, all four worked examples, the validation rubric, and the three companion tools — ends up inline in SKILL.md. Once invoked, SKILL.md enters the conversation as a single message and **stays there for the rest of the session** (it is not re-read; after auto-compaction only the first ~5,000 tokens of each invoked skill are re-attached, sharing a 25,000-token budget). A bloated methodology skill therefore taxes every subsequent turn and risks being truncated after compaction.

**Why it happens:**
This project's deliverables (4 domains of examples, a rubric, 3 companion tools) naturally pull toward one big file. Authors treat SKILL.md like a document rather than a "table of contents". The original skill is small; the v1 expansion is exactly where bloat creeps in.

**How to avoid:**
- Keep the SKILL.md **body under 500 lines** (official limit for "optimal performance"). Treat it as a navigation hub: the 5-phase process summary, the output format, and one-line pointers to everything else.
- Worked examples → `examples/` (one file per domain). The rubric → `references/validation-rubric.md`. Each companion tool → its own `references/` file. These cost **zero context tokens until Claude reads them**.
- Apply the conciseness test to every paragraph: "Does Claude already know this?" Cut explanations of what "assumption" or "root cause" mean.
- Because the body stays resident, write it as **standing instructions** ("When applying this skill, do X") not one-time narration.

**Warning signs:**
- SKILL.md is creeping past ~400 lines.
- Examples or rubric text are pasted inline "so Claude definitely sees them".
- The body explains *why* first-principles thinking is valuable rather than *what to do*.

**Phase to address:** SKILL.md structure/authoring phase; enforce with the file-size check in the validation phase.

---

### Pitfall 3: Methodology too abstract to act on

**What goes wrong:**
The 5 phases (Identify Essence → Challenge Assumptions → Establish Ground Truths → Reason Upward → Validate) read as inspiring labels but give Claude nothing operational. "Identify the essence" without a procedure produces a restated problem statement, not a decomposition. The analysis sounds first-principles but is reasoning-by-analogy in disguise.

**Why it happens:**
First-principles thinking is genuinely hard to operationalize; it is tempting to gesture at it. The PROJECT.md itself flags the original methodology as "loose" — this is the known weak point. Authors under-specify because they assume a smart model fills the gap; but vague process instructions get vague compliance.

**How to avoid:**
- For each phase, give a **concrete operation with an artifact**: e.g. Challenge Assumptions → "List every assumption as a table row; for each, write the question that would falsify it and where the evidence to answer it comes from." That is actionable and verifiable.
- Match degrees of freedom to the step (official guidance). Phases where many paths are valid (Reason Upward) get high-freedom prose; phases that must be done a specific way (Establish Ground Truths must cite verifiable sources) get low-freedom, near-procedural instructions.
- Make the companion tools (5-Whys, pre-mortem, trade-off analysis) the *operational engines* of the abstract phases — e.g. 5-Whys is the procedure for "Challenge Assumptions", pre-mortem feeds "Validate". This converts abstraction into named, runnable sub-procedures.
- Test against the project's own Core Value: every conclusion must trace to a verified ground truth. If a worked run can't show that trace, the methodology is still too abstract.

**Warning signs:**
- A phase instruction is a single sentence with no artifact or output named.
- A worked example's "essence" section just rephrases the prompt.
- You cannot tell, from the output, whether Claude actually did the phase or skipped it.

**Phase to address:** Methodology-sharpening phase (this is the core requirement most at risk).

---

### Pitfall 4: Methodology so prescriptive it becomes box-ticking

**What goes wrong:**
The opposite failure: the process is so rigid that Claude mechanically fills every section to satisfy the format, producing a five-heading document where the headings are populated but no real reasoning happened. The output *looks* rigorous and is hand-waving — exactly the failure the Core Value forbids.

**Why it happens:**
Over-correcting Pitfall 3. A strict template plus "ALWAYS fill every section" trains the model to treat completion as the goal. Research on checklist-driven LLM generation shows checklists improve evaluation but can also be *gamed* — the model optimizes the visible criterion, not the underlying quality.

**How to avoid:**
- Use the official **template-strictness spectrum**: strict template for the *output shape*, but flexible guidance for the *content depth* ("use your best judgment based on the analysis").
- Allow phases to legitimately produce "nothing material here" with a justification, rather than forcing fabricated content. A pre-mortem with no plausible failure is a valid (rare) result; forcing three invented failures is box-ticking.
- Frame instructions around the *goal of the phase* ("surface the assumption that, if wrong, breaks the conclusion") not the *act of filling a section*.
- Keep one high-freedom phase explicitly: Reason Upward should say "build the chain however the problem demands" — not impose a fixed number of steps.

**Warning signs:**
- Every worked example has exactly the same section lengths and item counts.
- Instructions say "always include N assumptions / N whys".
- Output reads as a filled form; removing a section would not change the conclusion.

**Phase to address:** Methodology-sharpening phase and worked-examples phase (examples must demonstrate judgment, not uniformity).

---

### Pitfall 5: Validation rubric that is vague, unfalsifiable, or gameable

**What goes wrong:**
The Markdown self-check rubric uses criteria like "Is the analysis rigorous?" or "Did it follow first principles?" — questions Claude can answer "yes" to about any output. Or the rubric is a checklist the model satisfies by *adding the words the rubric looks for* rather than by doing the work. The rubric then certifies hand-waving as rigorous, which is worse than no rubric.

**Why it happens:**
Writing falsifiable evaluation criteria is hard. Self-evaluation by the same model that produced the output has a known optimism/self-consistency bias. Rubric criteria drift toward restating the methodology's section names ("Has an Assumptions section? ✓") which checks *presence*, not *quality*.

**How to avoid:**
- Make every rubric item a **falsifiable, evidence-pointing question**: not "assumptions challenged?" but "For each listed assumption, is there a specific named source or test that would confirm or refute it? Quote it." A criterion you cannot fail is not a criterion.
- Test for **traceability, not presence**: "Pick the final conclusion. Walk the chain backward. Does every link rest on a ground truth, or does one link rest on 'industry standard' / analogy?" — analogy-detection is the rubric's real job.
- Include **negative criteria** (anti-rigor detectors): flag phrases like "best practice", "everyone does", "obviously" used *as* justification.
- Have the rubric require the model to **quote the specific text** that satisfies each criterion, so a pass cannot be asserted without evidence.
- Accept that a Markdown rubric is a quality *forcing-function*, not a guarantee. Scope it honestly (the PROJECT.md already defers scripted scoring) and word it so the cheapest way to pass is to actually do the analysis.

**Warning signs:**
- A rubric item can be answered without re-reading the analysis.
- Criteria mirror the 5 phase names one-to-one (presence checking).
- The rubric has no item that could plausibly produce a "fail".
- Passing the rubric requires no quotation or pointer into the analysis.

**Phase to address:** Validation-rubric phase. Verify by running the rubric against a deliberately weak analysis — it must catch it.

---

### Pitfall 6: Worked examples that are filler, copied verbatim, or domain-uniform

**What goes wrong:**
The four new domain examples (software, product, personal, science) are padding — too long, too similar in structure, or written so completely that Claude copies an example's wording and structure verbatim into a real analysis instead of *applying the pattern*. Examples too uniform in shape reinforce the box-ticking failure (Pitfall 4).

**Why it happens:**
"More examples = better" is a tempting heuristic. Expanding to four domains invites copy-paste authoring where each example is the same skeleton with nouns swapped. Long, polished examples are the easiest thing for a model to mimic surface-level.

**How to avoid:**
- Each example must teach something the others don't: different domains should exercise the methodology *differently* — a science example leans on ground-truth verification, a personal-decision example leans on assumption-challenging, a product example leans on trade-off analysis. Deliberate variety teaches the pattern; uniformity teaches the template.
- Keep examples concrete and **as short as they can be while still showing the full trace**. Official guidance: examples must be concrete, not abstract — but conciseness still applies.
- Show the *reasoning move*, not just the polished result — include a moment where an assumption is found false and the analysis changes course. Verbatim-copyable examples have no such pivot.
- Put examples in `examples/`, one file per domain (zero context cost until read), and reference them from SKILL.md by what each *demonstrates*, not just by domain name.
- Consider showing one *weak* analysis (and the rubric catching it) as a contrast example — this teaches the pattern far better than four clean successes.

**Warning signs:**
- Two examples differ only in nouns.
- An example is longer than the methodology itself.
- Examples have no false-assumption pivot — every analysis runs straight to the "right" answer.
- Real analyses start reusing an example's exact phrasing.

**Phase to address:** Worked-examples phase.

---

### Pitfall 7: Scope creep — single skill drifting toward a collection or toward code

**What goes wrong:**
The companion tools (5-Whys, pre-mortem, trade-off analysis) quietly become three near-independent skills with their own triggers; or a validation script gets added "because it's more reliable". Either drift violates the explicit v1 boundary (single skill, pure Markdown) and pre-empts milestones 2 and 3.

**Why it happens:**
The companion tools genuinely *could* be separate skills — the boundary is a deliberate sequencing decision, not a natural one, so it erodes easily. The `uv` Python scaffold is sitting right there in the repo, tempting a "quick" scripted rubric. Official guidance even recommends utility scripts for deterministic operations, which reads as license to add code.

**How to avoid:**
- Companion tools live as `references/` files **inside the one skill**, invoked *by the methodology*, with no independent frontmatter/triggers. They are components, not skills.
- Treat the PROJECT.md "Out of Scope" list as a gate: splitting into multiple skills → milestone 2; Python builder → milestone 3; scripted scoring → later. Any PR proposing these in v1 is rejected by definition.
- Leave the `uv` scaffold untouched — do not let "the rubric would be better as a script" reopen the pure-Markdown decision. The validation rubric is Markdown the model applies; that is the decision of record.
- If a companion tool feels like it wants its own trigger, that is the signal it is being over-built for v1 — pull it back to a reference component.

**Warning signs:**
- A companion tool file grows its own YAML frontmatter or "Use when..." description.
- Discussion of "should the rubric just be a script" resurfaces.
- `main.py` / `pyproject.toml` get edited.
- The skill directory starts looking like it contains multiple `SKILL.md` files.

**Phase to address:** Every phase — this is a standing scope discipline. Reinforce at companion-tools phase (highest risk) and at any milestone/transition review.

---

## Technical Debt Patterns

Shortcuts that seem reasonable but create long-term problems.

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Inline the rubric/examples into SKILL.md "so Claude sees them" | Nothing to wire up; one file | Permanent per-turn context tax; truncation risk after compaction | Never — progressive disclosure is the whole point |
| Reuse one example skeleton across all four domains | Fast to author four examples | Teaches the template not the pattern; reinforces box-ticking | Never — defeats the purpose of multi-domain coverage |
| Vague "is it rigorous?" rubric items | Rubric ships fast | Certifies hand-waving; gives false confidence | Never — an unfalsifiable rubric is worse than none |
| Description as a bare label, no "Use when" | Quick to write | Skill never triggers or over-triggers | Never — costs almost nothing to fix, breaks everything if wrong |
| Deeply nested references (SKILL.md → A.md → B.md) | Tidy-looking hierarchy | Claude previews with `head` and reads partial files; misses content | Never — keep all references one level deep from SKILL.md |
| Skip activation testing across the four domains | Ship sooner | Discover non-triggering only after users complain | Only if a later phase explicitly schedules the test |

## Integration Gotchas

"Integration" here = the skill's contract with the Claude Code runtime and the original repo's install model.

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| YAML frontmatter | XML tags in `description`; reserved words "claude"/"anthropic" in `name`; `name` with uppercase/spaces | `name`: lowercase + hyphens, ≤64 chars; `description` ≤1024 chars, no XML tags, third person |
| `description` truncation | Long description with key trigger buried at the end | Put the primary use case first; combined `description`+`when_to_use` is cut at 1,536 chars |
| Cross-file references | Windows-style backslash paths; links Claude can't resolve | Forward slashes always (`references/pre-mortem.md`); all references one level deep from SKILL.md |
| Reference file length | A 200-line companion-tool file with no map | Add a table of contents to any reference file >100 lines so partial reads still see full scope |
| Install model | Restructuring the directory so copy/symlink into a skills dir breaks | Keep `SKILL.md` + `references/` + `examples/` layout matching the original repo |
| Skill content lifecycle | Writing the body as one-time steps assuming Claude re-reads it | Body is read once and stays resident — write standing instructions, keep it lean |

## Performance Traps

"Scale" for a methodology skill = context budget and number of co-installed skills, not users.

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| Always-resident SKILL.md bloat | Long sessions degrade; skill influence fades after compaction | Body <500 lines; push examples/rubric/tools to on-demand files | Noticeable once SKILL.md exceeds the first-5,000-token re-attach window after compaction |
| Description budget overflow | Skill description silently dropped when many skills installed | Keep description tight; lead with key use case; `/doctor` to check budget | When co-installed skills exceed the ~1%-of-context skill-listing budget |
| Skill stops influencing mid-session | Later turns ignore the methodology | Strengthen `description`/instructions; re-invoke after compaction | After invoking several other skills, or after auto-compaction drops older ones |
| Reference files Claude never opens | A companion tool is authored but never used | Reference it explicitly from SKILL.md by what it *does*; observe navigation in testing | When SKILL.md's pointer is vague or buried |

## Security Mistakes

Minimal surface for a pure-Markdown methodology skill, but not zero.

| Mistake | Risk | Prevention |
|---------|------|------------|
| Adding `allowed-tools` the methodology doesn't need | A trusted project skill silently grants broad tool access | v1 is pure reasoning — omit `allowed-tools` entirely; no tool pre-approval needed |
| Dynamic context injection (`` !`cmd` ``) for "convenience" | Runs shell commands before Claude sees content; expands attack/scope surface | v1 has no need for `!`command`` injection — keep the skill static Markdown |
| Methodology that defers to "common knowledge" as ground truth | Encodes unverified claims as fact — an integrity flaw, not a CVE | Ground Truths phase must require verifiable, citable sources; rubric flags analogy-as-evidence |

## UX Pitfalls

"Users" = both the human invoking the skill and Claude consuming it.

| Pitfall | User Impact | Better Approach |
|---------|-------------|-----------------|
| Output format Claude follows mechanically | Reader gets a filled form, not insight | Strict shape + flexible depth; allow justified "nothing material here" |
| Methodology jargon with no operational meaning | Claude produces plausible-sounding non-analysis | Every phase names a concrete operation and artifact |
| Four near-identical worked examples | Reader/model learns the skeleton, not the skill | Each example exercises the methodology differently per domain |
| Over-eager triggering | Skill fires on routine questions, slows ordinary chat | Specific "Use when" clause; test phrasings that should NOT trigger |
| Rubric that always passes | False confidence the analysis was rigorous | Falsifiable items; require quoted evidence; test against a weak analysis |

## "Looks Done But Isn't" Checklist

Things that appear complete but are missing critical pieces.

- [ ] **Description:** Often missing the "Use when..." clause — verify it names concrete trigger situations, in third person, key use case first.
- [ ] **SKILL.md size:** Often over 500 lines once examples/rubric creep in — verify body line count and that examples/rubric/tools are in separate files.
- [ ] **Methodology phases:** Often abstract labels — verify each phase names a concrete operation and a named output artifact.
- [ ] **Validation rubric:** Often unfalsifiable — verify each item is a question that could produce a "fail" and requires quoted evidence; test it against a deliberately weak analysis.
- [ ] **Worked examples:** Often domain-uniform — verify each exercises the methodology differently and includes a false-assumption pivot.
- [ ] **Companion tools:** Often drifting toward separate skills — verify they are `references/` files with no independent frontmatter/triggers.
- [ ] **Cross-references:** Often broken or nested too deep — verify every link is forward-slash, resolves, and is one level deep from SKILL.md.
- [ ] **Activation:** Often never tested — verify it triggers on realistic phrasings across all four domains and does NOT trigger on routine requests.
- [ ] **No time-sensitive content / no version drift** — verify dates and any "current vs old" framing use the `<details>` "old patterns" pattern, not inline conditionals.

## Recovery Strategies

When pitfalls occur despite prevention, how to recover.

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| Description never/over triggers | LOW | Rewrite `description`; add `when_to_use`; re-test activation phrasings — text-only change |
| SKILL.md bloat | MEDIUM | Extract examples/rubric/tools into `references/` and `examples/`; replace inline content with one-line pointers |
| Methodology too abstract | HIGH | Re-author each phase with a concrete operation + artifact; re-derive all worked examples to match; re-validate against Core Value |
| Methodology too prescriptive | MEDIUM | Loosen content-depth guidance; allow justified empty sections; de-uniform the examples |
| Rubric gameable/vague | MEDIUM | Rewrite items as falsifiable, evidence-quoting questions; add negative criteria; re-test against a weak analysis |
| Examples filler/uniform | MEDIUM | Rewrite each to exercise a different methodology emphasis; add a false-assumption pivot; trim length |
| Scope creep into collection/code | LOW-MEDIUM | Pull companion tools back to `references/` components; revert any script; reaffirm Out-of-Scope gate |
| Broken cross-references | LOW | Fix paths to forward-slash, one-level-deep; verify every link resolves |

## Pitfall-to-Phase Mapping

How roadmap phases should address these pitfalls. (Phase names are indicative — adjust to the actual roadmap.)

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| Description never/over triggers | SKILL.md authoring | Activation test: triggers on 8-10 realistic phrasings across 4 domains; stays silent on routine requests |
| SKILL.md bloat | SKILL.md structure / authoring | Body line count <500; examples/rubric/tools confirmed in separate files |
| Methodology too abstract | Methodology-sharpening | Each phase has a named operation + artifact; a worked run shows a full ground-truth trace |
| Methodology too prescriptive | Methodology-sharpening + worked-examples | Examples vary in shape; instructions allow justified empty sections; no fixed item counts |
| Rubric vague/gameable | Validation-rubric | Rubric run against a deliberately weak analysis catches it; every item can fail and requires quoted evidence |
| Examples filler/uniform | Worked-examples | Each example exercises a different methodology emphasis; each has a false-assumption pivot |
| Scope creep | All phases; reinforced at companion-tools phase | Single `SKILL.md`; companion tools have no own frontmatter; `uv` scaffold untouched; no scripts |
| Maintenance / version drift / broken refs | Final validation / packaging | No time-sensitive content; all cross-references resolve and are one level deep; install-by-copy still works |

## Maintenance Pitfalls (skill rot)

Specific to a long-lived methodology skill in a multi-milestone project.

- **Version drift between SKILL.md and `version` frontmatter / README.** Bump and reconcile them together; the PROJECT.md notes the original carries a `version` field.
- **Cross-reference rot when files are renamed.** Milestone 2 will split this into a collection — any rename breaks SKILL.md links. Keep references one level deep and few, so a rename is a small, auditable change.
- **Time-sensitive content baked into the methodology or examples.** Avoid "as of 2026..." phrasing; use the official `<details>`/"old patterns" convention if historical context is ever needed.
- **Terminology drift across files.** The methodology, rubric, and three companion tools must use one vocabulary ("assumption", "ground truth", "reasoning chain") consistently — inconsistent terms across reference files degrade Claude's ability to follow them.
- **Examples decaying as the methodology sharpens.** When a phase is rewritten, every worked example that demonstrates it must be re-derived, or the examples now teach an outdated process.

## Sources

- [Skill authoring best practices — Claude Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) — authoritative; conciseness, degrees of freedom, descriptions, progressive disclosure, anti-patterns, evaluation-driven development. HIGH confidence.
- [Extend Claude with skills — Claude Code Docs](https://code.claude.com/docs/en/skills) — authoritative; frontmatter reference, skill content lifecycle, description truncation/budget, troubleshooting "skill not triggering" / "triggers too often". HIGH confidence.
- [TICKing All the Boxes: Generated Checklists Improve LLM Evaluation and Generation (arXiv 2410.03608)](https://arxiv.org/abs/2410.03608) — informs the rubric-gaming / box-ticking pitfalls; checklists improve evaluation but can be optimized as a proxy. MEDIUM confidence.
- [chrisdavidson/first-principles-skill](https://github.com/chrisdavidson/first-principles-skill) — the source skill being enhanced; structure, 5-phase methodology, trigger phrases. MEDIUM confidence (GitHub page summary).
- `.planning/PROJECT.md` — project scope, constraints, Out-of-Scope boundaries, Core Value. HIGH confidence (project source of truth).

---
*Pitfalls research for: pure-Markdown Claude Code methodology/reasoning skill authoring*
*Researched: 2026-05-16*
