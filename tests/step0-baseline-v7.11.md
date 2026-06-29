# Step 0 Live Harness Baseline — v7.11

**Recorded:** 2026-06-28/29 UTC — 3-run best-genuine merge (run1 20260628T201506Z + run2 20260628T221800Z + run3 rerun 20260629T031934Z); monthly-spend-limit truncation in runs 1-2 recovered per D-02 resume-to-complete (145 live `claude` invocations: 29 prompts × 5 repeats)
**Script version:** `scripts/check-step0-live.py` (commit `63c81b9`)
**Core version:** `scripts/_battery_core.py` (commit `34100c0`)
**Fixture version:** `tests/step0-fixture-catalog.md` (commit `02fd820`)
**Agent version:** `first-principles/agents/first-principles.md` (commit `9a795e2`)
**Run flags:** `--repeat 5 --min-pass 3`
**Run cwd:** `/tmp` (out-of-repo — see Methodology notes)
**Baseline verdict:** BATTERY: FAIL
**Summary:** P 4/8 (8-technique canonical bar: S-P01–06 + S-P10 estimate, S-P14 theoretical-limit) | S-N 8/14 | S-P07/08/11/12/13/15 expected-FAIL (context-free / alternation falsifiers, excluded from the bar) | S-P16 merge-validation (outside /8): 0/5 (FAIL)

---

## Per-prompt results

| ID | Expected MODE | K/N | Verdict |
|----|---------------|-----|---------|
| S-P01 | focused-pre-mortem | 5/5 PASS | PASS |
| S-P02 | focused-inversion | 2/5 FAIL | FAIL |
| S-P03 | focused-fishbone | 4/5 PASS | PASS |
| S-P04 | focused-five-whys | 2/5 FAIL | FAIL |
| S-P05 | focused-trade-off | 5/5 PASS | PASS |
| S-P06 | focused-second-order | 4/5 PASS | PASS |
| S-N01 | full-composer | 1/5 FAIL | FAIL |
| S-N02 | full-composer | 3/5 PASS | PASS |
| S-N03 | full-composer | 3/5 PASS | PASS |
| S-N04 | full-composer | 2/5 FAIL | FAIL |
| S-P07 | focused-pre-mortem | 4/5 PASS | FAIL (expected — context-free parser-robustness fixture, not part of the 4/8 live-technique bar) |
| S-P08 | focused-pre-mortem | 0/5 FAIL | FAIL (expected — context-free parser-robustness fixture, not part of the 4/8 live-technique bar) |
| S-P10 | focused-estimate | 0/5 FAIL | FAIL |
| S-P11 | focused-estimate | 0/5 FAIL | FAIL (expected — context-free parser-robustness fixture, not part of the 4/8 live-technique bar) |
| S-P12 | focused-estimate | 0/5 FAIL | FAIL (expected — context-free parser-robustness fixture, not part of the 4/8 live-technique bar) |
| S-P13 | focused-estimate | 0/5 FAIL | FAIL (expected — context-free parser-robustness fixture, not part of the 4/8 live-technique bar) |
| S-N06 | full-composer | 5/5 PASS | PASS |
| S-P14 | focused-theoretical-limit | 0/5 FAIL | FAIL |
| S-P15 | focused-theoretical-limit | 0/5 FAIL | FAIL (expected — context-free parser-robustness fixture, not part of the 4/8 live-technique bar) |
| S-N07 | full-composer | 5/5 PASS | PASS |
| S-P16 | focused-five-whys | 0/5 FAIL | FAIL (merge-validation signal — outside /8 canonical bar; tracked via _s_p16_result line, not a residual-risk row) |
| S-N08 | full-composer | 5/5 PASS | PASS |
| S-N09 | full-composer | 3/5 PASS | PASS |
| S-N10 | full-composer | 3/5 PASS | PASS |
| S-N11 | full-composer | 2/5 FAIL | FAIL |
| S-N12 | full-composer | 2/5 FAIL | FAIL |
| S-N13 | full-composer | 5/5 PASS | PASS |
| S-N14 | full-composer | 2/5 FAIL | FAIL |
| S-N15 | full-composer | 2/5 FAIL | FAIL |

### Verdict-cell schema

Each row's K/N cell uses the falsifiable `<n>/N PASS|FAIL` format (matching the
`routing-battery-baseline-v4.3.md` convention). A row showing `<n>/5 FAIL`
does NOT satisfy the gate. `PASS` means `match_count >= min_pass`.
`FAIL` means `match_count < min_pass`.

---

## How this baseline was produced

```bash
REPO=/path/to/first-principles-skills
OUT_DIR=/tmp/step0-live-v7.11-$(date -u +%Y%m%dT%H%M%SZ)
cd /tmp && python3 "$REPO/scripts/check-step0-live.py" \
  --catalog "$REPO/tests/step0-fixture-catalog.md" \
  --plugin-dir "$REPO/first-principles" \
  --repeat 5 --min-pass 3 \
  --out "$OUT_DIR" \
  --baseline "$REPO/tests/step0-baseline-v7.11.md"
```

**Run date:** 2026-06-28/29 UTC — 3-run best-genuine merge (run1 20260628T201506Z + run2 20260628T221800Z + run3 rerun 20260629T031934Z); monthly-spend-limit truncation in runs 1-2 recovered per D-02 resume-to-complete

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

- `S-P02`: 2/5 FAIL — expected `focused-inversion`; observed modes: ['focused-inversion', 'full-composer', 'full-composer', 'full-composer', 'focused-inversion']. Residual-risk tracked as RR-114-01.
- `S-P04`: 2/5 FAIL — expected `focused-five-whys`; observed modes: ['full-composer', 'full-composer', 'focused-five-whys', 'full-composer', 'focused-five-whys']. Residual-risk tracked as RR-75-04.
- `S-N01`: 1/5 FAIL — expected `full-composer`; observed modes: ['full-composer', 'focused-pre-mortem', 'focused-pre-mortem', 'focused-pre-mortem', 'focused-pre-mortem']. Residual-risk tracked as RR-108-08.
- `S-N04`: 2/5 FAIL — expected `full-composer`; observed modes: ['focused-pre-mortem', 'focused-pre-mortem', 'focused-pre-mortem', 'full-composer', 'full-composer']. Residual-risk tracked as RR-80-01.
- `S-P10`: 0/5 FAIL — expected `focused-estimate`; observed modes: ['full-composer', 'full-composer', 'full-composer', 'full-composer', 'full-composer']. Residual-risk tracked as RR-108-04.
- `S-P14`: 0/5 FAIL — expected `focused-theoretical-limit`; observed modes: ['full-composer', 'full-composer', 'full-composer', 'full-composer', 'full-composer']. Residual-risk tracked as RR-108-05.
- `S-N11`: 2/5 FAIL — expected `full-composer`; observed modes: ['focused-pre-mortem', 'full-composer', 'focused-pre-mortem', 'full-composer', 'focused-pre-mortem']. Residual-risk tracked as RR-108-08.
- `S-N12`: 2/5 FAIL — expected `full-composer`; observed modes: ['full-composer', 'full-composer', 'focused-pre-mortem', 'focused-pre-mortem', 'focused-pre-mortem']. Residual-risk tracked as RR-108-08.
- `S-N14`: 2/5 FAIL — expected `full-composer`; observed modes: ['focused-pre-mortem', 'focused-pre-mortem', 'full-composer', 'full-composer', 'focused-pre-mortem']. Residual-risk tracked as RR-108-08.
- `S-N15`: 2/5 FAIL — expected `full-composer`; observed modes: ['focused-pre-mortem', 'full-composer', 'full-composer', 'focused-pre-mortem', 'focused-pre-mortem']. Residual-risk tracked as RR-108-08.

---

## Scores (scores.tsv)

```
id	run	expected	actual	match
S-P01	1	focused-pre-mortem	focused-pre-mortem	1
S-P01	2	focused-pre-mortem	focused-pre-mortem	1
S-P01	3	focused-pre-mortem	focused-pre-mortem	1
S-P01	4	focused-pre-mortem	focused-pre-mortem	1
S-P01	5	focused-pre-mortem	focused-pre-mortem	1
S-P02	1	focused-inversion	focused-inversion	1
S-P02	2	focused-inversion	full-composer	0
S-P02	3	focused-inversion	full-composer	0
S-P02	4	focused-inversion	full-composer	0
S-P02	5	focused-inversion	focused-inversion	1
S-P03	1	focused-fishbone	focused-fishbone	1
S-P03	2	focused-fishbone	focused-fishbone	1
S-P03	3	focused-fishbone	full-composer	0
S-P03	4	focused-fishbone	focused-fishbone	1
S-P03	5	focused-fishbone	focused-fishbone	1
S-P04	1	focused-five-whys	full-composer	0
S-P04	2	focused-five-whys	full-composer	0
S-P04	3	focused-five-whys	focused-five-whys	1
S-P04	4	focused-five-whys	full-composer	0
S-P04	5	focused-five-whys	focused-five-whys	1
S-P05	1	focused-trade-off	focused-trade-off	1
S-P05	2	focused-trade-off	focused-trade-off	1
S-P05	3	focused-trade-off	focused-trade-off	1
S-P05	4	focused-trade-off	focused-trade-off	1
S-P05	5	focused-trade-off	focused-trade-off	1
S-P06	1	focused-second-order	focused-second-order	1
S-P06	2	focused-second-order	focused-second-order	1
S-P06	3	focused-second-order	focused-second-order	1
S-P06	4	focused-second-order	focused-second-order	1
S-P06	5	focused-second-order	full-composer	0
S-N01	1	full-composer	full-composer	1
S-N01	2	full-composer	focused-pre-mortem	0
S-N01	3	full-composer	focused-pre-mortem	0
S-N01	4	full-composer	focused-pre-mortem	0
S-N01	5	full-composer	focused-pre-mortem	0
S-N02	1	full-composer	full-composer	1
S-N02	2	full-composer	full-composer	1
S-N02	3	full-composer	full-composer	1
S-N02	4	full-composer	focused-pre-mortem	0
S-N02	5	full-composer	focused-pre-mortem	0
S-N03	1	full-composer	focused-pre-mortem	0
S-N03	2	full-composer	full-composer	1
S-N03	3	full-composer	focused-inversion	0
S-N03	4	full-composer	full-composer	1
S-N03	5	full-composer	full-composer	1
S-N04	1	full-composer	focused-pre-mortem	0
S-N04	2	full-composer	focused-pre-mortem	0
S-N04	3	full-composer	focused-pre-mortem	0
S-N04	4	full-composer	full-composer	1
S-N04	5	full-composer	full-composer	1
S-P07	1	focused-pre-mortem	focused-pre-mortem	1
S-P07	2	focused-pre-mortem	full-composer	0
S-P07	3	focused-pre-mortem	focused-pre-mortem	1
S-P07	4	focused-pre-mortem	focused-pre-mortem	1
S-P07	5	focused-pre-mortem	focused-pre-mortem	1
S-P08	1	focused-pre-mortem	full-composer	0
S-P08	2	focused-pre-mortem	focused-fishbone	0
S-P08	3	focused-pre-mortem	ambiguous	0
S-P08	4	focused-pre-mortem	ambiguous	0
S-P08	5	focused-pre-mortem	ambiguous	0
S-P10	1	focused-estimate	full-composer	0
S-P10	2	focused-estimate	full-composer	0
S-P10	3	focused-estimate	full-composer	0
S-P10	4	focused-estimate	full-composer	0
S-P10	5	focused-estimate	full-composer	0
S-P11	1	focused-estimate	full-composer	0
S-P11	2	focused-estimate	full-composer	0
S-P11	3	focused-estimate	full-composer	0
S-P11	4	focused-estimate	full-composer	0
S-P11	5	focused-estimate	full-composer	0
S-P12	1	focused-estimate	full-composer	0
S-P12	2	focused-estimate	full-composer	0
S-P12	3	focused-estimate	full-composer	0
S-P12	4	focused-estimate	full-composer	0
S-P12	5	focused-estimate	full-composer	0
S-P13	1	focused-estimate	full-composer	0
S-P13	2	focused-estimate	full-composer	0
S-P13	3	focused-estimate	full-composer	0
S-P13	4	focused-estimate	full-composer	0
S-P13	5	focused-estimate	full-composer	0
S-N06	1	full-composer	full-composer	1
S-N06	2	full-composer	full-composer	1
S-N06	3	full-composer	full-composer	1
S-N06	4	full-composer	full-composer	1
S-N06	5	full-composer	full-composer	1
S-P14	1	focused-theoretical-limit	full-composer	0
S-P14	2	focused-theoretical-limit	full-composer	0
S-P14	3	focused-theoretical-limit	full-composer	0
S-P14	4	focused-theoretical-limit	full-composer	0
S-P14	5	focused-theoretical-limit	full-composer	0
S-P15	1	focused-theoretical-limit	full-composer	0
S-P15	2	focused-theoretical-limit	full-composer	0
S-P15	3	focused-theoretical-limit	full-composer	0
S-P15	4	focused-theoretical-limit	full-composer	0
S-P15	5	focused-theoretical-limit	full-composer	0
S-N07	1	full-composer	full-composer	1
S-N07	2	full-composer	full-composer	1
S-N07	3	full-composer	full-composer	1
S-N07	4	full-composer	full-composer	1
S-N07	5	full-composer	full-composer	1
S-P16	1	focused-five-whys	full-composer	0
S-P16	2	focused-five-whys	full-composer	0
S-P16	3	focused-five-whys	full-composer	0
S-P16	4	focused-five-whys	full-composer	0
S-P16	5	focused-five-whys	full-composer	0
S-N08	1	full-composer	full-composer	1
S-N08	2	full-composer	full-composer	1
S-N08	3	full-composer	full-composer	1
S-N08	4	full-composer	full-composer	1
S-N08	5	full-composer	full-composer	1
S-N09	1	full-composer	full-composer	1
S-N09	2	full-composer	focused-pre-mortem	0
S-N09	3	full-composer	full-composer	1
S-N09	4	full-composer	full-composer	1
S-N09	5	full-composer	focused-pre-mortem	0
S-N10	1	full-composer	full-composer	1
S-N10	2	full-composer	full-composer	1
S-N10	3	full-composer	focused-pre-mortem	0
S-N10	4	full-composer	focused-pre-mortem	0
S-N10	5	full-composer	full-composer	1
S-N11	1	full-composer	focused-pre-mortem	0
S-N11	2	full-composer	full-composer	1
S-N11	3	full-composer	focused-pre-mortem	0
S-N11	4	full-composer	full-composer	1
S-N11	5	full-composer	focused-pre-mortem	0
S-N12	1	full-composer	full-composer	1
S-N12	2	full-composer	full-composer	1
S-N12	3	full-composer	focused-pre-mortem	0
S-N12	4	full-composer	focused-pre-mortem	0
S-N12	5	full-composer	focused-pre-mortem	0
S-N13	1	full-composer	full-composer	1
S-N13	2	full-composer	full-composer	1
S-N13	3	full-composer	full-composer	1
S-N13	4	full-composer	full-composer	1
S-N13	5	full-composer	full-composer	1
S-N14	1	full-composer	focused-pre-mortem	0
S-N14	2	full-composer	focused-pre-mortem	0
S-N14	3	full-composer	full-composer	1
S-N14	4	full-composer	full-composer	1
S-N14	5	full-composer	focused-pre-mortem	0
S-N15	1	full-composer	focused-pre-mortem	0
S-N15	2	full-composer	full-composer	1
S-N15	3	full-composer	full-composer	1
S-N15	4	full-composer	focused-pre-mortem	0
S-N15	5	full-composer	focused-pre-mortem	0
```

---

## Lineage

This baseline records the Phase 128-129 v7.11 **whole-system live re-measure** of Step 0
technique selection. This is a **measurement-only** re-measure: there is NO detector change
and NO agent-body change this milestone. The agent body is measured **as-shipped (v7.10)**
and the detector `scripts/_battery_core.py` is **frozen** (`_TECHNIQUE_CATEGORIES` unchanged —
inversion 13 markers, trade-off 10 markers (post-Phase-121 OCH-02) — `MIN_HEADER_HITS=2`,
`_COMPOSER_FOCUS_CEILING=4` byte-unchanged). This run uses the 8 canonical rows:
S-P01 pre-mortem, S-P02 inversion, S-P03 fishbone, S-P04 five-whys, S-P05
trade-off, S-P06 second-order, S-P10 estimate, S-P14 theoretical-limit. All 8
techniques have a v7.8 prior K/N. S-P16 (the absorbed reduce-to-primitives prompt
routing to focused-five-whys) is measured as a dedicated merge-validation signal
outside the /8 canonical bar (D-01a). Honesty-not-score (D-01) governs the committed
verdict; the falsifiable criterion is applied at a blocking human checkpoint, not forced.
This run is uncapped (no spend-limit constraint); all 29 S-P/S-N fixture rows are measured
(S-A semantic-ambiguity rows excluded from live run).

Three carried residuals from v7.8 may be resolved-or-carried in this run: RR-114-01
(S-P02 inversion, v7.6 live 1/5; RESOLVED-STRUCTURALLY-OFFLINE Phase 121 OCH-02;
live pass-rate re-measure this run), RR-108-04 (S-P10 estimate, v7.6
spend-limit-indeterminate), RR-108-05 (S-P14 theoretical-limit, v7.6
spend-limit-indeterminate). Each is CLOSED at its observed K/N if it reaches
min-pass (≥3/5), or CARRIED FORWARD under a freshly-minted superseding Phase-129
RR ID otherwise (that mint is conditional and post-run — it is NOT pre-baked in
the offline firewall commit).

Prior baseline: tests/step0-baseline-v7.8.md (Phase 118-119 CONF-03) — BATTERY: PASS,
targeted 6-row confirmation (S-P01/S-P03 + S-N01/S-N02/S-N03/S-N04); residuals
RR-114-01 (S-P02 inversion, CARRIED — structural offline resolution Phase 121),
RR-108-04 (S-P10 estimate, CARRIED-indeterminate), RR-108-05 (S-P14 theoretical-limit,
CARRIED-indeterminate) carried forward into this v7.11 run.

---

## Residual Dispositions (v7.11)

Disposition applied per D-04 (K/N ≥ 3/5 → CLOSED; below → CARRIED keeping the existing RR ID per
D-09 CLOSE-keeps-ID precedent — no RR-129-NN successor is minted; this explicitly supersedes the
auto-Lineage "freshly-minted superseding Phase-129 RR ID" note above); `_RR_ID_MAP` / BATT-06
`_load_excerpt_v711` sentinel re-point deferred to Phase 131 (D-05). Human-confirmed at the Phase
129 Plan 03 blocking checkpoint (honesty-not-score, D-01).

| Prompt | Technique | v7.11 K/N | Disposition | RR ID (kept) |
|--------|-----------|-----------|-------------|--------------|
| S-P02 | inversion | 2/5 FAIL | CARRIED (2/5 < 3/5) | RR-114-01 |
| S-P10 | estimate | 0/5 FAIL | CARRIED (0/5 < 3/5) | RR-108-04 |
| S-P14 | theoretical-limit | 0/5 FAIL | CARRIED (0/5 < 3/5) | RR-108-05 |
