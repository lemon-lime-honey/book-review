import sqlalchemy.orm as so
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from domain.account.router import load_current_account
from domain.comment import schemas
from domain.comment import crud as c_crud
from domain.review import crud as r_crud
from database import get_db
from models import Account

router = APIRouter(prefix="/api/comment")


@router.post("/create/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def comment_create(
    review_id: int,
    _comment_create: schemas.CommentCreate,
    db: so.Session = Depends(get_db),
    current_user: Account = Depends(load_current_account),
):
    review = r_crud.get_review(db, review_id)
    if review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="후기가 존재하지 않습니다."
        )
    c_crud.create_comment(db, _comment_create, review, current_user)


@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def comment_update(
    _comment_create: schemas.CommentUpdate,
    db: so.Session = Depends(get_db),
):
    comment = c_crud.get_comment(db, _comment_create.comment_id)
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="댓글이 존재하지 않습니다."
        )
    c_crud.update_comment(db, _comment_create, comment)


@router.get("/detail/{comment_id}", response_model=schemas.Comment)
def comment_detail(comment_id: int, db: so.Session = Depends(get_db)):
    return c_crud.get_comment(db, comment_id)


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def comment_delete(
    _comment_delete: schemas.CommentDelete,
    db: so.Session = Depends(get_db),
    current_user: Account = Depends(load_current_account),
):
    comment = c_crud.get_comment(db, _comment_delete.comment_id)
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="댓글이 존재하지 않습니다."
        )
    if current_user.id != comment.author.id:
        raise HTTPException(status_code=status.HTTP_403, detail="삭제 권한이 없습니다.")
    c_crud.delete_comment(db, comment)
