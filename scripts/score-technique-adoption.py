#!/usr/bin/env python3
"""Technique-adoption scorer for the v9.12 technique-coverage catalog.

Offline and deterministic: it never invokes `claude`, never writes into
`tests/`, and defaults its emission to stdout. It reads captures a live
harness run already produced -- `.jsonl` transcripts, or the extracted
`.md` analyses persisted beside them -- and reports, per capture, how each
v9.10.0 technique workstream fared.

Why it is three-valued rather than binary
-----------------------------------------
`.planning/AGENT-EVAL-3GEN-2026-09-24.md` §5 recorded `TIGHT-02 three-tier
bracket: 0/5` and then had to explain, in prose, that an ethics/allocation
problem has no governing physical bound, so theoretical-limit correctly
declined to fire. A present/absent reading cannot express that: the zero
for "the technique declined" and the zero for "the technique fired and
ignored its prescription" are the same number, and the difference between
them is the entire finding. So every workstream reports one of:

    n/a -- technique not invoked
    absent -- invoked, prescription not followed
    present

Invocation is detected separately from prescription-adherence, from
disjoint marker sets, so `absent` is reachable rather than collapsing back
into a binary.

Where the markers come from
---------------------------
Every marker literal is transcribed from shipped source -- the technique
reference files under `shared/references/` and the phase prose in
`shared/spine/SKILL-body.md` -- and carries its own `path:line` citation in
`WORKSTREAMS` below. `--self-test` re-reads each cited location and fails if
the literal is not there, so a marker someone invents later (measuring a
guess about the prescription rather than the prescription) cannot pass
silently.

Disclosed bounds
----------------
(a) The verdict is derived from emitted text only. A `Read` of a technique's
    own reference file is reported as supporting evidence when scoring a
    `.jsonl`, and never folded into the verdict: opening a procedure is not
    applying it.
(b) Marker matching is whitespace-normalised across the whole document, so a
    literal hard-wrapped across lines is still found; it is case-insensitive;
    and it is literal, never semantic. A prescription followed in reworded
    form reads `absent` here. That is the honest failure direction for an
    adoption reading of prescribed vocabulary.
(c) Scoring a capture directory is a measurement, not a gate. It exits
    successfully whatever the verdicts say. `docs/v8.7-constraint-teardown.md`
    §2 item 3 bars a K-of-N live result from gating a phase, and this tool is
    deliberately unregistered in `scripts/check-firewall-battery.sh`.

Usage:
    python3 scripts/score-technique-adoption.py --captures DIR [--detail]
    python3 scripts/score-technique-adoption.py --self-test

Exit codes:
    0  scoring completed, or --self-test passed
    1  --self-test failed, or a usage/IO error
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Callable, NamedTuple

REPO_ROOT = Path(__file__).resolve().parent.parent

# --- the three values -------------------------------------------------------
#
# The exact strings this tool reports. They are the vocabulary the eval's §5
# lacked; keep them stable so a later reading can be compared to an earlier one.
NA = "n/a — technique not invoked"
ABSENT = "absent — invoked, prescription not followed"
PRESENT = "present"

_VALUES = (NA, ABSENT, PRESENT)


class Marker(NamedTuple):
    """One marker literal plus the shipped location it was transcribed from.

    `source` is `<repo-relative path>:<line>`. `--self-test` re-reads that
    line and asserts the literal is present on it.
    """

    literal: str
    source: str


class Component(NamedTuple):
    """One technique within a workstream.

    `invocation` markers say the technique fired at all; `prescription`
    markers say the prescribed behaviour was followed. The two sets are
    disjoint by construction -- a self-test control asserts it -- because an
    overlap would make `absent` unreachable.

    `prescription_mode` is `all` when the prescription is a conjunction (the
    lens pass is a coverage check over both lenses) and `any` when the
    prescription has accepted alternate surface forms (a direction word for
    one tier, a bare noun for another).

    A conjunction across several `Component`s within one `Workstream`, each
    itself `any`, is expressed by giving every one of them the SAME
    `invocation` set and letting `combine()` roll them up (999.171): when the
    technique is invoked at all, every sibling component's `inv_hits` becomes
    non-empty together, so each one reads `present` or `absent` -- never
    `n/a` -- and the workstream is `present` only when every sibling is. The
    three-tier bracket (`TIGHT-02`) uses this shape: one `any`-mode component
    per tier, not one `all`-mode component with alternates inside it.
    """

    name: str
    slug: str
    invocation: tuple[Marker, ...]
    prescription: tuple[Marker, ...]
    prescription_mode: str


class Workstream(NamedTuple):
    """A v9.10.0 technique workstream, as named in the eval's §1 table."""

    id: str
    title: str
    components: tuple[Component, ...]


# The declination form the agent body prescribes when an invocation does not
# fire. Transcribed from shared/spine/SKILL-body.md:116:
#   "when an invocation does not fire, record one line, `<technique> — not
#    applicable — <reason>`, in a `Techniques not applied:` block"
# A line matching this shape for a technique is stripped before invocation
# scanning -- otherwise the technique's own name, written there to say it did
# NOT fire, would read as evidence that it did.
DECLINATION_BLOCK_HEADING = Marker("Techniques not applied:", "shared/spine/SKILL-body.md:116")
DECLINATION_LINE_PHRASE = Marker("not applicable", "shared/spine/SKILL-body.md:116")


WORKSTREAMS: tuple[Workstream, ...] = (
    Workstream(
        # Restructured 999.171: the prescription is a conjunction across three
        # tiers with accepted alternates *within* each tier (a direction word
        # for tier 1, a bare noun for tier 3) -- a shape the old single
        # `prescription_mode="all"` component could not express without either
        # requiring every alternate at once or accepting any one of them
        # anywhere. Splitting into one `Component` per tier, each
        # `prescription_mode="any"`, lets `combine()` supply the conjunction
        # across tiers for free: it already returns `absent` if any component
        # is `absent` and `present` only when all are. All three components
        # share the same invocation markers, which is what makes that
        # conjunction correct rather than merely convenient -- see the
        # Component docstring.
        id="TIGHT-02",
        title="theoretical-limit — three-tier bracket",
        components=(
            Component(
                name="theoretical-limit ideal-bound tier",
                slug="theoretical-limit",
                invocation=(
                    Marker("theoretical limit", "shared/references/theoretical-limit.md:1"),
                    Marker("theoretical-limit", "shared/spine/SKILL-body.md:103"),
                    Marker("governing hard constraint", "shared/references/theoretical-limit.md:21"),
                    Marker("law-permitted", "shared/references/theoretical-limit.md:47"),
                ),
                # theoretical-limit.md:88 "**Bracket in three tiers.**", tier 1
                # (:90-91) named as either instantiation of the ideal bound --
                # the 999.171 direction widening.
                prescription=(
                    Marker("ideal ceiling", "shared/references/theoretical-limit.md:90"),
                    Marker("ideal floor", "shared/references/theoretical-limit.md:91"),
                ),
                prescription_mode="any",
            ),
            Component(
                name="theoretical-limit best-demonstrated tier",
                slug="theoretical-limit",
                invocation=(
                    Marker("theoretical limit", "shared/references/theoretical-limit.md:1"),
                    Marker("theoretical-limit", "shared/spine/SKILL-body.md:103"),
                    Marker("governing hard constraint", "shared/references/theoretical-limit.md:21"),
                    Marker("law-permitted", "shared/references/theoretical-limit.md:47"),
                ),
                # theoretical-limit.md:94, tier 2.
                prescription=(
                    Marker("best demonstrated", "shared/references/theoretical-limit.md:94"),
                ),
                prescription_mode="any",
            ),
            Component(
                name="theoretical-limit conventional tier",
                slug="theoretical-limit",
                invocation=(
                    Marker("theoretical limit", "shared/references/theoretical-limit.md:1"),
                    Marker("theoretical-limit", "shared/spine/SKILL-body.md:103"),
                    Marker("governing hard constraint", "shared/references/theoretical-limit.md:21"),
                    Marker("law-permitted", "shared/references/theoretical-limit.md:47"),
                ),
                # theoretical-limit.md:97, tier 3 -- the bare noun (matching
                # "Conventional figure", "Conventional:" and "conventional
                # practice" alike) plus "current practice" from the same line.
                # Deliberately NOT widened to accept "this plant" or any other
                # system name: that is the label rule Task 1 now states
                # explicitly (":97-100"), so an unprescribed name is measurably
                # non-adherent rather than merely unrecognised. See FIXTURES
                # "r1-verbatim" for the standing control.
                prescription=(
                    Marker("conventional", "shared/references/theoretical-limit.md:97"),
                    Marker("current practice", "shared/references/theoretical-limit.md:97"),
                ),
                prescription_mode="any",
            ),
        ),
    ),
    Workstream(
        id="TECH-01",
        title="five-whys — counterfactual test",
        components=(
            Component(
                name="five-whys counterfactual test",
                slug="five-whys",
                invocation=(
                    Marker("5-whys", "shared/references/five-whys.md:1"),
                    Marker("five whys", "shared/spine/SKILL-body.md:106"),
                    Marker("5 whys", "shared/spine/SKILL-body.md:106"),
                    Marker("reduce-to-primitives", "shared/references/five-whys.md:1"),
                    Marker("root cause", "shared/references/five-whys.md:105"),
                ),
                # five-whys.md:66 "**Apply the counterfactual test to every cause
                # before descending into it.**" -- accepted alternate surface
                # forms are the test's own question form and its pass verdict.
                prescription=(
                    Marker("counterfactual test", "shared/references/five-whys.md:66"),
                    Marker("counterfactually necessary", "shared/references/five-whys.md:69"),
                    Marker(
                        "would the symptom still have happened",
                        "shared/references/five-whys.md:67",
                    ),
                ),
                prescription_mode="any",
            ),
        ),
    ),
    Workstream(
        id="TECH-05",
        title="second-order — actor/time lens",
        components=(
            Component(
                name="second-order actor/time lens",
                slug="second-order",
                invocation=(
                    Marker("second-order", "shared/references/second-order.md:1"),
                    Marker("2nd-order", "shared/references/second-order.md:33"),
                    Marker("downstream consequences", "shared/spine/SKILL-body.md:108"),
                ),
                # second-order.md:49 "**Enumerate 2nd-order consequences through
                # two lenses.**", naming them at :54 and :60. Both, because the
                # lenses are coverage checks over different failure directions.
                prescription=(
                    Marker("actor lens", "shared/references/second-order.md:54"),
                    Marker("time lens", "shared/references/second-order.md:60"),
                ),
                prescription_mode="all",
            ),
        ),
    ),
    Workstream(
        # Carried as positive controls: both read 5/5 on the ethics prompt in
        # the eval's §1 table. If either reads `absent` on a capture here,
        # suspect this scorer before believing the finding.
        id="TRADE/PASS",
        title="trade-off knock-out + pre-mortem tripwire (positive controls)",
        components=(
            Component(
                name="trade-off knock-out",
                slug="trade-off",
                invocation=(
                    Marker("trade-off", "shared/references/trade-off.md:1"),
                    Marker("weighted total", "shared/references/trade-off.md:34"),
                ),
                # trade-off.md:30 "**State the must-haves and apply them as
                # knock-outs.**"; :33 "report it under `## Options` as knocked
                # out, with the must-have it failed".
                prescription=(
                    Marker("knock-out", "shared/references/trade-off.md:30"),
                    Marker("knocked out", "shared/references/trade-off.md:33"),
                ),
                prescription_mode="any",
            ),
            Component(
                name="pre-mortem tripwire",
                slug="pre-mortem",
                # Only the hyphenated form: `premortem` appears nowhere in
                # shipped source, and the provenance control caught it when it
                # was first written here as a plausible-looking variant.
                invocation=(Marker("pre-mortem", "shared/references/pre-mortem.md:1"),),
                # pre-mortem.md:83 "**Give every fatal and costly cluster a
                # tripwire.**"
                prescription=(Marker("tripwire", "shared/references/pre-mortem.md:83"),),
                prescription_mode="any",
            ),
        ),
    ),
)


# --- text preparation -------------------------------------------------------


def _normalise(text: str) -> str:
    """Lowercase and collapse all whitespace runs to single spaces.

    Disclosed bound (b): this is what lets a marker hard-wrapped across two
    physical lines still match, and it is why matching is case-insensitive.
    """
    return re.sub(r"\s+", " ", text).lower()


def _strip_declination_lines(text: str, slug: str) -> tuple[str, bool]:
    """Remove the prescribed declination line for *slug*, if present.

    Returns the remaining text and whether a declination was seen. A line
    naming the technique alongside the `not applicable` phrase is the body's
    prescribed way of recording that the invocation did NOT fire
    (SKILL-body.md:116), so its mention of the technique must not be counted
    as invocation evidence.
    """
    kept: list[str] = []
    declined = False
    phrase = DECLINATION_LINE_PHRASE.literal.lower()
    for line in text.splitlines():
        low = line.lower()
        if slug in low and phrase in low:
            declined = True
            continue
        kept.append(line)
    return "\n".join(kept), declined


def _matched(norm: str, markers: tuple[Marker, ...]) -> list[str]:
    return [m.literal for m in markers if m.literal.lower() in norm]


# --- scoring ----------------------------------------------------------------


class ComponentReading(NamedTuple):
    component: str
    verdict: str
    invocation_hits: tuple[str, ...]
    prescription_hits: tuple[str, ...]
    declined: bool


def score_component(text: str, comp: Component) -> ComponentReading:
    """Three-valued reading for one component.

    Order matters. A satisfied prescription implies invocation -- an emission
    that brackets in tiers has plainly run theoretical-limit whether or not it
    named it -- so the prescription test comes first and the invocation test
    only decides between `absent` and `n/a`.
    """
    stripped, declined = _strip_declination_lines(text, comp.slug)
    norm = _normalise(stripped)
    pres_hits = _matched(norm, comp.prescription)
    inv_hits = _matched(norm, comp.invocation)

    if comp.prescription_mode == "all":
        satisfied = len(pres_hits) == len(comp.prescription)
    elif comp.prescription_mode == "any":
        satisfied = bool(pres_hits)
    else:  # pragma: no cover - guarded by _self_test_structure_problems
        raise ValueError(f"unknown prescription_mode {comp.prescription_mode!r}")

    if satisfied:
        verdict = PRESENT
    elif inv_hits or pres_hits:
        verdict = ABSENT
    else:
        verdict = NA
    return ComponentReading(
        component=comp.name,
        verdict=verdict,
        invocation_hits=tuple(inv_hits),
        prescription_hits=tuple(pres_hits),
        declined=declined,
    )


def combine(readings: list[ComponentReading]) -> str:
    """Roll component readings up to a workstream verdict.

    All components silent -> the workstream was not invoked. Any invoked
    component whose prescription is unmet -> `absent`; a partial adoption is
    reported as non-adoption rather than averaged away.
    """
    verdicts = [r.verdict for r in readings]
    if all(v == NA for v in verdicts):
        return NA
    if any(v == ABSENT for v in verdicts):
        return ABSENT
    return PRESENT


def score_text(text: str) -> dict[str, str]:
    """Workstream id -> one of the three values."""
    return {
        ws.id: combine([score_component(text, c) for c in ws.components])
        for ws in WORKSTREAMS
    }


def score_text_detail(text: str) -> dict[str, list[ComponentReading]]:
    return {ws.id: [score_component(text, c) for c in ws.components] for ws in WORKSTREAMS}


# --- capture loading --------------------------------------------------------

_TEXT_SUFFIXES = (".md", ".txt")


def _jsonl_text(path: Path) -> str:
    """Every text-bearing field of a transcript, concatenated.

    Assistant text blocks, tool-result text (a subagent hands its analysis
    back through one) and the terminal `result` string. Undecodable lines are
    skipped rather than raising -- a truncated capture should still score.
    """
    chunks: list[str] = []
    raw = path.read_text(encoding="utf-8", errors="replace")
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(obj, dict):
            continue
        if isinstance(obj.get("result"), str):
            chunks.append(obj["result"])
        message = obj.get("message")
        content = message.get("content") if isinstance(message, dict) else None
        if isinstance(content, str):
            chunks.append(content)
        elif isinstance(content, list):
            for block in content:
                if not isinstance(block, dict):
                    continue
                if isinstance(block.get("text"), str):
                    chunks.append(block["text"])
                inner = block.get("content")
                if isinstance(inner, str):
                    chunks.append(inner)
                elif isinstance(inner, list):
                    for sub in inner:
                        if isinstance(sub, dict) and isinstance(sub.get("text"), str):
                            chunks.append(sub["text"])
    return "\n".join(chunks)


def _reference_reads(path: Path) -> tuple[str, ...]:
    """Which technique reference files a transcript shows being read.

    Supporting evidence only -- disclosed bound (a). Empty for `.md` inputs,
    which carry no tool-call record at all.
    """
    if path.suffix != ".jsonl":
        return ()
    text = path.read_text(encoding="utf-8", errors="replace")
    slugs = sorted(
        {
            c.slug
            for ws in WORKSTREAMS
            for c in ws.components
            if f"references/{c.slug}.md" in text
        }
    )
    return tuple(slugs)


def load_captures(directory: Path) -> list[tuple[str, str, tuple[str, ...]]]:
    """(label, text, reference_reads) per capture file, sorted by name.

    A `.jsonl` and its extracted `.md` sibling describe the same generation,
    so when both are present the `.md` wins -- it is the analysis, without the
    transcript scaffolding around it.
    """
    if not directory.is_dir():
        raise SystemExit(f"error: --captures {directory} is not a directory")
    by_stem: dict[str, Path] = {}
    for path in sorted(directory.iterdir()):
        if not path.is_file():
            continue
        if path.suffix not in _TEXT_SUFFIXES and path.suffix != ".jsonl":
            continue
        prev = by_stem.get(path.stem)
        if prev is not None and prev.suffix in _TEXT_SUFFIXES:
            continue
        by_stem[path.stem] = path
    out: list[tuple[str, str, tuple[str, ...]]] = []
    for stem in sorted(by_stem):
        path = by_stem[stem]
        text = _jsonl_text(path) if path.suffix == ".jsonl" else path.read_text(
            encoding="utf-8", errors="replace"
        )
        out.append((path.name, text, _reference_reads(path)))
    return out


# --- emission ---------------------------------------------------------------


def render(captures: list[tuple[str, str, tuple[str, ...]]], detail: bool) -> str:
    lines: list[str] = []
    lines.append("# Technique adoption reading")
    lines.append("")
    lines.append(
        "Three-valued per workstream. A recorded observation stated with its N, "
        "never a gate (docs/v8.7-constraint-teardown.md §2 item 3)."
    )
    lines.append("")
    lines.append(f"N = {len(captures)} capture file(s).")
    lines.append("")
    header = "| Capture | " + " | ".join(ws.id for ws in WORKSTREAMS) + " | Reference reads |"
    sep = "|---|" + "---|" * (len(WORKSTREAMS) + 1)
    lines.append(header)
    lines.append(sep)
    tally: dict[str, dict[str, int]] = {
        ws.id: {v: 0 for v in _VALUES} for ws in WORKSTREAMS
    }
    for label, text, refs in captures:
        verdicts = score_text(text)
        for ws in WORKSTREAMS:
            tally[ws.id][verdicts[ws.id]] += 1
        cells = " | ".join(verdicts[ws.id] for ws in WORKSTREAMS)
        lines.append(f"| {label} | {cells} | {', '.join(refs) if refs else '—'} |")
    lines.append("")
    lines.append("## Adoption")
    lines.append("")
    lines.append("| Workstream | Technique | present | absent | n/a |")
    lines.append("|---|---|---|---|---|")
    n = len(captures)
    for ws in WORKSTREAMS:
        t = tally[ws.id]
        lines.append(
            f"| {ws.id} | {ws.title} | {t[PRESENT]}/{n} | {t[ABSENT]}/{n} | {t[NA]}/{n} |"
        )
    lines.append("")
    lines.append(
        "`n/a` is the technique not firing, which on a prompt with no occasion for it "
        "is correct behaviour; `absent` is the technique firing and not following its "
        "prescription. Read them separately — collapsing them is the ambiguity this "
        "tool exists to remove."
    )
    if detail:
        lines.append("")
        lines.append("## Matched literals")
        lines.append("")
        for label, text, _refs in captures:
            lines.append(f"### {label}")
            lines.append("")
            for ws in WORKSTREAMS:
                for r in score_text_detail(text)[ws.id]:
                    inv = ", ".join(r.invocation_hits) or "—"
                    pres = ", ".join(r.prescription_hits) or "—"
                    dec = " [explicitly declined]" if r.declined else ""
                    lines.append(
                        f"- {ws.id} / {r.component}: {r.verdict}{dec} "
                        f"(invocation: {inv}; prescription: {pres})"
                    )
            lines.append("")
    return "\n".join(lines) + "\n"


# --- self-test --------------------------------------------------------------

_FIX_PRESENT_ALL = """
## Phase 4 — Reason Upward

The governing hard constraint is the free energy of mixing, so the theoretical limit
is derived rather than observed. Bracket in three tiers: the Ideal ceiling is the
law-permitted floor; the Best demonstrated figure is a cited published result; the
Conventional figure is what this plant achieves today.

A 5-Whys pass drills the recurrence. Applying the counterfactual test to each cause:
had this cause not occurred, would the symptom still have happened?

Second-order effects, through the actor lens (who changes what they do) and the
time lens (immediately, after a few cycles, once assumed).

Trade-off analysis: the must-haves are applied as knock-outs before any scoring, so
option C is knocked out rather than scored, and the weighted total decides the rest.

Pre-mortem: each fatal cluster carries a tripwire naming the observation that would
tell us the failure is underway.
"""

_FIX_ABSENT_ALL = """
## Phase 4 — Reason Upward

The theoretical limit for this separation is about one kilowatt-hour per cubic metre.
We compare the vendor's quoted figure against it and conclude there is headroom.

A 5-Whys pass gives the root cause: the inventory lock is contended under load.

Second-order effects: consumers redeploy, and the 2nd-order cost compounds.

Trade-off analysis over three options, scored and weighted; the highest weighted
total wins.

Pre-mortem: the plan fails because the migration window slips.
"""

_FIX_NONE = """
## Phase 4 — Reason Upward

We priced the upgrade against the current spend and concluded the payback period is
longer than the board's horizon, so we recommend deferring the purchase and
renegotiating the quote next cycle.
"""

_FIX_DECLINED = """
## Phase 4 — Reason Upward

Second-order effects through the actor lens and the time lens are enumerated below.
The must-haves are applied as knock-outs before scoring. Every fatal cluster in the
pre-mortem carries a tripwire.

Techniques not applied:
- theoretical-limit — not applicable — no governing physical bound binds this decision
- five-whys — not applicable — this is a forward-looking choice, not a recurrence
"""

_FIX_PARTIAL = """
## Phase 4 — Reason Upward

The theoretical limit is derived from the governing law. The Ideal ceiling is stated
and the Conventional figure is stated, and the gap between them is the headroom.

Second-order effects are enumerated through the actor lens.
"""

_FIX_MIXED_CONTROLS = """
## Phase 4 — Reason Upward

Trade-off analysis: the must-haves are applied as knock-outs, so the non-viable
option is knocked out rather than scored.

Pre-mortem: the plan has already failed, and the causes cluster into three
structural weaknesses, each triaged fatal, costly but survivable, or tolerable.
"""

_FIX_WRAPPED = """
## Phase 4 — Reason Upward

Second-order effects are walked through the actor
lens and the time
lens.

The bracket: Ideal
ceiling, Best
demonstrated, Conventional
figure — the governing hard constraint fixes the first.
"""

# The three fixtures below (999.171) stand in for the `260924-tcv` QT-P1
# captures. Those 15 captures were never persisted -- 999.172 records them as
# session scratchpad, deliberately outside `tests/` and therefore ephemeral --
# so there is nothing on disk to re-score. Each text below is transcribed
# verbatim from the two output blocks quoted inside the 999.171 ROADMAP
# amendment, the only surviving evidence the defect reached live output.
_FIX_MINIMISATION_PRESENT = """
Theoretical-limit tiers:
- Ideal floor: about 1.3 kWh/m³ (reversible, at 45% recovery).
- Best demonstrated: under 2 kWh/m³ (GT-8, salinity unstated).
- Conventional: 3.8 kWh/m³.
"""

_FIX_R3_VERBATIM = """
Theoretical-limit bracket:
- **Ideal ceiling:** 1.28 kWh/m³ (reversible), or 1.75 kWh/m³ for single-stage with perfect equipment.
- **Best demonstrated:** about 3 kWh/m³ (GT-11), at ordinary rather than Gulf salinity.
- **Conventional:** this plant's 3.8 kWh/m³.
- **Gaps:** ... About 1.2–1.7 kWh/m³ from demonstrated to ceiling, reached by nobody.
"""

_FIX_R1_VERBATIM = """
Theoretical-limit tiers:
- Ideal floor: about 1.3 kWh/m³ (reversible, at 45% recovery).
- Best demonstrated: under 2 kWh/m³ (GT-8, salinity unstated).
- This plant: 3.8 kWh/m³.
"""


class Fixture(NamedTuple):
    name: str
    text: str
    expected: dict[str, str]
    note: str


FIXTURES: tuple[Fixture, ...] = (
    Fixture(
        "present-all",
        _FIX_PRESENT_ALL,
        {"TIGHT-02": PRESENT, "TECH-01": PRESENT, "TECH-05": PRESENT, "TRADE/PASS": PRESENT},
        "every prescription followed in its prescribed vocabulary",
    ),
    Fixture(
        "absent-all",
        _FIX_ABSENT_ALL,
        {"TIGHT-02": ABSENT, "TECH-01": ABSENT, "TECH-05": ABSENT, "TRADE/PASS": ABSENT},
        "every technique invoked, no prescription followed — the state a binary "
        "scorer cannot tell from n/a",
    ),
    Fixture(
        "none-invoked",
        _FIX_NONE,
        {"TIGHT-02": NA, "TECH-01": NA, "TECH-05": NA, "TRADE/PASS": NA},
        "no technique fired; on a prompt with no occasion for one this is correct",
    ),
    Fixture(
        "explicitly-declined",
        _FIX_DECLINED,
        {"TIGHT-02": NA, "TECH-01": NA, "TECH-05": PRESENT, "TRADE/PASS": PRESENT},
        "the prescribed declination block: the technique named there must not read "
        "as invoked (SKILL-body.md:116)",
    ),
    Fixture(
        "partial-conjunction",
        _FIX_PARTIAL,
        {"TIGHT-02": ABSENT, "TECH-01": NA, "TECH-05": ABSENT, "TRADE/PASS": NA},
        "a bracket missing a tier and a lens pass missing a lens are not partial "
        "credit — prescription_mode='all'",
    ),
    Fixture(
        "controls-split",
        _FIX_MIXED_CONTROLS,
        {"TIGHT-02": NA, "TECH-01": NA, "TECH-05": NA, "TRADE/PASS": ABSENT},
        "one component present, the other invoked-without-prescription: the "
        "workstream reads absent, not averaged",
    ),
    Fixture(
        "hard-wrapped",
        _FIX_WRAPPED,
        {"TIGHT-02": PRESENT, "TECH-01": NA, "TECH-05": PRESENT, "TRADE/PASS": NA},
        "markers wrapped across physical lines still match — disclosed bound (b)",
    ),
    Fixture(
        "minimisation-present",
        _FIX_MINIMISATION_PRESENT,
        {"TIGHT-02": PRESENT, "TECH-01": NA, "TECH-05": NA, "TRADE/PASS": NA},
        "999.171: the QT-P1 r1 bracket transcribed from the ROADMAP amendment, "
        "with its unprescribed third-tier label ('This plant:') replaced by the "
        "prescribed 'Conventional:' — the fixture that fails if the direction "
        "widening (ideal floor) is ever reverted. Stands in for a capture that "
        "was never persisted; no re-score of the 15 originals occurred.",
    ),
    Fixture(
        "r3-verbatim",
        _FIX_R3_VERBATIM,
        {"TIGHT-02": PRESENT, "TECH-01": NA, "TECH-05": NA, "TRADE/PASS": NA},
        "999.171: QT-P1 r3, transcribed verbatim from the ROADMAP amendment — "
        "the run that followed the (then maximisation-only) prescription into a "
        "directional error, labelling an energy floor 'Ideal ceiling'. The "
        "fixture that fails if the noun widening (bare 'conventional') is ever "
        "reverted. Stands in for a capture that was never persisted; no "
        "re-score of the 15 originals occurred.",
    ),
    Fixture(
        "r1-verbatim",
        _FIX_R1_VERBATIM,
        {"TIGHT-02": ABSENT, "TECH-01": NA, "TECH-05": NA, "TRADE/PASS": NA},
        "999.171: QT-P1 r1, transcribed verbatim from the ROADMAP amendment — "
        "the standing non-widening control. Its third tier reads 'This plant:', "
        "the system's name rather than the prescribed 'Conventional' label; "
        "declining to match it is a deliberate, recorded call, not an "
        "oversight. Stands in for a capture that was never persisted; no "
        "re-score of the 15 originals occurred.",
    ),
)

Classifier = Callable[[str], dict[str, str]]


def evaluate_fixtures(classify: Classifier) -> list[str]:
    """Run FIXTURES through *classify* and return one failure line per mismatch.

    Parameterised on the classifier so a deliberately-degenerate one can be
    injected and shown to fail — the anti-masking controls below.
    """
    failures: list[str] = []
    for fx in FIXTURES:
        got = classify(fx.text)
        for ws in WORKSTREAMS:
            want = fx.expected[ws.id]
            actual = got.get(ws.id)
            if actual != want:
                failures.append(
                    f"fixture {fx.name}: {ws.id} expected {want!r}, got {actual!r}"
                )
    return failures


def always_present(_text: str) -> dict[str, str]:
    """Anti-masking control: a scorer that never finds anything absent."""
    return {ws.id: PRESENT for ws in WORKSTREAMS}


def always_na(_text: str) -> dict[str, str]:
    """Anti-masking control: a scorer that calls every technique un-invoked."""
    return {ws.id: NA for ws in WORKSTREAMS}


def structure_problems() -> list[str]:
    """Structural controls over WORKSTREAMS itself."""
    problems: list[str] = []
    seen_ids: set[str] = set()
    for ws in WORKSTREAMS:
        if ws.id in seen_ids:
            problems.append(f"duplicate workstream id {ws.id!r}")
        seen_ids.add(ws.id)
        if not ws.components:
            problems.append(f"{ws.id}: no components")
        for c in ws.components:
            if c.prescription_mode not in ("any", "all"):
                problems.append(
                    f"{ws.id}/{c.name}: unknown prescription_mode {c.prescription_mode!r}"
                )
            if not c.invocation:
                problems.append(f"{ws.id}/{c.name}: no invocation markers")
            if not c.prescription:
                problems.append(f"{ws.id}/{c.name}: no prescription markers")
            inv = {m.literal.lower() for m in c.invocation}
            pres = {m.literal.lower() for m in c.prescription}
            overlap = inv & pres
            if overlap:
                # An overlapping literal would make `absent` unreachable for
                # that component, collapsing the tool back into a binary.
                problems.append(
                    f"{ws.id}/{c.name}: invocation/prescription markers overlap: "
                    f"{sorted(overlap)}"
                )
            for a in inv:
                for b in pres:
                    if a in b or b in a:
                        problems.append(
                            f"{ws.id}/{c.name}: marker {a!r} is a substring of {b!r} — "
                            "the two sets must be independent"
                        )
    return problems


def provenance_problems() -> list[str]:
    """Re-read every cited shipped location and confirm the literal is there.

    This is the control that stops an invented marker. A literal that no
    longer sits at its cited line is a failure, whether because someone made
    it up or because the shipped prose moved underneath it.
    """
    problems: list[str] = []
    cache: dict[str, list[str]] = {}
    markers: list[Marker] = [DECLINATION_BLOCK_HEADING, DECLINATION_LINE_PHRASE]
    for ws in WORKSTREAMS:
        for c in ws.components:
            markers.extend(c.invocation)
            markers.extend(c.prescription)
    for m in markers:
        path_part, _, line_part = m.source.rpartition(":")
        if not path_part or not line_part.isdigit():
            problems.append(f"marker {m.literal!r}: malformed source {m.source!r}")
            continue
        if path_part not in cache:
            p = REPO_ROOT / path_part
            if not p.is_file():
                problems.append(f"marker {m.literal!r}: source file {path_part} not found")
                cache[path_part] = []
                continue
            cache[path_part] = p.read_text(encoding="utf-8").splitlines()
        lines = cache[path_part]
        lineno = int(line_part)
        if not 1 <= lineno <= len(lines):
            problems.append(f"marker {m.literal!r}: {m.source} is out of range")
            continue
        if m.literal.lower() not in lines[lineno - 1].lower():
            problems.append(
                f"marker {m.literal!r} not found at {m.source} — "
                "derive markers from shipped source, never invent them"
            )
    return problems


def io_problems() -> list[str]:
    """Controls over loading and emission, without touching the filesystem."""
    problems: list[str] = []
    jsonl = "\n".join(
        [
            json.dumps(
                {
                    "type": "assistant",
                    "message": {
                        "content": [
                            {"type": "text", "text": "Ideal ceiling, Best demonstrated,"},
                            {"type": "text", "text": "Conventional figure; theoretical limit."},
                        ]
                    },
                }
            ),
            "{ not json",
            json.dumps({"type": "result", "result": "actor lens and time lens; second-order."}),
        ]
    )
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        (d / "gen-a.jsonl").write_text(jsonl, encoding="utf-8")
        (d / "gen-b.md").write_text(_FIX_NONE, encoding="utf-8")
        # gen-d carries the `absent` value, so the rendering control below can
        # assert all three values reach the emission.
        (d / "gen-d.md").write_text(_FIX_ABSENT_ALL, encoding="utf-8")
        (d / "gen-c.jsonl").write_text(
            json.dumps({"type": "assistant", "message": {"content": "references/five-whys.md"}}),
            encoding="utf-8",
        )
        (d / "gen-c.md").write_text(_FIX_PRESENT_ALL, encoding="utf-8")
        (d / "ignored.log").write_text("noise", encoding="utf-8")
        caps = load_captures(d)
        labels = [c[0] for c in caps]
        if labels != ["gen-a.jsonl", "gen-b.md", "gen-c.md", "gen-d.md"]:
            problems.append(f"load_captures labels wrong: {labels}")
        a = score_text(caps[0][1])
        if a["TIGHT-02"] != PRESENT or a["TECH-05"] != PRESENT:
            problems.append(f"jsonl text extraction lost markers: {a}")
        if caps[0][2] != ():
            problems.append(f"unexpected reference reads on gen-a: {caps[0][2]}")
        out = render(caps, detail=True)

    if "## Adoption" not in out or "Matched literals" not in out:
        problems.append("render() missing a required section")
    for value in _VALUES:
        if value not in out:
            problems.append(f"render() never emitted the value {value!r}")
    if "N = 4 capture file(s)." not in out:
        problems.append("render() did not state its N")
    return problems


def self_test() -> int:
    problems: list[str] = []
    problems += [f"[structure] {p}" for p in structure_problems()]
    problems += [f"[provenance] {p}" for p in provenance_problems()]
    problems += [f"[fixture] {p}" for p in evaluate_fixtures(score_text)]
    problems += [f"[io] {p}" for p in io_problems()]

    # Anti-masking: a scorer that cannot fail is not a scorer. Each degenerate
    # classifier is run through the same fixture suite and MUST be caught by it.
    for label, stub in (("always-present", always_present), ("always-na", always_na)):
        stub_failures = evaluate_fixtures(stub)
        if stub_failures:
            print(
                f"[anti-masking] {label} stub: FAILED as designed "
                f"({len(stub_failures)} fixture/workstream mismatches); "
                f"first: {stub_failures[0]}"
            )
        else:
            problems.append(
                f"[anti-masking] {label} stub passed the fixture suite — "
                "the suite cannot detect a degenerate scorer"
            )

    print(f"fixtures: {len(FIXTURES)}; workstreams: {len(WORKSTREAMS)}")
    if problems:
        for p in problems:
            print(f"FAIL {p}", file=sys.stderr)
        print(f"SELF-TEST: FAIL ({len(problems)} problems)", file=sys.stderr)
        return 1
    print("SELF-TEST: PASS")
    return 0


# --- CLI --------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=(
            "Three-valued technique-adoption scorer over a capture directory. "
            "Offline; never invokes claude; never writes into tests/."
        )
    )
    ap.add_argument("--captures", type=Path, help="directory of .jsonl / .md captures")
    ap.add_argument("--detail", action="store_true", help="also list the matched literals")
    ap.add_argument(
        "--out",
        type=Path,
        help="write the report here instead of stdout (refused under tests/)",
    )
    ap.add_argument("--self-test", action="store_true", help="run the offline control suite")
    args = ap.parse_args(argv)

    if args.self_test:
        return self_test()
    if args.captures is None:
        ap.error("one of --captures or --self-test is required")

    captures = load_captures(args.captures)
    if not captures:
        raise SystemExit(f"error: no .jsonl/.md captures found in {args.captures}")
    report = render(captures, detail=args.detail)

    if args.out is None:
        sys.stdout.write(report)
        return 0
    out = args.out.resolve()
    tests_dir = (REPO_ROOT / "tests").resolve()
    if out == tests_dir or tests_dir in out.parents:
        raise SystemExit(
            "error: refusing to write under tests/ — FROZEN-EVIDENCE sweeps that "
            "tree for untracked files; keep captures and reports outside it"
        )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report, encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
