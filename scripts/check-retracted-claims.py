#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""RETRACT-01 — a retracted claim may never reappear on a published surface.

WHY THIS GATE EXISTS
--------------------
Milestone v9.7.0 shipped seven blocking product defects. Every one was caught
by code review, and every one was caught AFTER some verification step had
passed the same area. Two of the seven were the *same claim shipping twice*:

  * 55-CR-01 retracted "each companion technique is owned by exactly one
    phase ... bounded at <= 8 lines" (two techniques are invoked at two
    phases each). The body and the payment record were corrected.
  * 58-CR-01 found that identical retracted premise shipping, three phases
    later, in `docs/requirements-matrix.md` — because the REQUIREMENTS.md
    statement the matrix row is generated from was never updated alongside
    the fix.

The defect class this gate closes is therefore narrow and specific: a claim
found false in one place, left standing in another. It is NOT a general
truth-checker, and the disclosed bound below says so.

WHAT IT DOES AND DOES NOT ASSERT
--------------------------------
Asserts: none of the registered retracted literals appears on a published
surface, except at the exact counts an entry's exemption list allows.

Does NOT assert: that any *other* claim is true; that a reworded restatement
of a retracted claim is caught (the register is literal, not semantic); or
that the registry is complete. A retracted claim nobody adds here is
invisible to this gate. Registry growth is a human act performed when a
review retracts a claim.

Matching is whitespace-normalised AND blockquote-continuation-normalised
outside fenced code blocks, so neither ordinary Markdown line-wrapping nor a
literal wrapped across a `>` blockquote line break can hide a reappearance
(AP-01, widened by BQ-01 / Phase 59). It was not always: the review that
found the whitespace gap demonstrated the literal "no new registered gate
asserts" sitting in CHANGELOG.md with a substring count of zero, wrapped
across a newline — this gate's pass on that entry had been luck rather than
correctness. A later audit found the same defect class surviving in a
blockquote-wrapped variant; Phase 59 closed it. Normalisation does not defeat
rewording, and nothing here does; that residual is the literal-not-semantic
bound stated above, not a second one.

THE EXEMPTION MECHANISM, AND WHY IT IS TWO-SIDED
------------------------------------------------
A retracted claim legitimately appears inside its own erratum — CHANGELOG.md's
disclosure table names "no phase owns" precisely to record that it was false.
An exemption is (path, exact_count), and it fires in BOTH directions:

  * above the count -> a new, unexempted occurrence crept in;
  * below the count -> the erratum itself was deleted, so the disclosure
    that justified the exemption no longer exists.

The second direction is the one a simple allowlist would miss.

Usage:
    python3 scripts/check-retracted-claims.py              # live scan
    python3 scripts/check-retracted-claims.py --self-test  # falsifiability controls
    python3 scripts/check-retracted-claims.py --describe   # CONF-SURFACE self-description

Exit codes:
    0  no retracted claim present off-exemption (or all self-test controls behaved)
    1  a retracted claim is present, or a control failed

    (No exit 2: argparse exits 2 itself on a usage error, and this gate has no
    external prerequisite that could be unmet — unlike VAL-03's pytest leg,
    whose absence the battery reports as BLOCKED. Stating a 2 this module never
    returns would be a small false claim in a gate against false claims.)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# Published surfaces. `.planning/` is deliberately absent: it is gitignored,
# archived at milestone close, and is where the *reasoning about* a retracted
# claim legitimately lives at length.
SCAN_GLOBS: tuple[str, ...] = (
    "CLAUDE.md",
    "README.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "docs/**/*.md",
    "docs/data/*.json",
    "shared/**/*.md",
    "first-principles/**/*.md",
    "scripts/*.py",
)


@dataclass(frozen=True)
class RetractedClaim:
    """One claim a review found false, and the literal that identifies it."""

    literal: str
    retracted_by: str
    corrected: str
    # (repo-relative path, exact number of occurrences permitted there)
    exemptions: tuple[tuple[str, int], ...] = field(default_factory=tuple)


# ---------------------------------------------------------------------------
# THE REGISTRY
#
# One entry per claim a code review retracted. Add an entry when a review
# finds a claim false; never delete one, because the whole point is that the
# claim stays barred after the immediate fix is forgotten.
# ---------------------------------------------------------------------------
REGISTRY: tuple[RetractedClaim, ...] = (
    RetractedClaim(
        literal="feeding only a MEDIUM- or LOW-confidence chain",
        retracted_by="999.164",
        corrected=(
            "The Phase 3 read population is the load-bearing chains, never the "
            "HIGH-confidence ones. Conditioning the read on the chain's "
            "confidence closes a loop: an unopened citation takes the `?` "
            "(provenance table), the `?` caps its chain below HIGH (D-07), and "
            "the capped chain then excuses the read. 'Open nothing' is a "
            "fixpoint of that rule and satisfies every clause of it. Measured "
            "matched-pair at N=5 per arm, 2026-09-24: external calls per run "
            "0,0,6,1,6 before and 14,4,3,10,14 after, zero-runs 2/5 -> 0/5."
        ),
        # Registered because this population has now grown a circularity TWICE
        # by two different routes. The first (the suffix deciding the read) was
        # closed at plan 01-03 by `_B5B_INCLUSIVE`, whose guard comment warns
        # that without it "the circularity returns" — and it returned anyway,
        # through the confidence label the suffix determines. A literal bar is
        # the only thing that makes a third return visible at commit time.
        # No exemption: the retraction is recorded in `.planning/ROADMAP.md`,
        # which is gitignored and therefore outside this gate's scanned
        # surfaces. A CHANGELOG entry quoting it will need one.
    ),
    RetractedClaim(
        literal="owned by exactly one phase",
        retracted_by="55-CR-01",
        corrected=(
            "Eight techniques carry ten invocation sites: theoretical-limit at "
            "Phases 1 and 4, inversion at Phases 2 and 5. The decline record is "
            "bounded at <= 10 lines per full-composer run, not <= 8."
        ),
        # CHANGELOG.md's v9.8.0 entry quotes the literal once, in the paragraph
        # explaining the defect class this gate exists to close.
        exemptions=(("CHANGELOG.md", 1),),
    ),
    RetractedClaim(
        literal="considered once, at the phase that owns it",
        retracted_by="55-CR-01",
        corrected=(
            "Apply each technique where a phase invokes it and its trigger fires; "
            "two techniques are invoked at two phases."
        ),
    ),
    RetractedClaim(
        literal="no phase owns",
        retracted_by="57-CR-01",
        corrected=(
            "Phase 5's named artifact IS the complete output document. Report is "
            "the emission of it, not an unowned accumulation."
        ),
        # Legitimate quotations of the retracted literal, each inside prose
        # whose subject IS the retraction:
        #   CHANGELOG.md  - the v9.7.0 disclosure table names the defect (1),
        #                   its narrative explains the false grep assertion
        #                   built on it (1), and the v9.8.0 entry cites the
        #                   same assertion as the worked example of a criterion
        #                   that pinned a claim which was itself false (1).
        #   CLAUDE.md     - the "Claims and falsifiers" rule cites it as the
        #                   worked example of an assertion that pinned a
        #                   claim which was itself false (1).
        # Both are two-sided: deleting the erratum fires this gate just as a
        # new unexempted occurrence does.
        exemptions=(("CHANGELOG.md", 3), ("CLAUDE.md", 1)),
    ),
    RetractedClaim(
        literal="no new registered gate asserts",
        retracted_by="58-CR-02",
        corrected=(
            "TERM-03 is reproducible: SCAN-GUARD's Body-15 asserts the Report "
            "emission invariant sentence against the live shipped agent body, in "
            "CI and in the battery. The coverage was inherited, not built."
        ),
        # CHANGELOG.md's v9.7.0 "Costs this release does not pay" bullet quotes
        # its own superseded wording ("As published, it read ...") as the
        # erratum recording 58-CR-02. Invisible to the gate until AP-01's
        # whitespace normalisation landed, because the paragraph wraps the
        # literal across a newline — the review's demonstration that the pass
        # on this entry had been luck rather than correctness.
        exemptions=(("CHANGELOG.md", 2),),
    ),
    # ---------------------------------------------------------------------
    # The four below were retracted by the 2026-09-23 documentation drift
    # audit rather than by a phase code review. RULE-01 clause 4 is written
    # for a review, but the property it protects is the same one: a claim
    # found false has copies, and correcting the instance leaves them. Each
    # literal below was measured against the live tree before registration --
    # the long forms were chosen precisely BECAUSE the short ones collide with
    # docs/conformance-baseline.md and docs/data/conformance.json, which
    # legitimately RECORD these sites as detected count-literals. Registering
    # a short form would have required exemptions against generated artifacts
    # whose counts move on every re-measure.
    # ---------------------------------------------------------------------
    RetractedClaim(
        literal="is produced by `HEADLINE-LOCK`'s sweep rather than a hand edit",
        retracted_by="DRIFT-2026-09-23",
        corrected=(
            "No such sweep exists. HEADLINE-LOCK is assertion-only: it has no "
            "write path, and check-traceability.py writes only "
            "requirements-matrix.md and matrix.json, via `emit`. A "
            "coverage-headline move is a hand edit that HEADLINE-LOCK then "
            "CHECKS. Believing otherwise licensed the v9.8.0 find-and-replace "
            "that corrupted headline-history row 26, because the previous "
            "headline literal is by construction what the last row's `to`-cell "
            "holds."
        ),
        # The one exempted occurrence is docs/requirements-traceability.md's
        # verbatim quotation of v8.26 ROADMAP's Phase 16 success criterion,
        # which must stay byte-intact: it is the record of what that milestone
        # required, not this tree's own assertion.
        #
        # DISCLOSED BOUND: the same file states the claim a SECOND time, in the
        # 2026-09-04 discharge note, where it is wrapped across two blockquote
        # lines. The gate cannot see it. `_normalise` collapses whitespace but
        # not the `>` continuation marker, so the normalised text reads
        # "...rather than a > hand edit". That is AP-01's defect class
        # surviving in a variant form, found by this audit and recorded here
        # rather than silently absorbed. If the normaliser is ever taught to
        # strip blockquote markers, this count becomes 2 and the gate will fire
        # -- which is the correct prompt to re-read both sites, not a
        # regression.
        #
        # CORRECTION, dated 2026-09-23 (Phase 59): the mechanism above was real
        # and is now closed -- `_normalise` strips line-leading blockquote
        # markers outside fences (BQ-01) -- but the worked example was wrong.
        # The second site (the 2026-09-04 discharge note) reads "), produced
        # by", not "is produced by": it is missing the registered literal's
        # leading "is ", so it is a paraphrase that the literal-not-semantic
        # bound correctly does not match, with or without the fix. A third
        # nearby paraphrase, in the 2026-09-23 correction block, says "the
        # sweep" rather than "`HEADLINE-LOCK`'s sweep" and is likewise not the
        # registered literal. The exemption below therefore STAYS 1; the
        # prediction that it would become 2 is retracted. Established two
        # ways: simulated against the live tree at plan time, and re-verified
        # by hand with `cat -A`.
        exemptions=(("docs/requirements-traceability.md", 1),),
    ),
    RetractedClaim(
        literal="Canonical baseline: `tests/step0-baseline-v7.8.md`",
        retracted_by="DRIFT-2026-09-23",
        corrected=(
            "The canonical Step 0 baseline is tests/step0-baseline-v8.5.md -- "
            "the version _BASELINE_VERSION in check-step0-live.py pins, the "
            "label the harness emits, and the file docs/gates/STEP0-06.md "
            "lists among its checked_files. v7.8 is the last FULL-RUN baseline "
            "(30 invocations, 6 prompts x 5) and the generation the RR-* "
            "residual sentinels cite; v8.5 is later but narrower."
        ),
        # Zero occurrences at registration: CLAUDE.md's two sites were both
        # corrected in 53c316e, and the replacement prose names v7.8 only in
        # its own distinct "is not a prior in the ordinary sense" sentence.
    ),
    RetractedClaim(
        literal="Two gates fire on `git commit`: the **sync-drift gate**",
        retracted_by="DRIFT-2026-09-23",
        corrected=(
            "Five gates fire on `git commit`, in order: sync-drift, the "
            "conformance generator self-test, the conformance-baseline drift "
            "gate, the claim-surface generator self-test, and the claim-surface "
            "drift gate. Both hook mechanisms run the same five."
        ),
        # Zero occurrences at registration. The bare phrase "Two gates fire on "
        # `git commit`" is deliberately NOT the registered literal: it appears
        # 6 times across docs/conformance-baseline.md and
        # docs/data/conformance.json, which record this site as a detected
        # count-literal. Those are measurements OF the defect, and their counts
        # move whenever the corpus is re-measured.
    ),
    RetractedClaim(
        literal="How to run every CI gate and the two pre-commit gates",
        retracted_by="DRIFT-2026-09-23",
        corrected=(
            "docs/TESTING.md documents every CI gate and all FIVE pre-commit "
            "gates. docs/ONBOARDING.md's index row said two."
        ),
        # Zero occurrences at registration. Same reasoning as the entry above:
        # the bare "the two pre-commit gates" appears 13 times across the
        # conformance artifacts and gen-gate-docs.py as recorded detections.
    ),
    RetractedClaim(
        literal="Carry-forward — expected FAIL (RR-95-02)",
        retracted_by="DRIFT-2026-09-23",
        corrected=(
            "S-P05's chain terminated at RR-108-02 CLOSED at 4/5 (Phase 114, "
            "v7.6 re-baseline), close sustained at 5/5 (Phase 129, v7.11 "
            "re-baseline). RR-108-02 is retained only as a regression guard; "
            "no successor id was minted. The cell did not merely name a stale "
            "id -- it instructed an operator to excuse a FAIL on a prompt "
            "whose last live reading was a clean sweep, which masks a "
            "regression rather than reporting one."
        ),
        # Measured before registration: 1 occurrence (docs/live-monitoring-
        # runbook.md, the site backlog 999.158 corrects), 0 after. No
        # collision with docs/conformance-baseline.md or docs/data/
        # conformance.json. The bare id RR-95-02 occurs widely in legitimate
        # chain strings across several scanned surfaces, so the long form
        # (this exact cell text) was chosen over the bare id to avoid
        # needing exemptions against those chain-string occurrences.
        exemptions=(),
    ),
    RetractedClaim(
        literal="Carry-forward — expected FAIL (RR-95-01)",
        retracted_by="DRIFT-2026-09-23",
        corrected=(
            "S-P02 genuinely is a live carry-forward, so the row's conclusion "
            "was right; what was false is the id. The current id is "
            "RR-114-01 (chain RR-79-02 -> RR-92-01 -> RR-95-01 -> RR-108-01 "
            "-> RR-114-01), [v8.0 ACCEPTED-FINAL]. Naming a retired id as the "
            "current tracking id is a false claim, not merely a stale one -- "
            "a wrong residual id reads as authoritative in a way a stale one "
            "does not (999.158's own filing note)."
        ),
        # Measured before registration: 1 occurrence (docs/live-monitoring-
        # runbook.md, the site backlog 999.158 corrects), 0 after. No
        # collision with the conformance artifacts, for the same reason as
        # the entry above.
        #
        # DISCLOSED BOUND: this is the weaker of the pair, registered because
        # the id is false rather than because the row's conclusion is false.
        # It bars only this exact cell form -- a reworded restatement of the
        # same error (e.g. a table naming RR-95-01 in different phrasing)
        # stays invisible, as the register is literal and always was.
        exemptions=(),
    ),
    # ---------------------------------------------------------------------
    # The three below were retracted by quick task 260924-swp (2026-09-24),
    # closing 999.129 RF-01/RF-02 and 999.128. One root: Phase 46's CR-02
    # rescope made GT-1's per-stage split explicitly unmeasured, and the
    # sentences written before that rescope kept speaking as though the
    # split were known. All three read 0 across the scanned surfaces at
    # registration, measured with this module's own `_normalise` and
    # `_iter_scan_files` rather than a bare grep, so none carries an
    # exemption. `.planning/ROADMAP.md` quotes all three at length and is
    # outside SCAN_GLOBS by design; a CHANGELOG entry quoting one will need
    # an exemption.
    # ---------------------------------------------------------------------
    RetractedClaim(
        literal="largest but unmeasured",
        retracted_by="999.129 RF-01",
        corrected=(
            "GT-1 states 'the per-stage split is not measured', so no sentence "
            "may rank the stages. Test execution is EXPECTED to be the largest "
            "stage for a codebase of this profile; the expectation is stated as "
            "an expectation, and profiling is what would confirm it. The "
            "ranking is not lost, only its epistemic status corrected."
        ),
        exemptions=(),
    ),
    RetractedClaim(
        literal="the test suite is the largest unmeasured share",
        retracted_by="999.129 RF-01",
        corrected=(
            "Same retraction as the entry above, in the wording chain C1's "
            "first hop used instead. Registered SEPARATELY because this is the "
            "form that already escaped once: the 2026-09-24 backlog sweep "
            "re-verified RF-01 by grepping the literal 'largest but "
            "unmeasured', found 2 of the 3 filed sites, and recorded RF-01's "
            "3-site list as stale -- while this third site sat in the same "
            "file asserting the same ranking in the same clause that declares "
            "it unmeasured. The executing task's co-occurrence falsifier "
            "(a ranking word within 40 characters of 'unmeasured') found all "
            "three. That is 58-CR-01's shape exactly: a retracted claim "
            "surviving in a paraphrase because only the registered wording was "
            "searched for."
        ),
        exemptions=(),
    ),
    RetractedClaim(
        literal="test suite runtime (GT-1) is usually the dominant stage",
        retracted_by="999.129 RF-02",
        corrected=(
            "The hedge on this sentence ('profiling confirms or refutes this') "
            "was always correct; the CITATION was the defect. GT-1 measures "
            "the 45-minute pipeline total and explicitly declines the "
            "per-stage split, so it cannot be the source of a claim about "
            "which stage dominates. The dominance claim now names itself an "
            "expectation and says GT-1 does not measure it."
        ),
        # DISCLOSED BOUND: this literal bars the GT-1-attributed form only. An
        # unattributed dominance claim ("test suite runtime is usually the
        # dominant stage") is the CORRECTED text and must stay legal, so the
        # literal necessarily includes the "(GT-1)" that made it false. A
        # future miscitation through a different ground truth -- "(GT-3) is
        # usually the dominant stage" -- is a different literal and is
        # invisible to this entry.
        exemptions=(),
    ),
    # ---------------------------------------------------------------------
    # The four below were retracted by quick task 260924-crn (2026-09-24),
    # closing 999.166 against the adjudication that found the Carnot worked
    # example's reservoir pair wrong on three independent grounds. One root:
    # the drill took the molten-salt COLD TANK (563 K) as the power cycle's
    # cold reservoir. It is not -- the salt loop is the heat SOURCE and
    # returns at 290 C, while the steam cycle rejects to a condenser at
    # near-ambient temperature, so nothing in the plant rejects heat at
    # 290 C. Every figure below followed from that one substitution. All four
    # read 0 across the scanned surfaces at registration, measured with this
    # module's own `_normalise` and `_iter_scan_files` rather than a bare
    # grep, so none carries an exemption. `.planning/` quotes all four at
    # length and is outside SCAN_GLOBS by design; a CHANGELOG entry quoting
    # one will need an exemption.
    #
    # DELIBERATELY NOT REGISTERED: "The Second Law imposes this ceiling
    # absolutely." The sentence is not false on its own -- the Second Law does
    # impose ceilings absolutely. What was false was its CO-OCCURRENCE with
    # ~33%, and a literal register cannot express a co-occurrence. Barring a
    # sentence that is true in isolation would make this gate assert something
    # it cannot support. The first entry below bars the number the sentence was
    # attached to, which is the part that was false.
    # ---------------------------------------------------------------------
    RetractedClaim(
        literal="Law-permitted ceiling: ~33%",
        retracted_by="999.166",
        corrected=(
            "The law-permitted ceiling for this cycle is ~61-62% -- 62.3% "
            "wet-cooled (1 - 316/838) and 60.6% air-cooled (1 - 330/838), the "
            "condenser being the cycle's actual cold reservoir. 32.8% is the "
            "Carnot bound between the two SALT TANK temperatures, which is not "
            "a reservoir pair any heat engine in the plant operates across. "
            "The decisive test needs no physics: current 565 C subcritical "
            "molten-salt tower technology is DESIGNED for 43.0% wet-cooled and "
            "41.2% air-cooled thermal-to-electric (Sandia, OSTI 1035342 Table "
            "2; NREL ATB, OSTI 1820100), so a claimed absolute Second-Law "
            "ceiling of ~33% on the same quantity is exceeded by the "
            "equipment's own design point."
        ),
        exemptions=(),
    ),
    RetractedClaim(
        literal="**Irreducible fraction:** zero",
        retracted_by="999.166",
        corrected=(
            "Most of the gap is irreducible, not none of it. Carnot's bound is "
            "the efficiency of a REVERSIBLE cycle, and reversible heat transfer "
            "requires either infinite exchanger area or infinite time; a machine "
            "delivering finite power through finite hardware destroys exergy at "
            "every heat exchange and cannot approach the ceiling however good "
            "the equipment gets. The original sentence conceded exactly this in "
            "its own parenthesis ('though never reaching it in finite time for a "
            "finite-power machine') and then set the irreducible share to zero "
            "anyway."
        ),
        exemptions=(),
    ),
    RetractedClaim(
        literal=(
            "The conventional 20–25% Rankine efficiency is engineering "
            "headroom, not a physical ceiling"
        ),
        retracted_by="999.166",
        corrected=(
            "20-25% is not a Rankine cycle efficiency. It is the band that "
            "WHOLE-PLANT annual solar-to-electric efficiency is quoted in -- "
            "after heliostat cosine, soiling and receiver losses, and then the "
            "power block. Solar Two's own test report separates the two: power "
            "block 34% measured / 42% predicted, whole plant 13% measured / 22% "
            "predicted (OSTI 793226, Table 6-1). Bracketing a power-block "
            "Carnot ceiling against a whole-plant figure attributes optical and "
            "receiver loss to the turbine."
        ),
        exemptions=(),
    ),
    RetractedClaim(
        literal="the conventional figure is anchored in published turbine operating data",
        retracted_by="999.166",
        corrected=(
            "It was anchored in nothing of the kind. The figure it justified "
            "(20-25%) is a whole-plant annual solar-to-electric band, so no "
            "turbine operating data could have produced it. A confidence line "
            "may name only supports that exist; this one named a provenance "
            "that never held. The replacement figures are anchored in published "
            "design characterizations (OSTI 1035342, 1088078, 1820100) and one "
            "published measurement (OSTI 793226), each cited at the ground "
            "truth that carries it."
        ),
        exemptions=(),
    ),
    RetractedClaim(
        literal="higher-value build is ruled out by the §5 dead end",
        retracted_by="999.156",
        corrected=(
            "The §5 dead end rules out one ARGUMENT for the Slack candidate "
            "being the higher-value build — stated preference read off an "
            "aggregated count that conflates three response surfaces with "
            "different selection biases — not that conclusion. C3 exists "
            "precisely to keep the value comparison open, and its own "
            "conclusion is that the recommendation flips if the Slack-side "
            "evidence picture changes materially. A dead end that had "
            "disposed of the conclusion would make C3 vacuous."
        ),
        # Scoped deliberately narrow, and the narrowness is the point. The
        # bare phrase "the Slack integration is the higher-value build" is
        # LEGITIMATE prose — §5 names it as the claim the dead end examined —
        # so barring that would bar correct text. Measured 2026-09-24 under
        # this module's own `_normalise`, over its own SCAN_GLOBS: the bare
        # phrase has 2 off-registry occurrences (shared/examples/product-
        # business-2.md and its generated twin), this literal has 0. What is
        # barred is the CONJUNCTION — the value conclusion asserted as ruled
        # out by §5 — never either half alone.
        # No exemption: the retraction is recorded in `.planning/ROADMAP.md`,
        # which is gitignored and therefore outside this gate's scanned
        # surfaces. A CHANGELOG entry quoting it will need one.
        exemptions=(),
    ),
    RetractedClaim(
        literal="Nothing can exceed it",
        retracted_by="999.171",
        corrected=(
            "The bound theoretical-limit derives is a ceiling only when higher "
            "is better and a floor when lower is better; 'nothing can exceed "
            "it' asserted the bound is unconditionally an upper bound, which is "
            "false for a minimisation quantity (latency, energy per unit "
            "output, cost, defect rate, time-to-X). Live evidence: QT-P1 r3 "
            "labelled a 1.28 kWh/m3 energy floor 'Ideal ceiling' while "
            "following the (then maximisation-only) prescription faithfully — "
            "the prescription induced the directional error, not the agent."
        ),
        exemptions=(),
    ),
    RetractedClaim(
        literal="ideal ceiling (derived), best demonstrated",
        retracted_by="999.171",
        corrected=(
            "This was the matrix restatement (v9.10/TIGHT-02) of the same "
            "maximisation-only premise 'Nothing can exceed it' retracts above. "
            "Registered separately because CLAUDE.md records 58-CR-01 as "
            "55-CR-01's retracted premise resurfacing in "
            "docs/requirements-matrix.md, from a requirement statement never "
            "updated alongside the fix — the exact propagation path this entry "
            "closes across scripts/*.py, docs/**/*.md and docs/data/*.json."
        ),
        exemptions=(),
    ),
)


# This file necessarily contains every literal it bars — the registry IS the
# definition of those literals, not an assertion of them. It is the single
# excluded path, named exactly rather than globbed, so the exclusion cannot
# quietly widen to cover another script that genuinely restates a retracted
# claim. C10 pins the exclusion to a population of one.
SELF_EXCLUDED_PATH = "scripts/check-retracted-claims.py"


# A fenced code block toggles on a ``` or ~~~ line; content inside must not
# be rewritten, since it may be showing Markdown syntax (including `>`) AS
# SOURCE. A line-leading blockquote marker is `>` at the start of a line,
# after optional whitespace, followed by a space or end-of-line — the space
# requirement is what spares `>>> ` doctest prompts.
_FENCE_RE = re.compile(r"^\s*(```|~~~)")
_LEADING_BQ_RE = re.compile(r"^(\s*)>(?: |$)")


def _normalise(text: str) -> str:
    """Collapse whitespace and strip line-leading blockquote markers.

    AP-01: a plain substring match is defeated by ordinary Markdown
    line-wrapping. Demonstrated live during review — the registered literal
    "no new registered gate asserts" had substring count 0 in CHANGELOG.md
    while being present, because the paragraph wraps it across a newline. The
    gate's pass on that entry was luck, not correctness. Both haystack and
    needle are normalised so a wrap point cannot hide a reappearance.

    BQ-01 (Phase 59): whitespace-collapsing alone does not close the same
    class of blind spot for a registered literal wrapped across two `>`
    blockquote lines — the `>` survives whitespace-collapsing as its own
    token and the phrase either side of it never rejoins. A line-leading `>`
    (optional whitespace, then `>`, then a space or end-of-line) is now
    stripped in a loop, so nested quoting (`> > text`) collapses fully — but
    ONLY outside a ``` / ~~~ fenced code block, so a fenced Markdown example
    that shows blockquote syntax AS SOURCE, or a `>>> ` doctest prompt, is
    left byte-intact. Fence-awareness is prospective, not a live save:
    measured at Phase 59, of the 10 line-leading `>` occurrences inside
    fences in the corpus scanned today, all ten are `>>> ` doctest prompts
    that a fence-UNaware, space-requiring strip already spares — the fence
    branch is pinned by its own control (C12), not by today's corpus.

    Residual bounds, disclosed:
      * Rewording. A retracted claim restated in different words remains
        invisible — the register is literal, not semantic, and always was.
      * Non-`>` line-leading Markdown syntax (list markers, table pipes,
        indentation) is out of scope. BQ-01 measured the blockquote case
        specifically; this function does not generalise beyond it.
      * A bare, un-fenced, line-leading shell redirect that is its own
        source line (e.g. `> output.txt`) is indistinguishable from a
        blockquote marker to this function and would be stripped. No such
        line occurs in the corpus scanned at Phase 59, so this is a
        disclosed residual bound, not a live defect — recorded here so it
        is not rediscovered as a surprise.
      * Fence DELIMITER TYPE is not tracked. The fence toggle flips on
        either ``` or ~~~ without recording which opened the block, so a
        literal ~~~ line inside a ```-fenced block (or the reverse) closes
        the fence early: markers after it are then treated as blockquotes
        and stripped, and a real blockquote following the true fence end is
        left alone. Found by the Phase 59 verifier, after the three bounds
        above were written. A corpus walk at Phase 59 found zero files with
        a mismatched open/close fence-type pair, so this has the same
        prospective shape as the fence branch itself — no live effect today,
        and no control pins it.
    """
    out_lines: list[str] = []
    in_fence = False
    for line in text.split("\n"):
        if _FENCE_RE.match(line):
            in_fence = not in_fence
            out_lines.append(line)
            continue
        if in_fence:
            out_lines.append(line)
            continue
        while True:
            m = _LEADING_BQ_RE.match(line)
            if not m:
                break
            line = line[m.end() :]
        out_lines.append(line)
    return " ".join(" ".join(out_lines).split())


def _iter_scan_files(root: Path) -> list[Path]:
    seen: dict[Path, None] = {}
    excluded = (root / SELF_EXCLUDED_PATH).resolve()
    for pattern in SCAN_GLOBS:
        for path in sorted(root.glob(pattern)):
            if not path.is_file():
                continue
            if path.resolve() == excluded:
                continue
            seen.setdefault(path, None)
    return list(seen)


def check(root: Path) -> tuple[bool, list[str]]:
    """Scan published surfaces. Returns (ok, problems)."""
    problems: list[str] = []

    if not REGISTRY:
        problems.append(
            "RETRACT-01: the registry is empty. An empty register passes "
            "vacuously and asserts nothing; that is a defect in the gate, not "
            "a clean tree."
        )
        return False, problems

    files = _iter_scan_files(root)
    if not files:
        problems.append(
            f"RETRACT-01: SCAN_GLOBS matched no files under {root}. The scan "
            "population is empty, so a pass would be vacuous."
        )
        return False, problems

    for claim in REGISTRY:
        exempt = dict(claim.exemptions)
        found: dict[str, int] = {}
        for path in files:
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            n = _normalise(text).count(_normalise(claim.literal))
            if n:
                found[str(path.relative_to(root))] = n

        for rel, n in sorted(found.items()):
            allowed = exempt.get(rel, 0)
            if n > allowed:
                problems.append(
                    f"RETRACT-01 [{claim.retracted_by}]: retracted claim "
                    f'"{claim.literal}" appears {n} time(s) in {rel}'
                    + (f" (exemption allows {allowed})" if allowed else "")
                    + f"\n    What is true instead: {claim.corrected}"
                )

        # Two-sided: an exemption below its count means the erratum that
        # justified it was deleted.
        for rel, allowed in sorted(exempt.items()):
            actual = found.get(rel, 0)
            if actual < allowed:
                problems.append(
                    f"RETRACT-01 [{claim.retracted_by}]: exemption for "
                    f'"{claim.literal}" in {rel} expects {allowed} occurrence(s) '
                    f"but found {actual}. The erratum that justified this "
                    "exemption appears to have been removed — either restore it "
                    "or drop the exemption."
                )

    return (not problems), problems


def describe() -> dict:
    """Pure, gate-agnostic self-description backing RETRACT-01 (D-03 shape)."""
    return {
        "derived_counts": {
            "registered_retracted_claims": len(REGISTRY),
            "exemption_entries": sum(len(c.exemptions) for c in REGISTRY),
        },
        "registered_surfaces": sorted(SCAN_GLOBS),
        "control_ids": sorted(_CONTROL_IDS),
        "control_count": len(_CONTROL_IDS),
    }


_CONTROL_IDS: tuple[str, ...] = (
    "C1-absent-passes",
    "C2-present-fails",
    "C3-exempt-at-count-passes",
    "C4-exempt-above-count-fails",
    "C5-exempt-below-count-fails",
    "C6-empty-registry-fails",
    "C7-empty-population-fails",
    "C8-live-tree",
    "C9-registry-literals-nonempty",
    "C10-self-exclusion-is-one-file",
    "C11-blockquote-wrapped-positive",
    "C12-fenced-blockquote-not-stripped",
    "C13-nonblockquote-leading-gt-preserved",
    "C14-nested-blockquote-fully-stripped",
)


def _fixture(tmp: Path, files: dict[str, str]) -> Path:
    root = tmp
    for rel, text in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    return root


def self_test() -> int:
    """Falsifiability controls. Each asserts the gate CAN fail, not just pass."""
    import tempfile

    global REGISTRY  # noqa: PLW0603 — controls swap the registry deliberately
    original = REGISTRY
    failures: list[str] = []

    recorded: list[str] = []

    def record(cid: str, ok: bool, note: str = "") -> None:
        recorded.append(cid)
        if ok:
            print(f"  PASS {cid}")
        else:
            failures.append(f"{cid}: {note}")
            print(f"  FAIL {cid} — {note}")

    one = (
        RetractedClaim(
            literal="owned by exactly one phase",
            retracted_by="TEST-01",
            corrected="ten invocation sites",
        ),
    )

    try:
        with tempfile.TemporaryDirectory() as td:
            # C1 — a clean tree passes.
            root = _fixture(Path(td) / "c1", {"CLAUDE.md": "nothing to see"})
            REGISTRY = one
            ok, probs = check(root)
            record("C1-absent-passes", ok, f"expected pass, got {probs}")

            # C2 — the claim present in a non-exempt file fails.
            root = _fixture(
                Path(td) / "c2",
                {"docs/x.md": "each technique is owned by exactly one phase, so..."},
            )
            ok, probs = check(root)
            record("C2-present-fails", not ok, "expected failure, gate passed")

            # C3 — exempt file at exactly its allowed count passes.
            REGISTRY = (
                RetractedClaim(
                    literal="no phase owns",
                    retracted_by="TEST-02",
                    corrected="Phase 5 owns it",
                    exemptions=(("CHANGELOG.md", 2),),
                ),
            )
            root = _fixture(
                Path(td) / "c3",
                {"CHANGELOG.md": "erratum: 'no phase owns' was false. no phase owns again."},
            )
            ok, probs = check(root)
            record("C3-exempt-at-count-passes", ok, f"expected pass, got {probs}")

            # C4 — exempt file ABOVE its count fails (new occurrence crept in).
            root = _fixture(
                Path(td) / "c4",
                {"CHANGELOG.md": "no phase owns / no phase owns / no phase owns"},
            )
            ok, _ = check(root)
            record("C4-exempt-above-count-fails", not ok, "expected failure, gate passed")

            # C5 — exempt file BELOW its count fails (the erratum was deleted).
            root = _fixture(Path(td) / "c5", {"CHANGELOG.md": "no phase owns"})
            ok, probs = check(root)
            below = any("appears to have been removed" in p for p in probs)
            record(
                "C5-exempt-below-count-fails",
                (not ok) and below,
                f"expected the two-sided exemption check to fire, got {probs}",
            )

            # C6 — an empty registry must fail, never pass vacuously.
            REGISTRY = ()
            root = _fixture(Path(td) / "c6", {"CLAUDE.md": "x"})
            ok, _ = check(root)
            record("C6-empty-registry-fails", not ok, "empty registry passed vacuously")

            # C7 — an empty scan population must fail, never pass vacuously.
            REGISTRY = one
            root = Path(td) / "c7"
            root.mkdir(parents=True, exist_ok=True)
            ok, _ = check(root)
            record("C7-empty-population-fails", not ok, "empty population passed vacuously")

            # C11 — BQ-01: a registered literal wrapped across two `>`
            # blockquote lines, spanning the wrap point, is counted just like
            # its unquoted twin. The fixture pair differs ONLY by the leading
            # `>` marker. Both twins must match (and therefore fail the gate,
            # since neither is exempted) — asserting only `not ok` would let a
            # broken fixture (e.g. a typo in one twin) pass as a "gate fires"
            # result even if the OTHER twin were silently not matching.
            REGISTRY = one
            root = _fixture(
                Path(td) / "c11",
                {
                    "docs/quoted.md": "> each technique is owned\n> by exactly one phase, so...\n",
                    "docs/plain.md": "each technique is owned\nby exactly one phase, so...\n",
                },
            )
            ok, probs = check(root)
            quoted_hit = any("quoted.md" in p for p in probs)
            plain_hit = any("plain.md" in p for p in probs)
            record(
                "C11-blockquote-wrapped-positive",
                (not ok) and quoted_hit and plain_hit,
                f"expected both twins to match and fail the gate, got ok={ok} probs={probs}",
            )

            # C12 — a line-leading `>` INSIDE a fence (``` or ~~~), even when
            # it IS blockquote syntax, is left untouched — a fenced Markdown
            # example that shows blockquote syntax as source must not be
            # silently rewritten. Per the plan's research corrections, the
            # `>>> ` doctest line alone cannot make this control fail against
            # a fence-unaware implementation (the space-requiring regex
            # already spares it); the `> a literal blockquote` line is what
            # makes this falsifiable.
            fenced_text = (
                "```markdown\n"
                "> a literal blockquote, shown as source\n"
                ">>> doctest_prompt()\n"
                "```\n"
                "~~~\n"
                "> another fenced blockquote line\n"
                "~~~\n"
            )
            normalised = _normalise(fenced_text)
            record(
                "C12-fenced-blockquote-not-stripped",
                "> a literal blockquote, shown as source" in normalised
                and "> another fenced blockquote line" in normalised,
                f"expected both fenced '>' lines preserved, got {normalised!r}",
            )

            # C13 — over-permissiveness negative: a `>` that is NOT a
            # line-leading blockquote marker survives unchanged, and none of
            # these forms spuriously match a registered literal.
            REGISTRY = one
            root = _fixture(
                Path(td) / "c13",
                {
                    "docs/x.md": (
                        ">>> foo(1, 2)\n>notablockquote\nRR-95-01 -> RR-108-01 and x > y\n"
                    )
                },
            )
            ok, _ = check(root)
            normalised = _normalise((root / "docs/x.md").read_text(encoding="utf-8"))
            preserved = (
                ">>> foo(1, 2)" in normalised
                and ">notablockquote" in normalised
                and "RR-95-01 -> RR-108-01 and x > y" in normalised
            )
            record(
                "C13-nonblockquote-leading-gt-preserved",
                ok and preserved,
                f"expected all forms preserved and no spurious match, got ok={ok} "
                f"normalised={normalised!r}",
            )

            # C14 — the `while` loop that handles nested blockquotes
            # (`> > text`) is otherwise untested code; this pins it.
            nested = _normalise("> > text spanning\n> > two nested lines")
            record(
                "C14-nested-blockquote-fully-stripped",
                nested == "text spanning two nested lines",
                f"expected fully-stripped nested quote, got {nested!r}",
            )
    finally:
        REGISTRY = original

    # C8 — live positive control over the real tree.
    ok, probs = check(REPO_ROOT)
    record("C8-live-tree", ok, "; ".join(probs))

    # C9 — no registry entry may carry an empty or whitespace literal, which
    # would match everywhere and make the gate unusable.
    bad = [c.retracted_by for c in REGISTRY if not c.literal.strip()]
    record("C9-registry-literals-nonempty", not bad, f"empty literals: {bad}")

    # C10 — the self-exclusion must cover exactly one file. If it ever widened,
    # a script genuinely restating a retracted claim could hide behind it.
    all_matched: set[str] = set()
    for pattern in SCAN_GLOBS:
        for path in REPO_ROOT.glob(pattern):
            if path.is_file():
                all_matched.add(str(path.relative_to(REPO_ROOT)))
    scanned = {str(p.relative_to(REPO_ROOT)) for p in _iter_scan_files(REPO_ROOT)}
    excluded = all_matched - scanned
    record(
        "C10-self-exclusion-is-one-file",
        excluded == {SELF_EXCLUDED_PATH},
        f"expected exactly {{{SELF_EXCLUDED_PATH!r}}} excluded, got {sorted(excluded)}",
    )

    # AP-02: this check was tautological — it built a set FROM _CONTROL_IDS and
    # compared its length to _CONTROL_IDS, so it could never fail. A control
    # that cannot fail is the exact defect class CLAUDE.md's "Claims and
    # falsifiers" section warns about, and it was sitting inside the self-test
    # written to prevent it. It now compares what record() actually ran against
    # what the roster declares, in both directions.
    declared, ran = set(_CONTROL_IDS), set(recorded)
    if declared != ran:
        missing, extra = sorted(declared - ran), sorted(ran - declared)
        failures.append(
            f"control roster mismatch: declared-but-never-run={missing}, "
            f"run-but-undeclared={extra}"
        )
        print(f"  FAIL roster — missing={missing} extra={extra}")
    else:
        print(f"  PASS roster — all {len(declared)} declared controls ran")
    if len(recorded) != len(set(recorded)):
        failures.append(f"a control id ran more than once: {recorded}")

    if failures:
        print(f"\ncheck-retracted-claims: SELF-TEST FAIL — {len(failures)} control(s)")
        return 1
    print(f"\ncheck-retracted-claims: SELF-TEST PASS — {len(_CONTROL_IDS)} controls run")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="RETRACT-01 retracted-claim register")
    ap.add_argument("--self-test", action="store_true", help="run falsifiability controls")
    ap.add_argument("--describe", action="store_true", help="emit self-description JSON")
    args = ap.parse_args(argv)

    if args.describe:
        print(json.dumps(describe(), indent=2, sort_keys=True))
        return 0
    if args.self_test:
        return self_test()

    ok, problems = check(REPO_ROOT)
    if ok:
        print(
            f"check-retracted-claims: PASS — {len(REGISTRY)} registered claim(s), "
            "none present off-exemption"
        )
        return 0
    for p in problems:
        print(p)
    print(f"\ncheck-retracted-claims: FAIL — {len(problems)} problem(s)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
