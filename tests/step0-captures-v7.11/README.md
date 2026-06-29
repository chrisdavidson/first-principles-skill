Frozen read-only v7.11 raw `.jsonl` per-invocation captures — `claude -p --output-format stream-json --verbose` stream-json output of all 145 **Phase 129 live run** captures under `tests/step0-captures-v7.11/{id}-run{n}.jsonl` (capture date: 2026-06-28/29, consolidated from three runs after monthly-spend-limit truncations). **All 145 captures are fully genuine agent transcripts** (each `type:result` event `subtype:success`, `is_error:false`; spend-limit-truncated captures were discarded and not committed here). **29 live catalog rows × 5 repeats = 145 files.**

**Run scope.** Full catalog `tests/step0-fixture-catalog.md`, `--repeat 5 --min-pass 3`, cwd `/tmp`, approach-② `_wrap_for_bypass` bypass channel. The 6 S-A semantic-ambiguity rows are excluded from the live run (owned by STEP0-08 SEMGATE), so 35 catalog rows → 29 live rows × 5 = 145 invocations. Command template: `python3 scripts/check-step0-live.py --catalog tests/step0-fixture-catalog.md --repeat 5 --min-pass 3 --out "$OUT_DIR" --baseline tests/step0-baseline-v7.11.md`.

**3-run best-genuine merge (D-02 truncation recovery).** The monthly spend limit (org-level overage disabled) truncated the run twice. Recovered per D-02 resume-to-complete + merge; the committed captures are the spend-limit-free subset only:

- **Run 1** (`20260628T201506Z`, uncapped, no `--priority`): genuine rows — S-P01, S-P02, S-P03, S-P04, S-P05, S-P06, S-N01, S-N02
- **Run 2** (`20260628T221800Z`, `--priority` front-loading 20 truncated rows): genuine rows — S-P07, S-P08, S-P10, S-P11, S-P12, S-P13, S-P14, S-P15, S-P16, S-N04, S-N06, S-N07, S-N08, S-N09, S-N10, S-N11, S-N12
- **Run 3** (`rerun-20260629T031934Z`, filtered 4-row temp catalog): genuine rows — S-N03, S-N13, S-N14, S-N15

Merge was performed by `scratchpad/merge_emit_baseline.py` (asserting each copied capture is spend-limit-free), with the baseline emitted via the harness's native `_write_baseline` / `_battery_gate` — no `claude` re-invocation, no edit to any byte-frozen surface.

**Provenance SHAs** (at time of run):

| File | Commit |
|------|--------|
| `scripts/check-step0-live.py` | `63c81b9` |
| `scripts/_battery_core.py` | `34100c0` |
| `first-principles/agents/first-principles.md` | `9a795e2` |
| `tests/step0-fixture-catalog.md` | `02fd820` |

**Format.** These are RAW `.jsonl` files — the full verbatim `stream-json` event stream per invocation — unlike the v7.8 captures which held extracted `.txt` assistant-text excerpts. The v7.11 format is raw `.jsonl` (D-06) because Phase 131's `_load_excerpt_v711` will read raw `.jsonl` directly.

**Anomaly.** Monthly-spend-limit truncation in runs 1–2 (org-level overage disabled). The spend-limit captures were identified by the presence of "monthly spend limit" in the response text and excluded from the merge. Every committed capture is `is_error:false` (genuine agent response). No single-call `is_error:true` transient errors observed in the final merged set (unlike v7.8's S-N04-run5 anomaly).

**Honest verdict (from `tests/step0-baseline-v7.11.md`).** `BATTERY: FAIL` — 13/29 rows ≥ 3/5. P: 4/8 canonical; N: 8/13 blocking negatives (+ 1 non-blocking S-N04). A documented FAIL is a valid outcome per D-01 honesty-not-score.

**Downstream consumer.** Phase 131 re-points the BATT-06 `_load_excerpt_v711` loader in `scripts/_battery_core.py:self_test_boundary()` at these raw `.jsonl` files — it reads them directly (not `.txt` excerpts). The file-naming convention `{id}-run{n}.jsonl` (e.g. `S-P01-run1.jsonl`) is what `_battery_core.py:_load_excerpt_v711` expects.

**Distinct from** the byte-frozen v7.8 excerpt set (`tests/step0-captures-v7.8/`), the v7.7 set, v7.6 set, v7.4 set, v6.4 set, v6.3 set, and v5.2 set. All prior capture dirs stay byte-frozen.
