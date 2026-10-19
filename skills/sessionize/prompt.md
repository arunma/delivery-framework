# Phase 11 · Session prompts

```
Write SESSIONS.md for <PRODUCT> from <framework>/templates/SESSIONS.md. Inputs: every
specs/*/plan.md "Session mapping" table and tasks.md phases, DECISIONS.md, OPEN-QUESTIONS.md,
BACKEND-SPLIT.md, the atlas (this-build.html).
1. Order: foundation first (flag, identifiers, E2E wrapper, capture build, shot helper, golden
   matrix, atlas-compare and parity-check, coverage gate; then the design system, the data layer,
   the shell), then engines with no screens, then screens wave by wave by dependency, sign-in and
   first run last, then a closing session that removes the flag. Later builds (deferred backend) in
   their own sections.
2. Keep the template's top sections: how to use it, order and why, wave table, Definition of done
   (5 steps, full), the parity reviewer prompt and the parity file format, owner tasks (each naming
   the session it blocks), "How to tell a session actually finished".
3. One block per session, named <area>-<what> in kebab case and sized to one context (sessionize
   skill). Heading: "### <step>. <name> — <what a person can do> · <JIRA_KEY>-NN", and on the next
   line "*Depends on: <names>. Branch: `wave/<closing key>-<wave-name>`. Epic: <EPIC>.*"
   (tools/create_tickets.py parses these). The fenced block is self-contained: guards, Jira
   start/done, GAPS IN, context discipline and HANDOFF, spec and FR range, stories, atlas screens
   (with reduced stand-ins), backend fallback, read-first list, set .specify/feature.json, "do not
   re-plan" for part 2+, watch-fors (the discrepancies and open questions that bite here), E2E flows
   by name, the DoD in short, the report format. A block pasted alone must carry everything.
4. A wave-close block, close-<wave-name> (close-foundation, close-wave-1), after every wave, with the seams specific to that wave.
   Then RUN-SHEET.md and SESSIONS-EXPLAINED.md from their templates.
5. Session coverage: list every FR not in any session's range; there must be none (or each is
   explicitly "not built in this build", with the reason).
6. Run python3 tools/create_tickets.py --dry-run --sessions SESSIONS.md --items
   docs/delivery/backend-items.json --project <JIRA_KEY> --epic <EPIC> --label <INITIATIVE> and fix
   every parse error or unknown dependency.
Do not edit specs. Report: sessions per wave, FR orphans (should be 0), the dry-run summary, the
owner tasks.
```
