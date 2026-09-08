# CONF-SURFACE: The claim-surface drift gate itself: regenerates `CLAUDE.md`'s and docs/ARCHITECTURE.md's gate tables and docs/gates/<ID>.md pages from this registry's ENTRIES and every gate's --describe emission, and fails on drift.

<!-- GENERATED:FACTS -->
## Facts

- `registered_surfaces` (39): `CLAUDE.md`, `CONTRIBUTING.md`, `docs/ARCHITECTURE.md`, `docs/COMPONENT-DIAGRAM.md`, `docs/DATA-FLOW.md`, `docs/MEASUREMENT-MAP.md`, `docs/PROCESS.md`, `docs/README.md`, `docs/TESTING.md`, `docs/gates/*.md`, `scripts/_battery_core.py`, `scripts/_gate_registry.py`, `scripts/_skill_io.py`, `scripts/check-act-limb.py`, `scripts/check-agent.py`, `scripts/check-body-budget.py`, `scripts/check-conf-gate.py`, `scripts/check-description-budget.py`, `scripts/check-focused-parity.py`, `scripts/check-high-confidence-bound.py`, `scripts/check-install-collisions.py`, `scripts/check-links.py`, `scripts/check-links_anchors_test.py`, `scripts/check-loop-closure.py`, `scripts/check-provenance.py`, `scripts/check-quality-harness.py`, `scripts/check-registration.py`, `scripts/check-routing-battery.py`, `scripts/check-routing.py`, `scripts/check-selfaudit-scan.py`, `scripts/check-step0-emulator.py`, `scripts/check-step0-live.py`, `scripts/check-traceability.py`, `scripts/check-trigger-collisions.py`, `scripts/check-version-stamps.py`, `scripts/gen-gate-docs.py`, `scripts/report-conformance.py`, `scripts/sync-content.py`, `scripts/trace-tests-usage.py`
- `checked_files` (69): `CLAUDE.md`, `CONTRIBUTING.md`, `docs/ARCHITECTURE.md`, `docs/COMPONENT-DIAGRAM.md`, `docs/DATA-FLOW.md`, `docs/MEASUREMENT-MAP.md`, `docs/PROCESS.md`, `docs/README.md`, `docs/TESTING.md`, `docs/gates/BATT-06.md`, `docs/gates/COLLIDE-01.md`, `docs/gates/CONF-GATE.md`, `docs/gates/CONF-SURFACE.md`, `docs/gates/DUAL-04.md`, `docs/gates/FROZEN-EVIDENCE.md`, `docs/gates/GATE-01.md`, `docs/gates/GATE-02-v8.5.md`, `docs/gates/HARN-01.md`, `docs/gates/HARN-02.md`, `docs/gates/HARN-03.md`, `docs/gates/HC-BOUND.md`, `docs/gates/INVARIANT-CHECK.md`, `docs/gates/PRECOMMIT-claim-surface-drift-gate.md`, `docs/gates/PRECOMMIT-claim-surface-generator-self-test.md`, `docs/gates/PRECOMMIT-conformance-baseline-drift-gate.md`, `docs/gates/PRECOMMIT-conformance-generator-self-test.md`, `docs/gates/PRECOMMIT-sync-drift-gate.md`, `docs/gates/PROV-GUARD.md`, `docs/gates/QUAL-01.md`, `docs/gates/REG-GUARD.md`, `docs/gates/SCAN-GUARD.md`, `docs/gates/STEP0-06.md`, `docs/gates/STEP0-08.md`, `docs/gates/TRACE-03.md`, `docs/gates/VAL-01.md`, `docs/gates/VAL-02.md`, `docs/gates/VAL-03.md`, `docs/gates/VAL-04.md`, `docs/gates/VAL-05.md`, `docs/gates/VERSION-01.md`, `scripts/_battery_core.py`, `scripts/_gate_registry.py`, `scripts/_skill_io.py`, `scripts/check-act-limb.py`, `scripts/check-agent.py`, `scripts/check-body-budget.py`, `scripts/check-conf-gate.py`, `scripts/check-description-budget.py`, `scripts/check-focused-parity.py`, `scripts/check-high-confidence-bound.py`, `scripts/check-install-collisions.py`, `scripts/check-links.py`, `scripts/check-links_anchors_test.py`, `scripts/check-loop-closure.py`, `scripts/check-provenance.py`, `scripts/check-quality-harness.py`, `scripts/check-registration.py`, `scripts/check-routing-battery.py`, `scripts/check-routing.py`, `scripts/check-selfaudit-scan.py`, `scripts/check-step0-emulator.py`, `scripts/check-step0-live.py`, `scripts/check-traceability.py`, `scripts/check-trigger-collisions.py`, `scripts/check-version-stamps.py`, `scripts/gen-gate-docs.py`, `scripts/report-conformance.py`, `scripts/sync-content.py`, `scripts/trace-tests-usage.py`
- `derived_counts` (23 entries): `literal_scan_exempt_commonmark-heading-depth`=0, `literal_scan_exempt_deferred-literal-ledger`=191, `literal_scan_exempt_headline-provenance-delta`=11, `literal_scan_exempt_maxturns-60-value`=0, `literal_scan_exempt_plan-number-identifier`=6, `literal_scan_exempt_retired-body-budget`=1, `literal_scan_exempt_sha256-digest`=2, `literal_scan_exempt_version-stamp-count`=3, `literal_scan_hits`=214, `literal_scan_ledger_adjudicated`=70, `literal_scan_ledger_entries`=183, `literal_scan_ledger_max`=183, `literal_scan_ledger_mechanical`=113, `literal_scan_non_exempt`=0, `literal_scan_nonmodule_docstring_hits`=382, `literal_scan_nonmodule_docstring_surfaces`=23, `literal_scan_py_population`=29, `literal_scan_read_files`=69, `literal_scan_surfaces`=39, `roster_arm_census_population`=29, `roster_arm_census_shapes`=3, `roster_arm_census_unreached`=4, `roster_arm_payload_assert_sites`=40
- `disclosed_bounds_anchors` (8): `line-scoped-detection`, `currency-not-correctness`, `closed-spelled-out-vocabulary`, `py-docstrings-only`, `enumerated-per-hit-ledger`, `ledger-repin-and-key-digest`, `non-primary-entries-pinned-mechanically`, `roster-arm-census-is-spelling-level`
- `control_ids` (74): `arithmetic-sentence-names-gates-not-hooks`, `arithmetic-sentence-pluralizes-correctly`, `check-dispatch-wired`, `check-reports-full-drift-count`, `confsurface-census-narrative-joined`, `containment-satisfied-passes`, `containment-spelled-out-normalised`, `containment-violation-fires`, `describe-emits-parseable-json`, `floors-run-together`, `framing-sentences-replaced`, `frozen-path-write-fires`, `frozen-paths-derived-not-typed`, `gates-link-resolves-per-surface`, `harvest-malformed-json-named`, `harvest-nonzero-exit-named`, `harvest-one-bad-does-not-abort`, `hook-mechanism-count-independent-of-precommit-count`, `ledger-injection-architecture-fires`, `ledger-injection-claude-md-fires`, `ledger-injection-testing-fires`, `ledger-key-digest-derived`, `ledger-key-digest-fires`, `ledger-not-an-unconditional-permit`, `ledger-occurrence-surplus-fires`, `ledger-ratchet-fires`, `ledger-ratchet-requires-repin-on-shrink`, `ledger-staleness-fires`, `literal-scan-covers-registry-module`, `literal-scan-py-population-complete`, `narrative-preserved-across-regeneration`, `no-row-wrapped`, `nondeterminism-exit-2`, `one-renderer-two-surfaces`, `own-registry-docstring-has-no-count`, `page-per-entry`, `population-arithmetic-derived`, `region-duplicate-end-raises`, `region-duplicate-start-raises`, `region-end-before-start-raises`, `region-happy-path`, `region-marker-in-fence-ignored`, `region-preserves-crlf`, `region-preserves-final-newline`, `region-preserves-surrounding-prose`, `region-real-file-claude-md`, `region-tilde-fence-quoting-backticks`, `region-zero-end-raises`, `region-zero-start-raises`, `registry-self-test`, `roster-arm-shape-census`, `roster-arm-shape-census-population-complete`, `roster-arm-shape-census-registry-covered`, `roster-arm-shape-census-vacuity`, `row-count-equals-entries`, `scan-coverage-floor-fires`, `scan-coverage-floor-signature-locked`, `scan-docstring-only`, `scan-exempt-class-attributed`, `scan-glob-narrowing-fires`, `scan-hit-inside-fence-passes`, `scan-hit-outside-fence-fires`, `scan-neutralization-arms`, `scan-spelled-out-detected`, `scan-unattributable-permit-fires`, `selffile-docstring-ratchet-fires`, `selffile-docstring-ratchet-requires-repin-on-shrink`, `slug-collision-raises`, `testing-index-links-resolve`, `testing-index-row-count-equals-entries`, `testing-real-file-region`, `thin-page-fully-generated`, `trace03-glob-substring-derived`, `version01-narrative-control-ids-live`
- `control_count`: `74`
- `locked_constants` (2 entries): `generated_end_marker`='<!-- END GENERATED -->', `generated_marker`='<!-- GENERATED — DO NOT EDIT. Source: {source}. Regenerate via: scripts/gen-gate-docs.py --write. -->'
<!-- END GENERATED:FACTS -->

<!-- GENERATED:HOW-TO-RUN -->
## How to run

```sh
python3 scripts/gen-gate-docs.py --self-test && python3 scripts/gen-gate-docs.py --check
```

CI job: `gen-gate-docs`
<!-- END GENERATED:HOW-TO-RUN -->

## Requirement amendment (CONF-12, D-07)

`.planning/REQUIREMENTS.md`'s CONF-12 originally required, alongside generation and the drift
gate, that no table cell in the generated CI-gate tables exceed a fixed character cap. That
clause was amended (Phase 21 plan 21-12, D-07): the cap is removed. A cell is short in practice
because its detail moved to this page — the split this generator implements — not because a
numeric ceiling is measured or enforced anywhere in this codebase. The count that satisfies the
milestone's standing instruction in the cap's place is named in the amended requirement text
itself: CONF-13's non-exempt hand-maintained literal count (this page's own `literal_scan_non_exempt`
field above, held at its target by this same generator's `--check`), and the gate registry's
equality floor over gate ids (`scripts/_gate_registry.py --self-test`). The full amendment text,
with its measured before/after evidence for the previously-oversized cells, lives in
`.planning/REQUIREMENTS.md`'s CONF-12 entry; `.planning/ROADMAP.md`'s Phase 21 success criterion
3 was updated in the same edit so the two documents do not diverge.

## Disclosed bounds

<!-- HAND-WRITTEN: preserved verbatim across regeneration. Fill in this
gate's disclosed bounds / limitations narrative below. -->

CONF-13's standing scanner enforces `21-CONF13-BASELINE.md`'s measured
taxonomy: a count-noun-adjacent number literal, outside a generated fence
and outside a named exemption class, fails `--check`. The bounds below are
disclosed in the same voice R7/R9/R10 use elsewhere in this repo — each
states a measured property of the detector, not an unconditional guarantee;
the `disclosed_bounds_anchors` field in the Facts fence above is the
derived count and name list, never restated by hand here.

**(1) Detection is line-scoped**, inherited from `HEADLINE-LOCK`'s own
disclosed bound. A hand-maintained count hard-wrapped across two physical
lines — the number on one line, its count noun on the next — is invisible
to this scanner. Not measured as occurring anywhere in the scanned surface
set today, but not structurally excluded either.

**(2) The scanner proves a number is CURRENT, never that it describes the
right thing** — the same D-06 bound the containment rule above already
carries, applied to a second surface. A count that is internally
consistent but attached to the wrong noun (e.g. correctly stating a fact
about branches while actually describing rows) passes this scanner.
Corroboration against a `--describe`-derived fact proves currency, not
correctness.

**(3) The spelled-out-number vocabulary is closed**: one through twenty,
the tens, hundred, and their hyphenated compounds. A number word outside
that vocabulary — an ordinal ("hundredth"), a fraction ("a third"), or a
compound the vocabulary does not enumerate — is not normalised and is
therefore not checked. This is the same vocabulary `21-CONF13-BASELINE.md`
measured and it is not widened here.

**(4) `.py` coverage is module docstrings only.** `ast.get_docstring()`
reaches exactly the module-level docstring; a function, async-function, or
class docstring — and a comment or an in-code string constant — carrying a
hand-maintained count is out of this scanner's reach by construction. The
written reason, carried over from the baseline: a literal sitting beside
the constant it describes has a much shorter drift distance than the
scattered cross-file prose this scanner exists to police, so a
comment-level count is lower-risk. Verified again during this phase's
fourth gap-closure round rather than assumed: this sentence already named
"a comment or an in-code string constant" as out of reach, so no widening
of it was required to close a second live demonstration
(`scripts/gen-gate-docs.py`'s own stale `#` comment naming a detail-page
count). What that demonstration DOES sharpen: the published SIZE of this
bound (`literal_scan_nonmodule_docstring_hits` /
`literal_scan_nonmodule_docstring_surfaces` in the Facts fence above)
measures non-module DOCSTRINGS only — it does not measure `#` comments —
so the published figure UNDERSTATES this bound's true reach. This bound is
deliberately NOT closed by widening the standing scan (plan 21-20 Task 3):
doing so would demand
either a very large number of prose remediations or an equally large
number of new ledger entries, and the deferred-literal ledger is now both
size-pinned and key-digest-locked (bound (6), below) — refilling it to
cover a widened scan is exactly the regression that lock closes.

**The `.py` population itself is every `.py` file directly under
`scripts/`, a live directory glob** — sized by `literal_scan_py_population`
in the Facts fence above, never restated by hand here. It was previously
derived from the gate registry's own `ENTRIES`, which made
`scripts/_gate_registry.py` — the module that DEFINES those entries —
structurally unable to ever be scanned; that gap is
closed by widening the population to the live directory glob, the same move
recorded during this phase's round-two verification for the roster-arm
census below. The docstring-only bound stated just above is unaffected by
this widening: it is a bound on WHAT a docstring reaches within a scanned
file, not on WHICH files are scanned, and it survives unchanged.

What changed instead is that the bound's SIZE is now published rather than
left unquantified: `literal_scan_nonmodule_docstring_hits` and
`literal_scan_nonmodule_docstring_surfaces` in the Facts fence above are a
live, re-derived measurement of every function/async-function/class
docstring literal across the registered `.py` surfaces, excluding each
module's own docstring. This measurement is READ-ONLY: it is never fed
into `literal_scan_non_exempt` and never turns `--check` red on its own.
The one exception is this phase's own generator file,
`scripts/gen-gate-docs.py` — the file a prior stale hand-maintained
control-roster count actually landed in — which additionally carries a
two-sided ratchet on its own share of the measurement: growth over its
pin is a finding (a second such literal landing in the same file), and a
shrink below the pin demands the pin be lowered in the same commit, the
same shape as bound (6)'s ledger-size predicate. Every other `.py`
surface's share of the measurement is published, not enforced.

The live per-surface reading — every surface this scanner reads
(`registered_surfaces` names an unexpanded glob as a single entry;
`checked_files` records every file that glob matched), the total hits
found, and how many are non-exempt — lives in the Facts fence above as
`derived_counts`, never restated by hand here (this narrative's own
containment obligation under D-06 is what forbids restating any of those
figures as a bare digit outside the fence). Plan 21-10 drove
`literal_scan_non_exempt` to **0** — the exemption-class breakdown
(version stamps, headline-provenance deltas, plan-number identifiers, the
retired body budget, the pinned `maxTurns` value, sha256 digests, the
CommonMark heading-depth range, and `deferred-literal-ledger`, described
below) sits in the Facts fence above, each keyed
`literal_scan_exempt_<class-name>`.

**(5) The deferred-literal-ledger is an enumerated PER-HIT permit, not a
whole-surface deferral.** Plan 21-10's Task 3 whole-surface-exempted a
registered surface by `hit.relpath` alone — every hit on that surface was
permitted regardless of what its text said, including `CLAUDE.md`,
`docs/ARCHITECTURE.md` and `docs/TESTING.md`, the surfaces this scanner
exists to protect. That structural zero survived a genuinely wrong
docs/TESTING.md sentence this same phase shipped, undercounting the real
pre-commit-gate count — the scanner saw it and permitted it (the exact
wording is recorded in plan 21-16's own SUMMARY, not restated here). Plan
21-16 replaced it with `scripts/gen-gate-docs.py`'s
`_DEFERRED_LITERAL_HITS`, keyed by `(relpath, normalised_text)`: a hit on a
registered surface that is NOT in the ledger is a finding regardless of
which surface it sits on, and a ledgered key's LIVE occurrence count
exceeding its pinned figure is also a finding — the same exact sentence
copied to a second place is a new finding, not a free ride on the existing
entry. Permanent registered controls (`ledger-injection-claude-md-fires`,
`ledger-injection-architecture-fires`, `ledger-injection-testing-fires`)
each inject a synthetic count literal into a single primary surface and
assert it is caught.

**What this ledger does NOT certify: that every pinned entry's number is
itself correct.** The entries on the primary surfaces (`CLAUDE.md`,
`docs/ARCHITECTURE.md`, `docs/TESTING.md` — backlog `999.42`) and on
`docs/README.md`, `docs/PROCESS.md` and `CONTRIBUTING.md` (backlog `999.44`
— `docs/README.md`'s entries from plan 22-04, the historical figures CR-05
found deleted, restored verbatim and each individually attributed, see
`docs/PROCESS.md` §1.2 for the count and the worked example;
`docs/PROCESS.md`'s and `CONTRIBUTING.md`'s own entries from plan 22-07,
the D-05 REACH widening that registered both files in
`LITERAL_SCAN_MD_GLOBS`; `docs/PROCESS.md`'s further entries from plan
22-09, reconciling §1.2's own CR-01/WR-02 rewrite) were adjudicated BY
HAND, one at a time (`literal_scan_ledger_adjudicated`, in the Facts fence
above, both backlog ids combined): most were confirmed
CORRECT-BUT-HAND-MAINTAINED (a
currently-true fact nothing derives) and the rest named NOT-A-COUNT (a
false positive of the adjacency heuristic — an enumerated-list marker, a
per-item ratio statement, or a correct number attached to the wrong
noun); the per-entry adjudication table, with its disposition counts, is
recorded in plan 21-16's own SUMMARY. The remaining
entries (`literal_scan_ledger_mechanical`, in the Facts fence above)
were pinned MECHANICALLY from a live scan, without per-entry adjudication
— a real reduction in what this ledger certifies, stated here rather than
left implicit:

- **backlog `999.40`** — the `docs/gates/*.md` narrative pages
  (`QUAL-01.md`, `SCAN-GUARD.md`, `TRACE-03.md`, `CONF-GATE.md`,
  `GATE-01.md`, `HC-BOUND.md`, `REG-GUARD.md`, `VAL-02.md`,
  `VERSION-01.md`, `STEP0-08.md`). Root cause: dense hand-written/migrated
  technical narrative uses ordinary-language small numbers that D-06's own
  citation-exemption vocabulary (plan 21-08) already learned to ignore for
  containment purposes, but this scanner does not share that vocabulary.
- **backlog `999.41`** — the `.py` module docstrings this scanner reads.
  Root cause: the same ordinary-language-number shape in dense narrative
  docstrings; `21-CONF13-BASELINE.md`'s own false-positive layer
  (ordinal-label-reference, adjacency-mistrack, enumerated-list-marker)
  was deliberately not ported into this standing scanner (plan 21-09's own
  key-decision).

**(6) The ledger never drifts silently, in either direction, and any change
must be re-pinned in the same commit.** Its pinned maximum
(`literal_scan_ledger_max`, in the Facts fence above) is a typed integer
constant, not a value derived from the ledger's own length — a
self-derived pin would compare the ledger against itself, which can never
fail. An un-repinned growth over the pin fails `--check`, naming both the
pinned and the live figure. A shrink (`literal_scan_ledger_entries`
falling below the pin — an entry removed once its underlying prose is
fixed) is still legal, but it is no longer free: plan 21-20 Task 1 closed
the headroom a shrink used to buy by making an un-repinned shrink itself a
finding, naming both figures and demanding `_DEFERRED_LEDGER_MAX` be
lowered to the live size in the same commit that shrinks it. A ledger key
that no longer matches any live hit is separately a finding — the ledger
cannot silently outlive its own findings, which drives most of its history
downward. **Growth is not barred outright** — plan 22-04 (D-22-D) grew it
134 → 152 by restoring the true historical figures CR-05 found deleted
from `docs/README.md` (see `docs/PROCESS.md` §1.2) and individually
attributing each one under a named `999.44` entry, plan 22-07 grew it
a second time, 152 → 182, by registering `docs/PROCESS.md` and
`CONTRIBUTING.md` in `LITERAL_SCAN_MD_GLOBS` (D-05) and individually
attributing every resulting hit under the same `999.44` backlog id, and
plan 22-09 grew it a third time, 182 → 184, by reconciling §1.2's own
CR-01/WR-02 rewrite (correcting the row-17 restore claim's own false
"verbatim" wording) and individually attributing the two resulting hits
under the same `999.44` backlog id; this
is the ledger widening what it certifies, not the
detector accepting a non-conforming artifact (CONTRACT-06 is untouched).
What the mechanism actually forbids is a SILENT size change: a genuine
growth is legal precisely because it lands with both guards re-pinned, in
the same commit, from the real final state.

**The size pin, even repinned every time, cannot see a same-size
substitution.** A remove-and-add performed in one commit — one real,
already-adjudicated entry removed, a fabricated, never-adjudicated permit
added in its place — leaves the live size exactly at the pin, so neither
the growth nor the shrink finding fires. `_DEFERRED_LEDGER_KEYS_DIGEST`, a
sha256 pin over the ledger's sorted key set (the same pin idiom
`scripts/check-quality-harness.py` already uses for its three CONTRACT-06
detector digests), closes that hole: any key-set change, including one
that preserves the ledger's size, changes the digest and is a finding
naming both digests. Disclosed bound, in the measured voice this page uses
elsewhere: the digest proves the key set changed DELIBERATELY — someone
edited the ledger and re-ran the pin — never that the change was
ADJUDICATED. It cannot distinguish a genuinely-remediated permit from a
rubber-stamped one; it can only prove the set is not drifting silently
underneath an unchanged pin.

**The roster-arm shape census.** A separate, permanent self-test control —
distinct from the literal-scan taxonomy above — scans for an enumerated,
NAMED set of defective spellings: `roster-arm-synthetic-id-membership`,
`roster-arm-bare-clause-marker`, and `roster-arm-value-bearing-clause-marker`.
This is a spelling-level scan for named spellings, **not a guarantee about
assertion SHAPE in general** — a whole-message assertion written in any
spelling outside this named set passes the scan clean. The
`roster_arm_census_population` and `roster_arm_census_shapes` fields in the
Facts fence above are the live, derived population size and shape-roster
size; neither is restated by hand here.

The routes this scan cannot reach are named too, rather than left an
unbounded admission: `roster-arm-unreached-payload-substring` (a
whole-message assertion against `problems[0]`, or any other joined
finding — its live population size is published, read-only and gating
nothing, as `roster_arm_payload_assert_sites` in the Facts fence above),
`roster-arm-unreached-other-spellings` (any other way of writing a
whole-message membership test; the spelling set named above is closed),
`roster-arm-unreached-outside-scripts` (`.py` files not directly under
`scripts/`), and `roster-arm-unreached-semantic-correctness` (whether a
roster arm is semantically right, which no source-shape scan can see).
`roster_arm_census_unreached` in the Facts fence above is the live,
derived size of this unreached-route roster.

**This paragraph previously stated an unscoped universal** about
assertion SHAPE, and live counterexamples inside the census's own scanned
population — confirmed live during this phase's round-three verification
— falsified it. The correction above is a spelling-level scan over a
named, enumerated set, never a claim about assertion shape in general.

**The join itself is disclosed, not assumed.** Every shape id and route
id named above is held to the live `_ROSTER_ARM_SHAPES` /
`_ROSTER_ARM_UNREACHED` rosters by a registered self-test control
(`confsurface-census-narrative-joined`) asserting SET EQUALITY in both
directions — a shape added in code and not named here is a finding, and
an id named here that does not exist in code is a finding too — and the
superseded sentence above is pinned so it cannot return to this page or
to the census docstrings it also lived on. This is an equality join plus
a spelling-level pin on a single superseded sentence; it does not prove
this page's narrative is honest in general, only that these named ids and
that superseded sentence stay in sync with the live code.

Its population was previously derived from the gate registry's own
`ENTRIES`, which made `scripts/_gate_registry.py` — the module that
DEFINES those entries — structurally unable to ever appear in its own
census; that gap is closed by widening the population to a live directory
glob, recorded during this phase's round-two verification.

Full item counts, reasons and the per-item closing move for every
hand-remediated item under plan 21-10's original ~15-item/6-file budget
sweep are recorded in
`.planning/phases/21-generate-the-claim-surface/21-CONF13-BASELINE.md`'s
"Plan 21-10 disposition ledger" section. Adjudicating a mechanically-pinned
entry (removing it from `_DEFERRED_LITERAL_HITS` once its prose is fixed
or its number confirmed correct) shrinks the ledger; the ratchet permits
that shrink — provided it is re-pinned in the same commit — but never a
growth back toward a whole-surface permit, and never a same-size
substitution the key digest would catch.
