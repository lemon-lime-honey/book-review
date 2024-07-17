import sqlalchemy as sa
import sqlalchemy.orm as so
from datetime import datetime
from typing import Optional
from database import Base


class Account(Base):
    __tablename__ = "account"

    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    username: so.Mapped[str] = so.mapped_column(
        sa.String(20), unique=True, nullable=False
    )
    password: so.Mapped[str] = so.mapped_column(sa.String, nullable=False)
    email: so.Mapped[str] = so.mapped_column(sa.String, unique=True, nullable=False)

    reviews: so.WriteOnlyMapped["Review"] = so.relationship(back_populates="author")


class Review(Base):
    __tablename__ = "review"

    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    book: so.Mapped[str] = so.mapped_column(sa.String, nullable=False)
    subject: so.Mapped[str] = so.mapped_column(sa.String(30), nullable=False)
    content: so.Mapped[str] = so.mapped_column(sa.Text, nullable=False)
    created_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime, nullable=False)
    updated_at: so.Mapped[Optional[datetime]] = so.mapped_column(sa.DateTime, nullable=True)

    author_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("account.id"), nullable=False
    )
    author: so.Mapped["Account"] = so.relationship(back_populates="reviews")
