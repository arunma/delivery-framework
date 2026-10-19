# Contributing

The framework follows itself. A change to it is held to the same rules it asks of a project:
evidence before claims, one concept with one name, and nothing resolved silently.

## Proposing a change

1. **Open an issue first** for anything larger than a typo. Say what went wrong (or what is
   missing), on which track (brownfield, greenfield, adopt midway) and which phase, and what you
   propose. A lesson from a real project is the best reason for a change; describe it without naming
   the project, its people or its code.
2. **Change every place the rule lives.** A rule usually appears in more than one file: the guide
   (`FRAMEWORK.md`), the gate (`CHECKLIST.md`), the prompt (`prompts/`), the template (`templates/`)
   and sometimes a tool (`tools/`). A pull request that changes one and leaves the others
   contradicting it will be asked to finish the job, or to record the gap.
3. **Keep the vocabulary.** Use the existing names (atlas, screen id, session, wave, parity round,
   Definition of done, GAPS IN, HANDOFF). Do not introduce a synonym for an existing concept.
4. **Prove tool changes.** For `tools/`, paste the output of the offline checks in the pull
   request:
   - `python3 tools/jira.py show X-1` with no credentials (it must fail cleanly, without printing
     a token);
   - `python3 tools/create_tickets.py --dry-run` against a sample `SESSIONS.md` and
     `tools/samples/backend-items.json`;
   - `uv run render_parts.py` and `uv run build_atlas.py --strict` in `tools/atlas-starter/`;
   - `python3 -m unittest discover -s tests` (hooks, `assess.py`, `sessionize.py`) and
     `claude plugin validate --strict .` for any change to the plugin's skills, commands, agents,
     hooks or manifests. A change to `assess.py` that alters a fixture's profile updates
     `tools/samples/fixtures/*.expected.json` in the same pull request, with the reason.
5. **Add to a case study** in `examples/` if the change comes from a lesson, with counts where you
   have them. Case studies are anonymised: no product names, company names, people, repository
   paths or file:line references into private code.
6. **Keep it short.** Every line should prevent a mistake. If a section grows, prune something.

## What will not be merged

- Secrets, tokens, real personal data or screenshots of real accounts.
- References to a specific company's tracker site, internal repositories or people.
- Changes that weaken a guard (no commit without the owner, staging and synthetic accounts only,
  never weaken a protection to make a test pass) without an issue that argues for it.

## Licence

By contributing you agree that your contribution is licensed under the repository's licence
([LICENSE](LICENSE)).
