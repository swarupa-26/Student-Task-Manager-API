# Student Task Manager Implementation Checklist

Purpose: actionable checklist to implement the Student Task Manager REST API (MVP).

-- Project Setup
- [ ] Create project skeleton and required folders (`src/`, `tests/`, `specs/`).
- [ ] Add `requirements.txt`, `.gitignore`, and `README.md` with quickstart.

-- Database & Config
- [ ] Add `src/db/config.py` with SQLAlchemy `Engine` and `SessionLocal`.
- [ ] Add `src/db/base.py` with declarative `Base` and init helper.
- [ ] Configure SQLite connection and `init_db()` on startup.

-- Models & Schemas
- [ ] Implement SQLAlchemy `Task` model in `src/models/task.py`.
- [ ] Implement Pydantic schemas in `src/schemas/task.py` (`TaskCreate`, `TaskUpdate`, `TaskResponse`).
- [ ] Ensure validation rules: title required, status enum, due_date date format, length limits.

-- Repository & Services
- [ ] Implement `src/repositories/task_repo.py` with CRUD functions.
- [ ] Implement `src/services/task_service.py` with business logic and ID generation.
- [ ] Ensure services enforce idempotency for completing tasks and handle not-found cases.

-- API Routes
- [ ] Implement routes in `src/api/routes.py`:
  - `GET /health`
  - `POST /tasks` (create)
  - `GET /tasks` (list)
  - `GET /tasks/{id}` (retrieve)
  - `PATCH /tasks/{id}` (partial update)
  - `DELETE /tasks/{id}` (delete)
  - `POST /tasks/{id}/complete` (complete action)
- [ ] Keep route handlers thin; delegate to services.

-- Error Handling
- [ ] Standardize error response shape (validation errors, not-found, conflicts, server errors).
- [ ] Ensure validation returns structured messages for clients.

-- Tests
- [ ] Unit tests for `task_service` covering create, update, delete, complete, validation.
- [ ] Integration tests for API endpoints using `TestClient` and a temporary SQLite DB.
- [ ] Tests for edge cases: missing title, invalid status, malformed dates, non-existent IDs.

-- Documentation
- [ ] Update `README.md` with quickstart, run commands, and API examples.
- [ ] Keep `specs/student-task-manager/spec.md` and `plan.md` referenced and up to date.

-- Quality Gates
- [ ] All tests pass: `python -m pytest -q`.
- [ ] Code follows constitution principles: simple architecture, validation, clear docs.
- [ ] Ensure no unnecessary dependencies introduced.

-- Optional polish (post-MVP)
- [ ] Add DB migrations (Alembic) if schema changes are expected.
- [ ] Add CI job to run tests on pushes/PRs.
- [ ] Replace SQLite with Postgres for production if needed.

Run/test commands (copy/paste):

```bash
python -m pip install -r requirements.txt
uvicorn main:app --reload
python -m pytest -q
```

Notes:
- Follow the spec and constitution when making trade-offs. Document any deviations in PR descriptions.
