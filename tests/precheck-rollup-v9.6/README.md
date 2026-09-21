# v9.6 Pre-Check/Roll-Up Composition Fixture — backlog OBS-02, roadmap SC3

**Synthetic fixture, not evidence of model behaviour.** `analyses/PC-ROLLUP.md` is hand-authored
directly against `shared/spine/references/output-template.md`'s confidence pre-check shape
(OBS-01) — it is not a live agent capture. It exists to demonstrate, with both readings taken by
actually running the two harness versions, that the pre-Phase-52 `detect_defects` reads this
analysis clean and the Phase 52 `detect_defects` trips it (D-06's second evidence leg; roadmap
SC3: "evidenced by a fixture capture that trips the new check where it previously passed").

## The defect and where it sits

`analyses/PC-ROLLUP.md` carries two §4 chains, C1 and C2, both rated `**Confidence:** MEDIUM`,
each preceded by a well-formed `**Pre-check:**` line whose `Inputs ceiling` matches its own
label. The §6 Conclusion rolls both chains up into a single recommendation, preceded by its own
pre-check —

```text
**Pre-check:** head C1 (MEDIUM), C2 (MEDIUM) · ?-marked: none · lowest cited: MEDIUM · Inputs ceiling: MEDIUM
**Confidence:** (chains C1 and C2) HIGH
```

— and rates the roll-up **HIGH**, above both cited chains and above its own stated `Inputs
ceiling`. This is the exact P2 composition case named in `docs/v9.6-instrument-rederivation.md`
§7: a chain (here, a §6 roll-up) rated above the lowest-rated chain its head cites. A trailing
legacy Self-Audit Gate block claims Criterion 5 `Rigorous` over the whole document.

## Which control pins it

`scripts/check-quality-harness.py`'s `_selftest_defects` control **(P24)** reads this file
directly (via the `_PRECHECK_ROLLUP_FIXTURE` module constant) and asserts the exact per-field
values recorded in the "New-harness reading" TSV below, plus that the pre-check disagreement's
`section` is `6` and its `kinds` is `["label_above_ceiling"]`.

## Both harness readings

Both readings were produced by actually running `scripts/check-quality-harness.py
--detect-defects tests/precheck-rollup-v9.6/analyses --out <path>` — the pre-Phase-52 leg inside a
detached `git worktree` checked out at the phase base, the new-harness leg against the working
tree at this commit's parent. Neither reading is inferred; both TSVs below are pasted verbatim.
Local scratch paths in the printed `--out` confirmation line are replaced with `<scratch>` and
disclosed as replaced; no other rewriting was done.

### Pre-Phase-52 reading

**Command:** `python3 <scratch>/pre52/scripts/check-quality-harness.py --detect-defects
tests/precheck-rollup-v9.6/analyses --out <scratch>/pre52.tsv`, run inside a detached worktree
(`git worktree add --detach <scratch>/pre52 183fb55`) — `183fb55`, the 52-01 phase base recorded
in `docs/v9.6-instrument-rederivation.md` §7's `**Phase base:**` line. (Diligence check, not a
blocker: `git diff 183fb55 a9c1232 -- scripts/check-quality-harness.py` shows the harness did
move between this base and the 52-02 commit — but only in one `_CONTRACT_FIXTURES` literal that
mirrors the template's new pre-check line in a contract-pin fixture, disclosed as a deviation in
`52-02-SUMMARY.md`; `detect_defects` itself is unaffected, and `183fb55` — before any Phase 52
edit at all — is the correct pre-Phase-52 base per this plan's own interfaces block.)

```text
analysis_id	conclusion_claims	untraced_claims	untraced_flag	verdict_cells	nonconforming_verdict_cells	verdict_flag	chain_blocks	malformed_chain_blocks	chain_flag	dependency_cycles	ungrounded_chains	selfaudit_disagreements	provenance_labels	unmatched_sources	unreadable_sources	literals_checked	unlocated_literals	misattributed_literals	zero_literal_gts	orphan_fetches	provenance_flag	high_conf_chains	high_conf_unverified_head	confidence_inversions	confidence_unparsed	selfaudit_bands_parsed	selfaudit_offvocab_bands
PC-ROLLUP	2	0	0	1	0	0	2	0	0	0	0	0	n/a	n/a	n/a	n/a	n/a	n/a	n/a	n/a	n/a	0	0	0	0	1	0
```

No `precheck_*` or `rollup_*` column exists at all at this commit — the pre-check surface and
both new detectors are Phase 52 additions. `selfaudit_disagreements` reads **0**: the legacy
harness has no field to reconcile the trailing Criterion 5 `Rigorous` claim against, so it passes
this analysis clean.

### New-harness reading

**Command:** `python3 scripts/check-quality-harness.py --detect-defects
tests/precheck-rollup-v9.6/analyses --out <scratch>/post.tsv`, run against the working tree at
commit `f00ce1a` (parent of this fixture's own commit — the last commit before this plan's own
edits landed).

```text
analysis_id	conclusion_claims	untraced_claims	untraced_flag	verdict_cells	nonconforming_verdict_cells	verdict_flag	chain_blocks	malformed_chain_blocks	chain_flag	dependency_cycles	ungrounded_chains	selfaudit_disagreements	provenance_labels	unmatched_sources	unreadable_sources	literals_checked	unlocated_literals	misattributed_literals	zero_literal_gts	orphan_fetches	provenance_flag	high_conf_chains	high_conf_unverified_head	confidence_inversions	confidence_unparsed	selfaudit_bands_parsed	selfaudit_offvocab_bands	prechecks_parsed	precheck_unparsed	precheck_disagreements	rollups_checked	rollup_inversions
PC-ROLLUP	2	0	0	1	0	0	2	0	0	0	0	2	n/a	n/a	n/a	n/a	n/a	n/a	n/a	n/a	n/a	0	0	0	0	1	0	3	0	1	1	1
```

`precheck_disagreements` reads **1** (the §6 roll-up's label `HIGH` sits above its own stated
`Inputs ceiling: MEDIUM` — `label_above_ceiling`) and `rollup_inversions` reads **1** (the same
roll-up, read independently against its two cited §4 chains' own labels, sits above their
`MEDIUM` minimum — R-52-01's detector, which reaches the same defect even without a pre-check
present). `selfaudit_disagreements` moves **0 → 2**: the widened `_SELFAUDIT_CONTRADICTIONS[5]`
now reconciles the trailing Criterion 5 `Rigorous` claim against both nonzero fields
independently, one `selfaudit_disagreements` entry per contradicting field — this is the trip
D-06 asks for.

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

`analyses/PC-ROLLUP.md` and this README are committed as-is and never regenerated or hand-edited
to match a later result. This directory is registered in `scripts/check-firewall-battery.sh`'s
`_FROZEN_PATHS` array, so an uncommitted edit to any of these tracked files turns the battery RED.

That protection has a documented gap, recorded here so nobody relies on it for something it does
not do: FROZEN-EVIDENCE is a `git diff --quiet HEAD` over the registered pathspec, plus a
separate untracked-files sweep. It catches an edit to a file already tracked at HEAD, and it
catches an untracked file appearing inside the directory — but a committed `git rm` of one of
these files passes it clean. It is tamper-evidence for modification, not a deletion guard. Any
change to this fixture's committed contents, including removal, must be reviewed in-diff like any
other commit; nothing here enforces that automatically.
