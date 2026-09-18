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
| shared/examples/personal-general-2.md | `993e00534d49333514865d7222df537b3e8edd6eb0143af5cdd29a900b76767d` | 124 | (pending — plan 44-02) | (pending — plan 44-02) |
| shared/examples/personal-general.md | `5e43d95329b2ca52fb6699601b382f11b5ea26cc7a992b83c891732d3301dea7` | 101 | (pending — plan 44-03) | (pending — plan 44-03) |
| shared/examples/product-business-2.md | `052691ec3a851f1d3b8dcb4aa2ff7cd0cad1b58cf22f127ae12c76ee32630935` | 211 | (pending — plan 44-03) | (pending — plan 44-03) |
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

*(pending - plan 44-02)*

### personal-general.md            (plan 44-03)

*(pending - plan 44-03)*

### product-business-2.md          (plan 44-03)

*(pending - plan 44-03)*

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
