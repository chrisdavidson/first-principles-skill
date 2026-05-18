#!/usr/bin/env bash
# Host-side link-resolution check for first-principles-thinking skill.
# Run from repo root. NOT part of the skill — pure dev tooling.
SKILL_DIR="./first-principles-thinking"
cd "$SKILL_DIR" || exit 1
BROKEN=0
while IFS=: read -r source_file link_target; do
  src_dir=$(dirname "$source_file")
  resolved="$src_dir/$link_target"
  if [ ! -f "$resolved" ]; then
    echo "BROKEN: $source_file -> $link_target"
    BROKEN=$((BROKEN+1))
  fi
done < <(grep -oP '\[.*?\]\(\K[^)#]+' SKILL.md references/*.md examples/*.md | grep -v '^http')
[ "$BROKEN" -eq 0 ] && echo "All links resolve OK" || echo "$BROKEN broken link(s)"
