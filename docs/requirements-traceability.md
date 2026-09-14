# Requirements and Traceability

This file is the active canonical source of truth for requirements and traceability in this project; it supersedes the 26 scattered `milestones/vX.Y-REQUIREMENTS.md` files for all forward use (CANON-01).

## Status

**Coverage headline:** 244 reproducible / 151 audit-only / 0 gap / 395 total

The full capability-to-requirement-to-test mapping — its row count is the total in the coverage
headline above — is in the generated matrix:
[`requirements-matrix.md`](requirements-matrix.md)

> **Honesty note (D-07):** A non-zero audit-only count is the expected honest success state.
> The audit-only count in the coverage headline above counts requirements validated by milestone audit or inspection without a re-runnable gate;
> No current open gaps — GEN-01 → reproducible (Phase 93; artifact bumped to the committed v7.13 residual-delta live re-baseline Phase 137; latest artifact `tests/step0-baseline-v7.13.md`; reproducible = measured, not passing — v7.13 S-P02 1/5, S-P10 0/5, S-P14 0/5 all CARRIED; v7.8 remains the canonical full 8-technique baseline) and GEN-02 → reproducible (runbook + wrapper; artifact `docs/live-monitoring-runbook.md`);
> 3 further requirements are confirmed by offline gates but remain honest live carry-forwards (RR-80-01, RR-114-01 (supersedes RR-108-01, supersedes RR-95-01, supersedes RR-92-01, supersedes RR-79-02), RR-77-08); RR-108-02 is CLOSED at 4/5 ≥ min-pass (Phase 114 v7.6 re-baseline — ID retained, sentinel present as regression guard); RR-79-01 is CLOSED at 3/5 ≥ min-pass (Phase 117 v7.7 CONF-01; CLOSE SUSTAINED 3/5 at Phase 119 v7.8 CONF-03 — ID retained, sentinel present as regression guard); RR-117-01 (S-P03 fishbone) CLOSED 5/5 at Phase 117 CONF-01; CLOSE SUSTAINED 4/5 at Phase 119 CONF-03; RR-117-02 (S-N03 precision) minted Phase 117 CONF-02, re-pointed to v7.8 Phase 119 CONF-04; RR-119-01/RR-119-02 (S-N01/S-N02 resolved-over-bar) minted Phase 119 CONF-04.
> **v8.0 audit-validated-reqs note (D-02):** v7.12, v7.13, and v8.0 requirements are validated by their milestone audits rather than matrix rows (honest-state framing of the zero-drift headline; the 9 v8.0 requirements are not registered as matrix rows per Phase 142 D-01). All three Step 0 residuals (RR-114-01 1/5, RR-108-04 0/5, RR-108-05 0/5) are v8.0 ACCEPTED-FINAL — see the v8.0 Terminal State block below.

> **v8.26 CHAINHEAD deferred-registration note, dated 2026-09-03 (Phase 13 plan 13-28):** this is a
> separate note beside D-02 above, not an extension of it — D-02 is written for v7.12/v7.13/v8.0
> specifically and must not be silently widened. `CHAINHEAD-01..07` (Phase 13's own requirements)
> and the milestone's remaining requirements (Phase 14's LEDGER-01..04, Phase 15's
> SCAN-01..04, Phase 16's SHIP-01..05) were deliberately row-less as of this note: v8.26.0's
> twenty requirements were to be registered as matrix rows in one lockstep batch at Phase 16, per
> ROADMAP's Phase 16 success criterion 3
> ("This milestone's 20 requirements are registered as matrix rows; the resulting
> coverage-headline move … is produced by `HEADLINE-LOCK`'s sweep rather than a hand edit, and
> the sentinel confirms it."). Registering seven of the twenty here
> would have moved the headline twice, by hand the second time, and split a lockstep registration
> Phase 16 exists to perform in one sweep.
>
> **Deferral discharged, dated 2026-09-04 (Phase 16 plan 16-02, SHIP-03):** this deferral is now
> closed. All twenty requirements (SHIP-05 was added 2026-09-04, raising the milestone's total by
> one — see `.planning/REQUIREMENTS.md`'s closing footer) were registered as matrix rows in one
> lockstep batch (`_rows_v826()`), moving the coverage headline
> `175/91/0/266` → `192/94/0/286` (headline-history row 12 below), produced by
> `HEADLINE-LOCK`'s sweep rather than a
> hand edit, per the ROADMAP criterion quoted above. `13-REVIEW.md` WR-05 called the pre-discharge
> absence undisclosed, not wrong; this note was, and remains, the disclosure.

> **Departure from the note above, dated 2026-08-29 (v8.18 Phase 4 / D-05, D-08):** the note above
> is left byte-intact as the record of what Phase 142 decided; this addendum states where v8.18
> departs from it and why. The v8.18 milestone's 23 requirements (ACT-01..05, LOOP-01..05,
> PAR-01..03, HARN-01..04, SHIP-01..06) **are** registered as matrix rows — the first **v8.x** milestone
> block since v7.9 (Phase 123 RECON-01) to add rows rather than resting on audit alone — the
> v7.11 block (Phase 131 RECON-03) added 11 audit-only rows in between, so the qualifier is
> load-bearing. The discriminator is the test headline-history row 2 already uses to justify that
> v7.9 block: **"each backed by a deterministic offline gate."** v7.12, v7.13, and v8.0 were live-measure and audit
> milestones with no deterministic offline gate behind their requirements — the note above states
> that correctly for its own moment. HARN-01/HARN-02/HARN-03 are deterministic, offline, and (per
> D-01/D-03 of `.planning/phases/04-ship/04-CONTEXT.md` — local-only, git-ignored; not present in
> a fresh clone, so named as plain text rather than linked, the same treatment the Cross-links
> section gives `docs/history/` and `.planning/PROJECT.md`) registered in both the firewall
> battery and CI, so v8.18's 21 gate-backed requirements are the first since v7.9 to satisfy the
> same test the note above applies to v7.12/v7.13/v8.0. This addendum therefore applies the
> project's own rule to a new milestone that happens to meet it, rather than making an exception
> to that rule. The Phase 142 note stands unedited as an accurate record of what was decided at
> that time, for the milestones it names.

> **Row-less shipped releases, dated 2026-09-13 (v9.3.0 Phase 33):** this is a separate note beside
> the D-02 note above, not a widening of it — D-02 names v7.12, v7.13 and v8.0 only. `v8.22.0` and
> `v8.23.0` are CHANGELOG-only releases with no requirements archive, so no row can carry a sourced
> statement — every row carries its sourced wording or the literal `statement unrecoverable`; none is
> reconstructed (D-T4). They are row-less by that rule, not by oversight. `v9.2.2`, `v9.2.3` and
> `v9.2.4` are the same class — CHANGELOG-only post-`v9.2.1` product patches with no requirements
> archive — and are row-less for the identical reason. The `v8.21.0` git tag is superseded: its
> stamps read `8.20.0`, and the content it names was released under CHANGELOG `[8.22.0]`. The v8.19,
> v8.20 and v8.21 requirements this phase registers are sourced from
> `.planning/milestones/v8.21.0-REQUIREMENTS.md` (the archive, not the tag) and are cited
> milestone-qualified throughout, for example `v8.21/GATE-05`, so none reads as an unqualified gate
> id or as a v8.24 requirement.
>
> Two further sibling sites are named here, not fixed (out of this phase's ROWS-01..05/RESID-01/02
> boundary): the Historical Ledger's own "v6.1 through v8.0" range sentence below does not
> individually name-match `v6.0`, `v6.2`, `v6.3`, `v7.0`, `v7.2` or `v7.3`, though each sits inside
> that stated range; and the point-release git tags between `v8.1` and `v8.17.5` sit past that
> sentence's own stated endpoint (`v8.0`) and are not covered by it at all. Neither has a
> `.planning/milestones/` archive or a `docs/history/` snapshot, so D-T4 governs regardless of how
> precisely that sentence names its range.

> **PROV-GUARD registered, dated 2026-08-31 (v8.24 Phase 6 / D-01, D-14):** `scripts/check-provenance.py`
> is registered as gate id **`PROV-GUARD`** — not `PROV-01`, since that is a requirement id in this
> milestone and `GATE-01` was already taken by `check-agent.py` — on both surfaces: CI job
> `check-provenance (PROV-GUARD)` and a battery `gate` call running `--self-test` **and** the live
> leg. It asserts that every `*Provenance: read-at-source*` ground truth in an analysis's section 3
> joins to a real `WebFetch`/`Read` of that source in the run's stored `.jsonl` capture, and that
> every literal the ground truth states appears verbatim in that source's retrieved text. Live
> result, quoted verbatim rather than paraphrased: `7/7 sources matched, 35/35 literals located`.
> In one sentence: every other column `detect_defects` emits scores the *form* of an analysis; this
> is the first check in the stack that can falsify a `*Provenance: read-at-source*` label against
> what the run actually fetched — it records fact, not form.
>
> **What it does not assert** — four documented limits, each traceable to the module docstring:
> 1. it verifies a stated number appears in the retrieved text of the named source; it does not
>    verify the number *means* what the analysis says, nor that the chain citing it is valid
>    inference — that is backlog `999.4`;
> 2. the literal regex also matches digit runs that are the tail of an alphanumeric identifier
>    (`x86` yields `86`), which still verify but carry no independent evidentiary weight — expected
>    behaviour, not a parser bug;
> 3. whole-span bold/quoted matching was measured and rejected (`4/11` bold spans, 4/8 quoted spans
>    located) and must not be resurrected as a "cleaner" rule;
> 4. PROV-04's no-network control blocks `socket`; it does not cover a `subprocess` shell-out — a
>    stated residual.
>
> **Why VAL-04 is the milestone's one audit-only row:** no gate re-runs to check that a docs record
> exists (the v8.18 SHIP-04/SHIP-05 precedent), which is why this addendum is the record.

**Headline history (D-01).** The coverage headline has moved once for every row of this table
except rows 4 and 5, which the table itself marks as deliberate zero-drift reconciliations that
moved no count — counted from the table, never restated as a number here — since the matrix was
first regenerated at 121/85/0/206 (Phase 119 CONF-04). **Correction, dated 2026-09-09 (Phase 23
plan 02):** this sentence read "nine times" immediately before this edit, which already disagreed
with the 12 rows then on the table (10 non-zero-drift rows, not 9) — a pre-existing instance of
the class this milestone measures, found and corrected here rather than silently absorbed
alongside row 13's own addition. **Reworded, dated 2026-09-13 (v9.3.0 Phase 33):** this sentence
carried a hand-typed count ("moved fourteen times … (1-16)") that every new row made stale; it now
points at the table's own rows instead. This table is a compact change log — one row per
reconciliation event — replacing what used to be seven separately stacked prose annotations.
Every delta below is already discharged — no row is a currently-open action item.

| # | Milestone / task | Headline before → after | Cause |
|---|-------------------|--------------------------|-------|
| 1 | Phase 119 CONF-04 | 121/85/0/206 → 125/85/0/210 | +4 reproducible rows added to the active tail: RR-117-01 (S-P03 fishbone, minted Phase 117 CONF-02), RR-117-02 (S-N03 precision, minted Phase 117 CONF-02), RR-119-01 (S-N01 resolved), RR-119-02 (S-N02 resolved) — these existed as sentinels in `_battery_core.py` but were not previously registered as matrix rows. |
| 2 | Phase 123 RECON-01 | 125/85/0/210 → 133/85/0/218 | +8 reproducible rows: the v7.9 milestone requirements NEGCAT-01, NEGCAT-02, OCH-01, OCH-02, OCH-03, COLLIDE-01, COLLIDE-02, RECON-01, each backed by a deterministic offline gate (STEP0-08 for NEGCAT-01/02; DUAL-04 + BATT-06 for OCH-01/02/03; COLLIDE-01 gate for COLLIDE-01/02; TRACE-03 for RECON-01). |
| 3 | Phase 131 RECON-03 | 133/85/0/218 → 133/96/0/229 | +11 audit-only rows: the v7.11 milestone requirements READY-01/02/03, STEP0L-01/02/03, ROUTEL-01/02, RECON-01/02/03 (audit-only; validated by one-shot manual live runs, not deterministic offline CI gates, D-04). GEN-01's artifact_link bumped v7.8 → v7.11 (paired data + gate-code edit, D-05). RR-130-01 (main-routing inline-answering regression) recorded as a documented residual with NO matrix row (v7.9 D-02 precedent). |
| 4 | Phase 133 (RR-130-01 fix) | 133/96/0/229 → 133/96/0/229 | **Zero drift.** RR-130-01 remains a documented residual with no matrix row (v7.9 D-02 precedent); the fix is a prose edit in `shared/` with no new matrix row. Reconcile = prove zero drift, not re-count (D-03). |
| 5 | Phase 138 RECON (v7.13) | 133/96/0/229 → 133/96/0/229 | **Zero drift.** v7.13 live measurements moved no counts: RR-130-01 RESOLVED/CLOSE at Phase 136 (P 11/13 = v3.13 anchor recovery), row-less per v7.9 D-02 precedent; S-P02 inversion 1/5 CARRIED (RR-114-01, ID kept), S-P10 estimate 0/5 CARRIED (RR-108-04, ID kept), S-P14 theoretical-limit 0/5 CARRIED (RR-108-05, ID kept); GEN-01 artifact_link bumped v7.11 → v7.13 (paired data + gate-code edit, D-05); 3 residual BATT-06 sentinels re-pointed v7.11 → v7.13 (Phase 138-02). |
| 6 | v8.8 post-close TEARDOWN-01 cleanup | 133/96/0/229 → 132/97/0/229 | −1 reproducible / +1 audit-only. Requirement **META-Q4** (agent-body budget) was re-tiered `reproducible` → `audit-only` in `scripts/check-traceability.py` and the matrix regenerated. It had been tiered `reproducible` on the strength of `scripts/git-hooks/pre-commit` invoking `scripts/check-body-budget.py`; TEARDOWN-01 (v8.7 Phase 163) retired the body-budget stanza from that hook, so the hook no longer invokes the script. The body line count is now report-only (`check-body-budget.py` always exits 0; reported every firewall-battery run as `[INFO] body-size` but not gated) — inspectable, not reproducibly enforced, i.e. genuinely audit-only. |
| 7 | quick task `260728-vxn` | 132/97/0/229 → 126/88/0/214 | −6 reproducible / −9 audit-only. All 15 v4.0/v4.1 builder requirements (CLI-01, CLI-02, CLI-03, CLI-04, CLI-05, CLI-06, CLI-07, CLI-08, INST-01, INST-02, INST-03, INST-04, INST-05, INST-06, INST-07) were retired from `scripts/check-traceability.py` and are absent from both regenerated artifacts. 9 audit-only rows were removed (CLI-01..08 + INST-06) and 6 reproducible rows were removed (INST-01..05, INST-07), for a net −15 total rows (229 → 214). The source of this decision is `docs/technical-debt-audit-2026-07-28.md`, whose top-listed Decision-For-The-User was a binary choice — repair the builder's test coverage and keep it, or retire the whole trio — and the user chose retire. `main.py`, both `templates/*.tmpl` files, the gitignored `generated/` output directory, and the four builder test files (`tests/test_59_02_task1.py`, `tests/test_60_01_check_agent_candidate.py`, `tests/test_64_01_install.py`, `tests/test_builder_check_adapters.py`) were deleted in the same quick task. **This is a product decision, not a coverage downgrade** — the 15 requirements are not unmet; the deliverable they described no longer exists. |
| 8 | v8.18 Phase 4 (SHIP-03 / D-05) | 126/88/0/214 → 147/90/0/237 | **+21 reproducible / +2 audit-only.** The 23 v8.18 milestone requirements (ACT-01..05, LOOP-01..05, PAR-01..03, HARN-01..04, SHIP-01..06) were registered as matrix rows for the first time (`_rows_v818()`, `scripts/check-traceability.py`) — the first **v8.x** milestone block added since v7.9 (row 2 above; row 3's v7.11 block is the last non-v8.x addition in between). 21 are reproducible, each backed by a deterministic offline gate (`scripts/check-act-limb.py`, `scripts/check-loop-closure.py`, `scripts/check-focused-parity.py`, `scripts/check-firewall-battery.sh`, `scripts/sync-content.py`, `scripts/check-version-stamps.py`); SHIP-04 and SHIP-05 are audit-only because no gate re-runs to check a CHANGELOG entry or a docs record. See the dated addendum beside the Phase 142 D-01 note above for why this departs from that note. |
| 9 | v8.24 Phase 6 (D-06/D-07) | 147/90/0/237 → 161/91/0/252 | **+14 reproducible / +1 audit-only.** The 15 v8.24 milestone requirements (CAP-01..03, PROV-01..05, GATE-01..03, VAL-01..04) were registered as matrix rows for the first time (`_rows_v824()`, `scripts/check-traceability.py`). 14 are reproducible, each backed by a deterministic offline gate (`scripts/check-provenance.py`, `scripts/check-quality-harness.py`, `scripts/check-registration.py`, `scripts/check-firewall-battery.sh`, `scripts/check-version-stamps.py`, `scripts/sync-content.py`); VAL-04 is audit-only because no gate re-runs to check that a docs record exists — the v8.18 SHIP-04/SHIP-05 precedent. The gate list here is the corrected one: the v8.24 code review found CAP-01/CAP-03 pointed at `check-provenance.py`, which verifies neither, and GATE-02 pointed at `check-firewall-battery.sh`, which never read its deliverable — all three were re-pointed at assertions that actually re-run them (CR-02, WR-02), leaving this row's tier partition unchanged. |
| 10 | v8.25 Phase 12 (A1/A2) | 161/91/0/252 → 174/92/0/266 | **+13 reproducible / +1 audit-only.** The 14 v8.25.0 milestone requirements (HEADLINE-01..05, CONTRACT-01..06, SHIP-01..03) were registered as matrix rows for the first time (`_rows_v825()`, `scripts/check-traceability.py`). 13 are reproducible, each backed by a deterministic offline gate (`scripts/check-traceability.py`'s HEADLINE-LOCK for HEADLINE-01..05 and SHIP-03, `scripts/check-quality-harness.py`'s QUAL-01 for CONTRACT-01..05, `scripts/check-version-stamps.py` for SHIP-01, `scripts/check-firewall-battery.sh` for SHIP-02); CONTRACT-06 is audit-only because nothing in the tree pins `_chain_block_well_formed` byte-unchanged — no gate re-runs to check that a byte-freeze claim holds (the v8.18 SHIP-04/SHIP-05 precedent). Two tiering calls were judgment calls, recorded rather than hidden: CONTRACT-06's tier (A1) and SHIP-03's tier (A2), both in `.planning/phases/12-integration-ship/12-RESEARCH.md` §A — each independently reversible without moving this row's total (266). |
| 11 | v8.26 Phase 13 (CHAINHEAD-07 / D-11) | 174/92/0/266 → 175/91/0/266 | **+1 reproducible / −1 audit-only, total unchanged at 266.** CONTRACT-06 was re-tiered `audit-only` → `reproducible` in `scripts/check-traceability.py` because `_selftest_chain_detector_pin` (`scripts/check-quality-harness.py`, added plan 13-03) now re-runs the byte-freeze claim that previously had no gate — closing the gap A1 (row 10 above) explicitly recorded as independently reversible. This reverses only the A1 judgment call; SHIP-03's tier (A2) is untouched. |
| 12 | v8.26 Phase 16 (SHIP-03) | 175/91/0/266 → 192/94/0/286 | **+17 reproducible / +3 audit-only.** The 20 v8.26 milestone requirements (CHAINHEAD-01..07, LEDGER-01..04, SCAN-01..04, SHIP-01..05) were registered as matrix rows for the first time (`_rows_v826()`, `scripts/check-traceability.py`). 17 are reproducible, each backed by a deterministic offline gate (`scripts/check-quality-harness.py`'s QUAL-01 for CHAINHEAD-01..06 and LEDGER-01..04, `scripts/check-quality-harness.py`'s CONTRACT-06 pin for CHAINHEAD-07, `scripts/check-selfaudit-scan.py`'s SCAN-GUARD for SCAN-01..03, `scripts/check-version-stamps.py` for SHIP-01, `scripts/check-firewall-battery.sh` for SHIP-02, and `scripts/check-traceability.py`'s own HEADLINE-LOCK sentinel for SHIP-03); SCAN-04, SHIP-04 and SHIP-05 are audit-only because no gate re-runs to check a validation-audit finding, a CHANGELOG entry, or a docs record (the v8.18 SHIP-04/SHIP-05 precedent). One tiering call was a judgment call, recorded rather than hidden: CHAINHEAD-07 is registered as its own v8.26 row distinct from the existing `v8.25/CONTRACT-06` row (A3) — independently reversible without moving this row's total (286). `_rows_v826()`'s docstring also discloses a boundary on SCAN-01..03's three anchors (`_check_body_text`, `_check_rubric_text`, `_check_cross_surface`): they are not dispatch-checked by `_resolve_artifact()`, which recognises only the `_selftest_*`/`_self_test_*` naming convention — the call-site census in `_self_test_v826_rows_sentinel()`'s block (h4) is what actually confirms those three are wired in, not `_resolve_artifact()`. |
| 13 | v9.0 Phase 23 (REL-03) | 192/94/0/286 → 208/97/0/305 | **+16 reproducible / +3 audit-only.** The 19 v9.0 milestone requirements (CONF-01..15, REL-01..04) were registered as matrix rows for the first time (`_rows_v9()`, `scripts/check-traceability.py`). 16 are reproducible: CONF-01/02/10 point at `scripts/report-conformance.py`; CONF-03/04/05/06 point at `scripts/check-conf-gate.py`; CONF-07 points at `scripts/check-firewall-battery.sh`; CONF-08/09 point at `scripts/report-conformance.py`; CONF-11/12/13 point at `scripts/gen-gate-docs.py`; REL-01 points at `scripts/check-version-stamps.py`; REL-02 points at `scripts/check-firewall-battery.sh`; REL-03 points at `scripts/check-traceability.py#_self_test_headline_lock`. CONF-14, CONF-15 and REL-04 are audit-only, named individually: CONF-14 and CONF-15 are `docs/PROCESS.md`/`CLAUDE.md` process and review-protocol prose — CLAUDE.md's own "Review protocol" section states plainly that no script, control or CI job enforces it; REL-04 is a `CHANGELOG.md` record, the v8.18/v8.24/v8.26 SHIP-04/05 precedent — no gate re-runs to check a CHANGELOG entry's prose content. `_rows_v9()`'s docstring discloses a DISCLOSED BOUNDARY carried into this row: of the 16 reproducible rows, only REL-03 carries a `#_self_test_*` anchor (`_self_test_headline_lock`) that `_resolve_artifact()` dispatch-checks; the other 15 carry a bare script path, because none of those five scripts (`report-conformance.py`, `check-conf-gate.py`, `check-firewall-battery.sh`, `gen-gate-docs.py`, `check-version-stamps.py`) defines a `_selftest_`/`_self_test_`-prefixed symbol — a bare path only proves the file exists, never that anything re-runs the claim; each script's own `--self-test`/`--check` CLI surface supplies that guarantee instead, exercised directly in this phase's own verification rather than by this matrix. |
| 14 | v9.1 Phase 27 (REL-07) | 208/97/0/305 → 217/106/0/323 | **+9 reproducible / +9 audit-only.** The 18 v9.1 milestone requirements (PROSE-01..04, CONTAIN-01..04, NARR-01..02, RATCHET-01..04, REL-05..08) were registered as matrix rows for the first time (`_rows_v91()`, `scripts/check-traceability.py`). 9 are reproducible: CONTAIN-01, CONTAIN-02, CONTAIN-04, NARR-02, RATCHET-01 and RATCHET-02 point at `scripts/gen-gate-docs.py` (`--check` re-runs their claims as pre-commit gate 5 and in CI); REL-05 points at `scripts/check-version-stamps.py`; REL-06 points at `scripts/check-firewall-battery.sh`; REL-07 points at `scripts/check-traceability.py#_self_test_headline_lock`. All 9 audit-only rows are named individually, transcribed from `_rows_v91()`'s own docstring: PROSE-01 — whether a mechanism is named in writing is not a predicate any gate evaluates; PROSE-02 — whether a sibling site was located before a fix was written is a fact about ordering in history, which no re-run can establish; PROSE-03 — a written scope exclusion, no gate reads it; PROSE-04 — a recorded disposition per finding, the v8.18/v8.24/v8.26 SHIP-04/05 and v9.0 REL-04 precedent for prose records; CONTAIN-03 — a written REACH-or-LEVEL determination, the argument is the deliverable and no gate reads arguments; NARR-01 — the generalized rule is process prose, the CONF-14/CONF-15 precedent; RATCHET-03 — discharged by a recorded DROP verdict, not by a shipped mechanism, so there is nothing to re-run; RATCHET-04 — dated written determinations, same character as CONTAIN-03; REL-08 — no gate re-runs to check a CHANGELOG entry's prose content, the REL-04 precedent. `_rows_v91()`'s docstring discloses a DISCLOSED BOUNDARY carried into this row: of the 9 reproducible rows, only REL-07 carries a `#_self_test_*` anchor (`_self_test_headline_lock`) that `_resolve_artifact()` dispatch-checks; the other 8 carry a bare script path, because none of `scripts/gen-gate-docs.py`, `scripts/check-version-stamps.py` or `scripts/check-firewall-battery.sh` defines a `_selftest_`/`_self_test_`-prefixed symbol — a bare path only proves the file exists, never that anything re-runs the claim; each script's own `--self-test`/`--check`/live-battery CLI surface supplies that guarantee instead, exercised directly in this phase's own verification rather than by this matrix. |
| 15 | v9.2 Phase 28 (REL-12) | 217/106/0/323 → 225/110/0/335 | **+8 reproducible / +4 audit-only.** The 12 v9.2 milestone requirements (SUP-01..04, GUARD-01..03, REL-09..13) were registered as matrix rows for the first time (`_rows_v92()`, `scripts/check-traceability.py`). 8 are reproducible: SUP-01 points at `scripts/check-loop-closure.py` (HARN-02's presence/absence literals on Input Contract bullet 4 re-run the claim on every CI run and battery pass); SUP-03 and SUP-04 point at `scripts/check-focused-parity.py` (Stub-13 re-runs the candidate-input tail's presence in each unclassified-facts stub, the no-cited-source clause's presence in every non-launcher stub, and the slot name's absence from every stub); GUARD-01 points at `scripts/check-loop-closure.py` (controls N38/N39 re-run in every `--self-test`); GUARD-02 points at `scripts/check-focused-parity.py` (controls g6/g7 re-run in every `--self-test`); REL-09 points at `scripts/check-version-stamps.py`; REL-10 points at `scripts/check-firewall-battery.sh`; REL-12 points at `scripts/check-traceability.py#_self_test_headline_lock`. All 4 audit-only rows are named individually, transcribed from `_rows_v92()`'s own docstring: SUP-02 — whether the bullet points at Phase 3's rule rather than restating the provenance table is a reading judgement, HARN-02's literal pins the candidate clause, not the label pointer or the absence of a restatement; GUARD-03 — a written REACH-or-LEVEL determination, the argument is the deliverable and no gate reads arguments (precedent: v9.1 CONTAIN-03); REL-11 — no gate re-runs to check a CHANGELOG entry's prose (precedent: REL-08, REL-04); REL-13 — the recurrence reading is a one-off grep recorded in the `[9.2.0]` entry, no gate re-runs the pre-registered pattern set over both trees, and HARN-02's/HARN-03's absence pins re-run two of its shapes on their own files only, which is not the requirement. `_rows_v92()`'s docstring discloses a DISCLOSED BOUNDARY carried into this row: of the 8 reproducible rows, only REL-12 carries a `#_self_test_*` anchor (`_self_test_headline_lock`) that `_resolve_artifact()` dispatch-checks; the other 7 carry a bare script or directory path, because none defines a `_selftest_`/`_self_test_`-prefixed symbol — a bare path only proves the file/directory exists, never that anything re-runs the claim; each script's own `--self-test` CLI surface supplies that guarantee instead, exercised directly in this phase's own verification rather than by this matrix. (Superseded at v9.3.0 Phase 34 / ANCH-01: GUARD-01 now also carries a `#_self_test_*` anchor, `#_self_test_guard01_bullet4_anchor`, whose block runs control N38 only, not N38/N39; SUP-01 was anchored in the same phase and returned to a bare path at the Phase 34 code review, WR-04; `check-loop-closure.py` now defines `_self_test_*` symbols. `_rows_v92()`'s docstring carries the updated reading, so this row no longer matches it verbatim — see the Self-test anchor work list below.) |
| 16 | v9.2.1 Phase 31 (REL-17) | 225/110/0/335 → 229/116/0/345 | **+4 reproducible / +6 audit-only.** The 10 v9.2.1 milestone requirements (HAND-01..05, REL-14..18) were registered as matrix rows for the first time (`_rows_v921()`, `scripts/check-traceability.py`). 4 are reproducible: HAND-04 points at `scripts/check-focused-parity.py` (Stub-13 asserts each of the ten unclassified-facts stubs carries the v9.2.0 tail literal exactly once, matched whitespace-flexibly by `_count_flex`; byte-identity against v9.2.0 was established by a one-off `sha256sum` comparison, not by this gate); HAND-05 points at `scripts/check-loop-closure.py` (the four-edge-present/five-edge-absent literals re-run in every `--self-test`); REL-14 points at `scripts/check-version-stamps.py`; REL-17 points at `scripts/check-traceability.py#_self_test_headline_lock`. All 6 audit-only rows are named individually, transcribed from `_rows_v921()`'s own docstring: HAND-01, HAND-02 and HAND-03 — each row's deliverable is one routed stub's own routing destination (`identify-essence` → the Input Contract's Problem statement, `reason-upward` → Phase 5 validation, `validate` → the Phase 5 verdict to act on), and nothing re-runs that claim: `check-focused-parity.py`'s Stub-13 loop reads `_HANDOFF_ROUTED_SLUGS` at exactly one check site, to EXCLUDE the three routed slugs from the `_HANDOFF_CANDIDATE_TAIL` assertion, and the only literal it pins on those stubs is the universal `_HANDOFF_NO_SOURCE_CLAUSE`, which names no destination — falsified at the Phase 31 review by deleting a destination clause from both trees and observing `--self-test` and the live leg both still at exit 0 (tracked as backlog 999.79/999.80; re-tier when a per-routed-stub destination literal lands). These three were published as `reproducible` when the milestone closed and were corrected here at the Phase 31 review (CR-01), which is why this row's delta reads +4/+6 rather than the +7/+3 first recorded; REL-15 — its own requirement text names the battery's GREEN line "corroboration only, never the evidence", so the live tally is a fresh count on every run, not a comparison against a stored prior baseline, and nothing fails automatically if the total drifts; the "unchanged since last release" half of the claim is discharged by a manual direct-count snippet against two named revisions, not by a registered CI/battery control; REL-16 — no gate re-runs to check a CHANGELOG entry's prose (precedent: REL-13, REL-11, REL-08, REL-04); REL-18 — the recurrence reading is a one-off pre-registered grep set read before and after the release commit and recorded in the `[9.2.1]` entry, no gate re-runs the pattern set over both trees (the REL-13 precedent holds unchanged). `_rows_v921()`'s docstring discloses a DISCLOSED BOUNDARY carried into this row: of the 4 reproducible rows, only REL-17 carries a `#_self_test_*` anchor (`_self_test_headline_lock`) that `_resolve_artifact()` dispatch-checks; the other 3 carry a bare script or directory path, because none defines a `_selftest_`/`_self_test_`-prefixed symbol — a bare path only proves the file/directory exists, never that anything re-runs the claim; each script's own `--self-test` CLI surface supplies that guarantee instead, exercised directly in this phase's own verification rather than by this matrix. (Superseded at v9.3.0 Phase 34 / ANCH-01: HAND-05 now also carries a `#_self_test_*` anchor, `#_self_test_hand05_no_new_edge`; `check-loop-closure.py` now defines `_self_test_*` symbols. `_rows_v921()`'s docstring carries the updated reading, so this row no longer matches it verbatim — see the Self-test anchor work list below.) |
| 17 | v9.3.0 Phase 33 (ROWS-01, RESID-01) | 229/116/0/345 → 246/125/0/371 | **+17 reproducible / +9 audit-only.** The v8.19 (HC-01..04), v8.20 (HARN-01-01..05) and v8.21 (v8.21/REG-01..06, v8.21/GATE-01..06, v8.21/VAL-01..03) milestone requirements, plus residuals RR-108-04 and RR-108-05, were registered as matrix rows for the first time (`_rows_v819()`, `_rows_v820()`, `_rows_v821()`, `_rows_active_tail()`, `scripts/check-traceability.py`), in one headline move. v8.19: HC-01, HC-02 and HC-03 are reproducible, each backed by `scripts/check-high-confidence-bound.py`; HC-04 is audit-only — the gate re-runs its tightened-criteria clause but not the stale "FIREWALL: GREEN (21/21)" count it quotes. v8.20: HARN-01-02, HARN-01-03 and HARN-01-05 are reproducible, each backed by `scripts/check-act-limb.py`'s anti-masking coverage floor; HARN-01-01 and HARN-01-04 are audit-only — the gate re-runs the branch coverage `check-act-limb.py --describe` reports but nothing re-reads the named branch-specification or comment-block prose. v8.21: v8.21/REG-01, v8.21/REG-02, v8.21/REG-03, v8.21/GATE-02 and v8.21/GATE-03 are reproducible at `scripts/check-registration.py` (v8.21/GATE-03 by its own `#verify_ci_job_registration` anchor); v8.21/GATE-04 and v8.21/GATE-05 are reproducible at `scripts/gen-gate-docs.py` (re-pointed from REG-GUARD per the D-01 re-pointing rule); v8.21/VAL-02 is reproducible at `scripts/check-version-stamps.py`; v8.21/VAL-03 is reproducible at `scripts/sync-content.py`. v8.21/REG-04 and v8.21/REG-05 are audit-only — their "registered in manifest" clause is K4, the shipped manifest carries no name/type roster to check against; v8.21/REG-06 is audit-only — a clause-scoped break of its "registered entries vs. discovered entries" summary left `scripts/check-registration.py` green (re-tiered by the Phase 33 code review, CR-01, from the reproducible tier first published in this row); v8.21/GATE-01 is audit-only — its "runs deterministically" clause is K4, stated but never re-run; v8.21/GATE-06 and v8.21/VAL-01 are audit-only — their quoted battery counts ("22/22") are stale against the battery's current total (CLAUDE.md's generated population-arithmetic sentence). RR-108-04 and RR-108-05 are reproducible at `scripts/_battery_core.py#self_test_boundary`, both ACCEPTED-FINAL at v8.0, re-measured at v8.5 and sustained at the 0/5 floor via `_NEW_TECH_SENTINELS` (Phase 156 re-point to `_load_excerpt_v85`). Every tier here rests on a break test run once at Phase 33, recorded in `.planning/phases/33-row-less-milestones-and-residuals/33-BREAK-TESTS.md` (local-only, git-ignored; not present in a fresh clone), under the rule that a tier stands only if a clause-scoped break turns the cited gate red. DISCLOSED BOUNDARY: only v8.21/GATE-03 carries a symbol anchor (`#verify_ci_job_registration`, non-prefixed); no row in this batch carries a `#_self_test_*` anchor. (Superseded at v9.3.0 Phase 34 / ANCH-01: v8.21/REG-01, v8.21/REG-02 and v8.21/REG-03 now carry `#_self_test_*` anchors — `#_self_test_reg01_discover_skills`, `#_self_test_reg02_discover_agent` and `#_self_test_reg03_parse_manifest` — see the Self-test anchor work list below.) |
| 18 | v9.3.0 Phase 34 (TIER-02) | 246/125/0/371 → 242/129/0/371 | **-4 reproducible / +4 audit-only.** The four test_69 rows (v4.2/BASE-01, v4.2/BASE-02, v4.3/BATT-07, v4.3/BATT-08) were re-tiered audit-only after a Phase 34 break test (34-BREAK-TESTS.md, standing instruction 7): mutating `tests/routing-battery-baseline-v4.3.md`'s BATTERY verdict line, and separately its lineage commit hash, left every registered gate green except FROZEN-EVIDENCE, which is excluded as the pin because its `git diff --quiet HEAD` check catches only an uncommitted edit and a committed edit to the same file passes clean; only the local, unregistered `tests/test_69_merged_baseline_invariants.py` pytest module (no battery registration, no CI job) detected either change. No battery registration or CI job was added (standing D-D). The eight v3.7 RIGOR rows (RIGOR-01..08) stay reproducible: five are re-pointed at the registered gate whose break test broke it red (RIGOR-03/RIGOR-05 at HC-BOUND, RIGOR-04/RIGOR-07 at SCAN-GUARD, RIGOR-06 at QUAL-01, battery-only), and the remaining three (RIGOR-01, RIGOR-02, RIGOR-08) are kept at their rubric anchor with a written reason — no registered gate transcribes a literal from those sections, so TRACE-03's own heading-presence check is the only re-read. Row count and tier for the RIGOR batch are unchanged; only their `artifact_link` and `gap_rationale` moved. (Superseded at the Phase 34 code review, WR-02: RIGOR-01, RIGOR-02 and RIGOR-08 were re-tiered audit-only — see row 19.) |
| 19 | v9.3.0 Phase 34 code review (TIER-01, WR-02) | 242/129/0/371 → 239/132/0/371 | **-3 reproducible / +3 audit-only.** RIGOR-01 (Criterion 1: Identify Essence), RIGOR-02 (Criterion 2: Challenge Assumptions) and RIGOR-08 (Scoring Model) were re-tiered audit-only with an empty `artifact_link` and `rerun_by="none"`. Row 18 had kept them reproducible at their rubric heading anchors, `ci` via TRACE-03, but that check re-reads only that each heading is present: deleting a whole section body leaves CI green, and no registered gate transcribes any sentence of the three sections. That is a looser bar than the one row 18 applied to the test_69 rows, whose break was at least caught by an unregistered pytest module, so one rule now holds for both batches — a row is reproducible only if a registered gate goes red when its content breaks. The now-uncited `validation-rubric.md` → TRACE-03 entry was removed from `_RERUN_CI_VIA` (`scripts/check-traceability.py`), since that map requires every key to be cited by a `ci` row. Row count unchanged at 371. |
| 20 | v9.3.0 Phase 35 (REL-20) | 239/132/0/371 → 244/151/0/395 | **+5 reproducible / +19 audit-only.** The 24 v9.3.0 milestone requirements (READ-01, SCHEMA-01/02, STMT-01/02, ROWS-01..05, RESID-01/02, TIER-01..04, ANCH-01/02, REL-19..REL-24) were registered as matrix rows for the first time (`_rows_v93()`, `scripts/check-traceability.py`), each tier resting on a fresh, clause-scoped break test run once against this phase's own tree (local-only, git-ignored break-test record; not present in a fresh clone). 5 are reproducible: SCHEMA-01 and STMT-01 at `scripts/check-traceability.py#_self_test_row_fields_live` (field presence, lockstep population and JSON emission all break red); SCHEMA-02 at `scripts/check-traceability.py#_self_test_headline_lock` (per-skill count and Uncovered list are Markdown/JSON-freshness-checked); TIER-03 at `scripts/check-traceability.py#_row_field_problems` (a live/manual artifact mislabeled `ci` breaks the D-03 registry check red); ANCH-01 at `scripts/check-traceability.py#_resolve_artifact` (the dispatch-checked-anchor claim). 19 are audit-only, each named with its own unchecked clause: READ-01 (reads the unregistered `rederive.py` instrument); ROWS-01 (the docstring tier-justification clause); ROWS-02 (a gitignored `.planning/milestones/` deliverable); ROWS-03 ("every gate is cited" — de-registering a gate's only citing rows stays green); ROWS-04 (milestone-qualification of prose citations); ROWS-05 (the milestone-naming clause and its now-unreachable Exit reading); RESID-01 (the free-text reading-description clause); RESID-02 (a written decision no gate scans for); STMT-02 (archive-fidelity — a fabricated archive-sourced statement stays green); TIER-01 (a re-point's content-correctness, and a kept row's non-empty reason); TIER-02 (tier-correctness and decision-recording for the test_69 batch); TIER-04 (the QUAL-01 cost/determinism measurement's own recording); ANCH-02 (no gate's subject is "did a scripts/ rename move a shared/ literal"); REL-19 (the specific value `9.3.0` — a uniform wrong value stays green everywhere); **REL-20 (the headline-history-row clause — deleting row 20 itself, whole, leaves `check-traceability.py --self-test` green; the only one of the six originally-drafted-reproducible rows whose own break stayed green, so it re-tiers audit-only inside this same commit, one headline move per D-07)**; REL-21 (the "unchanged from `fda29cc`" half of the battery/CI claim); REL-22 (CHANGELOG prose); REL-23 (a local-only recurrence reading); REL-24 (only presence is checked, obedience deferred to backlog 999.89). DISCLOSED BOUNDARY: of the 5 reproducible rows, SCHEMA-01, SCHEMA-02 and STMT-01 carry a dispatch-checked `#_self_test_*` anchor; TIER-03 and ANCH-01 carry a same-file function-name anchor that `_resolve_artifact()` confirms is defined but does not dispatch-check for a calling dispatcher. No new `-ROWS` sentinel: LEVEL determination (citing backlog 999.83, 999.85 and the Phase 33 precedent for the v8.19/v8.20/v8.21 batch) — `_rows_v93()` is re-run by TRACE-03's existing ROW-FIELDS live leg and by HEADLINE-LOCK, with the named residual that a tier swap between two `v9.3` rows holding the tier counts constant, or a statement edit `emit` then regenerates, passes both. Row count 371 → 395. |

> **Honesty note (v8.8 D-01 — RESOLVED):** the prior "known-stale / vacuously-green" flag on
> META-Q4 (TRACE-03 reporting coverage that no longer existed — "green because nothing checks it")
> is now **fixed at the source**, not just annotated: row 6 of the change log above makes the matrix
> state honest rather than qualified-and-flagged. The two same-class stale hook surfaces bundled with
> it (`scripts/smoke-test-hook.sh` retired, `scripts/install-hooks.sh:57` reworded) were cleared in
> the same cleanup. This closes the "finish TEARDOWN-01 cleanup" unit
> (`.planning/todos/pending/phase-167-stale-surfaces-from-163-review.md`).

> **Pre-existing drift corrected (quick task `260728-wdi`):** the bold audit-only-rows count heading
> further down this file was a pre-existing off-by-one against the headline, dating to the v8.8
> META-Q4 re-tier which moved the headline to 97 without updating that section's own count, and was
> deliberately left uncorrected by the prior quick task (`260728-vxn`) pending a separate doc-hygiene
> pass — recorded as a known, visible drift rather than silently absorbed. Quick task `260728-wdi`
> is that pass. **The rest of this note is dated history, not a live claim:** as of 2026-07-28
> the heading was corrected to agree with the then-current `126/88/0/214` headline and with
> `docs/data/matrix.json` as generated at that date. The headline has since moved again — to
> `147/90/0/237` at v8.18 Phase 4, recorded as headline-history row 8 above — and the heading
> moved with it; both now read 90. The headline moved again at v8.24 Phase 6 to `161/91/0/252`
> (headline-history row 9 above), and the audit-only-rows heading moved with it; both now read 91.
> The headline moved again at v8.25 Phase 12 to `174/92/0/266` (headline-history row 10 above),
> and the audit-only-rows heading moved with it; both now read 92.
> The headline moved again at v8.26 Phase 13 to `175/91/0/266` (headline-history row 11 above),
> and the audit-only-rows heading moved with it; both now read 91.
> The headline moved again at v8.26 Phase 16 (SHIP-03) to `192/94/0/286` (headline-history
> row 12 above), and the audit-only-rows heading moved with it; both now read 94.
> The headline moved again at v9.0 Phase 23 (REL-03) to `208/97/0/305` (headline-history row 13
> below), and the audit-only-rows heading moved with it; both now read 97.
> The headline moved again at v9.1 Phase 27 (REL-07) to `217/106/0/323` (headline-history row 14 above), and the audit-only-rows heading moved with it; both now read 106.
> The headline moved again at v9.2 Phase 28 (REL-12) to `225/110/0/335` (headline-history row 15 above), and the audit-only-rows heading moved with it; both now read 110.
> The headline moved again at v9.2.1 Phase 31 (REL-17) to `229/116/0/345` (headline-history row 16 above), and the audit-only-rows heading moved with it; both now read 116.
> **Correction and end of this chain, dated 2026-09-13 (v9.3.0 Phase 33):** the trailer above
> states that the honesty-note count and the audit-only-rows heading were moved at v9.2.1 Phase
> 31; both still read that phase's pre-CR-01 figure after the CR-01 re-tier moved the headline —
> the class this note tracks, recurring. From Phase 33 neither site carries a count; both point
> at the coverage headline HEADLINE-LOCK pins (headline-history row 17 above), so no further
> trailer is added here. The same class survived at a sixth site this sweep missed, GAP-02's
> MEDIUM/HIGH audit-only sub-counts below (found by the Phase 33 code review, WR-02); it too
> now carries no count.

## v8.0 Terminal State (2026-07-06)

**Project wrapped.** Phase 142 (Final Dispositions & Terminal Closure) is the terminal phase.
No forward-committed successors. No live re-measure.

Three Step 0 residuals are recorded **ACCEPTED-FINAL** (user decision at v8.0 milestone init;
honesty-not-score, D-01 global):

| Residual | True K/N | BATT-06 Sentinel | Disposition |
|----------|----------|-----------------|-------------|
| RR-114-01 (S-P02 inversion) | 1/5 live (v7.13) | `_load_excerpt_v713` in `_battery_core.self_test_boundary()` | ACCEPTED-FINAL |
| RR-108-04 (S-P10 estimate) | 0/5 live (v7.13) | `_load_excerpt_v713` in `_battery_core.self_test_boundary()` | ACCEPTED-FINAL |
| RR-108-05 (S-P14 theoretical-limit) | 0/5 live (v7.13) | `_load_excerpt_v713` in `_battery_core.self_test_boundary()` | ACCEPTED-FINAL |

BATT-06 sentinels retained as regression guards; no successor minted; no further live re-measure.
All remaining forward-committed live re-measures across the active surface (including the RR-108-02 trade-off emission re-measure) are terminally accepted as not-to-be-run: the v7.13 live baselines are the final measured state (OFFLINE-ONLY, honesty-not-score, D-01).
See [`v8.0-final-closure.md`](v8.0-final-closure.md) for the durable terminal record.

### v8.5 Live Re-Measure Annotation (2026-07-20)

v8.5 (Context Optimization — Execute the Reference-File Split) executed the 4-file reference
split and narrowly relaxed the v8.0 "no further live re-measure" disposition for exactly
RR-108-04 and RR-108-05 (governing record: v8.5-byte-freeze-relaxation.md). It then ran a
72-call live re-measure and re-pointed four BATT-06 sentinels to the v8.5 captures via the new
`_load_excerpt_v85` helper reading tests/step0-captures-v8.5/ (honest verdict:
v8.5-live-remeasure-verdict.md §1). No matrix row was added or removed, so the coverage headline
stays byte-identical at 133/96/0/229 — this annotation records the measured outcome only, per
honesty-not-score (D-01):

| Residual | Split status | v8.5 K/N | Disposition |
|----------|--------------|----------|-------------|
| RR-108-04 (S-P10 estimate) | SPLIT (Phase 154) | 0/5 | CARRY — SUSTAINED at floor (re-opened + re-measured, landed exactly on prior 0/5 floor) |
| RR-108-05 (S-P14 theoretical-limit) | SPLIT (Phase 154) | 0/5 | CARRY — SUSTAINED at floor (re-opened + re-measured, landed exactly on prior 0/5 floor) |
| RR-114-01 (S-P02 inversion) | UNSPLIT CONTROL | 0/5 | CARRY (was 1/5 v7.13; −1) |
| RR-117-01 (S-P03 fishbone) | SPLIT (Phase 154) | 3/5 | CLOSE SUSTAINED (≥ 3/5; sentinel retained as regression guard) |

No row improved. The IDs are kept in every case — no successor minted. Detector constants
(pre-mortem 9, fishbone 7, inversion 13, trade-off 10), MIN_HEADER_HITS, and
_COMPOSER_FOCUS_CEILING stayed byte-unchanged and gating through the split.

### v8.6 Live Re-Measure Annotation (2026-07-21)

v8.6 (Agent-Body Procedure Compression) compressed the agent body's inlined `## Procedure`
prose for four techniques and ran a small 2-row live Step-0 re-measure, re-pointing RR-117-01
to the new `_load_excerpt_v86` helper reading tests/step0-captures-v8.6/ (honest verdict:
v8.6-live-remeasure-verdict.md section 1). No matrix row was added or removed, so the coverage
headline stays byte-identical at 133/96/0/229 — this annotation records the measured outcome
only (honesty-not-score, D-01).

| Residual | Split status | v8.6 K/N | Disposition |
|----------|--------------|----------|-------------|
| RR-117-01 (S-P03 fishbone) | marker-pinned (Phase 159) | 4/5 | SUSTAINED (+1 vs v8.5 3/5 floor; sentinel re-pointed to `_load_excerpt_v86`, vector [2,2,2,3,4]; DEC-02 CLOSE, retained as regression guard) |
| S-P04 (five-whys) | marker-pinned (Phase 159) | 2/5 | SUSTAINED (+2 vs v8.5 0/5 floor; observed but NOT banked — no BATT-06 sentinel exists or is minted; single 5-run sample, documented run-to-run variance 2/5 v7.11 to 0/5 v8.5 to 2/5 v8.6) |

Both rows measured this cycle landed at or above their own frozen floor; no row regressed (the
inverse of v8.5's "no row improved"); the IDs are kept; no successor minted; detector constants
(pre-mortem 9, fishbone 7, inversion 13, trade-off 10), MIN_HEADER_HITS, and
_COMPOSER_FOCUS_CEILING stayed byte-unchanged and gating.

> **S-P04 decision, dated 2026-09-13 (v9.3.0 Phase 33 / RESID-02):** S-P04 (five-whys) stays
> observed-but-unbanked, with no RR ID, no BATT-06 sentinel and no matrix row. The governing record
> is `docs/v8.7-constraint-teardown.md` §2 item 3: "K-of-5 Step 0 results are recorded observations from here forward; they may not gate a phase." The swing that record cites as its evidence is
> S-P04's own reading across v7.11, v8.5 and v8.6 (2/5 → 0/5 → 2/5), as the table row above records.
> `docs/v8.6-live-remeasure-verdict.md` §3 already recorded the gain as observed but not banked.
> Minting an RR ID would add a BATT-06 assertion over existing captures and lock a single 5-run
> sample in as an expectation; that would change what BATT-06 asserts, and nothing since v8.6
> supplies a reason to. The Phase 33 residual reading (`.planning/phases/999.93-shipped-milestones-requirements-have-no-matrix-row-undisclos/trace-atlas/rederive.py residuals`, a local-only planning tool, git-ignored and not present in a fresh clone) does not list S-P04 because it was never recorded
> ACCEPTED-FINAL — this decision is its disposition.

### v8.13 DETECT-03 Accepted Limitation (2026-07-27)

v8.13 (DETECTFIX-01) Phase 184 corrected `_chain_block_well_formed` in
`scripts/check-quality-harness.py`. **ROADMAP criterion 3 — "the looser block matcher does not
become a blanket pass, proven by an explicit negative fixture" — is recorded ACCEPTED LIMITATION
(user decision, 2026-07-27; honesty-not-score, D-01 global; in-source statement at
`_segment_sentence_closed`, D-21).**

The criterion is an **unbounded negative verified by a finite fixture table**. Finite examples
cannot discharge a universal claim. Four rounds each closed the shape then known and each was
defeated by a shape outside the table, with every CI gate green throughout — the gates assert only
the table:

| Round | Refusal rule added | How it was evaded | Verdict |
|-------|-------------------|-------------------|---------|
| 184-01/02 | (none — unbounded join) | any GT + two arrows fused | gaps_found 5/6 |
| 184-03 | line-break **position** | move the first arrow to the next line | gaps_found 2/6 (also regressed 4 other criteria below base `1f71211`) |
| 184-04/05 | sentence-ending **punctuation** | put a markdown closer after the punctuation (CR-01) | gaps_found 5/6 |
| 184-06 | normalise (mask GT tokens, strip markdown closers) **then** test | — not probed further, by decision | ACCEPTED |

**What IS closed and pinned:** the three shapes found across the four rounds, plus the two
directions of the 184-06 root cause. `C-JOIN-ARROW-BOLDCLOSE` (over-acceptance) and
`C-WRAP-GT-QMARK` (under-acceptance) are each proven load-bearing by their own fault injection
(INJ-7, INJ-8) under both `python3` and `python3 -O`. `_CALIBRATION_MALFORMED_CHAIN_BLOCKS`
`[2, 2, 2, 2, 3, 3]` is asserted by `_selftest_defects`, so a movement in that column is a gate
failure rather than a comment edit.

**What is NOT closed:** the class. Closing it would require a **generator** — property-based
testing over a grammar of renderings (bold × backtick × blockquote × list × table × order mark ×
arrow position × sentence closer) — not more fixtures. That is deliberately not built; no successor
phase is minted for it. Both defects fixed in 184-06 were found by *code review probing past the
fixture table*, never by a gate.

**Standing caveat for any future reader:** treat a green chain axis as "no KNOWN shape regresses",
never as "no shape passes". DETECT-03 is marked complete on this basis and on no stronger one.

## Active Surface

Exactly 12 live items (v7.13: RR-130-01 RESOLVED/CLOSE at Phase 136 live re-measure — P 11/13 = v3.13 anchor recovery, ID kept as regression sentinel, row-less per v7.9 D-02 precedent). Nothing shipped or superseded belongs here. **[v8.0 terminal note]** Phase 142 is the terminal phase — all 12 items are dispositioned; RR-114-01/RR-108-04/RR-108-05 are ACCEPTED-FINAL per the v8.0 Terminal State block above.

1. **RR-79-01** [HIGH] — S-P01 pre-mortem. **CLOSED at Phase 117 v7.7 CONF-01** (S-P01 3/5 ≥ min-pass; FIX-01 detector recalibration confirmed out-of-sample). **CLOSE SUSTAINED at Phase 119 v7.8 CONF-03** (S-P01 3/5 = v7.4 floor). ID retained; sentinel re-pointed to v7.8 live captures, vector [1,2,3,0,2], retained as regression guard. Confirmed by BATT-06 (RR-79-01 sentinel in `_battery_core.self_test_boundary()`).

2. **RR-114-01** [HIGH] — S-P02 inversion (Phase 114, supersedes RR-108-01, supersedes RR-95-01, supersedes RR-92-01, supersedes RR-79-02; full chain: RR-79-02 -> RR-92-01 -> RR-95-01 -> RR-108-01 -> RR-114-01). 1/5 FAIL at Phase 114 v7.6 re-baseline (no change vs v7.4 1/5; below min-pass 3/5). **RESOLVED-STRUCTURALLY-OFFLINE Phase 121 OCH-02**: the detector now reads the heading-anchored output-contract headers (inversion extended 9→13 by adding ## Inverted Claim / ## Failure-Guaranteeing Conditions / ## Necessary Preconditions / ## Stress-Test Verdict); the frozen v7.6 vector [2,0,1,1,1] is UNCHANGED (captures predate the headers); the live S-P02 pass-rate re-measure is the forward-committed half (honesty-not-score, D-01). ID kept; no successor minted. Confirmed by BATT-06 (RR-114-01 sentinel in `_battery_core.self_test_boundary()`).
   **[v8.0 ACCEPTED-FINAL]** True K/N: 1/5 (v7.13 live). No successor minted; no live re-measure. BATT-06 sentinel retained (`_load_excerpt_v713`). Terminal disposition — project wrapped.

3. **RR-108-02** [HIGH] — S-P05 trade-off (Phase 108, supersedes RR-95-02, supersedes RR-92-02, supersedes RR-79-03; full chain: RR-79-03 -> RR-92-02 -> RR-95-02 -> RR-108-02 CLOSED). **CLOSED at 4/5 ≥ min-pass at Phase 114 v7.6 re-baseline** (the lone canonical improver; S-P05 trade-off cleared min-pass). **Structurally extended Phase 121 OCH-02**: trade-off extended 6→10 by adding 4 heading-anchored output-contract markers (## Options / ## Criteria & Weights / ## Scoring / ## Recommendation); frozen v7.6 vector [2,2,2,2,1] UNCHANGED (captures predate the headers); live trade-off emission re-measure forward-committed (honesty-not-score, D-01). ID retained; sentinel re-pointed to v7.6 count vector [2,2,2,2,1] and remains present as a regression guard.

4. **RR-77-08** [MEDIUM] — CEILING=4 vs expected=3 warning: incidental `\bVerdict\b` IGNORECASE match in `composer_hits`; not a blocking defect but unresolved. Locked by BATT-06 anti-masking sentinel (CEILING=4) in `_battery_core.self_test_boundary()`. **[v8.0 terminal]** Accepted as permanently locked by the BATT-06 CEILING=4 sentinel; no further resolution planned — project wrapped.

5. **GEN-01** [reproducible] — Full Step 0 classifier rearchitecture (GEN-01-REARCH, Phases 91-93). GEN-01 is now reproducible: the Step 0 classifier capability is reproducibly measured by the committed baselines — v7.6 (Phase 114), v7.7 CONF-01 (Phase 117), v7.8 CONF-03 (Phase 119), and the v7.11 whole-system live re-baseline (Phase 129). Latest artifact: `tests/step0-baseline-v7.13.md` (bumped Phase 138 RECON Plan 03, paired data + gate-code edit D-05; v7.8 remains the canonical full 8-technique baseline; v7.13 is a 3-row residual-delta re-measure). Reproducible = measured, not passing. Phase 129 v7.11 verdict: BATTERY: FAIL, P 4/8 (S-P01 5/5, S-P03 4/5, S-P05 5/5, S-P06 4/5 PASS; S-P02 2/5, S-P04 2/5, S-P10 0/5, S-P14 0/5 FAIL) — honest measured state (honesty-not-score, D-01). Phase 137 v7.13 residual-delta: S-P02 inversion 1/5 CARRIED (RR-114-01), S-P10 estimate 0/5 CARRIED (RR-108-04), S-P14 theoretical-limit 0/5 CARRIED (RR-108-05) — all three **[v8.0 ACCEPTED-FINAL]** per the v8.0 Terminal State block above. No open gap (the tier reflects reproducible measurement, not a passing score).

6. **GEN-02** [reproducible] — Periodic live monitoring cadence; runbook + wrapper script established (Phase 89). Confirmed by git-tracked runbook and wrapper; artifact: `docs/live-monitoring-runbook.md`. No longer an open gap.

7. **RR-80-01** [CRITICAL] — S-N04 semantically-pre-mortem over-routing. CLOSED 4/5 at Phase 95 re-baseline (v6.4). At v7.4: S-N04 2/5 (regression). At v7.6: S-N04 3/5 PASS. At Phase 117 v7.7 CONF-01: S-N04 2/5, NON_BLOCKING (D-16 — genuine pre-mortem routing on semantically-pre-mortem prompt). At Phase 119 v7.8 CONF-03: S-N04 5/5 non-blocking (Phase-118 prose fix moved over bar; run5 is_error anomaly, count=0). Sentinel re-pointed to v7.8 vector [1,1,1,1,0].
   **Lineage:** Formerly tracked as S-N04 (placeholder `RR-75-NN`). Assigned RR-80-01 in Phase 83 (D-05).
   Confirmed by STEP0-08 (S-N04 emulator assertion in `check-step0-emulator.py --self-test`) and BATT-06 (marker-counting assertion in `_battery_core.self_test_boundary()`).

8. **RR-117-01** [HIGH] — S-P03 fishbone. **CLOSED at Phase 117 v7.7 CONF-01** (S-P03 5/5; FIX-01 detector recalibration confirmed out-of-sample). **CLOSE SUSTAINED at Phase 119 v7.8 CONF-03** (S-P03 4/5 ≥ v7.4 floor 3/5; D-1b softening). First fishbone vector sentinel; RR-75-03 lineage. Sentinel re-pointed to v7.8 vector [1,4,2,2,3] + fishbone drift guard == 7. ID retained; retained as regression guard. Confirmed by BATT-06 (RR-117-01 sentinel in `_battery_core.self_test_boundary()`).

9. **RR-117-02** [MEDIUM] — S-N03 precision (Phase 117 CONF-02; re-pointed to v7.8 Phase 119 CONF-04). The one truly-oblique negative: debugging prompt with no pre-mortem framing. Proves FIX-01+FIX-03/FIX-04 did NOT hurt routing on genuinely-oblique prompts (5/5 full-composer at v7.8). Sentinel re-pointed to v7.8 vector [1,0,0,0,0] (all runs stay below MIN_HEADER_HITS). Confirmed by BATT-06 (RR-117-02 sentinel in `_battery_core.self_test_boundary()`). D-17 precision finding sustained.

10. **RR-119-01** [MEDIUM] — S-N01 over-routing, resolved-over-bar (Phase 119 CONF-04, minted). At v7.7: S-N01 0/5 (all-over-route). At v7.8 CONF-03: S-N01 3/5 PASS (Phase-118 FIX-03/FIX-04 prose fix moved over bar). Residual disposition: RESOLVED-OVER-BAR with detector-under-count caveat (negative passes are a MIX of genuine clarification-holds and under-counts; D-01). NOT a reclassification (D-4). Sentinel asserts v7.8 vector [0,2,1,1,3]. Confirmed by BATT-06 (RR-119-01 sentinel in `_battery_core.self_test_boundary()`).

11. **RR-119-02** [MEDIUM] — S-N02 over-routing, resolved-over-bar (Phase 119 CONF-04, minted). At v7.7: S-N02 2/5 (over-routes on 3 of 5 runs). At v7.8 CONF-03: S-N02 3/5 PASS (Phase-118 FIX-03/FIX-04 prose fix moved over bar). Residual disposition: RESOLVED-OVER-BAR with detector-under-count caveat (runs 2,3 are documented detector under-counts where agent still ran a pre-mortem; D-01). NOT a reclassification (D-4). Sentinel asserts v7.8 vector [0,3,3,1,1]. Confirmed by BATT-06 (RR-119-02 sentinel in `_battery_core.self_test_boundary()`)..

12. **RR-130-01** [HIGH] — Main-routing inline-answering regression (Phase 130). P **1/13** DELEGATE FAIL at the v7.11 live re-baseline (`tests/routing-baseline-v7.11.md`) vs the v3.13 anchor (P 11/13); the orchestrator answers the first-principles prompt **inline** (`num_turns:1`, `stop_reason:end_turn`, no `Task` tool_use) instead of auto-delegating — only P4 delegated. Likely a newer/more-capable orchestrator model satisfying the prompt directly. Negatives unchanged (N 20/20). ID kept (RR-`<phase>`-NN convention; Phase-130 slot free). **Documented residual with NO matrix row** (v7.9 D-02 precedent); named the open whole-system gap by `docs/whole-system-remeasure-verdict.md`. honesty-not-score (D-01): recorded as observed, never forced. Offline fix **applied at Phase 133** (imperative `description:` rewrite of `shared/spine/SKILL.meta.yml`, regenerated at zero drift; STRENGTHEN verdict per `docs/rr-130-01-diagnosis.md`). **RESOLVED/CLOSE at Phase 136 live re-measure** (P **11/13** = v3.13 anchor recovery, N 20/20; `tests/routing-baseline-v7.13.md`; see `docs/v7.13-live-remeasure-verdict.md`). ID kept as regression sentinel (row-less, v7.9 D-02 precedent; no count change — RR-130-01 was minted row-less and RESOLVE moves no count). D-04 RESOLVE disposition.

## Reproducible-tier re-run record (v9.3.0 Phase 34)

Three dated sub-blocks recording Phase 34's own re-run basis: the QUAL-01 measurement TIER-04
rests on, and the per-row disposition RIGOR-01..08 (TIER-01) and the four test_69 rows (TIER-02)
carry after their break tests (`.planning/phases/34-reproducible-tier-honesty-and-anchors/34-BREAK-TESTS.md`,
local-only, git-ignored; not present in a fresh clone). This section carries no slash-form
coverage headline — see the Status line and the Headline history table above for that.

### QUAL-01 cost and determinism (TIER-04, D-T2), dated 2026-09-14

`python3 scripts/check-quality-harness.py --self-test` was run ten times in one process loop at
BASE commit `5dad4eb`, timed with `time.perf_counter()` around each `subprocess.run` call, with
nothing else running concurrently. Wall-clock: min 0.421 seconds, median 0.4290 seconds, max
0.524 seconds (one outlier run, +0.09 seconds over the rest, consistent with ordinary OS
scheduling jitter). Distinct stdout sha256 across all ten runs: one. Distinct exit codes across
all ten runs: one (0). The self-test is deterministic over these ten runs — no differing lines
between any pair of runs.

Decision: D-T2 is held — no QUAL-01 CI job is added. QUAL-01's rows carry `battery-only` in the
matrix's Re-run By column, so a green CI badge is never read as covering them; only the offline
battery's own `--self-test` leg re-runs QUAL-01's claims.

### RIGOR-01..08 (TIER-01, D-05), dated 2026-09-14

Each of the eight `v3.7/RIGOR-*` rows was break-tested by deleting a sentence from its cited
validation-rubric.md section and confirming which registered gate goes red. Dispositions,
transcribed from `_rows_methodology_rigor()`'s own docstring in `scripts/check-traceability.py`:

- **RIGOR-01** (Criterion 1: Identify Essence) — re-tiered audit-only. No registered gate
  transcribes a literal from this section, so no break was possible.
- **RIGOR-02** (Criterion 2: Challenge Assumptions) — re-tiered audit-only. Its one literal
  candidate, check-quality-harness.py, stayed green on break (a coincidental substring match
  inside a synthetic self-test fixture, never a live read of the rubric file).
- **RIGOR-03** (Criterion 3: Establish Ground Truths) — re-pointed at
  `scripts/check-high-confidence-bound.py` (HC-BOUND), which broke red naming the deleted text.
  Scope: HC-3..HC-6 pin the v8.19 HIGH-confidence-tightening literals (`at least one
  HIGH-confidence chain` and its EXCEPT clause) inside Criterion 3's Rigorous band only; no
  other sentence of the section is re-read.
- **RIGOR-04** (Criterion 4: Reason Upward) — re-pointed at `scripts/check-selfaudit-scan.py`
  (SCAN-GUARD), whose self-test and live leg both broke red naming the deleted sentence. Scope:
  Rubric-9 asserts the scan-half quoted-span sentence and its direct-quotation half each occur
  exactly once inside the Criterion 4 slice; no other sentence of the section is re-read.
- **RIGOR-05** (Criterion 5: Validate) — re-pointed at
  `scripts/check-high-confidence-bound.py` (HC-BOUND), which broke red naming the deleted text.
  Scope: HC-9..HC-12 pin the v8.19 HIGH-confidence-tightening literals (`at least one
  HIGH-confidence` and its EXCEPT clauses) inside Criterion 5's Rigorous band only; no other
  sentence of the section is re-read.
- **RIGOR-06** (Criterion 6: Conclusion-to-Ground-Truth Traceability) — re-pointed at
  `scripts/check-quality-harness.py` (QUAL-01, battery-only); its render_contract positive
  control broke red naming the section's rule number. Scope: that control asserts rule R11's
  one literal is present somewhere in the file (whole-file, not section-scoped); no other
  sentence of the section is re-read.
- **RIGOR-07** (the section now headed "How to Apply This Gate") — re-pointed at
  `scripts/check-selfaudit-scan.py` (SCAN-GUARD). The row's prior anchor named the section's
  retired name, "How to Apply This Rubric"; the re-point drops the rubric citation entirely
  rather than merely correcting the wording. Scope: Rubric-2 asserts the `**Assumption Audit
  (verify before scoring)**` line is present somewhere in the file (whole-file, plus its order
  relative to the scan block), not that it sits in this section; no other sentence of the
  section is re-read.
- **RIGOR-08** (Scoring Model) — re-tiered audit-only. No registered gate transcribes a literal
  from this section, so no break was possible.

RIGOR-01, RIGOR-02 and RIGOR-08 were first kept `reproducible` at their rubric heading anchors,
`ci` via TRACE-03 (D-05's keep branch). The Phase 34 code review (WR-02) re-tiered them: TRACE-03
checks only that each heading is present, so deleting a section body leaves CI green — a looser
bar than the test_69 rows below were held to. Each now carries an empty `artifact_link` and
`rerun_by="none"`, the test_69 shape; the headline moved 242/129 → 239/132 (Headline history
row 19).

Every re-point proves that a live gate re-reads the named literal(s) at the stated scope, not
that the rest of the section is re-read and not that the row's own unrecoverable v3.7
requirement claim is reconstructed (D-T4). Row count is unchanged for this batch. The five
re-pointed rows keep their tier and moved only `artifact_link`, `gap_rationale` and (for
RIGOR-06) `rerun_by`; the three audit-only rows moved tier as well.

### test_69 rows (TIER-02, D-06), dated 2026-09-14

The four `test_69`-evidenced rows (`v4.2/BASE-01`, `v4.2/BASE-02`, `v4.3/BATT-07`,
`v4.3/BATT-08`) were break-tested with two mutations against
`tests/routing-battery-baseline-v4.3.md`: flipping its `BATTERY: PASS` verdict line to
`BATTERY: FAIL`, and separately replacing its lineage commit `151b197` with `0000000` — each
mutation restored before the next. Both mutations turned FROZEN-EVIDENCE red, but
FROZEN-EVIDENCE is not credited as the pin: its mechanism is `git diff --quiet HEAD` against the
last committed state of every `_FROZEN_PATHS` member, which catches only an uncommitted edit
sitting in the working tree — a committed edit to the baseline file makes its diff clean again
immediately, so it cannot detect the drift a normal commit would introduce. No other registered
gate went red on either mutation; only the local, unregistered
`tests/test_69_merged_baseline_invariants.py` pytest module (no battery registration, no CI job)
caught either change.

Decision: all four rows are re-tiered `audit-only` with an empty `artifact_link` and
`rerun_by="none"` (`check_consistency()` fixture (5); the V818-ROWS precedent). No battery
registration or CI job is added (standing D-D).

### Self-test anchor work list (ANCH-01, D-13), dated 2026-09-14

A reproducible row's `artifact_link` counts as dispatch-checked, not merely defined, only when it
names a separable `_self_test_<claim>` block that is called by literal name from its own script's
`self_test()`/`_run_self_test()` dispatcher and re-runs every clause of the row's statement
(D-12). `_resolve_artifact()`'s own rule decides this — a name matching the `_self_test_`/
`_selftest_` prefix convention, not a bare regex over the anchor string. The full ranking below
(by rows genuinely unlocked under that rule, then by reorder cost, then by whether the script
carries its own `_check_anchor_control_coverage` ratchet) is published in order; only the top
three were taken this phase (D-13).

**Taken:**

1. `scripts/check-loop-closure.py` — anchored: `v8.18/LOOP-01`, `v8.18/LOOP-02`, `v8.18/LOOP-03`,
   `v8.18/LOOP-04`, `v8.18/LOOP-05`, `v9.2/GUARD-01`, `v9.2.1/HAND-05`. Bare: `v9.2/SUP-01`
   (D-14, returned to a bare path at the Phase 34 code review, WR-04: its statement's second
   target, sentences in the emitted agent body describing supplied facts as exempt, is not
   re-run by any block — `_self_test_sup01_candidate_entry` still runs N38/N39, but both drive
   the input-contract check only, which reads `shared/agent/input-contract.md` and nothing
   else in the agent body);
   `v8.18/HARN-02` (D-14: a whole-gate existence claim restating the combined effect of this
   script's own other rows; no distinguishable clause of its own to re-run without re-anchoring
   the whole self-test).
2. `scripts/check-act-limb.py` — anchored: `v8.18/ACT-01`, `v8.18/ACT-02`, `v8.18/ACT-03`,
   `v8.18/ACT-04`, `v8.18/ACT-05`. Bare: `v8.18/HARN-01` (D-14: whole-gate existence claim, same
   reasoning as `v8.18/HARN-02` above); `v8.20/HARN-01-02`, `v8.20/HARN-01-03`, `v8.20/HARN-01-05`
   (D-14: historical build-log entries describing work already done, re-run only as a side effect
   of the aggregate branch-coverage floor staying green, with no distinguishable ongoing clause of
   their own).
3. `scripts/check-registration.py` — anchored: `v8.21/REG-01`, `v8.21/REG-02`, `v8.21/REG-03`.
   Bare: `v8.21/GATE-02` (D-14: whole-gate existence claim restating the combined existence of
   every control in this script's fixture); `v8.21/GATE-03` and `v8.24/GATE-02` (D-14: already
   anchored at a live, non-`_self_test_`-prefixed function that also runs in the live `check`
   leg — D-12 forbids renaming it to manufacture an anchor).

**Every other ranked script, with its exclusion reason:**

- `scripts/check-high-confidence-bound.py` — every row's claim has a separable block, but the
  claims require reordering non-contiguous control clusters and the script carries its own
  `_check_anchor_control_coverage` ratchet; loses the tie-break against `check-registration.py`.
- `scripts/check-agent.py`, `scripts/check-description-budget.py`,
  `scripts/check-install-collisions.py`, `scripts/check-links.py` — DIRECT dispatcher shape, but
  every row's statement is `statement unrecoverable` (D-T4): there is no sourced clause to extract
  into a block.
- `scripts/check-step0-live.py`, `scripts/check-trigger-collisions.py` — same reason: DIRECT
  shape, every row's statement unrecoverable.
- `scripts/check-version-stamps.py` — DIRECT shape, but every row's statement asserts a live-tree
  fact re-verified only by the live `check()` walk over the real tracked files, not by an isolable
  self-test fixture; no new block would change this (D-14).
- `scripts/check-selfaudit-scan.py` — every row is already anchored at a live, non-`_self_test_`-
  prefixed function that also runs outside the self-test leg; D-12 forbids renaming it.
- `scripts/check-traceability.py` (its own remaining unanchored rows) — the model script for D-12
  already dispatch-checks the rest of its rows; what remains is one `statement unrecoverable` row
  plus rows already anchored at live helper functions D-12 forbids renaming.
- `scripts/check-step0-emulator.py` — DIRECT shape, but every row's statement is unrecoverable
  (D-T4); the raw bare-row-count leader by the research document's naive count, excluded here on
  sourcing grounds alone.
- `scripts/check-conf-gate.py`, `scripts/gen-gate-docs.py`, `scripts/report-conformance.py` — LOOP
  dispatch: the call site is a loop variable (`control_fn()`) inside a `for control_id, control_fn
  in _CONTROLS` table, never a literal function name; the anchor-name substring check can never
  match regardless of how the controls are renamed.
- `scripts/check-provenance.py` — INDIRECT dispatch: the dispatcher passes a function object to a
  runner (`_run_control(name, fn)`); the literal call the checker searches for is the runner's own
  name, never the individual control's.
- `scripts/check-focused-parity.py` — WRAPPER dispatch: the entire dispatcher body is a single
  delegate call to one inner function; D-12 rejects a single wrapper anchoring every row of a
  script without adding any check.
- `scripts/check-routing-battery.py` — CROSS-FILE dispatch: the assertion logic it calls lives in
  `scripts/_battery_core.py`, one file removed from its own bare-path rows; also every row's
  statement is unrecoverable.
- `scripts/sync-content.py` — defines no top-level `self_test()`/`_run_self_test()` dispatcher at
  all; its only self-test entry point is CLI-flag dispatched (`cmd_self_test()` via `--self-test`),
  which the dispatch check cannot see.

### Residual: self_test_boundary rows are definition-checked (D-10), dated 2026-09-14

The rows citing `scripts/_battery_core.py#self_test_boundary` are left as they are: nothing is
renamed and no wrapper is added, and they keep `rerun_by="ci"`. `_battery_core.py` defines no
`self_test()`/`_run_self_test()` dispatcher of its own — `self_test_boundary` and its sibling
`self_test_focused` are called from `scripts/check-routing-battery.py`'s own `self_test()`, one
file away. `_selftest_dispatch_problems` is a same-file substring check by its own docstring, so
it cannot see this cross-file call; `_resolve_artifact()` reports no problem for these rows only
because `self_test_boundary` resolves as a defined top-level function, not because the dispatch is
checked. Cross-file dispatch is outside TRACE-03's check today and is a backlog candidate, not
fixed in this phase (standing instruction 2). `_battery_core.py` also holds the RR-* sentinels and
INVARIANT-CHECK's constants, which is a further reason it is not touched here.

## Gap Findings

Summary of Phase 82 gap analysis. Full details in [`requirements-matrix.md`](requirements-matrix.md) (sections "Gap Findings (GAP-01)" and "Future-Milestone Candidate Work List (GAP-02)").

### GAP-01: Current gap picture

**No current open gaps.** Both previously-open gap rows are resolved:

- **GEN-01** → **reproducible** (Phase 93, GEN-01-REARCH Phases 91-93; artifact pointer bumped to the committed v7.13 residual-delta live re-baseline in Phase 137). Artifact: `tests/step0-baseline-v7.13.md` (v7.8 remains the canonical full 8-technique baseline). The Step 0 classifier capability is now reproducibly measured by committed live re-baselines; earned by the committed baseline, not a passing score (reproducible = measured, not passing — v7.13 S-P02 1/5, S-P10 0/5, S-P14 0/5 all CARRIED). The "live re-baseline deferred" carry-forward (carried since v7.1) is RESOLVED. Removed from the open-gap set.
- **GEN-02** → **reproducible** (runbook + wrapper script; Phase 89). Artifact: `docs/live-monitoring-runbook.md`. The periodic live monitoring cadence is now confirmed by a git-tracked runbook with re-runnable harness invocations; it is removed from the open-gap set.

**9 reproducible rows with confirming offline gates** (plus GEN-01/GEN-02 above, confirmed by committed baselines/runbook — 11 total; live behavior documented at Phase 114 v7.6 re-baseline + Phase 117 v7.7 CONF-01 + Phase 119 v7.8 CONF-03):

- **RR-80-01** [CRITICAL] — S-N04 semantically-pre-mortem over-routing; NON_BLOCKING per D-16. Observed 5/5 at Phase 119 v7.8 CONF-03 (Phase-118 prose fix moved over bar; run5 is_error anomaly). Sentinel re-pointed to v7.8 vector [1,1,1,1,0]. Confirmed by STEP0-08 + BATT-06. Artifact: `scripts/_battery_core.py#self_test_boundary`.
- **RR-79-01** [HIGH] — S-P01 **CLOSED** at 3/5 ≥ min-pass at Phase 117 v7.7 CONF-01; **CLOSE SUSTAINED** 3/5 at Phase 119 v7.8 CONF-03 (FIX-01 confirmed; v7.8 vector [1,2,3,0,2]; ID retained, sentinel retained as regression guard). Confirmed by BATT-06. Artifact: `scripts/_battery_core.py#self_test_boundary`.
- **RR-114-01** [HIGH] — S-P02 inversion (supersedes RR-108-01, supersedes RR-95-01, supersedes RR-92-01, supersedes RR-79-02; chain: RR-79-02 -> RR-92-01 -> RR-95-01 -> RR-108-01 -> RR-114-01); CARRIED 1/5 at Phase 114 v7.6 re-baseline; **RESOLVED-STRUCTURALLY-OFFLINE Phase 121 OCH-02** (inversion extended 9→13; detector now reads heading-anchored output-contract headers; frozen v7.6 vector [2,0,1,1,1] UNCHANGED; live S-P02 re-measure forward-committed, honesty-not-score D-01; ID kept, no successor). Confirmed by BATT-06. Artifact: `scripts/_battery_core.py#self_test_boundary`. **[v8.0 ACCEPTED-FINAL]** True K/N: 1/5 (v7.13 live). Terminal disposition — project wrapped.
- **RR-108-02** [HIGH] — S-P05 CLOSED at 4/5 ≥ min-pass at Phase 114 v7.6 re-baseline (chain: RR-79-03 -> RR-92-02 -> RR-95-02 -> RR-108-02 CLOSED). Structurally extended Phase 121 OCH-02 (trade-off extended 6→10; live emission re-measure forward-committed, honesty-not-score D-01). ID retained, sentinel re-pointed to v7.6 vector [2,2,2,2,1]. Confirmed by BATT-06. Artifact: `scripts/_battery_core.py#self_test_boundary`.
- **RR-77-08** [MEDIUM] — CEILING=4 warning; locked by BATT-06 anti-masking sentinel (CEILING=4). Artifact: `scripts/_battery_core.py#self_test_boundary`.
- **RR-117-01** [HIGH] — S-P03 fishbone **CLOSED** at 5/5 at Phase 117 v7.7 CONF-01; **CLOSE SUSTAINED** 4/5 (≥ v7.4 floor) at Phase 119 v7.8 CONF-03 (first fishbone vector sentinel; v7.8 vector [1,4,2,2,3]; RR-75-03 lineage; retained as regression guard). Confirmed by BATT-06. Artifact: `scripts/_battery_core.py#self_test_boundary`.
- **RR-117-02** [MEDIUM] — S-N03 precision sentinel; re-pointed to v7.8 vector [1,0,0,0,0] at Phase 119 CONF-04. All runs stay below MIN_HEADER_HITS → full-composer 5/5 at v7.8. Proves FIX-01+FIX-03/FIX-04 did not hurt routing on genuinely-oblique prompts. D-17 precision finding sustained. Confirmed by BATT-06. Artifact: `scripts/_battery_core.py#self_test_boundary`.
- **RR-119-01** [MEDIUM] — S-N01 over-routing, **RESOLVED-OVER-BAR** at Phase 119 v7.8 CONF-03 (3/5 PASS; v7.8 vector [0,2,1,1,3]; under-count caveat; NOT a reclassification, D-4). Minted Phase 119 CONF-04. Confirmed by BATT-06. Artifact: `scripts/_battery_core.py#self_test_boundary`.
- **RR-119-02** [MEDIUM] — S-N02 over-routing, **RESOLVED-OVER-BAR** at Phase 119 v7.8 CONF-03 (3/5 PASS; v7.8 vector [0,3,3,1,1]; under-count caveat documented — runs 2,3 are detector under-counts where agent still ran a pre-mortem; NOT a reclassification, D-4). Minted Phase 119 CONF-04. Confirmed by BATT-06. Artifact: `scripts/_battery_core.py#self_test_boundary`.

**Audit-only rows** (count: the coverage headline above) — validated by milestone audit; no re-runnable gate exists. These represent genuine coverage but cannot be re-verified programmatically without new confirming tests.

### GAP-02: Candidate work list

Future-milestone candidates: add a confirming Test-Network or Methodology gate for each remaining audit-only row. Priority: MEDIUM audit-only items first, then HIGH. Both sub-counts are derived from the `_SEVERITY_LABEL` 2×2 map over `coverage_tier` × `capability` plus the `_ACTIVE_TAIL_SEVERITY` overrides in `scripts/check-traceability.py` — referenced by symbol, not by line range, which had gone stale twice (WR-02 at v8.18, WR-03 at v8.24) as rows were appended above it — applied to the audit-only total in the coverage headline above, and are read from the `[MEDIUM]`/`[HIGH]` tags in `docs/requirements-matrix.md`'s generated candidate list, not restated here (a hand-typed sub-count here read 91 audit-only / MEDIUM 53 / HIGH 38 from v8.25 until the Phase 33 code review, WR-02). The prior figure of 85 tracked the 206-era audit-only total — see the `121/85/0/206` headline recorded above — not a MEDIUM sub-count; it was never produced by this severity method). The rows promoted in Phase 86 (RR-80-01, RR-79-01, RR-79-02→RR-92-01→RR-95-01→RR-108-01→RR-114-01, RR-79-03→RR-92-02→RR-95-02→RR-108-02-CLOSED, RR-77-08) now have confirming offline gates; Phase 117 CONF-02 adds RR-117-01 (S-P03 fishbone CLOSED) and RR-117-02 (S-N03 precision); Phase 119 CONF-04 adds RR-119-01/RR-119-02 (S-N01/S-N02 resolved-over-bar). Closing the remaining live routing dip (RR-114-01 S-P02 1/5, chain: RR-79-02->RR-92-01->RR-95-01->RR-108-01->RR-114-01) **was** scoped as a future live-routing milestone — **SUPERSEDED**, no such milestone exists (v8.0 terminal). RR-108-02 S-P05 is CLOSED at 4/5 at the v7.6 re-baseline (lone canonical improver); RR-79-01 S-P01 and RR-117-01 S-P03 are CLOSED at Phase 117 v7.7 CONF-01 and their CLOSE SUSTAINED at Phase 119 v7.8 CONF-03. v7.4 introduced three first-time residuals: RR-108-03 (decompose, 0/5) RESOLVED-BY-MERGE (v7.5 decompose→five-whys merge, see `decompose-five-whys-merge.md`), RR-108-04 (estimate, 0/5) CARRIED-INDETERMINATE (spend-limit-truncated at v7.4), RR-108-05 (theoretical-limit, 0/5) CARRIED-INDETERMINATE (spend-limit-truncated at v7.4) — both measurements stand; the CARRIED-INDETERMINATE *status* is **SUPERSEDED** by the ACCEPTED-FINAL disposition below. v7.6 Phase 114 measurement: S-P16 0/5 (merge did NOT improve five-whys routing — REGRESSION; fix forward-committed and APPLIED at Phase 117 — see `merge-validation-verdict.md` Phase 117 section); S-P01/S-P03 regressions RESOLVED at Phase 117 v7.7 CONF-01 and SUSTAINED at Phase 119 v7.8 CONF-03. Merge pairs recorded as deferred at the time: theoretical-limit↔inversion (SECOND recommendation) and estimate↔? (FLAG, partner unscoped) — **SUPERSEDED**, terminally closed as won't-do (v8.0). GEN-01 and GEN-02 are resolved (see GAP-01 above) and no longer appear in this work list. Phase 117 FIX-01/FIX-02/CONF-01/CONF-02 + Phase 118 FIX-03/FIX-04 + Phase 119 CONF-03/CONF-04 complete: the v7.8 fix-and-confirm chain is closed (D-1c CONFIRMED; all 5 blocking conjuncts hold; honesty-not-score: positive conjuncts S-P01 3/5 + S-P03 4/5 sustained; S-N01/S-N02 moved over bar — under-count caveat documented, not reclassified D-4). Recorded as deferred at the time (out-of-scope Fix-#3): NON_BLOCKING_NEGATIVE_IDS reclassification for S-N01/S-N02 (the prompts remain semantically pre-mortem; their resolved-over-bar state is documented) — **SUPERSEDED**, terminally closed as won't-do (v8.0). **[v8.0 ACCEPTED-FINAL]** RR-114-01 (1/5), RR-108-04 (0/5), and RR-108-05 (0/5) are all ACCEPTED-FINAL — no future milestone; project wrapped at Phase 142. The CARRIED-INDETERMINATE notation for RR-108-04/RR-108-05 and the "future live-routing milestone" framing for RR-114-01 are superseded by this terminal disposition. The still-deferred merge-pair recommendations (theoretical-limit↔inversion SECOND, estimate↔? FLAG) and the NON_BLOCKING_NEGATIVE_IDS reclassification for S-N01/S-N02 are likewise terminally closed as won't-do — no future milestones exist.

## Historical Ledger

One row per milestone through v5.3 (per-milestone snapshot promotion to `history/` stopped after
v5.3). Later milestones (v6.1 through v8.0) have no snapshot rows; their records live in the
per-milestone docs — see [`v8.0-final-closure.md`](v8.0-final-closure.md),
`v7.13-live-remeasure-verdict.md`,
[`whole-system-remeasure-verdict.md`](whole-system-remeasure-verdict.md) — and the annotated git
tag history (`git tag -n`). Each row below names the frozen snapshot files, which live in the
**local-only, git-ignored** `docs/history/` directory — they are retained on the working machine
but are not published to the remote, so the filenames below are references, not links.
Milestones with no audit file did not produce one at the time of shipping.

| Milestone | Status | Requirements | Roadmap | Audit |
|-----------|--------|-------------|---------|-------|
| v1.0 | shipped 2026-05-18 | `v1.0-REQUIREMENTS.md` | `v1.0-ROADMAP.md` | `v1.0-MILESTONE-AUDIT.md` |
| v1.1 | shipped 2026-05-19 | `v1.1-REQUIREMENTS.md` | `v1.1-ROADMAP.md` | — |
| v1.2 | shipped 2026-05-20 | `v1.2-REQUIREMENTS.md` | `v1.2-ROADMAP.md` | — |
| v2.0 | shipped 2026-05-22 | `v2.0-REQUIREMENTS.md` | `v2.0-ROADMAP.md` | `v2.0-MILESTONE-AUDIT.md` |
| v3.0 | shipped 2026-05-23 | `v3.0-REQUIREMENTS.md` | `v3.0-ROADMAP.md` | `v3.0-MILESTONE-AUDIT.md` |
| v3.1 | shipped 2026-05-23 | `v3.1-REQUIREMENTS.md` | `v3.1-ROADMAP.md` | — |
| v3.2 | shipped 2026-05-24 | `v3.2-REQUIREMENTS.md` | `v3.2-ROADMAP.md` | `v3.2-MILESTONE-AUDIT.md` |
| v3.3 | shipped 2026-05-25 | `v3.3-REQUIREMENTS.md` | `v3.3-ROADMAP.md` | `v3.3-MILESTONE-AUDIT.md` |
| v3.4 | shipped 2026-05-25 | `v3.4-REQUIREMENTS.md` | `v3.4-ROADMAP.md` | — |
| v3.5 | shipped 2026-05-25 | `v3.5-REQUIREMENTS.md` | `v3.5-ROADMAP.md` | — |
| v3.6 | shipped 2026-05-26 | `v3.6-REQUIREMENTS.md` | `v3.6-ROADMAP.md` | — |
| v3.7 | shipped 2026-05-27 | `v3.7-REQUIREMENTS.md` | `v3.7-ROADMAP.md` | — |
| v3.8 | shipped 2026-05-28 | `v3.8-REQUIREMENTS.md` | `v3.8-ROADMAP.md` | `v3.8-MILESTONE-AUDIT.md` |
| v3.9 | shipped 2026-05-29 | `v3.9-REQUIREMENTS.md` | `v3.9-ROADMAP.md` | — |
| v3.10 | shipped 2026-05-29 | `v3.10-REQUIREMENTS.md` | `v3.10-ROADMAP.md` | — |
| v3.11 | shipped 2026-05-30 | `v3.11-REQUIREMENTS.md` | `v3.11-ROADMAP.md` | — |
| v3.12 | shipped 2026-05-30 | `v3.12-REQUIREMENTS.md` | `v3.12-ROADMAP.md` | `v3.12-MILESTONE-AUDIT.md` |
| v3.13 | shipped 2026-06-03 | `v3.13-REQUIREMENTS.md` | `v3.13-ROADMAP.md` | `v3.13-MILESTONE-AUDIT.md` |
| v4.0 | shipped 2026-06-04 | `v4.0-REQUIREMENTS.md` | `v4.0-ROADMAP.md` | `v4.0-MILESTONE-AUDIT.md` |
| v4.1 | shipped 2026-06-06 | `v4.1-REQUIREMENTS.md` | `v4.1-ROADMAP.md` | `v4.1-MILESTONE-AUDIT.md` |
| v4.2 | shipped 2026-06-11 | `v4.2-REQUIREMENTS.md` | `v4.2-ROADMAP.md` | `v4.2-MILESTONE-AUDIT.md` |
| v4.3 | shipped 2026-06-11 | `v4.3-REQUIREMENTS.md` | `v4.3-ROADMAP.md` | `v4.3-MILESTONE-AUDIT.md` |
| v5.0 | shipped 2026-06-12 | `v5.0-REQUIREMENTS.md` | `v5.0-ROADMAP.md` | — |
| v5.1 | shipped 2026-06-13 | `v5.1-REQUIREMENTS.md` | `v5.1-ROADMAP.md` | `v5.1-MILESTONE-AUDIT.md` |
| v5.2 | shipped 2026-06-13 | `v5.2-REQUIREMENTS.md` | `v5.2-ROADMAP.md` | `v5.2-MILESTONE-AUDIT.md` |
| v5.3 | shipped 2026-06-14 | `v5.3-REQUIREMENTS.md` | `v5.3-ROADMAP.md` | `v5.3-MILESTONE-AUDIT.md` |

## Cross-links

- **Generated matrix (row count: the coverage headline's total):** [`requirements-matrix.md`](requirements-matrix.md)
- **Frozen milestone history:** `docs/history/` — local-only, git-ignored; not present in a fresh clone
- **Project overview and active milestone context:** `.planning/PROJECT.md` — local-only,
  git-ignored; not present in a fresh clone, so deliberately not a link (same treatment as the
  `docs/history/` line above, which it previously contradicted by being one; VAL-03 skips `../`
  targets and so never caught it).
  *(Note: `.planning/` is gitignored, as is `docs/history/`. The canonical historical detail is the promoted `docs/history/` copies named above, which are retained locally only.)*
- **v7.10 agent-goal alignment audit** (ALIGN-01/02/03 — authoritative prioritized inventory of method-fidelity gaps and technical debt behind the DEBT-*/METHFID-* split): `agent-goal-alignment-audit.md`

---

**Addendum — 2026-07-19 (Phase 152 FREEZE-02):** RR-108-04 (S-P10 estimate) and RR-108-05
(S-P14 theoretical-limit) — both recorded ACCEPTED-FINAL above, with "no further live
re-measure" — are re-opened by v8.5's narrow byte-freeze relaxation. See
[`v8.5-byte-freeze-relaxation.md`](v8.5-byte-freeze-relaxation.md) for the exact scope of the
relaxation and what remains frozen. This addendum does not alter the ACCEPTED-FINAL statement
above, which stands as accurate for the v8.0 terminal record; it records a later, additive event.
The BATT-06 sentinels guarding these two residuals remain in place as regression guards and are
unaffected by this re-open. Because this file is the authoritative active-residual surface, note
explicitly: the two residuals' dispositions above are subject to update by the v8.5 re-measure
(Phase 156) — a reader consulting the Active Surface section is not misled by the terminal-state
table appearing earlier in this document.
