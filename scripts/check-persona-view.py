#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""PERSONA-GATE: checker and self-test for a persona view against its source analysis.

Proves that a persona view (a role-scoped overlay of one delivered first-principles
analysis — decision-owner, operator, risk, skeptic) adds no claim its source analysis
does not already carry. Checks, mechanically: the file-format header (title line,
provenance sentence, Band line), the body's word count against the role's band, that
every role's fixed question list appears verbatim and in order as each bullet's bold
lead-in (PV-QUESTIONS) with a dropped, reordered or invented question each failing
alone, that every body sentence and bullet carries a citation token (the question's
own text is exempt, the answer after it is not), that every cited chain id,
ground-truth id (including its `?` marking), assumption id and quoted dead-end title
resolves against the source analysis, that every number in the body appears as a
number in the source, and that the Band line agrees with the source's own §6
confidence band. It also checks the companion business-reading guide names only
sections and fields that exist in the output template, and that the guide stays
inside its word ceiling.

What this does NOT prove: that a cited id actually supports the sentence it is
attached to. Resolving `(chain C1)` only shows the analysis declares a C1 — it does
not show C1's content backs the claim beside it. That is a semantic-support question,
deliberately out of scope here (see `citation-presence-not-semantic-support` in
`--describe`).

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

# D-04: the independent transcription this module's own contract-parity control
# (P02) compares the shipped contract's roster table against. Band = each role's
# fixed question words (33/30/20/26, counted by this module's own counting rule)
# plus 60-140 words of answer; the D-01 approved sample (144 words) sits inside
# the decision-owner band.
LOCKED_ROSTER: dict[str, tuple[str, int, int]] = {
    "decision-owner": ("Decision Owner", 93, 173),
    "operator": ("Operator", 90, 170),
    "risk": ("Risk", 80, 160),
    "skeptic": ("Skeptic", 86, 166),
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
)


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
            "_sb_for_persona_view", REPO_ROOT / "scripts" / "check-summary-block.py")
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

_ROSTER_SECTION_RE = re.compile(r"^## Persona roster\n(.*?)(?=^## |\Z)", re.MULTILINE | re.DOTALL)
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


_ROLE_SECTION_RE = re.compile(r"^## (?P<title>[A-Za-z ]+)\n(?P<body>.*?)(?=^## |\Z)", re.MULTILINE | re.DOTALL)
_QUESTIONS_BLOCK_RE = re.compile(r"\*\*Questions \(in order\):\*\*\n\n(?P<list>(?:\d+\.\s+.+\n)+)")
_QUESTION_LINE_RE = re.compile(r"^\d+\.\s+(?P<q>.+?)\s*$", re.MULTILINE)


def load_questions(
    contract_text: str, roster: dict[str, tuple[str, int, int]],
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
        raise SourceError(f"analysis text does not resolve into sections 1-6: {exc}") from exc
    chain_ids = frozenset(sbmod._doc_chain_index(sections.get(4, ""))[0])
    gt_declared = dict(sbmod._gt_declarations(sections.get(3, "")))
    assumption_row_count = len(sbmod._table_columns(sections.get(2, ""), ("Assumption",)))
    dead_end_titles = frozenset(
        re.sub(r"\s+", " ", m.group("name")).strip()
        for m in sbmod._DEAD_END_HEADING_RE.finditer(sections.get(5, ""))
    )
    band = _read_section6_band(sections.get(6, ""))
    if band is None:
        raise SourceError("no readable **Confidence:** band in section 6")
    numbers = frozenset(numbers_in(analysis_text))
    return SourceFacts(chain_ids, gt_declared, assumption_row_count, dead_end_titles, band, numbers)


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

_TITLE_LINE_RE = re.compile(r"^# (?P<title>.+?) view — (?P<atitle>\S.*)$")
_BAND_LINE_RE = re.compile(r"^\*\*Band \(from §6\):\*\* (?P<band>HIGH|MEDIUM|LOW)\s*$")


@dataclass
class HeaderResult:
    role: str | None
    band: str | None
    body: str
    findings: list[Finding] = field(default_factory=list)


def split_header(persona_text: str, analysis_name: str, roster: dict[str, tuple[str, int, int]]) -> HeaderResult:
    findings: list[Finding] = []
    lines = persona_text.split("\n")
    title_to_slug = {title: slug for slug, (title, _lo, _hi) in roster.items()}

    role: str | None = None
    if lines:
        m = _TITLE_LINE_RE.match(lines[0])
        if m and m.group("title") in title_to_slug:
            role = title_to_slug[m.group("title")]
        else:
            findings.append(Finding("PV-HEADER", f"line 1 does not match a roster title: {lines[0]!r}"))
    else:
        findings.append(Finding("PV-HEADER", "persona file is empty"))

    expected_provenance = "*" + PROVENANCE_TEMPLATE.format(name=analysis_name) + "*"
    if len(lines) >= 3:
        if lines[2].strip() != expected_provenance:
            findings.append(Finding(
                "PV-HEADER", f"line 3 does not match the provenance sentence: {lines[2]!r}"))
    else:
        findings.append(Finding("PV-HEADER", "persona file has fewer than 3 lines; missing provenance line"))

    band: str | None = None
    band_idx: int | None = None
    for i, line in enumerate(lines[:7]):
        m = _BAND_LINE_RE.match(line.strip())
        if m:
            band = m.group("band")
            band_idx = i
            break
    if band is None:
        findings.append(Finding("PV-HEADER", "no **Band (from §6):** line found in the first seven lines"))
        body_lines = lines[3:] if len(lines) > 3 else []
    else:
        body_lines = lines[band_idx + 1:]
    while body_lines and body_lines[0].strip() == "":
        body_lines.pop(0)
    body = "\n".join(body_lines)
    return HeaderResult(role=role, band=band, body=body, findings=findings)


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
        if (_HEADING_RE.match(raw_line) or _TABLE_ROW_RE.match(raw_line)
                or _CODE_FENCE_RE.match(raw_line) or _NUMBERED_RE.match(raw_line)):
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
            findings.append(Finding("PV-DEADEND", f'quoted §5 title not found in §5: "{title}"'))

    masked = _QUOTED_DEADEND_RE.sub(lambda m: "§Q" + " " * (len(m.group(0)) - 2), body_text)

    for m in _RESOLVE_GT_RE.finditer(masked):
        gid = f"GT-{m.group(1)}"
        has_q = m.group(2) == "?"
        if gid not in facts.gt_declared:
            findings.append(Finding("PV-ID", f"{gid}{'?' if has_q else ''} not declared in §3"))
            continue
        expected_q = not facts.gt_declared[gid]
        if has_q != expected_q:
            findings.append(Finding(
                "PV-ID",
                f"{gid}{'?' if has_q else ''} marking disagrees with §3's declaration"))

    for m in _RESOLVE_CHAIN_RE.finditer(masked):
        cid = f"C{m.group(1)}"
        if cid not in facts.chain_ids:
            findings.append(Finding("PV-ID", f"{cid} not declared in §4"))

    for m in _RESOLVE_A_RE.finditer(masked):
        n = int(m.group(1))
        if not (1 <= n <= facts.assumption_row_count):
            findings.append(Finding(
                "PV-ID",
                f"A-{n} outside the Assumptions Table's row range (1..{facts.assumption_row_count})"))

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
        findings.append(Finding(
            "PV-GUIDE-WORDS", f"guide body is {word_count} words, exceeds {GUIDE_MAX_WORDS}"))
    g = _normalize_ws(guide_text)
    t = _normalize_ws(template_text)
    names = _GUIDE_BACKTICK_RE.findall(g) + _GUIDE_QUOTE_RE.findall(g)
    for name in names:
        if name not in t:
            findings.append(Finding(
                "PV-GUIDE-NAME", f"name not found verbatim in output-template.md: {name!r}"))
    return findings


# ---------------------------------------------------------------------------
# Questions (Phase 87 D-05): each role answers its fixed, ordered question
# list; the question text itself is exempt from the citation rule (like an
# absent-input sentence) but the answer following it is not.
# ---------------------------------------------------------------------------

_LEAD_IN_RE = re.compile(r"^\*\*(?P<q>[^*]+?)\*\*\s*(?P<answer>.*)$")


def check_questions(
    units: list[BodyUnit], expected: tuple[str, ...],
) -> tuple[list[Finding], list[str]]:
    """Walk valid body units against a role's fixed `expected` question list.

    Returns (findings, citation_texts): citation_texts is what the PV-UNCITED
    sentence loop checks instead of raw unit text -- a matched question's
    citation text is its answer only (the question itself is exempt); an
    invented/reworded question, a bare paragraph or a lead-in-less bullet is
    NOT exempt and contributes its full unit text instead.
    """
    findings: list[Finding] = []
    citations: list[str] = []
    seen: list[str] = []
    seen_set: set[str] = set()

    for u in units:
        if u.kind == "paragraph":
            findings.append(Finding(
                "PV-QUESTIONS", f"content outside a question bullet: {u.text!r}"))
            citations.append(u.text)
            continue
        m = _LEAD_IN_RE.match(u.text)
        if not m:
            findings.append(Finding(
                "PV-QUESTIONS", f"bullet has no bold question lead-in: {u.text!r}"))
            citations.append(u.text)
            continue
        q = m.group("q").strip()
        if q not in expected:
            findings.append(Finding(
                "PV-QUESTIONS", f"invented or reworded question: {q!r}"))
            citations.append(u.text)
            continue
        if q in seen_set:
            findings.append(Finding("PV-QUESTIONS", f"question repeated: {q!r}"))
        else:
            seen_set.add(q)
            seen.append(q)
        answer = m.group("answer").strip()
        if not answer:
            findings.append(Finding("PV-QUESTIONS", f"question has no answer: {q!r}"))
        citations.append(answer)

    for q in expected:
        if q not in seen_set:
            findings.append(Finding("PV-QUESTIONS", f"missing question: {q!r}"))

    expected_seen = [q for q in expected if q in seen_set]
    if seen != expected_seen:
        findings.append(Finding(
            "PV-QUESTIONS", f"questions out of order: {seen} != {expected_seen}"))

    return findings, citations


# ---------------------------------------------------------------------------
# check_view
# ---------------------------------------------------------------------------

def check_view(
    persona_text: str, analysis_text: str, analysis_name: str, roster: dict[str, tuple[str, int, int]],
    *, questions: dict[str, tuple[str, ...]] | None = None,
) -> list[Finding]:
    try:
        facts = source_facts(analysis_text)
    except SourceError as exc:
        return [Finding("PV-SOURCE", str(exc))]

    if questions is None:
        questions = load_questions(CONTRACT.read_text(), roster)

    header = split_header(persona_text, analysis_name, roster)
    findings: list[Finding] = list(header.findings)

    units = body_units(header.body)
    for u in units:
        if u.kind == "violation":
            findings.append(Finding("PV-SHAPE", f"non-paragraph/bullet content in body: {u.text!r}"))
    valid_units = [u for u in units if u.kind != "violation"]
    combined_text = "\n".join(u.text for u in valid_units)

    if header.role is not None:
        _title, lo, hi = roster[header.role]
        word_count = sum(len(u.text.split()) for u in valid_units)
        if not (lo <= word_count <= hi):
            findings.append(Finding(
                "PV-WORDS",
                f"body is {word_count} words, outside the {header.role} band [{lo}, {hi}]"))

    if header.role is not None:
        q_findings, citation_texts = check_questions(valid_units, questions.get(header.role, ()))
        findings.extend(q_findings)
    else:
        citation_texts = [u.text for u in valid_units]

    for text in citation_texts:
        for s in sentences(text):
            if s.strip() and not _CITATION_PRESENT_RE.search(s):
                findings.append(Finding("PV-UNCITED", f"no citation token: {s.strip()!r}"))

    findings.extend(resolve_ids(combined_text, facts))

    body_numbers = numbers_in(combined_text)
    missing_numbers = body_numbers - facts.numbers
    if missing_numbers:
        findings.append(Finding(
            "PV-NUMBER", f"number(s) not present in the source analysis: {sorted(missing_numbers)}"))

    if header.band is not None and header.band != facts.band:
        findings.append(Finding(
            "PV-BAND", f"Band line {header.band} disagrees with the source's §6 band {facts.band}"))

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
        return f"questions {questions} does not equal LOCKED_QUESTIONS {LOCKED_QUESTIONS}"
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
    lines = text.split("\n")
    if len(lines) > 2:
        del lines[2]
    return "\n".join(lines)


def _m_pad_over(text: str) -> str:
    # Padding strong enough to clear the widest roster band's ceiling (173,
    # decision-owner, Phase 87 D-05) with margin, not just the pre-87 one
    # (120). Appended inside the last bullet's own answer (never as new
    # bullets) so the strict one-bullet-per-question shape survives the
    # mutation and only PV-WORDS fires, not PV-QUESTIONS (Phase 87 Task 2).
    padding = " The engineering team has 3.2 engineer-quarters of capacity this quarter (C1)."
    return text.rstrip("\n") + padding * 10 + "\n"


def _m_cut_under(text: str) -> str:
    # Four bullets, each a valid question lead-in with a minimal cited
    # answer -- 45 words total (33 fixed question words + 4 x 3 answer
    # words), below the decision-owner band's 93 floor, so this mutation
    # trips PV-WORDS alone, never PV-QUESTIONS (Phase 87 Task 2).
    lines = text.split("\n")
    band_idx = next(i for i, l in enumerate(lines) if l.startswith("**Band"))
    head = lines[: band_idx + 1]
    qs = load_questions(CONTRACT.read_text(), _load_roster_from_contract())["decision-owner"]
    short_body = [""] + [f"- **{q}** Stated in §6." for q in qs]
    return "\n".join(head + short_body)


def _m_insert_shape(text: str) -> str:
    lines = text.split("\n")
    band_idx = next(i for i, l in enumerate(lines) if l.startswith("**Band"))
    lines.insert(band_idx + 2, "## Extra")
    return "\n".join(lines)


def _m_deadend(text: str) -> str:
    original = '§5 "Sixty percent of polled customers said they want Slack, therefore build Slack"'
    mutated = '§5 "Fifty percent of polled customers said they want Slack, therefore build Slack"'
    return text.replace(original, mutated, 1)


def _m_q_drop(text: str) -> str:
    return text.replace("**How sure is it, and what is it unsure about?** ", "", 1)


def _m_q_order(text: str) -> str:
    lines = text.split("\n")
    bullet_idxs = [i for i, l in enumerate(lines) if l.startswith("- **")]
    i2, i3 = bullet_idxs[1], bullet_idxs[2]
    lines[i2], lines[i3] = lines[i3], lines[i2]
    return "\n".join(lines)


def _m_q_invent(text: str) -> str:
    return text.replace(
        "**Where do I find the recommendation?**", "**What else does the analysis cover?**", 1)


_MUTATIONS: tuple[tuple[str, str, str, Callable[[str], str], frozenset[str]], ...] = (
    ("M-ID", "product-business-2-decision-owner.md", "shared/examples/product-business-2.md",
     lambda t: t.replace("GT-5?", "GT-6"), frozenset({"PV-ID"})),
    ("M-AGREE", "product-business-2-decision-owner.md", "shared/examples/product-business-2.md",
     lambda t: t.replace("GT-5?", "GT-5"), frozenset({"PV-ID"})),
    ("M-NUMBER", "product-business-2-decision-owner.md", "shared/examples/product-business-2.md",
     lambda t: t.replace("$180,000", "$190,000"), frozenset({"PV-NUMBER"})),
    ("M-UNCITED", "product-business-2-decision-owner.md", "shared/examples/product-business-2.md",
     _m_uncited, frozenset({"PV-UNCITED"})),
    # 84-REVIEW CR-01: a token that merely ENDS in C<digits> (SPEC1) is not a
    # citation; the stripped sentence must still read as uncited.
    ("M-PSEUDO", "product-business-2-decision-owner.md", "shared/examples/product-business-2.md",
     lambda t: _m_uncited(t).replace(
         "the recommendation is reconsidered.", "the recommendation is reconsidered per SPEC1.", 1),
     frozenset({"PV-UNCITED"})),
    ("M-BAND", "product-business-2-decision-owner.md", "shared/examples/product-business-2.md",
     lambda t: t.replace("**Band (from §6):** MEDIUM", "**Band (from §6):** HIGH"), frozenset({"PV-BAND"})),
    ("M-HEADER", "product-business-2-decision-owner.md", "shared/examples/product-business-2.md",
     _m_remove_provenance, frozenset({"PV-HEADER"})),
    ("M-OVER", "product-business-2-decision-owner.md", "shared/examples/product-business-2.md",
     _m_pad_over, frozenset({"PV-WORDS"})),
    ("M-UNDER", "product-business-2-decision-owner.md", "shared/examples/product-business-2.md",
     _m_cut_under, frozenset({"PV-WORDS"})),
    ("M-SHAPE", "product-business-2-decision-owner.md", "shared/examples/product-business-2.md",
     _m_insert_shape, frozenset({"PV-SHAPE"})),
    ("M-DEADEND", "product-business-2-skeptic.md", "shared/examples/product-business-2.md",
     _m_deadend, frozenset({"PV-DEADEND"})),
    ("M-Q-DROP", "product-business-2-decision-owner.md", "shared/examples/product-business-2.md",
     _m_q_drop, frozenset({"PV-QUESTIONS"})),
    ("M-Q-ORDER", "product-business-2-decision-owner.md", "shared/examples/product-business-2.md",
     _m_q_order, frozenset({"PV-QUESTIONS"})),
    ("M-Q-INVENT", "product-business-2-decision-owner.md", "shared/examples/product-business-2.md",
     _m_q_invent, frozenset({"PV-QUESTIONS"})),
)


def _make_mutation_control(
    fixture_name: str, src_relpath: str, build: Callable[[str], str], expected_codes: frozenset[str],
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
            return f"expected {sorted(expected_codes)}, got {sorted(codes)} ({findings})"
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
    build: Callable[[str], str], expected_codes: frozenset[str],
) -> Callable[[], str | None]:
    def _control() -> str | None:
        guide_text = GUIDE.read_text()
        mutated = build(guide_text)
        if mutated == guide_text:
            return "mutation was a no-op"
        findings = check_guide(mutated, TEMPLATE.read_text())
        codes = {f.code for f in findings}
        if codes != expected_codes:
            return f"expected {sorted(expected_codes)}, got {sorted(codes)} ({findings})"
        return None
    return _control


def _u01_numbers() -> str | None:
    got = numbers_in('$180,000/year, 3.2, 17%, 3–5, GT-5? C1 A-3 §6')
    want = {"180000", "3.2", "17", "3", "5"}
    if got != want:
        return f"expected {want}, got {got}"
    return None


def _u02_sentence_boundaries() -> str | None:
    text = (
        'The chain cites GT-5? and 3.2 percent of the volume (C1), ruled out by '
        '§5 "Sixty percent of polled customers said they want Slack, therefore build Slack." '
        'as a dead end.'
    )
    sents = sentences(text)
    if len(sents) != 1:
        return f"expected exactly 1 sentence, got {len(sents)}: {sents}"
    if sents[0] != text:
        return f"sentence text was altered by masking/unmasking: {sents[0]!r} != {text!r}"
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
    """The {name} a persona's own line 3 cites. Parsed, never assumed to
    equal its shared/examples/ source's filename: the shipped examples cite
    an analysis-<UTC>.md name instead, since each was a real
    /first-principles:persona run against a worked example rendered as an
    analysis file (86-02-SUMMARY.md)."""
    lines = persona_text.split("\n")
    if len(lines) < 3:
        return None
    m = _PROVENANCE_NAME_RE.match(lines[2].strip())
    return m.group("name") if m else None


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
        findings = check_view(persona_text, source_path.read_text(), analysis_name, roster)
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
    stem = sorted(p.stem for p in PERSONA_EXAMPLES_DIR.glob("*.md"))[0]
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
    mutated = persona_text[: m.start()] + bad_token + persona_text[m.end():]
    if mutated == persona_text:
        return "mutation was a no-op"

    findings = check_view(mutated, source_text, analysis_name, roster)
    codes = {f.code for f in findings}
    if "PV-ID" not in codes:
        return f"{stem}: expected PV-ID among findings for {bad_token!r}, got {sorted(codes)}"
    return None


_CONTROLS: tuple[tuple[str, Callable[[], str | None]], ...] = (
    ("P01", _p01_fixtures_clean),
    ("P02", _p02_contract_parity),
    ("P03", _p03_guide_passes),
    ("P04", _p04_questions_parity),
) + tuple(
    (cid, _make_mutation_control(fixture, src, build, expected))
    for cid, fixture, src, build, expected in _MUTATIONS
) + tuple(
    (cid, _make_guide_control(build, expected))
    for cid, build, expected in _GUIDE_MUTATIONS
) + (
    ("U01", _u01_numbers),
    ("U02", _u02_sentence_boundaries),
    ("U03", _u03_band_reader),
    ("U04", _u04_code_registry_complete),
    ("EX-REACH", _ex_reach),
    ("EX-REACH-ID", _ex_reach_id_mutation),
    ("EX-REACH-EMPTY", _ex_reach_empty),
    ("EX-REACH-ROSTER", _ex_reach_roster_mismatch),
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
        print(f"PERSONA-GATE: FAIL ({len(failures)}/{len(_CONTROLS)} failed: {failures})")
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
            persona_example_sources.add(_relpath(REPO_ROOT / "shared" / "examples" / f"{split[0]}.md"))
    checked_files = sorted(
        {_relpath(FIXTURE_DIR / name) for name, _src in FIXTURES} | {src for _name, src in FIXTURES}
        | {_relpath(p) for p in persona_example_files}
        | persona_example_sources
    )
    return {
        "control_ids": [cid for cid, _fn in _CONTROLS],
        "control_count": len(_CONTROLS),
        "registered_surfaces": sorted([_relpath(CONTRACT), _relpath(GUIDE), _relpath(TEMPLATE)]),
        "checked_files": checked_files,
        "locked_constants": {
            "roster": {slug: [title, lo, hi] for slug, (title, lo, hi) in LOCKED_ROSTER.items()},
            "questions": {slug: list(qs) for slug, qs in LOCKED_QUESTIONS.items()},
            "guide_max_words": GUIDE_MAX_WORDS,
            "provenance_template": PROVENANCE_TEMPLATE,
        },
        "derived_counts": {
            "finding_codes": len(FINDING_CODES),
            "fixtures": len(FIXTURES),
            "personas": len(LOCKED_ROSTER),
            "persona_examples": len(persona_example_files),
        },
        "disclosed_bounds_anchors": sorted([
            "citation-presence-not-semantic-support",
            "numbers-matched-by-value-not-by-context",
            "absent-input-sentences-not-checked-for-truth",
            "guide-names-checked-against-output-template-only",
            "fixtures-are-worked-examples-not-live-analyses",
        ]),
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("persona", nargs="?", help="path to the persona-view Markdown file")
    ap.add_argument("analysis", nargs="?", help="path to the source analysis Markdown file")
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
