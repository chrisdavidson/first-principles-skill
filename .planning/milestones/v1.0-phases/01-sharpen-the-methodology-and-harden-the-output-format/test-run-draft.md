# Test Run (Draft) — First Principles Analysis

> **Status:** Working draft (D-09). This file dogfoods the methodology in
> `methodology.md` against the output shape in `output-template.md`. It is a
> Phase 1 verification artifact and is **not** a shipped `examples/` file —
> Phase 5 may later polish it into one.
>
> **Subject (D-08):** A genuinely unresolved design question from this skill
> build — candidate (c) from `01-RESEARCH.md` Open Question 3. The 4-type
> classification scheme was adopted by discussion (decision D-06); whether it
> survives a rigorous first-principles re-derivation was *not* settled. That is
> what this run tests.

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
| A1: Every real assumption falls cleanly into exactly one of the four types. | untested belief | verify, or flag unverified | **Discard** | False. Counterexample constructed below (→ GT-3): a single assumption that is simultaneously a convention and an untested belief. |
| A2: The classification scheme exists to *select a treatment*, not merely to label. | convention (stated design principle) | challenge before use | **Accept** | `methodology.md` Phase 2: "Classification drives the method — it is not merely labelling." Holds in this context. Promoted to GT-2. |
| A3: Each of the four types maps to a distinct, non-substitutable treatment. | convention (design of the scheme) | challenge before use | **Accept** | `methodology.md` Phase 2 treatment table — four treatments, none interchangeable. Promoted to GT-1. |
| A4: Adding a category to a classification scheme is cost-free. | untested belief | verify, or flag unverified | **Discard** | False. A fifth category enlarges Phase 2's exit-criterion surface and adds a routing decision to every assumption. Not free. |
| A5: A multi-type assumption can be rewritten as single-type component assumptions. | untested belief | verify | **Accept** | Demonstrated on the GT-3 counterexample below — it splits cleanly into one convention and one untested belief. Promoted to GT-5. |
| A6: Authors will reserve a catch-all "mixed" category strictly for genuinely unclassifiable assumptions. | untested belief | flag unverified (D-07) | **Challenge** | Cannot be verified — no usage data exists for an unbuilt scheme. Carried forward as the unverified ground truth GT-6?. |

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

GT-2 (the scheme's function is to select a treatment for each assumption)
+ GT-4 (a "mixed" category names the absence of a type, not a treatment)
→ an assumption placed in a "mixed / uncertain" category reaches the end of
Phase 2 without any of the four prescribed treatments being selected — it exits
classification *untreated*
→ adding a fifth "mixed / uncertain" category creates a classification outcome
that does not drive a treatment, which directly contradicts the scheme's stated
purpose.

**Confidence:** HIGH — both inputs (GT-2, GT-4) are verified.

### Conclusion: The four-type scheme as written has a real gap — it is silent on multi-type assumptions.

GT-1 (four types, four distinct treatments)
+ GT-3 (real assumptions span more than one type simultaneously)
→ when an assumption spans, e.g., convention + untested belief, the scheme
offers two applicable treatments and *no rule* for choosing between them or
combining them — the analyst is left to improvise, and Phase 2's exit criterion
("every assumption is classified") gives no guidance on the multi-type case
→ the four-type scheme has a genuine gap: it does not tell the analyst what to
do with a multi-type assumption. This gap is the real problem the proposed fifth
category was reaching for.

**Confidence:** HIGH — both inputs (GT-1, GT-3) are verified.

### Conclusion: The gap should be closed with a decomposition rule, not a fifth category.

GT-5 (a multi-type assumption can be split into single-type components)
+ GT-4 (a "mixed" category names the absence of a treatment)
→ decomposing a multi-type assumption into single-type component assumptions
routes *each component* to exactly one of the four existing prescribed
treatments — this closes the gap identified above without ever producing the
untreated-outcome defect of a "mixed" category
→ the methodology should keep four types and add a decomposition rule — "an
assumption that spans multiple types is split into single-type component
assumptions, each classified and treated separately" — rather than adding a
fifth category.

**Confidence:** HIGH — inputs GT-5 and GT-4 are verified; the chain consumes no
`GT-N?` input.

### Conclusion: The fifth category fails on structural grounds regardless of how disciplined its users are.

GT-6? (authors would reserve a catch-all category strictly, using it as intended)
+ GT-4 (a "mixed" category names the absence of a treatment)
→ even granting the most favorable assumption about author behavior, an
assumption placed in the catch-all *still* exits Phase 2 without a treatment —
disciplined usage does not repair the structural defect, it only limits how
often the defect is triggered
→ the fifth category fails on its own structural terms whether or not its users
are disciplined; the behavioral misuse risk is a secondary aggravator, not the
deciding factor.

**Confidence:** MEDIUM — this chain consumes GT-6?, an unverified behavioral
prediction. The conclusion holds at MEDIUM because the structural argument
(GT-4) carries it independently of GT-6?. Verification that would raise it to
HIGH: observing real analyses authored under a fifth-category scheme and
measuring whether the catch-all is used as intended. Until such usage data
exists, GT-6? stays flagged.

---

## 5. Abandoned Reasoning

### Dead End: Encode confidence gradations into the type taxonomy

**What was tried:** Before weighing a fifth category, an earlier path was to make
the scheme *more granular* by splitting "untested belief" into
"untested-but-plausible" and "untested-and-doubtful" — reasoning that confidence
varies within that type and the scheme should capture it.

**Why abandoned:** This conflates classification with machinery that already
exists. Confidence is recorded twice already — per assumption in the **Verdict**
column, and per conclusion in the Derivation Chains **Confidence** line
(HIGH/MEDIUM/LOW). Folding confidence into the *type* duplicates an existing
mechanism and makes both axes harder to check. The path contradicts no ground
truth, but it fails the scheme's purpose (GT-2): the type's job is to select a
treatment, and confidence does not change which treatment an untested belief
needs — it is still "verify, or flag."

**What it ruled out:** It rules out any future proposal to encode confidence
levels into the type column. Confidence belongs in Verdict and in the chain
Confidence line — never in Type.

### Dead End: Drop classification entirely and "just verify everything"

**What was tried:** A more radical path — if multi-type assumptions are awkward,
perhaps the type scheme itself is the problem; replace classification with one
flat rule, "verify every assumption."

**Why abandoned:** This contradicts GT-1 and GT-2 directly. The four treatments
are not interchangeable: a physical law cannot be empirically "verified" in the
sense an untested belief is, and a current constraint needs its *expiry
conditions* recorded rather than a verification. "Verify everything" collapses
four distinct, non-substitutable treatments into one that is simply wrong for
three of the four types.

**What it ruled out:** It rules out treating classification as optional
overhead that could be flattened to a universal rule. The four treatments are
irreducibly different, so the scheme cannot be removed — only refined.

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
