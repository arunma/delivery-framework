# <PRODUCT> (<PROJECT>) — project instructions

<!-- Guidance: loaded automatically in every Claude Code session. Keep it under ~150 lines; move
reference material to docs/AGENTS.md. Every line should prevent a mistake. Delete these comments
once filled in. -->

Loaded automatically in every session. The global `~/.claude/CLAUDE.md` still applies; this adds
what is specific to this project. **If these conflict with a generic instinct, these win.**

<One paragraph: what the product is, for whom, on which platforms, in which stack. Name the
user-facing name and the internal name if they differ.> The current initiative is specified in
`specs/` and sequenced in `SESSIONS.md`. Further detail: [docs/AGENTS.md](docs/AGENTS.md).

---

## 0. Things that will be got wrong without reading this

<!-- Guidance: every trap an agent has hit, or the bootstrap found. Each item: the symptom, the
cause, and the fix. Concrete commands, flags and file names. Add one each time a session trips. -->

Each of these has already been got wrong once.

1. **<Protection X> hides <what> from the test runner**, so E2E finds nothing and fails with
   misleading selector errors. For E2E and screenshots, build <STAGING> with `<CAPTURE_SWITCH>`
   (a no-op in production). Never weaken <protection X> itself to make a test pass.
2. **<E2E tool and version> ignores plainly exported shell variables**, so the flow types
   `undefined`. Use `tools/maestro/e2e.sh`, which passes them with `-e`.
3. **Run the app with `<flavor/env flag>`.** <The other flavor> fails because <cause>.
4. **The user-facing name is <PRODUCT>.** Never write <internal name> in copy, strings or store text.
5. **<Design constraint>** (for example: system fonts only; colours come from the tokens, never
   literals).
6. **No backend change unless `design/BACKEND-SPLIT.md` lists it**, and even then ship the client
   fallback it names.
7. **The atlas is the UI contract.** A UI change starts in `design/atlas-src`, is rebuilt into the
   atlas, and only then is specified and built. Specs cite screen ids.
8. **No commit and no push without the owner's explicit say-so, every time.** Approval for
   something that needs a commit is not approval to commit. Stage the work, show what would go in,
   and ask.

## 1. The non-negotiables

<!-- Guidance: a summary of .specify/memory/constitution.md. Cite its version and keep it in
step with every amendment. One or two lines per principle; mark the non-negotiable ones. -->

From `.specify/memory/constitution.md` v<X.Y.Z>. Read it; it is short.

- **<Product principle> (I).** <One sentence.>
- **Nothing fails silently (IV).** No dropped async result, no empty `catch`, no empty state while
  loading.
- **One concept, one name (V).** Names are in `docs/delivery/GLOSSARY.md`.
- **Tested at three layers (VI):** unit, widget/component + golden, E2E for every story and atlas
  screen a session builds. Coverage ≥ <80>%.
- **Built screens match the atlas, and that is checked (XIII).** A reviewer who did not write the
  code compares captures with the atlas; differences are fixed or recorded in
  `design/parity/NNN.md`.
- **Minimal backend (VIII).** Every server dependency has a client fallback or is deferred.
- **The atlas is the contract (XI).**

## 2. Where things are

| What | Where |
| --- | --- |
| Constitution | `.specify/memory/constitution.md` |
| Architecture | `ARCHITECTURE.md` |
| Specs (the contract) | `specs/NNN-name/`; start with `checklists/requirements.md` |
| Session order and prompts | `SESSIONS.md` |
| Old → new coverage (brownfield) | `TRACEABILITY.md` |
| Owner decisions (win over everything) | `docs/delivery/DECISIONS.md` |
| Open questions, glossary, discrepancies, backlog | `docs/delivery/*` |
| UI atlas | `design/atlas/index.html`, `this-build.html`; source `design/atlas-src` |
| Backend split | `design/BACKEND-SPLIT.md` (source `design/atlas-src/backend_map.py`) |

## 3. Tracking work

Work is tracked in Jira, project **<JIRA_KEY>** at <JIRA_SITE>. Every feature has an epic; this
initiative's tickets carry the label `<INITIATIVE>`. Reference the Jira key — never an ad-hoc scheme
— in branch names (`feat/<JIRA_KEY>-14-short-slug`), commit subjects (`<JIRA_KEY>-14: page the
list`) and code comments. A session moves its own ticket with `python3 tools/jira.py`.

Scratch TODOs that are not worth a ticket go in <scratch tracker, e.g. bd>. Never leave markdown TODO
lists in the repo.

## 4. Commands

<!-- Guidance: the real commands, verified by running them. -->

- `<lint command>` — lint; run before proposing a commit
- `<full lint command>` — before a PR
- `<test command>` — unit and widget tests with coverage
- `<e2e command>` — E2E against <STAGING>
- `<build-for-capture command>` — the build E2E and screenshots use
- `graphify update .` — rebuild the code graph (local, no AI calls) when code changed since
  `graphify-out/graph.json`; `graphify affected "<symbol>"` before changing a symbol. Call edges can
  be incomplete for <language/pattern>: confirm callers with grep or the language server. Only
  `graphify-out/GRAPH_REPORT.md` is committed.

## 5. Testing

- Unit/widget tests: `<test command>`.
- E2E: read `<e2e README>` first, and see §0.1–0.2. **Point tests at <STAGING> only, never
  production, and only ever at a synthetic account** matching `<SYNTHETIC_PATTERN>`. The wrapper
  refuses anything else.
- E2E selects elements by <accessibility identifier mechanism>. <Framework-only keys> are not
  visible to it; add an identifier to any widget a flow must reach.
- A bug fix adds the test that would have caught it, shown failing first.

## 6. Secrets

`JIRA_SITE`, `JIRA_USER` and `JIRA_TOKEN` live in `.env` (gitignored). Never commit a token. Never
put credentials, tokens, personal data or customer content into reports, logs, tickets or
screenshots.

## 7. Committing and finishing

- Commit only with the owner's say-so (§0.8).
- Run `<lint command>` before proposing a commit, and `<full lint command>` before a PR.
