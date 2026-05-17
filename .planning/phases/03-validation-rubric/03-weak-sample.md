# Weak Sample (Draft) — First Principles Analysis

> **Status:** Deliberately-weak verification artifact (D-04). This file is a
> Phase 3 verification artifact for the validation rubric in
> `first-principles-thinking/references/validation-rubric.md`. It is **not** a
> shipped `examples/` file and is **not** embedded in the rubric itself — it
> lives under `.planning/` and is never installed with the skill.
>
> **Purpose:** It is a deliberately-degraded copy of
> `01-.../test-run-draft.md` (a passing-quality analysis of the same subject).
> Three named rigor failures are injected so the rubric's fail behavior can be
> demonstrated against a real analysis attempt rather than a blank document:
>
> - **Injection 1 (Criterion 4):** the Derivation Chains are flattened — every
>   chain runs straight from the GT-pair to the conclusion with no intermediate
>   step.
> - **Injection 2 (Criterion 2):** the Assumptions Table is stripped of
>   four-type classification — Type cells read "general assumption" and the
>   Verdict / Verification cells are generic or empty.
> - **Injection 3 (Criterion 4, escape-valve abuse per D-08):** the Abandoned
>   Reasoning section's two documented dead ends are replaced with one generic
>   line.
>
> The `## 1. Problem Essence`, `## 3. Ground Truths`, and `## 6. Conclusion`
> sections are preserved intact so the rubric must catch subtle within-section
> failures, not mere emptiness.

---

## 1. Problem Essence

**Core problem:** Should the assumption-classification scheme keep exactly four
types (physical law / current constraint / convention / untested belief), or add
a fifth "mixed / uncertain" category for assumptions that do not fit one type?

**Success criteria:**

- The chosen scheme assigns every real assumption a classification that routes
  it to a *concrete prescribed treatment* — a reader can check that no
  assumption exits Phase 2 untreated.
- The scheme does not create any classification outcome that labels an
  assumption without directing what to do with it.
- Phase 2's exit criterion stays mechanically checkable: "every assumption is
  classified and has a recorded verdict" must remain a yes/no test.

---

## 2. Assumptions Table

These are the assumptions *this analysis* rests on — meta-assumptions about the
classification scheme itself.

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| A1: Every real assumption falls cleanly into exactly one of the four types. | general assumption | look into it | | unsure |
| A2: The classification scheme exists to *select a treatment*, not merely to label. | general assumption | look into it | possibly true | |
| A3: Each of the four types maps to a distinct, non-substitutable treatment. | general assumption | | possibly true | unsure |
| A4: Adding a category to a classification scheme is cost-free. | general assumption | look into it | | |
| A5: A multi-type assumption can be rewritten as single-type component assumptions. | general assumption | | possibly true | unsure |
| A6: Authors will reserve a catch-all "mixed" category strictly for genuinely unclassifiable assumptions. | general assumption | look into it | | possibly true |

---

## 3. Ground Truths

- **GT-1** `methodology.md` Phase 2 assigns each of the four types a distinct,
  specific prescribed treatment (accept as ground-truth candidate / record
  expiry conditions / explicitly challenge / verify-or-flag). — source:
  `methodology.md` Phase 2, "The four assumption types and their prescribed
  treatments" table.
- **GT-2** The scheme's stated function is to *select a treatment* for each
  assumption — classification drives the method. — source: `methodology.md`
  Phase 2 Operation, "Classification drives the method — it is not merely
  labelling."
- **GT-3** Real assumptions exist that draw on more than one type at once.
  Concrete instance: "users will accept a CLI-only tool" is *both* a convention
  (CLI-only is an adopted interface practice) *and* an untested belief
  (acceptance has not been measured). — source: direct construction; the two
  type-definitions in `output-template.md` both apply to the one sentence.
- **GT-4** A "mixed / uncertain" category is *defined* as "does not fit a single
  type." By that definition it names the *absence* of a clear type — it does not
  itself name any treatment. — source: definitional, from the proposed
  category's own description.
- **GT-5** A multi-type assumption can be rewritten as a set of component
  assumptions, each single-type. The GT-3 instance splits into: "CLI-only is the
  correct interface convention here" (convention) + "users will accept whatever
  interface this tool ships" (untested belief). — source: direct construction.
- **GT-6?** Authors given a catch-all category will reserve it strictly for
  genuinely unclassifiable assumptions, rather than defaulting to it under time
  pressure. — unverified: this is a behavioral prediction about a scheme that
  does not yet exist; no usage data can be collected for it in this analysis.

---

## 4. Derivation Chains

### Conclusion: A fifth "mixed / uncertain" category cannot satisfy the scheme's own stated purpose.

GT-2 + GT-4 → adding a fifth "mixed / uncertain" category cannot satisfy the
scheme's own stated purpose.

**Confidence:** HIGH — both inputs (GT-2, GT-4) are verified.

### Conclusion: The four-type scheme as written has a real gap — it is silent on multi-type assumptions.

GT-1 + GT-3 → the four-type scheme has a real gap: it is silent on multi-type
assumptions.

**Confidence:** HIGH — both inputs (GT-1, GT-3) are verified.

### Conclusion: The gap should be closed with a decomposition rule, not a fifth category.

GT-5 + GT-4 → the gap should be closed with a decomposition rule, not a fifth
category.

**Confidence:** HIGH — both inputs (GT-5, GT-4) are verified.

### Conclusion: The fifth category fails on structural grounds regardless of how disciplined its users are.

GT-6? + GT-4 → the fifth category fails on structural grounds regardless of how
disciplined its users are.

**Confidence:** MEDIUM — this chain consumes GT-6?, an unverified input.

---

## 5. Abandoned Reasoning

Nothing material here — no dead ends were encountered.

---

## 6. Conclusion

**Recommended approach:** Keep the four-type classification scheme. Add a
**decomposition rule** to Phase 2: an assumption that genuinely spans multiple
types is not given a new category — it is split into single-type component
assumptions, each classified and treated separately. Do **not** add a fifth
"mixed / uncertain" category.

**Key insight:** The fifth-category proposal correctly identified a *real* gap —
the four-type scheme is genuinely silent on multi-type assumptions (Conclusion
2) — but proposed a fix that defeats the scheme's purpose, because a "mixed"
classification names the absence of a treatment rather than a treatment
(Conclusion 1). The non-obvious finding is that the correct fix is structurally
different from *both* options that were on the table: not "four types unchanged"
and not "five types," but "four types plus a decomposition rule." The binary
framing of the original question — *add a category, yes or no?* — would have
hidden this answer entirely. This is exactly the failure mode the methodology
exists to catch: a question framed as a two-way choice when the real answer is a
third structure neither option contained.

**Trade-offs acknowledged:** The decomposition rule adds work to Phase 2 — the
analyst must actively split multi-type assumptions instead of reaching for a
catch-all, and Phase 2's exit criterion grows slightly more demanding (every
*component*, not merely every assumption, must be classified). That cost is
accepted deliberately: it is the price of keeping every classification outcome
treatment-bearing, which Success Criterion 1 of this analysis requires.

**Confidence:** MEDIUM. The core recommendation rests on Conclusions 1–3, which
are all HIGH and depend on no unverified input. The MEDIUM rating is carried in
solely by Conclusion 4, whose chain consumes **GT-6?** — an unverified
behavioral prediction about how authors use a catch-all category. Conclusion 4
is not load-bearing for the recommendation: even if GT-6? turned out false (or
true), Conclusions 1–3 still stand and the recommendation is unchanged.
Verification that would raise overall confidence to HIGH: usage data from real
first-principles analyses authored under a fifth-category scheme, showing
whether the catch-all is used as intended. Until that data exists, GT-6? stays
flagged and the conclusion is reported at MEDIUM — honestly, rather than
inflated to HIGH on a chain that contains an unverified link.

---

> **Injected failures (for the scorer).** This artifact carries exactly three
> deliberate rigor failures, mapped to the rubric criteria they are designed to
> trip:
>
> - **Injection 1 → Criterion 4 (Reason Upward).** Every chain in
>   `## 4. Derivation Chains` is flattened: each runs `GT-N + GT-M → conclusion`
>   with the intermediate-claim line removed. The intermediate step is where the
>   reasoning happens — its absence is the defect.
> - **Injection 2 → Criterion 2 (Challenge Assumptions).** Every Type cell in
>   `## 2. Assumptions Table` reads "general assumption" — a freeform label
>   outside the four-type scheme (physical law / current constraint / convention
>   / untested belief). Verdict and Verification cells are generic ("possibly
>   true", "unsure") or empty.
> - **Injection 3 → Criterion 4 (Reason Upward), escape-valve abuse (D-08).**
>   `## 5. Abandoned Reasoning` replaces two documented dead ends with the single
>   generic line "Nothing material here — no dead ends were encountered." — a
>   reason that could be copy-pasted to any analysis without alteration.

---

## Rubric Scoring Run

This run applies `first-principles-thinking/references/validation-rubric.md` to
the weak analysis above — all six criteria, in methodology-phase order, each
producing one verdict block in the rubric's prescribed format (D-07). Sections
that score `Absent` use the D-09 gap-citation variant only when the named
artifact is missing or empty; the Assumptions Table here is present-but-broken,
so it is scored with a quoted span.

### Criterion 1: Identify Essence

**Quoted span:** "Should the assumption-classification scheme keep exactly four
types (physical law / current constraint / convention / untested belief), or add
a fifth 'mixed / uncertain' category for assumptions that do not fit one type?"
followed by three success criteria including "Phase 2's exit criterion stays
mechanically checkable: 'every assumption is classified and has a recorded
verdict' must remain a yes/no test."

**Band:** Rigorous

**Justification:** The Essence Statement is a single sentence naming the core
decision (not a symptom or a prompt restatement), and each success criterion is
a checkable condition a reader could verify against the final conclusion without
asking the analyst for clarification — the Rigorous descriptor for this criterion.

### Criterion 2: Challenge Assumptions

**Quoted span:** "| A1: Every real assumption falls cleanly into exactly one of
the four types. | general assumption | look into it | | unsure |" — and every
other row likewise carries the Type value "general assumption".

**Band:** Absent

**Justification:** The table exists with populated rows, but every row's Type
cell reads "general assumption" — a freeform label with no mapping to the
four-type scheme (physical law / current constraint / convention / untested
belief) — which is exactly the Absent descriptor: the table is a list of
undifferentiated claims rather than a classified set.

### Criterion 3: Establish Ground Truths

**Quoted span:** "GT-1 `methodology.md` Phase 2 assigns each of the four types a
distinct, specific prescribed treatment ... — source: `methodology.md` Phase 2,
'The four assumption types and their prescribed treatments' table." and "GT-6?
... — unverified: this is a behavioral prediction about a scheme that does not
yet exist."

**Band:** Rigorous

**Justification:** Every GT carries a stable identifier that matches the IDs
referenced in the Derivation Chains, every verified GT has a source citation
more specific than "common knowledge", and the one unverified entry carries the
`?` suffix (GT-6?) — the Rigorous descriptor for this criterion.

### Criterion 4: Reason Upward

**Quoted span:** "GT-2 + GT-4 → adding a fifth 'mixed / uncertain' category
cannot satisfy the scheme's own stated purpose." (every chain in section 4 is
flattened identically), and the section 5 body in full: "Nothing material here —
no dead ends were encountered."

**Band:** Hand-wavy

**Justification:** Every chain runs straight from its GT-pair to its conclusion
with no intermediate claim (the Sound descriptor — "the chain goes directly from
GT-IDs to conclusion"), and the Abandoned Reasoning section uses the honest-depth
escape valve with a reason that would apply equally to any analysis (the
Hand-wavy descriptor for escape-valve abuse) — the lower of the two applicable
bands governs, so this criterion scores Hand-wavy. It is not Absent: derivation
chains are present for every conclusion, so the rubric's Absent descriptor
("no derivation chains exist") does not apply.

### Criterion 5: Validate

**Quoted span:** "**Confidence:** MEDIUM — this chain consumes GT-6?, an
unverified input." (the confidence line on the only chain consuming a `GT-N?`
input).

**Band:** Sound

**Justification:** Confidence ratings are present on every chain, the GT-6?
input is named in its chain's confidence line, and no chain consuming a `GT-N?`
input is rated HIGH — but the flattened chains expose no weakest-link analysis
and the per-chain caveat does not state what verification would raise confidence
to HIGH, so the criterion falls one identifiable step short of Rigorous.

### Criterion 6: Conclusion-to-Ground-Truth Traceability

**Quoted span:** "The decomposition rule adds work to Phase 2 ... and Phase 2's
exit criterion grows slightly more demanding (every *component*, not merely
every assumption, must be classified)."

**Band:** Sound

**Justification:** Every Conclusion claim maps to a `### Conclusion:` chain
heading in section 4 and the Key Insight names a genuinely non-obvious finding,
but the trade-off elaboration quoted above is developed only in section 6 — the
flattened chains are too bare to contain it — which is the Sound descriptor:
one claim is introduced for the first time in the Conclusion section.

## Overall Verdict

**FAIL.**

**Rule fired — the gate.** Criterion 2 (Challenge Assumptions) scores Absent.
The rubric's gate states: any criterion scored Absent fails the entire analysis,
regardless of how all other criteria score. Criterion 2 alone is therefore
sufficient to fail this analysis.

**Cap not triggered.** Exactly one criterion (Criterion 4, Reason Upward) scores
Hand-wavy. The hand-wavy cap fails an analysis only at two or more Hand-wavy
criteria; one isolated Hand-wavy is tolerated. The cap does not fire here — the
FAIL stands entirely on the gate. (Reported honestly: the precision of the
rubric is part of what is being demonstrated — it does not over-fire the cap on
a single weak section.)

**Score distribution:** Rigorous ×3 (Criteria 1, 3), Sound ×2 (Criteria 5, 6),
Hand-wavy ×1 (Criterion 4), Absent ×1 (Criterion 2). Two criteria score below
Sound — one Absent (gate) and one Hand-wavy — so the analysis is decisively
below the pass bar (every criterion Sound or above, at most one Hand-wavy).

**Disposition:** This analysis must be revised before its conclusions could be
presented. The required fixes are localized and named by the verdict blocks:
restore four-type classification to every Assumptions Table row (Criterion 2),
re-insert the intermediate claim into every derivation chain (Criterion 4), and
replace the generic Abandoned Reasoning line with the actual documented dead
ends (Criterion 4).

**Phase 3 Success Criterion 4 satisfied.** Applying the authored rubric to a
deliberately-weak analysis produced an overall fail, localized to specific
quoted spans per criterion — the rubric catches hand-waving rather than
certifying it.
