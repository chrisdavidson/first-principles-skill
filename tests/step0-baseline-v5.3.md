# Step 0 Live Harness Baseline — v5.3

**Recorded:** 2026-06-14T03:54:54Z (60 live `claude` invocations: 12 prompts × 5 repeats)
**Script version:** `scripts/check-step0-live.py` (commit `54d3103`)
**Core version:** `scripts/_battery_core.py` (commit `000cafc`)
**Fixture version:** `tests/step0-fixture-catalog.md` (commit `03d5ec5`)
**Agent version:** `first-principles/agents/first-principles.md` (commit `251eff3`)
**Run flags:** `--repeat 5 --min-pass 3`
**Run cwd:** `/tmp` (out-of-repo — see Methodology notes)
**Baseline verdict:** BATTERY: FAIL
**Summary:** P 3/6 (S-P01–06) | S-N 3/4 | S-P07/08 expected-FAIL (context-free)

---

## Per-prompt results

| ID | Expected MODE | K/N | Verdict |
|----|---------------|-----|---------|
| S-P01 | focused-pre-mortem | 1/5 FAIL | FAIL |
| S-P02 | focused-inversion | 0/5 FAIL | FAIL |
| S-P03 | focused-fishbone | 4/5 PASS | PASS |
| S-P04 | focused-five-whys | 5/5 PASS | PASS |
| S-P05 | focused-trade-off | 0/5 FAIL | FAIL |
| S-P06 | focused-second-order | 4/5 PASS | PASS |
| S-N01 | full-composer | 3/5 PASS | PASS |
| S-N02 | full-composer | 5/5 PASS | PASS |
| S-N03 | full-composer | 5/5 PASS | PASS |
| S-N04 | full-composer | 2/5 FAIL | FAIL |
| S-P07 | focused-pre-mortem | 3/5 PASS | FAIL (expected — context-free parser-robustness fixture, not part of the 4/6 live-technique bar) |
| S-P08 | focused-pre-mortem | 0/5 FAIL | FAIL (expected — context-free parser-robustness fixture, not part of the 4/6 live-technique bar) |

### Verdict-cell schema

Each row's K/N cell uses the falsifiable `<n>/N PASS|FAIL` format (matching the
`routing-battery-baseline-v4.3.md` convention). A row showing `<n>/5 FAIL`
does NOT satisfy the gate. `PASS` means `match_count >= min_pass`.
`FAIL` means `match_count < min_pass`.

---

## How this baseline was produced

```bash
REPO=/path/to/first-principles-skills
OUT_DIR=/tmp/step0-live-v5.3-$(date -u +%Y%m%dT%H%M%SZ)
cd /tmp && python3 "$REPO/scripts/check-step0-live.py" \
  --catalog "$REPO/tests/step0-fixture-catalog.md" \
  --plugin-dir "$REPO/first-principles" \
  --repeat 5 --min-pass 3 \
  --out "$OUT_DIR" \
  --baseline "$REPO/tests/step0-baseline-v5.3.md"
```

**Run date:** 2026-06-14T03:54:54Z

---

## Methodology notes

**Why run from `/tmp`.** Same rationale as the routing battery: when run from the
project root, the orchestrator's sub-agent may discover `.planning/` and plugin context,
enriching its response with project-specific artifacts. Running from `/tmp` ensures
the full-composer mode responds to the verbatim prompt only, matching the routing
battery baseline methodology (v4.3 Methodology notes).

**Why `--plugin-dir` must be an absolute path.** The script is invoked from `/tmp`;
a relative path would resolve against `/tmp`. Always pass an absolute path.

**Why `_classify_mode` infers `full-composer` from `none` + dispatch evidence.**
When `detect_output_structure_from_file` returns `none` but the capture shows
`Agent(subagent_type="first-principles:first-principles")` was dispatched, the
sub-agent ran the full-composer path but produced a non-structured response
(e.g., a clarification request when `AskUserQuestion` is unavailable). The
dispatch itself proves Step 0 chose the full-composer path. This inference is
applied only in the Step 0 harness; `_battery_core.py` is not modified (D-02).

**Residual risk notes (D-03).** The following rows did not reach `min_pass`.
Their true observed K/N is recorded below; a forced PASS is never written.

- `S-P01`: 1/5 FAIL — expected `focused-pre-mortem`; observed modes: ['full-composer', 'full-composer', 'focused-pre-mortem', 'full-composer', 'full-composer']. Residual-risk tracked as RR-79-01.
- `S-P02`: 0/5 FAIL — expected `focused-inversion`; observed modes: ['full-composer', 'full-composer', 'full-composer', 'full-composer', 'full-composer']. Residual-risk tracked as RR-79-02.
- `S-P05`: 0/5 FAIL — expected `focused-trade-off`; observed modes: ['full-composer', 'full-composer', 'full-composer', 'full-composer', 'full-composer']. Residual-risk tracked as RR-79-03.
- `S-N04`: 2/5 FAIL — expected `full-composer`; observed modes: ['focused-pre-mortem', 'full-composer', 'full-composer', 'focused-pre-mortem', 'focused-pre-mortem']. Residual-risk tracked as RR-75-NN (unassigned — needs a tracked RR ID).

---

## Scores (scores.tsv)

```
id	run	expected	actual	match
S-P01	1	focused-pre-mortem	full-composer	0
S-P01	2	focused-pre-mortem	full-composer	0
S-P01	3	focused-pre-mortem	focused-pre-mortem	1
S-P01	4	focused-pre-mortem	full-composer	0
S-P01	5	focused-pre-mortem	full-composer	0
S-P02	1	focused-inversion	full-composer	0
S-P02	2	focused-inversion	full-composer	0
S-P02	3	focused-inversion	full-composer	0
S-P02	4	focused-inversion	full-composer	0
S-P02	5	focused-inversion	full-composer	0
S-P03	1	focused-fishbone	focused-fishbone	1
S-P03	2	focused-fishbone	focused-fishbone	1
S-P03	3	focused-fishbone	focused-fishbone	1
S-P03	4	focused-fishbone	full-composer	0
S-P03	5	focused-fishbone	focused-fishbone	1
S-P04	1	focused-five-whys	focused-five-whys	1
S-P04	2	focused-five-whys	focused-five-whys	1
S-P04	3	focused-five-whys	focused-five-whys	1
S-P04	4	focused-five-whys	focused-five-whys	1
S-P04	5	focused-five-whys	focused-five-whys	1
S-P05	1	focused-trade-off	full-composer	0
S-P05	2	focused-trade-off	full-composer	0
S-P05	3	focused-trade-off	full-composer	0
S-P05	4	focused-trade-off	full-composer	0
S-P05	5	focused-trade-off	full-composer	0
S-P06	1	focused-second-order	focused-second-order	1
S-P06	2	focused-second-order	focused-second-order	1
S-P06	3	focused-second-order	focused-second-order	1
S-P06	4	focused-second-order	focused-second-order	1
S-P06	5	focused-second-order	full-composer	0
S-N01	1	full-composer	full-composer	1
S-N01	2	full-composer	focused-pre-mortem	0
S-N01	3	full-composer	full-composer	1
S-N01	4	full-composer	focused-pre-mortem	0
S-N01	5	full-composer	full-composer	1
S-N02	1	full-composer	full-composer	1
S-N02	2	full-composer	full-composer	1
S-N02	3	full-composer	full-composer	1
S-N02	4	full-composer	full-composer	1
S-N02	5	full-composer	full-composer	1
S-N03	1	full-composer	full-composer	1
S-N03	2	full-composer	full-composer	1
S-N03	3	full-composer	full-composer	1
S-N03	4	full-composer	full-composer	1
S-N03	5	full-composer	full-composer	1
S-N04	1	full-composer	focused-pre-mortem	0
S-N04	2	full-composer	full-composer	1
S-N04	3	full-composer	full-composer	1
S-N04	4	full-composer	focused-pre-mortem	0
S-N04	5	full-composer	focused-pre-mortem	0
S-P07	1	focused-pre-mortem	focused-pre-mortem	1
S-P07	2	focused-pre-mortem	focused-pre-mortem	1
S-P07	3	focused-pre-mortem	full-composer	0
S-P07	4	focused-pre-mortem	full-composer	0
S-P07	5	focused-pre-mortem	focused-pre-mortem	1
S-P08	1	focused-pre-mortem	full-composer	0
S-P08	2	focused-pre-mortem	full-composer	0
S-P08	3	focused-pre-mortem	full-composer	0
S-P08	4	focused-pre-mortem	full-composer	0
S-P08	5	focused-pre-mortem	full-composer	0
```

---

## Lineage

This baseline records the Phase 80 live re-baseline of Step 0 technique selection,
following the Phase 79 capture-grounded detector resolution. Phase 79 applied three
carry-forward provenance fixes (DET-13: S-P01 pre-mortem comment, commit 000cafc;
DET-14: S-P02 inversion comment, commit 7d4f9fc; DET-15: S-P05 trade-off comment,
commit c5d5d3f). No new detector markers were added for S-P01/02/05 because grep proofs
over all Phase 79 captures confirmed no false-positive-safe phrase exists for those rows.
The three residuals are carried forward as RR-79-01 (S-P01), RR-79-02 (S-P02),
and RR-79-03 (S-P05) — renamed from RR-75-01/02/05 after Phase 79 evidence.

Prior baseline: tests/step0-baseline-v5.2.md (Phase 78, commit 6cc52b5) — BATTERY: FAIL,
P 3/6 (S-P01-06), S-N 4/4; residuals RR-75-01/02/05 renamed RR-79-01/02/03 after Phase 79 evidence.
