from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import (
    Question as QuestionModel,
    Option as OptionModel,
    User as UserModel,
    ImageType as ImageTypeModel,
)
from main import get_current_user
from schemas import (
    Question as QuestionSchema,
    QuestionCreate,
    Option as OptionSchema,
    OptionCreate,
)

router = APIRouter()


def require_admin(current_user: UserModel = Depends(get_current_user)):
    if current_user.role != "Amministratore":
        raise HTTPException(status_code=403, detail="Forbidden")
    return current_user


@router.post(
    "/questions/",
    response_model=QuestionSchema,
    dependencies=[Depends(require_admin)],
)
def create_question(question: QuestionCreate, db: Session = Depends(get_db)):
    db_question = QuestionModel(question_text=question.question_text)
    if question.image_type_ids:
        db_question.image_types = (
            db.query(ImageTypeModel)
            .filter(ImageTypeModel.id.in_(question.image_type_ids))
            .all()
        )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


@router.put(
    "/questions/{question_id}",
    response_model=QuestionSchema,
    dependencies=[Depends(require_admin)],
)
def update_question(
    question_id: int, question: QuestionCreate, db: Session = Depends(get_db)
):
    db_question = db.query(QuestionModel).filter_by(id=question_id).first()
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")
    db_question.question_text = question.question_text
    db_question.image_types = (
        db.query(ImageTypeModel)
        .filter(ImageTypeModel.id.in_(question.image_type_ids))
        .all()
        if question.image_type_ids
        else []
    )
    db.commit()
    db.refresh(db_question)
    return db_question


@router.delete(
    "/questions/{question_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)],
)
def delete_question(question_id: int, db: Session = Depends(get_db)):
    db_question = db.query(QuestionModel).filter_by(id=question_id).first()
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")
    db.delete(db_question)
    db.commit()
    return None


@router.get("/questions/", response_model=List[QuestionSchema])
def list_questions(db: Session = Depends(get_db)):
    return db.query(QuestionModel).all()


@router.post(
    "/questions/{question_id}/options",
    response_model=OptionSchema,
    dependencies=[Depends(require_admin)],
)
def create_option(
    question_id: int, option: OptionCreate, db: Session = Depends(get_db)
):
    if not db.query(QuestionModel).filter_by(id=question_id).first():
        raise HTTPException(status_code=404, detail="Question not found")
    db_option = OptionModel(question_id=question_id, option_text=option.option_text)
    db.add(db_option)
    db.commit()
    db.refresh(db_option)
    return db_option


@router.put(
    "/options/{option_id}",
    response_model=OptionSchema,
    dependencies=[Depends(require_admin)],
)
def update_option(
    option_id: int, option: OptionCreate, db: Session = Depends(get_db)
):
    db_option = db.query(OptionModel).filter_by(id=option_id).first()
    if not db_option:
        raise HTTPException(status_code=404, detail="Option not found")
    db_option.option_text = option.option_text
    db.commit()
    db.refresh(db_option)
    return db_option


@router.delete(
    "/options/{option_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)],
)
def delete_option(option_id: int, db: Session = Depends(get_db)):
    db_option = db.query(OptionModel).filter_by(id=option_id).first()
    if not db_option:
        raise HTTPException(status_code=404, detail="Option not found")
    db.delete(db_option)
    db.commit()
    return None


@router.get("/questions/{question_id}/options", response_model=List[OptionSchema])
def list_options(question_id: int, db: Session = Depends(get_db)):
    return db.query(OptionModel).filter_by(question_id=question_id).all()
