# CI pilot: tickets to pull requests (example)

**This is an example for the pilot, not a tested workflow for your repository.** Copy
[delivery-session.yml](delivery-session.yml) into the project's `.github/workflows/`, read it, and
adapt it. Run it first with `workflow_dispatch` on one low-risk session.

## What happens

1. An issue whose title is `<SESSION-ID> · <summary> · <TICKET-KEY>` gets the label
   `delivery:ready`, or someone runs the workflow by hand with a session id and a ticket key.
2. The job validates both ids against strict patterns (issue text never reaches a shell command
   unquoted), creates the branch `feat/<TICKET-KEY>-session-<id>`, and runs
   [`anthropics/claude-code-action@v1`](https://github.com/anthropics/claude-code-action) in automation
   mode with the plugin installed from this marketplace and the prompt `/delivery:session <ID> --ci`.
3. The session runs the execution loop and ends with its work **staged**. The plugin's git guard
   blocks Claude from committing or pushing.
4. A plain shell step commits the staged files to the session branch and opens a **draft** pull
   request. The pull request is the owner's review: evidence, verification file, diff. Nothing merges
   automatically.

## Secrets (placeholders; set them in the repository's Actions secrets)

| Secret | Needed | Notes |
| --- | --- | --- |
| `ANTHROPIC_API_KEY` | yes (or `CLAUDE_CODE_OAUTH_TOKEN` with the `claude_code_oauth_token` input) | Claude API access for the action |
| `JIRA_SITE`, `JIRA_USER`, `JIRA_TOKEN` | optional | Without them the session reports Jira as NOT RUN |
| Staging settings for integration tests | optional | **Staging only, synthetic accounts only.** No production secret may exist in this repository |

The Claude GitHub App must be installed on the repository for the action's default authentication
(see the action's README). `id-token: write` is needed for that.

## Permissions

The job asks for `contents: write` (push the session branch), `pull-requests: write` (open the
draft), `issues: write` (the action may comment on the triggering issue) and `id-token: write` (the
action's authentication). Nothing else. Protect the default branch so a person must approve every
merge.

## Limits to know before the pilot

- **No device E2E on a Linux runner.** UI sessions report Maestro or simulator flows as NOT RUN, so
  their parity round needs a local or device-farm run before the PR is ready. API, data and CLI
  sessions can run their integration layer in CI if the environment allows.
- **Pull requests opened with the default `GITHUB_TOKEN` do not trigger other workflows.** Use a
  GitHub App token or run the project's CI by hand on the branch.
- **Cost:** `--max-turns` and `timeout-minutes` cap a run; `concurrency` stops two runs on the same
  issue at once.
- **Never on a production configuration**: no production URLs, flavors or credentials in the
  runner. Set `prod_guard` patterns in `.delivery/guards.json` so a slip is stopped.
