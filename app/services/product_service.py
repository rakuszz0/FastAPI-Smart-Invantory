from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.product import Product
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
)

from app.repositories.product_repository import ProductRepository
from app.repositories.supplier_repository import SupplierRepository


class ProductService:

    def __init__(self):
        self.product_repo = ProductRepository()
        self.supplier_repo = SupplierRepository()

    def get_all(
        self,
        db: Session
    ):
        return self.product_repo.get_all(db)

    def get_by_id(
        self,
        db: Session,
        product_id: int
    ):

        product = self.product_repo.get_by_id(
            db,
            product_id
        )

        if product is None:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        return product

    def create(
        self,
        db: Session,
        payload: ProductCreate
    ):

        supplier = self.supplier_repo.get_by_id(
            db,
            payload.supplier_id
        )

        if supplier is None:
            raise HTTPException(
                status_code=404,
                detail="Supplier not found"
            )

        product = Product(
            name=payload.name,
            category=payload.category,
            stock=payload.stock,
            price=payload.price,
            supplier_id=payload.supplier_id
        )

        return self.product_repo.create(
            db,
            product
        )

    def update(
        self,
        db: Session,
        product_id: int,
        payload: ProductUpdate
    ):

        product = self.product_repo.get_by_id(
            db,
            product_id
        )

        if product is None:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        update_data = payload.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(product, key, value)

        return self.product_repo.update(
            db,
            product
        )

    def delete(
        self,
        db: Session,
        product_id: int
    ):

        product = self.product_repo.get_by_id(
            db,
            product_id
        )

        if product is None:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        self.product_repo.delete(
            db,
            product
        )

        return {
            "message": "Product deleted successfully"
        }

    def search(
        self,
        db: Session,
        keyword: str
    ):

        return self.product_repo.search(
            db,
            keyword
        )

    def low_stock(
        self,
        db: Session,
        minimum_stock: int = 10
    ):

        return self.product_repo.get_low_stock(
            db,
            minimum_stock
        )