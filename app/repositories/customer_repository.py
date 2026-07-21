from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.repositories.base_repository import BaseRepository


class CustomerRepository(BaseRepository[Customer]):

    def __init__(self):
        super().__init__(Customer)

    def get_by_email(
        self,
        db: Session,
        email: str
    ):

        return (
            db.query(Customer)
            .filter(
                Customer.email == email
            )
            .first()
        )

    def search(
        self,
        db: Session,
        keyword: str
    ):

        return (
            db.query(Customer)
            .filter(
                Customer.name.ilike(
                    f"%{keyword}%"
                )
            )
            .all()
        )