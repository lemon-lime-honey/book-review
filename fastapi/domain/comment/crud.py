import sqlalchemy.orm as so
from datetime import datetime, UTC
from domain.comment import schemas
from models import Account, Review, Comment


def create_comment(
    db: so.Session,
    comment_create: schemas.CommentCreate,
    review: Review,
    current_user: Account,
):
    comment = Comment(
        content=comment_create.content,
        review=review,
        created_at=datetime.now(UTC),
        author=current_user,
    )
    db.add(comment)
    db.commit()


def get_comment(db: so.Session, comment_id: int):
    return db.get(Comment, comment_id)


def get_comment_list(db: so.Session, review_id: int, skip: int = 0, limit: int = 10):
    _comment_list = db.query(Comment).filter_by(review_id=review_id).order_by(Comment.id.asc())
    total = _comment_list.count()
    comment_list = _comment_list.offset(skip).limit(limit).all()
    return total, comment_list


def update_comment(
    db: so.Session, comment_update: schemas.CommentUpdate, comment: Comment
):
    comment.content = comment_update.content
    comment.updated_at = datetime.now(UTC)
    db.add(comment)
    db.commit()


def delete_comment(db: so.Session, comment: Comment):
    db.delete(comment)
    db.commit()


def like_comment(db: so.Session, comment: Comment, current_user: Account):
    if current_user in comment.like_accounts:
        comment.like_accounts.remove(current_user)
    else:
        comment.like_accounts.append(current_user)
    db.commit()


def dislike_comment(db: so.Session, comment: Comment, current_user: Account):
    if current_user in comment.dislike_accounts:
        comment.dislike_accounts.remove(current_user)
    else:
        comment.dislike_accounts.append(current_user)
    db.commit()
