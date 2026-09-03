---
phase: 14-closure-ledger-claim-inventory
plan: 05
subsystem: testing
tags: [quality-harness, closure-ledger, frozen-fixture, self-test, mutation-testing]

# Dependency graph
requires:
  - phase: 14-closure-ledger-claim-inventory (plan 01)
    provides: "the post-fix 7/0/1 detect_defects reading (D-02 section-6 slicer fix, D-03 ledger-row narrowing) this fixture pins"
  - phase: 14-closure-ledger-claim-inventory (plan 04)
    provides: "the render-contract fixture/floor machinery this plan's control (j) parallels for the claim-inventory axis"
provides:
  - "tests/quality-ledger-v8.26/ — a frozen, tracked fixture (PR-P1.jsonl, PR-P1.md, README.md) carrying the 2026-09-02 PR-P1 analysis, unreachable-by-gate .planning/captures/ bytes now copied into the tracked tree"
  - "control (j) in _selftest_ledger_traceability — QUAL-01's live leg over the fixture, asserting conclusion_claims==7, zero closure-ledger fragments, untraced_claims==1, and the untraced claim's identity"
  - "three anti-vacuity mutation arms (untraced/claims/ledger axes), each independently neutralization-tested to reproduce its own 'passing vacuously' failure"
affects: [14-06, 15-scan]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "verify-by-mutation on disposable rsync --exclude .git scratch copies, git status --porcelain confirmed empty before/after; both fixture-text mutation (real bug injection) and control-code mutation (arm neutralization) used to prove falsifiability"
    - "derive every mutation from the text/data the control itself already read (via detect_defects' own returned _claims_text/_untraced_claims_text), never a hand-transcribed literal — avoids transcription drift between the fixture and the mutation code"

key-files:
  created:
    - tests/quality-ledger-v8.26/PR-P1.md
    - tests/quality-ledger-v8.26/PR-P1.jsonl
    - tests/quality-ledger-v8.26/README.md
  modified:
    - scripts/check-quality-harness.py

key-decisions:
  - "D-04's 'live leg' extends _selftest_ledger_traceability with a new control (j), not a new CLI flag or main()-level branch — Q3, the planner's stated decision, carried out exactly as specified"
  - "Arm 2's mutation (claims axis) is derived from detect_defects' own _claims_text field, filtering for the Key Insight claim by its bold lead-in prefix, rather than hand-transcribing the paragraph — this sidesteps transcription mismatches (an em-dash/italics slip broke a hand-typed first attempt at this same string)"
  - "Arm 3's quoted span is sliced directly out of the untraced claim's own text (trade_offs_line), guaranteeing the inserted ledger row's quote is a real substring of the claim it is meant to discharge, rather than a second hand-copied excerpt"

patterns-established:
  - "Neutralizing an anti-vacuity arm means patching the CONTROL's mutation code (in a scratch copy) so its mutation still changes the text but no longer produces the predicted detect_defects change — distinct from a 'precondition' failure, which fires when the mutation target cannot be located at all"

requirements-completed: [LEDGER-04]

# Metrics
duration: ~25min
completed: 2026-09-03
---

# Phase 14 Plan 05: Closure-Ledger Claim-Inventory Fixture (D-04) Summary

**Committed the 2026-09-02 PR-P1 analysis as a frozen `tests/quality-ledger-v8.26/` fixture and added control (j) — a QUAL-01 `--self-test` leg asserting its exact `detect_defects` reading (7 claims / 0 ledger fragments / 1 untraced) plus the untraced claim's identity, backed by three independently-neutralization-tested anti-vacuity mutation arms.**

## Performance

- **Duration:** ~25 min
- **Tasks:** 2 completed (2 commits, one per task)
- **Files modified:** 4 (3 created under `tests/quality-ledger-v8.26/`, 1 modified: `scripts/check-quality-harness.py`)

## Accomplishments

- `tests/quality-ledger-v8.26/PR-P1.md` and `PR-P1.jsonl` are byte-identical copies (sha256-verified) of the gitignored `.planning/captures/pr-p1-v8.25.0-2026-09-02/` source — the first time this specific capture becomes reachable by any gate.
- `tests/quality-ledger-v8.26/README.md` follows the `quality-provenance-v8.24/` nine-section precedent: chain of custody with a sha256 table, the verbatim prompt, metadata, per-event census (measured directly from the `.jsonl`, not copied from the donor README), the measured reading with the untraced claim's identity, why the v8.7 corpus and the provenance fixture cannot substitute, guardrail relationship, the pre-§1 ledger disclosure (with an explicit "do not fix this" instruction), and frozen-evidence discipline including the sequencing note that plan 14-06 (not this plan) registers `_FROZEN_PATHS`.
- Control (j), added to `_selftest_ledger_traceability`, reads `tests/quality-ledger-v8.26/PR-P1.md` unconditionally from `REPO_ROOT` — the same shape control (i) already uses for the v8.7 corpus — and asserts `conclusion_claims == 7`, `len(_closure_ledger_fragments) == 0`, `untraced_claims == 1`, and that the single untraced claim's text starts with the `**Trade-offs acknowledged:**` paragraph's opening.
- Three anti-vacuity mutation arms, each derived from the control's own already-read data (never a hand-transcribed literal): Arm 1 appends an inline `(chain C5).` citation to the untraced claim (must flip `untraced_claims` to 0); Arm 2 deletes the Key Insight claim, located via `_claims_text` filtering rather than hand-copied text (must drop `conclusion_claims` to 6); Arm 3 inserts a fenced structural ledger row quoting a real substring of the untraced claim and citing chain C5 (must produce a fragment AND flip `untraced_claims` to 0).
- `python3 scripts/check-quality-harness.py --self-test` exits 0. `bash scripts/check-firewall-battery.sh` reports `FIREWALL: GREEN (23/23)` — confirmed by running the battery, not assumed; the tally is unchanged from before this plan.
- `grep -c 'quality-ledger-v8.26' scripts/check-quality-harness.py` = 3; `grep -c 'quality-ledger-v8.26' scripts/check-firewall-battery.sh` = 0 (registration deliberately deferred to plan 14-06, per this plan's own sequencing note).

## Task Commits

Each task was committed atomically:

1. **Task 1: Create the tracked fixture directory with its provenance README** - `0014330` (feat)
2. **Task 2: Add the live leg and its three-arm anti-vacuity control** - `e5b214b` (feat)

_No TDD tasks in this plan._

## Files Created/Modified

- `tests/quality-ledger-v8.26/PR-P1.md` — the 2026-09-02 extracted analysis, byte-identical to its `.planning/captures/` source (sha256 `5cdf59957ee10464ab5c982ec5fd7a9ae8be08b139b2bc9bc05005e05de7c282`)
- `tests/quality-ledger-v8.26/PR-P1.jsonl` — the raw capture, byte-identical to its source (sha256 `01528c2ebea4982b32fefc85d4ef9bc47d6f47616ba4c9c5aac9766a371b7a96`)
- `tests/quality-ledger-v8.26/README.md` — nine-section provenance record: chain of custody, prompt, metadata, per-event census, the measured 7/0/1 reading with claim identity, substitution analysis, guardrail relationship, pre-§1 ledger note, frozen-evidence discipline
- `scripts/check-quality-harness.py` — new control (j) in `_selftest_ledger_traceability`: the live leg over the fixture, its identity assertion, and three anti-vacuity mutation arms; docstring extended to name the new controls, state this is a QUAL-01 leg (not a new gate), and record the disclosed bounds

## Decisions Made

- Extended `_selftest_ledger_traceability` in place with control (j) rather than a new function, new CLI flag, or `main()`-level live/self-test split (Q3, the plan's stated decision) — matches the existing shape of control (i), which already reads a fixed corpus off disk unconditionally inside `--self-test`.
- Derived Arm 2's deletion target from `detect_defects`'s own `_claims_text` output (filtered by the `**Key insight` prefix) rather than a hand-transcribed paragraph literal. A first attempt hand-typing the paragraph mismatched the source by two characters (missing `*model*`/`*level*` italics markers around two words), which would have silently produced a no-op mutation; deriving it from the extractor's own output makes this class of transcription error structurally impossible.
- Derived Arm 3's quoted span as a slice of the untraced claim's own text (`trade_offs_line`) rather than a second hand-copied excerpt, guaranteeing the inserted ledger row's quote is a real substring of the claim it discharges (and therefore clears `_MIN_LEDGER_FRAGMENT_TOKENS` and `_LEDGER_COVERAGE_THRESHOLD` by construction — verified, not assumed).
- Did not create a `catalog.md` for the new fixture (per the plan's explicit instruction) — `detect_defects` reads `PR-P1.md` directly with no catalog-shaped reader in the path, so an adapter file would wrap nothing.
- Did not touch `_FROZEN_PATHS` in `scripts/check-firewall-battery.sh` or `.github/workflows/validation.yml` — confirmed by `git status --short` showing no changes to either file across both commits. Plan 14-06 registers the new fixture directory after this plan's commits land at HEAD (the plan's own stated sequencing constraint: registering it here would make the battery's untracked-file sweep fail on files not yet committed).

## Deviations from Plan

None — plan executed exactly as written. Both tasks' acceptance criteria were verified by direct execution (not by reading), including all mutation and neutralization scenarios listed below.

## Mutation Verdicts (verbatim, per plan `<output>` instruction)

All mutations were performed on disposable `rsync -a --exclude .git` scratch copies under the scratchpad directory (later deleted); `git status --porcelain` on the real worktree was confirmed empty of any unintended change before and after every mutation — only the two files this plan's tasks intentionally created/modified were staged, matching the plan's own file list.

### Fixture-text mutations (prove the live leg can fail on the exact bytes it reads)

**1 — changing the pinned `7` to `8` in control (j)'s `conclusion_claims` check:**
```
self-test FAIL: ledger_traceability (j) conclusion_claims: measured 7 != pinned 8
```

**2 — deleting the trade-offs paragraph line from the scratch copy's `PR-P1.md`:**
```
self-test FAIL: ledger_traceability (j) conclusion_claims: measured 6 != pinned 7
self-test FAIL: ledger_traceability (j) untraced_claims: measured 0 != pinned 1
self-test FAIL: ledger_traceability (j) untraced claim identity moved: [] does not start with "**Trade-offs acknowledged:** step 2's ~73% is a ceiling requiring a long-term, all-upfront commitment"
```
Both the count and the identity assertion fail, as the acceptance criteria require (plus expected cascading failures in the arm-1/3 precondition and arm-2 anti-vacuity check, since deleting the line also removes the text those arms derive their mutations from).

### Anti-vacuity neutralization (prove each arm's own falsifiability, in isolation)

**Arm 1 neutralized** — mutation string changed from `" (chain C5)."` to `" (see appendix)."` (no chain reference):
```
self-test FAIL: ledger_traceability (j) arm 1 ANTI-VACUITY: appending an inline chain C5 citation to the trade-offs claim did not discharge it — untraced_claims measured 1, expected 0; the untraced-axis assertion is passing vacuously
```

**Arm 2 neutralized** — mutation changed to truncate one trailing character of the Key Insight claim instead of deleting the whole claim:
```
self-test FAIL: ledger_traceability (j) arm 2 ANTI-VACUITY: deleting the Key Insight claim did not drop conclusion_claims to 6 — measured 7; the claims-axis assertion is passing vacuously
```

**Arm 3 neutralized** — inserted ledger row's arrow and `chain` keyword dropped (`"...` `" see C5`` instead of `` `" -> chain C5` ``), so it no longer matches `_STRUCTURAL_LEDGER_ROW_RE`:
```
self-test FAIL: ledger_traceability (j) arm 3 ANTI-VACUITY: inserting a structural ledger row inside section 6 yielded zero closure-ledger fragments; the ledger-axis assertion is passing vacuously
```

Each neutralization was run on its own fresh scratch copy, with only that one arm's code patched — confirming the three arms fail independently, not in combination.

## Measured Readings (verified by execution)

```
                                claims  ledger_frags  untraced
tests/quality-ledger-v8.26/PR-P1.md       7            0          1   <- pinned by control (j)
```

Untraced claim identity (verbatim, from `PR-P1.md` §6): `**Trade-offs acknowledged:** step 2's ~73% is a ceiling requiring a long-term, all-upfront commitment (A19, unverified) and ARM-compatible dependencies (A20, unverified); the realized figure on a 1-year no-upfront plan is materially lower. …`

sha256 digests (checkable against `tests/quality-ledger-v8.26/README.md`'s own table):
```
PR-P1.jsonl  01528c2ebea4982b32fefc85d4ef9bc47d6f47616ba4c9c5aac9766a371b7a96
PR-P1.md     5cdf59957ee10464ab5c982ec5fd7a9ae8be08b139b2bc9bc05005e05de7c282
```

Battery tally: `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (23/23)`, run twice (once after Task 2's implementation, once as the final pre-commit check) — the tally is unchanged from before this plan.

## Credential/Path Check (T-14-15, threat register)

Before committing, the copied `.jsonl` was scanned for credentials, tokens, and out-of-repo paths (`grep -oiE '(api[_-]?key|secret|token|password|bearer|AKIA[0-9A-Z]{16}|/home/[a-zA-Z0-9_.-]+)'`). Matches found: `apiKeySource":"none"` (a session-metadata field recording that no key was used, not a key itself), the word "secrets" inside fetched AWS documentation prose (general advice text, not a credential), "token"/"Token" as usage/token-count JSON fields (not auth tokens), and absolute paths under `/home/chrisdavidson/Projects/...`, `/home/chrisdavidson/.claude/...` — the same class of "donor machine's absolute paths" the `quality-provenance-v8.24/README.md` precedent already discloses and explicitly instructs not to "fix". No credential, API key, or path outside this repo/plugin-cache class was found.

## Issues Encountered

- Same as plans 14-01/14-02/14-03/14-04: this worktree had no pytest-capable interpreter, so `bash scripts/check-firewall-battery.sh` initially reported `FIREWALL: BLOCKED` naming `[PREREQ] VAL-03`. Resolved via `uv sync` (creates `.venv`, ships pytest 9.1.1); battery then reported `FIREWALL: GREEN (23/23)`. `.venv` is gitignored and was not committed.
- `.planning/captures/pr-p1-v8.25.0-2026-09-02/` (the gitignored source directory) and `.planning/phases/14-closure-ledger-claim-inventory/{14-05-PLAN.md,14-CONTEXT.md,14-PATTERNS.md}` were not present in this fresh worktree because `.planning/` is gitignored repo-wide; copied from the main working tree at the start of execution — a local-only, uncommitted copy of already-committed-elsewhere planning artifacts and capture bytes, matching every prior plan's (14-01 through 14-04) identical note.
- A first hand-transcription of the Key Insight paragraph (for the original Arm 2 mutation design) silently mismatched the source by two characters (missing italics markers), which would have produced a no-op mutation undetected by casual reading. Caught during prototyping (not after commit) by deriving the mutation from `_claims_text` instead — recorded here as the reasoning behind that design decision, not as a shipped defect.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- Plan 14-06 can now register `tests/quality-ledger-v8.26` in `scripts/check-firewall-battery.sh`'s `_FROZEN_PATHS` — this plan's files are committed at HEAD, satisfying the sequencing constraint plan 14-05 itself stated.
- Control (j) proves LEDGER-04's fixture half is not merely present but falsifiable on all three of its pinned numbers plus the untraced claim's identity — a future loosening of `_conclusion_claims`, `_closure_ledger_fragments`, or `_claim_is_traced` that silently discharges the trade-offs paragraph will fail this control by name.
- No blockers.

---
*Phase: 14-closure-ledger-claim-inventory*
*Completed: 2026-09-03*
