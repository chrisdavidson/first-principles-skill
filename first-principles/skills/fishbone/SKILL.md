---
name: fishbone
description: Runs a focused fishbone only — cause-category map for a multi-causal effect. Invoke via /fishbone only.
disable-model-invocation: true
metadata:
  version: "3.8.0"
license: MIT
---
<!-- DO NOT EDIT — generated from shared/skills/fishbone/SKILL.md by sync-content.py -->

# Focused Fishbone Mode

You are running in focused-fishbone mode. Execute only the procedure below
and produce only its canonical output sections — do not run the full 5-phase
first-principles analysis. Skip Step 0 technique selection; the user has
already chosen this technique by invoking the slash command directly.

## When to reach for this

Use a fishbone diagram when the problem has multiple interacting causes with no single
traceable causal chain — you need breadth across the cause space, not depth into one chain.

**Good fit:** multiple plausible contributing factors exist across different areas; the
problem recurs despite surface fixes and the cause is unclear; you need a structured way
to ensure no category of cause is overlooked before narrowing focus.

**Not a good fit:** the problem has a single traceable causal chain and you need to drill
to the root cause — that calls for a [5-Whys](five-whys.md) analysis instead, which is a
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

1. **Define the effect.** Write one sentence naming the observable problem — the effect
   to be explained. State what is happening, not why. Do not name a suspected cause.

2. **Choose categories.** Pick the category set by domain signal: use **6M** (Machine,
   Method, Material, Measurement, Man, Mother Nature) for a physical production line,
   factory floor, or ops process with equipment; use **8P** (Product, Price, Place,
   Promotion, People, Process, Physical Evidence, Productivity) for a service business
   with a customer offer, channel, pricing, and marketing mix; use **4S** (Surroundings,
   Suppliers, Systems, Skills) for a narrow-scope service-delivery operation with no
   marketing mix; use the **default six-category set** (People, Process, Technology and
   Tools, Environment, Information, Resources) for software, knowledge work,
   cross-functional teams, research domains, or when no preset fits cleanly. The default
   six-category set is always a valid fallback. Lock the set now. Do not add, rename, or
   remove categories once brainstorming begins.

3. **Brainstorm causes.** For each category, generate candidate causes that could
   plausibly contribute to the effect. Work one category at a time. Do not evaluate
   or discard causes during this step — record everything.

4. **Identify sub-causes.** For any cause that is itself explained by a deeper cause,
   add a sub-cause beneath it. Two levels of nesting are typically enough; go deeper
   only where the extra depth changes what action is possible.

5. **Prioritise and verify.** Review the completed map. Identify the branches most
   likely to be contributing based on available evidence. Mark unverified candidate
   causes explicitly. Select the highest-priority branches for evidence gathering or
   further depth analysis.

---

## Example

**Effect:** The weekly team status report is consistently delivered late.

- **People**
  - Contributors underestimate how long their section takes to write
    - No time is blocked in calendars for report writing
  - One contributor is in a different time zone and submits last
- **Process**
  - No agreed submission deadline for individual sections
  - The compiler waits for all sections before starting the summary
    - A partial-draft process has never been established
- **Technology & Tools**
  - The shared document template is hosted on a slow system
  - Version conflicts occur when two contributors edit simultaneously
- **Environment**
  - Report day coincides with the standing all-hands meeting
    - Contributors are context-switching at the highest-load point of the week
- **Information**
  - Section owners do not receive a reminder until the morning it is due
- **Resources**
  - Report compilation is an informal role with no dedicated time allocation

The cause map surfaces six categories of contributor. Before this step, the problem
looked like a single individual submitting late; the map reveals that the process
and environment categories carry causes independent of any one person.

---

## Failure modes

**Blank-canvas paralysis.** Staring at empty category branches with no starting
prompt is the most common reason a fishbone session stalls. Start by asking for the
most obvious cause in one category — even a wrong answer primes the group to respond
with corrections and additions. The diagram is a brainstorm scaffold, not a test.

**Treating the diagram as a verified conclusion.** Every entry on a fishbone is a
candidate cause — a hypothesis, not a finding. A branch that looks plausible is not
evidence that the branch is real. Presenting the completed diagram as a diagnosis
without subsequent evidence gathering is the single most consequential misuse of the
tool. The diagram's job is to generate hypotheses; verification is a separate step.

**Using a fishbone when Five Whys fits.** If the problem has a single traceable
causal chain and the goal is to find the root of that chain, a fishbone adds overhead
without adding breadth. The multi-category structure is an advantage only when
multiple independent cause types are plausibly in play. When you already know the
cause type and need to drill deeper, reach for [5-Whys](five-whys.md) instead.

---

## Handoff

The candidate causes mapped here enter the 5-phase methodology at
Phase 2 (Challenge Assumptions). Each branch on the fishbone is an `untested belief` —
the fourth assumption class in Phase 2's four-type scheme — because the diagram is a
brainstorm of plausible contributors, not a set of verified facts. Add each candidate
cause as a row in the Classified Assumptions Table with type `untested belief`.

Do not route fishbone branches directly to Phase 3 (Establish Ground Truths). A
branch is promoted to a ground truth only after evidence confirms it — that promotion
happens inside Phase 2's challenge-and-verify operation, not by skipping it.

For branches that warrant deeper causal investigation, pair the fishbone with
[5-Whys](five-whys.md): the fishbone is the breadth-first cause map that identifies
which branch to investigate; 5-Whys is the depth-first root-cause drill that traces
that branch to its actionable source. The two tools are complementary — fishbone
first to survey the cause space, then 5-Whys to drill the highest-priority branch.

---

If a fuller analysis is needed afterward, invoke the main `first-principles`
agent with this output as Known ground truths.
