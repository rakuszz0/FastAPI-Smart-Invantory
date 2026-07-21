from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional


class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    phone: str


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class CustomerResponse(CustomerBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )