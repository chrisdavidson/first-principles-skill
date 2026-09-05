# Adversarial corpus v9.0 — false-negative-rate fixture

**Status: FROZEN read-only evidence — never regenerated, never hand-edited to match a later
result.** Every `.md` item in this directory is **deliberately false content**: it is a form-clean
analysis, under the unmodified, CONTRACT-06-frozen `detect_defects`, that is substantively wrong.
Nothing here is a fact, a recommendation, or a template. No item's prose may ever be quoted as fact
or copied into `shared/` or `first-principles/` — doing so would ship a fabricated ground truth, a
wrong-chain citation, or a two-orders-of-magnitude arithmetic error as shipped content.

## Origin and chain of custody

The thirteen items were authored in three plans, each producing disjoint filenames so the work ran
fully in parallel with zero shared state:

1. **Plan 19-01** authored `t01`, `t07`, `t09` and `t12` — including the 999.2 seed case (`t01`),
   the LEDGER-01 falsehood in its original closure-ledger form. All four are `derived:` items —
   copied verbatim from a shipped `shared/examples/*.md` exemplar that already measured 0/0/0 under
   Phase 18, then edited by a single surgical passage so the falsehood is content, never form.
2. **Plan 19-02** authored `t02`, `t08`, `t11` and `t14` — the corpus's single stratum-B1 item
   (`t02`, a fabricated `read-at-source` provenance citation) plus three stratum-B2 items broadening
   the falsehood families a form-clean detector cannot see. Also `derived:` items, same method.
3. **Plan 19-03** authored `t03`, `t04`, `t05`, `t06` and `t13` — the five stratum-A items. These
   are `hand-authored`: none of the fourteen Phase-18 exemplars uses the GAP-6 composition chain
   head (`GT-n (label) + Cm (label) → … → …`) a stratum-A item needs to reach `dependency_cycles` or
   `ungrounded_chains`, so a small text edit could not produce one.

Per-item provenance — which plan authored it, and for a `derived:` item, which exemplar it was
copied from — lives in `catalog.md`'s `Source` column, not restated here. A reader who wants to
reproduce any single item's derivation should start there.

## Why the items are committed in full rather than excerpted

`detect_defects` raises `SectionResolutionError` unless all six section numbers resolve, in
ascending order, with no gaps. A `## 4.` + `## 6.` excerpt would be unmeasurable under the same
detector this corpus exists to probe, and an unmeasurable item is not a probe — it is discarded
before it can be scored. Every item here is therefore a complete six-section analysis, committed
byte for byte as produced.

## Why no existing fixture can substitute

The fourteen `shared/examples/` exemplars are the shipped **positive** control — driven to 0/0/0 by
Phase 18, they establish what "reads clean" means when the analysis really is sound. This corpus is
the deliberately-wrong **negative** probe set the false-negative rate needs on the other side of the
ledger. A false-negative rate is a statement about both: how often something genuinely wrong reads
clean. Neither surface can play the other's role, and no other fixture directory in this tree pairs
form-clean construction with a stated, catalogued falsehood the way this one does.

## The corpus has no generated twin, deliberately

This directory is a test fixture, not a shipped artifact: nothing under `shared/` produces it, and
`sync-content.py` never emits it. There is therefore no second surface for it to agree with, and the
corpus section of `docs/conformance-baseline.md` carries no pair-agreement row the way the
`shared-examples` / `generated-twin` surfaces do. This is stated here positively, not left for a
reader to notice as an omission.

## A stratum-A item is allowed to score non-clean

CONF-07's form precondition is that `malformed_chain_blocks`, `nonconforming_verdict_cells` and
`untraced_claims` all read zero on every item here — that precondition is form-cleanliness, and it
holds corpus-wide. `dependency_cycles`, `ungrounded_chains` and `selfaudit_disagreements` are **not**
form checks; they are the three columns with genuine substantive reach, and this corpus's stratum-A
positive controls (`t03`, `t04`, `t05`) are built to fire on them on purpose. Driving those three
columns to zero across the corpus would destroy the phase's only non-tautological signal — a corpus
that scored fully clean on every axis by construction would make the published rate a tautology
rather than a measurement.

## Frozen-evidence discipline

`tests/adversarial-corpus-v9.0` is registered in `scripts/check-firewall-battery.sh`'s
`_FROZEN_PATHS` array (see the sequencing note below for exactly when). FROZEN-EVIDENCE runs a
`git diff --quiet HEAD` over that pathspec, plus a `git status --porcelain --untracked-files=all`
sweep over the same paths, so both an edit to an already-tracked file and a new file appearing
inside this directory turn the battery RED. That protection has one documented gap, carried over
unchanged from the `tests/quality-provenance-v8.24/` and `tests/quality-ledger-v8.26/` precedents: a
committed `git rm` of one of these files is in HEAD by the time the check runs, so no worktree
comparison ever sees it — the check is tamper-evidence for **modification and addition**, never a
deletion guard. Any change to this fixture's committed contents, including removal, must be reviewed
in-diff like any other commit; nothing here enforces that automatically.

**Sequencing note:** this fixture was created by plans 19-01 through 19-04, and plan 19-07
registered it — `scripts/check-firewall-battery.sh`'s `_FROZEN_PATHS` array now carries
`tests/adversarial-corpus-v9.0`, so both FROZEN-EVIDENCE legs described above cover this directory
today: the `git diff --quiet HEAD` sweep catches an edit to any file already tracked here, and the
`git status --porcelain --untracked-files=all` sweep catches a new file appearing inside it. The
residual is unchanged by registration and is restated rather than reopened: a committed `git rm` of
one of these files is in HEAD by the time the check runs, so no worktree comparison ever sees it —
the protection is tamper-evidence for modification and addition, never a deletion guard.

**The working rule for an editor.** FROZEN-EVIDENCE compares the worktree and index against HEAD,
never against some prior state — so a deliberate, committed correction to a corpus item passes the
check cleanly. The protection is tamper-evidence in review, not an edit lock. Any such correction
must move that file's sha256 row in the table below in the same commit, or the table itself goes
stale relative to the bytes it claims to describe.

## sha256 chain-of-custody table

One row per committed `.md` file in this directory, including `catalog.md`, produced by
`sha256sum tests/adversarial-corpus-v9.0/*.md` as the last edit of plan 19-04.

| File | sha256 |
|---|---|
| `catalog.md` | `e4a355eaad300cf10cfd0e55bc674f1f8950b4872708aa0653d4ba7799d33766` |
| `t01-ledger-arbitrary-chain.md` | `7a4ccb0a4c5fc946b33b52008e0dad143fc69a8ff8ad1217bbae44d7fe1ac1bc` |
| `t02-fabricated-read-at-source.md` | `dc2b05f2e6fdb739ecf39ce93f5d4af5ce7005552c664b9108b221d6173b7460` |
| `t03-composition-cycle.md` | `0ca685c530ac2feb878fe50970dff0a3efee003d265b7dc154d60a010e543b99` |
| `t04-chain-only-head-ungrounded.md` | `56f57e06dd096f7e7eb3c2f6403e2c799f6ddb154291c74375efe7ee26aa1b21` |
| `t05-selfaudit-overclaim-under-cycle.md` | `31277a509cc0a3ad52da333145ce82eb48446dae79c7e50783171638554a2ed9` |
| `t06-hidden-cycle-past-head.md` | `836a35eac376e10d1366a415bd7ba1106ac251bdf1302d8bd3969644acc4c1cc` |
| `t07-non-sequitur-between-hops.md` | `cfae09f9dbc33abbb6d1b8e4f24b73f036a594c3fdaa8c5f5c80ee4b37e32d3d` |
| `t08-verdict-contradicts-its-type.md` | `6e390444b8d1d303976ae955df07ce77da77cb336c631c1e1102d483241bacaa` |
| `t09-arithmetic-does-not-follow.md` | `93a56abddeecac07ae3ef0d210e051b448f60e576cedef18232db5eebef7079d` |
| `t11-fabricated-ground-truth.md` | `a7a37aa88fe0be96e03564ca99ec3ef5c518507340e7fc8697b9b81cbc0e229a` |
| `t12-inline-citation-wrong-chain.md` | `0cd68475537f0e1e5a47e931cc427f867f1a8b5b3507b963f789ba2d277f0b01` |
| `t13-grounded-alongside-cyclic-ref.md` | `2e0814a72ca4b7eb99b252599f5531010899009bcd55e04ac6735146c2157329` |
| `t14-order-of-magnitude-conversion.md` | `6e6007f266bf8e93111bdf4b705112b2916842056fa1557668cd822f78cc3616` |

`README.md`'s own digest is deliberately absent from this table: a self-hash would be false the
moment it is written, since writing the hash in changes the very bytes the hash would need to cover.
