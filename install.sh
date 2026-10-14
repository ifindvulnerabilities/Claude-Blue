#!/usr/bin/env bash
# claude-blue installer — copies skills into a Claude skills directory.
set -euo pipefail

TARGET="${HOME}/.claude/skills"
CATEGORY=""
SRC="$(cd "$(dirname "$0")" && pwd)/Skills"

usage() {
  echo "Usage: $0 [--target DIR] [--category soc|detection|ir|intel|hardening|people]"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target)   TARGET="${2:?--target needs a directory}"; shift 2 ;;
    --category) CATEGORY="${2:?--category needs a name}"; shift 2 ;;
    -h|--help)  usage; exit 0 ;;
    *) echo "Unknown option: $1"; usage; exit 1 ;;
  esac
done

available=()
for cat_dir in "$SRC"/*/; do
  available+=("$(basename "$cat_dir")")
done

if [[ -n "$CATEGORY" ]]; then
  if [[ ! -d "$SRC/$CATEGORY" ]]; then
    echo "No such category: $CATEGORY"
    echo "Available: ${available[*]}"
    exit 1
  fi
  categories=("$CATEGORY")
else
  categories=("${available[@]}")
fi

mkdir -p "$TARGET"
count=0
for cat in "${categories[@]}"; do
  for dir in "$SRC/$cat"/*/; do
    [[ -f "$dir/SKILL.md" ]] || continue
    name="$(basename "$dir")"
    if [[ -e "$TARGET/$name" ]]; then
      echo "skip   $name (already exists in $TARGET)"
      continue
    fi
    cp -R "$dir" "$TARGET/$name"
    echo "added  $name"
    count=$((count + 1))
  done
done

echo "Installed $count skill(s) to $TARGET"
echo "Principles: every skill hands the decision back to you. See PRINCIPLES.md."
