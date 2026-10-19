---
description: Start the delivery framework on this project - assess it, choose the track and tier, and name the next step
argument-hint: "[brownfield|greenfield|adopt-midway] [S|M|L]"
---

Start the delivery framework in this project. Arguments (optional): $ARGUMENTS

1. If `.delivery/profile.json` is missing, or the arguments change the track or tier, run the
   `delivery:assess` skill first, passing the track and tier given here.
2. If the track or tier is still unknown, ask the owner for both in one question: track
   (brownfield: existing code; greenfield: new repo; adopt midway: specs or docs already exist) and
   tier (S: ticket → PR; M: one spec and plan; L: the full pipeline). Use the `delivery:tiering`
   skill to recommend a tier.
3. Show `.delivery/PROFILE.md` in short: surfaces and their contract artefacts, the gates, and the
   phases that are off or swapped.
4. Name the next command: tier L → the track's bootstrap skill (`delivery:bootstrap-brownfield`,
   `delivery:bootstrap-greenfield` or `delivery:adopt-midway`); tier M → `delivery:specify-from-atlas`;
   tier S → `/delivery:session <TICKET-KEY>`. Do not run it without the owner's go-ahead.
