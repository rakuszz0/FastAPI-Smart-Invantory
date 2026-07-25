import uuid

from sqlalchemy.orm import Session

from app.core import database as _database
from app.core.security import create_access_token, hash_password
from app.models.user import User


def _user_with_token(db: Session, role: str) -> tuple[User, str]:
    unique = uuid.uuid4().hex[:8]
    user = User(
        fullname=f"{role} account",
        email=f"{role}.{unique}@example.com",
        password=hash_password("Password123"),
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user, create_access_token({"sub": str(user.id)})


def test_regular_user_can_only_update_own_profile(client):
    db = Session(bind=_database.engine)
    user, token = _user_with_token(db, "user")
    other_user, _ = _user_with_token(db, "user")

    response = client.put(
        "/api/v1/auth/me",
        json={"fullname": "Updated Regular User"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["fullname"] == "Updated Regular User"
    assert response.json()["role"] == "user"

    forbidden = client.put(
        f"/api/v1/users/{other_user.id}",
        json={"fullname": "Not Allowed"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert forbidden.status_code == 403
    db.close()


def test_staff_can_edit_user_profile_but_not_role(client):
    db = Session(bind=_database.engine)
    _, staff_token = _user_with_token(db, "staff")
    user, _ = _user_with_token(db, "user")

    response = client.put(
        f"/api/v1/users/{user.id}",
        json={"fullname": "Updated By Staff"},
        headers={"Authorization": f"Bearer {staff_token}"},
    )
    assert response.status_code == 200
    assert response.json()["fullname"] == "Updated By Staff"
    assert response.json()["role"] == "user"
    db.close()


def test_admin_can_edit_staff_and_change_role(client):
    db = Session(bind=_database.engine)
    _, admin_token = _user_with_token(db, "admin")
    staff, _ = _user_with_token(db, "staff")

    response = client.put(
        f"/api/v1/admin/users/{staff.id}",
        json={"fullname": "Updated Staff", "role": "user"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    assert response.json()["fullname"] == "Updated Staff"
    assert response.json()["role"] == "user"
    db.close()


def test_registration_always_creates_regular_user(client):
    unique = uuid.uuid4().hex[:8]
    response = client.post(
        "/api/v1/auth/register",
        json={
            "fullname": "New Regular User",
            "email": f"register.{unique}@example.com",
            "password": "Password123",
            "role": "admin",
        },
    )
    assert response.status_code == 201
    assert response.json()["role"] == "user"
