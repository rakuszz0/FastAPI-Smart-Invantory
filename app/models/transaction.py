from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import String

from sqlalchemy.orm import relationship

from app.core.database import Base


class Transaction(Base):

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)

    quantity = Column(Integer)

    total = Column(Float)

    status = Column(String(50), default="pending", nullable=False)

    product_id = Column(
        Integer,
        ForeignKey("products.id")
    )

    customer_id = Column(
        Integer,
        ForeignKey("customers.id")
    )

    product = relationship(
        "Product",
        back_populates="transactions"
    )

    customer = relationship(
        "Customer",
        back_populates="transactions"
    )


# Backref for payments
Transaction.payments = relationship("Payment", back_populates="transaction")