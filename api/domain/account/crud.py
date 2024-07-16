import sqlalchemy.orm as so
from passlib.context import CryptContext
from domain.account import schemas
from models import Account

pwd_context = CryptContext(schemes=["bcrypt"])


def create_account(db: so.Session, account_create: schemas.AccountCreate):
    account = Account(
        username=account_create.username,
        password=pwd_context.hash(account_create.password1),
        email=account_create.email,
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


def find_account(db: so.Session, username: str):
    return db.query(Account).filter(Account.username == username).first()
