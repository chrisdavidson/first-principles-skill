# Step 0 Live Harness Baseline — v8.5

**Recorded:** 2026-07-20T14:20:12Z (25 live `claude` invocations: 5 prompts × 5 repeats)
**Script version:** `scripts/check-step0-live.py` (commit `cf7435d`)
**Core version:** `scripts/_battery_core.py` (commit `5cd4537`)
**Fixture version:** `tests/step0-fixture-catalog.md` (commit `02fd820`)
**Agent version:** `first-principles/agents/first-principles.md` (commit `8c3411c`)
**Run flags:** `--repeat 5 --min-pass 3`
**Run cwd:** `/tmp` (out-of-repo — see Methodology notes)
**Baseline verdict:** BATTERY: FAIL
**Summary:** P 1/5 (5-technique canonical bar: S-P01–06 + S-P10 estimate, S-P14 theoretical-limit) | S-N 0/0 | S-P07/08/11/12/13/15 expected-FAIL (context-free / alternation falsifiers, excluded from the bar) | S-P16 merge-validation (outside /8): N/A/N/A (not measured this run)

---

## Per-prompt results

| ID | Expected MODE | K/N | Verdict |
|----|---------------|-----|---------|
| S-P03 | focused-fishbone | 3/5 PASS | PASS |
| S-P02 | focused-inversion | 0/5 FAIL | FAIL |
| S-P04 | focused-five-whys | 0/5 FAIL | FAIL |
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
OUT_DIR=/tmp/step0-live-v8.5-$(date -u +%Y%m%dT%H%M%SZ)
cd /tmp && python3 "$REPO/scripts/check-step0-live.py" \
  --catalog "$REPO/tests/step0-fixture-catalog.md" \
  --plugin-dir "$REPO/first-principles" \
  --repeat 5 --min-pass 3 \
  --out "$OUT_DIR" \
  --baseline "$REPO/tests/step0-baseline-v8.5.md"
```

**Run date:** 2026-07-20T14:20:12Z

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

- `S-P02`: 0/5 FAIL — expected `focused-inversion`; observed modes: ['full-composer', 'focused-second-order', 'full-composer', 'full-composer', 'full-composer']. Residual-risk tracked as RR-114-01.
- `S-P04`: 0/5 FAIL — expected `focused-five-whys`; observed modes: ['full-composer', 'full-composer', 'full-composer', 'full-composer', 'full-composer']. Residual-risk tracked as RR-75-04.
- `S-P10`: 0/5 FAIL — expected `focused-estimate`; observed modes: ['full-composer', 'full-composer', 'full-composer', 'full-composer', 'full-composer']. Residual-risk tracked as RR-108-04.
- `S-P14`: 0/5 FAIL — expected `focused-theoretical-limit`; observed modes: ['full-composer', 'full-composer', 'full-composer', 'full-composer', 'full-composer']. Residual-risk tracked as RR-108-05.

---

## Scores (scores.tsv)

```
id	run	expected	actual	match
S-P03	1	focused-fishbone	focused-fishbone	1
S-P03	2	focused-fishbone	focused-fishbone	1
S-P03	3	focused-fishbone	full-composer	0
S-P03	4	focused-fishbone	full-composer	0
S-P03	5	focused-fishbone	focused-fishbone	1
S-P02	1	focused-inversion	full-composer	0
S-P02	2	focused-inversion	focused-second-order	0
S-P02	3	focused-inversion	full-composer	0
S-P02	4	focused-inversion	full-composer	0
S-P02	5	focused-inversion	full-composer	0
S-P04	1	focused-five-whys	full-composer	0
S-P04	2	focused-five-whys	full-composer	0
S-P04	3	focused-five-whys	full-composer	0
S-P04	4	focused-five-whys	full-composer	0
S-P04	5	focused-five-whys	full-composer	0
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

This baseline records the Phase 156 v8.5 **affected-technique re-measure** of five Step 0
rows via a filtered temp catalog: S-P02 inversion, S-P03 fishbone, S-P04 five-whys,
S-P10 estimate, S-P14 theoretical-limit (5 rows x 5 repeats = 25 invocations).
S-P02 inversion is the **unsplit control** — its reference file was never split, so
movement in that row indicates drift or run-to-run noise rather than a split effect.
The four remaining rows correspond to the four techniques whose reference files Phase 154
split (five-whys, theoretical-limit, estimate, fishbone).

This is a **measurement-only**, **cap-defensive** re-measure: there is NO detector change
and NO agent-body change this milestone. The agent body is measured **as-shipped**
(post Phase 154/155 split) and the detector `scripts/_battery_core.py` is **frozen**
(`_TECHNIQUE_CATEGORIES` unchanged — inversion 13 markers, trade-off 10 markers, fishbone 7
markers, pre-mortem 9 markers — `MIN_HEADER_HITS=2`, `_COMPOSER_FOCUS_CEILING=4`
byte-unchanged). Honesty-not-score (D-01) governs the committed verdict; the falsifiable
criterion is applied at a blocking human checkpoint, not forced.
`tests/step0-baseline-v7.8.md` remains the canonical full 8-technique Step 0 baseline;
this file is an affected-technique delta only. The BATTERY verdict is therefore N/A as a
full 8-technique signal — it reflects only the five measured rows.

Floor provenance is mixed by row (D-04), because `tests/step0-baseline-v7.13.md` is a
three-row residual-delta baseline that does not contain the fishbone or five-whys rows:
S-P02 inversion, S-P10 estimate, and S-P14 theoretical-limit are judged against
`tests/step0-baseline-v7.13.md`; S-P03 fishbone and S-P04 five-whys are judged against
`tests/step0-baseline-v7.11.md`.

Residual IDs re-measured this run: RR-114-01 (S-P02 inversion, v7.13 live 1/5), RR-108-04
(S-P10 estimate, v7.13 live 0/5), RR-108-05 (S-P14 theoretical-limit, v7.13 live 0/5) —
each CLOSED at its observed K/N if it reaches min-pass (>=3/5), or CARRIED; ID kept either
way, no Phase 156 successor ID minted. RR-117-01 (S-P03 fishbone) is re-measured against
its v7.11 4/5 floor. S-P04 five-whys carries only the infra-only map entry RR-75-04 and has
no sentinel. The re-measure of RR-108-04 and RR-108-05 is authorized by
docs/v8.5-byte-freeze-relaxation.md, which narrowly re-opened exactly those two residuals'
disposition.

Prior baseline: tests/step0-baseline-v7.13.md (Phase 137 residual-delta re-measure,
3 rows: S-P02, S-P10, S-P14) and tests/step0-baseline-v7.11.md (Phase 128-129
whole-system re-measure, 29 S-P/S-N rows) — the two floor sources this run judges against.
