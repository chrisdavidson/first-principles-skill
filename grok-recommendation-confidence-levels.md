**Deep Dive: P1 — HIGH confidence chains that consume unverified ground truths (`GT-N?`)**

### What P1 actually is

P1 is a violation of the **Unverified input rule (D-07)**:

> A chain that includes any `GT-N?` input must end with a MEDIUM or LOW confidence line.  
> The line must name the unverified input and state what verification would raise confidence to HIGH.  
> **A HIGH confidence claim cannot rest on an unverified ground truth.**

This rule appears in two canonical places:

- `output-template.md` (right under the chain template)
- `validation-rubric.md` Criterion 5 Rigorous / Sound descriptors

In the demo run, two chains violated it:

| Chain | Label | Head | Status |
|-------|-------|------|--------|
| C1    | **HIGH** | `GT-1 + GT-9?` | Violated |
| C7    | **HIGH** | `GT-2 + GT-4 + GT-13?` | Violated |
| C3, C5, C6 | MEDIUM (correctly) | contained `?` inputs | Compliant |

The agent *understood* the rule — it correctly demoted other chains — but failed to apply it consistently on two chains. That inconsistency is the core problem.

### Why this matters for first-principles reasoning

First-principles analysis is only as strong as its weakest load-bearing input. Confidence is not a decorative label; it is a **propagation property** of the derivation graph.

When a model labels a chain HIGH while it still depends on a `GT-N?`:

1. It breaks the epistemological contract of the methodology.
2. Downstream conclusions (especially the final decision chain) inherit false certainty.
3. The Self-Audit Gate becomes unreliable, because Criterion 5’s strongest checks live inside the Rigorous/Sound band descriptors. If the model invents its own vocabulary (“PRESENT”) or skips the real checks, the gate reports a false pass.
4. It trains the model (and future readers) that “mostly verified” is good enough for HIGH — which is the opposite of first-principles discipline.

In short: consistency of confidence assignment is not a formatting nicety. It is the mechanism that keeps the derivation chains honest.

### Why the model fails this (even when it “knows” the rule)

From the demo and the surrounding methodology, the failure modes are predictable:

1. **Local vs. global attention**  
   The model correctly applies D-07 when the `?` is salient in the head it is currently writing. When the head is more complex or the chain feels “mostly solid,” it drifts into holistic judgment (“this chain is strong overall”) instead of the strict token-level rule.

2. **Post-hoc rationalization**  
   Once the model has already decided a conclusion is important, it is biased toward protecting its confidence label. Demoting to MEDIUM feels like weakening the analysis.

3. **Missing forced intermediate step**  
   There is currently no explicit “confidence assignment checklist” that must be emitted before the `**Confidence:**` line. The rule exists, but the process does not force the model to *look* at every input identifier in the head immediately before choosing the label.

4. **Asymmetric cost**  
   Writing HIGH is cheap and feels assertive. Writing MEDIUM + remediation text requires extra work and looks more tentative. Models optimize for the cheaper, more confident-looking output unless the prompt makes the cheaper path invalid.

5. **Composition blindness** (related to P2)  
   Even when individual chains are correct, the model does not yet treat confidence as transitive through chain-on-chain composition. P1 is the simpler case of the same deeper issue.

### Practical tips to mold the model toward consistency

These are ordered from highest leverage / lowest cost to more structural changes.

**1. Force an explicit confidence pre-check (highest leverage, one paragraph)**

Add a short, mandatory process step right before any `**Confidence:**` line is written. Something like:

```text
Before writing the **Confidence:** line for any chain, emit a one-line pre-check:
  Inputs: [list every GT-N / GT-N? / Cn in the head]
  Contains GT-N?: [yes/no]
  → Label must be: [HIGH only if no GT-N?; else MEDIUM or LOW]
Then write the Confidence line. Do not skip the pre-check.
```

This turns a latent rule into an explicit, local, hard-to-skip action. Models obey local, just-in-time checklists far better than distant global rules.

**2. Make the remediation text non-optional and formulaic**

Require the exact shape:

```text
**Confidence:** MEDIUM
Unverified input: GT-9? (reason). Verification that would raise to HIGH: [specific action].
```

When the format is rigid, the model is less likely to omit the demotion. The current template already asks for this; making the wording even more formulaic helps.

**3. Elevate the rule into the Self-Audit Gate’s self-audit scan**

The existing self-audit scan (Table 1) already walks every chain head. Add one column:

```text
| Chain | ... | Contains GT-N? | Confidence label | D-07 compliant? |
```

Then require the model to mark any non-compliant row and fix it before the gate can clear. This re-uses an existing process artifact instead of inventing a new one.

**4. Add a short “confidence is transitive” reminder next to D-07**

Even before full P2 language lands, a single sentence helps:

> Confidence is a property of the entire head. If any input is `GT-N?` or is itself a MEDIUM/LOW chain, the derived chain cannot be HIGH.

This starts training the composition intuition that P2 formalizes.

**5. Negative examples in the body or worked examples**

Show one short counter-example:

```text
# Non-conforming (do not do this)
GT-1 + GT-9? → ... → conclusion
**Confidence:** HIGH   ← violates D-07

# Conforming
GT-1 + GT-9? → ... → conclusion
**Confidence:** MEDIUM
Unverified input: GT-9?. Verification that would raise to HIGH: open the source and confirm the figure on p. 14.
```

Models learn constraints better from contrast than from positive rules alone.

**6. Make the Self-Audit Gate’s Criterion 5 scoring impossible to fake**

The review already showed that inventing “PRESENT” let the gate report a false pass. The recent body changes (explicit Read of the rubric + “do not score from recollection”) are the right direction. Reinforce it by requiring the model to quote the exact D-07 sentence or the Rigorous descriptor when scoring Criterion 5.

**7. Longer-term apparatus support (from the review’s H1)**

Once the detector has columns for `high_conf_unverified_head` and `confidence_inversions`, you can measure compliance on every run instead of relying on occasional manual review. That feedback loop is the only reliable way to keep the model honest over many iterations.

### Suggested minimal prompt patch (product side)

The single highest-ROI change is still the one the review recommended for R1, but specialized for confidence:

In the Phase 4 / Derivation Chains section (or immediately before the Confidence line template), add:

> **Confidence assignment rule (mandatory)**  
> Immediately before writing any `**Confidence:**` line, list every identifier in the chain head.  
> If the list contains any `GT-N?`, the label **must** be MEDIUM or LOW and the line must name the input and the verification that would raise it.  
> A HIGH label is only legal when every input is an unsuffixed `GT-N` or a HIGH chain.  
> This check is local to the chain being written; do not rely on a later global audit to catch it.

This keeps the rule close to the moment of decision — exactly where the model currently drifts.

---

**Summary**

P1 is not a minor formatting slip. It is a direct failure of the confidence-propagation contract that makes first-principles chains trustworthy. The model already knows the rule in the abstract; the failure is in consistent, local application under cognitive load.

The most effective molding techniques are:

1. Force a just-in-time pre-check right before the Confidence line.
2. Make the remediation text rigid and non-skippable.
3. Surface the check inside the existing self-audit scan.
4. Eventually make the violation mechanically detectable (H1).

Would you like me to draft the exact paragraph(s) that could be inserted into `SKILL-body.md` and/or `output-template.md` to implement the highest-leverage fixes?