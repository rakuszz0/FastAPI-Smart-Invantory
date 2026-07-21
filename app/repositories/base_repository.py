from typing import Generic, TypeVar, Type, Optional

from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):

    def __init__(
        self,
        model: Type[ModelType]
    ):
        self.model = model

    def get_all(
        self,
        db: Session
    ):

        return db.query(self.model).all()

    def get_by_id(
        self,
        db: Session,
        object_id: int
    ):

        return (
            db.query(self.model)
            .filter(self.model.id == object_id)
            .first()
        )

    def create(
        self,
        db: Session,
        obj: ModelType
    ):

        db.add(obj)
        db.commit()
        db.refresh(obj)

        return obj

    def update(
        self,
        db: Session,
        obj: ModelType
    ):

        db.commit()
        db.refresh(obj)

        return obj

    def delete(
        self,
        db: Session,
        obj: ModelType
    ):

        db.delete(obj)
        db.commit()

        return True

    def exists(
        self,
        db: Session,
        object_id: int
    ):

        return (
            db.query(self.model)
            .filter(self.model.id == object_id)
            .first()
            is not None
        )

    def count(
        self,
        db: Session
    ):

        return db.query(self.model).count()