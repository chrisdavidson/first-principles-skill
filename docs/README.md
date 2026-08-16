# docs/ — Documentation Index

> **Retrieving removed documents.** On 2026-08-16 this directory was pruned of 34 historical
> milestone documents — per-milestone verdicts, protocols, findings, and superseded plans whose
> conclusions are already carried by the prose in this index, by `requirements-traceability.md`,
> and by the annotated release tags. Nothing was lost: every removed file remains in git history.
> Document names appearing in `backticks` rather than as links throughout this index refer to
> those files. Retrieve one with:
>
> ```sh
> git log --diff-filter=D --name-only -- 'docs/*.md'   # find the removing commit
> git show v8.7:docs/v8.7-correctness-spot-check.md    # read any file at its milestone tag
> ```
>
> The gate-load-bearing documents (`live-monitoring-runbook.md`, `gen-01-rearch-milestone.md`),
> the standing governing records, and all current-state developer docs were kept.

> **Current state — start here:** [`requirements-traceability.md`](requirements-traceability.md)
> — the authoritative surface: active residuals, dispositions, and the **current** coverage
> headline of **126 reproducible / 88 audit-only / 0 gap / 214 total**.
>
> **Historical terminal record:** [`v8.0-final-closure.md`](v8.0-final-closure.md) — accepted
> limitations, deferred-ledger disposition, and the v8.0 coverage headline of 133/96/0/229. That
> document calls its figure "final" because v8.0 was intended to wrap the project; work continued,
> and the headline has moved twice since (133/96 → 132/97 at the v8.8 post-close re-tier, then
> → 126/88 when 15 builder requirements were retired, taking the row count 229 → 214). Read it as
> a record of where v8.0 stood, not as the current state.
>
> Later milestones v8.1 (a Grok-review triage that selectively implemented 7 docs/metadata items), v8.2 (a fresh analysis-only re-investigation of the 19 not-approved items), v8.3 (a technique-overlap + context-optimization evaluation, findings-only, byte-freeze untouched), and v8.4 (an implementation-readiness evaluation that returned a GO verdict on the GROK-04 hero banner — specified and costed but not built in that milestone — and a NO-GO on reference-file extraction) left this terminal baseline unchanged.

> **GROK-04 disposition (final, 2026-07-24):** the hero banner was subsequently built and embedded at v8.5 (Phase 153), then **removed entirely** by explicit user decision — asset, embed, and the standing landing-page-placement question all dropped. The v8.2/v8.4 documents are the frozen record of the decisions made at the time; they were never rewritten, and were removed from the working tree in the 2026-08-16 docs prune (see **Retrieving removed documents** below).

Milestone v8.5 (Context Optimization — Execute the Reference-File Split) is the first implementation + live milestone since v8.1: it executed the 4-file reference split (five-whys, theoretical-limit, estimate, fishbone into core + on-demand `-detail.md` siblings, dropping 398 lines off the skill surface) and ran the milestone's only live spend — a 72-call re-measure — narrowly relaxing the byte-freeze to re-open and re-measure exactly RR-108-04/RR-108-05, unlike the v8.2–v8.4 analysis-only milestones. The detector constants stayed byte-unchanged and the coverage headline stayed 133/96/0/229.

Milestone v8.6 (Agent-Body Procedure Compression) is the second consecutive live-measure milestone: it compressed the always-loaded, auto-routed agent body's inlined `## Procedure` prose for four techniques — estimate and theoretical-limit (no emission detector, zero measured-floor risk) and five-whys and fishbone (marker-pinned) — cutting the agent body 612 to 590 lines, the surface v8.5's reference-file split structurally could not shrink, since the agent body inlines only `## Procedure`. It then ran a small 2-row live Step-0 re-measure confirming neither compressed detector-covered row regressed (fishbone 3/5 to 4/5, five-whys 0/5 to 2/5 unbanked). The detector constants and the coverage headline stayed unchanged (133/96/0/229).

Milestone v8.7 (Analysis Correctness, Constraint Teardown & Output-Contract Integrity) breaks the pattern of every milestone since v8.1 — its scope traces to a v8.6 post-hoc finding and a fresh constraint audit, not to the prior milestone's own optimization paperwork, and for the first time in 161 phases an instrument asked whether the agent's analyses are actually *correct* rather than merely well-formed. The correctness spot-check (Phase 162) re-derived 65 load-bearing claims across six frozen analyses — 47 correct / 6 wrong / 12 unverifiable, zero material errors, milestone proceeds — but surfaced the more consequential finding: rubric conformance does not predict arithmetic correctness (the most accurate document failed the rubric; the least accurate passed). Constraint teardown (Phase 163) then retired five carried constraints on that evidence: the 644-line body-budget gate, the `_COMPOSER_FOCUS_CEILING=4` freeze, K-of-5 Step 0 as a phase gate, the blanket gitignored-planning posture, and the `phases.clear`-stays-OFF workaround. Harness promotion (Phase 164) turned the throwaway blind A/B rig into a permanent, self-testing `scripts/check-quality-harness.py` instrument (`QUAL-01`, battery 15 to 16) and froze a pre-fix quality baseline as committed evidence. The output-contract fix (Phase 165) then landed chain-form conversion, a §6→§4 closure check, and a Verdict-token prefix format — five behavior-changing consistency fixes, shipped without a live re-measure of Step 0 or routing (an explicitly accepted caveat). The post-fix blind re-measure (Phase 166) returned an honest **MIXED** verdict: the untraced-defect incidence held flat at 6/6, chain-defect incidence improved 6/6 to 4/6, and the aggregate +9 band delta shrank to roughly +3 once drift noise was controlled for — the real signal is the chain-rigor improvement, not the aggregate. Closure reconcile (Phase 167) indexes these four documents, brings `CLAUDE.md` and `docs/TESTING.md` to the same terminal shape every prior milestone reached, and stages the honest-MIXED `v8.7` tag message — and folds in the seven deferred Phase-165 code-review fixes (five of them behavior-changing), applied *after* the Phase-166 measurement above and deliberately not re-measured, so the shipped v8.7 contract differs from the one that verdict measured (stated plainly, honesty-not-score — the before/after of those five fixes is left to a future self-measuring follow-up).

> **Correction (v8.13 DETECT-05, 2026-07-27; pointer added 2026-08-07).** The two defect-incidence figures in the Phase-166 sentence above were produced by a detector corrected *after* this paragraph was written, and both reverse under the corrected detector: `untraced` did **not** hold flat — it improved 6/6 → 4/6 — and `chain` did **not** improve 6/6 → 4/6 — it **worsened** 5/6 → 6/6. So "the real signal is the chain-rigor improvement" is refuted (the sweep's own §8 Reasoning-test reads REFUTED). The **+9 → +3 aggregate is unaffected** — it derives from the band scorelines, which DETECT-05 never touched. The full per-axis correction, its cause (FIX-CONTRACT-01, shipped 2026-07-24), and reproducibility live in the correction blocks of `v8.7-post-fix-remeasure.md`; the `untraced` mention is separately dispositioned out-of-scope in `tests/detect05-blast-radius-sweep-v8.13.md`.

Milestone v8.9 (DIAGNOSE-01) is the first `docs/`-shipping milestone since v8.7 — the intervening v8.8 was a doc-only technical-debt and framing-correction milestone that added no new `docs/` file — and it diagnoses, rather than fixes, why v8.7's §6→§4 output-contract fix left the untraced-defect incidence flat at 6/6: a pre-registered blind hand-read of all six frozen post-fix analyses, reconciled against the machine detector, found the flat flag is driven by three isolated `scripts/check-quality-harness.py` extraction limitations, not an agent-reasoning gap — adopted verdict **MEASUREMENT** (6/6), with the fragility disclosed directly alongside it: the verdict rides on one post-hoc claim-scoping reading and flips to **MECHANISM** (5/6) under the alternate every-extracted-sentence reading. The recommendation is costed for a future FIX-CONTRACT-01 offline detector fix (no prompt re-attempt — the lever is the detector, not the prompt); the detector constants and the coverage headline stayed byte-unchanged (132/97/0/229, the value since v8.8's post-close re-tier).

Milestone v8.10 (CORRECTGATE-01) validated FIX-CONTRACT-01 out-of-sample on six fresh problems and found it **DIVERGES**: under the `declarative-only` reading the aggregate is measurement-signal (4/6, FIX-CONTRACT-01 **stands**), while under the `every-extracted-sentence` reading it is mechanism-signal (5/6, FIX-CONTRACT-01 **must-revisit**) — and `Q-N4` is untraced under **both** readings, independent of the reading fork (its §6 conclusion never cites a chain id, only assumption-table ids). Only from that measured DIVERGE does the milestone then *design* — not build — a correctness instrument: a support-adequacy triad (present ∧ valid ∧ non-vacuous) that resolves the reading fork by defining the load-bearing claim itself, plus a committed acceptance/falsification fixture manifest (50%-arithmetic doc → FAIL, 100%-arithmetic doc → PASS, META-Q4 vacuous-green → FLAG, `Q-N4` → FAIL, the other five fresh documents → PASS). Building and wiring that instrument into the offline battery is the named out-of-scope downstream successor, **`CGATE-BUILD-01`**. The coverage headline stayed 132/97/0/229 and byte-freeze held.

Milestone v8.11 (DEFROBUST-01) tested whether v8.10's D-03 load-bearing-claim definition actually *dissolves* the `Q-N2`/`Q-N3`/`Q-N6` reading fork, as the v8.10 design claimed, or merely *relocates* it — and found it **DIVERGES**: two independent, mutually-blind reads applying the identical pre-registered D-03 rule to the same four documents (`Q-N2`, `Q-N3`, `Q-N4`, `Q-N6`) reproduced near-identical load-bearing-claim denominators (`Q-N2` 10/10, `Q-N3` 7/8, `Q-N4` 8/8, `Q-N6` 6/6) but reached different traced/untraced verdicts on 2 of 4 documents (`Q-N2` and `Q-N6`: read-A PARTIAL vs. read-B TRACED), while `Q-N3` and `Q-N4` agreed. The D-03 definition did not relocate the fork into *which* claims count — it relocated it one level deeper, into how directly a load-bearing claim's own number must be derived before it counts as traced. Per the pre-registered gate (agreement required on all four documents), **`CGATE-BUILD-01`** (building and wiring the designed correctness instrument into the offline battery) is **WON'T-DO** — the DIVERGE line closed as **characterized-but-not-closable**, with no successor build milestone scoped — and per honesty-not-score, that divergence is the test succeeding at exactly what it was built to do, not a failure to chase to agreement. The coverage headline stayed 132/97/0/229 (no matrix rows added) and byte-freeze held.

Milestone v8.12 (REALREAD-01) took the first read of first-principles analyses produced on real external work and never previously read back, and found the untraced-conclusions defect **is present** in that real output — 10 / 10 over the codeable subset, 10 / 11 over the fixed eleven-document denominator — **and** the re-coded control puts it at 9 / 12, so the attribution is **PRE-EXISTING**, not real-use-specific. The companion section-role census returned **NOT-WELL-FORMED**, ground **RENUMBERING** (real corpus `k`/`L` 3 / 10 against the control's own 8 / 12, attribution again **PRE-EXISTING**) — the measurement harness itself renumbers more than real work does. A further, unreconciled-by-design finding: the re-coded control's post-fix subset came out 4 / 6 untraced where the historical frozen detector reported 6 / 6 on the same documents, so measured incidence depends materially on the instrument that measured it. This is the first milestone in the project's history whose evidence is **not reader-auditable** — the corpus is client work and stays outside git, so this paragraph and `v8.12-findings.md` carry the aggregates a reader can check, not the underlying rows. The coverage headline stayed 132 / 97 / 0 / 229 with no matrix rows added, and byte-freeze held.

**Post-v8.11 state (2026-07-24) — PAUSED, and the gate on any next milestone.** With the DIVERGE line closed and no successor scoped, there is no open measured defect and therefore no legitimate scope source for a v8.12. The 2026-07-24 altitude check also examined usage for the first time. Measured over a single 30-day window, the **5-phase composer is the surface with real use** — 19 agent dispatches, 12 of them in external work projects on actual problems — while the focused technique skills were slash-invoked **zero** times in that window; their large lifetime counters (`pre-mortem` 125, `inversion` 38) last incremented on the v8.5/v8.6 live re-measure dates and are best read as harness activity. (An earlier version of this paragraph claimed the reverse; it compared a lifetime counter against a 30-day count and missed that the composer is dispatched through the Agent tool. Corrected 2026-07-24.) So the five milestones v8.7–v8.11 spent instrumenting the composer were aimed at the right surface after all. The only admissible scope source from here is [use-journal.md](use-journal.md): about five entries of real, non-harness use, then a read-back. If disappointment does not cluster, v8.11 is the terminal state. Scope may not be opened from prior milestone paperwork, from an altitude check, or from evidence about the measurement apparatus — all three are exhausted. **Disposition, as of 2026-07-25:** that gate is satisfied on the **evidence limb** only — v8.12 (REALREAD-01) opens on 13 first-principles analyses produced on real external work and never read, an evidence class this project has never collected and therefore sourced from none of the three exhausted channels above; the altitude check named the question, it did not supply the evidence. The **use-journal limb** remains open and unsubstituted: `use-journal.md` still needs about five live entries and its own read-back, and v8.12 repairs its capture path rather than standing in for it. The cost is stated rather than glossed: v8.12 is the first milestone whose evidence a reader cannot audit — the corpus is client work, it stays outside git, and the findings will be published as codings by label only. **Disposition, as of 2026-07-26:** the **evidence limb is now spent** — the corpus has been read, once, and its finding recorded in `v8.12-findings.md`. The **use-journal limb remains open and unsubstituted**: `use-journal.md` still needs about five live entries and its own read-back, with the CLOSE-03 run-count denominator guard in force, and nothing has been built to drive that use. **No successor is scoped** — a fix, if one is ever pursued, needs its own trigger and its own pre-registered success criterion, and the **PRE-EXISTING** attribution above means this evidence does not by itself establish that a fix is warranted. **Disposition, as of 2026-07-29 (after v8.14 closed):** the **delivery limb v8.14 rode in on is now spent too** — the path from repository to installed session has been measured on both of its mechanisms and found working, so it cannot admit another milestone. Of the gate's three limbs, two (evidence, delivery) are spent by construction and only the **use-journal limb** is live; it holds **one** entry and nothing has been built to drive that use. The gate now reads, in full: (a) **it binds quick tasks, not only milestones** — the three quick tasks of 2026-07-28 (`260728-pa2`, `260728-vxn`, `260728-wdi`) were all apparatus-and-paperwork-sourced and would have been barred at milestone scale, so a lighter command must not route around the bar; a quick task may do reversible hygiene (deletions proven dead, count reconciliation, release mechanics) but may not produce new instruments, new methodologies, or new findings documents without a use-journal entry or a real-output trigger. (b) **No standing residual may be its own trigger** — not the three D-18 residuals, not `WR-01`, not any successor: a residual recorded as accepted or characterized-but-not-closable is a *record*, not a scope source, and citing one as the trigger for any future milestone is barred absent a use-journal entry or a real-output finding.

**`GREENMEAN-01`'s battery-integrity scope is `WON'T-DO`** (2026-07-29). The three stopped phases' question — does a GREEN battery assert anything a user experiences — is **unanswered**, and it is closed as won't-do rather than held as a re-admittable candidate. The reason is admissibility, not disinterest: v8.14 was built expressly to find an anchor for it, measured the one anchor it had, and found the premise too broad; the scope is otherwise apparatus-about-apparatus, which the gate above bars standing alone. Holding it warm as "re-admit on a fresh anchor" is the standing-backlog posture the v8.0 decision row exists to prevent. Recorded so the closure is read as *barred, not unnoticed*: the class it would have hunted has **four** measured instances — QUAL-01's self-test pinning the broken behaviour it was built to catch (v8.13); `main.py`'s three dedicated test files collecting **0 items each** for two years (`260728-pa2`); sixteen green gates over a version stamp that left the *update* path inert (v8.14 / DELIV-01); and, fourth, produced by v8.14's **own milestone audit**, a check that ran `git show HEAD:.planning/REQUIREMENTS.md` against a **gitignored** path, compared 6 live rows to 0 baseline rows and printed a pass. That fourth instance is the sharpest statement of the bind and it is left standing on the record: the failure class this project is best at finding is the one its own scope gate forbids it to work on.

Milestone v8.14 (GREENMEAN-01) opened on the delivery limb — on the milestone-open belief that
v8.13's launcher had sat undeliverable to every install for two days while 16 gates stayed green —
and Phase 188 measured that premise rather than inheriting it, finding it too broad. As two
separate facts: a fresh install reaches `8.14.0` cleanly (DELIVERED), and an existing older install
also receives `8.14.0` cleanly through the update path (DELIVERED). Applying the wave-1
pre-registered mapping to that finding reaches **STOP** for Phases 189-191, published in full in
[v8.14-delivery-verification.md](v8.14-delivery-verification.md).

This folder documents the first-principles plugin system. New here? Start with [GETTING-STARTED.md](GETTING-STARTED.md), then [ONBOARDING.md](ONBOARDING.md), then [DATA-FLOW.md](DATA-FLOW.md).

---

## Milestone-close rules

**Version-stamp rule.** Any change under `first-principles/` requires the version stamp in
`first-principles/.claude-plugin/plugin.json` to advance before the milestone is closed. Plugin
installs are version-gated, not content-gated — `claude plugin marketplace update` and
`claude plugin update` compare version strings, so an edit shipped without a bump never reaches an
already-installed session. This is a **rule, not a gate**: nothing checks it automatically, no
script enforces it, and the offline battery is deliberately not grown to check it — the
milestone's build bar is measure plus rules only. See [DEVELOPMENT.md](DEVELOPMENT.md) for the
mechanism's full detail and its 2026-07-27 empirical note.

## Standing of the nine milestone documents

Adjudicated 2026-08-16 (audit stream 3, S-7). These nine were the only per-milestone documents to
survive the prune, and they were surviving as an undifferentiated block: nothing distinguished a
rule still in force from a measurement true only of its date. Each now carries its verdict as a
banner **in the document itself**, because the one failure this closes — `v8.0-final-closure.md`
asserting a "final" coverage headline that had moved twice — survived precisely because the
warning lived in `CLAUDE.md` and not in the document a reader opens.

Three classes, and no deletions: adjudication was the deliverable, and every one of the nine
earned its keep on a distinct ground.

| Document | Standing | Why it is kept |
|---|---|---|
| [v8.7-constraint-teardown.md](v8.7-constraint-teardown.md) | **Governing record** | TEARDOWN-01/02/03 and the K-of-5 demotion are in force; 16 surfaces cite it, including both pre-commit hooks and a string `check-body-budget.py` prints at runtime |
| [v8.5-byte-freeze-relaxation.md](v8.5-byte-freeze-relaxation.md) | **Governing record** | The relaxation still scopes which reference files may split; `sync-content.py` and `check-step0-live.py` cite it as the authority |
| [v8.14-delivery-verification.md](v8.14-delivery-verification.md) | **Governing record** | The published form of the pre-registered STOP governing Phases 189–191 and GREENMEAN-01's WON'T-DO. One inbound reference; inbound count is the wrong test |
| [v8.0-final-closure.md](v8.0-final-closure.md) | **Split** — governing / superseded | Its terminal ACCEPTED-FINAL dispositions still stand; **every count in it is superseded** (133/96/0/229 → 126/88/0/214; battery 15/15 → 17/17) |
| [gen-01-rearch-milestone.md](gen-01-rearch-milestone.md) | **Gate-pinned artifact** | The only one of the nine whose file a gate resolves: TRACE-03 fixture (9) deep-resolves it, proven by removal |
| [whole-system-remeasure-verdict.md](whole-system-remeasure-verdict.md) | **Frozen evidence** | Provenance anchor for 13 live matrix rows' dispositions |
| [v8.7-quality-baseline-freeze.md](v8.7-quality-baseline-freeze.md) | **Frozen evidence** (live baseline) | Provenance for QUAL-01 and the committed `tests/quality-baseline-v8.7*` the harness still reads. Carries inline DETECT-05 corrections — read them before quoting a figure |
| [v8.6-quality-ab-experiment.md](v8.6-quality-ab-experiment.md) | **Frozen evidence** | The source experiment the QUAL-01 instrument was promoted from; still the record of the four reproducible output-contract defects |
| [v8.6-live-remeasure-verdict.md](v8.6-live-remeasure-verdict.md) | **Frozen evidence** | Records the S-P04 2/5 → 0/5 → 2/5 swing that is the evidence behind the K-of-5 demotion |

**How to read the classes.** A *governing record* states a decision still in force — cite it,
do not restate its rules on another surface. *Frozen evidence* is a measurement: true of its
recorded date and of nothing later, kept because live artifacts cite it for provenance. A
*gate-pinned artifact* may be either, plus a file whose absence fails a gate.

**What the adjudication turned on.** Not inbound-reference counts. This audit's §3 already got
"pinned" wrong twice by reading greps instead of resolving fields, so each claim was checked at
the field level (`artifact_link` is deep-resolved; `deliverable_path` is not) and settled by
removing the file and running the gates. Note the confound that had to be cleared first:
**removing any of the nine fails VAL-03**, because this index links all nine — that measures the
index, not the document, and the prune convention above (demote the link to backticks) clears it.
The narrower question, *does a gate resolve the file itself?*, is yes for exactly one.

## Core docs

| Document | What it covers |
|----------|----------------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | System architecture: `shared/` → generation pipeline, plugin layout, five-phase agent methodology, measurement subsystem, CI + pre-commit gate table |
| [CONFIGURATION.md](CONFIGURATION.md) | Skill frontmatter rules, version-string format, reserved words, anti-masking invariants (`MIN_HEADER_HITS=2`, `_COMPOSER_FOCUS_CEILING=4`) |
| [DEVELOPMENT.md](DEVELOPMENT.md) | Contributor workflow: `shared/` source-of-truth model, validation-script inventory, standard editing loop, pre-commit hook setup, key invariants |
| [FIVE-PHASE-FLOW.md](FIVE-PHASE-FLOW.md) | Mermaid flow diagram of the 5-phase methodology: Step 0 mode selection, phase chain with named artifacts, companion-technique handoff edges, and the second-order route-back |
| [GETTING-STARTED.md](GETTING-STARTED.md) | Install the plugin, invoke the agent and the fourteen slash-invocable skills (thirteen companions plus the launcher) |
| [METHODOLOGY-CHEATSHEET.md](METHODOLOGY-CHEATSHEET.md) | One-page quick reference: the 5-phase flow, named artifacts, assumption types, derivation-chain format, and all thirteen companion/focused skills with slash commands |
| [TESTING.md](TESTING.md) | How to run every CI gate and the two pre-commit gates — VAL/DUAL/GATE/STEP0/BATT/TRACE matrix, each mapped to its script |
| [testing-agents-headlessly.md](testing-agents-headlessly.md) | Headless testing: routing battery, two-layer Step 0 harness, `stream-json` capture |

## System-connection docs

| Document | What it covers |
|----------|----------------|
| [DATA-FLOW.md](DATA-FLOW.md) | End-to-end trace: `shared/` source edit → `sync-content.py` → generated plugin → CI gates → measurement harness |
| [MEASUREMENT-MAP.md](MEASUREMENT-MAP.md) | Layered test stack: routing battery ↔ Step 0 emulator ↔ Step 0 live ↔ traceability matrix ↔ BATT-06 sentinels; which gate owns which residual |
| [COMPONENT-DIAGRAM.md](COMPONENT-DIAGRAM.md) | Mermaid diagrams of the generation pipeline and measurement stack — what reads what, what generates what |
| [ONBOARDING.md](ONBOARDING.md) | Contributor on-ramp: end-to-end "make a change" walkthrough from `shared/` edit to shipped, gated plugin artifact |

## Requirements & traceability

| Document | What it covers |
|----------|----------------|
| [v8.0-final-closure.md](v8.0-final-closure.md) | The v8.0 terminal ACCEPTED-FINAL dispositions and deferred-ledger summary. **Its counts are superseded** — see its Standing banner and the table above |
| [requirements-traceability.md](requirements-traceability.md) | Authoritative requirements traceability surface: active residuals, coverage headline, compact historical ledger, gap findings |
| [requirements-matrix.md](requirements-matrix.md) | Generated 214-row capability → requirement → test matrix |

## v8.5 — Context optimization (reference-file split)

| Document | What it covers |
|----------|----------------|
| [v8.5-byte-freeze-relaxation.md](v8.5-byte-freeze-relaxation.md) | Governing record narrowly re-opening RR-108-04/RR-108-05's re-measure disposition + the 4 split files' content; all other frozen constants keep gating. |

## v8.6 — Agent-body procedure compression

| Document | What it covers |
|----------|----------------|
| [v8.6-live-remeasure-verdict.md](v8.6-live-remeasure-verdict.md) | Live 2-row Step-0 re-measure honest verdict (MEASURE-01/02) — S-P03 fishbone 4/5 SUSTAINED (+1), S-P04 five-whys 2/5 SUSTAINED (+2, unbanked), D-05 fired-set / composer-ceiling provenance trace, RR-117-01 re-point to `_load_excerpt_v86`. |
| [v8.6-quality-ab-experiment.md](v8.6-quality-ab-experiment.md) | Post-hoc blind A/B of analysis *quality* at 590 vs 612 body lines, scored by 6 independent blinded judges against the validation rubric — no detectable difference (both arms 2/3 PASS, band total 35/35); failures track the problem, not the arm. Also reports the rubric's 2-level effective range and four reproducible output-contract defects. |

## v8.7 — Analysis correctness, constraint teardown & output-contract integrity

| Document | What it covers |
|----------|----------------|
| [v8.7-constraint-teardown.md](v8.7-constraint-teardown.md) | Standing governing record (TEARDOWN-01/02/03) retiring five carried constraints — the body-budget gate, the `_COMPOSER_FOCUS_CEILING=4` freeze, K-of-5 Step 0 as a phase gate, the blanket gitignored-planning posture, and the `phases.clear`-stays-OFF workaround — against the four that survived the audit. |
| [v8.7-quality-baseline-freeze.md](v8.7-quality-baseline-freeze.md) | Phase 164 write-up (HARNESS-01): promotes the blind A/B rig to the permanent, self-testing `scripts/check-quality-harness.py` instrument (`QUAL-01`, battery 15→16) and freezes the pre-fix quality baseline as committed evidence. |

## v8.11 — DEFROBUST-01

| Document | What it covers |
|----------|----------------|
| [tests/defrobust-v8.11/](../tests/defrobust-v8.11/) | The frozen read-input plus both mutually-blind captures and their provenance (`manifest.tsv`, `read-input.md`, `reads/`, `README.md`). |

## v8.14 — GREENMEAN-01

| Document | What it covers |
|----------|----------------|
| [v8.14-delivery-verification.md](v8.14-delivery-verification.md) | 2026-07-29. Phase 188 — the pre-registered continuation-decision rule and DELIV-02 outcome table (both committed before their evidence), the per-path DELIV-01 delivery verdict (fresh install and update path stated side by side, deliberately not collapsed), the second-date `RUNTIME-WIDE` re-observation result, and the dated continuation decision. **Outcome:** the fresh install path is DELIVERED and, as a separate fact, the update path is also DELIVERED; applying the pre-registered mapping to that finding reaches **STOP** for Phases 189-191. |

## Reference & history

| Document | What it covers |
|----------|----------------|
| [audit-2026-08-16-duplication-staleness.md](audit-2026-08-16-duplication-staleness.md) | Repo-wide audit of capability duplication and stale information: what is duplicated where, what is out of date, which `tests/**` artifacts any gate actually reads, and a per-stream remediation estimate with running status |
| [gen-01-rearch-milestone.md](gen-01-rearch-milestone.md) | ADR: the GEN-01 rearchitecture milestone record |
| [live-monitoring-runbook.md](live-monitoring-runbook.md) | Runbook for live routing-battery and Step 0 monitoring runs |
| [whole-system-remeasure-verdict.md](whole-system-remeasure-verdict.md) | v7.11 whole-system live re-measure and honest verdict; referenced by 13 rows of the traceability matrix |
| [use-journal.md](use-journal.md) | Running log of real (non-harness) invocations and where they fell short — the only admissible scope source for a post-v8.11 milestone |
| `history/` (local-only) | Frozen per-milestone snapshots (REQUIREMENTS, ROADMAP, MILESTONE-AUDIT) — immutable archives. **Not published:** `docs/history/` is git-ignored and untracked, so it is absent from a fresh clone and this entry is deliberately not a link. Same disclosure as [requirements-traceability.md](requirements-traceability.md). |
