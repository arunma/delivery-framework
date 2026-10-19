---
description: Run one session (a SESSIONS.md block) or one tier-S ticket through the execution loop, ending staged with a report
argument-hint: "<SESSION-ID | TICKET-KEY> [--ci]"
---

Run the `delivery:run-session` skill for: $ARGUMENTS

If no session id or ticket key was given, list the next sessions whose dependencies are done
(from SESSIONS.md and `python3 ${CLAUDE_PLUGIN_ROOT}/tools/sessionize.py status`) and ask which to run.
End with the work staged and the report. Never commit or push.
