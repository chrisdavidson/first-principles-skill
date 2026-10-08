#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""PERSONA-GATE: checker and self-test for a persona view against its source analysis.

Proves that a persona view (a role-scoped overlay of one delivered first-principles
analysis — decision-owner, operator, risk, skeptic) adds no claim its source analysis
does not already carry. Checks, mechanically: the memo header (a title line, a
To/Re/Basis/Band blockquote block, and the provenance sentence), the body's word count
against the role's band, that the body is a memo -- an `In brief:` paragraph first,
then exactly one paragraph per the role's fixed question in order, with no bullet
line, no bold label and no printed question text (PV-QUESTIONS; it counts paragraphs
and cannot prove each one answers its question), that every body sentence carries a
citation token, that every cited chain id, ground-truth id (including its `?`
marking), assumption id and quoted dead-end title resolves against the source
analysis, that every number in the body appears as a number in the source, and that
the Band line agrees with the source's own §6 confidence band. It also checks the
companion business-reading guide names only sections and fields that exist in the
output template, and that the guide stays inside its word ceiling.

It also checks that a body sentence never hands down a decision: no denylisted
imperative opener, no second-person address, no verdict on the reader, and no long
verbatim run of §6's `**Recommended approach:**` paragraph (PV-DIRECTIVE).

What this does NOT prove: that a cited id actually supports the sentence it is
attached to, or that a paragraph's prose actually answers the question it sits at
the position of (see `memo-structure-counts-paragraphs-not-answers` in `--describe`).
Resolving `(chain C1)` only shows the analysis declares a C1 — it does not show C1's
content backs the claim beside it. That is a semantic-support question, deliberately
out of scope here (see `citation-presence-not-semantic-support` in `--describe`).
PV-DIRECTIVE is lexical, not semantic: it cannot see an imperative embedded after an
introductory clause (sentence-initial only), and it compares only against §6's own
Recommended approach paragraph, never the Answer block or the rest of the body (see
`directive-check-is-lexical-not-semantic`,
`imperative-check-is-sentence-initial-only`, and
`verbatim-run-checked-against-section6-recommended-approach-only` in `--describe`).

Usage:
    python3 scripts/check-persona-view.py <persona.md> <analysis.md>
    python3 scripts/check-persona-view.py --self-test
    python3 scripts/check-persona-view.py --describe
"""

from __future__ import annotations

import argparse
import ast
import importlib.util
import json
import re
import sys
import tempfile
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import NamedTuple

REPO_ROOT = Path(__file__).resolve().parent.parent
CONTRACT = REPO_ROOT / "shared" / "spine" / "references" / "persona-views.md"
GUIDE = REPO_ROOT / "shared" / "spine" / "references" / "how-to-read.md"
TEMPLATE = REPO_ROOT / "shared" / "spine" / "references" / "output-template.md"
FIXTURE_DIR = REPO_ROOT / "tests" / "persona-views-v9.18"

# (fixture filename under FIXTURE_DIR, source relpath from REPO_ROOT)
FIXTURES: tuple[tuple[str, str], ...] = (
    ("product-business-2-decision-owner.md", "shared/examples/product-business-2.md"),
    ("product-business-2-operator.md", "shared/examples/product-business-2.md"),
    ("product-business-2-risk.md", "shared/examples/product-business-2.md"),
    ("product-business-2-skeptic.md", "shared/examples/product-business-2.md"),
    ("personal-general-risk.md", "shared/examples/personal-general.md"),
)

# D-11 (Phase 87): the independent transcription this module's own
# contract-parity control (P02) compares the shipped contract's roster table
# against. Band = the In-brief words of the D-11 approved memo shape (30,
# measured by this module's own whitespace-split counting rule over body
# units) plus the 60-140 words of paragraph room measured in 87-01; the D-11
# sample body (126 words) sits inside it. Question words no longer count
# toward the band because the questions are hidden structure, never printed.
LOCKED_ROSTER: dict[str, tuple[str, int, int]] = {
    "decision-owner": ("Decision Owner", 90, 170),
    "operator": ("Operator", 90, 170),
    "risk": ("Risk", 90, 170),
    "skeptic": ("Skeptic", 90, 170),
}

# D-05/P04: the independent transcription of the contract's four D-02 fixed
# question lists (87-CONTEXT.md), checked the same way LOCKED_ROSTER is --
# never retyped from this module's own parser's output.
LOCKED_QUESTIONS: dict[str, tuple[str, ...]] = {
    "decision-owner": (
        "What was examined, and why does it matter?",
        "What has it settled that I can rely on?",
        "How sure is it, and what is it unsure about?",
        "Where do I find the recommendation?",
    ),
    "operator": (
        "What does this mean for the work in front of me?",
        "Which constraints hold, and until when?",
        "What was tried and set aside, and why?",
        "What facts are still missing?",
    ),
    "risk": (
        "What risk does the analysis retire?",
        "What is unverified?",
        "What could change?",
        "What does the analysis itself flag for caution?",
    ),
    "skeptic": (
        "What does the argument rest on?",
        "What alternatives were considered, and why were they set aside?",
        "Where is the argument weakest?",
        "What evidence would overturn it?",
    ),
}

GUIDE_MAX_WORDS = 500
PROVENANCE_TEMPLATE = (
    "Derived from §6 and the structured summary of {name}; "
    "the six sections remain the source of truth."
)

# Closed set of finding codes. PV-SOURCE is an addition to the contract's own D-07
# list, raised only when the analysis itself cannot be sliced into sections 1-6 or
# carries no readable §6 band -- so a malformed source never masquerades as a
# persona defect.
FINDING_CODES: tuple[str, ...] = (
    "PV-HEADER",
    "PV-WORDS",
    "PV-UNCITED",
    "PV-ID",
    "PV-NUMBER",
    "PV-BAND",
    "PV-SHAPE",
    "PV-DEADEND",
    "PV-GUIDE-NAME",
    "PV-GUIDE-WORDS",
    "PV-SOURCE",
    "PV-QUESTIONS",
    "PV-DIRECTIVE",
)

# D-05 (Phase 87): the contract's own **Denylisted openers:** line
# (shared/spine/references/persona-views.md, Voice section) is the sole
# source for this set -- P05 asserts parity so a hand-edited constant
# cannot silently drift from the contract's own prose. Union of the
# research corpus's denylisted-opener list with every imperative the
# 2026-10-02 review found in the live CSA views the user objected to
# (Decide, Move, Read, Risk-classify, Confirm, Keep, Classify, Switch,
# Finish).
DIRECTIVE_OPENERS: frozenset[str] = frozenset(
    {
        "build",
        "classify",
        "confirm",
        "consider",
        "decide",
        "finish",
        "keep",
        "move",
        "read",
        "reject",
        "risk-classify",
        "switch",
        "take",
        "treat",
    }
)
# The contract's two-word "Do not" opener, plus its contraction -- neither
# is a single DIRECTIVE_OPENERS token, so each is matched as a short
# sentence-initial phrase instead.
DIRECTIVE_PHRASE_OPENERS: tuple[tuple[str, ...], ...] = (("do", "not"), ("don't",))
_SECOND_PERSON_RE = re.compile(r"\b(?:you|your|yours|yourself|you're)\b", re.IGNORECASE)
_READER_VERDICT_RE = re.compile(
    r"\b(?:objection|reader)\s+is\s+(?:right|wrong)\b", re.IGNORECASE
)
# Measured 2026-10-02 (planner): the frozen pre-87 fixture shares a 16-word
# run with its source's §6 Recommended approach paragraph; a constructed
# single-sentence restatement (M-D-RUN) shares 9; the D-01 approved sample
# shares none. 6 sits well inside that margin on both sides.
VERBATIM_RUN_WORDS = 6

# D-11 (Phase 87): the memo's own fixed structure -- the four blockquote
# fields in order, and the literal opener of the body's first paragraph.
MEMO_FIELDS: tuple[str, ...] = ("To", "Re", "Basis", "Band (from §6)")
IN_BRIEF_PREFIX = "In brief:"


class Finding(NamedTuple):
    code: str
    detail: str


class SourceError(Exception):
    """The analysis text cannot be read as a six-section analysis at all."""


def _relpath(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


# ---------------------------------------------------------------------------
# Reused parsers (importlib precedent: check-report-figures.py's `sb()`) --
# never a second grammar for section slicing, chain ids, GT declarations,
# table rows or dead-end headings.
# ---------------------------------------------------------------------------

_SB = None
_QH = None


def sb():
    global _SB
    if _SB is None:
        spec = importlib.util.spec_from_file_location(
            "_sb_for_persona_view", REPO_ROOT / "scripts" / "check-summary-block.py"
        )
        mod = importlib.util.module_from_spec(spec)
        sys.modules["_sb_for_persona_view"] = mod
        spec.loader.exec_module(mod)
        _SB = mod
    return _SB


def qh():
    global _QH
    if _QH is None:
        _QH = sb()._load_qh()
    return _QH


# ---------------------------------------------------------------------------
# Roster (contract parsing)
# ---------------------------------------------------------------------------

_ROSTER_SECTION_RE = re.compile(
    r"^## Persona roster\n(.*?)(?=^## |\Z)", re.MULTILINE | re.DOTALL
)
_BAND_SPLIT_RE = re.compile(r"[–-]")


def load_roster(contract_text: str) -> dict[str, tuple[str, int, int]]:
    """Parse the contract's `## Persona roster` table into slug -> (title, min, max)."""
    m = _ROSTER_SECTION_RE.search(contract_text)
    section_text = m.group(1) if m else ""
    rows = sb()._table_columns(section_text, ("Slug", "Title", "Body words"))
    roster: dict[str, tuple[str, int, int]] = {}
    for row in rows:
        slug = row["Slug"].strip()
        title = row["Title"].strip()
        band = row["Body words"].strip()
        parts = [p.strip() for p in _BAND_SPLIT_RE.split(band) if p.strip()]
        if not slug or len(parts) != 2:
            continue
        roster[slug] = (title, int(parts[0]), int(parts[1]))
    return roster


_ROLE_SECTION_RE = re.compile(
    r"^## (?P<title>[A-Za-z ]+)\n(?P<body>.*?)(?=^## |\Z)", re.MULTILINE | re.DOTALL
)
_QUESTIONS_BLOCK_RE = re.compile(
    r"\*\*Questions \(in order\):\*\*\n\n(?P<list>(?:\d+\.\s+.+\n)+)"
)
_QUESTION_LINE_RE = re.compile(r"^\d+\.\s+(?P<q>.+?)\s*$", re.MULTILINE)


def load_questions(
    contract_text: str,
    roster: dict[str, tuple[str, int, int]],
) -> dict[str, tuple[str, ...]]:
    """Parse each roster role's `## <Title>` section's `**Questions (in
    order):**` numbered list into slug -> ordered question tuple. A role
    section carrying no such block maps to an empty tuple."""
    title_to_slug = {title: slug for slug, (title, _lo, _hi) in roster.items()}
    questions: dict[str, tuple[str, ...]] = {slug: () for slug in roster}
    for m in _ROLE_SECTION_RE.finditer(contract_text):
        slug = title_to_slug.get(m.group("title").strip())
        if slug is None:
            continue
        qm = _QUESTIONS_BLOCK_RE.search(m.group("body"))
        if qm is None:
            continue
        questions[slug] = tuple(_QUESTION_LINE_RE.findall(qm.group("list")))
    return questions


# ---------------------------------------------------------------------------
# Source facts
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SourceFacts:
    chain_ids: frozenset[str]
    gt_declared: dict[str, bool]  # id -> read_at_source
    assumption_row_count: int
    dead_end_titles: frozenset[str]
    band: str
    numbers: frozenset[str]
    # Phase 87 D-05: §6's own **Recommended approach:** paragraph, label
    # removed, wrapped lines joined -- the sole text PV-DIRECTIVE's
    # verbatim-run check compares an answer against. Empty when §6 carries
    # no such paragraph.
    recommended_approach: str = ""


_SECTION6_CONFIDENCE_LINE_RE = re.compile(r"\b(HIGH|MEDIUM|LOW)\b")


def _read_section6_band(section6_text: str) -> str | None:
    """The first HIGH|MEDIUM|LOW token on the first section-6 line starting
    `**Confidence`."""
    for line in section6_text.splitlines():
        if line.strip().startswith("**Confidence"):
            m = _SECTION6_CONFIDENCE_LINE_RE.search(line)
            return m.group(1) if m else None
    return None


def source_facts(analysis_text: str) -> SourceFacts:
    sbmod = sb()
    qhmod = qh()
    try:
        sections = qhmod._slice_sections(analysis_text)
    except qhmod.SectionResolutionError as exc:
        raise SourceError(
            f"analysis text does not resolve into sections 1-6: {exc}"
        ) from exc
    chain_ids = frozenset(sbmod._doc_chain_index(sections.get(4, ""))[0])
    gt_declared = dict(sbmod._gt_declarations(sections.get(3, "")))
    assumption_row_count = len(
        sbmod._table_columns(sections.get(2, ""), ("Assumption",))
    )
    dead_end_titles = frozenset(
        re.sub(r"\s+", " ", m.group("name")).strip()
        for m in sbmod._DEAD_END_HEADING_RE.finditer(sections.get(5, ""))
    )
    band = _read_section6_band(sections.get(6, ""))
    if band is None:
        raise SourceError("no readable **Confidence:** band in section 6")
    numbers = frozenset(numbers_in(analysis_text))
    recommended_approach = _recommended_approach(sections.get(6, ""))
    return SourceFacts(
        chain_ids,
        gt_declared,
        assumption_row_count,
        dead_end_titles,
        band,
        numbers,
        recommended_approach,
    )


_RECOMMENDED_APPROACH_RE = re.compile(
    r"^\*\*Recommended approach:\*\*(?P<rest>.*?)(?=\n[ \t]*\n|\Z)",
    re.MULTILINE | re.DOTALL,
)


def _recommended_approach(section6_text: str) -> str:
    """The §6 **Recommended approach:** paragraph, label removed, wrapped
    lines joined into one line. Empty string if §6 carries no such
    paragraph."""
    m = _RECOMMENDED_APPROACH_RE.search(section6_text)
    if m is None:
        return ""
    return re.sub(r"\s+", " ", m.group("rest")).strip()


# ---------------------------------------------------------------------------
# numbers_in -- masks citation tokens and quoted dead-end spans, joins
# thousands separators, then returns the set of number cores.
# ---------------------------------------------------------------------------

_NUM_MASK_PATTERNS: tuple[re.Pattern, ...] = (
    re.compile(r'§5\s+"[^"]*"'),
    re.compile(r"GT-\d+\??"),
    re.compile(r"\bC\d+\b"),
    re.compile(r"\bA-\d+\b"),
    re.compile(r"§[1-6]\b"),
)
_THOUSANDS_RE = re.compile(r"(?<=\d),(?=\d{3}(?:\D|$))")
_NUMBER_CORE_RE = re.compile(r"\d+(?:\.\d+)?")


def numbers_in(text: str) -> set[str]:
    masked = text
    for pat in _NUM_MASK_PATTERNS:
        masked = pat.sub("", masked)
    joined = _THOUSANDS_RE.sub("", masked)
    return set(_NUMBER_CORE_RE.findall(joined))


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------

_TITLE_LINE_RE = re.compile(r"^# (?P<title>.+?) memo — (?P<atitle>\S.*)$")
# D-11 (Phase 87): the memo block is lines 3-6, each a blockquote field. To,
# Re and Basis end in a CommonMark hard-break backslash; Band does not. A
# missing hard-break backslash fails the field's own regex -- it is a miss,
# the same as a missing or mismatched value.
_MEMO_TO_RE = re.compile(r"^> \*\*To:\*\* (?P<v>.+?)\\$")
_MEMO_RE_RE = re.compile(r"^> \*\*Re:\*\* (?P<v>.+?)\\$")
_MEMO_BASIS_RE = re.compile(r"^> \*\*Basis:\*\* (?P<v>.+?)\\$")
_MEMO_BAND_RE = re.compile(
    r"^> \*\*Band \(from §6\):\*\* (?P<band>HIGH|MEDIUM|LOW)\s*$"
)
_MEMO_FIELDS: tuple[tuple[str, re.Pattern, str], ...] = (
    ("To", _MEMO_TO_RE, "v"),
    ("Re", _MEMO_RE_RE, "v"),
    ("Basis", _MEMO_BASIS_RE, "v"),
    ("Band", _MEMO_BAND_RE, "band"),
)


def source_h1(analysis_text: str) -> str | None:
    """The text after `# ` of the first line that starts with exactly one
    hash and a space, outside a fenced code block (``` or ~~~ toggles), or
    None when the analysis has no such heading."""
    fence: str | None = None
    for line in analysis_text.split("\n"):
        stripped = line.lstrip()
        marker = stripped[:3]
        if marker in ("```", "~~~"):
            if fence is None:
                fence = marker
            elif fence == marker:
                fence = None
            continue
        if fence is None and line.startswith("# "):
            return line[2:].strip()
    return None


def normalise_title(s: str) -> str:
    """Normalisation applied to both sides of the analysis-title comparison:
    strip markdown emphasis and code markers (`**`, `*`, backtick), collapse
    whitespace runs to one space, strip the ends. Underscores are kept
    (titles may carry snake_case identifiers) and case is not folded (a case
    change is a real difference)."""
    for mark in ("**", "*", "`"):
        s = s.replace(mark, "")
    return " ".join(s.split())


def basis_value(analysis_name: str) -> str:
    """D-12 (plan 87-11): the Basis field links the analysis, its reader
    report and the folder index -- the three files beside the view. The
    report's name swaps the analysis's `analysis-` prefix for `report-`, the
    same mapping the agent's delivery step 6 uses; a name without that prefix
    (a hand-written fixture named after its worked example) is prefixed."""
    report = "report-" + analysis_name.removeprefix("analysis-")
    return f"[{analysis_name}]({analysis_name}) · [Report]({report}) · [All files](INDEX.md)"


@dataclass
class HeaderResult:
    role: str | None
    band: str | None
    body: str
    findings: list[Finding] = field(default_factory=list)
    atitle: str | None = None


def split_header(
    persona_text: str, analysis_name: str, roster: dict[str, tuple[str, int, int]]
) -> HeaderResult:
    """D-11: parse the nine-line memo header -- a title line, a blank, the
    To/Re/Basis/Band blockquote block (lines 3-6), a blank, the provenance
    sentence (line 8), a blank, then the body. Each memo-field miss (missing,
    malformed, or disagreeing with line 1 / the analysis name) is its own
    PV-HEADER finding naming the field; header finding details echo header
    lines only, never body text."""
    findings: list[Finding] = []
    lines = persona_text.split("\n")
    title_to_slug = {title: slug for slug, (title, _lo, _hi) in roster.items()}

    role: str | None = None
    title: str | None = None
    atitle: str | None = None
    if lines:
        m = _TITLE_LINE_RE.match(lines[0])
        if m and m.group("title") in title_to_slug:
            role = title_to_slug[m.group("title")]
            title = m.group("title")
            atitle = m.group("atitle")
        else:
            findings.append(
                Finding(
                    "PV-HEADER", f"line 1 does not match a roster title: {lines[0]!r}"
                )
            )
    else:
        findings.append(Finding("PV-HEADER", "persona file is empty"))

    # The memo block is the contiguous run of lines starting `>` from line 3
    # (index 2). A file carrying no such run (e.g. the frozen pre-87
    # fixture) gets one "memo block missing" finding instead of four
    # per-field misses, and the provenance search falls back to line 2 on.
    memo_lines: list[str] = []
    i = 2
    while i < len(lines) and lines[i].startswith(">"):
        memo_lines.append(lines[i])
        i += 1

    band: str | None = None
    if not memo_lines:
        findings.append(
            Finding("PV-HEADER", "memo block missing (lines 3-6 do not start with '>')")
        )
        search_start = 1
    else:
        values: dict[str, str] = {}
        for idx, (name, pattern, group) in enumerate(_MEMO_FIELDS):
            if idx >= len(memo_lines):
                findings.append(Finding("PV-HEADER", f"memo field {name} missing"))
                continue
            line = memo_lines[idx]
            m = pattern.match(line)
            if not m:
                findings.append(
                    Finding("PV-HEADER", f"memo field {name} malformed: {line!r}")
                )
                continue
            values[name] = m.group(group)
        if "To" in values and title is not None and values["To"] != title:
            findings.append(
                Finding(
                    "PV-HEADER",
                    f"To field {values['To']!r} disagrees with line 1's title {title!r}",
                )
            )
        if "Re" in values and atitle is not None and values["Re"] != atitle:
            findings.append(
                Finding(
                    "PV-HEADER",
                    f"Re field {values['Re']!r} disagrees with line 1's analysis title {atitle!r}",
                )
            )
        if "Basis" in values and values["Basis"] != basis_value(analysis_name):
            findings.append(
                Finding(
                    "PV-HEADER",
                    f"Basis field {values['Basis']!r} is not the linked form for {analysis_name!r}",
                )
            )
        band = values.get("Band")
        search_start = 2 + len(memo_lines)

    # The provenance line is the first non-blank line after the memo block.
    # A line that opens the provenance shape but disagrees in content is a
    # mismatch finding (still consumed); a line that is not provenance-shaped
    # at all is a "provenance line missing" finding, and the body starts AT
    # that line so no body paragraph is ever swallowed.
    expected_provenance = "*" + PROVENANCE_TEMPLATE.format(name=analysis_name) + "*"
    j = search_start
    while j < len(lines) and lines[j].strip() == "":
        j += 1
    if j >= len(lines):
        findings.append(
            Finding("PV-HEADER", "no provenance line found after the memo block")
        )
        body_start = j
    elif lines[j].strip().startswith("*Derived from"):
        if lines[j].strip() != expected_provenance:
            findings.append(
                Finding(
                    "PV-HEADER",
                    f"provenance line does not match the expected sentence: {lines[j]!r}",
                )
            )
        body_start = j + 1
    else:
        findings.append(Finding("PV-HEADER", "provenance line missing"))
        body_start = j

    body_lines = lines[body_start:]
    while body_lines and body_lines[0].strip() == "":
        body_lines.pop(0)
    body = "\n".join(body_lines)
    return HeaderResult(
        role=role, band=band, body=body, findings=findings, atitle=atitle
    )


# ---------------------------------------------------------------------------
# Body shape
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class BodyUnit:
    kind: str  # "paragraph" | "bullet" | "violation"
    text: str


_HEADING_RE = re.compile(r"^\s*#{1,6}\s")
_TABLE_ROW_RE = re.compile(r"^\s*\|")
_CODE_FENCE_RE = re.compile(r"^\s*```")
_NUMBERED_RE = re.compile(r"^\s*\d+[.)]\s")
_BLOCKQUOTE_RE = re.compile(r"^\s*>")
_BULLET_RE = re.compile(r"^-\s+(?P<text>.*)$")


def body_units(body: str) -> list[BodyUnit]:
    units: list[BodyUnit] = []
    paragraph_lines: list[str] = []

    def flush() -> None:
        if paragraph_lines:
            units.append(BodyUnit("paragraph", " ".join(paragraph_lines)))
            paragraph_lines.clear()

    for raw_line in body.split("\n"):
        if raw_line.strip() == "":
            flush()
            continue
        if (
            _HEADING_RE.match(raw_line)
            or _TABLE_ROW_RE.match(raw_line)
            or _CODE_FENCE_RE.match(raw_line)
            or _NUMBERED_RE.match(raw_line)
            or _BLOCKQUOTE_RE.match(raw_line)
        ):
            flush()
            units.append(BodyUnit("violation", raw_line.strip()))
            continue
        bm = _BULLET_RE.match(raw_line)
        if bm:
            flush()
            units.append(BodyUnit("bullet", bm.group("text")))
            continue
        paragraph_lines.append(raw_line.strip())
    flush()
    return units


# ---------------------------------------------------------------------------
# Sentences -- a sentence ends at `.`/`?`/`!` followed by whitespace or EOL,
# except the `?` closing a `GT-n?` id, the `.` inside a decimal, or either
# inside a quoted §5 title (D-06).
# ---------------------------------------------------------------------------

_GT_Q_RE = re.compile(r"GT-\d+\?")
_QUOTED_DEADEND_RE = re.compile(r'§5\s+"([^"]*)"')
# Abbreviations whose period is not a sentence end (84-REVIEW WR-03). "etc."
# is deliberately absent: it usually ends a sentence, and masking it would
# merge two sentences into one citation unit.
_ABBREV_RE = re.compile(r"\b(?:e\.g|i\.e|vs|cf)\.")
_DECIMAL_RE = re.compile(r"(?<=\d)\.(?=\d)")
_UNMASK = {"\x00": ".", "\x01": "?", "\x02": "!"}
_TERMINATOR_SPLIT_RE = re.compile(r"(?<=[.?!])(?:\s+|$)")


def _mask_sentence_breaks(text: str) -> str:
    chars = list(text)
    for pat in (_GT_Q_RE, _QUOTED_DEADEND_RE, _ABBREV_RE):
        for m in pat.finditer(text):
            for i in range(m.start(), m.end()):
                c = chars[i]
                if c == ".":
                    chars[i] = "\x00"
                elif c == "?":
                    chars[i] = "\x01"
                elif c == "!":
                    chars[i] = "\x02"
    for m in _DECIMAL_RE.finditer(text):
        chars[m.start()] = "\x00"
    return "".join(chars)


def sentences(unit_text: str) -> list[str]:
    masked = _mask_sentence_breaks(unit_text)
    parts = _TERMINATOR_SPLIT_RE.split(masked)
    result = []
    for p in parts:
        if p == "":
            continue
        restored = "".join(_UNMASK.get(c, c) for c in p)
        result.append(restored)
    return result


# ---------------------------------------------------------------------------
# Citation presence and resolution
# ---------------------------------------------------------------------------

# Every token needs a leading word boundary (84-REVIEW CR-01): without it,
# "SPEC1" or "RFC2119" satisfied the C<n> alternative and an uncited
# sentence passed as cited.
_CITATION_PRESENT_RE = re.compile(r"\bC\d+\b|\bGT-\d+\??|\bA-\d+\b|§[1-6]\b")
_RESOLVE_GT_RE = re.compile(r"GT-(\d+)(\??)")
_RESOLVE_CHAIN_RE = re.compile(r"\bC(\d+)\b")
_RESOLVE_A_RE = re.compile(r"\bA-(\d+)\b")


def resolve_ids(body_text: str, facts: SourceFacts) -> list[Finding]:
    findings: list[Finding] = []

    for m in _QUOTED_DEADEND_RE.finditer(body_text):
        title = m.group(1)
        if title not in facts.dead_end_titles:
            findings.append(
                Finding("PV-DEADEND", f'quoted §5 title not found in §5: "{title}"')
            )

    masked = _QUOTED_DEADEND_RE.sub(
        lambda m: "§Q" + " " * (len(m.group(0)) - 2), body_text
    )

    for m in _RESOLVE_GT_RE.finditer(masked):
        gid = f"GT-{m.group(1)}"
        has_q = m.group(2) == "?"
        if gid not in facts.gt_declared:
            findings.append(
                Finding("PV-ID", f"{gid}{'?' if has_q else ''} not declared in §3")
            )
            continue
        expected_q = not facts.gt_declared[gid]
        if has_q != expected_q:
            findings.append(
                Finding(
                    "PV-ID",
                    f"{gid}{'?' if has_q else ''} marking disagrees with §3's declaration",
                )
            )

    for m in _RESOLVE_CHAIN_RE.finditer(masked):
        cid = f"C{m.group(1)}"
        if cid not in facts.chain_ids:
            findings.append(Finding("PV-ID", f"{cid} not declared in §4"))

    for m in _RESOLVE_A_RE.finditer(masked):
        n = int(m.group(1))
        if not (1 <= n <= facts.assumption_row_count):
            findings.append(
                Finding(
                    "PV-ID",
                    f"A-{n} outside the Assumptions Table's row range (1..{facts.assumption_row_count})",
                )
            )

    return findings


# ---------------------------------------------------------------------------
# Guide checks (Phase 83 D-04)
# ---------------------------------------------------------------------------

_GUIDE_BACKTICK_RE = re.compile(r"`([^`]+)`")
_GUIDE_QUOTE_RE = re.compile(r'["“]([^"”]+)["”]')


def _normalize_ws(s: str) -> str:
    return re.sub(r"\s+", " ", s)


def check_guide(guide_text: str, template_text: str) -> list[Finding]:
    findings: list[Finding] = []
    lines = guide_text.split("\n")
    body_text = "\n".join(lines[1:]) if len(lines) > 1 else ""
    word_count = len(body_text.split())
    if word_count > GUIDE_MAX_WORDS:
        findings.append(
            Finding(
                "PV-GUIDE-WORDS",
                f"guide body is {word_count} words, exceeds {GUIDE_MAX_WORDS}",
            )
        )
    g = _normalize_ws(guide_text)
    t = _normalize_ws(template_text)
    names = _GUIDE_BACKTICK_RE.findall(g) + _GUIDE_QUOTE_RE.findall(g)
    for name in names:
        if name not in t:
            findings.append(
                Finding(
                    "PV-GUIDE-NAME",
                    f"name not found verbatim in output-template.md: {name!r}",
                )
            )
    return findings


# ---------------------------------------------------------------------------
# Questions (Phase 87 D-11): the body is a memo -- an `In brief:` paragraph
# first, then exactly one paragraph per the role's fixed question, in order.
# The questions are never printed; there is no citation exemption left for
# any unit (the old bullet-lead-in exemption was a feature of the bullet
# format this plan retires).
# ---------------------------------------------------------------------------

_BOLD_LEAD_RE = re.compile(r"^\*\*[^*]+\*\*")


def check_questions(
    units: list[BodyUnit],
    expected: tuple[str, ...],
) -> tuple[list[Finding], list[str]]:
    """Walk the body's paragraph/bullet units against the memo structure.

    Returns (findings, citation_texts): citation_texts is every unit's full
    text -- no exemption remains, so the PV-UNCITED sentence loop checks the
    `In brief:` paragraph exactly like every other unit. Findings name only
    paragraph positions or the contract's own question text, never body
    text, so a finding detail cannot leak a user's private analysis prose.
    """
    findings: list[Finding] = []
    citations = [u.text for u in units]

    for i, u in enumerate(units, start=1):
        if u.kind == "bullet":
            findings.append(
                Finding("PV-QUESTIONS", f"bullet line in a memo body (paragraph {i})")
            )
            continue
        if _BOLD_LEAD_RE.match(u.text):
            findings.append(
                Finding("PV-QUESTIONS", f"paragraph {i} opens with a bold label")
            )

    if not units or not units[0].text.startswith(IN_BRIEF_PREFIX + " "):
        findings.append(
            Finding("PV-QUESTIONS", "first paragraph does not open with 'In brief:'")
        )

    expected_count = 1 + len(expected)
    if len(units) != expected_count:
        findings.append(
            Finding(
                "PV-QUESTIONS",
                f"expected {expected_count} paragraphs (In brief plus one per question), "
                f"found {len(units)}",
            )
        )

    combined = " ".join(u.text for u in units)
    for q in expected:
        if q in combined:
            findings.append(
                Finding("PV-QUESTIONS", f"fixed question printed in the body: {q!r}")
            )

    return findings, citations


# ---------------------------------------------------------------------------
# Voice (Phase 87 D-05): an answer sentence never hands down a decision --
# PV-DIRECTIVE is lexical and over-reports by design (CLAUDE.md: a noisy
# falsifier that fires beats a clean presence check that does not).
# ---------------------------------------------------------------------------

_LEADING_NONLETTER_RE = re.compile(r"^[^A-Za-z]+")
_TRAILING_PUNCT_RE = re.compile(r"[:;.,!?]+$")
_VOICE_TOKEN_RE = re.compile(r"[a-z0-9]+(?:['’-][a-z0-9]+)*")


def _voice_tokens(text: str) -> list[str]:
    """Citation tokens and markdown emphasis stripped, lowercased, split
    into word tokens. Reuses `_NUM_MASK_PATTERNS` -- the same citation-token
    shapes `numbers_in` already masks out."""
    masked = text
    for pat in _NUM_MASK_PATTERNS:
        masked = pat.sub("", masked)
    masked = masked.replace("*", "").lower()
    return _VOICE_TOKEN_RE.findall(masked)


def _sentence_opener_words(sentence: str) -> list[str]:
    """Leading non-letters stripped, then each whitespace-split token with
    trailing `:,;.!?` stripped and lowercased."""
    stripped = _LEADING_NONLETTER_RE.sub("", sentence)
    return [_TRAILING_PUNCT_RE.sub("", w).lower() for w in stripped.split()]


def _longest_shared_run(a: list[str], b: list[str]) -> int:
    """Longest contiguous run of tokens appearing, in the same order, as a
    contiguous subsequence of both `a` and `b`."""
    if not a or not b:
        return 0
    prev = [0] * (len(b) + 1)
    best = 0
    for ai in a:
        curr = [0] * (len(b) + 1)
        for j, bj in enumerate(b, start=1):
            if ai == bj:
                curr[j] = prev[j - 1] + 1
                best = max(best, curr[j])
        prev = curr
    return best


def check_voice(answer_texts: list[str], facts: SourceFacts) -> list[Finding]:
    """D-05 PV-DIRECTIVE: flags an answer sentence that opens with a
    denylisted imperative or the "Do not"/"don't" phrase, an answer that
    addresses the reader in the second person or passes a verdict on the
    reader, or an answer sharing a long verbatim run of words with §6's
    Recommended approach paragraph. Over-reports by design; proves none of
    these phrasings are present, never that the answer's meaning is sound.
    The question text itself is never passed here -- only the answer that
    follows it."""
    findings: list[Finding] = []
    source_tokens = (
        _voice_tokens(facts.recommended_approach) if facts.recommended_approach else []
    )
    for answer in answer_texts:
        for s in sentences(answer):
            if not s.strip():
                continue
            words = _sentence_opener_words(s)
            if not words:
                continue
            first = words[0]
            if first in DIRECTIVE_OPENERS:
                findings.append(
                    Finding(
                        "PV-DIRECTIVE",
                        f"answer sentence opens with a denylisted imperative: {first.capitalize()}",
                    )
                )
                continue
            for phrase in DIRECTIVE_PHRASE_OPENERS:
                if tuple(words[: len(phrase)]) == phrase:
                    findings.append(
                        Finding("PV-DIRECTIVE", "answer sentence opens with 'Do not'")
                    )
                    break
        if _SECOND_PERSON_RE.search(answer):
            findings.append(Finding("PV-DIRECTIVE", "second-person address"))
        if _READER_VERDICT_RE.search(answer):
            findings.append(Finding("PV-DIRECTIVE", "verdict on the reader"))
        if source_tokens:
            run = _longest_shared_run(_voice_tokens(answer), source_tokens)
            if run >= VERBATIM_RUN_WORDS:
                findings.append(
                    Finding(
                        "PV-DIRECTIVE",
                        f"shares {run}+ consecutive words with §6's recommended approach",
                    )
                )
    return findings


# ---------------------------------------------------------------------------
# check_view
# ---------------------------------------------------------------------------


def check_view(
    persona_text: str,
    analysis_text: str,
    analysis_name: str,
    roster: dict[str, tuple[str, int, int]],
    *,
    questions: dict[str, tuple[str, ...]] | None = None,
) -> list[Finding]:
    try:
        facts = source_facts(analysis_text)
    except SourceError as exc:
        return [Finding("PV-SOURCE", str(exc))]

    if questions is None:
        questions = load_questions(CONTRACT.read_text(), roster)

    header = split_header(persona_text, analysis_name, roster)
    findings: list[Finding] = list(header.findings)

    if header.atitle is not None:
        h1 = source_h1(analysis_text)
        if h1 is None:
            findings.append(
                Finding(
                    "PV-HEADER",
                    "source analysis has no H1 to compare line 1's analysis title with",
                )
            )
        elif normalise_title(header.atitle) != normalise_title(h1):
            findings.append(
                Finding(
                    "PV-HEADER",
                    f"line 1's analysis title {header.atitle!r} disagrees with the source analysis's H1 {h1!r}",
                )
            )

    units = body_units(header.body)
    for u in units:
        if u.kind == "violation":
            findings.append(
                Finding("PV-SHAPE", f"non-paragraph/bullet content in body: {u.text!r}")
            )
    valid_units = [u for u in units if u.kind != "violation"]
    combined_text = "\n".join(u.text for u in valid_units)

    if header.role is not None:
        _title, lo, hi = roster[header.role]
        word_count = sum(len(u.text.split()) for u in valid_units)
        if not (lo <= word_count <= hi):
            findings.append(
                Finding(
                    "PV-WORDS",
                    f"body is {word_count} words, outside the {header.role} band [{lo}, {hi}]",
                )
            )

    if header.role is not None:
        q_findings, citation_texts = check_questions(
            valid_units, questions.get(header.role, ())
        )
        findings.extend(q_findings)
    else:
        citation_texts = [u.text for u in valid_units]

    findings.extend(check_voice(citation_texts, facts))

    for text in citation_texts:
        for s in sentences(text):
            if s.strip() and not _CITATION_PRESENT_RE.search(s):
                findings.append(
                    Finding("PV-UNCITED", f"no citation token: {s.strip()!r}")
                )

    findings.extend(resolve_ids(combined_text, facts))

    body_numbers = numbers_in(combined_text)
    missing_numbers = body_numbers - facts.numbers
    if missing_numbers:
        findings.append(
            Finding(
                "PV-NUMBER",
                f"number(s) not present in the source analysis: {sorted(missing_numbers)}",
            )
        )

    if header.band is not None and header.band != facts.band:
        findings.append(
            Finding(
                "PV-BAND",
                f"Band line {header.band} disagrees with the source's §6 band {facts.band}",
            )
        )

    return findings


# ---------------------------------------------------------------------------
# --self-test
# ---------------------------------------------------------------------------


def _load_roster_from_contract() -> dict[str, tuple[str, int, int]]:
    return load_roster(CONTRACT.read_text())


def _p01_fixtures_clean() -> str | None:
    roster = _load_roster_from_contract()
    for name, src in FIXTURES:
        persona_text = (FIXTURE_DIR / name).read_text()
        analysis_text = (REPO_ROOT / src).read_text()
        findings = check_view(persona_text, analysis_text, Path(src).name, roster)
        if findings:
            return f"{name}: expected zero findings, got {findings}"
    return None


_ABSENT_SENTENCE_RE = re.compile(r'^- "([^"]+)"\s*$', re.MULTILINE)


def _p02_contract_parity() -> str | None:
    contract_text = CONTRACT.read_text()
    roster = load_roster(contract_text)
    if roster != LOCKED_ROSTER:
        return f"roster {roster} does not equal LOCKED_ROSTER {LOCKED_ROSTER}"
    found = _ABSENT_SENTENCE_RE.findall(contract_text)
    if not found:
        return "no absent-input sentences found in the contract"
    for text in found:
        for s in sentences(text):
            if not _CITATION_PRESENT_RE.search(s):
                return f"absent-input sentence has no citation token: {text!r}"
        if numbers_in(text):
            return f"absent-input sentence carries an unexpected number: {text!r}"
    return None


def _p04_questions_parity() -> str | None:
    contract_text = CONTRACT.read_text()
    roster = load_roster(contract_text)
    questions = load_questions(contract_text, roster)
    if questions != LOCKED_QUESTIONS:
        return (
            f"questions {questions} does not equal LOCKED_QUESTIONS {LOCKED_QUESTIONS}"
        )
    for slug, qs in questions.items():
        for q in qs:
            if not q.endswith("?"):
                return f"{slug} question does not end in '?': {q!r}"
            if _CITATION_PRESENT_RE.search(q):
                return f"{slug} question carries a citation token: {q!r}"
            if numbers_in(q):
                return f"{slug} question carries an unexpected number: {q!r}"
            if re.search(r"\byou\b|\byour\b", q, re.IGNORECASE):
                return f"{slug} question carries you/your: {q!r}"
    return None


_DENYLIST_LINE_RE = re.compile(
    r'^\*\*Denylisted openers:\*\* (?P<list>.+?); and the two-word opener "Do not"\.$',
    re.MULTILINE,
)


def _p05_denylist_parity(contract_path: Path = CONTRACT) -> str | None:
    """P05: the contract's own **Denylisted openers:** line (Voice section)
    is the sole source for DIRECTIVE_OPENERS -- a hand-edited constant
    cannot silently drift from the contract's own prose."""
    contract_text = contract_path.read_text()
    m = _DENYLIST_LINE_RE.search(contract_text)
    if m is None:
        return "Denylisted openers line not found, or does not match the expected shape"
    openers = frozenset(
        w.strip().lower() for w in m.group("list").split(", ") if w.strip()
    )
    if openers != DIRECTIVE_OPENERS:
        return f"contract openers {sorted(openers)} != DIRECTIVE_OPENERS {sorted(DIRECTIVE_OPENERS)}"
    return None


def _p03_guide_passes() -> str | None:
    if not GUIDE.exists():
        return "shared/spine/references/how-to-read.md is absent (Phase 83 prerequisite missing)"
    findings = check_guide(GUIDE.read_text(), TEMPLATE.read_text())
    if findings:
        return f"expected zero findings against the shipped guide, got {findings}"
    return None


def _m_uncited(text: str) -> str:
    # Strip the trailing citation from one specific, uniquely-occurring sentence
    # that carries no other citation token, leaving the sentence otherwise
    # unchanged.
    anchor = "If that evidence improves, the recommendation is reconsidered (C3)."
    replacement = "If that evidence improves, the recommendation is reconsidered."
    return text.replace(anchor, replacement, 1)


def _m_remove_provenance(text: str) -> str:
    # D-11: the provenance line now sits after the memo block (line 8), not
    # at a fixed index -- find it by its own opening text.
    lines = text.split("\n")
    idx = next((i for i, l in enumerate(lines) if l.startswith("*Derived from")), None)
    if idx is not None:
        del lines[idx]
    return "\n".join(lines)


def _m_pad_over(text: str) -> str:
    # Padding strong enough to clear the roster band's ceiling (170) with
    # margin over the widest fixture (150 words at plan time). Appended to
    # the end of the last paragraph's own physical line (never as a new
    # paragraph) so the memo's exact paragraph-count shape survives the
    # mutation and only PV-WORDS fires, not PV-QUESTIONS.
    padding = (
        " The engineering team has 3.2 engineer-quarters of capacity this quarter (C1)."
    )
    return text.rstrip("\n") + padding * 10 + "\n"


def _m_cut_under(text: str) -> str:
    # In brief plus four short, validly-shaped paragraphs -- 17 body words
    # total, below the roster's 90-word floor, so this mutation trips
    # PV-WORDS alone, never PV-QUESTIONS: the paragraph count and the In
    # brief opener are both still correct.
    lines = text.split("\n")
    prov_idx = next(i for i, l in enumerate(lines) if l.startswith("*Derived from"))
    head = lines[: prov_idx + 1]
    paragraphs = ["In brief: stated in §6."] + ["Stated in §6."] * 4
    short_body: list[str] = [""]
    for idx, p in enumerate(paragraphs):
        if idx:
            short_body.append("")
        short_body.append(p)
    return "\n".join(head + short_body)


def _m_insert_shape(text: str) -> str:
    lines = text.split("\n")
    idx = next(i for i, l in enumerate(lines) if l.startswith("In brief:"))
    lines.insert(idx, "## Extra")
    return "\n".join(lines)


def _m_deadend(text: str) -> str:
    original = '§5 "Sixty percent of polled customers said they want Slack, therefore build Slack"'
    mutated = '§5 "Fifty percent of polled customers said they want Slack, therefore build Slack"'
    return text.replace(original, mutated, 1)


# D-11 Phase 87: the decision-owner fixture's paragraph 3 (the Q2 answer)
# is the anchor every M-Q-* question-structure control mutates.
_M_Q_P3_ANCHOR = "It has settled that the reporting rewrite carries a signed commitment"


def _m_q_bullet(text: str) -> str:
    return text.replace(_M_Q_P3_ANCHOR, "- " + _M_Q_P3_ANCHOR, 1)


def _m_q_brief(text: str) -> str:
    return text.replace("In brief: ", "", 1)


def _m_q_few(text: str) -> str:
    anchor = "since capacity binds to one candidate (C1).\n\n" + _M_Q_P3_ANCHOR
    replacement = "since capacity binds to one candidate (C1).\n" + _M_Q_P3_ANCHOR
    return text.replace(anchor, replacement, 1)


def _m_q_many(text: str) -> str:
    return text.replace(
        " If that evidence improves", "\n\nIf that evidence improves", 1
    )


def _m_q_print(text: str) -> str:
    return text.replace(
        _M_Q_P3_ANCHOR,
        "**What has it settled that I can rely on?** " + _M_Q_P3_ANCHOR,
        1,
    )


def _m_h_to(text: str) -> str:
    return text.replace("> **To:** Decision Owner\\", "> **To:** Operator\\", 1)


# D-12 (plan 87-11): the pre-link bare Basis must fail, and so must a link
# whose report target names a different analysis than the view's own.
_M_H_BASIS_LINKED = (
    "> **Basis:** [product-business-2.md](product-business-2.md) · "
    "[Report](report-product-business-2.md) · [All files](INDEX.md)\\"
)


def _m_h_basis(text: str) -> str:
    return text.replace(_M_H_BASIS_LINKED, "> **Basis:** product-business-2.md\\", 1)


def _m_h_link(text: str) -> str:
    return text.replace(
        _M_H_BASIS_LINKED,
        _M_H_BASIS_LINKED.replace(
            "(report-product-business-2.md)", "(report-personal-general.md)"
        ),
        1,
    )


def _m_h_break(text: str) -> str:
    return text.replace("> **To:** Decision Owner\\", "> **To:** Decision Owner", 1)


# D-05 Phase 87: all three mutations replace the same single anchor sentence
# in the decision-owner fixture, so each is a single-code probe of exactly
# one PV-DIRECTIVE trigger (denylisted opener / second-person / verbatim
# run) without disturbing any other check (citation, word band, shape).
_M_D_ANCHOR = "If that evidence improves, the recommendation is reconsidered (C3)."


def _m_d_open(text: str) -> str:
    return text.replace(_M_D_ANCHOR, "Decide again if that evidence improves (C3).", 1)


def _m_d_you(text: str) -> str:
    return text.replace(
        _M_D_ANCHOR,
        "If that evidence improves, you should reconsider the recommendation (C3).",
        1,
    )


def _m_d_run(text: str) -> str:
    # Shares "defer the slack integration to the next planning cycle" (9
    # words) with product-business-2.md's §6 Recommended approach paragraph.
    return text.replace(
        _M_D_ANCHOR,
        "Under that evidence, defer the Slack integration to the next planning cycle (C3).",
        1,
    )


_MUTATIONS: tuple[tuple[str, str, str, Callable[[str], str], frozenset[str]], ...] = (
    (
        "M-ID",
        "product-business-2-decision-owner.md",
        "shared/examples/product-business-2.md",
        lambda t: t.replace("GT-5?", "GT-6"),
        frozenset({"PV-ID"}),
    ),
    (
        "M-AGREE",
        "product-business-2-decision-owner.md",
        "shared/examples/product-business-2.md",
        lambda t: t.replace("GT-5?", "GT-5"),
        frozenset({"PV-ID"}),
    ),
    (
        "M-NUMBER",
        "product-business-2-decision-owner.md",
        "shared/examples/product-business-2.md",
        lambda t: t.replace("$180,000", "$190,000"),
        frozenset({"PV-NUMBER"}),
    ),
    (
        "M-UNCITED",
        "product-business-2-decision-owner.md",
        "shared/examples/product-business-2.md",
        _m_uncited,
        frozenset({"PV-UNCITED"}),
    ),
    # 84-REVIEW CR-01: a token that merely ENDS in C<digits> (SPEC1) is not a
    # citation; the stripped sentence must still read as uncited.
    (
        "M-PSEUDO",
        "product-business-2-decision-owner.md",
        "shared/examples/product-business-2.md",
        lambda t: _m_uncited(t).replace(
            "the recommendation is reconsidered.",
            "the recommendation is reconsidered per SPEC1.",
            1,
        ),
        frozenset({"PV-UNCITED"}),
    ),
    (
        "M-BAND",
        "product-business-2-decision-owner.md",
        "shared/examples/product-business-2.md",
        lambda t: t.replace("**Band (from §6):** MEDIUM", "**Band (from §6):** HIGH"),
        frozenset({"PV-BAND"}),
    ),
    (
        "M-HEADER",
        "product-business-2-decision-owner.md",
        "shared/examples/product-business-2.md",
        _m_remove_provenance,
        frozenset({"PV-HEADER"}),
    ),
    (
        "M-ATITLE",
        "product-business-2-decision-owner.md",
        "shared/examples/product-business-2.md",
        lambda t: t.replace(
            "Worked Example: Product and Business (Feature Prioritization)",
            "Worked Example: Something Else",
        ),
        frozenset({"PV-HEADER"}),
    ),
    (
        "M-OVER",
        "product-business-2-decision-owner.md",
        "shared/examples/product-business-2.md",
        _m_pad_over,
        frozenset({"PV-WORDS"}),
    ),
    (
        "M-UNDER",
        "product-business-2-decision-owner.md",
        "shared/examples/product-business-2.md",
        _m_cut_under,
        frozenset({"PV-WORDS"}),
    ),
    (
        "M-SHAPE",
        "product-business-2-decision-owner.md",
        "shared/examples/product-business-2.md",
        _m_insert_shape,
        frozenset({"PV-SHAPE"}),
    ),
    (
        "M-DEADEND",
        "product-business-2-skeptic.md",
        "shared/examples/product-business-2.md",
        _m_deadend,
        frozenset({"PV-DEADEND"}),
    ),
    (
        "M-Q-BULLET",
        "product-business-2-decision-owner.md",
        "shared/examples/product-business-2.md",
        _m_q_bullet,
        frozenset({"PV-QUESTIONS"}),
    ),
    (
        "M-Q-BRIEF",
        "product-business-2-decision-owner.md",
        "shared/examples/product-business-2.md",
        _m_q_brief,
        frozenset({"PV-QUESTIONS"}),
    ),
    (
        "M-Q-FEW",
        "product-business-2-decision-owner.md",
        "shared/examples/product-business-2.md",
        _m_q_few,
        frozenset({"PV-QUESTIONS"}),
    ),
    (
        "M-Q-MANY",
        "product-business-2-decision-owner.md",
        "shared/examples/product-business-2.md",
        _m_q_many,
        frozenset({"PV-QUESTIONS"}),
    ),
    (
        "M-Q-PRINT",
        "product-business-2-decision-owner.md",
        "shared/examples/product-business-2.md",
        _m_q_print,
        frozenset({"PV-QUESTIONS"}),
    ),
    (
        "M-H-TO",
        "product-business-2-decision-owner.md",
        "shared/examples/product-business-2.md",
        _m_h_to,
        frozenset({"PV-HEADER"}),
    ),
    (
        "M-H-BREAK",
        "product-business-2-decision-owner.md",
        "shared/examples/product-business-2.md",
        _m_h_break,
        frozenset({"PV-HEADER"}),
    ),
    (
        "M-H-BASIS",
        "product-business-2-decision-owner.md",
        "shared/examples/product-business-2.md",
        _m_h_basis,
        frozenset({"PV-HEADER"}),
    ),
    (
        "M-H-LINK",
        "product-business-2-decision-owner.md",
        "shared/examples/product-business-2.md",
        _m_h_link,
        frozenset({"PV-HEADER"}),
    ),
    (
        "M-D-OPEN",
        "product-business-2-decision-owner.md",
        "shared/examples/product-business-2.md",
        _m_d_open,
        frozenset({"PV-DIRECTIVE"}),
    ),
    (
        "M-D-YOU",
        "product-business-2-decision-owner.md",
        "shared/examples/product-business-2.md",
        _m_d_you,
        frozenset({"PV-DIRECTIVE"}),
    ),
    (
        "M-D-RUN",
        "product-business-2-decision-owner.md",
        "shared/examples/product-business-2.md",
        _m_d_run,
        frozenset({"PV-DIRECTIVE"}),
    ),
)


def _make_mutation_control(
    fixture_name: str,
    src_relpath: str,
    build: Callable[[str], str],
    expected_codes: frozenset[str],
) -> Callable[[], str | None]:
    def _control() -> str | None:
        persona_text = (FIXTURE_DIR / fixture_name).read_text()
        mutated = build(persona_text)
        if mutated == persona_text:
            return "mutation was a no-op"
        analysis_text = (REPO_ROOT / src_relpath).read_text()
        roster = _load_roster_from_contract()
        findings = check_view(mutated, analysis_text, Path(src_relpath).name, roster)
        codes = {f.code for f in findings}
        if codes != expected_codes:
            return (
                f"expected {sorted(expected_codes)}, got {sorted(codes)} ({findings})"
            )
        return None

    return _control


def _m_guide_name(text: str) -> str:
    return text.replace('"Recommendation"', '"Nonexistent Section Name"', 1)


def _m_guide_words(text: str) -> str:
    words = text.split()
    filler = " ".join(words[:15])
    return text + "\n\n" + filler + " " + filler


_GUIDE_MUTATIONS: tuple[tuple[str, Callable[[str], str], frozenset[str]], ...] = (
    ("G-NAME", _m_guide_name, frozenset({"PV-GUIDE-NAME"})),
    ("G-WORDS", _m_guide_words, frozenset({"PV-GUIDE-WORDS"})),
)


def _make_guide_control(
    build: Callable[[str], str],
    expected_codes: frozenset[str],
) -> Callable[[], str | None]:
    def _control() -> str | None:
        guide_text = GUIDE.read_text()
        mutated = build(guide_text)
        if mutated == guide_text:
            return "mutation was a no-op"
        findings = check_guide(mutated, TEMPLATE.read_text())
        codes = {f.code for f in findings}
        if codes != expected_codes:
            return (
                f"expected {sorted(expected_codes)}, got {sorted(codes)} ({findings})"
            )
        return None

    return _control


def _u01_numbers() -> str | None:
    got = numbers_in("$180,000/year, 3.2, 17%, 3–5, GT-5? C1 A-3 §6")
    want = {"180000", "3.2", "17", "3", "5"}
    if got != want:
        return f"expected {want}, got {got}"
    return None


def _u02_sentence_boundaries() -> str | None:
    text = (
        "The chain cites GT-5? and 3.2 percent of the volume (C1), ruled out by "
        '§5 "Sixty percent of polled customers said they want Slack, therefore build Slack." '
        "as a dead end."
    )
    sents = sentences(text)
    if len(sents) != 1:
        return f"expected exactly 1 sentence, got {len(sents)}: {sents}"
    if sents[0] != text:
        return (
            f"sentence text was altered by masking/unmasking: {sents[0]!r} != {text!r}"
        )
    return None


def _u03_band_reader() -> str | None:
    cases = {
        "**Confidence:** (chains C1 and C3) MEDIUM.": "MEDIUM",
        "**Confidence:** MEDIUM — chain C1 is HIGH confidence.": "MEDIUM",
        "**Confidence: MEDIUM**": "MEDIUM",
    }
    for line, expected in cases.items():
        got = _read_section6_band(line)
        if got != expected:
            return f"{line!r}: expected {expected!r}, got {got!r}"
    return None


def _u04_code_registry_complete() -> str | None:
    observed: set[str] = set()
    for _cid, _fixture, _src, _build, expected in _MUTATIONS:
        observed |= set(expected)
    for _cid, _build, expected in _GUIDE_MUTATIONS:
        observed |= set(expected)

    roster = _load_roster_from_contract()
    persona_text = (FIXTURE_DIR / FIXTURES[0][0]).read_text()
    bad_analysis = "# 1. Problem Essence\nNothing material here.\n"
    codes = {f.code for f in check_view(persona_text, bad_analysis, "x.md", roster)}
    if codes != {"PV-SOURCE"}:
        return f"PV-SOURCE control: expected {{'PV-SOURCE'}} on an unsliceable analysis, got {sorted(codes)}"
    observed |= codes

    unknown = observed - set(FINDING_CODES)
    if unknown:
        return f"observed codes outside FINDING_CODES: {sorted(unknown)}"
    missing = set(FINDING_CODES) - observed
    if missing:
        return f"codes never observed by any control: {sorted(missing)}"
    return None


# D-05 (Phase 87): the behavior block's positive and negative inline
# sentences, run through check_voice directly -- no private text appears in
# this checker; these are constructed strings only.
_U05_POSITIVE_SENTENCES: tuple[str, ...] = tuple(
    f"{w} the remaining work under the procedure (C1)."
    for w in (
        "Build",
        "Classify",
        "Confirm",
        "Consider",
        "Decide",
        "Finish",
        "Keep",
        "Move",
        "Read",
        "Reject",
        "Risk-classify",
        "Switch",
        "Take",
        "Treat",
    )
) + (
    "Do not change the method now (C1).",
    "Your objection is right about the timing and wrong about the method (C1).",
    "The reader's objection is wrong (C1).",
)

_U05_NEGATIVE_SENTENCES: tuple[str, ...] = (
    "Which assurance method fits the unexecuted remainder (§1).",
    "CSV and CSA serve one unchanged obligation (C1).",
    "All three rate HIGH (C8).",
    "MEDIUM overall, because three facts are not yet established (§6, GT-9?).",
    "In the Answer block and §6, together with the three conditions it depends on (§6).",
    "Confidence is MEDIUM because the estimates are top-down (§6).",
    "Raising to HIGH needs bottom-up costs (§6).",
    "Would change it: a win/loss audit (C3).",
    "Risk retired by the analysis is the cost question (C1).",
    "Reading at source confirmed it (GT-1).",
)


def _u06_title_normalisation() -> str | None:
    h1 = source_h1("# **Worked  Example:** `X`\n\nbody\n")
    if h1 is None or normalise_title(h1) != normalise_title("Worked Example: X"):
        return f"emphasis/whitespace normalisation failed: {h1!r}"
    if normalise_title("Case_Id") == normalise_title("case_id"):
        return "normaliser folded case or underscores"
    fenced = "```\n# not a title\n```\n\n# Real Title\n"
    if source_h1(fenced) != "Real Title":
        return f"H1 inside a code fence was not ignored: {source_h1(fenced)!r}"
    if source_h1("```\n# only in fence\n```\n## sub\n") is not None:
        return "fence-only H1 was returned"
    roster = _load_roster_from_contract()
    name, src = FIXTURES[0]
    persona = (FIXTURE_DIR / name).read_text()
    nosrc = "\n".join(
        ln
        for ln in (REPO_ROOT / src).read_text().split("\n")
        if not ln.startswith("# ")
    )
    found = check_view(persona, nosrc, name, roster)
    if not any(f.code == "PV-HEADER" and "no H1" in f.detail for f in found):
        return f"missing source H1 did not yield a PV-HEADER naming it: {found!r}"
    return None


def _u05_directive_lexicon() -> str | None:
    facts = SourceFacts(frozenset(), {}, 0, frozenset(), "MEDIUM", frozenset(), "")
    for text in _U05_POSITIVE_SENTENCES:
        codes = {f.code for f in check_voice([text], facts)}
        if codes != {"PV-DIRECTIVE"}:
            return f"expected {{'PV-DIRECTIVE'}} for {text!r}, got {sorted(codes)}"
    for text in _U05_NEGATIVE_SENTENCES:
        codes = {f.code for f in check_voice([text], facts)}
        if codes:
            return f"expected no findings for {text!r}, got {sorted(codes)}"
    return None


# D-05 (Phase 87): the pre-87 shipped decision-owner example, frozen before
# re-derivation, kept as a must-fail fixture. Never added to FIXTURES: P01
# requires zero findings on every FIXTURES member, and this file is a
# must-fail by design.
PRE87_FIXTURE = FIXTURE_DIR / "pre87-product-business-2-decision-owner.md"


def _d_pre87_directive() -> str | None:
    """D-PRE87: the frozen pre-87 example fails for PV-DIRECTIVE alone among
    content-voice rules -- it opens "Decide to build the reporting
    rewrite..." and restates §6's own Recommended approach paragraph almost
    verbatim. PV-HEADER also fires on the full check_view reading: the file
    predates the memo header (its line 1 reads "... view — ...", not "...
    memo — ..."), so line 1 fails to resolve a role and the memo block
    (lines 3-6) is absent too -- both structural, not voice failures. Since
    the role never resolves, the old bullet body is never run through the
    structural question check at all, so PV-QUESTIONS does not fire here
    under the memo contract (re-measured at Phase 87 D-11; the pre-memo
    contract's pinned set was {PV-DIRECTIVE, PV-QUESTIONS}). Pins the exact
    two-code set so any new failure mode on this artifact is caught."""
    persona_text = PRE87_FIXTURE.read_text()
    source_path = REPO_ROOT / "shared" / "examples" / "product-business-2.md"
    analysis_text = source_path.read_text()
    roster = _load_roster_from_contract()
    analysis_name = _provenance_name(persona_text)
    if analysis_name is None:
        return (
            "could not parse the pre-87 fixture's provenance analysis name from line 3"
        )

    facts = source_facts(analysis_text)
    header = split_header(persona_text, analysis_name, roster)
    units = body_units(header.body)
    valid_units = [u for u in units if u.kind != "violation"]
    voice_findings = check_voice([u.text for u in valid_units], facts)
    voice_codes = {f.code for f in voice_findings}
    if voice_codes != {"PV-DIRECTIVE"}:
        return f"expected check_voice alone to yield only PV-DIRECTIVE, got {voice_findings}"
    if not any("denylisted imperative" in f.detail for f in voice_findings):
        return f"expected at least one opener finding, got {voice_findings}"
    if not any("consecutive words" in f.detail for f in voice_findings):
        return f"expected at least one verbatim-run finding, got {voice_findings}"

    full_codes = {
        f.code for f in check_view(persona_text, analysis_text, analysis_name, roster)
    }
    if full_codes != {"PV-DIRECTIVE", "PV-HEADER"}:
        return f"expected exactly {{'PV-DIRECTIVE', 'PV-HEADER'}} from check_view, got {sorted(full_codes)}"
    return None


# ---------------------------------------------------------------------------
# EX-REACH -- D-02 gate reach over every shipped persona example (Phase 86-03)
# ---------------------------------------------------------------------------

PERSONA_EXAMPLES_DIR = REPO_ROOT / "shared" / "persona-examples"
SYNC_SCRIPT = REPO_ROOT / "scripts" / "sync-content.py"

_PROVENANCE_NAME_RE = re.compile(
    r"^\*Derived from §6 and the structured summary of (?P<name>.+?); "
    r"the six sections remain the source of truth\.\*\s*$"
)
_EX_REACH_CITED_ID_RE = re.compile(r"\bC(\d+)\b|\bGT-(\d+)\b")


def _read_persona_examples_tuple() -> tuple[str, ...]:
    """ast-parse PERSONA_EXAMPLES out of scripts/sync-content.py -- never
    import that module directly, since it requires PyYAML and this script
    carries no such dependency."""
    tree = ast.parse(SYNC_SCRIPT.read_text(), filename=str(SYNC_SCRIPT))
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "PERSONA_EXAMPLES" for t in node.targets
        ):
            return tuple(ast.literal_eval(node.value))
    raise ValueError("PERSONA_EXAMPLES tuple not found in scripts/sync-content.py")


def _provenance_name(persona_text: str) -> str | None:
    """The {name} a persona's own provenance sentence cites. Parsed, never
    assumed to equal its shared/examples/ source's filename: the shipped
    examples cite an analysis-<UTC>.md name instead, since each was a real
    /first-principles:persona run against a worked example rendered as an
    analysis file (86-02-SUMMARY.md).

    Scans the header's first ten lines rather than a fixed index (D-11,
    Phase 87): the pre-87 bullet format carries the provenance sentence on
    line 3 (index 2, right after the title), while the memo format moves it
    to line 8 (index 7, after the four-line To/Re/Basis/Band block) -- the
    same provenance-line search `split_header` already performs for the
    memo header, so this helper is not a second, drifting assumption about
    where the line sits."""
    lines = persona_text.split("\n")
    for line in lines[:10]:
        m = _PROVENANCE_NAME_RE.match(line.strip())
        if m:
            return m.group("name")
    return None


def _ex_reach_split_role(
    stem: str, roster: dict[str, tuple[str, int, int]]
) -> tuple[str, str] | None:
    """Split stem into (example, role) by matching the LONGEST role suffix
    in roster -- guards a stem like "estimate-fermi-decision-owner" against
    mis-splitting on a shorter role slug that also happens to be a suffix."""
    best: tuple[str, str] | None = None
    for role in roster:
        suffix = "-" + role
        if stem.endswith(suffix) and (best is None or len(role) > len(best[1])):
            best = (stem[: -len(suffix)], role)
    return best


def _ex_reach(
    persona_dir: Path = PERSONA_EXAMPLES_DIR,
    roster_stems: tuple[str, ...] | None = None,
) -> str | None:
    """D-02: PERSONA-GATE's reach over every shipped persona example.

    (a) population = sorted persona_dir/*.md; an empty population is a
        FAILURE, never a vacuous pass (T-86-10).
    (b) roster_stems (PERSONA_EXAMPLES, ast-parsed by default) and the disk
        population must be set-equal; a mismatch names whichever side is
        short.
    (c) each stem splits into <example>-<role> against the contract's role
        roster; shared/examples/<example>.md must exist.
    (d) each persona checked against its real source (not the analysis-<UTC>
        name its own provenance line cites) via check_view -- the checker's
        own entry point -- must yield zero findings.
    """
    files = sorted(persona_dir.glob("*.md"))
    if not files:
        return f"no persona example files found under {_relpath(persona_dir)}"
    population = tuple(p.stem for p in files)

    if roster_stems is None:
        roster_stems = _read_persona_examples_tuple()
    pop_set, roster_set = set(population), set(roster_stems)
    if pop_set != roster_set:
        return (
            "PERSONA_EXAMPLES roster and the shared/persona-examples/ "
            f"population disagree: on disk only={sorted(pop_set - roster_set)}, "
            f"in roster only={sorted(roster_set - pop_set)}"
        )

    roster = _load_roster_from_contract()
    for stem in population:
        split = _ex_reach_split_role(stem, roster)
        if split is None:
            return f"{stem}: no role suffix in {sorted(roster)} matches"
        example, _role = split
        source_path = REPO_ROOT / "shared" / "examples" / f"{example}.md"
        if not source_path.exists():
            return f"{stem}: source shared/examples/{example}.md does not exist"
        persona_text = (persona_dir / f"{stem}.md").read_text()
        analysis_name = _provenance_name(persona_text)
        if analysis_name is None:
            return f"{stem}: could not parse the provenance analysis name from line 3"
        findings = check_view(
            persona_text, source_path.read_text(), analysis_name, roster
        )
        if findings:
            return f"{stem}: expected zero findings against {source_path.name}, got {findings}"
    return None


def _ex_reach_empty() -> str | None:
    """EX-REACH-EMPTY: an empty population must be reported as a failure,
    never pass vacuously (T-86-10)."""
    with tempfile.TemporaryDirectory() as tmp:
        result = _ex_reach(persona_dir=Path(tmp))
    if result is None:
        return "an empty persona_dir unexpectedly reported success"
    return None


def _ex_reach_roster_mismatch() -> str | None:
    """EX-REACH-ROSTER: a roster carrying one name absent from disk must be
    named in the failure, not silently ignored."""
    real = _read_persona_examples_tuple()
    extra = "nonexistent-example-skeptic"
    result = _ex_reach(roster_stems=real + (extra,))
    if result is None or extra not in result:
        return f"expected a failure naming {extra!r}, got {result!r}"
    return None


def _ex_reach_id_mutation() -> str | None:
    """EX-REACH-ID: replacing one cited C<n>/GT-<n> token in the first
    shipped example with an id one above the source's own highest of that
    kind must produce PV-ID -- proving the reach is real, not a presence
    check."""
    roster = _load_roster_from_contract()
    stem = min(p.stem for p in PERSONA_EXAMPLES_DIR.glob("*.md"))
    split = _ex_reach_split_role(stem, roster)
    if split is None:
        return f"{stem}: no role suffix in {sorted(roster)} matches"
    example, _role = split
    source_path = REPO_ROOT / "shared" / "examples" / f"{example}.md"
    source_text = source_path.read_text()
    facts = source_facts(source_text)
    persona_text = (PERSONA_EXAMPLES_DIR / f"{stem}.md").read_text()
    analysis_name = _provenance_name(persona_text)
    if analysis_name is None:
        return f"{stem}: could not parse the provenance analysis name from line 3"

    m = _EX_REACH_CITED_ID_RE.search(persona_text)
    if not m:
        return f"{stem}: no cited C<n>/GT-<n> token found to mutate"
    if m.group(1) is not None:
        highest = max((int(c[1:]) for c in facts.chain_ids), default=0)
        bad_token = f"C{highest + 1}"
    else:
        highest = max((int(g[3:]) for g in facts.gt_declared), default=0)
        bad_token = f"GT-{highest + 1}"
    mutated = persona_text[: m.start()] + bad_token + persona_text[m.end() :]
    if mutated == persona_text:
        return "mutation was a no-op"

    findings = check_view(mutated, source_text, analysis_name, roster)
    codes = {f.code for f in findings}
    if "PV-ID" not in codes:
        return f"{stem}: expected PV-ID among findings for {bad_token!r}, got {sorted(codes)}"
    return None


_CONTROLS: tuple[tuple[str, Callable[[], str | None]], ...] = (
    (
        ("P01", _p01_fixtures_clean),
        ("P02", _p02_contract_parity),
        ("P03", _p03_guide_passes),
        ("P04", _p04_questions_parity),
        ("P05", _p05_denylist_parity),
    )
    + tuple(
        (cid, _make_mutation_control(fixture, src, build, expected))
        for cid, fixture, src, build, expected in _MUTATIONS
    )
    + tuple(
        (cid, _make_guide_control(build, expected))
        for cid, build, expected in _GUIDE_MUTATIONS
    )
    + (
        ("U01", _u01_numbers),
        ("U02", _u02_sentence_boundaries),
        ("U03", _u03_band_reader),
        ("U04", _u04_code_registry_complete),
        ("U05", _u05_directive_lexicon),
        ("U06-title-normalisation", _u06_title_normalisation),
        ("D-PRE87", _d_pre87_directive),
        ("EX-REACH", _ex_reach),
        ("EX-REACH-ID", _ex_reach_id_mutation),
        ("EX-REACH-EMPTY", _ex_reach_empty),
        ("EX-REACH-ROSTER", _ex_reach_roster_mismatch),
    )
)


def self_test() -> int:
    failures: list[str] = []
    for cid, fn in _CONTROLS:
        try:
            msg = fn()
        except Exception as exc:  # noqa: BLE001
            msg = f"{type(exc).__name__}: {exc}"
        if msg:
            print(f"[FAIL] {cid}: {msg}")
            failures.append(cid)
        else:
            print(f"[PASS] {cid}")
    if failures:
        print(
            f"PERSONA-GATE: FAIL ({len(failures)}/{len(_CONTROLS)} failed: {failures})"
        )
        return 1
    print(f"PERSONA-GATE: PASS ({len(_CONTROLS)}/{len(_CONTROLS)} controls)")
    return 0


# ---------------------------------------------------------------------------
# --describe
# ---------------------------------------------------------------------------


def describe() -> dict:
    """Pure self-description. Every value is derived from this module's own data."""
    roster = _load_roster_from_contract()
    persona_example_files = sorted(PERSONA_EXAMPLES_DIR.glob("*.md"))
    persona_example_sources: set[str] = set()
    for p in persona_example_files:
        split = _ex_reach_split_role(p.stem, roster)
        if split is not None:
            persona_example_sources.add(
                _relpath(REPO_ROOT / "shared" / "examples" / f"{split[0]}.md")
            )
    checked_files = sorted(
        {_relpath(FIXTURE_DIR / name) for name, _src in FIXTURES}
        | {src for _name, src in FIXTURES}
        | {_relpath(p) for p in persona_example_files}
        | persona_example_sources
        | {_relpath(PRE87_FIXTURE)}
    )
    return {
        "control_ids": [cid for cid, _fn in _CONTROLS],
        "control_count": len(_CONTROLS),
        "registered_surfaces": sorted(
            [_relpath(CONTRACT), _relpath(GUIDE), _relpath(TEMPLATE)]
        ),
        "checked_files": checked_files,
        "locked_constants": {
            "roster": {
                slug: [title, lo, hi] for slug, (title, lo, hi) in LOCKED_ROSTER.items()
            },
            "questions": {slug: list(qs) for slug, qs in LOCKED_QUESTIONS.items()},
            "guide_max_words": GUIDE_MAX_WORDS,
            "provenance_template": PROVENANCE_TEMPLATE,
            "directive_openers": sorted(DIRECTIVE_OPENERS),
            "directive_phrase_openers": [list(p) for p in DIRECTIVE_PHRASE_OPENERS],
            "verbatim_run_words": VERBATIM_RUN_WORDS,
            "memo_fields": list(MEMO_FIELDS),
            "in_brief_prefix": IN_BRIEF_PREFIX,
        },
        "derived_counts": {
            "finding_codes": len(FINDING_CODES),
            "fixtures": len(FIXTURES),
            "personas": len(LOCKED_ROSTER),
            "persona_examples": len(persona_example_files),
        },
        "disclosed_bounds_anchors": sorted(
            [
                "citation-presence-not-semantic-support",
                "numbers-matched-by-value-not-by-context",
                "absent-input-sentences-not-checked-for-truth",
                "guide-names-checked-against-output-template-only",
                "fixtures-are-worked-examples-not-live-analyses",
                "directive-check-is-lexical-not-semantic",
                "imperative-check-is-sentence-initial-only",
                "verbatim-run-checked-against-section6-recommended-approach-only",
                "memo-structure-counts-paragraphs-not-answers",
                "title-compared-after-emphasis-and-whitespace-normalisation",
            ]
        ),
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("persona", nargs="?", help="path to the persona-view Markdown file")
    ap.add_argument(
        "analysis", nargs="?", help="path to the source analysis Markdown file"
    )
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--describe", action="store_true")
    args = ap.parse_args(argv)

    if args.describe:
        print(json.dumps(describe(), indent=2, sort_keys=True))
        return 0

    if args.self_test:
        return self_test()

    if not args.persona or not args.analysis:
        ap.print_help()
        return 2

    persona_path = Path(args.persona)
    analysis_path = Path(args.analysis)
    try:
        persona_text = persona_path.read_text()
    except OSError as exc:
        print(f"usage error: cannot read {args.persona}: {exc}")
        return 2
    try:
        analysis_text = analysis_path.read_text()
    except OSError as exc:
        print(f"usage error: cannot read {args.analysis}: {exc}")
        return 2

    roster = _load_roster_from_contract()
    findings = check_view(persona_text, analysis_text, analysis_path.name, roster)
    for f in findings:
        print(f"{f.code}: {f.detail}")
    if findings:
        print(f"PERSONA-GATE: FAIL ({len(findings)} findings)")
        return 1
    print("PERSONA-GATE: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
