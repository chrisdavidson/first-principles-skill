#!/usr/bin/env bash
# Append one row of GitHub adoption telemetry to docs/adoption-telemetry.csv.
#
# WHY THIS EXISTS: GitHub's traffic API serves a 14-day ROLLING window and is not
# retroactive — data older than 14 days is permanently unrecoverable. Without a
# periodic snapshot there is no adoption trend, only a single reading. Installed
# 2026-07-22 per the ALTITUDE.md addendum of the same date.
#
# READING THE DATA: `views_*` is the human signal. `clones_*` is dominated by this
# repo's own GitHub Actions checkouts (validation.yml runs on every push), so clone
# spikes track our commit activity, not visitors. Never cite clones as adoption.
#
# Idempotent per day: re-running on the same date replaces that date's row rather
# than appending a duplicate, so cron retries and manual runs cannot double-count.

set -euo pipefail

REPO="chrisdavidson/first-principles-skill"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CSV="$ROOT/docs/adoption-telemetry.csv"
HEADER="date,stars,forks,watchers,open_issues,views_14d,views_uniq_14d,clones_14d,clones_uniq_14d,top_referrer"

today="$(date -u +%Y-%m-%d)"

repo_json="$(gh repo view "$REPO" --json stargazerCount,forkCount,watchers,issues)"
views_json="$(gh api "repos/$REPO/traffic/views")"
clones_json="$(gh api "repos/$REPO/traffic/clones")"
refs_json="$(gh api "repos/$REPO/traffic/popular/referrers")"

stars=$(printf '%s' "$repo_json"   | jq -r '.stargazerCount')
forks=$(printf '%s' "$repo_json"   | jq -r '.forkCount')
watchers=$(printf '%s' "$repo_json" | jq -r '.watchers.totalCount')
issues=$(printf '%s' "$repo_json"  | jq -r '.issues.totalCount')

views=$(printf '%s' "$views_json"       | jq -r '.count')
views_uniq=$(printf '%s' "$views_json"  | jq -r '.uniques')
clones=$(printf '%s' "$clones_json"     | jq -r '.count')
clones_uniq=$(printf '%s' "$clones_json" | jq -r '.uniques')

# Empty referrer list is normal at this traffic level; record "-" rather than failing.
top_ref=$(printf '%s' "$refs_json" | jq -r 'if length > 0 then .[0].referrer else "-" end')

row="$today,$stars,$forks,$watchers,$issues,$views,$views_uniq,$clones,$clones_uniq,$top_ref"

if [ ! -f "$CSV" ]; then
    printf '%s\n' "$HEADER" > "$CSV"
fi

# Drop any pre-existing row for today, then append this one.
tmp="$(mktemp)"
grep -v "^$today," "$CSV" > "$tmp" || true
printf '%s\n' "$row" >> "$tmp"
mv "$tmp" "$CSV"

printf 'snapshot %s -> %s\n' "$today" "$CSV"
printf '  human signal : %s views / %s unique\n' "$views" "$views_uniq"
printf '  self-noise   : %s clones / %s unique (CI-dominated)\n' "$clones" "$clones_uniq"
printf '  stars %s | forks %s | watchers %s | issues %s | top referrer %s\n' \
    "$stars" "$forks" "$watchers" "$issues" "$top_ref"
