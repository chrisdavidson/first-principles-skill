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

from _skill_io import PLUGIN_SKILLS_DIR, REPO_ROOT, iter_plugin_skills  # noqa: E402

# ---------------------------------------------------------------------------
# Path / structural constants. No leading underscore: not ratchet-tracked
# (the ratchet only scans `_[A-Z]...` names), matching this repo's existing
# gates' convention of leaving plain path/count constants untracked.
# ---------------------------------------------------------------------------

LAUNCHER_SLUG = "first-principles-analysis"
EXPECTED_STUB_COUNT = 13

# D-11: the agent-surface generated-tree targets this gate reads. Never
# `shared/` — DUAL-04 already guarantees `shared/` and the emitted tree
# agree, and D-11's scope for this gate is "what actually ships."
AGENT_FILE = REPO_ROOT / "first-principles" / "agents" / "first-principles.md"
AGENT_REFERENCES_DIR = REPO_ROOT / "first-principles" / "agents" / "references"

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

# PAR-01/D-10: the five parity tokens are defined ONCE, further below (the
# `_PT_*` constants plan 03-04 Task 1 introduced), collected there into a
# single `_PARITY_TOKENS` tuple both the stub-surface (this constant's
# original home, Stub-9) and the agent-surface (Agent-5/Agent-6) assertions
# reference — never retyped as a second independent five-string literal.

# D-03: the one-pass revision bound.
_ONE_PASS_BOUND = "Revise at most one time."

# D-03 (negative half): no OTHER numeric revision bound may be stated
# anywhere in a stub — "revise twice", "revise two times", "revise N times"
# for any N other than the one-pass clause above.
_OTHER_BOUND_RE = re.compile(r"[Rr]evise\s+(?:twice|two\s+times|three\s+times|\d+\s+times)")

# ---------------------------------------------------------------------------
# Agent-surface content anchors (plan 03-04, D-04/D-09/D-10). Same discipline
# as the stub-surface anchors above: one module-level `_UPPER_SNAKE` constant
# per pinned literal, taken verbatim from the live-verified emitted tree
# (never retyped from memory), with a comment naming the decision it serves.
# ---------------------------------------------------------------------------

# D-04/D-06: the bold Exit-criterion line shape, reused on the agent
# reference-sibling surface (Agent-7) and the fishbone stub clamp-safety
# check (Agent-8) — the same literal `_COMPLETION_CONDITION_FORMS` already
# pins for the stub surface under the key "exit-criterion".
_EXIT_CRITERION_LINE = "**Exit criterion:**"

# PAR-03: the amended focused-mode branching parenthetical, naming Validate.
# Taken verbatim from `03-01-SUMMARY.md` and confirmed live against
# `first-principles/agents/first-principles.md`.
_AGENT_VALIDATE_NAMED = "Derivation Chains, Validate, and Second-Order Effects when applicable"

# PAR-03 (negative half): the pre-edit parenthetical this amendment replaced.
# Anchored starting at "Derivation Chains," rather than only the shorter
# trailing fragment "...applicable) run as written" — that shorter fragment
# is a substring of BOTH the retired form and the amended form (the sentence
# always ends "...applicable) run as written." regardless of whether
# "Validate," was inserted earlier in the list), so it cannot distinguish
# them. Confirmed live: the longer anchor below is 0 occurrences on the
# correct (amended) tree; the shorter fragment alone is 1 (a false positive).
_AGENT_VALIDATE_RETIRED = "Derivation Chains, Second-Order Effects when applicable) run as written"

# Placement anchors for Agent-3: the validate-named literal must fall between
# the branching label and the full-composer bullet.
_AGENT_EXECUTION_BRANCHING_LABEL = "**Execution branching.**"
_AGENT_FULL_COMPOSER_ANCHOR = "MODE = full-composer"

# D-11's interfaces block, live-verified: `agents/references/` emits only the
# 8 TOOLS slugs, never the five phase slugs — so Agent-7 iterates this
# explicit three-slug tuple (the three D-04 gave a stated Exit criterion),
# not a 13-way loop, which would raise FileNotFoundError against a directory
# that never emits identify-essence.md, challenge-assumptions.md, etc.
_AGENT_REFERENCE_SLUGS: tuple[str, ...] = ("fishbone", "pre-mortem", "second-order")

# PAR-01 parity tokens, one module-level constant per literal (D-10's static
# derivation, plan 03-04 Task 2 unifies these into a single `_PARITY_TOKENS`
# tuple shared by both surfaces). Taken verbatim from `03-01-SUMMARY.md`,
# confirmed live in `first-principles/agents/first-principles.md`.
_PT_SIX_CRITERION_GATE = "six-criterion Self-Audit Gate"
_PT_SIX_SECTION_DOC = "six-section analysis document"
_PT_SCOPE_PROPORTIONATE = "scope-proportionate"
_PT_NO_ACQUIRE_EVIDENCE = "does not acquire evidence"
_PT_STAYS_MARKED = "stays marked"

# D-10 static derivation: ONE tuple collecting all five _PT_* constants,
# referenced by the stub-surface assertion (Stub-9, ex-`_PARITY_LITERALS`)
# and by `_check_cross_surface_parity()`'s runtime derivation. Never
# retyped as a second independent five-string literal anywhere in this file.
_PARITY_TOKENS: tuple[str, ...] = (
    _PT_SIX_CRITERION_GATE,
    _PT_SIX_SECTION_DOC,
    _PT_SCOPE_PROPORTIONATE,
    _PT_NO_ACQUIRE_EVIDENCE,
    _PT_STAYS_MARKED,
)

# D-09/D-10 static derivation: the agent-surface assertions' two component
# groupings, each DERIVED from the shared _PT_* constants above (never
# retyped) — the depth-difference component (Agent-5) and the larger,
# absent-Act-limb component (Agent-6). `_check_anchor_coherence()` verifies
# these still equal a fresh recomputation from the same _PT_* names.
_AGENT_DEPTH_TOKENS: tuple[str, ...] = (
    _PT_SIX_CRITERION_GATE,
    _PT_SIX_SECTION_DOC,
    _PT_SCOPE_PROPORTIONATE,
)
_AGENT_ACT_LIMB_TOKENS: tuple[str, ...] = (_PT_NO_ACQUIRE_EVIDENCE, _PT_STAYS_MARKED)


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
    """Assert the derived anchor pairs still stand in the relation their
    derivation creates (D-10's static half, `scripts/check-act-limb.py`
    WR-14's shape).

    Derivation alone makes the relation true by construction — every pair
    below is built from the same `_PT_*` constants on both sides. This
    function is what fails loudly if a future editor UN-derives one half:
    re-points `_AGENT_DEPTH_TOKENS`, `_AGENT_ACT_LIMB_TOKENS`, or
    `_PARITY_TOKENS` to an independently retyped literal tuple that happens
    to differ from a fresh recomputation off the shared `_PT_*` names. The
    pair table is built INSIDE the function body, not at import, so it reads
    the current module globals rather than a snapshot — the same shape
    `check-act-limb.py`'s `_check_anchor_coherence()` uses.
    """
    failures: list[str] = []
    pairs: tuple[tuple[str, tuple[str, ...], tuple[str, ...]], ...] = (
        (
            "agent depth-component tokens (Agent-5)",
            _AGENT_DEPTH_TOKENS,
            (_PT_SIX_CRITERION_GATE, _PT_SIX_SECTION_DOC, _PT_SCOPE_PROPORTIONATE),
        ),
        (
            "agent act-limb-component tokens (Agent-6)",
            _AGENT_ACT_LIMB_TOKENS,
            (_PT_NO_ACQUIRE_EVIDENCE, _PT_STAYS_MARKED),
        ),
        (
            "stub/cross-surface parity-token set (Stub-9, Parity-2..5)",
            _PARITY_TOKENS,
            (
                _PT_SIX_CRITERION_GATE,
                _PT_SIX_SECTION_DOC,
                _PT_SCOPE_PROPORTIONATE,
                _PT_NO_ACQUIRE_EVIDENCE,
                _PT_STAYS_MARKED,
            ),
        ),
    )
    for name, actual, expected in pairs:
        if actual != expected:
            failures.append(
                f"Coherence (D-10, derived anchor pair): {name} — {actual!r} "
                f"!= {expected!r}; the two halves must be derived from one "
                "token, not restated as independent literals"
            )
    return failures


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
        missing = [p for p in _PARITY_TOKENS if _count_flex(body, p) == 0]
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


# ---------------------------------------------------------------------------
# Agent-surface real-content checks (plan 03-04).
# ---------------------------------------------------------------------------


def _procedure_bounds(text: str) -> tuple[int, int] | None:
    """Return the (start, end) character offsets of *text*'s `## Procedure`
    section — from the heading line's start to the next H2 heading, or EOF
    if none follows. Returns `None` if no `## Procedure` heading is found.

    The two regexes are local, not module-level `_UPPER_SNAKE` constants —
    deliberately, so they are not swept into the anchor-control coverage
    ratchet (D-12): they are structural parsing machinery, not a pinned
    content literal a stub or the agent body must carry, and the ratchet
    exists to guard the latter.
    """
    heading_re = re.compile(r"^##\s+Procedure\s*$", re.MULTILINE)
    next_h2_re = re.compile(r"^##\s+\S.*$", re.MULTILINE)
    heading_match = heading_re.search(text)
    if heading_match is None:
        return None
    rest = text[heading_match.end() :]
    next_h2_match = next_h2_re.search(rest)
    end = heading_match.end() + next_h2_match.start() if next_h2_match else len(text)
    return heading_match.start(), end


def _agent_parity_note(text: str) -> str | None:
    """Extract the focused-mode proportionality paragraph from the emitted
    agent body: the text between the `MODE = full-composer` bullet
    (`_AGENT_FULL_COMPOSER_ANCHOR`) and the next standalone `---` divider.

    The full-composer anchor is searched for only AFTER
    `_AGENT_EXECUTION_BRANCHING_LABEL` — the "Default rule" paragraph
    earlier in Step 0 also sets `MODE = full-composer` in prose (the same
    landmine Agent-3 already had to account for), so anchoring on the FIRST
    occurrence in the whole file would capture a much larger, wrong slice
    starting from that earlier sentence. Measured live: the naive
    first-occurrence anchor produced a 1796-character slice that swallowed
    the branching-block bullets themselves, not the ~500-character
    proportionality paragraph alone — masked in earlier ad hoc checks only
    because the noisy prefix happened not to break substring containment.

    Returns `None` when any anchor cannot be found in *text* — distinct from
    an empty string, which means all anchors were found but nothing (or
    only whitespace) lies between the full-composer bullet and the divider.
    Agent-4 reports these as two separate failure conditions; Parity-1
    (plan 03-04 Task 2) reuses this same distinction as its own anti-vacuity
    guard.
    """
    eb_match = _find_flex(text, _AGENT_EXECUTION_BRANCHING_LABEL)
    if eb_match is None:
        return None
    after_eb = text[eb_match.end() :]
    fc_match = _find_flex(after_eb, _AGENT_FULL_COMPOSER_ANCHOR)
    if fc_match is None:
        return None
    after = after_eb[fc_match.end() :]
    divider_match = re.search(r"^---\s*$", after, re.MULTILINE)
    if divider_match is None:
        return None
    return after[: divider_match.start()].strip()


def _stub_parity_note(body: str) -> str | None:
    """Extract a stub's `## Focused-mode validation` section: from the
    heading (`_STUB_SECTION_HEADING`) to the next standalone `---` divider,
    or EOF if none follows. Mirrors `_agent_parity_note()`'s divider-stop
    shape so both surfaces are sliced the same way before token derivation.
    Returns `None` if the heading itself is not found. Plan 03-04 Task 2's
    `_check_cross_surface_parity()` is this helper's only caller.
    """
    heading_match = _find_flex(body, _STUB_SECTION_HEADING)
    if heading_match is None:
        return None
    after = body[heading_match.start() :]
    divider_match = re.search(r"^---\s*$", after, re.MULTILINE)
    if divider_match is None:
        return after
    return after[: divider_match.start()]


def _check_agent_surface(
    agent_text: str,
    reference_texts: dict[str, str],
    fishbone_stub_text: str,
) -> list[str]:
    """Validate the eight agent-surface assertions.

    *agent_text* is the emitted agent body
    (`first-principles/agents/first-principles.md`). *reference_texts* maps
    each of `_AGENT_REFERENCE_SLUGS` (fishbone, pre-mortem, second-order —
    NOT all 13; `agents/references/` only emits the 8 TOOLS slugs, per this
    plan's live-verified interfaces block) to that file's full text.
    *fishbone_stub_text* is the emitted `skills/fishbone/SKILL.md` body,
    checked for the D-05 clamp-safety case (Agent-8).

    Operating on plain strings/dicts rather than reading disk directly is
    what makes this function callable identically against the real emitted
    tree and against an in-memory self-test fixture, matching
    `_check_stub_surface()`'s shape.

    Returns failure strings, each beginning with a stable
    `Agent-N (<REQ-ID>, <label>): <detail>` check ID.
    """
    failures: list[str] = []

    # --- Agent-1 (PAR-03, validate named) --------------------------------
    if not _contains(agent_text, _AGENT_VALIDATE_NAMED):
        failures.append(
            "Agent-1 (PAR-03, validate named): the amended branching "
            f"parenthetical {_AGENT_VALIDATE_NAMED!r} was not found"
        )

    # --- Agent-2 (PAR-03, retired form absent) -----------------------------
    retired_count = _count_flex(agent_text, _AGENT_VALIDATE_RETIRED)
    if retired_count != 0:
        failures.append(
            "Agent-2 (PAR-03, retired form absent): the retired parenthetical "
            f"{_AGENT_VALIDATE_RETIRED!r} appears {retired_count} time(s), "
            "expected 0"
        )

    # --- Agent-3 (PAR-03, placement) ---------------------------------------
    # Both the validate-named literal and the full-composer bullet are
    # searched for only in the text AFTER the branching label — the
    # "Default rule" paragraph earlier in Step 0 also sets `MODE =
    # full-composer` in prose, so the FIRST occurrence of that anchor in the
    # whole file is not the branching bullet this check cares about.
    eb_match = _find_flex(agent_text, _AGENT_EXECUTION_BRANCHING_LABEL)
    if eb_match is None:
        failures.append(
            "Agent-3 (PAR-03, placement): the "
            f"{_AGENT_EXECUTION_BRANCHING_LABEL!r} label was not found; "
            "cannot check ordering"
        )
    else:
        remainder = agent_text[eb_match.end() :]
        validate_match = _find_flex(remainder, _AGENT_VALIDATE_NAMED)
        fc_match = _find_flex(remainder, _AGENT_FULL_COMPOSER_ANCHOR)
        if validate_match is None or fc_match is None:
            failures.append(
                "Agent-3 (PAR-03, placement): one or both of the "
                "validate-named literal and the full-composer bullet were "
                f"not found after {_AGENT_EXECUTION_BRANCHING_LABEL!r}; "
                "cannot check ordering"
            )
        elif not (validate_match.start() < fc_match.start()):
            failures.append(
                "Agent-3 (PAR-03, placement): the validate-named literal "
                f"does not fall between {_AGENT_EXECUTION_BRANCHING_LABEL!r} "
                f"and {_AGENT_FULL_COMPOSER_ANCHOR!r}"
            )

    # --- Agent-4 (PAR-01, note present) -------------------------------------
    note = _agent_parity_note(agent_text)
    if note is None:
        failures.append(
            "Agent-4 (PAR-01, note present): the proportionality note's "
            f"anchor pair ({_AGENT_FULL_COMPOSER_ANCHOR!r} then a trailing "
            "'---' divider) was not found"
        )
    elif not note:
        failures.append(
            "Agent-4 (PAR-01, note present): the proportionality note's "
            "anchors were found but the slice between them is empty"
        )

    # --- Agent-5 (PAR-01, depth component) ----------------------------------
    depth_tokens = _AGENT_DEPTH_TOKENS
    if note:
        missing_depth = [t for t in depth_tokens if not _contains(note, t)]
        if missing_depth:
            failures.append(
                "Agent-5 (PAR-01, depth component): the proportionality "
                f"note is missing depth-component literal(s): {missing_depth}"
            )
    else:
        failures.append(
            "Agent-5 (PAR-01, depth component): cannot check depth-component "
            "literals — the proportionality note could not be extracted"
        )

    # --- Agent-6 (PAR-01, act-limb component) -------------------------------
    act_limb_tokens = _AGENT_ACT_LIMB_TOKENS
    if note:
        missing_act = [t for t in act_limb_tokens if not _contains(note, t)]
        if missing_act:
            failures.append(
                "Agent-6 (PAR-01, act-limb component): the proportionality "
                f"note is missing act-limb-component literal(s): {missing_act}"
            )
    else:
        failures.append(
            "Agent-6 (PAR-01, act-limb component): cannot check act-limb-"
            "component literals — the proportionality note could not be "
            "extracted"
        )

    # --- Agent-7 (D-04/D-06, agent reference conditions) --------------------
    for slug in _AGENT_REFERENCE_SLUGS:
        text = reference_texts.get(slug)
        if text is None:
            failures.append(
                "Agent-7 (D-04/D-06, agent reference conditions): "
                f"agents/references/{slug}.md text was not supplied to the "
                "checker"
            )
            continue
        count = _count_flex(text, _EXIT_CRITERION_LINE)
        if count != 1:
            failures.append(
                "Agent-7 (D-04/D-06, agent reference conditions): "
                f"agents/references/{slug}.md carries {_EXIT_CRITERION_LINE!r} "
                f"{count} time(s), expected exactly 1"
            )
            continue
        bounds = _procedure_bounds(text)
        if bounds is None:
            failures.append(
                "Agent-7 (D-04/D-06, agent reference conditions): "
                f"agents/references/{slug}.md has no '## Procedure' heading"
            )
            continue
        match = _find_flex(text, _EXIT_CRITERION_LINE)
        assert match is not None  # count == 1 guarantees a match
        if not (bounds[0] <= match.start() < bounds[1]):
            failures.append(
                "Agent-7 (D-04/D-06, agent reference conditions): "
                f"agents/references/{slug}.md's {_EXIT_CRITERION_LINE!r} "
                "line falls outside its '## Procedure' section"
            )

    # --- Agent-8 (D-05, clamp safety) ---------------------------------------
    if _count_flex(fishbone_stub_text, _EXIT_CRITERION_LINE) == 0:
        failures.append(
            "Agent-8 (D-05, clamp safety): first-principles/skills/fishbone/"
            f"SKILL.md is missing {_EXIT_CRITERION_LINE!r} — the "
            "SLUGS_WITH_DETAIL '## Example' clamp may have truncated it"
        )

    return failures


def _check_cross_surface_parity(agent_text: str, stubs: dict[str, str]) -> list[str]:
    """D-10's runtime cross-surface derivation — the assertion the whole
    plan exists for: derive the set of parity tokens actually present in the
    agent-side proportionality note, and require EVERY one of the 13
    non-launcher stub validation notes to carry EXACTLY that set (set
    equality, not subset — a stub carrying an EXTRA token the agent note
    dropped is also drift, per the plan's action text).

    Three anti-vacuity guards run, in order, before the 13-way comparison —
    each its own separately-failable check ID, because an empty or
    unreadable agent note would otherwise make `set() <= anything` trivially
    true and every stub "pass" for the wrong reason:

    - Parity-1: the agent note is absent or blank.
    - Parity-2: the note is present but yields ZERO parity tokens.
    - Parity-3: the note yields SOME but not all five tokens.

    Only once all three guards clear does Parity-4 run the 13-way
    comparison, and Parity-5 re-asserts the 13-count at THIS layer — the
    guard against a silently-shrunk iteration making Parity-4 vacuously true
    even if Stub-1 already caught the same shrink at the stub-surface layer.

    Returns failure strings, each beginning with a stable
    `Parity-N (D-10, <label>): <detail>` check ID.
    """
    failures: list[str] = []
    note = _agent_parity_note(agent_text)

    # --- Parity-1 (D-10, note missing) -------------------------------------
    if note is None or not note.strip():
        failures.append(
            "Parity-1 (D-10, note missing): the agent-side proportionality "
            "note is absent or blank — cross-surface parity cannot be derived"
        )
        return failures

    derived = tuple(t for t in _PARITY_TOKENS if _contains(note, t))

    # --- Parity-2 (D-10, empty derivation) ----------------------------------
    if not derived:
        failures.append(
            "Parity-2 (D-10, empty derivation): the agent note yields ZERO "
            "parity tokens — a derived set of zero would trivially satisfy "
            "every stub and is therefore treated as a gate failure, not a pass"
        )
        return failures

    # --- Parity-3 (D-10, incomplete derivation) -----------------------------
    if len(derived) != len(_PARITY_TOKENS):
        missing = [t for t in _PARITY_TOKENS if t not in derived]
        failures.append(
            f"Parity-3 (D-10, incomplete derivation): the agent note yields "
            f"{len(derived)} of {len(_PARITY_TOKENS)} parity tokens; missing: "
            f"{missing}"
        )
        return failures

    agent_set = set(derived)

    # --- Parity-4 (D-10, cross-surface equality) ----------------------------
    non_launcher = {slug: body for slug, body in stubs.items() if slug != LAUNCHER_SLUG}
    for slug, body in sorted(non_launcher.items()):
        stub_note = _stub_parity_note(body)
        if stub_note is None or not stub_note.strip():
            failures.append(
                f"Parity-4 (D-10, cross-surface equality): {slug} has no "
                f"{_STUB_SECTION_HEADING!r} section to derive tokens from"
            )
            continue
        stub_set = {t for t in _PARITY_TOKENS if _contains(stub_note, t)}
        if stub_set != agent_set:
            missing_in_stub = sorted(agent_set - stub_set)
            extra_in_stub = sorted(stub_set - agent_set)
            failures.append(
                f"Parity-4 (D-10, cross-surface equality): {slug} drifts "
                f"from the agent note — missing {missing_in_stub}, extra "
                f"{extra_in_stub}"
            )

    # --- Parity-5 (D-10, stub count) ----------------------------------------
    if len(non_launcher) != EXPECTED_STUB_COUNT:
        failures.append(
            f"Parity-5 (D-10, stub count): {len(non_launcher)} non-launcher "
            f"stub notes were iterated, expected exactly {EXPECTED_STUB_COUNT}"
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

    if not AGENT_FILE.exists():
        sys.stderr.write(f"check-focused-parity: agent file not found: {AGENT_FILE}\n")
        return 2
    agent_text = AGENT_FILE.read_text(encoding="utf-8")

    reference_texts: dict[str, str] = {}
    for slug in _AGENT_REFERENCE_SLUGS:
        ref_path = AGENT_REFERENCES_DIR / f"{slug}.md"
        if not ref_path.exists():
            sys.stderr.write(f"check-focused-parity: agent reference file not found: {ref_path}\n")
            return 2
        reference_texts[slug] = ref_path.read_text(encoding="utf-8")

    if "fishbone" not in stubs:
        sys.stderr.write(
            "check-focused-parity: fishbone stub not found in the loaded stub set — "
            "cannot check the D-05 clamp-safety case (Agent-8)\n"
        )
        return 2

    failures = (
        _check_anchor_coherence()
        + _check_stub_surface(stubs)
        + _check_agent_surface(agent_text, reference_texts, stubs["fishbone"])
        + _check_cross_surface_parity(agent_text, stubs)
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


def _move_validate_outside_branching(text: str) -> str:
    """Build the Agent-3 placement-violation fixture: cut the validate-named
    literal out of its natural place (inside the branching bullet) and
    prepend a standalone copy of it, parenthesised, at the very top of the
    file — guaranteed to sit BEFORE `_AGENT_EXECUTION_BRANCHING_LABEL`, so
    the literal is present exactly once but no longer falls between the
    label and the full-composer bullet."""
    eb_match = _find_flex(text, _AGENT_EXECUTION_BRANCHING_LABEL)
    if eb_match is None:
        raise AssertionError(
            "placement fixture precondition failed: execution-branching label not found"
        )
    prefix = text[: eb_match.start()]
    suffix = text[eb_match.start() :]
    replacement = "Derivation Chains, and Second-Order Effects when applicable"
    suffix_without = _replace_once(suffix, _AGENT_VALIDATE_NAMED, replacement)
    return prefix + f"({_AGENT_VALIDATE_NAMED})\n\n" + suffix_without


def _strip_agent_note(text: str) -> str:
    """Build the Agent-4/Parity-1 fixture: remove the WHOLE proportionality
    note slice `_agent_parity_note()` extracts, leaving the surrounding
    anchors (the full-composer bullet, the trailing `---` divider) intact
    but nothing between them — the "anchors found, slice empty" branch,
    distinct from "anchors not found" entirely."""
    note = _agent_parity_note(text)
    if not note:
        raise AssertionError("agent parity note precondition failed: note is empty or None")
    return _replace_once(text, note, "")


def _mutate_ref(
    reference_texts: dict[str, str], slug: str, target: str, replacement: str = ""
) -> dict[str, str]:
    """Return a copy of *reference_texts* with a single-site substitution
    applied to one slug's text — the agent-reference-surface counterpart of
    `_mutate_one`."""
    new_texts = dict(reference_texts)
    new_texts[slug] = _replace_once(reference_texts[slug], target, replacement)
    return new_texts


def _duplicate_in_ref(reference_texts: dict[str, str], slug: str, text: str) -> dict[str, str]:
    """Return a copy of *reference_texts* with *text* appended a second time
    to one slug's body — the agent-reference-surface counterpart of
    `_append_to`, builds Agent-7's duplicate-count fixture."""
    new_texts = dict(reference_texts)
    new_texts[slug] = reference_texts[slug] + "\n\n" + text
    return new_texts


def _move_exit_criterion_to_top(reference_texts: dict[str, str], slug: str) -> dict[str, str]:
    """Build the Agent-7 "outside Procedure" placement-violation fixture:
    cut the Exit-criterion LINE (the whole line it sits on, not just the
    bold marker) out of its natural place inside `## Procedure` and prepend
    it at the very top of the file — guaranteed to sit before the `##
    Procedure` heading regardless of whether that file's Procedure section
    is followed by another H2 or runs to EOF (fishbone.md has no trailing
    H2; pre-mortem.md and second-order.md do), so this one fixture shape
    covers all three files without a per-file EOF/H2 branch."""
    text = reference_texts[slug]
    match = _find_flex(text, _EXIT_CRITERION_LINE)
    if match is None:
        raise AssertionError(
            f"placement fixture precondition failed for {slug}: Exit criterion line not found"
        )
    line_start = text.rfind("\n", 0, match.start()) + 1
    line_end = text.find("\n", match.end())
    line_end = line_end + 1 if line_end != -1 else len(text)
    line_text = text[line_start:line_end]
    without = text[:line_start] + text[line_end:]
    new_texts = dict(reference_texts)
    new_texts[slug] = line_text + without
    return new_texts


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

    if not AGENT_FILE.exists():
        sys.stderr.write(f"check-focused-parity --self-test: agent file not found: {AGENT_FILE}\n")
        return 2
    real_agent_text = AGENT_FILE.read_text(encoding="utf-8")

    real_reference_texts: dict[str, str] = {}
    for slug in _AGENT_REFERENCE_SLUGS:
        ref_path = AGENT_REFERENCES_DIR / f"{slug}.md"
        if not ref_path.exists():
            sys.stderr.write(
                f"check-focused-parity --self-test: agent reference file not found: {ref_path}\n"
            )
            return 2
        real_reference_texts[slug] = ref_path.read_text(encoding="utf-8")

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
        print(
            "(coh) anchor coherence: PASS — 3 derived anchor pairs "
            "(agent depth tokens, agent act-limb tokens, stub/cross-surface "
            "parity-token set), each recomputed from the shared _PT_* "
            "constants and compared to the module-level tuple it derives"
        )

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

    # (a2) agent-surface positive control: the real emitted agent body and
    # its three reference siblings produce zero Agent-N failures.
    _check_positive(
        "a2",
        _check_agent_surface(real_agent_text, real_reference_texts, real_stubs["fishbone"]),
    )

    # (a3) cross-surface positive control: the real agent note and all 13
    # real stub notes derive the same parity-token set — zero Parity-N
    # failures.
    _check_positive("a3", _check_cross_surface_parity(real_agent_text, real_stubs))

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
    for i, literal in enumerate(_PARITY_TOKENS, start=1):
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

    # --- Agent-surface and cross-surface controls (plan 03-04 Task 2) ------

    # (s) Agent-1 control: strip the validate-named literal.
    s_agent = _replace_once(
        real_agent_text,
        _AGENT_VALIDATE_NAMED,
        "Derivation Chains, and Second-Order Effects when applicable",
    )
    _check_negative(
        "s",
        _check_agent_surface(s_agent, real_reference_texts, real_stubs["fishbone"]),
        "Agent-1",
    )

    # (t) Agent-2 control: reinstate the retired parenthetical form.
    t_agent = real_agent_text + "\n\n" + _AGENT_VALIDATE_RETIRED + "\n"
    _check_negative(
        "t",
        _check_agent_surface(t_agent, real_reference_texts, real_stubs["fishbone"]),
        "Agent-2",
    )

    # (u) Agent-3 control: move the validate-named literal outside the
    # branching block entirely (it is still present exactly once).
    u_agent = _move_validate_outside_branching(real_agent_text)
    _check_negative(
        "u",
        _check_agent_surface(u_agent, real_reference_texts, real_stubs["fishbone"]),
        "Agent-3",
    )

    # (v/v2) Agent-4 control: remove the proportionality paragraph entirely.
    # Must fire BOTH Agent-4 (agent-surface note-present check) and Parity-1
    # (cross-surface note-missing anti-vacuity guard) from the SAME fixture —
    # each asserted under its own label.
    v_agent = _strip_agent_note(real_agent_text)
    _check_negative(
        "v",
        _check_agent_surface(v_agent, real_reference_texts, real_stubs["fishbone"]),
        "Agent-4",
    )
    _check_negative("v2", _check_cross_surface_parity(v_agent, real_stubs), "Parity-1")

    # (w1-w3) Agent-5 controls: strip each of the three depth literals in
    # turn, so no single literal's assertion can rot.
    for i, literal in enumerate(_AGENT_DEPTH_TOKENS, start=1):
        w_agent = _replace_once(real_agent_text, literal, "XXX")
        _check_negative(
            f"w{i}",
            _check_agent_surface(w_agent, real_reference_texts, real_stubs["fishbone"]),
            "Agent-5",
            literal,
        )

    # (x1-x2) Agent-6 controls: strip each of the two act-limb literals.
    for i, literal in enumerate(_AGENT_ACT_LIMB_TOKENS, start=1):
        x_agent = _replace_once(real_agent_text, literal, "XXX")
        _check_negative(
            f"x{i}",
            _check_agent_surface(x_agent, real_reference_texts, real_stubs["fishbone"]),
            "Agent-6",
            literal,
        )

    # (y1-y9) Agent-7 controls: for each of the three reference files, in
    # turn — (a) strip the Exit criterion line, (b) duplicate it (the
    # failure must cite the count), (c) move it outside `## Procedure`.
    y_index = 0
    for ref_slug in _AGENT_REFERENCE_SLUGS:
        y_index += 1
        strip_refs = _mutate_ref(real_reference_texts, ref_slug, _EXIT_CRITERION_LINE, "")
        _check_negative(
            f"y{y_index}",
            _check_agent_surface(real_agent_text, strip_refs, real_stubs["fishbone"]),
            "Agent-7",
            "expected exactly 1",
        )

        y_index += 1
        dup_refs = _duplicate_in_ref(real_reference_texts, ref_slug, _EXIT_CRITERION_LINE)
        _check_negative(
            f"y{y_index}",
            _check_agent_surface(real_agent_text, dup_refs, real_stubs["fishbone"]),
            "Agent-7",
            "2 time(s)",
        )

        y_index += 1
        moved_refs = _move_exit_criterion_to_top(real_reference_texts, ref_slug)
        _check_negative(
            f"y{y_index}",
            _check_agent_surface(real_agent_text, moved_refs, real_stubs["fishbone"]),
            "Agent-7",
            "falls outside",
        )

    # (z) Agent-8 control: strip the Exit criterion line from the fishbone
    # stub fixture — the D-05 clamp-safety case.
    z_fishbone_stub = _replace_once(real_stubs["fishbone"], _EXIT_CRITERION_LINE, "")
    _check_negative(
        "z",
        _check_agent_surface(real_agent_text, real_reference_texts, z_fishbone_stub),
        "Agent-8",
    )

    # (aa) Parity-1 control: the agent note is absent (strip the
    # branching-label anchor `_agent_parity_note()` depends on).
    aa_agent = _replace_once(real_agent_text, _AGENT_EXECUTION_BRANCHING_LABEL, "")
    _check_negative("aa", _check_cross_surface_parity(aa_agent, real_stubs), "Parity-1")

    # (ab) Parity-2 control: the agent note is present (anchors intact) but
    # every parity token has been replaced with neutral prose that names
    # none of the five — the empty-derivation anti-vacuity proof.
    real_note = _agent_parity_note(real_agent_text)
    assert real_note  # positive control (a3) already proved this is non-empty
    ab_agent = _replace_once(
        real_agent_text,
        real_note,
        "Focused mode behaves differently in ways not described by any pinned phrase here.",
    )
    _check_negative("ab", _check_cross_surface_parity(ab_agent, real_stubs), "Parity-2")

    # (ac) Parity-3 control: the agent note is missing exactly ONE of the
    # five tokens — must fire Parity-3, NOT Parity-2.
    ac_agent = _replace_once(real_agent_text, _PT_SIX_SECTION_DOC, "XXX")
    _check_negative("ac", _check_cross_surface_parity(ac_agent, real_stubs), "Parity-3")

    # (ad) Parity-4 one-sided-reword control — the exact scenario D-10
    # exists to catch: reword a parity token in ONE stub's section while
    # leaving the agent note untouched.
    ad_stubs = _mutate_one(real_stubs, "validate", _PT_STAYS_MARKED, "remains flagged")
    _check_negative(
        "ad", _check_cross_surface_parity(real_agent_text, ad_stubs), "Parity-4", "validate"
    )

    # (ae) Parity-4 reverse control: reword a parity token in the AGENT note
    # while leaving all 13 stubs untouched. MEASURED (not assumed) which ID
    # this trips: removing any one of the five tokens from the agent note
    # makes the agent-side derivation itself incomplete (4 of 5), so
    # Parity-3's guard returns before the 13-way stub comparison (Parity-4)
    # ever runs — this is the anti-vacuity layering working as intended, not
    # a mis-targeted control. Documented here rather than asserting Parity-4
    # and silently getting a "wrong reason" report.
    ae_agent = _replace_once(real_agent_text, _PT_SIX_CRITERION_GATE, "XXX")
    _check_negative("ae", _check_cross_surface_parity(ae_agent, real_stubs), "Parity-3")

    # (af) Parity-5 control: a fixture set with 12 stubs (one whole
    # non-launcher slug removed), re-asserting the count at the parity
    # layer distinctly from Stub-1's own count check.
    af_stubs = dict(real_stubs)
    del af_stubs["five-whys"]
    _check_negative("af", _check_cross_surface_parity(real_agent_text, af_stubs), "Parity-5")

    # (ag) Coherence control: un-derive one anchor in a scratch namespace
    # (assign an independent literal that differs from a fresh
    # recomputation) and assert `_check_anchor_coherence` fires.
    _this_module_for_ag = sys.modules[__name__]
    original_depth_tokens = _this_module_for_ag._AGENT_DEPTH_TOKENS
    try:
        _this_module_for_ag._AGENT_DEPTH_TOKENS = (
            _PT_SIX_CRITERION_GATE,
            "an independently retyped literal, not derived from _PT_SIX_SECTION_DOC",
            _PT_SCOPE_PROPORTIONATE,
        )
        ag_failures = _check_anchor_coherence()
    finally:
        _this_module_for_ag._AGENT_DEPTH_TOKENS = original_depth_tokens
    _check_negative("ag", ag_failures, "Coherence")

    # (ah/ah2) Reflow control (positive): the agent body re-wrapped at a
    # width distinct from the shipped file's must still PASS both the
    # agent-surface and the cross-surface checks — the direct, measured
    # guard against the Phase 2 whitespace defect, applied to this plan's
    # own new surface.
    ah_agent = _reflow(real_agent_text, _WRAP_WIDTH)
    _check_positive(
        "ah", _check_agent_surface(ah_agent, real_reference_texts, real_stubs["fishbone"])
    )
    _check_positive("ah2", _check_cross_surface_parity(ah_agent, real_stubs))

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
