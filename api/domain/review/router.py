import sqlalchemy.orm as so
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from domain.account.router import load_current_account
from domain.review import schemas, crud
from database import get_db
from models import Account

router = APIRouter(prefix="/api/review")


@router.get("/list", response_model=List[schemas.Review])
def review_list(db: so.Session = Depends(get_db)):
    return crud.get_review_list(db)


@router.get("/detail/{review_id}", response_model=schemas.Review)
def review_detail(review_id: int, db: so.Session = Depends(get_db)):
    review = crud.get_review(db, review_id)
    if review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="후기가 존재하지 않습니다."
        )
    return review


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def review_create(
    _review_create: schemas.ReviewCreate,
    db: so.Session = Depends(get_db),
    current_user: Account = Depends(load_current_account),
):
    crud.create_review(db, _review_create, current_user)


@router.put("/update/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def review_update(
    _review_update: schemas.ReviewUpdate, db: so.Session = Depends(get_db)
):
    review = crud.get_review(db, _review_update.review_id)
    if review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="후기가 존재하지 않습니다."
        )
    crud.update_review(db, _review_update, review)


@router.delete("/delete/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def review_delete(
    _review_delete: schemas.ReviewDelete, db: so.Session = Depends(get_db)
):
    review = crud.get_review(db, _review_delete.review_id)
    if review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="후기가 존재하지 않습니다."
        )
    crud.delete_review(db, review)
