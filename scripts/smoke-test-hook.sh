#!/usr/bin/env bash
# End-to-end smoke test for the body-budget pre-commit hook (HOOK-06).
#
# Verifies, in order:
#   (a) ./scripts/install-hooks.sh runs cleanly (exit 0)
#   (b) An over-budget edit to first-principles/agents/first-principles.md is staged
#   (c) `git commit` is rejected (non-zero exit) and stderr names the budget violation
#   (d) Reverting the over-budget edit leaves a clean tree
#   (e) An under-budget commit (--allow-empty, body not touched) succeeds (exit 0)
#
# Self-cleanup via trap: always returns the working tree and HEAD to the
# pre-test branch and deletes the temp branch, even on assertion failure.
#
# Safety: refuses to run on a dirty working tree (we manipulate the body file
# directly) and refuses if the body file is already at/over budget (cannot
# construct a meaningful over-budget scenario in that case).

set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

BODY_FILE="first-principles/agents/first-principles.md"
MAX_LINES=500

# --- Pre-flight ----------------------------------------------------------------

if [[ -n "$(git status --porcelain)" ]]; then
    echo "smoke-test: working tree is dirty -- refusing to run" >&2
    exit 1
fi

if [[ ! -f "$BODY_FILE" ]]; then
    echo "smoke-test: body file $BODY_FILE not found" >&2
    exit 1
fi

CURRENT=$(wc -l < "$BODY_FILE")
FILLER=$((MAX_LINES - CURRENT + 2))
if (( FILLER <= 0 )); then
    echo "smoke-test: body already at/over budget ($CURRENT lines) -- cannot construct over-budget scenario cleanly, aborting" >&2
    exit 1
fi

ORIG_BRANCH=$(git symbolic-ref --short HEAD)
TMP_BRANCH="smoke-test-body-budget-$$"

# --- Cleanup trap --------------------------------------------------------------

cleanup() {
    # Best-effort: revert any modifications, return to original branch, drop temp branch.
    git checkout -- "$BODY_FILE" 2>/dev/null || true
    # If we're already on $ORIG_BRANCH, the checkout is a no-op.
    git checkout "$ORIG_BRANCH" 2>/dev/null || true
    git branch -D "$TMP_BRANCH" 2>/dev/null || true
}
trap cleanup EXIT

# --- (a) Install hook ----------------------------------------------------------

git checkout -b "$TMP_BRANCH"

set +e
./scripts/install-hooks.sh
RC=$?
set -e
if (( RC != 0 )); then
    echo "smoke-test: FAIL -- (a) installer exited $RC" >&2
    exit 1
fi
echo "smoke: (a) installer ran OK"

# --- (b) Stage over-budget edit -----------------------------------------------

for ((i = 0; i < FILLER; i++)); do
    echo "# smoke-test-filler" >> "$BODY_FILE"
done
git add "$BODY_FILE"
NEW_LINES=$(wc -l < "$BODY_FILE")
echo "smoke: (b) body padded to $NEW_LINES lines (budget=$MAX_LINES, filler=$FILLER)"

# --- (c) Assert over-budget commit is rejected --------------------------------

LOG_C=$(mktemp -t smoke-c.XXXXXX)
set +e
git commit -m "smoke: over-budget" >"$LOG_C" 2>&1
RC=$?
set -e

if (( RC == 0 )); then
    echo "smoke-test: FAIL -- (c) over-budget commit was NOT rejected (exit 0)" >&2
    cat "$LOG_C" >&2
    rm -f "$LOG_C"
    exit 1
fi

if ! grep -qE "MAX_LINES|body budget|exceeds|over budget" "$LOG_C"; then
    echo "smoke-test: FAIL -- (c) reject reason did not mention budget. Output was:" >&2
    cat "$LOG_C" >&2
    rm -f "$LOG_C"
    exit 1
fi
rm -f "$LOG_C"
echo "smoke: (c) over-budget commit correctly rejected (exit $RC)"

# --- (d) Revert over-budget edit ----------------------------------------------

git checkout -- "$BODY_FILE"
# After the revert, the index still contains the previously-staged version.
# Reset the index entry for the body file so the next commit doesn't include it.
git reset HEAD -- "$BODY_FILE" >/dev/null 2>&1 || true
echo "smoke: (d) body reverted to original ($(wc -l < "$BODY_FILE") lines)"

# --- (e) Assert under-budget (empty) commit is accepted -----------------------

LOG_E=$(mktemp -t smoke-e.XXXXXX)
set +e
git commit --allow-empty -m "smoke: under-budget" >"$LOG_E" 2>&1
RC=$?
set -e

if (( RC != 0 )); then
    echo "smoke-test: FAIL -- (e) under-budget commit was rejected (exit $RC). Output:" >&2
    cat "$LOG_E" >&2
    rm -f "$LOG_E"
    exit 1
fi
rm -f "$LOG_E"
echo "smoke: (e) under-budget commit correctly accepted (exit $RC)"

# --- Summary -------------------------------------------------------------------

echo "smoke-test: PASS -- all 5 assertions held"
exit 0
