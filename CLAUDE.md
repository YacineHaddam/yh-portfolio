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
