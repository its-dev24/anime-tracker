from fastapi import APIRouter, Depends, status, HTTPException, Response
from app.database import get_db
from sqlalchemy import text

healthcheck_router = APIRouter(prefix="/healthcheck", tags=["Health Check"])


@healthcheck_router.get("/", status_code=status.HTTP_200_OK)
async def healthcheck(db=Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return Response(
            content="Server Health OK", headers={"Content-Type": "application/text"}
        )
    except Exception as e:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
