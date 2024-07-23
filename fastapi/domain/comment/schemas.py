from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, field_validator
from domain.account.schemas import Account


class CommentCreate(BaseModel):
    content: str

    @field_validator("content")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("빈 칸은 허용되지 않습니다.")
        return v


class Comment(BaseModel):
    id: int
    content: str
    author: Account
    review_id: int
    created_at: datetime
    updated_at: datetime | None = None
    like_accounts: Optional[List[Account]]
    dislike_accounts: Optional[List[Account]]


class CommentUpdate(CommentCreate):
    comment_id: int


class CommentDelete(BaseModel):
    comment_id: int


class CommentLikeDislike(BaseModel):
    comment_id: int
