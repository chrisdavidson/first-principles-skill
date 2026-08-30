---
name: fishbone
description: Runs a focused fishbone only — breadth-first cause-category map. Invoke via /fishbone only.
disable-model-invocation: true
metadata:
  version: "8.20.0"
license: MIT
---
<!-- DO NOT EDIT — generated from shared/skills/fishbone/SKILL.md by sync-content.py -->

# Focused Fishbone Mode

You are running in focused-fishbone mode. Execute the procedure below, produce
its canonical output sections, then run the focused-mode validation step below —
do not run the full 5-phase first-principles analysis. Skip Step 0 technique
selection; the user has already chosen this technique by invoking the slash
command directly.

## When to reach for this

Use a fishbone diagram when the problem has multiple interacting causes with no single
traceable causal chain — you need breadth across the cause space, not depth into one chain.

**Good fit:** multiple plausible contributing factors exist across different areas; the
problem recurs despite surface fixes and the cause is unclear; you need a structured way
to ensure no category of cause is overlooked before narrowing focus.

**Not a good fit:** the problem has a single traceable causal chain and you need to drill
to the root cause — that calls for a [5-Whys](${CLAUDE_PLUGIN_ROOT}/skills/five-whys/SKILL.md) analysis instead, which is a
depth-first root-cause drill down one causal chain rather than a breadth-first map across
categories.

---

## Cause categories

The category set is chosen once, before brainstorming begins. Two paths: use the
domain-neutral default set, or select a named preset that matches your domain. The
decision rule below maps domain signals to the recommended choice.

### Default category set

The domain-neutral default covers most situations cleanly. Use it when no preset
row in the table below clearly matches your domain.

| Category | What it covers |
|----------|----------------|
| **People** | Human contributors — skills, behaviours, training, workload, decision-making |
| **Process** | Methods, procedures, workflows, sequences of steps |
| **Technology & Tools** | Equipment, software, instruments, physical tools, infrastructure |
| **Environment** | Physical surroundings, conditions, constraints imposed by the setting |
| **Information** | Data quality, availability, communication, documentation, reporting |
| **Resources** | Materials, budget, time, capacity, supply inputs |

### Named presets

Use a named preset when your domain maps cleanly to an established category vocabulary.
Each preset's category list is fixed — do not rename or merge categories mid-analysis.

**6M** (manufacturing / operations):
Machine, Method, Material, Measurement, Man (People), Mother Nature (Environment).
Use when analysing a production or operations process with physical machinery and
materials at the centre.

**8P** (service / marketing):
Product, Price, Place, Promotion, People, Process, Physical Evidence, Productivity.
Use when the problem sits inside a service delivery or marketing context where the
customer experience and offer design are the relevant axes.

**4S** (service delivery):
Surroundings, Suppliers, Systems, Skills.
Use when the problem is a service-delivery failure and a compact four-category lens
is sufficient — typically a narrower operational scope than 8P.

### Decision rule

| Domain signal | Recommended category set | Note |
|---------------|--------------------------|------|
| Physical production line, factory floor, ops process with equipment | 6M | Machine and Measurement categories capture equipment and process-quality causes that the default set folds into Technology & Tools and Process |
| Service business — customer offer, channel, pricing, marketing mix | 8P | Covers the full service-marketing mix; too broad for narrowly scoped delivery failures |
| Service delivery operation — narrow scope, no marketing mix needed | 4S | Compact; suited to front-line service failures where offer design is not in scope |
| Software, knowledge work, cross-functional teams, research | Default (six categories) | Domain-neutral labels avoid manufacturing jargon; Technology & Tools and Information handle the technical axes cleanly |
| Unclear domain, or no preset row fits cleanly | Default (six categories) | The default set is always a valid fallback — prefer it over forcing a preset that does not fit |

The default set is always a valid fallback when no preset row clearly matches your
situation. Choosing a preset that does not fit the domain produces misleading category
labels and blank branches.

---

## Procedure

1. **Define the effect.** One sentence naming the observable problem to be explained —
   what is happening, not why. Do not name a suspected cause.

2. **Choose categories.** Pick the set by domain signal: **6M** (Machine, Method,
   Material, Measurement, Man, Mother Nature) for a physical production line; **8P**
   (Product, Price, Place, Promotion, People, Process, Physical Evidence, Productivity)
   for a service business with a marketing mix; **4S** (Surroundings, Suppliers, Systems,
   Skills) for a narrow-scope service-delivery operation; the **default six-category set**
   (People, Process, Technology and Tools, Environment, Information, Resources) for
   software, knowledge work, or when no preset fits cleanly — always a valid fallback.
   Lock the set now. Do not add, rename, or remove categories once brainstorming begins.

3. **Brainstorm causes.** For each category, generate candidate causes that could
   plausibly contribute to the effect, one category at a time. Do not evaluate
   or discard causes during this step — record everything.

4. **Identify sub-causes.** For any cause that is itself explained by a deeper cause,
   add a sub-cause beneath it. Two levels of nesting are typically enough; go deeper
   only where the extra depth changes what action is possible.

5. **Prioritise and verify.** Review the completed map, identify the branches most
   likely contributing based on available evidence, and mark unverified candidate
   causes explicitly. Select the highest-priority branches for evidence gathering or
   further depth analysis.

**Exit criterion:** Every category in the chosen set has been walked, each candidate
cause is attached to exactly one category, unverified candidate causes are explicitly
marked as unverified, and the highest-priority branches for evidence gathering or
further depth are named. A reader can tell which causes were tested and which are
still candidates.

**Read [fishbone-detail.md](references/fishbone-detail.md) when you need:**
- a worked example of this technique
- the failure modes and how to avoid them
- handoff guidance to another technique

## Focused-mode validation

**Check the output against its own completion condition before presenting it.** The
procedure above states one, in whichever form this technique uses — an exit criterion, a
stop test, or an output contract. Read that condition again and confirm the output actually
produced meets every requirement it names, not just the ones that were easiest to satisfy.

**This is a scope-proportionate check, not the six-criterion Self-Audit Gate.** That gate
scores a six-section analysis document; this run produced one technique's output sections,
not six, so walking all six criteria against it would score structure that was never
produced. The larger of the two components: a focused run does not acquire evidence — it
opens no cited source — so a claim resting on a source this run did not open stays marked
rather than being resolved as confirmed.

**Carry the mark forward.** Anything this run could not verify is carried into the output
marked with a `?` rather than dropped or silently asserted as fact.

**Revise once, then stop.** If the check fails, revise the output and check it again.
Revise at most one time. If it still fails after that pass, present the output with the
gap named rather than revising again.

**End every run with a validation line, without exception.** State exactly one of the
following, verbatim, never silently:

- `Focused-mode validation: satisfied`
- `Focused-mode validation: revised once, now satisfied`
- `Focused-mode validation: not satisfied - <reason>`

Close with the reason this line is unconditional: a silent run is indistinguishable from a
run that skipped the check.

---

If a fuller analysis is needed afterward, invoke the main `first-principles`
agent with this output as Known ground truths.
