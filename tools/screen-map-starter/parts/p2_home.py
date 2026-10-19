"""Part 2 · Home and item detail. Reference part: copy this shape.

Ids: redesigned screens keep the number of the 'before' screenshot ('02-home'); new mockups use the
review's S-number then a slug ('S-01-item-detail'); states of one S-number add a letter ('S-01b-…').
"""
from kit import FACTS, ITEMS, OWNER, Screen, confirm, icon, nav, page, primary, row, status, tabs

P = 'Home'

first = ITEMS[1]  # the item the detail screens show; read from the seed, never retyped


def home():
    rows = ''.join(row(n, status(k, w), icon('chevron')) for n, k, w, _ in ITEMS)
    return page(
        '<div class="content">'
        f'<div class="title">Hello, {OWNER.split()[0]}</div>'
        f'<div class="sec"><b>Your items</b><span class="meta">{FACTS["total"]}</span></div>'
        f'{rows}</div>' + tabs('Home'))


def detail(reduced=False):
    name, kind, word, when = first
    shared = ('<div class="banner">Sharing shows once the server supports it.</div>' if reduced
              else row('Shared with', FACTS['shared_with'], icon('chevron'), ic='user'))
    return page(
        '<div class="content full">' + nav('Home', name)
        + f'<div class="title">{name}</div><div style="padding:0 16px 16px">{status(kind, word)}'
        + f'<div class="meta">{when}</div></div>'
        + primary('Mark done') + '<div style="height:16px"></div>' + shared
        + row('Delete', '', '', ic='trash', cls='error') + '</div>')


def delete_confirm():
    return page('<div class="content full">' + nav('Home', first[0]) + '</div>'
                + confirm(f'Delete {first[0]}?', 'This cannot be undone.', 'Delete'))


SCREENS = [
    Screen('02-home', P, 'Home', 'Everything that needs you, in one list.', home(),
           reached_from=[('Sign in', '01-sign-in'), ('Home tab', None)],
           goes_to=[(f'{ITEMS[1][0]} row', 'S-01-item-detail'), ('Items tab', None), ('You tab', None)],
           before='02-home'),
    Screen('S-01-item-detail', P, 'Item', 'One item: its status, one action, who it is shared with.', detail(),
           reached_from=[('Home row', '02-home')],
           goes_to=[('Back', '02-home'), ('Mark done', '02-home'), ('Delete', 'S-02')]),
    Screen('S-01b-item-detail-reduced', P, 'Item (reduced)',
           'The item without server sharing: the sharing row becomes a note.', detail(reduced=True),
           reached_from=[('Home row', '02-home')],
           goes_to=[('Back', '02-home'), ('Mark done', '02-home'), ('Delete', 'S-02')]),
    Screen('S-02-delete-confirm', P, 'Delete?', 'Destructive confirm names what is lost.', delete_confirm(),
           reached_from=[('Delete', 'S-01-item-detail')],
           goes_to=[('Delete', '02-home'), ('Cancel', 'S-01-item-detail')]),
]
