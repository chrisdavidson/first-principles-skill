#!/usr/bin/env python3
"""Classify every tracked file under tests/ by its executable relationship to the repo.

Manual tool, not a CI gate — the same standing as `check-traceability.py emit`. It exists so
the `tests/README.md` classification can be re-derived rather than trusted, which is the
lesson of the 2026-08-16 audit: a stale inventory of what is load-bearing is worse than none,
because it reads as proof.

Three tiers, in the order they are checked:

  gate-pinned      opened at runtime by an offline gate's self-test, OR named as a matrix
                   `artifact_link` (which TRACE-03 deep-resolves, so the file must exist).
  live-unwired     executed by pytest, but not by any CI job.
  archive          no executable relationship. Tracked, referenced in prose, never read.

Measurement, not inference. Runtime reads are captured with `sys.addaudithook` over an
`open` event while each gate script runs in-process under `runpy`; nothing is concluded from
grepping for filenames. Two ways that inference has already gone wrong here:

  * `deliverable_path` looks like a pin and is not — only `artifact_link` is deep-resolved.
  * A loader passed as a function object (`..., _load_excerpt_v74, ...`) is invisible to a
    grep for `_load_excerpt_v74(`, which reports live capture directories as dead.

Usage:
    python3 scripts/trace-tests-usage.py              # summary + per-directory table
    python3 scripts/trace-tests-usage.py --list-archive
    python3 scripts/trace-tests-usage.py --tier gate-pinned

Exit status is 0 only when every gate command ran cleanly. A gate that fails contributes zero
paths and would silently push everything it reads into `archive`, so a partial trace exits 1 and
says so — an understated classification that looks complete is worse than no classification.
This tool reports; it does not gate.
"""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import runpy
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Every offline gate command that could plausibly read tests/, plus the report-only reporter.
# Read-only invocations only — `sync-content.py --write` is deliberately absent.
GATE_COMMANDS: tuple[tuple[str, ...], ...] = (
    ("scripts/sync-content.py", "--check"),
    ("scripts/sync-content.py", "--self-test"),
    ("scripts/check-step0-live.py", "--self-test"),
    ("scripts/check-step0-emulator.py", "--self-test"),
    ("scripts/check-links.py", "--self-test"),
    ("scripts/check-links.py",),
    ("scripts/check-trigger-collisions.py", "--self-test"),
    ("scripts/check-trigger-collisions.py",),
    ("scripts/check-description-budget.py",),
    ("scripts/check-version-stamps.py", "--self-test"),
    ("scripts/check-version-stamps.py",),
    ("scripts/check-agent.py", "--self-test"),
    ("scripts/check-agent.py", "--file", "first-principles/agents/first-principles.md"),
    ("scripts/check-routing-battery.py", "--self-test"),
    ("scripts/check-traceability.py", "--self-test"),
    ("scripts/check-install-collisions.py", "--self-test"),
    ("scripts/check-install-collisions.py",),
    ("scripts/check-quality-harness.py", "--self-test"),
    ("scripts/check-body-budget.py",),
)


# tests/README.md is this classification's own index, not evidence. Counting it would make the
# document report on itself and shift its own totals by one the moment it is committed.
SELF_EXCLUDE = frozenset({"tests/README.md"})


def tracked_test_files() -> list[str]:
    out = subprocess.run(
        ["git", "ls-files", "tests"],
        cwd=REPO_ROOT, capture_output=True, text=True, check=True,
    ).stdout
    return sorted(line for line in out.splitlines() if line and line not in SELF_EXCLUDE)


def trace_one(command: tuple[str, ...]) -> set[str]:
    """Run one gate command in-process and return the tests/ paths it opened."""
    seen: set[str] = set()
    prefix = str(REPO_ROOT) + os.sep

    def hook(event: str, args: tuple) -> None:
        if event != "open":
            return
        path = args[0]
        if isinstance(path, bytes):
            try:
                path = path.decode()
            except UnicodeDecodeError:
                return
        if not isinstance(path, str):
            return
        absolute = os.path.abspath(path)
        if absolute.startswith(prefix):
            relative = absolute[len(prefix):]
            if relative.startswith("tests/"):
                seen.add(relative)

    sys.addaudithook(hook)  # audit hooks cannot be removed; one process per run is fine
    saved_argv = sys.argv[:]
    saved_cwd = os.getcwd()
    try:
        os.chdir(REPO_ROOT)
        sys.argv = list(command)
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            try:
                runpy.run_path(str(REPO_ROOT / command[0]), run_name="__main__")
            except SystemExit:
                pass
    finally:
        sys.argv = saved_argv
        os.chdir(saved_cwd)
    return seen


def gate_opened_paths() -> tuple[set[str], list[str]]:
    """Fan the trace out over one subprocess per gate — audit hooks are process-global.

    Returns (paths, failures). A gate that errors contributes zero paths, which silently
    reclassifies everything it would have read as `archive` — the exact shape of the wrong
    answer this tool exists to prevent. So every non-zero exit is surfaced and made fatal
    rather than absorbed into a plausible-looking table.
    """
    opened: set[str] = set()
    failures: list[str] = []
    tracer = Path(__file__).resolve()
    for command in GATE_COMMANDS:
        result = subprocess.run(
            [sys.executable, str(tracer), "--trace-one", *command],
            cwd=REPO_ROOT, capture_output=True, text=True,
        )
        paths = [line for line in result.stdout.splitlines() if line.startswith("tests/")]
        opened.update(paths)
        if result.returncode != 0:
            detail = (result.stderr.strip().splitlines() or ["(no stderr)"])[-1]
            failures.append(
                f"{' '.join(command)} exited {result.returncode}, "
                f"contributed {len(paths)} paths — {detail}"
            )
    return opened, failures


def artifact_link_paths() -> set[str]:
    """tests/ paths named as `artifact_link` — the only matrix field TRACE-03 deep-resolves."""
    matrix = json.loads((REPO_ROOT / "docs" / "data" / "matrix.json").read_text())
    rows = matrix["rows"] if isinstance(matrix, dict) else matrix
    return {
        link for row in rows
        if (link := (row.get("artifact_link") or "").strip()).startswith("tests/")
    }


def pytest_collected_paths() -> set[str]:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "--collect-only", "-q"],
        cwd=REPO_ROOT, capture_output=True, text=True,
    )
    return {
        line.split("::", 1)[0]
        for line in result.stdout.splitlines()
        if line.startswith("tests/") and "::" in line
    }


def classify() -> tuple[dict[str, str], list[str]]:
    tracked = tracked_test_files()
    opened, failures = gate_opened_paths()
    pinned = opened | artifact_link_paths()
    collected = pytest_collected_paths()
    tiers: dict[str, str] = {}
    for path in tracked:
        if path in pinned:
            tiers[path] = "gate-pinned"
        elif path in collected:
            tiers[path] = "live-unwired"
        else:
            tiers[path] = "archive"
    return tiers, failures


def group_of(path: str) -> str:
    rest = path[len("tests/"):]
    return rest.split("/", 1)[0] if "/" in rest else "(top level)"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trace-one", nargs=argparse.REMAINDER,
                        help="internal: trace a single gate command and print its tests/ reads")
    parser.add_argument("--tier", choices=("gate-pinned", "live-unwired", "archive"),
                        help="print every path in one tier and exit")
    parser.add_argument("--list-archive", action="store_true",
                        help="shorthand for --tier archive")
    args = parser.parse_args()

    if args.trace_one:
        for path in sorted(trace_one(tuple(args.trace_one))):
            print(path)
        return 0

    tiers, failures = classify()
    for failure in failures:
        print(f"[warn] {failure}", file=sys.stderr)

    if args.tier or args.list_archive:
        wanted = args.tier or "archive"
        for path in sorted(p for p, t in tiers.items() if t == wanted):
            print(path)
        return 1 if failures else 0

    counts: dict[str, int] = {"gate-pinned": 0, "live-unwired": 0, "archive": 0}
    sizes: dict[str, int] = {"gate-pinned": 0, "live-unwired": 0, "archive": 0}
    per_group: dict[str, dict[str, int]] = {}
    for path, tier in tiers.items():
        counts[tier] += 1
        with contextlib.suppress(OSError):
            sizes[tier] += (REPO_ROOT / path).stat().st_size
        per_group.setdefault(group_of(path), {"gate-pinned": 0, "live-unwired": 0, "archive": 0})
        per_group[group_of(path)][tier] += 1

    total = len(tiers)
    print(f"tracked under tests/: {total} files\n")
    for tier in ("gate-pinned", "live-unwired", "archive"):
        share = (100 * counts[tier] / total) if total else 0
        print(f"  {tier:<13} {counts[tier]:>4} files  ({share:4.1f} %)  {sizes[tier] / 1_000_000:.2f} MB")

    print("\nper directory (gate-pinned / live-unwired / archive):")
    for group in sorted(per_group):
        row = per_group[group]
        print(f"  {group:<28} {row['gate-pinned']:>4} / {row['live-unwired']:>4} / {row['archive']:>4}")

    if failures:
        print(
            f"\nINCOMPLETE — {len(failures)} gate command(s) failed (listed above). Every file "
            "they would have read is counted as archive, so these numbers understate what is "
            "load-bearing. Do not quote them.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
