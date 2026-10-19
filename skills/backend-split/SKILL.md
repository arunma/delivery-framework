---
name: backend-split
description: Phase 6 - audit the backend with file:line evidence and classify every backend item a client needs as ships reduced (with a client fallback), deferred, or critical, keeping the backend change to the minimum; regenerates BACKEND-SPLIT.md. Use when a UI or client depends on a backend, when the profile's backend-split phase is on, or when someone asks what can ship on today's backend.
---

# Backend split and audit

Plugin root: `${CLAUDE_PLUGIN_ROOT}`. Read `${CLAUDE_PLUGIN_ROOT}/reference/CONVENTIONS.md` first and
check the profile (phase `backend-split`; on only when a client depends on a backend).

1. Read [prompt.md](prompt.md) and run it.
2. Delegate the audit to the `backend-auditor` agent, once per backend repo (in parallel when there
   are several). It is read-only and returns findings with `repo/path:line`; you write
   `docs/delivery/BACKEND-AUDIT.md` from `${CLAUDE_PLUGIN_ROOT}/templates/BACKEND-AUDIT.md` with the
   commit read for each repo.
3. UI projects: update `design/screen-map-src/backend_map.py` (`BACKEND`, `ITEMS`, `REDUCED`) and
   regenerate with `uv run build_backend_split.py`; never hand-edit `design/BACKEND-SPLIT.md`.
   Other clients (a CLI, a pipeline reading a service): keep the same table by hand in
   `docs/delivery/BACKEND-SPLIT.md` from `${CLAUDE_PLUGIN_ROOT}/templates/BACKEND-SPLIT.md`.
4. Classify each item as exactly one of: **ships reduced** (a client fallback with a stated reduced
   behaviour), **deferred** (no fallback, not needed now), **critical** (no fallback and this build
   cannot ship without it; name the reason). Aim for no critical items.
5. Write `docs/delivery/backend-items.json` for `jira-sync` (format in `tools/create_tickets.py`).

Gate (CHECKLIST.md §6): every "already exists" claim has a file:line; every item is classified; the
critical list is empty or approved by the owner. Report, stage, ask.
