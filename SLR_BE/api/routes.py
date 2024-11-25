from fastapi import APIRouter, HTTPException
from api.slr import router as slr_router

router = APIRouter()

router.include_router(slr_router, prefix="/slr", tags=["slr"])