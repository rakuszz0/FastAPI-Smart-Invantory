from typing import List

from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.transaction import (
    TransactionCreate,
    TransactionResponse,
)

from app.services.transaction_service import TransactionService


router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)


@router.get("/", response_model=List[TransactionResponse])
def get_transactions(
    db: Session = Depends(get_db),
    service: TransactionService = Depends(TransactionService),
):

    return service.get_all(db)


@router.post("/", response_model=TransactionResponse)
def create_transaction(
    payload: TransactionCreate,
    db: Session = Depends(get_db),
    service: TransactionService = Depends(TransactionService),
):

    return service.create(db, payload)
