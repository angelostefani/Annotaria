from datetime import datetime
from pydantic import BaseModel


class AnnotationBase(BaseModel):
    image_id: int
    label: str
    x: float
    y: float
    width: float
    height: float


class AnnotationCreate(AnnotationBase):
    pass


class AnnotationUpdate(BaseModel):
    image_id: int | None = None
    label: str | None = None
    x: float | None = None
    y: float | None = None
    width: float | None = None
    height: float | None = None


class Annotation(AnnotationBase):
    id: int
    user_id: int
    annotated_at: datetime | None = None

    class Config:
        orm_mode = True
