import sqlalchemy.orm as so
from datetime import datetime, UTC
from passlib.context import CryptContext
from domain.account import schemas
from models import Account

pwd_context = CryptContext(schemes=["bcrypt"])


def create_account(db: so.Session, account_create: schemas.AccountCreate):
    account = Account(
        username=account_create.username,
        password=pwd_context.hash(account_create.password1),
        email=account_create.email,
        birthday=account_create.birthday,
        summary=account_create.summary,
        created_at=datetime.now(UTC)
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


def follow(db: so.Session, account: Account, current_user: Account):
    if current_user in account.followers:
        account.followers.remove(current_user)
    else:
        account.followers.append(current_user)
    db.commit()
