#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""DEPRECATED shim: check-sub-skill-routing.py.

This file is a thin delegating shim that translates the old per-signal
CLI surface (--p-threshold / --n-threshold) onto the merged battery's
namespaced flags (--boundary-p-threshold / --boundary-n-threshold) and
forwards to `scripts/check-routing-battery.py`.

Old CLI preserved for backwards compatibility (D-01, D-07):
    --p-threshold N  → --boundary-p-threshold N  (default: 2)
    --n-threshold N  → --boundary-n-threshold N  (default: 2)
    --self-test      → _bat.self_test()
    all other flags passed through unchanged

Use `scripts/check-routing-battery.py` directly for new invocations.
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Load the merged battery module via importlib (hyphenated filename is not a
# valid Python identifier, so `import check-routing-battery` is a syntax error).
# ---------------------------------------------------------------------------
_SCRIPTS_DIR = str(Path(__file__).resolve().parent)
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

_bat_path = str(Path(__file__).resolve().parent / "check-routing-battery.py")
_spec = importlib.util.spec_from_file_location("check_routing_battery", _bat_path)
if _spec is None or _spec.loader is None:
    print(
        f"error: could not load check-routing-battery.py from {_bat_path}",
        file=sys.stderr,
    )
    sys.exit(2)
_bat = importlib.util.module_from_spec(_spec)
sys.modules["check_routing_battery"] = _bat
_spec.loader.exec_module(_bat)  # type: ignore[union-attr]


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

REPO_ROOT: Path = Path(__file__).resolve().parents[1]
DEFAULT_PLUGIN_DIR: Path = REPO_ROOT / "first-principles"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="check-sub-skill-routing.py",
        description=(
            "DEPRECATED: thin shim delegating to scripts/check-routing-battery.py. "
            "Sub-skill routing boundary battery — classifies stream-json logs into "
            "{pre-mortem, inversion, both, none-or-other}."
        ),
    )
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--catalog",
        type=Path,
        help="Path to a Markdown sub-skill routing catalog.",
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
            "(default: /tmp/check-sub-skill-routing-<UTC-timestamp>/)."
        ),
    )
    p.add_argument(
        "--p-threshold",
        type=int,
        default=2,
        help=(
            "Min P-cases matching expected sub-skill for battery PASS "
            "(default: 2 — all P rows must pass; strict per v4.2 fixture correction). "
            "Forwarded as --boundary-p-threshold to scripts/check-routing-battery.py."
        ),
    )
    p.add_argument(
        "--n-threshold",
        type=int,
        default=2,
        help=(
            "Min N-cases classified none-or-other for battery PASS (default: 2). "
            "Forwarded as --boundary-n-threshold to scripts/check-routing-battery.py."
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
        help="Parse the catalog and print counts; do not invoke claude.",
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
    print(
        "DEPRECATED: check-sub-skill-routing.py is a thin shim; "
        "use scripts/check-routing-battery.py",
        file=sys.stderr,
    )

    parser = build_parser()
    args = parser.parse_args(argv)

    if args.self_test:
        return _bat.self_test()

    # Translate old flags to the merged battery's namespaced flags (D-04 mapping)
    forwarded: list[str] = [
        "--catalog", str(args.catalog),
        "--boundary-p-threshold", str(args.p_threshold),
        "--boundary-n-threshold", str(args.n_threshold),
    ]
    if args.plugin_dir is not None:
        forwarded += ["--plugin-dir", str(args.plugin_dir)]
    if args.out is not None:
        forwarded += ["--out", str(args.out)]
    if args.quiet:
        forwarded.append("--quiet")
    if args.dry_run:
        forwarded.append("--dry-run")
    forwarded += ["--repeat", str(args.repeat)]
    forwarded += ["--min-pass", str(args.min_pass)]

    return _bat.main(forwarded)


if __name__ == "__main__":
    sys.exit(main())
