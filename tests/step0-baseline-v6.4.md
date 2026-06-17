# Step 0 Live Harness Baseline — v6.4

**Recorded:** 2026-06-17T16:29:38Z (60 live `claude` invocations: 12 prompts × 5 repeats)
**Script version:** `scripts/check-step0-live.py` (commit `70f4876`)
**Core version:** `scripts/_battery_core.py` (commit `2769683`)
**Fixture version:** `tests/step0-fixture-catalog.md` (commit `03d5ec5`)
**Agent version:** `first-principles/agents/first-principles.md` (commit `03d6788`)
**Run flags:** `--repeat 5 --min-pass 3`
**Run cwd:** `/tmp` (out-of-repo — see Methodology notes)
**Baseline verdict:** BATTERY: FAIL
**Summary:** P 3/6 (S-P01–06) | S-N 4/4 | S-P07/08 expected-FAIL (context-free)

---

## Per-prompt results

| ID | Expected MODE | K/N | Verdict |
|----|---------------|-----|---------|
| S-P01 | focused-pre-mortem | 4/5 PASS | PASS |
| S-P02 | focused-inversion | 1/5 FAIL | FAIL |
| S-P03 | focused-fishbone | 4/5 PASS | PASS |
| S-P04 | focused-five-whys | 2/5 FAIL | FAIL |
| S-P05 | focused-trade-off | 2/5 FAIL | FAIL |
| S-P06 | focused-second-order | 3/5 PASS | PASS |
| S-N01 | full-composer | 3/5 PASS | PASS |
| S-N02 | full-composer | 5/5 PASS | PASS |
| S-N03 | full-composer | 5/5 PASS | PASS |
| S-N04 | full-composer | 4/5 PASS | PASS |
| S-P07 | focused-pre-mortem | 2/5 FAIL | FAIL (expected — context-free parser-robustness fixture, not part of the 3/6 live-technique bar) |
| S-P08 | focused-pre-mortem | 0/5 FAIL | FAIL (expected — context-free parser-robustness fixture, not part of the 3/6 live-technique bar) |

### Verdict-cell schema

Each row's K/N cell uses the falsifiable `<n>/N PASS|FAIL` format (matching the
`routing-battery-baseline-v4.3.md` convention). A row showing `<n>/5 FAIL`
does NOT satisfy the gate. `PASS` means `match_count >= min_pass`.
`FAIL` means `match_count < min_pass`.

---

## How this baseline was produced

```bash
REPO=/home/chrisdavidson/programming/first-principles-skills
OUT_DIR=/tmp/step0-live-v6.4-20260617T152153Z
cd /tmp && python3 "$REPO/scripts/check-step0-live.py" \
  --catalog "$REPO/tests/step0-fixture-catalog.md" \
  --plugin-dir "$REPO/first-principles" \
  --repeat 5 --min-pass 3 \
  --out "$OUT_DIR"
```

**Run date:** 2026-06-17T15:21:53Z (completed 2026-06-17T16:29:38Z)

The baseline file was hand-written from the authoritative `/tmp` out-dir captures (D-05:
one run only, D-06: orchestrator-owned with blocking human checkpoint before finalize).
The `scores.tsv` block below is embedded verbatim from the run out-dir.

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

- `S-P02`: 1/5 FAIL — expected `focused-inversion`; observed modes: ['focused-inversion', 'full-composer', 'full-composer', 'full-composer', 'full-composer']. 4/5 runs under-routed to full-composer (Step 0 inversion trigger did not fire). Residual-risk tracked as RR-95-01 (supersedes RR-92-01). Phase 94's directed fix (inversion markers 7→9, SKILL-body.md Step 0 trigger tightening) was the expected lift for this row — the committed verdict is 1/5, an improvement from v6.3's 0/5 but below min-pass. Carry-forward is the legitimate, honesty-not-score outcome (D-01/D-04).
- `S-P04`: 2/5 FAIL — expected `focused-five-whys`; observed modes: ['focused-five-whys', 'full-composer', 'full-composer', 'focused-five-whys', 'full-composer']. Residual-risk tracked as RR-75-04.
- `S-P05`: 2/5 FAIL — expected `focused-trade-off`; observed modes: ['full-composer', 'focused-trade-off', 'focused-trade-off', 'full-composer', 'full-composer']. 3/5 runs under-routed to full-composer (Step 0 trade-off trigger did not fire). Residual-risk tracked as RR-95-02 (supersedes RR-92-02). Phase 94's directed fix (trade-off markers 5→6, SKILL-body.md Step 0 trigger tightening) was the expected lift for this row — the committed verdict is 2/5, an improvement from v6.3's 1/5 but below min-pass. Carry-forward is the legitimate, honesty-not-score outcome (D-01/D-04).

---

## Scores (scores.tsv)

```
id	run	expected	actual	match
S-P01	1	focused-pre-mortem	focused-pre-mortem	1
S-P01	2	focused-pre-mortem	focused-pre-mortem	1
S-P01	3	focused-pre-mortem	focused-pre-mortem	1
S-P01	4	focused-pre-mortem	full-composer	0
S-P01	5	focused-pre-mortem	focused-pre-mortem	1
S-P02	1	focused-inversion	focused-inversion	1
S-P02	2	focused-inversion	full-composer	0
S-P02	3	focused-inversion	full-composer	0
S-P02	4	focused-inversion	full-composer	0
S-P02	5	focused-inversion	full-composer	0
S-P03	1	focused-fishbone	focused-fishbone	1
S-P03	2	focused-fishbone	focused-fishbone	1
S-P03	3	focused-fishbone	full-composer	0
S-P03	4	focused-fishbone	focused-fishbone	1
S-P03	5	focused-fishbone	focused-fishbone	1
S-P04	1	focused-five-whys	focused-five-whys	1
S-P04	2	focused-five-whys	full-composer	0
S-P04	3	focused-five-whys	full-composer	0
S-P04	4	focused-five-whys	focused-five-whys	1
S-P04	5	focused-five-whys	full-composer	0
S-P05	1	focused-trade-off	full-composer	0
S-P05	2	focused-trade-off	focused-trade-off	1
S-P05	3	focused-trade-off	focused-trade-off	1
S-P05	4	focused-trade-off	full-composer	0
S-P05	5	focused-trade-off	full-composer	0
S-P06	1	focused-second-order	focused-second-order	1
S-P06	2	focused-second-order	full-composer	0
S-P06	3	focused-second-order	focused-second-order	1
S-P06	4	focused-second-order	focused-second-order	1
S-P06	5	focused-second-order	full-composer	0
S-N01	1	full-composer	full-composer	1
S-N01	2	full-composer	full-composer	1
S-N01	3	full-composer	focused-pre-mortem	0
S-N01	4	full-composer	full-composer	1
S-N01	5	full-composer	focused-pre-mortem	0
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
S-N04	1	full-composer	full-composer	1
S-N04	2	full-composer	full-composer	1
S-N04	3	full-composer	focused-pre-mortem	0
S-N04	4	full-composer	full-composer	1
S-N04	5	full-composer	full-composer	1
S-P07	1	focused-pre-mortem	full-composer	0
S-P07	2	focused-pre-mortem	focused-pre-mortem	1
S-P07	3	focused-pre-mortem	full-composer	0
S-P07	4	focused-pre-mortem	focused-pre-mortem	1
S-P07	5	focused-pre-mortem	full-composer	0
S-P08	1	focused-pre-mortem	full-composer	0
S-P08	2	focused-pre-mortem	full-composer	0
S-P08	3	focused-pre-mortem	full-composer	0
S-P08	4	focused-pre-mortem	full-composer	0
S-P08	5	focused-pre-mortem	full-composer	0
```

---

## Lineage

This baseline records the Phase 95 live re-baseline of Step 0 technique selection
against the Phase 94 directed-fix detector+agent-body (`scripts/_battery_core.py`,
capture-backed `_TECHNIQUE_CATEGORIES` markers — inversion strengthened 7→9,
trade-off strengthened 5→6 — `MIN_HEADER_HITS=2`, `_COMPOSER_FOCUS_CEILING=4`
unchanged). Phase 94 applied a directed fix to the S-P02 (inversion) and S-P05
(trade-off) pipeline: additive `_TECHNIQUE_CATEGORIES` markers plus Step 0 trigger
tightening in `shared/spine/SKILL-body.md` (D-03 deviation, approved). This run
measures the expected lift; honesty-not-score (D-01) governs the committed verdict.

**Phase 94 as expectation-not-verdict (D-04):** Phase 94's directed fix was the
expected source of improvement for RR-92-01 (S-P02 inversion) and RR-92-02 (S-P05
trade-off). The expectation was that both rows would improve, possibly to CLOSED
(≥3/5). The committed verdict from this single authoritative run is: S-P02 1/5
(+1 vs. v6.3's 0/5, below min-pass) and S-P05 2/5 (+1 vs. v6.3's 1/5, below
min-pass). Both rows carry forward under freshly-minted superseding RR-95-NN IDs.
The CLOSED bar remains exactly ≥3/5; no result was forced or masked.

**Residual resolution (D-03):**
- **RR-95-01** (S-P02 focused-inversion, supersedes RR-92-01): CARRIED FORWARD at
  1/5. Supersession chain: RR-75-NN → RR-79-02 → RR-92-01 → **RR-95-01**.
- **RR-95-02** (S-P05 focused-trade-off, supersedes RR-92-02): CARRIED FORWARD at
  2/5. Supersession chain: RR-75-NN → RR-79-03 → RR-92-02 → **RR-95-02**.

**Previously resolved residuals (re-measured; no new action required):**
- RR-79-01 (S-P01 pre-mortem): CLOSED at v6.3 (3/5); v6.4 re-measurement = 4/5 PASS (stable).
- RR-80-01 (S-N04 full-composer): CLOSED at v6.3 (4/5); v6.4 re-measurement = 4/5 PASS (stable).

Successor note: RR-79-02 (S-P02 inversion) superseded by RR-92-01 (Phase 93);
RR-92-01 in turn superseded by RR-95-01 (Phase 95, this baseline). RR-79-03 (S-P05
trade-off) superseded by RR-92-02 (Phase 93); RR-92-02 in turn superseded by
RR-95-02 (Phase 95, this baseline). The conditional RR-95-NN mints are recorded in
the RR_ID_MAP update in `scripts/check-step0-live.py` (Commit 2, post-run finalize,
per D-02/D-03).

Prior baseline: tests/step0-baseline-v6.3.md (Phase 92) — BATTERY: FAIL,
P 4/6 (S-P01-06), S-N 4/4; residuals RR-92-01 (S-P02 0/5) + RR-92-02 (S-P05 1/5) carried forward.
