# Tasks: 001-sample-list (sample for tools/sessionize.py)

## Phase 1: Session S01 · A person can browse the list

**Depends on**: F1

- [x] T001 `python3 tools/jira.py start DEMO-11`; GAPS IN
- [x] T002 [P] [US1] Unit tests for list sorting (FR-001, FR-002) in test/list_sort_test
- [x] T003 [US1] Golden tests for the list and empty states (FR-003, FR-004) in test/list_golden
- [x] T004 [US1] List screen (FR-001–FR-004) in src/list
- [ ] T005 Definition of done steps 1–5; stage and ask

## Phase 2: Session S02 · A person can open one item

- [ ] T006 `python3 tools/jira.py start DEMO-12`; start from HANDOFF.md; GAPS IN
- [ ] T007 [US2] Detail screen tests (FR-005, FR-006) in test/detail
- [ ] T008 [US2] Detail screen (FR-005, FR-006) in src/detail
- [ ] T009 Definition of done steps 1–5; stage and ask

## FR → task coverage

| FR | Tasks |
| --- | --- |
| FR-001 | T002, T004 |
