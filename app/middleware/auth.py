from fastapi import Request
from fastapi.responses import JSONResponse

from jose import JWTError

from app.core.security import decode_access_token


class AuthMiddleware:

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):

        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive)

        public_paths = {
            "/",
            "/docs",
            "/redoc",
            "/openapi.json",
            "/auth/login",
            "/auth/register"
        }

        if request.url.path in public_paths:
            await self.app(scope, receive, send)
            return

        authorization = request.headers.get("Authorization")

        if authorization is None:

            response = JSONResponse(
                status_code=401,
                content={
                    "success": False,
                    "message": "Authorization header missing"
                }
            )

            await response(scope, receive, send)
            return

        if not authorization.startswith("Bearer "):

            response = JSONResponse(
                status_code=401,
                content={
                    "success": False,
                    "message": "Invalid token format"
                }
            )

            await response(scope, receive, send)
            return

        token = authorization.replace(
            "Bearer ",
            ""
        )

        try:

            payload = decode_access_token(token)

            if payload is None:

                response = JSONResponse(
                    status_code=401,
                    content={
                        "success": False,
                        "message": "Invalid token"
                    }
                )

                await response(scope, receive, send)
                return

            scope["user"] = payload

        except JWTError:

            response = JSONResponse(
                status_code=401,
                content={
                    "success": False,
                    "message": "Token expired or invalid"
                }
            )

            await response(scope, receive, send)
            return

        await self.app(scope, receive, send)