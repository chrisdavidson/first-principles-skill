#!/usr/bin/env python3
"""Structural check on the template-only provenance roll-up (backlog 999.173).

What this reads, and why that artifact
--------------------------------------
`shared/spine/references/output-template.md:129-134` prescribes a two-line
provenance roll-up at the end of section 3:

    ?-marked: GT-2, GT-5, GT-9, GT-14 (4 of 22)
    Read-at-source: GT-3 — 45 CFR 164.514(b)(2)(i), subsections (A)/(B)/(R) quoted verbatim

That form is measured **template-only** -- 0 occurrences in
`shared/spine/SKILL-body.md`, 0 across all `shared/references/*.md`, 0 across
all `shared/examples/*.md`, 1 in the template -- and emitted in 12 of 15 live
captures read at quick task `260924-tcv`. So an emitted artifact traceable to
the template alone exists; nothing looked for it. This tool looks for it.

That template-only claim is a factual claim about this tree, so it ships with a
falsifier rather than with prose: `template_only_problems()` re-derives the
four counts above from the working tree on every `--self-test` and FAILS if any
of them has moved. It is a deliberate tripwire, not an incidental control. If a
later change prescribes the roll-up in the agent body, this checker stops
measuring what it claims to measure, and the self-test must say so loudly
instead of continuing to pass. That is exactly the mechanism that destroyed
backlog 999.90: `**Confidence:**` and the unverified-input rule were both
absorbed into `SKILL-body.md` after 999.90 nominated `**Confidence:**` as a
template-only form, and its candidate silently stopped proving anything.

**Nothing here prescribes the roll-up anywhere.** A detector reads output. This
module adds not one word to `shared/`, to the agent body, or to any shipped
surface, and its own `--self-test` fails if someone else does.

Why this is not a presence check
--------------------------------
`CLAUDE.md` § "Claims and falsifiers" bars the shape this repository shipped
seven blocking defects behind: `grep -c '<literal>' <file> == N`, which asks
only whether a string appears. The template itself names the difference, at
`:136`:

> A stated integer does not satisfy this -- an integer cannot be checked
> against the list it summarizes, and an enumeration can. Where a count and
> its enumeration disagree, **the enumeration governs.**

So the roll-up carries a count `(N of M)` **and** the enumeration it
summarises, and both can be cross-checked against the `GT-N` population in the
document's own list of ground truths. That is what check 2 below does. It
cannot be satisfied by emitting the label, and it fails for a real reason.

The checks, and which of them can fail
--------------------------------------
1. **Presence** -- is the roll-up emitted at all? **REPORT ONLY. Never fails,
   on any input.** Emission rate is an N=15 observation, and
   `docs/v8.7-constraint-teardown.md` §2 item 3 bars a K-of-N live reading from
   gating anything -- measured on the S-P04 vector swinging 2/5 -> 0/5 -> 2/5
   with no source change between readings.
2. **Enumeration agreement** -- when the roll-up is present: the ids it
   enumerates are exactly the `?`-suffixed ground truths in section 3, `M`
   equals the section-3 ground-truth population, and `N` equals the length of
   the enumeration beside it. **FAILING CHECK.** This is the one worth having.
3. **Read-at-source coverage** -- when the roll-up is present: every unsuffixed
   ground truth feeding a HIGH-confidence chain is named, with a location, on a
   `Read-at-source:` line of the roll-up. **REPORT ONLY -- downgraded from a
   failing check on measurement, see "Why check 3 is report-only" below.**

Per the template's rule, check 2 resolves a count/enumeration disagreement by
believing the enumeration: the section-3 comparison always runs against the
enumerated ids, never against the integer. The integer disagreeing with the
list it summarises is reported as its own finding, because a disagreement is
the very thing `:136` legislates about.

The anti-masking case that matters
----------------------------------
An empty section-3 population would make every enumeration agree vacuously and
check 2 would pass on everything -- a control invariant to the thing it checks,
the CONF-GATE CR-02(a) shape. So a present roll-up over an **empty** section-3
population is a check-2 FAILURE here, never a pass: agreement that cannot be
evaluated is not assumed. `--inject empty-ground-truths` degrades the section-3
parser to return nothing and must exit non-zero.

The sibling quick task `260924-jdg` hit this trap live: its first mock judge
keyed on claim text alone and the `always-SUPPORTS` injection PASSED. No
fixture expectation in this file is derived from the parser under test -- every
expected id set is hand-transcribed beside its fixture text.

What check 2 was measured to do
-------------------------------
Stated with its N, and with what it did NOT do.

Over 45 documents across eight capture directories under `tests/`, 21 carried a
roll-up and **check 2 found no disagreement in any of them**. So the honest
claim is not "it catches real defects in the corpus"; it is that the corpus's
roll-ups agree with their own ground-truth list, and that the check can fail.

That it can fail is shown by mutation rather than by fixtures alone.
`tests/baseline-reading-v9.6/Q-P1.md` passes; four independent single-point
mutations of its roll-up each make check 2 fire, and the unmutated control still
passes:

| mutation | finding |
|---|---|
| `(7 of 9)` -> `(7 of 10)` | stated M is 10, the population is 9 |
| drop `GT-7` from the enumeration | `?`-marked in section 3 but absent from the enumeration: gt-7 |
| add unsuffixed `GT-8` to the enumeration | enumerated but not `?`-marked in section 3: gt-8 |
| replace the list with a prose integer | every marked id absent from the enumeration; a stated N against an enumeration of none |

The final table row above is what `output-template.md:136` legislates about, and
fixture `integer-not-a-list` pins it offline.

Why check 3 is report-only
--------------------------
Measured, not assumed. "Feeds a HIGH-confidence chain" is resolved through
`_chain_head_refs`, which reads a chain's **head line only** -- the
CONTRACT-06-frozen read window backlog 999.35 asked to widen and was refused
(that request needs a written amendment to the milestone goal before the diff,
and no such amendment exists; this tool authors none). Three reasons follow, all
observed on the live corpus rather than reasoned about -- the first two from
that read window and the grammar of the line, the third from the prescription
itself:

(a) A ground truth cited in a chain's body but not its head is invisible, so
    the check silently under-reports. That direction is safe for a gate.
(b) The `Read-at-source:` line has no prescribed grammar, and the corpus uses
    at least four shapes for it: per-id (`GT-1 — Lambda pricing page, ...`),
    grouped (`GT-1, GT-2, GT-4 — Lambda pricing page, quoted`), a numeric
    range (`GT-1..GT-5 — definitional terminus`), and running prose (`GT-2 and
    GT-3 are definitional, stated in full above`). Segmenting a location per
    identifier across those shapes is a judgement, not a parse. That direction
    is NOT safe for a gate: it invents findings.

(c) **The decisive one, and it is about the prescription, not the parse.** The
    template at `:129` asks the ROLL-UP to name the location. Every ground-truth
    ENTRY already carries its own `read-at-source:` field (`:114`), and the
    corpus overwhelmingly names the location there and does not repeat it on the
    roll-up line. Measured over the same 45 documents: 3 documents produce
    check-3 observations, 19 observations in total, and **17 of those 19 name a
    read-at-source location in the ground truth's own section-3 entry.** So a
    strict reading of `:129` would fail those documents over where the location
    is written, not over whether it exists. Whether the per-entry field
    discharges the roll-up's naming duty is a reading of the prescription that
    the template does not settle and this tool has no standing to settle.

Shipping (b) or (c) as a failing check would mean gating on a heuristic reading
of free prose, or on one side of an ambiguity in the prescription itself. The
plan for this task admits the downgrade explicitly -- "if determining 'feeds a
HIGH-confidence chain' proves unreliable, downgrade this check to report-only
and say so rather than shipping a check you cannot trust." It is said here, and
(c) is why: the 17-of-19 reading is the finding, and it says the observations
are mostly about placement.

The observations are still worth emitting. The 2 of 19 that are NOT located in
their own entry either are genuine unnamed provenance on a HIGH chain, and a
reader can adjudicate each from the report.

Disclosed bounds
----------------
(a) **Registered as PROV-ROLLUP** in `scripts/check-firewall-battery.sh` and in
    `.github/workflows/validation.yml` (backlog 999.173's registration
    residual). It shipped registered nowhere, and `structure_problems()` then
    asserted that non-registration, because it was a claim the shipping task
    made about its own scope. Registration retires both of those assertions
    rather than inverting them: REG-GUARD already derives "every id the battery
    registers has a matching CI job" from the battery's own source text, and
    restating it here would be the second grammar over one file that
    REG-GUARD's own D-01 floor note forbids. The third assertion --- that no
    file under `shared/` names this script --- is 999.90's trap guard, is
    unaffected by registration, and stays.
(b) **The roll-up is located inside section 3 only**, via the frozen
    `_slice_sections`. A roll-up emitted elsewhere in a document is not found,
    and the document reads as ABSENT (report-only, so nothing fails).
(c) **A `**Pre-check:**` line is not a roll-up.** That per-chain line is
    body-prescribed and also carries a `?-marked:` fragment -- it occurs on
    shipped surfaces (`shared/examples/estimate-fermi.md`,
    `shared/examples/product-business-2.md`,
    `shared/references/reason-upward.md`). The line-start anchor in
    `_ROLLUP_MARKED_RE` excludes it, and control `roll-up/pre-check` pins that.
(d) **The `?` suffix is a provenance label, not part of an identity.** Ids are
    compared `?`-insensitively, because the corpus writes the enumeration both
    ways (`GT-1, GT-2, ...` against section-3 `GT-1?, GT-2?, ...` in
    `tests/baseline-reading-v9.6/Q-P1.md`; suffixed in
    `tests/confidence-transitivity-v9.4/CT-A1.md`). **Section 3 is the sole
    authority on which ground truths carry the label** -- a roll-up cannot
    grant itself agreement by writing or omitting a `?`.
(e) **Section 3 is read outside fenced code.** The roll-up itself is often
    inside a ```text fence; ground-truth ENTRIES are the unfenced bullets. Both
    readings use the harness's own CommonMark fence tracker
    (`_fenced_code_flags`), not a parity toggle.
(f) **A document whose six sections do not resolve is reported unreadable, not
    clean.** `_slice_sections` raises rather than returning a partial slice, and
    that exception is surfaced per document. An unreadable document fails no
    check -- it is counted and named.

Nothing in `check-quality-harness.py` is modified. Every function used from it
is called: `_slice_sections`, `_chain_head_refs`, `_chain_ids`, `_chain_blocks`,
`_chain_confidence_label`, `_normalize_chain_id` and `_fenced_code_flags`. The
first two are frozen under CONTRACT-06.

Usage:
    python3 scripts/check-provenance-rollup.py --analysis FILE [FILE ...]
    python3 scripts/check-provenance-rollup.py --dir shared/examples
    python3 scripts/check-provenance-rollup.py --self-test
    python3 scripts/check-provenance-rollup.py --inject empty-ground-truths
    python3 scripts/check-provenance-rollup.py --describe   # CONF-SURFACE self-description

Exit codes:
    0  a reading completed with no failing-check finding, or --self-test passed
    1  a failing-check (check 2) finding, a --self-test failure (including
       under --inject), or a usage/IO error
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Callable, NamedTuple

REPO_ROOT = Path(__file__).resolve().parent.parent
_HARNESS_PATH = REPO_ROOT / "scripts" / "check-quality-harness.py"


# --- the imported, never-modified detector surface --------------------------


def _load_harness():
    """Import `check-quality-harness.py` as a module and return it.

    The filename carries hyphens, so it is not importable by name. Registered
    in `sys.modules` before `exec_module` because the harness defines frozen
    dataclasses and `dataclasses` resolves `cls.__module__` through
    `sys.modules` while processing them.

    Nothing in the loaded module is ever written to.
    """
    spec = importlib.util.spec_from_file_location("_qh_for_provenance_rollup", _HARNESS_PATH)
    if spec is None or spec.loader is None:
        raise SystemExit(f"error: cannot load {_HARNESS_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


QH = _load_harness()

# The harness names this module relies on. Asserted by
# `harness_surface_problems()` so a rename there is caught loudly instead of
# skipping a check silently.
_REQUIRED_HARNESS_NAMES: tuple[str, ...] = (
    "_slice_sections",
    "_chain_head_refs",
    "_chain_ids",
    "_chain_blocks",
    "_chain_confidence_label",
    "_normalize_chain_id",
    "_fenced_code_flags",
    "SectionResolutionError",
)


# --- section-3 ground-truth population --------------------------------------

# A section-3 ground-truth entry: a list item whose first bold span is a GT id.
# Up to three leading spaces, because CommonMark permits that much before a
# list marker and four or more makes an indented code block.
_GT_ENTRY_RE = re.compile(r"^ {0,3}[-*][ \t]+\*\*(GT-[A-Za-z0-9]+\??)\*\*")

# A GT token anywhere in running text. Deliberately this module's own symbol
# rather than a reuse of the harness's `_GT_TOKEN_WIDE`, because the two are
# scanning different things and a shared regex would couple a frozen detector's
# read window to this tool's.
_GT_TOKEN_RE = re.compile(r"GT-[A-Za-z0-9]+\??")

# A numeric id range on a Read-at-source line: `GT-1..GT-5`.
_GT_RANGE_RE = re.compile(r"GT-(\d+)[ \t]*\.\.[ \t]*GT-(\d+)")

# Ceiling on range expansion, so a typo (`GT-1..GT-99999`) cannot turn into an
# unbounded id set.
_MAX_RANGE_SPAN = 200


class GroundTruth(NamedTuple):
    """One section-3 ground truth.

    `written` is the id exactly as section 3 writes it (`GT-5?`), `key` its
    `?`-insensitive comparable form (`gt-5`), and `marked` whether it carries
    the `?` provenance suffix. Section 3 is the sole authority on `marked`
    (disclosed bound (d)).
    """

    written: str
    key: str
    marked: bool


def gt_key(raw: str) -> str:
    """Comparable form of a GT id: `?`-suffix dropped, case-folded."""
    return raw.strip().rstrip("?").casefold()


def section3_ground_truths(section3: str) -> list[GroundTruth]:
    """Return section 3's ground truths, in document order, deduplicated by id.

    Bullets inside a fenced code block are skipped: the roll-up itself is
    routinely fenced, and the template's own prose fences example forms. Fence
    tracking is the harness's CommonMark-correct `_fenced_code_flags`, not a
    parity toggle.

    A repeated id keeps its FIRST entry -- the template's rule is that ids are
    stable once assigned, so a second `**GT-5**` bullet is the same ground
    truth, not a second one. Repeats are surfaced separately by
    `duplicate_gt_ids()` rather than swallowed here.
    """
    lines = section3.splitlines()
    inside = QH._fenced_code_flags(lines)
    out: list[GroundTruth] = []
    seen: set[str] = set()
    for i, line in enumerate(lines):
        if inside[i]:
            continue
        m = _GT_ENTRY_RE.match(line)
        if m is None:
            continue
        written = m.group(1)
        key = gt_key(written)
        if key in seen:
            continue
        seen.add(key)
        out.append(GroundTruth(written, key, written.endswith("?")))
    return out


def duplicate_gt_ids(section3: str) -> list[str]:
    """Ids section 3 declares more than once, in document order of the repeat."""
    lines = section3.splitlines()
    inside = QH._fenced_code_flags(lines)
    seen: set[str] = set()
    dupes: list[str] = []
    for i, line in enumerate(lines):
        if inside[i]:
            continue
        m = _GT_ENTRY_RE.match(line)
        if m is None:
            continue
        key = gt_key(m.group(1))
        if key in seen and key not in dupes:
            dupes.append(key)
        seen.add(key)
    return dupes


# --- locating the roll-up ---------------------------------------------------

# The roll-up's first line. Anchored at line start (after optional indent and
# an optional wrapping backtick, both observed in the corpus) so that a
# `**Pre-check:**` line -- which also carries a `?-marked:` fragment, mid-line,
# and is body-prescribed -- can never match (disclosed bound (c)). The same
# anchor excludes a `?-marked:` fragment quoted inside prose.
_ROLLUP_MARKED_RE = re.compile(r"^ {0,3}`?[ \t]*\?-marked:[ \t]*(?P<body>.*?)[ \t]*`?[ \t]*$")

# The roll-up's `(N of M)` tail.
_ROLLUP_COUNT_RE = re.compile(r"\((?P<n>\d+)[ \t]+of[ \t]+(?P<m>\d+)\)[ \t]*$")

# A `Read-at-source:` line of the roll-up. The same line-start anchor: a
# `Read-at-source:` fragment inside an individual ground-truth ENTRY (observed
# in `tests/baseline-reading-v9.6/Q-P1.md`, indented under its bullet) is part
# of that entry, not part of the roll-up.
_ROLLUP_READ_RE = re.compile(r"^ {0,3}`?[ \t]*Read-at-source:[ \t]*(?P<body>.*?)[ \t]*`?[ \t]*$")

# A fenced-code delimiter, so the scan for the roll-up's Read-at-source lines
# can step over a closing fence without ending.
_FENCE_LINE_RE = re.compile(r"^ {0,3}(?:`{3,}|~{3,})")


class Rollup(NamedTuple):
    """A located provenance roll-up.

    `enumerated` holds the ids the `?-marked:` line names, as written, in order.
    `stated_n` / `stated_m` are the `(N of M)` integers, or None when the tail
    is absent. `read_lines` holds the roll-up's `Read-at-source:` line bodies.
    """

    marked_line: str
    enumerated: tuple[str, ...]
    stated_n: int | None
    stated_m: int | None
    read_lines: tuple[str, ...]

    @property
    def enumerated_keys(self) -> set[str]:
        return {gt_key(x) for x in self.enumerated}


def find_rollup(section3: str) -> Rollup | None:
    """Locate the provenance roll-up in a section-3 body, or return None.

    The roll-up's `Read-at-source:` lines are the run of such lines following
    the `?-marked:` line, stepping over blank lines and fence delimiters and
    stopping at the first other non-blank line. All four observed shapes of
    that line are captured verbatim; none is parsed here.
    """
    lines = section3.splitlines()
    idx: int | None = None
    body = ""
    for i, line in enumerate(lines):
        m = _ROLLUP_MARKED_RE.match(line)
        if m is not None:
            idx, body = i, m.group("body")
            break
    if idx is None:
        return None

    stated_n: int | None = None
    stated_m: int | None = None
    enum_part = body
    cm = _ROLLUP_COUNT_RE.search(body)
    if cm is not None:
        stated_n = int(cm.group("n"))
        stated_m = int(cm.group("m"))
        enum_part = body[: cm.start()]

    enumerated = tuple(_GT_TOKEN_RE.findall(enum_part))

    read_lines: list[str] = []
    for line in lines[idx + 1 :]:
        if not line.strip():
            continue
        if _FENCE_LINE_RE.match(line):
            continue
        rm = _ROLLUP_READ_RE.match(line)
        if rm is None:
            break
        read_lines.append(rm.group("body"))

    return Rollup(lines[idx].strip(), enumerated, stated_n, stated_m, tuple(read_lines))


# --- check 2: enumeration agreement (FAILING) -------------------------------


def enumeration_problems(rollup: Rollup, population: list[GroundTruth]) -> list[str]:
    """Check 2. Findings are failures; an empty list is agreement.

    Three comparisons, in this order:

    1. **The population must be non-empty.** A present roll-up over a section 3
       this tool read as empty is a FAILURE, not a pass. Every enumeration
       agrees vacuously with an empty set, so passing here would be a control
       invariant to the thing it checks -- the CONF-GATE CR-02(a) shape, and
       what `--inject empty-ground-truths` exists to demonstrate.
    2. **The enumerated ids are exactly section 3's `?`-marked ids**, compared
       `?`-insensitively and against section 3's own labelling (disclosed bound
       (d)). Reported in both directions: enumerated-but-not-marked, and
       marked-but-not-enumerated.
    3. **`M` equals the population size, and `N` equals the length of the
       enumeration.** Per `output-template.md:136` the enumeration governs, so
       comparison 2 above is never decided by an integer; a disagreeing integer
       is its own finding, because a stated integer that disagrees with the list
       it summarises is precisely what that line legislates about. A missing
       `(N of M)` tail is a finding too: the template prescribes it.
    """
    problems: list[str] = []

    if not population:
        problems.append(
            "the roll-up is present but section 3 yields no ground truths -- agreement "
            "cannot be evaluated and is not assumed (an empty population makes every "
            "enumeration agree vacuously)"
        )
        return problems

    marked = {g.key for g in population if g.marked}
    enumerated = rollup.enumerated_keys

    extra = sorted(enumerated - marked)
    missing = sorted(marked - enumerated)
    if extra:
        problems.append(
            f"enumerated but not `?`-marked in section 3: {', '.join(extra)}"
        )
    if missing:
        problems.append(
            f"`?`-marked in section 3 but absent from the enumeration: {', '.join(missing)}"
        )

    if rollup.stated_m is None or rollup.stated_n is None:
        problems.append(
            "the roll-up states no `(N of M)` count -- the template prescribes both the "
            "enumeration and the count"
        )
    else:
        if rollup.stated_m != len(population):
            problems.append(
                f"stated M is {rollup.stated_m}, section 3's ground-truth population "
                f"is {len(population)}"
            )
        if rollup.stated_n != len(enumerated):
            problems.append(
                f"stated N is {rollup.stated_n}, the enumeration beside it names "
                f"{len(enumerated)} id(s) -- the enumeration governs "
                "(output-template.md:136)"
            )

    return problems


# --- check 3: read-at-source coverage (REPORT ONLY) -------------------------


def high_chain_head_gts(section4: str) -> list[tuple[str, tuple[str, ...]]]:
    """Per HIGH-labelled chain: `(chain id, GT tokens in its head line)`.

    Confidence is read by the harness's `_chain_confidence_label` and head
    references by the frozen `_chain_head_refs`, which reads the head LINE only
    -- the window backlog 999.35 asked to widen and was refused. A ground truth
    cited past the head is therefore invisible here (disclosed bound, check-3
    consequence (a)), which under-reports and never over-reports.

    A section whose chain ids cannot be paired with its blocks is keyed by the
    pseudo-id `block-<n>`, mirroring `_confidence_defects`'s unpairable rule.
    """
    ids = QH._chain_ids(section4)
    blocks = QH._chain_blocks(section4)
    if ids and len(ids) == len(blocks):
        names = [QH._normalize_chain_id(i) for i in ids]
    else:
        names = [f"block-{i}" for i in range(1, len(blocks) + 1)]

    out: list[tuple[str, tuple[str, ...]]] = []
    for name, block in zip(names, blocks):
        if QH._chain_confidence_label(block) != "HIGH":
            continue
        gt_refs, _chain_refs = QH._chain_head_refs(block)
        out.append((name, tuple(sorted(gt_refs))))
    return out


def _expand_ranges(text: str) -> list[str]:
    """Ids named by a `GT-1..GT-5` range, expanded inclusively."""
    out: list[str] = []
    for lo_s, hi_s in _GT_RANGE_RE.findall(text):
        lo, hi = int(lo_s), int(hi_s)
        if lo > hi or hi - lo > _MAX_RANGE_SPAN:
            continue
        out.extend(f"GT-{n}" for n in range(lo, hi + 1))
    return out


def located_read_at_source(read_lines: tuple[str, ...]) -> set[str]:
    """Ids the roll-up's Read-at-source lines name WITH a location.

    Each line is split on `;` into segments -- the corpus's separator when one
    line carries several ids each with its own location. A segment's ids count
    as located when the segment carries a location tail: at least three word
    characters once its GT tokens, ranges and separator punctuation are removed.
    `Read-at-source: none — no source was cited` therefore locates nothing,
    because it names no id.

    This is a coarse reading of free prose and is why check 3 is report-only
    (see the module docstring, check-3 consequence (b)). It is stated rather
    than hidden: the segment rule cannot tell which of several ids a location
    belongs to, only that the segment has one.
    """
    located: set[str] = set()
    for line in read_lines:
        for segment in line.split(";"):
            ids = _GT_TOKEN_RE.findall(segment) + _expand_ranges(segment)
            if not ids:
                continue
            tail = _GT_RANGE_RE.sub(" ", segment)
            tail = _GT_TOKEN_RE.sub(" ", tail)
            tail = re.sub(r"[^0-9A-Za-z]+", " ", tail)
            if len(tail.replace(" ", "")) < 3:
                continue
            located.update(gt_key(i) for i in ids)
    return located


def coverage_observations(
    rollup: Rollup, population: list[GroundTruth], section4: str
) -> list[str]:
    """Check 3. Observations, never failures.

    For every HIGH-labelled chain, the unsuffixed ground truths in its head
    line -- unsuffixed per SECTION 3, which is the authority -- must be named
    with a location on a `Read-at-source:` line of the roll-up. A head id
    section 3 does not declare is reported as its own observation rather than
    folded into a coverage miss: that is a different defect, and not this
    tool's to adjudicate.
    """
    if not population:
        return [
            "not evaluated: section 3 yields no ground truths, so no input's "
            "provenance label can be resolved"
        ]

    by_key = {g.key: g for g in population}
    located = located_read_at_source(rollup.read_lines)

    observations: list[str] = []
    for chain_id, head_gts in high_chain_head_gts(section4):
        for token in head_gts:
            key = gt_key(token)
            gt = by_key.get(key)
            if gt is None:
                observations.append(
                    f"HIGH chain {chain_id} head cites {token}, which section 3 does "
                    "not declare"
                )
                continue
            if gt.marked:
                continue
            if key not in located:
                observations.append(
                    f"HIGH chain {chain_id} rests on unsuffixed {gt.written}, which no "
                    "`Read-at-source:` line of the roll-up names with a location"
                )
    return observations


# --- per-document reading ---------------------------------------------------


class DocReading(NamedTuple):
    """One document's reading. `unreadable` is set when sections do not resolve."""

    name: str
    unreadable: str | None
    present: bool
    rollup: Rollup | None
    population: int
    marked: int
    duplicates: tuple[str, ...]
    check2: tuple[str, ...]
    check3: tuple[str, ...]

    @property
    def failing(self) -> bool:
        """Whether this reading carries a FAILING-check finding.

        Check 2 only. Presence is report-only by policy and check 3 by
        measurement; neither can make a document fail.
        """
        return bool(self.check2)


# Swappable seams, so an injection degrades one component and the control
# suite has to notice. Module-level and rebound by `_run_controls`.
Section3Parser = Callable[[str], list[GroundTruth]]
Check2 = Callable[[Rollup, list[GroundTruth]], list[str]]

_SECTION3_PARSER: Section3Parser = section3_ground_truths
_CHECK2: Check2 = enumeration_problems


def read_document(name: str, text: str) -> DocReading:
    """Read one analysis document: presence, check 2, check 3."""
    try:
        sections = QH._slice_sections(text)
    except QH.SectionResolutionError as exc:
        return DocReading(name, str(exc), False, None, 0, 0, (), (), ())

    section3 = sections[3]
    section4 = sections[4]
    population = _SECTION3_PARSER(section3)
    dupes = tuple(duplicate_gt_ids(section3))
    marked = sum(1 for g in population if g.marked)

    rollup = find_rollup(section3)
    if rollup is None:
        return DocReading(
            name, None, False, None, len(population), marked, dupes, (), ()
        )

    check2 = tuple(_CHECK2(rollup, population))
    check3 = tuple(coverage_observations(rollup, population, section4))
    return DocReading(
        name, None, True, rollup, len(population), marked, dupes, check2, check3
    )


def render_report(readings: list[DocReading]) -> str:
    """Render the reading. Presence is a rate; check 2 is a verdict."""
    out: list[str] = []
    readable = [r for r in readings if r.unreadable is None]
    present = [r for r in readable if r.present]
    failing = [r for r in readable if r.failing]

    out.append("# Provenance roll-up reading (backlog 999.173)")
    out.append("")
    out.append(
        f"documents: {len(readings)}; readable: {len(readable)}; "
        f"roll-up present: {len(present)}; check-2 failures: {len(failing)}"
    )
    out.append("")
    out.append(
        "Presence is REPORT-ONLY and fails nothing (emission rate is an N=15 "
        "observation; docs/v8.7-constraint-teardown.md §2 item 3). Check 2 "
        "(enumeration agreement) is the failing check. Check 3 (read-at-source "
        "coverage) is REPORT-ONLY -- see the module docstring for the measured "
        "reason."
    )
    out.append("")

    for r in readings:
        out.append(f"## {r.name}")
        if r.unreadable is not None:
            out.append(f"- unreadable: {r.unreadable}")
            out.append("")
            continue
        out.append(
            f"- presence: {'PRESENT' if r.present else 'ABSENT'} (report-only)"
        )
        out.append(
            f"- section 3: {r.population} ground truth(s), {r.marked} `?`-marked"
        )
        if r.duplicates:
            out.append(
                f"- note: section 3 declares {', '.join(r.duplicates)} more than once"
            )
        if not r.present:
            out.append("- check 2: n/a (no roll-up to check)")
            out.append("- check 3: n/a (no roll-up to check)")
            out.append("")
            continue
        assert r.rollup is not None
        out.append(f"- roll-up: `{r.rollup.marked_line}`")
        out.append(
            f"- check 2: {'FAIL' if r.check2 else 'PASS'} "
            f"({len(r.check2)} finding(s))"
        )
        for p in r.check2:
            out.append(f"  - FAIL {p}")
        out.append(
            f"- check 3: {len(r.check3)} observation(s) (report-only)"
        )
        for p in r.check3:
            out.append(f"  - note {p}")
        out.append("")

    if failing:
        out.append("VERDICT: FAIL -- " + ", ".join(r.name for r in failing))
    else:
        out.append("VERDICT: PASS (no check-2 finding)")
    return "\n".join(out)


# ---------------------------------------------------------------------------
# --self-test
# ---------------------------------------------------------------------------
#
# Every fixture below carries its expectation HAND-TRANSCRIBED beside its text:
# the `?`-marked id set and the population size are read off the fixture by a
# human, never computed by `section3_ground_truths`, which is the parser under
# test. Deriving an expectation from the parser is the trap `260924-jdg` hit
# live -- its first mock judge keyed on claim text alone and the
# `always-SUPPORTS` injection passed.


def _doc(section3: str, section4: str) -> str:
    """A minimal six-section analysis document around a section 3 and 4."""
    return (
        "# 1. Problem Essence\n\nOne sentence.\n\n"
        "## 2. Assumptions Table\n\n| Assumption | Type |\n|---|---|\n| A1 | belief |\n\n"
        "## 3. Ground Truths\n\n" + section3.strip("\n") + "\n\n"
        "## 4. Derivation Chains\n\n" + section4.strip("\n") + "\n\n"
        "## 5. Abandoned Reasoning\n\nNothing abandoned.\n\n"
        "## 6. Conclusion\n\nA conclusion (chain C1).\n"
    )


_CHAIN_HIGH = (
    "### Conclusion C1: The claim\n\n"
    "```text\n"
    "GT-1 (first) + GT-2 (second)\n"
    "→ an intermediate claim\n"
    "→ the conclusion\n"
    "```\n\n"
    "**Confidence:** HIGH\n"
)

_CHAIN_MEDIUM = (
    "### Conclusion C1: The claim\n\n"
    "```text\n"
    "GT-1 (first) + GT-2? (second)\n"
    "→ an intermediate claim\n"
    "→ the conclusion\n"
    "```\n\n"
    "**Confidence:** MEDIUM\n"
)


class Fixture(NamedTuple):
    """One offline fixture and its hand-transcribed expectation.

    `expect_present`, `expect_population`, `expect_marked` and
    `expect_check2_fail` are transcribed from the fixture text by hand.
    `why` names what the fixture is for, so a failure report says which
    property broke.
    """

    fid: str
    text: str
    why: str
    expect_present: bool
    expect_population: int
    expect_marked: tuple[str, ...]
    expect_check2_fail: bool
    expect_check3_notes: int


# F1 -- roll-up ABSENT. Section 3 has three ground truths, GT-2? marked.
# Hand-read: population 3, marked {gt-2}. Presence report-only, check 2 n/a.
_F1 = Fixture(
    "absent",
    _doc(
        "- **GT-1** A definitional identity. source: arithmetic; read-at-source: in-entry\n"
        "- **GT-2?** A user-supplied figure. unverified: no source named\n"
        "- **GT-3** A second identity. source: arithmetic; read-at-source: in-entry\n",
        _CHAIN_MEDIUM,
    ),
    "no roll-up emitted: presence is reported, nothing fails",
    False,
    3,
    ("gt-2",),
    False,
    0,
)

# F2 -- roll-up PRESENT and AGREEING. Population 4 (GT-1..GT-4); marked
# {gt-2, gt-3}. Roll-up enumerates GT-2, GT-3 (2 of 4). Chain C1 is MEDIUM, so
# check 3 has no HIGH chain to read and yields zero observations.
_F2 = Fixture(
    "agreeing",
    _doc(
        "- **GT-1** A definitional identity. source: arithmetic; read-at-source: in-entry\n"
        "- **GT-2?** A user-supplied figure. unverified: no source named\n"
        "- **GT-3?** A delegate-reported figure. cited to: a doc; reported-by-delegate: a search\n"
        "- **GT-4** A second identity. source: arithmetic; read-at-source: in-entry\n"
        "\n```text\n"
        "?-marked: GT-2, GT-3 (2 of 4)\n"
        "Read-at-source: GT-1 — identity stated in its entry; GT-4 — arithmetic in its entry\n"
        "```\n",
        _CHAIN_MEDIUM,
    ),
    "the agreeing case: enumeration equals section 3's marked set, M equals the population",
    True,
    4,
    ("gt-2", "gt-3"),
    False,
    0,
)

# F3 -- count/enumeration DISAGREEMENT. Population 4; marked {gt-2, gt-3}.
# Roll-up enumerates GT-2, GT-3 but states `(3 of 7)`: N is 3 against an
# enumeration of 2, and M is 7 against a population of 4. Two findings.
_F3 = Fixture(
    "count-disagrees",
    _doc(
        "- **GT-1** A definitional identity. source: arithmetic; read-at-source: in-entry\n"
        "- **GT-2?** A user-supplied figure. unverified: no source named\n"
        "- **GT-3?** A delegate-reported figure. cited to: a doc; reported-by-delegate: a search\n"
        "- **GT-4** A second identity. source: arithmetic; read-at-source: in-entry\n"
        "\n```text\n"
        "?-marked: GT-2, GT-3 (3 of 7)\n"
        "Read-at-source: GT-1 — identity stated in its entry\n"
        "```\n",
        _CHAIN_MEDIUM,
    ),
    "a stated integer disagreeing with the list it summarises fails, and the "
    "enumeration still governs the section-3 comparison",
    True,
    4,
    ("gt-2", "gt-3"),
    True,
    0,
)

# F4 -- an enumerated id that is NOT `?`-marked in section 3. Population 4;
# marked {gt-2}. Roll-up enumerates GT-2, GT-4 (2 of 4) -- GT-4 is unsuffixed.
_F4 = Fixture(
    "enumerated-not-marked",
    _doc(
        "- **GT-1** A definitional identity. source: arithmetic; read-at-source: in-entry\n"
        "- **GT-2?** A user-supplied figure. unverified: no source named\n"
        "- **GT-3** A second identity. source: arithmetic; read-at-source: in-entry\n"
        "- **GT-4** A third identity. source: arithmetic; read-at-source: in-entry\n"
        "\n```text\n"
        "?-marked: GT-2, GT-4 (2 of 4)\n"
        "Read-at-source: GT-1 — identity stated in its entry\n"
        "```\n",
        _CHAIN_MEDIUM,
    ),
    "an id the roll-up marks that section 3 does not fails",
    True,
    4,
    ("gt-2",),
    True,
    0,
)

# F5 -- a `?`-marked section-3 id MISSING from the roll-up. Population 4;
# marked {gt-2, gt-3}. Roll-up enumerates GT-2 only, and states `(1 of 4)`, so
# the count agrees with the enumeration and the only finding is the omission --
# which is the point: a self-consistent roll-up can still be wrong about §3.
# Its chain is MEDIUM, so check 3 has no HIGH chain to read and yields zero
# observations. (The first transcription of this fixture said one, and the
# control suite caught the transcription, not the code: there is no HIGH chain
# here. Recorded because it is the suite doing its job.)
_F5 = Fixture(
    "marked-not-enumerated",
    _doc(
        "- **GT-1** A definitional identity. source: arithmetic; read-at-source: in-entry\n"
        "- **GT-2?** A user-supplied figure. unverified: no source named\n"
        "- **GT-3?** A delegate-reported figure. cited to: a doc; reported-by-delegate: a search\n"
        "- **GT-4** A second identity. source: arithmetic; read-at-source: in-entry\n"
        "\n```text\n"
        "?-marked: GT-2 (1 of 4)\n"
        "Read-at-source: GT-1 — identity stated in its entry\n"
        "```\n",
        _CHAIN_MEDIUM,
    ),
    "an internally consistent roll-up that omits a marked section-3 id still fails",
    True,
    4,
    ("gt-2", "gt-3"),
    True,
    0,
)

# F6 -- a HIGH chain whose unsuffixed input has NO named location. Population 3;
# marked {gt-3}. Roll-up enumerates GT-3 (1 of 3) -- check 2 agrees. Chain C1 is
# HIGH and its head cites GT-1 and GT-2, both unsuffixed; the Read-at-source
# line names GT-1 only. Hand-read expectation: check 2 PASSES, check 3 yields
# exactly one observation (GT-2). This fixture is what proves check 3 is
# computed rather than stubbed, and that a check-3 observation does not fail the
# document.
_F6 = Fixture(
    "high-chain-uncovered",
    _doc(
        "- **GT-1** A definitional identity. source: arithmetic; read-at-source: in-entry\n"
        "- **GT-2** A second identity. source: arithmetic; read-at-source: in-entry\n"
        "- **GT-3?** A user-supplied figure. unverified: no source named\n"
        "\n```text\n"
        "?-marked: GT-3 (1 of 3)\n"
        "Read-at-source: GT-1 — the identity stated in full in its own entry\n"
        "```\n",
        _CHAIN_HIGH,
    ),
    "a HIGH chain resting on an unsuffixed input with no named location is "
    "OBSERVED, and does not fail the document",
    True,
    3,
    ("gt-3",),
    False,
    1,
)

# F7 -- the same HIGH chain, both inputs located, one of them through a
# grouped segment. Population 3; marked {gt-3}; roll-up `GT-3 (1 of 3)`.
# Hand-read: check 2 passes, check 3 yields zero observations.
_F7 = Fixture(
    "high-chain-covered",
    _doc(
        "- **GT-1** A definitional identity. source: arithmetic; read-at-source: in-entry\n"
        "- **GT-2** A second identity. source: arithmetic; read-at-source: in-entry\n"
        "- **GT-3?** A user-supplied figure. unverified: no source named\n"
        "\n```text\n"
        "?-marked: GT-3 (1 of 3)\n"
        "Read-at-source: GT-1, GT-2 — both identities stated in full in their own entries\n"
        "```\n",
        _CHAIN_HIGH,
    ),
    "a grouped Read-at-source segment locates every id it names",
    True,
    3,
    ("gt-3",),
    False,
    0,
)

# F8 -- the range form, observed live in `tests/live-conformance-v9.0/PR-P2.md`.
# Population 3; marked {gt-3}; roll-up `GT-3 (1 of 3)`; the Read-at-source line
# writes `GT-1..GT-2`. Hand-read: check 2 passes, check 3 yields zero.
_F8 = Fixture(
    "range-form",
    _doc(
        "- **GT-1** A definitional identity. source: arithmetic; read-at-source: in-entry\n"
        "- **GT-2** A second identity. source: arithmetic; read-at-source: in-entry\n"
        "- **GT-3?** A user-supplied figure. unverified: no source named\n"
        "\n```text\n"
        "?-marked: GT-3 (1 of 3)\n"
        "Read-at-source: GT-1..GT-2 — definitional terminus, no external figure asserted\n"
        "```\n",
        _CHAIN_HIGH,
    ),
    "the `GT-1..GT-5` range form locates the ids it spans",
    True,
    3,
    ("gt-3",),
    False,
    0,
)

# F9 -- the backticked line form, observed live in
# `tests/adversarial-firing-v9.5/Q-P2.md`, together with `?`-suffixed ids in the
# enumeration (observed in `tests/confidence-transitivity-v9.4/CT-A1.md`).
# Population 3; marked {gt-2, gt-3}; roll-up `GT-2?, GT-3? (2 of 3)`.
# Hand-read: check 2 passes -- ids compare `?`-insensitively.
_F9 = Fixture(
    "backticked-and-suffixed",
    _doc(
        "- **GT-1** A definitional identity. source: arithmetic; read-at-source: in-entry\n"
        "- **GT-2?** A user-supplied figure. unverified: no source named\n"
        "- **GT-3?** A delegate-reported figure. cited to: a doc; reported-by-delegate: a search\n"
        "\n"
        "`?-marked: GT-2?, GT-3? (2 of 3)`\n"
        "`Read-at-source: GT-1 — the identity stated in full in its own entry`\n",
        _CHAIN_MEDIUM,
    ),
    "the backticked line form and a `?`-suffixed enumeration both parse",
    True,
    3,
    ("gt-2", "gt-3"),
    False,
    0,
)

# F10 -- a `**Pre-check:**` line carrying a `?-marked:` fragment, and NO
# roll-up. That line is body-prescribed and occurs on three shipped surfaces;
# reading it as a roll-up would make the presence rate meaningless and would
# hand check 2 a bogus enumeration. Hand-read: presence ABSENT, check 2 n/a.
_F10 = Fixture(
    "pre-check-is-not-a-rollup",
    _doc(
        "- **GT-1** A definitional identity. source: arithmetic; read-at-source: in-entry\n"
        "- **GT-2?** A user-supplied figure. unverified: no source named\n"
        "\n"
        "**Pre-check:** head GT-1, GT-2? · ?-marked: GT-2? · lowest cited: none · "
        "Inputs ceiling: MEDIUM\n",
        _CHAIN_MEDIUM,
    ),
    "a `**Pre-check:**` line is not a roll-up (disclosed bound (c))",
    False,
    2,
    ("gt-2",),
    False,
    0,
)

# F11 -- the form `output-template.md:136` exists to bar: a stated INTEGER in
# place of the list. Population 4; marked {gt-2, gt-3}. The line writes
# `?-marked: 2 of 4 ground truths are unverified (2 of 4)` -- an integer that is
# arithmetically CORRECT and still fails, because it enumerates nothing and so
# cannot be checked against the list it summarises. Hand-read: two findings --
# both marked ids absent from the (empty) enumeration, and N=2 against an
# enumeration of 0. The same shape was confirmed by mutating
# `tests/baseline-reading-v9.6/Q-P1.md`, which the module docstring records.
_F11 = Fixture(
    "integer-not-a-list",
    _doc(
        "- **GT-1** A definitional identity. source: arithmetic; read-at-source: in-entry\n"
        "- **GT-2?** A user-supplied figure. unverified: no source named\n"
        "- **GT-3?** A delegate-reported figure. cited to: a doc; reported-by-delegate: a search\n"
        "- **GT-4** A second identity. source: arithmetic; read-at-source: in-entry\n"
        "\n```text\n"
        "?-marked: 2 of 4 ground truths are unverified (2 of 4)\n"
        "Read-at-source: GT-1 — identity stated in its entry\n"
        "```\n",
        _CHAIN_MEDIUM,
    ),
    "an arithmetically correct integer in place of the list still fails -- an "
    "integer cannot be checked against the list it summarises "
    "(output-template.md:136)",
    True,
    4,
    ("gt-2", "gt-3"),
    True,
    0,
)

FIXTURES: tuple[Fixture, ...] = (
    _F1,
    _F2,
    _F3,
    _F4,
    _F5,
    _F6,
    _F7,
    _F8,
    _F9,
    _F10,
    _F11,
)


def fixture_problems() -> list[str]:
    """Every fixture reads as its hand-transcribed expectation says."""
    problems: list[str] = []
    for f in FIXTURES:
        r = read_document(f.fid, f.text)
        if r.unreadable is not None:
            problems.append(f"{f.fid}: document did not resolve: {r.unreadable}")
            continue
        if r.present != f.expect_present:
            problems.append(
                f"{f.fid}: presence {r.present} != expected {f.expect_present} ({f.why})"
            )
        if r.population != f.expect_population:
            problems.append(
                f"{f.fid}: section-3 population {r.population} != expected "
                f"{f.expect_population}"
            )
        marked = tuple(
            sorted(g.key for g in _SECTION3_PARSER(QH._slice_sections(f.text)[3]) if g.marked)
        )
        if marked != tuple(sorted(f.expect_marked)):
            problems.append(
                f"{f.fid}: `?`-marked set {marked!r} != hand-transcribed "
                f"{tuple(sorted(f.expect_marked))!r}"
            )
        if r.failing != f.expect_check2_fail:
            problems.append(
                f"{f.fid}: check 2 {'FAIL' if r.failing else 'PASS'} != expected "
                f"{'FAIL' if f.expect_check2_fail else 'PASS'} ({f.why}); "
                f"findings={list(r.check2)!r}"
            )
        if len(r.check3) != f.expect_check3_notes:
            problems.append(
                f"{f.fid}: check 3 gave {len(r.check3)} observation(s), expected "
                f"{f.expect_check3_notes}: {list(r.check3)!r}"
            )
        # Keyed on "check 3 alone made it fail", not on "the verdict differs
        # from check 2's expectation": the looser form reported a check-3
        # violation whenever check 2 failed for its own reason, which was a
        # misleading message rather than a real finding.
        if r.check3 and not r.check2 and r.failing:
            problems.append(
                f"{f.fid}: a check-3-only finding made the document fail -- "
                "check 3 is report-only"
            )
    return problems


def report_only_problems() -> list[str]:
    """Presence and check 3 must never make a document fail, on any fixture.

    Asserted over the whole fixture set rather than argued in prose: a document
    whose only findings are absence or check-3 observations reads as not
    failing. This is the control behind the docstring's report-only claim.
    """
    problems: list[str] = []
    for f in FIXTURES:
        r = read_document(f.fid, f.text)
        if r.unreadable is not None:
            continue
        if not r.present and r.failing:
            problems.append(f"{f.fid}: an absent roll-up made the document fail")
        if r.check3 and not r.check2 and r.failing:
            problems.append(
                f"{f.fid}: a check-3-only finding made the document fail"
            )
    # At least one fixture must actually exercise each report-only surface, or
    # the assertions above are vacuous.
    if not any(not read_document(f.fid, f.text).present for f in FIXTURES):
        problems.append("no fixture exercises an ABSENT roll-up")
    if not any(read_document(f.fid, f.text).check3 for f in FIXTURES):
        problems.append("no fixture produces a check-3 observation")
    return problems


def roll_up_locator_problems() -> list[str]:
    """`find_rollup` recognises the observed forms and rejects the near-misses."""
    problems: list[str] = []

    cases: tuple[tuple[str, str, bool], ...] = (
        ("plain", "?-marked: GT-1, GT-2 (2 of 5)\n", True),
        ("backticked", "`?-marked: GT-1, GT-2 (2 of 5)`\n", True),
        ("fenced", "```text\n?-marked: GT-1 (1 of 5)\n```\n", True),
        (
            "pre-check",
            "**Pre-check:** head GT-1 · ?-marked: GT-1 · lowest cited: none\n",
            False,
        ),
        (
            "quoted-in-prose",
            'Quoted span: *"?-marked: GT-8, GT-9 (2 of 10)"* was checked.\n',
            False,
        ),
        ("no-count", "?-marked: GT-1, GT-2\n", True),
    )
    for name, text, expect in cases:
        found = find_rollup(text) is not None
        if found != expect:
            problems.append(
                f"locator/{name}: found={found}, expected={expect}"
            )

    # The `(N of M)` tail parses, and the enumeration excludes it.
    r = find_rollup("?-marked: GT-2, GT-5, GT-9, GT-14 (4 of 22)\n")
    if r is None:
        problems.append("locator: the template's own example line did not parse")
    else:
        if (r.stated_n, r.stated_m) != (4, 22):
            problems.append(
                f"locator: template example parsed (N, M) as {(r.stated_n, r.stated_m)!r}, "
                "expected (4, 22)"
            )
        if r.enumerated != ("GT-2", "GT-5", "GT-9", "GT-14"):
            problems.append(
                f"locator: template example enumerated {r.enumerated!r}, expected the "
                "four ids"
            )

    # Multiple Read-at-source lines are all collected (observed in
    # `tests/live-conformance-v9.0/PR-P2.md`), and a following non-matching line
    # ends the run.
    r = find_rollup(
        "?-marked: GT-7, GT-8, GT-9 (3 of 9)\n"
        "Read-at-source: GT-6 — the prompt, quoted verbatim\n"
        "Read-at-source: GT-1..GT-5 — definitional terminus\n"
        "\n"
        "Some other prose that is not part of the roll-up.\n"
        "Read-at-source: GT-99 — must not be collected\n"
    )
    if r is None:
        problems.append("locator: the two-Read-at-source form did not parse")
    elif len(r.read_lines) != 2:
        problems.append(
            f"locator: collected {len(r.read_lines)} Read-at-source line(s), expected 2 "
            "(the run ends at the first other non-blank line)"
        )

    # A per-entry `Read-at-source:` inside a ground-truth bullet is part of the
    # entry, not the roll-up: it must not be picked up as a roll-up line, and
    # its bullet must not be read as a roll-up.
    if find_rollup(
        "- **GT-8** An identity.\n"
        "  Source: arithmetic. Read-at-source: definitional, stated in this entry.\n"
    ) is not None:
        problems.append("locator: a ground-truth entry was read as a roll-up")

    return problems


def section3_parser_problems() -> list[str]:
    """`section3_ground_truths` reads bullets, skips fences, and dedups ids."""
    problems: list[str] = []

    text = (
        "- **GT-1** first\n"
        "- **GT-2?** second\n"
        "```text\n"
        "- **GT-9** this bullet is inside a fence and is not an entry\n"
        "?-marked: GT-2 (1 of 2)\n"
        "```\n"
    )
    got = tuple((g.key, g.marked) for g in section3_ground_truths(text))
    want = (("gt-1", False), ("gt-2", True))
    if got != want:
        problems.append(f"parser/fence: {got!r} != {want!r}")

    dup = "- **GT-1** first\n- **GT-1?** the same id again\n"
    got2 = tuple(g.key for g in section3_ground_truths(dup))
    if got2 != ("gt-1",):
        problems.append(f"parser/dedup: {got2!r} != ('gt-1',)")
    if duplicate_gt_ids(dup) != ["gt-1"]:
        problems.append(
            f"parser/dedup: duplicate_gt_ids gave {duplicate_gt_ids(dup)!r}, "
            "expected ['gt-1']"
        )

    # An indented continuation line is not a second entry.
    cont = (
        "- **GT-8** An identity.\n"
        "  Source: arithmetic. Read-at-source: in-entry.\n"
        "- **GT-9?** A belief.\n"
    )
    got3 = tuple(g.key for g in section3_ground_truths(cont))
    if got3 != ("gt-8", "gt-9"):
        problems.append(f"parser/continuation: {got3!r} != ('gt-8', 'gt-9')")

    return problems


def located_read_problems() -> list[str]:
    """`located_read_at_source` on each observed shape of the line."""
    problems: list[str] = []
    cases: tuple[tuple[str, tuple[str, ...], set[str]], ...] = (
        (
            "per-id",
            ("GT-1 — Lambda pricing page, x86 on-demand table",),
            {"gt-1"},
        ),
        (
            "grouped",
            ("GT-1, GT-2, GT-4 — Lambda pricing page, quoted",),
            {"gt-1", "gt-2", "gt-4"},
        ),
        (
            "semicolon-segments",
            ("GT-8 — identity stated in its entry; GT-9 — percentile definition",),
            {"gt-8", "gt-9"},
        ),
        (
            "range",
            ("GT-1..GT-3 — definitional terminus, no external figure asserted",),
            {"gt-1", "gt-2", "gt-3"},
        ),
        (
            "prose",
            ("GT-2 and GT-3 are definitional, stated in full above",),
            {"gt-2", "gt-3"},
        ),
        ("none", ("none — no source was cited, so no read was possible",), set()),
        ("bare-id-no-location", ("GT-5",), set()),
    )
    for name, lines, want in cases:
        got = located_read_at_source(lines)
        if got != want:
            problems.append(f"located/{name}: {sorted(got)!r} != {sorted(want)!r}")
    return problems


def vacuous_agreement_problems() -> list[str]:
    """Check 2 refuses to pass a present roll-up over an empty population.

    Handed an empty population BY CONSTRUCTION, never through the parser, so
    the guard is asserted rather than inferred. Stated separately from the
    `empty-ground-truths` injection on purpose: the injection proves the SUITE
    notices a degraded parser, while this proves the CHECK carries the guard.
    Without it, every enumeration agrees vacuously with an empty set and check 2
    passes on everything -- CONF-GATE's CR-02(a) shape, a control invariant to
    the thing it checks.

    Routed through the `_CHECK2` seam rather than calling
    `enumeration_problems` by name, so the `always-pass` and
    `presence-is-agreement` injections are caught here too and not only through
    the fixture set. The `empty-ground-truths` injection swaps the parser, not
    `_CHECK2`, so this control still exercises the real check under it.

    The populated arm is asserted beside it, because "always finds a problem" is
    not a guard either.
    """
    problems: list[str] = []
    rollup = find_rollup("?-marked: GT-2, GT-3 (2 of 4)\n")
    if rollup is None:
        return ["vacuous: the probe roll-up did not parse"]

    if not _CHECK2(rollup, []):
        problems.append(
            "check 2 PASSED a present roll-up over an empty ground-truth population -- "
            "every enumeration agrees vacuously with an empty set"
        )

    # The same roll-up over the population it actually describes must pass, or
    # the guard above is just an unconditional failure.
    population = [
        GroundTruth("GT-1", "gt-1", False),
        GroundTruth("GT-2?", "gt-2", True),
        GroundTruth("GT-3?", "gt-3", True),
        GroundTruth("GT-4", "gt-4", False),
    ]
    findings = _CHECK2(rollup, population)
    if findings:
        problems.append(
            f"check 2 failed an agreeing roll-up: {findings!r} -- the empty-population "
            "guard must not be an unconditional failure"
        )
    return problems


def harness_surface_problems() -> list[str]:
    """Every harness name this module calls still exists.

    A rename in `check-quality-harness.py` must break loudly here rather than
    silently skipping a check.
    """
    problems: list[str] = []
    for name in _REQUIRED_HARNESS_NAMES:
        if not hasattr(QH, name):
            problems.append(f"check-quality-harness.py no longer provides {name}")
    return problems


# --- the template-only tripwire (a falsifier, not a promise) ----------------

# The roll-up form, as the four plan-time falsifiers F1-F3 match it: a
# line-start `?-marked:` carrying a `(N of M)` tail. Deliberately the same
# shape as `_ROLLUP_MARKED_RE` + `_ROLLUP_COUNT_RE` so the tripwire and the
# locator cannot drift apart.
_TEMPLATE_PATH = Path("shared/spine/references/output-template.md")
_BODY_PATH = Path("shared/spine/SKILL-body.md")

# (label, paths, expected number of files carrying the roll-up form). Measured
# 2026-09-24 at HEAD 02005fd0 by quick task `260924-prv`; the same counts the
# ROADMAP's Phase 999.90 FALSIFIED note tabulates.
_TEMPLATE_ONLY_SURFACES: tuple[tuple[str, str, int], ...] = (
    ("the agent body", "shared/spine/SKILL-body.md", 0),
    ("the companion references", "shared/references/*.md", 0),
    ("the worked exemplars", "shared/examples/*.md", 0),
    ("the output template", "shared/spine/references/output-template.md", 1),
)


def _files_with_rollup(paths: list[Path]) -> list[str]:
    """Which of `paths` carry the roll-up form, by the locator's own rule."""
    hits: list[str] = []
    for p in paths:
        try:
            text = p.read_text(encoding="utf-8")
        except OSError:
            continue
        for line in text.splitlines():
            m = _ROLLUP_MARKED_RE.match(line)
            if m is not None and _ROLLUP_COUNT_RE.search(m.group("body")):
                hits.append(p.as_posix())
                break
    return hits


def template_only_problems() -> list[str]:
    """FAIL if the roll-up is no longer template-only.

    This module's central factual claim about the tree is that the roll-up form
    is prescribed in `output-template.md` and NOWHERE else on a shipped
    surface, which is what makes emitting it evidence that the template was
    read. `CLAUDE.md` § "Claims and falsifiers" requires a claim about this tree
    to ship with a command that exits non-zero if the claim is FALSE, not with a
    check that the sentence is present. This is that command.

    It is a deliberate tripwire. If a later change prescribes the roll-up in the
    agent body -- the mechanism that destroyed backlog 999.90, where
    `**Confidence:**` and the unverified-input rule were both absorbed into
    `SKILL-body.md` after 999.90 nominated `**Confidence:**` -- then this
    checker stops measuring template reading, and the right outcome is a loud
    failure here, not a quiet pass. Do not relax it to a warning; retire the
    checker instead, and say why.
    """
    problems: list[str] = []
    for label, pattern, expected in _TEMPLATE_ONLY_SURFACES:
        if "*" in pattern:
            paths = sorted(REPO_ROOT.glob(pattern))
        else:
            paths = [REPO_ROOT / pattern]
        hits = _files_with_rollup(paths)
        if len(hits) != expected:
            problems.append(
                f"the roll-up form now occurs in {len(hits)} file(s) under {label} "
                f"({pattern}), expected {expected}: {hits!r} -- the roll-up is no "
                "longer template-only and this checker no longer measures what its "
                "docstring claims"
            )
    # The enumeration-governs rule this module's check 2 rests on must still be
    # stated where the docstring cites it.
    template = (REPO_ROOT / _TEMPLATE_PATH).read_text(encoding="utf-8")
    if "the enumeration governs" not in template:
        problems.append(
            f"{_TEMPLATE_PATH.as_posix()} no longer states the enumeration-governs rule "
            "that check 2 rests on"
        )
    return problems


def structure_problems() -> list[str]:
    """This module prescribes nothing.

    That is a claim the tool makes about itself, so it is checked.
    `template_only_problems()` owns it for the roll-up form specifically; this
    adds the wider assertion that no file under `shared/` mentions this script
    at all, which is 999.90's trap guard -- a detector reads output, so naming
    it on a shipped surface would convert the template-only artifact it
    measures into a body-prescribed one and destroy the signal.

    Registration under PROV-ROLLUP (999.173's residual) retired this
    function's two former assertions that the script appeared in neither
    `scripts/check-firewall-battery.sh` nor `.github/workflows/validation.yml`.
    They were controls on the shipping task's scope claim, not product
    invariants, and they are not inverted here: REG-GUARD derives
    battery-id-implies-CI-job from the battery's own source text, and a second
    grammar over that same file is what its D-01 floor note forbids.
    """
    problems: list[str] = []
    me = Path(__file__).name

    shared = REPO_ROOT / "shared"
    if shared.is_dir():
        mentions = [
            p.relative_to(REPO_ROOT).as_posix()
            for p in sorted(shared.rglob("*.md"))
            if me in p.read_text(encoding="utf-8")
        ]
        if mentions:
            problems.append(
                f"{me} is named on a shipped source surface ({mentions!r}) -- a detector "
                "reads output and prescribes nothing"
            )
    return problems


def exemplar_problems() -> list[str]:
    """The 14 shipped exemplars read without a wall of failures.

    The plan's own verification: `shared/examples/*.md` is a runtime-artifact-free
    surface, so every exemplar must read as presence ABSENT with check 2 n/a.
    Should an exemplar ever grow a roll-up, this control stops asserting absence
    and instead requires check 2 to have genuinely evaluated it -- which is the
    behaviour the plan asks for, not a frozen count.
    """
    problems: list[str] = []
    examples = sorted((REPO_ROOT / "shared" / "examples").glob("*.md"))
    if not examples:
        return ["shared/examples/ holds no .md files"]
    for p in examples:
        r = read_document(p.name, p.read_text(encoding="utf-8"))
        if r.unreadable is not None:
            # An exemplar the six-section slicer cannot read is not this
            # module's finding to make; it is reported, never failed.
            continue
        if r.present and not r.check2 and r.population == 0:
            problems.append(
                f"{p.name}: a roll-up was found but section 3 read empty, and check 2 "
                "still passed"
            )
    return problems


# --- injections -------------------------------------------------------------
#
# Each injection degrades exactly one component and MUST make the control suite
# fail. `--inject NAME` runs the whole suite with it active, so the catch is
# demonstrable as a non-zero exit rather than asserted in prose.

INJECTIONS: tuple[str, ...] = (
    "always-pass",
    "presence-is-agreement",
    "empty-ground-truths",
)


def _inject_always_pass(rollup: Rollup, population: list[GroundTruth]) -> list[str]:
    """Check 2 stubbed to pass unconditionally."""
    return []


def _inject_presence_is_agreement(
    rollup: Rollup, population: list[GroundTruth]
) -> list[str]:
    """Check 2 degraded to a presence check: the roll-up exists, so it agrees.

    This is the exact shape `CLAUDE.md` § "Claims and falsifiers" bars, written
    out so the suite can be shown to reject it.
    """
    return [] if rollup.marked_line else ["no roll-up"]


def _inject_empty_ground_truths(section3: str) -> list[GroundTruth]:
    """The section-3 parser degraded to return nothing.

    The injection that matters. An empty population makes every enumeration
    agree vacuously, so check 2 would pass on everything -- a control invariant
    to the thing it checks (CONF-GATE CR-02(a)). Check 2's first comparison
    exists to catch precisely this.
    """
    return []


def _run_controls(injection: str | None) -> list[str]:
    """Run every control group, with `injection` (if any) active."""
    global _SECTION3_PARSER, _CHECK2
    saved_parser, saved_check2 = _SECTION3_PARSER, _CHECK2

    if injection == "always-pass":
        _CHECK2 = _inject_always_pass
    elif injection == "presence-is-agreement":
        _CHECK2 = _inject_presence_is_agreement
    elif injection == "empty-ground-truths":
        _SECTION3_PARSER = _inject_empty_ground_truths
    elif injection is not None:
        raise SystemExit(f"error: unknown injection {injection!r}; one of {INJECTIONS}")

    try:
        problems: list[str] = []
        problems += [f"[harness] {p}" for p in harness_surface_problems()]
        problems += [f"[structure] {p}" for p in structure_problems()]
        problems += [f"[template-only] {p}" for p in template_only_problems()]
        problems += [f"[section3] {p}" for p in section3_parser_problems()]
        problems += [f"[locator] {p}" for p in roll_up_locator_problems()]
        problems += [f"[located] {p}" for p in located_read_problems()]
        problems += [f"[vacuous] {p}" for p in vacuous_agreement_problems()]
        problems += [f"[fixture] {p}" for p in fixture_problems()]
        problems += [f"[report-only] {p}" for p in report_only_problems()]
        problems += [f"[exemplar] {p}" for p in exemplar_problems()]
        return problems
    finally:
        _SECTION3_PARSER, _CHECK2 = saved_parser, saved_check2


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
        f"fixtures: {len(FIXTURES)}; injections: {len(INJECTIONS)}; "
        f"template-only surfaces: {len(_TEMPLATE_ONLY_SURFACES)}"
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
    for d in args.dir or []:
        for f in sorted(Path(d).glob("*.md")):
            if f.name in ("README.md", "catalog.md"):
                continue
            paths.append(f)
    return paths


def describe() -> dict:
    """Pure, gate-agnostic self-description backing PROV-ROLLUP (D-03 shape).

    Every field is DERIVED from this module's own rosters, never hand-typed: a
    hand-copied count in a generated doc page is the defect CONF-SURFACE exists
    to prevent, and this gate's whole subject is counts that agree with the
    lists they summarise.
    """
    control_ids = sorted([f.fid for f in FIXTURES] + list(INJECTIONS))
    return {
        "control_ids": control_ids,
        "control_count": len(control_ids),
        "registered_surfaces": sorted(
            relpath
            for _label, relpath, _expected in _TEMPLATE_ONLY_SURFACES
            if "*" not in relpath
        ),
        "scan_globs": sorted(
            relpath
            for _label, relpath, _expected in _TEMPLATE_ONLY_SURFACES
            if "*" in relpath
        ),
        "locked_constants": {
            relpath: expected
            for _label, relpath, expected in _TEMPLATE_ONLY_SURFACES
        },
        "derived_counts": {
            "fixtures": len(FIXTURES),
            "injections": len(INJECTIONS),
            "template_only_surfaces": len(_TEMPLATE_ONLY_SURFACES),
        },
        "disclosed_bounds_anchors": sorted(
            [
                "presence-is-report-only",
                "read-at-source-coverage-is-report-only",
                "rollup-located-in-section-3-only",
                "pre-check-line-is-not-a-rollup",
                "ids-compared-question-mark-insensitively",
                "section-3-read-outside-fenced-code",
                "unreadable-document-is-named-not-failed",
                "chain-head-window-is-head-line-only",
                "read-at-source-grammar-unprescribed",
            ]
        ),
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=(
            "Cross-check an analysis's provenance roll-up against its own section 3. "
            "Presence and read-at-source coverage are report-only; enumeration "
            "agreement is the failing check. Registered as PROV-ROLLUP in the "
            "offline battery and in CI."
        )
    )
    ap.add_argument("--analysis", nargs="+", help="one or more analysis .md files")
    ap.add_argument(
        "--dir", action="append", help="a directory of analysis .md files (repeatable)"
    )
    ap.add_argument("--out", type=Path, help="write the report here instead of stdout")
    ap.add_argument("--self-test", action="store_true", help="run the offline control suite")
    ap.add_argument(
        "--inject",
        choices=INJECTIONS,
        help="run the control suite with one component degraded; must exit non-zero",
    )
    ap.add_argument("--describe", action="store_true", help="emit self-description JSON")
    args = ap.parse_args(argv)

    if args.describe:
        print(json.dumps(describe(), indent=2, sort_keys=True))
        return 0

    if args.inject:
        return self_test(args.inject)
    if args.self_test:
        return self_test()

    paths = _collect_inputs(args)
    if not paths:
        ap.error("one of --analysis, --dir, --self-test or --inject is required")

    readings: list[DocReading] = []
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"error: cannot read {path}: {exc}", file=sys.stderr)
            return 1
        readings.append(read_document(path.name, text))

    report = render_report(readings)
    if args.out:
        args.out.write_text(report + "\n", encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        print(report)
    return 1 if any(r.failing for r in readings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
