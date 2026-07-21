from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import relationship

from app.core.database import Base


class Supplier(Base):

    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)

    company_name = Column(String(150), nullable=False)

    email = Column(String(100), unique=True)

    phone = Column(String(30))

    address = Column(String(255))

    products = relationship(
        "Product",
        back_populates="supplier"
    )