#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml>=6.0"]
# ///
"""GATE-01 gate: validate the generated agent surface against the locked frontmatter schema.

Usage:
    python3 scripts/check-agent.py [--self-test]

Exit codes:
    0  all checks passed
    1  validation failure (file content wrong)
    2  environment error (Python <3.12, PyYAML missing, file not found, malformed YAML)

--self-test: runs three inline malformed fixtures and exits 0 if all correctly fail;
             exits 1 if any fixture wrongly passes.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REPO_ROOT: Path = Path(__file__).resolve().parents[1]
AGENT_FILE: Path = REPO_ROOT / "first-principles" / "agents" / "first-principles.md"

# Frontmatter fence pattern (from scripts/_skill_io.py)
_FENCE_RE = re.compile(r"^---\s*$", re.MULTILINE)

# Unresolved sync marker pattern — the sync pipeline uses {{TOOL:<slug>}} markers
_MARKER_RE = re.compile(r"\{\{.*?\}\}")

# Top-level `name:` frontmatter key, used by the live anti-vacuity control in
# _assert_live_coverage() to mutate the text this run actually read.
_NAME_KEY_RE = re.compile(r"^name:.*$\n", re.MULTILINE)

# Expected locked values
_EXPECTED_NAME = "first-principles"
_MAX_DESCRIPTION_LEN = 1024
# Phase 5's Self-Audit Gate runs last and depends on this exact turn budget for
# its headroom (SCAN-04, first-principles.md:84). Checking only that the key
# exists (as Check 5 did before) lets the value silently drift — a `60 -> 20`
# edit passed every gate in the battery undetected.
_EXPECTED_MAX_TURNS = 60
_REQUIRED_PHRASES = [
    "first principles",
    "challenge assumptions",
    "reason from ground truth",
    "decompose this problem",
]

# Phase 21 (D-21-J): the check roster GATE-01's CLAUDE.md row publishes —
# "8 frontmatter/body assertions". This is an ENUMERATION LIFT, not a
# refactor: the checks below, their order, their failure messages and their
# verdicts are unchanged (D-21-J's hard bound). Each entry's index is the
# fixed position `_check_agent_text()` gates that check's execution on
# (`if IDX < len(_CHECK_DESCRIPTIONS):`) — so len(_CHECK_DESCRIPTIONS) is
# the count this module actually runs, not a hand-typed "8" beside untouched
# inline code. Check 1 (index 0, the frontmatter-fence parse) is the sole
# exception: it is structurally required to reach every later check (there
# is no frontmatter/body to inspect without it) and stays unconditional,
# matching how a malformed-fence input already exits(2) as an
# environment-class error rather than accumulating into `failures`.
#
# Phase 21-15 (CR-05): this claim used to rest on the gating condition alone —
# nothing recorded which indices actually ran, so a fabricated ninth entry
# appended to this tuple would publish `branch_count` 9 with nothing behind
# it. `_check_agent_text()` now records every index it actually reaches into
# the module-level `_EXECUTED_CHECK_INDICES` set (cleared at the top of each
# call), and `_run_self_test()` floors that set against
# `range(len(_CHECK_DESCRIPTIONS))` — minus `_SKIP_NAME_CHECK_SCOPED_INDICES`
# under `--skip-name-check` — via `_index_roster_problems()`, in both
# directions, with a permanent synthetic negative arm proving the floor
# itself fires.
_CHECK_DESCRIPTIONS: tuple[str, ...] = (
    "Check 1: file begins with a frontmatter fence and splits into exactly 3 parts",
    "Check 2: 'name' key present and equals the locked identity "
    "(skipped under --skip-name-check)",
    "Check 3: 'description' is a non-empty string within the max-length budget",
    "Check 4: 'disallowedTools' key is present",
    "Check 5: 'maxTurns' key is present; for the canonical identity only, "
    "also carries the locked value (value clause skipped under --skip-name-check)",
    "Check 6: body is non-empty after stripping whitespace",
    "Check 7: body contains no unresolved sync markers",
    "Check 8: 'description' contains all mandatory trigger phrases "
    "(skipped under --skip-name-check)",
)

# Indices into _CHECK_DESCRIPTIONS scoped out under --skip-name-check — a
# published fact of GATE-01's CLAUDE.md row (Checks 2, 5's value clause, 8),
# derived here rather than re-typed in prose on every surface that states it.
_SKIP_NAME_CHECK_SCOPED_INDICES: tuple[int, ...] = (1, 4, 7)

# Phase 21-15 (CR-05): populated fresh on every `_check_agent_text()` call
# with the index of every check that call actually reached (cleared as that
# function's first statement). Module-level rather than a return value so the
# existing return type (`list[str]` of failures) does not have to change to
# carry it.
_EXECUTED_CHECK_INDICES: set[int] = set()


def _index_roster_problems(executed: set[int], expected: set[int]) -> list[str]:
    """Pure set-equality floor shared by `_run_self_test()`'s live arms and
    its own synthetic negative arm, so the negative arm exercises the SAME
    code the live floor uses rather than a re-implementation.

    Reports both directions in one message (D-04 lesson): an index expected
    but never reached is named under `missing=`; an index reached but not
    expected is named under `extra=`.
    """
    missing = expected - executed
    extra = executed - expected
    if missing or extra:
        return [
            f"executed/registered check-index mismatch: missing={sorted(missing)} "
            f"extra={sorted(extra)}"
        ]
    return []


# Self-test fixture: fully valid canonical agent — zero failures under
# skip_name_check=False, used by the executed-check-index floor (Phase 21-15)
# to assert every check actually ran, not merely that a malformed fixture
# happened to reach the gate that catches its one defect.
_FIXTURE_VALID_CANONICAL = """\
---
name: first-principles
description: Analyze from first principles; challenge assumptions; reason from ground truth; decompose this problem into its ground truths.
license: MIT
metadata:
  version: "3.0.0"
disallowedTools:
  - Write
  - Edit
maxTurns: 60
AskUserQuestion: permitted
---
## Body

This is a non-empty body with valid content and no unresolved sync markers.
"""

# Self-test fixture: missing `name` key in frontmatter
_FIXTURE_MISSING_NAME = """\
---
description: A test agent for first-principles analysis.
license: MIT
metadata:
  version: "3.0.0"
disallowedTools:
  - Write
  - Edit
maxTurns: 30
AskUserQuestion: permitted
---
## Body

This is a non-empty body with valid content.
"""

# Self-test fixture: empty body (whitespace-only after closing ---)
_FIXTURE_EMPTY_BODY = """\
---
name: first-principles
description: A test agent for first-principles analysis.
license: MIT
metadata:
  version: "3.0.0"
disallowedTools:
  - Write
  - Edit
maxTurns: 30
AskUserQuestion: permitted
---

   \t
"""

# Self-test fixture: unresolved sync marker in body
_FIXTURE_UNRESOLVED_MARKER = """\
---
name: first-principles
description: A test agent for first-principles analysis.
license: MIT
metadata:
  version: "3.0.0"
disallowedTools:
  - Write
  - Edit
maxTurns: 30
AskUserQuestion: permitted
---
## Body

This body contains an unresolved sync marker: {{TOOL:five-whys}}
"""

# Self-test fixture: wrong `name` value (present but not "first-principles")
_FIXTURE_WRONG_NAME = """\
---
name: wrong-agent-name
description: A test agent for first-principles analysis.
license: MIT
metadata:
  version: "3.0.0"
disallowedTools:
  - Write
  - Edit
maxTurns: 30
AskUserQuestion: permitted
---
## Body

This is a non-empty body with valid content.
"""

# Self-test fixture: description exceeds the 1024-char limit
_FIXTURE_LONG_DESCRIPTION = (
    "---\n"
    "name: first-principles\n"
    'description: "' + ("x" * (_MAX_DESCRIPTION_LEN + 1)) + '"\n'
    "license: MIT\n"
    "metadata:\n"
    '  version: "3.0.0"\n'
    "disallowedTools:\n"
    "  - Write\n"
    "  - Edit\n"
    "maxTurns: 30\n"
    "AskUserQuestion: permitted\n"
    "---\n"
    "## Body\n"
    "\n"
    "This is a non-empty body with valid content.\n"
)

# Self-test fixture: missing `maxTurns` key
_FIXTURE_MISSING_MAXTURNS = """\
---
name: first-principles
description: A test agent for first-principles analysis.
license: MIT
metadata:
  version: "3.0.0"
disallowedTools:
  - Write
  - Edit
AskUserQuestion: permitted
---
## Body

This is a non-empty body with valid content.
"""

# Self-test fixture: `maxTurns` present but not the locked value (60)
_FIXTURE_WRONG_MAXTURNS_VALUE = """\
---
name: first-principles
description: A test agent for first-principles analysis.
license: MIT
metadata:
  version: "3.0.0"
disallowedTools:
  - Write
  - Edit
maxTurns: 20
AskUserQuestion: permitted
---
## Body

This is a non-empty body with valid content.
"""

# Self-test fixture: missing `disallowedTools` key
_FIXTURE_MISSING_DISALLOWED_TOOLS = """\
---
name: first-principles
description: A test agent for first-principles analysis.
license: MIT
metadata:
  version: "3.0.0"
maxTurns: 30
AskUserQuestion: permitted
---
## Body

This is a non-empty body with valid content.
"""

# Self-test fixture: description missing one mandatory trigger phrase
_FIXTURE_MISSING_TRIGGER_PHRASE = """\
---
name: first-principles
description: Analyze from first principles; challenge assumptions; reason from ground truth. No decompose phrase.
license: MIT
metadata:
  version: "3.0.0"
disallowedTools:
  - Write
  - Edit
maxTurns: 30
AskUserQuestion: permitted
---
## Body

This is a non-empty body with valid content.
"""

# Self-test fixture: structurally valid candidate with a non-first-principles name
# and no trigger phrases — used to verify skip_name_check=True path
_FIXTURE_CANDIDATE_VALID = """\
---
name: my-builder-agent
description: A builder-generated candidate agent for structural validation testing.
license: MIT
metadata:
  version: "1.0.0"
disallowedTools:
  - Write
  - Edit
maxTurns: 30
AskUserQuestion: permitted
---
## Body

Non-empty body content for the candidate agent fixture.
"""


def _require_python_version() -> None:
    if sys.version_info < (3, 12):
        sys.stderr.write(
            f"scripts/check-agent.py requires Python >=3.12 "
            f"(running {sys.version_info.major}.{sys.version_info.minor}).\n"
        )
        sys.exit(2)


def _require_pyyaml() -> None:
    """Catch missing PyYAML at startup with a clear remediation message."""
    try:
        import yaml  # noqa: F401
    except ImportError:
        sys.stderr.write(
            "scripts/check-agent.py needs PyYAML.\n"
            "  Easiest:  uv run scripts/check-agent.py\n"
            "  Or:       pip install --user 'pyyaml>=6.0'  &&  "
            "python3 scripts/check-agent.py\n"
        )
        sys.exit(2)


def _check_agent_text(text: str, skip_name_check: bool = False) -> list[str]:
    """Validate agent file text against the locked schema.

    Args:
        text: The full agent file text (frontmatter + body).
        skip_name_check: If True, skip Check 2 (name identity) and Check 8
            (trigger-phrase presence). Use for builder-generated candidate agents
            that are structurally valid but do not have the first-principles identity.

    Returns a list of failure-message strings (empty list == valid).
    Exits with code 2 for environment-class errors (malformed YAML, non-mapping frontmatter).
    """
    import yaml

    # Phase 21-15 (CR-05): reset the executed-index collector at the top of
    # every call so a prior call's indices never leak into this one's floor.
    _EXECUTED_CHECK_INDICES.clear()

    # Check 1: file must begin with a frontmatter fence, then split into 3 parts
    if not text.startswith("---"):
        sys.stderr.write("check-agent: agent file does not begin with a frontmatter fence\n")
        sys.exit(2)
    parts = _FENCE_RE.split(text, maxsplit=2)
    if len(parts) < 3 or parts[0].strip():
        sys.stderr.write("check-agent: agent file is missing/has malformed frontmatter fences\n")
        sys.exit(2)

    fm_text = parts[1]
    body = parts[2]

    # Parse frontmatter
    try:
        frontmatter = yaml.safe_load(fm_text)
    except yaml.YAMLError as exc:
        sys.stderr.write(f"check-agent: malformed YAML in frontmatter: {exc}\n")
        sys.exit(2)

    if not isinstance(frontmatter, dict):
        got = "empty/null" if frontmatter is None else type(frontmatter).__name__
        sys.stderr.write(f"check-agent: frontmatter is not a mapping (got {got})\n")
        sys.exit(2)

    # Check 1 completed without exiting — record it unconditionally, matching
    # the comment above _CHECK_DESCRIPTIONS: index 0 is structurally required
    # to reach every later check and is never gated on n_checks.
    _EXECUTED_CHECK_INDICES.add(0)

    failures: list[str] = []
    description: object = frontmatter.get("description")
    n_checks = len(_CHECK_DESCRIPTIONS)

    # Check 2: name present and exactly "first-principles"
    if 1 < n_checks and not skip_name_check:
        _EXECUTED_CHECK_INDICES.add(1)
        name = frontmatter.get("name")
        if name is None:
            failures.append(f"frontmatter missing required key 'name'")
        elif name != _EXPECTED_NAME:
            failures.append(f"name must be '{_EXPECTED_NAME}', got '{name}'")

    # Check 3: description is a non-empty string with len <= 1024
    if 2 < n_checks:
        _EXECUTED_CHECK_INDICES.add(2)
        if description is None:
            failures.append("frontmatter missing required key 'description'")
        elif not isinstance(description, str):
            failures.append(f"'description' must be a string, got {type(description).__name__}")
        elif len(description) == 0:
            failures.append("'description' must not be empty")
        elif len(description) > _MAX_DESCRIPTION_LEN:
            failures.append(
                f"'description' length {len(description)} exceeds max {_MAX_DESCRIPTION_LEN} chars"
            )

    # Check 4: disallowedTools key present
    if 3 < n_checks:
        _EXECUTED_CHECK_INDICES.add(3)
        if "disallowedTools" not in frontmatter:
            failures.append("frontmatter missing required key 'disallowedTools'")

    # Check 5: maxTurns key present, and — for the canonical first-principles
    # identity only — carries the locked value. The value clause is scoped to
    # skip_name_check like Checks 2/8: it is an identity-specific invariant
    # (the shipped agent's Self-Audit Gate budget headroom), not a generic
    # structural schema requirement every builder-generated candidate must
    # share, so a candidate agent under a different turn budget is not
    # penalized for it.
    if 4 < n_checks:
        # Index 4 is recorded as executed exactly when the skip_name_check-
        # scoped value clause is in play (mirroring Checks 2/8's simpler
        # `and not skip_name_check` gate) — the key-presence half below always
        # runs and is not itself scoped, so it does not gate this append.
        if not skip_name_check:
            _EXECUTED_CHECK_INDICES.add(4)
        if "maxTurns" not in frontmatter:
            failures.append("frontmatter missing required key 'maxTurns'")
        elif not skip_name_check and frontmatter.get("maxTurns") != _EXPECTED_MAX_TURNS:
            failures.append(
                f"'maxTurns' must be {_EXPECTED_MAX_TURNS} (Phase 5 Self-Audit Gate "
                f"budget headroom), got {frontmatter.get('maxTurns')!r}"
            )

    # Check 6: body non-empty after strip
    if 5 < n_checks:
        _EXECUTED_CHECK_INDICES.add(5)
        if not body.strip():
            failures.append("agent file body is empty (whitespace-only after closing '---')")

    # Check 7: no unresolved sync markers in body
    if 6 < n_checks:
        _EXECUTED_CHECK_INDICES.add(6)
        markers = _MARKER_RE.findall(body)
        if markers:
            failures.append(
                f"body contains unresolved sync markers: {', '.join(markers[:5])}"
            )

    # Check 8: description must contain all four mandatory trigger phrases
    if 7 < n_checks and not skip_name_check:
        _EXECUTED_CHECK_INDICES.add(7)
        if isinstance(description, str) and len(description) > 0:
            missing = [p for p in _REQUIRED_PHRASES if p not in description.lower()]
            if missing:
                failures.append(
                    "'description' missing required trigger phrase(s): "
                    + ", ".join(f'"{p}"' for p in missing)
                )

    return failures


def _assert_live_coverage(text: str, agent_path: Path) -> None:
    """Anti-vacuity control: prove the checker engaged *this* file's content.

    GATE-01 is the only gate that validates the agent frontmatter. `claude
    plugin validate` (VAL-01) does not: it walks *subdirectories* of `agents/`
    and never validates a flat `agents/*.md`, so it inspects the 29 reference
    siblings and skips the one file that is actually an agent. Verified against
    the CLI with a minimal single-agent probe plugin — a flat `agents/solo.md`
    alone produces no `Validating agent:` line at all.

    A clean PASS therefore cannot be taken on trust: if `_check_agent_text`
    ever went vacuous, or the live leg were pointed at some other file, nothing
    downstream would notice. So mutate the frontmatter this run actually read —
    strip the `name:` key — and require the checker to report that specific
    defect. Mirrors the anti-masking negatives REG-GUARD and GATE-02-v8.5 carry,
    but runs on the live leg rather than in `--self-test`: the self-test
    fixtures are in-memory by design and never read the shipped tree, so only
    the live leg can assert this against the shipped plugin.
    """
    mutated, substitutions = _NAME_KEY_RE.subn("", text, count=1)
    if substitutions != 1:
        sys.stderr.write(
            f"check-agent: COVERAGE FAIL — could not locate a 'name:' frontmatter "
            f"key to mutate in {agent_path}; the anti-vacuity control cannot run\n"
        )
        sys.exit(1)

    control_failures = _check_agent_text(mutated)
    if not any("missing required key 'name'" in msg for msg in control_failures):
        sys.stderr.write(
            f"check-agent: COVERAGE FAIL — stripping 'name:' from {agent_path} did "
            f"not produce the expected failure; GATE-01 is passing vacuously and is "
            f"NOT validating this file\n"
        )
        sys.exit(1)


def _validate_agent_file(agent_path: Path, skip_name_check: bool = False) -> None:
    """Validate the agent file at *agent_path*. Exits non-zero on failure."""
    if not agent_path.exists():
        sys.stderr.write(
            f"check-agent: agent file not found: {agent_path}\n"
        )
        sys.exit(2)

    text = agent_path.read_text(encoding="utf-8")
    failures = _check_agent_text(text, skip_name_check=skip_name_check)

    if failures:
        for msg in failures:
            sys.stderr.write(f"check-agent: FAIL — {msg}\n")
        sys.exit(1)

    # Only the canonical agent carries the `name:` key the control mutates;
    # builder candidates run under --skip-name-check and are exempt.
    if not skip_name_check:
        _assert_live_coverage(text, agent_path)

    print(f"check-agent: COVERAGE — validated {agent_path}")
    print("check-agent: PASS")


def describe() -> dict:
    """Phase 21 (D-03/D-21-J): pure, gate-agnostic self-description backing
    GATE-01.

    `branch_count` is `len(_CHECK_DESCRIPTIONS)` — a measured read of the
    roster `_check_agent_text()` gates its checks on, not a hand-typed "8"
    beside untouched inline code. Reads module-level constants only — no
    disk I/O (AGENT_FILE's existence is not checked here), no argv, no
    subprocess.
    """
    return {
        "branch_roster": list(_CHECK_DESCRIPTIONS),
        "branch_count": len(_CHECK_DESCRIPTIONS),
        "scoped_branches": [
            _CHECK_DESCRIPTIONS[i]
            for i in _SKIP_NAME_CHECK_SCOPED_INDICES
            if i < len(_CHECK_DESCRIPTIONS)
        ],
        "locked_constants": {
            "expected_name": _EXPECTED_NAME,
            "max_description_len": _MAX_DESCRIPTION_LEN,
            "expected_max_turns": _EXPECTED_MAX_TURNS,
        },
        "checked_files": [str(AGENT_FILE.relative_to(REPO_ROOT))],
        "disclosed_bounds_anchors": ["live-coverage-anti-vacuity"],
    }


def _run_self_test() -> None:
    """Run inline malformed fixtures and verify each produces failures."""
    # Each fixture declares the substring its *intended* check must emit, so a
    # fixture cannot pass for the wrong reason (e.g. an unrelated defect firing).
    fixtures = [
        ("fixture-a (missing name)", _FIXTURE_MISSING_NAME,
         "missing required key 'name'"),
        ("fixture-b (empty body)", _FIXTURE_EMPTY_BODY,
         "body is empty"),
        ("fixture-c (unresolved sync marker)", _FIXTURE_UNRESOLVED_MARKER,
         "unresolved sync markers"),
        ("fixture-d (wrong name)", _FIXTURE_WRONG_NAME,
         f"name must be '{_EXPECTED_NAME}'"),
        ("fixture-e (over-length description)", _FIXTURE_LONG_DESCRIPTION,
         "exceeds max"),
        ("fixture-f (missing maxTurns)", _FIXTURE_MISSING_MAXTURNS,
         "missing required key 'maxTurns'"),
        ("fixture-j (wrong maxTurns value)", _FIXTURE_WRONG_MAXTURNS_VALUE,
         f"'maxTurns' must be {_EXPECTED_MAX_TURNS}"),
        ("fixture-g (missing disallowedTools)", _FIXTURE_MISSING_DISALLOWED_TOOLS,
         "missing required key 'disallowedTools'"),
        ("fixture-h (missing trigger phrase)", _FIXTURE_MISSING_TRIGGER_PHRASE,
         "missing required trigger phrase"),
    ]

    wrong_passes: list[str] = []

    for label, text, expected in fixtures:
        failures = _check_agent_text(text)
        if not failures:
            print(f"check-agent --self-test: {label} WRONGLY PASSED (expected failure)")
            wrong_passes.append(f"{label} (no failures produced)")
        elif not any(expected in f for f in failures):
            print(
                f"check-agent --self-test: {label} failed for the WRONG reason "
                f"(expected '{expected}', got: {'; '.join(failures)})"
            )
            wrong_passes.append(f"{label} (expected '{expected}')")
        else:
            print(f"check-agent --self-test: {label} correctly failed ({len(failures)} failure(s))")

    # Fixture-i: structurally valid candidate with skip_name_check=True
    # This is a "positive" fixture — expects zero failures (pass case)
    fi_failures = _check_agent_text(_FIXTURE_CANDIDATE_VALID, skip_name_check=True)
    if fi_failures:
        print(
            f"check-agent --self-test: fixture-i (valid candidate, skip_name_check) "
            f"WRONGLY FAILED ({len(fi_failures)} failure(s): {'; '.join(fi_failures)})"
        )
        wrong_passes.append("fixture-i (unexpected failures)")
    else:
        print(
            "check-agent --self-test: fixture-i (valid candidate, skip_name_check) "
            "correctly passed (0 failures)"
        )

    # Executed-check-index floor (Phase 21-15, CR-05), unconditional arm: run
    # the fully valid fixture with skip_name_check=False and assert every
    # index in _CHECK_DESCRIPTIONS was actually reached — not merely gated on
    # n_checks in the abstract.
    _check_agent_text(_FIXTURE_VALID_CANONICAL, skip_name_check=False)
    full_expected = set(range(len(_CHECK_DESCRIPTIONS)))
    full_problems = _index_roster_problems(_EXECUTED_CHECK_INDICES, full_expected)
    if full_problems:
        print(f"check-agent --self-test: index-floor (unconditional) FAIL — {'; '.join(full_problems)}")
        wrong_passes.append("index-floor-unconditional: " + "; ".join(full_problems))
    else:
        print(
            f"check-agent --self-test: index-floor (unconditional) PASS — "
            f"all {len(full_expected)} check indices reached"
        )

    # Executed-check-index floor, --skip-name-check arm: the same fixture
    # under skip_name_check=True must reach every index EXCEPT the ones
    # _SKIP_NAME_CHECK_SCOPED_INDICES declares scoped out — making that tuple
    # load-bearing rather than merely a published fact with nothing behind it.
    _check_agent_text(_FIXTURE_VALID_CANONICAL, skip_name_check=True)
    scoped_expected = full_expected - set(_SKIP_NAME_CHECK_SCOPED_INDICES)
    scoped_problems = _index_roster_problems(_EXECUTED_CHECK_INDICES, scoped_expected)
    if scoped_problems:
        print(f"check-agent --self-test: index-floor (skip-name-check) FAIL — {'; '.join(scoped_problems)}")
        wrong_passes.append("index-floor-skip-name-check: " + "; ".join(scoped_problems))
    else:
        print(
            f"check-agent --self-test: index-floor (skip-name-check) PASS — "
            f"all {len(scoped_expected)} unscoped check indices reached, "
            f"{len(_SKIP_NAME_CHECK_SCOPED_INDICES)} scoped indices correctly skipped"
        )

    # Negative arm (permanent registered control): prove _index_roster_problems
    # — the SAME helper the two floor arms above call — actually fires on a
    # synthetic mismatch and names both the missing and the extra index, so
    # the floor's own falsification machinery is itself under test.
    synthetic_expected = {0, 1, 2}
    synthetic_executed = {0, 1, 3}
    synthetic_problems = _index_roster_problems(synthetic_executed, synthetic_expected)
    synthetic_text = " ".join(synthetic_problems)
    missing_clause = synthetic_text.split("missing=", 1)[-1].split(" extra=", 1)[0] if synthetic_problems else ""
    extra_clause = synthetic_text.split("extra=", 1)[-1] if synthetic_problems else ""
    if not synthetic_problems:
        print("check-agent --self-test: index-floor negative-arm WRONGLY PASSED (expected failure)")
        wrong_passes.append("index-floor-negative-arm (no failures produced)")
    elif "2" not in missing_clause or "3" not in extra_clause:
        print(
            f"check-agent --self-test: index-floor negative-arm fired but did not "
            f"name both the missing and extra indices: {synthetic_problems!r}"
        )
        wrong_passes.append("index-floor-negative-arm (wrong indices named)")
    else:
        print(
            f"check-agent --self-test: index-floor negative-arm PASS — fires and "
            f"names both directions: {synthetic_problems!r}"
        )

    if wrong_passes:
        sys.stderr.write(
            f"check-agent --self-test: FAIL — these fixtures wrongly passed or "
            f"failed for the wrong reason: {', '.join(wrong_passes)}\n"
        )
        sys.exit(1)

    total_fixtures = len(fixtures) + 1  # + fixture-i (the skip_name_check positive case)
    total_controls = total_fixtures + 3  # + the two index-floor arms + the negative arm
    print(
        f"check-agent --self-test: PASS ({total_fixtures} fixtures, "
        f"{total_controls} controls total)"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="GATE-01: validate the generated first-principles agent surface."
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run inline malformed fixtures and verify each produces failures",
    )
    parser.add_argument(
        "--file",
        default=None,
        help=(
            "path to the agent .md file to validate "
            "(default: the shipped agent at AGENT_FILE)"
        ),
    )
    parser.add_argument(
        "--skip-name-check",
        action="store_true",
        help=(
            "skip name identity check (Check 2) and trigger-phrase check (Check 8); "
            "use for builder-generated candidate agents"
        ),
    )
    parser.add_argument(
        "--describe",
        action="store_true",
        help="Emit this script's self-description as a flat JSON blob on stdout (Phase 21).",
    )
    args = parser.parse_args()

    _require_python_version()
    _require_pyyaml()

    if args.self_test:
        _run_self_test()
        return

    if args.describe:
        print(json.dumps(describe(), indent=2, sort_keys=True))
        return

    # Default to the repo-anchored AGENT_FILE rather than requiring a caller-
    # supplied path. The battery and CI previously each passed the same relative
    # path, which made the gate cwd-sensitive and left its target silently
    # re-pointable; the constant is now the single source of truth.
    agent_path = AGENT_FILE if args.file is None else Path(args.file)

    _validate_agent_file(agent_path, skip_name_check=args.skip_name_check)


if __name__ == "__main__":
    main()
