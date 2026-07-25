from app.repositories.base_repository import BaseRepository


class PaymentRepository(BaseRepository):

    def __init__(self, model):
        super().__init__(model)

    def get_by_provider_id(self, db, provider_payment_id: str):

        return (
            db.query(self.model)
            .filter(self.model.provider_payment_id == provider_payment_id)
            .first()
        )
