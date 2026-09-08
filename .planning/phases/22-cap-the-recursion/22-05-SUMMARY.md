---
phase: 22-cap-the-recursion
plan: 05
subsystem: apparatus
tags: [product-findings, 999-31, deferred-ledger, honesty-not-score]
dependency_graph:
  requires:
    - "22-04 — closed CR-05; left the deferred-literal ledger at 152 entries, both guards repinned fresh"
  provides:
    - "scripts/check-selfaudit-scan.py — corrected multi-literal census (11 constructs, not 9), _VALIDATE_LEG_SYMBOLS named as its exception, zip comment matches the plain zip call"
    - "scripts/gen-gate-docs.py — one deferred-literal ledger key re-adjudicated by hand, both guards repinned fresh"
  affects:
    - "22-08 (records 999.31 items 1 and 2 closed; exit count 2 for the product-tier backlog moves toward 0)"
tech_stack:
  added: []
  patterns:
    - "narrow a false published claim to its measured reach, rather than adding a lock or control to make it true (D-01 depth rule, this plan's own worked example)"
    - "re-derive a count by independent enumeration, never by transcribing a prior MEDIUM-confidence recount (999.31 item 1's own defect class)"
    - "keep a ledger entry's correct backlog-id classification even when hand-adjudicating its reason, and disclose the resulting partial-adjudication exception in the class-level comment rather than silently mismatching it"
key_files:
  created: []
  modified:
    - scripts/check-selfaudit-scan.py
    - scripts/gen-gate-docs.py
decisions:
  - "The re-derived census counts 11 multi-literal constructs, not the research's own MEDIUM-confidence hypothesis of 10 — _VALIDATE_LEG_SYMBOLS is folded into the docstring's own stated scope ('every construct in this file'), not left as a separate unenumerated finding beside the total"
  - "The one deferred-literal ledger key affected by the docstring edit keeps backlog id 999.41 (the correct classification for a .py module docstring hit) rather than being assigned a new hand-adjudication id — its written reason was upgraded from the mechanical placeholder to a real one, and the class-level comment above the ledger dict now discloses this one exception so the 'without per-entry adjudication' claim stays honest"
  - "_VALIDATE_LEG_SYMBOLS_LOCK was deliberately not added — 999.30 item 1's closed-by-decision disposition is left standing; adding the lock here would make the census claim true by extending the depth rule's recursion in the very phase that writes the rule down"
metrics:
  duration: "~70 minutes"
  completed: 2026-09-08
---

# Phase 22 Plan 05: Close 999.31 Items 1 and 2 Summary

Closed the two product-tier findings in `scripts/check-selfaudit-scan.py` that a reader outside
the build loop could not audit without re-deriving them independently: the multi-literal census
published as "nine found in total ... no named exceptions" (999.31 item 1), and a comment
claiming a `zip(..., strict=True)` call the code does not make (999.31 item 2). Both fixes narrow
the published claim to its measured reach; neither adds a lock, a control, or a gate. The deferred-
literal ledger key the docstring edit moved was re-adjudicated by hand and both its guards
repinned fresh; the battery confirmed `FIREWALL: GREEN (26/26)` afterward.

## What Was Built

**Task 1 — corrected the `zip(strict=True)` comment.** The comment near the Rubric-11 loop
(`~line 2749`) claimed the loop was driven `via zip(..., strict=True)`, but the actual call
(`~line 2769`, unchanged) is plain `zip(_BAND_BULLETS, _BAND_NAMES)` — contradicting the file's
own correct disclosures at lines 221 and 570 that `strict=True` was deliberately rejected because
it makes the LENGTHENING direction fail-open. Replacement text:

> `_BAND_BULLETS` literal, driven from the tuple ITSELF via a plain
> `zip` over `_BAND_BULLETS` and `_BAND_NAMES` rather than a hand-written
> four-literal list — deliberately NOT `strict=True`: that would turn
> a length-mismatched pair into a loud `ValueError` instead of a
> silently-uncovered branch, which makes the LENGTHENING direction
> fail-open (see bound (11) above). The verifier reproduced live that
> narrowing `_BAND_BULLETS` from four literals to one ...

The call itself and the branch roster are byte-unchanged. One acceptance-criterion adjustment: the
plan's Task 1 acceptance expected `grep -c "zip(_BAND_BULLETS, _BAND_NAMES)"` to print exactly `1`
after the fix. Measured baseline (pre-plan, `git show HEAD`) was actually **3**, not 1 — the exact
literal string `zip(_BAND_BULLETS, _BAND_NAMES)` already appears twice in existing correct prose
(lines 221 and 570) in addition to the one real call. The replacement comment was worded to avoid
introducing a fourth occurrence of that literal string (`a plain \`zip\` over \`_BAND_BULLETS\` and
\`_BAND_NAMES\`` rather than restating the parenthesized call form), so the count stayed at the
pre-existing baseline of 3 rather than rising to 4. This is a stale premise in the plan's own
acceptance text, not a live discrepancy in the tree — documented under Deviations below.

**Task 2 — re-derived the multi-literal census by enumeration.** Read every candidate construct
named in the research's own hypothesis, plus a broader sweep (`for ... in (`, `for ... in _[A-Z]`,
`zip(` across the whole file) to confirm nothing was missed. Full roster:

| Line(s) | Construct | Form | One arm per literal? |
|---|---|---|---|
| 1243, 1251, 2769 | `_BAND_BULLETS` (module-level 4-tuple) | Iterated at `Rubric-11`'s two production sites (`_check_rubric_text`, crit4/crit6 slices) and by the self-test's own `zip(_BAND_BULLETS, _BAND_NAMES)` generator | **YES** — the generator emits 8 mutually-discriminating ids (`R-11-bands-crit{4,6}-{rigorous,sound,handwavy,absent}`), one per literal per criterion slice |
| 956 | Body-7 | `for lit in (_BODY_ROWRULE_CHAIN, _BODY_ROWRULE_CLAIM)` | YES — `B-07-rowrule-chain`/`B-07-rowrule-claim`, two hand-written self-test arms |
| 975 | Body-10 | `for lit in (_BODY_LEDGER_INDEP_1, _BODY_LEDGER_INDEP_2)` | YES — `B-10-ledger-indep-1`/`-2` |
| 986 | Body-11 | `lit for lit in (_BODY_RECON_LEAD, _BODY_RECON_TEMPLATE) if not _contains(...)` | YES — `B-11-recon-lead`/`-template` |
| 996 | Body-12 | `lit for lit in (_BODY_PLACEMENT_1, _BODY_PLACEMENT_2) if not _contains(...)` | YES — `B-12-placement-1`/`-2` |
| 1124 | Rubric-3 | `for lit in (_RUBRIC_DIVLABOUR_1, _RUBRIC_DIVLABOUR_2)` | YES — `R-03-divlabour-1`/`-2` |
| 1146 | Rubric-5 | `lit for lit in (_COLS_CHAIN, _COLS_CLAIM) if not _contains(...)` | YES — `R-05-cols-chain`/`-claim` |
| 1338 | Rubric-13 region loop | `for region_name, region_text, detail_prefix in (("TEMPLATE", ...), ("ADMISSION", ...))` | YES — jointly covered, with the nested clause loop below, by 8 ids (`R-13-format-{template,admission}-{c2,c46}-{dup,missing}`) |
| 1342 | Rubric-13 clause loop (nested inside 1338) | `for clause_name, clause_literal in (("Criteria-4/6", ...), ("Criterion-2", ...))` | YES — same 8 ids as above |
| 1426 | Cross-1 (X-01) | `for col_name, col_literal in (("chain-form...", _COLS_CHAIN), ("claim-inventory...", _COLS_CLAIM))` | YES — `X-01-cols-{chain,claim}-{body,rubric}`, 4 ids |
| 1515, 3505, 1795/3739 | `_VALIDATE_LEG_SYMBOLS` (module-level 4-tuple) | `for _leg_symbol in _VALIDATE_LEG_SYMBOLS:` (validate-census live check) and a dict-comprehension usage in `describe()`-consistency | **NO** — both usages collapse to a single aggregate pass/fail message (`_validate_census_ok` boolean; dict-equality), with no per-leg id and no membership lock |

**Total: 11 constructs, 10 compliant, 1 exception (`_VALIDATE_LEG_SYMBOLS`).**

How this differs from the research's own hypothesis (`22-RESEARCH.md` Assumptions Log A2, MEDIUM
confidence, "9 inline + `_BAND_BULLETS` zip = 10 total"): the research's 10 already correctly
split `Rubric-13`'s region loop (line 1338) and clause loop (line 1342) into two constructs rather
than one — kept unchanged here, confirmed independently. What the research's "10" did **not**
fold in was `_VALIDATE_LEG_SYMBOLS` itself: it flagged `_VALIDATE_LEG_SYMBOLS` as a separate
HIGH-confidence "undisclosed exception" claim, but did not add it to the arithmetic total. Since
the docstring's own claim is scoped to "every construct in this file" (not "every construct in the
three checks"), and the task instruction explicitly named `_VALIDATE_LEG_SYMBOLS` as a construct
to include, this enumeration folds it into the total: **9 inline tuples + `_BAND_BULLETS` +
`_VALIDATE_LEG_SYMBOLS` = 11**, kept, dropped, or added exactly as follows relative to the
research's candidate list: all 9 of the research's line numbers (956, 975, 986, 996, 1124, 1146,
1338, 1342, 1426) kept unchanged; `_BAND_BULLETS` kept as one entry despite 3 separate iteration
sites (matching the original docstring's own precedent of counting a named tuple once regardless
of how many places it is iterated); `_VALIDATE_LEG_SYMBOLS` added as an 11th entry, the one named
exception.

Replacement docstring paragraph (verbatim, `~lines 226-247`):

> A census of every construct in this file where a check iterates over more than one
> literal, re-derived by direct enumeration against the live file (not
> transcribed from any prior count) on 2026-09-08: eleven found in
> total — `_BAND_BULLETS` (iterated at `Rubric-11`'s two production
> sites, `~lines 1243` and `~1251`, and by this `zip` generator), nine
> inline `for … in (…)` tuples across the body, rubric and cross-surface
> checks (`Rubric-13`'s region-split loop and its nested clause loop
> count as two separate constructs, not one, since each iterates its own
> tuple independently), and `_VALIDATE_LEG_SYMBOLS` (`~line 1515`). Ten
> of the eleven carry one hand-written arm per literal.
> `_VALIDATE_LEG_SYMBOLS` is a NAMED EXCEPTION: a four-literal tuple
> driving the `validate-census` check (`~line 3505`) through a single
> aggregate pass/fail message with no per-leg id and no membership
> lock — the same shape backlog 999.30 item 1 records, closed-by-decision
> under the depth rule (`docs/PROCESS.md` §1) rather than fixed here,
> because adding the missing lock or a per-leg arm to make this census
> claim true would extend the very recursion the depth rule exists to
> stop. The published "every multi-literal tuple has one arm per
> literal" claim therefore holds for ten of the file's eleven
> multi-literal constructs, with `_VALIDATE_LEG_SYMBOLS` the one
> deliberately unclosed, named exception — a measured bound, not an
> unconditional universal.

No lock, control, or gate was added (`_VALIDATE_LEG_SYMBOLS_LOCK` deliberately absent from the
diff, verified below); `--self-test` still reports "All 100 branches covered", `--describe` still
reports `branch_count` 100 and `control_count` 12 — unchanged, per the acceptance criteria.

**Task 3 — re-adjudicated the moved ledger key, regenerated, re-gated.** `python3
scripts/gen-gate-docs.py --check` (before this task's own fix) reported the expected stale-ledger
finding: the `'literal (nine'` key on `scripts/check-selfaudit-scan.py#__doc__` no longer matched
any live hit, and a new non-exempt hit appeared for `'check (\`~line 3505\`)'` (a source-line
citation the replacement text introduced, adjacent to the word "check"). Ran
`--emit-deferred-ledger`, diffed its 152-entry output against the live 152-entry
`_DEFERRED_LITERAL_HITS` dict programmatically (not by eye): confirmed exactly one key removed,
one key added, and the other 151 keys unchanged in occurrence/backlog-id shape (only their reason
text reverted to the emitter's `TODO` placeholder, as expected — restored from the pre-emission
dict). Merged: the 151 unaffected keys' existing written reasons were preserved byte-for-byte
(programmatically verified, not eyeballed); the one new key was hand-adjudicated with a
NOT-A-COUNT reason rather than left as the emitted placeholder:

> `NOT-A-COUNT: '~line 3505' is a source-line citation pointing at the validate-census check's
> call site (scripts/check-selfaudit-scan.py:3505 as of 2026-09-08), from the multi-literal census
> re-derivation this plan's docstring paragraph records for 999.31 item 1 -- the adjacency
> heuristic attaches the digit to the word 'check' as though it counted something, but it names a
> line number, not a population.`

**Backlog-id decision:** the new key kept backlog id `999.41` — the correct classification for a
`.py` module docstring hit — rather than being assigned a new hand-adjudication id (999.42 is
scoped by the emitter's own function to `CLAUDE.md`/`docs/ARCHITECTURE.md`/`docs/TESTING.md` only;
999.44 to `docs/README.md` only; reusing either for this relpath would repeat exactly the
false-label-via-default problem D-22-D exists to avoid). Because the class-level comment above the
ledger dict states all 999.41 entries are "pinned MECHANICALLY ... without per-entry adjudication,"
and this one entry now has a real, hand-written reason, the comment was updated to disclose the
single exception by name (Rule 1 — the class-level claim was made imprecise by this task's own
edit; not touching it would leave the guard's own documentation stating something the guard's own
state now contradicts, the exact CR-05 defect shape this phase exists to end).

| Guard | Before this plan | After |
|---|---|---|
| `_DEFERRED_LEDGER_MAX` | 152 | **152** (unchanged — one key removed, one added, net zero) |
| `_DEFERRED_LEDGER_KEYS_DIGEST` | `sha256:3ba9791b998420e5e6b1bb8e660e136198d2d636075bd1ec03902f006f29009f` | **`sha256:bf71a11703d09210a274702b9c19db8b3665ddcedcc46836b39b7ed91aa14c74`** |

Full diff of ledger dict entries (programmatic diff, not eyeballed):

```
-    ('scripts/check-selfaudit-scan.py#__doc__', 'literal (nine'): ('999.41', 1, 'Pinned mechanically ...'),
+    ('scripts/check-selfaudit-scan.py#__doc__', 'check (`~line 3505`)'): ('999.41', 1, "NOT-A-COUNT: '~line 3505' is a source-line citation ... (2026-09-08) ..."),
```

Ran `--write` (34 files regenerated, only `scripts/gen-gate-docs.py` carrying a real diff —
`CLAUDE.md` and `docs/ARCHITECTURE.md` regenerated byte-identical, since neither's generated fence
renders the literal-scan ledger facts by value), `--self-test` (74 controls, PASS), `--check`
(exit 0), both pre-commit hooks (`.githooks/pre-commit` and `scripts/git-hooks/pre-commit`, both
exit 0), and `python3 scripts/check-selfaudit-scan.py --self-test` (exit 0, 100 branches). `git
diff scripts/check-quality-harness.py` confirmed empty — the three CONTRACT-06 sha256 pins are
byte-unchanged. `bash scripts/check-firewall-battery.sh` printed `FIREWALL: GREEN (26/26)`.

**`--describe` readings, before/after (this plan's own commits):**

| Measurement | Value |
|---|---|
| `check-selfaudit-scan.py --describe` `branch_count` | 100 (unchanged) |
| `check-selfaudit-scan.py --describe` `control_count` | 12 (unchanged) |
| `gen-gate-docs.py --describe` `control_count` | 74 |
| `gen-gate-docs.py --describe` `registered_surfaces` | 37 |
| `gen-gate-docs.py --describe` `literal_scan_non_exempt` | 0 |
| `gen-gate-docs.py --describe` `literal_scan_ledger_entries` | 152 (== `literal_scan_ledger_max`) |
| `gen-gate-docs.py --describe` `literal_scan_hits` | 179 (unchanged from end of wave 4) |
| `gen-gate-docs.py --describe` `literal_scan_ledger_adjudicated` | 38 (unchanged — the new key kept backlog id 999.41, so it is not counted as hand-adjudicated by this computation; a disclosed, deliberate imprecision, not a bug) |
| `gen-gate-docs.py --describe` `literal_scan_ledger_mechanical` | 114 (unchanged, same reason) |

## Deviations from Plan

### Documented pre-existing discrepancy — Task 1's acceptance-criteria baseline (not a live bug)

Task 1's acceptance criteria expected `grep -c "zip(_BAND_BULLETS, _BAND_NAMES)"` to read exactly
`1` after the fix, implying a pre-change baseline of 1. The measured pre-change baseline
(`git show HEAD:scripts/check-selfaudit-scan.py | grep -c ...`) is actually **3**: the literal
string already appears twice in the file's own correct disclosures (lines 221, 570) in addition to
the one real call. The replacement comment text was worded to avoid restating that literal
parenthesized form, keeping the post-change count at 3 (matching the true baseline, not the plan's
assumed baseline of 1) rather than rising to 4. The call itself, verified separately, is
byte-unchanged. Logged as a stale premise in the plan text, not fixed (out of scope to edit the
plan), and worked around by wording rather than by literal count.

### Documented pre-existing discrepancy — one `TODO: written reason` match survives (not caused by this plan)

Verification item 7 measures `1`, not `0`. The one match is `emit_deferred_ledger()`'s own
output-template string (`'"TODO: written reason"),'` at `~line 2607`) — the maintenance harness's
boilerplate for whoever next runs `--emit-deferred-ledger`, not a leftover placeholder inside an
actual `_DEFERRED_LITERAL_HITS` entry. Confirmed by parsing the dict body's own literal source
range and checking the substring is absent there (0 occurrences) — the same condition
`22-03-SUMMARY.md` and `22-04-SUMMARY.md` already documented for the identical reason. Editing
`emit_deferred_ledger()`'s template string is out of this plan's `<action>` and its `read_first`
list — logged, not fixed, per SCOPE BOUNDARY.

### Rule 1 fix — class-level ledger comment's "without per-entry adjudication" claim (in `scripts/gen-gate-docs.py`, Task 3's own file)

Directly caused by this task's own edit: hand-adjudicating one 999.41 key's written reason made
the class-level comment above `_DEFERRED_LITERAL_HITS` ("remaining ... entries ... are pinned
MECHANICALLY ... without per-entry adjudication") imprecise for that one entry. Corrected in place
by naming the single exception, rather than left standing as a guard's own documentation
contradicting the guard's own state — the same discipline CR-05/22-04 established for the
"ratchets down, never up" claim.

No other deviations. All three tasks' `<action>` and `<acceptance_criteria>` items were executed
and independently re-verified on the live tree.

## Verification

All 14 plan-level `<verification>` items re-run on the live tree, in order:

1. `grep -c "nine found in total" scripts/check-selfaudit-scan.py` → **0** (baseline 1)
2. `grep -c "no named exceptions" scripts/check-selfaudit-scan.py` → **0**
3. `grep -c "999.30" scripts/check-selfaudit-scan.py` → **1** (at least 1 required)
4. `git diff <base>..HEAD -- scripts/check-selfaudit-scan.py | grep -cE "_VALIDATE_LEG_SYMBOLS_LOCK|^\+def _control_|zip\(.*strict=True\)"` → **0**
5. `grep -c "'literal (nine'" scripts/gen-gate-docs.py` → **0**
6. `grep -c "'eight arms'" scripts/gen-gate-docs.py` → **1**
7. `grep -c "TODO: written reason" scripts/gen-gate-docs.py` → **1** — see documented pre-existing discrepancy above (the maintenance-harness template string, not a ledger placeholder)
8. `python3 scripts/check-selfaudit-scan.py --self-test` → exit **0**, "All 100 branches covered"
9. `python3 scripts/check-selfaudit-scan.py --describe` → `branch_count` **100**, `control_count` **12**
10. `python3 scripts/gen-gate-docs.py --self-test` → exit **0**; `--check` → exit **0**
11. `python3 scripts/gen-gate-docs.py --describe` → `control_count` **74**, `registered_surfaces` **37**, `literal_scan_non_exempt` **0**
12. `git diff scripts/check-quality-harness.py` → **empty**
13. `sh .githooks/pre-commit` → exit **0**; `sh scripts/git-hooks/pre-commit` → exit **0**
14. `bash scripts/check-firewall-battery.sh` → **FIREWALL: GREEN**, total **26**

## Issues Encountered

None beyond the two documented pre-existing discrepancies above and the one in-scope Rule 1 fix
documented under Deviations.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- 999.31 items 1 and 2 are closed: the multi-literal census is re-derived by enumeration (11
  constructs, 10 compliant, `_VALIDATE_LEG_SYMBOLS` the one named exception citing 999.30 item 1's
  closed-by-decision disposition), and the `zip` comment matches the plain `zip` call.
- 999.30 in full and 999.31 item 3 remain apparatus, closed-by-decision — untouched by this plan,
  reserved for plan 22-08's terminal-disposition recording.
- 999.31 item 4 (the "eight not-found reporting arms" undercount) is untouched — reserved for plan
  22-06, including its own `'eight arms'` ledger key, confirmed still present and unmodified.
- The deferred-literal ledger stands at 152 entries (net unchanged — one key swapped for another),
  `_DEFERRED_LEDGER_KEYS_DIGEST` repinned fresh to reflect the swapped key set.
- Battery confirmed `FIREWALL: GREEN (26/26)` on the full tree with this plan's three commits
  applied; both `.githooks/pre-commit` and `scripts/git-hooks/pre-commit` exit 0.
- No blockers for downstream plans in this phase.

## Self-Check: PASSED

- `[ -f scripts/check-selfaudit-scan.py ]` → FOUND (modified)
- `[ -f scripts/gen-gate-docs.py ]` → FOUND (modified)
- `git log --oneline --all | grep -q 40b358f` → FOUND (Task 1 commit)
- `git log --oneline --all | grep -q 5d5d00e` → FOUND (Task 2 commit)
- `git log --oneline --all | grep -q a06b99a` → FOUND (Task 3 commit)
- All plan-level `<verification>` commands re-run above with observed (not assumed) output,
  including `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (26/26)`.

---
*Phase: 22-cap-the-recursion*
*Completed: 2026-09-08*
