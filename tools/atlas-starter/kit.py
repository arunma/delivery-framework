"""The kit: the ONLY styling and component source for the mockups.

Every part in parts/ builds HTML with these helpers. Rules:
  * Colours come from the CSS variables below. Never write a colour literal in a part.
  * Seed facts (owner, dates, items, counts) come from the SEED block at the bottom. A part never
    invents or retypes a fact, so every screen tells the same story.
  * Status is a word plus a dot, never colour alone. One filled primary button per screen at most.
"""
import html

e = html.escape

PRODUCT = 'Example'          # the user-facing product name; replace with <PROJECT>'s
DEVICE = (402, 874)          # logical points, iPhone 16 Pro-class. Change per project.
SCALE = 3                    # device pixel ratio for the PNGs

CSS = r"""
:root{--bg:#FFFFFF;--fill:#F4F6F9;--line:#E3E7ED;--ink:#121A26;--ink2:#46505F;--ink3:#5E6878;
 --action:#2058D6;--ok:#1C7C47;--warn:#8A5A00;--error:#B83A0E;--ai:#6346D9;--scrim:rgba(18,26,38,.42)}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:402px;height:874px;overflow:hidden;background:var(--bg)}
body{font-family:-apple-system,BlinkMacSystemFont,'SF Pro Text',Roboto,system-ui,sans-serif;color:var(--ink);
 font-size:16px;line-height:24px;-webkit-font-smoothing:antialiased}
.phone{position:relative;width:402px;height:874px;overflow:hidden}
.sb{position:absolute;top:0;left:0;right:0;height:54px;display:flex;align-items:center;justify-content:space-between;
 padding:6px 32px 0 48px;font-weight:600;font-size:17px}
.hi{position:absolute;bottom:8px;left:0;right:0;margin:0 auto;width:139px;height:5px;border-radius:3px;background:var(--ink)}
.content{position:absolute;top:54px;left:0;right:0;bottom:84px;overflow:hidden}
.content.full{bottom:0}
.nav{height:48px;display:flex;align-items:center;padding:0 8px;position:relative}
.nav .back{display:flex;align-items:center;gap:2px;color:var(--action)}
.nav .ttl{position:absolute;left:70px;right:70px;text-align:center;font-weight:500;font-size:17px;
 white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.title{font-size:26px;line-height:32px;font-weight:600;padding:8px 16px 4px}
.meta{font-size:14px;line-height:20px;color:var(--ink3)}
.sec{display:flex;justify-content:space-between;align-items:baseline;padding:20px 16px 6px}
.sec b{font-size:14px;font-weight:500;color:var(--ink3)}
.row{display:flex;align-items:center;gap:12px;min-height:60px;padding:8px 16px;border-bottom:1px solid var(--line)}
.row .t{flex:1;min-width:0} .row .t div:first-child{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ic{width:22px;height:22px;flex:none;color:var(--ink2)}
.btn{display:flex;align-items:center;justify-content:center;height:50px;border-radius:12px;font-weight:600;margin:0 16px}
.btn.p{background:var(--action);color:#fff} .btn.t{color:var(--action)} .btn.d{color:var(--error)}
.dot{display:inline-flex;align-items:center;gap:6px;font-size:14px}
.dot::before{content:'';width:8px;height:8px;border-radius:4px;background:currentColor}
.row.error .ic{color:var(--error)}
.ok{color:var(--ok)} .warn{color:var(--warn)} .error{color:var(--error)}
.field{margin:8px 16px;height:50px;border:1px solid var(--ink3);border-radius:12px;padding:0 14px;display:flex;align-items:center;color:var(--ink3)}
.tabs{position:absolute;bottom:0;left:0;right:0;height:84px;border-top:1px solid var(--line);display:flex;padding-top:8px;background:var(--bg)}
.tabs div{flex:1;display:flex;flex-direction:column;align-items:center;font-size:11px;color:var(--ink3)}
.tabs .on{color:var(--action)}
.scrim{position:absolute;inset:0;background:var(--scrim);display:flex;align-items:center;justify-content:center}
.dialog{width:300px;background:var(--bg);border-radius:16px;padding:20px 0 8px;text-align:center}
.dialog h3{font-size:17px;font-weight:600;padding:0 20px} .dialog p{font-size:14px;color:var(--ink2);padding:6px 20px 12px}
.dialog .btn{margin:0;border-top:1px solid var(--line);border-radius:0;height:46px}
.empty{text-align:center;padding:96px 32px;color:var(--ink2)} .empty b{display:block;color:var(--ink);font-size:18px;margin:12px 0 4px}
.banner{margin:12px 16px;padding:12px 14px;border-radius:12px;background:var(--fill);font-size:14px;color:var(--ink2)}
"""

# Built-in outline icons (24x24 paths), so rendering needs no network. Add what a project needs.
ICONS = {
    'home': '<path d="M3 10l9-7 9 7v10a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/>',
    'list': '<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>',
    'user': '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    'file': '<path d="M14 3H6a1 1 0 0 0-1 1v16a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8z"/><path d="M14 3v5h5"/>',
    'chevron': '<path d="M9 6l6 6-6 6"/>',
    'back': '<path d="M15 6l-6 6 6 6"/>',
    'search': '<circle cx="11" cy="11" r="7"/><path d="M21 21l-5-5"/>',
    'plus': '<path d="M12 5v14M5 12h14"/>',
    'trash': '<path d="M4 7h16M10 11v6M14 11v6M6 7l1 13h10l1-13M9 7V4h6v3"/>',
}


def icon(name, cls='ic'):
    if name not in ICONS:
        raise KeyError(f'no icon {name!r}; add it to kit.ICONS')
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" '
            f'stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>')


def status_bar():
    return '<div class="sb"><span>9:41</span><span>●●● ▮</span></div>'


def nav(back=None, title=''):
    """Pushed-screen bar. Back labels over 14 characters become 'Back'."""
    b = ''
    if back:
        b = f'<span class="back">{icon("back")}{e(back if len(back) <= 14 else "Back")}</span>'
    return f'<div class="nav">{b}<span class="ttl">{e(title)}</span></div>'


def row(title, sub='', tail='', ic='file', cls=''):
    s = f'<div class="meta">{sub}</div>' if sub else ''
    return f'<div class="row {cls}">{icon(ic)}<div class="t"><div>{e(title)}</div>{s}</div>{tail}</div>'


def primary(label):
    return f'<div class="btn p">{e(label)}</div>'


def status(kind, word):
    """Status is a word plus a dot. kind: ok | warn | error."""
    return f'<span class="dot {kind}">{e(word)}</span>'


def tabs(active):
    t = [('Home', 'home'), ('Items', 'list'), ('You', 'user')]
    return '<div class="tabs">' + ''.join(
        f'<div class="{"on" if n == active else ""}">{icon(i)}{n}</div>' for n, i in t) + '</div>'


def confirm(title, text, verb, cancel='Cancel'):
    """Destructive confirm: red text verb and Cancel, never a filled red button."""
    return (f'<div class="scrim"><div class="dialog"><h3>{e(title)}</h3><p>{e(text)}</p>'
            f'<div class="btn d">{e(verb)}</div><div class="btn t">{e(cancel)}</div></div></div>')


def empty(title, text):
    return f'<div class="empty">{icon("file")}<b>{e(title)}</b>{e(text)}</div>'


def page(body):
    w, h = DEVICE
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width={w}">'
            f'<style>{CSS}</style></head><body><div class="phone">{status_bar()}{body}<div class="hi"></div></div></body></html>')


class Screen:
    """A mockup and its place in the atlas. reached_from / goes_to: [(label, id | id prefix | None)]."""
    def __init__(self, sid, part, title, purpose, html_, reached_from, goes_to, before=None):
        self.sid, self.part, self.title, self.purpose = sid, part, title, purpose
        self.html, self.reached_from, self.goes_to, self.before = html_, reached_from, goes_to, before


# ---------------------------------------------------------------- SEED: the one source of facts
# Screens read facts from here and never inline them. Change a fact here and every screen agrees.
# All synthetic: no real people, organisations, numbers or documents.
OWNER = 'Alex Example'
TODAY = '13 Oct 2026'
ITEMS = [  # name, status kind, status word, detail
    ('Item one', 'ok', 'Up to date', 'Updated 12 Oct 2026'),
    ('Item two', 'warn', 'Due in 5 days', 'Due 18 Oct 2026'),
    ('Item three', 'error', 'Overdue', 'Was due 2 Oct 2026'),
    ('Item four', 'ok', 'Up to date', 'Updated 1 Oct 2026'),
]
FACTS = dict(total=len(ITEMS), shared_with='sam@example.com', email='alex@example.com')
