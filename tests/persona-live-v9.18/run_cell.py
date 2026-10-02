#!/usr/bin/env python3
"""Single-cell paid-run protocol for the PEX-02 live persona reading.

Pre-registered in docs/v9.18-persona-live-reading.md. Runs one
`/first-principles:persona <role>` call against one frozen source, in an isolated
scratch working directory outside the repo, and appends one manifest line recording
the outcome. `--dry-run` previews the argv without spending anything. A usage-limit
stub stops the whole sequence (exit 3) rather than being silently retried -- the
caller resumes later by re-running the same cell.

This script never checks the persona view it copies out; `scripts/check-persona-view.py`
is a separate, later step, so the runner cannot shape its own verdict.

Usage:
    python3 run_cell.py --source sources/analysis-<UTC>.md --role <role> \\
        --work <scratch dir outside the repo> --out <dir inside tests/persona-live-v9.18/> \\
        --manifest <jsonl path> --cell <id> [--dry-run]
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PRIVATE_DIR = (REPO_ROOT / ".first-principles").resolve()
PLUGIN_DIR = REPO_ROOT / "first-principles"

MODEL = "claude-opus-5-5"
ALLOWED_ROLES = ("decision-owner", "operator", "risk", "skeptic")

_UTC_RE = re.compile(r"analysis-(\d{8}T\d{6}Z)\.md$")


def _load_is_limit_stub():
    """Load `is_limit_stub` from scripts/check-trackb-comparative.py by path.

    Registered in sys.modules BEFORE exec_module -- its dataclasses raise
    AttributeError on Python 3.14 otherwise (measured at plan time on
    scripts/check-quality-harness.py).
    """
    spec = importlib.util.spec_from_file_location(
        "_trackb_comparative", REPO_ROOT / "scripts" / "check-trackb-comparative.py"
    )
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_trackb_comparative"] = mod
    spec.loader.exec_module(mod)
    return mod.is_limit_stub


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def utc_stamp(source: Path) -> str:
    m = _UTC_RE.search(source.name)
    if not m:
        raise SystemExit(f"source filename does not match analysis-<UTC>.md: {source.name}")
    return m.group(1)


def build_argv(role: str, source_name: str) -> tuple[list[str], str]:
    prompt = f"/first-principles:persona {role} .first-principles/{source_name}"
    argv = [
        "claude", "-p", "--model", MODEL,
        "--plugin-dir", str(PLUGIN_DIR.resolve()),
        "--output-format", "stream-json", "--verbose",
        "--no-session-persistence", "--permission-mode", "bypassPermissions",
        prompt,
    ]
    return argv, prompt


def last_result(jsonl: str) -> dict:
    """The last `type == "result"` event in the stream, or {} if none."""
    last: dict = {}
    for line in jsonl.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("type") == "result":
            last = obj
    return last


def _append_manifest(path: Path, entry: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry) + "\n")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", required=True, type=Path)
    ap.add_argument("--role", required=True)
    ap.add_argument("--work", required=True, type=Path,
                     help="scratch working directory, must resolve outside the repo")
    ap.add_argument("--out", required=True, type=Path,
                     help="directory inside tests/persona-live-v9.18/ to receive the persona file")
    ap.add_argument("--manifest", required=True, type=Path)
    ap.add_argument("--cell", required=True)
    ap.add_argument("--dry-run", action="store_true")
    return ap.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if args.role not in ALLOWED_ROLES:
        print(
            f"refused: role {args.role!r} is not one of {ALLOWED_ROLES} -- this runner "
            "never makes a single `all` run, only twelve independent single-role runs",
            file=sys.stderr,
        )
        return 2

    source = args.source.resolve()
    if source == PRIVATE_DIR or PRIVATE_DIR in source.parents:
        print(
            f"refused: --source {args.source} resolves under the user's private "
            f"{PRIVATE_DIR} -- that directory is never read by this runner",
            file=sys.stderr,
        )
        return 2

    utc = utc_stamp(source)
    source_name = source.name
    expected_persona = f"persona-{args.role}-{utc}.md"
    argv_cmd, prompt = build_argv(args.role, source_name)

    work_resolved = args.work.resolve()
    if work_resolved == REPO_ROOT or REPO_ROOT in work_resolved.parents:
        print(f"refused: --work {args.work} resolves inside the repo {REPO_ROOT}",
              file=sys.stderr)
        return 2

    cell_dir = work_resolved / args.cell
    if cell_dir.exists() and any(cell_dir.iterdir()):
        print(f"refused: --work/{args.cell} already exists and is non-empty: {cell_dir}",
              file=sys.stderr)
        return 2

    if args.dry_run:
        print(json.dumps(argv_cmd))
        return 0

    if not source.is_file():
        print(f"refused: --source does not exist: {source}", file=sys.stderr)
        return 2

    fp_dir = cell_dir / ".first-principles"
    fp_dir.mkdir(parents=True, exist_ok=True)
    source_copy = fp_dir / source_name
    source_copy.write_bytes(source.read_bytes())
    source_sha_before = sha256_of(source_copy)

    started = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    proc = subprocess.run(argv_cmd, capture_output=True, text=True, cwd=cell_dir, timeout=1800)
    finished = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    raw_text = proc.stdout
    raw_path = cell_dir / "raw.jsonl"
    raw_path.write_text(raw_text, encoding="utf-8")
    raw_sha256 = sha256_of(raw_path)

    manifest_entry = {
        "cell": args.cell,
        "source": source_name,
        "source_sha256": source_sha_before,
        "role": args.role,
        "model": MODEL,
        "prompt": prompt,
        "started": started,
        "finished": finished,
        "raw_sha256": raw_sha256,
    }

    is_limit_stub = _load_is_limit_stub()
    if is_limit_stub(raw_text):
        manifest_entry["status"] = "limit_stub"
        _append_manifest(args.manifest, manifest_entry)
        print(f"[limit_stub] {args.cell}: usage-limit stub -- stop the sequence, "
              "re-run this same cell to resume", file=sys.stderr)
        return 3

    result_obj = last_result(raw_text)
    manifest_entry.update({
        "is_error": result_obj.get("is_error"),
        "subtype": result_obj.get("subtype"),
        "num_turns": result_obj.get("num_turns"),
        "total_cost_usd": result_obj.get("total_cost_usd"),
    })

    files_after = sorted(p.name for p in fp_dir.iterdir())
    source_unchanged = source_copy.is_file() and sha256_of(source_copy) == source_sha_before
    persona_present = expected_persona in files_after
    extra_files = [f for f in files_after if f not in (source_name, expected_persona)]

    persona_sha256 = None
    if persona_present:
        persona_src = fp_dir / expected_persona
        args.out.mkdir(parents=True, exist_ok=True)
        persona_dst = args.out / expected_persona
        persona_dst.write_bytes(persona_src.read_bytes())
        persona_sha256 = sha256_of(persona_dst)

    status = "complete" if persona_present else "no_file"
    manifest_entry.update({
        "persona": expected_persona if persona_present else None,
        "persona_sha256": persona_sha256,
        "source_unchanged": source_unchanged,
        "extra_files": extra_files,
        "status": status,
    })
    _append_manifest(args.manifest, manifest_entry)
    return 0 if status == "complete" else 4


if __name__ == "__main__":
    sys.exit(main())
