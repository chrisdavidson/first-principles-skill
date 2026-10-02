# persona-live-v9.18d — linked-header example re-derivation (plan 87-11)

**FROZEN.** This directory is a registered `_FROZEN_PATHS` entry in
`scripts/check-firewall-battery.sh`, and nothing edits it after the plan-87-11 commit.

Plan 87-11 (D-12) changed the persona memo's Basis field from a bare analysis basename to three
links: the analysis, its reader report and the folder index `INDEX.md`. The four shipped persona
examples were re-derived by real `/first-principles:persona` runs under that header. They are
never hand-edited, because each shipped example is a `cp` of a recorded run.

## examples/

These are the same two worked-example sources and the same roles as the 86-02, 87-05 and 87-09
runs (`product-business-2` x `estimate-fermi`, `decision-owner` x `skeptic`), run serially with
`claude-opus-5-5` through the frozen `tests/persona-live-v9.18/run_cell.py`. The sources are the
frozen `tests/persona-live-v9.18/sources/analysis-2026010100000{1,2}Z.md`. Each passing output is
copied by `cp` to `shared/persona-examples/<example>-<role>.md`, and its sha256 is checked
against its manifest entry's `persona_sha256`.

- `manifest.jsonl`: one line per cell, with the fields `run_cell.py` documents.
  `extra_files` now lists `INDEX.md` and `INDEX.pdf` beside the view's PDF, because the skill
  rewrites the folder index after every run.
- `checks.tsv`: cell, source, role, persona file, PASS/FAIL, PERSONA-GATE codes, persona sha256.
- `out/`: the persona files the runs produced.

This is a re-derivation record, not a reading. It carries no pass rate and no pre-registration.

Invocation, per cell:

```sh
python3 tests/persona-live-v9.18/run_cell.py \
  --source tests/persona-live-v9.18/sources/<analysis file> \
  --role <decision-owner|skeptic> \
  --work <scratch dir outside the repo> \
  --out tests/persona-live-v9.18d/examples/out \
  --manifest tests/persona-live-v9.18d/examples/manifest.jsonl \
  --cell <E01..E04>
```
