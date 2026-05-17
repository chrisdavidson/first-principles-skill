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
