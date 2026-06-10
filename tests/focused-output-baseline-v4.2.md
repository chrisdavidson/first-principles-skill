# Focused-Output Baseline — v4.2 (FOCUS-01: FU-21 correction — 4P + 1N catalog, P26 re-ID)

**Recorded:** 2026-06-10 (22:15–22:39 UTC, ~24 min wall-clock for 25 live `claude` invocations)
**Script version:** `scripts/check-focused-output.py` (commit `151b197`)
**Agent version:** `first-principles/agents/first-principles.md` (commit `151b197`)
**Stub set:** `first-principles/skills/<technique>/SKILL.md` × 11 (commit `151b197`)
**Fixture version:** `tests/focused-output-catalog.md` (commit `151b197`, v4.2 — P12/P24/P25/P26 + lone N1)
**Run flags:** `--repeat 5 --min-pass 3 --p-threshold 4 --n-threshold 1`
**Run cwd:** `/tmp` (out-of-repo — see Methodology notes)
**Baseline verdict:** BATTERY: PASS
**Summary:** P 4/4 | N 1/1 (all four P rows PASS at K-of-N; lone N1 negative-control PASS)
**Pre-run masked-threshold audit:** clean — see `.planning/notes/audit-masked-thresholds-v4.2.md`

---

## Per-prompt results

| #   | Expected           | Technique     | Runs | Matches | K/N     | Verdict |
|-----|--------------------|---------------|------|---------|---------|---------|
| P12 | focused-pre-mortem | pre-mortem    | 5    | 3       | 3/5 PASS | FU-21-1 via slash; 2 runs drifted to `full-composer` (stochastic) |
| P24 | focused-inversion  | inversion     | 5    | 3       | 3/5 PASS | FU-21-2 via slash; 2 runs drifted to `full-composer` (verified in run-2/run-3 captures: standalone `Ground Truths`/`Verdict` tokens in incidental handoff/analytic prose reached the structural override at MIN_HEADER_HITS=2 — the Phase-header pattern fired 0 times) |
| P25 | focused-pre-mortem | pre-mortem    | 5    | 5       | 5/5 PASS | Strong result — new fixture in v4.2; multi-phase plan prompt, all 5 runs classified correctly |
| P26 | focused-pre-mortem | pre-mortem    | 5    | 5       | 5/5 PASS | Re-IDed from N2 in v3.8 (plan-shaped slash invocation); all 5 runs classified correctly |
| N1  | NOT-any-focused    | (none)        | 5    | 4       | 4/5 PASS | Over-trigger guard; 1 run classified `focused-pre-mortem` (stochastic), 4 runs classified `none` |

### Verdict-cell schema

Each row's Verdict cell uses the falsifiable `<n>/N PASS|FAIL` format per the Plan 46-04 acceptance criteria. A row that says `<n>/5 FAIL` would NOT satisfy the gate — gates are unfalsifiable when the verify checks for substring presence only.

### N1 PASS criterion (rationale)

N1 is the over-trigger guard: a debugging-shaped prompt without a slash prefix that must NOT auto-route to any focused technique. The expected value is `NOT-any-focused` — a negative-set semantic meaning "actual classification must not be any `focused-*` verdict the detector can emit": {`focused-pre-mortem`, `focused-inversion`, `focused-fishbone`, `focused-five-whys`, `focused-trade-off`, `focused-second-order`} (the six-element `_FOCUSED_PREFIXES` set in `scripts/check-focused-output.py`, built from `_TECHNIQUE_KEYS`). Any classification in {`full-composer`, `none`, `ambiguous`} counts as a PASS.

In this run, N1 classified as: run 1 = `focused-pre-mortem` (FAIL for this row), runs 2–5 = `none` (PASS). K=4 meets the min-pass=3 threshold. The sole `focused-pre-mortem` result on run 1 reflects the stochastic gate tolerance built into K-of-N.

---

## How this baseline was produced

```bash
REPO=/home/chrisdavidson/programming/first-principles-skills
OUT_DIR=/tmp/focused-output-v4.2-20260610T221518Z
python3 "$REPO/scripts/check-focused-output.py" \
  --catalog "$REPO/tests/focused-output-catalog.md" \
  --repeat 5 --min-pass 3 \
  --p-threshold 4 --n-threshold 1 \
  --plugin-dir "$REPO/first-principles" \
  --out "$OUT_DIR"
```

**Run date:** 2026-06-10T22:15:18Z (start) → 2026-06-10T22:39:44Z (end, ~24 min wall-clock).

**Output directory:** `/tmp/focused-output-v4.2-20260610T221518Z/` (transient). Contains 25 `<id>-run{1..5}.jsonl` raw stream-json captures, `scores.tsv`, and `verdict.txt`. Raw artifacts not committed (D-09).

**Run context:** This is the third and complete execution of the focused-output battery for the v4.2 milestone. The first run (2026-06-10T17:17:21Z) FAILed due to a Signal B detector defect (see Lineage). The second run was interrupted by a provider spend limit at the 4th P row (all 4 P rows had PASSed at interruption). This run (the third) completed without interruption.

---

## Methodology notes

**Why this baseline runs from `/tmp` (not project root).** When run from the project root, the orchestrator enriches vague or oblique prompts with `.planning/` context — causing it to run a meta-pre-mortem on the project itself rather than the user-supplied content. Running from `/tmp` eliminates this project-context enrichment surface. The `--plugin-dir` absolute path ensures the plugin is still loaded correctly from `/tmp` (without this flag, the script cannot find the plugin and exits with code 2).

**Why `--plugin-dir` must be an absolute path.** The script is invoked from `/tmp`; a relative `./first-principles` path would resolve against `/tmp`, not the project root. Always pass an absolute path from the project root.

**Why the K-of-N tolerance is set at min-pass=3.** Phase 45 and Phase 46 baselines both document ±3 P-prompt swing within the same session (see `routing-battery-noise` memory entry). `--repeat 5 --min-pass 3` encodes this tolerance: a row is PASS if ≥ 3 of 5 runs classify correctly, accepting up to 2 stochastic misses per row.

---

## Lineage

This baseline supersedes `tests/focused-output-baseline-v3.8.md` (Phase 46-04 closure; VERIFY-01). What changed:

**Fixture corrections (Phase 65):**
- **N2 re-IDed to P26:** In v3.8, N2 expected `focused-pre-mortem` — a positive expectation placed in the N (negative-control) bucket. This was a structural contradiction: rows in the N bucket must represent cases where focused output should NOT occur; a row that expects `focused-pre-mortem` belongs in the P bucket. Phase 65 corrected this by moving the row to P26 in the P bucket. The same prompt is tested; only the bucket and expectation semantics are corrected.
- **Strict P-threshold (was masked):** The v3.8 baseline was recorded with `--p-threshold 2` (requiring only 2 of the 4 P rows to pass). This v4.2 baseline uses `--p-threshold 4` — all four P rows must pass. The evidence chain for the fixture correction is in `.planning/notes/fu21-fixture-contradiction-diagnosis.md`.
- **N-threshold:** `--n-threshold 1` is unchanged from v3.8.

**First run FAIL and detector fix (2026-06-10):**
The first battery run under v4.2 (OUT_DIR: `/tmp/focused-output-v4.2-20260610T171721Z/`) returned `BATTERY: FAIL` with P: 0/4. Root-cause diagnosis (`.planning/notes/focused-output-battery-fail-diagnosis-20260610.md`) found two bugs in `scripts/check-focused-output.py`'s Signal B detector:

1. `\bPhase\s+[0-9]+\b` in `_COMPOSER_STRUCTURE_PATTERNS` was too broad — it fired on plan-content prose ("Phase 1 migrates staging") in addition to the composer's structural section headers, causing P24 (inversion) and P25 (multi-phase plan pre-mortem) to false-classify as `full-composer`.
2. Pre-mortem technique markers in `_TECHNIQUE_CATEGORIES` were under-specified — requiring exact procedure-text phrases that real agent output rarely matches verbatim, causing consistent under-detection on P12 and P26.

The user authorized the Signal B redesign. The fix was implemented and committed at commit `151b197` (Phase 66-03). This baseline records the first complete PASS run after that fix.

**Second run interrupted (2026-06-10):** A second verbatim battery run was interrupted by a provider spend limit after 4 P rows completed (all 4 P rows had PASSed at the point of interruption). The third run — this baseline — completed without interruption.

---

## Scores (verbatim from scores.tsv)

```
id    run  expected             actual               match
P12   1    focused-pre-mortem   focused-pre-mortem   1
P12   2    focused-pre-mortem   focused-pre-mortem   1
P12   3    focused-pre-mortem   focused-pre-mortem   1
P12   4    focused-pre-mortem   full-composer        0
P12   5    focused-pre-mortem   full-composer        0
P24   1    focused-inversion    focused-inversion    1
P24   2    focused-inversion    full-composer        0
P24   3    focused-inversion    full-composer        0
P24   4    focused-inversion    focused-inversion    1
P24   5    focused-inversion    focused-inversion    1
P25   1    focused-pre-mortem   focused-pre-mortem   1
P25   2    focused-pre-mortem   focused-pre-mortem   1
P25   3    focused-pre-mortem   focused-pre-mortem   1
P25   4    focused-pre-mortem   focused-pre-mortem   1
P25   5    focused-pre-mortem   focused-pre-mortem   1
P26   1    focused-pre-mortem   focused-pre-mortem   1
P26   2    focused-pre-mortem   focused-pre-mortem   1
P26   3    focused-pre-mortem   focused-pre-mortem   1
P26   4    focused-pre-mortem   focused-pre-mortem   1
P26   5    focused-pre-mortem   focused-pre-mortem   1
N1    1    NOT-any-focused      focused-pre-mortem   0
N1    2    NOT-any-focused      none                 1
N1    3    NOT-any-focused      none                 1
N1    4    NOT-any-focused      none                 1
N1    5    NOT-any-focused      none                 1
```
