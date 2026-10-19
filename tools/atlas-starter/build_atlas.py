"""Build out/atlas/index.html (every screen) and out/atlas/this-build.html (what ships now).

    uv run build_atlas.py [--strict]        (after render_parts.py)

this-build.html drops screens that need a backend item with no fallback, and swaps each full screen
in backend_map.REDUCED for its reduced stand-in. The build FAILS (exit 1) on:
  - a duplicate screen id;
  - an ambiguous link target (a prefix matching more than one id: ids are colliding);
  - a screen no spec owns (spec_map.RULES);
  - a backend item used in BACKEND but missing from ITEMS;
  - with --strict, any link target that resolves to no screen (otherwise counted and printed).
"""
import html
import pathlib
import sys

from PIL import Image

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import kit  # noqa: E402
from backend_map import BACKEND, ITEMS, REDUCED  # noqa: E402
from render_parts import PNG, load  # noqa: E402
from spec_map import NAME, SPECS, TITLE, spec_of  # noqa: E402

OUT = HERE / 'out' / 'atlas'
IMG = OUT / 'img'
e = html.escape


def check(every):
    errors = []
    ids = [s.sid for s in every]
    errors += [f'duplicate id: {i}' for i in sorted({i for i in ids if ids.count(i) > 1})]
    for s in every:
        try:
            spec_of(s.sid)
        except KeyError as x:
            errors.append(str(x))
    errors += [f'backend item {i} (screen {sid}) is not in ITEMS'
               for sid, lst in BACKEND.items() for i, _ in lst if i not in ITEMS]
    errors += [f'REDUCED names unknown screen {x}' for pair in REDUCED.items() for x in pair if x not in ids]
    return errors


def resolver(all_ids):
    def resolve(t):
        """Exact id, else the one id starting with 't-', else the one id starting with 't'."""
        if t is None or t in all_ids:
            return t, None
        hits = [i for i in all_ids if i.startswith(t + '-')] or [i for i in all_ids if i.startswith(t)]
        if len(hits) > 1:
            return None, f'ambiguous target {t!r} matches {hits}'
        return (hits[0] if hits else False), None
    return resolve


def blocked(sid):
    return sid in BACKEND and not all(ITEMS[i]['fallback'] for i, _ in BACKEND[sid])


def badge(sid):
    be = BACKEND.get(sid)
    if not be:
        return '<div class="be ok"><b>Client only</b> Ships without backend changes.</div>'
    fb = all(ITEMS[i]['fallback'] for i, _ in be)
    lines = ''.join(f'<div><code>{e(i)}</code> {e(r)}'
                    + (f' <i>Fallback: {e(ITEMS[i]["fallback"])}</i>' if ITEMS[i]['fallback'] else '') + '</div>'
                    for i, r in be)
    return f'<div class="be {"fb" if fb else "no"}"><b>{"Ships reduced first" if fb else "Needs backend"}</b>{lines}</div>'


def jpg(sid):
    src = PNG / f'{sid}.png'
    if not src.exists():
        raise SystemExit(f'missing {src}: run render_parts.py first')
    im = Image.open(src).convert('RGB')
    im.thumbnail((804, 1748))
    im.save(IMG / f'{sid}.jpg', 'JPEG', quality=76, optimize=True)
    return f'img/{sid}.jpg'


CSS = """
:root{--bg:#FFFFFF;--fill:#F4F6F9;--fg:#121A26;--fg2:#46505F;--fg3:#5E6878;--line:#E3E7ED;--accent:#2058D6;--miss:#B83A0E;
 --ok-bg:#EAF6EF;--ok-fg:#14532D;--fb-bg:#FDF6E3;--fb-fg:#6B4A00;--no-bg:#FDF1EC;--no-fg:#7A2E0C}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0D1420;--fill:#151E2C;--fg:#E8EDF4;--fg2:#B0BAC8;
 --fg3:#8C97A8;--line:#222D3D;--accent:#86A9FF;--miss:#FF9D70;--ok-bg:#12291D;--ok-fg:#A7E3BD;--fb-bg:#2A2410;--fb-fg:#F0D58C;
 --no-bg:#2D1A12;--no-fg:#FFB596;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#0D1420;--fill:#151E2C;--fg:#E8EDF4;--fg2:#B0BAC8;--fg3:#8C97A8;--line:#222D3D;--accent:#86A9FF;
 --miss:#FF9D70;--ok-bg:#12291D;--ok-fg:#A7E3BD;--fb-bg:#2A2410;--fb-fg:#F0D58C;--no-bg:#2D1A12;--no-fg:#FFB596;color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.6 system-ui,-apple-system,sans-serif}
aside{position:fixed;top:0;bottom:0;left:0;width:240px;overflow:auto;border-right:1px solid var(--line);padding:24px 16px}
aside .np{font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--fg3);margin:18px 0 6px}
aside a{display:block;color:var(--fg2);text-decoration:none;font-size:13px;padding:3px 8px;border-radius:6px}
aside a:hover{background:var(--fill)}
aside a.nb::after{content:'●';color:var(--miss);font-size:9px;margin-left:6px}
aside a.nb.fb::after{color:#D99A00}
main{margin-left:240px;padding:40px 40px 120px;max-width:1100px}
h1{font-size:1.9rem;line-height:1.2;margin:0 0 10px} h2{margin:0} h3{margin:0 0 4px}
p{margin:0;color:var(--fg2);max-width:65ch}
a{color:var(--accent)}
.part{padding-top:64px;border-top:1px solid var(--line);margin-top:56px}
.screen{padding-top:44px}
code{font:12px ui-monospace,Menlo,monospace;color:var(--fg3)}
.grid{display:grid;grid-template-columns:minmax(0,1fr) 240px;gap:28px;margin-top:16px}
.figs{display:grid;grid-template-columns:repeat(auto-fill,minmax(0,280px));gap:20px}
figure{margin:0} figcaption{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--fg3);margin-bottom:8px}
figure img{width:100%;height:auto;border-radius:24px;border:1px solid var(--line)}
.links{list-style:none;margin:0 0 18px;padding:0;font-size:13px} .links li{padding:2px 0;color:var(--fg2)}
h4{font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--fg3);margin:0 0 6px}
.sys{font-size:11px;color:var(--fg3)} .miss{color:var(--miss)}
.be{margin-top:12px;border-radius:10px;padding:10px 14px;font-size:13px;max-width:72ch}
.be b{display:block} .be.ok b{display:inline;margin-right:6px}
.be.ok{background:var(--ok-bg);color:var(--ok-fg)} .be.fb{background:var(--fb-bg);color:var(--fb-fg)}
.be.no{background:var(--no-bg);color:var(--no-fg)}
body.hide-be .needs-be, body.hide-be aside a.nb{display:none}
.stats{display:flex;gap:28px;margin:18px 0} .stats b{display:block;font-size:1.5rem}
.menu{display:none}
@media (max-width:900px){aside{display:none} main{margin-left:0;padding:24px 16px 80px}
 .grid{grid-template-columns:1fr} .figs{grid-template-columns:minmax(0,1fr)} .menu{display:block}}
"""


def build(every, this_build, out_name, strict):
    all_ids = [s.sid for s in every]
    resolve = resolver(all_ids)
    deferred = {s.sid for s in every if blocked(s.sid)} if this_build else set()
    swap = dict(REDUCED) if this_build else {}
    stand_ins = set(REDUCED.values())
    screens = [s for s in every if s.sid not in deferred and s.sid not in swap]
    shown = {s.sid for s in screens}
    errors, missing = [], []

    def links(pairs, sid):
        out = []
        for label, t in pairs:
            r, err = resolve(t)
            if err:
                errors.append(f'{sid}: {err}')
                continue
            r = swap.get(r, r)
            if r is None:
                out.append(f'<li>{e(label)} <span class="sys">system</span></li>')
            elif r is False:
                missing.append((sid, label, t))
                out.append(f'<li>{e(label)} <span class="miss">→ {e(t)} (not drawn)</span></li>')
            elif r not in shown:
                out.append(f'<li>{e(label)} <span class="sys">deferred · needs backend</span></li>')
            else:
                out.append(f'<li><a href="#{r}">{e(label)}</a></li>')
        return '<ul class="links">' + ''.join(out) + '</ul>'

    groups = {}
    for s in screens:
        groups.setdefault(spec_of(s.sid), []).append(s)
    navh, body = [], []
    for n, _, _ in SPECS:
        if n not in groups:
            continue
        cls = lambda sid: (' class="nb fb"' if not blocked(sid) else ' class="nb"') if sid in BACKEND else ''  # noqa: E731
        navh.append(f'<div class="np">{n} · {e(TITLE[n])}</div>'
                    + ''.join(f'<a href="#{s.sid}"{cls(s.sid)}>{e(s.title)}</a>' for s in groups[n]))
        body.append(f'<section class="part" id="spec-{n}"><h2>{n} · {e(TITLE[n])}</h2>'
                    f'<p>{len(groups[n])} screen{"s" if len(groups[n]) != 1 else ""} · <code>specs/{e(NAME[n])}/spec.md</code></p></section>')
        for s in groups[n]:
            figs = ''
            before = HERE / 'before' / f'{s.before}.png' if s.before else None
            if before and before.exists():
                im = Image.open(before).convert('RGB')
                im.thumbnail((804, 1748))
                im.save(IMG / f'before-{s.before}.jpg', 'JPEG', quality=76)
                figs += f'<figure><figcaption>Today</figcaption><img src="img/before-{e(s.before)}.jpg" alt="Today: {e(s.title)}" loading="lazy"></figure>'
            src = jpg(s.sid)
            figs += (f'<figure><figcaption>{"Proposed" if s.before else "New"}</figcaption>'
                     f'<a href="{src}" target="_blank"><img src="{src}" alt="{e(s.title)}" loading="lazy"></a></figure>')
            tag = ' <span class="sys">reduced stand-in</span>' if s.sid in stand_ins else ''
            body.append(
                f'<section class="screen{" needs-be" if s.sid in BACKEND else ""}" id="{s.sid}"><code>{e(s.sid)}</code>{tag}'
                f'<h3>{e(s.title)}</h3><p>{e(s.purpose)}</p>{badge(s.sid)}<div class="grid"><div class="figs">{figs}</div>'
                f'<div><h4>Reached from</h4>{links(s.reached_from, s.sid)}<h4>Goes to</h4>{links(s.goes_to, s.sid)}</div></div></section>')

    other = ('index.html', 'See every screen →') if this_build else ('this-build.html', 'See only this build →')
    head = 'This build: what ships with today’s backend' if this_build else 'Every screen, and how you get there'
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(kit.PRODUCT)} Atlas</title><style>{CSS}</style></head>
<body><aside><b>{e(kit.PRODUCT)} · atlas</b>{''.join(navh)}</aside><main>
<h1>{head}</h1><p>Each screen with its id, purpose, where it is reached from and where each control goes.
All data is synthetic. {f'{len(deferred)} screens are deferred; {len(swap)} are replaced by their reduced form.' if this_build else ''}</p>
<div class="stats"><div><b>{len(screens)}</b>screens</div><div><b>{len(groups)}</b>specs</div><div><b>{len(missing)}</b>links not drawn</div></div>
<label><input type="checkbox" onchange="document.body.classList.toggle('hide-be',this.checked)"> Show only client-only screens</label>
<p style="margin-top:10px"><a href="{other[0]}">{other[1]}</a></p>
<div class="menu">{''.join(f'<a href="#spec-{n}" style="margin-right:12px">{n}</a>' for n in groups)}</div>
{''.join(body)}</main></body></html>"""
    (OUT / out_name).write_text(page)
    for m in missing:
        print('  unresolved link', m)
    if strict and missing:
        errors.append(f'{len(missing)} unresolved links (--strict)')
    return len(screens), len(missing), errors


def main():
    strict = '--strict' in sys.argv
    every = load()
    errors = check(every)
    if errors:
        print('\n'.join('ERROR ' + x for x in errors))
        raise SystemExit(1)
    IMG.mkdir(parents=True, exist_ok=True)
    n1, m1, err1 = build(every, False, 'index.html', strict)
    n2, m2, err2 = build(every, True, 'this-build.html', strict)
    errors = sorted(set(err1 + err2))
    if errors:
        print('\n'.join('ERROR ' + x for x in errors))
        raise SystemExit(1)
    print(f'atlas: {n1} screens, this build: {n2}, unresolved links: {m1}; wrote {OUT}')


if __name__ == '__main__':
    main()
