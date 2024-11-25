from pydantic import BaseModel
from typing import List


class TestDTO(BaseModel):
    name: str
    age: int