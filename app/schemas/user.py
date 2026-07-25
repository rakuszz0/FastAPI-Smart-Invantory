from datetime import date, datetime
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    model_validator,
)

from app.utils.enums import UserRole


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

    confirm_password: str = Field(
        ...,
        min_length=6,
        max_length=100,
    )

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Password confirmation does not match")
        return self


# =====================================
# Login
# =====================================

class UserLogin(BaseModel):

    email: EmailStr

    password: str


# =====================================
# Update
# =====================================

class ProfileUpdate(BaseModel):

    fullname: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=150,
    )

    email: Optional[EmailStr] = None

    password: Optional[str] = Field(
        default=None,
        min_length=6,
        max_length=100,
    )

    phone: Optional[str] = Field(
        default=None,
        min_length=8,
        max_length=30,
    )

    address: Optional[str] = Field(
        default=None,
        min_length=5,
        max_length=255,
    )

    date_of_birth: Optional[date] = None

    gender: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=20,
    )


class AdminUserUpdate(ProfileUpdate):

    role: Optional[UserRole] = None



# Backward-compatible name for callers that already import UserUpdate.
UserUpdate = AdminUserUpdate


# =====================================
# Response
# =====================================

class UserResponse(UserBase):

    id: int

    role: str

    is_active: bool

    phone: Optional[str] = None

    address: Optional[str] = None

    date_of_birth: Optional[date] = None

    gender: Optional[str] = None

    profile_is_complete: bool

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
