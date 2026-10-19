# Pilot guide

How a team tries the plugin for three weeks and decides, with numbers, whether to keep it. Read
[README.md](README.md) first.

## 1. Decide what success means

Before week 1, write your bars in `pilot/LOG.md` (copy [templates/pilot-LOG.md](templates/pilot-LOG.md)).
Every number links to a ticket, a PR or a file.

| Measure | How | Suggested bar |
| --- | --- | --- |
| Cycle time: ticket started → PR ready | Tracker timestamps | No worse than comparable past work |
| Rework: sessions that needed a second go | Count in the log | At most 1 in 3 |
| Check passed first time (no open rows) | `design/parity/*.md`, `verification/*.md` | At least half by week 2 |
| PRs a person had to fix before merge | PR history | Falling week on week |
| Sessions that fit in one context | Count in the log | At least 70% |
| Guard incidents (a commit, push, `.env` write or production command got through) | Log | 0 |

## 2. Pick the project and the slice

- A project the team knows, with a staging environment and a way to load synthetic data.
- Two or three low-risk sessions from one feature: no auth, payment or encryption changes. Medium
  size is the usual fit; one small ticket is a good warm-up.
- If you can, pilot two projects: one app and one API or data pipeline, so both kinds of check get
  tried.
- Avoid a deadline-critical release, sensitive or regulated data, or a repo with no tests (add a test
  harness first, as its own ticket).

## 3. What you need

- Claude Code (built and checked on 2.1.285) and the plugin ([install](README.md#install));
  `/delivery:` should autocomplete.
- Python 3.9+. Optional: graphify and archify (`tools/setup-tools.sh`, installs globally, read it
  first), Mermaid CLI (`mmdc`), spec-kit for medium and large work. Without them, sessions mark those
  checks NOT RUN.
- Tracker credentials in the project's gitignored `.env`; never pasted into a chat or a ticket.
- Staging and synthetic accounts only. No production URL or credential on a pilot machine; list
  production patterns in `.delivery/guards.json` so the guard catches them.
- Somewhere to run end-to-end checks: a simulator or device (apps), an ephemeral environment (APIs),
  a local warehouse such as DuckDB (data).

## 4. Who

- **Owner** (one person): confirms the profile, answers questions, approves the contract, commits,
  makes the go/no-go call.
- **Engineer** (one or two): runs the sessions, reads every report, keeps the log.
- **Reviewer** (not running sessions): reviews PRs as usual, notes every fix they had to make, and
  spot-checks one check file per session against the contract.

## 5. Week by week

**Week 0, set up.**
1. `/delivery:start` in the pilot repo. Correct what it detected; confirm the size; read `PROFILE.md`
   with the owner.
2. Test the guards: ask the agent to `git commit` (it must be blocked) and to `cat .env` (it must ask
   first). Add a production pattern and check it is caught.
3. For the pilot slice only: write the contract (`/delivery:screen-map` or `/delivery:contract`), then
   `/delivery:specify-from-contract`, `/delivery:verify-specs`, `/delivery:plan-and-tasks`. The owner
   approves each.
4. `/delivery:jira-sync` as a dry run. Record baseline numbers from comparable past work.
5. Create the wave branch, `wave/<closing key>-<wave-name>`, from an up-to-date main. Every pilot
   session works on it. `RUN-SHEET.md` has the commands.

**Weeks 1 and 2, run sessions.**
1. At most one session a day, each started by hand in a fresh Claude Code session:
   `/delivery:session <name>`.
2. Check the report against [CHECKLIST.md](CHECKLIST.md) §13 first. Missing evidence: send it back
   and count it as rework.
3. The owner reviews `git diff --staged` and commits it on the wave branch (one commit per session,
   its key in the subject). After the wave's close session, the owner pushes the branch once and
   opens one PR for the wave; the reviewer reviews it. A wave that does not reach its close stays
   unpushed.
4. Log the session the same day.

**Week 3, decide.**
1. `/delivery:close-wave 1`: re-run everything, the real not-done list, lessons turned into rules.
2. Fill the go/no-go list below with the owner, the engineers and the reviewer.
3. Send generic lessons back to the framework ([CONTRIBUTING.md](CONTRIBUTING.md)), anonymised.

## 6. Every day

1. `/delivery:status`: what is next, what drifted.
2. Pick the next session whose dependencies are done; run it in a fresh session.
3. Answer what it asks; don't let it decide product questions.
4. Read the report, check the evidence; the owner commits or sends it back.
5. Log it: ten minutes at the end of the day.

## 7. Known problems and fixes

From the case study ([examples/case-study-mobile-vault.md](examples/case-study-mobile-vault.md)) and
later use.

| Symptom | Cause | Fix |
| --- | --- | --- |
| E2E fails with selector errors that look like wrong ids | Screen protection hides the app from UI automation | A staging-only capture switch that does nothing in production, with a test. Never weaken the protection |
| The E2E flow types `undefined` into a field | Some E2E tools ignore exported shell variables | Pass credentials with `-e` through `tools/maestro/e2e.sh` |
| Imported test files get names like `IMG_<timestamp>` | Importing from the photo library renames them | Import from the Files app |
| Untracked specs or mockups overwritten | An agent rewrote files with no git history | Back up before every change; the skills do it first |
| Parallel planning agents step on each other | Shared files and branch-switching scripts | Each writes only its own spec folder; one main session merges; check `git status` |
| Every dependency link in Jira is backwards | The tracker's link payload is inverted | `create_tickets.py` handles it; check one pair by hand |
| Links in the mockups go to the wrong screen | Two screen ids share a prefix | `build_screen_map.py --strict` fails on it |
| Different screens show different facts | Each part invented its own sample data | One facts block in the kit |
| A session block fails when run on its own | It said "see above" | Every block repeats its guards in full |
| "Done" with nothing pasted | The session summarised instead of proving | Reject it, send it back, count it as rework |
| The session ran out of context | The slice was too big | Stop at a task boundary, write `HANDOFF.md`; split it into named parts (sessionize skill) |
| The agent commits after "looks good" | Approval of the work was read as approval to commit | The git guard blocks it; the owner approves each commit |
| The agent pushed as well as committed | `.delivery/APPROVED` allows any commit and push for its whole window | Delete it right after the one commit |
| The planning documents cannot be committed, with no error | `docs/` or another planning folder is in `.gitignore` | `git check-ignore -v` on each folder before the first commit; re-include it |
| `/delivery:status` shows no progress for any session | The status tool did not read the project's phase headings | Use the `tasks.md` template's heading; report any other format as a framework bug |
| A token stops working after a key was appended to `.env` | `.env` had no trailing newline, so two lines merged | Check `tail -c1 .env` before appending |
| Pipeline tests pass on a changed answer key | The key was regenerated to make a test pass | The answer key changes only with the contract |

## 8. Go or no-go

Go if all of these hold:
- [ ] The bars set in week 0 were met, or missed for a reason that is now fixed.
- [ ] Zero guard incidents.
- [ ] Every merged PR had a check file with no open rows and pasted test output.
- [ ] The reviewer would accept the same process on the next feature.
- [ ] A non-app project was piloted too, or the decision is limited to app work.

No-go or partial: keep what helped (often contract first, the guards and the independent check) and
run everything as small work until the team chooses otherwise.

**Rollback** (nothing is irreversible): `claude plugin disable delivery@delivery-framework` stops the
hooks at once; delete the project's `.delivery/` folder; the contracts, specs and plans stay as
ordinary docs.

## 9. Optional: sessions from CI

Once interactive sessions work, you can run them from CI.
[ci/github-actions/](ci/github-actions/) has an **example** workflow: run by hand with a session name
and the wave branch, it runs `/delivery:session <name> --ci` headless on that branch, commits the
session there and opens the wave's draft PR if it has none. It never creates a branch. Read its
README, adapt it, and run it on the smallest session first. It needs the Claude GitHub App, an `ANTHROPIC_API_KEY` secret and branch protection. App
end-to-end flows can't run on a Linux runner; they show NOT RUN and need a local run before the PR is
ready. Never point it at production. To roll back, remove the workflow file and its secrets.
