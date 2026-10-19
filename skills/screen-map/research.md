# Phase 3 · Research and review

## 3a · Research best practice

```
Research current (last 18 months) practice for <product category> on <platforms>: <3–6 comparable
products>, plus the platform guidelines (Apple HIG, Material 3, WCAG 2.2) on navigation, search,
sheets, empty states, and — if the product uses AI — suggestion patterns that keep a person in
control. Use subagents. Cite every claim with a URL and access date; mark what you could not verify.
Keep only principles that change a screen. Write design/research.md, at most two pages: a short
matrix, then 12–15 principles, each with "Seen in" and "For <PRODUCT>". Commit nothing.
```

## 3b · Review the current UI (brownfield)

```
Review today's UI from design/before/*.png. Read CLAUDE.md, the constitution draft, design/research.md
and the current inventory (or build one: every route, screen, sheet, action, setting and flag, with
file paths). For each screenshot write 3–5 findings in design/review.md: what is confusing,
cluttered, duplicated or missing. Tie each to a principle or Nielsen heuristic and to the file that
renders it. Score each screen 1–5 for clarity, focus and findability. End with the ten changes that
matter most, ranked, and the features that must not be lost (keep, merge or drop each, with the
reason). Treat earlier briefs as proposals, not truth; where you disagree, say so under "Changes I'd
make to the brief". Commit nothing.
```

Greenfield: replace 3b with walkthroughs of 2–3 comparable products (screenshots from public material
only) and the owner's sketches, using the same findings format.

## 3c · Independent design review (fresh reviewer; also used for screen map rounds)

```
You are an independent design reviewer for <PRODUCT>. You did not draw these screens. Read
CLAUDE.md, docs/delivery/DECISIONS.md, docs/delivery/GLOSSARY.md and design/research.md, then open
every screen in design/screen-map/index.html (or design/before/ for a current-UI review). Write
design/design-review-<N>.md:
  1. Global findings: consistency of tokens, type, icons, spacing, button hierarchy, copy voice.
  2. Per screen (by id): 1–3 findings, each with a severity (High/Med/Low), the rule it violates, and
     the fix as an instruction a part author can apply.
  3. Navigation: dead ends, missing back paths, links to screens not drawn.
  4. Missing states: empty, loading, error, offline, confirm, undo — listed as new screen ids
     (S-nn-slug).
  5. Seed consistency: any fact (date, count, name) that differs between screens.
  6. The top ten fixes, numbered so a fix brief can cite them.
Be concrete. No praise. Do not edit anything.
```
