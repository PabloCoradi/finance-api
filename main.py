from fastapi import FastAPI
from db.database import engine, Base
import models
from api.routers.auth import router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(router, prefix="/auth")
