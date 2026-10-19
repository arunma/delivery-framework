# Phase 5 · Decisions, open questions, glossary, discrepancies

## 5a · Draft the questions

```
Collect every unresolved product question for <PRODUCT> from design/review.md, the design reviews,
the atlas (unresolved links, screens marked "to decide"), ARCHITECTURE.md §11 and
docs/delivery/DISCREPANCIES.md. Write them to docs/delivery/OPEN-QUESTIONS.md
(<framework>/templates/OPEN-QUESTIONS.md): one row each, with the options and their cost, a
recommendation with the reason, and what it blocks (screens, specs, sessions). Group them by theme.
Mark any question that touches a non-negotiable principle. Edit nothing else. Report the count by
theme and the five that block the most.
```

## 5b · Apply the owner's answers

```
The owner has answered <ids> (answers below, or in <file>). Record each in
docs/delivery/DECISIONS.md, dated and numbered (never renumber existing entries). Mark the rows in
OPEN-QUESTIONS.md as Answered (date, decision id). Then apply them: back up design/atlas-src
(uv run backup.py), change the atlas source, rebuild, and fix any broken link. List every spec,
constitution principle or session block that the answers now contradict. Do not edit specs; add each
contradiction to docs/delivery/DISCREPANCIES.md. Report: decisions recorded, atlas screens changed,
contradictions raised.
<answers>
```

## 5c · Glossary

```
Build docs/delivery/GLOSSARY.md (<framework>/templates/GLOSSARY.md) from the atlas: every noun a
person sees, one name each, with a one-sentence meaning and a Not column of synonyms that must not
appear. Search the atlas source and the specs for every Not word and list the hits (screen id or
file:line). Where two concepts need an explainer to tell apart, raise it as a design defect in
OPEN-QUESTIONS.md, not as a glossary entry. Report the entries and the hits.
```

## 5d · Discrepancy triage (before execution, and at every wave close)

```
Read docs/delivery/DISCREPANCIES.md. For every Open entry, check it against DECISIONS.md, the atlas
and the current specs. Propose one of: resolved by <decision/FR> (with evidence), amend the spec,
amend the atlas, or carry to <wave>. Apply nothing; present a table (id, proposal, evidence) and
wait for the owner.
```
