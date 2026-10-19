# The steps

A plain reference to every step. [README.md](README.md) explains the idea and walks through two
examples; [CHECKLIST.md](CHECKLIST.md) has a short checklist per step. The detail of how each step is
done lives in its skill (`skills/<name>/SKILL.md`), its prompt ([prompts/](prompts/)) and its
template ([templates/](templates/)), so it is not repeated here.

Each step below says what it's for, what you run, what you get, and when it's done. Steps the
project's profile turns off are skipped; how much runs depends on the size of the work:

- **Small:** a ticket goes straight to a PR. Run `/delivery:session <TICKET-KEY>`; steps 0 and 13 only.
- **Medium:** a short spec and plan first: steps 0, 9, 10, 12 and 13.
- **Large:** the full flow below.

(In `profile.json` and the skills, size is `tier` S, M or L, and "what you're building" is
`surface`.)

## What changes with what you're building

The rule is the same everywhere: the contract says what "done" looks like, and someone who did not
build the result checks it against the contract.

| What you're building | The contract | How the result is checked |
| --- | --- | --- |
| App (mobile, web, desktop) | Clickable mockups of every screen (the "atlas") | Screenshots of the built app beside the mockups |
| API or service | OpenAPI, AsyncAPI or protobuf, plus sequence diagrams | Contract tests and a contract diff |
| Data pipeline | Data contract, plus a golden dataset with its expected output (the answer key) | Output equals the answer key; quality checks; a second run matches |
| Library or CLI | Every public command and function, with runnable examples | Examples run as tests; golden output; semver check |
| Infrastructure | Diagram plus the infrastructure-as-code plan | Plan diff and policy checks (plan only, never apply, in a pilot) |
| ML model | Eval set, answer key and a pass rule | Scores meet the rule on named hardware |

A project with several parts (an app with its own API) gets every row that applies. Templates:
[templates/contracts/](templates/contracts/). In the skills, the check is called "parity" for apps
and "verification" in general.

## Existing project or new project

| | Existing project (brownfield) | New project (greenfield) | Specs or docs already exist (adopt midway) |
| --- | --- | --- | --- |
| Start with | `/delivery:bootstrap-brownfield` | `/delivery:bootstrap-greenfield` | `/delivery:adopt-midway` |
| Step 2, capture today | Required | Skipped | Required for an app with no capture yet |
| Architecture | Written from the code, with file:line | A target design | Checked against the code |
| Specs | Cite today's code; `TRACEABILITY.md` maps every current feature to its new home | Cite research and decisions | Re-checked, not rewritten |

From step 4 on, every project runs the same steps.

## Who does what

| Who | Does | Never does |
| --- | --- | --- |
| **Owner** | Decides, answers questions, approves the contract, commits and merges | Lets the agent decide a product question |
| **Engineer** | Runs one session per fresh context, reads each report, checks each step is done | Accepts "done" without pasted output |
| **Agent** | Writes the documents, code and tests; moves its own ticket; records every disagreement | Commits, pushes, edits the spec it is building, touches production or real data |
| **Reviewer agent** | Checks work it did not write | Reads the diff it is judging, or fixes anything |

---

## 0 · Assess

- **For:** knowing what kind of project this is before anything runs, so a data pipeline is never
  asked for mockups.
- **Run:** `/delivery:start [brownfield|greenfield|adopt-midway] [S|M|L]` (skills `assess`, `tiering`).
- **You get:** `.delivery/profile.json` and `.delivery/PROFILE.md` (what you're building, existing or
  new, size, risks, and every step below marked on, off or swapped), and `.delivery/guards.json`,
  which turns the guard hooks on.
- **Done when:** the owner has confirmed what you're building, the size and the risks.

## 0 · Bootstrap and 1 · Setup

- **For:** a repo every agent session can start from, with the same rules and traps.
- **Run:** `/delivery:bootstrap-brownfield`, `/delivery:bootstrap-greenfield` or `/delivery:adopt-midway`.
- **You get:** `CLAUDE.md` and `AGENTS.md` (rules, and every trap already hit with its fix), a draft
  `ARCHITECTURE.md`, open questions and discrepancies, the tracker project and a gitignored `.env`.
  Existing projects also get the code graph; new projects get the stack decision and a scaffold.
- **Done when:** the owner has read the report and answered or deferred every question.

## 2 · Capture today (existing projects)

- **For:** a record of today's behaviour, so nothing is lost by accident.
- **Run:** `/delivery:capture-before`.
- **You get:** screenshots of every current screen (apps), or a baseline for other projects
  (recorded API responses, today's pipeline output, golden CLI output, today's plan, baseline scores).
  Staging and synthetic data only.
- **Done when:** every capture was opened and checked, and unreachable ones are listed with a reason.

## 3 · Research and 4 · Contract

- **For:** writing down what "done" looks like before writing specs.
- **Run:** `/delivery:atlas` for an app; `/delivery:contract <api|data|cli|infra|ml>` otherwise.
- **You get:** a short research note, independent design reviews, and the contract: clickable
  mockups of every screen in `design/atlas/`, or files in `contracts/`.
- **Done when:** the contract builds or validates with no errors, every id is unique, and the owner
  has approved it in writing in `DECISIONS.md`.

## 5 · Decisions

- **For:** one place where the owner's word is final, and every open question has a recommendation.
- **Run:** `/delivery:decisions`.
- **You get:** `docs/delivery/DECISIONS.md` (wins over every other document), `OPEN-QUESTIONS.md`,
  `GLOSSARY.md` (one concept, one name) and `DISCREPANCIES.md` (every disagreement, never resolved
  silently).
- **Done when:** every question has a recommendation and says what it blocks, and every answer is
  applied to the contract.

## 6 · Backend split (when a client depends on a backend)

- **For:** knowing which features ship on today's backend, which ship reduced, and which wait.
- **Run:** `/delivery:backend-split`.
- **You get:** `BACKEND-AUDIT.md` with file:line evidence, and `BACKEND-SPLIT.md` classifying each
  backend item as ships reduced, deferred or critical.
- **Done when:** every item is classified and the critical list is empty or approved by the owner.

## 7 · Constitution

- **For:** a short list of principles that every plan is checked against.
- **Run:** `/delivery:constitution`.
- **You get:** `.specify/memory/constitution.md`, versioned.
- **Done when:** the owner chose the non-negotiables and `CLAUDE.md` cites the same version.

## 8 · Architecture

- **For:** how the pieces fit, and where each spec lives in the code.
- **Run:** `/delivery:architecture`.
- **You get:** `ARCHITECTURE.md` with Mermaid diagrams; claims marked verified (with file:line),
  proposed or unverified.
- **Done when:** every verified claim has a file:line, conflicts are in `DISCREPANCIES.md`, and the
  diagrams compile.

## 9 · Specs

- **For:** one testable spec per feature, citing the contract ids it builds.
- **Run:** `/delivery:specify-from-atlas`, then `/delivery:verify-specs`.
- **You get:** `specs/NNN-name/spec.md` with stories, numbered requirements (FRs), a test plan and
  flow diagrams; `docs/delivery/SPEC-VERIFICATION.md`.
- **Done when:** every contract id is covered, every reference resolves, and nothing needs
  clarification. Never renumber a requirement: withdraw it and leave the gap.

## 10 · Plans and tasks

- **For:** a plan per spec grounded in the real code, with tasks grouped by session.
- **Run:** `/delivery:plan-and-tasks` (one planning agent per spec, in parallel).
- **You get:** `plan.md` and `tasks.md` in each spec folder; spec problems merged into
  `DISCREPANCIES.md`.
- **Done when:** every requirement has a task and every plan passes the constitution check.

## 11 · Sessions

- **For:** a list of self-contained prompts, one per agent context, in dependency order.
- **Run:** `/delivery:sessionize`.
- **You get:** `SESSIONS.md`: the Definition of done, one block per session, grouped into batches
  (waves) with a close block after each.
- **Done when:** `sessionize.py validate SESSIONS.md --strict` passes and every requirement is in
  some session.

## 12 · Tracker

- **For:** Jira as the record of progress, kept current by each session.
- **Run:** `/delivery:jira-sync` (dry run first).
- **You get:** a ticket per session and per backend item, dependency links, `jira-map.json`, and a
  dashboard. Dashboard gadgets need pointing at their filters once by hand.
- **Done when:** every session heading and spec carries its ticket key.

## 13 · Run the sessions

- **For:** building one session's slice, proving it, and handing it to the owner staged.
- **Run:** `/delivery:session <ID>` in a fresh context; `/delivery:status` to see what is next.
- **You get:** code and tests written test-first, end-to-end runs (staging, synthetic data), an
  independent check against the contract (`design/parity/NNN.md` or `verification/NNN.md`), a report,
  and the work staged.
- **Done when:** the report has pasted test output, every check passed or is marked NOT RUN with a
  reason, the check file has no open rows, and the owner has committed.

## 14 · Close the batch

- **For:** knowing the real state after a batch of sessions, and turning each mistake into a rule.
- **Run:** `/delivery:close-wave <n>`.
- **You get:** every check re-run, a list of what is really not done, proposed fixes for open
  discrepancies, and proposed rules for `AGENTS.md`.
- **Done when:** every lesson is a rule, a template change, or "no rule needed", approved by the owner.

---

## Where things go in a project

Every skill, template and prompt uses these paths.

```
CLAUDE.md  AGENTS.md  ARCHITECTURE.md  SESSIONS.md  TRACEABILITY.md
.delivery/profile.json  PROFILE.md  guards.json   # step 0 output; hook settings
contracts/api/  contracts/data/  contracts/surface/  contracts/infra/  contracts/eval/  # non-app contracts
verification/NNN.md  verification/NNN/             # non-app checks and raw results
.specify/memory/constitution.md         # spec-kit reads it from here
.env                                    # gitignored: JIRA_SITE, JIRA_USER, JIRA_TOKEN
docs/delivery/
  DECISIONS.md  OPEN-QUESTIONS.md  GLOSSARY.md  DISCREPANCIES.md  BACKLOG.md
  BACKEND-AUDIT.md  SPEC-BRIEF.md  PLAN-BRIEF.md  SPEC-VERIFICATION.md
  JIRA.md  jira-map.json  backend-items.json
docs/diagrams/<name>.json (+ .html, .png)  # archify sources and renders
graphify-out/GRAPH_REPORT.md            # the only committed part of the code graph
.graphifyignore                         # from templates/graphifyignore
design/
  seed.md  research.md  review.md  design-review-N.md
  before/<screen-id>.png                # existing apps only
  atlas-src/                            # the mockup generator (from tools/atlas-starter)
  atlas/index.html  atlas/this-build.html
  BACKEND-SPLIT.md                      # generated from atlas-src/backend_map.py
  ui-review/NNN.md                      # one per spec
  app/<screen-id>.png                   # screenshots of the built app
  parity/NNN.md                         # one per spec
specs/NNN-name/                         # spec-kit feature folders
tools/jira.py  tools/create_tickets.py  tools/jira_dashboard.py
.maestro/                               # or the platform's E2E harness
```

Placeholders in templates and prompts: `<PROJECT>` (repo name), `<PRODUCT>` (the name users see),
`<JIRA_KEY>` (project key), `<EPIC>`, `<INITIATIVE>` (the label for this piece of work), `<STAGING>`
(the test environment), `<CAPTURE_SWITCH>` (the test-only build flag that allows screenshots).

## Tools

- **graphify** builds a queryable graph of the code (`graphify update .`; query before broad file
  reads). Call edges can be incomplete, so confirm callers with grep before changing shared code.
- **Mermaid** is the source of every diagram; compile with `mmdc`. **archify** makes polished
  versions for reviews ([templates/diagrams/README.md](templates/diagrams/README.md)).
- `tools/setup-tools.sh` installs graphify and archify globally; read it first.
- **spec-kit** writes specs, plans and tasks; **Jira** is the tracker.
