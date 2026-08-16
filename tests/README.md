# `tests/` — what is load-bearing, and what is archive

**Decision (2026-08-16, audit stream 4): keep all 550 tracked files. Nothing is deleted.**
What was missing was never the disk space — it was the ability to tell, for any one file, whether
something reads it. That is what this document supplies, and it is re-derivable rather than
asserted:

```sh
python3 scripts/trace-tests-usage.py                  # the table below, recomputed
python3 scripts/trace-tests-usage.py --list-archive   # the 441 individually
```

The tracer runs every offline gate under a `sys.addaudithook` `open` hook and records what each
one actually reads. It measures; it does not grep for filenames. Two ways grepping has already
produced wrong answers in this repo are recorded under **Traps** below.

The counts describe evidence files. This file is the index and is excluded from its own totals —
otherwise the document would report on itself and shift its numbers by one on the commit that
created it.

## Three tiers

| Tier | Files | Size | Definition |
|---|---|---|---|
| **gate-pinned** | **102** (18.5 %) | 0.52 MB | Opened at runtime by an offline gate's `--self-test`, or named as a matrix `artifact_link` — which TRACE-03 deep-resolves, so the file must exist. Deleting one turns the battery RED. |
| **live-unwired** | **7** (1.3 %) | 0.08 MB | Executed by `pytest`, and **by no CI job**. Real assertions, no automation behind them. |
| **archive** | **441** (80.2 %) | 2.25 MB | No executable relationship. Tracked, often cited in prose, never read by anything that runs. |

The two-way split this replaces (pinned / archival) is what let the second tier hide inside the
third.

### The 7 live-unwired files are the finding, not the 441

`.github/workflows/validation.yml` runs pytest on exactly one path —
`scripts/check-links_anchors_test.py`, 8 tests. The eight suites under `tests/` carry **123
assertions between them and are run by no CI job**:

| Suite | Tests | What it guards |
|---|---|---|
| `test_67_battery_core.py` | 26 | BATT-06 sentinel internals |
| `test_65_doc_invariants.py` | 23 | Doc invariants — **including the retirement guards stream 2 migrated here** |
| `test_66_baseline_invariants.py` | 22 | Frozen-baseline invariants |
| `test_69_merged_baseline_invariants.py` | 20 | Merged routing-battery baselines (also `artifact_link`-pinned, so it counts as gate-pinned above) |
| `test_82_traceability.py` | 14 | Traceability schema |
| `test_step0_live_task1.py` | 8 | Step 0 live-harness parsing |
| `test_70_step0_emulator_invariants.py` | 5 | Emulator invariants |
| `test_step0_live_task2.py` | 5 | Step 0 live-harness scoring |

They pass today (`python3 -m pytest tests/ -q` → 123 passed) because contributors run them by
hand. Nothing makes that true tomorrow. **Wiring them into CI is logged as follow-up, not done
here** — stream 4's remit was to classify, and adding a CI job is a change to the gate surface.

This is the project's own recurring failure class: a green signal that asserts less than it
appears to. Prior instances are enumerated in `docs/README.md`'s GREENMEAN-01 paragraph.

## Per directory

`gate-pinned / live-unwired / archive`, from `scripts/trace-tests-usage.py`:

| Directory | Pinned | Unwired | Archive |
|---|---|---|---|
| `(top level)` | 6 | 7 | 40 |
| `step0-captures-v7.11` | 30 | 0 | 117 |
| `step0-captures-v8.5` | 15 | 0 | 12 |
| `step0-captures-v7.4` | 5 | 0 | 31 |
| `step0-captures-v8.6` | 5 | 0 | 6 |
| `step0-captures-v5.2` | 0 | 0 | 16 |
| `step0-captures-v6.3` | 0 | 0 | 21 |
| `step0-captures-v6.4` | 0 | 0 | 21 |
| `step0-captures-v7.6` | 0 | 0 | 21 |
| `step0-captures-v7.7` | 0 | 0 | 31 |
| `step0-captures-v7.7-diag` | 0 | 0 | 6 |
| `step0-captures-v7.8` | 0 | 0 | 31 |
| `step0-captures-v7.13` | 0 | 0 | 17 |
| `quality-fixtures-v8.7` | 24 | 0 | 7 |
| `quality-baseline-v8.7` | 8 | 0 | 2 |
| `quality-baseline-v8.7-postfix` | 4 | 0 | 23 |
| `quality-baseline-v8.7-regenerated` | 4 | 0 | 23 |
| `quality-baseline-v8.10-oos` | 0 | 0 | 10 |
| `quality-probe-v8.7` | 1 | 0 | 1 |
| `defrobust-v8.11` | 0 | 0 | 5 |

**Every number on this page is a measurement of the gate set as it stood on 2026-08-16**, not a
property of the files. Adding, removing or re-scoping any gate can move a file between tiers, so
re-run the tracer after any change to the gate surface rather than quoting these figures forward.
The tracer exits 1 if any gate command fails, because a partial trace understates what is
load-bearing while looking complete.

**Eight of the twelve capture generations are read by nothing** (v5.2, v6.3, v6.4, v7.6, v7.7,
v7.7-diag, v7.8, v7.13 — 164 files). Their `_load_excerpt_v*` loaders in
`scripts/_battery_core.py` are retained byte-frozen so a superseded sentinel generation stays
readable; the loaders are live code, the captures they would read are not currently reached.

## Why nothing was deleted

Four reasons, in descending weight. The first is the only one that would be hard to reverse.

1. **Comparability is the asset.** Every frozen `step0-baseline-v*.md` and its captures are what
   make a v8.6 measurement comparable to a v7.4 one. That property is destroyed by deletion and
   cannot be rebuilt — the live runs that produced them cost real spend and cannot be re-run
   against past agent bodies.
2. **This repo has already deleted test evidence once.** On 2026-07-28 a `git filter-repo` removed
   237 raw `tests/**.jsonl` captures and rewrote every SHA from v6.0 onward. The cost is still
   being paid: commit references in documents predating that date do not resolve.
3. **Provenance is not visible to a reader.** An archive file can be the evidence behind a
   published figure while appearing in no script. Deletion decisions of that kind are diff-review
   questions, not grep questions.
4. **2.25 MB.** The storage argument does not survive contact with the numbers.

**If you disagree, the cost of the other option is:** `--list-archive` gives the exact set;
excluding the 8 pytest suites and the 6 stream-2 orphans below leaves ~427 files and ~2.2 MB, and
the battery stays GREEN through the deletion. The reversibility, not the mechanics, is the
objection.

## Traps

- **`FROZEN-EVIDENCE` is not a deletion guard.** The battery's inline check is
  `git diff --quiet` over a pathspec — it catches *uncommitted worktree edits* to frozen files. A
  committed `git rm` passes it clean. Nothing in the battery prevents deleting frozen evidence.
- **`artifact_link` is deep-resolved; `deliverable_path` is not.** A `tests/` path in
  `deliverable_path` is reported and never existence-checked, so it looks pinned and is not.
  `tests/step0-captures-v7.11` is exactly this case — RECON-02's `deliverable_path`, which is why
  117 of its 147 files land in archive.
- **Grepping for a loader's call site lies.** `_load_excerpt_v74` is passed as a *function object*
  inside a sentinel tuple, so `grep '_load_excerpt_v74('` matches only its `def` and reports a
  live generation as dead. The runtime trace shows it reading five v7.4 files. Measure, don't
  grep — the whole reason `trace-tests-usage.py` exists.
- **Five `.jsonl` files must stay tracked** for QUAL-01, which survived the 2026-07-28 purge for
  that reason.

## Stream-2 orphans

Retiring `check-sub-skill-routing.py` and `check-focused-output.py` orphaned six files, all now in
the archive tier: `focused-output-catalog.md`, `sub-skill-routing-catalog.md`, and the
`focused-output-baseline-v3.8/v4.2` and `sub-skill-routing-baseline-v*` sets.

The two baseline sets sit **inside the `FROZEN-EVIDENCE` pathspec**, so the battery now protects
the frozen evidence of a retired tool. **Both pathspec entries are kept, deliberately.** Retiring
a tool does not unfreeze what it measured, and dropping the entries would make those files
editable in place — silently reducing protection to tidy a list. The cost is two pathspec lines;
the alternative is the only change that could let a frozen measurement drift unnoticed.
