from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional


class SupplierBase(BaseModel):
    company_name: str
    email: EmailStr
    phone: str
    address: str


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(BaseModel):
    company_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class SupplierResponse(SupplierBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )