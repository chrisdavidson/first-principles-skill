#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml>=6.0"]
# ///
"""HARN-03 gate (stub-surface half): assert the `## Focused-mode validation`
section that plan 03-02 inlined into all 13 slash-invocable focused stubs is
present, correctly placed, correctly counted, and carries every load-bearing
literal — and stays absent from the `first-principles-analysis` launcher.

Phase 3 (Focused-Mode Parity) closed PAR-02 by inlining a single canonical
snippet (`shared/spine/focused-validation-step.md`) into all 13
`shared/skills/<slug>/SKILL.md` sources via a new `{{FOCUSED_VALIDATION}}`
token (03-02), after amending the wrapper sentence that used to contradict it
and stating a completion condition for every technique that lacked one
(03-01). This gate asserts those two plans' combined result against the
**emitted** tree — `first-principles/skills/<slug>/SKILL.md` — never against
`shared/`, because the emitted tree is what a slash-invoked skill actually
loads at runtime; DUAL-04 (`sync-content.py --check`) already guarantees
`shared/` and the emitted tree agree, and the v8.14 failure mode this
project's gate culture guards against was a defect that existed only on the
emitted surface (D-11).

Scope: this file guards the STUB surface only. The agent-surface assertions
(Step 0 names Validate, the agent-body proportionality note) and the
cross-surface parity check between the two proportionality notes are plan
03-04's job, built on top of the machinery this file ships — the whitespace
matching, the ID-based negative-control matcher, and the anchor-control
coverage ratchet are all written to be extended, not duplicated.

This gate is not yet registered in `scripts/check-firewall-battery.sh` —
Phase 4 / HARN-04 owns registration and the battery tally bump.

Usage:
    python3 scripts/check-focused-parity.py [--self-test]

Exit codes:
    0  all checks passed
    1  validation failure (a `Stub-N` assertion, the anchor coherence check,
       or the anchor-control coverage ratchet failed)
    2  environment error (Python <3.12, the plugin skills directory missing)

--self-test: runs an offline control battery built by mutating in-memory
             copies of the real emitted stub bodies, and exits 0 if every
             control behaves as intended; exits 1 on any wrong-pass or
             wrong-reason failure. Never writes to the repository.

## What this gate does not assert

Stated here, in the pattern `check-act-limb.py` (HARN-01) established for
this repo's gate culture, rather than left for the next maintainer to
rediscover.

- It asserts that named literals are PRESENT, in the right file, at the
  right count. It does not assert that the surrounding prose MEANS what
  those literals imply — a stub that retains every anchored literal but
  states the opposite intent in the connective prose between them passes.
- Stub-8 asserts every technique states ONE of the four recognised
  completion-condition forms. It does not assert that the recognised form is
  the RIGHT one for that technique, or that the technique's own numbered
  steps actually satisfy it — that is a semantic property no literal-anchor
  gate can reach.
- Reaching semantic direction needs a live-measurement layer, which this
  project deliberately does not gate on: a K-of-5 result is a recorded
  observation, not a gate (governing record section 2 item 3,
  `docs/v8.7-constraint-teardown.md`).
"""

from __future__ import annotations

import argparse
import re
import sys
import textwrap
from pathlib import Path

# Adjust sys.path so _skill_io is importable when invoked from any cwd —
# mirrors scripts/check-trigger-collisions.py.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _skill_io import PLUGIN_SKILLS_DIR, iter_plugin_skills  # noqa: E402

# ---------------------------------------------------------------------------
# Path / structural constants. No leading underscore: not ratchet-tracked
# (the ratchet only scans `_[A-Z]...` names), matching this repo's existing
# gates' convention of leaving plain path/count constants untracked.
# ---------------------------------------------------------------------------

LAUNCHER_SLUG = "first-principles-analysis"
EXPECTED_STUB_COUNT = 13

# ---------------------------------------------------------------------------
# Whitespace-insensitive matching machinery — copied in shape from
# scripts/check-loop-closure.py (`_WS`, `_WRAP_WIDTH`, `_flat`, `_contains`,
# `_flex_pattern`, `_replace_once`, credited per file), because Phase 2
# shipped a gate whose pinned literals were defeated by ordinary Markdown
# hard-wrapping and had to repair it. Every assertion and every fixture
# mutation in this file goes through this layer; a raw `in text` test
# against a multi-word literal is forbidden.
# ---------------------------------------------------------------------------

_WS = re.compile(r"\s+")

# The reflow width the self-test's positive reflow control (p) re-wraps every
# real stub body to, deliberately distinct from the ~78-95 column width the
# real files ship at, so the control proves whitespace tolerance rather than
# happening to match the shipped wrap point.
_WRAP_WIDTH = 48


def _flat(text: str) -> str:
    """Collapse every whitespace run to a single space.

    Copied in shape from `scripts/check-loop-closure.py`'s `_flat`. Every
    presence and absence assertion in this module compares whitespace-
    normalised text against a whitespace-normalised literal — a raw
    `literal in text` test against a multi-word literal is forbidden, because
    a pinned phrase that straddles a hard-wrap line break reads as two
    different characters (space vs. newline) to a naive substring test.
    """
    return _WS.sub(" ", text)


def _contains(text: str, literal: str) -> bool:
    """Whitespace-insensitive containment — the only membership test this
    module's assertions may use against a multi-word pinned literal."""
    return _flat(literal) in _flat(text)


def _flex_pattern(target: str) -> re.Pattern[str]:
    """A pattern matching *target* with any whitespace run standing in for
    each of its spaces — the fixture-side counterpart of `_flat()`, copied in
    shape from `scripts/check-loop-closure.py`. Used both to COUNT and to
    LOCATE occurrences of a literal in raw (non-flattened) text, since
    flattening text loses the character offsets a placement assertion needs.
    """
    return re.compile(r"\s+".join(re.escape(w) for w in _flat(target).strip().split(" ")))


def _count_flex(text: str, literal: str) -> int:
    """Whitespace-insensitive occurrence count of *literal* in *text*."""
    return len(_flex_pattern(literal).findall(text))


def _find_flex(text: str, literal: str) -> re.Match[str] | None:
    """Whitespace-insensitive first-occurrence search of *literal* in *text*,
    returning a Match (so callers can read `.start()`) rather than a bool."""
    return _flex_pattern(literal).search(text)


def _replace_once(text: str, target: str, replacement: str = "") -> str:
    """Single-site substitution — never a broad sweep, so a fixture mutation
    cannot accidentally remove a second occurrence and make a control pass
    for a reason it did not intend. Copied in shape from
    `scripts/check-loop-closure.py`'s `_replace_once`; raises loudly if the
    target is not found, so a mutation cannot silently degrade into a no-op.
    """
    pattern = _flex_pattern(target)
    if pattern.search(text) is None:
        raise AssertionError(f"target not found in text while building fixture: {target!r}")
    return pattern.sub(lambda _m: replacement, text, count=1)


# ---------------------------------------------------------------------------
# Content anchors. One module-level `_UPPER_SNAKE` constant per pinned
# literal or literal group, each with a comment naming the decision and
# requirement it serves. Every string is taken verbatim from
# `03-02-SUMMARY.md` / `03-01-SUMMARY.md` and confirmed live against the
# emitted tree before being pinned here — never retyped from memory.
# ---------------------------------------------------------------------------

# D-10/PAR-02: the section heading `{{FOCUSED_VALIDATION}}` opens with.
_STUB_SECTION_HEADING = "## Focused-mode validation"

# The heading `_extract_skill_content()` guarantees opens the inlined
# procedure slice — used as the "after the inlined procedure" placement
# anchor for Stub-2.
_WHEN_TO_REACH_HEADING = "## When to reach for this"

# The closing handoff sentence every stub ends with, used as the "before the
# closing handoff" placement anchor for Stub-2. Deliberately the fragment
# that names the agent, not the whole sentence, so it is immune to a
# reflow that moves the line break elsewhere in the sentence.
_CLOSING_HANDOFF_ANCHOR = "invoke the main `first-principles`"

# D-03: the three verdict-state literals, emitted verbatim and unconditionally.
_VERDICT_LITERALS: tuple[str, ...] = (
    "Focused-mode validation: satisfied",
    "Focused-mode validation: revised once, now satisfied",
    "Focused-mode validation: not satisfied - <reason>",
)

# D-03: the clause stating the verdict line is emitted on every run, not only
# on exception — "a silent run is indistinguishable from a run that skipped
# the check."
_UNCONDITIONAL_CLAUSE = "without exception"

# D-07: the inline `?` definition — the snippet defines the unverified mark
# without naming `read-at-source` / `reported-by-delegate`, which are
# undefined vocabulary outside `shared/spine/SKILL-body.md`.
_UNVERIFIED_MARK_CLAUSE = (
    "carried into the output marked with a `?` rather than dropped or "
    "silently asserted as fact"
)

# D-07 (negative half): these two provenance terms must appear in NEITHER the
# 13 stubs NOR the launcher — a stub has no provenance table to resolve them
# against.
_PROVENANCE_LEAK_TERMS: tuple[str, ...] = ("read-at-source", "reported-by-delegate")

# D-01: the amended wrapper clause that admits the validation step, replacing
# the contradiction the old wrapper sentence shipped.
_WRAPPER_ADMITS = "then run the focused-mode validation step below"

# D-01 (negative half): the retired wrapper clause the amendment replaced.
# Its presence anywhere (including the launcher, which never carried the new
# clause either) is the exact contradiction D-01 exists to close.
_WRAPPER_RETIRED = "produce only its canonical output sections"

# D-06: the four recognised completion-condition forms, keyed by name for
# readable failure messages. Verified live across all 13 emitted stubs
# (03-PATTERNS.md): 8 use the bold Exit-criterion line, five-whys uses the
# Stop-test heading, inversion/trade-off use the Output-contract heading, and
# estimate/theoretical-limit use the inline stop-criterion sentence.
_COMPLETION_CONDITION_FORMS: dict[str, str] = {
    "exit-criterion": "**Exit criterion:**",
    "stop-test-heading": "## Stop test",
    "output-contract-heading": "## Output contract",
    "inline-stop-criterion": "stop criterion",
}

# PAR-01: the five parity literals plan 03-01 put on the agent surface and
# plan 03-02 put on the stub surface via the same inlined snippet. Plan
# 03-04's cross-surface check requires the SAME five on both surfaces; this
# file only requires them present on the stub surface (D-11's scope for this
# plan).
_PARITY_LITERALS: tuple[str, ...] = (
    "six-criterion Self-Audit Gate",
    "six-section analysis document",
    "scope-proportionate",
    "does not acquire evidence",
    "stays marked",
)

# D-03: the one-pass revision bound.
_ONE_PASS_BOUND = "Revise at most one time."

# D-03 (negative half): no OTHER numeric revision bound may be stated
# anywhere in a stub — "revise twice", "revise two times", "revise N times"
# for any N other than the one-pass clause above.
_OTHER_BOUND_RE = re.compile(r"[Rr]evise\s+(?:twice|two\s+times|three\s+times|\d+\s+times)")


# ---------------------------------------------------------------------------
# The anchor-control coverage ratchet (D-12, copied in shape from
# `scripts/check-act-limb.py`'s WR-02 repair). Every module-level
# `_UPPER_SNAKE` constant defined above must be referenced at least three
# times in this file (its definition, at least one assertion, at least one
# control), or be listed in one of the two dicts below. EXEMPT is permanent
# and each entry must carry a one-sentence justification; PENDING is
# temporary debt and each entry must name the task that discharges it.
# ---------------------------------------------------------------------------

# --- ratchet-bookkeeping-begin ---
_ANCHOR_CONTROL_EXEMPT: dict[str, str] = {}
_ANCHOR_CONTROL_PENDING: dict[str, str] = {}
# --- ratchet-bookkeeping-end ---

# Re-entrancy sentinel guarding the dispatch control (r), copied in shape
# from `scripts/check-act-limb.py`'s `_HARN01_DISPATCH_REENTRANT`. Set only
# for the duration of the nested `main(["--self-test"])` call the dispatch
# control drives, and restored in a `finally` so an exception cannot leave it
# set and silently skip every later dispatch-control run.
_DISPATCH_REENTRANT = False


def _check_anchor_control_coverage(
    source: str,
    exempt: dict[str, str] | None = None,
    pending: dict[str, str] | None = None,
) -> list[str]:
    """Fail when a module-level anchor constant ships without a control.

    Enumerates every module-level `_UPPER_SNAKE` assignment in *source* and
    requires at least three references to each (definition + at least one
    assertion + at least one control), unless the name is listed in
    `_ANCHOR_CONTROL_EXEMPT` (permanent, must carry a justification) or in
    `_ANCHOR_CONTROL_PENDING` (temporary debt, must still be short — a
    pending entry that is no longer short is a stale ratchet entry and is
    itself reported).

    *exempt* and *pending* default to the module-level lists. They are
    injectable only so control (q) can drive every branch of this function
    against synthetic input — the ratchet is itself an assertion, and an
    assertion whose branches are never exercised is exactly what this gate
    exists to prevent elsewhere in the file.
    """
    failures: list[str] = []
    exempt_list = _ANCHOR_CONTROL_EXEMPT if exempt is None else exempt
    pending_list = _ANCHOR_CONTROL_PENDING if pending is None else pending
    marker_start = "# --- ratchet-bookkeeping-begin ---"
    marker_end = "# --- ratchet-bookkeeping-end ---"
    constant_re = re.compile(r"^(_[A-Z][A-Z0-9_]*)\s*(?::[^=\n]+)?=", re.MULTILINE)

    # Ratchet self-integrity: the two bookkeeping dicts and the dispatch
    # sentinel are machinery, not content anchors, so they are exempt from
    # the reference count — but a retyped machinery global would silently
    # disable the ratchet (or degrade control (r) to its nested-skip path),
    # so their TYPES are asserted here instead.
    if not isinstance(_ANCHOR_CONTROL_EXEMPT, dict) or not isinstance(
        _ANCHOR_CONTROL_PENDING, dict
    ):
        failures.append(
            "Coverage (D-12, ratchet integrity): _ANCHOR_CONTROL_EXEMPT and "
            "_ANCHOR_CONTROL_PENDING must both be dicts, found "
            f"{type(_ANCHOR_CONTROL_EXEMPT).__name__} and "
            f"{type(_ANCHOR_CONTROL_PENDING).__name__}"
        )
        return failures
    if not isinstance(_DISPATCH_REENTRANT, bool):
        failures.append(
            "Coverage (D-12, ratchet integrity): _DISPATCH_REENTRANT must be a bool, "
            f"found {type(_DISPATCH_REENTRANT).__name__} — a non-bool sentinel is "
            "truthy and silently turns control (r) into a permanent skip"
        )

    names = list(dict.fromkeys(constant_re.findall(source)))
    if not names:
        failures.append(
            "Coverage (D-12, anchor-control ratchet): the enumerator matched no "
            "module-level anchor constants — a ratchet that enumerates nothing is "
            "broken, not satisfied"
        )
        return failures

    start = source.find(marker_start)
    end = source.find(marker_end, start + 1) if start != -1 else -1
    if start == -1 or end == -1:
        failures.append(
            "Coverage (D-12, ratchet integrity): bookkeeping markers not found — "
            "cannot exclude the exempt/pending lists from the reference counts"
        )
        return failures
    counting_source = source[:start] + source[end + len(marker_end) :]

    for name in names:
        is_exempt = name in exempt_list
        is_pending = name in pending_list
        # Word-boundary count: a shorter anchor name that is a proper
        # substring of a longer one must not be credited with the longer
        # name's references.
        count = len(
            re.findall(rf"(?<![A-Za-z0-9_]){re.escape(name)}(?![A-Za-z0-9_])", counting_source)
        )
        if is_exempt and is_pending:
            failures.append(
                "Coverage (D-12, anchor-control ratchet): "
                f"{name} is listed in BOTH _ANCHOR_CONTROL_EXEMPT and "
                "_ANCHOR_CONTROL_PENDING — permanent and temporary are not both"
            )
            continue
        if is_exempt:
            if not str(exempt_list[name]).strip():
                failures.append(
                    "Coverage (D-12, anchor-control ratchet): "
                    f"{name} is exempt with an empty justification — an "
                    "unjustified exemption is an allow-list entry, not a decision"
                )
            continue
        if is_pending:
            if count >= 3:
                failures.append(
                    "Coverage (D-12, anchor-control ratchet): "
                    f"{name} is listed pending ({pending_list[name]}) but is "
                    f"already referenced {count} time(s) — a stale ratchet entry "
                    "is itself a finding; remove it from _ANCHOR_CONTROL_PENDING"
                )
            continue
        if count < 3:
            failures.append(
                "Coverage (D-12, anchor-control ratchet): "
                f"{name} is referenced {count} time(s), expected at least 3 "
                "(definition, at least one assertion, at least one control)"
            )

    for name in exempt_list:
        if name not in names:
            failures.append(
                "Coverage (D-12, anchor-control ratchet): exempt entry "
                f"{name} names no module-level anchor constant — stale"
            )
    for name in pending_list:
        if name not in names:
            failures.append(
                "Coverage (D-12, anchor-control ratchet): pending entry "
                f"{name} names no module-level anchor constant — stale"
            )
    return failures


def _check_anchor_coherence() -> list[str]:
    """Assert derived cross-anchor pairs still stand in the relation their
    derivation creates.

    This file has no derived anchor pairs YET — D-10's cross-surface parity
    check (deriving a shared token set from the agent-surface proportionality
    note and requiring it on the stub surface) is plan 03-04's addition, on
    top of this plan's stub-surface-only machinery. This function exists now,
    empty, so `_validate_files()`'s composition shape does not change when
    03-04 populates it — an empty coherence check that asserts nothing is
    honestly different from one that asserts something and always passes,
    and this docstring is where that honesty lives.
    """
    return []


# ---------------------------------------------------------------------------
# Stub-surface real-content checks.
# ---------------------------------------------------------------------------


def _load_real_stubs() -> dict[str, str]:
    """Read all emitted stub bodies from disk via `iter_plugin_skills()`.

    Returns slug -> body for all 14 generated skills (13 techniques plus the
    launcher). Never reads `shared/` (D-11).
    """
    return {slug: body for slug, _frontmatter, body in iter_plugin_skills()}


def _check_stub_surface(stubs: dict[str, str]) -> list[str]:
    """Validate the ten stub-surface assertions against *stubs*.

    *stubs* is a slug -> body mapping for all 14 generated skills. Operating
    on a plain dict rather than reading disk directly is what makes this
    function callable identically against the real emitted tree and against
    an in-memory self-test fixture — the shared checker `_check_negative`'s
    controls drive.

    Returns a list of failure strings, each beginning with a stable
    `Stub-N (<REQ-ID>, <label>): <detail>` check ID — the leading token
    `_check_negative` matches controls against.
    """
    failures: list[str] = []

    if LAUNCHER_SLUG not in stubs:
        failures.append(
            f"Stub-0 (PAR-02, fixture integrity): launcher slug {LAUNCHER_SLUG!r} "
            "is missing from the stub set — cannot check launcher exclusion"
        )
        return failures

    launcher_body = stubs[LAUNCHER_SLUG]
    non_launcher = {slug: body for slug, body in stubs.items() if slug != LAUNCHER_SLUG}

    # --- Stub-1 (PAR-02, count) ---------------------------------------
    if len(non_launcher) != EXPECTED_STUB_COUNT:
        failures.append(
            f"Stub-1 (PAR-02, count): {len(non_launcher)} non-launcher slugs are "
            f"present, expected exactly {EXPECTED_STUB_COUNT}"
        )
    carrying = sorted(
        slug for slug, body in non_launcher.items()
        if _count_flex(body, _STUB_SECTION_HEADING) >= 1
    )
    if len(carrying) == 0:
        failures.append(
            f"Stub-1 (PAR-02, count): ZERO non-launcher stubs carry "
            f"{_STUB_SECTION_HEADING!r} — vacuous-pass guard tripped (D-10); "
            f"expected exactly {EXPECTED_STUB_COUNT}"
        )
    elif len(carrying) != EXPECTED_STUB_COUNT:
        missing = sorted(set(non_launcher) - set(carrying))
        failures.append(
            f"Stub-1 (PAR-02, count): {len(carrying)} of {len(non_launcher)} "
            f"non-launcher stubs carry {_STUB_SECTION_HEADING!r}, expected exactly "
            f"{EXPECTED_STUB_COUNT}; missing: {missing}"
        )

    # --- Stub-2 (PAR-02, placement) ------------------------------------
    for slug, body in sorted(non_launcher.items()):
        count = _count_flex(body, _STUB_SECTION_HEADING)
        if count != 1:
            failures.append(
                f"Stub-2 (PAR-02, placement): {slug} carries "
                f"{_STUB_SECTION_HEADING!r} {count} time(s), expected exactly 1"
            )
            continue
        heading_match = _find_flex(body, _STUB_SECTION_HEADING)
        when_match = _find_flex(body, _WHEN_TO_REACH_HEADING)
        handoff_match = _find_flex(body, _CLOSING_HANDOFF_ANCHOR)
        assert heading_match is not None  # count == 1 guarantees a match
        if when_match is None:
            failures.append(
                f"Stub-2 (PAR-02, placement): {slug} is missing the "
                f"{_WHEN_TO_REACH_HEADING!r} anchor needed to check ordering"
            )
            continue
        if handoff_match is None:
            failures.append(
                f"Stub-2 (PAR-02, placement): {slug} is missing the closing "
                f"handoff anchor {_CLOSING_HANDOFF_ANCHOR!r} needed to check ordering"
            )
            continue
        if heading_match.start() <= when_match.start():
            failures.append(
                f"Stub-2 (PAR-02, placement): {slug}'s {_STUB_SECTION_HEADING!r} "
                f"occurs at or before the inlined procedure heading "
                f"{_WHEN_TO_REACH_HEADING!r}"
            )
        if heading_match.start() >= handoff_match.start():
            failures.append(
                f"Stub-2 (PAR-02, placement): {slug}'s {_STUB_SECTION_HEADING!r} "
                "occurs at or after the closing handoff sentence"
            )

    # --- Stub-3 (PAR-02, launcher exclusion) ---------------------------
    launcher_count = _count_flex(launcher_body, _STUB_SECTION_HEADING)
    if launcher_count != 0:
        failures.append(
            f"Stub-3 (PAR-02, launcher exclusion): the launcher stub carries "
            f"{_STUB_SECTION_HEADING!r} {launcher_count} time(s), expected 0"
        )

    # --- Stub-4 (D-03, verdict) -----------------------------------------
    for slug, body in sorted(non_launcher.items()):
        missing_verdicts = [v for v in _VERDICT_LITERALS if _count_flex(body, v) == 0]
        if missing_verdicts:
            failures.append(
                f"Stub-4 (D-03, verdict): {slug} is missing verdict literal(s): "
                f"{missing_verdicts}"
            )
        if _count_flex(body, _UNCONDITIONAL_CLAUSE) == 0:
            failures.append(
                f"Stub-4 (D-03, verdict): {slug} does not state the verdict line "
                f"is unconditional ({_UNCONDITIONAL_CLAUSE!r} not found)"
            )

    # --- Stub-5 (D-07, unverified mark) ---------------------------------
    for slug, body in sorted(non_launcher.items()):
        if _count_flex(body, _UNVERIFIED_MARK_CLAUSE) == 0:
            failures.append(
                f"Stub-5 (D-07, unverified mark): {slug} is missing the "
                f"unverified mark clause {_UNVERIFIED_MARK_CLAUSE!r}"
            )
    for slug, body in sorted(stubs.items()):
        for leaked in _PROVENANCE_LEAK_TERMS:
            if _count_flex(body, leaked) > 0:
                failures.append(
                    f"Stub-5 (D-07, unverified mark): {slug} leaks the undefined "
                    f"provenance term {leaked!r} — a stub has no provenance table "
                    "to resolve it against"
                )

    # --- Stub-6 (D-01, wrapper) ------------------------------------------
    for slug, body in sorted(non_launcher.items()):
        count = _count_flex(body, _WRAPPER_ADMITS)
        if count != 1:
            failures.append(
                f"Stub-6 (D-01, wrapper): {slug} carries {_WRAPPER_ADMITS!r} "
                f"{count} time(s), expected exactly 1"
            )

    # --- Stub-7 (D-01, wrapper retired) -----------------------------------
    for slug, body in sorted(stubs.items()):
        count = _count_flex(body, _WRAPPER_RETIRED)
        if count != 0:
            failures.append(
                f"Stub-7 (D-01, wrapper retired): {slug} carries the retired "
                f"clause {_WRAPPER_RETIRED!r} {count} time(s), expected 0"
            )

    # --- Stub-8 (D-06, completion condition) ------------------------------
    matched_slugs: list[str] = []
    unmatched_slugs: list[str] = []
    for slug, body in sorted(non_launcher.items()):
        forms = [
            name for name, literal in _COMPLETION_CONDITION_FORMS.items()
            if _count_flex(body, literal) > 0
        ]
        if forms:
            matched_slugs.append(slug)
        else:
            unmatched_slugs.append(slug)
    if len(matched_slugs) != EXPECTED_STUB_COUNT:
        failures.append(
            f"Stub-8 (D-06, completion condition): {len(matched_slugs)} of "
            f"{len(non_launcher)} non-launcher stubs carry a recognised "
            f"completion condition, expected exactly {EXPECTED_STUB_COUNT}; "
            f"anchorless: {unmatched_slugs}"
        )

    # --- Stub-9 (PAR-01, parity tokens present) ---------------------------
    for slug, body in sorted(non_launcher.items()):
        missing = [p for p in _PARITY_LITERALS if _count_flex(body, p) == 0]
        if missing:
            failures.append(
                f"Stub-9 (PAR-01, parity tokens present): {slug} is missing "
                f"parity literal(s): {missing}"
            )

    # --- Stub-10 (D-03, bound) ---------------------------------------------
    for slug, body in sorted(non_launcher.items()):
        if _count_flex(body, _ONE_PASS_BOUND) == 0:
            failures.append(
                f"Stub-10 (D-03, bound): {slug} is missing the one-pass bound "
                f"clause {_ONE_PASS_BOUND!r}"
            )
        other_bounds = _OTHER_BOUND_RE.findall(body)
        if other_bounds:
            failures.append(
                f"Stub-10 (D-03, bound): {slug} states an additional numeric "
                f"revision bound not matching the one-pass clause: {other_bounds}"
            )

    return failures


def _validate_files() -> int:
    """Validate the live emitted stub tree. Returns a process exit code."""
    if not PLUGIN_SKILLS_DIR.exists():
        sys.stderr.write(
            f"check-focused-parity: plugin skills directory not found: "
            f"{PLUGIN_SKILLS_DIR}\n"
        )
        return 2

    try:
        stubs = _load_real_stubs()
    except (ValueError, FileNotFoundError) as exc:
        sys.stderr.write(f"check-focused-parity: could not read stub tree: {exc}\n")
        return 2

    if not stubs:
        sys.stderr.write(
            "check-focused-parity: zero skills yielded by iter_plugin_skills() — "
            "a gate that reads nothing cannot pass vacuously\n"
        )
        return 2

    failures = (
        _check_anchor_coherence()
        + _check_stub_surface(stubs)
        + _check_anchor_control_coverage(Path(__file__).read_text(encoding="utf-8"))
    )

    if failures:
        for msg in failures:
            sys.stderr.write(f"check-focused-parity: FAIL - {msg}\n")
        return 1

    print("check-focused-parity: PASS")
    return 0


# ---------------------------------------------------------------------------
# Self-test: in-memory mutation fixtures, never touching a file on disk.
# ---------------------------------------------------------------------------


def _check_negative(
    label: str,
    failures: list[str],
    expected_check_id: str,
    expected_detail: str | None = None,
) -> None:
    """Assert a mutated fixture failed, and failed for its OWN reason.

    Copied in shape from `scripts/check-act-limb.py`'s `_check_negative`
    (`01-REVIEW.md` WR-02's repair): the match key is the failing message's
    own leading check ID, plus (optionally) a sub-item detail unique to the
    assertion under test. Free-text substring matching against ANY failure in
    the list is forbidden — that lets a SIBLING check's failure satisfy a
    control's expectation, which is indistinguishable at the verdict line
    from a control whose target assertion is dead.

    The ID match is boundary-anchored (`Stub-1` must not match `Stub-10`),
    and a wrong-reason report names the check IDs that DID fire so a
    mis-targeted control is diagnosable in one read.
    """

    def _fired_ids(msgs: list[str]) -> list[str]:
        return sorted({m.split(" ", 1)[0].rstrip(":") for m in msgs})

    def _id_matches(msg: str, check_id: str) -> bool:
        if not msg.startswith(check_id):
            return False
        rest = msg[len(check_id):]
        return rest[:1] in (" ", ":")

    if not failures:
        print(f"({label}) WRONGLY PASSED (expected failure)")
        _problems.append(f"{label}: no failures produced")
        return
    matched = [f for f in failures if _id_matches(f, expected_check_id)]
    if not matched:
        print(
            f"({label}) failed for the WRONG reason (expected check ID "
            f"{expected_check_id!r}; check IDs that DID fire: "
            f"{', '.join(_fired_ids(failures))}; got: {'; '.join(failures)})"
        )
        _problems.append(f"{label}: wrong-reason failure")
        return
    if expected_detail is not None and not any(expected_detail in f for f in matched):
        print(
            f"({label}) failed for the WRONG reason (check ID "
            f"{expected_check_id!r} fired but no message of that ID contains "
            f"detail {expected_detail!r}; got: {'; '.join(matched)})"
        )
        _problems.append(f"{label}: wrong-detail failure")
        return
    print(f"({label}) correctly failed ({expected_check_id})")


def _check_positive(label: str, failures: list[str]) -> None:
    """Assert a fixture that should pass produced zero failures."""
    if failures:
        print(f"({label}) WRONGLY FAILED: {'; '.join(failures)}")
        _problems.append(f"{label}: unexpected failure(s)")
    else:
        print(f"({label}) correctly passed (0 failures)")


def _mutate_one(stubs: dict[str, str], slug: str, target: str, replacement: str = "") -> dict[str, str]:
    """Return a copy of *stubs* with a single-site whitespace-tolerant
    substitution applied to one slug's body. Never mutates the input dict or
    any string it holds — `str` is immutable and `dict(stubs)` is a shallow
    copy, so the caller's fixture is untouched."""
    new_stubs = dict(stubs)
    new_stubs[slug] = _replace_once(stubs[slug], target, replacement)
    return new_stubs


def _mutate_all_non_launcher(stubs: dict[str, str], target: str, replacement: str = "") -> dict[str, str]:
    """Like `_mutate_one`, applied to every non-launcher slug — builds the
    Stub-1 zero-match fixture (control b)."""
    new_stubs = dict(stubs)
    for slug in stubs:
        if slug != LAUNCHER_SLUG:
            new_stubs[slug] = _replace_once(stubs[slug], target, replacement)
    return new_stubs


def _append_to(stubs: dict[str, str], slug: str, text: str) -> dict[str, str]:
    """Return a copy of *stubs* with *text* appended to one slug's body —
    builds duplicate/injection fixtures."""
    new_stubs = dict(stubs)
    new_stubs[slug] = stubs[slug] + "\n\n" + text
    return new_stubs


def _move_section_after_handoff(stubs: dict[str, str], slug: str) -> dict[str, str]:
    """Build the Stub-2 placement-violation fixture (control d): cut the
    validation section (heading through the point just before the closing
    handoff anchor) and reinsert it AFTER the handoff anchor, inverting the
    two blocks' order so the heading now follows the handoff instead of
    preceding it."""
    body = stubs[slug]
    heading_match = _find_flex(body, _STUB_SECTION_HEADING)
    handoff_match = _find_flex(body, _CLOSING_HANDOFF_ANCHOR)
    if heading_match is None or handoff_match is None:
        raise AssertionError(
            f"placement fixture precondition failed for {slug}: both anchors "
            "must be found"
        )
    if not heading_match.start() < handoff_match.start():
        raise AssertionError(
            f"placement fixture precondition failed for {slug}: expected "
            "heading before handoff in the baseline fixture"
        )
    before = body[: heading_match.start()]
    middle = body[heading_match.start() : handoff_match.start()]
    tail_from_handoff = body[handoff_match.start() :]
    mutated = before + tail_from_handoff.rstrip("\n") + "\n\n" + middle.rstrip("\n") + "\n"
    new_stubs = dict(stubs)
    new_stubs[slug] = mutated
    return new_stubs


def _move_section_before_when(stubs: dict[str, str], slug: str) -> dict[str, str]:
    """Build the Stub-2 "before the inlined procedure" placement-violation
    fixture (control d4): cut the whole tail from the heading through end of
    file (heading, section, and the closing handoff paragraph together, in
    their original relative order) and move it to the very front of the
    body, ahead of `## When to reach for this`. Moving the whole tail as one
    block keeps the heading-before-handoff relation intact, so this fixture
    isolates the "before When to reach" branch without also tripping the
    "after handoff" branch `_move_section_after_handoff` already covers."""
    body = stubs[slug]
    heading_match = _find_flex(body, _STUB_SECTION_HEADING)
    if heading_match is None:
        raise AssertionError(
            f"before-when fixture precondition failed for {slug}: heading not found"
        )
    before = body[: heading_match.start()]
    tail = body[heading_match.start() :]
    mutated = tail.rstrip("\n") + "\n\n" + before.rstrip("\n") + "\n"
    new_stubs = dict(stubs)
    new_stubs[slug] = mutated
    return new_stubs


def _reflow(text: str, width: int) -> str:
    """Rewrap every plain paragraph in *text* to *width* columns, leaving
    headings, list items, table rows, code fences and blank lines untouched.

    A structural, not literal, transformation: it exists to prove this
    file's whitespace-insensitive matching survives an ordinary Markdown
    reflow at a width distinct from the shipped files' — the direct guard
    against the Phase 2 defect (pinned literals defeated by hard-wrapping)
    that this repo already paid for once. `break_long_words=False,
    break_on_hyphens=False` keep a hyphenated literal (e.g.
    `scope-proportionate`) or a bold-marker literal (e.g.
    `**Exit criterion:**`) from being split WITHIN a single flex-pattern
    "word" — a break `_flex_pattern` cannot tolerate, since it only inserts
    flexible whitespace between space-separated words, not inside one.
    """
    lines = text.split("\n")
    out: list[str] = []
    buf: list[str] = []

    def _flush() -> None:
        if buf:
            wrapped = textwrap.wrap(
                " ".join(buf), width=width, break_long_words=False, break_on_hyphens=False
            )
            out.extend(wrapped or [""])
            buf.clear()

    for line in lines:
        stripped = line.strip()
        is_structural = (
            not stripped
            or stripped.startswith("#")
            or stripped.startswith("-")
            or stripped.startswith("|")
            or stripped.startswith("```")
            or (stripped[:1].isdigit() and ". " in stripped[:4])
        )
        if is_structural:
            _flush()
            out.append(line)
        else:
            buf.append(stripped)
    _flush()
    return "\n".join(out)


_problems: list[str] = []


def _run_self_test() -> int:
    """Run the offline control battery (controls a-r). Returns 0 on all-pass,
    1 on any failure."""
    if not PLUGIN_SKILLS_DIR.exists():
        sys.stderr.write(
            "check-focused-parity --self-test: cannot derive fixtures — "
            f"{PLUGIN_SKILLS_DIR} not found\n"
        )
        return 2

    global _problems
    _problems = []

    try:
        real_stubs = _load_real_stubs()
    except (ValueError, FileNotFoundError) as exc:
        sys.stderr.write(f"check-focused-parity --self-test: could not read fixtures: {exc}\n")
        return 2

    if LAUNCHER_SLUG not in real_stubs or len(real_stubs) != EXPECTED_STUB_COUNT + 1:
        sys.stderr.write(
            "check-focused-parity --self-test: unexpected live stub set shape "
            f"({len(real_stubs)} entries, launcher present: "
            f"{LAUNCHER_SLUG in real_stubs}) — cannot build fixtures safely\n"
        )
        return 2

    # A representative slug per completion-condition form, used by controls
    # (l) and (m). Chosen from the confirmed live mapping in 03-PATTERNS.md.
    form_reps = {
        "exit-criterion": "validate",
        "stop-test-heading": "five-whys",
        "output-contract-heading": "inversion",
        "inline-stop-criterion": "estimate",
    }

    # Two module-level checks, printed before the fixture battery.
    coherence_failures = _check_anchor_coherence()
    if coherence_failures:
        print(f"(coh) anchor coherence: WRONGLY FAILED: {'; '.join(coherence_failures)}")
        _problems.append("(coh): anchor coherence check failed unexpectedly")
    else:
        print("(coh) anchor coherence: PASS (trivial — no derived pairs yet; plan 03-04 adds them)")

    coverage_failures = _check_anchor_control_coverage(Path(__file__).read_text(encoding="utf-8"))
    if coverage_failures:
        print("(cov) anchor-control coverage: FAIL — " + "; ".join(coverage_failures))
        _problems.append("(cov): anchor constant(s) without a control")
    else:
        print(
            "(cov) anchor-control coverage: PASS — every module-level anchor is "
            f"referenced >=3 times or listed ({len(_ANCHOR_CONTROL_EXEMPT)} exempt, "
            f"{len(_ANCHOR_CONTROL_PENDING)} pending)"
        )

    # (a) positive control: the real emitted files produce zero failures.
    _check_positive("a", _check_stub_surface(real_stubs))

    # (b) Stub-1 zero-match control: strip the heading from EVERY non-launcher
    # stub. Distinct from (c)'s wrong-count message.
    b_stubs = _mutate_all_non_launcher(real_stubs, _STUB_SECTION_HEADING)
    _check_negative("b", _check_stub_surface(b_stubs), "Stub-1", "ZERO")

    # (c) Stub-1 wrong-count control: strip the heading from exactly one stub.
    c_stubs = _mutate_one(real_stubs, "five-whys", _STUB_SECTION_HEADING)
    _check_negative("c", _check_stub_surface(c_stubs), "Stub-1", "12 of 13")

    # (c2) Stub-1 structural-count control: remove a whole non-launcher slug
    # from the stub set (rather than mutating a body's content), exercising
    # the "N non-launcher slugs are present" sub-assertion the (b)/(c)
    # content-only mutations never reach.
    c2_stubs = dict(real_stubs)
    del c2_stubs["five-whys"]
    _check_negative("c2", _check_stub_surface(c2_stubs), "Stub-1", "non-launcher slugs are present")

    # (d) Stub-2 placement control: move the section after the handoff.
    d_stubs = _move_section_after_handoff(real_stubs, "trade-off")
    _check_negative("d", _check_stub_surface(d_stubs), "Stub-2", "at or after")

    # (d2) Stub-2 missing-"When to reach"-anchor control: strip that heading
    # while leaving the validation section heading and the handoff anchor
    # intact, exercising the "is missing the ... anchor needed to check
    # ordering" branch for the When-to-reach anchor specifically.
    d2_stubs = _mutate_one(real_stubs, "trade-off", _WHEN_TO_REACH_HEADING)
    _check_negative("d2", _check_stub_surface(d2_stubs), "Stub-2", _WHEN_TO_REACH_HEADING)

    # (d3) Stub-2 missing-handoff-anchor control: strip the closing handoff
    # anchor while leaving the other two anchors intact, exercising the
    # sibling "missing the closing handoff anchor" branch.
    d3_stubs = _mutate_one(real_stubs, "trade-off", _CLOSING_HANDOFF_ANCHOR)
    _check_negative("d3", _check_stub_surface(d3_stubs), "Stub-2", "closing handoff anchor")

    # (d4) Stub-2 "before When to reach" placement control: move the whole
    # heading+section+handoff tail to the front of the body, ahead of
    # `## When to reach for this` — exercises the "occurs at or before"
    # branch, the mirror of (d)'s "at or after handoff" branch.
    d4_stubs = _move_section_before_when(real_stubs, "trade-off")
    _check_negative("d4", _check_stub_surface(d4_stubs), "Stub-2", "at or before")

    # (e) Stub-2 duplicate control: the heading appears twice in one stub.
    e_stubs = _append_to(real_stubs, "trade-off", _STUB_SECTION_HEADING)
    _check_negative("e", _check_stub_surface(e_stubs), "Stub-2", "2 time(s)")

    # (f) Stub-3 launcher control: inject the heading into the launcher.
    f_stubs = _append_to(real_stubs, LAUNCHER_SLUG, _STUB_SECTION_HEADING)
    _check_negative("f", _check_stub_surface(f_stubs), "Stub-3")

    # (g) Stub-4 verdict control: strip one verdict literal from one stub.
    g_stubs = _mutate_one(real_stubs, "second-order", _VERDICT_LITERALS[0])
    _check_negative("g", _check_stub_surface(g_stubs), "Stub-4", "verdict literal")

    # (h) Stub-5 mark control: strip the `?` clause from one stub.
    h_stubs = _mutate_one(real_stubs, "second-order", _UNVERIFIED_MARK_CLAUSE)
    _check_negative("h", _check_stub_surface(h_stubs), "Stub-5", "unverified mark clause")

    # (i) Stub-5 provenance-leak control: inject `read-at-source` into one stub.
    i_stubs = _append_to(real_stubs, "second-order", f"Provenance: {_PROVENANCE_LEAK_TERMS[0]}.")
    _check_negative("i", _check_stub_surface(i_stubs), "Stub-5", "leaks")

    # (j) Stub-6 wrapper control: strip the amended wrapper clause.
    j_stubs = _mutate_one(real_stubs, "ground-truths", _WRAPPER_ADMITS)
    _check_negative("j", _check_stub_surface(j_stubs), "Stub-6")

    # (k) Stub-7 retired-clause control: reinstate the retired wrapper clause.
    k_stubs = _append_to(real_stubs, "ground-truths", _WRAPPER_RETIRED)
    _check_negative("k", _check_stub_surface(k_stubs), "Stub-7")

    # (l) Stub-8 completion-condition control: strip validate's Exit-criterion
    # marker; the failure must NAME the slug.
    l_stubs = _mutate_one(
        real_stubs, form_reps["exit-criterion"], _COMPLETION_CONDITION_FORMS["exit-criterion"]
    )
    _check_negative("l", _check_stub_surface(l_stubs), "Stub-8", form_reps["exit-criterion"])

    # (m) Stub-8 all-forms control: for EACH of the four recognised forms, a
    # fixture in which that form is the ONLY thing carrying its
    # representative slug's completion condition, mutated away.
    for i, (form_name, rep_slug) in enumerate(form_reps.items(), start=1):
        literal = _COMPLETION_CONDITION_FORMS[form_name]
        m_stubs = _mutate_one(real_stubs, rep_slug, literal)
        _check_negative(f"m{i}", _check_stub_surface(m_stubs), "Stub-8", rep_slug)

    # (n) Stub-9 parity control: for EACH of the five parity literals, a
    # fixture with that one literal stripped from one stub.
    for i, literal in enumerate(_PARITY_LITERALS, start=1):
        n_stubs = _mutate_one(real_stubs, "challenge-assumptions", literal)
        _check_negative(f"n{i}", _check_stub_surface(n_stubs), "Stub-9", literal)

    # (o) Stub-10 bound control: strip the one-pass bound clause.
    o_stubs = _mutate_one(real_stubs, "reason-upward", _ONE_PASS_BOUND)
    _check_negative("o", _check_stub_surface(o_stubs), "Stub-10", "one-pass bound clause")

    # (o2) Stub-10 other-bound control: inject a competing numeric revision
    # bound (`_OTHER_BOUND_RE`'s territory) into one stub, alongside the
    # real one-pass clause, and confirm the "additional numeric revision
    # bound" branch fires distinctly from (o)'s "missing clause" branch.
    o2_stubs = _append_to(real_stubs, "reason-upward", "Revise twice if the first pass fails.")
    _check_negative("o2", _check_stub_surface(o2_stubs), "Stub-10", "additional numeric revision bound")

    # (p) reflow control (positive): every real stub body re-wrapped at a
    # width distinct from the shipped files' must still PASS — the direct,
    # measured guard against the Phase 2 whitespace defect.
    p_stubs = {slug: _reflow(body, _WRAP_WIDTH) for slug, body in real_stubs.items()}
    _check_positive("p", _check_stub_surface(p_stubs))

    # (q) ratchet branch control: drive `_check_anchor_control_coverage`
    # against synthetic sources to exercise every branch.
    markers = "# --- ratchet-bookkeeping-begin ---\n# --- ratchet-bookkeeping-end ---\n"

    q1_source = markers + '_FOO = "bar"\n'
    q1_failures = _check_anchor_control_coverage(q1_source, exempt={}, pending={})
    if any("referenced 1 time(s)" in f for f in q1_failures):
        print("(q1) under-referenced constant: correctly failed")
    else:
        print(f"(q1) under-referenced constant: WRONGLY PASSED OR WRONG REASON: {q1_failures}")
        _problems.append("q1: under-referenced constant control did not fire correctly")

    q2_failures = _check_anchor_control_coverage(
        q1_source, exempt={"_FOO": "justified in one sentence"}, pending={}
    )
    if not q2_failures:
        print("(q2) valid exempt entry: correctly passed")
    else:
        print(f"(q2) valid exempt entry: WRONGLY FAILED: {q2_failures}")
        _problems.append("q2: valid exempt entry incorrectly failed")

    q3_failures = _check_anchor_control_coverage(q1_source, exempt={"_FOO": "   "}, pending={})
    if any("empty justification" in f for f in q3_failures):
        print("(q3) exempt entry with empty justification: correctly failed")
    else:
        print(f"(q3) exempt entry with empty justification: WRONGLY PASSED OR WRONG REASON: {q3_failures}")
        _problems.append("q3: empty-justification exempt control did not fire correctly")

    q4_failures = _check_anchor_control_coverage(
        q1_source, exempt={}, pending={"_FOO": "Task 2 discharges this"}
    )
    if not q4_failures:
        print("(q4) short pending entry (count < 3): correctly passed")
    else:
        print(f"(q4) short pending entry: WRONGLY FAILED: {q4_failures}")
        _problems.append("q4: short pending entry incorrectly failed")

    q5_source = markers + '_FOO = "bar"\n_FOO\n_FOO\n'
    q5_failures = _check_anchor_control_coverage(
        q5_source, exempt={}, pending={"_FOO": "stale on purpose"}
    )
    if any("already referenced 3 time(s)" in f for f in q5_failures):
        print("(q5) stale pending entry (count >= 3): correctly failed")
    else:
        print(f"(q5) stale pending entry: WRONGLY PASSED OR WRONG REASON: {q5_failures}")
        _problems.append("q5: stale pending entry control did not fire correctly")

    q6_failures = _check_anchor_control_coverage(
        q1_source, exempt={"_FOO": "x"}, pending={"_FOO": "y"}
    )
    if any("BOTH" in f for f in q6_failures):
        print("(q6) constant listed in both EXEMPT and PENDING: correctly failed")
    else:
        print(f"(q6) both-lists control: WRONGLY PASSED OR WRONG REASON: {q6_failures}")
        _problems.append("q6: both-exempt-and-pending control did not fire correctly")

    q7_failures = _check_anchor_control_coverage(markers)
    if any("enumerator matched no" in f for f in q7_failures):
        print("(q7) no anchors present: correctly failed")
    else:
        print(f"(q7) no-anchors control: WRONGLY PASSED OR WRONG REASON: {q7_failures}")
        _problems.append("q7: no-anchors control did not fire correctly")

    q8_failures = _check_anchor_control_coverage('_FOO = "bar"\n_FOO\n_FOO\n')
    if any("bookkeeping markers not found" in f for f in q8_failures):
        print("(q8) missing bookkeeping markers: correctly failed")
    else:
        print(f"(q8) missing-markers control: WRONGLY PASSED OR WRONG REASON: {q8_failures}")
        _problems.append("q8: missing-markers control did not fire correctly")

    _this_module = sys.modules[__name__]
    original_exempt = _this_module._ANCHOR_CONTROL_EXEMPT
    try:
        _this_module._ANCHOR_CONTROL_EXEMPT = "not a dict"  # type: ignore[assignment]
        q9_failures = _check_anchor_control_coverage(q1_source)
    finally:
        _this_module._ANCHOR_CONTROL_EXEMPT = original_exempt
    if any("must both be dicts" in f for f in q9_failures):
        print("(q9) retyped machinery global (_ANCHOR_CONTROL_EXEMPT): correctly failed")
    else:
        print(f"(q9) retyped-global control: WRONGLY PASSED OR WRONG REASON: {q9_failures}")
        _problems.append("q9: retyped machinery global control did not fire correctly")

    original_reentrant = _this_module._DISPATCH_REENTRANT
    try:
        _this_module._DISPATCH_REENTRANT = "not a bool"  # type: ignore[assignment]
        q10_failures = _check_anchor_control_coverage(q1_source)
    finally:
        _this_module._DISPATCH_REENTRANT = original_reentrant
    if any("_DISPATCH_REENTRANT must be a bool" in f for f in q10_failures):
        print("(q10) retyped machinery global (_DISPATCH_REENTRANT): correctly failed")
    else:
        print(f"(q10) retyped-reentrant control: WRONGLY PASSED OR WRONG REASON: {q10_failures}")
        _problems.append("q10: retyped _DISPATCH_REENTRANT control did not fire correctly")

    # (r) dispatch control: prove the CLI layer reaches this block, not
    # merely that _run_self_test() is correct when called directly.
    if not _this_module._DISPATCH_REENTRANT:
        _this_module._DISPATCH_REENTRANT = True
        try:
            import contextlib
            import io

            dispatch_out, dispatch_err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(dispatch_out), contextlib.redirect_stderr(dispatch_err):
                dispatch_rc = main(["--self-test"])
            dispatch_text = dispatch_out.getvalue()
            if dispatch_rc != 0:
                print(
                    "(r) dispatch control: WRONGLY FAILED — main(['--self-test']) "
                    f"returned {dispatch_rc}, expected 0"
                )
                _problems.append(f"r: main(['--self-test']) returned {dispatch_rc}, expected 0")
            elif "(a) correctly passed" not in dispatch_text:
                print(
                    "(r) dispatch control: WRONGLY FAILED — captured stdout did not "
                    f"contain control (a)'s pass text: {dispatch_text!r}"
                )
                _problems.append("r: captured stdout missing control (a) pass text")
            else:
                print(
                    "(r) dispatch control: PASS — main(['--self-test']) reaches this "
                    "block end-to-end"
                )
        except Exception as exc:  # noqa: BLE001 - self-test must report, not crash
            print(f"(r) dispatch control: WRONGLY FAILED — unexpected exception: {exc!r}")
            _problems.append(f"r: unexpected exception: {exc!r}")
        finally:
            _this_module._DISPATCH_REENTRANT = False
    else:
        print("(r) dispatch control: skipped (nested self-test run)")

    if _problems:
        sys.stderr.write(
            "check-focused-parity --self-test: FAIL — " + "; ".join(_problems) + "\n"
        )
        return 1

    print("check-focused-parity --self-test: PASS")
    return 0


def main(argv: list[str] | None = None) -> int:
    """Run the check-focused-parity CLI and return a process exit code.

    `argv` accepts an explicit list (defaulting to None, which makes
    argparse fall back to `sys.argv[1:]`) so control (r) can drive
    `main(["--self-test"])` in-process and inspect the return code, proving
    the CLI dispatch itself reaches the self-test block rather than only
    `_run_self_test()` being correct when called directly.
    """
    if sys.version_info < (3, 12):
        sys.stderr.write(
            "scripts/check-focused-parity.py requires Python >=3.12 "
            f"(running {sys.version_info.major}.{sys.version_info.minor}).\n"
        )
        return 2

    parser = argparse.ArgumentParser(
        prog="check-focused-parity.py",
        description=(
            "HARN-03 (stub-surface half): assert the '## Focused-mode validation' "
            "section is present, correctly placed, correctly counted, and carries "
            "every load-bearing literal in all 13 emitted focused stubs, and stays "
            "absent from the launcher."
        ),
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run the offline self-test control battery (controls a-r)",
    )
    args = parser.parse_args(argv)

    if args.self_test:
        return _run_self_test()

    return _validate_files()


if __name__ == "__main__":
    sys.exit(main())
