from typing import List
from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core.core_schema import ValidationInfo


class AccountCreate(BaseModel):
    username: str
    password1: str
    password2: str
    email: EmailStr

    @field_validator("username", "password1", "password2", "email")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("필수항목입니다.")
        return v

    @field_validator("password2")
    def passwords_match(cls, v, info: ValidationInfo):
        if "password1" in info.data and v != info.data.get("password1"):
            raise ValueError("비밀번호가 일치하지 않습니다.")
        return v


class AccountBase(BaseModel):
    id: int


class Account(AccountBase):
    username: str
    email: str
    followers: List[AccountBase]
    following: List[AccountBase]
    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int


class Follow(BaseModel):
    account_id: int
