# v9.6 Hop-Validity Fixture — backlog 999.138 / OBS-03, roadmap SC2

**Synthetic fixture, not evidence of model behaviour.** `analyses/HV-ARITH.md` and
`analyses/HV-NONSEQ.md` are hand-authored directly against
`shared/spine/references/output-template.md`'s chain-hop shape — neither is a live agent
capture. They exist to demonstrate, with both readings taken by actually running the two
harness versions, that the pre-Phase-53 `detect_defects` reads `HV-ARITH.md` clean and the
Phase 53 `detect_defects` trips it on Criterion 4 (D-01's mechanical evidence leg; roadmap SC2:
"evidenced by a fixture that moves, not by the prose alone").

## The defect and where it sits

`analyses/HV-ARITH.md` carries two §4 chains. C1's first hop is correct (`40 × 150 = 6,000 km`)
and its second, chained hop is out of the narrow parser's binary-only reach
(`40 × 150 × 5 = 30,000 km`, three operators — counted `unparsed`, never silently read as a
mismatch). C2's endpoint-bearing hop states `6,000 × 0.25 = 1,200 L`; the true product is
`1,500`, the D-01 defect the endpoint depends on. A trailing legacy self-audit block claims
`**Criterion 4: Reason Upward**` / `Band: **Rigorous**` over the whole document.

`analyses/HV-NONSEQ.md` carries one §4 chain whose endpoint-bearing hop's arithmetic is correct
(`200 − 180 = 20 ms`) but does not follow: 20 ms of headroom today says nothing about latency
after traffic doubles again. It also claims a trailing `Rigorous` self-audit over Criterion 4.
This is the D-04 pure-non-sequitur case — see "The non-sequitur arm (D-04)" below.

## Which control pins it

`scripts/check-quality-harness.py`'s `_selftest_defects` control **(P30)** reads both files
directly (via the `_HOP_VALIDITY_FIXTURE_DIR` module constant) and asserts the exact
new-harness per-field values recorded in the "New-harness reading" TSV below for both rows,
plus that HV-ARITH's single `_selfaudit_disagreements` entry has `criterion == 4` and
`contradicted_by == "hop_arithmetic_mismatches"`, and its single mismatch has `stated == 1200`
and `computed == 1500`; and that HV-NONSEQ's `hop_arithmetic_mismatches` and
`selfaudit_disagreements` both read 0 — the pinned disclosed bound (P29) already reads
`HV-ARITH.md` end to end for its own narrower Criterion 4 join; (P30) is the fixture-directory
control that pins both files' full field sets together, matching (P24)'s shape for the
precheck/roll-up fixture.

## Both harness readings

Both readings were produced by actually running `scripts/check-quality-harness.py
--detect-defects tests/hop-validity-v9.6/analyses --out <path>` — the pre-Phase-53 leg inside a
detached `git worktree` checked out at the 53-01 fixture commit, the new-harness leg against the
working tree at this fixture's own parent commit. Neither reading is inferred; both TSVs below
are pasted verbatim. Local scratch paths in the printed `--out` confirmation line are replaced
with `<scratch>` and disclosed as replaced; no other rewriting was done.

### Pre-Phase-53 reading

**Command:** `python3 <scratch>/pre53/scripts/check-quality-harness.py --detect-defects
tests/hop-validity-v9.6/analyses --out <scratch>/pre53.tsv`, run inside a detached worktree
(`git worktree add --detach <scratch>/pre53 78e1d7a`) — `78e1d7a`, the 53-01 fixture commit
(parent `d250539`, the phase base). Confirmed first that `scripts/check-quality-harness.py` is
byte-unchanged between `d250539` and `78e1d7a` (`git diff --quiet d250539 78e1d7a --
scripts/check-quality-harness.py`, exit 0).

```text
analysis_id	conclusion_claims	untraced_claims	untraced_flag	verdict_cells	nonconforming_verdict_cells	verdict_flag	chain_blocks	malformed_chain_blocks	chain_flag	dependency_cycles	ungrounded_chains	selfaudit_disagreements	provenance_labels	unmatched_sources	unreadable_sources	literals_checked	unlocated_literals	misattributed_literals	zero_literal_gts	orphan_fetches	provenance_flag	high_conf_chains	high_conf_unverified_head	confidence_inversions	confidence_unparsed	selfaudit_bands_parsed	selfaudit_offvocab_bands	prechecks_parsed	precheck_unparsed	precheck_disagreements	rollups_checked	rollup_inversions
HV-ARITH	2	0	0	1	0	0	2	0	0	0	0	0	n/a	n/a	n/a	n/a	n/a	n/a	n/a	n/a	n/a	2	0	0	0	1	0	3	0	0	1	0
HV-NONSEQ	2	0	0	1	0	0	1	0	0	0	0	0	n/a	n/a	n/a	n/a	n/a	n/a	n/a	n/a	n/a	1	0	0	0	1	0	2	0	0	1	0
```

No `hop_arithmetic_*` column exists at all at this commit — the detector is a Phase 53
addition. `selfaudit_disagreements` reads **0** on both rows: the legacy harness has no field
to reconcile the trailing Criterion 4 `Rigorous` claim against, so it passes both fixtures
clean.

### New-harness reading

**Command:** `python3 scripts/check-quality-harness.py --detect-defects
tests/hop-validity-v9.6/analyses --out <scratch>/post53.tsv`, run against the working tree at
commit `d66612f` (53-04's commit — the last commit before this plan's own edits landed).

```text
analysis_id	conclusion_claims	untraced_claims	untraced_flag	verdict_cells	nonconforming_verdict_cells	verdict_flag	chain_blocks	malformed_chain_blocks	chain_flag	dependency_cycles	ungrounded_chains	selfaudit_disagreements	provenance_labels	unmatched_sources	unreadable_sources	literals_checked	unlocated_literals	misattributed_literals	zero_literal_gts	orphan_fetches	provenance_flag	high_conf_chains	high_conf_unverified_head	confidence_inversions	confidence_unparsed	selfaudit_bands_parsed	selfaudit_offvocab_bands	prechecks_parsed	precheck_unparsed	precheck_disagreements	rollups_checked	rollup_inversions	hop_arithmetic_checked	hop_arithmetic_unparsed	hop_arithmetic_mismatches
HV-ARITH	2	0	0	1	0	0	2	0	0	0	0	1	n/a	n/a	n/a	n/a	n/a	n/a	n/a	n/a	n/a	2	0	0	0	1	0	3	0	0	1	0	2	1	1
HV-NONSEQ	2	0	0	1	0	0	1	0	0	0	0	0	n/a	n/a	n/a	n/a	n/a	n/a	n/a	n/a	n/a	1	0	0	0	1	0	2	0	0	1	0	1	0	0
```

`hop_arithmetic_checked`/`_unparsed`/`_mismatches` read **2/1/1** for HV-ARITH: C1's first hop
(`40 × 150 = 6,000`) and C2's endpoint hop (`6,000 × 0.25 = 1,200`, stated 1,200 vs. computed
1,500) are both `checked`, C1's second, chained hop (`40 × 150 × 5 = 30,000`) is `unparsed`
(reason `chained`), and C2's hop is the single `mismatch`. `selfaudit_disagreements` moves
**0 → 1**: the widened `_SELFAUDIT_CONTRADICTIONS[4]` now reconciles the trailing Criterion 4
`Rigorous` claim against `hop_arithmetic_mismatches` — this is the trip D-01 asks for.
HV-NONSEQ reads **1/0/0**: its one hop (`200 − 180 = 20`) is `checked` and passes (the
arithmetic is correct), so `hop_arithmetic_mismatches` and `selfaudit_disagreements` both stay
**0** — the detector cannot see, and does not claim to see, a non-sequitur with correct
arithmetic. See the next section.

## The non-sequitur arm (D-04)

HV-NONSEQ reads identically under both harnesses — `selfaudit_disagreements 0` on both TSV
rows above — because no column this detector (or any prior one) computes can see a hop whose
arithmetic recomputes correctly but whose inference does not follow from it. This is the
detector's disclosed bound, stated by D-02/D-03: the arithmetic arm recomputes numbers, not
inference validity. SC2's "moves" claim rests on the arithmetic arm (HV-ARITH, above); the
non-sequitur arm is disclosed as observation-only, never claimed as a second mechanical trip.

Its evidence is the model-graded observation recorded under `observation/` — see
`observation/reading.txt`. One pinned model (`claude-opus-5`), N=3 single-turn calls per rubric
arm (six calls total, run sequentially, one at a time), graded HV-NONSEQ's quoted hop under the
pre-Phase-53 Criterion 4 text ("before") and the Phase 53 Criterion 4 text ("after"). The
per-arm tally:

```
before arm (old Criterion 4 text): Sound 3/3, Rigorous 0/3, Hand-wavy 0/3, Absent 0/3
after  arm (new Criterion 4 text): Hand-wavy 3/3, Rigorous 0/3, Sound 0/3, Absent 0/3
```

Every before-arm call graded the hop Sound; every after-arm call graded the identical hop
Hand-wavy, tracking the rubric text each arm was given. This is an observation, not a gate —
`observation/reading.txt` states plainly what a 3/3-vs-3/3 split at N=3 can and cannot show: it
shows this model, on this one fixture, grades the non-sequitur differently under the two rubric
texts; it does not show how the agent grades its own live output (999.147's job), and it is not
statistical proof at this sample size. Nothing in this repository gates on it.

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

`analyses/HV-ARITH.md`, `analyses/HV-NONSEQ.md`, everything under `observation/`, and this
README are committed as-is and never regenerated or hand-edited to match a later result. This
directory is registered in `scripts/check-firewall-battery.sh`'s `_FROZEN_PATHS` array, so an
uncommitted edit to any of these tracked files turns the battery RED.

That protection has a documented gap, recorded here so nobody relies on it for something it does
not do: FROZEN-EVIDENCE is a `git diff --quiet HEAD` over the registered pathspec, plus a
separate untracked-files sweep. It catches an edit to a file already tracked at HEAD, and it
catches an untracked file appearing inside the directory — but a committed `git rm` of one of
these files passes it clean. It is tamper-evidence for modification, not a deletion guard. Any
change to this fixture's committed contents, including removal, must be reviewed in-diff like any
other commit; nothing here enforces that automatically.
