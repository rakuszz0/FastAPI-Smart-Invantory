from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.supplier import Supplier
from app.schemas.supplier import (
    SupplierCreate,
    SupplierUpdate
)


class SupplierService:

    @staticmethod
    def get_all(db: Session):
        return db.query(Supplier).all()

    @staticmethod
    def get_by_id(
        db: Session,
        supplier_id: int
    ):

        supplier = db.query(Supplier).filter(
            Supplier.id == supplier_id
        ).first()

        if not supplier:
            raise HTTPException(
                status_code=404,
                detail="Supplier not found"
            )

        return supplier

    @staticmethod
    def create(
        db: Session,
        payload: SupplierCreate
    ):

        supplier = Supplier(
            company_name=payload.company_name,
            email=payload.email,
            phone=payload.phone,
            address=payload.address
        )

        db.add(supplier)
        db.commit()
        db.refresh(supplier)

        return supplier

    @staticmethod
    def update(
        db: Session,
        supplier_id: int,
        payload: SupplierUpdate
    ):

        supplier = db.query(Supplier).filter(
            Supplier.id == supplier_id
        ).first()

        if not supplier:
            raise HTTPException(
                status_code=404,
                detail="Supplier not found"
            )

        update_data = payload.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(supplier, key, value)

        db.commit()
        db.refresh(supplier)

        return supplier

    @staticmethod
    def delete(
        db: Session,
        supplier_id: int
    ):

        supplier = db.query(Supplier).filter(
            Supplier.id == supplier_id
        ).first()

        if not supplier:
            raise HTTPException(
                status_code=404,
                detail="Supplier not found"
            )

        db.delete(supplier)
        db.commit()

        return {
            "message": "Supplier deleted successfully"
        }