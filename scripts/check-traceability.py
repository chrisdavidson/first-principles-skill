#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""TRACE-01..TRACE-03 / GAP-01 gate: traceability matrix emitter + consistency gate.

Emits a Markdown matrix table (MATRIX.md) and a structured JSON sidecar
(matrix.json) from an internal list of MatrixRow dataclass objects, then
validates the sidecar for consistency.

Usage:
    python3 scripts/check-traceability.py --self-test
    python3 scripts/check-traceability.py emit \\
        --md-output docs/requirements-matrix.md \\
        --json-output docs/data/matrix.json
    python3 scripts/check-traceability.py check \\
        --input docs/data/matrix.json

Exit codes:
    0  all fixtures pass (--self-test) or subcommand completes cleanly
    1  fixture mismatch or consistency failure
    2  environment error (Python <3.12) or path confinement violation

--self-test: runs the inline fixtures + named sentinels (no disk I/O beyond
             checking known-present repo files) and exits 0 only if all pass.
             This is the CI gate entry point (TRACE-03 + STEP0-08 pattern).

emit: writes MATRIX.md + matrix.json from build_matrix_rows(); both paths
      must be under .planning/ or docs/ (T-82-01 path-confinement guard).

check: reads matrix.json, validates every row has a valid capability and
       coverage_tier, and deep-resolves every reproducible artifact_link (D-08).
"""

import argparse
import contextlib
import io
import json
import re
import sys
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import NamedTuple


REPO_ROOT: Path = Path(__file__).resolve().parents[1]

# Whitelist for CLI-tool artifact links that have no script file (Pitfall 6)
KNOWN_CLI_GATES: set[str] = {
    "claude plugin validate ./first-principles",
    "markdownlint-cli2",
}

# Valid values for capability and coverage_tier fields
VALID_CAPABILITIES: set[str] = {"Methodology", "Test-Network"}
VALID_TIERS: set[str] = {"reproducible", "audit-only", "gap", "scheduled"}

# Surfaces where the published coverage headline is asserted as a present-tense claim by
# _self_test_headline_lock(). This set is allowed to under-count without being wrong: it
# does not need to be exhaustive for correctness, only for the gate to stay green — a
# surface stating the headline but missing from this set is caught loudly by the
# HEADLINE_SCAN_GLOBS tree-wide scan, block (j) of _self_test_headline_lock(), never
# silently accepted here. Treat this as a "known covered" record, not a trusted exhaustive
# inventory. Locate each entry's own statement by scanning the live file, never by a
# hardcoded line number (IN-01) — this module's own stated rule, since any unrelated edit
# to the file invalidates an unverified line-number comment.
COVERED_HEADLINE_SURFACES: frozenset[str] = frozenset({
    "docs/requirements-traceability.md",  # prose form (already gated pre-Phase-10)
    "CLAUDE.md",                          # prose form
    "docs/README.md",                     # prose form
    "docs/MEASUREMENT-MAP.md",            # prose form
    "docs/COMPONENT-DIAGRAM.md",          # slash form ONLY — no prose form in this file
})

# Whole-file historical exemption for HEADLINE-03: files whose entire purpose is recording a
# frozen or dated coverage figure. A hit in one of these files is never "the current claim"
# even with no arrow on the line — each entry below is a deliberate editorial decision, not a
# default, and every entry must carry its own justification.
#
# Three mechanical invariants are asserted by _self_test_headline_lock()'s (0) preamble: this
# set is disjoint from COVERED_HEADLINE_SURFACES; every entry resolves to an existing file
# (WR-01, WARNING scope); and, as of WR-03, this set's MEMBERSHIP is locked by name against a
# literal expectation — growth or shrinkage is a deliberate, reviewable edit in two places
# rather than a one-line change, the way REG-GUARD pins QUAL-01 as its own named exemption. A
# whole-file exemption disables both (f) and the tree-wide scan (j) for that file's entire
# contents, permanently, which is exactly why an unreviewed addition or removal must fail the
# gate rather than pass silently. The free-text "justification" prose in each entry's own
# comment below remains unenforced — only set MEMBERSHIP is mechanically locked.
#
# Safe-failure direction: because the search target used against this set is always the
# *current* literal derived live from build_matrix_rows() (never a generic numeric pattern), a
# value that is superseded stops matching the search the moment the headline moves — no entry
# here ever needs retiring on that account. This set only needs to grow (a new milestone-closure
# doc), and a document that states the current literal without an arrow and is missing from this
# set is not silently accepted: it is loudly caught as an unregistered surface by the tree-wide
# scan, block (j) of _self_test_headline_lock(), never here.
HISTORICAL_EXEMPT_FILES: frozenset[str] = frozenset({
    "CHANGELOG.md",                 # dated log by definition; already covered by the arrow
                                     # layer at its single delta-row occurrence (located by
                                     # scanning, never by line number — this block's own
                                     # stated rule, and a log that gains entries at the TOP on
                                     # every release invalidates a line-number note by the next
                                     # version bump), kept here too because a dated log is
                                     # definitionally historical narration
    "docs/v8.0-final-closure.md",   # frozen v8.0 terminal record; its "Superseded" callout
                                     # states both current renderings with NO arrow on that
                                     # line — the live proof that the arrow layer alone is
                                     # insufficient and the whole-file layer is load-bearing here
})

# Tree-wide scan scope for HEADLINE-05 (unregistered-surface detection): the same
# non-recursive, hand-curated glob idiom as check-links.py's DOCS_CHECK_GLOBS — Path.glob()
# only, with no tree-walking helper and no shell-out of any kind. Any tracked file matched
# here that states the current headline as a non-historical occurrence must also be a member
# of COVERED_HEADLINE_SURFACES, or the tree-wide scan in _self_test_headline_lock() fails,
# naming the file and line.
HEADLINE_SCAN_GLOBS: list[str] = [
    "docs/*.md",    # deliberately non-recursive: can never descend into docs/history/, which
                     # is git-ignored and untracked and must not be scanned
    "CLAUDE.md",     # already a registered current-fact surface (COVERED_HEADLINE_SURFACES)
    "CHANGELOG.md",  # whole-file historical exemption (HISTORICAL_EXEMPT_FILES)
    "README.md",     # repo root; matches zero occurrences today, included as forward
                     # protection against a future surface silently gaining a stale mention
]

# The two hand-maintained TRACE-03 doc rows block (n) locks. Named here, next to the constant
# whose transcription it checks, because every other multi-use path set in this module is a
# named module-level constant with a justification comment — and because block (n) exists
# precisely to catch hand-copied duplicates drifting, which made typing this pair twice inside
# (n) itself the module's own smallest instance of the defect it guards (CN-02, Phase 10
# review). Both files are current-fact surfaces for the gate inventory; CLAUDE.md is
# additionally a COVERED_HEADLINE_SURFACES member (for its coverage-headline statement, a
# different claim in a different section), docs/ARCHITECTURE.md is not.
_TRACE03_DOC_ROWS: tuple[str, ...] = ("CLAUDE.md", "docs/ARCHITECTURE.md")


# Arrow-layer tokens for _is_historical_headline_hit()'s figure-adjacency test (CR-03/WR-07).
# Neither constant contains any digit from the coverage headline itself. _HTML_COMMENT_CLOSE is
# defined FIRST and _ARROW_TOKENS references it by name (never retyped), because the same three
# bytes play a dual role in this tree: they close an HTML comment AND are a plausible way a
# Markdown author writes a delta arrow (the ASCII long arrow). That dual role is exactly why the
# comment strip below must remove only COMPLETE comments, and must run before the arrow test —
# treating every bare occurrence of "-->" as a comment terminator would silently delete a
# genuine delta's arrow (WR-07).
_HTML_COMMENT_CLOSE: str = "-->"
_ARROW_TOKENS: tuple[str, ...] = ("→", "->", _HTML_COMMENT_CLOSE)

# The SHAPE a coverage figure takes in the compact-slash rendering — four slash-separated
# integer counts — as a regex source fragment. It contains no digit of the headline itself,
# so it is not a hardcoded figure. Used only on the RIGHT-hand side of the arrow layer's
# second orientation, where "any digit run" was an undisclosed fail-open (WR-09, Phase 10
# review): a line stating the current figure followed by an arrow and ANY digits — a mermaid
# edge whose SOURCE label is the headline, a "current → projected" planning note, a table cell
# "| 161/91/0/252 | → | 5 |" — was silently exempted from both the per-surface presence
# assertion and the tree-wide scan, which is the direction that hides a CURRENT-FACT statement
# rather than a superseded one. The left-hand orientation deliberately keeps the looser
# "any digit run" form: there the current literal sits AFTER the arrow, so the line reads
# "superseded → current", and this tree writes that superseded reading in shapes narrower than
# a full 4-tuple (e.g. "147/90 → 161/91").
_COVERAGE_FIGURE_PATTERN: str = r"\d+/\d+/\d+/\d+"

# A fixed, non-current placeholder figure used to construct delta-shaped synthetic lines
# (a superseded reading, an arrow, then the current figure) throughout _self_test_headline_lock().
# It is not the headline and is therefore outside the no-literal rule that governs every other
# headline-adjacent figure in this module — but it is typed in exactly ONE place (IN-09): every
# consumer references this constant, never a retyped copy, so a future collision between this
# placeholder and a live headline degenerates loudly in one spot rather than in three silently.
# Block (0) asserts this constant differs from the live slash rendering.
_SUPERSEDED_PLACEHOLDER: str = "0/0/0/1"

# Non-greedy, single-pass match of a COMPLETE HTML comment (opening through closing marker),
# substituted with a space rather than the empty string so removing a comment can never join
# two previously separate tokens into a new false match. `re.DOTALL` is load-bearing as of the
# WR-06 fix: `_strip_complete_html_comments()` applies this pattern to WHOLE FILE TEXT, so a
# comment spanning several lines is matched as one span. Applied to a single line (which is
# what `_is_historical_headline_hit()` still does, deliberately — its input is one line by
# contract) the flag is inert, and while that was the only call site an ordinary block comment
# in any docs/*.md was reported by the tree-wide scan as a current-fact statement.
_HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)


def _strip_complete_html_comments(text: str) -> str:
    """Remove every COMPLETE HTML comment from `text`, preserving both the line count and
    token separation (WR-06, Phase 10 review).

    Each matched comment is replaced by a single space plus one newline per newline the
    comment spanned: the space stops the removal joining two previously separate tokens into
    a new false match (the reason the substitution was never the empty string), and the
    newlines keep every following line at its original 1-based number, which the scan's
    findings and every control's line-number assertion depend on.

    Only COMPLETE comments are removed — an unclosed "<!--" is left exactly as written, which
    is what keeps a bare "-->" available to the arrow layer as the ASCII long arrow rather
    than silently deleting a genuine delta's arrow (the WR-07 property (i2) arms 5 and 6 lock).
    """
    return _HTML_COMMENT_RE.sub(lambda _m: " " + "\n" * _m.group(0).count("\n"), text)


def _headline_literals() -> tuple[str, str]:
    """Derive the current coverage headline's two renderings live from build_matrix_rows().

    Returns (slash_rendering, prose_rendering) — slash first, so a caller unpacking both
    names cannot silently swap them without a type error going unnoticed.

    Deliberately NOT memoized — no caching decorator, no module-level cache variable. A cache
    would survive a monkeypatched build_matrix_rows() and silently defeat the headline-move
    simulation the verifier and block (h2) both depend on: both rely on calling this function
    again, after replacing build_matrix_rows(), and seeing the new figures reflected. Measured
    cost: 0.150 ms per call over 200 calls, which every call site in this module can afford
    without caching.
    """
    _rows = build_matrix_rows()
    _repro = sum(1 for r in _rows if r.coverage_tier == "reproducible")
    _audit = sum(1 for r in _rows if r.coverage_tier == "audit-only")
    _gap = sum(1 for r in _rows if r.coverage_tier == "gap")
    _slash_rendering = f"{_repro}/{_audit}/{_gap}/{len(_rows)}"
    _prose_rendering = (
        f"{_repro} reproducible / {_audit} audit-only / {_gap} gap / {len(_rows)} total"
    )
    return _slash_rendering, _prose_rendering


def _is_historical_headline_hit(
    relpath: str, line: str, literals: tuple[str, str] | None = None
) -> bool:
    """HEADLINE-03 two-layer historical classifier, shared by every consumer: the per-surface
    presence assertion, its positive controls, and the tree-wide unregistered-surface scan.

    A hit (a line already known to contain the current headline literal, in either rendering)
    is historical if EITHER layer applies, checked in this order:
      1. whole-file: relpath is a member of HISTORICAL_EXEMPT_FILES.
      2. figure-adjacent arrow: an arrow token (_ARROW_TOKENS) must delimit THIS line's
         headline mention from an adjacent figure, on one side or the other — a superseded
         reading (any digit run) immediately followed by the arrow and the current literal,
         or the current literal immediately followed by the arrow and a figure SHAPED like a
         coverage reading (_COVERAGE_FIGURE_PATTERN: four slash-separated counts). The two
         orientations are deliberately asymmetric (WR-09, Phase 10 review): the right-hand
         one used to accept any digit run, which silently exempted a current-fact statement
         followed by an arrow and anything numeric at all. A delta whose right-hand side is
         written in the PROSE rendering is therefore not exempted — fail-closed and loud,
         which is the safe direction here. An unrelated
         numeric arrow elsewhere on the line (a battery-count delta, a K-of-5 vector) is not
         evidence that THIS line's headline mention is historical; only an arrow anchored to
         the headline literal itself is. The HTML comment terminator is removed only as part
         of a COMPLETE comment before the arrow test runs (via _HTML_COMMENT_RE, substituting
         a space), so an open-but-unclosed marker can never supply an arrow, while a genuine
         delta written with the ASCII long arrow keeps it (WR-07).

    Deliberately does not do any tense, marker-word, or surrounding-prose detection — this tree
    contains at least four distinct historical phrasings ("stayed X", "moved to X", "from X to
    Y", "the then-current X") and a marker list could never be proven exhaustive. The two
    structural layers above are what the live tree actually requires (see the
    <measured_baseline> in this phase's plan) and nothing more.

    `literals`, when given, overrides the (slash, prose) pair the arrow layer anchors to
    instead of calling `_headline_literals()`. It exists for exactly one caller — block (h2)'s
    headline-move invariance control, which must evaluate a perturbed line against the SAME
    perturbed figure rather than the live one — and no production call site passes it.

    This narrowing was measured against the live tree during planning (Phase 10 Plan 04's
    <measured_baseline>, re-measured for the figure-anchored form in Plan 08): every one of the
    11 headline-bearing lines in the current scan scope keeps the identical classification
    under this anchored test that it had before — zero verdicts moved. The green self-test
    result after this change is therefore a checked property, not a hope.

    Three residual detection limits are disclosed, not closed: (1) a headline hard-wrapped
    across two physical lines is not detected — matching is line-scoped, as it always has been;
    (2) a line of the form "<digits> --> <current literal>" is treated as a delta even when it
    is a mermaid edge whose target label happens to begin with the headline text — measured as
    unreachable in this tree today; (3) symmetrically, "<current literal> --> <coverage-shaped
    figure>" is treated as a delta even when it is a mermaid edge whose SOURCE label is the
    headline. (3) is what remains of WR-09 after the right-hand narrowing above: it is far
    narrower than the previous "any digit run", and (i2) arms 7 and 8 lock both halves of the
    decision so it stays a choice rather than an accident. The verdict IS invariant when the figure and the line move
    TOGETHER (a real headline move does exactly that, and block (h2) asserts it); it is not,
    and was never claimed to be, independent of the figure altogether.
    """
    if relpath in HISTORICAL_EXEMPT_FILES:
        return True
    _slash_lit, _prose_lit = literals if literals is not None else _headline_literals()
    _stripped = _HTML_COMMENT_RE.sub(" ", line)
    for _tok in _ARROW_TOKENS:
        for _lit in (_slash_lit, _prose_lit):
            if re.search(
                rf"\d[\d\s/]*\s*{re.escape(_tok)}\s*{re.escape(_lit)}", _stripped
            ) or re.search(
                rf"{re.escape(_lit)}\s*{re.escape(_tok)}\s*{_COVERAGE_FIGURE_PATTERN}",
                _stripped,
            ):
                return True
    return False


def _headline_scan_files(globs: list[str]) -> list[Path]:
    """Expand a HEADLINE_SCAN_GLOBS-shaped glob list against REPO_ROOT with Path.glob,
    deduplicated by path, preserving sorted order per pattern (the check-links.py
    _collect_files idiom). Module level so block (j) and its non-vacuity control, block
    (l), call the identical function object — a control exercising a parallel copy would
    prove nothing (research Pitfall 4). No tree-walking helper, no shell-out.
    """
    _seen: set[Path] = set()
    _files: list[Path] = []
    for _glob_pattern in globs:
        for _candidate in sorted(REPO_ROOT.glob(_glob_pattern)):
            if _candidate not in _seen:
                _seen.add(_candidate)
                _files.append(_candidate)
    return _files


class _HeadlineScanRead(NamedTuple):
    """The single source of truth for what the (j) tree-wide scan actually read.

    Any caller recomputing reachability from a separate glob or `is_file()` sweep
    instead of reading these fields reintroduces BL-02 — the shipped defect where the
    PASS line's "reached" claim, and the accounted-hit floor, were derived from a
    different, more permissive filter than the one the read loop actually applied.
    """
    read_relpaths: set[str]
    hits_by_surface: dict[str, int]
    findings: list[tuple[str, str]]
    skipped: list[tuple[str, str]]
    read_errors: list[tuple[str, str]]


def _headline_scan_floor_breaches(read: _HeadlineScanRead) -> list[str]:
    """Derived coverage floor and accounted-hit floor for the tree-wide scan (CR-01 fix,
    BL-02 fix).

    Returns a list of breach descriptions (empty when both floors hold), evaluated in this
    order — coverage first, since an unreachable surface makes the accounted-hit count
    meaningless. Both floors are derived from the constants, never a magic number, so a
    narrowing typo or an emptied glob list is caught proportionally rather than only on
    total absence. Module level so block (j) and its non-vacuity controls, blocks (l) and
    (m), call the identical function object.

    The single parameter is the `_HeadlineScanRead` record itself, never a loose
    `set[str]` plus a loose `dict` (CR-01, Phase 10 review). Both floors read
    `read.read_relpaths` and `read.hits_by_surface` off that record, so the BL-02 wiring
    defect — feeding the coverage floor a glob-derived sweep such as
    `_scan_relpaths(_scan_files)` instead of what the read loop actually opened — is no
    longer expressible at any call site: a bare set has no `.read_relpaths`, and the
    attempt fails loudly instead of passing a green gate. Three (m) arms lock the helper's
    own semantics; this signature is what locks block (j)'s WIRING to it.

    Reachability here means "was READ" — a member of `read.read_relpaths`, the set
    `_headline_scan_read()` actually populated as it opened each candidate — deliberately
    NOT "was globbed" (that weaker question is `_scan_relpaths()`'s, over the raw
    glob-matched candidate list, which does not know whether the loop actually opened
    anything). Conflating the two was BL-02: a symlink resolving outside REPO_ROOT is
    "reached" by a bare glob-based `is_file()` sweep (which follows symlinks) but was never
    opened by the loop, so a surface the loop refused to read was still counted reached.

    The accounted-hit floor is PER SURFACE, never a running total compared against a
    cardinality: `read.hits_by_surface.get(surface, 0)` is checked individually for every member
    of COVERED_HEADLINE_SURFACES. A running-total floor has slack whenever any surface
    contributes more than one hit — measured on the live tree, docs/requirements-
    traceability.md contributes two, so a running total leaves exactly one registered
    surface free to go entirely unread while the floor still reports satisfied.
    """
    _unreachable = sorted(
        (COVERED_HEADLINE_SURFACES | HISTORICAL_EXEMPT_FILES) - read.read_relpaths
    )
    if _unreachable:
        return [
            f"(j) coverage floor unmet: the scan never READ {_unreachable} — the "
            "tree-wide scan cannot be load-bearing for surfaces it never opened"
        ]
    _starved = sorted(
        _surface
        for _surface in COVERED_HEADLINE_SURFACES
        if read.hits_by_surface.get(_surface, 0) < 1
    )
    if _starved:
        return [
            f"(j) accounted-hit floor unmet: {_starved} registered surface(s) accounted "
            "for zero non-historical hits — either the scan is not reading what it claims "
            "to read, or that surface no longer states the current headline (check the "
            "(f) results above first)"
        ]
    return []


def _headline_hits(text: str) -> list[tuple[int, str]]:
    """Return every (1-based line number, line text) pair whose line states either
    the current headline's prose or compact-slash rendering, after complete HTML comments
    have been stripped from the whole text (see `_strip_complete_html_comments()`).

    Both renderings are matched with a DIGIT BOUNDARY on each side, not as unbounded
    substrings (WR-08, Phase 10 review): `_headline_hits("build 1161/91/0/2521 was fine")`
    used to report a headline occurrence, so any docs/*.md line carrying a longer figure that
    happens to embed the current slash rendering — a build number, a byte count, a future
    4-tuple — would produce an unregistered-surface FAIL naming a line that does not state the
    headline at all, an unactionable red gate. The boundary is expressed as a lookaround on
    each side rather than \b, because the renderings begin and end with digits and \b would
    also fire between a digit and a slash.

    Shared by every per-surface assertion in `_self_test_headline_lock()`, its own
    non-vacuity control, and the (j) tree-wide scan via `_headline_scan_read()` — never
    re-implemented in parallel — so a control that calls this function proves the real
    assertion's code path is non-vacuous, not a copy that could silently diverge.

    This function deliberately has NO `literals` override. It carried one, documented as
    existing "only so a headline-move control can drive it explicitly", but no control was
    ever written: all four call sites used the default, and the (h2) headline-move control
    goes through `_is_historical_headline_hit()`'s own `literals` parameter instead. An
    untested branch in a gate whose stated design rule is that every helper is exercised by
    the identical function object its real assertion calls is worth less than nothing, so it
    was deleted rather than left as a claim (WR-07, Phase 10 review). If a future control
    genuinely needs to drive a headline move at this layer, add it back together with that
    control, in the same commit.
    """
    _slash_lit, _prose_lit = _headline_literals()
    _bounded = tuple(
        re.compile(rf"(?<!\d){re.escape(_lit)}(?!\d)") for _lit in (_slash_lit, _prose_lit)
    )
    return [
        (_i, _line)
        for _i, _line in enumerate(
            _strip_complete_html_comments(text).splitlines(), start=1
        )
        if any(_pattern.search(_line) for _pattern in _bounded)
    ]


def _non_historical_headline_hits(
    text: str, relpath: str
) -> list[tuple[int, str]]:
    """Block (f)'s tightened per-surface presence predicate (HEADLINE-03, Phase 10 Plan 02),
    expressed exactly once at module level: every headline hit in `text` that
    `_is_historical_headline_hit()` does NOT call historical, at `relpath`.

    The tightening is what stops a surface whose only occurrence is a ledger delta or a
    historical statement from satisfying (f) on a technicality. It lives here rather than
    inline in (f)'s loop so that (f), its (g) perturbation control, and the (f2) synthetic
    control all drive the IDENTICAL function object — the module's standing rule (research
    Pitfall 4: a control exercising a parallel copy proves nothing). Reverting the tightening
    (returning every hit) therefore fails (f2) rather than leaving the gate green, which is
    what it did while this predicate was an inline comprehension (WR-01, Phase 10 review).
    """
    return [
        (_lineno, _line)
        for _lineno, _line in _headline_hits(text)
        if not _is_historical_headline_hit(relpath, _line)
    ]


def _unregistered_headline_finding(
    relpath: str, hit: tuple[int, str]
) -> tuple[bool, str]:
    """The (j) scan's per-hit decision, shared by the real scan (via
    `_headline_scan_read()`) and its (k) non-vacuity control — a control exercising a
    parallel copy would prove nothing (research Pitfall 4). Returns
    (is_finding, message-or-empty-string).

    A hit is a finding only if BOTH of these hold: `_is_historical_headline_hit()`
    classifies it non-historical, AND `relpath` is absent from
    COVERED_HEADLINE_SURFACES. Gating the decision behind the classifier first is what
    proves the scan cannot false-positive on a correctly historical or delta statement
    (T-10-07) — HEADLINE-05's documented dependency on HEADLINE-03 is enforced by this
    function calling the classifier directly, not by convention.
    """
    _lineno, _line = hit
    if _is_historical_headline_hit(relpath, _line):
        return False, ""
    if relpath in COVERED_HEADLINE_SURFACES:
        return False, ""
    return True, (
        f"{relpath}:{_lineno} states the current headline as a non-historical "
        "occurrence but is not registered in COVERED_HEADLINE_SURFACES"
    )


def _scan_relpaths(files: list[Path]) -> set[str]:
    """REPO_ROOT-relative POSIX relpath of every regular file in `files`.

    This is the GLOB-reach definition (IN-07): it answers "which registered paths did
    the globs MATCH", never "which did the scan actually OPEN". Those are two different
    questions, and conflating them is BL-02's root cause. The single source of truth for
    what the tree-wide scan actually read is `_headline_scan_read().read_relpaths`,
    never this function.
    """
    return {_p.relative_to(REPO_ROOT).as_posix() for _p in files if _p.is_file()}


def _headline_read_or_fail(
    path: Path, label: str, wrong_results: list[str]
) -> str | None:
    """Read `path` as UTF-8 for a HEADLINE-LOCK assertion, or record a named FAIL and return
    None (CN-03, Phase 10 review).

    `_headline_scan_read()` catches `UnicodeDecodeError` and `OSError` on the tree-wide scan's
    reads and converts them into named findings, with a docstring paragraph explaining why —
    but the sentinel's own five live-file reads were unguarded, so a permission change, a
    truncated checkout, or a non-UTF-8 byte in any one of them exited `--self-test` with a
    traceback rather than a finding. This helper is that same policy in one place for those
    reads. Every call site keeps its own `is_file()` guard and its own "not found" message:
    absence and unreadability are different defects and stay differently worded.

    Returns the file's text, or None once a FAIL has been printed and appended. A caller
    receiving None must skip whatever it would have asserted — the finding is already
    recorded, so a second one would double-count the same defect.
    """
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as _decode_exc:
        print(
            f"  HEADLINE-LOCK FAIL: {label} could not be decoded as UTF-8: {_decode_exc}"
        )
        wrong_results.append(f"HEADLINE-LOCK: {label} could not be decoded as UTF-8")
        return None
    except OSError as _os_exc:
        print(f"  HEADLINE-LOCK FAIL: {label} could not be read: {_os_exc}")
        wrong_results.append(f"HEADLINE-LOCK: {label} could not be read")
        return None


def _headline_scan_read(
    scan_files: list[Path], root: Path | None = None
) -> _HeadlineScanRead:
    """Open and classify every candidate in `scan_files`, returning a structured record
    of exactly what happened — the single source of truth for what the (j) tree-wide
    scan read. Module level so block (j) and block (m)'s permanent controls call the
    identical function object (research Pitfall 4).

    `root` is the confinement boundary and the base for relpath derivation; it defaults to
    REPO_ROOT and no production call site passes it. It exists so (m)'s confinement and
    read-error arms can drive THIS function object over a throwaway tree — the only way to
    exercise the "resolves outside the root" and "could not be decoded" branches without
    writing anything inside the repository (WR-02/WR-03, Phase 10 review; before it, deleting
    the confinement guard outright, or collapsing both read-error handlers into a fail-open
    `except Exception: continue`, left --self-test green). Unlike `_headline_hits()`'s former
    dead `literals` parameter, this one is genuinely driven by a control, which is the whole
    reason it is here.

    `read_relpaths` and `hits_by_surface` are populated AS THE LOOP GOES, never
    recomputed afterwards from a separate glob or `is_file()` sweep — any caller that
    does so reintroduces BL-02. `hits_by_surface` carries an explicit zero entry for
    every relpath in `read_relpaths`, so a starved registered surface is representable
    rather than silently absent from the mapping.

    Every candidate the loop declines to open is recorded in `skipped` with a distinct
    reason ("not a regular file" or "resolves outside REPO_ROOT") — never a silent
    `continue`. A read error other than a UTF-8 decode failure — permission denied,
    is-a-directory, or any other `OSError` — is recorded in `read_errors` rather than
    propagating as a traceback out of --self-test (`UnicodeDecodeError` derives from
    `ValueError`, not `OSError`, so both are caught explicitly).

    Returns pure data: this function never prints and never touches wrong_results. The
    caller owns both.
    """
    _read_relpaths: set[str] = set()
    _hits_by_surface: dict[str, int] = {}
    _findings: list[tuple[str, str]] = []
    _skipped: list[tuple[str, str]] = []
    _read_errors: list[tuple[str, str]] = []
    _scan_root = REPO_ROOT if root is None else root
    _scan_root_resolved = _scan_root.resolve()

    for _scan_path in scan_files:
        if not _scan_path.is_file():
            _skipped.append((str(_scan_path), "not a regular file"))
            continue
        _resolved_scan_path = _scan_path.resolve()
        if not _resolved_scan_path.is_relative_to(_scan_root_resolved):
            _skipped.append((str(_scan_path), "resolves outside REPO_ROOT"))
            continue  # never follow a symlink resolving outside the repository
        try:
            _scan_text = _scan_path.read_text(encoding="utf-8")
        except UnicodeDecodeError as _decode_exc:
            _read_errors.append(
                (str(_scan_path), f"could not be decoded as UTF-8: {_decode_exc}")
            )
            continue
        except OSError as _os_exc:
            _read_errors.append((str(_scan_path), f"could not be read: {_os_exc}"))
            continue

        _scan_relpath = _scan_path.relative_to(_scan_root).as_posix()
        _read_relpaths.add(_scan_relpath)
        _hits_by_surface.setdefault(_scan_relpath, 0)
        for _hit in _headline_hits(_scan_text):
            _is_finding, _finding_msg = _unregistered_headline_finding(_scan_relpath, _hit)
            if _is_finding:
                _findings.append((_scan_relpath, _finding_msg))
            elif not _is_historical_headline_hit(_scan_relpath, _hit[1]):
                _hits_by_surface[_scan_relpath] += 1

    return _HeadlineScanRead(
        read_relpaths=_read_relpaths,
        hits_by_surface=_hits_by_surface,
        findings=_findings,
        skipped=_skipped,
        read_errors=_read_errors,
    )


# ---------------------------------------------------------------------------
# MatrixRow dataclass (D-12: single internal representation for dual output)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MatrixRow:
    key: str              # milestone-qualified: "v3.1/ROUTE-02"
    bare_id: str          # "ROUTE-02"
    milestone: str        # "v3.1"
    capability: str       # "Methodology" | "Test-Network"
    deliverable_path: str # live file path or "active-tail" sentinel
    coverage_tier: str    # "reproducible" | "audit-only" | "gap" | "scheduled"
    artifact_link: str    # resolves to real path/row/section or whitelist CLI
    gap_rationale: str    # non-empty when coverage_tier != "reproducible"


# ---------------------------------------------------------------------------
# Matrix row content — curated in Plan 02 (two inclusion paths per D-05)
# ---------------------------------------------------------------------------

# residual/ key prefix for non-milestone RR and S-N residuals.
# CONFIRMED at Task 3 checkpoint (82-02 Plan, 2026-06-14) — key scheme approved;
# no re-keying required. If scheme ever changes, update only this constant
# and re-run emit + check; the key form changes everywhere at once.
_RESIDUAL_KEY_PREFIX = "residual"


def _rows_methodology_agent() -> list[MatrixRow]:
    """v3.0 agent-body, sync, migrate, PKG, EVAL reqs — Methodology."""
    audit_rationale = "Validated by v3.0-MILESTONE-AUDIT; no re-runnable gate"
    return [
        MatrixRow("v3.0/AGENT-01", "AGENT-01", "v3.0", "Methodology",
                  "first-principles/agents/first-principles.md",
                  "audit-only", "", audit_rationale),
        MatrixRow("v3.0/AGENT-02", "AGENT-02", "v3.0", "Methodology",
                  "first-principles/agents/first-principles.md",
                  "audit-only", "", audit_rationale),
        MatrixRow("v3.0/AGENT-03", "AGENT-03", "v3.0", "Methodology",
                  "first-principles/agents/first-principles.md",
                  "audit-only", "", audit_rationale),
        MatrixRow("v3.0/AGENT-04", "AGENT-04", "v3.0", "Methodology",
                  "first-principles/agents/first-principles.md",
                  "audit-only", "", audit_rationale),
        MatrixRow("v3.0/AGENT-05", "AGENT-05", "v3.0", "Methodology",
                  "first-principles/agents/first-principles.md",
                  "audit-only", "", audit_rationale),
        MatrixRow("v3.0/AGENT-06", "AGENT-06", "v3.0", "Methodology",
                  "first-principles/agents/first-principles.md",
                  "audit-only", "", audit_rationale),
        MatrixRow("v3.0/SYNC-01", "SYNC-01", "v3.0", "Methodology",
                  "scripts/sync-content.py",
                  "audit-only", "", audit_rationale),
        MatrixRow("v3.0/SYNC-02", "SYNC-02", "v3.0", "Methodology",
                  "scripts/sync-content.py",
                  "audit-only", "", audit_rationale),
        MatrixRow("v3.0/SYNC-03", "SYNC-03", "v3.0", "Methodology",
                  "scripts/sync-content.py",
                  "audit-only", "", audit_rationale),
        MatrixRow("v3.0/SYNC-04", "SYNC-04", "v3.0", "Methodology",
                  "scripts/sync-content.py",
                  "audit-only", "", audit_rationale),
        MatrixRow("v3.0/PKG-01", "PKG-01", "v3.0", "Methodology",
                  "first-principles/agents/first-principles.md",
                  "audit-only", "", audit_rationale),
        MatrixRow("v3.0/PKG-02", "PKG-02", "v3.0", "Methodology",
                  "first-principles/agents/first-principles.md",
                  "audit-only", "", audit_rationale),
        MatrixRow("v3.0/EVAL-01", "EVAL-01", "v3.0", "Methodology",
                  "first-principles/agents/first-principles.md",
                  "audit-only", "", audit_rationale),
    ]


def _rows_methodology_agent_cont() -> list[MatrixRow]:
    """v3.0 MIGRATE/DEPR/GATE rows + v3.2 META rows — Methodology."""
    audit_v30 = "Validated by v3.0-MILESTONE-AUDIT; no re-runnable gate"
    audit_v32 = "Validated by v3.2-MILESTONE-AUDIT; no re-runnable gate"
    return [
        MatrixRow("v3.0/MIGRATE-01", "MIGRATE-01", "v3.0", "Methodology",
                  "first-principles/agents/first-principles.md",
                  "audit-only", "", audit_v30),
        MatrixRow("v3.0/MIGRATE-02", "MIGRATE-02", "v3.0", "Methodology",
                  "first-principles/agents/first-principles.md",
                  "audit-only", "", audit_v30),
        MatrixRow("v3.0/MIGRATE-03", "MIGRATE-03", "v3.0", "Methodology",
                  "first-principles/agents/first-principles.md",
                  "audit-only", "", audit_v30),
        MatrixRow("v3.0/MIGRATE-04", "MIGRATE-04", "v3.0", "Methodology",
                  "first-principles/agents/first-principles.md",
                  "audit-only", "", audit_v30),
        MatrixRow("v3.0/MIGRATE-05", "MIGRATE-05", "v3.0", "Methodology",
                  "first-principles/agents/first-principles.md",
                  "audit-only", "", audit_v30),
        MatrixRow("v3.0/MIGRATE-06", "MIGRATE-06", "v3.0", "Methodology",
                  "first-principles/agents/first-principles.md",
                  "audit-only", "", audit_v30),
        MatrixRow("v3.0/DEPR-01", "DEPR-01", "v3.0", "Methodology",
                  "first-principles/agents/first-principles.md",
                  "audit-only", "", audit_v30),
        MatrixRow("v3.0/DEPR-02", "DEPR-02", "v3.0", "Methodology",
                  "first-principles/agents/first-principles.md",
                  "audit-only", "", audit_v30),
        MatrixRow("v3.0/DEPR-03", "DEPR-03", "v3.0", "Methodology",
                  "first-principles/agents/first-principles.md",
                  "audit-only", "", audit_v30),
        # v3.2 — worked examples + rubric (META-*/META-Q-*)
        MatrixRow("v3.2/META-01", "META-01", "v3.2", "Methodology",
                  "first-principles/agents/references/examples",
                  "audit-only", "", audit_v32),
        MatrixRow("v3.2/META-02", "META-02", "v3.2", "Methodology",
                  "first-principles/agents/references/assumption-taxonomy.md",
                  "audit-only", "", audit_v32),
        MatrixRow("v3.2/META-03-SW", "META-03-SW", "v3.2", "Methodology",
                  "first-principles/agents/references/examples",
                  "audit-only", "", audit_v32),
        MatrixRow("v3.2/META-03-PB", "META-03-PB", "v3.2", "Methodology",
                  "first-principles/agents/references/examples",
                  "audit-only", "", audit_v32),
        MatrixRow("v3.2/META-03-PG", "META-03-PG", "v3.2", "Methodology",
                  "first-principles/agents/references/examples",
                  "audit-only", "", audit_v32),
        MatrixRow("v3.2/META-03-SE", "META-03-SE", "v3.2", "Methodology",
                  "first-principles/agents/references/examples",
                  "audit-only", "", audit_v32),
        MatrixRow("v3.2/META-Q1", "META-Q1", "v3.2", "Methodology",
                  "shared/spine/references/validation-rubric.md",
                  "audit-only", "", audit_v32),
        MatrixRow("v3.2/META-Q2", "META-Q2", "v3.2", "Methodology",
                  "first-principles/agents/first-principles.md",
                  "audit-only", "", audit_v32),
        MatrixRow("v3.2/META-Q3", "META-Q3", "v3.2", "Methodology",
                  "first-principles/agents/references/examples",
                  "audit-only", "", audit_v32),
        MatrixRow("v3.2/META-Q4", "META-Q4", "v3.2", "Methodology",
                  "scripts/check-body-budget.py",
                  "audit-only", "",
                  "TEARDOWN-01 (v8.7 Phase 163, docs/v8.7-constraint-teardown.md) retired the "
                  "body-budget pre-commit gate. scripts/check-body-budget.py is now report-only "
                  "(always exits 0) and scripts/git-hooks/pre-commit no longer invokes it — the "
                  "body line count is reported every firewall-battery run ([INFO] body-size) but "
                  "is not gated. META-Q4 is therefore audit-only (reported/inspectable), not "
                  "reproducibly enforced. Re-tiered reproducible -> audit-only in the v8.8 "
                  "post-close TEARDOWN-01 cleanup, replacing the prior vacuously-green tier."),
    ]


def _rows_methodology_rigor() -> list[MatrixRow]:
    """v3.7 RIGOR rows — Methodology (validation rubric).

    Rubric anchor strings must be substrings present in the rubric file
    (D-08 resolution: plain substring check after '#' split).
    These match the actual section headings in validation-rubric.md.
    """
    rubric = "shared/spine/references/validation-rubric.md"
    # Anchor text = literal substring expected in the rubric file
    crit1 = rubric + "#Criterion 1: Identify Essence"
    crit2 = rubric + "#Criterion 2: Challenge Assumptions"
    crit3 = rubric + "#Criterion 3: Establish Ground Truths"
    crit4 = rubric + "#Criterion 4: Reason Upward"
    crit5 = rubric + "#Criterion 5: Validate"
    crit6 = rubric + "#Criterion 6: Conclusion-to-Ground-Truth Traceability"
    r_link = rubric + "#How to Apply This Rubric"
    scoring = rubric + "#Scoring Model"
    return [
        MatrixRow("v3.7/RIGOR-01", "RIGOR-01", "v3.7", "Methodology",
                  rubric, "reproducible", crit1, ""),
        MatrixRow("v3.7/RIGOR-02", "RIGOR-02", "v3.7", "Methodology",
                  rubric, "reproducible", crit2, ""),
        MatrixRow("v3.7/RIGOR-03", "RIGOR-03", "v3.7", "Methodology",
                  rubric, "reproducible", crit3, ""),
        MatrixRow("v3.7/RIGOR-04", "RIGOR-04", "v3.7", "Methodology",
                  rubric, "reproducible", crit4, ""),
        MatrixRow("v3.7/RIGOR-05", "RIGOR-05", "v3.7", "Methodology",
                  rubric, "reproducible", crit5, ""),
        MatrixRow("v3.7/RIGOR-06", "RIGOR-06", "v3.7", "Methodology",
                  rubric, "reproducible", crit6, ""),
        MatrixRow("v3.7/RIGOR-07", "RIGOR-07", "v3.7", "Methodology",
                  rubric, "reproducible", r_link, ""),
        MatrixRow("v3.7/RIGOR-08", "RIGOR-08", "v3.7", "Methodology",
                  rubric, "reproducible", scoring, ""),
    ]


def _rows_methodology_focused_stubs() -> list[MatrixRow]:
    """v3.8 focused-mode stubs + v3.12 phase-level skills — Methodology."""
    audit_v38 = "Validated by v3.8-MILESTONE-AUDIT; no re-runnable gate"
    audit_v312 = "Validated by v3.12-MILESTONE-AUDIT; no re-runnable gate"
    fp_agent = "first-principles/agents/first-principles.md"
    fp_skills = "first-principles/skills"
    return [
        MatrixRow("v3.8/DISP-01", "DISP-01", "v3.8", "Methodology",
                  fp_agent, "audit-only", "", audit_v38),
        MatrixRow("v3.8/STUB-01", "STUB-01", "v3.8", "Methodology",
                  fp_skills, "audit-only", "", audit_v38),
        # EVAL-01's original deliverable, scripts/check-focused-output.py, was
        # retired at the 2026-08-16 audit (stream 2) after being superseded by
        # the merged check-routing-battery.py. The deliverable_path is repointed
        # at the successor rather than left dangling: deliverable_path is
        # reported, never existence-resolved (only artifact_link is), so a stale
        # path here would have failed silently and misled a matrix reader.
        MatrixRow("v3.8/EVAL-01", "EVAL-01", "v3.8", "Methodology",
                  "scripts/check-routing-battery.py",
                  "audit-only", "",
                  audit_v38 + ". Original deliverable scripts/check-focused-output.py"
                  " retired 2026-08-16 (superseded by the merged battery);"
                  " deliverable repointed to its successor."),
        MatrixRow("v3.12/PHASE-01", "PHASE-01", "v3.12", "Methodology",
                  fp_skills, "audit-only", "", audit_v312),
        MatrixRow("v3.12/PHASE-02", "PHASE-02", "v3.12", "Methodology",
                  fp_skills, "audit-only", "", audit_v312),
        MatrixRow("v3.12/PHASE-03", "PHASE-03", "v3.12", "Methodology",
                  fp_skills, "audit-only", "", audit_v312),
        MatrixRow("v3.12/PHASE-04", "PHASE-04", "v3.12", "Methodology",
                  fp_skills, "audit-only", "", audit_v312),
        MatrixRow("v3.12/PHASE-05", "PHASE-05", "v3.12", "Methodology",
                  fp_skills, "audit-only", "", audit_v312),
        MatrixRow("v3.12/PHASE-06", "PHASE-06", "v3.12", "Methodology",
                  fp_skills, "audit-only", "", audit_v312),
        MatrixRow("v3.12/PHASE-07", "PHASE-07", "v3.12", "Methodology",
                  fp_skills, "audit-only", "", audit_v312),
        MatrixRow("v3.12/PHASE-08", "PHASE-08", "v3.12", "Methodology",
                  fp_skills, "audit-only", "", audit_v312),
        MatrixRow("v3.12/PHASE-09", "PHASE-09", "v3.12", "Methodology",
                  fp_skills, "audit-only", "", audit_v312),
        MatrixRow("v3.12/PHASE-10", "PHASE-10", "v3.12", "Methodology",
                  fp_skills, "audit-only", "", audit_v312),
        MatrixRow("v3.13/TAX-01", "TAX-01", "v3.13", "Methodology",
                  "first-principles/agents/references/assumption-taxonomy.md",
                  "audit-only", "",
                  "Validated by v3.13-MILESTONE-AUDIT; no re-runnable gate"),
        MatrixRow("v3.13/TAX-02", "TAX-02", "v3.13", "Methodology",
                  "first-principles/agents/references/assumption-taxonomy.md",
                  "audit-only", "",
                  "Validated by v3.13-MILESTONE-AUDIT; no re-runnable gate"),
        MatrixRow("v3.13/WKEX-01", "WKEX-01", "v3.13", "Methodology",
                  "first-principles/agents/references/examples",
                  "audit-only", "",
                  "Validated by v3.13-MILESTONE-AUDIT; no re-runnable gate"),
        MatrixRow("v3.13/WKEX-02", "WKEX-02", "v3.13", "Methodology",
                  "first-principles/agents/references/examples",
                  "audit-only", "",
                  "Validated by v3.13-MILESTONE-AUDIT; no re-runnable gate"),
    ]


def _rows_testnet_ci_gates() -> list[MatrixRow]:
    """CI gate rows — Test-Network (VAL-01..05, DUAL-04, GATE-01..03, HOOK-*)."""
    hook = ".githooks/pre-commit"
    audit_v30 = "Validated by v3.0-MILESTONE-AUDIT; no re-runnable gate"
    audit_v33 = "Validated by v3.3-MILESTONE-AUDIT; no re-runnable gate"
    return [
        # VAL-01/02 via KNOWN_CLI_GATES whitelist (Pitfall 6)
        MatrixRow("v2.0/VAL-01", "VAL-01", "v2.0", "Test-Network",
                  "first-principles/agents/first-principles.md",
                  "reproducible", "claude plugin validate ./first-principles",
                  ""),
        MatrixRow("v2.0/VAL-02", "VAL-02", "v2.0", "Test-Network",
                  "first-principles/agents/first-principles.md",
                  "reproducible", "markdownlint-cli2", ""),
        MatrixRow("v2.0/VAL-03", "VAL-03", "v2.0", "Test-Network",
                  "scripts/check-links.py",
                  "reproducible", "scripts/check-links.py", ""),
        MatrixRow("v2.0/VAL-04", "VAL-04", "v2.0", "Test-Network",
                  "scripts/check-trigger-collisions.py",
                  "reproducible", "scripts/check-trigger-collisions.py", ""),
        MatrixRow("v2.0/VAL-05", "VAL-05", "v2.0", "Test-Network",
                  "scripts/check-description-budget.py",
                  "reproducible", "scripts/check-description-budget.py", ""),
        # v3.0 GATE rows
        MatrixRow("v3.0/GATE-01", "GATE-01", "v3.0", "Test-Network",
                  "scripts/check-agent.py",
                  "reproducible", "scripts/check-agent.py", ""),
        MatrixRow("v3.0/GATE-02", "GATE-02", "v3.0", "Test-Network",
                  "scripts/check-trigger-collisions.py",
                  "reproducible", "scripts/check-trigger-collisions.py", ""),
        MatrixRow("v3.0/GATE-03", "GATE-03", "v3.0", "Test-Network",
                  "scripts/sync-content.py",
                  "reproducible", "scripts/sync-content.py", ""),
        # DUAL-04 sync-check gate
        MatrixRow("v2.0/DUAL-04", "DUAL-04", "v2.0", "Test-Network",
                  "scripts/sync-content.py",
                  "audit-only", "",
                  "v2.0-MILESTONE-AUDIT passed; v2.0 DUAL-04 predates current --check flag"),
        # v3.3 body-budget pre-commit hook rows
        MatrixRow("v3.3/HOOK-01", "HOOK-01", "v3.3", "Test-Network",
                  hook, "audit-only", "", audit_v33),
        MatrixRow("v3.3/HOOK-02", "HOOK-02", "v3.3", "Test-Network",
                  hook, "audit-only", "", audit_v33),
        MatrixRow("v3.3/HOOK-03", "HOOK-03", "v3.3", "Test-Network",
                  hook, "audit-only", "", audit_v33),
        MatrixRow("v3.3/HOOK-04", "HOOK-04", "v3.3", "Test-Network",
                  hook, "reproducible", hook, ""),
        MatrixRow("v3.3/HOOK-05", "HOOK-05", "v3.3", "Test-Network",
                  hook, "reproducible", hook, ""),
        MatrixRow("v3.3/HOOK-06", "HOOK-06", "v3.3", "Test-Network",
                  hook, "audit-only", "", audit_v33),
        # v3.13 INFRA rows (CI extension)
        MatrixRow("v3.13/INFRA-01", "INFRA-01", "v3.13", "Test-Network",
                  "scripts/check-trigger-collisions.py",
                  "reproducible", "scripts/check-trigger-collisions.py", ""),
        MatrixRow("v3.13/INFRA-02", "INFRA-02", "v3.13", "Test-Network",
                  "scripts/check-description-budget.py",
                  "reproducible", "scripts/check-description-budget.py", ""),
        MatrixRow("v3.13/INFRA-03", "INFRA-03", "v3.13", "Test-Network",
                  "scripts/check-agent.py",
                  "reproducible", "scripts/check-agent.py", ""),
        MatrixRow("v3.13/INFRA-04", "INFRA-04", "v3.13", "Test-Network",
                  "scripts/check-links.py",
                  "reproducible", "scripts/check-links.py", ""),
        MatrixRow("v3.13/INFRA-05", "INFRA-05", "v3.13", "Test-Network",
                  "scripts/sync-content.py",
                  "reproducible", "scripts/sync-content.py", ""),
        MatrixRow("v3.13/INFRA-06", "INFRA-06", "v3.13", "Test-Network",
                  "scripts/check-trigger-collisions.py",
                  "reproducible", "scripts/check-trigger-collisions.py", ""),
    ]


def _rows_testnet_routing_battery() -> list[MatrixRow]:
    """Routing battery rows — Test-Network (v3.1 ROUTE + v3.4 NOISE + v3.5/3.6 CAT)."""
    cat = "tests/routing-catalog.md"
    audit_v31 = "Validated by v3.1-MILESTONE-AUDIT; no re-runnable gate"
    return [
        MatrixRow("v3.1/ROUTE-01", "ROUTE-01", "v3.1", "Test-Network",
                  "first-principles/agents/first-principles.md",
                  "audit-only", "", audit_v31),
        MatrixRow("v3.1/ROUTE-02", "ROUTE-02", "v3.1", "Test-Network",
                  "scripts/check-routing.py",
                  "reproducible", "scripts/check-routing.py", ""),
        MatrixRow("v3.1/ROUTE-03", "ROUTE-03", "v3.1", "Test-Network",
                  "docs/testing-agents-headlessly.md",
                  "audit-only", "", audit_v31),
        MatrixRow("v3.1/DOC-01", "DOC-01", "v3.1", "Test-Network",
                  "docs/testing-agents-headlessly.md",
                  "audit-only", "", audit_v31),
        MatrixRow("v3.4/NOISE-01", "NOISE-01", "v3.4", "Test-Network",
                  "scripts/check-routing.py",
                  "reproducible", "scripts/check-routing.py", ""),
        MatrixRow("v3.4/NOISE-02", "NOISE-02", "v3.4", "Test-Network",
                  "scripts/check-routing.py",
                  "reproducible", "scripts/check-routing.py", ""),
        MatrixRow("v3.4/NOISE-03", "NOISE-03", "v3.4", "Test-Network",
                  "scripts/check-routing.py",
                  "reproducible", "scripts/check-routing.py", ""),
        MatrixRow("v3.4/NOISE-04", "NOISE-04", "v3.4", "Test-Network",
                  "scripts/check-routing.py",
                  "reproducible", "scripts/check-routing.py", ""),
        MatrixRow("v3.4/NOISE-05", "NOISE-05", "v3.4", "Test-Network",
                  "scripts/check-routing.py",
                  "reproducible", "scripts/check-routing.py", ""),
        MatrixRow("v3.4/NOISE-06", "NOISE-06", "v3.4", "Test-Network",
                  "scripts/check-routing.py",
                  "reproducible", "scripts/check-routing.py", ""),
        MatrixRow("v3.5/FRAG-01", "FRAG-01", "v3.5", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.5/FRAG-02", "FRAG-02", "v3.5", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.5/FRAG-03", "FRAG-03", "v3.5", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.5/FRAG-04", "FRAG-04", "v3.5", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.5/FRAG-05", "FRAG-05", "v3.5", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.5/FRAG-06", "FRAG-06", "v3.5", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.5/FRAG-07", "FRAG-07", "v3.5", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.5/FRAG-08", "FRAG-08", "v3.5", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.5/FRAG-09", "FRAG-09", "v3.5", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.6/CAT-01", "CAT-01", "v3.6", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.6/CAT-02", "CAT-02", "v3.6", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.6/CAT-03", "CAT-03", "v3.6", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.6/CAT-04", "CAT-04", "v3.6", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.6/CAT-05", "CAT-05", "v3.6", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.6/CAT-06", "CAT-06", "v3.6", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.6/CAT-07", "CAT-07", "v3.6", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.6/CAT-08", "CAT-08", "v3.6", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.6/CAT-09", "CAT-09", "v3.6", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.6/CAT-10", "CAT-10", "v3.6", "Test-Network",
                  cat, "reproducible", cat, ""),
    ]


def _rows_testnet_routing_v38() -> list[MatrixRow]:
    """v3.8 FIXTURE/VERIFY/DOC-01 routing test rows — Test-Network."""
    audit_v38 = "Validated by v3.8-MILESTONE-AUDIT; no re-runnable gate"
    batt_script = "scripts/check-routing-battery.py"
    return [
        MatrixRow("v3.8/FIXTURE-01", "FIXTURE-01", "v3.8", "Test-Network",
                  "tests/step0-fixture-catalog.md",
                  "audit-only", "", audit_v38),
        MatrixRow("v3.8/FIXTURE-02", "FIXTURE-02", "v3.8", "Test-Network",
                  "tests/step0-fixture-catalog.md",
                  "audit-only", "", audit_v38),
        MatrixRow("v3.8/VERIFY-01", "VERIFY-01", "v3.8", "Test-Network",
                  batt_script, "reproducible", batt_script, ""),
        MatrixRow("v3.8/VERIFY-02", "VERIFY-02", "v3.8", "Test-Network",
                  batt_script, "reproducible", batt_script, ""),
        MatrixRow("v3.8/VERIFY-03", "VERIFY-03", "v3.8", "Test-Network",
                  batt_script, "reproducible", batt_script, ""),
        MatrixRow("v3.8/DOC-01", "DOC-01", "v3.8", "Test-Network",
                  "docs/testing-agents-headlessly.md",
                  "audit-only", "", audit_v38),
    ]


def _rows_testnet_routing_v39_plus() -> list[MatrixRow]:
    """v3.9 P8, v3.10 CONV, v3.11 MON, v3.13 META — Test-Network."""
    cat = "tests/routing-catalog.md"
    batt = "tests/routing-battery-catalog.md"
    audit_v39 = "Validated by v3.9-MILESTONE-AUDIT; no re-runnable gate"
    audit_v311 = "Validated by v3.11-MILESTONE-AUDIT; no re-runnable gate"
    return [
        # v3.9 P8 routing fix
        MatrixRow("v3.9/P8-01", "P8-01", "v3.9", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.9/P8-02", "P8-02", "v3.9", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.9/P8-03", "P8-03", "v3.9", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.9/P8-04", "P8-04", "v3.9", "Test-Network",
                  cat, "reproducible", cat, ""),
        # v3.10 CONV — convention files (test-network: new test gates)
        MatrixRow("v3.10/CONV-01", "CONV-01", "v3.10", "Test-Network",
                  ".planning/phases",
                  "audit-only", "",
                  "Validated by v3.10-MILESTONE-AUDIT; VERIFICATION.md convention files"),
        MatrixRow("v3.10/CONV-02", "CONV-02", "v3.10", "Test-Network",
                  ".planning/phases",
                  "audit-only", "",
                  "Validated by v3.10-MILESTONE-AUDIT; VALIDATION.md convention files"),
        # v3.11 MON — routing forward monitoring
        MatrixRow("v3.11/MON-01", "MON-01", "v3.11", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.11/MON-02", "MON-02", "v3.11", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.11/MON-03", "MON-03", "v3.11", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.11/MON-04", "MON-04", "v3.11", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.11/MON-05", "MON-05", "v3.11", "Test-Network",
                  cat, "audit-only", "", audit_v311),
        # v3.13 META-01/02 (routing-catalog content)
        MatrixRow("v3.13/META-01", "META-01", "v3.13", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v3.13/META-02", "META-02", "v3.13", "Test-Network",
                  cat, "reproducible", cat, ""),
    ]


def _rows_testnet_merged_battery() -> list[MatrixRow]:
    """v4.2 focused-output + v4.3 BATT merged-battery rows — Test-Network."""
    batt = "scripts/check-routing-battery.py"
    audit_v42 = "Validated by v4.2-MILESTONE-AUDIT; no re-runnable gate"
    audit_v43 = "Validated by v4.3-MILESTONE-AUDIT; no re-runnable gate"
    bcat = "tests/routing-battery-catalog.md"
    return [
        MatrixRow("v4.2/CAT-01", "CAT-01", "v4.2", "Test-Network",
                  bcat, "reproducible", batt, ""),
        MatrixRow("v4.2/CAT-02", "CAT-02", "v4.2", "Test-Network",
                  bcat, "reproducible", batt, ""),
        MatrixRow("v4.2/CAT-03", "CAT-03", "v4.2", "Test-Network",
                  bcat, "reproducible", batt, ""),
        MatrixRow("v4.2/CAT-04", "CAT-04", "v4.2", "Test-Network",
                  bcat, "reproducible", batt, ""),
        MatrixRow("v4.2/FOCUS-01", "FOCUS-01", "v4.2", "Test-Network",
                  batt, "reproducible", batt, ""),
        MatrixRow("v4.2/FOCUS-02", "FOCUS-02", "v4.2", "Test-Network",
                  batt, "reproducible", batt, ""),
        MatrixRow("v4.2/FOCUS-03", "FOCUS-03", "v4.2", "Test-Network",
                  batt, "reproducible", batt, ""),
        MatrixRow("v4.2/STRICT-01", "STRICT-01", "v4.2", "Test-Network",
                  batt, "reproducible", batt, ""),
        MatrixRow("v4.2/STRICT-02", "STRICT-02", "v4.2", "Test-Network",
                  batt, "reproducible", batt, ""),
        MatrixRow("v4.2/BASE-01", "BASE-01", "v4.2", "Test-Network",
                  "tests/routing-battery-baseline-v4.3.md",
                  "reproducible",
                  "tests/test_69_merged_baseline_invariants.py", ""),
        MatrixRow("v4.2/BASE-02", "BASE-02", "v4.2", "Test-Network",
                  "tests/routing-battery-baseline-v4.3.md",
                  "reproducible",
                  "tests/test_69_merged_baseline_invariants.py", ""),
        MatrixRow("v4.3/BATT-01", "BATT-01", "v4.3", "Test-Network",
                  batt, "reproducible", batt, ""),
        MatrixRow("v4.3/BATT-02", "BATT-02", "v4.3", "Test-Network",
                  batt, "reproducible", batt, ""),
        MatrixRow("v4.3/BATT-03", "BATT-03", "v4.3", "Test-Network",
                  batt, "reproducible", batt, ""),
        MatrixRow("v4.3/BATT-04", "BATT-04", "v4.3", "Test-Network",
                  batt, "reproducible", batt, ""),
        MatrixRow("v4.3/BATT-05", "BATT-05", "v4.3", "Test-Network",
                  batt, "reproducible", batt, ""),
        MatrixRow("v4.3/BATT-06", "BATT-06", "v4.3", "Test-Network",
                  batt, "reproducible", batt, ""),
        MatrixRow("v4.3/BATT-07", "BATT-07", "v4.3", "Test-Network",
                  "tests/routing-battery-baseline-v4.3.md",
                  "reproducible",
                  "tests/test_69_merged_baseline_invariants.py", ""),
        MatrixRow("v4.3/BATT-08", "BATT-08", "v4.3", "Test-Network",
                  "tests/routing-battery-baseline-v4.3.md",
                  "reproducible",
                  "tests/test_69_merged_baseline_invariants.py", ""),
    ]


def _rows_testnet_step0_harness() -> list[MatrixRow]:
    """v5.0 STEP0, v5.1 FIX/DET/SAFE/BASE — Test-Network."""
    emul = "scripts/check-step0-emulator.py"
    live = "scripts/check-step0-live.py"
    cat = "tests/step0-fixture-catalog.md"
    audit_v51 = "Validated by v5.1-MILESTONE-AUDIT; no re-runnable gate"
    return [
        # v5.0 Step 0 harness rows
        MatrixRow("v5.0/STEP0-01", "STEP0-01", "v5.0", "Test-Network",
                  emul, "reproducible", emul, ""),
        MatrixRow("v5.0/STEP0-02", "STEP0-02", "v5.0", "Test-Network",
                  live, "reproducible", live, ""),
        MatrixRow("v5.0/STEP0-03", "STEP0-03", "v5.0", "Test-Network",
                  cat, "reproducible", cat, ""),
        MatrixRow("v5.0/STEP0-04", "STEP0-04", "v5.0", "Test-Network",
                  emul, "reproducible", emul, ""),
        MatrixRow("v5.0/STEP0-05", "STEP0-05", "v5.0", "Test-Network",
                  live, "reproducible", live, ""),
        MatrixRow("v5.0/STEP0-06", "STEP0-06", "v5.0", "Test-Network",
                  live, "reproducible", live, ""),
        MatrixRow("v5.0/STEP0-07", "STEP0-07", "v5.0", "Test-Network",
                  live, "reproducible", live, ""),
        MatrixRow("v5.0/STEP0-08", "STEP0-08", "v5.0", "Test-Network",
                  emul, "reproducible", emul, ""),
        MatrixRow("v5.0/STEP0-09", "STEP0-09", "v5.0", "Test-Network",
                  cat, "reproducible", cat, ""),
        # v5.1 detector fix + safe rows
        MatrixRow("v5.1/FIX-01", "FIX-01", "v5.1", "Test-Network",
                  emul, "reproducible", emul, ""),
        MatrixRow("v5.1/FIX-02", "FIX-02", "v5.1", "Test-Network",
                  emul, "reproducible", emul, ""),
        MatrixRow("v5.1/FIX-03", "FIX-03", "v5.1", "Test-Network",
                  emul, "reproducible", emul, ""),
        MatrixRow("v5.1/DET-01", "DET-01", "v5.1", "Test-Network",
                  emul, "reproducible", emul, ""),
        MatrixRow("v5.1/DET-02", "DET-02", "v5.1", "Test-Network",
                  emul, "reproducible", emul, ""),
        MatrixRow("v5.1/DET-03", "DET-03", "v5.1", "Test-Network",
                  emul, "reproducible", emul, ""),
        MatrixRow("v5.1/SAFE-01", "SAFE-01", "v5.1", "Test-Network",
                  emul, "reproducible", emul, ""),
        MatrixRow("v5.1/SAFE-02", "SAFE-02", "v5.1", "Test-Network",
                  emul, "reproducible", emul, ""),
        MatrixRow("v5.1/SAFE-03", "SAFE-03", "v5.1", "Test-Network",
                  emul, "reproducible", emul, ""),
        MatrixRow("v5.1/BASE-01", "BASE-01", "v5.1", "Test-Network",
                  "tests/step0-baseline-v5.1.md",
                  "audit-only", "", audit_v51),
        MatrixRow("v5.1/BASE-02", "BASE-02", "v5.1", "Test-Network",
                  "tests/step0-baseline-v5.1.md",
                  "audit-only", "", audit_v51),
        MatrixRow("v5.1/BASE-03", "BASE-03", "v5.1", "Test-Network",
                  "tests/step0-baseline-v5.1.md",
                  "audit-only", "", audit_v51),
        MatrixRow("v5.1/BASE-04", "BASE-04", "v5.1", "Test-Network",
                  "tests/step0-baseline-v5.1.md",
                  "audit-only", "", audit_v51),
    ]


def _rows_testnet_v52_v53() -> list[MatrixRow]:
    """v5.2 DIAG/DET/ROUTE-10/REBASE + v5.3 DET/SAFE/REBASE/TOOL-01 — Test-Network."""
    emul = "scripts/check-step0-emulator.py"
    live = "scripts/check-step0-live.py"
    audit_v52 = "Validated by v5.2-MILESTONE-AUDIT; no re-runnable gate"
    audit_v53 = "Validated by v5.3-MILESTONE-AUDIT; no re-runnable gate"
    agent = "first-principles/agents/first-principles.md"
    return [
        MatrixRow("v5.2/DIAG-01", "DIAG-01", "v5.2", "Test-Network",
                  emul, "audit-only", "", audit_v52),
        MatrixRow("v5.2/DIAG-02", "DIAG-02", "v5.2", "Test-Network",
                  emul, "audit-only", "", audit_v52),
        MatrixRow("v5.2/DIAG-03", "DIAG-03", "v5.2", "Test-Network",
                  emul, "audit-only", "", audit_v52),
        MatrixRow("v5.2/DET-10", "DET-10", "v5.2", "Test-Network",
                  emul, "reproducible", emul, ""),
        MatrixRow("v5.2/DET-11", "DET-11", "v5.2", "Test-Network",
                  emul, "reproducible", emul, ""),
        MatrixRow("v5.2/DET-12", "DET-12", "v5.2", "Test-Network",
                  emul, "reproducible", emul, ""),
        MatrixRow("v5.2/ROUTE-10", "ROUTE-10", "v5.2", "Methodology",
                  agent, "audit-only", "", audit_v52),
        MatrixRow("v5.2/REBASE-01", "REBASE-01", "v5.2", "Test-Network",
                  "tests/step0-baseline-v5.2.md",
                  "audit-only", "", audit_v52),
        MatrixRow("v5.2/REBASE-02", "REBASE-02", "v5.2", "Test-Network",
                  "tests/step0-baseline-v5.2.md",
                  "audit-only", "", audit_v52),
        MatrixRow("v5.2/REBASE-03", "REBASE-03", "v5.2", "Test-Network",
                  "tests/step0-baseline-v5.2.md",
                  "audit-only", "", audit_v52),
        MatrixRow("v5.3/DET-13", "DET-13", "v5.3", "Test-Network",
                  emul, "reproducible", emul, ""),
        MatrixRow("v5.3/DET-14", "DET-14", "v5.3", "Test-Network",
                  emul, "reproducible", emul, ""),
        MatrixRow("v5.3/DET-15", "DET-15", "v5.3", "Test-Network",
                  emul, "reproducible", emul, ""),
        MatrixRow("v5.3/SAFE-04", "SAFE-04", "v5.3", "Test-Network",
                  emul, "reproducible", emul, ""),
        MatrixRow("v5.3/REBASE-04", "REBASE-04", "v5.3", "Test-Network",
                  "tests/step0-baseline-v5.3.md",
                  "audit-only", "", audit_v53),
        MatrixRow("v5.3/REBASE-05", "REBASE-05", "v5.3", "Test-Network",
                  "tests/step0-baseline-v5.3.md",
                  "audit-only", "", audit_v53),
        # v5.3/TOOL-01: quick task closure for check-routing.py (Test-Network)
        MatrixRow("v5.3/TOOL-01", "TOOL-01", "v5.3", "Test-Network",
                  "scripts/check-routing.py",
                  "audit-only", "", audit_v53),
    ]



def _rows_active_tail() -> list[MatrixRow]:
    """D-05 path (b): active-tail rows — included unconditionally, mixed tiers.

    These residuals are exempt from the deliverable-existence gate. GEN-01 has
    been flipped from 'scheduled' to 'reproducible' (Phase 93, D-08) — the Step 0
    classifier capability is now reproducibly measured by the committed v7.6 live
    re-baseline (tests/step0-baseline-v7.6.md, Phase 114). Earned by the committed
    baseline, not a passing score (BATTERY: FAIL, P 3/8 REGRESSION — honest
    v7.6 measured state). GEN-02 has been converted to coverage_tier='reproducible'
    (runbook + wrapper script, Phase 89) and no longer belongs to the open-gap set.

    Key form: v5.3/GEN-01 and v5.3/GEN-02 carry the canonical v5.3 milestone
    prefix. RR-80-01, RR-79-01, RR-114-01, RR-108-02, and RR-77-08 are non-milestone
    residuals that use the _RESIDUAL_KEY_PREFIX (confirmed at Task 3 checkpoint,
    82-02). RR-114-01 supersedes RR-108-01 (Phase 114 v7.6 carry-forward, S-P02
    inversion CARRIED 1/5); RR-108-02 is CLOSED at 4/5 (Phase 114 v7.6 re-baseline,
    S-P05 trade-off cleared min-pass — the lone canonical improver; ID retained,
    sentinel present as regression guard). Full chains: RR-79-02 ->
    RR-92-01 -> RR-95-01 -> RR-108-01 -> RR-114-01 (S-P02); RR-79-03 -> RR-92-02 ->
    RR-95-02 -> RR-108-02 CLOSED (S-P05).
    """
    p = _RESIDUAL_KEY_PREFIX  # e.g. "residual" — confirmed Task 3 checkpoint
    tail_rationale_gen01 = (
        "Full Step 0 classifier rearchitecture (GEN-01-REARCH, Phases 91-93). "
        "GEN-01 is now reproducible: the Step 0 classifier capability is reproducibly "
        "measured by committed live re-baselines (latest: v7.13 residual-delta, Phase 137). "
        "Earned by the committed baseline, not a passing score (reproducible = measured, not passing). "
        "Phase 129 v7.11 8-technique BATTERY: FAIL, P 4/8 (S-P01 5/5, S-P03 4/5, S-P05 5/5, "
        "S-P06 4/5 PASS; S-P02 2/5, S-P04 2/5, S-P10 0/5, S-P14 0/5 FAIL) — honest measured "
        "state (honesty-not-score, D-01). Prior baselines frozen: v7.6 (Phase 114, FAIL), "
        "v7.7 (Phase 117 CONF-01, SHORT OF BAR), v7.8 (Phase 119 CONF-03, targeted 6-row PASS). "
        "v7.11 dispositions (Phase 129; see docs/whole-system-remeasure-verdict.md): "
        "RR-79-01 S-P01 CLOSE SUSTAINED 5/5; RR-117-01 S-P03 fishbone CLOSE SUSTAINED 4/5; "
        "RR-108-02 S-P05 trade-off CLOSE SUSTAINED 5/5; "
        "RR-114-01 S-P02 inversion CARRIED 2/5 (supersedes RR-108-01); "
        "RR-108-04 estimate CARRIED 0/5; RR-108-05 theoretical-limit CARRIED 0/5 "
        "(both first genuine live measurement, v7.4 was spend-limit-indeterminate); "
        "RR-108-03 decompose RESOLVED-BY-MERGE (v7.5; sentinel stays on frozen v7.4 evidence). "
        "v7.13 residual-delta re-measure (Phase 137, 3-row filtered catalog; "
        "tests/step0-baseline-v7.8.md remains the canonical full 8-technique baseline): "
        "S-P02 inversion 1/5 CARRIED (RR-114-01, ID kept, no successor); "
        "S-P10 estimate 0/5 CARRIED (RR-108-04, ID kept); "
        "S-P14 theoretical-limit 0/5 CARRIED (RR-108-05, ID kept). "
        "Confirming artifact: tests/step0-baseline-v7.13.md."
    )
    tail_rationale_gen02 = (
        "Runbook + wrapper script established (Phase 89). Cadence: milestone boundary + "
        "detector-surface changes. See docs/live-monitoring-runbook.md."
    )
    return [
        MatrixRow(f"{p}/RR-80-01", "RR-80-01", p, "Test-Network",
                  "active-tail", "reproducible", "scripts/_battery_core.py#self_test_boundary", ""),
        MatrixRow("v5.3/GEN-01", "GEN-01", "v5.3", "Test-Network",
                  "active-tail", "reproducible", "tests/step0-baseline-v7.13.md",
                  tail_rationale_gen01),
        MatrixRow("v5.3/GEN-02", "GEN-02", "v5.3", "Test-Network",
                  "active-tail", "reproducible", "docs/live-monitoring-runbook.md",
                  tail_rationale_gen02),
        MatrixRow(f"{p}/RR-79-01", "RR-79-01", p, "Test-Network",
                  "active-tail", "reproducible", "scripts/_battery_core.py#self_test_boundary", ""),
        # RR-114-01 supersedes RR-108-01 (Phase 114 v7.6 carry-forward, S-P02 inversion CARRIED 1/5)
        # Full chain: RR-79-02 -> RR-92-01 -> RR-95-01 -> RR-108-01 -> RR-114-01
        MatrixRow(f"{p}/RR-114-01", "RR-114-01", p, "Test-Network",
                  "active-tail", "reproducible", "scripts/_battery_core.py#self_test_boundary", ""),
        # RR-108-02 supersedes RR-95-02 (Phase 108 v7.4 carry-forward, S-P05 trade-off CARRIED 2/5)
        # Full chain: RR-79-03 -> RR-92-02 -> RR-95-02 -> RR-108-02 CLOSED
        # CLOSED at 4/5 ≥ min-pass at Phase 114 v7.6 re-baseline (lone canonical improver;
        # ID retained, sentinel in _battery_core.self_test_boundary() re-pointed to v7.6 vector)
        MatrixRow(f"{p}/RR-108-02", "RR-108-02", p, "Test-Network",
                  "active-tail", "reproducible", "scripts/_battery_core.py#self_test_boundary", ""),
        MatrixRow(f"{p}/RR-77-08", "RR-77-08", p, "Test-Network",
                  "active-tail", "reproducible", "scripts/_battery_core.py#self_test_boundary", ""),
        # RR-117-01: S-P03 fishbone CLOSED at 5/5 at Phase 117 CONF-01; CLOSE SUSTAINED 4/5 at v7.8 CONF-03.
        # First fishbone vector sentinel; RR-75-03 lineage; re-pointed to v7.8 in Phase 119 CONF-04.
        MatrixRow(f"{p}/RR-117-01", "RR-117-01", p, "Test-Network",
                  "active-tail", "reproducible", "scripts/_battery_core.py#self_test_boundary", ""),
        # RR-117-02: S-N03 precision sentinel; D-17 precision finding; re-pointed to v7.8 in Phase 119 CONF-04.
        MatrixRow(f"{p}/RR-117-02", "RR-117-02", p, "Test-Network",
                  "active-tail", "reproducible", "scripts/_battery_core.py#self_test_boundary", ""),
        # RR-119-01: S-N01 over-routing RESOLVED-OVER-BAR at Phase 119 CONF-03 (v7.8 vector [0,2,1,1,3]).
        # Under-count caveat documented; NOT a reclassification (D-4, Phase 119 CONF-04).
        MatrixRow(f"{p}/RR-119-01", "RR-119-01", p, "Test-Network",
                  "active-tail", "reproducible", "scripts/_battery_core.py#self_test_boundary", ""),
        # RR-119-02: S-N02 over-routing RESOLVED-OVER-BAR at Phase 119 CONF-03 (v7.8 vector [0,3,3,1,1]).
        # Under-count caveat documented; NOT a reclassification (D-4, Phase 119 CONF-04).
        MatrixRow(f"{p}/RR-119-02", "RR-119-02", p, "Test-Network",
                  "active-tail", "reproducible", "scripts/_battery_core.py#self_test_boundary", ""),
    ]


def _rows_v79() -> list[MatrixRow]:
    """v7.9 milestone rows — 8 reproducible requirements (D-01 / Phase 123).

    All rows carry milestone="v7.9", coverage_tier="reproducible", gap_rationale="".
    Keys use the milestone-qualified form "v7.9/<bare_id>".

    D-02 PROHIBITION: no coverage_tier="scheduled" row here; RR-114-01 / trade-off
    live re-measure is a documented residual handled as prose in 123-02 (not a
    matrix row).

    The 8 requirements and their V79-ROWS TRACE-03 sentinel lock are added here
    as the first milestone block since v5.3. Three fix phases produce them:
      Phase 120 (Fix #3): NEGCAT-01/02 — Step 0 negative-catalog expansion
      Phase 121 (Fix #4): OCH-01/02/03 — output-contract headers + detector
      Phase 122 (Fix #5): COLLIDE-01/02 — dual-install collision checker
      Phase 123 (RECON):  RECON-01 — traceability reconcile + battery green

    Artifact_link resolution notes:
      NEGCAT-01/02: scripts/check-step0-emulator.py (owns STEP0-08 NEGCAT assertions)
      OCH-01:       scripts/sync-content.py (DUAL-04 gate; agent body zero-drift proven)
      OCH-02:       scripts/check-routing-battery.py (BATT-06 owns inversion/trade-off
                    heading-anchored marker assertions)
      OCH-03:       scripts/_battery_core.py#self_test_boundary (anchor substring in file)
      COLLIDE-01/02: scripts/check-install-collisions.py (COLLIDE-01 CI gate)
      RECON-01:     scripts/check-traceability.py (TRACE-03 self-test, this file)
    """
    return [
        MatrixRow("v7.9/NEGCAT-01", "NEGCAT-01", "v7.9", "Test-Network",
                  "tests/step0-fixture-catalog.md",
                  "reproducible", "scripts/check-step0-emulator.py", ""),
        MatrixRow("v7.9/NEGCAT-02", "NEGCAT-02", "v7.9", "Test-Network",
                  "scripts/check-step0-emulator.py",
                  "reproducible", "scripts/check-step0-emulator.py", ""),
        MatrixRow("v7.9/OCH-01", "OCH-01", "v7.9", "Methodology",
                  "shared/references/inversion.md",
                  "reproducible", "scripts/sync-content.py", ""),
        MatrixRow("v7.9/OCH-02", "OCH-02", "v7.9", "Test-Network",
                  "scripts/_battery_core.py",
                  "reproducible", "scripts/check-routing-battery.py", ""),
        MatrixRow("v7.9/OCH-03", "OCH-03", "v7.9", "Test-Network",
                  "scripts/_battery_core.py",
                  "reproducible", "scripts/_battery_core.py#self_test_boundary", ""),
        MatrixRow("v7.9/COLLIDE-01", "COLLIDE-01", "v7.9", "Test-Network",
                  "scripts/check-install-collisions.py",
                  "reproducible", "scripts/check-install-collisions.py", ""),
        MatrixRow("v7.9/COLLIDE-02", "COLLIDE-02", "v7.9", "Test-Network",
                  ".github/workflows/validation.yml",
                  "reproducible", "scripts/check-install-collisions.py", ""),
        MatrixRow("v7.9/RECON-01", "RECON-01", "v7.9", "Test-Network",
                  "docs/requirements-traceability.md",
                  "reproducible", "scripts/check-traceability.py", ""),
    ]


def _rows_v711() -> list[MatrixRow]:
    """v7.11 milestone rows — 11 audit-only requirements (D-04 / Phase 131).

    The v7.11 milestone is a whole-system live re-measure. Its own requirements
    (harness-readiness firewall, the three live re-baselines, and the terminal
    reconcile) are verified by ONE-SHOT MANUAL LIVE RUNS, not deterministic offline
    CI gates — so they are tiered "audit-only" (they grow the audit-only count, not
    reproducible), with artifact_link="" and a non-empty gap_rationale (D-04).

    Keys use the milestone-qualified form "v7.11/<bare_id>" — the "v7.11/" prefix
    prevents collision with the existing "v7.9/RECON-01" row.

    RR-130-01 (the main-routing inline-answering regression) is a DOCUMENTED RESIDUAL
    with NO matrix row (v7.9 D-02 precedent) — it is recorded as prose in
    docs/requirements-traceability.md, not here.
    """
    audit_v711 = (
        "Validated by the v7.11 whole-system live re-baseline (Phases 128-131); "
        "one-shot manual live run, no re-runnable offline gate (D-04). "
        "See docs/whole-system-remeasure-verdict.md."
    )
    return [
        MatrixRow("v7.11/READY-01", "READY-01", "v7.11", "Test-Network",
                  "scripts/check-firewall-battery.sh", "audit-only", "", audit_v711),
        MatrixRow("v7.11/READY-02", "READY-02", "v7.11", "Test-Network",
                  "scripts/check-step0-live.py", "audit-only", "", audit_v711),
        MatrixRow("v7.11/READY-03", "READY-03", "v7.11", "Test-Network",
                  "scripts/check-firewall-battery.sh", "audit-only", "", audit_v711),
        MatrixRow("v7.11/STEP0L-01", "STEP0L-01", "v7.11", "Test-Network",
                  "tests/step0-baseline-v7.11.md", "audit-only", "", audit_v711),
        MatrixRow("v7.11/STEP0L-02", "STEP0L-02", "v7.11", "Test-Network",
                  "tests/step0-baseline-v7.11.md", "audit-only", "", audit_v711),
        MatrixRow("v7.11/STEP0L-03", "STEP0L-03", "v7.11", "Test-Network",
                  "tests/step0-baseline-v7.11.md", "audit-only", "", audit_v711),
        MatrixRow("v7.11/ROUTEL-01", "ROUTEL-01", "v7.11", "Test-Network",
                  "tests/routing-baseline-v7.11.md", "audit-only", "", audit_v711),
        MatrixRow("v7.11/ROUTEL-02", "ROUTEL-02", "v7.11", "Test-Network",
                  "tests/routing-battery-baseline-v7.11.md", "audit-only", "", audit_v711),
        MatrixRow("v7.11/RECON-01", "RECON-01", "v7.11", "Test-Network",
                  "docs/whole-system-remeasure-verdict.md", "audit-only", "", audit_v711),
        MatrixRow("v7.11/RECON-02", "RECON-02", "v7.11", "Test-Network",
                  "tests/step0-captures-v7.11", "audit-only", "", audit_v711),
        MatrixRow("v7.11/RECON-03", "RECON-03", "v7.11", "Test-Network",
                  "docs/requirements-matrix.md", "audit-only", "", audit_v711),
    ]


def _rows_v818() -> list[MatrixRow]:
    """v8.18 milestone rows — 23 requirements, 21 reproducible + 2 audit-only (D-05/D-06, Phase 4).

    All rows carry milestone="v8.18". Keys use the milestone-qualified form
    "v8.18/<bare_id>".

    D-05 departure from Phase 142 D-01: `docs/requirements-traceability.md:11` records that
    v7.12, v7.13 and v8.0 requirements are validated by their milestone audits rather than
    matrix rows, because those milestones were live-measure and audit work with no
    deterministic offline gate behind their requirements. No v8.x milestone has added a row
    since v7.9 (Phase 123) for that reason. v8.18's requirements are the first since v7.9 to
    pass headline-history row 2's test — "each backed by a deterministic offline gate" —
    because HARN-01/HARN-02/HARN-03 are deterministic, offline, and (per D-01/D-03) both
    battery- and CI-registered. This is an application of the existing rule, not an exception
    to it. See the dated addendum beside the Phase 142 D-01 note in
    docs/requirements-traceability.md (D-08: the original note stays byte-intact).

    Capability assignment: ACT-*/LOOP-*/PAR-* change the agent's methodology prose, so they
    are "Methodology"; HARN-01..04 and SHIP-01/02/03/06 are harness and release apparatus, so
    they are "Test-Network"; SHIP-04 and SHIP-05 are records of the methodology milestone, so
    they are "Methodology" too — which under _SEVERITY_LABEL gives them MEDIUM rather than
    HIGH if either is ever downgraded to a gap, matching the judgment that a missing
    changelog entry is not a verification-system gap.

    Tiering (D-06, decided per row against "does something re-run", not by block):
    SHIP-04 (CHANGELOG entry exists) and SHIP-05 (docs record exists) are audit-only, with
    artifact_link="" and a non-empty gap_rationale — no gate re-runs to check a changelog
    entry or a docs/ record. The other 21 are reproducible with a named artifact_link:
      ACT-*                -> scripts/check-act-limb.py
      LOOP-*                -> scripts/check-loop-closure.py
      PAR-* / HARN-03       -> scripts/check-focused-parity.py
      HARN-01               -> scripts/check-act-limb.py
      HARN-02               -> scripts/check-loop-closure.py
      HARN-04, SHIP-03, SHIP-06 -> scripts/check-firewall-battery.sh
      SHIP-01               -> scripts/sync-content.py
      SHIP-02               -> scripts/check-version-stamps.py
    Rejected: all 23 reproducible (would give SHIP-04/SHIP-05 an artifact_link that does not
    exist — the vacuous-green shape this project has flagged four times).
    """
    audit_v818 = (
        "Validated by inspecting the shipped record — the CHANGELOG.md milestone entry "
        "(SHIP-04) or the docs/v8.18-praor-loop-closure.md milestone record (SHIP-05) — "
        "not by a re-runnable offline gate (D-06). No gate re-runs to check a changelog "
        "entry or a docs/ narrative exists, or is proposed, for either requirement."
    )
    return [
        MatrixRow("v8.18/ACT-01", "ACT-01", "v8.18", "Methodology",
                  "shared/spine/SKILL-body.md",
                  "reproducible", "scripts/check-act-limb.py", ""),
        MatrixRow("v8.18/ACT-02", "ACT-02", "v8.18", "Methodology",
                  "shared/spine/SKILL-body.md",
                  "reproducible", "scripts/check-act-limb.py", ""),
        MatrixRow("v8.18/ACT-03", "ACT-03", "v8.18", "Methodology",
                  "shared/spine/SKILL-body.md",
                  "reproducible", "scripts/check-act-limb.py", ""),
        MatrixRow("v8.18/ACT-04", "ACT-04", "v8.18", "Methodology",
                  "shared/spine/SKILL-body.md",
                  "reproducible", "scripts/check-act-limb.py", ""),
        MatrixRow("v8.18/ACT-05", "ACT-05", "v8.18", "Methodology",
                  "shared/spine/references/validation-rubric.md",
                  "reproducible", "scripts/check-act-limb.py", ""),
        MatrixRow("v8.18/LOOP-01", "LOOP-01", "v8.18", "Methodology",
                  "shared/spine/SKILL-body.md",
                  "reproducible", "scripts/check-loop-closure.py", ""),
        MatrixRow("v8.18/LOOP-02", "LOOP-02", "v8.18", "Methodology",
                  "shared/agent/input-contract.md",
                  "reproducible", "scripts/check-loop-closure.py", ""),
        MatrixRow("v8.18/LOOP-03", "LOOP-03", "v8.18", "Methodology",
                  "shared/spine/references/validation-rubric.md",
                  "reproducible", "scripts/check-loop-closure.py", ""),
        MatrixRow("v8.18/LOOP-04", "LOOP-04", "v8.18", "Methodology",
                  "shared/spine/SKILL-body.md",
                  "reproducible", "scripts/check-loop-closure.py", ""),
        MatrixRow("v8.18/LOOP-05", "LOOP-05", "v8.18", "Methodology",
                  "shared/spine/SKILL-body.md",
                  "reproducible", "scripts/check-loop-closure.py", ""),
        MatrixRow("v8.18/PAR-01", "PAR-01", "v8.18", "Methodology",
                  "shared/spine/SKILL-body.md",
                  "reproducible", "scripts/check-focused-parity.py", ""),
        MatrixRow("v8.18/PAR-02", "PAR-02", "v8.18", "Methodology",
                  "shared/spine/focused-validation-step.md",
                  "reproducible", "scripts/check-focused-parity.py", ""),
        MatrixRow("v8.18/PAR-03", "PAR-03", "v8.18", "Methodology",
                  "shared/spine/SKILL-body.md",
                  "reproducible", "scripts/check-focused-parity.py", ""),
        MatrixRow("v8.18/HARN-01", "HARN-01", "v8.18", "Test-Network",
                  "scripts/check-act-limb.py",
                  "reproducible", "scripts/check-act-limb.py", ""),
        MatrixRow("v8.18/HARN-02", "HARN-02", "v8.18", "Test-Network",
                  "scripts/check-loop-closure.py",
                  "reproducible", "scripts/check-loop-closure.py", ""),
        MatrixRow("v8.18/HARN-03", "HARN-03", "v8.18", "Test-Network",
                  "scripts/check-focused-parity.py",
                  "reproducible", "scripts/check-focused-parity.py", ""),
        MatrixRow("v8.18/HARN-04", "HARN-04", "v8.18", "Test-Network",
                  "scripts/check-firewall-battery.sh",
                  "reproducible", "scripts/check-firewall-battery.sh", ""),
        MatrixRow("v8.18/SHIP-01", "SHIP-01", "v8.18", "Test-Network",
                  "scripts/sync-content.py",
                  "reproducible", "scripts/sync-content.py", ""),
        MatrixRow("v8.18/SHIP-02", "SHIP-02", "v8.18", "Test-Network",
                  "scripts/check-version-stamps.py",
                  "reproducible", "scripts/check-version-stamps.py", ""),
        MatrixRow("v8.18/SHIP-03", "SHIP-03", "v8.18", "Test-Network",
                  "scripts/check-firewall-battery.sh",
                  "reproducible", "scripts/check-firewall-battery.sh", ""),
        MatrixRow("v8.18/SHIP-06", "SHIP-06", "v8.18", "Test-Network",
                  "scripts/check-firewall-battery.sh",
                  "reproducible", "scripts/check-firewall-battery.sh", ""),
        MatrixRow("v8.18/SHIP-04", "SHIP-04", "v8.18", "Methodology",
                  "CHANGELOG.md", "audit-only", "", audit_v818),
        MatrixRow("v8.18/SHIP-05", "SHIP-05", "v8.18", "Methodology",
                  "docs/v8.18-praor-loop-closure.md", "audit-only", "", audit_v818),
    ]


def _rows_v824() -> list[MatrixRow]:
    """v8.24 milestone rows — 15 requirements, 14 reproducible + 1 audit-only (D-06/D-07, Phase 6).

    All rows carry milestone="v8.24". Keys use the milestone-qualified form
    "v8.24/<bare_id>".

    Capability assignment, and the departure it makes: v8.18's discriminator was "changes the
    agent's methodology prose -> Methodology; harness and release apparatus -> Test-Network".
    None of v8.24's 15 requirements change agent methodology prose -- every one is verification
    apparatus or release bookkeeping -- so all 14 reproducible rows are Test-Network. VAL-04 is
    Methodology, following the SHIP-04/SHIP-05 carve-out exactly: an audit-only docs-record
    requirement is Methodology so _SEVERITY_LABEL reads MEDIUM rather than HIGH, matching this
    project's own stated judgment that a missing docs record is not a verification-system gap.
    This departs from 06-RESEARCH.md's "Open Questions" item 1, which recommended CAP-*/PROV-*
    -> Methodology, because those requirements are properties of gate scripts and a test
    fixture, not of the agent's prose.

    Tiering (D-07, decided per row against "does something re-run", not by block): 14
    reproducible, VAL-04 audit-only. All 15 reproducible is rejected for the same reason
    _rows_v818() rejects it -- VAL-04 would get an artifact_link that does not exist, the
    vacuous-green shape.

    CAP-01/CAP-03 (CR-02, v8.24 code review): both rows deliver into
    scripts/check-quality-harness.py, and both originally pointed their artifact_link at
    scripts/check-quality-harness.py's sibling scripts/check-provenance.py -- a script that
    mentions neither requirement and touches neither deliverable, so _resolve_artifact()'s
    bare-path existence check resolved it while nothing re-ran the requirement. Deleting the
    two self-test items would have left both rows reporting "reproducible" against an artifact
    that exists: the same vacuously-green shape the paragraph above rejects, and the shape
    headline-history row 6 (META-Q4) records. They now point at the assertions that actually
    re-run them, by symbol anchor rather than by file, so the link binds to the assertion:
    QUAL-01's _selftest_analysis_persistence() ("Item 20 (v8.24.0 Phase 4, CAP-01)") and
    _selftest_capture_tool_reader() ("Item 19 (v8.24.0 Phase 4, CAP-03)"). CAP-02 keeps
    scripts/check-provenance.py -- its deliverable is the committed fixture, which that
    script's live leg genuinely reads.

    GATE-02 (WR-02, v8.24 code review): this row used to point at
    scripts/check-firewall-battery.sh with a docstring note conceding that no offline gate
    re-read .github/workflows/validation.yml -- which made "reproducible" a claim nothing
    could falsify, the vacuously-green shape this function's tiering paragraph above rejects
    for VAL-04. REG-GUARD now carries a real leg for it: verify_ci_job_registration() reads
    the battery's own `gate "<ID>"` registrations and every CI job's `name: <job> (<GATE-ID>)`
    field, and fails when a battery gate has no CI job (QUAL-01 is the single named
    battery-only exemption). Deleting the check-provenance job from validation.yml now turns
    REG-GUARD red -- measured as a live negative control -- so the artifact_link points at
    that assertion by symbol anchor, binding the row to the check rather than to a file's mere
    existence.
    """
    audit_v824 = (
        "Validated by inspecting the shipped record -- CLAUDE.md's CI gates table and this "
        "file's PROV-GUARD record -- not by a re-runnable offline gate. No gate re-runs to "
        "check that a docs record exists, and none is proposed (the v8.18 SHIP-04/SHIP-05 "
        "precedent, D-07)."
    )
    return [
        MatrixRow("v8.24/CAP-01", "CAP-01", "v8.24", "Test-Network",
                  "scripts/check-quality-harness.py",
                  "reproducible",
                  "scripts/check-quality-harness.py#_selftest_analysis_persistence", ""),
        MatrixRow("v8.24/CAP-02", "CAP-02", "v8.24", "Test-Network",
                  "tests/quality-provenance-v8.24/README.md",
                  "reproducible", "scripts/check-provenance.py", ""),
        MatrixRow("v8.24/CAP-03", "CAP-03", "v8.24", "Test-Network",
                  "scripts/check-quality-harness.py",
                  "reproducible",
                  "scripts/check-quality-harness.py#_selftest_capture_tool_reader", ""),
        MatrixRow("v8.24/PROV-01", "PROV-01", "v8.24", "Test-Network",
                  "scripts/check-provenance.py",
                  "reproducible", "scripts/check-provenance.py", ""),
        MatrixRow("v8.24/PROV-02", "PROV-02", "v8.24", "Test-Network",
                  "scripts/check-provenance.py",
                  "reproducible", "scripts/check-provenance.py", ""),
        MatrixRow("v8.24/PROV-03", "PROV-03", "v8.24", "Test-Network",
                  "scripts/check-provenance.py",
                  "reproducible", "scripts/check-provenance.py", ""),
        MatrixRow("v8.24/PROV-04", "PROV-04", "v8.24", "Test-Network",
                  "scripts/check-provenance.py",
                  "reproducible", "scripts/check-provenance.py", ""),
        MatrixRow("v8.24/PROV-05", "PROV-05", "v8.24", "Test-Network",
                  "scripts/check-quality-harness.py",
                  "reproducible", "scripts/check-provenance.py", ""),
        MatrixRow("v8.24/GATE-01", "GATE-01", "v8.24", "Test-Network",
                  "scripts/check-provenance.py",
                  "reproducible", "scripts/check-provenance.py", ""),
        MatrixRow("v8.24/GATE-02", "GATE-02", "v8.24", "Test-Network",
                  ".github/workflows/validation.yml",
                  "reproducible",
                  "scripts/check-registration.py#verify_ci_job_registration", ""),
        MatrixRow("v8.24/GATE-03", "GATE-03", "v8.24", "Test-Network",
                  "scripts/check-firewall-battery.sh",
                  "reproducible", "scripts/check-firewall-battery.sh", ""),
        MatrixRow("v8.24/VAL-01", "VAL-01", "v8.24", "Test-Network",
                  "scripts/check-firewall-battery.sh",
                  "reproducible", "scripts/check-firewall-battery.sh", ""),
        MatrixRow("v8.24/VAL-02", "VAL-02", "v8.24", "Test-Network",
                  "scripts/check-version-stamps.py",
                  "reproducible", "scripts/check-version-stamps.py", ""),
        MatrixRow("v8.24/VAL-03", "VAL-03", "v8.24", "Test-Network",
                  "scripts/sync-content.py",
                  "reproducible", "scripts/sync-content.py", ""),
        MatrixRow("v8.24/VAL-04", "VAL-04", "v8.24", "Methodology",
                  "CLAUDE.md", "audit-only", "", audit_v824),
    ]


def _rows_v825() -> list[MatrixRow]:
    """v8.25 milestone rows — 14 requirements, 13 reproducible + 1 audit-only (Phase 12).

    All rows carry milestone="v8.25". Keys use the milestone-qualified form
    "v8.25/<bare_id>".

    Capability assignment, and the departure it makes: v8.24's discriminator assigned all 14
    reproducible rows Test-Network because none of that milestone's requirements touched agent
    prose. CONTRACT-01..05 are different in kind: their deliverable is literally
    output-template.md / SKILL-body.md prose (the emission contract), which the discriminator's
    own stated rule ("changes the agent's methodology prose -> Methodology") puts in
    Methodology, not Test-Network. This has zero severity effect while these rows stay
    reproducible (_SEVERITY_LABEL only maps gap/audit-only tiers). HEADLINE-* and SHIP-* are
    Test-Network apparatus, matching the v8.18/v8.24 precedent. CONTRACT-06 is Test-Network
    because the claim is about detector code (check-quality-harness.py), not agent prose.

    Tiering, decided per row against "does something re-run", not by block: 13 reproducible,
    CONTRACT-06 audit-only. Two contested calls, both recorded rather than hidden, each
    independently reversible without moving this row's total (266) — see
    .planning/phases/12-integration-ship/12-RESEARCH.md §A for the full argument:
      - A1 — CONTRACT-06's tier. Nothing in the tree pins _chain_block_well_formed
        byte-unchanged (the sha256 in .planning/PROJECT.md:41 is prose; the only real sha256
        pin, check-quality-harness.py:7193, covers _RENDER_RULE_LITERALS, a different claim).
        Tiered audit-only rather than backed by a new sha256-freeze control, matching the v8.18
        SHIP-04/SHIP-05 precedent (no gate re-runs to check that a byte-freeze claim holds).
        The alternative is filed as backlog 999.17, not implemented.
      - A2 — SHIP-03's tier. _self_test_headline_lock predates this phase's rows (authored and
        mutation-tested in Phase 10), so this is a held-out oracle applied to new input, not a
        tautology. Tiered reproducible against it.
    """
    audit_v825 = (
        "Nothing in the tree pins _chain_block_well_formed byte-unchanged -- the sha256 in "
        ".planning/PROJECT.md:41 is prose, and the only real sha256 pin in "
        "scripts/check-quality-harness.py:7193 covers _RENDER_RULE_LITERALS, a different "
        "claim; no gate re-runs to check that a byte-freeze holds (the v8.18 SHIP-04/SHIP-05 "
        "precedent, D-07)."
    )
    return [
        MatrixRow("v8.25/HEADLINE-01", "HEADLINE-01", "v8.25", "Test-Network",
                  "scripts/check-traceability.py",
                  "reproducible",
                  "scripts/check-traceability.py#_headline_lock_surfaces", ""),
        MatrixRow("v8.25/HEADLINE-02", "HEADLINE-02", "v8.25", "Test-Network",
                  "scripts/check-traceability.py",
                  "reproducible",
                  "scripts/check-traceability.py#_headline_literals", ""),
        MatrixRow("v8.25/HEADLINE-03", "HEADLINE-03", "v8.25", "Test-Network",
                  "scripts/check-traceability.py",
                  "reproducible",
                  "scripts/check-traceability.py#_is_historical_headline_hit", ""),
        MatrixRow("v8.25/HEADLINE-04", "HEADLINE-04", "v8.25", "Test-Network",
                  "scripts/check-traceability.py",
                  "reproducible",
                  "scripts/check-traceability.py#_headline_lock_surfaces", ""),
        MatrixRow("v8.25/HEADLINE-05", "HEADLINE-05", "v8.25", "Test-Network",
                  "scripts/check-traceability.py",
                  "reproducible",
                  "scripts/check-traceability.py#_headline_lock_scan", ""),
        MatrixRow("v8.25/CONTRACT-01", "CONTRACT-01", "v8.25", "Methodology",
                  "shared/spine/references/output-template.md",
                  "reproducible",
                  "scripts/check-quality-harness.py#_selftest_render_contract", ""),
        MatrixRow("v8.25/CONTRACT-02", "CONTRACT-02", "v8.25", "Methodology",
                  "shared/spine/references/output-template.md",
                  "reproducible",
                  "scripts/check-quality-harness.py#_selftest_render_contract", ""),
        MatrixRow("v8.25/CONTRACT-03", "CONTRACT-03", "v8.25", "Methodology",
                  "shared/spine/SKILL-body.md",
                  "reproducible",
                  "scripts/check-quality-harness.py#_selftest_render_contract", ""),
        MatrixRow("v8.25/CONTRACT-04", "CONTRACT-04", "v8.25", "Methodology",
                  "shared/spine/references/output-template.md",
                  "reproducible",
                  "scripts/check-quality-harness.py#_selftest_render_contract", ""),
        MatrixRow("v8.25/CONTRACT-05", "CONTRACT-05", "v8.25", "Methodology",
                  "shared/spine/SKILL-body.md",
                  "reproducible",
                  "scripts/check-quality-harness.py#_selftest_render_contract", ""),
        MatrixRow("v8.25/CONTRACT-06", "CONTRACT-06", "v8.25", "Test-Network",
                  "scripts/check-quality-harness.py",
                  "audit-only", "", audit_v825),
        MatrixRow("v8.25/SHIP-01", "SHIP-01", "v8.25", "Test-Network",
                  "scripts/check-version-stamps.py",
                  "reproducible", "scripts/check-version-stamps.py", ""),
        MatrixRow("v8.25/SHIP-02", "SHIP-02", "v8.25", "Test-Network",
                  "scripts/check-firewall-battery.sh",
                  "reproducible", "scripts/check-firewall-battery.sh", ""),
        MatrixRow("v8.25/SHIP-03", "SHIP-03", "v8.25", "Test-Network",
                  "scripts/check-traceability.py",
                  "reproducible",
                  "scripts/check-traceability.py#_self_test_headline_lock", ""),
    ]


def build_matrix_rows() -> list[MatrixRow]:
    """Return the curated list of MatrixRow objects (Plan 02 — fully populated).

    Seven inclusion paths. (a)-(c) were enumerated per the original D-05; (d) has been in the
    body since Phase 131 RECON-03 but went undocumented here until 2026-08-29; (e) was added
    at v8.18 Phase 4; (f) was added at v8.24 Phase 6; (g) was added at v8.25 Phase 12.
    (a) Live-shipping requirements — deliverable-gated (D-01/D-02/D-03).
        Grouped by capability (D-04): Methodology first, then Test-Network.
    (b) Active tail — included unconditionally (see `_rows_active_tail()`); all reproducible (D-05b):
        GEN-01 reproducible (Phase 93 flip, artifact bumped to v7.11 baseline Phase 131 RECON-03),
        GEN-02 + residuals reproducible. RR-114-01 supersedes RR-108-01 (Phase 114 v7.6);
        RR-108-02 CLOSED at 4/5 v7.6 (ID retained, sentinel present);
        RR-117-01/RR-117-02 added Phase 117 CONF-02; RR-119-01/RR-119-02 added Phase 119 CONF-04.
    (c) v7.9 milestone (8 rows) — first milestone block since v5.3; all reproducible
        (Phase 123, D-01). NEGCAT-01/02 (Phase 120), OCH-01/02/03 (Phase 121),
        COLLIDE-01/02 (Phase 122), RECON-01 (Phase 123).
    (d) v7.11 milestone (11 rows) — all audit-only (Phase 131 RECON-03, D-04): validated by
        one-shot manual live runs, not by deterministic offline CI gates, which is why they
        carry artifact_link="" and a shared gap_rationale. See `_rows_v711()`. This path was
        present in the body from Phase 131 but absent from this docstring until 2026-08-29;
        its absence is what made the "first block since v7.9" claim below look true.
    (e) v8.18 milestone (23 rows, 21 reproducible + 2 audit-only) — first **v8.x** milestone block
        since v7.9 (Phase 4/D-05; the v7.11 block at (d) is the last non-v8.x addition): the
        discriminator is headline-history row 2's phrase "each backed by a deterministic offline
        gate", which v7.12, v7.13 and v8.0 did not satisfy but HARN-01/02/03 do. See
        `_rows_v818()` for the full per-row rationale.
    (f) v8.24 milestone (15 rows, 14 reproducible + 1 audit-only) — Phase 6/D-06/D-07: the
        milestone's CAP-*/PROV-*/GATE-*/VAL-* requirements, all Test-Network apparatus except
        VAL-04 (Methodology, audit-only — a docs record, not a re-runnable gate). See
        `_rows_v824()` for the full per-row rationale.
    (g) v8.25 milestone (14 rows, 13 reproducible + 1 audit-only) — Phase 12: the milestone's
        HEADLINE-*/CONTRACT-*/SHIP-* requirements. CONTRACT-01..05 carry Methodology (agent
        emission-contract prose), departing from (f)'s default-to-Test-Network choice because
        none of that milestone's rows touched agent prose; HEADLINE-* and SHIP-* stay
        Test-Network apparatus. CONTRACT-06 is audit-only (Test-Network) — no gate re-runs to
        check that its byte-freeze claim holds. See `_rows_v825()` for the full per-row
        rationale.

    The 'residual/' key prefix for non-milestone residuals is confirmed
    (Task 3 checkpoint, 82-02). See _RESIDUAL_KEY_PREFIX for the change point.
    """
    rows: list[MatrixRow] = []
    # --- Methodology capability ---
    rows.extend(_rows_methodology_agent())
    rows.extend(_rows_methodology_agent_cont())
    rows.extend(_rows_methodology_rigor())
    rows.extend(_rows_methodology_focused_stubs())
    # --- Test-Network capability ---
    rows.extend(_rows_testnet_ci_gates())
    rows.extend(_rows_testnet_routing_battery())
    rows.extend(_rows_testnet_routing_v38())
    rows.extend(_rows_testnet_routing_v39_plus())
    rows.extend(_rows_testnet_merged_battery())
    rows.extend(_rows_testnet_step0_harness())
    rows.extend(_rows_testnet_v52_v53())
    # --- Active tail (D-05 path b) ---
    rows.extend(_rows_active_tail())
    # --- v7.9 milestone (D-01 / Phase 123) ---
    rows.extend(_rows_v79())
    # --- v7.11 milestone (D-04 / Phase 131) — 11 audit-only rows ---
    rows.extend(_rows_v711())
    # --- v8.18 milestone (D-05 / Phase 4) — 21 reproducible + 2 audit-only ---
    rows.extend(_rows_v818())
    # --- v8.24 milestone (D-06 / Phase 6) — 14 reproducible + 1 audit-only ---
    rows.extend(_rows_v824())
    # --- v8.25 milestone (Phase 12 / A1 / A2) — 13 reproducible + 1 audit-only ---
    rows.extend(_rows_v825())
    return rows


# ---------------------------------------------------------------------------
# Python version guard
# ---------------------------------------------------------------------------


def _require_python_version() -> None:
    if sys.version_info < (3, 12):
        sys.stderr.write(
            f"scripts/check-traceability.py requires Python >=3.12 "
            f"(running {sys.version_info.major}.{sys.version_info.minor}).\n"
        )
        sys.exit(2)


# ---------------------------------------------------------------------------
# Path-confinement guard (T-82-01; loosened in Phase 83 to allow docs/)
# ---------------------------------------------------------------------------

ALLOWED_OUTPUT_ROOTS: tuple[Path, ...] = (
    (REPO_ROOT / ".planning").resolve(),
    (REPO_ROOT / "docs").resolve(),
)


def _resolve_confined_output(path: Path) -> Path:
    """Resolve path and enforce T-82-01: must be under REPO_ROOT/.planning/ or docs/.

    Returns the resolved absolute path if confined.
    Writes a stderr message and calls sys.exit(2) if the path escapes.
    """
    resolved = path.resolve()
    confined = any(
        resolved == root or str(resolved).startswith(str(root) + "/")
        for root in ALLOWED_OUTPUT_ROOTS
    )
    if not confined:
        sys.stderr.write(
            f"check-traceability: --output path must be under .planning/ or docs/ "
            f"(got: {resolved})\n"
        )
        sys.exit(2)
    return resolved


# ---------------------------------------------------------------------------
# Artifact resolution (D-08 deep check)
# ---------------------------------------------------------------------------


def _resolve_artifact(artifact_link: str) -> list[str]:
    """Deep-resolve an artifact_link; return a list of issue descriptions.

    Resolution rules per RESEARCH.md §Pattern 3:
      - CLI whitelist entry (KNOWN_CLI_GATES) → membership check
      - catalog-row anchor (path#ROW-ID) → file exists + row ID in file text
      - rubric anchor (path#anchor) → file exists + heading found in file
      - plain file path → file exists

    Returns empty list if the artifact resolves correctly.
    Empty artifact_link string is not dispatched here (callers check tier first).
    """
    if not artifact_link:
        return []

    # CLI whitelist check (Pitfall 6: VAL-01/VAL-02 have no script file)
    if artifact_link in KNOWN_CLI_GATES:
        return []

    # Anchor-based resolution (catalog rows and rubric sections)
    if "#" in artifact_link:
        file_part, anchor = artifact_link.split("#", 1)
        file_path = REPO_ROOT / file_part
        if not file_path.exists():
            return [f"artifact file not found: {file_part!r}"]
        content = file_path.read_text(encoding="utf-8")

        if file_part.endswith(".py"):
            # For .py files: require the anchor to match a real top-level symbol.
            # Arm 1: def/class (functions incl. `async def`, classes; indented
            #        methods also matched).
            # Arm 2: module constant / annotated assignment at column 0.
            # This prevents a comment-only substring from falsely resolving.
            #
            # Known, accepted limitation (WR-02): this is a line-anchored regex,
            # NOT an AST walk (D-03 — AST was intentionally rejected as
            # over-engineered for a CI gate whose only live anchor is
            # `#self_test_boundary`). A symbol-like line sitting at column 0
            # inside a triple-quoted string or docstring can therefore
            # false-positive. The self-test proves comment-only rejection +
            # substring non-vacuity; it does not claim string-literal rejection.
            escaped = re.escape(anchor)
            # Arm 1 allows an optional `async ` prefix so `async def <anchor>`
            # resolves (WR-03 — a bare `(def|class)` alternation misses it
            # because the line begins with `async`, not `def`).
            _def_class_pat = re.compile(
                r"^\s*(?:async\s+def|def|class)\s+" + escaped + r"\b", re.MULTILINE
            )
            _const_pat = re.compile(
                r"^" + escaped + r"\s*[=:]", re.MULTILINE
            )
            if not (_def_class_pat.search(content) or _const_pat.search(content)):
                return [
                    f"anchor {anchor!r} is not a def/class/module-level symbol in {file_part!r}"
                ]
            return []

        # Non-.py files: catalog-row form (row ID like B-P12, S-P01, etc.) and
        # rubric anchors (heading slugs). Use plain substring membership
        # (RESEARCH.md §Parenthetical gotcha: avoid pipe-table split over content
        # with | alternation characters).
        if anchor not in content:
            return [
                f"anchor {anchor!r} not found in {file_part!r}"
            ]
        return []

    # Plain file path resolution
    file_path = REPO_ROOT / artifact_link
    if not file_path.exists():
        return [f"artifact file not found: {artifact_link!r}"]
    return []


# ---------------------------------------------------------------------------
# Consistency gate
# ---------------------------------------------------------------------------


def check_consistency(rows: list[MatrixRow]) -> list[str]:
    """Validate each row; return list of issue descriptions (empty == consistent).

    Per-row checks:
      - capability must be in VALID_CAPABILITIES (TRACE-01)
      - coverage_tier must be in VALID_TIERS (TRACE-03)
      - for reproducible AND scheduled rows: artifact_link must resolve via
        _resolve_artifact (WR-02/D-02); a dangling scheduled artifact FAILS check
        the same as a dangling reproducible artifact
      - audit-only and gap rows with no artifact link are valid states (D-06)
    """
    issues: list[str] = []
    for row in rows:
        if row.capability not in VALID_CAPABILITIES:
            issues.append(
                f"{row.key}: invalid capability {row.capability!r} "
                f"(must be one of {sorted(VALID_CAPABILITIES)!r})"
            )
        if row.coverage_tier not in VALID_TIERS:
            issues.append(
                f"{row.key}: invalid coverage_tier {row.coverage_tier!r} "
                f"(must be one of {sorted(VALID_TIERS)!r})"
            )
        if row.coverage_tier in ("reproducible", "scheduled"):
            link_issues = _resolve_artifact(row.artifact_link)
            for issue in link_issues:
                issues.append(f"{row.key}: {issue}")
    return issues


# ---------------------------------------------------------------------------
# Emitter: dual output from one row list (D-12 anti-drift)
# ---------------------------------------------------------------------------

# Severity matrix per D-14: coverage-tier × capability-undermined
# gap+Test-Network=CRITICAL, gap+Methodology=HIGH,
# audit-only+Test-Network=HIGH, audit-only+Methodology=MEDIUM
_SEVERITY_LABEL: dict[tuple[str, str], str] = {
    ("gap", "Test-Network"): "CRITICAL",
    ("gap", "Methodology"): "HIGH",
    ("audit-only", "Test-Network"): "HIGH",
    ("audit-only", "Methodology"): "MEDIUM",
}

# Human-curated per-item severity overrides for the 7 active-tail gap rows.
# Approved at Task 3 checkpoint (82-02 Plan, 2026-06-14); rationale in
# 82-RESEARCH.md §Gap Prioritization Model lines 719-724.
# These override the pure D-14 2×2 formula for the named bare_ids only;
# all other rows continue to use the _SEVERITY_LABEL 2×2 map.
_ACTIVE_TAIL_SEVERITY: dict[str, str] = {
    "RR-80-01": "CRITICAL",   # negative-control regression in step0-baseline
    # GEN-01 removed — now "reproducible" (committed live re-baseline; flip Phase 93 on v6.3 Phase 92, now tracks v6.4 Phase 95)
    # GEN-02 removed — now "reproducible" (runbook + wrapper script, Phase 89)
    "RR-79-01": "HIGH",       # live S-P routing unresolved
    # RR-114-01 supersedes RR-108-01 (Phase 114 v7.6 carry-forward, S-P02 inversion CARRIED 1/5)
    # Full chain: RR-79-02 -> RR-92-01 -> RR-95-01 -> RR-108-01 -> RR-114-01
    "RR-114-01": "HIGH",      # live S-P routing unresolved (carried v7.6)
    # RR-108-02 supersedes RR-95-02 (Phase 108 v7.4 carry-forward, S-P05 trade-off CARRIED 2/5)
    # Full chain: RR-79-03 -> RR-92-02 -> RR-95-02 -> RR-108-02 CLOSED
    # CLOSED at 4/5 ≥ min-pass at Phase 114 v7.6 re-baseline (ID retained, sentinel present)
    "RR-108-02": "HIGH",      # CLOSED at 4/5 v7.6 (ID retained as regression guard)
    "RR-77-08": "MEDIUM",     # ceiling warning, non-blocking
}

# Sort rank keyed on final label (CRITICAL first → MEDIUM last).
# Using label→rank keeps sort correct even when override changes the label.
_SEVERITY_RANK: dict[str, int] = {
    "CRITICAL": 0,
    "HIGH":     1,
    "MEDIUM":   2,
    "UNKNOWN":  99,
}


def _gap_severity(row: MatrixRow) -> str:
    """Return the effective severity label for an audit-only or gap row.

    Checks the human-curated _ACTIVE_TAIL_SEVERITY override FIRST (approved
    at Task 3 checkpoint, 82-02, for the 7 active-tail rows). Falls back to
    the D-14 2×2 _SEVERITY_LABEL map for all other rows.

    CRITICAL: gap + Test-Network (or override). Verification system unverified.
    HIGH:     gap + Methodology OR audit-only + Test-Network (or override).
    MEDIUM:   audit-only + Methodology (or override).
    """
    if row.bare_id in _ACTIVE_TAIL_SEVERITY:
        return _ACTIVE_TAIL_SEVERITY[row.bare_id]
    return _SEVERITY_LABEL.get((row.coverage_tier, row.capability), "UNKNOWN")


def _render_gap_findings(uncovered: list[MatrixRow]) -> list[str]:
    """Render the severity-ordered Gap Findings + Candidate Work List sections.

    Implements GAP-01 (named gap findings) + GAP-02 (prioritized carry-forward).
    Uncovered rows = audit-only + gap rows, sorted CRITICAL -> HIGH -> MEDIUM.
    Sort is by final label rank (_SEVERITY_RANK) so override labels sort correctly.
    """
    # Sort by final severity label rank (ascending rank = descending severity)
    sorted_rows = sorted(
        uncovered,
        key=lambda r: _SEVERITY_RANK.get(_gap_severity(r), 99),
    )
    lines: list[str] = []
    lines.append("## Gap Findings (GAP-01)")
    lines.append("")
    lines.append(
        "> **D-15 honesty note:** A non-zero audit-only+gap count is the "
        "expected success state — an honest 'N requirements are uncovered' "
        "finding is the goal, not a zero-gap matrix."
    )
    lines.append("")
    current_sev = ""
    for r in sorted_rows:
        sev = _gap_severity(r)
        if sev != current_sev:
            lines.append(f"### {sev}")
            lines.append("")
            current_sev = sev
        lines.append(
            f"- **{r.bare_id}** ({r.key}) [{r.coverage_tier}] "
            f"[{r.capability}]: {r.gap_rationale}"
        )
    lines.append("")
    lines.append("## Future-Milestone Candidate Work List (GAP-02)")
    lines.append("")
    lines.append(
        "The following items are carried forward as candidate work for a "
        "future milestone. No new confirming tests are written this phase."
    )
    lines.append("")
    for r in sorted_rows:
        sev = _gap_severity(r)
        lines.append(
            f"- [{sev}] **{r.bare_id}** ({r.key}): Add a confirming "
            f"{r.capability} gate/test. Rationale: {r.gap_rationale[:80]}"
            f"{'...' if len(r.gap_rationale) > 80 else ''}"
        )
    lines.append("")
    return lines


def render_matrix_markdown(rows: list[MatrixRow]) -> str:
    """Render the matrix as a Markdown string (list[str] → join pattern).

    Coverage Distribution folds scheduled rows into the reproducible bucket
    (D-01/WR-01): the reproducible bullet shows len(reproducible)+len(scheduled)
    with an `(incl. N scheduled)` annotation when N > 0. No standalone scheduled
    bullet is emitted. uncovered = audit_only + gap only (scheduled is not
    uncovered and must not enter _render_gap_findings).
    """
    reproducible = [r for r in rows if r.coverage_tier == "reproducible"]
    audit_only = [r for r in rows if r.coverage_tier == "audit-only"]
    gap = [r for r in rows if r.coverage_tier == "gap"]
    scheduled = [r for r in rows if r.coverage_tier == "scheduled"]
    uncovered = audit_only + gap

    lines: list[str] = []
    lines.append("<!-- GENERATED — DO NOT EDIT -->")
    lines.append("<!-- Source: scripts/check-traceability.py build_matrix_rows() -->")
    lines.append(
        "<!-- Regenerate: python3 scripts/check-traceability.py emit"
        " --md-output docs/requirements-matrix.md"
        " --json-output docs/data/matrix.json -->"
    )
    lines.append("")
    lines.append("# Requirements Traceability Matrix")
    lines.append("")
    lines.append(
        "> Generated by: "
        "`python3 scripts/check-traceability.py emit"
        " --md-output docs/requirements-matrix.md ...`"
    )
    lines.append("")
    lines.append("## Coverage Distribution")
    _folded_reproducible = len(reproducible) + len(scheduled)
    if len(scheduled) > 0:
        lines.append(
            f"- reproducible: {_folded_reproducible} (incl. {len(scheduled)} scheduled)"
        )
    else:
        lines.append(f"- reproducible: {_folded_reproducible}")
    lines.append(f"- audit-only: {len(audit_only)}")
    lines.append(f"- gap: {len(gap)}")
    lines.append(f"- total: {len(rows)}")
    lines.append("")
    lines.append("## Matrix Table")
    lines.append(
        "| Key | Bare ID | Capability | Deliverable | Tier | "
        "Artifact | Gap Rationale |"
    )
    lines.append(
        "|-----|---------|------------|-------------|------|----------|---------------|"
    )
    for r in rows:
        lines.append(
            f"| {r.key} | {r.bare_id} | {r.capability} | "
            f"{r.deliverable_path} | {r.coverage_tier} | "
            f"{r.artifact_link} | {r.gap_rationale} |"
        )
    lines.append("")
    if uncovered:
        lines.extend(_render_gap_findings(uncovered))
    return "\n".join(lines)


def emit_matrix(
    rows: list[MatrixRow],
    md_path: Path,
    json_path: Path,
) -> None:
    """Write MATRIX.md + matrix.json from one row list (D-12 single repr).

    Both paths must pass _resolve_confined_output() first.
    Writes JSON sidecar first, then Markdown.
    """
    md_resolved = _resolve_confined_output(md_path)
    json_resolved = _resolve_confined_output(json_path)

    md_resolved.parent.mkdir(parents=True, exist_ok=True)
    json_resolved.parent.mkdir(parents=True, exist_ok=True)

    json_resolved.write_text(
        json.dumps([asdict(r) for r in rows], indent=2),
        encoding="utf-8",
    )
    md_resolved.write_text(
        render_matrix_markdown(rows),
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# load_rows: JSON sidecar → list[MatrixRow]
# ---------------------------------------------------------------------------


def load_rows(json_path: Path) -> list[MatrixRow]:
    """Load matrix.json → list[MatrixRow] via json.loads + dataclass constructor.

    The constructor catches missing fields (Don't-Hand-Roll: per RESEARCH.md).
    """
    raw = json.loads(json_path.read_text(encoding="utf-8"))
    return [MatrixRow(**item) for item in raw]


# ---------------------------------------------------------------------------
# Self-test fixtures
# ---------------------------------------------------------------------------


def _self_test_valid_rows_fixtures(wrong_results: list[str]) -> None:
    """Fixtures 1, 5, 6: valid rows that must pass check_consistency."""
    # Fixture (1): valid reproducible row with a real repo file
    row1 = MatrixRow(
        key="v5.0/STEP0-F1",
        bare_id="STEP0-F1",
        milestone="v5.0",
        capability="Test-Network",
        deliverable_path="scripts/check-step0-emulator.py",
        coverage_tier="reproducible",
        artifact_link="scripts/check-step0-emulator.py",
        gap_rationale="",
    )
    issues1 = check_consistency([row1])
    if issues1:
        print(f"check-traceability --self-test: fixture(1) FAIL — {issues1!r}")
        wrong_results.append("fixture(1) valid reproducible row flagged incorrectly")
    else:
        print("check-traceability --self-test: fixture(1) valid reproducible row PASS")

    # Fixture (5): audit-only row with no artifact link — valid state (D-06)
    row5 = MatrixRow(
        key="v3.1/ROUTE-02",
        bare_id="ROUTE-02",
        milestone="v3.1",
        capability="Test-Network",
        deliverable_path="scripts/check-routing.py",
        coverage_tier="audit-only",
        artifact_link="",
        gap_rationale="Validated by v3.1 milestone audit; no re-runnable gate",
    )
    issues5 = check_consistency([row5])
    if issues5:
        print(f"check-traceability --self-test: fixture(5) FAIL — {issues5!r}")
        wrong_results.append(
            "fixture(5) audit-only row with no artifact flagged (should be valid)"
        )
    else:
        print("check-traceability --self-test: fixture(5) audit-only no-artifact PASS")

    # Fixture (6): gap row with rationale, no artifact link — valid state (D-06)
    # Generic gap-row STRUCTURAL test; coverage_tier="gap" is still a valid tier.
    # NOT tied to the live GEN-01 state (GEN-01 is now "scheduled" after Phase 88).
    row6 = MatrixRow(
        key="v5.3/GEN-01",
        bare_id="GEN-01",
        milestone="v5.3",
        capability="Test-Network",
        deliverable_path="active-tail",
        coverage_tier="gap",
        artifact_link="",
        gap_rationale="Full Step 0 classifier rearchitecture; perpetually deferred",
    )
    issues6 = check_consistency([row6])
    if issues6:
        print(f"check-traceability --self-test: fixture(6) FAIL — {issues6!r}")
        wrong_results.append(
            "fixture(6) gap row with rationale flagged (should be valid)"
        )
    else:
        print("check-traceability --self-test: fixture(6) gap row with rationale PASS")

    # Fixture (9): scheduled row with resolvable artifact link — valid state (D-02/Phase 88)
    # Proves that coverage_tier="scheduled" is accepted by check_consistency() AND
    # that deep-resolve passes for a scheduled row with a real artifact (WR-02/Phase 90).
    # check_consistency() now deep-resolves artifact links for both "reproducible" AND
    # "scheduled" rows. Fixture passes because docs/gen-01-rearch-milestone.md exists.
    # The GEN-01-SCHEDULED sentinel (below) also verifies the file exists.
    row9 = MatrixRow(
        key="v5.3/GEN-01",
        bare_id="GEN-01",
        milestone="v5.3",
        capability="Test-Network",
        deliverable_path="active-tail",
        coverage_tier="scheduled",
        artifact_link="docs/gen-01-rearch-milestone.md",
        gap_rationale="Committed future milestone GEN-01-REARCH",
    )
    issues9 = check_consistency([row9])
    if issues9:
        print(f"check-traceability --self-test: fixture(9) FAIL — {issues9!r}")
        wrong_results.append("fixture(9) scheduled row flagged (should be valid)")
    else:
        print("check-traceability --self-test: fixture(9) scheduled row with artifact PASS")

    # ---------------------------------------------------------------------------
    # DISTRIBUTION-FOLD fixture (10) — WR-01 renderer fold lock (TRACE-03)
    # Calls render_matrix_markdown on a tiny SYNTHETIC row set (hardcoded, NOT
    # live build_matrix_rows) so the fixture can never go vacuous if live counts
    # shift. Asserts the three WR-01 regression conditions:
    #   (a) Sum guard: Coverage Distribution bullets sum to len(rows).
    #   (b) Annotation guard: "(incl. 1 scheduled)" appears in the rendered output.
    #   (c) Positive counter-check (non-vacuous): folded reproducible count
    #       strictly > bare reproducible count (mirrors GEN-01-SCHEDULED
    #       _gen01_was_gap and RR-77-08 composer_hits == CEILING-1 idioms).
    # Honesty-not-score: asserts renderer math, not any live pass-rate.
    # Any revert of the scheduled-fold in render_matrix_markdown fails this fixture.
    # ---------------------------------------------------------------------------
    _fold_repro1 = MatrixRow(
        key="fixture/FOLD-REPRO-01", bare_id="FOLD-REPRO-01", milestone="fixture",
        capability="Test-Network", deliverable_path="active-tail",
        coverage_tier="reproducible", artifact_link="", gap_rationale="",
    )
    _fold_repro2 = MatrixRow(
        key="fixture/FOLD-REPRO-02", bare_id="FOLD-REPRO-02", milestone="fixture",
        capability="Test-Network", deliverable_path="active-tail",
        coverage_tier="reproducible", artifact_link="", gap_rationale="",
    )
    _fold_sched1 = MatrixRow(
        key="fixture/FOLD-SCHED-01", bare_id="FOLD-SCHED-01", milestone="fixture",
        capability="Test-Network", deliverable_path="active-tail",
        coverage_tier="scheduled", artifact_link="",
        gap_rationale="Synthetic scheduled row for DISTRIBUTION-FOLD fixture",
    )
    _fold_rows = [_fold_repro1, _fold_repro2, _fold_sched1]  # 2 repro + 1 scheduled
    _fold_bare_reproducible = 2   # bare count (before fold)
    _fold_rendered = render_matrix_markdown(_fold_rows)
    _fold_dist = _fold_rendered.split("## Coverage Distribution")[1].split("## Matrix Table")[0]

    # (a) Sum guard: the total bullet must equal len(rows); reproducible+audit+gap
    # must equal len(rows) (the scheduled rows are folded into reproducible).
    # Parse the total bullet and the three tier bullets separately.
    import re as _re
    _fold_total_match = _re.search(r"^- total: (\d+)", _fold_dist, _re.MULTILINE)
    _fold_total_val = int(_fold_total_match.group(1)) if _fold_total_match else -1
    _fold_sum_ok = _fold_total_val == len(_fold_rows)
    if not _fold_sum_ok:
        print(
            f"check-traceability --self-test: fixture(10) DISTRIBUTION-FOLD FAIL "
            f"— total bullet is {_fold_total_val}, expected {len(_fold_rows)} "
            f"(scheduled row dropped, sum is wrong)"
        )
        wrong_results.append(
            "DISTRIBUTION-FOLD: total bullet does not equal len(rows) (scheduled row dropped)"
        )
    else:
        print(
            "check-traceability --self-test: fixture(10) DISTRIBUTION-FOLD sum guard PASS "
            f"(total={_fold_total_val} == {len(_fold_rows)})"
        )

    # (b) Annotation guard: "(incl. 1 scheduled)" must appear in the rendered output
    _fold_annotation_ok = "(incl. 1 scheduled)" in _fold_dist
    if not _fold_annotation_ok:
        print(
            "check-traceability --self-test: fixture(10) DISTRIBUTION-FOLD FAIL "
            "— annotation '(incl. 1 scheduled)' not found in Coverage Distribution"
        )
        wrong_results.append("DISTRIBUTION-FOLD: (incl. 1 scheduled) annotation missing")
    else:
        print(
            "check-traceability --self-test: fixture(10) DISTRIBUTION-FOLD annotation PASS"
        )

    # (c) Positive counter-check: folded reproducible count (3) > bare count (2)
    # Extract the reproducible bullet value from the rendered distribution
    _fold_repro_match = _re.search(r"^- reproducible: (\d+)", _fold_dist, _re.MULTILINE)
    _fold_folded_count = int(_fold_repro_match.group(1)) if _fold_repro_match else -1
    _fold_noop = _fold_folded_count <= _fold_bare_reproducible
    if _fold_noop or _fold_folded_count < 0:
        print(
            f"check-traceability --self-test: fixture(10) DISTRIBUTION-FOLD FAIL "
            f"— folded reproducible count ({_fold_folded_count}) not strictly > "
            f"bare reproducible count ({_fold_bare_reproducible}); fold is a no-op or missing"
        )
        wrong_results.append(
            "DISTRIBUTION-FOLD: folded count not strictly > bare reproducible count"
        )
    else:
        print(
            f"check-traceability --self-test: fixture(10) DISTRIBUTION-FOLD positive "
            f"counter-check PASS ({_fold_folded_count} > {_fold_bare_reproducible})"
        )

    # ---------------------------------------------------------------------------
    # GEN-01-REPRODUCIBLE named sentinel (D-09 / Phase 93)
    # Repurposed from GEN-01-SCHEDULED (Phase 88) — GEN-01 is now 'reproducible'
    # (Phase 93 flip, D-08) because the Step 0 classifier capability is reproducibly
    # measured by a committed live re-baseline. The flip was earned in Phase 93 on
    # tests/step0-baseline-v6.3.md (Phase 92); the artifact_link now tracks the current
    # authoritative re-baseline tests/step0-baseline-v7.13.md (Phase 137, residual-delta).
    # Artifact bump history: v7.6 (Phase 114) → v7.8 (Phase 119) → v7.11 (Phase 131 RECON-03, D-05)
    # → v7.13 (Phase 138 Plan 03, D-05). tests/step0-baseline-v7.8.md remains the canonical
    # full 8-technique baseline; v7.13 is a 3-row residual-delta re-measure.
    # The flip is earned by the committed baseline, not a passing score
    # (Phase 129 v7.11: BATTERY: FAIL P 4/8 — reproducible = measured, not passing, D-01).
    # Asserts:
    #   (a) GEN-01's tier is "reproducible" (not "scheduled", not "gap")
    #   (b) GEN-01's artifact_link is the committed v7.13 baseline (deep-resolved)
    #   (c) Exactly-one GEN-01 row drift guard
    #   (d) Not-scheduled counter-check (transition non-vacuous)
    # Mirrors the Phase 84/85 RR-80-01 idiom: hardcoded named assertion +
    # positive counter-check + drift guard. No live claude session required.
    # No gitignored-file dependency (.planning/ROADMAP.md removed — ABSENT in CI).
    # Honesty-not-score (D-01): asserts the documented reproducible state, not a
    # live pass-rate. Any future revert of the tier, deletion of the GEN-01 row,
    # or removal of the v7.13 baseline file fails CI.
    # ---------------------------------------------------------------------------

    # (1) Live-sourced tier read — call _rows_active_tail() directly (Pitfall 4:
    # do NOT hardcode a MatrixRow literal; the function is the source of truth).
    _gen01_rows = [r for r in _rows_active_tail() if r.bare_id == "GEN-01"]
    _gen01_count = len(_gen01_rows)
    _gen01_tier = _gen01_rows[0].coverage_tier if _gen01_rows else "MISSING"
    _gen01_artifact = _gen01_rows[0].artifact_link if _gen01_rows else ""

    # (c) Drift guard: GEN-01 must exist exactly once (not deleted, not duplicated).
    if _gen01_count != 1:
        print(
            f"  GEN-01-REPRODUCIBLE FAIL: expected exactly 1 GEN-01 row in "
            f"_rows_active_tail(), got {_gen01_count} — drift guard failed."
        )
        wrong_results.append("GEN-01-REPRODUCIBLE: row count drift")

    # (d) Not-scheduled counter-check: proves the scheduled→reproducible transition
    # is non-vacuous. _gen01_was_scheduled would have been True pre-Phase 93; asserting
    # NOT scheduled is meaningful (mirrors the old _gen01_was_gap idiom from Phase 88).
    _gen01_was_scheduled = _gen01_tier == "scheduled"
    _gen01_is_reproducible = _gen01_tier == "reproducible"

    if _gen01_is_reproducible and not _gen01_was_scheduled:
        print(
            f"  GEN-01-REPRODUCIBLE PASS: GEN-01 tier={_gen01_tier!r} "
            f"(not 'scheduled', not 'gap'); artifact_link={_gen01_artifact!r}"
        )
    else:
        print(
            f"  GEN-01-REPRODUCIBLE FAIL: GEN-01 tier={_gen01_tier!r} "
            f"(expected 'reproducible', not 'scheduled' or 'gap'). "
            f"Phase 93 flip not applied or tier reverted. "
            f"See D-08 in 93-02-PLAN.md."
        )
        wrong_results.append("GEN-01-REPRODUCIBLE: tier not 'reproducible'")

    # (b) Artifact deep-resolve (D-09): GEN-01's artifact_link must be the committed
    # v7.13 baseline (Phase 137 residual-delta — the latest authoritative re-baseline).
    # Deep-resolve via _resolve_artifact (git-tracked, present in CI).
    # Bump history: v7.6 (Phase 114) → v7.8 (Phase 119) → v7.11 (Phase 131 RECON-03, Plan 03, D-05)
    # → v7.13 (Phase 138 Plan 03, D-05). tests/step0-baseline-v7.8.md remains canonical full baseline.
    _gen01_expected_artifact = "tests/step0-baseline-v7.13.md"
    if _gen01_artifact != _gen01_expected_artifact:
        print(
            f"  GEN-01-REPRODUCIBLE FAIL: artifact_link={_gen01_artifact!r} "
            f"(expected {_gen01_expected_artifact!r})."
        )
        wrong_results.append("GEN-01-REPRODUCIBLE: artifact_link not v7.13 baseline")
    else:
        _gen01_resolve_issues = _resolve_artifact(_gen01_artifact)
        # Belt-and-suspenders: explicit path existence check
        _gen01_baseline_path = REPO_ROOT / "tests" / "step0-baseline-v7.13.md"
        if _gen01_resolve_issues or not _gen01_baseline_path.exists():
            print(
                f"  GEN-01-REPRODUCIBLE FAIL: artifact deep-resolve failed for "
                f"{_gen01_artifact!r}: {_gen01_resolve_issues}; "
                f"file exists={_gen01_baseline_path.exists()}"
            )
            wrong_results.append("GEN-01-REPRODUCIBLE: v7.13 baseline not resolvable")
        else:
            print(
                f"  GEN-01-REPRODUCIBLE PASS: artifact_link={_gen01_artifact!r} "
                f"deep-resolves OK (tests/step0-baseline-v7.13.md exists, git-tracked)."
            )

    # ---------------------------------------------------------------------------
    # GEN-02-RUNBOOK named sentinel (D-03 / Phase 89)
    # Asserts (a) GEN-02's tier is "reproducible" (not "gap") in _rows_active_tail()
    # and (b) dual artifact-existence: docs/live-monitoring-runbook.md exists AND
    # scripts/run-live-monitoring.sh exists.
    # Mirrors the Phase 88 GEN-01-SCHEDULED idiom: live _rows_active_tail() read +
    # positive counter-check + drift guard + existence checks. No live claude session.
    # Honesty-not-score (D-06): asserts the documented reproducible confirming state,
    # not a live pass-rate. Any future revert of the tier, deletion of the GEN-02 row,
    # or removal of the runbook/wrapper fails CI.
    # ---------------------------------------------------------------------------

    # (1) Live-sourced tier read — call _rows_active_tail() directly (Pitfall 1:
    # do NOT hardcode a MatrixRow literal; the function is the source of truth).
    _gen02_rows = [r for r in _rows_active_tail() if r.bare_id == "GEN-02"]
    _gen02_count = len(_gen02_rows)
    _gen02_tier = _gen02_rows[0].coverage_tier if _gen02_rows else "MISSING"
    _gen02_artifact = _gen02_rows[0].artifact_link if _gen02_rows else ""

    # (3) Drift guard: GEN-02 must exist exactly once (not deleted, not duplicated).
    if _gen02_count != 1:
        print(
            f"  GEN-02-RUNBOOK FAIL: expected exactly 1 GEN-02 row in "
            f"_rows_active_tail(), got {_gen02_count} — drift guard failed."
        )
        wrong_results.append("GEN-02-RUNBOOK: row count drift")

    # (2) Positive counter-check: _gen02_was_gap proves the transition is non-vacuous.
    # _gen02_was_gap would have been True pre-Phase 89; asserting NOT gap is meaningful.
    _gen02_was_gap = _gen02_tier == "gap"
    _gen02_is_reproducible = _gen02_tier == "reproducible"

    if _gen02_is_reproducible and not _gen02_was_gap:
        print(
            f"  GEN-02-RUNBOOK PASS: GEN-02 tier={_gen02_tier!r} (not 'gap'); "
            f"artifact_link={_gen02_artifact!r}"
        )
    else:
        print(
            f"  GEN-02-RUNBOOK FAIL: GEN-02 tier={_gen02_tier!r} "
            f"(expected 'reproducible', not 'gap'). "
            f"Runbook + wrapper not established or tier reverted. "
            f"See docs/live-monitoring-runbook.md."
        )
        wrong_results.append("GEN-02-RUNBOOK: tier not 'reproducible'")

    # (b) Dual artifact-existence check (D-03): runbook AND wrapper must both exist.
    _gen02_runbook_path = REPO_ROOT / "docs" / "live-monitoring-runbook.md"
    if _gen02_runbook_path.exists():
        print("  GEN-02-RUNBOOK PASS: docs/live-monitoring-runbook.md exists.")
    else:
        print(
            "  GEN-02-RUNBOOK FAIL: docs/live-monitoring-runbook.md does not exist "
            "— D-03 dual-artifact check (part 1) not satisfied."
        )
        wrong_results.append("GEN-02-RUNBOOK: docs/live-monitoring-runbook.md missing")

    _gen02_wrapper_path = REPO_ROOT / "scripts" / "run-live-monitoring.sh"
    if _gen02_wrapper_path.exists():
        print("  GEN-02-RUNBOOK PASS: scripts/run-live-monitoring.sh exists.")
    else:
        print(
            "  GEN-02-RUNBOOK FAIL: scripts/run-live-monitoring.sh does not exist "
            "— D-03 dual-artifact check (part 2) not satisfied."
        )
        wrong_results.append("GEN-02-RUNBOOK: scripts/run-live-monitoring.sh missing")


def _self_test_dangling_fixtures(wrong_results: list[str]) -> None:
    """Fixtures 2, 3, 4: dangling references that must flag non-zero."""
    # Fixture (2): reproducible row with dangling file path
    row2 = MatrixRow(
        key="test/DANGLE-01",
        bare_id="DANGLE-01",
        milestone="test",
        capability="Test-Network",
        deliverable_path="scripts/check-routing-battery.py",
        coverage_tier="reproducible",
        artifact_link="scripts/nonexistent-check-99.py",
        gap_rationale="",
    )
    issues2 = check_consistency([row2])
    if not issues2:
        print("check-traceability --self-test: fixture(2) FAIL — dangling path not detected")
        wrong_results.append(
            "fixture(2) dangling file path not flagged (nonexistent-check-99.py)"
        )
    else:
        print("check-traceability --self-test: fixture(2) dangling file path detected PASS")

    # Fixture (3): reproducible row with catalog row not in catalog
    row3 = MatrixRow(
        key="test/DANGLE-02",
        bare_id="DANGLE-02",
        milestone="test",
        capability="Test-Network",
        deliverable_path="scripts/check-routing-battery.py",
        coverage_tier="reproducible",
        artifact_link="tests/routing-battery-catalog.md#B-NONEXISTENT",
        gap_rationale="",
    )
    issues3 = check_consistency([row3])
    if not issues3:
        print("check-traceability --self-test: fixture(3) FAIL — dangling catalog row not detected")
        wrong_results.append(
            "fixture(3) dangling catalog row not flagged (B-NONEXISTENT)"
        )
    else:
        print(
            "check-traceability --self-test: fixture(3) dangling catalog row detected PASS"
        )

    # Fixture (4): reproducible row with missing rubric anchor
    row4 = MatrixRow(
        key="test/DANGLE-03",
        bare_id="DANGLE-03",
        milestone="test",
        capability="Methodology",
        deliverable_path="shared/spine/references/validation-rubric.md",
        coverage_tier="reproducible",
        artifact_link=(
            "shared/spine/references/validation-rubric.md"
            "#criterion-99-nonexistent"
        ),
        gap_rationale="",
    )
    issues4 = check_consistency([row4])
    if not issues4:
        print("check-traceability --self-test: fixture(4) FAIL — missing rubric anchor not detected")
        wrong_results.append(
            "fixture(4) missing rubric anchor not flagged (criterion-99-nonexistent)"
        )
    else:
        print(
            "check-traceability --self-test: fixture(4) missing rubric anchor detected PASS"
        )


def _self_test_schema_fixtures(wrong_results: list[str]) -> None:
    """Fixtures 7, 8: schema violations (missing capability or coverage_tier)."""
    # Fixture (7): row with empty capability
    row7 = MatrixRow(
        key="test/SCHEMA-01",
        bare_id="SCHEMA-01",
        milestone="test",
        capability="",
        deliverable_path="scripts/check-routing-battery.py",
        coverage_tier="audit-only",
        artifact_link="",
        gap_rationale="no capability assigned",
    )
    issues7 = check_consistency([row7])
    if not issues7:
        print("check-traceability --self-test: fixture(7) FAIL — missing capability not detected")
        wrong_results.append("fixture(7) empty capability not flagged")
    else:
        print("check-traceability --self-test: fixture(7) missing capability detected PASS")

    # Fixture (8): row with empty coverage_tier
    row8 = MatrixRow(
        key="test/SCHEMA-02",
        bare_id="SCHEMA-02",
        milestone="test",
        capability="Test-Network",
        deliverable_path="scripts/check-routing-battery.py",
        coverage_tier="",
        artifact_link="",
        gap_rationale="no tier assigned",
    )
    issues8 = check_consistency([row8])
    if not issues8:
        print("check-traceability --self-test: fixture(8) FAIL — missing coverage_tier not detected")
        wrong_results.append("fixture(8) empty coverage_tier not flagged")
    else:
        print("check-traceability --self-test: fixture(8) missing coverage_tier detected PASS")


def _self_test_pyanchor_resolver(wrong_results: list[str]) -> None:
    """pyanchor teeth: 3 positive controls + 1 comment-only negative control + non-vacuity check.

    Proves the extension-gated .py#anchor resolver is non-vacuous:
      (a) def-arm positive: scripts/_battery_core.py#self_test_boundary resolves (real def).
      (b) constant-arm positive: scripts/_battery_core.py#MIN_HEADER_HITS resolves (module const).
      (c) comment-only negative control: a .py file whose content mentions a token ONLY
          in a comment is rejected by the stricter resolver; the substring non-vacuity
          counter-check proves the OLD loose resolver would have falsely passed it
          (the name IS a substring).
      (d) async-def positive control (WR-03): `async def <anchor>` must resolve — guards
          the optional `async ` prefix in the def-arm against regression.

    Scope note (WR-02): these controls prove comment-only rejection + substring
    non-vacuity + async-def acceptance. They deliberately do NOT assert
    string-literal rejection, because the line-anchored regex (D-03, not AST)
    genuinely cannot reject a symbol-like line inside a docstring/string — that is
    a known, accepted limitation, not a defect this self-test claims to cover.
    """
    # (a) Positive control — def-arm: live OCH-03 anchor must still resolve.
    issues_a = _resolve_artifact("scripts/_battery_core.py#self_test_boundary")
    if issues_a:
        print(
            f"  PYANCHOR FAIL (a): def-arm regressed — "
            f"self_test_boundary not resolved: {issues_a}"
        )
        wrong_results.append(
            "PYANCHOR (a): scripts/_battery_core.py#self_test_boundary def-arm regressed"
        )
    else:
        print(
            "  PYANCHOR PASS (a): scripts/_battery_core.py#self_test_boundary def-arm resolves OK"
        )

    # (b) Positive control — constant-arm: MIN_HEADER_HITS is a module-level constant.
    issues_b = _resolve_artifact("scripts/_battery_core.py#MIN_HEADER_HITS")
    if issues_b:
        print(
            f"  PYANCHOR FAIL (b): constant-arm broken — "
            f"MIN_HEADER_HITS not resolved: {issues_b}"
        )
        wrong_results.append(
            "PYANCHOR (b): scripts/_battery_core.py#MIN_HEADER_HITS constant-arm broken"
        )
    else:
        print(
            "  PYANCHOR PASS (b): scripts/_battery_core.py#MIN_HEADER_HITS constant-arm resolves OK"
        )

    # (c) Negative control + substring non-vacuity counter-check.
    # Write a .py file with the token ONLY in a comment — no def/class/module-const.
    with tempfile.TemporaryDirectory() as _tmpdir:
        _fake_py = Path(_tmpdir) / "fake.py"
        _fake_py.write_text(
            "# comment_only_symbol mentioned here\nx = 1\n", encoding="utf-8"
        )
        _fake_content = _fake_py.read_text(encoding="utf-8")

        # Counter-check: the name IS a plain substring — proves the old loose resolver
        # would have falsely passed it, so the fix is non-vacuous.
        if "comment_only_symbol" not in _fake_content:
            print(
                "  PYANCHOR FAIL (c-counter): fixture not a substring — non-vacuity check invalid"
            )
            wrong_results.append(
                "PYANCHOR (c-counter): comment_only_symbol not a substring of fake.py"
            )
        else:
            print(
                "  PYANCHOR PASS (c-counter): comment_only_symbol IS a substring "
                "(old loose resolver would have falsely passed — fix is non-vacuous)"
            )

        # Negative control: the stricter resolver must REJECT this comment-only anchor.
        # The "#" form drives anchor resolution; pathlib absolute-path joining keeps the
        # absolute path (REPO_ROOT / absolute_path == absolute_path).
        issues_c = _resolve_artifact(f"{_fake_py}#comment_only_symbol")
        if not issues_c:
            print(
                "  PYANCHOR FAIL (c): stricter resolver did not reject comment-only anchor"
            )
            wrong_results.append(
                "PYANCHOR (c): comment_only_symbol in comment not rejected by .py resolver"
            )
        else:
            print(
                f"  PYANCHOR PASS (c): comment-only anchor correctly rejected: {issues_c}"
            )

    # (d) Positive control — async-def arm (WR-03): `async def <anchor>` must resolve.
    # Gives the optional `async ` prefix teeth — a bare `(def|class)` alternation
    # would FALSE-NEGATIVE here because the line begins with `async`, not `def`.
    with tempfile.TemporaryDirectory() as _tmpdir_d:
        _async_py = Path(_tmpdir_d) / "fake_async.py"
        _async_py.write_text(
            "async def some_async_anchor():\n    return 1\n", encoding="utf-8"
        )
        issues_d = _resolve_artifact(f"{_async_py}#some_async_anchor")
        if issues_d:
            print(
                f"  PYANCHOR FAIL (d): async-def arm did not resolve "
                f"`async def some_async_anchor`: {issues_d}"
            )
            wrong_results.append(
                "PYANCHOR (d): async def anchor not resolved by .py resolver (WR-03 regression)"
            )
        else:
            print(
                "  PYANCHOR PASS (d): async-def anchor `some_async_anchor` resolves OK"
            )


def _self_test_v79_rows_sentinel(wrong_results: list[str]) -> None:
    """V79-ROWS named sentinel (D-01 / Phase 123).

    Asserts the 8 v7.9 milestone rows registered in _rows_v79():
      (a) Exactly 8 rows (drift guard — not deleted, not duplicated).
      (b) bare_id set equals the canonical 8 IDs.
      (c) Every row's coverage_tier == "reproducible" (D-02: no "scheduled" rows).
      (d) Every artifact_link deep-resolves via _resolve_artifact (zero issues).
      (e) Positive counter-check: RECON-01 is present and reproducible, proving
          the assertion is non-vacuous (mirrors GEN-01-REPRODUCIBLE idiom).
      (f) milestone/key lock: every row has milestone == "v7.9" AND a key prefixed
          "v7.9/" (attribution guard — a mis-attributed row passes (a)-(e) silently).
      (g) capability lock: every row's capability is in VALID_CAPABILITIES (the same
          TRACE-01 whitelist check_consistency enforces; not re-run by --self-test).

    Called from _rows_v79() live — never hardcodes a MatrixRow literal (Pitfall 4).
    Honesty-not-score (D-01): asserts the documented reproducible registration,
    not a live pass-rate. Any deletion, tier revert, or dangling artifact_link fails CI.
    """
    # (a) Drift guard: read live, assert exactly 8 rows.
    _v79_rows = _rows_v79()
    _v79_count = len(_v79_rows)
    _EXPECTED_V79_IDS = {
        "NEGCAT-01", "NEGCAT-02", "OCH-01", "OCH-02", "OCH-03",
        "COLLIDE-01", "COLLIDE-02", "RECON-01",
    }
    if _v79_count != 8:
        print(
            f"  V79-ROWS FAIL: expected exactly 8 rows in _rows_v79(), "
            f"got {_v79_count} — drift guard failed."
        )
        wrong_results.append("V79-ROWS: row count drift (expected 8)")

    # (b) bare_id set assertion.
    _v79_ids = {r.bare_id for r in _v79_rows}
    if _v79_ids != _EXPECTED_V79_IDS:
        _missing = _EXPECTED_V79_IDS - _v79_ids
        _extra = _v79_ids - _EXPECTED_V79_IDS
        print(
            f"  V79-ROWS FAIL: bare_id set mismatch — "
            f"missing={sorted(_missing)!r}, extra={sorted(_extra)!r}"
        )
        wrong_results.append("V79-ROWS: bare_id set mismatch")
    else:
        print(f"  V79-ROWS PASS: bare_id set = {sorted(_v79_ids)!r}")

    # (c) Every row must be reproducible (D-02 prohibition on "scheduled" rows).
    _non_repro = [r for r in _v79_rows if r.coverage_tier != "reproducible"]
    if _non_repro:
        print(
            f"  V79-ROWS FAIL: {len(_non_repro)} row(s) are not 'reproducible': "
            f"{[r.bare_id for r in _non_repro]!r}"
        )
        wrong_results.append("V79-ROWS: non-reproducible row(s) found")
    else:
        print(f"  V79-ROWS PASS: all {_v79_count} rows are coverage_tier='reproducible'")

    # (d) Deep-resolve every artifact_link; assert zero issues.
    _link_issues: list[str] = []
    for _row in _v79_rows:
        for _issue in _resolve_artifact(_row.artifact_link):
            _link_issues.append(f"{_row.bare_id}: {_issue}")
    if _link_issues:
        for _issue in _link_issues:
            print(f"  V79-ROWS FAIL: artifact_link issue — {_issue}")
        wrong_results.append(f"V79-ROWS: {len(_link_issues)} artifact_link issue(s)")
    else:
        print(f"  V79-ROWS PASS: all {_v79_count} artifact_links deep-resolve OK")

    # (e) Positive counter-check: RECON-01 is present and reproducible.
    _recon01_rows = [r for r in _v79_rows if r.bare_id == "RECON-01"]
    _recon01_present = len(_recon01_rows) == 1
    _recon01_repro = _recon01_rows[0].coverage_tier == "reproducible" if _recon01_rows else False
    if _recon01_present and _recon01_repro:
        print(
            f"  V79-ROWS PASS: RECON-01 present and reproducible "
            f"(artifact_link={_recon01_rows[0].artifact_link!r}) — counter-check non-vacuous"
        )
    else:
        print(
            f"  V79-ROWS FAIL: RECON-01 positive counter-check failed "
            f"(present={_recon01_present}, reproducible={_recon01_repro})"
        )
        wrong_results.append("V79-ROWS: RECON-01 counter-check failed")

    # (f) milestone/key lock: every v7.9 row must carry milestone == "v7.9" AND a
    #     milestone-qualified key of the form "v7.9/<bare_id>". A mis-attributed row
    #     (e.g. key "v8.0/OCH-01" with milestone="v8.0") keeps bare_id/count/tier/link
    #     valid and would otherwise pass silently — this assertion is the attribution lock.
    _bad_ms = [
        r.key for r in _v79_rows
        if r.milestone != "v7.9" or not r.key.startswith("v7.9/")
    ]
    if _bad_ms:
        print(f"  V79-ROWS FAIL: milestone/key drift — {_bad_ms!r}")
        wrong_results.append(f"V79-ROWS: milestone/key drift {_bad_ms!r}")
    else:
        print(f"  V79-ROWS PASS: all {_v79_count} rows carry milestone='v7.9' and 'v7.9/' key prefix")

    # (g) capability lock: reuse the module-level VALID_CAPABILITIES whitelist (the same
    #     set check_consistency enforces, TRACE-01). A capability typo such as
    #     "methodology" (lowercase) is invalid and must fail here, since TRACE-03
    #     --self-test does not run check_consistency() over the live matrix.
    _bad_cap = [r.bare_id for r in _v79_rows if r.capability not in VALID_CAPABILITIES]
    if _bad_cap:
        print(f"  V79-ROWS FAIL: invalid capability on row(s) {_bad_cap!r}")
        wrong_results.append(f"V79-ROWS: invalid capability {_bad_cap!r}")
    else:
        print(
            f"  V79-ROWS PASS: all {_v79_count} rows carry a valid capability "
            f"(in {sorted(VALID_CAPABILITIES)!r})"
        )


def _self_test_v818_rows_sentinel(wrong_results: list[str]) -> None:
    """V818-ROWS named sentinel (D-07 / Phase 4).

    Asserts the 23 v8.18 milestone rows registered in _rows_v818():
      (a) Exactly 23 rows (drift guard — not deleted, not duplicated).
      (b) bare_id set equals the canonical 23 IDs.
      (c) Tier partition pinned by ID, not by count (D-07's first adaptation): the
          audit-only bare_id set is exactly {"SHIP-04", "SHIP-05"} AND the reproducible
          bare_id set is exactly the other 21, named. A blanket 21/2 count assert is
          explicitly rejected — swapping SHIP-04's tier with SHIP-01's would keep the
          counts right and pass silently, the same class of silent pass (f) closes below.
      (d) Deep-resolve artifact_link over the 21 reproducible rows only (D-07's second
          adaptation) — a straight copy of the v7.9 (d) iterates all rows, which is wrong
          here because 2 of the 23 rows are audit-only. Also asserts both audit-only rows
          carry artifact_link == "", so the skip cannot silently become a skip-everything.
      (e) Positive counter-check: HARN-04 is present exactly once, reproducible, and
          carries a non-empty artifact_link (mirrors the V79-ROWS RECON-01 idiom).
      (f) milestone/key lock: every row has milestone == "v8.18" AND a key prefixed
          "v8.18/" (attribution guard — a mis-attributed row passes (a)-(e) silently).
      (g) capability lock: every row's capability is in VALID_CAPABILITIES (the same
          TRACE-01 whitelist check_consistency enforces; not re-run by --self-test).

    Called from _rows_v818() live — never hardcodes a MatrixRow literal (Pitfall 4).
    Honesty-not-score (D-01 idiom): asserts the documented reproducible/audit-only
    registration, not a live pass-rate. Any deletion, tier swap, or dangling
    artifact_link fails CI.
    """
    # (a) Drift guard: read live, assert exactly 23 rows.
    _v818_rows = _rows_v818()
    _v818_count = len(_v818_rows)
    _EXPECTED_V818_IDS = {
        "ACT-01", "ACT-02", "ACT-03", "ACT-04", "ACT-05",
        "LOOP-01", "LOOP-02", "LOOP-03", "LOOP-04", "LOOP-05",
        "PAR-01", "PAR-02", "PAR-03",
        "HARN-01", "HARN-02", "HARN-03", "HARN-04",
        "SHIP-01", "SHIP-02", "SHIP-03", "SHIP-04", "SHIP-05", "SHIP-06",
    }
    _EXPECTED_V818_AUDIT_ONLY_IDS = {"SHIP-04", "SHIP-05"}
    _EXPECTED_V818_REPRODUCIBLE_IDS = _EXPECTED_V818_IDS - _EXPECTED_V818_AUDIT_ONLY_IDS
    if _v818_count != 23:
        print(
            f"  V818-ROWS FAIL: expected exactly 23 rows in _rows_v818(), "
            f"got {_v818_count} — drift guard failed."
        )
        wrong_results.append("V818-ROWS: row count drift (expected 23)")
    else:
        print(f"  V818-ROWS PASS: row count == 23")

    # (b) bare_id set assertion.
    _v818_ids = {r.bare_id for r in _v818_rows}
    if _v818_ids != _EXPECTED_V818_IDS:
        _missing = _EXPECTED_V818_IDS - _v818_ids
        _extra = _v818_ids - _EXPECTED_V818_IDS
        print(
            f"  V818-ROWS FAIL: bare_id set mismatch — "
            f"missing={sorted(_missing)!r}, extra={sorted(_extra)!r}"
        )
        wrong_results.append("V818-ROWS: bare_id set mismatch")
    else:
        print(f"  V818-ROWS PASS: bare_id set = {sorted(_v818_ids)!r}")

    # (c) Tier partition pinned by ID, not by count.
    _audit_only_ids = {r.bare_id for r in _v818_rows if r.coverage_tier == "audit-only"}
    _reproducible_ids = {r.bare_id for r in _v818_rows if r.coverage_tier == "reproducible"}
    if _audit_only_ids != _EXPECTED_V818_AUDIT_ONLY_IDS:
        print(
            f"  V818-ROWS FAIL: audit-only bare_id set mismatch — "
            f"expected={sorted(_EXPECTED_V818_AUDIT_ONLY_IDS)!r}, got={sorted(_audit_only_ids)!r}"
        )
        wrong_results.append("V818-ROWS: audit-only bare_id set mismatch")
    elif _reproducible_ids != _EXPECTED_V818_REPRODUCIBLE_IDS:
        print(
            f"  V818-ROWS FAIL: reproducible bare_id set mismatch — "
            f"expected={sorted(_EXPECTED_V818_REPRODUCIBLE_IDS)!r}, got={sorted(_reproducible_ids)!r}"
        )
        wrong_results.append("V818-ROWS: reproducible bare_id set mismatch")
    else:
        print(
            f"  V818-ROWS PASS: tier partition pinned by ID — audit-only={sorted(_audit_only_ids)!r}, "
            f"21 reproducible IDs confirmed by name"
        )

    # (d) Deep-resolve artifact_link over the 21 reproducible rows only; both audit-only
    #     rows must carry artifact_link == "" (so the skip cannot become a skip-everything).
    _v818_repro_rows = [r for r in _v818_rows if r.coverage_tier == "reproducible"]
    _v818_audit_rows = [r for r in _v818_rows if r.coverage_tier == "audit-only"]
    _link_issues: list[str] = []
    for _row in _v818_repro_rows:
        for _issue in _resolve_artifact(_row.artifact_link):
            _link_issues.append(f"{_row.bare_id}: {_issue}")
    _nonempty_audit_links = [r.bare_id for r in _v818_audit_rows if r.artifact_link != ""]
    if _link_issues:
        for _issue in _link_issues:
            print(f"  V818-ROWS FAIL: artifact_link issue — {_issue}")
        wrong_results.append(f"V818-ROWS: {len(_link_issues)} artifact_link issue(s)")
    elif _nonempty_audit_links:
        print(
            f"  V818-ROWS FAIL: audit-only row(s) with non-empty artifact_link — "
            f"{_nonempty_audit_links!r}"
        )
        wrong_results.append("V818-ROWS: audit-only row(s) with non-empty artifact_link")
    else:
        print(
            f"  V818-ROWS PASS: all {len(_v818_repro_rows)} reproducible artifact_links "
            f"deep-resolve OK, both audit-only rows carry artifact_link=''"
        )

    # (e) Positive counter-check: HARN-04 is present, reproducible, non-empty artifact_link.
    _harn04_rows = [r for r in _v818_rows if r.bare_id == "HARN-04"]
    _harn04_present = len(_harn04_rows) == 1
    _harn04_repro = _harn04_rows[0].coverage_tier == "reproducible" if _harn04_rows else False
    _harn04_link = _harn04_rows[0].artifact_link if _harn04_rows else ""
    if _harn04_present and _harn04_repro and _harn04_link:
        print(
            f"  V818-ROWS PASS: HARN-04 present and reproducible "
            f"(artifact_link={_harn04_link!r}) — counter-check non-vacuous"
        )
    else:
        print(
            f"  V818-ROWS FAIL: HARN-04 positive counter-check failed "
            f"(present={_harn04_present}, reproducible={_harn04_repro}, link={_harn04_link!r})"
        )
        wrong_results.append("V818-ROWS: HARN-04 counter-check failed")

    # (f) milestone/key lock.
    _bad_ms = [
        r.key for r in _v818_rows
        if r.milestone != "v8.18" or not r.key.startswith("v8.18/")
    ]
    if _bad_ms:
        print(f"  V818-ROWS FAIL: milestone/key drift — {_bad_ms!r}")
        wrong_results.append(f"V818-ROWS: milestone/key drift {_bad_ms!r}")
    else:
        print(f"  V818-ROWS PASS: all {_v818_count} rows carry milestone='v8.18' and 'v8.18/' key prefix")

    # (g) capability lock.
    _bad_cap = [r.bare_id for r in _v818_rows if r.capability not in VALID_CAPABILITIES]
    if _bad_cap:
        print(f"  V818-ROWS FAIL: invalid capability on row(s) {_bad_cap!r}")
        wrong_results.append(f"V818-ROWS: invalid capability {_bad_cap!r}")
    else:
        print(
            f"  V818-ROWS PASS: all {_v818_count} rows carry a valid capability "
            f"(in {sorted(VALID_CAPABILITIES)!r})"
        )


def _self_test_v824_rows_sentinel(wrong_results: list[str]) -> None:
    """V824-ROWS named sentinel (D-09 / Phase 6).

    Asserts the 15 v8.24 milestone rows registered in _rows_v824():
      (a) Exactly 15 rows (drift guard — not deleted, not duplicated).
      (b) bare_id set equals the canonical 15 IDs.
      (c) Tier partition pinned by ID, not by count (D-07): the audit-only bare_id set is
          exactly {"VAL-04"} AND the reproducible bare_id set is exactly the other 14, named.
          A blanket 14/1 count assert is explicitly rejected — swapping VAL-04's tier with a
          reproducible row's would keep the counts right and pass silently.
      (d) Deep-resolve artifact_link over the 14 reproducible rows only. Also asserts the
          audit-only row carries artifact_link == "", so the skip cannot silently become a
          skip-everything.
      (e) Positive counter-check: GATE-03 is present exactly once, reproducible, and carries a
          non-empty artifact_link (mirrors the V818-ROWS HARN-04 idiom).
      (f) milestone/key lock: every row has milestone == "v8.24" AND a key prefixed
          "v8.24/" (attribution guard — a mis-attributed row passes (a)-(e) silently).
      (g) capability lock: every row's capability is in VALID_CAPABILITIES (the same
          TRACE-01 whitelist check_consistency enforces; not re-run by --self-test).

    Called from _rows_v824() live — never hardcodes a MatrixRow literal (Pitfall 4).
    Honesty-not-score (D-01 idiom): asserts the documented reproducible/audit-only
    registration, not a live pass-rate. Any deletion, tier swap, or dangling
    artifact_link fails CI.
    """
    # (a) Drift guard: read live, assert exactly 15 rows.
    _v824_rows = _rows_v824()
    _v824_count = len(_v824_rows)
    _EXPECTED_V824_IDS = {
        "CAP-01", "CAP-02", "CAP-03",
        "PROV-01", "PROV-02", "PROV-03", "PROV-04", "PROV-05",
        "GATE-01", "GATE-02", "GATE-03",
        "VAL-01", "VAL-02", "VAL-03", "VAL-04",
    }
    _EXPECTED_V824_AUDIT_ONLY_IDS = {"VAL-04"}
    _EXPECTED_V824_REPRODUCIBLE_IDS = _EXPECTED_V824_IDS - _EXPECTED_V824_AUDIT_ONLY_IDS
    if _v824_count != 15:
        print(
            f"  V824-ROWS FAIL: expected exactly 15 rows in _rows_v824(), "
            f"got {_v824_count} — drift guard failed."
        )
        wrong_results.append("V824-ROWS: row count drift (expected 15)")
    else:
        print(f"  V824-ROWS PASS: row count == 15")

    # (b) bare_id set assertion.
    _v824_ids = {r.bare_id for r in _v824_rows}
    if _v824_ids != _EXPECTED_V824_IDS:
        _missing = _EXPECTED_V824_IDS - _v824_ids
        _extra = _v824_ids - _EXPECTED_V824_IDS
        print(
            f"  V824-ROWS FAIL: bare_id set mismatch — "
            f"missing={sorted(_missing)!r}, extra={sorted(_extra)!r}"
        )
        wrong_results.append("V824-ROWS: bare_id set mismatch")
    else:
        print(f"  V824-ROWS PASS: bare_id set = {sorted(_v824_ids)!r}")

    # (c) Tier partition pinned by ID, not by count.
    _audit_only_ids = {r.bare_id for r in _v824_rows if r.coverage_tier == "audit-only"}
    _reproducible_ids = {r.bare_id for r in _v824_rows if r.coverage_tier == "reproducible"}
    if _audit_only_ids != _EXPECTED_V824_AUDIT_ONLY_IDS:
        print(
            f"  V824-ROWS FAIL: audit-only bare_id set mismatch — "
            f"expected={sorted(_EXPECTED_V824_AUDIT_ONLY_IDS)!r}, got={sorted(_audit_only_ids)!r}"
        )
        wrong_results.append("V824-ROWS: audit-only bare_id set mismatch")
    elif _reproducible_ids != _EXPECTED_V824_REPRODUCIBLE_IDS:
        print(
            f"  V824-ROWS FAIL: reproducible bare_id set mismatch — "
            f"expected={sorted(_EXPECTED_V824_REPRODUCIBLE_IDS)!r}, got={sorted(_reproducible_ids)!r}"
        )
        wrong_results.append("V824-ROWS: reproducible bare_id set mismatch")
    else:
        print(
            f"  V824-ROWS PASS: tier partition pinned by ID — audit-only={sorted(_audit_only_ids)!r}, "
            f"14 reproducible IDs confirmed by name"
        )

    # (d) Deep-resolve artifact_link over the 14 reproducible rows only; the audit-only
    #     row must carry artifact_link == "" (so the skip cannot become a skip-everything).
    _v824_repro_rows = [r for r in _v824_rows if r.coverage_tier == "reproducible"]
    _v824_audit_rows = [r for r in _v824_rows if r.coverage_tier == "audit-only"]
    _link_issues: list[str] = []
    for _row in _v824_repro_rows:
        for _issue in _resolve_artifact(_row.artifact_link):
            _link_issues.append(f"{_row.bare_id}: {_issue}")
    _nonempty_audit_links = [r.bare_id for r in _v824_audit_rows if r.artifact_link != ""]
    if _link_issues:
        for _issue in _link_issues:
            print(f"  V824-ROWS FAIL: artifact_link issue — {_issue}")
        wrong_results.append(f"V824-ROWS: {len(_link_issues)} artifact_link issue(s)")
    elif _nonempty_audit_links:
        print(
            f"  V824-ROWS FAIL: audit-only row(s) with non-empty artifact_link — "
            f"{_nonempty_audit_links!r}"
        )
        wrong_results.append("V824-ROWS: audit-only row(s) with non-empty artifact_link")
    else:
        print(
            f"  V824-ROWS PASS: all {len(_v824_repro_rows)} reproducible artifact_links "
            f"deep-resolve OK, audit-only row carries artifact_link=''"
        )

    # (e) Positive counter-check: GATE-03 is present, reproducible, non-empty artifact_link.
    _gate03_rows = [r for r in _v824_rows if r.bare_id == "GATE-03"]
    _gate03_present = len(_gate03_rows) == 1
    _gate03_repro = _gate03_rows[0].coverage_tier == "reproducible" if _gate03_rows else False
    _gate03_link = _gate03_rows[0].artifact_link if _gate03_rows else ""
    if _gate03_present and _gate03_repro and _gate03_link:
        print(
            f"  V824-ROWS PASS: GATE-03 present and reproducible "
            f"(artifact_link={_gate03_link!r}) — counter-check non-vacuous"
        )
    else:
        print(
            f"  V824-ROWS FAIL: GATE-03 positive counter-check failed "
            f"(present={_gate03_present}, reproducible={_gate03_repro}, link={_gate03_link!r})"
        )
        wrong_results.append("V824-ROWS: GATE-03 counter-check failed")

    # (f) milestone/key lock.
    _bad_ms = [
        r.key for r in _v824_rows
        if r.milestone != "v8.24" or not r.key.startswith("v8.24/")
    ]
    if _bad_ms:
        print(f"  V824-ROWS FAIL: milestone/key drift — {_bad_ms!r}")
        wrong_results.append(f"V824-ROWS: milestone/key drift {_bad_ms!r}")
    else:
        print(f"  V824-ROWS PASS: all {_v824_count} rows carry milestone='v8.24' and 'v8.24/' key prefix")

    # (g) capability lock.
    _bad_cap = [r.bare_id for r in _v824_rows if r.capability not in VALID_CAPABILITIES]
    if _bad_cap:
        print(f"  V824-ROWS FAIL: invalid capability on row(s) {_bad_cap!r}")
        wrong_results.append(f"V824-ROWS: invalid capability {_bad_cap!r}")
    else:
        print(
            f"  V824-ROWS PASS: all {_v824_count} rows carry a valid capability "
            f"(in {sorted(VALID_CAPABILITIES)!r})"
        )


def _self_test_v825_rows_sentinel(wrong_results: list[str]) -> None:
    """V825-ROWS named sentinel (Phase 12).

    Asserts the 14 v8.25 milestone rows registered in _rows_v825():
      (a) Exactly 14 rows (drift guard — not deleted, not duplicated).
      (b) bare_id set equals the canonical 14 IDs.
      (c) Tier partition pinned by ID, not by count: the audit-only bare_id set is exactly
          {"CONTRACT-06"} AND the reproducible bare_id set is exactly the other 13, named. A
          blanket 13/1 count assert is explicitly rejected — swapping CONTRACT-06's tier with
          a reproducible row's would keep the counts right and pass silently.
      (d) Deep-resolve artifact_link over the 13 reproducible rows only. Also asserts the
          audit-only row carries artifact_link == "", so the skip cannot silently become a
          skip-everything.
      (e) Positive counter-check: HEADLINE-01 is present exactly once, reproducible, and
          carries a non-empty artifact_link (mirrors the V824-ROWS GATE-03 idiom).
      (f) milestone/key lock: every row has milestone == "v8.25" AND a key prefixed
          "v8.25/" (attribution guard — a mis-attributed row passes (a)-(e) silently).
      (g) capability lock: every row's capability is in VALID_CAPABILITIES (the same
          TRACE-01 whitelist check_consistency enforces; not re-run by --self-test).

    Called from _rows_v825() live — never hardcodes a MatrixRow literal (Pitfall 4).
    Honesty-not-score (D-01 idiom): asserts the documented reproducible/audit-only
    registration, not a live pass-rate. Any deletion, tier swap, or dangling
    artifact_link fails CI.
    """
    # (a) Drift guard: read live, assert exactly 14 rows.
    _v825_rows = _rows_v825()
    _v825_count = len(_v825_rows)
    _EXPECTED_V825_IDS = {
        "HEADLINE-01", "HEADLINE-02", "HEADLINE-03", "HEADLINE-04", "HEADLINE-05",
        "CONTRACT-01", "CONTRACT-02", "CONTRACT-03", "CONTRACT-04", "CONTRACT-05",
        "CONTRACT-06",
        "SHIP-01", "SHIP-02", "SHIP-03",
    }
    _EXPECTED_V825_AUDIT_ONLY_IDS = {"CONTRACT-06"}
    _EXPECTED_V825_REPRODUCIBLE_IDS = _EXPECTED_V825_IDS - _EXPECTED_V825_AUDIT_ONLY_IDS
    if _v825_count != 14:
        print(
            f"  V825-ROWS FAIL: expected exactly 14 rows in _rows_v825(), "
            f"got {_v825_count} — drift guard failed."
        )
        wrong_results.append("V825-ROWS: row count drift (expected 14)")
    else:
        print(f"  V825-ROWS PASS: row count == 14")

    # (b) bare_id set assertion.
    _v825_ids = {r.bare_id for r in _v825_rows}
    if _v825_ids != _EXPECTED_V825_IDS:
        _missing = _EXPECTED_V825_IDS - _v825_ids
        _extra = _v825_ids - _EXPECTED_V825_IDS
        print(
            f"  V825-ROWS FAIL: bare_id set mismatch — "
            f"missing={sorted(_missing)!r}, extra={sorted(_extra)!r}"
        )
        wrong_results.append("V825-ROWS: bare_id set mismatch")
    else:
        print(f"  V825-ROWS PASS: bare_id set = {sorted(_v825_ids)!r}")

    # (c) Tier partition pinned by ID, not by count.
    _audit_only_ids = {r.bare_id for r in _v825_rows if r.coverage_tier == "audit-only"}
    _reproducible_ids = {r.bare_id for r in _v825_rows if r.coverage_tier == "reproducible"}
    if _audit_only_ids != _EXPECTED_V825_AUDIT_ONLY_IDS:
        print(
            f"  V825-ROWS FAIL: audit-only bare_id set mismatch — "
            f"expected={sorted(_EXPECTED_V825_AUDIT_ONLY_IDS)!r}, got={sorted(_audit_only_ids)!r}"
        )
        wrong_results.append("V825-ROWS: audit-only bare_id set mismatch")
    elif _reproducible_ids != _EXPECTED_V825_REPRODUCIBLE_IDS:
        print(
            f"  V825-ROWS FAIL: reproducible bare_id set mismatch — "
            f"expected={sorted(_EXPECTED_V825_REPRODUCIBLE_IDS)!r}, got={sorted(_reproducible_ids)!r}"
        )
        wrong_results.append("V825-ROWS: reproducible bare_id set mismatch")
    else:
        print(
            f"  V825-ROWS PASS: tier partition pinned by ID — audit-only={sorted(_audit_only_ids)!r}, "
            f"13 reproducible IDs confirmed by name"
        )

    # (d) Deep-resolve artifact_link over the 13 reproducible rows only; the audit-only
    #     row must carry artifact_link == "" (so the skip cannot become a skip-everything).
    _v825_repro_rows = [r for r in _v825_rows if r.coverage_tier == "reproducible"]
    _v825_audit_rows = [r for r in _v825_rows if r.coverage_tier == "audit-only"]
    _link_issues: list[str] = []
    for _row in _v825_repro_rows:
        for _issue in _resolve_artifact(_row.artifact_link):
            _link_issues.append(f"{_row.bare_id}: {_issue}")
    _nonempty_audit_links = [r.bare_id for r in _v825_audit_rows if r.artifact_link != ""]
    if _link_issues:
        for _issue in _link_issues:
            print(f"  V825-ROWS FAIL: artifact_link issue — {_issue}")
        wrong_results.append(f"V825-ROWS: {len(_link_issues)} artifact_link issue(s)")
    elif _nonempty_audit_links:
        print(
            f"  V825-ROWS FAIL: audit-only row(s) with non-empty artifact_link — "
            f"{_nonempty_audit_links!r}"
        )
        wrong_results.append("V825-ROWS: audit-only row(s) with non-empty artifact_link")
    else:
        print(
            f"  V825-ROWS PASS: all {len(_v825_repro_rows)} reproducible artifact_links "
            f"deep-resolve OK, audit-only row carries artifact_link=''"
        )

    # (e) Positive counter-check: HEADLINE-01 is present, reproducible, non-empty artifact_link.
    _headline01_rows = [r for r in _v825_rows if r.bare_id == "HEADLINE-01"]
    _headline01_present = len(_headline01_rows) == 1
    _headline01_repro = _headline01_rows[0].coverage_tier == "reproducible" if _headline01_rows else False
    _headline01_link = _headline01_rows[0].artifact_link if _headline01_rows else ""
    if _headline01_present and _headline01_repro and _headline01_link:
        print(
            f"  V825-ROWS PASS: HEADLINE-01 present and reproducible "
            f"(artifact_link={_headline01_link!r}) — counter-check non-vacuous"
        )
    else:
        print(
            f"  V825-ROWS FAIL: HEADLINE-01 positive counter-check failed "
            f"(present={_headline01_present}, reproducible={_headline01_repro}, link={_headline01_link!r})"
        )
        wrong_results.append("V825-ROWS: HEADLINE-01 counter-check failed")

    # (f) milestone/key lock.
    _bad_ms = [
        r.key for r in _v825_rows
        if r.milestone != "v8.25" or not r.key.startswith("v8.25/")
    ]
    if _bad_ms:
        print(f"  V825-ROWS FAIL: milestone/key drift — {_bad_ms!r}")
        wrong_results.append(f"V825-ROWS: milestone/key drift {_bad_ms!r}")
    else:
        print(f"  V825-ROWS PASS: all {_v825_count} rows carry milestone='v8.25' and 'v8.25/' key prefix")

    # (g) capability lock.
    _bad_cap = [r.bare_id for r in _v825_rows if r.capability not in VALID_CAPABILITIES]
    if _bad_cap:
        print(f"  V825-ROWS FAIL: invalid capability on row(s) {_bad_cap!r}")
        wrong_results.append(f"V825-ROWS: invalid capability {_bad_cap!r}")
    else:
        print(
            f"  V825-ROWS PASS: all {_v825_count} rows carry a valid capability "
            f"(in {sorted(VALID_CAPABILITIES)!r})"
        )


class _HeadlineLockContext(NamedTuple):
    """Everything the HEADLINE-LOCK stages derive from the oracle, in one place.

    Derived by `_headline_lock_context()`, which every stage calls for itself. That is what
    lets the four stages take `wrong_results` and nothing else, matching the dispatch shape
    `_run_self_test()` already uses for its seven peer sentinels (CN-04, Phase 10 review) —
    and it is safe precisely because `_headline_literals()` is deliberately un-memoized and
    `build_matrix_rows()` is deterministic, so re-deriving per stage cannot disagree with
    itself. Block (0) still asserts that `expected` and `prose`, which come from two
    independent calls to `build_matrix_rows()`, agree.
    """
    rows: list["MatrixRow"]
    repro: int
    audit: int
    gap: int
    expected: str
    headline: str
    slash: str
    prose: str


def _headline_lock_context() -> _HeadlineLockContext:
    """Derive the HEADLINE-LOCK stages' shared locals from build_matrix_rows(), live.

    Hoisted out of the former single-function sentinel verbatim, so each stage names its
    locals exactly as it did while they were one function's scope — the split changed which
    function holds a line, never the line itself.
    """
    _rows = build_matrix_rows()
    _repro = sum(1 for r in _rows if r.coverage_tier == "reproducible")
    _audit = sum(1 for r in _rows if r.coverage_tier == "audit-only")
    _gap = sum(1 for r in _rows if r.coverage_tier == "gap")
    _expected = (
        f"{_repro} reproducible / {_audit} audit-only / {_gap} gap / {len(_rows)} total"
    )
    # Label-agnostic literals: bare numbers, no "**Coverage headline:**" prefix and no bold
    # wrapping, so a match works regardless of a surface's own label wording. Obtained from
    # the shared _headline_literals() helper (IN-03 fix) rather than a second hand-derivation
    # of the same _repro/_audit/_gap/len(_rows) locals — two independent derivations of one
    # value invite an edit that changes one and not the other, at which point (a) and (f)
    # would silently disagree about what the headline is.
    _slash, _prose = _headline_literals()
    return _HeadlineLockContext(
        rows=_rows,
        repro=_repro,
        audit=_audit,
        gap=_gap,
        expected=_expected,
        headline=f"**Coverage headline:** {_expected}",
        slash=_slash,
        prose=_prose,
    )


def _headline_lock_preamble(wrong_results: list[str]) -> tuple[str, ...]:
    """HEADLINE-LOCK stage 1 — blocks (0) and (a)-(e): the exemption-set preamble, the
    published-headline lock and its control, and artifact freshness with its control.

    Returns the block labels it ran, which `_self_test_headline_lock()` reconciles against
    the documented block list — a stage dropped from the dispatch tuple is a named FAIL
    rather than a silently shorter run (CN-04, Phase 10 review).
    """
    # (0) Preamble: mechanical invariants on HISTORICAL_EXEMPT_FILES (WR-01, WARNING scope
    # for the first two — not one of the three established CRITICALs). The free-text "every
    # entry must carry its own justification" convention in the constant's comment block
    # remains unenforced; a comment-parsing check is out of scope here. What IS enforced, as
    # of WR-03, is the set's own membership (below).
    _disjoint_violation = sorted(COVERED_HEADLINE_SURFACES & HISTORICAL_EXEMPT_FILES)
    if _disjoint_violation:
        print(
            f"  HEADLINE-LOCK FAIL: (0) {_disjoint_violation} are both registered in "
            "COVERED_HEADLINE_SURFACES and whole-file exempt in HISTORICAL_EXEMPT_FILES — "
            "the two sets carry contradictory meanings and a path in both makes (f) "
            "unsatisfiable for that surface"
        )
        wrong_results.append(
            f"HEADLINE-LOCK: (0) contradictory membership for {_disjoint_violation}"
        )
    else:
        print(
            "  HEADLINE-LOCK PASS: (0) COVERED_HEADLINE_SURFACES and HISTORICAL_EXEMPT_FILES "
            "are disjoint"
        )

    _stale_exemptions = sorted(
        _exempt
        for _exempt in HISTORICAL_EXEMPT_FILES
        if not (REPO_ROOT / _exempt).is_file()
    )
    if _stale_exemptions:
        print(
            f"  HEADLINE-LOCK FAIL: (0) {_stale_exemptions} in HISTORICAL_EXEMPT_FILES do "
            "not resolve to an existing file — a stale entry is a silent whole-file escape "
            "hatch pointed at nothing"
        )
        wrong_results.append(f"HEADLINE-LOCK: (0) stale exemption(s) {_stale_exemptions}")
    else:
        print(
            "  HEADLINE-LOCK PASS: (0) every HISTORICAL_EXEMPT_FILES entry resolves to an "
            "existing file"
        )

    # Named-membership lock (WR-03): HISTORICAL_EXEMPT_FILES may only grow or shrink by an
    # edit that also updates this literal, following the same pattern REG-GUARD uses to pin
    # QUAL-01 as its own single named battery-only exemption. Without this, adding an
    # arbitrary current-fact document to the set (e.g. docs/TESTING.md) produces zero
    # findings and silently makes that file's entire contents invisible to both (f) and the
    # tree-wide scan (j), forever — a whole-file exemption is exactly the shape of escape
    # hatch that must be a deliberate, reviewable edit in two places, never a one-line
    # change. The comparison is symmetric-difference based, so the lock catches shrinkage
    # (a member silently removed, defeating whatever that entry's own comment justifies) as
    # well as growth — a growth-only heuristic would not be a membership lock.
    _expected_exempt = {"CHANGELOG.md", "docs/v8.0-final-closure.md"}
    _exempt_drift = sorted(set(HISTORICAL_EXEMPT_FILES) ^ _expected_exempt)
    if _exempt_drift:
        print(
            f"  HEADLINE-LOCK FAIL: (0) HISTORICAL_EXEMPT_FILES has changed "
            f"({_exempt_drift}) — a whole-file exemption disables both (f) and the "
            "tree-wide scan for that file's entire contents and must be justified here, "
            "with this literal updated to match"
        )
        wrong_results.append(
            f"HEADLINE-LOCK: (0) unreviewed whole-file exemption change {_exempt_drift}"
        )
    else:
        print(
            f"  HEADLINE-LOCK PASS: (0) HISTORICAL_EXEMPT_FILES membership locked "
            f"({sorted(_expected_exempt)})"
        )

    # Named-membership lock (Phase 10 UAT, test 8 residual (a)): _TRACE03_DOC_ROWS may only
    # grow or shrink by an edit that also updates this literal, exactly as HISTORICAL_EXEMPT_FILES
    # is locked above. Hoisting the pair out of block (n) (CN-02) removed the drift risk between
    # (n)'s two former inline copies, but it also made dropping a surface a ONE-line edit where it
    # previously took two: with the pair unasserted, rewriting it to ("CLAUDE.md",) silently stops
    # checking docs/ARCHITECTURE.md's TRACE-03 row while the self-test still exits 0 — measured at
    # the Phase 10 UAT. The comparison is symmetric-difference based so shrinkage is caught, not
    # just growth; a growth-only heuristic would not be a membership lock. Restating the pair here
    # is the point: a lock deriving its expectation from the constant would assert nothing.
    _expected_trace03_rows = {"CLAUDE.md", "docs/ARCHITECTURE.md"}
    _trace03_drift = sorted(set(_TRACE03_DOC_ROWS) ^ _expected_trace03_rows)
    if _trace03_drift:
        print(
            f"  HEADLINE-LOCK FAIL: (0) _TRACE03_DOC_ROWS has changed ({_trace03_drift}) — "
            "block (n) checks the TRACE-03 row transcription only on the files named in that "
            "tuple, so dropping one silently stops checking it; update this literal to match"
        )
        wrong_results.append(
            f"HEADLINE-LOCK: (0) unreviewed TRACE-03 doc-row set change {_trace03_drift}"
        )
    else:
        print(
            f"  HEADLINE-LOCK PASS: (0) _TRACE03_DOC_ROWS membership locked "
            f"({sorted(_expected_trace03_rows)})"
        )

    _rows = build_matrix_rows()
    _repro = sum(1 for r in _rows if r.coverage_tier == "reproducible")
    _audit = sum(1 for r in _rows if r.coverage_tier == "audit-only")
    _gap = sum(1 for r in _rows if r.coverage_tier == "gap")
    _expected = (
        f"{_repro} reproducible / {_audit} audit-only / {_gap} gap / {len(_rows)} total"
    )
    _headline = f"**Coverage headline:** {_expected}"

    # Label-agnostic literals: bare numbers, no "**Coverage headline:**" prefix and no bold
    # wrapping, so a match works regardless of a surface's own label wording. Obtained from
    # the shared _headline_literals() helper (IN-03 fix) rather than a second hand-derivation
    # of the same _repro/_audit/_gap/len(_rows) locals — two independent derivations of one
    # value invite an edit that changes one and not the other, at which point (a) and (f)
    # would silently disagree about what the headline is.
    _slash, _prose = _headline_literals()

    # (0) continued: the sentinel's own _expected (built from this call's _rows) must equal
    # _headline_literals()'s prose rendering (built from ITS OWN independent call to
    # build_matrix_rows()). This turns "two call sites that happen to agree" into a checked
    # invariant — the cheap mechanical enforcement that block (a) (keyed to _expected) and
    # block (f) (keyed to _prose) are asserting against the same figure.
    if _prose != _expected:
        print(
            f"  HEADLINE-LOCK FAIL: (0) _headline_literals() prose rendering {_prose!r} "
            f"disagrees with this sentinel's own _expected {_expected!r} — two independent "
            "calls to build_matrix_rows() produced different figures"
        )
        wrong_results.append(
            f"HEADLINE-LOCK: (0) _prose/_expected mismatch ({_prose!r} vs {_expected!r})"
        )
    else:
        print("  HEADLINE-LOCK PASS: (0) _headline_literals()'s prose rendering matches _expected")

    # Placeholder-collision assertion (IN-09): _SUPERSEDED_PLACEHOLDER must differ from the
    # live slash rendering. Every (h)/(h2)/(i2)/(k) delta-shaped synthetic line is built by
    # joining this fixed placeholder to the CURRENT figure with an arrow — if the placeholder
    # ever equalled the live headline, that join would silently stop being a genuine delta
    # and all four controls would degenerate into asserting nothing, together and silently.
    if _SUPERSEDED_PLACEHOLDER == _slash:
        print(
            f"  HEADLINE-LOCK FAIL: (0) _SUPERSEDED_PLACEHOLDER {_SUPERSEDED_PLACEHOLDER!r} "
            f"collides with the live slash rendering {_slash!r} — every delta-shaped "
            "synthetic line built from it would silently stop being a genuine delta"
        )
        wrong_results.append("HEADLINE-LOCK: (0) placeholder/live-headline collision")
    else:
        print(
            "  HEADLINE-LOCK PASS: (0) _SUPERSEDED_PLACEHOLDER does not collide with the "
            "live headline"
        )

    def _headline_matches(text: str) -> bool:
        """The (a) predicate, isolated so (b) can exercise the identical code path."""
        return _headline in text

    # (a) Published-headline lock. Scoped guard (WR-01): a missing artifact here skips only
    # (b), which is the sole downstream consumer of `_trace` — every block from (c) onward
    # is independent of this guard and must run whether or not it holds, so the guard never
    # aborts the function.
    _trace_path = REPO_ROOT / "docs" / "requirements-traceability.md"
    if not _trace_path.is_file():
        print(f"  HEADLINE-LOCK FAIL: {_trace_path} not found")
        wrong_results.append("HEADLINE-LOCK: docs/requirements-traceability.md missing")
    elif (
        _trace := _headline_read_or_fail(
            _trace_path, "docs/requirements-traceability.md", wrong_results
        )
    ) is None:
        pass  # unreadable: the FAIL is already recorded, and (b) consumes `_trace`
    else:
        if _headline_matches(_trace):
            print(f"  HEADLINE-LOCK PASS: published headline == {_expected}")
        else:
            print(
                f"  HEADLINE-LOCK FAIL: docs/requirements-traceability.md does not state "
                f"{_expected!r} — build_matrix_rows() and the published headline disagree"
            )
            wrong_results.append(
                f"HEADLINE-LOCK: published headline disagrees with build_matrix_rows() "
                f"(expected {_expected!r})"
            )

        # (b) Non-vacuity control for (a): perturb the reproducible count, expect a mismatch.
        # Scoped inside (a)'s guard because it consumes `_trace` directly.
        _mutated_trace = _trace.replace(
            _headline, f"**Coverage headline:** {_repro + 1} reproducible / {_audit} "
            f"audit-only / {_gap} gap / {len(_rows)} total"
        )
        if _headline_matches(_mutated_trace):
            print("  HEADLINE-LOCK FAIL: (a) passed a perturbed headline — assertion is vacuous")
            wrong_results.append("HEADLINE-LOCK: (a) negative control did not fail")
        else:
            print("  HEADLINE-LOCK PASS: (a) rejects a perturbed headline — non-vacuous")

    # (c)/(d) Artifact freshness, and (e) its non-vacuity control, evaluated through ONE
    # shared comparison expression per artifact (CR-02, Phase 10 review). For each tracked
    # artifact the on-disk bytes are compared against two candidate renderings produced by
    # the same renderer — the live row set (that verdict is (c)/(d)) and a deliberately
    # different row set (that verdict is (e)) — inside a single dict comprehension, so the
    # freshness assertion and its own non-vacuity control cannot come from two independently
    # editable expressions. That is what closes CR-02: the previous (e) appended a newline to
    # the DISK side and asserted `_md_disk + "\n" != _md_live`, which is provably true
    # whenever (c)/(d) pass — no string equals both X and X + "\n" — so it could not fail
    # while (c)/(d) passed and never touched the comparison operator under test. Replacing
    # (c)/(d)'s comparisons with `if _md_disk is not None:` — making both freshness
    # assertions unconditionally true, the precise defect (e) claims to exclude — left
    # --self-test green while (e) still printed "non-vacuous". Under the shared expression
    # below the identical mutation makes the PERTURBED verdict true as well, which (e) reports
    # as a vacuous byte-comparison.
    #
    # Scoped guard (WR-01): a missing artifact is a named FAIL for that artifact and removes
    # only its own half of (e) — every block from (f) onward is independent of this guard and
    # must run whether or not it holds, so the guard never aborts the function.

    def _render_matrix_json(rows: list[MatrixRow]) -> str:
        """The JSON artifact exactly as emit_matrix writes it — the same
        json.dumps(..., indent=2) over asdict, in one place so (d) and (e) cannot drift.
        """
        return json.dumps([asdict(r) for r in rows], indent=2)

    _artifact_cases = (
        (
            "docs/requirements-matrix.md",
            REPO_ROOT / "docs" / "requirements-matrix.md",
            render_matrix_markdown,
            "render_matrix_markdown()",
        ),
        (
            "docs/data/matrix.json",
            REPO_ROOT / "docs" / "data" / "matrix.json",
            _render_matrix_json,
            "emit output",
        ),
    )
    # (e)'s perturbation: the same rows minus the last one. Guarded by an explicit named
    # precondition (the (k)/(l)/(m) idiom) — with fewer than two rows the perturbed set is
    # not distinguishable from the real one and the control would prove nothing.
    _e_rows_ok = len(_rows) >= 2
    _e_perturbed_rows = _rows[:-1] if _e_rows_ok else _rows
    _e_perturbed_verdicts: dict[str, bool] = {}
    _e_missing: list[str] = []
    for _artifact_rel, _artifact_path, _artifact_render, _artifact_oracle in _artifact_cases:
        if not _artifact_path.is_file():
            print(f"  HEADLINE-LOCK FAIL: {_artifact_path} not found")
            wrong_results.append(f"HEADLINE-LOCK: {_artifact_rel} missing")
            _e_missing.append(_artifact_rel)
            continue
        _artifact_disk = _headline_read_or_fail(
            _artifact_path, _artifact_rel, wrong_results
        )
        if _artifact_disk is None:
            # Unreadable is as fatal to (e) as absent: it has no disk bytes to compare.
            _e_missing.append(_artifact_rel)
            continue
        # ONE comparison expression, evaluated over both candidate renderings. (c)/(d) read
        # the "live" verdict; (e) below reads the "perturbed" verdict. A rewrite that makes
        # this expression unconditionally true therefore breaks (e) rather than passing it.
        _artifact_verdicts = {
            _which: _artifact_disk == _candidate
            for _which, _candidate in (
                ("live", _artifact_render(_rows)),
                ("perturbed", _artifact_render(_e_perturbed_rows)),
            )
        }
        _e_perturbed_verdicts[_artifact_rel] = _artifact_verdicts["perturbed"]
        if _artifact_verdicts["live"]:
            print(
                f"  HEADLINE-LOCK PASS: {_artifact_rel} byte-identical to "
                f"{_artifact_oracle} ({len(_rows)} rows)"
            )
        else:
            print(
                f"  HEADLINE-LOCK FAIL: {_artifact_rel} is stale — re-run the emit "
                "subcommand"
            )
            wrong_results.append(
                f"HEADLINE-LOCK: {_artifact_rel} disagrees with build_matrix_rows()"
            )

    # (e) Non-vacuity control for (c)/(d): every artifact present above must compare UNEQUAL
    # against the perturbed rendering. A precondition failure here is named rather than an
    # abort, and does not skip any block that follows.
    if _e_missing:
        print(
            f"  HEADLINE-LOCK FAIL: (e) precondition violated — cannot run the non-vacuity "
            f"control because {_e_missing} is missing"
        )
        wrong_results.append(f"HEADLINE-LOCK: (e) precondition violated (missing {_e_missing})")
    elif not _e_rows_ok:
        print(
            f"  HEADLINE-LOCK FAIL: (e) precondition violated — build_matrix_rows() returned "
            f"{len(_rows)} row(s); at least two are needed to render a genuinely different "
            "artifact to compare against"
        )
        wrong_results.append(f"HEADLINE-LOCK: (e) precondition violated ({len(_rows)} rows)")
    else:
        _e_vacuous = sorted(_rel for _rel, _same in _e_perturbed_verdicts.items() if _same)
        if _e_vacuous:
            print(
                f"  HEADLINE-LOCK FAIL: byte-comparison is vacuous — {_e_vacuous} compared "
                f"EQUAL against an artifact rendered from a different row set "
                f"({len(_e_perturbed_rows)} of {len(_rows)} rows)"
            )
            wrong_results.append("HEADLINE-LOCK: (c)/(d) negative control did not fail")
        else:
            print(
                f"  HEADLINE-LOCK PASS: (c)/(d) reject both artifacts re-rendered from a "
                f"different row set ({len(_e_perturbed_rows)} of {len(_rows)} rows) — the "
                "shared byte comparison discriminates, non-vacuous"
            )
    return ("0", "a", "b", "c", "d", "e")


def _headline_lock_surfaces(wrong_results: list[str]) -> tuple[str, ...]:
    """HEADLINE-LOCK stage 2 — blocks (f)-(i3): per-surface headline presence, its
    tightening and perturbation controls, layer attribution and its invariance control, and
    the classifier/adjacency/hit-detection controls.

    Returns the block labels it ran; see `_headline_lock_preamble()` for why.
    """
    _ctx = _headline_lock_context()
    _rows, _repro, _audit, _gap = _ctx.rows, _ctx.repro, _ctx.audit, _ctx.gap
    _expected, _slash, _prose = _ctx.expected, _ctx.slash, _ctx.prose

    # (f) Per-surface headline presence across every currently covered surface (sorted for
    # deterministic output), including docs/requirements-traceability.md again via the
    # label-agnostic scanner — (a) above is specific to that file's own
    # "**Coverage headline:**" label wording, so (f) additionally proves the bare-literal
    # scanner every other surface relies on also covers it.
    _perturbed_prose = (
        f"{_repro + 1} reproducible / {_audit} audit-only / {_gap} gap / {len(_rows)} total"
    )
    _perturbed_slash = f"{_repro + 1}/{_audit}/{_gap}/{len(_rows)}"

    def _perturb_non_historical_hits(text: str, relpath: str) -> str:
        """Return a copy of text with the current headline literal replaced ONLY on lines
        that _is_historical_headline_hit() does not call historical, leaving every
        historical/delta line byte-unchanged. This is what makes (g) sharp: it perturbs
        exactly the lines (f) counts as evidence, via the SAME classifier, rather than a
        rendering-keyed guess at which occurrence is "the" current-fact line. A rendering
        guess (perturb only the prose form, say) is not sound here —
        docs/requirements-traceability.md carries two non-historical hits in two different
        renderings (line 7 prose, line 99 slash narrative — see the measured classification
        table, point 3) and one historical hit in the slash rendering (line 80, arrow), so
        "perturb the prose rendering only" would leave line 99's non-historical slash hit
        live in the mutated copy, silently defeating the control. Verified live against both
        docs/README.md (line 20 non-historical vs. line 100 historical/arrow) and
        docs/requirements-traceability.md (lines 7/99 non-historical vs. line 80
        historical/arrow) before adopting this approach over the rendering-keyed one.
        """
        return "\n".join(
            _line.replace(_prose, _perturbed_prose).replace(_slash, _perturbed_slash)
            if (_prose in _line or _slash in _line)
            and not _is_historical_headline_hit(relpath, _line)
            else _line
            for _line in text.splitlines()
        )

    # (f2) Synthetic control for (f)'s HEADLINE-03 tightening (WR-01, Phase 10 review).
    # (g) is documented as (f)'s non-vacuity control, but it tests the PERTURBATION, not the
    # tightening: reverting (f) to the untightened `list(_hits)` left --self-test at exit 0
    # with zero FAIL lines, and reverting (f) AND (g) together was caught only incidentally,
    # by the two surfaces that happen to carry a historical hit. These two arms depend on no
    # live file's current shape, and both drive _non_historical_headline_hits() — the
    # identical function object (f) and (g) call.
    #   Arm 1 (the tightening): a text whose ONLY headline occurrence is a delta row must
    #   yield zero hits, so a surface can never satisfy (f) on a ledger delta alone.
    #   Arm 2 (anti-tautology): the same text with one present-tense line appended must yield
    #   exactly that line, so a predicate rewritten to return nothing cannot pass arm 1.
    _f2_path = "docs/synthetic-f-tightening-check.md"
    if _f2_path in COVERED_HEADLINE_SURFACES or _f2_path in HISTORICAL_EXEMPT_FILES:
        print(
            "  HEADLINE-LOCK FAIL: (f2) precondition violated — synthetic path is "
            "registered or whole-file exempt"
        )
        wrong_results.append("HEADLINE-LOCK: (f2) precondition violated")
    else:
        _f2_delta_only = (
            f"| 9 | some milestone | {_SUPERSEDED_PLACEHOLDER} → {_slash} | ... |"
        )
        _f2_delta_hits = _non_historical_headline_hits(_f2_delta_only, _f2_path)
        if _f2_delta_hits:
            print(
                "  HEADLINE-LOCK FAIL: (f2) a delta-only text satisfies the per-surface "
                f"presence predicate ({_f2_delta_hits}) — (f)'s HEADLINE-03 tightening has "
                "been reverted"
            )
            wrong_results.append("HEADLINE-LOCK: (f2) tightening reverted (delta-only arm)")
        else:
            print(
                "  HEADLINE-LOCK PASS: (f2) a text whose only headline occurrence is a delta "
                "row yields zero non-historical hits — (f)'s tightening is in force"
            )
        _f2_mixed = f"{_f2_delta_only}\nThe coverage headline is now {_prose}."
        _f2_mixed_hits = _non_historical_headline_hits(_f2_mixed, _f2_path)
        if [_lineno for _lineno, _ in _f2_mixed_hits] == [2]:
            print(
                "  HEADLINE-LOCK PASS: (f2) anti-tautology arm — the same text plus one "
                "present-tense line yields exactly that line (line 2), so the predicate is "
                "not simply returning nothing"
            )
        else:
            print(
                "  HEADLINE-LOCK FAIL: (f2) anti-tautology arm — expected exactly the "
                f"present-tense line (line 2), got {_f2_mixed_hits}"
            )
            wrong_results.append("HEADLINE-LOCK: (f2) anti-tautology arm failed")

    for _surface in sorted(COVERED_HEADLINE_SURFACES):
        _surface_path = REPO_ROOT / _surface
        if not _surface_path.is_file():
            print(f"  HEADLINE-LOCK FAIL: (f) {_surface} not found")
            wrong_results.append(f"HEADLINE-LOCK: (f) {_surface} missing")
            continue
        _surface_text = _headline_read_or_fail(
            _surface_path, f"(f) {_surface}", wrong_results
        )
        if _surface_text is None:
            continue  # this surface's (f) and (g) cannot run; the FAIL is already recorded
        _current_hits = _non_historical_headline_hits(_surface_text, _surface)
        if _current_hits:
            _renderings = sorted(
                {"prose" if _prose in _line else "slash" for _, _line in _current_hits}
            )
            print(
                f"  HEADLINE-LOCK PASS: (f) {_surface} states the current, non-historical "
                f"headline (rendering(s): {', '.join(_renderings)})"
            )
        else:
            print(
                f"  HEADLINE-LOCK FAIL: (f) {_surface} does not state {_expected!r} as a "
                f"non-historical occurrence — build_matrix_rows() and {_surface} disagree, "
                f"or the only occurrence present is historical/delta"
            )
            wrong_results.append(
                f"HEADLINE-LOCK: (f) {_surface} does not state the current headline "
                f"(expected {_expected!r})"
            )

        # (g) Non-vacuity control for (f): perturb this surface's in-memory copy so that
        # (f)'s tightened, non-historical-only predicate finds zero hits. Only lines the
        # classifier does NOT call historical are perturbed — every historical/delta line
        # (e.g. an arrow-marked ledger row) is left byte-correct in the mutated copy, so the
        # control proves the classifier (not a blanket textual perturbation) is what does
        # the rejecting. For surfaces with a single, non-historical occurrence this has the
        # same effect as plan 10-01's blanket perturbation.
        _mutated_surface = _perturb_non_historical_hits(_surface_text, _surface)
        _mutated_current_hits = _non_historical_headline_hits(_mutated_surface, _surface)
        if _mutated_current_hits:
            print(
                f"  HEADLINE-LOCK FAIL: (g) {_surface} still has a non-historical match "
                f"after its current-fact occurrence was perturbed — control is vacuous"
            )
            wrong_results.append(f"HEADLINE-LOCK: (g) {_surface} negative control did not fail")
        else:
            print(
                f"  HEADLINE-LOCK PASS: (g) {_surface} rejects a perturbed headline — "
                f"non-vacuous"
            )

    def _headline_exempt_layer(
        relpath: str, line: str, literals: tuple[str, str] | None = None
    ) -> str:
        """Which layer of _is_historical_headline_hit() classifies (relpath, line) as
        historical: "whole-file" if relpath is a member of HISTORICAL_EXEMPT_FILES,
        "arrow" if the classifier accepted the line for any other reason, or "" if the
        classifier does not call it historical at all.

        Delegates to _is_historical_headline_hit() rather than re-deriving the arrow test,
        so this helper can never disagree with the classifier it attributes — a control
        exercising a parallel copy would prove nothing (research Pitfall 4, the same rule
        _unregistered_headline_finding() below already observes). If the classifier's arrow
        layer is narrowed or a third layer is ever added, this helper picks up the change
        automatically instead of silently keeping stale semantics while still printing PASS.

        `literals`, when given, is forwarded unchanged to _is_historical_headline_hit() — this
        helper re-derives nothing of its own.
        """
        if not _is_historical_headline_hit(relpath, line, literals=literals):
            return ""
        # Whole-file is checked first by the classifier, so a member relpath is attributed
        # there regardless of the line; anything else the classifier accepted is arrow-layer.
        return "whole-file" if relpath in HISTORICAL_EXEMPT_FILES else "arrow"

    # (h) Positive controls (ROADMAP criterion 3, CR-02 fix): layer attribution is asserted
    # on SYNTHETIC lines carrying the current literal at the REAL surface relpath, never on
    # a line located by scanning the live file for today's figure — the synthetic line is
    # built from the current literal at call time, not scanned out of the live file's text,
    # so binding the control to a live occurrence of it made the precondition ("this line
    # contains today's headline") strictly stronger than the property under test ("this line
    # is historical") — the next legitimate headline move broke all three controls and could
    # only be resolved by editing CHANGELOG.md or docs/v8.0-final-closure.md, two records this
    # repo designates historical and frozen (CR-02). Every literal below is built from the
    # in-scope _prose/_slash locals; the delta row's superseded left-hand figure is a fixed,
    # non-current placeholder and is not the headline, so it may be typed.
    _synthetic_no_arrow_line = f"Superseded: the headline is now {_prose}."
    _synthetic_delta_line = (
        f"| 9 | some milestone | {_SUPERSEDED_PLACEHOLDER} → {_slash} | ... |"
    )
    for _relpath, _line, _want in (
        ("docs/v8.0-final-closure.md", _synthetic_no_arrow_line, "whole-file"),
        ("CHANGELOG.md", _synthetic_no_arrow_line, "whole-file"),
        ("docs/requirements-traceability.md", _synthetic_delta_line, "arrow"),
    ):
        if (
            _relpath == "docs/requirements-traceability.md"
            and _relpath in HISTORICAL_EXEMPT_FILES
        ):
            # Explicit precondition (T-10-05): if this file were ever added to the
            # whole-file exemption, assertion (a) (which requires this same file to state
            # the current headline as a present-tense claim) would be defeated. Say so
            # rather than silently attributing the delta row to the wrong layer.
            print(
                f"  HEADLINE-LOCK FAIL: (h) precondition violated — {_relpath} is in "
                "HISTORICAL_EXEMPT_FILES, which would defeat assertion (a)"
            )
            wrong_results.append(f"HEADLINE-LOCK: (h) {_relpath} precondition violated")
            continue
        _got = _headline_exempt_layer(_relpath, _line)
        if _got == _want:
            print(
                f"  HEADLINE-LOCK PASS: (h) {_relpath} attributes a synthetic "
                f"{'delta-shaped' if _want == 'arrow' else 'no-arrow'} line carrying the "
                f"current literal to the {_want.upper()} layer"
            )
        else:
            print(
                f"  HEADLINE-LOCK FAIL: (h) {_relpath} attributed a synthetic "
                f"{'delta-shaped' if _want == 'arrow' else 'no-arrow'} line to {_got!r}, "
                f"wanted {_want!r}"
            )
            wrong_results.append(f"HEADLINE-LOCK: (h) {_relpath} layer attribution failed")

    # Discriminating arm (WR-06 fix): the identical synthetic no-arrow line, evaluated at a
    # relpath that is NOT whole-file exempt, must attribute "" — proving it is whole-file
    # MEMBERSHIP, not the line's content, that rescues the two whole-file cases above. This
    # is what stops the CHANGELOG.md/v8.0-final-closure.md cases from being tautological:
    # the same line at a non-exempt path is correctly NOT rescued.
    _non_exempt_relpath = "docs/does-not-exist-synthetic-non-exempt-headline-check.md"
    if _non_exempt_relpath in HISTORICAL_EXEMPT_FILES:
        print(
            "  HEADLINE-LOCK FAIL: (h) precondition violated — the discriminating arm's "
            "synthetic path is in HISTORICAL_EXEMPT_FILES"
        )
        wrong_results.append("HEADLINE-LOCK: (h) discriminating-arm precondition violated")
    else:
        _got = _headline_exempt_layer(_non_exempt_relpath, _synthetic_no_arrow_line)
        if _got == "":
            print(
                "  HEADLINE-LOCK PASS: (h) the same no-arrow synthetic line attributes to "
                "'' at a non-whole-file-exempt relpath — whole-file MEMBERSHIP rescues the "
                "line, not its content"
            )
        else:
            print(
                f"  HEADLINE-LOCK FAIL: (h) the no-arrow synthetic line attributed to "
                f"{_got!r} at a non-exempt relpath — should be '' (content alone should "
                "not rescue it)"
            )
            wrong_results.append(
                "HEADLINE-LOCK: (h) discriminating arm did not attribute ''"
            )

    # Demoted live-file observation (CR-02): the whole-file layer's only live proof in this
    # tree — a no-arrow current-literal line genuinely present in docs/v8.0-final-closure.md
    # — is reported for visibility in diff review, never asserted, because it legitimately
    # stops being true the moment the headline moves; binding the gate to it is precisely
    # the defect CR-02 records. A missing docs/v8.0-final-closure.md is still a real
    # repository defect and stays a wrong_results finding.
    _v80_path = REPO_ROOT / "docs" / "v8.0-final-closure.md"
    if not _v80_path.is_file():
        print(f"  HEADLINE-LOCK FAIL: (h) {_v80_path} not found")
        wrong_results.append("HEADLINE-LOCK: (h) docs/v8.0-final-closure.md missing")
    elif (
        _v80_text := _headline_read_or_fail(
            _v80_path, "(h) docs/v8.0-final-closure.md", wrong_results
        )
    ) is None:
        pass  # unreadable: the FAIL is already recorded, the INFO line below is not reachable
    else:
        # Selector delegates to _headline_exempt_layer() rather than a parallel whole-line
        # substring test (WR-04): a line the ARROW layer would not have rescued is any line
        # NOT attributed to "arrow". docs/v8.0-final-closure.md is itself whole-file exempt,
        # so _headline_exempt_layer() attributes every hit here to "whole-file" regardless of
        # content — the selector therefore picks the first hit unconditionally, which is the
        # correct behavior for this specific file: the arrow layer could never have been what
        # rescued a hit here in the first place, so there is nothing left for the substring
        # test to approximate.
        _v80_hit = next(
            (
                (_i, _line)
                for _i, _line in _headline_hits(_v80_text)
                if _headline_exempt_layer("docs/v8.0-final-closure.md", _line) != "arrow"
            ),
            None,
        )
        if _v80_hit is not None:
            print(
                "  HEADLINE-LOCK INFO: (h) docs/v8.0-final-closure.md still carries a live "
                f"no-arrow current-literal line (line {_v80_hit[0]}) — reported only, not "
                "asserted, because it is expected to stop being true on a headline move"
            )
        else:
            print(
                "  HEADLINE-LOCK INFO: (h) docs/v8.0-final-closure.md no longer carries a "
                "live no-arrow current-literal line — expected after a headline move, "
                "reported only, not asserted"
            )

    # (h2) Headline-move invariance control: for each (h) case, build the identical synthetic
    # line twice — once from _prose/_slash, once from _perturbed_prose/_perturbed_slash
    # (already in scope for block (g), reused rather than re-derived) — and require
    # _headline_exempt_layer() to return the SAME layer for both. The property this asserts is
    # NOT "the classifier never reads the figure" (it does, as of Plan 08's anchoring fix): it
    # is that layer attribution is invariant when the FIGURE AND THE LINE MOVE TOGETHER, which
    # is exactly what a real headline move does. The two evaluations are therefore deliberately
    # asymmetric: the original line is evaluated against the CURRENT literals (the classifier's
    # default), and the perturbed line is evaluated against the PERTURBED literals, passed
    # explicitly as `literals=(_perturbed_slash, _perturbed_prose)` (slash first, matching
    # _headline_literals()'s documented order). Evaluating the perturbed line against the
    # CURRENT literals instead — the naive form — would now assert something FALSE rather than
    # invariant: the anchored classifier no longer finds the current literal adjacent to an
    # arrow on a line that was rewritten to state the perturbed one. A second arm asserts the
    # two constructed lines are NOT byte-equal, so a future edit that made the perturbation a
    # no-op cannot leave this comparing a string to itself forever.
    _perturbed_no_arrow_line = f"Superseded: the headline is now {_perturbed_prose}."
    _perturbed_delta_line = (
        f"| 9 | some milestone | {_SUPERSEDED_PLACEHOLDER} → {_perturbed_slash} | ... |"
    )
    _perturbed_literals = (_perturbed_slash, _perturbed_prose)
    # Each case carries the layer it is EXPECTED to be attributed to, and both are asserted:
    # invariance (the two evaluations agree) and attribution (they agree on the right layer).
    # Attribution is what stops two of these arms from being decorative (WR-05, Phase 10
    # review): `_is_historical_headline_hit()` short-circuits on whole-file membership BEFORE
    # `literals` is resolved, so for the two whole-file cases both evaluations return
    # "whole-file" without the perturbed literals ever reaching the arrow layer — structurally
    # incapable of failing while the (0) membership lock holds. Those two arms are still worth
    # keeping (they assert the property the frozen documents rely on), but the invariance
    # property itself is carried ONLY by an arm that goes through the arrow layer, so a fourth
    # case runs the same delta-shaped line at a synthetic NON-exempt relpath — the only shape
    # in which the perturbed-literals path can produce a different verdict, and one that does
    # not depend on docs/requirements-traceability.md's membership staying as it is.
    _h2_synthetic_path = "docs/does-not-exist-synthetic-h2-non-exempt.md"
    _h2_cases = (
        (
            "docs/v8.0-final-closure.md",
            _synthetic_no_arrow_line,
            _perturbed_no_arrow_line,
            "whole-file",
        ),
        ("CHANGELOG.md", _synthetic_no_arrow_line, _perturbed_no_arrow_line, "whole-file"),
        (
            "docs/requirements-traceability.md",
            _synthetic_delta_line,
            _perturbed_delta_line,
            "arrow",
        ),
        (_h2_synthetic_path, _synthetic_delta_line, _perturbed_delta_line, "arrow"),
    )
    _h2_precondition_failed = [
        _relpath
        for _relpath, _orig_line, _pert_line, _want in _h2_cases
        if _orig_line == _pert_line
    ]
    if _h2_synthetic_path in HISTORICAL_EXEMPT_FILES:
        # Without this, the fourth case would be rescued by whole-file membership and would
        # degenerate into a fourth copy of the two decorative arms.
        print(
            "  HEADLINE-LOCK FAIL: (h2) precondition violated — the non-exempt arm's "
            "synthetic path is in HISTORICAL_EXEMPT_FILES"
        )
        wrong_results.append("HEADLINE-LOCK: (h2) non-exempt arm precondition violated")
    elif _h2_precondition_failed:
        print(
            f"  HEADLINE-LOCK FAIL: (h2) precondition violated for "
            f"{_h2_precondition_failed} — synthetic and perturbed lines are byte-equal, "
            "the perturbation did not change the line"
        )
        wrong_results.append(
            f"HEADLINE-LOCK: (h2) precondition violated for {_h2_precondition_failed}"
        )
    else:
        _h2_verdicts = [
            (_relpath, _want, _headline_exempt_layer(_relpath, _orig_line),
             _headline_exempt_layer(_relpath, _pert_line, literals=_perturbed_literals))
            for _relpath, _orig_line, _pert_line, _want in _h2_cases
        ]
        _h2_broken = [
            (_relpath, _layer_orig, _layer_pert)
            for _relpath, _want, _layer_orig, _layer_pert in _h2_verdicts
            if _layer_orig != _layer_pert
        ]
        _h2_misattributed = [
            (_relpath, _want, _layer_orig)
            for _relpath, _want, _layer_orig, _layer_pert in _h2_verdicts
            if _layer_orig != _want
        ]
        if _h2_broken:
            print(
                f"  HEADLINE-LOCK FAIL: (h2) layer attribution is NOT invariant under a "
                f"perturbed figure: {_h2_broken} — a consumer has been rebound to the "
                "current literal"
            )
            wrong_results.append(
                f"HEADLINE-LOCK: (h2) invariance broken for "
                f"{[r for r, _, _ in _h2_broken]}"
            )
        elif _h2_misattributed:
            print(
                f"  HEADLINE-LOCK FAIL: (h2) invariance holds but attribution is wrong: "
                f"{_h2_misattributed} (relpath, wanted, got) — the arms that are supposed to "
                "carry the property through the ARROW layer are not reaching it"
            )
            wrong_results.append(
                f"HEADLINE-LOCK: (h2) misattributed layers for "
                f"{[r for r, _, _ in _h2_misattributed]}"
            )
        else:
            _h2_arrow_arms = [
                _relpath for _relpath, _want, _, _ in _h2_verdicts if _want == "arrow"
            ]
            print(
                "  HEADLINE-LOCK PASS: (h2) all four verdicts are invariant under a "
                "perturbed figure and land on the expected layer; the two whole-file arms "
                "(docs/v8.0-final-closure.md, CHANGELOG.md) are invariant by MEMBERSHIP — "
                "the perturbed literals never reach the arrow layer — and the invariance "
                f"property itself is carried by the arrow arms {_h2_arrow_arms}"
            )

    # (i) Non-vacuity control for the classifier itself (T-10-04): prevents (h)'s positive
    # controls from passing off a classifier rewritten to always return "historical".
    # Preconditions are asserted explicitly so this control cannot silently degrade if a
    # future edit adds the synthetic path to HISTORICAL_EXEMPT_FILES.
    # WR-04: the former separate "does this line contain an arrow" precondition was itself a
    # parallel whole-line substring copy of the arrow semantics (research Pitfall 4 — a
    # control exercising a parallel copy proves nothing). It is deleted rather than rewired,
    # because the very next branch already calls _is_historical_headline_hit() directly on
    # this exact (path, line) pair — rewiring the precondition to the identical call would
    # only produce two branches testing the same condition, the second permanently
    # unreachable. The remaining branch's FAIL message already names the classifier verdict.
    _synthetic_path = "docs/does-not-exist-synthetic-headline-check.md"
    _synthetic_line = f"This is a synthetic current-fact line: {_prose}"
    if _synthetic_path in HISTORICAL_EXEMPT_FILES:
        print(
            "  HEADLINE-LOCK FAIL: (i) precondition violated — synthetic path is in "
            "HISTORICAL_EXEMPT_FILES"
        )
        wrong_results.append("HEADLINE-LOCK: (i) precondition violated (whole-file)")
    elif _is_historical_headline_hit(_synthetic_path, _synthetic_line):
        print(
            "  HEADLINE-LOCK FAIL: (i) classifier called a non-exempt, no-arrow line "
            "historical — classifier is vacuous or over-broad"
        )
        wrong_results.append("HEADLINE-LOCK: (i) classifier non-vacuity control did not fail")
    else:
        print(
            "  HEADLINE-LOCK PASS: (i) classifier correctly rejects a non-exempt, no-arrow "
            "line as historical — non-vacuous"
        )

    # (i2) Adjacency-specific controls (CR-03, WR-07, BL-01/T-10-08). Six named arms, each
    # driving through _unregistered_headline_finding() — the SAME decision function (j) and
    # (k) call, never a parallel copy. Writes nothing to disk. One sentence per arm on what it
    # guards, four fail-open (a defect that would let a stale current-fact statement escape
    # detection) and two fail-closed (a defect that would falsely flag a genuine delta):
    #   1. mermaid edge (fail-open)         — a diagram edge must not donate an arrow.
    #   2. bare HTML comment close (fail-open) — an unclosed "-->" must not donate an arrow.
    #   3. genuine delta (fail-closed)      — a real superseded->current reading stays exempt.
    #   4. arrow-collision (fail-open, BL-01) — an unrelated numeric arrow sharing the line
    #      with the current headline must not exempt it; not contrived — 67 in-scope lines
    #      already carry an unrelated digit-arrow-digit pair.
    #   5. ASCII-long-arrow delta (fail-closed, WR-07) — a genuine delta written "-->" must
    #      stay exempt in the rendering the old unconditional comment strip used to destroy.
    #   6. complete-comment counter-arm (fail-open, WR-07) — a real "<!-- ... -->" comment
    #      must not donate its terminator to the arrow layer once removed; without this arm,
    #      arm 5 alone would also pass against a classifier that simply stopped stripping
    #      comments altogether.
    _i2_path = "docs/synthetic-adjacency-check.md"
    if _i2_path in COVERED_HEADLINE_SURFACES or _i2_path in HISTORICAL_EXEMPT_FILES:
        print(
            "  HEADLINE-LOCK FAIL: (i2) precondition violated — synthetic path is "
            "registered or whole-file exempt"
        )
        wrong_results.append("HEADLINE-LOCK: (i2) precondition violated")
    else:
        print(
            f"  HEADLINE-LOCK PASS: (i2) precondition — {_i2_path} is absent from both "
            "COVERED_HEADLINE_SURFACES and HISTORICAL_EXEMPT_FILES"
        )

        # 1. Mermaid edge is NOT exempt.
        _i2_mermaid_line = f"NODE_A --> NODE_B carrying {_prose}"
        _i2_mermaid_finding, _i2_mermaid_msg = _unregistered_headline_finding(
            _i2_path, (1, _i2_mermaid_line)
        )
        if _i2_mermaid_finding and _i2_path in _i2_mermaid_msg:
            print(
                "  HEADLINE-LOCK PASS: (i2) a mermaid edge sharing a line with the current "
                "headline is reported as a finding — not exempt"
            )
        else:
            print(
                "  HEADLINE-LOCK FAIL: (i2) a mermaid edge sharing a line with the current "
                "headline was NOT reported as a finding"
            )
            wrong_results.append("HEADLINE-LOCK: (i2) mermaid edge non-exemption failed")

        # 2. HTML comment terminator is NOT exempt — the exact CR-03 reproduction, promoted
        # into a permanent control.
        _i2_html_line = f"See -->  {_prose}"
        _i2_html_finding, _i2_html_msg = _unregistered_headline_finding(
            _i2_path, (1, _i2_html_line)
        )
        if _i2_html_finding and _i2_path in _i2_html_msg:
            print(
                "  HEADLINE-LOCK PASS: (i2) an HTML comment terminator sharing a line with "
                "the current headline is reported as a finding — not exempt"
            )
        else:
            print(
                "  HEADLINE-LOCK FAIL: (i2) an HTML comment terminator sharing a line with "
                "the current headline was NOT reported as a finding"
            )
            wrong_results.append(
                "HEADLINE-LOCK: (i2) HTML comment terminator non-exemption failed"
            )

        # 3. A genuine delta line IS exempt — without this arm, controls 1 and 2 would pass
        # against a classifier that returns False unconditionally.
        _i2_delta_line = f"{_SUPERSEDED_PLACEHOLDER} → {_slash}"
        _i2_delta_finding, _ = _unregistered_headline_finding(_i2_path, (1, _i2_delta_line))
        if not _i2_delta_finding:
            print(
                "  HEADLINE-LOCK PASS: (i2) a genuine delta line (superseded figure → "
                "current figure) is NOT reported as a finding — exempt as expected"
            )
        else:
            print(
                "  HEADLINE-LOCK FAIL: (i2) a genuine delta line was reported as a finding "
                "— the narrowing over-disabled the arrow layer"
            )
            wrong_results.append("HEADLINE-LOCK: (i2) delta-line exemption failed")

        # 4. Arrow-collision non-exemption (BL-01, permanently encoded). An unrelated
        # battery-count delta sharing a line with a present-tense statement of the current
        # headline must NOT exempt that line — the sentence shape is lifted from
        # docs/README.md:187, with the headline half built from _prose and never typed. Not
        # contrived: 67 in-scope lines already carry an unrelated digit-arrow-digit pair, and
        # this is the escape that made SC5 fail before this plan.
        _i2_unrelated_line = f"The offline battery moved 17 → 20 and coverage is now {_prose}."
        _i2_unrelated_finding, _i2_unrelated_msg = _unregistered_headline_finding(
            _i2_path, (1, _i2_unrelated_line)
        )
        if _i2_unrelated_finding and _i2_path in _i2_unrelated_msg:
            print(
                "  HEADLINE-LOCK PASS: (i2) an unrelated numeric arrow sharing a line with "
                "the current headline is reported as a finding — not exempt"
            )
        else:
            print(
                "  HEADLINE-LOCK FAIL: (i2) an unrelated numeric arrow sharing a line with "
                "the current headline was NOT reported as a finding"
            )
            wrong_results.append("HEADLINE-LOCK: (i2) arrow-collision non-exemption failed")

        # 5. ASCII-long-arrow delta exemption (WR-07 reproduction). A genuine delta written
        # with the ASCII long arrow must stay exempt — the rendering the unconditional
        # comment strip used to destroy. References _HTML_COMMENT_CLOSE for the arrow rather
        # than retyping it, so the control and the classifier share the one literal.
        _i2_long_arrow_delta_line = f"{_SUPERSEDED_PLACEHOLDER} {_HTML_COMMENT_CLOSE} {_slash}"
        _i2_long_arrow_finding, _ = _unregistered_headline_finding(
            _i2_path, (1, _i2_long_arrow_delta_line)
        )
        if not _i2_long_arrow_finding:
            print(
                "  HEADLINE-LOCK PASS: (i2) a genuine delta line written with the ASCII "
                "long arrow is NOT reported as a finding — exempt as expected"
            )
        else:
            print(
                "  HEADLINE-LOCK FAIL: (i2) a genuine delta line written with the ASCII long "
                "arrow was reported as a finding — the comment strip destroyed its arrow"
            )
            wrong_results.append("HEADLINE-LOCK: (i2) ASCII-long-arrow delta exemption failed")

        # 6. Complete-comment strip counter-arm (WR-07). A line that opens AND closes an HTML
        # comment before stating the headline as present-tense fact must still be reported —
        # proving the narrowed strip removed the comment without donating its terminator to
        # the arrow layer. Without this arm, arm 5 alone would also pass against a classifier
        # that simply stopped stripping comments altogether. The superseded placeholder is
        # placed INSIDE the comment, immediately before its own closing "-->", so an
        # unstripped classifier would misread the comment's terminator as a genuine delta
        # arrow between the placeholder and the current literal — a comment strip that merely
        # stopped running (rather than one narrowed to complete comments) would let this line
        # through undetected, which is exactly the risk this arm exists to catch.
        _i2_complete_comment_line = f"<!-- {_SUPERSEDED_PLACEHOLDER} --> {_prose}"
        _i2_complete_comment_finding, _i2_complete_comment_msg = _unregistered_headline_finding(
            _i2_path, (1, _i2_complete_comment_line)
        )
        if _i2_complete_comment_finding and _i2_path in _i2_complete_comment_msg:
            print(
                "  HEADLINE-LOCK PASS: (i2) a complete HTML comment preceding the current "
                "headline is reported as a finding — the removed comment did not donate an "
                "arrow"
            )
        else:
            print(
                "  HEADLINE-LOCK FAIL: (i2) a complete HTML comment preceding the current "
                "headline was NOT reported as a finding"
            )
            wrong_results.append(
                "HEADLINE-LOCK: (i2) complete-comment strip counter-arm failed"
            )

        # 7. Right-direction arrow non-exemption (WR-09, Phase 10 review). The arrow layer's
        # second orientation used to exempt "<current literal> <arrow> <any digit run>", so a
        # line stating the current figure followed by an arrow and any digits at all — a
        # mermaid edge whose SOURCE label is the headline, a "current → projected" planning
        # note, a table cell "| <literal> | → | 5 |" — was silently dropped from both (f) and
        # the tree-wide scan. That is the direction that hides a CURRENT-FACT statement rather
        # than a superseded one, and neither TRACE-03 doc row disclosed it. The right-hand side
        # must now be shaped like a coverage reading, and this arm encodes that decision so it
        # cannot revert to an accident.
        _i2_right_digits_line = f"{_slash} {_HTML_COMMENT_CLOSE} 999"
        _i2_right_digits_finding, _i2_right_digits_msg = _unregistered_headline_finding(
            _i2_path, (1, _i2_right_digits_line)
        )
        if _i2_right_digits_finding and _i2_path in _i2_right_digits_msg:
            print(
                "  HEADLINE-LOCK PASS: (i2) the current headline followed by an arrow and a "
                "bare digit run is reported as a finding — not exempt"
            )
        else:
            print(
                "  HEADLINE-LOCK FAIL: (i2) the current headline followed by an arrow and a "
                "bare digit run was NOT reported as a finding — the right-direction arrow "
                "rule is fail-open again"
            )
            wrong_results.append(
                "HEADLINE-LOCK: (i2) right-direction digit-run non-exemption failed"
            )

        # 8. Right-direction arrow exemption counter-arm (WR-09, fail-closed half). A genuine
        # "current figure → some other coverage reading" delta must stay exempt — without this
        # arm, arm 7 would also pass against a classifier that simply deleted the right-hand
        # orientation altogether.
        _i2_right_figure_line = f"{_slash} → {_SUPERSEDED_PLACEHOLDER}"
        _i2_right_figure_finding, _ = _unregistered_headline_finding(
            _i2_path, (1, _i2_right_figure_line)
        )
        if not _i2_right_figure_finding:
            print(
                "  HEADLINE-LOCK PASS: (i2) the current headline followed by an arrow and a "
                "coverage-shaped figure is NOT reported as a finding — exempt as expected"
            )
        else:
            print(
                "  HEADLINE-LOCK FAIL: (i2) a genuine right-direction delta (current figure "
                "→ another coverage reading) was reported as a finding — the narrowing "
                "deleted the right-hand orientation instead of tightening it"
            )
            wrong_results.append(
                "HEADLINE-LOCK: (i2) right-direction figure exemption failed"
            )

    # (i3) Hit-detection controls (WR-06, Phase 10 review). These drive `_headline_hits()`
    # itself — the function every per-surface assertion and the (j) scan collect their hits
    # through — rather than the classifier (i)/(i2) exercise.
    #   Arm 1 (multi-line comment): the strip that removes complete HTML comments used to run
    #   per LINE, inside the classifier, so a perfectly ordinary block comment stating the
    #   headline across three lines was reported by the tree-wide scan as a current-fact
    #   statement — a fail-closed defect, but one that breaks CI on a legitimate edit with a
    #   message naming the wrong problem. The strip now runs over WHOLE FILE TEXT in
    #   `_headline_hits()`, and this arm requires a headline commented out that way to produce
    #   no hit while a real statement two lines later still does, AT ITS ORIGINAL LINE NUMBER
    #   (the strip preserves line count precisely so findings stay citable).
    #   Arm 2 (anti-tautology): the identical text with the comment markers replaced by plain
    #   words must produce BOTH hits — without it, arm 1 would also pass against a
    #   `_headline_hits()` that had simply stopped matching.
    _i3_commented = "\n".join(
        (
            "<!--",
            f"An old note: {_prose}",
            _HTML_COMMENT_CLOSE,
            f"Current: {_prose}",
        )
    )
    _i3_uncommented = "\n".join(
        (
            "(comment opens here)",
            f"An old note: {_prose}",
            "(comment closes here)",
            f"Current: {_prose}",
        )
    )
    #   Arm 3 (digit boundary, WR-08): a longer digit run that merely EMBEDS the current
    #   slash rendering is not a headline occurrence. Unbounded substring matching reported
    #   `build 1161/91/0/2521 was fine` as a hit, which on any docs/*.md line would produce an
    #   unregistered-surface FAIL naming a line that does not state the headline at all.
    #   Arm 4 (anti-tautology for arm 3): the bare rendering on an otherwise similar line must
    #   still be found, so arm 3 cannot pass against a matcher that stopped matching.
    _i3_commented_hits = [_lineno for _lineno, _ in _headline_hits(_i3_commented)]
    _i3_uncommented_hits = [_lineno for _lineno, _ in _headline_hits(_i3_uncommented)]
    if _i3_commented_hits == [4]:
        print(
            "  HEADLINE-LOCK PASS: (i3) a headline inside a complete multi-line HTML comment "
            "produces no hit, while a real statement below it is still found at its original "
            "line number (4) — comment stripping is whole-text and line-count preserving"
        )
    else:
        print(
            "  HEADLINE-LOCK FAIL: (i3) expected exactly one hit at line 4 for a headline "
            f"commented out across three lines; got {_i3_commented_hits}"
        )
        wrong_results.append("HEADLINE-LOCK: (i3) multi-line comment arm failed")
    if _i3_uncommented_hits == [2, 4]:
        print(
            "  HEADLINE-LOCK PASS: (i3) anti-tautology arm — the same text without comment "
            "markers produces both hits (lines 2 and 4), so arm 1 is not passing against a "
            "scanner that stopped matching"
        )
    else:
        print(
            "  HEADLINE-LOCK FAIL: (i3) anti-tautology arm — expected hits at lines [2, 4] "
            f"for the uncommented text; got {_i3_uncommented_hits}"
        )
        wrong_results.append("HEADLINE-LOCK: (i3) anti-tautology arm failed")

    _i3_embedded = f"build 1{_slash}1 was fine"
    _i3_bare = f"build {_slash} was fine"
    _i3_embedded_hits = _headline_hits(_i3_embedded)
    _i3_bare_hits = [_lineno for _lineno, _ in _headline_hits(_i3_bare)]
    if not _i3_embedded_hits:
        print(
            "  HEADLINE-LOCK PASS: (i3) a longer digit run embedding the current slash "
            "rendering is NOT reported as a headline occurrence — the literals are matched "
            "with a digit boundary, not as unbounded substrings"
        )
    else:
        print(
            "  HEADLINE-LOCK FAIL: (i3) a longer digit run embedding the current slash "
            f"rendering was reported as a headline occurrence: {_i3_embedded_hits}"
        )
        wrong_results.append("HEADLINE-LOCK: (i3) digit-boundary arm failed")
    if _i3_bare_hits == [1]:
        print(
            "  HEADLINE-LOCK PASS: (i3) anti-tautology arm — the bare slash rendering on an "
            "otherwise identical line IS found, so the digit boundary did not simply disable "
            "matching"
        )
    else:
        print(
            "  HEADLINE-LOCK FAIL: (i3) anti-tautology arm — expected the bare slash "
            f"rendering to be found at line 1; got {_i3_bare_hits}"
        )
        wrong_results.append("HEADLINE-LOCK: (i3) digit-boundary anti-tautology arm failed")
    return ("f", "f2", "g", "h", "h2", "i", "i2", "i3")


def _headline_lock_scan(wrong_results: list[str]) -> tuple[str, ...]:
    """HEADLINE-LOCK stage 3 — blocks (j)-(m): the tree-wide unregistered-surface scan, its
    two derived floors, and the non-vacuity and permanent controls behind them.

    Returns the block labels it ran; see `_headline_lock_preamble()` for why.
    """
    _ctx = _headline_lock_context()
    _slash, _prose = _ctx.slash, _ctx.prose

    # (j) Tree-wide unregistered-surface scan (HEADLINE-05). Collect files through the
    # shared _headline_scan_files() helper (also driven directly by block (l)'s
    # non-vacuity control) so glob expansion is never a parallel copy. The read itself
    # goes through the shared _headline_scan_read() helper (BL-02 fix) — the single
    # source of truth for what was actually opened, never re-derived from a separate
    # is_file() sweep.
    _scan_files: list[Path] = _headline_scan_files(HEADLINE_SCAN_GLOBS)

    _scan_ok = True
    _scan_result = _headline_scan_read(_scan_files)
    for _finding_relpath, _finding_msg in _scan_result.findings:
        print(f"  HEADLINE-LOCK FAIL: (j) {_finding_msg}")
        wrong_results.append(f"HEADLINE-LOCK: (j) {_finding_msg}")
        _scan_ok = False
    for _err_path, _err_reason in _scan_result.read_errors:
        print(f"  HEADLINE-LOCK FAIL: (j) {_err_path} {_err_reason}")
        wrong_results.append(f"HEADLINE-LOCK: (j) {_err_path} read error")
        _scan_ok = False
    for _skip_path, _skip_reason in _scan_result.skipped:
        print(f"  HEADLINE-LOCK INFO: (j) skipped {_skip_path} — {_skip_reason}")

    _scanned_count = len(_scan_result.read_relpaths)
    _total_non_historical_hits = sum(_scan_result.hits_by_surface.values())

    # (j-floor) Coverage floor and accounted-hit floor (CR-01 fix, BL-02 fix): the scan must
    # have actually READ every registered-plus-exempt surface and accounted for at least one
    # non-historical hit per registered surface, or the PASS line below is vacuous — a
    # narrowed or emptied HEADLINE_SCAN_GLOBS, or a registered surface the loop silently
    # declined to open, must be caught here, not stay silently green. Evaluated through the
    # shared _headline_scan_floor_breaches() helper, driven by what _headline_scan_read()
    # actually read — never a separate is_file() sweep — before the PASS branch, so the PASS
    # branch can never be reached vacuously.
    if _scan_ok:
        for _breach in _headline_scan_floor_breaches(_scan_result):
            print(f"  HEADLINE-LOCK FAIL: {_breach}")
            wrong_results.append(f"HEADLINE-LOCK: {_breach}")
            _scan_ok = False

    if _scan_ok:
        _reachable_surfaces = COVERED_HEADLINE_SURFACES | HISTORICAL_EXEMPT_FILES
        _reached_count = len(_reachable_surfaces & _scan_result.read_relpaths)
        print(
            f"  HEADLINE-LOCK PASS: (j) tree-wide scan read {_scanned_count} files, "
            f"{_total_non_historical_hits} non-historical occurrence(s) accounted for by registered "
            f"surfaces, both floors evaluated, {_reached_count} of "
            f"{len(_reachable_surfaces)} registered-plus-exempt paths reached, "
            f"{len(_scan_result.skipped)} skipped"
        )

    # (k) Non-vacuity control for (j) (T-10-08). Preconditions are asserted explicitly so
    # this control cannot silently degrade into a tautology if a future edit changes a
    # constant. Writes nothing to disk — no tempfile, no fixture file, no touch of the tree.
    _synth_path = "docs/synthetic-unregistered-surface.md"
    _synth_line = f"This document states the coverage headline: {_prose}."
    if _synth_path in COVERED_HEADLINE_SURFACES:
        print(
            "  HEADLINE-LOCK FAIL: (k) precondition violated — synthetic path is in "
            "COVERED_HEADLINE_SURFACES"
        )
        wrong_results.append("HEADLINE-LOCK: (k) precondition violated (covered)")
    elif _synth_path in HISTORICAL_EXEMPT_FILES:
        print(
            "  HEADLINE-LOCK FAIL: (k) precondition violated — synthetic path is in "
            "HISTORICAL_EXEMPT_FILES"
        )
        wrong_results.append("HEADLINE-LOCK: (k) precondition violated (whole-file)")
    elif _is_historical_headline_hit(_synth_path, _synth_line):
        # WR-04: delegates to the classifier directly rather than a parallel whole-line
        # substring test, so this precondition rejects exactly the lines the classifier
        # would exempt and no others. Distinct from the "direction" assertions below, which
        # exercise _unregistered_headline_finding() — never the same call twice.
        print(
            "  HEADLINE-LOCK FAIL: (k) precondition violated — the classifier already calls "
            "the synthetic line historical, so direction 1 would prove nothing"
        )
        wrong_results.append("HEADLINE-LOCK: (k) precondition violated (already historical)")
    else:
        # Direction 1: the synthetic unregistered hit IS reported as a finding, naming the
        # synthetic path.
        _unreg_finding, _unreg_msg = _unregistered_headline_finding(
            _synth_path, (1, _synth_line)
        )
        # Direction 2 precondition (WR-02): build the candidate list as the sorted
        # difference of the two registered/exempt sets rather than indexing the bare
        # sorted registered-surfaces set directly — an empty COVERED_HEADLINE_SURFACES
        # must report a named precondition failure instead of raising IndexError, and if
        # the alphabetically-first registered surface were ever also whole-file exempt,
        # this direction would pass through the classifier gate rather than the
        # registration gate and prove nothing about registration while still printing PASS.
        _k_registered_candidates = sorted(COVERED_HEADLINE_SURFACES - HISTORICAL_EXEMPT_FILES)
        if not _k_registered_candidates:
            print(
                "  HEADLINE-LOCK FAIL: (k) precondition violated — no registered, "
                "non-whole-file-exempt surface available for direction 2"
            )
            wrong_results.append(
                "HEADLINE-LOCK: (k) precondition violated (no registered path)"
            )
        else:
            # Direction 2: the SAME synthetic line attributed to a REGISTERED path is NOT
            # reported — otherwise the decision function would simply flag everything and
            # the scan's greenness on the live tree would be luck, not correctness.
            _registered_path = _k_registered_candidates[0]
            _reg_finding, _ = _unregistered_headline_finding(
                _registered_path, (1, _synth_line)
            )
            # Direction 3 (T-10-08 / ROADMAP criterion 5's "gated behind HEADLINE-03"
            # clause): a genuinely delta-shaped line — a fixed superseded figure, an arrow,
            # then the current slash rendering (built from the in-scope _slash local, never
            # typed) — at the SAME unregistered synthetic path, is NOT reported. This
            # proves the scan is gated behind the historical classifier and not merely a
            # registered-surface membership test. The left-hand figure is a fixed
            # non-current placeholder; it is not the headline and does not fall under the
            # no-literal rule.
            _delta_line = f"{_SUPERSEDED_PLACEHOLDER} → {_slash}"
            if not _is_historical_headline_hit(_synth_path, _delta_line):
                print(
                    "  HEADLINE-LOCK FAIL: (k) precondition violated — the delta-shaped "
                    "line is not classified historical, so direction 3 would prove nothing"
                )
                wrong_results.append(
                    "HEADLINE-LOCK: (k) precondition violated (delta-shaped)"
                )
            else:
                _delta_finding, _ = _unregistered_headline_finding(
                    _synth_path, (1, _delta_line)
                )
                if (
                    _unreg_finding
                    and _synth_path in _unreg_msg
                    and not _reg_finding
                    and not _delta_finding
                ):
                    print(
                        f"  HEADLINE-LOCK PASS: (k) synthetic unregistered surface "
                        f"{_synth_path} is reported as a finding, the same line at a "
                        f"registered surface is not, and a delta-shaped line at the same "
                        f"synthetic path is not — non-vacuous and gated behind HEADLINE-03"
                    )
                else:
                    print(
                        f"  HEADLINE-LOCK FAIL: (k) non-vacuity control for the tree-wide "
                        f"scan did not behave as expected (unregistered finding="
                        f"{_unreg_finding}, registered finding={_reg_finding}, "
                        f"delta-shaped finding={_delta_finding})"
                    )
                    wrong_results.append(
                        "HEADLINE-LOCK: (k) non-vacuity control did not behave as expected"
                    )

    # (l) Non-vacuity control for the (j-floor) coverage/hit floors (CR-01, WR-09, T-10-09).
    # Unlike (k), which exercises _unregistered_headline_finding() in isolation, arms 1 and 2
    # drive the REAL _headline_scan_files() AND _headline_scan_read() — the same function
    # objects (j) calls — with alternative glob lists, so glob expansion, the real read path
    # and relative_to() path derivation are all genuinely exercised (not a hand-built
    # simulation of the detection function, per the research's Pitfall 4 concern). Writes
    # nothing to disk: Path.glob over the existing tree plus in-memory set arithmetic. Arm 3
    # is anti-tautology only (WR-09) and does not re-run the live glob path — (j-floor)
    # above already owns the live verdict, and re-deriving it here would append one defect
    # to wrong_results twice under two labels.
    _l_reachable = COVERED_HEADLINE_SURFACES | HISTORICAL_EXEMPT_FILES

    def _l_reached_paths(files: list[Path]) -> set[str]:
        """GLOB-reach (which candidates the glob list matches), via the shared
        _scan_relpaths() helper — a different, weaker question than READ-reach, which the
        floor breaches below derive from _headline_scan_read() instead. Used only for these
        arms' own "does narrowing reduce candidate reach" preconditions, never for a floor
        input (IN-08: one relpath comprehension in the module, inside _scan_relpaths()).
        """
        return _scan_relpaths(files) & _l_reachable

    # Reuses _scan_files (already collected by block (j)) rather than a second live call to
    # _headline_scan_files() (IN-08).
    _l_live_reached = _l_reached_paths(_scan_files)

    # Arm 1: empty-globs (the CR-01 reproduction, permanently encoded). A control that only
    # asserted "non-empty" would pass against a floor that reported a generic message, so
    # this requires the breach to name a specific registered surface. WR-02: the candidate
    # surface is selected only after an explicit, named precondition confirms the
    # registered-surfaces set is non-empty — indexing its sorted form directly would raise
    # IndexError out of --self-test rather than reporting a finding.
    _l_empty_files = _headline_scan_files([])
    _l_empty_read = _headline_scan_read(_l_empty_files)
    _l_empty_breaches = _headline_scan_floor_breaches(_l_empty_read)
    _l_registered_candidates = sorted(COVERED_HEADLINE_SURFACES)
    if not _l_registered_candidates:
        print(
            "  HEADLINE-LOCK FAIL: (l) empty-globs arm precondition violated — "
            "COVERED_HEADLINE_SURFACES is empty, arm 1 would prove nothing"
        )
        wrong_results.append(
            "HEADLINE-LOCK: (l) empty-globs arm precondition violated (empty)"
        )
    else:
        _l_named_surface = _l_registered_candidates[0]
        if _l_empty_breaches and any(_l_named_surface in _b for _b in _l_empty_breaches):
            print(
                "  HEADLINE-LOCK PASS: (l) empty-globs arm — an emptied glob list drives "
                f"the real collection and read helpers to a non-empty breach naming a "
                f"registered surface ({_l_named_surface})"
            )
        else:
            print(
                "  HEADLINE-LOCK FAIL: (l) empty-globs arm — an emptied glob list did not "
                "produce a breach naming a registered surface"
            )
            wrong_results.append("HEADLINE-LOCK: (l) empty-globs arm failed")

    # Arm 2: narrowed-globs (the "narrowing typo" case, e.g. a well-meaning "temporarily
    # narrow the scan" edit). Proves the floor degrades proportionally rather than only
    # detecting total absence. Precondition asserted explicitly, following (i)/(k): the
    # narrowed glob must genuinely reach fewer registered-or-exempt paths than the live
    # globs, or this arm would prove nothing.
    _l_narrow_globs = ["CHANGELOG.md"]
    _l_narrow_files = _headline_scan_files(_l_narrow_globs)
    _l_narrow_read = _headline_scan_read(_l_narrow_files)
    _l_narrow_reached = _l_reached_paths(_l_narrow_files)
    if len(_l_narrow_reached) >= len(_l_live_reached):
        print(
            "  HEADLINE-LOCK FAIL: (l) narrowed-globs arm — precondition violated, the "
            "narrowed glob list does not reach fewer registered-or-exempt paths than the "
            "live globs"
        )
        wrong_results.append("HEADLINE-LOCK: (l) narrowed-globs arm precondition violated")
    else:
        _l_narrow_breaches = _headline_scan_floor_breaches(_l_narrow_read)
        _l_missing = sorted(_l_reachable - _l_narrow_reached)
        _l_breach_text = " ".join(_l_narrow_breaches)
        if _l_narrow_breaches and all(_m in _l_breach_text for _m in _l_missing):
            print(
                "  HEADLINE-LOCK PASS: (l) narrowed-globs arm — a single-pattern glob list "
                f"drives the real collection and read helpers to a breach naming every "
                f"registered-or-exempt surface it cannot reach ({_l_missing})"
            )
        else:
            print(
                "  HEADLINE-LOCK FAIL: (l) narrowed-globs arm — breach list did not name "
                f"every unreachable registered-or-exempt surface ({_l_missing})"
            )
            wrong_results.append("HEADLINE-LOCK: (l) narrowed-globs arm failed")

    # Arm 3: anti-tautology only (WR-09). Feeds the floor helper a synthetic input already
    # known to satisfy both floors — a read set equal to every registered-plus-exempt
    # surface, and a hit map giving each registered surface exactly one hit, constructed as
    # an explicit _HeadlineScanRead because that record is the only shape the helper accepts
    # (CR-01) — and requires an EMPTY breach list. Without this arm, arms 1 and 2 would also pass against a floor
    # helper that returned a breach unconditionally. This arm deliberately does not re-run
    # the live glob path: (j-floor) above already owns that live verdict, and arms 1/2
    # above already genuinely exercise glob expansion and the real read path.
    _l_synthetic_read = _HeadlineScanRead(
        read_relpaths=set(_l_reachable),
        hits_by_surface={_surface: 1 for _surface in COVERED_HEADLINE_SURFACES},
        findings=[],
        skipped=[],
        read_errors=[],
    )
    _l_synthetic_breaches = _headline_scan_floor_breaches(_l_synthetic_read)
    if not _l_synthetic_breaches:
        print(
            "  HEADLINE-LOCK PASS: (l) anti-tautology arm — a synthetic read result "
            f"already satisfying both floors ({len(_l_reachable)} registered-plus-exempt "
            "paths, one hit per registered surface) produces zero breaches"
        )
    else:
        print(
            "  HEADLINE-LOCK FAIL: (l) anti-tautology arm — a synthetic read result "
            f"already satisfying both floors still produced breaches "
            f"({_l_synthetic_breaches})"
        )
        wrong_results.append("HEADLINE-LOCK: (l) anti-tautology arm failed")

    # (m) Permanent controls for both halves of the BL-02 escape (T-10-09). Every arm drives
    # _headline_scan_read() or _headline_scan_floor_breaches() — the same function objects
    # block (j) calls — and every arm is pure in-memory set/dict arithmetic. Writes nothing
    # to disk, creates no tempfile.

    # Arm 1: silently-skipped registered surface (BL-02 half one). The shipped code computed
    # reachability from a glob-based is_file() sweep that followed symlinks, so a surface the
    # loop refused to read was counted as "reached" and the PASS line printed a full-coverage
    # claim it had not verified. Removes one registered surface from a COPY of the live read
    # result's read_relpaths (leaving the real _scan_result untouched) and requires the floor
    # helper to breach naming it. The precondition — the chosen surface must actually be
    # present in the live read set — is asserted explicitly, and an empty
    # COVERED_HEADLINE_SURFACES reports a named precondition failure rather than raising.
    _m_arm1_candidates = sorted(COVERED_HEADLINE_SURFACES)
    if not _m_arm1_candidates:
        print(
            "  HEADLINE-LOCK FAIL: (m) arm 1 precondition violated — "
            "COVERED_HEADLINE_SURFACES is empty, arm 1 would prove nothing"
        )
        wrong_results.append("HEADLINE-LOCK: (m) arm 1 precondition violated (empty)")
    else:
        _m_removed_surface = _m_arm1_candidates[0]
        if _m_removed_surface not in _scan_result.read_relpaths:
            print(
                f"  HEADLINE-LOCK FAIL: (m) arm 1 precondition violated — "
                f"{_m_removed_surface!r} is absent from the live read_relpaths, arm 1 "
                "would prove nothing"
            )
            wrong_results.append("HEADLINE-LOCK: (m) arm 1 precondition violated (absent)")
        else:
            _m_arm1_read = _scan_result._replace(
                read_relpaths=_scan_result.read_relpaths - {_m_removed_surface}
            )
            _m_arm1_breaches = _headline_scan_floor_breaches(_m_arm1_read)
            if _m_arm1_breaches and any(
                _m_removed_surface in _b for _b in _m_arm1_breaches
            ):
                print(
                    "  HEADLINE-LOCK PASS: (m) arm 1 — a registered surface silently "
                    f"absent from read_relpaths ({_m_removed_surface}) is caught by the "
                    "coverage floor, naming that surface"
                )
            else:
                print(
                    "  HEADLINE-LOCK FAIL: (m) arm 1 — a registered surface silently "
                    f"absent from read_relpaths ({_m_removed_surface}) was NOT caught by "
                    "the coverage floor"
                )
                wrong_results.append("HEADLINE-LOCK: (m) arm 1 failed")

    # Arm 2: starved surface masked by a spare hit (BL-02 half two). Measured fact: on the
    # live tree, docs/requirements-traceability.md alone contributes two non-historical
    # hits, so a running-total floor has exactly one unit of slack — any single registered
    # surface can go entirely unread today and the running total still meets the old
    # threshold. Builds a hit map giving one registered surface zero hits and moving those
    # hits onto a DIFFERENT registered surface, so the TOTAL is unchanged and still meets or
    # exceeds the old running-total threshold — asserted explicitly as a precondition, or the
    # arm would prove nothing against a restored running-total floor.
    _m_arm2_surfaces = sorted(COVERED_HEADLINE_SURFACES)
    if len(_m_arm2_surfaces) < 2:
        print(
            "  HEADLINE-LOCK FAIL: (m) arm 2 precondition violated — fewer than two "
            "registered surfaces, arm 2 would prove nothing"
        )
        wrong_results.append("HEADLINE-LOCK: (m) arm 2 precondition violated (too few)")
    else:
        _m_starved_surface = _m_arm2_surfaces[0]
        _m_donor_surface = _m_arm2_surfaces[1]
        _m_arm2_hits = dict(_scan_result.hits_by_surface)
        _m_starved_amount = _m_arm2_hits.get(_m_starved_surface, 0)
        _m_arm2_hits[_m_starved_surface] = 0
        _m_arm2_hits[_m_donor_surface] = (
            _m_arm2_hits.get(_m_donor_surface, 0) + _m_starved_amount
        )
        _m_arm2_total = sum(_m_arm2_hits.get(_s, 0) for _s in _m_arm2_surfaces)
        if _m_arm2_total < len(COVERED_HEADLINE_SURFACES):
            print(
                "  HEADLINE-LOCK FAIL: (m) arm 2 precondition violated — the constructed "
                f"total ({_m_arm2_total}) does not meet or exceed the old running-total "
                f"threshold ({len(COVERED_HEADLINE_SURFACES)}), arm 2 would prove nothing "
                "against a restored running-total floor"
            )
            wrong_results.append("HEADLINE-LOCK: (m) arm 2 precondition violated (total)")
        else:
            _m_arm2_breaches = _headline_scan_floor_breaches(
                _scan_result._replace(hits_by_surface=_m_arm2_hits)
            )
            if _m_arm2_breaches and any(
                _m_starved_surface in _b for _b in _m_arm2_breaches
            ):
                print(
                    "  HEADLINE-LOCK PASS: (m) arm 2 — a registered surface starved of "
                    f"hits ({_m_starved_surface}) while the running total stays unchanged "
                    f"(masked by {_m_donor_surface}'s spare hit) is caught by the "
                    "per-surface accounted-hit floor"
                )
            else:
                print(
                    "  HEADLINE-LOCK FAIL: (m) arm 2 — a starved registered surface masked "
                    f"by a spare hit ({_m_starved_surface}) was NOT caught by the "
                    "accounted-hit floor"
                )
                wrong_results.append("HEADLINE-LOCK: (m) arm 2 failed")

    # Arm 3: skip visibility (anti-tautology for arms 1 and 2, and the loop-side half of the
    # property). Without this arm, arms 1 and 2 would also pass against a read loop that
    # silently dropped everything, because both construct their inputs by hand rather than
    # driving the loop itself.
    _m_skip_candidate = REPO_ROOT / "docs"  # a directory, not a regular file
    _m_arm3_result = _headline_scan_read([_m_skip_candidate])
    _m_arm3_skip_paths = {_p for _p, _reason in _m_arm3_result.skipped}
    if not _m_arm3_result.read_relpaths and str(_m_skip_candidate) in _m_arm3_skip_paths:
        print(
            "  HEADLINE-LOCK PASS: (m) arm 3 — a non-regular-file candidate is named in "
            "skipped and absent from read_relpaths — the read loop cannot silently drop a "
            "candidate"
        )
    else:
        print(
            "  HEADLINE-LOCK FAIL: (m) arm 3 — a non-regular-file candidate was not "
            "correctly recorded as skipped"
        )
        wrong_results.append("HEADLINE-LOCK: (m) arm 3 failed")

    # Arm 4: symlink confinement, and the loop's positive counterpart (WR-02, Phase 10
    # review). The `is_relative_to()` guard is this module's ONLY path-confinement check —
    # the thing that stops a symlinked docs/*.md from making the scan read outside the
    # repository — and deleting its four lines outright left --self-test at exit 0, because
    # arm 3 above exercises only the OTHER decline reason ("not a regular file", via a
    # directory). This arm drives the identical _headline_scan_read() function object over a
    # throwaway tree, passing that tree as `root`, so the escape can be built without writing
    # anything inside the repository: `inside.md` is a plain file under the root, `escape.md`
    # is a symlink under the root whose target resolves OUTSIDE it. Asserting both in one
    # call is what keeps the arm honest — the confinement half alone would also pass against
    # a read loop that declined everything.
    with tempfile.TemporaryDirectory() as _m_arm4_tmp:
        _m_arm4_root = Path(_m_arm4_tmp) / "root"
        _m_arm4_root.mkdir()
        _m_arm4_inside = _m_arm4_root / "inside.md"
        _m_arm4_inside.write_text("A plain in-root surface with no headline.\n", encoding="utf-8")
        _m_arm4_outside = Path(_m_arm4_tmp) / "outside.md"
        _m_arm4_outside.write_text("An out-of-root surface with no headline.\n", encoding="utf-8")
        _m_arm4_link = _m_arm4_root / "escape.md"
        try:
            _m_arm4_link.symlink_to(_m_arm4_outside)
        except OSError as _m_arm4_symlink_exc:
            print(
                "  HEADLINE-LOCK FAIL: (m) arm 4 precondition violated — this platform "
                f"could not create a symlink ({_m_arm4_symlink_exc}), so the confinement "
                "guard cannot be exercised"
            )
            wrong_results.append("HEADLINE-LOCK: (m) arm 4 precondition violated (symlink)")
        else:
            # Precondition: the escaping candidate must look like a regular file, or the
            # loop would decline it for the OTHER reason and this arm would prove nothing.
            if not _m_arm4_link.is_file():
                print(
                    "  HEADLINE-LOCK FAIL: (m) arm 4 precondition violated — the symlinked "
                    "candidate does not report is_file(), so it would be declined as 'not a "
                    "regular file' rather than by the confinement guard"
                )
                wrong_results.append("HEADLINE-LOCK: (m) arm 4 precondition violated (is_file)")
            else:
                _m_arm4_result = _headline_scan_read(
                    [_m_arm4_inside, _m_arm4_link], root=_m_arm4_root
                )
                _m_arm4_skips = {
                    _p: _reason for _p, _reason in _m_arm4_result.skipped
                }
                _m_arm4_confined = (
                    _m_arm4_skips.get(str(_m_arm4_link)) == "resolves outside REPO_ROOT"
                    and _m_arm4_result.read_relpaths == {"inside.md"}
                    and not _m_arm4_result.read_errors
                )
                if _m_arm4_confined:
                    print(
                        "  HEADLINE-LOCK PASS: (m) arm 4 — a symlinked candidate resolving "
                        "outside the scan root is named in skipped with the confinement "
                        "reason and absent from read_relpaths, while a plain in-root file in "
                        "the same call IS read — the confinement guard is load-bearing"
                    )
                else:
                    print(
                        "  HEADLINE-LOCK FAIL: (m) arm 4 — expected the symlinked candidate "
                        "to be skipped as 'resolves outside REPO_ROOT' and only 'inside.md' "
                        f"to be read; got skipped={_m_arm4_result.skipped}, "
                        f"read_relpaths={sorted(_m_arm4_result.read_relpaths)}, "
                        f"read_errors={_m_arm4_result.read_errors}"
                    )
                    wrong_results.append("HEADLINE-LOCK: (m) arm 4 failed")

    # Arm 5: read-error visibility (WR-03, Phase 10 review). The explicit
    # UnicodeDecodeError / OSError split is the only thing in this gate that turns an I/O
    # failure into a FAIL rather than a silent skip, and nothing asserted it: replacing both
    # handlers with a bare `except Exception: continue` — the textbook fail-open in a gate
    # whose brief is to fail closed — left --self-test at exit 0. The coverage floor catches
    # that swallow only for registered or exempt surfaces; an undecodable UNREGISTERED
    # docs/*.md would drop from FAIL to invisible with no control noticing. This arm drives
    # the identical function object over a throwaway tree (same `root` mechanism as arm 4)
    # containing one undecodable file and one valid file, and requires the undecodable one in
    # `read_errors` — absent from BOTH `read_relpaths` and `skipped`, since a swallow that
    # merely re-labelled the failure as a skip would be the same fail-open — while the valid
    # file in the same call is read. Only the decode branch is driven: an OSError cannot be
    # provoked portably here (a chmod-based fixture is a no-op for a root-privileged runner,
    # and a dangling symlink is declined by is_file() before the read), and the fail-open
    # rewrite this arm exists to catch removes both handlers together.
    with tempfile.TemporaryDirectory() as _m_arm5_tmp:
        _m_arm5_root = Path(_m_arm5_tmp)
        _m_arm5_valid = _m_arm5_root / "valid.md"
        _m_arm5_valid.write_text("A decodable in-root surface with no headline.\n", encoding="utf-8")
        _m_arm5_undecodable = _m_arm5_root / "undecodable.md"
        _m_arm5_undecodable.write_bytes(b"\xff\xfe headline")
        _m_arm5_result = _headline_scan_read(
            [_m_arm5_valid, _m_arm5_undecodable], root=_m_arm5_root
        )
        _m_arm5_errors = {_p: _reason for _p, _reason in _m_arm5_result.read_errors}
        _m_arm5_skips = {_p for _p, _reason in _m_arm5_result.skipped}
        _m_arm5_ok = (
            "could not be decoded as UTF-8"
            in _m_arm5_errors.get(str(_m_arm5_undecodable), "")
            and str(_m_arm5_undecodable) not in _m_arm5_skips
            and _m_arm5_result.read_relpaths == {"valid.md"}
        )
        if _m_arm5_ok:
            print(
                "  HEADLINE-LOCK PASS: (m) arm 5 — an undecodable candidate is named in "
                "read_errors (not skipped, not read) while a valid file in the same call IS "
                "read — an I/O failure cannot be swallowed into a silent skip"
            )
        else:
            print(
                "  HEADLINE-LOCK FAIL: (m) arm 5 — expected the undecodable candidate in "
                "read_errors and only 'valid.md' to be read; got "
                f"read_errors={_m_arm5_result.read_errors}, "
                f"skipped={_m_arm5_result.skipped}, "
                f"read_relpaths={sorted(_m_arm5_result.read_relpaths)}"
            )
            wrong_results.append("HEADLINE-LOCK: (m) arm 5 failed")

    # Arm 6: the sentinel's OWN read guard (CN-03, Phase 10 review). Arm 5 above covers the
    # tree-wide scan's read loop; this arm covers `_headline_read_or_fail()`, the same policy
    # applied to the five live-file reads the sentinel makes directly, which were unguarded
    # until this review (a permission change or a non-UTF-8 byte in any of them exited
    # --self-test with a traceback rather than a finding). Both halves are asserted against a
    # THROWAWAY wrong_results list, so the control cannot contaminate the real one, and the
    # helper's own FAIL line is captured rather than printed — a run in which every assertion
    # passes must not emit a FAIL line, and capturing it lets the arm assert the line was
    # emitted at all, not merely that the finding was appended.
    with tempfile.TemporaryDirectory() as _m_arm6_tmp:
        _m_arm6_valid = Path(_m_arm6_tmp) / "valid.md"
        _m_arm6_valid.write_text("readable\n", encoding="utf-8")
        _m_arm6_broken = Path(_m_arm6_tmp) / "broken.md"
        _m_arm6_broken.write_bytes(b"\xff\xfe headline")
        _m_arm6_findings: list[str] = []
        _m_arm6_captured = io.StringIO()
        with contextlib.redirect_stdout(_m_arm6_captured):
            _m_arm6_good = _headline_read_or_fail(
                _m_arm6_valid, "(m) arm 6 valid", _m_arm6_findings
            )
            _m_arm6_bad = _headline_read_or_fail(
                _m_arm6_broken, "(m) arm 6 broken", _m_arm6_findings
            )
        _m_arm6_output = _m_arm6_captured.getvalue()
        _m_arm6_ok = (
            _m_arm6_good == "readable\n"
            and _m_arm6_bad is None
            and _m_arm6_findings == [
                "HEADLINE-LOCK: (m) arm 6 broken could not be decoded as UTF-8"
            ]
            and "HEADLINE-LOCK FAIL: (m) arm 6 broken" in _m_arm6_output
        )
        if _m_arm6_ok:
            print(
                "  HEADLINE-LOCK PASS: (m) arm 6 — the sentinel's own read guard returns the "
                "text of a readable file appending nothing, and converts an undecodable one "
                "into exactly one named finding plus a printed FAIL line, never a traceback"
            )
        else:
            print(
                "  HEADLINE-LOCK FAIL: (m) arm 6 — the sentinel's own read guard did not "
                f"behave as specified: returned {_m_arm6_good!r} / {_m_arm6_bad!r}, "
                f"appended {_m_arm6_findings}, printed {_m_arm6_output!r}"
            )
            wrong_results.append("HEADLINE-LOCK: (m) arm 6 failed")
    return ("j", "k", "l", "m")


def _headline_lock_doc_rows(wrong_results: list[str]) -> tuple[str, ...]:
    """HEADLINE-LOCK stage 4 — block (n): the TRACE-03 doc-row transcription lock.

    Depends on no context: it reads module constants and the two rows only. Returns the block
    labels it ran; see `_headline_lock_preamble()` for why.
    """
    # (n) Doc-row transcription lock (WR-06): the two hand-maintained TRACE-03 rows transcribe
    # HEADLINE_SCAN_GLOBS' live value by hand. Nothing previously compared them — this is the
    # exact drift class HEADLINE-LOCK exists to catch, newly created by the fix for it, and
    # the two copies had already diverged once inside this phase. Rendered the same way the
    # rows already state it (a comma-joined sequence of backtick-quoted patterns) so the lock
    # goes green on today's text without any doc edit — derived from the constant, never typed
    # as a literal here, exactly as every other assertion in this sentinel derives from
    # build_matrix_rows().
    _n_glob_prose = ", ".join(f"`{_g}`" for _g in HEADLINE_SCAN_GLOBS)
    _n_row_prefix = "| TRACE-03 "

    def _n_trace03_row(relpath: str) -> str | None:
        """The single TRACE-03 table row in `relpath`, or None (with a named FAIL already
        recorded) when the file is missing or does not carry exactly one.

        Scoping to the row is what makes this a transcription lock rather than a whole-file
        containment test (WR-04, Phase 10 review): the previous form searched the entire
        file, so any future mention of the glob list ANYWHERE in CLAUDE.md or
        docs/ARCHITECTURE.md — a new note, an appendix — would let the TRACE-03 row's own
        transcription drift to anything at all while (n) stayed green, which is precisely the
        drift class this block was added to close. A file carrying zero or several TRACE-03
        rows is a FAIL, never a silent skip, because "which row do I lock" would otherwise
        have no answer.
        """
        _path = REPO_ROOT / relpath
        if not _path.is_file():
            print(f"  HEADLINE-LOCK FAIL: (n) {_path} not found")
            wrong_results.append(f"HEADLINE-LOCK: (n) {relpath} missing")
            return None
        _text = _headline_read_or_fail(_path, f"(n) {relpath}", wrong_results)
        if _text is None:
            return None
        _rows = [
            _line for _line in _text.splitlines() if _line.startswith(_n_row_prefix)
        ]
        if len(_rows) != 1:
            print(
                f"  HEADLINE-LOCK FAIL: (n) {relpath} carries {len(_rows)} lines beginning "
                f"{_n_row_prefix!r} — expected exactly one TRACE-03 row to lock"
            )
            wrong_results.append(
                f"HEADLINE-LOCK: (n) {relpath} has {len(_rows)} TRACE-03 rows, expected 1"
            )
            return None
        return _rows[0]

    for _n_row_file in _TRACE03_DOC_ROWS:
        _n_row = _n_trace03_row(_n_row_file)
        if _n_row is None:
            continue
        if _n_glob_prose in _n_row:
            print(
                f"  HEADLINE-LOCK PASS: (n) {_n_row_file}'s TRACE-03 row transcribes "
                f"HEADLINE_SCAN_GLOBS correctly ({_n_glob_prose})"
            )
        else:
            print(
                f"  HEADLINE-LOCK FAIL: (n) {_n_row_file} does not transcribe "
                f"HEADLINE_SCAN_GLOBS (expected {_n_glob_prose!r} to appear in its TRACE-03 "
                "row)"
            )
            wrong_results.append(
                f"HEADLINE-LOCK: (n) {_n_row_file} TRACE-03 row does not transcribe "
                f"HEADLINE_SCAN_GLOBS ({_n_glob_prose})"
            )

    # Non-vacuity arm: a DELIBERATELY DIFFERENT glob list, rendered the identical way, must be
    # ABSENT from both files. Without this, a lock whose comparison always succeeded (e.g. a
    # containment test against an empty string) would be indistinguishable from a passing
    # lock — the same anti-tautology rule (b), (e), (i), (k), (l) and (m) already observe.
    _n_different_globs = ["docs/*.markdown", "CONTRIBUTING.md"]
    _n_different_prose = ", ".join(f"`{_g}`" for _g in _n_different_globs)
    _n_vacuity_rows = {
        _row_file: _n_trace03_row(_row_file)
        for _row_file in _TRACE03_DOC_ROWS
    }
    _n_vacuity_violations = [
        _row_file
        for _row_file, _row in _n_vacuity_rows.items()
        if _row is not None and _n_different_prose in _row
    ]
    if _n_vacuity_violations:
        print(
            f"  HEADLINE-LOCK FAIL: (n) non-vacuity arm — a deliberately different glob "
            f"rendering ({_n_different_prose}) was found in {_n_vacuity_violations}, so the "
            "containment test above cannot be trusted"
        )
        wrong_results.append("HEADLINE-LOCK: (n) non-vacuity arm did not fail")
    else:
        print(
            f"  HEADLINE-LOCK PASS: (n) non-vacuity arm — a deliberately different glob "
            f"rendering ({_n_different_prose}) is absent from both TRACE-03 rows "
            f"(row-scoped, not whole-file)"
        )
    return ("n",)


_HEADLINE_LOCK_STAGES: tuple = (
    _headline_lock_preamble,
    _headline_lock_surfaces,
    _headline_lock_scan,
    _headline_lock_doc_rows,
)

# Every lettered block the four stages above are jointly responsible for running, in order.
# Reconciled against what the stages report at the end of _self_test_headline_lock(): a stage
# dropped from _HEADLINE_LOCK_STAGES, or one that stops running a block it owns, is a named
# FAIL instead of a silently shorter green run (CN-04, Phase 10 review). The labels are
# self-reported by each stage, so this reconciles the DISPATCH, not the block bodies — the
# block bodies are what every other control in this sentinel already covers.
_HEADLINE_LOCK_BLOCKS: tuple[str, ...] = (
    "0", "a", "b", "c", "d", "e",
    "f", "f2", "g", "h", "h2", "i", "i2", "i3",
    "j", "k", "l", "m",
    "n",
)


def _self_test_headline_lock(wrong_results: list[str]) -> None:
    """HEADLINE-LOCK named sentinel (WR-08 / v8.18 Phase 4 review).

    Ties the three published, hand-copied or generator-written coverage surfaces back to
    build_matrix_rows(), which nothing previously did. The v8.18 review measured the gap:
    no script anywhere contained the literal headline figure, and TRACE-03's --self-test
    never re-rendered the matrix to compare it against the tracked artifacts, because the
    `emit` subcommand is a manual regeneration step that CI does not run.

    That gap is not hypothetical. The same review's CR-01 was exactly this drift: an
    `88 audit-only` figure surviving in two places six and fifty lines from a headline the
    same commit had moved to 90. It was corrected by hand, closing the instance and leaving
    the mechanism intact, so the next headline move would have reopened it identically.

    Asserts:
      (0) Preamble: COVERED_HEADLINE_SURFACES and HISTORICAL_EXEMPT_FILES are disjoint
          (WR-01, WARNING scope) — the two sets carry contradictory meanings ("must state
          the current fact" vs "never states a current fact") — and every entry in
          HISTORICAL_EXEMPT_FILES resolves to an existing file, so a stale entry cannot
          silently keep exempting a whole file's contents from both (f) and (j). As of
          WR-03, HISTORICAL_EXEMPT_FILES' MEMBERSHIP is also locked by name against a
          literal expectation set: growth or shrinkage now fails the gate naming the
          symmetric difference, so a new whole-file escape hatch — which disables both (f)
          and the tree-wide scan for that file's entire contents, permanently — requires a
          second, reviewable edit rather than a one-line change. What remains unenforced is
          the free-text justification each entry's own comment carries, not its membership.
          A final (0) assertion (IN-09) requires _SUPERSEDED_PLACEHOLDER to differ from the
          live slash rendering, so the day a real headline collides with the fixed
          placeholder used throughout (h)/(h2)/(i2)/(k), the gate says so explicitly instead
          of three controls degenerating simultaneously and silently. _TRACE03_DOC_ROWS is
          membership-locked on the same pattern (Phase 10 UAT): block (n) checks the TRACE-03
          row transcription only on the files that tuple names, so dropping one silently stops
          checking that row — measured green before this lock existed. The expectation is
          restated as a literal on purpose; deriving it from the constant would assert nothing.
      (a) Published-headline lock: docs/requirements-traceability.md states exactly the
          headline build_matrix_rows() produces. Every one of the four figures is derived
          live — including the gap count, which is NOT hardcoded to 0. Hardcoding it would
          mean that the first real gap row makes this sentinel fail while blaming the prose,
          which would be a correct document losing to a stale assertion.
      (b) Non-vacuity control for (a): the same predicate, run against a copy of the document
          with the reproducible count perturbed, must report a mismatch. Without this, a
          rewritten (a) that always passes is indistinguishable from a passing (a).
      (c) Markdown artifact freshness: docs/requirements-matrix.md on disk is byte-identical
          to render_matrix_markdown(rows). Deterministic — the renderer embeds no timestamp.
      (d) JSON artifact freshness: docs/data/matrix.json on disk is byte-identical to what
          emit_matrix writes, built through the same json.dumps(..., indent=2) over asdict.
      (e) Non-vacuity control for (c)/(d): each artifact must compare UNEQUAL against a
          rendering of a deliberately different row set (the same rows minus the last),
          produced by the same renderer (c)/(d) use. Rewritten in the Phase 10 review's CR-02
          fix, twice over: the perturbation moved from the DISK side to the LIVE side — the
          old form asserted `disk + "\n" != live`, provably true whenever (c)/(d) pass and
          therefore incapable of failing — and, more importantly, both verdicts are now read
          out of ONE shared comparison expression evaluated over the two candidate renderings,
          so a (c)/(d) comparison rewritten to be unconditionally true (`if disk is not
          None:`, the exact defect this control names) makes the perturbed verdict true as
          well and is reported here as a vacuous byte-comparison, instead of leaving the gate
          green under a "non-vacuous" PASS line. Preconditions (missing artifact, fewer than
          two rows) are named FAILs, never silent skips.
      (f) Per-surface headline presence: every surface named in COVERED_HEADLINE_SURFACES
          states the current headline in either rendering (prose or compact-slash),
          label-agnostic — this is what proves docs/COMPONENT-DIAGRAM.md is covered even
          though it only ever states the bare slash form and never the
          "**Coverage headline:**" label (a) is keyed to. Tightened in Phase 10 Plan 02
          (HEADLINE-03) to require at least one hit that
          `_is_historical_headline_hit()` does NOT call historical — a delta row or
          historical statement elsewhere in the same file must not be able to satisfy this
          on its own, so a surface whose only occurrence is a ledger delta (e.g. an arrow
          row) correctly fails here rather than passing on a technicality.
      (g) Non-vacuity control for (f): for each surface independently, perturbing its
          in-memory copy so that (f)'s tightened, non-historical-only predicate finds zero
          hits — holding every other surface's real text untouched. Sharpened in Phase 10
          Plan 02 to perturb ONLY the lines `_is_historical_headline_hit()` does NOT call
          historical, via `_perturb_non_historical_hits()`, leaving every historical/delta
          line (e.g. an arrow-marked ledger row) byte-correct in the mutated copy — this is
          a line-level, classifier-driven perturbation rather than a rendering-keyed guess
          (perturb "the prose form") because docs/requirements-traceability.md carries two
          non-historical hits in two different renderings (line 7 prose, line 99 slash
          narrative) and one historical hit in the slash rendering (line 80, arrow); a
          rendering guess cannot correctly single out just the historical line. For surfaces
          with a single, non-historical occurrence this has the same effect as plan 10-01's
          blanket perturbation. Each control's message names its own surface.
      (f2) Synthetic control for (f)'s tightening itself (WR-01, Phase 10 review). (g) tests
          the perturbation, not the tightening — reverting (f) to the untightened form left
          --self-test green — so the tightened predicate is expressed once, module level, as
          `_non_historical_headline_hits()` (the identical function object (f) and (g) call)
          and driven here by two synthetic texts that depend on no live file's shape: a
          delta-only text must yield ZERO hits, and the same text plus one present-tense line
          must yield exactly that line (anti-tautology, so a predicate returning nothing
          cannot pass the first arm).
      (h) Positive controls (HEADLINE-03, ROADMAP criterion 3, CR-02 fix): layer
          attribution is asserted on SYNTHETIC lines carrying the current literal at the
          REAL surface relpath — docs/v8.0-final-closure.md and CHANGELOG.md must attribute
          a no-arrow line to the WHOLE-FILE layer, and docs/requirements-traceability.md
          must attribute a delta-shaped line to the ARROW layer specifically, inside a file
          that is NOT whole-file exempt (T-10-05 — if it were, assertion (a) would be
          defeated). None of the three needs the LIVE FILE to still contain today's figure,
          because each synthetic line is built from the current literal at call time (via
          `_headline_literals()`), not scanned out of the file's own text — a control bound to
          a live occurrence tested a strictly narrower, stronger precondition than the
          historicity property it claimed to prove, and broke on every legitimate headline
          move (CR-02). The classifier itself IS figure-aware as of Plan 08's anchoring fix;
          what survives is that its verdict is invariant when the figure and the line move
          TOGETHER, which is what block (h2) asserts. A discriminating arm (WR-06) evaluates the
          identical no-arrow line at a relpath that is NOT whole-file exempt and requires
          `""`, proving whole-file MEMBERSHIP — not the line's content — is what rescues the
          two whole-file cases. The one genuinely live-file claim that survives —
          docs/v8.0-final-closure.md still containing a no-arrow current-literal line today
          — is reported as INFO, never asserted, because it legitimately stops being true
          the moment the headline moves.
      (h2) Headline-move invariance control (T-10-05/T-10-08): for each (h) case, asserts
          `_headline_exempt_layer()` returns the SAME layer for the original line (evaluated
          against the CURRENT literals) and the perturbed line (evaluated against the
          PERTURBED literals, passed explicitly) — a cheap, deterministic, in-process stand-in
          for manually simulating a headline move. The property is that layer attribution is
          invariant when the figure AND the line move TOGETHER (what a real headline move
          does), not that the classifier ignores the figure altogether — Plan 08 made the
          classifier figure-aware, and this control's perturbed evaluation was rewired to
          supply the matching perturbed literals rather than the live ones. A second arm
          requires the two constructed lines to be non-byte-equal, so a future edit that made
          the perturbation a no-op cannot leave this passing vacuously forever. Every case
          also carries the LAYER it is expected to land on, and misattribution is its own
          named FAIL (WR-05, Phase 10 review): `_is_historical_headline_hit()` short-circuits
          on whole-file membership before `literals` is resolved, so the two whole-file cases
          compare "whole-file" against "whole-file" and cannot fail while the (0) membership
          lock holds — they are invariant by MEMBERSHIP, not by the property under test. The
          invariance property is carried by the ARROW arms, and a fourth case runs the same
          delta-shaped line at a synthetic NON-exempt relpath so that property does not
          depend on docs/requirements-traceability.md's membership staying as it is. The PASS
          line says which arms carry what, rather than crediting all of them equally.
      (i) Non-vacuity control for the classifier (T-10-04): feeds
          `_is_historical_headline_hit()` a synthetic, non-exempt path and a synthetic line
          containing the current literal with no arrow, and requires NOT historical.
          Prevents (h)'s positive controls from passing off a classifier rewritten to
          `return True` unconditionally.
      (i2) Adjacency-specific controls (CR-03, WR-07, BL-01/T-10-08, WR-09): eight named arms, every
          one driving through `_unregistered_headline_finding()` itself, never a parallel
          copy. 1. mermaid edge and 2. bare HTML comment close must NOT exempt a line sharing
          it with the current headline (the fail-unsafe case CR-03 names); 3. a genuine delta
          line (a superseded figure, an arrow, then the current figure) still must be exempt,
          proving the narrowing did not simply disable the arrow layer; 4. an unrelated
          numeric arrow elsewhere on the line (a battery-count delta) must NOT exempt the
          headline mention on that line (BL-01's reproduction, permanently encoded — not
          contrived, 67 in-scope lines already carry this shape); 5. a genuine delta written
          with the ASCII long arrow must stay exempt (WR-07's reproduction); 6. a complete
          `<!-- ... -->` comment preceding the headline must NOT exempt it, proving the
          narrowed strip does not donate its terminator to the arrow layer once removed —
          without arm 6, arm 5 alone would also pass against a classifier that simply stopped
          stripping comments; 7. the current headline followed by an arrow and a BARE DIGIT RUN
          must NOT be exempt (WR-09's fail-open: that orientation used to accept any digits, so
          a mermaid edge whose SOURCE label is the headline, or a "current → projected" note,
          silently hid a current-fact statement), while 8. the same shape with a
          COVERAGE-SHAPED right-hand figure must stay exempt — without arm 8, arm 7 would also
          pass against a classifier that deleted the orientation instead of narrowing it.
      (i3) Hit-detection controls (WR-06/WR-08, Phase 10 review): four arms driving
          `_headline_hits()`
          itself rather than the classifier. Complete HTML comments are stripped from WHOLE
          FILE TEXT before hits are collected — while that strip ran per line inside the
          classifier, an ordinary block comment stating the headline across three lines was
          reported by the tree-wide scan as a current-fact statement, breaking CI on a
          legitimate edit with a message naming the wrong problem, and `re.DOTALL` on the
          comment pattern was inert. Arm 1 requires such a comment to produce no hit while a
          real statement two lines later is still found AT ITS ORIGINAL LINE NUMBER (the strip
          substitutes one newline per newline removed, so findings stay citable); arm 2
          requires the same text with the markers replaced by plain words to produce both
          hits, so arm 1 cannot pass against a scanner that stopped matching. Arms 3 and 4
          lock the digit boundary (WR-08): a longer digit run merely EMBEDDING the current
          slash rendering ("build 1161/91/0/2521 was fine", a hit under the previous unbounded
          substring test) must produce no hit, while the bare rendering on an otherwise
          identical line still must.
      (j) Tree-wide unregistered-surface scan (HEADLINE-05, T-10-07, BL-02 fix): files are
          collected through the shared `_headline_scan_files()` helper, then actually opened
          and classified through `_headline_scan_read()` (T-10-09) — the single source of
          truth for what was read, its `read_relpaths`/`hits_by_surface` populated as the
          loop goes, never re-derived afterwards from a separate glob or `is_file()` sweep
          (BL-02's root cause). Each hit is decided by `_unregistered_headline_finding()`
          (which itself calls `_is_historical_headline_hit()` — the identical function
          object (h)/(i) exercise, so HEADLINE-05's documented dependency on HEADLINE-03
          already holding is enforced by construction, not by convention): a non-historical
          hit whose file is not in COVERED_HEADLINE_SURFACES is a FAIL naming the file and
          line; a read error (UTF-8 decode failure or any other `OSError`) is a FAIL; a
          candidate the loop declines to open (not a regular file, or a symlink resolving
          outside REPO_ROOT) is a named INFO line — never a silent skip. Before the PASS
          branch, `_headline_scan_floor_breaches()` (CR-01 fix, BL-02 fix) asserts a derived
          coverage floor — every path in COVERED_HEADLINE_SURFACES | HISTORICAL_EXEMPT_FILES
          must be a member of `read_relpaths`, i.e. was actually OPENED, never merely
          glob-matched — and, if that holds, a derived accounted-hit floor evaluated PER
          SURFACE: every member of COVERED_HEADLINE_SURFACES must individually account for
          at least one non-historical hit, never a running total compared against a
          cardinality (a running total has exactly as much slack as the surface contributing
          the most hits beyond one — measured as one unit on the live tree). Both floors are
          derived from the constants, never a magic number, so an emptied or narrowed
          HEADLINE_SCAN_GLOBS, or a registered surface the loop silently declined to open,
          can no longer stay green; this is what lets COVERED_HEADLINE_SURFACES under-count
          without being silently wrong: an omission is caught loudly here rather than
          trusted. The PASS line's reached count is derived from `read_relpaths` (never
          recomputed from a separate sweep) and also reports the number of skipped
          candidates. Never follows a symlink resolving outside REPO_ROOT and never descends
          into the git-ignored, untracked docs/history/ (the glob is non-recursive by
          construction).
      (k) Non-vacuity control for (j) (T-10-08): a synthetic path/line combination, driven
          through the SAME `_unregistered_headline_finding()` function object the real scan
          calls, proves three directions — the synthetic unregistered hit IS reported; the
          identical line attributed to a registered surface is NOT reported (else the
          function would simply flag everything); and the same synthetic path with an arrow
          appended is NOT reported (proving the scan is gated behind HEADLINE-03's
          classifier, not merely a membership test). Preconditions are asserted explicitly so
          the control cannot silently degrade into a tautology.
      (l) Non-vacuity control for the (j-floor) coverage/hit floors (CR-01, WR-09, T-10-09):
          unlike (k), which exercises `_unregistered_headline_finding()` in isolation, arms 1
          and 2 drive `_headline_scan_files()` AND `_headline_scan_read()` themselves — the
          same functions (j) calls — with alternative glob lists, so glob expansion, the
          real read path and `relative_to()` path derivation are all genuinely exercised.
          Three arms: an empty-globs arm (the CR-01 reproduction, permanently encoded)
          asserting a non-empty breach list naming a registered surface; a narrowed-globs arm
          proving the floor degrades proportionally on a "temporarily narrow the scan" typo,
          not only on total absence; and an anti-tautology arm (WR-09) that feeds the floor
          helper a synthetic read result already known to satisfy both floors and requires
          zero breaches. The anti-tautology arm deliberately does NOT re-run the live glob
          path a second time — (j-floor) above already owns that live verdict, and
          duplicating it here would append one defect to wrong_results twice under two
          labels, which is exactly what the shipped code did. Without the anti-tautology arm,
          the first two would also pass against a floor helper that returned a breach
          unconditionally.
      (m) Permanent controls for both halves of the BL-02 escape (T-10-09), plus the decline
          and error branches of BOTH read paths: six arms, every one driving
          `_headline_scan_read()` or `_headline_scan_floor_breaches()` — the identical
          function objects (j) calls, never a parallel copy. Arm 1 removes one
          registered surface from a COPY of the live read result's `read_relpaths` and
          requires the coverage floor to breach naming it — the half of BL-02 where a
          surface the loop refused to read was still counted "reached" by a glob-based
          `is_file()` sweep that followed symlinks. Arm 2 builds a hit map giving one
          registered surface zero hits while moving those hits onto a different registered
          surface so the TOTAL is unchanged, and requires the per-surface floor to breach
          naming the starved surface — the half of BL-02 where a running-total floor had
          exactly one unit of slack (measured: docs/requirements-traceability.md alone
          contributes two hits against five registered surfaces). Arm 3 calls
          `_headline_scan_read()` with a non-regular-file candidate and requires it to be
          named in `skipped` and absent from `read_relpaths` — without this arm, arms 1 and 2
          would also pass against a read loop that silently dropped everything, since both
          construct their inputs by hand rather than driving the loop itself. Arm 4 (WR-02,
          Phase 10 review) drives the same function object over a throwaway tree passed as
          `root`, and requires a symlink whose target resolves outside that root to be named
          in `skipped` with the confinement reason and absent from `read_relpaths`, while a
          plain in-root file in the SAME call is read — the module's only path-confinement
          guard, whose outright deletion previously left the gate green because arm 3
          exercises the other decline reason only. Arm 5 (WR-03, Phase 10 review) drives it
          over a throwaway tree holding one undecodable and one valid file, and requires the
          undecodable one in `read_errors` — absent from both `read_relpaths` and `skipped` —
          while the valid one is read: collapsing the UnicodeDecodeError/OSError split into a
          fail-open `except Exception: continue` previously left the gate green for any
          UNREGISTERED surface, which no floor covers. Arm 6 (CN-03, Phase 10 review) covers
          the OTHER read path — `_headline_read_or_fail()`, the same policy applied to the
          five live-file reads this sentinel makes directly, which were unguarded until this
          review — requiring a readable file to come back verbatim with nothing appended and
          an undecodable one to become exactly one named finding plus a printed FAIL line.
          Both halves run against a throwaway findings list with stdout captured, so the
          control can assert the FAIL line was emitted without emitting one itself. Each arm asserts
          its own precondition explicitly before asserting the property, so none can silently
          degrade into a tautology if a future edit changes a constant. What these arms lock
          is the floor helper's own SEMANTICS; none of them observes what block (j) passes to
          it, so block (j)'s WIRING is locked structurally instead (CR-01, Phase 10 review):
          `_headline_scan_floor_breaches()` takes the `_HeadlineScanRead` record itself, so
          re-deriving the floor input from a glob-based sweep — `_scan_relpaths(_scan_files)`,
          the literal BL-02 defect — is no longer expressible at the call site rather than
          being merely asserted against by a fourth prose control.
      (n) Doc-row transcription lock (WR-06): the two hand-maintained TRACE-03 rows in
          CLAUDE.md and docs/ARCHITECTURE.md transcribe HEADLINE_SCAN_GLOBS' live value by
          hand, and nothing previously compared them — the exact drift class HEADLINE-LOCK
          exists to catch, newly created by the fix for it, and the two copies had already
          diverged once inside this phase (one stated the accounted-hit floor's union claim,
          the other did not). Asserts the rendered glob list is present in each file's own
          TRACE-03 ROW — the single line beginning "| TRACE-03 ", located by slicing the file
          and FAILing when a file carries zero or several such lines (WR-04, Phase 10 review:
          the previous whole-file containment test would have let the row's own transcription
          drift to anything at all as soon as the glob list was mentioned anywhere else in
          either file, the exact drift class this block exists to close). Guards both files
          for existence first (a named FAIL rather than a traceback), and carries a
          non-vacuity arm requiring a DELIBERATELY DIFFERENT rendering to be absent from both
          rows, sliced the same way — without it, a lock whose comparison always succeeded would be
          indistinguishable from a passing lock, the same anti-tautology rule (b), (e), (i),
          (k), (l) and (m) already observe. This lock asserts the GLOB LIST's transcription
          only; the rest of each row's prose remains unasserted, which is a real and
          disclosed limit, not an oversight.

    Reads live files rather than fixtures (Pitfall 4 idiom, as V79-ROWS / V818-ROWS do), so
    it locks the shipped surfaces themselves and not a copy of them. Offline and deterministic:
    no live claude session, no network, no writes.

    LAYOUT (CN-04, Phase 10 review). Everything above runs from this function, but the blocks
    live in four stage functions, on the block seams the review named:

      _headline_lock_preamble   (0), (a)-(e)   exemption sets, published headline, artifacts
      _headline_lock_surfaces   (f)-(i3)       per-surface presence, layers, classifier, hits
      _headline_lock_scan       (j)-(m)        tree-wide scan, floors, permanent controls
      _headline_lock_doc_rows   (n)            TRACE-03 doc-row transcription lock

    Each takes `wrong_results` and nothing else, matching the dispatch shape `_run_self_test()`
    already uses for its seven peer sentinels; each derives the shared literals for itself from
    `_headline_lock_context()`, which is sound because `_headline_literals()` is deliberately
    un-memoized and `build_matrix_rows()` is deterministic (block (0) still checks the two
    independent derivations agree). This function stayed the single entry point and kept this
    docstring, so nothing outside the module sees the split.

    The split was verified as a refactor, not a rewrite: --self-test stdout is byte-identical
    to the pre-split run, in set AND order, and every mutant in this phase's suite still fails.
    Each stage additionally reports the block labels it ran, reconciled below against
    `_HEADLINE_LOCK_BLOCKS` — a stage dropped from `_HEADLINE_LOCK_STAGES` would otherwise be a
    silently shorter green run, which is the specific hazard of splitting a non-vacuity gate.
    Those labels are self-reported, so the reconciliation covers the DISPATCH, not the block
    bodies; the bodies are what every other control here already covers.
    """
    _ran: list[str] = []
    for _stage in _HEADLINE_LOCK_STAGES:
        _ran.extend(_stage(wrong_results))
    if tuple(_ran) != _HEADLINE_LOCK_BLOCKS:
        print(
            f"  HEADLINE-LOCK FAIL: stage dispatch ran {tuple(_ran)}, expected "
            f"{_HEADLINE_LOCK_BLOCKS} — a stage was dropped, reordered, or stopped running "
            "a block it owns"
        )
        wrong_results.append(
            f"HEADLINE-LOCK: stage dispatch incomplete (ran {tuple(_ran)})"
        )


def _run_self_test() -> None:
    """Run the inline artifact-resolution / schema / sentinel fixtures — no .planning/ reads required.

    Fixtures per PATTERNS.md §Required fixtures:
      (1) valid reproducible row → PASS
      (2) reproducible row with dangling file path → flagged
      (3) reproducible row with dangling catalog row → flagged
      (4) reproducible row with missing rubric anchor → flagged
      (5) audit-only row, no artifact link → PASS (valid state)
      (6) gap row with rationale, no artifact link → PASS (valid state; generic structural test)
      (7) row missing capability → flagged
      (8) row missing coverage_tier → flagged
      (9) scheduled row with resolvable artifact link → PASS (WR-02/D-02/Phase 90)
      (10) DISTRIBUTION-FOLD: render_matrix_markdown on synthetic 2-repro+1-scheduled set;
           asserts bullets sum to len(rows), (incl. 1 scheduled) annotation present,
           folded count strictly > bare reproducible count (WR-01 fold lock / TRACE-03)

    Named sentinels:
      GEN-01-REPRODUCIBLE: live tier assertion (reproducible) + not-scheduled counter-check
                           + drift guard + deep-resolve of tests/step0-baseline-v7.6.md
                           (D-09/Phase 93; repurposed from GEN-01-SCHEDULED Phase 88;
                           artifact bumped v6.4->v7.4 Phase 108; bumped v7.4->v7.6 Phase 114)
      GEN-02-RUNBOOK: live tier assertion + counter-check + drift guard + dual-file existence
                      check (runbook + wrapper) (D-03/Phase 89)
      V79-ROWS: live row count + bare_id set + reproducible-tier + deep-resolve + RECON-01
                positive counter-check (D-01 / Phase 123); locks all 8 v7.9 milestone rows
                against silent drift; no live claude session required.
      V818-ROWS: live row count + bare_id set + ID-pinned 21/2 tier partition + deep-resolve
                 over reproducible rows only + HARN-04 positive counter-check + milestone/key
                 attribution lock + capability lock (D-07 / Phase 4); locks all 23 v8.18
                 milestone rows against silent drift, including a tier swap between two
                 named IDs that a blanket count assert would miss; no live claude session
                 required.
      V824-ROWS: live row count + bare_id set + ID-pinned 14/1 tier partition + deep-resolve
                 over reproducible rows only + GATE-03 positive counter-check + milestone/key
                 attribution lock + capability lock (D-09 / Phase 6); locks all 15 v8.24
                 milestone rows against silent drift, including a tier swap between two
                 named IDs that a blanket count assert would miss; no live claude session
                 required.
      V825-ROWS: live row count + bare_id set + ID-pinned 13/1 tier partition + deep-resolve
                 over reproducible rows only + HEADLINE-01 positive counter-check + milestone/key
                 attribution lock + capability lock (Phase 12); locks all 14 v8.25
                 milestone rows against silent drift, including a tier swap between two
                 named IDs that a blanket count assert would miss; no live claude session
                 required.
      HEADLINE-LOCK: ties the published coverage headline in
                 docs/requirements-traceability.md, and both tracked artifacts
                 (docs/requirements-matrix.md, docs/data/matrix.json), back to
                 build_matrix_rows() — with non-vacuity controls on both comparisons
                 (WR-08 / Phase 4 review). Closes the drift class that produced that
                 review's own CR-01, which was corrected by hand with the mechanism
                 left intact. All four headline figures are derived live, gap included.
    """
    wrong_results: list[str] = []
    _self_test_valid_rows_fixtures(wrong_results)
    _self_test_dangling_fixtures(wrong_results)
    _self_test_schema_fixtures(wrong_results)
    _self_test_pyanchor_resolver(wrong_results)
    _self_test_v79_rows_sentinel(wrong_results)
    _self_test_v818_rows_sentinel(wrong_results)
    _self_test_v824_rows_sentinel(wrong_results)
    _self_test_v825_rows_sentinel(wrong_results)
    _self_test_headline_lock(wrong_results)
    if wrong_results:
        sys.stderr.write(
            f"check-traceability --self-test: FAIL — {', '.join(wrong_results)}\n"
        )
        sys.exit(1)
    print("check-traceability --self-test: PASS")


# ---------------------------------------------------------------------------
# Subcommand handlers
# ---------------------------------------------------------------------------


def _run_emit(md_output: Path, json_output: Path) -> None:
    """Handler for the emit subcommand."""
    rows = build_matrix_rows()
    emit_matrix(rows, md_output, json_output)
    print(
        f"check-traceability emit: PASS — {len(rows)} rows written to "
        f"{md_output} + {json_output}"
    )


def _run_check(input_path: Path) -> None:
    """Handler for the check subcommand."""
    rows = load_rows(input_path)
    issues = check_consistency(rows)
    if issues:
        for issue in issues:
            sys.stderr.write(f"check-traceability check: ISSUE — {issue}\n")
        sys.exit(1)
    print(
        f"check-traceability check: PASS — {len(rows)} rows consistent"
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "TRACE-01..TRACE-03 / GAP-01 gate: traceability matrix emitter + "
            "consistency gate (stdlib-only)."
        )
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help=(
            "run the inline fixtures + named sentinels (no .planning/ reads required); "
            "exit 0 only if all pass (CI gate entry point)"
        ),
    )
    subparsers = parser.add_subparsers(dest="subcommand")

    emit_parser = subparsers.add_parser(
        "emit",
        help="Write MATRIX.md + matrix.json from build_matrix_rows()",
    )
    emit_parser.add_argument(
        "--md-output",
        type=Path,
        required=True,
        help="Path for requirements-matrix.md (must be under .planning/ or docs/; T-82-01)",
    )
    emit_parser.add_argument(
        "--json-output",
        type=Path,
        required=True,
        help="Path for matrix.json (must be under .planning/ or docs/; T-82-01)",
    )

    check_parser = subparsers.add_parser(
        "check",
        help="Validate matrix.json for consistency (D-08)",
    )
    check_parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Path to matrix.json to validate",
    )

    args = parser.parse_args()
    _require_python_version()

    if args.self_test:
        _run_self_test()
        return

    if args.subcommand == "emit":
        _run_emit(args.md_output, args.json_output)
    elif args.subcommand == "check":
        _run_check(args.input)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
