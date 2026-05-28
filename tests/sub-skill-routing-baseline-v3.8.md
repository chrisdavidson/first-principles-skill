# Sub-Skill Routing Baseline — v3.8 (FU-21-1 / FU-21-2 regression baseline)

**Recorded:** 2026-05-28 (14:36–15:05 UTC, ~30 min wall-clock for 20 live `claude` invocations)
**Script version:** `scripts/check-sub-skill-routing.py` (commit `29cb502`, v2.1 — routing-field-scoped Signal A; raw-text fallback removed)
**Fixture version:** `tests/sub-skill-routing-catalog.md` (commit `399425d`, v2-aligned header)
**Run flags:** `--repeat 5 --min-pass 3 --p-threshold 0 --n-threshold 2`
**Baseline verdict:** REPRODUCES REGRESSIONS (expected for Phase 45)
**Summary:** P 0/2 (both fail by design) | N 1/2 (N1 holds; N2 forward-looking — fails as predicted)

---

## Per-prompt results

| # | Expected | Runs | Matches | K/N | Verdict |
|---|----------|------|---------|-----|---------|
| P12 | pre-mortem | 5 | 0 | 0/5 | FAIL  ← FU-21-1 reproduced |
| P24 | inversion  | 5 | 0 | 0/5 | FAIL  ← FU-21-2 reproduced |
| N1  | none-or-other | 5 | 5 | 5/5 | PASS |
| N2  | pre-mortem    | 5 | 0 | 0/5 | FAIL  ← forward-looking control (see Notes) |

All 20 captured runs classified as `none-or-other` under v2.1 detection — i.e., the orchestrator invoked the `first-principles:first-principles` composer agent for every prompt, never naming a specific sub-skill (`first-principles:pre-mortem` or `first-principles:inversion`). This is exactly the FU-21 regression class: the current shipped descriptions route to the composer instead of dispatching to a specific sub-skill.

---

## How this baseline was produced

```bash
OUT_DIR=/tmp/sub-skill-45-baseline-$(date -u +%Y%m%dT%H%M%SZ)
python3 scripts/check-sub-skill-routing.py \
  --catalog tests/sub-skill-routing-catalog.md \
  --repeat 5 --min-pass 3 \
  --p-threshold 0 --n-threshold 2 \
  --out "$OUT_DIR"
```

**Run date:** 2026-05-28T14:36:06Z (start) → 2026-05-28T15:05:44Z (end).

**Output directory:** `/tmp/sub-skill-45-baseline-20260528T143606Z/` (transient).
Contains 20 `<id>-run{1..5}.jsonl` raw stream-json captures, the original `scores.tsv` / `verdict.txt`, and v2.1 reclassification artefacts (`scores-v2.1.tsv` / `verdict-v2.1.txt`). The numbers above are the v2.1-reclassified scores; the original `scores.tsv` reflects v2.0 detection which had two false-positive vectors (see Notes).

The `<id>-run{1..5}.jsonl` files hold the raw stream-json evidence for any future re-inspection (sub-skill invocations, Read tool_use envelopes, tool_results — everything the verifier saw).

---

## Phase 46 comparison gate

Phase 46 (Description Fixes + Regression Verification + Closeout) must re-run this same fixture against the edited `:pre-mortem` and `:inversion` descriptions (post-ROUTE-01 / ROUTE-02). Run the same command with the same flags (`--repeat 5 --min-pass 3 --p-threshold 0 --n-threshold 2`) against the same `scripts/check-sub-skill-routing.py` commit (or a forward-compatible successor) so the measurement methodology is byte-identical.

**Success criteria:**

- P12 → `pre-mortem` PASS (≥ 3/5 invocations of `Skill: first-principles:pre-mortem` or `Agent: subagent_type=first-principles:pre-mortem`).
- P24 → `inversion` PASS (≥ 3/5 invocations of `first-principles:inversion`).
- N1 → `none-or-other` PASS (≥ 3/5 — debugging-shaped prompt must not over-trigger on the widened `:pre-mortem`).
- N2 → `pre-mortem` PASS (≥ 3/5 — plan-shaped pre-mortem prompt must not be poached by the sharpened `:inversion`).

Same K-of-N tolerance is load-bearing for apples-to-apples comparison. Note that N2 starts FAILing in this v3.8 baseline and must START PASSing post-Phase-46 — that ratchet itself is part of the gate evidence (it shows the description widening reaches plan-shaped framing in general, not just P12 in particular).

---

## Notes

### Verifier journey during Phase 45

The detection layer was tuned three times before producing the baseline above:

1. **v1 (Plan 45-01)** — Signal A looked for Read tool_use of `agents/references/<name>.md`. Wave 0 calibration (2026-05-28, P09 verbatim, `/tmp/check-sub-skill-routing-calib-20260528T133944Z/`) showed those Reads happen inside the composer subagent's nested stream, invisible to the outer capture. Signal A never fired; Signal B (text markers) misclassified composer-only runs because the composer emits all six techniques' procedure text verbatim.
2. **v2 (Plan 45-04)** — Signal A rewritten to inspect `Skill` / `Agent` / `Task` tool_use envelopes for sub-skill name matches via stringified-input regex; Signal B removed. The first live baseline (this file's `scores.tsv`) showed two false-positive vectors:
   - N1 over-triggered to `both` 3/5: the raw-text regex fallback matched `first-principles:pre-mortem` / `:inversion` strings inside Read tool_result content (the agent Read in-repo files — this script's source, plan files — whose source code contains those literals).
   - P12-run4 classified `both` despite `subagent_type` being `first-principles:first-principles`: the orchestrator had enriched P12's vague prompt with project-state context that quoted the verifier's design text verbatim, and stringifying the whole input dict caught the quoted strings.
3. **v2.1 (this commit)** — removed the raw-text fallback entirely and scoped the structured walk to inspect only the routing fields (`input.skill`, `input.subagent_type`). Two new LOAD-BEARING self-test fixtures encode both contamination vectors. Re-classified the same 20 baseline jsonls; the numbers above are the result.

### `both` classifications under v2.0 (now eliminated)

For Phase 46 readers comparing against the original `scores.tsv`: the `both` classifications in the v2.0 raw output (P12 runs 2 and 4; N1 runs 1-3) were all false positives — none corresponded to actual `first-principles:pre-mortem` or `first-principles:inversion` invocations in the structured tool_use envelopes. v2.1 re-classification gives the same data the clean answer (`none-or-other` everywhere).

### Why N2 fails before Phase 46

The Phase 45 fixture (`tests/sub-skill-routing-catalog.md`) frames N2 as a guard against `:inversion` sharpening poaching plan-shaped `:pre-mortem` traffic post-Phase-46. Against the current shipped descriptions, however, *neither* sub-skill is invoked for N2 — the orchestrator routes to the composer just as it does for P12. So N2's expected outcome (`pre-mortem`) is forward-looking; it represents what the description widening must achieve, not what current behavior is. This is encoded in the fixture header's "Expected baseline outcomes" block and committed in `tests/sub-skill-routing-catalog.md`.

### Cost

20 live `claude -p` invocations × ~80 s/invocation (the composer agent runs all six techniques) = ~26 min of compute time, ~30 min wall-clock with overhead. Phase 46's re-run will be the same.
