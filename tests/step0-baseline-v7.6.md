# Step 0 Live Harness Baseline — v7.6

**Recorded:** 2026-06-23T12:46:20Z (110 live `claude` invocations: 22 prompts × 5 repeats)
**Script version:** `scripts/check-step0-live.py` (commit `8d446f5`)
**Core version:** `scripts/_battery_core.py` (commit `be0540e`)
**Fixture version:** `tests/step0-fixture-catalog.md` (commit `926bf52`)
**Agent version:** `first-principles/agents/first-principles.md` (commit `518ec6f`)
**Run flags:** `--repeat 5 --min-pass 3`
**Run cwd:** `/tmp` (out-of-repo — see Methodology notes)
**Baseline verdict:** BATTERY: FAIL
**Summary:** P 3/8 (8-technique canonical bar: S-P01–06 + S-P10 estimate, S-P14 theoretical-limit; 6 genuinely measured, **2 spend-limit-truncated**) | S-N 4/4 measured PASS (S-N06/07/08 truncated) | S-P07/08/11/12/13/15 expected-FAIL (context-free / alternation falsifiers, excluded from the bar) | S-P16 merge-validation (outside /8): **0/5** | **D-02 verdict: REGRESSION** (merge did not improve five-whys routing) | **PARTIAL RUN — truncated at the monthly spend limit after 55/110 calls (D-03)**

---

## 8-technique tally + D-02 five-whys-merge verdict (REBASE-02)

This is the v7.6 measurement-only re-baseline VALIDATING whether the v7.5
decompose→five-whys consolidation merge (shipped on offline-only evidence, never
live-re-measured) actually improved five-whys routing. The single authoritative run
was **truncated at the monthly spend limit after 55/110 calls** (see *Spend-limit
truncation* below). The `--priority` front-load (D-02/D-03) landed both core rows —
**S-P04** (five-whys anchor) and **S-P16** (merge-validation) — in the genuine zone
before the cutoff, so the milestone's core question is answered on genuine evidence.

| # | Technique | Row | v7.4 floor | **v7.6** | vs floor |
|---|-----------|-----|:---:|:---:|:---:|
| 1 | pre-mortem | S-P01 | 3/5 | **2/5 FAIL** | ▼ −1 (regression) |
| 2 | inversion | S-P02 | 1/5 | **1/5 FAIL** | = holds |
| 3 | fishbone | S-P03 | 3/5 | **1/5 FAIL** | ▼ −2 (regression) |
| 4 | five-whys | S-P04 | 4/5 | **3/5 PASS** | ▼ −1 (still passes) |
| 5 | trade-off | S-P05 | 2/5 | **4/5 PASS** | ▲ +2 (improved) |
| 6 | second-order | S-P06 | 5/5 | **4/5 PASS** | ▼ −1 (still passes) |
| 7 | estimate | S-P10 | 0/5 *(contaminated)* | **— truncated** | indeterminate |
| 8 | theoretical-limit | S-P14 | 0/5 *(contaminated)* | **— truncated** | indeterminate |

**Tally: P 3/8** (6 genuinely measured, 2 spend-limit-truncated/indeterminate).

**★ Merge-validation (S-P16, outside the /8 bar): 0/5 — genuinely measured.** All five
runs routed to the **full composer**, not the focused five-whys skill (the run's
captures show `first-principles:first-principles` dispatched; the "five-whys" text in
them is the full composer naming the technique internally, not a focused-mode route).
The v7.4 **decompose anchor (S-P09) was 0/5**. **S-P16 = 0/5 is NOT > 0/5**, so per the
falsifiable D-02 criterion the v7.5 merge did **not** improve five-whys routing: the
"decompose this claim…" prompt still routes to the full composer, exactly as the
standalone decompose technique did pre-merge. Five-whys *itself* still fires
(S-P04 3/5) — it is the "decompose" phrasing that does not trigger it.

**D-02 verdict: REGRESSION (human-confirmed at the blocking checkpoint).** Two signals
combine: (1) S-P16 0/5 = the decompose anchor → the merge did not improve routing
(routing-neutral on the merge question); and (2) **canonical rows fell below their v7.4
floors** — S-P01 pre-mortem 3/5→2/5, S-P03 fishbone 3/5→1/5 (both now below min-pass),
plus S-P04 five-whys 4/5→3/5 and S-P06 second-order 5/5→4/5 (both still passing). Per
the pre-registered D-02 rule ("any canonical row below its v7.4 K/N → regression"), the
human recorded this as a **REGRESSION finding with a forward-committed fix** (the fix
itself is Phase 115 / a follow-up milestone, out of scope for this measurement phase).
The one improvement is S-P05 trade-off (▲ +2, closing RR-108-02).

**D-02a contamination caveat.** The v7.4 floors for **S-P10 (estimate) and S-P14
(theoretical-limit) were 0/5 spend-limit-contaminated** — indeterminate floors, NOT
endorsements. In v7.6 these two rows were *again* truncated by the spend limit, so they
remain indeterminate; a v7.6 "0/5" on them is **not** read as "held steady." The
meaningful five-whys no-regression check is **S-P04 (4/5 → 3/5, ▼ −1)** — five-whys
routing degraded by one run but still clears min-pass.

**Negative-control discipline (measured zone).** S-N01 4/5, S-N02 4/5, S-N03 5/5,
S-N04 3/5 → **4/4 measured N-rows PASS**; no spurious over-routing in the genuine zone.
S-N06/07/08 were truncated (indeterminate, not genuine 0/5). The raw header "S-N 4/7"
reflects the emitter counting truncated rows as failing; the honest measured result is
4/4.

## Spend-limit truncation (D-03 — honest partial run)

The single authoritative run hit the local `claude` account's **monthly spend limit**
after exactly **55/110 calls (the first 11 prompts × 5 repeats)**. Every subsequent
call returned the verbatim API-429 message *"You've hit your monthly spend limit ·
raise it at claude.ai/settings/usage"* (`is_error: true`, `output_tokens: 0`), which
the harness classifies as `none`. Per D-01/D-03 the run is **NOT re-run to chase a
number** — the honest partial IS the deliverable, and the `--priority` front-load
guaranteed the S-P04/S-P16 merge-validation core landed first.

- **Genuinely measured (11 prompts, 55 calls):** S-P04, S-P16, S-P01, S-P02, S-P03,
  S-P05, S-P06, S-N01, S-N02, S-N03, S-N04 — real agent transcripts (30 KB–220 KB
  captures); their K/N cells below are true measurements.
- **Spend-limit-truncated / INDETERMINATE (11 prompts, 55 calls):** S-P07, S-P08,
  S-P10, S-P11, S-P12, S-P13, S-N06, S-P14, S-P15, S-N07, S-N08 — uniform ~11.5 KB
  API-429 captures classified `none`. Their `0/5` cells below are **truncation
  artifacts, not genuine routing measurements** (recorded verbatim per D-01, never
  masked, never forced to a different value). Of these, the two canonical rows
  **S-P10 (estimate) and S-P14 (theoretical-limit)** are carried-indeterminate
  (RR-108-04 / RR-108-05 kept; no fresh RR-114 mint — there is no clean K/N to
  supersede with).

---

## Per-prompt results

| ID | Expected MODE | K/N | Verdict |
|----|---------------|-----|---------|
| S-P01 | focused-pre-mortem | 2/5 FAIL | FAIL |
| S-P02 | focused-inversion | 1/5 FAIL | FAIL |
| S-P03 | focused-fishbone | 1/5 FAIL | FAIL |
| S-P04 | focused-five-whys | 3/5 PASS | PASS |
| S-P05 | focused-trade-off | 4/5 PASS | PASS |
| S-P06 | focused-second-order | 4/5 PASS | PASS |
| S-P07 | focused-pre-mortem | 0/5 FAIL | FAIL (expected — context-free parser-robustness fixture, not part of the 3/8 live-technique bar) |
| S-P08 | focused-pre-mortem | 0/5 FAIL | FAIL (expected — context-free parser-robustness fixture, not part of the 3/8 live-technique bar) |
| S-P10 | focused-estimate | 0/5 FAIL | FAIL |
| S-P11 | focused-estimate | 0/5 FAIL | FAIL (expected — context-free parser-robustness fixture, not part of the 3/8 live-technique bar) |
| S-P12 | focused-estimate | 0/5 FAIL | FAIL (expected — context-free parser-robustness fixture, not part of the 3/8 live-technique bar) |
| S-P13 | focused-estimate | 0/5 FAIL | FAIL (expected — context-free parser-robustness fixture, not part of the 3/8 live-technique bar) |
| S-P14 | focused-theoretical-limit | 0/5 FAIL | FAIL |
| S-P15 | focused-theoretical-limit | 0/5 FAIL | FAIL (expected — context-free parser-robustness fixture, not part of the 3/8 live-technique bar) |
| S-P16 | focused-five-whys | 0/5 FAIL | FAIL (merge-validation signal — outside /8 canonical bar; tracked via _s_p16_result line, not a residual-risk row) |
| S-N01 | full-composer | 4/5 PASS | PASS |
| S-N02 | full-composer | 4/5 PASS | PASS |
| S-N03 | full-composer | 5/5 PASS | PASS |
| S-N04 | full-composer | 3/5 PASS | PASS |
| S-N06 | full-composer | 0/5 FAIL | FAIL |
| S-N07 | full-composer | 0/5 FAIL | FAIL |
| S-N08 | full-composer | 0/5 FAIL | FAIL |

### Verdict-cell schema

Each row's K/N cell uses the falsifiable `<n>/N PASS|FAIL` format (matching the
`routing-battery-baseline-v4.3.md` convention). A row showing `<n>/5 FAIL`
does NOT satisfy the gate. `PASS` means `match_count >= min_pass`.
`FAIL` means `match_count < min_pass`.

---

## How this baseline was produced

```bash
REPO=/path/to/first-principles-skills
OUT_DIR=/tmp/step0-live-v7.6-$(date -u +%Y%m%dT%H%M%SZ)
cd /tmp && python3 "$REPO/scripts/check-step0-live.py" \
  --catalog "$REPO/tests/step0-fixture-catalog.md" \
  --plugin-dir "$REPO/first-principles" \
  --repeat 5 --min-pass 3 \
  --out "$OUT_DIR" \
  --baseline "$REPO/tests/step0-baseline-v7.6.md"
```

**Run date:** 2026-06-23T12:46:20Z

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
Their true observed K/N is recorded below; a forced PASS is never written. Read
together with *Spend-limit truncation* above: **S-P01/S-P02/S-P03 are genuine
measurements** (real transcripts); **S-P10/S-P14/S-N06/S-N07/S-N08 are
spend-limit-truncated `none` artifacts** (indeterminate, recorded verbatim, NOT genuine
0/5). Of the genuine fails, **S-P01 (pre-mortem 3/5→2/5) and S-P03 (fishbone 3/5→1/5)
are new REGRESSIONS** from their v7.4 PASS — recorded as findings here; their RR-ID
reconciliation (the listed RR-79-01 / RR-75-03 are prior/legacy anchors) and the
forward-committed fix are Phase-115 scope. **S-P02 (1/5)** carries forward as the fresh
**RR-114-01** (supersedes RR-108-01). **S-P10/S-P14** keep RR-108-04/RR-108-05
(carried-indeterminate — truncated, not re-measured).

- `S-P01`: 2/5 FAIL — expected `focused-pre-mortem`; observed modes: ['full-composer', 'focused-pre-mortem', 'full-composer', 'focused-pre-mortem', 'full-composer']. Residual-risk tracked as RR-79-01.
- `S-P02`: 1/5 FAIL — expected `focused-inversion`; observed modes: ['focused-inversion', 'full-composer', 'full-composer', 'full-composer', 'full-composer']. Residual-risk tracked as RR-114-01.
- `S-P03`: 1/5 FAIL — expected `focused-fishbone`; observed modes: ['full-composer', 'full-composer', 'focused-fishbone', 'full-composer', 'full-composer']. Residual-risk tracked as RR-75-03.
- `S-P10`: 0/5 FAIL — expected `focused-estimate`; observed modes: ['none', 'none', 'none', 'none', 'none']. Residual-risk tracked as RR-108-04.
- `S-P14`: 0/5 FAIL — expected `focused-theoretical-limit`; observed modes: ['none', 'none', 'none', 'none', 'none']. Residual-risk tracked as RR-108-05.
- `S-N06`: 0/5 FAIL — expected `full-composer`; observed modes: ['none', 'none', 'none', 'none', 'none']. Residual-risk tracked as RR-108-06.
- `S-N07`: 0/5 FAIL — expected `full-composer`; observed modes: ['none', 'none', 'none', 'none', 'none']. Residual-risk tracked as RR-108-06.
- `S-N08`: 0/5 FAIL — expected `full-composer`; observed modes: ['none', 'none', 'none', 'none', 'none']. Residual-risk tracked as RR-108-08.

---

## Scores (scores.tsv)

```
id	run	expected	actual	match
S-P01	1	focused-pre-mortem	full-composer	0
S-P01	2	focused-pre-mortem	focused-pre-mortem	1
S-P01	3	focused-pre-mortem	full-composer	0
S-P01	4	focused-pre-mortem	focused-pre-mortem	1
S-P01	5	focused-pre-mortem	full-composer	0
S-P02	1	focused-inversion	focused-inversion	1
S-P02	2	focused-inversion	full-composer	0
S-P02	3	focused-inversion	full-composer	0
S-P02	4	focused-inversion	full-composer	0
S-P02	5	focused-inversion	full-composer	0
S-P03	1	focused-fishbone	full-composer	0
S-P03	2	focused-fishbone	full-composer	0
S-P03	3	focused-fishbone	focused-fishbone	1
S-P03	4	focused-fishbone	full-composer	0
S-P03	5	focused-fishbone	full-composer	0
S-P04	1	focused-five-whys	focused-five-whys	1
S-P04	2	focused-five-whys	full-composer	0
S-P04	3	focused-five-whys	full-composer	0
S-P04	4	focused-five-whys	focused-five-whys	1
S-P04	5	focused-five-whys	focused-five-whys	1
S-P05	1	focused-trade-off	focused-trade-off	1
S-P05	2	focused-trade-off	focused-trade-off	1
S-P05	3	focused-trade-off	focused-trade-off	1
S-P05	4	focused-trade-off	focused-trade-off	1
S-P05	5	focused-trade-off	full-composer	0
S-P06	1	focused-second-order	full-composer	0
S-P06	2	focused-second-order	focused-second-order	1
S-P06	3	focused-second-order	focused-second-order	1
S-P06	4	focused-second-order	focused-second-order	1
S-P06	5	focused-second-order	focused-second-order	1
S-P07	1	focused-pre-mortem	none	0
S-P07	2	focused-pre-mortem	none	0
S-P07	3	focused-pre-mortem	none	0
S-P07	4	focused-pre-mortem	none	0
S-P07	5	focused-pre-mortem	none	0
S-P08	1	focused-pre-mortem	none	0
S-P08	2	focused-pre-mortem	none	0
S-P08	3	focused-pre-mortem	none	0
S-P08	4	focused-pre-mortem	none	0
S-P08	5	focused-pre-mortem	none	0
S-P10	1	focused-estimate	none	0
S-P10	2	focused-estimate	none	0
S-P10	3	focused-estimate	none	0
S-P10	4	focused-estimate	none	0
S-P10	5	focused-estimate	none	0
S-P11	1	focused-estimate	none	0
S-P11	2	focused-estimate	none	0
S-P11	3	focused-estimate	none	0
S-P11	4	focused-estimate	none	0
S-P11	5	focused-estimate	none	0
S-P12	1	focused-estimate	none	0
S-P12	2	focused-estimate	none	0
S-P12	3	focused-estimate	none	0
S-P12	4	focused-estimate	none	0
S-P12	5	focused-estimate	none	0
S-P13	1	focused-estimate	none	0
S-P13	2	focused-estimate	none	0
S-P13	3	focused-estimate	none	0
S-P13	4	focused-estimate	none	0
S-P13	5	focused-estimate	none	0
S-P14	1	focused-theoretical-limit	none	0
S-P14	2	focused-theoretical-limit	none	0
S-P14	3	focused-theoretical-limit	none	0
S-P14	4	focused-theoretical-limit	none	0
S-P14	5	focused-theoretical-limit	none	0
S-P15	1	focused-theoretical-limit	none	0
S-P15	2	focused-theoretical-limit	none	0
S-P15	3	focused-theoretical-limit	none	0
S-P15	4	focused-theoretical-limit	none	0
S-P15	5	focused-theoretical-limit	none	0
S-P16	1	focused-five-whys	full-composer	0
S-P16	2	focused-five-whys	full-composer	0
S-P16	3	focused-five-whys	full-composer	0
S-P16	4	focused-five-whys	full-composer	0
S-P16	5	focused-five-whys	full-composer	0
S-N01	1	full-composer	full-composer	1
S-N01	2	full-composer	full-composer	1
S-N01	3	full-composer	full-composer	1
S-N01	4	full-composer	full-composer	1
S-N01	5	full-composer	focused-pre-mortem	0
S-N02	1	full-composer	full-composer	1
S-N02	2	full-composer	full-composer	1
S-N02	3	full-composer	focused-pre-mortem	0
S-N02	4	full-composer	full-composer	1
S-N02	5	full-composer	full-composer	1
S-N03	1	full-composer	full-composer	1
S-N03	2	full-composer	full-composer	1
S-N03	3	full-composer	full-composer	1
S-N03	4	full-composer	full-composer	1
S-N03	5	full-composer	full-composer	1
S-N04	1	full-composer	full-composer	1
S-N04	2	full-composer	focused-pre-mortem	0
S-N04	3	full-composer	full-composer	1
S-N04	4	full-composer	focused-pre-mortem	0
S-N04	5	full-composer	full-composer	1
S-N06	1	full-composer	none	0
S-N06	2	full-composer	none	0
S-N06	3	full-composer	none	0
S-N06	4	full-composer	none	0
S-N06	5	full-composer	none	0
S-N07	1	full-composer	none	0
S-N07	2	full-composer	none	0
S-N07	3	full-composer	none	0
S-N07	4	full-composer	none	0
S-N07	5	full-composer	none	0
S-N08	1	full-composer	none	0
S-N08	2	full-composer	none	0
S-N08	3	full-composer	none	0
S-N08	4	full-composer	none	0
S-N08	5	full-composer	none	0
```

---

## Lineage

This baseline records the Phase 113-114 v7.6 **8-technique live re-baseline** of Step 0
technique selection. This is a **measurement-only** re-baseline following the v7.5
five-whys consolidation merge: there is NO detector change and NO agent-body change this
milestone. The agent body is measured **as-shipped (v7.5)** and the detector
`scripts/_battery_core.py` is **frozen** (`_TECHNIQUE_CATEGORIES` unchanged —
inversion 9 markers, trade-off 6 markers — `MIN_HEADER_HITS=2`,
`_COMPOSER_FOCUS_CEILING=4` byte-unchanged). This run uses the 8 canonical rows:
S-P01 pre-mortem, S-P02 inversion, S-P03 fishbone, S-P04 five-whys, S-P05
trade-off, S-P06 second-order, S-P10 estimate, S-P14 theoretical-limit. All 8
techniques have a v7.4 prior K/N. S-P16 (the absorbed reduce-to-primitives prompt
routing to focused-five-whys) is measured as a dedicated merge-validation signal
outside the /8 canonical bar (D-01a). Honesty-not-score (D-01) governs the committed
verdict; the falsifiable criterion is applied at a blocking human checkpoint, not forced.

**Falsifiable verdict (REBASE-02): the v7.5 decompose→five-whys merge did NOT improve
five-whys routing → REGRESSION (human-confirmed).** S-P16 (merge-validation) = 0/5,
equal to the v7.4 decompose S-P09 0/5 anchor — not greater, so no improvement; the
"decompose this claim…" prompt still routes to the full composer. Compounding it,
genuine canonical rows fell below their v7.4 floors (S-P01 3/5→2/5, S-P03 3/5→1/5 now
below min-pass; S-P04 4/5→3/5 and S-P06 5/5→4/5 still passing), with S-P05 trade-off the
lone improver (▲ +2). Per the pre-registered D-02 rule the human recorded a REGRESSION
finding + forward-committed fix (the fix is Phase 115 / a follow-up, out of scope here).
Honesty-not-score (D-01) governs: this BATTERY: FAIL + the truncated partial are the
legitimate committed outcome.

**Residual resolution (D-03/D-04), from the single authoritative partial run:**
- **RR-108-02** (S-P05 focused-trade-off): **CLOSED** at 4/5 ≥ min-pass. The close bar
  is exactly ≥3/5; no new ID minted. Chain resolved: RR-79-03 → RR-92-02 → RR-95-02 →
  RR-108-02 → CLOSED.
- **RR-114-01** (S-P02 focused-inversion, **supersedes RR-108-01**): CARRIED FORWARD at
  1/5 (genuinely measured, < min-pass). Chain: RR-79-02 → RR-92-01 → RR-95-01 →
  RR-108-01 → **RR-114-01**.
- **RR-108-04** (S-P10 focused-estimate): CARRIED-INDETERMINATE — spend-limit-truncated
  this run (all 5 runs `none`), not a clean measurement; RR-108-04 kept (no fresh K/N to
  supersede, no RR-114 mint).
- **RR-108-05** (S-P14 focused-theoretical-limit): CARRIED-INDETERMINATE —
  spend-limit-truncated this run; RR-108-05 kept.
- **New regressions (Phase-115 scope):** S-P01 pre-mortem (3/5→2/5) and S-P03 fishbone
  (3/5→1/5) regressed from v7.4 PASS to below min-pass. Recorded as findings; full
  traceability-ledger reconciliation + the forward-committed fix are deferred to Phase
  115 (this measurement phase does not author the verdict/fix artifact).

The fresh RR-114-01 mint is recorded in the `RR_ID_MAP` update in
`scripts/check-step0-live.py` (Task 2 finalize, post-checkpoint, D-04). The BATT-06
honest-state sentinels in `scripts/_battery_core.self_test_boundary()` are re-pointed to
the frozen v7.6 evidence under `tests/step0-captures-v7.6/` (`_load_excerpt_v76`),
asserting the documented v7.6 count vectors (honesty-not-score, C-02), not the live pass
rate. Priors (`tests/step0-baseline-v5.0.md … v7.4.md`, `tests/step0-captures-v6.4/`,
`tests/step0-captures-v7.4/`) and the detector constants (`MIN_HEADER_HITS=2`,
`_COMPOSER_FOCUS_CEILING=4`, all markers) are byte-frozen.

Prior baseline: tests/step0-baseline-v7.4.md (Phase 108) — BATTERY: FAIL,
P 4/9 (S-P01-06 + three expanded techniques), S-N 4/4; residuals RR-108-01 (S-P02 inversion, CARRIED 1/5),
RR-108-02 (S-P05 trade-off, CARRIED 2/5), RR-108-04 (S-P10 estimate, CARRIED 0/5),
RR-108-05 (S-P14 theoretical-limit, spend-limit-indeterminate) carried forward.
