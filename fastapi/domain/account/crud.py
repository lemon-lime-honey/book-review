import bcrypt
import sqlalchemy.orm as so
from datetime import datetime, UTC
from domain.account import schemas
from models import Account


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


def follow(db: so.Session, account: Account, current_user: Account):
    if current_user in account.followers:
        account.followers.remove(current_user)
    else:
        account.followers.append(current_user)
    db.commit()
