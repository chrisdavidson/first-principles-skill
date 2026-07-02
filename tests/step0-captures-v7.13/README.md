Frozen read-only v7.13 raw `.jsonl` per-invocation captures — `claude -p --output-format stream-json --verbose` stream-json output of the **Phase 137 residual-delta live run** (3 deferred Step 0 residuals: S-P02 inversion / S-P10 estimate / S-P14 theoretical-limit). **All 15 captures are fully genuine agent transcripts** (each `type:result` event `is_error:false`, `api_error_status:null`; 0 spend-limit-truncated captures committed). **3 live catalog rows × 5 repeats = 15 `.jsonl` + 15 `.txt` pairs.**

**Run scope.** RESIDUAL-DELTA: filtered temp catalog `/tmp/step0-residuals-v7.13.md` (3 rows only — S-P02 inversion, S-P10 estimate, S-P14 theoretical-limit), `--repeat 5 --min-pass 3`, cwd `/tmp`, approach-② `_wrap_for_bypass` bypass channel. The S-A semantic-ambiguity rows are excluded from the live run (owned by STEP0-08 SEMGATE) and were not in the filtered temp catalog. Command: `python3 scripts/check-step0-live.py --catalog /tmp/step0-residuals-v7.13.md --plugin-dir /home/chrisdavidson/programming/first-principles-skills/first-principles --repeat 5 --min-pass 3 --out /tmp/step0-live-v7.13-20260702T105054Z --baseline tests/step0-baseline-v7.13.md`.

**Single run (cap-defensive, 15 invocations).** At 15 invocations the monthly spend cap was not hit. All 15 captures are from a single uninterrupted run (`20260702T105054Z`). No resume or merge required.

**Provenance SHAs** (at time of run):

| File | Commit |
|------|--------|
| `scripts/check-step0-live.py` | `dc878d5` |
| `scripts/_battery_core.py` | `8c7c117` |
| `first-principles/agents/first-principles.md` | `ef22988` |
| `tests/step0-fixture-catalog.md` | `02fd820` |

**Format.** Each pair: raw `.jsonl` (full verbatim `stream-json` event stream per invocation, as written by the harness) and extracted `.txt` assistant-text excerpt (concatenation of all `text` fields from `type:assistant` content items, derived by inspecting the v7.11 `.txt`/`.jsonl` extraction pattern — same rule as `tests/step0-captures-v7.11/`). The `.jsonl` is committed verbatim from `$OUT_DIR`; the `.txt` was extracted via a throwaway scratchpad helper (not committed).

**Honest verdict.** `BATTERY: FAIL` (from `tests/step0-baseline-v7.13.md`). This is a **RESIDUAL-DELTA baseline** — only 3 rows measured; BATTERY is N/A as a full 8-technique signal (D-01b). Per-residual observed K/5: S-P02 1/5, S-P10 0/5, S-P14 0/5. All three CARRIED per D-02 (< 3/5 min-pass). Dispositions human-confirmed at the Phase 137 blocking checkpoint (honesty-not-score, D-01).

**Downstream consumer.** Phase 138 re-points the BATT-06 `_load_excerpt_v713` loader in `scripts/_battery_core.py:self_test_boundary()` at these `.txt` files — it reads the `.txt` excerpt (not `.jsonl` directly), following the same pattern as `_load_excerpt_v711` at line 905. The file-naming convention `{id}-run{n}.txt` (e.g. `S-P02-run1.txt`) is what `_battery_core.py:_load_excerpt_v713` will expect.

**Distinct from** the byte-frozen v7.11 excerpt set (`tests/step0-captures-v7.11/`), the v7.8 set (`tests/step0-captures-v7.8/`), v7.6 set, v7.4 set, v6.4 set, v6.3 set, and v5.2 set. All prior capture dirs stay byte-frozen.
