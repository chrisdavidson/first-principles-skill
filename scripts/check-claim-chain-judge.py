#!/usr/bin/env python3
"""Semantic claim-to-chain correspondence judge (backlog 999.4).

Asks one question, per claim, that no shipped instrument asks: **does the
derivation chain this claim cites actually support it?**

What is already checked, stated accurately
------------------------------------------
`_claim_is_traced` in `scripts/check-quality-harness.py` (the function behind
the `untraced_claims` column) returns true by any of three citation routes:

 1. the claim names a chain id -- the exact stored form, or a normalised
    abbreviated/pluralised one (`(C1)`, `chain **C1**`, `(Chains C2, C3)`);
 2. the claim names more than one Ground Truth identifier, and those
    identifiers co-occur inside a single chain block;
 3. the claim is quoted by a closure-ledger entry that cites a real chain.

All three ask whether a citation is *present*. **None of them opens the cited
chain to test whether it supports the claim.** That is the gap this tool
fills, and the distinction it turns on is citation presence versus semantic
support. A claim that cites the wrong chain, a chain that reaches a different
conclusion, or a chain that contradicts it, reads clean on every route above.
(The ROADMAP's own preamble compresses this to "tests whether a claim contains
the substring C1"; that is the first route only. Do not propagate the
compression -- the implementation is richer, and still presence-only.)

Decision D-1: backlog 999.35 is SUBSUMED here, not fixed first
--------------------------------------------------------------
Recorded so the next reader does not reopen it. Two grounds, both from
999.35's own record:

 1. `_chain_head_refs` sits inside CONTRACT-06's frozen detector surface.
    Widening its read window is "exactly the kind of mid-measurement detector
    change 999.2 exists to forbid, and any such change requires a written
    amendment to the milestone goal before the diff, never after." No such
    amendment exists, and this tool does not author one.
 2. T-06's circularity was already caught by fresh-context reasoning review in
    both arms of the 2026-09-15 Option 5B measurement, at the catalogued
    section-4 prose location (score tokens `s009`, `s016`). 999.35 records that
    as "a measured input on the 'subsume' side" and concludes a mechanical fix
    is "optional, not the only route".

So this tool modifies no frozen detector. It imports `_slice_sections`,
`_chain_ids`, `_chain_blocks`, `_chain_head_refs`, `_conclusion_claims`,
`_cites_chain`, `_ledger_fragment_covers` and the transport helpers from
`check-quality-harness.py` and calls them; it never edits one. A circularity
stated past a chain's head line is visible to the judge here because the whole
chain block is handed over verbatim, not because any read window moved.

Blinding, which is the integrity of the whole reading
----------------------------------------------------
A judge told that its input is wrong "finds" a defect in everything and the
run measures nothing. So the judge sees the claim, the chains the claim itself
names, and the ground truths those chains rest on -- nothing else. No
filename, no directory, no label, no statement that the input may be false,
and no framing of what the reading is for. `blinding_problems()` asserts this
over the **assembled prompt**, template plus packet content, and
`assert_blinded()` raises; every live invocation passes through it.

Two deliberate scoping choices in that term list, both measured rather than
assumed:

(a) The list bars `catalog.md` and `catalogued falsehood`, **not** bare
    `catalog`. Bare `catalog` occurs in legitimate product-domain prose on
    shipped surfaces -- `shared/examples/composed-inversion-second-order.md`
    ("the catalog-search endpoint", "the catalog service's published event
    schema") and `shared/examples/self-application.md` ("delegates a *catalog*
    (a reference ...)"). Barring it would fire on honest content and the
    assertion would have to be switched off, which is worse than a narrower
    term. Same reason `fixture` is barred only inside `adversarial fixture`:
    `shared/examples/science-engineering.md` prices LED lighting by the
    fixture.
(b) `check-quality-harness.py`'s own `_FORBIDDEN_JUDGE_PROMPT_SUBSTRINGS` is
    deliberately NOT reused. Its leak family is a *comparison* leak (another arm,
    a baseline, a prior result) and it bars `compare`, `comparison`,
    `baseline`, `versus`. This tool judges one document with no other arm in
    existence, and analysis prose routinely and legitimately compares things
    -- `shared/examples/estimate-fermi.md` reasons about "the comparison
    against lithium-ion". Importing that list would make the assertion
    unusable. The two lists guard different leaks.

Disclosed bounds
----------------
(a) **This is a measurement, never a gate.** It is registered in no CI job and
    in no `scripts/check-firewall-battery.sh` entry, and it exits 0 whatever
    the verdicts say. A live reading carries its N and is an observation:
    `docs/v8.7-constraint-teardown.md` §2 item 3 bars a K-of-N live
    result from gating a phase, measured on the S-P04 vector swinging
    2/5 -> 0/5 -> 2/5 with no source change.
(b) **The tool never reads `tests/adversarial-corpus-v9.0/catalog.md`,** and
    has no code path that could. Joining a verdict to a catalogued target is
    hand work done in a findings write-up, precisely so no catalogued
    expectation can leak into the prompt or bias the reading.
(c) **"Claim" means exactly what `_conclusion_claims` means by it** -- no
    second claim definition is invented here, and `complete_claims` adds none
    and drops none (it only extends each identified claim to the end of its own
    paragraph, because `_conclusion_claims` returns a physical LINE and a
    hard-wrapped document's line is a sentence fragment; see that function's
    docstring for what was measured). One consequence, disclosed rather than
    hidden: because the citation scan then runs over the completed sentence, a
    chain cited on a continuation line is found here where `_claim_is_traced`'s
    line-scoped reading would not find it. The difference only ever runs toward
    finding MORE citations, never fewer. That function counts some
    section-6 meta lines (a `**Confidence:**` roll-up, a `**Pre-check:**`
    line) as claims. Asked whether a chain "supports" a confidence roll-up, a
    judge should answer UNDECIDABLE, which is one of the reasons the third
    verdict value is not optional: without it those lines would be forced into
    a false binary and the DOES-NOT-SUPPORT rate would stop being readable.
(d) **A claim that cites no chain at all is excluded from judging** and
    counted separately. That case is what `untraced_claims` already covers;
    folding it in would mix a presence finding into a support reading.
(e) **An unresolved chain-shaped reference is reported, not diagnosed.** A
    section-6 `(C3)` where section 4 defines no chain C3 reaches the judge as
    a stated fact about the material. Measured instance where that is *not* a
    wrong citation: `shared/examples/decompose-irreducibility.md` uses `C1`,
    `C2`, `C3` as irreducibility-drill branch labels in section 4 while its
    only derivation chain is `Conclusion C1`, so its section-6 `(C3)` names a
    branch, not a chain. The tool states what it found; a reader adjudicates.
(f) **The blinding term list is validated against honest content on demand,
    not inside `--self-test`.** `--dry-run --dir <DIR>` assembles and
    blinding-checks every document in a directory without invoking anything,
    so `--dry-run --dir shared/examples` and `--dry-run --dir
    tests/adversarial-corpus-v9.0` together are the reproduction of the claim
    that no term fires on honest prose. That check is deliberately NOT folded
    into `--self-test`, which stays free of any dependency on those 27 files.
(g) **Transitive chain expansion is bounded and cycle-safe.** When a chain's
    head composes on another chain, that chain's block is included too, to
    `_MAX_COMPOSITION_DEPTH` levels, each block once. A genuine citation cycle
    therefore reaches the judge as blocks that cite each other, which is
    visible reasoning, not a structural flag.
(h) **Expansion reads chain bodies as well as heads, and that was forced by
    measurement.** Head-driven expansion alone inherits the blindness D-1
    declines to fix in the detector: `_chain_head_refs` reads one line, so a
    chain naming another chain in the prose *under* its head yields no
    expansion. Measured on `t06-hidden-cycle-past-head.md` -- the catalogued
    999.35 item -- where head-only expansion handed each packet a single block
    and both claims read SUPPORTS. A second, depth-one hop now also pulls in
    chains referenced anywhere in an included chain's body, labelled
    `referenced-by:` in the packet so the reader can tell how a block arrived.
    The scan is this module's own and reads a block the frozen function already
    returned; `_chain_head_refs` is called, never altered.
(i) **A chain reference is the document's own `C<n>` token, not prose.** A
    chain that says "which Chain 2 does" in words contributes no expansion,
    because the reference vocabulary is the token form `_chain_head_refs` and
    `_cites_chain` already recognise. Measured instance:
    `t08-verdict-contradicts-its-type.md`'s C1 confidence note.

Usage:
    python3 scripts/check-claim-chain-judge.py --self-test
    python3 scripts/check-claim-chain-judge.py --dry-run --analysis FILE.md
    python3 scripts/check-claim-chain-judge.py --analysis FILE.md [FILE.md ...]
    python3 scripts/check-claim-chain-judge.py --dir DIR [--out REPORT.md]
    python3 scripts/check-claim-chain-judge.py --inject always-supports

Exit codes:
    0  a reading completed, a --dry-run completed, or --self-test passed
    1  --self-test failed (including under --inject), or a usage/IO error
    2  `claude` is not on PATH and a live reading was asked for
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Callable, NamedTuple

REPO_ROOT = Path(__file__).resolve().parent.parent
_HARNESS_PATH = REPO_ROOT / "scripts" / "check-quality-harness.py"


# --- the imported, never-modified detector surface --------------------------


def _load_harness():
    """Import `check-quality-harness.py` as a module and return it.

    The filename carries hyphens, so it is not importable by name. Registered
    in `sys.modules` before `exec_module` because the harness defines frozen
    dataclasses, and `dataclasses` resolves `cls.__module__` through
    `sys.modules` while processing them.

    Nothing in the loaded module is ever written to. Every function this tool
    uses from it is called, never redefined, and four of them
    (`_chain_head_refs`, `_conclusion_claims`, `_slice_sections`, and
    `_chain_block_well_formed` via its digest pin) are frozen under
    CONTRACT-06.
    """
    spec = importlib.util.spec_from_file_location("_qh_for_claim_chain_judge", _HARNESS_PATH)
    if spec is None or spec.loader is None:
        raise SystemExit(f"error: cannot load {_HARNESS_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


QH = _load_harness()

# Bounded transitive expansion of composition heads (disclosed bound (g)).
_MAX_COMPOSITION_DEPTH = 3

# A section-3 ground-truth entry: a list item whose first bold span is a GT id.
_GT_ENTRY_RE = re.compile(r"^[ \t]*[-*][ \t]*\*\*(GT-[A-Za-z0-9]+\??)\*\*", re.MULTILINE)

# A chain-shaped reference in claim prose, after GT tokens are masked out so
# `GT-C1` can never read as a reference to chain `C1` (the same hazard
# `_chain_head_refs` documents for head lines).
_CHAIN_SHAPED_REF_RE = re.compile(r"\bC\d+\b")
_GT_TOKEN_MASK_RE = re.compile(r"GT-[A-Za-z0-9]+\??")


# --- packet extraction (Task 1) ---------------------------------------------


class ChainText(NamedTuple):
    """One derivation chain as the judge will see it.

    `via` is `cited` when the claim names this chain itself, `ledger` when a
    closure-ledger row quotes the claim and cites this chain, and
    `composed-by:<id>` when the chain was pulled in because another included
    chain's head builds on it.
    """

    chain_id: str
    text: str
    via: str


class ClaimPacket(NamedTuple):
    """The claim, the chains it cites, and the ground truths those rest on.

    Nothing else. `unresolved_refs` holds chain-shaped references in the claim
    that section 4 defines no chain for -- stated to the judge rather than
    silently dropped (disclosed bound (e)).
    """

    index: int
    claim_text: str
    chains: tuple[ChainText, ...]
    ground_truths: tuple[tuple[str, str], ...]
    unresolved_refs: tuple[str, ...]
    all_chain_ids: tuple[str, ...]

    @property
    def judgeable(self) -> bool:
        """Whether asking the support question of this claim is meaningful.

        False when the claim names no chain and no unresolved chain-shaped
        reference -- the `untraced_claims` case, excluded per disclosed bound
        (d).
        """
        return bool(self.chains) or bool(self.unresolved_refs)


def ground_truth_entries(section3: str) -> list[tuple[str, str]]:
    """Return `(gt_id, full entry text)` for each section-3 ground truth, in order."""
    matches = list(_GT_ENTRY_RE.finditer(section3))
    entries: list[tuple[str, str]] = []
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(section3)
        body = section3[start:end].strip()
        # A trailing horizontal rule belongs to the section, not the entry.
        body = re.sub(r"\n*-{3,}\s*$", "", body).strip()
        entries.append((m.group(1), body))
    return entries


def _gt_key(gt_id: str) -> str:
    """Comparable form of a GT id: case-folded, `?`-suffix dropped.

    A chain head may write `GT-7` where section 3 writes `GT-7?` (or the
    reverse); the `?` marks verification state, not identity.
    """
    return gt_id.strip().rstrip("?").casefold()


def complete_claims(section6: str, claims: list[str]) -> list[str]:
    """Extend each `_conclusion_claims` claim to the end of its own paragraph.

    `_conclusion_claims` identifies claims line by line and returns the
    stripped physical line (or, for a list item, its text after the marker).
    On a hard-wrapped document that is a sentence FRAGMENT, and a fragment is
    not a claim a support question can be asked about. Measured before this
    existed: half the claims on both measured surfaces arrived cut mid-sentence
    (`shared/examples/estimate-fermi.md` read "The bracket width (chain C1)
    reflects the uncertainty in", and a judge correctly answered UNDECIDABLE
    four times over on that document because the text asserted nothing).

    **The claim POPULATION is untouched.** This returns exactly one string per
    input claim, in the same order, and adds no claim and drops none --
    `_conclusion_claims` remains the sole authority on which lines are claims,
    and it is called, never altered. What changes is only how much of each
    identified claim's own paragraph the judge is shown.

    Continuation stops at a blank line, a fenced line, or a line that opens a
    new claim shape. Lines are joined with single spaces, undoing the wrap.
    """
    lines = section6.split("\n")
    fenced = QH._fenced_code_flags(lines)
    completed: list[str] = []
    cursor = 0
    for claim in claims:
        found: int | None = None
        for idx in range(cursor, len(lines)):
            if fenced[idx]:
                continue
            stripped = lines[idx].strip()
            if stripped == claim:
                found = idx
                break
            lm = QH._LIST_ITEM_RE.match(stripped)
            if lm and lm.group(1).strip() == claim:
                found = idx
                break
        if found is None:
            # Unlocatable: hand over the claim exactly as the detector gave it
            # rather than guessing. Never a silent drop.
            completed.append(claim)
            continue
        cursor = found + 1
        parts = [claim]
        for idx in range(found + 1, len(lines)):
            if fenced[idx]:
                break
            nxt = lines[idx].strip()
            if not nxt:
                break
            if QH._BOLD_LEADIN_COLON_RE.match(nxt) or QH._LIST_ITEM_RE.match(nxt):
                break
            if nxt.startswith("#") or re.fullmatch(r"-{3,}", nxt):
                break
            parts.append(nxt)
            cursor = idx + 1
        completed.append(" ".join(parts))
    return completed


def _ledger_rows(section6: str) -> list[tuple[str, str]]:
    """Return `(quoted fragment, chain id)` for each structural closure-ledger row.

    Uses the harness's own `_STRUCTURAL_LEDGER_ROW_RE` -- the row shape
    `output-template.md` prescribes -- read, never redefined, so this tool and
    `_closure_ledger_fragments` cannot disagree about what a ledger row is.
    """
    rows: list[tuple[str, str]] = []
    for line in section6.splitlines():
        m = QH._STRUCTURAL_LEDGER_ROW_RE.match(line.strip())
        if m:
            rows.append((m.group(1), m.group(2)))
    return rows


def extract_packets(analysis_text: str) -> list[ClaimPacket]:
    """Build one judge packet per section-6 claim.

    Raises the harness's `SectionResolutionError` when the six sections do not
    resolve -- an unmeasurable document is not silently scored as clean.
    """
    sections = QH._slice_sections(analysis_text)
    section3, section4, section6 = sections[3], sections[4], sections[6]

    chain_ids = QH._chain_ids(section4)
    blocks = QH._chain_blocks(section4)
    # `_chain_blocks` returns the whole section as one block when it finds no
    # labels; that block belongs to no id, so pair only what pairs.
    by_id: dict[str, str] = {}
    if len(blocks) == len(chain_ids):
        by_id = dict(zip(chain_ids, blocks))
    norm_to_id = {QH._normalize_chain_id(cid): cid for cid in chain_ids}

    gt_entries = ground_truth_entries(section3)
    gt_by_key = {_gt_key(gt_id): (gt_id, body) for gt_id, body in gt_entries}

    ledger_rows = _ledger_rows(section6)
    # `_conclusion_claims` decides WHICH lines are claims; `complete_claims`
    # only extends each one to its own paragraph so the judge is shown a
    # sentence rather than a wrapped fragment. Population, order and count are
    # identical -- asserted by a control in `packet_problems`.
    claims = complete_claims(section6, QH._conclusion_claims(section6, chain_ids))

    packets: list[ClaimPacket] = []
    for idx, claim in enumerate(claims, start=1):
        chains: list[ChainText] = []
        seen: set[str] = set()

        def add(chain_id: str, via: str) -> None:
            if chain_id in seen or chain_id not in by_id:
                return
            seen.add(chain_id)
            chains.append(ChainText(chain_id, by_id[chain_id].strip(), via))

        for cid in chain_ids:
            if QH._cites_chain(claim, [cid]):
                add(cid, "cited")
        for fragment, ledger_chain in ledger_rows:
            if QH._ledger_fragment_covers(fragment, claim):
                target = norm_to_id.get(QH._normalize_chain_id(ledger_chain))
                if target is not None:
                    add(target, "ledger")

        # Bounded, cycle-safe transitive expansion of composition heads.
        frontier = [(c.chain_id, 0) for c in chains]
        while frontier:
            parent, depth = frontier.pop(0)
            if depth >= _MAX_COMPOSITION_DEPTH:
                continue
            _gts, refs = QH._chain_head_refs(by_id.get(parent, ""))
            for ref in sorted(refs):
                target = norm_to_id.get(QH._normalize_chain_id(ref))
                if target is None or target in seen:
                    continue
                add(target, f"composed-by:{QH._normalize_chain_id(parent).upper()}")
                frontier.append((target, depth + 1))

        # One further hop, driven by the chain BODY rather than its head
        # (disclosed bound (h)). Head-driven expansion alone inherits exactly
        # the blindness D-1 declines to fix in the detector: `_chain_head_refs`
        # reads one line, so a chain that names another chain in the prose
        # under its head contributes no expansion and the judge is handed one
        # side of a two-sided dependence. Measured on
        # `t06-hidden-cycle-past-head.md`, where both packets carried a single
        # block and both claims read SUPPORTS. This scan lives here, in this
        # module, and reads a block the frozen function already returned --
        # `_chain_head_refs` is called, never altered.
        for parent in [c.chain_id for c in chains]:
            body = by_id.get(parent, "")
            masked = _GT_TOKEN_MASK_RE.sub(" ", body)
            for ref in sorted({r.upper() for r in _CHAIN_SHAPED_REF_RE.findall(masked)}):
                target = norm_to_id.get(QH._normalize_chain_id(ref))
                if target is None or target in seen:
                    continue
                add(target, f"referenced-by:{QH._normalize_chain_id(parent).upper()}")

        # Ground truths named by the heads of every included chain.
        gts_needed: list[str] = []
        for c in chains:
            head_gts, _refs = QH._chain_head_refs(c.text)
            for g in sorted(head_gts):
                key = _gt_key(g)
                if key in gt_by_key and key not in gts_needed:
                    gts_needed.append(key)
        ground_truths = tuple(gt_by_key[k] for k in gts_needed)

        masked = _GT_TOKEN_MASK_RE.sub(" ", claim)
        refs_in_claim = {r.upper() for r in _CHAIN_SHAPED_REF_RE.findall(masked)}
        known = {QH._normalize_chain_id(cid).upper() for cid in chain_ids}
        unresolved = tuple(sorted(r for r in refs_in_claim if r not in known))

        packets.append(
            ClaimPacket(
                index=idx,
                claim_text=claim.strip(),
                chains=tuple(chains),
                ground_truths=ground_truths,
                unresolved_refs=unresolved,
                all_chain_ids=tuple(chain_ids),
            )
        )
    return packets


# --- the judge prompt (Task 2) ----------------------------------------------

_VERDICT_START = "=== CLAIM-CHAIN-VERDICT-START ==="
_VERDICT_END = "=== CLAIM-CHAIN-VERDICT-END ==="

SUPPORTS = "SUPPORTS"
DOES_NOT_SUPPORT = "DOES-NOT-SUPPORT"
UNDECIDABLE = "UNDECIDABLE"
UNPARSEABLE = "UNPARSEABLE"

# Three values, and the third is not optional: without UNDECIDABLE the judge is
# forced into a false binary and the DOES-NOT-SUPPORT rate stops being readable.
_VERDICT_VOCAB = (SUPPORTS, DOES_NOT_SUPPORT, UNDECIDABLE)

PROMPT_HEADER = (
    "For each numbered item below, answer one question and only that "
    "question: does the reasoning quoted in the item establish the claim "
    "quoted in the item?\n\n"
    "Each item gives you a claim, the full text of every derivation the claim "
    "itself names, and the stated facts those derivations rest on. That is "
    "the whole of the material. Judge each item on exactly that material, on "
    "its own terms, reaching no conclusion about where it came from or why "
    "you are being asked.\n\n"
    "Use exactly one of these three values per item:\n"
    f"- {SUPPORTS} -- the quoted reasoning establishes the quoted claim: it "
    "is about the same thing, and its stated steps reach what the claim "
    "asserts.\n"
    f"- {DOES_NOT_SUPPORT} -- it does not. Among the ways this happens: the "
    "reasoning reaches a different conclusion from the one the claim states; "
    "it is about a different subject; the claim asserts more than the "
    "reasoning establishes; the steps do not follow from the stated facts "
    "given; the claim names a derivation the material says is not defined; or "
    "two derivations rest on each other with nothing underneath.\n"
    f"- {UNDECIDABLE} -- the material is genuinely not enough to tell either "
    "way, or the quoted claim asserts nothing that reasoning could "
    "establish.\n\n"
    "Judge the reasoning, not the wording: a claim worded loosely but reached "
    "by the steps shown still counts as established, and a claim worded "
    "confidently that the steps do not reach does not. Where a claim names "
    "more than one derivation, ask whether the ones named, taken together, "
    "reach it.\n\n"
    "Work through the items in your own words first if that helps. Then close "
    "your response with exactly this block, and write nothing after it:\n\n"
    f"{_VERDICT_START}\n"
    "ITEM-1: <" + "|".join(_VERDICT_VOCAB) + "> -- <one clause giving the reason>\n"
    "ITEM-2: <" + "|".join(_VERDICT_VOCAB) + "> -- <one clause giving the reason>\n"
    f"{_VERDICT_END}\n\n"
    "Emit exactly one ITEM- line per item, numbered from 1 upward in the "
    "order the items appear, with no line omitted, added, reordered or "
    "renamed. Replace each placeholder with exactly one value from the "
    "three-value list above, spelled exactly as written there, followed by "
    "the ` -- ` separator and a one-clause reason."
)


def render_packet(packet: ClaimPacket) -> str:
    """Render one packet as the judge sees it.

    Carries the claim, the chains, and the ground truths -- and no filename,
    no id from any catalogue, and no statement about the material's quality.
    """
    parts = [f"### Item {packet.index}", "", "Claim:", "", f"> {packet.claim_text}", ""]
    if packet.chains:
        parts.append("Derivations the claim names:")
        parts.append("")
        for c in packet.chains:
            if c.via == "cited":
                how = "named by the claim"
            elif c.via == "ledger":
                how = "paired with this claim by the document's own closure ledger"
            elif c.via.startswith("composed-by:"):
                how = (
                    "included because "
                    f"{c.via.split(':', 1)[1]}'s first line builds on it"
                )
            else:
                how = (
                    "included because "
                    f"{c.via.split(':', 1)[1]} refers to it"
                )
            parts.append(f"{c.chain_id} ({how}):")
            parts.append("")
            parts.append(c.text)
            parts.append("")
    else:
        parts.append("Derivations the claim names: none of the document's derivations is named.")
        parts.append("")
    if packet.unresolved_refs:
        defined = ", ".join(packet.all_chain_ids) if packet.all_chain_ids else "none"
        parts.append(
            "Note: the claim refers to "
            + ", ".join(packet.unresolved_refs)
            + ", for which the document defines no derivation. The derivations it "
            f"defines are: {defined}."
        )
        parts.append("")
    if packet.ground_truths:
        parts.append("Stated facts those derivations rest on:")
        parts.append("")
        for gt_id, body in packet.ground_truths:
            parts.append(body)
            parts.append("")
    else:
        parts.append("Stated facts those derivations rest on: none is named by their first lines.")
        parts.append("")
    return "\n".join(parts).rstrip() + "\n"


def build_prompt(packets: list[ClaimPacket]) -> str:
    """Assemble the full judge prompt for one document's judgeable packets.

    The packets are renumbered 1..N for the prompt so the item numbers the
    judge answers against are contiguous; `judgeable_packets` keeps the
    mapping back to the document's own claim indices.
    """
    judgeable = judgeable_packets(packets)
    if not judgeable:
        raise ValueError("no judgeable claim packets: nothing to ask")
    renumbered = [p._replace(index=i) for i, p in enumerate(judgeable, start=1)]
    body = "\n".join(render_packet(p) for p in renumbered)
    return f"{PROMPT_HEADER}\n\n---\n\n{body}"


def judgeable_packets(packets: list[ClaimPacket]) -> list[ClaimPacket]:
    return [p for p in packets if p.judgeable]


# --- blinding (Task 2) ------------------------------------------------------


class ForbiddenTerm(NamedTuple):
    """One term the assembled prompt may not contain, with its pattern and reason."""

    label: str
    pattern: str
    why: str


# Every entry bars a phrase that would tell the judge what the reading is for,
# or that its input is known-wrong. Scoping is measured, not guessed -- see the
# module docstring's (a) and (b) for the two families deliberately narrowed and
# the shipped lines that forced each narrowing.
FORBIDDEN_TERMS: tuple[ForbiddenTerm, ...] = (
    ForbiddenTerm("adversarial", r"adversarial", "names the probe set's purpose"),
    ForbiddenTerm(
        "adversarial-corpus", r"adversarial-corpus", "the probe directory's own name"
    ),
    ForbiddenTerm(
        "deliberately false", r"deliberately\s+false", "states the input is wrong"
    ),
    ForbiddenTerm(
        "deliberately wrong", r"deliberately\s+wrong", "states the input is wrong"
    ),
    ForbiddenTerm(
        "substantively wrong", r"substantively\s+wrong", "states the input is wrong"
    ),
    ForbiddenTerm(
        "catalogued falsehood",
        r"catalogued\s+falsehood",
        "states a falsehood is recorded for this input",
    ),
    ForbiddenTerm(
        "catalog.md",
        r"catalog\.md",
        "the sidecar holding the expected answer; bare `catalog` is NOT barred -- "
        "it occurs in honest product prose (composed-inversion-second-order.md, "
        "self-application.md)",
    ),
    ForbiddenTerm(
        "never quote as fact",
        r"never\s+quote\s+as\s+fact",
        "the probe marker's own warning line",
    ),
    ForbiddenTerm("corpus", r"\bcorpus\b", "names the probe set"),
    ForbiddenTerm(
        "stratum", r"\bstrat(?:um|a)\b", "names the probe set's reachability labels"
    ),
    ForbiddenTerm(
        "false-negative", r"false[\s-]negatives?\b", "names the rate being measured"
    ),
    ForbiddenTerm(
        "positive control", r"positive\s+control", "would flag which items must fire"
    ),
    ForbiddenTerm(
        "probe-item filename t0",
        r"\bt0\d",
        "a probe item's filename prefix, which encodes its catalogued defect",
    ),
    ForbiddenTerm(
        "probe-item filename t1n",
        r"\bt1[1-4]-",
        "a probe item's filename prefix, which encodes its catalogued defect",
    ),
    ForbiddenTerm(
        "detector name", r"detect_defects", "names the instrument and its frame"
    ),
    ForbiddenTerm(
        "planted defect",
        r"\b(?:planted|injected|seeded)\s+(?:defect|error|flaw|falsehood)",
        "states the input is wrong",
    ),
    ForbiddenTerm(
        "known defect", r"known\s+(?:defect|falsehood)", "states the input is wrong"
    ),
    ForbiddenTerm(
        "fixture (adversarial)",
        r"adversarial\s+fixture",
        "the probe marker's own label; bare `fixture` is NOT barred -- it occurs in "
        "honest product prose (science-engineering.md prices LED fixtures)",
    ),
    ForbiddenTerm(
        "what is false",
        r"what\s+is\s+false\s+(?:about|in|here)",
        "asks the judge to confirm rather than to judge",
    ),
)

_COMPILED_FORBIDDEN = tuple(
    (t, re.compile(t.pattern, re.IGNORECASE)) for t in FORBIDDEN_TERMS
)


def blinding_problems(prompt: str) -> list[str]:
    """Return one problem line per forbidden term found in the assembled prompt.

    Checked over the WHOLE assembled prompt -- template and packet content
    together -- because a leak that arrives through the document's own bytes
    (a warning banner prepended to a file, say) blinds the reading exactly as
    badly as a leak written into the template.
    """
    problems: list[str] = []
    for term, rx in _COMPILED_FORBIDDEN:
        m = rx.search(prompt)
        if m:
            start = max(0, m.start() - 40)
            context = prompt[start : m.end() + 40].replace("\n", " ")
            problems.append(
                f"forbidden term {term.label!r} (pattern {term.pattern!r}) present: "
                f"...{context}... -- {term.why}"
            )
    return problems


class PromptNotBlindError(ValueError):
    """Raised when an assembled prompt carries a forbidden term."""


def assert_blinded(prompt: str, *, checker: Callable[[str], list[str]] | None = None) -> None:
    """Raise `PromptNotBlindError` if the assembled prompt is not blind.

    `checker` is injectable so the self-test can prove a weakened check is
    caught; every production call site uses the default.
    """
    check = checker or blinding_problems
    problems = check(prompt)
    if problems:
        raise PromptNotBlindError(
            "assembled judge prompt is not blind; refusing to invoke:\n  "
            + "\n  ".join(problems)
        )


# The template alone must be blind too, checked at import time the way the
# quality harness checks `JUDGE_PROMPT`. A leak written into the template is a
# leak on every document at once.
if blinding_problems(PROMPT_HEADER):
    raise RuntimeError(
        "PROMPT_HEADER carries a forbidden term: "
        + "; ".join(blinding_problems(PROMPT_HEADER))
    )


# --- verdict parsing --------------------------------------------------------

_VERDICT_BLOCK_RE = re.compile(
    re.escape(_VERDICT_START) + r"\n(?P<body>.*?)\n?" + re.escape(_VERDICT_END),
    re.DOTALL,
)
_ITEM_LINE_RE = re.compile(
    r"^ITEM-(?P<n>\d+)\s*:\s*(?P<verdict>[A-Za-z][A-Za-z-]*)\s*(?:--|—|-)?\s*(?P<reason>.*)$"
)


class Verdict(NamedTuple):
    item: int
    value: str
    reason: str


def parse_verdicts(response: str, expected: int) -> list[Verdict]:
    """Parse the sentinel-delimited verdict block into `expected` verdicts.

    Every failure mode collapses to UNPARSEABLE for the item concerned rather
    than to an exception or a silent default, so a malformed response is
    visible in the tabulation instead of being scored as agreement.
    """
    unparsed = [Verdict(i, UNPARSEABLE, "") for i in range(1, expected + 1)]
    m = _VERDICT_BLOCK_RE.search(response)
    if not m:
        return unparsed
    found: dict[int, Verdict] = {}
    for line in m.group("body").splitlines():
        lm = _ITEM_LINE_RE.match(line.strip())
        if not lm:
            continue
        n = int(lm.group("n"))
        value = lm.group("verdict").strip().upper()
        if value not in _VERDICT_VOCAB:
            continue
        if n in found:
            # A duplicated item number is a malformed block, not a re-vote.
            found[n] = Verdict(n, UNPARSEABLE, "duplicate item line")
            continue
        found[n] = Verdict(n, value, lm.group("reason").strip())
    return [found.get(i, Verdict(i, UNPARSEABLE, "")) for i in range(1, expected + 1)]


# --- judging one document ---------------------------------------------------

JudgeFn = Callable[[str], str]


class ClaimResult(NamedTuple):
    claim_index: int
    claim_text: str
    cited: tuple[str, ...]
    unresolved: tuple[str, ...]
    verdict: str
    reason: str


class DocResult(NamedTuple):
    label: str
    claims_total: int
    excluded_uncited: int
    results: tuple[ClaimResult, ...]
    error: str = ""


def judge_document(
    label: str,
    analysis_text: str,
    judge: JudgeFn,
    *,
    extractor: Callable[[str], list[ClaimPacket]] | None = None,
    blind_checker: Callable[[str], list[str]] | None = None,
) -> DocResult:
    """Extract, ask, parse -- for one document.

    `extractor` and `blind_checker` are injectable so the self-test can prove
    a degenerate extractor and a weakened blinding check are both caught.
    Production callers pass neither.
    """
    extract = extractor or extract_packets
    try:
        packets = extract(analysis_text)
    except Exception as exc:  # SectionResolutionError and anything else
        return DocResult(label, 0, 0, (), f"{type(exc).__name__}: {exc}")
    judgeable = judgeable_packets(packets)
    excluded = len(packets) - len(judgeable)
    if not judgeable:
        return DocResult(label, len(packets), excluded, (), "no judgeable claim")
    prompt = build_prompt(packets)
    try:
        assert_blinded(prompt, checker=blind_checker)
    except PromptNotBlindError as exc:
        return DocResult(label, len(packets), excluded, (), str(exc))
    response = judge(prompt)
    verdicts = parse_verdicts(response, len(judgeable))
    results = tuple(
        ClaimResult(
            claim_index=p.index,
            claim_text=p.claim_text,
            cited=tuple(c.chain_id for c in p.chains),
            unresolved=p.unresolved_refs,
            verdict=v.value,
            reason=v.reason,
        )
        for p, v in zip(judgeable, verdicts)
    )
    return DocResult(label, len(packets), excluded, results)


def live_judge(captures_dir: Path) -> JudgeFn:
    """A judge backed by one `claude -p` invocation per document.

    `--plugin-dir` is omitted, so the judge has no agent-dispatch surface, and
    `extract_judge_verdict` raises if the capture shows an Agent dispatch
    anyway. Both come from the quality harness, imported and called.
    """
    counter = {"n": 0}

    def judge(prompt: str) -> str:
        counter["n"] += 1
        out = captures_dir / f"judge-{counter['n']:02d}.jsonl"
        QH._run_prompt_to(prompt, out, plugin_dir=None, cwd=captures_dir)
        try:
            return QH.extract_judge_verdict(out)
        except ValueError as exc:
            return f"[extraction failed: {exc}]"

    return judge


# --- report rendering -------------------------------------------------------


def _excerpt(text: str, width: int = 72) -> str:
    one = " ".join(text.split())
    return one if len(one) <= width else one[: width - 1] + "…"


def render_report(docs: list[DocResult]) -> str:
    """Render the reading. Always states N, and never states a rate as a gate."""
    lines: list[str] = ["# Claim-to-chain correspondence -- a judged reading", ""]
    judged = sum(len(d.results) for d in docs)
    lines.append(
        f"N = {len(docs)} document(s), {judged} judged claim(s). "
        "This is an observation, not a gate: `docs/v8.7-constraint-teardown.md` "
        "section 2 item 3 bars a K-of-N live result from gating a phase, and this "
        "tool is registered in no CI job and no battery entry."
    )
    lines.append("")
    lines.append(
        "Each verdict answers one question -- does the derivation this claim "
        "names establish it -- over the claim, the named derivations and their "
        "stated facts, and nothing else."
    )
    lines.append("")

    totals = {v: 0 for v in (*_VERDICT_VOCAB, UNPARSEABLE)}
    excluded = 0
    for d in docs:
        excluded += d.excluded_uncited
        lines.append(f"## {d.label}")
        lines.append("")
        if d.error and not d.results:
            lines.append(f"Not judged: {d.error}")
            lines.append("")
            continue
        lines.append("| Claim | Names | Unresolved | Verdict | Reason |")
        lines.append("|---|---|---|---|---|")
        for r in d.results:
            totals[r.verdict] = totals.get(r.verdict, 0) + 1
            cited = ", ".join(QH._normalize_chain_id(c).upper() for c in r.cited) or "--"
            unres = ", ".join(r.unresolved) or "--"
            lines.append(
                f"| {_excerpt(r.claim_text, 60)} | {cited} | {unres} | "
                f"{r.verdict} | {_excerpt(r.reason, 90) or '--'} |"
            )
        lines.append("")
        if d.excluded_uncited:
            lines.append(
                f"Excluded from judging: {d.excluded_uncited} claim(s) naming no "
                "derivation at all -- the case `untraced_claims` already covers."
            )
            lines.append("")

    lines.append("## Totals")
    lines.append("")
    for v in (*_VERDICT_VOCAB, UNPARSEABLE):
        lines.append(f"- {v}: {totals.get(v, 0)}")
    lines.append(
        f"- excluded (names no derivation; `untraced_claims`' case): {excluded}"
    )
    lines.append("")
    lines.append(
        "A DOES-NOT-SUPPORT count here is a count of claims one judge read as "
        "unestablished by the derivation they name. It is not a defect count "
        "and not a precision or recall figure: establishing either would need "
        "a set of analyses whose substantive correctness has been "
        "independently adjudicated, which this project does not have."
    )
    lines.append("")
    return "\n".join(lines)


# ===========================================================================
# --self-test (Task 3)
# ===========================================================================
#
# Offline: no `claude`, no network, no write into `tests/`. The scripted judge
# below stands in for the live model. Every expectation in FIXTURES is
# hand-transcribed from reading the fixture document, never computed from the
# code under test -- CONF-GATE's CR-02(a) found every fixture in another gate
# deriving its expected value from the constant it checked, which left that
# gate green with all its floors at 0.

_FIX_SOUND = """
# A document

Preamble prose that no section owns.

## 1. Problem Essence

**Core problem:** whether to add a second checkout worker.

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| Queue depth is the binding constraint | untested belief | Verify | Challenge | measured |

## 3. Ground Truths

- **GT-1** The checkout queue holds a mean of 40 jobs and a p99 of 900 jobs.
  -- source: direct measurement (the queue's own depth metric, 30 days).
- **GT-2** One worker clears 12 jobs per minute at steady state.
  -- source: direct measurement (worker throughput counter, 30 days).

## 4. Derivation Chains

### Conclusion C1: a second worker halves the p99 drain time

GT-1 (queue depth measured) + GT-2 (per-worker throughput measured)
-> A p99 depth of 900 jobs drains in 75 minutes on one worker at 12 jobs per minute
-> Two workers clear 24 jobs per minute, so the same p99 depth drains in about
   38 minutes, halving the worst-case drain

**Confidence:** HIGH

### Conclusion C2: the queue metric is the right thing to watch

GT-1 (queue depth measured)
-> Depth is recorded continuously and is the only signal that leads the incident
-> Watching depth rather than worker CPU gives the earliest warning

**Confidence:** MEDIUM

## 5. Abandoned Reasoning

### Dead End: buy a bigger machine

**Why abandoned:** vertical scaling does not change per-worker throughput.

## 6. Conclusion

**Recommended approach:** (chain C1) Add a second checkout worker, which halves the
worst-case drain time from about 75 minutes to about 38 minutes.

**Key insight:** (chain C2) Queue depth, not worker CPU, is the signal that leads
the incident and so the one to alert on.
"""

_FIX_WRONG_CHAIN = """
# A document

## 1. Problem Essence

**Core problem:** whether to add a second checkout worker.

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| Queue depth is the binding constraint | untested belief | Verify | Challenge | measured |

## 3. Ground Truths

- **GT-1** The checkout queue holds a mean of 40 jobs and a p99 of 900 jobs.
  -- source: direct measurement (the queue's own depth metric, 30 days).
- **GT-2** One worker clears 12 jobs per minute at steady state.
  -- source: direct measurement (worker throughput counter, 30 days).

## 4. Derivation Chains

### Conclusion C1: a second worker halves the p99 drain time

GT-1 (queue depth measured) + GT-2 (per-worker throughput measured)
-> A p99 depth of 900 jobs drains in 75 minutes on one worker at 12 jobs per minute
-> Two workers clear 24 jobs per minute, so the same p99 depth drains in about
   38 minutes, halving the worst-case drain

**Confidence:** HIGH

### Conclusion C2: the queue metric is the right thing to watch

GT-1 (queue depth measured)
-> Depth is recorded continuously and is the only signal that leads the incident
-> Watching depth rather than worker CPU gives the earliest warning

**Confidence:** MEDIUM

## 5. Abandoned Reasoning

### Dead End: buy a bigger machine

**Why abandoned:** vertical scaling does not change per-worker throughput.

## 6. Conclusion

**Recommended approach:** (chain C2) Add a second checkout worker, which halves the
worst-case drain time from about 75 minutes to about 38 minutes.

**Key insight:** (chain C1) Queue depth, not worker CPU, is the signal that leads
the incident and so the one to alert on.
"""

_FIX_UNRESOLVED = """
# A document

## 1. Problem Essence

**Core problem:** whether to add a second checkout worker.

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| Queue depth is the binding constraint | untested belief | Verify | Challenge | measured |

## 3. Ground Truths

- **GT-1** The checkout queue holds a mean of 40 jobs and a p99 of 900 jobs.
  -- source: direct measurement (the queue's own depth metric, 30 days).

## 4. Derivation Chains

### Conclusion C1: a second worker halves the p99 drain time

GT-1 (queue depth measured)
-> A p99 depth of 900 jobs drains in 75 minutes on one worker
-> A second worker halves that worst-case drain

**Confidence:** HIGH

## 5. Abandoned Reasoning

### Dead End: buy a bigger machine

**Why abandoned:** vertical scaling does not change per-worker throughput.

## 6. Conclusion

**Recommended approach:** (chain C1) Add a second checkout worker.

**Key insight:** (chain C7) The cost comparison remains favourable at current prices.

- Queue depth should be alerted on rather than worker CPU.
"""

_FIX_CYCLE = """
# A document

## 1. Problem Essence

**Core problem:** whether to add a third on-call engineer.

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| Rotation load is the binding constraint | untested belief | Verify | Challenge | measured |

## 3. Ground Truths

- **GT-1** The payments rotation pages 14 times a week on a two-person roster.
  -- source: direct measurement (the pager's own event log, 12 weeks).

## 4. Derivation Chains

### Conclusion C1: the rotation needs a third engineer

GT-1 (page volume measured) + C2 (backlog is unsustainable)
-> The roster carries 7 pages per person per week
-> A third engineer is required, because the review backlog C2 establishes is
   unsustainable at that page volume

**Confidence:** HIGH

### Conclusion C2: the review backlog is unsustainable

C1 (a third engineer is required)
-> Reviews queue behind paging work
-> The backlog is unsustainable, since the rotation needs the third engineer C1
   establishes

**Confidence:** HIGH

## 5. Abandoned Reasoning

### Dead End: outsource the rotation

**Why abandoned:** an outside roster cannot hold the service context.

## 6. Conclusion

**Recommended approach:** (chain C1) Add a third engineer to the payments rotation.

**Key insight:** (chain C2) The review backlog is the cost the rotation is paying.
"""

# Hard-wrapped section-6 prose, the shape every shipped exemplar uses. Claim 1's
# sentence runs across three physical lines; claim 2's chain citation sits on a
# CONTINUATION line, so it is invisible to a line-scoped citation scan.
_FIX_WRAPPED_CLAIMS = """
# A document

## 1. Problem Essence

**Core problem:** whether to add a second checkout worker.

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| Queue depth is the binding constraint | untested belief | Verify | Challenge | measured |

## 3. Ground Truths

- **GT-1** The checkout queue holds a p99 of 900 jobs -- source: direct measurement.
- **GT-2** One worker clears 12 jobs per minute -- source: direct measurement.

## 4. Derivation Chains

### Conclusion C1: a second worker halves the p99 drain time

GT-1 (queue depth measured) + GT-2 (per-worker throughput measured)
-> A p99 depth of 900 jobs drains in 75 minutes on one worker
-> Two workers clear 24 jobs a minute, halving that worst case to about 38 minutes

**Confidence:** HIGH

### Conclusion C2: the queue metric is the right thing to watch

GT-1 (queue depth measured)
-> Depth is recorded continuously and leads the incident
-> Watching depth rather than worker CPU gives the earliest warning

**Confidence:** MEDIUM

## 5. Abandoned Reasoning

### Dead End: buy a bigger machine

**Why abandoned:** vertical scaling does not change per-worker throughput.

## 6. Conclusion

**Recommended approach:** (chain C1) Add a second checkout worker, taking the
worst-case drain from about 75 minutes to about 38 minutes and thereby
halving the worst-case drain to about 38 minutes.

**Key insight:** Queue depth, not worker CPU, is the signal that leads the
incident, and so the one to alert on (chain C2).
"""

# The 999.35 shape: the cross-reference is stated in the prose UNDER each head,
# not in the head itself, so `_chain_head_refs` returns no chain ref for either
# block and head-driven expansion yields nothing. Transcribed in shape (not in
# content) from `t06-hidden-cycle-past-head.md`, the catalogued item this was
# measured against.
_FIX_PROSE_LOOP = """
# A document

## 1. Problem Essence

**Core problem:** whether the new fee schedule is a net gain.

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| The fee change is net-positive | untested belief | Verify | Challenge | measured |

## 3. Ground Truths

- **GT-1** Per-transaction net revenue rose from $0.34 to $0.41 over four weeks.
  -- source: direct measurement (the ledger's own per-transaction record).
- **GT-2** Pricing-attributed cancellations rose from 6 a week to 14 a week.
  -- source: direct measurement (the cancellation reason codes, 12 weeks).

## 4. Derivation Chains

### Conclusion C1: the revenue gain is real and material

GT-1 (per-transaction revenue rose)
-> The $0.07 per-transaction increase across measured volume is material
-> The fee change is producing a measurable revenue gain

This gain is only worth keeping once the retention picture in C2 is weighed against
it, and C2's own loss figure is itself calculated by assuming the fee change in this
chain stays in place.

**Confidence:** MEDIUM

### Conclusion C2: the churn loss is a real and growing cost

GT-2 (cancellations rose)
-> The extra 8 cancellations a week carry a recurring revenue loss
-> The churn loss is a growing cost of keeping the schedule

This loss is a fair comparison against C1's gain only once that gain is confirmed to
persist, since the loss computed here presumes the schedule C1 justifies keeping.

**Confidence:** MEDIUM

## 5. Abandoned Reasoning

### Dead End: raise fees further

**Why abandoned:** the cancellation trend is already the binding cost.

## 6. Conclusion

**Recommended approach:** (chain C1) Keep the new fee schedule.
"""

_FIX_LEAKY = """
# A document

## 1. Problem Essence

**Core problem:** whether to add a second checkout worker.

## 2. Assumptions Table

| Assumption | Type | Treatment | Verdict | Verification |
|---|---|---|---|---|
| Queue depth is the binding constraint | untested belief | Verify | Challenge | measured |

## 3. Ground Truths

- **GT-1** The checkout queue holds a p99 of 900 jobs -- source: direct measurement.

## 4. Derivation Chains

### Conclusion C1: a second worker halves the p99 drain time

GT-1 (queue depth measured)
-> A p99 depth of 900 jobs drains in 75 minutes on one worker
-> A second worker halves that worst-case drain (ADVERSARIAL FIXTURE, do not trust)

**Confidence:** HIGH

## 5. Abandoned Reasoning

### Dead End: buy a bigger machine

**Why abandoned:** vertical scaling does not change per-worker throughput.

## 6. Conclusion

**Recommended approach:** (chain C1) Add a second checkout worker. This document is DELIBERATELY FALSE; see catalog.md for the catalogued falsehood and its stratum.
"""


class ClaimExpectation(NamedTuple):
    """One hand-written expectation about a fixture's claim.

    `phrase` is a distinctive substring of the claim as the fixture writes it;
    the scripted judge keys on it, so an extractor that mis-orders or
    mis-attributes claims sends the canned answers to the wrong items and the
    fixture fails. `names` is the chains the claim should be found to name.
    `verdict` is what a correct reading of THIS fixture yields, read by hand
    from the fixture's own text -- not computed from anything here.
    """

    phrase: str
    names: tuple[str, ...]
    unresolved: tuple[str, ...]
    verdict: str


class Fixture(NamedTuple):
    name: str
    text: str
    claims_total: int
    excluded: int
    expectations: tuple[ClaimExpectation, ...]
    note: str


FIXTURES: tuple[Fixture, ...] = (
    Fixture(
        "sound",
        _FIX_SOUND,
        claims_total=2,
        excluded=0,
        expectations=(
            ClaimExpectation("Add a second checkout worker", ("Conclusion C1",), (), SUPPORTS),
            ClaimExpectation("Queue depth, not worker CPU", ("Conclusion C2",), (), SUPPORTS),
        ),
        note="each claim names the chain that reaches it; a correct reading is all SUPPORTS",
    ),
    Fixture(
        "swapped-citations",
        _FIX_WRONG_CHAIN,
        claims_total=2,
        excluded=0,
        expectations=(
            ClaimExpectation(
                "Add a second checkout worker", ("Conclusion C2",), (), DOES_NOT_SUPPORT
            ),
            ClaimExpectation(
                "Queue depth, not worker CPU", ("Conclusion C1",), (), DOES_NOT_SUPPORT
            ),
        ),
        note=(
            "byte-identical to `sound` except that the two citations are swapped -- the "
            "LEDGER-01 family, and the case every citation-presence route reads clean"
        ),
    ),
    Fixture(
        "unresolved-reference",
        _FIX_UNRESOLVED,
        claims_total=3,
        excluded=1,
        expectations=(
            ClaimExpectation("Add a second checkout worker", ("Conclusion C1",), (), SUPPORTS),
            ClaimExpectation(
                "The cost comparison remains favourable", (), ("C7",), DOES_NOT_SUPPORT
            ),
        ),
        note=(
            "one claim names a chain the document never defines (reported, not dropped); "
            "one names nothing at all and is excluded as `untraced_claims`' case"
        ),
    ),
    Fixture(
        "mutual-composition",
        _FIX_CYCLE,
        claims_total=2,
        excluded=0,
        expectations=(
            ClaimExpectation(
                "Add a third engineer",
                ("Conclusion C1", "Conclusion C2"),
                (),
                DOES_NOT_SUPPORT,
            ),
            ClaimExpectation(
                "The review backlog is the cost",
                ("Conclusion C2", "Conclusion C1"),
                (),
                DOES_NOT_SUPPORT,
            ),
        ),
        note=(
            "each chain's head builds on the other, so bounded transitive expansion puts "
            "both blocks in each packet and the mutual dependence is readable prose -- the "
            "999.35 shape, reached without widening any frozen read window (D-1)"
        ),
    ),
)

# The scripted judge's canned answers, keyed on the PAIR the judge actually
# reads: a distinctive phrase from the claim, and the derivations the packet put
# in front of it. Keying on the claim alone would be the one mistake that makes
# this whole suite vacuous -- `swapped-citations` is byte-identical to `sound`
# except for which chain each claim names, so a claim-only key answers both
# fixtures identically and the suite could not tell a correct extraction from
# one that hands over the wrong chain. That is exactly the defect the tool
# exists to find, so the mock has to be sensitive to it.
_SCRIPTED: dict[tuple[str, tuple[str, ...]], tuple[str, str]] = {
    ("Add a second checkout worker, which halves", ("C1",)): (
        SUPPORTS,
        "the derivation reaches the halved drain time the claim states",
    ),
    ("Add a second checkout worker, which halves", ("C2",)): (
        DOES_NOT_SUPPORT,
        "the derivation shown concerns which signal to watch, not drain time",
    ),
    ("Queue depth, not worker CPU", ("C2",)): (
        SUPPORTS,
        "the derivation reaches depth as the leading signal",
    ),
    ("Queue depth, not worker CPU", ("C1",)): (
        DOES_NOT_SUPPORT,
        "the derivation shown concerns drain time, not which signal leads",
    ),
    ("Add a second checkout worker.", ("C1",)): (
        SUPPORTS,
        "the derivation reaches the second worker",
    ),
    ("The cost comparison remains favourable", ()): (
        DOES_NOT_SUPPORT,
        "the named derivation is not defined in the material",
    ),
    ("Add a third engineer", ("C1", "C2")): (
        DOES_NOT_SUPPORT,
        "the two derivations rest on each other with nothing underneath",
    ),
    ("The review backlog is the cost", ("C2", "C1")): (
        DOES_NOT_SUPPORT,
        "the two derivations rest on each other with nothing underneath",
    ),
}

# Longest phrase first: "Add a second checkout worker." is a prefix-collision
# with "Add a second checkout worker, which halves".
_SCRIPTED_PHRASES = tuple(sorted({k[0] for k in _SCRIPTED}, key=len, reverse=True))

_ITEM_SPLIT_RE = re.compile(r"^### Item (\d+)$", re.MULTILINE)
_PACKET_CLAIM_RE = re.compile(r"^> (.+)$", re.MULTILINE)
_PACKET_CHAIN_RE = re.compile(
    r"^(.+?) \((?:named by the claim|paired with this claim|included because)",
    re.MULTILINE,
)


def _read_items(prompt: str) -> list[tuple[str, str, tuple[str, ...]]]:
    """Read back `(item number, claim text, chain labels)` from an assembled prompt.

    Deliberately parses the prompt rather than taking the packets directly:
    what the judge can answer from is what the prompt says, so the mock reads
    the same surface the model would.
    """
    parts = _ITEM_SPLIT_RE.split(prompt)
    items: list[tuple[str, str, tuple[str, ...]]] = []
    # parts == [preamble, n1, body1, n2, body2, ...]
    for i in range(1, len(parts) - 1, 2):
        number, body = parts[i], parts[i + 1]
        cm = _PACKET_CLAIM_RE.search(body)
        claim = cm.group(1) if cm else ""
        chains = tuple(
            QH._normalize_chain_id(m.group(1)).upper()
            for m in _PACKET_CHAIN_RE.finditer(body)
        )
        items.append((number, claim, chains))
    return items


def scripted_judge(prompt: str) -> str:
    """A judge answering from `_SCRIPTED`, keyed on each item's (claim, chains) pair.

    Stands in for the live model offline. Because the key includes the chains
    the packet handed over, an extractor that drops a chain, hands over the
    wrong one, reorders items or empties a packet cannot be answered correctly
    -- which is what makes the empty-packet injection bite, and what makes the
    swapped-citation fixture discriminating.
    """
    lines = []
    for number, claim, chains in _read_items(prompt):
        answer = None
        for phrase in _SCRIPTED_PHRASES:
            if phrase in claim:
                answer = _SCRIPTED.get((phrase, chains))
                break
        if answer is None:
            lines.append(
                f"ITEM-{number}: {UNDECIDABLE} -- no scripted answer for this "
                "claim/derivation pair"
            )
        else:
            lines.append(f"ITEM-{number}: {answer[0]} -- {answer[1]}")
    return (
        "Reading each item in turn.\n\n"
        + f"{_VERDICT_START}\n"
        + "\n".join(lines)
        + f"\n{_VERDICT_END}\n"
    )


def always_supports(prompt: str) -> str:
    """Anti-masking control: a judge that never finds a claim unsupported."""
    n = len(re.findall(r"### Item \d+", prompt))
    body = "\n".join(f"ITEM-{i}: {SUPPORTS} -- looks fine" for i in range(1, n + 1))
    return f"{_VERDICT_START}\n{body}\n{_VERDICT_END}\n"


def always_does_not_support(prompt: str) -> str:
    """Anti-masking control: a judge that finds every claim unsupported."""
    n = len(re.findall(r"### Item \d+", prompt))
    body = "\n".join(
        f"ITEM-{i}: {DOES_NOT_SUPPORT} -- looks wrong" for i in range(1, n + 1)
    )
    return f"{_VERDICT_START}\n{body}\n{_VERDICT_END}\n"


def empty_extractor(_analysis_text: str) -> list[ClaimPacket]:
    """Anti-masking control: an extractor that finds no claim in any document."""
    return []


def never_leaks(_prompt: str) -> list[str]:
    """Anti-masking control: a blinding check weakened to always pass."""
    return []


# --- self-test control groups ----------------------------------------------


def fixture_problems(
    judge: JudgeFn,
    extractor: Callable[[str], list[ClaimPacket]] | None = None,
) -> list[str]:
    """Run FIXTURES end to end and return one line per mismatch.

    Parameterised on the judge and the extractor so a degenerate one can be
    injected and shown to fail.
    """
    problems: list[str] = []
    for fx in FIXTURES:
        got = judge_document(fx.name, fx.text, judge, extractor=extractor)
        if got.error and not got.results:
            problems.append(f"{fx.name}: not judged ({got.error})")
            continue
        if got.claims_total != fx.claims_total:
            problems.append(
                f"{fx.name}: expected {fx.claims_total} claim(s), found {got.claims_total}"
            )
        if got.excluded_uncited != fx.excluded:
            problems.append(
                f"{fx.name}: expected {fx.excluded} excluded claim(s), "
                f"found {got.excluded_uncited}"
            )
        if len(got.results) != len(fx.expectations):
            problems.append(
                f"{fx.name}: expected {len(fx.expectations)} judged claim(s), "
                f"found {len(got.results)}"
            )
            continue
        for exp, res in zip(fx.expectations, got.results):
            if exp.phrase not in res.claim_text:
                problems.append(
                    f"{fx.name}: expected a claim containing {exp.phrase!r}, "
                    f"got {_excerpt(res.claim_text)!r}"
                )
                continue
            if res.cited != exp.names:
                problems.append(
                    f"{fx.name}/{exp.phrase!r}: expected to name {exp.names!r}, "
                    f"found {res.cited!r}"
                )
            if res.unresolved != exp.unresolved:
                problems.append(
                    f"{fx.name}/{exp.phrase!r}: expected unresolved {exp.unresolved!r}, "
                    f"found {res.unresolved!r}"
                )
            if res.verdict != exp.verdict:
                problems.append(
                    f"{fx.name}/{exp.phrase!r}: expected {exp.verdict}, got {res.verdict}"
                )
    return problems


def blinding_control_problems(checker: Callable[[str], list[str]] | None = None) -> list[str]:
    """Prove the blinding assertion FIRES on a leaky prompt and not on clean ones.

    Three legs:
      (a) a deliberately-leaky document assembles a prompt the check rejects,
          and `assert_blinded` raises on it;
      (b) each forbidden term, spliced into an otherwise clean prompt on its
          own, is caught -- so no entry in the list is dead;
      (c) every clean fixture prompt passes.
    """
    check = checker or blinding_problems
    problems: list[str] = []

    leaky_prompt = build_prompt(extract_packets(_FIX_LEAKY))
    found = check(leaky_prompt)
    if not found:
        problems.append(
            "the leaky-prompt control was NOT caught -- the blinding assertion "
            "cannot see a leak arriving through the document's own bytes"
        )
    else:
        try:
            assert_blinded(leaky_prompt, checker=check)
            problems.append(
                "blinding_problems reported a leak but assert_blinded did not raise"
            )
        except PromptNotBlindError:
            pass

    clean = build_prompt(extract_packets(_FIX_SOUND))
    for term, _rx in _COMPILED_FORBIDDEN:
        probe = clean + "\n\n" + _term_example(term)
        if not check(probe):
            problems.append(
                f"forbidden term {term.label!r} is dead: its own example text "
                "is not caught by the check"
            )

    for fx in FIXTURES:
        prompt = build_prompt(extract_packets(fx.text))
        leaks = check(prompt)
        if leaks:
            problems.append(f"clean fixture {fx.name} reads as leaky: {leaks[0]}")
    return problems


# One example string per forbidden term, used by leg (b) above to prove no
# entry in the list is dead. Hand-written to match each pattern; a term whose
# example does not match its own pattern is itself a failure.
_TERM_EXAMPLES: dict[str, str] = {
    "adversarial": "this is an adversarial probe",
    "adversarial-corpus": "see tests/adversarial-corpus-v9.0/",
    "deliberately false": "the content is deliberately false",
    "deliberately wrong": "the content is deliberately wrong",
    "substantively wrong": "form-clean and substantively wrong",
    "catalogued falsehood": "a catalogued falsehood lives here",
    "catalog.md": "per catalog.md row 4",
    "never quote as fact": "never quote as fact",
    "corpus": "one item of the corpus",
    "stratum": "this item's stratum is A",
    "false-negative": "the false-negative rate",
    "positive control": "a positive control item",
    "probe-item filename t0": "t06-hidden-cycle-past-head.md",
    "probe-item filename t1n": "t13-grounded-alongside-cyclic-ref.md",
    "detector name": "scored under detect_defects",
    "planted defect": "a planted defect sits in section 4",
    "known defect": "a known defect is present",
    "fixture (adversarial)": "ADVERSARIAL FIXTURE",
    "what is false": "say what is false about this",
}


def _term_example(term: ForbiddenTerm) -> str:
    return _TERM_EXAMPLES[term.label]


def structure_problems() -> list[str]:
    """Controls over the fixture table and the term list themselves.

    These are the anti-vacuity guards. A fixture suite whose expectations were
    all one verdict value could not catch an always-that-value judge, and a
    term list with no example could not prove a term live. Both are asserted
    here rather than assumed.
    """
    problems: list[str] = []

    expected_values = {
        e.verdict for fx in FIXTURES for e in fx.expectations
    }
    for required in (SUPPORTS, DOES_NOT_SUPPORT):
        if required not in expected_values:
            problems.append(
                f"no fixture expects {required}: the suite cannot catch a judge "
                f"stubbed to return {required} unconditionally"
            )
    if not any(fx.excluded for fx in FIXTURES):
        problems.append(
            "no fixture exercises the excluded-uncited path, so the exclusion rule "
            "is unmeasured"
        )
    if not any(e.unresolved for fx in FIXTURES for e in fx.expectations):
        problems.append(
            "no fixture exercises an unresolved chain-shaped reference, so the "
            "'says so rather than silently dropping it' requirement is unmeasured"
        )
    if not any(len(e.names) > 1 for fx in FIXTURES for e in fx.expectations):
        problems.append(
            "no fixture exercises transitive composition expansion, so disclosed "
            "bound (g) is unmeasured"
        )

    names = [fx.name for fx in FIXTURES]
    if len(set(names)) != len(names):
        problems.append(f"duplicate fixture name in {names}")

    # Anti-vacuity guard on the MOCK, not just on the tool. At least one claim
    # phrase must appear in `_SCRIPTED` under two different chain tuples with
    # two different verdicts -- otherwise the mock is answering from the claim
    # alone, the swapped-citation fixture becomes indistinguishable from the
    # sound one, and the suite silently stops testing whether the extractor
    # hands over the right chain. This is CONF-GATE's CR-02(a) failure mode
    # (a control deriving its expectation from the thing it checks) rewritten
    # for a mock.
    by_phrase: dict[str, set[tuple[tuple[str, ...], str]]] = {}
    for (phrase, chains), (verdict, _reason) in _SCRIPTED.items():
        by_phrase.setdefault(phrase, set()).add((chains, verdict))
    discriminating = [
        phrase
        for phrase, entries in by_phrase.items()
        if len({c for c, _v in entries}) > 1 and len({v for _c, v in entries}) > 1
    ]
    if not discriminating:
        problems.append(
            "no claim phrase in _SCRIPTED is answered differently for two "
            "different chain sets: the mock is keyed on the claim alone and the "
            "suite cannot detect a wrong chain being handed to the judge"
        )
    for (phrase, _chains) in _SCRIPTED:
        if phrase not in _SCRIPTED_PHRASES:
            problems.append(f"_SCRIPTED phrase {phrase!r} missing from _SCRIPTED_PHRASES")

    labels = [t.label for t in FORBIDDEN_TERMS]
    if len(set(labels)) != len(labels):
        problems.append(f"duplicate forbidden-term label in {labels}")
    missing_examples = sorted(set(labels) - set(_TERM_EXAMPLES))
    if missing_examples:
        problems.append(f"forbidden terms with no example: {missing_examples}")
    stray_examples = sorted(set(_TERM_EXAMPLES) - set(labels))
    if stray_examples:
        problems.append(f"examples for no registered term: {stray_examples}")
    for term in FORBIDDEN_TERMS:
        if not term.why.strip():
            problems.append(f"forbidden term {term.label!r} carries no reason")

    # The plan's named minimum coverage, asserted by matching each required
    # phrase against the live term list rather than by counting entries.
    required_coverage = (
        "adversarial",
        "corpus",
        "stratum",
        "deliberately false",
        "t06-hidden-cycle-past-head.md",
        "catalog.md",
        "false-negative",
    )
    for phrase in required_coverage:
        if not blinding_problems(phrase):
            problems.append(
                f"required blinding coverage missing: {phrase!r} is not caught"
            )

    for value in _VERDICT_VOCAB:
        if value not in PROMPT_HEADER:
            problems.append(f"PROMPT_HEADER never offers the verdict value {value!r}")
    if UNDECIDABLE not in _VERDICT_VOCAB:
        problems.append("UNDECIDABLE is not in the verdict vocabulary")
    return problems


_PARSE_CASES: tuple[tuple[str, str, int, tuple[str, ...]], ...] = (
    (
        "well-formed",
        f"prose\n{_VERDICT_START}\nITEM-1: {SUPPORTS} -- fine\n"
        f"ITEM-2: {DOES_NOT_SUPPORT} -- wrong chain\n{_VERDICT_END}\n",
        2,
        (SUPPORTS, DOES_NOT_SUPPORT),
    ),
    (
        "em-dash separator",
        f"{_VERDICT_START}\nITEM-1: {UNDECIDABLE} — not enough given\n{_VERDICT_END}",
        1,
        (UNDECIDABLE,),
    ),
    (
        "no sentinel block",
        f"ITEM-1: {SUPPORTS} -- fine",
        1,
        (UNPARSEABLE,),
    ),
    (
        "unterminated block",
        f"{_VERDICT_START}\nITEM-1: {SUPPORTS} -- fine\n",
        1,
        (UNPARSEABLE,),
    ),
    (
        "off-vocabulary verdict",
        f"{_VERDICT_START}\nITEM-1: MOSTLY-SUPPORTS -- hedged\n{_VERDICT_END}",
        1,
        (UNPARSEABLE,),
    ),
    (
        "short by one item",
        f"{_VERDICT_START}\nITEM-1: {SUPPORTS} -- fine\n{_VERDICT_END}",
        2,
        (SUPPORTS, UNPARSEABLE),
    ),
    (
        "duplicate item number",
        f"{_VERDICT_START}\nITEM-1: {SUPPORTS} -- fine\n"
        f"ITEM-1: {DOES_NOT_SUPPORT} -- no\n{_VERDICT_END}",
        1,
        (UNPARSEABLE,),
    ),
    (
        "lowercase verdict is normalised",
        f"{_VERDICT_START}\nITEM-1: supports -- fine\n{_VERDICT_END}",
        1,
        (SUPPORTS,),
    ),
    (
        "reason omitted",
        f"{_VERDICT_START}\nITEM-1: {SUPPORTS}\n{_VERDICT_END}",
        1,
        (SUPPORTS,),
    ),
    (
        "trailing prose after the block is ignored",
        f"{_VERDICT_START}\nITEM-1: {DOES_NOT_SUPPORT} -- no\n{_VERDICT_END}\nafterword",
        1,
        (DOES_NOT_SUPPORT,),
    ),
)


def parse_problems() -> list[str]:
    problems: list[str] = []
    for name, response, expected_n, expected in _PARSE_CASES:
        got = tuple(v.value for v in parse_verdicts(response, expected_n))
        if got != expected:
            problems.append(f"parse case {name}: expected {expected}, got {got}")
    return problems


def packet_problems() -> list[str]:
    """Controls over extraction itself, independent of any judge.

    Asserts the Task-1 verify conditions directly: every cited chain id
    appears in the packet, no uncited one does, and a claim citing a
    nonexistent chain yields a packet that says so.
    """
    problems: list[str] = []

    packets = extract_packets(_FIX_SOUND)
    if len(packets) != 2:
        problems.append(f"sound fixture: expected 2 packets, got {len(packets)}")
    first = packets[0]
    ids = [c.chain_id for c in first.chains]
    if ids != ["Conclusion C1"]:
        problems.append(f"sound/claim-1: expected only Conclusion C1, got {ids}")
    gt_ids = [g[0] for g in first.ground_truths]
    if gt_ids != ["GT-1", "GT-2"]:
        problems.append(f"sound/claim-1: expected GT-1 and GT-2 in packet, got {gt_ids}")
    rendered = render_packet(first)
    if "halving the worst-case drain" not in rendered:
        problems.append("sound/claim-1: the cited chain's body is not in the packet")
    if "only signal that leads the incident" in rendered:
        problems.append("sound/claim-1: an UNCITED chain's body leaked into the packet")
    if "12 jobs per minute at steady state" not in rendered:
        problems.append("sound/claim-1: a head-named ground truth is missing from the packet")
    if "Assumptions Table" in rendered or "Dead End" in rendered:
        problems.append("sound/claim-1: material beyond claim/chains/facts leaked in")

    unresolved = extract_packets(_FIX_UNRESOLVED)
    hits = [p for p in unresolved if p.unresolved_refs]
    if len(hits) != 1 or hits[0].unresolved_refs != ("C7",):
        problems.append(
            f"unresolved fixture: expected exactly one packet naming C7, got "
            f"{[p.unresolved_refs for p in unresolved]}"
        )
    else:
        text = render_packet(hits[0])
        if "C7" not in text or "defines no derivation" not in text:
            problems.append(
                "unresolved fixture: the packet does not state that the named "
                "derivation is undefined"
            )
    silent = [p for p in unresolved if not p.judgeable]
    if len(silent) != 1:
        problems.append(
            f"unresolved fixture: expected 1 claim naming nothing, got {len(silent)}"
        )

    cyc = extract_packets(_FIX_CYCLE)
    got_ids = [tuple(c.chain_id for c in p.chains) for p in cyc]
    if got_ids != [("Conclusion C1", "Conclusion C2"), ("Conclusion C2", "Conclusion C1")]:
        problems.append(
            f"cycle fixture: expected each packet to carry both blocks, got {got_ids}"
        )
    vias = {c.via for p in cyc for c in p.chains}
    if not any(v.startswith("composed-by:") for v in vias):
        problems.append("cycle fixture: head-driven transitive expansion never fired")

    # Disclosed bound (h): the prose-stated loop. Head-driven expansion alone
    # must find nothing here -- asserted, so a later edit cannot quietly make
    # this fixture pass through the head path and leave the body path
    # unmeasured -- and the body-driven hop must supply the other block.
    loop = extract_packets(_FIX_PROSE_LOOP)
    if len(loop) != 1:
        problems.append(f"prose-loop fixture: expected 1 claim, got {len(loop)}")
    else:
        got = [(c.chain_id, c.via) for c in loop[0].chains]
        if got != [("Conclusion C1", "cited"), ("Conclusion C2", "referenced-by:C1")]:
            problems.append(
                "prose-loop fixture: expected C1 cited plus C2 pulled in by a body "
                f"reference, got {got}"
            )
        rendered = render_packet(loop[0])
        if "C1 refers to it" not in rendered:
            problems.append(
                "prose-loop fixture: the packet does not disclose HOW the second "
                "block arrived"
            )
        if "the loss computed here presumes the schedule" not in rendered:
            problems.append(
                "prose-loop fixture: the other side of the dependence is not in the "
                "packet, so the judge cannot see both halves of the loop"
            )
    for block in QH._chain_blocks(QH._slice_sections(_FIX_PROSE_LOOP)[4]):
        _gts, refs = QH._chain_head_refs(block)
        if refs:
            problems.append(
                "prose-loop fixture no longer states its cross-reference past the "
                f"head line ({refs!r} is head-visible), so it no longer exercises "
                "disclosed bound (h)"
            )

    # Claim completion. Two properties, both load-bearing: the population is
    # identical to `_conclusion_claims`' on every fixture, and a wrapped claim
    # arrives as a whole sentence rather than a fragment.
    for fx_text, label in (
        (_FIX_SOUND, "sound"),
        (_FIX_WRAPPED_CLAIMS, "wrapped"),
        (_FIX_UNRESOLVED, "unresolved"),
        (_FIX_CYCLE, "cycle"),
        (_FIX_PROSE_LOOP, "prose-loop"),
    ):
        s6 = QH._slice_sections(fx_text)[6]
        ids = QH._chain_ids(QH._slice_sections(fx_text)[4])
        raw = QH._conclusion_claims(s6, ids)
        done = complete_claims(s6, raw)
        if len(done) != len(raw):
            problems.append(
                f"complete_claims changed the claim population on {label}: "
                f"{len(raw)} -> {len(done)}"
            )
            continue
        for r, d in zip(raw, done):
            if not d.startswith(r):
                problems.append(
                    f"complete_claims on {label} did not preserve the detector's own "
                    f"claim text as a prefix: {r!r} -> {d!r}"
                )

    wrapped = extract_packets(_FIX_WRAPPED_CLAIMS)
    if len(wrapped) != 2:
        problems.append(f"wrapped fixture: expected 2 claims, got {len(wrapped)}")
    else:
        first = wrapped[0].claim_text
        if "halving the worst-case drain to about 38 minutes." not in first:
            problems.append(
                "wrapped fixture: the claim still arrives cut mid-sentence "
                f"({first!r}) -- a fragment is not a claim a support question can "
                "be asked about"
            )
        if "\n" in first:
            problems.append("wrapped fixture: the completed claim was not unwrapped")
        # The citation sits on a continuation line, so this also proves the
        # widened citation window the docstring discloses under (c).
        if [c.chain_id for c in wrapped[1].chains] != ["Conclusion C2"]:
            problems.append(
                "wrapped fixture: a citation on a continuation line was not found, "
                f"got {[c.chain_id for c in wrapped[1].chains]}"
            )
    # The fixture must actually BE wrapped, or it stops exercising any of this.
    raw_wrapped = QH._conclusion_claims(
        QH._slice_sections(_FIX_WRAPPED_CLAIMS)[6],
        QH._chain_ids(QH._slice_sections(_FIX_WRAPPED_CLAIMS)[4]),
    )
    if not any(not re.search(r"[.!?]$", c.strip()) for c in raw_wrapped):
        problems.append(
            "wrapped fixture is no longer hard-wrapped mid-sentence, so it no "
            "longer exercises complete_claims"
        )

    # Ground-truth entry parsing, including the `?`-marked form.
    entries = ground_truth_entries(
        "- **GT-1** first -- source: a.\n- **GT-2?** second -- source: b.\n\n---\n"
    )
    if [e[0] for e in entries] != ["GT-1", "GT-2?"]:
        problems.append(f"ground_truth_entries: got {[e[0] for e in entries]}")
    if entries and entries[-1][1].endswith("-"):
        problems.append("ground_truth_entries: a trailing horizontal rule leaked into an entry")

    # A claim naming `GT-C1` must not read as naming chain C1 (the masking rule).
    masked = _GT_TOKEN_MASK_RE.sub(" ", "grounded in GT-C1 alone")
    if _CHAIN_SHAPED_REF_RE.search(masked):
        problems.append("GT masking failed: `GT-C1` read as a reference to chain C1")
    return problems


def emission_problems() -> list[str]:
    """Controls over the report: it states N, and states no rate as a gate."""
    problems: list[str] = []
    docs = [judge_document(fx.name, fx.text, scripted_judge) for fx in FIXTURES]
    report = render_report(docs)
    judged = sum(len(d.results) for d in docs)
    if f"N = {len(docs)} document(s), {judged} judged claim(s)." not in report:
        problems.append("render_report does not state its N")
    for value in (*_VERDICT_VOCAB, UNPARSEABLE):
        if f"- {value}:" not in report:
            problems.append(f"render_report omits the {value} total")
    for phrase in (
        "not a gate",
        "not a precision or recall figure",
        "independently adjudicated",
    ):
        if phrase not in report:
            problems.append(f"render_report omits the required disclosure {phrase!r}")
    if blinding_problems(report):
        problems.append("the report itself carries a forbidden term")
    return problems


def harness_surface_problems() -> list[str]:
    """Confirm this tool only calls the harness, and calls what it claims to.

    A name that moved or disappeared in the harness would otherwise surface as
    an AttributeError mid-reading. Nothing here writes to the module.
    """
    problems: list[str] = []
    required = (
        "_slice_sections",
        "_chain_ids",
        "_chain_blocks",
        "_chain_head_refs",
        "_conclusion_claims",
        "_cites_chain",
        "_normalize_chain_id",
        "_ledger_fragment_covers",
        "_STRUCTURAL_LEDGER_ROW_RE",
        "_run_prompt_to",
        "extract_judge_verdict",
        "_ensure_claude_available",
    )
    for name in required:
        if not hasattr(QH, name):
            problems.append(f"check-quality-harness.py no longer provides {name!r}")
    # `_claim_is_traced` is the presence-only function this tool exists beside.
    # Asserting the gap concretely: the swapped-citation fixture's claims are
    # all traced under it, which is why a support reading is needed at all.
    if hasattr(QH, "_claim_is_traced"):
        sections = QH._slice_sections(_FIX_WRONG_CHAIN)
        ids = QH._chain_ids(sections[4])
        blocks = QH._chain_blocks(sections[4])
        for claim in QH._conclusion_claims(sections[6], ids):
            if not QH._claim_is_traced(claim, ids, blocks):
                problems.append(
                    "the swapped-citation fixture is NOT fully traced under "
                    "_claim_is_traced, so it does not demonstrate the gap this "
                    "tool fills; rewrite the fixture"
                )
    else:
        problems.append("check-quality-harness.py no longer provides _claim_is_traced")
    return problems


# --- injections -------------------------------------------------------------
#
# Each injection degrades exactly one component and MUST make the self-test
# fail. `--inject NAME` runs the whole self-test with it active, so the failure
# is demonstrable as a non-zero exit rather than asserted in prose.

INJECTIONS: tuple[str, ...] = (
    "always-supports",
    "always-does-not-support",
    "empty-packet",
    "weak-blinding",
)


def _run_controls(injection: str | None) -> list[str]:
    """Run every control group, with `injection` (if any) active."""
    judge: JudgeFn = scripted_judge
    extractor: Callable[[str], list[ClaimPacket]] | None = None
    blind: Callable[[str], list[str]] | None = None

    if injection == "always-supports":
        judge = always_supports
    elif injection == "always-does-not-support":
        judge = always_does_not_support
    elif injection == "empty-packet":
        extractor = empty_extractor
    elif injection == "weak-blinding":
        blind = never_leaks
    elif injection is not None:
        raise SystemExit(f"error: unknown injection {injection!r}; one of {INJECTIONS}")

    problems: list[str] = []
    problems += [f"[structure] {p}" for p in structure_problems()]
    problems += [f"[harness] {p}" for p in harness_surface_problems()]
    problems += [f"[packet] {p}" for p in packet_problems()]
    problems += [f"[parse] {p}" for p in parse_problems()]
    problems += [f"[blinding] {p}" for p in blinding_control_problems(blind)]
    problems += [f"[fixture] {p}" for p in fixture_problems(judge, extractor)]
    problems += [f"[emission] {p}" for p in emission_problems()]
    return problems


def self_test(injection: str | None = None) -> int:
    problems = _run_controls(injection)

    if injection is None:
        # Anti-masking: every injection must be caught by the controls above.
        # An injection the suite passes means the suite cannot see that
        # component failing, which is the CONF-GATE CR-02(a) failure mode.
        for name in INJECTIONS:
            caught = _run_controls(name)
            if caught:
                print(
                    f"[anti-masking] {name}: CAUGHT as designed "
                    f"({len(caught)} control failure(s)); first: {caught[0]}"
                )
            else:
                problems.append(
                    f"[anti-masking] injection {name!r} PASSED the control suite -- "
                    "the suite cannot detect that component failing"
                )

    print(
        f"fixtures: {len(FIXTURES)}; forbidden terms: {len(FORBIDDEN_TERMS)}; "
        f"parse cases: {len(_PARSE_CASES)}; injections: {len(INJECTIONS)}"
    )
    if problems:
        for p in problems:
            print(f"FAIL {p}", file=sys.stderr)
        label = f" (injection: {injection})" if injection else ""
        print(f"SELF-TEST: FAIL ({len(problems)} problems){label}", file=sys.stderr)
        return 1
    if injection:
        print(
            f"SELF-TEST: PASS with injection {injection!r} -- this is a FAILURE of the "
            "control suite, which should have caught it",
            file=sys.stderr,
        )
        return 1
    print("SELF-TEST: PASS")
    return 0


# --- CLI --------------------------------------------------------------------


def _collect_inputs(args: argparse.Namespace) -> list[Path]:
    paths: list[Path] = []
    for p in args.analysis or []:
        paths.append(Path(p))
    if args.dir:
        for f in sorted(Path(args.dir).glob("*.md")):
            if f.name in ("README.md", "catalog.md"):
                continue
            paths.append(f)
    return paths


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=(
            "Ask, per claim, whether the derivation chain it names supports it. "
            "A measurement, never a gate: registered in no CI job and no battery entry."
        )
    )
    ap.add_argument("--analysis", nargs="+", help="one or more analysis .md files")
    ap.add_argument("--dir", help="a directory of analysis .md files")
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="assemble and print the prompts, run the blinding assertion, invoke nothing",
    )
    ap.add_argument("--out", type=Path, help="write the report here instead of stdout")
    ap.add_argument(
        "--captures-out",
        type=Path,
        help="keep the live judge captures here (default: a temporary directory)",
    )
    ap.add_argument("--self-test", action="store_true", help="run the offline control suite")
    ap.add_argument(
        "--inject",
        choices=INJECTIONS,
        help="run the control suite with one component degraded; must exit non-zero",
    )
    args = ap.parse_args(argv)

    if args.inject:
        return self_test(args.inject)
    if args.self_test:
        return self_test()

    paths = _collect_inputs(args)
    if not paths:
        ap.error("one of --analysis, --dir, --self-test or --inject is required")

    if args.dry_run:
        for path in paths:
            text = path.read_text(encoding="utf-8")
            try:
                packets = extract_packets(text)
            except Exception as exc:
                print(f"# {path.name}: not measurable -- {type(exc).__name__}: {exc}")
                continue
            judgeable = judgeable_packets(packets)
            print(
                f"# {path.name}: {len(packets)} claim(s), {len(judgeable)} judgeable, "
                f"{len(packets) - len(judgeable)} naming no derivation"
            )
            if not judgeable:
                continue
            prompt = build_prompt(packets)
            assert_blinded(prompt)
            print(f"# prompt: {len(prompt)} chars, blinding assertion passed")
            print(prompt)
            print()
        return 0

    QH._ensure_claude_available()
    tmp: tempfile.TemporaryDirectory | None = None
    if args.captures_out:
        captures = args.captures_out
        captures.mkdir(parents=True, exist_ok=True)
    else:
        tmp = tempfile.TemporaryDirectory(prefix="claim-chain-judge-")
        captures = Path(tmp.name)
    tests_dir = (REPO_ROOT / "tests").resolve()
    if captures.resolve() == tests_dir or tests_dir in captures.resolve().parents:
        raise SystemExit(
            "error: refusing to write captures under tests/ -- FROZEN-EVIDENCE sweeps "
            "that tree for untracked files"
        )

    judge = live_judge(captures)
    docs: list[DocResult] = []
    for path in paths:
        # Sequential by construction: one invocation per document, in order.
        print(f"judging {path.name} ...", file=sys.stderr)
        docs.append(judge_document(path.name, path.read_text(encoding="utf-8"), judge))
    report = render_report(docs)

    if args.out is None:
        sys.stdout.write(report)
    else:
        out = args.out.resolve()
        if out == tests_dir or tests_dir in out.parents:
            raise SystemExit("error: refusing to write the report under tests/")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report, encoding="utf-8")
        print(f"wrote {out}")
    if tmp is not None:
        tmp.cleanup()
    return 0


if __name__ == "__main__":
    sys.exit(main())
