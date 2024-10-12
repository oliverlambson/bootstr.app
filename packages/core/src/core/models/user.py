from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, EmailStr
from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base import Base, MutableMixin


class UserUpsert(BaseModel):
    email: EmailStr


class User(MutableMixin, Base):
    __tablename__ = "user"
    email: Mapped[EmailStr] = mapped_column(nullable=False, unique=True, index=True)
    verifications: Mapped[list[UserVerification]] = relationship(back_populates="user")


class UserVerificationInsert(BaseModel):
    user_id: int
    expires_at: datetime


class UserVerificationUpdate(BaseModel):
    id: UUID
    verified_at: datetime


class UserVerification(MutableMixin, Base):
    __tablename__ = "user_verification"
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    expires_at: Mapped[datetime] = mapped_column(nullable=False)
    verified_at: Mapped[datetime] = mapped_column()

    user: Mapped[User] = relationship()

    __table_args__: Any = (CheckConstraint("verified_at <= expires_at"),)
