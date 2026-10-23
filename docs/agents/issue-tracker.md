# Issue tracker: local markdown

Issues for this repo live as markdown files in `.scratch/`, not on a remote tracker.

## Layout

```
.scratch/
  <feature>/
    spec.md            # output of /to-spec (optional)
    issues/
      001-<slug>.md    # one file per ticket
      002-<slug>.md
```

- `<feature>` is a short kebab-case name for the body of work.
- Ticket files are numbered in creation order; the number is the ticket's ID.

## Ticket file format

```markdown
---
title: <short title>
status: needs-triage | needs-info | ready-for-agent | ready-for-human | wontfix | in-progress | done
blocked-by: [001, 003]   # IDs of tickets that must be done first; [] if none
---

<description, acceptance criteria, notes>
```

## Operations

- **Create**: write a new numbered file under `.scratch/<feature>/issues/`.
- **Read / list**: read the files; filter on the `status` frontmatter.
- **Update status / labels**: edit the `status` field.
- **Comment**: append a dated entry under a `## Comments` section at the bottom of the file.
- **Close**: set `status: done` (or `wontfix`). Don't delete the file.
- **Pick next work**: any ticket with `status: ready-for-agent` whose `blocked-by` tickets are all `done`.
