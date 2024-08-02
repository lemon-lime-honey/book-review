from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core.core_schema import ValidationInfo
from error_msg import FormErrorMessage


class AccountCreate(BaseModel):
    username: str
    password1: str
    password2: str
    email: EmailStr
    birthday: date
    summary: str

    @field_validator("username", "password1", "password2", "email")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError(FormErrorMessage.REQUIRED.value)
        return v

    @field_validator("password2")
    def passwords_match(cls, v, info: ValidationInfo):
        if "password1" in info.data and v != info.data.get("password1"):
            raise ValueError(FormErrorMessage.PASSWORD_CONFLICT.value)
        return v


class AccountBase(BaseModel):
    id: int


class Account(AccountBase):
    username: str
    email: str
    birthday: date
    summary: str
    created_at: datetime
    last_visit: Optional[datetime]
    followers: List[AccountBase]
    following: List[AccountBase]


class AccountUpdate(BaseModel):
    id: int
    username: str
    email: str
    birthday: date
    summary: str


class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    username: str


class Follow(BaseModel):
    account_id: int
