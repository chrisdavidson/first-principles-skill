#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""HARN-02 gate: assert every re-entry edge and its bound survives in the four
`shared/` source files that carry Phase 2's loop-closure prose and the
frontmatter permission one of those edges depends on.

Usage:
    python3 scripts/check-loop-closure.py [--self-test]

Exit codes:
    0  all checks passed
    1  validation failure (a pinned literal is missing, or an unbounded
       instruction has been reinstated)
    2  environment error (Python <3.12, a source file is missing)

--self-test: runs a positive control (the live tree must be clean), then a
             table of negative controls (each a single stripped, reinstated or
             inverted literal on an in-memory copy of one real file), a scope
             control (proving the bound-paragraph mutation is confined to that
             paragraph), anti-masking controls (proving a failure is attributed
             to the right source file), and anchor-arity controls (proving a
             scoped, single-line assertion does not go vacuous when its anchor
             matches zero or more than one line). Exits 0 if every control
             behaves as expected; exits 1 if any control wrongly passes or
             fails for the wrong reason.

             The control count is reported by the emitted PASS lines, never
             asserted here as a magic number — a hand-maintained tally in a
             docstring goes stale by construction.

             Two of the negative controls reinstate their literal PRE-WRAPPED
             at the guarded files' own ~95-column width. That is the shape a
             real regression takes in a hard-wrapped Markdown repo, and the
             blind spot that let an unbounded re-score instruction ship with
             this gate green; see `_flat()` and `_reinstate_hard_wrapped()`.

This gate reads four `shared/` SOURCE files as four separate strings — never
the merged, generated `first-principles/agents/first-principles.md` — so a
failure message can name which source file the missing edge belongs to. The
fourth is `SKILL.meta.yml`: the mid-run re-open edge's prose is unfirable
without the frontmatter permission it depends on, so the prose and the
permission are asserted together.
Negative controls always mutate an in-memory copy of the real text; no file on
disk is ever written by this script.

Not registered in `scripts/check-firewall-battery.sh`. Registration is a
separate, later step; the battery's printed tally is unaffected by this file.
"""

from __future__ import annotations

import argparse
import re
import sys
import textwrap
from pathlib import Path

REPO_ROOT: Path = Path(__file__).resolve().parents[1]
BODY_PATH: Path = REPO_ROOT / "shared" / "spine" / "SKILL-body.md"
CONTRACT_PATH: Path = REPO_ROOT / "shared" / "agent" / "input-contract.md"
RUBRIC_PATH: Path = REPO_ROOT / "shared" / "spine" / "references" / "validation-rubric.md"
META_PATH: Path = REPO_ROOT / "shared" / "spine" / "SKILL.meta.yml"

_BODY_NAME = "SKILL-body.md"
_CONTRACT_NAME = "input-contract.md"
_RUBRIC_NAME = "validation-rubric.md"
_META_NAME = "SKILL.meta.yml"

# ---------------------------------------------------------------------------
# Pinned literals (see 02-03-PLAN.md <gate_contract>; wording confirmed
# byte-identical to 02-01-SUMMARY.md / 02-02-SUMMARY.md's "Exact Final
# Wording of Added Sentences").
#
# `_BOUND` is used against BOTH SKILL-body.md and validation-rubric.md — this
# single shared constant IS assertion D1 (cross-file drift): the two prose
# sites cannot diverge without both failing this gate, because there is only
# one string for both checks to compare against.
# ---------------------------------------------------------------------------
_BOUND = "at most one re-perception pass"  # L1 (body) / L8 (rubric)

# L1a / L8a: the bound WITH its polarity carrier.
#
# `_BOUND` on its own is a bare noun phrase, so substring presence cannot tell
# the rule from its negation. Both of these pass a bare-`_BOUND` check while
# inverting the rule the phase exists to install:
#     body:   "edge fires more than **at most one re-perception pass** per analysis"
#     rubric: "not bounded to **at most one re-perception pass** per analysis"
# Hedging qualifiers accrete onto rules over edits, so this is drift, not
# contrivance. These two literals pin the operative verb phrase immediately
# adjacent to the bound, so a hedge inserted between them breaks the match.
# `_BOUND` itself is retained for the D1 cross-file drift assertion.
_BOUND_BODY = "Each edge fires **at most one re-perception pass** per analysis."  # L1a
_BOUND_RUBRIC = (
    "revise the analysis and re-score — bounded to "
    "**at most one re-perception pass** per analysis"
)  # L8a

# X4 / X5: the two demonstrated inversions, pinned ABSENT directly. A positive
# pin catches a hedge inserted INSIDE the pinned span; these catch the negation
# forms that a plain substring test would swallow whole.
_INVERTED_BOUND_BODY = "more than **at most one re-perception pass**"  # X4
_INVERTED_BOUND_RUBRIC = "not bounded to **at most one re-perception pass**"  # X5
_DEGRADE = "unresolved gap with a confidence caveat"  # L2

# L14: the degradation sentence used to be criterion-scoped ("A second failure of
# the SAME criterion after one pass..."), competing with the edge-scoped bound in
# the sentence immediately before it. That carve-out said nothing about a
# criterion failing for the FIRST time after a pass — and the Fix step ("revise
# every criterion that does not pass") routinely perturbs sections other than the
# one it targets — so a reader applying it as the operative rule could loop
# indefinitely by alternating which criterion fails. This clause subordinates the
# degradation sentence to the edge-scoped bound; it is the load-bearing half.
_BOUND_SUBORDINATION = (
    "the edge has already fired and does not fire again, regardless of which "
    "criterion is at fault"
)  # L14
_PHASE1_ROUTE = "returns to Phase 1 to re-frame the Essence Statement"  # L3
_FIRING_RECORD = "name which re-entry edge fired"  # L4
_UNBOUNDED_REPEAT = "until every criterion clears the gate"  # X1 (must be ABSENT)

_MIDRUN_SCOPE = "not only before the analysis starts"  # L5
_NO_PER_DELEGATION = "does not confirm framing on every delegation"  # L6
_ASK_TOOL = "AskUserQuestion"  # L7
_ASK_FALLBACK = "If `AskUserQuestion` is unavailable at runtime"  # L7b

# L16: the fallback's mid-run branch.
#
# The clarification clause was widened to fire mid-run, but the unavailability
# fallback stayed written for the pre-analysis case only — "states what it needs
# ... before proceeding with a best-effort analysis". Applied at the mid-run
# trigger point, the gate has already scored a criterion Absent, and two rules
# forbid what that licenses: the rubric's "any criterion scored Absent fails the
# entire analysis — it must be revised before conclusions are presented", and the
# body's "do not present conclusions until ... the Self-Audit Gate is cleared".
# Proceeding best-effort past an Absent verdict is the escape hatch those two
# rules exist to close.
_ASK_FALLBACK_MIDRUN = (
    "If it is unavailable at the mid-run re-open, the analysis does not proceed "
    "past the Absent verdict"
)  # L16

# L12: the mid-run re-open's landing point. It used to read "re-enters through
# Phase 2" — but Phase 2's own entry criterion is "The Essence Statement from
# Phase 1 is complete", which is definitionally what a Criterion 1 Absent
# verdict reports missing. The route handed the user's answer to a phase whose
# entry condition the verdict itself falsified, and skipped the only phase that
# produces the missing artifact. The landing point now tracks the artifact, so
# pin the artifact-tracking clause rather than a bare phase number.
_MIDRUN_LANDING = "re-enters at the phase that owns the artifact the Absent verdict named"  # L12
_MIDRUN_LANDING_BODY = "re-enters at the phase that owns the missing artifact"  # L13

# L15: the frontmatter permission the mid-run re-open edge depends on.
#
# The gate pins that edge's PROSE (L5, L6, L7, L7b, L12) across two files, but
# the edge is unfirable unless the agent is permitted to call the tool. Drop this
# key and every prose assertion stays green while one of the enumerated re-entry
# edges silently becomes dead: the agent follows an instruction to use a tool it
# cannot invoke, and the documented unavailability fallback fires permanently and
# invisibly. Nothing else in this repo ties that key to the prose that needs it.
_ASK_PERMITTED = "AskUserQuestion: permitted"  # L15

_TURN_DISCIPLINE = "Turn discipline"  # L9
_UNBOUNDED_RESCORE = "revise the analysis and re-score from the beginning"  # X2 (must be ABSENT)

# X3: the phrase-shape the unbounded instruction keeps returning as. The rubric's
# Usage Note shipped it in wording X2 does not match ("the relevant sections"
# rather than "the analysis") AND split across a hard-wrap boundary, so two
# independent blind spots kept it green. X3 pins the surviving fragment — the
# operative "start over" instruction itself — so a reworded restatement is caught
# on the part that carries the meaning.
_UNBOUNDED_RESCORE_ALT = "re-score from the beginning"  # X3 (must be ABSENT)

# The Usage Note is the LAST operative sentence a model reads before it starts
# scoring, so recency favours whatever it says. L11 pins it to the same bound the
# rubric states at the top of the file; without this positive pin, deleting the
# bound from the Usage Note (rather than contradicting it) would pass X3.
_USAGE_NOTE_BOUND = (
    "revise the relevant sections and re-score — bounded to "
    "**at most one re-perception pass** per analysis"
)  # L11

_COMPLETENESS_CLAIM = "complete enough that Phase 4 can reason upward"  # L10a
# L10b: the exception CLAUSE, not the token. This used to be the seven-character
# token "re-entry", which any sentence containing the word satisfied — including
# one that removes the exception ("this exit criterion admits no re-entry"). The
# pin could not distinguish the clause from its negation, and did not check that
# the clause names the edges or defers to the bound.
_REENTRY_EXCEPTION = "except through the bounded re-entry edges named under Turn discipline"
_SECOND_ORDER = "second-order"  # scoped to the Turn discipline bound paragraph (S3)

# L17 / L18 / X6: the edge enumeration.
#
# The list used to name five edges, two of which — "the Self-Audit Gate's
# Fix/Repeat loop" and "the Self-Audit Gate rubric's re-score instruction" — are
# one operation described in two documents (revise, then re-score). The rubric's
# own sentence points back at the body's rule, which then listed it as a separate
# edge from the loop it belongs to. Under "Each edge fires at most one
# re-perception pass", enumerating one loop twice grants it two passes, and an
# analysis can defend a second re-score by naming the other entry. The count is
# load-bearing prose — a reader checks it against the list — so it is pinned,
# with the superseded count pinned ABSENT.
_EDGE_COUNT = "Four re-entry edges exist in this methodology"  # L17
_ONE_EDGE_TWO_STATEMENTS = "one edge, two statements"  # L18
_SUPERSEDED_EDGE_COUNT = "Five re-entry edges exist in this methodology"  # X6
_RE_PERCEPTION_PASS = "re-perception pass"  # scoped to the Repeat line (S1)

# Anchors for scoped, single-line assertions. Each must match exactly one
# line — zero or two is itself a failure (see _find_unique_line below), so a
# duplicated or renamed anchor is caught rather than silently skipped.
_S1_ANCHOR = "3. **Repeat**"
_S2_ANCHOR = "**Exit criterion:** All ground truths have stable IDs"
# S4: the Phase-1 route sentence must live in the paragraph that owns it. Checked
# whole-text, the sentence could migrate anywhere in the document — into a
# companion-tool blurb, say — and still pass. S1, S2 and S3 are all scoped; L3
# was not, with no stated reason.
_S4_ANCHOR = "**A Criterion 1 Absent verdict returns to Phase 1.**"
_TURN_DISCIPLINE_HEADING = "### Turn discipline"


_WS = re.compile(r"\s+")

# The prevailing hard-wrap width of every Markdown file this gate guards. Used
# only by the self-test, to build a fixture in the shape a real regression takes.
_WRAP_WIDTH = 95


def _flat(text: str) -> str:
    """Collapse every whitespace run to a single space.

    Every file this gate guards is hard-wrapped at ~95 columns, so a pinned
    multi-word literal can straddle a line break. A raw `literal in text` test
    is blind to that: it reads a newline as a different character than a space,
    so a reinstated unbounded instruction that happens to wrap inside the pinned
    phrase sails through, and a merely-reflowed (but unchanged) pinned phrase
    reports a false failure. Both directions are defects; normalising whitespace
    on both the haystack and the needle closes both.

    Every presence and absence assertion in this module compares `_flat(text)`
    against `_flat(literal)` for exactly this reason. Do not reintroduce a raw
    `in text` comparison against a multi-word literal.
    """
    return _WS.sub(" ", text)


def _contains(text: str, literal: str) -> bool:
    """Whitespace-insensitive containment — the only membership test this
    module's assertions may use against a multi-word pinned literal."""
    return _flat(literal) in _flat(text)


def _require_python_version() -> None:
    if sys.version_info < (3, 12):
        sys.stderr.write(
            f"scripts/check-loop-closure.py requires Python >=3.12 "
            f"(running {sys.version_info.major}.{sys.version_info.minor}).\n"
        )
        sys.exit(2)


_LIST_ITEM_RE = re.compile(r"^\s*(?:\d+[.)]|[-*+])\s")


def _block_end(lines: list[str], idx: int) -> int:
    """Index one past the last line of the logical block starting at *idx*.

    A block ends at a blank line, at the start of a new list item, at a heading,
    or at a horizontal rule. Shared by the checker (`_find_unique_block`) and by
    the self-test's mutators (`_mutate_block`) so the two cannot drift apart
    about what "the Repeat line" means."""
    end = idx + 1
    while end < len(lines):
        stripped = lines[end].strip()
        if not stripped:
            break
        if _LIST_ITEM_RE.match(lines[end]) or stripped.startswith("#") or set(stripped) == {"-"}:
            break
        end += 1
    return end


def _find_unique_block(text: str, anchor: str) -> tuple[str | None, int]:
    """Return (the logical block starting at *anchor*, match count).

    Returns (None, n) when n != 1, so a caller can report "expected exactly one,
    found N" rather than silently picking the first match (or none). The anchor
    is matched line-anchored (`startswith` on a line), never as a free substring.

    A "block" is the LOGICAL Markdown unit, not the physical line: the anchor
    line plus every following line that continues it — non-blank, not the start
    of a new list item, not a heading or a horizontal rule.

    Scoping these assertions to the physical line is what forced SKILL-body.md's
    two pinned-literal lines out to 186 and 258 characters in a file that
    otherwise wraps at ~95: the document had been hand-shaped around the matcher,
    and the next markdownlint config change, formatter run or routine re-wrap
    would have turned this gate red for no content reason. Reading the logical
    unit removes that coupling, so the source can be wrapped like its neighbours.
    """
    lines = text.splitlines()
    starts = [i for i, ln in enumerate(lines) if ln.startswith(anchor)]
    if len(starts) != 1:
        return None, len(starts)
    idx = starts[0]
    return "\n".join(lines[idx:_block_end(lines, idx)]), 1


def _extract_turn_discipline_section(text: str) -> tuple[str | None, int]:
    """Slice the `### Turn discipline` section out of *text*, from the heading to
    the next horizontal rule. Returns (section, heading match count); the section
    is None whenever the count is not exactly 1.

    Three defects in the previous `str.find` implementation, each of which this
    file's sibling `_find_unique_block` was already written to refuse:

    * `find` took the FIRST match silently. A duplicated `### Turn discipline`
      heading — the exact scenario the anchor-arity controls exist to catch for
      S1 and S2 — was accepted without comment. The count is now returned so the
      caller can report a duplicate distinctly from a missing heading.
    * `find` is a substring search, not line-anchored, and `#### Turn discipline`
      CONTAINS `### Turn discipline`. Demoting the heading one level left the
      extraction working and pointed S3 at a section that was no longer a peer of
      Step 0 and the phases. Matching whole lines refuses that.
    * The terminator `find("\\n---")` also matched `----`, `-----`, or any line
      merely BEGINNING with `---`, silently truncating the section. The
      terminator is now a line that IS `---`.
    """
    lines = text.splitlines(keepends=True)
    starts = [
        i for i, ln in enumerate(lines) if ln.rstrip("\n") == _TURN_DISCIPLINE_HEADING
    ]
    if len(starts) != 1:
        return None, len(starts)
    idx = starts[0]
    for j in range(idx + 1, len(lines)):
        if lines[j].rstrip("\n") == "---":
            return "".join(lines[idx:j]), 1
    return "".join(lines[idx:]), 1


# ---------------------------------------------------------------------------
# Pure check functions. Each takes text and returns a list of failure-message
# strings; never raises, never prints. Every message is prefixed with the
# source file's basename, so a merged check could not tell which file to fix.
# ---------------------------------------------------------------------------


def _check_body_text(text: str) -> list[str]:
    failures: list[str] = []
    src = _BODY_NAME

    if not _contains(text, _BOUND):
        failures.append(f'{src}: missing the re-entry bound ("{_BOUND}")')
    if not _contains(text, _EDGE_COUNT):
        failures.append(
            f'{src}: the re-entry edge enumeration has lost its count ("{_EDGE_COUNT}")'
        )
    if _contains(text, _SUPERSEDED_EDGE_COUNT):
        failures.append(
            f'{src}: the edge enumeration double-counts the Fix/Repeat loop, granting it '
            f'two passes under a per-edge bound ("{_SUPERSEDED_EDGE_COUNT}")'
        )
    if not _contains(text, _ONE_EDGE_TWO_STATEMENTS):
        failures.append(
            f'{src}: the enumeration no longer says the Fix/Repeat loop and the rubric\'s '
            f're-score instruction are one edge stated twice '
            f'("{_ONE_EDGE_TWO_STATEMENTS}")'
        )
    if not _contains(text, _BOUND_BODY):
        failures.append(
            f'{src}: the bound has lost its polarity carrier — a bare noun phrase '
            f'cannot distinguish the rule from its negation ("{_BOUND_BODY}")'
        )
    if _contains(text, _INVERTED_BOUND_BODY):
        failures.append(
            f'{src}: the bound has been inverted by a hedging qualifier '
            f'("{_INVERTED_BOUND_BODY}")'
        )
    if not _contains(text, _DEGRADE):
        failures.append(f'{src}: missing the degradation path ("{_DEGRADE}")')
    if not _contains(text, _BOUND_SUBORDINATION):
        failures.append(
            f'{src}: the degradation sentence is not subordinated to the edge-scoped '
            f'bound — a criterion-scoped carve-out leaves the loop reopenable by '
            f'alternating which criterion fails ("{_BOUND_SUBORDINATION}")'
        )
    # S4: L3 is scoped to the paragraph that owns it, not checked whole-text.
    s4_block, s4_count = _find_unique_block(text, _S4_ANCHOR)
    if s4_count != 1:
        failures.append(
            f'{src}: expected exactly one paragraph starting with "{_S4_ANCHOR}", '
            f"found {s4_count}"
        )
        if not _contains(text, _PHASE1_ROUTE):
            failures.append(f'{src}: missing the Phase-1 re-entry route ("{_PHASE1_ROUTE}")')
    elif not _contains(s4_block, _PHASE1_ROUTE):
        failures.append(
            f'{src}: missing the Phase-1 re-entry route from the paragraph that owns it '
            f'("{_PHASE1_ROUTE}")'
        )
    if not _contains(text, _FIRING_RECORD):
        failures.append(f'{src}: missing the re-entry firing record ("{_FIRING_RECORD}")')
    if _contains(text, _UNBOUNDED_REPEAT):
        failures.append(
            f'{src}: unbounded Repeat instruction still present ("{_UNBOUNDED_REPEAT}")'
        )
    if not _contains(text, _MIDRUN_LANDING_BODY):
        failures.append(
            f'{src}: the mid-run re-open route is not widened past Criterion 1 with an '
            f'artifact-tracking landing point ("{_MIDRUN_LANDING_BODY}")'
        )

    # S1: the Repeat line names the bound.
    s1_line, s1_count = _find_unique_block(text, _S1_ANCHOR)
    if s1_count != 1:
        failures.append(
            f'{src}: expected exactly one line starting with "{_S1_ANCHOR}", found {s1_count}'
        )
    elif not _contains(s1_line, _RE_PERCEPTION_PASS):
        failures.append(
            f'{src}: the "{_S1_ANCHOR}" line is missing "{_RE_PERCEPTION_PASS}"'
        )

    # S2: the Phase 3 exit-criterion line keeps the completeness claim AND
    # carries the new re-entry exception clause.
    s2_line, s2_count = _find_unique_block(text, _S2_ANCHOR)
    if s2_count != 1:
        failures.append(
            f'{src}: expected exactly one line starting with "{_S2_ANCHOR}", found {s2_count}'
        )
    else:
        if not _contains(s2_line, _COMPLETENESS_CLAIM):
            failures.append(
                f'{src}: the Phase 3 exit-criterion line lost the completeness claim '
                f'("{_COMPLETENESS_CLAIM}")'
            )
        if not _contains(s2_line, _REENTRY_EXCEPTION):
            failures.append(
                f'{src}: the Phase 3 exit-criterion line lost the re-entry exception clause '
                f'("{_REENTRY_EXCEPTION}")'
            )

    # S3: exactly one paragraph inside Turn discipline carries the bound, and
    # that paragraph names the second-order edge. The second-order→Phase 2
    # edge has no site-of-trigger sentence of its own (nothing in this phase
    # edits it) — it is bounded only by being named here, so this is the sole
    # assertion protecting that edge.
    section, heading_count = _extract_turn_discipline_section(text)
    if section is None and heading_count == 0:
        failures.append(f'{src}: could not locate the "{_TURN_DISCIPLINE_HEADING}" section')
    elif section is None:
        failures.append(
            f'{src}: expected exactly one "{_TURN_DISCIPLINE_HEADING}" heading, '
            f"found {heading_count} — a duplicated heading is not a missing one"
        )
    else:
        paragraphs = [p for p in section.split("\n\n") if p.strip()]
        bound_paragraphs = [p for p in paragraphs if _contains(p, _BOUND)]
        if len(bound_paragraphs) != 1:
            failures.append(
                f"{src}: expected exactly one paragraph in Turn discipline containing "
                f'the bound ("{_BOUND}"), found {len(bound_paragraphs)}'
            )
        elif not _contains(bound_paragraphs[0], _SECOND_ORDER):
            failures.append(
                f'{src}: the bound paragraph in Turn discipline does not name the '
                f'second-order edge ("{_SECOND_ORDER}")'
            )

    return failures


def _check_input_contract_text(text: str) -> list[str]:
    failures: list[str] = []
    src = _CONTRACT_NAME

    if not _contains(text, _MIDRUN_SCOPE):
        failures.append(f'{src}: missing the mid-run scope clause ("{_MIDRUN_SCOPE}")')
    if not _contains(text, _NO_PER_DELEGATION):
        failures.append(
            f'{src}: missing the per-delegation prohibition ("{_NO_PER_DELEGATION}")'
        )
    if not _contains(text, _ASK_TOOL):
        failures.append(f'{src}: missing the AskUserQuestion tool reference')
    if not _contains(text, _ASK_FALLBACK):
        failures.append(
            f'{src}: missing the AskUserQuestion-unavailable fallback clause ("{_ASK_FALLBACK}")'
        )
    if not _contains(text, _ASK_FALLBACK_MIDRUN):
        failures.append(
            f'{src}: the AskUserQuestion-unavailable fallback has no mid-run branch — as '
            f'written it licenses proceeding best-effort past an Absent verdict '
            f'("{_ASK_FALLBACK_MIDRUN}")'
        )
    if not _contains(text, _MIDRUN_LANDING):
        failures.append(
            f'{src}: the mid-run re-open does not route its answer by which artifact is '
            f'missing ("{_MIDRUN_LANDING}")'
        )

    return failures


def _check_rubric_text(text: str) -> list[str]:
    failures: list[str] = []
    src = _RUBRIC_NAME

    # L8 uses the SAME _BOUND constant as the body's L1 — assertion D1.
    if not _contains(text, _BOUND):
        failures.append(f'{src}: missing the re-entry bound ("{_BOUND}")')
    if not _contains(text, _BOUND_RUBRIC):
        failures.append(
            f'{src}: the bound has lost its polarity carrier — a bare noun phrase '
            f'cannot distinguish the rule from its negation ("{_BOUND_RUBRIC}")'
        )
    if _contains(text, _INVERTED_BOUND_RUBRIC):
        failures.append(
            f'{src}: the bound has been inverted by a hedging qualifier '
            f'("{_INVERTED_BOUND_RUBRIC}")'
        )
    if not _contains(text, _TURN_DISCIPLINE):
        failures.append(
            f'{src}: missing the Turn discipline cross-reference ("{_TURN_DISCIPLINE}")'
        )
    if _contains(text, _UNBOUNDED_RESCORE):
        failures.append(
            f'{src}: unbounded re-score instruction still present ("{_UNBOUNDED_RESCORE}")'
        )
    if _contains(text, _UNBOUNDED_RESCORE_ALT):
        failures.append(
            f'{src}: unbounded re-score instruction still present in its reworded form '
            f'("{_UNBOUNDED_RESCORE_ALT}")'
        )
    if not _contains(text, _USAGE_NOTE_BOUND):
        failures.append(
            f'{src}: the Usage Note no longer brings its closing re-score instruction '
            f'under the bound ("{_USAGE_NOTE_BOUND}")'
        )

    return failures


def _check_meta_text(text: str) -> list[str]:
    failures: list[str] = []
    src = _META_NAME

    if not _contains(text, _ASK_PERMITTED):
        failures.append(
            f'{src}: the mid-run re-open edge requires "{_ASK_PERMITTED}" in the agent '
            f"frontmatter — without it the edge is unfirable and its prose is dead"
        )

    return failures


def _check_loop_closure(body: str, contract: str, rubric: str, meta: str) -> list[str]:
    """Pure aggregator over four strings — lets the self-test feed it
    mutated in-memory copies without touching any file on disk."""
    return (
        _check_body_text(body)
        + _check_input_contract_text(contract)
        + _check_rubric_text(rubric)
        + _check_meta_text(meta)
    )


def _read_source_files() -> tuple[str, str, str, str]:
    missing = [
        str(p)
        for p in (BODY_PATH, CONTRACT_PATH, RUBRIC_PATH, META_PATH)
        if not p.exists()
    ]
    if missing:
        sys.stderr.write(
            "check-loop-closure: source file(s) not found: " + ", ".join(missing) + "\n"
        )
        sys.exit(2)
    return (
        BODY_PATH.read_text(encoding="utf-8"),
        CONTRACT_PATH.read_text(encoding="utf-8"),
        RUBRIC_PATH.read_text(encoding="utf-8"),
        META_PATH.read_text(encoding="utf-8"),
    )


def _validate_live_tree() -> None:
    body, contract, rubric, meta = _read_source_files()
    failures = _check_loop_closure(body, contract, rubric, meta)
    if failures:
        for msg in failures:
            sys.stderr.write(f"check-loop-closure: FAIL — {msg}\n")
        sys.exit(1)
    print("check-loop-closure: PASS")


# ---------------------------------------------------------------------------
# Self-test: in-memory mutation fixtures, never touching a file on disk.
# ---------------------------------------------------------------------------


def _flex_pattern(target: str) -> re.Pattern[str]:
    """A pattern matching *target* with any whitespace run standing in for each
    of its spaces — the fixture-side counterpart of `_flat()`.

    Without this, a control that strips a pinned literal breaks the moment the
    real file reflows that literal across a line boundary: the raw
    `str.replace` finds nothing, the precondition guard trips, and the control
    stops being a control."""
    return re.compile(r"\s+".join(re.escape(w) for w in _flat(target).strip().split(" ")))


def _replace_once(text: str, target: str, replacement: str = "REMOVED") -> str:
    """Single-site substitution — never a broad sweep, so a mutation cannot
    accidentally remove a second occurrence and make a control pass for a
    reason it did not intend. Whitespace-tolerant (see `_flex_pattern`)."""
    pattern = _flex_pattern(target)
    assert pattern.search(text) is not None, f"target not found in text: {target!r}"
    return pattern.sub(replacement, text, count=1)


def _strip_everywhere(text: str, target: str, replacement: str = "REMOVED") -> str:
    """Remove EVERY occurrence of *target* from *text*.

    A whole-text "must contain" assertion (`target not in text`) is a
    text-wide existential claim, not a site-scoped one. `_DEGRADE`
    ("unresolved gap with a confidence caveat") is currently stated twice in
    `SKILL-body.md` — once in the canonical Turn discipline bound paragraph,
    once in the Repeat item's own sentence — so a single-site strip
    (`_replace_once`) leaves the second copy standing and the presence
    assertion never fires: exactly the WRONGLY PASSED failure this control
    exists to catch. Used only for the whole-text presence checks (L1-L6,
    L8); the S1/S2/S3 line- and paragraph-scoped mutations stay single-site
    via `_replace_once`/`_mutate_line`, since those targets are confirmed
    single-occurrence within their scoped line or paragraph.

    Whitespace-tolerant (see `_flex_pattern`)."""
    pattern = _flex_pattern(target)
    assert pattern.search(text) is not None, f"target not found in text: {target!r}"
    return pattern.sub(replacement, text)


def _mutate_block(text: str, anchor: str, transform) -> str:
    """Find the single logical block starting with *anchor*, apply *transform*
    to the whole block, and return the reassembled text. Asserts exactly one
    match exists.

    Block-scoped rather than physical-line-scoped, matching what
    `_find_unique_block` reads — otherwise re-wrapping a pinned literal onto a
    continuation line silently takes the mutator's target out of reach and the
    control stops being a control."""
    lines = text.splitlines(keepends=True)
    matches = [i for i, ln in enumerate(lines) if ln.startswith(anchor)]
    assert len(matches) == 1, f"expected exactly one line starting with {anchor!r}, found {len(matches)}"
    idx = matches[0]
    end = _block_end(lines, idx)
    block = "".join(lines[idx:end])
    return "".join(lines[:idx]) + transform(block) + "".join(lines[end:])


def _duplicate_line(text: str, anchor: str) -> str:
    """Find the single line starting with *anchor* and duplicate it — used by
    the anchor-arity controls to prove a scoped assertion does not silently
    pick the first of several matches."""
    lines = text.splitlines(keepends=True)
    matches = [i for i, ln in enumerate(lines) if ln.startswith(anchor)]
    assert len(matches) == 1, f"expected exactly one line starting with {anchor!r}, found {len(matches)}"
    idx = matches[0]
    lines.insert(idx, lines[idx])
    return "".join(lines)


def _append_to_block(block: str, suffix: str) -> str:
    nl = "\n" if block.endswith("\n") else ""
    core = block[:-1] if nl else block
    return f"{core} {suffix}{nl}"


def _strip_from_block(block: str, target: str) -> str:
    return _replace_once(block, target)


def _break_literal_across_lines(text: str, literal: str) -> str:
    """Reflow *literal* in *text* so every space inside it becomes a line break.

    The fixture for the false-RED direction: the literal is present and
    unchanged, only its wrapping moved. A raw `literal in text` test reports a
    failure for that, which is why SKILL-body.md's two pinned-literal lines had
    been stretched to 186 and 258 characters against a file that wraps at ~95.
    Raises if the construction did not in fact break the literal."""
    pattern = _flex_pattern(literal)
    match = pattern.search(text)
    assert match is not None, f"target not found in text: {literal!r}"
    broken = _WS.sub("\n", match.group(0))
    # Guard on THIS occurrence, not on the whole document: a literal that also
    # appears elsewhere (the bound is stated twice in the rubric) would otherwise
    # mask a fixture that broke nothing.
    if literal in broken:
        raise ValueError(f"fixture did not break the literal across lines: {literal!r}")
    return text[: match.start()] + broken + text[match.end():]


def _duplicate_bound_paragraph(body: str) -> str:
    """Duplicate the Turn discipline bound paragraph, so the S3 arity guard sees
    two matches instead of one.

    The comment above S3 states it is the sole assertion protecting the
    second-order -> Phase 2 edge, and the arity guard is the part that stops that
    assertion going vacuous when the paragraph is split or duplicated. It was the
    untested half of the sole protection for that edge."""
    section, _ = _extract_turn_discipline_section(body)
    assert section is not None, "could not locate Turn discipline section"
    paragraphs = section.split("\n\n")
    bound_indices = [i for i, para in enumerate(paragraphs) if _contains(para, _BOUND)]
    assert len(bound_indices) == 1, (
        f"expected exactly one bound paragraph, found {len(bound_indices)}"
    )
    idx = bound_indices[0]
    paragraphs.insert(idx, paragraphs[idx])
    return body.replace(section, "\n\n".join(paragraphs), 1)


def _reinstate_hard_wrapped(base: str, literal: str) -> str:
    """Reinstate *literal* into *base* inside a paragraph hard-wrapped at
    `_WRAP_WIDTH`, with the wrap boundary falling INSIDE the literal.

    This is the shape a real regression takes in this repo: someone re-adds
    prose and the editor or formatter reflows it at the file's own width. The
    raw `literal in text` test the gate used before CR-01 is blind to exactly
    this, which is how the rubric's Usage Note shipped an unbounded re-score
    instruction with the gate green.

    The two guards below make the fixture self-proving: the constructed text
    must NOT contain the literal contiguously (otherwise the control would pass
    for the trivial unwrapped reason and prove nothing about wrapping), and
    must contain it once whitespace is normalised (otherwise the fixture is not
    a reinstatement at all). If either guard trips, this raises rather than
    handing back a vacuous fixture."""
    for filler in range(0, 80):
        lead = "The analysis re-scores, " + ("fixes it again, " * filler)
        sentence = f"{lead}{literal}, however many passes that takes."
        wrapped = "\n".join(textwrap.wrap(sentence, width=_WRAP_WIDTH))
        if literal not in wrapped and _contains(wrapped, literal):
            return base + "\n\n" + wrapped + "\n"
    raise ValueError(
        f"could not build a hard-wrapped fixture splitting the literal: {literal!r}"
    )


def _mutate_bound_paragraph_strip_second_order(body: str) -> str:
    """N13: strip `second-order` from the Turn discipline bound paragraph
    ONLY. A whole-text str.replace(..., 1) is not used here — `second-order`
    occurs earlier in the Step 0 trigger table than in Turn discipline in the
    current file, so a naive single-site replace would hit the wrong
    occurrence if the document were ever reordered. Slicing out the bound
    paragraph and mutating only that slice keeps the control targeting what
    it claims to target regardless of document order."""
    section, _ = _extract_turn_discipline_section(body)
    assert section is not None, "could not locate Turn discipline section"
    paragraphs = section.split("\n\n")
    bound_indices = [i for i, p in enumerate(paragraphs) if _contains(p, _BOUND)]
    assert len(bound_indices) == 1, f"expected exactly one bound paragraph, found {len(bound_indices)}"
    idx = bound_indices[0]
    original_paragraph = paragraphs[idx]
    assert _contains(original_paragraph, _SECOND_ORDER), "bound paragraph does not contain second-order"
    mutated_paragraph = _replace_once(original_paragraph, _SECOND_ORDER)
    mutated_section = section.replace(original_paragraph, mutated_paragraph, 1)
    mutated_body = body.replace(section, mutated_section, 1)
    return mutated_body


def _run_self_test() -> int:
    body, contract, rubric, meta = _read_source_files()

    offenders: list[str] = []

    def _report(label: str, ok: bool, detail: str = "") -> None:
        if ok:
            print(f"check-loop-closure --self-test: {label} PASS")
        else:
            print(f"check-loop-closure --self-test: {label} FAIL — {detail}")
            offenders.append(label)

    # (a) Positive control: the live tree itself must be clean. If it is not,
    # the self-test fails — a gate whose positive control is not green is
    # measuring nothing.
    live_failures = _check_loop_closure(body, contract, rubric, meta)
    _report(
        "positive control (live tree)",
        not live_failures,
        f"live tree has {len(live_failures)} failure(s): {'; '.join(live_failures)}",
    )

    # Every fixture below is derived from the live text, so a live tree that is
    # missing a pinned literal makes the next mutator raise `target not found in
    # text` — the remaining controls never run and the operator gets a traceback
    # in place of the diagnostic table the self-test exists to print. That is
    # also the most likely reason someone runs --self-test at all: the live gate
    # went red and they want to know whether the gate or the content broke.
    # Short-circuit with the diagnosis, and exit 1 deliberately rather than
    # coincidentally (Python's uncaught-exception code).
    if live_failures:
        sys.stderr.write(
            "check-loop-closure --self-test: cannot run the negative controls — the "
            "live tree is not clean, and every fixture is derived from it. Fix the "
            "live tree first:\n"
            + "".join(f"  {msg}\n" for msg in live_failures)
        )
        return 1

    def _guarded(label: str, thunk):
        """Run *thunk*, converting any fixture-construction error into a reported
        FAIL. A fixture that cannot be built is a control that did not run — the
        self-test must say so in its own table, not abort the remaining controls
        with a traceback."""
        try:
            return thunk(), True
        except Exception as exc:  # noqa: BLE001 — deliberately broad; see docstring
            _report(
                label,
                False,
                f"fixture construction failed: {type(exc).__name__}: {exc}",
            )
            return None, False

    # --- Negative controls: table of (label, mutated-text-thunk, which-check, expected-substring) ---

    def check_body(text: str) -> list[str]:
        return _check_body_text(text)

    def check_contract(text: str) -> list[str]:
        return _check_input_contract_text(text)

    def check_rubric(text: str) -> list[str]:
        return _check_rubric_text(text)

    def check_meta(text: str) -> list[str]:
        return _check_meta_text(text)

    negative_controls = [
        (
            "N1 (body: strip L1 bound)",
            lambda: _strip_everywhere(body, _BOUND),
            check_body,
            f'{_BODY_NAME}: missing the re-entry bound',
        ),
        (
            "N2 (body: strip L3 Phase-1 route)",
            lambda: _strip_everywhere(body, _PHASE1_ROUTE),
            check_body,
            f'{_BODY_NAME}: missing the Phase-1 re-entry route',
        ),
        (
            "N3 (body: strip L4 firing record)",
            lambda: _strip_everywhere(body, _FIRING_RECORD),
            check_body,
            f'{_BODY_NAME}: missing the re-entry firing record',
        ),
        (
            "N4 (body: strip L2 degradation path — occurs twice in the real "
            "text, so every occurrence must be stripped for the control to "
            "be load-bearing)",
            lambda: _strip_everywhere(body, _DEGRADE),
            check_body,
            f'{_BODY_NAME}: missing the degradation path',
        ),
        (
            "N5 (body: reinstate X1 on the Repeat line)",
            lambda: _mutate_block(body, _S1_ANCHOR, lambda b: _append_to_block(b, _UNBOUNDED_REPEAT)),
            check_body,
            f'{_BODY_NAME}: unbounded Repeat instruction still present',
        ),
        (
            "N6 (body: strip re-perception pass from the Repeat line only)",
            lambda: _mutate_block(body, _S1_ANCHOR, lambda b: _strip_from_block(b, _RE_PERCEPTION_PASS)),
            check_body,
            f'{_BODY_NAME}: the "{_S1_ANCHOR}" line is missing "{_RE_PERCEPTION_PASS}"',
        ),
        (
            "N7 (body: strip re-entry from the Phase 3 exit line only)",
            lambda: _mutate_block(body, _S2_ANCHOR, lambda b: _strip_from_block(b, _REENTRY_EXCEPTION)),
            check_body,
            f'{_BODY_NAME}: the Phase 3 exit-criterion line lost the re-entry exception clause',
        ),
        (
            "N8 (body: strip the completeness claim from the Phase 3 exit line)",
            lambda: _mutate_block(body, _S2_ANCHOR, lambda b: _strip_from_block(b, _COMPLETENESS_CLAIM)),
            check_body,
            f'{_BODY_NAME}: the Phase 3 exit-criterion line lost the completeness claim',
        ),
        (
            "N9 (input-contract: strip L5 mid-run scope)",
            lambda: _strip_everywhere(contract, _MIDRUN_SCOPE),
            check_contract,
            f'{_CONTRACT_NAME}: missing the mid-run scope clause',
        ),
        (
            "N10 (input-contract: strip L6 per-delegation prohibition)",
            lambda: _strip_everywhere(contract, _NO_PER_DELEGATION),
            check_contract,
            f'{_CONTRACT_NAME}: missing the per-delegation prohibition',
        ),
        (
            "N11 (rubric: strip L8 bound)",
            lambda: _strip_everywhere(rubric, _BOUND),
            check_rubric,
            f'{_RUBRIC_NAME}: missing the re-entry bound',
        ),
        (
            "N12 (rubric: reinstate X2 unbounded re-score)",
            lambda: rubric + "\n" + _UNBOUNDED_RESCORE + "\n",
            check_rubric,
            f'{_RUBRIC_NAME}: unbounded re-score instruction still present',
        ),
        (
            "N16 (rubric: reinstate X3 — the reworded 'start over' instruction)",
            lambda: rubric + "\n" + _UNBOUNDED_RESCORE_ALT + "\n",
            check_rubric,
            f'{_RUBRIC_NAME}: unbounded re-score instruction still present in its reworded form',
        ),
        (
            "N17 (rubric: reinstate X3 hard-wrapped — the exact two-blind-spot "
            "shape that shipped the Usage Note contradiction)",
            lambda: _reinstate_hard_wrapped(rubric, _UNBOUNDED_RESCORE_ALT),
            check_rubric,
            f'{_RUBRIC_NAME}: unbounded re-score instruction still present in its reworded form',
        ),
        (
            "N18 (rubric: strip L11, the Usage Note's bounded remedy)",
            lambda: _strip_everywhere(rubric, _USAGE_NOTE_BOUND),
            check_rubric,
            f'{_RUBRIC_NAME}: the Usage Note no longer brings its closing re-score instruction',
        ),
        (
            "N19 (input-contract: strip L12, the artifact-tracking landing point)",
            lambda: _strip_everywhere(contract, _MIDRUN_LANDING),
            check_contract,
            f'{_CONTRACT_NAME}: the mid-run re-open does not route its answer by which artifact',
        ),
        (
            "N20 (body: strip L13, the widened mid-run route)",
            lambda: _strip_everywhere(body, _MIDRUN_LANDING_BODY),
            check_body,
            f'{_BODY_NAME}: the mid-run re-open route is not widened past Criterion 1',
        ),
        (
            "N21 (body: strip L14, the clause subordinating the degradation "
            "sentence to the edge-scoped bound)",
            lambda: _strip_everywhere(body, _BOUND_SUBORDINATION),
            check_body,
            f'{_BODY_NAME}: the degradation sentence is not subordinated to the edge-scoped bound',
        ),
        # N22-N26 cover the five check branches that had no negative control
        # at all. An unexercised assertion is one nobody has shown can fire.
        (
            "N22 (input-contract: strip L7, the AskUserQuestion tool reference)",
            lambda: _strip_everywhere(contract, _ASK_TOOL),
            check_contract,
            f'{_CONTRACT_NAME}: missing the AskUserQuestion tool reference',
        ),
        (
            "N23 (input-contract: strip L7b, the unavailable-fallback clause)",
            lambda: _strip_everywhere(contract, _ASK_FALLBACK),
            check_contract,
            f'{_CONTRACT_NAME}: missing the AskUserQuestion-unavailable fallback clause',
        ),
        (
            "N24 (rubric: strip L9, the Turn discipline cross-reference)",
            lambda: _strip_everywhere(rubric, _TURN_DISCIPLINE),
            check_rubric,
            f'{_RUBRIC_NAME}: missing the Turn discipline cross-reference',
        ),
        (
            "N25 (body: rename the Turn discipline heading — the section becomes "
            "unlocatable)",
            lambda: body.replace(_TURN_DISCIPLINE_HEADING, "### Turn budget", 1),
            check_body,
            f'{_BODY_NAME}: could not locate the "{_TURN_DISCIPLINE_HEADING}" section',
        ),
        (
            "N26 (body: duplicate the bound paragraph — exercises S3's arity "
            "guard, the untested half of the sole assertion protecting the "
            "second-order edge)",
            lambda: _duplicate_bound_paragraph(body),
            check_body,
            f"{_BODY_NAME}: expected exactly one paragraph in Turn discipline containing",
        ),
        (
            "N27 (body: invert the bound with 'more than' — the bare noun phrase "
            "survives, the rule does not)",
            lambda: _strip_everywhere(
                body,
                _BOUND_BODY,
                "Each edge fires more than **at most one re-perception pass** per analysis.",
            ),
            check_body,
            f'{_BODY_NAME}: the bound has lost its polarity carrier',
        ),
        (
            "N28 (rubric: invert the bound with 'not' — a plain substring test "
            "swallows the negation whole)",
            lambda: _strip_everywhere(
                rubric,
                _BOUND_RUBRIC,
                "revise the analysis and re-score — not bounded to "
                "**at most one re-perception pass** per analysis",
            ),
            check_rubric,
            f'{_RUBRIC_NAME}: the bound has lost its polarity carrier',
        ),
        (
            "N29 (body: duplicate the Turn discipline heading — a duplicate must "
            "report distinctly from a missing heading, not be silently accepted)",
            lambda: _duplicate_line(body, _TURN_DISCIPLINE_HEADING),
            check_body,
            f'{_BODY_NAME}: expected exactly one "{_TURN_DISCIPLINE_HEADING}" heading, found 2',
        ),
        (
            "N30 (body: demote the Turn discipline heading one level — "
            "'#### Turn discipline' CONTAINS the anchor, so a substring search "
            "accepted it)",
            lambda: body.replace(
                _TURN_DISCIPLINE_HEADING, "#" + _TURN_DISCIPLINE_HEADING, 1
            ),
            check_body,
            f'{_BODY_NAME}: could not locate the "{_TURN_DISCIPLINE_HEADING}" section',
        ),
        (
            "N31 (body: relocate L3 out of its owning paragraph — whole-text "
            "presence still holds, the scoped assertion must not)",
            lambda: _mutate_block(
                body, _S4_ANCHOR, lambda b: _strip_from_block(b, _PHASE1_ROUTE)
            )
            + "\n\n"
            + _PHASE1_ROUTE
            + "\n",
            check_body,
            f'{_BODY_NAME}: missing the Phase-1 re-entry route from the paragraph that owns it',
        ),
        (
            "N32 (body: replace the Phase 3 exception clause with its negation — "
            "the old seven-character 're-entry' token survived this)",
            lambda: _mutate_block(
                body,
                _S2_ANCHOR,
                lambda b: _strip_from_block(b, _REENTRY_EXCEPTION).replace(
                    "REMOVED", "and this exit criterion admits no re-entry", 1
                ),
            ),
            check_body,
            f'{_BODY_NAME}: the Phase 3 exit-criterion line lost the re-entry exception clause',
        ),
        (
            "N33 (body: duplicate the Criterion-1 paragraph anchor)",
            lambda: _duplicate_line(body, _S4_ANCHOR),
            check_body,
            f'{_BODY_NAME}: expected exactly one paragraph starting with "{_S4_ANCHOR}", found 2',
        ),
        (
            "N34 (meta: strip L15, the AskUserQuestion frontmatter permission the "
            "mid-run re-open edge depends on)",
            lambda: _strip_everywhere(meta, _ASK_PERMITTED),
            check_meta,
            f'{_META_NAME}: the mid-run re-open edge requires "{_ASK_PERMITTED}"',
        ),
        (
            "N35 (input-contract: strip L16, the fallback's mid-run branch)",
            lambda: _strip_everywhere(contract, _ASK_FALLBACK_MIDRUN),
            check_contract,
            f'{_CONTRACT_NAME}: the AskUserQuestion-unavailable fallback has no mid-run branch',
        ),
        (
            "N36 (body: restore the superseded five-edge enumeration)",
            lambda: _strip_everywhere(body, _EDGE_COUNT, _SUPERSEDED_EDGE_COUNT),
            check_body,
            f'{_BODY_NAME}: the edge enumeration double-counts the Fix/Repeat loop',
        ),
        (
            "N37 (body: strip L18, the one-edge-two-statements clause)",
            lambda: _strip_everywhere(body, _ONE_EDGE_TWO_STATEMENTS),
            check_body,
            f"{_BODY_NAME}: the enumeration no longer says the Fix/Repeat loop",
        ),
        (
            "N13 (body: strip second-order from the bound paragraph only)",
            lambda: _mutate_bound_paragraph_strip_second_order(body),
            check_body,
            f'{_BODY_NAME}: the bound paragraph in Turn discipline does not name the second-order edge',
        ),
        (
            "N14 (body: reinstate X1 hard-wrapped at the file's own width — the "
            "shape a real regression takes; this is the control whose absence "
            "let a whitespace-sensitive removal check ship)",
            lambda: _reinstate_hard_wrapped(body, _UNBOUNDED_REPEAT),
            check_body,
            f'{_BODY_NAME}: unbounded Repeat instruction still present',
        ),
        (
            "N15 (rubric: reinstate X2 hard-wrapped at the file's own width)",
            lambda: _reinstate_hard_wrapped(rubric, _UNBOUNDED_RESCORE),
            check_rubric,
            f'{_RUBRIC_NAME}: unbounded re-score instruction still present',
        ),
    ]

    mutated_body_n1: str | None = None
    mutated_contract_n9: str | None = None
    mutated_body_n13: str | None = None

    for label, make_mutated, checker, expected_substring in negative_controls:
        mutated, built = _guarded(label, make_mutated)
        if not built:
            continue
        if label.startswith("N1 "):
            mutated_body_n1 = mutated
        if label.startswith("N9 "):
            mutated_contract_n9 = mutated
        if label.startswith("N13 "):
            mutated_body_n13 = mutated
        failures = checker(mutated)
        if not failures:
            _report(label, False, "WRONGLY PASSED (expected a failure, got none)")
            continue
        if not any(expected_substring in f for f in failures):
            _report(
                label,
                False,
                f"failed for the WRONG reason (expected substring {expected_substring!r}, "
                f"got: {'; '.join(failures)})",
            )
            continue
        _report(label, True)

    # N13 scope check: prove the bound-paragraph mutation is confined to that
    # paragraph.
    #
    # This assertion used to read `n13_mutated.count(_SECOND_ORDER) >= 1`, which
    # could not fail. `SKILL-body.md` names `second-order` many times and the
    # mutation is built on `_replace_once`, which removes at most one, so the
    # post-mutation count could never reach 0 — the only value the old assertion
    # rejected. It passed for "removed the right one", for "removed nothing at
    # all", and for "removed the wrong one" alike. A control that distinguishes
    # nothing reads as coverage while providing none — the same defect class as
    # the bug `_strip_everywhere` was written to fix.
    #
    # The replacement asserts the DELTA (exactly one occurrence gone) and the
    # LOCATION (the one that went was the bound paragraph's).
    if mutated_body_n13 is None:
        _report(
            "N13 scope check (exactly one occurrence removed, and it was the bound "
            "paragraph's)",
            False,
            "N13's fixture could not be built, so its scope could not be checked",
        )
        return 1
    before = body.count(_SECOND_ORDER)
    after = mutated_body_n13.count(_SECOND_ORDER)
    section_after, _ = _extract_turn_discipline_section(mutated_body_n13)
    bound_paras_after = [
        para
        for para in (section_after or "").split("\n\n")
        if _contains(para, _BOUND)
    ]
    bound_para_after = bound_paras_after[0] if len(bound_paras_after) == 1 else ""
    _report(
        "N13 scope check (exactly one occurrence removed, and it was the bound "
        "paragraph's)",
        after == before - 1
        and len(bound_paras_after) == 1
        and not _contains(bound_para_after, _SECOND_ORDER),
        f"before={before} after={after} (expected {before - 1}); bound paragraphs "
        f"found={len(bound_paras_after)} (expected 1); bound paragraph still names "
        f"second-order={_contains(bound_para_after, _SECOND_ORDER)} (expected False)",
    )

    # --- (b) Anti-masking controls ---
    if mutated_contract_n9 is None or mutated_body_n1 is None:
        _report(
            "anti-masking controls",
            False,
            "the N1 and/or N9 fixture could not be built, so attribution could not "
            "be checked",
        )
        return 1

    # The two controls that used to sit here mutated ONE file at a time and
    # asserted the other file's basename did not appear in the message set. They
    # could not fail: no message string in `_check_body_text` contains the
    # literal "input-contract.md" and none in `_check_input_contract_text`
    # contains "SKILL-body.md", so the "wrongly names the other file" term was
    # always False and the controls collapsed onto N1 and N9, which had already
    # run. They added two free green lines and asserted nothing.
    #
    # The replacement mutates BOTH files at once and asserts each file's failure
    # set is exactly what that file's own check produces in isolation, with no
    # message left unattributed to either. That is a real claim about the
    # aggregator, and it is falsifiable — the meta-control below proves the
    # predicate can return False rather than being structurally incapable of it.
    def _attribution_ok(
        failures: list[str], body_alone: list[str], contract_alone: list[str]
    ) -> bool:
        body_msgs = [f for f in failures if f.startswith(_BODY_NAME + ":")]
        contract_msgs = [f for f in failures if f.startswith(_CONTRACT_NAME + ":")]
        return (
            bool(body_msgs)
            and bool(contract_msgs)
            and body_msgs == body_alone
            and contract_msgs == contract_alone
            and len(body_msgs) + len(contract_msgs) == len(failures)
        )

    body_alone = _check_body_text(mutated_body_n1)
    contract_alone = _check_input_contract_text(mutated_contract_n9)
    simultaneous = _check_loop_closure(mutated_body_n1, mutated_contract_n9, rubric, meta)
    _report(
        "anti-masking (simultaneous body+contract mutations stay separately "
        "attributed, and nothing leaks between the two message sets)",
        _attribution_ok(simultaneous, body_alone, contract_alone),
        f"body-attributed={len([f for f in simultaneous if f.startswith(_BODY_NAME + ':')])} "
        f"(expected {len(body_alone)}), contract-attributed="
        f"{len([f for f in simultaneous if f.startswith(_CONTRACT_NAME + ':')])} "
        f"(expected {len(contract_alone)}), total={len(simultaneous)}; "
        f"failures: {'; '.join(simultaneous)}",
    )

    # Meta-control: feed the attribution predicate a deliberately mis-attributed
    # failure list. If it accepts that, it is incapable of failing and the
    # control above proves nothing — which is precisely the defect WR-02 named.
    leaked = simultaneous + [
        f"{_BODY_NAME}: a leaked message no single-file check ever produced"
    ]
    _report(
        "anti-masking meta-control (the attribution predicate can return False)",
        not _attribution_ok(leaked, body_alone, contract_alone),
        "the attribution predicate accepted a deliberately mis-attributed failure "
        "list — it cannot fail, so the control above is not load-bearing",
    )

    # --- (c) Anchor-arity controls ---
    for arity_label, arity_anchor in (
        ("Repeat line", _S1_ANCHOR),
        ("Phase 3 exit line", _S2_ANCHOR),
    ):
        label = f"anchor-arity (duplicated {arity_label} reports 'expected exactly one')"
        duplicated, built = _guarded(label, lambda a=arity_anchor: _duplicate_line(body, a))
        if not built:
            continue
        arity_failures = _check_body_text(duplicated)
        _report(
            label,
            any("expected exactly one" in f and arity_anchor in f for f in arity_failures),
            f"failures: {'; '.join(arity_failures)}",
        )

    # --- (d) Reflow controls: the false-RED direction of the same defect.
    # A pinned literal that merely MOVED across a wrap boundary — present,
    # unchanged, only re-wrapped — must not fail. Without these, the source has
    # to stay hand-shaped around the matcher, and every routine reflow is a
    # spurious red the standard remedy (re-unwrap the line) further entrenches.
    reflow_controls = [
        ("body / L3 Phase-1 route", body, _PHASE1_ROUTE, check_body),
        ("body / L10a completeness claim", body, _COMPLETENESS_CLAIM, check_body),
        ("rubric / L8 bound", rubric, _BOUND, check_rubric),
        ("contract / L12 landing point", contract, _MIDRUN_LANDING, check_contract),
    ]
    for reflow_label, source, literal, checker in reflow_controls:
        label = (
            f"reflow control ({reflow_label} re-wrapped, content unchanged, "
            f"gate stays green)"
        )
        reflowed, built = _guarded(
            label, lambda s=source, l=literal: _break_literal_across_lines(s, l)
        )
        if not built:
            continue
        failures = checker(reflowed)
        _report(
            label,
            not failures,
            f"a pure re-wrap produced {len(failures)} failure(s): {'; '.join(failures)}",
        )

    if offenders:
        sys.stderr.write(
            "check-loop-closure --self-test: FAIL — these controls wrongly passed or "
            "failed for the wrong reason: " + ", ".join(offenders) + "\n"
        )
        return 1

    print("check-loop-closure --self-test: PASS")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description="HARN-02: assert every re-entry edge and its bound is present "
        "across the three shared/ source files."
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run the positive control, negative controls, and anti-masking/anchor-arity controls",
    )
    args = parser.parse_args()

    _require_python_version()

    if args.self_test:
        sys.exit(_run_self_test())

    _validate_live_tree()


if __name__ == "__main__":
    main()
