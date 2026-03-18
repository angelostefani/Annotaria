from typing import List

from pydantic import BaseModel, ConfigDict
from . import ImageType


class ExpertTypeBase(BaseModel):
    name: str


class ExpertTypeCreate(ExpertTypeBase):
    image_type_ids: List[int] = []


class ExpertType(ExpertTypeBase):
    id: int
    image_types: List[ImageType] = []

    model_config = ConfigDict(from_attributes=True)
