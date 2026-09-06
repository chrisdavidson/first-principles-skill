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

## Why every item carries an in-file marker

**Decision: `add-marker`. Date: 2026-09-05. Decider: Christopher Davidson.**

Eight of the thirteen items (`t01`, `t02`, `t07`, `t08`, `t09`, `t11`, `t12`, `t14`) are
near-byte-identical falsified copies of shipped `shared/examples/*.md` exemplars, keeping the
source file's `# Worked Example: …` title and preamble verbatim -- `t12` diverges from its shipped
original (`shared/examples/product-business.md`) by only 2 lines out of 94, confirmed by reading
the first ten lines of each side by side. `t02` additionally carries a fabricated SKF
bearing-catalogue citation labelled `*Provenance: read-at-source.*` -- the exact marker PROV-GUARD
treats as a verified-source claim -- with nothing inside the file (before this change) saying it is
invented.

`19-VERIFICATION.md` did not score this as a requirement failure: CONF-07/CONF-08 as literally
written discharge the "written statement of what is false" obligation through the `catalog.md`
sidecar, which every item already had. `19-REVIEW.md` rated it a blocker (CR-02): a falsified twin
this close to its shipped original is precisely the artifact most likely to be mistaken for the
original in a search result, a diff, a context window, or a copy-paste back into `shared/` or
`first-principles/`. Both readings were defensible; the choice between them was routed to a human
product-safety judgment (plan 19-09, D-19-09-C) rather than decided by the planner.

The risk this closes: without an in-file marker, `grep -rln "^# Worked Example"` returned 14
shipped exemplars and 8 falsified copies with identical titles, indistinguishable from each other
outside of opening `README.md` or `catalog.md` in a sibling directory -- a warning nothing forced a
reader, human or model, to open first.

The fix is the identical two-line Markdown blockquote prepended to all thirteen items (not just the
eight near-identical ones, so the marker's presence does not itself become a signal that
distinguishes "close copy" from "hand-authored" among falsified content), above the `# ` title line
and followed by one blank line:

> **ADVERSARIAL FIXTURE — DELIBERATELY FALSE.** Catalogued falsehood; see `README.md` and
> `catalog.md`. Never quote as fact, never copy into `shared/` or `first-principles/`.

Measurement neutrality was proved by measurement, not assumed from `19-REVIEW.md`'s single-item
(`t01`) check: `python3 scripts/report-conformance.py` was re-run after the edit and the two
regenerated artifacts (`docs/conformance-baseline.md`, `docs/data/conformance.json`) were diffed
byte-for-byte against copies captured before the edit, across **all thirteen** items, not just one.
Both diffs were empty -- the marker moved no reading. `catalog.md`'s sha256 row in the table below
is unchanged; this branch did not edit that file.

## sha256 chain-of-custody table

One row per committed `.md` file in this directory, including `catalog.md`, produced by
`sha256sum tests/adversarial-corpus-v9.0/*.md` as the last edit of plan 19-04.

| File | sha256 |
|---|---|
| `catalog.md` | `e4a355eaad300cf10cfd0e55bc674f1f8950b4872708aa0653d4ba7799d33766` |
| `t01-ledger-arbitrary-chain.md` | `ad47ae04633eb299582cf2095f8df4e3a10136f3a65edf03ad99ac6de436d2aa` |
| `t02-fabricated-read-at-source.md` | `fbc26f04ecc4a3ca8e2285fda44c732f188e394e7cbf109fa0b489b501c520fe` |
| `t03-composition-cycle.md` | `fc8cbc6fd0ed0593008163a3987ef7d4bd50a9ff80b36efb613396e9956f4c1e` |
| `t04-chain-only-head-ungrounded.md` | `56771927a22386766f4ed5bc55b1d78302d6030e2fb206be3cbf2cfcb1cd9bf5` |
| `t05-selfaudit-overclaim-under-cycle.md` | `1cf70bff52bbd478338bdee2037de1dc8fdecac0d2db73e04db4aa099fc51cd4` |
| `t06-hidden-cycle-past-head.md` | `2c645182d70d9a4d1d31786c0439a9d9633312e1a65f1c735e8c9bc181c431e3` |
| `t07-non-sequitur-between-hops.md` | `05d5665c23fb5d416dd60f7708c443331ce484929554ff4f1f09b3c28a00f075` |
| `t08-verdict-contradicts-its-type.md` | `38e44ca028a48753d303ac1d42f5087a10690360574d08fb648d1505e4f5fc17` |
| `t09-arithmetic-does-not-follow.md` | `87ce22ee4390727ba389ff521a7ec6f3a8c7a2edbcc55e1a3597d06a3be46f0b` |
| `t11-fabricated-ground-truth.md` | `ac6a733356a790816156d55a0515b8d0e1036e7d58adc437d4ba30f5069e7f9e` |
| `t12-inline-citation-wrong-chain.md` | `dc5ba58a4d1b43d471325b169849c011fcff257352fdbcc0e95b316ed4406e19` |
| `t13-grounded-alongside-cyclic-ref.md` | `687959d6aba90e601d3c46b7e2e55d164751ac1d9fb64b42bf79ab2e2204b6b5` |
| `t14-order-of-magnitude-conversion.md` | `1aa929a3bd3334b8e5ad38158b3343e2b3ab82b725cb0bfaeab7fcc6c606f4c8` |

`README.md`'s own digest is deliberately absent from this table: a self-hash would be false the
moment it is written, since writing the hash in changes the very bytes the hash would need to cover.
