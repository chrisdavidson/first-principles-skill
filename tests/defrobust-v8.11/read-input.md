# Blind Read Task — Apply a Pre-Registered Rule to Four Analyses

You are a careful, neutral reader. Your only task is to apply the **pre-registered rule** stated in
the "PRE-REGISTRATION PROTOCOL" section below to the **four documents** (`Q-N2`, `Q-N3`, `Q-N4`,
`Q-N6`) provided after it.

Consult **nothing** beyond (a) the rule in the protocol below and (b) the four documents themselves.
Do not draw on any outside knowledge of what a "correct" or "expected" answer should be — there is no
expected answer. Apply the rule mechanically to what each document actually contains. Each of the four
documents is a first-principles analysis carrying numbered sections (roughly §1–§6): §4 holds the
derivation chains / ground truths, and the final section (≈§6) holds the conclusion.

For **each** of the four documents, in turn, produce exactly the following, and nothing else:

1. **Load-bearing-claim set** — the set of paragraph/bullet-level claims in that document that are
   load-bearing under the protocol's include/exclude rule (Rule 1). **Quote each such claim verbatim**
   from that document. If the set is empty under the rule, say so explicitly.
2. **Traced / untraced marks** — for each load-bearing claim, mark it **traced** or **untraced**,
   citing the specific §4 derivation chain / ground truth **in that same document** that supports it,
   or noting the absence of any such support.
3. **Document verdict** — exactly one of **TRACED**, **UNTRACED**, or **PARTIAL**, applying the
   protocol's definitions (including the empty-denominator rule: a document whose load-bearing-claim
   set is empty is vacuously **TRACED**).

Address all four documents. Clearly label each document's section by its ID (`Q-N2`, `Q-N3`, `Q-N4`,
`Q-N6`). Work only from the rule and the four documents that follow.

═══════════════════════════════════════════════════════════════════════════════
PRE-REGISTRATION PROTOCOL (apply this rule; do not treat it as a document to classify)
═══════════════════════════════════════════════════════════════════════════════
# v8.11 — DEFROBUST-01 Definition-Robustness Test Pre-Registration Protocol

**This document is pre-registered and immutable.** It is authored and committed alone, in its own
dedicated commit — the pre-registration anchor — strictly **before** either of the two blind read
passes named below is generated, captured, or opened. Once committed, this protocol is never edited
to match a later read's finding. Any amendment discovered necessary after a read begins is recorded
as a new, dated addendum appended below the original text, never as a silent rewrite of the rules
that follow — the same discipline `docs/v8.10-fix-contract-oos-protocol.md` and
`docs/v8.9-diagnose-contract-fix.md`'s DIAG-01 section demonstrate.

**Authored blind.** Neither blind read named below has been generated or opened while writing this
protocol. This document records rules only. It contains no per-document classification, no
per-document verdict, and no `CGATE-BUILD-01` disposition — all three are produced downstream, after
this commit, strictly by applying the rules fixed here.

## Purpose

`docs/v8.10-correctness-instrument-design.md` resolves the untraced-§6 reading fork (the
`declarative-only` vs. `every-extracted-sentence` disagreement measured in
`docs/v8.10-fix-contract-oos-validation.md`) by *defining* the load-bearing claim rather than
choosing a side of the fork. That resolution — the D-03 include/exclude rule — is, as of that
document, **the designer's own single reading** of the four documents it turns on
(`Q-N2`/`Q-N3`/`Q-N4`/`Q-N6`). This protocol exists to test that resolution before any milestone
commits to building the instrument the design proposes. If two genuinely independent, mutually-blind
readers applying the pre-registered D-03 rule agree on both the load-bearing-claim set and the
traced/untraced verdict for all four documents, the definition is fork-robust and `CGATE-BUILD-01`
is worth committing. If they still diverge, the definition only relocated the fork into "what counts
as load-bearing," and the honest disposition is `CGATE-BUILD-01` WON'T-DO — not a failure to chase
to "agree," but a legitimate, publishable outcome (honesty-not-score, D-01).

## The frozen problem set

This protocol governs exactly the two blind reads of the four fork-sensitive documents already
frozen under `tests/quality-baseline-v8.10-oos/analyses/`: `Q-N2.md`, `Q-N3.md`, `Q-N4.md`,
`Q-N6.md`. `Q-N1` and `Q-N5` are explicitly out of scope for the agreement gate — they carry no fork
to test — and are not among the four documents fed to either read. No other document, and nothing
generated after this commit, is in scope.

## (1) The D-03 load-bearing-claim definition — quoted verbatim

This is the rule under test, reproduced from `docs/v8.10-correctness-instrument-design.md`, §"Defining
the load-bearing claim — resolving the reading fork," exactly as written there, with no paraphrase:

- **Include** (a claim is load-bearing if it is one of these, and the conclusion rests on it):
  **recommendations, decisions, quantitative results, and causal assertions** the conclusion rests
  on.
- **Exclude** (never load-bearing, so never in the denominator): **section-intro labels**,
  **restatements of already-cited content**, and the **`**Confidence:**` / caveat field**.

This include/exclude pair is the denominator each blind read must identify per document — the
load-bearing-claim set. No other document, prior worked example, or per-document application of this
rule is reproduced in this protocol; the designer's own claimed per-document answers for
`Q-N2`/`Q-N3`/`Q-N4`/`Q-N6` are deliberately withheld from both readers (see the D-06 rule below).

## (2) Claim-unit granularity

A load-bearing claim is counted at **paragraph/bullet level** — the same unit the v8.10 hand-read
supplement used. A reader identifies a load-bearing claim as a distinct paragraph or bulleted item in
a document's conclusion (or elsewhere, if the conclusion rests on it), not as an isolated clause
within a longer paragraph and not as an entire section. This fixes the unit both readers apply
identically before either sees any document.

## (3) The two-part agreement criterion

Two readers **agree** on a document if and only if they agree on **both**:

- the load-bearing-claim set (the denominator) — the set of paragraph/bullet-level claims each
  reader identifies as load-bearing under the Rule (1) include/exclude pair; and
- the traced/untraced verdict for that document.

Each read must produce, per document, exactly one of three verdicts: **TRACED**, **UNTRACED**, or
**PARTIAL**, with the cited §4 chain / ground-truth evidence supporting each load-bearing claim's
traced-or-not judgment. Verdict agreement alone does not constitute agreement — because the fork
lived in the denominator, two readers reaching the same verdict via different load-bearing-claim sets
is not, by itself, evidence the definition is fork-robust; both parts must match (subject to the D-04
material-equivalence rule below).

## (4) The `CGATE-BUILD-01` decision gate

Stated here, before either read exists:

- **Agree on all four documents** (both denominator and verdict, per the D-04 material-equivalence
  rule below, for `Q-N2`, `Q-N3`, `Q-N4`, and `Q-N6`) → the D-03 definition is fork-robust →
  `CGATE-BUILD-01` (build and wire the correctness instrument into the firewall battery against the
  v8.10 fixture manifest) is worth committing as a future build milestone.
- **Any residual divergence** on any of the four documents (denominator or verdict, after applying
  D-04) → the definition only relocated the fork rather than dissolving it → `CGATE-BUILD-01` is
  marked **WON'T-DO**, and the DIVERGE line is closed as **characterized-but-not-closable** — not a
  fork the definition can be trusted to resolve, and not worth building a fork-dependent gate against.

Per honesty-not-score (D-01): a residual divergence is a legitimate, publishable outcome. This
protocol does not treat "diverge" as a failed test to be re-run, re-worded, or adjudicated toward
agreement after the fact.

## (5) D-04 — material-equivalence near-miss adjudication rule

"Agree on the load-bearing-claim set" uses **material-equivalence**, not raw string or byte
identity. Two claim-sets are **materially equivalent** if and only if every difference between them
is either:

- (i) a sentence both readers would **exclude** under the Rule (1) exclude list (a section-intro
  label, a restatement of already-cited content, or the `**Confidence:**`/caveat field); or
- (ii) a difference whose inclusion or exclusion does **not** change that document's traced/untraced
  verdict.

A difference that **flips** a document's verdict counts as **divergence**, regardless of how small
the differing claim-set is. This rule is fixed before either read and is applied identically to both
passes' output during reconciliation — it is not discretionary at reconciliation time.

Three edge rules, also fixed before any read:

- **Empty-denominator rule:** a document whose load-bearing-claim set is empty under the Rule (1)
  definition is pre-registered as **vacuously TRACED** — an empty denominator has no uncited
  load-bearing claim, so there is nothing to fail tracing on. Both readers apply this identically.
- **Order-insensitivity rule:** load-bearing-claim-set equivalence is **order-insensitive** (set
  semantics). The sequence in which a reader lists claims never affects equivalence scoring.
- **Meaning-not-bytes rule:** denominator equality is material-equivalence by meaning, per the D-04
  rule above — never raw string/byte identity of the quoted sentences. Two readers quoting the same
  claim with trivially different wrapping, punctuation, or excerpt boundaries are not, on that basis
  alone, divergent.

## (6) D-05 — three-signal reporting rule

To prevent the D-04 verdict-preserving equivalence rule from silently masking a real denominator
fork, the reconciliation (Plan 03) must record **all three signals**, per document:

- (a) raw load-bearing-claim-set overlap between the two reads (before applying D-04);
- (b) traced/untraced/partial verdict agreement between the two reads; and
- (c) the binary gate verdict under the D-04 material-equivalence rule (agree / diverge).

Signal (c) is what decides the `CGATE-BUILD-01` gate in Rule (4). But any case where the two reads
land on the same verdict (b) via a genuinely different denominator (a) — a same-verdict,
different-denominator case — must be **disclosed as an explicit caveat** in the reconciliation, never
folded silently into "agree." This is the reporting-completeness rule that honors the roadmap's
"check both verdict AND denominator" requirement while still applying the operational D-04 gate.

## (7) D-06 — the designer's own v8.10 reading is excluded from the gate

The decision gate in Rule (4) is **purely inter-pass agreement** between the two blind reads. The
designer's original v8.10 reading (its specific per-document verdicts are deliberately **not**
reproduced in this protocol, so the protocol can be fed verbatim to both readers without leaking the
answer) is:

- **withheld from both readers** during the read (neither blind pass is given
  `docs/v8.10-correctness-instrument-design.md`, any per-document worked example from it, or the
  other pass's output); and
- **reported afterward only as a third data point / consistency note** in the reconciliation — it
  never decides the gate, and a match or mismatch between the designer's reading and the two blind
  reads' agreed (or diverged) result is not itself evidence for or against `CGATE-BUILD-01`.

Folding a non-blind, non-independent reading into the gate would weaken the independence claim this
milestone exists to establish.

## (8) The read transport

The two mutually-blind reads are two **separate** plain `claude -p` invocations — one inference
context each, never a single orchestrator authoring both passes (a single context writing both
reads cannot be blind to itself). Each invocation:

- uses the **default model**, with **no** `--plugin-dir first-principles`, **no** `--probe`, and
  **no** first-principles agent dispatch of any kind — the reader is a general rule-applier reading
  this protocol and the four raw documents, not the agent under study, and this keeps the D-03
  invariant reframing below literally true;
- is fed **exactly** this protocol plus the four raw analyses (`Q-N2.md`, `Q-N3.md`, `Q-N4.md`,
  `Q-N6.md` under `tests/quality-baseline-v8.10-oos/analyses/`) and nothing else — not
  `docs/v8.10-correctness-instrument-design.md`, not the designer's worked examples, not the other
  pass's output;
- is captured to its own read-only file under `tests/defrobust-v8.11/`, mirroring the
  `tests/quality-baseline-v8.10-oos/` freeze conventions (a provenance README and manifest
  alongside the two captures and the shared read-input).

### Required per-document output format

For each of the four documents, each read must produce:

- the identified load-bearing-claim set, with each claim quoted **verbatim** from the source
  document;
- a traced/untraced mark for each load-bearing claim, citing the §4 chain / ground-truth evidence
  (or its absence) that the mark rests on; and
- the single document-level verdict: **TRACED**, **UNTRACED**, or **PARTIAL**.

No other output is required or expected from either read.

## (9) Invariant 2 reframed — zero live `claude` spend becomes zero live first-principles-agent spend

Milestone Invariant 2, as originally stated, reads "ZERO live `claude` spend." That invariant was
written to forbid the expensive live re-generation of the first-principles `Q-N*` analyses — the cost
`CORRECTGATE-01` (v8.10) already spent once, out-of-sample, and which this milestone does not repeat.

**This protocol explicitly reframes Invariant 2 to: "zero live first-principles-agent spend."** The
two blind read-passes described in Rule (8) are a permitted, bounded, one-shot cost precisely because
neither invokes `--plugin-dir first-principles` or dispatches the first-principles agent — they are
plain `claude -p` reads of documents already frozen on disk. Re-generating any of the `Q-N*`
analyses, or dispatching the first-principles agent for any purpose, remains forbidden under this
milestone. This reframing is a wording clarification, not a scope change, and it is stated here on
the page rather than left silent.

## What this protocol does not assert

This protocol asserts nothing about what either blind read will actually find in
`Q-N2`/`Q-N3`/`Q-N4`/`Q-N6`. It contains no per-document verdict, no load-bearing-claim set for any
document, and no `CGATE-BUILD-01` disposition, because neither read has been run at the time this
document is committed. Every rule above is stated in the abstract, to be applied mechanically once
the two reads exist — exactly the discipline this document exists to enforce on itself.

## Downstream procedure this protocol governs

For Plan 02 (`DEFROBUST-02`): dispatch the two separate, mutually-blind `claude -p` reads per Rule
(8), freeze both captures plus the shared read-input plus a provenance README/manifest under
`tests/defrobust-v8.11/`, and confirm via commit ordering that this protocol's commit strictly
precedes both read commits.

For Plan 03 (`DEFROBUST-03`): reconcile the two reads' per-document output under the two-part
agreement criterion (Rule 3), applying the D-04 material-equivalence rule (Rule 5) to adjudicate
near-misses, recording all three D-05 signals (Rule 6) per document, and reporting the designer's own
v8.10 reading only as the D-06 third data point (Rule 7). Apply the `CGATE-BUILD-01` decision gate
(Rule 4) to reach a single committed disposition in `docs/v8.11-defrobust-reconciliation.md`. Confirm
the human-arbiter fragility finding still stands as an open risk in
`docs/v8.10-correctness-instrument-design.md`'s "Open risk" section.

No document has been classified and no verdict has been computed as of this commit. This document
records rules only.


═══════════════════════════════════════════════════════════════════════════════
DOCUMENT Q-N2  (source: tests/quality-baseline-v8.10-oos/analyses/Q-N2.md)
═══════════════════════════════════════════════════════════════════════════════

## Missing inputs (stated per the input contract, then proceeding best-effort)

Three numbers would change the strength — not the direction — of this analysis, and one would change the direction:

1. **Direction-changing:** what share of current volume the two month-to-month accounts represent. I have flagged this as `GT-16?` and built the recommendation around a threshold rather than guessing it.
2. Contribution margin per kg roasted (`GT-11?`).
3. Current actual weekly roasted kg and true utilization (`GT-17?`), plus roaster lead time (`GT-12?`).

**Step 0 — technique selection:** no technique-specific trigger phrase fires (the prompt asks a decision question without naming a technique). `MODE = full-composer`. All five phases run; Phase 4 walks all eight companion techniques.

---

# Process output

## Phase 4 end-of-phase Assumption Audit (scan table)

| Chain | Step | Step text (brief) | Assumption surfaced? | Added to table? |
|---|---|---|---|---|
| C1 | 1 | 35kg raises capacity ~2.3x | Yes — the 35kg *replaces* the 15kg as primary rather than running alongside it with a second operator | Yes (A-9) |
| C1 | 2 | 20%/yr needs ~4.6 yrs to fill it | Yes — growth rate persists and is not a one-off catch-up year | Yes (A-3) |
| C1 | 3 | Asset under-utilised 3–4 yrs | No new assumption | — |
| C2 | 1 | Physical ceiling ≈5x current | No new assumption (from theoretical-limit derivation) | — |
| C2 | 2 | One shift is convention, not a bound | No new assumption | — |
| C2 | 3 | Second shift ≈2x ≈3.8 yrs of growth | Yes — a competent second-shift roaster is hireable and retainable at $4,200/mo | Yes (A-10) |
| C3 | 1 | Annualised capex ≈1/3 of shift labour | Yes — 7-year depreciation life and no financing interest | Yes (A-11) |
| C3 | 2 | Contribution at stake ≈$100–250k/yr | Yes — unmet demand is *fillable* demand, not enquiry noise | Yes (A-12) |
| C3 | 3 | Cost gap is second-order | No new assumption | — |
| C4 | 1 | Shift downside ≈$5–10k | Yes — no severance/notice obligation beyond one month | Yes (A-13) |
| C4 | 2 | Roaster downside ≈$40–60k | Yes — install work is non-recoverable; used-roaster market is liquid | Yes (A-6, already present) |
| C4 | 3 | Reversibility premium is worth paying | No new assumption | — |
| C5 | 1 | Duty cycle 2x halves time-to-service | Yes — wear scales with operating hours, not thermal cycles | Yes (A-8, already present) |
| C5 | 2 | Zero redundancy persists | No new assumption | — |
| C5 | 3 | Shift is bridge, not destination | No new assumption | — |
| C6 | 1 | Twin machine gives same 2x + redundancy | Yes — a second 15–25kg machine is available at roughly half the $103k | Yes (A-14) |
| C6 | 2 | Preserves existing roast profiles | Yes — profiles transfer between identical-model machines without re-development | Yes (A-15) |
| C7 | 1 | Bridge covers the lead-time window | Yes — accounts will engage on term conversion at all | Yes (A-16) |
| C7 | 2 | Defer irreversible spend | No new assumption | — |
| C7 →[2nd] | 3 | Term-conversion push runs in parallel | Yes — asking for terms may invite the account to shop competitors | Yes (A-17) |
| C7 →[3rd] | 4 | Bottleneck migrates downstream | No new assumption | — |

No enumerated second/third-order effect contradicts a Ground Truth, so no conclusion routes back to Phase 2.

## §6 → §4 closure ledger

```text
- "Do not buy the 35kg roaster now"                     → chains C1, C4 ✓
- "Do not adopt a permanent double shift as end state"  → chain  C5 ✓
- "Do not hold off entirely"                            → chains C2, C3 ✓
- "Bridge with a partial second shift now"              → chains C2, C7 ✓
- "Price a twin 15–25kg against the 35kg"               → chain  C6 ✓
- "Buy on a pre-registered trigger, not a feeling"      → chains C4, C7 ✓
- "The 35kg is sized to demand you don't have yet"      → chain  C1 ✓
- "Cost is not the deciding variable here"              → chain  C3 ✓
```

Ledger clean — every §6 claim carries a §4 chain reference.

---

# 1. Problem Essence

**Essence Statement:** *Given that capacity is binding now but the durability of the demand behind it is unverified, what is the cheapest way to buy production headroom without committing capital that becomes unrecoverable if the unsecured accounts leave?*

This is deliberately not "which of the three options is best." The question you asked frames it as a three-way pick between two capacity instruments and inaction. Stripped down, the real decision has two independent dimensions that the three-way framing conflates:

- **How much capacity, and when** (a sizing question, answerable from arithmetic)
- **How reversible the commitment is** (a risk question, answerable only after the account-terms uncertainty resolves)

Success criteria a correct answer must satisfy:

1. Relieves the binding constraint within the next 1–3 months (demand is being turned away now)
2. Does not create an unrecoverable loss larger than the roastery can absorb if both at-risk accounts exit
3. Does not increase the probability of a total production outage
4. Preserves cup quality and existing roast profiles for wholesale accounts
5. Leaves the capital decision improvable by information you can obtain cheaply

---

# 2. Assumptions Table

Built via **fishbone** (breadth, default six-category set — People, Process, Technology, Environment, Information, Resources) and **inversion** (what would guarantee this decision fails).

| # | Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|---|
| A-1 | Capacity, not demand, is the current binding constraint | current constraint | Record expiry conditions | ACCEPTED — expires if either large account exits | Stated: "selling out capacity most weeks" |
| A-2 | "Selling out most weeks" means turning away orders, not just running full | untested belief | Verify | **UNVERIFIED — flagged** | Needs order-refusal log |
| A-3 | 20% YoY growth persists forward | untested belief | Verify | **UNVERIFIED — flagged** | One year of history; could be post-COVID catch-up or one account ramping |
| A-4 | The two at-risk accounts are material enough that losing them un-binds capacity | untested belief | Verify — **direction-changing** | **UNVERIFIED — flagged as `GT-16?`** | You have this number; I don't |
| A-5 | Month-to-month means terminable at short notice with no penalty | convention | Challenge before use | ACCEPTED | Standard wholesale coffee practice; confirm the actual notice clause |
| A-6 | $15k electrical/ventilation is non-recoverable; roaster resells at 50–70% | convention | Challenge before use | ACCEPTED with range | Used-roaster market is real but thin for 35kg |
| A-7 | Bigger machine = better unit economics | convention | **Challenge** | **REJECTED as stated** — true only at high utilisation; see C1 | Fixed cost per kg falls only if the kg exist |
| A-8 | Machine wear scales with operating hours | current constraint | Record expiry | ACCEPTED, partial | Drum/bearing wear does; thermal-cycling fatigue scales with *starts*, which a continuous second shift actually reduces per kg |
| A-9 | The 35kg replaces the 15kg as primary | untested belief | Verify | **UNVERIFIED — flagged** | Surfaced by audit (C1); if you run both simultaneously you need a second operator, which re-imports the shift's labour cost |
| A-10 | A competent second-shift roaster is hireable at $4,200/mo | untested belief | Verify | **UNVERIFIED — flagged** | Surfaced by audit (C2); specialty roasting is a skilled role and evening shifts are hard to staff |
| A-11 | 7-year depreciation, no financing interest | untested belief | Verify | **UNVERIFIED — flagged** | Surfaced by audit (C3); a loan at 8–10% adds ~$25k over the term |
| A-12 | Unmet demand is fillable demand | untested belief | Verify | **UNVERIFIED — flagged** | Surfaced by audit (C3) |
| A-13 | Shift is cancellable at ~1 month with no severance | untested belief | Verify | **UNVERIFIED — flagged** | Surfaced by audit (C4); jurisdiction-dependent |
| A-14 | A second 15–25kg machine is available at roughly half of $103k | untested belief | Verify | **UNVERIFIED — flagged** | Surfaced by audit (C6); quote it |
| A-15 | Profiles transfer between identical-model machines without re-development | untested belief | Verify | **UNVERIFIED — flagged** | Surfaced by audit (C6); near-true for identical models, false across sizes |
| A-16 | The accounts will engage on term conversion | untested belief | Verify | **UNVERIFIED — flagged** | Surfaced by audit (C7) |
| A-17 | Asking for terms carries no downside | untested belief | **Challenge** | **REJECTED** — it invites re-evaluation; pair the ask with a price or priority incentive | Surfaced by audit (C7 second-order) |
| A-18 | The three named options are the complete option set | convention | **Challenge** | **REJECTED** — a right-sized twin machine, a partial shift, and toll roasting are all in scope | Five-whys reduction (§3) shows the constraint admits three classes of fix: add hours, add asset, outsource |
| A-19 | Roasting is the only bottleneck | untested belief | Verify | **UNVERIFIED — flagged** | Doubling output loads packaging, QC, delivery |
| A-20 | $15k install estimate holds | untested belief | Verify | **UNVERIFIED — flagged** | Three-phase service upgrades, permits, and fire suppression routinely overrun |

**Inversion pass (what would guarantee failure), abbreviated:** both accounts exit within 12 months → stranded capex; second-shift roaster cannot be hired or quits → capacity gain never materialises; the single 15kg fails under doubled duty during peak → total outage; 35kg profile migration changes the flagship blend → account churn; install overruns → capex materially above $103k; growth was a one-off → all added capacity idles. Each unverified precondition is recorded above.

---

# 3. Ground Truths

**GT-1** — Roasted output = batch size × batches/hour × operating hours. Capacity scales linearly in each factor independently. *(Definitional.)*

**GT-2** — Green→roasted mass loss is ~14–18% for medium roasts (free moisture plus organic dry-matter loss). *(Physical; well-established.)*

**GT-3** — 35 ÷ 15 = 2.33. A 35kg machine delivers 2.33x the mass per batch. *(Arithmetic.)*

**GT-4** — Drum-roaster cycle time is roughly size-independent within the commercial class (~10–16 min), because machines are engineered to a target cycle rather than a target heat flux. *(Direct measurement / design convention; confirm against your candidate machine's spec sheet.)*

**GT-5** — Roaster option total capex = $88,000 + $15,000 = **$103,000**. *(Given.)*

**GT-6** — Shift option = $4,200/mo = **$50,400/yr**. *(Given.)*

**GT-7** — Demand +20% YoY. *(Given measurement; persistence is A-3, unverified.)*

**GT-8** — Two largest wholesale accounts are month-to-month with no commitment. *(Given.)*

**GT-9** — Capacity is binding most weeks. *(Given.)*

**GT-13** — Operating expense is terminable at the notice period; capital expenditure is sunk at the moment of purchase. This asymmetry is definitional, not situational. *(Definitional — irreducible.)*

**GT-14** — With one roaster, roaster downtime sets production to zero. There is no partial-failure mode. *(Definitional.)*

**GT-10?** — Install work non-recoverable; roaster resale 50–70%. *(Unverified.)*
**GT-11?** — Contribution margin ≈ $6–10/kg roasted wholesale. *(Unverified.)*
**GT-12?** — New roaster lead time + install ≈ 3–6 months. *(Unverified.)*
**GT-15?** — Doubling duty cycle roughly halves calendar time to major service. *(Unverified; partially contradicted by A-8's thermal-cycling caveat.)*
**GT-16?** — **Share of volume held by the two at-risk accounts: UNKNOWN.** *(The single highest-leverage missing fact.)*
**GT-17?** — Current weekly roasted kg: unknown; estimated below.

**Five-whys reduction of "we are selling out capacity":** orders exceed roasted kg available → roasted kg is fixed by batch size × batches × hours → all three are fixed → because there is one machine run one shift → because staffing was never scaled past the original configuration. **Root:** the constraint is a *staffing convention plus a single-asset design*, not a physical limit. This bottoms out at an actionable, in-your-control cause, and it establishes that the fix classes are exactly three: add hours, add asset, or outsource — which is what rejects A-18.

---

# 4. Derivation Chains

### C1 — The 35kg is sized to demand you do not yet have

**Estimate (Fermi) sub-step.** Target: current weekly roasted kg. Unit decomposition: `(kg green/batch) × (batches/hr) × (hr/day) × (days/wk) × (roasted/green) → kg roasted/wk`.

- kg green/batch: 13 (GT-1; full 15kg drums are typically run at 85–90% for profile control)
- batches/hr: 4 (GT-4, 15-min cycle)
- productive hr/day: 6 of an 8-hr shift (warm-up, cleaning, QC, changeover)
- days/wk: 5
- roasted/green: 0.84 (GT-2)

Central: 13 × 4 × 6 × 5 × 0.84 = **1,310 kg roasted/wk**. Bracket **[850, 1,310, 1,800]**. Decision-resolution check: both ends drive the same conclusion below, so the estimate is good enough.

**Chain:** GT-1 + GT-3 + GT-7 → *a 35kg run as primary lifts capacity ~2.3x, while 20%/yr compounding needs* `ln(2.3) ÷ ln(1.2) ≈ 4.6 years` *to consume it* → *the $103,000 asset runs below 50% utilisation for roughly its first three years* → **the 35kg is not sized to your demand curve; it is sized to your 2030 demand curve.** `[Assumes: A-9, A-3]`

Confidence: **HIGH** on the arithmetic, **MEDIUM** on the conclusion (depends on A-3). This is the finding that reframes the whole question: the choice was presented as "enough capacity vs. not enough," and it is actually "roughly 2x vs. roughly 2.3x-that-you-pay-for-now."

### C2 — A second shift is the increment that matches the curve

**Theoretical-limit sub-step.** Governing constraint: none of thermodynamics binds here — the limit is duty cycle and human availability. Law-permitted ceiling: 4 batches/hr × 20 hr/day (4 hr reserved for cool-down, chaff clearing, and cleaning) × 13kg × 7 days × 0.84 ≈ **6,100 kg roasted/wk**. Conventional figure: ~1,310 kg/wk. **Gap: ~4.7x.** Irreducible portion: thermal recovery between batches, chaff-fire risk requiring daily cleaning, and roaster fatigue — these cap sustained operation near 2–2.5 shifts, not 3. Convention-driven portion: the single-shift staffing pattern, which is pure inertia.

**Chain:** GT-1 + GT-9 + [theoretical limit ≈ 4.7x headroom] → *one shift is a staffing convention, not a machine limit; the machine can sustain ~2–2.5 shifts* → *a second shift delivers ~2x, which at 20%/yr covers* `ln(2) ÷ ln(1.2) ≈ 3.8 years` → **the shift is the better-matched capacity increment, and the machine will physically take it.** `[Assumes: A-10]`

Confidence: **HIGH** on the physical headroom, **MEDIUM-HIGH** overall (hinges on hiring).

### C3 — Cost is not the deciding variable

**Chain:** GT-5 + GT-6 + GT-11? → *annualised roaster cost ≈ $103k ÷ 7 ≈ $14.7k/yr plus energy, versus $50.4k/yr for the shift — a spread of ~$35k/yr* → *meanwhile, unmet demand at ~1,000 incremental kg/wk × $6–10/kg contribution is roughly $100k–250k/yr of margin* → **the cost difference between the two options is a fraction of the margin at stake, so the decision should be optimised for demand durability and supply reliability, not for lowest cost.** `[Assumes: A-11, A-12]`

Confidence: **MEDIUM** — GT-11? is unverified and drives the magnitude. Verifying your actual contribution margin would raise this to HIGH.

### C4 — The reversibility asymmetry is worth its premium *for a bounded period*

**Chain:** GT-8 + GT-13 + GT-10? → *shift downside if demand evaporates ≈ one month's notice + hiring and training sunk ≈ $5–10k; roaster downside in the same scenario ≈ $15k install (unrecoverable) + 30–50% of $88k depreciation on forced resale ≈ $40–60k* → *the shift costs ~$35k/yr more but caps the bad outcome roughly 6x lower* → **paying the reversibility premium is rational for exactly as long as the account-terms uncertainty is live — and irrational after it resolves.** `[Assumes: A-13, A-6]`

Confidence: **MEDIUM-HIGH.** The time-bounding is the load-bearing part: this chain does not argue for the shift permanently, and C5 explains why it must not be permanent.

### C5 — A permanent double shift makes the fragility worse

**Chain:** GT-14 + GT-15? → *doubling duty cycle on a single machine roughly halves calendar time to major service while leaving zero redundancy* → *the failure probability rises fastest exactly when volume and commitments are highest* → **the second shift is defensible as a bridge and indefensible as an end state.** `[Assumes: A-8]`

Confidence: **MEDIUM-HIGH.** Softened by A-8's caveat — continuous running actually reduces thermal cycling per kg, so wear may scale sub-linearly. The redundancy half of the argument is unaffected by that caveat and carries the conclusion on its own.

### C6 — The 35kg is not the only capital option, and probably not the best one

**Trade-off analysis sub-step.** Criteria and weights locked before any scoring:

| Criterion | Weight | A: 35kg | B: full 2nd shift | C: hold | D: staged | E: twin 15–25kg |
|---|---|---|---|---|---|---|
| Capacity headroom vs growth | 5 | 5 | 3 | 1 | 4 | 3 |
| Reversibility under demand loss | 5 | 2 | 5 | 5 | 4 | 3 |
| Capital preservation | 4 | 2 | 5 | 5 | 4 | 4 |
| Supply reliability (redundancy) | 4 | 5 | 1 | 2 | 4 | 5 |
| Quality / profile continuity | 3 | 3 | 3 | 5 | 4 | 5 |
| Speed to relief | 4 | 2 | 5 | 1 | 5 | 3 |
| Unit economics at 2–3 yrs | 3 | 5 | 2 | 1 | 4 | 4 |
| **Weighted total** | | **95** | **99** | **80** | **116** | **105** |

*Sensitivity:* A (95) and B (99) sit within 4% — a genuine near-tie, and both are defensible as pure plays. The criterion that would flip them is redundancy (weight 4); I do not believe that weight is wrong, so the near-tie is a real finding rather than a scoring artefact. D and E separate cleanly from both and from each other by more than the noise band.

**Chain:** C1 + C5 + GT-3 → *a second machine matched to your current batch size delivers the same ~2x as the shift, adds full redundancy, preserves existing profiles because thermal mass and drum geometry are unchanged, and costs roughly half of $103,000* → **the capital question is not "35kg or nothing" — a right-sized twin dominates the 35kg on every criterion except raw headroom you will not use for four years.** `[Assumes: A-14, A-15]`

Confidence: **MEDIUM** — A-14 and A-15 are both unverified and both cheap to verify (one quote, one conversation with the manufacturer).

### C7 — The staged path, with second-order extension

**Chain:** C2 + C4 + C6 + GT-12? → *only a staged path relieves capacity inside the 3–6 month equipment lead time, preserves reversibility while the terms uncertainty is live, and defers the irreversible spend until it can be sized on better information* → **bridge with a partial second shift now; resolve account terms within 60–90 days; then buy a right-sized second machine on a pre-registered trigger.** `[Assumes: A-16]`

→**[2nd]** Hiring a second-shift roaster in a thin labour market may take 4–8 weeks and adds cross-shift quality variance requiring a documented profile and QC protocol. `[Assumes: A-10]`
→**[2nd]** Doubling green throughput lengthens the cash-conversion cycle — more green inventory, more capital tied up, before any additional receivable lands.
→**[2nd]** The term-conversion ask may itself prompt an account to re-evaluate and shop the market. `[Assumes: A-17]` — mitigate by pairing the ask with something they want: locked pricing, priority allocation during peak, or a volume rebate.
→**[3rd]** A successful term conversion becomes financeable evidence, improving equipment-loan terms and lowering the effective cost of the eventual capex.
→**[3rd]** At 2x output the bottleneck migrates downstream to packaging, QC cupping, and delivery — neither original option addresses this, and it will surface within weeks of the shift starting.
→**[3rd]** Excess capacity, once installed, creates pressure to fill it with private-label or co-packing work, which is itself a hedge against wholesale concentration.

Stopping at the 3rd order; the 4th becomes speculation. **Contradiction check:** no enumerated effect contradicts GT-1 through GT-17?. The A-17 effect refines GT-8 rather than contradicting it. No route back to Phase 2 is triggered.

Confidence: **MEDIUM-HIGH.**

---

# 5. Abandoned Reasoning

**Framed as an NPV cost-minimisation.** My first pass built a discounted-cash-flow comparison of $103k capex against a $50.4k/yr opex stream, yielding a ~24-month crossover. Abandoned once C3 showed the annual spread (~$35k) is small relative to the contribution at stake (~$100–250k/yr). A model that optimises a second-order variable to three decimal places while the first-order variable is unmeasured is precision theatre.

**Recommending an outright "buy" on asymmetric payoff.** I built a case that bounded downside (~$55k stranded) versus unbounded upside (~$250k/yr of margin) favours buying even at p(demand holds) ≈ 0.5. Abandoned because C1 broke the premise: the upside is not gated on *35kg* capacity specifically. A cheaper twin captures nearly all of the same margin, so the asymmetry argues for buying *something*, not for buying *this*.

**Toll roasting / co-packing as the bridge.** Retained as a fallback, rejected as primary. It transfers your profiles and green sourcing to a third party, most co-packers will not take specialty-scale volumes at acceptable quality, and the QC exposure lands precisely on the two accounts you can least afford to disappoint.

**"Hold off" as a standing option.** Rejected outright: capacity is binding now (GT-9), so holding is the only option that carries an ongoing cost — foregone margin — while purchasing no option value in return. Its 80 in the trade-off matrix is the lowest of the five for exactly this reason.

**Buying the 35kg but running both machines simultaneously.** Considered as a way to defeat C1's utilisation argument. Abandoned because it requires a second operator, which re-imports the shift's ~$50k/yr labour cost on top of the $103k capex — the worst of both options rather than the best.

---

# 6. Conclusion

**Do none of the three things as posed. Stage it.**

**The 35kg roaster is sized to demand you do not have yet (C1).** At 20% annual growth it takes about 4.6 years to fill. You would be paying $103,000 today for headroom that sits idle for roughly three of those years, while the two accounts underwriting the growth can leave with thirty days' notice.

**Do not adopt a permanent double shift as the end state either (C5).** It doubles duty cycle on a single machine with zero redundancy — raising outage probability exactly when your commitments peak. It is a fine bridge and a poor destination.

**Do not hold off (C2, C3).** Capacity binds now, the machine has roughly 4.7x physical headroom that only a staffing convention is blocking, and the margin you are turning away likely exceeds the cost of either fix by an order of magnitude.

**What to do, in order:**

1. **Now — add a partial second shift**, not a full one. A four-to-five-hour evening turn at roughly $2,100–2,500/mo buys most of the capacity at half the cost and half the wear, and it is cancellable at thirty days (C2, C4, C7). This is the bridge across the equipment lead time, which you will need regardless of what you eventually buy.
2. **Within 30 days — get the one number that decides this.** What percentage of volume do those two accounts represent? Rough thresholds from C1's arithmetic: if their combined share is **under ~20%**, growth alone keeps you capacity-bound through their loss and you should buy. If it is **over ~35%**, losing them returns you to slack capacity and you should not commit capital until the account base is broader.
3. **Within 60–90 days — convert the terms.** Offer locked pricing, priority peak allocation, or a volume rebate in exchange for a six-to-twelve-month commitment or a monthly volume floor. Do not make a bare ask: it invites them to shop (A-17, C7 second-order). A signed floor is also financeable collateral that improves your eventual loan terms.
4. **Then buy — but price a twin, not the 35kg (C6).** A second 15–25kg machine gives you the same ~2x capacity, full redundancy against the failure mode that scares me most, identical roast profiles with no re-development risk to your flagship blends, and roughly half the capital outlay. Get that quote before you sign anything for the 35kg.
5. **Pre-register the trigger now, while you are calm.** Write it down: *"We order when (a) contracted or floor-committed volume covers X kg/week, or (b) the two at-risk accounts fall below Y% of volume, whichever comes first."* Deciding the rule before the data arrives is what stops a good month from being mistaken for a trend.

**Cost is not the deciding variable here (C3).** The $35k/yr spread between your two original options is a rounding error against the ~$100–250k/yr of margin that hinges on whether the demand is durable. Spend the next ninety days buying information about that, not equipment.

---

## Phase 5 — Validation

**Weakest links, flagged rather than resolved:**

- **`GT-16?` (account concentration) is load-bearing for the entire recommendation.** Every threshold in §6 step 2 is derived arithmetic, but the input is yours to supply. This is the single verification that would move the whole analysis from MEDIUM to HIGH confidence.
- **`GT-11?` (contribution margin) is load-bearing for C3**, which is what demotes cost from a primary to a secondary criterion. If your true contribution is nearer $3/kg than $8/kg, C3 weakens materially and the cost comparison re-enters as a first-order concern.
- **A-14/A-15 (twin machine price and profile transfer) are load-bearing for C6**, my most actionable recommendation. Both are unverified. Both cost one phone call to verify. Do not act on C6 before making those calls.
- **A-10 (hireability) is load-bearing for C2 and C7.** If you cannot hire a competent evening roaster, the bridge does not exist and the decision collapses back to a straight buy-or-hold — in which case, given C1 and C6, buy the twin.
- **A-8 partially contradicts GT-15?**, softening C5's wear argument. C5's conclusion survives on the redundancy argument alone, which is unaffected.

**Pre-mortem (prospective hindsight — "the plan has already failed; what caused it?"):** the recurring cluster across enumerated failure causes is not cost overrun or misjudged demand. It is **the single point of failure combined with the unmeasured concentration number** — the same two roots appear in five of seven failure paths. That clustering is a structural weakness in your current position, independent of which option you pick, and it is why redundancy carries a weight of 4 in the matrix and why C6 ends up dominating. The staged plan addresses both roots: step 2 measures the concentration, step 4 removes the single point of failure. If you take nothing else from this, take those two.

**Rubric gate:** Essence answered ✓ · every §6 claim traced to a named chain ✓ (see ledger) · every chain contains at least one intermediate step ✓ · all assumptions classified and verdicted ✓ · unverified inputs marked `?` and their dependent conclusions caveated ✓ · abandoned paths recorded ✓ · no analogy used as standalone evidence ✓ · second-order pass run with contradiction check ✓ · Assumption Audit run and table updated ✓.

**Overall confidence: MEDIUM-HIGH on the sequencing, MEDIUM on the thresholds.** The sequencing (bridge → measure → convert → buy right-sized) is robust across the full range of my unverified inputs. The specific 20%/35% thresholds move with `GT-16?` and `GT-11?`.

═══════════════════════════════════════════════════════════════════════════════
DOCUMENT Q-N3  (source: tests/quality-baseline-v8.10-oos/analyses/Q-N3.md)
═══════════════════════════════════════════════════════════════════════════════

## Process output — Step 0 technique selection

No technique-specific trigger phrase fires ("should we X, Y, or Z" is a decision framing, not a named technique request). **MODE = full-composer.** All five phases run; Phase 4 walks the companion techniques the problem calls for (estimate, trade-off, second-order), Phase 5 runs pre-mortem.

One note on the input contract: you gave a clear problem statement, domain, and constraints. Two things I would normally ask for are missing — **what fraction of revenue the biggest customer represents**, and **whether the renewal decision date is the renewal date**. I have proceeded and carried both as explicitly flagged unverified inputs (GT-5?, GT-8?) rather than stalling, because the analysis's direction turns out not to hinge on them; the *strength* of the recommendation does. See the Conclusion's caveats.

---

# First-Principles Analysis: Flutter Consolidation Decision

## 1. Problem Essence

**Core question:** Given a fixed engineering capacity and a dated, revenue-critical commitment 9 months out, what is the lowest-regret allocation of the next ~9 months of engineering time across platform consolidation and feature delivery?

This is deliberately *not* "is Flutter the right long-term technology." That is a separate and much easier question. The triggering event is a technology-choice question; the actual decision under constraint is a **scheduling and sequencing** problem in which the technology choice is one variable. Reframing matters here because the two questions have different answers — Flutter can be the correct destination while "start the 7-month migration now" is the wrong move.

**Success criteria** — a correct answer must:

1. State what happens to the 9-month renewal under each option, not just the 7-month build.
2. Distinguish the cost of *choosing wrong* from the cost of *choosing late*.
3. Account for the 1/3 older-device population as a constraint on the destination, not just the journey.
4. Name what evidence would change the recommendation, and by when it must be gathered.

---

## 2. Assumptions Table

| # | Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|---|
| A1 | The 7-month migration estimate is a central estimate | convention | Challenge before use | **Rejected.** Rewrite estimates for feature-parity migrations are near-universally floors, not centrals — they price the build and omit parity burn-in, platform-channel edge cases, and defect re-discovery | Challenged in Phase 4 via estimate; see C2 |
| A2 | "Largely stall" means zero feature output | untested belief | Verify or flag | **Refined.** 5 of 8 engineers migrate; 3 remain. Stall is partial, and that residual capacity is the decision's main degree of freedom | Derived from your own numbers (8 engineers, 5 assigned) |
| A3 | The renewal decision happens at month 9 | untested belief | Verify or flag | **Flagged unverified — load-bearing.** Enterprise renewal evaluations typically commit 2–4 months before the paper date | → GT-8? |
| A4 | Two feature requests are a renewal *condition*, not a wish list | untested belief | Verify or flag | **Flagged unverified.** Materially changes stakes; a customer naming specific features at renewal time usually means conditions | → GT-10? |
| A5 | Flutter runs acceptably on the older third of devices | convention | Challenge before use | **Challenged, unresolved.** Flutter ships an embedded engine, raising binary size and cold-start cost relative to native; on low-RAM/older-SoC devices this is where regressions concentrate. Not disproven — but untested *on your device mix* | → GT-9? |
| A6 | Consolidation halves platform engineering cost | convention | Challenge before use | **Partially rejected.** Consolidation removes duplicated UI/business logic but not platform-specific integration, store compliance, or per-OS QA. Savings are real but sub-linear | Structural; see C4 |
| A7 | Delay is free | untested belief | Verify or flag | **Rejected.** Delay accrues duplicated feature cost every month both codebases stay live, and each new native feature enlarges the eventual migration surface | Feeds C5 |
| A8 | The 120k LOC total is the migration's true scope | current constraint | Record expiry conditions | **Accepted with caveat.** Expires the moment new native features land — scope grows with every month of deferral | Feeds C5 |
| A9 | Team retention survives a 7-month feature freeze | untested belief | Verify or flag | **Flagged unverified.** Freezes plus rewrites are a known attrition trigger; losing 1 of 5 migration engineers mid-rewrite is schedule-fatal | Surfaced by pre-mortem, Phase 5 |
| A10 | The biggest customer is a large enough revenue share to dominate the decision | untested belief | Verify or flag | **Flagged unverified — load-bearing** | → GT-5? |
| A11 *(surfaced by audit)* | 3 residual native engineers can deliver 2 features in ~6 months | untested belief | Verify or flag | **Flagged.** Plausible for 2 scoped features on a mature codebase, but unsized here | Added by Phase 4 audit |
| A12 *(surfaced by audit)* | Features built natively during a deferral are re-portable to Flutter | untested belief | Verify or flag | **Flagged.** True in most cases, but re-port cost is real and additive | Added by Phase 4 audit |
| A13 *(surfaced by audit)* | A bounded Flutter spike produces decision-grade evidence | untested belief | Verify or flag | **Flagged.** True only if the spike targets the riskiest surface (older devices + hardest platform integration), not a demo screen | Added by Phase 4 audit |

**Inversion pass** (applied because "consolidate to Flutter" felt like the tidy answer). Inverted claim: *"Consolidating to Flutter now will not succeed."* Failure-guaranteeing conditions enumerated: (i) migration overruns past the renewal decision date; (ii) Flutter regresses UX on older devices badly enough to be noticed; (iii) the two customer features slip; (iv) an engineer departs mid-rewrite; (v) the rewritten app ships at parity but with a defect tail that consumes the post-launch months. Necessary preconditions extracted from these became A1, A5, A9, A11 above — note that **four of the five failure modes are schedule-adjacent, and only one is technology-adjacent.** That asymmetry is the analysis's first real finding.

---

## 3. Ground Truths

| ID | Fact | Source |
|---|---|---|
| GT-1 | Two native codebases, ~60k LOC each (~120k total) | Reported directly |
| GT-2 | 8 engineers total, 4 per platform | Reported directly |
| GT-3 | Proposed migration: 5 engineers, ~7 months, with feature work largely stalled | Reported directly |
| GT-4 | ~1/3 of users are on older devices | Reported directly |
| GT-5? | The renewing customer is the largest, contract renews in 9 months | Reported; *revenue share unverified* |
| GT-6 | The customer has asked for two specific features | Reported directly |
| GT-7 | A Flutter app embeds a rendering engine and runtime, adding baseline binary size and cold-start cost relative to a native app | Platform architecture; direction certain, magnitude device-dependent |
| GT-8? | Enterprise renewal decisions commonly commit before the contract's paper date | Industry pattern — **unverified for this customer** |
| GT-9? | Flutter's performance on your specific older-device mix is unmeasured | Absence of evidence, stated as such |
| GT-10? | Whether the two features are renewal conditions is unestablished | **Unverified** |
| GT-11 | Migration consumes 5 of 8 engineers, leaving 3 | Arithmetic on GT-2 + GT-3 |

Irreducibility note: GT-11 is derived, not reported, but bottoms out at arithmetic over two reported measurements, so it qualifies. GT-7 bottoms out at an architectural fact about how Flutter ships (its own renderer rather than platform widgets) — the *direction* is a structural consequence, the *magnitude* is not, which is exactly why GT-9? exists as a separate, explicitly-empty ground truth.

---

## 4. Derivation Chains

### C1 — The schedule collision (the load-bearing chain)

`GT-3 + GT-5? + GT-8? → the migration completes at month 7, but the renewal decision likely commits at months 5–7 → the customer evaluates you during the deepest part of the stall, on a codebase mid-rewrite → consolidating now places the renewal inside the risk window rather than after it.`

Confidence: **MEDIUM-HIGH**, capped by GT-8?. If the renewal decision genuinely happens at month 9 with no earlier evaluation, this chain weakens considerably — verifying GT-8? is the single highest-value hour of work available to you this week.

### C2 — What the 7 months actually buys (estimate)

Target quantity: engineer-months required to reach shipped feature parity on Flutter.

Decomposition (units: `LOC × engineer-months/LOC → engineer-months`):

- Migratable scope: 120k LOC across two platforms, but the duplicated business/UI logic converges. Target Flutter surface ≈ **60–75k LOC**.
- Proposed budget: 5 engineers × 7 months = **35 engineer-months** → implies ~1,700–2,100 LOC/engineer-month.
- That rate is defensible for *greenfield* code. This is not greenfield: it is a parity rewrite, where the binding cost is not authoring lines but rediscovering the undocumented behaviour those lines encode — every edge case two mature codebases learned over their lifetime must be re-learned.
- Parity rewrites additionally carry a tail the build estimate rarely prices: platform-channel work for native integrations, store/compliance re-certification, and a defect burn-in period after "code complete."

Bracket: **[7 months (if the estimate is right and nothing is rediscovered), ~10 months central, 14+ months if the parity tail behaves typically].**

Decision-resolution stop criterion: **the bracket fails it.** The lower bound (7 months) and the upper bound (14 months) drive *opposite* decisions relative to the 9-month renewal. This is not an estimate that can be tightened by thinking harder — it can only be tightened by measurement, which is itself an argument for the spike in C4. `[Assumes: A1, A8]`

### C3 — The older-device constraint binds the destination, not just the route

`GT-4 + GT-7 + GT-9? → one third of your users sit in the exact band where Flutter's engine overhead is most likely to be perceptible → the consolidation's viability depends on an unmeasured quantity → committing 35+ engineer-months before measuring it inverts the normal order of risk retirement.`

Confidence: **MEDIUM** (GT-9? is an explicit unknown). The point is not that Flutter will fail on older devices — it very often does not. The point is that you would be spending your largest engineering investment in years on an untested premise, when the test costs perhaps 2–3 engineer-weeks. `[Assumes: A5]`

### C4 — Trade-off analysis

Criteria and weights **locked before scoring**:

| Criterion (higher = better) | Weight |
|---|---|
| Protects the 9-month renewal | 5 |
| Delivery-risk containment (tolerates overrun) | 4 |
| Older-device experience preserved | 4 |
| Long-run engineering cost efficiency | 3 |
| Optionality / reversibility preserved | 3 |
| Decision quality at commit time (evidence available) | 3 |
| Team retention & morale | 2 |

Options: **(1) Consolidate now** · **(2) Keep both native indefinitely** · **(3) Structured deferral** — ship the two features natively now, run a bounded Flutter de-risking spike in parallel, decide at a dated checkpoint.

| Criterion | W | Opt 1 | Opt 2 | Opt 3 |
|---|---|---|---|---|
| Renewal protection | 5 | 1 | 5 | 5 |
| Delivery-risk containment | 4 | 1 | 5 | 4 |
| Older-device UX | 4 | 2 | 5 | 5 |
| Long-run cost efficiency | 3 | 5 | 2 | 3 |
| Optionality preserved | 3 | 1 | 3 | 5 |
| Decision quality at commit | 3 | 2 | 2 | 5 |
| Retention & morale | 2 | 2 | 3 | 4 |
| **Weighted total** | | **45** | **92** | **108** |

`Trade-off result → Option 3 (108) > Option 2 (92) > Option 1 (45).`

Sensitivity: the 1↔3 gap is decisive and not worth probing. The 2↔3 gap is ~15%, above the 10% near-tie band, so it stands — but the criterion that would flip it is *long-run cost efficiency*. If you weighted that at 5 and optionality at 1, Option 2 gains and Option 3 loses ground, though Option 3 still leads. Option 1 does not win under any weighting I can justify **before** seeing results, which is the relevant test. `[Assumes: A11, A13]`

### C5 — Second-order extension of the Option 3 recommendation

First-order: *Ship the two features natively now; run a bounded Flutter spike in parallel; commit or abandon at a dated checkpoint.*

**2nd-order effects:**

- →[2nd] The two native features must eventually be re-ported to Flutter, adding scope to any later migration. **Adverse.** `[Assumes: A12]`
- →[2nd] The spike converts GT-9? from an unknown into a measurement, so the eventual go/no-go is evidence-based rather than estimate-based. **Favourable.**
- →[2nd] Both codebases keep accruing duplicated feature cost during the deferral. **Adverse — this is the real price of Option 3, and it is not zero.** `[Assumes: A7]`
- →[2nd] The team is not subjected to a 7-month freeze, removing the attrition trigger. **Favourable.**

**3rd-order effects:**

- →[3rd] Re-port scope growth compounds: the longer the deferral runs without a decision, the more the eventual migration costs — meaning an *undated* deferral silently converts into Option 2 by default. This is why the checkpoint must carry a date and a pre-registered decision rule, not a review meeting.
- →[3rd] A successful spike on older devices makes the later migration's estimate materially more credible, tightening C2's bracket enough to satisfy its stop criterion.
- →[3rd] If the customer renews on the strength of two delivered features, the *next* window is a clean 12-month runway with no dated external constraint — structurally the best migration window you will get. **Favourable, and it is the strategic case for Option 3 over Option 1.**

**Contradiction check against Ground Truths:** none of the enumerated effects contradicts GT-1 through GT-11. No return to Phase 2 required. Stopping at 3rd order; a 4th layer here would be speculation about customer behaviour I have no ground truth for.

---

### Process output — Phase 4 end-of-phase Assumption Audit

| Chain | Step | Step text (brief) | Assumption surfaced? | Added to table? |
|---|---|---|---|---|
| C1 | 1 | Migration completes month 7 | A1 (already present) | — |
| C1 | 2 | Renewal commits months 5–7 | A3 → GT-8? (present) | — |
| C1 | 3 | Renewal falls inside stall | none | — clean |
| C2 | 1 | Target surface 60–75k LOC | Convergence of duplicated logic | Covered by A6 |
| C2 | 2 | 35 engineer-months budget | none (arithmetic) | — clean |
| C2 | 3 | Parity rewrite ≠ greenfield rate | A1 (present) | — |
| C2 | 4 | Bracket 7 / 10 / 14+ | A1, A8 | Both present |
| C3 | 1 | Older devices are the sensitive band | A5 (present) | — |
| C3 | 2 | Viability depends on unmeasured quantity | none | — clean |
| C4 | 1 | Option 3 assumes 3 engineers can ship 2 features | **A11 new** | **Yes** |
| C4 | 2 | Option 3 assumes spike yields decision-grade evidence | **A13 new** | **Yes** |
| C5 | 1 | Native features re-portable to Flutter | **A12 new** | **Yes** |
| C5 | 2 | Duplicated cost accrues during deferral | A7 (present) | — |
| C5 | 3 | Undated deferral degrades to Option 2 | none | — clean |

Three assumptions surfaced and were added to the Assumptions Table (A11, A12, A13). No duplicates created.

---

## 5. Abandoned Reasoning

**Path abandoned — "migrate one platform first, then the other."** Initially attractive as a risk-staged compromise: rewrite Android in Flutter, keep iOS native, converge later. Abandoned because it produces the worst of both structures — you run three codebases (native iOS, native Android in maintenance, Flutter) instead of two, and the consolidation savings that justify the whole exercise do not arrive until *both* platforms land. The staging reduces peak risk while more than doubling total duration. Recording it because it is the option most teams reach for at exactly this juncture, and the reason it fails is not obvious until you count codebases rather than platforms.

**Path abandoned — sizing the decision by revenue-at-risk.** I attempted to build a chain comparing expected migration savings against expected renewal loss. It required a revenue share for GT-5? that I do not have, and a churn probability I would have had to invent. Any number I produced would have been a false precision that made the analysis look more rigorous than it is. Dropped rather than fabricated — but note that **you can build this chain**, and if the biggest customer is >20% of revenue it will dominate everything above.

**Path not taken — comparing Flutter to React Native / KMP.** Out of scope: you asked whether to consolidate, not what to consolidate onto. Flagging only that C3's device-mix concern applies with different magnitudes to different frameworks (Kotlin Multiplatform, notably, shares logic while keeping native UI — which is the shape that most directly addresses GT-4). If the spike in C4 shows Flutter struggling on older devices, that is the branch to explore rather than abandoning consolidation entirely.

---

### Process output — Phase 5 pre-mortem

*Premise: it is 12 months from now. The plan failed. What caused it?*

1. **The deferral had no date.** The checkpoint slipped, then slipped again, and Option 3 quietly became Option 2 — three years of duplicated feature cost with no decision ever made. *(Clusters with C5's 3rd-order finding — this is the dominant failure mode, and it is organisational, not technical.)*
2. **The spike was a demo, not a test.** Someone built a beautiful Flutter screen on a modern device, everyone was impressed, and GT-9? was never actually answered. *(→ A13.)*
3. **The two features shipped, and the customer churned anyway** for reasons unrelated to features. *(→ GT-10? was never verified; the whole plan was optimised against an unconfirmed condition.)*
4. **The 3 residual engineers could not deliver two features in 6 months** because the features were larger than assumed. *(→ A11, never sized.)*
5. **An engineer left**, and the spike + feature work both slipped. *(Note: this risk is *lower* under Option 3 than Option 1 — the freeze is the bigger attrition trigger.)*

Would I have suppressed any of these in a group? **Item 1** — "our checkpoint will slip" is socially awkward to say in the meeting where the checkpoint is being set. It is also the highest-signal item on the list. Adversarially interrogated and retained.

**Structural weakness identified:** items 1, 2, 3, and 4 all share one root — *the plan depends on downstream discipline that nothing in the plan enforces.* The mitigation is not more analysis; it is pre-registering the checkpoint date, the spike's success criteria, and the feature scope **now**, before any of them can be renegotiated against results.

**Weak links flagged:**

- C1's dependency on GT-8? — verifiable this week, and it is the chain that carries the recommendation.
- C4's dependency on A11 (feature sizing) — verifiable in days.
- C3's dependency on GT-9? — that is what the spike is *for*; flagged as deliberately open, not as an oversight.

---

### Process output — §6→§4 closure ledger

- "Do not start the Flutter migration now" → chain C1, C2 ✓
- "Ship the two features natively first" → chain C4 ✓
- "Run a bounded older-device Flutter spike in parallel" → chain C3, C4 ✓
- "Set a dated checkpoint with a pre-registered decision rule" → chain C5 ✓
- "Deferral is not free" → chain C5 ✓
- "Verify the renewal decision date immediately" → chain C1 ✓
- "Flutter may still be the right destination" → chain C4 (long-run cost, score 5 for Option 1) ✓

Ledger clean — every §6 claim carries a chain reference.

---

## 6. Conclusion

**Recommendation: Option 3 — structured deferral. Do not start the migration now; do not settle into "keep both native" either.**

Concretely, for the next 9 months:

1. **Ship the two customer features natively, starting now.** This is the only option that keeps the renewal outside the risk window (C1, C4). Size them this week — if they are larger than 3 engineers can carry, that changes the plan (A11).

2. **Run a bounded Flutter spike in parallel — 2–3 engineer-weeks, no more.** Its job is to answer GT-9?, not to impress anyone. Target the *hardest* surface: your oldest supported device class, plus whichever native integration you most fear porting. A spike that ships a pretty demo on a flagship phone has told you nothing (C3, pre-mortem item 2).

3. **Set a dated checkpoint — I would put it at month 4–5 — with the decision rule written down before results arrive.** Something of the form: *"If the spike shows cold-start and frame-time within X% of native on the oldest supported device, and the two features have shipped, we commit to migration starting month 10."* Pre-registering the rule is what stops the deferral from silently becoming permanent (C5, pre-mortem item 1).

4. **Verify this week whether the renewal decision actually commits at month 9 or earlier** (GT-8?). It is one conversation, and it is the load-bearing input to C1.

**Confidence: MEDIUM-HIGH.** The recommendation *against consolidating now* is the robust part — it holds under every weighting I could justify in advance, and it is supported independently by the schedule collision (C1) and the estimate bracket (C2), so it does not rest on either alone. The recommendation *for* structured deferral over plain "keep native" is the softer part, at a 15% trade-off margin.

**What would change this.** If you verify that (a) the renewal decision truly lands at month 9 with no earlier evaluation, **and** (b) the two features are not renewal conditions, **and** (c) the customer is a modest revenue share — then C1 largely dissolves and consolidating now becomes defensible. All three would have to hold. Conversely, if the customer is a large revenue share and the features are conditions, Option 3 stops being merely preferable and becomes the only responsible choice.

**The honest cost of my recommendation:** Option 3 is not free. Every month both codebases stay alive, you pay duplicated feature cost, and each native feature you ship enlarges the eventual migration (C5, A7). What you are buying with that money is the conversion of a 35-engineer-month bet on an unmeasured premise into a 3-engineer-week measurement — and, if the renewal lands, a clean 12-month window with no dated external constraint, which is structurally the best migration conditions you are likely to see.

**Flutter may well be the right destination.** In the trade-off it scores highest of all options on long-run cost efficiency, and nothing in this analysis argues against it as a technology. The argument is entirely about *when* — and right now you would be starting the largest engineering commitment in your recent history seven months before a nine-month deadline, on a performance premise you have never tested against a third of your users.

---

### Rubric validation

| Criterion | Verdict | Evidence |
|---|---|---|
| Essence isolates the real question, not the trigger | PASS | §1 reframes technology-choice → sequencing-under-constraint; success criteria checkable |
| All assumptions classified by the four-type scheme | PASS | 13 rows, each typed and with a recorded verdict |
| Conventions explicitly challenged before use | PASS | A1 rejected, A5 challenged-unresolved, A6 partially rejected |
| Ground truths carry IDs, sources, `?` on unverified | PASS | GT-1…GT-11; GT-5?, GT-8?, GT-9?, GT-10? flagged |
| Every chain has ≥1 intermediate step | PASS | C1, C3, C5 shown with explicit intermediates; C2/C4 are procedural derivations |
| No analogy used as standalone evidence | PASS | GT-8? industry pattern is explicitly flagged unverified and never load-bearing without that caveat |
| Second-order pass run; contradictions checked | PASS | C5, contradiction check clean, stopped at 3rd order with stated reason |
| Assumption audit run; new assumptions added | PASS | Audit table; A11/A12/A13 added |
| Weak links resolved or flagged with caveats | PASS | Three flagged in Phase 5 with verification cost stated |
| Conclusions inherit confidence caveats from `GT-N?` inputs | PASS | MEDIUM-HIGH on C1, MEDIUM on C3, explicit "what would change this" |
| Abandoned reasoning recorded, not hidden | PASS | §5, including a path abandoned for lack of data rather than fabricating numbers |
| §6 claims all trace to §4 chains | PASS | Closure ledger, 7/7 clean |

Gate cleared on first pass; no Fix iteration required, so no ledger re-verification was needed.

═══════════════════════════════════════════════════════════════════════════════
DOCUMENT Q-N4  (source: tests/quality-baseline-v8.10-oos/analyses/Q-N4.md)
═══════════════════════════════════════════════════════════════════════════════

## Process output — Assumption Audit (Phase 4, end-of-phase scan)

| Chain | Step | Step text (brief) | Assumption surfaced? | Added to Table? |
|---|---|---|---|---|
| C1 | 1 | 81,900 WC orders/yr × $3.10 | 3PL rate is all-in (no accessorials/storage/receiving) | Yes → A-9 |
| C1 | 2 | → 3PL = $253,890/yr | Rate holds at this volume tier | Yes → A-10 |
| C2 | 1 | $420k lease is facility-only | Lease figure excludes labor | Yes → A-4 |
| C2 | 2 | 8 hires × fully-loaded cost | Fully-loaded ≈ 1.3× base | Yes → A-5 |
| C2 | 3 | + other opex (WMS, MHE, utilities, shrink) | Omitted-cost line exists and is non-zero | Yes → A-6 |
| C2 | 4 | → ~$1.0M/yr, ~$12.20/order | — (clean) | n/a |
| C3 | 1 | per-head throughput ~32,500 orders/yr | Pick/pack productivity benchmark | Yes → A-7 |
| C3 | 2 | fixed $520k + $1.85/order variable | Lease/overhead does not step up with volume | Yes → A-11 |
| C3 | 3 | → breakeven V ≈ 416,000 orders/yr | — (clean) |  n/a |
| C4 | 1 | split diverts volume from fixed-cost node | No fixed-cost reduction available at half scale | Yes → A-12 |
| C4 | 2 | → split dominated on cost | — (clean) | n/a |
| C5 | 1 | 5pp return-rate deterioration scenario | Return handling ≈ $15–25 each | Yes → A-8 |
| C5 | 2 | → ~$82k/yr vs $746k/yr gap | Control damage is bounded and quantifiable | Yes → A-13 |
| C1 | →[2nd] | 3PL dependency / renewal pricing | Provider has pricing power at renewal | Yes → A-14 |
| C3 | →[2nd] | 3-year lease locks ~$1.26M | Growth is unquantified | Yes → A-2 (existing) |

---

# 1. Problem Essence

**Core question:** At current and near-term west-coast volume, which fulfillment structure delivers 2-day west-coast delivery at the lowest total cost per order without foreclosing future options?

This is not "do we want a west-coast warehouse." It is a **capacity-utilization decision under demand uncertainty**: a warehouse is a large fixed cost that only beats a per-unit price above a threshold volume. The triggering event (growth) is not the question; the question is whether current volume clears that threshold.

**Success criteria** (checkable against the conclusion):
1. Both options deliver the stated 2-day west-coast SLA.
2. Total annual cost is compared on a like-for-like basis (all-in, not lease-vs-rate).
3. The volume at which the ranking flips is stated numerically.
4. The commitment's reversibility under demand uncertainty is addressed.
5. The non-cost factor (packaging/returns control) is priced, not asserted.

---

# 2. Assumptions Table

| # | Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|---|
| A-1 | 35% of 4,500/wk = 1,575 WC orders/wk | current constraint | Expires if mix shifts | Accepted | Given |
| A-2 | "Growing" — rate unquantified | untested belief | Verify or flag | **UNVERIFIED — flagged** | Needs 8-quarter WC trendline |
| A-3 | Both options meet 2-day SLA | current constraint | Recorded as stated | Accepted | Given; 3PL side needs contractual SLA |
| A-4 | $420k/yr is facility-only, excludes the 8 hires | untested belief | Verify | **UNVERIFIED — flagged**; analysis run both ways | Read the lease term sheet |
| A-5 | Fully-loaded warehouse labor $50–70k/head | untested belief | Bracketed | Flagged with range | Regional comp data |
| A-6 | Startup + running opex beyond lease/labor is non-zero (WMS, racking, MHE, utilities, insurance, shrink) | physical law–adjacent (definitional: a warehouse cannot operate on rent alone) | Accept as ground-truth candidate | Accepted | Structurally necessary |
| A-7 | ~125 orders/person/day pick-pack-ship | untested belief | Bracketed 80–150 | Flagged with range | Industry benchmark |
| A-8 | Return handling ≈ $15–25 per return | untested belief | Bracketed | Flagged | Own current returns cost |
| A-9 | $3.10 is all-in (no receiving/storage/accessorial) | **convention — challenged** | 3PL quotes conventionally exclude storage and inbound | **Likely FALSE as stated** | Demand a fully-burdened quote |
| A-10 | $3.10 holds at 81,900/yr | convention | Challenge | Probably tier-dependent | Get the rate card |
| A-11 | Lease/overhead is flat across relevant volume | current constraint | Expires at facility capacity | Accepted in range | Sq-ft capacity check |
| A-12 | No half-size facility option exists at ~half cost | untested belief | Verify | **UNVERIFIED** | Test smaller-footprint quotes |
| A-13 | Control loss is bounded (returns + packaging quality) | untested belief | Verify | Flagged — brand damage is not fully bounded | See §5 |
| A-14 | 3PL has renewal pricing power once you depend on it | convention → verified pattern | Challenge, then mitigate contractually | Accepted as a risk to price in | Structural |
| A-15 | Only two structures exist (build / 3PL / 50-50) | **convention — challenged and REJECTED** | Challenge before use | **FALSE** — asymmetric hybrid exists | See §6 |

**Inversion pass (what would guarantee the 3PL recommendation is wrong):** (i) $3.10 is not all-in and true landed cost is 2–3×; (ii) WC volume is on a trajectory to 5× within the lease term; (iii) a control-critical revenue segment exists whose loss exceeds $746k/yr; (iv) the 8 hires are already inside the $420k; (v) no 3PL will contract for 2-day SLA with penalties. Each is now a row above.

---

# 3. Ground Truths

- **GT-1:** 1,575 WC orders/week = **81,900/year**. (4,500 × 0.35 × 52; arithmetic from given figures.)
- **GT-2:** 3PL quoted rate = **$3.10/order** (as stated; scope caveat A-9).
- **GT-3:** Warehouse lease = **$420,000/year × 3 years = $1,260,000 committed**.
- **GT-4:** Warehouse requires **8 new hires**.
- **GT-5?:** Fully-loaded labor $50–70k/head → **$400k–$560k/yr** (unverified, bracketed).
- **GT-6?:** Non-lease, non-labor opex **$60k–$150k/yr** plus **$200k–$600k one-time fit-out** (unverified, bracketed; structurally necessary per A-6).
- **GT-7?:** Throughput **~32,500 orders/head/year** (125/day × 260 days) (unverified, bracketed 80–150/day).
- **GT-8?:** Return handling **$15–25 each** (unverified).
- **GT-9:** A fixed cost divided by volume falls monotonically as volume rises — **definitional**, not empirical. This is the load-bearing structural truth of the whole analysis.
- **GT-10:** A 3-year lease plus 8 employment relationships is **materially harder to reverse** than a logistics contract. (Definitional: real property leases and employment carry exit costs; a service contract's exit cost is set by its term.)

---

# 4. Derivation Chains

**C1 — 3PL annual cost**
GT-1 + GT-2 → 81,900 × $3.10 → **3PL ≈ $254,000/yr, fully variable**. *(Confidence: HIGH on arithmetic, MEDIUM on scope — depends on A-9.)*
→[2nd] Dependence on a single provider grows with tenure; renewal leverage shifts to them [Assumes: A-14].
→[3rd] Switching cost (re-integration, inventory transfer) rises each year → mitigate now via term length, exit clause, and data-ownership terms, not later.

**C2 — In-house annual cost**
GT-3 + GT-4 + GT-5? + GT-6? → $420k + $480k (central) + $100k (central) → **≈$1.0M/yr [bracket: $880k – $1.13M]**, plus $200–600k one-time → **≈$12.20/order at current volume** → **in-house costs ≈$746k/yr more than the 3PL today**, i.e. a **~$9.10/order control premium**. *(Confidence: MEDIUM-HIGH — the bracket's lower bound $880k still exceeds $254k by 3.5×, so both ends drive the same decision. If A-4 is false and $420k is all-in, in-house is still $420k vs $254k — same direction.)*

**C3 — Breakeven volume**
GT-9 + GT-3 + GT-6? (fixed ≈ $520k) + GT-7? (variable labor ≈ $1.85/order) → cost/order = $520,000 ÷ V + $1.85 → set equal to $3.10 → $520,000 ÷ V = $1.25 → **V ≈ 416,000 orders/yr ≈ 8,000 WC orders/week** → **breakeven requires ~5× current west-coast volume — nearly 2× the company's entire current order book (4,500/wk)**. *(Confidence: MEDIUM — sensitive to GT-7?. At the pessimistic 80 orders/day the breakeven rises further; at the optimistic 150/day it falls to ~5,900/wk, still 3.7× current. The bracket does not straddle the decision threshold.)*
→[2nd] The 3-year lease commits $1.26M against a growth rate that is **unquantified** [Assumes: A-2] — the commitment's term exceeds the horizon over which the growth assumption is verified.

**C4 — The split option**
C2 + C3 + GT-9 → a 50/50 split routes ~40,950 orders/yr through a node carrying the **full** $520k fixed cost → in-house cost/order rises to **≈$14.55**, worse than the unsplit $12.20 → **the split is dominated on cost by the pure 3PL option and dominated on control by the pure build option** [Assumes: A-12 — no proportionally smaller facility available]. *(Confidence: HIGH, conditional on A-12.)*

**C5 — Pricing the control gap**
C2 + GT-8? → worst-case 5pp return-rate deterioration = 4,095 extra returns × $20 → **≈$82k/yr** → the modelled control damage is **~9× smaller than the $746k cost gap** → **control considerations alone cannot justify the build at current volume**. *(Confidence: MEDIUM — bounds the *measurable* control cost. Unmeasured brand/repeat-purchase damage is not captured [Assumes: A-13]; see §5.)*
→[2nd] Poor 3PL packaging degrades unboxing → repeat-purchase rate → this is the one channel through which control loss could plausibly reach $746k, and it is **not** bounded by C5 → therefore it must be handled contractually (packaging spec, mystery-shop audits, SLA penalties), not waved away.
**Contradiction check:** no second-order effect contradicts GT-1, GT-3, GT-9, or GT-10. No return to Phase 2 required beyond the rows already added.

---

# 5. Abandoned Reasoning

- **"Do it in-house to build a strategic capability asset."** Abandoned as an *analogy-based* argument (Amazon built its own network, therefore we should). Amazon's ground truth was volume 4+ orders of magnitude above GT-1; the analogy transfers no verified fact about *this* situation. Rejected per the no-analogy-as-evidence rule.
- **Straight 50/50 split.** Pursued seriously through C4 and abandoned on the arithmetic: it worsens the very ratio that makes the build unattractive.
- **Cost-per-order-only framing.** Abandoned mid-analysis as insufficient — it cannot price irreversibility (GT-10) or lock-in, which is why C1/C3 carry second-order extensions rather than stopping at the dollar figures.
- **Bounding brand damage.** Attempted in C5 and **explicitly not completed** — repeat-purchase elasticity to packaging quality is not knowable from available data. Flagged rather than fabricated.

---

## Process output — §6→§4 closure ledger

- "Use the 3PL" → chain **C1 + C2** ✓
- "Warehouse is ~$746k/yr more expensive today" → chain **C2** ✓
- "Breakeven needs ~8,000 WC orders/week" → chain **C3** ✓
- "The 50/50 split is dominated" → chain **C4** ✓
- "Control alone doesn't justify the build" → chain **C5** ✓
- "Contract for optionality, not lowest rate" → chain **C1 →[2nd]/[3rd]** ✓
- "An asymmetric hybrid may be worth testing" → chain **C4 + A-15 rejection** ✓
- ~~"3PLs generally deliver better unit economics at small scale"~~ → **CUT** (no chain; unsupported generalization removed)

---

# 6. Conclusion

**Use the 3PL. Do not build the warehouse. Do not split 50/50.**

**The decisive number:** the warehouse breaks even against $3.10/order at roughly **8,000 west-coast orders per week**. You have **1,575**. You would need to grow west-coast volume ~5× — to nearly double your entire current company throughput — before the build pays for itself, and you would be committing $1.26M of lease plus 8 jobs for three years to a growth rate you have not quantified (A-2).

**The gap is not close.** In-house runs ≈$1.0M/yr [$880k–$1.13M] against ≈$254k for the 3PL — about **$9.10 per order** you would be paying for control. Modelled worst-case control damage (a 5-point return-rate deterioration) is ≈$82k/yr, roughly one-ninth of that premium. Even under the most warehouse-favourable reading of your figures (if $420k already includes the 8 hires), the ranking does not flip.

**The split is the worst of the three.** Half the volume through a facility carrying full fixed cost pushes in-house unit cost *up*, to ≈$14.55/order, while still not giving you the end-to-end control the build was supposed to buy.

**What to do instead of just signing:**

1. **Verify A-9 before anything else.** Get a fully-burdened 3PL quote — receiving, storage, accessorials, returns processing, peak surcharges. $3.10 is conventionally a pick-pack rate. If the landed rate is materially higher, re-run C3; the decision would still favour the 3PL, but the margin matters for term negotiation.
2. **Buy optionality, not the lowest rate.** Negotiate a **2-year term (not 3+)**, volume-tiered pricing with a step-down, contractual 2-day SLA with penalties, a defined packaging specification with audit rights, returns-data ownership, and a clean exit/transition clause. The second-order analysis says your leverage is highest now and decays with every month of dependence.
3. **Pre-register the revisit trigger.** Re-open the build decision when west-coast volume sustains **≥6,000 orders/week** for two consecutive quarters, or if audited 3PL packaging/returns quality breaches the SLA. Write the number down now, before you have a result you want to justify.
4. **Test the option this analysis rejected as a false binary (A-15).** A 50/50 split is dominated — but an *asymmetric* hybrid is not the same thing: 3PL for standard volume, with a control-critical segment (subscription boxes, high-AOV, custom packaging) retained in your existing facility and shipped west at higher transit cost. That requires no second lease and no 8 hires. Whether it's worth it depends on whether such a segment actually exists in your order mix — which is a data question you can answer this week.

**Confidence:** HIGH that the 3PL beats the build at current volume (every bracket end drives the same decision). MEDIUM on the precise breakeven point (sensitive to unverified GT-7?). The single assumption that could most change this is **A-9** — if $3.10 is not the real all-in rate, verify it before signing anything.

═══════════════════════════════════════════════════════════════════════════════
DOCUMENT Q-N6  (source: tests/quality-baseline-v8.10-oos/analyses/Q-N6.md)
═══════════════════════════════════════════════════════════════════════════════

## Scope note before the analysis

One input is missing that changes exactly one conclusion: **jurisdiction**. The dollar figures and "CBCT" suggest a US practice, and the shared-referral chain (C4) below is derived under that assumption. If you are outside the US, treat C4 as unverified and substitute your local self-referral/inducement rules — every other chain is jurisdiction-independent. I proceeded rather than blocking because the primary answer does not depend on it.

**Step 0 — technique selection:** No focused-technique trigger phrase fired. `MODE = full-composer`. All five phases run; Phase 4 walks the eight companion techniques.

---

# 1. Problem Essence

**Essence Statement:** Does the contribution margin recoverable from scans you currently refer out exceed the full cost of owning the capacity to produce them — and is that margin robust enough to survive being wrong about how many referrals you can actually keep?

Success criteria for a correct answer:

- [ ] States a break-even scan volume, not just a payback period
- [ ] Distinguishes the volume you *send out* from the volume you can *keep in-house*
- [ ] Treats the neighboring-practice offer at its actual structural role, not as stated
- [ ] Names what would have to be measured to move the answer from "probably" to "yes"

**Reframe applied.** The question as posed is "buy / refer / explore" — three options. The analysis below finds that is not the real structure (see Abandoned Reasoning §5.2). The essence also strips out one framing artifact immediately: *"the machine would sit idle much of the week"* is presented as a cost. It is not one. See chain C2.

---

# 2. Assumptions Table

| # | Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|---|
| A1 | $110,000 capital cost is complete | current constraint | Record expiry conditions | **Likely incomplete** | Quoted price typically excludes room shielding/lead lining, electrical, operatory downtime, staff certification, and software licensing. Ask the vendor for an all-in installed figure. |
| A2 | $9,000/yr covers all recurring cost | current constraint | Record expiry conditions | **Likely incomplete** | Omits radiologist overread fees (see A9) and staff chair-time. Expires if you contract a teleradiology service. |
| A3 | All 25 monthly referrals are convertible to in-house scans | untested belief | Verify or flag | **UNVERIFIED — load-bearing** | Some referrals go out for specialist *interpretation*, patient insurance steering, or surgical co-treatment — not because you lack a machine. This is the single highest-stakes unverified input in the analysis. |
| A4 | $180/scan is net revenue | untested belief | Verify or flag | **False as stated** | $180 is gross. Reclassified to contribution margin ≈$140 in GT-3. |
| A5 | Machine useful life ≈7 years | convention | Challenge before use | **Accepted with caveat** | 7 yrs is the conservative end of the 7–10 yr industry/depreciation convention. Sensor and software obsolescence, not mechanical failure, usually sets the real horizon. Conservative choice favors the "don't buy" side — appropriate. |
| A6 | Purchase is cash, not financed | untested belief | Verify or flag | **Assumed** | Financing at ~8%/5yr adds ~$24k total interest. Changes timing and magnitude, not the sign of the answer. |
| A7 | Neighbor's offer is firm and durable | untested belief | Verify or flag | **UNVERIFIED** | A verbal offer from a party with no contractual exposure. Treated as zero-value in the base case. |
| A8 | Referral volume is stable at 25/mo | untested belief | Verify or flag | **Assumed** | Derived from your own stated average; seasonality and case-mix drift not modeled. |
| A9 | You can interpret the full CBCT field of view | untested belief | Verify or flag | **UNVERIFIED — surfaced by C5** | Owning the scan creates a duty of care over the *entire* imaged volume, including incidental findings outside the dental region of interest. Either a dentist takes that liability or you pay per-scan overread. |
| A10 | Stopping referrals has no cost | untested belief | Verify or flag | **False — surfaced by C5** | Specialist referral relationships are frequently reciprocal. |
| A11 | US jurisdiction | untested belief | Verify or flag | **ASSUMED — flagged** | Governs C4 only. |
| A12 | Scan indications stay constant post-purchase | untested belief | Verify or flag | **UNVERIFIED — surfaced by C5** | Owning imaging capacity reliably increases ordering rates ("indication creep"). Cuts both ways: revenue up, dose-stewardship and payer-scrutiny exposure up. |

**Inversion pass** (what would guarantee this purchase fails): capture rate below ~60%; overread fees materially eroding the $180; the neighbor deal evaporating after purchase; a reciprocity collapse costing more inbound patients than the scans earn; obsolescence before year 7. A3, A7, A9, A10 above are the preconditions those failure modes attack — each is currently unverified.

**Fishbone pass** (cause categories for "referrals leave the practice"): *People* — dentist comfort with 3D interpretation; *Process* — referral is habitual, not clinical; *Technology* — no machine (the assumed cause); *Information* — specialist wants their own imaging protocol; *Resources* — chair time; *Environment* — insurance networks steering the patient. Only the *Technology* branch is fixed by buying a machine. This is the direct source of A3's doubt.

---

# 3. Ground Truths

- **GT-1:** Capital outlay ≈$110,000, quoted (user-supplied; understated per A1).
- **GT-2:** Recurring cost ≈$9,000/yr, quoted (user-supplied; understated per A2).
- **GT-3?:** Contribution margin per scan ≈**$140** (bracket $100–$180). Derived: $180 gross, less ~$20–40 loaded staff/chair time, less $0–60 optional overread. *Unverified — depends on your overread decision.*
- **GT-4:** ~25 CBCT referrals leave the practice monthly (user-supplied, direct measurement).
- **GT-5:** Four dentists share the practice (user-supplied).
- **GT-6?:** Useful life ≈7 years (convention, conservative end — A5).
- **GT-7:** *Definitional:* fixed costs accrue per unit of time, not per unit of use. Idle hours generate no incremental cash cost.
- **GT-8:** *Derived from GT-7:* marginal cash cost of one additional scan on an owned machine ≈ staff time only, near zero relative to the $180 fee.
- **GT-9?:** Under US federal law (Anti-Kickback Statute; Stark Law where applicable), remuneration exchanged between providers in connection with patient referrals is restricted, and arrangements structured as per-referral or volume-linked value transfer carry criminal and civil exposure. *Conditional on A11.*
- **GT-10:** *Irreducibility drill on "the machine pays for itself":* reduces to → (scans captured/mo) × (contribution/scan) × 12 ≥ (capital ÷ life) + (annual fixed). Every term bottoms out at a measurement or a definition. No further reduction available.

---

# 4. Derivation Chains

### C1 — The break-even volume, not the payback period *(estimate / Fermi)*

Target quantity: **scans per month required to break even**, units = scans/month.

Unit cancellation: `($/yr required) ÷ ($/scan) ÷ (12 mo/yr) → scans/month` ✓

Annualized capital recovery, undiscounted: $110,000 ÷ 7 yr = **$15,714/yr**
At an 8% cost of capital (7-yr annuity factor 5.206): $110,000 ÷ 5.206 = **$21,130/yr**

> **GT-1 + GT-2 + GT-6? + GT-3? → required annual contribution = $15,714–$21,130 (capital) + $9,000 (fixed) = $24,714–$30,130 → ÷ $140/scan ÷ 12 → break-even ≈ 15–18 scans/month → you must retain 60–72% of your existing 25 monthly referrals just to reach zero.**

Full bracket on annual net cash:

| Scenario | Capture | Contribution | Fixed | Annual net | Payback |
|---|---|---|---|---|---|
| Conservative | 12/mo (48%) | $100 | $15,000 | **−$600** | never |
| Central | 18/mo (72%) | $140 | $9,000 | **+$21,240** | 5.2 yr |
| Aggressive | 25/mo (100%) | $180 | $9,000 | **+$45,000** | 2.4 yr |

**Stop-criterion result: FAILED.** The decision-resolution rule requires both bracket ends to drive the same decision. They do not — the lower end loses money over the machine's entire life while the upper end pays back in under two and a half years. The dominant uncertain factor is capture rate (A3). Per the procedure, this escalates: **tighten that factor with a measurement before deciding.** Confidence: **HIGH** in the break-even band, **LOW** in which side of it you land on.

### C2 — Idle time is not a cost

> **GT-7 + GT-8 → the machine's fixed cost is identical whether it runs 4 hours a week or 40 → utilization is not a term in the break-even equation → "it would sit idle much of the week" is emotionally salient and economically irrelevant.**

The only question idle capacity raises is whether *filling* it (i.e., the neighbor) is a legitimate route to volume — which is C4's problem, not a cost problem. Confidence: **HIGH**.

### C3 — What the neighbor's offer actually is

> **GT-6? (offer is verbal, non-binding, from a party with no exposure) + C1 (base case is uncomfortably near break-even) → the offer's function is to make a marginal purchase look clearly positive → an unenforceable input is doing load-bearing work in a $110,000 decision → the offer must be valued at zero in the base case and treated strictly as upside.**

If the deal is real and legal, it plausibly adds 10–20 scans/month, which would push you decisively clear of break-even. That is precisely why it must be verified *before* it influences the purchase, not after. Confidence: **HIGH**.

### C4 — The shared-referral arrangement is the highest-risk element, not the safest *(conditional on A11)*

> **GT-9? + C3 → an arrangement in which one practice directs patients to another practice's revenue-generating equipment is the exact fact pattern federal referral law scrutinizes → "explore the shared-referral arrangement" is not a low-commitment first step; it is the step requiring counsel before any money moves → [Assumes: A11 — US jurisdiction].**

This does not mean the arrangement is unlawful. Compliant structures exist (fair-market-value per-scan technical fees set in advance, not varying with volume or value of referrals; written agreements of at least one year; safe-harbor-conforming terms). It means the structure must be designed by a healthcare attorney rather than agreed over coffee. Confidence: **MEDIUM** (HIGH on the need for counsel; LOW on the outcome, which depends on structure and state law).

### C5 — Second-order consequences

Applying the second-order pass to the C1 conclusion ("buying is marginally positive at central assumptions"):

**2nd-order effects:**
1. Referrals to oral surgeons/endodontists drop → those specialists' reciprocal inbound referrals to you may drop `[Assumes: A10]`
2. In-house availability increases scanning frequency beyond current clinical indications `[Assumes: A12]`
3. You acquire a duty of care over the full imaged volume, including non-dental incidental findings `[Assumes: A9]`
4. The neighbor practice becomes operationally dependent on your equipment uptime

**3rd-order effects:**
1a. Net patient flow could decline even as scan revenue rises — a reciprocity loss of even 2–3 restorative or surgical cases per month can exceed $2,000/mo in production, dwarfing the ~$1,700/mo net scan contribution
2a. Higher scan volume → cumulative patient dose stewardship obligations, malpractice exposure on over-ordering, and payer utilization scrutiny
3a. Duty over the full FOV means either a dentist reads regions outside their training (liability) or you pay $25–60/scan for radiologist overread (**this is what reduces GT-3? from $180 to ~$140 — the effect feeds directly back into C1's dominant term**)
4a. Equipment downtime becomes a relationship failure, not just an internal inconvenience

**Contradiction check:** effect 3a materially undercuts the naive $180/scan premise. Per the routing rule, this returned to Phase 2 for re-challenging — A4 was reclassified as **false as stated** and GT-3? was rebuilt at $140. No remaining effect contradicts a ground truth. Confidence: **MEDIUM** on magnitudes, **HIGH** on direction.

### C6 — Weighted trade-off *(weights locked before scoring)*

Options: **(1)** Buy now · **(2)** Keep referring indefinitely · **(3)** Measure and clear the two unknowns first, then decide

| Criterion | Wt | Opt 1 | Opt 2 | Opt 3 |
|---|---|---|---|---|
| Expected 7-yr net cash | 5 | 4 | 2 | 4 |
| Downside protection / reversibility | 4 | 2 | 5 | 5 |
| Legal & regulatory safety | 5 | 3 | 5 | 5 |
| Diagnostic quality & speed of care | 3 | 5 | 2 | 3 |
| Specialist relationship preservation | 2 | 2 | 5 | 4 |
| Decision speed / cost to pursue | 2 | 4 | 5 | 3 |
| Information gained on the key unknown | 4 | 2 | 1 | 5 |
| **Weighted total** | | **78** | **85** | **108** |

**Sensitivity check:** Options 1 and 2 sit within 9% of each other — a genuine near-tie, meaning *buying now and never buying are roughly equally defensible on today's information*. That near-tie is itself the finding: it is what makes the information criterion decisive. Option 3 clears both by >25%; no weight adjustment flips it.

> **C1 (bracket straddles the threshold) + C3 (key input unenforceable) + C4 (legal structure unresolved) → the two decisive unknowns are both cheap to resolve and expensive to be wrong about → measuring first strictly dominates → Option 3.**

Confidence: **HIGH**.

### Assumption Audit (end-of-Phase-4 scan)

| Chain | Step | Step text (brief) | Assumption surfaced? | Added to table? |
|---|---|---|---|---|
| C1 | 1 | Annualized capital recovery | Useful life = 7 yr | Already present (A5) |
| C1 | 2 | ÷ $140/scan | Contribution ≠ gross fee | Already present (A4) |
| C1 | 3 | Break-even 15–18/mo | Capture rate unknown | Already present (A3) |
| C1 | 4 | Bracket table | Cash purchase | Already present (A6) |
| C2 | 1 | Fixed cost time-invariant | — | Clean pass |
| C2 | 2 | Utilization not a term | — | Clean pass |
| C3 | 1 | Offer non-binding | Offer durability | Already present (A7) |
| C3 | 2 | Value at zero in base case | — | Clean pass |
| C4 | 1 | Federal referral law applies | **Jurisdiction** | **Added — A11** |
| C4 | 2 | Counsel required pre-commitment | — | Clean pass |
| C5 | 2a | Reciprocity loss | **Referral reciprocity** | **Added — A10** |
| C5 | 2b | Indication creep | **Ordering-rate stability** | **Added — A12** |
| C5 | 2c | Full-FOV duty of care | **Interpretation competence/liability** | **Added — A9** |
| C5 | 3a | Overread fee feeds back to GT-3? | — | Routed to Phase 2; A4 reclassified |
| C6 | 1 | Weights locked pre-scoring | — | Clean pass |
| C6 | 2 | Option 3 dominates | — | Clean pass |

---

# 5. Abandoned Reasoning

**5.1 — Utilization framing.** The initial framing treated "sits idle much of the week" as a cost to be offset. Abandoned at C2: idle capacity is a psychological cost, not a cash cost, and including it would have biased the analysis toward chasing volume (the neighbor deal) for its own sake. This is the exact reasoning error the neighbor's offer is positioned to exploit.

**5.2 — Three-option framing.** The question presents buy / refer / share as parallel alternatives. Abandoned: the shared-referral arrangement is not an alternative to buying — it is a *volume modifier on the buy option* that only has value if you own a machine. Recognizing this collapses the decision to buy-vs-don't with a contingent upside, which is what made C6's third option (measure first) constructible.

**5.3 — Lease-vs-buy.** Explored and set aside. Financing changes the timing and total cost (~$24k interest at 8%/5yr) but does not change the sign of the answer or the break-even volume materially. It becomes relevant *after* the capture-rate question is settled, not before.

**5.4 — Reasoning from "most practices this size own one."** Rejected as analogy. Any comparable practice's decision would only be evidence if their capture rate and case mix were verified — at which point their capture rate, not their decision, is the useful datum.

---

# 6. Conclusion

**Do not buy yet, and do not walk away. Spend 30–60 days and a few hundred dollars closing the two unknowns that the whole decision rests on** *(chain C6)*.

Concretely:

1. **Audit your last 75–100 referrals** (three to four months) and tag each with the *actual* reason it left the building: no machine · specialist interpretation needed · surgical co-treatment · insurance steering · patient preference. Only the first category converts. **Your break-even is 15–18 scans/month — 60–72% capture** *(chain C1)*. If the audit shows you'd retain 20+, buy without further deliberation. If it shows 12 or fewer, the machine loses money over its entire life and the answer is a clean no. Between 15 and 18, it is a coin flip on financial grounds and you should decide on clinical and strategic grounds instead.

2. **Get a healthcare attorney's read on the neighbor arrangement before it influences the purchase.** It is the most legally exposed element here, not the safest first step, and it is currently doing load-bearing work in a $110,000 decision on the strength of a verbal offer *(chains C3, C4)*. Structure it as a fair-market-value technical fee fixed in advance and independent of volume, or not at all.

3. **Settle the overread question in the same window.** Whether a dentist reads the full field of view or you pay a radiologist per scan is what moves your per-scan contribution between $100 and $180 — the second-largest lever in the model, and one you control by choosing *(chain C5)*.

Two things the model deliberately does not count, both of which favor buying: incremental case acceptance on implant and endodontic treatment made possible by same-day 3D imaging, and the patients you stop losing to specialists who retain them. If your referral audit lands near break-even, these are the reasons to lean yes. Against them, weigh the reciprocity loss from specialists you stop feeding *(chain C5)* — a decline of two to three restorative cases a month can quietly exceed the entire scan contribution.

**The single sentence:** your decision hinges on one number you have never measured, that number is cheap to measure, and the machine will still be for sale in sixty days.

---

<details>
<summary><b>Process output — §6→§4 closure ledger and rubric pass</b></summary>

**Closure ledger (every §6 claim → its §4 chain):**

- "Do not buy yet, do not walk away; measure first" → chain **C6** ✓
- "Break-even is 15–18 scans/month, 60–72% capture" → chain **C1** ✓
- "Neighbor offer is load-bearing on a verbal commitment" → chain **C3** ✓
- "Legal structure must precede purchase influence" → chain **C4** ✓
- "Overread decision moves contribution $100–$180" → chain **C5** ✓
- "Reciprocity loss can exceed scan contribution" → chain **C5** ✓
- "Idle time is not a reason against buying" → chain **C2** ✓ *(carried implicitly in §6's framing; chain present)*
- ~~"Most comparable practices own one"~~ → **CUT** (analogy, no chain — removed at §5.4)

Ledger clean; no §6 claim survives without a named chain. Re-verified after the Fix pass below; no chain was renamed or merged.

**Rubric pass:** Essence names a question distinct from the one asked (reframed from three-option to two-option-plus-measurement) ✓ · All four assumption types represented, treatments applied ✓ · Ground truths carry IDs, `?` flags on GT-3/6/9 ✓ · Every chain has ≥1 intermediate step ✓ · Second-order pass ran and one effect (3a) routed back to Phase 2, reclassifying A4 ✓ · Assumption audit ran, four assumptions added (A9–A12) ✓ · Weakest link identified and flagged: **A3, capture rate** — it is the load-bearing unverified input, it is explicitly named as such, and the entire recommendation is structured around verifying it rather than assuming past it ✓ · Estimate stop-criterion honestly reported as FAILED rather than papered over ✓ · Abandoned reasoning non-empty and substantive ✓ · Jurisdiction gap disclosed at the top rather than silently assumed ✓

Gate cleared.

</details>