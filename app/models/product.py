from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship

from app.core.database import Base


class Product(Base):

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False)

    category = Column(String(100))

    stock = Column(Integer, default=0)

    price = Column(Float)

    supplier_id = Column(
        Integer,
        ForeignKey("suppliers.id")
    )

    supplier = relationship(
        "Supplier",
        back_populates="products"
    )

    transactions = relationship(
        "Transaction",
        back_populates="product"
    )