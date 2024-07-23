import sqlalchemy as sa
import sqlalchemy.orm as so
from datetime import datetime
from typing import List, Optional
from database import Base


like_review_table = sa.Table(
    "like_review_table",
    Base.metadata,
    sa.Column("like_review_account", sa.ForeignKey("account.id"), primary_key=True),
    sa.Column("like_review", sa.ForeignKey("review.id"), primary_key=True),
)

dislike_review_table = sa.Table(
    "dislike_review_table",
    Base.metadata,
    sa.Column("dislike_review_account", sa.ForeignKey("account.id"), primary_key=True),
    sa.Column("dislike_review", sa.ForeignKey("review.id"), primary_key=True),
)

like_comment_table = sa.Table(
    "like_comment_table",
    Base.metadata,
    sa.Column("like_comment_account", sa.ForeignKey("account.id"), primary_key=True),
    sa.Column("like_comment", sa.ForeignKey("comment.id"), primary_key=True),
)

dislike_comment_table = sa.Table(
    "dislike_comment_table",
    Base.metadata,
    sa.Column("dislike_comment_account", sa.ForeignKey("account.id"), primary_key=True),
    sa.Column("dislike_comment", sa.ForeignKey("comment.id"), primary_key=True),
)


class Account(Base):
    __tablename__ = "account"

    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    username: so.Mapped[str] = so.mapped_column(
        sa.String(20), unique=True, nullable=False
    )
    password: so.Mapped[str] = so.mapped_column(sa.String, nullable=False)
    email: so.Mapped[str] = so.mapped_column(sa.String, unique=True, nullable=False)

    reviews: so.Mapped[List["Review"]] = so.relationship(
        back_populates="author", passive_deletes=True
    )
    comments: so.Mapped[List["Comment"]] = so.relationship(
        back_populates="author", passive_deletes=True
    )
    like_reviews: so.Mapped[List["Review"]] = so.relationship(
        "Review", secondary=like_review_table, back_populates="like_accounts"
    )
    dislike_reviews: so.Mapped[List["Review"]] = so.relationship(
        "Review", secondary=dislike_review_table, back_populates="dislike_accounts"
    )
    like_comments: so.Mapped[List["Comment"]] = so.relationship(
        "Comment", secondary=like_comment_table, back_populates="like_accounts"
    )
    dislike_comments: so.Mapped[List["Comment"]] = so.relationship(
        "Comment", secondary=dislike_comment_table, back_populates="dislike_accounts"
    )


class Review(Base):
    __tablename__ = "review"

    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    book: so.Mapped[str] = so.mapped_column(sa.String, nullable=False)
    subject: so.Mapped[str] = so.mapped_column(sa.String(30), nullable=False)
    content: so.Mapped[str] = so.mapped_column(sa.Text, nullable=False)
    created_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime, nullable=False)
    updated_at: so.Mapped[Optional[datetime]] = so.mapped_column(
        sa.DateTime, nullable=True
    )

    author_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("account.id"), nullable=False
    )
    author: so.Mapped["Account"] = so.relationship(back_populates="reviews")
    comments: so.Mapped[List["Comment"]] = so.relationship(
        back_populates="review", passive_deletes=True
    )
    like_accounts: so.Mapped[List["Account"]] = so.relationship(
        "Account", secondary=like_review_table, back_populates="like_reviews"
    )
    dislike_accounts: so.Mapped[List["Account"]] = so.relationship(
        "Account", secondary=dislike_review_table, back_populates="dislike_reviews"
    )


class Comment(Base):
    __tablename__ = "comment"

    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    content: so.Mapped[str] = so.mapped_column(sa.String(300), nullable=False)
    created_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime, nullable=False)
    updated_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime, nullable=True)

    review_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("review.id"), nullable=False
    )
    review: so.Mapped["Review"] = so.relationship(back_populates="comments")
    author_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("account.id"), nullable=False
    )
    author: so.Mapped["Account"] = so.relationship(back_populates="comments")
    like_accounts: so.Mapped[List["Account"]] = so.relationship(
        "Account", secondary=like_comment_table, back_populates="like_comments"
    )
    dislike_accounts: so.Mapped[List["Account"]] = so.relationship(
        "Account", secondary=dislike_comment_table, back_populates="dislike_comments"
    )
