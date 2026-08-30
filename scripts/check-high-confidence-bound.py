#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# ///
"""HC-04 gate: assert the Phase 5 tightening of Criterion 3 (Evidence) and
Criterion 5 (Conclusion) is present and well-formed in the Self-Audit rubric,
and that all three EXCEPT exceptions are documented, and that the
`## Exceptions Summary` navigation section exists in its required position.

Phase 5 tightened the rubric's prose to require HIGH-confidence chains
supporting ground truths and conclusions, with three documented exceptions.
Nothing currently stops a future edit from silently reverting it — no existing
gate reads the Criterion 3 or Criterion 5 Rigorous descriptors for the
HIGH-confidence bound, and VAL-04 is structurally blind to rubric content.
This gate is the ratchet that makes the tightening permanent.

This gate validates rubric structure only. It does NOT measure whether the
agent actually produces HIGH-confidence analyses — that is MEAS-01/MEAS-02,
deferred to v8.20+.

Usage:
    python3 scripts/check-high-confidence-bound.py [--self-test]

Exit codes:
    0  all checks passed
    1  validation failure (missing or malformed rubric elements)
    2  environment error (Python <3.12, rubric file not found)

--self-test: runs an offline control battery with negative and positive
             controls, exits 0 if every control behaves as intended; exits 1
             on any wrong-pass or wrong-reason failure.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REPO_ROOT: Path = Path(__file__).resolve().parents[1]
CANONICAL_RUBRIC: Path = REPO_ROOT / "shared" / "spine" / "references" / "validation-rubric.md"
EMITTED_RUBRIC: Path = REPO_ROOT / "first-principles" / "agents" / "references" / "validation-rubric.md"

# --- Heading literals (identica in both canonical and emitted copies) ---
_HOW_TO_APPLY = "## How to Apply This Gate"
_EXCEPTIONS_SUMMARY = "## Exceptions Summary"
_SCORING_MODEL = "## Scoring Model"
_CRITERION3_START = "### Criterion 3: Establish Ground Truths"
_CRITERION4_START = "### Criterion 4: Reason Upward"
_CRITERION5_START = "### Criterion 5: Validate"
_CRITERION6_START = "### Criterion 6: Conclusion-to-Ground-Truth Traceability"

# --- Rigorous band anchors (the "Sound" bullet ends each band) ---
_C3_SOUND_LEAD = "- **Sound** — GT-IDs are present and stable"
_C5_SOUND_LEAD = "- **Sound** — confidence ratings exist on chains"

# --- Whitespace flattening layer (copied from check-focused-parity.py) ---
_WS = re.compile(r"\s+")


def _flat(text: str) -> str:
    """Collapse every whitespace run to a single space."""
    return _WS.sub(" ", text)


def _contains(text: str, literal: str) -> bool:
    """Whitespace-insensitive containment."""
    return _flat(literal) in _flat(text)


def _count_flex(text: str, literal: str) -> int:
    """Whitespace-insensitive occurrence count of *literal* in *text*."""
    pattern = re.compile(
        r"\s+".join(re.escape(w) for w in _flat(literal).strip().split(" "))
    )
    return len(pattern.findall(text))


# --- Slicing contract (copied from check-act-limb.py) ---
def _slice(text: str, start_heading: str, end_heading: str) -> str | None:
    """Return the text strictly between *start_heading* and *end_heading*.

    Returns None if either heading is missing or they appear out of order.
    A vanished section is a failure to report, not an empty string to silently
    pass through.
    """
    start_idx = text.find(start_heading)
    if start_idx == -1:
        return None
    content_start = start_idx + len(start_heading)
    end_idx = text.find(end_heading, content_start)
    if end_idx == -1:
        return None
    return text[content_start:end_idx]


def _rigorous_region(slice_text: str | None, sound_anchor: str) -> str | None:
    """Return the Rigorous descriptor region from the start up to sound_anchor.

    Returns None if the anchor is missing or if slice_text is None.
    The Rigorous region includes the Rigorous bullet and follow-on paragraphs.
    """
    if slice_text is None:
        return None
    # Find the sound anchor
    idx = slice_text.find(sound_anchor)
    if idx == -1:
        return None
    return slice_text[:idx]


def _check_criterion3(text: str, surface: str) -> list[str]:
    """Check Criterion 3 Rigorous descriptors. Returns failure strings."""
    failures: list[str] = []

    # HC-1: Criterion 3 slice present
    c3_slice = _slice(text, _CRITERION3_START, _CRITERION4_START)
    if c3_slice is None:
        failures.append(f"HC-1: {surface} — Criterion 3 slice not found")
        return failures

    # HC-2: Criterion 3 Rigorous region present
    c3_rigorous = _rigorous_region(c3_slice, _C3_SOUND_LEAD)
    if c3_rigorous is None:
        failures.append(f"HC-2: {surface} — Criterion 3 Rigorous region not found (Sound anchor missing)")
        return failures

    # HC-3: "at least one HIGH-confidence chain"
    if not _contains(c3_rigorous, "at least one HIGH-confidence chain"):
        failures.append(f"HC-3: {surface} — Criterion 3 Rigorous: 'at least one HIGH-confidence chain' not found")

    # HC-4: "reachable"
    if not _contains(c3_rigorous, "reachable"):
        failures.append(f"HC-4: {surface} — Criterion 3 Rigorous: 'reachable' not found")

    # HC-5: EXCEPT clause with "unreachable"
    # Split on EXCEPT: and check if unreachable appears after the EXCEPT token
    except_parts = c3_rigorous.split("EXCEPT:")
    unreachable_found = False
    if len(except_parts) > 1:
        # Check the text following the first EXCEPT token (only the part of the first clause)
        first_clause = except_parts[1].split(".")[0] if "." in except_parts[1] else except_parts[1]
        if _contains(first_clause, "unreachable"):
            unreachable_found = True
    if not unreachable_found:
        failures.append(f"HC-5: {surface} — Criterion 3 Rigorous: EXCEPT clause with 'unreachable' not found")

    # HC-6: "Phase 3"
    if not _contains(c3_rigorous, "Phase 3"):
        failures.append(f"HC-6: {surface} — Criterion 3 Rigorous: 'Phase 3' not found")

    return failures


def _check_criterion5(text: str, surface: str) -> list[str]:
    """Check Criterion 5 Rigorous descriptors. Returns failure strings."""
    failures: list[str] = []

    # HC-7: Criterion 5 slice present
    c5_slice = _slice(text, _CRITERION5_START, _CRITERION6_START)
    if c5_slice is None:
        failures.append(f"HC-7: {surface} — Criterion 5 slice not found")
        return failures

    # HC-8: Criterion 5 Rigorous region present
    c5_rigorous = _rigorous_region(c5_slice, _C5_SOUND_LEAD)
    if c5_rigorous is None:
        failures.append(f"HC-8: {surface} — Criterion 5 Rigorous region not found (Sound anchor missing)")
        return failures

    # HC-9: "at least one HIGH-confidence"
    if not _contains(c5_rigorous, "at least one HIGH-confidence"):
        failures.append(f"HC-9: {surface} — Criterion 5 Rigorous: 'at least one HIGH-confidence' not found")

    # HC-10: "Conclusion" (case-insensitive for first letter)
    if not (_contains(c5_rigorous, "Conclusion") or _contains(c5_rigorous, "conclusion")):
        failures.append(f"HC-10: {surface} — Criterion 5 Rigorous: 'Conclusion' not found")

    # HC-11: EXCEPT clause mentioning "speculative"
    # Split on EXCEPT: and check if any following text contains "speculative"
    except_parts = c5_rigorous.split("EXCEPT:")
    speculative_found = False
    if len(except_parts) > 1:
        # Check each EXCEPT clause
        for part in except_parts[1:]:
            if _contains(part.split("EXCEPT:")[0], "speculative"):
                speculative_found = True
                break
    if not speculative_found:
        failures.append(f"HC-11: {surface} — Criterion 5 Rigorous: EXCEPT clause with 'speculative' not found")

    # HC-12: EXCEPT clause mentioning "absent-fails" (or "absent fails")
    absent_fails_found = False
    if len(except_parts) > 1:
        # Check each EXCEPT clause
        for part in except_parts[1:]:
            part_text = part.split("EXCEPT:")[0]
            if _contains(part_text, "absent-fails") or _contains(part_text, "absent fails"):
                absent_fails_found = True
                break
    if not absent_fails_found:
        failures.append(f"HC-12: {surface} — Criterion 5 Rigorous: EXCEPT clause with 'absent-fails' not found")

    return failures


def _check_exceptions_summary(text: str, surface: str) -> list[str]:
    """Check Exceptions Summary section. Returns failure strings."""
    failures: list[str] = []

    # HC-13: Exceptions Summary occurs exactly once
    count = _count_flex(text, _EXCEPTIONS_SUMMARY)
    if count != 1:
        failures.append(f"HC-13: {surface} — Exceptions Summary occurs {count} time(s), expected 1")
        return failures

    # HC-14: Placement — strictly between How to Apply and Scoring Model
    how_to_idx = text.find(_HOW_TO_APPLY)
    exceptions_idx = text.find(_EXCEPTIONS_SUMMARY)
    scoring_idx = text.find(_SCORING_MODEL)

    if how_to_idx == -1 or exceptions_idx == -1 or scoring_idx == -1:
        # Should not happen if HC-13 passed, but be defensive
        failures.append(f"HC-14: {surface} — placement check failed (missing heading)")
        return failures

    if exceptions_idx < how_to_idx:
        failures.append(f"HC-14: {surface} — Exceptions Summary appears before How to Apply This Gate")
    elif exceptions_idx > scoring_idx:
        failures.append(f"HC-14: {surface} — Exceptions Summary appears after Scoring Model")

    # HC-15: Three lettered entries present, in order, inside the section
    exceptions_span = _slice(text, _EXCEPTIONS_SUMMARY, _SCORING_MODEL)
    if exceptions_span is not None:
        # Check for the three lettered entries
        entries = [
            ("(a)", "nreachable source"),  # nreachable matches "unreachable source" case-insensitively
            ("(b)", "peculative chain"),    # peculative matches "speculative chain" case-insensitively
            ("(c)", "bsent-fails derivation"), # bsent-fails matches "absent-fails" case-insensitively
        ]

        entry_positions = []
        for letter, keyword in entries:
            # Check if both letter and keyword appear in the span
            if _contains(exceptions_span, letter) and _contains(exceptions_span, keyword):
                # Find position of the letter to check order
                letter_idx = exceptions_span.lower().find(letter)
                entry_positions.append((letter, keyword, letter_idx))
            else:
                failures.append(f"HC-15: {surface} — Exceptions Summary: entry '{letter}' with '{keyword}' not found")

        # Check order
        if len(entry_positions) == 3:
            # Verify they are in a-b-c order by position
            positions = [pos[2] for pos in entry_positions]
            if positions != sorted(positions):
                failures.append(f"HC-15: {surface} — Exceptions Summary: entries not in a-b-c order")

    return failures


def _check_except_distribution(text: str, surface: str) -> list[str]:
    """Check EXCEPT clause distribution across sections. Returns failure strings."""
    failures: list[str] = []

    # HC-16: EXCEPT: occurs exactly 3 times total, with specific distribution
    total_except = _count_flex(text, "EXCEPT:")

    # Count in Criterion 3 slice
    c3_slice = _slice(text, _CRITERION3_START, _CRITERION4_START)
    c3_except = _count_flex(c3_slice, "EXCEPT:") if c3_slice else 0

    # Count in Criterion 5 slice
    c5_slice = _slice(text, _CRITERION5_START, _CRITERION6_START)
    c5_except = _count_flex(c5_slice, "EXCEPT:") if c5_slice else 0

    # Count in Exceptions Summary span
    exceptions_span = _slice(text, _EXCEPTIONS_SUMMARY, _SCORING_MODEL)
    summary_except = _count_flex(exceptions_span, "EXCEPT:") if exceptions_span else 0

    if total_except != 3 or c3_except != 1 or c5_except != 2 or summary_except != 0:
        failures.append(
            f"HC-16: {surface} — EXCEPT distribution incorrect: "
            f"total={total_except} (expect 3), C3={c3_except} (expect 1), "
            f"C5={c5_except} (expect 2), Summary={summary_except} (expect 0)"
        )

    return failures


def _check_sync(canonical_text: str, emitted_text: str) -> list[str]:
    """Check that emitted copy is byte-identical to canonical from line 3 onward. Returns failure strings."""
    failures: list[str] = []

    # HC-17: Check header shape first
    emitted_lines = emitted_text.split("\n")
    if len(emitted_lines) < 2:
        failures.append(
            f"HC-17: emitted rubric has fewer than 2 lines; "
            f"expected GENERATED header + blank line"
        )
        return failures

    # Check first line contains GENERATED
    if "GENERATED" not in emitted_lines[0]:
        failures.append(
            f"HC-17: emitted rubric first line does not contain 'GENERATED'; "
            f"expected 'GENERATED — DO NOT EDIT' marker"
        )
        return failures

    # Check second line is blank
    if emitted_lines[1].strip() != "":
        failures.append(
            f"HC-17: emitted rubric second line is not blank; "
            f"expected blank line after GENERATED header"
        )
        return failures

    # Now check byte-for-byte sync from line 3 onward
    emitted_content = "\n".join(emitted_lines[2:])
    if emitted_content != canonical_text:
        failures.append(
            f"HC-17: emitted rubric diverges from canonical source; "
            f"sync-content.py regeneration required"
        )

    return failures


def _validate_files() -> int:
    """Validate the live rubric files. Returns a process exit code."""
    if not CANONICAL_RUBRIC.exists():
        sys.stderr.write(
            f"check-high-confidence-bound: canonical rubric file not found: {CANONICAL_RUBRIC}\n"
        )
        return 2

    if not EMITTED_RUBRIC.exists():
        sys.stderr.write(
            f"check-high-confidence-bound: emitted rubric file not found: {EMITTED_RUBRIC}\n"
        )
        return 2

    canonical_text = CANONICAL_RUBRIC.read_text(encoding="utf-8")
    emitted_text = EMITTED_RUBRIC.read_text(encoding="utf-8")

    # Strip the two-line header from emitted text for comparison
    emitted_lines = emitted_text.split("\n")
    emitted_stripped = "\n".join(emitted_lines[2:]) if len(emitted_lines) > 2 else ""

    # Run all checks on both canonical and emitted (with header stripped)
    failures = (
        _check_criterion3(canonical_text, "canonical")
        + _check_criterion5(canonical_text, "canonical")
        + _check_exceptions_summary(canonical_text, "canonical")
        + _check_except_distribution(canonical_text, "canonical")
        + _check_criterion3(emitted_stripped, "emitted")
        + _check_criterion5(emitted_stripped, "emitted")
        + _check_exceptions_summary(emitted_stripped, "emitted")
        + _check_except_distribution(emitted_stripped, "emitted")
        + _check_sync(canonical_text, emitted_text)
    )

    if failures:
        for msg in failures:
            sys.stderr.write(f"check-high-confidence-bound: FAIL — {msg}\n")
        return 1

    print("check-high-confidence-bound: PASS")
    return 0


def _run_self_test() -> int:
    """Run the offline self-test control battery. Placeholder for Task 3."""
    print("check-high-confidence-bound --self-test: control battery not yet populated")
    return 0


def main(argv: list[str] | None = None) -> int:
    """Run the check-high-confidence-bound CLI and return a process exit code."""
    if sys.version_info < (3, 12):
        sys.stderr.write(
            "scripts/check-high-confidence-bound.py requires Python >=3.12 "
            f"(running {sys.version_info.major}.{sys.version_info.minor}).\n"
        )
        return 2

    parser = argparse.ArgumentParser(
        prog="check-high-confidence-bound.py",
        description=(
            "HC-04: assert the Phase 5 tightening of Criterion 3 (Evidence) and "
            "Criterion 5 (Conclusion) is present and well-formed in the Self-Audit rubric."
        ),
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run the offline self-test control battery",
    )
    args = parser.parse_args(argv)

    if args.self_test:
        return _run_self_test()

    return _validate_files()


if __name__ == "__main__":
    sys.exit(main())
