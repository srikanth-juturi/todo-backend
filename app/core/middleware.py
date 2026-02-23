import logging
import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.request_context import set_trace_id

logger = logging.getLogger("app.request")


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        trace_id = request.headers.get("x-trace-id") or str(uuid.uuid4())
        set_trace_id(trace_id)

        started_at = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = round((time.perf_counter() - started_at) * 1000, 2)

        response.headers["x-trace-id"] = trace_id

        logger.info(
            "request_completed",
            extra={
                "route": request.url.path,
                "method": request.method,
                "status_code": response.status_code,
                "latency_ms": elapsed_ms,
            },
        )
        return response
