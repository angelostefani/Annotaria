from pydantic import BaseModel, Field


class ImageTypeBase(BaseModel):
    name: str


class ImageTypeCreate(ImageTypeBase):
    pass


class ImageType(ImageTypeBase):
    id: int

    class Config:
        orm_mode = True


class Image(BaseModel):
    id: int
    filename: str
    path: str
    image_type_id: int | None = None

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
    image_type: ImageType | None = None


class ImageUpdate(BaseModel):
    filename: str | None = None
    path: str | None = None
    image_type_id: int | None = None
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
    image_types: list[ImageType] = Field(default_factory=list)

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


from .answer import Answer, AnswerCreate
from .annotation import Annotation, AnnotationCreate, AnnotationUpdate
from .expert_type import ExpertType, ExpertTypeBase, ExpertTypeCreate
