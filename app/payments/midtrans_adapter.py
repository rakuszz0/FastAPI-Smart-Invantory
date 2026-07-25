import base64

from app.core.config import settings

MIDTRANS_BASE = settings.MIDTRANS_BASE or "https://api.sandbox.midtrans.com"


class MidtransAdapter:

    def __init__(self, server_key: str | None = None):
        self.server_key = server_key or settings.MIDTRANS_SERVER_KEY

    def _auth_header(self):
        if not self.server_key:
            raise RuntimeError("MIDTRANS_SERVER_KEY not configured")

        token = base64.b64encode(f"{self.server_key}:".encode()).decode()

        return {"Authorization": f"Basic {token}", "Accept": "application/json"}

    def initiate_payment(self, transaction, payment):
        """Call Midtrans charge API and return a redirect URL or token.

        This implementation targets the sandbox /charge endpoint.
        """

        # import httpx lazily so tests that mock this method don't require httpx installed
        import httpx

        url = f"{MIDTRANS_BASE}/v2/charge"

        payload = {
            "payment_type": "bank_transfer",
            "transaction_details": {
                "order_id": f"txn-{transaction.id}",
                "gross_amount": int(payment.amount)
            },
            "bank_transfer": {
                "bank": "bca"
            }
        }

        headers = self._auth_header()

        resp = httpx.post(url, json=payload, headers=headers, timeout=10.0)

        resp.raise_for_status()

        data = resp.json()

        # midtrans returns va_numbers or redirect_url depending on payment type
        return data
