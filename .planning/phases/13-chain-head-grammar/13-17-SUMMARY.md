---
phase: 13-chain-head-grammar
plan: 17
subsystem: quality-harness / traceability self-tests (WR-01, WR-02, doc-row honesty)
tags: [gap-closure, falsifiability, chain-head-grammar, documentation-accuracy]
dependency-graph:
  requires: ["13-16"]
  provides:
    - "whitespace-vocabulary-derived body-boundary pattern (_next_top_level_pat) with three new (h1) arms"
    - "call-site census / entry-source lock locked as QUAL-01 doc-row tokens (tenth, eleventh)"
    - "DOCSTRING COUNT LOCK closing the negative-case-count drift channel"
  affects: ["scripts/check-traceability.py", "scripts/check-quality-harness.py", "CLAUDE.md", "docs/ARCHITECTURE.md"]
tech-stack:
  added: []
  patterns:
    - "derive a boundary/comparison pattern from an existing pattern's own vocabulary rather than restating it as a literal"
    - "runtime docstring self-inspection (inspect.getdoc) compared against the same live registries the code floor uses, to close a three-surface drift channel"
key-files:
  created: []
  modified:
    - scripts/check-traceability.py
    - scripts/check-quality-harness.py
    - CLAUDE.md
    - docs/ARCHITECTURE.md
decisions: []
metrics:
  duration: "~2.5 hours (agent wall-clock)"
  completed: 2026-09-03
---

# Phase 13 Plan 17: Close round-4 WARNINGs WR-01/WR-02 and correct both QUAL-01 doc rows against the final code state Summary

Derived `_next_top_level_pat`'s body-boundary pattern from `_SELFTEST_DISPATCHER_PAT`'s own
whitespace vocabulary (closing WR-01's multi-space/tab fail-opens), pinned plan 13-16's
three-helper call-site census and ENTRY-SOURCE LOCK as two new locked `| QUAL-01 |` doc-row
tokens (correcting the rows against what the code now actually does), and closed the
NEGATIVE-CASE COUNT FLOOR's docstring drift channel with a DOCSTRING COUNT LOCK that reads its
own docstring at runtime and compares both factors against the live registries (WR-02) — leaving
`FIREWALL: GREEN (23/23)` with the frozen `_chain_block_well_formed` byte-unchanged.

## What Was Built

**Task 1 — whitespace-vocabulary-derived body-boundary pattern (WR-01).**
`_next_top_level_pat` in `scripts/check-traceability.py` changed from the hardcoded literal
`^(?:async def |def |class |@)` (exactly one space) to
`^(?:(?:async\s+)?def\s|class\s|@)`, built from the SAME whitespace vocabulary
`_SELFTEST_DISPATCHER_PAT` uses, so the two patterns cannot disagree on whitespace by
construction. `_selftest_dispatch_problems`'s docstring paragraph stating the two-patterns
invariant was rewritten to state the property that now holds (shared whitespace vocabulary)
rather than the narrower single-space claim 13-15 established. Three new `(h1)` synthetic
control arms were added immediately after the existing ASYNC BODY-BOUNDARY / PLAIN-`def`
CONTRAST arms: MULTI-SPACE BOUNDARY, TAB BOUNDARY, and MULTI-SPACE DISPATCHER — each driving
`_selftest_dispatch_problems` with in-memory literals only and asserting exactly one problem
naming the anchor and `never called from self_test()`. The shared TRACE-03 sentence in both
`CLAUDE.md` and `docs/ARCHITECTURE.md` was amended (byte-identical in both files) so the
published closure claim now matches every whitespace rendering the dispatcher pattern accepts,
not only the canonical single-space one.

**Task 2 — pin the census and entry-source claims as locked doc-row tokens (R4-CR-01/R4-CR-02).**
Appended `call-site census` and `entry-source lock` (tenth and eleventh tokens, in that order)
to both `_QUAL01_DOC_ROW_TOKENS` and its second inline transcription
`expected_qual01_doc_row_tokens` in `scripts/check-quality-harness.py`. Moved control (m)'s
NEGATIVE-CASE COUNT FLOOR from 18 (2 doc rows x 9 tokens) to 22 (2 doc rows x 11 tokens),
re-derived live via `len(_QUAL01_DOC_ROWS) * len(_QUAL01_DOC_ROW_TOKENS)` rather than
transcribed. Both `| QUAL-01 |` rows (in `CLAUDE.md` and `docs/ARCHITECTURE.md`) were edited
identically, inside their shared byte-identical suffix, to: (1) name plan 13-16's extension of
control (t)'s call-site census to all three floor helpers with their landed per-helper counts;
(2) describe the ENTRY-SOURCE LOCK's re-derivation discipline; (3) correct the prior DISCLOSED
LIMITATIONS sentence, which said the dispatch-reachability entry's required side was "a locked
set rather than a derived one" — it is now a locked set with a second, independent
transcription in the entry-source lock, making narrowing it a two-place edit, with the
remaining EQUAL-value-rebind blind spot stated honestly; (4) add the census's own disclosed
bound (catches deletion of a real call, not discarding of its result).

**Task 3 — DOCSTRING COUNT LOCK closing the WR-02 drift channel.**
`_selftest_render_contract`'s docstring paragraph was corrected: the plan-by-plan token
enumeration now runs through 13-14's ninth token (worked-example conformance) and this plan's
tenth/eleventh (call-site census, entry-source lock, referred to by bare Python identifier with
no trailing paren per hard constraint 6), and the NEGATIVE-CASE COUNT FLOOR sentence now states
22 (2 doc rows x 11 tokens). A new `(m2) DOCSTRING COUNT LOCK` arm reads
`_selftest_render_contract`'s own docstring at runtime via `inspect.getdoc`, derives the
expected total from the same two live registries the floor uses, and asserts — with whitespace
normalized on both sides, since the sentence wraps across a line break — that the docstring's
sentence contains BOTH factors together (not only their product), so a partial fix is still
caught. On mismatch it reports both the docstring's actual (stale) transcription and the
live-derived value (added in a follow-up commit after MUTATION N7's first pass showed the
message named only the expected value, not the found one).

## Doc-Row Claims Added, Traced to Their Backing Arm/Mutation (13-16-SUMMARY.md)

| Claim added to both `\| QUAL-01 \|` rows | Backing arm | Backing mutation(s) in `13-16-SUMMARY.md` |
|---|---|---|
| Control (t)'s call-site census now covers all three floor helpers (coverage-floor-registry 6, worked-example-conformance 6, entry-source 5 call sites) | control (t) SCORING RECORDER LOCK, three new counters | M6 (leg 5 real call → `pass`, caught), M8 (control (x) THE FLOOR ITSELF → `pass`, caught), M9 (ENTRY-SOURCE LOCK real call → `pass`, caught); each with its anti-masking pair (counters removed → exit 0) |
| ENTRY-SOURCE LOCK re-derives each entry's required side at lock time and rejects a rebind to the entry's own actual side | control (x) ENTRY-SOURCE LOCK, isolation arms x6-x9 | M1 (arm 4a rebind + narrowing), M2 (rebind via a decoy local, not the registry binding), M3 (`ALIASED` — same object bound to both sides), M4/M5 (UNREGISTERED / MISSING ENTRY) |
| Dispatch-reachability entry's required side is a locked set with a second, independent transcription — narrowing it is a two-place edit; a same-VALUE rebind is still invisible | control (x)'s `"(u) dispatch-reachability symbol set"` registered entry | Same ENTRY-SOURCE LOCK mechanism as above (x6-x9); this entry's own value is exercised by the REGISTRY MEMBERSHIP LOCK's pre-existing coverage |
| The call-site census counts source text and observes no behaviour — it catches deletion of a call, not discarding of its result | control (t)'s own DISCLOSED LIMITATION | Stated as-is in `13-16-SUMMARY.md`'s Task 2 write-up (no code change needed, already true of the extended counters) |

## Mutations N1-N8 (verbatim)

All driven either directly against the pure function (N1-N3, no tree mutation needed) or on
`rsync -a --exclude .git --exclude .venv --exclude .planning` scratch copies — never the tracked
tree.

| Mutation | Command / edit | Result | Arm named |
|---|---|---|---|
| **N1** | `_selftest_dispatch_problems("_selftest_x", "def self_test():\n    pass\n\nasync  def other():\n    _selftest_x()\n", "f.py")` (two-space `async  def`), driven directly at HEAD (post-fix) | `["anchor '_selftest_x' is defined in 'f.py' but is never called from self_test() — ..."]` — exactly one problem | new MULTI-SPACE BOUNDARY arm |
| **N2** | Same with `def\tother():` (tab between `def` and name) | Exactly one problem, same shape | new TAB BOUNDARY arm |
| **N3** | Same with `async  def self_test():` (two-space) dispatcher and `async  def other():` (two-space) body-following construct | Exactly one problem, same shape | new MULTI-SPACE DISPATCHER arm |
| **N4 (anti-vacuity)** | Scratch copy: reverted `_next_top_level_pat` to its pre-plan literal `r"^(?:async def \|def \|class \|@)"`; ran `--self-test` | `EXIT=1`. `V825-ROWS FAIL: (h1) multi-space async body-boundary case failed: []`, `... tab body-boundary case failed: []`, `... multi-space dispatcher body-boundary case failed: []` — all three new arms failed by name; the two pre-existing arms (`async body-boundary leak case`, `plain-`def` body-boundary contrast case`) still PASSED | proves the three new arms, not a passive re-check, cover a rendering the old pattern did not |
| **N5a** | Scratch copy: deleted `entry-source lock` from `CLAUDE.md`'s `\| QUAL-01 \|` row only | `EXIT=1`. `self-test FAIL: render_contract (m) POSITIVE: CLAUDE.md: the '\| QUAL-01 \|' row is missing required token 'entry-source lock'` | control (m) POSITIVE |
| **N5b** | Scratch copy: deleted `call-site census` from `CLAUDE.md`'s row only | `EXIT=1`. Same shape, naming `CLAUDE.md` and `'call-site census'` | control (m) POSITIVE |
| **N5c** | Scratch copy: deleted `entry-source lock` from `docs/ARCHITECTURE.md`'s row only | `EXIT=1`. Same shape, naming `docs/ARCHITECTURE.md` and `'entry-source lock'` | control (m) POSITIVE |
| **N5d** | Scratch copy: deleted `call-site census` from `docs/ARCHITECTURE.md`'s row only | `EXIT=1`. Same shape, naming `docs/ARCHITECTURE.md` and `'call-site census'` | control (m) POSITIVE |
| **N6** | Scratch copy: dropped `entry-source lock` from `_QUAL01_DOC_ROW_TOKENS` only (both doc rows and the second transcription `expected_qual01_doc_row_tokens` left intact) | `EXIT=1`. `self-test FAIL: render_contract (h) MEMBERSHIP LOCK: qual01_doc_row_tokens: (...10 entries...) != expected (...11 entries...)`, plus `(m) NEGATIVE-CASE COUNT FLOOR: derived 20 ... != expected 22` (both fired) | (h) MEMBERSHIP LOCK naming `qual01_doc_row_tokens` |
| **N7** | Scratch copy: left the inline NEGATIVE-CASE COUNT FLOOR at 18 after the token additions (i.e. reverted only the `!= 22` check back to `!= 18` and its message) | `EXIT=1`. `self-test FAIL: render_contract (m) NEGATIVE-CASE COUNT FLOOR: derived 22 (file, token) case(s) from 2 doc row(s) x 11 token(s) != expected 18` | control (m) NEGATIVE-CASE COUNT FLOOR |
| **N7 (docstring form)** | Separate scratch copy: reverted ONLY the docstring's stated sentence to `16 (2 doc rows x 8 tokens)`, code floor left correct at 22/11 | `EXIT=1`. `self-test FAIL: render_contract (m2) DOCSTRING COUNT LOCK: the docstring's transcription reads 'derives the expected 16 (2 doc rows x 8 tokens)' but the live registries derive 'derives the expected 22 (2 doc rows x 11 tokens)' — ...` | new (m2) DOCSTRING COUNT LOCK |
| **N8** | Same scratch family: docstring perturbed to `22 (2 doc rows x 10 tokens)` — total (22) left "correct", only the token-count factor wrong | `EXIT=1`. `self-test FAIL: render_contract (m2) DOCSTRING COUNT LOCK: the docstring's transcription reads 'derives the expected 22 (2 doc rows x 10 tokens)' but the live registries derive 'derives the expected 22 (2 doc rows x 11 tokens)' — ...` | new (m2) DOCSTRING COUNT LOCK — proves BOTH factors are asserted, not only the product |
| **ANTI-VACUITY** | Same scratch copy as N7 (docstring form): removed the entire `(m2) DOCSTRING COUNT LOCK` block, re-ran `--self-test` with the stale docstring (16/8) still in place | `EXIT=0`. `self-test: render_contract sub-check PASSED` | confirms the (m2) arm alone is what catches N7/N8 — removing it lets the stale docstring pass silently |

## Shared-Suffix Byte-Identity (hard constraint 3)

Measured via longest-common-suffix comparison from the anchor
`). As of Phase 11 (CONTRACT-03/CONTRACT-05)` to end of the `\| QUAL-01 \|` row line, in both
`CLAUDE.md` and `docs/ARCHITECTURE.md`:

- **Before this plan's doc-row edits:** 8,619 bytes, identical in both files.
- **After Task 1's TRACE-03 edit (different row, unaffected):** unchanged, still 8,619.
- **After Task 2's `\| QUAL-01 \|` row edits:** 10,738 bytes, identical in both files (verified by
  direct Python string comparison, not by eye).

The amended TRACE-03 sentence (Task 1) was independently verified byte-identical between
`CLAUDE.md` and `docs/ARCHITECTURE.md` by direct substring-presence check on both files.

## Three Agreeing Count Values (Task 3)

- Docstring's stated total (after correction): **22 (2 doc rows x 11 tokens)**.
- Control (m)'s inline NEGATIVE-CASE COUNT FLOOR value: **22**.
- `len(_QUAL01_DOC_ROWS) * len(_QUAL01_DOC_ROW_TOKENS)` computed live from the constants:
  **2 * 11 = 22**.

All three agree; the new DOCSTRING COUNT LOCK asserts the first against the third at self-test
time.

## `_chain_block_well_formed` Byte-Identity Evidence

- Function range at HEAD: lines **4277-4397** (`def _chain_block_well_formed` at 4277; next
  `def _chain_detector_source` at 4400) — unchanged from the plan's starting commit `9789b8f`.
- `git diff 9789b8f HEAD -- scripts/check-quality-harness.py` hunk headers:
  `@@ -7395,6 +7395,8 @@`, `@@ -7821,6 +7823,8 @@`, `@@ -9401,9 +9405,24 @@`,
  `@@ -11838,19 +11857,70 @@` — none overlaps 4277-4397, and
  `git diff 9789b8f HEAD -- scripts/check-quality-harness.py | grep -c _CHAIN_DETECTOR_PINNED_DIGEST`
  returns **0**.
- `python3 scripts/check-quality-harness.py --self-test`: `chain_detector_pin` sub-check PASSED.

## Verification Results (real tree, HEAD, no mutation)

1. `python3 scripts/check-quality-harness.py --self-test` — **EXIT 0**, `render_contract
   sub-check PASSED`, `chain_detector_pin sub-check PASSED`.
2. `python3 scripts/check-traceability.py --self-test` — **EXIT 0**; live headline:
   `published headline == 175 reproducible / 91 audit-only / 0 gap / 266 total` — unchanged.
3. `python3 scripts/sync-content.py --check` — **EXIT 0**, no drift (this plan touched no
   `shared/` file; both edited scripts and both edited docs are outside `shared/`).
4. `bash scripts/check-firewall-battery.sh` — final line **`FIREWALL: GREEN (23/23)`**, EXIT 0.
   (`.venv` did not exist in this fresh worktree checkout; ran `uv sync` first, creating it with
   pytest 9.1.1, matching plan 13-16's documented resolution — `.venv` is gitignored.)
5. `git status --porcelain` — empty before the first mutation and after the last, for every
   mutation round (N4; N5a-d; N6; N7/N7-docstring/N8/anti-vacuity) — all mutation work ran on
   `rsync`-excluded scratch copies under the session scratchpad, cleaned up after each round.
6. `git diff --stat 9789b8f HEAD` lists exactly the plan's four `files_modified`:
   `CLAUDE.md`, `docs/ARCHITECTURE.md`, `scripts/check-quality-harness.py`,
   `scripts/check-traceability.py`.

## Deviations from Plan

**1. [Rule 1 - Bug] Follow-up fix to the DOCSTRING COUNT LOCK's own failure message.**
- **Found during:** Task 3, running MUTATION N7 against the newly-added `(m2)` arm.
- **Issue:** The arm's first version reported only the expected (derived) sentence on mismatch,
  not what the docstring actually said — the plan's acceptance criteria for N7 require the
  failure line to name "the docstring transcription, the found value and the derived value."
- **Fix:** Added a regex extraction of the docstring's actual `derives the expected N (R doc
  rows x T tokens)` sentence and included it in the `_fail` message alongside the derived value.
- **Files modified:** `scripts/check-quality-harness.py`.
- **Verification:** Re-ran MUTATION N7 and N8 on fresh scratch copies; both failure lines now
  name both the found (stale) and derived (live) sentences. Re-ran the real-tree self-test —
  still `render_contract sub-check PASSED`.
- **Committed in:** `331c08d` (separate commit, immediately after `e0741f6`).

---

**Total deviations:** 1 auto-fixed (1 bug).
**Impact on plan:** Necessary to meet Task 3's own acceptance criteria for MUTATION N7's failure
message; no scope creep — same arm, same file, same task.

## Issues Encountered

The worktree's base commit initially resolved to an ancestor (`d4da381`, pre-Phase-13) rather
than the expected `9789b8f` (post-13-16) — the `worktree_branch_check` step's merge-base
comparison caught this and `git reset --hard 9789b8f` corrected it before any plan work began.
Not a plan deviation; standard worktree-setup housekeeping.

## Self-Check: PASSED

- `scripts/check-traceability.py` — FOUND (modified, Task 1 commit present).
- `scripts/check-quality-harness.py` — FOUND (modified, Task 2/3 commits present).
- `CLAUDE.md`, `docs/ARCHITECTURE.md` — FOUND (modified, Task 1 and Task 2 commits present).
- Commit `ee2fd5b` (Task 1) — FOUND in `git log --oneline`.
- Commit `5dd1eee` (Task 2) — FOUND in `git log --oneline`.
- Commit `e0741f6` (Task 3) — FOUND in `git log --oneline`.
- Commit `331c08d` (Task 3 follow-up fix) — FOUND in `git log --oneline`.
- `python3 scripts/check-quality-harness.py --self-test` — re-run at HEAD, EXIT 0, confirmed.
- `python3 scripts/check-traceability.py --self-test` — re-run at HEAD, EXIT 0, headline
  `175/91/0/266`, confirmed.
- `bash scripts/check-firewall-battery.sh` — re-run at HEAD, `FIREWALL: GREEN (23/23)`,
  confirmed.
- `git status --porcelain` on the real tree — empty, confirmed.
