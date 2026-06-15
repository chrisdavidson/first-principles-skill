#!/usr/bin/env bash
# Run both live monitoring harnesses — Step-0 (STEP0-06) + routing battery (BATT-06).
# Hybrid cadence; see docs/live-monitoring-runbook.md.

set -euo pipefail

# Move to repo root.
if ! REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"; then
    echo "run-live-monitoring: not inside a git working tree" >&2
    exit 1
fi
cd "$REPO_ROOT"

# Both harnesses exit non-zero on BATTERY:FAIL, which the runbook documents as the
# EXPECTED, non-blocking honest carry-forward state (S-P01/02/05, S-N04 at v5.3). So we
# must NOT let `set -e` abort after the first harness — capture each exit code with
# `|| rc=$?`, run both unconditionally, then report. This wrapper is a convenience runner,
# not a CI gate; interpret the per-harness BATTERY: lines per docs/live-monitoring-runbook.md.
step0_rc=0
battery_rc=0

echo "==> Step 0 live harness (STEP0-06 domain; ~60 claude invocations)"
python3 scripts/check-step0-live.py --catalog tests/step0-fixture-catalog.md --repeat 5 --min-pass 3 || step0_rc=$?

echo "==> Routing battery (BATT-06 domain; live)"
python3 scripts/check-routing-battery.py --catalog tests/routing-battery-catalog.md --repeat 5 --min-pass 3 || battery_rc=$?

echo ""
echo "==> Done. Exit codes (non-zero = BATTERY:FAIL, expected/non-blocking per runbook):"
echo "    check-step0-live.py       exit ${step0_rc}  (STEP0-06)"
echo "    check-routing-battery.py  exit ${battery_rc}  (BATT-06)"
echo ""
echo "==> Record results in:"
echo "    1. A new versioned baseline file: tests/step0-baseline-v<milestone>.md"
echo "    2. The rolling results table in:  docs/live-monitoring-runbook.md"
