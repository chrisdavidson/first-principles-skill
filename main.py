#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml>=6.0"]
# ///
"""Interactive builder: generate a candidate SKILL.md or agent .md from templates.

Usage:
    python3 main.py
    uv run main.py

Exit codes:
    0  normal completion
    1  user aborted / file write error
    2  environment error (Python <3.12)
"""

from __future__ import annotations

import argparse
import re
import string
import subprocess
import sys
from pathlib import Path

_MAX_DESCRIPTION_LEN = 1024
_DEFAULT_VERSION = "0.1.0"
_RESERVED_NAME_WORDS = frozenset({"anthropic", "claude"})

# Description budget cap (D-19-8 — mirrors CAP constant in scripts/check-description-budget.py)
_DESCRIPTION_BUDGET_CAP = 2000

# YAML frontmatter fence pattern (mirrors scripts/_skill_io.py _FENCE_RE)
_FENCE_RE = re.compile(r"^---\s*$", re.MULTILINE)

REPO_ROOT: Path = Path(__file__).resolve().parent
TEMPLATES_DIR: Path = REPO_ROOT / "templates"
GENERATED_DIR: Path = REPO_ROOT / "generated"
PLUGIN_SKILLS_DIR: Path = REPO_ROOT / "first-principles" / "skills"
SHARED_SKILLS_DIR: Path = REPO_ROOT / "shared" / "skills"
SHARED_AGENT_DIR: Path = REPO_ROOT / "shared" / "agent"


def _require_python_version() -> None:
    if sys.version_info < (3, 12):
        sys.stderr.write(
            f"main.py requires Python >=3.12 "
            f"(running {sys.version_info.major}.{sys.version_info.minor}).\n"
        )
        sys.exit(2)


def _require_pyyaml() -> None:
    """Catch missing PyYAML at startup with a clear remediation message."""
    try:
        import yaml  # noqa: F401
    except ImportError:
        sys.stderr.write(
            "main.py needs PyYAML.\n"
            "  Easiest:  uv run main.py\n"
            "  Or:       pip install --user 'pyyaml>=6.0'  &&  python3 main.py\n"
        )
        sys.exit(2)


def _parse_args() -> argparse.Namespace:
    """Parse CLI arguments and return the resulting Namespace."""
    parser = argparse.ArgumentParser(
        description="Interactive builder: generate a candidate SKILL.md or agent .md."
    )
    parser.add_argument(
        "--install",
        action="store_true",
        help="Copy to shared/ and regenerate plugin surface",
    )
    return parser.parse_args()


def _prompt_artifact_type() -> str:
    """Prompt the user to select artifact type; loops until a valid choice is given."""
    print("Select artifact type:")
    print("  1) skill")
    print("  2) agent")
    while True:
        choice = input("Choice: ").strip().lower()
        if choice in ("1", "skill"):
            return "skill"
        if choice in ("2", "agent"):
            return "agent"
        sys.stderr.write("Invalid choice. Enter 1 or skill, or 2 or agent.\n")


def _prompt_name() -> str:
    """Prompt for a skill/agent name; rejects reserved words."""
    while True:
        value = input("Name: ").strip()
        if not value:
            sys.stderr.write("Name is required and cannot be empty.\n")
            continue
        lower = value.lower()
        if any(word in lower for word in _RESERVED_NAME_WORDS):
            sys.stderr.write(
                f"Name cannot contain reserved words: "
                f"{', '.join(sorted(_RESERVED_NAME_WORDS))}.\n"
            )
            continue
        return value


def _prompt_description() -> str:
    """Prompt for a description; re-prompts if empty or over 1024 chars."""
    while True:
        value = input("Description: ").strip()
        if not value:
            sys.stderr.write("Description is required and cannot be empty.\n")
            continue
        if len(value) > _MAX_DESCRIPTION_LEN:
            sys.stderr.write(
                f"Description is {len(value)} chars; maximum is {_MAX_DESCRIPTION_LEN}.\n"
            )
            continue
        return value


def _prompt_trigger_phrases() -> list[str]:
    """Prompt for trigger phrases one per line; blank line ends the list."""
    print("Enter trigger phrases (blank line to finish):")
    phrases: list[str] = []
    while True:
        line = input("  > ").strip()
        if not line:
            break
        phrases.append(line)
    print(f"Done. {len(phrases)} phrases captured.")
    return phrases


def _slug(name: str) -> str:
    """Derive a safe output filename slug: lowercase, spaces to hyphens, strip path separators."""
    slug = name.lower().replace(" ", "-")
    # Strip any path-separator characters to prevent path traversal (T-58-03)
    slug = slug.replace("/", "").replace("\\", "").replace("..", "")
    # Remove any remaining characters that are not alphanumeric, hyphen, or underscore
    slug = "".join(c for c in slug if c.isalnum() or c in "-_")
    # Strip leading/trailing separator chars so inputs like "---" don't produce a bare-separator slug
    slug = slug.strip("-_")
    return slug or "untitled"


def _render_and_write(
    artifact_type: str,
    name: str,
    description: str,
    trigger_phrases: list[str],
) -> Path | None:
    """Render the selected template and write the candidate file to generated/.

    Returns the written Path on success, or None if the user declined the overwrite prompt.
    """
    slug = _slug(name)
    out_path = GENERATED_DIR / f"{slug}.md"

    # Select template
    tmpl_name = "skill.md.tmpl" if artifact_type == "skill" else "agent.md.tmpl"
    tmpl_path = TEMPLATES_DIR / tmpl_name
    if not tmpl_path.exists():
        sys.stderr.write(f"Template not found: {tmpl_path}\n")
        sys.exit(1)
    template_text = tmpl_path.read_text(encoding="utf-8")

    # Build substitution mapping.
    # name in frontmatter must equal the parent directory name (the slug) per
    # the plugin invariant in CLAUDE.md. The human-readable display name is
    # kept as a separate key for use in the H1 heading.
    mapping: dict[str, str] = {
        "name": slug,
        "display_name": name,
        "description": description,
        "version": _DEFAULT_VERSION,
    }
    if artifact_type == "skill":
        if trigger_phrases:
            mapping["trigger_phrases"] = "\n".join(f"- {p}" for p in trigger_phrases)
        else:
            mapping["trigger_phrases"] = "<!-- TODO: add trigger phrases -->"

    # Render with strict substitution (missing markers fail loudly — D-08)
    rendered = string.Template(template_text).substitute(mapping)

    # Overwrite guard (D-06)
    if out_path.exists():
        answer = input(
            f"generated/{out_path.name} already exists. Overwrite? [y/N] "
        ).strip().lower()
        if answer != "y":
            print("Aborted.")
            return None

    # Write output
    try:
        out_path.write_text(rendered, encoding="utf-8")
    except OSError as exc:
        sys.stderr.write(f"Write error: {exc}\n")
        sys.exit(1)

    print(f"Wrote {out_path}")
    return out_path


def _check_description_budget(candidate_path: Path) -> tuple[bool, str]:
    """Check that the candidate skill description fits within the 2000-char budget.

    Mirrors scripts/check-description-budget.py algorithm (D-01/CLI-04).
    Returns (True, "N/2000 chars") on pass, (False, "description N chars; over by M chars") on fail.
    """
    import yaml  # lazy import — pyyaml declared in PEP 723 header
    text = candidate_path.read_text(encoding="utf-8")
    parts = _FENCE_RE.split(text, maxsplit=2)
    fm = yaml.safe_load(parts[1]) if len(parts) >= 3 else {}
    fm = fm or {}   # guard: yaml.safe_load returns None for empty frontmatter
    desc: str = fm.get("description", "") or ""
    wtu: str = fm.get("when_to_use", "") or ""
    surface = f"{desc} {wtu}" if wtu else desc
    n = len(surface)
    if n > _DESCRIPTION_BUDGET_CAP:
        return False, f"description {n} chars; over by {n - _DESCRIPTION_BUDGET_CAP} chars"
    return True, f"{n}/{_DESCRIPTION_BUDGET_CAP} chars"


def _tokens(s: str) -> list[str]:
    """Tokenize per D-19-7: lowercase + \\W+ split, drop empties.

    Mirrors tokens() from scripts/check-trigger-collisions.py verbatim.
    """
    return [t for t in re.split(r"\W+", s.lower()) if t]


def _ngrams(toks: list[str], n: int = 4) -> set[tuple[str, ...]]:
    """Return all contiguous n-grams from a token list.

    Mirrors ngrams() from scripts/check-trigger-collisions.py verbatim.
    """
    return {tuple(toks[i : i + n]) for i in range(len(toks) - n + 1)}


def _check_trigger_collisions(candidate_path: Path) -> tuple[bool, str]:
    """Check for 4-gram collisions between candidate description and installed skills.

    Mirrors scripts/check-trigger-collisions.py algorithm (D-02/CLI-05).
    Compares candidate against first-principles/skills/*/SKILL.md only — never
    includes the candidate's own generated/ path (Pitfall 4).
    Returns (True, "no 4-gram collisions") on pass,
            (False, "4-gram collision with '<slug>': <gram words>") on fail.
    """
    import yaml  # lazy import — pyyaml declared in PEP 723 header
    text = candidate_path.read_text(encoding="utf-8")
    parts = _FENCE_RE.split(text, maxsplit=2)
    fm = yaml.safe_load(parts[1]) if len(parts) >= 3 else {}
    fm = fm or {}   # guard: yaml.safe_load returns None for empty frontmatter
    cand_desc: str = fm.get("description", "") or ""
    cand_wtu: str = fm.get("when_to_use", "") or ""
    cand_surface = f"{cand_desc} {cand_wtu}" if cand_wtu else cand_desc
    cand_grams = _ngrams(_tokens(cand_surface))

    collisions: list[str] = []
    if PLUGIN_SKILLS_DIR.exists():
        for skill_dir in sorted(PLUGIN_SKILLS_DIR.iterdir()):
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.exists():
                continue
            slug = skill_dir.name
            st = skill_md.read_text(encoding="utf-8")
            sparts = _FENCE_RE.split(st, maxsplit=2)
            sfm = yaml.safe_load(sparts[1]) if len(sparts) >= 3 else {}
            sfm = sfm or {}   # guard: yaml.safe_load returns None for empty frontmatter
            sdesc: str = sfm.get("description", "") or ""
            swtu: str = sfm.get("when_to_use", "") or ""
            ssurface = f"{sdesc} {swtu}" if swtu else sdesc
            hits = cand_grams & _ngrams(_tokens(ssurface))
            for gram in sorted(hits):
                collisions.append(f"'{slug}': {' '.join(gram)}")

    if collisions:
        return False, "4-gram collision with " + "; ".join(collisions)
    return True, "no 4-gram collisions"


def _check_agent_subprocess(candidate_path: Path) -> tuple[bool, str]:
    """Run scripts/check-agent.py --file on the candidate agent file via subprocess.

    Uses sys.executable per D-05. Filters output for FAIL/ERROR lines per D-09.
    Returns (True, "all checks passed") on pass,
            (False, "<fail detail>") on fail.
    """
    result = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "check-agent.py"),
            "--file",
            str(candidate_path),
            "--skip-name-check",
        ],
        capture_output=True,
        text=True,
    )
    combined = result.stdout + result.stderr
    fail_lines = [
        line for line in combined.splitlines()
        if "FAIL" in line or "ERROR" in line
    ]
    if result.returncode == 0:
        return True, "all checks passed"
    detail = "; ".join(fail_lines) if fail_lines else f"exit {result.returncode}"
    return False, detail


def _run_validation(artifact_type: str, candidate_path: Path) -> bool:
    """Print a structured pass/fail validation report for the generated candidate.

    Validation is advisory — this function never calls sys.exit() (D-06/D-07).
    For skill artifacts: runs description-budget and trigger-collision checks.
    For agent artifacts: runs check-agent.py via subprocess.
    Output format per D-08/D-10: blank line separator, one line per check.
    Returns True if all checks pass, False if any check fails.
    """
    print()  # blank-line separator per D-10
    print("Validation:")
    all_passed = True
    if artifact_type == "skill":
        ok, detail = _check_description_budget(candidate_path)
        if not ok:
            all_passed = False
        status = "PASS" if ok else "FAIL"
        suffix = f"({detail})" if ok else f"— {detail}"
        print(f"  check-description-budget: {status} {suffix}")

        ok, detail = _check_trigger_collisions(candidate_path)
        if not ok:
            all_passed = False
        status = "PASS" if ok else "FAIL"
        suffix = f"({detail})" if ok else f"— {detail}"
        print(f"  check-trigger-collisions: {status} {suffix}")
    else:  # agent
        ok, detail = _check_agent_subprocess(candidate_path)
        if not ok:
            all_passed = False
        status = "PASS" if ok else "FAIL"
        suffix = f"({detail})" if ok else f"— {detail}"
        print(f"  check-agent: {status} {suffix}")
    # No sys.exit() — validation is advisory per D-06/D-07
    return all_passed


def _install(artifact_type: str, candidate_path: Path, *, install: bool) -> None:
    """Copy the generated candidate to the correct shared/ destination.

    When install=False, returns immediately (no-op; preserves v4.0 advisory behavior).
    When install=True:
      1. Runs validation as a hard gate — aborts with exit 1 if any check fails (INST-05).
      2. Derives the destination path from artifact_type:
           skill → shared/skills/<slug>/SKILL.md (INST-01)
           agent → shared/agent/<slug>.md (INST-02)
      3. Conflict guard — aborts with exit 1 if the destination file already exists (INST-03).
         A pre-existing parent directory without the target file is not a conflict.
      4. Creates the parent directory as needed (mkdir -p).
      5. Copies via write_text/read_text only — no new imports (D-06).
    """
    if not install:
        return

    slug = candidate_path.stem

    if not _run_validation(artifact_type, candidate_path):
        sys.stderr.write("Install aborted: validation failed.\n")
        sys.exit(1)

    if artifact_type == "skill":
        dest_path = SHARED_SKILLS_DIR / slug / "SKILL.md"
    else:  # agent
        dest_path = SHARED_AGENT_DIR / f"{slug}.md"

    if dest_path.exists():
        sys.stderr.write(
            f"Install aborted: {dest_path.relative_to(REPO_ROOT)} already exists.\n"
        )
        sys.exit(1)

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_text(candidate_path.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"Installed {dest_path.relative_to(REPO_ROOT)}")
    _sync_content(dest_path)


def _sync_content(dest_path: Path) -> None:
    """Invoke scripts/sync-content.py --write after a successful install write.

    On success (returncode == 0): returns normally with no output.
    On failure (non-zero returncode):
      1. Deletes dest_path (rollback — OSError propagates as traceback if delete fails).
      2. Writes subprocess stdout to sys.stderr if non-empty (diagnostic output first).
      3. Writes subprocess stderr verbatim to sys.stderr (root cause).
      4. Writes a rollback notice line to sys.stderr.
      5. Calls sys.exit(1).
    """
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "sync-content.py"), "--write"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        dest_path.unlink(missing_ok=True)
        if result.stdout:
            sys.stderr.write(result.stdout)
        sys.stderr.write(result.stderr)
        sys.stderr.write(
            f"Rolled back: deleted {dest_path.relative_to(REPO_ROOT)}\n"
            "Warning: generated/ tree may be partially updated; "
            "run 'python3 scripts/sync-content.py --write' to repair.\n"
        )
        sys.exit(1)


def main() -> None:
    _require_python_version()
    _require_pyyaml()
    args = _parse_args()

    GENERATED_DIR.mkdir(exist_ok=True)

    try:
        artifact_type = _prompt_artifact_type()
        name = _prompt_name()
        description = _prompt_description()

        trigger_phrases: list[str] = []
        if artifact_type == "skill":
            trigger_phrases = _prompt_trigger_phrases()

        candidate_path = _render_and_write(artifact_type, name, description, trigger_phrases)
        if candidate_path is not None:
            if not args.install:
                _run_validation(artifact_type, candidate_path)
            _install(artifact_type, candidate_path, install=args.install)
    except (EOFError, KeyboardInterrupt):
        sys.stderr.write("\nAborted.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
