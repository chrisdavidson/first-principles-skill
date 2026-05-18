---
phase: 02-skill-md-skeleton-and-frontmatter
reviewed: 2026-05-16T00:00:00Z
depth: standard
files_reviewed: 10
files_reviewed_list:
  - first-principles-thinking/SKILL.md
  - first-principles-thinking/references/output-template.md
  - first-principles-thinking/references/validation-rubric.md
  - first-principles-thinking/references/five-whys.md
  - first-principles-thinking/references/pre-mortem.md
  - first-principles-thinking/references/trade-off-analysis.md
  - first-principles-thinking/examples/software-systems.md
  - first-principles-thinking/examples/product-business.md
  - first-principles-thinking/examples/personal-general.md
  - first-principles-thinking/examples/science-engineering.md
findings:
  critical: 0
  warning: 4
  info: 5
  total: 9
status: issues_found
---

# Phase 2: Code Review Report

**Reviewed:** 2026-05-16
**Depth:** standard
**Files Reviewed:** 10
**Status:** issues_found

## Summary

Reviewed the `first-principles-thinking` skill: `SKILL.md`, five `references/` files, and four `examples/` files. The skill directory name matches the frontmatter `name` (a hard `skills-ref` requirement) and the structure is one-level-deep as required. The YAML frontmatter is valid and uses spec-sanctioned fields only (`name`, `description`, `license`, `metadata.version`) — no schema violations.

The substantive content — `SKILL.md` (176 lines) and `output-template.md` (150 lines) — is internally consistent and well-structured. `SKILL.md` is well under the 500-line budget.

The dominant issue is **stub state**: 8 of 10 reviewed files are stubs (3-5 lines each, describing what the file *will* contain, tagged "Authored in Phase N"). The phase plan for this phase ("SKILL.md skeleton and frontmatter") may legitimately scope only the skeleton — but two correctness defects exist regardless of stub status: `SKILL.md` links to stub files as if they were authoritative content, and it references an undefined identifier scheme (`D-07`, `D-03`).

## Warnings

### WR-01: `D-07` and `D-03` referenced but never defined

**File:** `first-principles-thinking/SKILL.md:71,81,97`; `first-principles-thinking/references/output-template.md:44,83,114,134,150`
**Issue:** The methodology and output template repeatedly invoke decision identifiers `D-07` ("the confidence caveat rules from D-07", "per D-07", "satisfies D-03") as if they are defined constraints the reader can look up. No file in the skill defines what `D-07` or `D-03` are, nor states where they live. A reader (human or model) following these references hits a dead identifier. Either these are internal planning-doc IDs that leaked into shipped skill content, or a `references/` file defining the D-codes is missing. As written, every `D-07`/`D-03` citation is unresolvable.
**Fix:** Either (a) remove the bare `D-NN` citations and inline the rule text directly (e.g. "...inherits an explicit confidence caveat" with the rule stated, not cited), or (b) add the defining text to the skill and link to it. Shipped skill content must not reference identifiers that only exist in `.planning/`.

### WR-02: `SKILL.md` links to stub files as if they were complete content

**File:** `first-principles-thinking/SKILL.md:151,165,166,167,173,174,175,176`
**Issue:** `SKILL.md` directs the model to read `validation-rubric.md`, `five-whys.md`, `pre-mortem.md`, `trade-off-analysis.md`, and all four `examples/*.md` files for operative instructions — e.g. line 150-151 says "Score the completed analysis against the rubric in [references/validation-rubric.md]". But every one of those targets is a 3-5 line stub containing only a description of future content ("Authored in Phase 3", "Authored in Phase 5"). A model triggered today would be instructed to apply a rubric that does not exist, and to calibrate against worked examples that contain no analysis. The links resolve as file paths but the content behind them is non-functional. This is a correctness defect: the skill's "Before presenting conclusions" gate (lines 148-157) cannot be satisfied because its referenced rubric is empty.
**Fix:** If this phase only ships the skeleton, gate the dependent instructions — e.g. mark the "Before presenting conclusions" and "Companion thinking tools"/"Worked examples" sections as pending, or do not link stub files from operative instructions until they are authored. Alternatively, accept this as known phased state and confirm the phase plan explicitly defers these — but `SKILL.md` should not present an empty rubric as a live gate.

### WR-03: Stub files do not clearly signal stub status to a model consumer

**File:** `first-principles-thinking/references/validation-rubric.md:1-5`; `five-whys.md:1-5`; `pre-mortem.md:1-5`; `trade-off-analysis.md:1-3`; all four `examples/*.md:1-3`
**Issue:** Each stub's body is written as a descriptive sentence ("A self-contained root-cause drill-down procedure — when to use it, a branching procedure...") with no explicit "STUB" / "TODO" / "not yet authored" marker. A model that reads `five-whys.md` after being sent there by `SKILL.md` will see prose that reads like a summary of present content, not a placeholder. The only stub signal is the trailing "Authored in Phase N" clause, which describes provenance ambiguously — it reads equally as "this was authored in Phase N" (past, done) as "this is to be authored in Phase N" (future, pending). The skeleton intent is not unambiguously communicated.
**Fix:** Add an explicit status marker to every stub, e.g. a first line `> **STATUS: STUB — full content authored in Phase N. Do not rely on this file yet.**` so both humans and the model can tell the file is incomplete.

### WR-04: `output-template.md` references the unresolved `D-07`/`D-03` codes in author-facing guidance

**File:** `first-principles-thinking/references/output-template.md:44,83,114,134,150`
**Issue:** Same root cause as WR-01, but worth flagging separately because `output-template.md` is *fully authored* content (150 lines) — it is not a stub, so its dependence on undefined codes is a shipped defect, not a deferred one. Line 134 ("The escape valve still satisfies D-03") and line 114 ("Unverified input rule (D-07)") present these as authoritative rule citations within otherwise-complete instructions. A user authoring an analysis from this template cannot verify they have satisfied D-03/D-07 because the criteria are nowhere stated.
**Fix:** Inline the actual rule each code stands for. `output-template.md` already restates most D-07 logic in prose (lines 87, 114, 150) — drop the bare `(D-07)` / `D-03` tags or replace them with a self-contained rule name the document itself defines.

## Info

### IN-01: `validation-rubric.md` advertises "6-8 analytic criteria" — a range that may drift from the eventual rubric

**File:** `first-principles-thinking/references/validation-rubric.md:2`
**Issue:** The stub pre-commits to "6-8 analytic criteria" and the named levels "Rigorous / Adequate / Hand-wavy / Absent". If the Phase 3 authoring lands on a different count or level names, this stub becomes a stale spec. Minor — but stubs that over-specify create later inconsistency risk.
**Fix:** Keep the stub minimal (state intent, not exact counts) or treat the count/levels as a binding spec the Phase 3 work must honor.

### IN-02: Inconsistent em-dash vs hyphen and "5-Whys" capitalization across files

**File:** `first-principles-thinking/references/five-whys.md:1` ("5-Whys"); `SKILL.md:165` ("5-Whys"); `SKILL.md:9` ("a pre-mortem or 5-Whys")
**Issue:** Cosmetic only — the heading "# 5-Whys" vs prose "5-Whys" is consistent, but worth a pass at authoring time to keep tool names uniform (e.g. "Pre-Mortem" heading vs "pre-mortem" in `SKILL.md:166`).
**Fix:** Pick one canonical casing per tool name and apply it consistently when the reference files are authored.

### IN-03: `output-template.md` "Note" claims a condensed skeleton "lives resident in SKILL.md" — verify it stays in sync

**File:** `first-principles-thinking/references/output-template.md:3-6`
**Issue:** `SKILL.md` "Output format" (lines 117-144) and `output-template.md` both define the six-section order and the chain format. They currently agree exactly. This is duplicated content across two files — a future edit to one risks drift. Not a defect now; a maintenance hazard.
**Fix:** Acceptable as deliberate progressive-disclosure duplication. Consider a comment in both files noting the sibling must be kept in sync, or treat `output-template.md` as the single source and have `SKILL.md` carry only section names.

### IN-04: `description` front-loads well but is long (620 chars of the 1024 cap)

**File:** `first-principles-thinking/SKILL.md:3-12`
**Issue:** The `description` is 620 characters — within the hard 1024 cap and the combined 1536 truncation budget, so no violation. It is a single long trigger list. The key use case ("analyze from first principles") is front-loaded correctly. Flagged only so the team is aware there is limited remaining headroom if `when_to_use` is later added.
**Fix:** None required. Monitor combined length if `when_to_use` is introduced.

### IN-05: Examples stubs all promise "a dead-end" / "abandoned reasoning path" — confirm each domain example actually delivers one

**File:** `examples/software-systems.md:3`; `product-business.md:3`; `personal-general.md:3`; `science-engineering.md:3`
**Issue:** Each example stub commits to "showing a dead-end" / "showing at least one abandoned reasoning path". The output format (`SKILL.md:125`, `output-template.md:118-134`) makes the Abandoned Reasoning section mandatory with an escape valve. When these examples are authored in Phase 5, each must contain a *genuine* dead end, not an escape-valve note — otherwise the example fails to calibrate the very section it is meant to demonstrate.
**Fix:** No action now. Phase 5 authoring must ensure each example shows a real abandoned path with a substantive "Why abandoned" reason (per `output-template.md:126`).

---

_Reviewed: 2026-05-16_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
