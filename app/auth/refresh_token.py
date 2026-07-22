from app.core.security import (
    decode_access_token,
    create_access_token
)


class RefreshTokenService:

    def refresh(
        self,
        token: str
    ):

        payload = decode_access_token(
            token
        )

        if payload is None:

            return None

        return {

            "access_token": create_access_token(

                {

                    "sub": payload["sub"],

                    "email": payload["email"],

                    "fullname": payload["fullname"]

                }

            ),

            "token_type": "bearer"

        }


refresh_access_token = RefreshTokenService()