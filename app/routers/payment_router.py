import hashlib
import hmac
import json
import os
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.payment_service import PaymentService
from app.payments.midtrans_adapter import MidtransAdapter
from app.payments.doku_adapter import DokuAdapter
from app.repositories.payment_repository import PaymentRepository
from app.models.payment import Payment
from app.models.transaction import Transaction
from app.dependencies.auth import require_role


router = APIRouter()


class InitiatePaymentRequest(BaseModel):
    transaction_id: int
    provider: str = "midtrans"


class InitiatePaymentResponse(BaseModel):
    payment_id: int
    provider: str
    provider_response: dict


@router.post("/payments/initiate", response_model=InitiatePaymentResponse, tags=["Payments"])
def initiate_payment(req: InitiatePaymentRequest, db: Session = Depends(get_db)):

    # load transaction
    transaction = db.query(Transaction).filter(Transaction.id == req.transaction_id).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    payment_service = PaymentService()

    payment = payment_service.create_payment(db, transaction, amount=transaction.total or 0.0, provider=req.provider)

    if req.provider == "midtrans":
        adapter = MidtransAdapter()
    elif req.provider == "doku":
        adapter = DokuAdapter()
    else:
        raise HTTPException(status_code=400, detail="Unsupported provider")

    try:
        provider_resp = adapter.initiate_payment(transaction, payment)
    except Exception as e:
        payment_service.update_payment_status(db, payment, "failed")
        raise HTTPException(status_code=502, detail=str(e))

    provider_payment_id = provider_resp.get("order_id") or provider_resp.get("transaction_id") or provider_resp.get("va_number")
    if isinstance(provider_payment_id, dict):
        provider_payment_id = str(provider_payment_id)

    payment_service.update_payment_status(db, payment, "pending", provider_payment_id=provider_payment_id)

    return InitiatePaymentResponse(payment_id=payment.id, provider=req.provider, provider_response=provider_resp)


@router.post("/payments/webhook", tags=["Payments"])
async def payment_webhook(request: Request, db: Session = Depends(get_db)):

    raw_body = await request.body()
    try:
        payload = json.loads(raw_body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise HTTPException(status_code=400, detail="Payload must be valid JSON")

    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="Payload must be a JSON object")

    provider = payload.get("provider") or "midtrans"
    provider_payment_id = payload.get("provider_payment_id") or payload.get("transaction_id") or payload.get("order_id")
    status = payload.get("status")

    if not provider_payment_id:
        raise HTTPException(status_code=400, detail="Missing provider_payment_id")

    if not status:
        midtrans_status = payload.get("transaction_status")
        if midtrans_status in {"settlement", "capture"}:
            status = "paid"
        elif midtrans_status in {"deny", "cancel", "failure", "expire", "expired"}:
            status = "failed"
        else:
            status = midtrans_status

    if not status:
        raise HTTPException(status_code=400, detail="Missing status")

    secret = os.environ.get("PAYMENT_WEBHOOK_SECRET")
    signature = request.headers.get("X-Signature")
    if secret and signature:
        expected = hmac.new(secret.encode(), raw_body, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected, signature):
            raise HTTPException(status_code=401, detail="Invalid webhook signature")

    repo = PaymentRepository(Payment)
    payment = repo.get_by_provider_id(db, provider_payment_id)

    if not payment:
        payment = (
            db.query(Payment)
            .filter(Payment.provider == provider)
            .filter(Payment.status == "pending")
            .order_by(Payment.id.desc())
            .first()
        )

    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    if not payment.provider_payment_id:
        payment.provider_payment_id = provider_payment_id

    ps = PaymentService()
    ps.update_payment_status(db, payment, status, provider_payment_id=provider_payment_id)

    transaction = db.query(Transaction).filter(Transaction.id == payment.transaction_id).first()
    if transaction:
        ps.finalize_transaction_state(db, payment, transaction, status)

    return {"success": True}


@router.get("/admin/payments/", response_model=list[dict[str, Any]], tags=["Admin"])
def list_payments(
    db: Session = Depends(get_db),
    _ = Depends(require_role("admin")),
):
    payments = db.query(Payment).all()
    return [
        {
            "id": payment.id,
            "transaction_id": payment.transaction_id,
            "amount": payment.amount,
            "status": payment.status,
            "provider": payment.provider,
            "provider_payment_id": payment.provider_payment_id,
        }
        for payment in payments
    ]


@router.post("/admin/payments/{payment_id}/retry", tags=["Admin"])
def retry_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    _ = Depends(require_role("admin")),
):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    transaction = db.query(Transaction).filter(Transaction.id == payment.transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    if payment.provider == "midtrans":
        adapter = MidtransAdapter()
        response = adapter.initiate_payment(transaction, payment)
    elif payment.provider == "doku":
        adapter = DokuAdapter()
        response = adapter.initiate_payment(transaction, payment)
    else:
        raise HTTPException(status_code=400, detail="Unsupported provider")

    payment.status = "pending"
    transaction.status = "pending"
    db.commit()

    return {"success": True, "payment_id": payment.id, "provider_response": response}


@router.post("/admin/payments/{payment_id}/refund", tags=["Admin"])
def refund_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    _ = Depends(require_role("admin")),
):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    transaction = db.query(Transaction).filter(Transaction.id == payment.transaction_id).first()
    if transaction:
        transaction.status = "refunded"

    payment.status = "refunded"
    db.commit()

    return {"success": True, "payment_id": payment.id, "status": payment.status}


@router.post("/admin/payments/{payment_id}/cancel", tags=["Admin"])
def cancel_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    _ = Depends(require_role("admin")),
):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    transaction = db.query(Transaction).filter(Transaction.id == payment.transaction_id).first()
    if transaction:
        transaction.status = "canceled"

    payment.status = "canceled"
    db.commit()

    return {"success": True, "payment_id": payment.id, "status": payment.status}
