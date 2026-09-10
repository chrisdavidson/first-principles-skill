# Recurrence-reading sweep protocol (v9.1.0, REL-08)

This is the published sweep protocol behind `docs/conformance-baseline.md`'s
`recurrence-reading` labelled surface. It is written for a reader who has never seen this
repository. Follow it exactly; a third reader re-running it against the same commit must land
the same sites figure.

## What is being counted

Instances of the **quantity-shaped claim class**: a claim whose truth is a digit corroborable
against a generated fact. `docs/PROCESS.md` section 2's standing constraint on restated moving
counts is the rule this sweep tests compliance against and reach beyond — cited here, not
restated. The consistency-shaped class (one rule stated two contradictory ways, with no digit to
check) is out of scope for this sweep.

## Surface list

Walk the two tiers below, in the order listed. Record every hit under its own tier; the two
tiers are reported as two figures and are never summed (CONTEXT.md D-02).

### Product tier

Walked in this order:

1. `CLAUDE.md`
2. `README.md`
3. `CONTRIBUTING.md`
4. `CHANGELOG.md`
5. `docs/**/*.md`
6. `shared/**/*.md`
7. `first-principles/**/*.md`

### Apparatus tier

Walked in this order:

1. `scripts/**/*.py` — docstrings and comments only, not executable code
2. `scripts/**/*.sh` — comments only
3. `.github/**`
4. `.planning/**/*.md`

Tier follows `docs/PROCESS.md` section 2's claim-audience cut, cited rather than restated here.

## Hit criterion

A hit is one `file:line` stating a quantity-shaped value — an Arabic digit, or a spelled-out
number, naming a count, size, rate or ordinal over live repository state — that disagrees with
the value the live tree produces, where the live value was obtained by a named, re-runnable
command at reading time.

"I believe this is stale" is not a hit. If you cannot name the command you ran to obtain the
live value, no hit is recorded for that site.

## Exclusions

Six exclusions, each with its reason:

1. **Frozen historical counts** — per `docs/PROCESS.md` section 2's frozen-historical-count
   paragraph, a specific, closed, immutable past state — the same kind of dated plan-and-round
   count that paragraph itself cites as its own worked example — is not a moving count and is
   excluded.
2. **Any value inside a `<!-- GENERATED ... -->` region** — machine-produced; drift there is the
   scanner arm's territory, covered by `scripts/gen-gate-docs.py --check`, not this prose sweep.
3. **Consistency-shaped claims carrying no digit** — out of milestone scope per CONTEXT.md D-E,
   routed to backlog 999.50 / 999.51 rather than counted here.
4. **The version stamps enumerated by `scripts/check-version-stamps.py`, while the release
   bracket is open** — they are the release act's own subject, not a recurrence to sweep for.
5. **`docs/history/`** — git-ignored and absent from a fresh clone, so no third reader can
   reproduce a reading there.
6. **A value explicitly labelled in its own surrounding text as illustrative or as an example** —
   it makes no claim about live state.

## Walk order and de-duplication

Surfaces are walked in the order listed above. Every hit is recorded as found — hits are never
de-duplicated across files. Grouping structurally identical restatements into one distinct claim
is the `distinct claim` column's job (CONTEXT.md D-04), so the sites:claims ratio stays readable
as a breadth-versus-depth signal, not a raw hit count.

## Record format

Six frozen record files, one per (timing x arm) cell:

- `pre-arm-scanner.md`
- `pre-arm-reader-a.md`
- `pre-arm-reader-b.md`
- `post-arm-scanner.md`
- `post-arm-reader-a.md`
- `post-arm-reader-b.md`

Reader id, arm and timing live in each file's header and filename, not in a table column. Each
record file carries one Markdown table with this fixed eight-column header, reproduced verbatim:

| # | file:line | claimed value | live generated value | how derived | tier | fence class | distinct claim |
|---|-----------|----------------|-----------------------|-------------|------|-------------|-----------------|

Each file ends with a line in this exact shape:

```
**Totals this file:** N sites / M distinct claims.
```

Plan 27-03's reader re-derives that total from the parsed table rows and fails on mismatch — the
hand-typed total is corroborated by construction, not trusted on its own.

**The zero-finding case is explicit, not an absence.** A reader who finds nothing still commits
the file, with the table header present, zero rows, and the totals line reading
`0 sites / 0 distinct claims`. An absent file is indistinguishable from a reading never taken and
must never occur once that file's own timing has been measured. Before a timing is measured, its
record files are legitimately absent, and the surface that renders this sweep's results names
that absence explicitly rather than rendering it as a zero.

## Fence classes

Every pre-arm site is classified, at reading time, into exactly one of two fence classes,
recorded in the record's own `fence class` column:

- **FENCED** — byte-frozen through every release act. Any byte change at a FENCED site is a
  fence break, adjudicated at release time and disclosed with its bound — never silently
  absorbed.
- **RELEASE-OWNED** — declared out of the byte-freeze in advance, in writing, because the
  release act mechanically owns the bytes. Exactly four sub-classes qualify, and nothing else
  does:
  (a) a site inside a `<!-- GENERATED ... -->` / `<!-- END GENERATED ... -->` region on any
  surface `scripts/gen-gate-docs.py --write` regenerates;
  (b) a coverage-headline statement on any of the five `COVERED_HEADLINE_SURFACES` registered in
  `scripts/check-traceability.py`;
  (c) one of the version stamps enumerated by `scripts/check-version-stamps.py`;
  (d) `docs/requirements-matrix.md` or `docs/data/matrix.json`.

A RELEASE-OWNED site is still **counted** in the pre-arm figure if it is a recurrence — the class
exempts it from the byte-freeze, never from the measurement. Its post-arm state is re-checked; if
it is still a recurrence after the acts, it counts in the post-arm figure too.

A break on a FENCED site is recorded as `HELD-WITH-DISCLOSED-EXCEPTION` — the existing term from
Phase 23. No new status word is coined for this sweep.

## The trip predicate

`docs/PROCESS.md` section 3 limit 2's same-class trip fires if at least one site appears in the
**union** of the two readers' records — either reader, either tier, either timing — satisfying
all three of:

(a) the claimed value disagrees with the live generated value;
(b) the live value was obtained by a command named in the record and re-runnable by a third
    party;
(c) the site is not excluded under this protocol's own exclusion list above.

Union, not intersection: an intersection would let one reader's miss silently discharge the
other reader's hit.

The published per-reader figures stay per-reader, per-tier, per-timing and unreconciled — the
union above is a separately-stated derived predicate, never a merged figure and never summed
with anything.

A **disputed site** — one reader records it as a hit, the other does not — that is the only site
making the predicate fire must be named as disputed wherever the trip's firing is reported, so a
reader can see the trip rests on one reader's judgement.

## Two instruments, never summed

The scanner arm is the frozen instruments already shipped in this repository:
`run_literal_scan`, `narrative_restatement_problems`, `detail_page_containment_problems` and
`chain_terminus_problems`, all in `scripts/gen-gate-docs.py`. The scanner and prose figures are
published side by side, and **the gap between them is itself the published measurement** of how
far the Phase 26 mechanism reaches versus how much of the class still needs a human reader.

## Prohibition

This protocol may not be executed by running `scripts/gen-gate-docs.py --check` and reporting
its output. That is roadmap criterion 4's explicitly-rejected shape wearing a human-in-the-loop
costume. A reader whose findings are exactly the scanner's findings has not run this protocol —
the whole reason two instruments are reported side by side is that the scanner cannot find an
instance outside its own reach, and a prose read that only reproduces the scanner's population
proves nothing.

## Reproducibility clause

A third reader re-running this protocol against the same commit must land the same sites figure.
Where two readers legitimately diverge, the divergence is a measurement of how much of the
figure is judgement (CONTEXT.md D-05) and is published as such. Where a third reader cannot
reproduce either figure, this protocol's own text is the defect, not the reader.
