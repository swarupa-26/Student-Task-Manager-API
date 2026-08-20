from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router
from src.api.errors import (
    http_exception_handler,
    request_validation_exception_handler
)
from src.db.config import init_db
app = FastAPI(
    title="Student Task Manager",
    description="A simple REST API to manage student tasks with secure validation and clean architecture.",
    version="1.0.0",
)
# Allow the react.js frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(router)


# Register error handlers
app.add_exception_handler(
    HTTPException,
    http_exception_handler
)

app.add_exception_handler(
    RequestValidationError,
    request_validation_exception_handler
)


# Initialize database when application starts
@app.on_event("startup")
def on_startup():
    init_db()