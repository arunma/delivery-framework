#!/usr/bin/env python3
"""SessionStart: put the project's restart doc and the code graph's freshness in context.

Plain stdout from a SessionStart hook is added as context for Claude. Prints nothing unless the
project has a .delivery/ directory.
"""
import json
import subprocess
import sys

from common import config, project_dir, read_input


def graph_line(root):
    graph = root / "graphify-out" / "graph.json"
    if not graph.is_file():
        return "Code graph: none (graphify-out/graph.json missing; build it with `graphify update .`)."
    try:
        last = int(subprocess.run(["git", "-C", str(root), "log", "-1", "--format=%ct"],
                                  capture_output=True, text=True, timeout=5).stdout.strip() or 0)
    except (OSError, ValueError, subprocess.TimeoutExpired):
        last = 0
    if last and graph.stat().st_mtime < last:
        return "Code graph: STALE (older than the last commit). Run `graphify update .` before reading code."
    return "Code graph: current (graphify-out/graph.json). Query it before broad file reads."


def main():
    data = read_input()
    root = project_dir(data)
    cfg = config(root, "session_start")
    if not cfg:
        return 0
    lines = ["[delivery] Project context"]
    profile = root / ".delivery" / "profile.json"
    if profile.is_file():
        try:
            p = json.loads(profile.read_text())
            lines.append(f"Profile: surfaces {', '.join(p.get('surfaces', []))}; track {p.get('track')}; "
                         f"tier {p.get('tier')} (.delivery/PROFILE.md lists the phases on, off and swapped).")
        except ValueError:
            lines.append("Profile: .delivery/profile.json is not valid JSON; re-run /delivery:assess.")
    for name in cfg["docs"]:
        doc = root / name
        if doc.is_file():
            text = doc.read_text(errors="replace").splitlines()
            lines += [f"Restart doc: {name}", *text[: cfg["max_lines"]]]
            if len(text) > cfg["max_lines"]:
                lines.append(f"... ({len(text) - cfg['max_lines']} more lines in {name})")
            break
    if cfg.get("graph"):
        lines.append(graph_line(root))
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
