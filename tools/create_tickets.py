#!/usr/bin/env python3
"""Create one Jira story per SESSIONS.md session and one task per backend item, with links.

    python3 tools/create_tickets.py --sessions SESSIONS.md --items backend-items.json \\
        --project <JIRA_KEY> --epic <EPIC> --label <initiative> --prefix "[<INITIATIVE>]" \\
        --map jira-map.json --write-index docs/JIRA.md --dry-run

SESSIONS.md format (see templates/SESSIONS.md):
  ## <Wave name>                                   sets the wave for the sessions below it
  ### <ID> · <summary> [· <KEY>-<n>]               one session; a trailing key means it exists
  *Depends on: <ID>, <ID>. Branch: `...`. Epic: <EPIC>.*   first non-blank line, every clause optional

Backend items file: a JSON list of
  {"id", "title", "kind": "task"|"bug"|"decision", "epic", "fallback", "sessions": [ids], "labels": []}

Links: each dependency "Blocks" the session that depends on it; each item "Relates" to its sessions.
Idempotent: ids in the map file (and keys written in headings) are not created again, the map is
saved after every create, and existing links are skipped. --dry-run needs no credentials.
"""
import argparse
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import jira  # noqa: E402

HEAD = re.compile(r"^###\s+(.+?)\s*$")
KEY = re.compile(r"^[A-Z][A-Z0-9]+-\d+$")


def parse_sessions(text):
    """Return [{id, summary, key, wave, deps, epic, branch}] in file order."""
    sessions, wave, lines = [], None, text.splitlines()
    in_fence = False
    for i, line in enumerate(lines):
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if line.startswith("## "):
            wave = line[3:].strip()
            continue
        m = HEAD.match(line)
        if not m or " · " not in m.group(1):
            continue
        parts = [p.strip() for p in m.group(1).split(" · ")]
        sid, rest = parts[0].strip("`"), parts[1:]
        key = None
        if len(rest) > 1 and KEY.match(rest[-1]):
            key = rest.pop()
        s = {"id": sid, "summary": " · ".join(rest), "key": key, "wave": wave, "deps": [],
             "epic": None, "branch": None}
        for nxt in lines[i + 1:]:
            if not nxt.strip():
                continue
            if nxt.strip().startswith("*") and any(w in nxt for w in ("Depends on", "Epic:", "Branch:")):
                body = nxt.strip().strip("*")
                d = re.search(r"Depends on:\s*([^.]*)", body)
                if d:
                    s["deps"] = [x.strip().strip("`") for x in d.group(1).split(",")
                                 if x.strip() and x.strip().lower() not in ("none", "—", "-")]
                e = re.search(r"Epic:\s*([^\s.*]+)", body)
                if e and "<" not in e.group(1):
                    s["epic"] = e.group(1)
                b = re.search(r"Branch:\s*`([^`]+)`", body)
                if b:
                    s["branch"] = b.group(1)
            break
        sessions.append(s)
    return sessions


def validate(sessions, items):
    errors, ids = [], [s["id"] for s in sessions] + [x["id"] for x in items]
    for i in sorted({i for i in ids if ids.count(i) > 1}):
        errors.append(f"duplicate id: {i}")
    known = {s["id"] for s in sessions}
    for s in sessions:
        errors += [f"{s['id']}: depends on unknown session {d}" for d in s["deps"] if d not in known]
    for x in items:
        if x.get("kind", "task") not in ("task", "bug", "decision"):
            errors.append(f"{x['id']}: kind must be task, bug or decision")
        errors += [f"{x['id']}: relates to unknown session {d}" for d in x.get("sessions", []) if d not in known]
    return errors


def load_map(path):
    p = pathlib.Path(path)
    return json.loads(p.read_text()) if p.exists() else {}


def save_map(path, mapping):
    pathlib.Path(path).write_text(json.dumps(mapping, indent=1, ensure_ascii=False) + "\n")


def plan(sessions, items, a):
    """Every issue to create, as dicts ready for display and for the API."""
    out = []
    for s in sessions:
        out.append({"id": s["id"], "type": a.story_type, "epic": s["epic"] or a.epic,
                    "labels": list(a.label), "summary": f"{a.prefix} {s['id']} · {s['summary']}".strip(),
                    "description": f"Session {s['id']} ({s['wave']}). The prompt is the {s['id']} block in "
                                   f"SESSIONS.md." + (f" Branch: {s['branch']}." if s["branch"] else "")})
    for x in items:
        kind = x.get("kind", "task")
        tag = {"task": "[Backend]", "bug": "[Bug]", "decision": "[Decision]"}[kind]
        desc = x.get("title", "")
        if x.get("fallback"):
            desc += f"\n\nClient fallback in this build: {x['fallback']}"
        out.append({"id": x["id"], "type": a.bug_type if kind == "bug" else a.task_type,
                    "epic": x.get("epic") or a.epic, "labels": list(a.label) + list(x.get("labels", [])),
                    "summary": f"{a.prefix}{tag} {x['id']} · {x['title']}".strip()[:250], "description": desc})
    return out


def links(sessions, items):
    out = []
    for s in sessions:
        out += [("Blocks", d, s["id"]) for d in s["deps"]]
    for x in items:
        out += [("Relates", x["id"], sid) for sid in x.get("sessions", [])]
    return out


def create(issue, project):
    fields = {"project": {"key": project}, "issuetype": {"name": issue["type"]},
              "summary": issue["summary"], "description": issue["description"], "labels": issue["labels"]}
    if issue["epic"]:
        fields["parent"] = {"key": issue["epic"]}
    code, res = jira.api("/rest/api/2/issue", {"fields": fields})
    if code != 201:
        raise jira.JiraError(f"create {issue['id']} failed: {code} {str(res)[:300]}")
    return res["key"]


def existing_links(key):
    code, res = jira.api(f"/rest/api/2/issue/{key}?fields=issuelinks")
    if code != 200:
        raise jira.JiraError(f"{key}: cannot read links: {code}")
    have = set()
    for l in res["fields"].get("issuelinks", []):
        name = l["type"]["name"]
        if "outwardIssue" in l:
            have.add((name, key, l["outwardIssue"]["key"]))
        if "inwardIssue" in l:
            have.add((name, l["inwardIssue"]["key"], key))
    return have


def link(kind, outward, inward):
    # The REST payload is inverted: "inwardIssue" A, "outwardIssue" B creates "A blocks B".
    # Verified on a live Jira Cloud project, Oct 2026 (a first run created every link backwards).
    payload = {"type": {"name": kind}, "inwardIssue": {"key": outward}, "outwardIssue": {"key": inward}}
    code, res = jira.api("/rest/api/2/issueLink", payload)
    if code not in (200, 201):
        raise jira.JiraError(f"link {outward} {kind} {inward} failed: {code} {str(res)[:200]}")


def write_index(path, sessions, items, mapping, issues, site):
    by_id = {i["id"]: i for i in issues}

    def key(i):
        k = mapping.get(i)
        return f"[{k}]({site}/browse/{k})" if k and site else (k or "not created")

    lines = ["# Jira index", "",
             "Generated by `tools/create_tickets.py` from SESSIONS.md and the backend items file. "
             "Regenerate rather than edit.", ""]
    waves = []
    for s in sessions:
        if s["wave"] not in waves:
            waves.append(s["wave"])
    for w in waves:
        lines += [f"## {w}", "", "| Id | Key | Epic | Summary | Depends on |", "| --- | --- | --- | --- | --- |"]
        for s in (s for s in sessions if s["wave"] == w):
            lines.append(f"| {s['id']} | {key(s['id'])} | {by_id[s['id']]['epic'] or '—'} | {s['summary']} | "
                         f"{', '.join(s['deps']) or '—'} |")
        lines.append("")
    if items:
        lines += ["## Backend tasks, bugs and decisions", "",
                  "| Id | Key | Kind | Epic | Summary | Fallback | Sessions |", "| --- | --- | --- | --- | --- | --- | --- |"]
        for x in items:
            lines.append(f"| {x['id']} | {key(x['id'])} | {x.get('kind', 'task')} | {by_id[x['id']]['epic'] or '—'} | "
                         f"{x['title']} | {x.get('fallback') or 'none'} | {', '.join(x.get('sessions', [])) or '—'} |")
        lines.append("")
    pathlib.Path(path).write_text("\n".join(lines))


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--sessions", required=True, help="path to SESSIONS.md")
    p.add_argument("--items", help="backend items JSON (optional)")
    p.add_argument("--project", required=True, help="Jira project key, e.g. <JIRA_KEY>")
    p.add_argument("--epic", help="default parent epic key")
    p.add_argument("--label", action="append", default=[], help="label on every ticket (repeatable)")
    p.add_argument("--prefix", default="", help='summary prefix, e.g. "[<INITIATIVE>]"')
    p.add_argument("--map", default="jira-map.json", help="id -> key map file (read and updated)")
    p.add_argument("--story-type", default="Story")
    p.add_argument("--task-type", default="Task")
    p.add_argument("--bug-type", default="Bug")
    p.add_argument("--write-index", help="write a PM-facing markdown index here")
    p.add_argument("--dry-run", action="store_true", help="print the plan; no credentials, no network")
    a = p.parse_args(argv)

    sessions = parse_sessions(pathlib.Path(a.sessions).read_text())
    items = json.loads(pathlib.Path(a.items).read_text()) if a.items else []
    if not sessions:
        print(f"no session blocks found in {a.sessions}", file=sys.stderr)
        return 1
    errors = validate(sessions, items)
    if errors:
        print("\n".join(f"error: {e}" for e in errors), file=sys.stderr)
        return 1

    mapping = load_map(a.map)
    for s in sessions:
        if s["key"] and "<" not in s["key"]:
            mapping.setdefault(s["id"], s["key"])
    issues, todo_links = plan(sessions, items, a), links(sessions, items)

    print(f"{len(sessions)} sessions, {len(items)} items, {len(todo_links)} links; map {a.map}")
    for i in issues:
        state = f"skip ({mapping[i['id']]})" if i["id"] in mapping else "create"
        print(f"  {state:<16} {i['id']:<12} {i['type']:<6} epic={i['epic'] or '—'} "
              f"labels={','.join(i['labels']) or '—'}  {i['summary']}")
    for kind, out_id, in_id in todo_links:
        print(f"  link             {out_id} {kind.lower()} {in_id}")

    site = jira.setting("JIRA_SITE", default="")
    if a.dry_run:
        if a.write_index:
            write_index(a.write_index, sessions, items, mapping, issues, site.rstrip("/"))
            print(f"wrote {a.write_index} (dry run: unmapped ids show 'not created')")
        print("dry run: nothing created")
        return 0

    jira.credentials()
    created = 0
    for i in issues:
        if i["id"] in mapping:
            continue
        mapping[i["id"]] = create(i, a.project)
        save_map(a.map, mapping)  # after every create, so a crash is resumable
        created += 1
        print(f"created {i['id']} -> {mapping[i['id']]}")
    made, cache = 0, {}
    for kind, out_id, in_id in todo_links:
        o, n = mapping[out_id], mapping[in_id]
        if o not in cache:
            cache[o] = existing_links(o)
        if (kind, o, n) in cache[o] or (kind == "Relates" and (kind, n, o) in cache[o]):
            continue
        link(kind, o, n)
        cache[o].add((kind, o, n))
        made += 1
    save_map(a.map, mapping)
    if a.write_index:
        write_index(a.write_index, sessions, items, mapping, issues, jira.credentials()["JIRA_SITE"])
    print(f"done: {created} created, {made} links added")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except jira.JiraError as e:
        print(f"create_tickets.py: {e}", file=sys.stderr)
        sys.exit(2)
