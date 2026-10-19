# Phase 4 · Mockup atlas

Copy `<framework>/tools/atlas-starter/` to `design/atlas-src/` first. The starter writes to
`out/`; point its output paths at `design/atlas/`, `design/png/` and `design/BACKEND-SPLIT.md`
(the paths at the top of each script). **Back up before every change**: `uv run backup.py`.

## 4a · Kit and reference part (one agent; it owns kit.py)

```
Build the mockup kit for <PRODUCT> in design/atlas-src/kit.py from the starter. Read
docs/delivery/DECISIONS.md (brand, fonts, palette), design/research.md and design/review.md first.
Back up first (uv run backup.py). Then:
  - Tokens as CSS variables only; measure contrast (WCAG 2.2 AA) and note the ratios in a comment.
  - Components the review calls for (nav, rows, buttons, status as a word plus a dot, sheets,
    dialogs, confirm, snackbar, empty state, tabs), plus a reserved-icon list (one meaning per icon).
  - ONE facts block: owner, today's date, the synthetic items with their attributes (dates, counts,
    states), organisations, codes. Every screen will read facts from here. Nothing is ever inlined.
  - A reference part, parts/p2_<area>.py, with 3–5 screens, each a Screen(sid, part, title, purpose,
    html, reached_from, goes_to, before=<before id or None>).
Render (uv run render_parts.py) and open every PNG. Build (uv run build_atlas.py) and fix every
unresolved link. Write design/atlas-src/PART-BRIEF.md (prompt 4b, filled in with the id ranges
taken by each part). Commit nothing.
```

## 4b · Part author brief (one agent per part, in parallel)

Write this to `design/atlas-src/PART-BRIEF.md`, then give each agent: "Draw part N (<area>), screens
<list>. Follow design/atlas-src/PART-BRIEF.md. Edit only parts/pN_<area>.py."

```
You are drawing one part of the <PRODUCT> mockup atlas. Read, in this order:
1. design/atlas-src/kit.py — the ONLY styling and component source. Do not edit it. If you need a
   small helper, define it in your part file. No new colours: use the CSS variables. Inline style=
   for layout only.
2. design/atlas-src/parts/p2_<area>.py — the reference part. Copy its shape exactly.
3. design/design-review-<N>.md: the findings and missing states for your screens; design/review.md.
4. docs/delivery/DECISIONS.md, docs/delivery/GLOSSARY.md, and the spec(s) for your area if they
   exist, so copy, states and rules match.
5. design/before/ for the screens you redesign (brownfield).
Rules:
  - Product name <PRODUCT>; never the internal name in copy. Every fact (names, dates, counts,
    organisations) comes from kit's facts block. Never invent one that contradicts it.
  - <Owner's visual rules from DECISIONS.md: one primary button per screen, status as word + dot, …>
  - Ids: redesigns keep the before id ('07-item-actions') and set before=; new screens 'S-nn-slug';
    states of one screen 'S-nna-…', 'S-nnb-…'. Ids already taken by other parts: <list>. Link to
    them; don't redraw them. A new id must not be a prefix of, or share a prefix with, another id's
    number (the atlas resolves links by prefix and fails on ambiguity).
  - reached_from / goes_to: (label, target id or number prefix, or None for system entry points).
    Every tappable element on your screen appears in goes_to.
  - Every state on your list (empty, loading, error, confirm, undo) gets its own screen.
Done means: uv run render_parts.py pN_<area>, then open EVERY PNG you produced and look at it. Fix
anything clipped, overlapping, truncated mid-word or inconsistent; render again. Then run
uv run build_atlas.py and fix any failure or unresolved link in your part. Report: the screen ids
written, the link targets you used that no part owns, anything you could not apply and why.
```

## 4c · Fix round (after a design review)

```
Round <N>: apply design/design-review-<N>.md to your part. Read it (search for every one of your
screen ids) and design/atlas-src/PART-BRIEF.md again. Back up first (uv run backup.py). Then edit
ONLY your part file so that:
1. Every seed fact comes from kit's facts block (no inline dates, counts, names or colours).
2. Every fix in the review that names one of your screens is applied, including the new states. If a
   fix conflicts with an owner rule, the owner rule wins; say so in your report.
3. Existing screen ids stay stable (other parts link to them). New ids follow the conventions, and
   every goes_to target resolves.
Render, open EVERY PNG, fix, re-render until clean; then run build_atlas.py. Report: fixes applied
(by number), fixes not applied and why, new ids.
```

## 4d · Design review round

Use prompt 3c with a fresh reviewer, on `design/atlas/index.html`.

## 4e · Atlas check (any agent, after every round)

```
In design/atlas-src: uv run backup.py, then uv run render_parts.py, uv run build_atlas.py --strict,
uv run build_backend_split.py. Report the summary lines: screen counts (all / this build),
duplicate ids, ambiguous prefixes, unowned screens, unresolved links (each with its source screen),
and the backend split counts. Then open 5 PNGs at random and say whether any fact differs from
kit's facts block. Change nothing else.
```
