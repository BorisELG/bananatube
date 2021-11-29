from fastapi import APIRouter

from api.api_v1.endpoints import split


api_router = APIRouter()
api_router.include_router(split.router, prefix="/split", tags=["split"])
