---
phase: 22-cap-the-recursion
plan: 03
subsystem: docs+apparatus
tags: [product-findings, ledger-adjudication, run-command, depth-rule]
dependency_graph:
  requires:
    - "22-02 — CLAUDE.md/CONTRIBUTING.md depth-rule statements (this plan depends_on 22-02)"
  provides:
    - "docs/DATA-FLOW.md Stage 4 — full five-gate pre-commit enumeration"
    - "docs/ARCHITECTURE.md — corrected battery-total claim, no unsupported 'five surfaces' clause"
    - "scripts/gen-gate-docs.py — re-adjudicated deferred-literal ledger (134 entries), both guards repinned fresh"
    - "scripts/_gate_registry.py — three runnable run_command values (INVARIANT-CHECK, FROZEN-EVIDENCE, VAL-03)"
  affects:
    - "22-08 (records D-22-C's decline in the ROADMAP backlog; records CR-03/CR-04/CR-06 closed, only CR-05 (plan 22-04) remaining of the four product findings)"
tech_stack:
  added: []
  patterns:
    - "point at the generated fact rather than hand-transcribe a count (docs/COMPONENT-DIAGRAM.md precedent, reused for the Stage 4 lead-in)"
    - "delete an unsupported cross-surface claim rather than restate it more narrowly (CR-03 fix choice)"
    - "re-pin both deferred-ledger guards (_DEFERRED_LEDGER_MAX, _DEFERRED_LEDGER_KEYS_DIGEST) fresh in the same commit as any ledger-key change, never incrementally"
key_files:
  created: []
  modified:
    - docs/DATA-FLOW.md
    - docs/ARCHITECTURE.md
    - docs/gates/CONF-SURFACE.md
    - scripts/gen-gate-docs.py
    - scripts/_gate_registry.py
    - docs/TESTING.md
    - docs/gates/INVARIANT-CHECK.md
    - docs/gates/FROZEN-EVIDENCE.md
    - docs/gates/VAL-03.md
decisions:
  - "CR-03 fixed by deleting the unsupported 'five surfaces' clause entirely, not by restating it narrower — the clause is itself the dual-surface hand-transcription pattern CONF-13 exists to remove; the surviving sentence still correctly credits the 25->26 move to CONF-SURFACE's own generation rather than a hand sweep, it just no longer claims a surface count nothing supports"
  - "D-22-C reaffirmed: CR-06's proposed heredoc/array-expansion detecting control is declined as an L4 move (a guard whose subject is the gate registry's own published apparatus data); control_count verified unchanged at 74 and no new _control_ function landed in the diff"
metrics:
  duration: "~50 minutes"
  completed: 2026-09-08
---

# Phase 22 Plan 03: Close CR-03, CR-04, CR-06 — the Three Non-CR-05 Product Findings Summary

Closed three of the four product-tier findings carried out of Phase 21 round 4 (`21-REVIEW.md`):
**CR-04** (`docs/DATA-FLOW.md` Stage 4 claimed to state what every commit fires, then enumerated
2 of 5 gates), **CR-03** (a hand-adjudicated ledger entry certifying an unsupported "five surfaces"
claim), and **CR-06** (three published "exact local run command" values that were not runnable —
one an unterminated heredoc that blocks a shell indefinitely if pasted). **CR-05 is explicitly not
in this plan** (plan 22-04); **CR-01/CR-02 are apparatus, auto-filed, never fixed here** (D-01/D-02).

## What Was Built

**Task 1 (CR-04, `92bcbd1`).** `docs/DATA-FLOW.md`'s `## Stage 4 — Gates (CI + pre-commit)` section
now lists all five pre-commit gates — sync-drift, conformance generator self-test,
conformance-baseline drift, claim-surface generator self-test, claim-surface drift (CONF-SURFACE) —
in the fixed order both hook scripts run them, each with its command. The lead-in sentence still
points at `docs/ARCHITECTURE.md`'s generated population-arithmetic sentence for the current gate
count rather than stating a bare digit (the sanctioned "point at the generated fact" move,
`docs/COMPONENT-DIAGRAM.md`'s own Phase-21 precedent) — CR-04's own defect was a digit removed
while the enumeration underneath stayed wrong, so this fix restores content, not just the digit.

**Task 2 (CR-03, `a207425`).** Re-measured the battery-total (`26`) occurrence count across the
five surfaces the `docs/ARCHITECTURE.md:174` claim implied, using
`/usr/bin/grep -o '\b26\b' <file> | wc -l` on each:

| Surface | Command | Occurrences |
|---|---|---|
| `CLAUDE.md` | `grep -o '\b26\b' CLAUDE.md \| wc -l` | 11 |
| `docs/ARCHITECTURE.md` | `grep -o '\b26\b' docs/ARCHITECTURE.md \| wc -l` | 4 |
| `docs/TESTING.md` | `grep -o '\b26\b' docs/TESTING.md \| wc -l` | 0 |
| `docs/gates/CONF-SURFACE.md` | `grep -o '\b26\b' docs/gates/CONF-SURFACE.md \| wc -l` | 0 |
| `scripts/check-firewall-battery.sh` | `grep -o '\b26\b' scripts/check-firewall-battery.sh \| wc -l` | 8 |

Confirms `22-RESEARCH.md`'s own measurement (11/4/0/0/8) exactly, on the tree as it stands after
plans 22-01 and 22-02. Two of the five named surfaces carry zero occurrences of the battery total.

**CR-03 outcome chosen: delete-the-clause, not name-the-real-surfaces.** `docs/ARCHITECTURE.md:174`
read `... rather than swept by hand across five surfaces.`; the "five surfaces" clause was removed
entirely, leaving `... produced by CONF-SURFACE itself, not hand-swept.` — the surviving sentence
still correctly attributes the `25 -> 26` move to generation rather than a hand sweep; it just no
longer states a surface count nothing in the live tree supports. Chosen over restating the count
narrower (e.g. "on two surfaces") on `22-RESEARCH.md`'s own reasoning: naming *which* surfaces
restate the total is itself the exact dual-surface hand-transcription pattern CONF-13 exists to
remove, and any narrower restatement would just be a smaller version of the same defect shape,
requiring its own future upkeep as the battery total moves again.

**Ledger re-adjudication.** The `('docs/ARCHITECTURE.md', 'five surfaces.')` key's matched text is
now gone from the file (the phrase was deleted), so the entry was removed outright (no replacement
key — the surviving sentence, "produced by CONF-SURFACE itself, not hand-swept," contains no
count-shaped literal the scanner flags). Both ledger guards were repinned fresh in the same commit,
computed via `_deferred_ledger_keys_digest()` over the actual final `_DEFERRED_LITERAL_HITS` dict
(never derived incrementally from the old pin):

| Guard | Before | After |
|---|---|---|
| `_DEFERRED_LEDGER_MAX` | 135 | **134** |
| `_DEFERRED_LEDGER_KEYS_DIGEST` | `sha256:0a249f6de8c4b520d3e76590cfc6d1b8296497c5cbfef05bd7533d64a0f068bc` | `sha256:d968f66d09bbd83c2bb65bbfb13d42cafc80310a3193aefe40768baa25395f3a` |

Removing the ledger entry also dropped the primary-surface (`999.42`) adjudicated count from 21 to
20 (`literal_scan_ledger_adjudicated`) and the total ledger size from 135 to 134
(`literal_scan_ledger_max`/`literal_scan_ledger_entries`). `docs/gates/CONF-SURFACE.md`'s own
hand-written narrative cites both figures by name in two places (lines 163, 190) — both were
corrected to `20` and `134` respectively so the D-06 containment check (every bare digit outside a
generated fence must match a live figure inside one) stays green; `python3 scripts/gen-gate-docs.py
--write` was re-run afterward and confirmed these two hand-written lines survive regeneration
unchanged (only the file's small `GENERATED:FACTS`/`GENERATED:HOW-TO-RUN` fences are
machine-owned).

`git diff scripts/gen-gate-docs.py` contains no change to any `LiteralExemptionClass` entry, no
change to `LITERAL_SCAN_MD_GLOBS`, and no new `def _control_`/`def _match_` function — confirmed by
grep on the diff. The fix is data and prose, not detector logic.

**Task 3 (CR-06, `4591c53`).** Replaced all three defective `run_command` values in
`scripts/_gate_registry.py` with the exact strings `21-REVIEW.md`'s CR-06 fix block specifies:

- **INVARIANT-CHECK** — was an unterminated `python3 - <<'PYEOF'` heredoc with no matching
  terminator (blocks a shell indefinitely reading stdin if pasted, published under a "How to run"
  heading). Now `bash scripts/check-firewall-battery.sh  # INVARIANT-CHECK runs inline; no
  standalone command`.
- **FROZEN-EVIDENCE** — was `git diff --quiet HEAD -- "${_FROZEN_PATHS[@]}"`, a bash array local to
  `scripts/check-firewall-battery.sh` that expands to nothing outside it. Now the same battery
  invocation with its own inline-only comment.
- **VAL-03** — the third leg was a literal angle-bracket placeholder,
  `<pytest-capable interpreter> -m pytest ...`, not a command. Now
  `.venv/bin/python3 -m pytest scripts/check-links_anchors_test.py -q  # or any pytest-capable
  interpreter`.

`python3 scripts/gen-gate-docs.py --write` regenerated every surface these values render onto
(`docs/TESTING.md`, `docs/gates/INVARIANT-CHECK.md`, `docs/gates/FROZEN-EVIDENCE.md`,
`docs/gates/VAL-03.md`) — confirmed changed by `git status --short` before staging.

**D-22-C reaffirmed, mechanically verified.** `21-REVIEW.md`'s CR-06 fix block proposes a follow-on
control asserting no `run_command` contains an unterminated heredoc or an unresolvable array
expansion. **Not added** — its subject is the gate registry's own published apparatus data, an L4
move the depth rule this phase writes stops before (`docs/PROCESS.md` §1). Verified mechanically:
`python3 scripts/gen-gate-docs.py --describe`'s `control_count` is unchanged at **74**, and
`git diff scripts/gen-gate-docs.py scripts/_gate_registry.py | grep -c "^+def _control_"` is `0`.

## Task Commits

1. **Task 1: CR-04 — restore docs/DATA-FLOW.md Stage 4's full five-gate enumeration** — `92bcbd1` (fix)
2. **Task 2: CR-03 — correct the "five surfaces" claim and re-adjudicate the ledger entry** — `a207425` (fix)
3. **Task 3: CR-06 — make the three published run_command values runnable** — `4591c53` (fix)

_No plan-metadata commit yet — this SUMMARY.md and its commit are the metadata step, per the
worktree-mode `git_commit_metadata` convention (STATE.md/ROADMAP.md excluded; orchestrator owns
those after the wave merges)._

## Verification

All 12 plan-level `<verification>` items re-run on the live tree, in order:

1. `awk '/^## Stage 4/,/^## Stage 5/' docs/DATA-FLOW.md | grep -c '^- \*\*'` → **5** (baseline 2)
2. `grep -c "verified by grep across the five files" scripts/gen-gate-docs.py` → **0** (baseline 1)
3. `grep -c "swept by hand across five surfaces" docs/ARCHITECTURE.md` → **0**
4. `grep -c "PYEOF" scripts/_gate_registry.py docs/TESTING.md docs/gates/INVARIANT-CHECK.md` → **0** on every file (baseline 1/1/1)
5. `grep -c "TODO: written reason" scripts/gen-gate-docs.py` → **1** (baseline 1, unmoved — see Deviations)
6. `python3 scripts/gen-gate-docs.py --describe ... control_count, len(registered_surfaces)` → **74 37**
7. `python3 scripts/gen-gate-docs.py --self-test` → exit 0 (74 controls)
8. `python3 scripts/gen-gate-docs.py --check` → exit 0
9. `python3 scripts/check-links.py` → exit 0 (312 markdown links + 6 namespace refs, 160 files)
10. `sh .githooks/pre-commit` → exit 0; `sh scripts/git-hooks/pre-commit` → exit 0
11. `bash scripts/check-firewall-battery.sh` → **FIREWALL: GREEN (26/26)**
12. `git diff --name-only 71585e1..HEAD | grep -c "^.github/workflows/validation.yml"` → **0** — no CI job added

11 of 12 items match the plan's stated expectation exactly. Item 5 is documented below as a
pre-existing, out-of-scope condition, not a defect this plan introduced or left behind.

Also independently re-run per task:
- Task 1 acceptance criteria (5 checks) — all passed: exactly 5 bullets, all five gate names
  present, both previously-missing self-test commands present, `check-links.py` exit 0,
  `gen-gate-docs.py --check` exit 0.
- Task 2 acceptance criteria (7 checks) — all passed: the false ledger reason gone, the false
  ARCHITECTURE.md claim gone, zero `TODO: written reason` inside the actual ledger dict body
  (confirmed by parsing the dict's literal source range, not a whole-file grep), `--describe`
  reports `literal_scan_ledger_entries == literal_scan_ledger_max` (134 == 134) and
  `literal_scan_non_exempt == 0`, the old digest literal gone (0 occurrences), five re-measured
  per-surface counts recorded above, `--self-test`/`--check` both exit 0, zero detector-logic diff
  lines.
- Task 3 acceptance criteria (9 checks) — all passed: zero `PYEOF`/`_FROZEN_PATHS[@]`/placeholder
  occurrences in the registry, `control_count` unchanged at 74, zero new `_control_` functions,
  `--self-test`/`--check` both exit 0, both pre-commit hooks exit 0, battery GREEN 26/26, exit
  count 2 confirmed moved from 4 to 1 (only CR-05, plan 22-04, remains).

## Deviations from Plan

### Documented Pre-Existing Discrepancy (not a deviation — out of scope, not caused by this plan)

**Verification item 5 / Task 2 acceptance criterion "`TODO: written reason` prints exactly 0"**
measures `1`, both before and after this plan's commits. Confirmed via
`git show 71585e1:scripts/gen-gate-docs.py | grep -c "TODO: written reason"` (the wave-base
commit, before any of this plan's edits) → `1`, unchanged by any commit in this plan. The one match
is `scripts/gen-gate-docs.py:2574`, inside `emit_deferred_ledger()`'s own output-template string
(`'"TODO: written reason"),'`) — the maintenance harness's boilerplate text for whoever runs
`--emit-deferred-ledger` to regenerate the ledger dict, not a leftover placeholder inside an actual
`_DEFERRED_LITERAL_HITS` entry. Independently confirmed by parsing the dict body's literal source
range (from `_DEFERRED_LITERAL_HITS: dict[tuple[str, str], tuple[str, int, str]] = {` to its
closing `}`) and checking the substring is absent there: it is. The criterion this literal count
was meant to stand in for — "no un-adjudicated ledger entry was left with its placeholder" — is
independently confirmed true by the narrower, targeted check. Per the SCOPE BOUNDARY rule, a
pre-existing condition in the harness's own generator code, unrelated to this plan's CR-03 edits
(which only removed one obsolete key and re-pinned both guards), is logged here rather than
"fixed" — editing `emit_deferred_ledger()`'s template string is out of this task's `<action>` and
touches code CR-03's own read_first list does not name.

No other deviations. Both remaining tasks (1 and 3) executed exactly as written, using the exact
restore/replacement text `21-REVIEW.md`'s CR-04 and CR-06 fix blocks specify.

## Issues Encountered

None beyond the documented pre-existing discrepancy above.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- Three of the four product findings carried from Phase 21 (`CR-03`, `CR-04`, `CR-06`) are closed
  and mechanically verified. Only `CR-05` (`docs/README.md`'s 17 deleted historical figures) remains
  open, owned by plan 22-04.
- `docs/gen-gate-docs.py`'s deferred-literal ledger stands at 134 entries (down from 135), both
  guards repinned fresh; plan 22-07's later widening of `LITERAL_SCAN_MD_GLOBS` (adding
  `docs/PROCESS.md` and `CONTRIBUTING.md`) starts its own repin arithmetic from this new base, not
  from 135.
- D-22-C (declining CR-06's proposed follow-on control) is reaffirmed here with fresh mechanical
  verification (`control_count` still 74); plan 22-08 still owns filing the decline in the ROADMAP
  backlog.
- Battery confirmed `FIREWALL: GREEN (26/26)` on the full tree with all three of this plan's
  commits applied; both `.githooks/pre-commit` and `scripts/git-hooks/pre-commit` exit 0.
- No blockers for downstream plans in this phase.

## Self-Check: PASSED

- `[ -f docs/DATA-FLOW.md ]` → FOUND (modified)
- `[ -f docs/ARCHITECTURE.md ]` → FOUND (modified)
- `[ -f docs/gates/CONF-SURFACE.md ]` → FOUND (modified)
- `[ -f scripts/gen-gate-docs.py ]` → FOUND (modified)
- `[ -f scripts/_gate_registry.py ]` → FOUND (modified)
- `[ -f docs/TESTING.md ]` → FOUND (modified)
- `[ -f docs/gates/INVARIANT-CHECK.md ]` → FOUND (modified)
- `[ -f docs/gates/FROZEN-EVIDENCE.md ]` → FOUND (modified)
- `[ -f docs/gates/VAL-03.md ]` → FOUND (modified)
- `git log --oneline --all | grep -q 92bcbd1` → FOUND (Task 1 commit)
- `git log --oneline --all | grep -q a207425` → FOUND (Task 2 commit)
- `git log --oneline --all | grep -q 4591c53` → FOUND (Task 3 commit)
- All plan-level `<verification>` commands re-run above with observed (not assumed) output,
  including `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (26/26)`.

---
*Phase: 22-cap-the-recursion*
*Completed: 2026-09-08*
