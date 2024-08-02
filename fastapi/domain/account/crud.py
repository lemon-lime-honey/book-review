import bcrypt
import sqlalchemy.orm as so
from datetime import datetime, UTC
from domain.account import schemas
from models import Account, Comment, Review


def hash_password(password: str):
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password.decode("utf-8")


def verify_password(pw_ipt, pw_hash):
    pwd_bytes = pw_ipt.encode("utf-8")
    pw_hash_bytes = pw_hash.encode("utf-8")
    return bcrypt.checkpw(password=pwd_bytes, hashed_password=pw_hash_bytes)


def create_account(db: so.Session, account_create: schemas.AccountCreate):
    account = Account(
        username=account_create.username,
        password=hash_password(account_create.password1),
        email=account_create.email,
        birthday=account_create.birthday,
        summary=account_create.summary,
        created_at=datetime.now(UTC),
    )
    db.add(account)
    db.commit()


def check_account(db: so.Session, account_create: schemas.AccountCreate):
    return (
        db.query(Account)
        .filter(
            (Account.username == account_create.username)
            | (Account.email == account_create.email)
        )
        .first()
    )


def get_account(db: so.Session, account_id: int):
    return db.get(Account, account_id)


def find_account(db: so.Session, username: str):
    return db.query(Account).filter(Account.username == username).first()


def update_account(
    db: so.Session, account_update: schemas.AccountUpdate, account: Account
):
    account.username = account_update.username
    account.email = account_update.email
    account.birthday = account_update.birthday
    account.summary = account_update.summary

    db.add(account)
    db.commit()


def delete_account(db: so.Session, account: Account):
    db.delete(account)
    db.commit()


def match_account(db: so.Session, username: str, email: str):
    account = db.query(Account).filter_by(username=username, email=email).first()
    return account


def change_password(db: so.Session, account_id: int, password):
    account = db.get(Account, account_id)
    account.password = hash_password(password)
    db.add(account)
    db.commit()


def follow(db: so.Session, account: Account, current_user: Account):
    if current_user in account.followers:
        account.followers.remove(current_user)
    else:
        account.followers.append(current_user)
    db.commit()


def get_reviews(db: so.Session, account_id: int, skip: int = 0, limit: int = 5):
    _review_list = (
        db.query(Review).filter_by(author_id=account_id).order_by(Review.id.desc())
    )
    total = _review_list.count()
    review_list = _review_list.offset(skip).limit(limit).all()
    return total, review_list


def get_comments(db: so.Session, account_id: int, skip: int = 0, limit: int = 5):
    _comment_list = (
        db.query(Comment).filter_by(author_id=account_id).order_by(Comment.id.desc())
    )
    total = _comment_list.count()
    comment_list = _comment_list.offset(skip).limit(limit).all()
    return total, comment_list
