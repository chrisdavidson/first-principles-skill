#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml>=6.0"]
# ///
"""VAL-03 gate: validate relative markdown links + backticked namespace refs.

Usage:
    python3 scripts/check-links.py

Exit codes:
    0  all links resolve and all namespace refs are valid
    1  one or more broken relative links or unknown namespace refs found
    2  environment error (Python <3.12, PyYAML missing, malformed frontmatter)

Broken-ref stderr format (one line per broken ref, ctrl-click navigable):
    BROKEN: <source-file>:<line>: <link-or-token> -> <reason>

Scan surfaces (relative link checking + namespace ref checking):
    - first-principles/skills/thinking/SKILL.md           (plugin spine)
    - first-principles/skills/thinking/references/*.md     (plugin spine appendices)
    - first-principles-thinking/SKILL.md                   (monolith spine)
    - first-principles-thinking/references/*.md            (monolith companion refs)

Scan surfaces (namespace ref checking only — not relative-link-checked):
    - first-principles/skills/*/SKILL.md  (plugin companion skills — cross-skill
      relative links use the shared/ source filename convention, not the plugin
      directory layout; relative links here are validated via the monolith surface)
    - shared/**/*.md  (source templates — per D-19-6, scanned to catch namespace
      ref typos; relative links in shared/ use the monolith filename convention)

Namespace-ref enforcement (D-19-6, open question #3):
    Strict backtick-only: bare /first-principles:name in prose is ignored.
    Only `/first-principles:name` (backtick-enclosed) is checked.

<see also> research §VAL-03 for the em-dash tokenization tangent (P6) and
    the frontmatter double-counting edge case (P1, handled via _strip_frontmatter).
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

# Path resolution: relative to this script's location, not Path.cwd() (mirrors sync-content.py).
REPO_ROOT = Path(__file__).resolve().parents[1]

# Scan globs: surfaces that receive BOTH relative-link and namespace-ref validation.
FULL_CHECK_GLOBS = [
    "first-principles/skills/thinking/SKILL.md",
    "first-principles/skills/thinking/references/*.md",
    "first-principles-thinking/SKILL.md",
    "first-principles-thinking/references/*.md",
]

# Scan globs: surfaces that receive namespace-ref validation ONLY.
# Relative links in these files use conventions valid in their source context
# (shared/ uses monolith filenames; plugin companion SKILL.md files use the
# shared/ context filenames), not the installed plugin directory layout.
NAMESPACE_ONLY_GLOBS = [
    "first-principles/skills/*/SKILL.md",
    "shared/**/*.md",
]

# Markdown link pattern: [label](target)
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

# Namespace ref pattern: backtick-enclosed /first-principles:<name> (strict per D-19-6).
NAMESPACE_RE = re.compile(r"`/first-principles:([a-z][a-z0-9-]*)`")

# Frontmatter fence (matches ^---\s*$ on its own line).
_FENCE_RE = re.compile(r"^---\s*$", re.MULTILINE)


def _require_python_version() -> None:
    if sys.version_info < (3, 12):
        sys.stderr.write(
            f"scripts/check-links.py requires Python >=3.12 "
            f"(running {sys.version_info.major}.{sys.version_info.minor}).\n"
        )
        sys.exit(2)


def _require_pyyaml() -> None:
    """Catch missing PyYAML at startup with a clear remediation message (template-consistent)."""
    try:
        import yaml  # noqa: F401
    except ImportError:
        sys.stderr.write(
            "scripts/check-links.py needs PyYAML.\n"
            "  Easiest:  uv run scripts/check-links.py\n"
            "  Or:       pip install --user 'pyyaml>=6.0'  &&  "
            "python3 scripts/check-links.py\n"
        )
        sys.exit(2)


def _strip_frontmatter(text: str) -> str:
    """Strip YAML frontmatter from markdown text; return body only.

    If the file begins with '---\\n', split on the closing fence and return
    the third chunk. Otherwise return the original text unchanged.
    Body leading newlines are preserved (byte-level fidelity, mirrors _skill_io.py).
    """
    if not text.startswith("---\n") and not text.startswith("---\r\n"):
        return text
    parts = _FENCE_RE.split(text, maxsplit=2)
    if len(parts) < 3:
        return text  # Malformed: no closing fence — return as-is.
    return parts[2]


def _collect_files(
    globs: list[str],
) -> list[Path]:
    """Expand globs against REPO_ROOT and return sorted unique paths."""
    seen: set[Path] = set()
    result: list[Path] = []
    for pattern in globs:
        for path in sorted(REPO_ROOT.glob(pattern)):
            if path not in seen:
                seen.add(path)
                result.append(path)
    return result


def _frontmatter_line_offset(full_text: str, body: str) -> int:
    """Return the number of lines consumed by frontmatter (including closing fence).

    Invariant: reported line N opens to the line containing the broken link
    in the original file.

    Computed as: number of '\\n' chars in the prefix of full_text that is not
    in body (i.e., the frontmatter block).
    """
    prefix_len = len(full_text) - len(body)
    return full_text.count("\n", 0, prefix_len)


def _resolve_link(raw_target: str, source_file: Path) -> Path:
    """Resolve a markdown link target to an absolute path.

    Strips any #fragment. Paths starting with '/' are repo-root relative;
    others are relative to the containing file's parent directory.

    URL-decode: not applied — repo doesn't use encoded paths today.
    (Deferred edge case: if encoded paths are introduced, add urllib.parse.unquote here.)
    """
    target = raw_target.split("#")[0]
    if not target:
        return source_file  # Pure anchor — no file to resolve.
    if target.startswith("/"):
        return (REPO_ROOT / target.lstrip("/")).resolve()
    return (source_file.parent / target).resolve()


def _check_file(
    source_file: Path,
    check_links: bool,
    valid_slugs: set[str],
    broken: list[tuple[Path, int, str, str]],
    total_links: list[int],
    total_refs: list[int],
) -> None:
    """Check a single file, appending any broken refs to `broken`."""
    try:
        full_text = source_file.read_text(encoding="utf-8")
    except OSError as exc:
        sys.stderr.write(f"check-links: cannot read {source_file}: {exc}\n")
        sys.exit(2)

    body = _strip_frontmatter(full_text)
    fm_offset = _frontmatter_line_offset(full_text, body)

    try:
        rel = source_file.relative_to(REPO_ROOT)
    except ValueError:
        rel = source_file

    # --- Relative markdown links (only for full-check surfaces) ---
    if check_links:
        for match in LINK_RE.finditer(body):
            raw_target = match.group(2)

            # Skip URLs, mailto:, and pure anchors.
            if raw_target.startswith(("http://", "https://", "mailto:", "#")):
                continue

            total_links[0] += 1
            resolved = _resolve_link(raw_target, source_file)

            if not resolved.exists():
                # Line number: 1-indexed, relative to original file.
                line_in_body = body[: match.start()].count("\n") + 1
                line_in_file = line_in_body + fm_offset
                broken.append((rel, line_in_file, raw_target, "file not found"))

    # --- Backticked namespace refs (all surfaces) ---
    for match in NAMESPACE_RE.finditer(body):
        name = match.group(1)
        total_refs[0] += 1

        if name not in valid_slugs:
            line_in_body = body[: match.start()].count("\n") + 1
            line_in_file = line_in_body + fm_offset
            broken.append(
                (rel, line_in_file, f"`/first-principles:{name}`",
                 "unknown namespace ref (not a sibling skill)")
            )


def main() -> int:
    _require_python_version()
    _require_pyyaml()

    # Import _skill_io for PLUGIN_SKILLS_DIR and the valid slug set.
    sys.path.insert(0, str(Path(__file__).parent))
    try:
        import _skill_io
    except Exception as exc:
        sys.stderr.write(f"check-links: failed to import _skill_io: {exc}\n")
        sys.exit(2)

    # Build valid namespace-ref slug set at runtime (not hard-coded — Phase 20+ safe).
    try:
        valid_slugs: set[str] = {
            name
            for name in os.listdir(_skill_io.PLUGIN_SKILLS_DIR)
            if (_skill_io.PLUGIN_SKILLS_DIR / name / "SKILL.md").exists()
        }
    except Exception as exc:
        sys.stderr.write(f"check-links: cannot enumerate plugin skills: {exc}\n")
        sys.exit(2)

    full_check_files = _collect_files(FULL_CHECK_GLOBS)
    namespace_only_files = _collect_files(NAMESPACE_ONLY_GLOBS)

    # Deduplicate: files in full_check_files should not also appear in namespace_only_files.
    full_check_set = set(full_check_files)
    namespace_only_files = [f for f in namespace_only_files if f not in full_check_set]

    broken: list[tuple[Path, int, str, str]] = []
    total_links: list[int] = [0]
    total_refs: list[int] = [0]

    for source_file in full_check_files:
        _check_file(source_file, True, valid_slugs, broken, total_links, total_refs)

    for source_file in namespace_only_files:
        _check_file(source_file, False, valid_slugs, broken, total_links, total_refs)

    total_files = len(full_check_files) + len(namespace_only_files)

    # --- Report ---
    if broken:
        # Sort by (source file path string, line number) for consistent output.
        broken.sort(key=lambda t: (str(t[0]), t[1]))
        for rel, line, ref, reason in broken:
            sys.stderr.write(f"BROKEN: {rel}:{line}: {ref} -> {reason}\n")
        sys.exit(1)

    print(
        f"check-links: PASS ({total_links[0]} markdown links + {total_refs[0]} namespace refs"
        f" across {total_files} files)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
