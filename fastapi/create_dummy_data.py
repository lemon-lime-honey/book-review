import time
from datetime import datetime, date, timedelta, UTC
from random import randint
from domain.account.crud import hash_password
from database import SessionLocal
from models import Account, Review, Comment

data = open("./names.txt", encoding="utf-8")
username = data.readlines()
data.close()

data = open("./summary.txt", encoding="utf-8")
summary = data.readlines()
data.close()

data = open("./book.txt", encoding="utf-8")
book = data.readlines()
data.close()

data = open("./title.txt", encoding="utf-8")
title = data.readlines()
data.close()

data = open("./content.txt", encoding="utf-8")
content = data.readlines()
data.close()

basetime = datetime.now(UTC) - timedelta(days=10)

db = SessionLocal()
accounts = list()
reviews = list()
comments = list()

account_idx = 0
t = 1

while t < 1001:
    account = Account(
        username=username[account_idx],
        password=hash_password(username[account_idx]),
        email=f"{username[account_idx]}@example.com",
        birthday=date.today() - timedelta(weeks=56 * 20),
        summary=summary[randint(0, len(summary) - 1)],
        created_at=basetime + timedelta(minutes=10 * t),
    )

    db.add(account)
    db.commit()
    accounts.append(account)
    account_idx += 1
    t += 1

    if len(accounts) > 10:
        for i in range(len(accounts) * 20):
            review = Review(
                book=book[randint(0, len(book) - 1)],
                subject=title[randint(0, len(title) - 1)],
                content=content[randint(0, len(content) - 1)],
                created_at=basetime + timedelta(minutes=10 * t),
                author_id=randint(1, len(accounts)),
            )

            db.add(review)
            reviews.append(review)
            t += 1

        db.commit()

        for i in range(len(accounts) * 50):
            comment = Comment(
                content=content[randint(0, len(content) - 1)][:300],
                created_at=basetime + timedelta(minutes=10 * t),
                review_id=randint(1, len(reviews)),
                author_id=randint(1, len(accounts)),
            )
            db.add(comment)
            comments.append(comment)
            t += 1

        db.commit()
