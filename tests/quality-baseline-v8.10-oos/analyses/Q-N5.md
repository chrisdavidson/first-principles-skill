## Missing information (stated, not silently assumed)

`AskUserQuestion` is unavailable in this session, so per the input contract I'm naming the gap and proceeding with a best-effort analysis rather than blocking.

One input would change the ranking of the two finalists: **which specific roles you're targeting.** "ML research scientist / applied scientist at a large lab" and "ML engineer / MLOps at a product company or startup" have materially different screens. The analysis below carries this as `GT-12?` and shows exactly where the answer flips. Everything else in your prompt is workable as given.

---

# First-Principles Analysis: Master's vs. Self-Study for an Analyst→ML Transition

**MODE:** `full-composer` (no focused-technique trigger phrase fired; "Should I pursue X, Y, or some combination?" is a holistic decision prompt, not a request for a named technique).

---

## 1. Problem Essence

**Essence Statement:** *What is the cheapest way to buy past whichever screen actually gates the ML roles I want — and is that screen the credential, the shipped work, or neither?*

Note what this is **not**. The triggering question was "master's, self-study, or combination?" That framing presupposes the credential's price is fixed at $46,000 and that the two signals compete for one budget. Both presuppositions are challenged in Phase 2, and one of them does not survive.

**Success criteria** (each is a pass/fail scan of the Conclusion section):

1. The conclusion **names which screen is binding** for the target roles, or names the specific fact that must be checked to determine it.
2. The conclusion **compares options on dollars-per-percentage-point of transition probability**, not on absolute cost.
3. The conclusion **allocates the ~1,560-hour budget explicitly** across both paths, treating it as one conserved resource.
4. The conclusion **states what happens if the transition fails**, not only the success case.
5. The conclusion **presents at least one option not contained in the original two.**

---

## 2. Assumptions Table

| # | Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|---|
| A1 | $46,000 is the price of an accredited part-time ML/CS master's | convention | Challenge before use | **Discard** — the figure is a property of one program's price point, not of the credential class | Accredited online CS/ML master's programs (Georgia Tech OMSCS, UT Austin MSCSO/MSDSO) list total tuition in the ~$7k–$12k range as of my Jan 2026 cutoff. Confirm current tuition pages directly → `GT-3` |
| A2 | The master's and self-study paths are mutually exclusive | convention | Challenge before use | **Discard** — mutual exclusivity follows only from A1's price, not from the time budget | A ~10 hr/wk program inside a 15 hr/wk budget leaves ~5 hr/wk for shipping → `GT-2`, `GT-6` |
| A3 | 15 hrs/week is sustainable on top of full-time work for 104 consecutive weeks | untested belief | Verify, or flag as unverified | **Challenge** — plausible but unproven for you specifically, and load-bearing | unverified — flagged → `GT-7?` |
| A4 | Employers weigh credentials and shipped work additively on one scale ("partly… partly…") | untested belief | Verify, or flag as unverified | **Discard** — hiring pipelines are sequential and conjunctive, not additive; the two signals are read by different people at different stages | Structural property of corporate hiring: ATS/recruiter screen precedes hiring-manager work-sample evaluation → `GT-4` |
| A5 | A portfolio will actually be read | untested belief | Verify, or flag as unverified | **Challenge** — conditional on clearing the upstream screen first (A4's correction) | unverified — flagged; depends on `GT-4` + `GT-12?` |
| A6 | Target-role compensation exceeds $95k by a material margin | untested belief | Verify, or flag as unverified | **Challenge** — used as a chain input with an explicit bracket rather than a point estimate | unverified — flagged → `GT-11?`; verifiable in one afternoon from levels.fyi / local postings for your city and seniority |
| A7 | Your employer will not subsidize tuition | untested belief | Verify, or flag as unverified | **Challenge** — commonly false; the cheapest possible check in this whole analysis | US IRC §127 permits up to $5,250/yr of employer educational assistance tax-free → `GT-5`. One HR email resolves it |
| A8 | An internal analyst→ML move is unavailable | untested belief | Verify, or flag as unverified | **Challenge** — unstated in the prompt, never tested, and would bypass the binding screen entirely | unverified — flagged → `GT-13?` |
| A9 | The credential's screening value persists through 2028 and beyond | current constraint | Record expiry conditions | **Accept with expiry** — expires under credential inflation or a labor-market shift in what ML hiring screens on | Not verifiable prospectively; treated as a constraint with a stated expiry, not a law |
| A10 | "ML roles" is one homogeneous target | convention | Challenge before use | **Discard** — research scientist, applied scientist, ML engineer, and MLOps have divergent credential gates | Distinct job families with distinct posted requirements → forces `GT-12?` |
| A11 | Self-study reliably converts into a shipped portfolio | untested belief | Verify, or flag as unverified | **Challenge** — the failure mode is unstructured study with no completion forcing function | unverified — flagged → `GT-8?` |
| A12 | The 1,560 hours have zero alternative economic use | untested belief | Verify, or flag as unverified | **Challenge** — partially false; some fraction is convertible to freelance/consulting income | unverified — flagged; see Abandoned Reasoning for why I did *not* price these at your wage rate |
| A13 | Enrolling does not change your behavior in the current job | untested belief | Verify, or flag as unverified | **Challenge** — surfaced by the second-order pass on C4 | unverified — flagged; two-year programs commonly induce candidates to defer job moves until graduation |
| A14 | The cheap and expensive programs deliver equivalent cohort/referral networks | untested belief | Verify, or flag as unverified | **Challenge** — surfaced by the third-order pass on C4; this is the one legitimate argument for a $46k program | unverified — flagged; checkable via the program's published employment report and alumni outcomes |
| A15 | Production ML work outranks personal repos as demonstrated evidence | untested belief | Verify, or flag as unverified | **Challenge** — surfaced by the C5 audit; widely held by hiring managers but unverified here | unverified — flagged |

*(A13, A14, A15 were added by the end-of-Phase-4 Assumption Audit, not by the initial sweep.)*

---

## 3. Ground Truths

| ID | Fact | Source / status |
|---|---|---|
| **GT-1** | The stated cash delta between the two options is $46,000 − $3,000 = **$43,000** over 2 years | Arithmetic on your figures |
| **GT-2** | The stated time budget is 15 hrs/wk × ~104 wks ≈ **1,560 hours**, about 0.75 of a full-time work-year (2,080 hrs) | Arithmetic on your figures |
| **GT-3** | Accredited online CS/ML master's degrees exist at total tuition of roughly **$7,000–$12,000** | Public tuition pages, Georgia Tech OMSCS and UT Austin online CS/DS master's, as of Jan 2026. HIGH confidence on existence; MEDIUM on the exact figure — verify current rates |
| **GT-4** | Hiring pipelines are **sequential**: an application passes an ATS/recruiter filter *before* a hiring manager evaluates work samples | Structural property of corporate hiring processes |
| **GT-5** | US IRC §127 permits employers to provide up to **$5,250/year tax-free** in educational assistance ($10,500 over 2 years) | US Internal Revenue Code §127 |
| **GT-6** | Both paths draw on the same conserved resource — hours outside a full-time job. An hour spent in coursework is definitionally not an hour spent shipping | Identity |
| **GT-7?** | Attrition among part-time graduate students working full-time is substantial | **unverified — flagged.** Commonly cited in the 30–50% range; not verified for the specific program type or for you |
| **GT-8?** | Self-directed study without external deadlines has high non-completion | **unverified — flagged.** MOOC completion is commonly cited below 10%, but that population is not "motivated career-changer with a concrete goal," so the figure likely understates your case |
| **GT-9** | An earned credential does not expire; a portfolio project's *technical* relevance decays as tooling shifts | Definitional for the credential; observational for tooling churn. MEDIUM confidence |
| **GT-10** | Income remains $95,000 throughout **both** paths — neither involves an earnings interruption | Given |
| **GT-11?** | Target-role compensation exceeds current by roughly $40k/yr (central), bracket $20k–$60k | **unverified — flagged.** Not verified for your city, seniority, or specific target role |
| **GT-12?** | The target roles apply a credential filter at the recruiter/ATS stage | **unverified — flagged.** This is the pivot variable named at the top of this response |
| **GT-13?** | Your current employer has ML-adjacent work an analyst could credibly propose to work on | **unverified — flagged.** Not stated in the prompt; cheapest item to check |

No assumption carrying a **Discard** verdict (A1, A2, A4, A10) appears in this list.

---

## 4. Derivation Chains

### C1 — The price is a convention, not a constraint

> `GT-3 + A1(challenged)` → the $46,000 figure is a property of one program's price point, not of the credential class → the "expensive credential OR cheap portfolio" framing is a **false dilemma manufactured by a price assumption** → **an accredited MS credential is obtainable for roughly $7k–$12k, collapsing the cash gap from $43,000 to roughly $4,000–$9,000.**

Confidence: **HIGH** on the existence claim (the chain needs only that such programs exist, which is robust). MEDIUM on the exact dollar figure — verify current tuition before acting.

### C2 — Break-even probability lift (quantitative rebuild)

Target quantity and units: **dollars per percentage-point of transition probability** ($/pp).
Unit decomposition: `($) ÷ ($ NPV of transition) → dimensionless fraction → ×100 → pp`.

> `GT-1 + GT-10` → the stake is a $43,000 marginal spend against an unchanged income base, so the entire decision is a probability purchase, not an income bet
> → `GT-11?` → net present value of a successful transition: central case $40k/yr delta × 10 yrs discounted at 5% ≈ $309k pre-tax ≈ **$216k net**; conservative $20k/yr × 7 yrs ≈ **$81k net**; aggressive $60k/yr × 15 yrs ≈ **$436k net**
> → break-even lift = $43,000 ÷ NPV → **[10 pp, 20 pp, 53 pp]** across the bracket
> → **the $46k program must raise your absolute probability of landing the role by ~20 percentage points over the alternative to pay for itself; the ~$8k program needs only ~4 pp.** `[Assumes: A6 — a material comp delta exists at all]`

Decision-resolution check: the bracket spans 10–53 pp, which is wide — but every point in it exceeds the ~4 pp the cheap program needs by a factor of 2.5× to 13×. **Both ends of the bracket drive the same decision**, so the estimate resolves despite its width. This is the stop criterion being met.

Confidence: **MEDIUM** — consumes `GT-11?`. Raised to HIGH by pulling actual posted compensation for your target role, city, and seniority.

### C3 — The two signals are complements, not substitutes

> `GT-4 + GT-12?` → screening is sequential, so portfolio evaluation occurs *downstream* of a credential/keyword filter → for a candidate whose current job title is not "ML anything," the **upstream filter is the binding constraint**, and a portfolio's value is conditional on clearing it → **the credential functions as a gate key and the portfolio as a conversion instrument; they operate at different pipeline stages and cannot be traded off against each other on one scale.** `[Assumes: A5 — a portfolio has near-zero effect if the resume never reaches a human]`

Confidence: **MEDIUM** — consumes `GT-12?`. Raised to HIGH by reading 15–20 live postings for your exact target role and counting how many state a degree requirement, plus one conversation with a recruiter who fills them.

### C4 — The combination dominates both stated options

> `C1 + C3` → both signals are separately necessary at different stages **and** independently purchasable once A1 is discarded
> → `GT-6 + GT-2` → the 1,560-hour budget splits as ~10 hrs/wk coursework + ~5 hrs/wk shipping without exceeding your own stated commitment
> → **a low-cost accredited program run concurrently with a modest shipping cadence acquires both signals for ~$8k — or ~$0 net if `GT-5` employer assistance applies — versus $46,000 for one signal.**
> →[2nd] enrolling creates a 2-year commitment that suppresses job mobility during the program `[Assumes: A13]`; the cohort creates referral paths that bypass the `GT-4` filter entirely; 15 hrs/wk sustained draws energy from current-job performance, eroding the fallback; shipped work compounds, each project accelerating the next
> →[3rd] suppressed mobility delays the salary delta by ~2 years, reducing C2's NPV by roughly 10% — **within the bracket, does not flip the result**; referrals being the actual payoff mechanism implies **cohort quality and employer pipeline matter more than curriculum**, which is the one legitimate case for a premium program `[Assumes: A14]`; degraded job performance worsens the failure-case fallback (staying an analyst with normal raises)

Contradiction check: no second- or third-order effect contradicts a Ground Truth. The referral finding *refines* C1 rather than overturning it — `GT-3` supports that the credential signal is cheap, but says nothing about network access being uniformly available across cheap programs. Recorded as a caveat; no return to Phase 2 triggered.

Confidence: **MEDIUM** — inherits from C3's `GT-12?`.

### C5 — The highest-return move is free and comes first

> `GT-4 + GT-10` → an internal candidate is **not subject to the external screen at all**, which is precisely the constraint C3 identified as binding
> → `GT-13? + A8` → an ML-adjacent project inside your current job produces *production* evidence with a business outcome attached `[Assumes: A15 — production work outranks personal repos as demonstrated evidence]`
> → **before committing any capital, run a 90-day internal experiment: propose and ship one ML-flavored project in your current role. It simultaneously tests the transition hypothesis, generates portfolio evidence stronger than any personal repo, and costs $0.**

Confidence: **MEDIUM**, and strictly conditional — the chain voids entirely if `GT-13?` is false. Raised to HIGH by one conversation with your manager.

### C6 — Weighted trade-off across four options

Options: **A** = $46k master's · **B** = self-study only · **C** = low-cost accredited MS + portfolio · **D** = internal experiment first, then C.

Weights locked **before** any scoring, per the trade-off procedure:

| Criterion | Weight |
|---|---|
| 1. Probability of clearing the upstream screen | 5 |
| 2. Strength of demonstrated-work signal | 4 |
| 3. Cost efficiency (lower outlay better) | 4 |
| 4. Completion probability at 15 hr/wk | 4 |
| 5. Speed to first ML-titled role | 3 |
| 6. Downside protection if the transition fails | 3 |
| 7. Network / referral access | 2 |

| Criterion (w) | A | B | C | D |
|---|---|---|---|---|
| 1. Upstream screen (5) | 5 | 2 | 4 | 5 |
| 2. Demonstrated work (4) | 2 | 5 | 4 | 5 |
| 3. Cost efficiency (4) | 1 | 5 | 4 | 5 |
| 4. Completion probability (4) | 2 | 2 | 3 | 4 |
| 5. Speed (3) | 2 | 4 | 3 | 5 |
| 6. Downside protection (3) | 2 | 4 | 4 | 5 |
| 7. Network (2) | 4 | 2 | 3 | 2 |
| **Weighted total** | **65** | **86** | **91** | **115** |

> `GT-7? + GT-8? + GT-12?` feed criteria 1 and 4 → totals rank **D (115) > C (91) > B (86) > A (65)** → **sensitivity:** C and B are 5.5% apart, inside the 10% near-tie band, so scores are *not* refined; instead the flipping criterion is identified → **criterion 1 is the flipping weight: if the target roles do not gate on credentials, B's score on criterion 1 rises 2→4 and B (96) overtakes C (91).** `[Assumes: A3 — 15 hr/wk is sustainable, which drives every criterion-4 score]`

Confidence: **MEDIUM** for "A is the worst option" (that gap is 26 points and survives any single weight change). **LOW** for the C-vs-B *ordering* specifically — a genuine near-tie that the procedure forbids me to resolve by score-tuning. D's high score partly reflects that it is cheap and reversible, and it is available only if `GT-13?` holds; D is also not a substitute for C but a **sequencing step before** it.

---

### End-of-Phase-4 Assumption Audit (process output)

| Chain | Step | Step text (brief) | Assumption surfaced? | Added to table? |
|---|---|---|---|---|
| C1 | 1 | $46k is one program's price, not the credential's | none (A1 already in table) | n/a |
| C1 | 2 | Framing is a false dilemma from a price assumption | none (A2 already in table) | n/a |
| C1 | 3 | Credential obtainable at $7k–$12k | none (GT-3 covers) | n/a |
| C2 | 1 | Stake is a probability purchase, not an income bet | none (GT-10 covers) | n/a |
| C2 | 2 | NPV of transition = [$81k, $216k, $436k] net | A6 (already in table) | n/a |
| C2 | 3 | Break-even lift = [10, 20, 53] pp | none | n/a |
| C2 | 4 | $46k needs ~20 pp; $8k needs ~4 pp | none | n/a |
| C3 | 1 | Screening is sequential; portfolio is downstream | none (A4 already in table) | n/a |
| C3 | 2 | Upstream filter binds for a non-ML-titled candidate | A5 (already in table) | n/a |
| C3 | 3 | Credential = gate key, portfolio = conversion instrument | none | n/a |
| C4 | 1 | Both signals independently purchasable | none | n/a |
| C4 | 2 | 1,560 hrs splits 10/5 within stated commitment | none (GT-2, GT-6 cover) | n/a |
| C4 | 3 | Combination costs ~$8k or ~$0 net vs $46k | none (GT-5 covers) | n/a |
| C4 | 4 (2nd) | Enrollment suppresses job mobility for 2 years | **A13 — new** | **yes** |
| C4 | 5 (2nd) | Cohort referrals bypass the GT-4 filter | none (folds into A14) | n/a |
| C4 | 6 (2nd) | 15 hr/wk erodes current-job performance | none (A3 covers) | n/a |
| C4 | 7 (3rd) | Cohort quality matters more than curriculum | **A14 — new** | **yes** |
| C5 | 1 | Internal candidates bypass the external screen | none (GT-4 covers) | n/a |
| C5 | 2 | Internal project yields production evidence | **A15 — new** | **yes** |
| C5 | 3 | Run a 90-day internal experiment first | none (A8/GT-13? cover) | n/a |
| C6 | 1 | Weights locked, options scored | none | n/a |
| C6 | 2 | Totals D 115 > C 91 > B 86 > A 65 | A3 (already in table) | n/a |
| C6 | 3 | C-vs-B near-tie flips on criterion 1 | none (GT-12? covers) | n/a |

---

## 5. Abandoned Reasoning

**Tried:** Compute a simple payback period on the master's — $46,000 against a post-degree salary uplift.
**Why abandoned:** The intermediate step could not be established. A payback period compares the degree against the *status quo*, which silently assumes the self-study path produces a $0 uplift. That is exactly the quantity in dispute. Any ROI framing that omits the counterfactual is structurally unable to answer this question.
**What it ruled out:** Every "is the master's worth it?" framing measured against staying put. The only admissible comparison is marginal — degree versus alternative, which is what C2 does.

**Tried:** Price the 1,560 hours at your effective hourly wage ($95,000 ÷ 2,080 ≈ $46/hr → ~$71,000), making the master's "really" cost ~$117,000.
**Why abandoned:** Contradicts `GT-10`. Your income is unchanged in both paths, so those hours are not fungible with wages — the wage rate prices hours you are already selling. Applying it here double-counts. A defensible opportunity cost would use a realistic freelance rate times a realistic utilization fraction, which is far smaller and, critically, *identical across both options* — so it cancels out of the comparison entirely.
**What it ruled out:** The dramatic "the degree costs six figures" reframe, which is rhetorically strong and analytically wrong.

**Tried:** Break the C-versus-B near-tie by refining the individual scores.
**Why abandoned:** The trade-off procedure's sensitivity rule explicitly forbids score-refinement inside the 10% band — refining scores after seeing the totals is the reverse-engineering failure mode the locked-weights discipline exists to prevent.
**What it ruled out:** A false confident ordering. The tie is a real finding, and it points at `GT-12?` as the one fact that resolves the decision.

---

### §6 → §4 closure ledger (process output)

- "Sequence D then C: run a 90-day internal experiment, then enroll in a low-cost accredited program with a concurrent shipping cadence" → chains **C5, C4, C6** ✓
- "Do not pay $46,000 unless a named, verified brand or employer-pipeline advantage is worth ≥16 pp of transition probability" → chains **C1, C2** ✓
- "Key insight: $46,000 is a price assumption rather than a constraint, and the two signals are stage-complements rather than substitutes" → chains **C1, C3** ✓
- "The C-vs-B ordering is genuinely undetermined until GT-12? is checked" → chain **C6** ✓
- "Overall confidence: MEDIUM" → inherited from **C2, C3, C4, C5** ✓

Ledger clean — no unbacked §6 claim. Proceeding to the rubric.

---

### Pre-mortem (Phase 5 stress test)

*It is 2028. You did the plan. It failed. What caused it?* Written without filtering: you never finished the degree because 15 hrs/wk collided with a promotion cycle; you shipped three half-finished repos nobody read; the market shifted and entry-level classical-ML pipeline work thinned out; you optimized for credential acquisition and never spoke to a single hiring manager for two years; the internal proposal was declined once and you dropped it; you never confirmed that the roles you wanted were reachable from your background at all.

**Cluster:** five of six causes share one root — **the plan has no falsification checkpoint.** That is a structural weakness, not a list of risks.

**Plan change (a pre-mortem with no plan change was box-ticking):** insert a hard month-6 checkpoint requiring three artifacts — (1) three conversations with recruiters or hiring managers in the target role, (2) one shipped artifact with at least one real user, (3) a direct answer on whether the credential is actually asked for. If any is missing at month 6, the plan is wrong and stops rather than continuing on momentum.

---

### Rubric scoring (Phase 5)

Assumption Audit verified present, one row per chain per step, in order, no step skipped — 23 rows covering C1(3), C2(4), C3(3), C4(7), C5(3), C6(3).

**Criterion 1: Identify Essence**
Quoted span: *"What is the cheapest way to buy past whichever screen actually gates the ML roles I want — and is that screen the credential, the shipped work, or neither?"*
Band: **Rigorous**
Justification: single sentence naming the underlying question rather than the prompt's framing, with five success criteria each stating a verb + subject + outcome testable by scanning section 6.

**Criterion 2: Challenge Assumptions**
Quoted span: *"A1 | $46,000 is the price of an accredited part-time ML/CS master's | convention | Challenge before use | **Discard** — the figure is a property of one program's price point, not of the credential class"*
Band: **Rigorous**
Justification: all 15 rows use exactly the four-type scheme, Treatment cells use each type's prescribed vocabulary, Verdicts are a leading token plus em-dash plus specific justification, unverified chain inputs read "unverified — flagged," and four assumptions carry Discard verdicts.

**Criterion 3: Establish Ground Truths**
Quoted span: *"GT-12? | The target roles apply a credential filter at the recruiter/ATS stage | **unverified — flagged.** This is the pivot variable"*
Band: **Sound**
Justification: all IDs are stable and match chain references and every unverified entry carries the `?` suffix, but GT-4 and GT-6 cite a structural property and an identity rather than a named external source.

**Criterion 4: Reason Upward**
Quoted span: *"→ for a candidate whose current job title is not 'ML anything,' the **upstream filter is the binding constraint** … `[Assumes: A5 …]`"*
Band: **Rigorous**
Justification: six chains, each with at least one genuine intermediate claim not statable from any single named GT; `[Assumes:]` tokens declare the four chain-surfaced assumptions; three dead ends documented with what-was-tried / why-abandoned / what-it-ruled-out; no analogy used as standalone evidence — the OMSCS/UT Austin reference is grounded in GT-3 as a verifiable tuition fact, not as "others did it this way."

**Criterion 5: Validate**
Quoted span: *"Confidence: **MEDIUM** — consumes `GT-11?`. Raised to HIGH by pulling actual posted compensation for your target role, city, and seniority."*
Band: **Rigorous**
Justification: every chain carries a confidence line naming the specific `GT-N?` input that caused the downgrade and the specific verification that raises it; no chain consuming a `GT-N?` is rated HIGH; the pre-mortem produced a named structural weakness and a corresponding plan change.

**Criterion 6: Conclusion-to-Ground-Truth Traceability**
Quoted span: *"Key insight: $46,000 is a price assumption rather than a constraint, and the two signals are stage-complements rather than substitutes" → chains **C1, C3***
Band: **Rigorous**
Justification: the ledger shows every section-6 claim citing a named section-4 chain with no new claims introduced, and the Key Insight names a finding neither convention nor analogy reaches rather than restating the recommendation.

**Gate:** no criterion Absent. **Hand-wavy cap:** zero at Hand-wavy. **Rubric cleared.**

---

## 6. Conclusion

**Recommended approach — sequence D, then C** (chains C5, C4, C6):

1. **Weeks 0–12, $0.** Ask your manager for one ML-flavored project inside your current role. In parallel, send one email to HR about tuition assistance (`GT-5`: up to $5,250/yr tax-free — potentially $10,500 of the total), and read 15–20 live postings for your exact target role, counting how many state a degree requirement. That last count resolves `GT-12?`, which is the single fact this whole decision turns on.
2. **Month 4 onward.** Enroll in an accredited low-cost online master's (~$7k–$12k, `GT-3`) at ~10 hrs/wk, reserving ~5 hrs/wk to ship. Same 15-hour commitment you already budgeted; roughly one-fifth the cash, and possibly near zero after employer assistance.
3. **Month 6, hard checkpoint.** Three recruiter/hiring-manager conversations, one shipped artifact with a real user, and a direct answer on credential requirements. Missing any of the three means the plan is wrong and stops — this is the falsification gate the pre-mortem showed was absent.

**Do not pay $46,000** unless you can name and verify a specific advantage of that program — cohort quality, a published employment report, a concrete employer pipeline — worth at least ~16 percentage points of transition probability over the cheap alternative (chains C1, C2). Curriculum is not that advantage; per C4's third-order pass, the referral network plausibly is. Demand evidence, not a brochure.

**Key insight** (chains C1, C3) — the non-obvious finding, and the one that convention and analogy do not reach: **your question contains a hidden price assumption and a hidden model of hiring, and both are wrong.** The $46,000 is a property of one program, not of the credential. And "employers screen partly on credentials and partly on shipped work" describes a weighted sum, whereas hiring is a sequence: the credential is a gate key read by a recruiter, the portfolio is a conversion instrument read by a hiring manager. You cannot trade one against the other, because they are not spent in the same place. Once both errors are removed, the trade-off you posed largely dissolves — you can buy both signals for roughly 17–26% of the price you assumed you'd pay for one.

**Trade-offs acknowledged and left open** (chain C6): the ranking of C over B is a genuine near-tie (91 vs 86, inside the sensitivity band) and I am deliberately **not** resolving it, because resolving a near-tie by adjusting scores after seeing the result is the exact failure the locked-weights discipline prevents. It flips on criterion 1: if your target roles do not gate on credentials — likelier for ML engineering at startups and product companies than for applied/research scientist roles at large labs — self-study alone wins outright and you should skip the degree. Step 1 above is designed to answer this before you spend anything.

**Downside case:** if the transition fails, path C leaves you with a permanent credential (`GT-9`), ~$8k spent, and an intact $95k income (`GT-10`). Path A leaves you $46,000 down. Path B leaves you with projects whose technical relevance decays. This asymmetry, not the expected-value calculation, is the strongest argument for C over A.

**Overall confidence: MEDIUM**, matching the weakest load-bearing chains (C2 via `GT-11?`, C3 via `GT-12?`, C5 via `GT-13?`). The LOW-confidence element — the C-vs-B ordering — is stated above as an open question, not as a recommendation, so no conclusion presented here rests on it. All three unverified inputs are resolvable in under a week of low-effort checking, which would raise this to HIGH. Do that checking before you spend anything.