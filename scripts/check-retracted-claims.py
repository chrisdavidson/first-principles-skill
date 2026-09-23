#!/usr/bin/env python3
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
    2  usage / environment error
"""

from __future__ import annotations

import argparse
import json
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
        literal="owned by exactly one phase",
        retracted_by="55-CR-01",
        corrected=(
            "Eight techniques carry ten invocation sites: theoretical-limit at "
            "Phases 1 and 4, inversion at Phases 2 and 5. The decline record is "
            "bounded at <= 10 lines per full-composer run, not <= 8."
        ),
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
        #   CHANGELOG.md  - the v9.7.0 disclosure table names the defect (1)
        #                   and the narrative explains the false grep
        #                   assertion built on it (1).
        #   CLAUDE.md     - the "Claims and falsifiers" rule cites it as the
        #                   worked example of an assertion that pinned a
        #                   claim which was itself false (1).
        # Both are two-sided: deleting the erratum fires this gate just as a
        # new unexempted occurrence does.
        exemptions=(("CHANGELOG.md", 2), ("CLAUDE.md", 1)),
    ),
    RetractedClaim(
        literal="no new registered gate asserts",
        retracted_by="58-CR-02",
        corrected=(
            "TERM-03 is reproducible: SCAN-GUARD's Body-15 asserts the Report "
            "emission invariant sentence against the live shipped agent body, in "
            "CI and in the battery. The coverage was inherited, not built."
        ),
    ),
)


# This file necessarily contains every literal it bars — the registry IS the
# definition of those literals, not an assertion of them. It is the single
# excluded path, named exactly rather than globbed, so the exclusion cannot
# quietly widen to cover another script that genuinely restates a retracted
# claim. C10 pins the exclusion to a population of one.
SELF_EXCLUDED_PATH = "scripts/check-retracted-claims.py"


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
            n = text.count(claim.literal)
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

    def record(cid: str, ok: bool, note: str = "") -> None:
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

    covered = {cid for cid in _CONTROL_IDS}
    if len(covered) != len(_CONTROL_IDS):
        failures.append("control roster mismatch")

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
