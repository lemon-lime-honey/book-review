from datetime import datetime
from pydantic import BaseModel, field_validator
from domain.account.schemas import Account


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
    updated_at: datetime | None = None
    author: Account


class ReviewUpdate(ReviewCreate):
    review_id: int


class ReviewDelete(BaseModel):
    review_id: int