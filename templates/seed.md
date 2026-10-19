# Seed data for captures

<!-- Guidance: the synthetic dataset every capture and parity screenshot uses. Never real people,
documents, numbers or addresses. Brownfield: record what was there before and what was deleted
(with the owner's agreement). Greenfield: no "before" section; the seed is the screen map's facts
block, loaded into the first build. The screen map kit's facts block and this file must agree; a
mapping table covers unavoidable differences. -->

Seeded <YYYY-MM-DD> into the synthetic <STAGING> account (`<SYNTHETIC_PATTERN>`, credentials in
the gitignored E2E env file — never here). Display name: **<synthetic name>**. Every item is
generated (stamped SPECIMEN, placeholder bars) — no real names, numbers or content.

## What was there before (brownfield)

<What the account held, and how it was cleared, with the owner's agreement.>

## Dataset (<N> items)

| Group | Item | Attributes (type, starred, shared, expiry …) |
|---|---|---|
| <group> | <item name> | <…> |

<Legend for markers. Counts as the app shows them after seeding.>

## Seed ↔ screen map mapping

| Screen map (kit facts) | App seed | Why they differ |
|---|---|---|
| Owner *<screen map name>* | *<seed display name>* | <…> |

## How it was seeded

1. `<generator command>` writes the synthetic files.
2. <How they reach the device/app, e.g. copied into the simulator's Files app so names survive.>
3. `<E2E seed flows>` create groups, import items, set attributes. Run with credentials passed by
   `-e`, against <STAGING> only.

## Things that went wrong while seeding (kept as review evidence)

- <Each glitch seen while seeding: it is a finding for the review.>

## Restoring the seed

<How a flow that changes data restores it, or which second synthetic account it uses instead.>
