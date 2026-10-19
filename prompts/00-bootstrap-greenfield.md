# Bootstrap — greenfield (an empty or new repo)

Paste the fenced block into a **fresh agent session** in the new repo. The owner should be present:
the session starts with an interview. It ends at a gate with a report.

**Phases for greenfield.** Skipped: 2 (capture the before). Phase 3 replaces the current-UI review
with competitors and the owner's sketches. Optional: `TRACEABILITY.md` (use it to map the
interview's needs to specs). The backend audit becomes a target inventory.

```
You are bootstrapping the delivery framework on a new project: <PROJECT>. The framework is at <path
to delivery-framework>; read its README.md and FRAMEWORK.md (phases 0–8) first. You commit nothing.

## Step 1 — Interview the owner (ask, wait, record)
Ask these in small groups (no more than five questions at a time). Record each answer, verbatim and
dated, in docs/delivery/DECISIONS.md as D0.n. Do not guess an answer; mark it "to decide" and move it
to OPEN-QUESTIONS.md with your recommendation.
  1. Product: what it does, for whom, the one job it must do well; what it must never do.
  2. Users: who, how many, how technical; accessibility needs; languages and locales.
  3. Platforms: mobile (iOS/Android), web, desktop (which OS), CLI; offline needs.
  4. Constraints: deadlines, team size, devices to support, performance budgets.
  5. Data sensitivity: personal data, regulated data, where data may live, encryption, retention.
  6. Backend: none, existing (which), or new; auth provider; third parties.
  7. Budget and licences: hosting budget, paid services, licence rules (e.g. permissive only).
  8. Tracker: Jira site and project key, epics, labels; who owns the token.
  9. Brand and design: name, existing palette or design system, fonts, references they like.

## Step 2 — Choose the stack (research, options, recommendation)
For each choice that matters (language/framework, state, storage, backend, auth, E2E tool, CI),
research current options. Use subagents and cite sources with access dates. Give two or three
options with tradeoffs, then a recommendation. Check licences against the owner's rule. Write it as
docs/delivery/DECISIONS.md D1 "Stack — proposed", and ask the owner to confirm. Do not scaffold
before the owner answers.

## Step 3 — Scaffold (after the owner confirms the stack)
- CLAUDE.md and AGENTS.md from the framework's templates (fill in what is known; §0 starts with the
  traps you hit while scaffolding).
- .specify/ with spec-kit installed (its templates and scripts); .specify/memory/constitution.md
  drafted from templates/constitution.md, with product principles from the interview, not ratified.
- Lint, formatter, analyzer, a test runner with a coverage gate, CI running them, pre-commit hooks.
- The E2E harness chosen in Step 2, with one smoke flow, a wrapper that passes credentials explicitly
  and refuses non-synthetic accounts (see tools/maestro/ for the pattern), and a test-only capture
  switch if the platform blocks screenshots.
- .env handling: .env in .gitignore, .env.example with empty JIRA_SITE/JIRA_USER/JIRA_TOKEN, and
  any app config with a staging/production split.
- Synthetic fixtures: a generator with a fixed seed, no real data, ever.
- tools/: jira.py, create_tickets.py, jira_dashboard.py, setup-tools.sh from the framework.
- design/atlas-src/ copied from tools/atlas-starter; check that `uv run render_parts.py` and
  `uv run build_atlas.py` run.
Run lint, tests and the E2E smoke flow, and paste the output.

## Step 4 — Architecture as a target design
Write ARCHITECTURE.md from templates/ARCHITECTURE.md as a target. Mark every claim [P] (proposed).
Mermaid for context, containers, the main flows and deployment, each compiled with `mmdc`. Put the
risks and the open decisions in §11 and in OPEN-QUESTIONS.md.

## Step 5 — Tracker
Check `python3 tools/jira.py show <JIRA_KEY>-1` works (never print the token). Propose the epics and
the initiative label; create nothing until the owner agrees.

## Gate — stop here and report (≤ 40 lines)
1. Interview: answered / to decide (ids).
2. Stack: the recommendation, the alternatives, and the owner's answer (or "waiting").
3. Scaffold: what exists; lint, test, E2E smoke output (pasted, short).
4. Constitution: the principles proposed; the questions for the owner.
5. ARCHITECTURE.md: sections, diagrams compiled.
6. Tracker status.
7. Next: phase 3 (research and sketches) → phase 4 (the atlas, drawn from research and sketches).
Commit nothing. List the files you created, and ask.
```
