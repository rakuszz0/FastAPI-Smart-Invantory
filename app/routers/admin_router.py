from typing import List

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserResponse
from app.dependencies.auth import require_role


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/users/", response_model=List[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    _ = Depends(require_role("admin")),
):

    return UserRepository.get_all(db)
