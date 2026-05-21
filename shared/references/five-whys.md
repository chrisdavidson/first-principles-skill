# 5-Whys

> A branching root-cause drill-down procedure — reach for it when a symptom keeps
> recurring despite surface fixes and you need to trace the causal chain to its
> actionable source.

---

## When to reach for this

Use 5-Whys when a problem keeps coming back. The symptom is observable, the surface fix
has been tried, and you need to find what is actually driving recurrence.

**Good fit:** the problem has a traceable causal chain; one or a small number of root
causes are likely; corrective action is within your control.

**Not a good fit:** the problem involves multiple interacting subsystems with no single
causal chain — that pattern calls for a fishbone (Ishikawa) diagram instead, which maps
causes across categories in parallel.

---

## Procedure

**State the symptom.** Write one sentence: the observable problem that keeps occurring.
Do not state a suspected cause — state the observable effect.

**Ask: Why did this happen?** Write every cause you can identify. Do not filter yet.
Multiple causes at the first level are expected.

**For each cause, ask why again.** At each level, ask "What else caused this?" before
going deeper into any one branch. Complete the lateral scan at a level before descending.
Multiple valid causes each become their own branch.

**Stop drilling a branch when BOTH hold:**
- You can state a specific corrective action that would prevent recurrence.
- That action is within your practical control.

If a branch reaches a cause with no actionable corrective — a systemic constraint outside
your control — record it as a real finding and move to the next branch. A cause you cannot
fix is still worth knowing.

**Validate each causal link** with observable evidence, not inference. If you cannot point
to evidence for a link, flag it as assumed before continuing.

---

## Example

**Symptom:** The bread keeps going stale before it is finished.

- Why? → The loaf is too large for one person to finish quickly.
  - Why? → Only standard-size loaves are bought.
    - Why else? — considered: the household eats less bread than it used to;
      rejected, weekly bread consumption has not changed — only the loaf size on
      offer has.
    - Why? → Half-loaves were not known to be available.
      - **Stop:** Corrective action — check the store for half-loaves or switch to a
        smaller format. Specific, in control, prevents recurrence. **(Branch ends here.)**
- Why (else at level 1)? → The bread is stored on the counter.
  - Why? → No one sealed the bag after the first slice.
    - Why else? — considered: the bag itself is defective and will not seal;
      rejected, the bag seals fine when the clip is used — the issue is that the
      clip is not at hand.
    - Why? → The bag clip is kept in a different drawer.
      - **Stop:** Corrective action — keep a clip at the bread storage point.
        Specific, in control, prevents recurrence. **(Branch ends here.)**

Both branches reach actionable corrective actions. The root causes are a purchasing
habit and a storage habit — not the bread itself.

---

## Failure modes

**Stopping on a count, not a test.** Asking "why" exactly five times and declaring done
is the most common failure. Five is a typical depth, not a rule. Stop when the test is
met, not when the count is reached.

**Single-thread drilling.** Moving straight down one causal chain without asking "What
else caused this?" at each level. This misses parallel causes and produces an incomplete
picture.

**Inference without evidence.** Writing "probably because X" and continuing down that
branch. Every causal link needs observable evidence, or must be flagged as assumed.

**Confirmation bias.** Starting with a suspected cause and steering the chain toward it.
The lateral scan at each level ("What else caused this?") is the check against this — it
forces consideration of causes that contradict the hypothesis.

---

## Handoff

The root cause(s) identified here are inputs to the 5-phase methodology. If you reached
for this tool during Phase 2 (Challenge Assumptions), add each root cause as a challenged
assumption row in the Classified Assumptions Table. If you reached for it during
Phase 3 (Establish Ground Truths), promote each evidence-backed root cause to a ground truth —
give it a stable GT-N identifier and a source citation, or the `GT-N?` suffix if its
causal link is still assumed rather than verified. If you reached for it during Phase 4
(Reason Upward), add each cause as a validated step in the relevant Derivation Chain.
