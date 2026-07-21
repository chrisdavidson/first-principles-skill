Frozen read-only v8.6 raw `.jsonl` per-invocation captures — `claude -p --output-format
stream-json --verbose` stream-json output of the **Phase 160 detector-covered-row live
re-measure** (2 Step 0 rows: S-P03 fishbone / S-P04 five-whys — the two rows whose
Procedures Phase 159 compressed and which carry an emission detector). **All 10 captures
are fully genuine agent transcripts** (each `type:result` event `is_error:false`,
`api_error_status:null`, `subtype:success`; 0 spend-limit-truncated captures committed).
**2 live catalog rows × 5 repeats = 10 `.jsonl` + 10 `.txt` pairs.**

**Run scope.** DETECTOR-COVERED: filtered temp catalog `/tmp/step0-v8.6-2row.md` (2 rows,
S-P03 then S-P04), `--repeat 5 --min-pass 3`, cwd `/tmp`. `S-P03` fishbone and `S-P04`
five-whys are the two techniques Phase 159 marker-pinned-compressed AND the only two
Phase-159-touched rows carrying an emission detector (`estimate` and `theoretical-limit`,
the other two Phase-158 compressions, have no emission detector, hence zero measured-floor
risk and no live row here). Command:

```
REPO=/home/chrisdavidson/programming/first-principles-skills
OUT_DIR=/tmp/step0-live-v8.6-20260721T170134Z
cd /tmp && python3 "$REPO/scripts/check-step0-live.py" \
  --catalog /tmp/step0-v8.6-2row.md \
  --plugin-dir "$REPO/first-principles" \
  --repeat 5 --min-pass 3 \
  --out "$OUT_DIR"
```

**No `--baseline` was passed.** The `--baseline` emitter hardcodes `_BASELINE_VERSION =
"v8.5"`; passing it would overwrite `tests/step0-baseline-v8.5.md` mislabeled. This narrow
2-row delta is hand-interpreted in `docs/v8.6-live-remeasure-verdict.md` (Plan 02) directly
from these captures + `scores.tsv`, matching the v8.5 precedent for narrow deltas.

**Single run (cap-defensive, ~11 live calls).** Launched 2026-07-21T17:01:34Z, completed
2026-07-21T17:17:57Z (~16 min). Economics: **~11 live calls total — 10 measurement
(2 rows × 5 repeats) + 1 prior budget probe (`claude -p "Reply with exactly: OK"` → `OK`),
NOT ~26.** The ~26 figure in earlier STATE.md/ROADMAP prose was the stale v8.5 *5-row*
count copied forward without rescaling to this phase's 2-row scope (2×5+1 = 11). At 11
invocations the rolling five-hour spend cap was not hit. All 10 captures are from a single
uninterrupted run (`20260721T170134Z`). No truncation, no resume, no merge required.

**Zero-stub verification.** 0 files match the structural `api_error_status: 429`
discriminator; every `.jsonl`'s `type:result` event has `is_error:false` and
`subtype:success`. No capture was re-rolled to change a number (honesty-not-score, D-05).

**Provenance SHAs** (at time of run):

| File | Commit |
|------|--------|
| `scripts/check-step0-live.py` | `cf7435d` |
| `scripts/_battery_core.py` | `8827d02` |
| `first-principles/agents/first-principles.md` | `3b6d64c` |
| `tests/step0-fixture-catalog.md` | `02fd820` |

**Format.** Each pair: raw `.jsonl` (full verbatim `stream-json` event stream per
invocation, as written by the harness) and extracted `.txt` assistant-text excerpt
(concatenation of all `text` fields from `type:assistant` content items, produced by
calling `_extract_assistant_text()` from `scripts/_battery_core.py` directly against the
parsed `.jsonl` lines — the same extraction rule the harness itself uses for marker
detection, not a hand-written approximation). The `.jsonl` is committed verbatim from
`$OUT_DIR`; the `.txt` was extracted via a throwaway scratchpad helper (not committed).

**Honest verdict.** `BATTERY: FAIL` (printed by the harness). This is a **DETECTOR-COVERED
2-row run** — only 2 rows measured; BATTERY is **N/A** as a full 8-technique signal (the
canonical bar needs the 8 P-rows + N-rows, absent here) and must not be read as a real
battery verdict. Per-row observed K/5:

| Row | Technique | Floor (`tests/step0-baseline-v8.5.md`) | Observed K/5 | Direction |
|-----|-----------|----------------------------------------|--------------|-----------|
| S-P03 | focused-fishbone | 3/5 PASS | **4/5 PASS** | +1 above floor |
| S-P04 | focused-five-whys | 0/5 FAIL | **2/5 FAIL** | +2 gain off floor |

S-P03 fishbone routed focused on runs 1–4 and `full-composer` on run5 (the run5 output DID
emit 4 fishbone markers — clearing `MIN_HEADER_HITS=2` — but also 4 composer-structure
headers, hitting `_COMPOSER_FOCUS_CEILING=4`, so the structural override routed it
full-composer). S-P04 five-whys routed focused on runs 3–4 only. Disposition of each row
against its floor is authored in `docs/v8.6-live-remeasure-verdict.md` (Plan 02), not in
this frozen-evidence directory.

**Downstream consumer.** Plan 02 adds a `_load_excerpt_v86` loader in
`scripts/_battery_core.py` pointed at these `.txt` files (reads the `.txt` excerpt, not
`.jsonl` directly), following the `_load_excerpt_v85` pattern, and re-points the RR-117-01
(S-P03 fishbone) BATT-06 sentinel to the observed v8.6 vector. The file-naming convention
`{id}-run{n}.txt` (e.g. `S-P03-run1.txt`) is what `_load_excerpt_v86` expects. **No
sentinel is authored for S-P04 (five-whys)** — it has none, and its +2 gain off floor is
recorded as observed but not banked (D-03/D-04).

**Distinct from** the byte-frozen v8.5 excerpt set (`tests/step0-captures-v8.5/`), the
v7.13 set (`tests/step0-captures-v7.13/`), the v7.11 set, v7.8 set, v7.7 set, v7.6 set,
v7.4 set, v6.4 set, v6.3 set, and v5.2 set. All prior capture dirs stay byte-frozen.

**Temp catalog reproduced verbatim** (so the run is reproducible from git alone without the
ephemeral `/tmp` file; the two data rows are byte-identical to
`tests/step0-fixture-catalog.md` lines 40–41, commit `02fd820`):

```
| ID | Prompt | Expected MODE | Notes |
|---|--------|--------------|-------|
| S-P03 | draw a fishbone diagram on the production incident — our checkout API returned 503 errors for 40 minutes starting 14:10 UTC yesterday, affecting all users; we have ruled out the database layer | focused-fishbone | Fires `fishbone` trigger phrase. Technique: fishbone. Context added (Phase 74 FIX-01): names the affected service, the error type, duration, scope, and one ruled-out cause branch so the live agent can enumerate cause categories without fabrication. Anti-regression: natural-language trigger phrase only; no slash-invocation positives. |
| S-P04 | do a five whys on this outage — our payment service API returned 500 errors for 12 minutes at 09:30 UTC on 2026-06-11; it recovered after a pod restart; 8k transactions were affected | focused-five-whys | Fires `five whys` trigger phrase. Technique: five-whys. Context added (Phase 74 FIX-01): names the symptom, timestamp, recovery event, and impact so the live agent has an observable starting symptom for the Why-chain without fabrication. Anti-regression: natural-language trigger phrase only; no slash-invocation positives. |
```

Note: the table above is a verbatim reproduction of `/tmp/step0-v8.6-2row.md` (Plan 01's
byte-faithful extract of `tests/step0-fixture-catalog.md` lines 40–41, `diff`-verified
against the source). Consult `tests/step0-fixture-catalog.md` (commit `02fd820`) for the
byte-authoritative source if this excerpt and the fixture catalog ever appear to diverge.
