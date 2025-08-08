from pydantic import BaseModel

from .expert_type import ExpertType


class UserBase(BaseModel):
    username: str
    role: str = "Esperto"


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(UserBase):
    id: int
    expert_types: list[ExpertType] = []

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
