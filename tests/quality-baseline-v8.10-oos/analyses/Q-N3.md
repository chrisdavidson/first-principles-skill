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