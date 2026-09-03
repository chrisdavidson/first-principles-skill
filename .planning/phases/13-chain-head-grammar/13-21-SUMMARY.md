---
phase: 13-chain-head-grammar
plan: 21
subsystem: quality-harness
tags: [chain-head-grammar, rendering-contract, doc-row-honesty, gap-closure, CR-01, CR-02, CR-03, phase-close]

# Dependency graph
requires:
  - phase: 13-chain-head-grammar (plan 18, CR-02 literal half)
    provides: R9's positional-bound disclosure sentence and re-pointed
      expected_literal_clauses["R9"], which this plan's doc-row correction
      states in prose
  - phase: 13-chain-head-grammar (plan 19, CR-02 fixture half)
    provides: R-HEAD-GTHOP-LATE and the fifteen/ten fixture-population
      counts this plan's doc-row correction states in prose
  - phase: 13-chain-head-grammar (plan 20, CR-03)
    provides: reason-upward.md registered as the fourth _RENDER_RULE_SURFACES
      entry, which this plan's doc-row correction states in prose
provides:
  - both `| QUAL-01 |` doc rows (CLAUDE.md, docs/ARCHITECTURE.md) corrected
    once against the final code state — fifteen fixtures, ten chain-family,
    four registered surfaces, the GTHOP pair's positional scope with its
    non-detected position pinned by R-HEAD-GTHOP-LATE, and the measured
    two-arrow-truncation mechanism behind leg 5's disclosed blind spot,
    replacing the CR-01 misattribution entirely
  - two new locked `_QUAL01_DOC_ROW_TOKENS` entries (R-HEAD-GTHOP-LATE,
    reason-upward.md) with their second inline transcription, four supplied
    per-token rationales (restoring the IN-05 convention for tokens 10-11
    too), and the negative-case count floor/docstring lock moved 22 -> 26
  - WR-05 (orphaned TRACE-03 sentence), WR-02 (leg 5's mislabelled failure
    message) and WR-03 (stale _resolve_artifact docstring) all closed
  - Phase 13 closed: FIREWALL: GREEN (23/23), frozen detector byte-identity
    re-proven across the whole 13-18..13-21 batch, coverage headline swept
    by gate and by grep
affects: []

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "A doc-row correction spanning multiple landed plans is deliberately
      deferred and applied ONCE against the final code state, rather than
      repeated per-plan against a moving target — the discipline this whole
      four-plan closure batch (13-18..13-21) was structured around."
    - "Re-measure a misattribution before republishing a fix — the review's
      prose named a mechanism (any()-over-candidates masking) that a direct
      re-measurement showed is not what fires on the cited reproductions;
      the corrected sentence states the measured mechanism (a two-arrow
      truncation bound), not a supplemented list of candidate causes."

key-files:
  created: []
  modified:
    - CLAUDE.md
    - docs/ARCHITECTURE.md
    - scripts/check-quality-harness.py
    - scripts/check-traceability.py

key-decisions:
  - "Re-measured CR-01's mechanism directly against the live
    _chain_block_well_formed on the three reproduction shapes from
    13-REVIEW.md, instrumenting the algorithm's own candidate-examination
    loop rather than merely counting regex matches — the naive 'lines
    matching _GT_HEAD_RE' count gives 1/2/2 candidates for the three
    shapes, but only the wrap and GT-led-hop reproductions actually
    return True on their FIRST examined candidate (the truncated 2-arrow
    match short-circuits before any second candidate is tried); the
    head-split reproduction genuinely tries a second candidate (i=0
    fails, i=1 succeeds) after the first fails. The corrected sentence
    states the mechanism the wrap/GT-led-hop reproductions demonstrate
    (two-arrow truncation, single examined candidate) since that is what
    the doc row's own two clauses (wrap, GT-led hop) describe; the
    head-split clause is stated separately without claiming
    any()-masking either, per hard constraint 6 (the detector's
    behaviour is out-of-scope, frozen under CONTRACT-06)."
  - "The additional_input's MUTATION Q2 finding (13-20-SUMMARY.md) does
    not require a published-sentence correction: verified by grep that no
    shipped surface (CLAUDE.md, docs/ARCHITECTURE.md, or
    check-quality-harness.py's own comments/docstrings) claims control
    (j) independently re-validates _RENDER_RULE_SURFACES against a
    locked expectation. Control (j)'s own preceding comment already
    states its narrower, accurate job ('proves no registered surface
    silently dropped OUT of the returned records'), and the doc row's
    leg-2 'registry lock' sentence describes control (h)/(h2) — which DID
    fire correctly on the Q2 mutation. The drift was confined to
    13-20-PLAN.md's own acceptance-criteria prediction, a planning
    artifact outside the shipped tree, and is already recorded there as
    an Assumption Drift advisory. No doc change made; recorded here as a
    verified non-issue, not deferred."

requirements-completed: [CHAINHEAD-01, CHAINHEAD-02, CHAINHEAD-03, CHAINHEAD-04, CHAINHEAD-05]

# Metrics
duration: ~55min
completed: 2026-09-03
---

# Phase 13 Plan 21: Doc-row honesty sweep and phase close Summary

Both `| QUAL-01 |` doc rows are now true against the final code state — fifteen fixtures, ten chain-family, four registered surfaces, R9's positional-hop-1 scope with `R-HEAD-GTHOP-LATE` pinning the non-detected position, and a re-measured (not transcribed) two-arrow-truncation mechanism replacing the CR-01 misattribution — with both new claims pinned as locked tokens; three residual findings this phase itself authored (WR-05, WR-02, WR-03) are closed; and Phase 13 ends `FIREWALL: GREEN (23/23)` with the frozen chain detector proven byte-identical across the whole 13-18..13-21 gap-closure batch.

## Performance

- **Duration:** ~55 min
- **Completed:** 2026-09-03
- **Tasks:** 3/3 completed
- **Files modified:** 4 (CLAUDE.md, docs/ARCHITECTURE.md, scripts/check-quality-harness.py, scripts/check-traceability.py)

## Accomplishments

- Re-measured CR-01's real mechanism directly against the live `_chain_block_well_formed` (not transcribed from review prose) on the three reproduction shapes, instrumenting the algorithm's own candidate-examination loop — recorded below — and replaced the `any()`-over-candidates misattribution with the measured two-arrow-truncation mechanism, with zero residual mentions of the old attribution.
- Corrected leg (1)'s fixture-population counts (fourteen → fifteen worked examples, nine → ten chain-family) and leg (2)'s surface count (three → four, registering `shared/references/reason-upward.md` with its `R6-R9` set and a one-clause canonicality rationale) on both doc rows, inside their byte-identical shared suffix.
- Corrected R9's disclosure to state the GTHOP pair pins both directions at hop position 1 only, with `R-HEAD-GTHOP-LATE` pinning the measured non-detection at a later position — mirroring R7/`R-HEAD-PROSE-MID`'s own disclosure shape.
- Pinned both new claims (`R-HEAD-GTHOP-LATE`, `reason-upward.md`) as the 12th/13th `_QUAL01_DOC_ROW_TOKENS` entries with a second inline transcription, supplied all four missing per-token rationales (restoring IN-05's broken convention for tokens 10-11 too), and moved the negative-case count floor and its docstring lock from 22 to 26 — the first count move since 13-17 built the drift-guard lock, exercised here rather than left theoretical.
- Closed WR-05 (repaired the orphaned TRACE-03 sentence to state both 13-15's and 13-17's closures as separate statements, byte-identical across both files), WR-02 (leg 5's failure message no longer calls the `### Conclusion` heading the "head" — it names the heading as a heading and reports the first head-candidate line separately), and WR-03 (`_resolve_artifact`'s docstring now states the post-13-11/13-15/13-17 two-prefix, two-dispatcher, optional-`async` behaviour).
- Closed Phase 13: `FIREWALL: GREEN (23/23)`, `_chain_block_well_formed` proven byte-identical against both this plan's starting commit and the commit that closed plan 13-17 (whole batch), coverage headline unmoved at `175/91/0/266` and confirmed by five targeted greps for renderings `HEADLINE-LOCK` cannot see.

## Task Commits

1. **Task 1: Correct both `| QUAL-01 |` rows against the final code state and pin the two new claims as locked tokens** — `9a9defd` (fix)
2. **Task 2: Close the three residual findings whose text this phase authored (WR-05, WR-02, WR-03)** — `9ee844d` (fix)
3. **Task 3: Close Phase 13 — battery 23/23 GREEN, frozen detector byte-identity re-proven for the batch, headline swept** — no file changes (evidence-only task; all gates passed on the first re-run after `uv sync` resolved the VAL-03 prerequisite, the same one-time gap plans 13-08/13-18/13-19/13-20 documented for this worktree lineage).

**Plan metadata:** (this commit, following SUMMARY creation)

## Files Created/Modified

- `CLAUDE.md` — `| QUAL-01 |` row corrected (fifteen/ten/four counts, GTHOP positional disclosure, CR-01 misattribution replaced); `| TRACE-03 |` row's orphaned sentence repaired
- `docs/ARCHITECTURE.md` — same two corrections, identical text inside the shared byte-identical suffix
- `scripts/check-quality-harness.py` — two new `_QUAL01_DOC_ROW_TOKENS` entries + second transcription + four rationales; negative-case count floor and docstring lock moved 22 → 26; `_render_example_conformance_problems`'s malformed-block message corrected (WR-02)
- `scripts/check-traceability.py` — `_resolve_artifact`'s resolution-rules docstring bullet corrected (WR-03)

## CR-01 Re-measurement (Task 1, before any doc edit)

Driven directly against the live, unmutated `_chain_block_well_formed`, using the review's own three reproduction block shapes, with an instrumented count of lines matching `_GT_HEAD_RE` (naive "candidate" count) alongside a trace of which candidates the algorithm's own loop actually examines before returning:

| Shape | Verdict | Naive candidate-line count | Candidates actually examined |
|---|---|---|---|
| wrap on the final hop | `True` | 1 | 1 (i=0 returns True immediately — the continuation line lacking a leading arrow is never absorbed, so the truncated 2-arrow head+2-hops candidate matches before the wrap is ever reached) |
| GT-led hop after the second arrow | `True` | 2 (head line + the offending hop, since the hop itself contains a `GT-4` token) | 1 (i=0 returns True immediately — `_ARROW_LED_GT_RE` correctly refuses to absorb the GT-led hop, but the already-absorbed 2-arrow truncated candidate matches before the loop would ever try the offending hop as its own candidate at i=3) |
| head split across two physical lines | `True` | 2 (`GT-1 (a) +` and `GT-2 (b)`, each independently matching `_GT_HEAD_RE`) | 2 (i=0 fails — no arrow follows on the next line, so the candidate never reaches 2 arrows; i=1 succeeds — starting from `GT-2 (b)` alone, the two hops absorb cleanly, silently dropping `GT-1`) |

Conclusion, matching the plan's prediction: the wrap and GT-led-hop reproductions each score conforming on their **first examined candidate** — a two-arrow truncation bound, not `any()`-over-candidates masking, since no second candidate is ever tried. The head-split reproduction genuinely does try a second candidate (a real any()-over-candidates instance, dropping `GT-1`), but the doc row's own final sentence only ever described the wrap and GT-led-hop cases as the misattributed pair — the corrected sentence states the two-arrow-truncation mechanism those two demonstrate and separately notes the head-split's first-input-dropped behaviour, without re-invoking `any()` terminology for either. Reproduction script and measurement retained at `/tmp/.../scratchpad/cr01_remeasure.py` (not committed; scratch only).

## Four Supplied Per-Token Rationales (verbatim, `scripts/check-quality-harness.py`)

```
# The tenth token, `call-site census`, added by plan 13-16 (R4-CR-01): without
# it a row can keep describing three forgery-proof floors while the census that
# makes deleting any floor's single real call site loud is silently dropped.
# The eleventh token, `entry-source lock`, added by plan 13-17 (R4-CR-02):
# without it a row can describe a coverage floor whose required side may be
# rebound to its own actual side with the battery green.
# The twelfth token, `R-HEAD-GTHOP-LATE`, added by plan 13-21 (round 5
# closure, `13-VERIFICATION-round5.md`): the sixth token pins the
# GT-leading-hop refusal's prescribed remedy, but neither token states that
# the pair's coverage is positional — without this token a row can claim the
# pair pins R9's refusal "as measured" while silently dropping the fixture
# that pins the position the form check does not reach.
# The thirteenth token, `reason-upward.md`, added by plan 13-21 (round 5
# closure, CR-03's doc half): pins the fourth scanned surface exactly as the
# second token pins the third — without it a row can describe the scan while
# silently reverting to naming three surfaces instead of four.
```

## Count Agreement Across Three Surfaces

| Surface | Value |
|---|---|
| Inline `qual01_negative_case_count` derivation (`len(_QUAL01_DOC_ROWS) * len(_QUAL01_DOC_ROW_TOKENS)`) | `2 * 13 = 26` |
| Adjacent comment arithmetic ("2 doc rows x 13 required tokens = 26 cases") | `26` |
| `_selftest_render_contract` docstring sentence ("derives the expected 26 (2 doc rows x 13 tokens)") | `26` |

All three agree at `26`, confirmed by the passing `(m2) DOCSTRING COUNT LOCK` sub-check and by MUTATION R3 firing in both directions below.

## Shared-Suffix Byte-Identity (hard constraint 2)

- Suffix anchor: `). As of Phase 11 (CONTRACT-03/CONTRACT-05)` through end of the `| QUAL-01 |` line.
- Length **before** this plan's edit: **10738** bytes, identical between `CLAUDE.md` and `docs/ARCHITECTURE.md`.
- Length **after** this plan's edit: **11785** bytes, identical between both files (confirmed by direct string comparison, not by eye).

## MUTATION R1 (four cases, scratch copies only; real tree confirmed clean before/after)

| Case | Command | Result |
|---|---|---|
| Strip `R-HEAD-GTHOP-LATE` from `CLAUDE.md`'s row | `check-quality-harness.py --self-test` | `FAIL: render_contract (m) POSITIVE: CLAUDE.md: the '\| QUAL-01 \|' row is missing required token 'R-HEAD-GTHOP-LATE'` — exit 1 |
| Strip `reason-upward.md` from `CLAUDE.md`'s row | same | `FAIL: render_contract (m) POSITIVE: CLAUDE.md: the '\| QUAL-01 \|' row is missing required token 'reason-upward.md'` — exit 1 |
| Strip `R-HEAD-GTHOP-LATE` from `docs/ARCHITECTURE.md`'s row | same | `FAIL: render_contract (m) POSITIVE: docs/ARCHITECTURE.md: the '\| QUAL-01 \|' row is missing required token 'R-HEAD-GTHOP-LATE'` — exit 1 |
| Strip `reason-upward.md` from `docs/ARCHITECTURE.md`'s row | same | `FAIL: render_contract (m) POSITIVE: docs/ARCHITECTURE.md: the '\| QUAL-01 \|' row is missing required token 'reason-upward.md'` — exit 1 |

## MUTATION R2 (scratch copy)

Dropped `"R-HEAD-GTHOP-LATE",` from `_QUAL01_DOC_ROW_TOKENS` while both doc rows and `expected_qual01_doc_row_tokens` stayed intact:

```
FAIL: render_contract (h) MEMBERSHIP LOCK: qual01_doc_row_tokens: (... 12 entries, R-HEAD-GTHOP-LATE absent ...) != expected (... 13 entries ...)
```

Exit 1, naming `qual01_doc_row_tokens` as required.

## MUTATION R3 (scratch copies, both directions)

**(a) inline count floor left at 22** (docstring/comment untouched):

```
FAIL: render_contract (m) NEGATIVE-CASE COUNT FLOOR: derived 26 (file, token) case(s) from 2 doc row(s) x 13 token(s) != expected 26
```

Exit 1, naming the derived-vs-expected mismatch (the mutated `!=` comparison target).

**(b) docstring transcription left stale** (`26 (2 doc rows x 13 tokens)` reverted to `22 (2 doc rows x 11 tokens)`, inline floor and comment left correct at 26):

```
FAIL: render_contract (m2) DOCSTRING COUNT LOCK: the docstring's transcription reads 'derives the expected 22 (2 doc rows x 11 tokens)' but the live registries derive 'derives the expected 26 (2 doc rows x 13 tokens)' — the NEGATIVE-CASE COUNT FLOOR sentence has drifted from the value the code actually derives
```

Exit 1. This is the first count move since plan 13-17 built the `(m2)` lock, and it fired exactly as designed on both directions.

## MUTATION R4 (scratch copy, `shared/examples/ishikawa-fishbone.md`)

Reintroduced a malformed condition in the first claiming file's first chain block (removed the second hop's leading arrow, dropping the truncated candidate to a single arrow):

**Pre-plan message shape** (reconstructed from the pre-edit code, not re-run against reverted code): `shared/examples/ishikawa-fishbone.md:165: chain block scored malformed under the frozen detector — head '### Conclusion: The primary verified contributor to churn is'`

**Post-plan message** (measured, live):
```
shared/examples/ishikawa-fishbone.md:165: chain block scored malformed under the frozen detector — heading '### Conclusion: The primary verified contributor to churn is', head candidate 'GT-2 (11 of 23 churned accounts cite "felt unsupported") + G'
```

The heading is named as a heading; the head candidate (the first line after it matching `_CHAIN_HEAD_TOKEN_RE`) is reported separately. Mutation restored (scratch copy discarded).

Control (t)'s call-site census for the worked-example-conformance helper (`_render_example_conformance_problems(` occurrence count inside `_selftest_render_contract`'s source): **6**, unchanged from before this plan's message-only edit.

## `_resolve_artifact` Docstring (WR-03)

`_resolve_artifact`'s resolution-rules docstring bullet now mentions both anchor prefixes (`_selftest_`, `_self_test_`), both dispatcher names (`self_test()`, `_run_self_test()`), and the optional `async` form — confirmed programmatically (`'_selftest_' in doc`, `'_self_test_' in doc`, `'self_test()' in doc`, `'_run_self_test()' in doc`, `'async' in doc` all `True`). The three already-disclosed WR-02-deferred boundaries (string-literal/docstring mention counting as dispatch; last-top-level-construct body overrun; first-of-two-dispatcher-names-only sliced) remain stated in `_selftest_dispatch_problems`'s own docstring — confirmed present by grep, unchanged.

## Repaired TRACE-03 Sentence (WR-05)

Byte-identical in both files (confirmed by direct substring containment, not by eye):

> "13-15 (CR-02) closed a fourth, unguarded gap in the same body-slicing step, independent of these three: the body-boundary pattern did not recognise `async def`, so an `async def` construct following the dispatcher was absorbed into its body slice. 13-17 (WR-01) then derived the body-boundary pattern from the dispatcher pattern's own whitespace vocabulary, so a multi-space `async  def`, or a tab-separated `def` construct following the dispatcher is no longer absorbed into its body slice either."

Source of the 13-15 closure statement: `.planning/phases/13-chain-head-grammar/13-15-SUMMARY.md`'s Task 1 ("`_next_top_level_pat` ... widened from `^(?:def |class |@)` to `^(?:async def |def |class |@)`").

## Zero-Count Greps (real tree, post-edit)

```
grep -c '`any()`-over-candidates masking' CLAUDE.md docs/ARCHITECTURE.md   -> 0, 0
grep -c "pin both directions of that behaviour as measured" CLAUDE.md docs/ARCHITECTURE.md  -> 0, 0
```

## `_chain_block_well_formed` Byte-Identity (Task 3, twice)

- Function spans lines **4277-4397** of `scripts/check-quality-harness.py` (`def _chain_block_well_formed` at 4277; `return False` at 4397; next `def _chain_detector_source` at 4400) — unchanged from plans 13-18/13-19/13-20's own measurement.
- **(a) This plan's diff** (`git diff -U0 7b0307953008c7b399c5047fdb54b87ef60575aa HEAD -- scripts/check-quality-harness.py`): all hunks begin at line 6970 or later. `_CHAIN_DETECTOR_PINNED_DIGEST` occurrence count in the diff: `0`.
- **(b) Whole-batch diff** (`git diff -U0 8eb5f76 HEAD -- scripts/check-quality-harness.py`, `8eb5f76` = the commit closing plan 13-17): all hunks begin at line 4429 or later — the earliest (line 4429) is a comment-only edit inside `_chain_detector_source`'s preceding block, changing "three canonical surfaces" to "four" in prose (landed by plan 13-20, not this plan); none overlap the 4277-4397 function-body range. `_CHAIN_DETECTOR_PINNED_DIGEST` occurrence count in the diff: `0`.
- **Live digest**, computed exactly as `_chain_detector_pin_problems` does (`sha256(source.rstrip("\n").encode("utf-8"))`): `sha256:d7d42d7a0bd781bdb01f073d2929f7277c33c86c92f49bb63a48055ad15f13c3` — **matches** `_CHAIN_DETECTOR_PINNED_DIGEST` exactly (not merely a prefix match). Source length: **121 lines**. Prefix `d7d42d7a0bd781bd` confirmed.

## Headline Sweep — Gate Plus Five Named Greps (Task 3)

Gate: `python3 scripts/check-traceability.py --self-test` → `HEADLINE-LOCK PASS: published headline == 175 reproducible / 91 audit-only / 0 gap / 266 total`.

This batch registers no matrix row and re-tiers nothing, so the expected result below is that nothing moved — confirmed as a measured finding, not assumed:

1. **Bare `266-row` count** — `grep -rn "266-row" docs/*.md CLAUDE.md CHANGELOG.md README.md`: 4 hits, all in "generated 266-row capability matrix" phrasing describing the current matrix artifact — none is a stale figure.
2. **Derivation chains stopping one hop short** — `grep -n "161/91\|147/90\|174/92"` across the same surfaces: every hit is a historical delta row (`147/90/0/237 → 161/91/0/252`, etc.) or a fully-chained supersession note that terminates at `175/91/0/266`; none states an intermediate figure as current fact without continuing the chain.
3. **"superseded N times" count** — `CLAUDE.md:233`: "superseded six times" — verified accurate: v8.0's 133/96/0/229 has been superseded by exactly six subsequent moves (META-Q4 re-tier; v4.0/v4.1 retirement; v8.18 Phase 4; v8.24 Phase 6; v8.25 Phase 12; CONTRACT-06 re-tier), unaffected by this batch (no new supersession registered).
4. **Supersession-table arrow** — `grep -n "supersession"`: only `docs/v8.7-constraint-teardown.md:196` ("This record supersedes..."), an unrelated document-level note, not a coverage-figure table.
5. **Headline hard-wrapped across two physical lines** — `grep -n "175 reproducible"` / `grep -rn "175/91"` across all named surfaces: every occurrence of the full headline sits on one physical line; no wrap found.

Nothing moved, as expected.

## MUTATION Q2 Finding — Verified, No Doc Change (per additional_input)

Re-verified against the live tree, per the additional_input directive. `13-20-SUMMARY.md` recorded that MUTATION Q2 (removing the fourth `_RENDER_RULE_SURFACES` entry) fires controls `(h)` and `(k)`, not `(h)` and `(j)` as its own plan predicted — `(j)`'s expected set is derived from the same live tuple being mutated, so it structurally cannot independently catch a shrink of `_RENDER_RULE_SURFACES` itself.

**Verified: no published sentence over-claims this.** Grepped `CLAUDE.md`, `docs/ARCHITECTURE.md`, and `scripts/check-quality-harness.py`'s own comments/docstrings for any claim that control `(j)` independently re-validates the surface registry against a locked expectation (`grep -n "fires.*h.*j\|(h) and (j)\|(j) and (h)\|de-registration" scripts/check-quality-harness.py` — zero hits). Control `(j)`'s own preceding comment already states its real, narrower job accurately: "this floor additionally proves no registered surface silently dropped OUT of the returned records" — never claims to re-validate the registry itself. The `| QUAL-01 |` doc row's leg-2 "registry lock" sentence describes controls `(h)`/`(h2)`, not `(j)` — and `(h)` DID fire correctly on the Q2 mutation (confirmed in 13-20's own measurement). The drift was confined entirely to `13-20-PLAN.md`'s own acceptance-criteria prediction (a `.planning/` artifact, out of scope for the public repo per `docs/v8.0-final-closure.md`'s and CLAUDE.md's own `.planning/` scoping notes), and is already recorded there as an Assumption Drift advisory, exactly the mechanism designed for this. No code or doc change made in response; recorded here as a verified non-issue, not a deferred residual.

## Claim-to-Arm Traceability Table

| New/corrected doc-row claim | Backing arm/mutation | Source SUMMARY |
|---|---|---|
| "fifteen worked examples" / "if any of the fifteen is not requested" | `R-HEAD-GTHOP-LATE` fixture registered as the fifteenth extraction row, arm 4a/4b entries, consumption-floor entry | 13-19-SUMMARY.md Task 2 |
| "the ten chain-family fixtures are additionally re-scored" / "all fifteen locked ids" | chain-family derivation grown 9→10 with zero hand-typed count (`_render_chain_family_ids`); MUTATION P1 | 13-19-SUMMARY.md Task 2 |
| "no registered surface among all four" / `reason-upward.md` added to the path list / its `(R6, R7, R8, R9)` set | `_RENDER_RULE_SURFACES` grown to four entries; `_RENDER_SURFACE_REQUIRED_RULES["shared/references/reason-upward.md"]`; MUTATIONS Q1 (four cases), Q3 | 13-20-SUMMARY.md Task 1/2 |
| GTHOP pair pins both directions "at hop position 1" / `R-HEAD-GTHOP-LATE` pins the non-detection | R9's disclosure sentence (13-18 literal half) + `R-HEAD-GTHOP-LATE` fixture + positional-discrimination control (P3) | 13-18-SUMMARY.md Task 1; 13-19-SUMMARY.md Task 1 |
| leg 5's corrected two-arrow-truncation mechanism, `any()`-masking attribution removed | this plan's own live re-measurement (three block shapes, candidate-examination trace) | this plan (13-21), Task 1 |

## Phase-Closing Table

| Blocking gap (`13-VERIFICATION-round5.md`) | Closing plan(s) | Proving mutation |
|---|---|---|
| Gap 1 (CR-02) — R9 shipped as an unconditional refusal while its measured behaviour is positional | 13-18 (literal half: disclosure sentence, digest recompute) + 13-19 (fixture half: `R-HEAD-GTHOP-LATE`, discriminating third needle on `R-HEAD-GTHOP-BAD`) + this plan (doc-row correction) | 13-18's MUTATION M3(b) (perturbed disclosure clause fails the membership lock); 13-19's MUTATION P3 (moved offending hop fails the chain-verdict floor by name); this plan's MUTATION R1 (stripped token fails control (m) by name) |
| Gap 2 (CR-03) — `shared/references/reason-upward.md` states the chain form with no head grammar and is registered nowhere | 13-20 (registered the surface with R6-R9) + this plan (doc-row correction) | 13-20's MUTATIONS Q1 (four cases, stripped literal fails control (i) by name) and Q2 (de-registration fails (h) MEMBERSHIP LOCK and (k) CASE-COUNT FLOOR); this plan's MUTATION R1 (stripped `reason-upward.md` token fails control (m) by name) |

CR-01 (the frozen detector's two-arrow floor and the doc-row's misattribution of it) was recorded as a non-blocking finding in `13-VERIFICATION-round5.md` — the underlying detector mechanism is an accepted limitation frozen under CONTRACT-06, out of this phase's scope to fix; only the doc-row's causal misattribution was in scope, closed by this plan's Task 1 re-measurement.

## Gate Verdicts (Task 3, final)

1. `python3 scripts/check-quality-harness.py --self-test` → exit 0, all sub-checks including `render_contract` and `chain_detector_pin` PASSED.
2. `python3 scripts/check-traceability.py --self-test` → exit 0; `HEADLINE-LOCK PASS: published headline == 175 reproducible / 91 audit-only / 0 gap / 266 total`.
3. `python3 scripts/sync-content.py --check` → exit 0, no drift.
4. `bash scripts/check-firewall-battery.sh` → final line `FIREWALL: GREEN (23/23)`, exit 0.
   - First run hit `FIREWALL: BLOCKED (1 prerequisite(s) unmet; 22/23 passed)` on VAL-03 (`[PREREQ] VAL-03 — no pytest-capable interpreter found`), the same prerequisite gap plans 13-08/13-18/13-19/13-20 documented for this worktree lineage. Ran `uv sync` (documented CLAUDE.md remedy) to create `.venv`; re-ran to `FIREWALL: GREEN (23/23)`. See Deviations below.
5. `git status --porcelain` on the real tree: empty immediately before this plan's first scratch mutation (Task 1) and empty after every subsequent scratch-mutation cycle across Tasks 1-3, aside from the untracked, gitignored `.venv/` created by `uv sync` (confirmed via `git check-ignore -v .venv`).

## Decisions Made

- Re-measured CR-01's mechanism directly against the live detector, instrumenting which candidates the algorithm's own loop actually examines (not just which lines match the head regex), because the naive line-count measurement (1/2/2) would have contradicted the review's "exactly one candidate" claim for two of the three shapes — the corrected, instrumented measurement (1/1/2 examined candidates) resolves the apparent contradiction and matches the plan's predicted mechanism exactly for the two clauses the doc row actually states.
- Applied the additional_input's MUTATION Q2 directive by verifying (not assuming) that no published sentence over-claims control (j)'s guarantee, and recorded the verification explicitly rather than silently taking no action.
- Kept the "not all fourteen worked examples" doc-row occurrence (leg 5's own file-count clause) unchanged, mapping it to hard constraint/item 7's intent (a file count, not a fixture-population count) even though the doc row's literal wording differs slightly from the plan's quoted source-code phrasing.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - blocking prerequisite] VAL-03 blocked on a missing `.venv`**
- **Found during:** Task 3's closing verification, first `bash scripts/check-firewall-battery.sh` run.
- **Issue:** This worktree had no `.venv`, so no pytest-capable interpreter was found; VAL-03 reported `[PREREQ]` and the battery printed `FIREWALL: BLOCKED` (exit 2), not a gate failure. Identical to the prerequisite gap plans 13-08/13-18/13-19/13-20 documented for the same worktree lineage.
- **Fix:** Ran `uv sync` (documented remedy in CLAUDE.md's own VAL-03 note) to create `.venv`, then re-ran the battery to `FIREWALL: GREEN (23/23)`.
- **Files modified:** none (`.venv/` is gitignored, not committed).

---

**Total deviations:** 1 auto-fixed (1 blocking prerequisite)
**Impact on plan:** No scope creep; the prerequisite fix is a one-time worktree setup step documented as the standard remedy, not a code change.

## Issues Encountered

None beyond the documented VAL-03 prerequisite gap and the MUTATION Q2 verification (both recorded above; neither required a code or doc change).

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

Phase 13 (chain-head-grammar) is closed. Both blocking gaps from round 5 (`13-VERIFICATION-round5.md`) are closed with named proving mutations; the phase's own three self-authored residuals (WR-05, WR-02, WR-03) are closed; the non-blocking CR-01 misattribution is corrected; the battery is `FIREWALL: GREEN (23/23)`; the frozen chain detector is proven byte-identical across the whole four-plan gap-closure batch; and the coverage headline is unmoved and swept by both gate and grep. No blockers for the next milestone phase.

## Self-Check: PASSED

- `CLAUDE.md` — FOUND, contains `R-HEAD-GTHOP-LATE` and `reason-upward.md` on its `| QUAL-01 |` row (grep confirmed, count 1 each).
- `docs/ARCHITECTURE.md` — FOUND, contains `R-HEAD-GTHOP-LATE` and `reason-upward.md` on its `| QUAL-01 |` row (grep confirmed, count 1 each).
- `scripts/check-quality-harness.py` — FOUND, contains the two new `_QUAL01_DOC_ROW_TOKENS` entries, the moved count floor (26), the `(m2)` docstring lock, and the corrected `_render_example_conformance_problems` message.
- `scripts/check-traceability.py` — FOUND, `_resolve_artifact`'s docstring bullet contains both anchor prefixes, both dispatcher names, and "async".
- Commit `9a9defd` — FOUND in `git log --oneline --all`.
- Commit `9ee844d` — FOUND in `git log --oneline --all`.
- `bash scripts/check-firewall-battery.sh` — re-run after both commits landed: `FIREWALL: GREEN (23/23)`, exit 0.

---
*Phase: 13-chain-head-grammar*
*Completed: 2026-09-03*
