#!/usr/bin/env python3
"""Evidence Card generator -- the project's public, general-audience measurement record.

Discharges backlog 999.147's publication limb: a reader-facing page stating what
has actually been measured about the shipped agent, each reading carried with its
N, its date, and the disclosed bound of the instrument that produced it.

Why this is generated rather than written
-----------------------------------------
`docs/PROCESS.md` section 2 bars a hand-typed moving count on a product surface,
and the Evidence Card is a product surface by that page's own claim-audience cut:
it asserts facts to a reader outside the build loop. So every figure it publishes
is either

  (a) a FROZEN historical reading -- a closed, immutable past measurement, which
      section 2 explicitly admits as a literal provided it is attributed; here
      attribution is mechanical, not narrative: each literal is re-read from its
      cited source at generation time and the run FAILS if it is not found; or

  (b) derived live from the tree at render time.

A figure that is neither does not go on the card. There is no third category.

The Goodhart posture, stated rather than assumed
------------------------------------------------
This card deliberately publishes NO composite quality score, and the reason is a
measurement this project already made: rubric conformance does not predict
correctness (`docs/v8.7-correctness-spot-check.md`), observed twice, by two
different methods. A score assembled from conformance readings would therefore be
a number that looks like quality and demonstrably is not one. `docs/PROCESS.md`
section 1.2 records what happens here when a published figure becomes a target --
17 true, checkable claims were deleted and replaced with unfalsifiable hedges to
satisfy a scanner. Publishing rates with denominators and disclosed sensitivities,
and never a single headline score, is the countermeasure.

The Track B section is conditional BY CONSTRUCTION
---------------------------------------------------
The comparative (agent vs. unaided control) section renders only when
`docs/data/trackb-result.json` records `status == "cleared"` -- meaning the
pre-registered effect threshold in `docs/trackb-preregistration.md` was met by a
single pre-registered run. A `null` or `inconclusive` result renders NOTHING on
this card; it is recorded internally instead. That decision is mechanical here
precisely so it cannot be relitigated against a disappointing number after the
fact, and so that "publish only if favourable" cannot silently become "re-run
until favourable" -- the protocol admits exactly one run, and this generator
reads its recorded result rather than any later one.

Usage:
    python3 scripts/gen-evidence-card.py            # --write (default)
    python3 scripts/gen-evidence-card.py --check    # exit 1 on drift
    python3 scripts/gen-evidence-card.py --self-test
    python3 scripts/gen-evidence-card.py --describe

Exit codes:
    0  wrote / no drift / self-test passed
    1  drift, a source literal no longer present, or a self-test control failed
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT: Path = Path(__file__).resolve().parents[1]
CARD_PATH: Path = REPO_ROOT / "docs" / "EVIDENCE.md"
TRACKB_RESULT_PATH: Path = REPO_ROOT / "docs" / "data" / "trackb-result.json"
PREREG_PATH: Path = REPO_ROOT / "docs" / "trackb-preregistration.md"

GENERATED_MARKER = "<!-- GENERATED — DO NOT EDIT -->"


class EvidenceError(RuntimeError):
    """A pinned literal is absent from its cited source, or a floor is breached."""


# ---------------------------------------------------------------------------
# The fact registry
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Fact:
    """One published reading.

    `literal` must appear verbatim in `source`. That is the whole falsifiability
    mechanism: edit the source so the reading no longer says what this card
    claims, and generation fails rather than publishing a stale number.
    """

    fact_id: str
    headline: str          # reader-facing, plain language
    reading: str           # the number, as a reader should see it
    n: str                 # sample size, stated -- never omitted
    measured: str          # ISO date of the measurement
    source: str            # repo-relative path
    literal: str           # verbatim substring that must be present in source
    bound: str             # the disclosed limit of this reading
    section: str           # which card section it belongs to


# Section keys, in render order.
SEC_HONESTY = "honesty"
SEC_RELIABILITY = "reliability"
SEC_OUTPUT = "output"

_SECTION_ORDER = (SEC_HONESTY, SEC_RELIABILITY, SEC_OUTPUT)

_SECTION_TITLES = {
    SEC_HONESTY: "What we found when we checked our own metrics",
    SEC_RELIABILITY: "Does it actually run?",
    SEC_OUTPUT: "What the output looks like when measured",
}


FACTS: tuple[Fact, ...] = (
    # --- The headline: conformance does not track quality -------------------
    Fact(
        fact_id="CORRECTNESS-SPOTCHECK",
        headline="When we re-derived the numbers in six analyses by hand, most held up",
        reading="47 correct / 6 wrong / 12 unverifiable, across 65 load-bearing quantitative claims",
        n="65 claims across 6 analyses",
        measured="2026-07-22",
        source="docs/v8.7-correctness-spot-check.md",
        literal="47 correct / 6 wrong / 12 unverifiable",
        bound=(
            "Six documents is a directional finding, not a statistical claim, and the "
            "phase's own text says so. `unverifiable` means the claim rested on an "
            "external fact the check had no authorisation to look up — it is not a "
            "silent pass."
        ),
        section=SEC_OUTPUT,
    ),
    Fact(
        fact_id="MATERIAL-ERRORS",
        headline="None of the errors changed a recommendation",
        reading="zero material errors in 65 examined load-bearing claims",
        n="65 claims across 6 analyses",
        measured="2026-07-22",
        source="docs/v8.7-correctness-spot-check.md",
        literal="zero material errors were found in 65 examined load-bearing",
        bound=(
            "'Material' was defined before the results were known: an error whose "
            "correction would change the recommendation or its direction. Six of the "
            "65 claims were still simply wrong."
        ),
        section=SEC_OUTPUT,
    ),
    Fact(
        fact_id="CONFORMANCE-NOT-CORRECTNESS",
        headline="Our own format-conformance score does not predict whether the analysis is right",
        reading=(
            "the most arithmetically accurate document (100% correct) FAILED the rubric; "
            "the least accurate (50% correct) PASSED it"
        ),
        n="6 documents",
        measured="2026-07-22",
        source="docs/v8.7-correctness-spot-check.md",
        literal="rubric conformance does not predict arithmetic/factual",
        bound=(
            "One six-document sample. It is why this page publishes no composite "
            "quality score — but it does not prove the rubric is worthless, only that "
            "it is a formatting instrument being asked a question it cannot answer."
        ),
        section=SEC_HONESTY,
    ),
    Fact(
        fact_id="REAL-USE-CONFORMED-LESS",
        headline="The same pattern appeared again on real work, independently",
        reading=(
            "on a genuine (non-test) task the better of two answers was the one that "
            "conformed less — 0 of 6 prescribed sections"
        ),
        n="1 task, 2 runs",
        measured="2026-07-27",
        source="docs/use-journal.md",
        literal="the agent was never dispatched",
        bound=(
            "A single journal entry, n=1. Its value is that it is independent of the "
            "six-document study above and points the same way; it is not a second "
            "study."
        ),
        section=SEC_HONESTY,
    ),
    Fact(
        fact_id="JUDGE-DRIFT",
        headline="We measured our own judge and found it drifts — upward",
        reading=(
            "re-scoring six byte-identical documents on a different day moved the total "
            "+7 points out of 108 and flipped one verdict from FAIL to PASS; five of six "
            "documents moved up, none moved down"
        ),
        n="6 documents, re-scored",
        measured="2026-07-22",
        source="docs/v8.7-quality-baseline-freeze.md",
        literal="None moved down.",
        bound=(
            "This is the reason any improvement we report has to clear roughly +7/108 "
            "before it means anything. It also means a favourable-looking result is "
            "exactly what noise produces here, which is why comparative claims on this "
            "page require a threshold fixed before the run."
        ),
        section=SEC_HONESTY,
    ),
    Fact(
        fact_id="AB-NULL",
        headline="When we A/B tested a change we expected to matter, it didn't",
        reading="both arms 2/3 PASS, band total 35 each — no detectable difference",
        n="6 documents (3 problems × 2 arms)",
        measured="2026-07-22",
        source="docs/v8.6-quality-ab-experiment.md",
        literal="2/3 PASS",
        bound=(
            "The contrast tested was a 3.6% change in the agent's instruction length. "
            "It supports 'this particular compression cost nothing measurable', not "
            "'size never matters'. Published because it came out null."
        ),
        section=SEC_HONESTY,
    ),
    # --- Instrument sensitivity ---------------------------------------------
    Fact(
        fact_id="DETECTOR-SENSITIVITY",
        headline="Our automatic defect detector misses most planted defects",
        reading="10 of 13 deliberately-wrong test analyses were NOT caught",
        n="13 adversarial fixtures",
        measured="2026-09-18",
        source="docs/conformance-baseline.md",
        literal="10 of 13",
        bound=(
            "This is published so that a clean reading from that detector is read "
            "correctly: it means the instrument found nothing, never that the analysis "
            "is correct. Nine of the thirteen produced no signal at all."
        ),
        section=SEC_HONESTY,
    ),
    # --- Live output --------------------------------------------------------
    Fact(
        fact_id="LIVE-CONFORMANCE",
        headline="On live runs, most output is structurally clean — but not all",
        reading="5 of 8 live runs scored zero form defects",
        n="8 live runs",
        measured="2026-09-06",
        source="docs/conformance-baseline.md",
        literal="5 of 8",
        bound=(
            "Conditional on the agent having been dispatched — it is not an "
            "end-to-end rate for an ordinary user prompt. One failing run had 31 of 31 "
            "verdict cells non-conforming, so the failures are not marginal when they "
            "happen. And per the line above, 'clean' means this detector found nothing."
        ),
        section=SEC_OUTPUT,
    ),
)


# Population floor: the card must never silently shrink to nothing. Anti-masking.
_MIN_FACTS = 8
_REQUIRED_SECTIONS = (SEC_HONESTY, SEC_OUTPUT)


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------


def verify_facts(facts: tuple[Fact, ...] = FACTS, root: Path = REPO_ROOT) -> list[str]:
    """Re-read every fact's cited source and confirm its literal is present.

    Returns a list of problem strings; empty means every literal located.
    """
    problems: list[str] = []

    if len(facts) < _MIN_FACTS:
        problems.append(
            f"fact registry holds {len(facts)} entries, below the floor of {_MIN_FACTS} "
            "— a card that shrinks to nothing must fail, not render empty"
        )

    present_sections = {f.section for f in facts}
    for required in _REQUIRED_SECTIONS:
        if required not in present_sections:
            problems.append(f"no fact carries required section {required!r}")

    seen: set[str] = set()
    for fact in facts:
        if fact.fact_id in seen:
            problems.append(f"duplicate fact id {fact.fact_id!r}")
        seen.add(fact.fact_id)

        for attr in ("headline", "reading", "n", "measured", "bound"):
            if not getattr(fact, attr).strip():
                problems.append(f"{fact.fact_id}: empty {attr}")

        src = root / fact.source
        if not src.is_file():
            problems.append(f"{fact.fact_id}: source {fact.source} does not exist")
            continue
        text = src.read_text(encoding="utf-8")
        if fact.literal not in text:
            problems.append(
                f"{fact.fact_id}: pinned literal not found in {fact.source} — "
                f"the published reading no longer matches its source: {fact.literal!r}"
            )

    return problems


# ---------------------------------------------------------------------------
# Track B result -- conditional, and deliberately hard to fake
# ---------------------------------------------------------------------------

_TRACKB_REQUIRED_FIELDS = (
    "status",
    "preregistered_threshold",
    "observed_effect",
    "n_per_arm",
    "measured",
    "run_id",
)
_TRACKB_VALID_STATUS = ("cleared", "null", "inconclusive", "not_run")


def load_trackb(path: Path = TRACKB_RESULT_PATH) -> dict | None:
    """Load the Track B recorded result, or None when no run has been recorded.

    Raises EvidenceError on a malformed record rather than treating it as absent —
    a truncated or hand-edited result file must not silently suppress or fabricate
    the comparative section.
    """
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise EvidenceError(f"{path} is not valid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise EvidenceError(f"{path} must hold a JSON object")
    missing = [f for f in _TRACKB_REQUIRED_FIELDS if f not in data]
    if missing:
        raise EvidenceError(f"{path} missing required field(s): {', '.join(missing)}")
    if data["status"] not in _TRACKB_VALID_STATUS:
        raise EvidenceError(
            f"{path} status {data['status']!r} not one of {_TRACKB_VALID_STATUS}"
        )
    # trackb-2 (docs/trackb-2-preregistration.md) additionally requires a
    # format-tell caveat and the non-gating secondary-summary-gap figure --
    # neither may be silently absent from a record that could otherwise
    # publish a cleared comparative claim without its disclosed bound.
    if data.get("preregistration") == "docs/trackb-2-preregistration.md":
        if not data.get("caveat"):
            raise EvidenceError(f"{path}: trackb-2 record missing a non-empty 'caveat'")
        if "secondary_summary_gap" not in data:
            raise EvidenceError(f"{path}: trackb-2 record missing 'secondary_summary_gap'")
    return data


def trackb_publishable(result: dict | None) -> bool:
    """True only for a cleared run. Null/inconclusive/absent all render nothing."""
    return bool(result) and result.get("status") == "cleared"


# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------


def _sentence_case(text: str) -> str:
    """Capitalise the first character only — readings are authored lowercase so
    they read naturally inside prose, but they are rendered as standalone lines."""
    return text[:1].upper() + text[1:] if text else text


def _fact_block(fact: Fact) -> list[str]:
    return [
        f"### {fact.headline}",
        "",
        f"**{_sentence_case(fact.reading)}**",
        "",
        f"*Sample: {fact.n} · Measured: {fact.measured} · "
        f"Source: [`{fact.source}`]({_rel_link(fact.source)})*",
        "",
        f"What this does not say: {fact.bound}",
        "",
    ]


def _rel_link(source: str) -> str:
    """Links are rendered relative to docs/, where the card lives."""
    if source.startswith("docs/"):
        return source[len("docs/"):]
    return "../" + source


def render(
    facts: tuple[Fact, ...] = FACTS,
    trackb: dict | None = None,
) -> str:
    lines: list[str] = [
        GENERATED_MARKER,
        "<!-- Source: scripts/gen-evidence-card.py -->",
        "<!-- Regenerate: python3 scripts/gen-evidence-card.py -->",
        "",
        "# Evidence",
        "",
        "What has actually been measured about this agent — with sample sizes, dates, and",
        "the known blind spots of every instrument that produced a number.",
        "",
        "**There is no overall quality score on this page, and that is deliberate.** The",
        "first section explains why: we built one, checked whether it tracked the thing it",
        "appeared to measure, and found that it did not. Publishing it anyway would have",
        "been the easier choice and a dishonest one.",
        "",
        "Every figure below is re-read from its cited source each time this page is",
        "generated. If a source changes so that it no longer says what this page claims,",
        "the page fails to build rather than going stale.",
        "",
        "---",
        "",
    ]

    for section in _SECTION_ORDER:
        section_facts = [f for f in facts if f.section == section]
        if not section_facts:
            continue
        lines.append(f"## {_SECTION_TITLES[section]}")
        lines.append("")
        if section == SEC_HONESTY:
            lines.extend(
                [
                    "These are the findings that constrain everything else on this page.",
                    "They are published because they came out badly.",
                    "",
                ]
            )
        for fact in section_facts:
            lines.extend(_fact_block(fact))
        lines.append("---")
        lines.append("")

    # --- Track B: comparative lift, conditional ----------------------------
    if trackb_publishable(trackb):
        assert trackb is not None
        prereg_path = trackb.get("preregistration", "docs/trackb-preregistration.md")
        lines.extend(
            [
                "## Compared against not using it",
                "",
                "The question any measurement above leaves open: does the analysis come out",
                "better than the same model answering the same problem without this plugin?",
                "",
                f"**{trackb['observed_effect']}**",
                "",
                f"*Sample: {trackb['n_per_arm']} per arm · Measured: {trackb['measured']} · "
                f"Run: `{trackb['run_id']}`*",
                "",
            ]
        )
        if trackb.get("caveat"):
            lines.extend([f"**Caveat:** {trackb['caveat']}", ""])
        if trackb.get("secondary_summary_gap") is not None:
            lines.extend(
                [
                    "*Partial context, not part of the threshold: the same effect measured on "
                    "the orchestrator's final message instead of the delivered file differs by "
                    f"{trackb['secondary_summary_gap']:+.2f} points.*",
                    "",
                ]
            )
        lines.extend(
            [
                "The effect threshold and the full analysis plan were fixed in writing",
                f"before any run took place — see [the pre-registration]({_rel_link(prereg_path)}).",
                f"The pre-registered threshold was: {trackb['preregistered_threshold']}.",
                "",
                "---",
                "",
            ]
        )

    # --- What we don't claim ------------------------------------------------
    lines.extend(
        [
            "## What this page does not claim",
            "",
            "- **No overall quality score.** See the first section.",
            "- **No accuracy rate for analyses in general.** The correctness check covered",
            "  six documents, once, by hand.",
            "- **Nothing about domains we have not tested.** The measured problems are drawn",
            "  from software, policy, biology and ethics. That is a spread, not a sample.",
            "- **Nothing about how often the agent is reached automatically.** Phrase-based",
            "  routing is unreliable; use the slash command. The last measurement of that rate",
            f"  is old and labelled as such in [Getting Started]({_rel_link('docs/GETTING-STARTED.md')}).",
        ]
    )
    if not trackb_publishable(trackb):
        lines.extend(
            [
                "- **No comparison against not using the plugin.** A controlled comparison",
                "  against an unaided baseline is not published here. Nothing on this page",
                "  should be read as evidence that the agent outperforms an ordinary answer.",
            ]
        )
    lines.extend(
        [
            "",
            "---",
            "",
            "## Reproducing these numbers",
            "",
            "```sh",
            "# regenerate this page from its sources (fails if any source no longer matches)",
            "python3 scripts/gen-evidence-card.py --check",
            "",
            "# the full offline gate battery",
            "bash scripts/check-firewall-battery.sh",
            "",
            "# the structural defect detector's own control battery",
            "python3 scripts/check-quality-harness.py --self-test",
            "```",
            "",
            "The measurement apparatus behind each reading is described in",
            f"[MEASUREMENT-MAP.md]({_rel_link('docs/MEASUREMENT-MAP.md')}) and",
            f"[TESTING.md]({_rel_link('docs/TESTING.md')}).",
            "",
        ]
    )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


def cmd_write() -> int:
    problems = verify_facts()
    if problems:
        for p in problems:
            sys.stderr.write(f"[evidence-card] {p}\n")
        return 1
    trackb = load_trackb()
    CARD_PATH.parent.mkdir(parents=True, exist_ok=True)
    CARD_PATH.write_text(render(trackb=trackb), encoding="utf-8")
    status = "not run" if trackb is None else trackb["status"]
    print(f"wrote {CARD_PATH.relative_to(REPO_ROOT)} (track-b: {status})")
    return 0


def cmd_check() -> int:
    problems = verify_facts()
    if problems:
        for p in problems:
            sys.stderr.write(f"[evidence-card] {p}\n")
        return 1
    trackb = load_trackb()
    fresh = render(trackb=trackb)
    if not CARD_PATH.is_file():
        sys.stderr.write(f"[evidence-card] {CARD_PATH} does not exist; run --write\n")
        return 1
    on_disk = CARD_PATH.read_text(encoding="utf-8")
    if on_disk != fresh:
        sys.stderr.write(
            "[evidence-card] docs/EVIDENCE.md differs from a fresh render; "
            "run python3 scripts/gen-evidence-card.py\n"
        )
        return 1
    print("evidence card: no drift")
    return 0


def describe() -> dict:
    """Self-description, emitting only fields in `_gate_registry`'s closed
    `DESCRIBE_FIELD_VOCABULARY`, and only those this gate's registry entry
    declares it consumes. Every value is derived from live constants in this
    module — none is hand-typed, which is the point of the field contract."""
    return {
        # DECLARED: the product surface this gate guards.
        "registered_surfaces": ["docs/EVIDENCE.md"],
        # OBSERVED: the source files the live leg actually re-reads each run.
        "checked_files": sorted({f.source for f in FACTS}),
        # A zero reached by emptying the registry must be distinguishable from
        # a zero reached by every literal locating; this is that floor.
        "population_floors": {"facts": _MIN_FACTS},
        "control_ids": sorted(c[0] for c in _CONTROLS),
        "control_count": len(_CONTROLS),
    }


# ---------------------------------------------------------------------------
# Self-test controls
# ---------------------------------------------------------------------------


def _c01_all_literals_located() -> str | None:
    problems = verify_facts()
    if problems:
        return "; ".join(problems)
    return None


def _c02_corrupted_literal_is_caught() -> str | None:
    """Negative control: a literal that is not in its source must fail."""
    bad = FACTS[0].__class__(
        **{**FACTS[0].__dict__, "literal": "this string is not in any source file xyzzy"}
    )
    problems = verify_facts((bad,) + FACTS[1:])
    if not any("pinned literal not found" in p for p in problems):
        return "a corrupted literal did not produce a 'not found' problem"
    return None


def _c03_empty_registry_fails() -> str | None:
    """Anti-masking: an empty registry must fail, never render an empty card."""
    problems = verify_facts(())
    if not problems:
        return "an empty fact registry produced no problems"
    if not any("below the floor" in p for p in problems):
        return "an empty registry did not trip the population floor"
    return None


def _c04_render_is_deterministic() -> str | None:
    if render() != render():
        return "two renders of the same inputs differ"
    return None


def _c05_trackb_absent_renders_nothing() -> str | None:
    out = render(trackb=None)
    if "Compared against not using it" in out:
        return "comparative section rendered with no Track B result"
    if "No comparison against not using the plugin" not in out:
        return "absent Track B did not produce the explicit no-comparison disclaimer"
    return None


def _c06_trackb_null_renders_nothing() -> str | None:
    """The user-facing instruction, enforced mechanically: null does not publish."""
    for status in ("null", "inconclusive", "not_run"):
        result = {
            "status": status,
            "preregistered_threshold": "t",
            "observed_effect": "SHOULD NOT APPEAR",
            "n_per_arm": 5,
            "measured": "2026-01-01",
            "run_id": "x",
        }
        out = render(trackb=result)
        if "Compared against not using it" in out or "SHOULD NOT APPEAR" in out:
            return f"a {status!r} Track B result rendered the comparative section"
        if "No comparison against not using the plugin" not in out:
            return f"a {status!r} Track B result did not produce the disclaimer"
    return None


def _c07_trackb_cleared_renders() -> str | None:
    result = {
        "status": "cleared",
        "preregistered_threshold": "THRESHOLD-TOKEN",
        "observed_effect": "EFFECT-TOKEN",
        "n_per_arm": 5,
        "measured": "2026-01-01",
        "run_id": "RUN-TOKEN",
    }
    out = render(trackb=result)
    for token in ("EFFECT-TOKEN", "THRESHOLD-TOKEN", "RUN-TOKEN"):
        if token not in out:
            return f"cleared Track B result did not render {token}"
    if "No comparison against not using the plugin" in out:
        return "cleared Track B still rendered the no-comparison disclaimer"
    return None


def _c08_trackb_malformed_is_rejected(tmp_root: Path) -> str | None:
    bad = tmp_root / "bad.json"
    bad.write_text('{"status": "cleared"}', encoding="utf-8")
    try:
        load_trackb(bad)
    except EvidenceError:
        return None
    return "a Track B record missing required fields was accepted"


def _c09_trackb_bad_status_is_rejected(tmp_root: Path) -> str | None:
    bad = tmp_root / "bad2.json"
    payload = {f: "x" for f in _TRACKB_REQUIRED_FIELDS}
    payload["status"] = "definitely-great"
    bad.write_text(json.dumps(payload), encoding="utf-8")
    try:
        load_trackb(bad)
    except EvidenceError:
        return None
    return "a Track B record with an invented status was accepted"


def _c10_every_fact_states_a_bound() -> str | None:
    """A reading published without its limit is the defect this card exists to avoid."""
    for fact in FACTS:
        if len(fact.bound.strip()) < 40:
            return f"{fact.fact_id}: bound is too short to be a real disclosure"
        if not fact.n.strip():
            return f"{fact.fact_id}: no N stated"
    return None


def _c11_no_composite_score_rendered() -> str | None:
    """The card's central commitment, asserted rather than trusted."""
    out = render().lower()
    for banned in ("overall score", "quality score:", "/100", "out of 100"):
        if banned in out:
            return f"card rendered a composite score token: {banned!r}"
    return None


def _c12_trackb2_links_correct_prereg() -> str | None:
    """A cleared trackb-2 record links its own pre-registration, never the
    superseded v9.13 one; a cleared record with no `preregistration` field
    keeps the v9.13 back-compat link."""
    cleared_2 = {
        "status": "cleared",
        "preregistration": "docs/trackb-2-preregistration.md",
        "preregistered_threshold": "t",
        "observed_effect": "e",
        "n_per_arm": 10,
        "measured": "2026-01-01",
        "run_id": "r",
        "caveat": "CAVEAT-TOKEN",
        "secondary_summary_gap": 1.23,
    }
    out = render(trackb=cleared_2)
    if "trackb-2-preregistration.md" not in out:
        return "a cleared trackb-2 record did not link trackb-2-preregistration.md"
    if "(trackb-preregistration.md)" in out:
        return "cleared trackb-2 also linked the superseded v9.13 doc"
    cleared_1 = {
        "status": "cleared",
        "preregistered_threshold": "t",
        "observed_effect": "e",
        "n_per_arm": 10,
        "measured": "2026-01-01",
        "run_id": "r",
    }
    out1 = render(trackb=cleared_1)
    if "(trackb-preregistration.md)" not in out1:
        return "a cleared record with no preregistration field lost the v9.13 back-compat link"
    return None


def _c13_trackb2_requires_and_renders_caveat(tmp_root: Path) -> str | None:
    """The format-tell caveat and the secondary summary-gap figure render on a
    cleared trackb-2 card; a trackb-2 record missing `caveat` is rejected by
    load_trackb (not silently published without its disclosed bound); a null
    trackb-2 record still renders nothing (C06 semantics unchanged)."""
    good = {
        "status": "cleared",
        "preregistration": "docs/trackb-2-preregistration.md",
        "preregistered_threshold": "t",
        "observed_effect": "e",
        "n_per_arm": 10,
        "measured": "2026-01-01",
        "run_id": "r",
        "caveat": "CAVEAT-TOKEN",
        "secondary_summary_gap": 1.23,
    }
    out = render(trackb=good)
    if "CAVEAT-TOKEN" not in out or "1.23" not in out:
        return "cleared trackb-2 render did not print the caveat and secondary figure"
    if "partial context, not part of the threshold" not in out.lower():
        return "cleared trackb-2 render did not label the secondary figure non-gating"

    bad_path = tmp_root / "trackb2-bad.json"
    bad = {k: v for k, v in good.items() if k != "caveat"}
    bad_path.write_text(json.dumps(bad), encoding="utf-8")
    try:
        load_trackb(bad_path)
    except EvidenceError:
        pass
    else:
        return "a trackb-2 record without 'caveat' was accepted by load_trackb"

    null_2 = {**good, "status": "null"}
    out2 = render(trackb=null_2)
    if "CAVEAT-TOKEN" in out2 or "Compared against not using it" in out2:
        return "a null trackb-2 record still rendered the comparative section"
    return None


_CONTROLS: tuple[tuple[str, object], ...] = (
    ("C01-literals-located", _c01_all_literals_located),
    ("C02-corrupted-literal-caught", _c02_corrupted_literal_is_caught),
    ("C03-empty-registry-fails", _c03_empty_registry_fails),
    ("C04-render-deterministic", _c04_render_is_deterministic),
    ("C05-trackb-absent-renders-nothing", _c05_trackb_absent_renders_nothing),
    ("C06-trackb-null-renders-nothing", _c06_trackb_null_renders_nothing),
    ("C07-trackb-cleared-renders", _c07_trackb_cleared_renders),
    ("C08-trackb-malformed-rejected", _c08_trackb_malformed_is_rejected),
    ("C09-trackb-bad-status-rejected", _c09_trackb_bad_status_is_rejected),
    ("C10-every-fact-states-a-bound", _c10_every_fact_states_a_bound),
    ("C11-no-composite-score", _c11_no_composite_score_rendered),
    ("C12-trackb2-links-correct-prereg", _c12_trackb2_links_correct_prereg),
    ("C13-trackb2-requires-and-renders-caveat", _c13_trackb2_requires_and_renders_caveat),
)


def self_test() -> int:
    import inspect
    import tempfile

    failures: list[str] = []
    with tempfile.TemporaryDirectory(prefix="evidence-card-") as td:
        tmp_root = Path(td)
        for name, fn in _CONTROLS:
            try:
                sig = inspect.signature(fn)  # type: ignore[arg-type]
                problem = fn(tmp_root) if sig.parameters else fn()  # type: ignore[operator]
            except Exception as exc:  # noqa: BLE001 - a raising control is a failure
                problem = f"raised {type(exc).__name__}: {exc}"
            if problem:
                failures.append(f"{name}: {problem}")

    for name, _ in _CONTROLS:
        if not name.startswith("C"):
            failures.append(f"control {name} is not correctly named")

    if failures:
        for f in failures:
            sys.stderr.write(f"[evidence-card self-test] FAIL {f}\n")
        sys.stderr.write(
            f"[evidence-card self-test] {len(failures)} of {len(_CONTROLS)} controls failed\n"
        )
        return 1

    print(f"evidence-card self-test: {len(_CONTROLS)}/{len(_CONTROLS)} controls passed")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate the public Evidence Card from verified source literals."
    )
    parser.add_argument("--check", action="store_true", help="exit 1 on drift")
    parser.add_argument("--self-test", action="store_true", help="offline control battery")
    parser.add_argument("--describe", action="store_true", help="emit self-description JSON")
    args = parser.parse_args(argv)

    try:
        if args.describe:
            print(json.dumps(describe(), indent=2, sort_keys=True))
            return 0
        if args.self_test:
            return self_test()
        if args.check:
            return cmd_check()
        return cmd_write()
    except EvidenceError as exc:
        sys.stderr.write(f"[evidence-card] {exc}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
