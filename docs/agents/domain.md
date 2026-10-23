# Domain docs

## Layout: single-context

- `GLOSSARY.md` (repo root): the project's domain language, one entry per term, with its meaning and any terms to avoid.
- `docs/adr/`: Architecture Decision Records, one file per hard-to-reverse decision, named `NNNN-<slug>.md`.

## Rules for consumers

- Before working on a feature, read `GLOSSARY.md` and use its terms in code, tickets, and conversation.
- If a term is missing, fuzzy, or overloaded, flag it (via `/domain-modeling` or `/grill-with-docs`) instead of inventing a synonym.
- Read the ADRs relevant to the area you're touching. Don't contradict an ADR silently; propose a new one that supersedes it.
- Either may not exist yet. Create them lazily, the first time there's something to record.
