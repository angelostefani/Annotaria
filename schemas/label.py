from typing import List

from pydantic import BaseModel
from . import ImageType


class LabelBase(BaseModel):
    name: str


class LabelCreate(LabelBase):
    image_type_ids: List[int] = []


class Label(LabelBase):
    id: int
    image_types: List[ImageType] = []

    class Config:
        orm_mode = True
