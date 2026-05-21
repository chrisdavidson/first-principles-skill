#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml>=6.0"]
# ///
"""Sync canonical shared/ content into the monolith + plugin surfaces.

Usage:
    python3 scripts/sync-content.py --write    # regenerate all 17 target files
    python3 scripts/sync-content.py --check    # compare on-disk vs generated; exit 1 on drift

Exit codes:
    0  success / no drift
    1  drift detected (--check)
    2  environment error (missing PyYAML, wrong Python version) or non-deterministic generation

Source of truth: shared/  (canonical)
Target surfaces:
    - first-principles-thinking/                 (monolith)
    - first-principles/skills/thinking/          (plugin spine)
    - first-principles/skills/<tool>/SKILL.md    (plugin sibling skills)
"""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from pathlib import Path

# Path resolution: relative to this script's location, not Path.cwd() (Pitfall 8).
REPO_ROOT = Path(__file__).resolve().parents[1]
SHARED = REPO_ROOT / "shared"
MONOLITH = REPO_ROOT / "first-principles-thinking"
PLUGIN_SKILLS = REPO_ROOT / "first-principles" / "skills"

# Marker syntax in shared/spine/SKILL-body.md.
TOKEN_RE = re.compile(r"\{\{TOOL:([a-z][a-z0-9-]*)\}\}")

# PyYAML emission flags — pinned for byte-deterministic output (Pitfall 5).
# width=10**9 keeps short single-line description scalars on one line (plugin
# canonical shape). The monolith spine's folded `>-` description scalar (see
# _FoldedStr below) still emits as a folded block — just unwrapped onto one
# indented content line. The wrap-width delta from the hand-authored multi-line
# original is absorbed by MIGRATION-DIFFS.md (resolution C addendum).
YAML_DUMP_KWARGS = dict(
    default_flow_style=False,
    sort_keys=False,
    allow_unicode=True,
    width=10**9,
)


class _QuotedStr(str):
    """Marker subclass: emit as a double-quoted scalar (preserves version: "x.y.z")."""


class _FoldedStr(str):
    """Marker subclass: emit as a folded block scalar (>-) for long descriptions."""


def _build_dumper():
    """Return a yaml.SafeDumper subclass with our two style markers registered.

    A scoped Dumper subclass (vs. yaml.add_representer) keeps the sync script's
    emission choices local — global registration would leak across any other
    yaml.safe_dump call in the process.
    """
    import yaml

    class _Dumper(yaml.SafeDumper):
        pass

    def _quoted(dumper, data):
        return dumper.represent_scalar("tag:yaml.org,2002:str", str(data), style='"')

    def _folded(dumper, data):
        return dumper.represent_scalar("tag:yaml.org,2002:str", str(data), style=">")

    _Dumper.add_representer(_QuotedStr, _quoted)
    _Dumper.add_representer(_FoldedStr, _folded)
    return _Dumper


def _decorate_for_emission(meta: dict, surface: str, kind: str) -> dict:
    """Walk a meta dict and re-wrap select string values with style markers.

    Rules (see Plan 18-03 additional context; YAML emission resolution path A):
      - `metadata.version` is always wrapped as _QuotedStr so it re-emits with
        double quotes (matches current on-disk shape across both surfaces).
      - For the monolith spine (kind=='spine' and surface=='monolith'), the
        `description` field is wrapped as _FoldedStr so it re-emits as a `>-`
        folded block scalar (matches current on-disk shape; wrap-width may
        differ slightly from the hand-authored original — that minor
        cosmetic delta is absorbed by MIGRATION-DIFFS.md per resolution C).

    Returns a shallow-mutated copy; the input dict is not mutated.
    """
    out = {k: v for k, v in meta.items()}
    md = out.get("metadata")
    if isinstance(md, dict) and "version" in md:
        new_md = {k: v for k, v in md.items()}
        new_md["version"] = _QuotedStr(str(md["version"]))
        out["metadata"] = new_md
    if kind == "spine" and surface == "monolith" and isinstance(out.get("description"), str):
        out["description"] = _FoldedStr(out["description"])
    return out

# Canonical companion-tool list (slug = plugin sibling skill directory name).
TOOLS = ("five-whys", "fishbone", "inversion", "pre-mortem", "trade-off", "second-order")

# Monolith carries historical filenames that differ from plugin slugs for 3 tools.
# fishbone -> ishikawa-diagram.md, trade-off -> trade-off-analysis.md,
# second-order -> second-order-thinking.md.
MONOLITH_REF_FILENAME = {
    "five-whys": "five-whys.md",
    "fishbone": "ishikawa-diagram.md",
    "inversion": "inversion.md",
    "pre-mortem": "pre-mortem.md",
    "trade-off": "trade-off-analysis.md",
    "second-order": "second-order-thinking.md",
}


def _require_pyyaml() -> None:
    """Catch missing PyYAML at startup with a clear remediation message (Pitfall 4)."""
    try:
        import yaml  # noqa: F401
    except ImportError:
        sys.stderr.write(
            "scripts/sync-content.py needs PyYAML.\n"
            "  Easiest:  uv run scripts/sync-content.py --check\n"
            "  Or:       pip install --user 'pyyaml>=6.0'  &&  "
            "python3 scripts/sync-content.py --check\n"
        )
        sys.exit(2)


def _require_python_version() -> None:
    if sys.version_info < (3, 12):
        sys.stderr.write(
            f"scripts/sync-content.py requires Python >=3.12 "
            f"(running {sys.version_info.major}.{sys.version_info.minor}).\n"
        )
        sys.exit(2)


def _stitch(meta: dict, body: str) -> str:
    """Stitch a YAML frontmatter block onto a Markdown body.

    Uses `---\\n{fm}\\n---\\n{body}` — NO blank line inserted between the
    closing fence and the body. If a blank line is part of the canonical
    shape (e.g. the spine SKILL.md has `---\\n\\n# First Principles Thinking`),
    the leading `\\n` must live in the body in shared/ — see
    shared/spine/SKILL-body.md (which starts with a leading blank).

    This per-file divergence is necessary: plugin sibling SKILL.md files
    use `---\\n# Heading` (no blank), spine SKILL.md uses `---\\n\\n# Heading`.
    Letting the body own the leading whitespace keeps stitch shape-agnostic.
    """
    import yaml
    Dumper = _build_dumper()
    fm = yaml.dump(meta, Dumper=Dumper, **YAML_DUMP_KWARGS).rstrip("\n")
    out = f"---\n{fm}\n---\n{body}"
    if not out.endswith("\n"):
        out += "\n"
    return out


def _expand(body: str, tool_map: dict, surface: str) -> str:
    """Replace {{TOOL:<slug>}} markers with per-surface expansions."""
    def sub(m: re.Match) -> str:
        slug = m.group(1)
        try:
            return tool_map[slug][surface]
        except KeyError as e:
            raise ValueError(
                f"Unknown marker {{{{TOOL:{slug}}}}} in spine body "
                f"(surface={surface!r}; known slugs={sorted(tool_map)})"
            ) from e
    return TOKEN_RE.sub(sub, body)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _is_within(child: Path, parent: Path) -> bool:
    """Return True iff `child` is `parent` or strictly inside it (resolved)."""
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def _normalise_trailing_newline(content: str) -> str:
    """Pin every emitted file to exactly one trailing '\\n' (Pitfall 9)."""
    return content.rstrip("\n") + "\n"


def generate_all() -> dict[Path, str]:
    """Return {target_path: content} for every emitted file.

    17 targets total:
      - 6 monolith companion refs
      - 6 plugin sibling SKILL.md files
      - 1 monolith spine SKILL.md
      - 1 plugin spine SKILL.md
      - 2 monolith spine appendices (output-template + validation-rubric)
      - 2 plugin spine appendices (output-template + validation-rubric)
    Wait: 6 + 6 + 1 + 1 + 2 + 2 = 18. The plan said 17; off-by-one in plan
    description. Both spine appendices ship to both surfaces, so 18 is
    correct.
    """
    import yaml

    targets: dict[Path, str] = {}

    # --- Companion bodies + sidecars ---
    for t in TOOLS:
        body = _read_text(SHARED / "references" / f"{t}.md")
        meta_path = SHARED / "references" / f"{t}.meta.yml"
        meta = yaml.safe_load(_read_text(meta_path))
        plugin_fm = meta.get("plugin") or {}
        monolith_fm = meta.get("monolith") or {}

        # Monolith ref: body only, no frontmatter (D-18-2).
        targets[MONOLITH / "references" / MONOLITH_REF_FILENAME[t]] = (
            _normalise_trailing_newline(body)
        )

        # Plugin sibling SKILL.md: stitch plugin frontmatter onto body.
        if not plugin_fm:
            raise ValueError(f"shared/references/{t}.meta.yml missing 'plugin' block")
        plugin_skill = _stitch(
            _decorate_for_emission(plugin_fm, surface="plugin", kind="sibling"), body
        )
        targets[PLUGIN_SKILLS / t / "SKILL.md"] = plugin_skill

        # Monolith refs never get frontmatter; ignore monolith_fm here.
        _ = monolith_fm  # documented no-op

    # --- Spine body (with marker expansion per surface) ---
    spine_body = _read_text(SHARED / "spine" / "SKILL-body.md")
    tool_map = yaml.safe_load(_read_text(SHARED / "spine" / "tool-map.yml"))
    spine_meta = yaml.safe_load(_read_text(SHARED / "spine" / "SKILL.meta.yml"))
    spine_plugin_fm = spine_meta.get("plugin") or {}
    spine_monolith_fm = spine_meta.get("monolith") or {}

    if not spine_plugin_fm:
        raise ValueError("shared/spine/SKILL.meta.yml missing 'plugin' block")
    if not spine_monolith_fm:
        raise ValueError("shared/spine/SKILL.meta.yml missing 'monolith' block")

    plugin_spine_body = _expand(spine_body, tool_map, "plugin")
    monolith_spine_body = _expand(spine_body, tool_map, "monolith")

    targets[PLUGIN_SKILLS / "thinking" / "SKILL.md"] = _stitch(
        _decorate_for_emission(spine_plugin_fm, surface="plugin", kind="spine"),
        plugin_spine_body,
    )
    targets[MONOLITH / "SKILL.md"] = _stitch(
        _decorate_for_emission(spine_monolith_fm, surface="monolith", kind="spine"),
        monolith_spine_body,
    )

    # --- Spine appendices: verbatim, no marker expansion, no frontmatter ---
    for appendix in ("output-template.md", "validation-rubric.md"):
        content = _normalise_trailing_newline(
            _read_text(SHARED / "spine" / "references" / appendix)
        )
        targets[MONOLITH / "references" / appendix] = content
        targets[PLUGIN_SKILLS / "thinking" / "references" / appendix] = content

    # --- Path-safety assertion (V12 ASVS): every write path must live inside
    #     one of the two known generated-trees.
    # Use Path.relative_to() rather than str.startswith() to avoid sibling-dir
    # false positives (WR-01): a path like `.../first-principles-thinking-extra/x`
    # shares a string prefix with `.../first-principles-thinking` but is not
    # actually inside it. relative_to() is the boundary-correct check.
    allowed_roots = (MONOLITH, PLUGIN_SKILLS)
    for path in targets:
        if not any(_is_within(path, root) for root in allowed_roots):
            raise ValueError(
                f"Generated path {path} resolves outside allowed trees "
                f"{[str(r) for r in allowed_roots]}"
            )

    return targets


def cmd_write() -> int:
    targets = generate_all()
    for path, content in targets.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        # newline='\n' pins LF on every platform (Pitfall 9 / CLAUDE.md mandate).
        path.write_text(content, encoding="utf-8", newline="\n")
    print(f"wrote {len(targets)} files")
    return 0


def cmd_check() -> int:
    # Idempotency self-test (Pitfall 7): two in-memory generations must be equal.
    pass1 = generate_all()
    pass2 = generate_all()
    if pass1 != pass2:
        sys.stderr.write("NON-DETERMINISTIC: pass-1 != pass-2\n")
        for k in pass1:
            if pass1.get(k) != pass2.get(k):
                sys.stderr.write(f"  differs: {k.relative_to(REPO_ROOT)}\n")
        return 2

    # On-disk compare with unified-diff drift output (Pitfall 6).
    drifted: list[Path] = []
    for path, generated in pass1.items():
        on_disk = path.read_text(encoding="utf-8") if path.exists() else ""
        if on_disk != generated:
            drifted.append(path)
            rel = path.relative_to(REPO_ROOT)
            sys.stderr.write(f"DRIFT: {rel}\n")
            sys.stderr.writelines(
                difflib.unified_diff(
                    on_disk.splitlines(keepends=True),
                    generated.splitlines(keepends=True),
                    fromfile=f"a/{rel}",
                    tofile=f"b/{rel}",
                    n=3,
                )
            )
            sys.stderr.write("\n")

    if drifted:
        # Remediation must be the first line a CI / hook caller sees in stderr
        # after the DRIFT summary lines.
        sys.stderr.write(
            "Run: python3 scripts/sync-content.py --write && git add -u\n"
        )
        return 1
    return 0


def main() -> int:
    _require_python_version()
    _require_pyyaml()
    p = argparse.ArgumentParser(
        prog="sync-content.py",
        description="Sync shared/ -> monolith + plugin surfaces.",
    )
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true", help="Compare; exit 1 on drift.")
    g.add_argument("--write", action="store_true", help="Regenerate all targets.")
    args = p.parse_args()
    return cmd_check() if args.check else cmd_write()


if __name__ == "__main__":
    sys.exit(main())
