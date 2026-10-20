---
name: run-wave
description: Run a whole wave of SESSIONS.md sessions from one conversation - resolve the wave, check its branch, find the next undone session, then spawn one fresh session-runner subagent per session in dependency order, route every question it returns to the owner, stop after each so the owner commits with `!`, run the wave's close, and print the push and PR commands for the owner. Resumable. Use when someone runs /delivery:wave, says "run wave 2" or "run the foundation", or wants every session of a wave run in turn.
argument-hint: "<wave number | name>"
---

# Run a wave

Plugin root: `${CLAUDE_PLUGIN_ROOT}`. Read `${CLAUDE_PLUGIN_ROOT}/reference/CONVENTIONS.md` first.
Wave: `$ARGUMENTS`.

You are the **parent**. You never write the session's code yourself: each session runs in a
**child**, a fresh `session-runner` subagent (`${CLAUDE_PLUGIN_ROOT}/agents/session-runner.md`)
that does exactly what `/delivery:session <name>` does and returns a report of at most 25 lines.
A subagent cannot ask the owner anything, so a child that needs a decision stops and returns
`NEEDS USER`; you ask, and pass the answer back. You keep only the reports, not the children's work.

**Never** run `git commit` or `git push`, create or touch the approval file, or pass `--no-verify`.
The git guard blocks commits and pushes in children too. Creating or switching the wave branch is
allowed, and only after the owner says so.

## 1. Resolve the wave

```
python3 ${CLAUDE_PLUGIN_ROOT}/tools/sessionize.py wave "<arg>" --sessions SESSIONS.md --tasks specs/*/tasks.md
```

It prints JSON: `title`, `branch` (`branches` if blocks disagree), `close` (the close sessions) and
`sessions` in dependency order, each with `step`, `name`, `key`, `depends_on`, `after` (dependencies
outside this wave), `parallel_with`, `close` and `tasks` (ticked/total). The argument is `0` or a
word of the first section's title for the first section, `N` for "Wave N", a word of a section title
(`close`, `model`), the wave branch or a word in it, or a session name. With no argument, use the
current branch. An unknown or ambiguous argument exits 1 with the list of waves: ask which
(AskUserQuestion). Stop if the branch still holds a `<JIRA_KEY>` placeholder (run `jira-sync` first)
or `branches` has more than one entry (ask which).

## 2. Check the branch

The **base branch** is `base_branch` in `.delivery/profile.json`, default `main`. A project that keeps
long work off `main` (e.g. a long-lived `ui-revamp` branch) sets it there; waves branch from it and
their PRs target it.

`git branch --show-current`. If it is not the wave's branch, ask (AskUserQuestion): switch to it
(it exists: `git rev-parse --verify <branch>`), create it from an up-to-date base branch
(`git switch <base> && git pull --ff-only && git switch -c <branch>`), or stop. Uncommitted changes
travel with a switch: show `git status --short` and ask before switching.

## 3. Find what is done and show the plan

A session is **done** when a commit whose subject starts with `<KEY>:` is reachable from HEAD
(`git log --format=%s | grep "^<KEY>:"`). Show `tasks` beside it; all tasks ticked with no commit
means work staged and waiting for the owner. With Jira credentials in `.env`, add
`sessionize.py status --sessions SESSIONS.md specs/*/tasks.md --jira` and report drift (never print
the credentials). Check every `after` dependency the same way; one not done is a blocker to raise.

If `git diff --staged` is not empty before the first child, ask what it is: a finished session
waiting for its commit (give the `!` commit line, §4 step 4), or something to set aside first.

Show one screen: wave title and branch; **Done** (name · key); **Next**; **Remaining** in order with
their dependencies; blockers. If two runnable sessions list each other under `parallel_with`, offer
to run them together (§5, default off). Ask to start.

## 4. One child per session, in order

For the next undone session whose dependencies are done:

1. **Spawn** one `session-runner` subagent (`delivery:session-runner`; plain `session-runner` if the
   scoped name is not found) and wait for its report before doing anything else. Give it only:
   `Run session <name> (<KEY>) from SESSIONS.md on branch <branch>. Plugin root: ${CLAUDE_PLUGIN_ROOT}.`
   plus any owner answers for this session. Nothing from your own notes.
2. **needs-user:** ask the questions with AskUserQuestion (up to four per call), the child's
   recommendation first and marked *(Recommended)*. Send the answers to the same child with
   SendMessage (its agent id), which resumes it with its context intact. If it cannot be resumed,
   spawn a fresh `session-runner` for the same session with the answers in its task; it continues
   from the HANDOFF and the working tree. Repeat until it returns done or stopped-short.
3. **stopped-short:** show the report and offer (AskUserQuestion): a fresh child for the same
   session (it resumes from HANDOFF.md), commit the partial work first, or stop the wave here.
4. **done:** show the report and `git diff --staged --stat`. Check it against SESSIONS.md *How to
   tell a session actually finished*; if evidence is missing, say what and offer a fresh child to
   finish it. Otherwise tell the owner to review and commit it in this chat:

   ```
   ! git diff --staged
   ! git commit -m "<KEY>: <summary>"
   ```

   Then stop and wait. Output from a `!` command lands in this conversation, and you answer it.
   Continue only when `git log -1 --format=%s` starts with `<KEY>:` and nothing is staged; if not,
   say what is missing and wait again. If the owner asks you to commit, say that the owner commits.
5. **Context.** After each session, if this conversation is getting long (several sessions run, or
   long reports and questions), say so and suggest `/clear` then `/delivery:wave <wave>`: commits,
   `tasks.md` and HANDOFF files hold all the state, so it resumes at the next undone session.

## 5. Parallel (opt-in, default off)

Only for two sessions that list each other under `parallel_with`, are both runnable, and do not
work on the same spec (the same `tasks.md` or `HANDOFF.md`), and only if the owner opts in and says
they will not contend for one device, emulator or staging account. Spawn both children in one
message; tell each the other is running in the same working tree. When both are done, check their
staged file lists do not overlap (if they do, stop and ask), then give one commit per session,
limited to its files: `! git commit -m "<KEY>: <summary>" -- <its files>`. Never more than two.

## 6. Close the wave

The wave's close sessions (`close` in the JSON) run last, each as a child like any other; the child
follows the block with the `wave-close` skill. A section with no close session skips this. Then
print, for the owner to run, never run them yourself:

```
! git log --oneline <base>..<branch>
! git push -u origin <branch>
! gh pr create --base <base> --head <branch> --title "<wave title>" --body "<every key in the wave>"
```

## Report

The wave, its branch, each session with its key and outcome, the questions asked and the answers,
what was skipped or stopped short, and the next step (push and PR, or the next undone session).
