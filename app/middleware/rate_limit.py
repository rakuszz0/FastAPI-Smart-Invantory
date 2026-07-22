import time

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class RateLimitMiddleware(BaseHTTPMiddleware):

    RATE_LIMIT = 100
    WINDOW = 60

    requests = {}

    async def dispatch(
        self,
        request: Request,
        call_next
    ):

        client = request.client.host

        now = time.time()

        if client not in self.requests:
            self.requests[client] = []

        self.requests[client] = [
            t
            for t in self.requests[client]
            if now - t < self.WINDOW
        ]

        if len(self.requests[client]) >= self.RATE_LIMIT:

            return JSONResponse(
                status_code=429,
                content={
                    "success": False,
                    "message": "Too many requests"
                }
            )

        self.requests[client].append(now)

        response = await call_next(request)

        return response