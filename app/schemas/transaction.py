from pydantic import BaseModel, ConfigDict
from typing import Optional


class TransactionBase(BaseModel):
    quantity: int
    product_id: int
    customer_id: int


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    quantity: Optional[int] = None
    total: Optional[float] = None
    product_id: Optional[int] = None
    customer_id: Optional[int] = None


class TransactionResponse(TransactionBase):
    id: int
    total: float

    model_config = ConfigDict(
        from_attributes=True
    )