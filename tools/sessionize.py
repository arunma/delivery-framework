#!/usr/bin/env python3
"""Generate, validate and track SESSIONS.md blocks from the session phases of tasks.md.

    python3 tools/sessionize.py generate specs/*/tasks.md [--template templates/SESSIONS.md]
                                         [--wave wave-1] [--close-key ABC-9] [--first-step 1]
                                         [--set "<JIRA_KEY>=ABC" ...] [--out SESSIONS.draft.md]
    python3 tools/sessionize.py validate SESSIONS.md [--strict]
    python3 tools/sessionize.py status --sessions SESSIONS.md specs/*/tasks.md
                                       [--map docs/delivery/jira-map.json] [--jira]
    python3 tools/sessionize.py wave <wave> [--sessions SESSIONS.md] [--tasks specs/*/tasks.md]

generate  one block per "## Phase n — <name> · <KEY>: <summary>" in each tasks.md, built from the
          first full implementation block of the SESSIONS template, filled from the phase's tasks
          and plan.md's "Session mapping" row, then the wave's close block, close-<wave>. Headings
          are "### <step>. <name> — <summary> · <KEY>"; every block names the wave's branch,
          wave/<close key>-<wave>. Placeholders it cannot fill stay as <...> for the agent.
validate  every session block is self-contained (guards, Jira start/done, GAPS IN, HANDOFF, the
          five Definition of done steps, the report), dependencies resolve, ids are unique, nothing
          says "see above". Leftover <placeholders> are warnings, or errors with --strict.
status    per session: tasks done/total from tasks.md, the ticket key, and with --jira the ticket's
          status; reports drift between them. Without --jira it needs no credentials.
wave      one wave as JSON: its title, branch, sessions in dependency order (step, name, key,
          depends_on, after (dependencies outside the wave), parallel_with, close) and, with
          --tasks, each session's ticked/total tasks. <wave> is a number (0 = the first
          section, N = "Wave N"), a word from a section title ("close", "model"), the wave branch
          or a word in it, or a session name. Waves are the "## " sections holding session blocks.

Exit codes: 0 ok, 1 problems found, 2 usage error. Standard library only.
"""
import argparse
import json
import pathlib
import re
import sys

# "## Phase 1: Session S01 · summary" (template), "## Phase 1a — S03a1 · ABC-148: summary", or a
# kebab-case name id, "## Phase 3 — labels-domain · ABC-148: summary" ("Session" optional; an
# optional tracker key, or its <JIRA_KEY>-NN placeholder, after the id is skipped). A name id must
# be followed by " · " or ":".
PHASE = re.compile(r"^##\s+Phase\s+[\w.]+\s*[:.\-—]\s*(?:Session\s+)?`?"
                   r"([A-Za-z][\w·\-]*\d[\w·\-]*|[a-z][a-z0-9]*(?:-[a-z0-9]+)+(?=`?\s*[·:]))`?"
                   r"(?:\s*·\s*(?:[A-Z][A-Z0-9]+-\d+|<[A-Z_]+>-NN))?\s*(?:[·:\-—]\s*(.*))?$")
DEPENDS = re.compile(r"^\*\*Depends on\*\*\s*:\s*(.+)$")
TASK = re.compile(r"^\s*-\s+\[([ xX])\]\s+(T\d+)\b(.*)$")
FR = re.compile(r"\bFR-\d+[a-z]?\b")
STORY = re.compile(r"\[US(\d+)\]")
HEAD = re.compile(r"^###\s+(.+?)\s*$")
# "### 3. labels-domain — summary · ABC-148": a step number, then the name that is the id; the
# " · KEY" suffix is absent before tickets exist.
NAMED = re.compile(r"^\d+\.\s+`?([a-z][a-z0-9]*(?:-[a-z0-9]+)+)`?\s+—")
KEY = re.compile(r"^[A-Z][A-Z0-9]+-\d+$")

# What every block must carry, as (label, regex). Wave-close blocks use CLOSE_REQUIRED.
REQUIRED = [
    ("Jira start", r"jira\.py start"), ("Jira done", r"jira\.py done"),
    ("GAPS IN", r"GAPS IN"), ("HANDOFF", r"HANDOFF"), ("no commit guard", r"[Nn]o commit"),
    ("synthetic accounts guard", r"[Ss]ynthetic"), ("DISCREPANCIES", r"DISCREPANCIES"),
    ("DoD 1 tests", r"^\s*1\.\s+Tests"), ("DoD 2 E2E", r"^\s*2\.\s+E2E"),
    ("DoD 3 verification", r"^\s*3\.\s+(Parity|Verification|Contract|Answer|Golden|Plan|Eval)"),
    ("DoD 4 closing review", r"^\s*4\.\s+Closing review"), ("DoD 5 lint", r"^\s*5\.\s+.*lint"),
    ("report", r"Report at the end"), ("stage and ask", r"stage the work|[Ss]tage, report"),
]
CLOSE_REQUIRED = [
    ("Jira start", r"jira\.py start"), ("GAPS IN", r"GAPS IN"), ("no commit guard", r"[Nn]o commit"),
    ("run every flow", r"[Rr]un every"), ("not-done list", r"NOT done"), ("report", r"Report"),
]


def compress(frs):
    """FR-001, FR-002, FR-003, FR-007 -> FR-001–FR-003, FR-007."""
    nums = sorted({(int(re.sub(r"\D", "", f[3:]) or 0), f) for f in frs})
    out, run = [], []
    for n, f in nums:
        if run and n == run[-1][0] + 1 and not f[-1].isalpha() and not run[-1][1][-1].isalpha():
            run.append((n, f))
            continue
        if run:
            out.append(run[0][1] if len(run) == 1 else f"{run[0][1]}–{run[-1][1]}")
        run = [(n, f)]
    if run:
        out.append(run[0][1] if len(run) == 1 else f"{run[0][1]}–{run[-1][1]}")
    return ", ".join(out)


def parse_tasks(path):
    """[{id, summary, spec, deps, tasks: [(id, done, text)], frs, stories}] in file order."""
    path = pathlib.Path(path)
    spec = path.parent.name
    phases, cur = [], None
    for line in path.read_text().splitlines():
        m = PHASE.match(line)
        if m:
            cur = {"id": m.group(1), "summary": (m.group(2) or "").strip(), "spec": spec, "deps": None,
                   "tasks": [], "frs": set(), "stories": set(), "file": str(path)}
            phases.append(cur)
            continue
        if line.startswith("## "):
            cur = None
            continue
        if cur is None:
            continue
        d = DEPENDS.match(line.strip())
        if d and cur["deps"] is None:
            cur["deps"] = [x.strip().strip("`") for x in d.group(1).split(",")
                           if x.strip() and x.strip().lower() not in ("none", "—", "-")]
            continue
        t = TASK.match(line)
        if t:
            cur["tasks"].append((t.group(2), t.group(1) != " ", t.group(3).strip()))
            cur["frs"] |= set(FR.findall(line))
            cur["stories"] |= set(STORY.findall(line))
    prev = None
    for ph in phases:
        if ph["deps"] is None:
            ph["deps"] = [prev] if prev else []
        prev = ph["id"]
    return phases


def plan_mapping(spec_dir):
    """{session id: {frs, stories, screens, flows}} from plan.md's Session mapping table."""
    plan = pathlib.Path(spec_dir) / "plan.md"
    rows = {}
    if not plan.is_file():
        return rows
    in_table = False
    for line in plan.read_text().splitlines():
        if re.match(r"^#+\s+.*Session mapping", line, re.I):
            in_table = True
            continue
        if in_table and line.startswith("#"):
            break
        if in_table and line.startswith("|") and not re.match(r"^\|\s*-", line):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            sid = re.split(r"[\s·]", cells[0].strip("`"))[0] if cells else ""
            key = next((k for k in re.split(r"[\s·`]+", cells[0]) if KEY.match(k)), None) if cells else None
            if len(cells) >= 5 and sid and sid.lower() != "session":
                rows[sid] = {"frs": cells[1], "stories": cells[2], "screens": cells[3], "flows": cells[4],
                             "key": key}
    return rows


def template_block(template, close=False):
    """The fenced block of the template's first full implementation session (one carrying every
    REQUIRED item), or with close=True of its first wave-close session."""
    for sid, _, _, body, _ in blocks(pathlib.Path(template).read_text()):
        if sid.startswith("close-") != close:
            continue
        if close or all(re.search(rx, body, re.M) for _, rx in REQUIRED):
            return body
    raise SystemExit(f"sessionize.py: no full {'close' if close else 'implementation'} block in {template}")


def set_branch(block, branch):
    return re.sub(r"Branch: \S+?(?=\.?(\s|$))", f"Branch: {branch}", block)


def render(ph, mapping, block, sets, step, branch):
    row = mapping.get(ph["id"], {})
    frs = row.get("frs") or compress(ph["frs"]) or "<FR range>"
    stories = row.get("stories") or (", ".join(sorted(ph["stories"], key=int)) or "<stories>")
    screens = [s.strip() for s in re.split(r",|<br>", row.get("screens", "")) if s.strip() and s.strip() != "—"]
    flows = [s.strip() for s in re.split(r",|<br>", row.get("flows", "")) if s.strip() and s.strip() != "—"]
    b = block.replace("specs/00N-<name>", f"specs/{ph['spec']}").replace("00N-<name>", ph["spec"])
    b = b.replace("FR-001–FR-0xx", frs)
    b = re.sub(r"^User stories: .*$", f"User stories: {stories}.", b, flags=re.M)
    b = b.replace("--spec 00N", f"--spec {ph['spec'][:3]}").replace("parity/00N", f"parity/{ph['spec'][:3]}")
    b = b.replace("check> 00N", f"check> {ph['spec'][:3]}")
    if screens:
        b = re.sub(r"(Screens this session ships.*?\n)(  - <screen-id>\n)+(  - <screen-id> — reduced.*?\n)?",
                   lambda m: m.group(1) + "".join(f"  - {s}\n" for s in screens), b, flags=re.S)
    if flows:
        b = re.sub(r"(E2E flows \(.*?\n)(  - 00N_.*?\n)+",
                   lambda m: m.group(1) + "".join(f"  - {f}\n" for f in flows), b, flags=re.S)
    tasks = ", ".join(t[0] for t in ph["tasks"])
    b = re.sub(r"(/speckit-implement\s+for\s+this\s+session's\s+phase\s+of\s+tasks\.md)",
               lambda m: f"{m.group(1)} ({tasks})", b)
    if row.get("key"):
        b = b.replace("<JIRA_KEY>-NN", row["key"])
    for k, v in sets.items():
        b = b.replace(k, v)
    b = set_branch(b, branch)
    deps = ", ".join(ph["deps"]) or "none"
    head = (f"### {step}. {ph['id']} — {ph['summary'] or '<what a person can do>'} (`{ph['spec']}`)"
            f" · {row.get('key') or '<JIRA_KEY>-NN'}")
    return finish(head, f"*Depends on: {deps}. Branch: `{branch}`. Epic: <EPIC>.*", b, sets)


def render_close(wave, deps, block, sets, step, branch, key):
    b = set_branch(block.replace("<JIRA_KEY>-NN", key), branch)
    head = f"### {step}. close-{wave} — Close {wave} · {key}"
    return finish(head, f"*Depends on: {', '.join(deps) or 'none'}. Branch: `{branch}`. Epic: <EPIC>.*", b, sets)


def finish(head, meta, body, sets):
    for k, v in sets.items():
        head, meta, body = head.replace(k, v), meta.replace(k, v), body.replace(k, v)
    return f"{head}\n\n{meta}\n\n```\n{body}\n```\n"


def blocks(text):
    """[(id, heading, meta, fenced body, key)] for every session heading outside fences: an old
    "### <ID> · summary [· KEY]" or a named "### <step>. <name> — summary [· KEY]"."""
    out, lines, fence = [], text.splitlines(), False
    for i, line in enumerate(lines):
        if line.startswith("```"):
            fence = not fence
            continue
        m = HEAD.match(line)
        named = NAMED.match(m.group(1)) if m else None
        if fence or not m or (" · " not in m.group(1) and not named):
            continue
        parts = [p.strip() for p in m.group(1).split(" · ")]
        key = parts[-1] if (len(parts) > 2 or named) and KEY.match(parts[-1]) else None
        meta, body, j = "", None, i + 1
        while j < len(lines) and not lines[j].startswith("### ") and not lines[j].startswith("## "):
            if not meta and lines[j].strip().startswith("*") and "Depends on" in lines[j]:
                meta = lines[j]
            if lines[j].startswith("```") and body is None:
                k = j + 1
                while k < len(lines) and not lines[k].startswith("```"):
                    k += 1
                body = "\n".join(lines[j + 1:k])
                j = k
            j += 1
        out.append((named.group(1) if named else parts[0].strip("`"), line, meta, body or "", key))
    return out


def validate(text, strict=False):
    errors, warnings = [], []
    bl = blocks(text)
    if not bl:
        return ["no session blocks found"], []
    if "## Definition of done" not in text:
        errors.append("missing the full 'Definition of done' section")
    if "parity reviewer" not in text.lower() and "verification reviewer" not in text.lower():
        errors.append("missing the reviewer prompt (The parity reviewer)")
    ids = [b[0] for b in bl]
    for d in sorted({i for i in ids if ids.count(i) > 1}):
        errors.append(f"duplicate session id {d}")
    for sid, head, meta, body, _ in bl:
        if not meta:
            errors.append(f"{sid}: no '*Depends on: … Branch: … Epic: …*' line under the heading")
        dm = re.search(r"Depends on:\s*([^.]*)", meta)
        for dep in ([x.strip().strip("`") for x in dm.group(1).split(",")] if dm else []):
            if dep and dep.lower() not in ("none", "—", "-") and dep not in ids:
                errors.append(f"{sid}: depends on unknown session {dep}")
        if not body.strip():
            errors.append(f"{sid}: no fenced prompt block")
            continue
        required = CLOSE_REQUIRED if "close" in sid.lower() else REQUIRED
        missing = [label for label, rx in required if not re.search(rx, body, re.M)]
        if missing:
            errors.append(f"{sid}: not self-contained, missing {', '.join(missing)}")
        if re.search(r"\bsee above\b|\bas above\b", body, re.I):
            errors.append(f"{sid}: says 'see above'; a block pasted alone must carry everything")
        holes = sorted(set(re.findall(r"<[A-Za-z][^<>\n]{0,40}>", body)))
        if holes:
            (errors if strict else warnings).append(f"{sid}: {len(holes)} placeholders left, e.g. {', '.join(holes[:4])}")
    return errors, warnings


def status(sessions_text, task_files, mapping, use_jira):
    keys = {sid: key for sid, _, _, _, key in blocks(sessions_text)}
    known = set(keys)
    for sid, key in mapping.items():
        if sid in known and not keys.get(sid):
            keys[sid] = key
    phases = [ph for f in task_files for ph in parse_tasks(f)]
    jira = None
    if use_jira:
        sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
        import jira as jira_mod  # noqa: E402
        jira = jira_mod
    rows, drift = [], []
    for ph in phases:
        done = sum(1 for t in ph["tasks"] if t[1])
        total = len(ph["tasks"])
        key = keys.get(ph["id"])
        state = "—"
        if jira and key:
            code, res = jira.api(f"/rest/api/2/issue/{key}?fields=status")
            state = res["fields"]["status"]["name"] if code == 200 else f"error {code}"
        rows.append((ph["id"], ph["spec"], f"{done}/{total}", key or "no key", state))
        if ph["id"] not in known:
            drift.append(f"{ph['id']}: a tasks.md phase with no SESSIONS.md block ({ph['file']})")
        if not key:
            drift.append(f"{ph['id']}: no ticket key (heading or map)")
        if jira and key:
            if total and done == total and state.lower() != "done":
                drift.append(f"{ph['id']}: every task is ticked but {key} is '{state}'")
            if state.lower() == "done" and done < total:
                drift.append(f"{ph['id']}: {key} is Done with {total - done} unticked tasks")
            if state.lower() in ("backlog", "selected for development", "to do") and done:
                drift.append(f"{ph['id']}: {done} tasks ticked but {key} is '{state}'")
    for sid in sorted(known - {ph["id"] for ph in phases}):
        if "close" not in sid.lower():
            drift.append(f"{sid}: a SESSIONS.md block with no tasks.md phase")
    return rows, drift


WAVE_NO = re.compile(r"^(?:wave[\s\-]*|w)?(\d+)$", re.I)


def sections(text):
    """[{title, sessions}] for every "## " section (outside fences) that holds session blocks. Each
    session: {step, name, key, summary, depends_on, parallel_with, branch, close}. The meta lines
    (Depends on, Branch, Parallel with) are read from everything between the heading and the
    prompt's fence, so a meta line wrapped over two lines still parses."""
    out, chunk, title, fence = [], [], None, False

    def flush():
        if title is None:
            return
        body = "\n".join(chunk)
        found = []
        for sid, head, _, _, key in blocks(body):
            lines = body.splitlines()
            i = lines.index(head) + 1
            meta = []
            while i < len(lines) and not lines[i].startswith(("```", "### ", "## ")):
                meta.append(lines[i].strip())
                i += 1
            meta = " ".join(meta)
            step = re.match(r"^###\s+(\d+)\.", head)
            summary = re.match(r"^###\s+(?:\d+\.\s+)?`?[^\s`]+`?\s+[—·]\s+(.*?)(?:\s+·\s+[A-Z][A-Z0-9]+-\d+)?$", head)
            branch = re.search(r"Branch:\s*`?(wave/[^`\s*]+?)`?\.?(?:[\s*]|$)", meta)
            found.append({
                "step": int(step.group(1)) if step else None, "name": sid, "key": key,
                "summary": summary.group(1) if summary else "",
                "depends_on": _names(re.search(r"Depends on:\s*([^.]*)", meta)),
                "parallel_with": _names(re.search(r"Parallel with:\s*([^.]*)", meta)),
                "branch": branch.group(1) if branch else None, "close": sid.startswith("close-")})
        if found:
            out.append({"title": title, "sessions": found})

    for line in text.splitlines():
        if line.startswith("```"):
            fence = not fence
        if not fence and line.startswith("## "):
            flush()
            title, chunk = line[3:].strip(), []
            continue
        chunk.append(line)
    flush()
    return out


def _names(m):
    return [x.strip().strip("`") for x in m.group(1).split(",")
            if x.strip() and x.strip().lower() not in ("none", "nothing", "—", "-")] if m else []


def find_wave(secs, arg):
    """(index, error): the section a wave argument names."""
    a = arg.strip()
    def branches(sec):
        return {s["branch"] for s in sec["sessions"] if s["branch"]}
    m = WAVE_NO.match(a)
    if m:
        n = int(m.group(1))
        hits = [i for i, s in enumerate(secs) if re.match(rf"^Wave\s+{n}\b", s["title"], re.I)]
        if not hits and n == 0 and secs:
            hits = [0]
        return (hits[0], None) if hits else (None, f"no 'Wave {n}' section")
    tiers = [
        [i for i, s in enumerate(secs) if a in branches(s)],
        [i for i, s in enumerate(secs) if re.search(rf"\b{re.escape(a)}", s["title"], re.I)],
        [i for i, s in enumerate(secs) if any(re.search(rf"[/\-]{re.escape(a)}(?:-|$)", b, re.I) for b in branches(s))],
        [i for i, s in enumerate(secs) if any(x["name"] == a for x in s["sessions"])],
    ]
    for hits in tiers:
        if len(hits) == 1:
            return hits[0], None
        if len(hits) > 1:
            return None, f"'{a}' matches several waves: " + "; ".join(secs[i]["title"] for i in hits)
    return None, f"no wave matches '{a}'"


def dependency_order(sessions):
    """Names in dependency order within the wave (ties by step order); dependencies outside the
    wave are ignored here. Raises ValueError on a cycle."""
    names = [s["name"] for s in sessions]
    deps = {s["name"]: [d for d in s["depends_on"] if d in names] for s in sessions}
    order, left = [], list(names)
    while left:
        ready = [n for n in left if all(d in order for d in deps[n])]
        if not ready:
            raise ValueError(f"dependency cycle among {', '.join(left)}")
        order.append(ready[0])
        left.remove(ready[0])
    return order


def wave(sessions_text, arg, task_files=()):
    secs = sections(sessions_text)
    i, err = find_wave(secs, arg)
    if err:
        listing = "; ".join(f"{n}: {s['title']}" for n, s in enumerate(secs))
        raise LookupError(f"{err}. Waves (by position): {listing}")
    sec = secs[i]
    by = {s["name"]: s for s in sec["sessions"]}
    tasks = {}
    for f in task_files:
        for ph in parse_tasks(f):
            t = tasks.setdefault(ph["id"], [0, 0])
            t[0] += sum(1 for x in ph["tasks"] if x[1])
            t[1] += len(ph["tasks"])
    out = []
    for name in dependency_order(sec["sessions"]):
        s = dict(by[name])
        s["after"] = [d for d in s["depends_on"] if d not in by]
        if task_files:
            s["tasks"] = "{}/{}".format(*tasks[name]) if name in tasks else None
        out.append(s)
    branches = list(dict.fromkeys(s["branch"] for s in sec["sessions"] if s["branch"]))
    number = re.match(r"^Wave\s+(\d+)\b", sec["title"], re.I)
    return {"title": sec["title"], "position": i, "number": int(number.group(1)) if number else None,
            "branch": branches[0] if branches else None, "branches": branches,
            "close": [s["name"] for s in out if s["close"]], "sessions": out}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("generate")
    g.add_argument("tasks", nargs="+")
    g.add_argument("--template", default=str(pathlib.Path(__file__).resolve().parent.parent / "templates" / "SESSIONS.md"))
    g.add_argument("--wave", default="wave-1", help="the wave's kebab-case name (close-<wave>, its branch)")
    g.add_argument("--close-key", default="<JIRA_KEY>-NN", help="the close session's ticket key (names the branch)")
    g.add_argument("--first-step", type=int, default=1, help="the step number of the first generated block")
    g.add_argument("--set", action="append", default=[], help='"<PLACEHOLDER>=value" (repeatable)')
    g.add_argument("--out")
    v = sub.add_parser("validate")
    v.add_argument("sessions")
    v.add_argument("--strict", action="store_true")
    s = sub.add_parser("status")
    s.add_argument("tasks", nargs="+")
    s.add_argument("--sessions", required=True)
    s.add_argument("--map", default="docs/delivery/jira-map.json")
    s.add_argument("--jira", action="store_true", help="read ticket status from Jira (needs .env)")
    w = sub.add_parser("wave")
    w.add_argument("wave", help="0/foundation, N (Wave N), a title word, the branch, or a session name")
    w.add_argument("--tasks", nargs="*", default=[], help="tasks.md files, to add ticked/total per session")
    w.add_argument("--sessions", default="SESSIONS.md")
    a = ap.parse_args(argv)

    if a.cmd == "wave":
        try:
            res = wave(pathlib.Path(a.sessions).read_text(), a.wave, a.tasks)
        except (LookupError, ValueError) as e:
            print(f"sessionize.py: {e}", file=sys.stderr)
            return 1
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return 0

    if a.cmd == "generate":
        sets = dict(x.split("=", 1) for x in a.set if "=" in x)
        block = template_block(a.template)
        branch = f"wave/{a.close_key}-{a.wave}"
        out, ids = [], []
        for f in a.tasks:
            phases = parse_tasks(f)
            if not phases:
                print(f"sessionize.py: no 'Phase n — <name> · <KEY>: <summary>' headings in {f}", file=sys.stderr)
            mapping = plan_mapping(pathlib.Path(f).parent)
            for ph in phases:
                if ph["id"] in ids:
                    print(f"sessionize.py: duplicate session id {ph['id']} in {f}", file=sys.stderr)
                    return 1
                ids.append(ph["id"])
                out.append(render(ph, mapping, block, sets, a.first_step + len(out), branch))
        if not out:
            return 1
        out.append(render_close(a.wave, ids, template_block(a.template, close=True),
                                sets, a.first_step + len(out), branch, a.close_key))
        text = "\n".join(out)
        if a.out:
            pathlib.Path(a.out).write_text(text)
            print(f"wrote {len(out)} session blocks to {a.out}; paste them into SESSIONS.md under their wave, "
                  "then run: sessionize.py validate SESSIONS.md")
        else:
            sys.stdout.write(text)
        return 0

    if a.cmd == "validate":
        errors, warnings = validate(pathlib.Path(a.sessions).read_text(), a.strict)
        for w in warnings:
            print(f"warning: {w}")
        for e in errors:
            print(f"error: {e}")
        n = len(blocks(pathlib.Path(a.sessions).read_text()))
        print(f"{n} blocks, {len(errors)} errors, {len(warnings)} warnings")
        return 1 if errors else 0

    mp = pathlib.Path(a.map)
    mapping = json.loads(mp.read_text()) if mp.is_file() else {}
    rows, drift = status(pathlib.Path(a.sessions).read_text(), a.tasks, mapping, a.jira)
    w = max([12] + [len(r[0]) for r in rows])
    print(f"{'Session':<{w}} {'Spec':<28} {'Tasks':<7} {'Key':<12} Status")
    for r in rows:
        print(f"{r[0]:<{w}} {r[1]:<28} {r[2]:<7} {r[3]:<12} {r[4]}")
    print("\nDrift:" if drift else "\nDrift: none")
    for d in drift:
        print(f"  - {d}")
    return 1 if drift else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # jira.JiraError and file errors: a clean message, no traceback
        if type(e).__name__ in ("JiraError", "FileNotFoundError"):
            print(f"sessionize.py: {e}", file=sys.stderr)
            sys.exit(2)
        raise
