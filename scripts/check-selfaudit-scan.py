#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# ///
"""SCAN-GUARD gate: assert the self-audit scan's prescription (plan 15-01) and its
verify block and quote-source sentences (plan 15-02) are present, correctly placed
and internally coherent in the emitted first-principles tree.

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
`.github/workflows/validation.yml`; the battery tally moved 23 -> 24 when it
landed (plan 15-04).

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
    cycle or name an ungrounded input (`_chain_dependency_defects`,
    `scripts/check-quality-harness.py:5058`), or that a claim really is untraced —
    only that the prescription and the verify block exist, are placed correctly
    and are internally coherent; content reconciliation is what
    `_selfaudit_calibration_defects` (`scripts/check-quality-harness.py:5193`)
    already performs after the fact on a real run's text, and this gate does not
    duplicate it.
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
    pins**: the gate pins that the Verdict Block Format admits the self-audit
    scan for Criteria 4 and 6 only, that each of those two criteria's quoted-span
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
before `## Self-Audit Gate` (the same D-04 slot RESEARCH.md §5 measured): **2,288
characters, 27 lines, 17 table data rows.**

In plain words: the new scan is smaller than the Assumption Audit scan on every unit
measured here — roughly two-thirds its size in characters (2,288 / 3,408), about
half its size in lines (27 / 52), and about two-fifths its size in table rows
(17 / 44). Measured 2026-09-04.

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
    "for Criteria 4 and 6 only, from the self-audit scan emitted as "
    'process output for this analysis.]"'
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
    if aa_idx != -1 and scan_idx != -1 and precedence_idx != -1:
        if not (aa_idx < scan_idx < precedence_idx):
            failures.append(
                "Rubric-2: scan block is not placed strictly between the "
                "Assumption Audit block and the Precedence rule (placement violated)"
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

        # Rubric-13 (plan 15-08, closing CR-01): the admission's two clauses
        # — the self-audit scan for Criteria 4/6, and the Assumption Audit
        # scan for Criterion 2 — each occur exactly once inside the same
        # section slice. Split so a later edit that drops one clause while
        # keeping the whole-sentence count intact (e.g. via the OTHER
        # clause's text) is still caught.
        c46_count = _count_flat(format_slice, _ADMISSION_SCOPE_C46)
        if c46_count != 1:
            failures.append(
                f"Rubric-13: admission's Criteria-4/6 clause occurs "
                f"{c46_count} time(s) in the Verdict Block Format "
                "section, expected exactly 1"
            )

        c2_count = _count_flat(format_slice, _ADMISSION_SCOPE_C2)
        if c2_count != 1:
            failures.append(
                f"Rubric-13: admission's Criterion-2 clause occurs "
                f"{c2_count} time(s) in the Verdict Block Format "
                "section, expected exactly 1"
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
    return failures


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

    if failures:
        for msg in failures:
            sys.stderr.write(f"check-selfaudit-scan: FAIL — {msg}\n")
        return 1

    print(f"check-selfaudit-scan: COVERAGE — {AGENT_FILE}, {RUBRIC_FILE}")
    print("check-selfaudit-scan: PASS")
    return 0


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

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
        "R-11-bands-crit4",
        "R-11-bands-crit6",
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
        "R-02-placement-order", "R-02-placement-anchor",
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
        "R-11-bands-crit4", "R-11-bands-crit6",
        "R-12-halt-missing", "R-12-halt-dup",
        "R-13-format-amended-missing", "R-13-format-amended-dup",
        "R-13-format-admission-missing", "R-13-format-admission-dup",
        "R-13-format-preamendment", "R-13-format-order",
        "R-13-format-admission-c46-missing", "R-13-format-admission-c46-dup",
        "R-13-format-admission-c2-missing", "R-13-format-admission-c2-dup",
        "R-13-format-admission-superseded",
        "R-14-c2-descriptor-missing", "R-14-c2-descriptor-dup",
        "B-17-validate-missing", "B-17-validate-dup", "B-17-validate-preamendment",
        "X-01-cols-chain-body", "X-01-cols-chain-rubric",
        "X-01-cols-claim-body", "X-01-cols-claim-rubric",
        "X-02-heading-body", "X-02-heading-rubric",
        "X-03-bound-body", "X-03-bound-rubric",
        "X-04-admission-c46-body", "X-04-admission-c46-rubric",
        "X-04-admission-c2-body", "X-04-admission-c2-rubric",
    }
)


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
    # — the literal remains present but out of order.
    rubric_r02a = _relocate(real_rubric, _RUBRIC_SCAN_BLOCK, _RUBRIC_PRECEDENCE)
    _check_negative(
        "R-02a",
        _check_rubric_text(rubric_r02a),
        "Rubric-2",
        "placement violated",
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

    # R-11-bands-crit4: strip one band bullet from the Criterion 4 slice.
    rubric_r11a = _mutate_within_range(
        real_rubric, _CRIT4_START, _CRIT5_START, _BAND_SOUND, "REMOVED"
    )
    _check_negative(
        "R-11a",
        _check_rubric_text(rubric_r11a),
        "Rubric-11",
        "in Criterion 4 slice",
        "R-11-bands-crit4",
    )

    # R-11-bands-crit6: duplicate one band bullet in the Criterion 6 slice.
    rubric_r11b = _mutate_within_range(
        real_rubric,
        _CRIT6_START,
        _USAGE_NOTE,
        _BAND_SOUND,
        _BAND_SOUND + "\n" + _BAND_SOUND,
    )
    _check_negative(
        "R-11b",
        _check_rubric_text(rubric_r11b),
        "Rubric-11",
        "in Criterion 6 slice",
        "R-11-bands-crit6",
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

    # THE FLOOR ITSELF (WR-02, `15-REVIEW.md`): roster-equality plus
    # coverage-subset, routed through `_roster_problems` so the isolation
    # arms below drive the exact code path this real call uses.
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
    args = parser.parse_args(argv)

    if args.self_test:
        return _run_self_test()

    return _validate_files()


if __name__ == "__main__":
    sys.exit(main())
