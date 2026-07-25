from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user import AdminUserUpdate, UserResponse
from app.dependencies.auth import require_role
from app.core.security import hash_password
from app.utils.enums import UserRole


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/users/", response_model=List[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    _ = Depends(require_role(UserRole.ADMIN.value, UserRole.SUPER_ADMIN.value)),
):

    return UserRepository.get_all(db)


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user_profile(
    user_id: int,
    payload: AdminUserUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(
        require_role(UserRole.ADMIN.value, UserRole.SUPER_ADMIN.value)
    ),
):
    """Update a staff/user profile and, when allowed, its role."""

    user = UserRepository.get_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    manageable_roles = {UserRole.STAFF.value, UserRole.USER.value}
    if current_user.role == UserRole.SUPER_ADMIN.value:
        manageable_roles.add(UserRole.ADMIN.value)

    if user.role not in manageable_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot edit this user",
        )

    if payload.role is not None:
        allowed_new_roles = {UserRole.STAFF, UserRole.USER}
        if current_user.role == UserRole.SUPER_ADMIN.value:
            allowed_new_roles.add(UserRole.ADMIN)

        if payload.role not in allowed_new_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot assign this role",
            )

        user.role = payload.role.value

    _apply_profile_changes(db, user, payload)
    return UserRepository.update(db, user)


def _apply_profile_changes(db: Session, user, payload: AdminUserUpdate):
    if payload.email is not None and payload.email != user.email:
        existing_user = UserRepository.get_by_email(db, payload.email)
        if existing_user is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already in use",
            )
        user.email = payload.email

    if payload.fullname is not None:
        user.fullname = payload.fullname

    if payload.password is not None:
        user.password = hash_password(payload.password)
