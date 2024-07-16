import os
import sqlalchemy.orm as so
from datetime import datetime, timedelta, UTC
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from starlette import status
from domain.account import schemas, crud
from database import get_db

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("HASH_ALGORITHM")

router = APIRouter(prefix="/account")


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def account_create(
    _account_create: schemas.AccountCreate, db: so.Session = Depends(get_db)
):
    if crud.check_account(db, _account_create):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="이미 존재하는 회원입니다."
        )
    crud.create_account(db, _account_create)


@router.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: so.Session = Depends(get_db)
):
    account = crud.find_account(db, form_data.username)
    if not account or not crud.pwd_context.verify(form_data.password, account.password):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="아이디 또는 비밀번호가 다릅니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    claims = {
        "sub": account.username,
        "exp": datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    access_token = jwt.encode(claims, SECRET_KEY, ALGORITHM)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": account.username,
    }
