# 5-Whys & Decompose (Root-Cause & Reduce-to-Primitives)

> Two co-equal recursive drills united in one technique: **causal recursion** — trace
> a recurring symptom back through its causal chain to an actionable corrective; and
> **structural reduction** — break a compound claim into its constituent facts until
> each branch bottoms out at a physical law, a definition, or a direct measurement.

---

- [When to reach for this](#when-to-reach-for-this)
- [Procedure](#procedure)
- [Stop test](#stop-test)

---

## When to reach for this

**Mode-selection rule (choose before starting):**

- **Causal mode (root-cause drill):** Use when a problem keeps coming back. You have an
  observable symptom, a surface fix has been tried, and you need to trace the causal
  chain to its actionable source. The question is *"Why does this symptom keep recurring?"*
  Stops when a branch reaches a specific corrective action within your practical control.

- **Reduce-to-primitives mode (irreducibility drill):** Use when you are holding a compound
  claim — a cost estimate, a performance promise, a design requirement, a qualitative
  conclusion — and you cannot tell whether the claim is solid or whether one of its hidden
  constituents is assumed. The question is *"What is this claim actually made of, and is THAT
  verified?"* Stops when each branch bottoms out at an irreducible primitive (physical law /
  definition / direct measurement).

**Trigger vocabulary for reduce-to-primitives mode (D-01a):** *"reduce to primitives"*,
*"what is X made of"*, *"irreducibility drill"*, *"irreducibility test"*,
*"break X into constituent parts"*, *"break X into constituent facts"*, *"decompose this
claim"*, *"decompose into primitives"*.

**Not a good fit for either mode:** the problem involves multiple interacting subsystems
with no single causal chain and no single compound claim to verify — that pattern calls for
a fishbone (Ishikawa) diagram instead, which maps causes across categories in parallel.

**Intra-technique vs. external boundary:**
- Causal vs. reduce-to-primitives is an *intra-technique* mode choice (both are this tool).
- Fishbone is an *external* cross-technique boundary: use it for causal breadth across
  cause categories, not causal depth or structural reduction.

A single analysis can use all three: apply reduce-to-primitives to verify the performance
claim, run the causal drill on the failure that prompted the analysis, and use a fishbone
to structure the initial hypothesis space.

---

## Procedure

### Causal mode (root-cause drill)

**State the symptom.** One sentence: the observable problem that keeps occurring — not a
suspected cause, the observable effect.

**Ask: Why did this happen?** List every cause you can identify without filtering.
Multiple causes at the first level are expected.

**For each cause, ask "What else caused this?" before descending into any one branch.**
Complete the lateral scan at a level before descending. Multiple valid causes each become
their own branch.

**Stop drilling a branch when BOTH hold:**
- You can state a specific corrective action that would prevent recurrence.
- That action is within your practical control.

A branch with no actionable corrective — a systemic constraint outside your control — is
still a real finding: record it and move to the next branch.

**Validate each causal link** with observable evidence, not inference; flag unevidenced
links as assumed.

### Reduce-to-primitives mode (irreducibility drill)

**State the claim.** One sentence naming the compound claim to verify.

**Identify its immediate constituents.** List every component fact, assumption, or parameter
the claim depends on. Complete the lateral scan at one level before descending.

**Apply the irreducibility test to each constituent.** Is it itself reducible? If yes,
recurse. If no, apply the stop test (see §Stop test).

**Record the verdict for each branch:**
- Passes stop test: `Verified — [physical law / definition / measurement]: <source>`.
- Fails stop test: `Assumed — unverified` → becomes GT-N? in Phase 3.

**Validate the parent claim.** Verified only if every branch is verified — one assumed
branch flags the whole parent with `?`.

**Read [five-whys-detail.md](five-whys-detail.md) when you need:**
- a worked example of this technique
- the failure modes and how to avoid them
- handoff guidance to another technique

---

## Stop test

Stop recursing a branch *only* when it bottoms out at one of these three irreducible anchors:

- **Physical law** — a law of thermodynamics, conservation law, Ohm's law, Planck's
  relation, Newton's laws, etc. The branch is irreducible because physics does not reduce
  further.
- **Definition** — a formal or conventional definition that is true by construction, e.g.
  "one kilowatt-hour = 3.6 MJ". Reducible no further because the definition terminates
  the chain.
- **Direct measurement** — an observation you can point to: a datasheet spec, a calibrated
  instrument reading, a published standard value with a traceable source. The branch stops
  because the fact is empirically anchored.

A branch that stops on a guess, an industry rule of thumb, or a vague recollection has
**not** passed the stop test — flag it as assumed.
