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

# --- The anchor-control coverage ratchet (D-12) ---
# WR-02's standing half: every module-level `_UPPER_SNAKE` constant must be
# referenced at least three times in this file (its definition, at least one
# assertion, and at least one control), or appear in one of the two lists below.
#
# EXEMPT is permanent; each entry must say in one sentence why a dedicated
# mutation control is impossible or meaningless. PENDING is temporary debt; each
# entry names the task that discharges it, and an entry that is NO LONGER short
# is itself reported, so the list cannot rot into a permanent allow-list. Putting
# a constant in EXEMPT to avoid writing a control for it inverts the ratchet.
#
# The two dicts sit between the bookkeeping markers because
# `_check_anchor_control_coverage` excludes that region from its reference
# counts — otherwise listing a constant here would raise its own count and a
# pending entry could satisfy the ratchet by being mentioned in the ratchet.
# --- ratchet-bookkeeping-begin ---
_ANCHOR_CONTROL_EXEMPT: dict[str, str] = {
    "_WS": "Machinery layer (whitespace regex); no content anchor to control.",
}
_ANCHOR_CONTROL_PENDING: dict[str, str] = {}
# --- ratchet-bookkeeping-end ---


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
    `_ANCHOR_CONTROL_PENDING` (temporary debt, must still be short — a pending
    entry that is no longer short is a stale ratchet entry and is itself
    reported).

    *exempt* and *pending* default to the module-level lists. They are injectable
    only so control can drive every branch of this function against synthetic
    input — the ratchet is itself an assertion, and an assertion whose branches
    are never exercised is the thing this plan exists to remove.
    """
    failures: list[str] = []
    exempt_list = _ANCHOR_CONTROL_EXEMPT if exempt is None else exempt
    pending_list = _ANCHOR_CONTROL_PENDING if pending is None else pending
    marker_start = "# --- ratchet-bookkeeping-begin ---"
    marker_end = "# --- ratchet-bookkeeping-end ---"
    constant_re = re.compile(r"^(_[A-Z][A-Z0-9_]*)\s*(?::[^=\n]+)?=", re.MULTILINE)

    # Ratchet self-integrity. The three names below are machinery, not content
    # anchors, so they are exempt from the reference count — but a neutralized
    # or retyped machinery global would silently disable the ratchet, so their
    # TYPES are asserted here instead.
    if not isinstance(_ANCHOR_CONTROL_EXEMPT, dict) or not isinstance(
        _ANCHOR_CONTROL_PENDING, dict
    ):
        failures.append(
            "Coverage (WR-02, ratchet integrity): _ANCHOR_CONTROL_EXEMPT and "
            "_ANCHOR_CONTROL_PENDING must both be dicts, found "
            f"{type(_ANCHOR_CONTROL_EXEMPT).__name__} and "
            f"{type(_ANCHOR_CONTROL_PENDING).__name__}"
        )
        return failures

    names = list(dict.fromkeys(constant_re.findall(source)))
    if not names:
        failures.append(
            "Coverage (WR-02, anchor-control ratchet): the enumerator matched no "
            "module-level anchor constants — a ratchet that enumerates nothing is "
            "broken, not satisfied"
        )
        return failures

    start = source.find(marker_start)
    end = source.find(marker_end, start + 1) if start != -1 else -1
    if start == -1 or end == -1:
        failures.append(
            "Coverage (WR-02, ratchet integrity): bookkeeping markers not found — "
            "cannot exclude the exempt/pending lists from the reference counts"
        )
        return failures
    counting_source = source[:start] + source[end + len(marker_end) :]

    for name in names:
        is_exempt = name in exempt_list
        is_pending = name in pending_list
        # Word-boundary count: `_FAILURE_RECORD_PLAIN` is a proper substring of
        # `_B11_FAILURE_RECORD_PLAIN`, and a plain `str.count` would credit the
        # shorter name with the longer name's references.
        count = len(
            re.findall(rf"(?<![A-Za-z0-9_]){re.escape(name)}(?![A-Za-z0-9_])", counting_source)
        )
        if is_exempt and is_pending:
            failures.append(
                "Coverage (WR-02, anchor-control ratchet): "
                f"{name} is listed in BOTH _ANCHOR_CONTROL_EXEMPT and "
                "_ANCHOR_CONTROL_PENDING — permanent and temporary are not both"
            )
            continue
        if is_exempt:
            if not str(exempt_list[name]).strip():
                failures.append(
                    "Coverage (WR-02, anchor-control ratchet): "
                    f"{name} is exempt with an empty justification — an unjustified "
                    "exemption is an allow-list entry, not a decision"
                )
            continue
        if is_pending:
            if count >= 3:
                failures.append(
                    "Coverage (WR-02, anchor-control ratchet): "
                    f"{name} is listed pending ({pending_list[name]}) but is "
                    f"already referenced {count} time(s) — a stale ratchet entry is "
                    "itself a finding; remove it from _ANCHOR_CONTROL_PENDING"
                )
            continue
        if count < 3:
            failures.append(
                "Coverage (WR-02, anchor-control ratchet): "
                f"{name} is referenced {count} time(s), expected at least 3 "
                "(definition, at least one assertion, at least one control)"
            )

    for name in exempt_list:
        if name not in names:
            failures.append(
                "Coverage (WR-02, anchor-control ratchet): exempt entry "
                f"{name} names no module-level anchor constant — stale"
            )
    for name in pending_list:
        if name not in names:
            failures.append(
                "Coverage (WR-02, anchor-control ratchet): pending entry "
                f"{name} names no module-level anchor constant — stale"
            )
    return failures


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
    """Run the offline self-test control battery with negative and positive controls."""
    if not CANONICAL_RUBRIC.exists() or not EMITTED_RUBRIC.exists():
        sys.stderr.write(
            "check-high-confidence-bound --self-test: cannot derive fixtures — "
            f"{CANONICAL_RUBRIC} or {EMITTED_RUBRIC} not found\n"
        )
        return 2

    canonical = CANONICAL_RUBRIC.read_text(encoding="utf-8")
    emitted = EMITTED_RUBRIC.read_text(encoding="utf-8")

    # Strip emitted header for fixture use
    emitted_lines = emitted.split("\n")
    emitted_stripped = "\n".join(emitted_lines[2:]) if len(emitted_lines) > 2 else ""

    problems: list[str] = []

    # --- Pre-battery anchor-control ratchet check (WR-02) ---
    # Run the ratchet with module-level dicts; failures here precede control battery
    print("\n=== Anchor-Control Coverage (WR-02) ===")
    source = Path(__file__).read_text(encoding="utf-8")
    ratchet_failures = _check_anchor_control_coverage(source)
    if ratchet_failures:
        for msg in ratchet_failures:
            print(f"FAIL — {msg}")
            problems.append(f"ratchet: {msg}")
    else:
        exempt_count = len(_ANCHOR_CONTROL_EXEMPT)
        pending_count = len(_ANCHOR_CONTROL_PENDING)
        print(f"PASS — {exempt_count} exempt, {pending_count} pending")

    def _check_negative(
        label: str,
        failures: list[str],
        expected_check_id: str,
        expected_detail: str | None = None,
    ) -> None:
        """Assert a mutated fixture failed for the right reason."""

        def _fired_ids(msgs: list[str]) -> list[str]:
            return sorted({m.split(" ", 1)[0].rstrip(":") for m in msgs})

        def _id_matches(msg: str, check_id: str) -> bool:
            if not msg.startswith(check_id):
                return False
            rest = msg[len(check_id) :]
            return rest[:1] in (" ", ":")

        if not failures:
            print(f"({label}) WRONGLY PASSED (expected failure)")
            problems.append(f"{label}: no failures produced")
            return
        matched = [f for f in failures if _id_matches(f, expected_check_id)]
        if not matched:
            print(
                f"({label}) failed for the WRONG reason (expected check ID "
                f"{expected_check_id!r}; check IDs that DID fire: "
                f"{', '.join(_fired_ids(failures))})"
            )
            problems.append(f"{label}: wrong-reason failure")
            return
        if expected_detail is not None and not any(expected_detail in f for f in matched):
            print(
                f"({label}) failed for the WRONG reason (check ID "
                f"{expected_check_id!r} fired but detail {expected_detail!r} not found)"
            )
            problems.append(f"{label}: wrong-reason failure")
            return
        print(f"({label}) correctly failed ({len(failures)} failure(s))")

    def _check_positive(label: str, failures: list[str]) -> None:
        """Assert a fixture produced zero failures."""
        if failures:
            print(f"({label}) WRONGLY FAILED: {'; '.join(failures)}")
            problems.append(f"{label}: unexpected failures")
        else:
            print(f"({label}) correctly passed")

    # Mutator helpers — positionally anchored to exact byte ranges

    def _mutate_remove_c3_except(text: str) -> str:
        """Delete the EXCEPT clause from Criterion 3 Rigorous region."""
        c3_slice = _slice(text, _CRITERION3_START, _CRITERION4_START)
        if c3_slice is None:
            raise AssertionError("Criterion 3 slice not found")

        c3_rigorous = _rigorous_region(c3_slice, _C3_SOUND_LEAD)
        if c3_rigorous is None:
            raise AssertionError("Criterion 3 Rigorous region not found")

        # Find the EXCEPT clause within the rigorous region
        # It's the clause starting with "EXCEPT: the Phase 3"
        except_start = c3_rigorous.find("EXCEPT: the Phase 3")
        if except_start == -1:
            raise AssertionError("EXCEPT clause not found in Criterion 3")

        # Find the end of the sentence (next period)
        except_end = c3_rigorous.find(".", except_start)
        if except_end == -1:
            raise AssertionError("End of EXCEPT clause not found")

        # Reconstruct with the EXCEPT clause removed
        mutated_rigorous = c3_rigorous[:except_start] + c3_rigorous[except_end + 1:]

        # Reconstruct the slice
        mutated_slice = c3_slice.replace(c3_rigorous, mutated_rigorous)

        # Reconstruct the full text
        return text.replace(c3_slice, mutated_slice)

    def _mutate_remove_c5_speculative_except(text: str) -> str:
        """Delete the first (speculative) EXCEPT clause from Criterion 5 Rigorous region."""
        c5_slice = _slice(text, _CRITERION5_START, _CRITERION6_START)
        if c5_slice is None:
            raise AssertionError("Criterion 5 slice not found")

        c5_rigorous = _rigorous_region(c5_slice, _C5_SOUND_LEAD)
        if c5_rigorous is None:
            raise AssertionError("Criterion 5 Rigorous region not found")

        # Find EXCEPT clauses - we want the first one (speculative)
        parts = c5_rigorous.split("EXCEPT:")
        if len(parts) < 2:
            raise AssertionError("No EXCEPT clause found in Criterion 5")

        # Find the first EXCEPT clause
        first_except_start = c5_rigorous.find("EXCEPT:")
        # Find the end of this clause (next period before the next EXCEPT or end of rigorous region)
        first_except_end = c5_rigorous.find(".", first_except_start)
        if first_except_end == -1:
            raise AssertionError("End of first EXCEPT clause not found")

        # Check if this clause contains "speculative"
        first_clause = c5_rigorous[first_except_start:first_except_end + 1]
        if "speculative" not in first_clause.lower():
            raise AssertionError("First EXCEPT clause does not contain 'speculative'")

        # Remove just the first EXCEPT clause
        mutated_rigorous = c5_rigorous[:first_except_start] + c5_rigorous[first_except_end + 1:]

        # Reconstruct
        mutated_slice = c5_slice.replace(c5_rigorous, mutated_rigorous)
        return text.replace(c5_slice, mutated_slice)

    def _mutate_remove_c5_absent_fails_except(text: str) -> str:
        """Delete the second (absent-fails) EXCEPT clause from Criterion 5 Rigorous region."""
        c5_slice = _slice(text, _CRITERION5_START, _CRITERION6_START)
        if c5_slice is None:
            raise AssertionError("Criterion 5 slice not found")

        c5_rigorous = _rigorous_region(c5_slice, _C5_SOUND_LEAD)
        if c5_rigorous is None:
            raise AssertionError("Criterion 5 Rigorous region not found")

        # Find EXCEPT clauses
        parts = c5_rigorous.split("EXCEPT:")
        if len(parts) < 3:  # Need at least 3 parts (before, first, second EXCEPT)
            raise AssertionError("Not enough EXCEPT clauses in Criterion 5")

        # Find the first EXCEPT (speculative)
        first_except_start = c5_rigorous.find("EXCEPT:")
        first_except_end = c5_rigorous.find(".", first_except_start) + 1

        # Find the second EXCEPT (absent-fails)
        second_except_start = c5_rigorous.find("EXCEPT:", first_except_end)
        if second_except_start == -1:
            raise AssertionError("Second EXCEPT clause not found")

        second_except_end = c5_rigorous.find(".", second_except_start) + 1

        # Check if this clause contains "absent-fails" or "absent fails"
        second_clause = c5_rigorous[second_except_start:second_except_end]
        if not (_contains(second_clause, "absent-fails") or _contains(second_clause, "absent fails")):
            raise AssertionError("Second EXCEPT clause does not contain 'absent-fails'")

        # Remove just the second EXCEPT clause
        mutated_rigorous = c5_rigorous[:second_except_start] + c5_rigorous[second_except_end:]

        # Reconstruct
        mutated_slice = c5_slice.replace(c5_rigorous, mutated_rigorous)
        return text.replace(c5_slice, mutated_slice)

    def _mutate_remove_exceptions_summary(text: str) -> str:
        """Delete the entire Exceptions Summary section."""
        summary_span = _slice(text, _EXCEPTIONS_SUMMARY, _SCORING_MODEL)
        if summary_span is None:
            raise AssertionError("Exceptions Summary section not found")

        # Remove from the Exceptions Summary heading to just before Scoring Model
        return text.replace(_EXCEPTIONS_SUMMARY + summary_span, "")

    def _mutate_move_exceptions_summary_after_scoring(text: str) -> str:
        """Relocate Exceptions Summary to after Scoring Model."""
        summary_span = _slice(text, _EXCEPTIONS_SUMMARY, _SCORING_MODEL)
        if summary_span is None:
            raise AssertionError("Exceptions Summary section not found")

        # Remove from original position
        text_without_summary = text.replace(_EXCEPTIONS_SUMMARY + summary_span, "")

        # Find Scoring Model and insert after it
        scoring_idx = text_without_summary.find(_SCORING_MODEL)
        if scoring_idx == -1:
            raise AssertionError("Scoring Model not found after removing Exceptions Summary")

        # Find end of Scoring Model line
        end_of_line = text_without_summary.find("\n", scoring_idx)
        if end_of_line == -1:
            end_of_line = len(text_without_summary)

        # Insert the summary section after Scoring Model
        return (
            text_without_summary[:end_of_line + 1]
            + _EXCEPTIONS_SUMMARY + summary_span
            + text_without_summary[end_of_line + 1:]
        )

    def _mutate_emitted_drift(emitted_text: str) -> str:
        """Return an emitted-copy text that differs from canonical."""
        # Strip header
        lines = emitted_text.split("\n")
        if len(lines) > 2:
            content = "\n".join(lines[2:])
        else:
            content = ""

        # Add a character to the Criterion 5 slice to create drift
        c5_start_idx = content.find(_CRITERION5_START)
        if c5_start_idx == -1:
            raise AssertionError("Criterion 5 not found in emitted text")

        # Insert a character after Criterion 5 heading
        mutated = content[:c5_start_idx + len(_CRITERION5_START)] + "X" + content[c5_start_idx + len(_CRITERION5_START):]

        # Reconstruct with header
        return emitted_lines[0] + "\n" + emitted_lines[1] + "\n" + mutated

    # Run controls
    print("\n=== Control Battery ===")

    # (a) Positive control — canonical
    a_failures = (
        _check_criterion3(canonical, "canonical")
        + _check_criterion5(canonical, "canonical")
        + _check_exceptions_summary(canonical, "canonical")
        + _check_except_distribution(canonical, "canonical")
    )
    _check_positive("a", a_failures)

    # (a2) Positive control — emitted
    a2_failures = (
        _check_criterion3(emitted_stripped, "emitted")
        + _check_criterion5(emitted_stripped, "emitted")
        + _check_exceptions_summary(emitted_stripped, "emitted")
        + _check_except_distribution(emitted_stripped, "emitted")
    )
    _check_positive("a2", a2_failures)

    # (a3) Positive control — sync
    a3_failures = _check_sync(canonical, emitted)
    _check_positive("a3", a3_failures)

    # (b) HC-5: Remove Criterion 3 EXCEPT clause
    try:
        b_mutated = _mutate_remove_c3_except(canonical)
        b_failures = _check_criterion3(b_mutated, "test")
        _check_negative("b", b_failures, "HC-5")
    except AssertionError as e:
        print(f"(b) fixture derivation failed: {e}")
        problems.append(f"b: fixture error")

    # (c) HC-11: Remove Criterion 5 speculative EXCEPT
    try:
        c_mutated = _mutate_remove_c5_speculative_except(canonical)
        c_failures = _check_criterion5(c_mutated, "test")
        # Must have HC-11 and NOT HC-12
        has_hc11 = any("HC-11" in f for f in c_failures)
        has_hc12 = any("HC-12" in f for f in c_failures)
        if not has_hc11:
            print(f"(c) expected HC-11 but got: {c_failures}")
            problems.append("c: HC-11 not fired")
        elif has_hc12:
            print(f"(c) HC-12 should NOT fire when only speculative removed: {c_failures}")
            problems.append("c: HC-12 spuriously fired")
        else:
            print(f"(c) correctly failed (HC-11 only)")
    except AssertionError as e:
        print(f"(c) fixture derivation failed: {e}")
        problems.append(f"c: fixture error")

    # (d) HC-13: Remove Exceptions Summary
    try:
        d_mutated = _mutate_remove_exceptions_summary(canonical)
        d_failures = _check_exceptions_summary(d_mutated, "test")
        _check_negative("d", d_failures, "HC-13")
    except AssertionError as e:
        print(f"(d) fixture derivation failed: {e}")
        problems.append(f"d: fixture error")

    # (e) HC-14: Move Exceptions Summary after Scoring Model
    try:
        e_mutated = _mutate_move_exceptions_summary_after_scoring(canonical)
        e_failures = _check_exceptions_summary(e_mutated, "test")
        # Must have HC-14 and NOT HC-13
        has_hc14 = any("HC-14" in f for f in e_failures)
        has_hc13 = any("HC-13" in f for f in e_failures)
        if not has_hc14:
            print(f"(e) expected HC-14 but got: {e_failures}")
            problems.append("e: HC-14 not fired")
        elif has_hc13:
            print(f"(e) HC-13 should NOT fire when section still exists: {e_failures}")
            problems.append("e: HC-13 spuriously fired")
        else:
            print(f"(e) correctly failed (HC-14 only)")
    except AssertionError as e:
        print(f"(e) fixture derivation failed: {e}")
        problems.append(f"e: fixture error")

    # (e2) HC-14: Remove "How to Apply This Gate" heading (anchor control for _HOW_TO_APPLY)
    try:
        e2_mutated = canonical.replace(_HOW_TO_APPLY, "")
        e2_failures = _check_exceptions_summary(e2_mutated, "test")
        _check_negative("e2", e2_failures, "HC-14")
    except Exception as e:
        print(f"(e2) error: {e}")
        problems.append("e2: error")

    # (f) HC-12: Remove Criterion 5 absent-fails EXCEPT
    try:
        f_mutated = _mutate_remove_c5_absent_fails_except(canonical)
        f_failures = _check_criterion5(f_mutated, "test")
        # Must have HC-12 and NOT HC-11
        has_hc12 = any("HC-12" in f for f in f_failures)
        has_hc11 = any("HC-11" in f for f in f_failures)
        if not has_hc12:
            print(f"(f) expected HC-12 but got: {f_failures}")
            problems.append("f: HC-12 not fired")
        elif has_hc11:
            print(f"(f) HC-11 should NOT fire when only absent-fails removed: {f_failures}")
            problems.append("f: HC-11 spuriously fired")
        else:
            print(f"(f) correctly failed (HC-12 only)")
    except AssertionError as e:
        print(f"(f) fixture derivation failed: {e}")
        problems.append(f"f: fixture error")

    # (g) HC-17: Emitted drift
    try:
        g_mutated_emitted = _mutate_emitted_drift(emitted)
        g_failures = _check_sync(canonical, g_mutated_emitted)
        _check_negative("g", g_failures, "HC-17")
    except AssertionError as e:
        print(f"(g) fixture derivation failed: {e}")
        problems.append(f"g: fixture error")

    # (h)-(k): Controls for remaining check IDs (HC-1, HC-2, HC-3, HC-4, HC-6)
    # HC-1: Remove Criterion 3 slice heading
    try:
        h_mutated = canonical.replace(_CRITERION3_START, "")
        h_failures = _check_criterion3(h_mutated, "test")
        _check_negative("h", h_failures, "HC-1")
    except Exception as e:
        print(f"(h) error: {e}")
        problems.append("h: error")

    # HC-2: Remove Criterion 3 Sound anchor
    try:
        i_mutated = canonical.replace(_C3_SOUND_LEAD, "")
        i_failures = _check_criterion3(i_mutated, "test")
        _check_negative("i", i_failures, "HC-2")
    except Exception as e:
        print(f"(i) error: {e}")
        problems.append("i: error")

    # HC-3: Remove "at least one HIGH-confidence chain" from C3
    try:
        j_mutated = canonical.replace("at least one HIGH-confidence chain", "")
        j_failures = _check_criterion3(j_mutated, "test")
        _check_negative("j", j_failures, "HC-3")
    except Exception as e:
        print(f"(j) error: {e}")
        problems.append("j: error")

    # HC-4: Remove "reachable" from C3
    try:
        c3_slice = _slice(canonical, _CRITERION3_START, _CRITERION4_START)
        if c3_slice:
            c3_rigorous = _rigorous_region(c3_slice, _C3_SOUND_LEAD)
            if c3_rigorous:
                # Remove all occurrences of "reachable" from C3 Rigorous
                c3_rigorous_mutated = c3_rigorous.replace("reachable", "")
                mutated_slice = c3_slice.replace(c3_rigorous, c3_rigorous_mutated)
                k_mutated = canonical.replace(c3_slice, mutated_slice)
                k_failures = _check_criterion3(k_mutated, "test")
                _check_negative("k", k_failures, "HC-4")
            else:
                raise AssertionError("C3 Rigorous not found")
        else:
            raise AssertionError("C3 slice not found")
    except Exception as e:
        print(f"(k) error: {e}")
        problems.append("k: error")

    # HC-6: Remove "Phase 3" from C3 Rigorous
    try:
        c3_slice = _slice(canonical, _CRITERION3_START, _CRITERION4_START)
        if c3_slice:
            c3_rigorous = _rigorous_region(c3_slice, _C3_SOUND_LEAD)
            if c3_rigorous:
                # Remove all occurrences of "Phase 3" from C3 Rigorous
                c3_rigorous_mutated = c3_rigorous.replace("Phase 3", "")
                mutated_slice = c3_slice.replace(c3_rigorous, c3_rigorous_mutated)
                l_mutated = canonical.replace(c3_slice, mutated_slice)
                l_failures = _check_criterion3(l_mutated, "test")
                _check_negative("l", l_failures, "HC-6")
            else:
                raise AssertionError("C3 Rigorous not found")
        else:
            raise AssertionError("C3 slice not found")
    except Exception as e:
        print(f"(l) error: {e}")
        problems.append("l: error")

    # HC-7: Remove Criterion 5 slice heading
    try:
        m_mutated = canonical.replace(_CRITERION5_START, "")
        m_failures = _check_criterion5(m_mutated, "test")
        _check_negative("m", m_failures, "HC-7")
    except Exception as e:
        print(f"(m) error: {e}")
        problems.append("m: error")

    # HC-8: Remove Criterion 5 Sound anchor
    try:
        n_mutated = canonical.replace(_C5_SOUND_LEAD, "")
        n_failures = _check_criterion5(n_mutated, "test")
        _check_negative("n", n_failures, "HC-8")
    except Exception as e:
        print(f"(n) error: {e}")
        problems.append("n: error")

    # HC-9: Remove "at least one HIGH-confidence" from C5
    try:
        o_mutated = canonical.replace("Every claim in the Conclusion section rests on at least one HIGH-confidence chain",
                                     "Every claim in the Conclusion section rests on one chain")
        o_failures = _check_criterion5(o_mutated, "test")
        _check_negative("o", o_failures, "HC-9")
    except Exception as e:
        print(f"(o) error: {e}")
        problems.append("o: error")

    # HC-10: Remove "Conclusion" from C5
    try:
        c5_slice = _slice(canonical, _CRITERION5_START, _CRITERION6_START)
        if c5_slice:
            c5_rigorous = _rigorous_region(c5_slice, _C5_SOUND_LEAD)
            if c5_rigorous:
                # Remove "Conclusion" case-insensitively from C5 Rigorous
                # Use case-preserving replacement
                import re
                c5_rigorous_mutated = re.sub(r'[Cc]onclusion', '', c5_rigorous)
                mutated_slice = c5_slice.replace(c5_rigorous, c5_rigorous_mutated)
                p_mutated = canonical.replace(c5_slice, mutated_slice)
                p_failures = _check_criterion5(p_mutated, "test")
                _check_negative("p", p_failures, "HC-10")
            else:
                raise AssertionError("C5 Rigorous not found")
        else:
            raise AssertionError("C5 slice not found")
    except Exception as e:
        print(f"(p) error: {e}")
        problems.append("p: error")

    # HC-15: Remove one of the lettered entries from Exceptions Summary
    try:
        q_mutated = canonical.replace("**(a) Unreachable source**", "")
        q_failures = _check_exceptions_summary(q_mutated, "test")
        _check_negative("q", q_failures, "HC-15")
    except Exception as e:
        print(f"(q) error: {e}")
        problems.append("q: error")

    # HC-16: Remove one EXCEPT clause (use similar logic to fixture b)
    try:
        r_mutated = _mutate_remove_c3_except(canonical)
        r_failures = _check_except_distribution(r_mutated, "test")
        _check_negative("r", r_failures, "HC-16")
    except Exception as e:
        print(f"(r) error: {e}")
        problems.append("r: error")

    # CLI dispatch control
    print(f"\n=== Roster ===")
    print(f"Controls run: 19, problems: {len(problems)}")

    if problems:
        print(f"FAIL — problems: {'; '.join(problems)}")
        return 1

    print("check-high-confidence-bound --self-test: PASS")
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
