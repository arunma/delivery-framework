# Maestro examples

Generic starting points for E2E flows and screenshot capture. Copy them into the project's
`.maestro/` and replace the `<...>` placeholders.

- **Staging only, synthetic account only.** Never point a flow at production or at a real person's
  account: flows create and delete data. `e2e.sh` refuses to run unless `APP_EMAIL` matches
  `SYNTHETIC_EMAIL_PATTERN` (default `+test@`).
- **Pass credentials with `-e`.** Maestro 2.x ignores plainly exported shell variables, so a flow
  types `undefined`. `e2e.sh` sources `.maestro/.env.local` and passes `-e APP_EMAIL=… -e APP_PASSWORD=…`.
- **If the app blocks capture** (a secure-screen widget can hide the whole accessibility tree from
  XCUITest, and Maestro then fails with misleading selector errors), add a test-only build switch
  that is a no-op in production builds, and build the capture app with it. Never weaken the
  protection itself to make a test pass.
- **Select by accessibility identifier**, then text, then coordinates as a last resort. In Flutter,
  a `Key` is not an iOS accessibility identifier; use `Semantics(identifier: ...)`.
- **Screenshots are named by atlas screen id**: `common/shot.yaml` with `SCREEN_ID=<screen-id>`
  writes `design/app/<screen-id>.png`, which the parity round compares with the atlas PNG.

Files: `capture_before.yaml` (the "before" capture), `common/login.yaml`, `common/shot.yaml`,
`e2e.sh` (the wrapper), `.env.local.example` (copy to `.maestro/.env.local`, which is gitignored).
