# Run sheet — <PRODUCT> <initiative>

<!-- Guidance: written by the sessionize skill next to SESSIONS.md (docs/delivery/RUN-SHEET.md). It
says only what to type and when; the prompts are in SESSIONS.md. One "#### <step>. <name> — …" heading per
session, every session exactly once, each after everything it depends on. Check it with
`python3 tools/runsheet.py RUN-SHEET.md --sessions SESSIONS.md`. Lines starting with `/` are typed
inside Claude Code; the rest in a terminal at the repo root. Remove these comments when filled in. -->

The exact commands, one by one, in dependency order, grouped by wave. Owner decisions:
`docs/delivery/DECISIONS.md`. How the sessions were derived: `SESSIONS-EXPLAINED.md`.

**Rules that hold throughout**

- **Runs are manual.** Each session is a fresh Claude Code session started by hand, with the
  `delivery` plugin. CI-driven runs are optional (`PILOT.md` §9).
- **One branch per wave**, `wave/<closing key>-<wave-name>`, where the key is the close session's
  ticket. Created from an up-to-date main; every session of the wave works on it.
- **The agent never commits or pushes.** A session ends staged with a report. You review it and
  commit it from your own terminal: one commit per session, subject `<KEY>: <summary>`. After the
  wave's close session passes, you push the branch once and open one PR for the wave.
- **The approval file.** `touch .delivery/APPROVED` lets the agent commit, but for its whole time
  window it allows any commit *and* any push. Delete it right after the one commit.
- **Strictly in order**, unless a session says **May run in parallel**. Parallel runs on a second
  machine commit there and bring the commit over (`git format-patch -1 HEAD`, then `git am`) before
  any session that depends on it starts, so the wave is still pushed once, from one machine.

## Legend

| Name | Means |
| --- | --- |
| Step number | The order to run in, across the whole build |
| `<area>-<what>` | A session (`labels-domain`: the labels area, its domain logic) |
| Two names, one area | A session split to fit one context (`labels-domain`, `labels-store`). Each part is its own ticket and closes itself |
| `close-<wave-name>` | The session that closes that wave (`close-foundation`, `close-wave-1`) |

## When a session stops short

A session that runs out of context stops at a task boundary, writes `specs/NNN-*/HANDOFF.md` naming
the next task, and leaves its ticket *In Progress* with a comment.

1. Leave the partial work staged, or commit it if you want to.
2. Start a **fresh** Claude Code session and run the **same** command. It resumes from the HANDOFF.
3. A session that **blocked** wrote the problem to `docs/delivery/DISCREPANCIES.md` and asked you.
   Answer, then re-run the same name.

Commit only when the report meets `SESSIONS.md` *How to tell a session actually finished*.

---

## Once, before anything

```
claude --version
/plugin marketplace add arunma/delivery-framework    # inside Claude Code, then:
/plugin install delivery@delivery-framework
tail -c1 .env | xxd | grep -q 0a || echo >> .env    # .env must end with a newline before you append
git check-ignore -v docs/delivery specs design      # must print nothing, or the plan cannot be committed
```

---

## Foundation — `wave/<KEY>-NN-foundation`

Sessions: foundation-flag, …, close-foundation. Each wave has the same shape as wave 1 below:
before the wave, one heading per session, then its close, push and PR.

#### 1. foundation-flag — The flag, identifiers, the E2E wrapper, goldens and parity tooling · <KEY>-NN

After: nothing. Strictly in order.

```
claude                                  # fresh session at the repo root, on the wave branch
/delivery:session foundation-flag
git diff --staged
git commit -m "<KEY>-NN: the flag, identifiers, the E2E wrapper, goldens and parity tooling"
```

---

## Wave 1 — <theme> — `wave/<KEY>-NN-wave-1`

Sessions: widgets-domain, widgets-screens, close-wave-1. Tickets: <KEY>-NN …

**Before the wave**

```
git switch main && git pull
git switch -c wave/<KEY>-NN-wave-1      # the key of close-wave-1
graphify update .                       # refresh the code graph
claude                                  # then, inside Claude Code:
/delivery:status                        # read-only: what is done, what is next, drift
```

#### 2. widgets-domain — <what a person can do when it is done> · <KEY>-NN

After: foundation-flag. Strictly in order.

```
claude                                  # fresh session at the repo root, on the wave branch
/delivery:session widgets-domain        # or paste its block from SESSIONS.md
# wait for the staged report; check it against SESSIONS.md 'How to tell a session actually finished'
git diff --staged
git commit -m "<KEY>-NN: <what a person can do when it is done>"
```

#### 3. widgets-screens — <what a person can do when it is done> · <KEY>-NN

After: widgets-domain. Strictly in order.

```
claude
/delivery:session widgets-screens
git diff --staged
git commit -m "<KEY>-NN: <what a person can do when it is done>"
```

#### 4. close-wave-1 — Close wave 1 · <KEY>-NN

After: widgets-domain, widgets-screens. Strictly in order.

```
claude
/delivery:close-wave 1
git diff --staged
git commit -m "<KEY>-NN: close wave 1"
```

**Wave close — push and PR**

```
git log --oneline main..wave/<KEY>-NN-wave-1   # one commit per session, each with its key
git push -u origin wave/<KEY>-NN-wave-1
gh pr create --base main --head wave/<KEY>-NN-wave-1 --title "<wave title>" --body "<keys>"
# review the PR, merge it, then:
git switch main && git pull
```
