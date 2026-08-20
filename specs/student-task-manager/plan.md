# Implementation Plan: Student Task Manager

**Branch**: `student-task-manager` | **Date**: 2026-08-11

## Summary
Deliver a minimal, well-tested Student Task Manager REST API that fulfills the spec: create, list, retrieve, update, delete, and complete tasks. The plan is phased so we deliver a reliable MVP quickly and add durability and polish in later phases.

## Phases

### Phase 0 — Setup (1 day)
Purpose: Create project skeleton, tooling, and CI basics.
- Create repository structure: `src/` or root `main.py` (existing), `tests/`, `specs/`, `docs/`.
- Add `requirements.txt`, `.gitignore`, and `README.md` (done).
- Configure minimal CI (optional): run `pytest` on push.

### Phase 1 — Foundational (1–2 days)
Purpose: Implement core models, validation, and routing skeleton.
- Task T001: Define the `Task` data model and validation rules in `spec.md` and code (title, description, status enum, due_date, id).
- Task T002: Implement input validation guidelines and error response schema.
- Task T003: Add routing skeleton for endpoints: `GET /health`, `POST /tasks`, `GET /tasks`, `GET /tasks/{id}`, `PATCH /tasks/{id}`, `DELETE /tasks/{id}`, `POST /tasks/{id}/complete`. (Use `PATCH` for partial updates; `PUT` is not required for v1.)
- Task T004: Add repository abstraction backed by SQLAlchemy/SQLite to provide durable persistence for v1.

### Phase 2 — User Story Implementation (2–3 days)
Purpose: Implement and test each user story independently (P1 → P2 → P3).
- US1 (P1): Task CRUD
  - T005 Implement `POST /tasks` with validation and `201` response.
  - T006 Implement `GET /tasks` and `GET /tasks/{id}` with `200`/`404` behaviors.
  - T007 Implement `PATCH` for updates (partial update) including status transitions.
  - T008 Implement `DELETE /tasks/{id}` returning `204`.
- US2 (P2): Validation and errors
  - T009 Add test coverage for invalid inputs (missing title, bad date, invalid status).
  - T010 Ensure consistent error response shape across endpoints.
- US3 (P3): Health & Docs
  - T011 Add `GET /health` and verify `/docs` and `/redoc` are present.

### Phase 3 — Tests, Edge Cases, and Polishing (1–2 days)
Purpose: Strengthen quality with tests and small improvements.
- T012 Add unit tests for model validation and business rules.
- T013 Add integration tests for the full request flows (create→update→complete→delete).
- T014 Add tests for idempotency (completing an already completed task).
- T015 Add input sanitization checks and length-limits tests.

### Phase 4 — Documentation & Handover (half day)
Purpose: Ensure developers and users can run and understand the API.
- T016 Update `README.md` with quickstart and API examples.
- T017 Add `specs/` references and acceptance test instructions.

## Acceptance Criteria (mapped to tasks)
- Creating a task returns `201` and the created resource (T005).
- Listing tasks returns `200` and an array (T006).
- Retrieving missing task returns `404` (T006).
- Updating with invalid status returns validation error and no change (T009).
- Deleting a task returns `204` and subsequent GET returns `404` (T008).
- Marking completed changes `status` to `completed` and is idempotent (T007, T014).

## Risks & Mitigations
- Risk: Concurrency/consistency with in-memory store — Mitigation: single-student v1, add persistence and optimistic locking later.
- Risk: Unclear update semantics (`PUT` vs `PATCH`) — Mitigation: Use `PATCH` for partial updates and document behavior; `PUT` can be full replace if needed.

## Next Steps
1. Implement Phase 1 tasks (models, validation, routes) and push small PRs per user story.
2. Add tests as features are implemented (write tests before fixes where practical).
3. After MVP, switch the repository abstraction to a persistent store (SQLite/Postgres) if needed.


---

## File map suggested for implementation
```
main.py                # FastAPI app and routes (or backend/src/api.py)
```
main.py                # FastAPI app and routes
src/
  db/                  # DB config and base (SQLAlchemy + SQLite)
  models/              # SQLAlchemy models (Task)
  repositories/        # Repository abstractions (SQLAlchemy-backed)
  services/            # Business logic
  api/                 # FastAPI routers
tests/
  integration/         # integration tests
  unit/                # unit tests
specs/
  student-task-manager/spec.md
  student-task-manager/plan.md
  student-task-manager/technical-plan.md
README.md
requirements.txt
```
- MVP (Phases 0–2): 4–6 days of focused work
- Polish and docs (Phase 3–4): 1–2 days

