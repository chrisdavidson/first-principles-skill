# CONF-13 Baseline: hand-maintained branch-count literals in prose

**Plan:** 21-01
**Purpose:** establish the real, noise-filtered figure for CONF-13's "hand-maintained
branch-count literals in prose" before any later plan in Phase 21 commits to a remediation
target. Three prior readings existed and all three were known-wrong: the roadmap's `9`
(self-declared partial, misses spelled-out forms), `21-RESEARCH.md`'s `1,015` raw repo-wide hits,
and its `76` hits over four files. None is a target. This document supersedes all three.

---

## Sweep method

### Vocabulary and detection shape

The sweep detects **count-bearing literals adjacent to a count noun**, over three number forms:

- **digit form** — `\d{1,4}` adjacent to a count noun
- **spelled-out form** — the number words `one` through `twenty`, the tens (`thirty` …
  `ninety`), and `hundred`, including hyphenated compounds (`fifty-eight`, `twenty-two`) — the
  axis the roadmap's own sweep admits it misses
- **range/delta form** — `<n> to <m>`, `<n> → <m>`, `<n> -> <m>`, `<n>/<m>`, `up from <n>`; a
  range collapses to **one** combined span rather than two independent number hits

**Count nouns** (singular/plural, harvested from `CLAUDE.md`'s `QUAL-01`/`SCAN-GUARD`/
`TRACE-03`/`CONF-GATE` rows per the plan's instruction, not guessed): `branch`/`branches`,
`control`/`controls`, `arm`/`arms`, `gate`/`gates`, `row`/`rows`, `entry`/`entries`,
`fixture`/`fixtures`, `surface`/`surfaces`, `call site`/`call sites`, `assertion`/`assertions`,
`check`/`checks`, `id`/`ids`, `literal`/`literals`, `stamp`/`stamps`, `pin`/`pins`, `job`/`jobs`,
`plan`/`plans`, `mutation`/`mutations`, `leg`/`legs`, `criterion`/`criteria`, `column`/`columns`,
`case`/`cases`, `probe`/`probes`, `item`/`items`.

**Adjacency window:** the noun within 3 tokens either side of the number (line-scoped — a
hard-wrapped literal is invisible, the same disclosed bound `HEADLINE-LOCK` carries; see
Disclosed bounds below).

### Two tightening passes (recorded, not hidden)

The sweep's first run (see raw figures in the git history of this document's construction, not
retained as a separate artifact per the plan's instruction to record only the final reproducible
command) measured false-positive rates above 25% on several small `.py`-docstring surfaces. Per
the plan's own instruction ("tighten the pattern and re-run Task 1's sweep rather than absorbing
the noise into the taxonomy"), two structural exclusions were added to the sweep itself (not the
classifier):

1. **Exit-code line/prose exclusion** — `Exit codes:` docstring blocks render as
   `    0  description` (a lone leading digit 0/1/2 followed by 2+ spaces); prose form
   (`exits 0 if every control behaves...`) is excluded by checking the word immediately before
   the number for `exits`/`exit`. Exit codes are never a hand-maintained branch count.
2. **Ordinal/label exclusion** — a noun from a curated set (`criterion`, `criteria`, `phase`,
   `check`, `item`, `arm`, `row`, `plan`, `leg`, `id`, `gate`, `step`) sitting **immediately
   before** a number (`Criterion 4`, `Phase 3`, `Item 3,`, `Plan 01`, `Step 0`) identifies WHICH
   instance, not HOW MANY. This is direction-based: `27 rows` / `16 branches` (number-before-noun)
   are unaffected — only noun-before-number is excluded.
3. **Section-reference exclusion** — a raw token beginning with `§` (e.g. `§2`) is never a count,
   regardless of adjacency direction, and is blanked before scanning.

After these two passes every surface's false-positive share is under the 25% ceiling (see
Classification below); the sweep pattern did not need a third tightening.

### The exact, re-runnable command

Save the two scripts below verbatim as `conf13_sweep.py` and `conf13_classify.py` in the same
directory, then run:

```sh
python3 conf13_sweep.py --selftest --repo-root /path/to/first-principles-skill
python3 conf13_sweep.py --repo-root /path/to/first-principles-skill
python3 conf13_classify.py --repo-root /path/to/first-principles-skill
```

`conf13_sweep.py` prints the `## Raw counts` table and full hit list reproduced below.
`conf13_classify.py` prints the `## Classification` table, the exemption/false-positive class
breakdowns, and the full classified hit list (the join of Task 1's hits against Task 2's
disposition — every hit appears exactly once, by construction, since the classifier consumes
`conf13_sweep.run_sweep()`'s output directly with no filtering step).

Both runs are deterministic (verified by running each twice and diffing byte-for-byte identical
output) and read-only (`git status --porcelain` before and after each run showed no change
outside this plan's two `.planning/` files).

<details>
<summary><code>conf13_sweep.py</code> (verbatim, 374 lines)</summary>

```python
#!/usr/bin/env python3
"""CONF-13 baseline sweep — measurement instrument only, not shipped.

Detects count-bearing literals (digit form, spelled-out form, range/delta form)
adjacent to a count noun, over the D-21-E candidate surface set:

    CLAUDE.md; docs/ARCHITECTURE.md; docs/TESTING.md; docs/MEASUREMENT-MAP.md;
    docs/COMPONENT-DIAGRAM.md; docs/DATA-FLOW.md; docs/README.md; docs/gates/*.md;
    and the module docstrings (ast.get_docstring()) of every script-backed
    registry entry (the 20 scripts backing the battery's script-backed gates).

Usage:
    python3 conf13_sweep.py                 # print per-surface counts + full hit list
    python3 conf13_sweep.py --selftest       # run the two falsifiability checks named
                                              # in 21-01-PLAN.md's acceptance criteria

Deterministic: no randomness, no network, no mutation of the tree (read-only).
"""
from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Vocabulary (verbatim from 21-01-PLAN.md Task 1 <action>)
# ---------------------------------------------------------------------------

_ONES_1_20 = [
    "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
    "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen",
    "eighteen", "nineteen", "twenty",
]
_ONES_1_9 = _ONES_1_20[:9]
_TENS = ["thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

# Count nouns (singular/plural), verbatim from the plan's enumerated vocabulary.
# "call site"/"call sites" is handled as a bigram separately from this set.
NOUNS: frozenset[str] = frozenset({
    "branch", "branches", "control", "controls", "arm", "arms", "gate", "gates",
    "row", "rows", "entry", "entries", "fixture", "fixtures", "surface", "surfaces",
    "assertion", "assertions", "check", "checks", "id", "ids", "literal", "literals",
    "stamp", "stamps", "pin", "pins", "job", "jobs", "plan", "plans", "mutation",
    "mutations", "leg", "legs", "criterion", "criteria", "column", "columns",
    "case", "cases", "probe", "probes", "item", "items",
})
# "call site"/"call sites" bigram noun.
BIGRAM_NOUN_HEAD = "call"
BIGRAM_NOUN_TAILS = frozenset({"site", "sites"})

_NUM_ATOM_ALTS = sorted(
    [re.escape(w) for w in (_TENS + _ONES_1_20)], key=len, reverse=True
)
# tens-ones compound, e.g. "fifty-eight"; a bare tens word e.g. "eighty";
# a bare ones word 1-20 e.g. "sixteen"; digit run 1-4 digits; "(one )?hundred".
_NUM_ATOM_RE = re.compile(
    r"(?:\d{1,4}"
    r"|(?:" + "|".join(sorted([re.escape(w) for w in _TENS], key=len, reverse=True)) + r")"
    r"(?:-(?:" + "|".join(sorted([re.escape(w) for w in _ONES_1_9], key=len, reverse=True)) + r"))?"
    r"|" + "|".join(_NUM_ATOM_ALTS) + r"|(?:one\s+)?hundred)",
    re.IGNORECASE,
)

_RANGE_SEP = {"to", "→", "->"}

# Ordinal/label nouns: when one of these sits IMMEDIATELY before a number
# ("Criterion 4", "Phase 3", "Item 3,", "Plan 01", "Check 5", "Arm 4",
# "Row 03", "Leg 4", "ID 12", "Gate 5"), the number identifies WHICH
# instance, not HOW MANY — direction-based, so "27 rows" / "16 branches"
# (number-before-noun) are unaffected. Tightened after Task 1's first run
# measured this as the dominant false-positive source on several small
# .py-docstring surfaces (exceeding the 25% per-surface ceiling).
_ORDINAL_ADJACENT_NOUNS = frozenset({
    "criterion", "criteria", "phase", "check", "item", "arm", "row",
    "plan", "leg", "id", "gate", "step",
})

# "exits 0 if every control ...", "exits 1 if any control ..." — prose-form
# exit-code statements (as opposed to the tabular _EXIT_CODE_LINE_RE shape
# above). The word immediately before the number, not a noun, is the
# reliable signal here.
_EXIT_CODE_PROSE_WORDS = frozenset({"exits", "exit"})

# "Exit codes:" docstring blocks render as "    0  description", a single
# leading digit (0/1/2) followed by 2+ spaces then prose — this shape is
# unique to that enumeration and never a hand-maintained count. Tightened
# for the same reason as _ORDINAL_ADJACENT_NOUNS above.
_EXIT_CODE_LINE_RE = re.compile(r"^\s*[012]\s{2,}\S")

# ---------------------------------------------------------------------------
# Candidate surfaces (D-21-E)
# ---------------------------------------------------------------------------

MD_GLOB_SURFACES = [
    "CLAUDE.md",
    "docs/ARCHITECTURE.md",
    "docs/TESTING.md",
    "docs/MEASUREMENT-MAP.md",
    "docs/COMPONENT-DIAGRAM.md",
    "docs/DATA-FLOW.md",
    "docs/README.md",
    "docs/gates/*.md",
]

# The 20 scripts backing the battery's script-backed gate registrations
# (scripts/check-firewall-battery.sh `gate "<ID>" ... "python3 scripts/<X>.py" ...`
# lines), i.e. every registry entry with a Python module to introspect via
# ast.get_docstring(). Orphans with no script (VAL-01, VAL-02, VAL-03's pytest
# leg, INVARIANT-CHECK, FROZEN-EVIDENCE) are excluded by construction, matching
# D-21-E / D-01's measured "5 gates with no Python script" finding.
PY_DOCSTRING_SURFACES = [
    "scripts/sync-content.py",
    "scripts/check-step0-live.py",
    "scripts/check-step0-emulator.py",
    "scripts/check-links.py",
    "scripts/check-trigger-collisions.py",
    "scripts/check-description-budget.py",
    "scripts/check-version-stamps.py",
    "scripts/check-registration.py",
    "scripts/check-agent.py",
    "scripts/check-routing-battery.py",
    "scripts/check-traceability.py",
    "scripts/check-install-collisions.py",
    "scripts/check-quality-harness.py",
    "scripts/check-provenance.py",
    "scripts/check-act-limb.py",
    "scripts/check-loop-closure.py",
    "scripts/check-focused-parity.py",
    "scripts/check-selfaudit-scan.py",
    "scripts/check-high-confidence-bound.py",
    "scripts/check-conf-gate.py",
]


class Hit:
    __slots__ = ("surface", "line", "text")

    def __init__(self, surface: str, line: int, text: str) -> None:
        self.surface = surface
        self.line = line
        self.text = text

    def key(self) -> str:
        return f"{self.surface}:{self.line}: {self.text}"


def _tokenize(line: str) -> list[tuple[int, int, str]]:
    """Return (start, end, raw_token) for every whitespace-delimited token."""
    return [(m.start(), m.end(), m.group()) for m in re.finditer(r"\S+", line)]


def _clean(raw: str) -> str:
    """Strip leading/trailing punctuation, keep internal hyphens/word chars."""
    return re.sub(r"^[^\w]+|[^\w]+$", "", raw)


def _is_num_atom(clean: str) -> bool:
    if not clean:
        return False
    return bool(re.fullmatch(_NUM_ATOM_RE, clean))


def _is_noun(clean: str) -> bool:
    return clean.lower() in NOUNS


def scan_text(surface: str, text: str) -> list[Hit]:
    """Scan one surface's text (already decoded) for count-noun-adjacent
    number literals. Line-scoped (disclosed bound, matches HEADLINE-LOCK)."""
    hits: list[Hit] = []
    lines = text.splitlines()
    for lineno, line in enumerate(lines, start=1):
        if _EXIT_CODE_LINE_RE.match(line):
            continue
        toks = _tokenize(line)
        cleaned = [_clean(t[2]) for t in toks]
        n = len(toks)
        # "§N" section-reference tokens are identifiers, never counts,
        # regardless of adjacency direction — blank them out before scanning.
        for _si in range(n):
            if toks[_si][2].startswith("§"):
                cleaned[_si] = ""

        # ---- "up from <N>" arm (Arm B): hit regardless of adjacent noun ----
        for i in range(n - 1):
            if cleaned[i].lower() == "up" and i + 1 < n and cleaned[i + 1].lower() == "from":
                if i + 2 < n and _is_num_atom(cleaned[i + 2]):
                    start = toks[i][0]
                    end = toks[i + 2][1]
                    hits.append(Hit(surface, lineno, line[start:end]))

        # ---- primary noun-adjacency arm, with range/slash combination ----
        i = 0
        while i < n:
            if not _is_num_atom(cleaned[i]):
                i += 1
                continue
            span_start_idx = i
            span_end_idx = i
            # slash-combined single token, e.g. "58/72"
            slash_m = re.fullmatch(r"(\d{1,4})/(\d{1,4})", cleaned[i])
            if slash_m:
                span_end_idx = i
            # two-token range: "<num> to|→|-> <num>"
            elif i + 2 < n and cleaned[i + 1] in _RANGE_SEP and _is_num_atom(cleaned[i + 2]):
                span_end_idx = i + 2
            # "one hundred" spelled as two tokens
            elif cleaned[i].lower() == "one" and i + 1 < n and cleaned[i + 1].lower() == "hundred":
                span_end_idx = i + 1

            window_lo = max(0, span_start_idx - 3)
            window_hi = min(n - 1, span_end_idx + 3)

            # ordinal/label exclusion: a noun in _ORDINAL_ADJACENT_NOUNS
            # immediately before the span (distance 1, noun-then-number
            # order) identifies which instance, not how many.
            if (
                span_start_idx - 1 >= 0
                and (
                    cleaned[span_start_idx - 1].lower() in _ORDINAL_ADJACENT_NOUNS
                    or cleaned[span_start_idx - 1].lower() in _EXIT_CODE_PROSE_WORDS
                )
            ):
                i = span_end_idx + 1
                continue

            noun_idx = None
            for j in range(window_lo, window_hi + 1):
                if span_start_idx <= j <= span_end_idx:
                    continue
                if _is_noun(cleaned[j]):
                    noun_idx = j
                    break
                if (
                    cleaned[j].lower() in BIGRAM_NOUN_TAILS
                    and j - 1 >= 0
                    and cleaned[j - 1].lower() == BIGRAM_NOUN_HEAD
                ):
                    noun_idx = j
                    break

            if noun_idx is not None:
                lo_idx = min(span_start_idx, noun_idx)
                hi_idx = max(span_end_idx, noun_idx)
                start = toks[lo_idx][0]
                end = toks[hi_idx][1]
                hits.append(Hit(surface, lineno, line[start:end]))

            i = span_end_idx + 1

    return hits


def _expand_md_globs(repo_root: Path) -> list[str]:
    out: list[str] = []
    for pattern in MD_GLOB_SURFACES:
        if "*" in pattern:
            for p in sorted(repo_root.glob(pattern)):
                if p.is_file():
                    out.append(str(p.relative_to(repo_root)))
        else:
            p = repo_root / pattern
            if p.is_file():
                out.append(pattern)
    return out


def run_sweep(repo_root: Path) -> dict[str, list[Hit]]:
    results: dict[str, list[Hit]] = {}

    for relpath in _expand_md_globs(repo_root):
        p = repo_root / relpath
        text = p.read_text(encoding="utf-8")
        results[relpath] = scan_text(relpath, text)

    for relpath in PY_DOCSTRING_SURFACES:
        p = repo_root / relpath
        src = p.read_text(encoding="utf-8")
        doc = ast.get_docstring(ast.parse(src, filename=str(p)))
        surface_label = f"{relpath}#__doc__"
        if doc is None:
            results[surface_label] = []
            continue
        results[surface_label] = scan_text(surface_label, doc)

    return results


def print_report(results: dict[str, list[Hit]]) -> None:
    total = 0
    print("## Raw counts\n")
    for surface in sorted(results):
        count = len(results[surface])
        total += count
        print(f"{surface}: {count}")
    print(f"\nTOTAL (upper bound, unclassified): {total}\n")
    print("## Hit list\n")
    for surface in sorted(results):
        for hit in results[surface]:
            print(f"{hit.surface}:{hit.line}: {hit.text}")


def _selftest() -> int:
    ok = True

    # 1. spelled-out-form arm falsifiability
    fixture = "fifty-eight to seventy-two controls\neighty-six branches\nninety-four branches\n"
    hits = scan_text("fixture", fixture)
    if len(hits) != 3:
        print(f"FAIL: spelled-out arm expected 3 hits, got {len(hits)}: {[h.text for h in hits]}")
        ok = False
    else:
        print(f"PASS: spelled-out arm returns 3 hits: {[h.text for h in hits]}")

    # removing the spelled-out arm (simulate by only allowing digit atoms) -> 0
    digit_only_re = re.compile(r"\d{1,4}")

    def _is_num_atom_digit_only(clean: str) -> bool:
        return bool(re.fullmatch(digit_only_re, clean)) if clean else False

    global _is_num_atom
    _orig = _is_num_atom
    _is_num_atom = _is_num_atom_digit_only  # type: ignore[assignment]
    try:
        hits0 = scan_text("fixture", fixture)
    finally:
        _is_num_atom = _orig  # type: ignore[assignment]
    if len(hits0) != 0:
        print(f"FAIL: digit-only (spelled-out arm removed) expected 0 hits, got {len(hits0)}")
        ok = False
    else:
        print("PASS: digit-only (spelled-out arm removed) returns 0 hits")

    # 2. .py docstring arm falsifiability: check-selfaudit-scan.py must fire >=1
    repo_root = Path(sys.argv[sys.argv.index("--repo-root") + 1]) if "--repo-root" in sys.argv else Path.cwd()
    p = repo_root / "scripts/check-selfaudit-scan.py"
    src = p.read_text(encoding="utf-8")
    doc = ast.get_docstring(ast.parse(src, filename=str(p)))
    doc_hits = scan_text("scripts/check-selfaudit-scan.py#__doc__", doc or "")
    if len(doc_hits) < 1:
        print("FAIL: check-selfaudit-scan.py docstring arm returned 0 hits (under-detecting)")
        ok = False
    else:
        print(f"PASS: check-selfaudit-scan.py docstring arm returns {len(doc_hits)} hits (>=1)")

    return 0 if ok else 1


def main() -> int:
    if "--selftest" in sys.argv:
        return _selftest()

    if "--repo-root" in sys.argv:
        repo_root = Path(sys.argv[sys.argv.index("--repo-root") + 1]).resolve()
    else:
        repo_root = Path.cwd()

    results = run_sweep(repo_root)
    print_report(results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

</details>

<details>
<summary><code>conf13_classify.py</code> (verbatim, 179 lines)</summary>

```python
#!/usr/bin/env python3
"""CONF-13 baseline classifier — Task 2. Reads the Task-1 sweep's hits (via
conf13_sweep.run_sweep) and classifies every hit into exactly one of four
dispositions: structural, scanner-target, exempt, false-positive.

Measurement instrument only, not shipped. Deterministic, read-only.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import conf13_sweep as sweep  # noqa: E402

# ---------------------------------------------------------------------------
# Structural ranges: prose replaced by generated text under this phase's own
# plans (D-05 detail-page split for the two CI-gate tables; D-21-F for
# docs/TESTING.md's per-gate sections). Line numbers are 1-indexed, inclusive.
# ---------------------------------------------------------------------------
STRUCTURAL_RANGES: dict[str, list[tuple[int, int]]] = {
    "CLAUDE.md": [(150, 187)],                 # ### CI gates table (header+rows) + blank
    "docs/ARCHITECTURE.md": [(114, 189)],       # ## CI and pre-commit gate inventory table
    "docs/TESTING.md": [(12, 224)],             # D-21-F: per-gate ### sections folded
}

EXIT_CODE_RE = re.compile(r"^\s*[012]\s")
ORDINAL_LABEL_RE = re.compile(
    r"^(Criterion|Criteria|Phase|Check|Item|Arm|Row|Plan)\s+\d", re.IGNORECASE
)
ORDINAL_LABEL_TRAILING_RE = re.compile(
    r"(Criterion|Criteria|Phase|Check|Item|Arm|Row|Plan)\s+\d+\s*(,|\.|$|and\s)", re.IGNORECASE
)
VERSION_STAMP_RE = re.compile(r"version stamp", re.IGNORECASE)
BODY_BUDGET_RE = re.compile(r"\b644\b")
CALL_SITE_STUB_RE = re.compile(r"^sites:\s*\d")  # "sites: 1" continuation artifact
LEG_NUM_RE = re.compile(r"^\(leg \d", re.IGNORECASE)
HEADLINE_DELTA_RE = re.compile(
    r"\b(192|94|286|229|214|237|252|266)\b.*\brows?\b|\brows?\b.*\b(192|94|286|229|214|237|252|266)\b",
    re.IGNORECASE,
)


def _in_structural_range(surface: str, line: int) -> bool:
    for lo, hi in STRUCTURAL_RANGES.get(surface, []):
        if lo <= line <= hi:
            return True
    return False


def classify(hit: "sweep.Hit") -> tuple[str, str]:
    """Return (disposition, class_name)."""
    text = hit.text.strip()

    # 1. structural — prose this phase's own plans replace with generated text
    if _in_structural_range(hit.surface, hit.line):
        return "structural", "ci-gate-table-narrative" if "TESTING" not in hit.surface else "testing-per-gate-section"

    # 2. false-positive — ordinal/label references (identify WHICH item, not
    #    HOW MANY), exit-code lines, and adjacency-mistracking artifacts.
    if EXIT_CODE_RE.match(text) and ("check" in text.lower() or "control" in text.lower() or "fixture" in text.lower() or "stamp" in text.lower()):
        return "false-positive", "exit-code-line"
    if ORDINAL_LABEL_RE.match(text) or ORDINAL_LABEL_TRAILING_RE.search(text):
        return "false-positive", "ordinal-label-reference"
    if CALL_SITE_STUB_RE.match(text):
        return "false-positive", "line-wrap-continuation-artifact"
    if LEG_NUM_RE.match(text):
        return "false-positive", "ordinal-label-reference"
    if text.lower() in {"gate: the phase 3", "gate: asserts phase 5", "gate: governing record §2", "gate (governing record §2"}:
        return "false-positive", "ordinal-label-reference"
    if re.fullmatch(r"item \d,?", text, re.IGNORECASE) or re.fullmatch(r"§2 item", text, re.IGNORECASE):
        return "false-positive", "enumerated-list-marker"

    # 3. exempt — legitimate numbers that are not hand-maintained branch counts
    if VERSION_STAMP_RE.search(text):
        return "exempt", "version-stamp-count"
    if BODY_BUDGET_RE.search(text):
        return "exempt", "retired-body-budget"
    if re.search(r"\bplan \d{2}(-\d{2})?\b", text, re.IGNORECASE) and not re.search(
        r"\b(more|added|split)\b", text, re.IGNORECASE
    ):
        return "exempt", "plan-number-identifier"
    if HEADLINE_DELTA_RE.search(text):
        return "exempt", "headline-provenance-delta"
    if re.search(r"\bitems? each\b", text, re.IGNORECASE):
        return "false-positive", "ordinal-label-reference"

    # remaining known adjacency-mistrack false positives, named individually
    # because they are genuine mis-splits of a longer sentence rather than a
    # new class of exemption
    _NAMED_FALSE_POSITIVES = {
        "gate over **two**", "two assembly surfaces,", "row claimed, \"one",
        "10 plans", "1 plan", "plans 08-09,", "fixture (9)", "fixture and Phase 72",
    }
    if text in _NAMED_FALSE_POSITIVES:
        return "false-positive", "adjacency-mistrack"

    # 4. everything else is a scanner-target: a genuine hand-maintained count
    #    in prose that must be driven to 0 (or held there by the standing scanner)
    return "scanner-target", "hand-maintained-count"


def main() -> int:
    repo_root = Path(sys.argv[sys.argv.index("--repo-root") + 1]) if "--repo-root" in sys.argv else Path.cwd()
    results = sweep.run_sweep(repo_root)

    per_surface: dict[str, dict[str, int]] = {}
    all_hits: list[tuple[sweep.Hit, str, str]] = []
    for surface, hits in results.items():
        counts = {"structural": 0, "scanner-target": 0, "exempt": 0, "false-positive": 0}
        for h in hits:
            disp, cls = classify(h)
            counts[disp] += 1
            all_hits.append((h, disp, cls))
        per_surface[surface] = counts

    print("## Classification (per-surface)\n")
    print("| Surface | Raw | structural | scanner-target | exempt | false-positive | fp% |")
    print("|---|---|---|---|---|---|---|")
    total_raw = 0
    total_counts = {"structural": 0, "scanner-target": 0, "exempt": 0, "false-positive": 0}
    for surface in sorted(per_surface):
        c = per_surface[surface]
        raw = sum(c.values())
        total_raw += raw
        for k in total_counts:
            total_counts[k] += c[k]
        fp_pct = (c["false-positive"] / raw * 100) if raw else 0.0
        print(
            f"| {surface} | {raw} | {c['structural']} | {c['scanner-target']} | "
            f"{c['exempt']} | {c['false-positive']} | {fp_pct:.1f}% |"
        )
    print(
        f"| **TOTAL** | **{total_raw}** | {total_counts['structural']} | "
        f"{total_counts['scanner-target']} | {total_counts['exempt']} | "
        f"{total_counts['false-positive']} | "
        f"{total_counts['false-positive']/total_raw*100:.1f}% |"
    )

    print("\n## Exemption taxonomy classes used\n")
    exempt_class_counts: dict[str, int] = {}
    for h, disp, cls in all_hits:
        if disp == "exempt":
            exempt_class_counts[cls] = exempt_class_counts.get(cls, 0) + 1
    for cls, n in sorted(exempt_class_counts.items()):
        print(f"- {cls}: {n}")

    print("\n## False-positive classes used\n")
    fp_class_counts: dict[str, int] = {}
    for h, disp, cls in all_hits:
        if disp == "false-positive":
            fp_class_counts[cls] = fp_class_counts.get(cls, 0) + 1
    for cls, n in sorted(fp_class_counts.items()):
        print(f"- {cls}: {n}")

    print("\n## Full classified hit list\n")
    for h, disp, cls in all_hits:
        print(f"{h.surface}:{h.line}: [{disp}/{cls}] {h.text}")

    # Per-surface false-positive ceiling check (25%)
    over_ceiling = []
    for surface, c in per_surface.items():
        raw = sum(c.values())
        if raw == 0:
            continue
        pct = c["false-positive"] / raw
        if pct > 0.25:
            over_ceiling.append((surface, pct))
    if over_ceiling:
        print("\n## FALSE-POSITIVE CEILING EXCEEDED\n")
        for surface, pct in over_ceiling:
            print(f"- {surface}: {pct*100:.1f}%")
        return 1

    print("\nAll surfaces under 25% false-positive ceiling.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

</details>

---

## Raw counts

Run: `python3 conf13_sweep.py --repo-root <repo>`

| Surface | Raw hits |
|---|---|
| CLAUDE.md | 105 |
| docs/ARCHITECTURE.md | 62 |
| docs/COMPONENT-DIAGRAM.md | 2 |
| docs/DATA-FLOW.md | 2 |
| docs/MEASUREMENT-MAP.md | 1 |
| docs/README.md | 23 |
| docs/TESTING.md | 5 |
| docs/gates/*.md | 0 (directory does not exist yet — forward protection, per D-21-E) |
| scripts/check-act-limb.py#__doc__ | 1 |
| scripts/check-agent.py#__doc__ | 1 |
| scripts/check-conf-gate.py#__doc__ | 3 |
| scripts/check-description-budget.py#__doc__ | 0 |
| scripts/check-focused-parity.py#__doc__ | 2 |
| scripts/check-high-confidence-bound.py#__doc__ | 0 |
| scripts/check-install-collisions.py#__doc__ | 0 |
| scripts/check-links.py#__doc__ | 1 |
| scripts/check-loop-closure.py#__doc__ | 1 |
| scripts/check-provenance.py#__doc__ | 2 |
| scripts/check-quality-harness.py#__doc__ | 4 |
| scripts/check-registration.py#__doc__ | 1 |
| scripts/check-routing-battery.py#__doc__ | 0 |
| scripts/check-selfaudit-scan.py#__doc__ | 28 |
| scripts/check-step0-emulator.py#__doc__ | 4 |
| scripts/check-step0-live.py#__doc__ | 2 |
| scripts/check-traceability.py#__doc__ | 0 |
| scripts/check-trigger-collisions.py#__doc__ | 0 |
| scripts/check-version-stamps.py#__doc__ | 0 |
| scripts/sync-content.py#__doc__ | 0 |
| **TOTAL** | **250** |

**This raw total (250) is an upper bound containing known noise (ordinal labels that survived
both tightening passes, adjacency mis-splits) — it is NOT CONF-13's target figure.** Task 2
below classifies every one of these 250 hits.

**Falsifiability checks** (run via `--selftest`):

- Spelled-out-form arm: an in-memory fixture (`fifty-eight to seventy-two controls\neighty-six
  branches\nninety-four branches`) returns **3 hits**; removing the spelled-out arm (digit-only)
  returns **0 hits** — the arm is load-bearing, not decorative.
- `.py` docstring arm: `scripts/check-selfaudit-scan.py`'s module docstring returns **28 hits**
  (≥1) — CONF-13 names this file's docstring as a known instance; the arm is not under-detecting.

**Determinism:** the sweep was run twice back to back; output was byte-for-byte identical both
times.

## Classification

Run: `python3 conf13_classify.py --repo-root <repo>` (consumes `conf13_sweep.run_sweep()`'s
output directly, with no filtering step — every one of the 250 raw hits is classified exactly
once, by construction, so `unclassified=0` and `double-classified=0` hold structurally rather
than needing a separate join script).

| Surface | Raw | structural | scanner-target | exempt | false-positive | fp% |
|---|---|---|---|---|---|---|
| CLAUDE.md | 105 | 87 | 8 | 9 | 1 | 1.0% |
| docs/ARCHITECTURE.md | 62 | 59 | 2 | 1 | 0 | 0.0% |
| docs/COMPONENT-DIAGRAM.md | 2 | 0 | 2 | 0 | 0 | 0.0% |
| docs/DATA-FLOW.md | 2 | 0 | 2 | 0 | 0 | 0.0% |
| docs/MEASUREMENT-MAP.md | 1 | 0 | 1 | 0 | 0 | 0.0% |
| docs/README.md | 23 | 0 | 17 | 4 | 2 | 8.7% |
| docs/TESTING.md | 5 | 4 | 1 | 0 | 0 | 0.0% |
| scripts/check-act-limb.py#__doc__ | 1 | 0 | 1 | 0 | 0 | 0.0% |
| scripts/check-agent.py#__doc__ | 1 | 0 | 1 | 0 | 0 | 0.0% |
| scripts/check-conf-gate.py#__doc__ | 3 | 0 | 3 | 0 | 0 | 0.0% |
| scripts/check-description-budget.py#__doc__ | 0 | 0 | 0 | 0 | 0 | 0.0% |
| scripts/check-focused-parity.py#__doc__ | 2 | 0 | 2 | 0 | 0 | 0.0% |
| scripts/check-high-confidence-bound.py#__doc__ | 0 | 0 | 0 | 0 | 0 | 0.0% |
| scripts/check-install-collisions.py#__doc__ | 0 | 0 | 0 | 0 | 0 | 0.0% |
| scripts/check-links.py#__doc__ | 1 | 0 | 1 | 0 | 0 | 0.0% |
| scripts/check-loop-closure.py#__doc__ | 1 | 0 | 1 | 0 | 0 | 0.0% |
| scripts/check-provenance.py#__doc__ | 2 | 0 | 2 | 0 | 0 | 0.0% |
| scripts/check-quality-harness.py#__doc__ | 4 | 0 | 3 | 1 | 0 | 0.0% |
| scripts/check-registration.py#__doc__ | 1 | 0 | 1 | 0 | 0 | 0.0% |
| scripts/check-routing-battery.py#__doc__ | 0 | 0 | 0 | 0 | 0 | 0.0% |
| scripts/check-selfaudit-scan.py#__doc__ | 28 | 0 | 25 | 0 | 3 | 10.7% |
| scripts/check-step0-emulator.py#__doc__ | 4 | 0 | 4 | 0 | 0 | 0.0% |
| scripts/check-step0-live.py#__doc__ | 2 | 0 | 2 | 0 | 0 | 0.0% |
| scripts/check-traceability.py#__doc__ | 0 | 0 | 0 | 0 | 0 | 0.0% |
| scripts/check-trigger-collisions.py#__doc__ | 0 | 0 | 0 | 0 | 0 | 0.0% |
| scripts/check-version-stamps.py#__doc__ | 0 | 0 | 0 | 0 | 0 | 0.0% |
| scripts/sync-content.py#__doc__ | 0 | 0 | 0 | 0 | 0 | 0.0% |
| **TOTAL** | **250** | **150** | **79** | **15** | **6** | **2.4%** |

**Per-surface arithmetic (asserted per surface, not just in aggregate):** every row's
`structural + scanner-target + exempt + false-positive` sums to exactly that row's `Raw` column
(verified by the classifier's own construction — each hit is routed to exactly one of the four
buckets and every bucket is summed from the same `per_surface[surface]` dict the `Raw` column is
derived from). Aggregate: `150 + 79 + 15 + 6 = 250` = the raw total.

**False-positive ceiling:** the classifier's own `--repo-root` run exits `0` with
`All surfaces under 25% false-positive ceiling.` printed — every one of the 28 surfaces (27
candidate files/globs + `docs/gates/*.md`'s vacuous 0) is at or under 10.7% (the worst surface,
`scripts/check-selfaudit-scan.py#__doc__`, 3/28). This is after the two sweep-pattern
tightenings recorded above; no surface required a third pass.

## Exemption taxonomy

Every exemption class actually used, with its matching rule and written reason. A class with 0
hits is not listed (none were removed — all classes named below fired at least once).

| Class | Matching rule | Written reason | Hits |
|---|---|---|---|
| `version-stamp-count` | text contains `version stamp` | The 14 `shared/skills/*/SKILL.md` + `SKILL.meta.yml` + 2 manifests = 17 hand-maintained version stamps (VERSION-01's own invariant, `CLAUDE.md` § Key invariants) are legitimate, gate-enforced numbers — not a CONF-13 branch count. Both the "17 total" and "14 skill-file" sub-counts appear (`docs/ARCHITECTURE.md:96` distinguishes 14 skill stamps from the 17-stamp total, itself a real, VERSION-01-enforced fact, not drift). | 3 |
| `headline-provenance-delta` | digit(s) matching one of `192,94,286,229,214,237,252,266` adjacent to `row`/`rows` | These are `HEADLINE-LOCK`'s own remit (`scripts/check-traceability.py`) — the coverage-headline row-count's historical provenance narrative (`229 → 214 → 237 → 252 → 266 → 286`), asserted live off `build_matrix_rows()`, not hand-transcribed. CONF-13's own exempt list names "the coverage headline `192/94/0/286`... owned by HEADLINE-LOCK, out of this scanner's remit by construction"; this class extends that same reasoning to the intermediate deltas the identical narrative cites, since they document how HEADLINE-LOCK's own figure arrived at its current value, not a separate hand-maintained count. | 11 |
| `plan-number-identifier` | text matches `plan \d{2}(-\d{2})?` with no adjacent verb (`more`/`added`/`split`) | Plan numbers (`Plan 04 Task 1`) are identifiers, matching the exempt list's own named example (`13-10`) — they name which plan, not how many plans exist. | 1 |
| `retired-body-budget` | text contains `644` | The retired 644-line agent-body budget (TEARDOWN-01) — explicitly named in the exempt list. Measured 0 hits this run (the `docs/ARCHITECTURE.md:185` mention of `644` fell inside the structural CI-gate-table range and was classified `structural`, not `exempt` — recorded here for completeness even though it did not surface as a standalone exempt hit). |

**`maxTurns` 60, gate ids (`VAL-01`, `STEP0-08`), sha256 digests, and CommonMark heading depths
(1-6)** — all named in the exempt list — measured **0 hits** on this sweep's candidate surfaces.
Not listed as taxonomy rows per the plan's instruction ("an exemption class with 0 hits is
removed rather than left as dead weight"); recorded here once so their absence is a measured
fact, not an oversight.

## Target

**Per-surface `scanner-target → 0` figures** (the count that must reach 0, driven by hand in
plans `21-10`/`21-04`/`21-07`/`21-08` and then held at 0 by plan `21-09`'s standing scanner):

| Surface | scanner-target → 0 | exempt (scanner must permit) |
|---|---|---|
| CLAUDE.md | 8 | 9 |
| docs/ARCHITECTURE.md | 2 | 1 |
| docs/COMPONENT-DIAGRAM.md | 2 | 0 |
| docs/DATA-FLOW.md | 2 | 0 |
| docs/MEASUREMENT-MAP.md | 1 | 0 |
| docs/README.md | 17 | 4 |
| docs/TESTING.md | 1 | 0 |
| scripts/check-act-limb.py#__doc__ | 1 | 0 |
| scripts/check-agent.py#__doc__ | 1 | 0 |
| scripts/check-conf-gate.py#__doc__ | 3 | 0 |
| scripts/check-focused-parity.py#__doc__ | 2 | 0 |
| scripts/check-links.py#__doc__ | 1 | 0 |
| scripts/check-loop-closure.py#__doc__ | 1 | 0 |
| scripts/check-provenance.py#__doc__ | 2 | 0 |
| scripts/check-quality-harness.py#__doc__ | 3 | 1 |
| scripts/check-registration.py#__doc__ | 1 | 0 |
| scripts/check-selfaudit-scan.py#__doc__ | 25 | 0 |
| scripts/check-step0-emulator.py#__doc__ | 4 | 0 |
| scripts/check-step0-live.py#__doc__ | 2 | 0 |
| **Aggregate** | **79** | **15** |

**CONF-13's driveable target is `79` (`scanner-target → 0`), with `15` legitimate exempt hits
the standing scanner (plan `21-09`) must continue to permit.** This is not `9` (the roadmap's
admitted-partial figure), not `1015`, and not `76` (the two unfiltered readings this document
supersedes) — it is materially different from all three, as expected, and its derivation (raw
250 → 150 structural + 79 scanner-target + 15 exempt + 6 false-positive) is fully shown above
rather than asserted.

**Composition note, so later plans do not need to re-derive it:** of the 79 scanner-target hits,
25 (32%) sit in a single file's docstring — `scripts/check-selfaudit-scan.py`, CONF-13's own
named example — confirming the requirement's own instinct that this file carries a
disproportionate share. The remaining 54 are spread across the two CI-gate-table host files'
non-table prose (10), `docs/README.md`'s changelog-style narrative (17), the three peripheral
`docs/*.md` files (`COMPONENT-DIAGRAM.md` 2, `DATA-FLOW.md` 2, `MEASUREMENT-MAP.md` 1,
`TESTING.md` 1), and 17 further `.py` docstrings averaging under 2 hits each.

**150 of the 250 raw hits (60%) are `structural`** — they sit inside the CI-gate-table narrative
that plans `21-04`–`21-08` replace with generated `docs/gates/<ID>.md` links (D-05), or inside
`docs/TESTING.md`'s per-gate sections folded into a generated index (D-21-F). These reach 0 by
construction, with no scanner involvement, the moment those plans land — confirming
`21-RESEARCH.md`'s prediction that "a large fraction... will be eliminated structurally, for
free, the moment D-05's detail-page split lands."

## Disclosed bounds

**Detection is line-scoped, inherited from `HEADLINE-LOCK`'s own disclosed bound.** A
hand-maintained count hard-wrapped across two physical lines (the number on one line, its count
noun on the next) is invisible to this sweep. Not measured as occurring in this corpus today, but
not structurally excluded either — the same bound `HEADLINE-LOCK` itself carries and discloses.

**Containment proves a number is current, not that it describes the right thing (the D-06
bound).** This baseline — and the standing scanner plan `21-09` builds from it — can confirm a
literal number appears in prose; neither can confirm that number is attached to the correct noun,
or that it agrees with the artifact it claims to describe. A count that is internally consistent
but wrong (e.g. correctly stating "8 checks" for a function that actually has 9) passes this
sweep and would pass the standing scanner too.

**The exemption taxonomy is judgment, not a closed enumeration.** `21-CONTEXT.md`'s exempt list
names version stamps, the retired body budget, `maxTurns` 60, plan numbers, gate ids, sha256
digests, the coverage headline, CommonMark heading depths, and "ordinary English quantifiers with
no count-noun referent." This document additionally classified ordinal/label references
(`Criterion 4`, `Phase 3`) as **false-positive** rather than exempt (reasoning: the number
identifies which instance, not how many — "no count claim" per the plan's own false-positive
definition) and treated headline-provenance deltas as an **exempt** extension of the
already-named coverage-headline exemption (reasoning: same HEADLINE-LOCK-owned narrative, not a
separately hand-maintained figure). Both calls are documented with their reasoning above so a
later reviewer can re-derive or dispute them from the artifact, not from memory.

**The `.py` docstring surface set (`PY_DOCSTRING_SURFACES`, 20 scripts) is a snapshot of the
battery's current script-backed gate registrations.** If a future phase adds or removes a
script-backed gate, this list drifts from `scripts/check-firewall-battery.sh`'s live
registrations until manually re-derived — plan `21-09`'s standing scanner is expected to derive
this set programmatically (by parsing `check-firewall-battery.sh`'s `gate "<ID>" ...
"python3 scripts/<X>.py"` lines) rather than hand-list it a second time, closing this baseline's
own hand-transcription.

**`git status --porcelain` before and after both Task 1 and Task 2 showed only this plan's two
`.planning/` files** (`21-CONF13-BASELINE.md` itself and, after this plan completes,
`21-01-SUMMARY.md`) — no `scripts/`, `docs/`, or `CLAUDE.md` file was modified by this plan. The
sweep and classifier scripts themselves live only in the session scratchpad
(`/tmp/claude-*/scratchpad/`), never in `scripts/`, per the plan's own instruction that this is a
measurement instrument, not the standing scanner (plan `21-09`'s deliverable).

---

## Full classified hit list

The complete join of Task 1's 250 raw hits against Task 2's disposition — `[disposition/class]`
prefixes each line. Format: `relpath:line: [disposition/class] matched text`.

```
CLAUDE.md:7: [exempt/version-stamp-count] 17 version stamps
CLAUDE.md:37: [scanner-target/hand-maintained-count] (24 controls)
CLAUDE.md:39: [scanner-target/hand-maintained-count] (42 controls)
CLAUDE.md:134: [false-positive/adjacency-mistrack] two assembly surfaces,
CLAUDE.md:157: [structural/ci-gate-table-narrative] one missed stamp
CLAUDE.md:157: [structural/ci-gate-table-narrative] one missing its stamp
CLAUDE.md:158: [structural/ci-gate-table-narrative] gate over **two**
CLAUDE.md:158: [structural/ci-gate-table-narrative] 29 isolated control
CLAUDE.md:161: [structural/ci-gate-table-narrative] checks — 8
CLAUDE.md:161: [structural/ci-gate-table-narrative] 24 battery gates
CLAUDE.md:161: [structural/ci-gate-table-narrative] Checks 2
CLAUDE.md:161: [structural/ci-gate-table-narrative] Checks 2 and 8
CLAUDE.md:161: [structural/ci-gate-table-narrative] 8: Check
CLAUDE.md:163: [structural/ci-gate-table-narrative] 7 SEMGATE named assertions
CLAUDE.md:165: [structural/ci-gate-table-narrative] five named current-fact surfaces
CLAUDE.md:165: [structural/ci-gate-table-narrative] literal itself: one
CLAUDE.md:165: [structural/ci-gate-table-narrative] eight named arms,
CLAUDE.md:165: [structural/ci-gate-table-narrative] four cases
CLAUDE.md:165: [structural/ci-gate-table-narrative] two whole-file cases
CLAUDE.md:165: [structural/ci-gate-table-narrative] two ARROW arms,
CLAUDE.md:165: [structural/ci-gate-table-narrative] arms, one
CLAUDE.md:165: [structural/ci-gate-table-narrative] site (`(m)`'s three
CLAUDE.md:167: [structural/ci-gate-table-narrative] six separate legs:
CLAUDE.md:167: [structural/ci-gate-table-narrative] legs: (1)
CLAUDE.md:167: [structural/ci-gate-table-narrative] thirteen chain-family fixtures
CLAUDE.md:167: [structural/ci-gate-table-narrative] (6 call sites:
CLAUDE.md:167: [structural/ci-gate-table-narrative] sites: 1
CLAUDE.md:167: [structural/ci-gate-table-narrative] (6 call sites:
CLAUDE.md:167: [structural/ci-gate-table-narrative] sites: 1
CLAUDE.md:167: [structural/ci-gate-table-narrative] (5 call sites:
CLAUDE.md:167: [structural/ci-gate-table-narrative] sites: 1
CLAUDE.md:167: [structural/ci-gate-table-narrative] (2) cross-surface literal
CLAUDE.md:167: [structural/ci-gate-table-narrative] literal reconciliation — twelve
CLAUDE.md:167: [structural/ci-gate-table-narrative] surface among all four
CLAUDE.md:167: [structural/ci-gate-table-narrative] two contract surfaces
CLAUDE.md:167: [structural/ci-gate-table-narrative] surfaces declare all twelve);
CLAUDE.md:167: [structural/ci-gate-table-narrative] four registered surfaces
CLAUDE.md:167: [structural/ci-gate-table-narrative] three entries
CLAUDE.md:167: [structural/ci-gate-table-narrative] (5) **worked-example conformance** (plan
CLAUDE.md:167: [structural/ci-gate-table-narrative] literals on all three
CLAUDE.md:167: [structural/ci-gate-table-narrative] nine `R-CLAIM-*` fixtures
CLAUDE.md:167: [structural/ci-gate-table-narrative] fixtures pinning R11's three
CLAUDE.md:167: [structural/ci-gate-table-narrative] 6 absorbed the Gate
CLAUDE.md:167: [structural/ci-gate-table-narrative] three independently-neutralization-tested anti-vacuity arms,
CLAUDE.md:167: [structural/ci-gate-table-narrative] arms, plus two
CLAUDE.md:167: [structural/ci-gate-table-narrative] one row
CLAUDE.md:167: [structural/ci-gate-table-narrative] Eleven mutations
CLAUDE.md:167: [structural/ci-gate-table-narrative] one arm.
CLAUDE.md:167: [structural/ci-gate-table-narrative] four canonical surfaces
CLAUDE.md:167: [structural/ci-gate-table-narrative] arm for those five.
CLAUDE.md:167: [structural/ci-gate-table-narrative] surface (three
CLAUDE.md:167: [structural/ci-gate-table-narrative] check requires only two
CLAUDE.md:167: [structural/ci-gate-table-narrative] pins — three,
CLAUDE.md:167: [structural/ci-gate-table-narrative] two new pins
CLAUDE.md:167: [structural/ci-gate-table-narrative] four lettered controls
CLAUDE.md:168: [structural/ci-gate-table-narrative] fixtures for all 16
CLAUDE.md:168: [structural/ci-gate-table-narrative] branches (58
CLAUDE.md:171: [structural/ci-gate-table-narrative] one hundred clause-level named branches
CLAUDE.md:171: [structural/ci-gate-table-narrative] (plan 15-06 split thirty-one
CLAUDE.md:171: [structural/ci-gate-table-narrative] branches to fifty-eight
CLAUDE.md:171: [structural/ci-gate-table-narrative] one arm
CLAUDE.md:171: [structural/ci-gate-table-narrative] plan 15-07 added fourteen
CLAUDE.md:171: [structural/ci-gate-table-narrative] Criteria 4 and 6
CLAUDE.md:171: [structural/ci-gate-table-narrative] six branches
CLAUDE.md:171: [structural/ci-gate-table-narrative] column for (`Rubric-9`/`Rubric-10`, four
CLAUDE.md:171: [structural/ci-gate-table-narrative] two branches),
CLAUDE.md:171: [structural/ci-gate-table-narrative] two branches);
CLAUDE.md:171: [structural/ci-gate-table-narrative] plan 15-08 added fourteen
CLAUDE.md:171: [structural/ci-gate-table-narrative] four single-surface arms
CLAUDE.md:171: [structural/ci-gate-table-narrative] plan 15-09 added one
CLAUDE.md:171: [structural/ci-gate-table-narrative] plan 15-11 added seven
CLAUDE.md:171: [structural/ci-gate-table-narrative] two per-surface arms)
CLAUDE.md:171: [structural/ci-gate-table-narrative] "Criteria 4 and 6
CLAUDE.md:171: [structural/ci-gate-table-narrative] plan 15-12 added six
CLAUDE.md:171: [structural/ci-gate-table-narrative] two hand-written `_BAND_SOUND`-only ids
CLAUDE.md:171: [structural/ci-gate-table-narrative] ids with eight
CLAUDE.md:171: [structural/ci-gate-table-narrative] one literal
CLAUDE.md:171: [structural/ci-gate-table-narrative] surface in one
CLAUDE.md:171: [structural/ci-gate-table-narrative] four legs
CLAUDE.md:171: [structural/ci-gate-table-narrative] two synthetic isolation arms
CLAUDE.md:171: [structural/ci-gate-table-narrative] row claimed, "one
CLAUDE.md:171: [structural/ci-gate-table-narrative] (plan 15-12). Eight
CLAUDE.md:171: [structural/ci-gate-table-narrative] row named only five
CLAUDE.md:171: [structural/ci-gate-table-narrative] seven pre-15-11 arms,
CLAUDE.md:171: [structural/ci-gate-table-narrative] arms, omitting Rubric-2's two.
CLAUDE.md:171: [structural/ci-gate-table-narrative] Criterion 4 or 6
CLAUDE.md:173: [structural/ci-gate-table-narrative] 24 controls
CLAUDE.md:174: [structural/ci-gate-table-narrative] seven enforcement call sites
CLAUDE.md:174: [structural/ci-gate-table-narrative] four internal predicates (plan
CLAUDE.md:174: [structural/ci-gate-table-narrative] three mutations
CLAUDE.md:186: [structural/ci-gate-table-narrative] two inline checks
CLAUDE.md:190: [scanner-target/hand-maintained-count] Two gates
CLAUDE.md:192: [scanner-target/hand-maintained-count] 1. The **sync-drift gate**
CLAUDE.md:252: [exempt/headline-provenance-delta] 229 → 214 rows;
CLAUDE.md:252: [exempt/headline-provenance-delta] 214 rows;
CLAUDE.md:252: [scanner-target/hand-maintained-count] rows; the 23
CLAUDE.md:253: [exempt/headline-provenance-delta] 214 → 237 rows;
CLAUDE.md:253: [exempt/headline-provenance-delta] 237 rows;
CLAUDE.md:253: [scanner-target/hand-maintained-count] rows; the 15
CLAUDE.md:254: [exempt/headline-provenance-delta] 237 → 252 rows;
CLAUDE.md:254: [exempt/headline-provenance-delta] 252 rows;
CLAUDE.md:254: [scanner-target/hand-maintained-count] rows; the 14
CLAUDE.md:255: [exempt/headline-provenance-delta] (row count 252
CLAUDE.md:258: [exempt/headline-provenance-delta] row count 266
CLAUDE.md:339: [scanner-target/hand-maintained-count] surface now contributes 16
docs/ARCHITECTURE.md:82: [scanner-target/hand-maintained-count] one entry
docs/ARCHITECTURE.md:96: [exempt/version-stamp-count] 14 version stamps
docs/ARCHITECTURE.md:96: [scanner-target/hand-maintained-count] stamps rather than 13.
docs/ARCHITECTURE.md:121: [structural/ci-gate-table-narrative] Gates run on three
docs/ARCHITECTURE.md:124: [structural/ci-gate-table-narrative] 22 CI gates
docs/ARCHITECTURE.md:126: [structural/ci-gate-table-narrative] one registered gate
docs/ARCHITECTURE.md:126: [structural/ci-gate-table-narrative] job, plus the two
docs/ARCHITECTURE.md:136: [structural/ci-gate-table-narrative] 17 hand-maintained version stamps
docs/ARCHITECTURE.md:137: [structural/ci-gate-table-narrative] gate over two
docs/ARCHITECTURE.md:145: [structural/ci-gate-table-narrative] five current-fact surfaces
docs/ARCHITECTURE.md:145: [structural/ci-gate-table-narrative] literal itself (one
docs/ARCHITECTURE.md:145: [structural/ci-gate-table-narrative] four cases,
docs/ARCHITECTURE.md:145: [structural/ci-gate-table-narrative] two whole-file cases
docs/ARCHITECTURE.md:145: [structural/ci-gate-table-narrative] two arrow arms
docs/ARCHITECTURE.md:145: [structural/ci-gate-table-narrative] arms (one
docs/ARCHITECTURE.md:146: [structural/ci-gate-table-narrative] six separate legs:
docs/ARCHITECTURE.md:146: [structural/ci-gate-table-narrative] legs: (1)
docs/ARCHITECTURE.md:146: [structural/ci-gate-table-narrative] thirteen chain-family fixtures
docs/ARCHITECTURE.md:146: [structural/ci-gate-table-narrative] (6 call sites:
docs/ARCHITECTURE.md:146: [structural/ci-gate-table-narrative] sites: 1
docs/ARCHITECTURE.md:146: [structural/ci-gate-table-narrative] (6 call sites:
docs/ARCHITECTURE.md:146: [structural/ci-gate-table-narrative] sites: 1
docs/ARCHITECTURE.md:146: [structural/ci-gate-table-narrative] (5 call sites:
docs/ARCHITECTURE.md:146: [structural/ci-gate-table-narrative] sites: 1
docs/ARCHITECTURE.md:146: [structural/ci-gate-table-narrative] (2) cross-surface literal
docs/ARCHITECTURE.md:146: [structural/ci-gate-table-narrative] literal reconciliation — twelve
docs/ARCHITECTURE.md:146: [structural/ci-gate-table-narrative] surface among all four
docs/ARCHITECTURE.md:146: [structural/ci-gate-table-narrative] two contract surfaces
docs/ARCHITECTURE.md:146: [structural/ci-gate-table-narrative] surfaces declare all twelve);
docs/ARCHITECTURE.md:146: [structural/ci-gate-table-narrative] four registered surfaces
docs/ARCHITECTURE.md:146: [structural/ci-gate-table-narrative] three entries
docs/ARCHITECTURE.md:146: [structural/ci-gate-table-narrative] (5) **worked-example conformance** (plan
docs/ARCHITECTURE.md:146: [structural/ci-gate-table-narrative] literals on all three
docs/ARCHITECTURE.md:146: [structural/ci-gate-table-narrative] nine `R-CLAIM-*` fixtures
docs/ARCHITECTURE.md:146: [structural/ci-gate-table-narrative] fixtures pinning R11's three
docs/ARCHITECTURE.md:146: [structural/ci-gate-table-narrative] 6 absorbed the Gate
docs/ARCHITECTURE.md:146: [structural/ci-gate-table-narrative] three independently-neutralization-tested anti-vacuity arms,
docs/ARCHITECTURE.md:146: [structural/ci-gate-table-narrative] arms, plus two
docs/ARCHITECTURE.md:146: [structural/ci-gate-table-narrative] one row
docs/ARCHITECTURE.md:146: [structural/ci-gate-table-narrative] Eleven mutations
docs/ARCHITECTURE.md:146: [structural/ci-gate-table-narrative] one arm.
docs/ARCHITECTURE.md:146: [structural/ci-gate-table-narrative] four canonical surfaces
docs/ARCHITECTURE.md:146: [structural/ci-gate-table-narrative] arm for those five.
docs/ARCHITECTURE.md:146: [structural/ci-gate-table-narrative] surface (three
docs/ARCHITECTURE.md:146: [structural/ci-gate-table-narrative] check requires only two
docs/ARCHITECTURE.md:147: [structural/ci-gate-table-narrative] fixtures for all 16
docs/ARCHITECTURE.md:147: [structural/ci-gate-table-narrative] branches (58
docs/ARCHITECTURE.md:150: [structural/ci-gate-table-narrative] one hundred clause-level named branches
docs/ARCHITECTURE.md:150: [structural/ci-gate-table-narrative] branches (72
docs/ARCHITECTURE.md:150: [structural/ci-gate-table-narrative] plan 15-07; 72
docs/ARCHITECTURE.md:150: [structural/ci-gate-table-narrative] 86 at plan
docs/ARCHITECTURE.md:150: [structural/ci-gate-table-narrative] 87 at plan
docs/ARCHITECTURE.md:150: [structural/ci-gate-table-narrative] 94 at plan
docs/ARCHITECTURE.md:150: [structural/ci-gate-table-narrative] 100 at plan
docs/ARCHITECTURE.md:150: [structural/ci-gate-table-narrative] two hand-written ids
docs/ARCHITECTURE.md:150: [structural/ci-gate-table-narrative] ids with eight
docs/ARCHITECTURE.md:150: [structural/ci-gate-table-narrative] "one id
docs/ARCHITECTURE.md:150: [structural/ci-gate-table-narrative] seven arms
docs/ARCHITECTURE.md:153: [structural/ci-gate-table-narrative] arm whose four
docs/ARCHITECTURE.md:175: [structural/ci-gate-table-narrative] **Two gates
docs/ARCHITECTURE.md:179: [structural/ci-gate-table-narrative] two unrelated checks.
docs/ARCHITECTURE.md:185: [structural/ci-gate-table-narrative] gate at all; 644
docs/TESTING.md:124: [structural/testing-per-gate-section] two fixture
docs/TESTING.md:166: [structural/testing-per-gate-section] gate count from 15 to 16.
docs/TESTING.md:187: [structural/testing-per-gate-section] Two gates
docs/TESTING.md:219: [structural/testing-per-gate-section] five labelled surfaces:
docs/TESTING.md:245: [scanner-target/hand-maintained-count] literal `== 4`
docs/MEASUREMENT-MAP.md:52: [scanner-target/hand-maintained-count] assertion — one
docs/COMPONENT-DIAGRAM.md:66: [scanner-target/hand-maintained-count] 12 CI gates,
docs/COMPONENT-DIAGRAM.md:66: [scanner-target/hand-maintained-count] two pre-commit gates)
docs/DATA-FLOW.md:51: [scanner-target/hand-maintained-count] 4 — Gates
docs/DATA-FLOW.md:53: [scanner-target/hand-maintained-count] two pre-commit gates
docs/README.md:26: [exempt/headline-provenance-delta] row count 229
docs/README.md:29: [exempt/headline-provenance-delta] row count 237
docs/README.md:30: [exempt/headline-provenance-delta] row count 252
docs/README.md:36: [scanner-target/hand-maintained-count] 7 docs/metadata items),
docs/README.md:36: [scanner-target/hand-maintained-count] 19 not-approved items),
docs/README.md:42: [scanner-target/hand-maintained-count] 612 to 590 lines, the surface
docs/README.md:56: [scanner-target/hand-maintained-count] five entries
docs/README.md:56: [scanner-target/hand-maintained-count] five live entries
docs/README.md:56: [scanner-target/hand-maintained-count] five live entries
docs/README.md:56: [scanner-target/hand-maintained-count] **one** entry
docs/README.md:58: [scanner-target/hand-maintained-count] **0 items
docs/README.md:58: [false-positive/ordinal-label-reference] items each** for two
docs/README.md:58: [scanner-target/hand-maintained-count] sixteen green gates
docs/README.md:58: [scanner-target/hand-maintained-count] 6 live rows
docs/README.md:58: [scanner-target/hand-maintained-count] rows to 0
docs/README.md:61: [scanner-target/hand-maintained-count] 16 gates
docs/README.md:102: [scanner-target/hand-maintained-count] 16 surfaces
docs/README.md:106: [false-positive/adjacency-mistrack] fixture (9)
docs/README.md:107: [scanner-target/hand-maintained-count] 13 live matrix rows'
docs/README.md:135: [scanner-target/hand-maintained-count] gate and the two
docs/README.md:191: [scanner-target/hand-maintained-count] three new offline gates
docs/README.md:192: [exempt/version-stamp-count] 17 version stamps
docs/README.md:207: [scanner-target/hand-maintained-count] 13 rows
scripts/check-step0-live.py#__doc__:27: [scanner-target/hand-maintained-count] fixture (default: 5)
scripts/check-step0-live.py#__doc__:28: [scanner-target/hand-maintained-count] row PASS (default: 3)
scripts/check-step0-emulator.py#__doc__:17: [scanner-target/hand-maintained-count] TWO fixture
scripts/check-step0-emulator.py#__doc__:18: [scanner-target/hand-maintained-count] 1. Fault-injection fixtures
scripts/check-step0-emulator.py#__doc__:18: [scanner-target/hand-maintained-count] fixtures (D-05) — four
scripts/check-step0-emulator.py#__doc__:20: [scanner-target/hand-maintained-count] 2. Classification fixtures
scripts/check-links.py#__doc__:14: [scanner-target/hand-maintained-count] two newly-extended scan surfaces
scripts/check-registration.py#__doc__:10: [scanner-target/hand-maintained-count] 29 named, decision-traceable controls
scripts/check-agent.py#__doc__:11: [scanner-target/hand-maintained-count] three inline malformed fixtures
scripts/check-quality-harness.py#__doc__:20: [exempt/plan-number-identifier] **Plan 04 Task 1
scripts/check-quality-harness.py#__doc__:61: [scanner-target/hand-maintained-count] [ID]        Dispatch exactly one
scripts/check-quality-harness.py#__doc__:66: [scanner-target/hand-maintained-count] one tabulated row.
scripts/check-quality-harness.py#__doc__:66: [scanner-target/hand-maintained-count] row. Dispatches exactly one
scripts/check-provenance.py#__doc__:28: [scanner-target/hand-maintained-count] 2. The literal
scripts/check-provenance.py#__doc__:35: [scanner-target/hand-maintained-count] 4. PROV-04's no-network control
scripts/check-act-limb.py#__doc__:51: [scanner-target/hand-maintained-count] 2 item
scripts/check-loop-closure.py#__doc__:35: [scanner-target/hand-maintained-count] gate reads four
scripts/check-focused-parity.py#__doc__:15: [scanner-target/hand-maintained-count] check between the two
scripts/check-focused-parity.py#__doc__:67: [scanner-target/hand-maintained-count] 2 item
scripts/check-selfaudit-scan.py#__doc__:24: [scanner-target/hand-maintained-count] two tables. This gate
scripts/check-selfaudit-scan.py#__doc__:34: [scanner-target/hand-maintained-count] surfaces run TWO
scripts/check-selfaudit-scan.py#__doc__:42: [scanner-target/hand-maintained-count] 17 stamps
scripts/check-selfaudit-scan.py#__doc__:90: [scanner-target/hand-maintained-count] 2 item
scripts/check-selfaudit-scan.py#__doc__:97: [scanner-target/hand-maintained-count] two surfaces
scripts/check-selfaudit-scan.py#__doc__:104: [false-positive/ordinal-label-reference] Criteria 4 and 6
scripts/check-selfaudit-scan.py#__doc__:132: [false-positive/ordinal-label-reference] Criteria 4 and 6,
scripts/check-selfaudit-scan.py#__doc__:156: [false-positive/ordinal-label-reference] Criterion 4 or 6
scripts/check-selfaudit-scan.py#__doc__:170: [scanner-target/hand-maintained-count] eight arms
scripts/check-selfaudit-scan.py#__doc__:178: [scanner-target/hand-maintained-count] literal via the `-1`
scripts/check-selfaudit-scan.py#__doc__:187: [scanner-target/hand-maintained-count] four assertions
scripts/check-selfaudit-scan.py#__doc__:191: [scanner-target/hand-maintained-count] (9) **What plan
scripts/check-selfaudit-scan.py#__doc__:210: [scanner-target/hand-maintained-count] literals themselves — two
scripts/check-selfaudit-scan.py#__doc__:213: [scanner-target/hand-maintained-count] (11) **What plan
scripts/check-selfaudit-scan.py#__doc__:216: [scanner-target/hand-maintained-count] (eight ids
scripts/check-selfaudit-scan.py#__doc__:221: [scanner-target/hand-maintained-count] 0 ("All 94 branches
scripts/check-selfaudit-scan.py#__doc__:221: [scanner-target/hand-maintained-count] 94 branches
scripts/check-selfaudit-scan.py#__doc__:222: [scanner-target/hand-maintained-count] six now-uncovered ids.
scripts/check-selfaudit-scan.py#__doc__:224: [scanner-target/hand-maintained-count] literal (nine
scripts/check-selfaudit-scan.py#__doc__:227: [scanner-target/hand-maintained-count] one hand-written arm
scripts/check-selfaudit-scan.py#__doc__:228: [scanner-target/hand-maintained-count] one arm
scripts/check-selfaudit-scan.py#__doc__:238: [scanner-target/hand-maintained-count] (12) **What plan
scripts/check-selfaudit-scan.py#__doc__:273: [scanner-target/hand-maintained-count] one row
scripts/check-selfaudit-scan.py#__doc__:275: [scanner-target/hand-maintained-count] one row
scripts/check-selfaudit-scan.py#__doc__:275: [scanner-target/hand-maintained-count] fixture actually contains, 7
scripts/check-selfaudit-scan.py#__doc__:280: [scanner-target/hand-maintained-count] 17 table data rows**
scripts/check-selfaudit-scan.py#__doc__:293: [scanner-target/hand-maintained-count] rows (17
scripts/check-selfaudit-scan.py#__doc__:293: [scanner-target/hand-maintained-count] rows (17 / 44)
scripts/check-conf-gate.py#__doc__:1: [scanner-target/hand-maintained-count] gate over the fourteen
scripts/check-conf-gate.py#__doc__:26: [scanner-target/hand-maintained-count] surface for the two
scripts/check-conf-gate.py#__doc__:44: [scanner-target/hand-maintained-count] two arms
```

---

*Phase: 21-generate-the-claim-surface*
*Plan: 21-01*
*Baseline measured: 2026-09-06*
