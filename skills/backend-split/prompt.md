# Phase 6 · Backend audit and split

## 6a · Backend audit (read-only)

```
Audit the backend for <PRODUCT>'s <initiative>. Read-only: local checkouts only, fetch nothing,
change nothing. Repos: <list with paths>. Record each repo's commit and date.
For every screen in design/screen-map-src/backend_map.py BACKEND (and every server call the specs or
ARCHITECTURE.md assume), find what already exists. Cite repo/path:line. Use `graphify query`,
`graphify path` and `graphify explain` on each repo's graph before broad reads. Write
docs/delivery/BACKEND-AUDIT.md (<framework>/templates/BACKEND-AUDIT.md):
  - What exists (no change needed), with evidence.
  - Client-side bugs found on the way (what the client sends vs what the server reads).
  - Each item: needed by, today, the minimal change, the client fallback (or none, and why), a
    classification (ships reduced / deferred / critical), risks.
  - Prerequisites the lists missed (bugs, missing cascades, security gaps).
  - Sequencing and open questions (each with a recommendation).
Never claim "exists" without a citation; mark unverified claims [?]. Report: items by
classification, critical items with reasons, new prerequisites, client bugs.
```

Greenfield: the same prompt produces a target inventory. Every item's status is "to build", and the
fallback question decides what the first build needs.

## 6b · Backend split

```
Update design/screen-map-src/backend_map.py from docs/delivery/BACKEND-AUDIT.md: BACKEND (screen → [(item,
reason)]), ITEMS (item → title, where, status, fallback or None, sessions, later), REDUCED (full
screen → the reduced stand-in drawn for this build). Draw each reduced stand-in the screen map needs (part
brief rules). Back up first. Run uv run build_screen_map.py and uv run build_backend_split.py. Then add a
"Fallbacks in detail" section (full form, this build, what the person sees, how it switches) for each
item with a fallback to design/BACKEND-SPLIT.md, or, better, to the generator. Report: counts
(client-only, reduced, deferred, critical), and each critical item with its reason for the owner.
```
