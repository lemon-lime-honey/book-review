import sqlalchemy.orm as so
from datetime import datetime, UTC
from domain.review import schemas
from models import Account, Review


def create_review(
    db: so.Session, review_create: schemas.ReviewCreate, current_user: Account
):
    review = Review(
        book=review_create.book,
        subject=review_create.subject,
        content=review_create.content,
        created_at=datetime.now(UTC),
        author=current_user,
    )
    db.add(review)
    db.commit()


def get_review_list(db: so.Session):
    return db.query(Review).order_by(Review.id.desc()).all()


def get_review(db: so.Session, review_id: int):
    return db.get(Review, review_id)


def update_review(db: so.Session, review_update: schemas.ReviewUpdate, review: Review):
    review.book = review_update.book
    review.subject = review_update.subject
    review.content = review_update.content
    review.updated_at = datetime.now(UTC)
    db.add(review)
    db.commit()


def delete_review(db: so.Session, review: Review):
    db.delete(review)
    db.commit()


def like_review(db: so.Session, review: Review, current_user: Account):
    if current_user in review.like_accounts:
        review.like_accounts.remove(current_user)
    else:
        review.like_accounts.append(current_user)
    db.commit()


def dislike_review(db: so.Session, review: Review, current_user: Account):
    if current_user in review.dislike_accounts:
        review.dislike_accounts.remove(current_user)
    else:
        review.dislike_accounts.append(current_user)
    db.commit()
