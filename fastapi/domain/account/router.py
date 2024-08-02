import os
import sqlalchemy.orm as so
from datetime import datetime, timedelta, UTC
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from starlette import status
from domain.account import schemas, crud
from domain.comment.schemas import CommentList
from domain.review.schemas import ReviewList
from database import get_db
from error_msg import AccountErrorMessage
from models import Account

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("HASH_ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/account/login")

router = APIRouter(prefix="/api/account")


def load_current_account(
    token: str = Depends(oauth2_scheme), db: so.Session = Depends(get_db)
):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=AccountErrorMessage.ACCOUNT_CANNOT_VALIDATE.value,
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


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def account_create(
    _account_create: schemas.AccountCreate, db: so.Session = Depends(get_db)
):
    if crud.check_account(db, _account_create):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=AccountErrorMessage.ACCOUNT_EXISTS.value,
        )
    crud.create_account(db, _account_create)


@router.get("/get/{username}", response_model=schemas.Account)
def account_get(username: str, db: so.Session = Depends(get_db)):
    return crud.find_account(db, username)


@router.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: so.Session = Depends(get_db)
):
    account = crud.find_account(db, form_data.username)
    if not account or not crud.verify_password(form_data.password, account.password):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=AccountErrorMessage.ACCOUNT_DIFFERENT_DATA.value,
            headers={"WWW-Authenticate": "Bearer"},
        )
    claims = {
        "sub": account.username,
        "exp": datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    access_token = jwt.encode(claims, SECRET_KEY, ALGORITHM)
    account.last_visit = datetime.now(UTC)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": account.id,
        "username": account.username,
    }


@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def account_update(
    _account_update: schemas.AccountUpdate,
    db: so.Session = Depends(get_db),
    current_user: Account = Depends(load_current_account),
):
    account = db.get(Account, _account_update.id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=AccountErrorMessage.ACCOUNT_NOT_FOUND.value,
        )
    if account.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=AccountErrorMessage.ACCOUNT_DIFFERENT_ACCOUNT.value,
        )
    crud.update_account(db, _account_update, account)


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def account_delete(
    db: so.Session = Depends(get_db),
    current_user: Account = Depends(load_current_account),
):
    crud.delete_account(db, current_user)


@router.post("/match", response_model=schemas.AccountBase)
def account_match(
    _account_match: schemas.AccountMatch, db: so.Session = Depends(get_db)
):
    account = crud.match_account(db, _account_match.username, _account_match.email)
    if account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=AccountErrorMessage.ACCOUNT_NOT_FOUND.value,
        )
    return {"id": account.id}


@router.post("/reset", status_code=status.HTTP_204_NO_CONTENT)
def reset_password(
    _reset_password: schemas.PasswordReset, db: so.Session = Depends(get_db)
):
    crud.change_password(db, _reset_password.account_id, _reset_password.password1)


@router.post("/change", status_code=status.HTTP_204_NO_CONTENT)
def change_password(
    _change_password: schemas.PasswordChange,
    db: so.Session = Depends(get_db),
    current_user: Account = Depends(load_current_account),
):
    if not crud.verify_password(_change_password.password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=AccountErrorMessage.ACCOUNT_DIFFERENT_DATA.value,
        )
    current_user.password = crud.hash_password(_change_password.password1)
    db.add(current_user)
    db.commit()


@router.post("/follow", status_code=status.HTTP_204_NO_CONTENT)
def follow(
    _follow: schemas.Follow,
    db: so.Session = Depends(get_db),
    current_user: Account = Depends(load_current_account),
):
    account = db.get(Account, _follow.account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=AccountErrorMessage.ACCOUNT_NOT_FOUND.value,
        )
    crud.follow(db, account, current_user)


@router.get("/reviews", response_model=ReviewList)
def review_list_by_account(
    account_id: int, db: so.Session = Depends(get_db), page: int = 0, size: int = 5
):
    account = crud.get_account(db, account_id)
    if account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=AccountErrorMessage.ACCOUNT_NOT_FOUND.value,
        )
    total, _review_list = crud.get_reviews(db, account_id, skip=page * size, limit=size)
    return {"total": total, "review_list": _review_list}


@router.get("/comments", response_model=CommentList)
def comment_list_by_account(
    account_id: int, db: so.Session = Depends(get_db), page: int = 0, size: int = 5
):
    account = crud.get_account(db, account_id)
    if account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=AccountErrorMessage.ACCOUNT_NOT_FOUND.value,
        )
    total, _comment_list = crud.get_comments(
        db, account_id, skip=page * size, limit=size
    )
    return {"total": total, "comment_list": _comment_list}
