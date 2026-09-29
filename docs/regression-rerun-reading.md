# Regression re-run — the reading

**A recorded reading with its N. Not a gate.**
**Protocol:** [`docs/regression-rerun-protocol.md`](regression-rerun-protocol.md) — §1
(`regression-rerun`) and §2 (`regression-rerun-2`), each registered before any run under its id.
**Captures:** `tests/regression-rerun/` and `tests/regression-rerun-2/` (frozen) — each run's
stream, the agent's own transcript, and the delivered file.

---

## The answer

**All four agent regressions the [example re-run](example-rerun-reading.md) found are resolved:
each affected example passed its pre-registered check in both of its runs.** One of them needed a
second attempt. The fifth finding, a defect in the shipped `estimate-fermi` example itself, was
fixed in the example (`ceb16c52`) and needed no run.

| Regression | Example | Body | Run 1 | Run 2 | Resolved |
|---|---|---|---|---|---|
| Combined figure below its inputs | `science-engineering` | `rerun-fixes` | PASS | PASS | yes |
| Success criterion foreclosed the hybrid | `software-systems-2` | `rerun-fixes` (§1) | PASS | **FAIL** | no |
| — revised rule | `software-systems-2` | `rerun-fixes-2` (§2) | PASS | PASS | **yes** |
| `GT6` ids; estimate shown as practice | `theoretical-limit-carnot` | `rerun-fixes` | PASS | PASS | yes |
| Return and loan rate on unstated bases | `personal-general-2` | `rerun-fixes` | PASS | PASS | yes |

All ten runs delivered a complete file on the first attempt; none was a miss.

## The evidence, per run

Each check was scored by reading the document; the evidence is recorded here so it can be
re-checked against the frozen file.

**`science-engineering`** — every combined figure lands where its operation puts it.
- r1: the December tilt-adjusted figure scales from a 2.5 PSH horizontal base (GT-4?) up to 5.0
  PSH (chain C2); every downstream product recomputes in the Recompute block (2,200 ÷ 3.75 =
  586.7 W; 700 × 5.0 × 0.75 = 2,625 Wh).
- r2: derives 170.36 / 31 = 5.50 PSH and carries it consistently.
- Neither run reports a scaled-up figure below its base, which is what the original 4.4 → 4.3 did.

**`theoretical-limit-carnot`** — no bare `GT` + digits id; every practice figure labelled.
- r1: 0 bare ids, 17 distinct hyphenated ids; design-point values read at source and labelled as
  such; the annual-average figure labelled "Estimated".
- r2: 0 bare ids, 11 distinct hyphenated ids; conclusion C8 labels the design-point figures "a
  ceiling on, not a measurement of" practice. **Caveat:** GT-1's own wording says the plant
  "achieves" 41.1%, and the label that makes it a design value arrives only in C8. Passes the
  check as registered; the wording on GT-1 alone would not.

**`personal-general-2`** — both rates stated on a basis, and compared on the same one.
- r1: the mortgage's 6.25% is named nominal, and GT-3? (standard deduction, no tax shield) makes it
  the after-tax rate; the equity return is stated pretax nominal and converted to after-tax before
  comparison, giving a 7.54% pretax nominal break-even (C2). The Assumptions table discards the
  direct rate-versus-raw-return comparison as "naive".
- r2: the mortgage's 6.25% APR becomes an effective 6.4322% with zero tax shield (GT-2?, chain C3);
  the long-run equity baseline is stated 9.8% nominal / 6% real (C2); the break-even is 7.5–7.8%
  pretax nominal (C5), explicitly "not 6.25%".

**`software-systems-2`, §1 (`rerun-fixes`)** — r1 passed (criterion allows "build / buy /
phased-hybrid"; recommends WorkOS plus an in-house tenant/role layer). r2 failed: its first
criterion required "a single option", no split was evaluated, and it recommended buying wholesale.
The Phase 1 sentence alone did not hold, so the rule was revised under §2 rather than re-scored.

**`software-systems-2`, §2 (`rerun-fixes-2`)** — the trade-off procedure's step 1 now requires a
composite option, and Phase 1's exit criterion checks for the exactly-one-option shape.
- r1: the option set is "Build-only, Buy-only, Hybrid (composite)"; weighted totals Hybrid 99,
  Buy-only 89, Build-only 48; recommends the hybrid (buy commodity auth, build the domain audit
  log). Criterion 1 allows "build, buy, or a named hybrid split".
- r2: scores Build, Buy and a thicker Hybrid — 43 / 119 / 110 — and recommends Buy; the Hybrid is
  evaluated and recorded as a Dead End with its reason. No criterion requires exactly one option.
  **Caveat:** its criterion 1 requires the Conclusion to name "a specific per-surface ownership
  split", which leans the other way — it presupposes a split shape. The recommendation still
  describes a per-surface Buy, so it is not self-contradicting, but the rule's aim (criteria state
  what the answer must achieve, not its shape) is only half met in this run.

## What this does and does not show

- **Two runs per example, one model.** A pass shows each rule working on these runs, not a rate.
  §2 exists because the first attempt passed once and failed once.
- **Different bodies.** The three regressions resolved under §1 ran on `rerun-fixes`; the shipped
  body is `rerun-fixes-2`, which adds only the trade-off composite step and the Phase 1 exit check.
  They were not re-run on `rerun-fixes-2`.
- **The regressions were chosen by one judge per pair** in the example re-run; the checks test that
  those specific failures do not recur, not that the documents are better overall.
