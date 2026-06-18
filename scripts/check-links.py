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

Scan surfaces (docs/ cross-doc link checking — D-04, DOCTOOL-01):
    - docs/*.md  (user-facing documentation; relative cross-doc links + anchor
      validation via github-slugger rule; docs/-prefixed links flagged as CF-04
      violations; docs/history/** excluded — frozen archives)

Namespace-ref enforcement (D-19-6, open question #3):
    Strict backtick-only: bare /first-principles:name in prose is ignored.
    Only `/first-principles:name` (backtick-enclosed) is checked.

Anchor validation (docs/ surface only, D-04):
    Per-space github-slugger rule: lowercase, strip punctuation (incl. em-dash),
    replace EACH remaining space individually with a hyphen (no collapsing).
    Em-dash headings produce double-hyphen anchors, e.g.:
      '## CI gates — operational run-detail' -> '#ci-gates--operational-run-detail'

<see also> research §VAL-03 for the em-dash tokenization tangent (P6) and
    the frontmatter double-counting edge case (P1, handled via _strip_frontmatter).
"""

from __future__ import annotations

import os
import re
import sys
import unicodedata
from pathlib import Path

# Path resolution: relative to this script's location, not Path.cwd() (mirrors sync-content.py).
REPO_ROOT = Path(__file__).resolve().parents[1]

# Scan globs: surfaces that receive BOTH relative-link and namespace-ref validation.
# Phase 26.1 adds the agent surface — first-principles.md is the agent spine and
# references/*.md its companion files. references/examples/ is illustrative
# content (worked examples), NOT link-checked source.
#
# Phase 26.1 Plan 04 deviation (Rule 3, in-scope): monolith + plugin-spine
# entries removed for the same "dead config after Plan 05" reason as the
# NAMESPACE_ONLY_GLOBS plugin-skill entry. Reconciling shared/ link targets
# with the agent tree's short-slug reference filenames (second-order.md,
# trade-off.md) — required to make the agent surface link-check clean —
# would otherwise leave the monolith's long-slug filenames
# (second-order-thinking.md, trade-off-analysis.md) unable to resolve those
# same links. Both trees are deleted in Plan 05; pruning now is dead-config
# cleanup, not coverage loss.
FULL_CHECK_GLOBS = [
    "first-principles/agents/first-principles.md",
    "first-principles/agents/references/*.md",
]

# Scan globs: surfaces that receive namespace-ref validation ONLY.
# Relative links in these files use conventions valid in their source context
# (shared/ uses monolith filenames), not the installed plugin directory layout.
# Phase 26.1: removed `first-principles/skills/*/SKILL.md` — Plan 05 deletes
# that tree, after which the glob would match zero files (dead config).
NAMESPACE_ONLY_GLOBS = [
    "shared/**/*.md",
]

# Scan globs: docs/ surface — relative cross-doc links + anchor validation (D-04).
# docs/history/** is excluded: frozen per-milestone archives with stale links that
# are intentionally not gated (per REQUIREMENTS Out-of-Scope).
DOCS_CHECK_GLOBS = [
    "docs/*.md",
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


def _github_slug(heading: str) -> str:
    """Convert an ATX Markdown heading to a github-slugger anchor slug.

    Algorithm (per github-slugger v1/v2, D-04):
      1. Strip leading '#' characters and surrounding whitespace.
      2. Lowercase.
      3. Remove every character that is NOT an ASCII letter, ASCII digit,
         a space (' '), or a hyphen ('-'). This strips punctuation including
         em-dash (U+2014), colons, parentheses, backticks, slashes, periods,
         and all other Unicode non-alphanumeric characters.
      4. Replace EACH remaining space individually with one hyphen — do NOT
         collapse runs of spaces. This is the load-bearing rule: an em-dash
         '—' between two spaces leaves two spaces after step 3, which become
         two consecutive hyphens in step 4:
             '## CI gates — operational run-detail'
             -> 'ci gates  operational run-detail'  (two spaces)
             -> 'ci-gates--operational-run-detail'  (double hyphen)

    Do NOT use re.sub(r'\\s+', '-', ...) — that collapses multi-space runs
    into a single hyphen and false-positives every em-dash heading (the exact
    bug in the P99 orchestrator's first resolver, per D-04).
    """
    # Strip leading '#' marks and surrounding whitespace.
    text = heading.lstrip("#").strip()
    # Lowercase.
    text = text.lower()
    # Remove all non-ASCII-alphanumeric, non-space, non-hyphen characters.
    # unicodedata.category helps but a simple keep-list is clearer and correct.
    kept: list[str] = []
    for ch in text:
        if ch == " " or ch == "-" or ("a" <= ch <= "z") or ("0" <= ch <= "9"):
            kept.append(ch)
    # Per-space replacement: each space → one hyphen (no collapse).
    return "".join("-" if ch == " " else ch for ch in kept)


# ATX heading pattern: one or more '#' at line start followed by text.
_ATX_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)


def _doc_anchors(path: Path) -> set[str]:
    """Return the set of heading-slug anchors defined in a Markdown doc.

    Reads the file at `path`, strips frontmatter, and slugs every ATX heading
    via _github_slug. Inline HTML anchors (<a name="...">) are NOT collected —
    the docs/ surface uses only ATX headings for navigation (D-04).
    """
    try:
        full_text = path.read_text(encoding="utf-8")
    except OSError:
        return set()
    body = _strip_frontmatter(full_text)
    return {_github_slug(m.group(0)) for m in _ATX_HEADING_RE.finditer(body)}


def _check_docs_file(
    source_file: Path,
    docs_dir: Path,
    broken: list[tuple[Path, int, str, str]],
    total_links: list[int],
    total_refs: list[int],
) -> None:
    """Check one docs/ file for broken relative cross-doc links (D-04, DOCTOOL-01).

    Validation rules:
      1. A link target beginning with 'docs/' is flagged BROKEN — it would
         resolve relative to docs/ as docs/docs/X.md (a 404). The correct form
         is the bare filename (CF-04).
      2. A bare-filename '.md' link (e.g. 'TESTING.md' or 'TESTING.md#anchor')
         is resolved relative to the source file's parent (which is docs/).
         If the file does not exist → BROKEN (file not found).
         If a '#anchor' is present and does not match any heading slug → BROKEN.
      3. A pure '#anchor' link (no file component) validates against the source
         file's own headings.
      4. URL links (http://, https://, mailto:) and links to ../ paths are skipped.
    """
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

    # Heading slugs for this source file (used for pure-anchor validation).
    source_anchors: set[str] | None = None

    for match in LINK_RE.finditer(body):
        raw_target = match.group(2)

        # Skip URLs and mailto.
        if raw_target.startswith(("http://", "https://", "mailto:")):
            continue

        # Line number (1-indexed, relative to original file).
        line_in_body = body[: match.start()].count("\n") + 1
        line_in_file = line_in_body + fm_offset

        # --- Rule 1: docs/-prefixed link (CF-04 violation) ---
        if raw_target.startswith("docs/"):
            total_links[0] += 1
            broken.append((
                rel,
                line_in_file,
                raw_target,
                (
                    "docs/-prefixed link resolves to docs/docs/... (404); "
                    "use bare filename (CF-04)"
                ),
            ))
            continue

        # --- Pure anchor (no file component): validate against own headings ---
        if raw_target.startswith("#"):
            total_links[0] += 1
            anchor = raw_target[1:]
            if source_anchors is None:
                source_anchors = _doc_anchors(source_file)
            if anchor not in source_anchors:
                broken.append((
                    rel,
                    line_in_file,
                    raw_target,
                    f"anchor #{anchor} not found in {source_file.name}",
                ))
            continue

        # --- Skip non-.md links and relative-up paths (../) ---
        file_part = raw_target.split("#")[0]
        if not file_part.endswith(".md"):
            continue
        if file_part.startswith("../") or file_part == "..":
            continue

        total_links[0] += 1

        # --- Resolve bare-filename link relative to docs/ ---
        target_path = (source_file.parent / file_part).resolve()

        if not target_path.exists():
            broken.append((rel, line_in_file, raw_target, "file not found"))
            continue

        # --- Validate anchor (if present) ---
        if "#" in raw_target:
            anchor = raw_target.split("#", 1)[1]
            if anchor:  # Non-empty anchor
                target_anchors = _doc_anchors(target_path)
                if anchor not in target_anchors:
                    broken.append((
                        rel,
                        line_in_file,
                        raw_target,
                        (
                            f"anchor #{anchor} not found in {target_path.name} "
                            f"(heading anchors: {sorted(target_anchors)[:5]}...)"
                            if len(target_anchors) > 5
                            else f"anchor #{anchor} not found in {target_path.name} "
                            f"(heading anchors: {sorted(target_anchors)})"
                        ),
                    ))


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
    # Phase 26.1: tolerate missing first-principles/skills/ (Plan 05 deletes it)
    # AND include the agent's namespace token `first-principles` whenever the
    # agent file exists (so `/first-principles:first-principles` references in
    # the agent body resolve cleanly).
    valid_slugs: set[str] = set()
    if _skill_io.PLUGIN_SKILLS_DIR.exists():
        try:
            valid_slugs |= {
                name
                for name in os.listdir(_skill_io.PLUGIN_SKILLS_DIR)
                if (_skill_io.PLUGIN_SKILLS_DIR / name / "SKILL.md").exists()
            }
        except Exception as exc:
            sys.stderr.write(f"check-links: cannot enumerate plugin skills: {exc}\n")
            sys.exit(2)

    if (REPO_ROOT / "first-principles" / "agents" / "first-principles.md").exists():
        valid_slugs.add("first-principles")

    full_check_files = _collect_files(FULL_CHECK_GLOBS)
    namespace_only_files = _collect_files(NAMESPACE_ONLY_GLOBS)
    docs_files = _collect_files(DOCS_CHECK_GLOBS)

    # Deduplicate: files in full_check_files should not also appear in namespace_only_files.
    full_check_set = set(full_check_files)
    namespace_only_files = [f for f in namespace_only_files if f not in full_check_set]

    # docs/ scan uses a separate docs_dir root for CF-04 prefix detection.
    docs_dir = REPO_ROOT / "docs"

    broken: list[tuple[Path, int, str, str]] = []
    total_links: list[int] = [0]
    total_refs: list[int] = [0]

    for source_file in full_check_files:
        _check_file(source_file, True, valid_slugs, broken, total_links, total_refs)

    for source_file in namespace_only_files:
        _check_file(source_file, False, valid_slugs, broken, total_links, total_refs)

    for source_file in docs_files:
        _check_docs_file(source_file, docs_dir, broken, total_links, total_refs)

    total_files = len(full_check_files) + len(namespace_only_files) + len(docs_files)

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
