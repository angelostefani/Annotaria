from datetime import datetime
from typing import List

from pydantic import BaseModel

from .label import Label


class Point(BaseModel):
    x: float
    y: float


class AnnotationBase(BaseModel):
    image_id: int
    label_id: int
    points: List[Point]


class AnnotationCreate(AnnotationBase):
    pass


class AnnotationUpdate(BaseModel):
    image_id: int | None = None
    label_id: int | None = None
    points: List[Point] | None = None


class Annotation(AnnotationBase):
    id: int
    user_id: int
    annotated_at: datetime | None = None
    label: Label

    class Config:
        orm_mode = True

