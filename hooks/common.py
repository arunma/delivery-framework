"""Shared helpers for the delivery hooks. Standard library only.

Every hook is a no-op unless the project has opted in by having a `.delivery/` directory
(created by /delivery:assess or /delivery:start). Settings come from `.delivery/guards.json`
(template: templates/guards.json); a missing file or key falls back to DEFAULTS.
"""
import json
import os
import pathlib
import sys

DEFAULTS = {
    "git_guard": {"enabled": True, "approval_file": ".delivery/APPROVED", "approval_ttl_minutes": 15,
                  "env_flag": "DELIVERY_ALLOW_GIT"},
    "secrets_guard": {"enabled": True, "read_mode": "ask"},
    "prod_guard": {"enabled": False, "patterns": [], "mode": "ask"},
    "session_start": {"enabled": True, "docs": ["ARCHITECTURE-PROMPT.md", "docs/RESTART.md"],
                      "max_lines": 60, "graph": True},
}


def read_input():
    try:
        return json.load(sys.stdin)
    except ValueError:
        return {}


def project_dir(data):
    return pathlib.Path(os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd())


def config(root, section):
    """The section's settings, or None when the project has not opted in or disabled it."""
    if not (root / ".delivery").is_dir():
        return None
    merged = dict(DEFAULTS[section])
    f = root / ".delivery" / "guards.json"
    if f.is_file():
        try:
            merged.update(json.loads(f.read_text()).get(section) or {})
        except ValueError:
            print(f"delivery hooks: {f} is not valid JSON; using defaults", file=sys.stderr)
    return merged if merged.get("enabled") else None


def block(message):
    """Blocking exit: PreToolUse stops the tool call and shows stderr to Claude."""
    print(message, file=sys.stderr)
    sys.exit(2)


def decide(mode, message):
    """mode: block (exit 2), ask (the user confirms), or warn (shown to the user, tool runs)."""
    if mode == "block":
        block(message)
    if mode == "ask":
        out = {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "ask",
                                      "permissionDecisionReason": message}}
    else:
        out = {"systemMessage": message}
    print(json.dumps(out))
    sys.exit(0)
