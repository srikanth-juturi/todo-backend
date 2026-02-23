from typing import Any

from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.request_context import get_trace_id


class AppError(Exception):
    def __init__(
        self,
        *,
        code: str,
        message: str,
        status_code: int,
        details: Any = None,
    ) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(message)


class TodoNotFoundError(AppError):
    def __init__(self, todo_id: int) -> None:
        super().__init__(
            code="TODO_NOT_FOUND",
            message="Todo not found",
            status_code=404,
            details={"todo_id": todo_id},
        )


class TodoValidationError(AppError):
    def __init__(self, message: str, details: Any = None) -> None:
        super().__init__(
            code="TODO_VALIDATION_ERROR",
            message=message,
            status_code=422,
            details=details,
        )


def build_error_response(*, code: str, message: str, details: Any, status_code: int) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": code,
                "message": message,
                "details": jsonable_encoder(details),
                "trace_id": get_trace_id(),
            }
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def handle_app_error(_: Request, exc: AppError) -> JSONResponse:
        return build_error_response(
            code=exc.code,
            message=exc.message,
            details=exc.details,
            status_code=exc.status_code,
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(_: Request, exc: RequestValidationError) -> JSONResponse:
        return build_error_response(
            code="REQUEST_VALIDATION_ERROR",
            message="Validation failed",
            details=exc.errors(),
            status_code=422,
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_error(_: Request, __: Exception) -> JSONResponse:
        return build_error_response(
            code="INTERNAL_SERVER_ERROR",
            message="Unexpected server error",
            details=None,
            status_code=500,
        )
