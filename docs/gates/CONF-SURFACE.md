# CONF-SURFACE: The claim-surface drift gate itself: regenerates `CLAUDE.md`'s and docs/ARCHITECTURE.md's gate tables and docs/gates/<ID>.md pages from this registry's ENTRIES and every gate's --describe emission, and fails on drift.

<!-- GENERATED:FACTS -->
## Facts

- `registered_surfaces` (29): `CLAUDE.md`, `docs/ARCHITECTURE.md`, `docs/COMPONENT-DIAGRAM.md`, `docs/DATA-FLOW.md`, `docs/MEASUREMENT-MAP.md`, `docs/README.md`, `docs/TESTING.md`, `docs/gates/*.md`, `scripts/check-act-limb.py`, `scripts/check-agent.py`, `scripts/check-conf-gate.py`, `scripts/check-description-budget.py`, `scripts/check-focused-parity.py`, `scripts/check-high-confidence-bound.py`, `scripts/check-install-collisions.py`, `scripts/check-links.py`, `scripts/check-loop-closure.py`, `scripts/check-provenance.py`, `scripts/check-quality-harness.py`, `scripts/check-registration.py`, `scripts/check-routing-battery.py`, `scripts/check-selfaudit-scan.py`, `scripts/check-step0-emulator.py`, `scripts/check-step0-live.py`, `scripts/check-traceability.py`, `scripts/check-trigger-collisions.py`, `scripts/check-version-stamps.py`, `scripts/report-conformance.py`, `scripts/sync-content.py`
- `checked_files` (56): `CLAUDE.md`, `docs/ARCHITECTURE.md`, `docs/COMPONENT-DIAGRAM.md`, `docs/DATA-FLOW.md`, `docs/MEASUREMENT-MAP.md`, `docs/README.md`, `docs/TESTING.md`, `docs/gates/BATT-06.md`, `docs/gates/COLLIDE-01.md`, `docs/gates/CONF-GATE.md`, `docs/gates/CONF-SURFACE.md`, `docs/gates/DUAL-04.md`, `docs/gates/FROZEN-EVIDENCE.md`, `docs/gates/GATE-01.md`, `docs/gates/GATE-02-v8.5.md`, `docs/gates/HARN-01.md`, `docs/gates/HARN-02.md`, `docs/gates/HARN-03.md`, `docs/gates/HC-BOUND.md`, `docs/gates/INVARIANT-CHECK.md`, `docs/gates/PRECOMMIT-conformance-baseline-drift-gate.md`, `docs/gates/PRECOMMIT-sync-drift-gate.md`, `docs/gates/PROV-GUARD.md`, `docs/gates/QUAL-01.md`, `docs/gates/REG-GUARD.md`, `docs/gates/SCAN-GUARD.md`, `docs/gates/STEP0-06.md`, `docs/gates/STEP0-08.md`, `docs/gates/TRACE-03.md`, `docs/gates/VAL-01.md`, `docs/gates/VAL-02.md`, `docs/gates/VAL-03.md`, `docs/gates/VAL-04.md`, `docs/gates/VAL-05.md`, `docs/gates/VERSION-01.md`, `scripts/check-act-limb.py`, `scripts/check-agent.py`, `scripts/check-conf-gate.py`, `scripts/check-description-budget.py`, `scripts/check-focused-parity.py`, `scripts/check-high-confidence-bound.py`, `scripts/check-install-collisions.py`, `scripts/check-links.py`, `scripts/check-loop-closure.py`, `scripts/check-provenance.py`, `scripts/check-quality-harness.py`, `scripts/check-registration.py`, `scripts/check-routing-battery.py`, `scripts/check-selfaudit-scan.py`, `scripts/check-step0-emulator.py`, `scripts/check-step0-live.py`, `scripts/check-traceability.py`, `scripts/check-trigger-collisions.py`, `scripts/check-version-stamps.py`, `scripts/report-conformance.py`, `scripts/sync-content.py`
- `derived_counts` (12 entries): `literal_scan_exempt_commonmark-heading-depth`=0, `literal_scan_exempt_deferred-remediation`=134, `literal_scan_exempt_headline-provenance-delta`=11, `literal_scan_exempt_maxturns-60-value`=0, `literal_scan_exempt_plan-number-identifier`=3, `literal_scan_exempt_retired-body-budget`=1, `literal_scan_exempt_sha256-digest`=0, `literal_scan_exempt_version-stamp-count`=3, `literal_scan_hits`=152, `literal_scan_non_exempt`=0, `literal_scan_read_files`=56, `literal_scan_surfaces`=29
- `disclosed_bounds_anchors` (5): `line-scoped-detection`, `currency-not-correctness`, `closed-spelled-out-vocabulary`, `py-docstrings-only`, `deferred-remediation-is-budget-driven`
- `control_ids` (49): `arithmetic-sentence-pluralizes-correctly`, `check-dispatch-wired`, `check-reports-full-drift-count`, `containment-satisfied-passes`, `containment-spelled-out-normalised`, `containment-violation-fires`, `describe-emits-parseable-json`, `floors-run-together`, `framing-sentences-replaced`, `frozen-path-write-fires`, `frozen-paths-derived-not-typed`, `gates-link-resolves-per-surface`, `harvest-malformed-json-named`, `harvest-nonzero-exit-named`, `harvest-one-bad-does-not-abort`, `narrative-preserved-across-regeneration`, `no-row-wrapped`, `nondeterminism-exit-2`, `one-renderer-two-surfaces`, `page-per-entry`, `population-arithmetic-derived`, `region-duplicate-end-raises`, `region-duplicate-start-raises`, `region-end-before-start-raises`, `region-happy-path`, `region-marker-in-fence-ignored`, `region-preserves-crlf`, `region-preserves-final-newline`, `region-preserves-surrounding-prose`, `region-real-file-claude-md`, `region-tilde-fence-quoting-backticks`, `region-zero-end-raises`, `region-zero-start-raises`, `row-count-equals-entries`, `scan-coverage-floor-fires`, `scan-coverage-floor-signature-locked`, `scan-docstring-only`, `scan-exempt-class-attributed`, `scan-glob-narrowing-fires`, `scan-hit-inside-fence-passes`, `scan-hit-outside-fence-fires`, `scan-neutralization-arms`, `scan-spelled-out-detected`, `scan-unattributable-permit-fires`, `testing-index-links-resolve`, `testing-index-row-count-equals-entries`, `testing-real-file-region`, `thin-page-fully-generated`, `trace03-glob-substring-derived`
- `control_count`: `49`
- `locked_constants` (2 entries): `generated_end_marker`='<!-- END GENERATED -->', `generated_marker`='<!-- GENERATED — DO NOT EDIT. Source: {source}. Regenerate via: scripts/gen-gate-docs.py --write. -->'
<!-- END GENERATED:FACTS -->

<!-- GENERATED:HOW-TO-RUN -->
## How to run

```sh
python3 scripts/gen-gate-docs.py --self-test && python3 scripts/gen-gate-docs.py --check
```

CI job: `gen-gate-docs`
<!-- END GENERATED:HOW-TO-RUN -->

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
reaches exactly the module-level docstring; a comment or an in-code string
constant carrying a hand-maintained count is out of this scanner's reach by
construction. The written reason, carried over from the baseline: a
literal sitting beside the constant it describes has a much shorter drift
distance than the scattered cross-file prose this scanner exists to
police, so a comment-level count is lower-risk.

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
CommonMark heading-depth range, and `deferred-remediation`) sits in the
Facts fence above, each keyed `literal_scan_exempt_<class-name>`.

**(5) `deferred-remediation` is a budget-driven whole-surface deferral, not
a content-based exemption.** Plan 21-10's Task 3 inherited a non-exempt-hit
count and a file count both far beyond the task's own ~15-item/6-file
working budget (see the Facts fence above for the exact reading before
this class existed: `21-CONF13-BASELINE.md`'s "Plan 21-10 disposition
ledger" section states it directly). It hand-remediated every item on the
surfaces its own scope named (`docs/COMPONENT-DIAGRAM.md`,
`docs/MEASUREMENT-MAP.md`, `docs/DATA-FLOW.md`, `docs/README.md`), and
deferred the rest as three coherent groups, each under its own numbered
backlog id, each matched by relpath (never by hit text) in
`scripts/gen-gate-docs.py`'s `_DEFERRED_REMEDIATION_SURFACES`:

- **backlog `999.32`** — the `docs/gates/*.md` narrative pages
  (`QUAL-01.md`, `SCAN-GUARD.md`, `TRACE-03.md`, `CONF-GATE.md`,
  `GATE-01.md`, `HC-BOUND.md`, `REG-GUARD.md`, `VAL-02.md`,
  `VERSION-01.md`, `STEP0-08.md`). Root cause: dense hand-written/migrated
  technical narrative uses ordinary-language small numbers that D-06's own
  citation-exemption vocabulary (plan 21-08) already learned to ignore for
  containment purposes, but this scanner does not share that vocabulary.
- **backlog `999.33`** — the `.py` module docstrings this scanner reads.
  Root cause: the same ordinary-language-number shape in dense narrative
  docstrings; `21-CONF13-BASELINE.md`'s own false-positive layer
  (ordinal-label-reference, adjacency-mistrack, enumerated-list-marker)
  was deliberately not ported into this standing scanner (plan 21-09's own
  key-decision).
- **backlog `999.34`** — `CLAUDE.md`, `docs/ARCHITECTURE.md`,
  `docs/TESTING.md`. Root cause: these three carry operational/provenance
  narrative outside the generated CI-gate-table region (D-02) or outside
  the CI-gate `###` sections `docs/TESTING.md`'s own fold reached (D-21-F).

Full item counts, reasons and the per-item closing move for every
hand-remediated item are recorded in
`.planning/phases/21-generate-the-claim-surface/21-CONF13-BASELINE.md`'s
"Plan 21-10 disposition ledger" section. Closing any of the three deferred
groups requires either porting D-06's citation-exemption vocabulary into
this scanner, or hand-remediating the named surfaces with the same three
moves (point at generated fact / corroborate / exempt with a named class)
— then removing the corresponding entries from
`_DEFERRED_REMEDIATION_SURFACES`.
