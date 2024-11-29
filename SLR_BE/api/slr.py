from fastapi import APIRouter, HTTPException
from services.SLRService import predict
from model.dto.LandmarkPayload import LandmarkPayload


router = APIRouter()

@router.post("/predict")
async def create_item(lm_list: LandmarkPayload):
    label = predict(lm_list)
    return {"label": label}






