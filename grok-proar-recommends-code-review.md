**Recommendation: treat PRAOR as an explicit, first-class control loop that the five-phase methodology *implements*, not as an after-the-fact mapping.** The repo already closed the major structural gaps in v8.18 (Act limb, Observe→Perceive edges, focused-mode parity, and the three HARN gates). The remaining consistency problems are mostly *semantic drift*, *live vs. structural enforcement*, and *incomplete React semantics*. Fix those and the loop becomes reliable end-to-end.

### Current mapping (what already exists)

| PRAOR phase | Current coverage in the skill | Strength |
|-------------|-------------------------------|----------|
| **Perceive** | Phase 1 (Essence) + Input Contract + mid-run `AskUserQuestion` re-open + Criterion-1 Absent → Phase 1 | Strong (with bounded re-entry) |
| **Reason** | Phases 2–4 (Assumptions → Ground Truths → Derivation Chains) + companion techniques | Strong |
| **Act** | Phase 3 verification step (“Acquire the evidence — attempt the read…”) using Read/Grep/WebFetch; labels `read-at-source` / `reported-by-delegate` / `?` | Present in prose + HARN-01, but still structural only |
| **Observe** | Self-Audit Gate (Phase 5) + Fix/Repeat + failure records + confidence caveats | Strong *inside the document*; weak on real-world outcomes |
| **React** | Bounded re-entry edges (at most one re-perception pass), second-order → Phase 2, degradation to “unresolved gap + caveat” | Present but under-named and under-enforced live |

The v8.18 record is accurate: Perceive / Reason / Report were already solid; Act was missing; Observe was purely introspective; there was no clean Observe→Perceive return; focused stubs diverged. Those structural holes are closed. Consistency still fails in four places.

### Root causes of the consistency issues

1. **Structural gates ≠ live behaviour**  
   HARN-01/02/03 only assert that the *prose* and *literals* exist and are well-formed. They explicitly do **not** measure whether the model actually opens a source, fires a re-entry edge, or respects the one-pass bound. MEAS-01/02 were deferred. That is the largest consistency gap.

2. **Focused-mode residual divergence is still disclosed but real**  
   Slash-invoked focused skills still skip evidence acquisition and run a scope-proportionate check instead of the full Self-Audit Gate. The divergence is stated, which is good, but it means two invocation paths produce observably different PRAOR coverage. Readers and the model itself can treat them as equivalent.

3. **“React” is distributed and under-named**  
   The four re-entry edges + degradation rule *are* React, but they are never labelled as such in the agent body or Step 0. The model therefore has no single mental model of “after Observe, either react (re-perceive once) or degrade and report.” That produces inconsistent application across turns and across focused vs full-composer paths.

4. **Turn-budget pressure still privileges early phases**  
   The Self-Audit Gate runs last. When the 60-turn budget is tight, Observe and React are the first things to be truncated. The current “turn discipline” text acknowledges this but does not give the model a concrete prioritisation rule that protects the loop-closing limbs.

5. **No explicit state machine or artefact that records the current PRAOR step**  
   Artefacts are phase-named (Essence Statement, Classified Assumptions Table, …). There is no durable “current loop state” or “edges fired so far” marker that survives across a Fix/Repeat or a mid-run clarification. Silent loss of that state is exactly what the regeneration rule tries (and sometimes fails) to prevent.

### Concrete recommendations (ordered by leverage)

**1. Make PRAOR the explicit outer control loop (highest leverage)**  
Add a short, imperative section near the top of `shared/spine/SKILL-body.md` (and therefore the generated agent body):

```markdown
### Control loop: Perceive → Reason → Act → Observe → React

Every analysis runs inside this loop. The five phases implement it; they do not replace it.

- **Perceive** — acquire or re-acquire the frame (Phase 1 + Input Contract + mid-run AskUserQuestion).
- **Reason** — classify, verify candidates, derive (Phases 2–4).
- **Act** — open cited sources before labelling them `read-at-source` (Phase 3 verification step).
- **Observe** — Self-Audit Gate + failure records + confidence caveats (Phase 5).
- **React** — at most one re-perception pass per edge, then degrade to “unresolved gap + caveat”. 
  Never spin. Never silently drop an edge that fired.

When a re-entry edge fires, name it at the top of the response. When the one-pass budget is exhausted, report the residual gap; do not invent a second pass.
```

Keep the five-phase procedure underneath it. The outer loop becomes the consistency invariant; the phases become the detailed implementation.

**2. Close the live-behaviour gap (the real consistency problem)**  
- Implement the deferred MEAS-01 (does the agent actually attempt the read when a source is reachable?) and MEAS-02 (does evidence acquisition change analysis quality?) as *observational* harnesses, not hard gates. Record K-of-N results the same way the confidence-transitivity captures are already recorded.
- Add a lightweight “Act limb fired / not fired / source unreachable” marker to the Ground Truths list and to the Self-Audit Gate’s Criterion 3 scoring. This makes the Act step visible in every signed-off analysis without changing the output template shape.

**3. Tighten focused-mode parity without killing the cost saving**  
- Keep the disclosed residual (no full evidence acquisition, proportionate validation).
- Make the residual *mandatory disclosure* in the focused skill’s own output template and in Step 0, so both the model and the human reader see the same sentence.
- Optionally add a one-line “escalate to full-composer if any `?` ground truth becomes load-bearing” rule. That gives React a clean path out of focused mode.

**4. Protect Observe + React under turn pressure**  
Strengthen the turn-discipline paragraph:

- Explicit priority order: named artefacts for Phases 1–4 → Act limb (if any HIGH-confidence chain needs it) → Self-Audit Gate → React edges.
- If the budget is exhausted before the Gate, the response must still emit the partial artefacts + an explicit “Observe incomplete — residual confidence caveat” rather than a silent truncation.

**5. Add a minimal loop-state artefact**  
A single short block (or a line in the existing omission-disclosure section) that records:

- edges that have already fired this analysis,
- whether the Act limb was attempted,
- current confidence band of each derivation chain.

This makes the regeneration rule and the “disclose which edge fired” rule mechanically checkable and removes the silent-state-loss class of inconsistency.

**6. Keep the existing structural gates; do not weaken them**  
HARN-01/02/03 + the battery registration are valuable. Leave them. Just stop treating a green structural gate as proof of live PRAOR compliance. The next milestone should treat live measurement as the consistency layer on top of the structural layer.

### Suggested next milestone shape

Call it something like “PRAOR live consistency” (or fold into the existing v9.4 Source-Literal work if that is already the vehicle):

1. Add the explicit Control-loop section (prose only — cheap).
2. Instrument Act-limb firing and re-entry-edge firing in the quality harness / conformance baseline.
3. Make the focused-mode residual a required disclosure in both surfaces.
4. Add the loop-state marker.
5. Run a small set of live captures (5–10 prompts) that deliberately exercise evidence acquisition, Criterion-1 Absent, and second-order contradiction; record whether the model actually followed the loop.

That sequence turns the existing solid structural work into a reliably consistent Perceive-Reason-Act-Observe-React agent without rewriting the five-phase methodology.

If you want, I can draft the exact Control-loop section text, the loop-state marker wording, or a minimal set of live-test prompts that would surface the remaining consistency failures.
