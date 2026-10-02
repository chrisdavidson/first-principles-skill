# persona-live-v9.18

Fixtures and the single runner for the PEX-02 live-reading pre-registration,
[`docs/v9.18-persona-live-reading.md`](../../docs/v9.18-persona-live-reading.md). That document
is the authority on the cell order, pass definition and bar; this file only describes what lives
in this directory.

## sources/

Three frozen byte copies, never the user's private repo-root `.first-principles/`:

| File | Origin | sha256 |
|------|--------|--------|
| `analysis-20261002T015836Z.md` | v9.17 live molten-salt analysis from the 82-03 run on `tests/structured-summary-live/baseline/prompts/decompose-irreducibility.txt` (scratch path recorded in `.planning/phases/86-persona-examples-and-live-reading/86-01-PLAN.md`) | `9ef2ac19a922eef5d47dca7d11476349362a5f75d43ea5c05b2d1fddf05fd9ce` |
| `analysis-20260101T000001Z.md` | byte copy of `shared/examples/product-business-2.md`, renamed only -- the synthetic 2026-01-01 UTC is deliberately implausible as a real run time | `2826686e45beee2156f1c1a6c0d64e8ad55be5a73f890241f3c78e952ab9fd63` |
| `analysis-20260101T000002Z.md` | byte copy of `shared/examples/estimate-fermi.md`, renamed only, same synthetic-UTC convention | `f01752db9f0588dd0a831c72c4985f9ba7e7c90ad2a69d39412ba55bfbba3732` |

`shared/examples/` is read here, never written -- seven gates read that glob.

## examples/ and reading/ (created later)

`examples/` (86-02's four persona-example runs) and `reading/` (86-04's twelve reading-run
outputs and manifest) do not exist yet at this plan's commit. Both are created by their own
plans, through the same `run_cell.py`.

## run_cell.py

One runner, used for every paid run in this phase. It refuses a `--source` under the user's
private `.first-principles/`, refuses `--work` resolving inside the repo, refuses a non-empty
`--work/<cell>`, and refuses role `all` (always twelve independent single-role runs, never one
`all` run). `--dry-run` prints the exact argv as a JSON array and exits 0 without spending
anything.

Invocation:

```sh
python3 tests/persona-live-v9.18/run_cell.py \
  --source tests/persona-live-v9.18/sources/<analysis file> \
  --role <decision-owner|operator|risk|skeptic> \
  --work <scratch dir outside the repo> \
  --out tests/persona-live-v9.18/<examples|reading> \
  --manifest tests/persona-live-v9.18/<examples|reading>/manifest.jsonl \
  --cell <id>
```

It never runs `scripts/check-persona-view.py` -- checking the output is a separate step so the
runner cannot shape its own verdict. Exit codes: `0` complete, `2` refused input, `3` usage-limit
stub (stop the sequence, re-run the same cell to resume), `4` the call completed but produced no
persona file.

## Manifest fields

One JSON line appended per cell: `cell`, `source`, `source_sha256`, `role`, `model`, `prompt`,
`started`, `finished`, `raw_sha256`, `is_error`, `subtype`, `num_turns`, `total_cost_usd`,
`persona` (filename or null), `persona_sha256` (or null), `source_unchanged`, `extra_files`,
`status` (`complete` | `no_file` | `limit_stub`).

## Raw streams stay in scratch

`raw.jsonl` is written under `--work/<cell>/`, outside the repo, and is never committed -- it
carries local environment detail. The manifest records its sha256 instead of its content.
