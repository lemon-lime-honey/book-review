import sqlalchemy.orm as so
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from domain.account.router import load_current_account
from domain.comment import schemas
from domain.comment import crud as c_crud
from domain.review import crud as r_crud
from database import get_db
from error_msg import ReviewErrorMessage, CommentErrorMessage, ETCErrorMessage
from models import Account

router = APIRouter(prefix="/api/comment")


@router.post("/create/{review_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["comment"])
def comment_create(
    review_id: int,
    _comment_create: schemas.CommentCreate,
    db: so.Session = Depends(get_db),
    current_user: Account = Depends(load_current_account),
):
    review = r_crud.get_review(db, review_id)
    if review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ReviewErrorMessage.REVIEW_NOT_FOUND.value,
        )
    c_crud.create_comment(db, _comment_create, review, current_user)


@router.put("/update", status_code=status.HTTP_204_NO_CONTENT, tags=["comment"])
def comment_update(
    _comment_create: schemas.CommentUpdate,
    db: so.Session = Depends(get_db),
):
    comment = c_crud.get_comment(db, _comment_create.comment_id)
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=CommentErrorMessage.COMMENT_NOT_FOUND.value,
        )
    c_crud.update_comment(db, _comment_create, comment)


@router.get("/list/{review_id}", response_model=schemas.CommentList, tags=["comment"])
def comment_list(
    review_id: int, db: so.Session = Depends(get_db), page: int = 0, size: int = 10
):
    total, _comment_list = c_crud.get_comment_list(
        db, review_id, skip=page * size, limit=size
    )
    return {"total": total, "comment_list": _comment_list}


@router.get("/detail/{comment_id}", response_model=schemas.Comment, tags=["comment"])
def comment_detail(comment_id: int, db: so.Session = Depends(get_db)):
    return c_crud.get_comment(db, comment_id)


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT, tags=["comment"])
def comment_delete(
    _comment_delete: schemas.CommentDelete,
    db: so.Session = Depends(get_db),
    current_user: Account = Depends(load_current_account),
):
    comment = c_crud.get_comment(db, _comment_delete.comment_id)
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=CommentErrorMessage.COMMENT_NOT_FOUND.value,
        )
    if current_user.id != comment.author.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=ETCErrorMessage.AUTHOR_CONFLICT_DELETE.value,
        )
    c_crud.delete_comment(db, comment)


@router.post("/like", status_code=status.HTTP_204_NO_CONTENT, tags=["comment"])
def comment_like(
    _comment_like: schemas.CommentLikeDislike,
    db: so.Session = Depends(get_db),
    current_user: Account = Depends(load_current_account),
):
    comment = c_crud.get_comment(db, _comment_like.comment_id)
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=CommentErrorMessage.COMMENT_NOT_FOUND.value,
        )
    if current_user in comment.dislike_accounts:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=CommentErrorMessage.COMMENT_CANNOT_LIKE.value,
        )
    c_crud.like_comment(db, comment, current_user)


@router.post("/dislike", status_code=status.HTTP_204_NO_CONTENT, tags=["comment"])
def comment_dislike(
    _comment_dislike: schemas.CommentLikeDislike,
    db: so.Session = Depends(get_db),
    current_user: Account = Depends(load_current_account),
):
    comment = c_crud.get_comment(db, _comment_dislike.comment_id)
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=CommentErrorMessage.COMMENT_NOT_FOUND.value,
        )
    if current_user in comment.like_accounts:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=CommentErrorMessage.COMMENT_CANNOT_DISLIKE.value,
        )
    c_crud.dislike_comment(db, comment, current_user)
