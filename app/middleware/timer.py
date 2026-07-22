import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class TimerMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self,
        request: Request,
        call_next
    ):

        start = time.perf_counter()

        response = await call_next(request)

        end = time.perf_counter()

        response.headers["X-Process-Time"] = str(
            round(end - start, 6)
        )

        return response