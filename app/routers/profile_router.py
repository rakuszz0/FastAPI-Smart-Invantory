from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import hash_password
from app.dependencies.auth import get_current_user, require_role
from app.repositories.user_repository import UserRepository
from app.schemas.user import ProfileUpdate, UserResponse
from app.utils.enums import UserRole


router = APIRouter(tags=["Profile"])


@router.put("/auth/me", response_model=UserResponse)
def update_my_profile(
    payload: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """All authenticated users may update their own profile, never their role."""
    _apply_profile_changes(db, current_user, payload)
    return UserRepository.update(db, current_user)


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user_profile_as_staff(
    user_id: int,
    payload: ProfileUpdate,
    db: Session = Depends(get_db),
    _ = Depends(require_role(UserRole.STAFF.value)),
):
    """Staff may update only regular-user profiles and cannot change roles."""
    user = UserRepository.get_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if user.role != UserRole.USER.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Staff can only edit user profiles",
        )

    _apply_profile_changes(db, user, payload)
    return UserRepository.update(db, user)


def _apply_profile_changes(db: Session, user, payload: ProfileUpdate):
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
