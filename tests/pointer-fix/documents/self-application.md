# Answer

**Recommendation:** Don't fix the number — fix what the number is a proxy for. The ~500-line/~5,000-token budget was never a measured bound against context-window capacity or reprocessing cost (both ruled out quantitatively, chain C1/C2); it was the file's size on the day the gate was written, now functioning as an unexamined anchor. The right move is a **hybrid**: split the always-loaded body down to control-flow plus a short index of what exists and when to fetch it; push the full companion-tool procedures, output template, and validation rubric into separate files, each paired with a mandatory, point-of-use "open this now" instruction left behind in the body (exactly the pattern this very skill already uses for its own template and rubric — chain C6, GT-8); re-derive the CI ceiling against the *always-loaded body alone* rather than total file size; and run a one-time content audit of the 378 added lines to separate load-bearing growth from redundant restatement before deciding what to cut versus relocate.

**Band (from §6):** MEDIUM (chain C7).

**Would change it:** Two closable gaps, named in C7/C5/C6: (1) a diff-based content audit of the 378 added lines — unavailable here per the problem statement's own "no codebase access" framing; (2) measured compliance data on whether an agent reliably executes forced "open this file" instructions across many runs, versus the single observed instance in this transcript.

*(Disclosed deviation: this analysis is delivered as direct text rather than as a file with figures/PDF/JSON summary, per this session's explicit instruction not to write report files — the Self-Audit Gate's full ceremony, the closure ledger ,and structured summary are abbreviated accordingly; the six-section analytical content below is complete and self-contained.)*

---

## 1. Problem Essence

**Essence:** Given a Claude Code plugin file that inlines a methodology, companion-tool procedures, an output template, and a validation rubric, and that has grown 75% past its recorded CI-enforced size budget through organic feature growth — what is the budget actually protecting, and does "extract into on-demand reference files" serve that protection or just satisfy the gate's letter while risking a correctness regression?

**Success criteria** (what a correct answer must achieve, not which option it must pick):
- Identifies the actual Claude Code loading mechanism for this file type and uses it to rule in/out context-window exhaustion and reprocessing cost as the operative constraint, with numbers, not intuition.
- Separates "878 lines is bloat" from "878 lines is legitimate capability growth" using a content-based test, not the line count alone.
- States whether extraction-with-lazy-loading structurally preserves or structurally risks the correctness of the companion tools and rubric, and under what condition each holds.
- Produces a recommendation justified against the real underlying objective, open to a hybrid rather than forced into picking exactly one of the four options named in the prompt.

## 2. Assumptions Table

| # | Assumption | Type | Treatment | Verdict/Verification |
|---|---|---|---|---|
| A1 | The file's full content is read into context whenever the agent is invoked, not loaded lazily by default (as stated by the user for this file type) | current constraint | Stands as the architecture's current behavior; expires if Claude Code's harness changes how it loads Skill/subagent files | Partially corroborated directly this session (see GT-1); treated as given per Input Contract, still classified rather than taken as a ground truth outright |
| A2 | The 500-line/5,000-token number was set when the file first shipped and never re-derived against a stated constraint | untested belief | Flagged `GT-6` derivative; not independently verifiable without the file's history, which is stipulated unavailable | Unverified — flagged; plausible by Occam's razor and by the scenario's own framing ("recorded budget," no stated rationale, two milestones of drift) |
| A3 | Large, monolithic specification files degrade a human reviewer's ability to catch contradictions between sections | convention (general SE practice) | Challenged: does this transfer to a progressive-disclosure Skill file the same way it does to a plain config file? | Accepted as directionally true but unquantified for this specific case — feeds GT-7? |
| A4 | Context-window size is large enough that ~5,000-8,750 tokens is immaterial to context capacity | physical-law-adjacent (verified against current model specs) | Verify via a live reference rather than recollection | Verified this session (GT-3) — upgraded from assumption to ground truth |
| A5 | Prompt caching makes steady-state reprocessing of a stable file cheap | current constraint (product pricing/mechanism) | Verify via a live reference | Verified this session (GT-4, GT-5) |
| A6 | Extraction into on-demand reference files reliably gets re-loaded when needed | untested belief, stakes-escalated (this is the crux the user is worried about) | Push toward verified: inspect whether the mechanism that makes this reliable (forced point-of-use fetch instructions) is actually present in a working precedent | Partially verified — the mechanism is directly observed working in this transcript (GT-8), but *compliance rate across many runs* was not measured; stays flagged |
| A7 | "Splitting" is a single intervention with one risk profile | convention / hidden framing in the prompt's own option list | Explicitly challenged in C6: split risk depends on whether a forced fetch instruction is paired with the extraction, not on extraction per se | Rejected as stated; replaced with a conditional claim in C6 |

`?`-marked ground truths carried forward: GT-2?, GT-6 (stipulated, not independently verified — "no codebase access"), GT-7?.

## 3. Ground Truths

- **GT-1** (read-at-source — directly observed in this conversation's own skill body): Claude Code Skills load the SKILL.md body in full into the invoking agent's context whenever the skill triggers; files the body merely references by path (e.g. `output-template.md`, `validation-rubric.md`, the per-technique `-detail.md` files) are **not** auto-loaded — they require an explicit `Read` call at the point of use, which the body states explicitly ("Open the rubric once, before scoring the first criterion," "Open the output template once, before assembling the document").
- **GT-2?** (unverified this session, but supplied by the user as context for this file type): Claude Code subagent definitions (Task-tool-dispatched, `.claude/agents/*.md`) are loaded in full as the system prompt for every new invocation of that subagent, not incrementally.
- **GT-3** (read-at-source — read just now from the `claude-api` skill's cached model table, dated 2026-09-25): current Claude models have context windows of 1,000,000 tokens (Opus/Sonnet/Fable tiers) or 200,000 tokens (Haiku 4.5, the smallest current window).
- **GT-4** (read-at-source — same reference, Prompt Caching Quick Reference): cache reads cost roughly $0.20–$0.25 per million tokens versus $1–$10 per million tokens for fresh input on current models (a ~90–98% discount); the minimum cacheable prefix is 512–4,096 tokens depending on model.
- **GT-5** (read-at-source — same reference): prompt caching uses exact prefix matching; any byte change anywhere in a cached prefix invalidates everything after it, so a frequently-edited file forfeits its cache discount on each edit.
- **GT-6** (stipulated by the problem statement, not independently verifiable — "no codebase access is needed or available"): the file grew from first-shipped size to 878 lines (~75% over its ~500-line/~5,000-token budget) over two milestones of organic feature growth, and the CI gate is presumably now failing, disabled, or overridden.
- **GT-7?** (unverified general domain knowledge, not read from a cited source this session): large monolithic specification files are a recognized maintainability/review-burden risk in software engineering generally, used as the rationale for line-count-style CI gates elsewhere.
- **GT-8** (read-at-source — directly observed in this conversation's own skill body): the real, already-shipped precedent for this exact kind of file does **not** split everything uniformly. It splits unconditionally-needed scaffolding (output template, validation rubric) out into separate files but pairs each with a forced, named, point-of-use re-fetch instruction in the always-loaded body — while situational content (individual companion-tool procedures, worked examples) is split out and fetched only when its own trigger condition fires, also via an instruction living in the always-loaded body.

`?`-marked: GT-2, GT-7 (2 of 8). Not read — none pending; GT-6 is a stipulated premise of the hypothetical rather than a claim this analysis could verify, per the prompt's own framing.

## 4. Derivation Chains

**C1 — context-window exhaustion is not the operative constraint**
```
GT-3 (context windows: 1M / 200K tokens) + GT-6 (878 lines ≈ 8,750 tokens, 75% over 5,000)
→ 8,750 tokens is 0.875%–4.4% of even the smallest current context window
→ at 75% over budget the file still consumes a low single-digit percentage of available context, with 20–100x headroom remaining
→ a budget tracking real context-window risk would be denominated in tens of thousands of tokens or as a % of window, not ~5,000 — context capacity was never the binding constraint this gate protects
```
**Pre-check:** head: GT-3, GT-6 · ?-marked: none · lowest cited: n/a · Inputs ceiling: HIGH.
**Confidence: HIGH**

**C2 — reprocessing cost/latency is a minor, mostly-solved concern, except for churn**
```
GT-4 (cache reads ~90–98% cheaper; min prefix cleared by both 5,000 and 8,750 tokens) + GT-5 (exact-prefix-match caching, invalidated by any edit)
→ once stable, the marginal cost of 8,750 vs. 5,000 tokens is a few cents per thousand invocations, not a material driver
→ the real cost risk is GT-5's edit-churn effect: frequent organic edits forfeit the cache discount every time, paying full fresh-token price until the file stabilizes again
→ reprocessing cost is a second-order concern whose real lever is edit frequency, not absolute file size — shrinking the file does nothing to fix churn-driven cache misses
```
**Pre-check:** head: GT-4, GT-5 · ?-marked: none · lowest cited: n/a · Inputs ceiling: HIGH.
**Confidence: MEDIUM** — flip condition: this reads cache economics from a dated, cached reference table inside a tool skill rather than Anthropic's live pricing page; magnitudes could shift, but the qualitative conclusion (discount is large, min-prefix is far below both 5,000 and 8,750 tokens) is robust to that. Rival (named, not fully settled): aggregate cost across many parallel invocations could matter at scale — true, but it scales identically whether the file is 5,000 or 8,750 tokens, so it argues for watching invocation volume, a different and unmeasured lever, not for this specific line-count gate.

**C3 — maintainability/review-burden is a real but line-count-blind proxy**
```
GT-7? (large monolithic specs degrade reviewer defect-detection) + GT-8 (precedent already splits always-needed scaffolding from situational detail)
→ a line-count CI gate is a cheap, mechanically-checkable stand-in for "can a reviewer hold this file's logic in their head and catch cross-section contradictions"
→ this proxy cannot distinguish 378 added lines of load-bearing new capability from 378 added lines of duplicated boilerplate — it fires identically either way
→ a 75%-over reading is evidence a maintainability review is now due, not by itself evidence the content is unhealthy
```
**Pre-check:** head: GT-7?, GT-8 · ?-marked: GT-7 · lowest cited: n/a · Inputs ceiling: MEDIUM.
**Confidence: MEDIUM** — the `?` on GT-7 would close by reading this project's own PR-review history or code-review research specific to agent-definition files rather than general SE lore; verification path: diff the file's growth since first-shipped and classify each added block as load-bearing vs. redundant (unavailable here per GT-6's stipulation).

**C4 — "conciseness as discipline" targets the always-loaded body specifically, not total spec size**
```
C3 (maintainability proxy) + GT-1 (SKILL.md body re-read in full on every trigger)
→ because the whole body, not a diff of it, competes for the model's attention on every invocation, a bloated always-loaded body costs more than tokens — it costs the salience of the instructions that matter most, alongside whatever the user actually asked for
→ this is a distinct proxy from pure maintainability: "is each inlined line pulling enough weight to justify displacing attention from every other inlined line," evaluated only against what's in GT-1's always-loaded half, not against content GT-1's on-demand half already lets grow for free
→ the forcing-discipline candidate from the four candidate objectives maps specifically onto body content, not onto total file size
```
**Pre-check:** head: C3 (MEDIUM), GT-1 · ?-marked: none directly, inherits C3's · lowest cited: MEDIUM · Inputs ceiling: MEDIUM.
**Confidence: MEDIUM** — the qualitative direction (less relevant inlined text reduces salience of what matters) is a well-supported practitioner heuristic; the magnitude at ~8,750 tokens inside a 1M-token window is unmeasured — no eval compared a lean vs. bloated version of this exact file.

**C5 — is 878 lines itself evidence of a problem?**
```
C3 + C4 + GT-8 (what remains inlined today is control-flow plus 8 companion-tool procedures the agent invokes mid-reasoning)
→ if the growth from first-shipped size is driven by new, load-bearing companion-tool procedures and rubric criteria (the scenario's own framing), the growth is healthy capability expansion, and the 500-line figure was never a calculated ceiling against any of the four candidate objectives — it was an anchor, not a derived bound
→ under that reading, 75%-over is evidence the number failed to track what it nominally gated, not evidence the file is unhealthy
→ this reading flips if a content audit instead shows the added lines are substantially duplicated restatement or copy-drift across sections — the actual bloat failure mode
→ the honest verdict is conditional: healthy to the extent added content is load-bearing, bloat to the extent it is redundant, and the line count alone cannot distinguish the two
```
**Pre-check:** head: C3 (MEDIUM), C4 (MEDIUM), GT-8 · ?-marked: none directly, inherits · lowest cited: MEDIUM · Inputs ceiling: MEDIUM.
**Confidence: MEDIUM** — explicitly conditional on an unperformed content audit (verification path: diff against first-shipped version, classify each added block). Rival (named, not fully settled): an ignored or disabled CI gate is itself a process failure regardless of content quality — true, but this is a parallel, procedural problem layered on top of whichever content verdict holds, not a rebuttal of C5; both are addressed in §6.

**C6 — does extraction-with-lazy-loading serve the real objective, or regress correctness?**
```
GT-1 (reference files require an explicit Read call) + GT-8 (precedent pairs every extraction with a forced, point-of-use fetch instruction in the always-loaded body)
→ extracting the validation rubric and output template is safe specifically because the always-loaded body retains an explicit, non-skippable instruction to open each one at a named step every run — the correctness guarantee lives in that forcing instruction, not in the extraction itself
→ extracting a companion-tool procedure used only conditionally is a different but equally safe bet, provided the trigger condition and the fetch instruction for it both live in the always-loaded body, so no run exists where the technique is needed but the instruction to fetch it is absent
→ extraction becomes unsafe only when a rule is removed from the body without leaving behind the paired fetch-and-trigger instruction — a sloppy extraction, not a property of extraction per se
→ the user's stated worry (silent breakage from content "that may or may not get loaded") is real but describes the sloppy case, not the paired case this precedent demonstrates
```
**Pre-check:** head: GT-1, GT-8 · ?-marked: none · lowest cited: n/a · Inputs ceiling: HIGH.
**Confidence: MEDIUM** — downgraded from the Inputs ceiling because of a live, unsettled Rival: LLM instruction-following is probabilistic, not deterministic, so "the file is in context" is categorically more reliable than "the file is in context only if the agent successfully executes a fetch call" — this tension is real and not resolved by the one working instance observed in this transcript. Verification that would raise this to HIGH: measured compliance-rate data for forced "open this file" instructions across many independent runs, not a single observation.

**C7 — recommendation**
```
C1 (context window not binding) + C2 (bulk reprocessing cost not binding; churn is the real minor cost) + C5 (878 lines conditionally healthy, pending unperformed audit) + C6 (split is safe only when paired with forced fetch instructions; compliance-rate rival unsettled)
→ the fix should target whichever objective C1–C4 actually isolate (maintainability, attention-dilution discipline), not the gate's literal number, since context-window and bulk-cost are ruled out
→ the lowest-risk, highest-value intervention matching GT-8's own validated precedent: keep control-flow plus a short index of what exists and when to fetch it in the always-loaded body; move full procedure/template/rubric text to separate files, each paired with an explicit point-of-use fetch instruction left in the body
→ in parallel, re-derive the CI ceiling against the always-loaded body specifically (not total file size), sized to an attention-dilution budget rather than left at its original anchor value
→ run the one-time content audit C3/C5 both name as missing, to separate load-bearing growth from redundant restatement before deciding what to cut versus relocate
```
**Pre-check:** head: C1 (HIGH), C2 (MEDIUM), C5 (MEDIUM), C6 (MEDIUM) · ?-marked: none directly, inherits GT-7? via C3→C5 · lowest cited: MEDIUM · Inputs ceiling: MEDIUM.
**Confidence: MEDIUM**

## 5. Abandoned Reasoning

- **"Context-window exhaustion is the driver."** Tested in C1; discarded outright on arithmetic (GT-3, GT-6 — 8,750 tokens is under 5% of even the smallest current window).
- **"Per-call reprocessing cost at scale is the driver."** Tested in C2; mostly discarded as the gate's rationale (cache discount dominates at this size), though the volume-scaling rival was named rather than refuted — it's orthogonal to what a line-count gate measures, so it doesn't restore cost as *this* gate's purpose.
- **"Just raise the budget to ~900 lines and move on."** Considered as one of the four user-offered options; rejected as a complete answer — it fixes the CI failure but answers nothing about whether the added content is redundant (C5) or about attention-dilution from inlining situational content (C4). Ruled out by GT-2 of §4's own exit test: picking exactly one named option without checking whether a hybrid dominates.
- **"Never split; keep it one monolith forever."** The opposite extreme; rejected because GT-1/GT-8 show this exact skill already runs a working partial extraction, directly observed functioning in this transcript — overcorrecting for a mitigated (not eliminated) risk is worse than addressing the residual risk (measuring fetch-instruction compliance) directly.

## 6. Conclusion

**Recommended approach:** Split the always-loaded body down to control flow plus a short index of what exists and when to fetch it; externalize the full companion-tool procedures, output template, and validation rubric into separate files, each paired with a mandatory, named, point-of-use fetch instruction left in the body (chain C7, grounded in GT-1/GT-8's already-working precedent). Re-derive the CI ceiling against the always-loaded body alone, not total file size (chain C4). Run a one-time content audit of the lines added since the file first shipped, to separate load-bearing growth from redundant restatement (chains C3, C5) before finalizing what gets cut versus relocated.

**Key insight:** The ~500-line gate was never a measured bound against any of the real candidate constraints — context window and reprocessing cost are both ruled out quantitatively (chains C1, C2), leaving maintainability and attention-dilution discipline as the only objectives it could plausibly serve, and neither of those is actually tracked by raw line count. It was the file's size on day one, an anchor mistaken for a derived limit (chain C5). The artifact under scrutiny already demonstrates, in its own shipped form, the surgical split that serves those real objectives without the correctness regression a naive "extract everything" instinct risks: the forced, point-of-use fetch instruction — not the extraction itself — is the load-bearing design element (chain C6, GT-8).

**Trade-offs acknowledged:** This recommendation defers the one step that would move several chains from MEDIUM to HIGH confidence (C3, C5, C7): a diff-based content audit, unavailable here because the scenario stipulates no codebase access. It also accepts a named, unresolved risk from chain C6: forced fetch instructions make lazy-loading safe only to the extent an agent reliably executes them, and that compliance rate was observed once in this transcript, not measured across runs.

**Confidence: MEDIUM** (chain C7). Would move to HIGH with: (1) the content audit separating load-bearing growth from redundant restatement in the lines added since first ship, and (2) measured compliance data for forced "open this file" instructions across many independent runs rather than one observed instance.