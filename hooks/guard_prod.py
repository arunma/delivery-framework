#!/usr/bin/env python3
"""PreToolUse(Bash): stop commands that target production.

Off until .delivery/guards.json sets prod_guard.enabled and lists regex patterns, e.g.
["--flavor[= ]prod\\b", "https://api\\.example\\.com"]. mode: ask (default), warn or block.
"""
import re
import sys

from common import config, decide, project_dir, read_input


def main():
    data = read_input()
    cfg = config(project_dir(data), "prod_guard")
    cmd = (data.get("tool_input") or {}).get("command", "")
    if not cfg or not cmd:
        return 0
    for pattern in cfg.get("patterns", []):
        try:
            hit = re.search(pattern, cmd)
        except re.error:
            print(f"delivery: bad prod_guard pattern {pattern!r}", file=sys.stderr)
            continue
        if hit:
            decide(cfg.get("mode", "ask"), f"delivery: this command matches the production pattern "
                   f"{pattern!r}. Staging and synthetic accounts only.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
