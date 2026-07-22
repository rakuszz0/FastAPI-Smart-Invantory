from fastapi import APIRouter
from fastapi import Depends
from fastapi import Header

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.user import (
    UserRegister,
    UserLogin,
    UserResponse,
    LoginResponse,
    Token
)

from app.auth.register import register
from app.auth.login import login
from app.auth.refresh_token import refresh_access_token

from app.repositories.user_repository import UserRepository
from app.core.security import decode_access_token


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# ==========================================
# Register
# ==========================================

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201
)
def register_user(
    payload: UserRegister,
    db: Session = Depends(get_db),
):

    return register.register(
        db,
        payload
    )


# ==========================================
# Login
# ==========================================

@router.post(
    "/login",
    response_model=LoginResponse
)
def login_user(
    payload: UserLogin,
    db: Session = Depends(get_db),
):

    return login.login(
        db,
        payload
    )


# ==========================================
# Refresh Token
# ==========================================

@router.post(
    "/refresh",
    response_model=Token
)
def refresh_token(

    authorization: str = Header(...)

):

    token = authorization.replace(
        "Bearer ",
        ""
    )

    return refresh_access_token.refresh(
        token
    )


# ==========================================
# Current User
# ==========================================

@router.get(
    "/me",
    response_model=UserResponse
)
def get_current_user(

    authorization: str = Header(...),

    db: Session = Depends(get_db)

):

    token = authorization.replace(
        "Bearer ",
        ""
    )

    payload = decode_access_token(
        token
    )

    if payload is None:

        return None

    user = UserRepository.get_by_id(

        db,

        int(payload["sub"])

    )

    return user