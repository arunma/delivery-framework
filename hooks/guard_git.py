#!/usr/bin/env python3
"""PreToolUse(Bash): block `git commit` and `git push` unless the owner has approved.

Approval is either the env flag (default DELIVERY_ALLOW_GIT=1, for a CI wrapper that commits on
the owner's behalf) or the approval file (default .delivery/APPROVED) that the owner creates by
hand and that expires after approval_ttl_minutes. The agent may not create the approval file:
guard_secrets.py blocks writes to it.
"""
import os
import re
import sys
import time

from common import block, config, project_dir, read_input

GIT = re.compile(r"(^|[;&|(`$]|\s)git(\s+(-C|-c)\s+\S+|\s+--?[\w-]+(=\S+)?)*\s+(commit|push)\b")


def approved(root, cfg):
    if os.environ.get(cfg["env_flag"]) == "1":
        return True
    f = root / cfg["approval_file"]
    return f.is_file() and time.time() - f.stat().st_mtime < cfg["approval_ttl_minutes"] * 60


def main():
    data = read_input()
    root = project_dir(data)
    cfg = config(root, "git_guard")
    cmd = (data.get("tool_input") or {}).get("command", "")
    if not cfg or not GIT.search(cmd) or approved(root, cfg):
        return 0
    block("delivery: git commit/push is blocked until the owner approves it. Stage the work, show "
          "the staged files and a proposed subject, and ask. The owner approves by running "
          f"`touch {cfg['approval_file']}` (valid {cfg['approval_ttl_minutes']} min) or by setting "
          f"{cfg['env_flag']}=1. Approval of the work is not approval to commit.")


if __name__ == "__main__":
    sys.exit(main())
