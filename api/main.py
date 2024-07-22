from fastapi import FastAPI
from domain.account import router as account_router

app = FastAPI()

app.include_router(account_router.router)