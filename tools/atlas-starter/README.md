# Atlas starter kit

A small, runnable skeleton of the mockup atlas generator (framework phase 4). Mockups are HTML built
from one kit, rendered to PNG at device size, and gathered into an atlas page that shows every
screen with its id, purpose, where it is reached from, where each control goes, and its backend
dependency. The atlas is the UI contract: specs cite its screen ids.

## Files

| File | What it does |
| --- | --- |
| `kit.py` | The only styling and component source: tokens (CSS variables), system fonts, device size, components, built-in icons, `Screen`, and the one **seed** block (`OWNER`, `TODAY`, `ITEMS`, `FACTS`). |
| `parts/p*.py` | One file per area of the app. Each exports `SCREENS`, a list of `kit.Screen`. `p2_home.py` is the reference shape. |
| `spec_map.py` | Which spec owns each screen id (`RULES`, first match wins). A screen no spec owns fails the build. |
| `backend_map.py` | `BACKEND` (screen → backend items), `ITEMS` (item → fallback, sessions, `later`), `REDUCED` (full screen → reduced stand-in). |
| `render_parts.py` | Renders every part to `out/html/<id>.html` and `out/png/<id>.png` with Playwright. |
| `build_atlas.py` | Writes `out/atlas/index.html` (every screen) and `out/atlas/this-build.html` (deferred screens removed, reduced stand-ins swapped in). |
| `build_backend_split.py` | Generates `out/BACKEND-SPLIT.md` from the maps: client-only, reduced, deferred, critical. |
| `backup.py` | Tars the atlas source into `out/backups/<timestamp>.tar.gz`. |

Put "before" screenshots in `before/<name>.png` and set `before='<name>'` on a `Screen` to show
today's screen beside the proposal.

## Commands

```bash
uv sync
uv run playwright install chromium   # once per machine
uv run backup.py                     # before every change
uv run render_parts.py [part ...]    # e.g. uv run render_parts.py p2_home
uv run build_atlas.py [--strict]     # --strict also fails on links to undrawn screens
uv run build_backend_split.py
open out/atlas/index.html
```

`build_atlas.py` exits non-zero on a duplicate id, an ambiguous link target (a prefix that matches
more than one id), a screen with no owning spec, or a backend item missing from `ITEMS`.

## Rules

- **The kit is the only styling source.** Parts use its classes and CSS variables; no colour
  literals, no new fonts. Inline `style=` for layout only.
- **Facts come from the seed block only.** Names, dates, counts and statuses are read from
  `kit.ITEMS` / `kit.FACTS`, never typed into a part, so every screen tells the same story and copy
  stays consistent. Change a fact once, in the kit. All seed data is synthetic.
- **Screen ids are stable.** Specs, tests and screenshots cite them. Redesigns keep the number of
  the "before" screen (`02-home`); new mockups take `S-NN-slug`; states of one screen add a letter
  (`S-01b-…`). Never reuse an id; link by full id when a prefix could match two screens.
- **Every tappable element appears in `goes_to`**, and every entry point in `reached_from`
  (`None` for system entry points such as a push notification).
- **Back up before every change** (`uv run backup.py`). Untracked files have no git history.
- **Open every PNG after rendering** and look at it: nothing clipped, overlapping, truncated or off
  the rules. A render that ran is not a render that is right.
