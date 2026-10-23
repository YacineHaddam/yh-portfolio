# yh-portfolio

## Agent skills

### Issue tracker

Issues live as local markdown files under `.scratch/<feature>/`. See `docs/agents/issue-tracker.md`.

### Triage labels

Default five-role vocabulary (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `GLOSSARY.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.

## Working on tickets

- Every commit message names the spec (the `.scratch/<feature>` folder name) and the ticket number, as `Spec: <feature>` and `Ticket: <NN>` lines before the Co-Authored-By line. This applies to follow-up and fix commits too.
- When a ticket is finished, set its `status: done`, tick its acceptance criteria and add a dated entry under `## Comments` saying what was and wasn't verified.
- Tick only the criteria you verified. If one can't be verified yet (for example CI before a workflow exists), leave it unticked and say why in the comment.

## Testing

- Work test-first in vertical slices: one failing test, then the minimum code to pass it. Confirm the test fails for the right reason before writing the code.
- Tests assert on observable behaviour: the violations the source check reports, or what is present in the built site. Never on internals, config structure or real content (fixtures only).
- While iterating, run single test files (`uv run pytest tests/test_x.py`). Before every commit run `make check` (source check, strict build, pytest) and report its real output.
- Run commands the standard way: `uv run ...` and `make ...`. Do not call `.venv/bin/...` directly or set up workarounds. If a standard command fails, report the exact error and ask the user to run it with `! <command>`.

## Dependencies

- Add and change dependencies with `uv add`, `uv remove` and `uv lock`. Never hand-edit `uv.lock`.
- Anything a module imports directly must be a declared dependency, not a transitive one.
- Zensical is pinned to an exact version. Upgrade it only as described in `README.md`, and merge only if `make check` passes.

## Committing

- Commit when asked, or when the workflow in use says to (for example `/implement`). Commit to the current branch.
- Stage explicit paths, not `git add -A` or `git add .`, and look at `git status` before and after so nothing stray goes in or is left behind.
- Message: a short imperative subject, a line or two on what and why, then the `Spec:` and `Ticket:` lines, then the Co-Authored-By line.
- Fixes found in review go in a separate follow-up commit with the same `Spec:` and `Ticket:` lines.

## Zensical reference

Zensical is alpha and changes every few days, so do not answer from memory.

- The docs are in `references/zensical-docs/docs/`, a gitignored copy of `github.com/zensical/docs` (MIT). Read them there before changing `zensical.toml`, adding a plugin or setting, or answering a Zensical question.
- Run `make refresh-docs` first if `references/zensical-docs/.refreshed` is missing or older than 7 days, and after every Zensical upgrade. The file holds the upstream commit and the date, so cite them when relying on the docs.
- If the docs and the installed version disagree, trust the built-site check: unsupported settings are silently ignored.
