# v9.2.2 Reference-Reads Fixture — DEMO-MULTIREGION Capture

**Recovered:** 2026-09-16. **Status:** FROZEN read-only evidence — never regenerated, never
hand-edited to match a later result. `DEMO-MULTIREGION.md` is the rendered analysis document; this
README is its chain of custody and the phase's pre-registered readings. Both are committed as-is;
any correction to this evidence is a fresh, separately-provenanced capture, not a silent edit of
this one.

## Origin run and chain of custody

Repo HEAD at capture (quoted from the document's own Provenance table): `da59f3e`. Plugin version
at capture: **9.2.2** — all 17 version stamps agree (`check-version-stamps.py` PASS, self-test exit
0, per the document's own Provenance table). Gate state at capture (same table):
`FIREWALL: GREEN (26/26)`.

The exact transport, copied verbatim from `DEMO-first-principles-multiregion-latency.md` §
Provenance:

```bash
ANTHROPIC_MODEL=claude-opus-5 claude -p \
  --plugin-dir "$(pwd)/first-principles" \
  --no-session-persistence \
  --output-format stream-json \
  --verbose \
  --permission-mode bypassPermissions \
  "$(cat prompt.txt)"
```

Chain-of-custody hashes, checkable rather than merely asserted — measured on the untracked
repo-root source and re-measured on the frozen copy in this directory; both readings are
identical:

| File | sha256 |
|---|---|
| `DEMO-MULTIREGION.md` (source `DEMO-first-principles-multiregion-latency.md` / frozen copy, identical) | `268d3d2f505f998d79d42a5f61844b8bbb6b8e68f001831b04db587a958d3847` |

Verified via `cmp` returning exit 0 for the source→frozen pair, and via `sha256sum` producing the
identical digest on both the repo-root original and the frozen copy — not verified by size alone.

Repo HEAD at freeze (`git rev-parse --short HEAD`, this repository, before this plan's commit):
`0f9c072`.

## Limitation: one surviving file

Only the rendered demo document survived: no `.jsonl`, catalog, or TSV. Unlike the five-file
v9.2.1 set (`catalog.md`, `DEMO-TRIAGE.jsonl`, `DEMO-TRIAGE.md`, `defects.tsv`,
`baseline-defects.tsv`), this fixture carries no raw capture.

The document wraps the analysis in the author's own provenance and assessment prose.
`detect_defects` reads it whole, the six sections resolve, and §4 yields 11 chain blocks.

The document calls itself "deliberately untracked, outside every gate's scan scope." That
sentence was true at capture and is kept byte-frozen.

## Detector reading at freeze

Command:

```bash
S=$(mktemp -d) && cp tests/reference-reads-v9.2.2/DEMO-MULTIREGION.md "$S"/ \
    && python3 scripts/check-quality-harness.py --detect-defects "$S" --out "$S"/out.tsv \
    && cat "$S"/out.tsv
```

Row (22-column schema; `n/a` columns are the provenance-verification group, which this fixture
does not exercise):

```
analysis_id	conclusion_claims	untraced_claims	untraced_flag	verdict_cells	nonconforming_verdict_cells	verdict_flag	chain_blocks	malformed_chain_blocks	chain_flag	dependency_cycles	ungrounded_chains	selfaudit_disagreements	provenance_labels	unmatched_sources	unreadable_sources	literals_checked	unlocated_literals	misattributed_literals	zero_literal_gts	orphan_fetches	provenance_flag
DEMO-MULTIREGION	7	0	0	20	0	0	11	0	0	0	0	0	n/a	n/a	n/a	n/a	n/a	n/a	n/a	n/a	n/a
```

That is: `chain_blocks` 11, `malformed_chain_blocks` 0, `conclusion_claims` 7, `untraced_claims` 0,
`verdict_cells` 20, `nonconforming_verdict_cells` 0, `dependency_cycles` 0, `ungrounded_chains` 0,
`selfaudit_disagreements` 0. This TSV is never written under `tests/` — it is produced fresh in a
scratch directory each time this reading is reproduced, per the interfaces-block rule.

## Pre-registered readings (Phase 41, backlog 999.120)

These are the phase's pre-registered values, fixed at planning by a prototype run of the planned
parser against both documents, before any Phase 41 instrument code exists (D-08). The column
names are the exact names plans 41-02 and 41-04 implement. The before leg is
`tests/reference-reads-v9.2.1/DEMO-TRIAGE.md`, already frozen and not re-read into its own
`defects.tsv` (D-07).

| Column | DEMO-TRIAGE (before leg) | DEMO-MULTIREGION (after leg) |
|---|---|---|
| `chain_blocks` (existing) | 8 | 11 |
| `high_conf_chains` | 5 (C1, C2, C4, C7, C8) | 4 (C1, C3, C4, C10) |
| `high_conf_unverified_head` | 2 (C1 cites GT-9?, C7 cites GT-13?) | 0 |
| `confidence_inversions` | 1 (C8 HIGH over C3, C5, C6, all MEDIUM) | 0 (C3 HIGH cites C1 HIGH) |
| `confidence_unparsed` | 0 | 0 |
| `selfaudit_bands_parsed` | 0 | 6 |
| `selfaudit_offvocab_bands` | 6 (every criterion reads `PRESENT`) | 0 |
| `selfaudit_disagreements` (existing) | 0 | 0 (Criterion 5 is `Sound`) |

**H2 honesty note.** Neither leg is a live positive for the Criterion 5 contradiction.
DEMO-TRIAGE's verdict word is out of vocabulary, and the multiregion Criterion 5 is `Sound`. H2's
positive controls are synthetic (plan 41-03).

**Correction.** The backlog entry's "5 HIGH" was corrected to 4 by a direct count of the 11
`**Confidence:**` lines at research (D-08), confirmed again at freeze in this plan: 4 HIGH, 7
MEDIUM (`awk 'NR>=586 && NR<=730' tests/reference-reads-v9.2.2/DEMO-MULTIREGION.md | /usr/bin/grep
-c 'Confidence:\*\* HIGH'` prints 4).

A later measured mismatch against this table is recorded as a finding and never resolved by
editing this table.

## Why registering this path is not a new gate

FROZEN-EVIDENCE (`scripts/check-firewall-battery.sh`) is an inline check whose
`TOTAL=$((TOTAL + 1))` line fires exactly once, unconditionally, regardless of how many entries
`_FROZEN_PATHS` carries — the increment is not inside any loop over the array. Registering this
directory's path as one more `_FROZEN_PATHS` entry therefore does not add a new battery member:
the battery's total gate count and CI job count are unaffected by this registration. For the
current battery/CI population figures, see `CLAUDE.md`'s generated gate table — this README
deliberately states no bare digit of its own for that population, per `docs/PROCESS.md` §2's
standing constraint on moving counts.

## Frozen-evidence discipline

`DEMO-MULTIREGION.md` and this README are committed as-is and never regenerated or hand-edited to
match a later result. This directory is registered in `scripts/check-firewall-battery.sh`'s
`_FROZEN_PATHS` array, so an uncommitted edit to either of these tracked files turns the battery
RED.

That protection has a documented gap, recorded here so nobody relies on it for something it does
not do: FROZEN-EVIDENCE is a `git diff --quiet HEAD` over the registered pathspec, plus a separate
untracked-files sweep. It catches an edit to a file already tracked at HEAD, and it catches an
untracked file appearing inside the directory — but a committed `git rm` of one of these files
passes it clean. It is tamper-evidence for modification, not a deletion guard. Any change to this
fixture's committed contents, including removal, must be reviewed in-diff like any other commit;
nothing here enforces that automatically.
