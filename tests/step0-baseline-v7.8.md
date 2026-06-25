# Step 0 Live Harness Baseline — v7.8 (CONF-03)

**Recorded:** 2026-06-25T15:44:55Z (30 live `claude` invocations: 6 prompts × 5 repeats — full run, 29/30 genuine; S-N04-run5 returned `is_error:true`, see Methodology notes)
**Script version:** `scripts/check-step0-live.py` (commit `1ab608b` — the 119-01 `_BASELINE_VERSION` v7.6→v7.8 bump)
**Core version:** `scripts/_battery_core.py` (commit `7f3a50b` — Phase-117 FIX-02 detector: pre-mortem 9 markers, fishbone 7 markers, `MIN_HEADER_HITS=2`; byte-unchanged through Phase 118)
**Fixture version:** `tests/step0-fixture-catalog.md` (commit `086f7b2`)
**Agent version:** `first-principles/agents/first-principles.md` (commit `9a795e2` — the Phase-118 FIX-03 negative-match guard column + FIX-04 stay-in-composer tiebreaker)
**Run flags:** `--repeat 5 --min-pass 3 --priority S-P01 S-P03 S-N01 S-N02 S-N03` (no `--baseline`)
**Run cwd:** `/tmp` (out-of-repo — see Methodology notes)
**Baseline verdict:** BATTERY: PASS
**D-1c verdict:** **CONFIRMED** (human-locked at the blocking checkpoint) — all 5 blocking conjuncts hold by the instrument: positives S-P01 3/5, S-P03 4/5 (both ≥ their v7.4 floors); blocking oblique negatives S-N01 3/5, S-N02 3/5, S-N03 5/5. Non-blocking S-N04 5/5 (reported). **Recorded with an explicit detector-under-count caveat** (honesty-not-score, D-01): the negative "passes" are a MIX of genuine clarification-holds and detector under-counts where the agent still ran a pre-mortem — see "Why the confirmation carries a caveat" below.
**Summary:** This is the **Phase 119 CONF-03** targeted live confirmation of the Phase-118 prose fix (FIX-03 negative-match guard + FIX-04 stay-in-composer tiebreaker). vs the v7.7 prior: S-N01 **0/5 → 3/5**, S-N02 **2/5 → 3/5**, S-N04 **2/5 → 5/5** (non-blocking); positives held (S-P01 3/5 = 3/5; S-P03 5/5 → 4/5, still ≥ floor); the clean anchor S-N03 stayed 5/5. The fix moved the blocking oblique negatives over the bar — but transcript inspection shows part of the movement is genuine clarification-holding (S-N01) and part is the same detector under-count the v7.7 baseline flagged (S-N02). Markers were NOT tuned and the run was NOT repeated to chase a score.

---

## D-1c criterion + verdict (CONF-03)

This is the **Phase 119 CONF-03** live confirmation of the Phase-118 behavioral fix. Per 118 D-A, the green offline emulator firewall is a **regression-lock proxy only** — it proves the literal-trigger-plus-guard slice classifies `full-composer`, NOT that the live agent routes the genuinely-oblique S-N01/S-N02 to `full-composer`. **This live run is the sole real proof.** It re-samples the two on-trigger positives in a fresh run (genuine out-of-sample test) and measures the genuinely-oblique S-N01/S-N02/S-N03 as the blocking negative controls, with S-N04 measured but non-blocking (`NON_BLOCKING_NEGATIVE_IDS`, D-16 carried).

**D-1c criterion:** S-P01 ≥ 3/5 **AND** S-P03 ≥ 3/5 (their v7.4 floors — the **D-1b softening**, see below) **AND** S-N01 / S-N02 / S-N03 each ≥ 3/5 full-composer → fix confirmed. S-N04 reported, not a gate.

| Row | Technique / role | v7.4 floor | v7.7 (pre-fix) | **v7.8 (post-fix)** | D-1c conjunct |
|-----|------------------|:---:|:---:|:---:|:---:|
| S-P01 | pre-mortem (positive) | 3/5 | 3/5 | **3/5 PASS** | ✓ holds |
| S-P03 | fishbone (positive) | 3/5 | 5/5 | **4/5 PASS** | ✓ holds |
| S-N01 | oblique negative (blocking) | (full-composer) | 0/5 | **3/5 PASS** | ✓ holds |
| S-N02 | oblique negative (blocking) | (full-composer) | 2/5 | **3/5 PASS** | ✓ holds |
| S-N03 | oblique negative (blocking) | (full-composer) | 5/5 | **5/5 PASS** | ✓ holds |
| S-N04 | semantically-pre-mortem (non-blocking) | (full-composer) | 2/5 | **5/5** | reported, not a gate |

**Verdict: CONFIRMED.** All five blocking conjuncts hold by the instrument (`_classify_mode`, the same instrument that recorded v7.7 SHORT OF BAR — apples-to-apples). BATTERY: PASS.

### D-1b softening (REQUIREMENTS deviation — recorded honestly, not silent)

REQUIREMENTS.md text said **S-P03 ≥ 5/5**. This run applies the **≥ 3/5 v7.4 floor** instead (CONTEXT D-1b): the v7.7 5/5 was a fresh out-of-sample *sample*, not a floor, and requiring 5/5 would make a single out-of-sample miss fail the conjunct. The guard's only job w.r.t. positives is **not to regress them**, and ≥ 3/5 is the established no-regression floor. S-P03 measured **4/5** here (one fewer than v7.7's out-of-sample 5/5) — still comfortably ≥ the floor. This deviation from the literal requirement text is documented here so the reconcile is honest.

### Why the confirmation carries a caveat (honest, transcript-grounded — D-01)

**Every negative `full-composer` classification in this run is a `none → full-composer` inference** (raw `detect_output_structure` = `none`, agent dispatched → inferred `full-composer`), NOT a genuine multi-technique composer structure. This is the same instrument convention v7.7 used. Direct reading of the frozen excerpts shows the negative "passes" are **two distinct behaviors**:

- **Genuine clarification-holds (the stay-in-composer effect):** **S-N01-run1, S-N01-run3** — the agent dispatched first-principles, which *recognized* the pre-mortem framing ("It recognized this as a **pre-mortem** situation") but **held for the plan** rather than running a focused pre-mortem ("it can't run a meaningful pre-mortem without knowing what plan you're worried about, so it's holding for details"). No focused-pre-mortem output was produced — a genuine non-focused result.
- **Detector under-counts (the agent still ran a pre-mortem):** **S-N02-run1, S-N02-run5** — the orchestrator summary literally says *"The first-principles agent ran a pre-mortem on your migration"* and enumerates failure clusters / structural weaknesses, yet fewer than `MIN_HEADER_HITS=2` distinct pre-mortem markers landed in the short summary text, so `_classify_mode` scored these `full-composer`. These are the **same detector under-count** the v7.7 baseline flagged for S-N02/S-N04.

The honest read: the fix **does** narrow the live over-routing (S-N01 went from all-5-focused-pre-mortem to 3-of-5 not-focused, with two genuine clarification-holds; S-N04 went 2/5 → 5/5), but the "confirmation" partly rides on the documented detector under-count, not purely clean stay-in-composer behavior. Per D-01 this honest measurement — true K/N plus this caveat — is the deliverable; markers were not tuned to fit the captures.

### Live `_technique_hits` count vectors (the CONF-04 sentinel hand-off → Plan 119-03)

Distinct-marker counts per run over the frozen `tests/step0-captures-v7.8/` excerpts (`MIN_HEADER_HITS = 2`; a run routes focused when its count ≥ 2):

- **S-P01 pre-mortem:** `[1, 2, 3, 0, 2]` (runs 2,3,5 clear the barrier → focused 3/5)
- **S-P03 fishbone:** `[1, 4, 2, 2, 3]` (runs 2,3,4,5 clear → focused 4/5)
- **S-N01 pre-mortem:** `[0, 2, 1, 1, 3]` (runs 2,5 clear → over-routes 2/5 → full-composer 3/5)
- **S-N02 pre-mortem:** `[0, 3, 3, 1, 1]` (runs 2,3 clear → over-routes 2/5 → full-composer 3/5)
- **S-N03 pre-mortem:** `[1, 0, 0, 0, 0]` (none clear → full-composer 5/5)
- **S-N04 pre-mortem:** `[1, 1, 1, 1, 0]` (none clear → full-composer 5/5; run5 is the `is_error` 74-char capture, count 0)

**Residual-disposition signals for Plan 119-03 (CONF-04):**
- **S-P01 (RR-79-01):** sustained at 3/5 (= v7.4 floor) → **CLOSE candidate sustained** (re-point sentinel to `[1,2,3,0,2]`).
- **S-P03 fishbone (RR-117-01):** 4/5, vector `[1,4,2,2,3]` → **CLOSE candidate sustained** (re-point sentinel; ≥ floor, no regression).
- **S-N01 / S-N02 (the over-routing rows):** moved over the bar but with the under-count caveat → **mint new RR-119-NN** recording the disposition (resolved-over-bar with the under-count caveat documented; the prompts remain semantically-pre-mortem).
- **S-N03 (RR-117-02 precision anchor):** 5/5, vector `[1,0,0,0,0]` → re-point to v7.8.
- **S-N04 (RR-80-01):** 5/5 non-blocking, vector `[1,1,1,1,0]` → re-point to v7.8; note run5 `is_error`.
- **RR-114-01 (S-P02 inversion):** out of scope this run — **carried untouched**.

---

## Per-prompt results

| ID | Expected MODE | K/N | Verdict |
|----|---------------|-----|---------|
| S-P01 | focused-pre-mortem | 3/5 PASS | PASS (positive — fix confirmed out-of-sample at the v7.4 floor) |
| S-P03 | focused-fishbone | 4/5 PASS | PASS (positive — ≥ v7.4 floor; one fewer than v7.7's out-of-sample 5/5) |
| S-N01 | full-composer | 3/5 PASS | PASS (blocking — over the bar; 2 genuine clarification-holds + 1 under-count among the passes) |
| S-N02 | full-composer | 3/5 PASS | PASS (blocking — over the bar; ≥2 of the passes are detector under-counts where the agent ran a pre-mortem) |
| S-N03 | full-composer | 5/5 PASS | PASS (blocking — the one truly-oblique negative; debugging request, no pre-mortem) |
| S-N04 | full-composer | 5/5 | NON-BLOCKING (`NON_BLOCKING_NEGATIVE_IDS`, D-16 — reported, excluded from the bar; run5 `is_error`) |

### Verdict-cell schema

Each row's K/N cell uses the falsifiable `<n>/N PASS|FAIL` format. `PASS` means `match_count >= min_pass` (3/5); `FAIL` means `match_count < min_pass`. True observed K/N is recorded; a forced PASS is never written (D-01/D-13).

---

## How this baseline was produced

```bash
REPO=/path/to/first-principles-skills
# Restricted 6-row catalog (prompts byte-identical to tests/step0-fixture-catalog.md
# rows S-P01, S-P03, S-N01, S-N02, S-N03, S-N04):
CAT=/tmp/step0-v7.8-conf03-catalog.md
OUT_DIR=/tmp/step0-v7.8-conf03-$(date -u +%Y%m%dT%H%M%SZ)
cd /tmp && python3 "$REPO/scripts/check-step0-live.py" \
  --catalog "$CAT" \
  --plugin-dir "$REPO/first-principles" \
  --repeat 5 --min-pass 3 \
  --priority S-P01 S-P03 S-N01 S-N02 S-N03 \
  --out "$OUT_DIR"
# NO --baseline — this doc was written by the orchestrator (Plan 119-02, inline) from the
# recorded scores + the post-run _technique_hits analysis, not by the harness's --baseline emitter.
```

**Run date:** 2026-06-25T15:44:55Z · **Source /tmp dir:** `/tmp/step0-v7.8-conf03-20260625T154455Z`
(ephemeral) · raw `.jsonl` + assistant-text `.txt` + `scores.tsv` + `harness.log` preserved provisionally under the gitignored `.planning/phases/119-…/conf03-evidence/`.

---

## Methodology notes

**Why run from `/tmp`.** When run from the project root, the orchestrator's sub-agent may discover `.planning/` and plugin context, enriching its response with project-specific artifacts. Running from `/tmp` ensures the full-composer mode responds to the verbatim prompt only, matching every prior Step 0 baseline.

**Why `_classify_mode` infers `full-composer` from `none` + dispatch evidence.** When `detect_output_structure_from_file` returns `none` but the capture shows `Agent(subagent_type="first-principles:first-principles")` was dispatched, the sub-agent ran the full-composer path but produced a non-structured response (a clarification request, or a pre-mortem whose markers under-counted). The dispatch itself proves Step 0 chose the full-composer path. This inference is applied only in the Step 0 harness; `_battery_core.py` is not modified. **In this run every negative `full-composer` is such an inference** — see "Why the confirmation carries a caveat."

**Detector under-count is a known measurement limitation.** The detector counts distinct marker patterns in the short orchestrator-*summary* text, not the nested sub-agent transcript. When the agent runs a pre-mortem but the summary paraphrases it without ≥2 canonical markers, the run scores `full-composer` (an under-count "pass"). This was documented in v7.7 and persists here; it means the blocking-negative pass rate is a *lower bound* on how often the agent semantically engages the pre-mortem.

**S-N04-run5 anomaly.** `S-N04-run5.jsonl` returned `type:result subtype:success is_error:true num_turns:2` with a 74-char assistant text — a single transient single-call error on a non-blocking row. It is classified `full-composer` (no markers) and contributes the trailing `0` to the S-N04 count vector. The blocking verdict is unaffected (S-N04 is non-blocking). The other 29 captures are clean `is_error:false`.

**S-N04 non-blocking rationale (D-16), extended context.** S-N04 stays a catalog negative at the emulator/phrase-table layer (it fires NO Step 0 trigger phrase — STEP0-08 unchanged) but is excluded from the blocking live negative bar via `NON_BLOCKING_NEGATIVE_IDS` because its phrasing is semantically a pre-mortem request. In this run it scored 5/5 full-composer (vs 2/5 in v7.7), consistent with the fix's stay-in-composer steering, with the under-count caveat applying as for S-N01/S-N02.

**Not truncated (spend budget held).** All 30 rows ran; `--priority` front-loaded the 5 decision-critical rows; the monthly spend budget held for the full 6 rows × 5 repeats. The only non-clean capture is the S-N04-run5 `is_error` anomaly above; no row is truncation-indeterminate.

---

## Scores (scores.tsv)

```
id	run	expected	actual	match
S-P01	1	focused-pre-mortem	full-composer	0
S-P01	2	focused-pre-mortem	focused-pre-mortem	1
S-P01	3	focused-pre-mortem	focused-pre-mortem	1
S-P01	4	focused-pre-mortem	full-composer	0
S-P01	5	focused-pre-mortem	focused-pre-mortem	1
S-P03	1	focused-fishbone	full-composer	0
S-P03	2	focused-fishbone	focused-fishbone	1
S-P03	3	focused-fishbone	focused-fishbone	1
S-P03	4	focused-fishbone	focused-fishbone	1
S-P03	5	focused-fishbone	focused-fishbone	1
S-N01	1	full-composer	full-composer	1
S-N01	2	full-composer	focused-pre-mortem	0
S-N01	3	full-composer	full-composer	1
S-N01	4	full-composer	full-composer	1
S-N01	5	full-composer	focused-pre-mortem	0
S-N02	1	full-composer	full-composer	1
S-N02	2	full-composer	focused-pre-mortem	0
S-N02	3	full-composer	focused-pre-mortem	0
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
```

---

## Lineage

This baseline records the **Phase 119 CONF-03** live confirmation of the v7.8 behavioral fix (FIX-03 negative-match guard column + FIX-04 stay-in-composer tiebreaker, applied to `shared/spine/SKILL-body.md` and regenerated into `first-principles/agents/first-principles.md` in Phase 118). It is the **sole real proof** of that prose fix — the Phase-118 offline emulator firewall was a regression-lock proxy only (118 D-A).

**Falsifiable verdict (D-1c): CONFIRMED (human-locked at the blocking checkpoint).** All five blocking conjuncts hold by the instrument: positives S-P01 3/5, S-P03 4/5 (both ≥ v7.4 floor, D-1b softening) and blocking oblique negatives S-N01 3/5, S-N02 3/5, S-N03 5/5. Non-blocking S-N04 5/5. The fix narrowed the live over-routing (S-N01 0/5 → 3/5, S-N02 2/5 → 3/5, S-N04 2/5 → 5/5) without retuning the v7.7 detector (pre-mortem 9 markers, fishbone 7 markers byte-unchanged) and without reclassifying the negatives. Per honesty-not-score (D-01) the confirmation is recorded **with** the detector-under-count caveat: part of the negative pass rate reflects clarification-holds (genuine) and part reflects under-counts where the agent still ran a pre-mortem (S-N02) — so the pass rate is a lower bound on stay-in-composer behavior.

**Residual resolution (hand-off to Plan 119-03 CONF-04, D-5/D-6):**
- **RR-79-01** (S-P01 pre-mortem): sustained 3/5 → CLOSE sustained; 119-03 re-points its sentinel to the v7.8 vector `[1,2,3,0,2]` via `_load_excerpt_v78`.
- **RR-117-01** (S-P03 fishbone): 4/5 → CLOSE sustained; re-point to `[1,4,2,2,3]`.
- **S-N01 / S-N02** (over-routing): moved over the bar with the under-count caveat → 119-03 mints **RR-119-NN** asserting the v7.8 vectors `[0,2,1,1,3]` / `[0,3,3,1,1]` (resolved-over-bar, caveat documented — NOT a reclassification, D-4).
- **RR-117-02** (S-N03 precision): 5/5 → re-point to `[1,0,0,0,0]`.
- **RR-80-01** (S-N04): 5/5 non-blocking → re-point to `[1,1,1,1,0]` (note run5 `is_error`).
- **RR-114-01** (S-P02 inversion): out of scope — **carried untouched**.

The BATT-06 honest-state sentinels in `scripts/_battery_core.self_test_boundary()` are re-pointed to the frozen v7.8 evidence under `tests/step0-captures-v7.8/` (`_load_excerpt_v78`) in Plan 119-03, asserting the documented v7.8 count vectors (honesty-not-score, C-02), not the live pass rate. Priors (`tests/step0-baseline-v5.0.md … v7.7.md`, all prior `tests/step0-captures-*/` dirs) and the detector constants (`MIN_HEADER_HITS=2`, `_COMPOSER_FOCUS_CEILING=4`) are byte-frozen.

Prior baseline: `tests/step0-baseline-v7.7.md` (Phase 117 CONF-01) — BATTERY: FAIL / SHORT OF BAR, the pre-fix measurement (S-N01 0/5, S-N02 2/5) this v7.8 fix narrows.
