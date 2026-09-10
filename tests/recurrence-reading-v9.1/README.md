# v9.1.0 Recurrence-Reading Frozen Evidence

**Status: FROZEN read-only evidence — never regenerated, never hand-edited to match a later
result.** Every record file in this directory is a committed reading taken against a named
commit, following `protocol.md`'s sweep rules. A correction to a reading is a fresh,
separately-provenanced record file, not a silent edit of one of these.

## What this directory is

This is the frozen evidence behind `docs/conformance-baseline.md`'s `recurrence-reading` labelled
surface. The published sites/claims figures on that surface are **re-derived** from the record
files committed here by `scripts/report-conformance.py` (plan 27-03) — they are never hand-typed
into the baseline. See `protocol.md` in this directory for the sweep's own rules (surface list,
hit criterion, exclusions, record format, fence classes, trip predicate); they are not restated
here.

## Provenance and chain of custody

This table carries one row per record file this sweep produces, six in total. Filenames, timing
and arm are fixed by `protocol.md`'s `## Record format` section. Before its own plan lands, a
record file's row is legitimately `pending` in every measured column — that is not a defect,
it is the honest state of a reading not yet taken. Plans 27-04 (pre-arm) and 27-09 (post-arm)
fill their own rows in the same commits that add their record files.

| File | Timing | Arm | Reader id | Commit sha read | Isolation mechanism | sha256sum |
|------|--------|-----|-----------|------------------|----------------------|-----------|
| `pre-arm-scanner.md` | pre-arm | scanner | n/a | pending | pending | pending |
| `pre-arm-reader-a.md` | pre-arm | prose | A | pending | pending | pending |
| `pre-arm-reader-b.md` | pre-arm | prose | B | pending | pending | pending |
| `post-arm-scanner.md` | post-arm | scanner | n/a | pending | pending | pending |
| `post-arm-reader-a.md` | post-arm | prose | A | pending | pending | pending |
| `post-arm-reader-b.md` | post-arm | prose | B | pending | pending | pending |

## Reader independence

Each prose reader (A, B) is run as a fresh session whose entire instruction set is `protocol.md`
and the repository, with no access to the other reader's output, no access to the other reader's
session, and no shared scratch state. The specific mechanism used to isolate a given run (for
example, separate agent dispatches with no shared context window) is recorded in that run's own
chain-of-custody row above, not asserted generically here — a generic assertion in this section
would be exactly the unreachable claim `protocol.md`'s hit criterion excludes.

## What was deliberately NOT committed, and why

- **The readers' intermediate scratch notes.** Not evidence — the record file is the reading. A
  scratch note that disagreed with the committed record would only invite a question the record
  file itself already answers.
- **Any candidate site that was examined and excluded.** The exclusion belongs in `protocol.md`'s
  rules, not in a per-site not-a-hit ledger. A not-a-hit ledger would grow without bound and would
  itself carry quantity-shaped claims about how many sites were examined — the exact class this
  sweep exists to measure, reproduced inside its own evidence.

## Amendment rule

A correction is a NEW, separately-provenanced record file with its own chain-of-custody row,
never a silent edit of an existing one. `FROZEN-EVIDENCE` is expected to read RED between writing
a new record file and committing it — that is the mechanism working, not a fault — and must read
GREEN again immediately after the commit lands. Reaching for `git commit --no-verify` to get past
that window is forbidden.

This mirrors `scripts/check-firewall-battery.sh`'s own documented amendment procedure for
`tests/live-conformance-catalog.md` (the one pre-existing `_FROZEN_PATHS` entry whose contents the
design expects to be revised): the freeze is kept deliberately, corrections happen anyway, and the
answer is a new commit that lands the correction and immediately re-satisfies the check — never a
bypassed gate.

## The live-conformance template, and where it does not transfer

`27-CONTEXT.md` D-07 names `tests/live-conformance-v9.0/` as the template for this directory. Its
**mechanism** claim is exactly what this directory implements: freeze human- or agent-produced
evidence once, then derive the published figure from it forever after, so a non-reproducible act
yields a reproducible number. That half of D-07 holds and is unchanged.

Its **file shape** does not transfer, and this supersedes D-07's file-shape reference (D-27-05).
`tests/live-conformance-v9.0/`'s unit is a full `claude -p` session capture — a `.jsonl` transport
dump paired with an extracted `.md` analysis — scored by a document-defect detector
(`detect_defects`). There is no session to capture here and no document for `detect_defects` to
score: this directory's unit is a human-authored sites/claims table, produced by a reader
following `protocol.md`, not by a live agent dispatch. Building `.jsonl`/`.md` pairs for this
directory would be inventing captures that never happened.

The shape adopted instead is `tests/adversarial-corpus-v9.0/catalog.md`'s single machine-parsed
Markdown table, replicated once per (timing x reader/arm) cell per `protocol.md`'s `## Record
format` section — six files, each its own frozen artifact, rather than one shared table with a
reader column. This supersession is stated here explicitly so a later reader is not left to
rediscover the discrepancy between what D-07 names and what this directory actually contains.
