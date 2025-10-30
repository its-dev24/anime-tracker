from fastapi import APIRouter

healthcheck_router = APIRouter(prefix="/healthcheck", tags=["Health Check"])


@healthcheck_router.get("/")
async def healthcheck():
    return {"detail": "Server Health Good"}
