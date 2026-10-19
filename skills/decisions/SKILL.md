---
name: decisions
description: Phase 5 - maintain docs/delivery/DECISIONS.md (the owner's word, wins over every other document), OPEN-QUESTIONS.md (each with a recommendation and what it blocks), GLOSSARY.md (one concept, one name, banned synonyms) and DISCREPANCIES.md (every disagreement, never resolved silently). Use when the owner answers questions, when a document and the code or two documents disagree, when a new term appears, or when someone asks to record a decision.
argument-hint: "[record | round | questions | glossary | discrepancy | triage]"
---

# Decisions, open questions, glossary, discrepancies

Plugin root: `${CLAUDE_PLUGIN_ROOT}`. Read `${CLAUDE_PLUGIN_ROOT}/reference/CONVENTIONS.md` first.
Mode: `$ARGUMENTS` (default: show what is open in all four files).

Templates: `${CLAUDE_PLUGIN_ROOT}/templates/DECISIONS.md`, `OPEN-QUESTIONS.md`, `GLOSSARY.md`,
`DISCREPANCIES.md`. Files live in `docs/delivery/`. The prompt is
[prompt.md](prompt.md).

- **record:** write the owner's answer into DECISIONS.md the same day, dated, with the question id.
  Then apply it: to the contract source first (screen map source, OpenAPI file, data contract), then
  rebuild or re-validate. Answers left in chat get lost.
- **round:** after a planning round (specs, plans, a verification pass), collect every item the
  agents marked as needing the owner into one short list: each with its id, a recommendation and
  what it blocks. Show the list, not the agents' reports. When the owner answers "accept all",
  record it as one dated section, `## R<n> · <round> recommendations accepted (<date>)`, listing
  the ids; record exceptions one by one. Then apply them as in *record*.
- **questions:** every open question gets an id, a recommendation and what it blocks. A session that
  reaches an unanswered question builds the recommendation and says so, unless the question touches
  a non-negotiable principle; then it waits.
- **glossary:** every noun on the contract (screen copy, operation and field names, column names,
  command names) has one entry, with banned synonyms in the *Not* column. A concept that needs an
  explainer to tell it from another is a design defect, not a glossary entry.
- **discrepancy:** append, never resolve silently: both quotes with their sources, options, a
  recommendation, what is built meanwhile, Status: Open. Only the owner closes one.
- **triage:** list every Open entry, oldest first, with a proposed resolution; apply none without
  the owner.

Gate (CHECKLIST.md §5): every question has a recommendation and names what it blocks; every answer is
in DECISIONS.md and applied to the contract; the glossary covers the contract's nouns. Stage, ask.
