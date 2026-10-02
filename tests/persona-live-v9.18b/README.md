# persona-live-v9.18b

Fixtures and the reproducer for the post-87 live-reading pre-registration,
[`docs/v9.18b-persona-live-reading.md`](../../docs/v9.18b-persona-live-reading.md). That document
is the authority on the cell order, pass definition and bar; this file only describes what lives
in this directory.

This directory holds no `sources/` of its own: both the reading cells (S01-S12) and the example
re-derivation cells (E01-E04) read their three frozen analysis files straight from
`tests/persona-live-v9.18/sources/` (read-only reuse) — that directory is FROZEN-EVIDENCE and is
never copied or modified by anything under this directory.

## examples/

Holds the four plan-87-05 persona-example re-derivation cells (`manifest.jsonl`, `checks.tsv`,
`out/`): the same two worked-example sources and roles as the original 86-02 run
(`product-business-2` x `estimate-fermi`, `decision-owner` x `skeptic`), re-run under the
post-87 question/voice contract. Each passing output is shipped by `cp` (never hand-edited) to
`shared/persona-examples/<example>-<role>.md`, sha256-verified against its manifest entry's
`persona_sha256`, per the 86 D-01 rule: a failing cell is recorded, never hand-fixed into an
example.

## reading/

Holds the twelve post-87 reading-run cells (S01-S12), created by plan 87-06 (not this plan):
`manifest.jsonl` (one JSON line per cell, the same fields as `examples/manifest.jsonl`),
`results.tsv` (cell, source, role, persona file, PASS/FAIL, codes, persona sha256 — 12 rows, no
persona prose), and `out/` (the twelve persisted persona files, one per cell). Empty at
registration time (no cell has run yet).

## reproduce.py

Copied from `tests/persona-live-v9.18/reproduce.py` (FROZEN, never edited) and adapted: reads
`reading/manifest.jsonl`, `reading/results.tsv` and `reading/out/` under this directory, but
still reads its three sources from the frozen `tests/persona-live-v9.18/sources/` directory
(`SOURCES_DIR`, read-only reuse); cell ids are `S01`-`S12`, not `R01`-`R12`; the verdict line it
parses and recomputes additionally carries PV-QUESTIONS and PV-DIRECTIVE cell counts when the doc
states them. Exits non-zero on any mismatch (a wrong row, a wrong code set, a wrong pass count, or
a wrong bar outcome) — never trusts the doc's own prose as ground truth.

```sh
python3 tests/persona-live-v9.18b/reproduce.py
# or, against a copy under test:
python3 tests/persona-live-v9.18b/reproduce.py --doc /path/to/copy.md
```

With no reading cells run yet, this exits non-zero (missing `results.tsv`) — that failure is
expected at registration time, before any paid run under this id.

## run_cell.py

Reused directly from `tests/persona-live-v9.18/run_cell.py` (FROZEN — invoke only, never copied
or edited). Its own `--out` help text says "inside tests/persona-live-v9.18/", but nothing
enforces that; every invocation under this plan passes `tests/persona-live-v9.18b/...` paths for
`--out` and `--manifest` explicitly. It refuses a `--source` under the user's private
`.first-principles/`, refuses `--work` resolving inside the repo, refuses a non-empty
`--work/<cell>`, and refuses role `all` (always independent single-role runs). `--dry-run` prints
the exact argv as a JSON array and exits 0 without spending anything.

Invocation:

```sh
python3 tests/persona-live-v9.18/run_cell.py \
  --source tests/persona-live-v9.18/sources/<analysis file> \
  --role <decision-owner|operator|risk|skeptic> \
  --work <scratch dir outside the repo> \
  --out tests/persona-live-v9.18b/<examples|reading>/out \
  --manifest tests/persona-live-v9.18b/<examples|reading>/manifest.jsonl \
  --cell <id>
```

It never runs `scripts/check-persona-view.py` — checking the output is a separate step so the
runner cannot shape its own verdict. Exit codes: `0` complete, `2` refused input, `3` usage-limit
stub (stop the sequence, re-run the same cell to resume), `4` the call completed but produced no
persona file.

## Manifest fields

One JSON line appended per cell: `cell`, `source`, `source_sha256`, `role`, `model`, `prompt`,
`started`, `finished`, `raw_sha256`, `is_error`, `subtype`, `num_turns`, `total_cost_usd`,
`persona` (filename or null), `persona_sha256` (or null), `source_unchanged`, `extra_files`,
`status` (`complete` | `no_file` | `limit_stub`).

## Raw streams stay in scratch

`raw.jsonl` is written under `--work/<cell>/`, outside the repo, and is never committed — it
carries local environment detail. The manifest records its sha256 instead of its content.
