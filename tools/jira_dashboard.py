#!/usr/bin/env python3
"""Create saved filters and a dashboard for one initiative label.

    python3 tools/jira_dashboard.py --project <JIRA_KEY> --label <initiative> --name "<PROJECT> delivery" [--dry-run]

Filters are looked up by name first, so a re-run reuses them. The dashboard is shared with the
project.

Limitation (learned the hard way): Jira Cloud's REST API can create a dashboard and add gadgets, but
setting which filter a gadget shows did not work reliably through the API. Configure each gadget once
by hand in the Jira UI; this script prints the filter ids and URLs to pick. Reads JIRA_SITE,
JIRA_USER and JIRA_TOKEN like tools/jira.py. --dry-run needs no credentials.
"""
import argparse
import pathlib
import sys
import urllib.parse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import jira  # noqa: E402

NOTE = ("NOTE: gadget configuration (which filter each gadget shows) cannot be set reliably through "
        "the REST API. Open the dashboard once in the Jira UI, edit each gadget and pick the filter "
        "listed below.")

# Gadget module keys for Jira Cloud. Adding them may work; configuring them is a manual step.
GADGETS = [
    ("com.atlassian.jira.gadgets:filter-results-gadget", "In progress"),
    ("com.atlassian.jira.gadgets:pie-chart-gadget", "All tickets"),
    ("com.atlassian.jira.gadgets:filter-results-gadget", "Blocked or flagged"),
    ("com.atlassian.jira.gadgets:created-vs-resolved-issues-chart-gadget", "All tickets"),
]


def filters(project, label):
    base = f'project = {project} AND labels = "{label}"'
    return [
        ("All tickets", f"{base} ORDER BY Rank"),
        ("Sessions open", f"{base} AND issuetype = Story AND statusCategory != Done ORDER BY Rank"),
        ("In progress", f'{base} AND statusCategory = "In Progress" ORDER BY updated DESC'),
        ("Done this week", f"{base} AND statusCategory = Done AND resolved >= startOfWeek() ORDER BY resolved DESC"),
        ("Backend tasks", f'{base} AND issuetype = Task AND summary ~ "Backend" ORDER BY Rank'),
        ("Bugs", f"{base} AND issuetype = Bug ORDER BY priority DESC"),
        ("Decisions", f'{base} AND summary ~ "Decision" ORDER BY created'),
        ("Blocked or flagged", f'{base} AND (issueLinkType = "is blocked by" AND statusCategory != Done '
                               f'OR Flagged is not EMPTY) ORDER BY Rank'),
    ]


def find_filter(name):
    q = urllib.parse.urlencode({"filterName": f'"{name}"', "expand": "jql"})
    code, res = jira.api(f"/rest/api/3/filter/search?{q}")
    if code != 200:
        raise jira.JiraError(f"filter search failed: {code} {str(res)[:200]}")
    return next((f for f in res.get("values", []) if f["name"] == name), None)


def ensure_filter(name, jql, project_id):
    f = find_filter(name)
    if f:
        if f.get("jql") != jql:
            code, res = jira.api(f"/rest/api/3/filter/{f['id']}", {"name": name, "jql": jql}, method="PUT")
            if code != 200:
                raise jira.JiraError(f"update filter {name!r} failed: {code} {str(res)[:200]}")
        return f["id"], "reused"
    code, res = jira.api("/rest/api/3/filter", {
        "name": name, "jql": jql,
        "sharePermissions": [{"type": "project", "project": {"id": project_id}}]})
    if code != 200:
        raise jira.JiraError(f"create filter {name!r} failed: {code} {str(res)[:200]}")
    return res["id"], "created"


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--project", required=True, help="Jira project key, e.g. <JIRA_KEY>")
    p.add_argument("--label", required=True, help="initiative label every ticket carries")
    p.add_argument("--name", required=True, help="dashboard name; filters are named '<name> · <filter>'")
    p.add_argument("--dry-run", action="store_true", help="print the plan; no credentials, no network")
    a = p.parse_args(argv)

    plan = [(f"{a.name} · {n}", jql) for n, jql in filters(a.project, a.label)]
    if a.dry_run:
        print("Filters (created, or reused by name):")
        for n, jql in plan:
            print(f"  {n}\n    {jql}")
        print(f"Dashboard: {a.name!r}, shared with project {a.project}")
        print("Gadgets to add: " + "; ".join(f"{g.split(':')[1]} -> {f}" for g, f in GADGETS))
        print(NOTE)
        print("dry run: nothing created")
        return 0

    site = jira.credentials()["JIRA_SITE"]
    code, proj = jira.api(f"/rest/api/3/project/{a.project}")
    if code != 200:
        raise jira.JiraError(f"project {a.project}: {code}")
    ids = {}
    for n, jql in plan:
        ids[n], how = ensure_filter(n, jql, proj["id"])
        print(f"{how:<8} filter {ids[n]}  {n}  {site}/issues/?filter={ids[n]}")

    code, res = jira.api("/rest/api/3/dashboard/search?" + urllib.parse.urlencode({"dashboardName": a.name}))
    dash = next((d for d in (res.get("values", []) if code == 200 else []) if d["name"] == a.name), None)
    if dash:
        print(f"reused   dashboard {dash['id']}  {site}/jira/dashboards/{dash['id']}")
    else:
        code, dash = jira.api("/rest/api/3/dashboard", {
            "name": a.name, "description": f"Delivery dashboard for label {a.label}",
            "sharePermissions": [{"type": "project", "project": {"id": proj["id"]}}],
            "editPermissions": []})
        if code != 200:
            raise jira.JiraError(f"create dashboard failed: {code} {str(dash)[:200]}")
        print(f"created  dashboard {dash['id']}  {site}/jira/dashboards/{dash['id']}")
        for module, fname in GADGETS:
            code, res = jira.api(f"/rest/api/3/dashboard/{dash['id']}/gadget",
                                 {"moduleKey": module, "title": f"{fname}"})
            state = "added" if code == 200 else f"not added ({code})"
            print(f"  gadget {module.split(':')[1]}: {state}; configure it to show '{a.name} · {fname}'")
    print(NOTE)
    for n in ids:
        print(f"  {n}: filter {ids[n]}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except jira.JiraError as e:
        print(f"jira_dashboard.py: {e}", file=sys.stderr)
        sys.exit(2)
