from typing import Any

from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def build_error_response(error: str, message: str, fields: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "error": error,
        "fields": fields or {},
        "message": message,
    }


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    message = exc.detail if isinstance(exc.detail, str) else str(exc.detail)
    error_code = "not_found" if exc.status_code == 404 else "error"
    return JSONResponse(
        status_code=exc.status_code,
        content=build_error_response(error_code, message),
    )


async def request_validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    fields: dict[str, str] = {}
    for error in exc.errors():
        loc = error.get("loc", [])
        field = ".".join(str(item) for item in loc if item != "body")
        if not field:
            field = "body"
        fields[field] = error.get("msg", "Invalid value")

    return JSONResponse(
        status_code=422,
        content=build_error_response("validation_error", "Invalid request data", fields),
    )
