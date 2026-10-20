---
name: wave-close
description: Close a wave of sessions - re-run every E2E or integration check written so far, sweep verification for drift across the whole wave, propose (never apply) resolutions for the wave's discrepancies, list what is really not done, test the seams between specs, run a simpler-way review, and run the learning loop that turns each miss into a rule. Use after the last session of a wave is committed, or when someone asks for the wave's real completion state.
argument-hint: "<wave number>"
---

# Close a wave

Plugin root: `${CLAUDE_PLUGIN_ROOT}`. Read `${CLAUDE_PLUGIN_ROOT}/reference/CONVENTIONS.md` first and
check the profile (phase `wave-close`). Wave: `$ARGUMENTS`.

1. Find the wave's close block in SESSIONS.md (`### W<n>·Close · …`, or a named one such as
   `### 18. close-<wave-name> — …`) and follow it; it is
   self-contained. Work on the wave's branch (`wave/<closing key>-<wave-name>`), never a new one.
   Jira start first; GAPS IN as the first output.
2. Re-run every E2E flow, integration test, golden-dataset run or eval written so far, not only this
   wave's, on a fresh build against staging or an ephemeral environment, synthetic data only. A run
   that passed in its session and fails now is a regression: name the session.
3. Unit, coverage, analyzer and full lint. Paste the output.
4. Whole-wave verification sweep: run `parity-review` for every spec this wave touched, looking for
   drift since its own round; re-run every *Partial* row whose owner spec is now built.
5. Discrepancies from this wave: propose a resolution for each (amend the spec, amend the contract,
   close it). Apply none without the owner.
6. The real not-done list, by spec: success criteria with no test, stories with no flow, contract ids
   with no passing verification row, runs NOT RUN.
7. Test the seams the block lists (numbers two features must agree on, flows crossing two specs).
8. Simpler-way review across the wave.
9. **Learning loop** ([prompt.md](prompt.md)): every mistake an agent made this
   wave becomes a proposed rule for AGENTS.md *Project Learnings*, a §0 trap for CLAUDE.md, a template
   change, or "no rule needed". Propose pruning (AGENTS.md near 100 lines, under 300). Apply none
   without the owner. Generic lessons go back to the framework (CONTRIBUTING.md).
10. Check tracker drift: `python3 ${CLAUDE_PLUGIN_ROOT}/tools/sessionize.py status --sessions SESSIONS.md specs/*/tasks.md --jira`.

Report the pasted outputs, the sweep's results, the proposals waiting on the owner, the not-done
list, the seams, the learning-loop proposals and the staged files. Then ask. The owner commits this
session like the others (`git log --oneline <base>..<wave branch>` (base: `base_branch` in `.delivery/profile.json`, default `main`) shows one commit per session, each
with its key), then pushes the wave branch once and opens one pull request for the wave.
