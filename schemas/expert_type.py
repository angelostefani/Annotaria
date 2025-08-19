from typing import List

from pydantic import BaseModel
from . import ImageType


class ExpertTypeBase(BaseModel):
    name: str


class ExpertTypeCreate(ExpertTypeBase):
    image_type_ids: List[int] = []


class ExpertType(ExpertTypeBase):
    id: int
    image_types: List[ImageType] = []

    class Config:
        orm_mode = True
