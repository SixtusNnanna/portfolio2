# app/models/orm.py
from __future__ import annotations

from datetime import datetime
from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey, DateTime, func, Boolean
from app.database.core import Base
from ulid import ULID


def generate_ulid() -> str:
    return str(ULID())


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(26),
        primary_key=True,
        default=generate_ulid,
        unique=True,
    )
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(250), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationship: one user → many projects
    # projects: Mapped[List["Project"]] = relationship(
    #     "Project",
    #     back_populates="user",
    #     cascade="all, delete-orphan",   # delete projects if user is deleted
    #     lazy="selectin",                # best default for performance
    # )


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(
        String(26),
        primary_key=True,
        default=generate_ulid,
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)        # ← fixed typo!
    image_url: Mapped[str] = mapped_column(Text, nullable=True)
    url: Mapped[str | None] = mapped_column(Text, nullable=True)
    github_repo: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),        # ← use func.now(), not func.current_timestamp()
        nullable=False,
        index=True,
    )

    # Foreign key
    