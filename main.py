from fastapi import FastAPI
from db.database import engine, Base
import models  # Esse import é necessário para a função base.metadata
from api.routers.auth import router as auth_router
from api.routers.account import router as account_router
from api.routers.expense import router as expense_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router, prefix="/auth")
app.include_router(account_router, prefix="/accounts")
app.include_router(expense_router)
