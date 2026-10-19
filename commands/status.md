---
description: Report delivery status - tasks done per session from tasks.md, ticket status from the tracker, and the drift between them
argument-hint: "[--jira]"
---

Report the delivery status of this project. Arguments: $ARGUMENTS

1. Show `.delivery/PROFILE.md` in one line (surfaces, track, tier); if it is missing, say so and
   suggest `/delivery:assess`.
2. Run `python3 ${CLAUDE_PLUGIN_ROOT}/tools/sessionize.py status --sessions SESSIONS.md specs/*/tasks.md --map docs/delivery/jira-map.json`
   and add `--jira` when the arguments include it and `.env` credentials exist (never print them).
   Without SESSIONS.md (tier S or M), list the specs and their tasks.md progress instead.
3. Count the Open entries in `docs/delivery/DISCREPANCIES.md` and `OPEN-QUESTIONS.md`, and list the
   verification files (`design/parity/*.md`, `verification/*.md`) with Open rows.
4. Report in at most 15 lines: per-session progress, every drift line, what is blocked and on whom,
   and the next session to run. Change nothing.
