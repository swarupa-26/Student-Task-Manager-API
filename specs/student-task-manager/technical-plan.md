# Technical Implementation Plan — Student Task Manager

**Stack**
- Python 3.13
- FastAPI (REST API)
- Pydantic (request/response validation)
- SQLAlchemy (ORM)
- SQLite (initial database)
- pytest (tests)

This plan follows the project constitution and the approved feature specification. The architecture is intentionally simple and modular: separate API routes, schemas, DB models, DB configuration, business logic (services/repositories), and tests.

## Goals
- Implement the required CRUD + complete operations for tasks.
- Enforce validation and status enum rules.
- Keep modules small and single-responsibility to ease testing and future extension.
- Use SQLite for durability in v1 while keeping the repository layer pluggable for later DB changes.

## Project layout (recommended)
```
student-task-manager/
├── main.py                  # FastAPI app entry (keeps minimal app startup)
├── requirements.txt
├── README.md
├── CONSTITUTION.md
├── specs/
│   └── student-task-manager/
│       ├── spec.md
│       ├── plan.md
│       └── technical-plan.md
├── src/
│   ├── api/
│   │   └── routes.py        # API route registration and route handlers
│   ├── schemas/
│   │   └── task.py          # Pydantic request/response models
│   ├── models/
│   │   └── task.py          # SQLAlchemy ORM models
│   ├── db/
│   │   ├── config.py        # Engine, session and initialization helpers
│   │   └── base.py          # Declarative base and session utilities
│   ├── services/
│   │   └── task_service.py  # Business logic + repository interface
│   └── repositories/
│       └── task_repo.py     # DB access methods (CRUD)
├── tests/
│   ├── unit/
│   │   └── test_task_service.py
│   └── integration/
│       └── test_api.py
└── migrations/               # Optional: for DB migrations if later needed
```

Notes:
- `main.py` imports and includes `src.api.routes` and initializes DB (if needed).
- Keep FastAPI app instantiation minimal to keep it importable by tests.

## Components & Responsibilities

- API routes (`src/api/routes.py`)
  - Register endpoints and map requests to service calls.
  - Keep route handlers thin: validate request (Pydantic does this), call service, map result to response model.

- Request/response schemas (`src/schemas/task.py`)
  - Define `TaskCreate`, `TaskUpdate`, `TaskResponse` Pydantic models.
  - Enforce: `title` required, `description` optional, `status` enum restricted to `pending`, `in_progress`, `completed`, `due_date` as date.

- Database models (`src/models/task.py`)
  - SQLAlchemy ORM `Task` model with `id` (UUID or autoincrement integer), `title`, `description`, `status`, `due_date`, `created_at`, `updated_at`.
  - For simplicity and portability, use SQLite-supported types. Use `UUID` as string column or SQLAlchemy's `GUID` pattern; choose string-based UUID for cross-DB compatibility.

- Database configuration (`src/db/config.py`)
  - Create SQLAlchemy `Engine` with `sqlite:///./data.db` (file in project root) or in-memory option for tests.
  - Provide a `SessionLocal` factory and dependency helper for FastAPI (yielding session and closing after request).

- Business logic (`src/services/task_service.py`)
  - Implement higher-level operations: create_task, list_tasks, get_task, update_task, delete_task, complete_task.
  - Handle status semantics and validation beyond schema-level rules (e.g., idempotency for complete).
  - Use the repository for DB operations; services implement transactional boundaries.

- Repository (`src/repositories/task_repo.py`)
  - Encapsulate raw DB operations (SQLAlchemy ORM queries). Return model instances or primitives.
  - Keep simple interface: add, get_by_id, list_all, update, delete.

- Tests (`tests/`)
  - Unit tests for `task_service` using a SQLite in-memory DB and per-test session resets.
  - Integration tests for API using FastAPI `TestClient` and a temporary SQLite DB file or in-memory DB wired to the app dependency overrides.

## Data model details
- `Task` fields:
  - `id`: string UUID (generated server-side), primary key
  - `title`: string, required, length limit 1–200
  - `description`: text, optional, max length 1000
  - `status`: string/enum, allowed values: `pending`, `in_progress`, `completed`
  - `due_date`: DATE, optional
  - `created_at`: timestamp
  - `updated_at`: timestamp

Validation rules are enforced at the Pydantic layer and re-checked in the service layer when necessary.

## Transactions & Concurrency
- For v1 single-student app, simple transactions per request are sufficient. Use session-per-request pattern.
- Document that multi-user concurrency is out of scope for v1; repository/service layer should be designed so adding optimistic locking later is straightforward.

## Error handling
- Return consistent JSON error responses. Use HTTP codes:
  - `201 Created` for successful create
  - `200 OK` for successful reads/updates
  - `204 No Content` for successful delete
  - `404 Not Found` when task does not exist
  - `422 Unprocessable Entity` for validation errors (Pydantic default) or `400 Bad Request` for custom validations
  - `409 Conflict` for uniqueness/constraint violations (unlikely in v1)
  - `500 Internal Server Error` for unexpected failures

Error response example:
```json
{ "error": "validation_error", "fields": { "title": "required" } }
```

## Implementation steps (detailed)
1. Create module structure (folders and __init__.py as needed).
2. Add DB config (`src/db/config.py`) with `create_engine`, `SessionLocal`, `Base`.
3. Implement SQLAlchemy `Task` model in `src/models/task.py`.
4. Implement Pydantic schemas in `src/schemas/task.py`.
5. Implement repository `src/repositories/task_repo.py` with CRUD methods.
6. Implement service `src/services/task_service.py` using the repository.
7. Add API routes in `src/api/routes.py` and wire to `main.py`.
8. Add tests:
   - Unit tests for service using an in-memory SQLite DB.
   - Integration tests for API using `TestClient` with dependency override for DB session.
9. Update `README.md` with quickstart and test commands.
10. Run test suite and iterate.

## Development & run commands
Install dependencies:
```bash
python -m pip install -r requirements.txt
```
Run app in development:
```bash
uvicorn main:app --reload
```
Run tests:
```bash
python -m pytest -q
```

## Estimated effort
- Phase 0–2 full implementation: 2–4 days
- Tests and polish: 1–2 days

## Notes and non-goals
- Do not add ORMs or migration tools beyond SQLAlchemy for v1 unless migrations are required; keep DB simple.
- Authentication, multi-tenant/multi-user support, and advanced concurrency are out of scope for initial delivery.

---

If you want, I can now scaffold the `src/` modules and implement the DB config, models, schemas and basic routes, then run tests. Which implementation step should I start with?"