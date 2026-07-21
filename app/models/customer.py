from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import relationship

from app.core.database import Base


class Customer(Base):

    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)

    name = Column(String(150))

    email = Column(String(150))

    phone = Column(String(50))

    transactions = relationship(
        "Transaction",
        back_populates="customer"
    )