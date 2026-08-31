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
_REQUIRED_PHRASES = [
    "first principles",
    "challenge assumptions",
    "reason from ground truth",
    "decompose this problem",
]

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

    failures: list[str] = []

    # Check 2: name present and exactly "first-principles"
    if not skip_name_check:
        name = frontmatter.get("name")
        if name is None:
            failures.append(f"frontmatter missing required key 'name'")
        elif name != _EXPECTED_NAME:
            failures.append(f"name must be '{_EXPECTED_NAME}', got '{name}'")

    # Check 3: description is a non-empty string with len <= 1024
    description = frontmatter.get("description")
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
    if "disallowedTools" not in frontmatter:
        failures.append("frontmatter missing required key 'disallowedTools'")

    # Check 5: maxTurns key present
    if "maxTurns" not in frontmatter:
        failures.append("frontmatter missing required key 'maxTurns'")

    # Check 6: body non-empty after strip
    if not body.strip():
        failures.append("agent file body is empty (whitespace-only after closing '---')")

    # Check 7: no unresolved sync markers in body
    markers = _MARKER_RE.findall(body)
    if markers:
        failures.append(
            f"body contains unresolved sync markers: {', '.join(markers[:5])}"
        )

    # Check 8: description must contain all four mandatory trigger phrases
    if not skip_name_check:
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

    if wrong_passes:
        sys.stderr.write(
            f"check-agent --self-test: FAIL — these fixtures wrongly passed or "
            f"failed for the wrong reason: {', '.join(wrong_passes)}\n"
        )
        sys.exit(1)

    print("check-agent --self-test: PASS")


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
    args = parser.parse_args()

    _require_python_version()
    _require_pyyaml()

    if args.self_test:
        _run_self_test()
        return

    # Default to the repo-anchored AGENT_FILE rather than requiring a caller-
    # supplied path. The battery and CI previously each passed the same relative
    # path, which made the gate cwd-sensitive and left its target silently
    # re-pointable; the constant is now the single source of truth.
    agent_path = AGENT_FILE if args.file is None else Path(args.file)

    _validate_agent_file(agent_path, skip_name_check=args.skip_name_check)


if __name__ == "__main__":
    main()
