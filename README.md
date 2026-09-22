
Built entirely through Spec-Driven Development (SDD)—where machine-readable markdown specifications act as the single source of truth before any code is generated.

# Overview
This project does not rely on ad-hoc or "vibe" coding. Instead, every feature, data contract, and architectural boundary is formally defined in structured specification files. AI coding agents and developers use these specs as strict execution and validation gates.

# Student Task Manager

A simple REST API for managing student tasks with clean code, secure validation, and meaningful automated tests.

## Features

- Create, update, list, and delete tasks
- Validated REST API input using Pydantic models
- Clear status codes and error handling
- Built-in API documentation via FastAPI

## Quick Start

1. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

2. Start the development server:

```powershell
uvicorn main:app --reload
```

3. Open the API docs:

- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`

## REST API Endpoints

- `GET /health` — health check
- `GET /tasks` — list all tasks
- `GET /tasks/{task_id}` — retrieve a single task
- `POST /tasks` — create a task
- `PATCH /tasks/{task_id}` — update a task
- `DELETE /tasks/{task_id}` — remove a task
- `POST /tasks/{task_id}/complete` — mark a task as completed

## Testing

Run tests with:

```powershell
pytest
```
