#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml>=6.0"]
# ///
"""VAL-05 gate: check that rendered skill listing text fits within the 2000-char ceiling.

Usage:
    python3 scripts/check-description-budget.py

Exit codes:
    0  all skills within budget
    1  total listing text exceeds 2000 chars
    2  environment error (Python <3.12, PyYAML missing, malformed frontmatter)
"""

from __future__ import annotations

import sys
from pathlib import Path

# D-19-8 — default 1% listing budget on 200k-context model.
# CAP is in characters (Python str length). Today's descriptions are ASCII;
# char == byte. If non-ASCII enters, char count stays the right unit per D-19-8.
CAP = 2000


def _require_python_version() -> None:
    if sys.version_info < (3, 12):
        sys.stderr.write(
            f"scripts/check-description-budget.py requires Python >=3.12 "
            f"(running {sys.version_info.major}.{sys.version_info.minor}).\n"
        )
        sys.exit(2)


def _require_pyyaml() -> None:
    """Catch missing PyYAML at startup with a clear remediation message."""
    try:
        import yaml  # noqa: F401
    except ImportError:
        sys.stderr.write(
            "scripts/check-description-budget.py needs PyYAML.\n"
            "  Easiest:  uv run scripts/check-description-budget.py\n"
            "  Or:       pip install --user 'pyyaml>=6.0'  &&  "
            "python3 scripts/check-description-budget.py\n"
        )
        sys.exit(2)


def main() -> None:
    _require_python_version()
    _require_pyyaml()

    # Insert scripts/ directory into sys.path so _skill_io can be imported
    # without installation — mirrors Plan 19-02 Task 1 pattern.
    scripts_dir = Path(__file__).resolve().parent
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))

    try:
        from _skill_io import iter_plugin_skills
    except ImportError as exc:
        sys.stderr.write(f"check-description-budget: cannot import _skill_io: {exc}\n")
        sys.exit(2)

    # Collect per-skill surface lengths.
    # Surface = description + " " + when_to_use (if when_to_use present) — D-19-8.
    rows: list[tuple[str, int, int, int]] = []
    try:
        for slug, fm, _body in iter_plugin_skills():
            desc: str = fm.get("description", "") or ""
            wtu: str = fm.get("when_to_use", "") or ""
            surface = f"{desc} {wtu}" if wtu else desc
            rows.append((slug, len(desc), len(wtu), len(surface)))
    except (ValueError, FileNotFoundError) as exc:
        sys.stderr.write(f"check-description-budget: {exc}\n")
        sys.exit(2)

    # iter_plugin_skills already sorts by slug; rows are already deterministic.
    # Sort explicitly here in case caller wraps iter_plugin_skills differently.
    rows.sort(key=lambda r: r[0])

    total = sum(r[3] for r in rows)
    slack = CAP - total

    slug_width = max((len(r[0]) for r in rows), default=4)
    slug_width = max(slug_width, 4)

    header = f"  {'slug':<{slug_width}}  {'description':>11}  {'when_to_use':>11}  {'total':>7}"
    divider = f"  {'-' * slug_width}  {'-' * 11}  {'-' * 11}  {'-' * 7}"

    lines: list[str] = [
        "check-description-budget: per-skill totals",
        header,
        divider,
    ]
    for slug, desc_len, wtu_len, total_len in rows:
        lines.append(
            f"  {slug:<{slug_width}}  {desc_len:>11}  {wtu_len:>11}  {total_len:>7}"
        )
    lines.append(divider)
    lines.append(f"  {'TOTAL':<{slug_width}}  {'':>11}  {'':>11}  {total:>7}")
    lines.append(f"cap {CAP}; slack {slack} chars")

    if total > CAP:
        out = "\n".join(lines)
        sys.stderr.write(out + "\n")
        sys.stderr.write(
            f"check-description-budget: FAIL ({total} > {CAP}; over by {total - CAP} chars)\n"
        )
        sys.exit(1)

    print("\n".join(lines))
    print("check-description-budget: PASS")


if __name__ == "__main__":
    main()
