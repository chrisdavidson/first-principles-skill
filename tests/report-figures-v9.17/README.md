# `tests/report-figures-v9.17/` — fixture provenance

Two structured-summary JSON fixtures for `scripts/check-report-figures.py`'s (Plan 02) self-test
and for Plan 01's own acceptance checks against `shared/spine/references/report-figures.md`'s
typst library. Both validate against `shared/spine/references/summary-schema.json` with zero
findings from `check-summary-block.py`'s `validate_report(..., exemplar=False)`.

## `analysis-20261001T204943Z.json`

Source: `.first-principles/analysis-20261001T204943Z.md`'s single fenced ` ```json ` block
(lines 636-949 of that file), copied verbatim and pretty-printed (`json.dump(..., indent=2)`,
keys in source order) with **exactly one hand-added field**: `conclusion.rests_on`.

That source file predates Phase 80 (`shared/spine/references/summary-schema.json`'s
`conclusion.rests_on` field) — its own `conclusion` object carries only `recommendation` and
`confidence`, no `rests_on` key. The added value,

```json
"rests_on": ["C1","C2","C3","C4","C5","C6","C7","C8","GT-18?"]
```

is transcribed, not invented, from that same source file's own section 6 Pre-check line
(line 289): `**Pre-check:** head C1 (HIGH), C2 (HIGH), C3 (MEDIUM), C4 (MEDIUM), C5 (MEDIUM),
C6 (HIGH), C7 (HIGH), C8 (MEDIUM), GT-18? · ?-marked: GT-18?` — the ids on the head, in order,
each `Cn` without its parenthesised band and `GT-18` with its `?` kept, per D-09 and
`summary-schema.json`'s own `conclusion.rests_on.source` field description.

Fixture-derived counts (independently re-derivable from the JSON, not asserted here as fact):
18 ground truths, 8 chains, 17 assumptions, 33 GT/chain-to-chain edges
(`sum(len(c["rests_on"]) for c in chains)`), 9 conclusion edges
(`len(conclusion["rests_on"])`).

## `worst-case-labels.json`

A derived copy of `analysis-20261001T204943Z.json`, built to stress the figure library's label
width (D-02/node-w) rather than to represent a real analysis. Every ground-truth id is renumbered
`GT-1..GT-18` → `GT-82..GT-99` (18 ids, so the widest id is the two-digit `GT-99`, kept
unverified — `read_at_source: false`, same as the source `GT-18`); every chain id is renumbered
`C1..C8` → `C92..C99` (8 ids, widest `C99`); every chain's `confidence` is forced to `MEDIUM` (the
widest confidence-band word the schema allows, `C99 · MEDIUM` being the longest label
`evidence-trace()` can draw); `conclusion.confidence` is forced to `MEDIUM` to match. Every
`rests_on` reference (chain-level and `conclusion.rests_on`) is remapped through the same two id
maps so every reference still resolves to a renumbered id — no reference is dropped or left
dangling.

This fixture proves the bound the library's own prose states: labels fit at two-digit ids
(`GT-99`, `C99 · MEDIUM`) with zero `overflow` on both figures (D-04b) — not just at the
single-digit ids the real analysis happens to use.

## Never tracked

`.first-principles/` is this repository's scratch working directory for live agent runs — it is
untracked (`git ls-files .first-principles` prints nothing) and never staged. Only the one JSON
value copied out of it, by hand, into this directory's tracked fixture above, is committed.
