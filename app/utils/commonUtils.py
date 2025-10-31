from app.model import models
from contextlib import asynccontextmanager
from app.database import engine
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server Starting")
    try:
        models.Base.metadata.create_all(bind=engine)
        print("tables created ")
    except Exception as e:
        print(str(e))
    yield
