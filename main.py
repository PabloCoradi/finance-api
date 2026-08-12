from fastapi import FastAPI
from db.database import engine, Base
import models
from api.routers.auth import router as auth_router
from api.routers.account import router as account_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router, prefix="/auth")
app.include_router(account_router, prefix="/accounts")
