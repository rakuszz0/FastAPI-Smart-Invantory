from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository

from app.schemas.user import UserLogin

from app.core.security import (
    verify_password,
    create_access_token
)

from app.exceptions.authentication import (
    InvalidCredentialException
)


class LoginService:

    def __init__(self):

        self.user_repo = UserRepository()

    def login(
        self,
        db: Session,
        payload: UserLogin
    ):

        user = self.user_repo.get_by_email(
            db,
            payload.email
        )

        if user is None:

            raise InvalidCredentialException()

        if not verify_password(
            payload.password,
            user.password
        ):

            raise InvalidCredentialException()

        token = create_access_token(

            {

                "sub": str(user.id),

                "email": user.email,

                "fullname": user.fullname

            }

        )

        return {

            "access_token": token,

            "token_type": "bearer",

            "user": user

        }


login = LoginService()