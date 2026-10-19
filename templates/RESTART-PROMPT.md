# Restart prompt — <PRODUCT> <initiative>

<!-- Guidance: lives at docs/RESTART.md, which the SessionStart hook shows at the start of every
session (its first 60 lines; another path goes in .delivery/guards.json, session_start.docs).
Refresh it at the end of every major step: contract, decisions round, specs, plans, sessions,
tracker, each wave close. Keep the fenced block first and under about 25 lines. Never put
credentials, tokens or real data in it. Remove these comments when filled in. -->

Written <YYYY-MM-DD> at the end of <step>. Paste the fenced block into a fresh Claude Code session
at the repo root to resume from here. Everything below it is the context it points to.

```
You are resuming the planning and delivery of <PRODUCT> <initiative>. Do not redo finished work.
Read, in order:
  1. CLAUDE.md, AGENTS.md, .specify/memory/constitution.md (v<X.Y.Z>)
  2. docs/RESTART.md (this file): state, map, decisions, traps, open items
  3. docs/delivery/DECISIONS.md: every owner decision; the newest sections win
  4. ARCHITECTURE.md, SESSIONS.md (intro and Definition of done), docs/delivery/OPEN-QUESTIONS.md,
     docs/delivery/DISCREPANCIES.md
Then report what is done, what is open (section 5 below), and propose the next step.
Rules: staging and synthetic data only; no commit or push without the owner's say-so; the contract
wins; back up untracked docs before rewriting them; parallel agents never write the same file.
```

## 1. State

<Two or three lines: what the product is, what this initiative changes, and which step it is at.
Counts from the files: contract ids, specs, FRs, tasks, sessions, tickets.>

## 2. Where everything is

| What | Where |
| --- | --- |
| Owner decisions (newest last) | `docs/delivery/DECISIONS.md` |
| Open questions, discrepancies | `docs/delivery/OPEN-QUESTIONS.md`, `docs/delivery/DISCREPANCIES.md` |
| Contract | <`design/screen-map/` or `contracts/`> |
| Specs, plans, tasks | `specs/NNN-*/` |
| Sessions, run sheet, explainer | `SESSIONS.md`, `docs/delivery/RUN-SHEET.md`, `docs/delivery/SESSIONS-EXPLAINED.md` |
| Tracker | `docs/delivery/JIRA.md`, `docs/delivery/jira-map.json` |

## 3. Decisions that shape everything

<The five to ten decisions a newcomer gets wrong, each one line, citing its DECISIONS.md id.>

## 4. Traps already hit

<Each: symptom, cause, fix, one line. The same list as CLAUDE.md §0, plus planning-only traps.>

## 5. Open items

<Each: what, who it waits on, what it blocks. Mark items done with the date rather than deleting
them until the next refresh.>
