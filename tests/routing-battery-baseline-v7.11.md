# Routing Battery Baseline — v7.11 (Merged: Boundary + Focused-Output)

**Recorded:** 2026-06-29T13:19:16Z–13:48:09Z (45 live `claude` invocations: 9 prompts × 5 repeats)
**Script version:** `scripts/check-routing-battery.py` (commit `c0ce903`)
**Core version:** `scripts/_battery_core.py` (commit `34100c0`)
**Fixture version:** `tests/routing-battery-catalog.md` (commit `1ab943f`)
**Agent version:** `first-principles/agents/first-principles.md` at commit `9a795e2`
**Catalog:** `tests/routing-battery-catalog.md`
**Run flags:** `--repeat 5 --min-pass 3 --boundary-p-threshold 2 --focused-p-threshold 4 --focused-n-threshold 1`
**Run cwd:** `/tmp` (out-of-repo — orchestrator-owned background run, Phase-78 pattern)
**Baseline verdict:** BATTERY: PASS
**Summary:** boundary P 2/2 | N 2/2; focused P 4/4 | N 1/1; overall PASS
**Milestone:** v7.11 Live Re-Measure — first live re-baseline of the merged dual-signal routing layer since v4.3 (2026-06-11). honesty-not-score (D-01): the observed verdict is recorded as-measured, never forced.

---

## Per-prompt results

| #     | Expected Boundary | Expected Output    | Boundary K/N | Focused K/N | Both-Match Verdict |
|-------|-------------------|--------------------|--------------|-------------|--------------------|
| B-P12 | none-or-other     | n-a                | 5/5          | n-a         | PASS               |
| B-P24 | none-or-other     | n-a                | 5/5          | n-a         | PASS               |
| B-N1  | none-or-other     | n-a                | 5/5          | n-a         | PASS               |
| B-N2  | none-or-other     | n-a                | 5/5          | n-a         | PASS               |
| F-P12 | n-a               | focused-pre-mortem | n-a          | 5/5 PASS    | PASS               |
| F-P24 | n-a               | focused-inversion  | n-a          | 5/5 PASS    | PASS               |
| F-P25 | n-a               | focused-pre-mortem | n-a          | 5/5 PASS    | PASS               |
| F-P26 | n-a               | focused-pre-mortem | n-a          | 5/5 PASS    | PASS               |
| F-N1  | n-a               | NOT-any-focused    | n-a          | 5/5 PASS    | PASS               |

---

### Verdict-cell schema

Each row's active-signal K/N cell uses the falsifiable `<n>/N PASS|FAIL` form (carried from
`tests/routing-battery-baseline-v4.3.md`). A row's non-primary signal is `n-a` because the merged
catalog expects only one signal per row (boundary rows `B-*`; focused rows `F-*`). The both-match
verdict requires the active signal to pass; all 9 rows passed both gates this run.

---

## How this baseline was produced

Orchestrator-owned background run from `/tmp` (Phase-78 live-run pattern, D-01 — not a worktree
subagent):

```
OUT=/tmp/check-routing-battery-v7.11-20260629T131916Z
python3 scripts/check-routing-battery.py \
  --catalog tests/routing-battery-catalog.md \
  --plugin-dir first-principles \
  --repeat 5 --min-pass 3 \
  --boundary-p-threshold 2 --focused-p-threshold 4 --focused-n-threshold 1 \
  --out "$OUT"
```

Uncapped, no `--priority` front-loading (D-01). The run completed cleanly — 45/45 invocations, **zero
spend-limit truncation** (0 `monthly spend limit` captures, 0 `is_error` captures). The per-prompt
K/N table + inlined `## Scores` were assembled from `$OUT/scores-boundary.tsv`,
`$OUT/scores-focused.tsv`, and `$OUT/verdict.txt` by the throwaway helper
`scratchpad/emit_routing_baselines.py` (D-04 — no baseline emitter exists in the harness; the
STEP0-06 routing-emitter-absence guard is intentional). Raw `.jsonl` are not committed (D-05); the
inlined scores are the self-contained git deliverable.

---

## Methodology notes

- **`--repeat 5 --min-pass 3`** (best-of-5, K=3): a row PASSes if ≥ 3 of 5 runs classify correctly —
  identical gate shape to the v4.3 anchor (v4.3 also ran `--repeat 5 --min-pass 3`).
- **Blocking human checkpoint (D-06):** the honest verdict was confirmed by a human before this
  baseline was committed. No residual dispositions occur in this phase (RR-114-01 / S-P10 / S-P14 are
  all Step-0, resolved/carried in Phase 129).
- **Priors byte-frozen:** the v4.3 anchor and all prior baselines are read-only; the firewall
  FROZEN-EVIDENCE gate (`bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (15/15)`) was
  confirmed before and after this commit.

---

## Classification — vs the v4.3 anchor

**PASS — clean reproduction of the v4.3 anchor at the merged dual-signal layer.**

| Signal | v7.11 (this run) | v4.3 anchor | Delta |
|--------|------------------|-------------|-------|
| Boundary | P 2/2 · N 2/2 PASS | P 2/2 · N 2/2 PASS | none |
| Focused output | P 4/4 · N 1/1 PASS | P 4/4 · N 1/1 PASS | none |
| Overall (both-match) | **BATTERY: PASS** | BATTERY: PASS | none |

Despite the substantial routing-surface changes since v4.x (8-technique Step 0, expanded negative
catalog, output-contract headers, the v7.8 guard column + stay-in-composer tiebreaker), the merged
boundary + focused-output battery is **unchanged at verdict level** — every boundary row still routes
to `none-or-other` (the orchestrator never auto-routes to the slash-only sub-skills), and every
focused row still produces its expected focused-technique output (F-P12/F-P25/F-P26 →
`focused-pre-mortem`, F-P24 → `focused-inversion`, F-N1 → no focused output). The two boundary
P-prompts and all focused P-prompts landed at 5/5 on their active signal — stronger than the v4.3
floor (where F-P12/F-P24 sat at the 3/5–4/5 K-of-N boundary). honesty-not-score (D-01): this PASS is
the true observed outcome, not a forced count.

---

## Scores

### Boundary scores (scores-boundary.tsv)

```
id	run	expected	actual	match
B-P12	1	none-or-other	none-or-other	1
B-P12	2	none-or-other	none-or-other	1
B-P12	3	none-or-other	none-or-other	1
B-P12	4	none-or-other	none-or-other	1
B-P12	5	none-or-other	none-or-other	1
B-P24	1	none-or-other	none-or-other	1
B-P24	2	none-or-other	none-or-other	1
B-P24	3	none-or-other	none-or-other	1
B-P24	4	none-or-other	none-or-other	1
B-P24	5	none-or-other	none-or-other	1
F-P12	1	n-a	none-or-other	1
F-P12	2	n-a	none-or-other	1
F-P12	3	n-a	none-or-other	1
F-P12	4	n-a	none-or-other	1
F-P12	5	n-a	none-or-other	1
F-P24	1	n-a	none-or-other	1
F-P24	2	n-a	none-or-other	1
F-P24	3	n-a	none-or-other	1
F-P24	4	n-a	none-or-other	1
F-P24	5	n-a	none-or-other	1
F-P25	1	n-a	none-or-other	1
F-P25	2	n-a	none-or-other	1
F-P25	3	n-a	none-or-other	1
F-P25	4	n-a	none-or-other	1
F-P25	5	n-a	none-or-other	1
F-P26	1	n-a	none-or-other	1
F-P26	2	n-a	none-or-other	1
F-P26	3	n-a	none-or-other	1
F-P26	4	n-a	none-or-other	1
F-P26	5	n-a	none-or-other	1
B-N1	1	none-or-other	none-or-other	1
B-N1	2	none-or-other	none-or-other	1
B-N1	3	none-or-other	none-or-other	1
B-N1	4	none-or-other	none-or-other	1
B-N1	5	none-or-other	none-or-other	1
B-N2	1	none-or-other	none-or-other	1
B-N2	2	none-or-other	none-or-other	1
B-N2	3	none-or-other	none-or-other	1
B-N2	4	none-or-other	none-or-other	1
B-N2	5	none-or-other	none-or-other	1
F-N1	1	n-a	none-or-other	1
F-N1	2	n-a	none-or-other	1
F-N1	3	n-a	none-or-other	1
F-N1	4	n-a	none-or-other	1
F-N1	5	n-a	none-or-other	1
```

### Focused scores (scores-focused.tsv)

```
id	run	expected	actual	match
B-P12	1	n-a	none	1
B-P12	2	n-a	none	1
B-P12	3	n-a	none	1
B-P12	4	n-a	none	1
B-P12	5	n-a	none	1
B-P24	1	n-a	none	1
B-P24	2	n-a	none	1
B-P24	3	n-a	none	1
B-P24	4	n-a	none	1
B-P24	5	n-a	none	1
F-P12	1	focused-pre-mortem	focused-pre-mortem	1
F-P12	2	focused-pre-mortem	focused-pre-mortem	1
F-P12	3	focused-pre-mortem	focused-pre-mortem	1
F-P12	4	focused-pre-mortem	focused-pre-mortem	1
F-P12	5	focused-pre-mortem	focused-pre-mortem	1
F-P24	1	focused-inversion	focused-inversion	1
F-P24	2	focused-inversion	focused-inversion	1
F-P24	3	focused-inversion	focused-inversion	1
F-P24	4	focused-inversion	focused-inversion	1
F-P24	5	focused-inversion	focused-inversion	1
F-P25	1	focused-pre-mortem	focused-pre-mortem	1
F-P25	2	focused-pre-mortem	focused-pre-mortem	1
F-P25	3	focused-pre-mortem	focused-pre-mortem	1
F-P25	4	focused-pre-mortem	focused-pre-mortem	1
F-P25	5	focused-pre-mortem	focused-pre-mortem	1
F-P26	1	focused-pre-mortem	focused-pre-mortem	1
F-P26	2	focused-pre-mortem	focused-pre-mortem	1
F-P26	3	focused-pre-mortem	focused-pre-mortem	1
F-P26	4	focused-pre-mortem	focused-pre-mortem	1
F-P26	5	focused-pre-mortem	focused-pre-mortem	1
B-N1	1	n-a	none	1
B-N1	2	n-a	none	1
B-N1	3	n-a	none	1
B-N1	4	n-a	none	1
B-N1	5	n-a	none	1
B-N2	1	n-a	none	1
B-N2	2	n-a	none	1
B-N2	3	n-a	none	1
B-N2	4	n-a	none	1
B-N2	5	n-a	none	1
F-N1	1	NOT-any-focused	none	1
F-N1	2	NOT-any-focused	none	1
F-N1	3	NOT-any-focused	none	1
F-N1	4	NOT-any-focused	none	1
F-N1	5	NOT-any-focused	none	1
```
