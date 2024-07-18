from datetime import datetime
from pydantic import BaseModel, field_validator
from domain.account.schemas import Account
from domain.review.schemas import Review


class CommentCreate(BaseModel):
    content: str
    review: Review
    author: Account

    @field_validator("content")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("빈 칸은 허용되지 않습니다.")
        return v


class Comment(BaseModel):
    id: int
    content: str
    review: Review
    author: Account
    created_at: datetime
    updated_at: datetime | None = None


class CommentUpdate(CommentCreate):
    comment_id: int


class CommentDelete(BaseModel):
    comment_id: int
