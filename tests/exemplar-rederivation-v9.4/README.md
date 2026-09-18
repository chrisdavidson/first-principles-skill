# v9.4 Exemplar Re-Derivation Fixture — backlog 999.118

**Captured:** 2026-09-18. **Status:** frozen hand re-derivation record, appended to (never
rewritten) across plans 44-01 through 44-07. This fixture is NOT registered in
`scripts/check-firewall-battery.sh`'s `_FROZEN_PATHS` array by this plan — plan 44-06 adds that
registration once the artifact is final (registering it now would make `FROZEN-EVIDENCE` fail on
every later plan's in-flight edit to this same file).

## Chain of custody

- **Repo HEAD SHA at the start of Phase 44:** `f7efc17febdfadc62e682d06f40d98017032828d` (read via
  `git rev-parse HEAD` before this plan's Task 1 made any edit).
- **Repo HEAD SHA at the end of Phase 44's content corrections:**
  `bcf8a886d7d066643b30b3a974b7dae81614eeab` (`bcf8a88`) — plan 44-06's `fix(44-06): supply
  science-engineering-2.md's missing Hertz contact geometry` commit, the last commit to touch a
  `shared/examples/*.md` source file or its generated twin in this phase, confirmed via `git
  rev-parse bcf8a88`. This plan (44-07) adds no further edit to any `shared/examples/*.md` file —
  its own commits (this artifact's completion, the `_FROZEN_PATHS` registration, and the
  `.planning/ROADMAP.md` plan-list update) are administrative, not content corrections, so
  `bcf8a88` is the SHA every `git diff --quiet <phase-start-SHA> -- shared/examples/...` and
  per-file source-hash comparison in this section is checked against.
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
| shared/examples/product-business.md | `d948f9fda657dba4fc8c66fd9e60c5846d837c8b78655e1c2b41d2a8fe2b42c4` | 94 | `a0dc5e9257c13b338052accd3e425603301b2b511a6ecbc362f3a9b8a319d826` | 94 |
| shared/examples/science-engineering-2.md | `282db9d21c058c7ed1dd05df45dd328eded851a7bb1d1ae7e38e379f09264aa5` | 218 | `7b8a87f2b5d91b4c8cb9e3e04a8b1e552aa9be255cddc3348e613756a47022ba` | 234 |
| shared/examples/science-engineering.md | `d5aed303b62e07f1d7ab00e4d171af2ef60a02e9009af156336095b4f4bdfe54` | 187 | `9fecf530d5f18622196b5c25e98bf70d9fe9ab324e33d41d4db78d3b771a6e41` | 198 |
| shared/examples/self-application.md | `47adb0226654cb6246b0004d83c399a81431ebcba98f9509fd61228beda0ce11` | 399 | `47adb0226654cb6246b0004d83c399a81431ebcba98f9509fd61228beda0ce11` (IDENTICAL to pre-edit — D-03, confirmed by `git diff --quiet HEAD -- shared/examples/self-application.md` exiting 0 at the phase's final HEAD SHA below) | 399 |
| shared/examples/software-systems-2.md | `66c6548e402398c5f2c18acca34b5323d10a9ab6781754251034f265b5d9d596` | 346 | `66c6548e402398c5f2c18acca34b5323d10a9ab6781754251034f265b5d9d596` (unchanged — plan 44-01 Task 2 found nothing to fix) | 346 |
| shared/examples/software-systems.md | `9c883ea780c2ddde363147d86db91f1ad20212b29eccc07b8dbacc03d7e3fa61` | 301 | `fa800d3f3a277ea037185212389a1be71a8aad848ab0cee513d5590af06b5b44` | 303 |
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

## Post-edit gate baseline (plan 44-07, Task 1 Part B)

Every command below was re-run live at the phase's final content-correction HEAD
(`bcf8a88`, recorded in Chain of custody above), after all six of plans 44-02 through 44-06's
content-correction commits landed and before this plan's own `_FROZEN_PATHS` registration
(Task 2) or `.planning/ROADMAP.md` update (Task 3). Verbatim final line of each, placed beside
the pre-edit baseline above for direct comparison:

```text
$ python3 scripts/sync-content.py --check
(no output; exit 0 — shared/ and the generated tree are in sync)

$ python3 scripts/check-conf-gate.py
check-conf-gate: PASS

$ python3 scripts/report-conformance.py --check
report-conformance: PASS — no drift

$ python3 scripts/check-version-stamps.py
check-version-stamps: PASS

$ python3 scripts/gen-gate-docs.py --check
harvested 19/19 expected script-backed entries (19 total)

$ bash scripts/check-firewall-battery.sh
FIREWALL: GREEN (23/23)
```

`check-conf-gate.py`'s post-edit live run printed the same standing COVERAGE line
(`check-conf-gate: COVERAGE — measured 28 artifacts across shared-examples, generated-twin`) and
the same three `D-08` synthetic-injection self-check lines against `personal-general.md`, unchanged
in shape from the pre-edit run (the D-08 needles were re-pinned in-flight by plan 44-03 against
`personal-general.md`'s corrected text — see that plan's own section above — and pass clean here).
`check-version-stamps.py`'s post-edit run confirms all 17 stamps still read `9.3.2` (D-04) and
`git tag -l v9.4.0` (run separately, Task 3 Part B) prints nothing.

**Comparison, read side by side:** every one of the six commands' verbatim final lines is
byte-identical between the pre-edit baseline above and this post-edit reading — `sync-content.py
--check` silent/exit-0 both times, `check-conf-gate: PASS` both times, `report-conformance: PASS —
no drift` both times, `check-version-stamps: PASS` both times (17/17 stamps at `9.3.2`, D-04
held), `gen-gate-docs.py --check` harvesting 19/19 both times, and `FIREWALL: GREEN (23/23)` both
times — same verdict, same gate count, same 23 individual `[PASS]` lines (confirmed by reading
the full post-edit battery output line by line: DUAL-04, GATE-02-v8.5, STEP0-06, STEP0-08, VAL-01,
VAL-02, VAL-03, VERSION-01, REG-GUARD, GATE-01, BATT-06, TRACE-03, QUAL-01, PROV-GUARD, HARN-01,
HARN-02, HARN-03, SCAN-GUARD, HC-BOUND, CONF-GATE, CONF-SURFACE, INVARIANT-CHECK, FROZEN-EVIDENCE —
all `[PASS]`). Six waves of content edits across seven files moved zero gate readings from this
artifact's own pre-edit baseline — every movement this phase produced is confined to the
per-file `docs/conformance-baseline.md`/`docs/data/conformance.json` column changes each owning
plan's own section above pre-registered and reconciled (`high_conf_chains` and one investigated
`conclusion_claims` movement), none of which this six-command gate chain surfaces as drift, since
`report-conformance.py --check` and `check-conf-gate.py` both measure structural conformance
against the currently-committed content, not against a frozen prior reading.

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

**Defect 1 — GT-4's missing `?` suffix and the resulting D-07 double violation (999.118 step 3,
the one instance the phase pre-names; origin: line 38; head-line citations at lines 46, 56;
downstream confidence lines at 50, 60, 94).**
- Inputs (file's own): GT-4's own sentence, read live — "The free-to-paid conversion rate for
  this product in this ICP segment is unknown and has not been measured; no historical pilot or
  freemium experiment has been run." — source: verified gap.
- Rule applied (`shared/spine/references/output-template.md:114,335`, quoted in the plan's own
  interfaces block): a GT whose own text states unknown/unmeasured must carry `**GT-N?**`; a
  chain whose head cites a `GT-N?` must end MEDIUM or LOW, never HIGH.
- Operation: added the `?` inside the bold span (`**GT-4?**`); changed both C1's and C2's head-line
  citations from `GT-4 (...)` to `GT-4? (...)`; changed both chains' `**Confidence:** HIGH` to
  `**Confidence:** MEDIUM`, each with a stated reason naming GT-4? and the verification path (the
  time-boxed pilot C2 itself recommends). Both bare HIGH labels (pre-edit) carried no reason at
  all — the replacement MEDIUM labels do, so the correction does not reproduce the same defect
  (an unreasoned label) at a different band.
- Result: GT-4 → GT-4? (line 38); C1 confidence HIGH → MEDIUM with reason (line 50); C2
  confidence HIGH → MEDIUM with reason (line 60).
- C1's head-line citation is checked and confirmed unaffected by the D-07 sweep on the head-line
  citation of the chain itself: C1 cites no other chain on its head, only GT-3 and GT-4?, so rule
  3 (transitive ceiling) does not separately reach it beyond rule 2's own direct effect.
- **C3 checked and confirmed unaffected, not omitted.** C3's head cites GT-2 and GT-3 only —
  neither carries a `?` — and C3 cites no other chain on its head, so neither rule 2 nor rule 3
  reaches it; C3's `**Confidence:** HIGH` (line 70) is left unchanged.
- **Section 6's file-level confidence (line 94) — the transitivity judgment call 44-PATTERNS.md
  flagged, decided here.** Section 6's Recommended approach explicitly cites "(chains C2 and
  C3)"; C2 is now capped at MEDIUM under rule 2, and the shipped remediation convention requires
  a synthesizing section's confidence to inherit the lower of the chains it names, not average
  across them. Decided: section 6's `**Confidence:** HIGH` → `**Confidence:** MEDIUM`, with the
  inherited cap and GT-4? named explicitly in the added reason. The Key insight (chain C1, now
  itself MEDIUM for the same GT-4? reason) and the Trade-offs (chains C2 and C3) sit under the
  same section-level rating.
- Provenance: 999.118's own step-3 instruction (adjudicate D-07/`?`-suffix violations); this
  plan's own interfaces block, which independently re-confirmed the live text at lines 38, 46,
  50, 56, 60, 64, 67, 88, 94 before any edit.

**Defect 2 — the break-even formula's dimensional inconsistency (origin: C3 hop 1, line 67;
restated at §6, line 88; 999.118's own citation `product-business.md:67,88`).**
- Inputs (file's own): "blended monthly cost per free user" (numerator, no named GT supplies its
  magnitude — GT-3 establishes only that this cost is real and must be separately budgeted) and
  GT-1's "~$10,000 per team per year" (the average ANNUAL contract value, denominator).
- Operation: the pre-edit form divided a MONTHLY numerator directly by an ANNUAL denominator
  with no unit reconciliation — `(monthly cost) / (annual value)` understates the true monthly-
  basis threshold by a factor of 12, since a correct annual-basis comparison requires the
  numerator annualised: `(monthly cost × 12) / (annual value)`. Re-derived live:
  `python3 -c "print(12)"` confirms the multiplier is exactly 12 (months per year) — this is a
  units correction, not a re-estimate of either input's magnitude, and neither input's stated
  value changes.
- Result: both hop 1 (line 67) and §6 (line 88) restated as `(blended monthly cost per free
  user × 12) / (average annual contract value per converting account)`, with the 12x
  understatement named explicitly at both sites (`× 12` / `annualised` appears at both).
- **Second, independent mismatch found and corrected at both sites, per the plan's own
  instruction:** the numerator is a cost per free USER; the denominator (GT-1) is a contract
  value per converting ACCOUNT (a paying team, not an individual user). The formula is not
  dimensionally complete until the average number of free users per converting account is also
  named — this is stated as a second required pilot input at both sites, alongside the
  per-free-user cost the hop already names. The hop's and §6's existing conclusion — that the
  threshold is not yet calculable from the named ground truths — is kept intact; it now holds for
  two named reasons (the missing per-free-user cost AND the missing users-per-account ratio)
  instead of one.
- Sites: C3 hop 1 (line 67, origin), §6 Recommended approach (line 88, restatement) — confirmed
  no third site: `/usr/bin/grep -n 'break-even\|blended monthly cost'
  shared/examples/product-business.md` returns exactly these two prose sites plus the §6 heading
  reference to "the break-even threshold *formula*", matching 44-RESEARCH.md's own finding ("no
  further propagation found — C1 and C2 do not restate the formula").
- Provenance: 999.118's own table row (`product-business.md:67,88`); 44-RESEARCH.md item 5;
  44-PATTERNS.md's per-file table.

### software-systems.md            (plan 44-04)

**Arithmetic re-derived first, before any edit, per the plan's own instruction:**
`python3 -c "print(480/45); print(1440/45)"` → `10.666666666666666` and `32.0`. An 8-hour
working day (480 minutes) admits approximately 10.7 sequential 45-minute pipeline runs; a
24-hour day (1440 minutes) admits 32. The measured ceiling (2/day, GT-3's own sourced figure)
sits roughly five times below the pipeline's own sequential throughput bound — the 45-minute
floor constrains cadence but does not, by itself, explain why the observed ceiling sits so far
below what the floor alone would permit.

**Defect — the invalid "mechanically blocked / sufficient explanation" argument, restated at
five sites (999.118's own citation `software-systems.md:68,91`; 44-PATTERNS.md's four confirmed
sites plus the line-163 site it flagged and handed to this plan).**
- Inputs (file's own): GT-3's pre-edit clause "higher frequency is mechanically blocked by the
  45-minute pipeline assuming sequential execution" and C1 hop 2's pre-edit sentence "The
  45-minute pipeline is a sufficient explanation of the 2-deploy/day ceiling without any
  architectural coupling claim" (C1's own stated ground for its HIGH rating).
- Operation: each site replaced the false necessity/sufficiency claim with a statement of what
  the corrected arithmetic actually establishes — the 45-minute pipeline bounds sequential
  deploys at roughly 10/working day, well above the observed 2/day, so the floor constrains
  cadence WITHOUT explaining the observed ceiling; what sets the ceiling below the floor's own
  bound is not established by any named ground truth.
- Sites and results:
  1. GT-3 (lines 67-70, origin): "mechanically blocked" clause replaced with the 480÷45≈10.7
     derivation and the "not established by any named ground truth" statement; the sourced
     "measured deploy frequency..." clause left byte-unchanged.
  2. C1 hop 1 (line 93 post-edit): "the 2-deploy/day ceiling follows directly from that floor
     combined with the full-pipeline-per-deploy requirement" replaced with the corrected
     relation (floor bounds ~10/day, well above observed 2/day, so it constrains without
     explaining); the hop's closing clause, which had separately asserted the pipeline structure
     "is the sufficient cause of the measured 2-deploy/day ceiling," was also corrected to state
     that whether the pipeline structure, the architecture, or an unmeasured factor is what
     actually binds the ceiling has not been established — left uncorrected, this closing clause
     would have restated the same invalid sufficiency claim the plan requires removed, one
     sentence after the corrected opening clause, producing an internally self-contradictory hop.
     The 8-minute parallelised-suite comparison and the independent-deployment point are kept
     intact, per the plan's own instruction.
  3. C1 hop 2 (line 94 post-edit): "The 45-minute pipeline is a sufficient explanation of the
     2-deploy/day ceiling without any architectural coupling claim" — C1's own stated ground for
     HIGH — REPLACED (not deleted) with: the pipeline is a NECESSARY constraint on cadence but
     not a SUFFICIENT explanation of the ceiling, since it bounds deploys at roughly five times
     the observed rate; the unexplained factor (deploy windows, approval gates, release batching
     policy) has not been measured. The hop's conclusion sentence ("Architecture cannot be
     concluded to be the primary deploy bottleneck until... profiled") is kept intact — it is a
     claim about what the evidence establishes, and it survives the correction unchanged.
  4. Assumption Audit row (line 233 post-edit, "Bottleneck | 1"): Step Text changed to name the
     ~10/day pipeline bound and state the 2/day ceiling is not explained by it; "Assumption
     surfaced?" changed from "none — ... definitional" (no longer true) to naming the unexplained
     gap as a surfaced-but-unresolved measurement question; "Added to Table?" set to "not added —
     carried as an open measurement gap in chain C1", so no Assumptions Table row was added (the
     section's own contract forbids one, and adding one would move this file's verdict_cells
     reading).
  5. Section 5, line 163 (the site 44-PATTERNS.md flagged and explicitly left unresolved) —
     **adjudicated as requiring correction, not preservation.** The sentence is written in the
     ANALYST's own voice as the stated reason for rejecting the microservices dead end ("GT-1 +
     GT-2 together provide a fully sufficient explanation of the current bottleneck that does not
     require any architectural claim"), not a restatement of the rejected reasoning being
     described — so the preserved-rejected-value exception (the one that keeps `personal-
     general.md`'s discarded $70,000 figure intact in its own §5) does not apply here. Corrected
     to: "GT-1 and GT-2 establish a pipeline-level constraint the migration premise never
     addresses, so the premise is unsupported on its own terms and no architectural claim is
     needed to reject it" — a claim the corrected arithmetic supports (GT-1/GT-2 establish the
     pipeline-level floor; whether that floor alone explains the ceiling is exactly the open
     question the rest of the file now states, so no sufficiency claim is needed to reject the
     microservices premise on its own terms). Re-read the surrounding paragraph after editing;
     the dead-end's own conclusion ("This dead end establishes that 'microservices enable faster
     deploys' may not be used as a ground truth...") still reads correctly and needs no further
     change.
- **Additional restatement sites found by this plan, not named by 999.118, 44-RESEARCH.md or
  44-PATTERNS.md — a Rule 1 auto-fix, recorded per Pitfall 1's own instruction to grep every
  restatement of a corrected claim.** C1's and C3's head-line citations of GT-3 (lines 92 and 112
  pre-edit) both read "(2 deploys/day ... ceiling imposed by the sequential pipeline)" — a
  compact label asserting the same causal-sufficiency relationship GT-3 itself no longer states.
  Left uncorrected, these two head-line citations would have stood in direct tension with GT-3's
  own corrected text three lines above them and with C1's own corrected hops immediately below.
  Corrected both to "(2 deploys/day ... ceiling, not explained by the 45-minute pipeline alone)".
- **C1's confidence (line 96 post-edit) — the decision the plan required either way.** Re-read
  the corrected chain end to end: the conclusion ("architecture cannot be concluded to be the
  primary bottleneck") is a NEGATIVE claim about what the named ground truths establish, directly
  supported by GT-1 and GT-2 plus the documented absence of profiling data; the chain's head
  cites no `GT-N?`, so the D-07 ceiling rule does not reach it; and the conclusion does not
  depend on the withdrawn sufficient-explanation claim — it depends only on the absence of
  profiling data, which the withdrawal does not touch. **Decision: kept HIGH**, with the bare
  label replaced by a stated reason saying exactly this and saying explicitly that the rating
  does not rest on the withdrawn claim. This is the plan's own default disposition; Task 3's
  conformance pre-registration below reflects "kept HIGH" (`software-systems: 3 -> 3`).
- Provenance: 999.118's own table row (`software-systems.md:68,91`); 44-RESEARCH.md item 4 and
  Pitfall 2; 44-PATTERNS.md's per-file table and its explicitly-unresolved line-163 flag.

### science-engineering.md         (plan 44-05)

**Defect 1 — GT-2's false "consistent with" derivation claim, NARROW fix per D-01 (origin: line
55, pre-edit; the Assumptions Table row at line 36 makes the identical claim and moved with it;
999.118's own citation `science-engineering.md:55`).**
- Inputs (file's own): GT-2's own five enumerated loss/retention figures, read live at
  `shared/examples/science-engineering.md:51-60` before any edit — temperature losses ~8%
  (0.92 retained), wiring losses ~5% (0.95 retained), MPPT ~3% (0.97 retained), inverter ~4%
  (0.96 retained), and LiFePO4 round-trip loss 5-8% (0.92 to 0.95 retained).
- Operation, re-derived live with `python3` before any edit:
  `0.92 * 0.95 * 0.97 * 0.96 = 0.8138688`; `0.8138688 * 0.92 = 0.748759296`;
  `0.8138688 * 0.95 = 0.7731753599999999`. So the enumerated list compounds to a retained
  fraction of approximately **0.749 to 0.773**, not 0.80 — 0.80 is modestly optimistic relative
  to this list by roughly 3 to 5 percentage points.
- **D-01's NARROW fix applied, not the broad recompute-and-cascade variant — see the declined
  variant below.** GT-2's false sentence ("Combined, these losses are consistent with a 0.80
  conservative derating factor.") was replaced with a sentence stating the compounded
  0.749-0.773 range explicitly enough to be reproduced from the five percentages GT-2 already
  states, and stating that 0.80 is retained on its own independent basis (the GT's own
  "source: NREL and NABCEP off-grid design guidelines" clause), not as a figure derived from the
  enumerated list. Not one number GT-2 itself uses (0.80, the five loss percentages) moved.
- The Assumptions Table row (line 36, the "linked row" 44-PATTERNS.md names) makes the identical
  claim in its Verification cell ("... is reflected in the conservative 0.80 factor alongside
  wiring ... inverter ... losses"). Under D-01 the row's NUMBER (0.80) does not move; its
  Verification cell was rewritten to state the same corrected relationship as GT-2 (0.80 is the
  independently-sourced design-practice value; the enumerated losses compound to approximately
  0.75-0.77, slightly below it; see GT-2) so the two sites no longer contradict each other. The
  row's Assumption, Type, Treatment and Verdict cells were left byte-unchanged; no row was added
  or removed (verdict_cells stays 8, confirmed post-edit).
- **C1 hop 1's "complete loss model" sentence — adjudicated, not skipped.** C1 (line 107
  post-edit) states "The 0.80 factor is the complete loss model — it accounts for every loss
  between panel output and delivered load, including battery round-trip loss, so no further
  derating is needed for battery inefficiency." Read against the corrected GT-2: this sentence
  asserts SCOPE completeness — which losses 0.80 is meant to bundle (battery round-trip loss is
  included in scope, so it must not be subtracted a second time) — not numerical agreement
  between 0.80 and the enumerated list's compounded value. GT-2's own text (unchanged by this
  correction) already states the same scope claim ("battery round-trip loss is a real,
  non-negligible term in the energy path and is explicitly included here"). Because the sentence
  never restates the withdrawn "consistent with" numerical claim, it is left UNCHANGED — the
  plan's own default disposition, confirmed rather than assumed.
- **Declined broad recompute-and-cascade variant, named explicitly per D-01's own requirement
  that the option considered-and-declined be recorded, not merely absent.** The broad variant
  would have recomputed the design constant to approximately 0.75-0.78 and cascaded: C1's
  `1,875 Wh/day` gross generation target would move to approximately **1,923 Wh/day**
  (1.5 kWh ÷ 0.78), the `341 W` minimum panel capacity would move to approximately **350 W**
  (1,923 Wh ÷ 5.5 PSH), the stated `17% margin` above that minimum would recompute to a smaller
  margin, and the winter-minimum recompute (`~417 W`) would also move — all while leaving the
  shipped `400 W array` recommendation itself untouched, so the file's own stated margin language
  would become internally inconsistent with the shipped number unless the recommendation itself
  were also revisited. D-01 locked the narrow fix instead: 0.80 is independently defensible
  design-practice guidance (NREL/NABCEP), not a figure the file claims to derive from the
  enumerated list once the false "consistent with" sentence is removed, so recomputing it is
  unnecessary and would touch a shipped equipment recommendation this phase does not license.
- D-01 guard, confirmed live post-edit: `0.80`, `1,875`, `341 W`, `17% margin`, `417 W` and
  `400 W` are all still present verbatim in `shared/examples/science-engineering.md`; `consistent
  with a 0.80` returns zero hits.

**Defect 2 — the 1.8 kWh/day upsizing threshold, wrong at four sites governed by two different
constraints (999.118's own table cites only lines 108, 124, 162; this plan's own interfaces
block additionally confirms the first occurrence at line 94, GT-5?'s own verification-path
sentence — a site 999.118's table never named).**
- Inputs (file's own): the shipped 6 kWh LiFePO4 bank (C2's recommendation), GT-3's 80% DoD, GT-4's
  3-day autonomy target (battery-limited path); the shipped 400 W array (C1's recommendation),
  GT-1's 5.5 PSH, GT-2's 0.80 derating factor (panel-limited path).
- Operation, re-derived live with `python3` before any edit: `6 * 0.80 / 3 = 1.6000000000000003`
  (battery-limited, kWh/day) and `400 * 5.5 * 0.80 = 1760.0` Wh/day = **1.76 kWh/day**
  (panel-limited). The battery binds first (1.60 < 1.76): above 1.60 kWh/day the shipped 6 kWh
  bank already fails to meet the 3-day autonomy target, before the 400 W array fails to meet the
  daily load at 1.76 kWh/day. The file previously used a single wrong number, 1.8 kWh/day, at all
  four sites, conflating these two different constraints.
- Sites and results (each matched to the constraint its own sentence names, not applied
  uniformly):
  1. **Line 94 (post-Task-1-edit line number; pre-Task-1 line ~93-94), GT-5?'s own
     verification-path sentence** — governs "the sizing outputs below" as a whole, so it takes
     the BINDING threshold: "exceeds 1.8 kWh/day" -> "exceeds 1.6 kWh/day", with the
     `6 kWh × 0.80 DoD ÷ 3 days = 1.6 kWh/day` derivation stated inline and the binding
     (battery-before-panel) relationship named explicitly. **This is the site 999.118's own
     table never listed** — found by this plan's own interfaces-block blast-radius read, per
     44-RESEARCH.md's item 2.
  2. **C1's confidence** — governs "the required panel capacity exceeds 400 W", so it takes the
     PANEL-limited threshold: "exceeds 1.8 kWh/day" -> "exceeds 1.76 kWh/day", with the
     `400 W × 5.5 PSH × 0.80 = 1,760 Wh/day = 1.76 kWh/day` derivation stated inline. The
     bolded-value `**Confidence: MEDIUM**` sub-variant form was preserved exactly.
  3. **C2's confidence** — governs "upsize the battery bank", so it takes the BATTERY-limited
     threshold: "exceeds 1.8 kWh/day" -> "exceeds 1.6 kWh/day", with the
     `6 kWh × 0.80 ÷ 3 days = 1.6 kWh/day` derivation stated inline. Line 122's (unchanged)
     independent illustrative "e.g., 2.0 kWh/day" what-if and its own derived 7.5 kWh figure were
     left entirely alone — confirmed by `2.0 kWh/day`'s count matching `git show HEAD:` exactly.
  4. **Section 6's recommendation** — names BOTH upsizes (600 W array AND 7.5-8 kWh bank), so it
     states BOTH thresholds rather than picking one: rewritten as a single semicolon-joined
     sentence (not split into two sentences, per the plan's own instruction not to move
     `conclusion_claims`) naming 1.6 kWh/day for the battery upsize and 1.76 kWh/day for the
     panel upsize, each with its derivation stated inline.
- Sweep confirmed: `1.8 kWh/day` returns 0 hits; `1.6 kWh/day` returns 3 hits (sites 1, 3, 4);
  `1.76 kWh/day` returns 2 hits (sites 2, 4); `2.0 kWh/day`'s count is unchanged from `git show
  HEAD:`; `1,760` (the Wh/day form of the panel-limited derivation) appears on the page.
- Provenance: 999.118's own table row (`science-engineering.md:108,124,162`); 44-RESEARCH.md
  item 2 (blast-radius findings); this plan's own interfaces block, which independently
  re-confirmed all four sites live before any edit, including the unlisted line-94 site.

**Adjudication recorded per the plan's own instruction that it be stated either way — Task 3's
D-07 sweep below.**

### science-engineering-2.md       (plan 44-06)

**Defect — GT-2's stated 0.35-0.45 mm Hertz subsurface-shear-maximum depth is not reproducible
from its own stated inputs (origin: lines 69-75, pre-edit; 999.118's own citation
`science-engineering-2.md:70,113`). D-02 locks the fix shape: SUPPLY THE MISSING GEOMETRY — the
band itself, C1's diagnostic argument, section 5's dead-end walk and section 6's key insight all
stay intact. This is not a number-swap defect; the input list itself is incomplete (`"...roller
diameter 22 mm, race radii, and steel E = 207 GPa..."` — "race radii" is a bare, unfilled
placeholder). Task 1 re-derives the geometry that completes the input list; Task 2 records the
disclosure-shape decision; Task 3 applies both.**

**Relations used** (all four standard; the file already cites the fourth itself):
```
Reduced modulus (both bodies steel, plane strain):  E* = E / (2(1 - ν²))
Effective radius, inner race (convex on convex):     1/R = 1/R_roller + 1/R_race
Effective radius, outer race (roller in concave raceway): 1/R = 1/R_roller - 1/R_race
Contact half-width, line contact:                    a = √(4 P' R / (π E*)), P' = load per unit length
Depth of maximum subsurface shear (the file's own cited relation): z = 0.78 a
```

**(a) Reduced-modulus check**, re-derived live with `python3` before any edit:
`E* = 207e9 / (2 * (1 - 0.3**2)) = 113,736,263,736.26 Pa = 113.7363 GPa`, rounding to
**113.7 GPa**. Matches both 999.118's and 44-RESEARCH.md's independently stated value — the
derivation proceeds on this basis.

**(b) Sweep**, `R_roller = 11 mm` (from the file's own stated 22 mm roller diameter), rated load
`P = 12 kN` (the file's own stated value), `R_race` swept 30-120 mm, effective contact length `L`
swept 3-22 mm, for both race cases. Representative rows (full sweep script output retained in the
session scratchpad, not committed — a scratch script never committed is not repository tooling,
per this plan's own threat-model disposition T-44-06-SC):

| Race case | R_race (mm) | R (mm) | L (mm) | a (mm) | z (mm) |
|---|---|---|---|---|---|
| inner | 30 | 8.05 | 4 | 0.5199 | 0.4055 |
| inner | 30 | 8.05 | 5 | 0.4650 | 0.3627 |
| inner | 50 | 9.02 | 4 | 0.5503 | 0.4292 |
| inner | 50 | 9.02 | 6 | 0.4493 | 0.3505 |
| inner | 70 | 9.51 | 4 | 0.5650 | 0.4407 |
| inner | 70 | 9.51 | 5 | 0.5054 | 0.3942 |
| inner | 90 | 9.80 | 4 | 0.5738 | 0.4475 |
| inner | 90 | 9.80 | 6 | 0.4685 | 0.3654 |
| inner | 110 | 10.00 | 5 | 0.5183 | 0.4043 |
| inner | 110 | 10.00 | 6 | 0.4732 | 0.3691 |
| outer | 30 | 17.37 | 8 | 0.5400 | 0.4212 |
| outer | 30 | 17.37 | 10 | 0.4830 | 0.3768 |
| outer | 50 | 14.10 | 6 | 0.5619 | 0.4383 |
| outer | 50 | 14.10 | 9 | 0.4588 | 0.3579 |
| outer | 70 | 13.05 | 6 | 0.5406 | 0.4216 |
| outer | 70 | 13.05 | 8 | 0.4681 | 0.3651 |
| outer | 90 | 12.53 | 6 | 0.5297 | 0.4132 |
| outer | 90 | 12.53 | 8 | 0.4587 | 0.3578 |
| outer | 120 | 12.11 | 5 | 0.5704 | 0.4449 |
| outer | 120 | 12.11 | 8 | 0.4509 | 0.3517 |

**(c) Minimum and maximum effective contact length landing inside 0.35-0.45 mm**, read off the
full swept grid (`R_race` from 30 to 120 mm in 10 mm steps, `L` from 3 to 22 mm in 1 mm steps):
- **Inner race:** `L` ranges from **4 mm to 6 mm** across the whole `R_race` span (30-120 mm) —
  no combination outside this range lands inside the band.
- **Outer race:** `L` ranges from **5 mm to 10 mm** across the whole `R_race` span.
- **18 mm typical full-length contact** (the counter-anchor — roughly the full 22 mm roller
  width minus a small edge margin), re-derived live: inner race at `R_race = 60 mm` gives
  `z = 0.2054 mm`, at `R_race = 70 mm` gives `z = 0.2078 mm`; outer race at `R_race = 60 mm`
  gives `z = 0.2473 mm`, at `R_race = 70 mm` gives `z = 0.2434 mm`. **This lands at
  0.205-0.247 mm — matching 999.118's own 0.20 mm figure and the interfaces block's stated
  0.21-0.25 mm range, and is the reason this defect was filed at all: the nominal full-width
  contact does not reproduce the stated band.**

**(d) Sourcing judgement.** The geometry that reproduces the stated 0.35-0.45 mm band requires an
effective roller contact length of roughly **4-10 mm — about a fifth to a half of the nominal
22 mm roller diameter**, depending on race case and race radius. An effective contact length this
much shorter than the nominal roller width implies heavy crowning, edge relief, or a
misalignment-narrowed contact patch — all real bearing-design features, but **no named source in
this exemplar's scenario ties a specific crowning profile, edge-relief geometry, or misalignment
figure to this bearing.** The scenario (`shared/examples/science-engineering-2.md:10-20`) is
illustrative — a wind-turbine HSS gearbox bearing with no manufacturer, part number, or drawing
cited anywhere in the file. **This research/plan cannot name a source for the required geometry.
This is the expected outcome** (44-RESEARCH.md's Assumptions Log entry A1 flags exactly this
risk). No manufacturer, part number, or drawing reference is invented to fill the gap — doing so
would be a worse defect than the one being fixed (T-44-06-01).

**(e) Supersession of 44-RESEARCH.md's `[ASSUMED]` ~5.6 mm figure.** 44-RESEARCH.md's Blast-radius
section (item 3) and its Assumptions Log (A1) carried forward an unverified, race-case-unspecified
~5.6 mm contact-length figure (from "0.40 mm needs ~2.1 MN/m, a ~5.6 mm contact length" — a single
approximate anchor with no stated race case or race radius). **This derivation supersedes that
figure**, replacing it with race-case-specific values: the interfaces block's own worked anchors
(inner race, `R_race ≈ 70 mm` → `L ≈ 4.9 mm`; outer race, `R_race ≈ 60 mm` → `L ≈ 6.9 mm`) are
both independently reproduced here (re-derived live: inner anchor `L = 4.856 mm`, matching the
interfaces block's stated 4.9 mm; outer anchor recomputed the same way in the interfaces block
itself, `L = 6.9 mm`). **The derivation agrees with 44-RESEARCH.md's ~5.6 mm figure in order of
magnitude**: ~5.6 mm sits between the inner-race anchor (4.86 mm) and the outer-race anchor
(6.90 mm), consistent with 44-RESEARCH.md's figure being a single rough estimate rather than a
race-case-specific value. This derivation replaces that single approximate figure with a
race-case-specific pair, closing 44-RESEARCH.md's own `[ASSUMED]` flag with a shown re-derivation
rather than a copied-forward number.

**(f) Recommended geometry set for Task 3** — the parameter set that reproduces the **middle** of
the stated 0.35-0.45 mm band (`z = 0.40 mm`, matching GT-1's own observed 0.4 mm crack-origin
depth exactly, which is what C1's diagnostic argument cites):
- **Race case:** inner race (convex-on-convex, roller against the inner raceway)
- **Race radius:** `R_race = 70 mm`, giving effective radius `R = 9.506 mm`
  (`1/R = 1/11 mm + 1/70 mm`)
- **Effective roller contact length:** `L = 4.9 mm` (re-derived exactly: `L = 4.856 mm`, stated
  to one decimal place for the exemplar's prose)
- **Resulting depth:** re-derived live with `python3`: `P' = P/L = 12{,}000 / 0.004856 =
  2.4712 MN/m`; `a = √(4 × 2.4712e6 × 0.009506 / (π × 113.736e9)) = 0.5128 mm`;
  `z = 0.78 × 0.5128 = 0.4000 mm` — **exactly the middle of the stated 0.35-0.45 mm band**, and
  exactly matching GT-1's own 0.4 mm observation, which is the coincidence C1's diagnostic
  argument is built on.

**Task 2 decision — GT-2's disclosure shape and C1's rating.** Presented to the developer at a
`checkpoint:decision` (gate: blocking). `workflow.auto_advance` reads `true` in
`.planning/config.json`, so this checkpoint was auto-advanced rather than answered by a person.

- **Chosen option: `option-flagged`** — supply the geometry AND flag it: GT-2 becomes `GT-2?`,
  C1's confidence becomes MEDIUM.
- **Date:** 2026-09-18.
- **Reasoning (one sentence):** Task 1's sourcing judgement (d) found that no source can be named
  for the required geometry — the expected outcome — which makes `option-sourced` unavailable
  (it would require inventing a citation, prohibited by T-44-06-01), and the plan's own text names
  `option-flagged` as the mandatory default when this checkpoint is auto-advanced rather than
  answered by a person.
- **Taken by auto-advance, not by a person** — recorded explicitly per the plan's own instruction,
  so a reviewer can see which it was. No source is named for `option-sourced` because none exists
  to name.

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

### product-business.md

Rule, quoted as above. Applied to every `**GT-N**` bullet and every chain in this file's own
`## 3. Ground Truths` and `## 4. Derivation Chains` sections, read live after Task 1 of this
plan landed.

**GT-level table:**

| File | GT | Clause deciding ?-required | ?-required | ?-present | Verdict |
|---|---|---|---|---|---|
| product-business.md | GT-1 | "source: internal financial report (company's own ARR dashboard)" | no | no | OK |
| product-business.md | GT-2 | "source: known channel mix (sales team records)" | no | no | OK |
| product-business.md | GT-3 | "source: accounting principle; confirmed by finance team" | no | no | OK |
| product-business.md | GT-4? | "is unknown and has not been measured; no historical pilot or freemium experiment has been run" — source: verified gap | yes | yes (added by this plan's Task 1) | OK |

**Chain-level table:**

| File | Chain | Head-line citations | Confidence | Cites a `GT-N?` on head | Rule 2 holds | Rule 3 holds |
|---|---|---|---|---|---|---|
| product-business.md | C1 | GT-3 + GT-4? | MEDIUM (was HIGH pre-edit) | yes (`GT-4?`) | yes (not HIGH) | yes (no chain cited on head) |
| product-business.md | C2 | GT-1 + GT-4? | MEDIUM (was HIGH pre-edit) | yes (`GT-4?`) | yes (not HIGH) | yes (no chain cited on head) |
| product-business.md | C3 | GT-2 + GT-3 | HIGH (unchanged — checked, not omitted) | no | yes (no `GT-N?` cited, so rule 2 imposes no ceiling) | yes (no chain cited on head) |

**Sweep result for product-business.md: one violation found and corrected by this plan's Task 1
(the D-07 violation 999.118 step 3 pre-names).** GT-4 was the file's only Ground Truth whose own
text states unmeasured/unknown language and, pre-edit, did not carry the required `?` — both C1
and C2 cited it directly on their heads while rated HIGH, a double violation of rules 1 and 2.
Corrected: GT-4 → GT-4? (line 38); C1 and C2 → MEDIUM with stated reasons (lines 50, 60). C3 is
confirmed checked and unaffected — its head cites GT-2 and GT-3 only, neither a `GT-N?`, so
neither rule 2 nor rule 3 reaches it; its HIGH rating is left unchanged. Section 6's own
Confidence line (a synthesizing, not a chain-level, rating) was separately adjudicated per the
transitivity judgment call 44-PATTERNS.md flagged: since it explicitly cites "(chains C2 and
C3)" and C2 is now capped at MEDIUM, section 6's own confidence inherits that cap and moved
HIGH → MEDIUM. This matches the CONF-GATE floors interface block's post-edit expectation for
this file: `high_conf_chains` moves from 3 (C1, C2, C3 all HIGH pre-edit) to 1 (C3 only,
post-edit) — pre-registered below before regeneration and confirmed by the observed diff.

### software-systems.md

Rule, quoted as above. Applied to every `**GT-N**` bullet and every chain in this file's own
`## 3. Ground Truths` and `## 4. Derivation Chains` sections, read live after Task 2 of this
plan landed.

**GT-level table:**

| File | GT | Clause deciding ?-required | ?-required | ?-present | Verdict |
|---|---|---|---|---|---|
| software-systems.md | GT-1 | "source: measured pipeline execution time (CI dashboard logs; 30-day average of successful pipeline runs)" | no | no | OK |
| software-systems.md | GT-2 | "source: observed CI pipeline configuration file (deploy stage definition)" | no | no | OK |
| software-systems.md | GT-3 | "source: measured deploy frequency from CI/CD deployment records (30-day trailing count)" — the 2/day figure itself is a direct measurement; correcting the invalid "mechanically blocked" inference clause attached to it does not change this, because the measured figure was never the unverified part (see the re-derivation section above, which states explicitly this does not change the `?` answer) | no | no | OK (unchanged by Task 2's edit — explicitly re-checked, not assumed) |
| software-systems.md | GT-4 | "source: architectural fact documented in microservices engineering literature (Newman, DORA)" | no | no | OK |
| software-systems.md | GT-5 | "source: observed codebase structure (direct inspection of database schema and ORM model relationships)" | no | no | OK |

**Chain-level table:**

| File | Chain | Head-line citations | Confidence | Cites a `GT-N?` on head | Rule 2 holds | Rule 3 holds |
|---|---|---|---|---|---|---|
| software-systems.md | C1 | GT-1 + GT-2 + GT-3 | HIGH (kept, reason added — see the re-derivation section above) | no | yes (no `GT-N?` cited, so rule 2 imposes no ceiling) | yes (no chain cited on head) |
| software-systems.md | C2 | GT-5 + GT-4 | HIGH (unchanged) | no | yes | yes |
| software-systems.md | C3 | GT-1 + GT-3 + GT-4 | HIGH (unchanged) | no | yes | yes |

**Sweep result for software-systems.md: zero `?`-suffix violations found.** No Ground Truth in
this file states unverified/unmeasured/preliminary language in its own text — GT-3's pre-edit
"mechanically blocked" clause was an invalid INFERENCE bolted onto a measured figure, not a
statement that the figure itself is unverified, so correcting that inference does not create a
`?`-suffix requirement (explicitly re-checked per the plan's own instruction, not assumed from
the personal-general-2.md/product-business-2.md precedent of "correcting an inference doesn't
suffix the GT"). No chain in this file cites a `GT-N?` on its head, so rule 2 imposes no ceiling
on any of the three chains; all three legitimately remain HIGH. This matches the CONF-GATE
floors interface block's post-edit expectation: `high_conf_chains` stays at 3 (C1 kept HIGH per
this plan's Task 2 decision, C2 and C3 untouched) — pre-registered below before regeneration and
confirmed by the observed diff.

### science-engineering.md

Rule, quoted as above. Applied to every `**GT-N**` bullet and every chain/section-level
confidence line in this file's own `## 3. Ground Truths`, `## 4. Derivation Chains` and
`## 6. Conclusion` sections, read live after both of this plan's tasks landed.

**GT-level table:**

| File | GT | Clause deciding ?-required | ?-required | ?-present | Verdict |
|---|---|---|---|---|---|
| science-engineering.md | GT-1 | "source: NREL solar radiation maps; illustrative figure verifiable via NREL PVWatts for the specific site coordinates" — states illustrative/verifiable, not unverified/unmeasured | no | no | OK |
| science-engineering.md | GT-2 | Post-correction text: "0.80 is retained here on its independent basis (NREL and NABCEP conservative off-grid design practice, cited below), not as a figure derived from the list above" — cites a named source and states a deterministic compounded range computed from GT-2's own already-stated percentages; no unverified/unmeasured language appears anywhere in GT-2's own text, before or after the correction | no | no | OK — re-examined explicitly, not assumed (see below) |
| science-engineering.md | GT-3 | "source: LiFePO4 manufacturer specifications and electrochemical battery design literature" — a chemistry fact, not unverified | no | no | OK |
| science-engineering.md | GT-4 | "source: current design constraint and occupant decision" — a stated design decision, not an unverified empirical claim | no | no | OK |
| science-engineering.md | GT-5 | "unverified: this figure is derived from the per-appliance load breakdown below, which depends on occupant behavior..." | yes | yes (`GT-5?`, already suffixed pre-edit) | OK |

**GT-2's `?` question, re-examined explicitly per the plan's own instruction, not skipped
because the site happened to be edited by Task 1.** GT-2's corrected text changes WHY 0.80 is
retained (an independently-sourced design-practice convention, not a figure claimed to be
derived from the enumerated list) but does not change WHAT KIND of claim GT-2 makes about
itself: GT-2 never says its own value is unverified, unmeasured, or preliminary — it names a
citable source (NREL/NABCEP) both before and after the correction, and the corrected
0.749-0.773 range is itself a deterministic arithmetic product of percentages GT-2 already
stated, not a new empirical claim requiring its own verification. **Conclusion: the correction
does not change the `?` answer for GT-2 — it remains unsuffixed.** No chain's confidence band
changes as a result, so `high_conf_chains` does not move (pre-registered below).

**Chain/section-level table:**

| File | Chain/section | Head-line citations | Confidence | Cites a `GT-N?` on head | Rule 2 holds | Rule 3 holds |
|---|---|---|---|---|---|---|
| science-engineering.md | C1 | GT-2 + GT-5? + GT-1 | MEDIUM (unchanged) | yes (`GT-5?`) | yes (MEDIUM, not HIGH) | yes (no chain cited on head) |
| science-engineering.md | C2 | GT-5? + GT-4 | MEDIUM (unchanged) | yes (`GT-5?`) | yes (MEDIUM, not HIGH) | yes (no chain cited on head) |
| science-engineering.md | §6 Conclusion | "(chains C1 and C2)" throughout | MEDIUM (unchanged) | n/a (cites chains, not GTs, directly) | n/a | yes (cites C1 and C2, both MEDIUM; §6 is MEDIUM, not higher than either) |

**Sweep result for science-engineering.md: zero `?`-suffix violations found, and no confidence
label moved.** GT-5? already carried its suffix pre-edit and both chains were already MEDIUM
citing it on their heads, so rules 2 and 3 already held before this plan's edits — **recorded as
the expected null result.** GT-2's post-correction text was re-examined explicitly (above) and
found not to trigger a `?` suffix. This matches the CONF-GATE floors interface block's reading
(`high_conf_chains 0`) and the plan's own pre-registration below: no measured conformance value
is expected to move for this file.

### science-engineering-2.md

Rule, quoted as above. Applied to every `**GT-N**` bullet and every chain/section-level
confidence line in this file's own `## 3. Ground Truths`, `## 4. Derivation Chains` and
`## 6. Conclusion` sections, read live after this plan's Task 3 edits landed.

**GT-level table:**

| File | GT | Clause deciding ?-required | ?-required | ?-present | Verdict |
|---|---|---|---|---|---|
| science-engineering-2.md | GT-1 | "source: metallographic report from accredited failure-analysis lab; image set retained" — a direct measurement | no | no | OK |
| science-engineering-2.md | GT-2? | Post-Task-3 text: "Unverified: the effective roller contact length and race radius are inferred from the bearing's rated-load condition rather than read at a named source" | yes | yes (this plan's Task 3, option-flagged) | OK |
| science-engineering-2.md | GT-3 | "source: same metallographic report; SEM imagery confirms the characteristic WEC morphology" | no | no | OK |
| science-engineering-2.md | GT-4 | "source: bearing manufacturer's life calculation per ISO 281; SCADA-derived load spectrum" | no | no | OK |
| science-engineering-2.md | GT-5 | "source: on-removal electrical-test report from the same failure-analysis lab" | no | no | OK |
| science-engineering-2.md | GT-6 | "source: turbine OEM data sheet; matches the IEC TS 60034-25 domain of applicability" | no | no | OK |
| science-engineering-2.md | GT-7? | "unverified: a tribology textbook reference... supports the morphology mapping, but no in-house controlled test has been run" | yes | yes (already suffixed pre-edit) | OK |

**Chain/section-level table:**

| File | Chain/section | Head-line citations | Confidence | Cites a `GT-N?` on head | Rule 2 holds | Rule 3 holds |
|---|---|---|---|---|---|---|
| science-engineering-2.md | C1 | GT-1 + GT-2? | MEDIUM (this plan's Task 3, was HIGH) | yes (`GT-2?`) | yes (MEDIUM, not HIGH) | yes (no chain cited on head) |
| science-engineering-2.md | C2 | GT-3 + GT-4 + GT-5 + GT-6 | HIGH (unchanged) | no (none of C2's four head-line citations carry a `?`) | yes (no `GT-N?` cited, so no ceiling applies) | yes (no chain cited on head) |
| science-engineering-2.md | §6 Conclusion | Confidence sub-field cites GT numbers directly ("GT-1 through GT-6"), not a chain reference — unlike its three sibling sub-fields (Recommended approach, Key insight, Trade-offs), which each carry an explicit "(chain CN)" annotation | HIGH (unchanged) | n/a (cites GTs directly, not a chain head-line) | n/a — not a formally-cited chain under rule 2's mechanical test | n/a — rule 3 binds on explicit chain-citation, which this sub-field does not carry |

**C2 checked separately per the plan's own instruction, and the transitivity question
answered explicitly.** C2's head line cites GT-3, GT-4, GT-5, GT-6 only — none of them carry a
`?`, and C2's head does not cite C1 or any other chain. **The transitivity rule (rule 3) does
NOT reach C2 from C1**: rule 3 caps a chain "no higher than the lowest-rated chain its head
cites," and C2's head cites zero chains (only GTs), so C1's MEDIUM rating has no path to C2. C2
correctly remains HIGH — its root-cause/EIBD argument was never built on GT-2? and does not
inherit C1's cap.

**Out-of-plan finding, recorded rather than silently absorbed: §6's own Confidence sub-field
required a correction this plan's PART C/D did not explicitly name, but Task 3's application of
option-flagged made necessary (Rule 1 — the sentence became factually false, not merely
stylistically stale).** §6's Confidence sub-field (distinct from §6's "Key insight" sub-field,
which D-02 explicitly protects and which this plan confirmed byte-unchanged) pre-edit read "the
primary causal chain rests on GT-1 through GT-6, all of which are verified independently. The
single unverified item (GT-7?) is not load-bearing..." — once GT-2 became GT-2?, this sentence
asserted something now false (that all six GTs, including GT-2?, are "verified independently",
and that GT-7? is "the single" unverified item). Unlike C1 hop 1's adjudication in plan 44-05
(which examined a SCOPE-completeness claim untouched by its correction and left it unchanged),
this sentence directly restates a VERIFICATION-STATUS claim about the exact set of GTs whose
verification status changed — the same test 44-05 applied, applied here, points the other way.
**Fix applied:** the sentence was corrected to name both `?`-bearing items (GT-2? and GT-7?) and
state, using the file's own established GT-7?-is-corroborative-not-load-bearing reasoning
pattern (already present in §6 Trade-offs), that neither is load-bearing for the root-cause
finding or the recommended intervention — GT-1 alone (§5) already establishes the
subsurface-versus-surface origin independent of GT-2?'s exact band. **The `HIGH` label itself
was NOT changed**, because — unlike C1, which is mechanically capped by D-07 rule 2 via its own
formal head-line citation of GT-2? — §6's Confidence sub-field carries no explicit chain-citation
of C1 the way its three sibling sub-fields do (see the chain/section-level table above), so
D-07's mechanical rule 3 does not formally bind it, and the root-cause finding it primarily rests
on (C2, HIGH, unaffected by GT-2?) remains fully supported. Verified this does not move
`conclusion_claims`: the sentence was already long and sentence-punctuated pre-edit (already
counted as 1 of the file's 3 conclusion claims) and remains so post-edit — no claim was added or
removed.

**Sweep result for science-engineering-2.md: one violation found and fixed (C1, GT-2? cap under
rule 2), one out-of-plan factual-consistency fix applied (§6's Confidence sub-field, Rule 1), and
C2 confirmed independently HIGH with no transitivity path from C1.** `high_conf_chains` moves
**2 → 1** for this file and its twin (pre-registered below).

### Pre-registered conformance expectation (plan 44-05, Task 3 Part B/C)

Written BEFORE running `sync-content.py --write` or `report-conformance.py`, per the plan's own
instruction that the expected movement be pre-registered ahead of regeneration. Read live
against `docs/conformance-baseline.md`'s current rows immediately before this pre-registration
(not from memory): `shared/examples/science-engineering.md` and its generated twin both read
`conclusion_claims=3, verdict_cells=8, chain_blocks=2, high_conf_chains=0,
marked_untraced_claims=0`.

**Pre-registration:** no `**Confidence:**` label was moved anywhere in this file by Tasks 1 or
2 (C1, C2 and §6 all stay MEDIUM — see the D-07 sweep immediately above), no Assumptions Table
row or `### Conclusion` block was added or removed, and this file carries no claim-marker, so
NO measured conformance value is expected to move for `shared/examples/science-engineering.md`
or its generated twin. The regenerated twin should differ from the source by nothing but the
`GENERATED_MARKER` header line, and `report-conformance.py --check` should report no drift.

**Observed outcome, live:** matched the pre-registration exactly. `python3
scripts/sync-content.py --write` (wrote 48 files) followed by `--check` (exit 0); `diff <(tail -n
+3 first-principles/agents/references/examples/science-engineering.md)
shared/examples/science-engineering.md` printed nothing (twin byte-identical below the generated
header). `python3 scripts/report-conformance.py` (regenerate, `PASS — wrote ... (42 rows)`),
then `git diff --stat -- docs/conformance-baseline.md docs/data/conformance.json` printed
nothing — zero bytes moved in either conformance artifact, confirmed by `python3
scripts/report-conformance.py --check` (`PASS — no drift`). `python3 scripts/check-conf-gate.py`
passed clean on the first live run (`check-conf-gate: PASS`, 28 artifacts, the three D-08
self-check lines against `personal-general.md` unrelated to this plan's files) — confirmed by
direct reading that no literal substring of `science-engineering.md`'s prose is transcribed
anywhere in `scripts/check-conf-gate.py`, so no needle re-pin was needed (unlike plan 44-03's
`_D08_*` case). `python3 scripts/gen-gate-docs.py --check` (harvested 19/19, exit 0). `python3
scripts/check-version-stamps.py` (17 stamps, all `9.3.2`, PASS). `git diff --quiet HEAD --
tests/adversarial-corpus-v9.0 shared/examples/self-application.md` exited 0 (both
byte-unchanged). `bash scripts/check-firewall-battery.sh` printed `FIREWALL: GREEN (23/23)`,
reproducing the pre-edit baseline exactly (23/23, same gate set). No movement occurred outside
the pre-registered set — every column for `shared/examples/science-engineering.md` and its twin
(`conclusion_claims=3, verdict_cells=8, chain_blocks=2, high_conf_chains=0,
marked_untraced_claims=0`) held at its pre-registered value.

### Pre-registered conformance expectation (plan 44-04, Task 3 Part B)

Written BEFORE running `sync-content.py --write` or `report-conformance.py`, per the plan's own
instruction that the expected movement be pre-registered ahead of regeneration. Read live against
`docs/conformance-baseline.md`'s current rows immediately before this pre-registration (not from
memory): `shared/examples/product-business.md` and its generated twin both read
`conclusion_claims=3, verdict_cells=7, chain_blocks=3, high_conf_chains=3, marked_untraced_claims=0`;
`shared/examples/software-systems.md` and its generated twin both read `conclusion_claims=8,
verdict_cells=6, chain_blocks=3, high_conf_chains=3, marked_untraced_claims=0`.

**Pre-registration:**
- `shared/examples/product-business.md` and its generated twin: `high_conf_chains` **3 → 1** (C1
  and C2 lowered to MEDIUM under the D-07 rule; C3 keeps HIGH; both rows move identically since
  DUAL-04 requires the twin to be byte-identical to the source below the generated header).
- `shared/examples/software-systems.md` and its generated twin: `high_conf_chains` **3 → 3, no
  movement** (this plan's Task 2 decision keeps C1 at HIGH with a replaced, correctly-grounded
  reason; C2 and C3 were never touched).
- No other column is expected to move for either file or its twin — not `conclusion_claims`
  (no hop, chain, or GT was added or removed by either task), not `verdict_cells` (no
  Assumptions Table row was added to either file — software-systems.md's Task 2 explicitly
  avoided this), not `chain_blocks` (no `### Conclusion` block was added or removed), not
  `marked_untraced_claims` (neither file carries a claim-marker; the project-wide ratchet stays
  at exactly 4, unmoved by this plan). Any movement outside this pre-registered set is a
  stop-and-investigate per the plan's own instruction; the actual regeneration diff is compared
  against this pre-registration below, not the other way around.

**Observed outcome, live:** `python3 scripts/sync-content.py --write` (wrote 48 files) followed
by `--check` (exit 0). `python3 scripts/report-conformance.py` (regenerate, `PASS — wrote ...
(42 rows)`), then `git diff --stat -- docs/conformance-baseline.md docs/data/conformance.json`
showed exactly two rows changed on each side (source + twin) for `product-business.md`:
`high_conf_chains` **3 → 1**, matching the pre-registration exactly. `software-systems.md`'s row
did not appear in the diff at all — `high_conf_chains` stayed at **3**, also matching the
pre-registration exactly.

**One movement outside the pre-registered set, found, investigated, and recorded rather than
silently absorbed, per T-44-04-01's own mitigation.** `product-business.md`'s and its twin's
`conclusion_claims` column moved **3 → 4** (and the corpus-wide "§6 conclusion claims (untraced)"
headline moved 77 → 78), which this plan's own pre-registration explicitly said should NOT move
("no hop, chain, or GT was added or removed by either task"). Investigated against
`scripts/check-quality-harness.py`'s `_conclusion_claims` extractor (`_is_assertive_claim`,
`_BOLD_LEADIN_COLON_RE`): a bold colon-lead-in inside `## 6. Conclusion` counts as a claim only
if the text after the lead-in is over 40 characters or ends in sentence punctuation — the
pre-edit `**Confidence:** HIGH` line (20 characters, no terminal punctuation) did NOT qualify and
was never counted; Task 1's required replacement — a full reason naming the inherited GT-4? cap,
per the plan's own acceptance criterion that a bare `**Confidence:** MEDIUM` is NOT acceptable —
is long and sentence-punctuated, so it now DOES qualify and is counted as a fourth conclusion
claim. `untraced_claims` stayed at 0 both before and after: the new claim is traced by its own
inline "(chains C2 and C3)" citation. This is a mechanical, unavoidable side effect of the plan's
own explicit Task 1 requirement (a stated, non-bare reason on section 6's Confidence line), not a
defect introduced by this plan and not a movement this plan could have both satisfied Task 1's
acceptance criteria and also avoided. `_CLAIM_FLOORS["product-business"]` in
`scripts/check-conf-gate.py` is a floor (`>= 3`), not an exact-equality pin, so `check-conf-gate.py`
required no re-pin and passed clean on the first live run — confirmed by re-reading the script
(unlike plan 44-03's `_D08_*` needles, no literal substring transcription of this file's prose
exists anywhere in `check-conf-gate.py`). `python3 scripts/check-conf-gate.py` (`check-conf-gate:
PASS`, COVERAGE 28 artifacts, the three D-08 self-check lines unrelated to this plan's files).
`python3 scripts/report-conformance.py --check` (`PASS — no drift`). `python3
scripts/gen-gate-docs.py --check` (harvested 19/19, exit 0). `python3
scripts/check-version-stamps.py` (17 stamps, all `9.3.2`, PASS). `git diff --quiet HEAD --
tests/adversarial-corpus-v9.0 shared/examples/self-application.md` exited 0 (both byte-unchanged).
Both twin diffs (`diff <(tail -n +3 <twin>) <source>`) printed nothing for both files.
`bash scripts/check-firewall-battery.sh` printed `FIREWALL: GREEN (23/23)`, reproducing the
pre-edit baseline exactly (23/23, same gate set). No other column moved for either file or twin —
`verdict_cells`, `chain_blocks`, and `marked_untraced_claims` (project-wide sum still 4) all held
at their pre-registered values.

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

### Pre-registered conformance expectation (plan 44-06, Task 3 Part E)

Written BEFORE running `sync-content.py --write` or `report-conformance.py`, per the plan's own
instruction that the expected movement be pre-registered ahead of regeneration. Read live against
`docs/conformance-baseline.md`'s current rows immediately before this pre-registration (not from
memory): `shared/examples/science-engineering-2.md` and its generated twin both read
`heading_chain_blocks=2, conclusion_claims=3, verdict_cells=8, chain_blocks=2, high_conf_chains=2,
marked_untraced_claims=0` — matching the interfaces block's own stated reading exactly.

**Pre-registration, under option-flagged (the checkpoint's auto-advanced choice):**
- `shared/examples/science-engineering-2.md` and its generated twin: `high_conf_chains` **2 → 1**
  (C1 lowered to MEDIUM under the D-07 rule, since its head line now cites `GT-2?`; C2 keeps HIGH,
  confirmed independently in the D-07 sweep above — no transitivity path from C1 reaches it).
- No other column is expected to move: not `conclusion_claims` (no hop, chain, or GT bullet was
  added or removed — GT-2 became GT-2? in place, and §6's Confidence sub-field's out-of-plan fix
  changed prose length/wording only, confirmed above to remain a single already-long,
  sentence-punctuated bold-colon claim both before and after), not `verdict_cells` (no Assumptions
  Table row was added or removed), not `heading_chain_blocks`/`chain_blocks` (no `### Conclusion
  CN` block was added, removed, or malformed), not `marked_untraced_claims` (this file carries no
  claim-marker; the project-wide ratchet stays at exactly 4, unmoved). Any movement outside this
  pre-registered set is a stop-and-investigate per the plan's own instruction.

**Observed outcome, live:** matched the pre-registration exactly. `python3
scripts/sync-content.py --write` (wrote 48 files) followed by `--check` (exit 0); `diff <(tail -n
+3 first-principles/agents/references/examples/science-engineering-2.md)
shared/examples/science-engineering-2.md` printed nothing (twin byte-identical below the generated
header). `python3 scripts/report-conformance.py` (regenerate, `PASS — wrote ... (42 rows)`), then
`git diff --stat -- docs/conformance-baseline.md docs/data/conformance.json` showed exactly two
lines changed (one `shared/examples/science-engineering-2.md` row, one generated-twin row), each
moving only `high_conf_chains` **2 → 1**, matching the pre-registration exactly — confirmed by
direct reading of the diff, no other column on either row moved. `python3
scripts/report-conformance.py --check` (`PASS — no drift`). `python3 scripts/check-conf-gate.py`
passed clean on the first live run (`check-conf-gate: PASS`, COVERAGE 28 artifacts, the three D-08
self-check lines against `personal-general.md` unrelated to this plan's file) — confirmed by
direct reading that no literal substring of `science-engineering-2.md`'s prose is transcribed
anywhere in `scripts/check-conf-gate.py`, so no needle re-pin was needed. `python3
scripts/gen-gate-docs.py --check` (harvested 19/19, exit 0). `python3
scripts/check-version-stamps.py` (17 stamps, all `9.3.2`, PASS). `git diff --quiet HEAD --
tests/adversarial-corpus-v9.0 shared/examples/self-application.md` exited 0 (both byte-unchanged).
The twin diff (`diff <(tail -n +3 <twin>) <source>`) printed nothing. No movement occurred outside
the pre-registered set.

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

**All eleven rows of backlog 999.118's defect table are corrected**, each independently
re-derived from the owning exemplar's own stated inputs in this session (not copied forward from
999.118's, 44-RESEARCH.md's or 44-PATTERNS.md's own first-pass figures), and each verified stale
zero times over in a post-edit `/usr/bin/grep -F` sweep for its own superseded literal(s):
`personal-general-2.md`'s GT-6, C1 hop 1, C1 hop 2 and C2 (plan 44-02); `personal-general.md`'s C1
basis-mixing defect (plan 44-03); `product-business-2.md`'s GT-1 distinct-account inference (plan
44-03); `product-business.md`'s GT-4 `?`-suffix violation and break-even formula (plan 44-04);
`software-systems.md`'s GT-3/C1 "mechanically blocked" argument (plan 44-04);
`science-engineering.md`'s GT-2 derating claim and 1.8 kWh/day threshold (plan 44-05); and
`science-engineering-2.md`'s GT-2 missing Hertz geometry (plan 44-06, D-02's locked
supply-the-geometry shape).

**The blast radius extended well beyond 999.118's own eleven line citations, and every additional
site found was corrected, not merely noted.** Beyond the four sites 999.118's research phase
pre-named — `personal-general-2.md`'s §6 Trade-offs restatement (line 122) and its C1 confidence
sensitivity claim (line 64), `software-systems.md`'s Assumption Audit row (line 231), and
`science-engineering.md`'s line-94 first occurrence of the 1.8/1.6 kWh/day threshold — the
owning plans' own post-edit restatement sweeps found and fixed a further set no upstream artifact
had named at all: `personal-general-2.md`'s line-81 C3 terminal-value parenthetical;
`personal-general.md`'s lines 18, 56 and 67 (found by plan 44-03's own required `effective`
sweep); `software-systems.md`'s two GT-3 head-line-citation glosses on C1 and C3, plus C1 hop 1's
own closing clause (found by plan 44-04 re-reading the corrected chain end to end); and
`science-engineering-2.md`'s §6 file-level Confidence sub-field, which became factually false the
moment GT-2 carried the `?` suffix (found and fixed by plan 44-06). `software-systems.md`'s
line-163 site, which 44-PATTERNS.md flagged and explicitly left unresolved for the owning plan to
adjudicate, was adjudicated by plan 44-04 as requiring correction (written in the analyst's own
voice, not a preserved restatement of rejected reasoning) and corrected accordingly. Two of the
seven files' defects were argument-structure problems, not value substitutions —
`software-systems.md`'s GT-3/C1 claim was the chain's own stated ground for a HIGH confidence
rating, and `science-engineering-2.md`'s GT-2 range was the coincidence C1's whole diagnostic
argument depended on matching GT-1's independent 0.4 mm observation — and both were re-examined
for whether their chain's stated confidence still followed once the false claim was corrected,
not merely patched at the number level.

**The seven previously-untested exemplars were hand-re-derived (999.118 step 4); six are CONFIRMED
clean, one carries a disclosed non-arithmetic staleness issue filed out of scope.**
`estimate-fermi.md`, `theoretical-limit-carnot.md`, `decompose-irreducibility.md`,
`ishikawa-fishbone.md` and `software-systems-2.md` all re-derive cleanly with zero arithmetic
disagreements (plan 44-01); `composed-inversion-second-order.md` carries no re-derivable numeric
content (one grep hit, confirmed a false-positive step-number cross-reference, not a quantity).
`self-application.md` is arithmetically self-consistent in full (every figure re-derives exactly
from its own stated inputs) but its Ground Truths describe a repository state that has since
changed — see the D-03 exclusion below.

**The `?`-suffix / D-07 confidence-ceiling sweep (999.118 step 3) was run across all fourteen
`shared/examples/*.md` files, not just the one instance 999.118 pre-named.** One violation was
found and corrected: `product-business.md`'s GT-4, which stated unmeasured/unknown language
without carrying the required `?` while both chains citing it directly on their heads were rated
HIGH — corrected to GT-4?, both chains downgraded to MEDIUM with stated reasons, and section 6's
own synthesizing confidence line downgraded in step (plan 44-04). A second violation surfaced as
a direct consequence of plan 44-06's own D-02 fix, not as a pre-existing defect: once GT-2 in
`science-engineering-2.md` was correctly suffixed to GT-2? (because its geometry is inferred, not
read at a named source), C1's HIGH rating — resting directly on GT-2? in its head-line citation —
required the same downgrade to MEDIUM, applied by that plan. Every other Ground Truth and chain
across all fourteen files, including the seven previously-untested exemplars and the six
remaining defective files, was swept and found already compliant: every unverified GT already
carried its `?`, and no chain citing a `GT-N?` (directly or transitively) was rated above MEDIUM.
Zero violations required a fix in `personal-general-2.md`, `personal-general.md`,
`product-business-2.md`, `software-systems.md`, `science-engineering.md`, or any of the seven
untested exemplars.

**What this artifact does NOT establish.** Every figure recorded here was re-derived BY HAND —
`python3 -c` arithmetic checked by a human/executor against each exemplar's own stated inputs, not
by any automated arithmetic checker, because no such checker exists anywhere in this repository
and building one is explicitly out of bounds (`.planning/STATE.md` standing instruction 2;
44-RESEARCH.md's "Don't Hand-Roll" section). The guarantee this artifact offers is therefore only
as strong as the recorded derivations a skeptical reader can independently re-run — which is
exactly why every defect and restatement site above states its inputs, its operation, and its
result inline, rather than asserting a bare corrected value. The gate chain this phase re-ran
before and after every edit — `sync-content.py --check`, `check-conf-gate.py`,
`report-conformance.py --check`, `check-version-stamps.py`, `gen-gate-docs.py --check`, and the
full offline battery — proves only that nothing ELSE broke: that source and generated twin stayed
in sync, that structural conformance counts moved only where pre-registered and reconciled, that
version stamps and the frozen corpus stayed untouched, and that no other gate in the battery
regressed. None of these gates reads arithmetic, checks a dollar figure, or validates a physics
formula — `docs/conformance-baseline.md`'s own per-exemplar columns count structural elements
(chain blocks, table rows, claim markers), never a Ground Truth's stated number, confirmed live in
44-RESEARCH.md's "Gate Impact" section before this phase made any edit. **Do not read this
artifact, or the phase it records, as a gate-verified guarantee that these exemplars' arithmetic
is clean — it is a recorded, reproducible hand-verification, with every step shown for a skeptic
to check, not a certification an automated instrument could reproduce on its own.**

**`self-application.md` is excluded from this phase's corrections (D-03) and is byte-unchanged.**
Confirmed throughout the phase and again at this artifact's completion:
`git diff --quiet HEAD -- shared/examples/self-application.md` exits 0, and its pre-edit and
post-edit sha256 in the chain-of-custody table above are identical
(`47adb0226654cb6246b0004d83c399a81431ebcba98f9509fd61228beda0ce11`). Its arithmetic is fully
self-consistent (every figure re-derives exactly from its own stated inputs — see the
Untested-exemplar re-derivation section above); what is stale is that its Ground Truths describe a
repository state that has since changed (an 878-line agent body with the Output Template and
Validation Rubric appendices still inlined, governed by a binding META-Q4 line-count gate — none
of which is true of the current 807-line, de-inlined, META-Q4-retired tree). This is a
citation-currency issue, a different defect class from 999.118's "arithmetic, unit or citation
defect re-derivable as wrong from the file's own stated inputs" scope, and is filed as backlog
999.124 (plan 44-01, Task 3) rather than fixed in this phase, per the locked decision D-03.

**Eight items in the frozen `tests/adversarial-corpus-v9.0/` corpus are `derived:` copies of the
seven exemplars this phase touched, and by design still carry the defects this phase corrected in
their source (D-05).** The corpus is FROZEN-EVIDENCE-registered and was not edited — confirmed by
`git diff --quiet HEAD -- tests/adversarial-corpus-v9.0` exiting 0 throughout the phase (see the
Adversarial-corpus inheritance section above for the full eight-item table: T-01, T-02, T-07,
T-08, T-09, T-11, T-12, T-14). Each of these items now carries an arithmetic/citation defect its
own catalog entry does not name, layered underneath the deliberately-injected falsehood the
catalog does name and that each item was constructed to demonstrate. This second, uncatalogued
layer of wrongness is recorded — never fixed inside the frozen corpus itself — via a
cross-reference this phase added under backlog 999.4's own entry in `.planning/ROADMAP.md`, so
anything built on this corpus as a clean-negative validation set (starting with backlog 999.4's
own semantic claim-to-chain judge) is warned to read this section first.

## Erratum (2026-09-18)

The Finding section above is frozen and left byte-unchanged. The numbered corrections below
supersede the specific sentences they cite; no re-derivation, sha256, line count or sweep reading
recorded above is affected. Raised by the Phase 44 code review and appended additively per this
file's own Frozen-evidence discipline section, never as a rewrite of the original text.

1. **"`science-engineering-2.md`'s §6 file-level Confidence sub-field, which became factually
   false the moment GT-2 carried the `?` suffix (found and fixed by plan 44-06)" (Finding section,
   Blast-radius paragraph).** Narrowed: plan 44-06 corrected the sub-field's *text*; it did
   **not** re-band the rating. Verified at this phase's final content-correction HEAD
   (`git show bcf8a88:shared/examples/science-engineering-2.md`), §6 line 224 still read
   `**Confidence: HIGH**`, while the same section's `**Recommended approach:**` (line 196) names
   chain C1 — which that same plan had re-banded to MEDIUM at line 122. A reader of the original
   sentence would reasonably conclude the §6 banding was resolved; it was not. Filed as
   code-review finding CR-01 and corrected after this artifact was frozen. The correct reading of
   the original sentence is "the sub-field's *text* was corrected; its rating was not re-banded."

2. **"no chain citing a `GT-N?` (directly or transitively) was rated above MEDIUM" and "Zero
   violations required a fix in `personal-general-2.md`, ..." (Finding section, `?`-suffix /
   D-07 sweep paragraph).** Narrowed: the sweep's subject was **chain-level ratings only**, and
   at chain level its result stands. `shared/spine/references/validation-rubric.md` Criterion 5
   also binds the §6 **Conclusion section** rating to the weakest chain that section names — the
   rule plan 44-04 applied correctly in `product-business.md`, and the rule this sweep did not
   apply. Under it, two files were non-compliant at `bcf8a88`:

   - `science-engineering-2.md` — §6 rated HIGH while naming chain C1 (MEDIUM). Item 1 above;
     code-review finding CR-01.
   - `personal-general-2.md` — §6 rated MEDIUM while naming chains C1 (LOW) and C2 (LOW), both
     verified LOW at `bcf8a88` lines 64 and 74. Code-review finding WR-06.

   The sweep's scope was therefore narrower than the claim made for it. The claim is restated as:
   swept at chain level, and clean at chain level; the Criterion 5 section-level rule was not
   swept, and two files failed it.

Neither correction changes any figure, any re-derivation, any custody-table hash or any gate
reading recorded above. Both narrow a **closure claim** — what the phase established — rather
than a measurement.

## Erratum 2 (2026-09-18)

The Finding, Untested-exemplar re-derivation, chain-of-custody table and Frozen-evidence
discipline sections above are frozen and left byte-unchanged. The numbered items below supersede
the specific sentences they cite; no re-derivation, sha256, line count or sweep reading recorded
above is affected. Raised by the Phase 44 verification (`44-VERIFICATION.md` gaps VG-01, VG-02,
VG-03; residual findings RF-01, RF-02) and appended additively per this file's own Frozen-evidence
discipline section, never as a rewrite of the original text.

1. **"The blast radius extended well beyond 999.118's own eleven line citations, and every
   additional site found was corrected, not merely noted." (Finding section, Blast-radius
   paragraph).** Narrowed for `software-systems.md`. At `695250b` the claim that the 45-minute
   pipeline binds the 2/day deploy ceiling survived, re-worded, at further sites an exact-substring
   sweep could not reach: C1 hop 1 (:93), C3 hop 2 (:114), the §5 runner dead end (:187, :196-197,
   :201-202, :214-216, :220-222), the Assumption Audit intro (:230), §6 steps 1-3 (:250-253, :255,
   :269), the Key insight (:283-286) and the Trade-offs bullet (:290), plus the Scenario line (:9).
   This is a further live instance of backlog **999.125**'s defect class — a re-worded restatement
   an exact-substring sweep cannot see. Closed by plan 44-08 (commit `3bde82f`), which ran a
   concept sweep instead of a sentence sweep — `/usr/bin/grep -noiE 'bottleneck|deploy-frequency|
   deploy frequency|limiting|achievable|sufficient|almost certainly|correct (lever|intervention)|
   single-digit|core problem|order-of-magnitude|ceiling'` against both the pre-edit and post-edit
   file — adjudicating every hit S (corrected) or P (preserved, with a written reason).

   | Site | Location | Before (concept) | After |
   |---|---|---|---|
   | S1 | :9 | "limiting the team ... to roughly 2 deploys per day" | "and the team ... ships roughly 2 deploys per day" |
   | S2 | :93 C1 hop 1 | "no architectural change is needed to remove the deploy-frequency bottleneck" | "per-deploy pipeline time is set by pipeline structure, and no architectural change is needed to shorten it" |
   | S3 | :113 C3 hop 1 | scope = four pipeline stages only | scope widened to the completion-to-next-deploy gap, cited to GT-3 |
   | S4 | :114 C3 hop 2 | "(almost certainly parallelization first)" | conditional on what profiling identifies as binding |
   | S5 | :187 | "seemed to directly address the measured bottleneck" | "seemed to directly address the measured 45-minute runtime (GT-1)" |
   | S6 | :196-197 | "still well above the threshold needed to increase deploy frequency meaningfully" | states no such threshold is established |
   | S7 | :201-202 | "The correct lever is not the test runner" | "The larger lever on pipeline time is not the test runner" |
   | S8 | :214-216 | "reduces the bottleneck ... core problem" | "trims pipeline time ... the pipeline's structure" |
   | S9 | :220-222 | "The correct intervention is parallelization ... order-of-magnitude" (unconditional) | conditional on profiling showing pipeline time binds |
   | S10 | :230 | "the pipeline-bottleneck diagnosis chain" | "the bottleneck-diagnosis chain" |
   | S11 | :250-253 | "Identify the dominant bottleneck" (pipeline stages only) | reads the completion-to-next-deploy gap too |
   | S12 | :255 | "Parallelize the test suite and decouple the restart" (unconditional) | conditional on profiling identifying a pipeline stage as binding |
   | S13 | :269 | "after removing the pipeline bottleneck" | "after removing whatever constraint profiling identified as binding" |
   | S14 | :283-286 | "the same deploy-frequency improvement ... is achievable through pipeline configuration changes" | "What the analysis does show is the order of the work" |
   | S15 | :290 | "address the deploy-frequency bottleneck" (unconditional) | conditional on profiling identifying a pipeline stage as binding |
   | S16 | :240 | Audit row scoped to pipeline stages only | + completion-to-next-deploy gap; + GT-3's source |

   All eleven P-sites (P1-P11) were preserved with their voice adjudication recorded — notably P2,
   the fenced abandoned-reasoning chain "Current deploys take 45 minutes, limiting releases to
   ~2/day.", preserved verbatim as rejected reasoning inside the fenced block the analyst's own
   voice refutes three paragraphs later. Re-running the same concept sweep post-edit mapped every
   hit to a named S- or P-site; none fell outside the table. No confidence label and no structural
   count moved.

2. **Step 4's "All six editable files' arithmetic is CONFIRMED with zero disagreements; no edit was
   required in any of them." and the `estimate-fermi.md` table's "every figure re-derives cleanly."
   (Untested-exemplar re-derivation section, `estimate-fermi.md — CONFIRMED`).** Narrowed: the
   table omitted the O&M addition step. The file cited O&M reserve `≈ $5-10/kWh of capacity` but
   used `$3` and `$8` in its lower/upper bounds and printed a `$25-35/kWh` central band its own
   inputs give as `$25.6-30.6/kWh`. Closed by plan 44-09 (commit `e0fb140`), which kept the cited
   `$5-10/kWh` range byte-unchanged and re-derived every downstream figure from it rather than
   rewriting the citation to fit the stale bounds — a citation rewrite trades an arithmetic defect
   for an unverifiable citation change, which is strictly worse. Re-derived with `python3` before
   writing: `8.6*0.40*3.5+5 = 17.0` (lower bound), `8.6*0.60*4+7.5 = 28.0` (central, at the O&M
   midpoint `$7.5`, published `~$28/kWh`), `8.6*0.80*5+10 = 44.0` (upper bound); levelised cost
   `17/12000 = 0.0014`, `28/10000 = 0.0028`, `44/8000 = 0.0055` (`~$0.0014-0.0055/kWh`); the
   decision-check ratio `150/44 = 3.4x`. `$17-$44/kWh` now appears exactly 3 times (the
   decision-resolution check, §6 Recommended approach, §6 bullet). The NREL `$20-50/kWh` sentence
   and the `~$40/kWh` straddle sentence stayed byte-unchanged (re-checked: 40 still lies inside
   17-44).

3. **The `science-engineering-2.md` re-derivation's added "0.21-0.25 mm — matching ... the
   interfaces block's stated 0.21-0.25 mm range" (a figure this fixture's own
   `science-engineering-2.md` re-derivation entry above did not separately re-check).** Narrowed:
   the `0.247/0.243 mm` (rounded to `0.25 mm`) end is an outer-race computation whose geometry the
   exemplar never states; only the `0.208 mm` (rounded to `0.21 mm`) inner-race end re-derives from
   the file's own stated 70 mm inner-race radius. Closed by plan 44-09 (commit `e0fb140`), which
   narrowed the counter-figure to "about 0.21 mm (0.208 mm)" and named the 70 mm inner-race radius
   it derives from. The load-bearing conclusion — the nominal-contact band excludes GT-1's observed
   0.4 mm — is unchanged at every value the band ever carried; GT-2? keeps its `?`, and C1, C2 and
   §6 keep their confidence labels.

4. **Chain-of-custody table, post-edit columns for `shared/examples/software-systems.md`,
   `shared/examples/estimate-fermi.md` and `shared/examples/science-engineering-2.md` (Chain of
   custody section above).** Superseded, not overwritten — post-`44-09` values:

   | file | post-edit sha256 | post-edit lines |
   |---|---|---|
   | shared/examples/software-systems.md | `a6cf941bf62dd11c1cea54c7aa28b4b3187d56c60cee6563213089fffc9dc54f` | 316 |
   | shared/examples/estimate-fermi.md | `0e0bad3eb377f33df84e02382e1eaf32d7a1fe9f1e277cdfb53e66b27b7e1d6b` | 269 |
   | shared/examples/science-engineering-2.md | `072ce9b3e7477a64975d190cbf209c4e7ae62d376eeaeca317b9cfce55ca9822` | 254 |

   The original table's `estimate-fermi.md` entry, "(unchanged — plan 44-01 Task 2 found nothing to
   fix)", is superseded by item 2 above — the file's post-`44-07` sha256/line count that entry
   recorded is no longer current; its arithmetic, not merely its bytes, has since changed.

5. **Adversarial-corpus inheritance (recorded, never fixed).** T-14 (`derived:software-systems`)
   also carries every 44-08 S-site's pre-fix text — recorded, never fixed (D-05); the
   cross-reference already added under backlog 999.4 already warns readers of this section not to
   treat corpus items as a clean negative class. No corpus item derives from `estimate-fermi.md`.
   T-02 (`derived:science-engineering-2`) also derives from a file this erratum's item 3 narrows,
   but its own catalogued defect (`tests/adversarial-corpus-v9.0/catalog.md:49`) is GT-4's
   fabricated `read-at-source` provenance, not the GT-2? counter-figure item 3 narrows — unaffected.

6. **"Once registered by plan 44-06" and "Until plan 44-06's registration lands" (Frozen-evidence
   discipline section).** Corrected: `tests/exemplar-rederivation-v9.4` was registered in
   `_FROZEN_PATHS` by plan **44-07** (Task 2), commit `6ac123c` (`chore(44-07)`), confirmed against
   `44-07-PLAN.md` must_have 3. The registration itself — that it happened, and what it does — is
   correct; only the plan number naming it was wrong.

7. **Disposition, not a correction.** `personal-general-2.md`'s "approximately $12,030" (inputs
   give $12,028) was reviewed under RF-03 / review finding IN-01 and deliberately left unedited,
   because the file applies the same labelled 4-significant-figure rounding convention to its C2
   gap ($36,232 → "$36,230"). Editing only the smaller figure would make the file inconsistent with
   its own stated convention.

Items 1-3 both narrow a closure claim — what the phase established — and record a content
correction made after this artifact was frozen; items 4-6 correct bookkeeping; item 7 records a
disposition, not a defect. No pre-edit baseline, gate reading or re-derivation recorded above this
erratum is altered, and every figure items 2 and 3 supersede — `estimate-fermi.md`'s O&M-derived
bracket and `science-engineering-2.md`'s nominal-contact counter-figure — is named above with its
corrected value.

## Phase-wide close-out sweep (plan 44-07, Task 3)

Run at the phase's final content-correction HEAD (`bcf8a88`) plus this plan's own two prior
commits (`ddc2663` artifact completion, `6ac123c` `_FROZEN_PATHS` registration), immediately
before the `.planning/ROADMAP.md` plan-list update (Task 3 Part D, gitignored, not committed).

### Part A — stale-literal sweep, every 44-PATTERNS.md §4 pattern, all seven corrected files

| File | Pattern | Hits | Expected |
|---|---|---|---|
| personal-general-2.md | `113,000` | 0 | 0 |
| personal-general-2.md | `120,000` | 0 | 0 |
| personal-general-2.md | `$3,000–$10,000` | 0 | 0 |
| personal-general-2.md | `roughly 5–9%` | 0 | 0 |
| personal-general-2.md | `$32,000` | 0 | 0 |
| personal-general-2.md | `76,000–$78,000` | 0 | 0 |
| personal-general-2.md | `90,000–$110,000` | 0 | 0 |
| personal-general-2.md | `7–8 years` | 0 | 0 |
| personal-general-2.md | `30,000–$35,000` | 0 | 0 |
| personal-general.md | `overstates the real gain by roughly 23%` | 0 | 0 |
| personal-general.md | `$54,000` (presence, corrected label) | 6 | >0 |
| science-engineering.md | `consistent with a 0.80` | 0 | 0 |
| science-engineering.md | `1.8 kWh/day` | 0 | 0 |
| science-engineering.md | `1.6 kWh/day` (presence, corrected) | 4 | >0 |
| science-engineering.md | `1.76 kWh/day` (presence, corrected) | 3 | >0 |
| science-engineering-2.md | `race radii` (bare placeholder) | 0 | 0 |
| software-systems.md | `mechanically blocked by the 45-minute pipeline` | 0 | 0 |
| software-systems.md | `sufficient explanation of the 2-deploy/day ceiling` | 0 | 0 |
| software-systems.md | `ceiling follows from sequential pipeline` | 0 | 0 |
| software-systems.md | `fully sufficient explanation of the current bottleneck` | 0 | 0 |
| software-systems.md | `follows directly` | 1 | 0, investigated |
| product-business.md | `(blended monthly cost per free user) / (average contract value)` | 0 | 0 |
| product-business.md | `blended monthly cost per free user divided by average contract value` | 0 | 0 |
| product-business.md | `**GT-4**` (unsuffixed) | 0 | 0 |
| product-business.md | `**GT-4?**` (presence, corrected) | 1 | 1 |
| product-business-2.md | `41 requesting accounts` | 0 | 0 |

**`software-systems.md`'s `follows directly` hit, investigated:** the one hit is at line 238, the
Assumption Audit table's "Min viable" row — "this sequencing follows directly from the cost-risk
ordering established in Step 1" — an unrelated use of the same three-word phrase describing a
different claim (test-execution sequencing, not the withdrawn deploy-ceiling causal-sufficiency
argument). Confirmed by direct reading, matching the same false-positive pattern 44-RESEARCH.md's
own live sweep found twice elsewhere in the repository for this exact phrase. Not a stale
restatement; no fix needed.

**Preserved-value assertions, confirmed PRESENT at their expected counts:**
- `personal-general.md`: `$70,000` present **10** times, `$70K` present **3** times — the
  intentionally-preserved dead-end nominal-figure references (999.118's own preserved-value
  exception; confirmed matching `git show f7efc17:shared/examples/personal-general.md` counts).
- `science-engineering.md`, D-01-protected: `0.80` present **15**, `1,875` present **2**,
  `341 W` present **2**, `17% margin` present **1**, `417 W` present **1**, `400 W` present
  **7** — all six literals byte-unchanged from `git show f7efc17:`, confirming D-01's narrow fix
  held and no cascade shipped.
- `science-engineering-2.md`, D-02-protected: `0.35-0.45 mm` present **2** times, unchanged from
  pre-edit — the band itself was never touched; only the previously-bare "race radii" input list
  was completed with concrete numbers.
- `science-engineering.md`, unrelated illustrative figure: `2.0 kWh/day` present **1** time,
  matching its pre-edit count exactly — confirmed this file's C2 what-if example was not
  conflated with the corrected 1.6/1.76 kWh/day thresholds.

**Twin regeneration check, all seven files:** `diff <(tail -n +3 <twin>) <source>` prints nothing
for all seven — `personal-general-2.md`, `personal-general.md`, `science-engineering.md`,
`science-engineering-2.md`, `software-systems.md`, `product-business.md`,
`product-business-2.md`. Every twin is byte-identical to its source below the generated-marker
header.

**Sweep result: every pattern returns zero hits except the four preserved-value classes (all
confirmed present at their expected, unmoved counts) and one investigated false positive
(`follows directly`, confirmed unrelated by direct reading, not a defect).**

### Part B — locked-decision audit D-01 through D-06

Checked against the phase-start SHA recorded in Chain of custody above
(`f7efc17febdfadc62e682d06f40d98017032828d`), not `HEAD~n`.

| Decision | Command | Result |
|---|---|---|
| D-01 | (Part A above) all six protected literals present, unmoved | HOLDS |
| D-02 | `/usr/bin/grep -cF '0.35-0.45 mm' shared/examples/science-engineering-2.md` → 2; re-run plan 44-06's recomputation live: `E*=113.736 GPa`, `R=9.506 mm`, `a=0.5105 mm`, `z=0.78×a=0.3982 mm` | HOLDS — `z` recomputes to 0.398 mm from GT-2's own post-edit inputs, inside the unchanged 0.35-0.45 mm band |
| D-03 | `git diff --quiet f7efc17 -- shared/examples/self-application.md` → exit 0; `/usr/bin/grep -n '999.124' .planning/ROADMAP.md` → two hits (backlog entry heading at line ~7508, cross-reference at line ~587) | HOLDS |
| D-04 | `python3 scripts/check-version-stamps.py` → `check-version-stamps: PASS` (17/17 at `9.3.2`); `git tag -l v9.4.0` → empty | HOLDS |
| D-05 | `git diff --quiet f7efc17 -- tests/adversarial-corpus-v9.0` → exit 0; eight-item inheritance table present above | HOLDS |
| D-06 | `git diff --name-only f7efc17 HEAD -- scripts/` → `scripts/check-conf-gate.py`, `scripts/check-firewall-battery.sh` (both **Modified**, confirmed via `--name-status`: zero files with status `A`) | HOLDS in substance — see discrepancy note below |

**D-06 citation discrepancy, recorded rather than silently reconciled.** This plan's own
acceptance criteria (44-07-PLAN.md Task 3) state the scripts/ diff "lists at most
`scripts/check-firewall-battery.sh`." The live diff also lists `scripts/check-conf-gate.py`,
modified by plan 44-03 to re-transcribe its D-08 anti-vacuity needles after Task 1's edit to
`personal-general.md` removed the literal substrings those needles pinned — a Rule 3
blocking-issue auto-fix, recorded in full in plan 44-03's own summary and in this artifact's
`personal-general.md (plan 44-03)` section above, and explicitly the scenario
`check-conf-gate.py`'s own source comment names as expected apparatus-code behavior for a future
content edit. This plan's acceptance-criteria text did not anticipate that earlier plan's
apparatus fix when it was written. **D-06's actual substance — no NEW checker script was written
anywhere under `scripts/`** — holds without qualification: `git diff --name-status f7efc17 HEAD
-- scripts/` shows both files as `M` (Modified), zero as `A` (Added). The "at most one file"
literal wording is stale against the phase's own recorded history, not a violation of D-06's own
rule.

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
