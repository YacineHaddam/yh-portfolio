#!/usr/bin/env bash
# One-off walkthrough for the steps only the author can do: create the public
# GitHub repo, add the remote, push, and switch Pages to "GitHub Actions".
# Run from the repo root: bash scripts/publish-wizard.sh
set -euo pipefail

TOTAL=5
N=0
REPO="yh-portfolio"

stage() {
  N=$((N + 1))
  printf '\n=== Stage %d of %d: %s ===\n\n' "$N" "$TOTAL" "$1"
}

pause() {
  read -r -p "Press Enter when done (Ctrl-C to stop)... " _
}

confirm() {
  local answer
  read -r -p "$1 [y/N] " answer
  [[ "$answer" == "y" || "$answer" == "Y" ]]
}

stage "Your GitHub username"
read -r -p "GitHub username: " GH_USER
[[ -n "$GH_USER" ]] || { echo "A username is required."; exit 1; }
SITE_URL="https://${GH_USER}.github.io/${REPO}/"
echo "The site will be served at ${SITE_URL}"

stage "Set site_url in zensical.toml"
if grep -q '^site_url = ' zensical.toml; then
  # Rewrite the single site_url line; the TODO comment above it is left for you to delete.
  sed -i.bak "s|^site_url = .*|site_url = \"${SITE_URL}\"|" zensical.toml
  rm -f zensical.toml.bak
  echo "Updated site_url. Also replace the placeholder handles under [[project.extra.social]],"
  echo "and delete the TODO comment above site_url."
else
  echo "No site_url line found in zensical.toml; add it by hand and re-run." && exit 1
fi
pause

stage "Create the public repo"
echo "Open https://github.com/new and create a PUBLIC repo named '${REPO}'."
echo "Leave it empty: no README, .gitignore or licence."
pause

stage "Add the remote and push"
echo "Commit the site_url change first (git add zensical.toml && git commit), then:"
echo
echo "  git remote add origin git@github.com:${GH_USER}/${REPO}.git"
echo "  git push -u origin main"
echo
if git remote get-url origin >/dev/null 2>&1; then
  echo "A remote named 'origin' already exists: $(git remote get-url origin)"
fi
confirm "Pushed to main?" || { echo "Push, then re-run from the top."; exit 1; }

stage "Set the Pages source to GitHub Actions"
echo "Open https://github.com/${GH_USER}/${REPO}/settings/pages"
echo "Under 'Build and deployment', set Source to 'GitHub Actions'."
echo "Then re-run the failed deploy job under the Actions tab if the first push ran before this."
pause

echo
echo "Done. Check ${SITE_URL} once the 'Documentation' workflow finishes,"
echo "and confirm the nav links resolve under /${REPO}/."
