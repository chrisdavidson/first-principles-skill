#!/usr/bin/env bash
# scripts/check-firewall-battery.sh
#
# One-shot offline battery runner — Phase 128 READY-03 (D-06).
#
# Runs all 23 offline gate commands, captures each exit code, and prints a
# FIREWALL: GREEN / RED / BLOCKED verdict. A GREEN result is the hard
# authorization gate for the Phase-129/130 live runs (D-01). VAL-01 (claude
# plugin validate) is a CLI schema check that spends ZERO model tokens and is
# explicitly permitted inside this offline firewall.
#
# Usage:  bash scripts/check-firewall-battery.sh
# Exits:  0 = FIREWALL GREEN   (all gates pass, no unmet prerequisite)
#         1 = FIREWALL RED     (one or more gates genuinely failed)
#         2 = FIREWALL BLOCKED (no gate failed, but a prerequisite is unmet —
#             currently only VAL-03's pytest interpreter; see below)
#
# Gates (23):
#   DUAL-04   GATE-02-v8.5  STEP0-06  STEP0-08  VAL-01
#   VAL-02    VAL-03        VERSION-01  GATE-01
#   BATT-06   TRACE-03      QUAL-01   HARN-01   HARN-02
#   HARN-03   HC-BOUND      REG-GUARD PROV-GUARD SCAN-GUARD
#   CONF-GATE   CONF-SURFACE  INVARIANT-CHECK
#   FROZEN-EVIDENCE
#
# 20 of the 21 non-inline gates are registered through the `gate` helper
# below. VAL-03 is registered through EITHER `gate` (a pytest-capable
# interpreter was resolved for its third leg) OR `gate_prereq` (none was —
# see "VAL-03 pytest resolution" below); either way it occupies exactly one
# of the 21 tally slots. The final two (INVARIANT-CHECK, FROZEN-EVIDENCE) are
# inline checks that each increment the same PASS/FAIL/TOTAL tally rather
# than going through `gate`, for a reported total of 23.
#
# VAL-03 pytest resolution (SHIP-06, plan 03-08):
# VAL-03's third leg runs scripts/check-links_anchors_test.py under pytest.
# `resolve_pytest_python` (below) picks the interpreter that runs it:
# $REPO/.venv/bin/python3 first, then `python3` — each confirmed by an
# `import pytest` execution preflight, never by parsing any pytest run's own
# output, so a real test failure whose text happens to mention pytest can
# never be reclassified as a missing prerequisite. Set FIREWALL_PYTEST_PYTHON
# to override with a single named candidate (no fallback) — it exists so
# this file's own measurements can drive every outcome deterministically,
# and it is still subject to the same preflight, so it cannot be used to
# fake a pass. If no candidate can import pytest, VAL-03 still runs its
# first two legs (check-links.py --self-test, check-links.py) — a failure
# there is reported as a genuine [FAIL] and outranks the prerequisite gap —
# and, only if both pass, reports [PREREQ] instead of [PASS] and increments
# a PREREQ counter (never PASS). GREEN now requires FAIL == 0 AND
# PREREQ == 0; an unmet prerequisite alone yields FIREWALL: BLOCKED and
# exit 2, a third, distinguishable, still-non-zero outcome — never GREEN,
# and never confused with a genuine gate failure (FIREWALL: RED, exit 1).
# Rejected: `uv run --with pytest`, which would resolve and potentially fetch
# a package from a remote index on every battery run — this script is by
# construction an OFFLINE firewall, and only already-installed interpreters
# are used.
#
# Composition change (HARNESS-01, Phase 164 -- docs/v8.7-quality-baseline-freeze.md):
# the battery gained one gate, QUAL-01, the promoted quality-measurement
# harness's offline self-test (scripts/check-quality-harness.py --self-test),
# which is what keeps the harness's eight labelled self-test items running
# after Phase 164 ends. Battery composition moved 15 -> 16. A gate that
# appears silently is indistinguishable from a gate that was always there.
#
# Composition change (TEARDOWN-01, docs/v8.7-constraint-teardown.md): the
# body-budget gate was retired -- its reporting script became report-only and
# always exited 0, so tallying it would have inflated the count with a gate
# that can never fail. It was still reported below as an un-tallied [INFO]
# line so the body's line count stayed visible on every run; the drop was
# named here rather than silently absorbed. Battery composition moved
# 16 -> 15 as a result. That un-tallied [INFO] body-size line and its
# report-only reporter script were themselves retired under
# docs/v9.4-gate-retirement.md section 2.5; the tally is unchanged by this
# further retirement, since the line was never counted in it.
#
# Composition change (audit 2026-08-16 stream 0 --
# docs/audit-2026-08-16-duplication-staleness.md): the battery gained one gate,
# VERSION-01 (scripts/check-version-stamps.py), which asserts that all 17
# hand-maintained version stamps carry the same value. Plugin installs are
# version-gated rather than content-gated, so a single missed stamp ships an
# inert update while every other gate stays green -- the v8.14 failure mode.
# Nothing previously asserted stamp EQUALITY: sync-content.py copies
# metadata.version through per-file, and the documented "version string
# invariant" checks the stamp's FORMAT, not its agreement with the other 16.
# This gate also runs its live scan, not just its self-test, because the
# invariant is a property of the working tree. Battery composition moved
# 16 -> 17. A gate that appears silently is indistinguishable from a gate that
# was always there.
#
# Composition change (HARN-04, Phase 4, v8.18.0): the battery gained three
# gates — HARN-01 (scripts/check-act-limb.py), HARN-02
# (scripts/check-loop-closure.py), and HARN-03 (scripts/check-focused-parity.py).
# HARN-01 guards the Act limb (the Phase 3 verification step and the
# Criterion 3 Fix note are present, correctly placed, and internally coherent
# in the emitted tree); HARN-02 guards the Observe->Perceive re-entry edges
# (a fired edge is bounded to one re-perception pass and is recorded); HARN-03
# guards focused-mode parity (stub surface, agent surface, and cross-surface
# parity-token set equality). All three scripts existed and passed standalone
# since Phases 1-3 with nothing registering them — this closes that gap.
# Battery composition moved 17 -> 20 (18 `gate`/`gate_prereq` registrations
# plus the 2 inline checks, INVARIANT-CHECK and FROZEN-EVIDENCE).
#
# Each of the three registers as a single `--self-test`-only `gate` call, not
# the two-command `--self-test` + live shape some other gates use: every one
# of the three self-tests already contains a positive control that runs over
# the real, live emitted tree (check-act-limb (a)/(b) over the body and
# rubric; check-loop-closure (a), "the live tree itself must be clean";
# check-focused-parity (a)/(a2)/(a3) over the stub, agent, and cross-surface
# targets), so a separate live invocation at the registration site would
# assert nothing the self-test does not already assert.
#
# Accepted residual, stated rather than absorbed: if a future refactor removes
# one of those internal positive controls, that gate's registration becomes
# vacuous with respect to the shipped tree, and nothing at the registration
# site itself would notice. This was surfaced, weighed, and accepted rather
# than guarded against here — no guard checking that every gate script is
# registered is added in this phase; it is explicitly out of scope.
#
# A gate that appears silently is indistinguishable from a gate that was
# always there.
#
# Composition change (HC-BOUND, Phase 6, v8.19.0): the battery gained one gate,
# HC-BOUND (scripts/check-high-confidence-bound.py --self-test). HC-BOUND asserts
# the tightened Criteria 3 and 5 HIGH-confidence bound is present and well-formed
# in the Self-Audit rubric, and that all three documented EXCEPT exceptions are
# present on both rubric surfaces (canonical and emitted). The gate registers as a
# single `--self-test`-only `gate` call because its self-test already contains
# positive controls (a, a2, a3) that run over the real, live rubric files, so a
# separate live invocation would assert nothing the self-test does not already assert.
# Battery composition moved 20 -> 21. A gate that appears silently is
# indistinguishable from a gate that was always there.
#
# Composition change (REG-GUARD, Phase 3, v8.21.0): the battery gained one gate,
# REG-GUARD (scripts/check-registration.py). REG-GUARD asserts registration
# completeness over two surfaces: (a) every skill directory and the main agent
# carry a frontmatter `name:` matching their own basename; (b) every gate
# registered in this file has a matching `name: <job> (<GATE-ID>)` job in
# .github/workflows/validation.yml, the gates named in BATTERY_ONLY_GATE_IDS
# excepted. It registers as a `--self-test` + live `gate` call, for
# the same reason VERSION-01 does: the self-test is fixture-isolated, so it
# alone asserts nothing about the shipped tree.
# REG-GUARD: Battery composition moved 21 -> 22. A gate that appears silently
# is indistinguishable from a gate that was always there.
#
# Composition change (PROV-GUARD, Phase 6, v8.24.0): the battery gained one
# gate, PROV-GUARD (scripts/check-provenance.py). PROV-GUARD joins every
# *Provenance: read-at-source* ground truth in an analysis's section 3 to a
# real WebFetch/Read of that source in the run's stored .jsonl capture, and
# requires every literal it states to appear verbatim in that source's
# retrieved text. It registers as `--self-test` + live, for the same reason
# REG-GUARD does: the self-test's fixtures are tempdir/in-memory, so the
# self-test alone asserts nothing about the committed capture at
# tests/quality-provenance-v8.24/ — the live leg reads 7/7 sources matched,
# 35/35 literals located.
# PROV-GUARD: Battery composition moved 22 -> 23. A gate that appears
# silently is indistinguishable from a gate that was always there.
#
# Composition change (SCAN-GUARD, Phase 15, unreleased at time of writing —
# .claude-plugin/marketplace.json still reads 8.25.0, and VERSION-01 moves all
# 17 stamps in lockstep at release): the battery gained one gate, SCAN-GUARD
# (scripts/check-selfaudit-scan.py). SCAN-GUARD guards the Phase 15 self-audit
# scan prescription (shared/spine/SKILL-body.md's chain-form and
# claim-inventory tables), its rubric verify block (Criterion 4/6 quote-source
# sentences in shared/spine/references/validation-rubric.md), and the
# Criterion-2-widened Verdict Block Format admission (plan 15-08), as emitted
# in the tree. It runs `--self-test` plus the bare live leg (plan 15-09,
# matching PROV-GUARD/REG-GUARD); the tally below is unchanged because gate()
# counts once per gate id regardless of how many commands run under it.
# SCAN-GUARD: Battery composition moved 23 -> 24.
#
# Composition change (CONF-GATE, Phase 18, v9.0.0): the battery gained one
# gate, CONF-GATE (scripts/check-conf-gate.py). CONF-GATE compares four
# conformance counts (unreadable, heading_malformed_blocks,
# nonconforming_verdict_cells, silent_untraced_claims) on both gated example
# surfaces (shared-examples, generated-twin) against source-literal zero
# targets held in its own source — never against docs/data/conformance.json,
# which is regenerated from the same tree and could therefore never fire
# (the 999.30/999.31 defect class). It registers as `--self-test` + live, for
# the same reason PROV-GUARD and SCAN-GUARD do: the self-test's rows are
# synthetic and assert nothing about the shipped corpus.
# CONF-GATE: Battery composition moved 24 -> 25. A gate that appears silently
# is indistinguishable from a gate that was always there.
#
# Composition change (CONF-SURFACE, Phase 21, D-21-C): the battery gained one
# gate, CONF-SURFACE (scripts/gen-gate-docs.py). CONF-SURFACE is the drift
# gate for the generated CI-gate claim surface itself: it regenerates
# CLAUDE.md's and docs/ARCHITECTURE.md's gate tables and docs/gates/<ID>.md
# pages from scripts/_gate_registry.py's ENTRIES and every gate's --describe
# emission, and fails if the committed tree has drifted from that
# regeneration or if its own standing CONF-13 literal scanner finds a
# non-exempt hand-maintained count literal. It registers as `--self-test`
# then `--check`, self-test first, per the WR-05 ordering lesson
# (18-VERIFICATION.md): a broken generator's own controls must be caught
# before its comparison against committed output is even attempted, since
# that comparison is meaningless if the generator is broken.
# CONF-SURFACE: Battery composition moved 25 -> 26. A gate that appears
# silently is indistinguishable from a gate that was always there.
#
# Composition change (COLLIDE-01 retired, Phase 40, v9.4.0 --
# docs/v9.4-gate-retirement.md §2.1): the battery lost one gate, COLLIDE-01
# (scripts/check-install-collisions.py). Its live scan compared the plugin's
# names against a second, monolith install surface that was removed at
# v3.0.0, well before this gate's own registration at v7.9 -- "monolith
# names: 0" on every run means it could never fail for any product reason.
# The name-versus-directory property it was believed to enforce is, and was
# already, owned entirely by REG-GUARD and GATE-01. Battery composition
# moved 26 -> 25. A gate that disappears silently is indistinguishable from
# a gate that never fired.
#
# Composition change (VAL-04 retired, Phase 40, v9.4.0 --
# docs/v9.4-gate-retirement.md §2.2): the battery lost one gate, VAL-04
# (the v3.0 4-gram trigger-collision scanner, carrying extra id GATE-02). With
# every shipped skill stub slash-only (disable-model-invocation: true), only
# one routing description -- the agent's own -- remains in the model's
# context, and a 4-gram collision needs two competing descriptions; the scan
# could not fail for any reason that affects routing. The property it was a
# proxy for -- every stub carrying disable-model-invocation: true -- is now
# asserted inside REG-GUARD's existing entry (plan 40-05), not a new
# registered gate. Battery composition moved 25 -> 24.
#
# Composition change (VAL-05 retired, Phase 40, v9.4.0 --
# docs/v9.4-gate-retirement.md §2.3): the battery lost one gate, VAL-05
# (the retired 2,000-character combined skill-description budget scan). The
# platform documents no such ceiling -- the only figure it states for this
# surface is a 1,536-character *combined* description+when_to_use truncation
# in the skill listing, and every shipped skill stub is
# disable-model-invocation: true (§2.2), so that listing never renders for
# any of them. No successor limit is added, because the only documented
# ceiling would guard a listing the slash-only stubs are not in.
# Battery composition moved 24 -> 23.
#
# Composition NON-change (PROV-GUARD relaxed to battery-only, Phase 40, v9.4.0
# -- docs/v9.4-gate-retirement.md §2.4, backlog 999.107, option B): PROV-GUARD's
# CI job and the battery's bare live leg are both removed; the `--self-test`
# command stays, in QUAL-01's own call shape, as one `gate` call. Battery
# composition is UNCHANGED -- still one `gate "PROV-GUARD"` registration,
# now `--self-test`-only -- because gate() counts once per gate id regardless
# of how many commands run under it. CI moves from 20 jobs to 19 (the
# check-provenance job is deleted); PROV-GUARD joins QUAL-01 in
# BATTERY_ONLY_GATE_IDS, so battery-only-by-design rises from 1 to 2.
#
# Composition change (CONF-DRIFT, Phase 90, backlog 999.38): Phase 89 D-01
# removed `report-conformance.py --check` from both pre-commit hooks, and the
# gate registry recorded it as "battery only" -- but no line in this file ran
# it, so between Phase 89 and Phase 90 the check ran nowhere. Phase 90
# registers it here as a third INLINE check (CONF-DRIFT), the shape of
# INVARIANT-CHECK and FROZEN-EVIDENCE: a bare TOTAL increment, never a `gate`
# call, so REG-GUARD's _BATTERY_GATE_RE does not parse it and it needs neither
# a CI job nor a widened BATTERY_ONLY_GATE_IDS. Battery composition moves
# 32 -> 33.
#
# Composition NON-change, recorded deliberately (WR-05, Phase 20 20-REVIEW):
# scripts/report-conformance.py is NOT registered here, and its ~98-control
# --self-test battery is NOT a gate in this file. That was already the standing
# decision for its --check leg (D-06, .planning 17-CONTEXT.md), recorded until
# now only in the two pre-commit hook headers; the review found that the
# --self-test leg had inherited the same non-registration by silence rather
# than by decision, so nothing automated ran ANY of those controls -- which is
# the direct reason a missing positive arm (CR-02) shipped able to hide the
# deletion of an entire enforcement floor.
#
# Why it stays out of this file rather than becoming gate 27:
#   - REG-GUARD's CI-job axis requires every gate registered here to have a
#     matching `name: <job> (<GATE-ID>)` job in .github/workflows/validation.yml,
#     with the gates named in BATTERY_ONLY_GATE_IDS excepted. Registering a gate
#     here therefore forces either a new CI job or a widened exemption set, and
#     widening that exemption list is exactly what makes the axis weaker.
#   - The generator's --check leg is a STALENESS check against a regenerated
#     baseline. It belongs at commit time, where the staleness is created, not
#     in an offline battery whose GREEN result authorizes live runs.
# Battery composition is UNCHANGED at 26 by this non-decision (report-conformance.py
# itself; CONF-SURFACE, a different generator, is what moved it 25 -> 26 above).
#
# Where those controls now run instead: both pre-commit hooks (.githooks/pre-commit
# and scripts/git-hooks/pre-commit) run `report-conformance.py --self-test` as
# their gate 2, ahead of the existing --check as gate 3. A gate that appears
# silently is indistinguishable from a gate that was always there -- and so is a
# gate that was deliberately never added.
#
# Superseded for the --check leg only (Phase 90, backlog 999.38): once Phase 89
# D-01 took --check out of both hooks, keeping it out of this file left it
# running nowhere, so --check now runs here as the inline CONF-DRIFT check
# (see the composition-change paragraph above). The --self-test leg remains
# unregistered here and stays in both pre-commit hooks as their gate 2.
#
# NOTE: set -u is active; set -e is intentionally ABSENT — every gate must run
# and be tallied even if an earlier gate fails (no early abort).

set -u

# Resolve repo root from this script's location so it runs from any cwd.
REPO=$(cd "$(dirname "$0")/.." && pwd)
cd "$REPO"

# Every Python process this battery starts, and every child they spawn, uses
# a bytecode cache that begins empty and dies with this run. CPython trusts a
# __pycache__ entry whose recorded source mtime (whole seconds) and size match,
# so a same-size edit made within the second -- a mutate-run-restore probe --
# can be served stale bytecode in either direction: the mutation unseen, or
# the restored file read as still mutated. Disabling writes alone still READS
# a stale entry. Redirecting the cache to a fresh per-run directory means no
# entry from an earlier run is ever read, while processes within this run,
# where no source is edited, still share compiled modules (writes stay on:
# turning them off measured 212s -> 450s for a full battery).
PYCACHE_DIR=$(mktemp -d "${TMPDIR:-/tmp}/fp-battery-pycache.XXXXXX")
trap 'rm -rf "$PYCACHE_DIR"' EXIT
export PYTHONPYCACHEPREFIX="$PYCACHE_DIR"

TOTAL=0
PASS=0
FAIL=0
PREREQ=0

# ---------------------------------------------------------------------------
# gate <gate-id> <display-cmd> <bash-cmd> [<bash-cmd2> ...]
#
# Runs each bash-cmd via `bash -c`. Gate passes only if every sub-command
# exits 0. Prints one [PASS]/[FAIL] line per gate. Stdout/stderr suppressed.
# ---------------------------------------------------------------------------
gate() {
    local gate_id="$1"
    local display_cmd="$2"
    shift 2
    local gate_exit=0
    local cmd_str
    for cmd_str in "$@"; do
        bash -c "$cmd_str" >/dev/null 2>&1 || gate_exit=1
    done
    TOTAL=$((TOTAL + 1))
    if [ "$gate_exit" -eq 0 ]; then
        printf "[PASS] %-14s  %s\n" "$gate_id" "$display_cmd"
        PASS=$((PASS + 1))
    else
        printf "[FAIL] %-14s  %s\n" "$gate_id" "$display_cmd"
        FAIL=$((FAIL + 1))
    fi
}

# ---------------------------------------------------------------------------
# gate_prereq <gate-id> <display-cmd> <reason> <bash-cmd> [<bash-cmd2> ...]
#
# Same run-and-tally shape as `gate`, for a gate whose full form has an
# unmet EXTERNAL prerequisite (currently: no pytest-capable interpreter for
# VAL-03's third leg). Runs every supplied sub-command exactly as `gate`
# does, via `bash -c ... >/dev/null 2>&1`, and increments TOTAL exactly once.
#
#   - If any supplied sub-command failed, the prerequisite gap is
#     irrelevant — a real failure OUTRANKS it. Prints [FAIL] and increments
#     FAIL, identically to `gate`. This is what stops the prerequisite
#     branch from converting a genuine leg-1/leg-2 failure into a skip.
#   - Only when every supplied sub-command passed does it print [PREREQ]
#     carrying <reason> and increment the PREREQ counter. It never
#     increments PASS — an unmet prerequisite is not a pass.
# ---------------------------------------------------------------------------
gate_prereq() {
    local gate_id="$1"
    local display_cmd="$2"
    local reason="$3"
    shift 3
    local gate_exit=0
    local cmd_str
    for cmd_str in "$@"; do
        bash -c "$cmd_str" >/dev/null 2>&1 || gate_exit=1
    done
    TOTAL=$((TOTAL + 1))
    if [ "$gate_exit" -ne 0 ]; then
        printf "[FAIL] %-14s  %s\n" "$gate_id" "$display_cmd"
        FAIL=$((FAIL + 1))
    else
        printf "[PREREQ] %-14s  %s\n" "$gate_id" "$reason"
        PREREQ=$((PREREQ + 1))
    fi
}

# ---------------------------------------------------------------------------
# resolve_pytest_python
#
# Echoes the path of the first candidate interpreter that can `import
# pytest`, and returns non-zero having echoed nothing if no candidate can.
#
# Candidate order:
#   - If FIREWALL_PYTEST_PYTHON is set and non-empty, it is the ONLY
#     candidate — no fallback. This exists so this file's own measurements
#     can drive every VAL-03 outcome deterministically. It is still subject
#     to the same import preflight below, so it cannot be used to fake a
#     pass.
#   - Otherwise: $REPO/.venv/bin/python3, then `python3` (resolved via PATH).
#
# The test for each candidate is an EXECUTION preflight — run the candidate
# with `-c 'import pytest'`, stdout/stderr suppressed — never a parse of any
# pytest run's output, so a real test failure whose text happens to mention
# pytest can never be reclassified as a missing prerequisite. `command -v`
# guards a candidate that is not an executable file at all (a bad
# FIREWALL_PYTEST_PYTHON, or an absent .venv), so this reports "not usable"
# instead of erroring under `set -u`.
# ---------------------------------------------------------------------------
resolve_pytest_python() {
    local candidates=()
    if [ -n "${FIREWALL_PYTEST_PYTHON:-}" ]; then
        candidates=("$FIREWALL_PYTEST_PYTHON")
    else
        candidates=("$REPO/.venv/bin/python3" "python3")
    fi
    local cand
    for cand in "${candidates[@]}"; do
        if command -v "$cand" >/dev/null 2>&1; then
            if "$cand" -c 'import pytest' >/dev/null 2>&1; then
                echo "$cand"
                return 0
            fi
        fi
    done
    return 1
}

echo "=== Phase 128 Offline Firewall Battery (READY-03 / D-06) ==="
echo ""

# DUAL-04 — shared/ and generated first-principles/ tree are in sync
gate "DUAL-04" \
    "sync-content.py --check" \
    "python3 scripts/sync-content.py --check"

# GATE-02-v8.5 — pointer drift-guard: each of the four split core files'
#                extracted Procedure slice carries exactly one well-formed
#                link to its own detail sibling (positive + missing/duplicate
#                negative controls + main() dispatch control, D-11). Proves
#                the pointer exists and is well-formed, NOT that it is
#                followed. Milestone-qualified label disambiguates it from
#                the pre-existing v3.0 GATE-02 (trigger-collision scanner).
gate "GATE-02-v8.5" \
    "sync-content.py --self-test (pointer drift-guard)" \
    "python3 scripts/sync-content.py --self-test"

# STEP0-06 — Step 0 live-harness self-test (decompose-absence, routing-count,
#             v7.13-emitter-target, routing-emitter-absence guards included)
gate "STEP0-06" \
    "check-step0-live.py --self-test" \
    "python3 scripts/check-step0-live.py --self-test"

# STEP0-08 — offline phrase-detection emulator self-test
gate "STEP0-08" \
    "check-step0-emulator.py --self-test" \
    "python3 scripts/check-step0-emulator.py --self-test"

# VAL-01 — claude plugin validate (CLI schema check; ZERO model tokens; D-01)
gate "VAL-01" \
    "claude plugin validate ./first-principles" \
    "claude plugin validate ./first-principles"

# VAL-02 — markdownlint across first-principles/**/*.md
gate "VAL-02" \
    "markdownlint-cli2 first-principles/**/*.md" \
    "markdownlint-cli2 --config .markdownlint.jsonc 'first-principles/**/*.md'"

# VAL-03 — check-links.py --self-test (v8.5 GATE-01) + relative MD link
#           validity + anchor tests. Leg 3 needs a pytest-capable
#           interpreter, resolved by resolve_pytest_python() (see header
#           comment "VAL-03 pytest resolution"). When none is found, legs 1
#           and 2 still run through gate_prereq — a failure there still
#           reports [FAIL]/RED, and only a clean pass of both reports
#           [PREREQ]/BLOCKED instead of [PASS]/GREEN.
_val03_python=$(resolve_pytest_python)
if [ -n "$_val03_python" ]; then
    gate "VAL-03" \
        "check-links.py --self-test + live + $_val03_python -m pytest check-links_anchors_test.py" \
        "python3 scripts/check-links.py --self-test" \
        "python3 scripts/check-links.py" \
        "$_val03_python -m pytest scripts/check-links_anchors_test.py -q"
else
    if [ -n "${FIREWALL_PYTEST_PYTHON:-}" ]; then
        _val03_reason="no pytest-capable interpreter found — FIREWALL_PYTEST_PYTHON=$FIREWALL_PYTEST_PYTHON was the only candidate (override in effect, no fallback) and could not import pytest, or is not an executable file; the anchors test did NOT run. Remedy: unset FIREWALL_PYTEST_PYTHON to use the default resolution order (\$REPO/.venv/bin/python3, then python3), or point it at an interpreter that has pytest installed."
    else
        _val03_reason="no pytest-capable interpreter found — tried $REPO/.venv/bin/python3 and python3, neither could import pytest; the anchors test did NOT run. Remedy: run 'uv sync' to create .venv (ships pytest), or install pytest for whichever interpreter 'python3' resolves to."
    fi
    gate_prereq "VAL-03" \
        "check-links.py --self-test + live (pytest anchors test SKIPPED — no interpreter)" \
        "$_val03_reason" \
        "python3 scripts/check-links.py --self-test" \
        "python3 scripts/check-links.py"
fi

# VERSION-01 — every hand-maintained version stamp carries the same value.
# Runs the live scan as well as the self-test: unlike most gates here, the
# invariant is a property of the working tree, not of the script's fixtures.
gate "VERSION-01" \
    "check-version-stamps.py --self-test + live" \
    "python3 scripts/check-version-stamps.py --self-test" \
    "python3 scripts/check-version-stamps.py"

# REG-GUARD — registration completeness over two surfaces: (a) every skill
#             directory and the main agent carry a frontmatter `name:` matching
#             their own basename; (b) every gate registered in THIS file has a
#             matching `name: <job> (<GATE-ID>)` job in
#             .github/workflows/validation.yml, the gates named in
#             BATTERY_ONLY_GATE_IDS excepted (WR-02, v8.24).
#             Runs the live scan as well as the self-test, for the same reason
#             VERSION-01 above does: the self-test is fixture-isolated, so the
#             self-test alone asserts nothing about the shipped tree.
#             Bare `python3`, not `uv run` — see the "Rejected: `uv run
#             --with pytest`" note in this file's header: `uv run` may resolve
#             and fetch from a remote index, and this script is by construction
#             an OFFLINE firewall.
gate "REG-GUARD" \
    "check-registration.py --self-test + live" \
    "python3 scripts/check-registration.py --self-test" \
    "python3 scripts/check-registration.py"

# GATE-01 — agent structural checks (self-test + live agent file).
# The live leg takes no --file: it targets the repo-anchored AGENT_FILE constant,
# so the gate cannot be silently re-pointed and is not cwd-sensitive. It emits a
# COVERAGE line naming the file it validated, backed by an anti-vacuity control.
# GATE-01 is the ONLY gate validating the agent frontmatter — VAL-01 does not
# reach it (see the VAL-01 row in CLAUDE.md).
gate "GATE-01" \
    "check-agent.py --self-test + live shipped agent (AGENT_FILE)" \
    "python3 scripts/check-agent.py --self-test" \
    "python3 scripts/check-agent.py"

# BATT-06 — merged boundary + focused-output battery self-test
gate "BATT-06" \
    "check-routing-battery.py --self-test" \
    "python3 scripts/check-routing-battery.py --self-test"

# TRACE-03 — requirements-traceability self-test
gate "TRACE-03" \
    "check-traceability.py --self-test" \
    "python3 scripts/check-traceability.py --self-test"

# QUAL-01 — quality-measurement harness offline self-test: extraction
#           guardrails A/B, scoreline parser, blinding integrity, tabulation
#           arithmetic, baseline-fixture integrity, defect detector, run-layer
#           composition (HARNESS-01, Phase 164)
gate "QUAL-01" \
    "check-quality-harness.py --self-test" \
    "python3 scripts/check-quality-harness.py --self-test"

# PROV-GUARD — capture-based provenance verification: the self-test
#              regression-tests the verifier's own parsing, join and
#              literal-location logic on in-memory/tempdir fixtures
#              (D-16 positive/negative/anti-masking controls). The bare live
#              leg over the frozen tests/quality-provenance-v8.24/ capture is
#              a manual fixture regression (docs/v9.4-gate-retirement.md
#              §2.4) — run by neither the battery nor CI as of Phase 40,
#              v9.4.0. Registers in QUAL-01's own call shape for the same
#              reason: a single `--self-test`-only `gate` call.
gate "PROV-GUARD" \
    "check-provenance.py --self-test" \
    "python3 scripts/check-provenance.py --self-test"

# HARN-01 — Act limb: the Phase 3 verification step and the Criterion 3 Fix
#           note are present, correctly placed, and internally coherent in
#           the emitted tree
gate "HARN-01" \
    "check-act-limb.py --self-test" \
    "python3 scripts/check-act-limb.py --self-test"

# HARN-02 — Observe->Perceive re-entry edges: a Criterion 1 Absent verdict
#           routes back to Phase 1, every re-entry edge is bounded to one
#           re-perception pass, and a fired edge is recorded
gate "HARN-02" \
    "check-loop-closure.py --self-test" \
    "python3 scripts/check-loop-closure.py --self-test"

# HARN-03 — focused-mode parity: stub surface, agent surface, and
#           cross-surface parity-token set equality
gate "HARN-03" \
    "check-focused-parity.py --self-test" \
    "python3 scripts/check-focused-parity.py --self-test"

# SCAN-GUARD — self-audit scan structural gate: the Phase 15 self-audit scan
#              prescription (agent body), its rubric verify block (Criterion
#              4/6 quote-source sentences), and the Criterion-2-widened
#              Verdict Block Format admission (plan 15-08) are present,
#              correctly placed and internally coherent in the emitted tree;
#              100 clause-level named branches (72 at plan 15-07; 72->86 at
#              plan 15-08 widening the admission to Criterion 2; 86->87 at
#              plan 15-09 splitting Rubric-2's placement predicate into
#              independently falsifiable halves; 87->94 at plan 15-11
#              region-splitting the quoted-span TEMPLATE and the admission
#              paragraph so each independently states both admitted-artifact
#              clauses, closing a gate-locked contradiction where the
#              pre-15-11 template rejected the correct fix; 94->100 at plan
#              15-12 replacing Rubric-11's two hand-written ids with eight
#              parameterized over every _BAND_BULLETS literal) each with
#              their own per-source negative control, an anti-masking
#              assertion, and a roster floored by an independent
#              transcription (_BRANCH_ROSTER_LOCK) so narrowing the registry
#              fails the gate. Runs --self-test plus the bare live leg (plan
#              15-09), matching PROV-GUARD/REG-GUARD. Coverage claim narrowed
#              per 15-REVIEW.md WR-03 — clause-level ids cover every count
#              guard, every multi-literal tuple (measured TRUE file-wide, no
#              named exceptions, plan 15-12) and every cross-surface arm, not
#              one id per arm; eight not-found reporting arms carry no id of
#              their own (net of the one R-02-placement-aa closed). See the
#              gate's own docstring for the full residual ledger (WR-01,
#              IN-04, IN-05, the SCAN-04 character figure; WR-04 is closed by
#              plan 15-12's ENTRY-SOURCE LOCK).
gate "SCAN-GUARD" \
    "check-selfaudit-scan.py --self-test + live" \
    "python3 scripts/check-selfaudit-scan.py --self-test" \
    "python3 scripts/check-selfaudit-scan.py"

# HC-BOUND — HIGH-confidence bound: Phase 5 tightening of Criterion 3 (Evidence)
#            and Criterion 5 (Conclusion) is present and well-formed in the
#            Self-Audit rubric, and all three documented EXCEPT exceptions are
#            present on both rubric surfaces
gate "HC-BOUND" \
    "check-high-confidence-bound.py --self-test" \
    "python3 scripts/check-high-confidence-bound.py --self-test"

# CONF-GATE — standing exemplar-conformance comparator: the four conformance
#             counts (unreadable, heading_malformed_blocks,
#             nonconforming_verdict_cells, silent_untraced_claims) on both
#             gated example surfaces (shared-examples, generated-twin) against
#             source-literal zero targets, the 14-entry claim floor locked by
#             equality to the live-discovered shared-examples ids, the D-03
#             prescribed-lead-in rule, and the marked-claim ratchet. Runs
#             --self-test plus the bare live leg (plan 18-08), matching
#             PROV-GUARD/SCAN-GUARD.
gate "CONF-GATE" \
    "check-conf-gate.py --self-test + live" \
    "python3 scripts/check-conf-gate.py --self-test" \
    "python3 scripts/check-conf-gate.py"

# CONF-SURFACE — the claim-surface drift gate itself (D-21-C): regenerates
#                CLAUDE.md's and docs/ARCHITECTURE.md's gate tables and
#                docs/gates/<ID>.md pages from scripts/_gate_registry.py's
#                ENTRIES and every gate's --describe emission, and fails on
#                drift or a non-exempt CONF-13 literal-scan finding.
#                --self-test runs first (WR-05 ordering: a broken generator's
#                own controls must be caught before --check's comparison
#                against committed output is even attempted), then --check.
#                `gate()` increments TOTAL once regardless of how many
#                commands run under it, so this is one tally slot, not two.
gate "CONF-SURFACE" \
    "gen-gate-docs.py --self-test + --check" \
    "python3 scripts/gen-gate-docs.py --self-test" \
    "python3 scripts/gen-gate-docs.py --check"

# RETRACT-01 — a claim a code review found false may never reappear on a
#              published surface. Added after v9.7.0 shipped seven blocking
#              product defects, two of which were the SAME claim shipping
#              twice: 55-CR-01 retracted the one-phase-per-technique premise,
#              and 58-CR-01 found it three phases later in the requirements
#              matrix, because the requirement statement the matrix row is
#              generated from was never updated alongside the fix.
#              Runs the live scan as well as the self-test: like VERSION-01,
#              the invariant is a property of the working tree, not of the
#              script's own fixtures. The self-test's C8 control already
#              covers the live tree, but the live leg is registered
#              separately so a battery reader sees the tree scanned by name.
gate "RETRACT-01" \
    "check-retracted-claims.py --self-test + live" \
    "python3 scripts/check-retracted-claims.py --self-test" \
    "python3 scripts/check-retracted-claims.py"

# PROV-ROLLUP — the provenance roll-up's enumeration must agree with the
#               section 3 it summarises. Backlog 999.173 asked for a detector
#               over the ONE artifact still traceable to output-template.md
#               alone; the checker shipped at 260924-prv registered nowhere,
#               so its reading gated nothing and 999.176 could ship green.
#               This is that registration residual.
#               Check 1 (presence) and check 3 (read-at-source coverage) are
#               report-only BY DESIGN and cannot fail — emission rate is a
#               K-of-N live reading, which docs/v8.7-constraint-teardown.md
#               §2 item 3 bars from gating anything. Check 2 is the failing
#               check, and it is not a presence check: it compares the
#               enumerated ids against the document's own section 3, so an
#               emitted label cannot satisfy it.
#               Runs --self-test plus a live leg over the 14 shipped
#               exemplars, matching RETRACT-01/CONF-GATE's shape. Since
#               Phase 91 every shipped exemplar carries a roll-up, so the live
#               leg's check 2 compares each one against its own section 3,
#               and the self-test's exemplar floor fails if any exemplar
#               loses its roll-up.
gate "PROV-ROLLUP" \
    "check-provenance-rollup.py --self-test + live exemplars" \
    "python3 scripts/check-provenance-rollup.py --self-test" \
    "python3 scripts/check-provenance-rollup.py --dir shared/examples"

# CHAIN-JUDGE — the offline control suite of the only instrument here that judges
#               SEMANTIC claim-to-chain support rather than citation presence.
#               ONLY --self-test is registered: the live reading disagrees with
#               itself across passes (6 of 10 reached, membership unstable) and
#               has no precision figure, so gating it would manufacture the false
#               confidence the instrument exists to detect. Registered at W2
#               2026-09-27; it had shipped registered nowhere.
gate "CHAIN-JUDGE" \
    "check-claim-chain-judge.py --self-test (offline; live reading NOT gated)" \
    "python3 scripts/check-claim-chain-judge.py --self-test"

# EMIT-STAGE-A — offline controls for the capture protocol that reads the agent's
#               own document instead of the orchestrator's summary of it. Two of
#               its controls exist because they caught real extraction bugs in the
#               script before anyone trusted its numbers.
gate "EMIT-STAGE-A" \
    "check-emission-stage-a.py --self-test" \
    "python3 scripts/check-emission-stage-a.py --self-test"

# EVIDENCE-01 — the public Evidence Card's every published figure is re-read
#               from its cited source, and the committed page reproduces a
#               fresh render byte-for-byte. This is a product-surface guard,
#               not an apparatus one: docs/EVIDENCE.md asserts measured facts
#               to a reader outside the build loop, which is exactly the
#               claim-audience cut docs/PROCESS.md section 2 draws, so a
#               figure there going stale is a product defect.
#               Runs --self-test first (WR-05 ordering: the generator's own
#               controls must pass before its output is compared to anything),
#               then --check. One tally slot, two commands.
gate "EVIDENCE-01" \
    "gen-evidence-card.py --self-test + --check" \
    "python3 scripts/gen-evidence-card.py --self-test" \
    "python3 scripts/gen-evidence-card.py --check"

# TRACKB-01 — the pre-registered comparative harness's own offline controls.
#             Registered in the battery specifically so control C13 runs on
#             every commit: C13 asserts that this script's pinned protocol
#             constants still agree with docs/trackb-preregistration.md's
#             stated text. A pre-registration whose executable form has
#             silently drifted from it is no longer a pre-registration, and
#             that drift is invisible to every other gate in this tree.
#             C01 is the other load-bearing one: it fails if the neutral
#             rubric ever acquires a format token, which would make the
#             comparison reward the agent's output shape rather than its
#             reasoning. Offline and deterministic — it spends nothing and
#             never invokes `claude`; the live run is manual and separate.
gate "TRACKB-01" \
    "check-trackb-comparative.py --self-test" \
    "python3 scripts/check-trackb-comparative.py --self-test"

# SUMM-BLOCK — the structured-summary-block checker's offline controls: finds
#             exactly one block at the end of a report's appendix, validates
#             it against the Phase 74 schema with a stdlib validator, and
#             cross-checks every id and value against the report's own prose.
#             Its must-fail controls are rebuilt in-tree from the real PRD
#             failure reports (a misread re-entry, a missed Fix/Repeat
#             disclosure, a rewritten first scoring pass, a recommendation
#             cut at its own colon), each required to fail for its own
#             finding code while the same report with a correct block stays
#             clean. Widened at Phase 76 to also run `--exemplar` over the
#             fourteen worked examples on both the source and generated-twin
#             surfaces — the fourteen examples are the surface the agent
#             learns the block from, so a later edit drifting one example's
#             prose from its block must not stay silent. `--exemplar`
#             permits a null field only where the example's own source
#             section is absent (D-15); reading live agent reports stays a
#             recorded measurement (Phase 77), never a gate.
gate "SUMM-BLOCK" \
    "check-summary-block.py --self-test + --exemplar worked examples" \
    "python3 scripts/check-summary-block.py --self-test" \
    "python3 scripts/check-summary-block.py --exemplar shared/examples/*.md" \
    "python3 scripts/check-summary-block.py --exemplar first-principles/references/examples/*.md"

# FIG-GATE — renders both figures of the typst library in
#            shared/spine/references/report-figures.md against the real
#            analysis fixture, a two-digit-id worst-case fixture and every
#            worked example's structured-summary block, and asserts through
#            `typst eval 'query(...)'` that drawn-edge, cell and overflow
#            counts match the source JSON exactly, with must-fail mutation
#            controls and a typst-absent exit-2 contract. Needs typst on
#            PATH; when absent, the bash wrapper below — not the script's own
#            exit code — decides [PREREQ]/BLOCKED instead of [PASS]/GREEN,
#            matching VAL-03's own command -v gated branch: gate_prereq
#            reports any non-zero sub-command as [FAIL], so the prerequisite
#            decision has to be made before the self-test is even attempted.
if command -v typst >/dev/null 2>&1; then
    gate "FIG-GATE" \
        "check-report-figures.py --self-test" \
        "python3 scripts/check-report-figures.py --self-test"
else
    gate_prereq "FIG-GATE" \
        "check-report-figures.py --describe (self-test SKIPPED — no typst)" \
        "typst not found on PATH — the figure-rendering self-test did NOT run. Remedy: install typst v0.15.1 (the CI job's pinned tarball; see shared/spine/references/report-figures.md) and Noto Sans or Liberation Sans." \
        "python3 scripts/check-report-figures.py --describe"
fi

# PERSONA-GATE — checks a reader-persona view against the analysis it was
#                derived from and the contract in
#                shared/spine/references/persona-views.md: the provenance
#                header, the band against section 6, the role's word band,
#                that every sentence and bullet carries a citation, and that
#                every cited chain, ground-truth (with matching `?` marking),
#                assumption and dead-end id resolves in the source, plus
#                every number. Also checks the reading guide's names against
#                the output template and its word ceiling. Needs no
#                prerequisite — stdlib Python only, no typst/claude/pytest
#                dependency — so it runs as a plain gate, never gate_prereq.
gate "PERSONA-GATE" \
    "check-persona-view.py --self-test" \
    "python3 scripts/check-persona-view.py --self-test"

# ---------------------------------------------------------------------------
# Invariant re-confirm (D-07) — byte-frozen constants in _battery_core.py.
#
# BATT-06 and STEP0-08 self-tests already internally assert these five constants;
# this block provides explicit value-greps as a direct double-check:
#   pre-mortem=9  fishbone=7  inversion=13  trade-off=10  MIN_HEADER_HITS=2
# The composer-focus ceiling constant was removed from this block when its
# freeze was released under TEARDOWN-02 per docs/v8.7-constraint-teardown.md —
# its value is unchanged (still 4) but no longer asserted here.
# No constant is changed here (re-confirm only, D-07).
# ---------------------------------------------------------------------------
python3 - <<'PYEOF' >/dev/null 2>&1
import sys
sys.path.insert(0, 'scripts')
from _battery_core import _TECHNIQUE_CATEGORIES as T, MIN_HEADER_HITS as MH
assert len(T['pre-mortem'])==9,  f"pre-mortem expected 9, got {len(T['pre-mortem'])}"
assert len(T['fishbone'])==7,    f"fishbone expected 7, got {len(T['fishbone'])}"
assert len(T['inversion'])==13,  f"inversion expected 13, got {len(T['inversion'])}"
assert len(T['trade-off'])==10,  f"trade-off expected 10, got {len(T['trade-off'])}"
assert MH==2,  f"MIN_HEADER_HITS expected 2, got {MH}"
PYEOF
_inv_exit=$?

TOTAL=$((TOTAL + 1))
if [ "$_inv_exit" -eq 0 ]; then
    printf "[PASS] %-14s  %s\n" "INVARIANT-CHECK" \
        "pre-mortem=9 fishbone=7 inversion=13 trade-off=10 MIN_HEADER_HITS=2"
    PASS=$((PASS + 1))
else
    printf "[FAIL] %-14s  %s\n" "INVARIANT-CHECK" \
        "marker count or threshold mismatch in _battery_core.py — see constants above"
    FAIL=$((FAIL + 1))
fi

# ---------------------------------------------------------------------------
# Conformance-drift check (CONF-DRIFT, Phase 90, backlog 999.38).
#
# Runs `report-conformance.py --check` ONLY. The generator's --self-test is NOT
# added here: it stays in both pre-commit hooks as their gate 2. --check fails
# when docs/conformance-baseline.md or docs/data/conformance.json no longer
# reproduce a fresh run byte-for-byte, AND, regardless of regeneration, on
# TARGET CAUGHT-SET DRIFT against _CORPUS_TARGET_CAUGHT_LOCK and on the corpus
# and live-conformance floors. Inline (a bare TOTAL increment), never a `gate`
# call, so REG-GUARD's _BATTERY_GATE_RE does not parse it.
# ---------------------------------------------------------------------------
_confdrift_err=$(python3 scripts/report-conformance.py --check 2>&1 >/dev/null)
_confdrift_exit=$?
_confdrift_first=$(printf '%s\n' "$_confdrift_err" | head -n 1)

TOTAL=$((TOTAL + 1))
if [ "$_confdrift_exit" -eq 0 ]; then
    printf "[PASS] %-14s  %s\n" "CONF-DRIFT" \
        "report-conformance.py --check: baseline reproduces; caught-set lock and corpus/live floors hold"
    PASS=$((PASS + 1))
else
    printf "[FAIL] %-14s  %s\n" "CONF-DRIFT" \
        "report-conformance.py --check exited $_confdrift_exit: $_confdrift_first"
    FAIL=$((FAIL + 1))
fi

# ---------------------------------------------------------------------------
# Frozen-evidence re-confirm (D-04) — prior baselines byte-for-byte untouched.
#
# git diff --quiet over all frozen baseline + capture paths must produce zero
# diff.  Any non-zero result means a frozen file has uncommitted modifications,
# which is a D-04 violation.
#
# Coverage change (HARNESS-01, Phase 164): four paths added to this existing
# check, not a second frozen-evidence gate registration. The first three are
# the phase's own new frozen evidence (prompt catalog, probe evidence,
# regenerated baseline). The fourth, tests/quality-baseline-v8.7, goes one
# path beyond those three because D-11 requires that older corpus stay
# byte-frozen and nothing else in this battery enforces it.
#
# Coverage change (MEASURE-01, Phase 166 Plan 02): a fifth path,
# tests/quality-baseline-v8.7-postfix, added to this same existing check —
# this phase's own new frozen post-fix evidence (D-05's 18-invocation live
# run against the post-165 agent body). Same reasoning as the fourth path
# above: nothing else in this battery enforces its byte-freeze.
#
# Coverage change (quick task 260728-pa2, technical-debt audit): four paths
# added to close a coverage asymmetry the audit surfaced — frozen evidence of
# exactly the same kind as the paths already listed, which had simply never
# been added to this list:
#   tests/routing-baseline-v7.13.md     (sibling of routing-baseline-v7.11.md)
#   tests/routing-battery-baseline-v8.5.md (sibling of ...-v4.3/v7.11.md)
#   tests/quality-baseline-v8.10-oos    (v8.10 CORRECTGATE-01 out-of-sample corpus)
#   tests/defrobust-v8.11               (v8.11 DEFROBUST-01 mutually-blind captures)
# The first two were RECOMMEND-REMOVE candidates in that audit purely because
# they lacked this protection while their siblings had it; protecting them
# resolves the asymmetry in the keep direction. See
# docs/technical-debt-audit-2026-07-28.md — pruned from the tree 2026-08-16,
# read it with `git show 09326e7~1:docs/technical-debt-audit-2026-07-28.md`.
#
# Coverage change (v8.24.0 Phase 4, CAP-02): one path added,
# tests/quality-provenance-v8.24 — the irreplaceable PR-P1 capture carrying
# real subagent WebFetch/Read tool calls, recovered from a reaping-vulnerable
# scratchpad and not reproducible without a paid live run. Nothing else in
# this battery enforces its byte-freeze.
#
# Coverage change (Phase 14 Plan 06, D-04): one path added,
# tests/quality-ledger-v8.26 — the 2026-09-02 PR-P1 analysis (v8.25.0)
# control (j) in check-quality-harness.py reads as its closure-ledger
# claim-inventory live leg (7 claims / 0 ledger fragments / 1 untraced).
# Irreplaceable for the same reason as quality-provenance-v8.24: the run is
# not reproducible by any command, and `.planning/` is gitignored, so this
# tracked copy is the only reachable one. The disclosed gap above (a
# committed `git rm` deletion is invisible to either leg) applies here too —
# restated, not newly introduced, by this addition.
#
# Strengthened (v8.24.0 Phase 4 Plan 04-04, WR-01): this was one leg —
# `git diff --quiet -- <paths>` with no commit argument, which compares
# worktree to INDEX, not to HEAD. Measured in an isolated repo before this
# change:
#   unstaged edit    exit 1 (RED, as documented)
#   staged edit      exit 0 (GREEN -- the documented guarantee did not hold;
#                            staged is exactly the state a file is in
#                            immediately before `git commit`)
#   untracked add    exit 0 (invisible either way; git diff never sees an
#                            untracked file regardless of the HEAD argument)
# Two legs now share one pathspec array (_FROZEN_PATHS) so they cannot drift
# apart: leg 1 adds the HEAD argument, catching staged and unstaged edits
# alike; leg 2 sweeps `git status --porcelain --untracked-files=all` over the
# same paths, catching a new file injected into a frozen directory. This is
# one inline check gaining a second leg, not a new gate -- TOTAL still
# increments once for FROZEN-EVIDENCE. The one gap that remains unchanged by
# either leg: a committed `git rm` of a frozen file is in HEAD, so no
# worktree comparison can see it (the fixture README already documents this
# residual gap).
# Amendment procedure for tests/live-conformance-catalog.md (WR-07, Phase 20
# 20-REVIEW). That path is the one entry in this array whose contents the design
# EXPECTS to be revised. It is not only prompt evidence: it is the disposition
# record `_live_disposition_problems` reads, and its own Provenance section says
# plan 20-03 "replaces each `MISSING` placeholder with the row's actual
# disposition ... once that run's reading is known". Three rows currently carry a
# `fix:` disposition naming a backlog item to be executed in a later phase; when
# one lands, the honest move is to update that row's disposition cell -- and
# doing so turns FROZEN-EVIDENCE RED, blocking every commit in the repo until the
# edit is reverted or this array is edited.
#
# The freeze is kept anyway, deliberately: the prompts and their per-row origin
# sentences are irreplaceable evidence for the eight paid live runs in
# tests/live-conformance-v9.0, and splitting the disposition column into an
# unfrozen sidecar would put the annotation and the thing it annotates in two
# files that can drift. What was missing was not the freeze but the written
# procedure, which is this:
#
#   To amend a disposition cell:
#     1. Edit the `disposition: ` substring in that row's Notes cell. Only the
#        disposition may change -- the ID, Prompt and origin sentence are the
#        frozen evidence and must stay byte-identical.
#     2. Regenerate: python3 scripts/report-conformance.py
#     3. Commit the catalog and both regenerated baseline artifacts TOGETHER.
#   FROZEN-EVIDENCE is expected RED between steps 1 and 3 and must be GREEN again
#   after. A RED that survives the commit means something other than a
#   disposition cell moved. Do not reach for --no-verify to get past step 1.
#
# ---------------------------------------------------------------------------
_FROZEN_PATHS=(
    'tests/step0-baseline-v*.md'
    'tests/step0-captures-v*'
    'tests/routing-baseline-v3.*.md'
    'tests/routing-battery-baseline-v4.3.md'
    'tests/routing-baseline-v7.11.md'
    'tests/routing-battery-baseline-v7.11.md'
    'tests/routing-baseline-v7.13.md'
    'tests/routing-battery-baseline-v8.5.md'
    'tests/focused-output-baseline-v*.md'
    'tests/sub-skill-routing-baseline-v*.md'
    'tests/quality-catalog-v8.7.md'
    'tests/quality-probe-v8.7'
    'tests/quality-baseline-v8.7-regenerated'
    'tests/quality-baseline-v8.7'
    'tests/quality-baseline-v8.7-postfix'
    'tests/quality-baseline-v8.10-oos'
    'tests/defrobust-v8.11'
    'tests/quality-provenance-v8.24'
    'tests/quality-ledger-v8.26'
    'tests/adversarial-corpus-v9.0'
    'tests/live-conformance-v9.0'
    'tests/live-conformance-catalog.md'
    'tests/recurrence-reading-v9.1'
    'tests/reference-reads-v9.2.1'
    'tests/reference-reads-v9.2.2'
    'tests/confidence-transitivity-v9.4'
    'tests/exemplar-rederivation-v9.4'
    'tests/pin-classification-v9.4'
    'tests/pin-conversion-v9.4'
    'tests/precheck-rollup-v9.6'
    'tests/hop-validity-v9.6'
    'tests/baseline-reading-v9.6'
    'tests/rebaseline-reading-v9.6'
    # Track B comparative run (2026-09-25) -- the project's first measurement
    # against NOT using the agent, and the baseline the evidence-grounding
    # Phase 1 work must move. Frozen because it is a before-reading: a later
    # phase that edited these captures could manufacture an improvement.
    'tests/trackb-run-v9.13'
    'tests/trackb-catalog-v9.13.md'
    # emission-phase1 Stage A (2026-09-26) -- the first captures of the AGENT'S OWN
    # document rather than the main session's summary of it. Frozen because the
    # erratum these transcripts establish (docs/trackb-transport-erratum.md) is
    # falsifiable only against them, and because raw/ is what makes a corrected
    # extraction rule re-derivable instead of re-spent. raw-attempt1/ holds TB-05's
    # voided first attempt -- the routing miss is evidence, not a mistake to tidy.
    'tests/emission-stage-a-v9.14'
    # w4-paired (2026-09-27) -- the same five prompts on the v9.0.0 and v9.12.0
    # bodies, the only paired body comparison of live output in this tree. Frozen
    # because its reading (docs/w4-paired-reading.md) closes a question two
    # published readings left open; raw/ keeps every voided and superseded attempt,
    # and the runner beside them is the protocol that re-derives the cells.
    'tests/w4-paired'
    # abandonment (2026-09-27) -- the Phase 0 reading over every frozen corpus with
    # subagent events, and the Phase 1 A/B of F2 against control. Frozen because the
    # published readings (docs/abandonment-phase0-reading.md, -phase1-reading.md) decided
    # not to ship a body edit on this evidence; raw/ keeps every miss, truncated
    # hand-back and interrupted run, which are most of what the run found.
    'tests/abandonment'
    # delivery (2026-09-28) -- the first captures here that keep the AGENT'S OWN
    # transcript (raw/<run>.agent/), so what the agent wrote can be compared with what
    # the caller received. Frozen because docs/delivery-reading.md's 5/20 is falsifiable
    # only against them.
    'tests/delivery'
    # delivery-fix, -2, -3 (2026-09-28) -- the three pre-registered attempts to keep the
    # agent's analysis whole: two instruction-only re-sends (both lost fidelity -- a re-sent
    # document is regenerated, not copied) and the file handoff (no cut-offs; not operational
    # as registered). Frozen because each verdict is falsifiable only against these runs.
    'tests/delivery-fix'
    'tests/delivery-fix-2'
    'tests/delivery-fix-3'
    # delivery-fix-4 (2026-09-28) -- the compliance re-run that confirmed file delivery:
    # 12 of 12 runs used the file; delivery-fix-4b (prospective) 9 of 9 delivered.
    'tests/delivery-fix-4'
    # example-rerun (2026-09-28/29) -- every worked example re-run on v9.13.0 and compared
    # with the shipped one (docs/example-rerun-reading.md), including the supplementary
    # full-context re-run. Frozen because the reading's findings -- among them a defect in
    # the shipped estimate-fermi example -- are checkable only against these runs.
    'tests/example-rerun'
    # regression-rerun, -2 (2026-09-29) -- two runs of each example whose re-run regressed,
    # on the fixed body (docs/regression-rerun-reading.md). Frozen because each "resolved"
    # verdict is checkable only against these runs.
    'tests/regression-rerun'
    'tests/regression-rerun-2'
    # trackb-run-v9.15 (2026-09-30) -- the superseding agent-vs-unaided run under
    # docs/trackb-2-preregistration.md: the first capture of the agent's OWN
    # delivered document (not an orchestrator summary) scored against an unaided
    # control, with dispatch recorded per cell. Frozen because docs/trackb-2-reading.md's
    # computed status is falsifiable only against these captures; raw/ keeps every
    # attempt including both usage-limit-pause specimens and the mid-run
    # is_limit_stub() false positive this run's own manifest/cells.json record.
    'tests/trackb-run-v9.15'
    # structured-summary-live (2026-10-01) -- the live confirmation of the
    # structured summary block on all 14 worked examples via agent-router's
    # run_examples.py runner (LIVE-01/LIVE-02/LIVE-03). Frozen because
    # docs/structured-summary-live-reading.md's verdict (9/14 checker PASS,
    # 13/14 gate cleared, median cost $2.8731) is falsifiable only against
    # these captures; raw/ keeps every voided zero-file attempt alongside the
    # collected report, and manifest.json records both invocations and the
    # automatic relaunch of the 3 examples that produced no analysis file on
    # the first pass.
    'tests/structured-summary-live'
    # summary-block-v9.16 (2026-09-30) -- the four real analysis-report
    # fixtures the structured-summary-block checker's P1-P4/X1/X2 controls
    # are anchored to (SUMM-BLOCK). Frozen because every must-fail control
    # mutates a copy of a fixture's parsed block, never the file on disk, and
    # the independent inventory falsifier (75-falsifiers.sh f5) is checkable
    # only against these exact prose/block pairs.
    'tests/summary-block-v9.16'
    # persona-live-v9.18 (2026-10-02) -- the PEX-02 live reading
    # (docs/v9.18-persona-live-reading.md) and the four 86-02 persona-example runs'
    # provenance. Frozen because the Results table's 12/12-pass verdict and the
    # examples' checks.tsv are falsifiable only against these sources, manifests and
    # out/ artifacts; raw.jsonl streams were kept in scratch by design, never
    # committed.
    'tests/persona-live-v9.18'
    # persona-live-v9.18b (2026-10-02) -- the post-87 live reading
    # (docs/v9.18b-persona-live-reading.md) and the four 87-05 example re-derivation runs'
    # provenance. Frozen because the Results table's 11/12-pass verdict (one PV-DIRECTIVE
    # FAIL, recorded as observed per the pre-registration's own §7 rule) and the examples'
    # checks.tsv are falsifiable only against these sources, manifests and out/ artifacts;
    # raw.jsonl streams were kept in scratch by design, never committed.
    'tests/persona-live-v9.18b'
    # persona-live-v9.18c (2026-10-02) -- the memo-format live reading
    # (docs/v9.18c-persona-live-reading.md) and the four 87-09 example re-derivation runs'
    # provenance. Frozen because the Results table's 11/12-pass verdict (one NO-FILE result,
    # the skill's own self-check rejecting an over-length draft on PV-WORDS and deleting it,
    # recorded as observed per the pre-registration's own §7 rule) and the examples'
    # checks.tsv are falsifiable only against these sources, manifests and out/ artifacts;
    # raw.jsonl streams were kept in scratch by design, never committed.
    'tests/persona-live-v9.18c'
    # persona-live-v9.18d (2026-10-02) -- the four 87-11 example re-derivation runs under the
    # linked Basis header (D-12). Frozen because the shipped examples' sha256 equality with
    # their runs is falsifiable only against this manifest, checks.tsv and out/.
    'tests/persona-live-v9.18d'
)

git diff --quiet HEAD -- "${_FROZEN_PATHS[@]}" 2>/dev/null
_frozen_exit=$?

_frozen_untracked=$(git status --porcelain --untracked-files=all -- "${_FROZEN_PATHS[@]}" 2>/dev/null)

TOTAL=$((TOTAL + 1))
if [ "$_frozen_exit" -eq 0 ] && [ -z "$_frozen_untracked" ]; then
    printf "[PASS] %-14s  %s\n" "FROZEN-EVIDENCE" \
        "diff-vs-HEAD + untracked sweep: frozen baselines/captures unmodified (D-04)"
    PASS=$((PASS + 1))
elif [ "$_frozen_exit" -ne 0 ]; then
    printf "[FAIL] %-14s  %s\n" "FROZEN-EVIDENCE" \
        "frozen baseline/capture files have modifications relative to HEAD (staged or unstaged) — D-04 violation"
    FAIL=$((FAIL + 1))
else
    printf "[FAIL] %-14s  %s\n" "FROZEN-EVIDENCE" \
        "untracked files have appeared inside a frozen path — D-04 violation: $_frozen_untracked"
    FAIL=$((FAIL + 1))
fi

# ---------------------------------------------------------------------------
# Final verdict
#
# GREEN requires FAIL == 0 AND PREREQ == 0 — an unmet prerequisite is NOT a
# pass. Three outcomes, in priority order: a genuine failure always yields
# RED regardless of PREREQ (a real defect outranks an unmet prerequisite);
# only when nothing failed does an unmet prerequisite yield BLOCKED instead
# of GREEN.
# ---------------------------------------------------------------------------
echo ""
if [ "$FAIL" -eq 0 ] && [ "$PREREQ" -eq 0 ]; then
    echo "FIREWALL: GREEN ($PASS/$TOTAL)"
    exit 0
elif [ "$FAIL" -gt 0 ]; then
    if [ "$PREREQ" -gt 0 ]; then
        echo "FIREWALL: RED ($FAIL gate(s) failed, $PREREQ prerequisite(s) unmet; $PASS/$TOTAL passed)"
    else
        echo "FIREWALL: RED ($FAIL gate(s) failed; $PASS/$TOTAL passed)"
    fi
    exit 1
else
    echo "FIREWALL: BLOCKED ($PREREQ prerequisite(s) unmet; $PASS/$TOTAL passed)"
    exit 2
fi
