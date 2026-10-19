# Phase 12 · Jira

Needs `.env` with `JIRA_SITE`, `JIRA_USER` and `JIRA_TOKEN`. The tools never print the token.

## 12a · Backend items file

```
Write docs/delivery/backend-items.json from design/screen-map-src/backend_map.py ITEMS and
docs/delivery/BACKEND-AUDIT.md: one object per item {"id","title","kind":"task"|"bug"|"decision",
"epic","fallback","sessions":[…],"labels":[…]}, plus the audit's prerequisites (kind "bug" where
they are defects), and every open owner decision that blocks a later build (kind "decision"). Use
the session ids in SESSIONS.md. Validate it with create_tickets.py --dry-run.
```

## 12b · Create tickets

```
Create the Jira tickets for <INITIATIVE>.
1. python3 tools/create_tickets.py --sessions SESSIONS.md --items docs/delivery/backend-items.json
   --project <JIRA_KEY> --epic <EPIC> --label <INITIATIVE> --prefix "[<INITIATIVE>]"
   --map docs/delivery/jira-map.json --dry-run
   Show me the plan (creates and links) and wait for my go-ahead.
2. After the go-ahead, run it without --dry-run. Then check one Blocks link by hand
   (python3 tools/jira.py show on both ends, or the Jira UI) to confirm the direction reads
   "<dependency> blocks <dependent>".
3. Write each key back into its SESSIONS.md heading (" · <KEY>"), its block's Jira lines and branch
   names, and each spec's **Jira** line. Run with --write-index docs/delivery/JIRA.md.
4. Set priorities: foundation and anything blocking a wave High, screens Medium, later builds Low.
Never print the token or the user. Report: counts by type, links created, and anything skipped.
```

## 12c · Dashboard and PM summary

```
Run python3 tools/jira_dashboard.py --project <JIRA_KEY> --label <INITIATIVE> --name "<INITIATIVE>
progress" --dry-run, show me the filters, then run it for real. Gadget configuration cannot be set
reliably through the API: list the filter ids and URLs and the gadgets I must point at them, once,
in the Jira UI. Then write a one-page PM summary (docs/delivery/JIRA.md header, or a Confluence page
if asked): what the initiative ships, the waves, how progress is recorded (each session moves its own
ticket with evidence), the filters, and the owner tasks.
```

Optional: Jira Automation rules (a branch or PR whose name contains the key moves the ticket to In
Progress; merging moves it to In Review). Sessions still move their own tickets with `jira.py`.
