"""Generate out/BACKEND-SPLIT.md from backend_map.py and the screens. Regenerate; never edit by hand.

    uv run build_backend_split.py
"""
import datetime
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from backend_map import BACKEND, ITEMS, REDUCED  # noqa: E402
from render_parts import load  # noqa: E402


def main():
    ids = [s.sid for s in load()]
    stand_ins = set(REDUCED.values())
    by_item = {}
    for sid, lst in BACKEND.items():
        for i, _ in lst:
            by_item.setdefault(i, []).append(sid)
    client = [i for i in ids if i not in BACKEND]
    reduced = [i for i in ids if i in BACKEND and all(ITEMS[x]['fallback'] for x, _ in BACKEND[i])]
    deferred = [i for i in ids if i in BACKEND and i not in reduced]
    critical = [i for i, v in ITEMS.items() if not v['fallback'] and not v.get('later')]

    out = [f'# Backend split\n\n*Generated {datetime.date.today()} by `build_backend_split.py` from `backend_map.py` — '
           'regenerate, don\'t edit.*\n',
           f'**Counts:** {len(ids)} screens. {len(client)} client-only, {len(reduced)} ship reduced with a client '
           f'fallback, {len(deferred)} deferred (no fallback). {len(stand_ins)} reduced stand-ins drawn.\n',
           '**Critical items:** ' + (', '.join(f'`{c}` ({ITEMS[c]["title"]})' for c in critical) if critical else 'none')
           + '. A critical item has no fallback and is needed by this build; say why for each.\n',
           f'## 1. Client-only ({len(client)})\n', ', '.join(f'`{i}`' for i in client) + '\n',
           '## 2. By backend item\n',
           '| Item | Status | Fallback in this build | Screens | Sessions |', '|---|---|---|---|---|']
    for i, v in ITEMS.items():
        fb = v['fallback'] or ('none — later build' if v.get('later') else '**none — critical**')
        out.append(f'| **{i}** {v["title"]} | {v["where"]} · {v["status"]} | {fb} | '
                   f'{", ".join(f"`{s}`" for s in by_item.get(i, [])) or "—"} | {", ".join(v.get("sessions", [])) or "—"} |')
    out += ['', f'## 3. Deferred: no fallback ({len(deferred)})\n', ', '.join(f'`{i}`' for i in deferred) or 'none', '',
            '## 4. Reduced stand-ins\n'] + [f'- `{a}` → `{b}`' for a, b in REDUCED.items()]
    path = HERE / 'out' / 'BACKEND-SPLIT.md'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('\n'.join(out) + '\n')
    print(f'wrote {path}: {len(client)} client-only, {len(reduced)} reduced, {len(deferred)} deferred, '
          f'{len(critical)} critical')


if __name__ == '__main__':
    main()
