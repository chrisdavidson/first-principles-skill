# v9.0 Live Conformance Fixture

**Status: FROZEN read-only evidence — never regenerated, never hand-edited to match a later
result.** Every `.jsonl`/`.md` pair in this directory is a real, live `claude -p` dispatch of the
shipped `first-principles:first-principles` agent, captured and committed as-is. Any correction
to a reading is a fresh, separately-provenanced capture, not a silent edit of one of these.

## Purpose

This fixture is the first measurement in this project's history that scores **the agent's own
live output**, rather than prose written about the agent, against the unmodified,
CONTRACT-06-frozen `detect_defects`. Every prior conformance surface
(`shared-examples`, `generated-twin`, `contract-surface`, `adversarial-corpus`) reads static
markdown authored or curated in-tree. Nothing here was authored: the eight `.md` analyses are
extracted verbatim from eight `claude -p --output-format stream-json --verbose` sessions, through
`_persist_or_diagnose_analysis`, with no edit of any kind. A capture in this directory is
**evidence**, not a shipped artifact, and no item's content may ever be quoted as fact or copied
into `shared/` or `first-principles/`.

## Provenance

- **Catalog dispatched from:** `tests/live-conformance-catalog.md` (8 rows, `| ID | Prompt |
  Notes |` shape). All eight prompts are copied verbatim from `tests/quality-catalog-v8.7.md` (3
  rows) and `tests/premise-rejection-catalog.md` (4 rows, `Prompt` column only), plus one
  distinct-id repeat of `PR-P1`'s prompt (`PR-P1-R2`) for the D-02 comparison pair.
- **Run date:** 2026-09-06 (all eight dispatches landed in one session window,
  2026-09-06T00:08 -> 01:23 local, per `20-02-SUMMARY.md`'s Task 2 table).
- **Body git sha the runs measure:** `41696efda42c29bb3f26f20143023411d9eb7ae6` — the commit
  recorded by plan 20-01 immediately before dispatch. Confirmed here, independently, that no file
  under `shared/` or `first-principles/` changed between that sha and the current HEAD
  (`git diff --name-only 41696efda42c29bb3f26f20143023411d9eb7ae6..HEAD -- shared/
  first-principles/` returns nothing) — the 8 runs and the tree as it stands today share the
  identical agent body, output template and validation rubric.
- **This is a written reinterpretation of CONF-09's "the shipped v8.26.0 body" (D-20-B).**
  `git diff --name-only v8.26.0..41696efda42c29bb3f26f20143023411d9eb7ae6 -- shared/
  first-principles/` returns exactly 28 files, all under `shared/examples/*` and
  `first-principles/agents/references/examples/*` — the Phase-18 worked-example rewrite. The
  agent body, the output template and the validation rubric are byte-unchanged since the
  `v8.26.0` tag. HEAD is read as satisfying CONF-09 because it is the only reading that can show
  whether Phase 18's exemplar conformance propagates into live output; the tag itself is a body
  no user has run since Phase 18.

## Chain of custody

One row per file in this directory. `.gitkeep` is the pre-dispatch placeholder from plan 20-01
and carries no run content (0 bytes, `d5*` well-known empty-file hash) — it is retained here
rather than deleted because deleting it deliberately would leave no committed non-README file at
all if every capture were ever pruned; it is not evidence of a run and is listed for completeness,
not chain-of-custody.

| File | sha256 |
|---|---|
| `.gitkeep` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `Q-P1.jsonl` | `6f0c94e01d0e7f7be9613443514bcf5dddaf4e0c67a5ea3ebe3c0e2c45a419a7` |
| `Q-P1.md` | `54a0140485c19a74eb62434b2aa2537db9bb63f340e9db24be14bc08fd1b3871` |
| `Q-P2.jsonl` | `dc478c05788d6df5c31e2b3cbcff543002c3e8c35da6deb2685474b59a661c0b` |
| `Q-P2.md` | `f8a4fa7e234249feded17deb2683063337088a16f29435e5e7fae941c712dea2` |
| `Q-P3.jsonl` | `433ec5a3ffeea5a09a690b150a8b3be18366c6891a5dcced90c2ad8fd0ab122c` |
| `Q-P3.md` | `8adfcc66ad1d445cf866974e1023b5f7ee03f62d7cf5a6878781c7320efc30a4` |
| `PR-P1.jsonl` | `30cfeffda0476e04ad6eee88496e060ea78e1cd9842bc14bace1b38b463f2263` |
| `PR-P1.md` | `31ca943a45737d96e99794350549cfb40629af0145e3045c6be553d1823b473b` |
| `PR-P2.jsonl` | `3c46807dcd32f4043f626f7c520c4ffd2de0e79bfd49c948299949352b6b2f03` |
| `PR-P2.md` | `e057d8adebb5cb53fd90842ffd7a7de8aaf39d0cef70449a2159a9da6206ec4e` |
| `PR-N1.jsonl` | `0a5d6928a18b77c2396688730f0c77e48eb358754fc9d72825f8b81ce1766f7a` |
| `PR-N1.md` | `e90b82f139a426759965f597e87e4534b9a3b0c4aed6f049c4ff3a081bfe11b5` |
| `PR-N2.jsonl` | `91ce6d8bd8b698904c4b8f29d8fb5b79dda0e8e67bd1693ab6ec258fcbbd4f1f` |
| `PR-N2.md` | `f0e9381843dc3929efc683d34e4819b58f34268ff4d20e46516f4ed7254ab6f8` |
| `PR-P1-R2.jsonl` | `d53c721146ce2738ebf5cfce9b3ed896d8b387e62537e542ec00b91ca95dbc52` |
| `PR-P1-R2.md` | `205678ffcaf4e45c1cf6410f7954276882131eea1fcb748527e34938117f5d32` |

`.jsonl` line counts and terminal outcome (`classify_invocation_outcome`, never a bare grep on
`api_error_status`):

| File | bytes | lines | outcome |
|---|---|---|---|
| `Q-P1.jsonl` | 216898 | 61 | `completed` |
| `Q-P2.jsonl` | 189059 | 44 | `completed` |
| `Q-P3.jsonl` | 710590 | 94 | `completed` |
| `PR-P1.jsonl` | 241287 | 71 | `completed` |
| `PR-P2.jsonl` | 241669 | 54 | `completed` |
| `PR-N1.jsonl` | 256671 | 82 | `completed` |
| `PR-N2.jsonl` | 239423 | 68 | `completed` |
| `PR-P1-R2.jsonl` | 258312 | 83 | `completed` |

Every hash and count above was recomputed directly against the bytes on disk in this session
(`sha256sum`, `wc -l`, `stat -c%s`, and a fresh `classify_invocation_outcome` call per file) — none
was copied from `20-02-SUMMARY.md`'s table without independent recomputation.

## Run inventory and outcomes

The four D-20-A counts, computed by the unmodified, CONTRACT-06-frozen `detect_defects` (via
`report-conformance.py::build_row`'s exact derivation — `heading_malformed_blocks` from the raw
text unconditionally; `nonconforming_verdict_cells` and `silent_untraced_claims` only when
`section_resolution` reads `"OK"`). All eight rows resolved; none is `unreadable`.

| ID | outcome | `.md` persisted | `section_resolution` | `heading_malformed_blocks` | `nonconforming_verdict_cells` | `silent_untraced_claims` | clean |
|---|---|---|---|---|---|---|---|
| Q-P1 | completed | yes | OK | 0 | 0 | 0 | yes |
| Q-P2 | completed | yes | OK | 0 | 31 | 0 | no |
| Q-P3 | completed | yes | OK | 0 | 0 | 0 | yes |
| PR-P1 | completed | yes | OK | 0 | 0 | 0 | yes |
| PR-P2 | completed | yes | OK | 0 | 0 | 0 | yes |
| PR-N1 | completed | yes | OK | 0 | 1 | 0 | no |
| PR-N2 | completed | yes | OK | 0 | 1 | 0 | no |
| PR-P1-R2 | completed | yes | OK | 0 | 0 | 0 | yes |

A run with no analysis would read the literal `no-analysis` in all four defect columns, never `0`
— not exercised in this corpus, since all eight runs completed and produced a persisted `.md`.

**Primary rate (clean over runs attempted):** `5 of 8`.
**Secondary conditional rate (clean over runs completed):** `5 of 8` (identical here because all
eight runs completed; the two rates diverge only when a transport-layer stub occurs, which none
of these eight did).

**Outcome breakdown:** 8 of 8 `completed`; 0 `rate_limit_stub`; 0 `transport_error_stub`; 0
`no_terminal_result`.

**The three non-clean runs, named precisely (never averaged over):** `Q-P2` fails on all 31 of
its 31 Assumptions Table Verdict cells, using its own richer vocabulary (`Accepted as a modelling
convention`, `Unverified — flagged`, `Challenged — rejected`, `Verified approximately true`,
`Partially verified by construction`) in place of the prescribed leading token
`Accept`/`Challenge`/`Discard`. `PR-N1` and `PR-N2` each fail on exactly one Verdict cell out of
12 and 19 respectively — `Accept as necessary, Challenge as sufficient` and `Accept
provisionally`, both inserting descriptive text between the leading token and the em-dash. Every
disposition is filed in `tests/live-conformance-catalog.md`'s Notes column against
`shared/spine/references/output-template.md`'s Verdict Vocabulary section and
`shared/spine/references/validation-rubric.md` Criterion 2's Rigorous descriptor — never against
a detector.

## Within-body variance and cross-body longitudinal comparisons (D-02)

Two comparisons D-02 bought at the cost of one extra run, both scored read-only by the same
unmodified `detect_defects`, both stated as an observation at this N, never as a trend:

**`PR-P1` vs `PR-P1-R2` (within-body variance — two runs of the identical prompt against the
identical HEAD body):**

| | `PR-P1` | `PR-P1-R2` |
|---|---|---|
| `conclusion_claims` | 6 | 11 |
| `untraced_claims` | 0 | 0 |
| `verdict_cells` | 21 | 17 |
| `nonconforming_verdict_cells` | 0 | 0 |
| `chain_blocks` | 9 | 9 |
| `malformed_chain_blocks` | 0 | 0 |

Both runs read clean under all four D-20-A counts. `conclusion_claims` and `verdict_cells` differ
materially between the two runs of the identical prompt against the identical body — a real
within-body variance signal on claim/cell *count*, even though the *conformance* reading is
unchanged. At N=2 this is an observation, not evidence of a trend: it says two runs of one prompt
are not verbatim-identical in shape, not that either shape is more representative.

**`PR-P1` (HEAD) vs `tests/quality-provenance-v8.24/PR-P1.md` (v8.24.0, cross-body longitudinal —
scored read-only; `git status --porcelain tests/quality-provenance-v8.24` confirmed empty before
and after this comparison, so the registered `_FROZEN_PATHS` fixture was read, never written):**

| | `PR-P1` (HEAD) | `PR-P1` (v8.24.0) |
|---|---|---|
| `conclusion_claims` | 6 | 4 |
| `untraced_claims` | 0 | 3 |
| `silent_untraced_claims` | 0 | 3 |
| `verdict_cells` | 21 | 16 |
| `nonconforming_verdict_cells` | 0 | 0 |
| `chain_blocks` | 9 | 5 |
| `malformed_chain_blocks` | 0 | 0 |
| `selfaudit_disagreements` | 0 | 1 |

The v8.24.0 capture would **not** have scored clean under D-20-A's own rubric (3 silent untraced
claims, 1 self-audit disagreement) had this fixture's rate existed at that time; the HEAD capture
does. At N=2 across two different bodies (`v8.24.0` vs. the Phase-18-plus HEAD body, separated by
28 rewritten worked-example files and one build), this is a two-point observation, not evidence
of a trend — it is consistent with an improvement, and it is equally consistent with ordinary
run-to-run variance of the kind `PR-P1`/`PR-P1-R2` already demonstrates on the identical body.
Neither reading is strong enough, alone, to attribute the difference to Phase 18's exemplar
rewrite.

## Bypass disclosure (D-04)

Every run in this fixture went through `--probe`'s frozen `_wrap_for_bypass` meta-instruction,
which commands verbatim Agent-tool dispatch and contains no Step 0 trigger phrases outside its
interpolated verbatim slot. **This is a conformance rate conditional on delegation having occurred, not an end-to-end user-path rate** — the same disclosed-bound voice R7/R9/R10 use on the chain-form and chain-head grammar checks. Whether a real, unwrapped user prompt would have
reached DELEGATE at all is a separate question this fixture does not measure; `check-routing.py`
and `check-routing-battery.py` are the instruments that measure it, and neither is touched or
extended by this fixture.

## Non-interactive-branch disclosure, prompt-correlated (carried forward from 20-02)

Five of the eight captures — all five `PR-*` rows (`PR-P1`, `PR-P2`, `PR-N1`, `PR-N2`,
`PR-P1-R2`); none of the three `Q-*` rows — open by disclosing that `AskUserQuestion` was
unavailable. This is the Input Contract's prescribed fallback
(`shared/agent/input-contract.md` lines 23-30) firing under the Plan-36-locked non-interactive
`claude -p` transport, **not a defect**: incidence is prompt-correlated (5/5 terse `PR-*` rows;
0/3 figure-dense `Q-*` rows) and carries no measured conformance penalty — the worst run in this
corpus by verdict-cell nonconformance (`Q-P2`) is a non-disclosure row, and `silent_untraced_claims`
reads 0 across all eight captures regardless of disclosure status. No run was re-dispatched on
account of it; it is filed as a finding, not a defect.

## Not reproducible

Stated outright, following the `quality-provenance-v8.24` precedent: no command in this repository reproduces these captures. There is no seed and no determinism guarantee for a live `claude -p` dispatch; re-running any one of these eight prompts against the identical body would produce a genuinely different analysis, as the `PR-P1`/`PR-P1-R2` within-body-variance comparison above demonstrates directly, on this fixture's own evidence, without needing to invoke the general principle. Do not attempt to "restore" a missing or corrupted file in this directory by re-dispatching the same prompt — that produces new evidence with its own provenance, never a replacement for lost evidence.

## Captures are not read this phase (D-06)

All nine PROV-GUARD provenance columns (`provenance_labels`, `unmatched_sources`,
`unreadable_sources`, `literals_checked`, `unlocated_literals`, `misattributed_literals`,
`zero_literal_gts`, `orphan_fetches`, `provenance_flag`) read `n/a` for all eight runs in this
fixture on the published `docs/conformance-baseline.md` surface, even though the `.jsonl`
captures needed to answer those columns exist in this very directory. `n/a` here means **no join
was performed**, never "checked, found clean" — the same three-way column vocabulary
(`number` / `"n/a"` / `"unreadable"`) every other surface in `docs/conformance-baseline.md`
already uses. `check-provenance.py` is not run over these captures this phase, and its live leg's
pinned `7/7 sources matched, 35/35 literals located` reading, from the `tests/quality-provenance-v8.24`
fixture, is untouched.

**Backlog 999.12 / MEAS-01 stays open**, with a written bound recorded here: its input — real,
committed, multi-prompt live captures with subagent tool-call detail — now exists in-tree for the
first time. This phase creates MEAS-01's substrate; it does not consume it.

## Frozen-evidence discipline and sequencing note

This directory, and `tests/live-conformance-catalog.md` beside it, are registered in
`scripts/check-firewall-battery.sh`'s `_FROZEN_PATHS` array by **plan 20-06**, deliberately in a
commit strictly after these captures and this README land. Registering earlier would turn
FROZEN-EVIDENCE red on its own untracked-file sweep leg before these files were ever committed,
and would make `is_frozen_destination` refuse `--probe`'s `.md` write during dispatch (plan
20-02) — both landmines the `tests/quality-ledger-v8.26` precedent already documents and this
fixture repeats deliberately rather than by oversight. At the time this README is written,
`_FROZEN_PATHS` holds 20 entries and does not yet include either of this fixture's two paths.

Carried forward from the `tests/quality-provenance-v8.24` precedent, restated rather than
re-derived: FROZEN-EVIDENCE's protection, once registration lands, is a `git diff --quiet HEAD`
sweep plus an untracked-file sweep over the registered pathspec. It catches an edit to an
already-tracked file and a new file appearing inside the frozen directory. It does **not** catch
a committed `git rm` of one of these files — that removal is already in HEAD by the time the
check runs, so no worktree comparison ever sees it. The check is tamper-evidence for modification
and addition, never a deletion guard. Any change to this fixture's committed contents, including
removal, must be reviewed in-diff like any other commit; nothing here enforces that
automatically.

## Superseded attempts

None. All 8 of 8 authorised runs completed on their first dispatch (`20-02-SUMMARY.md`, Task 2);
D-20-A's re-dispatch policy for a transport-layer stub was never invoked, and
`tests/live-conformance-v9.0/superseded/` does not exist.
