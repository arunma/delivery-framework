#!/usr/bin/env python3
"""Move a Jira ticket through its workflow and record evidence on it.

Sessions use this to keep Jira in step with the work:

    python3 tools/jira.py show <JIRA_KEY>-12
    python3 tools/jira.py start <JIRA_KEY>-12          # -> In Progress
    python3 tools/jira.py comment <JIRA_KEY>-12 "Maestro: 12/12 green; parity: design/parity/001.md"
    python3 tools/jira.py done <JIRA_KEY>-12 "PR #40; parity passed"   # comment, then -> Done
    python3 tools/jira.py select <JIRA_KEY>-12         # -> Selected for Development
    python3 tools/jira.py backlog <JIRA_KEY>-12        # -> Backlog

Settings come from the environment or from the nearest .env (searched upwards from the current
directory, then from this script's directory):

    JIRA_SITE   https://<your-site>.atlassian.net
    JIRA_USER   the account the API token belongs to
    JIRA_TOKEN  an Atlassian API token

Target status names can be overridden with JIRA_STATUS_START, JIRA_STATUS_DONE,
JIRA_STATUS_SELECT and JIRA_STATUS_BACKLOG. The token and user are never printed.
"""
import base64
import json
import os
import pathlib
import re
import sys
import urllib.error
import urllib.request

DEFAULT_STATUS = {"select": "Selected for Development", "start": "In Progress", "done": "Done",
                  "backlog": "Backlog"}


class JiraError(Exception):
    """A clean, user-facing failure (no traceback)."""


def _env_files():
    seen = []
    for start in (pathlib.Path.cwd(), pathlib.Path(__file__).resolve().parent):
        for d in (start, *start.parents):
            f = d / ".env"
            if f not in seen and f.is_file():
                seen.append(f)
    return seen


def setting(name, default=None):
    """Value of name from the environment, else the nearest .env that defines it."""
    if os.environ.get(name):
        return os.environ[name]
    for f in _env_files():
        m = re.search(rf'^\s*(?:export\s+)?{name}\s*=\s*["\']?([^"\'\n]+)', f.read_text(), re.M)
        if m:
            return m.group(1).strip()
    return default


def credentials():
    vals = {n: setting(n) for n in ("JIRA_SITE", "JIRA_USER", "JIRA_TOKEN")}
    missing = [n for n, v in vals.items() if not v]
    if missing:
        raise JiraError(f"missing {', '.join(missing)}: set them in the environment or in .env")
    vals["JIRA_SITE"] = vals["JIRA_SITE"].rstrip("/")
    return vals


def status_names():
    return {k: setting(f"JIRA_STATUS_{k.upper()}", v)
            for k, v in DEFAULT_STATUS.items()}


def api(path, payload=None, method=None, creds=None):
    """Call the Jira REST API. Returns (status code, parsed JSON or raw text)."""
    c = creds or credentials()
    auth = base64.b64encode(f"{c['JIRA_USER']}:{c['JIRA_TOKEN']}".encode()).decode()
    req = urllib.request.Request(
        c["JIRA_SITE"] + path,
        data=json.dumps(payload).encode() if payload is not None else None,
        method=method or ("POST" if payload is not None else "GET"),
        headers={"Authorization": f"Basic {auth}", "Accept": "application/json",
                 "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read().decode()
            try:
                return r.status, (json.loads(body) if body else {})
            except ValueError:
                return r.status, body
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(errors="replace")
    except (urllib.error.URLError, OSError) as e:
        raise JiraError(f"cannot reach {c['JIRA_SITE']}: {getattr(e, 'reason', e)}")


def comment(key, text):
    code, res = api(f"/rest/api/2/issue/{key}/comment", {"body": text})
    if code != 201:
        raise JiraError(f"comment on {key} failed: {code} {str(res)[:200]}")


def move(key, target):
    code, res = api(f"/rest/api/2/issue/{key}/transitions")
    if code != 200:
        raise JiraError(f"{key}: {code} {str(res)[:200]}")
    for t in res["transitions"]:
        if t["to"]["name"] == target:
            code, res = api(f"/rest/api/2/issue/{key}/transitions", {"transition": {"id": t["id"]}})
            if code != 204:
                raise JiraError(f"{key} -> {target} failed: {code} {str(res)[:200]}")
            return
    names = [t["to"]["name"] for t in res["transitions"]]
    raise JiraError(f"{key}: no transition to {target!r}; available: {names}")


def main(argv):
    commands = (*DEFAULT_STATUS, "show", "comment")
    if len(argv) < 2 or argv[1] in ("-h", "--help", "help"):
        print(__doc__.strip())
        return 0
    if argv[1] not in commands or len(argv) < 3:
        print(f"usage: jira.py {{{'|'.join(commands)}}} KEY [text]   (--help for more)", file=sys.stderr)
        return 2
    cmd, key, text = argv[1], argv[2], " ".join(argv[3:])
    if cmd == "comment" and not text:
        raise JiraError("comment needs text")
    credentials()  # fail fast and cleanly before any request
    if cmd == "show":
        code, res = api(f"/rest/api/2/issue/{key}?fields=summary,status")
        if code != 200:
            raise JiraError(f"{key}: {code}")
        print(f"{key} [{res['fields']['status']['name']}] {res['fields']['summary']}")
        return 0
    if cmd == "comment":
        comment(key, text)
    else:
        if text:
            comment(key, text)
        move(key, status_names()[cmd])
    print(f"{key}: {cmd} ok")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except JiraError as e:
        print(f"jira.py: {e}", file=sys.stderr)
        sys.exit(2)
    except KeyboardInterrupt:
        sys.exit(130)
