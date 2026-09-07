---
phase: 21-generate-the-claim-surface
plan: 12
subsystem: tooling
tags: [conf-11, conf-12, conf-13, phase-closure, d-07, requirements-amendment, mutation-proof, backlog-id-collision]
status: complete

# Dependency graph
requires:
  - phase: 21-generate-the-claim-surface
    plan: 11
    provides: "CONF-SURFACE registered as a battery gate, CI job and both
      pre-commit hooks; battery at GREEN 26/26."
provides:
  - "CONF-12 amended in .planning/REQUIREMENTS.md (D-07): the 2,000-character
    cell cap is removed and replaced, as the phase's driveable count, by
    CONF-13's non-exempt literal count and the gate registry's equality
    floor over gate ids. .planning/ROADMAP.md's Phase 21 success criterion 3
    and docs/gates/CONF-SURFACE.md's narrative both carry the same
    amendment so no surface is the stale copy."
  - "All five phase invariants asserted by command with recorded outputs:
    three CONTRACT-06 sha256 digests recomputed and matched byte-for-byte,
    _FROZEN_PATHS at 22 entries, _GATED_SURFACES the ordered 2-tuple, the
    coverage headline derived live and unmoved at
    192/94/0/286, and the battery total at 26 by call-site count."
  - "Eight mutation arms proved on rsync/git scratch copies: the drift gate
    fires on a hand-edited CLAUDE.md region and a hand-edited detail-page
    fence; a hand-written narrative paragraph survives --write byte-for-byte
    except the intended edit; CONF-13's scanner fires on a reintroduced
    literal; the registry equality floor fires on a deleted battery gate
    block (both gen-gate-docs.py --check and _gate_registry.py --self-test);
    D-04 fires on a narrowed consumes tuple; REG-GUARD fires on a removed CI
    job; the pre-commit hook blocks a drifted commit at the self-test gate."
  - "A genuine backlog-id collision found and fixed: plan 21-10's three
    CONF-13 deferred-remediation groups were filed under 999.32/999.33/
    999.34, which collide with three unrelated pre-existing backlog entries
    already using those ids (filed 2026-09-05). Renumbered to 999.40/
    999.41/999.42 in every shipped artifact and given real
    .planning/ROADMAP.md backlog rows."
affects: []

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "requirement amendment recorded in the requirement file itself with a
      dated, phase-attributed note (D-07's own precedent, declining
      20-D-08's in-plan-reinterpretation shape) — CONF-12's amendment lives
      in .planning/REQUIREMENTS.md, not scattered across plan prose."
    - "backlog id collisions are a real defect class, not just a bookkeeping
      nuisance — this phase's own closing plan found one between two
      different phases' deferred-item filings; the fix is renumbering plus
      a pointer note at the historical citation, not silently editing the
      historical SUMMARY that used the wrong id."

key-files:
  created: []
  modified:
    - .planning/REQUIREMENTS.md
    - .planning/ROADMAP.md
    - docs/gates/CONF-SURFACE.md
    - scripts/gen-gate-docs.py
    - .planning/phases/21-generate-the-claim-surface/21-CONF13-BASELINE.md

key-decisions:
  - "CONF-12's amendment avoids restating the original cap's exact wording
    ('no table cell exceeds 2,000 characters') verbatim in either
    REQUIREMENTS.md or ROADMAP.md, since the acceptance criteria requires
    that literal string to be absent — paraphrased the historical clause
    instead of quoting it, preserving the amendment's provenance without
    reintroducing the string being removed."
  - "docs/gates/CONF-SURFACE.md's new 'Requirement amendment' narrative
    avoids restating any bare-digit figure not already corroborated inside
    its own Facts fence (D-06 containment) — cites REQUIREMENTS.md and
    field names by reference rather than repeating numbers like the
    original 2,000-character cap or the pre-split cell sizes."
  - "The three CONF-13 deferred-remediation groups were renumbered
    999.32/999.33/999.34 -> 999.40/999.41/999.42 rather than left colliding
    with the pre-existing entries at those ids; 21-10-SUMMARY.md's own
    historical text was left unedited (force-tracked record of what that
    plan actually did) with a correction pointer added at
    21-CONF13-BASELINE.md instead."
  - "Task 2's invariant assertions produced no shipped-artifact changes, so
    no separate commit was made for it — its readings are recorded inline
    in this SUMMARY per the plan's own <files> tag for that task."

requirements-completed: [CONF-11, CONF-12, CONF-13]

# Metrics
duration: ~3h (single session)
completed: 2026-09-06
---

# Phase 21 Plan 12: Close Phase 21 — Amend CONF-12, Assert Invariants, Prove by Mutation Summary

**CONF-12 is amended in REQUIREMENTS.md (D-07) with its dated reason and replacement counts; all
five phase invariants are asserted mechanically with recorded outputs; eight mutation arms prove
every published claim on scratch copies rather than by reading; and a real backlog-id collision
between plan 21-10's CONF-13 deferrals and two unrelated pre-existing entries is found and fixed.**

## Status: COMPLETE

## Performance

- **Duration:** ~3h, single session
- **Tasks:** 3
- **Commits:** `b0a6ebd` (Task 1), `083898b` (Task 3 — includes the residual-filing fix; Task 2
  produced no shipped-artifact changes, see Decisions Made)

## Note on this SUMMARY's own worktree-file scope

Per the orchestrator's instructions for this run: `.planning/REQUIREMENTS.md` and
`.planning/ROADMAP.md` were edited in this worktree's local `.planning/` copy — both are
gitignored (`.planning/` blanket-ignored except force-tracked `*-SUMMARY.md` and this phase's
`21-CONF13-BASELINE.md`) and therefore **not captured by any git commit in this worktree**. This
plan's own tasks explicitly required both edits (CONF-12's amendment and the new backlog rows),
so they are flagged here rather than silently dropped — **the orchestrator should merge these two
files' changes into the main `.planning/` tree rather than overwriting them from a stale copy.**
The exact diffs are reproduced in full below so the orchestrator (or a human) can apply them
directly if the worktree copy is discarded.

---

## Task 1: CONF-12 amended in REQUIREMENTS.md, ROADMAP.md and CONF-SURFACE.md

### The amended CONF-12 text (verbatim, `.planning/REQUIREMENTS.md`)

```markdown
- [ ] **CONF-12**: `CLAUDE.md`'s CI-gate table and `docs/ARCHITECTURE.md`'s inventory are
      **generated** from those emissions, with a gate failing when committed text ≠ emitted text;
      per-gate detail moves to `docs/gates/<GATE-ID>.md`.

      **Amended 2026-09-06, Phase 21 plan 21-12 (D-07).** The original text of this requirement
      went on to impose a fixed character ceiling per cell, citing QUAL-01's pre-split width as
      the motivating example (git could not diff it; no reviewer could read it). That clause is
      removed.
      1. **What changed.** The character cap is removed. Each cell now carries a generated
         summary plus a link to `docs/gates/<GATE-ID>.md`; nothing measures cell width and no
         numeric ceiling is asserted or checked.
      2. **Why.** A character cap is a proxy for readability, not readability itself. The
         detail-page split (D-05/D-08) is the mechanism that actually makes the table readable —
         once the detail lives on its own page, the cell is short as a *consequence* of the
         split, not because a constraint holds it down. Measured evidence, before the split
         (pre-existing `CLAUDE.md`/`docs/ARCHITECTURE.md` cells) versus after (plan 21-08's
         generated cells): QUAL-01 22,630 characters → its `docs/gates/QUAL-01.md` page, with the
         table cell reduced to a short generated summary + link; SCAN-GUARD 9,307 → same
         treatment; TRACE-03 8,160 → same treatment; CONF-GATE 3,001 → same treatment. All four
         formerly-oversized cells are now under the split, not under a cap.
      3. **What replaces it as the driveable count.** Removing the cap removes CONF-12's own
         count, and the milestone's standing instruction requires a phase to name a count over
         shipped artifacts that can be driven to a target and declared done. That count is now
         supplied by two other measures, both already this phase's own requirements: **CONF-13's
         hand-maintained branch-count literals → 0** on the registered surfaces (aggregate figure
         `79` scanner-target hits established by plan 21-01's baseline sweep, driven to `0`
         non-exempt by plan 21-10's remediation and plan 21-09's standing scanner), and **the
         gate registry's equality floor over gate ids** (`registry ids symmetric-difference
         battery ids = 0`, asserted by `scripts/_gate_registry.py --self-test`). CONF-12 is
         satisfied by these two counts, not by cell width.
```

`.planning/ROADMAP.md`'s Phase 21 success criterion 3 was amended in lockstep with the same D-07
note (paraphrasing the removed cap rather than quoting it, matching the requirement's own
phrasing choice — see Decisions Made). `docs/gates/CONF-SURFACE.md` gained a new "Requirement
amendment (CONF-12, D-07)" section stating the same three elements for a reader with no
`.planning/` access, without restating any bare-digit figure not already corroborated in its own
Facts fence (D-06 containment).

### Verification

```
$ python3 scripts/gen-gate-docs.py --check
harvested 22/22 expected script-backed entries (22 total)
(exit 0)

$ python3 scripts/check-links.py
check-links: PASS (303 markdown links + 6 namespace refs across 156 files)
(exit 0)

$ bash scripts/check-firewall-battery.sh
...
FIREWALL: GREEN (26/26)
```

Acceptance-criteria assertions, individually:

- `.planning/REQUIREMENTS.md`'s CONF-12 no longer contains the literal string
  `no table cell exceeds 2,000 characters` — confirmed by `grep`, 0 matches (paraphrased instead,
  per Decisions Made).
- `.planning/ROADMAP.md`'s Phase 21 success criterion 3 no longer states the cap either —
  confirmed by `grep`, 0 matches on both documents.
- The replacement counts (`79` scanner-target aggregate; equality-floor = 0) match
  `21-CONF13-BASELINE.md`'s own Target table and `21-10-SUMMARY.md`'s final reading, cross-checked
  rather than restated from memory.
- `docs/gates/CONF-SURFACE.md`'s D-06 containment check passes with the new narrative present
  (`gen-gate-docs.py --check` exit 0, no containment findings).

Commit: `b0a6ebd` — `docs(21-12): record CONF-12's D-07 amendment on the claim-surface page`.

---

## Task 2: Five phase invariants asserted mechanically

No shipped artifact was modified for this task (per its own `<files>` scope: readings only). All
five commands were run and their outputs recorded verbatim below.

### 1. The three CONTRACT-06 sha256 pins

```python
# .venv/bin/python3, module loaded from scripts/check-quality-harness.py
_chain_block_well_formed: sha256:d7d42d7a0bd781bdb01f073d2929f7277c33c86c92f49bb63a48055ad15f13c3  (lines=121)
_conclusion_claims:       sha256:8b0cc1f1d2d32215e284f0276afbdbd63e761bcef573ec3723f6e6205405d394  (lines=63)
_slice_sections:          sha256:485ffe356a6782657709bc55ffaa1b474b1af2024398bcc00d2c799eb41c848e  (lines=149)
```

All three digests match the pinned literals in `scripts/check-quality-harness.py` byte-for-byte
(confirmed by direct grep of the pinned constants against the freshly recomputed digests). Line
counts 63 and 149 match the recorded values (`_conclusion_claims`, `_slice_sections`
respectively). `git diff -U0 2bb8bfa..HEAD -- scripts/check-quality-harness.py` was inspected: the
one hunk near `_slice_sections_pin_problems` (line 4735) adds a new `describe()` function
**after** the three pinned functions, not inside any of them; no pinned digest literal
(`d7d42d7a…`, `8b0cc1f1…`, `485ffe35…`) appears in either the `+` or `-` side of the diff — grep
for all three across the whole-phase diff returned zero matches, confirming no pin literal was
touched.

### 2. `_FROZEN_PATHS` at 22 entries

```
$ sed -n '/_FROZEN_PATHS=/,/^)/p' scripts/check-firewall-battery.sh | grep -c "^    '"
22
```

Entry list (verbatim): `tests/step0-baseline-v*.md`, `tests/step0-captures-v*`,
`tests/routing-baseline-v3.*.md`, `tests/routing-battery-baseline-v4.3.md`,
`tests/routing-baseline-v7.11.md`, `tests/routing-battery-baseline-v7.11.md`,
`tests/routing-baseline-v7.13.md`, `tests/routing-battery-baseline-v8.5.md`,
`tests/focused-output-baseline-v*.md`, `tests/sub-skill-routing-baseline-v*.md`,
`tests/quality-catalog-v8.7.md`, `tests/quality-probe-v8.7`,
`tests/quality-baseline-v8.7-regenerated`, `tests/quality-baseline-v8.7`,
`tests/quality-baseline-v8.7-postfix`, `tests/quality-baseline-v8.10-oos`,
`tests/defrobust-v8.11`, `tests/quality-provenance-v8.24`, `tests/quality-ledger-v8.26`,
`tests/adversarial-corpus-v9.0`, `tests/live-conformance-v9.0`,
`tests/live-conformance-catalog.md`. `git diff --stat 2bb8bfa..HEAD -- tests/` is empty across the
whole phase — nothing wrote into a frozen path.

### 3. `_GATED_SURFACES` the ordered 2-tuple

```
$ grep -n "_GATED_SURFACES" scripts/check-conf-gate.py | head -1
108:_GATED_SURFACES: tuple[str, ...] = ("shared-examples", "generated-twin")
```

Confirmed the ordered 2-tuple `("shared-examples", "generated-twin")`. Phase-scoped git log for
`scripts/check-conf-gate.py`:

```
$ git log --oneline -- scripts/check-conf-gate.py
82cb12e feat(21-05): add --describe limbs for STEP0-06, PROV-GUARD, CONF-GATE
b63abe1 test(18-13): ...
[... all remaining commits are Phase 18, pre-Phase-21 ...]
```

Only one Phase 21 commit touches this file (`82cb12e`, the `--describe` limb), confirming no
commit touched `_GATED_SURFACES` or any comparator predicate.

### 4. The coverage headline unmoved, derived live

```python
# .venv/bin/python3, scripts/check-traceability.py's _headline_literals()
slash: 192/94/0/286
prose: 192 reproducible / 94 audit-only / 0 gap / 286 total
```

Derived live from `_headline_literals()` (which internally calls `build_matrix_rows()`), not read
from any document. Matches the recorded headline exactly — this phase registered no matrix rows.

### 5. The battery total at 26, by call-site count

```
$ grep -cE '^\s*(gate|gate_prereq)\s' scripts/check-firewall-battery.sh
25
$ grep -oE 'gate(_prereq)? "[A-Za-z0-9_.-]+"' scripts/check-firewall-battery.sh | sed -E 's/^gate(_prereq)? //' | sort -u | wc -l
24
```

25 call sites (VAL-03 has two — a `gate` branch and a `gate_prereq` branch, mutually exclusive at
runtime), 24 unique gate ids. `24 + 2 inline (INVARIANT-CHECK, FROZEN-EVIDENCE) = 26`.

### Full regression set

```
$ bash scripts/check-firewall-battery.sh                     -> FIREWALL: GREEN (26/26)
$ python3 scripts/gen-gate-docs.py --check                   -> exit 0 (harvested 22/22)
$ python3 scripts/sync-content.py --check                    -> exit 0
$ python3 scripts/report-conformance.py --check               -> "report-conformance: PASS — no drift", exit 0
$ python3 scripts/check-links.py                               -> PASS (303 links + 6 namespace refs, 156 files), exit 0
$ python3 scripts/check-registration.py                        -> PASS (14/14 skills, 23/24 battery gates CI-registered + 1 battery-only), exit 0
```

Every gate's own `--self-test` was run individually (looped over `scripts/check-*.py`,
`sync-content.py`, `report-conformance.py`, `_gate_registry.py`, `gen-gate-docs.py`): all PASS.
(`check-links_anchors_test.py` is a pytest fixture file, not a standalone `--self-test` script —
its own leg is exercised correctly inside the battery's VAL-03 row via the `.venv` pytest
interpreter, confirmed PASS there; running it directly with bare `python3 file.py --self-test`
fails with `ModuleNotFoundError: pytest`, which is the wrong invocation for that file, not a real
failure.)

No commit for this task (readings only, per its own `<files>` scope).

---

## Task 3: Eight mutation arms, then three requirement declarations

All arms run on rsync/git scratch copies (`rsync -a --exclude .git`, and a full `git clone` for
Arm 8's git-shelling hook). Real repo `git status --porcelain` confirmed empty (0 lines) before
and after every single arm — recorded per arm below, all "0".

### Arm 1 — drift gate fires on a hand-edited CLAUDE.md generated region

Edited `CLAUDE.md:149`'s VAL-01 cell text on the scratch copy (`Plugin manifest schema validity`
→ `HAND-EDITED DRIFT ARM 1 plugin manifest schema validity`). `python3 scripts/gen-gate-docs.py
--check` → **exit 1**, printed `DRIFT: CLAUDE.md` with a unified diff naming line 149 exactly.
Real repo clean before/after: 0/0.

### Arm 2 — drift gate fires on a hand-edited detail page fence

Edited `docs/gates/VAL-01.md`'s Facts-fence line 6 on the scratch copy. `gen-gate-docs.py --check`
→ **exit 1**, printed `DRIFT: docs/gates/VAL-01.md` with a unified diff naming the page. Real
repo clean before/after: 0/0.

### Arm 3 — narrative preservation is real

Before-hash of `docs/gates/CONF-SURFACE.md`'s "Requirement amendment" narrative region (lines
25-38): `e89af5d6921e3d0d6a5a5eab8f6ebc411cb75f45d86cc7a0c835b93287f92871`. Appended
`MUTATION-ARM-3-NARRATIVE-EDIT` to its heading line, ran `gen-gate-docs.py --write` (`wrote 31
file(s)`, exit 0), then `--check` (exit 0, no drift). The edit **survived** — after-hash
`152ad091303e102e9a021e21e3e79b9fcd2cf1070c37a67a79e350db3738b7cb`, differing from the before-hash
by exactly the intended one-line addition (`diff` confirmed a single-line change, nothing
reverted). This is the one arm where the expected observation is that nothing fires — proves the
fenced split protects hand-written prose from `--write`. Real repo clean before/after: 0/0.

### Arm 4 — CONF-13's scanner fires on a reintroduced literal

Appended `"There are 63 controls newly claimed here for the phase-closure reintroduction proof."`
to `docs/README.md` on the scratch copy (a surface plan 21-10 cleaned). `gen-gate-docs.py --check`
→ **exit 1**:

```
docs/README.md:211: hand-maintained count literal '63 controls' (no exemption class matches)
literal-scan: 1 non-exempt hit(s) found
```

Named the exact file, line and text. Real repo clean before/after: 0/0.

### Arm 5 — the registry equality floor fires on a battery change

Deleted the `gate "VAL-05" ... ` block (lines 412-415) from the scratch copy's
`scripts/check-firewall-battery.sh`. Both:

```
$ python3 scripts/gen-gate-docs.py --check
D-01: registry names gate id(s) the battery does not register: ['VAL-05']
(exit 1)

$ python3 scripts/_gate_registry.py --self-test
_gate_registry: SELF-TEST FAIL [d01-live-battery-equality] — ["D-01: registry names gate id(s) the battery does not register: ['VAL-05']"]
(exit 1)
```

Both name `'VAL-05'` exactly. Real repo clean before/after: 0/0.

### Arm 6 — D-04 fires on a narrowed row

Changed `consumes=("derived_counts",)` to `consumes=()` for VAL-04's registry entry
(`scripts/_gate_registry.py:210`) on the scratch copy, while `check-trigger-collisions.py`'s
`--describe` still emits `derived_counts`. `gen-gate-docs.py --check` → **exit 1**:

```
D-04: scripts/check-trigger-collisions.py — --describe emits field 'derived_counts' but no registry entry or detail page consumes it
```

Names the specific script and field — the unconsumed-field direction, exactly the narrowing D-04
exists to catch. Real repo clean before/after: 0/0.

### Arm 7 — REG-GUARD fires on a removed CI job

Deleted the `gen-gate-docs:` job block (`name: gen-gate-docs (CONF-SURFACE)`, lines 332-343) from
the scratch copy's `.github/workflows/validation.yml`. `python3 scripts/check-registration.py` →
**exit 1**:

```
battery gate has no CI job: 'CONF-SURFACE' is registered in scripts/check-firewall-battery.sh
but no job in .github/workflows/validation.yml declares it (expected a `name: <job> (<GATE-ID>)`
entry)
```

Names `'CONF-SURFACE'`. Real repo clean before/after: 0/0.

### Arm 8 — the pre-commit hook blocks a drifted commit

A full local `git clone` of the worktree (separate from the rsync scratch copies used in Arms
1-7, since this arm needs a real `.git` for the hook's own `git add`/`git commit` to operate on),
`uv sync`'d, `core.hooksPath` set to `.githooks`. Made the same CLAUDE.md hand-edit as Arm 1,
`git add CLAUDE.md && git commit -m "arm 8 drift test commit"`. **Blocked**: the hook's gate 4
(`gen-gate-docs.py --self-test`) failed first —

```
gen-gate-docs: SELF-TEST FAIL [check-dispatch-wired] — DRIFT: CLAUDE.md
gen-gate-docs: SELF-TEST FAIL [check-reports-full-drift-count] — DRIFT: CLAUDE.md
```

— both naming CLAUDE.md with the exact injected line 149 diff, matching Arm 1's finding. `git log
--oneline -1` after the attempted commit still showed the pre-mutation HEAD (`b0a6ebd`) — the
"arm 8 drift test commit" never landed. Scratch git clone deleted after use. Real repo clean
before/after: 0/0.

**Real repo `git status --porcelain` was confirmed empty (0 lines) before Arm 1 and after every
one of the eight arms — never mutated at any point in this task.**

### Requirement declarations, each cross-checked against its producing SUMMARY

- **CONF-11**: script-backed registry entries with a working `--describe`: **22 of 22**
  (`gen-gate-docs.py --check`'s own `harvested 22/22 expected script-backed entries (22 total)`
  line, run just above). Hand-typed counts inside any `describe()` return: **0** — every
  `describe()` computes from live module constants (`len()`, `sorted()`, wrapper-source calls),
  cross-checked against `21-06-SUMMARY.md`'s and `21-07-SUMMARY.md`'s own "no hand-typed
  22/25/2 literals" statements for the population-arithmetic sentence. Describe-only shim
  scripts: **0** — this was D-01's own rejected alternative (`21-CONTEXT.md` D-01), never built;
  the 5 orphan gates (VAL-01, VAL-02, VAL-03's pytest leg, INVARIANT-CHECK, FROZEN-EVIDENCE) carry
  static registry descriptors instead.

- **CONF-12**: hand-maintained gate-table rows across both surfaces: **0** (both `CLAUDE.md` and
  `docs/ARCHITECTURE.md`'s CI-gate tables are generated regions under `--check`, confirmed clean
  above). Registry entries without a `docs/gates/` page: **0** — `len(_gate_registry.ENTRIES) ==
  28` and `ls docs/gates/*.md | wc -l == 28`, an exact match confirmed live. Drifted targets under
  `--check`: **0** (Task 1's and this task's own repeated `--check` runs, all exit 0). Disclosed
  bounds lost in the split: **0** — cross-checked against `21-08-SUMMARY.md`'s "Known Stubs" note
  confirming every `NARRATIVE_ENTRIES` page's disclosed-bound narrative and plan-number citations
  were migrated verbatim and no `(TODO: fill in this gate's disclosed bounds narrative.)`
  placeholder remains. D-07 amendment cited above for the removed cap.

- **CONF-13**: non-exempt hand-maintained branch-count literals on the registered surfaces: **0**,
  against the `79` scanner-target aggregate baseline plan 21-01 established
  (`21-CONF13-BASELINE.md`'s Target table). Cross-checked against `21-10-SUMMARY.md`'s own final
  reading — `0 non-exempt / 152 total hits` at that plan's close, now `157` total hits /
  `0` non-exempt after plan 21-11's registration widened the scanned surface set by one file
  (`scripts/gen-gate-docs.py` itself), read live from `docs/gates/CONF-SURFACE.md`'s Facts fence
  (`literal_scan_non_exempt`=0, `literal_scan_hits`=157). Exemption classes, each with a written
  reason: **8** — `version-stamp-count`, `headline-provenance-delta`, `plan-number-identifier`,
  `retired-body-budget`, `maxturns-60-value`, `sha256-digest`, `commonmark-heading-depth`,
  `deferred-remediation` (the last three exemption classes currently show `0`/`0`/`1` measured
  hits respectively on top of the two zero-hit classes named in the Facts fence — all 8 are named
  and reasoned in `LITERAL_EXEMPTION_CLASSES`, `scripts/gen-gate-docs.py`, regardless of current
  hit count).

None of the three declarations above is phrased as "the gate fails when X is broken" — each names
a counted figure over shipped artifacts.

### A genuine backlog-id collision, found and fixed (Rule 1 — bug)

While filing residuals per this task's own acceptance criteria ("every unclosed residual has a
`999.x` id... never a silent omission"), found that plan 21-10's three CONF-13
deferred-remediation groups were filed under `999.32`/`999.33`/`999.34`
(`21-10-SUMMARY.md`, `21-CONF13-BASELINE.md`'s pre-existing disposition ledger,
`docs/gates/CONF-SURFACE.md`'s Disclosed bounds, and `scripts/gen-gate-docs.py`'s
`_DEFERRED_REMEDIATION_SURFACES` map) — but those three ids were **already in use** by three
unrelated, pre-existing `.planning/ROADMAP.md` backlog entries, all filed 2026-09-05:
`999.32` (`report-conformance.py`'s provenance sentinel, Phase 17's review), `999.33` (Phase 17's
pre-commit gate-count doc sweep), `999.34` (CONF-GATE's `run_live()` control flow, Phase 18's
review) — confirmed by `grep -n "^### Phase 999\." .planning/ROADMAP.md`, which also showed
`999.39` as the highest existing id (no `999.4x` in use).

**Fix:** renumbered the three CONF-13 groups to `999.40`/`999.41`/`999.42` — the next free ids —
everywhere they are cited in shipped, non-historical artifacts:
`scripts/gen-gate-docs.py`'s `_DEFERRED_REMEDIATION_SURFACES` map, its surrounding comments, and
its exemption-class message string; `docs/gates/CONF-SURFACE.md`'s Disclosed bounds `(5)`;
`21-CONF13-BASELINE.md`'s disposition ledger table (with a new ID-correction note explaining the
renumbering and pointing at the historical citation). Added three real
`.planning/ROADMAP.md` § Backlog entries (`### Phase 999.40/41/42`) — previously these three
groups had **no real backlog row at all**, only bare id citations, which is exactly the gap this
task's acceptance criteria required closing. **`21-10-SUMMARY.md`'s own historical text is left
unedited** (force-tracked record of what that plan actually did at the time), per the same
"correction pointer, not silent rewrite" discipline this project uses elsewhere for post-hoc
corrections.

Verified after the fix: `gen-gate-docs.py --write` (idempotent — `git diff --stat` shows only the
three touched files, no unintended change to `CLAUDE.md` or any other generated region),
`gen-gate-docs.py --check` exit 0, `gen-gate-docs.py --self-test` PASS (49 controls),
`bash scripts/check-firewall-battery.sh` GREEN (26/26).

### Final verification

```
$ bash scripts/check-firewall-battery.sh   -> FIREWALL: GREEN (26/26)
$ python3 scripts/gen-gate-docs.py --check -> exit 0
$ git status --porcelain | wc -l           -> 0 (after Task 3's commit)
```

Commit: `083898b` — `fix(21-12): renumber colliding CONF-13 deferral backlog ids 999.32-34`.

### Rework cap

**Not touched.** Phase 21 ran 12 plans (`21-01` through `21-12`), all forward-progressing — no
gap-closure plan (`-gap-` naming or duplicated plan number) anywhere in the phase's commit history
(`git log --oneline 2bb8bfa..HEAD`, 51 commits, inspected). The rework cap of 2 gap-closure plans
was never approached.

---

## Task Commits

1. **Task 1: Amend CONF-12 with its reason and replacement count** — `b0a6ebd` (docs)
2. **Task 2: Assert every phase invariant mechanically** — no commit (readings only, no shipped
   artifact modified)
3. **Task 3: Prove claims by mutation; declare requirements; fix the backlog-id collision** —
   `083898b` (fix)

## Files Created/Modified

- `.planning/REQUIREMENTS.md` — CONF-12 amended (D-07); **gitignored, not captured by any commit
  in this worktree — see the note above.**
- `.planning/ROADMAP.md` — Phase 21 success criterion 3 amended in lockstep; three new
  `999.40`/`999.41`/`999.42` § Backlog entries added; **gitignored, not captured by any commit in
  this worktree — see the note above.**
- `docs/gates/CONF-SURFACE.md` — new "Requirement amendment (CONF-12, D-07)" narrative section;
  three backlog id references corrected `999.32/33/34` → `999.40/41/42`; committed (`b0a6ebd`,
  `083898b`)
- `scripts/gen-gate-docs.py` — three backlog id references corrected across
  `_DEFERRED_REMEDIATION_SURFACES`, its comments, and the `deferred-remediation` exemption-class
  message; committed (`083898b`)
- `.planning/phases/21-generate-the-claim-surface/21-CONF13-BASELINE.md` — disposition ledger's
  three backlog ids corrected, new ID-correction note added; committed (`083898b`)

## Decisions Made

See `key-decisions` in frontmatter, summarized: (1) CONF-12's amendment paraphrases rather than
quotes the removed cap's exact wording, since the acceptance criteria requires that literal
string's absence; (2) `docs/gates/CONF-SURFACE.md`'s new narrative avoids restating any bare-digit
figure not already corroborated in its own Facts fence (D-06); (3) the three colliding backlog ids
were renumbered rather than left colliding, with the historical SUMMARY left unedited and a
correction pointer added instead; (4) Task 2 produced no commit since it modified no shipped
artifact.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] CONF-12's original clause quoted verbatim would have re-triggered the very
acceptance criterion removing it**
- **Found during:** Task 1, drafting the amendment
- **Issue:** An initial draft quoted the original cap clause verbatim ("*and no table cell
  exceeds 2,000 characters...*") for provenance. This left the exact string
  `no table cell exceeds 2,000 characters` present in `.planning/REQUIREMENTS.md`, directly
  violating the acceptance criterion requiring that literal string's absence.
- **Fix:** Reworded to a paraphrase ("went on to impose a fixed character ceiling per cell...")
  that preserves the historical record without reintroducing the removed string. Applied the
  same fix to `.planning/ROADMAP.md`'s parallel wording.
- **Files modified:** `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`
- **Verification:** `grep -c "no table cell exceeds 2,000 characters"` / `grep -c "No table cell
  exceeds 2,000 characters"` both return 0 on their respective files.
- **Committed in:** not committed (gitignored `.planning/` files — see the worktree-file-scope
  note above)

**2. [Rule 1 - Bug] Colliding backlog ids 999.32/999.33/999.34**
- **Found during:** Task 3, filing residuals per the acceptance criteria
- **Issue:** Plan 21-10's three CONF-13 deferred-remediation groups were filed under ids already
  used by three unrelated pre-existing backlog entries (filed 2026-09-05 by Phases 17/18's
  reviews).
- **Fix:** Renumbered to `999.40`/`999.41`/`999.42` in every shipped, non-historical artifact;
  added real `.planning/ROADMAP.md` backlog rows for them (they previously had none); left
  `21-10-SUMMARY.md`'s historical text unedited with a correction pointer added at
  `21-CONF13-BASELINE.md`.
- **Files modified:** `scripts/gen-gate-docs.py`, `docs/gates/CONF-SURFACE.md`,
  `.planning/phases/21-generate-the-claim-surface/21-CONF13-BASELINE.md`,
  `.planning/ROADMAP.md`
- **Verification:** `gen-gate-docs.py --write` idempotent, `--check` exit 0, `--self-test` PASS
  (49 controls), `bash scripts/check-firewall-battery.sh` GREEN (26/26).
- **Committed in:** `083898b` (the three git-tracked files); `.planning/ROADMAP.md`'s new backlog
  rows are gitignored — see the worktree-file-scope note above.

**Total deviations:** 2 auto-fixed (both Rule 1 bugs), both surfaced by this plan's own required
verification steps and fixed before the affected work was considered done. Neither required a
Rule 4 architectural-change checkpoint.

## Assumption Drift (advisory)

- **Found during:** Task 3, cross-checking CONF-13's declared figure
- **Planned assumption:** the plan's own action text frames CONF-13's declaration as "non-exempt
  hand-maintained branch-count literals on the registered surfaces: 0 against the aggregate
  baseline figure plan 21-01 established," implicitly treating `79`/`152`-total as the stable
  reference pair.
- **What turned out true:** the live reading today is `157` total hits (not `152`), because plan
  21-11 landed CONF-SURFACE as a real (non-anticipatory) registry entry, which widened the
  scanned `.py`-docstring surface set to include `scripts/gen-gate-docs.py` itself — one
  additional file, `+5` total hits net of the one real finding 21-11 fixed inline. `0` non-exempt
  is unchanged.
- **Why it matters:** advisory only — the declaration's `0`-non-exempt figure and its `79`
  driveable-target baseline are both unmoved; only the incidental `total hits` denominator moved,
  a side effect of registering CONF-SURFACE itself (a phase invariant this plan's own Task 2
  did not name as one of its five tracked invariants, since it is not one of the five the plan
  specified). Recorded so a future reader comparing `21-10-SUMMARY.md`'s "152 total" against
  today's "157 total" does not read the discrepancy as an error.

## Issues Encountered

None beyond the two deviations above, both resolved within this plan's own scope.

## Next Phase Readiness

- **This plan is COMPLETE.** All three tasks landed (Task 2 needed no commit): `b0a6ebd`
  (Task 1), `083898b` (Task 3).
- `bash scripts/check-firewall-battery.sh` reports **FIREWALL: GREEN (26/26)** against the
  committed state.
- Real repo `git status --porcelain` is empty at close.
- **Handed to the orchestrator:** `.planning/REQUIREMENTS.md` and `.planning/ROADMAP.md` were
  edited in this worktree's local copy but are gitignored — not captured by any commit here. The
  orchestrator must merge these two files' changes (reproduced in full in Task 1 and in the new
  backlog entries above) into the shared `.planning/` tree rather than overwriting them from a
  stale copy.
- **Handed forward (backlog, not blocking):** `999.40`/`999.41`/`999.42` — CONF-13's standing
  scanner still over-fires on 3 surface classes (135 items total across 25 files), held at zero
  by the `deferred-remediation` whole-surface exemption. Entry condition for each: port D-06's
  citation-exemption vocabulary into the standing scanner, or hand-remediate.
- No blockers. Phase 21 (Generate the Claim Surface) is closed: CONF-11, CONF-12 (amended),
  CONF-13 all declared against counted, cross-checked figures.

## Known Stubs

None. Every artifact this plan touched is real, generated-or-verified content — no placeholder
text, no silently-absorbed gap. The three CONF-13 deferrals are named backlog items with entry
conditions, not stubs.

---
*Phase: 21-generate-the-claim-surface*
*Completed: 2026-09-06*

## Self-Check: PASSED

- FOUND: commit `b0a6ebd` (Task 1), `083898b` (Task 3) — `git log --oneline --all`
- FOUND: `docs/gates/CONF-SURFACE.md` contains "Requirement amendment (CONF-12, D-07)"
- FOUND: `scripts/gen-gate-docs.py` contains `999.40`, `999.41`, `999.42`; contains no `999.32`,
  `999.33`, `999.34`
- FOUND: `.planning/phases/21-generate-the-claim-surface/21-CONF13-BASELINE.md` contains the
  ID-correction note and the renumbered table
- FOUND: `python3 scripts/gen-gate-docs.py --check` exits 0 (real exit code confirmed)
- FOUND: `python3 scripts/gen-gate-docs.py --self-test` exits 0 (49 controls)
- FOUND: `bash scripts/check-firewall-battery.sh` reports `FIREWALL: GREEN (26/26)`
- FOUND: `git status --porcelain` empty in the real repo at close
- FOUND: three CONTRACT-06 digests recomputed match pinned literals exactly (grep-confirmed)
- FOUND: `_FROZEN_PATHS` = 22 entries; `git diff --stat 2bb8bfa..HEAD -- tests/` empty
- FOUND: coverage headline derived live = `192/94/0/286`, matching the recorded figure
