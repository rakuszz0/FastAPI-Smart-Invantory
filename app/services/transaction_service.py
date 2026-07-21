from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.transaction import Transaction
from app.models.product import Product
from app.models.customer import Customer

from app.schemas.transaction import (
    TransactionCreate,
    TransactionUpdate
)


class TransactionService:

    @staticmethod
    def get_all(db: Session):
        return db.query(Transaction).all()

    @staticmethod
    def get_by_id(
        db: Session,
        transaction_id: int
    ):

        transaction = db.query(Transaction).filter(
            Transaction.id == transaction_id
        ).first()

        if not transaction:
            raise HTTPException(
                status_code=404,
                detail="Transaction not found"
            )

        return transaction

    @staticmethod
    def create(
        db: Session,
        payload: TransactionCreate
    ):

        product = db.query(Product).filter(
            Product.id == payload.product_id
        ).first()

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        customer = db.query(Customer).filter(
            Customer.id == payload.customer_id
        ).first()

        if not customer:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        if product.stock < payload.quantity:
            raise HTTPException(
                status_code=400,
                detail="Insufficient stock"
            )

        total = product.price * payload.quantity

        transaction = Transaction(
            quantity=payload.quantity,
            total=total,
            product_id=payload.product_id,
            customer_id=payload.customer_id
        )

        product.stock -= payload.quantity

        db.add(transaction)

        db.commit()

        db.refresh(transaction)

        return transaction

    @staticmethod
    def update(
        db: Session,
        transaction_id: int,
        payload: TransactionUpdate
    ):

        transaction = db.query(Transaction).filter(
            Transaction.id == transaction_id
        ).first()

        if not transaction:
            raise HTTPException(
                status_code=404,
                detail="Transaction not found"
            )

        update_data = payload.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(transaction, key, value)

        db.commit()

        db.refresh(transaction)

        return transaction

    @staticmethod
    def delete(
        db: Session,
        transaction_id: int
    ):

        transaction = db.query(Transaction).filter(
            Transaction.id == transaction_id
        ).first()

        if not transaction:
            raise HTTPException(
                status_code=404,
                detail="Transaction not found"
            )

        product = db.query(Product).filter(
            Product.id == transaction.product_id
        ).first()

        if product:
            product.stock += transaction.quantity

        db.delete(transaction)

        db.commit()

        return {
            "message": "Transaction deleted successfully"
        }