import hashlib
import hmac
import json
import os
import uuid

from app.models.transaction import Transaction
from app.models.product import Product
from app.models.customer import Customer
from app.models.payment import Payment
from app.models.user import User
from app.core.security import create_access_token, hash_password
from app.services.payment_service import PaymentService


def test_initiate_payment_client_side(monkeypatch, client):

    # create a transaction directly in DB to reference
    from app.core import database as _database
    session = _database.SessionLocal()

    product = session.query(Product).first()
    customer = session.query(Customer).first()

    txn = Transaction(quantity=1, total=product.price, product_id=product.id, customer_id=customer.id)
    session.add(txn)
    session.commit()
    session.refresh(txn)

    # mock MidtransAdapter.initiate_payment to avoid external HTTP call
    class DummyResp(dict):
        pass

    def fake_initiate(self, transaction, payment):
        return {"order_id": f"txn-{transaction.id}", "va_numbers": [{"bank": "bca", "va_number": "1234567890"}]}

    monkeypatch.setattr("app.payments.midtrans_adapter.MidtransAdapter.initiate_payment", fake_initiate)

    payload = {"transaction_id": txn.id, "provider": "midtrans"}

    resp = client.post("/api/v1/payments/initiate", json=payload)

    assert resp.status_code == 200
    data = resp.json()
    assert data["provider"] == "midtrans"
    assert "payment_id" in data


def test_webhook_paid_marks_transaction_completed(client, monkeypatch):
    from app.core import database as _database

    session = _database.SessionLocal()
    product = session.query(Product).first()
    customer = session.query(Customer).first()

    txn = Transaction(quantity=1, total=product.price, product_id=product.id, customer_id=customer.id)
    session.add(txn)
    session.commit()
    session.refresh(txn)

    payment = PaymentService().create_payment(session, txn, amount=txn.total or 0.0, provider="midtrans")
    session.commit()

    monkeypatch.setenv("PAYMENT_WEBHOOK_SECRET", "test-secret")
    payload = {"provider": "midtrans", "provider_payment_id": "order-1", "status": "paid"}
    body = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
    signature = hmac.new(b"test-secret", body, hashlib.sha256).hexdigest()

    resp = client.post(
        "/api/v1/payments/webhook",
        content=body,
        headers={"content-type": "application/json", "X-Signature": signature},
    )

    assert resp.status_code == 200
    session.refresh(txn)
    session.refresh(payment)
    assert txn.status == "completed"
    assert payment.status == "paid"


def test_midtrans_style_webhook_payload_is_mapped_to_internal_status(client, monkeypatch):
    from app.core import database as _database

    session = _database.SessionLocal()
    product = session.query(Product).first()
    customer = session.query(Customer).first()

    txn = Transaction(quantity=1, total=product.price, product_id=product.id, customer_id=customer.id)
    session.add(txn)
    session.commit()
    session.refresh(txn)

    payment = PaymentService().create_payment(session, txn, amount=txn.total or 0.0, provider="midtrans")
    session.commit()

    monkeypatch.setenv("PAYMENT_WEBHOOK_SECRET", "test-secret")
    payload = {
        "transaction_time": "2026-07-26 10:00:00",
        "transaction_status": "settlement",
        "transaction_id": "midtrans-sandbox-001",
        "order_id": f"txn-{txn.id}",
        "gross_amount": "10000.00",
        "currency": "IDR",
        "fraud_status": "accept",
        "payment_type": "bank_transfer",
        "status_code": "200",
        "status_message": "midtrans payment notification",
    }
    body = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
    signature = hmac.new(b"test-secret", body, hashlib.sha256).hexdigest()

    resp = client.post(
        "/api/v1/payments/webhook",
        content=body,
        headers={"content-type": "application/json", "X-Signature": signature},
    )

    assert resp.status_code == 200
    session.refresh(txn)
    session.refresh(payment)
    assert txn.status == "completed"
    assert payment.status == "paid"


def test_admin_can_list_and_retry_payments(client, monkeypatch):
    from app.core import database as _database

    session = _database.SessionLocal()
    product = session.query(Product).first()
    customer = session.query(Customer).first()

    txn = Transaction(quantity=1, total=product.price, product_id=product.id, customer_id=customer.id)
    session.add(txn)
    session.commit()
    session.refresh(txn)

    payment = PaymentService().create_payment(session, txn, amount=txn.total or 0.0, provider="midtrans")
    session.commit()

    admin = User(
        fullname="Admin User",
        email=f"admin-{uuid.uuid4().hex[:8]}@example.com",
        password=hash_password("password"),
        role="admin",
    )
    session.add(admin)
    session.commit()
    session.refresh(admin)

    token = create_access_token({"sub": str(admin.id)})

    def fake_initiate(self, transaction, payment):
        return {"order_id": f"txn-{transaction.id}", "va_numbers": [{"bank": "bca", "va_number": "1234567890"}]}

    monkeypatch.setattr("app.payments.midtrans_adapter.MidtransAdapter.initiate_payment", fake_initiate)

    list_resp = client.get("/api/v1/admin/payments/", headers={"Authorization": f"Bearer {token}"})
    assert list_resp.status_code == 200
    assert len(list_resp.json()) >= 1

    retry_resp = client.post(
        f"/api/v1/admin/payments/{payment.id}/retry",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert retry_resp.status_code == 200
    data = retry_resp.json()
    assert data["payment_id"] == payment.id


def test_webhook_failed_and_expired_transitions(client, monkeypatch):
    from app.core import database as _database

    session = _database.SessionLocal()
    product = session.query(Product).first()
    customer = session.query(Customer).first()

    for status, expected_txn_status in (("failed", "failed"), ("expired", "expired")):
        txn = Transaction(quantity=1, total=product.price, product_id=product.id, customer_id=customer.id)
        session.add(txn)
        session.commit()
        session.refresh(txn)

        payment = PaymentService().create_payment(session, txn, amount=txn.total or 0.0, provider="midtrans")
        session.commit()

        monkeypatch.setenv("PAYMENT_WEBHOOK_SECRET", "test-secret")
        payload = {"provider": "midtrans", "provider_payment_id": f"order-{txn.id}", "status": status}
        body = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
        signature = hmac.new(b"test-secret", body, hashlib.sha256).hexdigest()

        resp = client.post(
            "/api/v1/payments/webhook",
            content=body,
            headers={"content-type": "application/json", "X-Signature": signature},
        )

        assert resp.status_code == 200
        session.refresh(txn)
        session.refresh(payment)
        assert txn.status == expected_txn_status
        assert payment.status == status


def test_admin_can_refund_and_cancel_payment(client, monkeypatch):
    from app.core import database as _database

    session = _database.SessionLocal()
    product = session.query(Product).first()
    customer = session.query(Customer).first()

    admin = User(
        fullname="Admin User",
        email=f"admin-{uuid.uuid4().hex[:8]}@example.com",
        password=hash_password("password"),
        role="admin",
    )
    session.add(admin)
    session.commit()
    session.refresh(admin)

    token = create_access_token({"sub": str(admin.id)})

    txn = Transaction(quantity=1, total=product.price, product_id=product.id, customer_id=customer.id)
    session.add(txn)
    session.commit()
    session.refresh(txn)

    payment = PaymentService().create_payment(session, txn, amount=txn.total or 0.0, provider="midtrans")
    payment.status = "paid"
    txn.status = "completed"
    session.commit()
    session.refresh(payment)
    session.refresh(txn)

    refund_resp = client.post(
        f"/api/v1/admin/payments/{payment.id}/refund",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert refund_resp.status_code == 200
    session.refresh(payment)
    session.refresh(txn)
    assert payment.status == "refunded"
    assert txn.status == "refunded"

    txn2 = Transaction(quantity=1, total=product.price, product_id=product.id, customer_id=customer.id)
    session.add(txn2)
    session.commit()
    session.refresh(txn2)

    payment2 = PaymentService().create_payment(session, txn2, amount=txn2.total or 0.0, provider="midtrans")
    payment2.status = "pending"
    txn2.status = "pending"
    session.commit()
    session.refresh(payment2)
    session.refresh(txn2)

    cancel_resp = client.post(
        f"/api/v1/admin/payments/{payment2.id}/cancel",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert cancel_resp.status_code == 200
    session.refresh(payment2)
    session.refresh(txn2)
    assert payment2.status == "canceled"
    assert txn2.status == "canceled"
