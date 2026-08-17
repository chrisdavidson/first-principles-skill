#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml>=6.0"]
# ///
"""VAL-03 gate: validate relative markdown links + backticked namespace refs.

Usage:
    python3 scripts/check-links.py [--self-test]

Exit codes:
    0  all links resolve and all namespace refs are valid (or --self-test PASS)
    1  one or more broken relative links or unknown namespace refs found
       (or --self-test FAIL)
    2  environment error (Python <3.12, PyYAML missing, malformed frontmatter)

--self-test (v8.5 GATE-01, D-03/D-04): builds an on-disk temp fixture and
drives the production _collect_files / _check_file functions against it to
prove the two newly-extended scan surfaces above are load-bearing —
non-vacuity, disjointness, positive detection + negative controls on both
axes, and run-to-run determinism. Does not require PyYAML or _skill_io.

Broken-ref stderr format (one line per broken ref, ctrl-click navigable):
    BROKEN: <source-file>:<line>: <link-or-token> -> <reason>

Scan surfaces (relative link checking + namespace ref checking):
    - first-principles/agents/first-principles.md          (agent spine)
    - first-principles/agents/references/*.md              (agent companion refs)
    - first-principles/skills/*/references/*.md            (v8.5 GATE-01 — skill-stub
      companion refs; D-01. This glob matches ZERO files on the tree today —
      Phase 154 is what creates skills/*/references/. A vacuously-clean live
      scan of this surface is NOT an error; the gate's teeth come from the
      inline `--self-test` fixture below until real files land.)

Scan surfaces (namespace ref checking only — not relative-link-checked):
    - first-principles/skills/*/SKILL.md  (plugin companion skills — restored
      per D-05. Namespace-only, NOT full-check, because 12 pre-existing
      cross-skill relative links in these stubs use the shared/ source
      filename convention rather than the plugin directory layout — e.g.
      `[5-Whys](five-whys.md)` in fishbone/SKILL.md does not resolve under
      first-principles/skills/fishbone/. D-02 defers fixing those links; this
      restoration only re-enables the namespace-ref axis, which today finds
      zero backticked namespace refs in any stub — also vacuous, per D-06.
      The inline `--self-test` fixture is what proves this axis load-bearing
      in the meantime. Count history (v8.5 Phase 154, D-17): was 14
      pre-existing cross-skill links; Plan 154-02's split moved 2 of
      fishbone's (its Failure modes and Handoff sections) into
      fishbone-detail.md, converting them to namespace refs and dropping the
      live count in these SKILL.md files to 12. A raw relative-link scan of
      this glob now also matches 4 new, correctly-resolving
      `references/<slug>-detail.md` on-demand-load pointers Plan 154-03
      introduced (16 relative-link matches total) — those 4 are NOT part of
      the non-resolving count this namespace-only decision is about; the
      FULL_CHECK_GLOBS entry above already full-checks them via
      first-principles/skills/*/references/*.md.)
    - shared/**/*.md  (source templates — per D-19-6, scanned to catch namespace
      ref typos; relative links in shared/ use the monolith filename convention)

Honesty note (D-06): both newly-added scan surfaces above —
first-principles/skills/*/references/*.md and first-principles/skills/*/SKILL.md
— currently match zero live findings (the former glob matches zero files at
all; the latter matches files but finds zero backticked namespace refs in
them). A vacuously-clean live scan of either surface is NOT an error and does
NOT mean the extension is a no-op: the `--self-test` mode proves both globs
are wired to the production `_collect_files` / `_check_file` functions and
will fire correctly the moment real content lands (Phase 154 for the first,
any future skill-stub cross-ref for the second).

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

import argparse
import contextlib
import io
import os
import re
import sys
import tempfile
import unicodedata
from pathlib import Path

# Path resolution: relative to this script's location, not Path.cwd() (mirrors sync-content.py).
REPO_ROOT = Path(__file__).resolve().parents[1]

# `${CLAUDE_PLUGIN_ROOT}` is Claude Code's portable intra-plugin path token: at
# runtime it expands to wherever the plugin was installed. The agent body uses
# it for every reference link so those links resolve against the plugin
# directory rather than the session working directory (see AGENT_REF_PREFIX in
# scripts/sync-content.py for why that matters). In THIS repo the plugin
# directory is `first-principles/`, so link checking maps the token onto that
# path — see _resolve_link, which resolves the token rather than skipping it.
PLUGIN_ROOT_TOKEN = "${CLAUDE_PLUGIN_ROOT}"
PLUGIN_ROOT_TOKEN_TARGET = "first-principles"

# Scan globs: surfaces that receive BOTH relative-link and namespace-ref validation.
# Phase 26.1 adds the agent surface — first-principles.md is the agent spine and
# references/*.md its companion files.
#
# references/examples/ was excluded as "illustrative content, NOT link-checked
# source" until v8.17.5. That exclusion hid a real broken link: a worked example
# QUOTED the agent body's `](references/assumption-taxonomy.md)` inside prose,
# which markdown rendered as a live link resolving to
# agents/references/examples/references/… — a file that never existed. Being
# illustrative makes a file's links no less broken, and no scan covered this
# directory, so a plugin-wide sweep is what surfaced it rather than the gate.
# The glob is now full-checked; the quotation was made inert (a code span) since
# it was never navigation in the first place.
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
#
# v8.5 GATE-01 (D-01): added first-principles/skills/*/references/*.md — the
# companion-ref surface the Phase 154 split creates. Full-check (relative
# links AND namespace refs) is correct here because references/*.md files are
# authored fresh for the split, unlike SKILL.md stub bodies (see D-01 note
# on NAMESPACE_ONLY_GLOBS below for why that surface stays namespace-only).
# The target directory does not exist yet, so this entry matches zero files
# until Phase 154 lands — the inline `--self-test` fixture is what makes it
# load-bearing in the meantime (D-03).
#
# v8.17.5 (D-02 closed): first-principles/skills/*/SKILL.md is PROMOTED here
# from NAMESPACE_ONLY_GLOBS. It sat namespace-only for one reason — 12
# cross-technique links in the stubs used the shared/ source filename
# convention and did not resolve under the plugin directory layout, so
# full-checking would have failed immediately. Those 12 now target
# `${CLAUDE_PLUGIN_ROOT}/skills/<slug>/SKILL.md` and resolve, so the
# justification for the deferral is gone and the surface is fully checked.
# It stays in NAMESPACE_ONLY_GLOBS too — _collect_files dedups, and both
# axes now apply to it.
FULL_CHECK_GLOBS = [
    "first-principles/agents/first-principles.md",
    "first-principles/agents/references/*.md",
    "first-principles/skills/*/references/*.md",
    "first-principles/skills/*/SKILL.md",
    "first-principles/agents/references/examples/*.md",
]

# Scan globs: surfaces that receive namespace-ref validation ONLY.
# Relative links in these files use conventions valid in their source context
# (shared/ uses monolith filenames), not the installed plugin directory layout.
#
# v8.5 GATE-01 (D-05): restored first-principles/skills/*/SKILL.md, which
# Phase 26.1 removed on the (incorrect, never-realized) assumption that Plan 05
# would delete the whole skills/ tree — it did not.
#
# HISTORICAL, resolved at v8.17.5. This entry was namespace-only (NOT
# full-check) for one concrete reason: 12 cross-technique links in the
# generated stubs (e.g. `[5-Whys](five-whys.md)` in fishbone/SKILL.md) used the
# shared/ source filename convention rather than the plugin directory layout,
# so full-checking would have failed them immediately, and D-02 deferred the
# question of where they SHOULD point. That question is now answered — they
# target `${CLAUDE_PLUGIN_ROOT}/skills/<slug>/SKILL.md` and resolve — so the
# glob has been ADDED to FULL_CHECK_GLOBS above. It remains listed here as
# well: _collect_files dedups by resolved path, and the surface legitimately
# wants both axes. Do not read this entry as evidence that the surface is
# still namespace-only.
#
# Count history (v8.5 Phase 154, D-17): Plan 154-02's split moved 2 of
# fishbone's cross-skill links (its Failure modes and Handoff sections) into
# fishbone-detail.md, dropping the non-resolving cross-skill count in these
# SKILL.md files from 14 to 12 — the 12 that v8.17.5 retargeted. The 4
# `references/<slug>-detail.md` on-demand-load pointers Plan 154-03 introduced
# were never part of that non-resolving count: they resolve against the
# stub's own directory, which is how the harness loads a slash-invoked skill,
# and they are deliberately left file-relative.
NAMESPACE_ONLY_GLOBS = [
    "shared/**/*.md",
    "first-principles/skills/*/SKILL.md",
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
    root: Path = REPO_ROOT,
) -> list[Path]:
    """Expand globs against `root` and return sorted unique paths.

    `root` defaults to the module-level REPO_ROOT constant. The parameter
    lets `--self-test` point the collector at a temp directory fixture
    without touching the real tree or monkeypatching REPO_ROOT.
    """
    seen: set[Path] = set()
    result: list[Path] = []
    for pattern in globs:
        for path in sorted(root.glob(pattern)):
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

    Strips any #fragment. Targets starting with the `${CLAUDE_PLUGIN_ROOT}/`
    portable-path token are plugin-root relative and map onto this repo's
    plugin directory (PLUGIN_ROOT_TOKEN_TARGET); paths starting with '/' are
    repo-root relative; others are relative to the containing file's parent
    directory.

    The `${CLAUDE_PLUGIN_ROOT}` branch is a *resolution* rule, not a skip
    rule, and that is deliberate. The agent body's reference links carry this
    prefix because an agent body is read with the session working directory in
    force, not the plugin directory (see AGENT_REF_PREFIX in
    scripts/sync-content.py). Silently skipping the token would drop the
    entire agent body out of VAL-03's link checking while the gate still
    reported green — exactly the vacuous-gate failure mode this repo guards
    against. Mapping it instead keeps every one of those links validated, and
    validates them against the path the agent will actually open at runtime.

    URL-decode: not applied — repo doesn't use encoded paths today.
    (Deferred edge case: if encoded paths are introduced, add urllib.parse.unquote here.)
    """
    target = raw_target.split("#")[0]
    if not target:
        return source_file  # Pure anchor — no file to resolve.
    if target.startswith(PLUGIN_ROOT_TOKEN):
        rest = target[len(PLUGIN_ROOT_TOKEN):].lstrip("/")
        return (REPO_ROOT / PLUGIN_ROOT_TOKEN_TARGET / rest).resolve()
    if target.startswith("/"):
        return (REPO_ROOT / target.lstrip("/")).resolve()
    return (source_file.parent / target).resolve()


def _github_slug(heading: str) -> str:
    """Convert an ATX Markdown heading to a github-slugger anchor slug.

    This is the pure BASE-slug function — it does NOT apply github-slugger's
    duplicate-heading dedup suffix (`-1`, `-2`, …). Dedup is occurrence-aware
    and therefore lives in _doc_anchors, which has per-file heading order.

    Algorithm (per github-slugger v1/v2, D-04):
      1. Strip leading '#' characters and surrounding whitespace.
      2. Lowercase.
      3. Remove every character that is NOT an ASCII letter, ASCII digit,
         an underscore ('_'), a space (' '), or a hyphen ('-'). The underscore
         is a word character and github-slugger PRESERVES it (e.g. a code-span
         heading like '`scripts/_battery_core.py`' keeps its leading '_'). This
         step strips punctuation including em-dash (U+2014), colons, parentheses,
         backticks, slashes, periods, and all other Unicode non-alphanumeric
         characters — but NOT the underscore.
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
    # Remove all non-ASCII-alphanumeric, non-underscore, non-space, non-hyphen
    # characters. The underscore is kept because github-slugger preserves it.
    kept: list[str] = []
    for ch in text:
        if ch in " -_" or ("a" <= ch <= "z") or ("0" <= ch <= "9"):
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

    Implements github-slugger's duplicate-heading dedup: the first occurrence
    of a base slug registers as-is; the Nth (N>=2) occurrence of the SAME base
    slug registers with a '-{N-1}' suffix (`overview`, `overview-1`,
    `overview-2`, …). Headings are processed in document order so the suffix
    assignment matches github-slugger exactly.
    """
    try:
        full_text = path.read_text(encoding="utf-8")
    except OSError:
        return set()
    body = _strip_frontmatter(full_text)
    anchors: set[str] = set()
    counts: dict[str, int] = {}
    for m in _ATX_HEADING_RE.finditer(body):
        base = _github_slug(m.group(0))
        seen = counts.get(base, 0)
        anchor = base if seen == 0 else f"{base}-{seen}"
        counts[base] = seen + 1
        anchors.add(anchor)
    return anchors


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


def _run_self_test() -> int:
    """Self-test (v8.5 GATE-01, D-03/D-04): prove the two newly-extended VAL-03
    scan surfaces are load-bearing on a synthetic fixture, independent of the
    live tree (which matches zero findings on both axes today — D-06):

      - first-principles/skills/*/references/*.md (D-01, FULL_CHECK_GLOBS)
      - first-principles/skills/*/SKILL.md         (D-05, NAMESPACE_ONLY_GLOBS)

    Builds an on-disk temp fixture mirroring the real plugin layout, then
    drives the PRODUCTION FULL_CHECK_GLOBS / NAMESPACE_ONLY_GLOBS constants
    through the production _collect_files / _check_file functions — never a
    reimplementation. Because the module-level glob lists are used verbatim
    (not a hand-picked pattern string), removing either new glob entry makes
    the corresponding non-vacuity assertion fail (mutation-proof).

    Section 7 additionally drives `main()` itself over the same fixture, so
    main()'s own loop dispatch and dedup wiring are covered — not just the
    building blocks it calls. Without that section, flipping either loop's
    `check_links` flag silently reduced coverage while both the live scan and
    this self-test still passed (Phase 152 code-review WR-01).

    Accumulates every failure into `wrong` and reports them all at once
    (rather than exiting on the first) so a regression is fully diagnosable
    from a single CI run. Returns an exit code; the caller propagates it.
    """
    wrong: list[str] = []
    slug = "self-test-skill"

    with tempfile.TemporaryDirectory() as tmp:
        tmp_root = Path(tmp)
        skill_dir = tmp_root / "first-principles" / "skills" / slug
        references_dir = skill_dir / "references"
        references_dir.mkdir(parents=True, exist_ok=True)

        # SKILL.md — well-formed frontmatter + one resolving namespace ref
        # (self) and one unknown namespace ref.
        (skill_dir / "SKILL.md").write_text(
            "---\n"
            f"name: {slug}\n"
            "description: synthetic fixture skill for check-links.py --self-test\n"
            "---\n\n"
            "# Fixture skill\n\n"
            f"See `/first-principles:{slug}` (resolves) and "
            "`/first-principles:unknown-fixture-skill` (does not resolve).\n",
            encoding="utf-8",
        )

        # references/good.md — a relative link that resolves. Points at the
        # sibling SKILL.md (NOT itself matched by the references/*.md glob),
        # keeping the file-count assertion below exact.
        (references_dir / "good.md").write_text(
            "# Good reference\n\nSee [the skill](../SKILL.md) for context.\n",
            encoding="utf-8",
        )

        # references/bad.md — a relative link to a target that does not exist.
        (references_dir / "bad.md").write_text(
            "# Bad reference\n\nSee [missing](./missing.md) for details.\n",
            encoding="utf-8",
        )

        # --- 1. Non-vacuity (D-03, the crux) ---
        # Uses the PRODUCTION FULL_CHECK_GLOBS / NAMESPACE_ONLY_GLOBS lists
        # (not a hand-picked single pattern) so removing either new glob
        # entry from the module constants is detectable here.
        # v8.17.5: FULL_CHECK_GLOBS now also matches SKILL.md (promoted from
        # namespace-only once D-02 retargeted the 12 cross-technique links),
        # so the expected count is 3, not 2.
        references_files = _collect_files(FULL_CHECK_GLOBS, root=tmp_root)
        if len(references_files) != 3:
            wrong.append(
                "non-vacuity: FULL_CHECK_GLOBS matched "
                f"{len(references_files)} file(s) under the fixture root, "
                "expected 3 (references/good.md, references/bad.md, SKILL.md) "
                "— a zero-match glob is the exact failure mode this mode "
                "exists to prevent"
            )

        skill_files = _collect_files(NAMESPACE_ONLY_GLOBS, root=tmp_root)
        if len(skill_files) != 1:
            wrong.append(
                "non-vacuity: NAMESPACE_ONLY_GLOBS matched "
                f"{len(skill_files)} file(s) under the fixture root, "
                "expected 1 (SKILL.md)"
            )

        # --- 2. Deliberate overlap + dedup (edge:adjacency) ---
        # Until v8.17.5 these two globs were disjoint and this section asserted
        # exactly that. SKILL.md is now INTENTIONALLY in both lists — it wants
        # relative-link checking AND namespace-ref checking — so disjointness
        # is no longer the property to hold. The risk it guarded against is
        # unchanged, though: main() must visit the shared file, and must visit
        # it once. Assert the overlap is exactly what we intend and that
        # dedup collapses it, rather than asserting an overlap of zero.
        references_set = set(references_files)
        skill_set = set(skill_files)
        overlap = references_set & skill_set
        if overlap != skill_set:
            wrong.append(
                "overlap: expected every NAMESPACE_ONLY_GLOBS match to also be "
                f"a FULL_CHECK_GLOBS match (SKILL.md is in both lists as of "
                f"v8.17.5), but the shared set was "
                f"{sorted(str(p) for p in overlap)} vs "
                f"{sorted(str(p) for p in skill_set)}"
            )
        union_size = len(references_set | skill_set)
        if union_size != len(references_set):
            wrong.append(
                f"dedup: union size {union_size} != FULL_CHECK size "
                f"{len(references_set)} — the namespace-only glob is matching "
                "a file the full-check glob does not, which main()'s dedup "
                "would then have to reconcile"
            )

        # --- 3/4/5/6. Positive detection, negative controls, determinism ---
        # Run the collection+checking sequence twice over the same fixture
        # and assert the resulting broken lists are element-for-element equal
        # (edge:ordering).
        broken_runs: list[list[tuple[Path, int, str, str]]] = []
        valid_slugs = {slug}
        for _ in range(2):
            broken: list[tuple[Path, int, str, str]] = []
            total_links: list[int] = [0]
            total_refs: list[int] = [0]

            for source_file in references_files:
                _check_file(source_file, True, valid_slugs, broken, total_links, total_refs)
            for source_file in skill_files:
                _check_file(source_file, False, valid_slugs, broken, total_links, total_refs)

            broken_runs.append(list(broken))

        broken = broken_runs[0]

        if broken_runs[0] != broken_runs[1]:
            wrong.append(
                "determinism: two runs of _collect_files + _check_file over "
                f"the same fixture disagreed — run1={broken_runs[0]!r} "
                f"run2={broken_runs[1]!r}"
            )

        # Positive detection — references axis (D-01): bad.md's broken link
        # must be flagged with the exact production reason string. Fixture
        # paths live outside REPO_ROOT so `broken` entries carry absolute
        # temp paths (relative_to(REPO_ROOT) falls back to absolute) —
        # match on filename substring, never a full expected path.
        bad_flagged = [
            entry for entry in broken
            if "bad.md" in str(entry[0]) and entry[3] == "file not found"
        ]
        if not bad_flagged:
            wrong.append(
                "positive detection (references axis): bad.md's broken "
                "link to ./missing.md was not flagged with reason "
                f"'file not found' — broken list: {broken!r}"
            )

        # Negative control — references axis: good.md's resolving link must
        # NOT be flagged (rules out a constant-true detector).
        good_flagged = [entry for entry in broken if "good.md" in str(entry[0])]
        if good_flagged:
            wrong.append(
                "negative control (references axis): good.md's resolving "
                f"link was incorrectly flagged: {good_flagged!r}"
            )

        # Positive detection — namespace axis (D-05): the unknown ref must
        # be flagged with the exact production reason string.
        unknown_flagged = [
            entry for entry in broken
            if "unknown-fixture-skill" in entry[2]
            and entry[3] == "unknown namespace ref (not a sibling skill)"
        ]
        if not unknown_flagged:
            wrong.append(
                "positive detection (namespace axis): unknown ref "
                "`/first-principles:unknown-fixture-skill` was not flagged "
                f"with the expected reason — broken list: {broken!r}"
            )

        # Negative control — namespace axis: the self-referential ref must
        # NOT be flagged (rules out a constant-true detector).
        self_flagged = [
            entry for entry in broken
            if f"/first-principles:{slug}`" in entry[2]
        ]
        if self_flagged:
            wrong.append(
                "negative control (namespace axis): self-referential ref "
                f"`/first-principles:{slug}` was incorrectly flagged: "
                f"{self_flagged!r}"
            )

        # --- 7. End-to-end main() wiring (Phase 152 WR-01) ---
        # Sections 1-6 exercise _collect_files/_check_file directly, which
        # leaves main()'s OWN wiring unguarded: flipping the `check_links`
        # argument on either of main()'s two loops silently checks fewer
        # links while the live scan and sections 1-6 both still pass. Drive
        # main() over the same fixture and assert both axes still surface
        # their break. argv=[] keeps argparse off sys.argv (which carries
        # --self-test here) and prevents re-entering this function.
        main_out, main_err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(main_out), contextlib.redirect_stderr(main_err):
            main_rc = main(argv=[], root=tmp_root)
        main_stderr = main_err.getvalue()

        if main_rc != 1:
            wrong.append(
                f"main() wiring: main(argv=[], root=<fixture>) returned {main_rc}, "
                "expected 1 — the fixture contains two broken references, so a "
                "0 means main() scanned nothing or reported nothing"
            )

        # Guards main()'s full_check loop: flipping its check_links flag to
        # False stops relative-link checking and drops this entry.
        if "bad.md" not in main_stderr or "file not found" not in main_stderr:
            wrong.append(
                "main() wiring (references axis): main() did not report "
                "bad.md's broken relative link — main()'s full-check loop "
                "dispatch or its check_links flag has regressed. stderr: "
                f"{main_stderr!r}"
            )

        # Guards main()'s namespace_only loop the same way.
        if "unknown-fixture-skill" not in main_stderr:
            wrong.append(
                "main() wiring (namespace axis): main() did not report the "
                "unknown namespace ref — main()'s namespace-only loop "
                f"dispatch has regressed. stderr: {main_stderr!r}"
            )

        # Negative control through main(): the resolving link must stay unflagged.
        if "good.md" in main_stderr:
            wrong.append(
                "main() wiring (negative control): main() flagged good.md's "
                f"resolving link. stderr: {main_stderr!r}"
            )

    # --- 8. ${CLAUDE_PLUGIN_ROOT} portable-path resolution ---
    # The agent body's reference links carry the ${CLAUDE_PLUGIN_ROOT} prefix
    # so they resolve against the plugin install directory at runtime instead
    # of the session working directory. The cheap way to stop VAL-03 choking
    # on an unfamiliar prefix would have been to SKIP it — which would have
    # silently dropped the whole agent body out of link checking while the
    # gate still printed PASS. _resolve_link maps the token instead, and this
    # section is what keeps that a real check rather than a comment.
    #
    # Drives the production _resolve_link with the production PLUGIN_ROOT_TOKEN
    # / PLUGIN_ROOT_TOKEN_TARGET constants against the LIVE tree (not the temp
    # fixture, whose root _resolve_link does not consult), so reverting the
    # mapping to a skip — or repointing PLUGIN_ROOT_TOKEN_TARGET — fails here.
    agent_body = REPO_ROOT / "first-principles" / "agents" / "first-principles.md"
    token_link = f"{PLUGIN_ROOT_TOKEN}/agents/references/validation-rubric.md"

    resolved_hit = _resolve_link(token_link, agent_body)
    expected_hit = (
        REPO_ROOT / PLUGIN_ROOT_TOKEN_TARGET
        / "agents" / "references" / "validation-rubric.md"
    ).resolve()
    if resolved_hit != expected_hit:
        wrong.append(
            f"{PLUGIN_ROOT_TOKEN} resolution: _resolve_link({token_link!r}) "
            f"returned {resolved_hit}, expected {expected_hit} — the token is "
            "being treated as a literal path segment (or skipped) instead of "
            "mapped onto the plugin directory"
        )
    if not resolved_hit.exists():
        wrong.append(
            f"{PLUGIN_ROOT_TOKEN} resolution (non-vacuity): {resolved_hit} does "
            "not exist, so a passing live scan of the agent body would prove "
            "nothing — the rubric this token exists to reach is missing"
        )

    # Negative control: a token-prefixed target that does NOT exist must
    # resolve to a missing path, so _check_file still flags it. Without this,
    # a mapping that resolved every token link onto some always-present path
    # would satisfy the positive assertion above and check nothing.
    resolved_miss = _resolve_link(
        f"{PLUGIN_ROOT_TOKEN}/agents/references/no-such-reference.md", agent_body
    )
    if resolved_miss.exists():
        wrong.append(
            f"{PLUGIN_ROOT_TOKEN} resolution (negative control): a token link "
            f"to a nonexistent reference resolved to an existing path "
            f"{resolved_miss} — broken agent-body links would go unreported"
        )

    if wrong:
        sys.stderr.write("check-links --self-test: FAIL\n")
        for w in wrong:
            sys.stderr.write(f"  - {w}\n")
        return 1

    print(
        "check-links --self-test: PASS — the VAL-03 scan surfaces "
        "(first-principles/skills/*/references/*.md, D-01; "
        "first-principles/skills/*/SKILL.md, D-05) proven load-bearing on a "
        "synthetic fixture (non-vacuity, intended glob overlap + dedup, "
        "positive detection + negative controls on both axes, run-to-run "
        "determinism, and end-to-end main() dispatch wiring). Live-finding "
        "status (supersedes D-06's 'both vacuous' note): "
        "skills/*/references/*.md matches 4 real files and "
        "skills/*/SKILL.md is now FULL-checked as of v8.17.5, contributing "
        "16 real relative links — so neither surface is vacuous any more; "
        "the namespace-ref axis still finds zero backticked refs in the "
        "stubs. Also proven: ${CLAUDE_PLUGIN_ROOT} link targets are RESOLVED "
        "onto the plugin directory, not skipped — so absolutising the agent "
        "body's reference links did not silently remove it from link "
        "checking."
    )
    return 0


def main(argv: list[str] | None = None, root: Path = REPO_ROOT) -> int:
    """Run the VAL-03 scan and return a process exit code.

    `argv` defaults to sys.argv[1:] (argparse's own default) and `root` to the
    module-level REPO_ROOT. Both parameters exist so `--self-test` can drive
    THIS function — not just the _collect_files/_check_file building blocks it
    calls — against a temp fixture. Without that, main()'s own loop dispatch
    and dedup wiring had no regression guard: flipping the `check_links` flag
    on either loop below silently checked fewer links while both the live scan
    and the self-test still passed (v8.5 Phase 152 code-review WR-01).

    Returns rather than calling sys.exit() so the self-test can assert on the
    exit code; the __main__ guard converts the return value into the process
    status.
    """
    parser = argparse.ArgumentParser(
        description=(
            "VAL-03: validate relative markdown links + backticked namespace "
            "refs across the plugin/agent/shared surfaces."
        )
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help=(
            "prove both newly-extended scan surfaces (D-01 "
            "skills/*/references/*.md, D-05 skills/*/SKILL.md) are "
            "load-bearing on a synthetic fixture tree"
        ),
    )
    args = parser.parse_args(argv)

    _require_python_version()

    if args.self_test:
        return _run_self_test()

    _require_pyyaml()

    # Build valid namespace-ref slug set at runtime (not hard-coded — Phase 20+ safe).
    # Phase 26.1: tolerate missing first-principles/skills/ (Plan 05 deletes it)
    # AND include the agent's namespace token `first-principles` whenever the
    # agent file exists (so `/first-principles:first-principles` references in
    # the agent body resolve cleanly).
    #
    # Derived from `root` rather than imported from _skill_io so the self-test's
    # fixture root resolves its own skills. Byte-identical to the previous
    # _skill_io.PLUGIN_SKILLS_DIR for the live case: that constant is defined as
    # REPO_ROOT / "first-principles" / "skills" against the same REPO_ROOT.
    plugin_skills_dir = root / "first-principles" / "skills"

    valid_slugs: set[str] = set()
    if plugin_skills_dir.exists():
        try:
            valid_slugs |= {
                name
                for name in os.listdir(plugin_skills_dir)
                if (plugin_skills_dir / name / "SKILL.md").exists()
            }
        except Exception as exc:
            sys.stderr.write(f"check-links: cannot enumerate plugin skills: {exc}\n")
            return 2

    if (root / "first-principles" / "agents" / "first-principles.md").exists():
        valid_slugs.add("first-principles")

    full_check_files = _collect_files(FULL_CHECK_GLOBS, root=root)
    namespace_only_files = _collect_files(NAMESPACE_ONLY_GLOBS, root=root)
    docs_files = _collect_files(DOCS_CHECK_GLOBS, root=root)

    # Deduplicate: files in full_check_files should not also appear in namespace_only_files.
    full_check_set = set(full_check_files)
    namespace_only_files = [f for f in namespace_only_files if f not in full_check_set]

    # docs/ scan uses a separate docs_dir root for CF-04 prefix detection.
    docs_dir = root / "docs"

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
        return 1

    print(
        f"check-links: PASS ({total_links[0]} markdown links + {total_refs[0]} namespace refs"
        f" across {total_files} files)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
