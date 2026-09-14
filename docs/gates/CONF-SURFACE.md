# CONF-SURFACE: The claim-surface drift gate itself: regenerates `CLAUDE.md`'s and docs/ARCHITECTURE.md's gate tables and docs/gates/<ID>.md pages from this registry's ENTRIES and every gate's --describe emission, and fails on drift.

<!-- GENERATED:FACTS -->
## Facts

- `registered_surfaces` (40): `CLAUDE.md`, `CONTRIBUTING.md`, `docs/ARCHITECTURE.md`, `docs/COMPONENT-DIAGRAM.md`, `docs/DATA-FLOW.md`, `docs/MEASUREMENT-MAP.md`, `docs/PROCESS.md`, `docs/README.md`, `docs/TESTING.md`, `docs/gates/*.md`, `scripts/_battery_core.py`, `scripts/_gate_registry.py`, `scripts/_skill_io.py`, `scripts/census-delta-vectors.py`, `scripts/check-act-limb.py`, `scripts/check-agent.py`, `scripts/check-body-budget.py`, `scripts/check-conf-gate.py`, `scripts/check-description-budget.py`, `scripts/check-focused-parity.py`, `scripts/check-high-confidence-bound.py`, `scripts/check-install-collisions.py`, `scripts/check-links.py`, `scripts/check-links_anchors_test.py`, `scripts/check-loop-closure.py`, `scripts/check-provenance.py`, `scripts/check-quality-harness.py`, `scripts/check-registration.py`, `scripts/check-routing-battery.py`, `scripts/check-routing.py`, `scripts/check-selfaudit-scan.py`, `scripts/check-step0-emulator.py`, `scripts/check-step0-live.py`, `scripts/check-traceability.py`, `scripts/check-trigger-collisions.py`, `scripts/check-version-stamps.py`, `scripts/gen-gate-docs.py`, `scripts/report-conformance.py`, `scripts/sync-content.py`, `scripts/trace-tests-usage.py`
- `checked_files` (70): `CLAUDE.md`, `CONTRIBUTING.md`, `docs/ARCHITECTURE.md`, `docs/COMPONENT-DIAGRAM.md`, `docs/DATA-FLOW.md`, `docs/MEASUREMENT-MAP.md`, `docs/PROCESS.md`, `docs/README.md`, `docs/TESTING.md`, `docs/gates/BATT-06.md`, `docs/gates/COLLIDE-01.md`, `docs/gates/CONF-GATE.md`, `docs/gates/CONF-SURFACE.md`, `docs/gates/DUAL-04.md`, `docs/gates/FROZEN-EVIDENCE.md`, `docs/gates/GATE-01.md`, `docs/gates/GATE-02-v8.5.md`, `docs/gates/HARN-01.md`, `docs/gates/HARN-02.md`, `docs/gates/HARN-03.md`, `docs/gates/HC-BOUND.md`, `docs/gates/INVARIANT-CHECK.md`, `docs/gates/PRECOMMIT-claim-surface-drift-gate.md`, `docs/gates/PRECOMMIT-claim-surface-generator-self-test.md`, `docs/gates/PRECOMMIT-conformance-baseline-drift-gate.md`, `docs/gates/PRECOMMIT-conformance-generator-self-test.md`, `docs/gates/PRECOMMIT-sync-drift-gate.md`, `docs/gates/PROV-GUARD.md`, `docs/gates/QUAL-01.md`, `docs/gates/REG-GUARD.md`, `docs/gates/SCAN-GUARD.md`, `docs/gates/STEP0-06.md`, `docs/gates/STEP0-08.md`, `docs/gates/TRACE-03.md`, `docs/gates/VAL-01.md`, `docs/gates/VAL-02.md`, `docs/gates/VAL-03.md`, `docs/gates/VAL-04.md`, `docs/gates/VAL-05.md`, `docs/gates/VERSION-01.md`, `scripts/_battery_core.py`, `scripts/_gate_registry.py`, `scripts/_skill_io.py`, `scripts/census-delta-vectors.py`, `scripts/check-act-limb.py`, `scripts/check-agent.py`, `scripts/check-body-budget.py`, `scripts/check-conf-gate.py`, `scripts/check-description-budget.py`, `scripts/check-focused-parity.py`, `scripts/check-high-confidence-bound.py`, `scripts/check-install-collisions.py`, `scripts/check-links.py`, `scripts/check-links_anchors_test.py`, `scripts/check-loop-closure.py`, `scripts/check-provenance.py`, `scripts/check-quality-harness.py`, `scripts/check-registration.py`, `scripts/check-routing-battery.py`, `scripts/check-routing.py`, `scripts/check-selfaudit-scan.py`, `scripts/check-step0-emulator.py`, `scripts/check-step0-live.py`, `scripts/check-traceability.py`, `scripts/check-trigger-collisions.py`, `scripts/check-version-stamps.py`, `scripts/gen-gate-docs.py`, `scripts/report-conformance.py`, `scripts/sync-content.py`, `scripts/trace-tests-usage.py`
- `derived_counts` (38 entries): `chain_termini_current`=5, `chain_termini_stale`=0, `chain_termini_uncorroborable`=0, `containment_ledger_cannot_reach`=7, `containment_ledger_entries`=21, `containment_ledger_frozen_historical`=5, `containment_ledger_max`=21, `containment_ledger_not_a_count_claim`=9, `containment_surfaces`=4, `literal_scan_exempt_commonmark-heading-depth`=0, `literal_scan_exempt_deferred-literal-ledger`=188, `literal_scan_exempt_generated-narrative-region`=0, `literal_scan_exempt_headline-provenance-delta`=13, `literal_scan_exempt_maxturns-60-value`=0, `literal_scan_exempt_plan-number-identifier`=6, `literal_scan_exempt_retired-body-budget`=1, `literal_scan_exempt_sha256-digest`=2, `literal_scan_exempt_version-stamp-count`=3, `literal_scan_hits`=213, `literal_scan_ledger_adjudicated`=69, `literal_scan_ledger_entries`=180, `literal_scan_ledger_max`=180, `literal_scan_ledger_mechanical`=111, `literal_scan_non_exempt`=0, `literal_scan_nonmodule_docstring_hits`=502, `literal_scan_nonmodule_docstring_surfaces`=24, `literal_scan_py_population`=30, `literal_scan_read_files`=70, `literal_scan_surfaces`=40, `narrative_regions`=3, `narrative_restatement_chain_hop`=0, `narrative_restatement_fenced`=0, `narrative_restatement_finding`=0, `narrative_restatement_in_region`=9, `roster_arm_census_population`=30, `roster_arm_census_shapes`=3, `roster_arm_census_unreached`=4, `roster_arm_payload_assert_sites`=51
- `disclosed_bounds_anchors` (14): `line-scoped-detection`, `currency-not-correctness`, `closed-spelled-out-vocabulary`, `py-docstrings-only`, `enumerated-per-hit-ledger`, `ledger-repin-and-key-digest`, `non-primary-entries-pinned-mechanically`, `roster-arm-census-is-spelling-level`, `second-g3-target-unreachable`, `component-diagram-mermaid-fence-unreachable`, `narrative-region-two-surface-lock-only`, `containment-ledger-reconciliation-delta`, `py-docstring-not-narrative-prose-scope`, `criterion-3-cannot-reach-residue`
- `control_ids` (112): `arithmetic-sentence-names-gates-not-hooks`, `arithmetic-sentence-pluralizes-correctly`, `chain-terminus-corrected-page-clean`, `chain-terminus-fence-silent-uncorroborable`, `chain-terminus-pre-fix-synthetic-fixture`, `check-dispatch-wired`, `check-reports-full-drift-count`, `citation-shape-len-matches-census-pin`, `citation-shape-slash-before-arrow`, `claude-headline-region-chained-not-reread`, `confsurface-census-narrative-joined`, `containment-ledger-class-counts-cover-ledger`, `containment-ledger-key-digest-fires`, `containment-ledger-not-an-unconditional-permit`, `containment-ledger-occurrence-surplus-fires`, `containment-ledger-ratchet-fires`, `containment-ledger-ratchet-requires-repin-on-shrink`, `containment-ledger-staleness-fires`, `containment-ledger-suppresses-known-finding`, `containment-satisfied-passes`, `containment-slash-paired-vector-stripped`, `containment-spelled-out-normalised`, `containment-surface-roster-empty-set-fires`, `containment-surface-roster-extra-fires`, `containment-surface-roster-lock-non-empty`, `containment-surface-roster-missing-fires`, `containment-surface-roster-satisfied-passes`, `containment-violation-fires`, `delta-chain-hops-claude-row-count-recovered`, `delta-chain-hops-confsurface-corrected`, `delta-chain-hops-qual01-out-of-grammar`, `delta-chain-hops-scanguard-spelled-out`, `describe-emits-parseable-json`, `floors-run-together`, `framing-sentences-replaced`, `frozen-path-write-fires`, `frozen-paths-derived-not-typed`, `gates-link-resolves-per-surface`, `harvest-malformed-json-named`, `harvest-nonzero-exit-named`, `harvest-one-bad-does-not-abort`, `hook-mechanism-count-independent-of-precommit-count`, `ledger-injection-architecture-fires`, `ledger-injection-claude-md-fires`, `ledger-injection-testing-fires`, `ledger-key-digest-derived`, `ledger-key-digest-fires`, `ledger-not-an-unconditional-permit`, `ledger-occurrence-surplus-fires`, `ledger-ratchet-fires`, `ledger-ratchet-requires-repin-on-shrink`, `ledger-staleness-fires`, `literal-scan-covers-registry-module`, `literal-scan-py-population-complete`, `narrative-exemption-matcher-never-suppresses`, `narrative-marker-context-legs`, `narrative-marker-context-live-tree-clean`, `narrative-marker-context-wired-into-cmd-check`, `narrative-marker-pairs-distinct`, `narrative-preserved-across-regeneration`, `narrative-region-roster-equals-lock`, `narrative-region-templates-single-value-slot`, `narrative-render-raises-on-absent-field`, `narrative-render-round-trips-through-disk-value`, `narrative-restatement-four-legs`, `narrative-restatement-wired-into-cmd-check`, `narrative-roster-accumulated-not-table-derived`, `narrative-roster-missing-and-extra-named`, `narrative-roster-no-default-raises`, `no-row-wrapped`, `nondeterminism-exit-2`, `one-renderer-two-surfaces`, `own-registry-docstring-has-no-count`, `page-per-entry`, `population-arithmetic-derived`, `region-duplicate-end-raises`, `region-duplicate-start-raises`, `region-end-before-start-raises`, `region-happy-path`, `region-marker-in-fence-ignored`, `region-preserves-crlf`, `region-preserves-final-newline`, `region-preserves-surrounding-prose`, `region-real-file-claude-md`, `region-tilde-fence-quoting-backticks`, `region-zero-end-raises`, `region-zero-start-raises`, `registry-self-test`, `roster-arm-shape-census`, `roster-arm-shape-census-population-complete`, `roster-arm-shape-census-registry-covered`, `roster-arm-shape-census-vacuity`, `row-count-equals-entries`, `scan-coverage-floor-fires`, `scan-coverage-floor-signature-locked`, `scan-docstring-only`, `scan-exempt-class-attributed`, `scan-glob-narrowing-fires`, `scan-hit-inside-fence-passes`, `scan-hit-outside-fence-fires`, `scan-neutralization-arms`, `scan-spelled-out-detected`, `scan-unattributable-permit-fires`, `selffile-docstring-ratchet-fires`, `selffile-docstring-ratchet-requires-repin-on-shrink`, `slug-collision-raises`, `testing-index-links-resolve`, `testing-index-row-count-equals-entries`, `testing-real-file-region`, `thin-page-fully-generated`, `trace03-glob-substring-derived`, `version01-narrative-control-ids-live`
- `control_count`: `112`
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
Plan 22-10 then lowered it twice more. Task 1 lowered it 184 → 183,
removing the stale hit pinning a dated call-site citation once it was
replaced with a rot-proof symbol anchor in the docstring itself (CR-03),
needing no replacement hit since the rewrite added no new digit. Task 2
lowered it again, 183 → 181, removing stale hits whose underlying prose
had already been rewritten to state the re-derived multi-literal and
not-found-arm censuses directly, again needing no replacement hit for the
same reason. Plan 26-06 Task 2 lowered it once more, 181 → 180,
reconciling CONTAIN-04's own deferred-literal half against measurement:
re-checking every ledger reason that asserted a live `--describe` value in
this session found a reason that had gone stale against its own naming
gate. The hand-typed prose that reason defended was replaced with a
pointer to this file's own generated CONF-GATE row rather than with a
corrected digit, because a marker-pair region cannot bracket that prose —
it sits inside a fenced shell code block, outside
`_generated_marker_pairs_for()`'s reach — removing that ledger entry with
no replacement. See `_DEFERRED_LEDGER_MAX`'s own comment in
`scripts/gen-gate-docs.py` for the concrete instance and the argument
distinguishing this fix from CR-05's gaming move. The chain's terminus is
the figure the Facts fence above publishes as `literal_scan_ledger_max` —
read it there, not restated here as a bare digit.
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

**(7) Chain-terminus corroboration on a `fence-silent` surface reports an
unmatched terminus as UNCORROBORABLE, never as a failure.** The narrative
surfaces `CLAUDE.md`, `docs/ARCHITECTURE.md` and `docs/TESTING.md` carry no
gate-specific Facts fence publishing every derived count they narrate, so a
growth chain's terminus absent from one of these pages' own generated
region cannot be told apart from a genuinely stale one by this page's own
text alone — see the `terminus_policy` field beside `_CONTAINMENT_SURFACES`
in `scripts/gen-gate-docs.py` for the structural argument this bound rests
on. This is a measured, disclosed gap, not a hypothetical one: the live
tally is published as `chain_termini_uncorroborable` in the Facts fence
above, never restated here as a bare digit.

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

**(8) The second G3 demonstration target, `tests/premise-rejection-catalog.md`, is
published as a reach gap, not a corrected instance.** `docs/v9.1-claim-containment-diagnosis.md`
Appendix A names this site alongside CR-01 as this milestone's own demonstration pair; unlike
CR-01 it stays permanently out of reach. The reason is structural, not a scoping choice:
`/usr/bin/grep -c "END GENERATED" tests/premise-rejection-catalog.md` reads zero — the file
carries no generated region at all, so containment's inside-fence set there is empty and no
verdict on any number stated on that page can ever be corroborated. This is the same structural
finding Phase 24 recorded for CR-03's `docs/README.md`, cited here rather than restated (see
`docs/v9.1-claim-containment-diagnosis.md` § 3). Widening the reached-surface set above to add a
fifth entry was rejected: the roster equality floor names the surfaces above by identity and a
fifth would break it by construction. A synthetic fixture asserting the arm would catch it was
rejected too, for the same reason `.planning/STATE.md` names R4-CR-01, R4-CR-02 and Phase 13's
`R-HEAD-GTHOP-LATE` fixture: a control demonstrating a control's presence, rather than its
measured effect, is vacuous. The site's own narrated growth is stale against
`python3 scripts/check-provenance.py --self-test`'s own live-printed tally — re-run that command
for the current reading rather than trusting a restated one here. The gap is a measured input to
Phase 26's NARR-02, which is about surfaces containment cannot reach; tracked as backlog `999.70`.

**(9) The pre-migration restatement census (Phase 26, NARR-01/NARR-02) found a
structurally-unreachable occurrence: `docs/COMPONENT-DIAGRAM.md`'s Mermaid node label
restating the coverage headline in slash form.** The line sits inside a fenced Mermaid code
block — `_fenced_line_flags()` marks it fenced — and a non-fenced marker line cannot bracket a
fenced one: every marker `_replace_region`/`_replace_or_bootstrap_region` writes is a whole,
non-fenced line, so this occurrence cannot become a D-01 region without either moving the label
out of its fence or giving the region primitive a fenced-aware variant, neither of which exists
today. The census swept every containment-unreachable narrative surface named in NARR-02's scope
(`docs/PROCESS.md`, `docs/README.md`, `CONTRIBUTING.md`, `docs/MEASUREMENT-MAP.md`,
`docs/COMPONENT-DIAGRAM.md`, `docs/DATA-FLOW.md`) plus `CLAUDE.md` for comparison, and found this
the only fenced occurrence among them; the unfenced occurrences on `docs/README.md` and
`docs/MEASUREMENT-MAP.md` were the region candidates plan 26-04 wired regions onto (bound (10)
below states what that wiring now guarantees, and what it does not).
This gap is published, not absorbed, following bound (8)'s own precedent: a synthetic fixture
proving a region mechanism reaches a fenced line is rejected for the same reason bound (8) rejects
a control asserting its own presence — a control demonstrating a control's presence rather than
its measured effect is vacuous — and widening the criterion to declare a fenced occurrence out of
scope by definition is rejected too, because that would silently absorb a real, currently-live
restatement rather than name it.

**(10) The NARR-02 regions guarantee a rendered sentence's currency against its own harvested
source, and now also guarantee that no hand-typed restatement of that same value survives outside
either fence on any roster surface — they do not guarantee anything wider.** Plan 26-04 wired
`narrative_region_surface_roster_problems` into `cmd_check()` over the surface-key set the
`generate_all()` loop itself accumulates (never a table-derived default, the same T-26-03 argument
`containment_surface_roster_problems` already makes), and wired `narrative_restatement_problems`
alongside it: a `'finding'`-class restatement — the value present outside any generated fence,
outside a fenced code block, and outside a linked delta chain — fails `--check` by naming the
file and line. The Facts fence's `narrative_restatement_finding` count above is that census's own
live reading, generated rather than hand-typed; `narrative_regions` above is the roster's own
size, and `literal_scan_exempt_generated-narrative-region` stays a named, auditable
declaration rather than the suppression mechanism itself (bound (5)'s sibling argument — the
actual suppression is `_generated_marker_pairs_for()`'s registration, not this exemption class).
Plan 26-05 extended the roster with CLAUDE.md's own coverage-headline sentence, following the
identical mechanism — registering a second, independent marker pair on a page that already
carries CLAUDE_REGION_MARKERS, chained onto the same target the CI-gate-table region writes.
What this does NOT reach: a page outside the roster's own hand-typed restatement of the same
value is invisible to this specific mechanism, because the roster lock is a fixed-population
equality floor over exactly the registered surfaces (`_NARRATIVE_REGION_SURFACES_LOCK`), never an
open-ended one (D-06 proviso 4's own discipline, reused here) — such a restatement is caught only
if that page already happens to be a registered `LITERAL_SCAN_SURFACES` member. Nor does it
guarantee correctness of any OTHER hand-typed count on any roster page: bound (2)'s currency-not-
correctness limit applies here identically.

**(11) The containment ledger's reconciliation is a measured delta between two endpoints, never
an estimate, and its residue is published by class rather than absorbed.** Plan 26-05 re-measured
the ledger at the start of its own session (never trusting a prior planning document's reading,
per D-05 proviso 3): the pre-migration size was pinned at the value the module's own growth/shrink
history records above `_CONTAINMENT_LEDGER_MAX`'s prior figure. CLAUDE.md's own generated
coverage-headline region (bound (10) above) removed the coverage-headline triple's entries
outright, and the reconciliation pass re-derived every surviving entry's classification against a
fresh invocation of its naming gate in the same session, discovering that a further entry's
"live-verified" reason had already gone false (see the comment above `_CONTAINMENT_LEDGER_MAX` for
the full account) — left ledgered and flagged rather than silently corrected out of this plan's
own stated scope. The Facts fence's `containment_ledger_cannot_reach` /
`containment_ledger_frozen_historical` / `containment_ledger_not_a_count_claim` counts above are
this reconciliation's own generated per-class tallies (`_containment_ledger_class_counts()`, never
hand-typed), summing to `containment_ledger_entries` exactly. The not-a-count-claim class is
published here as a residue this plan does NOT close — it needs containment's own citation-shape
stripper widened to recognise identifier, line-number-citation and arithmetic-expression shapes, a
REACH move on that stripper rather than a generated region, explicitly out of this phase's D-E
quantity-shaped scope — backlogged separately so it stays independently schedulable rather than
folded into the cannot-reach class it is not.

**(12) A Python module docstring is not "narrative prose" for NARR-02/criterion 3's
region target — decided, not left implicit.** `docs/PROCESS.md` section 2's own product/apparatus
cut (cited, not restated) draws the line by claim AUDIENCE: a module docstring's audience is
inside the build loop — a developer reading source, not a product's own README-facing surface —
which puts it on the apparatus side of that cut. NARR-02's own text already scopes its region
target to narrative prose on surfaces containment cannot reach — `docs/PROCESS.md`,
`docs/README.md`, `CONTRIBUTING.md`, `docs/MEASUREMENT-MAP.md`, `docs/COMPONENT-DIAGRAM.md` and
`docs/DATA-FLOW.md` — and this phase confirms that named set is exhaustive rather than widening
it to the `.py` docstrings too. The cost, stated honestly: this is the largest unadjudicated share
of the deferred-literal ledger — measured 2026-09-10 by counting `_DEFERRED_LITERAL_HITS` entries
carrying backlog `999.41` — and it stays ledgered under that existing blanket permit (bound (5)
above). Backlog `999.41` is where this closes; it is NOT closed by this phase.

Also decided here: `docs/v9.1-claim-containment-diagnosis.md` does not become a region host. That
page is a frozen diagnosis record whose figures are deliberately historical, and its own
discipline section already commits to pointing at a generated fact rather than restating one;
regionizing a frozen record would be the regression D-06 proviso 3 forbids (the same exception
bound (9)'s frozen-historical-count entries rely on).

### Criterion 3's published target

NARR-02's own scope names the containment-unreachable narrative surfaces plus `CLAUDE.md`
(`docs/PROCESS.md`, `docs/README.md`, `CONTRIBUTING.md`, `docs/MEASUREMENT-MAP.md`,
`docs/COMPONENT-DIAGRAM.md`, `docs/DATA-FLOW.md`, `CLAUDE.md`). Re-invoking
`run_literal_scan()` and filtering its hits to exactly that named set, in this session,
finds every hit on that set already carries a matching exemption class -- a hand-typed count
literal on those pages with no exemption class matching it is the target, and it is driven to
**zero**, over the shipped artifacts on disk today, not merely "the check passes": the same
`literal_scan_non_exempt` field the Facts fence above already publishes globally holds at zero
when the read is narrowed to this named-surface set (re-deriving the module and filtering
`run_literal_scan().hits` by `relpath` against the named set -- the exact command is transcribed
in `26-07-SUMMARY.md`). Before this phase, two of those pages (`docs/README.md`,
`docs/MEASUREMENT-MAP.md`) carried a live region-candidate restatement with no generated fence at
all -- the delta this phase closes, measured against `26-02-SUMMARY.md`'s own pre-migration
census rather than estimated: both candidates are now generated regions (bound (10) above),
`CLAUDE.md`'s own occurrence joined the roster the same way (plan 26-05), and the occurrence
outside the roster's reach is the fenced Mermaid label bound (9) already names. What this
narrowed-scope zero does NOT claim is answered by bound (13) below.

**(13) The cannot-reach residue behind criterion 3's published target is its own count, never
absorbed into the target above.** D-03's own load-bearing consequence is that a sentence stating a
value no gate currently `--describe`s cannot become a region until that gate exposes the field;
those sites are counted here, not fixed. The residue consists of exactly the sites already recorded
individually above: `tests/premise-rejection-catalog.md`'s second G3 demonstration target, which
carries no generated region at all so no value stated there can ever be corroborated (bound (8));
and `docs/COMPONENT-DIAGRAM.md`'s Mermaid node label, restating the coverage headline inside a
fenced code block that a non-fenced marker line cannot bracket (bound (9)). Re-deriving the
named-surface census this phase's own commands produce finds no further cannot-reach site beyond
these two -- the narrowed `literal_scan_non_exempt` reading the section above states is not a
wider population hiding behind an exemption class, it is genuinely exhausted by the exemption
classes named in the Facts fence. Following bound (8)'s own precedent, two alternatives were
rejected rather than built: a synthetic fixture proving a region mechanism could reach either site
(a control demonstrating a control's own presence rather than its measured effect, the same
vacuous shape bound (8) already rejects); and a widened criterion declaring a fenced or
unregioned occurrence out of scope by definition (which would silently absorb a real, currently-
live restatement rather than name it).

**(14) HEADLINE-LOCK verifies every surface `COVERED_HEADLINE_SURFACES` registers (D-27-08); `gen-gate-docs.py --write` produces only the `_NarrativeRegion`-backed subset.** `check-traceability.py`'s `COVERED_HEADLINE_SURFACES` registers the surfaces HEADLINE-LOCK's own self-test verifies -- `docs/gates/TRACE-03.md`'s own `registered_surfaces` field above states that population. This module's `narrative_regions` field above states the strictly narrower subset (`CLAUDE.md`, `docs/README.md`, `docs/MEASUREMENT-MAP.md`) that is `_NarrativeRegion`-backed and actually written by `--write`. The remaining members -- `docs/requirements-traceability.md` (the `**Coverage headline:**` line and the row-count sentence immediately below it) and `docs/COMPONENT-DIAGRAM.md` (its Mermaid node label, already named as structurally unreachable by bound (9) above, since the line sits inside a fenced code block a non-fenced marker line cannot bracket) -- both require a manual text edit on every headline move that HEADLINE-LOCK then VERIFIES rather than PRODUCES. Stated against Phase 27's own REL-07 clause, quoted verbatim: "produced by HEADLINE-LOCK's sweep, not a hand edit." The reading adopted: this is satisfied in the sense the requirement's own text is built on -- the *number* is machine-derived from `_rows_v91()`'s registration (never hand-computed) and machine-verified against every registered surface by HEADLINE-LOCK, so no surface states a figure nobody checked. It is NOT satisfied in the stronger sense that no file is manually touched by the sweep -- a strict subset of the registered surfaces requires exactly that on every future move. Widening `_NarrativeRegion`'s roster to cover the remaining members in this phase was rejected as a REACH move on the mechanism this phase measures rather than extends, out of scope for a release phase (D-27-08); publishing the residue here, rather than letting REL-07's clause read wider than what the sweep actually reaches, is this bound's own point.

## REACH-or-LEVEL determinations (v9.1.0, CONTAIN-01, CONTAIN-02, CONTAIN-03)

`docs/v9.1-claim-containment-diagnosis.md` §5a already classifies `CONTAIN-01`, `CONTAIN-02` and
`CONTAIN-03` as REACH at the requirement level, against `docs/PROCESS.md` §1.1's REACH/LEVEL
distinction. This section does not repeat that classification — `docs/PROCESS.md` §1's own rule
forbids restating a claim on a second surface. What follows instead is the per-change argument
§5a's own qualification asks for: §5a states that `CONTAIN-01`'s wider reach is, on its own, "a
wider point-fix, not a deeper one" unless paired with `CONTAIN-02`'s terminus arm. Making that
pairing good — naming, per change, the action a future contributor loses — is what the
paragraphs below do; the label itself is not asserted a further time.

**`CONTAIN-01` (reach).** The existing `docs/gates/*.md` containment guard
(`detail_page_containment_problems`) is pointed at `CLAUDE.md`, `docs/ARCHITECTURE.md` and
`docs/TESTING.md` — product surfaces stating the same shape of current-fact quantity claim it
already polices on the gate-detail pages, none of them reached before this phase. On its own this
widening is exactly the wider point-fix `docs/PROCESS.md` §1 warns against: it touches more files
with the same check, not a deeper one. What makes it a capability change rather than a wider
correction is its pairing with `CONTAIN-02`: the wider surface set is what gives the terminus arm
anything to see outside `docs/gates/*.md` in the first place, and the terminus arm is what makes
the wider surface set catch a shape of claim a flat containment pass structurally cannot — a chain
whose narrated final value has gone stale while every earlier hop stays true. Neither half carries
the argument alone: a wider reach with no terminus arm behind it is correction-only, and a terminus
arm with no reach beyond the gate pages behind it has nothing new to watch.

**`CONTAIN-02` (a new comparison, still REACH).** The new arm's subject is a chain's own terminus
value — the last hop of a narrated `N → M` (or a longer `N → M → P` sequence) — compared against a
value published inside that same page's own generated fence. The future action it removes: once
this arm lands, a contributor can no longer let a growth chain's own terminus drift away from the
live figure its page publishes without the check disputing it — an action that stays structurally
available today, as §5a's own measurement demonstrates, because the delta exemption strips a
chain's whole vector including its terminus. The arm's subject is a page's own claim about a live
figure, never a checker's own correctness, which is why this is REACH rather than the LEVEL move
`docs/PROCESS.md` §1.1 caps at L3: it points an existing product-guard's discipline at one more
thing the page says, it does not add a guard whose subject is `CONF-SURFACE`'s own correctness.

**`CONTAIN-03` (this section itself).** Writing this determination is not itself the meta-guard
regress `docs/PROCESS.md` §1 caps, because it adds no check, no CI job, no battery gate, and no
`--self-test` control asserting that a determination exists on this page. A control built to
assert the string "REACH" is present here would be exactly the label-assertion `CONTAIN-03`'s own
text forbids; what this requirement asks for is a written argument on a product page, read by a
reviewer, not scored by a mechanism.

Each unit landed in plans 25-02 and 25-03 carries a docstring line pointing at this section by
name — the function implementing the chain-terminus arm, and the call site widening containment's
reached-surface loop in `cmd_check()` — and none of them restates its content.

## REACH-or-LEVEL determinations (Phase 26, NARR-01, NARR-02, RATCHET-01, RATCHET-02, RATCHET-03)

### The cog question, answered

`.planning/research/STACK.md` recommends adopting `cogapp` for this problem, and
`.planning/research/ARCHITECTURE.md` §2 rejects that recommendation in terms. The two disagree, and
this project takes ARCHITECTURE.md's side (`26-CONTEXT.md` D-01): `cogapp` is not adopted, owing
STACK.md a written answer rather than a silent override. STACK.md's strongest point is conceded by name: cog's unit of
generation is a marked span inside an otherwise hand-written file, which is exactly the granularity
this problem needs — a whole-file or whole-table regeneration is the wrong shape for a narrative
paragraph carrying one live number. D-01 and D-02 reproduce that identical granularity without the
dependency: `_replace_region` and `_replace_or_bootstrap_region` already swap an exact marked span
between two anchor lines, and `_generated_marker_pairs_for` already registers which surface owns
which span, the same primitives `generate_all()` already uses to bootstrap the CI-gate-table
regions on `CLAUDE.md`, `docs/ARCHITECTURE.md` and `docs/TESTING.md`. A new host page's sentence
region is a call-site and registration change to those existing primitives, not a new generation
engine. The accepted cost of D-02's one-sentence granularity is stated plainly, citing
`.planning/research/ARCHITECTURE.md` §3's finding about `report-conformance.py`: that file's own
narrative is prose living as a Python string, so the sentence's wording now lives in Python code
rather than Markdown, and re-wording it (not re-valuing it) means editing and re-running a script.
That cost is paid once already, on a whole-page scale, and D-02 pays a narrower version of the
identical cost at sentence scale.

### The RATCHET verdicts, landed

RATCHET-01 is KEEP (REACH) — see `docs/v9.1-claim-containment-diagnosis.md` section 6's own
"RATCHET-01" subsection for the argument in full, cited here rather than restated. RATCHET-02 is
KEEP (REACH) — see that same section 6's "RATCHET-02" subsection. RATCHET-03 is DROP (LEVEL) — see that
same section 6's "RATCHET-03" subsection. What section 6 could not know, because the mechanism it judges did not
exist yet, is added here rather than re-argued: RATCHET-01's KEEP argument never turned on which
CLI compares a generated region to its own generating source — it turns on the comparison itself —
so substituting `scripts/gen-gate-docs.py --check` for `cog --check` (D-01) leaves the verdict
fully intact. The landing site is pre-commit gate 5 (`gen-gate-docs.py --check`, already present):
no additional pre-commit gate, no CI job and no battery registration is added to carry this arm.

### RATCHET-01, demonstrated by mutation

Per this plan's own mutation protocol, RATCHET-01 was proved by mutation, not by reading. On a
disposable `rsync --exclude .git` scratch copy -- the real repository confirmed clean by `git
status --porcelain` before the first mutation and after the last -- Arm A (the unmutated control)
passed `--check` unchanged; Arm B (mutating a narrative region's own rendered value on
`docs/README.md`, without touching any constant) made `--check` fail with a `DRIFT:` line naming
that file; Arm C (mutating a different, currently-accurate region on `CLAUDE.md`, a different host
surface) made `--check` fail with an independent `DRIFT:` line naming that second file, proving the
check is general rather than fitted to Arm B's own target; and the census arm (a hand-typed
restatement of a region's own rendered value appended to `docs/MEASUREMENT-MAP.md`, outside any
generated fence) made `--check` fail naming the file and the exact line. Every mutation was
restored and confirmed byte-identical against the real repository via `md5sum` before the next arm
ran. The full transcript, verbatim, is recorded in this plan's own summary (`26-07-SUMMARY.md`). No
sixth pre-commit gate, no CI job and no battery registration was added to carry this demonstration
-- it runs entirely through pre-commit gate 5 (`scripts/gen-gate-docs.py --check`), which already
existed.

### The meta-guard-regress argument, recorded

With RATCHET-03 dropped, the remaining pair is both REACH: neither RATCHET-01 nor RATCHET-02 takes
another guard's own correctness as its subject — RATCHET-01 compares generated prose to its live
generating source, and RATCHET-02 bounds a ledger's own product-visible size. `docs/v9.1-claim-
containment-diagnosis.md` section 6's "Whether the three together constitute the meta-guard regress"
subsection is cited for the argument in full; it is not reproduced here. This page's own new
narrative-restatement census (part 4 below, wired by a later plan in this phase) is classified
explicitly rather than left to fall through an implicit gap.

### Forward REACH-or-LEVEL determinations for this phase's own new mechanisms

Written here before any of the following exists, per RATCHET-04's own ordering requirement.

**NARR-01** is a non-code convention: REACH. `docs/v9.1-claim-containment-diagnosis.md` §5a
already classifies it; that classification is cited, not re-transcribed. Answered in one sentence,
per test 3's own worked framing: a generalized scope clause on an existing rule is not a second
rule governing whether the first rule was followed — it widens what the rule already reaches, the
same move §1.1's own worked example makes for a scanned population, rather than adding a rule that
audits the rule, which is what keeps the classification REACH rather than the LEVEL move §1.1
caps.

**NARR-02's generated narrative regions** point the "a moving value is generated, not hand-typed"
discipline this page's own containment mechanism already practices at more host pages — pages
containment structurally cannot reach today. The subject is a rendered sentence's own currency
against its harvested source, not another guard's correctness: REACH.

**The narrative sentence-region roster equality floor** is the identical set-equality-plus-
independently-transcribed-lock shape `_CONTAINMENT_SURFACES`/`_CONTAINMENT_SURFACES_LOCK` already
use for the containment loop, applied to the new region roster rather than to a new subject. Its
own subject is which product pages carry a registered region, a product-visible fact, never a
guard's correctness: REACH.

**The narrative-restatement census** that a later plan in this phase wires into `cmd_check()` names
its own subject explicitly: hand-typed restatements of an already-generated value on a product
surface, not another guard's correctness. It is therefore REACH, the identical argument
`_scan_text_for_literal_hits()` itself already carries for the standing literal scan it extends.

### The capability statement

Once this phase lands, a contributor will no longer be able to hand-type the live coverage headline
on a registered narrative surface, outside that surface's own generated region, and reach `HEAD` —
`CLAUDE.md` is the named surface this is proved against — because pre-commit gate 5 disputes both a
stale region body and a hand-typed restatement sitting outside it. Two facts make this a capability
change rather than a wider point-fix, per test 1's own framing: those sentences are hand-typed
today, and `HEADLINE-LOCK`'s own disclosed bound — cited from `CLAUDE.md`'s Key invariants rather
than restated — means a green sentinel is compatible with stale prose surviving on every one of
them, because a line still stating the superseded figure produces no hit at all. Removing that
surviving action, on the named surface, is the structural change this phase makes possible.

### The capability statement, demonstrated

Plan 26-01 wrote the capability statement above before any of this phase's mechanism existed --
a pre-commitment, not yet an observation. Restated here as a fact with its own evidence: a
contributor can no longer hand-type the live coverage headline on `CLAUDE.md`, outside its own
generated region, and reach `HEAD` -- Task 1's Arm C transcript (`26-07-SUMMARY.md`) is the
demonstration, mutating that exact region on that exact page and watching pre-commit gate 5
dispute it by name; the census arm's own transcript demonstrates the sibling capability change,
that a hand-typed restatement of a rendered value OUTSIDE its region, on any roster page, is
disputed too, naming the file and the line. The prior bound this closes is `HEADLINE-LOCK`'s own
disclosed bound, cited from `CLAUDE.md`'s Key invariants rather than restated: a line stating a
superseded figure used to produce no hit at all, because a green sentinel and stale prose could
coexist. What is NOT closed, stated plainly: the residue bound (13) just above (the two cannot-
reach sites), and every narrative page outside the roster's own fixed population -- a page that is
not `docs/README.md`, `docs/MEASUREMENT-MAP.md` or `CLAUDE.md` may still carry a hand-typed
restatement of the same value with nothing here to dispute it, unless that page also happens to
sit on the registered literal-scan surface set already (bound (10) above states this limit).

### The four self-referential tests, answered for this phase

**Test 1 (capability, not correction).** Answered directly above: the specific action a
contributor loses is hand-typing the coverage headline on `CLAUDE.md` outside its own region and
reaching `HEAD`, demonstrated by mutation rather than asserted.

**Test 2 (sibling site named first).** `26-02-SUMMARY.md`'s pre-migration census named every
region candidate and the one structurally-unreachable occurrence BEFORE any region was built --
the sibling-site discipline `docs/v9.1-claim-containment-diagnosis.md` established for CR-01/CR-02
applied to this phase's own new mechanism from its first plan, not retrofitted afterward.

**Test 3 (REACH-or-LEVEL in writing).** Plan 26-01's determinations section, written before any of
NARR-01, NARR-02, RATCHET-01, RATCHET-02 or the roster/census wiring existed, is the citation --
see "Forward REACH-or-LEVEL determinations for this phase's own new mechanisms" above, dated ahead
of the build it judges.

**Test 4 (recurrence, not compliance).** This phase's own verification is not "was the
generated-region convention followed" -- it is whether a stale live count can reach `HEAD` on the
migrated surfaces at all, the same distinction `docs/PROCESS.md` draws between measuring
recurrence and scoring compliance. That measurement lands at `REL-08`, this milestone's own
product-recurrence check, not inside this phase's own exit record.

### Requirement amendment (D-04)

`.planning/REQUIREMENTS.md`'s NARR-02 and RATCHET-01 texts, and `.planning/ROADMAP.md`'s Phase 26 success
criterion three (the exemption-class entry) and success criterion four (the pre-commit-blocking
behavior), named `cog`, `cog --check` and `cog-generated-region` as the mechanism to be built. This phase amends all four sites to name the mechanism actually built —
`generated-narrative-region` and `scripts/gen-gate-docs.py --check` — citing
`.planning/research/ARCHITECTURE.md` §2's rejection as the reason, in the same shape as the
existing CONF-12 amendment entry above. The edit is recorded here so a later reader cannot mistake
it for drift; the edits themselves land on their own surfaces, not here.
