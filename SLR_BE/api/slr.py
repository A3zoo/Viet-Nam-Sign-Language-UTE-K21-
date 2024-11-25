from fastapi import APIRouter, HTTPException
from services.SLRService import predict

router = APIRouter()

@router.post("/predict")
async def create_item(lm_list):
    return predict(lm_list)