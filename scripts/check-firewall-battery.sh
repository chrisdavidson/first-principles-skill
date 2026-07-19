#!/usr/bin/env bash
# scripts/check-firewall-battery.sh
#
# One-shot offline battery runner — Phase 128 READY-03 (D-06).
#
# Runs all 13 offline gate commands, captures each exit code, and prints a
# FIREWALL: GREEN / RED verdict. A GREEN result is the hard authorization gate
# for the Phase-129/130 live runs (D-01). VAL-01 (claude plugin validate) is a
# CLI schema check that spends ZERO model tokens and is explicitly permitted
# inside this offline firewall.
#
# Usage:  bash scripts/check-firewall-battery.sh
# Exits:  0 = FIREWALL GREEN (all gates pass)
#         1 = FIREWALL RED   (one or more gates failed)
#
# Gates (13):
#   DUAL-04   STEP0-06  STEP0-08  VAL-01    VAL-02
#   VAL-03    VAL-04    VAL-05    GATE-01   BATT-06
#   TRACE-03  COLLIDE-01  body-budget
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

echo "=== Phase 128 Offline Firewall Battery (READY-03 / D-06) ==="
echo ""

# DUAL-04 — shared/ and generated first-principles/ tree are in sync
gate "DUAL-04" \
    "sync-content.py --check" \
    "python3 scripts/sync-content.py --check"

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
#           validity + anchor tests
gate "VAL-03" \
    "check-links.py --self-test + live + pytest check-links_anchors_test.py" \
    "python3 scripts/check-links.py --self-test" \
    "python3 scripts/check-links.py" \
    "python3 -m pytest scripts/check-links_anchors_test.py -q"

# VAL-04 — 4-gram trigger-phrase collision scan (self-test + live)
gate "VAL-04" \
    "check-trigger-collisions.py --self-test + live" \
    "python3 scripts/check-trigger-collisions.py --self-test" \
    "python3 scripts/check-trigger-collisions.py"

# VAL-05 — skill-listing description budget (≤2000 chars)
gate "VAL-05" \
    "check-description-budget.py" \
    "python3 scripts/check-description-budget.py"

# GATE-01 — agent structural checks (self-test + live agent file)
gate "GATE-01" \
    "check-agent.py --self-test + --file first-principles/agents/first-principles.md" \
    "python3 scripts/check-agent.py --self-test" \
    "python3 scripts/check-agent.py --file first-principles/agents/first-principles.md"

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

# body-budget — agent body line count ≤644
gate "body-budget" \
    "check-body-budget.py" \
    "python3 scripts/check-body-budget.py"

# ---------------------------------------------------------------------------
# Invariant re-confirm (D-07) — byte-frozen constants in _battery_core.py.
#
# BATT-06 and STEP0-08 self-tests already internally assert these six constants;
# this block provides explicit value-greps as a direct double-check:
#   pre-mortem=9  fishbone=7  inversion=13  trade-off=10
#   MIN_HEADER_HITS=2  _COMPOSER_FOCUS_CEILING=4
# No constant is changed here (re-confirm only, D-07).
# ---------------------------------------------------------------------------
python3 - <<'PYEOF' >/dev/null 2>&1
import sys
sys.path.insert(0, 'scripts')
from _battery_core import _TECHNIQUE_CATEGORIES as T, MIN_HEADER_HITS as MH, _COMPOSER_FOCUS_CEILING as CC
assert len(T['pre-mortem'])==9,  f"pre-mortem expected 9, got {len(T['pre-mortem'])}"
assert len(T['fishbone'])==7,    f"fishbone expected 7, got {len(T['fishbone'])}"
assert len(T['inversion'])==13,  f"inversion expected 13, got {len(T['inversion'])}"
assert len(T['trade-off'])==10,  f"trade-off expected 10, got {len(T['trade-off'])}"
assert MH==2,  f"MIN_HEADER_HITS expected 2, got {MH}"
assert CC==4,  f"_COMPOSER_FOCUS_CEILING expected 4, got {CC}"
PYEOF
_inv_exit=$?

TOTAL=$((TOTAL + 1))
if [ "$_inv_exit" -eq 0 ]; then
    printf "[PASS] %-14s  %s\n" "INVARIANT-CHECK" \
        "pre-mortem=9 fishbone=7 inversion=13 trade-off=10 MIN_HEADER_HITS=2 _COMPOSER_FOCUS_CEILING=4"
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
# ---------------------------------------------------------------------------
git diff --quiet -- \
    'tests/step0-baseline-v*.md' \
    'tests/step0-captures-v*' \
    'tests/routing-baseline-v3.*.md' \
    'tests/routing-battery-baseline-v4.3.md' \
    'tests/routing-baseline-v7.11.md' \
    'tests/routing-battery-baseline-v7.11.md' \
    'tests/focused-output-baseline-v*.md' \
    'tests/sub-skill-routing-baseline-v*.md' \
    2>/dev/null
_frozen_exit=$?

TOTAL=$((TOTAL + 1))
if [ "$_frozen_exit" -eq 0 ]; then
    printf "[PASS] %-14s  %s\n" "FROZEN-EVIDENCE" \
        "git diff --quiet: frozen baselines/captures unmodified (D-04)"
    PASS=$((PASS + 1))
else
    printf "[FAIL] %-14s  %s\n" "FROZEN-EVIDENCE" \
        "frozen baseline/capture files have uncommitted modifications (D-04 violation)"
    FAIL=$((FAIL + 1))
fi

# ---------------------------------------------------------------------------
# Final verdict
# ---------------------------------------------------------------------------
echo ""
if [ "$FAIL" -eq 0 ]; then
    echo "FIREWALL: GREEN ($PASS/$TOTAL)"
    exit 0
else
    echo "FIREWALL: RED ($FAIL gate(s) failed; $PASS/$TOTAL passed)"
    exit 1
fi
