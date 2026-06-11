# Routing Battery Baseline — v4.3 (Merged: Boundary + Focused-Output)

**Recorded:** 2026-06-11T16:20:36Z–16:58:00Z (45 live `claude` invocations: 9 prompts × 5 repeats; claude 2.1.170)
**Script version:** `scripts/check-routing-battery.py` (commit `1969c07`)
**Core version:** `scripts/_battery_core.py` (commit `1969c07`)
**Fixture version:** `tests/routing-battery-catalog.md` (commit `1969c07`)
**Agent version:** `first-principles/agents/first-principles.md` (commit `1969c07`)
**Run flags:** `--repeat 5 --min-pass 3 --boundary-p-threshold 2 --focused-p-threshold 4 --focused-n-threshold 1`
**Run cwd:** `/tmp` (out-of-repo — see Methodology notes)
**Baseline verdict:** BATTERY: PASS
**Summary:** boundary P 2/2 | N 2/2; focused P 4/4 | N 1/1; overall PASS
**Pre-run masked-threshold audit:** clean — see `.planning/notes/audit-masked-thresholds-v4.3.md`

---

## Per-prompt results

| #     | Expected Boundary | Expected Output    | Boundary K/N | Focused K/N | Both-Match Verdict |
|-------|-------------------|--------------------|--------------|-------------|--------------------|
| B-P12 | none-or-other     | n-a                | 5/5          | n-a         | PASS               |
| B-P24 | none-or-other     | n-a                | 5/5          | n-a         | PASS               |
| B-N1  | none-or-other     | n-a                | 5/5          | n-a         | PASS               |
| B-N2  | none-or-other     | n-a                | 5/5          | n-a         | PASS               |
| F-P12 | n-a               | focused-pre-mortem | n-a          | 4/5 PASS    | PASS               |
| F-P24 | n-a               | focused-inversion  | n-a          | 5/5 PASS    | PASS               |
| F-P25 | n-a               | focused-pre-mortem | n-a          | 5/5 PASS    | PASS               |
| F-P26 | n-a               | focused-pre-mortem | n-a          | 5/5 PASS    | PASS               |
| F-N1  | n-a               | NOT-any-focused    | n-a          | 5/5 PASS    | PASS               |

### Verdict-cell schema

Each row's K/N cell uses the falsifiable `<n>/N PASS|FAIL` format (per the Plan 46-04 acceptance
criteria, carried forward from `tests/focused-output-baseline-v4.2.md`). A row that says
`<n>/5 FAIL` would NOT satisfy the gate — gates are unfalsifiable when the verifier checks for
substring presence only. The boundary K/N cells use plain `K/N` (no PASS/FAIL suffix) because the
boundary signal did not exhibit stochastic noise in v4.2 (all 5/5); the focused K/N cells use the
full falsifiable `<n>/5 PASS` form because F-P12/F-P24 landed at the K-of-N floor (3/5) in v4.2.

---

## How this baseline was produced

```bash
REPO=/home/chrisdavidson/programming/first-principles-skills
OUT_DIR=/tmp/routing-battery-v4.3-$(date -u +%Y%m%dT%H%M%SZ)
cd /tmp && python3 "$REPO/scripts/check-routing-battery.py" \
  --catalog "$REPO/tests/routing-battery-catalog.md" \
  --plugin-dir "$REPO/first-principles" \
  --repeat 5 --min-pass 3 \
  --boundary-p-threshold 2 \
  --focused-p-threshold 4 --focused-n-threshold 1 \
  --out "$OUT_DIR"
```

**Run date:** 2026-06-11T16:20:36Z–16:58:00Z

**Output directory:** `/tmp/routing-battery-v4.3-20260611T162036Z` (transient). Contains per-prompt
`<id>-run{1..5}.jsonl` raw stream-json captures, `scores-boundary.tsv`, `scores-focused.tsv`,
and `verdict.txt`. Raw artifacts not committed.

---

## Methodology notes

**Why this baseline runs from `/tmp` (not project root).** When run from the project root, the
orchestrator enriches vague or oblique prompts with `.planning/` context — causing it to run
a meta-analysis on the project itself rather than the user-supplied content. Running from `/tmp`
eliminates this project-context enrichment surface. The `--plugin-dir` absolute path ensures the
plugin is still loaded correctly from `/tmp` (without this flag, the script cannot find the plugin
and exits with code 2).

**Why `--plugin-dir` must be an absolute path.** The script is invoked from `/tmp`; a relative
`./first-principles` path would resolve against `/tmp`, not the project root. Always pass an
absolute path from the project root.

**Why the K-of-N tolerance is set at min-pass=3.** Phase 45 and Phase 46 baselines both document
±3 P-prompt swing within the same session (see `routing-battery-noise` memory entry). `--repeat 5
--min-pass 3` encodes this tolerance: a row is PASS if ≥ 3 of 5 runs classify correctly, accepting
up to 2 stochastic misses per row.

**Single cwd for the merged battery.** The v4.2 milestone ran two separate batteries with distinct
cwds: the boundary battery from project root and the focused battery from `/tmp`. The v4.3 merged
battery captures each prompt once in a single run. Because focused-output prompts require `/tmp` to
avoid `.planning/` enrichment, and the boundary signal is cwd-insensitive, the single v4.3 run uses
`/tmp` as the unified cwd — collapsing the v4.2 two-cwd split (D-01).

---

## Lineage

This baseline supersedes BOTH:
- `tests/sub-skill-routing-baseline-v4.2.md` (Phase 66 boundary discipline baseline)
- `tests/focused-output-baseline-v4.2.md` (Phase 66 focused-output FOCUS-01/FU-21 baseline)

**What changed:** The two separate batteries (`check-sub-skill-routing.py` and
`check-focused-output.py`) have been merged into a single battery (`check-routing-battery.py`)
with a single merged catalog (`tests/routing-battery-catalog.md`) that carries both expectation
columns per prompt. Each prompt is captured once; both signals are scored from the same `.jsonl`
capture stream; the per-prompt verdict is both-match (requiring both signals to pass). The v4.3
baseline captures this as a single file with a 9-row merged table (4 boundary + 5 focused),
replacing the two 4-row and 5-row tables in the v4.2 baseline pair.

**Detector provenance:** The focused-output Signal B detector fix was committed at `151b197`
(Phase 66-03). This merged baseline inherits that fix as its detector provenance baseline. The
`fu21-fixture-contradiction-diagnosis` evidence chain (`.planning/notes/fu21-fixture-contradiction-diagnosis.md`)
documents the architectural root cause (all sub-skills `disable-model-invocation: true`) that
the fixture corrections in Phase 65 addressed.

The v4.2 baseline files remain on disk as lineage (D-03/D-05); they are not deleted.

---

## Scores

### Boundary scores (scores-boundary.tsv)

```
id	run	expected	actual	match
B-P12	1	none-or-other	none-or-other	1
B-P12	2	none-or-other	none-or-other	1
B-P12	3	none-or-other	none-or-other	1
B-P12	4	none-or-other	none-or-other	1
B-P12	5	none-or-other	none-or-other	1
B-P24	1	none-or-other	none-or-other	1
B-P24	2	none-or-other	none-or-other	1
B-P24	3	none-or-other	none-or-other	1
B-P24	4	none-or-other	none-or-other	1
B-P24	5	none-or-other	none-or-other	1
F-P12	1	n-a	none-or-other	1
F-P12	2	n-a	none-or-other	1
F-P12	3	n-a	none-or-other	1
F-P12	4	n-a	none-or-other	1
F-P12	5	n-a	none-or-other	1
F-P24	1	n-a	none-or-other	1
F-P24	2	n-a	none-or-other	1
F-P24	3	n-a	none-or-other	1
F-P24	4	n-a	none-or-other	1
F-P24	5	n-a	none-or-other	1
F-P25	1	n-a	none-or-other	1
F-P25	2	n-a	none-or-other	1
F-P25	3	n-a	none-or-other	1
F-P25	4	n-a	none-or-other	1
F-P25	5	n-a	none-or-other	1
F-P26	1	n-a	none-or-other	1
F-P26	2	n-a	none-or-other	1
F-P26	3	n-a	none-or-other	1
F-P26	4	n-a	none-or-other	1
F-P26	5	n-a	none-or-other	1
B-N1	1	none-or-other	none-or-other	1
B-N1	2	none-or-other	none-or-other	1
B-N1	3	none-or-other	none-or-other	1
B-N1	4	none-or-other	none-or-other	1
B-N1	5	none-or-other	none-or-other	1
B-N2	1	none-or-other	none-or-other	1
B-N2	2	none-or-other	none-or-other	1
B-N2	3	none-or-other	none-or-other	1
B-N2	4	none-or-other	none-or-other	1
B-N2	5	none-or-other	none-or-other	1
F-N1	1	n-a	none-or-other	1
F-N1	2	n-a	none-or-other	1
F-N1	3	n-a	none-or-other	1
F-N1	4	n-a	none-or-other	1
F-N1	5	n-a	none-or-other	1
```

### Focused scores (scores-focused.tsv)

```
id	run	expected	actual	match
B-P12	1	n-a	none	1
B-P12	2	n-a	none	1
B-P12	3	n-a	none	1
B-P12	4	n-a	none	1
B-P12	5	n-a	none	1
B-P24	1	n-a	none	1
B-P24	2	n-a	none	1
B-P24	3	n-a	none	1
B-P24	4	n-a	none	1
B-P24	5	n-a	none	1
F-P12	1	focused-pre-mortem	none	0
F-P12	2	focused-pre-mortem	focused-pre-mortem	1
F-P12	3	focused-pre-mortem	focused-pre-mortem	1
F-P12	4	focused-pre-mortem	focused-pre-mortem	1
F-P12	5	focused-pre-mortem	focused-pre-mortem	1
F-P24	1	focused-inversion	focused-inversion	1
F-P24	2	focused-inversion	focused-inversion	1
F-P24	3	focused-inversion	focused-inversion	1
F-P24	4	focused-inversion	focused-inversion	1
F-P24	5	focused-inversion	focused-inversion	1
F-P25	1	focused-pre-mortem	focused-pre-mortem	1
F-P25	2	focused-pre-mortem	focused-pre-mortem	1
F-P25	3	focused-pre-mortem	focused-pre-mortem	1
F-P25	4	focused-pre-mortem	focused-pre-mortem	1
F-P25	5	focused-pre-mortem	focused-pre-mortem	1
F-P26	1	focused-pre-mortem	focused-pre-mortem	1
F-P26	2	focused-pre-mortem	focused-pre-mortem	1
F-P26	3	focused-pre-mortem	focused-pre-mortem	1
F-P26	4	focused-pre-mortem	focused-pre-mortem	1
F-P26	5	focused-pre-mortem	focused-pre-mortem	1
B-N1	1	n-a	none	1
B-N1	2	n-a	none	1
B-N1	3	n-a	none	1
B-N1	4	n-a	none	1
B-N1	5	n-a	none	1
B-N2	1	n-a	none	1
B-N2	2	n-a	none	1
B-N2	3	n-a	none	1
B-N2	4	n-a	none	1
B-N2	5	n-a	none	1
F-N1	1	NOT-any-focused	none	1
F-N1	2	NOT-any-focused	none	1
F-N1	3	NOT-any-focused	none	1
F-N1	4	NOT-any-focused	none	1
F-N1	5	NOT-any-focused	none	1
```
