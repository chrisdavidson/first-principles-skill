#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml>=6.0"]
# ///
"""Sync canonical shared/ content into the agent surface.

Usage:
    python3 scripts/sync-content.py --write    # regenerate all 48 target files
    python3 scripts/sync-content.py --check    # compare on-disk vs generated; exit 1 on drift

Exit codes:
    0  success / no drift
    1  drift detected (--check)
    2  environment error (missing PyYAML, wrong Python version) or non-deterministic generation

Source of truth: shared/  (canonical)
Target surface:
    - first-principles/agents/first-principles.md              (orchestrating agent)
    - first-principles/agents/references/<tool>.md             (8 companion-tool refs)
    - first-principles/agents/references/<spine-ref>.md        (3 spine refs)
    - first-principles/agents/references/<slug>-detail.md      (4 on-demand agent detail siblings)
    - first-principles/agents/references/examples/<name>.md    (worked-example siblings)
    - first-principles/skills/<slug>/SKILL.md                  (13 focused-mode stubs)
    - first-principles/skills/<slug>/references/<slug>-detail.md (4 on-demand skill detail siblings)
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
TOOLS = ("five-whys", "fishbone", "inversion", "pre-mortem", "trade-off", "second-order", "estimate", "theoretical-limit")

# Canonical slash-invocable focused-mode stub list (Phase 46-02, DEC-46-B).
# Each entry maps to a `shared/skills/<slug>/SKILL.md` source and a generated
# `first-principles/skills/<slug>/SKILL.md` sibling. All carry
# `disable-model-invocation: true` so the orchestrator cannot auto-route to
# them — only explicit `/first-principles:<slug>` slash invocation loads them.
# Phase 52 extends the original six companion-tool slugs with five new phase
# slugs (identify-essence, challenge-assumptions, ground-truths, reason-upward,
# validate). The shared/skills/<slug>/SKILL.md source stubs for the five new
# slugs are Phase 53 deliverables; running --write before they exist raises
# FileNotFoundError from _read_required().
SKILLS = (
    "pre-mortem", "inversion", "fishbone", "five-whys", "trade-off", "second-order",
    "identify-essence", "challenge-assumptions", "ground-truths", "reason-upward", "validate",
    "estimate", "theoretical-limit",
    "first-principles-analysis",
)

# Launcher stubs (DISPATCH-05): slugs whose stub body carries no inlined technique
# procedure and therefore no `{{PROCEDURE:<slug>}}` token. A launcher's whole job is
# to dispatch the composer agent explicitly, so there is no `shared/references/<slug>.md`
# to inline and the 80-LOC inline-copy floor does not apply to it.
#
# Why this exemption exists rather than a synthetic reference file: the alternative —
# a self-contained composer skill — would have to mirror the agent's entire reference
# tree (22 files: 12 worked examples, assumption-taxonomy, 4 detail siblings,
# output-template, validation-rubric) under the skill directory, because skill
# references must sit one level deep beside their own skill. That doubles the generated
# surface and gives the methodology a second copy that can drift from the agent's.
# The launcher keeps the agent as the single source of truth.
LAUNCHER_SKILLS = frozenset({"first-principles-analysis"})

# Token in shared/skills/<slug>/SKILL.md replaced by sync with the inlined
# technique content (from `## When to reach for this` to EOF of
# shared/references/<slug>.md). The pattern mirrors {{TOOL:<slug>}} expansion
# but targets the larger reference body (procedure + example + failure modes
# + handoff), which keeps every stub above the 80-LOC floor that
# 46-02-PLAN.md mandates for "procedure inlined" to be empirically falsifiable.
SKILL_TOKEN_RE = re.compile(r"\{\{PROCEDURE:([a-z][a-z0-9-]*)\}\}")

# Token in shared/skills/<slug>/SKILL.md replaced by sync with the canonical
# focused-mode validation step (03-02-PLAN.md, PAR-02). Unlike {{TOOL:slug}}
# and {{PROCEDURE:slug}}, this token takes NO slug argument — it resolves
# from one fixed path, not a per-slug reference file, because the validation
# step is technique-agnostic and identical in all 13 stubs.
FOCUSED_VALIDATION_TOKEN_RE = re.compile(r"\{\{FOCUSED_VALIDATION\}\}")

# Fixed source for the {{FOCUSED_VALIDATION}} token. Deliberately NOT under
# shared/spine/references/ (which is 1:1 with SPINE_REFERENCES and would make
# it an emitted target) — this file is inlined whole into every non-launcher
# stub and is never emitted as its own file, so GENERATED_TARGET_COUNT stays
# 48 and the path must never be added to SPINE_REFERENCES.
FOCUSED_VALIDATION_SOURCE = SHARED / "spine" / "focused-validation-step.md"

# Marker line stamped on every generated stub body, immediately after the
# closing frontmatter delimiter (Pitfall 7 mitigation, 46-02-PLAN must_haves).
SKILL_DO_NOT_EDIT_LINE = (
    "<!-- DO NOT EDIT — generated from shared/skills/{slug}/SKILL.md "
    "by sync-content.py -->\n"
)

# Marker line stamped on every byte-identical verbatim copy emitted to the
# agent surface (references, spine-references, examples) and at the top of
# the assembled agent body. Lets code reviewers (and any future
# `.reviewignore` consumer) shortcut the generated mirror under
# first-principles/agents/ and review the canonical shared/ source instead.
# Format: HTML comment so markdown renderers ignore it and the runtime
# agent loader sees a single inert line of prose.
GENERATED_MARKER = (
    "<!-- GENERATED — DO NOT EDIT. Source: shared/{source_rel}. "
    "Regenerate via: scripts/sync-content.py --write. -->\n"
)

# v8.5 Phase 154 (Rule 3 auto-fix, MECH-02): a detail sibling's canonical
# source (shared/references/<slug>-detail.md) deliberately opens on
# '## Example' with no H1 — Plan 02 locked "no H1, no back-pointer, no new
# prose" as a must-have truth for the split, and that is true as written for
# three of the four split files (five-whys, theoretical-limit, estimate).
# fishbone is the named exception: its split converted 2 pre-existing
# cross-technique Markdown links inside the moved Failure-modes/Handoff
# content into namespace refs — a genuine content edit within the moved
# text, not a pure relocation — see check-links.py's D-17 note for the
# rationale of record. That source file is already committed and
# byte-frozen. Once this plan wires the sibling into the generated tree,
# VAL-02 (markdownlint MD041, first-line-must-be-H1) flags every emission of
# it. Rather than add an H1 to the frozen source (an architectural reversal
# of Plan 02's decision) or disable MD041 tree-wide (weakening the gate for
# the other 43 generated files), this generator-only inline directive
# exempts exactly the eight new detail-sibling emissions — MD041 keeps full
# teeth everywhere else.
DETAIL_SIBLING_LINT_EXEMPT = "<!-- markdownlint-disable MD041 -->\n"

# Generated stub target tree (sibling to AGENT_DIR; never hand-edited).
SKILLS_DIR = REPO_ROOT / "first-principles" / "skills"


# Canonical worked-example list (filename stem under shared/examples/).
# Source-of-truth tree = shared/examples/ (established in Plan 26.1-03 Task 0).
# Plan 05 deletes the parallel monolith copies under
# first-principles-thinking/examples/; shared/examples/ survives as the
# sole source consumed by generate_agent_examples().
EXAMPLES = (
    "composed-inversion-second-order",
    "decompose-irreducibility",
    "estimate-fermi",
    "theoretical-limit-carnot",
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

# The four reference files v8.5 §2 authorises splitting into a core file plus
# a `-detail.md` appendix (docs/v8.4-implementation-readiness-eval.md §4's
# per-section boundary table — pruned from the tree 2026-08-16, read it with
# `git show 09326e7~1:docs/v8.4-implementation-readiness-eval.md`).
# This is the SINGLE source every slug-scoped
# branch in this module reads from — never re-derive the set inline. It must
# never be widened without a governing byte-freeze record like
# docs/v8.5-byte-freeze-relaxation.md: `pre-mortem` and `trade-off` also carry
# an appendix-style `## Example` heading and are deliberately excluded.
SLUGS_WITH_DETAIL = frozenset({"five-whys", "theoretical-limit", "estimate", "fishbone"})

# Plugin-root-anchored prefix for every reference link emitted into the agent
# body (first-principles/agents/first-principles.md).
#
# Why not a file-relative `references/...` target: an agent body is consumed
# with the *session* working directory in force, not the directory the agent
# file lives in. A relative target therefore resolves against the user's
# project — where `references/validation-rubric.md` does not exist — so the
# agent cannot open its own Self-Audit Gate, output template, assumption
# taxonomy, worked examples, or `-detail.md` appendices. Observed live at
# v8.14.0: the Phase 5 self-audit gate never fired across a 533k-char run.
#
# `${CLAUDE_PLUGIN_ROOT}` is the documented portable intra-plugin path form and
# is explicitly sanctioned for component files — commands, *agents*, skills —
# not just hooks.json and MCP manifests. It expands to the plugin install
# directory, which is this repo's `first-principles/`, so the agent surface's
# own references sit under `${CLAUDE_PLUGIN_ROOT}/agents/references/`.
#
# The skill stubs deliberately do NOT use this prefix: a slash-invoked skill is
# resolved by the harness against its own skill directory, so their historical
# file-relative `references/...` targets already work.
#
# VAL-03 (`scripts/check-links.py`) resolves this prefix back to
# `first-principles/` and keeps full-checking every one of these links — the
# absolutisation does not cost link-validation coverage.
AGENT_REF_PREFIX = "${CLAUDE_PLUGIN_ROOT}/agents/references/"

# Plugin-root-anchored prefix for a cross-technique link emitted into a SKILL
# STUB (first-principles/skills/<slug>/SKILL.md). A stub's bare cross-links
# (`](pre-mortem.md)`) are the same 12 source links the agent surface carries,
# but they fail here for a different reason: not absent resolution — the
# harness does resolve a slash-invoked skill against its own directory — but a
# WRONG PATH, since `skills/inversion/pre-mortem.md` does not exist. The stub's
# peer lives at `skills/pre-mortem/SKILL.md`.
#
# Resolved at v8.17.5, closing D-02. The alternatives were a backticked
# namespace ref (`/first-principles:pre-mortem`) and a link into the agent's
# own reference tree; the peer-stub file link was chosen because it leaves the
# surrounding prose byte-identical, resolves on disk, and lets VAL-03 promote
# this surface from namespace-only to full link-checking — which also retires
# D-05's deferral, whose whole justification was these 12 non-resolving links.
SKILL_PEER_PREFIX = "${CLAUDE_PLUGIN_ROOT}/skills/"

# Canonical total count of files that sync-content.py generates (len(generate_all())).
# Breakdown: 1 agent + 11 reference siblings + 4 agent detail siblings +
# 14 worked-example siblings + 14 skill stubs + 4 skill detail siblings.
# DISPATCH-05 adds the 14th skill stub: the `first-principles-analysis` launcher
# (LAUNCHER_SKILLS). It emits one stub and no detail sibling — a launcher inlines
# no technique procedure, so it adds exactly 1 to this count.
# v8.5 Phase 154 (MECH-02) adds the two four-entry detail-sibling families for
# SLUGS_WITH_DETAIL, raising the previous total (documented pre-Phase-154 in
# git history) to the count below.
# Three committed-but-hand-maintained files (first-principles/README.md,
# first-principles/LICENSE, first-principles/.claude-plugin/plugin.json) are NOT
# counted here because the path-safety assertion in generate_all() (the allowed_roots
# loop) forbids the generator from emitting outside AGENT_DIR / SKILLS_DIR — they are
# out-of-generator-scope.
# generate_all() raises ValueError if len(targets) != GENERATED_TARGET_COUNT so this
# number cannot silently drift again (D-01, DEBT-02).
GENERATED_TARGET_COUNT = 48

# v8.5 Phase 154 GATE-02 (D-11): module-level re-entrancy sentinel guarding
# cmd_self_test()'s dispatch control. That control drives main(["--self-test"])
# to prove the CLI dispatch layer itself reaches the GATE-02 block (not just
# that cmd_self_test() is correct when called directly, Phase 152 WR-01) — but
# main(["--self-test"]) calls cmd_self_test() again, which would re-enter the
# same dispatch control and recurse without bound. Set True only for the
# duration of that one nested call (restored in a finally clause so an
# exception cannot leave it set); the nested cmd_self_test() checks this flag
# and skips its own dispatch control while still running every other control.
_GATE02_DISPATCH_REENTRANT = False


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


# Matches an inline-link target that is a BARE markdown filename — no
# directory component, no scheme, no anchor, no `${...}` token. Deliberately
# narrow: `_absolutise_agent_ref_links()` must never touch a target that is
# already anchored, already relative-with-a-path, or a URL.
_BARE_MD_TARGET_RE = re.compile(r"\]\((?!https?:|mailto:|#|\$\{)([A-Za-z0-9._-]+\.md)\)")


def _agent_ref_allowed_targets() -> frozenset[str]:
    """Filenames that legitimately sit in first-principles/agents/references/.

    Derived from the same module-level lists that drive emission — never a
    hand-maintained second copy — so adding a companion tool or a spine
    reference extends this set automatically, and a bare link to anything
    NOT emitted into that directory is a typo this module should refuse to
    ship rather than silently anchor into a broken absolute path.
    """
    names = {f"{slug}.md" for slug in TOOLS}
    names |= {f"{slug}-detail.md" for slug in SLUGS_WITH_DETAIL}
    names |= {f"{stem}.md" for stem in SPINE_REFERENCES}
    return frozenset(names)


def _absolutise_agent_ref_links(text: str, source_rel: str) -> str:
    """Anchor every bare sibling-filename link in an agent reference file.

    The agent's on-demand reference siblings under
    first-principles/agents/references/ link to each other by bare filename
    (`](pre-mortem.md)`, `](five-whys-detail.md)`). Those targets resolve
    correctly *within that directory* — which is why DEC-A originally left
    them alone — but the model that opens one of these files is not sitting in
    that directory: it reads with the session working directory in force, the
    same condition that broke the agent body's own links before v8.17.3. So a
    second-hop load (references/five-whys.md -> five-whys-detail.md) failed in
    exactly the way the first hop did. **This function overturns DEC-A**, and
    GATE-02-v8.5's (g) assertion was flipped to match: the sibling surface now
    expects the anchored form and zero bare targets.

    Scope of the claim, deliberately narrower than the agent body's: the
    documented substitution table covers "Skill and agent content" — the
    registered component content the harness itself loads. These reference
    files are NOT registered components; they are plain files the model opens
    with Read, and the docs are SILENT on whether placeholders are substituted
    inside them (checked 2026-08-17 against code.claude.com's plugins-reference
    and skills pages). The token is used here because it is **self-describing
    and inference-resolvable** — the model reached this file via an already-
    expanded absolute path, so `${CLAUDE_PLUGIN_ROOT}/agents/references/x.md`
    is trivially recoverable, whereas a bare `x.md` requires reconstructing the
    directory from nothing. Do not restate the body's substitution guarantee
    for this surface.

    Raises ValueError on a bare `.md` target that is not an emitted sibling.
    Passing it through would leave the same-class bug alive with no signal;
    anchoring it blindly would mint a broken absolute path. Fail loudly.
    """
    allowed = _agent_ref_allowed_targets()
    unknown: list[str] = []

    def sub(m: re.Match) -> str:
        target = m.group(1)
        if target not in allowed:
            unknown.append(target)
            return m.group(0)
        return f"]({AGENT_REF_PREFIX}{target})"

    rewritten = _BARE_MD_TARGET_RE.sub(sub, text)
    if unknown:
        raise ValueError(
            f"{source_rel}: bare markdown link target(s) {sorted(set(unknown))!r} "
            f"are not files emitted into first-principles/agents/references/. "
            f"Either the filename is a typo, or a new reference file needs "
            f"adding to TOOLS / SLUGS_WITH_DETAIL / SPINE_REFERENCES so "
            f"_agent_ref_allowed_targets() knows about it."
        )
    return rewritten


def _absolutise_skill_peer_links(text: str, source_rel: str) -> str:
    """Retarget bare cross-technique links in a skill stub to the peer stub.

    A stub's `](pre-mortem.md)` pointers are routing prose — "use this other
    technique instead" — and they never resolved: the harness resolves a
    slash-invoked skill against its own directory, so the target read as
    `skills/inversion/pre-mortem.md`, which does not exist. The peer's content
    lives at `skills/pre-mortem/SKILL.md`. Rewritten to
    `${CLAUDE_PLUGIN_ROOT}/skills/<slug>/SKILL.md`.

    MUST run AFTER `_rewrite_detail_link()`. That helper turns the bare
    `<slug>-detail.md` pointer into `references/<slug>-detail.md`, which
    contains a `/` and so no longer matches `_BARE_MD_TARGET_RE` — that
    ordering is what keeps the detail pointer (which already resolves
    correctly against the stub's own directory) out of this rewrite. Running
    them in the other order would mis-target the detail sibling as a peer
    skill.

    Only TOOLS slugs are peers: the other six skills are phase skills with no
    `shared/references/<slug>.md`, so nothing links to them by filename. Any
    other bare `.md` target raises, for the same reason
    `_absolutise_agent_ref_links()` raises — silently passing one through
    would leave a non-resolving link alive with no signal, and VAL-03 now
    full-checks this surface, so a mis-anchored target is caught rather than
    invisible.
    """
    allowed = {f"{slug}.md": slug for slug in TOOLS}
    unknown: list[str] = []

    def sub(m: re.Match) -> str:
        target = m.group(1)
        peer = allowed.get(target)
        if peer is None:
            unknown.append(target)
            return m.group(0)
        return f"]({SKILL_PEER_PREFIX}{peer}/SKILL.md)"

    rewritten = _BARE_MD_TARGET_RE.sub(sub, text)
    if unknown:
        raise ValueError(
            f"{source_rel}: bare markdown link target(s) {sorted(set(unknown))!r} "
            f"in skill-stub content do not name a companion-technique peer "
            f"skill. Cross-technique links must target a TOOLS slug; anything "
            f"else is a typo or needs an explicit decision about where it "
            f"should point on the skill surface."
        )
    return rewritten


def _rewrite_detail_link(slice_text: str, slug: str, prefix: str = "references/") -> str:
    """Rewrite a bare '<slug>-detail.md' pointer target to '<prefix><slug>-detail.md'.

    Exists because the assembled agent body (first-principles/agents/first-
    principles.md) and the skill stub (first-principles/skills/<slug>/SKILL.md)
    each sit one directory level ABOVE where the detail sibling lands
    (agents/references/<slug>-detail.md and skills/<slug>/references/<slug>-
    detail.md respectively), so the bare filename that resolves correctly in
    shared/references/ and in the agent's OWN references/<slug>.md sibling
    (which sits alongside <slug>-detail.md and must NOT be rewritten, DEC-A)
    does not resolve from these two assembly surfaces. `_extract_procedure()`
    and `_extract_skill_content()` deliberately stay source-faithful — their
    raw output keeps the bare-filename form, which is exactly what GATE-02
    asserts against (DEC-B); this helper's rewritten form is a separate
    property asserted against the assembled output instead.

    `prefix` selects the per-surface form. The skill stub keeps the historical
    file-relative `references/` default: a slash-invoked skill is resolved by
    the harness against its own skill directory, so a relative target works
    there. The agent body passes AGENT_REF_PREFIX instead — an agent body is
    read with the *session* working directory in force, not the plugin
    directory, so a file-relative target silently resolves against the user's
    project and the read fails. See AGENT_REF_PREFIX for the full rationale.

    No-op for any slug outside SLUGS_WITH_DETAIL. Matches only the exact
    inline-link target string, not a loose regex, so it cannot match
    anything but the pointer.
    """
    if slug not in SLUGS_WITH_DETAIL:
        return slice_text
    return slice_text.replace(f"]({slug}-detail.md)", f"]({prefix}{slug}-detail.md)")


# v8.5 Phase 154 GATE-02 (D-01 template): the three trigger bullets every
# named-trigger pointer block carries, verbatim, immediately after its
# "**Read [<slug>-detail.md](<slug>-detail.md) when you need:**" line. Kept as
# a module-level tuple (not inlined into _check_detail_pointer) so a future
# change to the template's wording only needs updating here.
_POINTER_TRIGGER_BULLETS = (
    "a worked example of this technique",
    "the failure modes and how to avoid them",
    "handoff guidance to another technique",
)


def _check_detail_pointer(text: str, slug: str) -> list[str]:
    """Check `text` for exactly one well-formed bare detail-sibling pointer.

    Returns a list of problem strings — empty means well-formed. This is the
    ONE shared checker GATE-02's positive control and both negative controls
    (missing, duplicate) all run through: if the positive path and the
    negatives used different code, the negatives would prove nothing about
    what the positive control actually runs (D-11). Checks, in order:

      1. The bare link target '](<slug>-detail.md)' appears in `text` exactly
         once — not zero (missing pointer), not two-or-more (duplicated
         pointer, or the D-11 "at least one" weakness this exists to rule
         out).
      2. When the target count is exactly one, the link's label text is the
         bare filename '<slug>-detail.md' immediately preceding that target —
         catches a pointer that decayed into a bare see-also with different
         label text, which a target-only count would miss.
      3. All three `_POINTER_TRIGGER_BULLETS` are present in `text`.

    Deliberately operates on plain text, not a second markdown parser (D-10)
    — callers pass either `_extract_procedure()`'s real output or an
    in-memory fixture string derived from it; this function itself performs
    no file I/O and mutates nothing.
    """
    problems: list[str] = []
    target = f"]({slug}-detail.md)"
    count = text.count(target)
    if count == 0:
        problems.append(
            f"{slug}: pointer target {target!r} not found in text, expected exactly 1"
        )
    elif count > 1:
        problems.append(
            f"{slug}: pointer target {target!r} found {count} times, "
            f"expected exactly 1"
        )
    else:
        # `target` already begins with the closing ']' of the label bracket
        # pair, so the full label+target span is '[<slug>-detail.md' + target
        # (NOT '[<slug>-detail.md]' + target, which would double the ']').
        label_and_target = f"[{slug}-detail.md{target}"
        if label_and_target not in text:
            problems.append(
                f"{slug}: pointer target found once but its label does not "
                f"match the bare filename {slug}-detail.md — may have decayed "
                f"into a bare see-also"
            )
    for bullet in _POINTER_TRIGGER_BULLETS:
        if bullet not in text:
            problems.append(f"{slug}: missing trigger bullet {bullet!r}")
    return problems


_SKILL_CONTENT_RE = re.compile(
    r"(^## When to reach for this\n.*)\Z",
    re.MULTILINE | re.DOTALL,
)

# v8.5 Phase 154 (D-05): a core-only variant of _SKILL_CONTENT_RE, applied
# ONLY to slugs in SLUGS_WITH_DETAIL. Terminates on either the '## Example'
# heading OR end-of-input — the alternation is mandatory: a lookahead with no
# end-of-input branch would raise on every post-split core file, none of
# which contain an '## Example' heading any more (Plan 02 moved it to the
# detail sibling). Today the two patterns are behaviour-identical on the four
# split files (both match to EOF, byte-for-byte), so this is a guardrail
# against future re-inflation, not a functional change: if a future edit
# re-added an '## Example'-style section to one of the four core files, the
# stub would otherwise silently re-inflate with no gate catching it. Widening
# this pattern's application beyond SLUGS_WITH_DETAIL would silently truncate
# `pre-mortem` and `trade-off`, which also carry an '## Example' heading but
# sit outside v8.5 §2's authorisation — do not broaden the branch below.
_SKILL_CONTENT_CORE_ONLY_RE = re.compile(
    r"(^## When to reach for this\n.*?)(?=^## Example\b|\Z)",
    re.MULTILINE | re.DOTALL,
)


def _extract_skill_content(slug: str) -> str:
    """Extract the inline-copy region for a focused-mode stub body.

    Returns the slice of `shared/references/{slug}.md` starting at the
    `## When to reach for this` heading through end-of-file (covers When /
    Framing (where present) / Procedure / Example / Failure modes / Handoff
    — i.e. everything except the H1 title block and the leading blockquote).
    This is the content 46-RESEARCH.md §Q1 specifies for inline-copy under
    Option A. Distinct from `_extract_procedure()` (which inlines only the
    `## Procedure` section into the composer agent body) — these two
    surfaces have different inclusion contracts and must not share an extractor.

    The 80-LOC stub floor (46-02-PLAN.md must_haves) is achieved only when
    this slice is the inlined content; substituting `_extract_procedure()`
    here would produce stubs in the 45-55 LOC range and falsify the
    "procedure inlined" truth.

    v8.5 Phase 154 (D-05): for slugs in SLUGS_WITH_DETAIL, uses
    `_SKILL_CONTENT_CORE_ONLY_RE` instead of `_SKILL_CONTENT_RE` — a clamp
    that terminates the slice at the '## Example' heading (or EOF, whichever
    comes first) rather than always running to EOF. This is a guardrail, not
    a behaviour change today: the four split core files contain no '## Example'
    heading, so the clamp produces byte-identical output to the unclamped
    pattern on the current tree. It exists so a future re-inflation of one of
    the four core files with an appendix-style section is caught rather than
    silently inlined into the stub. The other nine SKILLS slugs keep
    `_SKILL_CONTENT_RE` exactly as it was — widening the clamp beyond
    SLUGS_WITH_DETAIL would silently truncate `pre-mortem` and `trade-off`,
    which carry the same heading and sit outside v8.5 §2's authorisation.

    Raises ValueError if the anchor heading is absent.
    """
    body = _read_required(
        SHARED / "references" / f"{slug}.md",
        hint=(
            f"shared/references/{slug}.md is required for the focused-mode "
            f"stub at first-principles/skills/{slug}/SKILL.md"
        ),
    )
    pattern = (
        _SKILL_CONTENT_CORE_ONLY_RE if slug in SLUGS_WITH_DETAIL else _SKILL_CONTENT_RE
    )
    m = pattern.search(body)
    if not m:
        raise ValueError(
            f"shared/references/{slug}.md has no '## When to reach for this' "
            f"heading — required as the inline-copy anchor for "
            f"first-principles/skills/{slug}/SKILL.md"
        )
    return _normalise_trailing_newline(m.group(1))


def _expand_skill_token(body: str, slug: str) -> str:
    """Replace `{{PROCEDURE:<slug>}}` with the inlined skill content.

    The token MUST appear at least once in the source body. The slug captured
    by the token MUST equal the stub's own slug — cross-slug token references
    (e.g. a pre-mortem stub embedding `{{PROCEDURE:inversion}}`) are rejected
    so the sync pipeline cannot silently propagate the wrong technique's
    procedure into a stub.
    """
    seen = 0

    def sub(m: re.Match) -> str:
        nonlocal seen
        seen += 1
        captured = m.group(1)
        if captured != slug:
            raise ValueError(
                f"shared/skills/{slug}/SKILL.md contains "
                f"{{{{PROCEDURE:{captured}}}}} — token slug must match the "
                f"stub's own slug ({slug!r})"
            )
        # Order is load-bearing: _rewrite_detail_link first (it gives the
        # detail pointer a `/`, taking it out of _BARE_MD_TARGET_RE's reach),
        # then peer retargeting over what remains. See
        # _absolutise_skill_peer_links().
        expanded = _rewrite_detail_link(_extract_skill_content(slug), slug)
        expanded = _absolutise_skill_peer_links(
            expanded, f"shared/references/{slug}.md (-> skills/{slug}/SKILL.md)"
        )
        return expanded.rstrip("\n")

    out = SKILL_TOKEN_RE.sub(sub, body)
    if seen == 0 and slug not in LAUNCHER_SKILLS:
        raise ValueError(
            f"shared/skills/{slug}/SKILL.md is missing the required "
            f"{{{{PROCEDURE:{slug}}}}} token — without it the stub body "
            f"falls below the 80-LOC floor and the inline-copy contract "
            f"(46-02-PLAN must_haves) is violated"
        )
    if seen and slug in LAUNCHER_SKILLS:
        raise ValueError(
            f"shared/skills/{slug}/SKILL.md is a launcher stub "
            f"(LAUNCHER_SKILLS) but contains a {{{{PROCEDURE:{slug}}}}} token. "
            f"A launcher dispatches the composer agent and must not inline a "
            f"technique procedure — remove the token or drop the slug from "
            f"LAUNCHER_SKILLS."
        )
    return out


def _expand_focused_validation_token(body: str, slug: str) -> str:
    """Replace `{{FOCUSED_VALIDATION}}` with the canonical validation snippet.

    Mirrors `_expand_skill_token()`'s enforcement shape (missing-token raise,
    launcher raise) but differs in the one structural way the token itself
    differs: it takes no slug argument and resolves from ONE fixed path
    (`FOCUSED_VALIDATION_SOURCE`), not a per-slug reference file. Because
    there is no capture group, the substitution is a plain fixed-string
    replacement, not a `sub(m)` callback that inspects `m.group(1)`.

    Must be called AFTER `_expand_skill_token()` has produced its result, and
    must NOT be folded inside it — this substitution runs on `expanded_body`,
    the already-expanded `{{PROCEDURE:<slug>}}` output. Because of that
    ordering, this snippet never passes through `_absolutise_skill_peer_links()`
    (which only runs inside `_expand_skill_token()`'s `sub()` callback), so a
    bare `.md` link in the snippet would ship broken instead of raising —
    guard 1 below exists to make that case raise here instead.
    """
    snippet = _read_required(
        FOCUSED_VALIDATION_SOURCE,
        hint=(
            "shared/spine/focused-validation-step.md is required as the "
            "single source for the {{FOCUSED_VALIDATION}} token inlined into "
            "every non-launcher skill stub (03-02-PLAN.md, PAR-02)"
        ),
    )

    # Guard 1 (bare-link guard): this snippet is inlined AFTER
    # _expand_skill_token() returns, so it never passes through
    # _absolutise_skill_peer_links(). A bare `.md` link here would ship as a
    # broken link instead of raising at generation time.
    bare_targets = sorted(set(_BARE_MD_TARGET_RE.findall(snippet)))
    if bare_targets:
        raise ValueError(
            f"shared/spine/focused-validation-step.md contains bare "
            f"markdown link target(s) {bare_targets!r}. This file is "
            f"inlined after _expand_skill_token() returns, so it never "
            f"passes through _absolutise_skill_peer_links() — a bare link "
            f"here would ship broken instead of raising. Remove the link."
        )

    # Guard 2: a nested {{...}} marker surviving into the emitted stub. This
    # is a GENERATION-TIME guard, not a downstream safety net —
    # check-agent.py is agent-only (CI passes it only the agent body, never
    # a skill stub) and cannot see this surface. The emitted-stub surface is
    # scanned for a surviving marker by HARN-03's `Stub-12`
    # (`scripts/check-focused-parity.py`, 03-05 Task 3), not by
    # check-agent.py.
    if "{{" in snippet:
        raise ValueError(
            f"shared/spine/focused-validation-step.md contains a nested "
            f"'{{{{' token sequence. A surviving marker would ship into "
            f"every emitted stub unresolved — remove the nested token."
        )

    replacement = snippet.rstrip("\n")
    seen = len(FOCUSED_VALIDATION_TOKEN_RE.findall(body))
    out = FOCUSED_VALIDATION_TOKEN_RE.sub(lambda m: replacement, body)

    if seen == 0 and slug not in LAUNCHER_SKILLS:
        raise ValueError(
            f"shared/skills/{slug}/SKILL.md is missing the required "
            f"{{{{FOCUSED_VALIDATION}}}} token — without it the emitted "
            f"stub has no Observe limb, violating PAR-02 (PAR-02 is "
            f"unconditional: documentation alone cannot satisfy it)."
        )
    if seen and slug in LAUNCHER_SKILLS:
        raise ValueError(
            f"shared/skills/{slug}/SKILL.md is a launcher stub "
            f"(LAUNCHER_SKILLS) but contains a {{{{FOCUSED_VALIDATION}}}} "
            f"token. A launcher dispatches the composer agent, which "
            f"already runs Phase 5 — it must not carry the token."
        )
    return out


def generate_skill_stub(slug: str) -> tuple[Path, str]:
    """Return (target_path, content) for one focused-mode stub.

    Reads `shared/skills/{slug}/SKILL.md`, expands the `{{PROCEDURE:<slug>}}`
    token via `_expand_skill_token`, and stamps the DO-NOT-EDIT marker line
    immediately after the closing `---` frontmatter delimiter (Pitfall 7).

    Frontmatter is passed through verbatim — including `disable-model-invocation:
    true` and `metadata.version: "3.8.0"` per DEC-46-B. The frontmatter shape is
    NOT re-emitted via PyYAML to avoid normalising the source author's quoting
    style; the source file is authored once and propagated byte-faithfully (the
    YAML re-emission path is reserved for files where shared/ stores a meta
    dict, e.g. `shared/spine/SKILL.meta.yml`).
    """
    source_path = SHARED / "skills" / slug / "SKILL.md"
    source = _read_required(
        source_path,
        hint=(
            f"shared/skills/{slug}/SKILL.md is required as the source for "
            f"first-principles/skills/{slug}/SKILL.md (Phase 46-02)"
        ),
    )

    # Split frontmatter from body: must open with `---\n` and contain a closing
    # `---\n` line. Reject sources that lack frontmatter — the stub contract
    # requires `name`, `disable-model-invocation`, and `metadata.version` keys.
    lines = source.split("\n")
    if not lines or lines[0] != "---":
        raise ValueError(
            f"shared/skills/{slug}/SKILL.md missing opening '---' frontmatter "
            f"delimiter"
        )
    try:
        close_idx = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError(
            f"shared/skills/{slug}/SKILL.md missing closing '---' frontmatter "
            f"delimiter"
        ) from exc

    frontmatter_block = "\n".join(lines[: close_idx + 1]) + "\n"
    body_block = "\n".join(lines[close_idx + 1 :])

    # Sanity: required frontmatter keys must be literally present so a CI
    # diff (`--check`) makes their removal a visible drift.
    for required in ("name:", "disable-model-invocation:", "version:"):
        if required not in frontmatter_block:
            raise ValueError(
                f"shared/skills/{slug}/SKILL.md frontmatter missing required "
                f"key fragment {required!r} (DEC-46-B)"
            )

    expanded_body = _expand_skill_token(body_block, slug)
    expanded_body = _expand_focused_validation_token(expanded_body, slug)
    do_not_edit = SKILL_DO_NOT_EDIT_LINE.format(slug=slug)
    # Place DO-NOT-EDIT line immediately after the closing `---` line, with a
    # single blank line separator so the marker reads as its own paragraph and
    # markdown renderers don't fold it into the next block.
    assembled = (
        frontmatter_block
        + do_not_edit
        + (expanded_body if expanded_body.startswith("\n") else "\n" + expanded_body)
    )
    content = _normalise_trailing_newline(assembled)
    return SKILLS_DIR / slug / "SKILL.md", content


def _warn_orphan_skill_dirs(skills_root: Path | None = None) -> list[str]:
    """Warn (non-fatally) about any shared/skills/<dir> that lacks a SKILL.md.

    Iterates the immediate subdirectories of skills_root (default: SHARED/"skills")
    and writes a single stderr advisory for each subdir that has no SKILL.md — the
    dir is skipped by the generator and generates nothing.  Returns the sorted list
    of orphan subdir names.  Never raises and never changes the exit code (D-05:
    the guard is informational only; a transient empty dir must not block --check).

    The skills_root parameter lets --self-test (and unit fixtures) point the guard
    at a temp directory without touching the real shared/skills/ tree.
    """
    if skills_root is None:
        skills_root = SHARED / "skills"
    if not skills_root.is_dir():
        # Missing or non-directory root: nothing to warn about. Stay non-fatal
        # per D-05 so the structured downstream error in generate_all() (the
        # _read_required() path) remains the single source of truth.
        return []
    orphans: list[str] = []
    for subdir in sorted(skills_root.iterdir()):
        if subdir.is_dir() and not (subdir / "SKILL.md").exists():
            sys.stderr.write(
                f"WARNING: {subdir.name!r} skipped — no SKILL.md found; generates nothing\n"
            )
            orphans.append(subdir.name)
    return sorted(orphans)


def generate_skill_stubs() -> dict[Path, str]:
    """Return {target_path: content} for every focused-mode stub (Phase 46-02).

    One target per slug in SKILLS. The byte-identity gate enforced by
    `cmd_check()` rejects any hand-edit to the generated files (Pitfall 7).
    """
    targets: dict[Path, str] = {}
    for slug in SKILLS:
        path, content = generate_skill_stub(slug)
        targets[path] = content
    return targets


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

    # --- Companion Techniques: 7 ## Procedure sections in TOOLS order ---
    companion_header = "\n## Companion Techniques\n\n"
    companion_blocks = "".join(
        _rewrite_detail_link(_extract_procedure(slug), slug, AGENT_REF_PREFIX) + "\n"
        for slug in TOOLS
    )

    # --- Assemble body and stitch frontmatter ---
    # NOTE: output-template.md and validation-rubric.md are intentionally NOT
    # inlined here (Phase 34-02, Path B). They reach the agent only as sibling
    # reference files via generate_agent_spine_references(); the spine body
    # links to them with file-relative markdown links.
    # Primary canonical source = shared/spine/SKILL-body.md (the bulk of the
    # assembled body). Frontmatter (shared/spine/SKILL.meta.yml) and the
    # inlined companion-technique procedures (shared/references/<slug>.md)
    # are secondary sources reachable as siblings of the primary — name only
    # the primary here so the marker remains a navigable path, matching the
    # source_rel shape used by every other call site (WR-02).
    agent_marker = GENERATED_MARKER.format(source_rel="spine/SKILL-body.md")
    body = _normalise_trailing_newline(
        agent_marker
        + "\n"
        + input_contract
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
    """Return {AGENT_DIR/references/{slug}.md: body} for the 8 companion tools.

    Source = shared/references/{slug}.md (the canonical tree). Per D-01/D-02,
    the agent's on-demand reference siblings ship verbatim — NO frontmatter,
    NO `{{TOOL:<slug>}}` marker expansion. Trailing newline normalised to
    exactly one.

    ONE exception to verbatim, added at v8.17.4: bare sibling-filename link
    targets are anchored by `_absolutise_agent_ref_links()`, because a model
    reading this file does so with the session working directory in force, not
    this directory. That overturns DEC-A — see that function's docstring. The
    source in shared/ deliberately keeps the bare form: it also feeds the skill
    stubs, whose correct target is a different path.

    A `GENERATED_MARKER` HTML-comment line is prepended (followed by a blank
    line) so code reviewers and the .reviewignore consumer can shortcut the
    mirror. The marker is markdown-inert and counts as two added lines per
    file; the source body itself is otherwise unmodified.
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
        body = _absolutise_agent_ref_links(body, f"shared/references/{slug}.md")
        marker = GENERATED_MARKER.format(source_rel=f"references/{slug}.md")
        targets[AGENT_DIR / "references" / f"{slug}.md"] = (
            _normalise_trailing_newline(marker + "\n" + body)
        )
    return targets


def generate_agent_detail_references() -> dict[Path, str]:
    """Return {AGENT_DIR/references/{slug}-detail.md: body} for SLUGS_WITH_DETAIL.

    Source = shared/references/{slug}-detail.md (Plan 02's four new canonical
    detail siblings). Mirrors generate_agent_references() line for line,
    changing only the iterated set (SLUGS_WITH_DETAIL instead of TOOLS), the
    source suffix (-detail.md), and the target filename. Per D-01/D-02, ships
    verbatim — NO frontmatter, NO `{{TOOL:<slug>}}` marker expansion. Trailing
    newline normalised to exactly one.

    Runs `_absolutise_agent_ref_links()` for the same reason its sibling
    emitter does — a model reads this file with the session working directory
    in force, not this directory. These four files carry ZERO relative links
    today, so the call is currently a no-op; it is wired anyway so a future
    back-link added to a detail appendix cannot reintroduce the second-hop
    break silently. No positive assertion is made about link forms here: with
    zero links present it would be vacuous, so GATE-02-v8.5 checks only that
    no bare target survives.

    A `GENERATED_MARKER` HTML-comment line is prepended (same shape as
    generate_agent_references()), followed by `DETAIL_SIBLING_LINT_EXEMPT` —
    see that constant's docstring for why (VAL-02/MD041, Plan 02's frozen
    no-H1 source shape).
    """
    targets: dict[Path, str] = {}
    for slug in SLUGS_WITH_DETAIL:
        body = _read_required(
            SHARED / "references" / f"{slug}-detail.md",
            hint=(
                f"shared/references/{slug}-detail.md is required for the "
                f"agent's on-demand detail sibling at "
                f"first-principles/agents/references/{slug}-detail.md"
            ),
        )
        body = _absolutise_agent_ref_links(
            body, f"shared/references/{slug}-detail.md"
        )
        marker = GENERATED_MARKER.format(source_rel=f"references/{slug}-detail.md")
        targets[AGENT_DIR / "references" / f"{slug}-detail.md"] = (
            _normalise_trailing_newline(
                marker + "\n" + DETAIL_SIBLING_LINT_EXEMPT + "\n" + body
            )
        )
    return targets


def generate_skill_detail_references() -> dict[Path, str]:
    """Return {SKILLS_DIR/{slug}/references/{slug}-detail.md: body} for SLUGS_WITH_DETAIL.

    Source = shared/references/{slug}-detail.md — the same source tree
    `generate_agent_detail_references()` reads. Mirrors that function's shape
    exactly, changing only the target root: under the per-slug skill
    directory's own `references/` subdirectory rather than
    `AGENT_DIR/references/`. That subdirectory does not exist on disk before
    this plan runs; `cmd_write()` already creates missing parent directories
    (`path.parent.mkdir(parents=True, exist_ok=True)`) before writing, so no
    extra directory-creation code is needed here. The target resolves inside
    `SKILLS_DIR`, so it passes `generate_all()`'s existing path-safety
    assertion unmodified.

    A `GENERATED_MARKER` HTML-comment line is prepended, followed by
    `DETAIL_SIBLING_LINT_EXEMPT` (see that constant's docstring — VAL-02/
    MD041, Plan 02's frozen no-H1 source shape). Trailing newline normalised
    to exactly one.
    """
    targets: dict[Path, str] = {}
    for slug in SLUGS_WITH_DETAIL:
        body = _read_required(
            SHARED / "references" / f"{slug}-detail.md",
            hint=(
                f"shared/references/{slug}-detail.md is required for the "
                f"skill stub's on-demand detail sibling at "
                f"first-principles/skills/{slug}/references/{slug}-detail.md"
            ),
        )
        marker = GENERATED_MARKER.format(source_rel=f"references/{slug}-detail.md")
        targets[SKILLS_DIR / slug / "references" / f"{slug}-detail.md"] = (
            _normalise_trailing_newline(
                marker + "\n" + DETAIL_SIBLING_LINT_EXEMPT + "\n" + body
            )
        )
    return targets


def generate_agent_spine_references() -> dict[Path, str]:
    """Return {AGENT_DIR/references/{slug}.md: body} for canonical spine references.

    Source = shared/spine/references/{slug}.md for each slug in SPINE_REFERENCES.
    Mirrors generate_agent_references() exactly: verbatim file copy, trailing-
    newline normalisation, NO frontmatter injection, NO `{{TOOL:<slug>}}` marker
    expansion, NO edits to the source body. A `GENERATED_MARKER` HTML-comment
    line is prepended (same shape as generate_agent_references). This is the
    post-Plan-26.1 spine-reference sync path — distinct from the 6 tool
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
        marker = GENERATED_MARKER.format(source_rel=f"spine/references/{slug}.md")
        targets[AGENT_DIR / "references" / f"{slug}.md"] = (
            _normalise_trailing_newline(marker + "\n" + body)
        )
    return targets


def generate_agent_examples() -> dict[Path, str]:
    """Return {AGENT_DIR/references/examples/{name}.md: body} for the 12 worked examples.

    Source = shared/examples/{name}.md (the source-of-truth tree established
    in Plan 26.1-03 Task 0 — NOT the monolith path). This preserves the
    single-source-of-truth invariant past Plan 05's monolith deletion:
    shared/examples/ survives, this generator survives, and the sync-drift
    CI gate continues to enforce byte-identity between source and emission.

    Per D-01 amended / MIGRATE-02 amended / E-3 resolution: verbatim copy of
    the source body — NO frontmatter, NO `{{TOOL:<slug>}}` marker expansion,
    NO edits to the source body. A `GENERATED_MARKER` HTML-comment line is
    prepended (same shape as generate_agent_references). Trailing newline
    normalised.
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
        marker = GENERATED_MARKER.format(source_rel=f"examples/{name}.md")
        targets[AGENT_DIR / "references" / "examples" / f"{name}.md"] = (
            _normalise_trailing_newline(marker + "\n" + body)
        )
    return targets


def generate_all() -> dict[Path, str]:
    """Return {target_path: content} for every emitted file.

    Phase 52 extended SKILLS to 11 entries; v7.1 (Phase 101) adds decompose,
    bringing TOOLS to 7, SKILLS to 12, and EXAMPLES to 12.
    v7.5 (Phase 110) folds decompose into five-whys and removes the standalone
    decompose surface, bringing TOOLS to 8, SKILLS to 13, and EXAMPLES to 14
    (the worked example file is kept at its current path per D-04, rebranded).
    v8.5 Phase 154 (MECH-01/MECH-02) adds the on-demand load mechanism: four
    core reference files (SLUGS_WITH_DETAIL) each carry a named-trigger
    pointer to a new `-detail.md` sibling, emitted on two surfaces (8 new
    generated files), raising the count below from its prior value.
    Current target count: 47 total.

      - 1 agent SKILL.md (first-principles/agents/first-principles.md)
      - 11 agent reference siblings (first-principles/agents/references/*.md:
        8 companion-tool refs + assumption-taxonomy + output-template + validation-rubric)
      - 4 agent detail siblings (first-principles/agents/references/<slug>-detail.md,
        SLUGS_WITH_DETAIL: five-whys, theoretical-limit, estimate, fishbone)
      - 14 agent worked-example siblings (first-principles/agents/references/examples/<name>.md)
      - 13 slash-invocable focused-mode stubs (first-principles/skills/<slug>/SKILL.md)
      - 4 skill detail siblings (first-principles/skills/<slug>/references/<slug>-detail.md,
        same SLUGS_WITH_DETAIL set)
    Total: 1 + 11 + 4 + 14 + 13 + 4 = 47.

    Note: the total count (47) reflects the 8 TOOLS + 3 spine-refs (for the
    reference siblings), 4 SLUGS_WITH_DETAIL (doubled — once per agent surface,
    once per skill surface), 14 EXAMPLES, and 13 SKILLS. generate_all() now
    gates on this count via the GENERATED_TARGET_COUNT invariant (raises on
    drift), and the sync-content.py --check pass additionally validates
    byte-identity per-file.
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

    # --- Agent surface ---
    targets.update(generate_agent(spine_meta, tool_map))
    targets.update(generate_agent_references())
    targets.update(generate_agent_detail_references())
    targets.update(generate_agent_spine_references())
    targets.update(generate_agent_examples())

    # --- Slash-invocable focused-mode stubs (Phase 46-02) ---
    # disable-model-invocation: true on every stub → no orchestrator
    # auto-routing; only `/first-principles:<slug>` slash invocation loads them.
    targets.update(generate_skill_stubs())
    targets.update(generate_skill_detail_references())

    # --- Path-safety assertion (V12 ASVS): every write path must live inside
    #     an allowed write root.
    # Use Path.relative_to() rather than str.startswith() to avoid sibling-dir
    # false positives (WR-01).
    allowed_roots = (AGENT_DIR, SKILLS_DIR)
    for path in targets:
        if not any(_is_within(path, root) for root in allowed_roots):
            raise ValueError(
                f"Generated path {path} resolves outside allowed trees "
                f"{[str(r) for r in allowed_roots]}"
            )

    # --- Count invariant (DEBT-02 / D-01): len(targets) must match the documented
    # constant so any future surface-change is caught immediately on --check/--write.
    # Use explicit if/raise (not assert) so the check survives python -O.
    if len(targets) != GENERATED_TARGET_COUNT:
        raise ValueError(
            f"generate_all() produced {len(targets)} targets but "
            f"GENERATED_TARGET_COUNT == {GENERATED_TARGET_COUNT}. "
            f"Update GENERATED_TARGET_COUNT (and the docstrings) when the "
            f"generated surface legitimately changes."
        )

    return targets


def cmd_write() -> int:
    _warn_orphan_skill_dirs()
    targets = generate_all()
    for path, content in targets.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        # newline='\n' pins LF on every platform (Pitfall 9 / CLAUDE.md mandate).
        path.write_text(content, encoding="utf-8", newline="\n")
    print(f"wrote {len(targets)} files")
    return 0


def cmd_check() -> int:
    _warn_orphan_skill_dirs()
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


def cmd_self_test() -> int:
    """Prove both DEBT guards are non-vacuous.  Returns 0 on all-pass, 1 on any failure.

    (a) Count positive control: len(generate_all()) == GENERATED_TARGET_COUNT.
    (b) Count negative control: temporarily set GENERATED_TARGET_COUNT to a wrong value
        and assert generate_all() raises ValueError, then restore the original.  Proves
        the raise-on-drift guard actually fires.
    (c) Orphan-guard teeth: create a temp dir with one SKILL.md-less subdir and one with
        a SKILL.md; assert _warn_orphan_skill_dirs distinguishes them correctly.

    v8.5 Phase 154 GATE-02 (D-11 full control set) — proves the named-trigger
    detail-sibling pointer authored by Plan 03 exists and is well-formed after
    every regeneration. Explicitly NOT proof that the pointer is followed
    (Phase 156's live question).

    (d) GATE-02 positive control: `_check_detail_pointer()` (the ONE shared
        checker also used by (e) and (f)) reports zero problems against
        `_extract_procedure()`'s real output, for every SLUGS_WITH_DETAIL slug.
    (e) GATE-02 negative control 1 (missing): strip the pointer from an
        in-memory copy of the real output; the shared checker must report a
        problem for every slug. Operates on a fixture string, never a real
        file, so a crashed run cannot leave the repo mutated.
    (f) GATE-02 negative control 2 (duplicate): append a second copy of the
        real output to itself; the shared checker must report a problem
        whose text cites the count (not merely "failed") for every slug — a
        checker that silently accepts two-or-more would pass a weaker
        "at least one present" assertion, the exact D-11 weakness this rules
        out.
    (g) GATE-02 rewrite assertion: a distinct property from (d)-(f)'s
        bare-form check (DEC-B, 154-01-SUMMARY.md) — the rewritten
        `references/`-prefixed form appears exactly once per slug in the
        assembled agent body and the skill stub, while the agent reference
        sibling still carries the bare (unrewritten) form. Driven off
        `generate_all()`'s in-memory return value, never files on disk.
    (h) GATE-02 dispatch control (Phase 152 WR-01 lesson): drives
        `main(["--self-test"])` and asserts its return code and captured
        stdout, proving the CLI dispatch branch itself reaches (d)'s PASS
        text — not just that this function is correct when called directly.
        Guarded by the module-level `_GATE02_DISPATCH_REENTRANT` sentinel
        (set only for the duration of the nested call, restored in a
        `finally` clause) so the nested invocation cannot recurse into its
        own dispatch control.
    """
    import contextlib
    import io
    import tempfile

    failures: list[str] = []

    # (a) Count positive control.
    try:
        result = generate_all()
        if len(result) != GENERATED_TARGET_COUNT:
            failures.append(
                f"FAIL (a): len(generate_all()) == {len(result)}, "
                f"expected {GENERATED_TARGET_COUNT}"
            )
        else:
            print(f"(a) count positive control: PASS — {len(result)} targets")
    except Exception as exc:
        failures.append(f"FAIL (a): generate_all() raised unexpectedly: {exc}")

    # (b) Count negative control — temporarily set GENERATED_TARGET_COUNT to wrong value.
    original_count = GENERATED_TARGET_COUNT
    # Reference the module-level variable via the module's globals dict so the
    # generate_all() closure sees the patched value (same module, no importlib needed).
    _this_module = sys.modules[__name__]
    try:
        _this_module.GENERATED_TARGET_COUNT = original_count + 1  # wrong value
        try:
            generate_all()
            failures.append("FAIL (b): generate_all() did NOT raise on wrong count")
        except ValueError:
            print("(b) count negative control: PASS — generate_all() raised ValueError on drift")
        except Exception as exc:
            failures.append(f"FAIL (b): unexpected exception type: {exc!r}")
    finally:
        _this_module.GENERATED_TARGET_COUNT = original_count  # always restore

    # (c) Orphan-guard teeth.
    try:
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "orphan").mkdir()  # no SKILL.md — must be flagged
            good = root / "good"
            good.mkdir()
            (good / "SKILL.md").write_text("x")
            err_buf = io.StringIO()
            with contextlib.redirect_stderr(err_buf):
                names = _warn_orphan_skill_dirs(root)
            if "orphan" not in names:
                failures.append("FAIL (c): 'orphan' not in returned orphan list")
            elif "good" in names:
                failures.append("FAIL (c): 'good' (has SKILL.md) wrongly flagged as orphan")
            elif "orphan" not in err_buf.getvalue():
                failures.append("FAIL (c): guard did not write 'orphan' to stderr")
            else:
                print("(c) orphan-guard teeth: PASS — flags SKILL.md-less, skips SKILL.md-present")
    except Exception as exc:
        failures.append(f"FAIL (c): unexpected exception: {exc!r}")

    # (d) GATE-02 positive control: the real extractor output must be clean.
    try:
        problems: list[str] = []
        for slug in sorted(SLUGS_WITH_DETAIL):
            problems.extend(_check_detail_pointer(_extract_procedure(slug), slug))
        if problems:
            failures.append(
                f"FAIL (d): GATE-02 positive control found problems in the "
                f"real extractor output: {problems!r}"
            )
        else:
            print(
                f"(d) GATE-02 pointer positive control: PASS — all "
                f"{len(SLUGS_WITH_DETAIL)} slugs carry exactly one "
                f"well-formed detail-sibling pointer"
            )
    except Exception as exc:
        failures.append(f"FAIL (d): unexpected exception: {exc!r}")

    # (e) GATE-02 negative control 1 (missing) — stripping the pointer from an
    # in-memory fixture must make the shared checker report a problem.
    try:
        missed: list[str] = []
        for slug in sorted(SLUGS_WITH_DETAIL):
            real_slice = _extract_procedure(slug)
            stripped = real_slice.replace(f"({slug}-detail.md)", "(REMOVED)")
            if not _check_detail_pointer(stripped, slug):
                missed.append(slug)
        if missed:
            failures.append(
                f"FAIL (e): GATE-02 negative control (missing) did NOT fail "
                f"for slugs {missed!r} — the checker silently accepts a "
                f"stripped pointer"
            )
        else:
            print(
                f"(e) GATE-02 pointer negative control (missing): PASS — "
                f"stripping the pointer fails the checker for all "
                f"{len(SLUGS_WITH_DETAIL)} slugs"
            )
    except Exception as exc:
        failures.append(f"FAIL (e): unexpected exception: {exc!r}")

    # (f) GATE-02 negative control 2 (duplicate) — the failure must cite the
    # count as the cause, not merely report "failed" (D-11).
    try:
        missed = []
        wrong_reason: list[tuple[str, list[str]]] = []
        for slug in sorted(SLUGS_WITH_DETAIL):
            real_slice = _extract_procedure(slug)
            dup = real_slice + real_slice
            dup_problems = _check_detail_pointer(dup, slug)
            if not dup_problems:
                missed.append(slug)
            elif not any("expected exactly 1" in p for p in dup_problems):
                wrong_reason.append((slug, dup_problems))
        if missed:
            failures.append(
                f"FAIL (f): GATE-02 negative control (duplicate) did NOT "
                f"fail for slugs {missed!r}"
            )
        elif wrong_reason:
            failures.append(
                f"FAIL (f): GATE-02 negative control (duplicate) failed for "
                f"the wrong reason (must cite the count): {wrong_reason!r}"
            )
        else:
            print(
                f"(f) GATE-02 pointer negative control (duplicate): PASS — "
                f"duplicating the pointer fails the checker, citing the "
                f"count, for all {len(SLUGS_WITH_DETAIL)} slugs"
            )
    except Exception as exc:
        failures.append(f"FAIL (f): unexpected exception: {exc!r}")

    # (g) GATE-02 rewrite assertion — a distinct property from (d)-(f)'s
    # bare-form check (DEC-B, 154-01-SUMMARY.md): the rewritten form must
    # appear exactly once per slug in the assembled agent body and the skill
    # stub; the agent reference sibling must still carry the bare form.
    # Driven off generate_all()'s in-memory return value, never files on disk.
    #
    # The two assembly surfaces now expect DIFFERENT rewritten forms. The
    # agent body carries the plugin-root-anchored AGENT_REF_PREFIX (an agent
    # body is read with the session working directory in force, so a
    # file-relative target does not resolve — see AGENT_REF_PREFIX); the skill
    # stub keeps the file-relative `references/` form, which the harness does
    # resolve against the skill's own directory. Asserting per-surface is what
    # stops the agent body silently regressing to the non-resolving form.
    try:
        wrong: list[str] = []
        all_targets = generate_all()
        agent_body = all_targets[AGENT_PATH]
        for slug in sorted(SLUGS_WITH_DETAIL):
            rewritten = f"](references/{slug}-detail.md)"
            agent_rewritten = f"]({AGENT_REF_PREFIX}{slug}-detail.md)"
            bare = f"]({slug}-detail.md)"

            body_count = agent_body.count(agent_rewritten)
            if body_count != 1:
                wrong.append(
                    f"{slug}: agent body carries the plugin-root-anchored "
                    f"pointer {agent_rewritten!r} {body_count} times, "
                    f"expected exactly 1"
                )

            # The agent body must carry NO file-relative pointer form: one
            # would resolve against the user's session directory and fail.
            body_relative = agent_body.count(rewritten)
            if body_relative != 0:
                wrong.append(
                    f"{slug}: agent body carries the file-relative pointer "
                    f"{rewritten!r} {body_relative} times, expected 0 — a "
                    f"file-relative target does not resolve from an agent body"
                )

            stub_content = all_targets.get(SKILLS_DIR / slug / "SKILL.md", "")
            stub_count = stub_content.count(rewritten)
            if stub_count != 1:
                wrong.append(
                    f"{slug}: skill stub carries the rewritten pointer "
                    f"{stub_count} times, expected exactly 1"
                )

            # v8.17.4 overturns DEC-A. The sibling used to be asserted to KEEP
            # the bare pointer, on the reasoning that it lands in the same
            # directory as its detail file. That reasoning held for the
            # filesystem and failed for the reader: a model opens this file
            # with the session working directory in force, so the bare target
            # resolved against the user's project and the second hop
            # (references/five-whys.md -> five-whys-detail.md) broke exactly
            # as the first hop did before v8.17.3. The assertion is inverted:
            # anchored exactly once, bare zero times.
            ref_content = all_targets.get(
                AGENT_DIR / "references" / f"{slug}.md", ""
            )
            ref_anchored_count = ref_content.count(agent_rewritten)
            if ref_anchored_count != 1:
                wrong.append(
                    f"{slug}: agent reference sibling carries the "
                    f"plugin-root-anchored pointer {agent_rewritten!r} "
                    f"{ref_anchored_count} times, expected exactly 1 "
                    f"(DEC-A overturned at v8.17.4)"
                )
            ref_bare_count = ref_content.count(bare)
            if ref_bare_count != 0:
                wrong.append(
                    f"{slug}: agent reference sibling still carries the bare "
                    f"pointer {bare!r} {ref_bare_count} times, expected 0 — a "
                    f"bare target does not resolve from a session working "
                    f"directory (DEC-A overturned at v8.17.4)"
                )

        # Directory-wide sweep. The per-slug loop above only covers the four
        # SLUGS_WITH_DETAIL pointers; the second-hop break also came from 12
        # cross-technique links (](pre-mortem.md), ](inversion.md), …) that no
        # per-slug assertion would ever reach. Assert the property that
        # actually matters — NO emitted agent reference file carries a bare
        # markdown target — over every file in that directory, so a newly
        # added cross-link cannot reintroduce the bug in a file this loop
        # does not name.
        ref_dir = AGENT_DIR / "references"
        swept = 0
        for path, content in all_targets.items():
            if path.parent != ref_dir or path.suffix != ".md":
                continue
            swept += 1
            leftover = sorted(set(_BARE_MD_TARGET_RE.findall(content)))
            if leftover:
                wrong.append(
                    f"{path.name}: carries bare markdown target(s) {leftover!r} "
                    f"— every link in an agent reference file must be "
                    f"plugin-root-anchored (DEC-A overturned at v8.17.4)"
                )
        if swept == 0:
            wrong.append(
                "directory-wide bare-target sweep matched ZERO agent reference "
                "files — the sweep is vacuous, so its clean result proves "
                "nothing"
            )

        # Same sweep over the skill-stub surface (v8.17.5, D-02 closed). The
        # 12 cross-technique links now target the peer stub; the only relative
        # targets that may survive here are the four
        # `references/<slug>-detail.md` pointers, which resolve against the
        # stub's own directory and carry a `/`, so _BARE_MD_TARGET_RE does not
        # match them. Any BARE target reaching a stub is a link that will not
        # resolve — VAL-03 full-checks this surface now, but this catches it
        # at generation with a message that names the cause.
        stub_swept = 0
        for path, content in all_targets.items():
            if path.name != "SKILL.md" or path.parent.parent != SKILLS_DIR:
                continue
            stub_swept += 1
            leftover = sorted(set(_BARE_MD_TARGET_RE.findall(content)))
            if leftover:
                wrong.append(
                    f"skills/{path.parent.name}/SKILL.md: carries bare markdown "
                    f"target(s) {leftover!r} — a bare filename resolves against "
                    f"the stub's own directory, where no peer technique file "
                    f"exists (D-02 closed at v8.17.5)"
                )
        if stub_swept == 0:
            wrong.append(
                "skill-stub bare-target sweep matched ZERO stubs — the sweep "
                "is vacuous, so its clean result proves nothing"
            )
        if wrong:
            failures.append(f"FAIL (g): GATE-02 rewrite assertion: {wrong!r}")
        else:
            print(
                f"(g) GATE-02 rewrite assertion: PASS — the rewritten "
                f"pointer appears exactly once in the agent body "
                f"(plugin-root-anchored, with zero file-relative fallbacks) "
                f"and once in the skill stub (file-relative), and the agent "
                f"reference sibling is anchored too (DEC-A overturned at "
                f"v8.17.4), for all {len(SLUGS_WITH_DETAIL)} slugs; "
                f"directory-wide sweep found zero bare markdown targets "
                f"across {swept} emitted agent reference files and "
                f"{stub_swept} skill stubs"
            )
    except Exception as exc:
        failures.append(f"FAIL (g): unexpected exception: {exc!r}")

    # (h) GATE-02 dispatch control (Phase 152 WR-01 lesson): prove main()
    # itself reaches this block when --self-test is passed, not just that
    # this function is correct when called directly. The re-entrancy
    # sentinel prevents the nested main(["--self-test"]) call from recursing
    # into its own dispatch control; it is restored in a finally clause so an
    # exception cannot leave it set.
    _this_module = sys.modules[__name__]
    if not _this_module._GATE02_DISPATCH_REENTRANT:
        _this_module._GATE02_DISPATCH_REENTRANT = True
        try:
            try:
                dispatch_out, dispatch_err = io.StringIO(), io.StringIO()
                with contextlib.redirect_stdout(dispatch_out), contextlib.redirect_stderr(
                    dispatch_err
                ):
                    dispatch_rc = main(["--self-test"])
                dispatch_text = dispatch_out.getvalue()
                if dispatch_rc != 0:
                    failures.append(
                        f"FAIL (h): main(['--self-test']) returned {dispatch_rc}, "
                        f"expected 0"
                    )
                elif "GATE-02 pointer positive control: PASS" not in dispatch_text:
                    failures.append(
                        f"FAIL (h): main(['--self-test'])'s captured stdout did "
                        f"not contain the GATE-02 positive-control PASS text: "
                        f"{dispatch_text!r}"
                    )
                else:
                    print(
                        "(h) GATE-02 dispatch control: PASS — "
                        "main(['--self-test']) reaches this block end-to-end"
                    )
            except Exception as exc:
                failures.append(f"FAIL (h): unexpected exception: {exc!r}")
        finally:
            _this_module._GATE02_DISPATCH_REENTRANT = False

    # (i) FOCUSED_VALIDATION missing-token control (03-02-PLAN.md, PAR-02):
    # an in-memory stub body carrying {{PROCEDURE:<slug>}} but no
    # {{FOCUSED_VALIDATION}} token must raise, and the message must name the
    # missing token — proving PAR-02 is enforced at generation time, not
    # only by a downstream gate.
    try:
        fixture_body = "{{PROCEDURE:five-whys}}\n\n---\n"
        try:
            _expand_focused_validation_token(fixture_body, "five-whys")
            failures.append("FAIL (i): missing-token control did NOT raise")
        except ValueError as exc:
            if "FOCUSED_VALIDATION" in str(exc) and "missing" in str(exc).lower():
                print(
                    "(i) FOCUSED_VALIDATION missing-token control: PASS — "
                    "a stub body lacking the token raises, citing the "
                    "missing token"
                )
            else:
                failures.append(
                    f"FAIL (i): raised for the wrong reason: {exc}"
                )
        except Exception as exc:
            failures.append(f"FAIL (i): unexpected exception type: {exc!r}")
    except Exception as exc:
        failures.append(f"FAIL (i): unexpected exception: {exc!r}")

    # (j) FOCUSED_VALIDATION launcher control: an in-memory launcher body
    # carrying {{FOCUSED_VALIDATION}} must raise, citing LAUNCHER_SKILLS or
    # the launcher slug — a launcher dispatches the composer agent, which
    # already runs Phase 5, so it must never carry the token.
    try:
        try:
            _expand_focused_validation_token(
                "{{FOCUSED_VALIDATION}}", "first-principles-analysis"
            )
            failures.append("FAIL (j): launcher control did NOT raise")
        except ValueError as exc:
            if "LAUNCHER_SKILLS" in str(exc) or "first-principles-analysis" in str(exc):
                print(
                    "(j) FOCUSED_VALIDATION launcher control: PASS — a "
                    "launcher body carrying the token raises, citing "
                    "LAUNCHER_SKILLS"
                )
            else:
                failures.append(
                    f"FAIL (j): raised for the wrong reason: {exc}"
                )
        except Exception as exc:
            failures.append(f"FAIL (j): unexpected exception type: {exc!r}")
    except Exception as exc:
        failures.append(f"FAIL (j): unexpected exception: {exc!r}")

    # (k) FOCUSED_VALIDATION bare-link control: a snippet fixture carrying a
    # bare `.md` link target must raise from the bare-link guard, with a
    # message naming the offending target. Drives the real function against
    # a fixture file by temporarily pointing the module-level
    # FOCUSED_VALIDATION_SOURCE constant at a tempdir fixture, restoring in a
    # `finally` clause (the (b) idiom) — never mutates a real file.
    try:
        with tempfile.TemporaryDirectory() as d:
            fixture_path = Path(d) / "focused-validation-step.md"
            fixture_path.write_text(
                "## Focused-mode validation\n\n"
                "See [details](bad-target.md) for more.\n",
                encoding="utf-8",
            )
            original_source = _this_module.FOCUSED_VALIDATION_SOURCE
            try:
                _this_module.FOCUSED_VALIDATION_SOURCE = fixture_path
                try:
                    _expand_focused_validation_token(
                        "{{FOCUSED_VALIDATION}}", "five-whys"
                    )
                    failures.append(
                        "FAIL (k): bare-link control did NOT raise"
                    )
                except ValueError as exc:
                    if "bad-target.md" in str(exc):
                        print(
                            "(k) FOCUSED_VALIDATION bare-link control: "
                            "PASS — a snippet fixture with a bare .md link "
                            "raises, naming the offending target"
                        )
                    else:
                        failures.append(
                            f"FAIL (k): raised for the wrong reason: {exc}"
                        )
                except Exception as exc:
                    failures.append(
                        f"FAIL (k): unexpected exception type: {exc!r}"
                    )
            finally:
                _this_module.FOCUSED_VALIDATION_SOURCE = original_source
    except Exception as exc:
        failures.append(f"FAIL (k): unexpected exception: {exc!r}")

    if failures:
        for msg in failures:
            sys.stderr.write(msg + "\n")
        return 1

    print("sync-content.py --self-test: ALL PASS")
    return 0


def main(argv: list[str] | None = None) -> int:
    """Run the sync-content CLI and return a process exit code.

    `argv` defaults to None, which makes argparse fall back to `sys.argv[1:]`
    exactly as before this parameter existed — the CLI's live behaviour is
    byte-identical. The parameter exists so a self-test can drive `main()`
    itself end-to-end against a fixture argv, proving the `if args.check` /
    `if args.self_test` / else dispatch is actually wired — not just the
    `cmd_check()` / `cmd_self_test()` / `cmd_write()` functions it calls
    (mirrors `check-links.py`'s `main(argv=...)` precedent, Phase 152 WR-01).
    """
    _require_python_version()
    _require_pyyaml()
    p = argparse.ArgumentParser(
        prog="sync-content.py",
        description="Sync shared/ -> monolith + plugin surfaces.",
    )
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true", help="Compare; exit 1 on drift.")
    g.add_argument("--write", action="store_true", help="Regenerate all targets.")
    g.add_argument(
        "--self-test",
        action="store_true",
        help="Prove DEBT-01 orphan-guard and DEBT-02 count-drift guard are non-vacuous.",
    )
    args = p.parse_args(argv)
    if args.check:
        return cmd_check()
    if args.self_test:
        return cmd_self_test()
    return cmd_write()


if __name__ == "__main__":
    sys.exit(main())
