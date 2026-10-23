# Triage labels

The `triage` skill moves issues through five canonical roles. In this repo each role's label string equals its name. With the local-markdown tracker, the label is the value of the ticket's `status` frontmatter field.

| Role | Label | Meaning |
|---|---|---|
| needs-triage | `needs-triage` | Raw, unreviewed issue |
| needs-info | `needs-info` | Blocked on more information from the reporter |
| ready-for-agent | `ready-for-agent` | Fully specified; an agent can pick it up |
| ready-for-human | `ready-for-human` | Needs a human (judgement, access, or manual steps) |
| wontfix | `wontfix` | Closed without action |

To rename a label, change the Label column here; skills read this file instead of hardcoding names.
