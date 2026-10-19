# Tasks: <NNN-name>

<!-- Guidance: written by the plan-writer (spec-kit /speckit.tasks shape) in specs/NNN-name/tasks.md.
One phase per session, in SESSIONS.md order. tools/sessionize.py reads:
  - the phase heading: "## Phase <n>: Session <ID> · <what a person can do when it is done>"
  - an optional "**Depends on**: <ID>, <ID>" line under it (default: the previous session of this spec)
  - task lines "- [ ] T001 [P] [US1] Description (FR-001, FR-002) in path/to/file"
and, from plan.md, the "Session mapping" table (Session | FRs | Stories | Screens | E2E flows).
Never renumber a task; withdraw it with a line through it and a reason. -->

**Input**: specs/<NNN-name>/spec.md, plan.md · **Sessions**: S01, S02

## Phase 1: Session S01 · <What a person can do when this session is done>

**Depends on**: F1

### Start
- [ ] T001 `python3 tools/jira.py start <JIRA_KEY>-NN`; write the GAPS IN list

### Tests first (must fail before implementation)
- [ ] T002 [P] [US1] Unit tests for <pure function> (FR-001, FR-002) in <test path>
- [ ] T003 [P] [US1] Component and golden tests for <screen or output> states (FR-003) in <test path>
- [ ] T004 [US1] E2E or integration flow <NNN_story-slug> (FR-001–FR-003) in <flow path>

### Implementation
- [ ] T005 [US1] <What is built> (FR-001, FR-002) in <source path>
- [ ] T006 [US1] <What is built> (FR-003) in <source path>

### Close (the Definition of done, in order)
- [ ] T007 Tests and coverage at the floor; paste the output
- [ ] T008 E2E or integration flows green with captures or outputs by contract id
- [ ] T009 Verification round by an independent reviewer (the gate in .delivery/profile.json)
- [ ] T010 Simpler-way review; leftovers to BACKLOG.md
- [ ] T011 Lint and analysis clean; diagrams current
- [ ] T012 HANDOFF.md if work remains; `jira.py done` or `comment`; stage and ask

## Phase 2: Session S02 · <What a person can do when this session is done>

**Depends on**: S01

### Start
- [ ] T013 `python3 tools/jira.py start <JIRA_KEY>-NN`; start from HANDOFF.md; GAPS IN

### Tests first (must fail before implementation)
- [ ] T014 [P] [US2] <Test> (FR-004) in <test path>

### Implementation
- [ ] T015 [US2] <What is built> (FR-004) in <source path>

### Close (the Definition of done, in order)
- [ ] T016 The five Definition of done steps, then stage and ask

## FR → task coverage

| FR | Tasks |
| --- | --- |
| FR-001 | T002, T004, T005 |
