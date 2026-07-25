from typing import Any

from app.repositories.payment_repository import PaymentRepository
from app.models.payment import Payment


class PaymentService:

    def __init__(self, repository: PaymentRepository | None = None):
        self.repo = repository or PaymentRepository(Payment)

    def create_payment(self, db, transaction, amount: float, provider: str) -> Payment:

        payment = Payment(
            transaction_id=transaction.id,
            amount=amount,
            provider=provider,
            status="pending"
        )

        return self.repo.create(db, payment)

    def update_payment_status(self, db, payment: Payment, status: str, provider_payment_id: str | None = None):

        payment.status = status
        if provider_payment_id:
            payment.provider_payment_id = provider_payment_id

        return self.repo.update(db, payment)

    def finalize_transaction_state(self, db, payment: Payment, transaction, status: str):
        if status == "paid":
            transaction.status = "completed"
        elif status in {"failed", "expired", "canceled", "refunded"}:
            transaction.status = status
        db.commit()
        return transaction
