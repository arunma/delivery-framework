# Brief for planning a specification (plan + tasks)

<!-- Guidance: lives at docs/delivery/PLAN-BRIEF.md. One agent per spec, in parallel. The
parallel-safety rules are the point: agents that share files or switch branches overwrite each
other's work. -->

You are producing the implementation plan and tasks for **one** spec, `specs/NNN-name/`, grounded in
the real code. Other agents are planning other specs at the same time in the same working tree.

## Parallel safety (non-negotiable)
1. Write **only** inside `specs/NNN-name/`: `plan.md`, `research.md`, `data-model.md`,
   `contracts/`, `quickstart.md`, `tasks.md`, and `plan-discrepancies.md`.
2. **Never edit a shared file**: `docs/delivery/*`, `SESSIONS.md`, `TRACEABILITY.md`, the
   constitution, `.specify/feature.json`, the atlas, other specs, or `spec.md` itself. Spec problems
   go to your `plan-discrepancies.md`; the main session merges them.
3. **Run no setup script** that creates or switches branches or writes shared state (spec-kit's
   `create-new-feature`, `setup-plan`, `check-prerequisites` with writes). Follow the
   `/speckit.plan`, `/speckit.tasks` and `/speckit.analyze` templates, but write the files directly.
4. Read code; change none. No `git` command that changes state.

## Read first
`CLAUDE.md`, the constitution, `DECISIONS.md`, your `spec.md` and checklist, the atlas screens it
owns, `BACKEND-SPLIT.md`, `SESSIONS.md` (the sessions that build this spec and their order), and the
`plan.md` of every spec yours depends on, if it exists. Use `graphify query` / `explain` / `path` to
find the code before reading files (run `graphify update .` first if the graph is stale). For every
existing symbol the plan changes, list `graphify affected "<symbol>"` in the plan, confirmed with grep
or the language server (call edges can be incomplete, e.g. widget construction in Dart).

## plan.md
- Header: branch per session (`feat/<JIRA_KEY>-NN-slug`), date, spec link, Input (FR and story
  counts).
- **Summary grounded in code**: what exists today, at `path:line`; what changes; which other specs'
  providers or modules this composes.
- Technical context.
- **Constitution Check** — a table, one row per principle, saying how this plan satisfies it. The
  gate: the non-negotiables pass, and a UI plan cites its atlas screen ids.
- Project structure (docs and source tree).
- **Session mapping**: Session · Jira | FRs | Stories | Screens shipped | E2E flows. Say what
  depends on what, and what this spec closes for others.
- Not in this plan. Complexity tracking (item, why needed, simpler alternative rejected because).
- Post-design constitution re-check.
- Diagrams: Mermaid for every new state machine, sync or handshake sequence, and module dependency
  the plan introduces.
- **Analysis pass** (`/speckit.analyze` style): a table of ID | Category | Severity | Location |
  Finding | Resolution, then a coverage line (FRs with ≥ 1 task, SCs, tasks, unmapped tasks).

## research.md, data-model.md, contracts/, quickstart.md
Each research item: Decision, Why, Rejected (with the evidence). The data model separates what is
read (owned elsewhere) from what is owned here. Contracts include *reduced screens*: full form
versus this build's fallback, and what the person sees. The quickstart says how to see it working,
on staging only with synthetic accounts.

## tasks.md
- One phase per session, in `SESSIONS.md` order. Each phase opens with **Start**
  (`jira.py start`, the GAPS IN list), then **Tests first (must fail before implementation)**, then
  **Implementation**, then **Close** (the Definition of done in order: tests and coverage → E2E flows
  with captures → build and run → parity round with a fresh reviewer → simpler-way review → lint →
  `HANDOFF.md` and `jira.py done`/`comment` → stage and ask).
- Format: `- [ ] T001 [P] [US1] Description with exact file paths`.
- End with **FR → task coverage** (every FR, including lettered ones) and success-criterion
  coverage. No FR without a task; no task without an FR, story or DoD step.

## plan-discrepancies.md
Spec problems found while planning, in the DISCREPANCIES format (`D-NNN-n`, both quotes, options,
recommendation, what the plan builds meanwhile, Status: Open).

Return ≤10 lines: files written, FR coverage (n/n), task count, sessions, discrepancies raised (ids),
any CRITICAL analysis finding.
