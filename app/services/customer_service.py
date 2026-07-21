from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.customer import Customer
from app.schemas.customer import (
    CustomerCreate,
    CustomerUpdate
)


class CustomerService:

    @staticmethod
    def get_all(db: Session):
        return db.query(Customer).all()

    @staticmethod
    def get_by_id(
        db: Session,
        customer_id: int
    ):

        customer = db.query(Customer).filter(
            Customer.id == customer_id
        ).first()

        if not customer:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        return customer

    @staticmethod
    def create(
        db: Session,
        payload: CustomerCreate
    ):

        customer = Customer(
            name=payload.name,
            email=payload.email,
            phone=payload.phone
        )

        db.add(customer)
        db.commit()
        db.refresh(customer)

        return customer

    @staticmethod
    def update(
        db: Session,
        customer_id: int,
        payload: CustomerUpdate
    ):

        customer = db.query(Customer).filter(
            Customer.id == customer_id
        ).first()

        if not customer:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        update_data = payload.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(customer, key, value)

        db.commit()
        db.refresh(customer)

        return customer

    @staticmethod
    def delete(
        db: Session,
        customer_id: int
    ):

        customer = db.query(Customer).filter(
            Customer.id == customer_id
        ).first()

        if not customer:
            raise HTTPException(
                status_code=404,
                detail="Customer not found"
            )

        db.delete(customer)
        db.commit()

        return {
            "message": "Customer deleted successfully"
        }