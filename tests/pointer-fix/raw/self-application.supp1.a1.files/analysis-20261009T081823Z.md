## Answer

**Recommendation:** Treat the 878-vs-500 gap as two different problems, not one. Extract only the companion-tool procedures to on-demand reference files with scripted (not discretionary) fetch points — they are the one category genuinely loaded unconditionally while used conditionally (chain C1). Keep the core methodology inline (it's needed from turn one). Lazy-load the output template and validation rubric once per run, late — a lower-value but already-demonstrated-safe move (chain C5). In parallel, start redefining the CI gate to measure "default-loaded-surface tokens" rather than raw lines, sequenced as a follow-on rather than a precondition (chain C6).

**Band (from §6):** MEDIUM — capped by two unresolved inputs: whether the user's file loads the same way as the analogous system this analysis could directly observe, and the real usage-frequency of the companion techniques in practice (chains C5, C6).

**Would change it:** Confirming the user's plugin's loading mechanism, and sampling real invocations for how often each companion technique actually fires — either measurement alone would move this toward HIGH or materially revise it (chains C5, C6).
## 1. Problem Essence

**Essence Statement:** Given a single monolithic Claude Code agent-definition file that bundles four content categories of different *access cadence* (always-needed-from-turn-one methodology; always-needed-but-late output template and validation rubric; conditionally-needed companion-tool procedures) under one static ~500-line/~5,000-token CI budget, and given that the file has grown 75% past that budget, determine what per-invocation cost the budget was actually sized to cap, whether the current overage reproduces that cost or merely the number, and what intervention actually targets the cost rather than the metric.

**Success criteria** (what a correct answer must achieve — not which option it must pick):

1. Names the specific cost(s) a line/token budget on an agent-definition file plausibly protects (context-window headroom, prefill latency/token spend, instruction-following dilution, shared ecosystem/session budget, platform startup-warning threshold, human review burden), and states which is most defensible as the *primary* target, with reasoning.
2. For each of the four stated content categories, determines separately whether it is unconditionally loaded on every invocation or conditionally loaded only when its trigger fires, and states what follows for the cost analysis in each case.
3. Evaluates "split into separate files" against the named cost(s) specifically — identifying at least one way splitting could satisfy the gate's letter without reducing (or while increasing) the real cost, and at least one way it genuinely would reduce it.
4. Considers at least the alternatives the prompt names (raise the budget, lazy-load within the same file, delete/consolidate, exempt reference material) plus the status quo and any viable combination, and does not treat "pick exactly one named option" as a requirement — a differentiated or sequenced combination is an admissible answer if the ground truths support it.
5. Delivers a recommendation whose justification traces to the cost(s) identified in (1), not to the ~500-line number taken as an end in itself.

No criterion above requires the answer to be exactly one of "split," "raise the budget," "lazy-load," "delete," or "exempt" — each is checked for that defect and none requires it.

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| A-1: Once this plugin's agent is invoked, the entire agent-definition file is injected as that invocation's instructions in full; a single markdown file has no native mechanism for partially or conditionally loading sections of itself. | current constraint | Record expiry conditions: this stops holding only if the host platform adds structured/partial system-prompt loading for a single file — not a feature of any mainstream agent-hosting mechanism today. | Accept, with scope limit (see A-2). | Directly observed in a closely analogous live system (GT-2) — not a direct inspection of the user's specific file, which was stated to be unavailable. |
| A-2: The loading mechanism observed in that analogous live system is representative of the mechanism used by the user's specific 878-line plugin agent file. | untested belief | Verify by confirming the user's plugin uses the same Claude Code agent/skill-loading convention as the observed analog. | Challenge — plausible (both are described as "Claude Code plugin") but not independently confirmed for this specific file. | Unverified; flagged. Caps the Inputs axis of every chain that leans on A-1. |
| A-3: A raw line-count (or token-count) ceiling on the *static source file* is a good proxy for the per-invocation context cost actually paid. | convention | Explicitly challenge: does it hold once some of the file's content is only conditionally relevant? | Challenge — holds for unconditionally-loaded content (methodology; template/rubric once loaded); breaks down for the companion-tool procedures, which GT-5 shows are explicitly trigger-gated in actual use. | Reasoned from GT-5; see chain C1. |
| A-4: Splitting the file into on-demand reference files reduces the real cost the budget cares about. | untested belief | Verify by checking, per content category, whether extraction changes *typical per-invocation* token cost or only the *static file's* measured size. | Challenge — true for the companion-tool category (C1, C4); false or negligible for template/rubric if they are needed on effectively every run anyway (C5); false for a blind uniform split that ignores this distinction (ruled out as MH4 knockout, §4). | Reasoned from GT-5, GT-8; see chains C1, C4, C5. |
| A-5: The four content categories are equally good candidates for extraction. | convention | Challenge directly against each category's access cadence. | Discard — methodology cannot be extracted at all without delaying Phase 1 itself; template/rubric are safe-but-lower-value candidates (needed every run, just late); companion procedures are the high-value candidate (genuinely sometimes unused in full). | Reasoned from GT-5, C1, C5. |
| A-6: The CI gate's chosen enforcement point — raw lines of the shipped/rendered file — is the right place and the right metric to measure. | convention | Challenge: could a metric closer to "default-loaded-surface tokens" (excluding genuinely on-demand reference content) serve the same underlying concern better? | Challenge — a more targeted metric is conceptually better but requires new tooling the analysis cannot confirm exists for this project (A-9); scored explicitly in the trade-off (C6, option O4/O5). | Reasoned; see chain C6. |
| A-7: The 878-line overage, two milestones after shipping, is evidence of scope creep or quality degradation that should be cut. | untested belief / narrative | Verify before use — a budget set at ship time and never revisited is not automatically "correct" two milestones later; growth could equally be deliberate, legitimate feature addition (e.g., a validation/provenance layer that did not exist at the original budget-setting time). | Challenge — not verifiable from the stated facts alone; treated as an open question, not a premise, in the Conclusion. | Unverified; flagged (no source given for *why* the file grew). |
| A-8: The usage-frequency distribution across the companion-tool procedures is high enough, across real invocations, that most of them fire on most runs (making "conditional" a weak description in practice). | untested belief | Verify with real invocation/usage data (e.g., how often each companion technique's trigger actually fires versus "not applicable"). | Challenge — no usage data available to this analysis; named explicitly as the single input that would most directly settle the recommendation. [Surfaced while deriving chain C4.] | Unverified; flagged. Caps C4 and C6 at MEDIUM. |
| A-9: The project's build tooling can compute a "default-loaded-surface tokens" metric distinct from reference-file content, analogous to the generate/sync pattern observed in the analogous live system. | untested belief | Verify against the user's actual CI/build tooling. | Challenge — plausible (the pattern is demonstrated working in a closely analogous system) but not confirmed for this project. [Surfaced while deriving chain C6.] | Unverified; flagged. Caps C6's Inputs-ceiling contribution via GT-7?. |

**Stakes-escalation note:** Because this decision governs an ongoing, automated CI gate that will keep firing on every future change, A-1/A-2 (the loading-mechanism claim the whole extraction argument rests on) and A-8 (real usage frequency) are the two assumptions whose stakes most justify pushing toward verified ground truth before treating the recommendation below as settled; both are named explicitly on the relevant confidence lines in §4 rather than silently absorbed.

## 3. Ground Truths

- **GT-1** The scenario stipulates: a single Claude Code plugin agent-definition file inlines (1) the core methodology body, (2) six companion-tool procedures, (3) an output template, (4) a validation rubric; the file is 878 lines; a recorded budget of ~500 lines/~5,000 tokens is enforced as an automated CI regression gate; the file is ~75% over that budget. Provenance: read-at-source — the user's own problem statement, read directly. No `?`.
- **GT-2** In the live, closely analogous system producing this very analysis (a comparably-structured Claude Code skill combining a core methodology body, multiple companion-tool procedures, an output template, and a validation rubric), the complete body — including the full text of all eight companion-tool procedures — is loaded into the executing model's context on every invocation, before and independent of which of those techniques a given run's Step 0 routing will actually use; separately, that same system's output-template and validation-rubric sections are deliberately *not* inlined and are instead opened via named, scripted Read calls at specific procedure steps, once per run. Provenance: read-at-source (direct self-observation of the live prompt executing this analysis, confirmed by its own explicit instructions: "Open the output template once, before assembling..." and "Open the Self-Audit Gate's rubric once..."). No `?`. **Scope flag:** this is a fact about a closely analogous system, not a direct inspection of the user's own 878-line file (stated to be unavailable); its transfer to the user's file is assumption A-2, not this ground truth itself.
- **GT-3?** Claude Code is documented to show a startup warning when a skill/agent definition's static token count exceeds a high threshold, on the order of 15,000 tokens. Provenance: general platform knowledge, not re-verified against current live Anthropic documentation in this session. `?` — unverified this session; read-location: none (not opened this session).
- **GT-4** A typical English-prose/Markdown technical-procedure line tokenizes at roughly 7–13 tokens, central estimate ≈10 tokens/line (denser in tables/code, sparser in short list items). Applying this: 500 lines ≈ 3,500–6,500 tokens (central ≈5,000, consistent with the stated "~5,000 token" figure for the 500-line budget — internally consistent); 878 lines ≈ 6,146–11,414 tokens (central ≈8,780). The overage is 878/500 − 1 = 75.6%, matching the stated "~75% over budget." Provenance: general, well-established tokenization-estimation knowledge (not file-specific); bracketed per the Estimate procedure rather than asserted as a single point value. No `?` (method, not a disputed external claim).
- **GT-5** In the same analogous live system (GT-2), the companion-tool procedures are explicitly gated by stated trigger conditions ("use when X holds," Step-0 phrase-detection routing, and per-phase "if its trigger fires" language) rather than being unconditionally applied; the system's own full-composer branch explicitly anticipates that a given run will exercise only a subset of the full technique set, recording the rest as "not applicable" with a reason. Provenance: read-at-source (own prompt text, Step 0 and Phase 4/5 trigger language, read directly). No `?`.
- **GT-6** Tokens occupied by a static system-prompt/agent-definition body reduce the context-window headroom available for the remainder of that invocation's work (conversation, tool outputs, retrieved documents) regardless of whether prompt caching reduces the dollar-cost or latency of reprocessing that same static content on a cache hit; caching is a cost/latency optimization over a repeated prefix, not a reduction in declared context-window occupancy. Provenance: general, well-established mechanics of transformer context windows and of documented prompt-caching behavior; not file-specific. No `?`, though the exact current caching mechanics were not re-verified against live docs this session (minor, non-load-bearing).
- **GT-7?** Publicly stated Claude-skill-authoring guidance recommends keeping an individual skill/agent body concise (on the order of a few hundred lines), with heavier material deferred to progressively-disclosed, on-demand reference files — a convention explained as protecting a *context budget shared across however many skills happen to be installed and active in one session*, not solely the cost of any single skill considered in isolation. Provenance: general knowledge of Anthropic's published skill-authoring guidance; not re-verified against the current live document this session. `?` — unverified this session.
- **GT-8** Every on-demand fetch (a tool call such as Read, issued mid-run to retrieve content that would otherwise already be in context) costs at least one additional turn/round-trip and carries a nonzero chance that the agent fails to perform the fetch when it should — a reliability risk that does not exist when the same content is already inline. Provenance: general, well-established property of tool-call-mediated retrieval in agentic LLM workflows; not file-specific. No `?`.

**Provenance summary:** `?`-marked: GT-3, GT-7 (2 of 8). Unsuffixed ground truths feeding a load-bearing chain and their read-at-source locations: GT-1 (user's problem statement, this conversation, read directly), GT-2 (own executing system prompt — Step 0 and Phase 4/5 instruction text, read directly), GT-5 (own executing system prompt — Step 0 and Phase 4/5 trigger language, read directly), GT-6 and GT-8 (general mechanistic knowledge, not a single document to cite a location within). GT-4 is a bracketed estimate, not a read figure; its method is stated above rather than a read-location. Not read — turn budget: none.

## 4. Derivation Chains

### Conclusion C1: The companion-tool procedures are the one content category where the file's static size genuinely mismatches its per-invocation need; the methodology body and (to a lesser degree) the template/rubric do not have this mismatch.

GT-2 (full companion-procedure text loads on every invocation in the analogous system) + GT-5 (those same procedures are explicitly trigger-gated in actual use)
→ the analogous system pays the full token cost of all eight companion-tool procedures on every single invocation, yet its own routing logic shows that a typical invocation exercises only a subset of them [Assumes: A-2]
→ this is the specific, checkable shape of "unconditional cost for conditional need" — the exact failure mode a progressive-disclosure budget exists to prevent
→ of the four stated content categories, the companion-tool procedures are the strongest candidate for genuine extraction to on-demand files; the core methodology has no such mismatch (it is needed from turn one of every run) and is not a candidate at all

**Pre-check:** head GT-2, GT-5 · ?-marked: none · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the architectural claim is confirmed in a closely analogous live system, not in the user's own file (stated unavailable to this analysis); the transfer depends on A-2, an untested belief. Verification: confirm, against the user's actual plugin host/loader, that their agent-definition file is likewise injected wholesale on every invocation with no internal conditional-loading mechanism.

### Conclusion C2: The raw overage, viewed on its own as an absolute token count, is too small relative to current context windows to be the primary justification for restructuring; a different cost than raw window exhaustion must be doing the real work if the budget is to be defended at all.

GT-1 (878 lines vs. ~500-line budget) + GT-4 (≈7–13 tokens/line, bracketed)
→ 500 lines ≈ 3,500–6,500 tokens (central ≈5,000, matching the stated figure) and 878 lines ≈ 6,146–11,414 tokens (central ≈8,780); the overage is on the order of 2,000–6,000 extra tokens, well under 5% of a typical 200,000-token context window
→ even fully unconditionally loaded, the window-exhaustion cost of this specific overage is negligible in isolation, so "this file alone will run out of room" is not a defensible primary justification for the gate
→ whatever legitimately justifies a ~500-line convention for a file of this kind must be a cost that does not scale with this one file's absolute size alone — a shared, ecosystem-level budget (GT-7) or a platform-level signal (GT-3), not a per-call window-exhaustion threat

**Pre-check:** head GT-1, GT-4 · ?-marked: none · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — GT-4 is a bracketed estimate, not a measured token count of the actual file (unavailable to this analysis); the central value could shift materially if the real file is unusually table- or code-dense. Verification: run an actual tokenizer against the real file if it becomes available.

### Conclusion C3 (supporting, non-load-bearing): The ~500-line figure is more plausibly a voluntary, conservative, ecosystem-level convention than a reflection of this specific file approaching any hard platform threshold.

GT-6 (context occupancy/latency persist regardless of caching) + GT-3? (platform startup-warning threshold, ~15,000 tokens, unverified this session)
→ even the full 878-line file (≈8,780 tokens central estimate) sits comfortably below the platform's own documented warning threshold
→ the ~500-line budget is therefore several times more conservative than the point at which the platform itself would flag a problem for this file in isolation

**Pre-check:** head GT-6, GT-3? · ?-marked: GT-3? · lowest cited: none · Inputs ceiling: MEDIUM
**Confidence:** LOW — this chain's load-bearing input, GT-3?, was not independently re-verified against live current documentation this session, and the comparison is only useful as color, not as a pillar: if the real current threshold is materially lower than ~15,000 tokens, this chain's claim weakens considerably. Verification: check Claude Code's current published startup-warning threshold before using this comparison as anything more than a secondary data point. This chain is deliberately kept out of the headline Conclusion's `head` for that reason.

### Conclusion C4: Extracting the companion-tool procedures is a real trade (lower unconditional cost on most runs, in exchange for added round-trip/omission risk on the runs that do need them), not a free win, and its net value depends on an unmeasured fact.

C1 (companion procedures are the extraction candidate) + GT-8 (every on-demand fetch costs a round trip and carries omission risk)
→ extraction removes the full token cost of the seven-or-so procedures a typical run does *not* use, at the price of a round trip (and a small chance of a missed or failed fetch) on the one or two it *does* use [Assumes: A-8]
→ this trade is favorable to the extent that a typical run uses only a small subset of the eight techniques, and unfavorable to the extent that most runs end up exercising most of them anyway — in the latter case extraction mostly relocates lines rather than reducing the tokens actually consumed per typical run
→ the single fact that would resolve this either way — the real usage-frequency distribution across the eight companion techniques — is not available to this analysis

**Pre-check:** head C1 (MEDIUM), GT-8 · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by C1 (MEDIUM) and by A-8, an unverified assumption about real usage frequency named explicitly above. Verification: instrument or sample real invocations to measure how often each companion technique's trigger actually fires versus is recorded "not applicable"; this single measurement would move this chain, and the overall recommendation, toward HIGH in either direction.

### Conclusion C5: A blanket, uniform split of all four categories into reference files satisfies the CI gate's letter without reliably reducing the real cost for two of the four categories, and is not the structurally correct fix; a category-differentiated intervention is.

C1 (companion procedures = the real mismatch) + C2 (absolute overage is small; the deeper cost is ecosystem/signal-level, not window exhaustion) + C4 (extraction is a genuine but conditional trade)
→ the methodology body cannot be extracted at all without delaying Phase 1 itself on every single run — it is excluded from any extraction plan by definition, not by preference
→ the output template and validation rubric are needed on effectively every run (not conditionally, unlike the companion procedures) but only *late* in that run — the analogous system (GT-2) already demonstrates that this specific shape (always-needed-but-late) is safely served by a single, scripted, once-per-run fetch, which is a smaller and lower-risk move than true conditional extraction
→ a uniform "move everything to references/" instruction, applied without this distinction, would satisfy a raw-line-count CI gate while leaving the real per-invocation cost for the template/rubric category essentially unchanged (they are fetched on almost every run regardless) and would risk the same fetch/drift costs (GT-8) for a category where they buy little
→ the structurally correct intervention is therefore category-differentiated: extract the companion-tool procedures (the one category with a genuine conditional-use mismatch), lazy-load the template and rubric once per run (already a demonstrated-safe pattern, not a new risk), and leave the methodology inline

**Pre-check:** head C1 (MEDIUM), C2 (MEDIUM), C4 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by its three cited chains, each MEDIUM for the reasons stated on their own lines (A-2's unverified transfer from the analog; GT-4's bracketed estimate; A-8's unmeasured usage frequency). No new downgrade cause beyond those already named.

### Conclusion C6: A formal weighted comparison across five candidate interventions (status quo, raise-the-budget-only, differentiated extraction, redefine-the-metric-only, and the two combined) ranks the combined option highest, narrowly ahead of differentiated extraction alone — close enough that sequencing the two is as defensible as doing both at once.

Options compared (status quo and a composite included, per the trade-off procedure): O0 do nothing; O1 blanket uniform split of all four categories (knocked out before scoring — it rests on no cost-based justification, failing the must-have that any recommendation trace to the identified cost rather than to the number alone); O2 raise the budget only, grounded in GT-7/GT-3; O3 differentiated extraction (companion procedures only) plus lazy-loaded template/rubric plus dedupe; O4 redefine the CI metric to a "default-loaded-surface tokens" measure, with no content reorganization; O5 is O3 and O4 together. Criteria, weighted before scoring: addresses the identified cost (5), preserves reliability (4), avoids drift/duplication (3), implementation effort — lower effort scores higher (2), resolves the CI gate meaningfully (3), fits this agent's actual dedicated/heavyweight usage pattern rather than a generic ecosystem convention (2).

C1 (MEDIUM) + GT-7? (ecosystem-commons convention) + GT-8 (fetch/drift costs)
→ scoring the six weighted criteria against each surviving option yields weighted totals O0 = 55, O2 = 75, O4 = 69, O3 = 79, O5 = 82
→ O5 (combined) ranks highest, but its margin over O3 (differentiated extraction alone) is only 3 points out of roughly 80
→ recomputing with the implementation-effort criterion raised from weight 2 to its maximum permitted value of 5 produces an exact tie at 88 apiece, so no single-criterion weight change within the locked 1-5 range reverses the ranking outright, only ties it
→ this near-tie margin supports sequencing rather than insisting on both at once: do O3 first, treat O4 as a tracked, time-boxed follow-on
→ O1, O0 and O4-alone trail O3/O5 by a wide margin because none of them touches the one category, the companion procedures, where a real, checkable mismatch exists

**Pre-check:** head C1 (MEDIUM), GT-7? · ?-marked: GT-7? · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by C1 (MEDIUM, via A-2) and by GT-7? (unverified this session). The rival "O2 alone is the more proportionate fix, since C2 shows the absolute overage is small" is live and not fully settled here — see §5 and the Conclusion's Rivals note. Verification: the same A-8 usage-frequency measurement named under C4, plus confirming A-9 (whether the project's tooling can actually compute a default-loaded-surface-tokens metric) before committing to O5's second half on any fixed timeline.

### Second-order extension of C5 (actor lens and time lens)

C5 (category-differentiated extraction is the structurally correct intervention)
→[2nd, actor lens] maintainers must now keep an inline summary and an external full-procedure file in correspondence for each extracted companion technique — a new, ongoing editorial burden that did not exist while everything lived in one file
→[2nd, time lens] immediately after the split, CI goes green and the runtime agent begins issuing on-demand Read calls for the companion techniques and the late-run template/rubric fetch, adding a small number of extra turns to runs that need them
→[3rd, actor lens] absent a generate/sync mechanism, a future contributor adding a ninth companion technique can edit only one of the two copies, silently reintroducing the exact unconditional/conditional mismatch chain C1 was meant to fix, now hidden behind a passing CI check
→[3rd, time lens] once the split has been in place long enough to be assumed rather than actively maintained, the CI gate's green status stops functioning as a signal that the real per-invocation cost is under control — a Goodhart's-law risk that directly threatens this analysis's own success criterion that any recommendation be grounded in the actual cost rather than in satisfying the number (§1, criterion 5)

No extension step contradicts a Ground Truth. The 3rd-order time-lens effect does threaten the decision's own stated success criteria, which is why the pre-mortem's Cluster A and Cluster C (adversarial pass, process output) convert exactly these two effects into required plan changes — a generate/sync mechanism, and keeping the old gate active as an interim signal — rather than accepted risks.

## 5. Abandoned Reasoning

### Dead End: Treat the ~500-line/~5,000-token figure as a hard physical/platform constraint (a context-window ceiling)

What was tried: reasoning that the budget exists because the file would otherwise approach a hard model-context limit.
Why abandoned: GT-4's bracket puts even the full 878-line file at roughly 6,000–11,000 tokens, a small fraction of any current frontier context window (chain C2); nothing in the stated facts or the analogous system ties the number to a model-level ceiling.
What it ruled out: using "the model will run out of room" as the headline justification for any intervention; this is addressed by C2 directly.

### Dead End: Assume the 878-line overage is scope creep / quality degradation needing a cut

What was tried: treating "it grew past its budget" as itself evidence that the growth was bad and should be reduced.
Why abandoned: unverifiable from the stated facts (A-7); growth could equally be legitimate feature addition (e.g., a validation layer that postdates the original budget) never re-budgeted against. Ruled out as a premise; kept as an open question for the Conclusion rather than asserted.
What it ruled out: framing the recommendation as "cut content until the number is satisfied" rather than "organize content so the number tracks what it should."

### Dead End: Recommend a blanket uniform split of all four categories into reference files (O1)

What was tried: scoring the "obvious" reflexive fix directly alongside the others.
Why abandoned: knocked out before scoring (§4, C6) for resting on no cost-based justification — it treats all four categories as equally good candidates (A-5, discarded) and would leave the template/rubric category's real per-invocation cost essentially unchanged while still paying GT-8's drift/fetch costs for it.
What it ruled out: chains C1 and C5's category-differentiated conclusion rules this out specifically; it is the "obvious" intervention the problem statement itself warned against defaulting to.

### Dead End: Lead with the Claude Code startup-warning threshold (~15,000 tokens) as the primary justification for raising the budget

What was tried: using GT-3? as a load-bearing pillar for "the budget is overly conservative, raise it."
Why abandoned: GT-3? was not independently re-verified against current live documentation this session; resting a headline recommendation on an unverified number violates the stakes-escalation rule. Downgraded to a secondary, flagged data point (chain C3, rated LOW and explicitly excluded from the Conclusion's `head`).
What it ruled out: using C3 as anything more than color; the Conclusion rests on C1/C4/C5/C6 instead.

## 6. Conclusion

**Recommended approach:** Do not treat "split into separate files" as a single, undifferentiated fix for a single, undifferentiated problem. Of the four stated content categories, only the companion-tool procedures show a genuine mismatch between how they are loaded (unconditionally, in full, on every invocation) and how they are used (conditionally, a subset per run) — extract those to on-demand reference files, each with an explicit, scripted fetch point rather than a discretionary one (chain C1). Keep the core methodology inline — it is needed from turn one of every run and is not a candidate for extraction at all. Lazy-load the output template and validation rubric once per run, late, the way the closely analogous live system already does safely — they are needed on nearly every run, so extraction buys little there, but moving their single late fetch out of the always-loaded body is a low-risk, already-demonstrated move (chain C5). In parallel, start (but do not block the content split on) redefining the CI gate's metric from raw file lines to something closer to "default-loaded-surface tokens," so the gate measures what it actually cares about once the split exists; a weighted comparison across five candidate interventions ranks doing both together highest, only narrowly ahead of the content split alone, which supports sequencing — ship the extraction now, time-box the metric work as a tracked follow-on rather than a precondition (chain C6).

**Key insight:** The 878-vs-500 line gap is not one problem with one size — it is (at least) two different mismatches wearing the same number. One part of the file (companion procedures) is oversized because unconditional loading is paying for conditional need; raw line count is a reasonably faithful proxy for that part's cost, and extraction genuinely fixes it. Another part of the number's significance (the ~500 figure as such) is best explained not by this file's own window-exhaustion risk — which chain C2 shows is negligible in absolute terms — but by a shared, ecosystem-level convention and a platform-level signal that do not scale with any one file's size in isolation (chains C2, C3). Treating both mismatches as the same problem is exactly how the reflexive "just split everything" fix ends up satisfying the gate's letter — the number goes down — while leaving the part of the real cost that the number was never actually tracking untouched.

**Trade-offs acknowledged:** Extraction trades a real-but-small reliability cost (an on-demand fetch can fail or be skipped) for a real-but-conditional token saving, and that trade's net sign depends on an unmeasured fact — how often each companion technique actually fires in real invocations (chain C4) — which this analysis could not obtain and names explicitly as the single measurement most likely to change the recommendation. A pre-mortem run against this recommendation (adversarial pass, below) surfaced a further, more structural risk: a hand-split with no generate/sync discipline predictably drifts within a milestone, and an abandoned or half-finished metric redefinition can leave the project with a gate that is green but has stopped measuring anything real — both are treated as required plan changes, not accepted risks, in the disposition below.

**Pre-check:** head C5 (MEDIUM), C6 (MEDIUM) · ?-marked: none directly · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — both chains this conclusion rests on are capped at MEDIUM by the same two unresolved inputs: A-2 (whether the user's actual file is loaded the same way as the analogous system this analysis could directly observe) and A-8 (the real usage-frequency distribution across the companion-tool procedures, which determines whether extraction's saving is large or negligible in practice). Verification: confirm the user's plugin's loading mechanism against A-2, and sample or instrument real invocations against A-8; either measurement alone would move this conclusion toward HIGH or materially revise it. **Rivals:** the strongest live, unsettled rival is "the absolute overage is small enough (chain C2) that recalibrating the budget number alone (O2) is the more proportionate fix" — this is not fully ruled out by the ground truths available here; it loses the formal comparison in chain C6 but only by a margin that a single-criterion weighting change can erase to a tie, and it would become the better-supported answer specifically if A-8 shows that most companion techniques fire on most real runs.
## Appendix — process output

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | Analog pays full cost of all 8 procedures per invocation | A-2 (analog representative of user's file) | Yes — A-2 |
| C1 | 2 | This is "unconditional cost for conditional need" | none beyond table | clean pass |
| C1 | 3 | Companion procedures = strongest extraction candidate | none beyond table | clean pass |
| C2 | 1 | Line→token bracket; overage ≈2,000–6,000 tokens | none beyond table (GT-4 already carries the estimate uncertainty) | clean pass |
| C2 | 2 | Window-exhaustion cost negligible in isolation | none beyond table | clean pass |
| C2 | 3 | Real justification must be ecosystem/signal-level | none beyond table | clean pass |
| C3 | 1 | 878-line file sits below platform warning threshold | none beyond table (GT-3? already flagged) | clean pass |
| C3 | 2 | ~500 is conservative margin, not a hard-threshold signal | none beyond table | clean pass |
| C4 | 1 | Extraction trades token saving for round-trip/omission risk | A-8 (real usage-frequency distribution unknown) | Yes — A-8 |
| C4 | 2 | Trade's favorability depends on usage frequency | none beyond table (A-8 already surfaced this step) | clean pass |
| C4 | 3 | The resolving measurement is unavailable to this analysis | none beyond table | clean pass |
| C5 | 1 | Methodology body excluded from extraction by definition | none beyond table | clean pass |
| C5 | 2 | Template/rubric: always-needed-but-late, safe to lazy-load | none beyond table | clean pass |
| C5 | 3 | Blanket split leaves template/rubric cost unchanged | none beyond table | clean pass |
| C5 | 4 | Category-differentiated intervention is correct | none beyond table | clean pass |
| C5 | 5 | 2nd-order, actor lens: maintainers must keep inline/external copies in sync | none beyond table (A-9's tooling question already covers this) | clean pass |
| C5 | 6 | 2nd-order, time lens: split adds extra turns to runs needing the fetches | none beyond table (GT-8 already covers round-trip cost) | clean pass |
| C5 | 7 | 3rd-order, actor lens: ungoverned future edits reintroduce the mismatch unseen | none beyond table | clean pass |
| C5 | 8 | 3rd-order, time lens: a green gate stops signalling real cost (Goodhart's-law risk) | none beyond table | clean pass |
| C6 | 1 | Weighted totals computed across 5 options | none beyond table | clean pass |
| C6 | 2 | Combined option (O5) beats split-alone (O3) by a thin, tie-able margin | none beyond table | clean pass |
| C6 | 3 | Thin margin supports sequencing O3 then O4 | A-9 (project tooling can compute a default-loaded-surface metric) | Yes — A-9 |
| C6 | 4 | O1/O0/O4-alone trail by a wide margin | none beyond table | clean pass |

Scan complete: 6 chains, 23 steps total, in order (including C5's 4-step second-order actor/time-lens extension); 3 assumptions surfaced (A-2, A-8, A-9), all previously unlisted and added to the Classified Assumptions Table in §2; 20 steps were a clean pass.

## Techniques not applied (process output)

Run mode: full-composer (no focused-technique trigger phrase fired in the request). Applied: Estimate (GT-4/chain C2 — magnitude rebuild of the line→token ratio, bracketed), Trade-off (chain C6 — weighted comparison of five interventions), Second-Order (actor lens + time lens, folded into the pre-mortem's cause generation and the Conclusion's trade-offs), Pre-Mortem (adversarial pass, below, since the headline conclusion is a plan/recommendation).

Not applied:
- five-whys (causal mode) — not applicable — no recurring symptom whose root cause needed tracing; the question is a design choice, not a diagnosed failure.
- five-whys (reduce-to-primitives mode) — not applicable — no single compound claim required formal recursive decomposition beyond what §3's ground truths already state as primitives (tokenization ratio, context-window mechanics, tool-call round-trip cost).
- fishbone — not applicable — the assumption space was enumerable directly with reasonable confidence (§2); it was not multi-causal in a way intuition could not reach.
- inversion (Phase 2 invocation) — not applicable — no conclusion or goal in this analysis presented as suspiciously clean before challenge; the assumption set was built from direct structural/mechanistic reasoning rather than from a thin, unexamined premise.
- inversion (Phase 5 invocation) — not applicable — the headline conclusion is a plan/recommendation, not a bare claim; per the decision rule, pre-mortem was selected instead and inversion's Phase-5 slot does not fire for a plan.
- theoretical-limit — not applicable — no governing hard physical/mathematical constraint sets a ceiling this decision turns on; the closest candidate (model context-window size) is shown by chain C2 to be far from binding, so deriving its exact ideal ceiling would not change the conclusion.

## Adversarial pass (process output)

**Recompute.** Line→token bracket (GT-4): 500 lines × 7–13 tok/line = 3,500–6,500 tokens (central 500×10=5,000, matches the stated figure); 878 lines × 7–13 = 6,146–11,414 tokens (central 878×10=8,780). Overage: 878/500 − 1 = 0.756 → 75.6%, matching the stated "~75% over." Trade-off weighted totals (chain C6), recomputed independently of the chain text: O0 = 1·5+5·4+5·3+5·2+1·3+1·2 = 5+20+15+10+3+2 = 55. O2 = 2·5+5·4+5·3+5·2+4·3+4·2 = 10+20+15+10+12+8 = 75. O4 = 3·5+5·4+5·3+2·2+3·3+3·2 = 15+20+15+4+9+6 = 69. O3 = 5·5+4·4+3·3+3·2+5·3+4·2 = 25+16+9+6+15+8 = 79. O5 = 5·5+4·4+4·3+2·2+5·3+5·2 = 25+16+12+4+15+10 = 82. (An earlier draft of this computation mis-summed O5 as 97; corrected here to 82 — the recompute step caught and fixed this before the figure was used in §4/§6.) Flip test: raising the implementation-effort criterion's weight from 2 to its maximum permitted value of 5 produces O3=88, O5=88 — an exact tie, not a reversal; no single-criterion weight change within the locked 1–5 range reverses the ranking outright. All chain-head arithmetic in §4 traces to GT-1–GT-8 as cited; no broken trace found.

**Sensitivity.** The single ground truth whose falsity would flip the conclusion is A-2 (not itself a GT, but the assumption every load-bearing chain's Inputs axis is capped by): if the user's actual plugin file is *not* loaded wholesale on every invocation the way the observed analog is — e.g., if its host already supports some partial/conditional loading within one file — chains C1, C4, C5, C6 lose their primary justification and the recommendation collapses toward O2 (recalibrate the budget number, no content reorganization). A-2 is `?`-equivalent (untested belief); verification path is named in C1's confidence line. The weakest link per chain: C1 — A-2's unverified transfer from analog to the user's actual file; C2 — GT-4's bracketed (not measured) token estimate; C3 — GT-3?'s unverified threshold figure; C4 — A-8's unmeasured usage-frequency distribution; C5 — inherits C1/C2/C4's weak links with no new one of its own; C6 — inherits C1's weak link plus GT-7?'s unverified ecosystem-convention claim.

**Rival.** Headline conclusion: strongest rival is O2 alone (recalibrate the budget number, no content split), on the grounds that C2 shows the absolute overage is small in window terms, so restructuring may be solving a non-problem at the margin. What keeps the headline conclusion ahead: C1/GT-5 show a real, checkable conditional-use mismatch independent of absolute magnitude, and C6's formal comparison scores O2 behind O3/O5 specifically on the cost-addressed and gate-meaningfulness criteria — but this rival is not ruled out, only outscored by a margin chain C6 itself shows is thin (§4; Abandoned Reasoning does not contain this rival because it remains live, not discarded). Intermediate chains: C1's rival ("inlining all 8 is fine because each procedure is short enough that the aggregate cost is negligible") is not ruled out — see rival not applicable — [no settling evidence available; flagged, not resolved] — this chain's own confidence line already carries the caveat. C2's rival ("the true tokens/line ratio for this specific file could be materially higher, e.g. if dense with tables") is not ruled out; GT-4's bracket already carries this uncertainty rather than resolving it.

**Premise.** It is two project milestones from now. The recommended intervention — differentiated extraction of the companion-tool procedures, lazy-loaded template/rubric, and a redefined CI gate metric — has already failed: the plugin's reliability or maintainability is worse than before the change, and the team wishes they had just raised the budget number instead.

**Causes** (generated from four viewpoints — the plugin maintainer, the invoked agent at runtime, the CI/tooling owner, and an external reviewer/integrator of the plugin):
- (Maintainer) The hand-split produced a duplicate pair per extracted procedure (an inline summary blurb plus a full external file) with no generate/sync script; a bug-fix edit touched only one copy and the two drifted within one milestone.
- (Maintainer) A ninth companion technique was added directly to an external reference file, but its trigger phrase was never added to the main body's routing logic, so the new technique is unreachable in practice.
- (Runtime agent) A Read call to a reference file failed mid-run (stale path after a refactor, missing file, permissions) and the run proceeded without the procedure it needed, producing a degraded analysis with no visible failure.
- (Runtime agent) The agent, mid-reasoning, simply omitted the Read call for a technique it needed — no hard gate forced the fetch — and the output still looked superficially complete.
- (CI/tooling owner) Building the "default-loaded-surface tokens" metric (O4/O5's second half) took longer than estimated; the team quietly reverted to the old raw-line-count gate, now pointed at an artificially small file because content had already moved out — green, but no longer measuring anything real.
- (External reviewer) A plugin reviewer who expected a single-file agent definition to be fully self-contained and auditable in one read is now missing context because key procedures live in files they did not know to open, making the plugin harder to audit from outside even though it looks smaller.

**Clusters:**
- **Cluster A — Split-but-not-synced** (causes 1, 2). No single source of truth maintaining the inline/external correspondence. Bears on: C1, C4, C5, C6 (the whole differentiated-extraction recommendation).
- **Cluster B — Fetch-time fragility** (causes 3, 4). Moving content from "always in context" to "fetched on demand" is a reliability risk, not only a latency cost. Bears on: C4, GT-8.
- **Cluster C — Metric gaming via incomplete redefinition** (cause 5). An abandoned O4 leaves the project with O3's content change plus a broken, silently-reverted gate — worse than either alone. Bears on: C6, options O4/O5.
- **Cluster D — Self-containment expectation broken** (cause 6). Externalizing content violates an unstated "one file, fully auditable" expectation. Bears on: C5, A-5.

**Disposition:**
- Cluster A — **Fatal, plan change required.** Ship the extraction only together with a generate/sync mechanism (or at minimum a CI check diffing each inline summary against its paired external file) — not as a later cleanup. Tripwire: a PR touching `shared/` or `references/` changes one copy without the other; owner: the reviewer of any such PR.
- Cluster B — **Costly but survivable, accepted risk with mitigation.** Mitigation: every fetch point is explicit, named, and scripted (as the methodology already prescribes for the analogous system), and any failed fetch is visibly disclosed rather than silently absorbed. Tripwire: a Read-call failure record appears in more than a small number of runs in a rolling window; owner: whoever reviews the plugin's own output/telemetry, if any exists.
- Cluster C — **Costly but survivable, plan change required.** Sequence O3 before O4; time-box O4; keep the old raw-line gate active as an imperfect-but-honest interim signal until O4 ships rather than silently dropping enforcement. Tripwire: O4 still open after one milestone; owner: the project's own roadmap/milestone tracking.
- Cluster D — **Tolerable, accepted risk with mitigation.** Mitigation: a prominent, visible reference-docs index in the main file (the analogous system already does this). Tripwire: a reviewer or new contributor asks "where is the rest of this agent's logic" within the first milestone after the split; owner: the README/docs maintainer.

**Falsification.** This analysis's recommendation is false if a real audit of invocation logs shows that most companion techniques fire on most actual runs (A-8 resolved high) — in that case extraction saves little real per-invocation cost, "conditional" is the wrong description in practice, and the better-supported fix collapses toward O2 (recalibrate the budget number) rather than O3/O5 (extract and/or redefine the metric).

## §6→§4 closure ledger (process output)

- "Do not treat "split into separate files" as a single, undifferentiated fix... extract those to on-demand reference files... (chain C1)... (chain C5)." → chain C1, chain C5 ✓
- "...a weighted comparison across five candidate interventions ranks doing both together highest... (chain C6)." → chain C6 ✓
- "The 878-vs-500 line gap is not one problem with one size... raw line count is a reasonably faithful proxy for that part's cost, and extraction genuinely fixes it... (chains C2, C3)." → chain C2, chain C3 ✓
- "Extraction trades a real-but-small reliability cost... depends on an unmeasured fact... (chain C4)." → chain C4 ✓
- "A pre-mortem run against this recommendation... surfaced a further, more structural risk..." → discharged by the adversarial pass record (process output, above), which this sentence directly names ("A pre-mortem run against this recommendation, below"); no separate chain citation needed for a sentence pointing at the adversarial pass rather than asserting a new traceable claim.
- "**Confidence:** MEDIUM — both chains this conclusion rests on are capped at MEDIUM by..." → discharged via D-07 naming chains C5 and C6 (both cited on the Pre-check `head` line) and assumptions A-2, A-8 ✓
- "**Rivals:** the strongest live, unsettled rival is... loses the formal comparison in chain C6..." → chain C6 ✓

Scan complete: 7 claims identified, 7 traced to a named chain or to the adversarial pass record; 0 cut.

## Self-audit scan (process output)

**Table 1 — chain form (section 4)**

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|---|---|---|---|---|---|---|---|
| C1 | GT-2 + GT-5 | yes | n/a | yes | MEDIUM | no | none |
| C2 | GT-1 + GT-4 | yes | n/a | yes | MEDIUM | no | none |
| C3 | GT-6 + GT-3? | yes | n/a | yes | LOW | no | none |
| C4 | C1 + GT-8 | yes | n/a | yes | MEDIUM | no | none |
| C5 | C1 + C2 + C4 | yes | n/a | yes | MEDIUM | no | none |
| C6 | C1 + GT-7? + GT-8 | yes | n/a (an earlier draft placed two prose paragraphs between the head and the first hop, violating the no-prose-before-first-arrow rule; corrected before this scan was taken — see Recompute note in the adversarial pass record) | yes | MEDIUM | no | none |

"Act attempted?" is `no` for every chain: no head input in this analysis required opening an external cited source via Read/Grep/WebFetch — GT-1 is the user's own problem statement (already in context), GT-2/GT-5 are this analysis's own direct reading of its own executing system prompt, GT-4 is a stated estimation method, and GT-3?/GT-7?/GT-8/GT-6 are general platform/mechanistic knowledge explicitly left unverified against a live external document this session (named on their own Ground Truths lines).

**Table 2 — claim inventory (section 6)**

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| Recommended approach | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1, C5, C6 |
| Key insight | bold lead-in | yes | same | C2, C3 |
| Trade-offs acknowledged | bold lead-in | yes | same | C4 (+ adversarial pass pointer) |
| Pre-check (Conclusion) | bold lead-in | yes | same | C5, C6 (self-citing) |
| Confidence (Conclusion) | bold lead-in | yes | same | C5, C6 |
| Rivals (within Confidence paragraph) | bold lead-in | yes | same | C6 |

Scan complete: 6 chain rows, one per section-4 chain block in order; 6 section-6 rows, one per construct in order — 6 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "Given a single monolithic Claude Code agent-definition file that bundles four content categories of different *access cadence*... under one static ~500-line/~5,000-token CI budget, and given that the file has grown 75% past that budget, determine what per-invocation cost the budget was actually sized to cap, whether the current overage reproduces that cost or merely the number, and what intervention actually targets the cost rather than the metric."
Band: **Rigorous**
Justification: The Essence Statement is a single distilled sentence naming the real decision (what cost is the budget for, does the overage reproduce it, what intervention fits), not the triggering event ("the file is over budget, split it"), and is followed by five checkable success criteria, none of which requires the answer to be exactly one of the named options.

**Criterion 2: Challenge Assumptions**
Quoted span (from the Assumption Audit scan, admitted source): "A-2 (analog representative of user's file) | Yes — A-2" and, from §2: "A-5: The four content categories are equally good candidates for extraction. | convention | Challenge directly against each category's access cadence. | Discard — ..."
Band: **Rigorous**
Justification: Every row in the Assumptions Table uses exactly one of the four prescribed Type values, each carries a specific (non-generic) Treatment, Verdict and Verification, the stakes-escalation rule is applied explicitly (A-1/A-2, A-8 named as the highest-stakes items), and the end-of-Phase-4 Assumption Audit scan shows three further assumptions (A-2, A-8, A-9) surfaced from chain steps and fed back into this same table, not left stranded.

**Criterion 3: Establish Ground Truths**
Quoted span: "GT-6 ... Provenance: general, well-established mechanics of transformer context windows and of documented prompt-caching behavior; not file-specific. No `?`, though the exact current caching mechanics were not re-verified against live docs this session (minor, non-load-bearing)."
Band: **Sound**
Justification: GT-IDs are stable, `?`-marked entries are enumerated by ID and match the table (GT-3, GT-7), and unsuffixed GTs feeding load-bearing chains name a read-at-source location where one exists (GT-1, GT-2, GT-5) — but GT-6 and GT-8, both load-bearing (cited by C2/C3 and C4/C5/C6 respectively), are justified by general/common-knowledge-style citation with no specific page, table, or passage named, which is the Sound descriptor's example of a shortfall rather than the Rigorous one.

**Criterion 4: Reason Upward**
Quoted span (from the self-audit scan Table 1, admitted source for this criterion): "C6 | C1 + GT-7? + GT-8 | yes | n/a (an earlier draft placed two prose paragraphs between the head and the first hop... corrected before this scan was taken...) | yes | MEDIUM | no | none"
Band: **Rigorous**
Justification: All six chains in Table 1 score Form conforming = yes and Dependency clean = yes after the disclosed C6 correction; every chain carries at least one intermediate hop; the end-of-phase Assumption Audit scan ran (23 steps) and fed three surfaced assumptions back into §2; the second-order procedure was applied with both the actor lens and the time lens explicitly walked and order-marked (`→[2nd, ...]`, `→[3rd, ...]`) as an extension of C5, and no extension step contradicts a Ground Truth; the Abandoned Reasoning section (§5) records four dead ends; no reference to the analogous system is used as standalone justification — GT-2/GT-5 are grounded as verified facts about that system specifically, and their generalization to the user's file is carried as the explicitly flagged assumption A-2, capping every chain that depends on it.

**Criterion 5: Validate**
Quoted span (from the adversarial pass record, admitted source): "An earlier draft of this computation mis-summed O5 as 97; corrected here to 82 — the recompute step caught and fixed this before the figure was used in §4/§6." and "Cluster A — Split-but-not-synced... Fatal, plan change required."
Band: **Rigorous**
Justification: All five stress-test steps (Recompute, Sensitivity, Rival, Adversarial technique, Falsification) are present with substantive content rather than not-applicable lines; Recompute independently re-derived the trade-off arithmetic and disclosed and fixed a genuine error found in drafting; the pre-mortem (chosen over inversion per the plan/claim decision rule) carries all four required parts (Premise, Causes from four named viewpoints, Clusters citing chain/GT ids, Disposition) with every cluster assigned a named plan change or an explicitly mitigated accepted risk and a tripwire; every weak link named in Sensitivity is either an existing flagged `?`/assumption with a stated verification path or is carried as an explicit confidence caveat.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (from the self-audit scan Table 2, admitted source): "Recommended approach | bold lead-in | yes | bold lead-in whose colon closes the bold span | C1, C5, C6" and, from the §6→§4 closure ledger: "Scan complete: 7 claims identified, 7 traced to a named chain or to the adversarial pass record; 0 cut."
Band: **Rigorous**
Justification: Every one of the six §6 constructs scored as a claim under R11 in Table 2 carries a cited chain, the §6→§4 closure ledger independently confirms 7/7 claims traced with zero cuts, and the Key Insight lead-in states a distinct claim (the budget-vs-number distinction) rather than restating the Recommended-approach lead-in's content.

**Gate result:** cleared · passes: 1 · Fix/Repeat fired: no

## Structured summary (process output)

```json
{
  "schema_version": 1,
  "run_mode": "full-composer",
  "assumptions": [
    {"id": "A-1", "type": "current constraint", "verdict": "Accept"},
    {"id": "A-2", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-3", "type": "convention", "verdict": "Challenge"},
    {"id": "A-4", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-5", "type": "convention", "verdict": "Discard"},
    {"id": "A-6", "type": "convention", "verdict": "Challenge"},
    {"id": "A-7", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-8", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-9", "type": "untested belief", "verdict": "Challenge"}
  ],
  "ground_truths": [
    {"id": "GT-1", "read_at_source": true},
    {"id": "GT-2", "read_at_source": true},
    {"id": "GT-3", "read_at_source": false},
    {"id": "GT-4", "read_at_source": true},
    {"id": "GT-5", "read_at_source": true},
    {"id": "GT-6", "read_at_source": true},
    {"id": "GT-7", "read_at_source": false},
    {"id": "GT-8", "read_at_source": true}
  ],
  "chains": [
    {"id": "C1", "confidence": "MEDIUM", "rests_on": ["GT-2", "GT-5"]},
    {"id": "C2", "confidence": "MEDIUM", "rests_on": ["GT-1", "GT-4"]},
    {"id": "C3", "confidence": "LOW", "rests_on": ["GT-6", "GT-3?"]},
    {"id": "C4", "confidence": "MEDIUM", "rests_on": ["C1", "GT-8"]},
    {"id": "C5", "confidence": "MEDIUM", "rests_on": ["C1", "C2", "C4"]},
    {"id": "C6", "confidence": "MEDIUM", "rests_on": ["C1", "GT-7?", "GT-8"]}
  ],
  "dead_ends": [
    "Treat the ~500-line/~5,000-token figure as a hard physical/platform constraint (a context-window ceiling)",
    "Assume the 878-line overage is scope creep / quality degradation needing a cut",
    "Recommend a blanket uniform split of all four categories into reference files (O1)",
    "Lead with the Claude Code startup-warning threshold (~15,000 tokens) as the primary justification for raising the budget"
  ],
  "techniques": {
    "applied": ["estimate", "trade-off", "second-order", "pre-mortem"],
    "not_applied": [
      {"technique": "five-whys", "phase": 3, "reason": "no single compound claim required formal recursive decomposition beyond what the ground truths already state as primitives"},
      {"technique": "fishbone", "phase": 2, "reason": "the assumption space was enumerable directly with reasonable confidence; not multi-causal in a way intuition could not reach"},
      {"technique": "inversion", "phase": 2, "reason": "no conclusion or goal presented as suspiciously clean before challenge"},
      {"technique": "inversion", "phase": 5, "reason": "the headline conclusion is a plan, not a claim; pre-mortem was selected instead per the decision rule"},
      {"technique": "theoretical-limit", "phase": 1, "reason": "the essence was not limited by a convention mistaken for a hard bound; reframing was not needed"},
      {"technique": "theoretical-limit", "phase": 4, "reason": "no governing hard physical/mathematical constraint sets a ceiling this decision turns on; the closest candidate (context-window size) is shown by chain C2 to be far from binding"}
    ]
  },
  "gate": {
    "passes": [
      {
        "bands": ["Rigorous", "Rigorous", "Sound", "Rigorous", "Rigorous", "Rigorous"],
        "gate_cleared": true,
        "hand_wavy_cap_cleared": true
      }
    ],
    "fix_repeat_fired": false,
    "cleared": true
  },
  "re_entry": {
    "fired": false,
    "edges": []
  },
  "conclusion": {
    "recommendation": "Do not treat \"split into separate files\" as a single, undifferentiated fix for a single, undifferentiated problem. Of the four stated content categories, only the companion-tool procedures show a genuine mismatch between how they are loaded (unconditionally, in full, on every invocation) and how they are used (conditionally, a subset per run) — extract those to on-demand reference files, each with an explicit, scripted fetch point rather than a discretionary one (chain C1). Keep the core methodology inline — it is needed from turn one of every run and is not a candidate for extraction at all. Lazy-load the output template and validation rubric once per run, late, the way the closely analogous live system already does safely — they are needed on nearly every run, so extraction buys little there, but moving their single late fetch out of the always-loaded body is a low-risk, already-demonstrated move (chain C5). In parallel, start (but do not block the content split on) redefining the CI gate's metric from raw file lines to something closer to \"default-loaded-surface tokens,\" so the gate measures what it actually cares about once the split exists; a weighted comparison across five candidate interventions ranks doing both together highest, only narrowly ahead of the content split alone, which supports sequencing — ship the extraction now, time-box the metric work as a tracked follow-on rather than a precondition (chain C6).",
    "confidence": "MEDIUM",
    "rests_on": ["C5", "C6"]
  }
}
```
