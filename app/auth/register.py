from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserRegister

from app.repositories.user_repository import UserRepository

from app.core.security import hash_password
from app.utils.enums import UserRole

from app.exceptions.authentication import (
    UserAlreadyExistsException
)


class RegisterService:

    def __init__(self):

        self.user_repo = UserRepository()

    def register(
        self,
        db: Session,
        payload: UserRegister
    ):

        user = self.user_repo.get_by_email(
            db,
            payload.email
        )

        if user:

            raise UserAlreadyExistsException()

        new_user = User(

            fullname=payload.fullname,

            email=payload.email,

            password=hash_password(
                payload.password
            ),

            # Public registration must never create a privileged account.
            role=UserRole.USER.value,

        )

        return self.user_repo.create(
            db,
            new_user
        )


register = RegisterService()
