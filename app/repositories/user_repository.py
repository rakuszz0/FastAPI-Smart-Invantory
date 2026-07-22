from typing import Optional

from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:

    @staticmethod
    def get_all(db: Session):

        return db.query(User).all()

    @staticmethod
    def get_by_id(
        db: Session,
        user_id: int
    ) -> Optional[User]:

        return (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    @staticmethod
    def get_by_email(
        db: Session,
        email: str
    ) -> Optional[User]:

        return (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

    @staticmethod
    def create(
        db: Session,
        user: User
    ) -> User:

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def update(
        db: Session,
        user: User
    ) -> User:

        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def delete(
        db: Session,
        user: User
    ):

        db.delete(user)
        db.commit()

        return True

    @staticmethod
    def exists_by_email(
        db: Session,
        email: str
    ) -> bool:

        return (
            db.query(User)
            .filter(User.email == email)
            .first()
            is not None
        )

    @staticmethod
    def exists_by_id(
        db: Session,
        user_id: int
    ) -> bool:

        return (
            db.query(User)
            .filter(User.id == user_id)
            .first()
            is not None
        )