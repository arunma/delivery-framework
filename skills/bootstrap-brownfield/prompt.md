# Bootstrap — brownfield (an existing codebase)

Paste the fenced block into a **fresh agent session at the repo root**. Fill in the `<…>` first. It
ends at a gate with a report; it implements no product change.

**Phases for brownfield.** Mandatory: 2 (capture the before), `TRACEABILITY.md` (phase 9), and the
backend audit (phase 6), which grounds the backend split in the existing code. Optional: the
interview parts of greenfield.

**Before pasting:** run `tools/setup-tools.sh` once on this machine (graphify, archify). Have the
owner ready to answer questions at the end.

```
You are bootstrapping the delivery framework on an existing codebase: <PROJECT>, shipped to users as
<PRODUCT>. The framework is at <path to delivery-framework>; read its README.md and FRAMEWORK.md
(phases 0–8) first. You change no product code in this session. You commit nothing.

## Step 0 — Back up before touching anything
List untracked and modified files (`git status --porcelain`). Copy every untracked document
(markdown, specs/, design/, mockups) to <backup dir outside the repo>/<date>/, preserving paths, and
print the path. Agents have overwritten untracked specs with no backup before; that is what this step
prevents.

## Step 1 — Build the code graph, then survey with subagents
1. Build the code graph (graphify must be installed; if not, say so and continue without it):
   copy <framework>/templates/graphifyignore to .graphifyignore and adapt it to this stack (secrets,
   generated code, mocks, build output, design artefacts); add `graphify-out/*` and
   `!graphify-out/GRAPH_REPORT.md` to .gitignore; run `graphify update .` (local, no AI calls). Read
   graphify-out/GRAPH_REPORT.md. From here on, query the graph (`graphify query "…"`,
   `graphify path "A" "B"`, `graphify explain "X"`, `graphify affected "X"`) before broad file reads.
   Call edges can be incomplete for some languages (e.g. widget construction in Dart): confirm any
   "no callers" result with grep or the language server. Record the graph rules in CLAUDE.md §4.
2. Run parallel subagents, each returning a short report with file:line evidence, over:
   a. Stack and versions, build system, package manager, flavors/environments/config
      (dev/staging/prod), and how to run the app.
   b. Modules and layers; the main data flows; state management; navigation.
   c. Tests: kinds, locations, how they run, coverage today, golden tests, E2E harness and how it
      gets credentials.
   d. CI, lint, analyzers, pre-commit hooks, release process.
   e. Existing docs and conventions: README, CLAUDE.md, AGENTS.md, docs/, ADRs, contributing
      guides, branch and commit conventions, issue tracker references.
   f. Security-sensitive paths: auth, crypto, secrets handling, screen protection, storage,
      logging of personal data, anything that must not be refactored casually.
   g. The backend(s) the app talks to: endpoints used (client side), and where their code lives.

## Step 2 — Find the traps
Find what will trip an agent: build or run variants that fail silently (a flavor with an empty key,
an env check that throws before the app starts); protections that hide the app from test runners
(screen protection hiding the accessibility tree); test tools that ignore exported variables;
generated code that must be regenerated; identifiers a test can or cannot see; a product name that
differs from the repo name. Run the commands to confirm each one. Write each as: symptom, cause, fix.

## Step 3 — Instructions files
Write CLAUDE.md and AGENTS.md from the framework's templates/CLAUDE.md and templates/AGENTS.md.
**Keep every existing instruction**: merge existing CLAUDE.md/AGENTS.md content in. Move long
reference material to docs/AGENTS.md rather than deleting it. List anything you would drop and ask.
§0 holds the traps from Step 2. §1 holds a placeholder summary of the proposed constitution (Step 7).
§4 and §5 hold real commands, each verified by running it.

## Step 4 — Issue tracking
Copy the framework's tools/jira.py, create_tickets.py and jira_dashboard.py into tools/. Check that
.env is gitignored (`git check-ignore .env`). If JIRA_SITE/JIRA_USER/JIRA_TOKEN are present, run
`python3 tools/jira.py show <JIRA_KEY>-1`; never print the token. Write the conventions (key in
branch, commit subject and code comments; no markdown TODO lists) into CLAUDE.md §3. Do not create
tickets yet.

## Step 5 — Capture the before (if the owner has given a staging account)
Follow the framework's skills/capture-before/prompt.md: synthetic seed (never real data), staging
only, a synthetic account, an E2E capture flow, a test-only capture switch if the app blocks
screenshots (a no-op in production, with a test). Open every screenshot and look at it. If there is
no staging account yet, write the plan and the owner task instead.

## Step 6 — Architecture draft and docs-versus-code discrepancies
Write ARCHITECTURE.md from templates/ARCHITECTURE.md, from the code: module map, dependencies and
hot spots from GRAPH_REPORT.md, each claim marked [V] with file:line, or [?]. Mermaid for the
context, the main flows (sequence) and any state machine, each compiled with `mmdc`. Every place
where existing docs disagree with the code goes to docs/delivery/DISCREPANCIES.md (templates/
DISCREPANCIES.md format).

## Step 7 — Propose the constitution
Draft .specify/memory/constitution.md from templates/constitution.md. Propose the product-specific
principles you can infer from the code and docs (what the product promises its users). Keep the
framework principles. Mark which you propose as NON-NEGOTIABLE. Do not ratify: ask the owner, one
question per principle that is a real choice.

## Step 8 — Open questions
Write docs/delivery/OPEN-QUESTIONS.md: every question you could not answer from the code, each with
a recommendation and what it blocks.

## Gate — stop here and report (≤ 40 lines)
1. Backup path.
2. Graph built (yes/no; node and edge counts), .graphifyignore written, and the three biggest hot
   spots it shows.
3. Stack, environments and how to run and test, as verified commands.
4. The traps (§0), one line each.
5. Instructions: what you merged, what you would drop (waiting for the owner).
6. Tracker: status of .env and jira.py.
7. Before capture: done (count, path) or the owner task.
8. ARCHITECTURE.md: sections written, count of [V] vs [?]; discrepancies raised (ids).
9. Constitution: the principles proposed, and the questions for the owner.
10. Open questions (ids).
11. Phases next: 2 (if not done), 3, then 4. Mandatory for brownfield: 2, TRACEABILITY.md (phase 9)
    and the backend audit (phase 6).
Commit nothing. List the files you created or changed, and ask.
```
