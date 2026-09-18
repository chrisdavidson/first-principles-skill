# v9.4 Exemplar Re-Derivation Fixture — backlog 999.118

**Captured:** 2026-09-18. **Status:** frozen hand re-derivation record, appended to (never
rewritten) across plans 44-01 through 44-07. This fixture is NOT registered in
`scripts/check-firewall-battery.sh`'s `_FROZEN_PATHS` array by this plan — plan 44-06 adds that
registration once the artifact is final (registering it now would make `FROZEN-EVIDENCE` fail on
every later plan's in-flight edit to this same file).

## Chain of custody

- **Repo HEAD SHA at the start of Phase 44:** `f7efc17febdfadc62e682d06f40d98017032828d` (read via
  `git rev-parse HEAD` before this plan's Task 1 made any edit).
- **Plugin version:** `9.3.2`, read live via `python3 scripts/check-version-stamps.py` — all 17
  hand-maintained stamps agree, `check-version-stamps: 17 stamps, all '9.3.2'` /
  `check-version-stamps: PASS`. Expected, and confirmed, unchanged for the whole phase per D-04.
- **This fixture records HAND arithmetic re-derivation, not live model capture.** Unlike the
  `tests/confidence-transitivity-v9.4/README.md` precedent (which chains custody through a
  `claude -p` transport command and a `.jsonl`/`.md` sha256 table per capture), no model is
  dispatched to produce this evidence — a human/executor re-computes each exemplar's own stated
  arithmetic with `python3 -c` and records the computed value beside the file's stated value.
  There is therefore no transport command and no capture-pair sha256 table here; the equivalent
  chain-of-custody instrument is the per-source-file hash table below, which pins exactly which
  bytes of `shared/examples/*.md` each recorded re-derivation was checked against.

Per-file source hash table, all 14 files under `shared/examples/`. Pre-edit columns captured live
at the repo HEAD above via `sha256sum` and `wc -l`; post-edit columns are filled by the plan that
last touches each file.

| file | pre-edit sha256 | pre-edit lines | post-edit sha256 | post-edit lines |
|---|---|---|---|---|
| shared/examples/composed-inversion-second-order.md | `3adfedef1542939ccd632589c6b646559eccf6aa8d7fbd8aa2de1c54a57d3377` | 341 | (pending — plan 44-01 Task 2) | (pending — plan 44-01 Task 2) |
| shared/examples/decompose-irreducibility.md | `e91e2bac8d25321aab4620fc688f64e63af291b3b24b2e6041bd805de9e643b2` | 345 | (pending — plan 44-01 Task 2) | (pending — plan 44-01 Task 2) |
| shared/examples/estimate-fermi.md | `7215c0c0485991429eeac27a6e2c612de38511a83c62db97b6fcc79bbac6ef67` | 269 | (pending — plan 44-01 Task 2) | (pending — plan 44-01 Task 2) |
| shared/examples/ishikawa-fishbone.md | `1e78a18f5f4edfbe601a0b230997ac474ef802b369e64904123581171ee713cb` | 355 | (pending — plan 44-01 Task 2) | (pending — plan 44-01 Task 2) |
| shared/examples/personal-general-2.md | `993e00534d49333514865d7222df537b3e8edd6eb0143af5cdd29a900b76767d` | 124 | (pending — plan 44-02) | (pending — plan 44-02) |
| shared/examples/personal-general.md | `5e43d95329b2ca52fb6699601b382f11b5ea26cc7a992b83c891732d3301dea7` | 101 | (pending — plan 44-03) | (pending — plan 44-03) |
| shared/examples/product-business-2.md | `052691ec3a851f1d3b8dcb4aa2ff7cd0cad1b58cf22f127ae12c76ee32630935` | 211 | (pending — plan 44-03) | (pending — plan 44-03) |
| shared/examples/product-business.md | `d948f9fda657dba4fc8c66fd9e60c5846d837c8b78655e1c2b41d2a8fe2b42c4` | 94 | (pending — plan 44-04) | (pending — plan 44-04) |
| shared/examples/science-engineering-2.md | `282db9d21c058c7ed1dd05df45dd328eded851a7bb1d1ae7e38e379f09264aa5` | 218 | (pending — plan 44-06) | (pending — plan 44-06) |
| shared/examples/science-engineering.md | `d5aed303b62e07f1d7ab00e4d171af2ef60a02e9009af156336095b4f4bdfe54` | 187 | (pending — plan 44-05) | (pending — plan 44-05) |
| shared/examples/self-application.md | `47adb0226654cb6246b0004d83c399a81431ebcba98f9509fd61228beda0ce11` | 399 | out of scope (D-03) — pre-edit and post-edit values must be identical | out of scope (D-03) — pre-edit and post-edit values must be identical |
| shared/examples/software-systems-2.md | `66c6548e402398c5f2c18acca34b5323d10a9ab6781754251034f265b5d9d596` | 346 | (pending — plan 44-01 Task 2) | (pending — plan 44-01 Task 2) |
| shared/examples/software-systems.md | `9c883ea780c2ddde363147d86db91f1ad20212b29eccc07b8dbacc03d7e3fa61` | 301 | (pending — plan 44-04) | (pending — plan 44-04) |
| shared/examples/theoretical-limit-carnot.md | `7e8949ab65ae678ad11dda352a73e43f97063515f614c1ab5d1aee1ee06aa594` | 197 | (pending — plan 44-01 Task 2) | (pending — plan 44-01 Task 2) |

## Pre-edit gate baseline

Every command below was run live at the repo HEAD recorded above, immediately before this plan's
Task 2 made any content edit. Verbatim final line of each:

```text
$ python3 scripts/sync-content.py --check
(no output; exit 0 — shared/ and the generated tree are in sync)

$ python3 scripts/check-conf-gate.py
check-conf-gate: PASS

$ python3 scripts/report-conformance.py --check
report-conformance: PASS — no drift

$ bash scripts/check-firewall-battery.sh
FIREWALL: GREEN (23/23)
```

`check-conf-gate.py`'s live run also printed its standing COVERAGE line
(`check-conf-gate: COVERAGE — measured 28 artifacts across shared-examples, generated-twin`) and
three `D-08` synthetic-injection self-check lines
(`D-08(a) hop re-wrap on shared/examples/personal-general.md — heading_malformed_blocks 0 -> 1`,
`D-08(b) verdict-cell strip on shared/examples/personal-general.md — nonconforming_verdict_cells
0 -> 1`, `D-08(c) citation removal on shared/examples/personal-general.md — silent_untraced_claims
0 -> 1`) — these are the script's own built-in mechanical-defect-detector self-check, run against a
disposable in-memory mutation, not a finding against the committed file; the script's own exit
code and terminal `PASS` line are the pass/fail signal.

44-RESEARCH.md's "Gate Impact, Re-Confirmed 2026-09-18" section captured `FIREWALL: GREEN (23/23)`,
`check-conf-gate.py` clean and `report-conformance.py --check` clean on 2026-09-18. **This run
reproduces that baseline exactly** — same verdict, same gate count (23/23), all 23 individual
gates `[PASS]` (confirmed by reading the full battery output line by line: DUAL-04, GATE-02-v8.5,
STEP0-06, STEP0-08, VAL-01, VAL-02, VAL-03, VERSION-01, REG-GUARD, GATE-01, BATT-06, TRACE-03,
QUAL-01, PROV-GUARD, HARN-01, HARN-02, HARN-03, SCAN-GUARD, HC-BOUND, CONF-GATE, CONF-SURFACE,
INVARIANT-CHECK, FROZEN-EVIDENCE — all `[PASS]`).

## Corrected-defect re-derivations (999.118 steps 1-2)

### personal-general-2.md          (plan 44-02)

*(pending - plan 44-02)*

### personal-general.md            (plan 44-03)

*(pending - plan 44-03)*

### product-business-2.md          (plan 44-03)

*(pending - plan 44-03)*

### product-business.md            (plan 44-04)

*(pending - plan 44-04)*

### software-systems.md            (plan 44-04)

*(pending - plan 44-04)*

### science-engineering.md         (plan 44-05)

*(pending - plan 44-05)*

### science-engineering-2.md       (plan 44-06)

*(pending - plan 44-06)*

## ?-suffix / D-07 confidence sweep (999.118 step 3)

Per-file sweeps for the seven defective files above are appended by the plan that owns each file
(44-02 through 44-06). The sweep over the seven untested files is filled below by this plan's
Task 2, under its own `### Untested seven` sub-heading.

*(filled by plan 44-01 Task 2 for the untested seven; filled by plans 44-02–44-06 for the seven
defective files)*

## Untested-exemplar re-derivation (999.118 step 4)

*(filled by plan 44-01 Task 2)*

## Adversarial-corpus inheritance (recorded, never fixed - D-05)

*(filled by plan 44-01 Task 3)*

## Finding

*(pending - plan 44-06)*

## Why registering this path is not a new gate

`FROZEN-EVIDENCE` in `scripts/check-firewall-battery.sh` (confirmed by direct read of lines
740-787) is an inline check whose `TOTAL=$((TOTAL + 1))` line fires exactly once, unconditionally,
**outside** any loop over `_FROZEN_PATHS` — there is no per-array-element loop anywhere in the
check; the entire array is passed as a single pathspec to one `git diff --quiet HEAD --
"${_FROZEN_PATHS[@]}"` call and one `git status --porcelain --untracked-files=all --
"${_FROZEN_PATHS[@]}"` call, and the pass/fail printf plus the `TOTAL`/`PASS` increments happen
once after both. Registering `tests/exemplar-rederivation-v9.4` as one more `_FROZEN_PATHS` entry
therefore adds zero to the battery's 23/23 tally and registers no new gate — which is what keeps
this phase inside `.planning/STATE.md` standing instruction 2 ("No new registered gate. A battery
or CI total may fall only for a gate named in a successor retirement record"). Verified directly
against the live script text in this session, not copied from the `tests/confidence-transitivity-
v9.4/README.md` precedent's own claim.

This plan (44-01) deliberately does NOT add the registration — plan 44-06 does that once the
artifact reaches its final, post-edit form. Registering an in-flight file here would make
`FROZEN-EVIDENCE` fail on every subsequent plan's edit to this same README, since the check reads
`git diff --quiet HEAD` over the registered pathspec and every plan 44-02 through 44-07 commits a
content change to this file.

## Frozen-evidence discipline

Once registered by plan 44-06, this file (and any sibling file placed in
`tests/exemplar-rederivation-v9.4/`) is committed as-is and never regenerated or silently
hand-edited to match a later result. A correction to something already committed here would be
recorded as a dated, additive erratum appended below the point of error — following the pattern
`tests/confidence-transitivity-v9.4/README.md`'s own "Erratum" section uses — never as a rewrite
of the original text. Until plan 44-06's registration lands, this file is an ordinary tracked file
under active construction across this phase's plans; the discipline described in this section
begins to apply once `_FROZEN_PATHS` names it.

`FROZEN-EVIDENCE`'s protection has a documented gap, carried forward from the precedent: it is a
`git diff --quiet HEAD` over the registered pathspec plus a separate untracked-files sweep. It
catches an edit to a file already tracked at HEAD, and it catches an untracked file appearing
inside the directory — but a committed `git rm` of one of these files passes it clean. It is
tamper-evidence for modification, not a deletion guard.
