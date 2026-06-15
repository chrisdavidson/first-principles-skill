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

echo "==> Step 0 live harness (STEP0-06 domain; ~60 claude invocations)"
python3 scripts/check-step0-live.py --catalog tests/step0-fixture-catalog.md --repeat 5 --min-pass 3

echo "==> Routing battery (BATT-06 domain; live)"
python3 scripts/check-routing-battery.py --catalog tests/routing-battery-catalog.md --repeat 5 --min-pass 3

echo ""
echo "==> Done. Record results in:"
echo "    1. A new versioned baseline file: tests/step0-baseline-v<milestone>.md"
echo "    2. The rolling results table in:  docs/live-monitoring-runbook.md"
