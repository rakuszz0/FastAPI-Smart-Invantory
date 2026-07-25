import os


class DokuAdapter:
    def __init__(self, client_id: str | None = None):
        self.client_id = client_id or os.environ.get("DOKU_CLIENT_ID")

    def initiate_payment(self, transaction, payment):
        if not self.client_id:
            raise RuntimeError("DOKU_CLIENT_ID not configured")

        return {
            "client_id": self.client_id,
            "order_id": f"doku-{transaction.id}",
            "amount": int(payment.amount),
            "currency": payment.currency or "IDR",
            "redirect_url": "https://sandbox.doku.com/checkout",
            "payload_example": {
                "order": {
                    "invoice_number": f"INV-{transaction.id}",
                    "amount": int(payment.amount),
                    "currency": payment.currency or "IDR"
                },
                "customer": {
                    "id": transaction.customer_id,
                    "name": "Customer"
                }
            }
        }
