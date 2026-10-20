---
description: Run a whole wave - one fresh child agent per session in dependency order, its questions brought to you, a stop after each so you commit with `!`, then the wave's close and the push and PR commands for you to run
argument-hint: "<wave number | name>"
---

Run the `delivery:run-wave` skill for wave: $ARGUMENTS

If no wave was given, use the current branch's wave, or list the waves and ask which. Each session
runs in its own `session-runner` subagent and ends staged. Never commit or push: the owner commits
each session with `! git commit -m "<KEY>: <summary>"` and pushes once after the close.
