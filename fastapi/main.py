from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles
from domain.account import router as account_router
from domain.comment import router as comment_router
from domain.review import router as review_router

app = FastAPI(swagger_ui_parameters={"docExpansion": True, "operationSorter": "method"})

origins = ["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(account_router.router)
app.include_router(review_router.router)
app.include_router(comment_router.router)
app.mount("/assets", StaticFiles(directory="../frontend/dist/assets"))


@app.get("/", tags=["root"])
def index():
    return FileResponse("../frontend/dist/index.html")
