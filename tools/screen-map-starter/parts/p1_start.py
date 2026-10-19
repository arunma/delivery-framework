"""Part 1 · Starting. Every part follows this shape: a SCREENS list of kit.Screen."""
from kit import FACTS, PRODUCT, Screen, e, page, primary

P = 'Starting'

SIGN_IN = page(
    '<div class="content full">'
    f'<div class="title" style="padding-top:120px">{e(PRODUCT)}</div>'
    '<p class="meta" style="padding:0 16px 24px">Sign in to continue.</p>'
    f'<div class="field">{e(FACTS["email"])}</div>'
    '<div style="height:12px"></div>'
    + primary('Continue')
    + '<div style="height:8px"></div><div class="btn t">Create an account</div>'
    '</div>')

SCREENS = [
    Screen('01-sign-in', P, 'Sign in', 'One field and one button; the same steps create an account.',
           SIGN_IN,
           reached_from=[('App launch, signed out', None), ('Sign out', None)],
           goes_to=[('Continue', '02-home'), ('Create an account', '02')],
           before='01-sign-in'),
]
