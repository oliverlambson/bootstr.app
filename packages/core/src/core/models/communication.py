from __future__ import annotations

from pydantic import BaseModel, EmailStr
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base, ImmutableMixin


class EmailInsert(BaseModel):
    sender: EmailStr
    recipient: EmailStr
    subject: str
    body: str


class Email(ImmutableMixin, Base):
    __tablename__ = "email"
    sender: Mapped[EmailStr] = mapped_column(nullable=False, unique=True)
    recipient: Mapped[EmailStr] = mapped_column(nullable=False, unique=True, index=True)
    subject: Mapped[str]
    body: Mapped[str]
    template_name: Mapped[str]
    template_data: Mapped[JSON]


class SMSInsert(BaseModel):
    sender: str
    recipient: str
    message: str


class SMS(ImmutableMixin, Base):
    __tablename__ = "sms"
    sender: Mapped[str] = mapped_column(nullable=False, unique=True)
    recipient: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    message: Mapped[str]
