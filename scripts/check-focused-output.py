#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""DEPRECATED shim: check-focused-output.py.

This file is a thin delegating shim that translates the old per-signal
CLI surface (--p-threshold / --n-threshold) onto the merged battery's
namespaced flags (--focused-p-threshold / --focused-n-threshold) and
forwards to `scripts/check-routing-battery.py`.

Old CLI preserved for backwards compatibility (D-01, D-07):
    --p-threshold N  → --focused-p-threshold N  (default: 4)
    --n-threshold N  → --focused-n-threshold N  (default: 1)
    --self-test      → _bat.self_test()
    --dry-run        → reports focused signal's per-signal counts (4 P / 1 N)
                       using MERGED_CATALOG — does NOT forward to the battery
                       (the merged battery would report 6 P / 3 N totals)

For live runs, always forwards --catalog MERGED_CATALOG (the single source of
truth, D-02), not the old caller-supplied path — eliminating the divergent
expectation source (BATT-05).

Use `scripts/check-routing-battery.py` directly for new invocations.
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Load sibling modules via sys.path + importlib.
# (scripts/ has no __init__.py; import by name requires sys.path surgery.)
# ---------------------------------------------------------------------------
_SCRIPTS_DIR = str(Path(__file__).resolve().parent)
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

import _battery_core as _bc  # noqa: E402

_bat_path = str(Path(__file__).resolve().parent / "check-routing-battery.py")
_spec = importlib.util.spec_from_file_location("check_routing_battery", _bat_path)
if _spec is None or _spec.loader is None:
    print(
        f"error: could not load check-routing-battery.py from {_bat_path}",
        file=sys.stderr,
    )
    sys.exit(2)
_bat = importlib.util.module_from_spec(_spec)
sys.modules.setdefault("check_routing_battery", _bat)
_spec.loader.exec_module(_bat)  # type: ignore[union-attr]

# ---------------------------------------------------------------------------
# Module-level constant: single source of truth catalog (D-02).
# For --dry-run per-signal counts, parse this directly.
# For live runs, always forward this catalog to the merged battery.
# ---------------------------------------------------------------------------
MERGED_CATALOG: Path = Path(__file__).resolve().parents[1] / "tests" / "routing-battery-catalog.md"

REPO_ROOT: Path = Path(__file__).resolve().parents[1]
DEFAULT_PLUGIN_DIR: Path = REPO_ROOT / "first-principles"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="check-focused-output.py",
        description=(
            "DEPRECATED: thin shim delegating to scripts/check-routing-battery.py. "
            "Focused-output structure detector — classifies stream-json logs into "
            "{focused-<technique>, ambiguous, full-composer, none}."
        ),
    )
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--catalog",
        type=Path,
        help="Path to a Markdown output-structure catalog (ignored for live runs; "
             "MERGED_CATALOG is always used as the single source of truth).",
    )
    mode.add_argument(
        "--self-test",
        dest="self_test",
        action="store_true",
        help="Validate detection logic against in-script fixtures and exit.",
    )
    p.add_argument(
        "--plugin-dir",
        type=Path,
        default=DEFAULT_PLUGIN_DIR,
        help=(
            f"Plugin directory passed to `claude --plugin-dir` "
            f"(default: {DEFAULT_PLUGIN_DIR})."
        ),
    )
    p.add_argument(
        "--out",
        type=Path,
        default=None,
        help=(
            "Output directory for per-prompt .jsonl + scores.tsv + verdict.txt "
            "(default: /tmp/check-focused-output-<UTC-timestamp>/)."
        ),
    )
    p.add_argument(
        "--p-threshold",
        type=int,
        default=4,
        help=(
            "Min P-cases matching expected structure for battery PASS "
            "(default: 4 — all four P rows in the calibrated FU-21 catalog "
            "must pass). Forwarded as --focused-p-threshold to "
            "scripts/check-routing-battery.py."
        ),
    )
    p.add_argument(
        "--n-threshold",
        type=int,
        default=1,
        help=(
            "Min N-cases matching expected for battery PASS "
            "(default: 1 — the sole over-trigger negative control N1 must pass). "
            "Forwarded as --focused-n-threshold to scripts/check-routing-battery.py."
        ),
    )
    p.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress per-prompt progress lines (final verdict still printed).",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help=(
            "Parse the merged catalog's focused-signal rows and print counts; "
            "do not invoke claude. Reports the focused signal's own 4 P / 1 N "
            "counts (not the merged 6 P / 3 N totals)."
        ),
    )
    p.add_argument(
        "--repeat",
        type=int,
        default=5,
        metavar="N",
        help="Run each catalog prompt N times (default: 5).",
    )
    p.add_argument(
        "--min-pass",
        type=int,
        default=3,
        metavar="K",
        help="K-of-N runs must match expected for prompt to PASS (default: 3).",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.self_test:
        print(
            "DEPRECATED: check-focused-output.py is a thin shim; "
            "use scripts/check-routing-battery.py",
            file=sys.stderr,
        )
        return _bat.self_test()

    print(
        "DEPRECATED: check-focused-output.py is a thin shim; "
        "use scripts/check-routing-battery.py",
        file=sys.stderr,
    )

    if args.dry_run:
        # D-07 CRITICAL: report the focused signal's per-signal counts, NOT
        # the merged battery's 6 P / 3 N totals. Filter the merged catalog
        # to only rows with expected_output != "n-a" (the focused-signal rows).
        try:
            positives, negatives = _bc.parse_merged_catalog(MERGED_CATALOG)
        except (FileNotFoundError, ValueError) as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        fp = [p for p in positives if p.expected_output != "n-a"]
        fn = [n for n in negatives if n.expected_output != "n-a"]
        print(f"Catalog: {len(fp)} P-prompts, {len(fn)} N-prompts")
        return 0

    # Live run: translate old flags → merged battery's namespaced flags (D-04).
    # Always forward MERGED_CATALOG, never the caller-supplied --catalog path.
    forwarded: list[str] = [
        "--catalog", str(MERGED_CATALOG),
        "--focused-p-threshold", str(args.p_threshold),
        "--focused-n-threshold", str(args.n_threshold),
    ]
    if args.plugin_dir is not None:
        forwarded += ["--plugin-dir", str(args.plugin_dir)]
    if args.out is not None:
        forwarded += ["--out", str(args.out)]
    if args.quiet:
        forwarded.append("--quiet")
    forwarded += ["--repeat", str(args.repeat)]
    forwarded += ["--min-pass", str(args.min_pass)]

    return _bat.main(forwarded)


if __name__ == "__main__":
    sys.exit(main())
