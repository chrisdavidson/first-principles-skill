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
every body sentence and bullet carries a citation token, that every cited chain id,
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
import importlib.util
import json
import re
import sys
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
# (P02) compares the shipped contract's roster table against.
LOCKED_ROSTER: dict[str, tuple[str, int, int]] = {
    "decision-owner": ("Decision Owner", 80, 120),
    "operator": ("Operator", 100, 150),
    "risk": ("Risk", 100, 150),
    "skeptic": ("Skeptic", 80, 120),
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
_QUOTED_DEADEND_RE = re.compile(r'§5\s+"[^"]*"')
_DECIMAL_RE = re.compile(r"(?<=\d)\.(?=\d)")
_UNMASK = {"\x00": ".", "\x01": "?", "\x02": "!"}
_TERMINATOR_SPLIT_RE = re.compile(r"(?<=[.?!])(?:\s+|$)")


def _mask_sentence_breaks(text: str) -> str:
    chars = list(text)
    for pat in (_GT_Q_RE, _QUOTED_DEADEND_RE):
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

_CITATION_PRESENT_RE = re.compile(r"C\d+\b|GT-\d+\??|A-\d+\b|§[1-6]\b")
_RESOLVE_GT_RE = re.compile(r"GT-(\d+)(\??)")
_RESOLVE_CHAIN_RE = re.compile(r"\bC(\d+)\b")
_RESOLVE_A_RE = re.compile(r"\bA-(\d+)\b")


def resolve_ids(body_text: str, facts: SourceFacts) -> list[Finding]:
    findings: list[Finding] = []

    for m in _QUOTED_DEADEND_RE.finditer(body_text):
        title = m.group(0)[len('§5 "'):-1]
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
# check_view
# ---------------------------------------------------------------------------

def check_view(
    persona_text: str, analysis_text: str, analysis_name: str, roster: dict[str, tuple[str, int, int]],
) -> list[Finding]:
    try:
        facts = source_facts(analysis_text)
    except SourceError as exc:
        return [Finding("PV-SOURCE", str(exc))]

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

    for u in valid_units:
        for s in sentences(u.text):
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
    extra = "\n- The engineering team has 3.2 engineer-quarters of capacity this quarter (C1)."
    return text + extra * 6


def _m_cut_under(text: str) -> str:
    lines = text.split("\n")
    band_idx = next(i for i, l in enumerate(lines) if l.startswith("**Band"))
    head = lines[: band_idx + 1]
    short_body = ["", "- The reporting rewrite has a verified expansion case (C1)."]
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


_MUTATIONS: tuple[tuple[str, str, str, Callable[[str], str], frozenset[str]], ...] = (
    ("M-ID", "product-business-2-decision-owner.md", "shared/examples/product-business-2.md",
     lambda t: t.replace("GT-5?", "GT-6"), frozenset({"PV-ID"})),
    ("M-AGREE", "product-business-2-decision-owner.md", "shared/examples/product-business-2.md",
     lambda t: t.replace("GT-5?", "GT-5"), frozenset({"PV-ID"})),
    ("M-NUMBER", "product-business-2-decision-owner.md", "shared/examples/product-business-2.md",
     lambda t: t.replace("$180,000", "$190,000"), frozenset({"PV-NUMBER"})),
    ("M-UNCITED", "product-business-2-decision-owner.md", "shared/examples/product-business-2.md",
     _m_uncited, frozenset({"PV-UNCITED"})),
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


_CONTROLS: tuple[tuple[str, Callable[[], str | None]], ...] = (
    ("P01", _p01_fixtures_clean),
    ("P02", _p02_contract_parity),
    ("P03", _p03_guide_passes),
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
    checked_files = sorted(
        {_relpath(FIXTURE_DIR / name) for name, _src in FIXTURES} | {src for _name, src in FIXTURES}
    )
    return {
        "control_ids": [cid for cid, _fn in _CONTROLS],
        "control_count": len(_CONTROLS),
        "registered_surfaces": sorted([_relpath(CONTRACT), _relpath(GUIDE), _relpath(TEMPLATE)]),
        "checked_files": checked_files,
        "locked_constants": {
            "roster": {slug: [title, lo, hi] for slug, (title, lo, hi) in LOCKED_ROSTER.items()},
            "guide_max_words": GUIDE_MAX_WORDS,
            "provenance_template": PROVENANCE_TEMPLATE,
        },
        "derived_counts": {
            "finding_codes": len(FINDING_CODES),
            "fixtures": len(FIXTURES),
            "personas": len(LOCKED_ROSTER),
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
