from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Answer as AnswerModel, User as UserModel
from schemas.answer import Answer as AnswerSchema, AnswerCreate
from main import get_current_user

router = APIRouter()


@router.post("/answers/", response_model=AnswerSchema)
def create_answer(
    answer: AnswerCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    db_answer = AnswerModel(**answer.dict(), user_id=current_user.id)
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer


@router.get("/answers/{image_id}", response_model=List[AnswerSchema])
def list_answers(
    image_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return (
        db.query(AnswerModel)
        .filter_by(image_id=image_id, user_id=current_user.id)
        .all()
    )
