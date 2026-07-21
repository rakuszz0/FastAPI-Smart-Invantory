from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.transaction import Transaction
from app.repositories.base_repository import BaseRepository


class TransactionRepository(
    BaseRepository[Transaction]
):

    def __init__(self):
        super().__init__(Transaction)

    def latest(
        self,
        db: Session,
        limit: int = 10
    ):

        return (
            db.query(Transaction)
            .order_by(
                desc(Transaction.id)
            )
            .limit(limit)
            .all()
        )

    def get_by_customer(
        self,
        db: Session,
        customer_id: int
    ):

        return (
            db.query(Transaction)
            .filter(
                Transaction.customer_id == customer_id
            )
            .all()
        )

    def get_by_product(
        self,
        db: Session,
        product_id: int
    ):

        return (
            db.query(Transaction)
            .filter(
                Transaction.product_id == product_id
            )
            .all()
        )