---
phase: 21-generate-the-claim-surface
plan: 21
subsystem: claim-surface-verification-harness
tags: [gate-registry, self-test, hook-roster, clause-splitting, rework-cap]
dependency_graph:
  requires: []
  provides:
    - "scripts/_gate_registry.py::_hook_roster_arm_clauses"
    - "scripts/_gate_registry.py::cr04-hook-roster-arm-shape-guard control"
  affects:
    - "scripts/_gate_registry.py"
    - "scripts/gen-gate-docs.py (census population, read-only in this plan)"
tech_stack:
  added: []
  patterns:
    - "clause-splitting parser ported from check-version-stamps.py's _roster_arm_clauses idiom, adapted for a list-of-separate-entries message grammar instead of one joined string"
key_files:
  created: []
  modified:
    - "scripts/_gate_registry.py"
decisions:
  - "Task 2 (planning-record edits to .planning/STATE.md, .planning/ROADMAP.md, .planning/phases/21-generate-the-claim-surface/21-CONTEXT.md) is NOT applied inside this isolated worktree — see Deviations below for the full reasoning and the drafted content ready for direct application."
metrics:
  duration: "~1 session"
  completed: "2026-09-07"
---

# Phase 21 Plan 21: Registry Hook-Roster Clause Extraction + Rework-Cap Record Summary

One-liner: Ported the `_roster_arm_clauses` clause-splitting idiom into `scripts/_gate_registry.py`
as `_hook_roster_arm_clauses`, closing CR-01's code half (the two arms at lines 1212/1229 that
asserted a bare `"missing="`/`"extra="` substring against a whole message rather than an extracted
clause), with a new message-shape guard control and five falsification arms proving the fix is
structural, not accidental.

## What Was Built

### Task 1 — `_hook_roster_arm_clauses` and the rewritten hook-roster arms (COMPLETE, verified)

- Added three shared module-level constants beside `_HOOK_PATHS`:
  `_HOOK_DIVERGENCE_PREFIX = "hook-divergence: "`,
  `_HOOK_ROSTER_MISSING_PREFIX = "hook-roster missing=: "`,
  `_HOOK_ROSTER_EXTRA_PREFIX = "hook-roster extra=: "`.
- `hook_roster_problems()`'s three `problems.append()` calls now build their messages by
  concatenating the shared prefix constant with the same remainder text as before — a
  message-CONSTRUCTION change only. Verified byte-identical below.
- Added `_hook_roster_arm_clauses(problems: list[str]) -> tuple[str, str]` immediately after
  `hook_roster_problems`, with four raising legs: (1) every entry must start with one of the three
  recognised prefixes, (2) no entry may carry both the `missing=` and `extra=` markers (checked via
  a `not in` precondition, never the bare `"missing=" in <identifier>` shape the CONF-13 census
  forbids), (3) no prefix may appear on more than one entry, (4) otherwise return
  `(missing_clause, extra_clause)`.
- Rewrote all three negative arms
  (`_control_cr04_hook_roster_missing_fires`, `_control_cr04_hook_roster_extra_fires`,
  `_control_cr04_hook_roster_divergence_fires`) to call the helper and assert against extracted
  clauses, each with an empty-opposite-clause assertion that a polarity swap cannot satisfy.
- Added `_control_cr04_hook_roster_arm_shape_guard`, registered in both `_CONTROLS` and
  `_CONTROL_IDS`, asserting the helper raises `ValueError` on (a) a both-markers entry (built by
  concatenating the two prefix constants across multiple physical source lines, per the
  self-match defence `_control_roster_arm_shape_census_vacuity` documents), (b) an unrecognised
  prefix, (c) two entries sharing the same prefix — plus the empty-list and well-formed-list
  return-value checks.
- Updated `_control_cr04_hook_roster_live_positive`'s docstring to name the helper as the parser
  its sibling arms now use.

### Task 2 — rework-cap exception record + STATE.md position refresh (NOT APPLIED — see Deviations)

The plan-drafted content for `.planning/phases/21-generate-the-claim-surface/21-CONTEXT.md`,
`.planning/ROADMAP.md` and `.planning/STATE.md` is fully worked out below under Deviations, ready
for direct application to the real `.planning/` tree. It was not applied inside this isolated
worktree; see the reasoning there.

## Evidence

### Before/after `SELF-TEST PASS` lines

- Before: `_gate_registry: SELF-TEST PASS — 20 controls run`
- After: `_gate_registry: SELF-TEST PASS — 21 controls run`

### `/usr/bin/grep -n '"missing=" in \|"extra=" in ' scripts/_gate_registry.py`

- Before: 2 lines —
  ```
  1212:    assert "missing=" in problems[0], problems
  1229:    assert "extra=" in problems[0], problems
  ```
- After: 0 lines (command run, empty output, exit 1/no-match confirmed).

  One transient regression during editing: my own new docstring initially contained the literal
  phrase `` `"missing=" in <identifier>` `` as prose explaining the forbidden shape, which the exact
  acceptance-criteria grep (looking for the raw substring, not the census's stricter identifier-only
  regex) also matched. Caught immediately by re-running the grep, reworded to
  `` `in`-membership-against-a-whole-message shape `` with no quoted `"missing=" in ` substring, and
  reconfirmed 0 lines. Recorded here as the drafting process, not as a shipped defect — the commit
  contains only the corrected wording.

### In-process census over `scripts/_gate_registry.py`

Loaded `scripts/gen-gate-docs.py` in-process and called
`roster_arm_shape_census_problems(sources={"scripts/_gate_registry.py": <real source text>})`:

- Before: `['scripts/_gate_registry.py:1212: bare clause-marker membership test against a whole message: \'"missing=" in problems\'', 'scripts/_gate_registry.py:1229: bare clause-marker membership test against a whole message: \'"extra=" in problems\'']` (2 findings)
- After: `[]` (0 findings)

### `_hook_roster_arm_clauses` behavior

- `_hook_roster_arm_clauses([])` → `("", "")`
- On the real synthetic missing-only fixture (a synthetic sixth invocation appended to a copy of
  the real hook source), the offending command
  `python3 scripts/check-agent.py --self-test` lands in the first (missing) element and the second
  (extra) element is `""`.

### Positive arm and rendered-message byte-identity

Real-tree `hook_roster_problems()` returns `[]` both before and after (unchanged). The three
rendered finding messages, captured via synthetic fixtures before and after the edit, are
byte-identical:

**Missing** (before and after, identical):
```
["hook-roster missing=: hook gate(s) with no PRECOMMIT: registry row: ['python3 scripts/check-agent.py --self-test']"]
```

**Extra** (before and after, identical):
```
["hook-roster extra=: PRECOMMIT: registry row(s) naming an invocation neither hook makes: ['python3 scripts/check-links.py --check']"]
```

**Divergence** (before and after, identical):
```
["hook-divergence: the two hook scripts' derived invocation sequences differ: ['python3 scripts/sync-content.py --check', 'python3 scripts/report-conformance.py --self-test'] != ['python3 scripts/sync-content.py --check', 'python3 scripts/report-conformance.py --check']"]
```

Confirmed programmatically (`missing_problems == before_missing`, etc.) — all three `True`.

### Registered-and-executed

`cr04-hook-roster-arm-shape-guard` appears in both `_CONTROLS` and `_CONTROL_IDS`.
`SELF-TEST PASS` line rose by exactly 1: 20 → 21 controls run.

### Five falsification arms

All five were run on disposable `rsync -a --exclude .git` scratch copies taken from a
`git status --porcelain`-clean real tree (confirmed empty before and after every single
falsification, listed individually below). Task 1's commit (`29891ef`) landed before any
falsification ran, so "real tree clean" is checked against the committed, fixed state throughout.

**Falsification 1 — the verifier's exact exploit (combined `missing=`/`extra=` message).**
Mutation: replaced the two separate `problems.append()` calls with one joined
`f"hook-roster missing={sorted(missing)} extra={sorted(extra)}"` entry (the shape
`self_test()`'s own coverage-floor message already uses).
Result: `python3 scripts/_gate_registry.py --self-test` exited **1**, stderr:
```
_gate_registry: SELF-TEST FAIL [cr04-hook-roster-missing-fires] — ValueError: _hook_roster_arm_clauses: entry does not start with a recognised prefix: "hook-roster missing=['python3 scripts/check-agent.py --self-test'] extra=[]"
_gate_registry: SELF-TEST FAIL [cr04-hook-roster-extra-fires] — ValueError: _hook_roster_arm_clauses: entry does not start with a recognised prefix: "hook-roster missing=[] extra=['python3 scripts/check-links.py --check']"
```
Both `cr04-hook-roster-missing-fires` and `cr04-hook-roster-extra-fires` named, as required.
Real tree `git status --porcelain`: empty before, empty after.

**Falsification 2 — polarity swap.**
Mutation: in the two negative-arm control functions, swapped which clause each asserts against
(missing arm now asserts against `extra_clause`, extra arm now asserts against `missing_clause`).
Result: exited **1**, stderr:
```
_gate_registry: SELF-TEST FAIL [cr04-hook-roster-missing-fires] — ["hook-roster missing=: hook gate(s) with no PRECOMMIT: registry row: ['python3 scripts/check-agent.py --self-test']"]
_gate_registry: SELF-TEST FAIL [cr04-hook-roster-extra-fires] — ["hook-roster extra=: PRECOMMIT: registry row(s) naming an invocation neither hook makes: ['python3 scripts/check-links.py --check']"]
```
Both arms named. Real tree `git status --porcelain`: empty before, empty after.

**Falsification 3 — combined message AND polarity swap together.**
Mutation: both falsification 1 and falsification 2 mutations applied to the same scratch copy.
Result: exited **1**, stderr:
```
_gate_registry: SELF-TEST FAIL [cr04-hook-roster-missing-fires] — ValueError: _hook_roster_arm_clauses: entry does not start with a recognised prefix: "hook-roster missing=['python3 scripts/check-agent.py --self-test'] extra=[]"
_gate_registry: SELF-TEST FAIL [cr04-hook-roster-extra-fires] — ValueError: _hook_roster_arm_clauses: entry does not start with a recognised prefix: "hook-roster missing=[] extra=['python3 scripts/check-links.py --check']"
```
Both arms named. Real tree `git status --porcelain`: empty before, empty after.

**Falsification 4 — grammar drift surfaces loudly, not silently.**
Mutation: renamed the missing-clause prefix inside `hook_roster_problems`'s append call only
(from the `_HOOK_ROSTER_MISSING_PREFIX` constant to a hardcoded `"hook-roster missing2=: "`
literal), leaving `_hook_roster_arm_clauses`'s constant reference untouched — simulating an edit
to the producer that the parser was not updated to match.
Result: exited **1**, stderr:
```
_gate_registry: SELF-TEST FAIL [cr04-hook-roster-missing-fires] — ValueError: _hook_roster_arm_clauses: entry does not start with a recognised prefix: "hook-roster missing2=: hook gate(s) with no PRECOMMIT: registry row: ['python3 scripts/check-agent.py --self-test']"
```
`ValueError` raised naming the exact offending text, proving the helper raises rather than
degrading to whole-message blindness. Real tree `git status --porcelain`: empty before, empty
after.

**Falsification 5 — the guard control is not vacuous.**
Mutation: neutered leg 2 of `_hook_roster_arm_clauses` (removed the `not in` precondition guarding
against both-markers entries, so a combined-marker entry now parses instead of raising).
Result: exited **1**, stderr:
```
_gate_registry: SELF-TEST FAIL [cr04-hook-roster-arm-shape-guard] — _hook_roster_arm_clauses accepted an entry carrying both roster clause markers
```
`cr04-hook-roster-arm-shape-guard` named, as required. Real tree `git status --porcelain`: empty
before, empty after.

### Invariance checks (run after Task 1's commit, real tree)

- `python3 scripts/gen-gate-docs.py --self-test` — `gen-gate-docs: SELF-TEST PASS — 69 controls run`
  (unchanged from before this plan). Exit 0.
- `python3 scripts/gen-gate-docs.py --check` — `harvested 22/22 expected script-backed entries
  (22 total)`, exit 0, zero `DRIFT:` lines.
- `python3 scripts/check-registration.py` — `check-registration: PASS (discovered 14 skills, agent
  present, manifest parsed, 14/14 names verified, 23/24 battery gates CI-registered + 1
  battery-only by design)`, exit 0.
- `sh .githooks/pre-commit` — exit 0.
- `sh scripts/git-hooks/pre-commit` — exit 0.
- `bash scripts/check-firewall-battery.sh` — `FIREWALL: GREEN (26/26)`, reported as an invariance
  check, not as evidence the defect is closed (the battery was GREEN throughout the defective
  state, per the plan's own framing).
- `git diff --stat scripts/check-quality-harness.py` — empty. `check-quality-harness.py` carries
  no hunk in this plan's diff; all three CONTRACT-06 sha256 pins are untouched by construction.
- `git status --short` after commit — empty (no untracked files, no accidental deletions;
  `git diff --diff-filter=D --name-only HEAD~1 HEAD` returned nothing).

Commit: `29891ef` — `feat(21-21): assert hook-roster arms against extracted clauses, not whole messages`

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 — blocking, self-caught mid-edit] My own new docstring text tripped the exact
acceptance-criteria grep it was documenting the ban of.**
- **Found during:** Task 1, immediately after writing `_hook_roster_arm_clauses`'s docstring.
- **Issue:** The docstring's leg-2 explanation quoted the forbidden shape literally
  (`` `"missing=" in <identifier>` ``), which matched
  `/usr/bin/grep -n '"missing=" in \|"extra=" in ' scripts/_gate_registry.py` — the plan's own
  acceptance-criteria command — even though it did not match the stricter CONF-13 census regex
  (which requires the substring to be followed by a bare identifier, and `<identifier>` starts
  with `<`, not a letter).
- **Fix:** Reworded to `` `in`-membership-against-a-whole-message shape `` with no quoted
  `"missing=" in ` substring anywhere in the file. Re-ran the grep and the census; both clean.
- **Files modified:** `scripts/_gate_registry.py` (docstring wording only).
- **Commit:** `29891ef` (folded into the single Task 1 commit; no separate commit was made for
  this self-correction since it was caught before staging).

### Not Applied — Task 2 (planning-record edits)

**Task 2's target files — `.planning/STATE.md`, `.planning/ROADMAP.md`, and
`.planning/phases/21-generate-the-claim-surface/21-CONTEXT.md` — were not edited inside this
worktree.** This is a genuine GSD-mechanics conflict between the plan and the worktree-isolation
protocol governing this execution, resolved here rather than by silently skipping or blocking on
a checkpoint (it is a process/mechanics question, not a product or strategy call):

1. **This isolated worktree's `.planning/` tree does not contain these files at all.** Only
   `.planning/phases/*/*-SUMMARY.md` and `.planning/phases/21-generate-the-claim-surface/21-CONF13-BASELINE.md`
   are present (the force-tracked exception to the project's blanket `.planning/` gitignore, per
   `CLAUDE.md`'s "Planning artifacts" constraint and the `planning-summaries-force-tracked` memory
   note). `.planning/STATE.md`, `.planning/ROADMAP.md` and
   `.planning/phases/21-generate-the-claim-surface/21-CONTEXT.md` are gitignored and were never
   copied into this worktree's checkout.
2. **The orchestrator's own governing instructions for this run are explicit:** "Do NOT update
   STATE.md or ROADMAP.md — the orchestrator owns those writes after all worktree agents in the
   wave complete," and "Do NOT modify STATE.md or ROADMAP.md. execute-plan.md auto-detects
   worktree mode ... and skips shared file updates automatically. The orchestrator updates them
   centrally after merge."
3. **Even a same-worktree edit to `21-CONTEXT.md` would not persist.** It is gitignored (unlike
   `*-SUMMARY.md`), so an edit made inside this worktree and committed on the worktree branch would
   not survive a normal `git` merge back to the main tree — only force-tracked files do. Writing it
   here would be theater, not a real record.

Given this, the substantive intellectual work of Task 2 — drafting the exact exception-record
text, the `ROADMAP.md` paragraph replacement, and the `STATE.md` position refresh — is done in
full below, ready for direct, mechanical application to the real `.planning/` tree by the
orchestrator or a human operator working outside worktree isolation. **This is the one part of the
plan not independently verified by running a command against the real files**, because those files
do not exist in this execution context; the acceptance criteria naming exact `grep` counts against
the real tree (`.planning/STATE.md`, `.planning/ROADMAP.md`) could not be run here and are not
claimed as passing.

#### Drafted content for `.planning/phases/21-generate-the-claim-surface/21-CONTEXT.md`

Insert immediately after the existing round-1 `RECORDED EXCEPTION — 2026-09-07` block (which stays
byte-unchanged), inside the `<domain>` section:

> **RECORDED EXCEPTION — 2026-09-07 (rounds 2 and 3): the cap is exceeded again — 4 + 3 = 7 more
> gap-closure plans (21-17..21-20, 21-21..21-23), running total 11 against a stated cap of 2.**
>
> *What happened.* Round 2 was plans 21-17..21-20, four gap-closure plans against
> `21-VERIFICATION.md` round 1's three blocking gaps, executed with no exception recorded at the
> time — a fact discovered by the round-2 verifier, not self-reported
> (`21-VERIFICATION.md`'s `process_finding`, round 2, 2026-09-07T20:00:00Z: "searched
> `21-CONTEXT.md`, `21-DISCUSSION-LOG.md` and `STATE.md` and found no second exception recorded for
> this round"). Round 3 is plans 21-21, 21-22 and 21-23: two against the single blocking gap CR-01
> that round 2's own closure apparatus opened (`roster_arm_shape_census_problems`'s population
> structurally excludes `scripts/_gate_registry.py` itself, so the exact defective roster-arm shape
> the census exists to eliminate survived undetected inside the file that defines the census), and
> a third added at plan-checking time, when the same structural defect was found live one
> requirement over: `_py_docstring_scan_scripts()` derives CONF-13's literal-scan population from
> the identical `_expected_harvest_scripts()` set that caused CR-01, so the same seven `.py` files
> — `scripts/_gate_registry.py` among them — are invisible to CONF-13's standing scanner too.
> Measured during that check: widening that population surfaces exactly four non-exempt
> hand-maintained count literals, all four in `scripts/_gate_registry.py`'s own module docstring.
> **Running total: 4 (round 1) + 4 (round 2) + 3 (round 3) = 11 gap-closure plans in Phase 21
> against a stated cap of 2.** Round 3 alone (3 plans) exceeds the cap on its own.
>
> *Why the exception rather than honouring the cap.* Round 2's four plans closed three
> independently-verified blocking gaps and were verified (`21-VERIFICATION.md` round 2,
> `gaps_closed`) to have closed them genuinely; the omission was of the RECORD, not of the
> deliberation — and an undocumented breach is worse than a documented one precisely because it
> cannot be reviewed. Round 3 was planned at two plans, inside the cap, and grew to three when
> plan-checking found the CONF-13 twin of CR-01 live on the tree. Recorded honestly: the third plan
> is not scope creep and not a fourth round of point-fixing — it closes a confirmed live instance
> of the same defect class, found BEFORE execution rather than after, and closing it now is what
> prevents a round 4. The verifier's own alternative — treating 21-13..21-23 as one continuous
> eleven-plan gap-closure effort rather than three capped rounds — is arguably the more honest
> framing of what actually happened (one root defect class, discovered and chased across three
> verification cycles); this entry adopts the three-round framing because that is how the work was
> actually planned and verified in sequence (each round's verifier evaluated a discrete plan set
> against a discrete gap list), but states the running total (11) explicitly so a reader is not
> misled by counting per round.
>
> *What this costs, stated plainly.* The cap is NOT amended; it stands at 2 for every other phase
> in this milestone, and Phase 19's "cap of 2 now spent" accounting is unaffected. A cap that has
> been exceeded three times in one phase without halting the phase is evidence about the cap's
> design, not only about this phase's discipline: a cap stated as a per-phase plan count cannot
> tell round 1 of a genuine multi-gap closure from round 4 of point-fixing, and it did not fire at
> all when round 2 breached it silently, because nothing mechanically checks that the exception
> record exists.
>
> *Downstream.* Phase 22 (CONF-15) formally writes the cap. Extend the round-1 entry's downstream
> note: Phase 22 must read BOTH this entry and the round-1 entry before writing the cap, and must
> additionally address that (a) a per-phase plan count could not distinguish round 1 of a
> three-gap closure from round 4 of point-fixes, and (b) the record can be silently skipped, as
> round 2 demonstrated, because nothing outside the record itself checks that it exists.

#### Drafted replacement paragraph for `.planning/ROADMAP.md` (currently lines 143-147)

Current text (verbatim, to be replaced):
> *One recorded exception to (2), Phase 21, 2026-09-07:* four gap-closure plans (21-13..21-16) were
> authorised by developer decision against three blocking verification gaps sharing one root cause,
> with the reasoning and its cost written into
> `.planning/phases/21-generate-the-claim-surface/21-CONTEXT.md`.
> The cap itself is unamended and stands at 2 everywhere else; Phase 19's "cap of 2 now spent"
> accounting is unaffected. Phase 22 must read that entry before writing the cap down.

Drafted replacement:
> *Three recorded exceptions to (2), Phase 21, 2026-09-07:* round 1 (plans 21-13..21-16, 4 plans),
> round 2 (plans 21-17..21-20, 4 plans; its exception was recorded retroactively at round 3, after
> the round-2 verifier found none written at the time), and round 3 (plans 21-21..21-23, 3 plans,
> itself exceeding the cap). Running total: 11 gap-closure plans against a stated cap of 2. Full
> reasoning in `.planning/phases/21-generate-the-claim-surface/21-CONTEXT.md`'s two
> `RECORDED EXCEPTION` entries. The cap itself is unamended and stands at 2 everywhere else;
> Phase 19's "cap of 2 now spent" accounting is unaffected. Phase 22 must read both entries before
> writing the cap down.

#### Drafted update for `.planning/ROADMAP.md`'s Phase 21 checklist line (currently line 165)

Current text (verbatim):
> `- [ ] **Phase 21: Generate the Claim Surface** - eliminate hand-transcribed gate documentation
> (20/20 plans executed; round-2 verification 2026-09-07 — 3/4 must-haves, all three round-1 gaps
> CLOSED, 1 NEW blocking gap CR-01 opened by round 2's own deliverable; see 21-VERIFICATION.md)`

Drafted replacement parenthetical (apply after 21-21/21-22/21-23 actually land; this plan alone
does not close CR-01's other half or the CONF-13 twin, so the checklist line should not be marked
closed until 21-22 and 21-23 also land — the orchestrator should re-check `21-VERIFICATION.md`'s
status before finalizing this line's wording):
> `(23/23 plans executed across 3 gap-closure rounds — round 3, plans 21-21..21-23, closes CR-01's
> code half plus the CONF-13 twin found at plan-checking time; see 21-VERIFICATION.md and
> 21-CONTEXT.md's round-2/3 RECORDED EXCEPTION entry)`

#### Drafted update for `.planning/STATE.md`

Derived counts (commands run against the real `.planning/` tree, 2026-09-07, before this plan's
own `21-21-PLAN.md`/`21-21-SUMMARY.md` are accounted for on that tree):
```
$ ls .planning/phases/21-generate-the-claim-surface/21-*-PLAN.md | wc -l
23
$ ls .planning/phases/21-generate-the-claim-surface/21-*-SUMMARY.md | wc -l
20
```
So the phase currently has 23 planned plans and 20 completed (with 21-21, this plan, completing a
21st once its own SUMMARY lands on the real tree — the orchestrator should re-run both commands
after merge to confirm 21/23 before writing the position).

- Replace the stale `## Current Position` block's `Plan: 1 of 16` line with the measured count
  (re-derive at apply time; do not hand-type).
- Set "Resume file" to `.planning/phases/21-generate-the-claim-surface/21-21-PLAN.md` (or the next
  unexecuted plan, 21-22, once this plan has landed).
- Set status to round-3 gap closure, naming the blocking gap CR-01 (code half closed by this plan;
  population-widening half is plan 21-22) and the CONF-13 twin plan 21-23 closes.
- Add a round-3 planning note naming the 21-21 → 21-22 → 21-23 ordering hazard: widening either
  population before fixing the source it will newly see turns `gen-gate-docs.py --self-test` and
  `--check` RED on the live tree (per `21-21-PLAN.md`'s own objective section), and the phase
  invariants all three plans assert (battery total stays 26, no new battery gate, no new CI job, no
  REG-GUARD exemptions, all three CONTRACT-06 sha256 pins byte-unchanged — all confirmed for this
  plan above).
- Update frontmatter `last_activity` and `last_updated` to reflect this plan's completion, and
  reconcile `total_plans`/`completed_plans` against the derived counts rather than the current
  hand-typed values (current frontmatter reads `total_plans: 55, completed_plans: 52` at the
  milestone level, which is a different axis than the phase-level `Plan: 1 of 16` figure being
  corrected here — the orchestrator should confirm which axis each field tracks before editing).
- Add a one-line pointer to the new `21-CONTEXT.md` round-2/3 exception entry, mirroring the
  existing `REWORK-CAP EXCEPTION (developer decision, 2026-09-07)` note already in `STATE.md`.

## Self-Check

- `[ -f scripts/_gate_registry.py ]` → FOUND
- `git log --oneline --all | grep -q 29891ef` → FOUND (commit `29891ef` present in worktree branch
  history)
- `.planning/STATE.md`, `.planning/ROADMAP.md`,
  `.planning/phases/21-generate-the-claim-surface/21-CONTEXT.md` — NOT checked against the real
  tree; not edited in this worktree, per the Deviations section above. Their drafted replacement
  content is stated above for direct application.

## Self-Check: PASSED (Task 1); Task 2 explicitly deferred to post-merge application, documented above rather than silently skipped

## Verification Summary

- `python3 scripts/_gate_registry.py --self-test` — exit 0, `SELF-TEST PASS — 21 controls run`
  (was 20). Verified by running the command, not by inspection.
- `/usr/bin/grep -c '"missing=" in \|"extra=" in ' scripts/_gate_registry.py` — 0 (was 2).
- In-process `roster_arm_shape_census_problems` over the real `scripts/_gate_registry.py` text —
  `[]` (was 2 findings).
- `python3 scripts/gen-gate-docs.py --self-test` — exit 0, 69 controls (unchanged).
- `python3 scripts/gen-gate-docs.py --check` — exit 0, `harvested 22/22`, zero `DRIFT:` lines.
- `python3 scripts/check-registration.py` — exit 0, PASS.
- `sh .githooks/pre-commit` and `sh scripts/git-hooks/pre-commit` — both exit 0.
- `bash scripts/check-firewall-battery.sh` — `FIREWALL: GREEN (26/26)`.
- Five falsification arms, each with exact exit code (all 1) and stderr text recorded above; real
  tree `git status --porcelain` confirmed empty before and after each.
- Task 2's acceptance criteria (`grep` counts and cross-surface figure agreement against
  `.planning/STATE.md`/`.planning/ROADMAP.md`/`21-CONTEXT.md`) were **not** run — those files are
  absent from this isolated worktree and out of scope per the orchestrator's explicit instruction.
  Drafted content is provided above in place of a passing verification claim.
