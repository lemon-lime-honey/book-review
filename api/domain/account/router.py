import os
import sqlalchemy.orm as so
from datetime import datetime, timedelta, UTC
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from starlette import status
from domain.account import schemas, crud
from database import get_db

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("HASH_ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/account/login")

router = APIRouter(prefix="/api/account")


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


def load_current_account(
    token: str = Depends(oauth2_scheme), db: so.Session = Depends(get_db)
):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
    except JWTError:
        raise credential_exception
    else:
        account = crud.find_account(db, username)
        if account is None:
            raise credential_exception
        return account
