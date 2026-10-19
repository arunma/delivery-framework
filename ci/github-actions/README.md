# CI pilot: sessions on the wave branch (example)

**This is an example for the pilot, not a tested workflow for your repository.** Copy
[delivery-session.yml](delivery-session.yml) into the project's `.github/workflows/`, read it, and
adapt it. Run it first with `workflow_dispatch` on one low-risk session.

## What happens

The model is one branch per wave, one commit per session and one push and pull request per wave.
The workflow fits into it; it never creates a branch.

1. The owner creates the wave branch, `wave/<closing key>-<wave-name>`, and pushes it. Then someone
   runs the workflow by hand with a session name, its ticket key and that wave branch.
2. The job validates all three against strict patterns (inputs never reach a shell command
   unquoted), checks out the wave branch, and runs
   [`anthropics/claude-code-action@v1`](https://github.com/anthropics/claude-code-action) in automation
   mode with the plugin installed from this marketplace and the prompt `/delivery:session <name> --ci`.
3. The session runs the execution loop and ends with its work **staged**. The plugin's git guard
   blocks Claude from committing or pushing.
4. A plain shell step commits the staged files as the session's one commit on the wave branch,
   pushes the branch, and opens the wave's **draft** pull request if it has none yet (later sessions
   add commits to the same pull request). The pull request is the owner's review: evidence,
   verification files, diff. It is marked ready after the wave's close. Nothing merges automatically.
5. Run the sessions of a wave one at a time, in the run sheet's order; `concurrency` queues a second
   run on the same wave branch.

## Secrets (placeholders; set them in the repository's Actions secrets)

| Secret | Needed | Notes |
| --- | --- | --- |
| `ANTHROPIC_API_KEY` | yes (or `CLAUDE_CODE_OAUTH_TOKEN` with the `claude_code_oauth_token` input) | Claude API access for the action |
| `JIRA_SITE`, `JIRA_USER`, `JIRA_TOKEN` | optional | Without them the session reports Jira as NOT RUN |
| Staging settings for integration tests | optional | **Staging only, synthetic accounts only.** No production secret may exist in this repository |

The Claude GitHub App must be installed on the repository for the action's default authentication
(see the action's README). `id-token: write` is needed for that.

## Permissions

The job asks for `contents: write` (push the wave branch), `pull-requests: write` (open the
wave's draft) and `id-token: write` (the action's authentication). Nothing else. Protect the default branch so a person must approve every
merge.

## Limits to know before the pilot

- **No device E2E on a Linux runner.** UI sessions report Maestro or simulator flows as NOT RUN, so
  their parity round needs a local or device-farm run before the PR is ready. API, data and CLI
  sessions can run their integration layer in CI if the environment allows.
- **Pull requests opened with the default `GITHUB_TOKEN` do not trigger other workflows.** Use a
  GitHub App token or run the project's CI by hand on the branch.
- **Cost:** `--max-turns` and `timeout-minutes` cap a run; `concurrency` stops two runs on the same
  wave branch at once.
- **Never on a production configuration**: no production URLs, flavors or credentials in the
  runner. Set `prod_guard` patterns in `.delivery/guards.json` so a slip is stopped.
