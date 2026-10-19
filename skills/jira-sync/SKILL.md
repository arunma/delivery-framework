---
name: jira-sync
description: Phase 12 - create the tracker tickets from SESSIONS.md and backend-items.json (a story per session, a task per backend item, bugs, decisions), add Blocks links in the correct direction and Relates links, write keys back into SESSIONS.md and specs, write the PM index, and build the filters and dashboard. Use when tickets need creating or syncing, when someone asks for the Jira dashboard, or after SESSIONS.md changes.
argument-hint: "[--dry-run | create | dashboard]"
---

# Jira sync

Plugin root: `${CLAUDE_PLUGIN_ROOT}`. Read `${CLAUDE_PLUGIN_ROOT}/reference/CONVENTIONS.md` first and
check the profile (phase `tracker`). Mode: `$ARGUMENTS` (default: dry run). Prompts:
`${CLAUDE_PLUGIN_ROOT}/prompts/12-jira.md`.

Credentials are `JIRA_SITE`, `JIRA_USER`, `JIRA_TOKEN` in the environment or the project's `.env`
(gitignored; the owner fills it; never print or write it). The tools never print the token.

1. Dry run and show the plan, then wait for the owner's go-ahead:
   `python3 ${CLAUDE_PLUGIN_ROOT}/tools/create_tickets.py --sessions SESSIONS.md --items docs/delivery/backend-items.json --project <KEY> --epic <EPIC> --label <INITIATIVE> --prefix "[<INITIATIVE>]" --map docs/delivery/jira-map.json --dry-run`
2. After the go-ahead, the same without `--dry-run`. Re-runs skip ids in the map, and the map is
   saved after every create, so a crash resumes.
3. **Check one Blocks link by hand** (`python3 ${CLAUDE_PLUGIN_ROOT}/tools/jira.py show` on both ends,
   or the Jira UI): it must read "<dependency> blocks <dependent>". The REST payload is inverted;
   the tool handles it, and this check proves it on your instance.
4. Write each key into its SESSIONS.md heading (` · <KEY>`), the block's Jira lines and branch, and
   each spec's **Jira** line; regenerate the index with `--write-index docs/delivery/JIRA.md`.
5. Dashboard: `python3 ${CLAUDE_PLUGIN_ROOT}/tools/jira_dashboard.py --project <KEY> --label <INITIATIVE> --name "<INITIATIVE> progress" --dry-run`,
   then for real. Gadgets must be pointed at the filters once by hand in the Jira UI; list the
   filter ids and which gadget gets which.
6. Priorities: foundation and wave blockers High, features Medium, later builds Low.

Gate (CHECKLIST.md §12). Report counts by type, links created and skipped, the hand-checked pair; stage, ask.
