# Phase 2 · Capture the before (brownfield)

Needs: a staging build that runs on a simulator or emulator, a **synthetic** staging account, and
the E2E tool. The owner approves deleting old test data from that account.

```
Capture today's app for <PRODUCT> so every redesign can be paired with what it replaces. Staging
only, never production. Synthetic account only (<SYNTHETIC_PATTERN>); never print its credentials.

1. Seed. Write a generator for synthetic content: 25–40 items with human names typical of the
   product, spread over the app's groupings, a few starred, one shared with the owner's own
   synthetic address. Each file is generated (stamped SPECIMEN, placeholder bars): no real names,
   numbers, addresses or documents. Load it through the app or an E2E seed flow. Import from a source
   that keeps file names (e.g. the Files app, not the photo library). Record exactly what you seeded,
   what was there before, and everything that went wrong while seeding in design/seed.md
   (<framework>/templates/seed.md). Glitches are review findings: keep them.
2. Capture switch. If the app's screen protection blocks screenshots or hides the accessibility tree
   from the test runner, add a test-only build switch, <CAPTURE_SWITCH>, that turns it off in
   staging only. It must be a no-op in the production build, and a unit test must prove that. Never
   weaken the protection itself. Add the trap to CLAUDE.md §0.
3. Flow. Write <e2e dir>/screenshots/capture_before.yaml (pattern:
   <framework>/tools/maestro/capture_before.yaml) that visits each screen in the list below and saves
   design/before/<screen-id>.png. Prefer accessibility identifiers, then text, then coordinates. Pass
   credentials with -e through tools/maestro/e2e.sh (Maestro ignores plainly exported variables).
   Screens: <01-sign-in, 02-home, …>, plus <02-home-dark> taken separately.
4. Look. Open every PNG. A capture that is blank, shows a spinner or an error, or shows the wrong
   screen does not count: fix the flow and capture again. A screen that truly cannot be reached goes
   to design/before/MISSING.md with the reason. Never pair a redesign with a screenshot of a
   different screen.

Commit nothing. Report: the screens captured, MISSING.md, the seed summary, the switch and its test
output, and the traps found.
