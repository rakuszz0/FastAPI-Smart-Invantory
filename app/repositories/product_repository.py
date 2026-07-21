from sqlalchemy.orm import Session

from app.models.product import Product
from app.repositories.base_repository import BaseRepository


class ProductRepository(BaseRepository[Product]):

    def __init__(self):
        super().__init__(Product)

    def search(
        self,
        db: Session,
        keyword: str
    ):

        return (
            db.query(Product)
            .filter(
                Product.name.ilike(f"%{keyword}%")
            )
            .all()
        )

    def get_low_stock(
        self,
        db: Session,
        minimum_stock: int = 10
    ):

        return (
            db.query(Product)
            .filter(Product.stock <= minimum_stock)
            .all()
        )

    def get_by_supplier(
        self,
        db: Session,
        supplier_id: int
    ):

        return (
            db.query(Product)
            .filter(
                Product.supplier_id == supplier_id
            )
            .all()
        )