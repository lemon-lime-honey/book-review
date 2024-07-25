from datetime import datetime, date, UTC
from random import randint
from database import SessionLocal
from models import Account, Review, Comment

db = SessionLocal()
accounts = list()

for i in range(1, 101):
    account = Account(
        username=f"test{i}",
        password=f"test{i}",
        email=f"test{i}@example.com",
        birthday=date.today(),
        summary=f"test{i}",
        created_at=datetime.now(UTC),
    )
    db.add(account)
    accounts.append(account)

db.commit()

for i in range(1, 301):
    review = Review(
        book=f"book{i}",
        subject=f"title{i}",
        content=f"content{i}",
        created_at=datetime.now(UTC),
        author_id=randint(1, 100),
    )
    db.add(review)

db.commit()

for i in range(1, 501):
    comment = Comment(
        content=f"comment{i}",
        created_at=datetime.now(UTC),
        review_id=randint(1, 300),
        author_id=randint(1, 100),
    )
    db.add(comment)

db.commit()

for i in range(501, 1001):
    comment = Comment(
        content=f"comment{i}",
        created_at=datetime.now(UTC),
        review_id=randint(280, 300),
        author_id=randint(1, 100),
    )
    db.add(comment)

db.commit()