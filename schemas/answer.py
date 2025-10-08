from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AnswerBase(BaseModel):
    image_id: int
    question_id: int
    selected_option_id: int


class AnswerCreate(AnswerBase):
    pass


class Answer(AnswerBase):
    id: int
    user_id: int
    answered_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
