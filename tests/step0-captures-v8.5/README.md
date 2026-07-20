Frozen read-only v8.5 raw `.jsonl` per-invocation captures — `claude -p --output-format
stream-json --verbose` stream-json output of the **Phase 156 affected-technique live
re-measure** (5 Step 0 rows: S-P02 inversion / S-P03 fishbone / S-P04 five-whys / S-P10
estimate / S-P14 theoretical-limit). **All 25 captures are fully genuine agent
transcripts** (each `type:result` event `is_error:false`, `api_error_status:null`; 0
spend-limit-truncated captures committed). **5 live catalog rows × 5 repeats = 25
`.jsonl` + 25 `.txt` pairs.**

**Run scope.** AFFECTED-TECHNIQUE: filtered temp catalog `/tmp/step0-v8.5-affected.md`
(5 rows, DEC-01 run order — S-P03, S-P02, S-P04, S-P10, S-P14), `--repeat 5
--min-pass 3`, cwd `/tmp`. `S-P02` inversion is the **unsplit control** — its
reference file was never split by Phase 154, so movement in that row indicates drift
or run-to-run noise rather than a split effect. `S-P03` fishbone, `S-P04` five-whys,
`S-P10` estimate, and `S-P14` theoretical-limit are the four techniques whose reference
files Phase 154 split. Command:

```
REPO=/home/chrisdavidson/programming/first-principles-skills
OUT_DIR=/tmp/step0-live-v8.5-20260720T134229Z
cd /tmp && python3 "$REPO/scripts/check-step0-live.py" \
  --catalog /tmp/step0-v8.5-affected.md \
  --plugin-dir "$REPO/first-principles" \
  --repeat 5 --min-pass 3 \
  --out "$OUT_DIR" \
  --baseline "$REPO/tests/step0-baseline-v8.5.md"
```

**Single run (cap-defensive, 25 invocations).** Launched 2026-07-20T13:42:29Z,
completed 2026-07-20T14:20:16Z (~38 min). At 25 invocations plus one prior budget
probe (`claude -p "OK"`; 26 live calls total against the ~25 estimate) the rolling
five-hour spend cap was not hit. All 25 captures are from a single uninterrupted run
(`20260720T134229Z`). No truncation, no resume, no merge required.

**Provenance SHAs** (at time of run):

| File | Commit |
|------|--------|
| `scripts/check-step0-live.py` | `cf7435d` |
| `scripts/_battery_core.py` | `5cd4537` |
| `first-principles/agents/first-principles.md` | `8c3411c` |
| `tests/step0-fixture-catalog.md` | `02fd820` |

**Format.** Each pair: raw `.jsonl` (full verbatim `stream-json` event stream per
invocation, as written by the harness) and extracted `.txt` assistant-text excerpt
(concatenation of all `text` fields from `type:assistant` content items, produced by
calling `_extract_assistant_text()` from `scripts/_battery_core.py` directly against
the parsed `.jsonl` lines — the same extraction rule the harness itself uses for
marker detection, not a hand-written approximation). The `.jsonl` is committed verbatim
from `$OUT_DIR`; the `.txt` was extracted via a throwaway scratchpad helper (not
committed).

**Honest verdict.** `BATTERY: FAIL` (from `tests/step0-baseline-v8.5.md`). This is an
**AFFECTED-TECHNIQUE baseline** — only 5 rows measured; BATTERY is N/A as a full
8-technique signal. Per-row observed K/5: S-P03 3/5 PASS, S-P02 0/5 FAIL, S-P04 0/5
FAIL, S-P10 0/5 FAIL, S-P14 0/5 FAIL. Only S-P03 fishbone reached `min_pass`. S-P02 is
the unsplit control and it also declined across the three most recent live
observations of that row (v7.11 2/5 → v7.13 1/5 → v8.5 0/5) — recorded here as an
observation only; disposition of every row belongs to Plan 04's verdict document, not
to this frozen-evidence directory.

**Downstream consumer.** Plan 05 re-points a `_load_excerpt_v85` loader in
`scripts/_battery_core.py` at these `.txt` files — it reads the `.txt` excerpt (not
`.jsonl` directly), following the same pattern as `_load_excerpt_v713` at
`scripts/_battery_core.py:916`. The file-naming convention `{id}-run{n}.txt` (e.g.
`S-P02-run1.txt`) is what `_battery_core.py:_load_excerpt_v85` will expect.

**Distinct from** the byte-frozen v7.13 excerpt set (`tests/step0-captures-v7.13/`),
the v7.11 set (`tests/step0-captures-v7.11/`), the v7.8 set (`tests/step0-captures-v7.8/`),
the v7.7 set, v7.6 set, v7.4 set, v6.4 set, v6.3 set, and v5.2 set. All prior capture
dirs stay byte-frozen.

**Temp catalog reproduced verbatim** (so the run is reproducible from git alone
without the ephemeral `/tmp` file; DEC-01 run order):

```
| ID | Prompt | Expected MODE | Notes |
|---|--------|--------------|-------|
| S-P03 | draw a fishbone diagram on the production incident — our checkout API returned 503 errors for 40 minutes starting 14:10 UTC yesterday, affecting all users; we have ruled out the database layer | focused-fishbone | Fires `fishbone` trigger phrase. Technique: fishbone — split Phase 154. |
| S-P02 | invert this claim: faster ships means better retention — our team ships every two weeks and we want to know when this assumption breaks down | focused-inversion | Fires `invert` trigger phrase. Technique: inversion — unsplit control. |
| S-P04 | do a five whys on this outage — our payment service API returned 500 errors for 12 minutes at 09:30 UTC on 2026-06-11; it recovered after a pod restart; 8k transactions were affected | focused-five-whys | Fires `five whys` trigger phrase. Technique: five-whys — split Phase 154. |
| S-P10 | roughly how much does a molten-salt thermal storage system cost per kWh of usable capacity for a 200 MWh utility-scale installation — assume a 30-year plant lifetime, a charging cycle once per day, and that the salt tanks are pre-commissioned | focused-estimate | Fires `roughly how much` trigger phrase. Technique: estimate — split Phase 154. |
| S-P14 | For a molten-salt thermal-storage plant, what's the theoretical limit on thermodynamic conversion efficiency, setting aside current engineering practice — what do the laws actually permit? | focused-theoretical-limit | Fires `theoretical limit` and `what the laws permit` trigger phrases. Technique: theoretical-limit — split Phase 154. |
```

Note: the table above is a verbatim reproduction of `/tmp/step0-v8.5-affected.md`
(Plan 01's byte-faithful extract, `diff`-verified against the source), reproduced here
so the run stays reproducible from git alone even after `/tmp` is cleared. Consult
`tests/step0-fixture-catalog.md` (commit `02fd820`) for the byte-authoritative source
if this excerpt and the fixture catalog ever appear to diverge.
