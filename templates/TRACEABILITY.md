# Traceability — <old version> → <new version>

<!-- Guidance: brownfield, MANDATORY. Proves every current capability has a named home in a new
spec, or a stated reason for removal. Nothing may disappear silently. Greenfield (optional): the
same table maps each need from the interview to the spec that meets it. Sessions update the rows
they implement. -->

What this file proves: every capability in <inventory source, e.g. docs/delivery/CURRENT-INVENTORY.md
at commit `<sha>`> has a named home in a spec, or a stated reason for removal.

- **Source of rows:** every route, screen, sheet or dialog, user action, setting, feature flag,
  gate and notable widget in the inventory.
- **Source of homes:** the specs, read in full: each *Carried over from today* table, the FRs, user
  stories and edge cases. FR ids are cited only where the requirement exists (checked by grep, on
  <date>). Where a spec covers an item only in its carried-over table, the cell says *carried*.
- **Status words:** **Kept** (same behaviour) · **Restyled** (same job, new look) · **Moved** (same
  job, different place) · **Merged** (folded into another surface) · **Replaced** (a different
  mechanism) · **Removed** (no successor; reason given).
- **Sessions** update this file when they implement a row.

**Counts (<date>):** <N> rows in <G> groups: <group n · …>. Kept <a> · Restyled <b> · Moved <c> ·
Merged <d> · Replaced <e> · Removed <f>.

## Table A — Every current capability → new home

### A.1 <Group>

| # | Capability today | Where (path) | Status | New home (spec · FR · screen) | Note |
|---|---|---|---|---|---|
| A1.1 | <…> | `<path>` | Restyled | `NNN` FR-0xx · `<screen-id>` | <…> |
| A1.2 | <…> | `<path>` | Removed | — | <reason; owner decision id> |

## Table B — New capabilities (no current equivalent)

| # | Capability | Spec · FR · screen |
|---|---|---|

## Table C — Specs → screens, FRs, backend items, sessions

| Spec | Screens | FRs | Backend items | Sessions (Jira) | Build |
|---|---|---|---|---|---|
| `NNN-name` | <n> | <n> | <ids> | <ids (keys)> | This build / reduced / later |
