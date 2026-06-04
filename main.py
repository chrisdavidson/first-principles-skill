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
    2  environment error (Python <3.12, PyYAML missing)
"""

from __future__ import annotations

import string
import sys
from pathlib import Path

_MAX_DESCRIPTION_LEN = 1024

REPO_ROOT: Path = Path(__file__).resolve().parent
TEMPLATES_DIR: Path = REPO_ROOT / "templates"
GENERATED_DIR: Path = REPO_ROOT / "generated"


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


def _prompt_nonempty(label: str) -> str:
    """Prompt for a required non-empty field; re-prompts if blank."""
    while True:
        value = input(f"{label}: ").strip()
        if value:
            return value
        sys.stderr.write(f"{label} is required and cannot be empty.\n")


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
    return slug or "untitled"


def _render_and_write(
    artifact_type: str,
    name: str,
    description: str,
    trigger_phrases: list[str],
) -> None:
    """Render the selected template and write the candidate file to generated/."""
    slug = _slug(name)
    out_path = GENERATED_DIR / f"{slug}.md"

    # Select template
    tmpl_name = "skill.md.tmpl" if artifact_type == "skill" else "agent.md.tmpl"
    tmpl_path = TEMPLATES_DIR / tmpl_name
    if not tmpl_path.exists():
        sys.stderr.write(f"Template not found: {tmpl_path}\n")
        sys.exit(1)
    template_text = tmpl_path.read_text(encoding="utf-8")

    # Build substitution mapping
    version = "0.1.0"
    mapping: dict[str, str] = {
        "name": name,
        "description": description,
        "version": version,
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
            return

    # Write output
    try:
        out_path.write_text(rendered, encoding="utf-8")
    except OSError as exc:
        sys.stderr.write(f"Write error: {exc}\n")
        sys.exit(1)

    print(f"Wrote {out_path}")


def main() -> None:
    _require_python_version()
    _require_pyyaml()

    GENERATED_DIR.mkdir(exist_ok=True)

    artifact_type = _prompt_artifact_type()
    name = _prompt_nonempty("Name")
    description = _prompt_description()

    trigger_phrases: list[str] = []
    if artifact_type == "skill":
        trigger_phrases = _prompt_trigger_phrases()

    _render_and_write(artifact_type, name, description, trigger_phrases)


if __name__ == "__main__":
    main()
