# Sub-Skill Routing Baseline — v4.2 (Boundary Discipline — corrected catalog)

**Recorded:** 2026-06-10 (11:55–12:26 UTC, ~31 min wall-clock for 20 live `claude` invocations)
**Script version:** `scripts/check-sub-skill-routing.py` (commit `2550d3e`)
**Fixture version:** `tests/sub-skill-routing-catalog.md` (commit `2550d3e`, v4.2 corrected — all rows expect `none-or-other`)
**Agent version:** `first-principles/agents/first-principles.md` (commit `2550d3e`)
**Run flags:** `--repeat 5 --min-pass 3` (strict defaults: `--p-threshold 2 --n-threshold 2`)
**Run cwd:** project root (`/home/chrisdavidson/programming/first-principles-skills`)
**Baseline verdict:** BATTERY: PASS
**Summary:** P 2/2 | N 2/2 (all 20 invocations classified `none-or-other` — orchestrator routes to composer for every prompt, never naming a specific sub-skill)
**Pre-run masked-threshold audit:** clean — see `.planning/notes/audit-masked-thresholds-v4.2.md`

---

## Per-prompt results

| # | Expected | Runs | Matches | K/N | Verdict |
|---|----------|------|---------|-----|---------|
| P12 | none-or-other | 5 | 5 | 5/5 | PASS |
| P24 | none-or-other | 5 | 5 | 5/5 | PASS |
| N1  | none-or-other | 5 | 5 | 5/5 | PASS |
| N2  | none-or-other | 5 | 5 | 5/5 | PASS |

All 20 captured runs classified as `none-or-other` under the routing-field-scoped Signal A detection — the orchestrator invoked the `first-principles:first-principles` composer agent for every prompt, never naming a specific sub-skill directly. This is the expected correct behavior: Phase 46 set `disable-model-invocation: true` on all eleven companion skills, so the orchestrator must never auto-route to them; this battery confirms the boundary discipline holds.

---

## How this baseline was produced

```bash
OUT_DIR=/tmp/sub-skill-v4.2-$(date -u +%Y%m%dT%H%M%SZ)
python3 scripts/check-sub-skill-routing.py \
  --catalog tests/sub-skill-routing-catalog.md \
  --repeat 5 --min-pass 3 \
  --out "$OUT_DIR"
```

**Run date:** 2026-06-10T11:55:23Z (start) → 2026-06-10T12:26:06Z (end, ~31 min wall-clock).

**Output directory:** `/tmp/sub-skill-v4.2-20260610T115523Z/` (transient). Contains 20 `<id>-run{1..5}.jsonl` raw stream-json captures, `scores.tsv`, and `verdict.txt`. Raw artifacts not committed (D-09).

**Executor context:** Task 1 (the live battery run) was completed by a prior executor agent which was interrupted by a provider spend limit after capturing the PASS artifacts. This continuation agent (Task 2) transcribed the artifacts from `/tmp/sub-skill-v4.2-20260610T115523Z/verdict.txt` and `scores.tsv` without re-running the battery. The artifact content is preserved verbatim; no re-run or re-scoring was performed.

---

## Lineage

This baseline supersedes `tests/sub-skill-routing-baseline-v3.8.md` (Phase 45 regression capture). What changed:

- **Fixture expectations corrected (Phase 65):** All four rows now expect `none-or-other`. The v3.8 fixture expected P12 → `pre-mortem` and P24 → `inversion`, contradicting the Phase 46 architecture (`disable-model-invocation: true` — orchestrator never auto-routes to sub-skills). The v3.8 baseline was recorded with `--p-threshold 0` to mask the resulting P-row failures. See the SUPERSEDED banner on the v3.8 file.
- **Strict defaults apply:** No `--p-threshold` flag is passed; the script's strict default `--p-threshold 2` requires all P rows to pass (was `--p-threshold 0` in v3.8, masking P12/P24 failures).
- **N2 expectation corrected:** In v3.8, N2 expected `pre-mortem` (a positive expectation placed in the N bucket — a structural contradiction). In v4.2, N2 correctly expects `none-or-other`, consistent with the architectural invariant.
- **Evidence chain:** `.planning/notes/fu21-fixture-contradiction-diagnosis.md`
