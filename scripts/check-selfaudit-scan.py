#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# ///
"""SCAN-GUARD gate: assert the self-audit scan's prescription (plan 15-01), its
verify block and quote-source sentences (plan 15-02), the widened Verdict Block
Format admission covering Criterion 2's Assumption Audit artifact alongside
Criteria 4/6 (plan 15-08), the independently falsifiable Assumption-Audit
half of the scan block's placement predicate (plan 15-09), and the quoted-span
TEMPLATE widened to state the same two admitted-artifact clauses as the
admission paragraph it governs, with a region-split mechanical agreement
check and a superseded-wording pin on both prescriptive surfaces (plan
15-11, closing `15-VERIFICATION.md`'s SCAN-02 gap) are present, correctly
placed and internally coherent in the emitted first-principles tree.
Plan 15-12 (closing `15-VERIFICATION.md` gap 2's two remaining `missing:`
items) strengthens the anti-masking floor that certifies all of the
above: `Rubric-11`'s controls are now parameterized over every
`_BAND_BULLETS` literal rather than exercising one of four, and the
roster floor's `covered` argument is now protected by a falsifiable
ENTRY-SOURCE LOCK against a one-token aliasing rebind.

Phase 15 plan 01 added a `## Self-audit scan (process output)` prescription to
`shared/spine/SKILL-body.md`'s "Before presenting conclusions" section — two tables
(chain form, then claim inventory) emitted after the §6→§4 closure ledger is clean
and before the Self-Audit Gate's verdict blocks. Plan 15-02 added a matching
`**Self-audit scan (verify before scoring)**` pre-scoring block to
`shared/spine/references/validation-rubric.md`, and pointed Criterion 4's and
Criterion 6's `Quoted span:` requirement at the scan's two tables. This gate
asserts both edits against the **emitted** tree —
`first-principles/agents/first-principles.md` and
`first-principles/agents/references/validation-rubric.md` — never against
`shared/`, because the emitted tree is what the model actually loads at runtime;
`DUAL-04` (`sync-content.py --check`) already guarantees `shared/` and the emitted
tree agree, so asserting on the emitted tree transitively covers the source.

This gate is registered as `SCAN-GUARD` in `scripts/check-firewall-battery.sh`
and as the CI job `check-selfaudit-scan (SCAN-GUARD)` in
`.github/workflows/validation.yml`. Both surfaces run TWO legs — `--self-test`
plus the bare live invocation against the shipped `AGENT_FILE`/`RUBRIC_FILE` —
matching the PROV-GUARD and REG-GUARD registration shape (plan 15-09, closing
`15-VERIFICATION.md` gap 2's WR-05 finding). The battery tally is unchanged by
the second leg: `gate()` increments its total once per gate id regardless of
how many commands run under it. The battery first gained this gate id at plan
15-04, under Phase 15 — unreleased at time of writing, so this paragraph
carries no version stamp: the shipped version is whatever
`.claude-plugin/marketplace.json` says, and VERSION-01 moves all 17 stamps in
lockstep at release (the same framing CLAUDE.md's TRACE-03 row uses for its
own unreleased work).

Usage:
    python3 scripts/check-selfaudit-scan.py [--self-test]

Exit codes:
    0  all checks passed
    1  validation failure (a pinned literal, placement, or coherence assertion failed)
    2  environment error (Python <3.12, a target file not found)

--self-test: runs an offline control battery built by mutating in-memory copies of
             the real emitted files, and exits 0 if every control behaves as
             intended (including the anti-masking branch-coverage assertion and the
             in-process dispatch-reachability control); exits 1 on any wrong-pass,
             wrong-reason failure, or uncovered branch.

## What this gate does not assert

(1) It asserts named literals are PRESENT, in the right slice, at the right count
    and in the right order relative to named anchors — not that the surrounding
    prose *means* what they imply.
(2) It does not assert a scan row's CONTENT is correct — that a chain really is
    malformed, that a chain really does or does not participate in a dependency
    cycle or name an ungrounded input
    (`scripts/check-quality-harness.py#_chain_dependency_defects`), or that a
    claim really is untraced — only that the prescription and the verify block
    exist, are placed correctly and are internally coherent. Content
    reconciliation is a narrower, open gap than an earlier version of this
    paragraph implied (`15-REVIEW.md` WR-07, confirmed by reading the function
    body rather than taking the review's word):
    `scripts/check-quality-harness.py#_selfaudit_calibration_defects`
    reconciles a CLAIMED Rigorous band against the measured defect record — it
    never reads the scan itself, since its inputs are
    `_selfaudit_bands(analysis_text)` and the measured `record`; it
    short-circuits entirely on any non-Rigorous band
    (`if bands.get(num) != "Rigorous": continue`); and no check anywhere in
    this tree compares the scan's own `Scan complete: … P chains malformed, Q
    claims untraced` reconciliation line against
    `record["malformed_chain_blocks"]` / `record["untraced_claims"]`, even
    though both are already computed by that point. That three-part gap is an
    open residual this gate does not close, not a duplicate it deliberately
    skips.
(3) It does not assert that a live run COMPLIED with the prescription — a gate can
    assert a prescription is present and well-formed, never that a run obeyed it;
    that layer is 999.12/999.13 and this repo deliberately does not gate on it,
    because a K-of-5 result is a recorded observation, not a gate (governing record
    section 2 item 3, `docs/v8.7-constraint-teardown.md`).
(4) **The requirement-wording deviation, recorded rather than dropped**: SCAN-03 as
    written in `.planning/REQUIREMENTS.md` says "both the agent and skill-stub
    surfaces", but no focused-mode skill stub carries Criterion 4 or Criterion 6 at
    all — `shared/spine/focused-validation-step.md` states that focused-mode
    validation "is a scope-proportionate check, not the six-criterion Self-Audit
    Gate", and that file is the single canonical source for all thirteen stubs.
    This gate therefore targets the two surfaces that really carry the contract,
    the agent body and the agent's rubric reference, which is the HARN-01 pattern
    exactly. No skill-stub-surface assertion is invented to satisfy the literal
    wording, and the clause is not silently dropped. Whether focused-mode surfaces
    belong in rendering-contract scope is backlog 999.16 and is not settled here.
(5) **The disclosed residual after plan 15-07's format-amendment and quoted-span
    pins, corrected at plan 15-11**: the gate pins that the Verdict Block
    Format admits the self-audit scan for Criteria 4 and 6 AND the Assumption
    Audit scan for Criterion 2 — stated in BOTH the quoted-span template and
    the admission paragraph two lines below it, with each of the two clauses
    asserted exactly once per statement (`Rubric-13`'s region split) rather
    than as one union-scoped count over the whole section, so the template
    and the admission cannot drift apart the way rounds 1 and 2 shipped. The
    gate also pins that each of Criteria 4 and 6's quoted-span
    instruction carries both a scan half (scoped to the limbs a scan table
    covers) and a direct-quotation half (for the limbs it does not), and that
    both surfaces state the same table-coverage-bound sentence. It does NOT
    assert that the limbs each direct-quotation half and the coverage-bound
    sentence enumerate — the Abandoned Reasoning section, the
    no-analogies-as-direct-evidence ban, a missing `[Assumes: X]` declaration,
    and Key-Insight non-obviousness — are the COMPLETE set of limbs the two scan
    tables fail to reach, because that completeness is a semantic property of
    the criterion descriptor prose (the Rigorous/Sound/Hand-wavy/Absent bullets
    under Criterion 4 and Criterion 6) and no mechanical check in this tree
    reads descriptor prose. If a future descriptor edit adds a new
    band-determining limb without a column in either scan table, the gate stays
    green and the enumeration goes stale — the same disclosed-bound shape R7/R9/
    R10 carry in `check-quality-harness.py`'s QUAL-01 row. The guard against
    that drift is procedural, not mechanical: a descriptor edit that adds such a
    limb must land in the same plan as an enumeration edit to the direct-half
    sentence and the coverage-bound sentence on both surfaces, which this
    disclosed bound exists to make explicit rather than silently assumed.
(6) **The widened Verdict Block Format admission's enumeration is a census, not
    a mechanical guarantee** (plan 15-08): the admission names the artifacts
    outside the six-section analysis a verdict block may quote — the
    self-audit scan for Criteria 4 and 6, the Assumption Audit scan for
    Criterion 2. That three-artifact enumeration was verified by an
    authoring-time census over the whole `## Criteria` section (searching for
    `process output`, `before scoring`, `Assumption Audit`, `self-audit scan`,
    `closure ledger`, `artifact produced`) and is verified by NO mechanical
    check in this file: a future descriptor edit that bands a further
    criterion on a process-output artifact leaves this gate green and the
    admission stale. `Rubric-14` narrows this by pinning the Criterion 2
    descriptor sentence the C2 admission clause depends on, so that one pair
    cannot drift apart in the direction measured to matter; it does not make
    the enumeration complete against every future descriptor edit. The guard
    against the rest is procedural, matching bound (5)'s shape one level up.
    Plan 15-11 made the quoted-span TEMPLATE state this same three-artifact
    enumeration in the admission's own words, and `Rubric-13`'s region-split
    clause guards now assert the two statements agree mechanically — a fix
    applied to one prescriptive statement and not the other (the specific
    drift that shipped in rounds 1 and 2) is no longer possible. This does
    NOT extend to the enumeration's COMPLETENESS against a future descriptor
    edit, which remains a census, not a mechanical guarantee, exactly as
    stated above.
(7) **`15-REVIEW.md` WR-01 remains open**: the shared table-coverage-bound
    sentence's enumeration of band-determining limbs neither scan table
    reaches is incomplete against the descriptors as they stand today, not
    merely at risk of future drift. The review named three further limbs a
    Criterion 4 or 6 verdict can band on with no column in either table and no
    quoting rule under either half of the instruction: a chain lacking a
    genuine intermediate step, and a conclusion carrying more than one
    derivation chain (both Criterion 4 Sound); and a Conclusion claim
    inconsistent with its section-4 chains (Criterion 6 Hand-wavy). This was
    not named in either `15-VERIFICATION.md` gap's `missing:` list and is not
    closed by this plan.
(8) **`15-REVIEW.md`'s remaining findings, named rather than fixed here**:
    WR-03's not-found reporting arms carry no branch id of their own (net of
    the one `R-02-placement-aa` closed) — Body-3's scan-lead,
    ledger-fence-tail and ledger-clean not-found reports; Rubric-2's
    scan-block and Precedence not-found reports; Rubric-13's
    admission-sentence and Criterion-4-index not-found guards; and
    Rubric-13's region-split anchor not-found guard (`split_idx`, the arm
    plan 15-11 added) — eight arms total, re-measured by per-arm
    neutralization against the tree plans 15-11 and 15-12 leave behind
    (`15-13-SUMMARY.md` Measurement 2; the pre-15-08 review measured seven
    and named five, omitting Rubric-2's two — an omission this plan closes
    by re-deriving the set rather than transcribing it) — are asserted
    only through their sibling count checks. WR-04: `_find_flat`'s
    normalization is not independently load-bearing in any ordering arm,
    because the fail-closed `-1` guard masks its absence — a raw-`find`
    reversion still fails on a hard-wrapped literal via the `-1` guard alone,
    so the two halves of that fix mask each other's absence and neither is
    falsifiable in isolation. IN-04: the self-test's own top-level assertions
    (the anti-masking gate, the dispatch-reachability control, positive
    control (a), `_check_negative`'s check-ID and `expected_detail` matches)
    have no meta-guard beyond the branch and call-site censuses already in
    place — plan 15-12 adds exactly one more such meta-guard, the
    `(roster-es-census)` call-site census over the ENTRY-SOURCE LOCK's own
    real call (bound (12)), narrowing this residual by one instance rather
    than closing it: the four assertions named above are still unguarded.
    IN-05: two residual raw-`str.find`/`.count` sites — `_slice`'s
    heading lookup and Rubric-11's band-bullet count — deviate from the
    file's stated one-discipline (`_find_flat`/`_count_flat`) rule.
(9) **What plan 15-09's live-leg registration and censuses do and do not
    prove**: `validate-census`, `live-census` and `live-dispatch-census` count
    source text and observe no behaviour — each catches DELETION of a real
    call, not a call whose returned result is discarded instead of being
    passed to the failure reporter. This is the same bound
    `check-quality-harness.py`'s own call-site census states about itself.
(10) **What `Rubric-13`'s region split (plan 15-11) does and does not prove**,
    in the same disclosed-bound voice as R7/R9/R10 in `check-quality-harness.py`:
    it proves the two prescriptive statements inside the `## Verdict Block
    Format` section — the fenced quoted-span TEMPLATE and the admission
    paragraph two lines below it — each carry both admitted-artifact clauses,
    independently, so a fix landed on one and not the other fails by name. It
    does NOT reach the agent body's Validate step (`shared/spine/
    SKILL-body.md:298`): that surface's agreement with the rubric's two
    statements is asserted separately, by `Body-17` and `Cross-4`, as literal
    presence rather than as a derived region-split equality — a Validate step
    that dropped a clause would still be caught, just by a different
    mechanism than the one this bound describes. It does NOT assert that the
    template and the admission say the same thing in any sense beyond the two
    clause literals themselves — two statements could carry both clauses,
    verbatim, and still differ in every other word, and this gate would not
    notice.
(11) **What plan 15-12's per-literal `Rubric-11` controls make true, closing
    `15-VERIFICATION.md` gap 2's first `missing:` item**: every literal in
    `_BAND_BULLETS` now carries its own controlled arm in each criterion
    slice (eight ids total, `R-11-bands-crit4/crit6-{rigorous,sound,
    handwavy,absent}`), driven from `zip(_BAND_BULLETS, _BAND_NAMES)` rather
    than a hand-written four-control list, so narrowing the tuple to any
    proper subset leaves the corresponding branch ids uncovered and fails
    the anti-masking floor by name — reproduced live: `_BAND_BULLETS =
    (_BAND_SOUND,)` moved `--self-test` from rc 0 ("All 94 branches
    covered") to rc 1, naming the six now-uncovered ids. A full census of
    every construct in this file where a check iterates over more than one
    literal (nine found in total: `_BAND_BULLETS` plus eight inline
    `for … in (…)` tuples across the body, rubric and cross-surface checks)
    found `_BAND_BULLETS` was the file's ONLY exception before this plan;
    the other eight already carried one hand-written arm per literal. The
    published "every multi-literal tuple has one arm per literal" claim is
    therefore now TRUE of the whole file, with no named exceptions —
    narrower and more precise than an aspiration, per the plan 15-12
    SUMMARY's census table. Deliberately NOT `strict=True` in the `zip`
    call: a length-mismatched `_BAND_BULLETS`/`_BAND_NAMES` pair fails
    LOUDLY (an uncaught `ValueError`, itself a nonzero exit) rather than
    silently, but this makes the LENGTHENING direction fail-open — a fifth
    literal appended to `_BAND_BULLETS` with no matching name appended to
    `_BAND_NAMES` would silently zip only four pairs. Guarded procedurally,
    matching bound (5)'s shape one level up, not mechanically.
(12) **What plan 15-12's ENTRY-SOURCE LOCK does and does not prove, closing
    `15-VERIFICATION.md` gap 2's second `missing:` item**: it proves the
    real `_roster_problems(...)` call's own argument-triple text, read from
    `inspect.getsource(_run_self_test)`, matches the expected
    `REQUIRED_BRANCHES, _BRANCH_ROSTER_LOCK, frozenset(covered_branches)`
    literal whitespace-normalized — reproduced live: aliasing the third
    argument to `frozenset(REQUIRED_BRANCHES)` left `--self-test` at rc 0
    with `ROSTER LOCK: PASS` before this plan (the roster-x1/x2/x3
    isolation arms and the `(roster-census)` call-site census both stayed
    green, because neither ever reads argument text); the same mutation now
    fails naming `(roster-entry-source)`. It does NOT observe behaviour —
    it catches an argument triple that was REWRITTEN (aliased, or the call
    site deleted), not a floor whose returned problems are computed
    correctly and then discarded before reaching `problems`; and an
    argument rebound to an expression of EQUAL VALUE to the one expected is
    harmless by construction and therefore invisible to this check, the
    same DISCLOSED LIMITATION `check-quality-harness.py`'s own
    ENTRY-SOURCE LOCK states for itself. It locks the roster floor's call
    specifically, not every argument of every floor in this file. Adds no
    new `REQUIRED_BRANCHES` ids — it is a named control, not a registered
    branch id, matching the `(roster-census)`/`(validate-census)`/
    `(live-census)` censuses' own status; the branch count stays at 100.

## Measured emission cost (SCAN-04)

Measured against the committed, FROZEN fixture `tests/quality-ledger-v8.26/PR-P1.md`
(recovered 2026-09-02, never regenerated or hand-edited — see the fixture's own
`README.md`). Both measurements below are in-memory only; the frozen file itself
was never written to.

**Assumption Audit scan's existing block** (from `## Assumption Audit scan (process
output)` to `## Self-Audit Gate`, exclusive): **3,408 characters, 52 lines, 44 table
data rows.**

**New self-audit scan block**, built with the real SCAN-01 prescribed shape (a
`## Self-audit scan (process output)` heading, an 8-row chain-form table — one row
per section-4 chain block this fixture actually contains — a 9-row claim-inventory
table — one row per section-6 construct this fixture actually contains, 7 claims
under R11 plus 2 excluded section-intro labels — and a `Scan complete: ...`
reconciliation line with real counts substituted, `P`/`Q` drawn from this fixture's
own measured `malformed_chain_blocks`/`untraced_claims` = 1/1), inserted immediately
before `## Self-Audit Gate` (the same D-04 slot RESEARCH.md §5 measured): **27
lines, 17 table data rows** — both independently reproduced by the
`15-REVIEW.md` reviewer against the same fixture and the same prescribed shape.

**The character-count figure does NOT reproduce, and is disclosed rather than
asserted as settled fact.** This gate's own construction of the block above
measured **2,288 characters**; the `15-REVIEW.md` reviewer's independent
reconstruction of the same prescribed shape from the same fixture measured
**1,381 characters** — a ~40% discrepancy on an uncommitted, hand-constructed
block. Neither figure is backed by a fixture, script or test that emits it, so
neither is mechanically falsifiable as shipped, and no check in this tree
would notice either one regressing. What survives this disclosure regardless
of which count is correct: the new block is smaller than the Assumption Audit
scan's existing block on every OTHER unit measured here — about half its size
in lines (27 / 52) and about two-fifths its size in table rows (17 / 44) — and
the structural-invariance result below, independently reproduced by the
`15-REVIEW.md` reviewer against the same fixture, is unaffected by which
character count is correct. Measured 2026-09-04. The open route to closing
this residual, per the review's suggested fix (`15-REVIEW.md` WR-08): commit
the constructed block as a fixture (e.g.
`tests/quality-ledger-v8.26/PR-P1-with-scan.md`) and add a self-test arm that
recomputes the size figures and the field-by-field invariance from it — the
same shape `check-provenance.py`'s live leg already uses.

**Structural-invariance result** (re-running RESEARCH.md §5's procedure against this
real block shape, not its minimal placeholder): running `detect_defects` on the
original fixture text and on the fixture with the block above inserted at the D-04
slot produces identical values for every field (`conclusion_claims`,
`untraced_claims`, `chain_blocks`, `malformed_chain_blocks`, `dependency_cycles`,
`ungrounded_chains`, `selfaudit_disagreements`, `verdict_cells`,
`nonconforming_verdict_cells`, `closure_ledger_fragments`), and `_slice_sections`'
section-6 slice is byte-for-byte identical (3,097 characters) between the two —
confirming the D-04 insertion moves zero readings against the real, not merely a
placeholder, block shape.

These are the block's size on one committed capture, not a prediction of any other
analysis's size — a different chain count or claim count in a different analysis
renders a differently sized block. No live turn-count measurement exists or is in
scope (999.12/999.13); `maxTurns: 60` (`shared/spine/SKILL.meta.yml`) is unedited by
this phase, and the new scan is prose emitted once in the same process-output slot
the Assumption Audit scan already occupies — it adds no re-entry edge and no
re-perception pass, so it is a structural claim about placement, not a turn-count
measurement.
"""

from __future__ import annotations

import argparse
import contextlib
import inspect
import io
import json
import re
import sys
import textwrap
from pathlib import Path

REPO_ROOT: Path = Path(__file__).resolve().parents[1]
AGENT_FILE: Path = REPO_ROOT / "first-principles" / "agents" / "first-principles.md"
RUBRIC_FILE: Path = (
    REPO_ROOT / "first-principles" / "agents" / "references" / "validation-rubric.md"
)

# --- Body (agent) anchors -----------------------------------------------------
_BODY_SECTION_START = "## Before presenting conclusions"
_BODY_SCAN_LEAD = (
    "**Self-audit scan (emit after the ledger is clean, before the verdict "
    "blocks):**"
)
_BODY_LEDGER_FENCE_TAIL = '- "[claim text]" → CUT (no chain; claim removed)'
_BODY_LEDGER_CLEAN = "Only once the ledger is clean"
_SCAN_HEADING = "## Self-audit scan (process output)"
_COLS_CHAIN = (
    "Chain | Chain Head (brief) | Form conforming? | Rule applied | "
    "Dependency clean?"
)
_COLS_CLAIM = (
    "§6 Span (brief) | Construct | Claim under R11? | R11 clause applied | "
    "Chain cited"
)
_BODY_ROWRULE_CHAIN = "one row per section-4 chain block, in order"
_BODY_ROWRULE_CLAIM = "one row per section-6 construct, in order"
_BODY_REJECTED_ROW = (
    "Every section-6 construct gets a row, non-claims included, each naming "
    "the R11 clause that included or excluded it."
)
_BODY_CLEANPASS = (
    "A chain that conforms and a construct that is not a claim each still "
    "get a row — a clean pass, not a suppressed row."
)
_BODY_LEDGER_INDEP_1 = (
    "derive both tables from the emitted text of sections 4 and 6 without "
    "consulting the §6→§4 closure ledger"
)
_BODY_LEDGER_INDEP_2 = (
    "the closure ledger is not admissible as Criterion 4 or Criterion 6 "
    "evidence — Criteria 4 and 6 quote this scan, never the ledger"
)
_BODY_RECON_LEAD = (
    "close the block with a single reconciliation line a reader can recount "
    "against sections 4 and 6"
)
_BODY_RECON_TEMPLATE = (
    "Scan complete: N chain rows, one per section-4 chain block in order; M "
    "section-6 rows, one per construct in order — K claims under R11, J "
    "excluded. P chains malformed, Q claims untraced."
)
_BODY_PLACEMENT_1 = (
    "included in the response as process output before the Phase 5 verdict "
    "blocks, immediately after the Assumption Audit scan and before the "
    "Self-Audit Gate's verdict blocks, under its own top-level heading"
)
_BODY_PLACEMENT_2 = (
    "This scan is the artifact the Phase-5 rubric's Self-audit scan check "
    "verifies is present, and the source Criteria 4 and 6 draw their quoted "
    "span from."
)
_BODY_REFIX = (
    "If any Fix step adds, removes, renames or re-renders a §4 chain, or "
    "edits a §6 span, re-run the affected rows of this scan against the "
    "current text before re-scoring."
)
_BODY_DISCLOSED_BOUND = (
    "This prescription binds the emission; no gate in this tree checks that "
    "a given run complied with it — a gate can assert the prescription is "
    "present and well-formed, never that a run obeyed it."
)
_BODY_DONOTPRESENT_AMENDED = (
    "Do not present conclusions until the closure ledger is clean, the "
    "self-audit scan has been emitted, AND the Self-Audit Gate is cleared."
)
_BODY_DONOTPRESENT_PREAMENDMENT = (
    "Do not present conclusions until the closure ledger is clean AND the "
    "Self-Audit Gate is cleared."
)
_BODY_VALIDATE_STEP = (
    "**Validate** — apply each gate criterion; quote the specific span that "
    "satisfies or fails each criterion — from the analysis text, or, per "
    "the Verdict Block Format's admission, from the self-audit scan for "
    "Criteria 4 and 6, and the Assumption Audit scan for Criterion 2."
)
_BODY_VALIDATE_PREAMENDMENT = (
    "quote the specific span of your analysis that satisfies or fails "
    "each criterion"
)

# --- Rubric anchors -------------------------------------------------------------
_RUBRIC_AA_BLOCK = "**Assumption Audit (verify before scoring)**"
_RUBRIC_SCAN_BLOCK = "**Self-audit scan (verify before scoring)**"
_RUBRIC_PRECEDENCE = "**Precedence rule (no double-counting):**"
_RUBRIC_FORMAT_START = "## Verdict Block Format"
_RUBRIC_CRITERIA_START = "## Criteria"
_CRIT2_START = "### Criterion 2: Challenge Assumptions"
_CRIT3_START = "### Criterion 3: Establish Ground Truths"
_CRIT4_START = "### Criterion 4: Reason Upward"
_CRIT5_START = "### Criterion 5: Validate"
_CRIT6_START = "### Criterion 6: Conclusion-to-Ground-Truth Traceability"
_USAGE_NOTE = "## Usage Note"

_RUBRIC_DIVLABOUR_1 = (
    "The scan itself is not performed here — the agent already performed it "
    "at Phase 5 emission time (`SKILL.md`, \"Before presenting conclusions\") "
    "before the verdict blocks are written."
)
_RUBRIC_DIVLABOUR_2 = (
    "This gate's job is narrower: verify the scan ran and quote its rows, "
    "not repeat the scan and not re-derive its rows."
)
_RUBRIC_TWO_CRIT_SENTENCE = (
    "This one scan backs two non-adjacent criteria: Criterion 4 quotes the "
    "chain-form table, Criterion 6 quotes the claim-inventory table."
)
_RUBRIC_LEDGER_INADMISSIBLE = (
    "The §6→§4 closure ledger is not admissible as Criterion 4 or Criterion "
    "6 evidence: it is a drafting artifact that ran before the Fix/Repeat "
    "loop, and the scan derives its rows from the emitted text of sections 4 "
    "and 6 without consulting it."
)
_RUBRIC_MISSING_SCAN = (
    "Do not re-perform the scan to fill a missing table; a missing or "
    "incomplete scan is itself the evidence to score against."
)
_RUBRIC_MISSING_SCAN_NEARTWIN = (
    "Do not re-perform the scan to fill a missing table; a missing or "
    "incomplete table is itself the evidence to score against."
)
_RUBRIC_DISCLOSED_BOUND = (
    "Verifying the scan is present and internally coherent is not verifying "
    "its rows are correct — a row's finding is checked against the analysis "
    "text by a reader, and no gate in this tree scores a live run's "
    "compliance."
)
_RUBRIC_QUOTED_SPAN_C4 = (
    "Quoted span: where the band is determined by chain form or chain "
    "dependency, it must be drawn from the self-audit scan's chain-form "
    "table row or rows that determine the band, not from the Derivation "
    "Chains prose directly."
)
_RUBRIC_QUOTED_SPAN_C4_DIRECT = (
    "Where the band is determined by the Abandoned Reasoning section, the "
    "no-analogies-as-direct-evidence ban, or a missing `[Assumes: X]` "
    "declaration — none of which the chain-form table carries a column for "
    "— quote the analysis text directly."
)
_RUBRIC_QUOTED_SPAN_C6 = (
    "Quoted span: where the band is determined by whether a section-6 "
    "claim traces to a named section-4 chain, it must be drawn from the "
    "self-audit scan's claim-inventory table row or rows that determine "
    "the band, not from the Conclusion prose directly."
)
_RUBRIC_QUOTED_SPAN_C6_DIRECT = (
    "Where the band is determined by the Key Insight being a restatement "
    "of the recommended approach rather than a non-obvious finding — a "
    "semantic property the claim-inventory table carries no column for — "
    "quote the analysis text directly."
)
_RUBRIC_FORMAT_QUOTED_SPAN = (
    'Quoted span: "[Direct quote of the specific text that most directly '
    "determines the band assigned — from the analysis being scored, or, "
    "per the admission below, from the self-audit scan for Criteria 4 "
    "and 6 or the Assumption Audit scan for Criterion 2, each emitted "
    'as process output for this analysis.]"'
)
# Pre-15-11 narrow template wording, pinned at count 0 so only reinstatement
# fires it — mirrors _RUBRIC_FORMAT_ADMISSION_SUPERSEDED's role and comment
# shape for plan 15-08's superseded admission clause.
_RUBRIC_FORMAT_QUOTED_SPAN_SUPERSEDED = (
    "for Criteria 4 and 6 only, from the self-audit scan"
)
_RUBRIC_FORMAT_PREAMENDMENT = (
    'Quoted span: "[Direct quote of the specific text in the analysis '
    "being scored — the span\nthat most directly determines the band "
    'assigned.]"'
)
_RUBRIC_FORMAT_ADMISSION = (
    "The self-audit scan and the Assumption Audit scan are not output "
    "sections, and they are the only artifacts outside the six-section "
    "analysis a verdict block may quote: the self-audit scan for "
    "Criteria 4 and 6, and the Assumption Audit scan for Criterion 2. "
    "Every other criterion quotes the analysis text itself, and the "
    "§6→§4 closure ledger is admitted nowhere — it is a drafting "
    "artifact that describes a document other than the one being scored."
)
# The admission sentence's lead clause, up to and including the colon —
# stable because it precedes BOTH admitted-artifact clauses. Used (plan
# 15-11) to locate the TEMPLATE/ADMISSION region boundary instead of the
# full `_RUBRIC_FORMAT_ADMISSION` literal: a clause dropped or duplicated
# from later in the same sentence corrupts the FULL-sentence match (the
# `admission_count` guard correctly fires on that), but must not also
# prevent the per-clause region split from resolving — that would mask the
# specific `R-13-format-admission-*` arm behind a generic "not found"
# failure instead of naming the dropped clause and its region.
_RUBRIC_FORMAT_ADMISSION_LEAD = (
    "The self-audit scan and the Assumption Audit scan are not output "
    "sections, and they are the only artifacts outside the six-section "
    "analysis a verdict block may quote:"
)
_RUBRIC_FORMAT_ADMISSION_SUPERSEDED = (
    "this is the sole place a verdict block may quote something outside "
    "the six-section analysis"
)
_ADMISSION_SCOPE_C46 = "the self-audit scan for Criteria 4 and 6"
_ADMISSION_SCOPE_C2 = "the Assumption Audit scan for Criterion 2"
_RUBRIC_C2_AA_ARTIFACT = (
    "Assumption Audit artifact produced before scoring (per \"How to "
    "Apply This Rubric\") confirms this scan was exhaustive over named "
    "derivation chain steps, not an open-ended survey of the universe "
    "of conceivable assumptions."
)
_TABLE_COVERAGE_BOUND = (
    "Neither table's columns reach every limb its criterion bands on: "
    "Criterion 4 also bands on the Abandoned Reasoning section, the "
    "no-analogies-as-direct-evidence ban and a missing `[Assumes: X]` "
    "declaration, and Criterion 6 also bands on whether the Key Insight "
    "is a restatement of the recommended approach — none of which either "
    "table carries a column for. For those limbs the criterion quotes the "
    "analysis text directly; the scan is quoted only where the band is "
    "determined by what its columns cover."
)
_RUBRIC_HALT_SENTENCE = "Do not proceed to verdict blocks until this is confirmed."
_BAND_RIGOROUS = "- **Rigorous**"
_BAND_SOUND = "- **Sound**"
_BAND_HANDWAVY = "- **Hand-wavy**"
_BAND_ABSENT = "- **Absent**"
_BAND_BULLETS = (_BAND_RIGOROUS, _BAND_SOUND, _BAND_HANDWAVY, _BAND_ABSENT)
# Paired 1:1 with `_BAND_BULLETS` by position — used only to name the
# per-literal Rubric-11 controls below (plan 15-12, closing WR-01): driving
# the control loop from `zip(_BAND_BULLETS, _BAND_NAMES)` rather than a
# hand-written four-control list is what makes narrowing `_BAND_BULLETS`
# itself leave a registered branch id uncovered. Deliberately NOT
# `strict=True`: the plan's own suggested implementation used it, but
# `strict=True` turns the exact mutation this control exists to catch
# (narrowing `_BAND_BULLETS`) into an uncaught `ValueError` traceback
# instead of the clean, named ANTI-MASKING GATE failure the acceptance
# criteria requires — observed live (Rule 1 fix). Plain `zip` truncates to
# the shorter sequence, so narrowing `_BAND_BULLETS` produces fewer
# controls and the anti-masking floor reports the resulting uncovered ids
# by name, which is the behaviour under test. DISCLOSED BOUND: this makes
# the LENGTHENING direction fail-open — a fifth literal appended to
# `_BAND_BULLETS` with no matching fifth name appended to `_BAND_NAMES`
# would silently zip only four pairs, the same procedural (not mechanical)
# guard shape the file's other future-edit bounds already carry.
_BAND_NAMES = ("rigorous", "sound", "handwavy", "absent")

_WS = re.compile(r"\s+")
_H2_RE = re.compile(r"^## ", re.MULTILINE)
_WRAP_WIDTH = 95

# v8.5-Phase-154-style re-entrancy sentinel guarding the dispatch control below.
_SCANGUARD_DISPATCH_REENTRANT = False


def _flat(s: str) -> str:
    """Collapse every whitespace run to a single space.

    The rubric surface is hard-wrapped at roughly 95 columns for its older prose
    (the new Self-audit scan block's own sentences are not, but the neighbouring
    Assumption Audit block's near-twin sentence is), so a raw `literal in text`
    test is blind by construction. Every presence/count assertion below compares
    `_flat` forms for exactly this reason.
    """
    return _WS.sub(" ", s)


def _contains(haystack: str, needle: str) -> bool:
    """Whitespace-insensitive containment for a multi-word pinned literal."""
    return _flat(needle) in _flat(haystack)


def _count_flat(haystack: str, needle: str) -> int:
    """Whitespace-normalized occurrence count, wrap-proof."""
    return _flat(haystack).count(_flat(needle))


def _find_flat(haystack: str, needle: str) -> int:
    """Return the index of `_flat(needle)` inside `_flat(haystack)`, or -1.

    The returned index is an offset into the NORMALIZED text and is
    therefore comparable only against other `_find_flat` results computed
    against the same haystack — never mixed with a raw `str.find` offset.
    Exists to prevent CR-01 (`15-REVIEW.md`): an ordering arm that counted
    a literal with `_count_flat` but then located it with a raw
    `str.find` silently stopped asserting anything about placement the
    moment the literal was hard-wrapped, because `_count_flat` still
    returned 1 while `find` returned -1.
    """
    return _flat(haystack).find(_flat(needle))


def _slice(text: str, start_heading: str, end_heading: str) -> str | None:
    """Return the text strictly between *start_heading* and *end_heading*.

    Returns None if either heading is missing or out of order — a vanished
    section is a failure to report, not an empty string to silently pass
    through.
    """
    start_idx = text.find(start_heading)
    if start_idx == -1:
        return None
    content_start = start_idx + len(start_heading)
    end_idx = text.find(end_heading, content_start)
    if end_idx == -1:
        return None
    return text[content_start:end_idx]


def _slice_to_next_h2(text: str, start_heading: str) -> tuple[str | None, int]:
    """Return (slice strictly between *start_heading* and the next '## '
    heading, count of *start_heading* in the whole file).

    A None slice means the start heading was not found exactly once, or no
    following '## ' heading exists after it.
    """
    count = text.count(start_heading)
    if count != 1:
        return None, count
    start_idx = text.find(start_heading)
    content_start = start_idx + len(start_heading)
    match = _H2_RE.search(text, content_start)
    if match is None:
        return None, count
    return text[content_start : match.start()], count


def _strip_everywhere(text: str, literal: str, replacement: str = "REMOVED") -> str:
    """Remove EVERY occurrence of *literal* from *text* (whitespace-tolerant
    is not needed here since every stripped literal is confirmed single-site
    and unwrapped in the live tree; this operates on the raw string)."""
    assert literal in text, f"target not found in text: {literal!r}"
    return text.replace(literal, replacement)


def _relocate(text: str, literal: str, new_anchor: str) -> str:
    """Remove *literal* (single occurrence) and reinsert it immediately after
    *new_anchor* — the literal remains PRESENT but out of order, which is what
    proves a placement check is not a disguised presence check."""
    count = text.count(literal)
    assert count == 1, f"expected exactly one occurrence of {literal!r}, found {count}"
    removed = text.replace(literal, "", 1)
    anchor_idx = removed.find(new_anchor)
    assert anchor_idx != -1, f"relocation anchor {new_anchor!r} not found after removal"
    idx = anchor_idx + len(new_anchor)
    return removed[:idx] + "\n\n" + literal + "\n\n" + removed[idx:]


def _mutate_within_range(
    text: str, start_anchor: str, end_anchor: str, target: str, replacement: str
) -> str:
    """Replace exactly one occurrence of *target*, located specifically inside
    the [start_anchor, end_anchor) range, leaving any other occurrence of
    *target* elsewhere in the file untouched."""
    start = text.find(start_anchor)
    assert start != -1, f"start anchor {start_anchor!r} not found"
    end = text.find(end_anchor, start)
    assert end != -1, f"end anchor {end_anchor!r} not found after start anchor"
    head, region, tail = text[:start], text[start:end], text[end:]
    count = region.count(target)
    assert count == 1, (
        f"expected exactly one occurrence of {target!r} within range "
        f"[{start_anchor!r}, {end_anchor!r}), found {count}"
    )
    mutated = region.replace(target, replacement, 1)
    return head + mutated + tail


def _hardwrap_reinstate_in_range(
    text: str, start_anchor: str, end_anchor: str, literal: str
) -> str:
    """Strip *literal* from inside the [start_anchor, end_anchor) range, then
    reinsert a hard-wrapped-at-95-columns rendering of it back inside that
    same range.

    Proves `_flat`/`_contains` normalization is load-bearing, not decorative:
    the constructed text must NOT contain the literal contiguously (otherwise
    the arm would prove nothing about wrapping) and must contain it once
    whitespace is normalised.
    """
    start = text.find(start_anchor)
    assert start != -1, f"start anchor {start_anchor!r} not found"
    end = text.find(end_anchor, start)
    assert end != -1, f"end anchor {end_anchor!r} not found after start anchor"
    head, region, tail = text[:start], text[start:end], text[end:]
    count = region.count(literal)
    assert count == 1, (
        f"expected exactly one occurrence of {literal!r} within range, found {count}"
    )
    stripped_region = region.replace(literal, "", 1)
    wrapped = "\n".join(textwrap.wrap(literal, width=_WRAP_WIDTH))
    if literal in wrapped:
        raise ValueError(f"fixture did not break the literal across lines: {literal!r}")
    if not _contains(wrapped, literal):
        raise ValueError(f"wrapped fixture no longer whitespace-normalizes to {literal!r}")
    new_region = stripped_region + "\n\n" + wrapped + "\n"
    return head + new_region + tail


def _hardwrap_relocate_in_range(
    text: str, start_anchor: str, end_anchor: str, literal: str, new_anchor: str
) -> str:
    """Strip *literal* from inside the [start_anchor, end_anchor) range, wrap
    it at `_WRAP_WIDTH`, and reinsert the wrapped rendering immediately AFTER
    *new_anchor* within that same range.

    Combines `_relocate`'s move with `_hardwrap_reinstate_in_range`'s wrap —
    this is CR-01's exact malformation (`15-REVIEW.md`): a sentence that is
    BOTH hard-wrapped AND moved out of order, which a strip-only control
    cannot see. Carries the wrap helper's two self-assertions (the
    constructed text must NOT contain *literal* contiguously, and MUST
    contain it once whitespace is normalized) plus a third: the reinsertion
    point must land inside the range, so a fixture that silently no-ops
    raises instead of producing a vacuous control.
    """
    start = text.find(start_anchor)
    assert start != -1, f"start anchor {start_anchor!r} not found"
    end = text.find(end_anchor, start)
    assert end != -1, f"end anchor {end_anchor!r} not found after start anchor"
    head, region, tail = text[:start], text[start:end], text[end:]
    count = region.count(literal)
    assert count == 1, (
        f"expected exactly one occurrence of {literal!r} within range, found {count}"
    )
    stripped_region = region.replace(literal, "", 1)
    anchor_idx = stripped_region.find(new_anchor)
    assert anchor_idx != -1, (
        f"relocation anchor {new_anchor!r} not found within range after strip"
    )
    wrapped = "\n".join(textwrap.wrap(literal, width=_WRAP_WIDTH))
    if literal in wrapped:
        raise ValueError(f"fixture did not break the literal across lines: {literal!r}")
    if not _contains(wrapped, literal):
        raise ValueError(f"wrapped fixture no longer whitespace-normalizes to {literal!r}")
    insert_idx = anchor_idx + len(new_anchor)
    new_region = (
        stripped_region[:insert_idx] + "\n\n" + wrapped + "\n\n" + stripped_region[insert_idx:]
    )
    return head + new_region + tail


def _duplicate_after(text: str, literal: str, anchor: str) -> str:
    """Insert a second copy of *literal* immediately after *anchor*, leaving
    every existing occurrence of *literal* in *text* untouched.

    *anchor* may equal *literal* itself, in which case the duplicate lands
    right after the literal's own first occurrence. The mirror image of
    `_strip_everywhere`: proves the "duplicated" direction of a `!= 1` count
    guard, not just the "missing" direction.
    """
    anchor_idx = text.find(anchor)
    assert anchor_idx != -1, f"anchor {anchor!r} not found"
    idx = anchor_idx + len(anchor)
    return text[:idx] + "\n\n" + literal + "\n\n" + text[idx:]


def _duplicate_within_range(
    text: str, start_anchor: str, end_anchor: str, literal: str
) -> str:
    """Insert a second copy of *literal* immediately after its own first
    occurrence, scoped inside [start_anchor, end_anchor) — the range's own
    count of *literal* doubles, everything outside the range is untouched."""
    start = text.find(start_anchor)
    assert start != -1, f"start anchor {start_anchor!r} not found"
    end = text.find(end_anchor, start)
    assert end != -1, f"end anchor {end_anchor!r} not found after start anchor"
    head, region, tail = text[:start], text[start:end], text[end:]
    lit_idx = region.find(literal)
    assert lit_idx != -1, f"literal {literal!r} not found within range"
    insert_idx = lit_idx + len(literal)
    new_region = region[:insert_idx] + "\n\n" + literal + "\n\n" + region[insert_idx:]
    return head + new_region + tail


def _flat_pattern(literal: str) -> re.Pattern[str]:
    """Build a whitespace-tolerant regex matching *literal* against RAW
    (non-normalized) text: escape it, then collapse every literal
    single-space token boundary to `\\s+` so the pattern matches whether
    *literal* sits on one physical line or is hard-wrapped across several
    with leading indent — the older-prose shape Criterion 2's Rigorous
    descriptor still carries (binding constraint: that descriptor is not
    unwrapped, unlike this file's plan-15-07/15-08 sentences)."""
    return re.compile(r"\s+".join(re.escape(word) for word in literal.split(" ")))


def _mutate_within_range_flat(
    text: str, start_anchor: str, end_anchor: str, target: str, replacement: str
) -> str:
    """Like `_mutate_within_range`, but locates the single occurrence of
    *target* inside the range via `_flat_pattern` rather than an exact raw
    substring, so a hard-wrapped target is still found. Replaces the
    matched (possibly multi-line) span with *replacement*."""
    start = text.find(start_anchor)
    assert start != -1, f"start anchor {start_anchor!r} not found"
    end = text.find(end_anchor, start)
    assert end != -1, f"end anchor {end_anchor!r} not found after start anchor"
    head, region, tail = text[:start], text[start:end], text[end:]
    matches = list(_flat_pattern(target).finditer(region))
    assert len(matches) == 1, (
        f"expected exactly one whitespace-tolerant match of {target!r} "
        f"within range [{start_anchor!r}, {end_anchor!r}), found {len(matches)}"
    )
    m = matches[0]
    mutated = region[: m.start()] + replacement + region[m.end() :]
    return head + mutated + tail


def _duplicate_within_range_flat(text: str, start_anchor: str, end_anchor: str, target: str) -> str:
    """Like `_duplicate_within_range`, but locates *target* inside the
    range via `_flat_pattern`, for a hard-wrapped target. Inserts a second,
    UNWRAPPED copy of *target* immediately after the matched (possibly
    multi-line) span — the range's flat-normalized count of *target*
    doubles."""
    start = text.find(start_anchor)
    assert start != -1, f"start anchor {start_anchor!r} not found"
    end = text.find(end_anchor, start)
    assert end != -1, f"end anchor {end_anchor!r} not found after start anchor"
    head, region, tail = text[:start], text[start:end], text[end:]
    matches = list(_flat_pattern(target).finditer(region))
    assert len(matches) == 1, (
        f"expected exactly one whitespace-tolerant match of {target!r} "
        f"within range [{start_anchor!r}, {end_anchor!r}), found {len(matches)}"
    )
    m = matches[0]
    new_region = region[: m.end()] + "\n\n" + target + "\n\n" + region[m.end() :]
    return head + new_region + tail


# ---------------------------------------------------------------------------
# Body (agent) checks
# ---------------------------------------------------------------------------


def _check_body_text(text: str) -> list[str]:
    """Validate the emitted agent body text. Returns failure strings (empty ==
    valid). Every failure message begins with its CHECK ID and a colon."""
    failures: list[str] = []

    section, heading_count = _slice_to_next_h2(text, _BODY_SECTION_START)
    if section is None:
        if heading_count != 1:
            failures.append(
                f"Body-1: {_BODY_SECTION_START!r} occurs {heading_count} time(s) "
                "in the whole file, expected exactly 1"
            )
        else:
            failures.append(
                f"Body-1: no '## ' heading found after {_BODY_SECTION_START!r} "
                "— cannot resolve the section slice"
            )
        return failures

    # Body-2: the scan lead occurs exactly once in the section slice and
    # exactly once in the whole file.
    slice_count = _count_flat(section, _BODY_SCAN_LEAD)
    if slice_count != 1:
        failures.append(
            f"Body-2: scan lead occurs {slice_count} time(s) in the section "
            "slice, expected exactly 1"
        )
    whole_count = _count_flat(text, _BODY_SCAN_LEAD)
    if whole_count != 1:
        failures.append(
            f"Body-2: scan lead occurs {whole_count} time(s) in the whole "
            "file, expected exactly 1"
        )

    # Body-3: placement — the scan lead sits strictly between the ledger-form
    # fenced block's tail line and the ledger-clean handoff sentence.
    lead_idx = _find_flat(text, _BODY_SCAN_LEAD)
    tail_idx = _find_flat(text, _BODY_LEDGER_FENCE_TAIL)
    clean_idx = _find_flat(text, _BODY_LEDGER_CLEAN)
    if lead_idx == -1:
        failures.append(f"Body-3: scan lead {_BODY_SCAN_LEAD!r} not found in whole file")
    if tail_idx == -1:
        failures.append(
            f"Body-3: ledger fence tail {_BODY_LEDGER_FENCE_TAIL!r} not found in whole file"
        )
    if clean_idx == -1:
        failures.append(
            f"Body-3: ledger-clean handoff {_BODY_LEDGER_CLEAN!r} not found in whole file"
        )
    if lead_idx != -1 and tail_idx != -1 and clean_idx != -1:
        if not (tail_idx < lead_idx < clean_idx):
            failures.append(
                "Body-3: scan lead is not placed strictly between the ledger "
                "fence tail and the ledger-clean handoff (placement violated)"
            )

    # Body-4: the scan heading occurs exactly once in the section slice.
    heading_in_slice = _count_flat(section, _SCAN_HEADING)
    if heading_in_slice != 1:
        failures.append(
            f"Body-4: scan heading occurs {heading_in_slice} time(s) in the "
            "section slice, expected exactly 1"
        )

    # Body-5: the chain-form column list occurs exactly once in the slice.
    chain_cols_count = _count_flat(section, _COLS_CHAIN)
    if chain_cols_count != 1:
        failures.append(
            f"Body-5: chain-form column list occurs {chain_cols_count} "
            "time(s) in the section slice, expected exactly 1"
        )

    # Body-6: the claim-inventory column list occurs exactly once in the slice.
    claim_cols_count = _count_flat(section, _COLS_CLAIM)
    if claim_cols_count != 1:
        failures.append(
            f"Body-6: claim-inventory column list occurs {claim_cols_count} "
            "time(s) in the section slice, expected exactly 1"
        )

    # Body-7: both row-population rules.
    missing_rowrule = [
        lit
        for lit in (_BODY_ROWRULE_CHAIN, _BODY_ROWRULE_CLAIM)
        if not _contains(section, lit)
    ]
    if missing_rowrule:
        failures.append(
            "Body-7: missing row-rule sentence(s): " + "; ".join(repr(m) for m in missing_rowrule)
        )

    # Body-8: non-claim construct rows are still populated.
    if not _contains(section, _BODY_REJECTED_ROW):
        failures.append(f"Body-8: missing sentence: {_BODY_REJECTED_ROW!r}")

    # Body-9: a conforming/non-claim row is a clean pass, not a suppressed row.
    if not _contains(section, _BODY_CLEANPASS):
        failures.append(f"Body-9: missing sentence: {_BODY_CLEANPASS!r}")

    # Body-10: ledger independence, both halves.
    missing_ledger_indep = [
        lit
        for lit in (_BODY_LEDGER_INDEP_1, _BODY_LEDGER_INDEP_2)
        if not _contains(section, lit)
    ]
    if missing_ledger_indep:
        failures.append(
            "Body-10: missing ledger-independence sentence(s): "
            + "; ".join(repr(m) for m in missing_ledger_indep)
        )

    # Body-11: the single reconciliation line, lead and template.
    missing_recon = [
        lit for lit in (_BODY_RECON_LEAD, _BODY_RECON_TEMPLATE) if not _contains(section, lit)
    ]
    if missing_recon:
        failures.append(
            "Body-11: missing reconciliation sentence(s): "
            + "; ".join(repr(m) for m in missing_recon)
        )

    # Body-12: the scan's own placement-and-provenance sentences.
    missing_placement = [
        lit for lit in (_BODY_PLACEMENT_1, _BODY_PLACEMENT_2) if not _contains(section, lit)
    ]
    if missing_placement:
        failures.append(
            "Body-12: missing placement sentence(s): "
            + "; ".join(repr(m) for m in missing_placement)
        )

    # Body-13: the re-run-on-Fix sentence.
    if not _contains(section, _BODY_REFIX):
        failures.append(f"Body-13: missing re-fix sentence: {_BODY_REFIX!r}")

    # Body-14: the disclosed enforcement bound.
    if not _contains(section, _BODY_DISCLOSED_BOUND):
        failures.append(f"Body-14: missing disclosed-bound sentence: {_BODY_DISCLOSED_BOUND!r}")

    # Body-15: the amended handoff sentence occurs exactly once in the whole
    # file, and the pre-amendment form occurs zero times.
    amended_count = _count_flat(text, _BODY_DONOTPRESENT_AMENDED)
    if amended_count != 1:
        failures.append(
            f"Body-15: amended handoff sentence occurs {amended_count} "
            "time(s) in the whole file, expected exactly 1"
        )
    preamendment_count = _count_flat(text, _BODY_DONOTPRESENT_PREAMENDMENT)
    if preamendment_count != 0:
        failures.append(
            "Body-15: pre-amendment handoff sentence still present "
            f"({preamendment_count} occurrence(s)), expected 0"
        )

    # Body-16: the shared table-coverage-bound sentence (plan 15-07) occurs
    # exactly once in the section slice.
    coverage_bound_count = _count_flat(section, _TABLE_COVERAGE_BOUND)
    if coverage_bound_count != 1:
        failures.append(
            f"Body-16: coverage-bound sentence occurs {coverage_bound_count} "
            "time(s) in the section slice, expected exactly 1"
        )

    # Body-17 (plan 15-08, closing WR-06): the amended Validate step occurs
    # exactly once in the section slice, and the pre-amendment restriction
    # ("quote the specific span of your analysis") is gone from the whole
    # file — the same amended/preamendment shape Body-15 uses.
    validate_count = _count_flat(section, _BODY_VALIDATE_STEP)
    if validate_count != 1:
        failures.append(
            f"Body-17: amended Validate step occurs {validate_count} "
            "time(s) in the section slice, expected exactly 1"
        )

    validate_preamendment_count = _count_flat(text, _BODY_VALIDATE_PREAMENDMENT)
    if validate_preamendment_count != 0:
        failures.append(
            "Body-17: pre-amendment Validate step still present "
            f"({validate_preamendment_count} occurrence(s)) in the whole "
            "file, expected 0"
        )

    return failures


# ---------------------------------------------------------------------------
# Rubric checks
# ---------------------------------------------------------------------------


def _check_rubric_text(text: str) -> list[str]:
    """Validate the emitted rubric text. Returns failure strings (empty ==
    valid)."""
    failures: list[str] = []

    # Rubric-1: the scan block heading occurs exactly once in the whole file.
    # No early return here (WR-10, `15-REVIEW.md`): Rubric-9, Rubric-10 and
    # Rubric-11 assert on the Criterion 4/6 slices, which are structurally
    # independent of the scan-block heading, so a heading defect must not
    # suppress them — Body-1's early return stays because everything after
    # IT genuinely depends on the section slice it resolves; this asymmetry
    # is deliberate, not an oversight to "fix" by symmetry.
    block_count = _count_flat(text, _RUBRIC_SCAN_BLOCK)
    if block_count != 1:
        failures.append(
            f"Rubric-1: scan block heading occurs {block_count} time(s) in "
            "the whole file, expected exactly 1"
        )

    # Rubric-2: placement — the scan block sits strictly between the
    # Assumption Audit block and the Precedence rule paragraph.
    aa_idx = _find_flat(text, _RUBRIC_AA_BLOCK)
    scan_idx = _find_flat(text, _RUBRIC_SCAN_BLOCK)
    precedence_idx = _find_flat(text, _RUBRIC_PRECEDENCE)
    if aa_idx == -1:
        failures.append(f"Rubric-2: {_RUBRIC_AA_BLOCK!r} not found in whole file")
    if scan_idx == -1:
        failures.append(f"Rubric-2: {_RUBRIC_SCAN_BLOCK!r} not found in whole file")
    if precedence_idx == -1:
        failures.append(f"Rubric-2: {_RUBRIC_PRECEDENCE!r} not found in whole file")
    # Split into two independently falsifiable halves (15-VERIFICATION.md
    # gap 2, SCAN-03): the combined predicate previously narrowed to
    # `scan_idx < precedence_idx` left `--self-test` at rc=0 reporting all
    # branches covered when a scan block was relocated BEFORE the Assumption
    # Audit block — the malformation class this split closes. Each half is
    # evaluated only when both indices it compares are `!= -1`, and each
    # emits its own detail so narrowing either half alone fails a distinct
    # named control rather than being covered by the other half's fixture.
    if aa_idx != -1 and scan_idx != -1:
        if not (aa_idx < scan_idx):
            failures.append(
                "Rubric-2: scan block does not follow the Assumption Audit "
                "block (placement violated, Assumption Audit half)"
            )
    if scan_idx != -1 and precedence_idx != -1:
        if not (scan_idx < precedence_idx):
            failures.append(
                "Rubric-2: scan block does not precede the Precedence rule "
                "(placement violated, Precedence half)"
            )

    scan_slice = _slice(text, _RUBRIC_SCAN_BLOCK, _RUBRIC_PRECEDENCE)
    if scan_slice is None:
        failures.append(
            "Rubric-3..8: scan-block slice not found — missing or out-of-order "
            f"heading {_RUBRIC_SCAN_BLOCK!r} / {_RUBRIC_PRECEDENCE!r}"
        )
    else:
        # Rubric-3: the division-of-labour sentence pair.
        missing_divlabour = [
            lit
            for lit in (_RUBRIC_DIVLABOUR_1, _RUBRIC_DIVLABOUR_2)
            if not _contains(scan_slice, lit)
        ]
        if missing_divlabour:
            failures.append(
                "Rubric-3: missing division-of-labour sentence(s): "
                + "; ".join(repr(m) for m in missing_divlabour)
            )

        # Rubric-4: the two-criteria pointer sentence. WR-09 (`15-REVIEW.md`):
        # this check used to also loop over ("Criterion 4", "Criterion 6")
        # asserting each name appears somewhere in `scan_slice` — that loop
        # carried no information, because three OTHER sentences in the same
        # slice already name both criteria (confirmed: neutralizing the loop
        # left it undetected, WR-01's m6), so it never independently failed.
        # Deleted rather than kept as coverage theatre; the presence check
        # below is the real, falsifiable assertion.
        if not _contains(scan_slice, _RUBRIC_TWO_CRIT_SENTENCE):
            failures.append("Rubric-4: missing two-criteria pointer sentence")

        # Rubric-5: both column lists.
        missing_cols = [
            lit for lit in (_COLS_CHAIN, _COLS_CLAIM) if not _contains(scan_slice, lit)
        ]
        if missing_cols:
            failures.append(
                "Rubric-5: missing column list(s) in scan slice: "
                + "; ".join(repr(m) for m in missing_cols)
            )

        # Rubric-6: the ledger non-admissibility sentence.
        if not _contains(scan_slice, _RUBRIC_LEDGER_INADMISSIBLE):
            failures.append("Rubric-6: missing ledger non-admissibility sentence")

        # Rubric-7: the missing-scan sentence, slice-scoped, AND the
        # Assumption Audit near-twin must NOT appear inside this slice.
        if not _contains(scan_slice, _RUBRIC_MISSING_SCAN):
            failures.append("Rubric-7: missing-scan sentence absent from scan slice")
        if _contains(scan_slice, _RUBRIC_MISSING_SCAN_NEARTWIN):
            failures.append(
                "Rubric-7: Assumption-Audit near-twin sentence found inside "
                "scan slice (slice-scoping violated)"
            )

        # Rubric-8: the disclosed-bound sentence.
        if not _contains(scan_slice, _RUBRIC_DISCLOSED_BOUND):
            failures.append("Rubric-8: missing disclosed-bound sentence")

    # Rubric-9: inside Criterion 4's slice, the chain-form (scan-half)
    # quoted-span sentence occurs exactly once and precedes the first
    # Rigorous bullet; the direct-quotation half — for the limbs the
    # chain-form table carries no column for (plan 15-07, closing CR-03) —
    # occurs exactly once in the same slice.
    crit4_slice = _slice(text, _CRIT4_START, _CRIT5_START)
    if crit4_slice is None:
        failures.append(
            "Rubric-9: Criterion 4 slice not found — missing or out-of-order "
            f"heading {_CRIT4_START!r} / {_CRIT5_START!r}"
        )
    else:
        c4_span_count = _count_flat(crit4_slice, _RUBRIC_QUOTED_SPAN_C4)
        if c4_span_count != 1:
            failures.append(
                f"Rubric-9: scan-half quoted-span sentence occurs "
                f"{c4_span_count} time(s) in Criterion 4 slice, expected "
                "exactly 1"
            )
        else:
            # locate on the SAME normalized text the count arm uses (CR-01)
            span_idx = _find_flat(crit4_slice, _RUBRIC_QUOTED_SPAN_C4)
            rigorous_idx = _find_flat(crit4_slice, _BAND_RIGOROUS)
            if span_idx == -1 or rigorous_idx == -1 or not (span_idx < rigorous_idx):
                failures.append(
                    "Rubric-9: scan-half quoted-span sentence does not "
                    "precede the Rigorous band bullet in Criterion 4"
                )

        c4_direct_count = _count_flat(crit4_slice, _RUBRIC_QUOTED_SPAN_C4_DIRECT)
        if c4_direct_count != 1:
            failures.append(
                f"Rubric-9: direct-quotation half occurs {c4_direct_count} "
                "time(s) in Criterion 4 slice, expected exactly 1"
            )

    # Rubric-10: same, for Criterion 6's claim-inventory quoted-span
    # sentence and its direct-quotation half.
    crit6_slice = _slice(text, _CRIT6_START, _USAGE_NOTE)
    if crit6_slice is None:
        failures.append(
            "Rubric-10: Criterion 6 slice not found — missing or out-of-order "
            f"heading {_CRIT6_START!r} / {_USAGE_NOTE!r}"
        )
    else:
        c6_span_count = _count_flat(crit6_slice, _RUBRIC_QUOTED_SPAN_C6)
        if c6_span_count != 1:
            failures.append(
                f"Rubric-10: scan-half quoted-span sentence occurs "
                f"{c6_span_count} time(s) in Criterion 6 slice, expected "
                "exactly 1"
            )
        else:
            # locate on the SAME normalized text the count arm uses (CR-01)
            span_idx = _find_flat(crit6_slice, _RUBRIC_QUOTED_SPAN_C6)
            rigorous_idx = _find_flat(crit6_slice, _BAND_RIGOROUS)
            if span_idx == -1 or rigorous_idx == -1 or not (span_idx < rigorous_idx):
                failures.append(
                    "Rubric-10: scan-half quoted-span sentence does not "
                    "precede the Rigorous band bullet in Criterion 6"
                )

        c6_direct_count = _count_flat(crit6_slice, _RUBRIC_QUOTED_SPAN_C6_DIRECT)
        if c6_direct_count != 1:
            failures.append(
                f"Rubric-10: direct-quotation half occurs {c6_direct_count} "
                "time(s) in Criterion 6 slice, expected exactly 1"
            )

    # Rubric-11: band-descriptor integrity in both criteria's slices.
    if crit4_slice is not None:
        for bullet in _BAND_BULLETS:
            n = crit4_slice.count(bullet)
            if n != 1:
                failures.append(
                    f"Rubric-11: band bullet {bullet!r} occurs {n} time(s) "
                    "in Criterion 4 slice, expected exactly 1"
                )
    if crit6_slice is not None:
        for bullet in _BAND_BULLETS:
            n = crit6_slice.count(bullet)
            if n != 1:
                failures.append(
                    f"Rubric-11: band bullet {bullet!r} occurs {n} time(s) "
                    "in Criterion 6 slice, expected exactly 1"
                )

    # Rubric-12: the halt sentence occurs exactly once inside the scan slice
    # (the Assumption Audit block carries an identical copy by design, so the
    # whole-file count is 2 and only a slice-scoped check is this gate's business).
    if scan_slice is not None:
        halt_count = _count_flat(scan_slice, _RUBRIC_HALT_SENTENCE)
        if halt_count != 1:
            failures.append(
                f"Rubric-12: halt sentence occurs {halt_count} time(s) "
                "inside the scan slice, expected exactly 1"
            )

    # Rubric-13: the Verdict Block Format amendment (plan 15-07, closing
    # CR-02) — the amended quoted-span template and the admission-sentence
    # pair are present exactly once inside the Verdict Block Format
    # section, the pre-amendment template is gone from the whole file, and
    # the admission sentence precedes the Criterion 4 heading.
    format_slice = _slice(text, _RUBRIC_FORMAT_START, _RUBRIC_CRITERIA_START)
    if format_slice is None:
        failures.append(
            "Rubric-13: Verdict Block Format slice not found — missing or "
            f"out-of-order heading {_RUBRIC_FORMAT_START!r} / "
            f"{_RUBRIC_CRITERIA_START!r}"
        )
    else:
        amended_count = _count_flat(format_slice, _RUBRIC_FORMAT_QUOTED_SPAN)
        if amended_count != 1:
            failures.append(
                f"Rubric-13: amended quoted-span template occurs "
                f"{amended_count} time(s) in the Verdict Block Format "
                "section, expected exactly 1"
            )

        admission_count = _count_flat(format_slice, _RUBRIC_FORMAT_ADMISSION)
        if admission_count != 1:
            failures.append(
                f"Rubric-13: admission sentence occurs {admission_count} "
                "time(s) in the Verdict Block Format section, expected "
                "exactly 1"
            )

        # Rubric-13 (plan 15-08, closing CR-01; region-split at plan 15-11,
        # closing SCAN-02): the admission's two clauses — the self-audit
        # scan for Criteria 4/6, and the Assumption Audit scan for
        # Criterion 2 — must each occur exactly once in the TEMPLATE region
        # (the quoted-span instruction itself, widened at plan 15-11) AND
        # exactly once in the ADMISSION region (the sentence governing it),
        # asserted independently per region rather than as one union-scoped
        # count over the whole section — a clause dropped from one
        # statement while the other still states it now fails by name,
        # which is the exact failure mode rounds 1 and 2 shipped (the fix
        # applied to one prescriptive statement and not its twin).
        #
        # NOTE: `split_idx` is scoped to `format_slice` (the Verdict Block
        # Format section only) — NOT the same haystack as `admission_idx`
        # below, which is `_find_flat(text, ...)` over the WHOLE FILE for
        # the "admission precedes Criterion 4" ordering check. `_find_flat`
        # docstrings its own offsets as comparable only within the same
        # haystack; reusing one name for both would invite a cross-haystack
        # comparison that is silently wrong, so the two are kept distinct.
        #
        # Located via `_RUBRIC_FORMAT_ADMISSION_LEAD`, not the full
        # `_RUBRIC_FORMAT_ADMISSION` sentence: the lead precedes both
        # admitted-artifact clauses, so a clause dropped or duplicated
        # later in the same sentence (exactly what the per-clause arms
        # below mutate) leaves the lead intact and the split still
        # resolves — the per-clause counts below are what catches that
        # mutation, not the split itself.
        split_idx = _find_flat(format_slice, _RUBRIC_FORMAT_ADMISSION_LEAD)
        if split_idx == -1:
            failures.append(
                "Rubric-13: admission sentence not found inside the "
                "Verdict Block Format section — cannot region-split the "
                "clause guards"
            )
        else:
            flat_format_slice = _flat(format_slice)
            template_region = flat_format_slice[:split_idx]
            admission_region = flat_format_slice[split_idx:]

            for region_name, region_text, detail_prefix in (
                ("TEMPLATE", template_region, ""),
                ("ADMISSION", admission_region, "admission's "),
            ):
                for clause_name, clause_literal in (
                    ("Criteria-4/6", _ADMISSION_SCOPE_C46),
                    ("Criterion-2", _ADMISSION_SCOPE_C2),
                ):
                    clause_count = region_text.count(_flat(clause_literal))
                    if clause_count != 1:
                        failures.append(
                            f"Rubric-13: {detail_prefix}{clause_name} "
                            f"clause occurs {clause_count} time(s) in the "
                            f"Verdict Block Format {region_name} region, "
                            "expected exactly 1"
                        )

    preamendment_count = _count_flat(text, _RUBRIC_FORMAT_PREAMENDMENT)
    if preamendment_count != 0:
        failures.append(
            "Rubric-13: pre-amendment quoted-span template still present "
            f"({preamendment_count} occurrence(s)) in the whole file, "
            "expected 0"
        )

    admission_idx = _find_flat(text, _RUBRIC_FORMAT_ADMISSION)
    crit4_idx = _find_flat(text, _CRIT4_START)
    if admission_idx == -1 or crit4_idx == -1 or not (admission_idx < crit4_idx):
        failures.append(
            "Rubric-13: admission sentence does not precede the Criterion "
            "4 heading (placement violated)"
        )

    # Rubric-13 (plan 15-08): the superseded 15-07 absolute clause is gone
    # from the whole file — pinned at count 0 so only reinstatement fires
    # it, mirroring the existing _RUBRIC_FORMAT_PREAMENDMENT guard above
    # with a distinct detail string so the two are not confusable.
    superseded_count = _count_flat(text, _RUBRIC_FORMAT_ADMISSION_SUPERSEDED)
    if superseded_count != 0:
        failures.append(
            "Rubric-13: superseded 'sole place' clause still present "
            f"({superseded_count} occurrence(s)) in the whole file, "
            "expected 0"
        )

    # Rubric-13 (plan 15-11): the pre-15-11 narrow quoted-span template
    # wording ("for Criteria 4 and 6 only, from the self-audit scan") is
    # gone from the whole file — pinned at count 0 so only reinstatement
    # fires it, mirroring the two count-0 guards immediately above with a
    # distinct detail string so all three stay unconfusable.
    quoted_span_superseded_count = _count_flat(
        text, _RUBRIC_FORMAT_QUOTED_SPAN_SUPERSEDED
    )
    if quoted_span_superseded_count != 0:
        failures.append(
            "Rubric-13: superseded narrow quoted-span wording still "
            f"present ({quoted_span_superseded_count} occurrence(s)) in "
            "the whole file, expected 0"
        )

    # Rubric-14 (plan 15-08): Criterion 2's Rigorous descriptor still names
    # the Assumption Audit artifact the admission's C2 clause exists for —
    # the two must move together, and deleting the descriptor clause to
    # make the admission's earlier absolute form true again is exactly the
    # regression this arm catches.
    crit2_slice = _slice(text, _CRIT2_START, _CRIT3_START)
    if crit2_slice is None:
        failures.append(
            "Rubric-14: Criterion 2 slice not found — missing or "
            f"out-of-order heading {_CRIT2_START!r} / {_CRIT3_START!r}"
        )
    else:
        c2_descriptor_count = _count_flat(crit2_slice, _RUBRIC_C2_AA_ARTIFACT)
        if c2_descriptor_count != 1:
            failures.append(
                "Rubric-14: Assumption Audit artifact descriptor sentence "
                f"occurs {c2_descriptor_count} time(s) in Criterion 2 "
                "slice, expected exactly 1"
            )

    return failures


def _check_cross_surface(body_text: str, rubric_text: str) -> list[str]:
    """Assert the shared column lists, the scan heading and the table-
    coverage-bound sentence appear on BOTH surfaces. Returns failure
    strings (empty == valid)."""
    failures: list[str] = []
    for col_name, col_literal in (("chain-form column list", _COLS_CHAIN), ("claim-inventory column list", _COLS_CLAIM)):
        if not _contains(body_text, col_literal):
            failures.append(f"Cross-1: {col_name} missing from agent-body surface")
        if not _contains(rubric_text, col_literal):
            failures.append(f"Cross-1: {col_name} missing from rubric surface")
    if not _contains(body_text, _SCAN_HEADING):
        failures.append("Cross-2: scan heading missing from agent-body surface")
    if not _contains(rubric_text, _SCAN_HEADING):
        failures.append("Cross-2: scan heading missing from rubric surface")
    if not _contains(body_text, _TABLE_COVERAGE_BOUND):
        failures.append("Cross-3: coverage-bound sentence missing from agent-body surface")
    if not _contains(rubric_text, _TABLE_COVERAGE_BOUND):
        failures.append("Cross-3: coverage-bound sentence missing from rubric surface")
    if not _contains(body_text, _ADMISSION_SCOPE_C46):
        failures.append("Cross-4: Criteria-4/6 admission clause missing from agent-body surface")
    if not _contains(rubric_text, _ADMISSION_SCOPE_C46):
        failures.append("Cross-4: Criteria-4/6 admission clause missing from rubric surface")
    if not _contains(body_text, _ADMISSION_SCOPE_C2):
        failures.append("Cross-4: Criterion-2 admission clause missing from agent-body surface")
    if not _contains(rubric_text, _ADMISSION_SCOPE_C2):
        failures.append("Cross-4: Criterion-2 admission clause missing from rubric surface")
    # Cross-5 (plan 15-11): the superseded narrow quoted-span wording is
    # absent from BOTH prescriptive surfaces — the rubric arm deliberately
    # overlaps Rubric-13's whole-file count-0 guard (the same overlap
    # Cross-1 already has with Body-05/Rubric-05); the body arm is new
    # coverage, since the agent body's Validate step is the other
    # prescriptive statement of the quoting rule and nothing else stops it
    # regressing to the narrow form.
    if _contains(body_text, _RUBRIC_FORMAT_QUOTED_SPAN_SUPERSEDED):
        failures.append("Cross-5: superseded narrow quoted-span wording present in agent-body surface")
    if _contains(rubric_text, _RUBRIC_FORMAT_QUOTED_SPAN_SUPERSEDED):
        failures.append("Cross-5: superseded narrow quoted-span wording present in rubric surface")
    return failures


def _live_exit_code(failures: list[str]) -> int:
    """Turn a concatenated failure list into a process exit code, in
    `_roster_problems`' voice: never called with anything but the real
    concatenated failure list from `_validate_files` at the real call site
    — the isolation arms in `_run_self_test` drive this same function with
    SYNTHETIC lists, so the failure-to-exit-code decision is proven correct
    independently of whether the shipped tree happens to be clean today.

    Writes one `check-selfaudit-scan: FAIL — <msg>` line to stderr per
    failure and returns 1 when *failures* is non-empty, 0 when it is empty.
    """
    if failures:
        for msg in failures:
            sys.stderr.write(f"check-selfaudit-scan: FAIL — {msg}\n")
        return 1
    return 0


def _validate_files() -> int:
    """Validate the live AGENT_FILE and RUBRIC_FILE. Returns a process exit code."""
    if not AGENT_FILE.exists():
        sys.stderr.write(f"check-selfaudit-scan: agent file not found: {AGENT_FILE}\n")
        return 2
    if not RUBRIC_FILE.exists():
        sys.stderr.write(f"check-selfaudit-scan: rubric file not found: {RUBRIC_FILE}\n")
        return 2

    body_text = AGENT_FILE.read_text(encoding="utf-8")
    rubric_text = RUBRIC_FILE.read_text(encoding="utf-8")

    failures = (
        _check_body_text(body_text)
        + _check_rubric_text(rubric_text)
        + _check_cross_surface(body_text, rubric_text)
    )

    exit_code = _live_exit_code(failures)
    if exit_code != 0:
        return exit_code

    print(f"check-selfaudit-scan: COVERAGE — {AGENT_FILE}, {RUBRIC_FILE}")
    print("check-selfaudit-scan: PASS")
    return 0


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

# D-21-J roster lift (Phase 21 plan 05): `_validate_files`' four call-site
# census legs, lifted from a local tuple inside `_run_self_test` to module
# scope so `describe()` can emit `call_site_census` without executing
# `_run_self_test` itself (D-03: pure, no I/O). `_run_self_test` now reads
# this same constant — a single source, not a parallel copy.
_VALIDATE_LEG_SYMBOLS: tuple[str, ...] = (
    "_check_body_text",
    "_check_rubric_text",
    "_check_cross_surface",
    "_live_exit_code",
)

# The self-test's own infrastructure-level controls — the named checks that
# sit OUTSIDE REQUIRED_BRANCHES/_BRANCH_ROSTER_LOCK (roster equality, the
# call-site censuses, the in-process dispatch controls, and this plan's new
# describe()-consistency control). Hand-authored-once tuple (D-21-J),
# matching batch B's check-act-limb.py precedent — REQUIRED_BRANCHES itself
# is explicitly NOT touched by this plan (its roster floor's two
# independently-transcribed halves are load-bearing and read-only here).
#
# Phase 21-15 (CR-05): this roster used to validate against itself (the
# describe-consistency control above compared `describe()` to this SAME
# constant). `_run_self_test()` now appends each meta-control's own id to a
# local `executed` list as its block's first action, and
# `_selfaudit_meta_floor_problems()` floors `set(executed) ==
# set(_META_CONTROL_IDS)` in both directions before the verdict.
# `roster-floor-missing` and `roster-floor-extra` are permanent negative-arm
# controls proving that floor fires, driven against a synthetic
# executed/registered pair through the SAME helper the live floor calls.
_META_CONTROL_IDS: tuple[str, ...] = (
    "roster-census",
    "roster-lock",
    "roster-entry-source",
    "roster-es-census",
    "validate-census",
    "live-census",
    "dispatch",
    "live-dispatch",
    "live-dispatch-census",
    "describe",
    "roster-floor-missing",
    "roster-floor-extra",
)


def _selfaudit_meta_floor_problems(
    executed: list[str], registered: tuple[str, ...]
) -> list[str]:
    """Pure set-equality floor shared by `_run_self_test()`'s live check and
    its own negative arms (`roster-floor-missing`/`roster-floor-extra`), so
    the arms exercise the SAME code the live floor uses rather than a
    re-implementation.

    Reports both directions in one message (D-04 lesson): a control
    registered but never executed is named under `missing=`; a control that
    executed but was never added to `_META_CONTROL_IDS` is named under
    `extra=`.
    """
    executed_set = set(executed)
    registered_set = set(registered)
    missing = registered_set - executed_set
    extra = executed_set - registered_set
    if missing or extra:
        return [
            f"control roster/executed mismatch: missing={sorted(missing)} "
            f"extra={sorted(extra)}"
        ]
    return []


def _roster_arm_clauses(text: str) -> tuple[str, str]:
    """Split a `..._roster_problems`-shaped message into its `missing=` and
    `extra=` clauses, so a roster negative arm can assert which direction
    its synthetic id actually landed in rather than merely that it appears
    somewhere in the joined message.

    Raises `ValueError` naming the offending text if either clause marker
    is absent, instead of silently returning the whole string as both
    clauses — a message-format change must fail loudly, not disable every
    arm built on this split at once.
    """
    if "missing=" not in text or " extra=" not in text:
        raise ValueError(
            f"roster arm message missing 'missing='/' extra=' markers: {text!r}"
        )
    missing_clause = text.split("missing=", 1)[-1].split(" extra=", 1)[0]
    extra_clause = text.split("extra=", 1)[-1]
    return missing_clause, extra_clause


REQUIRED_BRANCHES: frozenset[str] = frozenset(
    {
        "B-01-slice-count",
        "B-01-slice-noheading",
        "B-02-lead-slice",
        "B-02-lead-whole",
        "B-02-lead-dup",
        "B-03-placement-tail",
        "B-03-placement-clean",
        "B-04-heading-missing",
        "B-04-heading-dup",
        "B-05-cols-chain-missing",
        "B-05-cols-chain-dup",
        "B-06-cols-claim-missing",
        "B-06-cols-claim-dup",
        "B-07-rowrule-chain",
        "B-07-rowrule-claim",
        "B-08-rejected",
        "B-09-cleanpass",
        "B-10-ledger-indep-1",
        "B-10-ledger-indep-2",
        "B-11-recon-lead",
        "B-11-recon-template",
        "B-12-placement-1",
        "B-12-placement-2",
        "B-13-refix",
        "B-14-bound",
        "B-15-donotpresent-amended",
        "B-15-donotpresent-preamendment",
        "B-15-donotpresent-dup",
        "B-16-coverage-bound-missing",
        "B-16-coverage-bound-dup",
        "R-01-block-missing",
        "R-01-block-dup",
        "R-01-no-mask",
        "R-02-placement-order",
        "R-02-placement-anchor",
        "R-02-placement-aa",
        "R-03-divlabour-1",
        "R-03-divlabour-2",
        "R-04-two-criteria",
        "R-05-cols-chain",
        "R-05-cols-claim",
        "R-06-ledger",
        "R-07-missing-absent",
        "R-07-missing-neartwin",
        "R-08-bound",
        "R-09-crit4-count-missing",
        "R-09-crit4-count-dup",
        "R-09-crit4-order",
        "R-09-crit4-direct-missing",
        "R-09-crit4-direct-dup",
        "R-10-crit6-count-missing",
        "R-10-crit6-count-dup",
        "R-10-crit6-order",
        "R-10-crit6-direct-missing",
        "R-10-crit6-direct-dup",
        "R-11-bands-crit4-rigorous",
        "R-11-bands-crit4-sound",
        "R-11-bands-crit4-handwavy",
        "R-11-bands-crit4-absent",
        "R-11-bands-crit6-rigorous",
        "R-11-bands-crit6-sound",
        "R-11-bands-crit6-handwavy",
        "R-11-bands-crit6-absent",
        "R-12-halt-missing",
        "R-12-halt-dup",
        "R-13-format-amended-missing",
        "R-13-format-amended-dup",
        "R-13-format-admission-missing",
        "R-13-format-admission-dup",
        "R-13-format-preamendment",
        "R-13-format-order",
        "R-13-format-admission-c46-missing",
        "R-13-format-admission-c46-dup",
        "R-13-format-admission-c2-missing",
        "R-13-format-admission-c2-dup",
        "R-13-format-admission-superseded",
        "R-13-format-template-c46-missing",
        "R-13-format-template-c46-dup",
        "R-13-format-template-c2-missing",
        "R-13-format-template-c2-dup",
        "R-13-format-quoted-span-superseded",
        "R-14-c2-descriptor-missing",
        "R-14-c2-descriptor-dup",
        "B-17-validate-missing",
        "B-17-validate-dup",
        "B-17-validate-preamendment",
        "X-01-cols-chain-body",
        "X-01-cols-chain-rubric",
        "X-01-cols-claim-body",
        "X-01-cols-claim-rubric",
        "X-02-heading-body",
        "X-02-heading-rubric",
        "X-03-bound-body",
        "X-03-bound-rubric",
        "X-04-admission-c46-body",
        "X-04-admission-c46-rubric",
        "X-04-admission-c2-body",
        "X-04-admission-c2-rubric",
        "X-05-superseded-body",
        "X-05-superseded-rubric",
    }
)

# Anti-vacuity floor for REQUIRED_BRANCHES itself (WR-02, `15-REVIEW.md`): the
# anti-masking assertion below is computed FROM `REQUIRED_BRANCHES`
# (`REQUIRED_BRANCHES - covered_branches`), so it cannot see that set itself
# being silently narrowed — the verifier measured exactly this, deleting two
# entries and leaving `--self-test` green with a message
# ("All 27 branches covered") that reads identical in kind to the honest one.
# `_BRANCH_ROSTER_LOCK` is a SECOND, independently typed transcription of
# every branch id; `_roster_problems` compares it against `REQUIRED_BRANCHES`
# by equality before the anti-masking assertion runs, so adding or removing a
# branch is deliberately a two-place edit. DISCLOSED LIMITATION, the same
# bound `check-quality-harness.py`'s ENTRY-SOURCE LOCK states for its own
# required sides: a transcription of EQUAL value written a different way is
# harmless by construction and therefore invisible to this floor — only a
# set that actually differs is caught.
_BRANCH_ROSTER_LOCK: frozenset[str] = frozenset(
    {
        "B-01-slice-count", "B-01-slice-noheading",
        "B-02-lead-slice", "B-02-lead-whole", "B-02-lead-dup",
        "B-03-placement-tail", "B-03-placement-clean",
        "B-04-heading-missing", "B-04-heading-dup",
        "B-05-cols-chain-missing", "B-05-cols-chain-dup",
        "B-06-cols-claim-missing", "B-06-cols-claim-dup",
        "B-07-rowrule-chain", "B-07-rowrule-claim",
        "B-08-rejected", "B-09-cleanpass",
        "B-10-ledger-indep-1", "B-10-ledger-indep-2",
        "B-11-recon-lead", "B-11-recon-template",
        "B-12-placement-1", "B-12-placement-2",
        "B-13-refix", "B-14-bound",
        "B-15-donotpresent-amended", "B-15-donotpresent-preamendment",
        "B-15-donotpresent-dup",
        "B-16-coverage-bound-missing", "B-16-coverage-bound-dup",
        "R-01-block-missing", "R-01-block-dup", "R-01-no-mask",
        "R-02-placement-order", "R-02-placement-anchor", "R-02-placement-aa",
        "R-03-divlabour-1", "R-03-divlabour-2",
        "R-04-two-criteria",
        "R-05-cols-chain", "R-05-cols-claim",
        "R-06-ledger",
        "R-07-missing-absent", "R-07-missing-neartwin",
        "R-08-bound",
        "R-09-crit4-count-missing", "R-09-crit4-count-dup", "R-09-crit4-order",
        "R-09-crit4-direct-missing", "R-09-crit4-direct-dup",
        "R-10-crit6-count-missing", "R-10-crit6-count-dup", "R-10-crit6-order",
        "R-10-crit6-direct-missing", "R-10-crit6-direct-dup",
        "R-11-bands-crit4-rigorous", "R-11-bands-crit4-sound",
        "R-11-bands-crit4-handwavy", "R-11-bands-crit4-absent",
        "R-11-bands-crit6-rigorous", "R-11-bands-crit6-sound",
        "R-11-bands-crit6-handwavy", "R-11-bands-crit6-absent",
        "R-12-halt-missing", "R-12-halt-dup",
        "R-13-format-amended-missing", "R-13-format-amended-dup",
        "R-13-format-admission-missing", "R-13-format-admission-dup",
        "R-13-format-preamendment", "R-13-format-order",
        "R-13-format-admission-c46-missing", "R-13-format-admission-c46-dup",
        "R-13-format-admission-c2-missing", "R-13-format-admission-c2-dup",
        "R-13-format-admission-superseded",
        "R-13-format-template-c46-missing", "R-13-format-template-c46-dup",
        "R-13-format-template-c2-missing", "R-13-format-template-c2-dup",
        "R-13-format-quoted-span-superseded",
        "R-14-c2-descriptor-missing", "R-14-c2-descriptor-dup",
        "B-17-validate-missing", "B-17-validate-dup", "B-17-validate-preamendment",
        "X-01-cols-chain-body", "X-01-cols-chain-rubric",
        "X-01-cols-claim-body", "X-01-cols-claim-rubric",
        "X-02-heading-body", "X-02-heading-rubric",
        "X-03-bound-body", "X-03-bound-rubric",
        "X-04-admission-c46-body", "X-04-admission-c46-rubric",
        "X-04-admission-c2-body", "X-04-admission-c2-rubric",
        "X-05-superseded-body", "X-05-superseded-rubric",
    }
)


def describe() -> dict[str, object]:
    """This gate's own self-description (D-03, plan 21-05): pure, no disk
    I/O, no argv, no subprocess. `branch_roster`/`branch_count` are
    `REQUIRED_BRANCHES` — read only, never edited by this plan.
    `registered_surfaces` names `AGENT_FILE`/`RUBRIC_FILE`.
    `call_site_census` is `_VALIDATE_LEG_SYMBOLS` (each expected exactly
    once, the `(validate-census)` shape). `control_ids`/`control_count`
    are `_META_CONTROL_IDS` — the self-test's infrastructure-level
    controls that sit outside the branch roster. `locked_constants`
    carries the `_BAND_BULLETS` literal set (joined, since the
    vocabulary's `locked_constants` shape is scalar-valued)."""
    return {
        "branch_roster": sorted(REQUIRED_BRANCHES),
        "branch_count": len(REQUIRED_BRANCHES),
        "registered_surfaces": sorted(
            {
                str(AGENT_FILE.relative_to(REPO_ROOT)),
                str(RUBRIC_FILE.relative_to(REPO_ROOT)),
            }
        ),
        "call_site_census": {symbol: 1 for symbol in _VALIDATE_LEG_SYMBOLS},
        "control_ids": list(_META_CONTROL_IDS),
        "control_count": len(_META_CONTROL_IDS),
        "locked_constants": {"band_bullets": " | ".join(_BAND_BULLETS)},
    }


def _roster_problems(
    required: frozenset[str], lock: frozenset[str], covered: frozenset[str]
) -> list[str]:
    """Pure comparison the roster-equality and coverage-subset floors share.

    Never called with anything but `REQUIRED_BRANCHES`, `_BRANCH_ROSTER_LOCK`
    and `covered_branches` at the real call site — the isolation arms in
    `_run_self_test` drive this same function with SYNTHETIC id sets so the
    comparison logic itself is proven correct independently of whether the
    two real registries happen to agree today.
    """
    problems: list[str] = []
    if required != lock:
        problems.append(
            "ROSTER LOCK: REQUIRED_BRANCHES drifted from _BRANCH_ROSTER_LOCK: "
            f"missing={sorted(lock - required)}, extra={sorted(required - lock)}"
        )
    surplus = covered - required
    if surplus:
        problems.append(
            "ROSTER LOCK: control claims unregistered branch id(s) "
            f"(typo'd branch_id?): {sorted(surplus)}"
        )
    return problems


def _entry_source_problems(source_text: str, expected_call_args: str) -> list[str]:
    """Pure comparison behind the roster floor's ENTRY-SOURCE LOCK (plan
    15-12, WR-04 `15-REVIEW.md`) — mirrors `check-quality-harness.py`'s (x)
    ENTRY-SOURCE LOCK (R4-CR-02), applied to a call site's own argument text
    rather than to a floor-registry entry's required/actual pair.

    THE FLOOR ITSELF (`_roster_problems`'s surplus arm, `covered - required`)
    is only as trustworthy as the real call's own `covered` argument — a
    one-token rebind of that argument to `frozenset(REQUIRED_BRANCHES)`
    makes the surplus computation `x != x`, structurally incapable of
    reporting a problem, while the roster-x1/x2/x3 isolation arms and the
    (roster-census) call-site census both still pass, because they only
    ever drive `_roster_problems` with SYNTHETIC id sets and count
    OCCURRENCES of the call pattern, never its argument text — reproduced
    live (see the plan 15-12 SUMMARY's Step A re-reproduction).

    Asserts *expected_call_args* — the real call site's own argument-triple
    text — appears, whitespace-normalized (`_contains`, wrap-proof), inside
    *source_text*. Never called with anything but
    `inspect.getsource(_run_self_test)` and the real call's own argument
    text at the real call site; the roster-es-x1/x2/x3 isolation arms in
    `_run_self_test` drive this same function with SYNTHETIC source strings
    only, so the comparison logic is proven correct independently of
    whether the real call site happens to carry the correct triple today.

    DISCLOSED LIMITATION, in the same voice as `check-quality-harness.py`'s
    own ENTRY-SOURCE LOCK disclosure: this compares SOURCE TEXT and
    observes no behaviour — it catches an argument triple that was
    REWRITTEN (aliased to another name, or the call site deleted), not a
    floor whose returned problems are computed correctly and then
    discarded before reaching `problems`; and an argument rebound to an
    expression of EQUAL VALUE to the one expected is harmless by
    construction and therefore invisible to this check. It locks the
    roster floor's call specifically, not every argument of every floor in
    this file.
    """
    if _contains(source_text, expected_call_args):
        return []
    return [
        f"real call's argument-triple text {expected_call_args!r} not "
        "found in source (rewritten, aliased, or missing call site)"
    ]


def _run_self_test() -> int:
    """Run the offline control battery. Returns 0 on all-pass, 1 on any failure."""
    if not AGENT_FILE.exists() or not RUBRIC_FILE.exists():
        sys.stderr.write(
            "check-selfaudit-scan --self-test: cannot derive fixtures — "
            f"{AGENT_FILE} or {RUBRIC_FILE} not found\n"
        )
        return 2

    real_body = AGENT_FILE.read_text(encoding="utf-8")
    real_rubric = RUBRIC_FILE.read_text(encoding="utf-8")

    problems: list[str] = []
    covered_branches: set[str] = set()

    # Phase 21-15 (CR-05): every meta-control below appends its own id from
    # _META_CONTROL_IDS to this list as its block's first action — floored
    # against _META_CONTROL_IDS at the end of this function via
    # `_selfaudit_meta_floor_problems()`, in both directions.
    # REQUIRED_BRANCHES/_BRANCH_ROSTER_LOCK's own fixture battery (below,
    # via `_check_negative`) is a separate, pre-existing, read-only floor
    # and is NOT tracked in this list.
    executed: list[str] = []

    def _check_negative(
        label: str,
        failures: list[str],
        expected_check_id: str,
        expected_detail: str | None = None,
        branch_id: str | None = None,
    ) -> None:
        """Assert a mutated fixture failed, and failed for its OWN reason.

        The match key is the failing message's own CHECK ID, plus (optionally)
        a sub-item detail unique to the assertion under test — never a free-text
        substring against ANY failure in the list, which lets a sibling check's
        message accidentally satisfy a control's expectation.
        """

        def _fired_ids(msgs: list[str]) -> list[str]:
            return sorted({m.split(" ", 1)[0].rstrip(":") for m in msgs})

        def _id_matches(msg: str, check_id: str) -> bool:
            if not msg.startswith(check_id):
                return False
            rest = msg[len(check_id) :]
            return rest[:1] in (" ", ":")

        if not failures:
            print(f"({label}) WRONGLY PASSED (expected failure)")
            problems.append(f"{label}: no failures produced")
            return
        matched = [f for f in failures if _id_matches(f, expected_check_id)]
        if not matched:
            print(
                f"({label}) failed for the WRONG reason (expected check ID "
                f"{expected_check_id!r}; check IDs that DID fire: "
                f"{', '.join(_fired_ids(failures))}; got: {'; '.join(failures)})"
            )
            problems.append(f"{label}: wrong-reason failure")
            return
        if expected_detail is not None and not any(expected_detail in f for f in matched):
            print(
                f"({label}) failed for the WRONG reason (check ID "
                f"{expected_check_id!r} fired but no message of that ID contains "
                f"detail {expected_detail!r}; check IDs that DID fire: "
                f"{', '.join(_fired_ids(failures))}; got: {'; '.join(matched)})"
            )
            problems.append(f"{label}: wrong-reason failure")
            return
        print(f"({label}) correctly failed ({len(failures)} failure(s))")
        if branch_id is not None:
            covered_branches.add(branch_id)

    # (a) Positive control — body.
    a_failures = _check_body_text(real_body)
    if a_failures:
        print(f"(a) positive control — body: WRONGLY FAILED: {'; '.join(a_failures)}")
        problems.append("(a): unexpected failures against real body")
    else:
        print("(a) positive control — body: PASS (0 failures)")

    # (b) Positive control — rubric.
    b_failures = _check_rubric_text(real_rubric)
    if b_failures:
        print(f"(b) positive control — rubric: WRONGLY FAILED: {'; '.join(b_failures)}")
        problems.append("(b): unexpected failures against real rubric")
    else:
        print("(b) positive control — rubric: PASS (0 failures)")

    # (c) Positive control — cross-surface.
    c_failures = _check_cross_surface(real_body, real_rubric)
    if c_failures:
        print(f"(c) positive control — cross-surface: WRONGLY FAILED: {'; '.join(c_failures)}")
        problems.append("(c): unexpected failures against real cross-surface check")
    else:
        print("(c) positive control — cross-surface: PASS (0 failures)")

    # --- Body branch negative controls -------------------------------------
    # Clause-level split (plan 15-06, closing WR-01's body-surface rows m5,
    # m7, m8, m9, m10, m19, m21): every `!= 1` count guard gets a MISSING
    # (0) arm and, where the guard is genuinely `!= 1` rather than `< 1`, a
    # DUPLICATE (2) arm; every combined placement predicate gets one arm per
    # half; every multi-literal tuple gets one arm per literal.

    # B-01-slice-count: strip the section-start heading (occurs 0 times) —
    # the count guard fires before the slice is even attempted.
    body_b01a = _strip_everywhere(real_body, _BODY_SECTION_START)
    _check_negative(
        "B-01a",
        _check_body_text(body_b01a),
        "Body-1",
        "occurs 0 time(s)",
        "B-01-slice-count",
    )

    # B-01-slice-noheading: the section-start heading occurs exactly once,
    # but nothing that looks like a following '## ' heading exists — the
    # count guard passes, `_slice_to_next_h2` still cannot resolve the slice.
    _b01b_start = real_body.find(_BODY_SECTION_START)
    assert _b01b_start != -1, "section start heading not found in real body"
    body_b01b = (
        real_body[: _b01b_start + len(_BODY_SECTION_START)]
        + "\n\nNo further heading follows this line.\n"
    )
    _check_negative(
        "B-01b",
        _check_body_text(body_b01b),
        "Body-1",
        "no '## ' heading found",
        "B-01-slice-noheading",
    )

    # B-02-lead-slice / B-02-lead-whole (missing direction): the scan lead
    # has exactly one occurrence in the real body, so stripping it fires
    # BOTH the slice-scoped and whole-file count guards in one fixture —
    # each `_check_negative` call below targets its own guard's distinct
    # message text inside that same failures list.
    body_b02_strip = _strip_everywhere(real_body, _BODY_SCAN_LEAD)
    _b02_strip_failures = _check_body_text(body_b02_strip)
    _check_negative(
        "B-02-slice",
        _b02_strip_failures,
        "Body-2",
        "in the section slice, expected exactly 1",
        "B-02-lead-slice",
    )
    _check_negative(
        "B-02-whole-missing",
        _b02_strip_failures,
        "Body-2",
        "in the whole file, expected exactly 1",
        "B-02-lead-whole",
    )

    # B-02-lead-dup: duplicate the scan lead INSIDE the section slice — the
    # slice-scoped count guard now fires in the "occurs 2 time(s)" direction,
    # which the missing-direction fixture above cannot exercise.
    body_b02_dup = _duplicate_within_range(
        real_body, _BODY_SECTION_START, _BODY_LEDGER_CLEAN, _BODY_SCAN_LEAD
    )
    _check_negative(
        "B-02-dup",
        _check_body_text(body_b02_dup),
        "Body-2",
        "in the section slice",
        "B-02-lead-dup",
    )

    # B-03-placement-clean: relocate the scan lead PAST the ledger-clean
    # handoff — violates the `lead_idx < clean_idx` half of the placement
    # predicate while `tail_idx < lead_idx` still holds.
    body_b03_clean = _relocate(real_body, _BODY_SCAN_LEAD, _BODY_LEDGER_CLEAN)
    _check_negative(
        "B-03-clean",
        _check_body_text(body_b03_clean),
        "Body-3",
        "placement violated",
        "B-03-placement-clean",
    )

    # B-03-placement-tail: relocate the scan lead BEFORE the ledger fence
    # tail — violates the `tail_idx < lead_idx` half while `lead_idx <
    # clean_idx` still holds. This is WR-01's m19: a predicate narrowed to
    # only the "clean" half leaves this fixture undetected.
    body_b03_tail = _relocate(real_body, _BODY_SCAN_LEAD, _BODY_SECTION_START)
    _check_negative(
        "B-03-tail",
        _check_body_text(body_b03_tail),
        "Body-3",
        "placement violated",
        "B-03-placement-tail",
    )

    # B-04-heading-missing: strip the scan heading.
    body_b04a = _strip_everywhere(real_body, _SCAN_HEADING)
    _check_negative(
        "B-04a",
        _check_body_text(body_b04a),
        "Body-4",
        "occurs 0 time(s)",
        "B-04-heading-missing",
    )

    # B-04-heading-dup: duplicate the scan heading inside the section slice
    # — WR-01's m21, a `!= 1` guard narrowed to `< 1` leaves this undetected.
    # Inserted INLINE (same line, no leading blank line) rather than through
    # `_duplicate_within_range`'s blank-line-separated form: `_SCAN_HEADING`
    # itself starts with "## ", and a bare standalone copy would match
    # `_H2_RE` and get read as the section's own closing heading, truncating
    # the slice before Body-5 onward and producing a wrong-reason failure.
    _b04b_start = real_body.find(_BODY_SECTION_START)
    _b04b_end = real_body.find(_BODY_LEDGER_CLEAN, _b04b_start)
    assert _b04b_start != -1 and _b04b_end != -1
    _b04b_head, _b04b_region, _b04b_tail = (
        real_body[:_b04b_start],
        real_body[_b04b_start:_b04b_end],
        real_body[_b04b_end:],
    )
    _b04b_lit_idx = _b04b_region.find(_SCAN_HEADING)
    assert _b04b_lit_idx != -1
    _b04b_insert_at = _b04b_lit_idx + len(_SCAN_HEADING)
    body_b04b = (
        _b04b_head
        + _b04b_region[:_b04b_insert_at]
        + " "
        + _SCAN_HEADING
        + _b04b_region[_b04b_insert_at:]
        + _b04b_tail
    )
    _check_negative(
        "B-04b",
        _check_body_text(body_b04b),
        "Body-4",
        "occurs 2 time(s)",
        "B-04-heading-dup",
    )

    # B-05-cols-chain-missing: strip the chain-form column list.
    body_b05a = _strip_everywhere(real_body, _COLS_CHAIN)
    _check_negative(
        "B-05a",
        _check_body_text(body_b05a),
        "Body-5",
        "occurs 0 time(s)",
        "B-05-cols-chain-missing",
    )

    # B-05-cols-chain-dup: duplicate the chain-form column list in the slice.
    body_b05b = _duplicate_within_range(
        real_body, _BODY_SECTION_START, _BODY_LEDGER_CLEAN, _COLS_CHAIN
    )
    _check_negative(
        "B-05b",
        _check_body_text(body_b05b),
        "Body-5",
        "occurs 2 time(s)",
        "B-05-cols-chain-dup",
    )

    # B-06-cols-claim-missing: strip the claim-inventory column list.
    body_b06a = _strip_everywhere(real_body, _COLS_CLAIM)
    _check_negative(
        "B-06a",
        _check_body_text(body_b06a),
        "Body-6",
        "occurs 0 time(s)",
        "B-06-cols-claim-missing",
    )

    # B-06-cols-claim-dup: duplicate the claim-inventory column list in the slice.
    body_b06b = _duplicate_within_range(
        real_body, _BODY_SECTION_START, _BODY_LEDGER_CLEAN, _COLS_CLAIM
    )
    _check_negative(
        "B-06b",
        _check_body_text(body_b06b),
        "Body-6",
        "occurs 2 time(s)",
        "B-06-cols-claim-dup",
    )

    # B-07-rowrule-chain: strip the section-4 row-population rule.
    body_b07a = _strip_everywhere(real_body, _BODY_ROWRULE_CHAIN)
    _check_negative(
        "B-07a",
        _check_body_text(body_b07a),
        "Body-7",
        repr(_BODY_ROWRULE_CHAIN),
        "B-07-rowrule-chain",
    )

    # B-07-rowrule-claim: strip the section-6 row-population rule — WR-01's
    # m7, unasserted before this split.
    body_b07b = _strip_everywhere(real_body, _BODY_ROWRULE_CLAIM)
    _check_negative(
        "B-07b",
        _check_body_text(body_b07b),
        "Body-7",
        repr(_BODY_ROWRULE_CLAIM),
        "B-07-rowrule-claim",
    )

    # B-08-rejected: strip the non-claim-rows-populated sentence.
    body_b08 = _strip_everywhere(real_body, _BODY_REJECTED_ROW)
    _check_negative(
        "B-08", _check_body_text(body_b08), "Body-8", "missing sentence", "B-08-rejected"
    )

    # B-09-cleanpass: strip the clean-pass sentence.
    body_b09 = _strip_everywhere(real_body, _BODY_CLEANPASS)
    _check_negative(
        "B-09", _check_body_text(body_b09), "Body-9", "missing sentence", "B-09-cleanpass"
    )

    # B-10-ledger-indep-1: strip the "derive independently" half.
    body_b10a = _strip_everywhere(real_body, _BODY_LEDGER_INDEP_1)
    _check_negative(
        "B-10a",
        _check_body_text(body_b10a),
        "Body-10",
        repr(_BODY_LEDGER_INDEP_1),
        "B-10-ledger-indep-1",
    )

    # B-10-ledger-indep-2: strip the "ledger not admissible" half — WR-01's
    # m9, unasserted before this split.
    body_b10b = _strip_everywhere(real_body, _BODY_LEDGER_INDEP_2)
    _check_negative(
        "B-10b",
        _check_body_text(body_b10b),
        "Body-10",
        repr(_BODY_LEDGER_INDEP_2),
        "B-10-ledger-indep-2",
    )

    # B-11-recon-lead: strip the reconciliation lead sentence.
    body_b11a = _strip_everywhere(real_body, _BODY_RECON_LEAD)
    _check_negative(
        "B-11a",
        _check_body_text(body_b11a),
        "Body-11",
        repr(_BODY_RECON_LEAD),
        "B-11-recon-lead",
    )

    # B-11-recon-template: strip the reconciliation line's own template —
    # WR-01's m10, unasserted before this split.
    body_b11b = _strip_everywhere(real_body, _BODY_RECON_TEMPLATE)
    _check_negative(
        "B-11b",
        _check_body_text(body_b11b),
        "Body-11",
        repr(_BODY_RECON_TEMPLATE),
        "B-11-recon-template",
    )

    # B-12-placement-1: strip the first placement/provenance sentence.
    body_b12a = _strip_everywhere(real_body, _BODY_PLACEMENT_1)
    _check_negative(
        "B-12a",
        _check_body_text(body_b12a),
        "Body-12",
        repr(_BODY_PLACEMENT_1),
        "B-12-placement-1",
    )

    # B-12-placement-2: strip the second placement/provenance sentence —
    # WR-01's m8, unasserted before this split.
    body_b12b = _strip_everywhere(real_body, _BODY_PLACEMENT_2)
    _check_negative(
        "B-12b",
        _check_body_text(body_b12b),
        "Body-12",
        repr(_BODY_PLACEMENT_2),
        "B-12-placement-2",
    )

    # B-13-refix: strip the re-run-on-Fix sentence.
    body_b13 = _strip_everywhere(real_body, _BODY_REFIX)
    _check_negative(
        "B-13", _check_body_text(body_b13), "Body-13", "missing re-fix sentence", "B-13-refix"
    )

    # B-14-bound: strip the disclosed enforcement bound.
    body_b14 = _strip_everywhere(real_body, _BODY_DISCLOSED_BOUND)
    _check_negative(
        "B-14",
        _check_body_text(body_b14),
        "Body-14",
        "missing disclosed-bound sentence",
        "B-14-bound",
    )

    # B-15-donotpresent-amended: strip the amended handoff sentence.
    body_b15a = _strip_everywhere(real_body, _BODY_DONOTPRESENT_AMENDED)
    _check_negative(
        "B-15a",
        _check_body_text(body_b15a),
        "Body-15",
        "occurs 0 time(s)",
        "B-15-donotpresent-amended",
    )

    # B-15-donotpresent-preamendment: reinstate the pre-amendment form
    # ALONGSIDE the amended one (both present) — both halves of Body-15
    # are live.
    body_b15b = real_body + "\n\n" + _BODY_DONOTPRESENT_PREAMENDMENT
    _check_negative(
        "B-15b",
        _check_body_text(body_b15b),
        "Body-15",
        "pre-amendment handoff sentence still present",
        "B-15-donotpresent-preamendment",
    )

    # B-15-donotpresent-dup: duplicate the amended handoff sentence — the
    # `!= 1` count guard's OTHER direction, which the missing-direction
    # fixture above cannot exercise.
    body_b15c = _duplicate_after(
        real_body, _BODY_DONOTPRESENT_AMENDED, _BODY_DONOTPRESENT_AMENDED
    )
    _check_negative(
        "B-15c",
        _check_body_text(body_b15c),
        "Body-15",
        "occurs 2 time(s)",
        "B-15-donotpresent-dup",
    )

    # B-16-coverage-bound-missing: strip the shared table-coverage-bound
    # sentence (plan 15-07) from the section slice.
    body_b16a = _strip_everywhere(real_body, _TABLE_COVERAGE_BOUND)
    _check_negative(
        "B-16a",
        _check_body_text(body_b16a),
        "Body-16",
        "occurs 0 time(s)",
        "B-16-coverage-bound-missing",
    )

    # B-16-coverage-bound-dup: duplicate the coverage-bound sentence inside
    # the section slice.
    body_b16b = _duplicate_within_range(
        real_body, _BODY_SECTION_START, _BODY_LEDGER_CLEAN, _TABLE_COVERAGE_BOUND
    )
    _check_negative(
        "B-16b",
        _check_body_text(body_b16b),
        "Body-16",
        "occurs 2 time(s)",
        "B-16-coverage-bound-dup",
    )

    # B-17-validate-missing: strip the amended Validate step from the
    # whole file (it occurs exactly once, inside the section slice).
    body_b17a = _strip_everywhere(real_body, _BODY_VALIDATE_STEP)
    _check_negative(
        "B-17a",
        _check_body_text(body_b17a),
        "Body-17",
        "occurs 0 time(s)",
        "B-17-validate-missing",
    )

    # B-17-validate-dup: duplicate the amended Validate step inside the
    # section slice — the range extends past `_BODY_LEDGER_CLEAN` because
    # the Validate step sits in the numbered list AFTER that anchor.
    body_b17b = _duplicate_within_range(
        real_body, _BODY_SECTION_START, _BODY_DONOTPRESENT_AMENDED, _BODY_VALIDATE_STEP
    )
    _check_negative(
        "B-17b",
        _check_body_text(body_b17b),
        "Body-17",
        "occurs 2 time(s)",
        "B-17-validate-dup",
    )

    # B-17-validate-preamendment: reinstate the pre-amendment Validate
    # restriction ALONGSIDE the amended one — mirrors Body-15's shape.
    body_b17c = real_body + "\n\n" + _BODY_VALIDATE_PREAMENDMENT
    _check_negative(
        "B-17c",
        _check_body_text(body_b17c),
        "Body-17",
        "pre-amendment Validate step still present",
        "B-17-validate-preamendment",
    )

    # Hard-wrap arm 1 (body): reinstate a ledger-independence literal
    # hard-wrapped at ~95 columns, inside the section slice, and assert
    # Body-10 still passes (proves `_flat`/`_contains` are load-bearing).
    body_hw = _hardwrap_reinstate_in_range(
        real_body,
        _BODY_SECTION_START,
        _BODY_LEDGER_CLEAN,
        _BODY_LEDGER_INDEP_1,
    )
    hw_body_failures = [f for f in _check_body_text(body_hw) if f.startswith("Body-10")]
    if hw_body_failures:
        print(
            "(hw-body) hard-wrap arm: WRONGLY FAILED — Body-10 fired against a "
            f"hard-wrapped (but present) literal: {'; '.join(hw_body_failures)}"
        )
        problems.append("(hw-body): hard-wrap normalization not load-bearing")
    else:
        print("(hw-body) hard-wrap arm: PASS — Body-10 tolerates a hard-wrapped literal")

    # --- Rubric branch negative controls ------------------------------------
    # Clause-level split (plan 15-06, closing WR-01's rubric-surface rows m6,
    # m11, m12 and m20, and WR-10's early-return masking).

    # R-01-block-missing: strip the scan block heading.
    rubric_r01a = _strip_everywhere(real_rubric, _RUBRIC_SCAN_BLOCK)
    _check_negative(
        "R-01a",
        _check_rubric_text(rubric_r01a),
        "Rubric-1",
        "occurs 0 time(s)",
        "R-01-block-missing",
    )

    # R-01-block-dup: duplicate the scan block heading right after its own
    # first occurrence — the `!= 1` guard's other direction.
    rubric_r01b = _duplicate_after(real_rubric, _RUBRIC_SCAN_BLOCK, _RUBRIC_SCAN_BLOCK)
    _check_negative(
        "R-01b",
        _check_rubric_text(rubric_r01b),
        "Rubric-1",
        "occurs 2 time(s)",
        "R-01-block-dup",
    )

    # R-01-no-mask (WR-10): duplicate the scan block heading (Rubric-1 fires)
    # AND strip the Criterion 4 quoted-span sentence (Rubric-9 would fire)
    # in the SAME fixture. Before WR-10's fix, Rubric-1's early return
    # suppressed Rubric-9 here; both must now be present in one run.
    rubric_r01c = _mutate_within_range(
        real_rubric, _CRIT4_START, _CRIT5_START, _RUBRIC_QUOTED_SPAN_C4, ""
    )
    rubric_r01c = _duplicate_after(rubric_r01c, _RUBRIC_SCAN_BLOCK, _RUBRIC_SCAN_BLOCK)
    _r01c_failures = _check_rubric_text(rubric_r01c)
    _r01c_has_rubric1 = any(f.startswith("Rubric-1:") for f in _r01c_failures)
    _r01c_has_rubric9 = any(f.startswith("Rubric-9:") for f in _r01c_failures)
    if _r01c_has_rubric1 and _r01c_has_rubric9:
        print("(R-01c) correctly failed with BOTH Rubric-1 and Rubric-9 present")
        covered_branches.add("R-01-no-mask")
    else:
        print(
            "(R-01c) WRONGLY FAILED — expected BOTH Rubric-1 and Rubric-9: "
            f"rubric1={_r01c_has_rubric1}, rubric9={_r01c_has_rubric9}; "
            f"failures={_r01c_failures}"
        )
        problems.append("R-01-no-mask: early-return masking not closed")

    # R-02-placement-order: relocate the scan block past the Precedence rule
    # — the literal remains present but out of order. Violates only the
    # Precedence half (`scan_idx < precedence_idx`); the Assumption Audit
    # half still holds (`aa_idx < scan_idx`), so `expected_detail` targets
    # the Precedence half's own token to keep this arm from being satisfied
    # by the Assumption Audit half's distinct message.
    rubric_r02a = _relocate(real_rubric, _RUBRIC_SCAN_BLOCK, _RUBRIC_PRECEDENCE)
    _check_negative(
        "R-02a",
        _check_rubric_text(rubric_r02a),
        "Rubric-2",
        "Precedence half",
        "R-02-placement-order",
    )

    # R-02-placement-anchor: strip the Assumption Audit block, so the
    # not-found guard (`aa_idx == -1`) fires instead of the placement check.
    rubric_r02b = _strip_everywhere(real_rubric, _RUBRIC_AA_BLOCK)
    _check_negative(
        "R-02b",
        _check_rubric_text(rubric_r02b),
        "Rubric-2",
        repr(_RUBRIC_AA_BLOCK) + " not found",
        "R-02-placement-anchor",
    )

    # R-02-placement-aa (15-VERIFICATION.md gap 2, SCAN-03, reproduced live):
    # relocate the scan block heading to BEFORE the Assumption Audit block
    # — the scan block heading remains PRESENT but now sits before the
    # Assumption Audit block, which is what proves this arm is a placement
    # check and not a disguised presence check. Narrowing the combined
    # predicate to `scan_idx < precedence_idx` previously left `--self-test`
    # at rc=0 reporting all branches covered against exactly this
    # malformation. Violates only the Assumption Audit half.
    rubric_r02c = _relocate(real_rubric, _RUBRIC_SCAN_BLOCK, "## How to Apply This Gate")
    _r02c_failures = _check_rubric_text(rubric_r02c)
    _r02c_ids = sorted({f.split(" ", 1)[0].rstrip(":") for f in _r02c_failures})
    print(f"(R-02c) failure list check IDs: {_r02c_ids}")
    if _r02c_ids != ["Rubric-2"]:
        print(
            "(R-02c) co-firing detected — sibling check(s) fired alongside "
            f"Rubric-2 in the widened scan slice: {_r02c_ids}"
        )
    _check_negative(
        "R-02c",
        _r02c_failures,
        "Rubric-2",
        "Assumption Audit half",
        "R-02-placement-aa",
    )

    # R-03-divlabour-1: strip the first division-of-labour sentence.
    rubric_r03a = _mutate_within_range(
        real_rubric, _RUBRIC_SCAN_BLOCK, _RUBRIC_PRECEDENCE, _RUBRIC_DIVLABOUR_1, ""
    )
    _check_negative(
        "R-03a",
        _check_rubric_text(rubric_r03a),
        "Rubric-3",
        repr(_RUBRIC_DIVLABOUR_1),
        "R-03-divlabour-1",
    )

    # R-03-divlabour-2: strip the second division-of-labour sentence —
    # WR-01's m11, unasserted before this split.
    rubric_r03b = _mutate_within_range(
        real_rubric, _RUBRIC_SCAN_BLOCK, _RUBRIC_PRECEDENCE, _RUBRIC_DIVLABOUR_2, ""
    )
    _check_negative(
        "R-03b",
        _check_rubric_text(rubric_r03b),
        "Rubric-3",
        repr(_RUBRIC_DIVLABOUR_2),
        "R-03-divlabour-2",
    )

    # R-04-two-criteria: strip the two-criteria pointer sentence. WR-09's
    # information-free name loop was deleted from `_check_rubric_text`
    # rather than kept as an unfalsifiable arm — see the comment at its
    # former call site. This presence check is the real, falsifiable one.
    rubric_r04 = _mutate_within_range(
        real_rubric, _RUBRIC_SCAN_BLOCK, _RUBRIC_PRECEDENCE, _RUBRIC_TWO_CRIT_SENTENCE, ""
    )
    _check_negative(
        "R-04",
        _check_rubric_text(rubric_r04),
        "Rubric-4",
        "missing two-criteria pointer sentence",
        "R-04-two-criteria",
    )

    # R-05-cols-chain: strip the chain-form column list from the scan slice.
    rubric_r05a = _mutate_within_range(
        real_rubric, _RUBRIC_SCAN_BLOCK, _RUBRIC_PRECEDENCE, _COLS_CHAIN, ""
    )
    _check_negative(
        "R-05a",
        _check_rubric_text(rubric_r05a),
        "Rubric-5",
        repr(_COLS_CHAIN),
        "R-05-cols-chain",
    )

    # R-05-cols-claim: strip the claim-inventory column list from the scan
    # slice — WR-01's m12, unasserted before this split.
    rubric_r05b = _mutate_within_range(
        real_rubric, _RUBRIC_SCAN_BLOCK, _RUBRIC_PRECEDENCE, _COLS_CLAIM, ""
    )
    _check_negative(
        "R-05b",
        _check_rubric_text(rubric_r05b),
        "Rubric-5",
        repr(_COLS_CLAIM),
        "R-05-cols-claim",
    )

    # R-06-ledger: strip the ledger non-admissibility sentence.
    rubric_r06 = _mutate_within_range(
        real_rubric,
        _RUBRIC_SCAN_BLOCK,
        _RUBRIC_PRECEDENCE,
        _RUBRIC_LEDGER_INADMISSIBLE,
        "",
    )
    _check_negative(
        "R-06",
        _check_rubric_text(rubric_r06),
        "Rubric-6",
        "missing ledger non-admissibility sentence",
        "R-06-ledger",
    )

    # R-07-missing-absent: strip the missing-scan sentence from the scan slice.
    rubric_r07a = _mutate_within_range(
        real_rubric, _RUBRIC_SCAN_BLOCK, _RUBRIC_PRECEDENCE, _RUBRIC_MISSING_SCAN, ""
    )
    _check_negative(
        "R-07a",
        _check_rubric_text(rubric_r07a),
        "Rubric-7",
        "missing-scan sentence absent",
        "R-07-missing-absent",
    )

    # R-07-missing-neartwin: inject the Assumption-Audit near-twin into the
    # scan slice, proving the check discriminates the two.
    rubric_r07b = _mutate_within_range(
        real_rubric,
        _RUBRIC_SCAN_BLOCK,
        _RUBRIC_PRECEDENCE,
        _RUBRIC_MISSING_SCAN,
        _RUBRIC_MISSING_SCAN + " " + _RUBRIC_MISSING_SCAN_NEARTWIN,
    )
    _check_negative(
        "R-07b",
        _check_rubric_text(rubric_r07b),
        "Rubric-7",
        "near-twin sentence found inside scan slice",
        "R-07-missing-neartwin",
    )

    # R-08-bound: strip the disclosed-bound sentence.
    rubric_r08 = _mutate_within_range(
        real_rubric, _RUBRIC_SCAN_BLOCK, _RUBRIC_PRECEDENCE, _RUBRIC_DISCLOSED_BOUND, ""
    )
    _check_negative(
        "R-08",
        _check_rubric_text(rubric_r08),
        "Rubric-8",
        "missing disclosed-bound sentence",
        "R-08-bound",
    )

    # R-09-crit4-count-missing: strip the Criterion 4 quoted-span sentence.
    rubric_r09a = _mutate_within_range(
        real_rubric, _CRIT4_START, _CRIT5_START, _RUBRIC_QUOTED_SPAN_C4, ""
    )
    _check_negative(
        "R-09a",
        _check_rubric_text(rubric_r09a),
        "Rubric-9",
        "occurs 0 time(s)",
        "R-09-crit4-count-missing",
    )

    # R-09-crit4-count-dup: duplicate the Criterion 4 quoted-span sentence
    # inside the Criterion 4 slice — WR-01's m20 (`!= 1` narrowed to `< 1`
    # leaves this undetected).
    rubric_r09b = _duplicate_within_range(
        real_rubric, _CRIT4_START, _CRIT5_START, _RUBRIC_QUOTED_SPAN_C4
    )
    _check_negative(
        "R-09b",
        _check_rubric_text(rubric_r09b),
        "Rubric-9",
        "occurs 2 time(s)",
        "R-09-crit4-count-dup",
    )

    # R-09-crit4-order: wrap AND relocate the Criterion 4 quoted-span
    # sentence after the Rigorous band bullet — CR-01's exact malformation
    # (`15-REVIEW.md`), which a strip-only control cannot see.
    rubric_r09c = _hardwrap_relocate_in_range(
        real_rubric, _CRIT4_START, _CRIT5_START, _RUBRIC_QUOTED_SPAN_C4, _BAND_RIGOROUS
    )
    _check_negative(
        "R-09c",
        _check_rubric_text(rubric_r09c),
        "Rubric-9",
        "does not precede the Rigorous band bullet",
        "R-09-crit4-order",
    )

    # R-09-crit4-direct-missing: strip the Criterion 4 direct-quotation half
    # (plan 15-07, closing CR-03) from the Criterion 4 slice.
    rubric_r09d = _mutate_within_range(
        real_rubric, _CRIT4_START, _CRIT5_START, _RUBRIC_QUOTED_SPAN_C4_DIRECT, ""
    )
    _check_negative(
        "R-09d",
        _check_rubric_text(rubric_r09d),
        "Rubric-9",
        "direct-quotation half occurs 0 time(s)",
        "R-09-crit4-direct-missing",
    )

    # R-09-crit4-direct-dup: duplicate the Criterion 4 direct-quotation half
    # inside the Criterion 4 slice — the `!= 1` guard's other direction,
    # provably not a re-run of the strip control above (different
    # expected_detail: "occurs 2" versus "occurs 0").
    rubric_r09e = _duplicate_within_range(
        real_rubric, _CRIT4_START, _CRIT5_START, _RUBRIC_QUOTED_SPAN_C4_DIRECT
    )
    _check_negative(
        "R-09e",
        _check_rubric_text(rubric_r09e),
        "Rubric-9",
        "direct-quotation half occurs 2 time(s)",
        "R-09-crit4-direct-dup",
    )

    # R-10-crit6-count-missing: strip the Criterion 6 quoted-span sentence.
    rubric_r10a = _mutate_within_range(
        real_rubric, _CRIT6_START, _USAGE_NOTE, _RUBRIC_QUOTED_SPAN_C6, ""
    )
    _check_negative(
        "R-10a",
        _check_rubric_text(rubric_r10a),
        "Rubric-10",
        "occurs 0 time(s)",
        "R-10-crit6-count-missing",
    )

    # R-10-crit6-count-dup: duplicate the Criterion 6 quoted-span sentence
    # inside the Criterion 6 slice.
    rubric_r10b = _duplicate_within_range(
        real_rubric, _CRIT6_START, _USAGE_NOTE, _RUBRIC_QUOTED_SPAN_C6
    )
    _check_negative(
        "R-10b",
        _check_rubric_text(rubric_r10b),
        "Rubric-10",
        "occurs 2 time(s)",
        "R-10-crit6-count-dup",
    )

    # R-10-crit6-order: wrap AND relocate the Criterion 6 quoted-span
    # sentence after the Rigorous band bullet — CR-01's exact malformation
    # (`15-REVIEW.md`), which a strip-only control cannot see.
    rubric_r10c = _hardwrap_relocate_in_range(
        real_rubric, _CRIT6_START, _USAGE_NOTE, _RUBRIC_QUOTED_SPAN_C6, _BAND_RIGOROUS
    )
    _check_negative(
        "R-10c",
        _check_rubric_text(rubric_r10c),
        "Rubric-10",
        "does not precede the Rigorous band bullet",
        "R-10-crit6-order",
    )

    # R-10-crit6-direct-missing: strip the Criterion 6 direct-quotation half
    # (plan 15-07, closing CR-03) from the Criterion 6 slice.
    rubric_r10d = _mutate_within_range(
        real_rubric, _CRIT6_START, _USAGE_NOTE, _RUBRIC_QUOTED_SPAN_C6_DIRECT, ""
    )
    _check_negative(
        "R-10d",
        _check_rubric_text(rubric_r10d),
        "Rubric-10",
        "direct-quotation half occurs 0 time(s)",
        "R-10-crit6-direct-missing",
    )

    # R-10-crit6-direct-dup: duplicate the Criterion 6 direct-quotation half
    # inside the Criterion 6 slice.
    rubric_r10e = _duplicate_within_range(
        real_rubric, _CRIT6_START, _USAGE_NOTE, _RUBRIC_QUOTED_SPAN_C6_DIRECT
    )
    _check_negative(
        "R-10e",
        _check_rubric_text(rubric_r10e),
        "Rubric-10",
        "direct-quotation half occurs 2 time(s)",
        "R-10-crit6-direct-dup",
    )

    # R-11-bands-crit4-<band>/R-11-bands-crit6-<band> (plan 15-12, closing
    # `15-VERIFICATION.md`'s WR-01 gap): one strip-arm and one dup-arm per
    # `_BAND_BULLETS` literal, driven from the tuple ITSELF via a plain
    # `zip` over `_BAND_BULLETS` and `_BAND_NAMES` rather than a hand-written
    # four-literal list — deliberately NOT `strict=True`: that would turn
    # a length-mismatched pair into a loud `ValueError` instead of a
    # silently-uncovered branch, which makes the LENGTHENING direction
    # fail-open (see bound (11) above). The verifier reproduced live that
    # narrowing `_BAND_BULLETS` from four
    # literals to one (`(_BAND_SOUND,)`) left `--self-test` at rc=0
    # reporting "All 94 branches covered", because the prior R-11a/R-11b
    # controls this loop replaces exercised `_BAND_SOUND` only — the other
    # three literals had no arm in either criterion slice. Each of the
    # eight controls below carries an `expected_detail` naming its own
    # bullet's `repr()` and slice, so the eight are mutually discriminating
    # (no one control's failure message can satisfy a sibling's
    # expectation) rather than all satisfiable by any single `Rubric-11`
    # message. Mirrors R-11a's strip idiom for the Criterion 4 arms and
    # R-11b's duplicate idiom for the Criterion 6 arms, so both mutation
    # directions stay represented per literal.
    for _band_bullet, _band_name in zip(_BAND_BULLETS, _BAND_NAMES):
        rubric_r11_crit4 = _mutate_within_range(
            real_rubric, _CRIT4_START, _CRIT5_START, _band_bullet, "REMOVED"
        )
        _check_negative(
            f"R-11-{_band_name}-crit4",
            _check_rubric_text(rubric_r11_crit4),
            "Rubric-11",
            f"{_band_bullet!r} occurs 0 time(s) in Criterion 4 slice",
            f"R-11-bands-crit4-{_band_name}",
        )

        rubric_r11_crit6 = _mutate_within_range(
            real_rubric,
            _CRIT6_START,
            _USAGE_NOTE,
            _band_bullet,
            _band_bullet + "\n" + _band_bullet,
        )
        _check_negative(
            f"R-11-{_band_name}-crit6",
            _check_rubric_text(rubric_r11_crit6),
            "Rubric-11",
            f"{_band_bullet!r} occurs 2 time(s) in Criterion 6 slice",
            f"R-11-bands-crit6-{_band_name}",
        )

    # R-12-halt-missing: strip the halt sentence from inside the scan slice
    # only, leaving the Assumption Audit block's identical copy in place —
    # whole-file count drops 2 -> 1, only a slice-scoped check sees it.
    rubric_r12a = _mutate_within_range(
        real_rubric, _RUBRIC_SCAN_BLOCK, _RUBRIC_PRECEDENCE, _RUBRIC_HALT_SENTENCE, ""
    )
    _check_negative(
        "R-12a",
        _check_rubric_text(rubric_r12a),
        "Rubric-12",
        "occurs 0 time(s)",
        "R-12-halt-missing",
    )

    # R-12-halt-dup: duplicate the halt sentence inside the scan slice.
    rubric_r12b = _mutate_within_range(
        real_rubric,
        _RUBRIC_SCAN_BLOCK,
        _RUBRIC_PRECEDENCE,
        _RUBRIC_HALT_SENTENCE,
        _RUBRIC_HALT_SENTENCE + " " + _RUBRIC_HALT_SENTENCE,
    )
    _check_negative(
        "R-12b",
        _check_rubric_text(rubric_r12b),
        "Rubric-12",
        "occurs 2 time(s)",
        "R-12-halt-dup",
    )

    # --- Rubric-13 branch negative controls (plan 15-07, closing CR-02) ----
    # The Verdict Block Format amendment: the amended quoted-span template
    # and the admission-sentence pair, each split missing/dup, plus the
    # count-0 pre-amendment-reinstatement arm and the ordering arm.

    # R-13-format-amended-missing: strip the amended quoted-span template
    # from the Verdict Block Format section.
    rubric_r13a = _mutate_within_range(
        real_rubric,
        _RUBRIC_FORMAT_START,
        _RUBRIC_CRITERIA_START,
        _RUBRIC_FORMAT_QUOTED_SPAN,
        "",
    )
    _check_negative(
        "R-13a",
        _check_rubric_text(rubric_r13a),
        "Rubric-13",
        "amended quoted-span template occurs 0 time(s)",
        "R-13-format-amended-missing",
    )

    # R-13-format-amended-dup: duplicate the amended quoted-span template
    # inside the same section.
    rubric_r13b = _duplicate_within_range(
        real_rubric,
        _RUBRIC_FORMAT_START,
        _RUBRIC_CRITERIA_START,
        _RUBRIC_FORMAT_QUOTED_SPAN,
    )
    _check_negative(
        "R-13b",
        _check_rubric_text(rubric_r13b),
        "Rubric-13",
        "amended quoted-span template occurs 2 time(s)",
        "R-13-format-amended-dup",
    )

    # R-13-format-admission-missing: strip the admission sentence.
    rubric_r13c = _mutate_within_range(
        real_rubric,
        _RUBRIC_FORMAT_START,
        _RUBRIC_CRITERIA_START,
        _RUBRIC_FORMAT_ADMISSION,
        "",
    )
    _check_negative(
        "R-13c",
        _check_rubric_text(rubric_r13c),
        "Rubric-13",
        "admission sentence occurs 0 time(s)",
        "R-13-format-admission-missing",
    )

    # R-13-format-admission-dup: duplicate the admission sentence inside the
    # same section.
    rubric_r13d = _duplicate_within_range(
        real_rubric,
        _RUBRIC_FORMAT_START,
        _RUBRIC_CRITERIA_START,
        _RUBRIC_FORMAT_ADMISSION,
    )
    _check_negative(
        "R-13d",
        _check_rubric_text(rubric_r13d),
        "Rubric-13",
        "admission sentence occurs 2 time(s)",
        "R-13-format-admission-dup",
    )

    # R-13-format-preamendment: reinstate the pre-amendment quoted-span
    # template ALONGSIDE the amended one (both present) — the amendment
    # cannot be silently reverted by addition, mirroring Body-15's shape.
    rubric_r13e = real_rubric + "\n\n" + _RUBRIC_FORMAT_PREAMENDMENT
    _check_negative(
        "R-13e",
        _check_rubric_text(rubric_r13e),
        "Rubric-13",
        "pre-amendment quoted-span template still present",
        "R-13-format-preamendment",
    )

    # R-13-format-order: relocate the admission sentence to immediately
    # after the Criterion 4 heading — the literal remains present but out
    # of order relative to it.
    rubric_r13f = _relocate(real_rubric, _RUBRIC_FORMAT_ADMISSION, _CRIT4_START)
    _check_negative(
        "R-13f",
        _check_rubric_text(rubric_r13f),
        "Rubric-13",
        "does not precede the Criterion 4 heading",
        "R-13-format-order",
    )

    # --- Rubric-13/14 branch negative controls (plan 15-08, closing CR-01) -
    # The widened admission's two clauses, split missing/dup, the superseded
    # 15-07 clause's count-0 guard, and the Criterion 2 descriptor pin the
    # admission's C2 clause depends on.
    #
    # Re-pointed at plan 15-11 (SCAN-02, region split): these four arms now
    # mutate the ADMISSION region only — [_RUBRIC_FORMAT_ADMISSION,
    # _RUBRIC_CRITERIA_START) — rather than the whole Verdict Block Format
    # section, because the TEMPLATE now also states both clauses (task 1
    # widened it), so the whole-section count is 2 and a mutation scoped to
    # the whole section would trip `_mutate_within_range`'s own `count == 1`
    # assertion. Scoping to the admission sentence's own span leaves the
    # TEMPLATE-region arms below (R-13-format-template-*) untouched, which is
    # the split's whole point: each region is independently falsifiable.

    # R-13-format-admission-c46-missing: strip the Criteria-4/6 clause from
    # inside the ADMISSION region only.
    rubric_r13g = _mutate_within_range(
        real_rubric,
        _RUBRIC_FORMAT_ADMISSION,
        _RUBRIC_CRITERIA_START,
        _ADMISSION_SCOPE_C46,
        "",
    )
    _check_negative(
        "R-13g",
        _check_rubric_text(rubric_r13g),
        "Rubric-13",
        "Criteria-4/6 clause occurs 0 time(s) in the Verdict Block Format ADMISSION region",
        "R-13-format-admission-c46-missing",
    )

    # R-13-format-admission-c46-dup: duplicate the Criteria-4/6 clause
    # inside the same ADMISSION region.
    rubric_r13h = _duplicate_within_range(
        real_rubric, _RUBRIC_FORMAT_ADMISSION, _RUBRIC_CRITERIA_START, _ADMISSION_SCOPE_C46
    )
    _check_negative(
        "R-13h",
        _check_rubric_text(rubric_r13h),
        "Rubric-13",
        "Criteria-4/6 clause occurs 2 time(s) in the Verdict Block Format ADMISSION region",
        "R-13-format-admission-c46-dup",
    )

    # R-13-format-admission-c2-missing: strip the Criterion-2 clause from
    # inside the ADMISSION region only.
    rubric_r13i = _mutate_within_range(
        real_rubric,
        _RUBRIC_FORMAT_ADMISSION,
        _RUBRIC_CRITERIA_START,
        _ADMISSION_SCOPE_C2,
        "",
    )
    _check_negative(
        "R-13i",
        _check_rubric_text(rubric_r13i),
        "Rubric-13",
        "Criterion-2 clause occurs 0 time(s) in the Verdict Block Format ADMISSION region",
        "R-13-format-admission-c2-missing",
    )

    # R-13-format-admission-c2-dup: duplicate the Criterion-2 clause inside
    # the same ADMISSION region — the `!= 1` guard's OTHER direction.
    rubric_r13j = _duplicate_within_range(
        real_rubric, _RUBRIC_FORMAT_ADMISSION, _RUBRIC_CRITERIA_START, _ADMISSION_SCOPE_C2
    )
    _check_negative(
        "R-13j",
        _check_rubric_text(rubric_r13j),
        "Rubric-13",
        "Criterion-2 clause occurs 2 time(s) in the Verdict Block Format ADMISSION region",
        "R-13-format-admission-c2-dup",
    )

    # R-13-format-admission-superseded: reinstate the 15-07 absolute clause
    # verbatim somewhere in the rubric text, so the whole-file count-0
    # guard fires — mirrors R-13-format-preamendment's shape.
    rubric_r13k = real_rubric + "\n\n" + _RUBRIC_FORMAT_ADMISSION_SUPERSEDED
    _check_negative(
        "R-13k",
        _check_rubric_text(rubric_r13k),
        "Rubric-13",
        "superseded 'sole place' clause still present",
        "R-13-format-admission-superseded",
    )

    # --- Rubric-13 TEMPLATE-region branch negative controls (plan 15-11,
    # closing SCAN-02) --------------------------------------------------
    # The region split's other half: the same two clauses, now asserted
    # independently inside the TEMPLATE region — [_RUBRIC_FORMAT_START,
    # _RUBRIC_FORMAT_ADMISSION) — which task 1 widened to state both
    # clauses. A mutation here must leave the ADMISSION-region arms above
    # silent, and vice versa; that mutual silence is the proof the split is
    # real rather than one guard renamed twice.

    # R-13-format-template-c46-missing: strip the Criteria-4/6 clause from
    # inside the TEMPLATE region only.
    rubric_r13l = _mutate_within_range(
        real_rubric,
        _RUBRIC_FORMAT_START,
        _RUBRIC_FORMAT_ADMISSION,
        _ADMISSION_SCOPE_C46,
        "",
    )
    _check_negative(
        "R-13l",
        _check_rubric_text(rubric_r13l),
        "Rubric-13",
        "Criteria-4/6 clause occurs 0 time(s) in the Verdict Block Format TEMPLATE region",
        "R-13-format-template-c46-missing",
    )

    # R-13-format-template-c46-dup: duplicate the Criteria-4/6 clause inside
    # the same TEMPLATE region.
    rubric_r13m = _duplicate_within_range(
        real_rubric, _RUBRIC_FORMAT_START, _RUBRIC_FORMAT_ADMISSION, _ADMISSION_SCOPE_C46
    )
    _check_negative(
        "R-13m",
        _check_rubric_text(rubric_r13m),
        "Rubric-13",
        "Criteria-4/6 clause occurs 2 time(s) in the Verdict Block Format TEMPLATE region",
        "R-13-format-template-c46-dup",
    )

    # R-13-format-template-c2-missing: strip the Criterion-2 clause from
    # inside the TEMPLATE region only.
    rubric_r13n = _mutate_within_range(
        real_rubric,
        _RUBRIC_FORMAT_START,
        _RUBRIC_FORMAT_ADMISSION,
        _ADMISSION_SCOPE_C2,
        "",
    )
    _check_negative(
        "R-13n",
        _check_rubric_text(rubric_r13n),
        "Rubric-13",
        "Criterion-2 clause occurs 0 time(s) in the Verdict Block Format TEMPLATE region",
        "R-13-format-template-c2-missing",
    )

    # R-13-format-template-c2-dup: duplicate the Criterion-2 clause inside
    # the same TEMPLATE region — the `!= 1` guard's OTHER direction.
    rubric_r13o = _duplicate_within_range(
        real_rubric, _RUBRIC_FORMAT_START, _RUBRIC_FORMAT_ADMISSION, _ADMISSION_SCOPE_C2
    )
    _check_negative(
        "R-13o",
        _check_rubric_text(rubric_r13o),
        "Rubric-13",
        "Criterion-2 clause occurs 2 time(s) in the Verdict Block Format TEMPLATE region",
        "R-13-format-template-c2-dup",
    )

    # R-13-format-quoted-span-superseded: reinstate the pre-15-11 narrow
    # quoted-span wording verbatim somewhere in the rubric text, so the
    # whole-file count-0 guard fires — mirrors R-13-format-admission-
    # superseded's shape for the template's own superseded literal.
    rubric_r13p = real_rubric + "\n\n" + _RUBRIC_FORMAT_QUOTED_SPAN_SUPERSEDED
    _check_negative(
        "R-13p",
        _check_rubric_text(rubric_r13p),
        "Rubric-13",
        "superseded narrow quoted-span wording still present",
        "R-13-format-quoted-span-superseded",
    )

    # R-14-c2-descriptor-missing: strip the Assumption Audit artifact
    # descriptor sentence from Criterion 2's slice. Uses the `_flat`
    # helper, not `_mutate_within_range` — the descriptor is hard-wrapped
    # in the shipped source (it is NOT unwrapped, per the binding
    # constraint that Criterion 2's Rigorous descriptor stays exactly as
    # it is), so a raw-substring fixture would find zero occurrences.
    rubric_r14a = _mutate_within_range_flat(
        real_rubric, _CRIT2_START, _CRIT3_START, _RUBRIC_C2_AA_ARTIFACT, ""
    )
    _check_negative(
        "R-14a",
        _check_rubric_text(rubric_r14a),
        "Rubric-14",
        "occurs 0 time(s)",
        "R-14-c2-descriptor-missing",
    )

    # R-14-c2-descriptor-dup: duplicate the descriptor sentence inside the
    # same slice — inserts an UNWRAPPED second copy after the wrapped one,
    # so the slice's flat-normalized count goes to 2.
    rubric_r14b = _duplicate_within_range_flat(
        real_rubric, _CRIT2_START, _CRIT3_START, _RUBRIC_C2_AA_ARTIFACT
    )
    _check_negative(
        "R-14b",
        _check_rubric_text(rubric_r14b),
        "Rubric-14",
        "occurs 2 time(s)",
        "R-14-c2-descriptor-dup",
    )

    # Hard-wrap arm 2 (rubric): reinstate the ledger non-admissibility
    # sentence hard-wrapped at ~95 columns, inside the scan slice, and assert
    # Rubric-6 still passes.
    rubric_hw = _hardwrap_reinstate_in_range(
        real_rubric, _RUBRIC_SCAN_BLOCK, _RUBRIC_PRECEDENCE, _RUBRIC_LEDGER_INADMISSIBLE
    )
    hw_rubric_failures = [f for f in _check_rubric_text(rubric_hw) if f.startswith("Rubric-6")]
    if hw_rubric_failures:
        print(
            "(hw-rubric) hard-wrap arm: WRONGLY FAILED — Rubric-6 fired against a "
            f"hard-wrapped (but present) literal: {'; '.join(hw_rubric_failures)}"
        )
        problems.append("(hw-rubric): hard-wrap normalization not load-bearing")
    else:
        print("(hw-rubric) hard-wrap arm: PASS — Rubric-6 tolerates a hard-wrapped literal")

    # --- Cross-surface branch negative controls -----------------------------

    # Clause-level split (plan 15-06, closing WR-01's cross-surface rows m3,
    # m4 and m17): `_check_cross_surface` carries four arms inside its
    # column-list loop (chain/claim x body/rubric) plus two heading arms
    # (body/rubric) — each gets its own id and its own single-surface strip.

    # X-01-cols-chain-body: strip the chain-form column list from the body
    # ONLY, leaving the rubric intact.
    body_x01a = _strip_everywhere(real_body, _COLS_CHAIN)
    _check_negative(
        "X-01a",
        _check_cross_surface(body_x01a, real_rubric),
        "Cross-1",
        "chain-form column list missing from agent-body surface",
        "X-01-cols-chain-body",
    )

    # X-01-cols-chain-rubric: strip the chain-form column list from the
    # rubric ONLY, leaving the body intact — WR-01's m3.
    rubric_x01b = _strip_everywhere(real_rubric, _COLS_CHAIN)
    _check_negative(
        "X-01b",
        _check_cross_surface(real_body, rubric_x01b),
        "Cross-1",
        "chain-form column list missing from rubric surface",
        "X-01-cols-chain-rubric",
    )

    # X-01-cols-claim-body: strip the claim-inventory column list from the
    # body ONLY — WR-01's m17.
    body_x01c = _strip_everywhere(real_body, _COLS_CLAIM)
    _check_negative(
        "X-01c",
        _check_cross_surface(body_x01c, real_rubric),
        "Cross-1",
        "claim-inventory column list missing from agent-body surface",
        "X-01-cols-claim-body",
    )

    # X-01-cols-claim-rubric: strip the claim-inventory column list from the
    # rubric ONLY.
    rubric_x01d = _strip_everywhere(real_rubric, _COLS_CLAIM)
    _check_negative(
        "X-01d",
        _check_cross_surface(real_body, rubric_x01d),
        "Cross-1",
        "claim-inventory column list missing from rubric surface",
        "X-01-cols-claim-rubric",
    )

    # X-02-heading-body: strip the scan heading from the body ONLY, leaving
    # the rubric intact — WR-01's m4.
    body_x02a = _strip_everywhere(real_body, _SCAN_HEADING)
    _check_negative(
        "X-02a",
        _check_cross_surface(body_x02a, real_rubric),
        "Cross-2",
        "missing from agent-body surface",
        "X-02-heading-body",
    )

    # X-02-heading-rubric: strip the scan heading from the rubric ONLY,
    # leaving the body intact.
    rubric_x02b = _strip_everywhere(real_rubric, _SCAN_HEADING)
    _check_negative(
        "X-02b",
        _check_cross_surface(real_body, rubric_x02b),
        "Cross-2",
        "missing from rubric surface",
        "X-02-heading-rubric",
    )

    # X-03-bound-body: strip the shared table-coverage-bound sentence
    # (plan 15-07) from the body ONLY, leaving the rubric intact.
    body_x03a = _strip_everywhere(real_body, _TABLE_COVERAGE_BOUND)
    _check_negative(
        "X-03a",
        _check_cross_surface(body_x03a, real_rubric),
        "Cross-3",
        "missing from agent-body surface",
        "X-03-bound-body",
    )

    # X-03-bound-rubric: strip the coverage-bound sentence from the rubric
    # ONLY, leaving the body intact.
    rubric_x03b = _strip_everywhere(real_rubric, _TABLE_COVERAGE_BOUND)
    _check_negative(
        "X-03b",
        _check_cross_surface(real_body, rubric_x03b),
        "Cross-3",
        "missing from rubric surface",
        "X-03-bound-rubric",
    )

    # X-04-admission-c46-body: strip the Criteria-4/6 admission clause from
    # the body ONLY, leaving the rubric intact.
    body_x04a = _strip_everywhere(real_body, _ADMISSION_SCOPE_C46)
    _check_negative(
        "X-04a",
        _check_cross_surface(body_x04a, real_rubric),
        "Cross-4",
        "Criteria-4/6 admission clause missing from agent-body surface",
        "X-04-admission-c46-body",
    )

    # X-04-admission-c46-rubric: strip the Criteria-4/6 admission clause
    # from the rubric ONLY, leaving the body intact.
    rubric_x04b = _strip_everywhere(real_rubric, _ADMISSION_SCOPE_C46)
    _check_negative(
        "X-04b",
        _check_cross_surface(real_body, rubric_x04b),
        "Cross-4",
        "Criteria-4/6 admission clause missing from rubric surface",
        "X-04-admission-c46-rubric",
    )

    # X-04-admission-c2-body: strip the Criterion-2 admission clause from
    # the body ONLY, leaving the rubric intact.
    body_x04c = _strip_everywhere(real_body, _ADMISSION_SCOPE_C2)
    _check_negative(
        "X-04c",
        _check_cross_surface(body_x04c, real_rubric),
        "Cross-4",
        "Criterion-2 admission clause missing from agent-body surface",
        "X-04-admission-c2-body",
    )

    # X-04-admission-c2-rubric: strip the Criterion-2 admission clause from
    # the rubric ONLY, leaving the body intact.
    rubric_x04d = _strip_everywhere(real_rubric, _ADMISSION_SCOPE_C2)
    _check_negative(
        "X-04d",
        _check_cross_surface(real_body, rubric_x04d),
        "Cross-4",
        "Criterion-2 admission clause missing from rubric surface",
        "X-04-admission-c2-rubric",
    )

    # X-05-superseded-body: reinstate the pre-15-11 narrow quoted-span
    # wording in the body ONLY, leaving the rubric intact — the mirror
    # image of X-04's missing-clause arms, since Cross-5 is a PRESENCE
    # guard rather than an absence guard.
    body_x05a = real_body + "\n\n" + _RUBRIC_FORMAT_QUOTED_SPAN_SUPERSEDED
    _check_negative(
        "X-05a",
        _check_cross_surface(body_x05a, real_rubric),
        "Cross-5",
        "superseded narrow quoted-span wording present in agent-body surface",
        "X-05-superseded-body",
    )

    # X-05-superseded-rubric: reinstate the pre-15-11 narrow quoted-span
    # wording in the rubric ONLY, leaving the body intact.
    rubric_x05b = real_rubric + "\n\n" + _RUBRIC_FORMAT_QUOTED_SPAN_SUPERSEDED
    _check_negative(
        "X-05b",
        _check_cross_surface(real_body, rubric_x05b),
        "Cross-5",
        "superseded narrow quoted-span wording present in rubric surface",
        "X-05-superseded-rubric",
    )

    # THE FLOOR ITSELF (WR-02, `15-REVIEW.md`): roster-equality plus
    # coverage-subset, routed through `_roster_problems` so the isolation
    # arms below drive the exact code path this real call uses.
    executed.append("roster-lock")
    roster_real_problems = _roster_problems(
        REQUIRED_BRANCHES, _BRANCH_ROSTER_LOCK, frozenset(covered_branches)
    )
    if roster_real_problems:
        for roster_msg in roster_real_problems:
            print(f"(roster-lock) {roster_msg}")
        problems.extend(roster_real_problems)
    else:
        print(
            "(roster-lock) ROSTER LOCK: PASS — REQUIRED_BRANCHES == "
            "_BRANCH_ROSTER_LOCK and covered_branches has no unregistered "
            "branch id(s)"
        )

    # ISOLATION arms for `_roster_problems` itself, mirroring
    # `check-quality-harness.py`'s (x) ISOLATION shape: drive the pure
    # helper with SYNTHETIC id sets only — never `REQUIRED_BRANCHES`, never
    # `_BRANCH_ROSTER_LOCK` — so the comparison logic is proven correct
    # independently of whether the two real registries happen to agree today.
    roster_x1 = _roster_problems(frozenset({"A", "B"}), frozenset({"A", "B"}), frozenset({"A"}))
    if roster_x1 != []:
        print(f"(roster-x1) ISOLATION CLEAN: WRONGLY reported problem(s): {roster_x1}")
        problems.append(f"(roster-x1): clean case wrongly reported {roster_x1}")
    else:
        print("(roster-x1) ISOLATION CLEAN: PASS")

    roster_x2 = _roster_problems(frozenset({"A"}), frozenset({"A", "B"}), frozenset({"A"}))
    if not (len(roster_x2) == 1 and "B" in roster_x2[0] and "ROSTER LOCK:" in roster_x2[0]):
        print(f"(roster-x2) ISOLATION NARROWED: expected one problem naming 'B', got {roster_x2}")
        problems.append(f"(roster-x2): narrowed case did not name missing id 'B': {roster_x2}")
    else:
        print(f"(roster-x2) ISOLATION NARROWED: PASS ({roster_x2[0]})")

    roster_x3 = _roster_problems(
        frozenset({"A", "B"}), frozenset({"A", "B"}), frozenset({"A", "B", "C"})
    )
    if not (len(roster_x3) == 1 and "C" in roster_x3[0] and "unregistered" in roster_x3[0]):
        print(f"(roster-x3) ISOLATION EXTRA: expected one problem naming 'C', got {roster_x3}")
        problems.append(f"(roster-x3): extra case did not name surplus id 'C': {roster_x3}")
    else:
        print(f"(roster-x3) ISOLATION EXTRA: PASS ({roster_x3[0]})")

    # CALL-SITE CENSUS (R4-CR-01 lesson, CLAUDE.md's QUAL-01 row): a floor
    # whose only real call is deleted must fail the gate by name, not merely
    # pass because the isolation arms above still exercise the helper in
    # isolation. Counts THE FLOOR ITSELF plus the three isolation arms.
    executed.append("roster-census")
    roster_call_pattern = "_roster_problems" + "("
    roster_call_count = inspect.getsource(_run_self_test).count(roster_call_pattern)
    if roster_call_count != 4:
        print(
            f"(roster-census) CALL-SITE CENSUS: observed {roster_call_count} "
            "call site(s) to _roster_problems (expected 4: 1 real + 3 "
            "isolation arms)"
        )
        problems.append(
            f"(roster-census): observed {roster_call_count} _roster_problems "
            "call site(s), expected 4"
        )
    else:
        print(f"(roster-census) CALL-SITE CENSUS: PASS ({roster_call_count} call sites)")

    # (roster-entry-source) ENTRY-SOURCE LOCK (T-15-31, WR-04
    # `15-REVIEW.md`, plan 15-12 — mirrors `check-quality-harness.py`'s (x)
    # ENTRY-SOURCE LOCK, R4-CR-02): THE FLOOR ITSELF above is only as
    # trustworthy as the real call's own `covered` argument — a one-token
    # rebind to `frozenset(REQUIRED_BRANCHES)` makes `surplus = covered -
    # required` empty by construction (`x != x`, structurally incapable of
    # reporting a problem) while every isolation arm and the call-site
    # census above still pass, because both only ever drive the pure
    # helper with SYNTHETIC sets and count OCCURRENCES of the call
    # pattern, never its argument text — reproduced live, see the plan
    # 15-12 SUMMARY's Step A re-reproduction. This lock reads the real
    # call's own argument-triple text from
    # `inspect.getsource(_run_self_test)` and asserts it, whitespace-
    # normalized, against the expected literal below — a rewrite of the
    # third argument (or of the whole call site) fails here by name.
    #
    # DISCLOSED LIMITATION (mirroring `check-quality-harness.py`'s own
    # ENTRY-SOURCE LOCK disclosure): this compares SOURCE TEXT and
    # observes no behaviour — it catches an argument triple that was
    # REWRITTEN, not a floor whose returned problems are computed
    # correctly and then discarded before reaching `problems`; and an
    # argument rebound to an expression of EQUAL VALUE to the one expected
    # is harmless by construction and therefore invisible to this check.
    # This is a named control, not a registered branch id — matching the
    # (roster-census)/(validate-census)/(live-census) censuses' own
    # status — and is not counted toward `REQUIRED_BRANCHES`.
    # Built by concatenation, matching (roster-census)'s own convention
    # above (`roster_call_pattern = "_roster_problems" + "("`) — NOT
    # written out as one contiguous literal. This function's own
    # source is part of what `inspect.getsource(_run_self_test)` returns,
    # so a contiguous literal here would make the check below find its
    # OWN declaration and pass vacuously regardless of what the real call
    # site three lines above actually reads — observed live while
    # developing this control, fixed before landing.
    executed.append("roster-entry-source")
    roster_entry_source_expected = (
        "REQUIRED_BRANCHES" + ", " + "_BRANCH_ROSTER_LOCK" + ", "
        + "frozenset(covered_branches)"
    )
    roster_entry_source_problems = _entry_source_problems(
        inspect.getsource(_run_self_test), roster_entry_source_expected
    )
    if roster_entry_source_problems:
        for roster_es_msg in roster_entry_source_problems:
            print(f"(roster-entry-source) {roster_es_msg}")
        problems.extend(
            f"(roster-entry-source): {msg}" for msg in roster_entry_source_problems
        )
    else:
        print("(roster-entry-source) ENTRY-SOURCE LOCK: PASS")

    # roster-es-x1/x2/x3 ISOLATION: the ENTRY-SOURCE LOCK's own
    # falsifiability. Every arm drives `_entry_source_problems` with a
    # SYNTHETIC source string only — never
    # `inspect.getsource(_run_self_test)` — mirroring the roster-x1/x2/x3
    # arms' existing discipline.
    roster_es_x1 = _entry_source_problems(
        "call(\n        A, B, frozenset(C)\n    )", "A, B, frozenset(C)"
    )
    if roster_es_x1 != []:
        print(f"(roster-es-x1) ISOLATION CLEAN: WRONGLY reported problem(s): {roster_es_x1}")
        problems.append(f"(roster-es-x1): clean case wrongly reported {roster_es_x1}")
    else:
        print("(roster-es-x1) ISOLATION CLEAN: PASS")

    # roster-es-x2: the third argument aliased to A (the WR-04 shape).
    roster_es_x2 = _entry_source_problems(
        "call(\n        A, B, frozenset(A)\n    )", "A, B, frozenset(C)"
    )
    if len(roster_es_x2) != 1 or "not found" not in roster_es_x2[0]:
        print(
            "(roster-es-x2) ISOLATION ALIASED: expected one problem naming "
            f"the missing expected text, got {roster_es_x2}"
        )
        problems.append(
            f"(roster-es-x2): aliased case did not report as expected: {roster_es_x2}"
        )
    else:
        print(f"(roster-es-x2) ISOLATION ALIASED: PASS ({roster_es_x2[0]})")

    # roster-es-x3: no matching call at all (the call site itself deleted).
    roster_es_x3 = _entry_source_problems("def _other():\n    pass\n", "A, B, frozenset(C)")
    if len(roster_es_x3) != 1 or "not found" not in roster_es_x3[0]:
        print(
            "(roster-es-x3) ISOLATION MISSING: expected one problem naming "
            f"the missing call site, got {roster_es_x3}"
        )
        problems.append(
            f"(roster-es-x3): missing-call case did not report as expected: {roster_es_x3}"
        )
    else:
        print(f"(roster-es-x3) ISOLATION MISSING: PASS ({roster_es_x3[0]})")

    # CALL-SITE CENSUS for `_entry_source_problems` itself (R4-CR-01 lesson,
    # applied to this task's own new floor): counts THE LOCK ITSELF plus
    # the three isolation arms above, so deleting the real call leaves this
    # census red rather than the battery silently staying green with the
    # exact defect the lock exists to catch restored.
    executed.append("roster-es-census")
    roster_es_call_pattern = "_entry_source_problems" + "("
    roster_es_call_count = inspect.getsource(_run_self_test).count(roster_es_call_pattern)
    if roster_es_call_count != 4:
        print(
            f"(roster-es-census) CALL-SITE CENSUS: observed "
            f"{roster_es_call_count} call site(s) to _entry_source_problems "
            "(expected 4: 1 real + 3 isolation arms)"
        )
        problems.append(
            f"(roster-es-census): observed {roster_es_call_count} "
            "_entry_source_problems call site(s), expected 4"
        )
    else:
        print(f"(roster-es-census) CALL-SITE CENSUS: PASS ({roster_es_call_count} call sites)")

    # ISOLATION arms for `_live_exit_code` (T-15-18, `15-VERIFICATION.md` gap
    # 2): the failure-to-exit-code decision `_validate_files` makes is
    # driven here with SYNTHETIC lists — never the real, live failure list —
    # so the decision is proven correct independently of whether the
    # shipped tree happens to be clean today.
    _live_x1_err = io.StringIO()
    with contextlib.redirect_stderr(_live_x1_err):
        live_x1 = _live_exit_code([])
    if live_x1 != 0 or _live_x1_err.getvalue() != "":
        print(
            "(live-x1) ISOLATION CLEAN: expected rc=0 / no stderr, got "
            f"rc={live_x1}, stderr={_live_x1_err.getvalue()!r}"
        )
        problems.append(f"(live-x1): clean case wrongly reported rc={live_x1}")
    else:
        print("(live-x1) ISOLATION CLEAN: PASS (rc=0, no stderr)")

    _live_x2_err = io.StringIO()
    with contextlib.redirect_stderr(_live_x2_err):
        live_x2 = _live_exit_code(["Rubric-1: synthetic"])
    _live_x2_text = _live_x2_err.getvalue()
    if live_x2 != 1 or "Rubric-1: synthetic" not in _live_x2_text:
        print(
            "(live-x2) ISOLATION FAIL: expected rc=1 / stderr containing "
            f"'Rubric-1: synthetic', got rc={live_x2}, stderr={_live_x2_text!r}"
        )
        problems.append(f"(live-x2): fail case wrongly reported rc={live_x2}")
    else:
        print("(live-x2) ISOLATION FAIL: PASS (rc=1, stderr contains message)")

    # _validate_files CALL-SITE CENSUS: every leg of `_validate_files` — the
    # body check, the rubric check, the cross-surface check and the
    # failure-to-exit-code decision — must have exactly one call site
    # inside `_validate_files`' own source, so deleting a leg (or replacing
    # one with `[]`) fails this census by name instead of leaving
    # `--self-test` silently green (T-15-18). Each search pattern is built
    # by concatenating the symbol name with `"("`, matching the roster
    # census's own convention.
    executed.append("validate-census")
    _validate_files_src = inspect.getsource(_validate_files)
    _validate_census_ok = True
    for _leg_symbol in _VALIDATE_LEG_SYMBOLS:
        _leg_pattern = _leg_symbol + "("
        _leg_count = _validate_files_src.count(_leg_pattern)
        if _leg_count != 1:
            _validate_census_ok = False
            print(
                f"(validate-census) CALL-SITE CENSUS: {_leg_symbol} occurs "
                f"{_leg_count} time(s) in _validate_files' source, expected "
                "exactly 1"
            )
            problems.append(
                f"(validate-census): {_leg_symbol} occurs {_leg_count} "
                "time(s) in _validate_files, expected 1"
            )
    if _validate_census_ok:
        print(
            "(validate-census) CALL-SITE CENSUS: PASS (all four legs — "
            "body, rubric, cross-surface, exit-code decision — present "
            "exactly once)"
        )

    # `_live_exit_code` ISOLATION-ARM CENSUS: count `_live_exit_code` call
    # sites in `_run_self_test`'s OWN source against the number of isolation
    # arms added above (2), in the same shape as the roster census, so
    # deleting an isolation arm fails by name.
    executed.append("live-census")
    _live_call_pattern = "_live_exit_code" + "("
    _live_call_count = inspect.getsource(_run_self_test).count(_live_call_pattern)
    if _live_call_count != 2:
        print(
            f"(live-census) CALL-SITE CENSUS: observed {_live_call_count} "
            "call site(s) to _live_exit_code inside _run_self_test "
            "(expected 2: (live-x1) + (live-x2))"
        )
        problems.append(
            f"(live-census): observed {_live_call_count} _live_exit_code "
            "call site(s) inside _run_self_test, expected 2"
        )
    else:
        print(f"(live-census) CALL-SITE CENSUS: PASS ({_live_call_count} call sites)")

    # Anti-masking assertion: every required branch must have coverage from
    # the fixture battery above.
    uncovered = REQUIRED_BRANCHES - covered_branches
    if uncovered:
        print(
            f"ANTI-MASKING GATE FAILURE: {len(uncovered)} branch(es) not "
            f"covered: {sorted(uncovered)}"
        )
        problems.append(f"Anti-masking: {len(uncovered)} branches uncovered")
    else:
        print(
            f"ANTI-MASKING GATE: All {len(REQUIRED_BRANCHES)} branches covered: "
            f"{sorted(covered_branches)}"
        )

    # Dispatch-reachability control: re-enter main(["--self-test"]) in-process
    # to prove the CLI layer reaches this block, not merely that
    # _run_self_test() is correct when called directly.
    executed.append("dispatch")
    this_module = sys.modules[__name__]
    if not this_module._SCANGUARD_DISPATCH_REENTRANT:
        this_module._SCANGUARD_DISPATCH_REENTRANT = True
        try:
            dispatch_out, dispatch_err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(dispatch_out), contextlib.redirect_stderr(
                dispatch_err
            ):
                dispatch_rc = main(["--self-test"])
            dispatch_text = dispatch_out.getvalue()
            if dispatch_rc != 0:
                print(
                    "(dispatch) dispatch control: WRONGLY FAILED — "
                    f"main(['--self-test']) returned {dispatch_rc}, expected 0"
                )
                problems.append(
                    f"(dispatch): main(['--self-test']) returned {dispatch_rc}, expected 0"
                )
            elif "(a) positive control — body: PASS" not in dispatch_text:
                print(
                    "(dispatch) dispatch control: WRONGLY FAILED — captured "
                    f"stdout did not contain control (a)'s PASS text: {dispatch_text!r}"
                )
                problems.append("(dispatch): captured stdout missing control (a) PASS text")
            else:
                print(
                    "(dispatch) dispatch control: PASS — main(['--self-test']) "
                    "reaches this block end-to-end"
                )
        except Exception as exc:  # noqa: BLE001 - self-test must report, not crash
            print(f"(dispatch) dispatch control: WRONGLY FAILED — unexpected exception: {exc!r}")
            problems.append(f"(dispatch): unexpected exception: {exc!r}")
        finally:
            this_module._SCANGUARD_DISPATCH_REENTRANT = False
    else:
        print("(dispatch) dispatch control: skipped (nested self-test run)")

    # Live-leg dispatch control (T-15-19, `15-VERIFICATION.md` gap 2): drive
    # main([]) in-process — the documented CLI's `python3
    # scripts/check-selfaudit-scan.py` form with no flags — to prove the
    # live validate path is reachable from the CLI dispatch, not merely
    # that `_validate_files()` is correct when called directly. This gives
    # the documented CLI, its `COVERAGE —` line included, its first
    # coverage from any control. Unlike the `--self-test` dispatch control
    # above, `main([])` calls `_validate_files()`, not `_run_self_test()`,
    # so it never re-enters this function and needs no reentrancy sentinel.
    executed.append("live-dispatch")
    live_dispatch_out, live_dispatch_err = io.StringIO(), io.StringIO()
    try:
        with contextlib.redirect_stdout(live_dispatch_out), contextlib.redirect_stderr(
            live_dispatch_err
        ):
            live_dispatch_rc = main([])
        live_dispatch_text = live_dispatch_out.getvalue()
        if live_dispatch_rc != 0:
            print(
                "(live-dispatch) dispatch control: WRONGLY FAILED — "
                f"main([]) returned {live_dispatch_rc}, expected 0"
            )
            problems.append(
                f"(live-dispatch): main([]) returned {live_dispatch_rc}, expected 0"
            )
        elif "check-selfaudit-scan: COVERAGE —" not in live_dispatch_text:
            print(
                "(live-dispatch) dispatch control: WRONGLY FAILED — captured "
                f"stdout missing the COVERAGE marker: {live_dispatch_text!r}"
            )
            problems.append("(live-dispatch): captured stdout missing COVERAGE marker")
        elif "check-selfaudit-scan: PASS" not in live_dispatch_text:
            print(
                "(live-dispatch) dispatch control: WRONGLY FAILED — captured "
                f"stdout missing the PASS line: {live_dispatch_text!r}"
            )
            problems.append("(live-dispatch): captured stdout missing PASS line")
        else:
            print(
                "(live-dispatch) dispatch control: PASS — main([]) reaches "
                "_validate_files end-to-end"
            )
    except Exception as exc:  # noqa: BLE001 - self-test must report, not crash
        print(f"(live-dispatch) dispatch control: WRONGLY FAILED — unexpected exception: {exc!r}")
        problems.append(f"(live-dispatch): unexpected exception: {exc!r}")

    # Live-dispatch-control CALL-SITE CENSUS: count the live-dispatch
    # control's own real call site in `_run_self_test`'s source, so
    # deleting the entire control fails this census by name rather than
    # leaving `--self-test` silently green (T-15-19) — the census above
    # this one floors what the control asserts; this one floors that the
    # control itself still exists. Pattern built from two concatenated
    # halves so this line's own source never self-matches.
    executed.append("live-dispatch-census")
    _live_dispatch_call_pattern = "live_dispatch_rc = main(" + "[])"
    _live_dispatch_call_count = inspect.getsource(_run_self_test).count(
        _live_dispatch_call_pattern
    )
    if _live_dispatch_call_count != 1:
        print(
            f"(live-dispatch-census) CALL-SITE CENSUS: observed "
            f"{_live_dispatch_call_count} call site(s) to the live-dispatch "
            "control's main([]) invocation (expected 1)"
        )
        problems.append(
            f"(live-dispatch-census): observed {_live_dispatch_call_count} "
            "live-dispatch call site(s), expected 1"
        )
    else:
        print(
            "(live-dispatch-census) CALL-SITE CENSUS: PASS "
            f"({_live_dispatch_call_count} call site)"
        )

    # (roster-floor-missing / roster-floor-extra) Negative arms (permanent
    # registered controls, Phase 21-15, CR-05): prove
    # `_selfaudit_meta_floor_problems` — the SAME helper the live floor
    # below calls — actually fires on a synthetic mismatch and names the
    # specific offending ids, in both directions. Driven against a synthetic
    # executed/registered pair, never the real module roster, so these arms
    # cannot corrupt the live floor they are proving. Runs BEFORE the
    # (describe) control below so `executed` already carries all
    # non-describe ids by the time describe()'s own comparison reads it.
    executed.append("roster-floor-missing")
    executed.append("roster-floor-extra")
    _synthetic_registered = ("synthetic-a", "synthetic-b")
    _synthetic_executed = ["synthetic-a", "synthetic-c"]
    _synthetic_problems = _selfaudit_meta_floor_problems(
        _synthetic_executed, _synthetic_registered
    )
    _synthetic_text = " ".join(_synthetic_problems)
    if not _synthetic_problems:
        print(
            "(roster-floor-missing/extra) negative arms: WRONGLY FAILED — "
            "_selfaudit_meta_floor_problems did NOT fire on a synthetic mismatch"
        )
        problems.append("(roster-floor-missing/extra): floor did not fire on synthetic mismatch")
    else:
        _missing_clause, _extra_clause = _roster_arm_clauses(_synthetic_text)
        if "synthetic-b" not in _missing_clause or "synthetic-c" not in _extra_clause:
            print(
                "(roster-floor-missing/extra) negative arms: WRONGLY FAILED — fired but "
                f"did not name both the missing and extra synthetic ids in their "
                f"correct clauses: missing_clause={_missing_clause!r} extra_clause={_extra_clause!r}"
            )
            problems.append("(roster-floor-missing/extra): floor did not name both directions")
        else:
            print(
                "(roster-floor-missing/extra) negative arms: PASS — fires and names "
                f"both directions: missing_clause={_missing_clause!r} extra_clause={_extra_clause!r}"
            )

    # (describe) describe()-consistency control (D-03, plan 21-05): the
    # module-level constants --describe reads must agree with the live
    # REQUIRED_BRANCHES/_VALIDATE_LEG_SYMBOLS/_META_CONTROL_IDS/_BAND_BULLETS
    # this self-test just exercised. Deliberately NOT a REQUIRED_BRANCHES
    # entry — it lives alongside (dispatch)/(live-dispatch) in
    # _META_CONTROL_IDS, the self-test's infrastructure-control roster.
    #
    # Phase 21-15 (CR-05): the control_ids/control_count comparison below
    # used to compare `describe()` against `_META_CONTROL_IDS` — the SAME
    # constant `describe()` itself reads — which is a tautology, not a
    # check (CR-05's own finding). It now compares against `executed`, the
    # ids this self-test run actually reached, so a control silently
    # removed from _META_CONTROL_IDS or from the roster this run exercised
    # is caught here too, independent of the separate roster floor below.
    # This is the LAST control to append (its own id, "describe") before the
    # comparison runs, so `executed` is complete (all other 11 ids already
    # appended, including the two negative arms above) by the time
    # `_desc["control_count"]` (== len(_META_CONTROL_IDS) == 12) is compared
    # against `len(executed)`.
    executed.append("describe")
    _desc = describe()
    if _desc["branch_roster"] != sorted(REQUIRED_BRANCHES):
        problems.append("(describe): branch_roster disagrees with REQUIRED_BRANCHES")
    elif _desc["branch_count"] != len(REQUIRED_BRANCHES):
        problems.append("(describe): branch_count disagrees with len(REQUIRED_BRANCHES)")
    elif _desc["call_site_census"] != {symbol: 1 for symbol in _VALIDATE_LEG_SYMBOLS}:
        problems.append("(describe): call_site_census disagrees with _VALIDATE_LEG_SYMBOLS")
    elif set(_desc["control_ids"]) != set(executed):
        problems.append("(describe): control_ids disagrees with executed controls")
    elif _desc["control_count"] != len(executed):
        problems.append("(describe): control_count disagrees with len(executed)")
    elif _desc["locked_constants"]["band_bullets"] != " | ".join(_BAND_BULLETS):
        problems.append("(describe): band_bullets disagrees with _BAND_BULLETS")
    else:
        print(
            f"(describe) describe()-consistency: PASS "
            f"({len(REQUIRED_BRANCHES)} branches, {len(executed)} meta-controls "
            "executed, agreeing with control_ids)"
        )

    # Executed-vs-registered floor (Phase 21-15, CR-05): _META_CONTROL_IDS is
    # a second, independently-typed transcription of the meta-control ids
    # this function's controls append to `executed`. A control silently not
    # running — deleted, or an `executed.append()` call removed — leaves its
    # id absent from `executed`, which this floor catches BY NAME, in both
    # directions in one run, rather than silently narrowing the published
    # roster.
    _meta_roster_problems = _selfaudit_meta_floor_problems(executed, _META_CONTROL_IDS)
    if _meta_roster_problems:
        problems.extend(_meta_roster_problems)
        print("control roster/executed floor: FAIL — " + "; ".join(_meta_roster_problems))
    else:
        print(
            f"control roster/executed floor: PASS — {len(executed)} meta-controls "
            "executed, all registered in _META_CONTROL_IDS"
        )

    if problems:
        sys.stderr.write("check-selfaudit-scan --self-test: FAIL — " + "; ".join(problems) + "\n")
        return 1

    print("check-selfaudit-scan --self-test: PASS")
    return 0


def main(argv: list[str] | None = None) -> int:
    """Run the check-selfaudit-scan CLI and return a process exit code.

    `argv` accepts an explicit list (defaulting to None, which makes argparse
    fall back to `sys.argv[1:]`) so the dispatch-reachability control can drive
    `main(["--self-test"])` in-process and inspect the return code, proving the
    CLI dispatch itself reaches the self-test block rather than only
    `_run_self_test()` being correct when called directly.
    """
    if sys.version_info < (3, 12):
        sys.stderr.write(
            "scripts/check-selfaudit-scan.py requires Python >=3.12 "
            f"(running {sys.version_info.major}.{sys.version_info.minor}).\n"
        )
        return 2

    parser = argparse.ArgumentParser(
        prog="check-selfaudit-scan.py",
        description=(
            "SCAN-GUARD: assert the self-audit scan's prescription and verify "
            "block are present and well-formed in the emitted tree."
        ),
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run the offline self-test control battery",
    )
    parser.add_argument(
        "--describe",
        action="store_true",
        help="emit this gate's own self-description as JSON on stdout and exit",
    )
    args = parser.parse_args(argv)

    if args.describe:
        print(json.dumps(describe(), indent=2, sort_keys=True))
        return 0

    if args.self_test:
        return _run_self_test()

    return _validate_files()


if __name__ == "__main__":
    sys.exit(main())
