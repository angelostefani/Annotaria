from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import (
    ExpertType as ExpertTypeModel,
    ImageType as ImageTypeModel,
    User as UserModel,
)
from schemas import ExpertType as ExpertTypeSchema, ExpertTypeCreate
from main import get_current_user

router = APIRouter()


def require_admin(current_user: UserModel = Depends(get_current_user)):
    if current_user.role != "Amministratore":
        raise HTTPException(status_code=403, detail="Forbidden")
    return current_user


@router.post(
    "/expert-types/",
    response_model=ExpertTypeSchema,
    dependencies=[Depends(require_admin)],
)
def create_expert_type(expert_type: ExpertTypeCreate, db: Session = Depends(get_db)):
    image_types = (
        db.query(ImageTypeModel)
        .filter(ImageTypeModel.id.in_(expert_type.image_type_ids))
        .all()
        if expert_type.image_type_ids
        else []
    )
    db_type = ExpertTypeModel(name=expert_type.name, image_types=image_types)
    db.add(db_type)
    db.commit()
    db.refresh(db_type)
    return db_type


@router.put(
    "/expert-types/{type_id}",
    response_model=ExpertTypeSchema,
    dependencies=[Depends(require_admin)],
)
def update_expert_type(type_id: int, expert_type: ExpertTypeCreate, db: Session = Depends(get_db)):
    db_type = db.query(ExpertTypeModel).filter_by(id=type_id).first()
    if not db_type:
        raise HTTPException(status_code=404, detail="Expert type not found")
    image_types = (
        db.query(ImageTypeModel)
        .filter(ImageTypeModel.id.in_(expert_type.image_type_ids))
        .all()
        if expert_type.image_type_ids
        else []
    )
    db_type.name = expert_type.name
    db_type.image_types = image_types
    db.commit()
    db.refresh(db_type)
    return db_type


@router.delete(
    "/expert-types/{type_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)],
)
def delete_expert_type(type_id: int, db: Session = Depends(get_db)):
    db_type = db.query(ExpertTypeModel).filter_by(id=type_id).first()
    if not db_type:
        raise HTTPException(status_code=404, detail="Expert type not found")
    db.delete(db_type)
    db.commit()
    return None


@router.get("/expert-types/", response_model=List[ExpertTypeSchema])
def list_expert_types(db: Session = Depends(get_db)):
    return db.query(ExpertTypeModel).all()
