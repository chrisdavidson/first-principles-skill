# persona-live-v9.18c

**FROZEN-EVIDENCE as of 2026-10-02 (plan 87-10).** Registered in `_FROZEN_PATHS` in
`scripts/check-firewall-battery.sh` alongside `tests/persona-live-v9.18` and
`tests/persona-live-v9.18b`: the twelve S-series reading cells in `reading/` ran, were checked, and
the `## 9. Results` table in
[`docs/v9.18c-persona-live-reading.md`](../../docs/v9.18c-persona-live-reading.md) is now
falsifiable only against the committed `reading/manifest.jsonl`, `reading/results.tsv` and
`reading/out/` artifacts recorded here, the same way `examples/` has been frozen since 87-09.
Nothing under this directory is edited after this point.

Fixtures and the reproducer for the post-87 memo-format live-reading pre-registration,
[`docs/v9.18c-persona-live-reading.md`](../../docs/v9.18c-persona-live-reading.md). That document
is the authority on the cell order, pass definition and bar; this file only describes what lives
in this directory.

This directory holds no `sources/` of its own: both the reading cells (S01-S12) and the example
re-derivation cells (E01-E04) read their three frozen analysis files straight from
`tests/persona-live-v9.18/sources/` (read-only reuse) — that directory is FROZEN-EVIDENCE and is
never copied or modified by anything under this directory. `tests/persona-live-v9.18` and
`tests/persona-live-v9.18b` are also both FROZEN-EVIDENCE and are never edited by anything under
this directory.

## examples/

Holds the four plan-87-09 persona-example re-derivation cells (`manifest.jsonl`, `checks.tsv`,
`out/`): the same two worked-example sources and roles as the 86-02 and 87-05 runs
(`product-business-2` x `estimate-fermi`, `decision-owner` x `skeptic`), re-run under the D-11
memo contract. Each passing output is shipped by `cp` (never hand-edited) to
`shared/persona-examples/<example>-<role>.md`, sha256-verified against its manifest entry's
`persona_sha256`, per the 86 D-01 rule: a failing cell is recorded, never hand-fixed into an
example.

## reading/

Holds the twelve post-87 memo-format reading-run cells (S01-S12), run by plan 87-10:
`manifest.jsonl` (one JSON line per cell, the same fields as `examples/manifest.jsonl`),
`results.tsv` (cell, source, role, persona file, PASS/FAIL, codes, persona sha256 — 12 rows, no
persona prose), and `out/` (the eleven persisted persona files that were produced, one per
completed cell). 11/12 cells PASS; S12 (estimate-fermi, skeptic) is `FAIL`/`NO-FILE` — the skill's
own self-check rejected the draft on `PV-WORDS` (two words over the skeptic band's 170-word
ceiling after three allowed cut passes) and deleted it, producing no persona file at all. Recorded
as observed per the pre-registration's §7 rule and never re-run (only a non-terminal `limit_stub`
result is re-run; S12 reached a terminal `no_file` state).

## reproduce.py

Copied from `tests/persona-live-v9.18b/reproduce.py` (FROZEN as of 87-06, never edited) and
adapted: reads `reading/manifest.jsonl`, `reading/results.tsv` and `reading/out/` under this
directory, but still reads its three sources from the frozen `tests/persona-live-v9.18/sources/`
directory (`SOURCES_DIR`, read-only reuse); the verdict line it parses and recomputes additionally
carries a PV-HEADER cell count alongside PV-QUESTIONS and PV-DIRECTIVE, and every clause in the
verdict regex is REQUIRED — no optional groups, unlike the v9.18b reproducer, where an optional
clause could silently pass a wrongly ordered or dropped line (87-06 deviation 1). Exits non-zero on
any mismatch (a wrong row, a wrong code set, a wrong pass count, or a wrong bar outcome) — never
trusts the doc's own prose as ground truth. With no reading cells run yet and no results.tsv/
manifest.jsonl on disk, it prints a one-line `REPRODUCE: FAIL (not yet run -- missing ...)` message
and exits 1 — a clean failure, not a traceback.

```sh
python3 tests/persona-live-v9.18c/reproduce.py
# or, against a copy under test:
python3 tests/persona-live-v9.18c/reproduce.py --doc /path/to/copy.md
```

## run_cell.py

Reused directly from `tests/persona-live-v9.18/run_cell.py` (FROZEN — invoke only, never copied
or edited). Its own `--out` help text says "inside tests/persona-live-v9.18/", but nothing
enforces that; every invocation under this plan passes `tests/persona-live-v9.18c/...` paths for
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
  --out tests/persona-live-v9.18c/<examples|reading>/out \
  --manifest tests/persona-live-v9.18c/<examples|reading>/manifest.jsonl \
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
