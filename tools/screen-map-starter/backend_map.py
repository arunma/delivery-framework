"""Which screens need backend work, and the client fallback that lets them ship without it.

BACKEND: screen id -> [(item id, reason)]. A screen not listed ships with today's backend.
ITEMS:   item id -> title, where, status, fallback (None = no fallback), sessions, later.
         An item with no fallback that is not `later` is CRITICAL: the build cannot ship without it.
REDUCED: full screen -> the reduced screen drawn to stand in for it in this build.
"""
BACKEND = {
    'S-01-item-detail': [('B1', '"Shared with" needs the share list endpoint')],
    'S-02-delete-confirm': [('B2', 'Server-side delete with audit')],
}

ITEMS = {
    'B1': dict(title='Share list per item', where='api', status='missing',
               fallback='Hide the sharing row and show a note', sessions=['sharing-row'], later=False),
    'B2': dict(title='Audited delete', where='api', status='missing',
               fallback=None, sessions=['delete-audit'], later=True),
}

REDUCED = {'S-01-item-detail': 'S-01b-item-detail-reduced'}
