# Step 0 Live Harness Baseline — v5.0

**Recorded:** 2026-06-12T14:24:14Z (60 live `claude` invocations: 12 prompts × 5 repeats)
**Script version:** `scripts/check-step0-live.py` (commit `5d0af40`)
**Core version:** `scripts/_battery_core.py` (commit `59e2118`)
**Fixture version:** `tests/step0-fixture-catalog.md` (commit `4047591`)
**Agent version:** `first-principles/agents/first-principles.md` (commit `c35e3bb`)
**Run flags:** `--repeat 5 --min-pass 3`
**Run cwd:** `/tmp` (out-of-repo — see Methodology notes)
**Baseline verdict:** BATTERY: FAIL
**Summary:** P 0/8 | N 4/4; overall FAIL

---

## Per-prompt results

| ID | Expected MODE | K/N | Verdict |
|----|---------------|-----|---------|
| S-P01 | focused-pre-mortem | 0/5 FAIL | FAIL |
| S-P02 | focused-inversion | 0/5 FAIL | FAIL |
| S-P03 | focused-fishbone | 2/5 FAIL | FAIL |
| S-P04 | focused-five-whys | 0/5 FAIL | FAIL |
| S-P05 | focused-trade-off | 2/5 FAIL | FAIL |
| S-P06 | focused-second-order | 0/5 FAIL | FAIL |
| S-N01 | full-composer | 4/5 PASS | PASS |
| S-N02 | full-composer | 5/5 PASS | PASS |
| S-N03 | full-composer | 5/5 PASS | PASS |
| S-N04 | full-composer | 5/5 PASS | PASS |
| S-P07 | focused-pre-mortem | 1/5 FAIL | FAIL |
| S-P08 | focused-pre-mortem | 0/5 FAIL | FAIL |

### Verdict-cell schema

Each row's K/N cell uses the falsifiable `<n>/N PASS|FAIL` format (matching the
`routing-battery-baseline-v4.3.md` convention). A row showing `<n>/5 FAIL`
does NOT satisfy the gate. `PASS` means `match_count >= min_pass`.
`FAIL` means `match_count < min_pass`.

---

## How this baseline was produced

```bash
REPO=/path/to/first-principles-skills
OUT_DIR=/tmp/step0-live-v5.0-$(date -u +%Y%m%dT%H%M%SZ)
cd /tmp && python3 "$REPO/scripts/check-step0-live.py" \
  --catalog "$REPO/tests/step0-fixture-catalog.md" \
  --plugin-dir "$REPO/first-principles" \
  --repeat 5 --min-pass 3 \
  --out "$OUT_DIR" \
  --baseline "$REPO/tests/step0-baseline-v5.0.md"
```

**Run date:** 2026-06-12T14:24:14Z

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

- `S-P01`: 0/5 FAIL — expected `focused-pre-mortem`; observed modes: ['full-composer', 'full-composer', 'full-composer', 'full-composer', 'full-composer']. Residual-risk tracked as S-P01-RR01.
- `S-P02`: 0/5 FAIL — expected `focused-inversion`; observed modes: ['full-composer', 'full-composer', 'full-composer', 'full-composer', 'full-composer']. Residual-risk tracked as S-P02-RR01.
- `S-P03`: 2/5 FAIL — expected `focused-fishbone`; observed modes: ['focused-fishbone', 'full-composer', 'focused-fishbone', 'full-composer', 'full-composer']. Residual-risk tracked as S-P03-RR01.
- `S-P04`: 0/5 FAIL — expected `focused-five-whys`; observed modes: ['full-composer', 'full-composer', 'full-composer', 'full-composer', 'full-composer']. Residual-risk tracked as S-P04-RR01.
- `S-P05`: 2/5 FAIL — expected `focused-trade-off`; observed modes: ['full-composer', 'full-composer', 'full-composer', 'focused-trade-off', 'focused-trade-off']. Residual-risk tracked as S-P05-RR01.
- `S-P06`: 0/5 FAIL — expected `focused-second-order`; observed modes: ['full-composer', 'full-composer', 'full-composer', 'full-composer', 'full-composer']. Residual-risk tracked as S-P06-RR01.
- `S-P07`: 1/5 FAIL — expected `focused-pre-mortem`; observed modes: ['focused-pre-mortem', 'full-composer', 'full-composer', 'full-composer', 'full-composer']. Residual-risk tracked as S-P07-RR01.
- `S-P08`: 0/5 FAIL — expected `focused-pre-mortem`; observed modes: ['full-composer', 'full-composer', 'full-composer', 'full-composer', 'full-composer']. Residual-risk tracked as S-P08-RR01.

**Root-cause analysis (S-P side, added after Pitfall-1 bypass-gate inspection).**
The S-P01 bypass gate tripped (0/5), so per the plan's Pitfall 1 the captures were
inspected before recording. The S-P `0/8` result is **not a clean Step-0 routing
measurement** — it is dominated by two harness-side classification artifacts and
should be read as a known residual risk, not as evidence that focused routing is
broken:

1. **Context-free prompts trigger clarification, not the technique.** The S-P
   fixtures are bare technique commands with no subject to analyze (e.g. S-P01
   "run a pre-mortem on this launch", S-P04 "do a five whys on this outage",
   S-P06/S-P08). With no facts and `AskUserQuestion` unavailable from `/tmp`, the
   live agent correctly **asks for the missing context** instead of fabricating a
   technique. The detector returns `none`, and the `none`+dispatch inference then
   labels the clarification `full-composer`. Verified in the S-P01/S-P04/S-P06/S-P08
   captures (each is a "the agent needs X before it can run…" response).
2. **Detector false-negatives on genuine focused output.** In at least one case the
   agent **did** run the technique but was still scored `none`→`full-composer`:
   S-P02-run1 produced a real inversion ("## Claim, inverted … ## Why the inversion
   holds") yet `detect_output_structure_from_file` did not recognize its markers.
   The detector fires only intermittently and format-sensitively (S-P03 2/5,
   S-P05 2/5, S-P07 1/5), confirming marker coverage — not routing — is the
   limiter.

**Why this is not fixed in Phase 72 (scope).** A real fix means broadening the
focused-marker detector (which lives in `scripts/_battery_core.py` — untouchable
here under D-02) and/or giving the S-P fixtures concrete context like the S-N rows
(the catalog is a locked Phase-70 artifact). Both are out of scope for this phase
and the v5.0 milestone hard constraints. Tracked as a deferred follow-up
(**S-P-RR-DETECTOR**): "live focused-technique detection under-counts — broaden
`detect_output_structure_from_file` markers and/or add context to S-P fixtures,
then re-baseline." The S-N inference side (the milestone's D-01 root-cause finding)
is unaffected and confirmed (4/4).

---

## Scores (scores.tsv)

```
id	run	expected	actual	match
S-P01	1	focused-pre-mortem	full-composer	0
S-P01	2	focused-pre-mortem	full-composer	0
S-P01	3	focused-pre-mortem	full-composer	0
S-P01	4	focused-pre-mortem	full-composer	0
S-P01	5	focused-pre-mortem	full-composer	0
S-P02	1	focused-inversion	full-composer	0
S-P02	2	focused-inversion	full-composer	0
S-P02	3	focused-inversion	full-composer	0
S-P02	4	focused-inversion	full-composer	0
S-P02	5	focused-inversion	full-composer	0
S-P03	1	focused-fishbone	focused-fishbone	1
S-P03	2	focused-fishbone	full-composer	0
S-P03	3	focused-fishbone	focused-fishbone	1
S-P03	4	focused-fishbone	full-composer	0
S-P03	5	focused-fishbone	full-composer	0
S-P04	1	focused-five-whys	full-composer	0
S-P04	2	focused-five-whys	full-composer	0
S-P04	3	focused-five-whys	full-composer	0
S-P04	4	focused-five-whys	full-composer	0
S-P04	5	focused-five-whys	full-composer	0
S-P05	1	focused-trade-off	full-composer	0
S-P05	2	focused-trade-off	full-composer	0
S-P05	3	focused-trade-off	full-composer	0
S-P05	4	focused-trade-off	focused-trade-off	1
S-P05	5	focused-trade-off	focused-trade-off	1
S-P06	1	focused-second-order	full-composer	0
S-P06	2	focused-second-order	full-composer	0
S-P06	3	focused-second-order	full-composer	0
S-P06	4	focused-second-order	full-composer	0
S-P06	5	focused-second-order	full-composer	0
S-N01	1	full-composer	focused-pre-mortem	0
S-N01	2	full-composer	full-composer	1
S-N01	3	full-composer	full-composer	1
S-N01	4	full-composer	full-composer	1
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
S-N04	1	full-composer	full-composer	1
S-N04	2	full-composer	full-composer	1
S-N04	3	full-composer	full-composer	1
S-N04	4	full-composer	full-composer	1
S-N04	5	full-composer	full-composer	1
S-P07	1	focused-pre-mortem	focused-pre-mortem	1
S-P07	2	focused-pre-mortem	full-composer	0
S-P07	3	focused-pre-mortem	full-composer	0
S-P07	4	focused-pre-mortem	full-composer	0
S-P07	5	focused-pre-mortem	full-composer	0
S-P08	1	focused-pre-mortem	full-composer	0
S-P08	2	focused-pre-mortem	full-composer	0
S-P08	3	focused-pre-mortem	full-composer	0
S-P08	4	focused-pre-mortem	full-composer	0
S-P08	5	focused-pre-mortem	full-composer	0
```

---

## Lineage

This baseline establishes the first live K-of-N measurement of Step 0 technique
selection. It covers all 12 rows of `tests/step0-fixture-catalog.md` (S-P01–S-P08,
S-N01–S-N04) using approach-② bypass (`_wrap_for_bypass`) over the Plan-36-locked
transport, measured by `detect_output_structure_from_file` with the harness-side
`_classify_mode` inference wrapper (D-01/D-02 fix).

Prior measurement: Phase 71 spike (`scripts/check-step0-live-spike.py`) — 2-fixture
proof of approach ②, renamed in place to this script (D-04).
