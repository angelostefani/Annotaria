from pydantic import BaseModel


class ExpertTypeBase(BaseModel):
    name: str


class ExpertTypeCreate(ExpertTypeBase):
    pass


class ExpertType(ExpertTypeBase):
    id: int

    class Config:
        orm_mode = True
