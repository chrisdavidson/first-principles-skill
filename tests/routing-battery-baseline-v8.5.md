# Routing Battery Baseline — v8.5 (Merged: Boundary + Focused-Output)

**Recorded:** 2026-07-20T15:12:44Z–15:59:53Z (45 live `claude` invocations: 9 prompts × 5 repeats; 46 total live calls including the Task 1 budget probe)
**Script version:** `scripts/check-routing-battery.py` (commit `c0ce903`)
**Core version:** `scripts/_battery_core.py` (commit `5cd4537`)
**Fixture version:** `tests/routing-battery-catalog.md` (commit `1ab943f`)
**Agent version:** `first-principles/agents/first-principles.md` at commit `8c3411c`
**Catalog:** `tests/routing-battery-catalog.md`
**Run flags:** `--repeat 5 --min-pass 3 --boundary-p-threshold 2 --focused-p-threshold 4 --focused-n-threshold 1`
**Run cwd:** repo root (out-of-repo `/tmp` was NOT used this run — see Methodology notes for the confound this created and why the result is nonetheless kept)
**Baseline verdict:** BATTERY: PASS
**Summary:** boundary P 2/2 | N 2/2; focused P 4/4 | N 1/1; overall PASS
**Milestone:** v8.5 Live Re-Measure (Phase 156, MEASURE-02) — second live re-baseline of the merged dual-signal routing layer since v7.11 (2026-06-29). honesty-not-score (D-01): the observed verdict is recorded as-measured, never forced.

---

## Per-prompt results

| #     | Expected Boundary | Expected Output    | Boundary K/N | Focused K/N | Both-Match Verdict |
|-------|-------------------|--------------------|--------------|-------------|--------------------|
| B-P12 | none-or-other     | n-a                | 5/5 PASS     | n-a         | PASS               |
| B-P24 | none-or-other     | n-a                | 4/5 PASS     | n-a         | PASS               |
| B-N1  | none-or-other     | n-a                | 5/5 PASS     | n-a         | PASS               |
| B-N2  | none-or-other     | n-a                | 5/5 PASS     | n-a         | PASS               |
| F-P12 | n-a               | focused-pre-mortem | n-a          | 3/5 PASS    | PASS               |
| F-P24 | n-a               | focused-inversion  | n-a          | 5/5 PASS    | PASS               |
| F-P25 | n-a               | focused-pre-mortem | n-a          | 5/5 PASS    | PASS               |
| F-P26 | n-a               | focused-pre-mortem | n-a          | 5/5 PASS    | PASS               |
| F-N1  | n-a               | NOT-any-focused    | n-a          | 5/5 PASS    | PASS               |

---

### Verdict-cell schema

Each row's active-signal K/N cell uses the falsifiable `<n>/N PASS|FAIL` form (carried from
`tests/routing-battery-baseline-v4.3.md`, reproduced at `tests/routing-battery-baseline-v7.11.md`).
A row's non-primary signal is `n-a` because the merged catalog expects only one signal per row
(boundary rows `B-*`; focused rows `F-*`). `n-a` is not a zero and never contributes to a tally. The
both-match verdict requires the active signal to pass its own threshold; all 9 rows passed both
gates this run.

---

## How this baseline was produced

Orchestrator-owned background run (Phase-78 live-run pattern, D-01 — not a worktree subagent):

```
OUT=/tmp/check-routing-battery-v8.5-20260720T151244Z
python3 scripts/check-routing-battery.py \
  --catalog tests/routing-battery-catalog.md \
  --plugin-dir first-principles \
  --repeat 5 --min-pass 3 \
  --boundary-p-threshold 2 --focused-p-threshold 4 --focused-n-threshold 1 \
  --out "$OUT"
```

Uncapped, no `--priority` front-loading (D-02 in `156-CONTEXT.md`, this layer's D-01-analog). The
run completed cleanly — 45/45 invocations landed as 45 `.jsonl` capture files under `$OUT`, and the
structural `api_error_status` 429 discriminator matched zero files (see Methodology notes for the
full sweep result). The per-prompt K/N table and inlined `## Scores` below were assembled by hand
from `$OUT/scores-boundary.tsv`, `$OUT/scores-focused.tsv`, and `$OUT/verdict.txt` — this layer has
no baseline emitter, and the STEP0-06 `routing-emitter-absence` self-test guard asserts both
routing scripts stay emitter-free, so none was added. Raw `.jsonl` captures are not committed (the
v7.11 D-05 convention, carried here); the inlined scores below are the self-contained git
deliverable.

---

## Methodology notes

- **`--repeat 5 --min-pass 3`** (best-of-5, K=3): a row PASSes if at least 3 of 5 runs classify
  correctly on its active signal — identical gate shape to the v7.11 and v4.3 anchors.
- **Run-cwd confound (must be recorded, not softened).** This run was launched from the repo root,
  not from `/tmp`. The reason: `tests/routing-battery-baseline-v7.11.md`'s own "How this baseline
  was produced" reproduction block uses relative paths (`--catalog tests/routing-battery-catalog.md`,
  `--plugin-dir first-principles`), and those only resolve correctly when the command is run from the
  repo root — they would fail to resolve from `/tmp`. This directly contradicts that same v7.11
  document's header field, which reads `**Run cwd:** /tmp (out-of-repo — orchestrator-owned
  background run, Phase-78 pattern)`. The two statements in the v7.11 baseline are inconsistent with
  each other, and this run followed the reproduction block (the thing that actually has to execute
  successfully) rather than the header field's stated cwd.

  The measured consequence is confined to exactly one prompt: **B-P12**, across all 5 of its runs,
  invoked the Bash tool and read files under `.planning/`, including this phase's own directory
  (`.planning/phases/156-live-re-measure-honest-verdict/`). The other 8 prompts (40 of the 45 runs)
  never referenced `.planning/` and never invoked Bash. This was visible directly in the `.jsonl`
  transcripts for `B-P12-run{1..5}.jsonl`, which are substantially larger (308–451 KB) than every
  other prompt's captures (10–103 KB) — consistent with a live filesystem-exploration turn that the
  other 8 prompts did not take.

  B-P12's observed boundary result this run is **5/5 PASS**, identical to its v7.11 anchor value
  (also 5/5). Because the row's outcome did not move despite the confound, the overall verdict is
  robust to it — a different B-P12 outcome would have required re-running that row cleanly before
  this document could be trusted, but the observed value already matches the unconfounded prior
  measurement. Per the user's recorded decision, this baseline keeps the result as measured and
  documents the confound here rather than re-spending live calls to eliminate it. This is a known
  limitation of this baseline, not a hidden one: the v7.11 baseline's own header/reproduction
  mismatch is the root cause, and it is not corrected here — `tests/routing-battery-baseline-v7.11.md`
  is frozen evidence and stays byte-unchanged.
- **Observed live-call count vs. estimate:** 46 observed (45 battery-run invocations + 1 budget
  probe from Task 1) against the 45-invocation estimate for the battery itself. No truncation
  occurred; no recovery was needed.
- **429 sweep (structural discriminator only, never the word "spend" as a search term):** zero
  files under `$OUT` matched `"api_error_status": 429`. Two files —
  `B-P12-run3.jsonl` and `B-P24-run1.jsonl` — contain a nested `is_error: true` inside a single
  tool_result block, but both have a transport-level final result record reading
  `subtype: success, is_error: False`. Neither is a truncation. `B-P24-run1`'s nested error is the
  designed `disable-model-invocation` guard rejecting an attempted Skill call — benign and expected,
  not a spend-cap artifact.
- **honesty-not-score (D-01):** the verdict recorded above is transcribed exactly as
  `scripts/check-routing-battery.py` printed it in `$OUT/verdict.txt`, in whichever direction it
  went. No threshold flag was adjusted, no prompt was re-run, and `--repeat` was not extended to
  improve any tally.
- **Priors byte-frozen:** `tests/routing-battery-catalog.md` and
  `tests/routing-battery-baseline-v7.11.md` are read-only; `git diff --exit-code` against both
  exits 0 before and after this commit.

---

## Classification — vs the v7.11 anchor

**PASS at every threshold, with two individual row cells moved down from their v7.11 values.**
Boundary and focused are reported as two separate signals below and are never blended into one pass
rate — averaging them would conceal which signal actually moved.

| Signal | v8.5 (this run) | v7.11 anchor | Delta |
|--------|------------------|---------------|-------|
| Boundary | P 2/2 · N 2/2 PASS | P 2/2 · N 2/2 PASS | tally unchanged; B-P24 cell −1 (5/5 → 4/5), still PASS |
| Focused output | P 4/4 · N 1/1 PASS | P 4/4 · N 1/1 PASS | tally unchanged; F-P12 cell −2 (5/5 → 3/5), still PASS |
| Overall (both-match) | **BATTERY: PASS** | BATTERY: PASS | none |

Per-row detail:

| Row | Primary signal | v7.11 | v8.5 observed | Direction |
|-----|-----------------|-------|-----------------|-----------|
| B-P12 | boundary | 5/5 | 5/5 PASS | unchanged |
| B-P24 | boundary | 5/5 | 4/5 PASS | down 1, still PASS |
| B-N1  | boundary | 5/5 | 5/5 PASS | unchanged |
| B-N2  | boundary | 5/5 | 5/5 PASS | unchanged |
| F-P12 | focused  | 5/5 | 3/5 PASS | down 2, still PASS |
| F-P24 | focused  | 5/5 | 5/5 PASS | unchanged |
| F-P25 | focused  | 5/5 | 5/5 PASS | unchanged |
| F-P26 | focused  | 5/5 | 5/5 PASS | unchanged |
| F-N1  | focused  | 5/5 | 5/5 PASS | unchanged |

Seven of nine rows are unchanged at 5/5. B-P24 fell by 1 (raw `.jsonl` for that row's failing run
shows `expected none-or-other, actual pre-mortem` — a single-run boundary miss, still 4/5 PASS
overall). F-P12 fell by 2 (two of its five runs classified `none` on the focused signal rather than
`focused-pre-mortem` — still 3/5 PASS overall, at the K=3 floor). Both movements stayed inside their
respective PASS bands; neither pushed a tally below its threshold. This is consistent with routing
being non-deterministic run-to-run (documented repo-wide as "routing battery noise") rather than
evidence of a regression traceable to the Phase 154 split — this layer's catalog rows are not among
the four files the split touched (five-whys, theoretical-limit, estimate, fishbone reference
content), and the focused-output signal here exercises `focused-pre-mortem` / `focused-inversion`,
neither of which was split.

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
B-P24	1	none-or-other	pre-mortem	0
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
B-P12	1	n-a	focused-inversion	1
B-P12	2	n-a	full-composer	1
B-P12	3	n-a	none	1
B-P12	4	n-a	full-composer	1
B-P12	5	n-a	full-composer	1
B-P24	1	n-a	none	1
B-P24	2	n-a	none	1
B-P24	3	n-a	none	1
B-P24	4	n-a	none	1
B-P24	5	n-a	none	1
F-P12	1	focused-pre-mortem	none	0
F-P12	2	focused-pre-mortem	focused-pre-mortem	1
F-P12	3	focused-pre-mortem	focused-pre-mortem	1
F-P12	4	focused-pre-mortem	none	0
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
