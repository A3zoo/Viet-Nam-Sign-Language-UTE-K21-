from pydantic import BaseModel
from typing import List


class LandmarkPayload(BaseModel):
    lm_list: List[List[float]]  