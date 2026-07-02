# Step 0 Live Harness Baseline — v7.13

**Recorded:** 2026-07-02T11:25:00Z (15 live `claude` invocations: 3 prompts × 5 repeats)
**Script version:** `scripts/check-step0-live.py` (commit `dc878d5`)
**Core version:** `scripts/_battery_core.py` (commit `8c7c117`)
**Fixture version:** `tests/step0-fixture-catalog.md` (commit `02fd820`)
**Agent version:** `first-principles/agents/first-principles.md` (commit `ef22988`)
**Run flags:** `--repeat 5 --min-pass 3`
**Run cwd:** `/tmp` (out-of-repo — see Methodology notes)
**Baseline verdict:** BATTERY: FAIL
**Summary:** P 0/8 (8-technique canonical bar: S-P01–06 + S-P10 estimate, S-P14 theoretical-limit) | S-N 0/0 | S-P07/08/11/12/13/15 expected-FAIL (context-free / alternation falsifiers, excluded from the bar) | S-P16 merge-validation (outside /8): N/A/N/A (not measured this run)

> **RESIDUAL-DELTA baseline (Phase 137).** This baseline records 3 rows ONLY:
> S-P02 inversion (RR-114-01), S-P10 estimate (RR-108-04), S-P14 theoretical-limit (RR-108-05).
> `tests/step0-baseline-v7.8.md` remains the canonical full Step 0 baseline.
> The BATTERY verdict is N/A as a full 8-technique signal — it reflects only the 3 measured residuals (D-01b).

---

## Per-prompt results

| ID | Expected MODE | K/N | Verdict |
|----|---------------|-----|---------|
| S-P02 | focused-inversion | 1/5 FAIL | FAIL |
| S-P10 | focused-estimate | 0/5 FAIL | FAIL |
| S-P14 | focused-theoretical-limit | 0/5 FAIL | FAIL |

### Verdict-cell schema

Each row's K/N cell uses the falsifiable `<n>/N PASS|FAIL` format (matching the
`routing-battery-baseline-v4.3.md` convention). A row showing `<n>/5 FAIL`
does NOT satisfy the gate. `PASS` means `match_count >= min_pass`.
`FAIL` means `match_count < min_pass`.

---

## How this baseline was produced

```bash
REPO=/path/to/first-principles-skills
OUT_DIR=/tmp/step0-live-v7.13-$(date -u +%Y%m%dT%H%M%SZ)
cd /tmp && python3 "$REPO/scripts/check-step0-live.py" \
  --catalog "$REPO/tests/step0-fixture-catalog.md" \
  --plugin-dir "$REPO/first-principles" \
  --repeat 5 --min-pass 3 \
  --out "$OUT_DIR" \
  --baseline "$REPO/tests/step0-baseline-v7.13.md"
```

**Run date:** 2026-07-02T11:25:00Z

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

- `S-P02`: 1/5 FAIL — expected `focused-inversion`; observed modes: ['full-composer', 'full-composer', 'focused-inversion', 'full-composer', 'full-composer']. Residual-risk tracked as RR-114-01.
- `S-P10`: 0/5 FAIL — expected `focused-estimate`; observed modes: ['full-composer', 'full-composer', 'full-composer', 'full-composer', 'full-composer']. Residual-risk tracked as RR-108-04.
- `S-P14`: 0/5 FAIL — expected `focused-theoretical-limit`; observed modes: ['full-composer', 'full-composer', 'full-composer', 'full-composer', 'full-composer']. Residual-risk tracked as RR-108-05.

---

## Scores (scores.tsv)

```
id	run	expected	actual	match
S-P02	1	focused-inversion	full-composer	0
S-P02	2	focused-inversion	full-composer	0
S-P02	3	focused-inversion	focused-inversion	1
S-P02	4	focused-inversion	full-composer	0
S-P02	5	focused-inversion	full-composer	0
S-P10	1	focused-estimate	full-composer	0
S-P10	2	focused-estimate	full-composer	0
S-P10	3	focused-estimate	full-composer	0
S-P10	4	focused-estimate	full-composer	0
S-P10	5	focused-estimate	full-composer	0
S-P14	1	focused-theoretical-limit	full-composer	0
S-P14	2	focused-theoretical-limit	full-composer	0
S-P14	3	focused-theoretical-limit	full-composer	0
S-P14	4	focused-theoretical-limit	full-composer	0
S-P14	5	focused-theoretical-limit	full-composer	0
```

---

## Lineage

This baseline records the Phase 137 v7.13 **residual-delta re-measure** of three deferred Step 0 residuals
(S-P02 inversion, S-P10 estimate, S-P14 theoretical-limit) via a filtered temp catalog.
This is a **measurement-only**, **cap-defensive** re-measure (3 rows × 5 repeats = 15 invocations):
there is NO detector change and NO agent-body change this milestone. The agent body is
measured **as-shipped (v7.12)** and the detector `scripts/_battery_core.py` is **frozen**
(`_TECHNIQUE_CATEGORIES` unchanged — inversion 13 markers, trade-off 10 markers
(post-Phase-121 OCH-02) — `MIN_HEADER_HITS=2`, `_COMPOSER_FOCUS_CEILING=4` byte-unchanged).
Honesty-not-score (D-01) governs the committed verdict; the falsifiable criterion is applied
at a blocking human checkpoint, not forced. `tests/step0-baseline-v7.8.md` remains the
canonical full Step 0 baseline; this file is a residual-delta only (D-05).
The BATTERY verdict is N/A as a full 8-technique signal — it reflects only the 3 measured
residuals (D-01b). S-A excluded from live run.

Three carried residuals re-measured in this run: RR-114-01
(S-P02 inversion, v7.6 live 1/5; RESOLVED-STRUCTURALLY-OFFLINE Phase 121 OCH-02;
live pass-rate re-measure this run), RR-108-04 (S-P10 estimate, v7.6
spend-limit-indeterminate), RR-108-05 (S-P14 theoretical-limit, v7.6
spend-limit-indeterminate). Each is CLOSED at its observed K/N if it reaches
min-pass (≥3/5), or CARRIED FORWARD; ID kept in either case (D-03/D-09
CLOSE-keeps-ID — no phase-137 successor RR ID minted).

Prior baseline: tests/step0-baseline-v7.11.md (Phase 128-129 whole-system re-measure) — BATTERY: PASS,
29 S-P/S-N rows measured (S-A excluded); residuals
RR-114-01 (S-P02 inversion, CARRIED — structural offline resolution Phase 121),
RR-108-04 (S-P10 estimate, CARRIED-indeterminate), RR-108-05 (S-P14 theoretical-limit,
CARRIED-indeterminate) carried forward into this v7.13 run.

---

## Residual Dispositions (v7.13)

Disposition applied per D-02 (K/N ≥ 3/5 → CLOSED; below → CARRIED keeping the existing RR ID per
D-03/D-09 CLOSE-keeps-ID — no phase-137 successor RR ID minted). Human-confirmed at the Phase 137
blocking checkpoint (honesty-not-score, D-01). The `_load_excerpt_v713` BATT-06 sentinel re-point
is deferred to Phase 138.

| Prompt | Technique | v7.13 K/N | Disposition | RR ID (kept) |
|--------|-----------|-----------|-------------|--------------|
| S-P02 | inversion | 1/5 FAIL | CARRIED (1/5 < 3/5) | RR-114-01 |
| S-P10 | estimate | 0/5 FAIL | CARRIED (0/5 < 3/5) | RR-108-04 |
| S-P14 | theoretical-limit | 0/5 FAIL | CARRIED (0/5 < 3/5) | RR-108-05 |
