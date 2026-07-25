from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Integer,
    String,
)

from app.core.database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    fullname = Column(
        String(150),
        nullable=False,
    )

    email = Column(
        String(150),
        unique=True,
        nullable=False,
        index=True,
    )

    password = Column(
        String(255),
        nullable=False,
    )

    role = Column(
        String(50),
        default="user",
        nullable=False,
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    phone = Column(
        String(30),
        nullable=True,
    )

    address = Column(
        String(255),
        nullable=True,
    )

    date_of_birth = Column(
        Date,
        nullable=True,
    )

    gender = Column(
        String(20),
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    @property
    def profile_is_complete(self) -> bool:
        """Whether the optional personal-data fields have all been filled."""
        return all((
            self.phone,
            self.address,
            self.date_of_birth,
            self.gender,
        ))

    def __repr__(self):

        return (
            f"<User(id={self.id}, "
            f"email='{self.email}')>"
        )
