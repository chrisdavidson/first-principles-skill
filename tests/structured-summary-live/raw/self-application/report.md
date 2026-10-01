**Disclosed:** One re-entry edge fired: the Self-Audit Gate's Fix/Repeat loop. It was triggered because Criterion 3 scored Hand-wavy on the first pass (read-at-source ground truths fed only MEDIUM chains) and Criterion 5 found a miscalibrated rival on one chain. As a result, C2 was rebuilt, the old C5 was split into C5 and C6, the old C6 became C7, two dead ends were added, and the Essence Statement was tightened. Both passes are recorded under the Self-Audit Gate in the appendix.

## Answer

**Recommendation:** Don't split the body to meet the number. Remove the duplicated pre-mortem and trade-off procedures, report size in tokens with no threshold, and split only if a pre-registered large-difference A/B test shows harm (chain C7).

**Band (from §6):** MEDIUM (chain C7)

**Would change it:** A pre-registered A/B test showing harm at a large size difference would justify splitting now; one showing none would favour the status quo (chain C7). A tokenizer count, the model's published context window, and a measured read-compliance rate would close C6's gaps (chain C6).

# First-Principles Analysis: what the agent-body size budget optimizes for

All paths below are relative to `/home/chrisdavidson/Projects/first-principles-skill`. Figures were measured on the committed tree (the agent file was last changed in commit `f26d5ea2`, 2026-09-30, and has no uncommitted edits).

## 1. Problem Essence

**Core problem:** Which property, if any, the agent-body size budget (META-Q4, "~500 lines / ~5,000 tokens") actually protects, and which intervention best serves that property — including doing nothing, splitting, removing duplicates, measuring first, or a mix of these.

The prompt names three symptoms: the body is 878 lines, it is "~75% over", and the convention says to split it. None of these is the question. The question is which property the number stands for. An intervention chosen to make the number go green would treat the number as the goal, and that is the move this analysis is asked not to make.

**Success criteria:**
- SC1 — The Conclusion names the property the budget protects, with evidence, or states plainly that no property is measured.
- SC2 — Every figure the Conclusion states cites a chain whose hops show the arithmetic, and every such figure is recomputed independently in Phase 5.
- SC3 — The Conclusion's recommended intervention is justified by the property from SC1 and has been compared against the status quo and at least one composite option.
- SC4 — The Conclusion names the evidence that would change the recommendation.

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|------------|------|-----------|---------|--------------|
| A-1: The body violates the budget by about 75% (878 lines against 500) | untested belief | Verify against the current file | Challenge — the premise is stale. 878 was the line count on 2026-05-24. The file now has 1,236 lines (147.2% over), and on the token half of the budget it is about 6× over | GT-1, GT-2 |
| A-2: META-Q4 is a binding regression gate recorded in `.planning/REQUIREMENTS.md` | convention | Challenge before use | Discard — the requirement text is not in that file. The project matrix records the statement as unrecoverable and the requirement as audit-only, and nothing gates or reports the body's line count | GT-3, GT-4 |
| A-3: About 500 lines is a threshold beyond which this agent's output quality degrades | untested belief | Verify, or flag | Challenge — no measurement supports it. The limit was refitted 500, then 580, then 644 whenever it bound. The only A/B test compared a 22-line difference with n=3 per arm and says nothing about a 600+ line difference | GT-4, GT-5; load-bearing and unverified (from the inversion pass) |
| A-4: Line count measures the cost being budgeted | convention | Challenge before use | Discard — context load and per-call cost scale with tokens, not lines. This file averages about 24.1 tokens per line, while the budget's own pairing implies 10 | GT-1, GT-13? |
| A-5: Moving content into `references/` reduces what each run loads | untested belief | Verify | Challenge — true only for content that is needed conditionally and not already read on every trigger. When the trade-off or pre-mortem procedure fires, the body already requires reading its reference file, so the inline copy is loaded on top of it | GT-8, GT-9 |
| A-6: A split is a durable fix | untested belief | Verify | Discard — the split was already done once (892 to 419 lines on 2026-05-24) and the body grew back to 1,236 | GT-6, GT-7 |
| A-7: Anthropic's "keep SKILL.md body under 500 lines" guidance transfers unchanged to a subagent body | convention | Challenge before use | Challenge — the guidance assumes reference files cost nothing until read. A subagent body is always loaded in full, and each deferred read uses one of 60 turns and depends on the agent choosing to make the read | GT-10, GT-12, GT-15 |
| A-8: Content moved behind a "Read this file" instruction is reliably read | untested belief | Verify, or flag | Challenge — no measured read-compliance rate was found in the repository; flagged | unverified — flagged (GT-16?) |
| A-9: The context window is not the binding limit at the current body size | current constraint | Record when it would stop holding | Accept — holds until resident load plus reference reads plus transcript approach the window. It would stop holding if the window were smaller than the assumed 200k tokens or the body grew several-fold | unverified — flagged (GT-14?, window size) |
| A-10: Bytes ÷ 4 approximates the token count, within a 3.5–4.5 bytes-per-token bracket | convention | Challenge before use | Accept — used only as a bracketed estimate. No tokenizer was run, so it is flagged | unverified — flagged (GT-13?) |
| A-11: The growth rate over the last 129 days represents future growth | untested belief | Verify, or flag | Challenge — it is a two-point average across milestones of different kinds; flagged (surfaced by the assumption audit) | unverified — flagged |
| A-12: Removing the inline pre-mortem and trade-off copies changes no behaviour whenever the required read succeeds | untested belief | Verify, or flag | Accept — every substantive line of each inline copy appears verbatim in its reference file. The remaining risk is the read-failure path (surfaced by the assumption audit) | GT-8, GT-9 |
| A-13: Removing inline procedures requires changing the generator and the parity checks | untested belief | Verify, or flag | Challenge — `scripts/check-focused-parity.py` inspects `## Procedure` sections, but how much would have to change was not traced; flagged (surfaced by the assumption audit) | unverified — flagged (GT-17?) |

## 3. Ground Truths

The headline claim, "the body is ~75% over budget", was broken into three parts: the body's current size, the budget figure, and the budget's current standing. Each part was checked separately (five-whys, reduce-to-primitives mode). The results are GT-1 to GT-4.

- **GT-1** The agent body `first-principles/agents/first-principles.md` currently has 1,236 lines, 18,526 words and 119,194 bytes (measured) — source: `wc -l -w -c` on the committed file; read-at-source: the `wc` output `1236 18526 119194`.
- **GT-2** The body had exactly 878 lines at commits `74a9d33c` and `59c42b1a` (both 2026-05-24) (measured) — source: `git show <commit>:<path> | wc -l` across the file's history; read-at-source: the per-commit line counts.
- **GT-3** META-Q4 no longer appears in `.planning/REQUIREMENTS.md`. The project's requirements matrix records it as "statement unrecoverable", tier `audit-only`, with the note "nothing gates or reports the agent body's line count" — source: `grep META-Q4 .planning/REQUIREMENTS.md` (no match); read-at-source: `docs/requirements-matrix.md:80`.
- **GT-4** The body-budget gate was retired under TEARDOWN-01. The teardown record says the limit "was recalibrated whenever it bound, across the raise chain 500, then 580, then 644, rather than derived from any measured quality requirement". The same record says v8.6 "spent a whole milestone compressing the agent body to buy back 22 lines". The reporter script was later retired too — source: `docs/v8.7-constraint-teardown.md`; read-at-source: §2 item 1, lines 48–61; also `docs/v9.4-gate-retirement.md` §2.5, lines 833–880.
- **GT-5** The only blind quality A/B test of body length compared 590 lines with 612 lines. Both arms scored "2/3 PASS, band total 35", and the record's stated reading is "no detectable difference" — source: `docs/v8.6-quality-ab-experiment.md`; read-at-source: lines 22–23, 45–46 and 58. The 2/3 result means n = 3 runs per arm.
- **GT-6** The "split it" response has already been carried out once. Commit `6c37a5ba` ("stop inlining spine appendices into agent body") together with commit `acac7b37` ("sync agent surface after META-Q4 body extraction", 2026-05-24) took the body from 892 lines to 419 lines (28,651 bytes) — source: git history; read-at-source: the commit messages and `wc` output at both commits.
- **GT-7** Size of each region of the body after the split (`acac7b37`) and now (measured):

| Region | Lines then | Lines now | Bytes then | Bytes now | Bytes added |
|---|---|---|---|---|---|
| Header and Input Contract | 44 | 69 | 2,422 | 5,314 | 2,892 |
| Methodology | 97 | 232 | 12,060 | 41,915 | 29,855 |
| Output format | 31 | 175 | 1,359 | 17,420 | 16,061 |
| Before presenting conclusions | 13 | 139 | 498 | 17,526 | 17,028 |
| Skill files | 60 | 101 | 4,108 | 7,840 | 3,732 |
| Companion Techniques (inlined procedures) | 174 | 520 | 8,204 | 29,179 | 20,975 |
| **Total** | **419** | **1,236** | **28,651** | **119,194** | **90,543** |

  Source: `sed -n` byte counts over each heading's line range; read-at-source: heading line numbers from `grep -n '^## '` on both versions.
- **GT-8** Every substantive line (more than 20 characters) of three inline procedures appears verbatim in its reference file: inversion (body lines 857–902; 34 of 34 lines), pre-mortem (lines 903–970; 52 of 52), and trade-off (lines 971–1041; 57 of 57). The three blocks are 2,477, 3,777 and 4,350 bytes (measured) — source: `grep -Fxf references/<t>.md` against each inline block; read-at-source: that grep output.
- **GT-9** The body already requires the agent to open the trade-off reference with Read in Phase 4, and to open the pre-mortem or inversion reference with Read in Phase 5 ("The procedure is opened, not recalled"). If that Phase 5 read fails, the body says to "run the pass from the summary in Companion tools", which is not the inline procedure. Phase 2 uses "the inlined inversion procedure" without any read — source: the agent body; read-at-source: the Phase 2, Phase 4 and Phase 5 Operation paragraphs.
- **GT-10** Anthropic's skill-authoring guidance says: "Keep SKILL.md body under 500 lines for optimal performance. If your content exceeds this, split it into separate files". It gives the reason as "once Claude loads it, every token competes with conversation history and other context", and states that reference files "don't consume context tokens until actually read" — source: platform.claude.com, Skill authoring best practices; read-at-source: the "Technical notes › Token budgets", "Concise is key" and "Runtime environment" sections.
- **GT-11?** The ~500 figure in META-Q4 was copied from that guidance — unverified: the requirement statement cannot be recovered (GT-3), so the match in numbers is the only link.
- **GT-12** A subagent's whole body is loaded into its context on every invocation, conditionally needed procedures included (direct observation) — source: this run's own system prompt; read-at-source: it contains the body in full, through the theoretical-limit procedure at the end of "## Companion Techniques".
- **GT-13?** Tokens ≈ bytes ÷ 4, within a bracket of 3.5–4.5 bytes per token (estimate) — unverified: no tokenizer was run in this analysis.
- **GT-14?** The model's context window is at least 200k tokens (published design value, not measured here) — unverified: no documentation was opened for this model's window.
- **GT-15** The body's frontmatter sets `maxTurns: 60`. The file is generated from `shared/spine/SKILL-body.md` (660 lines) — source: the frontmatter and generated-file header; read-at-source: lines 1–15 of the agent body and `wc -l` on the spine file.
- **GT-16?** Content moved behind a "Read this file" instruction is sometimes not read. The body asserts the consequence ("a trailing `Confidence:` field going missing … is what that produces") — unverified: a search of `.planning/AGENT-EVAL*.md` and `docs/` found no measured read-compliance rate.
- **GT-17?** Removing inline procedures would require changes to `scripts/check-focused-parity.py`, which inspects `## Procedure` sections — unverified: the grep hits were seen, but how much would need to change was not traced.

**Provenance summary**
```text
?-marked: GT-11?, GT-13?, GT-14?, GT-16?, GT-17? (5 of 17)
Read-at-source: GT-1 wc output; GT-2 per-commit wc; GT-3 docs/requirements-matrix.md:80; GT-4 docs/v8.7-constraint-teardown.md §2 item 1 lines 48-61; GT-5 docs/v8.6-quality-ab-experiment.md lines 22-23, 45-46, 58; GT-6 commit messages 6c37a5ba/acac7b37 + wc; GT-7 region byte counts; GT-8 grep -Fxf output; GT-9 agent body Phase 2/4/5 Operation paragraphs; GT-10 platform.claude.com best-practices "Token budgets" section; GT-12 this run's system prompt; GT-15 agent frontmatter + wc of the spine file
```
Phase 3 failure records: none. Every load-bearing source that was attempted was opened, and the asserted figure or wording was found in it. GT-11?, GT-13?, GT-14?, GT-16? and GT-17? keep their `?` because no source exists for them, or none was attempted; none of them is the only support for a conclusion.

## 4. Derivation Chains

### Conclusion C1: No measured property stands behind the budget figure

GT-3 (statement unrecoverable, nothing gates) + GT-4 (refitted 500, then 580, then 644 whenever it bound) + GT-5 (22-line A/B, n=3, no detectable difference)
→ the requirement's own wording is gone, so the record no longer names a property the number protects
→ a limit raised each time it bound was tracking the body's size, not a fixed quality boundary
→ the one quality test spans 22 lines with 3 runs per arm and is silent about a 500-to-1,236 difference
→ no measured property stands behind "~500 lines / ~5,000 tokens", so any intervention must be justified by a property named somewhere else

**Pre-check:** head GT-3, GT-4, GT-5 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — every input was read at source, and each hop is a direct reading of those records. The strongest rival, "the budget is meaningless, so body length does not matter", over-reaches: a missing measurement is not a measured absence of effect. It is ruled out in §5 Dead End 1 using GT-5's 22-line scope.

### Conclusion C2: Line count is not a stable measure of how much text the body loads

GT-1 (1,236 lines, 119,194 bytes) + GT-2 (878 lines on 2026-05-24) + GT-6 (post-split body 419 lines, 28,651 bytes)
→ on lines the body is 1,236 ÷ 500 = 2.472, i.e. 147.2% over, not the prompt's 878 ÷ 500 = 1.756, i.e. 75.6% over
→ density rose from 28,651 ÷ 419 = 68.4 to 119,194 ÷ 1,236 = 96.4 bytes per line, a factor of 96.4 ÷ 68.4 ≈ 1.41
→ text volume therefore grew 119,194 ÷ 28,651 ≈ 4.16× while line count grew only 1,236 ÷ 419 ≈ 2.95×
→ the same line count carries different amounts of text over time, so a line figure cannot stand in for the volume of text the model loads

**Pre-check:** head GT-1, GT-2, GT-6 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — inputs were read at source (wc and git), and every hop is arithmetic that recomputes in the Phase 5 record. The rival "lines are close enough to text volume" is ruled out by hop 3's 1.41× divergence within one file's own history (§5 Dead End 8).

### Conclusion C3: Splitting cannot reach the line figure on its own, and does not address where growth comes from

GT-1 (1,236 lines now) + GT-7 (region sizes then and now) + GT-6 (the earlier split, 892 to 419) + GT-4 (one milestone of compression bought 22 lines)
→ moving all 520 Companion Techniques lines out leaves 1,236 − 520 = 716 lines, still 716 ÷ 500 = 1.432, i.e. 43.2% over
→ getting to 500 would mean moving another 716 − 500 = 216 lines out of the always-loaded core: methodology, output format and gate
→ the core supplied 62,944 of the 90,543 bytes added since the last split (69.5%), so most growth lands where a split cannot reach
→ at 90,543 bytes ÷ 129 days = 701.9 bytes per day, a 29,179-byte companion split is regrown in 29,179 ÷ 701.9 ≈ 41.6 days *[Assumes: A-11]*
→ cutting the 216 core lines by compression costs about 216 ÷ 22 ≈ 10 milestones at the one recorded rate
→ splitting reduces the current text but not the rate it grows, so the earlier 419-line result regrew to 1,236 (×2.95) and would again

**Pre-check:** head GT-1, GT-7, GT-6, GT-4 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — inputs read at source. A-11 is priced: if future growth were slower than 701.9 bytes per day, the regrowth time would lengthen, but the endpoint still stands. The 716 > 500 shortfall and the observed regrowth from 419 to 1,236 (GT-6) do not depend on the future rate. The rival "compress the core down to 500" is ruled out in §5 Dead End 2 using GT-4's recorded cost.

### Conclusion C4: The only measured waste is the duplicated pre-mortem and trade-off procedures

GT-8 (inline blocks verbatim in their references) + GT-9 (those references are read when the technique fires)
→ whenever trade-off or pre-mortem fires, its procedure is in context twice: once inline and once through the required read
→ whenever neither fires, the inline copy is loaded and never used
→ the 68 + 71 = 139 inline lines (3,777 + 4,350 = 8,127 bytes, 8,127 ÷ 119,194 = 6.8% of the body) do no work except as a read-failure fallback *[Assumes: A-12]*
→ removing those two copies is the only size cut backed by measurement, provided the trade-off read gets a named fallback the way Phase 5 already has one

**Pre-check:** head GT-8, GT-9 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — inputs read at source. A-12 is priced in the endpoint: if a pre-mortem read fails, the fallback the body already names is the Companion-tools summary, not the inline copy. For trade-off, the endpoint's proviso supplies the fallback. The inline inversion copy is deliberately kept, because Phase 2 uses it without a read (GT-9). The rival "the inline copies are the intended fallback" is ruled out by GT-9 for pre-mortem and handled by the proviso for trade-off (§5 Dead End 3).

### Conclusion C5: The 500-line guidance carries over as a token-versus-turns trade, not as a line threshold

GT-10 (500-line guidance; rationale is context competition; unread references cost nothing) + GT-12 (subagent body is always loaded in full) + GT-15 (maxTurns 60)
→ the guidance's reason for its limit is token competition, in a setting where content behind a reference costs nothing until it is read
→ in this subagent the whole body is loaded every time, and content moved behind a reference arrives only through a Read the agent must issue, using one of its 60 turns
→ what carries over is a trade between resident token load and turns plus read-issuance, so a fixed line count is not the transferable part

**Pre-check:** head GT-10, GT-12, GT-15 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — inputs read at source, and the hops are deductions from them. The endpoint is a ruling-out: it rejects "the 500-line threshold transfers as is", which does the rival's work.

### Conclusion C6: At its current size the body's token load binds no hard limit, and the token half of the budget was already exceeded after the split

C5 (HIGH) + GT-1 (119,194 bytes) + GT-6 (post-split 28,651 bytes) + GT-13? (bytes ÷ 4, bracket 3.5 to 4.5) + GT-14? (window ≥ 200k) + GT-16? (deferred reads are sometimes skipped)
→ resident load is 119,194 ÷ 4.5 to 119,194 ÷ 3.5, i.e. 26,488 to 34,055 tokens (central 29,799), which is 5.3× to 6.8× the 5,000-token figure
→ the 419-line post-split body already held 28,651 ÷ 4.5 to 28,651 ÷ 3.5, i.e. 6,367 to 8,186 tokens, so it passed the line half while failing the token half
→ at 13.2% to 17.0% of a 200k window, the current load binds no hard limit
→ moving content behind reads trades this load for turns at a read-compliance rate nobody has measured
→ the property gives a reason to prefer a smaller body, but no threshold that forces a structural change now

**Pre-check:** head C5 (HIGH), GT-1, GT-6, GT-13?, GT-14?, GT-16? · ?-marked: GT-13?, GT-14?, GT-16? · lowest cited: HIGH · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — only the Inputs axis is short. Three verifications would close it: a tokenizer count of both versions would remove GT-13?; reading the model's published context window would remove GT-14?; and measuring how often required reads actually happen, from captured run transcripts, would remove GT-16?. The token-half failure holds across the whole bracket (6,367 > 5,000). Even at a 100k window (an assumption), the share would be 26.5% to 34.1%: still not binding, but no longer negligible.

### Conclusion C7: Recommended intervention: a composite of removing duplicates, reporting size in tokens, and measuring before any split

C1 (HIGH) + C2 (HIGH) + C3 (HIGH) + C4 (HIGH) + C5 (HIGH) + C6 (MEDIUM)
→ O5, bringing back a 500-line gate, is knocked out because the number has no measured basis, which fails must-have M2
→ with weights fixed before scoring, the totals are O4 composite 59 > O0 status quo 53 = O2 remove-duplicates-only 53 > O1 companion split 35 > O3 split to 500 29 *[Assumes: A-13]*
→ the flip test finds one winner-changing move: raising the implementation-cost weight from 2 to 5 makes O0 win, 68 to 65
→ recommend O4: remove the duplicate copies now, report size in tokens with no threshold, and allow a split only if a pre-registered large-difference A/B shows harm
→[2nd] maintainers see each added rule as a token delta, so growth becomes visible where the retired reporter showed only a count
→[2nd] at the historical rate, the 8,127-byte saving is regrown in 8,127 ÷ 701.9 ≈ 11.6 days, so the cut is a cleanup and not a size strategy *[Assumes: A-11]*
→[3rd] a token report that sits long enough tends to become a target and get refitted, as 500, then 580, then 644 was, unless it carries no threshold

**Pre-check:** head C1 (HIGH), C2 (HIGH), C3 (HIGH), C4 (HIGH), C5 (HIGH), C6 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — C6 is rated MEDIUM and caps this chain; its own line gives the verification paths. A-13 is priced: if removing the procedures costs more than scored, O4's cost score drops from 2 to 1 and its total from 59 to 57, still above O0's 53. A-11 qualifies only a second-order extension, not the endpoint. The strongest rival, the status quo O0, is ruled out by the fixed-weight totals and survives only a +3 move on the cost weight (§5 Dead End 7). The pre-registered A/B is the observation that would reopen it.

## 5. Abandoned Reasoning

### Dead End 1: "The budget is meaningless, so body length does not matter"

**What was tried:** Going straight from C1 (no measured property) to the claim that length has no effect on quality, so the body can grow freely.

**Why abandoned:** The step from "not measured" to "no effect" is invalid. GT-5 tested only a 22-line difference with 3 runs per arm. It says nothing about a 1,236-line body compared with a 500- or 716-line body, and GT-10 names a real mechanism (token competition) that could act at larger differences. This is the rival to C1, and GT-5's scope rules it out.

**What it ruled out:** Treating the retirement of the gate as proof that size is free. Size is unpriced, not free. That is why C7 requires a measurement rather than accepting the status quo as settled.

### Dead End 2: Compressing the core prose until the body fits 500 lines

**What was tried:** Leaving the structure as it is and rewriting methodology, output-format and gate prose more tightly to remove the 216 lines a full companion split still leaves (C3).

**Why abandoned:** GT-4 records the one measured cost of this approach: a whole milestone of compression bought 22 lines. At that rate, 216 lines is about 216 ÷ 22 ≈ 9.8 milestones. The goal would also be a line figure that C1 shows has no basis and C2 shows is the wrong unit. C3 carries this ruling-out.

**What it ruled out:** Option O3 as a compression project. It also rules out any plan whose success test is "under 500 lines".

### Dead End 3: The inline pre-mortem and trade-off copies are the intended fallback

**What was tried:** Defending the duplicated inline procedures as deliberate redundancy for when a reference read fails.

**Why abandoned:** GT-9 shows the fallback the body actually names for a failed Phase 5 read is "the summary in Companion tools", not the inline procedure. For trade-off the body names no fallback at all, so the inline copy is an accidental fallback that nothing points to. C4 rules out the rival for pre-mortem and turns the trade-off case into a proviso.

**What it ruled out:** Keeping 8,127 bytes of exact duplicates on the grounds that they are a deliberate safety net.

### Dead End 4: "Split it" as the immediate intervention (option O1)

**What was tried:** Moving all eight Companion Techniques procedures into required reads, which takes the body to 716 lines.

**Why abandoned:** It does not reach the budget figure (716 is 43.2% over 500, per C3). It acts on an unmeasured belief (C1). It addresses at most 24.5% of the bytes, while 69.5% of recent growth landed in the core (C3). It replaces always-loaded content with turn-consuming reads whose compliance rate has not been measured (C5, C6). It scored 35 against O4's 59 (C7). The earlier split regrew to 2.95× its size (GT-6).

**What it ruled out:** Splitting without first measuring. O1 stays available as the action to take if the pre-registered A/B shows harm (C7).

### Dead End 5: Bringing back a line-count gate at 500 (option O5)

**What was tried:** Restoring META-Q4 as an enforced pre-commit gate.

**Why abandoned:** It fails must-have M2 (the intervention must be justified by a named, evidenced property). The number's history is a series of refits (GT-4), and its statement cannot be recovered (GT-3). C7 knocks it out before scoring.

**What it ruled out:** Any threshold-bearing gate until a dose-response measurement exists.

### Dead End 6: Using the context window as the governing hard limit (theoretical-limit framing)

**What was tried:** Treating the context window as the ceiling and deriving how much headroom the body has under it.

**Why abandoned:** At 26,488 to 34,055 tokens, the resident load is 13.2% to 17.0% of an assumed 200k window (C6). The ceiling is far from binding, so it cannot decide the question, and its value is itself unverified (GT-14?).

**What it ruled out:** Treating the question as one of physical capacity. It is a question of cost and adherence.

### Dead End 7: Leave the body as it is (status quo O0)

**What was tried:** Accepting the current body unchanged, on the grounds that no gate binds and the 22-line A/B found no effect.

**Why abandoned:** With weights fixed before scoring, O0 totals 53 against O4's 59 (C7). It has the lowest evidence-basis and durability scores of the non-split options, because it neither removes the measured duplication (C4) nor produces the missing measurement (C1). It wins only if implementation cost is weighted 5, equal to behavioural safety, which is a +3 move from the fixed weight.

**What it ruled out:** Treating "nothing currently fails" as a reason to stop. The status quo becomes the right answer again only if the pre-registered A/B finds no harm at a large size difference.

### Dead End 8: Treating line count as close enough to text volume

**What was tried:** Keeping lines as the budget unit on the grounds that lines and bytes move together.

**Why abandoned:** In this file's own history, bytes per line rose 1.41× (68.4 to 96.4), so text volume grew 4.16× while lines grew 2.95× (C2). A line figure therefore understates growth in exactly the quantity the guidance's rationale is about (GT-10).

**What it ruled out:** Any successor budget denominated in lines.

## 6. Conclusion

**Recommended approach:** Do not split the body to meet the number. Instead: (1) remove the inline pre-mortem and trade-off procedures, which duplicate references the body already requires the agent to read, and give the trade-off read a named fallback; (2) report the body's size in tokens, with no threshold attached; (3) pre-register a large-difference A/B test, the current body against a 716-line companion-split variant with run counts fixed in advance, and split only if that test shows harm (chain C7).

**Key insight:** The budget protects no measured property (chain C1). Its unit is unstable: text volume grew 4.16× while line count grew 2.95× (chain C2). The only property that carries over from the 500-line guidance is a trade between resident tokens and turns, not a threshold (chain C5). Splitting cannot reach 500 lines without moving always-needed core rules, and most growth happens in that core, so a split treats the current text while the variable that governs size is how fast it grows (chain C3).

**Trade-offs acknowledged:** The only immediate saving is small: 8,127 bytes, 6.8% of the body (chain C4). At the historical growth rate it is regrown in about 11.6 days (chain C7). Resident load stays at roughly 26k to 34k tokens until the A/B test reports (chain C6). Any token report risks becoming a refitted target the way the line gate did (chain C7).

- The current overrun is 147.2% on lines, not the 75% the prompt states (chain C2), and 5.3× to 6.8× on tokens (chain C6).

**Pre-check:** head C1 (HIGH), C2 (HIGH), C3 (HIGH), C4 (HIGH), C5 (HIGH), C6 (MEDIUM), C7 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — C6 and C7 are rated below HIGH (chain C7). C6's own §4 line gives the verification paths: a tokenizer count, the model's published context window, and a measured read-compliance rate. The pre-registered A/B in the recommendation is the observation that would decide between O4 and the status quo.

## Appendix — process output

## Provenance note (process output)

A `grep -rn META-Q4` run while locating the requirement listed matching lines from `first-principles/references/examples/self-application.md`. That file is the project's worked example on this same problem. It was not opened, and no ground truth, figure or chain in this analysis is taken from it. Every figure here was measured directly from the repository, its git history, or the cited documents.

## Trade-off (process output)

### Options
- **O0** — status quo: keep the 1,236-line body; no gate, no report.
- **O1** — split: move all eight Companion Techniques procedures into required reads (body becomes 716 lines).
- **O2** — remove duplicates only: delete the inline pre-mortem and trade-off copies (body becomes 1,236 − 139 = 1,097 lines; 119,194 − 8,127 = 111,067 bytes).
- **O3** — split to ≤ 500 lines: O1 plus moving 216 lines of core rules behind reads.
- **O4** — composite: O2 now, plus a token-denominated size report with no threshold, plus a pre-registered large-difference A/B test that decides whether O1 follows.
- **O5** — bring back a 500-line gate. **Knocked out** by must-have M2.

Must-haves: **M1** — every rule the run needs stays reachable when it is needed. **M2** — the intervention is justified by a named, evidenced property. O5 fails M2 (GT-3, GT-4). Every other option passes M1 on its face, and the risk to M1 is scored under criterion b.

### Criteria & Weights
Weights were fixed before any option was scored. Every criterion is phrased so that higher is better.

| Criterion | Weight | 1 means | 5 means | Ground truths |
|---|---|---|---|---|
| a. Reduction in resident token load | 3 | 0% | ≥ 50% (linear, about 12.5 percentage points per step) | GT-7, GT-8 |
| b. Behavioural safety | 5 | always-needed rules moved behind reads | no rule moved or changed in meaning | GT-9, GT-16? |
| c. Evidence basis | 4 | acts on an unmeasured belief | backed by measurement in this repo, or generates it | GT-4, GT-5, GT-8 |
| d. Durability against regrowth | 3 | addresses current size only | addresses the growth rate | GT-6, GT-7 |
| e. Low implementation cost | 2 | several phases with generator and test changes | trivial or none | GT-17? |

### Scoring
| Option | a (×3) | b (×5) | c (×4) | d (×3) | e (×2) | Total |
|---|---|---|---|---|---|---|
| O0 | 1 → 3 | 5 → 25 | 3 → 12 | 1 → 3 | 5 → 10 | **53** |
| O1 | 3 → 9 (24.5% cut: 1 + 24.5/12.5 ≈ 3) | 3 → 15 | 1 → 4 | 1 → 3 | 2 → 4 | **35** |
| O2 | 2 → 6 (6.8% cut: 1 + 6.8/12.5 ≈ 1.5, rounded up to 2) | 4 → 20 | 4 → 16 | 1 → 3 | 4 → 8 | **53** |
| O3 | 5 → 15 | 1 → 5 | 1 → 4 | 1 → 3 | 1 → 2 | **29** |
| O4 | 2 → 6 | 4 → 20 | 5 → 20 | 3 → 9 | 2 → 4 | **59** |

Sums: O0 3+25+12+3+10 = 53; O1 9+15+4+3+4 = 35; O2 6+20+16+3+8 = 53; O3 15+5+4+3+2 = 29; O4 6+20+20+9+4 = 59. These were recomputed by script, with identical results.

Notes on individual scores: b for O2 and O4 is 4, not 5, because the trade-off read-failure fallback must be added (C4). The c and e scores for O1 and O3 rest partly on GT-17? (parity-check scope not traced); per the trade-off procedure, the chain is capped at MEDIUM, and it already is MEDIUM through C6.

### Recommendation
**O4 at 59**, ahead of O0 and O2, which tie at 53.

Flip test, run over every single-weight move within 1–5:
- Cost weight e from 2 to 4 ties O4 with O0 at 63 each.
- Cost weight e from 2 to 5 flips the winner to O0: O0 = 3+25+12+3+25 = 68 against O4 = 6+20+20+9+10 = 65.
- Evidence weight c from 4 to 1 ties O4 with O0 at 44 each.
- No single-weight move makes O1, O2 or O3 the winner.

The smallest flip is +3 on the cost weight. It would mean treating implementation cost as equal in importance to behavioural safety, which is not defensible for an agent whose purpose is reliable analysis. The result is robust to everything except that move.

## Inversion pass, Phase 2 (process output)

Claim: "staying under ~500 lines protects this agent's output quality". Inverted: "staying under ~500 lines does not protect output quality". Conditions that would guarantee the inverted form, each with the precondition it negates:
1. Quality does not degrade with body length anywhere in the 500 to 1,236 range. Negated precondition: *quality degrades measurably in this range* — **load-bearing**, unverified, recorded as A-3.
2. Line count does not track the quantity that degrades. Negated precondition: *lines track tokens* — load-bearing, recorded as A-4 and discarded by C2.
3. The figure cannot be reached without moving rules the run always needs. Negated precondition: *500 is reachable by moving only conditional content* — load-bearing, refuted by C3.
4. Deferred content is not read when needed. Negated precondition: *required reads happen reliably* — recorded as A-8 (GT-16?).
5. The number was set by refitting, not by measurement. Negated precondition: *the figure was derived from a measured requirement* — refuted by GT-4.

The sharpest finding is precondition 1: it is both load-bearing and unverified. That is why C7 requires an A/B test.

## Techniques not applied (process output)

- fishbone — not applicable — the assumption space came from three enumerable record sources (requirements matrix, teardown record, A/B record). Category brainstorming would add breadth with nothing to discriminate between the branches.
- theoretical-limit (Phase 1 reframe) — not applicable — nobody claims the budget figure is a physical bound, so separating convention from hard bound does not reframe the question.
- theoretical-limit (Phase 4) — not applicable — the only hard ceiling, the context window, sits at least 5.9× above the resident load (200,000 ÷ 34,055) and its value is unverified (GT-14?). It cannot decide the question; the attempt is recorded as §5 Dead End 6.
- five-whys (causal mode) — not applicable — there is no recurring failure symptom to drill. Reduce-to-primitives mode was applied in Phase 3.
- inversion (Phase 5) — not applicable — the conclusion is a plan, so Phase 5 uses pre-mortem. Inversion was applied in Phase 2 (above).

## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | requirement's wording gone, no property named | no | n/a |
| C1 | 2 | refitted limit tracked size | no | n/a |
| C1 | 3 | A/B silent on large difference | no | n/a |
| C1 | 4 | no measured property behind the figure | no | n/a |
| C2 | 1 | 147.2% vs 75.6% over on lines | no | n/a |
| C2 | 2 | density 68.4 → 96.4 bytes per line (×1.41) | no | n/a |
| C2 | 3 | volume ×4.16 vs lines ×2.95 | no | n/a |
| C2 | 4 | line figure cannot stand in for text volume | no (A-4 already) | already A-4 |
| C3 | 1 | companion split leaves 716 lines | no | n/a |
| C3 | 2 | 216 core lines would have to move | no | n/a |
| C3 | 3 | core supplied 69.5% of growth | no | n/a |
| C3 | 4 | split regrown in about 41.6 days | yes — past growth rate continues | added A-11; step marked [Assumes: A-11] |
| C3 | 5 | compression ≈ 9.8 milestones | no | n/a |
| C3 | 6 | split treats current size, not growth | no | n/a |
| C4 | 1 | procedure loaded twice when fired | no | n/a |
| C4 | 2 | inline copy unused when not fired | no | n/a |
| C4 | 3 | 139 lines, 8,127 bytes redundant | yes — removal is behaviour-neutral when the read succeeds | added A-12; step marked [Assumes: A-12] |
| C4 | 4 | only measured cut, with fallback proviso | no | n/a |
| C5 | 1 | guidance rationale is token competition | no | n/a |
| C5 | 2 | deferred content needs an agent-issued Read costing a turn | no (A-7 already) | already A-7 |
| C5 | 3 | transferable part is the token/turn trade, not a line count | no (A-7 already) | already A-7 |
| C6 | 1 | 26,488 to 34,055 tokens, 5.3× to 6.8× | no (A-10 already) | already A-10 |
| C6 | 2 | 419-line body was 6,367 to 8,186 tokens | no (A-10 again) | already A-10 |
| C6 | 3 | 13.2% to 17.0% of 200k window | no (A-9 already) | already A-9 |
| C6 | 4 | read-compliance rate unmeasured | no (A-8 already) | already A-8 |
| C6 | 5 | no threshold forces action now | no | n/a |
| C7 | 1 | O5 knocked out by M2 | no | n/a |
| C7 | 2 | weighted totals | yes — removing procedures requires generator and parity changes (cost scores) | added A-13; step marked [Assumes: A-13] |
| C7 | 3 | flip test | no | n/a |
| C7 | 4 | recommend O4 | no | n/a |
| C7 | [2nd] | maintainers see token deltas | no | n/a |
| C7 | [2nd] | saving regrown in about 11.6 days | yes — A-11 again | already A-11; step marked [Assumes: A-11] |
| C7 | [3rd] | token report risks becoming a refitted target | no | n/a |

Each assumption has a single row in the Classified Assumptions Table. Every step that rests on an assumption added by this audit (A-11, A-12, A-13) carries the inline mark.

## Adversarial pass (process output)

**Recompute** — every figure was recomputed by an independent route: by subtraction or difference where the chain divides, and by script where it sums.
- 878 ÷ 500 = 1.756 → 75.6% over. Check: 500 × 1.756 = 878 ✓.
- 1,236 ÷ 500 = 2.472 → 147.2% over. Check: 1,236 − 500 = 736, and 736 ÷ 500 = 1.472 ✓.
- 119,194 ÷ 1,236 = 96.435 bytes per line. Check: 96.435 × 1,236 = 119,193.7 ✓. At 4 bytes per token that is 24.11 tokens per line ✓.
- 5,000 × 4 ÷ 96.435 = 207.4 lines. Check: 207.4 × 96.435 ÷ 4 = 5,000.1 ✓.
- 28,651 ÷ 4.5 = 6,366.9; ÷ 4 = 7,162.75; ÷ 3.5 = 8,186.0. All exceed 5,000 ✓. Pre-split density 28,651 ÷ 419 = 68.38 bytes per line ✓. Density ratio 96.435 ÷ 68.379 = 1.410 ✓. Volume ratio 119,194 ÷ 28,651 = 4.160 ✓. Cross-check: 4.160 ÷ 2.950 = 1.410, matching the density ratio ✓.
- Token bracket: 119,194 ÷ 4.5 = 26,487.6; ÷ 4 = 29,798.5; ÷ 3.5 = 34,055.4. Ratios to 5,000 are 5.30, 5.96 and 6.81 ✓. Words × 1.33 = 24,639.6, which falls just below the bracket and is consistent with prose-heavy text.
- Region totals: then 2,422 + 12,060 + 1,359 + 498 + 4,108 + 8,204 = 28,651 ✓ (matches wc); now 5,314 + 41,915 + 17,420 + 17,526 + 7,840 + 29,179 = 119,194 ✓ (matches wc). Lines: 44 + 97 + 31 + 13 + 60 + 174 = 419 ✓; 69 + 232 + 175 + 139 + 101 + 520 = 1,236 ✓.
- Growth: 119,194 − 28,651 = 90,543 bytes. Check against the per-region additions: 2,892 + 29,855 + 16,061 + 17,028 + 3,732 + 20,975 = 90,543 ✓. Core: 29,855 + 16,061 + 17,028 = 62,944 → 62,944 ÷ 90,543 = 69.5% ✓. Companion: 20,975 ÷ 90,543 = 23.2%. Remainder: (2,892 + 3,732) ÷ 90,543 = 7.3%. Shares sum to 69.5 + 23.2 + 7.3 = 100.0 ✓.
- Days from 2026-05-24 to 2026-09-30: 7 + 30 + 31 + 31 + 30 = 129 ✓. Rates: 817 ÷ 129 = 6.33 lines per day; 90,543 ÷ 129 = 701.9 bytes per day ✓.
- Split: 1,236 − 520 = 716 lines; 716 ÷ 500 = 1.432 ✓; 716 − 500 = 216 ✓. 119,194 − 29,179 = 90,015 bytes. Companion share 29,179 ÷ 119,194 = 24.5% ✓.
- Regrowth: 29,179 ÷ 701.9 = 41.57 days ✓; 8,127 ÷ 701.9 = 11.58 days ✓. Overall body ratio 1,236 ÷ 419 = 2.950 ✓.
- Duplicates: 68 + 71 = 139 lines; 3,777 + 4,350 = 8,127 bytes; 8,127 ÷ 119,194 = 6.82% ✓; 1,236 − 139 = 1,097 lines ✓.
- Window share: 26,488 ÷ 200,000 = 13.2%; 34,055 ÷ 200,000 = 17.0% ✓. At 100k the shares are 26.5% and 34.1% ✓. 200,000 ÷ 34,055 = 5.87 ✓.
- Compression: 216 ÷ 22 = 9.82 milestones ✓.
- Trade-off totals and flip results were recomputed by script, identical to the matrix ✓.

Every combined figure lands where its operation should put it. Each ratio above 1 was computed from a numerator larger than its denominator, and the part-shares sum to 100%.

**Sensitivity** — The ground truth whose falsity would flip the headline is GT-5's implied silence on large differences, i.e. A-3. If body length is already known to harm quality between 716 and 1,236 lines, O1 (split now) beats "measure first". A-3 is unverified, and resolving it is exactly what O4's A/B test does; the effect on confidence is carried on C7's MEDIUM line. Weakest link per chain:
- C1: hop 3 (the A/B scope reading).
- C2: hop 4 (from text volume to model load), which C6 quantifies.
- C3: hop 4 (A-11, the growth rate).
- C4: the trade-off read-fallback proviso.
- C5: hop 2 (that a deferred read needs the agent to issue it), a structural fact.
- C6: GT-16? (read-compliance), which bears directly on whether a split is safe.
- C7: the cost weight, where the flip distance is +3.

**Rival** — Headline: status quo O0. It is ruled out by C7's fixed-weight totals and survives only a +3 move on the cost weight → §5 Dead End 7, as stated on C7's Confidence line. C1: "length does not matter" → §5 Dead End 1. C2: "lines are close enough to text volume" → §5 Dead End 8. C3: "compress the core to 500" → §5 Dead End 2. C4: "the inline copies are the intended fallback" → §5 Dead End 3. C5: rival not applicable — C5's endpoint is itself a ruling-out of "the 500-line threshold transfers as is". C6: "a context-window ceiling forces action" → §5 Dead End 6. "Split now" (O1) → §5 Dead End 4. "Bring back the gate" (O5) → §5 Dead End 5.

**Premise** — It is March 2027. The O4 plan has failed: the body is larger than ever, no A/B test was ever run, and the token report has quietly become a new fitted gate.

**Causes** (unfiltered; viewpoints are the maintainer/author, the dispatching user of the agent, the evaluator paying for the A/B runs, and the owner of the generator and parity tooling):
1. Maintainer: the A/B test was deferred milestone after milestone because no defect forced it.
2. Maintainer: new rules kept being added to the core after each eval finding, at the same 700-bytes-per-day rate.
3. Maintainer: the token report got a "soft" threshold, which was then raised each time it bound.
4. Evaluator: the A/B was run with 3 runs per arm, came back null, and was read as "size is free".
5. Evaluator: the outcome measure was gate pass rate alone, which cannot see quieter adherence losses.
6. Evaluator: the run budget for the A/B was cut and the test was abandoned partway.
7. Tooling owner: removing the inline copies broke the parity checks, the fix took a phase, and the duplicates were restored.
8. Tooling owner: the generator was changed, but the trade-off fallback line was forgotten, so a failed read left no procedure at all.
9. Dispatching user: runs got slower and more expensive as resident load grew past 40k tokens, and nobody connected the cause.
10. Dispatching user: a split variant tested in the A/B dropped confidence fields because required reads were skipped.

**Clusters**
- **K1 — The measurement never happens or is underpowered** (causes 1, 4, 5, 6). Bears on C7 and C1, and on GT-5. Triage: fatal, because the plan's decision rule depends on it.
- **K2 — The report becomes a refitted gate** (cause 3). Bears on C7's [3rd] step and GT-4. Triage: costly but survivable.
- **K3 — Growth continues unabated** (causes 2, 9). Bears on C3 and C7's [2nd] step. Triage: costly but survivable.
- **K4 — Tooling friction or a missing fallback in the dedupe change** (causes 7, 8). Bears on C4 and GT-17?. Triage: costly but survivable.
- **K5 — Deferred reads are skipped** (cause 10). Bears on C6 and GT-16?. Triage: tolerable for O4 itself, since O4 moves no rule behind a new read; it matters to the O1 follow-on.

**Disposition**
- **K1** — Plan change: write the A/B pre-registration (arms, run count fixed above GT-5's 3 per arm, outcome measures including gate pass rate, turns used and confidence-field presence, and the meaning of a null result as "inconclusive" rather than "no effect") **before** the dedupe change lands. Tripwire: no pre-registration document by 2026-10-31, visible to the maintainer in the planning state.
- **K2** — Accepted risk with a named mitigation: the report states a figure and a trend only, with no threshold field. A threshold may be added only by citing a dose-response result. Tripwire: any commit adding a numeric limit to the report, seen at review.
- **K3** — Accepted risk with a named mitigation: the token report shows per-milestone growth, so growth is visible, and the dedupe is presented as a cleanup rather than a size strategy. Tripwire: per-milestone growth above about 700 bytes per day, read off the report at each milestone close.
- **K4** — Plan change: the dedupe change includes a one-line trade-off read fallback pointing at the Companion-tools summary, and the parity-check impact (GT-17?) is traced before the change is planned. Tripwire: a parity-check failure on the dedupe branch, seen in the pre-commit run.
- **K5** — Accepted risk with a named mitigation: the A/B's split arm measures read compliance directly (the GT-16? verification), so the O1 decision is never taken without that number.

**Falsification** — The conclusion is false if any of the following is observed: a pre-registered A/B test at a large size difference finds measurably worse output from the 1,236-line body, which makes O1 right now rather than conditionally; the original META-Q4 statement is recovered and names a measured property the line figure was derived from; or a tokenizer count shows the body's token load is far from the 26k to 34k bracket, which would change C6.

## §6→§4 closure ledger (process output)

- "Do not split the body to meet the number. Instead: (1) remove the inline pre-mortem and trade-off procedures … split only if that test shows harm" → chain C7 ✓
- "The budget protects no measured property … the variable that governs size is how fast it grows" → chains C1, C2, C5, C3 ✓
- "The only immediate saving is small: 8,127 bytes … the way the line gate did" → chains C4, C7, C6 ✓
- "The current overrun is 147.2% on lines, not the 75% the prompt states, and 5.3× to 6.8× on tokens" → chains C2, C6 ✓
- "Pre-check: head C1 (HIGH) … Inputs ceiling: MEDIUM" → chains C1–C7 ✓
- "Confidence: MEDIUM — C6 and C7 are rated below HIGH …" → chain C7 (names C6, C7) ✓

No claim was cut. The ledger was re-verified after the Fix step renumbered the chains (the former C5 was split into C5 and C6, and the former C6 became C7).

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|---|---|---|---|---|---|---|---|
| C1 | GT-3 + GT-4 + GT-5 | unreached | n/a — hops 3–4 sit beyond the check's reach for the GT-led-hop (R9) and sentence-closing-hop (R10) positions; no violation by inspection | yes | HIGH | yes | Fix/Repeat (re-scan only; chain text unchanged) |
| C2 | GT-1 + GT-2 + GT-6 | unreached | n/a — hops 3–4 beyond the check's reach (R9, R10); no violation by inspection | yes | HIGH | yes | Fix/Repeat (rebuilt: GT-13? and token hops moved to C6) |
| C3 | GT-1 + GT-7 + GT-6 + GT-4 | unreached | n/a — hops 3–6 beyond the check's reach (R9, R10); no violation by inspection | yes | HIGH | yes | Fix/Repeat (GT-1 added to head) |
| C4 | GT-8 + GT-9 | unreached | n/a — hops 3–4 beyond the check's reach (R9, R10); no violation by inspection | yes | HIGH | yes | Fix/Repeat (re-scan only; chain text unchanged) |
| C5 | GT-10 + GT-12 + GT-15 | unreached | n/a — hop 3 beyond the check's reach (R9, R10); no violation by inspection | yes | HIGH | yes | Fix/Repeat (split from former C5) |
| C6 | C5 + GT-1 + GT-6 + GT-13? + GT-14? + GT-16? | unreached | n/a — hops 3–5 beyond the check's reach (R9, R10); no violation by inspection | yes — C5 is upstream; no cycle | MEDIUM | yes | Fix/Repeat (split from former C5) |
| C7 | C1 + C2 + C3 + C4 + C5 + C6 | unreached | n/a — hops 3–7, including order-marked extensions, beyond the check's reach (R9, R10); no violation by inspection | yes — no cycle; all inputs resolve to upstream chains | MEDIUM | no | Fix/Repeat (renumbered from C6; rival moved to §5 Dead End 7) |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| Recommended approach: do not split; remove duplicates; token report; pre-registered A/B | bold lead-in | yes | bold lead-in whose colon closes the bold span (prescribed lead-in) | C7 |
| Key insight: no measured property; unstable unit; token/turn trade; growth governs size | bold lead-in | yes | bold lead-in whose colon closes the bold span (prescribed lead-in) | C1, C2, C5, C3 |
| Trade-offs acknowledged: 8,127-byte saving; regrowth; resident load; target risk | bold lead-in | yes | bold lead-in whose colon closes the bold span (prescribed lead-in) | C4, C7, C6 |
| Overrun is 147.2% on lines, 5.3× to 6.8× on tokens | list item | yes | list item that closes its own sentence and runs past forty characters | C2, C6 |
| Pre-check: head C1–C7 · Inputs ceiling MEDIUM | bold lead-in | yes | bold lead-in whose colon closes the bold span; cited by the chains its head names | C1, C2, C3, C4, C5, C6, C7 |
| Confidence: MEDIUM — C6, C7 below HIGH | bold lead-in | yes | bold lead-in whose colon closes the bold span (prescribed lead-in; discharged through the chains it names) | C7 |

```text
Scan complete: 7 chain rows, one per section-4 chain block in order; 6 section-6 rows, one per construct in order — 6 claims under R11, 0 excluded. 0 chains malformed, 0 claims untraced.
```

## Self-Audit Gate (process output)

**Pass 1 (before re-score):** Criterion 1 Sound · Criterion 2 Sound · Criterion 3 Hand-wavy · Criterion 4 Rigorous · Criterion 5 Sound · Criterion 6 Rigorous · Gate cleared: yes · Hand-wavy cap cleared: yes

Pass 1 findings, and what the Fix step changed:
- **Criterion 1** — the Essence Statement was two sentences, and SC2 was not a property of the Conclusion. Fix: rewritten as one sentence, and every SC now names what the Conclusion must show.
- **Criterion 2** — the A-9 and A-13 Verification cells lacked "unverified — flagged". Fix: added.
- **Criterion 3** — GT-1, GT-2, GT-10, GT-12 and GT-15 were read at source but fed only MEDIUM chains. Fix: acquire-before-downgrade did not apply, because they were already read. Instead the chains were restructured: C2 was rebuilt without GT-13?, the old C5 was split into C5 (HIGH, read inputs only) and C6 (MEDIUM, the `?` inputs), and GT-1 was added to C3's head.
- **Criterion 5** — old C6 carried MEDIUM while its Rivals axis was written as "live", which would make two axes short. Fix: the status-quo rival was recorded as ruled out (§5 Dead End 7) and the chain was renumbered C7.

**Criterion 1: Identify Essence**
Quoted span: "**Core problem:** Which property, if any, the agent-body size budget (META-Q4, "~500 lines / ~5,000 tokens") actually protects, and which intervention best serves that property — including doing nothing, splitting, removing duplicates, measuring first, or a mix of these." and "SC1 — The Conclusion names the property the budget protects, with evidence, or states plainly that no property is measured."
Band: **Rigorous**
Justification: The Essence Statement is a single sentence naming the underlying question (the protected property), not the symptom ("878 lines") or the triggering convention ("split it"). Each SC is a verb + subject + outcome test checked against the Conclusion section.

**Criterion 2: Challenge Assumptions**
Quoted span: "| C7 | 2 | weighted totals | yes — removing procedures requires generator and parity changes (cost scores) | added A-13; step marked [Assumes: A-13] |" and, from §2, "| unverified — flagged (GT-17?) |"
Band: **Rigorous**
Justification: All 13 rows use the four-type scheme, with em-dash verdicts and specific verification. Ten rows are Challenged or Discarded. Every unverified assumption used in a chain (A-8 to A-11, A-13) reads "unverified — flagged". The audit table has one row for each of the 33 chain steps, in order.

**Criterion 3: Establish Ground Truths**
Quoted span: Comparison — enumerated "GT-11?, GT-13?, GT-14?, GT-16?, GT-17? (5 of 17)"; the list carries `?` on exactly those five. Every unsuffixed GT (1–10, 12, 15) feeds at least one HIGH chain (GT-1, GT-2 and GT-6 → C2; GT-3 to GT-5 → C1; GT-7 → C3; GT-8 and GT-9 → C4; GT-10, GT-12 and GT-15 → C5), and each names its read-at-source location.
Band: **Rigorous**
Justification: Stable IDs, a provenance label on every entry, an enumeration that matches the list, and a named read location for every unsuffixed GT feeding a HIGH chain. No Discarded assumption appears in the list.

**Criterion 4: Reason Upward**
Quoted span: "| C2 | GT-1 + GT-2 + GT-6 | unreached | n/a — hops 3–4 beyond the check's reach (R9, R10); no violation by inspection | yes | HIGH | yes | Fix/Repeat (rebuilt: GT-13? and token hops moved to C6) |"
Band: **Sound**
Justification: Every conclusion has exactly one arrow-led chain with genuine intermediates, clean dependencies, declared `[Assumes]` premises and arithmetic that recomputes in the Phase 5 record. §5 carries eight structured dead ends. But every chain-form row reads `unreached` for hops past the second, and the rubric forbids scoring those positions as conforming on inspection alone, so this criterion stops short of Rigorous.

**Criterion 5: Validate**
Quoted span: "**Confidence:** MEDIUM — only the Inputs axis is short. Three verifications would close it: a tokenizer count of both versions would remove GT-13?; reading the model's published context window would remove GT-14?; and measuring how often required reads actually happen, from captured run transcripts, would remove GT-16?."
Band: **Rigorous**
Justification: Each band equals what its three axes license. C1 to C5 are HIGH with read inputs and priced `[Assumes]`; C6 is MEDIUM with each `GT-N?` named alongside its verification; C7 is capped by C6; §6 is MEDIUM, matching the weakest contributing chain. The adversarial record carries every part, and every cluster has a disposition.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: "| Key insight: no measured property; unstable unit; token/turn trade; growth governs size | bold lead-in | yes | bold lead-in whose colon closes the bold span (prescribed lead-in) | C1, C2, C5, C3 |"
Band: **Rigorous**
Justification: All six §6 claims cite chains, and none is untraced. The Key Insight (the number is unanchored, its unit is unstable, and growth rather than current size governs) is a finding the "split it" convention does not reach, not a restatement of the recommendation.

**Gate result:** cleared · passes: 2 · Fix/Repeat fired: yes

## Structured summary (process output)

```json
{
  "schema_version": 1,
  "run_mode": "full-composer",
  "assumptions": [
    {
      "id": "A-1",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-2",
      "type": "convention",
      "verdict": "Discard"
    },
    {
      "id": "A-3",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-4",
      "type": "convention",
      "verdict": "Discard"
    },
    {
      "id": "A-5",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-6",
      "type": "untested belief",
      "verdict": "Discard"
    },
    {
      "id": "A-7",
      "type": "convention",
      "verdict": "Challenge"
    },
    {
      "id": "A-8",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-9",
      "type": "current constraint",
      "verdict": "Accept"
    },
    {
      "id": "A-10",
      "type": "convention",
      "verdict": "Accept"
    },
    {
      "id": "A-11",
      "type": "untested belief",
      "verdict": "Challenge"
    },
    {
      "id": "A-12",
      "type": "untested belief",
      "verdict": "Accept"
    },
    {
      "id": "A-13",
      "type": "untested belief",
      "verdict": "Challenge"
    }
  ],
  "ground_truths": [
    {
      "id": "GT-1",
      "read_at_source": true
    },
    {
      "id": "GT-2",
      "read_at_source": true
    },
    {
      "id": "GT-3",
      "read_at_source": true
    },
    {
      "id": "GT-4",
      "read_at_source": true
    },
    {
      "id": "GT-5",
      "read_at_source": true
    },
    {
      "id": "GT-6",
      "read_at_source": true
    },
    {
      "id": "GT-7",
      "read_at_source": true
    },
    {
      "id": "GT-8",
      "read_at_source": true
    },
    {
      "id": "GT-9",
      "read_at_source": true
    },
    {
      "id": "GT-10",
      "read_at_source": true
    },
    {
      "id": "GT-11",
      "read_at_source": false
    },
    {
      "id": "GT-12",
      "read_at_source": true
    },
    {
      "id": "GT-13",
      "read_at_source": false
    },
    {
      "id": "GT-14",
      "read_at_source": false
    },
    {
      "id": "GT-15",
      "read_at_source": true
    },
    {
      "id": "GT-16",
      "read_at_source": false
    },
    {
      "id": "GT-17",
      "read_at_source": false
    }
  ],
  "chains": [
    {
      "id": "C1",
      "confidence": "HIGH",
      "rests_on": [
        "GT-3",
        "GT-4",
        "GT-5"
      ]
    },
    {
      "id": "C2",
      "confidence": "HIGH",
      "rests_on": [
        "GT-1",
        "GT-2",
        "GT-6"
      ]
    },
    {
      "id": "C3",
      "confidence": "HIGH",
      "rests_on": [
        "GT-1",
        "GT-7",
        "GT-6",
        "GT-4"
      ]
    },
    {
      "id": "C4",
      "confidence": "HIGH",
      "rests_on": [
        "GT-8",
        "GT-9"
      ]
    },
    {
      "id": "C5",
      "confidence": "HIGH",
      "rests_on": [
        "GT-10",
        "GT-12",
        "GT-15"
      ]
    },
    {
      "id": "C6",
      "confidence": "MEDIUM",
      "rests_on": [
        "C5",
        "GT-1",
        "GT-6",
        "GT-13?",
        "GT-14?",
        "GT-16?"
      ]
    },
    {
      "id": "C7",
      "confidence": "MEDIUM",
      "rests_on": [
        "C1",
        "C2",
        "C3",
        "C4",
        "C5",
        "C6"
      ]
    }
  ],
  "dead_ends": [
    "\"The budget is meaningless, so body length does not matter\"",
    "Compressing the core prose until the body fits 500 lines",
    "The inline pre-mortem and trade-off copies are the intended fallback",
    "\"Split it\" as the immediate intervention (option O1)",
    "Bringing back a line-count gate at 500 (option O5)",
    "Using the context window as the governing hard limit (theoretical-limit framing)",
    "Leave the body as it is (status quo O0)",
    "Treating line count as close enough to text volume"
  ],
  "techniques": {
    "applied": [
      "inversion",
      "five-whys",
      "estimate",
      "trade-off",
      "second-order",
      "pre-mortem"
    ],
    "not_applied": [
      {
        "technique": "fishbone",
        "phase": 2,
        "reason": "the assumption space came from three enumerable record sources (requirements matrix, teardown record, A/B record). Category brainstorming would add breadth with nothing to discriminate between the branches."
      },
      {
        "technique": "theoretical-limit",
        "phase": 1,
        "reason": "nobody claims the budget figure is a physical bound, so separating convention from hard bound does not reframe the question."
      },
      {
        "technique": "theoretical-limit",
        "phase": 4,
        "reason": "the only hard ceiling, the context window, sits at least 5.9× above the resident load (200,000 ÷ 34,055) and its value is unverified (GT-14?). It cannot decide the question; the attempt is recorded as §5 Dead End 6."
      },
      {
        "technique": "five-whys",
        "phase": 3,
        "reason": "there is no recurring failure symptom to drill. Reduce-to-primitives mode was applied in Phase 3."
      },
      {
        "technique": "inversion",
        "phase": 5,
        "reason": "the conclusion is a plan, so Phase 5 uses pre-mortem. Inversion was applied in Phase 2 (above)."
      }
    ]
  },
  "gate": {
    "passes": [
      {
        "bands": [
          "Sound",
          "Sound",
          "Hand-wavy",
          "Rigorous",
          "Sound",
          "Rigorous"
        ],
        "gate_cleared": true,
        "hand_wavy_cap_cleared": true
      },
      {
        "bands": [
          "Rigorous",
          "Rigorous",
          "Rigorous",
          "Sound",
          "Rigorous",
          "Rigorous"
        ],
        "gate_cleared": true,
        "hand_wavy_cap_cleared": true
      }
    ],
    "fix_repeat_fired": true,
    "cleared": true
  },
  "re_entry": {
    "fired": true,
    "edges": [
      {
        "edge": "the Self-Audit Gate's Fix/Repeat loop",
        "trigger": "Criterion 3 scored Hand-wavy on the first pass because read-at-source ground truths fed only MEDIUM chains, and Criterion 5 found the status-quo rival carried live on a MEDIUM chain."
      }
    ]
  },
  "conclusion": {
    "recommendation": "Do not split the body to meet the number. Instead: (1) remove the inline pre-mortem and trade-off procedures, which duplicate references the body already requires the agent to read, and give the trade-off read a named fallback; (2) report the body's size in tokens, with no threshold attached; (3) pre-register a large-difference A/B test, the current body against a 716-line companion-split variant with run counts fixed in advance, and split only if that test shows harm (chain C7).",
    "confidence": "MEDIUM"
  }
}
```
