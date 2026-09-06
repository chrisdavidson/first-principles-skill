#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# ///
"""CONF-SURFACE: generate the CI-gate claim surface from --describe emissions.

Hand-transcribed gate documentation produced 41% of all review findings
across Phases 13-15 — every branch count, surface list and disclosed bound
was copied by hand into up to five places with nothing checking they
agreed. This script is the fix's compute layer (D-21-B): it subprocess-
invokes every script-backed `scripts/_gate_registry.py` entry's `--describe`
leg, applies the registry's own D-01/D-04 floors plus a frozen-path
disjointness floor over its own write set, and exposes the region-
replacement primitive `docs/gates/<GATE-ID>.md` pages and the two hand-
written table regions will be regenerated through. The render layer that
turns harvested facts into `CLAUDE.md`/`docs/ARCHITECTURE.md`/`docs/gates/`
text is a later plan's job (`generate_all()` is a stub here, returning no
targets) — this plan proves the harvest, the floors and the region-rewrite
primitive work before any rendered text exists to drift against.

This module does not import any of the scripts it describes as gates (D-21-A
— it shells out to their `--describe` leg exactly as
`scripts/check-firewall-battery.sh` already does), and it perturbs none of
the three CONTRACT-06 sha256 pins (`_chain_block_well_formed`,
`_conclusion_claims`, `_slice_sections`) — it neither imports nor edits the
file that carries them.

Usage:
    python3 scripts/gen-gate-docs.py --write
    python3 scripts/gen-gate-docs.py --check
    python3 scripts/gen-gate-docs.py --self-test
    python3 scripts/gen-gate-docs.py --describe

Exit codes:
    0  write succeeded / check found no drift / self-test PASS
    1  check found drift, or a harvest/floor problem, or self-test FAIL
    2  check found a non-deterministic generate_all() (pass-1 != pass-2)
"""

from __future__ import annotations

import argparse
import difflib
import fnmatch
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import NamedTuple

REPO_ROOT: Path = Path(__file__).resolve().parents[1]
BATTERY_PATH: Path = REPO_ROOT / "scripts" / "check-firewall-battery.sh"

# ---------------------------------------------------------------------------
# Load _gate_registry.py via importlib (same MUST-pre-register-in-sys.modules
# discipline as scripts/check-step0-live.py's _battery_core load — Python
# 3.13+ @dataclass(frozen=True) compatibility, "Pitfall 3").
# ---------------------------------------------------------------------------

_REGISTRY_PATH: Path = Path(__file__).resolve().parent / "_gate_registry.py"
_registry_spec = importlib.util.spec_from_file_location("_gate_registry", _REGISTRY_PATH)
_gate_registry = importlib.util.module_from_spec(_registry_spec)  # type: ignore[arg-type]
sys.modules["_gate_registry"] = _gate_registry  # MUST precede exec_module
_registry_spec.loader.exec_module(_gate_registry)  # type: ignore[union-attr]

# `_this_module` is used by self-test controls that need to monkeypatch a
# module-level function (`generate_all`) and restore it afterwards — the
# exact idiom `scripts/sync-content.py`'s own `--self-test` control (l) uses
# for `GENERATED_TARGET_COUNT`.
_this_module = sys.modules[__name__]


# ---------------------------------------------------------------------------
# Stamping vocabulary (adapts scripts/sync-content.py:174-175's existing
# phrasing rather than inventing a second one).
# ---------------------------------------------------------------------------

GENERATED_MARKER = (
    "<!-- GENERATED — DO NOT EDIT. Source: {source}. "
    "Regenerate via: scripts/gen-gate-docs.py --write. -->"
)
GENERATED_END_MARKER = "<!-- END GENERATED -->"


# ---------------------------------------------------------------------------
# harvest(): subprocess-invoke every script-backed entry's --describe leg
# ---------------------------------------------------------------------------


class _HarvestEntry(NamedTuple):
    """The minimal shape harvest() needs from a registry entry — a `script`
    relpath (or, for self-test fixtures, an absolute temp-file path;
    `REPO_ROOT / script` returns `script` unchanged when it is already
    absolute, so both forms work through the same join). Duck-typed rather
    than `_gate_registry.GateEntry` itself so self-test fixtures do not have
    to construct every one of that frozen dataclass's unrelated fields."""

    script: str


def harvest(entries) -> tuple[dict[str, dict], list[str]]:
    """Subprocess-invoke `--describe` for every distinct script-backed entry.

    Returns `(by_script_relpath, problems)`. Never raises on a script that
    crashes, cannot be invoked, or emits malformed JSON (T-21-06-03): the
    script is named in `problems` and harvesting continues to the next one.
    `entries` may be `_gate_registry.GateEntry` instances or any object
    exposing a `.script` attribute (see `_HarvestEntry`); entries with a
    `None`/falsy `script` are skipped (nothing to invoke).
    """
    by_script: dict[str, dict] = {}
    problems: list[str] = []
    scripts = sorted({e.script for e in entries if e.script})
    for script in scripts:
        script_path = REPO_ROOT / script
        try:
            proc = subprocess.run(
                [sys.executable, str(script_path), "--describe"],
                capture_output=True,
                text=True,
                timeout=120,
            )
        except OSError as exc:
            problems.append(f"harvest: {script} could not be invoked: {exc!r}")
            continue
        if proc.returncode != 0:
            first_stderr_line = next(iter(proc.stderr.splitlines()), "")
            problems.append(
                f"harvest: {script} --describe exited {proc.returncode}: "
                f"{first_stderr_line}"
            )
            continue
        try:
            blob = json.loads(proc.stdout)
        except json.JSONDecodeError as exc:
            problems.append(
                f"harvest: {script} --describe emitted malformed JSON: {exc}"
            )
            continue
        by_script[script] = blob
    return by_script, problems


def _expected_harvest_scripts() -> frozenset[str]:
    """Script relpaths harvest() is expected to reach on a live run: every
    script-backed `ENTRIES` member, excluding the anticipatory ones
    (`CONF-SURFACE`, D-21-C) that are not wired into the battery yet —
    mirrors `_gate_registry._registry_entry_ids()`'s own exclusion so this
    vacuity floor and the D-01 id floor agree about what "documented"
    means."""
    return frozenset(
        e.script
        for e in _gate_registry.ENTRIES
        if e.script and e.key not in _gate_registry._ANTICIPATORY_KEYS
    )


# ---------------------------------------------------------------------------
# Frozen-path disjointness floor (T-21-06-02 / 19-D-08)
#
# `_FROZEN_PATHS_ARRAY_RE` / `_FROZEN_PATHS_ENTRY_RE` copy the identical
# grammar `scripts/check-quality-harness.py`'s `read_frozen_pathspecs` /
# `_frozen_spec_matches` already use over the same file — copied text, not a
# code dependency, the same boundary `_gate_registry.py`'s own
# `_BATTERY_GATE_RE` documents for its analogous D-01 extraction.
# ---------------------------------------------------------------------------

_FROZEN_PATHS_ARRAY_RE = re.compile(r"^_FROZEN_PATHS=\(\n(.*?)^\)$", re.MULTILINE | re.DOTALL)
_FROZEN_PATHS_ENTRY_RE = re.compile(r"^[ \t]*'([^']+)'[ \t]*$", re.MULTILINE)


def frozen_pathspecs(battery_text: str) -> tuple[str, ...]:
    """Pure regex extraction of `_FROZEN_PATHS` from the battery script's own
    source text — derived, never re-typed a second time (19-D-08). Returns
    `()` when the array cannot be located (a self-test fixture may
    deliberately pass array-free text); the live control asserts the real
    array parses to a non-empty tuple."""
    match = _FROZEN_PATHS_ARRAY_RE.search(battery_text)
    if match is None:
        return ()
    return tuple(_FROZEN_PATHS_ENTRY_RE.findall(match.group(1)))


def _frozen_pathspec_matches(rel_posix: str, spec: str) -> bool:
    """Mirrors git's default pathspec matching (fnmatch without
    FNM_PATHNAME, plus directory-prefix coverage) — the same semantics
    `check-quality-harness.py`'s `_frozen_spec_matches` documents for the
    battery's own `git diff`/`git status` legs."""
    return fnmatch.fnmatchcase(rel_posix, spec) or fnmatch.fnmatchcase(
        rel_posix, f"{spec}/*"
    )


def frozen_path_write_problems(write_paths, pathspecs) -> list[str]:
    """T-21-06-02: every path `generate_all()` would write must lie outside
    every `_FROZEN_PATHS` entry. A write inside a frozen path turns
    FROZEN-EVIDENCE red and blocks every commit in the repo (19-D-08)."""
    problems: list[str] = []
    for path in write_paths:
        try:
            rel = path.relative_to(REPO_ROOT).as_posix()
        except ValueError:
            rel = Path(path).as_posix()
        for spec in pathspecs:
            if _frozen_pathspec_matches(rel, spec):
                problems.append(
                    f"frozen-path-write: write target {rel!r} lies inside "
                    f"frozen pathspec {spec!r} (19-D-08)"
                )
                break
    return problems


# ---------------------------------------------------------------------------
# All floors, run together (D-01, D-04, vocabulary, frozen-path) — never
# short-circuited, so no floor can mask another (T-21-06-05's own lesson
# applied to the floor-runner itself).
# ---------------------------------------------------------------------------


def all_floor_problems(
    registry_ids: frozenset[str],
    battery_ids: frozenset[str],
    precommit_ids: frozenset[str],
    requested: dict[str, frozenset[str]],
    emitted: dict[str, frozenset[str]],
    write_paths,
    frozen_specs,
) -> list[str]:
    problems: list[str] = []
    problems += _gate_registry.registry_id_problems(registry_ids, battery_ids, precommit_ids)
    problems += _gate_registry.field_resolution_problems(requested, emitted)
    problems += _gate_registry.vocabulary_problems(emitted)
    problems += frozen_path_write_problems(write_paths, frozen_specs)
    return problems


# ---------------------------------------------------------------------------
# generate_all() — the single compute+render entry point (D-21-B interface).
# Render is a STUB in this plan (returns no targets); plan 21-07 implements
# it. Called ONCE per --write, TWICE per --check (idempotency), following
# report-conformance.py:2636-2646's "cannot disagree with each other"
# discipline.
# ---------------------------------------------------------------------------


def generate_all() -> dict[Path, str]:
    # STUB (plan 21-07 implements the render layer). Returning {} means
    # --write writes nothing and --check has no target to drift against —
    # both are proved by --self-test against synthetic fixtures in THIS
    # plan; the harvest+floor machinery above is exercised for real.
    return {}


# ---------------------------------------------------------------------------
# _replace_region: the region-replacement primitive (Task 2)
# ---------------------------------------------------------------------------


class RegionMarkerError(ValueError):
    """Raised by `_replace_region` on any malformed-marker shape (T-21-06-01):
    a marker occurring zero times, two-or-more times, or an end marker
    positioned before the start marker. Named, never a silent skip — the
    failure mode here is silent corruption of a project-instruction file."""


# A CommonMark fenced-code-block delimiter: up to three leading spaces, then
# three-or-more backticks or tildes, then the info string. Copied (not
# imported) from `scripts/check-quality-harness.py`'s `_FENCE_DELIM_RE` —
# that file's `_slice_sections` is CONTRACT-06 pinned and must not be
# imported or edited by this module.
_FENCE_DELIM_RE = re.compile(r"^ {0,3}(?P<fence>`{3,}|~{3,})(?P<info>.*)$")


def _fenced_line_flags(bare_lines: list[str]) -> list[bool]:
    """Per (already-terminator-stripped) line: is it inside — or itself — a
    CommonMark-fenced code block?

    Reimplements (does not import) `check-quality-harness.py`'s
    `_fenced_code_flags` closing-rule discipline: a fence closes only on the
    SAME delimiter character, at least as long as the opener, and carrying
    no info string of its own on the closer; a backtick opener may not have
    a backtick in its own info string. An unterminated fence runs to end of
    input. A naive parity toggle gets this wrong on a legal `~~~` block
    quoting an unclosed ``` example — this repo already shipped that exact
    bug once in `_slice_sections`; this function does not reinvent it.
    """
    inside = [False] * len(bare_lines)
    open_char: str | None = None
    open_len = 0
    for i, bare in enumerate(bare_lines):
        m = _FENCE_DELIM_RE.match(bare)
        if open_char is None:
            if m is not None:
                char = m.group("fence")[0]
                if not (char == "`" and "`" in m.group("info")):
                    open_char, open_len = char, len(m.group("fence"))
                    inside[i] = True
            continue
        inside[i] = True
        if (
            m is not None
            and m.group("fence")[0] == open_char
            and len(m.group("fence")) >= open_len
            and not m.group("info").strip()
        ):
            open_char, open_len = None, 0
    return inside


def _replace_region(
    text: str, start_marker: str, end_marker: str, new_content: str
) -> str:
    """Replace exactly the span from `start_marker`'s line through
    `end_marker`'s line, inclusive, leaving every other byte identical.

    Marker matching is on the WHOLE LINE (the marker string must equal a
    line's content, its own line terminator stripped) and ignores matches
    inside a CommonMark-fenced code block, so a marker string appearing in a
    fenced example (as `docs/gates/*.md` pages documenting this very
    mechanism will contain) is not treated as a real marker.

    Raises `RegionMarkerError`, naming the marker text and the observed
    count, when either marker's real (non-fenced) line-count is not exactly
    1, or when the end marker's line precedes the start marker's line —
    there is no best-effort branch and no silent skip.

    Every byte outside the replaced span — including the file's final
    newline (or lack of one) and any CRLF present — is preserved exactly.
    Inside the span, `new_content` is inserted between fresh copies of both
    markers using this repo's LF convention (CLAUDE.md's `newline='\\n'`
    mandate), except the end marker's own trailing terminator, which is
    reused from the original so a file with no final newline stays that
    way.
    """
    lines = text.splitlines(keepends=True)
    bare_lines = [ln.splitlines()[0] if ln.splitlines() else ln for ln in lines]
    fenced = _fenced_line_flags(bare_lines)

    def _find(marker: str) -> list[int]:
        return [
            i
            for i, (bare, is_fenced) in enumerate(zip(bare_lines, fenced))
            if not is_fenced and bare == marker
        ]

    start_idxs = _find(start_marker)
    if len(start_idxs) != 1:
        raise RegionMarkerError(
            f"start marker {start_marker!r}: found {len(start_idxs)} "
            "occurrence(s) outside fenced code blocks (expected exactly 1)"
        )
    end_idxs = _find(end_marker)
    if len(end_idxs) != 1:
        raise RegionMarkerError(
            f"end marker {end_marker!r}: found {len(end_idxs)} occurrence(s) "
            "outside fenced code blocks (expected exactly 1)"
        )
    start_idx, end_idx = start_idxs[0], end_idxs[0]
    if end_idx < start_idx:
        raise RegionMarkerError(
            f"end marker {end_marker!r} (line {end_idx}) precedes start "
            f"marker {start_marker!r} (line {start_idx})"
        )

    prefix = "".join(lines[:start_idx])
    suffix = "".join(lines[end_idx + 1 :])
    end_terminator = lines[end_idx][len(bare_lines[end_idx]) :]

    body = new_content
    if body and not body.endswith("\n"):
        body += "\n"
    span = f"{start_marker}\n{body}{end_marker}{end_terminator}"
    return prefix + span + suffix


# ---------------------------------------------------------------------------
# CLI: cmd_write / cmd_check / self_test / describe / main
# ---------------------------------------------------------------------------


def cmd_write() -> int:
    targets = generate_all()
    for path, content in targets.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
    print(f"wrote {len(targets)} file(s)")
    return 0


def cmd_check() -> int:
    """Idempotency self-check (sync-content.py's Pitfall-7 discipline), then
    the harvest + all four floors, then an on-disk drift diff.

    Exit 2 distinguishes a non-deterministic generator from a drifted tree
    (T-21-06-04) — a generator that disagrees with itself must never send a
    developer chasing a `--write` that can't converge.
    """
    pass1 = generate_all()
    pass2 = generate_all()
    if pass1 != pass2:
        sys.stderr.write("NON-DETERMINISTIC: pass-1 != pass-2\n")
        for k in pass1.keys() | pass2.keys():
            if pass1.get(k) != pass2.get(k):
                try:
                    rel = k.relative_to(REPO_ROOT)
                except ValueError:
                    rel = k
                sys.stderr.write(f"  differs: {rel}\n")
        return 2

    non_anticipatory = [
        e for e in _gate_registry.ENTRIES if e.key not in _gate_registry._ANTICIPATORY_KEYS
    ]
    by_script, harvest_problems = harvest(non_anticipatory)
    battery_text = BATTERY_PATH.read_text(encoding="utf-8")
    registry_ids = _gate_registry._registry_entry_ids()
    battery_ids = frozenset(_gate_registry.battery_gate_ids(battery_text))
    precommit_ids = _gate_registry._registry_precommit_ids()
    requested = _gate_registry._requested_fields_by_script()
    emitted_fields = {script: frozenset(blob.keys()) for script, blob in by_script.items()}
    specs = frozen_pathspecs(battery_text)

    problems: list[str] = list(harvest_problems)
    problems += all_floor_problems(
        registry_ids,
        battery_ids,
        precommit_ids,
        requested,
        emitted_fields,
        list(pass1.keys()),
        specs,
    )

    expected_scripts = _expected_harvest_scripts()
    print(f"harvested {len(by_script)}/{len(expected_scripts)} script-backed entries")
    missing_scripts = expected_scripts - set(by_script)
    if missing_scripts:
        problems.append(
            "cmd_check: harvested "
            f"{len(by_script)} of {len(expected_scripts)} expected script-backed "
            f"entries — missing: {sorted(missing_scripts)} (T-21-06-05)"
        )

    if problems:
        for p in problems:
            sys.stderr.write(p + "\n")
        return 1

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
        sys.stderr.write("Run: python3 scripts/gen-gate-docs.py --write && git add -u\n")
        return 1
    return 0


def describe() -> dict:
    """CONF-SURFACE's own self-description (D-21-C: "a generator that cannot
    describe itself would be the first exception to D-08's uniformity in
    the same phase that establishes it"). Pure — reads only this module's
    own constants."""
    return {
        "control_ids": sorted(_CONTROL_IDS),
        "control_count": len(_CONTROL_IDS),
        "locked_constants": {
            "generated_marker": GENERATED_MARKER,
            "generated_end_marker": GENERATED_END_MARKER,
        },
    }


# ---------------------------------------------------------------------------
# --self-test: _CONTROLS / _CONTROL_IDS / self_test() house style
# (scripts/report-conformance.py:5226-5361's shape)
# ---------------------------------------------------------------------------


def _control_harvest_nonzero_exit_named() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        bad = Path(tmp) / "bad_exit.py"
        bad.write_text("import sys\nsys.exit(1)\n", encoding="utf-8")
        by_script, problems = harvest([_HarvestEntry(script=str(bad))])
        assert by_script == {}, by_script
        assert len(problems) == 1, problems
        assert "bad_exit.py" in problems[0], problems


def _control_harvest_malformed_json_named() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        bad = Path(tmp) / "bad_json.py"
        bad.write_text("print('not json')\n", encoding="utf-8")
        by_script, problems = harvest([_HarvestEntry(script=str(bad))])
        assert by_script == {}, by_script
        assert len(problems) == 1, problems
        assert "bad_json.py" in problems[0], problems


def _control_harvest_one_bad_does_not_abort() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        good = Path(tmp) / "good_one.py"
        good.write_text(
            "import json\nprint(json.dumps({'control_count': 3}))\n",
            encoding="utf-8",
        )
        bad = Path(tmp) / "bad_one.py"
        bad.write_text("import sys\nsys.exit(1)\n", encoding="utf-8")
        by_script, problems = harvest(
            [_HarvestEntry(script=str(good)), _HarvestEntry(script=str(bad))]
        )
        assert len(problems) == 1, problems
        assert str(good) in by_script, by_script
        assert by_script[str(good)] == {"control_count": 3}, by_script


def _control_floors_run_together() -> None:
    registry_ids = frozenset({"REAL-ONE"})
    battery_ids = frozenset(
        _gate_registry.battery_gate_ids(
            'gate "REAL-ONE" "x" "true"\ngate "MISSING-ONE" "x" "true"\n'
        )
    )
    requested = {"scripts/x.py": frozenset({"branch_count"})}
    emitted: dict[str, frozenset[str]] = {"scripts/x.py": frozenset()}
    problems = all_floor_problems(
        registry_ids, battery_ids, frozenset(), requested, emitted, [], ()
    )
    assert len(problems) == 2, problems
    joined = " ".join(problems)
    assert "MISSING-ONE" in joined, problems
    assert "branch_count" in joined, problems


def _control_frozen_path_write_fires() -> None:
    write_target = REPO_ROOT / "tests" / "adversarial-corpus-v9.0" / "bogus.md"
    problems = frozen_path_write_problems(
        [write_target], ("tests/adversarial-corpus-v9.0",)
    )
    assert len(problems) == 1, problems
    assert "tests/adversarial-corpus-v9.0" in problems[0], problems


def _control_frozen_paths_derived_not_typed() -> None:
    battery_text = BATTERY_PATH.read_text(encoding="utf-8")
    derived = frozen_pathspecs(battery_text)
    match = _FROZEN_PATHS_ARRAY_RE.search(battery_text)
    assert match is not None, "could not locate _FROZEN_PATHS in the live battery script"
    body_lines = [ln.strip() for ln in match.group(1).splitlines() if ln.strip()]
    independent = tuple(
        ln[1:-1] for ln in body_lines if ln.startswith("'") and ln.endswith("'")
    )
    assert derived == independent, (derived, independent)
    assert len(derived) > 0, "frozen_pathspecs derived zero entries from the live battery script"


def _control_check_dispatch_wired() -> None:
    """Phase-152 WR-01 precedent: drive `main(["--check"])` itself
    in-process against the real tree, proving the CLI dispatch is wired —
    not just `cmd_check()` called directly."""
    rc = main(["--check"])
    assert rc == 0, f"main(['--check']) returned {rc}, expected 0 against the live tree"


def _control_nondeterminism_exit_2() -> None:
    original = _this_module.generate_all
    calls = {"n": 0}

    def _flaky() -> dict[Path, str]:
        calls["n"] += 1
        return {Path("/tmp/gen-gate-docs-fixture-target.md"): f"call-{calls['n']}"}

    try:
        _this_module.generate_all = _flaky
        rc = cmd_check()
        assert rc == 2, f"cmd_check() returned {rc}, expected 2 for a non-deterministic generator"
    finally:
        _this_module.generate_all = original


def _control_region_happy_path() -> None:
    text = "before\nSTART\nold body\nEND\nafter\n"
    result = _replace_region(text, "START", "END", "new body\n")
    assert result == "before\nSTART\nnew body\nEND\nafter\n", result


def _control_region_zero_start_raises() -> None:
    text = "before\nEND\nafter\n"
    try:
        _replace_region(text, "START", "END", "x\n")
        raise AssertionError("expected RegionMarkerError")
    except RegionMarkerError as exc:
        assert "START" in str(exc) and " 0 " in str(exc), str(exc)


def _control_region_zero_end_raises() -> None:
    text = "before\nSTART\nafter\n"
    try:
        _replace_region(text, "START", "END", "x\n")
        raise AssertionError("expected RegionMarkerError")
    except RegionMarkerError as exc:
        assert "END" in str(exc) and " 0 " in str(exc), str(exc)


def _control_region_duplicate_start_raises() -> None:
    text = "START\nmid\nSTART\nEND\n"
    try:
        _replace_region(text, "START", "END", "x\n")
        raise AssertionError("expected RegionMarkerError")
    except RegionMarkerError as exc:
        assert " 2 " in str(exc), str(exc)


def _control_region_duplicate_end_raises() -> None:
    text = "START\nEND\nmid\nEND\n"
    try:
        _replace_region(text, "START", "END", "x\n")
        raise AssertionError("expected RegionMarkerError")
    except RegionMarkerError as exc:
        assert " 2 " in str(exc), str(exc)


def _control_region_end_before_start_raises() -> None:
    text = "END\nmid\nSTART\n"
    try:
        _replace_region(text, "START", "END", "x\n")
        raise AssertionError("expected RegionMarkerError")
    except RegionMarkerError as exc:
        assert "precedes" in str(exc), str(exc)


def _control_region_marker_in_fence_ignored() -> None:
    # Two invariants must BOTH hold, or this control cannot discriminate
    # which one broke: whole-line anchoring (line 0 CONTAINS "START" as a
    # substring but does not EQUAL it — a substring search would wrongly
    # count it) and fence exclusion (the fenced "START" line equals the
    # marker exactly but must not count either). Only the real, non-fenced,
    # exact-match "START" line may be the start marker.
    text = (
        "See the START region below for an example.\n"
        "```\n"
        "START\n"
        "```\n"
        "START\n"
        "old\n"
        "END\n"
        "after\n"
    )
    result = _replace_region(text, "START", "END", "new\n")
    assert result.startswith(
        "See the START region below for an example.\n```\nSTART\n```\n"
    ), result
    assert result.endswith("START\nnew\nEND\nafter\n"), result


def _control_region_tilde_fence_quoting_backticks() -> None:
    # ~~~ ... ~~~ quotes an UNCLOSED ``` fence inside it. A parity toggle
    # inverts on the unclosed ``` and treats the real START (outside both
    # fences) as still "inside a fence" — CommonMark closing rules do not.
    text = "~~~\n```\nSTART\n```\n~~~\nSTART\nold\nEND\n"
    result = _replace_region(text, "START", "END", "new\n")
    assert result.startswith("~~~\n```\nSTART\n```\n~~~\n"), result
    assert result.endswith("START\nnew\nEND\n"), result


def _control_region_preserves_final_newline() -> None:
    text = "before\nSTART\nold\nEND"  # no trailing newline
    result = _replace_region(text, "START", "END", "new\n")
    assert result == "before\nSTART\nnew\nEND", result


def _control_region_preserves_crlf() -> None:
    text = "before\r\nSTART\r\nold\r\nEND\r\nafter\r\n"
    result = _replace_region(text, "START", "END", "new\n")
    assert result.startswith("before\r\nSTART\n"), result
    assert result.endswith("END\r\nafter\r\n"), result


def _control_real_file_claude_md_region() -> None:
    """A real-file control (Task 2): wrap the live CLAUDE.md's own
    "### CI gates" subsection with synthetic markers in memory only, call
    `_replace_region`, and assert everything before the heading and
    everything after the subsection is byte-identical to the untouched
    file. Nothing is written to disk."""
    text = (REPO_ROOT / "CLAUDE.md").read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    bare = [ln.splitlines()[0] if ln.splitlines() else ln for ln in lines]
    heading_idx = next(i for i, b in enumerate(bare) if b.strip() == "### CI gates")
    end_idx = next(
        i
        for i in range(heading_idx + 1, len(bare))
        if bare[i].startswith("## ") or bare[i].startswith("### ")
    )
    start_marker = "<!-- TEST-REGION-START -->"
    end_marker = "<!-- TEST-REGION-END -->"
    synthetic_lines = (
        lines[:heading_idx]
        + [start_marker + "\n"]
        + lines[heading_idx:end_idx]
        + [end_marker + "\n"]
        + lines[end_idx:]
    )
    synthetic_text = "".join(synthetic_lines)
    result = _replace_region(synthetic_text, start_marker, end_marker, "NEW CONTENT\n")
    prefix_original = "".join(lines[:heading_idx])
    suffix_original = "".join(lines[end_idx:])
    assert result.startswith(prefix_original), "prefix diverged from live CLAUDE.md bytes"
    assert result.endswith(suffix_original), "suffix diverged from live CLAUDE.md bytes"


def _control_describe_emits_parseable_json() -> None:
    blob = describe()
    encoded = json.dumps(blob, indent=2, sort_keys=True)
    decoded = json.loads(encoded)
    assert decoded == blob, "describe() output did not round-trip through JSON"


_CONTROLS: tuple[tuple[str, object], ...] = (
    ("harvest-nonzero-exit-named", _control_harvest_nonzero_exit_named),
    ("harvest-malformed-json-named", _control_harvest_malformed_json_named),
    ("harvest-one-bad-does-not-abort", _control_harvest_one_bad_does_not_abort),
    ("floors-run-together", _control_floors_run_together),
    ("frozen-path-write-fires", _control_frozen_path_write_fires),
    ("frozen-paths-derived-not-typed", _control_frozen_paths_derived_not_typed),
    ("check-dispatch-wired", _control_check_dispatch_wired),
    ("nondeterminism-exit-2", _control_nondeterminism_exit_2),
    ("region-happy-path", _control_region_happy_path),
    ("region-zero-start-raises", _control_region_zero_start_raises),
    ("region-zero-end-raises", _control_region_zero_end_raises),
    ("region-duplicate-start-raises", _control_region_duplicate_start_raises),
    ("region-duplicate-end-raises", _control_region_duplicate_end_raises),
    ("region-end-before-start-raises", _control_region_end_before_start_raises),
    ("region-marker-in-fence-ignored", _control_region_marker_in_fence_ignored),
    (
        "region-tilde-fence-quoting-backticks",
        _control_region_tilde_fence_quoting_backticks,
    ),
    ("region-preserves-final-newline", _control_region_preserves_final_newline),
    ("region-preserves-crlf", _control_region_preserves_crlf),
    ("region-real-file-claude-md", _control_real_file_claude_md_region),
    ("describe-emits-parseable-json", _control_describe_emits_parseable_json),
)

# Second, independently-typed transcription of every control id above (the
# SCAN-GUARD/CONF-GATE coverage-floor shape, D-21-K note: this discipline
# applies to self-test control-id coverage only, not to the battery gate-id
# set, which stays derived). A control added to _CONTROLS but missing here,
# or vice versa, fails self_test() by name rather than silently narrowing
# coverage.
_CONTROL_IDS: tuple[str, ...] = (
    "harvest-nonzero-exit-named",
    "harvest-malformed-json-named",
    "harvest-one-bad-does-not-abort",
    "floors-run-together",
    "frozen-path-write-fires",
    "frozen-paths-derived-not-typed",
    "check-dispatch-wired",
    "nondeterminism-exit-2",
    "region-happy-path",
    "region-zero-start-raises",
    "region-zero-end-raises",
    "region-duplicate-start-raises",
    "region-duplicate-end-raises",
    "region-end-before-start-raises",
    "region-marker-in-fence-ignored",
    "region-tilde-fence-quoting-backticks",
    "region-preserves-final-newline",
    "region-preserves-crlf",
    "region-real-file-claude-md",
    "describe-emits-parseable-json",
)


def self_test() -> int:
    executed: list[str] = []
    failures: list[tuple[str, str]] = []

    for control_id, control_fn in _CONTROLS:
        executed.append(control_id)
        try:
            control_fn()
        except AssertionError as exc:
            failures.append((control_id, str(exc)))
        except Exception as exc:  # noqa: BLE001 -- a control that crashes is a failure too
            failures.append((control_id, f"{type(exc).__name__}: {exc}"))

    registered = set(_CONTROL_IDS)
    ran = set(executed)
    missing = registered - ran
    extra = ran - registered
    if missing or extra:
        failures.append(
            (
                "coverage-floor",
                f"registered/executed control-id mismatch: missing={sorted(missing)} "
                f"extra={sorted(extra)}",
            )
        )

    if failures:
        for control_id, message in failures:
            sys.stderr.write(f"gen-gate-docs: SELF-TEST FAIL [{control_id}] — {message}\n")
        return 1
    print(f"gen-gate-docs: SELF-TEST PASS — {len(executed)} controls run")
    return 0


def main(argv: list[str] | None = None) -> int:
    """`argv` defaults to `None` so `--self-test` can drive `main()` itself
    end to end against a fixture argv, proving the CLI dispatch is wired,
    not just the `cmd_*` functions it calls (Phase-152 WR-01 precedent,
    `scripts/sync-content.py`'s own comment)."""
    p = argparse.ArgumentParser(
        prog="gen-gate-docs.py",
        description="Generate the CI-gate claim surface from --describe emissions.",
    )
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--write", action="store_true", help="Regenerate all targets.")
    g.add_argument(
        "--check",
        action="store_true",
        help="Compare; exit 1 on drift or a harvest/floor problem, exit 2 on non-determinism.",
    )
    g.add_argument("--self-test", action="store_true", help="Run the offline control battery.")
    g.add_argument(
        "--describe",
        action="store_true",
        help="Emit this gate's self-description as a flat JSON blob on stdout.",
    )
    args = p.parse_args(argv)
    if args.write:
        return cmd_write()
    if args.check:
        return cmd_check()
    if args.self_test:
        return self_test()
    print(json.dumps(describe(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
