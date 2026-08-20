# Tasks: Student Task Manager (complete, dependency-aware)

**Source artifacts**: `spec.md`, `plan.md`, `technical-plan.md`, `checklist.md`

This file organizes work into phases, with explicit task IDs and dependencies.

PHASE LEGEND: P0 = Setup, P1 = Foundational (blocking), P2 = Feature implementation, P3 = Tests & QA, P4 = Docs & Handover

---

## Phase P0 — Setup (quick wins)
- [T001] Project skeleton and tooling — Create `src/`, `tests/`, `specs/`, `README.md`, `.gitignore`, `requirements.txt` (depends: none) (status: done)
- [T002] CI / test runner smoke — Ensure `pytest` runs and basic linting (depends: T001)

Estimated: 0.5 day

---

## Phase P1 — Foundational (blocking)
These must be completed before feature endpoints are implemented.

- [T101] DB base and config — `src/db/base.py`, `src/db/config.py`, `init_db()` and `get_db()` dependency for FastAPI (depends: T001) (status: done)
- [T102] Database model — SQLAlchemy `Task` model in `src/models/task.py` (depends: T101) (status: done)
- [T103] Pydantic schemas — `src/schemas/task.py` (`TaskCreate`, `TaskUpdate`, `TaskResponse`) and validation rules (depends: T102) (status: done)
- [T104] Repository layer — `src/repositories/task_repo.py` with CRUD operations (add/get/list/update/delete) (depends: T102) (status: done)
- [T105] Service layer — `src/services/task_service.py` implementing business rules, id generation, `complete_task` logic (depends: T104, T103) (status: done)
- [T106] API routes skeleton — `src/api/routes.py` registering endpoints and wiring to services (depends: T105, T103, T101) (status: done)

Checkpoint: app starts, DB schema created, routes registered (but not feature-complete). Estimated: 1–2 days

---

## Phase P2 — Feature Implementation (user stories / endpoints)
Implement endpoints and map them to service methods. Tasks ordered by priority.

User Story US1 (Core CRUD) — Priority: P1
- [T201] Create task endpoint — `POST /tasks` (validate `TaskCreate`, return `201` with `TaskResponse`) (depends: T103, T105, T106) (status: done)
- [T202] List tasks endpoint — `GET /tasks` (depends: T104, T106) (status: done)
- [T203] Retrieve task endpoint — `GET /tasks/{id}` (return `200` or `404`) (depends: T104, T106) (status: done)
- [T204] Update task endpoint — `PATCH /tasks/{id}` (partial update) (depends: T105, T106) (status: done)
- [T205] Delete task endpoint — `DELETE /tasks/{id}` (permanently delete; return `204`) (depends: T104, T106) (status: done)
- [T206] Complete action endpoint — `POST /tasks/{id}/complete` (idempotent; set status=`completed`) (depends: T105, T106) (status: done)

User Story US2 (Validation & Errors) — Priority: P2
- [T207] Centralize error responses — agree schema and implement helper (e.g. `src/api/errors.py`) (depends: T106) (status: done)
- [T208] Validation checks in services — enforce title presence, allowed status values, due_date parsing (depends: T103, T105) (status: done)

User Story US3 (Health & Docs) — Priority: P3
- [T209] Health endpoint — `GET /health` and verify `/docs` and `/redoc` are available (depends: T106) (status: done)

Estimated: 1–3 days for MVP endpoints depending on testing cadence

---

## Phase P3 — Tests & QA
Tests must be written alongside implementation; listed here as explicit tasks.

- [T301] Unit tests for services — `tests/unit/test_task_service.py` covering create, update, delete, complete, validation (depends: T105) (status: done)
- [T302] Integration tests for API — `tests/integration/test_api.py` covering full request flows and error cases (depends: T201–T206, T207) (status: done)
- [T303] Edge case tests — missing title, invalid status, malformed due_date, non-existent IDs (depends: T302) (status: done)
- [T304] Idempotency tests — completing twice, deleting non-existent resource behavior (depends: T302) (status: done)

Quality gate: All tests pass locally and in CI. Estimated: 1–2 days

---

## Phase P4 — Documentation, polish & handover

- [T401] README quickstart & API examples — update `README.md` with run/test and example requests (depends: T201–T209)
- [T402] Update `specs/` — mark `spec.md`, `plan.md`, `technical-plan.md` as implemented where applicable (depends: T401)
- [T403] Code cleanup and constitution check — ensure code follows project constitution (simplicity, validation, docs) (depends: T301–T304)
- [T404] Optional: Add DB migrations (Alembic) if schema change plan exists (depends: T102)

Estimated: 0.5–1 day

---

## Dependencies & Execution order (summary)
- P1 foundational tasks (`T101` → `T102` → `T103` → `T104` → `T105` → `T106`) must complete before P2 endpoints.
- Endpoint tasks (`T201`–`T206`) depend on P1 and should be implemented in order T201, T202, T203, T204, T205, T206.
- Error handling (`T207`) and service validations (`T208`) should be in place early to ensure consistent behavior.
- Tests (`T301`–`T304`) should be created as soon as corresponding implementation tasks exist; they block merging to main.

---

## How to use this task list
- Assign one or more tasks to an issue/PR. Use the task ID in branch names (e.g., `feature/T201-create-task`).
- Keep each PR small and focused: one API resource or one service change per PR.
- Run tests locally before pushing and ensure CI runs `pytest`.

---

If you want, I can convert selected tasks into issues or start implementing `T201` (`POST /tasks`) and accompanying tests next. 