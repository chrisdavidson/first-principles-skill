# Contract abandonment — the Phase 0 reading

**A recorded reading with its N. Not a gate.** Offline, zero spend: every figure is read from
frozen transcripts.
**Protocol:** [`docs/abandonment-preregistration.md`](abandonment-preregistration.md) §3, with
Amendment 1 (§8).
**Re-derive:** `python3 tests/abandonment/phase0_reading.py`

---

## The answer

**H1 holds.** Over all 50 observable dispatched attempts in every frozen corpus that carries
subagent events, 4 are abandoned, and:

- **(a) every abandoned attempt is one-shot** — the subagent issued zero tool calls and answered
  in a single message;
- **(b) no attempt that read `output-template.md` is abandoned** — 34 read it, 34 kept the
  contract.

**The dispatch side is not implicated.** The pre-registered pattern (`concise`, `brief`,
`short`, `summar`, …) appears in 0 of the 7 one-shot dispatch prompts and in 4 of the 43 others,
and the one-shot prompts are not shorter (median 187 words against 214). The main session is not
asking for a short answer.

By the pre-registration's §4 table, **Phase 1 tests F2**: a six-section output contract stated at
the top of the agent body, where a run that uses no tools still reads it.

**Phase 1 did not reproduce the mechanism.** From an empty working directory, no attempt in either
arm was one-shot, F2 showed no reduction (4 of 10 abandoned against 2 of 10), and most of what
abandonment there was turned out to be delivery failure. H1 describes the frozen corpora above;
it did not generalise. See [`docs/abandonment-phase1-reading.md`](abandonment-phase1-reading.md).

| Body | Observable | One-shot | Abandoned | Abandoned among one-shot | Read the template |
|---|---|---|---|---|---|
| v9.0.0 (w4-paired) | 13 | 1 | 0 | 0 of 1 | 10 |
| v9.0-era (`live-conformance-v9.0`) | 8 | 1 | 0 | 0 of 1 | 1 |
| v8.24 (`quality-provenance-v8.24`) | 1 | 0 | 0 | — | 1 |
| **v9.12.0** (w4-paired, Stage A) | 28 | 5 | **4** | **4 of 5** | 22 |

## Contract-emission reliability — published as a rate

Conformance rates elsewhere in this tree are conditional on a readable document, so a run that
drops the contract entirely leaves every one of them unchanged. This is the rate they cannot show:
dispatched, non-transport attempts that kept the six-section contract.

| Body | Kept the contract |
|---|---|
| v9.0.0 | 13 of 13 |
| v9.0-era | 8 of 8 |
| v8.24 | 1 of 1 |
| **v9.12.0** | **24 of 28** |

Pooled, the older bodies kept it 22 of 22 times and v9.12.0 24 of 28 (one-sided p = 0.089).
**That comparison is not a pre-registered outcome and decides nothing** — the prompts differ
across corpora, and the older-body figure rests on only two one-shot runs. It is also the reason
F2 is worth testing: on the older bodies, the two one-shot runs kept the contract; on v9.12.0,
four of five did not.

## What this does not establish

- **Co-occurrence, not cause.** One-shot and abandonment coincide 4 of 4 times. Whether a text
  change moves abandonment is Phase 1's question, and only an A/B answers it.
- **Why a run goes one-shot is unexplained.** It is not the dispatch prompt. Seven one-shot runs
  in 50 is too few to model.
- **Small counts throughout.** Four abandonments.

## Falsifiers

```sh
# 1. H1's two conditions hold, and the reading says so.
python3 tests/abandonment/phase0_reading.py | grep -q '  H1: HOLDS'
# 2. The dispatch side is not implicated, so F2 -- not F3 -- is selected.
python3 tests/abandonment/phase0_reading.py | grep -q 'dispatch side not implicated'
# 3. The published emission figures are what the tool prints.
python3 tests/abandonment/phase0_reading.py | grep -q 'v9.12.0    24/28'
python3 tests/abandonment/phase0_reading.py | grep -q 'v9.0.0     13/13'
# 4. Amendment 1's fallback fires on the nine legacy captures and nowhere else.
python3 tests/abandonment/phase0_reading.py --json >/dev/null && python3 -c "
import json; r=json.load(open('tests/abandonment/phase0.json'))['rows']
used=[x['attempt'] for x in r if x['legacy_handback']]
assert len(used)==9 and all('live-conformance-v9.0' in u or 'quality-provenance-v8.24' in u for u in used)"
```
