# Worked examples re-run on the current agent — the example-rerun-2 reading

**A recorded reading with its N. Not a gate.**
**Protocol:** [`docs/example-rerun-2-protocol.md`](example-rerun-2-protocol.md), registered before
any run. **Predecessor:** [`example-rerun-reading.md`](example-rerun-reading.md) (v9.13.0).
**Captures:** `tests/example-rerun-2/` — each run's stream, the agent's own transcript, the
delivered files, `cells.json` and `comparison.json`. **Re-derive the mechanical table:**
`python3 tests/example-rerun-2/run_examples.py compare`

---

## The answer in one paragraph

**Yes — the shipped examples need updating.** Of the 13 examples a clean re-run could be judged
against (`self-application` was contaminated again), **every one carries at least one verified
must-fix, should-fix or should-add item, and 7 carry a must-fix** — an error or a contradiction in
the example's own text. None of the updates reverses an example's recommendation outright; most
correct a claim the example's own text contradicts, an overclaimed band, or a material
consideration both independent re-runs raised and the example omits. Four of the
predecessor's catches are **still unfixed** (the vesting cliff, free-tier cannibalisation, the
backwards cold-oil premise, worst-month sizing), and the one that was fixed (`estimate-fermi`,
`ceb16c52`) was fixed incompletely. Separately, and not about the examples: **3 of 14 registered
runs skipped the agent's procedure** and delivered no file, against 0 of 14 on v9.13.0 — a rate
a paired follow-up did not reproduce ([`skip-paired-reading.md`](skip-paired-reading.md): 0 of 9
against 1 of 9 on the same prompts).

## What was run

14 examples, one registered run each, on the agent at `2628e725` exported outside the
repository, `claude-sonnet-5`, CLI 2.1.289, sequential, empty working directory.

| Outcome | Examples |
|---|---|
| Six-section file delivered | 11 |
| Procedure skipped — no file (see *The agent* below) | 3: `decompose-irreducibility`, `personal-general-2`, `product-business` |
| Contaminated — read the repository | 1: `self-application` (of the 11) |

**Supplementary runs** (not registered by the protocol; added after the skips were observed,
same body and transport, recorded as `<name>.supp`): each of the three skipped examples was run
once more, and all three delivered a six-section file (7,805 / 9,338 / 9,545 words). Those three
examples are judged on their supplementary run. The registered first run stays the reading of
the agent's behaviour.

## Do the examples need updating — per example

Each item below was raised by the judge (one per example, given the shipped example, this
re-run and the v9.13.0 re-run) **and re-checked against the shipped example's text by the main
session** before being written here. Line numbers are `shared/examples/<name>.md` at
`2628e725`. *Must-fix* = an error or a contradiction in the example's own text; *should-add* = a
material consideration, raised independently by both re-runs, that qualifies the
recommendation.

| Example | Severity | Verified update |
|---|---|---|
| `composed-inversion-second-order` | must-fix | L112 still marks the upgrade-driver assumption "unverified" though GT-2 (L130–134) records that exact check as done; Step 5 (L88–89) still says all five are untested |
| | must-fix | GT-3's two-week estimate covers TTL invalidation (L136–137); the recommendation (L258–262) requires event-driven invalidation, "not TTL-only" — the estimate does not cover what is recommended |
| | must-fix | the only example still on the old `Type \| Source` assumptions header (L104); two summary-block rows carry `"type": null` |
| | should-add | the procurement lead time (L37) is never used; the fallback "execute the upgrade as planned" assumes a late reversal the scenario says is expensive |
| `estimate-fermi` | must-fix | `ceb16c52` reversed the verdict but left the old framing in six places: L125/L130 call the store "comparable to GT-6?"; L183–184 "settled at Step 6a"; L217–218 "harder to reach"; L223 and L361 "the conclusion is sensitive to it" (contradicts L325 "holds at any η"); L306–309 "turns on" the levelised figure |
| | should-add | the store bracket is large-plant data applied to 5 MWh with no scale caveat (the power block gets one); the long-duration claim is capital-only |
| `ishikawa-fishbone` | must-fix | C1 is HIGH (L176–180) on a step — the 11 accounts sit in the uncovered tier — that no ground truth supports and the example's own A-4 (L129) leaves unverified |
| | must-fix | L238 "explain the majority of the churn signal" directly after L237's 11 of 23 = 48% |
| `personal-general` | should-add | GT-1's $70K includes an equity grant (L39) treated as cash; vesting, cliff and forfeiture appear nowhere (0 hits). **Predecessor catch, unfixed** |
| | should-add | the example admits the terms could be negotiated (L31–32) but the recommendation never says to ask |
| `personal-general-2` | must-fix | the L103 dead end compares ~6.5% *real* with 6.25% *nominal* ("comfortably above"); L31 mixes the bases too; the stated ~1-point tax overstatement is ~1.6 ($122,040 on $60K over 10 y = 7.36%/y) |
| | should-add | the chains use the annual-compounding $110,012 though L52 gives the loan's monthly $111,913; the central gap is ~$10.1K not ~$12.0K and the one-point sensitivity becomes ~a tie |
| | should-fix | the split is described three ways (L92/L125/L133); a 50/50 split is exactly half of each payoff |
| `product-business` | should-add | cannibalisation or downgrade of the $2.4M paid base is never raised (0 hits); the pilot (L98) needs an existing-customer exclusion. **Predecessor catch, unfixed** |
| `product-business-2` | should-fix | C2 (L135–138) rules out the rival partly because "GT-1 records no churn signal" — a churn survey cannot see prospects lost before signing; L129 "does not foreclose it" and L184–185 lean on the same gap |
| | should-add | the rewrite's sizing gap (row 3, L42) caps confidence but is not a go/no-go step in §6 |
| `science-engineering-2` | must-fix | the cold-oil dead end (L176–183) walks "viscosity rises" → "film below roughness" without noting the premise is backwards; L204's fix belongs to the cold-starvation story. **Predecessor catch, unfixed** |
| | must-fix | L56 cites ISO 6336 (gears) and DIN 5401 (bearing balls) for a roller bearing |
| | should-fix | L103–104 "a non-classical mechanism is required": ~0.1–0.2% of classical bearings fail by 0.11 × L10 (ISO 281 reliability factor), so it is strongly disfavoured, not required |
| `science-engineering` | must-fix | L100–102 calls the battery the binding constraint; at the example's own winter 4.5 PSH (L120) the 400 W array gives 1.44 kWh/day, below the 1.5 load |
| | should-add | size on the worst month (the example admits it is "slightly undersized for worst-case winter"); LiFePO4 charging below 0 °C is never addressed. **Predecessor catch, unfixed** |
| | should-fix | L37 types 80% DoD as `physical law`; it is a manufacturer convention |
| `software-systems-2` | should-fix | C3 (L175) says lock-in is "lowest" on credentials/MFA; GT-5 (L101–104) says MFA seeds round-trip only partially |
| | should-fix | L174 calls tenant model and authorisation "lowest-blast-radius" in a HIGH chain with no input supporting it; a cross-tenant leak is high blast radius |
| `software-systems` | must-fix | C2/C3 are HIGH on unsourced judgement hops (C3's "~1 day"), which the output template's HIGH rule does not license; §6 follows them |
| | must-fix | L115 (and L305–306): schema decomposition "enables independent deploys" without splitting the deploy unit — a monolith deploys as one unit |
| | should-fix | L297–298 "no architectural risk" for blue-green on a shared schema; L49's DORA "~50 engineers / ~10 services" thresholds are unsourced; L50's hotfix bypass is in no ground truth |
| `decompose-irreducibility` | should-add | the refutation is stated as a physical law "at these temperatures" (L127, L202, L353) but holds only for resistive charging (L42); heat-pump charging's ideal round trip is 100%, and "heat pump" appears nowhere |
| | optional | L357 rounds estimate-fermi's ~3.7–18 h break-even to "4–18 h", hiding the one case ($279 < $300) where molten salt is cheaper at four hours |
| `theoretical-limit-carnot` | should-fix | L165–166 and L334 credit ~7 points to reheat; L152 says the same 7 points is mostly turbine scale and configuration |
| `self-application` | — | not judged: contaminated (below) |

**Checked and rejected** (by a judge or by the main session): every arithmetic chain the judges
re-derived in the shipped examples checks out except the two in `personal-general-2` above;
`estimate-fermi` and `theoretical-limit-carnot` are consistent where they share figures; one judge's
claim that `decompose-irreducibility` never states the salt's specific heat is wrong (L80 does);
the 2 untraced conclusion claims the detector finds in `decompose-irreducibility` are disclosed
as "no chain — flagged assumption only" and are not counted as defects. Differences explained by
the example carrying scenario facts a prompt cannot supply, by length, or by more `?`-marking were
excluded by the protocol.

## Mechanical comparison

| Example | Words | GT ids | `?` GTs | Chains | Defects u/m/n | Confidence |
|---|---|---|---|---|---|---|
| composed-inversion-second-order | 3,403 → 8,243 | 5 → 11 | 1 → 4 | 1 → 3 | 0/0/0 → 0/0/0 | MEDIUM → LOW |
| decompose-irreducibility (supp) | 3,279 → 7,805 | 8 → 14 | 2 → 12 | 1 → 4 | 2/0/0 → 0/0/0 | MEDIUM → LOW |
| estimate-fermi | 4,799 → 11,876 | 5 → 24 | 4 → 19 | 1 → 11 | 0/0/0 → 0/2/14 | MEDIUM → LOW |
| ishikawa-fishbone | 3,890 → 8,123 | 5 → 8 | 1 → 5 | 3 → 7 | 0/0/0 → 0/0/0 | MEDIUM → LOW |
| personal-general-2 (supp) | 5,537 → 9,338 | 6 → 16 | 1 → 11 | 3 → 8 | 0/0/0 → 0/0/15 | LOW → LOW |
| personal-general | 3,655 → 9,215 | 5 → 9 | 2 → 2 | 2 → 5 | 0/0/0 → 0/0/0 | MEDIUM → MEDIUM |
| product-business-2 | 3,348 → 8,253 | 5 → 7 | 1 → 7 | 3 → 7 | 0/0/0 → 0/1/1 | MEDIUM → LOW |
| product-business (supp) | 2,797 → 9,545 | 4 → 8 | 1 → 8 | 3 → 5 | 0/0/0 → 0/0/1 | MEDIUM → MEDIUM |
| science-engineering-2 | 3,845 → 9,707 | 7 → 22 | 2 → 15 | 2 → 9 | 0/0/0 → 0/0/1 | MEDIUM → LOW |
| science-engineering | 3,040 → 9,689 | 5 → 10 | 2 → 8 | 2 → 7 | 0/0/0 → 0/0/0 | MEDIUM → MEDIUM |
| self-application¹ | 5,714 → 11,974 | 9 → 13 | 1 → 0 | 3 → 6 | 0/0/0 → 4/6/1 | MEDIUM → MEDIUM |
| software-systems-2 | 5,406 → 10,207 | 7 → 12 | 1 → 1 | 3 → 7 | 0/0/0 → 0/0/1 | MEDIUM → MEDIUM |
| software-systems | 5,409 → 10,726 | 5 → 21 | 0 → 13 | 3 → 6 | 0/0/0 → 0/0/0 | HIGH → MEDIUM |
| theoretical-limit-carnot | 3,984 → 10,647 | 4 → 12 | 1 → 6 | 1 → 8 | 0/0/0 → 0/0/0 | MEDIUM → LOW |

Defects: untraced conclusion claims / malformed chain blocks / nonconforming verdict cells.
`(supp)` rows use the supplementary run; `run_examples.py compare` reads the registered runs, so
it prints the three skipped documents for those rows instead. ¹ Contaminated.

The curated examples stay near-zero on the detector; the re-runs are clean on untraced and
malformed claims in 11 of 14 (three supplementary), with nonconforming verdict cells
concentrated in `estimate-fermi` and `personal-general-2`. Re-runs are 1.7–3.4× longer and lower
or equal in confidence in every case; `software-systems` is the one HIGH example and the
re-run, like its predecessor, rates it MEDIUM — the verified must-fix above says why.

## The agent — findings that are not about the examples

- **Procedure skipped on 3 of 14 registered runs** (v9.13.0: 0 of 14; `delivery-fix-4`: 0 of 12
  after the delivery rule moved to the top of the body). `decompose-irreducibility` opened with a
  `Skill("anthropic-skills:first-principles")` call that failed as unknown, then answered from 10
  searches without reading the template or creating the file. `personal-general-2` made two
  `Bash` calculations and answered in 1,156 words with no contract vocabulary (its first attempt
  was a routing miss). `product-business` made **no tool call at all** and still returned a
  contract-shaped document as its final message. Model, CLI, agent registration and hand-off
  shape were identical to the runs that delivered. The rule binding file delivery is still the
  body's first directive. The body has grown 19% since v9.13.0 (16,772 → 19,982 words), mostly
  delivery machinery. **The paired test did not reproduce the skips**
  ([`skip-paired-reading.md`](skip-paired-reading.md)): on these three prompts, v9.13.0 skipped
  0 of 9 and the current body 1 of 9 (a delivered file without a template read; p = 0.50), and
  every one of the 18 runs delivered its file. The three skips here are not shown to be a
  property of the current body.
- **A wrong delivery pointer.** `estimate-fermi`'s final message points the reader at
  `.first-principles/report-…md` under the repository's absolute path; the files were written in
  the run's own working directory and no such file exists in the repository. The paired test
  found it in 3 of 9 current-body runs and 0 of 9 on v9.13.0 — a current-body defect in the
  final-pointer step, described in [`skip-paired-reading.md`](skip-paired-reading.md).
- **`self-application` contaminated again.** The protocol's export of the body outside the
  repository did not hold: the scratch path encodes the repository's name, the agent located the
  repository, ran `ls`/`find`/`grep` over it, and its grep output included lines of
  `shared/examples/self-application.md`. No other run touched the repository path.

## What limits this reading

One registered run per example; one judge per example. A judge is a judgement, not a
measurement (`CHAIN-JUDGE`, 7 of 13 self-agreement); every update above was re-checked against
the shipped text, but that confirms what the example says, not, for the few outside-world claims
(standards titles, ISO 281 reliability factors, LiFePO4 charging limits, OSTI 1088078's 566 °C
case), that the world agrees — those are marked in the judges' notes as settled by the named
source. Supplementary runs were not registered. Correctness in general is out of scope
(`docs/v8.7-correctness-spot-check.md`).

## Applied — 2026-10-08

Every verified update in the per-example table was applied to `shared/examples/` (13 files) and
regenerated into `first-principles/references/examples/`, with each example's structured-summary
block, provenance roll-up and pre-check lines kept consistent. Band changes that followed from
the fixes: `software-systems` C2, C3 and §6 HIGH → MEDIUM; `ishikawa-fishbone` C1 HIGH → MEDIUM,
and with it Criterion 3 Sound → Hand-wavy (two ground truths now feed only MEDIUM chains — the
rubric's multi-GT shortfall; one Hand-wavy criterion stays within the cap);
`software-systems-2` C3 HIGH → MEDIUM; `science-engineering-2` C2 HIGH → MEDIUM. The
`science-engineering` recommendation changed from a 400 W to a 600 W array on the winter design
basis. No recommendation reversed.

Apparatus changes that the fixes required: SUMM-BLOCK control C31 re-pinned to
`ishikawa-fishbone`'s new §6 pre-check line (it still fails on its own mutation); seven retracted
literals registered in RETRACT-01 (it fails when one is reinserted); the conformance baseline
regenerated (population counts rose, HIGH-chain counts fell, no defect count rose). Battery:
`FIREWALL: GREEN (33/33)`.
