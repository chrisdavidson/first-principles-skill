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
cause type and need to drill deeper, reach for `/first-principles:five-whys` instead.

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
`/first-principles:five-whys`: the fishbone is the breadth-first cause map that identifies
which branch to investigate; 5-Whys is the depth-first root-cause drill that traces
that branch to its actionable source. The two tools are complementary — fishbone
first to survey the cause space, then 5-Whys to drill the highest-priority branch.
