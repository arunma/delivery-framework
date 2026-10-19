# Phase 1 · Project setup

Usually done by the bootstrap prompt. Use these when setting up separately, or when re-doing one part.

## 1a · Instructions files

```
Write CLAUDE.md and AGENTS.md for <PROJECT> from <framework>/templates/CLAUDE.md and
templates/AGENTS.md. Keep every existing instruction (merge it, or move reference material to
docs/AGENTS.md); list anything you would drop and ask. CLAUDE.md §0: every trap known so far, each
as symptom, cause and fix, with the exact flag or command. §1: a summary of
.specify/memory/constitution.md at its current version. §4: commands, each verified by running it.
Keep CLAUDE.md under ~150 lines. Commit nothing. Report: line count, the traps, what moved where.
```

## 1b · Jira setup (owner does the admin; the agent checks and documents)

Owner: create the project `<JIRA_KEY>`, one epic per feature area, and an API token. Then put
`JIRA_SITE`, `JIRA_USER` and `JIRA_TOKEN` in `.env`.

```
Check the tracker setup for <PROJECT>. Confirm .env is gitignored (git check-ignore .env). Run
python3 tools/jira.py show <EPIC> and report the summary line only — never print the token or user.
Write CLAUDE.md §3: project <JIRA_KEY>, epics (key and name), the initiative label <INITIATIVE>, the
key in wave branch names (one branch per wave, wave/<closing key>-<wave-name>, the key of the wave's
close session), commit subjects (<JIRA_KEY>-NN: …, one commit per session, made by the owner) and code
comments, one push and one PR per wave after its close,
scratch TODOs in <scratch tracker>, no markdown TODO lists. Create no tickets. Commit nothing.
```
