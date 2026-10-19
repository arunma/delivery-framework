#!/usr/bin/env python3
"""Check that a run sheet lists every SESSIONS.md session exactly once, in dependency order.

    python3 tools/runsheet.py RUN-SHEET.md --sessions SESSIONS.md

The run sheet's session headings are "#### <step>. <name> — <summary> · <KEY>" (step optional).
Reports sessions missing from the sheet, listed twice, unknown to SESSIONS.md, or listed before a
session they depend on. Exit codes: 0 ok, 1 problems found, 2 usage error. Standard library only.
"""
import argparse
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from sessionize import blocks  # noqa: E402

STEP = re.compile(r"^####\s+(?:\d+\.\s+)?`?([\w·\-]+)`?\s+[—·]")


def sheet_ids(text):
    """Session names from the run sheet's #### headings, in order, outside code fences."""
    out, fence = [], False
    for line in text.splitlines():
        if line.startswith("```"):
            fence = not fence
            continue
        m = STEP.match(line)
        if not fence and m:
            out.append(m.group(1))
    return out


def check(sheet_text, sessions_text):
    deps = {}
    for sid, _, meta, _, _ in blocks(sessions_text):
        dm = re.search(r"Depends on:\s*([^.]*)", meta)
        deps[sid] = [d.strip().strip("`") for d in (dm.group(1).split(",") if dm else [])
                     if d.strip() and d.strip().lower() not in ("none", "nothing", "—", "-")]
    order = sheet_ids(sheet_text)
    errors = [f"{s}: in SESSIONS.md but not in the run sheet" for s in deps if s not in order]
    errors += [f"{s}: listed {order.count(s)} times" for s in sorted(set(order)) if order.count(s) > 1]
    errors += [f"{s}: in the run sheet but not in SESSIONS.md" for s in sorted(set(order) - set(deps))]
    seen = set()
    for s in order:
        errors += [f"{s}: listed before {d}, which it depends on" for d in deps.get(s, [])
                   if d in order and d not in seen]
        seen.add(s)
    return errors


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("sheet")
    ap.add_argument("--sessions", required=True)
    a = ap.parse_args(argv)
    errors = check(pathlib.Path(a.sheet).read_text(), pathlib.Path(a.sessions).read_text())
    for e in errors:
        print(f"ERROR {e}")
    print(f"runsheet.py: {len(sheet_ids(pathlib.Path(a.sheet).read_text()))} sessions listed, "
          f"{len(errors)} problems")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
