#!/usr/bin/env python3
"""Enumerate each non-overlapping N -> M delta match in narrative prose outside
a recognised generated fence, across tracked Markdown and scripts/ module
docstrings, in all three spellings the containment mechanism's own exemption
covers: an arrow (an ASCII "->"/"-->" or the unicode arrow), a slash-paired
operand group on each side of that same arrow ("133/96 -> 132/97"), and the
English-prose "N to M" form.

Match count, not hop count, stated because the two differ: re.finditer is
non-overlapping, so a chain written inline as one continuous span matches once
per pair of operands, not once per hop -- the middle operand anchors the first
match's tail and cannot also anchor the next match's head. That is the same
property `_strip_citation_shaped_numbers` itself has, analysed at length as a
property of the mechanism in the claim-containment diagnosis under docs/, and
restated here as a property of this census. The counts this tool prints are
exact on match count and a floor on hop count.

Manual tool, not a CI gate — the same standing as `trace-tests-usage.py`. It
is registered in `check-firewall-battery.sh`, in
`.github/workflows/validation.yml`, and in both pre-commit hook files exactly
nowhere; registering it there would move the battery total off the value
`CLAUDE.md`'s generated CI-gate table currently states, which this tool must
not do. It reports; it changes nothing it measures.

Named tension, stated rather than hidden: this reporter is close to a
prototype of a later phase's chain-terminus containment arm. It is
deliberately NOT that arm — it asserts nothing, gates nothing, and writes no
file; promoting it into an enforcement mechanism is a decision for whoever
designs that arm, not a decision this tool makes for them.

Scope bound: the population is the delta-vector members of the shared
citation/identifier exemption tuple ONLY, not the whole tuple. A span that
some other member of that tuple would also strip is still counted here if it
matches one of the three delta spellings — membership is decided by the delta
spellings alone, never by whether a different exemption would also apply.

Granularity bound, disclosed because the counts depend on it: this census
matches per physical line (`scan_relpath` iterates `lines` and calls
`finditer` on each one), while `_strip_citation_shaped_numbers` — the function
this census exists to enumerate faithfully — is applied by
`detail_page_containment_problems` to the whole joined document text. Both
delta patterns cross newlines, because the whitespace class each one puts
between its operands matches a newline as readily as a space,
so a vector that wraps a line break is stripped by the mechanism but is NOT
enumerated here. Worked instance, from this project's own tree: a three-hop
phase-chain citation whose second arrow closes one line and whose third
operand opens the next yields one match line-scoped and two document-scoped.
(That instance is described rather than transcribed on purpose — writing the
literal here would add a row to the `py-docstrings` rung this module's own
ladder reports.) The printed counts are therefore a floor on what the
mechanism strips, not an equality with it.

Pre-registered widening ladder, walked in this order, every rung published
with its count whatever that count is, including zero:

  md-narrow      the containment module's own narrow Markdown surface list,
                 fence-aware.
  md-all         every tracked Markdown path in the repository, fence-aware
                 where a recognised fence exists.
  py-docstrings  the module docstring of every Python file directly under
                 scripts/.
  shared-text    tracked Markdown under the shared methodology source tree.
                 Subset of md-all; isolates the shipped methodology surface
                 rather than adding population of its own.

Usage:
    python3 scripts/census-delta-vectors.py --rung md-narrow
    python3 scripts/census-delta-vectors.py --rung all --format tsv > out.tsv

Exit status is clean only on a complete, uncompromised run. An unreadable
file, a failed source-control listing, or a pattern-fidelity failure (the
two expected delta-vector regexes are no longer live members of the source
tuple) each make the run partial; the tool then prints an explicit stderr
message saying do not quote these numbers and exits non-zero. It carries no
offline gate-check flag and no file-mutating flag of its own — this is a
plain reporter, not a registered checker, and it mutates nothing it reads.
"""

from __future__ import annotations

import argparse
import ast
import importlib.util
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import NamedTuple

REPO_ROOT = Path(__file__).resolve().parent.parent

# --- load scripts/gen-gate-docs.py as a module, never retype its regexes ---

_GATE_DOCS_PATH = REPO_ROOT / "scripts" / "gen-gate-docs.py"
_spec = importlib.util.spec_from_file_location("_gen_gate_docs", _GATE_DOCS_PATH)
_gate_docs = importlib.util.module_from_spec(_spec)  # type: ignore[arg-type]
sys.modules["_gen_gate_docs"] = _gate_docs  # MUST precede exec_module (module executes
# `_this_module = sys.modules[__name__]` at module scope)
_spec.loader.exec_module(_gate_docs)  # type: ignore[union-attr]

# The three delta-vector pattern strings this census is faithful to, quoted
# verbatim from `_CITATION_SHAPE_RES`'s own three entries, never retyped as a
# second, independently-written grammar. Selected below by exact `.pattern`
# match against the live tuple — if any string is absent from the live
# tuple, the census is no longer faithful to the mechanism it was built to
# enumerate and refuses to run.
_EXPECTED_ARROW_PATTERN = r"\d[\d,]*\s*(?:→|-->|->)\s*\d[\d,]*"
_EXPECTED_ENGLISH_PATTERN = r"\b\d{1,4}\s+to\s+\d{1,4}\b"
# Added Phase 25 (CONTAIN-02): the slash-paired transition vector this
# census's own docstring previously anticipated as "a THIRD delta spelling".
_EXPECTED_SLASH_PATTERN = r"\d[\d,]*(?:/\d[\d,]*)+\s*(?:→|-->|->)\s*\d[\d,]*(?:/\d[\d,]*)+"

# Membership pin, deliberately re-pinned by hand. The three `.pattern`
# selections above are one-directional: they catch a delta spelling being
# REMOVED from `_CITATION_SHAPE_RES`, and catch nothing at all when a FOURTH
# delta spelling is ADDED to it (an en-dash range, an `N=>M` form). In that
# case this census would keep exiting 0 while enumerating a strictly smaller
# population than the mechanism strips, and the docstring's claim to cover "the
# delta-vector members of the shared citation/identifier exemption tuple" would
# silently become false — the failure mode most likely to matter, and the one
# the pattern pins do not reach. Pinning the tuple's length turns any change in
# its membership into a refusal to run plus a named stderr message.
#
# Pinned against `scripts/gen-gate-docs.py` at commit ca65d3b (27 members),
# re-pinned at commit b661281 (28 members, the slash-paired member landing in
# the same phase this comment was updated). Bumping this number is a
# deliberate act: re-adjudicate which members are delta spellings, and update
# `_EXPECTED_ARROW_PATTERN`/`_EXPECTED_ENGLISH_PATTERN`/`_EXPECTED_SLASH_PATTERN`
# if the answer changed, before quoting any count this tool prints.
_PINNED_TUPLE_LEN = 28

ORDERED_RUNGS: tuple[str, ...] = ("md-narrow", "md-all", "py-docstrings", "shared-text")


class Row(NamedTuple):
    rung: str
    path: str
    line: int
    spelling: str
    match: str
    fenced: bool
    context: str


def select_delta_patterns() -> tuple[re.Pattern[str], re.Pattern[str], re.Pattern[str]] | None:
    """The live arrow/english/slash delta-vector `re.Pattern` objects,
    selected out of `_gen_gate_docs._CITATION_SHAPE_RES` by exact `.pattern`
    string match. Returns None and prints a named error to stderr if any is
    missing, or if the tuple's own membership count no longer matches
    `_PINNED_TUPLE_LEN` — the second check is what catches a delta spelling
    being ADDED, which the per-pattern selections cannot see."""
    live_len = len(_gate_docs._CITATION_SHAPE_RES)
    if live_len != _PINNED_TUPLE_LEN:
        print(
            "FIDELITY FLOOR FAILED — _gen_gate_docs._CITATION_SHAPE_RES membership has "
            f"changed since this census was pinned (expected {_PINNED_TUPLE_LEN} members, "
            f"found {live_len}). A member added to that tuple may be a fourth delta "
            "spelling this census does not enumerate, which would make its counts a "
            "strictly smaller population than the mechanism strips. Re-adjudicate which "
            "members are delta spellings and re-pin _PINNED_TUPLE_LEN before quoting any "
            "count.",
            file=sys.stderr,
        )
        return None
    arrow: re.Pattern[str] | None = None
    english: re.Pattern[str] | None = None
    slash: re.Pattern[str] | None = None
    for pattern in _gate_docs._CITATION_SHAPE_RES:
        if pattern.pattern == _EXPECTED_ARROW_PATTERN:
            arrow = pattern
        elif pattern.pattern == _EXPECTED_ENGLISH_PATTERN:
            english = pattern
        elif pattern.pattern == _EXPECTED_SLASH_PATTERN:
            slash = pattern
    missing = []
    if arrow is None:
        missing.append("the arrow-transition delta-vector pattern")
    if english is None:
        missing.append("the English-prose 'N to M' delta-vector pattern")
    if slash is None:
        missing.append("the slash-paired transition-vector delta pattern")
    if missing:
        print(
            "FIDELITY FLOOR FAILED — " + " and ".join(missing) + " no longer appear as a "
            "live member of _gen_gate_docs._CITATION_SHAPE_RES with the expected .pattern "
            "string. The census would no longer be faithful to the diagnosed mechanism; "
            "refusing to fall back to a locally-defined regex.",
            file=sys.stderr,
        )
        return None
    return arrow, english, slash


def _git_ls_files(pathspec: str) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", pathspec],
        cwd=REPO_ROOT, capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"git ls-files {pathspec!r} exited {result.returncode}: {result.stderr.strip()}"
        )
    return sorted(line for line in result.stdout.splitlines() if line)


def _matches_narrow_glob(relpath: str, pattern: str) -> bool:
    """Whether one tracked repo-relative path is selected by one
    `LITERAL_SCAN_MD_GLOBS` entry, reproducing `Path.glob`'s own semantics
    rather than `fnmatch`'s: a literal entry matches by full equality (so a
    nested `sub/CLAUDE.md` is not selected by the entry `CLAUDE.md`), and a
    `*` never crosses a path separator (so `docs/gates/*.md` does not select
    `docs/gates/sub/x.md`)."""
    if "*" not in pattern:
        return relpath == pattern
    candidate, glob = PurePosixPath(relpath), PurePosixPath(pattern)
    return len(candidate.parts) == len(glob.parts) and candidate.match(pattern)


def files_for_rung(rung: str) -> list[str]:
    """Repo-relative paths for one rung of the ladder, per its pre-registered
    definition. Raises RuntimeError on a source-control listing failure."""
    if rung == "md-narrow":
        # A filter over the tracked listing, NOT a filesystem glob, so all four
        # rungs share one source of truth. Enumerating the filesystem here let an
        # untracked or gitignored `docs/gates/*.md` — a scratch copy, a
        # mutation-test artifact — enter `md-narrow` while never entering
        # `md-all`, silently breaking the ladder's documented subset relation
        # with a clean exit and no warning.
        return sorted(
            relpath for relpath in _git_ls_files("*.md")
            if any(_matches_narrow_glob(relpath, g)
                   for g in _gate_docs.LITERAL_SCAN_MD_GLOBS)
        )
    if rung == "md-all":
        return _git_ls_files("*.md")
    if rung == "py-docstrings":
        return list(_gate_docs._py_docstring_scan_scripts())
    if rung == "shared-text":
        return [p for p in _git_ls_files("shared") if p.endswith(".md")]
    raise ValueError(f"unknown rung: {rung}")


def _module_docstring(path: Path) -> tuple[str, int] | None:
    """(docstring text, starting line number in the source file) for `path`'s
    module docstring, or None if it has none. `clean=False` keeps the raw
    source text so a matched span is byte-identical to what is on disk, and
    so line offsets computed by counting newlines inside the docstring stay
    aligned with the physical source."""
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    doc = ast.get_docstring(tree, clean=False)
    if doc is None or not tree.body:
        return None
    first = tree.body[0]
    if not (isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant)):
        return None
    return doc, first.lineno


def scan_relpath(
    rung: str,
    relpath: str,
    arrow_re: re.Pattern[str],
    english_re: re.Pattern[str],
    slash_re: re.Pattern[str],
) -> tuple[list[Row], bool]:
    """Rows found in one file for one rung, plus whether the file carries a
    fence `_gen_gate_docs` recognises at all (recorded per-file, per D-09's
    requirement to state that fact even when no fence exists)."""
    full_path = REPO_ROOT / relpath
    if rung == "py-docstrings":
        parsed = _module_docstring(full_path)
        if parsed is None:
            return [], False
        text, base_lineno = parsed
        lines = text.splitlines()
        marker_pairs: tuple = ()
    else:
        text = full_path.read_text(encoding="utf-8")
        lines = text.splitlines()
        base_lineno = 1
        marker_pairs = _gate_docs._generated_marker_pairs_for(relpath)

    fenced = bool(marker_pairs)
    if fenced:
        inside = _gate_docs._generated_line_flags(lines, marker_pairs)
    else:
        inside = [False] * len(lines)

    rows: list[Row] = []
    for idx, line in enumerate(lines):
        if inside[idx]:
            continue
        for pattern, spelling in ((arrow_re, "arrow"), (english_re, "english"), (slash_re, "slash")):
            for m in pattern.finditer(line):
                rows.append(
                    Row(rung, relpath, base_lineno + idx, spelling, m.group(0), fenced, line.strip())
                )
    return rows, fenced


def _escape_md_cell(text: str) -> str:
    return text.replace("|", "\\|")


def render_markdown(rows: list[Row]) -> str:
    header = "| rung | path | line | spelling | match | fenced | context |"
    sep = "|---|---|---|---|---|---|---|"
    lines = [header, sep]
    for row in rows:
        lines.append(
            "| {} | {} | {} | {} | {} | {} | {} |".format(
                row.rung, row.path, row.line, row.spelling,
                _escape_md_cell(row.match), row.fenced, _escape_md_cell(row.context),
            )
        )
    return "\n".join(lines) + "\n"


def render_tsv(rows: list[Row]) -> str:
    lines = ["rung\tpath\tline\tspelling\tmatch\tfenced\tcontext"]
    for row in rows:
        lines.append(
            f"{row.rung}\t{row.path}\t{row.line}\t{row.spelling}\t{row.match}\t{row.fenced}\t{row.context}"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--rung", choices=(*ORDERED_RUNGS, "all"), default="all",
        help="which rung of the widening ladder to run (default: all)",
    )
    parser.add_argument(
        "--format", choices=("markdown", "tsv"), default="markdown",
        help="output table format (default: markdown)",
    )
    args = parser.parse_args()

    selected = select_delta_patterns()
    if selected is None:
        return 1
    arrow_re, english_re, slash_re = selected

    rungs = list(ORDERED_RUNGS) if args.rung == "all" else [args.rung]

    all_rows: list[Row] = []
    failures: list[str] = []

    for rung in rungs:
        try:
            paths = files_for_rung(rung)
        except RuntimeError as exc:
            failures.append(str(exc))
            continue

        per_file: dict[str, tuple[int, bool]] = {}
        rung_rows: list[Row] = []
        for relpath in paths:
            try:
                rows, fenced = scan_relpath(rung, relpath, arrow_re, english_re, slash_re)
            except (OSError, UnicodeDecodeError, SyntaxError) as exc:
                failures.append(f"{rung}: could not read {relpath}: {exc}")
                continue
            rung_rows.extend(rows)
            # Recorded per file, per D-09, even at zero: whether this file carries
            # a fence `_gen_gate_docs` recognises at all.
            per_file[relpath] = (len(rows), fenced)

        all_rows.extend(rung_rows)
        print(f"[census] rung={rung} total_vectors={len(rung_rows)}", file=sys.stderr)
        for relpath in sorted(per_file):
            count, fenced = per_file[relpath]
            print(f"[census]   {relpath} (fenced={fenced}): {count}", file=sys.stderr)

    output = render_markdown(all_rows) if args.format == "markdown" else render_tsv(all_rows)
    sys.stdout.write(output)

    if failures:
        print(
            "\nINCOMPLETE — {} failure(s) (listed above as [warn]-shaped entries in this "
            "message). Every path that failed contributes zero rows, so the printed counts "
            "understate the population. Do not quote these numbers.".format(len(failures)),
            file=sys.stderr,
        )
        for failure in failures:
            print(f"[warn] {failure}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
