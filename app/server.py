from fastapi import FastAPI
from app.routes import healthcheck_router

app = FastAPI()

app.include_router(healthcheck_router)
