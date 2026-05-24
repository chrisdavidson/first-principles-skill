#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml>=6.0"]
# ///
"""Sync canonical shared/ content into the agent surface.

Usage:
    python3 scripts/sync-content.py --write    # regenerate all 13 target files
    python3 scripts/sync-content.py --check    # compare on-disk vs generated; exit 1 on drift

Exit codes:
    0  success / no drift
    1  drift detected (--check)
    2  environment error (missing PyYAML, wrong Python version) or non-deterministic generation

Source of truth: shared/  (canonical)
Target surface (post Phase 26.1):
    - first-principles/agents/first-principles.md          (orchestrating agent)
    - first-principles/agents/references/<tool>.md         (6 companion-tool refs)
    - first-principles/agents/references/examples/<name>.md (6 worked-example siblings)
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
AGENT_DIR = REPO_ROOT / "first-principles" / "agents"
AGENT_PATH = AGENT_DIR / "first-principles.md"

# Marker syntax in shared/spine/SKILL-body.md.
TOKEN_RE = re.compile(r"\{\{TOOL:([a-z][a-z0-9-]*)\}\}")

# Heading-slice pattern for ## Procedure section extraction from reference files.
PROCEDURE_RE = re.compile(r"(^## Procedure\n.*?)(?=^## |\Z)", re.MULTILINE | re.DOTALL)

# PyYAML emission flags — pinned for byte-deterministic output (Pitfall 5).
# width=10**9 keeps short single-line description scalars on one line.
YAML_DUMP_KWARGS = dict(
    default_flow_style=False,
    sort_keys=False,
    allow_unicode=True,
    width=10**9,
)


class _QuotedStr(str):
    """Marker subclass: emit as a double-quoted scalar (preserves version: "x.y.z")."""


def _build_dumper():
    """Return a yaml.SafeDumper subclass with our style markers registered.

    A scoped Dumper subclass (vs. yaml.add_representer) keeps the sync script's
    emission choices local — global registration would leak across any other
    yaml.safe_dump call in the process.
    """
    import yaml

    class _Dumper(yaml.SafeDumper):
        pass

    def _quoted(dumper, data):
        return dumper.represent_scalar("tag:yaml.org,2002:str", str(data), style='"')

    _Dumper.add_representer(_QuotedStr, _quoted)
    return _Dumper


def _decorate_for_emission(meta: dict, surface: str, kind: str) -> dict:
    """Walk a meta dict and re-wrap select string values with style markers.

    Rule (see Plan 18-03 additional context; YAML emission resolution path A):
      - `metadata.version` is always wrapped as _QuotedStr so it re-emits with
        double quotes (matches current on-disk shape).

    `surface` / `kind` are retained for call-site compatibility; the only
    remaining surface after Phase 26.1 is the agent, but keeping the signature
    documents intent and leaves room for future surfaces without rippling
    changes through call sites.

    Returns a shallow-mutated copy; the input dict is not mutated.
    """
    out = {k: v for k, v in meta.items()}
    md = out.get("metadata")
    if isinstance(md, dict) and "version" in md:
        new_md = {k: v for k, v in md.items()}
        new_md["version"] = _QuotedStr(str(md["version"]))
        out["metadata"] = new_md
    return out

# Canonical companion-tool list (slug = plugin sibling skill directory name).
TOOLS = ("five-whys", "fishbone", "inversion", "pre-mortem", "trade-off", "second-order")

# Canonical worked-example list (filename stem under shared/examples/).
# Source-of-truth tree = shared/examples/ (established in Plan 26.1-03 Task 0).
# Plan 05 deletes the parallel monolith copies under
# first-principles-thinking/examples/; shared/examples/ survives as the
# sole source consumed by generate_agent_examples().
EXAMPLES = (
    "composed-inversion-second-order",
    "ishikawa-fishbone",
    "personal-general",
    "personal-general-2",
    "product-business",
    "product-business-2",
    "science-engineering",
    "science-engineering-2",
    "self-application",
    "software-systems",
    "software-systems-2",
)

# Canonical spine-references list (filename stem under shared/spine/references/)
# emitted verbatim as agent-side reference siblings under
# first-principles/agents/references/. Phase 31-02 introduces this list to ship
# `assumption-taxonomy.md` from the canonical spine tree to the agent surface.
#
# Inclusion contract: every entry MUST be a standalone reference file consumed
# by the agent as an on-demand sibling — NOT a spine appendix that
# generate_agent() inlines (e.g. `output-template.md`, `validation-rubric.md`).
# Mixing those in here would double-emit them (once inlined into the agent body,
# once as a sibling reference) and is explicitly forbidden by Phase 31-02
# Pitfall 1. Use an explicit list, never a glob.
SPINE_REFERENCES = (
    "assumption-taxonomy",
    # Phase 34-02 Path B: output-template and validation-rubric were previously
    # inlined into the agent body by generate_agent(). They are now emitted as
    # sibling reference files only, restoring META-Q4's <500-line body budget.
    # The spine body links to them via file-relative `references/...` links.
    "output-template",
    "validation-rubric",
)

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
    """Replace {{TOOL:<slug>}} markers with per-surface expansions.

    Distinguishes 'slug not in tool-map' from 'surface key missing on a known
    slug' (WR-06) so a contributor sees which mistake they made.
    """
    def sub(m: re.Match) -> str:
        slug = m.group(1)
        entry = tool_map.get(slug)
        if entry is None:
            raise ValueError(
                f"Unknown marker {{{{TOOL:{slug}}}}} in spine body "
                f"(surface={surface!r}; known slugs={sorted(tool_map)})"
            )
        if not isinstance(entry, dict) or surface not in entry:
            raise ValueError(
                f"Marker {{{{TOOL:{slug}}}}} has no '{surface}' surface in "
                f"shared/spine/tool-map.yml (slug is known, but its entry is "
                f"missing the '{surface}' key)"
            )
        return entry[surface]
    return TOKEN_RE.sub(sub, body)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _require_mapping(value, source_path: Path):
    """Ensure `yaml.safe_load` produced a dict, not None/list/scalar (WR-05).

    An empty or whitespace-only YAML file parses to None, which then crashes
    downstream with `'NoneType' object has no attribute 'get'`. Catch it here
    with a message that names the file.
    """
    if not isinstance(value, dict):
        try:
            rel = source_path.relative_to(REPO_ROOT)
        except ValueError:
            rel = source_path
        got = "empty/null" if value is None else type(value).__name__
        raise ValueError(
            f"{rel} did not parse to a YAML mapping (got {got}); "
            f"the file may be empty or malformed"
        )
    return value


def _read_required(path: Path, hint: str) -> str:
    """Read `path` as UTF-8; raise a structured FileNotFoundError on miss (WR-04).

    `hint` is appended to the error message so a contributor sees *why* the file
    is required (e.g. "did you add a TOOLS slug without a sidecar?") rather than
    a bare 'No such file or directory' traceback.
    """
    if not path.exists():
        try:
            rel = path.relative_to(REPO_ROOT)
        except ValueError:
            rel = path
        raise FileNotFoundError(f"{rel} not found ({hint})")
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


def _extract_procedure(slug: str) -> str:
    """Extract the ## Procedure section from shared/references/{slug}.md.

    Returns the text from the '## Procedure' heading line through (but not
    including) the next '## ' heading or EOF, with a trailing newline normalised
    to exactly one. Raises ValueError if the heading is absent.

    Used by generate_agent() to build the Companion Techniques section of the
    agent body — each slug's ## Procedure block is inlined verbatim.
    """
    body = _read_required(
        SHARED / "references" / f"{slug}.md",
        hint=f"shared/references/{slug}.md is required for the Companion Techniques section in the agent body",
    )
    m = PROCEDURE_RE.search(body)
    if not m:
        raise ValueError(
            f"shared/references/{slug}.md has no '## Procedure' heading"
        )
    slice_text = m.group(1)
    # Guard: raise if any intra-document anchor in the slice points at a heading
    # outside the slice (would become a dead link in the generated agent body).
    for fragment in re.findall(r"\]\(#([a-z0-9-]+)\)", slice_text):
        candidate = fragment.replace("-", " ")
        # A heading line inside the slice strips leading '#' chars and surrounding
        # whitespace; check case-insensitively.
        heading_in_slice = any(
            line.lstrip("#").strip().lower() == candidate
            for line in slice_text.splitlines()
            if line.startswith("#")
        )
        if not heading_in_slice:
            raise ValueError(
                f"shared/references/{slug}.md ## Procedure slice contains anchor "
                f"'#{fragment}' whose target heading is outside the inlined "
                f"## Procedure slice — this would become a dead link in the "
                f"generated agent body"
            )
    return _normalise_trailing_newline(slice_text)


def generate_agent(spine_meta: dict, tool_map: dict) -> dict[Path, str]:
    """Return {AGENT_PATH: content} for the first-principles orchestrating agent.

    Assembles the agent body from shared/ sources in this order:
      1. shared/agent/input-contract.md (verbatim prepend — before H1)
      2. shared/spine/SKILL-body.md expanded for the 'agent' surface
      3. ## Companion Techniques header + 6 ## Procedure blocks (TOOLS order)

    The output-template.md and validation-rubric.md spine appendices are NO
    LONGER inlined into the agent body (Phase 34-02, Path B). They are emitted
    solely as sibling reference files by generate_agent_spine_references() and
    linked from the spine body via file-relative `references/...` markdown links.
    This restores META-Q4's <500-line agent body budget without losing the
    content — the agent loads the references on demand.

    Stitches the agent: block from shared/spine/SKILL.meta.yml as YAML frontmatter.
    The generated file is never hand-edited; all content comes from shared/.
    """
    # --- Frontmatter from agent: block ---
    agent_fm = spine_meta.get("agent") or {}
    if not agent_fm:
        raise ValueError("shared/spine/SKILL.meta.yml missing 'agent' block")

    # --- Spine body expanded for the agent surface ---
    spine_body = _read_required(
        SHARED / "spine" / "SKILL-body.md",
        hint="canonical spine body is required for agent body assembly",
    )
    expanded_body = _expand(spine_body, tool_map, "agent")

    # --- Input contract (verbatim prepend — must precede the spine body's H1) ---
    input_contract = _read_required(
        SHARED / "agent" / "input-contract.md",
        hint="shared/agent/input-contract.md is required; add it per Phase 23 D-02",
    )

    # --- Companion Techniques: 6 ## Procedure sections in TOOLS order ---
    companion_header = "\n## Companion Techniques\n\n"
    companion_blocks = "".join(_extract_procedure(slug) + "\n" for slug in TOOLS)

    # --- Assemble body and stitch frontmatter ---
    # NOTE: output-template.md and validation-rubric.md are intentionally NOT
    # inlined here (Phase 34-02, Path B). They reach the agent only as sibling
    # reference files via generate_agent_spine_references(); the spine body
    # links to them with file-relative markdown links.
    body = _normalise_trailing_newline(
        input_contract
        + expanded_body
        + companion_header
        + companion_blocks
    )
    content = _stitch(
        _decorate_for_emission(agent_fm, surface="agent", kind="agent"),
        body,
    )
    return {AGENT_PATH: content}


def generate_agent_references() -> dict[Path, str]:
    """Return {AGENT_DIR/references/{slug}.md: body} for the 6 companion tools.

    Source = shared/references/{slug}.md (the canonical tree). Per D-01/D-02,
    the agent's on-demand reference siblings ship verbatim — NO frontmatter,
    NO marker expansion, NO edits. Trailing newline normalised to exactly one.
    """
    targets: dict[Path, str] = {}
    for slug in TOOLS:
        body = _read_required(
            SHARED / "references" / f"{slug}.md",
            hint=(
                f"shared/references/{slug}.md is required for the agent's "
                f"on-demand reference sibling at "
                f"first-principles/agents/references/{slug}.md"
            ),
        )
        targets[AGENT_DIR / "references" / f"{slug}.md"] = (
            _normalise_trailing_newline(body)
        )
    return targets


def generate_agent_spine_references() -> dict[Path, str]:
    """Return {AGENT_DIR/references/{slug}.md: body} for canonical spine references.

    Source = shared/spine/references/{slug}.md for each slug in SPINE_REFERENCES.
    Mirrors generate_agent_references() exactly: verbatim file copy, trailing-
    newline normalisation, NO frontmatter injection, NO marker expansion. This
    is the post-Plan-26.1 spine-reference sync path — distinct from the 6 tool
    references (which live under shared/references/, not shared/spine/references/).

    Phase 34-02 Path B: output-template.md and validation-rubric.md are now
    emitted via this path as sibling reference files only (previously
    generate_agent() inlined them into the agent body). The spine body links
    to them via file-relative `references/...` markdown links.
    """
    targets: dict[Path, str] = {}
    for slug in SPINE_REFERENCES:
        body = _read_required(
            SHARED / "spine" / "references" / f"{slug}.md",
            hint=(
                f"shared/spine/references/{slug}.md is required for the agent's "
                f"on-demand reference sibling at "
                f"first-principles/agents/references/{slug}.md"
            ),
        )
        targets[AGENT_DIR / "references" / f"{slug}.md"] = (
            _normalise_trailing_newline(body)
        )
    return targets


def generate_agent_examples() -> dict[Path, str]:
    """Return {AGENT_DIR/references/examples/{name}.md: body} for the 6 worked examples.

    Source = shared/examples/{name}.md (the source-of-truth tree established
    in Plan 26.1-03 Task 0 — NOT the monolith path). This preserves the
    single-source-of-truth invariant past Plan 05's monolith deletion:
    shared/examples/ survives, this generator survives, and the sync-drift
    CI gate continues to enforce byte-identity between source and emission.

    Per D-01 amended / MIGRATE-02 amended / E-3 resolution: verbatim copy —
    NO frontmatter, NO marker expansion, NO edits. Trailing newline normalised.
    """
    targets: dict[Path, str] = {}
    for name in EXAMPLES:
        body = _read_required(
            SHARED / "examples" / f"{name}.md",
            hint=(
                f"shared/examples/{name}.md is required for the agent's "
                f"on-demand worked-example sibling at "
                f"first-principles/agents/references/examples/{name}.md"
            ),
        )
        targets[AGENT_DIR / "references" / "examples" / f"{name}.md"] = (
            _normalise_trailing_newline(body)
        )
    return targets


def generate_all() -> dict[Path, str]:
    """Return {target_path: content} for every emitted file.

    14 targets total (Phase 31-02 adds the spine-references emission):
      - 1 agent SKILL.md (first-principles/agents/first-principles.md)
      - 6 agent reference siblings (first-principles/agents/references/<tool>.md)
      - 1 agent spine-reference sibling
        (first-principles/agents/references/assumption-taxonomy.md)
      - 6 agent worked-example siblings (first-principles/agents/references/examples/<name>.md)
    Total: 1 + 6 + 1 + 6 = 14.
    """
    import yaml

    targets: dict[Path, str] = {}

    # --- Spine + tool-map: still required for agent body assembly ---
    tool_map_path = SHARED / "spine" / "tool-map.yml"
    tool_map = _require_mapping(
        yaml.safe_load(_read_required(
            tool_map_path,
            hint="canonical tool-map drives {{TOOL:<slug>}} marker expansion",
        )),
        tool_map_path,
    )
    spine_meta_path = SHARED / "spine" / "SKILL.meta.yml"
    spine_meta = _require_mapping(
        yaml.safe_load(_read_required(
            spine_meta_path,
            hint="canonical spine frontmatter is required for the agent surface",
        )),
        spine_meta_path,
    )

    # --- Agent surface (sole remaining generated surface) ---
    targets.update(generate_agent(spine_meta, tool_map))
    targets.update(generate_agent_references())
    targets.update(generate_agent_spine_references())
    targets.update(generate_agent_examples())

    # --- Path-safety assertion (V12 ASVS): every write path must live inside
    #     the agent tree (the sole allowed root after Phase 26.1).
    # Use Path.relative_to() rather than str.startswith() to avoid sibling-dir
    # false positives (WR-01).
    allowed_roots = (AGENT_DIR,)
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
