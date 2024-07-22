from datetime import datetime
from typing import List, Optional, Set
from pydantic import BaseModel, field_validator
from domain.account.schemas import Account
from domain.comment.schemas import Comment


class ReviewCreate(BaseModel):
    book: str
    subject: str
    content: str

    @field_validator("book", "subject", "content")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("빈 칸은 허용되지 않습니다.")
        return v


class Review(BaseModel):
    id: int
    book: str
    subject: str
    content: str
    created_at: datetime
    updated_at: Optional[datetime]
    author: Account
    comments: Optional[List[Comment]]
    like_accounts: Set[Account]
    dislike_accounts: Set[Account]


class ReviewUpdate(ReviewCreate):
    review_id: int


class ReviewDelete(BaseModel):
    review_id: int


class ReviewLikeDislike(BaseModel):
    review_id: int
