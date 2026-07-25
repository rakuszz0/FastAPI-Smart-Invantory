from app.core.security import create_access_token, hash_password
from app.models.user import User
from app.core import database as _database
from sqlalchemy.orm import Session
import uuid


def make_token_for_role(db: Session, role: str):
    # create user directly and return token
    unique = uuid.uuid4().hex[:8]
    user = User(
        fullname=f"{role} user",
        email=f"{role}+{unique}@example.com",
        password=hash_password("password"),
        role=role
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": str(user.id)})

    return token


def test_admin_only_endpoint_allows_admin(client):
    # prepare DB and tokens
    db = Session(bind=_database.engine)
    admin_token = make_token_for_role(db, "admin")
    staff_token = make_token_for_role(db, "staff")
    user_token = make_token_for_role(db, "user")

    # admin should access
    resp = client.get(
        "/api/v1/admin/users/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert resp.status_code == 200

    # staff should be forbidden
    resp2 = client.get(
        "/api/v1/admin/users/",
        headers={"Authorization": f"Bearer {staff_token}"}
    )
    assert resp2.status_code == 403

    # unauthenticated should be 401
    resp3 = client.get(
        "/api/v1/admin/users/"
    )
    assert resp3.status_code == 401

    db.close()
