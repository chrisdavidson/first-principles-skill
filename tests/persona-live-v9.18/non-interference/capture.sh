#!/usr/bin/env bash
# Capture recipe for the D-03 non-interference proof. Run from the repo root:
#   bash tests/persona-live-v9.18/non-interference/capture.sh <outdir>
# Writes one file per D-03 gate command into <outdir>, each holding stdout,
# a "--- stderr ---" marker, stderr, then a "--- exit N ---" marker.
set -u
OUTDIR="$1"
mkdir -p "$OUTDIR"

capture() {
  local name="$1"
  shift
  local out_file="$OUTDIR/$name.txt"
  local tmp_out tmp_err
  tmp_out=$(mktemp)
  tmp_err=$(mktemp)
  "$@" >"$tmp_out" 2>"$tmp_err"
  local exit_code=$?
  {
    cat "$tmp_out"
    echo "--- stderr ---"
    cat "$tmp_err"
    echo "--- exit $exit_code ---"
  } > "$out_file"
  rm -f "$tmp_out" "$tmp_err"
}

capture "report-conformance-check" python3 scripts/report-conformance.py --check
capture "check-conf-gate" python3 scripts/check-conf-gate.py
capture "check-summary-block-exemplar" python3 scripts/check-summary-block.py --exemplar shared/examples/*.md first-principles/references/examples/*.md
