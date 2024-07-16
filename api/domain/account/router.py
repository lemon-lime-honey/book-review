import sqlalchemy.orm as so
from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from domain.account import schemas, crud
from database import get_db

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
