from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
)


# =====================================
# Base
# =====================================

class UserBase(BaseModel):

    fullname: str = Field(
        ...,
        min_length=3,
        max_length=150,
    )

    email: EmailStr


# =====================================
# Register
# =====================================

class UserRegister(UserBase):

    password: str = Field(
        ...,
        min_length=6,
        max_length=100,
    )


# =====================================
# Login
# =====================================

class UserLogin(BaseModel):

    email: EmailStr

    password: str


# =====================================
# Update
# =====================================

class UserUpdate(BaseModel):

    fullname: Optional[str] = None

    password: Optional[str] = None

    role: Optional[str] = None

    is_active: Optional[bool] = None


# =====================================
# Response
# =====================================

class UserResponse(UserBase):

    id: int

    role: str

    is_active: bool

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =====================================
# JWT Response
# =====================================

class Token(BaseModel):

    access_token: str

    token_type: str = "bearer"


class TokenData(BaseModel):

    user_id: Optional[int] = None

    email: Optional[str] = None


# =====================================
# Login Response
# =====================================

class LoginResponse(BaseModel):

    access_token: str

    token_type: str

    user: UserResponse