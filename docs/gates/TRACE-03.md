# TRACE-03: Offline traceability gate self-test — capability/tier schema, artifact resolution, plus the HEADLINE-LOCK sentinel asserting the published coverage headline against five named current-fact surfaces and both tracked matrix artifacts.

<!-- GENERATED:FACTS -->
## Facts

- `scan_globs` (4): `docs/*.md`, `CLAUDE.md`, `CHANGELOG.md`, `README.md`
- `registered_surfaces` (5): `CLAUDE.md`, `docs/COMPONENT-DIAGRAM.md`, `docs/MEASUREMENT-MAP.md`, `docs/README.md`, `docs/requirements-traceability.md`
- `branch_roster` (19): `0`, `a`, `b`, `c`, `d`, `e`, `f`, `f2`, `g`, `h`, `h2`, `i`, `i2`, `i3`, `j`, `k`, `l`, `m`, `n`
- `branch_count`: `19`
- `locked_constants` (4 entries): `headline_lock_stage_names`='_headline_lock_preamble | _headline_lock_surfaces | _headline_lock_scan | _headline_lock_doc_rows', `historical_exempt_files`='CHANGELOG.md | docs/v8.0-final-closure.md', `selftest_anchor_prefixes`='_selftest_ | _self_test_', `trace03_doc_rows`='CLAUDE.md | docs/ARCHITECTURE.md'
- `coverage_headline` (2 entries): `prose`='225 reproducible / 110 audit-only / 0 gap / 335 total', `slash`='225/110/0/335'
<!-- END GENERATED:FACTS -->

<!-- GENERATED:HOW-TO-RUN -->
## How to run

```sh
python3 scripts/check-traceability.py --self-test
```

CI job: `check-traceability`
<!-- END GENERATED:HOW-TO-RUN -->

<!-- HAND-WRITTEN: preserved verbatim across regeneration. -->

## How to run, in detail

The `--self-test` mode runs in-process fixtures and named sentinels with no disk I/O beyond the
script itself. To regenerate the capability → requirement → test matrix:

```sh
python3 scripts/check-traceability.py emit \
    --md-output docs/requirements-matrix.md \
    --json-output docs/data/matrix.json
```

## What it asserts

Offline traceability gate self-test — capability/tier schema + artifact resolution fixtures, plus
the `HEADLINE-LOCK` sentinel (WR-08, widened at Phase 10; arrow-anchoring and read-loop soundness
fixes landed Phase 10 plans 08-09, structural-residual closures landed plan 10, control-layer and
doc-row closures landed the Phase 10 review fixes — shipped at v8.25.0). Asserts the published
coverage headline, recognizing both the prose and compact-slash renderings, against five named
current-fact surfaces — `docs/requirements-traceability.md`, `CLAUDE.md`, `docs/README.md`,
`docs/MEASUREMENT-MAP.md`, `docs/COMPONENT-DIAGRAM.md` (the last states only the compact-slash form,
never the prose form, which is why two-rendering support is load-bearing rather than decorative) —
plus the two tracked generated artifacts (`docs/requirements-matrix.md`, `docs/data/matrix.json`),
all tied back to `build_matrix_rows()` with the figure appearing as a literal nowhere in the gate. A
two-layer historical/delta exemption — whole-file membership, then a figure-adjacent arrow layer
anchored to the headline literal itself: one of three recognised arrow renderings (`→`, `->`, or the
HTML comment closer `-->` reused as an ASCII long arrow) must sit immediately adjacent to THIS
line's headline mention, delimiting it from a digit run on one side or the other, so a mermaid edge,
a bare HTML comment terminator, or an unrelated numeric arrow elsewhere on the same line (a
battery-count delta, a K-of-5 vector) no longer exempts a current-fact statement — a complete `<!--
... -->` comment is stripped before the arrow test runs so its own terminator can never supply an
arrow, while a genuine delta written with the same three bytes keeps its arrow; complete comments
are also stripped from whole file text before hits are collected, line count preserved so findings
stay citable, so a headline commented out across several lines is not reported as a current-fact
statement at all (control `(i3)`) (all `(i2)`, eight named arms, each verified by neutralization to
fail alone when its own fix is reverted) — lets `docs/v8.0-final-closure.md` and `CHANGELOG.md`
state the same figure as a frozen or dated fact: control `(h)` asserts layer attribution on
synthetic lines carrying the current literal at each surface's real relpath, so the verdict is
independent of whether the live file still contains that literal, and the `(h2)` invariance control
asserts that same verdict is unchanged under a perturbed figure, over four cases each pinned to the
layer it must land on — the two whole-file cases are invariant by MEMBERSHIP (the classifier
short-circuits before the perturbed literals reach the arrow layer, so they cannot fail while the
membership lock holds) and the property itself is carried by the two ARROW arms, one at a live
relpath and one at a synthetic non-exempt path — together guaranteeing a headline move never forces
an edit to either frozen document. A tree-wide scan over `HEADLINE_SCAN_GLOBS` (live value:
`docs/*.md`, `CLAUDE.md`, `CHANGELOG.md`, `README.md`, non-recursive — it does not reach
`CONTRIBUTING.md`, `scripts/`, `shared/`, `first-principles/`, `.github/`, any future
`docs/<subdir>/`, `tests/`, or the git-ignored `docs/history/`) fails, naming the file and line, on
any tracked surface matched by those globs that states the headline as current fact while absent
from the registered set; every candidate the scan's own read loop declines to open is a named INFO
line, never a silent skip. Each surface carries its own named non-vacuity control (`(g)`), and the
scan carries two floors evaluated before its PASS branch, both derived from `read_relpaths` — the
set the read loop itself actually opened, never a separate glob-based sweep, which the floor
helper's signature is what enforces: it takes the `_HeadlineScanRead` record itself, so a
glob-derived `set[str]` cannot be handed to it at any call site (`(m)`'s three arms lock the
helper's own semantics; they do not observe block (j)'s wiring, which is why that wiring is made
unexpressible rather than merely asserted): a coverage floor requiring every path in the union of
`COVERED_HEADLINE_SURFACES` and `HISTORICAL_EXEMPT_FILES` to have been READ, and a per-surface
accounted-hit floor requiring each `COVERED_HEADLINE_SURFACES` member individually to account for at
least one non-historical hit, so one surface's extra hits can no longer mask another surface's zero
(`(j-floor)`/`(l)`/`(m)`) — plus block `(l)`, which drives the real glob-expansion and
file-collection path with alternative glob lists rather than a hand-built simulation: narrowing or
emptying `HEADLINE_SCAN_GLOBS` now fails the gate naming the surfaces it can no longer reach. Block
`(n)` asserts this row's own transcription of `HEADLINE_SCAN_GLOBS` against the constant in both
this file and `docs/ARCHITECTURE.md` — the two-file set is `_TRACE03_DOC_ROWS`, membership-locked in
`(0)` so dropping one cannot silently stop checking that row — covering the glob list's
transcription only; the rest of either row's prose remains unasserted.

## Provenance

As of Phase 13 (CR-02, dispatch reachability; widened at 13-11 for WR-01/WR-03), artifact resolution
over `reproducible` and `scheduled` rows additionally requires that a `.py#_selftest_*` OR
`.py#_self_test_*` anchor be CALLED from a top-level `self_test()` or `_run_self_test()` dispatcher
in the same file (either optionally `async def`), not merely defined — the leg now reaches this
file's own `reproducible` row, SHIP-03's `_self_test_headline_lock`, which the prior single-prefix
leg left completely exempt. The disclosed boundary: this proves the name appears in a call position
inside the matched dispatcher's own comment-stripped body, not that the call is reached at runtime,
not that it sits outside a dead branch, and not dispatch via a nested helper; also open (WR-02,
deferred, not fixed by this widening): a mention of the anchor inside a string literal or docstring
counts as a dispatch, and when the dispatcher is the last top-level construct in its file the body
slice extends to end of file, so trailing module-level code counts as dispatcher body; and when a
file defines both dispatcher names, only the first by position is sliced — a dispatch from the
second is not seen. All three are latent, no such mention or second-dispatcher-name file exists in
either file today. 13-15 (CR-02) closed a fourth, unguarded gap in the same body-slicing step,
independent of these three: the body-boundary pattern did not recognise `async def`, so an `async
def` construct following the dispatcher was absorbed into its body slice. 13-17 (WR-01) then derived
the body-boundary pattern from the dispatcher pattern's own whitespace vocabulary, so a multi-space
`async  def`, or a tab-separated `def` construct following the dispatcher is no longer absorbed into
its body slice either. CI still does not run the `emit` subcommand — that stays a manual
regeneration step.

## Disclosed bounds

**Does not assert** that the coverage figure is *correct* (`build_matrix_rows()` is the oracle; this
sentinel only ties the published surfaces to it); does not scan `tests/` or the git-ignored
`docs/history/`; detection is line-scoped, so a headline hard-wrapped across two physical lines is
not detected; and a line of the form `<digits> --> <current literal>` is treated as a delta even
when it is a mermaid edge whose target label happens to begin with the headline text (measured
unreachable in this tree today, not structurally excluded); symmetrically, `<current literal> -->
<coverage-shaped figure>` is treated as a delta even when it is a mermaid edge whose *source* label
is the headline — that right-hand side must be shaped like a coverage reading (four slash-separated
counts) rather than any digit run, which closes the undisclosed fail-open where a current-fact
statement followed by an arrow and any digits at all escaped both `(f)` and the scan (`(i2)` arms
7-8 lock both halves of the decision). `docs/data/matrix.json` is tracked as of TEARDOWN-03,
docs/v8.7-constraint-teardown.md. Deterministic, no live session.

**`HEADLINE_SCAN_GLOBS` is deliberately NOT widened to `docs/gates/*.md` (D-21-I, plan 21-10).**
The generated per-gate pages state derived facts and disclosed bounds, never the coverage headline
itself, so there is nothing for this sentinel to reach today. The trigger condition, stated so a
later reviewer does not have to rediscover it: if a `docs/gates/<GATE-ID>.md` page ever states the
coverage headline as current fact, the glob must be added explicitly — it will not happen
automatically, since `HEADLINE_SCAN_GLOBS` is a hand-maintained list, not a directory-wide sweep.
