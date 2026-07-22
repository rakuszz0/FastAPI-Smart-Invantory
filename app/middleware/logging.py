import time

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

from app.core.logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self,
        request: Request,
        call_next
    ):

        start_time = time.time()

        response = await call_next(request)

        process_time = (
            time.time() - start_time
        )

        logger.info(
            "%s %s | %s | %.4fs",
            request.method,
            request.url.path,
            response.status_code,
            process_time
        )

        return response