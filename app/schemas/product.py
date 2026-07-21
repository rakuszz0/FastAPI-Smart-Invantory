from pydantic import BaseModel, ConfigDict
from typing import Optional


class ProductBase(BaseModel):
    name: str
    category: str
    stock: int
    price: float
    supplier_id: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    stock: Optional[int] = None
    price: Optional[float] = None
    supplier_id: Optional[int] = None


class ProductResponse(ProductBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )