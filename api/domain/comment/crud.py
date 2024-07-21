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
        create_at=datetime.now(UTC),
        author=current_user,
    )
    db.add(comment)
    db.commit()


def get_comment_list(db: so.Session, review: Review):
    return (
        db.query(Comment)
        .filter(Comment.review == review)
        .order_by(Comment.id.desc())
        .all()
    )


def get_comment(db: so.Session, comment_id: int):
    return db.get(Comment, comment_id)


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
