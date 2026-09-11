---
phase: 27-ship-v9-1-0
plan: 05
subsystem: release-act-one-version-stamps
tags: [release, version-stamps, VERSION-01, mutation-proof, REL-05]

dependency-graph:
  requires:
    - "27-02: all fourteen pre-existing v9.1.0 requirement boxes re-derived clean, no ship blocker (this plan's own precondition)"
    - "27-04: the pre-release recurrence reading, whose 61 FENCED sites this plan's release act must not touch"
  provides:
    - "All 17 hand-maintained version stamps at 9.1.0, generated tree regenerated and drift-free"
    - "REL-05 ticked with fresh command-and-output evidence, including a scratch-copy mutation proof that VERSION-01's PASS is not vacuous"
  affects:
    - "plan 27-06..09 (the remaining release acts: matrix rows, headline sweep, CHANGELOG, post-arm reading) — all now run against a tree already at 9.1.0"

tech-stack:
  added: []
  patterns:
    - "rsync --exclude .git scratch-copy mutation proof, md5sum-confirmed restoration, real-tree git status --porcelain confirmed empty before/after (Phase 25/26 precedent)"

key-files:
  created: []
  modified:
    - .claude-plugin/marketplace.json
    - first-principles/.claude-plugin/plugin.json
    - shared/spine/SKILL.meta.yml
    - shared/skills/challenge-assumptions/SKILL.md
    - shared/skills/estimate/SKILL.md
    - shared/skills/first-principles-analysis/SKILL.md
    - shared/skills/fishbone/SKILL.md
    - shared/skills/five-whys/SKILL.md
    - shared/skills/ground-truths/SKILL.md
    - shared/skills/identify-essence/SKILL.md
    - shared/skills/inversion/SKILL.md
    - shared/skills/pre-mortem/SKILL.md
    - shared/skills/reason-upward/SKILL.md
    - shared/skills/second-order/SKILL.md
    - shared/skills/theoretical-limit/SKILL.md
    - shared/skills/trade-off/SKILL.md
    - shared/skills/validate/SKILL.md
    - first-principles/skills/challenge-assumptions/SKILL.md
    - first-principles/skills/estimate/SKILL.md
    - first-principles/skills/first-principles-analysis/SKILL.md
    - first-principles/skills/fishbone/SKILL.md
    - first-principles/skills/five-whys/SKILL.md
    - first-principles/skills/ground-truths/SKILL.md
    - first-principles/skills/identify-essence/SKILL.md
    - first-principles/skills/inversion/SKILL.md
    - first-principles/skills/pre-mortem/SKILL.md
    - first-principles/skills/reason-upward/SKILL.md
    - first-principles/skills/second-order/SKILL.md
    - first-principles/skills/theoretical-limit/SKILL.md
    - first-principles/skills/trade-off/SKILL.md
    - first-principles/skills/validate/SKILL.md
    - first-principles/agents/first-principles.md
    - .planning/REQUIREMENTS.md

decisions: []

requirements-completed: [REL-05]

metrics:
  duration: "~30 minutes"
  completed: "2026-09-11"
---

# Phase 27 Plan 05: Release Act One — Bump All 17 Version Stamps Summary

Moved all 17 hand-maintained version stamps from `9.0.0` to `9.1.0` in one atomic commit, regenerated the plugin tree from `shared/`, and proved VERSION-01's PASS is not vacuous by mutation on a disposable scratch copy. REL-05 is ticked on fresh evidence.

## What was built

**Precondition checked first.** Plan 27-02's summary records all fourteen pre-existing v9.1.0 requirement boxes re-derived clean this session, with no ship blocker raised — the release act was clear to run.

**Task 1 — bump and regenerate.** Ran `python3 scripts/check-version-stamps.py` first to get the authoritative before-reading: `17 stamps, all '9.0.0'`, `PASS`. Changed all 17 stamps to `9.1.0`, preserving each site's exact syntactic form (JSON double-quotes and trailing commas; YAML double-quoted string form, never a bare number):

- `.claude-plugin/marketplace.json` — `"version": "9.0.0"` → `"9.1.0"`
- `first-principles/.claude-plugin/plugin.json` — same
- `shared/spine/SKILL.meta.yml` — `version: "9.0.0"` → `"9.1.0"`
- 14 `shared/skills/<slug>/SKILL.md` frontmatter stamps — same

Ran `python3 scripts/sync-content.py --write` to regenerate the whole plugin tree from `shared/` (48 files written: 14 skill stubs + the assembled agent body plus their reference siblings), then `python3 scripts/sync-content.py --check` — exit 0, zero drift. Re-ran `check-version-stamps.py`: `17 stamps, all '9.1.0'`, `PASS`. `claude plugin validate ./first-principles` ran (CLI available, version 2.1.268) — "Validation passed with warnings"; the warnings are the pre-existing, expected "No frontmatter block found" notices on reference sibling files under `first-principles/agents/references/`, unrelated to the version bump (CLAUDE.md's own VAL-01 note: the CLI does not validate agent frontmatter for a flat `agents/*.md`, so this is not a regression).

`sh .githooks/pre-commit` exited 0 (report-conformance self-test 110 controls PASS, `--check` PASS no drift; gen-gate-docs self-test 112 controls PASS, `--check` harvested 22/22). `git diff first-principles/agents/first-principles.md` confirmed the only change is the single `version:` line — no fence violation against plan 27-04's 61 FENCED pre-arm sites, none of which live in this diff.

All 32 changed files (exactly the plan's declared `files_modified` list) landed in one commit, `b89fcb4`. `git diff --diff-filter=D --name-only HEAD~1 HEAD` — empty, no unexpected deletions. `git status --porcelain` clean after commit. `git diff --name-only` from the phase base does not touch `.github/workflows/validation.yml` or `scripts/check-firewall-battery.sh`.

**Task 2 — prove VERSION-01 is not vacuous, tick REL-05.** Confirmed the real repository's `git status --porcelain` was empty before the first mutation. Produced a disposable scratch copy via `rsync -a --exclude .git` into the session scratchpad (never the real tree).

- **Arm A** (unmutated scratch copy): `python3 scripts/check-version-stamps.py` → `17 stamps, all '9.1.0'`, `PASS`, exit 0.
- **Arm B** (`shared/skills/five-whys/SKILL.md`'s stamp reverted to `9.0.0` — chosen from the most numerous class per the plan's instruction): re-ran the same command → `check-version-stamps: version stamps diverge across 17 source(s): '9.0.0' <- 1 file(s) shared/skills/five-whys/SKILL.md ... FAIL`, exit 1 — names the disagreeing stamp by path.
- File restored (`sed` reverting `9.0.0` back to `9.1.0`) and confirmed byte-identical via `md5sum` (`9940fb5a5d140ed414899682cc9100ec` before and after) before the scratch copy was discarded (`rm -rf`). Re-ran the check after restoration: `PASS`, exit 0.

Both arms produced exactly their expected result. Confirmed the real repository's `git status --porcelain` was empty again after the scratch copy was discarded.

Ticked REL-05 in `.planning/REQUIREMENTS.md` (`- [ ]` → `- [x]`) with an evidence block of the Phase 23 D-02/D-03 shape: the `check-version-stamps.py` command and its literal before/after output, the `sync-content.py --check` command and its exit-0 result as its own pair (REL-05 names it explicitly), and the mutation-proof transcript, closing with the sentence connecting the readings to REL-05's own words. Updated the `## Traceability` table's REL-05 row from `Pending` to `Complete`. Confirmed `.planning/REQUIREMENTS.md` is gitignored via `git check-ignore -v` — no commit is expected or produced for this task's edits.

Ran `bash scripts/check-firewall-battery.sh` (took longer than the 120s foreground timeout; completed in the background) → `FIREWALL: GREEN (26/26)` — cited as a floor check per the plan's own instruction, never as the evidence for REL-05 itself.

## Deviations from Plan

None — plan executed exactly as written. Both tasks landed with the exact file sets and command sequence specified.

## Verification (observed this session)

- `python3 scripts/check-version-stamps.py` before the bump → `17 stamps, all '9.0.0'`, `PASS`, exit 0 (observed).
- `python3 scripts/check-version-stamps.py` after the bump → `17 stamps, all '9.1.0'`, `PASS`, exit 0 (observed).
- `python3 scripts/sync-content.py --check` → exit 0, no drift (observed, both immediately post-`--write` and post-commit).
- `/usr/bin/grep -rc "9\.0\.0" .claude-plugin/marketplace.json first-principles/.claude-plugin/plugin.json shared/spine/SKILL.meta.yml` → `0` for each of the three files (observed).
- `/usr/bin/grep -l '9\.1\.0' shared/skills/*/SKILL.md | wc -l` → `14`; `/usr/bin/grep -l '9\.0\.0' shared/skills/*/SKILL.md | wc -l` → `0` (observed — the plan's own `^version:` acceptance-criterion anchor does not match the actual indented `  version:` line under `metadata:`, so content-based confirmation was used instead).
- `sh .githooks/pre-commit` → exit 0 both pre- and post-commit (observed).
- `claude plugin validate ./first-principles` → "Validation passed with warnings" (pre-existing reference-sibling frontmatter warnings, unrelated to this plan), exit 0 (observed).
- `git show --stat HEAD` → 32 files changed, 32 insertions(+), 32 deletions(-) (observed).
- `git diff --name-only` from the phase base does not touch `.github/workflows/validation.yml` or `scripts/check-firewall-battery.sh` (observed).
- `git diff --diff-filter=D --name-only HEAD~1 HEAD` → empty (observed).
- Arm A (unmutated scratch copy) → `PASS`, exit 0 (observed).
- Arm B (`shared/skills/five-whys/SKILL.md` reverted to `9.0.0`) → `FAIL`, exit 1, names `shared/skills/five-whys/SKILL.md` explicitly (observed).
- `md5sum` of the mutated-then-restored file matches the pre-mutation reading exactly: `9940fb5a5d140ed414899682cc9100ec` (observed, both readings).
- Real repository `git status --porcelain` → empty, both before the first mutation and after the scratch copy was discarded (observed twice).
- `/usr/bin/grep -c "^- \[x\] \*\*REL-05\*\*" .planning/REQUIREMENTS.md` → `1` (observed).
- `git check-ignore -v .planning/REQUIREMENTS.md` → `.gitignore:1:.planning/ .planning/REQUIREMENTS.md` (observed) — confirms no commit is expected from Task 2's file edits.
- `bash scripts/check-firewall-battery.sh` → `FIREWALL: GREEN (26/26)` (observed) — floor check only, not evidence for REL-05.

## Self-Check: PASSED

- `.claude-plugin/marketplace.json` reads `"version": "9.1.0"` — FOUND.
- `shared/spine/SKILL.meta.yml` reads `version: "9.1.0"` — FOUND.
- Commit `b89fcb4` — FOUND (`git log --oneline --all | grep b89fcb4`).
- `.planning/REQUIREMENTS.md` REL-05 checkbox reads `[x]` — FOUND (verified by the grep count above).
- `.planning/REQUIREMENTS.md` Traceability REL-05 row reads `Complete` — FOUND (verified by direct read after edit).

## Requirements Note

`REL-05` is fully discharged by this plan: all 17 stamps read `9.1.0`, VERSION-01 is green, `sync-content.py --check` is clean, and the PASS is proven non-vacuous by mutation — all four of the requirement's own load-bearing claims verified against fresh command output this session.

## Next Phase Readiness

- Release act one (the version bump) is complete and committed. The tree is now at `9.1.0` on all 17 hand-maintained stamps.
- Plan 27-04's 61 FENCED pre-arm sites are unaffected — confirmed by direct diff of the only touched generated file (`first-principles/agents/first-principles.md`), which changed exactly one line.
- Next release acts (matrix-row registration, headline sweep, `[9.1.0]` CHANGELOG entry, post-arm reading) proceed per D-14's ordering — this plan's own commit is the first act inside that bracket.
