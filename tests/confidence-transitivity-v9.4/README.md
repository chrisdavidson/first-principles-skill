# v9.4 Confidence-Transitivity Fixture — backlog 999.119

**Captured:** 2026-09-16. **Status:** FROZEN read-only evidence — never regenerated, never
hand-edited to match a later result. `catalog.md` carries the D-09 pilot prompt and the eleven
capture rows; `read-qualifying.py` is the fixture reader; the ten `.jsonl`/`.md` pairs
(`CT-B1`..`CT-B5`, `CT-A1`..`CT-A5`) plus the pilot pair (`CT-P1`) are the raw captures and their
extracted analyses. All thirteen files, plus this README, are committed as-is; any correction to
this evidence is a fresh, separately-provenanced capture, not a silent edit of this one.

## What this is

The D-09 prompt was designed to elicit a chain whose head cites only MEDIUM chains and no `GT-N?`
— the qualifying shape backlog 999.119 exists to catch (DEMO-TRIAGE's C8 is the N=1 instance of
this shape, HIGH over three MEDIUM chains with no `GT-N?` in its own head). It was captured five
times before the ceiling clause was added to the rule text (D-10) and five times after (D-11),
with one pilot capture (`CT-P1`) taken first to confirm the shape was reproducible at all. See
`catalog.md` for the full prompt text and the pre-registered definitions of Q, K, and
`ceiling_bound_mixed`; see `read-qualifying.py` for the reader that computes them.

## Origin runs and chain of custody

- **Before-leg repo HEAD:** `1bab9e0` — the parent of plan 42-01's own test commit (`82ef1cb`),
  i.e. the tree exactly as it stood before any of this phase's shipped-text edits.
- **After-leg repo HEAD:** `3878030` — the `fix(42): cap a chain's confidence at the lowest-rated
  chain its head cites (999.119)` commit, before any version bump.
- **Plugin version for both legs:** `9.3.1` (all 17 stamps agree, `check-version-stamps.py` PASS,
  confirmed immediately before and after every dispatch in both legs).
- **Served model for both legs:** `claude-opus-5` for all eleven captures (`CT-P1`, `CT-B1`..`CT-B5`,
  `CT-A1`..`CT-A5`), read from each capture's own transcript. `claude` CLI: `2.1.273`.
- **Exact transport**, identical in both legs (only the probe ID and the tree state differ):

```bash
ANTHROPIC_MODEL=claude-opus-5 python3 scripts/check-quality-harness.py --probe <ID> \
    --catalog tests/confidence-transitivity-v9.4/catalog.md \
    --plugin-dir first-principles --out <scratch>
```

- **sha256 table**, every `.jsonl` and `.md` in this directory, including the pilot:

| File | sha256 |
|---|---|
| `CT-P1.jsonl` | `d5734ce5d7f6ec2ed76dc3ca98a6bb4afea87e19a44f7a88a765b31b61bf76e3` |
| `CT-P1.md` | `2cfa77b01c281b5834c788c8c06ab9ae75a9768696b9575d178c26320c8282eb` |
| `CT-B1.jsonl` | `07157cac030813596e7f2c874f8877160715297161e59c1a24702607986b91f3` |
| `CT-B1.md` | `d7d828c353d484cc6315904c7c4866d554722a75efd7beb3e4257d1c1757632b` |
| `CT-B2.jsonl` | `61825f05c2a6000ffe0547ab4a07564dae84adeb7e7050a8806d592b68dd252e` |
| `CT-B2.md` | `2d1bdf57cf834aae3f0dd3d2e36b8d30ec70d8a79ea097c80113a3480809b98f` |
| `CT-B3.jsonl` | `f6421aa467b32ecbba016befbfcc77d38b0633cf5cc3fcc972634cc2f6c208bf` |
| `CT-B3.md` | `729b39545d35919f6e94ddfc3c3d4d54d83879117666caf9244ed266c6b45d50` |
| `CT-B4.jsonl` | `67ed3c382c20d59971a52ce0fd4bf0be897fbc1b54193ebd014ee99b21fb1953` |
| `CT-B4.md` | `99fe98a4eea17aea82364708cab778f19f16b72debffc209e41027ec21434033` |
| `CT-B5.jsonl` | `2e8f474bcb3220be4fca7ded0d2c0e1e4fc5e00dc6aacd80c97f8c25105615c3` |
| `CT-B5.md` | `66e2d8fc8b46ef504d3ddf2377b890d33fa3fe918c999c3f10ab7089fb8c3ecb` |
| `CT-A1.jsonl` | `45a8dca4c1f8aba52029a363b3b8b49b8bd2782ae53e2894737667ee56ab44be` |
| `CT-A1.md` | `345cb52dde741d223d7c581c9169bf607c67fdfd3648ffeef4f8cad32a426697` |
| `CT-A2.jsonl` | `e7e4b57d2e6a167052886df477ff65d7774248495a97886824acd7974cb8dc7a` |
| `CT-A2.md` | `8b95bc03d4b25e647b1c352b138e38d5cf3d38c23dbfb1fc20288e9a768e8057` |
| `CT-A3.jsonl` | `35ade9818062bda6fa6fc1cbddc923cf092249d9aa8529957a0060c7bb721524` |
| `CT-A3.md` | `abd88fe73742a4bbea4d69bf259ace56f5ab5209b93598278cd6ecc8dc4476ea` |
| `CT-A4.jsonl` | `db62d980302e3eaeba794edab12f6c5bde7242e1f154b38dd50bfce67d816f39` |
| `CT-A4.md` | `94a754857eaf912499d6af6b6772fba87e3fd4637adb917f4a8d456129717a1b` |
| `CT-A5.jsonl` | `07a19805d8520b2c1e63718fa8b9efc3f45f95757b312ed8ba234675281e62a4` |
| `CT-A5.md` | `534e049c3f28d613bb1bc74aa789bb8085723e205c03afd696e82c102f1f7e17` |

Every row above was verified via `cmp` returning exit 0 for the scratch→committed pair, and via
`sha256sum` producing the identical digest on both the scratch original and the committed copy —
not verified by size alone.

**On the pilot.** `CT-P1` was dispatched once, before the before leg, to confirm the D-09 shape was
reproducible at all (D-09's own pilot protocol: one pilot capture, revise once if the shape does
not appear, escalate if it still does not). The shape appeared on the first capture (chain C9 cites
`C4 + C5 + C6 + C7 + C8`, all independently MEDIUM, no `GT-N?` on C9's own head), so no revision was
needed. `CT-P1` is frozen here as the record of that pilot decision. It is **excluded from K and Q
in both legs** — it was captured against the pre-edit tree, before the before leg's own five
captures, and counting it would double-count one of the eleven generations under a different
label than the five-per-leg design the catalog's decision record states.

## Reading method

```bash
python3 tests/confidence-transitivity-v9.4/read-qualifying.py <dir> --jsonl-dir <dir>
```

prints a TSV plus the summary lines `Q=`, `K=`, `NO_QUALIFYING=` and
`UNREADABLE_OR_UNPAIRABLE=`. `read-qualifying.py` is a fixture reader that reuses
`scripts/check-quality-harness.py`'s own chain-block/label parsers read-only via
`importlib`; it is **not** a registered gate, and no CI job or battery member invokes it.

**Positive control** — the frozen `tests/reference-reads-v9.2.1/DEMO-TRIAGE.md`:

```
capture	model	outcome	readable	chain_blocks	unpairable	confidence_inversions	qualifying	qualifying_count	qualifying_high	qualifying_unlabelled	ceiling_bound_mixed	k_reading
DEMO-TRIAGE	n/a	n/a	yes	8	no	1	c8=HIGH	1	1	0	0	no
Q=1	K=0	NO_QUALIFYING=0	UNREADABLE_OR_UNPAIRABLE=0
```

**Negative control** — a scratch copy of `DEMO-TRIAGE.md` with C8's heading relabelled from
`*(HIGH)*` to `*(MEDIUM)*`:

```
capture	model	outcome	readable	chain_blocks	unpairable	confidence_inversions	qualifying	qualifying_count	qualifying_high	qualifying_unlabelled	ceiling_bound_mixed	k_reading
DEMO-TRIAGE-MEDIUM	n/a	n/a	yes	8	no	0	c8=MEDIUM	1	0	0	0	yes
Q=1	K=1	NO_QUALIFYING=0	UNREADABLE_OR_UNPAIRABLE=0
```

Relabelling C8 from HIGH to MEDIUM flips `confidence_inversions` 1 → 0 and `k_reading` no → yes,
confirming the reader is not vacuous.

## Readings

Before-leg TSV (`CT-B1`..`CT-B5`, pilot excluded):

```
capture	model	outcome	readable	chain_blocks	unpairable	confidence_inversions	qualifying	qualifying_count	qualifying_high	qualifying_unlabelled	ceiling_bound_mixed	k_reading
CT-B1	claude-opus-5	completed	yes	5	no	0	-	0	0	0	0	n/a
CT-B2	claude-opus-5	completed	yes	6	no	1	-	0	0	0	0	n/a
CT-B3	claude-opus-5	completed	yes	8	no	0	-	0	0	0	0	n/a
CT-B4	claude-opus-5	completed	yes	7	no	1	-	0	0	0	0	n/a
CT-B5	claude-opus-5	completed	yes	7	no	0	-	0	0	0	0	n/a
Q=0	K=0	NO_QUALIFYING=5	UNREADABLE_OR_UNPAIRABLE=0
```

After-leg TSV (`CT-A1`..`CT-A5`):

```
capture	model	outcome	readable	chain_blocks	unpairable	confidence_inversions	qualifying	qualifying_count	qualifying_high	qualifying_unlabelled	ceiling_bound_mixed	k_reading
CT-A1	claude-opus-5	completed	yes	5	no	0	-	0	0	0	0	n/a
CT-A2	claude-opus-5	completed	yes	6	no	0	-	0	0	0	0	n/a
CT-A3	claude-opus-5	completed	yes	6	no	0	-	0	0	0	1	n/a
CT-A4	claude-opus-5	completed	yes	6	no	0	-	0	0	0	0	n/a
CT-A5	claude-opus-5	completed	yes	7	no	0	-	0	0	0	0	n/a
Q=0	K=0	NO_QUALIFYING=5	UNREADABLE_OR_UNPAIRABLE=0
```

Comparison table (from `42-EVIDENCE.md`):

| Column | Before leg (`CT-B1`..`CT-B5`) | After leg (`CT-A1`..`CT-A5`) | Frozen DEMO-TRIAGE |
|---|---|---|---|
| Q (captures with a qualifying chain) | 0 | 0 | 1 |
| K (qualifying chains rated MEDIUM or lower) | 0 | 0 | 0 |
| No-qualifying-chain count | 5 | 5 | 0 |
| Incomplete/unreadable/unpairable count | 0 | 0 | 0 |
| `confidence_inversions` (summed) | 2 (`CT-B2`=1, `CT-B4`=1) | 0 | 1 (`c8`) |
| `qualifying_high` (summed) | 0 | 0 | 1 (`c8=HIGH`) |
| `ceiling_bound_mixed` (summed, supplementary) | 0 | 1 (`CT-A3`) | 0 |

`K_before/Q_before = 0/0`. `K_after/Q_after = 0/0`. The frozen DEMO-TRIAGE reading:
`confidence_inversions = 1`, `c8=HIGH` (C8 cites `C3 (MEDIUM) + C6 (MEDIUM) + C5 (MEDIUM)`, no
`GT-N?`, and is itself rated HIGH) — reported alongside, not regenerated (D-15).

### Finding

Neither leg reproduced the D-09 qualifying shape (a HIGH chain whose head cites only MEDIUM `Cn`
chains, no `GT-N?` on that head) across five fresh generations. `Q_after` is 0, and
`K_after/Q_after` (0/0) is not above `K_before/Q_before` (0/0) — both trigger conditions in the
plan's pre-registration check. This is written plainly as a finding against the fix's reach, not
re-read as a pass: the before leg's own denominator is 0, so this after-leg reading has no
non-zero before-leg base to compare against, and no ratio comparison is possible in either
direction. The finding is scoped narrowly to what the K-of-5 legs show: five fresh generations on
each side of the edit did not reproduce the shape the pilot (`CT-P1`) and the frozen DEMO-TRIAGE
fixture (`C8`) both showed on other occasions. It is not evidence that the shipped ceiling clause
fails to work — `CT-A3`'s mixed-rank chain (C6, HIGH+MEDIUM inputs) and its `GT-N?`-naming chain
(C7) both show the model correctly capping and naming inherited MEDIUM inputs when a related shape
arises, and a direct instrument check against DEMO-TRIAGE (recorded in `42-EVIDENCE.md`) already
confirmed the shipped rule text names C8's exact violation.

K-of-5 is a recorded observation, never a gate (`docs/v8.7-constraint-teardown.md` §2 item 3, "the
S-P04 vector swung 2/5 → 0/5 → 2/5 across three measurements with no source change"). At N=5, noise
can equal effect — this reading, on both sides, is stated with that limit attached rather than read
as either a pass or a disproof.

## Why registering this path is not a new gate

FROZEN-EVIDENCE (`scripts/check-firewall-battery.sh`) is an inline check whose
`TOTAL=$((TOTAL + 1))` line fires exactly once, unconditionally, regardless of how many entries
`_FROZEN_PATHS` carries — the increment is not inside any loop over the array. Registering this
directory's path as one more `_FROZEN_PATHS` entry therefore does not add a new battery member: the
battery's total gate count and CI job count are unaffected by this registration. For the current
battery/CI population figures, see `CLAUDE.md`'s generated gate table — this README deliberately
states no bare digit of its own for that population, per `docs/PROCESS.md` §2's standing constraint
on moving counts (a digit copied here would go stale the next time either total moves, exactly the
defect class the rest of this repository's apparatus exists to prevent).

## Frozen-evidence discipline

`catalog.md`, `read-qualifying.py`, `CT-P1.jsonl`, `CT-P1.md`, `CT-B1.jsonl`..`CT-B5.md`,
`CT-A1.jsonl`..`CT-A5.md`, and this README are committed as-is and never regenerated or
hand-edited to match a later result. This directory is registered in
`scripts/check-firewall-battery.sh`'s `_FROZEN_PATHS` array, so an uncommitted edit to any of these
tracked files turns the battery RED.

That protection has a documented gap, recorded here so nobody relies on it for something it does
not do: FROZEN-EVIDENCE is a `git diff --quiet HEAD` over the registered pathspec, plus a separate
untracked-files sweep. It catches an edit to a file already tracked at HEAD, and it catches an
untracked file appearing inside the directory — but a committed `git rm` of one of these files
passes it clean. It is tamper-evidence for modification, not a deletion guard. Any change to this
fixture's committed contents, including removal, must be reviewed in-diff like any other commit;
nothing here enforces that automatically.
