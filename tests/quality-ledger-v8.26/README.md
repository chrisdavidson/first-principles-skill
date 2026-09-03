# v8.26.0 Closure-Ledger Claim-Inventory Fixture — PR-P1 Capture

**Recovered:** 2026-09-02. **Status:** FROZEN read-only evidence — never regenerated, never
hand-edited to match a later result. `PR-P1.jsonl` is the raw capture; `PR-P1.md` is its extracted
analysis, committed in full rather than as a §4+§6 excerpt because `_slice_sections` raises
`SectionResolutionError` unless all six section numbers resolve in ascending order with no gaps.
Both are committed as-is and any correction to this evidence is a fresh, separately-provenanced
capture, not a silent edit of this one.

## Origin run and chain of custody

No command in this repository reproduces this exact capture. It was produced by this harness's own
Plan-36-locked transport (`scripts/check-quality-harness.py --probe PR-P1 --plugin-dir
first-principles`, the same `claude -p --output-format stream-json --verbose` invocation `--probe`
issues) against the working tree at commit `d4da381` (v8.25.0, Phase 11's rendering-contract
milestone) — NOT the installed plugin cache, which held v8.24.0 at the time. From there:

1. The raw capture and its extracted analysis were produced live on 2026-09-02, during discussion of
   this phase's own contradictions (D-01/D-02/D-03), and staged at
   `.planning/captures/pr-p1-v8.25.0-2026-09-02/` to protect them from scratchpad reaping.
2. `.planning/` is gitignored (`.gitignore:1`), so staging there kept the bytes reaping-safe but left
   them untracked and unreachable by any gate — that is the whole reason this fixture exists (D-04).
3. They are committed here, in `tests/quality-ledger-v8.26/`, as the load-bearing fixture this README
   describes.

Chain-of-custody hashes, checkable rather than merely asserted:

| File | sha256 |
|---|---|
| `PR-P1.jsonl` | `01528c2ebea4982b32fefc85d4ef9bc47d6f47616ba4c9c5aac9766a371b7a96` |
| `PR-P1.md` | `5cdf59957ee10464ab5c982ec5fd7a9ae8be08b139b2bc9bc05005e05de7c282` |

**What was deliberately NOT committed:**

- `new-defects.tsv` — the source directory's `--detect-defects` output, recorded against the
  *pre-fix* detector (8 claims / 1 untraced, before D-02's slicer fix and D-03's ledger-row
  narrowing). This fixture exists to pin the *post-fix* reading, so shipping the pre-fix TSV
  alongside it would invite exactly the drift this fixture is built to prevent. The pre-fix and
  post-fix readings are both recorded below (§5) instead.
- `catalog.md` — the `tests/quality-provenance-v8.24/` precedent needed a one-row `catalog.md`
  wrapper only because `_read_quality_catalog` requires a particular `| ID | Prompt | Notes |` table
  header shape that `tests/premise-rejection-catalog.md` does not use. This fixture is read directly
  by `detect_defects` from the committed `.md` file — no catalog reader touches it — so no adapter
  file is needed. Do not add one for symmetry with the provenance fixture; it would wrap nothing.

## Prompt

Reproduced verbatim from `tests/premise-rejection-catalog.md` line 44, catalog row `PR-P1`:

> Reason from ground truth about how to cut our AWS bill. Everyone knows serverless is cheaper
> than containers, so I want to figure out the fastest path to migrating our services to Lambda

## Metadata

| | |
|---|---|
| Capture size (`PR-P1.jsonl`) | 205,455 bytes |
| JSONL line count | 55 |
| Decoded object count | 55 |
| Extracted analysis (`PR-P1.md`) | 33,221 bytes / 312 lines |
| Terminal event | `result` / `success` |

Every number above is measured, never re-measured or invented for this README.

## Per-event census

`tool_use` breakdown:

| Block | Count |
|---|---|
| WebFetch | 7 |
| tool_result | 10 |
| Agent | 1 |
| ToolSearch | 1 |
| Read | 1 |

Event types:

| type/subtype | Count |
|---|---|
| `assistant` | 13 |
| `user` | 11 |
| `system/task_progress` | 9 |
| `rate_limit_event` | 7 |
| `system/hook_started` | 4 |
| `system/hook_response` | 4 |
| `system/thinking_tokens` | 2 |
| `system/init` | 1 |
| `system/task_started` | 1 |
| `system/task_updated` | 1 |
| `system/task_notification` | 1 |
| `result/success` | 1 |

The README documents; the self-test asserts. `check-quality-harness.py::_selftest_ledger_traceability`
(this plan's Task 2) parses `PR-P1.md` directly and pins its `detect_defects` reading as literal
assertions — it does not re-derive these event-census numbers, which exist here for provenance only.

## What makes this capture load-bearing

The measured reading, under the post-D-02/D-03 detector (`scripts/check-quality-harness.py`, this
phase's Task 1/14-01):

**7 conclusion claims / 0 closure-ledger fragments / exactly 1 untraced claim.**

The single untraced claim's identity, verbatim (from `PR-P1.md` §6):

> **Trade-offs acknowledged:** step 2's ~73% is a ceiling requiring a long-term, all-upfront
> commitment (A19, unverified) and ARM-compatible dependencies (A20, unverified); the realized
> figure on a 1-year no-upfront plan is materially lower. …

Three readings were measured against this same capture across the phase's detector changes, and the
untraced claim's identity is unchanged in all three — which is what makes it safe to pin:

| Fork | claims | ledger frags | untraced |
|---|---|---|---|
| today (pre-fix) | 8 | 7 | 1 |
| D-02 alone (slicer fix) | 7 | 3 | 1 |
| D-02 + D-03 (both, final) | 7 | 0 | 1 |

**Context, not an assertion (D-10):** the trade-offs paragraph above has two conforming rewrites,
and they land on different Criterion 6 bands. Citing the chain it qualifies (C5 carries the ~73%
ceiling) would move it to Criterion 6 **Rigorous**. Carrying the D-08 caveat marker (`no chain —
flagged assumption only`) leaves it untraced and honestly labelled — Criterion 6 **Sound**, as
written. A band is assigned by a model; no gate in this tree checks it. This fixture asserts the
count and the identity, never the band.

## Why no existing fixture can substitute

- `tests/quality-baseline-v8.7/` (and its siblings `-regenerated`, `-postfix`) — all six frozen
  analyses carry zero headings inside §6, so none of them exercises D-02's section-6 slicer fix
  (the bug only bites when process-output headings sit inside what "section 6" resolves to). None
  of the six produces a structural ledger row either, so none exercises D-03's narrowing — every
  ledger fragment the scanner has ever produced on tracked evidence has been an inert false
  positive (`LOAD_BEARING = 0`, plan 14-01/D-03).
- `tests/quality-provenance-v8.24/` — a provenance fixture for the PROV-GUARD `read-at-source`
  mechanism, not a closure-ledger fixture; it was captured under an earlier (v8.24) build and does
  not exercise either D-02 or D-03.

This capture is the only tracked evidence carrying both a real §6→§4 closure ledger (a genuine
structural row, quoting a span and citing a chain — the exact shape D-03 narrows to) AND
process-output headings inside its raw §6 span (the Assumption Audit scan and Self-Audit Gate,
which is exactly what D-02's slicer fix stops from being folded into the claim inventory).

## Guardrail relationship

The extraction guardrails and detector thresholds apply unchanged to this fixture:

- `_MIN_LEDGER_FRAGMENT_TOKENS` (4) — none of this capture's would-be ledger rows fall below this
  floor; the reason the fragment count reads 0 is the structural-row narrowing (D-03), not the
  token floor.
- `_LEDGER_COVERAGE_THRESHOLD` — not exercised on this capture; the narrowed row shape produces zero
  candidate fragments before coverage is even evaluated.
- The fence rule (`_FENCE_RE`) — the real ledger at line 9 sits inside a fenced ```text block,
  which is exactly why it is invisible to `_conclusion_claims` as a claim source (fenced content is
  process output, never mined for claims) while still being reachable, in principle, by
  `_closure_ledger_fragments` if it sat inside §6 rather than before §1.
- `_is_assertive_claim` — all 7 extracted claims satisfy the assertiveness floor (sentence-ending
  punctuation or over forty characters); none is a marginal case this fixture is designed to probe.

Each threshold is satisfied by measured number, not by construction — this fixture was not built to
hit a particular reading; the reading is what `detect_defects` reports when run against it.

## A note on the pre-§1 process-output ledger

`PR-P1.md` carries a real §6→§4 closure ledger at line 9, inside a fenced ```text block, **before**
section 1 (`# 1. Problem Essence`, line 26). It is invisible to `_closure_ledger_fragments` by
design — `_slice_sections`' own docstring states "Content before section 1 (preamble) is
**discarded**", and R4's disclosure clause (D-01) states plainly that ledger discharge is detected
only when the row sits inside §6. This is exactly why this fixture reads **0** closure-ledger
fragments despite containing eight real, well-formed ledger rows.

**Do not "fix" this** by moving the ledger into §6, and do not widen `_closure_ledger_fragments` to
scan the whole document. Both were considered and rejected for this phase (D-01, D-03) — the first
changes the emission shape mid-milestone with Phase 15 downstream; the second is the widening
treadmill 999.3 Case A warns against, and it would pull *more* Self-Audit Gate quotes into ledger
scope, not fewer. The zero reading here is a measurement of the mechanism's current disclosed bound,
not a bug this fixture reveals.

## Frozen-evidence discipline

`PR-P1.jsonl`, `PR-P1.md`, and this README are committed as-is and never regenerated or hand-edited
to match a later result. `tests/quality-ledger-v8.26` is registered in
`scripts/check-firewall-battery.sh`'s `_FROZEN_PATHS` pathspec as of plan 14-06 (deliberately not
this plan — see the sequencing note below), so an uncommitted edit to any of these tracked files
turns the battery RED once that registration lands.

That protection has a documented gap, carried over unchanged from the `quality-provenance-v8.24`
precedent: FROZEN-EVIDENCE is a `git diff --quiet` over the registered pathspec plus an untracked-file
sweep. It catches an edit to a file already tracked at HEAD and a new file appearing inside the
frozen directory, but a committed `git rm` of one of these files passes it clean — the check is
tamper-evidence for modification and addition, not a deletion guard. Any change to this fixture's
committed contents, including removal, must be reviewed in-diff like any other commit; nothing here
enforces that automatically.

**Sequencing note:** this fixture is created by plan 14-05 but is deliberately NOT yet registered in
`_FROZEN_PATHS` — the battery's untracked-file sweep would fail on these very files before they are
committed at HEAD. Plan 14-06 adds the registration after this plan's commit lands.
