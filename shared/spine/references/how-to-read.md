# How to Read This Analysis for Business Value

A first-principles analysis is long because it shows its work. You do not need to read all of it
to act on it. This guide says where to look, and in what order.

## Start at the Answer

Read the `## Answer` block first. In the reader report it is headed Executive Summary. It has
three parts: the "Recommendation" says what to do; the "Band (from §6)" says how sure the analysis
is, HIGH, MEDIUM or LOW; and "Would change it" names the evidence that would move the band or the
advice. Each line names the chain behind it, such as (chain C2), so any claim you doubt can be
traced.

## Map to your role

- **Decision owner:** read the Answer, then the "Conclusion", above all its "Recommended approach"
  and "Trade-offs acknowledged".
- **Operator:** read the "Derivation Chains" to see how each step follows from facts, then
  "Abandoned Reasoning" to see which routes were tried and why they fail.
- **Risk and compliance:** read the "Assumptions Table". A row typed `current constraint` holds
  only until something changes, and its verdict says when. A row typed `untested belief` is
  unproven. Then look in the "Ground Truths" for any id written as `GT-N?`: that fact was not
  verified.

If a persona view for your role sits beside the report, it is a shorter route to the same
material; the six sections remain the source.

## Audit path for high-stakes decisions

Follow one claim back to its evidence:

1. Pick a claim in the "Conclusion" and note the chain it names.
2. Find that chain in the "Derivation Chains" and read each step.
3. Check every ground truth the chain starts from in the "Ground Truths", and whether it carries
   a `?`.
4. Check each assumption the chain marks with `[Assumes: A-N]` against the "Assumptions Table"
   and its verdict.
5. In the working file, the one whose name starts with analysis-, read the "Self-Audit Gate"
   verdicts and the structured summary at the end of the appendix: they record how the analysis
   scored itself.

## What business value looks like here

- **"Success criteria"** in the "Problem Essence": the measurable outcomes that would show the
  problem is solved. Use them as your acceptance test.
- **"expiry conditions"** on `current constraint` rows: the events that should trigger a review.
- **Each "Dead End"** in "Abandoned Reasoning": an option you need not fund again, with the reason
  it fails.
- **"Would change it":** the falsification condition, the result that would reverse the
  advice. If it is cheap to test, test it first.

## When to act and when to dig

Act when the band is HIGH and no ground truth the Conclusion rests on is marked `?`. The working
file's `**Pre-check:**` line lists both.

Otherwise, treat "Would change it" as your evidence plan: gather that evidence before you
commit. A MEDIUM or LOW `**Confidence:**` line names what holds the band down
and what would lift it.
