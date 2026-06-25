# Step 0 Live Harness Baseline — v7.7 (revised CONF-01)

**Recorded:** 2026-06-24T23:41:50Z (30 live `claude` invocations: 6 prompts × 5 repeats — full run, NOT truncated)
**Script version:** `scripts/check-step0-live.py` (commit `086f7b2`)
**Core version:** `scripts/_battery_core.py` (commit `fba3662`)
**Fixture version:** `tests/step0-fixture-catalog.md` (commit `086f7b2`)
**Agent version:** `first-principles/agents/first-principles.md` (commit `a60393e`)
**Run flags:** `--repeat 5 --min-pass 3 --priority S-P01 S-P03 S-N01 S-N02 S-N03` (no `--baseline`)
**Run cwd:** `/tmp` (out-of-repo — see Methodology notes)
**Baseline verdict:** BATTERY: FAIL
**D-17 verdict:** **SHORT OF BAR** (positives confirmed; 2 of 3 blocking oblique negatives fail — but the failing negatives are transcript-confirmed genuine pre-mortem routing on semantically-pre-mortem prompts, not a fix defect)
**Summary:** Positives **S-P01 3/5 PASS, S-P03 5/5 PASS** (both meet their v7.4 floors — the FIX-01 detector recalibration confirmed out-of-sample). Blocking oblique negatives **S-N01 0/5 FAIL, S-N02 2/5 FAIL, S-N03 5/5 PASS** (1/3 hold). Non-blocking **S-N04 2/5** (reported). Human verdict at the blocking checkpoint (D-17, honesty-not-score D-13): **record the honest short-of-bar baseline and proceed** — markers were NOT tuned and the run was NOT repeated to chase a score.

---

## D-17 revised criterion + verdict (CONF-01)

This is the **Phase 117 revised CONF-01** live confirmation of the FIX-01/FIX-02 detector
recalibration (pre-mortem markers 7→9, fishbone 6→7; the trigger-phrase sync at
`shared/spine/SKILL-body.md` rows 30/33). It re-samples the two on-trigger **positives in a
fresh run** (the markers were calibrated on the *old* frozen v7.6 captures, so re-sampling here
is the genuine out-of-sample test) and measures the genuinely-oblique **S-N01/S-N02/S-N03** as
the blocking negative controls, with **S-N04** measured but non-blocking
(`NON_BLOCKING_NEGATIVE_IDS`, D-16). It supersedes the first CONF-01 attempt (Plan 117-03), which
measured only S-N04 and paused.

**D-17 criterion (D-07′):** S-P01 ≥ 3/5 **AND** S-P03 ≥ 3/5 (their v7.4 floors) **AND**
S-N01 / S-N02 / S-N03 each stay full-composer ≥ 3/5 → fix confirmed. S-N04 reported, not a gate.

| Row | Technique / role | v7.4 floor | **v7.7 (post-fix)** | D-17 conjunct |
|-----|------------------|:---:|:---:|:---:|
| S-P01 | pre-mortem (positive) | 3/5 | **3/5 PASS** | ✓ holds |
| S-P03 | fishbone (positive) | 3/5 | **5/5 PASS** | ✓ holds |
| S-N01 | oblique negative (blocking) | (full-composer) | **0/5 FAIL** | ✗ fails |
| S-N02 | oblique negative (blocking) | (full-composer) | **2/5 FAIL** | ✗ fails |
| S-N03 | oblique negative (blocking) | (full-composer) | **5/5 PASS** | ✓ holds |
| S-N04 | semantically-pre-mortem (non-blocking) | (full-composer) | **2/5** | reported, not a gate |

**Verdict: SHORT OF BAR.** The two positive conjuncts hold (the fix works out-of-sample);
the blocking-negative conjunct fails because S-N01 (0/5) and S-N02 (2/5) over-route to
focused-pre-mortem.

### Why the negative failures are genuine routing, not a fix defect (transcript-grounded)

S-N01 (*"…surface every way this could blow up"*), S-N02 (*"…figure out everything that would
make it go wrong"*) and S-N04 (*"…walk through how this could go badly — what failure modes…"*)
are all **semantically pre-mortem requests in natural language**, and the live first-principles
agent **genuinely selects a focused pre-mortem** on them — exactly the discovery that triggered
the first re-scope for S-N04 (Plan 117-03), now shown to apply to S-N01/S-N02 as well. The
transcripts are explicit:

- **S-N01-run1:** *"I invoked the first-principles agent… It's ready to run a full pre-mortem…
  assume it's already failed six months out, work backwards… cluster those into the structural
  weaknesses…"* — pre-mortem selected.
- **S-N02-run1 / S-N04-run1:** both transcripts literally say *"The first-principles agent ran a
  full pre-mortem"* — yet only **1** distinct marker landed in the short orchestrator-summary
  text, so the detector scored these `full-composer` (a detector **under-count "pass"**). The
  S-N02 2/5 and S-N04 2/5 therefore **overstate** the negatives: the agent ran pre-mortems even
  on the "passing" runs.
- **S-N03** (*"my Python script crashes on startup… what could be wrong with my error
  handling"*) — a debugging request, **not** a pre-mortem: **0** pre-mortem markers on all 5
  runs, full-composer **5/5**. This is the one genuinely-oblique negative, and it passes cleanly
  — the real precision signal that the fix does **not** hurt routing on genuinely-unrelated
  prompts.

The honest read: the fix lands its target behaviors; the "blocking-negative" failures reflect the
negative-control **set being mis-chosen** (S-N01/S-N02 are pre-mortem-adjacent, like S-N04), not
a precision regression introduced by FIX-01. The over-routing reproduces **even with FIX-01
reverted** (the 117-03 finding: S-N04 ~1/5 without the fix). Per D-13 this honest measurement is
the deliverable; the negative-control redesign (e.g. moving S-N01/S-N02 into
`NON_BLOCKING_NEGATIVE_IDS` alongside S-N04) is a candidate follow-up, not authorized here.

### Live `_technique_hits` count vectors (the CONF-02 sentinel hand-off → Plan 117-07)

Distinct-marker counts per run over the frozen `tests/step0-captures-v7.7/` excerpts
(`MIN_HEADER_HITS = 2`; a run routes focused when its count ≥ 2):

- **S-P01 pre-mortem:** `[0, 2, 3, 1, 4]` (runs 2,3,5 clear the barrier → 3/5)
- **S-P03 fishbone:** `[3, 3, 2, 2, 2]` (all 5 clear → 5/5)
- **S-N01 pre-mortem:** `[3, 3, 3, 2, 2]` (all 5 clear → over-routes 5/5 → 0/5 full-composer)
- **S-N02 pre-mortem:** `[1, 3, 2, 1, 3]` (runs 2,3,5 clear → over-routes 3/5 → 2/5 full-composer)
- **S-N03 pre-mortem:** `[0, 0, 0, 0, 0]` (none clear → full-composer 5/5)
- **S-N04 pre-mortem:** `[1, 2, 2, 1, 3]` (runs 2,3,5 clear → over-routes 3/5 → 2/5 full-composer)

**Residual-disposition signals for Plan 117-07 (CONF-02):**
- **S-P01 (RR-79-01):** sustained at 3/5 (= v7.4 floor, clears min-pass) → **CLOSE candidate**
  (the pre-mortem under-routing residual is resolved by the fix; 117-07 decides CLOSE vs carry).
- **S-P03 fishbone:** 5/5 with vector `[3,3,2,2,2]` → mint a **new S-P03 fishbone count-vector
  sentinel**; the fishbone under-routing residual (RR-75-03 lineage) is a CLOSE candidate.
- **S-N01/S-N02/S-N04:** transcript-confirmed genuine pre-mortem routing → 117-07 may add an
  S-N01/02/03 **precision sentinel** if warranted (S-N03 0-vector is the clean anchor).
- **RR-114-01 (S-P02 inversion):** out of scope this run — **carried untouched**.

---

## Per-prompt results

| ID | Expected MODE | K/N | Verdict |
|----|---------------|-----|---------|
| S-P01 | focused-pre-mortem | 3/5 PASS | PASS (positive — fix confirmed out-of-sample) |
| S-P03 | focused-fishbone | 5/5 PASS | PASS (positive — fix confirmed out-of-sample) |
| S-N01 | full-composer | 0/5 FAIL | FAIL (blocking — genuine pre-mortem routing on a semantically-pre-mortem prompt) |
| S-N02 | full-composer | 2/5 FAIL | FAIL (blocking — genuine pre-mortem routing; the 2 "passes" are detector under-counts) |
| S-N03 | full-composer | 5/5 PASS | PASS (blocking — the one truly-oblique negative; agent correctly does not run a pre-mortem) |
| S-N04 | full-composer | 2/5 | NON-BLOCKING (`NON_BLOCKING_NEGATIVE_IDS`, D-16 — reported, excluded from the bar) |

### Verdict-cell schema

Each row's K/N cell uses the falsifiable `<n>/N PASS|FAIL` format. `PASS` means
`match_count >= min_pass` (3/5); `FAIL` means `match_count < min_pass`. True observed K/N is
recorded; a forced PASS is never written (D-13).

---

## How this baseline was produced

```bash
REPO=/path/to/first-principles-skills
# Restricted 6-row catalog (prompts byte-identical to tests/step0-fixture-catalog.md
# rows 38/40/44/45/46/47 — S-P01, S-P03, S-N01, S-N02, S-N03, S-N04):
CAT=/tmp/step0-v7.7-conf01-catalog.md
OUT_DIR=/tmp/step0-v7.7-conf01-$(date -u +%Y%m%dT%H%M%SZ)
cd /tmp && python3 "$REPO/scripts/check-step0-live.py" \
  --catalog "$CAT" \
  --plugin-dir "$REPO/first-principles" \
  --repeat 5 --min-pass 3 \
  --priority S-P01 S-P03 S-N01 S-N02 S-N03 \
  --out "$OUT_DIR"
# NO --baseline — this doc was written by the orchestrator (Plan 117-06, inline) from the
# recorded scores, not by the harness's --baseline emitter.
```

**Run date:** 2026-06-24T23:41:50Z · **Source /tmp dir:** `/tmp/step0-v7.7-conf01-20260624T234150Z`
(ephemeral) · raw `.jsonl` + `scores.tsv` + `harness.log` preserved provisionally under the
gitignored `.planning/phases/117-…/conf01-rev-evidence/`.

---

## Methodology notes

**Why run from `/tmp`.** When run from the project root, the orchestrator's sub-agent may discover
`.planning/` and plugin context, enriching its response with project-specific artifacts. Running
from `/tmp` ensures the full-composer mode responds to the verbatim prompt only, matching every
prior Step 0 baseline.

**Why `--plugin-dir` must be an absolute path.** The script is invoked from `/tmp`; a relative
path would resolve against `/tmp`. The harness default resolves `REPO_ROOT/first-principles` via
`__file__` (cwd-independent); an explicit absolute path was passed for parity with the documented
usage.

**Why `_classify_mode` infers `full-composer` from `none` + dispatch evidence.** When
`detect_output_structure_from_file` returns `none` but the capture shows
`Agent(subagent_type="first-principles:first-principles")` was dispatched, the sub-agent ran the
full-composer path but produced a non-structured response. The dispatch itself proves Step 0 chose
the full-composer path. This inference is applied only in the Step 0 harness; `_battery_core.py`
is not modified.

**S-N04 non-blocking rationale (D-16), extended to S-N01/S-N02.** S-N04 stays a catalog negative at
the emulator/phrase-table layer (it fires NO Step 0 trigger phrase — STEP0-08 unchanged) but is
excluded from the blocking live negative bar via `NON_BLOCKING_NEGATIVE_IDS` because the live agent
genuinely routes its semantically-pre-mortem phrasing to a focused pre-mortem. This run shows the
same phenomenon for S-N01 and S-N02; only S-N03 (a debugging request) is a clean oblique negative.

**Not truncated.** All 30 captures are genuine transcripts (`type:result` `subtype:success`,
`is_error:false`, 23 KB–198 KB). `--priority` front-loaded the 5 decision-critical rows; the
monthly spend budget held for the full run, so no row is truncation-indeterminate.

---

## Scores (scores.tsv)

```
id	run	expected	actual	match
S-P01	1	focused-pre-mortem	full-composer	0
S-P01	2	focused-pre-mortem	focused-pre-mortem	1
S-P01	3	focused-pre-mortem	focused-pre-mortem	1
S-P01	4	focused-pre-mortem	full-composer	0
S-P01	5	focused-pre-mortem	focused-pre-mortem	1
S-P03	1	focused-fishbone	focused-fishbone	1
S-P03	2	focused-fishbone	focused-fishbone	1
S-P03	3	focused-fishbone	focused-fishbone	1
S-P03	4	focused-fishbone	focused-fishbone	1
S-P03	5	focused-fishbone	focused-fishbone	1
S-N01	1	full-composer	focused-pre-mortem	0
S-N01	2	full-composer	focused-pre-mortem	0
S-N01	3	full-composer	focused-pre-mortem	0
S-N01	4	full-composer	focused-pre-mortem	0
S-N01	5	full-composer	focused-pre-mortem	0
S-N02	1	full-composer	full-composer	1
S-N02	2	full-composer	focused-pre-mortem	0
S-N02	3	full-composer	focused-pre-mortem	0
S-N02	4	full-composer	full-composer	1
S-N02	5	full-composer	focused-pre-mortem	0
S-N03	1	full-composer	full-composer	1
S-N03	2	full-composer	full-composer	1
S-N03	3	full-composer	full-composer	1
S-N03	4	full-composer	full-composer	1
S-N03	5	full-composer	full-composer	1
S-N04	1	full-composer	full-composer	1
S-N04	2	full-composer	focused-pre-mortem	0
S-N04	3	full-composer	focused-pre-mortem	0
S-N04	4	full-composer	full-composer	1
S-N04	5	full-composer	focused-pre-mortem	0
```

---

## Lineage

This baseline records the **Phase 117 revised CONF-01** live confirmation of the v7.7 behavioral
fix (the first agent-body/detector behavioral change since the v7.x measurement arc). Unlike the
v7.6 measurement-only re-baseline, v7.7 **changed the detector** (`_TECHNIQUE_CATEGORIES`
pre-mortem 7→9, fishbone 6→7, FIX-01) and the trigger-phrase sync (FIX-02), to resolve the v7.6
S-P01 pre-mortem (2/5) and S-P03 fishbone (1/5) regressions. This run confirms those positives
out-of-sample: **S-P01 3/5, S-P03 5/5** — both restored to their v7.4 floors.

**Falsifiable verdict (D-17): SHORT OF BAR (human-recorded at the blocking checkpoint).** The
positives are confirmed but two of the three blocking oblique negatives (S-N01 0/5, S-N02 2/5)
over-route to pre-mortem. The transcript evidence shows this is **genuine agent routing on
semantically-pre-mortem prompts** (the same phenomenon as S-N04, which drove the first re-scope),
not a precision regression from FIX-01 — and the one truly-oblique negative (S-N03) passes 5/5.
Per honesty-not-score (D-13) the markers were NOT tuned and the run was NOT repeated; this honest
short-of-bar result is the committed deliverable.

**Residual resolution (hand-off to Plan 117-07 CONF-02, D-04/D-09):**
- **RR-79-01** (S-P01 pre-mortem): S-P01 sustained at 3/5 (≥ min-pass) → **CLOSE candidate**;
  117-07 disposes (CLOSE vs carry) and re-points its sentinel to the frozen v7.7 vector `[0,2,3,1,4]`.
- **S-P03 fishbone** (RR-75-03 lineage): 5/5 → 117-07 mints a **new fishbone count-vector sentinel**
  over the frozen v7.7 vector `[3,3,2,2,2]`; CLOSE candidate.
- **RR-114-01** (S-P02 inversion): out of scope — **carried untouched**.
- **Precision finding (S-N01/S-N02/S-N04 genuine pre-mortem routing):** 117-07 may add an
  S-N01/02/03 precision sentinel (S-N03 `[0,0,0,0,0]` is the clean anchor) if warranted.

The BATT-06 honest-state sentinels in `scripts/_battery_core.self_test_boundary()` are re-pointed
to the frozen v7.7 evidence under `tests/step0-captures-v7.7/` (`_load_excerpt_v77`) in Plan
117-07, asserting the documented v7.7 count vectors (honesty-not-score, C-02), not the live pass
rate. Priors (`tests/step0-baseline-v5.0.md … v7.6.md`, all prior `tests/step0-captures-*/` dirs)
and the detector constants (`MIN_HEADER_HITS=2`, `_COMPOSER_FOCUS_CEILING=4`) are byte-frozen.

Prior baseline: `tests/step0-baseline-v7.6.md` (Phase 113-114) — BATTERY: FAIL, the measurement
that recorded the S-P01 (2/5) and S-P03 (1/5) regressions this v7.7 fix resolves.
First CONF-01 attempt: Plan 117-03 (paused at the verdict checkpoint; measured S-P01 4/5, S-P03
5/5, S-N04 0/5 — superseded by this fresh full re-baseline).
