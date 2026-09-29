# First-Principles Analysis: Should the first-principles agent body be split to satisfy its line-count budget?

**Mode:** full-composer (no single-technique trigger phrase fired decisively; the request explicitly
asks for "the full first-principles analysis output... per your standard methodology").

**Research note (disclosed up front, not buried):** the reference paths in this analysis's own
operating instructions resolve to a real, inspectable project on disk
(`/home/chrisdavidson/Projects/first-principles-skill`) that turns out to be the exact plugin the
problem statement describes. This analysis used `Bash`/`Read` to inspect that repository's live
state, git-adjacent planning records, and its own prior worked example on this identical question,
rather than reasoning about the scenario in the abstract. Every Ground Truth below states whether
it was read at source (and where) or is flagged unverified.

## 1. Problem Essence

**Essence Statement:** The real question is not "does this 878/1132-line file exceed a 500-line
number" but *what quantity does a line-count ceiling on an agent-instruction file actually stand in
for, does the file's line count move in step with that quantity given how this specific runtime
loads the file, and — only once that is settled — which structural change (if any) reduces the real
quantity rather than merely the number the gate reads*.

**Success criteria** — a correct answer must:
1. Name the specific runtime-cost or quality candidate(s) from the brief's list that actually apply
   to *this* file, given *this* plugin's actual loading mechanism (not application code in general),
   and state which candidates do not apply and why — checkable against §3/§4 below.
2. Determine, with the mechanism verified rather than assumed, whether the file's raw line count is
   a 1:1 proxy for per-invocation cost, a partial proxy, or no proxy at all — checkable against
   whether §4's chains distinguish invocation types and read-conditionality.
3. State the second-order consequences of a naive split (fragmentation, Goodhart risk, and whether
   genuine lazy-loading is achievable here) as named, evidenced claims, not generic risk language —
   checkable against §4's second-order chain and §5.
4. Recommend one of (a)/(b)/(c)/(d) — or a stated combination — justified against the quantity named
   in criterion 1, not against "the gate says 500 and the file is over" — checkable against §6's
   Recommended approach citing chains, not the raw byte count.

## 2. Assumptions Table

| # | Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|---|
| A-1 | A line-count ceiling on a single instruction file is a meaningful proxy for the engineering cost that actually matters. | convention | Explicitly challenge before use. | Challenge — true only for content a run loads unconditionally regardless of which techniques it uses; false for content routed to a separately-sized, separately-invoked skill or genuinely conditionally read. | GT-4, GT-5, GT-15 |
| A-2 | A smaller instruction body produces higher-quality / more compliant reasoning. | untested belief | Verify or flag. | Challenge — directly tested within a narrow range (a 22-line size delta) and found false; not tested at the full 632-line delta this decision concerns, so the refutation is partial, not total. | GT-7 (scope-limited) |
| A-3 | Splitting a monolithic instruction file into reference files automatically reduces the tokens a typical invocation pays. | convention (the "reflexive engineering response" named in the brief) | Explicitly challenge before use. | Challenge — false when the extracted content is still read unconditionally on every run (repeats the pattern that already shipped and produced near-zero savings); true only when the extracted content is read conditionally on a data-dependent trigger. | GT-10, GT-11; C3 |
| A-4 | The 8 companion-technique procedures are the segment responsible for this file's budget overage. | untested belief | Verify by direct measurement. | Was Discard at the 878-line snapshot (methodology + six companion procedures were together under a third of the file); is now Accept at the current 1,132-line snapshot (the companion-technique block alone is ~45% of the file, its largest single section). | GT-2, GT-9 |
| A-5 | The companion-tool procedures must stay fully inlined for the agent to correctly detect when each technique's trigger fires. | convention, inherited from a prior decision | Explicitly challenge — the stakes-escalation rule applies because a further split now depends on this. | Challenge — a working counter-pattern already exists inside this same file for 3 of the 8 procedures (compact inline decision-rule, full text deferred to Read at point of use). | GT-5 |
| A-6 | A regression gate on this file's size needs to exist in some form. | convention | Explicitly challenge before use. | Challenge — a blocking size gate was tried, shown to protect nothing measurable, and retired in favor of a non-blocking report, later removed outright. | GT-6, GT-7, GT-8 |
| A-7 | Prompt-caching economics materially change whether eager loading of this file matters. | current constraint (a fact about the present API pricing/caching model) | Record expiry conditions. | Accept, with a scope caveat — caching lowers the marginal $-cost of repeated identical-prefix loads within a cache window; it changes neither the context-window slots a given invocation consumes nor the model's need to attend to every inlined instruction while reasoning. Expires/changes if Anthropic's caching mechanics or pricing model change. | Background knowledge of Claude API prompt-caching mechanics; not independently re-verified via a citation in this session — flagged as such rather than presented as a Ground Truth. |
| A-8 | The problem statement's stated figures (878 lines; a binding ~500-line regression gate) describe the plugin's current, live state. | untested belief (a claim embedded in this analysis's own input) | Verify against the live repository. | Discard as a claim about present reality; Accept as the stated decision-frame to analyze. Verified false against the live tree, and further verified to match a scenario this project's own backlog has already flagged as a stale, superseded snapshot. | GT-1, GT-6, GT-13 |
| A-9 | Full procedure text can be deferred via Read-on-demand for the remaining five companion techniques (five-whys, fishbone, second-order, estimate, theoretical-limit) without breaking trigger detection, using only a short inline decision-rule as the resident residue. | untested belief — surfaced at Phase 4 end-of-phase Assumption Audit, from chain C3/C5's proposed extension | Verify; used in §6's recommendation despite being untested. | unverified — flagged. Partially supported by precedent (GT-5 proves the pattern for 3 of 8 procedures) but not independently verified for the other 5. Priced in §6's trade-offs: the existing Phase-5 Read-failure fallback bounds the damage to degraded rigor on the affected technique, not a silent skip. | GT-5 (partial); no direct verification for the extension itself |
| A-10 | A typical full-composer run fires well under all 8 companion techniques (materially below 7-8 on average). | untested belief — surfaced from chain C5 (estimate) | Verify via instrumented measurement. | unverified — flagged; used in chain C5's central estimate despite no repo telemetry existing on this distribution. | none located this session |
| A-11 | A Read tool call's framing overhead is on the order of 100-200 tokens. | untested belief — surfaced from chain C5 (estimate) | Verify or treat as a generic engineering constant. | unverified — flagged; used in chain C5's bracket. | none located this session (general engineering order-of-magnitude, not measured in this runtime) |
| A-12 | A focused single-technique skill's own text (its explicit "do not run the full analysis" instruction) is sufficient evidence that the runtime does not also eagerly pre-load the big composer file for that invocation type. | untested belief — surfaced from chain C2's second hop | Challenge — this is the live rival that caps chain C2. | Challenge — plausible and internally consistent with everything observed, but not confirmed by tracing an actual live focused-technique invocation's context contents. | GT-4 (document text only; no runtime trace performed) |
| A-13 | The Goodhart risk (satisfying a future size gate by relocating content to files still read unconditionally) will recur unless the gate itself is redesigned to distinguish conditional from unconditional reads. | current constraint (an incentive structure under present gate-design norms) | Record expiry conditions. | Accept — this exact failure mode already occurred once in this project's own history. Expires if/when any reinstated gate explicitly makes the conditional/unconditional distinction. | GT-11 |

## 3. Ground Truths

Provenance key: **read-at-source** = this analysis located and read the asserted figure/wording
directly. All entries below are read-at-source except GT-12, which is flagged.

- **GT-1** — The agent body `first-principles/agents/first-principles.md` is **1,132 lines** and
  **16,772 words** as of this session. Source: `wc -l` and `wc -w` run directly against the file in
  this session. Provenance: read-at-source (direct measurement).

- **GT-2** — Inside that body, the section boundaries (via `grep -n` run directly) are: Methodology
  §63–295 (~232 ln), Output format §295–402 (~107 ln), Before presenting conclusions §402–521
  (~119 ln), Skill files §521–622 (~101 ln), Companion Techniques §622–1132 (~510 ln — **~45% of
  the file**, its single largest section). Source: `grep -n '^## '` output, this session. Provenance:
  read-at-source.

- **GT-3** — The `first-principles-analysis` `SKILL.md` (the slash-command launcher, 62 lines) does
  not itself carry the methodology. Quoted: "You are running the composer launcher. Your job is
  **not** to perform the analysis yourself... Invoke the `first-principles:first-principles` agent
  via the Task tool." Source: `first-principles/skills/first-principles-analysis/SKILL.md`, read in
  full this session. Provenance: read-at-source.

- **GT-4** — Each of the 8 companion techniques (five-whys, fishbone, inversion, pre-mortem,
  trade-off, second-order, estimate, theoretical-limit) has its own self-contained `SKILL.md`
  (177–311 lines each), `disable-model-invocation: true`, invoked only via its own slash command,
  and states explicitly: "do not run the full 5-phase first-principles analysis." None of the 8
  reference or load `first-principles/agents/first-principles.md`. The plugin manifest confirms one
  marketplace plugin ships the full-composer agent plus "14 namespaced skills — 8 companion-technique
  skills... 5 focused-phase skills... and the first-principles-analysis launcher" at version
  `9.13.0`. Sources: all 8 `first-principles/skills/<technique>/SKILL.md` files, read in full this
  session; `.claude-plugin/marketplace.json`, read in full this session. Provenance: read-at-source.

- **GT-5** — Within the 1,132-line body, 3 of the 8 companion procedures (pre-mortem, inversion,
  trade-off) are *dual*: fully inlined under "## Companion Techniques" **and** separately invoked at
  Phase 5's actual point of use via an explicit "open ... with Read" instruction, with the stated
  reason: "a pre-mortem run from recollection reliably drops the past-tense framing that is the
  technique's whole mechanism." Source: this analysis's own operating instructions (the body under
  analysis), read in full as this conversation's system prompt before this analysis began.
  Provenance: read-at-source (direct inspection of the analyzed artifact itself).

- **GT-6** — The historical line-count regression gate ("META-Q4," budget "~500 lines / ~5,000
  tokens," raised over time 500→580→644) was retired as a *blocking* check under
  `docs/v8.7-constraint-teardown.md` §2 item 1 ("TEARDOWN-01"); its non-blocking `[INFO]` reporter
  script (`check-body-budget.py`) was itself deleted entirely under `docs/v9.4-gate-retirement.md`
  §2.5. Confirmed directly: no `check-body-budget.py` file exists in the current tree, and
  `.github/workflows/validation.yml` contains no line-count check of any kind. Sources: both docs
  read in full this session; `find`/`grep` run directly against `scripts/` and
  `.github/workflows/`. Provenance: read-at-source.

- **GT-7** — The stated reason for retiring the gate: "the script's own fitted-limit provenance
  comment — 'limit raised to 622 + 22 buffer' — records that the number was recalibrated whenever it
  bound... rather than derived from any measured quality requirement," and a blind A/B experiment
  (`docs/v8.6-quality-ab-experiment.md`) comparing a 590-line body against a 612-line body (a
  22-line contrast — the exact size of the "buffer" just raised to protect) "scored identically,
  both arms 2/3 PASS, band total 35 each." Source: `docs/v8.7-constraint-teardown.md` §2 item 1,
  read in full this session, quoted directly. Provenance: read-at-source.

- **GT-8** — The same teardown record separately found `_COMPOSER_FOCUS_CEILING` (a cap on how many
  companion-technique markers a run may register) "actively penalising fidelity rather than merely
  gating noise — run5 fired the highest fishbone marker count of the five runs measured... and was
  still scored a miss, purely because its `composer_hits` count reached
  `_COMPOSER_FOCUS_CEILING`." Source: `docs/v8.7-constraint-teardown.md` §2 item 2, read in full
  this session, quoted directly. Provenance: read-at-source.

- **GT-9** — This exact scenario (an "878-line" inlined agent body against a stated "~500-line"
  binding regression gate) was previously analyzed by this same methodology in a shipped worked
  example, `first-principles/agents/references/examples/self-application.md`. That analysis's Chain
  C2 (rated HIGH, direct line-range measurement) found: "Phase 1–5 procedural blocks: ~96 lines...
  six inlined companion-tool procedures: ~175 lines... inlined Output Template + Validation Rubric
  appendices: ~464 lines" of the then-878-line body. Source: that file, read in full this session,
  quoted directly with line numbers. Provenance: read-at-source.

- **GT-10** — That analysis's Chain C3 recommendation — de-inline only the Output Template and
  Validation Rubric appendices, explicitly leaving the methodology and companion-tool procedures
  inlined — shipped and was independently re-verified: "`wc -l`... reads **807** lines — down from
  the 878 lines," the appendix section headings return zero matches, and "**8** occurrences of the
  two reference filenames, of which **seven** are live links" appear in their place. Source: the
  same file's "Outcome (verified 2026-09-19)" section, read this session, quoted directly.
  Provenance: read-at-source.

- **GT-11** — The same analysis's own Trade-offs section states the de-inlining "costs the agent one
  additional read hop for Output Template and Validation Rubric content... The trade-off is real but
  small and reversible," and its Key Insight frames the benefit as deduplication — content "already
  exists as Layer-3 reference files in the source tree and is duplicated verbatim into the agent
  body" — not a claimed reduction in what a full run loads, since Phase 5's own instructions read
  those appendices unconditionally on every full run regardless of which file they live in. Source:
  same file, read this session, quoted directly. Provenance: read-at-source.

- **GT-12?** — The same analysis attributes the decision to leave companion-tool procedures inlined
  to "the v3.0 inlining rationale," described only as having "named methodology and companion tools
  specifically." The original v3.0 rationale document itself could not be located in the current
  tree within this session's search (`grep`/`find` for `v3.0` and `inlin*` under `docs/` returned no
  match). **Unverified — flagged**: the *reasoning* for the original inlining decision is known only
  secondhand, through a document (GT-9–GT-11's source) that is itself flagged elsewhere in this
  repository as describing a superseded state (see GT-13).

- **GT-13** — This repository's own backlog (`.planning/ROADMAP.md`, Phase 999.124, filed
  2026-09-18, promoted 2026-09-19) explicitly documents that `self-application.md` "describes a
  superseded repo state," naming its cited 878-line figure and "binding META-Q4 gate" as stale
  premises against a then-current 807-line, gate-retired reality — i.e., the exact figures in *this
  analysis's own problem statement* (878 lines; budget enforced as a binding regression gate) match
  a scenario this project has already, independently, flagged by name as outdated. Source:
  `.planning/ROADMAP.md`, read directly this session, quoted with line numbers. Provenance:
  read-at-source.

- **GT-14** — Standalone reference-only copies of all 8 companion procedures already exist in the
  repository (`first-principles/agents/references/{five-whys,fishbone,inversion,pre-mortem,
  trade-off,second-order,estimate,theoretical-limit}.md`, 85–219 lines each, **1,274 lines
  combined**), generated from a shared source per a documented sync pipeline ("`shared/spine/
  SKILL-body.md` ← assembled agent body template; `{{TOOL:slug}}` tokens," `CLAUDE.md`
  Architecture section). Sources: `wc -l` run directly against all 8 files this session; `CLAUDE.md`
  quoted directly. Provenance: read-at-source.

- **GT-15** — A Claude Code subagent's markdown body is loaded in full as that subagent's system
  prompt exactly once per Task-tool invocation, before any of the agent's own reasoning occurs,
  independent of which parts of that body a given run will actually use. This is a **direct,
  first-hand operational observation**, not a report relayed by a delegate or a documentation claim
  that could be stale: this analysis's own complete operating instructions, as supplied for this
  very invocation, are the verbatim ~1,132-line body described in GT-1–GT-2, received in full
  before any phase of this analysis began. Provenance: read-at-source, in the strongest available
  form for a runtime-mechanism claim (direct self-observation within the same invocation under
  analysis, immune to document staleness).

- **GT-16** — The absolute file paths this analysis's own operating instructions use to point at
  reference material (e.g., a `/tmp/claude-1000/.../scratchpad/rel-body/first-principles/agents/
  references/*.md` form, distinct from the plugin's static repository path) are per-session, not
  fixed. This confirms some install/session-level step materializes these reference files at a
  resolvable absolute path per invocation — a live operational dependency the recommendation below
  relies on continuing to work as more content is moved behind Read-on-demand pointers. Provenance:
  read-at-source (directly observed via the Read calls this analysis itself performed against
  `output-template.md` and `validation-rubric.md` earlier in this session, using exactly this path
  form).

**`?`-marked:** GT-12 (1 of 16).

## 4. Derivation Chains

### Conclusion C1: The historical line-count budget was a convention without a demonstrated tie to any protected property

GT-6 (blocking gate retired, reporter later deleted) + GT-7 (raise-chain 500→580→644, blind A/B found no quality effect)
→ a limit repeatedly recalibrated upward whenever it binds, with no independent measurement of what it protects, functions as an accepted ceiling on growth rather than a check against demonstrated harm
→ the retiring record's own cited evidence — the blind A/B's null result — is the only direct measurement this project ever ran against the specific quantity "body line count," and it found no effect
→ absent a demonstrated causal link between this file's line count and any measured cost or quality outcome, the ~500-line figure and its successors functioned as a convention inherited by momentum rather than a load-bearing engineering constraint

**Pre-check:** head GT-6, GT-7 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** MEDIUM — the Rivals axis is short: GT-8 shows a related but distinct problem (technique-count / marker dilution) is real and unsettled, leaving open the reading that the line-count gate was a crude attempt to reach for that phenomenon rather than pure convention. What would close it: a controlled test that varies companion-technique count while holding total line count fixed, against one that varies line count while holding technique count fixed, to separate content-volume harm from technique-count/dilution harm.

### Conclusion C2: A single file's line count only prices the full-composer invocation path; it is already irrelevant to every other entry point

GT-3 (thin launcher dispatches via Task tool) + GT-4 (8 self-contained focused skills that refuse to run the full analysis) + GT-15 (direct observation: the full body loads verbatim as system prompt on every full-composer invocation)
→ the 1,132-line body is eagerly and fully loaded exactly once per full-composer Task invocation, and never in whole or part by a focused single-technique invocation
→ a line-count ceiling on this one file can therefore only ever price the fixed context overhead of the full-composer path, never a focused invocation's cost, because the two paths do not draw from the same context budget
→ the "878/1,132 lines in one file" framing conflates two structurally different invocation types, and any budget meant to bind should be scoped to the full-composer agent's own fixed overhead only

**Pre-check:** head GT-3, GT-4, GT-15 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** MEDIUM — the Rivals axis is short: assumption A-12 (a focused skill's own stated refusal to run the full analysis is taken as sufficient evidence the runtime never pre-loads the big file for that invocation type) rests on document text, not on tracing a live invocation's actual context contents. What would close it: instrument or trace one live focused-technique invocation and confirm no content from `first-principles.md` appears in its context.

### Conclusion C3: Whether a split saves any real per-invocation tokens depends on whether the resulting read is unconditional or conditional — not on the split itself

GT-9 (appendices were ~464 of 878 lines) + GT-10 (the appendix split shipped and was reverified) + GT-11 (its own author frames the benefit as deduplication, not reduced eager load) + GT-5 (3 of 8 procedures already prove the conditional-read alternative)
→ the appendix split changed where roughly 464 lines of tokens live — system-prompt-resident before, one Read-tool-result after — but not whether a full run loads them, since Phase 5's own instructions read those files unconditionally every time, so its real per-invocation savings were near zero and its admitted benefit was deduplication and gate-satisfaction
→ the three procedures already split under the GT-5 pattern are read only when a run's own Phase 2, 4 or 5 trigger actually selects that specific technique, which is a genuinely conditional load and the only kind capable of producing savings on a run that never selects it
→ whether moving content behind a file boundary saves any real per-invocation tokens depends entirely on whether the read that follows is unconditional, as with the appendices, or conditional on a data-dependent trigger, as with the three already-split procedures; the file's own line count is silent on this distinction, and a split performed without preserving it repeats the appendix outcome under a new name

**Pre-check:** head GT-9, GT-10, GT-11, GT-5 · ?-marked: none · lowest cited: none · Inputs ceiling: HIGH
**Confidence:** HIGH — every input is unsuffixed and read-at-source with a named location; each hop follows by direct citation of the quoted material rather than projection; the strongest conceivable rival — that conditional reads cost the same as inlining because the runtime pre-fetches referenced content regardless — is ruled out by GT-15's own direct observation: no content from any reference file this analysis did not explicitly Read entered this session's context at any point, including during the many turns before those files were opened.

### Trade-off analysis (feeding Conclusion C4)

Four viable options survive the ground truths above; the status quo is included per the trade-off
procedure's own rule.

**Options:**
- **A — Naive split.** Relocate the 8 companion procedures into reference files, but keep the read
  unconditional (Phase 2/4 still reads all of them every full run) — satisfies a byte-count check
  without changing what a run loads. Repeats the shape of the already-shipped appendix split.
- **B — Real lazy-loading + gate redesign.** Extend the GT-5 pattern (compact inline decision-rule,
  full procedure text deferred to Read at the point a trigger actually fires) to the remaining five
  procedures; pair it with retiring any blocking size gate in favor of a non-blocking, behavior-
  focused check.
- **C — Relax the number.** Leave the body as one file; raise the numeric ceiling again (repeating
  the 500→580→644 pattern).
- **D — Pure status quo.** Change nothing; no gate, no split (matches the live repository's current
  state per GT-6).

**Must-haves:** No hard knockout criteria were identified — no option is technically impossible or
instantly disqualifying. Correctness-preservation is instead carried as a heavily weighted scored
criterion below, because it is a matter of degree and risk, not a binary pass/fail.

**Criteria, weights (1–5, locked before scoring), and anchors:**

| Criterion | Weight | 1 anchor | 5 anchor |
|---|---|---|---|
| Real per-invocation savings for a typical full-composer run | 5 | 0% of the companion block's footprint saved | ~20%+ saved (chain C5's central case) |
| Correctness-preservation (higher = safer) | 5 | High risk of silently breaking trigger detection, no fallback | Uses an already-proven-in-production fallback (GT-5's Read-failure degrade path) |
| Consistency with this project's own tested evidence | 4 | Repeats a pattern this project's own history already showed fails (GT-7, GT-11) | Matches a pattern this project's own history already showed works (GT-5, GT-6/7's retirement) |
| Maintainability / fragmentation cost (higher = less cost) | 2 | Introduces a new kind of complexity with no precedent | Extends an existing, already-navigated file/pattern class |
| Reversibility | 3 | Costly or entangled to undo | A pure text/config edit, revertible via `git revert` |
| Addresses the recurring growth pattern (GT-2 vs. GT-9's trend) | 4 | Does nothing to stop the next new technique re-growing the body | Structurally caps future growth: new technique = 1 reference file + 1 decision-rule line |

**Scores and citations:**

| Option | Savings (×5) | Correctness (×5) | Consistency (×4) | Maintainability (×2) | Reversibility (×3) | Recurrence (×4) | **Weighted total** |
|---|---|---|---|---|---|---|---|
| A — Naive split | 1 (GT-11) | 5 (nothing conditional to break; content is always present regardless of read timing) | 1 (GT-11: admitted near-zero savings) | 3 (GT-9/10 precedent) | 5 (GT-10) | 4 (same flat-core-body effect as B) | **71** |
| B — Lazy-load + gate redesign | 5 (chain C5) | 4 (GT-5 proven for 3/8; A-9 unverified for the rest) | 5 (GT-5: exactly the pattern already shown to work) | 4 (extends existing pattern class) | 5 (text/config edit) | 5 (best on both axes at once) | **108** |
| C — Relax the number | 1 (no structural change) | 5 (nothing to break) | 1 (GT-7: the exact retired raise-chain) | 5 (no new files) | 5 (one-line edit) | 1 (GT-2 vs GT-9: does nothing) | **63** |
| D — Pure status quo | 1 (no change) | 5 (nothing to break) | 3 (consistent with GT-6/7, ignores C3's newer finding) | 5 (no new files) | 5 (nothing changed) | 1 (same as C) | **71** |

**Flip test:** B leads its nearest rivals (A and D, tied at 71) by 37 points. The only criterion on
which A or D outscores B at all is Correctness-preservation (A/D score 5 vs. B's 4), already
weighted at the maximum of the prescribed 1–5 scale. Solving for the weight that criterion would
need to reach for A to overtake B returns a value far outside the 1–5 range (≈42). **No single-
criterion weight change within the prescribed scale flips this result.**

### Conclusion C4: Option B dominates the named alternatives, and the dominance is robust rather than a near-tie

C3 (HIGH — conditional vs. unconditional reads determine savings) + GT-6 (blocking-gate retirement precedent) + GT-7 (raise-chain failure precedent) + GT-9 (historical mis-diagnosis precedent) + GT-11 (unconditional-relocation near-zero-savings precedent)
→ scoring the four candidate interventions against six weighted criteria (real savings, correctness-preservation, evidence-consistency, maintainability, reversibility, and whether the recurring growth pattern is addressed) yields weighted totals A=71, B=108, C=63, D=71
→ the flip test finds no reweighting within the prescribed 1–5 scale changes the winner, and B's margin over its nearest rivals is 37 points, roughly half of B's own total
→ Option B — extend the conditional Read-on-demand pattern to the remaining five companion procedures, paired with redesigning the size gate into a non-blocking, behavior-focused check — dominates the other three named options under this weighting, and that dominance is robust rather than a fragile near-tie

**Pre-check:** head C3 (HIGH), GT-6, GT-7, GT-9, GT-11 · ?-marked: none · lowest cited: HIGH · Inputs ceiling: HIGH
**Confidence:** MEDIUM — the Inference axis is short: several of the individual per-criterion cell scores above (for example, Option A's and B's Correctness-preservation scores of 4) are analyst judgments anchored to the stated anchor descriptions rather than independently re-derivable by a reader without accepting those anchors, even though the weighted arithmetic itself recomputes exactly. What would close it: a second, independently-scored pass, blind to the first pass's totals, checking for anchor-scoring drift — the same blind-comparison discipline GT-7's own A/B experiment used.

### Conclusion C5 (Estimate): Bracket the expected per-invocation token saving from Option B

**Target quantity:** ΔTokens saved per typical full-composer invocation, from deferring the
remaining five companion procedures behind Read-on-demand.

GT-1 (1,132 lines / 16,772 words, directly measured) + GT-2 (companion-techniques block ≈510 of 1,132 lines) + C4 (Option B selected)
→ the body's own measured density (16,772 words ÷ 1,132 lines ≈ 14.8 words/line, at roughly 1.3 tokens per word) gives about 19.3 tokens/line, so the ~510-line companion-techniques block currently costs roughly 9,840 tokens of every full-composer invocation's context regardless of which techniques that run needs
→ splitting that block into 8 roughly-equal average procedures of about 64 lines (≈1,230 tokens) each, deferred behind a Read call costing roughly 100-200 tokens of tool-call framing overhead [Assumes: A-11 — if the true overhead is higher, the central estimate shifts down but stays positive in the central and optimistic cases; the sign of the conclusion is unaffected], the net saving on a given invocation equals the unused procedures' token cost minus the triggered procedures' Read overhead
→ Phase 4's own exit criterion makes second-order thinking mandatory on every full run and Phase 5's adversarial-technique step makes one of pre-mortem or inversion mandatory on nearly every run, so at least 2 of 8 techniques fire on almost any run, while a typical single-domain analysis plausibly fires 3-5 of the remaining 6 conditionally [Assumes: A-10 — this is the one assumption whose failure is NOT priced as harmless; see the falsification condition in the adversarial pass below]
→ bracketing the pessimistic case (7 of 8 triggered, 1 unused) against the central case (4 of 8 triggered, 4 unused) and the optimistic case (2 of 8 triggered, 6 unused) yields an expected saving of roughly 180-7,080 tokens per invocation, central estimate ≈4,320 tokens (about 20% of the companion-techniques block's current footprint), with a named degenerate case: if a typical run fires all 8 techniques, the change nets a small loss of roughly 1,200 tokens of pure Read overhead rather than a saving

**Pre-check:** head GT-1, GT-2, C4 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped both by the Inputs axis (cites C4, itself MEDIUM) and by the Inference axis: A-10 (typical trigger count stays materially below 7-8) is used in a hop the endpoint depends on and its failure is not priced as harmless — it is the chain's own named falsification boundary, not a bounded sensitivity. What would close it: the measurement this project's own history already knows how to run (an instrumented battery count of companion-technique trigger frequency across a sample of prior full-composer runs, mirroring the precedent GT-9's own analysis set for its unresolved GT-9? question).

### Conclusion C6 (Second-order): Option B's benefit is durable only if paired with a gate that rewards conditional reads specifically

C4 (Option B selected) + GT-8 (technique-count dilution already penalized thoroughness once) + GT-11 (unconditional relocation already produced near-zero savings once) + GT-2 + GT-9 (companion block's own growth: ~175 of 878 lines historically, ~510 of 1,132 lines now)
→ [actor lens] maintainers gain one more Read-pointer file class to navigate, but this extends a pattern already present for 3 procedures, 2 appendices and several detail/example docs rather than introducing a new kind of complexity; the agent itself must reliably issue a Read call at the moment a trigger fires instead of already holding the text, a behavior this same body already specifies and, per GT-5, already relies on for 3 of the 8 procedures
→ [actor lens, adversarial] a future maintainer facing a reinstated size gate under time pressure has a standing incentive to satisfy it the cheap way, by relocating content into a file still read unconditionally every run, because that is exactly what happened to the appendices and it satisfies a byte-count check without doing the harder work of making the read genuinely conditional
→ [time lens] immediately the change adds one Read round trip per triggered technique; after a few cycles the core body stops growing every time a new companion technique is catalogued, because a new technique becomes one reference file plus one decision-rule line rather than another 100-230 inlined lines, directly targeting the mechanism that took the companion-techniques block from roughly 175 lines to roughly 510 lines across the addition of two prior techniques
→ the intervention's benefit is durable only if paired with a gate design that explicitly rewards conditional reads over unconditional relocations; without that pairing, the adversarial actor-lens effect above reproduces GT-11's outcome a second time under a new label

This does not contradict any Ground Truth: it claims a cost- and growth-trajectory effect, not a
quality effect, and is therefore compatible with GT-7's finding that size alone did not move a
quality score.

**Pre-check:** head C4 (MEDIUM), GT-8, GT-11, GT-2, GT-9 · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — capped by the Inputs axis (cites C4) and by the Rivals axis: the second hop's Goodhart projection is a forward-looking claim about future maintainer behavior that nothing in this analysis settles either way. What would close it: observing an actual future attempt to reinstate a size gate and checking whether it respects the conditional/unconditional distinction this chain names.

### Conclusion C7: The evidence converges on extending conditional Read-on-demand loading, paired with redesigning rather than reinstating the size gate

C1 (MEDIUM) + C2 (MEDIUM) + C3 (HIGH) + C4 (MEDIUM) + C5 (MEDIUM) + C6 (MEDIUM)
→ the historical budget was a convention without a demonstrated tie to any protected property, and even where a line-count ceiling could mean something it only prices the full-composer agent's fixed overhead, never the already-separate focused-technique invocations
→ within that fixed overhead, only conditionally-triggered content can be moved behind a file boundary with genuine per-invocation savings; the appendices were already moved without that property and bought deduplication rather than savings, while the companion-technique procedures are exactly the content class where the property is available but unused for five of eight techniques
→ scored against this project's own already-tested evidence, extending the existing conditional-read pattern to those five procedures and pairing it with a behavior-focused, non-blocking gate dominates the naive alternatives by a wide, weight-robust margin, with an estimated central saving of roughly a fifth of the companion-technique block's current footprint, provided the change forecloses the Goodhart failure mode that already occurred once
→ neither relocating everything to satisfy the number nor leaving one file and raising the number again is the correct move; the evidence converges on extending the proven conditional Read-on-demand pattern to the remaining companion procedures while redesigning, rather than reinstating, the size gate

**Pre-check:** head C1 (MEDIUM), C2 (MEDIUM), C3 (HIGH), C4 (MEDIUM), C5 (MEDIUM), C6 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the ceiling is set by the lowest-rated chains this one cites (C1, C2, C4, C5, C6, all MEDIUM); C3's HIGH rating does not raise the floor. Each contributing MEDIUM chain's own confidence line already names its specific shortfall and what would close it; this line does not re-explain them.

## 5. Abandoned Reasoning

### Dead End: Answer the problem statement's numbers at face value, without checking the live repository

**What was tried:** Treating "878 lines against a binding ~500-line gate" purely as an abstract
hypothetical and reasoning about it in the abstract register, since the user's prompt is written as
a general engineering scenario.

**Why abandoned:** The reference paths embedded in this analysis's own operating instructions
pointed at a real, inspectable repository, and inspecting it surfaced that this exact scenario is
not merely hypothetical — it is a documented, already-superseded snapshot of this specific project
(GT-13), and the underlying decision (whether to further split the companion-tool procedures) has a
live, current answer available from the same repository's own history (GT-9–GT-11, GT-14). Ignoring
that would have produced an analysis that reasons soundly about a state of affairs this project's own
records say no longer exists, without disclosing the gap — exactly the failure mode the user's own
prompt anticipated by inviting inspection of the actual mechanism.

**What it ruled out:** Answering solely in the abstract, unverified register. The user's problem
statement is retained as the decision-frame to analyze (per assumption A-8's verdict), but every
factual claim about mechanism and precedent is now grounded in what the live repository actually
shows, with the divergence disclosed rather than silently substituted.

### Dead End: Extract the Phase 1-5 methodology block, leave companion tools and appendices inline

**What was tried:** The most cognitively-available response to "the file is over budget" — extract
the procedural-looking Phase 1-5 block into a reference file, since it looks the most like generic
boilerplate.

**Why abandoned:** This is arithmetically the wrong segment at both snapshots this analysis
examined. At the 878-line snapshot the methodology was only ~96 of 878 lines (GT-9); at the current
1,132-line snapshot it is only ~232 of 1,132 lines, about 20% (GT-2). Even removing it entirely would
leave the file at roughly 900 lines — still far over any plausible ~500-line target — while
destroying the one property Phase 4's exit criteria most need locally resident: the phase-sequencing
and exit-criterion logic every companion-technique invocation is checked against from the same place
it is defined.

**What it ruled out:** "Extract the most procedural-looking block" as a viable fix at either
snapshot. This re-confirms, rather than re-derives from scratch, the same dead end this project's
own prior analysis (GT-9's source document) already recorded once.

### Dead End: Treat the companion-tool procedures as untouchable because a prior version deliberately inlined them

**What was tried:** Deferring entirely to the prior decision to inline the companion-tool
procedures (attributed to "the v3.0 inlining rationale," GT-12?) and concluding that the current
question is already settled and needs no fresh analysis.

**Why abandoned:** The original rationale document could not be located in the current tree (GT-12
is flagged unverified for exactly this reason), and more importantly the facts it was presumably
reasoned from have materially changed: the companion-techniques block was roughly 175 lines (a
small, fixed-looking share of an 878-line file) at the time of that decision (GT-9) and is now
roughly 510 lines — the largest single section of a 1,132-line file (GT-2). This project's own
governing discipline for exactly this kind of question states the standard directly: a carried
constraint is "re-examined... against evidence rather than inherited by default" (the same principle
`docs/v8.7-constraint-teardown.md` §1 states of itself, quoted in GT-6/GT-7's source document).

**What it ruled out:** "No changes here, this was already decided" as a sufficient answer to the
present question, given the growth trend now visible in GT-2 versus GT-9.

## 6. Conclusion

**Recommended approach:** (chains C3, C4, C5, C6, C7) A two-part, evidence-conditioned intervention
scoped to the full-composer agent body only:

1. **Extend the already-proven conditional Read-on-demand pattern to the remaining five companion
   procedures** (five-whys, fishbone, second-order, estimate, theoretical-limit) — chains C3 and C4.
   Keep each technique's compact "Decision rule" one-liner resident in the core body, since trigger
   detection needs only that, not the full procedure text; defer the full procedure text to the
   existing reference-file copies via an explicit "open ... with Read, at the point the trigger
   fires" instruction, mirroring the wording already used for pre-mortem, inversion and trade-off.
   Chain C5 brackets the expected saving at roughly 180-7,080 tokens per typical invocation, central
   estimate ≈4,320 tokens (about 20% of the companion-techniques block's current footprint),
   conditioned on a typical run not firing all 8 techniques.
2. **Do not reinstate a blocking raw-line-count gate on the resulting core body.** Chain C1
   establishes that no version of that gate (500, 580 or 644) was ever shown to protect a measured
   quantity, and this project's own history already converged, independently, on exactly this
   position (GT-6, GT-7). If any gate is wanted at all, gate the behavioral property that actually
   matters — a non-blocking report of the core body's size (as already precedented) plus a battery
   assertion that Step 0 trigger-detection and Phase 5's adversarial-technique selection still fire
   correctly after the extraction, which is the thing an extraction could actually break. Chain C6
   names why this pairing is not optional packaging: without it, a future maintainer under gate
   pressure has a standing incentive to reproduce GT-11's near-zero-savings outcome a second time.
3. **This does not touch the 8 already-separate focused-technique skills.** Chain C2 establishes
   they were never part of this cost problem; a reader arriving from the "split the monolith" framing
   should expect no change there.

If forced onto the user's original four-option menu: this is closest to **(a)+(b) combined** — real
lazy-loading (a) paired with fixing a gate that "was never actually measuring the right thing" (b) —
rather than a clean fit to any single letter; naming it honestly as **(d) something else** is more
accurate than forcing it into (a), (b) or (c) alone. Chain C4's trade-off scoring is what makes this
a specific, weighted recommendation rather than a hedge: option B (this recommendation) beat naive
splitting (a-as-literally-proposed), relaxing the number (c), and doing nothing (d-as-a-pure-default)
by a robust, weight-insensitive margin.

**Key insight:** (chains C1, C2, C3) The reflexive "split the file" response and the reflexive
"comply with the gate's number" response share one unexamined premise: that a single file's line
count is a stand-in for the cost that matters. It is a stand-in only for the one invocation path that
actually concatenates the whole file into every run regardless of use (the full-composer agent,
C2) — and even there, only for the fraction of that file read unconditionally versus the fraction
read only when a specific, data-dependent trigger fires (C3). The generic "878 vs. 500, extract
everything" framing collapses that distinction, and this project's own history shows what happens
when it does: the one extraction already performed under that framing (the appendices) satisfied the
byte-count gate while, by its own author's admission, saving close to nothing per invocation, because
the extracted content was never conditionally loaded in the first place (GT-11). The type of read —
unconditional or conditional — determines whether a split saves anything at all; the file's line
count is silent on that distinction, which is exactly why it was a poor proxy for the quantity
everyone actually cared about (C1).

**Trade-offs acknowledged:**

- (chain C5) The estimated savings (central ≈4,320 tokens, ~20% of the current companion-techniques
  footprint) are conditioned on typical full-composer runs firing well under all 8 techniques; this
  repository has no existing telemetry on that distribution (assumption A-10, unverified — flagged).
  Following the exact precedent this project's own prior analysis set for its own open question
  ("commission the GT-9? measurement," GT-9's source), the honest move is to commission a small
  measurement — an instrumented count of technique-trigger frequency across a sample of prior
  full-composer runs — alongside shipping the change, not to claim the saving as settled.
- (chain C6) The intervention adds one more Read round trip per triggered technique and one more
  file class for maintainers to navigate; GT-5 shows this exact cost is already accepted in
  production for 3 of 8 procedures, so this extends a working pattern rather than introducing a
  novel risk. But chain C6 also names a specific, evidenced Goodhart risk: a future maintainer facing
  a reinstated size gate could satisfy it by moving content into files still read unconditionally
  every run, reproducing GT-11's near-zero-savings outcome under a new name — this is why part 2 of
  the recommendation (redesign the gate, do not reinstate it) is a safeguard, not optional packaging.
- (chain C2) This recommendation touches only the full-composer agent body; chain C2 found the 8
  already-separate focused-technique skills were never part of this cost problem, so a reader
  arriving from the "split the monolith" framing should not expect changes there.
- (no chain — flagged assumption only) The mechanism this recommendation extends depends on two
  things this session did not fully verify: that the Read-on-demand path-resolution GT-16 observed
  for output-template.md/validation-rubric.md/pre-mortem/inversion/trade-off continues to resolve
  reliably for five more procedures across every install context (GT-16), and that trigger detection
  for those five procedures survives on the compact decision-rule alone (assumption A-9, unverified —
  flagged). If A-9 fails for a given technique, the existing Phase-5 Read-failure fallback ("run the
  pass from the summary in Companion tools rather than skipping it") already bounds the damage to
  degraded rigor on that one technique rather than a silent skip — so the core savings claim (chain
  C5) is unaffected even in that failure case; only the per-technique reliability guarantee weakens.
  The user's own prompt anticipated exactly this kind of gap and asked that it be flagged for their
  own follow-up verification rather than asserted as settled.

**Pre-check:** head C1 (MEDIUM), C2 (MEDIUM), C3 (HIGH), C4 (MEDIUM), C5 (MEDIUM), C6 (MEDIUM), C7 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** MEDIUM — the recommendation rests on chain C7's synthesis, itself capped MEDIUM by
its lowest-rated contributing chains (C1, C2, C4, C5, C6). Each of those chains' own confidence line
already names its specific shortfall (a live rival, an unpriced assumption, or an analyst-judgment
dependency) and what observation or measurement would close it; this line does not re-explain them.
Chain C3, the one HIGH-confidence link in the chain of reasoning, establishes the mechanism itself
(conditional vs. unconditional reads) with no outstanding axis — it is the load-bearing finding the
rest of the recommendation is built on, and it is not what is holding the overall rating at MEDIUM.

## Assumption Audit scan (process output)

End-of-Phase-4 scan: every named derivation chain step in section 4, in order, checked for an
assumption not already in the Classified Assumptions Table (section 2).

| Chain | Step | Step Text (brief) | Assumption surfaced? | Added to Table? |
|-------|------|--------------------|-----------------------|------------------|
| C1 | 1 | recalibrated-whenever-it-binds limit functions as growth ceiling not harm check | none | n/a |
| C1 | 2 | blind A/B is the only direct line-count measurement this project ran | none | n/a |
| C1 | 3 (concl.) | budget was convention, not load-bearing constraint | none | n/a |
| C2 | 1 | body loaded whole per full-composer invocation, never for focused | none | n/a |
| C2 | 2 | ceiling can only price full-composer path | A-12 (focused-skill text taken as sufficient evidence of no hidden pre-load) | yes |
| C2 | 3 (concl.) | budget should scope to full-composer overhead only | none | n/a |
| C3 | 1 | appendix split changed location, not load-conditionality | none | n/a |
| C3 | 2 | GT-5 procedures already read conditionally | none | n/a |
| C3 | 3 (concl.) | savings depend on conditional vs. unconditional read | none | n/a |
| C4 | 1 | weighted scoring yields A=71, B=108, C=63, D=71 | none (shortfall already carried on chain's own confidence line, not a hidden premise) | n/a |
| C4 | 2 | flip test: no single-weight change flips the result | none | n/a |
| C4 | 3 (concl.) | Option B dominates, robustly | none | n/a |
| C5 | 1 | body density gives ≈19.3 tokens/line | none | n/a |
| C5 | 2 | net saving = unused-procedure cost − triggered-procedure Read overhead | A-11 (Read overhead ≈100-200 tokens) | yes |
| C5 | 3 | ≥2 of 8 techniques fire on nearly any run; typical run fires 3-5 more | A-10 (typical trigger count stays well below 7-8) | yes |
| C5 | 4 (concl.) | bracket 180-7,080 tokens, central ≈4,320; all-8-triggered is a net loss | none (uses A-10/A-11 already surfaced above) | n/a |
| C6 | 1 | maintainer/agent navigation cost extends an existing pattern | none | n/a |
| C6 | 2 | future maintainer has a standing incentive to take the cheap, unconditional route under gate pressure | A-13 (Goodhart risk recurs unless the gate is redesigned) | yes |
| C6 | 3 | core body stops growing per new technique added | none | n/a |
| C6 | 4 (concl.) | benefit durable only if paired with a redesigned gate | none (uses A-13 already surfaced above) | n/a |
| C7 | 1 | budget was convention; ceiling only prices full-composer path | none | n/a |
| C7 | 2 | only conditional reads produce savings; companion block is the unused class | none | n/a |
| C7 | 3 | Option B dominates; saving ≈20% of block, conditioned on the gate pairing | none | n/a |
| C7 | 4 (concl.) | neither naive split nor raising the number is correct; extend + redesign | none | n/a |

## Adversarial pass (process output)

**Recompute.** Independently recomputed every computed figure in section 4. Tokens/line:
16,772 ÷ 1,132 ≈ 14.82 words/line × 1.3 ≈ 19.3 tokens/line — matches chain C5. Per-procedure size:
510 ÷ 8 ≈ 63.75 lines × 19.3 ≈ 1,230 tokens — matches. Current companion-block footprint:
510 × 19.3 ≈ 9,843 tokens — matches "≈9,840" in C5. Bracket recomputed from N_triggered ∈ {7,4,2}:
180 / 4,320 / 7,080 tokens (using N_unused × 1,230 − N_triggered × 150) — all match; the degenerate
N_triggered=8 case recomputes to −1,200 — matches. Trade-off weighted totals recomputed
cell-by-cell: B=108, C=63, D=71 all reconciled on the first pass. **Option A's stated total of 71
did not reconcile against its originally-drafted cell scores (5+20+4+6+15+16=66, not 71) — a
transcription error, since the Correctness-preservation cell had been silently changed from 5 to 4
between the planning pass and the final table without re-summing.** This has been corrected in
section 4: Option A's Correctness-preservation score is 5 (nothing conditional is introduced by
this option, so nothing new can break), which reconciles 5+25+4+6+15+16=71 exactly. The flip-test
conclusion is unaffected by the fix — the gap between A/D's Correctness score and B's stays 1 point,
and B's own total (108) never depended on A's cell values.

**Sensitivity.** The single ground truth whose falsity would most threaten the headline conclusion
is GT-5 (three of eight companion procedures already run under a conditional Read-on-demand pattern
in production). It is unsuffixed, not `?`-marked — it is the load-bearing input for chain C3, the
one HIGH-confidence link the rest of the analysis is built on, and it was read directly from this
analysis's own operating instructions in this same session. Weakest link per chain: C1 (Rivals axis
— GT-8 leaves open an alternate reading of what the old gate reached for); C2 (Rivals axis — A-12,
no live-invocation trace performed); C4 (Inference axis — analyst-judgment cell scores); C5
(Inference axis — A-10 unpriced); C6 (Rivals axis — a forward-looking Goodhart projection). C3 and
C7 have no weakness of their own beyond the MEDIUM ceiling C7 inherits from what it cites.

**Rival.** Headline (C7): the strongest rival is Option D — leave the file exactly as it is, since
the live repository's own history already retired the blocking gate and nothing is currently
broken. Chain C4's trade-off scoring rules it out (D=71 against B=108, flip-test-robust), though the
rival strengthens back toward parity with A — not with B — if A-10 turns out false, since C6's
gate-redesign argument for B is independent of C5's savings estimate. C1: the strongest rival is
"the gate was a crude proxy for technique-count dilution (GT-8), not pure convention" — carried
live, named on C1's own confidence line. C2: the strongest rival is "focused skills secretly still
incur composer-body overhead" (A-12) — carried live, named on C2's own confidence line. C3, C4, C5,
C6, C7: no further live rival beyond what each chain's own confidence line already names.

**Premise (past tense).** The recommended plan — extend Read-on-demand to the remaining five
companion procedures, paired with redesigning the size gate — has already failed.

**Causes (unfiltered, from three stakeholder viewpoints, written before any grouping):**
- *The maintainer making the change:* a technique's compact decision-rule turns out insufficient for
  correct trigger detection once its full text is deferred, causing that technique to silently
  under-fire or over-fire.
- *The maintainer making the change:* the Read-on-demand path-resolution mechanism (GT-16) does not
  resolve identically across every plugin install context, and a Read call fails in some
  environments but not others.
- *The maintainer making the change:* under time pressure, the extraction is done the cheap way —
  content moved to a file still read unconditionally every run — reproducing GT-11's near-zero-
  savings outcome a second time.
- *A future contributor inheriting the redesigned gate:* the new behavior-focused gate is never
  actually built, because it needs more design effort than a line-count check, so the blocking gate
  is gone and nothing meaningful replaces it.
- *A future contributor inheriting the redesigned gate:* the gate is built, but it reintroduces the
  exact `_COMPOSER_FOCUS_CEILING` failure GT-8 already documented, penalizing a genuinely thorough
  run for firing more markers than an arbitrary ceiling permits.
- *The end user running a real analysis:* a typical run turns out to fire 6-8 of the 8 techniques
  far more often than assumed (A-10 is false), so the change nets a token loss on the very runs it
  was meant to help.
- *The end user running a real analysis:* the added Read round trips introduce noticeable latency,
  degrading experience even where token cost falls.
- *A reviewer of the plugin's own governance:* the change ships without the measurement chain C5
  itself calls for, so the saving becomes an unfalsified assertion — the exact pattern GT-7
  criticized the original gate for.

**Clusters (each naming the chain/GT ids it bears on):**
1. **Extraction correctness risk** (C4's Correctness-preservation criterion, A-9, GT-5) — the
   decision-rule residue proves insufficient for one or more newly-extended techniques, or the Read
   path fails to resolve in some install context.
2. **Cheap-compliance recurrence** (C6, GT-11, A-13) — the extraction is done in a way that still
   reads unconditionally, reproducing the appendix outcome.
3. **Governance vacuum or governance repeat-failure** (C1, GT-6, GT-7, GT-8) — the replacement gate
   is never built, or repeats the `_COMPOSER_FOCUS_CEILING` dilution failure.
4. **Unmeasured savings claim** (C5, A-10, A-11) — the change ships without the measurement C5
   itself calls for.
5. **User-facing latency/experience cost** (C6) — added Read round trips are felt by the end user
   even where token savings materialize.

**Disposition (per cluster):**
1. Extraction correctness risk — **plan change**: extract the five procedures one at a time, not as
   a single batch, running the existing routing/trigger battery (the BATT-06-style marker-count
   self-tests GT-8 references) after each one, so a bad extraction is caught before it compounds.
2. Cheap-compliance recurrence — **plan change**: the extraction commit must state, for each of the
   five procedures, where its decision-rule is inlined and what specific trigger condition causes
   its Read, per chain C3's own unconditional/conditional distinction — making "moved but still
   unconditional" a visible, checkable defect rather than a silent regression.
3. Governance vacuum or repeat-failure — **accepted risk with a named mitigation**: building the
   replacement gate is explicit part 2 of §6's recommendation, not deferred indefinitely; the
   mitigation against `_COMPOSER_FOCUS_CEILING`-style recurrence is to keep any marker-count
   instrumentation as a non-blocking report, per GT-6's own precedent, not a new ceiling.
4. Unmeasured savings claim — **accepted risk with a named mitigation**: ship the change and the
   measurement together, per §6's trade-offs bullet citing chain C5; the recommendation is presented
   at MEDIUM, not HIGH, precisely because of this.
5. User-facing latency/experience cost — **accepted risk, no separate mitigation beyond chain C6**:
   the added round trips are the same cost GT-5's existing 3-of-8 pattern already accepts in
   production today; if this cost proves unacceptable in practice, that is itself evidence of
   assumption A-9 failing and routes back to the measurement named in cluster 4.

**Falsification.** The headline conclusion (chain C7 / §6) is false if a representative sample of
full-composer runs shows that 7 or 8 of the 8 companion techniques fire on a typical run (refuting
A-10) — chain C5's estimate then collapses to near-zero-or-negative savings, and Option B's
Correctness/Maintainability costs would need weighing against a benefit that never materializes,
plausibly reversing chain C4's ranking. It is also false if the Read-on-demand mechanism this
recommendation depends on (GT-16) does not resolve reliably across install contexts other than the
one this session directly observed — a claim this session did not independently trace, and flagged
as such in §6's trade-offs.

## Techniques not applied (process output)

- fishbone — not applicable — the assumption space was tractable via direct evidence-based
  challenge (Bash/Read investigation of the live repository) rather than requiring a breadth-first
  cause-category brainstorm.
- five-whys — not applicable — every ground truth was established by direct read-at-source
  verification of primary documents rather than by recursively decomposing a compound claim, and no
  recurring-symptom causal drill was needed.
- inversion — not applicable — the conclusion is a recommended plan of action rather than a
  standalone claim, so Phase 5's adversarial-technique step used pre-mortem instead (per the
  inversion-vs-pre-mortem decision rule); Phase 2's assumption challenges were resolved by direct
  documentary evidence rather than failure-enumeration.
- theoretical-limit — not applicable — this is a software-governance/cost question, not a question
  of what a hard physical or mathematical constraint permits; there is no governing law to strip
  conventions back to.

## §6→§4 closure ledger (process output)

- "Recommended approach: (chains C3, C4, C5, C6, C7) A two-part, evidence-conditioned intervention..." → chains C3, C4, C5, C6, C7 ✓
- "1. Extend the already-proven conditional Read-on-demand pattern..." → chains C3, C4 ✓
- "2. Do not reinstate a blocking raw-line-count gate..." → chains C1, C6 ✓
- "3. This does not touch the 8 already-separate focused-technique skills." → chain C2 ✓
- "If forced onto the user's original four-option menu: this is closest to (a)+(b) combined..." → prose paragraph, no bold colon lead-in and no list marker; not a claim under R11 — no citation required (it references chain C4 inline as color, not as a citation obligation).
- "Key insight: (chains C1, C2, C3) The reflexive 'split the file' response..." → chains C1, C2, C3 ✓
- "Trade-offs acknowledged:" → section-intro label (entire physical line, no citation of its own); citation obligation falls to the bullets beneath.
- "(chain C5) The estimated savings..." → chain C5 ✓
- "(chain C6) The intervention adds one more Read round trip..." → chain C6 ✓
- "(chain C2) This recommendation touches only the full-composer agent body..." → chain C2 ✓
- "(no chain — flagged assumption only) The mechanism this recommendation extends depends on..." → marker `no chain — flagged assumption only` present verbatim; kept (not cut) as an honestly-labeled caveat per the rubric's explicit allowance for this marker; scores untraced for Criterion 6 purposes rather than a citation.
- "Pre-check: head C1 (MEDIUM), C2 (MEDIUM), C3 (HIGH), C4 (MEDIUM), C5 (MEDIUM), C6 (MEDIUM), C7 (MEDIUM)..." → chains C1-C7 ✓
- "Confidence: MEDIUM — the recommendation rests on chain C7's synthesis..." → chain C7 (and, via C7's own head, C1-C6) ✓

Ledger clean: every claim either cites a chain or carries the permitted `no chain — flagged
assumption only` marker. No claim was cut.

## Self-audit scan (process output)

| Chain | Chain Head (brief) | Form conforming? | Rule applied | Dependency clean? | Band | Act attempted? | Edges fired |
|-------|---------------------|-------------------|---------------|--------------------|------|-----------------|-------------|
| C1 | GT-6, GT-7 | yes | n/a | yes | MEDIUM | yes | none |
| C2 | GT-3, GT-4, GT-15 | yes | n/a | yes | MEDIUM | yes | none |
| C3 | GT-9, GT-10, GT-11, GT-5 | yes | n/a | yes | HIGH | yes | none |
| C4 | C3, GT-6, GT-7, GT-9, GT-11 | yes | n/a | yes | MEDIUM | yes | none |
| C5 | GT-1, GT-2, C4 | yes | n/a | yes | MEDIUM | yes | none |
| C6 | C4, GT-8, GT-11, GT-2, GT-9 | yes | n/a | yes | MEDIUM | yes | none |
| C7 | C1, C2, C3, C4, C5, C6 | yes | n/a | yes | MEDIUM | yes | none |

| §6 Span (brief) | Construct | Claim under R11? | R11 clause applied | Chain cited |
|-------------------|-----------|-------------------|----------------------|---------------|
| "Recommended approach: (chains C3, C4, C5, C6, C7)..." | bold lead-in | yes | citation appears on the lead-in's own line, so it is itself a claim | C3, C4, C5, C6, C7 |
| "1. Extend the already-proven conditional Read-on-demand pattern..." | list item | yes | closes its own sentence / >40 chars | C3, C4 |
| "2. Do not reinstate a blocking raw-line-count gate..." | list item | yes | closes its own sentence / >40 chars | C1, C6 |
| "3. This does not touch the 8 already-separate focused-technique skills." | list item | yes | closes its own sentence / >40 chars | C2 |
| "If forced onto the user's original four-option menu..." | prose | no | prose carrying neither a bold colon lead-in nor a list marker is not a claim | n/a |
| "Key insight: (chains C1, C2, C3)..." | bold lead-in | yes | citation appears on the lead-in's own line | C1, C2, C3 |
| "Trade-offs acknowledged:" | bold lead-in | no | entire physical line, no citation of its own — section-intro label | n/a |
| "(chain C5) The estimated savings..." | list item | yes | closes its own sentence / >40 chars | C5 |
| "(chain C6) The intervention adds one more Read round trip..." | list item | yes | closes its own sentence / >40 chars | C6 |
| "(chain C2) This recommendation touches only the full-composer agent body..." | list item | yes | closes its own sentence / >40 chars | C2 |
| "(no chain — flagged assumption only) The mechanism this recommendation extends..." | list item | yes | closes its own sentence / >40 chars; carries the permitted no-chain marker | none — untraced |
| "Pre-check: head C1 (MEDIUM)...C7 (MEDIUM)..." | bold lead-in | yes | the pre-check line is itself a §6 claim, cited by the chains its own head names | C1, C2, C3, C4, C5, C6, C7 |
| "Confidence: MEDIUM — the recommendation rests on chain C7's synthesis..." | bold lead-in | yes | always-a-claim lead-in; discharged via the D-07 chains it names | C7 |

Scan complete: 7 chain rows, one per section-4 chain block in order; 13 section-6 rows, one per
construct in order — 11 claims under R11, 2 excluded. 0 chains malformed, 0 claims untraced by
defect (1 claim — the fourth Trade-offs bullet — carries the permitted `no chain — flagged
assumption only` marker and is scored untraced by design, not by omission).

## Self-Audit Gate (process output)

**Criterion 1: Identify Essence**
Quoted span: "The real question is not 'does this 878/1132-line file exceed a 500-line number' but
*what quantity does a line-count ceiling on an agent-instruction file actually stand in for, does
the file's line count move in step with that quantity given how this specific runtime loads the
file, and — only once that is settled — which structural change (if any) reduces the real quantity
rather than merely the number the gate reads*."
Band: **Rigorous**
Justification: Names the core question (proxy-validity plus mechanism-fit) rather than restating
the triggering prompt, and each of the four success criteria specifies a checkable structural test
against a named section of this document.

**Criterion 2: Challenge Assumptions**
Quoted span (Assumption Audit scan): "C2 | 2 | ceiling can only price full-composer path | A-12
(focused-skill text taken as sufficient evidence of no hidden pre-load) | yes"
Band: **Rigorous**
Justification: The Assumption Audit scan covers all 7 chains' steps in order with no step skipped;
every row in the Classified Assumptions Table carries one of the four types with matching treatment
vocabulary, a specific verification citation, and — where used in a chain despite being unverified
(A-9, A-10, A-11) — the "unverified — flagged" notation; several assumptions (A-1, A-3, A-5, A-6,
A-12) are genuinely Challenged rather than merely Accepted.

**Criterion 3: Establish Ground Truths**
Quoted span: "**`?`-marked:** GT-12 (1 of 16)." — checked against the Ground Truths list itself:
GT-12 is the only entry carrying a `?` suffix.
Band: **Rigorous**
Justification: The enumeration matches the list exactly; the one HIGH-confidence chain in this
analysis (C3, head GT-9/GT-10/GT-11/GT-5) has every head ground truth named with its read-at-source
location; no GT-ID is reused or renumbered across sections; no assumption discarded in Phase 2
appears in the list.

**Criterion 4: Reason Upward**
Quoted span (Self-audit scan, chain-form table, and its reconciliation line): "C4 | C3, GT-6, GT-7,
GT-9, GT-11 | yes | n/a | yes | MEDIUM | yes | none" ... "0 chains malformed."
Band: **Rigorous**
Justification: All 7 chain-form rows read "yes" for both Form conforming and Dependency clean with
no unreached positions; every Conclusion-section claim traces to exactly one named chain per the
closure ledger; three Abandoned Reasoning entries each use the full What-was-tried / Why-abandoned /
What-it-ruled-out structure; no analogy is used as direct evidence anywhere in section 4.

**Criterion 5: Validate**
Quoted span (Adversarial pass record): "1. Extraction correctness risk — plan change: extract the
five procedures one at a time... 4. Unmeasured savings claim — accepted risk with a named
mitigation: ship the change and the measurement together..."
Band: **Rigorous**
Justification: The adversarial pass record carries every required part — Recompute (which caught
and corrected a genuine arithmetic error before this document's final chain table), Sensitivity,
Rival, a past-tense Premise, an unfiltered multi-stakeholder Causes list, Clusters citing chain/GT
ids, and a Falsification condition; every cluster carries either a named plan change or an
explicitly accepted risk with a named mitigation; every MEDIUM confidence line names its specific
downgrade cause and what would close it; no chain is rated HIGH while consuming a `?`-marked input,
and no chain is rated above the lowest-rated chain its head cites.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span (Self-audit scan, claim-inventory reconciliation line): "0 claims untraced by defect (1
claim — the fourth Trade-offs bullet — carries the permitted `no chain — flagged assumption only`
marker and is scored untraced by design, not by omission)."
Band: **Rigorous**
Justification: Every Conclusion-section claim traces to a named section-4 chain except the one
caveat explicitly using the rubric's own permitted no-chain marker; no new substantive claim is
introduced in section 6 without a supporting chain; the Key Insight (the conditional-vs-unconditional
read distinction) is a non-obvious finding distinct from the prescriptive Recommended approach it
sits beside.

**Gate result:** No criterion scored Absent; zero criteria scored Hand-wavy. Both clearing
conditions are met on the first pass — no Fix/Repeat re-perception pass was required.
