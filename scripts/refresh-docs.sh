#!/usr/bin/env bash
# Keep a local, gitignored copy of the Zensical docs in references/zensical-docs/.
# Source: https://github.com/zensical/docs (MIT), Markdown under docs/.
set -euo pipefail

REPO="https://github.com/zensical/docs.git"
DEST="references/zensical-docs"

if [ -d "$DEST/.git" ]; then
    git -C "$DEST" pull --ff-only --quiet
else
    mkdir -p "$(dirname "$DEST")"
    git clone --depth 1 --filter=blob:none --sparse --quiet "$REPO" "$DEST"
    git -C "$DEST" sparse-checkout set docs
fi

echo "$(git -C "$DEST" rev-parse HEAD) $(date +%F)" > "$DEST/.refreshed"
echo "Zensical docs at $(cut -c1-7 "$DEST/.refreshed") in $DEST ($(find "$DEST/docs" -name '*.md' | wc -l | tr -d ' ') Markdown files)"
