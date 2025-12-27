from fastapi import APIRouter, HTTPException
from services.SLRService import predict_with_STGCN
from model.dto.LandmarkPayload import LandmarkPayload


router = APIRouter()

@router.post("/predict")
async def create_item(lm_list: LandmarkPayload):
    label = predict_with_STGCN(lm_list)
    return {"label": label}






