from datetime import datetime
from typing import List
from pydantic import BaseModel


class Image(BaseModel):
    id: int
    filename: str
    path: str

    class Config:
        orm_mode = True


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


class Annotation(AnnotationBase):
    id: int
    annotated_at: datetime | None = None

    class Config:
        orm_mode = True
