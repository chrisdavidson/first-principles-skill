---
phase: 05-domain-spread-worked-examples
reviewed: 2026-05-17T00:00:00Z
depth: standard
files_reviewed: 4
files_reviewed_list:
  - first-principles-thinking/examples/software-systems.md
  - first-principles-thinking/examples/product-business.md
  - first-principles-thinking/examples/personal-general.md
  - first-principles-thinking/examples/science-engineering.md
findings:
  critical: 0
  warning: 6
  info: 7
  total: 13
status: issues_found
---

# Phase 5: Code Review Report

**Reviewed:** 2026-05-17
**Depth:** standard
**Files Reviewed:** 4
**Status:** issues_found

## Summary

Reviewed the four domain worked-example documents that calibrate the First Principles
Thinking skill: `software-systems.md`, `product-business.md`, `personal-general.md`, and
`science-engineering.md`. These are pure-Markdown deliverables; review focused on
structural conformance to the canonical six-section format (`references/output-template.md`),
internal consistency, factual/arithmetic correctness in the worked reasoning, adherence to
the skill's own derivation rules (D-07 unverified-input rule, the "no analogies as direct
evidence" rule, the chain-format rules), and cross-references.

All four files use the correct six section headings in the fixed order, and the quantitative
arithmetic in `science-engineering.md` and `personal-general.md` checks out. However, there
are real defects: the examples violate the skill's own stated chain-format and
one-chain-per-conclusion rules in several places, the documents are internally inconsistent
in how they label and number conclusions, and two examples make rule claims that the skill
files do not support ("Phase 4 no-analogies-as-direct-evidence rule"; the "Essence Statement"
naming). No critical (shipping-blocking) defects, but the consistency and rule-conformance
warnings undermine the examples' core purpose: they are explicitly meant to "calibrate format
and rigor" per `SKILL.md` line 171, so a format violation in an example is a propagating
defect.

## Warnings

### WR-01: Derivation chains violate the skill's own one-chain-per-conclusion rule

**File:** `first-principles-thinking/examples/software-systems.md:87-145`
**Issue:** `output-template.md:95` states: "Every conclusion offered in this analysis must
have exactly one chain here — no more (no redundant restatement), no fewer (no orphaned
conclusions)." The software-systems example labels three derivation chains "Conclusion A",
"Conclusion B", "Conclusion C", but the Section 6 Conclusion presents a single recommended
three-step approach. Conclusions A, B, and C are intermediate findings, not the conclusions
the analysis "offers" — the offered conclusion is the three-step intervention. Meanwhile
each of A/B/C maps to a step in Section 6, so the document effectively restates conclusions
across sections. The example does not cleanly demonstrate the one-chain-per-conclusion rule
it is supposed to calibrate readers on.
**Fix:** Either (a) rename A/B/C to make explicit they are sub-conclusions feeding one
synthesized recommendation, and ensure Section 6 does not introduce new reasoning (it
currently does — see WR-04), or (b) restructure so each Section 6 step traces to exactly
one named chain. Make the labelling consistent with `product-business.md`, which uses
unlettered `### Conclusion:` headings.

### WR-02: Inconsistent conclusion-heading convention across the four examples

**File:** `first-principles-thinking/examples/software-systems.md:87,106,127` and `first-principles-thinking/examples/science-engineering.md:94,114`
**Issue:** The four examples are meant to be a calibration set read together, but they use
three different conventions for Section 4 conclusion headings:
- `software-systems.md`: `### Conclusion A:`, `### Conclusion B:`, `### Conclusion C:`
- `product-business.md`: `### Conclusion:` (three times, unlabelled, unnumbered)
- `personal-general.md`: `### Conclusion:` (twice, unlabelled)
- `science-engineering.md`: `### Conclusion:` (twice, unlabelled)
A reader calibrating format from these examples gets contradictory signals about whether
chains are labelled/numbered. `output-template.md:105` shows the canonical form as
`### Conclusion: [Conclusion text]` with no letter/number.
**Fix:** Standardize all four examples on the template's `### Conclusion: [text]` form.
If multiple chains need disambiguation, append a stable identifier consistently (e.g.,
`### Conclusion C-1:`), but apply the same scheme in every file.

### WR-03: Chain in software-systems Conclusion A omits the GT-3 it relies on

**File:** `first-principles-thinking/examples/software-systems.md:87-100`
**Issue:** The chain header for Conclusion A declares its inputs as "GT-1 ... + GT-2 ...",
but the conclusion text ("the current bottleneck is the sequential pipeline that blocks
every deploy ... regardless of the code change size" and "a sufficient explanation of the
2-deploy/day ceiling") depends on GT-3 (the measured 2-deploys/day ceiling). The chain
asserts a fact about the 2-deploy/day ceiling without naming GT-3 as an input.
`output-template.md:107` requires the chain header to name every GT the chain combines.
Conclusion C (line 129) correctly cites GT-3; Conclusion A silently uses it.
**Fix:** Change the Conclusion A chain header to `GT-1 ... + GT-2 ... + GT-3 ...` and
verify the intermediate step is statable from the three combined.

### WR-04: Section 6 Conclusion introduces new reasoning and a new constraint, violating the synthesis-only rule

**File:** `first-principles-thinking/examples/software-systems.md:255-281`
**Issue:** `output-template.md:140` states the Conclusion section "synthesizes what the
Derivation Chains established — it does not introduce new claims or reasoning." The
software-systems Section 6 introduces concrete time estimates not present in any chain
("Profile the pipeline (1 day)", "days to 2 weeks") and a new pipeline stage taxonomy
("artifact build, deployment and restart, health-check wait") that does not appear in any
GT or chain. Conclusion C's chain (lines 127-145) discusses cost/risk in qualitative
terms ("days", "weeks-to-months") but the specific "1 day" profiling estimate and the
health-check-wait stage are new claims appearing only in Section 6.
**Fix:** Move the stage taxonomy and time estimates into the derivation chains (e.g.,
Conclusion C), or add a ground truth for the pipeline stages, so Section 6 only restates
what an earlier section established.

### WR-05: References a "Phase 4 no-analogies-as-direct-evidence rule" that the skill files do not define as a numbered rule

**File:** `first-principles-thinking/examples/product-business.md:76`
**Issue:** The text says: "The Phase 4 no-analogies-as-direct-evidence rule requires any
reference to how others solved a similar problem to be grounded in a named GT." The
no-analogies guidance does exist (`SKILL.md:95`, in the Phase 4 Operation paragraph), but
it is not named "the no-analogies-as-direct-evidence rule" anywhere, and it is not a
numbered rule the way `D-07` is. The example also references "the Phase 4
no-analogies-as-direct-evidence rule" (line 9 success criteria) as if it were a citable
named rule. This invents authoritative-sounding terminology that the skill does not
define, which will confuse a reader cross-checking against `SKILL.md`.
**Fix:** Either reword to cite the actual guidance ("the Phase 4 instruction not to use
analogies as direct evidence — `SKILL.md`") or, if a named/numbered rule is intended,
add it to `SKILL.md` so the example and the skill agree. Cross-file terminology must
match.

### WR-06: science-engineering applies a single 0.80 derating factor to an off-grid (battery-mediated) load without accounting for battery round-trip loss

**File:** `first-principles-thinking/examples/science-engineering.md:96-105,116-128`
**Issue:** The panel-sizing chain computes "Required daily panel output = 1.5 kWh ÷ 0.80
= 1,875 Wh/day", treating GT-2's 0.80 factor as covering "temperature losses, wiring
losses, MPPT controller efficiency, and inverter efficiency" (GT-2, line 51-54). In an
off-grid system with 3 days of autonomy, essentially all energy flows through the battery,
so battery charge/discharge round-trip efficiency (typically ~90-95% for LiFePO4) is also
a real loss between panel output and delivered load — but GT-2 explicitly does not list
it, and no other GT accounts for it. The chain therefore under-sizes the panel array
relative to its own stated loss model. This is a substantive correctness gap in an example
whose stated success criterion (lines 22-23) is "Every sizing number traces to a named
ground truth — no number is introduced without an antecedent."
**Fix:** Either add battery round-trip efficiency to GT-2's enumerated loss list (and note
0.80 already bundles it, making the factor internally complete), or add a separate GT for
round-trip efficiency and fold it into the chain. As written, the loss accounting is
incomplete against the chain's own claim of completeness.

## Info

### IN-01: Inconsistent presence of the explanatory preamble paragraph

**File:** `first-principles-thinking/examples/product-business.md:1-2`
**Issue:** `software-systems.md`, `personal-general.md`, and `science-engineering.md` each
open with an italic/plain preamble paragraph between the H1 and `## 1. Problem Essence`
describing what the example demonstrates and noting "Authored in Phase 5."
`product-business.md` jumps straight from the H1 to `## 1. Problem Essence` with no
preamble. For a calibration set, the structural inconsistency is a minor blemish.
**Fix:** Add a one-line preamble to `product-business.md` matching the other three, or
remove the preambles from the other three for uniformity.

### IN-02: "Essence Statement" capitalized as a proper artifact name but examples use the heading "Problem Essence"

**File:** `first-principles-thinking/examples/software-systems.md:281,300` and `first-principles-thinking/examples/product-business.md` (Section 1)
**Issue:** `software-systems.md` line 281 and 300 refer to "the Essence Statement" as a
named artifact ("stated in the Essence Statement"). `SKILL.md:44` does define the Phase 1
artifact as "Essence Statement", but the section heading in every example and in the
template is "Problem Essence". A reader is left to infer that "the Essence Statement" lives
inside the "Problem Essence" section. Minor, but the examples could make the mapping
explicit since they are calibration material.
**Fix:** On first use in each example, write "the Essence Statement (Section 1, Problem
Essence)" or consistently use one term.

### IN-03: Section 6 of personal-general re-derives the effective-compensation figure rather than synthesizing it

**File:** `first-principles-thinking/examples/personal-general.md:97`
**Issue:** Section 6 step 3 restates "the effective compensation figure from Chain 1
($50,000–$52,000)" and "The ~$18,000 annual cost differential" — this is acceptable
synthesis, but the document elsewhere (Chain 1, line 60) says "roughly $18,000/year before
accounting for other SF cost differences." Section 6 presents ~$18,000 as the firm
differential without the "before accounting for other costs" caveat that Chain 1 attached.
Minor inconsistency in how confidently the figure is stated between sections.
**Fix:** Carry the same caveat phrasing into Section 6, or drop it from Chain 1 if the
$18,000 is meant to be the operative figure.

### IN-04: Abandoned Reasoning count differs across examples without explanation

**File:** `first-principles-thinking/examples/product-business.md:72-78`
**Issue:** `software-systems.md` documents two dead ends, `science-engineering.md` one,
`personal-general.md` one, `product-business.md` one. This is legitimate (dead ends are
problem-specific), but the software-systems example's preamble (line 4) explicitly promises
"at least one abandoned reasoning path" while the others' preambles do not set expectations.
Not a defect, but the calibration set would be stronger if at least one example
demonstrated the `Nothing material here — [reason]` escape valve from `output-template.md:130-132`,
since no example currently shows it.
**Fix:** Consider adding a fifth note or adjusting one example to demonstrate the escape
valve, since it is a documented part of the format that the examples otherwise never model.

### IN-05: GT-5? notation rendering — verify "GT-5?" is intended literally including the question mark in the ID

**File:** `first-principles-thinking/examples/science-engineering.md:66,96,116`
**Issue:** The example uses `GT-5?` as the literal ground-truth identifier including the
`?`. This matches `output-template.md:85` and `SKILL.md:142`, so it is correct. Flagging
only to confirm: the chain headers (lines 96, 116) and confidence lines use `GT-5?`
consistently. One spot, line 39 (Assumptions Table) refers to "GT-5? notation" while line
66 introduces the actual `GT-5?` entry — the forward reference in the assumptions table
to a GT that does not exist yet at that point in the document is slightly awkward but
consistent with how IDs are assigned. No change required; documented for completeness.
**Fix:** None required — notation is correct per the template.

### IN-06: software-systems Conclusion A says "no architectural change is needed" then Conclusion B/C develop an architectural change

**File:** `first-principles-thinking/examples/software-systems.md:87-96,106-121`
**Issue:** Conclusion A's intermediate states "no architectural change is needed to achieve
that outcome" (referring to the 8-minute-deploy outcome). Conclusion B and Section 6 step 3
then recommend schema decomposition, which Conclusion B itself calls a coupling change
("schema decomposition is a prerequisite of ... a microservices migration"). The two are
reconcilable (schema decomposition is conditional on profiling per Section 6), but a reader
calibrating rigor may read A and B as in tension. The phrasing "no architectural change is
needed" is absolute where the analysis actually means "no architectural change is needed
*for the deploy-frequency bottleneck specifically*."
**Fix:** Tighten Conclusion A's wording to scope the claim to the deploy-frequency
bottleneck, so it does not appear contradicted by Conclusion B.

### IN-07: Heading hierarchy and Markdown structure are clean — no broken links

**File:** all four files
**Issue:** Confirmed: each file has a single H1, six `## N.` section headings in fixed
order, `###` subheadings for chains/dead-ends. No internal cross-reference links exist
within the example files to break, and `SKILL.md:173-176` links to all four files with
correct relative paths matching the actual filenames. Tables are well-formed. No fenced
code block is missing a language tag except the chain pseudo-blocks (lines using ``` for
the chain illustration in `software-systems.md:156-161`), which is consistent with how
`SKILL.md` and `output-template.md` render chains — acceptable.
**Fix:** None required — recorded as a positive confirmation.

---

_Reviewed: 2026-05-17_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
