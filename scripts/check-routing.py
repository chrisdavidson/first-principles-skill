#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Routing battery harness for the first-principles agent.

Why this exists:
    Phase 29 ran its routing battery out of `/tmp/phase29-battery/*.sh` — an
    ephemeral shell harness that lived on a single developer's machine. That
    approach proved the v2 catalog (8/8 P + 9/10 N) but could not be re-run
    by anyone else, was not under version control, and could not score
    expanded catalogs in later phases. This script is the checked-in,
    hardened replacement.

    See:
      - .planning/RETROSPECTIVE.md (v3.0 section on stream-json subagent capture)
      - .planning/milestones/v3.0-phases/25-agent-description-and-frontmatter-hardening/25-02-PLAN.md
        (battery scoring harness — first iteration)
      - .planning/milestones/v3.0-phases/29-routing-catalog-rewrite/29-01-PLAN.md
        (battery v2 — locked transport + detection)

    The transport flags and two-signal detection rule are ported verbatim
    from Phase 29's `detect_routing` bash function (D-10, D-11).

    Sequential execution only (D-12): the script issues prompts one at a
    time against a fresh `claude -p` session per prompt. Parallel execution
    risks rate-limit interference between fresh sessions and would
    contaminate the very routing decisions we are measuring. Promote to
    parallel only after seeing real-world execution times.

Usage:
    scripts/check-routing.py --catalog <path> [--plugin-dir <path>] [--out <dir>]
                             [--p-threshold N] [--n-threshold N] [--quiet]
                             [--dry-run]
    scripts/check-routing.py --self-test

Defaults:
    --plugin-dir   $(pwd)/first-principles
    --out          /tmp/check-routing-<UTC-timestamp>/
    --p-threshold  8   (P-cases >= 8/10 DELEGATE)
    --n-threshold  15  (N-cases >= 15/17 NO-DELEGATE)
    --repeat       3
    --min-pass     2

Exit codes:
    0  thresholds met (battery PASS), --self-test all fixtures correct,
       or --dry-run successful parse
    1  thresholds not met (battery FAIL) or --self-test fixture mismatch
    2  environment error (claude missing, catalog parse error, IO error,
       invalid CLI args)
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Literal


REPO_ROOT: Path = Path(__file__).resolve().parents[1]
DEFAULT_PLUGIN_DIR: Path = REPO_ROOT / "first-principles"

Verdict = Literal["DELEGATE", "NO-DELEGATE"]

# The six expected first-principles agent section-header categories
# (Signal B). Each category is a tuple of synonyms that all map to the
# same logical category (so "abandoned" and "dead-end" count as one).
_HEADER_CATEGORIES: list[tuple[str, ...]] = [
    ("essence",),
    ("assumption",),
    ("ground.?truth", "ground truth"),
    ("derivation",),
    ("abandoned", "dead.?end", "dead end"),
    ("conclusion", "verdict"),
]

# Compiled detection regexes
_HEADER_LINE_RE = re.compile(
    r"^#+\s*.*("
    r"essence|"
    r"assumption|"
    r"ground[- ]?truth|"
    r"derivation|"
    r"abandoned|dead[- ]?end|"
    r"conclusion|verdict"
    r")",
    re.IGNORECASE,
)
_SIGNAL_A_FALLBACK_RE = re.compile(
    r'"(subagent_type|agent[_-]?name|agent_id)"\s*:\s*"first-principles',
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Prompt:
    """One row from the routing catalog."""

    id: str
    text: str
    expected: Verdict


# ---------------------------------------------------------------------------
# Catalog parsing
# ---------------------------------------------------------------------------


def _strip_quotes(s: str) -> str:
    s = s.strip()
    if len(s) >= 2 and s[0] in ('"', "'") and s[-1] == s[0]:
        return s[1:-1]
    return s


def _split_row(line: str) -> list[str]:
    """Split a Markdown table row on `|`, returning trimmed cells.

    Leading/trailing `|` produce empty cells which we drop.
    """
    parts = [c.strip() for c in line.split("|")]
    # Drop the empty cells from leading/trailing pipes
    if parts and parts[0] == "":
        parts = parts[1:]
    if parts and parts[-1] == "":
        parts = parts[:-1]
    return parts


def _is_separator_row(cells: list[str]) -> bool:
    """A separator row in a Markdown table is all dashes (with optional colons)."""
    if not cells:
        return False
    return all(re.fullmatch(r":?-{3,}:?", c) is not None for c in cells)


def parse_catalog(path: Path) -> tuple[list[Prompt], list[Prompt]]:
    """Parse a 25-DELEGATION-TESTS.md-shaped Markdown catalog.

    Returns (positives, negatives). Rows are classified by the prefix of
    the id cell: `P*` -> positive, `N*` -> negative. Other ids are ignored.

    Raises FileNotFoundError if path missing, ValueError on parse error
    or empty result.
    """
    if not path.exists():
        raise FileNotFoundError(f"catalog not found: {path}")

    positives: list[Prompt] = []
    negatives: list[Prompt] = []

    in_table = False
    expecting_separator = False

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if not line.startswith("|"):
            in_table = False
            expecting_separator = False
            continue

        cells = _split_row(line)
        if not cells:
            in_table = False
            continue

        # Detect header row by presence of a column literally "Prompt"
        # case-insensitively in cell 2 — that is the catalog's signature.
        # The row immediately after a header is the separator row.
        if not in_table:
            if len(cells) >= 3 and cells[1].strip().lower() == "prompt":
                in_table = True
                expecting_separator = True
                continue
            # Not a header; treat any stray pipe-line as noise.
            continue

        if expecting_separator:
            expecting_separator = False
            if _is_separator_row(cells):
                continue
            # Some catalogs may omit the separator; fall through and treat
            # the row as data.

        # Data row.
        if len(cells) < 3:
            continue
        rid = cells[0].strip()
        prompt_text = _strip_quotes(cells[1])
        expected_raw = cells[2].strip().upper()

        # Skip id cells that do not start with P or N
        if not rid or rid[0] not in ("P", "N"):
            continue

        if expected_raw not in ("DELEGATE", "NO-DELEGATE"):
            raise ValueError(
                f"row {rid!r}: expected verdict must be 'DELEGATE' or 'NO-DELEGATE', "
                f"got {expected_raw!r}"
            )

        prompt = Prompt(id=rid, text=prompt_text, expected=expected_raw)  # type: ignore[arg-type]
        if rid.startswith("P"):
            positives.append(prompt)
        else:
            negatives.append(prompt)

    if not positives and not negatives:
        raise ValueError(f"catalog {path} contained no P* or N* rows")
    return positives, negatives


# ---------------------------------------------------------------------------
# Detection (Signal A / Signal B)
# ---------------------------------------------------------------------------


def _walk(obj: object) -> Iterable[object]:
    """Yield every node in a nested JSON-like structure (dicts/lists/scalars)."""
    yield obj
    if isinstance(obj, dict):
        for v in obj.values():
            yield from _walk(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _walk(v)


def _signal_a(parsed_lines: list[object], raw_text: str) -> bool:
    """Signal A: a Task tool_use with subagent_type 'first-principles'.

    Strategy:
      1. Structured walk: for every dict with name == "Task", stringify
         its `input` and case-insensitively search for "first-principles".
      2. Regex fallback over the raw text for the documented patterns.
    """
    needle = "first-principles"
    for parsed in parsed_lines:
        for node in _walk(parsed):
            if isinstance(node, dict) and node.get("name") == "Task":
                blob = json.dumps(node.get("input", {}))
                if needle in blob.lower():
                    return True
    if _SIGNAL_A_FALLBACK_RE.search(raw_text):
        return True
    return False


def _signal_b(parsed_lines: list[object]) -> bool:
    """Signal B: >= 4 of 6 expected agent section headers in text nodes."""
    text_blobs: list[str] = []
    for parsed in parsed_lines:
        for node in _walk(parsed):
            if isinstance(node, dict):
                t = node.get("text")
                if isinstance(t, str):
                    text_blobs.append(t)
    joined = "\n".join(text_blobs)

    matched_categories: set[int] = set()
    for line in joined.splitlines():
        m = _HEADER_LINE_RE.match(line)
        if not m:
            continue
        token = m.group(1).lower()
        for idx, syns in enumerate(_HEADER_CATEGORIES):
            for syn in syns:
                if re.search(syn, token, re.IGNORECASE):
                    matched_categories.add(idx)
                    break
    return len(matched_categories) >= 4


def detect_routing(jsonl_path: Path) -> Verdict:
    """Score a captured stream-json event log as DELEGATE or NO-DELEGATE.

    Ports Phase 29's `detect_routing` bash function: DELEGATE iff Signal A
    or Signal B fires; NO-DELEGATE otherwise.
    """
    raw_text = jsonl_path.read_text(encoding="utf-8", errors="replace")
    parsed_lines: list[object] = []
    for line in raw_text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            parsed_lines.append(json.loads(line))
        except json.JSONDecodeError:
            # Non-JSON line (e.g., stderr leakage); skip but raw_text still
            # captures it for the regex fallback in Signal A.
            continue

    if _signal_a(parsed_lines, raw_text):
        return "DELEGATE"
    if _signal_b(parsed_lines):
        return "DELEGATE"
    return "NO-DELEGATE"


# ---------------------------------------------------------------------------
# Transport: invoke claude -p per prompt
# ---------------------------------------------------------------------------


def _run_prompt_to(prompt: Prompt, plugin_dir: Path, out_path: Path) -> Path:
    """Issue one prompt via `claude -p` and capture the stream-json log to out_path.

    Transport per D-10 (verbatim):
        claude -p --plugin-dir <path> --no-session-persistence \
          --output-format stream-json --verbose \
          --permission-mode bypassPermissions <prompt>

    Returns out_path (combined stdout + stderr written there).
    """
    argv = [
        "claude",
        "-p",
        "--plugin-dir",
        str(plugin_dir),
        "--no-session-persistence",
        "--output-format",
        "stream-json",
        "--verbose",
        "--permission-mode",
        "bypassPermissions",
        prompt.text,
    ]
    # No timeout: sequential, one-prompt-at-a-time; Ctrl-C if it hangs.
    proc = subprocess.run(
        argv,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    out_path.write_bytes(proc.stdout or b"")
    return out_path


def _run_prompt(prompt: Prompt, plugin_dir: Path, out_dir: Path) -> Path:
    """Issue one prompt via `claude -p` and capture the stream-json log.

    Legacy single-run interface — writes to `out_dir/<id>.jsonl`.
    Preserved for backward compatibility; delegates to _run_prompt_to.

    Returns the path of the captured <out>/<id>.jsonl file.
    """
    return _run_prompt_to(prompt, plugin_dir, out_dir / f"{prompt.id}.jsonl")


def _run_prompt_n_times(
    prompt: Prompt, plugin_dir: Path, out_dir: Path, repeat: int
) -> list[Verdict]:
    """Run a single prompt N times and return a list of N Verdict values.

    When repeat == 1, writes to <id>.jsonl (legacy parity — no -run suffix).
    When repeat > 1, writes to <id>-run<n>.jsonl (1-indexed, n in 1..repeat).
    """
    results: list[Verdict] = []
    for run_idx in range(repeat):
        if repeat == 1:
            out_path = out_dir / f"{prompt.id}.jsonl"
        else:
            out_path = out_dir / f"{prompt.id}-run{run_idx + 1}.jsonl"
        jsonl_path = _run_prompt_to(prompt, plugin_dir, out_path)
        results.append(detect_routing(jsonl_path))
    return results


# ---------------------------------------------------------------------------
# Battery driver
# ---------------------------------------------------------------------------


def _ensure_claude_available() -> None:
    if shutil.which("claude") is None:
        print(
            "error: `claude` CLI not found on PATH; cannot run the routing battery",
            file=sys.stderr,
        )
        sys.exit(2)


def _print(msg: str, quiet: bool) -> None:
    if not quiet:
        print(msg, flush=True)


def run_battery(
    positives: list[Prompt],
    negatives: list[Prompt],
    plugin_dir: Path,
    out_dir: Path,
    p_threshold: int,
    n_threshold: int,
    quiet: bool,
    repeat: int = 1,
    min_pass: int = 1,
) -> int:
    """Run the full battery, write outputs, return 0 (PASS) or 1 (FAIL).

    When repeat == 1 (legacy mode), output is byte-identical to v3.1.
    When repeat > 1 (K-of-N mode), each prompt runs repeat times and counts
    as PASS only if min_pass-of-repeat runs match the expected verdict.
    """
    _ensure_claude_available()
    out_dir.mkdir(parents=True, exist_ok=True)

    total = len(positives) + len(negatives)
    _print(f"check-routing: catalog has {len(positives)} P + {len(negatives)} N (total {total})", quiet)
    _print(f"  plugin-dir: {plugin_dir}", quiet)
    _print(f"  out:        {out_dir}", quiet)
    _print(f"  thresholds: P >= {p_threshold}, N >= {n_threshold}", quiet)
    if repeat > 1:
        _print(f"  repeat:     {repeat} (K-of-N, min-pass={min_pass})", quiet)

    # K-of-N per-prompt data: (prompt, verdicts, match_count, prompt_passed)
    prompt_results: list[tuple[Prompt, list[Verdict], int, bool]] = []
    ordered = list(positives) + list(negatives)
    for idx, prompt in enumerate(ordered, start=1):
        _print(f"[{idx}/{total}] {prompt.id}: expected={prompt.expected} ...", quiet)
        verdicts = _run_prompt_n_times(prompt, plugin_dir, out_dir, repeat)
        match_count = sum(1 for v in verdicts if v == prompt.expected)
        prompt_passed = match_count >= min_pass
        prompt_results.append((prompt, verdicts, match_count, prompt_passed))
        if repeat == 1:
            # Legacy output format: byte-identical to v3.1
            actual = verdicts[0]
            _print(f"    -> actual={actual} {'PASS' if prompt_passed else 'FAIL'}", quiet)
        else:
            ratio_str = f"{match_count}/{repeat}"
            _print(f"    -> {ratio_str} {'PASS' if prompt_passed else 'FAIL'}", quiet)

    # scores.tsv
    scores_path = out_dir / "scores.tsv"
    with scores_path.open("w", encoding="utf-8") as fh:
        if repeat == 1:
            # Legacy format: byte-identical to v3.1
            fh.write("id\texpected\tactual\tpass\n")
            for prompt, verdicts, match_count, prompt_passed in prompt_results:
                actual = verdicts[0]
                fh.write(f"{prompt.id}\t{prompt.expected}\t{actual}\t{'pass' if prompt_passed else 'fail'}\n")
        else:
            # v3.4 per-run row format
            fh.write("id\trun\texpected\tactual\tmatch\n")
            for prompt, verdicts, match_count, prompt_passed in prompt_results:
                for run_idx, actual in enumerate(verdicts, start=1):
                    match_flag = 1 if actual == prompt.expected else 0
                    fh.write(f"{prompt.id}\t{run_idx}\t{prompt.expected}\t{actual}\t{match_flag}\n")

    p_pass = sum(
        1 for prompt, verdicts, match_count, prompt_passed in prompt_results
        if prompt.id.startswith("P") and prompt_passed
    )
    n_pass = sum(
        1 for prompt, verdicts, match_count, prompt_passed in prompt_results
        if prompt.id.startswith("N") and prompt_passed
    )
    battery_pass = p_pass >= p_threshold and n_pass >= n_threshold

    verdict_lines: list[str] = []
    verdict_lines.append(f"BATTERY: {'PASS' if battery_pass else 'FAIL'}")
    verdict_lines.append(f"P: {p_pass}/{len(positives)}  N: {n_pass}/{len(negatives)}")
    if not battery_pass:
        verdict_lines.append("")
        verdict_lines.append("Failed prompts:")
        for prompt, verdicts, match_count, prompt_passed in prompt_results:
            if not prompt_passed:
                if repeat == 1:
                    actual = verdicts[0]
                    verdict_lines.append(
                        f"  {prompt.id}: expected={prompt.expected} actual={actual}"
                    )
                else:
                    verdict_lines.append(
                        f"  {prompt.id}: expected={prompt.expected} {match_count}/{repeat} match"
                    )
    if repeat > 1:
        verdict_lines.append("")
        verdict_lines.append(f"Per-prompt K/N (best-of-{repeat}, K={min_pass}):")
        for prompt, verdicts, match_count, prompt_passed in prompt_results:
            verdict_lines.append(
                f"  {prompt.id}: {match_count}/{repeat} {'PASS' if prompt_passed else 'FAIL'}"
            )
    verdict_text = "\n".join(verdict_lines) + "\n"
    (out_dir / "verdict.txt").write_text(verdict_text, encoding="utf-8")

    # Always print verdict to stdout, even in --quiet mode
    print(verdict_text, end="")
    return 0 if battery_pass else 1


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------


# Fixture (a): DELEGATE via Signal A (Task tool_use w/ subagent_type)
_FIXTURE_SIGNAL_A = "\n".join(
    [
        json.dumps(
            {
                "type": "tool_use",
                "name": "Task",
                "input": {
                    "subagent_type": "first-principles",
                    "prompt": "Analyze from first principles ...",
                },
            }
        ),
        json.dumps({"type": "assistant", "text": "Hello world"}),
    ]
)

# Fixture (b): DELEGATE via Signal B (>= 4 distinct header categories)
_FIXTURE_SIGNAL_B = "\n".join(
    [
        json.dumps({"type": "assistant", "text": "## Essence\nThe core question is ..."}),
        json.dumps({"type": "assistant", "text": "## Assumption Audit\nWe assume ..."}),
        json.dumps({"type": "assistant", "text": "## Ground Truths\nWhat we know ..."}),
        json.dumps({"type": "assistant", "text": "## Conclusion\nTherefore ..."}),
    ]
)

# Fixture (c): NO-DELEGATE (neither signal)
_FIXTURE_NO_SIGNAL = "\n".join(
    [
        json.dumps({"type": "assistant", "text": "Hello world. Here is the answer."}),
        json.dumps({"type": "assistant", "text": "Nothing structural here at all."}),
    ]
)

# Fixture (d): DELEGATE via Signal A regex fallback (subagent_type in a
# non-Task object, exercising the raw-text fallback path)
_FIXTURE_SIGNAL_A_FALLBACK = "\n".join(
    [
        json.dumps({"type": "assistant", "text": "Hello world"}),
        # Note: name is NOT "Task" here — only the regex fallback catches it.
        json.dumps(
            {
                "type": "system",
                "name": "Other",
                "input": {"subagent_type": "first-principles"},
            }
        ),
    ]
)


def _assert_kofn(
    name: str,
    verdicts: list[Verdict],
    expected: Verdict,
    min_pass: int,
    should_pass: bool,
) -> bool:
    """Assert that K-of-N aggregation produces the expected prompt-level outcome."""
    match_count = sum(1 for v in verdicts if v == expected)
    actual_pass = match_count >= min_pass
    if actual_pass != should_pass:
        print(
            f"self-test FAIL: {name!r} expected prompt={'PASS' if should_pass else 'FAIL'}, "
            f"got {'PASS' if actual_pass else 'FAIL'} (match={match_count}/{len(verdicts)})",
            file=sys.stderr,
        )
        return False
    return True


def _run_one_fixture(name: str, body: str, expected: Verdict) -> bool:
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".jsonl", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(body)
        tmp_path = Path(tmp.name)
    try:
        actual = detect_routing(tmp_path)
        if actual != expected:
            print(
                f"self-test FAIL: fixture {name!r} expected {expected}, got {actual}",
                file=sys.stderr,
            )
            return False
        return True
    finally:
        try:
            tmp_path.unlink()
        except OSError:
            pass


def self_test() -> int:
    """Validate detection logic against in-script fixtures. No claude invocation."""
    fixtures: list[tuple[str, str, Verdict]] = [
        ("signal_a_structured", _FIXTURE_SIGNAL_A, "DELEGATE"),
        ("signal_b_headers", _FIXTURE_SIGNAL_B, "DELEGATE"),
        ("no_signal", _FIXTURE_NO_SIGNAL, "NO-DELEGATE"),
        ("signal_a_regex_fallback", _FIXTURE_SIGNAL_A_FALLBACK, "DELEGATE"),
    ]
    all_passed = True
    for name, body, expected in fixtures:
        if not _run_one_fixture(name, body, expected):
            all_passed = False

    # K-of-N aggregation fixtures (a)(b)(c)(d)
    # (a) Legacy parity: N=1, K=1 — single match, PASS
    if not _assert_kofn(
        "kofn_legacy_parity",
        verdicts=["DELEGATE"],
        expected="DELEGATE",
        min_pass=1,
        should_pass=True,
    ):
        all_passed = False

    # (b) PASS via 2-of-3: two matches out of three, min_pass=2
    if not _assert_kofn(
        "kofn_pass_2of3",
        verdicts=["DELEGATE", "NO-DELEGATE", "DELEGATE"],
        expected="DELEGATE",
        min_pass=2,
        should_pass=True,
    ):
        all_passed = False

    # (c) FAIL via 1-of-3: only one match, min_pass=2
    if not _assert_kofn(
        "kofn_fail_1of3",
        verdicts=["DELEGATE", "NO-DELEGATE", "NO-DELEGATE"],
        expected="DELEGATE",
        min_pass=2,
        should_pass=False,
    ):
        all_passed = False

    # (d) K>N rejection: --repeat 2 --min-pass 3 must exit 2 before any I/O
    try:
        rc = main(["--catalog", "/nonexistent/path/that/does/not/exist", "--repeat", "2", "--min-pass", "3"])
    except SystemExit as exc:
        rc = exc.code if isinstance(exc.code, int) else 2
    if rc != 2:
        print(
            f"self-test FAIL: 'kofn_invalid_kn_rejection' expected exit 2 (K>N guard), got {rc}",
            file=sys.stderr,
        )
        all_passed = False

    if all_passed:
        print("self-test PASS (8 fixtures)")  # Update this count if fixtures are added.
        return 0
    return 1


# ---------------------------------------------------------------------------
# Main / CLI
# ---------------------------------------------------------------------------


def _default_out_dir() -> Path:
    ts = _dt.datetime.now(_dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return Path("/tmp") / f"check-routing-{ts}"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="check-routing.py",
        description="Routing battery harness for the first-principles agent.",
    )
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--catalog",
        type=Path,
        help="Path to a Markdown routing catalog (shape of 25-DELEGATION-TESTS.md).",
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
        help=f"Plugin directory passed to `claude --plugin-dir` (default: {DEFAULT_PLUGIN_DIR}).",
    )
    p.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output directory for per-prompt .jsonl + scores.tsv + verdict.txt "
        "(default: /tmp/check-routing-<UTC-timestamp>/).",
    )
    p.add_argument(
        "--p-threshold",
        type=int,
        default=11,
        help="Min P-cases scored DELEGATE for battery PASS (default: 11).",
    )
    p.add_argument(
        "--n-threshold",
        type=int,
        default=18,
        help="Min N-cases scored NO-DELEGATE for battery PASS (default: 18).",
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
        default=3,
        metavar="N",
        help="Run each catalog prompt N times (default: 3). Use --repeat 1 for legacy single-run.",
    )
    p.add_argument(
        "--min-pass",
        type=int,
        default=2,
        metavar="K",
        help="K-of-N runs must match expected for a prompt to count as PASS (default: 2).",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()

    # K>N pre-flight guard — validated BEFORE any I/O (T-36-01)
    if args.repeat < 1:
        print("error: --repeat must be >= 1", file=sys.stderr)
        return 2
    # When --repeat 1, clamp min_pass to 1 for legacy-parity mode.
    # Otherwise validate the user-supplied --min-pass against --repeat.
    if args.repeat == 1:
        if args.min_pass != 1:
            print(
                f"warning: --repeat 1 forces --min-pass to 1 "
                f"(supplied {args.min_pass} ignored)",
                file=sys.stderr,
            )
        args.min_pass = 1
    elif args.min_pass < 1 or args.min_pass > args.repeat:
        print(
            f"error: --min-pass ({args.min_pass}) must be >= 1 and <= --repeat ({args.repeat})",
            file=sys.stderr,
        )
        return 2

    catalog_path: Path = args.catalog
    try:
        positives, negatives = parse_catalog(catalog_path)
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except ValueError as exc:
        print(f"error: failed to parse catalog: {exc}", file=sys.stderr)
        return 2

    if args.dry_run:
        print(f"Catalog: {len(positives)} P-prompts, {len(negatives)} N-prompts")
        return 0

    out_dir: Path = args.out if args.out is not None else _default_out_dir()
    try:
        return run_battery(
            positives,
            negatives,
            plugin_dir=args.plugin_dir,
            out_dir=out_dir,
            p_threshold=args.p_threshold,
            n_threshold=args.n_threshold,
            quiet=args.quiet,
            repeat=args.repeat,
            min_pass=args.min_pass,
        )
    except OSError as exc:
        print(f"error: IO failure during battery run: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
