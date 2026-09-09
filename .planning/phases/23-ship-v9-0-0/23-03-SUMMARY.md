---
phase: 23-ship-v9-0-0
plan: 03
subsystem: release-versioning
tags: [version-stamp, lockstep-bump, version-01, dual-04, falsification-mutation]

# Dependency graph
requires:
  - phase: 23-ship-v9-0-0
    plan: 02
    provides: "19 v9.0.0 matrix rows registered, coverage headline 192/94/0/286 -> 208/97/0/305 (commit ed73189)"
provides:
  - "All 17 hand-maintained version stamps at 9.0.0, propagated into the generated tree via sync-content.py --write (commit a27a308)"
  - "VERSION-01 and DUAL-04 proven, by scratch-copy mutation, to fail by name on a left-behind stamp and an unpropagated generated file"
  - "A measured (not assumed) reading of _YAML_STAMP_RE's reach against an unquoted scalar: it DOES catch that shape"
affects: ["23-04", "23-05"]

tech-stack:
  added: []
  patterns: ["falsification by scratch-copy mutation, never by reading", "REPO_ROOT = Path(__file__).resolve().parents[1] makes both gates git-independent, so no worktree trick was needed this plan"]

key-files:
  created: []
  modified:
    - ".claude-plugin/marketplace.json"
    - "first-principles/.claude-plugin/plugin.json"
    - "shared/spine/SKILL.meta.yml"
    - "shared/skills/challenge-assumptions/SKILL.md"
    - "shared/skills/estimate/SKILL.md"
    - "shared/skills/first-principles-analysis/SKILL.md"
    - "shared/skills/fishbone/SKILL.md"
    - "shared/skills/five-whys/SKILL.md"
    - "shared/skills/ground-truths/SKILL.md"
    - "shared/skills/identify-essence/SKILL.md"
    - "shared/skills/inversion/SKILL.md"
    - "shared/skills/pre-mortem/SKILL.md"
    - "shared/skills/reason-upward/SKILL.md"
    - "shared/skills/second-order/SKILL.md"
    - "shared/skills/theoretical-limit/SKILL.md"
    - "shared/skills/trade-off/SKILL.md"
    - "shared/skills/validate/SKILL.md"
    - "first-principles/agents/first-principles.md"
    - "first-principles/skills/*/SKILL.md (14 generated stubs)"

key-decisions:
  - "Both check-version-stamps.py and sync-content.py resolve REPO_ROOT from Path(__file__).resolve().parents[1], not from git — so the plan 20-06 git-worktree workaround for scratch-copy checks that shell out to git was not needed here; a plain rsync --exclude .git scratch copy runs both gates natively."
  - "Mutation 2 (unquoted `version: 9.0.0`) IS caught by _YAML_STAMP_RE with a named, specific error message. This is a measured result, not an assumption the plan left open as a possible non-catch; recorded here as the honest observed outcome per the plan's own instruction."

requirements-completed: [REL-01]

# Metrics
duration: ~20min
completed: 2026-09-09
---

# Phase 23 Plan 03: Bump All 17 Version Stamps to 9.0.0 in Lockstep Summary

**All 17 hand-maintained version stamps moved from `8.26.0` to `9.0.0` in one commit
(`a27a308`), propagated into the generated tree by `sync-content.py --write` rather than
hand-edited, with VERSION-01 and DUAL-04 each proven — by breaking a disposable scratch copy,
not by reading the script — to fail by name when a single stamp or a single generated file is
left behind.**

## Performance

- **Duration:** ~20 min
- **Completed:** 2026-09-09
- **Tasks:** 2 completed (task 1 committed; task 2 is scratch-copy only, no commit)
- **Files modified:** 32 tracked files in the one commit (17 sources + agent + 14 generated skill stubs)

## Accomplishments

- Ran `python3 scripts/check-version-stamps.py` before touching any file and recorded the
  pre-bump reading: 17 stamps, all `'8.26.0'`, `PASS` — confirming the starting state matched
  the plan's expectation before bumping over it.
- Edited all 17 hand-maintained sources to `9.0.0` via `sed`, preserving the double-quoted YAML
  scalar form in every frontmatter site (`version: "9.0.0"`, never bare) and the JSON string
  form in both manifest files.
- Ran `python3 scripts/sync-content.py --write` (48 files written), then `--check` (exit 0),
  then `check-version-stamps.py` again (exit 0, 17 stamps all `'9.0.0'`) — in the exact
  plan-mandated order.
- Confirmed via `/usr/bin/grep -rn "8\.26\.0"` that zero live-stamp hits remain in `shared/`,
  `.claude-plugin/`, `first-principles/.claude-plugin/`, or the generated
  `first-principles/agents/`/`first-principles/skills/` tree.
- Confirmed via targeted greps that no YAML stamp reads the unquoted `version: 9...` form, and
  that exactly 15 sites (14 skill sources + `shared/spine/SKILL.meta.yml`) carry
  `version: "9.0.0"`.
- Ran `gen-gate-docs.py --self-test` then `--check` (both clean — the version bump touches no
  gate-doc-embedded fact), then `sh .githooks/pre-commit` explicitly before committing (exit 0,
  all five pre-commit gates green).
- Committed all 32 files (17 sources + 15 generated) as `a27a308`; confirmed no post-commit
  deletions and `sync-content.py --check` still exits 0 after the commit.
- Task 2: on a disposable `rsync -a --exclude .git` scratch copy, applied and reverted three
  mutations, each with a verbatim before/after `md5sum` confirming byte-identical revert, and
  confirmed the real repository's `git status --porcelain` was empty both immediately before the
  first mutation and immediately after the last.

## Pre-bump / Post-bump Readings (verbatim)

**Pre-bump:**
```
check-version-stamps: 17 stamps, all '8.26.0'
  .claude-plugin/marketplace.json#plugins[0]
  first-principles/.claude-plugin/plugin.json
  shared/skills/challenge-assumptions/SKILL.md
  ... (14 shared/skills/*/SKILL.md total)
  shared/spine/SKILL.meta.yml
check-version-stamps: PASS
```

**Post-bump (post sync-content.py --write, pre-commit):**
```
check-version-stamps: 17 stamps, all '9.0.0'
  .claude-plugin/marketplace.json#plugins[0]
  first-principles/.claude-plugin/plugin.json
  shared/skills/challenge-assumptions/SKILL.md
  ... (14 shared/skills/*/SKILL.md total)
  shared/spine/SKILL.meta.yml
check-version-stamps: PASS
```

**Post-commit re-confirmation:**
```
$ python3 scripts/sync-content.py --check
(exit 0, no output — clean)
```

## Falsification Table (VERSION-01 / DUAL-04 non-vacuity, three scratch-copy mutations)

All three mutations applied only to a disposable `rsync -a --exclude .git` scratch copy under
the session scratchpad directory, never to the real tree. `git status --porcelain` in the real
repository was empty both immediately before mutation 1 and immediately after mutation 3's
revert — confirmed by direct command, not inferred.

| # | Mutation | Command | Verbatim result | CAUGHT? |
|---|---|---|---|---|
| 1 | Revert `shared/skills/five-whys/SKILL.md`'s stamp to `8.26.0`, leaving the other 16 at `9.0.0` | `python3 scripts/check-version-stamps.py` | `check-version-stamps: version stamps diverge across 17 source(s):` / `check-version-stamps:   '8.26.0'  <- 1 file(s)` / `check-version-stamps:       shared/skills/five-whys/SKILL.md` / `check-version-stamps:   '9.0.0'  <- 16 file(s)` (16 files listed) / `check-version-stamps: FAIL` — exit 1 | YES — names the exact offending file and the disagreeing value |
| 2 | Change `shared/spine/SKILL.meta.yml`'s stamp to the unquoted form `version: 9.0.0` | `python3 scripts/check-version-stamps.py` | `check-version-stamps: shared/spine/SKILL.meta.yml: version stamp '9.0.0' is not a double-quoted string (write version: "x.y.z" -- an unquoted stamp can parse as a float)` / `check-version-stamps: FAIL` — exit 1 | YES — `_YAML_STAMP_RE` DOES catch this shape; recorded exactly as observed, per the plan's instruction not to report a pass that did not happen. There is no un-caught bound to file here. |
| 3 | Revert `first-principles/skills/five-whys/SKILL.md`'s generated stamp to `8.26.0` without touching its `shared/` source | `python3 scripts/sync-content.py --check` | `DRIFT: first-principles/skills/five-whys/SKILL.md` with a unified diff showing `-  version: "8.26.0"` / `+  version: "9.0.0"`, followed by `Run: python3 scripts/sync-content.py --write && git add -u` — exit 1 | YES — names the exact drifted generated file with the expected fix command |

Each mutation reverted before the next; `md5sum` of the mutated file confirmed byte-identical to
a saved pre-mutation copy after every revert (`five-whys` shared source: `fc68069e...`;
`SKILL.meta.yml`: `4c5c579a...`; generated `five-whys` stub: `477fe65c...` — all matched on
revert). No tracked file was modified and no commit was made for task 2.

Both `check-version-stamps.py` and `sync-content.py` resolve their working root via
`REPO_ROOT = Path(__file__).resolve().parents[1]`, not via any `git` shell-out, so neither gate
needed the plan-20-06 git-worktree workaround for a `.git`-less scratch copy; a plain `rsync`
copy runs both checks natively.

## Verification Results

```
$ python3 scripts/check-version-stamps.py && echo EXIT:0
check-version-stamps: 17 stamps, all '9.0.0'
  ... (17 sources listed)
check-version-stamps: PASS
EXIT:0

$ python3 scripts/sync-content.py --check && echo EXIT:0
EXIT:0

$ sh .githooks/pre-commit && echo EXIT:0
(report-conformance self-test's own mutated-fixture DRIFT line, expected internal noise)
report-conformance: SELF-TEST PASS — 102 controls run
report-conformance: PASS — no drift
gen-gate-docs: SELF-TEST PASS — 74 controls run
harvested 22/22 expected script-backed entries (22 total)
EXIT:0

$ git status --porcelain | /usr/bin/grep -c . | /usr/bin/grep -qx 0 && python3 scripts/check-version-stamps.py && python3 scripts/sync-content.py --check && echo TASK2_VERIFY:PASS
TASK2_VERIFY:PASS

$ git log --oneline -1
a27a308 feat(23-03): bump all 17 version stamps to 9.0.0 in lockstep

$ git show --stat HEAD | tail -2
32 files changed, 32 insertions(+), 32 deletions(-)
```

- `FIREWALL: GREEN 26/26` was not used anywhere in this plan to discharge REL-01; every
  criterion above is evidenced by a specific command's observed output, per the plan's own
  instruction that a green battery is not evidence REL-01 is met.

## Deviations from Plan

None — plan executed exactly as written. Both tasks completed with no auto-fixes, no
architectural questions, and no checkpoints.

## Known Stubs

None. Every file touched is either a version-stamp source or its mechanically regenerated
sibling; no UI, no mock data path.

## Threat Flags

None. Per the plan's own threat model (T-23-04, T-23-05, both `mitigate`): mutation 2 measured
`_YAML_STAMP_RE`'s real reach against the unquoted-scalar shape (T-23-04) and found it catches
that shape; mutation 3 proved DUAL-04 fires by name on a hand-tampered generated file (T-23-05).
No new network, auth, or trust-boundary surface is introduced by a version-stamp bump.

## Next Steps

- Plan 23-04: REL-02 — battery GREEN with CONF-GATE and every Phase 21/22 control registered.
- Plan 23-05: REL-04 — the `[9.0.0]` CHANGELOG entry closing SHIP-05 by name, plus the
  CR-01/CR-02/CR-03 disclosures required by D-14 and success criterion 6, plus the final
  conformance-baseline reading.

## Self-Check: PASSED

- `test -f .claude-plugin/marketplace.json` → FOUND
- `test -f first-principles/.claude-plugin/plugin.json` → FOUND
- `test -f shared/spine/SKILL.meta.yml` → FOUND
- `test -f first-principles/agents/first-principles.md` → FOUND
- `git log --oneline --all | grep -q a27a308 && echo FOUND` → FOUND
- `python3 scripts/check-version-stamps.py` → PASS, 17 stamps all `9.0.0`
- `python3 scripts/sync-content.py --check` → exit 0
- `git status --porcelain` → empty
