from datetime import datetime
from pydantic import BaseModel

from .label import Label


class AnnotationBase(BaseModel):
    image_id: int
    label_id: int
    x: float
    y: float
    width: float
    height: float


class AnnotationCreate(AnnotationBase):
    pass


class AnnotationUpdate(BaseModel):
    image_id: int | None = None
    label_id: int | None = None
    x: float | None = None
    y: float | None = None
    width: float | None = None
    height: float | None = None


class Annotation(AnnotationBase):
    id: int
    user_id: int
    annotated_at: datetime | None = None
    label: Label

    class Config:
        orm_mode = True
