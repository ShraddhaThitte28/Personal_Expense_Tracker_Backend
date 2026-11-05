from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_allowed_origins, get_database_url, get_jwt_secret
from app.routers.auth import router as auth_router
from app.routers.expenses import router as expenses_router

get_database_url()
get_jwt_secret()

app = FastAPI(title="Personal Expense Tracker")

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(auth_router)
app.include_router(expenses_router)


@app.get("/")
def read_root():
    return {"message": "Personal Expense Tracker API is running"}
