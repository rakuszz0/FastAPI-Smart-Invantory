from datetime import datetime

from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Payment(Base):

    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)

    transaction_id = Column(
        Integer,
        ForeignKey("transactions.id"),
        nullable=False,
    )

    amount = Column(Float, nullable=False)

    currency = Column(String(10), default="IDR")

    status = Column(String(50), default="pending")

    provider = Column(String(50), nullable=False)

    provider_payment_id = Column(String(255), nullable=True, index=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    transaction = relationship(
        "Transaction",
        back_populates="payments",
        uselist=False,
    )

    def __repr__(self):
        return f"<Payment(id={self.id} transaction_id={self.transaction_id} status={self.status})>"
