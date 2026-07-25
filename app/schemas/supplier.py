from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional


class SupplierBase(BaseModel):
    # accept 'name' as an alias for company_name to match tests
    company_name: str = Field(..., alias="name")
    email: Optional[EmailStr] = None
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
        from_attributes=True,
        populate_by_name=True
    )