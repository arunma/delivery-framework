---
description: Run one session (a block in SESSIONS.md) or one small-project ticket - tests first, build, check against the contract - ending with the work staged and a report
argument-hint: "<session-name | TICKET-KEY> [--ci]"
---

Run the `delivery:run-session` skill for: $ARGUMENTS

If no session name or ticket key was given, list the next runnable sessions, those whose
dependencies are done (from SESSIONS.md and `python3 ${CLAUDE_PLUGIN_ROOT}/tools/sessionize.py status`),
one per line by step and name (`7. labels-domain — <summary> · <KEY>`), and ask which to run.
Work on the wave's branch; never create a branch. End with the work staged and the report. Never
commit or push.
