from fastapi import FastAPI
from app.routes import healthcheck_router, animerouter
from app.utils import lifespan

app = FastAPI(lifespan=lifespan)

app.include_router(healthcheck_router)
app.include_router(animerouter)
