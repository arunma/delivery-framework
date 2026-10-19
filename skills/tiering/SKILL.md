---
name: tiering
description: Classify a piece of work as tier S, M or L and pick the lightest delivery path - S is ticket to test-first change to PR, M is a spec plus a plan then one session, L is the full pipeline with contract, specs, plans, sessions and waves. Use at intake, when someone asks how much process a change needs, or when work in progress turns out bigger or smaller than its tier.
argument-hint: "[short description of the work or a ticket key]"
---

# Tier the work

Plugin root: `${CLAUDE_PLUGIN_ROOT}`. Read `${CLAUDE_PLUGIN_ROOT}/reference/CONVENTIONS.md` first.
Work to classify: `$ARGUMENTS` (ask for it if empty).

## Classify by the highest row that applies

| Signal | S | M | L |
| --- | --- | --- | --- |
| Contract change | none | adds to the contract (a screen, an operation, a column) | a new contract or a redesign |
| Size | one session, under a day | one to three sessions | many sessions, waves |
| Specs touched | none (the ticket is the spec) | one | several, with seams between them |
| Backend or cross-repo change | none | one with a client fallback | several, or no fallback |
| Risk flags in the profile | none apply to the change | one applies | sensitive or regulated data is touched |
| Unknowns | none | a few, answerable this week | open product questions |

When unsure between two tiers, choose the higher and say why. A non-negotiable principle touched by
the change (data leaving the device, sensitive data, auth) is never tier S.

## Paths

- **S, ticket → PR:** the ticket's description is the spec (acceptance criteria as Given/When/Then).
  Run `run-session` with the ticket key: Jira start, GAPS IN, failing test first, the change, the
  verification gate for the surface touched, lint, evidence comment, stage and ask. No SESSIONS.md.
- **M, spec + plan:** `specify-from-atlas` for the one spec (citing contract ids), `verify-specs`,
  `plan-and-tasks` with one session phase, `jira-sync` for its ticket, then `run-session`.
- **L, full pipeline:** the track's bootstrap, then every phase the profile has on, in FRAMEWORK.md order.

## Output

The tier, the one-line reason (the rows that decided it), the path's next command, and anything that
would raise the tier later. If `.delivery/profile.json` exists and its tier differs, re-run
`python3 ${CLAUDE_PLUGIN_ROOT}/tools/assess.py . --tier <T>` with the surfaces it already has, after
the owner agrees.
