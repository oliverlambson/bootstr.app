from datetime import datetime
from typing import ClassVar
from uuid import UUID

from pydantic import EmailStr
from sqlalchemy import JSON, Index, MetaData, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

metadata = MetaData()


class Base(DeclarativeBase):
    metadata: ClassVar[MetaData] = metadata
    type_annotation_map: ClassVar = {
        EmailStr: String(),
        JSON: JSONB(),
    }


class MutableMixin:
    """Base set of columns for tables with mutable rows"""

    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
    )
    uuid: Mapped[UUID] = mapped_column(
        insert_default=func.gen_random_uuid(),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        insert_default=func.current_timestamp(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        insert_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        nullable=False,
    )

    @declared_attr.directive
    def __table_args__(cls):
        return (
            Index(None, "uuid"),
            UniqueConstraint("uuid"),
        )


class ImmutableMixin:
    """Base set of columns for tables with immutable rows"""

    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
    )
    uuid: Mapped[UUID] = mapped_column(
        insert_default=func.gen_random_uuid(),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        insert_default=func.current_timestamp(),
        nullable=False,
    )

    @declared_attr.directive
    def __table_args__(cls):
        return (
            Index(None, "uuid"),
            UniqueConstraint("uuid"),
        )
