#!/usr/bin/env bash
# scripts/check-firewall-battery.sh
#
# One-shot offline battery runner — Phase 128 READY-03 (D-06).
#
# Runs all 17 offline gate commands, captures each exit code, and prints a
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
#   VAL-02    VAL-03        VAL-04    VAL-05    VERSION-01
#   GATE-01   BATT-06       TRACE-03  COLLIDE-01    QUAL-01
#   HARN-01   HARN-02       HARN-03   HC-BOUND     REG-GUARD
#   PROV-GUARD  INVARIANT-CHECK  FROZEN-EVIDENCE
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
# body-budget gate was retired -- scripts/check-body-budget.py is now
# report-only and always exits 0, so tallying it would inflate the count with
# a gate that can never fail. It is still reported below as an un-tallied
# [INFO] line so the body's line count stays visible on every run; the drop
# is named here rather than silently absorbed. Battery composition moved
# 16 -> 15 as a result.
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
# NOTE: set -u is active; set -e is intentionally ABSENT — every gate must run
# and be tallied even if an earlier gate fails (no early abort).

set -u

# Resolve repo root from this script's location so it runs from any cwd.
REPO=$(cd "$(dirname "$0")/.." && pwd)
cd "$REPO"

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

# VAL-04 — 4-gram trigger-phrase collision scan (self-test + live)
gate "VAL-04" \
    "check-trigger-collisions.py --self-test + live" \
    "python3 scripts/check-trigger-collisions.py --self-test" \
    "python3 scripts/check-trigger-collisions.py"

# VAL-05 — skill-listing description budget (≤2000 chars)
gate "VAL-05" \
    "check-description-budget.py" \
    "python3 scripts/check-description-budget.py"

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
#             .github/workflows/validation.yml, QUAL-01 excepted as the one
#             documented battery-only gate (WR-02, v8.24).
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

# COLLIDE-01 — plugin/monolith name-collision scan (self-test + live)
gate "COLLIDE-01" \
    "check-install-collisions.py --self-test + live" \
    "python3 scripts/check-install-collisions.py --self-test" \
    "python3 scripts/check-install-collisions.py"

# QUAL-01 — quality-measurement harness offline self-test: extraction
#           guardrails A/B, scoreline parser, blinding integrity, tabulation
#           arithmetic, baseline-fixture integrity, defect detector, run-layer
#           composition (HARNESS-01, Phase 164)
gate "QUAL-01" \
    "check-quality-harness.py --self-test" \
    "python3 scripts/check-quality-harness.py --self-test"

# PROV-GUARD — capture-based provenance verification: every read-at-source
#              ground truth in an analysis's section 3 joins to a real
#              WebFetch/Read of that source in the run's stored capture, and
#              every literal it states appears verbatim in the retrieved
#              text. Runs the live scan as well as the self-test, for the
#              same reason VERSION-01 and REG-GUARD above do: the self-test's
#              fixtures are tempdir/in-memory, so the self-test alone
#              asserts nothing about the committed capture at
#              tests/quality-provenance-v8.24/ — the live leg reads
#              7/7 sources matched, 35/35 literals located.
#              Bare `python3`, not `uv run` — see the "Rejected: `uv run
#              --with pytest`" note in this file's header: `uv run` may resolve
#              and fetch from a remote index, and this script is by construction
#              an OFFLINE firewall.
gate "PROV-GUARD" \
    "check-provenance.py --self-test + live" \
    "python3 scripts/check-provenance.py --self-test" \
    "python3 scripts/check-provenance.py"

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

# HC-BOUND — HIGH-confidence bound: Phase 5 tightening of Criterion 3 (Evidence)
#            and Criterion 5 (Conclusion) is present and well-formed in the
#            Self-Audit rubric, and all three documented EXCEPT exceptions are
#            present on both rubric surfaces
gate "HC-BOUND" \
    "check-high-confidence-bound.py --self-test" \
    "python3 scripts/check-high-confidence-bound.py --self-test"

# body-size — un-tallied [INFO] line (TEARDOWN-01: gate retired, docs/v8.7-constraint-teardown.md).
# Does NOT go through `gate()` -- `gate()` unconditionally increments TOTAL, and this line
# reports rather than passes/fails. Its exit status does not influence PASS/FAIL/TOTAL.
_body_size_report=$(python3 scripts/check-body-budget.py 2>&1)
printf "[INFO] %-14s  %s\n" "body-size" "$_body_size_report"

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
