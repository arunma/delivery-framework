# Checklist

One short checklist per step of [FRAMEWORK.md](FRAMEWORK.md). Don't start a step until the one
before it is ticked. Every tick needs evidence: a file, pasted command output, or the owner's written
word. Skip the steps your `PROFILE.md` marks off. For projects without screens, read "mockups" and
"screenshots" as your contract and its check (see the table in FRAMEWORK.md).

Project: `<PROJECT>` · Size: ☐ small ☐ medium ☐ large · ☐ existing ☐ new ☐ adopt midway

## Step 0 · Assess
- [ ] `.delivery/PROFILE.md` written; the owner confirmed what you're building, the size and the risks
- [ ] Each part has its contract and its check named
- [ ] `.delivery/guards.json` in place; the owner knows how to approve a commit

## 0 · Bootstrap
- [ ] Untracked docs backed up first
- [ ] The owner read the report and answered or deferred every question
- [ ] Existing project: code graph built; survey covers stack, modules, tests, CI, how to run
- [ ] New project: stack decision in `DECISIONS.md` with options and tradeoffs
- [ ] Adopt midway: every existing document mapped to a step; gap list agreed

## 1 · Setup
- [ ] `CLAUDE.md` §0 lists every trap found, each with symptom, cause and fix
- [ ] `AGENTS.md` has the owner's rules and a *Project Learnings* list
- [ ] Tracker project exists; `.env` holds its credentials and `git check-ignore .env` prints `.env`
- [ ] `.env` ends with a newline before anything is appended to it (`tail -c1 .env | xxd`)
- [ ] `git check-ignore -v docs/delivery specs design` prints nothing, so the plan can be committed

## 2 · Capture today
- [ ] Staging and synthetic data only; no real person's data anywhere
- [ ] Every capture opened and checked; unreachable ones in `MISSING.md`
- [ ] Any test-only capture switch does nothing in production, and a test proves it

## 3 · Research
- [ ] Every research claim has a source, or is marked unverified
- [ ] At least one review by a reviewer that did not draw the contract

## 4 · Contract
- [ ] Backed up before every change
- [ ] Builds or validates with no errors: unique ids, no broken links (mockups: `build_screen_map.py --strict`)
- [ ] Every review finding fixed, or rejected with a reason
- [ ] The owner approved it (dated line in `DECISIONS.md`)

## 5 · Decisions
- [ ] Every open question has a recommendation and says what it blocks
- [ ] Every answer is in `DECISIONS.md` and applied to the contract
- [ ] `GLOSSARY.md` covers every name in the contract

## 6 · Backend split
- [ ] Every "already exists" claim has a file:line
- [ ] Every item is ships reduced, deferred or critical; critical list empty or approved
- [ ] `BACKEND-SPLIT.md` regenerated, not hand-edited

## 7 · Constitution
- [ ] The owner chose the non-negotiables
- [ ] `CLAUDE.md` cites the same version; old version strings updated

## 8 · Architecture
- [ ] Every verified claim has a file:line; conflicts copied to `DISCREPANCIES.md`
- [ ] Mermaid diagrams compile (`mmdc`); `archify validate` passes for `docs/diagrams/*.json`

## 9 · Specs
- [ ] `specs/` backed up first
- [ ] Every contract id is covered by a requirement; 0 unresolved or duplicate references
- [ ] Every story has a flow diagram; no requirement renumbered
- [ ] Existing project: `TRACEABILITY.md` maps every current feature

## 10 · Plans and tasks
- [ ] Each planning agent wrote only in its own spec folder (`git status` checked)
- [ ] Every requirement has a task; every constitution check passes
- [ ] Every `plan-discrepancies.md` merged into `DISCREPANCIES.md`

## 11 · Sessions
- [ ] `sessionize.py validate SESSIONS.md --strict` passes
- [ ] Every session has a readable `<area>-<what>` name and fits one context; split ones are named parts
- [ ] `RUN-SHEET.md` passes `runsheet.py`; `SESSIONS-EXPLAINED.md` lists every session
- [ ] Every requirement falls in some session; a close block after every wave
- [ ] Owner tasks listed, each naming the session it blocks

## 12 · Tracker
- [ ] A ticket per session and backend item; one dependency link checked by hand
- [ ] `jira-map.json` committed; keys written into `SESSIONS.md` and specs

## 13 · Each session
- [ ] Ticket started; the first output lists the open gaps that touch this session
- [ ] Tests written first and seen failing; all three test layers green, output pasted
- [ ] Every end-to-end run passed or is marked **NOT RUN** with a reason
- [ ] Check file (`design/parity/NNN.md` or `verification/NNN.md`) by a fresh reviewer, no open rows
- [ ] Simpler-way review done; lint clean, output pasted
- [ ] Work staged on the wave branch and a commit message proposed. **The owner commits**: one
  commit per session, its key in the subject

## 13 · Each wave close
- [ ] Every check so far re-run; regressions traced to a session
- [ ] Real not-done list written; proposed fixes waiting on the owner
- [ ] The owner pushed the wave branch once and opened one PR; any `.delivery/APPROVED` is deleted

## 14 · Learning
- [ ] Every mistake this wave is a rule, a template change, or "no rule needed"
- [ ] `AGENTS.md` pruned (under 300 lines)
