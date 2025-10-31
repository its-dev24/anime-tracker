from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, TIMESTAMP, text, ForeignKey
from datetime import datetime


class Anime(Base):
    __tablename__ = "animes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    genre: Mapped[list[str]] = mapped_column(String, nullable=False)
    total_episodes: Mapped[int] = mapped_column(nullable=False)
    episodes_watched: Mapped[int] = mapped_column(nullable=False, default=0)
    status: Mapped[str] = mapped_column(
        String, server_default="Plan to Watch", nullable=False
    )  # e.g., "Watching", "Completed", "On Hold", "Dropped", "Plan to Watch"
    rating: Mapped[float] = mapped_column(
        server_default="0.0", nullable=False
    )  # User rating out of 10
    added_date: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
