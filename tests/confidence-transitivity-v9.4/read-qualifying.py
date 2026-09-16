#!/usr/bin/env python3
"""D-13 fixture reader for backlog 999.119's confidence-transitivity captures.

This is a fixture reader for backlog 999.119's D-13 readings, not a registered gate. It loads
`scripts/check-quality-harness.py` read-only, resolved relative to its own file as
`Path(__file__).resolve().parents[2] / "scripts" / "check-quality-harness.py"`, via
`importlib.util.spec_from_file_location`, `sys.modules` registration, then `exec_module` (the
`sys.modules` registration is mandatory — without it the module's `@dataclass(frozen=True)`
raises `AttributeError: 'NoneType' object has no attribute '__dict__'` on Python 3.14).

It writes no files and changes nothing under `scripts/`.
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

_HARNESS_PATH = Path(__file__).resolve().parents[2] / "scripts" / "check-quality-harness.py"


def _load_harness():
    spec = importlib.util.spec_from_file_location("cqh_read_qualifying", _HARNESS_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules["cqh_read_qualifying"] = module
    spec.loader.exec_module(module)
    return module


CQH = _load_harness()


def _collect_files(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for raw in paths:
        p = Path(raw)
        if p.is_dir():
            for f in sorted(p.glob("*.md")):
                if f.name in ("README.md", "catalog.md"):
                    continue
                files.append(f)
        else:
            files.append(p)
    return files


def _model_and_outcome(stem: str, jsonl_dir: str | None) -> tuple[str, str]:
    if not jsonl_dir:
        return "n/a", "n/a"
    jsonl_path = Path(jsonl_dir) / f"{stem}.jsonl"
    if not jsonl_path.exists():
        return "n/a", "n/a"
    model = "n/a"
    for obj in CQH._iter_jsonl_objects(jsonl_path):
        if obj.get("type") == "system" and obj.get("subtype") == "init":
            model = obj.get("model", "n/a")
            break
    outcome = CQH.classify_invocation_outcome(jsonl_path)
    return model, outcome


def _read_one(path: Path, jsonl_dir: str | None) -> dict:
    stem = path.stem
    model, outcome = _model_and_outcome(stem, jsonl_dir)
    text = path.read_text(encoding="utf-8")

    row = {
        "capture": stem,
        "model": model,
        "outcome": outcome,
        "readable": "no",
        "chain_blocks": "n/a",
        "unpairable": "n/a",
        "confidence_inversions": "n/a",
        "qualifying": "n/a",
        "qualifying_count": "n/a",
        "qualifying_high": "n/a",
        "qualifying_unlabelled": "n/a",
        "ceiling_bound_mixed": "n/a",
        "k_reading": "n/a",
    }

    try:
        sections = CQH._slice_sections(text)
    except CQH.SectionResolutionError:
        return row

    row["readable"] = "yes"
    section4 = sections[4]
    chain_ids_raw = CQH._chain_ids(section4)
    blocks = CQH._chain_blocks(section4)
    row["chain_blocks"] = len(blocks)

    pairable = bool(chain_ids_raw) and len(chain_ids_raw) == len(blocks)
    if not pairable:
        row["unpairable"] = "yes"
        row["confidence_inversions"] = CQH.detect_defects(text, stem)["confidence_inversions"]
        return row
    row["unpairable"] = "no"

    names = [CQH._normalize_chain_id(i) for i in chain_ids_raw]
    known = set(names)

    labels: dict[str, str | None] = {}
    head_refs: dict[str, tuple[set[str], set[str]]] = {}
    for name, block in zip(names, blocks):
        labels[name] = CQH._chain_confidence_label(block)
        head_refs[name] = CQH._chain_head_refs(block)

    qualifying: list[tuple[str, str | None]] = []
    ceiling_bound_mixed = 0

    for name in names:
        gt_refs, chain_refs = head_refs[name]
        cited = ({c.casefold() for c in chain_refs} & known) - {name}
        if not cited:
            continue
        gt_unverified = any(g.endswith("?") for g in gt_refs)
        cited_labels = [labels.get(c) for c in cited]

        if (
            not gt_unverified
            and cited_labels
            and all(lbl == "MEDIUM" for lbl in cited_labels)
        ):
            qualifying.append((name, labels[name]))

        if (
            not gt_unverified
            and all(lbl is not None for lbl in cited_labels)
            and "HIGH" in cited_labels
            and ("MEDIUM" in cited_labels or "LOW" in cited_labels)
        ):
            ceiling_bound_mixed += 1

    row["qualifying_count"] = len(qualifying)
    if qualifying:
        row["qualifying"] = ",".join(
            f"{n}={lbl if lbl is not None else 'UNPARSED'}" for n, lbl in qualifying
        )
    else:
        row["qualifying"] = "-"
    row["qualifying_high"] = sum(1 for _, lbl in qualifying if lbl == "HIGH")
    row["qualifying_unlabelled"] = sum(1 for _, lbl in qualifying if lbl is None)
    row["ceiling_bound_mixed"] = ceiling_bound_mixed

    if not qualifying:
        row["k_reading"] = "n/a"
    elif all(lbl in ("MEDIUM", "LOW") for _, lbl in qualifying):
        row["k_reading"] = "yes"
    else:
        row["k_reading"] = "no"

    row["confidence_inversions"] = CQH.detect_defects(text, stem)["confidence_inversions"]
    return row


_COLUMNS = [
    "capture",
    "model",
    "outcome",
    "readable",
    "chain_blocks",
    "unpairable",
    "confidence_inversions",
    "qualifying",
    "qualifying_count",
    "qualifying_high",
    "qualifying_unlabelled",
    "ceiling_bound_mixed",
    "k_reading",
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="one or more .md files or directories")
    parser.add_argument("--jsonl-dir", default=None, help="directory holding sibling .jsonl files")
    args = parser.parse_args()

    files = _collect_files(args.paths)
    rows = [_read_one(f, args.jsonl_dir) for f in files]

    print("\t".join(_COLUMNS))
    for row in rows:
        print("\t".join(str(row[c]) for c in _COLUMNS))

    q = sum(1 for r in rows if isinstance(r["qualifying_count"], int) and r["qualifying_count"] > 0)
    k = sum(1 for r in rows if r["k_reading"] == "yes")
    no_qualifying = sum(
        1
        for r in rows
        if r["readable"] == "yes"
        and r["unpairable"] == "no"
        and isinstance(r["qualifying_count"], int)
        and r["qualifying_count"] == 0
    )
    unreadable_or_unpairable = sum(
        1 for r in rows if r["readable"] == "no" or r["unpairable"] == "yes"
    )

    print(f"Q={q}")
    print(f"K={k}")
    print(f"NO_QUALIFYING={no_qualifying}")
    print(f"UNREADABLE_OR_UNPAIRABLE={unreadable_or_unpairable}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
