# v9.4 Exemplar Re-Derivation Fixture — backlog 999.118

**Captured:** 2026-09-18. **Status:** frozen hand re-derivation record, appended to (never
rewritten) across plans 44-01 through 44-07. This fixture is NOT registered in
`scripts/check-firewall-battery.sh`'s `_FROZEN_PATHS` array by this plan — plan 44-06 adds that
registration once the artifact is final (registering it now would make `FROZEN-EVIDENCE` fail on
every later plan's in-flight edit to this same file).

## Chain of custody

- **Repo HEAD SHA at the start of Phase 44:** `f7efc17febdfadc62e682d06f40d98017032828d` (read via
  `git rev-parse HEAD` before this plan's Task 1 made any edit).
- **Plugin version:** `9.3.2`, read live via `python3 scripts/check-version-stamps.py` — all 17
  hand-maintained stamps agree, `check-version-stamps: 17 stamps, all '9.3.2'` /
  `check-version-stamps: PASS`. Expected, and confirmed, unchanged for the whole phase per D-04.
- **This fixture records HAND arithmetic re-derivation, not live model capture.** Unlike the
  `tests/confidence-transitivity-v9.4/README.md` precedent (which chains custody through a
  `claude -p` transport command and a `.jsonl`/`.md` sha256 table per capture), no model is
  dispatched to produce this evidence — a human/executor re-computes each exemplar's own stated
  arithmetic with `python3 -c` and records the computed value beside the file's stated value.
  There is therefore no transport command and no capture-pair sha256 table here; the equivalent
  chain-of-custody instrument is the per-source-file hash table below, which pins exactly which
  bytes of `shared/examples/*.md` each recorded re-derivation was checked against.

Per-file source hash table, all 14 files under `shared/examples/`. Pre-edit columns captured live
at the repo HEAD above via `sha256sum` and `wc -l`; post-edit columns are filled by the plan that
last touches each file.

| file | pre-edit sha256 | pre-edit lines | post-edit sha256 | post-edit lines |
|---|---|---|---|---|
| shared/examples/composed-inversion-second-order.md | `3adfedef1542939ccd632589c6b646559eccf6aa8d7fbd8aa2de1c54a57d3377` | 341 | `3adfedef1542939ccd632589c6b646559eccf6aa8d7fbd8aa2de1c54a57d3377` (unchanged — plan 44-01 Task 2 found nothing to fix) | 341 |
| shared/examples/decompose-irreducibility.md | `e91e2bac8d25321aab4620fc688f64e63af291b3b24b2e6041bd805de9e643b2` | 345 | `e91e2bac8d25321aab4620fc688f64e63af291b3b24b2e6041bd805de9e643b2` (unchanged — plan 44-01 Task 2 found nothing to fix) | 345 |
| shared/examples/estimate-fermi.md | `7215c0c0485991429eeac27a6e2c612de38511a83c62db97b6fcc79bbac6ef67` | 269 | `7215c0c0485991429eeac27a6e2c612de38511a83c62db97b6fcc79bbac6ef67` (unchanged — plan 44-01 Task 2 found nothing to fix) | 269 |
| shared/examples/ishikawa-fishbone.md | `1e78a18f5f4edfbe601a0b230997ac474ef802b369e64904123581171ee713cb` | 355 | `1e78a18f5f4edfbe601a0b230997ac474ef802b369e64904123581171ee713cb` (unchanged — plan 44-01 Task 2 found nothing to fix) | 355 |
| shared/examples/personal-general-2.md | `993e00534d49333514865d7222df537b3e8edd6eb0143af5cdd29a900b76767d` | 124 | `32ee28396bb4e1d475c0cbf9259a67c145eb521b1fcd9fea637648fa203faee3` | 124 |
| shared/examples/personal-general.md | `5e43d95329b2ca52fb6699601b382f11b5ea26cc7a992b83c891732d3301dea7` | 101 | `96fc4803c59fb003bf189c5ab16092b64ae97fbee965f41f7d3675d3ea04f1a8` | 101 |
| shared/examples/product-business-2.md | `052691ec3a851f1d3b8dcb4aa2ff7cd0cad1b58cf22f127ae12c76ee32630935` | 211 | `d23626a775ee5765a97a72c61a5722c84fc70a044da349653399f42c5fd39096` | 216 |
| shared/examples/product-business.md | `d948f9fda657dba4fc8c66fd9e60c5846d837c8b78655e1c2b41d2a8fe2b42c4` | 94 | (pending — plan 44-04) | (pending — plan 44-04) |
| shared/examples/science-engineering-2.md | `282db9d21c058c7ed1dd05df45dd328eded851a7bb1d1ae7e38e379f09264aa5` | 218 | (pending — plan 44-06) | (pending — plan 44-06) |
| shared/examples/science-engineering.md | `d5aed303b62e07f1d7ab00e4d171af2ef60a02e9009af156336095b4f4bdfe54` | 187 | (pending — plan 44-05) | (pending — plan 44-05) |
| shared/examples/self-application.md | `47adb0226654cb6246b0004d83c399a81431ebcba98f9509fd61228beda0ce11` | 399 | out of scope (D-03) — pre-edit and post-edit values must be identical | out of scope (D-03) — pre-edit and post-edit values must be identical |
| shared/examples/software-systems-2.md | `66c6548e402398c5f2c18acca34b5323d10a9ab6781754251034f265b5d9d596` | 346 | `66c6548e402398c5f2c18acca34b5323d10a9ab6781754251034f265b5d9d596` (unchanged — plan 44-01 Task 2 found nothing to fix) | 346 |
| shared/examples/software-systems.md | `9c883ea780c2ddde363147d86db91f1ad20212b29eccc07b8dbacc03d7e3fa61` | 301 | (pending — plan 44-04) | (pending — plan 44-04) |
| shared/examples/theoretical-limit-carnot.md | `7e8949ab65ae678ad11dda352a73e43f97063515f614c1ab5d1aee1ee06aa594` | 197 | `7e8949ab65ae678ad11dda352a73e43f97063515f614c1ab5d1aee1ee06aa594` (unchanged — plan 44-01 Task 2 found nothing to fix) | 197 |

## Pre-edit gate baseline

Every command below was run live at the repo HEAD recorded above, immediately before this plan's
Task 2 made any content edit. Verbatim final line of each:

```text
$ python3 scripts/sync-content.py --check
(no output; exit 0 — shared/ and the generated tree are in sync)

$ python3 scripts/check-conf-gate.py
check-conf-gate: PASS

$ python3 scripts/report-conformance.py --check
report-conformance: PASS — no drift

$ bash scripts/check-firewall-battery.sh
FIREWALL: GREEN (23/23)
```

`check-conf-gate.py`'s live run also printed its standing COVERAGE line
(`check-conf-gate: COVERAGE — measured 28 artifacts across shared-examples, generated-twin`) and
three `D-08` synthetic-injection self-check lines
(`D-08(a) hop re-wrap on shared/examples/personal-general.md — heading_malformed_blocks 0 -> 1`,
`D-08(b) verdict-cell strip on shared/examples/personal-general.md — nonconforming_verdict_cells
0 -> 1`, `D-08(c) citation removal on shared/examples/personal-general.md — silent_untraced_claims
0 -> 1`) — these are the script's own built-in mechanical-defect-detector self-check, run against a
disposable in-memory mutation, not a finding against the committed file; the script's own exit
code and terminal `PASS` line are the pass/fail signal.

44-RESEARCH.md's "Gate Impact, Re-Confirmed 2026-09-18" section captured `FIREWALL: GREEN (23/23)`,
`check-conf-gate.py` clean and `report-conformance.py --check` clean on 2026-09-18. **This run
reproduces that baseline exactly** — same verdict, same gate count (23/23), all 23 individual
gates `[PASS]` (confirmed by reading the full battery output line by line: DUAL-04, GATE-02-v8.5,
STEP0-06, STEP0-08, VAL-01, VAL-02, VAL-03, VERSION-01, REG-GUARD, GATE-01, BATT-06, TRACE-03,
QUAL-01, PROV-GUARD, HARN-01, HARN-02, HARN-03, SCAN-GUARD, HC-BOUND, CONF-GATE, CONF-SURFACE,
INVARIANT-CHECK, FROZEN-EVIDENCE — all `[PASS]`).

## Corrected-defect re-derivations (999.118 steps 1-2)

### personal-general-2.md          (plan 44-02)

Four defect origins and five restatement sites, all independently re-derived with `python3 -c`
in this session (not copied forward from 44-RESEARCH.md's or 44-PATTERNS.md's own first-pass
figures — every value below was recomputed and, in every case, matched 999.118's and this
plan's own quoted figures within rounding). Three of the five restatement sites (lines 64, 80,
122) are named by no row of 999.118's own table (`personal-general-2.md:52,61,62,71-72`); of
those, line 80 is additionally named by no upstream artifact at all — not 44-RESEARCH.md's
blast-radius section, not 44-PATTERNS.md's per-file table — and was found while writing plan
44-02.

**Defect 1 — GT-6 (line 52, origin, self-contained, no downstream chain citation).**
- Inputs (file's own): $240,000 balance, 27-year (324-month) term, 6.25% APR, one-time $60,000
  additional principal payment.
- Operation: standard amortisation. Monthly payment `P × r / (1 − (1+r)^−n)` with
  `r = 0.0625/12`, `n = 324`. After the prepayment, remaining term
  `n' = −ln(1 − r·B/pmt) / ln(1+r)` with `B = $180,000`. Interest saved = (lifetime interest at
  `n`) − (lifetime interest at `n'`). Years-1–10 avoided interest = (interest paid in months
  1–120 without the prepayment) − (interest paid in months 1–120 with the prepayment, amortising
  from the $180,000 post-prepayment balance).
- Result: payment = $1,535.24/mo; remaining term drops from 324 to 182 months (`182 = ceil(181.58)`)
  — an 11.8-year shortening; lifetime interest saved = $158,644 (recorded as "approximately
  $158,600"); years-1–10 avoided interest = $51,913 (recorded as "approximately $51,900").
- Site: line 52 only (GT-6's own bullet). Confirmed isolated: `grep -n "GT-6"` elsewhere in the
  file returns nothing; no chain cites GT-6 on a head line.
- Reconciliation added: GT-6 now states explicitly that its amortisation-derived figures measure
  actual avoided interest over the remaining term, while the chains below use the separate
  guaranteed-return-equivalent method (`$60,000 × 1.0625^10 = $110,012` at the 10-year horizon,
  a figure that was already correct in the file) to measure the 10-year mortgage-balance-equivalent
  value of the same $60,000 — the two answer different questions over different horizons and are
  not inconsistent.
- Provenance: 999.118's own table (row `personal-general-2.md:52,61,62,71-72`); 44-RESEARCH.md's
  "Blast-radius findings" item 1; 44-PATTERNS.md's per-file table, line 52.

**Defect 2 — C1 hop 1 (line 61, origin).**
- Inputs (file's own): $60,000 deployment, 8.5% nominal expected holding-period return (9%
  nominal central estimate minus 0.5pp effective annual tax drag), 18% long-term capital-gains
  rate, 10-year horizon. The file's own stated formula,
  `$60,000 × (1.085)^10 × (1 − 0.18 × (1 − (1/(1.085)^10)))`, was already correct — only the
  number it was said to produce was wrong.
- Operation: `1.085^10 = 2.260983`; gross = `60000 × 2.260983 = $135,659`; `1/1.085^10 =
  0.442285`; tax-shield factor = `1 − 0.18 × (1 − 0.442285) = 0.899611`; after-tax = `135,659 ×
  0.899611`.
- Result: $122,040 (precisely $122,040.39). The file's prior claim of "$113,000–$120,000" was
  simply arithmetically wrong against its own stated formula.
- Site: line 61. Formula text left byte-unchanged; only the stated result and the range-vs-point
  framing were corrected — the sentence now states the point estimate is "exactly what the
  formula immediately preceding it produces."
- Provenance: 999.118's own table (row `personal-general-2.md:52,61,62,71-72`); 44-RESEARCH.md's
  "Blast-radius findings" item 1 (independently re-verified there to $122,041, matching within
  rounding); 44-PATTERNS.md's per-file table, line 61.

**Defect 3 — C1 hop 2 (line 62, origin — both the gap figure and its own interpretive
"characterisation" sentence).**
- Inputs (file's own): corrected C1 hop-1 after-tax terminal value $122,040 (this defect); the
  paydown branch's $110,012 (`$60,000 × 1.0625^10`, already correct in the file).
- Operation: gap = `122,040 − 110,012`; percent of principal = `gap / 60,000`.
- Result: gap = $12,028 (recorded as "$12,030"); 20.0% of principal (recorded as "roughly 20%").
  The file's prior claim of "$3,000–$10,000" / "roughly 5–9%" no longer matched the corrected
  hop-1 figure.
- Sites: line 62 (origin — the gap/percentage numbers) — and, on the same line, the
  characterisation sentence that followed them ("The two numbers are close enough that the
  margin is well within the noise of the input assumptions") was itself no longer supportable at
  a 20%-of-principal gap and was replaced with a claim the file's own chains do support: the
  central-estimate advantage is smaller than chain C2's worst-decile swing in the opposite
  direction, so the sign of the comparison is set by the return assumption, not by the size of
  the gap. This characterisation-sentence repair is the fifth of the plan's five named
  restatement sites, distinct from the numeric restatements at lines 64, 80, 82 and 122.
- Provenance: 999.118's own table (row `personal-general-2.md:52,61,62,71-72`);
  44-RESEARCH.md's "Blast-radius findings" item 1; 44-PATTERNS.md's per-file table, line 62.

**Defect 3, restatement — C1 confidence sensitivity claim (line 64). Named by NO row of
999.118's own table — found by 44-RESEARCH.md's blast-radius section and confirmed by
44-PATTERNS.md's per-file table.**
- Inputs (file's own): the corrected $12,030/20% gap (Defect 3, above); GT-3?'s 6.5% central
  real-return estimate; the file's own ~2.5% expected-inflation assumption (implicit in its
  6.5% real ≈ 9% nominal, 8.5% net-of-drag figure at line 60).
- Operation: recompute C1 hop 1's own formula at reduced real-return assumptions and compare
  each result to the unchanged $110,012 paydown figure. A 1-point real-return reduction (6.5%→
  5.5%) takes the nominal holding-period return from 8.5% to 7.5%: `60000 × 1.075^10 × (1 −
  0.18 × (1 − 1/1.075^10)) = $112,203`. A 2-point reduction (to 4.5% real, 6.5% nominal) gives
  `60000 × 1.065^10 × (1 − 0.18 × (1 − 1/1.065^10)) = $103,155`. Bisection on the nominal rate
  between these two endpoints locates the rate at which the formula's output equals $110,012
  exactly: nominal ≈ 7.265%, an ≈1.23-percentage-point reduction from the 8.5% baseline.
- Result: 1-point reduction narrows the gap to `112,203 − 110,012 ≈ $2,191` (recorded as
  "roughly $2,200"), still favouring indexing — the gap narrows but does not close. The gap
  closes at approximately a 1.2-percentage-point reduction (computed: 1.23 points). A 2-point
  reduction reverses the recommendation: `110,012 − 103,155 ≈ $6,857` (recorded as "roughly
  $6,900") now favours paydown. The file's prior sensitivity claim ("a 1-point reduction...
  closes the gap and a 2-point reduction... reverses the recommendation") was computed against
  the old, wrong $3,000–$10,000 gap and both of its numeric thresholds were wrong once the gap
  was corrected.
- Site: line 64 only. The LOW label, the `GT-3?` dependency clause, and the verification-path
  sentence were left intact, per the plan's own instruction.
- Provenance: NOT named by 999.118's own table. Named by 44-RESEARCH.md's "Blast-radius
  findings" item 1 ("this sentence must be re-derived against the corrected ~$12,030/20% gap,
  not merely left in place") and confirmed by 44-PATTERNS.md's per-file table (line 64,
  "Restatement").

**Defect 4 — C2 (lines 71–72, origin).**
- Inputs (file's own): $60,000 deployment, 2.5% nominal worst-decile annualised return (from
  GT-3?'s 0–2% real worst-decile plus ~2.5% expected inflation), 18% long-term capital-gains
  rate, 10-year horizon.
- Operation: gross = `60000 × 1.025^10`; gain = gross − 60,000; tax = `0.18 × gain`; after-tax =
  gross − tax. Gap vs. paydown = `110,012 − after-tax`; percent of principal = `gap / 60,000`.
- Result: `1.025^10 = 1.280085`; gross = $76,805; gain = $16,805; tax = $3,025; after-tax =
  $73,780. Gap = `110,012 − 73,780 = $36,232` (recorded as "$36,230"); `36,232 / 60,000 = 60.4%`
  (recorded as "roughly 60%"). The file's prior claim presented $76,000–$78,000 as already an
  after-tax figure via a hand-waved "× (1 − 0.18 × small fraction)" term and stated the gap as
  "approximately $32,000... roughly half the principal" — both wrong once the tax step is done
  explicitly rather than folded into an unexplained fraction.
- Sites: line 71 (gross and after-tax terminal value, origin — the "small fraction" hand-wave
  was removed and replaced with the explicit two-step computation), line 72 (gap and percentage
  characterisation, origin).
- Provenance: 999.118's own table (row `personal-general-2.md:52,61,62,71-72`); 44-RESEARCH.md's
  "Blast-radius findings" item 1; 44-PATTERNS.md's per-file table, lines 71–72.

**Defect 4, restatement — C3 hop, terminal-value parenthetical (line 81, cited as "line 80" by
the plan and by 44-PATTERNS.md — see the off-by-one note below). Named by NO upstream artifact
— found while writing plan 44-02.**
- Inputs (file's own): the corrected after-tax terminal value $73,780 (Defect 4, above).
- Operation: direct substitution — the parenthetical `(≈ $76,000–$78,000 terminal after a
  10-year flat-real-return period)` restated C2's pre-correction gross-looking figure as the
  "worst-decile index outcome," which after Defect 4's correction should read the after-tax
  figure, $73,780.
- Result: `(≈ $73,780 after-tax terminal after a 10-year flat-real-return period)`. The
  surrounding hard-floor argument was re-read after the edit and confirmed to still read
  correctly at the lower figure — a lower terminal value makes the hard-floor concern in the
  sentence's "if it does not cross any hard floor" clause strictly harder to satisfy, not
  easier, so the sentence's own logic is unaffected by the correction.
- Site: line 81 in both the pre-edit and post-edit file (`git show HEAD:shared/examples/
  personal-general-2.md | sed -n '81p'` confirms the parenthetical sat at line 81 before this
  plan's edits, not line 80). The plan's own task text and 44-PATTERNS.md's per-file table both
  cite this site as "line 80" — an off-by-one in the citation, not in the file; recorded here as
  an additional-site finding on the citation itself, distinct from the content correction. No
  line was added or removed above this point by the phase's edits, so the line number is
  unchanged before and after.
- Provenance: NOT named by 999.118's own table, NOT named by 44-RESEARCH.md's blast-radius
  section (which lists only lines 62, 64, 71-72, 82 and 122 for this file), NOT named by
  44-PATTERNS.md's per-file table (which lists only lines 52, 61, 62, 64, 71, 72, 82 and 122).
  Found at plan-writing, Phase 44 — recorded here rather than attributed to any upstream
  artifact, per the plan's own instruction not to misattribute this site to 44-PATTERNS.md.

**Defect 4, restatement — C3 hop, worst-decile underperformance (line 82). Named by
44-RESEARCH.md's blast-radius section and 44-PATTERNS.md's per-file table.**
- Result: `$32,000` → `$36,230`, matching Defect 4's corrected gap exactly.
- Provenance: 44-RESEARCH.md's "Blast-radius findings" item 1 ("restated in two further sites:
  C3 (line 82... )"); 44-PATTERNS.md's per-file table, line 82.

**Defect 3 + Defect 4, restatement — §6 Trade-offs (line 122), one sentence restating both
corrected gaps. Named by NO row of 999.118's own table — found by 44-RESEARCH.md's
blast-radius section and confirmed by 44-PATTERNS.md's per-file table.**
- Result: `$32,000` → `$36,230` (Defect 4's gap) and `$3,000–$10,000` → `$12,030` (Defect 3's
  gap), both in the same sentence. The sentence was neither split, merged nor deleted — the
  `conclusion_claims` floor for this file is 7 (CONF-GATE floors, plan interfaces block).
- Provenance: NOT named by 999.118's own table. Named by 44-RESEARCH.md's "Blast-radius
  findings" item 1 (both figures explicitly named as restated at line 122) and confirmed by
  44-PATTERNS.md's per-file table, line 122.

**Summary of the five restatement sites** (999.118 names none of these three by line number;
the phase's own table cites only the four origin lines 52, 61, 62, 71-72):
line 64 (C1 confidence sensitivity — 44-RESEARCH.md), line 81 (C3 terminal-value parenthetical,
cited as "line 80" upstream — found at plan-writing), line 82 (C3 underperformance gap —
44-RESEARCH.md and 44-PATTERNS.md), line 122 (§6 Trade-offs, both gaps — 44-RESEARCH.md and
44-PATTERNS.md), and the line-62 characterisation sentence (repaired alongside its own origin
number, per Defect 3 above).

### personal-general.md            (plan 44-03)

One defect origin with six restatement sites, all independently re-derived with `python3 -c`
in this session. 999.118's own table cites only two lines (`personal-general.md:57,79`);
44-RESEARCH.md's blast-radius section and 44-PATTERNS.md's per-file table both extend this to
six sites (53, 57, 59, 79, 93, 99); this plan's own post-edit `effective` sweep (required by its
own Task 1 action text) found three further sites named by NO upstream artifact (18, 56, 67).

**Defect — C1's pre-tax/after-tax basis mixing and percentage framing (origin: lines 53, 57,
59; 999.118's own table row `personal-general.md:57,79`).**
- Inputs (file's own): GT-1 $70,000/year nominal pre-tax compensation increase; GT-2
  ~$15,600/year San Francisco rent premium; GT-3 ~0 percentage-point CA-vs-OR state marginal
  tax differential.
- Operation: `70,000 - 15,600 = 54,400` (the subtraction itself was already correct — it rounds
  to the file's stated "approximately $54,000"); `15,600 / 70,000 = 0.2229` (the rent
  adjustment removes ~22% of the nominal figure); `15,600 / 54,400 = 0.2868` (the nominal figure
  is ~29% larger than the rent-adjusted figure); `(70,000 - 54,400) / 54,400 = 0.2868`, matching
  999.118's own statement of the same ~29% relation via `(70-54)/54 = 0.2963` (rounding
  difference is from using the file's rounded "$54,000" vs. the unrounded $54,400 — both round
  to "roughly 29%").
- Defect, two parts. (1) The file's prior sentence "roughly 23% less than the nominal headline
  figure" used neither of the two ratios above correctly: "overstates X by N%" means
  `N = (nominal - X) / X`, which is 29% (the `15,600 / 54,400` relation), not 23%; the ~22%
  figure is the OTHER relation (`15,600 / 70,000`, reduction from nominal). (2) More
  fundamentally, subtracting the after-tax $15,600 rent outlay from the pre-tax $70,000 raise
  mixes two different tax bases without naming that basis anywhere in the file — the prior text
  called $54,000 "measured in equivalent purchasing power," which it is not: converting the rent
  premium to its pre-tax equivalent requires the household's combined marginal tax rate, which
  no named ground truth in this analysis supplies (GT-3 supplies only the near-zero CA-vs-OR
  state differential, not a total marginal rate).
- Result: every site below now calls $54,000 "rent-adjusted" (never "effective" or "purchasing
  power"); the percentage is stated as "roughly 22% less... ($15,600 / $70,000)" with the
  denominator named inline; a new sentence discloses the basis-mixing issue explicitly and names
  the verification that would make an after-tax figure computable (read the household's combined
  marginal rate off the prior-year tax return).
- Sites (origin group): heading (line 53) — "effective" replaced with "rent-adjusted"; final hop
  (line 57) — the percentage re-stated with its denominator, the "measured in equivalent
  purchasing power" framing removed, and the basis-disclosure sentence appended to the same hop;
  confidence paragraph (line 59) — narrowed rather than downgraded (see decision below).
- Sites (restatement group, named by 999.118's table and 44-PATTERNS.md): abandoned-reasoning
  (line 79) — "the nominal figure overstates the real gain by roughly 23%" replaced with both
  ratios and their denominators, and "the effective purchasing-power gain" replaced with "the
  rent-adjusted gain"; section 6 point 3 (line 93) — "the effective compensation figure"
  replaced with "the rent-adjusted compensation figure"; section 6 Trade-offs (line 99) —
  "forgoing an effective ~$54,000/year increase" replaced with "forgoing a rent-adjusted
  ~$54,000/year increase."
- Sites (restatement group found by this plan's own sweep, named by NO upstream artifact —
  44-RESEARCH.md's blast-radius section and 44-PATTERNS.md's per-file table list only lines 53,
  57, 59, 79, 93 and 99):
  - Line 18 (Problem Essence success criterion): "The effective after-cost-of-living-and-tax
    compensation change is calculated explicitly from verifiable facts" promised an after-tax
    purchasing-power computation the corrected chain explicitly states is not computable from
    the named ground truths; restated to require that the basis (pre-tax nominal vs. after-tax
    purchasing power) be named explicitly instead, which is exactly what the corrected chain
    now does.
  - Line 56 (C1's middle hop): "Combined, these reduce the effective purchasing-power gain by
    roughly $15,600/year" restated to "reduce the rent-adjusted nominal gain by roughly
    $15,600/year."
  - Line 67 (C2's hop, citing Chain 1's result): "the effective ~$54K gain (Chain 1)" restated
    to "the rent-adjusted ~$54K gain (Chain 1)."
- Provenance: lines 53/57/59/79/93/99 — 999.118's own table (row `personal-general.md:57,79`)
  and 44-PATTERNS.md's per-file table (which additionally names 53, 59, 93, 99 as restatement
  sites). Lines 18/56/67 — found in this plan's own execution via Task 1's own required
  `/usr/bin/grep -nF 'effective'` sweep; named by no upstream artifact.

**C1 confidence decision: narrowed, kept HIGH (not lowered to MEDIUM).** The plan's Task 1 gave
an explicit choice: narrow the claim and keep HIGH, or — only if narrowing proved impossible
without re-authoring the chain — lower to MEDIUM. Narrowing was possible without touching the
chain's own hop structure or its GT-1/GT-2/GT-3 citations: the corrected confidence paragraph
states exactly what the chain establishes (the rent-adjusted NOMINAL figure, resting entirely on
three verified ground truths) and exactly what it does not (the after-tax purchasing-power
figure, which needs an input — the household's combined marginal rate — that no named ground
truth supplies). No hop was re-derived, re-ordered or re-authored to reach this narrowing; only
the confidence paragraph's own prose was rewritten. HIGH is therefore retained.

### product-business-2.md          (plan 44-03)

**Defect — GT-1's distinct-account inference (origin: lines 52-54; restated at lines 76, 195;
999.118's own table row `product-business-2.md:52-54,76,195`).**
- Inputs (file's own): 41 inbound Slack-integration requests, 240 active accounts, both read
  from GT-1's own stated source (an in-product feedback log + post-cancellation churn-survey
  instrument).
- Operation: `41 / 240 = 0.170833...` (≈17%). The division itself is correct arithmetic, but it
  is the share of ACCOUNTS only if all 41 requests came from 41 DISTINCT accounts — an
  assumption the file's own stated source never establishes, since a feedback log records
  requests, not distinct requesters.
- Result: the 17% figure is re-stated as an upper bound — "at most 41/240, approximately 17%,"
  with the reasoning (the log records requests, not distinct accounts, so the distinct-account
  count is bounded above by 41 and unknown below) and the de-duplication verification path
  (de-duplicate the feedback log by account id) both named inline at the origin site.
- Sites: GT-1 itself (lines 52-54, origin — the raw counts 41 and 240 and the source clause left
  byte-unchanged; only the inference drawn from them was corrected), GT-5? (line 76, restated
  "convert some fraction of the 41 requesting accounts" to "convert some fraction of the
  accounts behind the 41 requests (at most 41)"), section 6 Trade-offs (line 195, restated "some
  fraction of the 41 requesting accounts may quietly disengage" to "some fraction of the
  accounts behind the 41 requests may quietly disengage").
- No further sites found: confirmed via `/usr/bin/grep -n '41\|17%'` across the full
  post-edit file — chains C1, C2 and C3 cite GT-1 by name in their head lines, never by number,
  so no chain hop independently restates the 41/17% figures. This matches 44-RESEARCH.md's own
  finding ("no further sites found beyond what 999.118 already names").
- **GT-1 deliberately NOT given a `?` suffix — reasoning recorded per the plan's own
  instruction.** GT-1's two raw counts (41 requests, 240 accounts) are each read at a named
  source and are themselves verified measurements; what was wrong was the INFERENCE drawn from
  them (that all 41 requests came from 41 distinct accounts), not the counts. The corrected text
  states the derived share as a bound with its assumption named, rather than presenting it as a
  measured fact — this is a correction to the ANALYSIS drawn from GT-1, not a statement that
  GT-1's own underlying facts (the counts) are unverified. The `?` suffix under the shipped rule
  (`output-template.md:114`) marks a ground truth whose own stated fact is unverified,
  unmeasured, preliminary, or not confirmed; here the two facts GT-1 states (41, 240) remain
  fully verified at their named source, so no suffix applies.
- Provenance: 999.118's own table (row `product-business-2.md:52-54,76,195`); 44-RESEARCH.md's
  "Blast-radius findings" item 6; 44-PATTERNS.md's per-file table.

**Citation/line-wrap discrepancy recorded, not silently absorbed.** The plan's own Task 2
acceptance criteria assert `/usr/bin/grep -c '41 inbound Slack-integration requests'
shared/examples/product-business-2.md` returns 1. Read live, this phrase is hard-wrapped across
two lines in the file ("...show 41" / "inbound Slack-integration requests across 240 active
accounts...") — confirmed via `git show HEAD:shared/examples/product-business-2.md | sed -n
'52,54p'` that this wrapping already existed **before** this plan made any edit, so a
single-line grep for the full phrase returns 0 both pre-edit and post-edit; this is a
pre-existing plan-checking assumption that does not hold against the file's actual line-wrap
width, not a defect this plan introduced or a site this plan needed to reflow. The raw counts
themselves are independently confirmed present and unchanged: `/usr/bin/grep -c '240 active
accounts'` returns 1, and GT-1's own two numbers (41, 240) are unchanged by direct reading.


### product-business.md            (plan 44-04)

*(pending - plan 44-04)*

### software-systems.md            (plan 44-04)

*(pending - plan 44-04)*

### science-engineering.md         (plan 44-05)

*(pending - plan 44-05)*

### science-engineering-2.md       (plan 44-06)

*(pending - plan 44-06)*

## ?-suffix / D-07 confidence sweep (999.118 step 3)

Per-file sweeps for the seven defective files above are appended by the plan that owns each file
(44-02 through 44-06).

### personal-general-2.md

Rule, quoted from the interfaces block (`shared/spine/references/output-template.md:114,335`,
`validation-rubric.md:112-116`): (1) any GT whose own text says unverified/unmeasured/
preliminary/not-confirmed must carry the `GT-N?` suffix; (2) a chain whose head cites any
`GT-N?` must end MEDIUM or LOW, never HIGH; (3) the ceiling is transitive — a chain is rated no
higher than the lowest-rated chain its head cites. Applied to every `**GT-N**` bullet and every
chain in this file's own `## 3. Ground Truths` and `## 4. Derivation Chains` sections, read live
after Tasks 1 and 2 of this plan landed. Included in full, including the null result, per the
same discipline plan 44-01 applied to the untested seven.

**GT-level table:**

| File | GT | Clause deciding ?-required | ?-required | ?-present | Verdict |
|---|---|---|---|---|---|
| personal-general-2.md | GT-1 | "source: mortgage note and most recent statement" | no | no | OK |
| personal-general-2.md | GT-2 | "source: prior-year federal return + current standard-deduction figure... source: GT-1 × (1 − 0) = 6.25%" | no | no | OK |
| personal-general-2.md | GT-3? | "unverified: this is a central estimate from a historical distribution and is not a forward-looking measurement" | yes | yes | OK |
| personal-general-2.md | GT-4 | "source: prior-year federal+state return at current income level" | no | no | OK |
| personal-general-2.md | GT-5 | "source: direct verification of household cash position" | no | no | OK |
| personal-general-2.md | GT-6 | "source: amortisation arithmetic" — a computation over GT-1's already-verified mortgage terms, not itself an unverified belief | no | no | OK |

**Chain-level table:**

| File | Chain | Head-line citations | Confidence | Cites a `GT-N?` on head | Rule 2 holds | Rule 3 holds |
|---|---|---|---|---|---|---|
| personal-general-2.md | C1 | GT-1 + GT-2 + GT-3? + GT-4 | LOW | yes (GT-3?) | yes (not HIGH) | yes (no chain cited) |
| personal-general-2.md | C2 | GT-1 + GT-2 + GT-3? + GT-4 | LOW | yes (GT-3?) | yes (not HIGH) | yes (no chain cited) |
| personal-general-2.md | C3 | GT-5 | MEDIUM | no (head names only GT-5; the file's own Confidence prose explicitly ties the MEDIUM rating to the `GT-3?` dependency inherited indirectly from Chains 1 and 2 — "The `GT-3?` dependency from Chains 1 and 2 carries through indirectly") | yes | yes |

**Sweep result for personal-general-2.md: zero violations found.** GT-3? is the file's only
Ground Truth whose own text states unverified/preliminary language, and it already carries the
`?` suffix. Both chains whose head cites `GT-3?` (C1, C2) are rated LOW, well under the HIGH
ceiling rule 2 forbids. C3, which cites no `GT-N?` on its head line, is rated MEDIUM and its own
Confidence prose correctly discloses the transitive `GT-3?` dependency it inherits from C1/C2
rather than claiming HIGH — rule 3 holds. The file-level `## 6. Conclusion` Confidence line is
MEDIUM, consistent with the lowest-rated chain contributing to it. This matches the CONF-GATE
floors interface block's `high_conf_chains = 0` for this file (C1 LOW, C2 LOW, C3 MEDIUM,
section 6 MEDIUM) — confirmed unchanged by this plan's edits, since no `**Confidence:**` label
anywhere in the file was moved by Tasks 1 or 2. No edit was required as a result of this sweep.

### personal-general.md

Rule, quoted from the interfaces block (`shared/spine/references/output-template.md:114,335`,
`validation-rubric.md:112-116`): (1) any GT whose own text says unverified/unmeasured/
preliminary/not-confirmed must carry the `GT-N?` suffix; (2) a chain whose head cites any
`GT-N?` must end MEDIUM or LOW, never HIGH; (3) the ceiling is transitive — a chain is rated no
higher than the lowest-rated chain its head cites. Applied to every `**GT-N**` bullet and every
chain in this file's own `## 3. Ground Truths` and `## 4. Derivation Chains` sections, read live
after Task 1 of this plan landed. Included in full, including the null result.

**GT-level table:**

| File | GT | Clause deciding ?-required | ?-required | ?-present | Verdict |
|---|---|---|---|---|---|
| personal-general.md | GT-1 | "source: offer letter from the prospective employer" | no | no | OK |
| personal-general.md | GT-2 | "source: rental market listings... approximate figures... illustrative and verifiable" — a sourced, directionally-verifiable estimate, not a stated-unverified claim | no | no | OK |
| personal-general.md | GT-3 | "source: California Franchise Tax Board and Oregon Department of Revenue published rate schedules (illustrative... the directional effect... is verifiable from current published schedules)" | no | no | OK |
| personal-general.md | GT-4 | "source: direct statement from the partner (a current constraint; verified by statement, not external data)" | no | no | OK |
| personal-general.md | GT-5 | "source: direct statement by the person... verified by direct statement, not by external measurement. It is not inferred or assumed" | no | no | OK |

**Chain-level table:**

| File | Chain | Head-line citations | Confidence | Cites a `GT-N?` on head | Rule 2 holds | Rule 3 holds |
|---|---|---|---|---|---|---|
| personal-general.md | C1 | GT-1 + GT-2 + GT-3 | HIGH | no (no `GT-N?` exists in this file) | yes (no `GT-N?` cited, so rule 2 imposes no ceiling) | yes (no chain cited on head) |
| personal-general.md | C2 | GT-5 + GT-4 | MEDIUM | no | yes | yes |

**Sweep result for personal-general.md: zero violations found.** This file has no `GT-N?` at
all — every Ground Truth is sourced directly (an offer letter, published rental listings,
published state tax schedules, or a direct statement recorded as verified by statement) and none
of the five bullets' own text states unverified/unmeasured/preliminary/not-confirmed language.
Rule 2 therefore imposes no ceiling on either chain, and C1's HIGH rating (kept, narrowed, per
this plan's Task 1 confidence decision above) is consistent with the rule either way. Rule 3
holds trivially: neither chain's head line cites the other chain, and section 6's own Confidence
line (MEDIUM) correctly reflects the lower of the two chains it synthesizes ("(chains C1 and
C2)"). This matches the CONF-GATE floors interface block's `high_conf_chains = 1` for this file
(C1 HIGH, C2 MEDIUM, section 6 MEDIUM) — confirmed unchanged by this plan's edits, since the
narrow-and-keep-HIGH decision did not move any `**Confidence:**` label. No edit was required as
a result of this sweep.

### product-business-2.md

Rule, quoted as above. Applied to every `**GT-N**` bullet and every chain in this file's own
`## 3. Ground Truths` and `## 4. Derivation Chains` sections, read live after Task 2 of this
plan landed.

**GT-level table:**

| File | GT | Clause deciding ?-required | ?-required | ?-present | Verdict |
|---|---|---|---|---|---|
| product-business-2.md | GT-1 | "source: in-product feedback log + post-cancellation churn-survey instrument" — the two raw counts (41, 240) are directly sourced and verified; the corrected text states the DERIVED share as a bound, which is a correction to the inference, not a statement that GT-1's own facts are unverified (see the no-suffix reasoning in the re-derivation section above) | no | no | OK |
| product-business-2.md | GT-2 | "source: support-ticket export tagged `reporting-limitation`, cross-referenced with the account-management ARR roll-up" | no | no | OK |
| product-business-2.md | GT-3 | "source: signed LOI filed with finance and legal" | no | no | OK |
| product-business-2.md | GT-4 | "source: engineering manager's capacity plan, derived from headcount × historical sustained ship velocity" | no | no | OK |
| product-business-2.md | GT-5? | "unverified: no churn-survey reason code attributes departure to the missing integration, and no win/loss instrument isolates Slack-integration absence... The retention-delta and acquisition-uplift magnitudes are unmeasured" | yes | yes | OK |

**Chain-level table:**

| File | Chain | Head-line citations | Confidence | Cites a `GT-N?` on head | Rule 2 holds | Rule 3 holds |
|---|---|---|---|---|---|---|
| product-business-2.md | C1 | GT-2 + GT-3 | MEDIUM | no (head cites no `GT-N?`; the file's own Confidence prose explicitly ties the downgrade to `GT-5?`'s unmeasured Slack-side magnitudes even though the head line only names GT-2/GT-3) | yes (not HIGH regardless) | yes (no chain cited on head) |
| product-business-2.md | C2 | GT-1 + GT-3 | HIGH | no (GT-1 correctly carries no suffix per the reasoning above; GT-3 carries none either) | yes (no `GT-N?` cited, so rule 2 imposes no ceiling) | yes |
| product-business-2.md | C3 | GT-5? + GT-4 | MEDIUM | yes (`GT-5?`) | yes (not HIGH) | yes |

**Sweep result for product-business-2.md: zero violations found.** GT-5? is the file's only
Ground Truth whose own text states unverified/unmeasured language, and it already carries the
`?` suffix — confirmed unchanged by this plan's edits (`GT-5?` count is 9 both pre- and
post-edit). GT-1 correctly carries no suffix under the reasoning recorded above: its own stated
facts are sourced and verified; only the inference drawn from them was corrected. C3, whose head
cites `GT-5?`, is rated MEDIUM, satisfying rule 2. C2, whose head cites GT-1 and GT-3 (neither
carrying `?`), is rated HIGH — rule 2 imposes no ceiling here since no `GT-N?` is cited, so this
is consistent with the rule. C1 is rated MEDIUM for a reason its own prose discloses (the GT-5?
dependency) even though its head line does not name GT-5? directly — the same transitive-
disclosure pattern the personal-general-2.md sweep recorded for its own C3. Section 6's own
Confidence line ("(chains C1 and C3)" MEDIUM) correctly reflects the lower of the two chains it
names. This matches the CONF-GATE floors interface block's `high_conf_chains = 1` for this file
(C1 MEDIUM, C2 HIGH, C3 MEDIUM, section 6 MEDIUM) — confirmed unchanged by this plan's edits,
since no `**Confidence:**` label anywhere in the file was moved by Task 2. No edit was required
as a result of this sweep.

### Pre-registered conformance expectation (plan 44-03, Task 3 Part C)

Written BEFORE running `sync-content.py --write` or `report-conformance.py`, per the plan's own
instruction that the expected movement be pre-registered ahead of regeneration.

**Pre-registration:** Task 1's C1 confidence decision (personal-general.md) kept HIGH (narrowed,
not lowered to MEDIUM — see the re-derivation section above). Under the plan's own stated rule,
this means: no `**Confidence:**` label was moved anywhere in either touched file by Tasks 1 or
2, so no measured conformance value should move. `docs/conformance-baseline.md`'s and
`docs/data/conformance.json`'s per-artifact rows for `shared/examples/personal-general.md`,
`shared/examples/product-business-2.md` and their generated twins are expected to be
byte-identical before and after regeneration — the regenerated twins should differ from the
sources by nothing but the `GENERATED_MARKER` header line, and `report-conformance.py --check`
should report no drift.

**Observed outcome, live:** matched the pre-registration exactly. `python3
scripts/sync-content.py --write` followed by `--check` (exit 0); `git diff --stat -- 
docs/conformance-baseline.md docs/data/conformance.json` printed nothing both before and after
`python3 scripts/report-conformance.py` (regenerate) and `--check` (`report-conformance: PASS —
no drift`) — zero bytes moved in either conformance artifact. `python3 scripts/check-conf-gate.py`
initially FAILED with `D-08(a) mutation site not found (or not unique)` and `D-08(c) mutation
site not found (or not unique)` in `shared/examples/personal-general.md` — this is
`scripts/check-conf-gate.py`'s own D-08 anti-vacuity arm, which pins three literal substrings
transcribed from `personal-general.md`'s live text (`_D08_HOP_NEEDLE`, `_D08_CELL_NEEDLE`,
`_D08_CITE_NEEDLE`) to prove its synthetic-mutation self-check still locates a real site; Task 1's
edits removed the word "effective" from the two needles the hop (line 57) and the citation
(line 93) sites depend on, exactly the "a future edit to this file that removes one of these
needles" case the script's own comment names. Fixed by re-transcribing `_D08_HOP_NEEDLE` and
`_D08_CITE_NEEDLE` (and their paired `_REPLACEMENT` constants) from the corrected text in
`scripts/check-conf-gate.py` — a Rule 3 blocking-issue auto-fix on apparatus code, not a product
content change; `_D08_CELL_NEEDLE` (the Assumptions Table verdict cell) was untouched by Task 1
and needed no change. Re-run: `check-conf-gate.py --self-test` (`SELF-TEST PASS — 44 controls
run`) and the live run (`check-conf-gate: PASS`, with all three D-08 arms reporting their
expected single-defect increment). `python3 scripts/gen-gate-docs.py --check` (harvested 19/19,
exit 0). `python3 scripts/check-version-stamps.py` (17 stamps, all `9.3.2`, PASS). Both twin
diffs (`diff <(tail -n +3 <twin>) <source>`) printed nothing. `git diff --quiet HEAD --
tests/adversarial-corpus-v9.0 shared/examples/self-application.md` exited 0 (both byte-unchanged).
`bash scripts/check-firewall-battery.sh` printed `FIREWALL: GREEN (23/23)`, reproducing the
pre-edit baseline exactly (23/23, same gate set). No movement occurred outside the pre-registered
set — the one deviation (the D-08 needle re-pin) was in apparatus code required to make the
already-pre-registered "no measured value moves" outcome observable, not a movement of a measured
conformance value itself.

### Untested seven

Rule, quoted from the interfaces block (`shared/spine/references/output-template.md:114,335`,
`validation-rubric.md:112-116`): (1) any GT whose own text says unverified/unmeasured/
preliminary/not-confirmed must carry the `GT-N?` suffix; (2) a chain whose head cites any
`GT-N?` must end MEDIUM or LOW, never HIGH; (3) the ceiling is transitive — a chain is rated no
higher than the lowest-rated chain its head cites. Applied below to every `**GT-N**` bullet and
every chain in each of the seven untested files. Included in full, including the files where the
sweep found nothing to flag — a sweep that records only hits cannot be distinguished from a
sweep that was never run.

**GT-level table** (one row per Ground Truth bullet in each file's own `## 3. Ground Truths`
section; `?-required` is derived from whether the bullet's own text states unverified/
unmeasured/preliminary/not-confirmed language):

| File | GT | Clause deciding ?-required | ?-required | ?-present | Verdict |
|---|---|---|---|---|---|
| estimate-fermi.md | GT-4 | "source: published material data for Solar Salt (direct measurement)" | no | no | OK |
| estimate-fermi.md | GT-5 | "source: NREL direct measurement" | no | no | OK |
| estimate-fermi.md | GT-6 | "source: BloombergNEF direct measurement" | no | no | OK |
| theoretical-limit-carnot.md | GT-4 | "source: published material data for Solar Salt (direct measurement)" | no | no | OK |
| decompose-irreducibility.md | GT-1 | "physical law: P = I²R / Ohm's law; confirmed by equipment specifications" | no | no | OK |
| decompose-irreducibility.md | GT-2 | "Fourier's law governs thermal loss... Actual loss rate... is design-dependent and must be sourced" (governing law verified; the design-specific rate is a separate, correctly-unnamed input) | no | no | OK |
| decompose-irreducibility.md | GT-3 | "physical law: second law of thermodynamics... confirmed by published operational data" | no | no | OK |
| decompose-irreducibility.md | GT-4 | "direct measurement: published phase diagrams... verified in commercial CSP plant operating records" | no | no | OK |
| decompose-irreducibility.md | GT-5 | "direct measurement: NREL engineering cost estimates, 2023" | no | no | OK |
| decompose-irreducibility.md | GT-6 | "direct measurement: BloombergNEF 2023 market survey" | no | no | OK |
| decompose-irreducibility.md | GT-7? | "unverified — requires the tank engineering specification and insulation material datasheet (source: not yet obtained)" | yes | yes | OK |
| decompose-irreducibility.md | GT-8? | "unverified — requires the project financial model" | yes | yes | OK |
| ishikawa-fishbone.md | GT-1 | "source: company subscription and CRM records, verified against the billing system" | no | no | OK |
| ishikawa-fishbone.md | GT-2 | "source: CS team exit-interview log... reviewed and confirmed by the CS Director" | no | no | OK |
| ishikawa-fishbone.md | GT-3 | "source: CS Director debrief; headcount and customer-count figures from HR and CRM records" | no | no | OK |
| ishikawa-fishbone.md | GT-4 | "source: CS Director debrief; no documented mid-year capacity-review procedure exists" | no | no | OK |
| ishikawa-fishbone.md | GT-5? | "source: unverified; preliminary estimate from 4 accounts, not a statistically valid sample" | yes | yes | OK |
| software-systems-2.md | GT-1 | "source: direct team-experience inventory... verified by 1:1 confirmation" | no | no | OK |
| software-systems-2.md | GT-2 | "source: company finance and pipeline records" | no | no | OK |
| software-systems-2.md | GT-3 | "source: provider pricing pages, retrieved at the analysis date" — a verified snapshot of what is currently published, distinct from GT-3?'s claim about the future trajectory | no | no | OK |
| software-systems-2.md | GT-3? | "unverified: list prices are a snapshot, not a contract; the 24-month cost path depends on..." | yes | yes | OK |
| software-systems-2.md | GT-4 | "source: published engineering retrospectives... cross-referenced against the team-experience GT-1" | no | no | OK |
| software-systems-2.md | GT-5 | "source: published provider documentation... cross-referenced with engineering write-ups" | no | no | OK |
| software-systems-2.md | GT-6 | "source: direct observation of the team's current infrastructure" | no | no | OK |
| composed-inversion-second-order.md | GT-1 through GT-4 | all cite direct measurement / engineering records (full text not re-quoted here; re-read live, none contains unverified/unmeasured/preliminary/not-confirmed language) | no | no | OK |
| composed-inversion-second-order.md | GT-5? | "load-bearing, unverified" (per the chain head citation quoting it) | yes | yes | OK |
| self-application.md | GT-1 through GT-8 | all cite direct measurement of the repository / requirements file / scripts (full text not re-quoted here; re-read live, none contains unverified/unmeasured/preliminary/not-confirmed language) | no | no | OK |
| self-application.md | GT-9? | "unverified: no measurement exists in this repository that ties body line count to agent reasoning quality" | yes | yes | OK |

**Chain-level table** (one row per `### Conclusion CN` in each file's `## 4. Derivation Chains`;
"cites GT-N?" is checked against the chain's own head line, since that is what rules 2/3 bind on):

| File | Chain | Head-line citations | Confidence | Cites a `GT-N?` on head | Rule 2 holds | Rule 3 holds |
|---|---|---|---|---|---|---|
| estimate-fermi.md | C1 | GT-4 + GT-5 + GT-6 | HIGH | no | yes (no `GT-N?` cited) | yes (no chain cited) |
| theoretical-limit-carnot.md | C1 | GT-4 | HIGH | no | yes | yes |
| decompose-irreducibility.md | C1 | GT-1 + GT-2 + GT-3 | HIGH | no | yes | yes |
| ishikawa-fishbone.md | C1 | GT-2 + GT-3 | HIGH | no | yes | yes |
| ishikawa-fishbone.md | C2 | GT-3 + GT-4 | HIGH | no | yes | yes |
| ishikawa-fishbone.md | C3 | GT-1 + GT-5? | MEDIUM | yes (GT-5?) | yes (not HIGH) | yes (no chain cited) |
| software-systems-2.md | C1 | GT-4 + GT-3 | MEDIUM | no (cites GT-3, not GT-3?; downgraded anyway for the unverified team-capability hinge named in Section 2) | yes (not HIGH; not required to be, since head cites no `GT-N?`, but is not HIGH regardless) | yes |
| software-systems-2.md | C2 | GT-5 + GT-2 | MEDIUM | no (cites GT-2, not GT-3?; prose references GT-3?'s pricing trajectory inside a hop, not on the head line) | yes | yes |
| software-systems-2.md | C3 | GT-6 + GT-1 + GT-5 | HIGH | no | yes | yes |
| composed-inversion-second-order.md | C1 | GT-1 + GT-2 + GT-5? | MEDIUM | yes (GT-5?) | yes (not HIGH) | yes |
| self-application.md | C1 | GT-7 + GT-8 + GT-9? | MEDIUM | yes (GT-9?) | yes (not HIGH) | yes |
| self-application.md | C2 | GT-1 + GT-2 + GT-3 + GT-5 | HIGH | no | yes | yes |
| self-application.md | C3 | GT-4 + GT-5 + GT-6 + GT-8 | MEDIUM | no (head cites no `GT-N?`; the file's own Confidence prose explicitly ties the MEDIUM rating to chain C1's GT-9? dependency, applying rule 3's transitivity even though the head line only names GTs, not `C1`) | yes | yes |

**Sweep result for the untested seven: zero violations found.** Every unverified Ground Truth in
all seven files already carries the `?` suffix; no chain whose head cites a `GT-N?` is rated
above MEDIUM; the file-level `## 6. Conclusion` Confidence line in every file that has an
unverified dependency (`ishikawa-fishbone.md`, `software-systems-2.md`,
`composed-inversion-second-order.md`, `self-application.md`) is correctly capped at MEDIUM. No
edit was required in any of the six editable files as a result of this sweep.

## Untested-exemplar re-derivation (999.118 step 4)

All seven files were read in full (`## 3. Ground Truths` and `## 4. Derivation Chains`, plus any
preceding technique-specific drill section) and every re-derivable figure was independently
re-computed with `python3 -c` in this session — not copied forward from 44-RESEARCH.md's own
first pass. All six editable files' arithmetic is CONFIRMED with zero disagreements; no edit was
required in any of them.

### estimate-fermi.md — CONFIRMED

| Figure | File states | Re-computed |
|---|---|---|
| `Q/m = c_p × ΔT` | 418 kJ/kg | `1.52 × 275 = 418.0` — CONFIRMED |
| kWh/kg | ≈0.116 kWh/kg | `418 / 3600 = 0.11611...` — CONFIRMED |
| `material_mass` | 8.6 kg/kWh | `1 / 0.11611... = 8.6124...` ≈ 8.6 — CONFIRMED |
| Central `capital_per_kWh` | $20.6/kWh | `8.6 × 0.60 × 4 = 20.64` ≈ $20.6 — CONFIRMED |
| Lower bound | $12.0/kWh | `8.6 × 0.40 × 3.5 = 12.04` ≈ $12.0 — CONFIRMED |
| Upper bound | $34.4/kWh | `8.6 × 0.80 × 5.0 = 34.4` — CONFIRMED (exact) |

Classification: (a) carries extensive re-derivable arithmetic; every figure re-derives cleanly.

### theoretical-limit-carnot.md — CONFIRMED

| Figure | File states | Re-computed |
|---|---|---|
| `η_Carnot = 1 − T_cold/T_hot` | ≈33% | `1 - 563/838 = 0.32816...` ≈ 33% — CONFIRMED |
| Gap, lower | 8 points | `33 - 25 = 8` — CONFIRMED |
| Gap, upper | 13 points | `33 - 20 = 13` — CONFIRMED |

Classification: (a) carries re-derivable arithmetic; both the Carnot fraction and the two gap
subtractions re-derive cleanly.

### decompose-irreducibility.md — CONFIRMED

| Figure | File states | Re-computed |
|---|---|---|
| `C1a × C1b × C1c` | ≈38% | `0.97 × 0.99 × 0.40 = 0.38412` ≈ 38% — CONFIRMED |
| `η_Carnot = 1 − 303/838` | ≈63.8% | `1 - 303/838 = 0.63842...` ≈ 63.8% — CONFIRMED |

Classification: (a) carries re-derivable arithmetic; both figures re-derive cleanly. This file
carries 2 of the project's 4 ratcheted `no chain — flagged assumption only` marked claims
(§6 Key insight bullets 2 and 3) — confirmed present and unmodified by this task; the project-wide
count in `shared/examples/*.md` is confirmed at 2 (matching the pre-registered `_MARKED_RATCHET`
reading of 4 once the generated twin is counted), unchanged by this task.

### ishikawa-fishbone.md — CONFIRMED

| Figure | File states | Re-computed |
|---|---|---|
| Churn increase | 124% increase | `(9.2 - 4.1) / 4.1 = 1.24390...` ≈ 124% — CONFIRMED |

Classification: (a) carries re-derivable arithmetic; the single percentage figure re-derives
cleanly.

### software-systems-2.md — CONFIRMED

| Figure | File states | Re-computed |
|---|---|---|
| Build 3-yr TCO, low bound | ≈$54K | `0.1 × 15000 × 36 = 54000` — CONFIRMED |
| Build 3-yr TCO, high bound | ≈$90K | `0.1 × 25000 × 36 = 90000` — CONFIRMED |
| Build 3-yr TCO, upper FTE, low | ≈$162K | `0.3 × 15000 × 36 = 162000` — CONFIRMED |
| Build 3-yr TCO, upper FTE, high | ≈$270K | `0.3 × 25000 × 36 = 270000` — CONFIRMED |
| Build ongoing, low | $1,500/month | `0.1 × 15000 = 1500` — CONFIRMED |
| Build ongoing, high | $7,500/month | `0.3 × 25000 = 7500` — CONFIRMED |

The buy-path 3-year cumulative ranges ($15K–$40K, $40K–$100K, `## 5. Abandoned Reasoning`) are
stated as illustrative given the $200–800/month published pricing without a fully shown
per-tier-crossing derivation to the same precision as the figures above. **Recorded as
lower-precision prose, per 44-RESEARCH.md's own classification — NOT a defect, and NOT "fixed"**;
the buy-path monthly figures the file's chains actually reason from (GT-3's $200–$800/month
range) are themselves a direct-measurement citation, not a computed figure, so there is nothing
to re-derive at that layer.

Classification: (a) carries re-derivable arithmetic; every fully-shown computation re-derives
cleanly; the illustrative buy-path totals are intentionally lower-precision and out of scope for
re-derivation.

### composed-inversion-second-order.md — nothing to re-derive

Exhaustive numeric-pattern sweep: `/usr/bin/grep -nE '[0-9]+(\.[0-9]+)?%|\$[0-9]|[0-9]+\.[0-9]+' shared/examples/composed-inversion-second-order.md` returns **1 hit**, not zero as
44-RESEARCH.md's first pass reported — recorded as actually observed, not as expected. The hit
(line 204, "...contract implications of step 3.2) become non-actionable in the...") is a
cross-reference to a numbered analysis step ("step 3.2"), matched by the pattern's
`[0-9]+\.[0-9]+` branch as a false positive — it names a section of this file's own prose, not a
quantity, dollar figure, or percentage with an underlying computation. There is no re-derivable
numeric content in this file.

Classification: (c) qualitative — no re-derivable numeric content.

### self-application.md — CONFIRMED, arithmetic; staleness flagged, not fixed (D-03)

Not edited in this phase — read and swept only, per D-03. Every figure is internally
self-consistent with the file's own stated inputs:

| Figure | File states | Re-computed |
|---|---|---|
| Four-segment decomposition | 44+96+99+175+464 = 878 | `44+96+99+175+464 = 878` — CONFIRMED, matches GT-1's stated 878-line total |
| Body after methodology extraction | 878−96 = 782 | `878-96 = 782` — CONFIRMED |
| Overage after methodology extraction | 782−500 = 282 | `782-500 = 282` — CONFIRMED |
| Body after appendix de-inlining | 878−464 = 414 | `878-464 = 414` — CONFIRMED |
| Appendix share of body | 464/878 ≈ 53% | `464/878 = 0.52847...` ≈ 53% — CONFIRMED |
| GT-4 combined reference-file line count | 150+320 = 470 | `150+320 = 470` — CONFIRMED |

Zero arithmetic defects. **Staleness finding, recorded here per 999.118 step 4 and filed as
backlog 999.124 (Task 3 of this plan), not fixed in this phase (D-03):**

- GT-1 states the agent body is **878 lines** "as measured by `wc -l` at the time of this
  analysis." Live re-read: `wc -l first-principles/agents/first-principles.md` = **807 lines**,
  not 878 — 71 fewer than the file's own stated GT-1 figure.
- GT-5/GT-6/chain C3/§6 describe the Output Template and Validation Rubric appendices as
  currently **inlined** in the agent body (`## How to Use This Template` through end-of-file,
  ~464 lines). Live re-read: `/usr/bin/grep -n '^## How to Use This Template\|^## Self-Audit
  Gate' first-principles/agents/first-principles.md` returns **zero** matches — the appendix
  headings are not present; the body instead links out
  (`/usr/bin/grep -c 'output-template.md\|validation-rubric.md'
  first-principles/agents/first-principles.md` = **8** live reference-link occurrences, not the
  "five live reference links" 44-RESEARCH.md's own first pass reported — recorded as actually
  observed). The appendices are de-inlined.
- GT-7/GT-8 describe **META-Q4** as a binding line-count regression gate recorded in
  `.planning/REQUIREMENTS.md`. Live: `.planning/REQUIREMENTS.md` does not exist in this
  repository's current tree (`.planning/` carries no `REQUIREMENTS.md`; the project's
  requirements surface is `docs/requirements-traceability.md`, per `./CLAUDE.md`'s
  "Requirements surface" section), and `./CLAUDE.md`'s own Key Invariants section states
  plainly: "The agent body's line count is **not** an invariant: the 644-line gate was retired
  under TEARDOWN-01... and nothing reports or gates it." META-Q4 is retired.
- Chain C3's recommended intervention — de-inline the Output Template and Validation Rubric
  appendices, replacing them with reference links — **has, in fact, already been executed** by a
  later phase (confirmed by the zero-inlined-heading and eight-live-link findings above). The
  exemplar's conclusion is not wrong; its premises (GT-1, GT-5, GT-7) describe a repository state
  that has since changed. This is a citation-currency defect, not an arithmetic one — every
  number the file computes from its own stated inputs is correct; the inputs themselves are
  dated.

Classification: (a) carries extensive, fully self-consistent re-derivable arithmetic, with a
disclosed currency issue in its Ground Truths, not its computation. Filed as backlog 999.124 in
Task 3 of this plan; the file itself is byte-unchanged by this phase (D-03).

## Adversarial-corpus inheritance (recorded, never fixed - D-05)

The corpus is FROZEN-EVIDENCE (`_FROZEN_PATHS` in `scripts/check-firewall-battery.sh`) and was
NOT edited by this phase — confirmed by `git diff --quiet HEAD -- tests/adversarial-corpus-v9.0`
exiting 0 throughout this plan. Built directly from
`tests/adversarial-corpus-v9.0/catalog.md`'s own `derived:` column (read live, not copied from
44-RESEARCH.md's table), the eight items that are `derived:` copies of the seven exemplars this
phase touches:

| Corpus item | Derived from | Stratum | Which Phase 44 defect it inherits | Which plan corrects the source |
|---|---|---|---|---|
| T-01 | `personal-general` | B2 | `personal-general.md`'s C1/§5 pre/post-tax mixing defect (999.118 row `personal-general.md:57,79`) | plan 44-03 |
| T-02 | `science-engineering-2` | B1 | `science-engineering-2.md`'s GT-2/C1 Hertz-depth-not-reproducible defect (999.118 row `science-engineering-2.md:70,113`) | plan 44-06 |
| T-07 | `product-business` | B2 | `product-business.md`'s C3/§6 dimensionally-inconsistent break-even formula (999.118 row `product-business.md:67,88`) | plan 44-04 |
| T-08 | `personal-general-2` | B2 | `personal-general-2.md`'s C1/C2/GT-6 after-tax and amortization defects (999.118 row `personal-general-2.md:52,61,62,71-72`) | plan 44-02 |
| T-09 | `science-engineering` | B2 | `science-engineering.md`'s GT-2 derating-factor claim and the 1.8/1.6 kWh/day threshold defect (999.118 row `science-engineering.md:55,108,124,162`) | plan 44-05 |
| T-11 | `product-business-2` | B2 | `product-business-2.md`'s GT-1 41/240-distinct-account inference defect (999.118 row `product-business-2.md:52-54,76,195`) | plan 44-03 |
| T-12 | `product-business` | B2 | Same `product-business.md` source as T-07 (999.118 notes this is "the same source as T-07, different citation form") | plan 44-04 |
| T-14 | `software-systems` | B2 | `software-systems.md`'s GT-3/C1 invalid "mechanically blocked"/"sufficient explanation" claim (999.118 row `software-systems.md:68,91`) | plan 44-04 |

This live read exactly matches 999.118's own "Eight of its items are copies of these exemplars"
claim and 44-RESEARCH.md's Question 3 table — no discrepancy found.

**Stated plainly:** these eight corpus items now carry an arithmetic/citation defect their own
catalog entry does not name, ALONGSIDE the falsehood the catalog does name and that each item was
constructed to demonstrate. The catalog's own `What is false` column documents only the
deliberately-injected falsehood (e.g. T-08's verdict/Type incoherence); it says nothing about the
fact that the underlying dollar figures, thresholds, or claims it inherited from its source
exemplar were themselves wrong before 999.118/Phase 44 corrected them. Anything built on this
corpus as a validation set — starting with backlog 999.4's semantic claim-to-chain judge, which
consequence 2 of that entry already names as needing "a verified-clean negative class" — must
read this section first: the corpus items are not a clean negative-class representative of their
source exemplars until the reader accounts for this second, uncatalogued layer of wrongness. A
cross-reference sentence pointing here has been added under backlog 999.4's own entry in
`.planning/ROADMAP.md` (consequence 2's paragraph), discharging 999.118's "record the inheritance
where the corpus is next read as a validation set" constraint.

## Finding

*(pending - plan 44-06)*

## Why registering this path is not a new gate

`FROZEN-EVIDENCE` in `scripts/check-firewall-battery.sh` (confirmed by direct read of lines
740-787) is an inline check whose `TOTAL=$((TOTAL + 1))` line fires exactly once, unconditionally,
**outside** any loop over `_FROZEN_PATHS` — there is no per-array-element loop anywhere in the
check; the entire array is passed as a single pathspec to one `git diff --quiet HEAD --
"${_FROZEN_PATHS[@]}"` call and one `git status --porcelain --untracked-files=all --
"${_FROZEN_PATHS[@]}"` call, and the pass/fail printf plus the `TOTAL`/`PASS` increments happen
once after both. Registering `tests/exemplar-rederivation-v9.4` as one more `_FROZEN_PATHS` entry
therefore adds zero to the battery's 23/23 tally and registers no new gate — which is what keeps
this phase inside `.planning/STATE.md` standing instruction 2 ("No new registered gate. A battery
or CI total may fall only for a gate named in a successor retirement record"). Verified directly
against the live script text in this session, not copied from the `tests/confidence-transitivity-
v9.4/README.md` precedent's own claim.

This plan (44-01) deliberately does NOT add the registration — plan 44-06 does that once the
artifact reaches its final, post-edit form. Registering an in-flight file here would make
`FROZEN-EVIDENCE` fail on every subsequent plan's edit to this same README, since the check reads
`git diff --quiet HEAD` over the registered pathspec and every plan 44-02 through 44-07 commits a
content change to this file.

## Frozen-evidence discipline

Once registered by plan 44-06, this file (and any sibling file placed in
`tests/exemplar-rederivation-v9.4/`) is committed as-is and never regenerated or silently
hand-edited to match a later result. A correction to something already committed here would be
recorded as a dated, additive erratum appended below the point of error — following the pattern
`tests/confidence-transitivity-v9.4/README.md`'s own "Erratum" section uses — never as a rewrite
of the original text. Until plan 44-06's registration lands, this file is an ordinary tracked file
under active construction across this phase's plans; the discipline described in this section
begins to apply once `_FROZEN_PATHS` names it.

`FROZEN-EVIDENCE`'s protection has a documented gap, carried forward from the precedent: it is a
`git diff --quiet HEAD` over the registered pathspec plus a separate untracked-files sweep. It
catches an edit to a file already tracked at HEAD, and it catches an untracked file appearing
inside the directory — but a committed `git rm` of one of these files passes it clean. It is
tamper-evidence for modification, not a deletion guard.
