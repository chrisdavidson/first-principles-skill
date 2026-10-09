## Answer

**Recommendation:** Don't fix this by moving lines into other files that still get inlined at
build time, and don't treat the raw line count as the thing to optimize — both score worst or
near-worst of six scored options (chain C6). Instead, convert the eight always-inlined
companion-technique procedures to the same genuine Read-on-demand mechanism already proven, with
no recorded regression, for the output template and validation rubric (chain C3) — this removes
roughly 20% of guaranteed per-invocation load on focused-mode runs (chain C5) and scores as the
clear structural winner in the trade-off (chain C6). Keep the line-count figure report-only,
never gating — continuing what this project's own TEARDOWN-01 record already established
(chain C1) — and treat that plus a narrow documentation-drift cleanup (chain C4) as cheap,
separable follow-ups, not a bundled prerequisite (chain C6).

**Band (from §6):** MEDIUM.

**Would change it:** Re-measuring chain C5's token fractions with the real tokenizer instead of
the chars/4 approximation, opening `docs/v8.6-quality-ab-experiment.md` directly to confirm
chain C1's quoted result, and observing a live focused-mode run to confirm chain C5's branching
assumption, would raise the band to HIGH; discovering an unrecorded regression in the
Read-on-demand mechanism chain C3 relies on would lower it to LOW.
## 1. Problem Essence

**Essence Statement:** Given an agent definition file that has grown to roughly 2× a nominal
~500-line/~5,000-token budget across several milestones, the real question is not "how do we get
the line count under the budget" but **"what cost or failure mode was the budget a proxy for, does
splitting the file into separate reference files actually reduce that cost given how Claude Code
loads agent/skill content, and if some split is warranted, which content should move and by what
design — versus trimming, restructuring, or simply raising/retiring the budget?"** A fix aimed at
the proxy (the number the linter reads) rather than the underlying cost is not a fix; it is
measurable only by whether the linter is satisfied, which is exactly the failure mode this analysis
exists to avoid reproducing.

**Success criteria** — a correct answer must:
1. Name the concrete cost(s) the line/token budget plausibly protects, distinguishing load-bearing
   costs (real context-window token spend per invocation, measurable attention/instruction-following
   degradation) from unverified or convention-based ones.
2. Establish, from how this specific platform (Claude Code) actually loads agent and skill content,
   whether moving content to separate files changes what gets loaded on a given invocation — not
   assume it does.
3. Distinguish genuine scope growth from avoidable bloat (duplication, verbose prose, premature
   detail, unconditionally-inlined conditional content) as causes of the growth to date.
4. Produce a recommendation that is not constrained to "split" or "don't split" as the only two
   shapes — a combination (split only the conditionally-needed content; trim what remains; adjust
   or retire the budget; restructure for density) is an admissible answer if the evidence supports it.
5. The Conclusion section's confidence line names a concrete re-measurement or observation that
   would raise or lower the stated confidence band, so a reader can check the recommendation
   against future evidence rather than take it on authority.

This analysis is grounded in the actual repository this scenario describes
(`/home/chrisdavidson/Projects/first-principles-skill`, the Claude Code plugin this very skill
ships from), which has already lived through almost exactly the scenario in the prompt and left a
documented record of what it tried and what it found. That record is used throughout as
read-at-source evidence rather than as a hypothetical.
## 2. Assumptions Table

| # | Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|---|
| A-1 | Claude Code loads an agent definition's full body into the model's context on every invocation of that agent. | physical law (platform mechanic) | Accept as ground-truth candidate — this is how the host platform works, not negotiable by this project. | Accept — confirmed | Direct first-hand observation: this analysis's own system prompt *is* the full generated body of `shared/spine/SKILL-body.md`/`first-principles/agents/first-principles.md`, present in full before any task-specific work began. → GT-1. |
| A-2 | Moving content out of the main agent-body file into a separate file automatically reduces the tokens loaded on a given invocation. | convention (the "just split it" reflex treats this as self-evident) | Explicitly challenge — true only if the separate file is read conditionally; false if it is inlined at build time or always loaded. | Challenge — true for some content, false for other content in this codebase | GT-7 vs GT-8/GT-9 below: output-template.md/validation-rubric.md/`*-detail.md` are genuinely Read-on-demand (true case); the eight companion-technique procedures are inlined verbatim into the same body regardless of a separate source file existing for each (false case). |
| A-3 | The ~500-line/~5,000-token budget was derived from a measured cost, latency, or reasoning-quality requirement. | untested belief | Verify against the artifact that set the number and any record of recalibration. | Discard — falsified | GT-3: the number was raised 500→580→644, each raise re-fitted to current size ("limit raised to 622 + 22 buffer"), never derived from a measured requirement (`docs/v8.7-constraint-teardown.md` §2 item 1). |
| A-4 | Within the size range this file has occupied, line/token count is a reliable proxy for degraded instruction-following or attention quality. | untested belief | Verify empirically — this is directly testable with a blind comparison. | Discard — for the tested range (590 vs. 612 lines); not generalizable beyond it | GT-4: blind A/B test, both arms 2/3 PASS, identical band total (35), failures tracked the *problem*, not the arm (`docs/v8.6-quality-ab-experiment.md`, cited in `v8.7-constraint-teardown.md` §2 item 1). |
| A-5 | The core methodology procedure (Phases 1–5 + turn discipline + output format) must be present on every invocation. | physical law (definitional — this is what the agent does every run) | Accept as ground-truth candidate. | Accept — confirmed | GT-10 below; this content has no conditional-use pattern — every run executes all five phases. |
| A-6 | Each of the eight companion-tool procedures is needed only on the subset of runs where that specific technique fires (not every run uses Five Whys, Pre-Mortem, Trade-off, etc.). | current constraint (true of actual usage; expires only if every run started using every technique) | Record expiry condition and check whether the architecture already acts on it. | Challenge — confirmed as a usage fact, but **not acted on**: the architecture inlines all eight regardless. | GT-8: `docs/ARCHITECTURE.md`:119 — all eight companion procedures are "inlined verbatim into the agent body" on every invocation, independent of which techniques actually fire in a given run. This is the single largest unconditionally-loaded conditionally-needed content block in the file. |
| A-7 | The output template and validation rubric are needed only near the end of a run (assembly and self-audit), not at the start. | current constraint, already acted on | Record and confirm the architecture matches the usage pattern. | Accept — confirmed and correctly implemented | GT-7: these are fetched via the Read tool only at the point of use, not inlined (`docs/ARCHITECTURE.md`:119). This is the one place in the real codebase where "split by actual load pattern" was already done correctly before this analysis started. |
| A-8 | Splitting content into standalone, independently-invocable skill files (e.g., a `/five-whys` skill) reduces what the main orchestrating agent loads per invocation. | convention (treated as equivalent to the real fix) | Explicitly challenge. | Discard | GT-9: the thirteen companion skills are registered `disable-model-invocation: true` — slash-only, independent entry points the orchestrator never auto-routes to (`docs/ARCHITECTURE.md`:103,119). Their existence is orthogonal to the main agent body's per-invocation size; the body still inlines all eight full procedures regardless. |
| A-9 | Growth from the recorded 878 lines to the file's current size is explained by uncontrolled bloat (duplication, premature detail, verbose prose). | untested belief | Verify against the actual diff between milestones. | Challenge — partially discarded; mixed cause, not pure bloat | GT-5/GT-6: two of eight companion techniques (`estimate`, `theoretical-limit`) were added after the 878-line snapshot — genuine scope growth, each bringing its own inlined procedure, a `-detail.md` appendix, and worked examples. Separately, `docs/ARCHITECTURE.md`'s own 2026-09-26 self-correction ("this sentence previously claimed the procedures were NOT in the body, which is false against the shipped artifact") shows the maintainers' own model of what the file contained had drifted from what it actually contained — a documentation/legibility failure, not a content-volume failure, but one that compounds the same way. |
| A-10 | A regression gate that keeps getting silenced or raised to track actual size, rather than enforced, represents an engineering failure to "do the real fix." | convention (the framing implied by "gate failing or silenced" in the prompt) | Explicitly challenge against what actually happened when this was investigated. | Discard — as a general rule; retiring the gate was the considered engineering decision, not an avoidance of one | GT-3: an explicit constraint audit (`.planning/ALTITUDE.md`, 2026-07-22) re-examined nine carried constraints against evidence; the line-budget gate was one of five invalidated and formally retired under `TEARDOWN-01` (`docs/v8.7-constraint-teardown.md`), with the figure still reported (not hidden) but no longer blocking. |
| A-11 | Once the gate was retired with no size ceiling enforced at all, the file would grow without bound. | untested belief | Verify against the actual growth trajectory post-retirement. | Challenge — not fully discarded, but not confirmed as runaway; growth continued but tracks named feature additions across many subsequent milestones (current plugin version 9.19.1 vs. the 878-line/early-9.x snapshot) | GT-5/GT-6; no measured runaway-growth incident or quality regression is recorded against the body post-retirement in the documents inspected. This remains the weakest-evidenced assumption in this table (see §5 Sensitivity). |
| A-12 | The A/B experiment's reported result (GT-5) accurately reflects what was tested. | untested belief | Verify by opening `docs/v8.6-quality-ab-experiment.md` directly, not just its quotation in the teardown record. | Challenge — flagged, not independently verified | Surfaced by the end-of-phase Assumption Audit (chain C1, step 3); carried as a confidence caveat on chain C1 rather than resolved; unverified — flagged. |
| A-13 | The absence of a recorded regression for the Read-on-demand mechanism (GT-8) reflects an actual absence of regression, not merely absence of monitoring for one. | untested belief | Verify by checking whether any monitoring or testing exists for missed-Read-trigger failures on the rubric/template path. | Challenge — flagged, not independently verified | Surfaced by the end-of-phase Assumption Audit (chain C3, step 1); carried as a confidence caveat on chain C3 and chain C6's time-lens extension; unverified — flagged. |
| A-14 | Deployed `focused-<technique>` runs actually execute Step 0's branching as specified (only the named technique's procedure is used). | untested belief | Verify by observing a live focused-mode run; this analysis read the specification but did not observe one. | Challenge — flagged, not independently verified | Surfaced by the end-of-phase Assumption Audit (chain C5, step 5); carried as a confidence caveat on chain C5's focused-mode figure; unverified — flagged. |
| A-15 | Future maintainers honor TEARDOWN-01's stated re-adoption procedure rather than silently reinstating a line-count gate. | untested belief | Flag; this is a governance/process expectation this analysis cannot verify from repository state alone. | Challenge — flagged, not independently verified | Surfaced by the end-of-phase Assumption Audit (chain C6 second-order, actor lens); carried as a confidence caveat on that extension; unverified — flagged. |

**Fishbone sweep (brief, feeding the untested-belief rows above):** categories used —
*Methodology* (phases/procedures that must run every time vs. conditionally), *Platform*
(how Claude Code actually loads agent vs. skill content), *Process* (how the budget number was
set and re-set), *Content* (what kind of material accreted — procedure text, reference text,
worked examples, navigation prose). No category surfaced a cause outside A-1 through A-11 above;
the sweep is recorded as support for completeness, not as a separate source of new rows.
## 3. Ground Truths

All ground truths below were read at source during this analysis, by direct inspection of the
live repository at `/home/chrisdavidson/Projects/first-principles-skill` (the project this
scenario describes) — none are delegate-reported or carried over from the prompt's framing
unverified. `?`-marked: none (0 of 13).

- **GT-1** — Claude Code loads an agent's full generated body into the model's context before any
  task-specific work begins; there is no partial or lazy load of the main body itself.
  Provenance: read-at-source — direct observation. This analysis's own system prompt, present
  before this task started, *is* the full text of `shared/spine/SKILL-body.md` (confirmed by the
  `<!-- GENERATED — DO NOT EDIT. Source: shared/spine/SKILL-body.md -->` marker reproduced
  verbatim at its top).
- **GT-2** — The generated agent body (`first-principles/agents/first-principles.md`) currently
  measures **1368 lines**. Read-at-source: `wc -l first-principles/agents/first-principles.md`,
  run directly in this session.
- **GT-3** — The source of truth it is generated from, `shared/spine/SKILL-body.md`, measures
  **792 lines**. Read-at-source: `wc -l shared/spine/SKILL-body.md`, run directly.
- **GT-4** — The original line-count gate (recorded as requirement "META-Q4," budget "~500 lines
  / ~5,000 tokens," rationale "new content lives in references/") was raised three times —
  500 → 580 → 644 — each raise recalibrated to the file's then-current size rather than derived
  from a measured requirement; the retiring record quotes the gate script's own provenance
  comment: *"limit raised to 622 + 22 buffer."* Read-at-source: `docs/v8.7-constraint-teardown.md`
  §2 item 1.
- **GT-5** — A blind A/B experiment compared a 590-line and a 612-line generated body (a 22-line
  contrast — exactly the size of the "buffer" the limit had just been raised to protect) against
  the project's own pass/fail output criteria. Result: both arms scored 2/3 PASS with an
  identical band total of 35; failures tracked the *problem given to the agent*, not which arm
  produced the output. Read-at-source: `docs/v8.6-quality-ab-experiment.md`, quoted directly
  inside `docs/v8.7-constraint-teardown.md` §2 item 1.
- **GT-6** — The line-budget gate was formally retired under a named standing rule,
  **TEARDOWN-01**, following an evidence-based constraint audit
  (`.planning/ALTITUDE.md`, 2026-07-22) that re-examined nine carried constraints against
  evidence rather than inheriting them by default; five were invalidated and retired, four
  survived. The retirement is explicit that *the figure is not retired, the gate is*: the
  reporting script kept printing the current line count; only the commit-blocking behavior was
  removed. Read-at-source: `docs/v8.7-constraint-teardown.md` §§1–2.
- **GT-7** — Nothing in the current pre-commit hooks, CI, or offline battery gates or reports the
  generated agent body's line count; the report-only reporter itself was later retired under a
  follow-on record. Read-at-source: `docs/CONFIGURATION.md`, "Body line budget (gate and reporter
  both retired)" section; corroborated at `CLAUDE.md:86` ("body-budget retired under TEARDOWN-01,
  docs/v8.7-constraint-teardown.md").
- **GT-8** — What genuinely reaches the agent only on demand — i.e., is **not** inlined into the
  body and is instead fetched via the Read tool only at the point of use — is the output
  template, the validation rubric, and the four technique `-detail.md` appendices (five-whys,
  fishbone, estimate, theoretical-limit). Read-at-source: `docs/ARCHITECTURE.md:119`. Corroborated
  by direct observation in this session: this analysis had to call `Read` on
  `output-template.md` and `validation-rubric.md` mid-run — their content was not present in the
  initial system prompt.
- **GT-9** — All eight companion-technique full procedures (Five Whys, fishbone, inversion,
  pre-mortem, trade-off, second-order, estimate, theoretical-limit) are **inlined verbatim into
  the agent body** regardless of whether that technique fires in a given run, and regardless of
  each also having its own source file under `shared/skills/<slug>/SKILL.md`. Read-at-source:
  `docs/ARCHITECTURE.md:119`, which further records a 2026-09-26 self-correction: *"this sentence
  previously claimed the procedures were NOT in the body, which is false against the shipped
  artifact."* Corroborated by direct observation: this analysis's own system prompt contains the
  full `## Procedure` text of all eight techniques under "Companion Techniques."
- **GT-10** — The thirteen companion skills (the eight techniques plus five phase skills) are
  each registered as standalone, independently-invocable Claude Code skills with
  `disable-model-invocation: true` — slash-only; the main agent's own orchestration never
  auto-routes to them. Read-at-source: `docs/ARCHITECTURE.md:103,119`.
- **GT-11** — This project's own backlog explicitly flags a worked example describing "an 878-line
  inlined agent body and a binding META-Q4 gate" as depicting a **superseded repo state**, and
  promoted a phase to rewrite it to match the live, gate-retired tree. Read-at-source:
  `.planning/milestones/BACKLOG-ARCHIVE.md`, Phase 999.124 entry (also present verbatim across
  several `ROADMAP.md`/`milestones/*.md` snapshots).
- **GT-12** — Two of the eight current companion techniques — `estimate` and `theoretical-limit`
  — did not exist at the 878-line snapshot; each was added as a later, self-contained unit (its
  own inlined procedure, its own `<slug>-detail.md` appendix, its own worked example, its own
  standalone skill directory). Read-at-source: presence of
  `first-principles/references/estimate-detail.md`,
  `first-principles/references/theoretical-limit-detail.md`,
  `first-principles/skills/estimate/`, `first-principles/skills/theoretical-limit/` in the live
  tree (directory listing, this session), set against the six-technique count the 878-line
  snapshot's own worked example describes.
- **GT-13** — The plugin is currently at version **9.19.1** (`first-principles/.claude-plugin/plugin.json`),
  many milestones past the 878-line/~v9.1–9.3-era snapshot and past the gate's TEARDOWN-01
  retirement — i.e., the body kept growing for a long stretch *after* the line-count gate was
  removed entirely, to roughly 1.56× the 878-line figure (GT-2), with no line-count ceiling
  enforced at any point in that stretch. Read-at-source: `first-principles/.claude-plugin/plugin.json`;
  cross-referenced against `.planning/milestones/v9.1.0-REQUIREMENTS.md` /
  `v9.3.0-REQUIREMENTS.md` filenames present in the tree for the snapshot era.

Not read further (turn budget): the full text of `.planning/ALTITUDE.md`'s nine-constraint audit
and the complete `docs/v8.6-quality-ab-experiment.md` report were located and their cited
conclusions confirmed via the quoting document (`v8.7-constraint-teardown.md`), but their full
bodies were not separately opened — GT-6's "nine constraints, five invalidated" figure and GT-5's
A/B numbers rest on the teardown record's direct quotation of them rather than a second
independent read of the primary document. This is a deliberate scope limit, not a gap in what
those two ground truths assert.
## 4. Derivation Chains

### C1 — The budget was an unvalidated convention, not a verified constraint

```text
GT-4 (gate raised 500→580→644, re-fitted to size each time, never derived from a
measured requirement) + GT-5 (blind A/B at 590 vs. 612 lines found no quality
difference) + GT-6 (an evidence-based constraint audit formally retired the gate)
→ a number that is repeatedly re-fit to track the artifact it is supposed to constrain,
and that shows no measured relationship to the quality outcome it is nominally
protecting, is functioning as a convention inherited by momentum
→ this project's own governance record reached that exact conclusion independently,
through a dedicated audit rather than through this analysis
→ treating the ~500-line/~5,000-token figure as binding today would be re-adopting a
convention this project has already tested and retired, not applying a verified
constraint [Assumes: A-12]
```
**Pre-check:** head: GT-4, GT-5, GT-6, all HIGH/unsuffixed · ?-marked: none · lowest cited: none ·
Inputs ceiling: HIGH
**Confidence:** MEDIUM. Inputs are all read-at-source (Inputs axis: HIGH). Inference axis is
short: the final hop rests on `[Assumes: A-12]` — that the retirement record's quotation of the
A/B result accurately reflects what was tested — which this analysis has not independently
re-verified by opening `docs/v8.6-quality-ab-experiment.md` directly. Rivals: see §5 Rival — the
strongest rival ("the budget still protects something the A/B didn't test, e.g. tail-risk on
much larger bodies") is addressed there, not here. Would raise to HIGH: opening the primary A/B
report directly and confirming its quoted result.

### C2 — Splitting the file does not by itself reduce per-invocation cost; it depends on what the split changes

```text
GT-1 (the full agent body is loaded into context on every invocation, no partial load)
+ GT-9 (all eight companion-technique procedures are inlined verbatim into that body
regardless of a separate per-technique source file existing for each)
→ a separate source file already exists for every one of the eight companion
techniques (shared/skills/<slug>/SKILL.md) and the generated body still inlines all
eight in full on every run
→ "the content lives in a separate file" and "the content is not loaded on every
invocation" are two independent facts in this architecture, not one fact described two
ways
→ moving more content into more separate files, without also changing whether that
content is inlined at build time or read on demand at run time, would repeat the same
pattern: smaller individual source files, identical per-invocation token load
```
**Pre-check:** head: GT-1, GT-9, all HIGH/unsuffixed · ?-marked: none · lowest cited: none ·
Inputs ceiling: HIGH
**Confidence:** HIGH. This is the chain that most directly tests the "just split it" reflex
named in the prompt, and it is falsified by direct inspection of how this specific codebase's
build pipeline already behaves (GT-9), not by general reasoning about platforms in the
abstract.

### C3 — Genuine conditional loading is already a proven, working pattern in this codebase for some content

```text
GT-8 (output-template.md, validation-rubric.md, and the four `*-detail.md` appendices
reach the agent only via an explicit Read-tool call at the point of use, confirmed by
direct observation in this session) + C2 (splitting only helps when the split changes
load timing, not just file boundaries)
→ this project has already built and is already relying on, without a recorded
regression, exactly the mechanism the "just split it" reflex is reaching for in the
abstract [Assumes: A-13]
→ the design question is therefore not "should we invent a new splitting mechanism" but
"which currently-always-inlined content should move onto the mechanism that already
works"
```
**Pre-check:** head: GT-8, C2 (HIGH) · ?-marked: none · lowest cited: C2 (HIGH) · Inputs
ceiling: HIGH
**Confidence:** MEDIUM. Inputs axis: HIGH (GT-8 and chain C2 both read-at-source/HIGH).
Inference axis is short: the first hop rests on `[Assumes: A-13]` — that the absence of a
recorded regression for the Read-on-demand mechanism reflects an actual absence of regression,
not merely absence of monitoring — which this analysis has not independently verified. Rivals:
live, not ruled out — see §5 Rival's second item and pre-mortem cluster 3, which is why this
chain's recommendation (§4 C6) carries an explicit plan change rather than treating the
mechanism's reliability as settled. Would raise to HIGH: confirming, by checking test/monitoring
coverage, that the rubric/template mechanism's clean record reflects genuine reliability.

### C4 — The growth to date has (at least) two distinct causes with different fixes

```text
GT-12 (two of the eight companion techniques, estimate and theoretical-limit, were
added after the 878-line snapshot, each bringing its own procedure, detail appendix,
and worked example) + GT-9 (the project's own architecture document had to
self-correct in 2026-09-26 because its description of what was inlined no longer
matched the shipped artifact)
→ some of the growth is genuine, named scope addition (new companion techniques are a
real capability, not padding) with an auditable size cost
→ separately, some of the difficulty in reasoning about the file's size is that the
humans maintaining it had drifted out of sync with what the file actually contained —
a legibility failure that compounds growth without being caused by it
→ a single intervention aimed at only one of these (e.g., only reorganizing files, or
only trimming prose) will not address the other, and conflating them risks declaring
the problem "fixed" once the visible symptom (line count in one file) changes while the
cause that symptom didn't come from is untouched
```
**Pre-check:** head: GT-12, GT-9, both HIGH/unsuffixed · ?-marked: none · lowest cited: none ·
Inputs ceiling: HIGH
**Confidence:** HIGH.

### C5 — Quantifying the always-loaded, conditionally-needed block (Estimate)

**Target quantity:** tokens guaranteed-loaded per invocation from content that is only actually
used by a subset of runs, expressed as a fraction of the whole body.

**Decomposition:** `(tokens in the companion-techniques block) / (tokens in the whole generated
body)`, both measured directly rather than assumed, using a chars-to-tokens approximation
(`chars/4`) — a standard rough heuristic, not this provider's exact BPE tokenizer, which is why
this chain's confidence is capped below HIGH.

```text
GT-2 (the generated agent body measures 1368 lines / ~127,400 characters, directly
counted) + GT-9 (the eight companion-technique procedures occupy a single contiguous
block of that body, lines 849–1368)
→ measuring that block directly gives ~28,980 characters, ≈7,250 tokens at the chars/4
approximation, against ≈31,850 tokens for the whole body — the companion-techniques
block is roughly 23% of the body's total token weight (38% of its line count; the gap
between the two fractions is explained by that block's shorter average line length)
→ per-technique, that is roughly 7,250 / 8 ≈ 900 tokens apiece
→ a run in `focused-<technique>` mode structurally uses exactly one of the eight
(Step 0's own branching rule: the other seven are not walked) and therefore carries
roughly 7 × 900 ≈ 6,300 tokens of guaranteed-unusable content on every such invocation —
about 20% of the entire body, paid by every focused-mode run regardless of which
technique it names [Assumes: A-14]
→ a `full-composer` run may invoke any subset of the eight, so its waste is bounded
between 0% (if a given run happens to fire all eight — rare, since the techniques
largely address different problem shapes) and ≈87.5% (if it fires only one), bracketing
a plausible central case of roughly 40–60% of that block being unused on a typical
full-composer run, i.e., very roughly 9–14% of the whole body's tokens
```
**Lower/central/upper bound (fraction of whole-body tokens paid for but not used, per
invocation):** focused mode ≈ 20% (tight, structural, not a guess); full-composer mode ≈
[9%, 11–14%, 20%] depending on how many of the eight techniques a given analysis actually fires.
**Decision-resolution check:** both ends of the full-composer bracket (9% and 20%) and the tight
focused-mode figure (20%) all point the same direction — a materially sized, structural,
recoverable fraction of guaranteed load exists in exactly the content GT-9 already identified as
inlined-regardless-of-use — so the estimate is precise enough for the decision this analysis is
making (whether this block is worth re-architecting) without narrowing the bracket further.
**Pre-check:** head: GT-2, GT-9, both HIGH/unsuffixed · ?-marked: none · lowest cited: none ·
Inputs ceiling: HIGH
**Confidence:** MEDIUM. Inputs axis: HIGH. Inference axis carries two named, separately
addressable shortfalls, not one: (1) the chars/4 approximation is a genuine source of
imprecision in the headline numbers (not in the direction of the conclusion) — the real BPE
token counts could plausibly differ from this estimate by ±15–20% without changing which option
the trade-off below favors; removable by re-running the measurement with the actual tokenizer.
(2) the focused-mode waste figure rests on `[Assumes: A-14]` — that deployed focused-mode runs
actually execute Step 0's branching as specified — which this analysis has not observed in a
live run; removable by observing one. Neither cause is priced away here, which is why this
chain stays MEDIUM rather than HIGH despite its Inputs axis being clean. Verification that would
remove the first downgrade cause: re-run the same measurement with the actual Anthropic
tokenizer rather than the
chars/4 heuristic.

### C6 — Trade-off across candidate interventions (collapsed from the full trade-off procedure in the Appendix)

Six options were scored against six weighted criteria (full scoring table, must-have knockouts,
and flip test are in `## Adversarial pass (process output)`'s companion
`## Trade-off scoring (process output)` block in the Appendix). Options: **O0** status quo
(leave as is); **O1** the naive "just split it" move (relocate content into more source files
that remain inlined into the single generated body at build time — the Goodhart move this
analysis was asked to test); **O2** usage-pattern split (convert the eight always-inlined
companion procedures to genuine Read-on-demand references, copying the mechanism GT-8 already
proves works); **O3** trim/restructure for density without removing information; **O4**
formalize the budget as report-only, never gating (i.e., keep doing what TEARDOWN-01 already
established); **O5** composite of O2 + O4 + a bounded O3 pass limited to the content GT-9 flagged
as drifted.

```text
C1 (the budget itself is not the lever to pull) + C2 (file-boundary splitting alone does
not reduce load) + C3 (a genuine on-demand mechanism already exists and works) + C4 (two
distinct causes need two distinct fixes) + C5 (the companion-techniques block is the
single largest, most clearly conditional, always-loaded segment, at a quantified ~20%+
of focused-mode load)
→ scoring all six options against reduces-real-cost, preserves-correctness, effort,
fixes-the-named-causes, avoids-gaming, and navigability (weights locked before scoring)
gives O5 = 104 and O2 = 103, both clearly ahead of O1 = 48, O0 = 73, O4 = 77, and O3 = 81
→ the O5/O2 gap is a near-tie (flip test: a two-step move on either the effort weight or
the navigability weight reverses it), so the two are reported as roughly equally good,
not as a clear single winner
→ the practical reading of a near-tie between "the structural fix alone" (O2) and "the
structural fix plus a policy formalization plus a cleanup pass" (O5) is: do O2 now (it
is the load-bearing, non-fragile part of the win), and treat O4's policy formalization
and O3's targeted cleanup as cheap, independent follow-ups rather than a bundled
prerequisite — O1 (the naive split) and O0 (do nothing) are both clearly dominated and
should not be the chosen path
```
**Pre-check:** head: C1 (MEDIUM), C2 (HIGH), C3 (MEDIUM), C4 (HIGH), C5 (MEDIUM) · ?-marked:
none · lowest cited: C1, C3, C5 (MEDIUM) · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM. Three of the five cited chains (C1, C3, C5) carry a MEDIUM rating via
named, distinct Inference-axis shortfalls (`A-12`, `A-13`, `A-14` respectively) rather than any
shared defect, and none of the three changes any option's *relative* score in the trade-off
table — the ranking of O2/O5 over O0/O1/O3/O4 is robust to all three, because each affects the
magnitude of a cost estimate or the reliability of a precedent, not the direction of the
comparison. What is not robust is the *size* of the O5-over-O2 margin, which is explicitly a
near-tie (C6's own flip test) and should not be read as a confident preference for bundling all
three fixes together. Would change the band to HIGH: re-running C5 with the actual
tokenizer and confirming the fraction stays materially above the "worth re-architecting"
threshold used here.

### Second-order extension of C6 (actor lens and time lens)

**Actor lens.** *Maintainers* editing a companion technique would, under O2, edit exactly one
file and trust the same Read-on-demand mechanism already trusted for the output template and
rubric — lower risk of the kind of drift GT-9 already caught once. *A future maintainer who
reaches for a line-count gate again* (the behavior TEARDOWN-01 was written to prevent silently
recurring) is the actor C1 is most clearly aimed at: the retirement record itself anticipates this
("silence never means permission... a future milestone... must author its own successor record"),
so the second-order effect of adopting C1's conclusion here is reinforcing an already-written
institutional guardrail, not inventing a new one. [Assumes: A-15] *A user invoking `focused-<technique>` mode*
is the direct beneficiary of O2's ~20% reduction (C5) — they currently pay for seven procedures
they structurally cannot use; under O2 they stop paying for them. *A user running
`full-composer` mode on a problem that happens to fire most of the eight techniques* sees little
or no benefit from O2 and pays a small number of additional Read-tool round trips instead —
a real, non-zero cost this analysis has not bracketed in latency terms, only in tokens.

**Time lens.** *Immediately after O2 ships*: the generated agent body shrinks by roughly the
companion-techniques block's size; any downstream tooling that assumed the full text of all
eight procedures was present in the body in one read (for example, a reviewer diffing the agent
file, or a test fixture that greps the body for a specific technique's steps) would need to
follow the same Read-on-demand convention already established for the rubric and template, or
it would silently stop finding what it is looking for. *After a few milestones*: if a ninth
companion technique is added (the same growth pattern that produced `estimate` and
`theoretical-limit`, per GT-12), it is added directly onto the proven on-demand pattern rather
than onto the inlined block — the marginal cost of a new technique becomes a new reference file
plus a one-line pointer, not +100–150 inlined lines every run pays for regardless of use.
*Once this has been in place long enough to be assumed*: the risk is the inverse of the one that
produced GT-9's correction — a document describing the architecture could again drift out of
sync with what is actually inlined vs. Read-on-demand, now across a larger number of reference
files rather than one block; this is the same documentation-drift cause C4 names, recurring at a
different scale, and is why O5's bounded cleanup pass (keeping architecture docs honest about
what is genuinely on-demand) is a reasonable low-cost addition even though the trade-off's flip
test shows it is not the load-bearing part of the fix.

No step in this extension contradicts a ground truth from §3; both lenses extend C6 rather than
undermining it.
## 5. Abandoned Reasoning

**What was tried:** Analyzing the prompt's "878 lines vs. a ~500-line budget, two milestones of
growth, gate silenced or ignored" framing as a purely hypothetical, self-contained scenario,
reasoning only from general principles about context windows and attention.
**Why abandoned:** The scenario matches this project's own history closely enough (same four
content-type categories, the same 878-line figure, the same ~500-line/~5,000-token number) that
treating it as hypothetical when the real artifact and its full governance trail were directly
readable would have discarded better evidence in favor of weaker, generic reasoning.
**What it ruled out:** A purely speculative analysis of what the budget "probably" protects, in
favor of GT-3 through GT-7's directly-read record of what was actually tested and concluded.

**What was tried:** Accepting the general Claude-Code skill-authoring guidance ("keep SKILL.md
bodies under roughly 500 lines for best performance") as itself sufficient justification for a
line-count target, independent of this project's own evidence.
**Why abandoned:** That guidance is a convention of the same kind GT-4/GT-5 already tested and
found wanting for this specific artifact — adopting it without the same scrutiny applied to
everything else in this analysis would reintroduce exactly the untested-belief-treated-as-law
failure mode Phase 2 exists to catch (A-3/A-4).
**What it ruled out:** Using "the general guidance says 500" as a conclusion-level justification
anywhere in §4 or §6; it appears only as context for why the number was chosen originally, not as
evidence for what it should be now.

**What was tried:** An exhaustive line-by-line duplication and verbosity audit of the full
1368-line body, to independently quantify how much of the growth is repeated or padded prose
versus genuine new content, beyond the two data points already available (GT-9's correction note,
GT-12's two new techniques).
**Why abandoned:** Turn budget. The two available data points already establish that growth has
at least two distinct causes with different fixes (chain C4), which is what this analysis's
decision hinges on; a full duplication audit would sharpen the proportion between the two causes
but is unlikely to change which intervention (§6) is recommended.
**What it ruled out:** A quantified "X% of growth is genuine scope vs. Y% is duplication/bloat"
claim — this analysis makes no such claim and should not be read as implying one.

**What was tried:** Recommending a uniform treatment — "split all four content types (core
methodology, companion procedures, output template, validation rubric) the same way" — as a
single, simple instruction.
**Why abandoned:** GT-8 shows the output template and validation rubric are *already* on the
genuinely-conditional, Read-on-demand mechanism this analysis recommends extending to the
companion procedures (§4 C3/C6). A uniform instruction would have recommended re-doing work
that is already correctly done for half of the four content types, which is itself the kind of
proxy-chasing (treating "did we split files" as the goal, rather than "is the load pattern
correct") this analysis was asked to avoid.
**What it ruled out:** Any form of the recommendation in §6 that treats the output template or
validation rubric as needing further structural change; they do not.
## 6. Conclusion

**Recommended approach:** Do not pursue the naive "move lines into another file that still gets
inlined at build time" fix, and do not treat the raw line count itself as the thing to optimize
— both are the gaming move the prompt was right to be suspicious of, and both score worst or
near-worst among six scored options (chain C6). Adopt the structural fix instead: convert the
eight always-inlined companion-technique procedures to the same genuine Read-on-demand mechanism
already proven, with no recorded regression, for the output template and validation rubric
(chain C3), which removes roughly 20% of guaranteed per-invocation load on focused-mode runs and
a smaller, variable amount on full-composer runs (chain C5), and which the trade-off scores as
the clear structural winner (chain C6). Treat re-stating the line-count figure as report-only
and never gating — i.e., continuing what this project's own TEARDOWN-01 record already
established (chain C1) — and a narrow cleanup pass targeted at the documentation drift chain C4
identified, as cheap, separable follow-ups rather than a bundled prerequisite: the trade-off's
flip test shows the three-part bundle beats the structural fix alone by a margin too thin (a
two-step weight move away from a tie) to justify coupling them into one decision (chain C6).

**Key insight:** In this codebase, "the content lives in its own file" and "the content is
loaded on every invocation" are two independent facts, not one fact described two ways — a
separate source file already exists for every companion technique and all eight are still
inlined in full on every run regardless (chain C2). A split only reduces real cost when it
changes which of those two facts is true for a given block of content, and the single largest
block that structurally qualifies — because a `focused-<technique>` run can only ever use one of
the eight by the methodology's own branching rule — is the companion-techniques block (chains
C2, C5). The line-count gate itself was never shown to track anything but its own history of
being re-fit to the file's size (chain C1); the fix that matters operates on load pattern, not
on the number a linter reads.

**Trade-offs acknowledged:** Moving the companion procedures onto the Read-on-demand mechanism
multiplies that mechanism's call sites roughly eightfold over what has been validated so far,
which is a real, nonzero new failure surface (a missed Read-trigger would leave a firing
technique's procedure unavailable) even though no regression has been recorded for the three
reference types already using it (chain C6, criterion C2 scored 4 of 5, not 5). A
`full-composer` run that fires most of the eight techniques gains little or nothing from this
change and instead pays a small number of additional Read round-trips (second-order extension of
chain C6). The headline sizing (≈20% for focused mode; a 9–20% bracket for full-composer mode)
rests on a chars/4 token approximation rather than this provider's actual tokenizer, which is why
chains C5 and C6 are capped at MEDIUM rather than HIGH. Finally, the growth this analysis
diagnoses is only partly structural: a real documentation-drift component (chain C4) would
survive this fix untouched unless the separate, cheap cleanup pass is also done.

**Pre-check:** head: C1 (MEDIUM), C2 (HIGH), C3 (MEDIUM), C4 (HIGH), C5 (MEDIUM), C6 (MEDIUM)
· ?-marked: none · lowest cited: C1, C3, C5, C6 (MEDIUM) · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM. Every chain's inputs are read-at-source ground truths with no `?`
markers (Inputs axis: HIGH throughout). Four of six chains (C1, C3, C5, C6) carry a MEDIUM
rating via named Inference-axis shortfalls — `A-12` on C1, `A-13` on C3, `A-14` plus the chars/4
approximation on C5, and C5's own shortfall inherited by C6 — while C2 and C4 are independently
HIGH on all three axes. None of these shortfalls changes which option the trade-off favors;
each affects the magnitude or reliability of one input, not the direction of the comparison.
Would raise to HIGH: re-measuring C5's token fractions with the real tokenizer, opening
`docs/v8.6-quality-ab-experiment.md` directly to confirm A-12, and observing a live
focused-mode run to confirm A-14. Would lower to LOW: discovering that the Read-on-demand
mechanism *has* had an unrecorded regression (A-13) that this analysis could not detect from the
repository alone, which would undercut chain C3's load-bearing precedent for the entire
recommendation.
## Appendix — process output

## Trade-off scoring (process output)

**Must-haves (knockouts), checked before scoring:** MH1 — a companion technique's full procedure
must still be fully available to the agent in any run where that technique fires. MH2 — a
full-composer run must retain access to any of the eight techniques, not a fixed subset. All six
options pass both; none is knocked out.

**Criteria and locked weights** (1–5, assigned before scoring): C1 reduces real per-invocation
context cost (w=5, anchors: 1=no reduction, 5=removes >60% of guaranteed-but-unused load) · C2
preserves correctness/availability when a technique is actually needed (w=5, anchors: 1=often
breaks, 5=proven mechanism, no recorded regression) · C3 implementation effort (w=2, anchors:
1=large rewrite, 5=trivial) · C4 fixes the named root causes — unconditional inlining (GT-9) and
documentation drift (GT-9's correction) (w=4, anchors: 1=fixes neither, 5=fixes both) · C5 avoids
Goodhart gaming — the reported metric and the real cost move together (w=4, anchors: 1=pure
gaming, 5=fully honest) · C6 maintainer navigability vs. today (w=3, anchors: 1=worse than today,
3=same as today, 5=clearly easier than today).

| Option | C1 (w5) | C2 (w5) | C3 (w2) | C4 (w4) | C5 (w4) | C6 (w3) | Weighted total |
|---|---|---|---|---|---|---|---|
| O0 status quo | 1 | 5 | 5 | 1 | 5 | 3 | **73** |
| O1 naive split (relocate source, still inlined at build) | 1 | 5 | 2 | 1 | 1 | 2 | **48** |
| O2 usage-pattern split (8 procedures → Read-on-demand) | 5 | 4 | 3 | 5 | 5 | 4 | **103** |
| O3 trim/restructure, no content removed | 2 | 5 | 3 | 3 | 4 | 4 | **81** |
| O4 formalize budget as report-only (never gating) | 1 | 5 | 5 | 2 | 5 | 3 | **77** |
| O5 composite: O2 + O4 + bounded O3 cleanup | 5 | 4 | 2 | 5 | 5 | 5 | **104** |

Each score cites: C1/C5 from GT-1/GT-2/GT-9/C5 (chain); C2 from GT-8's no-recorded-regression
precedent for the mechanism each option does or doesn't extend; C3 from the known shape of
`scripts/sync-content.py`'s existing `{{PROCEDURE:slug}}` substitution (GT-9/ARCHITECTURE.md:119)
being the thing O2 would change; C4 from GT-9 and GT-9's correction note (two distinct causes);
C6 is a qualitative judgment anchored against "same as today."

**Result:** O5 (104) and O2 (103) lead, both clearly ahead of O3 (81), O4 (77), O0 (73), and O1
(48) — the naive "just split it" move scores lowest of all six options, confirming the
Goodhart-gaming concern the prompt raised rather than merely restating it.

**Flip test:** gap(O5 − O2) = −w(C3) + w(C6) = −2 + 3 = +1, a near-tie. A single-criterion weight
move that reverses the ranking (strictly, not just ties it): raise C3's weight from 2 to 4 (a
move of 2), or lower C6's weight from 3 to 1 (a move of 2). A move of 1 on either produces a tie,
not a reversal. No single-weight move of size 1 flips this result; a move of 2 does. Given the
margin is this thin, O2 and O5 are read as practically equivalent, and the recommendation below
treats O2 as the load-bearing fix and O4/O3 as cheap, separable follow-ups rather than claiming
O5 is decisively better.
## Assumption Audit scan (process output)

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | gate raise-chain + null A/B + retirement → convention verdict | No — fully grounded in GT-4/5/6 | n/a |
| C1 | 2 | project's own record reached the same conclusion | No | n/a |
| C1 | 3 | re-adopting the figure would be re-adopting a tested-and-retired convention | Yes — relies on the retirement record's account of the A/B result being accurate, not independently re-run | Added as A-12: "The A/B experiment's reported result (GT-5) accurately reflects what was tested." [Assumes: A-12] |
| C2 | 1 | full-body load + verbatim inlining regardless of source-file boundaries | No | n/a |
| C2 | 2 | separate source file already exists per technique, yet all inlined | No | n/a |
| C2 | 3 | "lives in a separate file" ≠ "not loaded every time" | No | n/a |
| C2 | 4 | more files without changing load timing repeats the pattern | No | n/a |
| C3 | 1 | on-demand mechanism proven for 3 reference types | Yes — relies on "no recorded regression" meaning no regression occurred, not merely none documented | Added as A-13: "The absence of a recorded regression for the Read-on-demand mechanism (GT-8) reflects absence of an actual regression, not merely absence of monitoring for one." [Assumes: A-13] |
| C3 | 2 | design question reframed as "which content moves onto the existing mechanism" | No | n/a |
| C4 | 1 | two new techniques = genuine scope growth | No | n/a |
| C4 | 2 | architecture doc self-correction = legibility failure | No | n/a |
| C4 | 3 | one intervention won't fix both causes | No | n/a |
| C5 | 1–4 | token/line measurement and per-technique share | Yes — chars/4 approximates the real tokenizer | Already flagged in-line as C5's own confidence caveat; not a new table row (same assumption, not duplicated) |
| C5 | 5 | focused-mode waste is structural (~20%) | Yes — relies on Step 0's branching rule being followed as written in actual runs, not bypassed | Added as A-14: "Deployed `focused-<technique>` runs actually execute Step 0's branching as specified (only the named technique's procedure is used)." [Assumes: A-14] |
| C6 | 1–3 | trade-off scoring and ranking | No — weights and anchors stated explicitly in the trade-off block; scores trace to GTs/C5 | n/a |
| C6 (2nd-order) | actor lens | future maintainer re-adding a gate is deterred by the written record | Yes — relies on the TEARDOWN-01 record's own "must author a successor record" clause being honored in practice | Added as A-15: "Future maintainers honor TEARDOWN-01's stated re-adoption procedure rather than silently reinstating a line-count gate." [Assumes: A-15] |
| C6 (2nd-order) | time lens | downstream tooling adapts to Read-on-demand convention | Yes — same as A-13's category but forward-looking | Covered by A-13 (no duplicate row) |

New rows A-12 through A-15 are added to the §2 Classified Assumptions Table (all type: untested
belief; treatment: flag and carry a confidence caveat, since none is independently verified in
this analysis) — see the table addendum immediately below.

| # | Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|---|
| A-12 | The A/B experiment's reported result (GT-5) accurately reflects what was tested. | untested belief | Flag; would require opening `docs/v8.6-quality-ab-experiment.md` directly (not just its quotation in the teardown record) to verify. | Flagged, not independently verified | Carried as a caveat on C1. |
| A-13 | The absence of a recorded regression for the Read-on-demand mechanism (GT-8) reflects an actual absence of regression, not merely absence of monitoring. | untested belief | Flag; would require checking whether any monitoring/testing exists for missed-Read-trigger failures on the rubric/template path. | Flagged, not independently verified | Carried as a caveat on C3 and on C6's time-lens extension. |
| A-14 | Deployed `focused-<technique>` runs actually execute Step 0's branching as written (only the named technique fires). | untested belief | Flag; this analysis read the methodology's own specification of the branching rule but did not observe a live focused-mode run to confirm behavior matches spec. | Flagged, not independently verified | Carried as a caveat on C5's focused-mode figure. |
| A-15 | Future maintainers honor TEARDOWN-01's stated re-adoption procedure rather than silently reinstating a line-count gate. | untested belief | Flag; this is a governance/process expectation, not something this analysis can verify from the current repository state. | Flagged, not independently verified | Carried as a caveat on C6's actor-lens extension. |
## Adversarial pass (process output)

**Recompute.** Independently re-derived every computed figure in §4: 520/1368 lines = 0.380
(stated "38%") ✓. 28,984 chars / 4 = 7,246 tokens (stated "~7,250") ✓. 127,381 chars / 4 = 31,845
tokens (stated "~31,850") ✓. 7,246 / 31,845 = 0.2276 (stated "~23%") ✓. 7,246 / 8 = 905.75
(stated "~900") ✓. 7 × 905.75 = 6,340.25 (stated "~6,300") ✓; 6,340 / 31,845 = 19.9% (stated
"~20%") ✓. Full-composer bracket: 40% of the block unused → 0.4 × 22.76% = 9.1%; 60% unused →
0.6 × 22.76% = 13.7% (stated "9–14%") ✓. Trade-off weighted totals re-summed independently from
the per-criterion scores and locked weights in the scoring table: O0=73, O1=48, O2=103, O3=81,
O4=77, O5=104 — all match §4/C6's reported totals; no arithmetic error found. Flip-test
arithmetic (gap = −w(C3) + w(C6) = −2+3 = +1) re-derived and confirmed.

**Sensitivity.** The single ground truth whose falsity would flip the recommendation is **GT-9**
(all eight companion-technique procedures are inlined verbatim regardless of use) — if false,
there is nothing in the always-loaded body for O2 to convert, and chains C2/C5/C6 collapse. GT-9
is unsuffixed and is unusually well-supported for this analysis: it rests on both a direct
documentation citation (`docs/ARCHITECTURE.md:119`) and independent direct observation (the
eight full procedures are visibly present, verbatim, in this analysis's own system prompt) —
two independent confirmations of the same fact, which is why it is not flagged `?` despite being
the most load-bearing single fact in the analysis. Weakest link per chain: C1 — relies on the
retirement record's quotation of the A/B result (A-12) rather than an independent re-read of
`docs/v8.6-quality-ab-experiment.md` itself. C3 — relies on "no recorded regression" meaning no
regression occurred (A-13); see the Rival and pre-mortem cluster 3 below for the sharper version
of this concern. C4 — scope-limited by a deliberately abandoned exhaustive duplication audit (§5). C2 —
the weakest link is the interpretive step "lives in a separate file" and "loaded every
invocation" are independent facts, not one fact described twice — a conceptual distinction this
analysis draws rather than one directly stated in a cited source, though both underlying facts
(GT-1, GT-9) are themselves directly cited. C5/C6 — the named chars/4 approximation, the
focused-mode assumption `A-14`, and the C6 near-tie itself.

**Rival.** Strongest rival to the headline conclusion: *"the only directly measured evidence in
this codebase of a size-to-quality relationship (GT-5) found none at ~600 lines, so there is no
demonstrated harm from inlining at 1368 lines either, and O4 alone (keep the figure report-only,
change nothing structurally) is sufficient."* This rival is **not fully ruled out** on the
quality axis — GT-5 tested one 22-line contrast near 600 lines, not the current size, and
nothing in this analysis's evidence bounds whether quality degrades somewhere between 612 and
1368 lines; that gap is real and unresolved, and is recorded here rather than papered over. The
rival is adequately addressed, however, on the axis the recommendation actually rests on: chain
C5's case for O2 is a raw per-invocation token-cost argument (money, latency, context-window
headroom for the rest of the run), not a quality-degradation argument — a dimension GT-5 never
measured and this rival does not contest. A second, intermediate-chain rival (bearing on C3,
not the headline): *"the rubric/template Read-on-demand mechanism's clean record may reflect
that those two are invoked at one fixed, late point in every run, while the eight companion
procedures are invoked conditionally across many different trigger conditions — making them
structurally more failure-prone to port to the same mechanism."* This rival is **live, not
ruled out** — it is exactly pre-mortem cluster 3 below, and is the basis for that cluster's plan
change (keep decision-rule disambiguation text inline; move only the step-by-step procedure
body on demand) rather than a claim that the risk doesn't exist.

**Adversarial technique — Pre-Mortem** (the conclusion is a plan/recommendation, not a bare
claim, per the pre-mortem-vs-inversion decision rule; opened via Read at
`first-principles/references/pre-mortem.md` before this pass was written).

**Premise:** It is six months from now. The migration of the eight companion-technique
procedures to Read-on-demand references has failed badly. What caused it?

**Causes** (generated from four viewpoints — the implementer, the user living with the result,
whoever pays for the migration in engineering time, and a future governance reviewer —
unfiltered):
- The `{{PROCEDURE:slug}}` substitution mechanism turned out to be more deeply coupled to the
  inlined text than expected — other scripts or tests grep the generated agent body for
  procedure text directly, and broke across multiple surfaces when that text moved.
- One of the eight call sites' new "open `<slug>.md` with Read" pointer was missing, malformed,
  or pointed at the wrong slug, silently making that technique's procedure permanently
  unavailable even on a run where it should fire.
- `sync-content.py --check`/`--write` was not updated to validate that every new on-demand
  pointer resolves to an existing file, so pointer/target drift goes undetected by the existing
  gate.
- A `full-composer` run that fires five or six of the eight techniques now makes five or six
  extra Read round-trips mid-run, consuming turns from the 60-turn budget and pushing more runs
  into the "Observe incomplete — residual caveat" fallback than before.
- Moving the step-by-step procedure off the page removed the short "Decision rule" disambiguation
  text that used to sit next to it inline, and the agent misapplied or skipped a disambiguation
  step it used to see "for free" by physical proximity (e.g., confusing inversion with pre-mortem
  without the adjacent decision-rule sentence as a reminder).
- The dozens of `tests/*` fixtures that assert against specific content or line ranges of the
  current inlined body required updating one by one, and this consumed far more engineering time
  than the trade-off's effort score (3/5) assumed.
- A future constraint audit, trying to inventory what capabilities the agent has, can no longer
  see all eight technique names and their procedures in one scroll of the generated body, making
  exactly the kind of governance review that caught the original line-budget problem harder to
  perform on this part of the system.

**Clusters:**
1. **Pipeline/tooling coupling underestimated** (causes 1, 3) — bears on C6 criterion C3
   (effort, scored 3/5) and C3.
2. **Runtime cost shifts from tokens to turns/latency** (cause 4) — bears on C5, C6 criterion C1,
   and the second-order time-lens extension of C6.
3. **Loss of inline disambiguation degrades technique-application correctness** (cause 2, 5) —
   bears on must-have MH1 directly and on C6 criterion C2 (scored 4/5, not 5) — this is the
   cluster closest to fatal, because it threatens the knockout criterion rather than just a score.
4. **Migration effort underestimated via sprawling test-fixture surface** (cause 6) — bears on
   C6 criterion C3.
5. **Auditability/discoverability regression for future governance review** (cause 7) — bears on
   C6 criterion C6 (navigability, scored 4/5) and the second-order time-lens extension.

**Disposition:**
1. **Plan change** — before treating O2 as shipped, extend `sync-content.py --check` with a
   dedicated validation that every new on-demand pointer resolves to an existing target file;
   this is a scoped, mechanical addition to a pipeline the project already maintains.
2. **Accepted risk, named mitigation** — the token-to-turn cost shift is accepted because the
   methodology already has a disclosed, handled fallback (turn-budget exhaustion is reported, not
   silent); mitigation is to watch tripwire 2 below rather than block the migration on it.
3. **Plan change** — this is the one cluster this pass changes the plan on directly: scope O2 so
   that each companion technique's short in-body "Decision rule" disambiguation sentence (the
   kind already present in the body's `## Companion tools` summaries) stays inline, and only the
   longer step-by-step `## Procedure` body moves to Read-on-demand — mirroring how the body
   already separates a short pointer from a longer on-demand reference elsewhere.
4. **Plan change** — track test-fixture migration as its own scoped sub-task with a named owner
   before declaring O2 complete, rather than folding it into the single effort estimate this
   analysis used.
5. **Accepted risk, no further mitigation** — already named plainly in §6's "Trade-offs
   acknowledged" and in C6's second-order time-lens extension; recorded and moved on.

**Tripwires:**
1. `sync-content.py --check` fails, or a new dedicated pointer-resolution check fails, on any
   commit touching a companion technique — owner: CI, checked on every commit.
2. The project's existing conformance/battery harness shows an increase in runs reaching "Observe
   incomplete — residual caveat" after the change relative to before — owner: whoever reviews the
   next battery run.
3. A conformance/battery test exercising a specific technique (focused- or full-composer-mode)
   shows visible misapplication or a skipped disambiguation step — owner: the existing test
   battery referenced in `docs/CONFIGURATION.md`.
4. The test-fixture migration sub-task (disposition 4) remains open past the milestone boundary
   intended for shipping O2 — owner: whoever plans that milestone.
5. None observable in advance for cluster 5; accepted as stated.

**Falsification.** This conclusion is false if either: (a) converting the companion-technique
procedures to Read-on-demand references measurably degrades technique-selection or
technique-application correctness in live runs (e.g., a conformance/battery test shows increased
misapplication, missed triggers, or disambiguation failures after the change) without a
token/cost benefit large enough to justify that cost; or (b) re-measuring chain C5's token
fractions with the real tokenizer (rather than the chars/4 approximation) shows the
companion-techniques block is in fact a small fraction of total body tokens, undermining the
stated ~20–23% magnitude the recommendation's cost-benefit case rests on.
## §6→§4 closure ledger (process output)

- "Do not pursue the naive 'move lines into another file that still gets inlined at build time'
  fix... both score worst or near-worst among six scored options" → chain C6 ✓ (inline)
- "Adopt the structural fix instead: convert the eight always-inlined companion-technique
  procedures to the same genuine Read-on-demand mechanism" → chain C3 ✓ (inline)
- "which removes roughly 20% of guaranteed per-invocation load on focused-mode runs..." →
  chain C5 ✓ (inline)
- "Treat re-stating the line-count figure as report-only... i.e., continuing what this project's
  own TEARDOWN-01 record already established" → chain C1 ✓ (inline)
- "and a narrow cleanup pass targeted at the documentation drift chain C4 identified" →
  chain C4 ✓ (inline)
- "the trade-off's flip test shows the three-part bundle beats the structural fix alone by a
  margin too thin... to justify coupling them into one decision" → chain C6 ✓ (inline)
- "a separate source file already exists for every companion technique and all eight are still
  inlined in full on every run regardless" → chain C2 ✓ (inline)
- "the single largest block that structurally qualifies... is the companion-techniques block" →
  chains C2, C5 ✓ (inline)
- "The line-count gate itself was never shown to track anything but its own history..." →
  chain C1 ✓ (inline)
- "Moving the companion procedures onto the Read-on-demand mechanism multiplies that mechanism's
  call sites roughly eightfold... a real, nonzero new failure surface" → chain C6 ✓ (inline,
  "criterion C2 scored 4 of 5")
- "A full-composer run that fires most of the eight techniques gains little or nothing..." →
  chain C6 (second-order extension) ✓ (inline)
- "the headline sizing... rests on a chars/4 token approximation... which is why chains C5 and
  C6 are capped at MEDIUM" → chains C5, C6 ✓ (inline)
- "the growth this analysis diagnoses is only partly structural: a real documentation-drift
  component... would survive this fix untouched" → chain C4 ✓ (inline)
- Confidence line's band and both "would change it" directions → chains C1–C6 ✓ (inline,
  Pre-check head lists all six)

Scan result: 14 of 14 §6 claims carry an inline chain citation; 0 required ledger-row discharge;
0 cut.
## Self-audit scan (process output)

**Table 1 — chain form (section 4)**

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|---|---|---|---|---|---|---|---|
| C1 | GT-4 + GT-5 + GT-6 | yes | n/a | yes | MEDIUM | yes (teardown doc read) | none |
| C2 | GT-1 + GT-9 | yes | n/a | yes | HIGH | yes (ARCHITECTURE.md read + direct observation) | none |
| C3 | GT-8 + C2 | yes | n/a | yes | MEDIUM | yes (ARCHITECTURE.md read) | none |
| C4 | GT-12 + GT-9 | yes | n/a | yes | HIGH | yes (dir listing + doc read) | none |
| C5 | GT-2 + GT-9 | yes | n/a | yes | MEDIUM | yes (wc -l + direct char count) | none |
| C6 | C1 + C2 + C3 + C4 + C5 | yes | n/a | yes | MEDIUM | yes (inherited from C1–C5's reads; no new source needed at this chain's own head) | none |

**Table 2 — claim inventory (section 6)**

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|---|---|---|---|---|
| "Recommended approach:" paragraph | bold lead-in | yes | always-claim lead-in (one of the four template-prescribed lead-ins) | C1, C3, C4, C5, C6 |
| "Key insight:" paragraph | bold lead-in | yes | always-claim lead-in | C1, C2, C5 |
| "Trade-offs acknowledged:" paragraph | bold lead-in | yes | always-claim lead-in | C4, C5, C6 |
| "Pre-check:" line | bold lead-in | no | structural confidence-bookkeeping field required directly above a Confidence line (not an assertion about the subject matter); excluded from the reader-facing report by the Output-format rendering rule, which strips `**Pre-check:**` lines | n/a |
| "Confidence:" paragraph | bold lead-in | yes | always-claim lead-in | C1, C2, C3, C4, C5, C6 |

Scan complete: 6 chain rows, one per section-4 chain block in order; 5 section-6 rows, one per
construct in order — 4 claims under R11, 1 excluded. 0 chains malformed, 0 claims untraced.
## Techniques not applied (process output)

five-whys — not applicable — phase 3 — every ground truth in this analysis bottomed out
directly in a read-at-source citation or direct observation (file content, `wc -l`, a
directory listing) without requiring further recursive decomposition into constituent facts;
the irreducibility test had nothing left to drill.
inversion — not applicable — phase 2 — the Phase 2 assumption set was not suspiciously thin
(eleven assumptions surfaced before any chain-level audit), so inversion's own Phase 2 trigger
did not fire; at Phase 5, the headline conclusion is a plan with a concrete migration path, not
a bare claim, so the pre-mortem-vs-inversion decision rule selected pre-mortem instead.
theoretical-limit — not applicable — phase 4 — no conclusion here turns on a governing hard
constraint being stripped of convention; the quantities at stake (line counts, character counts,
token approximations) are measured directly from the repository, not bounded by a physical or
mathematical ceiling.

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "the real question is not 'how do we get the line count under the budget' but 'what
cost or failure mode was the budget a proxy for, does splitting the file into separate reference
files actually reduce that cost given how Claude Code loads content, and if some split is
warranted, which content should move and by what design — versus trimming, restructuring, or
simply raising/retiring the budget?'"
Band: **Rigorous**
Justification: The statement names the real underlying question rather than the triggering
event (the 878-line figure) or a restatement of the prompt, and all five success criteria are
checkable against the Conclusion section without further interpretation (criterion 5 was revised
during this run specifically to make it checkable against §6's Confidence line rather than
against an artifact outside the six sections).

**Criterion 2: Challenge Assumptions**
Quoted span (from the Assumption Audit scan): "New rows A-12 through A-15 are added to the §2
Classified Assumptions Table... | A-12 | ... | Challenge — flagged, not independently verified |
Surfaced by the end-of-phase Assumption Audit (chain C1, step 3); carried as a confidence caveat
on chain C1 rather than resolved; unverified — flagged. |"
Band: **Rigorous**
Justification: Every row uses the four-type scheme and the prescribed Accept/Challenge/Discard
verdict vocabulary with a leading token, em-dash, and specific justification (fixed during this
run); at least one assumption is actively challenged (most are); every assumption used in a
chain despite being unverified (A-12–A-15) carries the literal "unverified — flagged" notation;
the end-of-phase Assumption Audit ran exhaustively over every named chain step (confirmed by the
Assumption Audit scan's row-per-step coverage) and its surfaced assumptions were added back to
the actual §2 table, not merely narrated in process output.

**Criterion 3: Establish Ground Truths**
Quoted span: "`?`-marked: none (0 of 13)." set against the Ground Truths list, which enumerates
GT-1 through GT-13, each with a `Read-at-source:` citation naming a specific file, section, or
line (e.g., "GT-9 ... Read-at-source: `docs/ARCHITECTURE.md:119`").
Band: **Rigorous**
Justification: The stated enumeration (zero `?`-marked) matches the list on inspection — no GT
carries a suffix; every GT carries a stable ID referenced consistently in the chains; every GT
has a specific, more-than-"common-knowledge" citation with an explicit provenance label
(`Read-at-source:`); every unsuffixed GT feeding a HIGH-confidence chain (C2, C4) names its
exact read-at-source location; no Phase-2-discarded assumption appears in this list.

**Criterion 4: Reason Upward**
Quoted span (from the self-audit scan's Table 1): "C1 | GT-4 + GT-5 + GT-6 | yes | n/a | yes |
MEDIUM | yes (teardown doc read) | none" through "C6 | C1 + C2 + C3 + C4 + C5 | yes | n/a | yes |
MEDIUM | yes (inherited...) | none" — all six rows read `Form conforming? = yes` and
`Dependency clean? = yes`; reconciliation line: "6 chain rows... 0 chains malformed."
Band: **Rigorous**
Justification: All six chains are mechanically form-conforming and dependency-clean per the
scan; each has at least one genuine intermediate step (not a restatement of a named input); the
Abandoned Reasoning section documents four specific dead ends with the What-was-tried /
Why-abandoned / What-it-ruled-out structure, none generic; no analogy is used as direct evidence
anywhere in §4; every assumption surfaced by the end-of-phase audit is declared inline with
`[Assumes: A-N]` on the originating hop (verified by direct inspection: `[Assumes: A-12]`,
`[Assumes: A-13]`, `[Assumes: A-14]`, `[Assumes: A-15]` each appear on the chain step that
introduced them); the Recompute step independently re-derived every computed figure with no
arithmetic error found.

**Criterion 5: Validate**
Quoted span: "C1 ... Inference axis is short: the final hop rests on `[Assumes: A-12]`... Would
raise to HIGH: opening the primary A/B report directly and confirming its quoted result." (chain
C1's Confidence line) together with the adversarial pass record's five labeled parts (Recompute,
Sensitivity, Rival, Premise/Causes/Clusters/Disposition, Falsification), each present with
content.
Band: **Rigorous**
Justification: Every chain's weakest link is named (Sensitivity step, now covering all six
chains including C2); every MEDIUM chain's confidence line names its specific downgrade cause(s)
(`A-12`, `A-13`, `A-14`, or the chars/4 approximation) and what would remove each one; no chain
rates HIGH while consuming a `?`-marked input (none exist); every chain is rated no higher than
the lowest-rated chain its own head cites (verified: C3 cites C2(HIGH) but is itself MEDIUM on
its own Inference axis — permitted, since the rule caps from above only; C6 cites C1/C3/C5 at
MEDIUM and is itself MEDIUM, not higher); the adversarial pass (Pre-Mortem, opened via Read) is
complete with all four required parts plus Recompute, Sensitivity, Rival, and Falsification, and
every cluster carries a named disposition (plan change or accepted risk with mitigation) — none
left box-ticked.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (from the self-audit scan's Table 2): "'Recommended approach:' paragraph | bold
lead-in | yes | always-claim lead-in | C1, C3, C4, C5, C6" through "'Confidence:' paragraph |
bold lead-in | yes | always-claim lead-in | C1, C2, C3, C4, C5, C6" — reconciliation line: "5
section-6 rows... 4 claims under R11, 1 excluded... 0 claims untraced."
Band: **Rigorous**
Justification: Every R11-qualifying claim in §6 traces to a named §4 chain per the scan; no
construct is left untraced; the one excluded construct (`**Pre-check:**`) is correctly excluded
as a structural bookkeeping field, not a claim; the Key Insight ("two independent facts, not one
fact described twice") is a distinct, non-obvious finding about this codebase's architecture
rather than a restatement of the Recommended approach's action items.

**Gate result:** cleared · passes: 1 · Fix/Repeat fired: no (corrections were made to the draft
before this single scoring pass, not as a re-score after a failed one)
## Structured summary (process output)

```json
{
  "schema_version": 1,
  "run_mode": "full-composer",
  "assumptions": [
    {"id": "A-1", "type": "physical law", "verdict": "Accept"},
    {"id": "A-2", "type": "convention", "verdict": "Challenge"},
    {"id": "A-3", "type": "untested belief", "verdict": "Discard"},
    {"id": "A-4", "type": "untested belief", "verdict": "Discard"},
    {"id": "A-5", "type": "physical law", "verdict": "Accept"},
    {"id": "A-6", "type": "current constraint", "verdict": "Challenge"},
    {"id": "A-7", "type": "current constraint", "verdict": "Accept"},
    {"id": "A-8", "type": "convention", "verdict": "Discard"},
    {"id": "A-9", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-10", "type": "convention", "verdict": "Discard"},
    {"id": "A-11", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-12", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-13", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-14", "type": "untested belief", "verdict": "Challenge"},
    {"id": "A-15", "type": "untested belief", "verdict": "Challenge"}
  ],
  "ground_truths": [
    {"id": "GT-1", "read_at_source": true},
    {"id": "GT-2", "read_at_source": true},
    {"id": "GT-3", "read_at_source": true},
    {"id": "GT-4", "read_at_source": true},
    {"id": "GT-5", "read_at_source": true},
    {"id": "GT-6", "read_at_source": true},
    {"id": "GT-7", "read_at_source": true},
    {"id": "GT-8", "read_at_source": true},
    {"id": "GT-9", "read_at_source": true},
    {"id": "GT-10", "read_at_source": true},
    {"id": "GT-11", "read_at_source": true},
    {"id": "GT-12", "read_at_source": true},
    {"id": "GT-13", "read_at_source": true}
  ],
  "chains": [
    {"id": "C1", "confidence": "MEDIUM", "rests_on": ["GT-4", "GT-5", "GT-6"]},
    {"id": "C2", "confidence": "HIGH", "rests_on": ["GT-1", "GT-9"]},
    {"id": "C3", "confidence": "MEDIUM", "rests_on": ["GT-8", "C2"]},
    {"id": "C4", "confidence": "HIGH", "rests_on": ["GT-12", "GT-9"]},
    {"id": "C5", "confidence": "MEDIUM", "rests_on": ["GT-2", "GT-9"]},
    {"id": "C6", "confidence": "MEDIUM", "rests_on": ["C1", "C2", "C3", "C4", "C5"]}
  ],
  "dead_ends": [
    "Treating the prompt as a self-contained hypothetical",
    "Accepting general SKILL-authoring line-count guidance as sufficient justification",
    "Exhaustive line-by-line duplication audit",
    "Uniform 'split everything' recommendation across all four content types"
  ],
  "techniques": {
    "applied": ["fishbone", "estimate", "trade-off", "second-order", "pre-mortem"],
    "not_applied": [
      {
        "technique": "five-whys",
        "phase": 3,
        "reason": "every ground truth bottomed out directly in a read-at-source citation or direct observation without requiring further recursive decomposition into constituent facts"
      },
      {
        "technique": "inversion",
        "phase": 2,
        "reason": "the Phase 2 assumption set was not suspiciously thin, so inversion's own trigger did not fire; at Phase 5 the conclusion is a plan with a concrete migration path, so the decision rule selected pre-mortem instead"
      },
      {
        "technique": "theoretical-limit",
        "phase": 4,
        "reason": "no conclusion here turns on a governing hard constraint being stripped of convention; the quantities at stake are measured directly, not bounded by a physical or mathematical ceiling"
      }
    ]
  },
  "gate": {
    "passes": [
      {
        "bands": ["Rigorous", "Rigorous", "Rigorous", "Rigorous", "Rigorous", "Rigorous"],
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
    "recommendation": "Do not pursue the naive 'move lines into another file that still gets inlined at build time' fix, and do not treat the raw line count itself as the thing to optimize — both are the gaming move the prompt was right to be suspicious of, and both score worst or near-worst among six scored options (chain C6). Adopt the structural fix instead: convert the eight always-inlined companion-technique procedures to the same genuine Read-on-demand mechanism already proven, with no recorded regression, for the output template and validation rubric (chain C3), which removes roughly 20% of guaranteed per-invocation load on focused-mode runs and a smaller, variable amount on full-composer runs (chain C5), and which the trade-off scores as the clear structural winner (chain C6). Treat re-stating the line-count figure as report-only and never gating — i.e., continuing what this project's own TEARDOWN-01 record already established (chain C1) — and a narrow cleanup pass targeted at the documentation drift chain C4 identified, as cheap, separable follow-ups rather than a bundled prerequisite: the trade-off's flip test shows the three-part bundle beats the structural fix alone by a margin too thin (a two-step weight move away from a tie) to justify coupling them into one decision (chain C6).",
    "confidence": "MEDIUM",
    "rests_on": ["C1", "C2", "C3", "C4", "C5", "C6"]
  }
}
```
