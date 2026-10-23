#!/usr/bin/env bash
# Keep local, gitignored copies of the reference docs under references/.
# Each entry is "<dest name> <repo url> <sparse paths...>"; only those paths are fetched.
set -euo pipefail

SOURCES=(
    "zensical-docs https://github.com/zensical/docs.git docs"
    "mkdocs-material https://github.com/squidfunk/mkdocs-material.git docs/reference docs/setup"
)

for source in "${SOURCES[@]}"; do
    read -r name repo paths <<< "$source"
    dest="references/$name"

    if [ -d "$dest/.git" ]; then
        git -C "$dest" pull --ff-only --quiet
    else
        mkdir -p references
        git clone --depth 1 --filter=blob:none --sparse --quiet "$repo" "$dest"
        # shellcheck disable=SC2086 # $paths is a deliberate word list
        git -C "$dest" sparse-checkout set $paths
    fi

    echo "$(git -C "$dest" rev-parse HEAD) $(date +%F)" > "$dest/.refreshed"
    echo "$name at $(cut -c1-7 "$dest/.refreshed"): $(find "$dest" -name '*.md' -not -path '*/.git/*' | wc -l | tr -d ' ') Markdown files"
done
