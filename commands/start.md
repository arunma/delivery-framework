---
description: Start on this project - work out what you are building, whether it is an existing or new project, and its size (small, medium, large), then name the next step
argument-hint: "[brownfield|greenfield|adopt-midway] [S|M|L]"
---

Start the delivery framework in this project. Arguments (optional): $ARGUMENTS

1. If `.delivery/profile.json` is missing, or the arguments change the track or tier, run the
   `delivery:assess` skill first, passing the track and tier given here.
2. If the track or tier is still unknown, ask the owner for both in one question, in plain words:
   is this an existing project (brownfield), a new project (greenfield), or one that already has
   specs or docs (adopt midway)? And how big is it: small (a ticket goes straight to a PR), medium
   (a short spec and plan first) or large (the full flow with a contract, specs and sessions)?
   Use the `delivery:tiering` skill to recommend a size. Small, medium and large are tiers S, M, L.
3. Show `.delivery/PROFILE.md` in short: what you are building and its contract, how the result
   is checked against the contract, and the steps that are off or swapped.
4. Name the next command: tier L → the track's bootstrap skill (`delivery:bootstrap-brownfield`,
   `delivery:bootstrap-greenfield` or `delivery:adopt-midway`); tier M → `delivery:specify-from-contract`;
   tier S → `/delivery:session <TICKET-KEY>`. Do not run it without the owner's go-ahead.
