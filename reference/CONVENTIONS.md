# Conventions every delivery skill follows

Every skill in this plugin reads this file first. It holds the rules that would otherwise be
repeated in each one. `${CLAUDE_PLUGIN_ROOT}` below means the plugin root path the calling skill
printed (skills get it substituted; this file is read as plain text).

## 1. Read the profile before doing anything

1. Open `.delivery/profile.json` in the project root. If it is missing, run the `assess` skill
   first (it writes the profile and `.delivery/PROFILE.md`), then come back.
2. Find this skill's phase in `phases`. If its `status` is `off`, say so in one line, name the
   reason (`why`), and stop unless the owner explicitly overrides it. If it is `swapped`, do the
   swapped work named in `with`, not the UI default.
3. Use the surface's contract artefact and verification gate from `contracts`. "Atlas" and
   "parity" in the framework text mean the UI case; for any other surface read them as "the
   contract artefact" and "the verification gate" the profile names.

## 2. Paths

- Plugin files: `${CLAUDE_PLUGIN_ROOT}/FRAMEWORK.md` (the full guide), `${CLAUDE_PLUGIN_ROOT}/CHECKLIST.md`
  (the gates), `${CLAUDE_PLUGIN_ROOT}/prompts/`, `${CLAUDE_PLUGIN_ROOT}/templates/`,
  `${CLAUDE_PLUGIN_ROOT}/tools/`.
- Tools: if the project has its own copy in `tools/` (the framework recommends copying them so
  sessions pasted without the plugin still work), use it. Otherwise call the plugin's copy, for
  example `python3 ${CLAUDE_PLUGIN_ROOT}/tools/jira.py show <KEY>`.
- Project paths are the ones in FRAMEWORK.md § "Where things go in a project". Never invent new ones.

## 3. Guards (never relaxed by a skill)

- Staging only, synthetic accounts and synthetic data only. Never production, never a real person's
  data, never production extracts as test data.
- No credentials, tokens, personal data or document contents in logs, reports, screenshots,
  fixtures, tickets or commit messages. Never print `.env`.
- **No commit and no push.** End with the work staged, the staged file list and a proposed subject
  (`<JIRA_KEY>-NN: …`), and ask. Approval of the work is not approval to commit. The `git_guard`
  hook enforces this in projects with a `.delivery/` directory.
- When two documents, or a document and the code, disagree: stop, append it to
  `docs/delivery/DISCREPANCIES.md` (template `${CLAUDE_PLUGIN_ROOT}/templates/DISCREPANCIES.md`),
  and ask. Never resolve it silently. Never edit the spec you are implementing.
- Back up untracked documents (specs, atlas source, contracts) before an agent rewrites them.
- Never weaken a protection (screen security, auth, validation) to make a test pass.

## 4. Evidence

"It works, I ran it" is not evidence. Paste command output. A check that could not run is reported
**NOT RUN** with its reason, never as passing. Claims about existing code carry `path:line`.

## 5. Code graph

If `graphify-out/graph.json` is older than the last commit, run `graphify update .` (local, no AI
calls). Query the graph (`graphify query`, `path`, `explain`, `affected`) before broad file reads.
Call edges can be incomplete; confirm callers with grep or the language server.

## 6. Tiers

`tier` in the profile sets how much of the pipeline runs: **S** = ticket → test-first change → PR,
**M** = a spec and a plan, then one session, **L** = the full pipeline with waves. A skill whose phase
is off for the tier says so; the `tiering` skill re-classifies when the work turns out bigger.
