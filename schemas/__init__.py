from datetime import datetime
from typing import List
from pydantic import BaseModel


class Image(BaseModel):
    id: int
    filename: str
    path: str

    class Config:
        orm_mode = True


class ImageDetail(Image):
    exif_datetime: str | None = None
    exif_gps_lat: float | None = None
    exif_gps_lon: float | None = None
    exif_gps_alt: float | None = None
    exif_camera_make: str | None = None
    exif_camera_model: str | None = None
    exif_lens_model: str | None = None
    exif_focal_length: float | None = None
    exif_aperture: float | None = None
    exif_iso: int | None = None
    exif_shutter_speed: str | None = None
    exif_orientation: str | None = None
    exif_image_width: int | None = None
    exif_image_height: int | None = None
    exif_drone_model: str | None = None
    exif_flight_id: str | None = None
    exif_pitch: float | None = None
    exif_roll: float | None = None
    exif_yaw: float | None = None


class QuestionBase(BaseModel):
    question_text: str


class QuestionCreate(QuestionBase):
    pass


class Question(QuestionBase):
    id: int

    class Config:
        orm_mode = True


class OptionBase(BaseModel):
    option_text: str


class OptionCreate(OptionBase):
    pass


class Option(OptionBase):
    id: int
    question_id: int

    class Config:
        orm_mode = True


class AnswerBase(BaseModel):
    image_id: int
    question_id: int
    selected_option_id: int


class AnswerCreate(AnswerBase):
    pass


class Answer(AnswerBase):
    id: int
    answered_at: datetime | None = None

    class Config:
        orm_mode = True


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
    annotated_at: datetime | None = None

    class Config:
        orm_mode = True
