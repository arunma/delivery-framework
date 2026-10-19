"""Render every part to out/html/<id>.html and out/png/<id>.png at device size.

    uv run render_parts.py [part_module ...]     e.g. uv run render_parts.py p2_home

Then open every PNG it writes and look at it.
"""
import importlib
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
HTML, PNG = HERE / 'out' / 'html', HERE / 'out' / 'png'
sys.path.insert(0, str(HERE))


def load(names=None):
    mods = names or sorted(p.stem for p in (HERE / 'parts').glob('p*.py'))
    screens = []
    for m in mods:
        screens += importlib.import_module(f'parts.{m}').SCREENS
    return screens


def main(names):
    from playwright.sync_api import sync_playwright

    import kit
    HTML.mkdir(parents=True, exist_ok=True)
    PNG.mkdir(parents=True, exist_ok=True)
    w, h = kit.DEVICE
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=kit.SCALE)
        for s in load(names):
            f = HTML / f'{s.sid}.html'
            f.write_text(s.html)
            pg.goto(f.as_uri())
            pg.wait_for_load_state('networkidle')
            pg.screenshot(path=str(PNG / f'{s.sid}.png'))
            print(s.sid)
        b.close()


if __name__ == '__main__':
    main(sys.argv[1:] or None)
