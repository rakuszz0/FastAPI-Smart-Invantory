from sqlalchemy.orm import Session

from app.models.supplier import Supplier
from app.repositories.base_repository import BaseRepository


class SupplierRepository(BaseRepository[Supplier]):

    def __init__(self):
        super().__init__(Supplier)

    def get_by_email(
        self,
        db: Session,
        email: str
    ):

        return (
            db.query(Supplier)
            .filter(
                Supplier.email == email
            )
            .first()
        )

    def search(
        self,
        db: Session,
        keyword: str
    ):

        return (
            db.query(Supplier)
            .filter(
                Supplier.company_name.ilike(
                    f"%{keyword}%"
                )
            )
            .all()
        )