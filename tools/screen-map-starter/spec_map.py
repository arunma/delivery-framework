"""Which specification owns each screen. The screen map groups by this; specs cite these screen ids."""
import re

SPECS = [  # number, slug, title
    ('001', 'sign-in', 'Sign in'),
    ('002', 'home', 'Home'),
    ('003', 'item-detail', 'Item detail'),
]
NAME = {n: f'{n}-{slug}' for n, slug, _ in SPECS}
TITLE = {n: t for n, _, t in SPECS}

# First matching rule wins. Patterns match the screen id.
RULES = [
    (r'^01-', '001'),
    (r'^02-', '002'),
    (r'^S-0[1-2]', '003'),
]


def spec_of(sid):
    for pat, n in RULES:
        if re.match(pat, sid):
            return n
    raise KeyError(f'no spec owns screen {sid!r}; add a rule to spec_map.RULES')
