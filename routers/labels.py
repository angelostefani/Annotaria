from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import Label as LabelModel, User as UserModel
from schemas import Label as LabelSchema, LabelCreate
from main import get_current_user

router = APIRouter()


def require_admin(current_user: UserModel = Depends(get_current_user)):
    if current_user.role != "Amministratore":
        raise HTTPException(status_code=403, detail="Forbidden")
    return current_user


@router.post(
    "/labels/",
    response_model=LabelSchema,
    dependencies=[Depends(require_admin)],
)
def create_label(label: LabelCreate, db: Session = Depends(get_db)):
    db_label = LabelModel(name=label.name)
    db.add(db_label)
    db.commit()
    db.refresh(db_label)
    return db_label


@router.put(
    "/labels/{label_id}",
    response_model=LabelSchema,
    dependencies=[Depends(require_admin)],
)
def update_label(label_id: int, label: LabelCreate, db: Session = Depends(get_db)):
    db_label = db.query(LabelModel).filter_by(id=label_id).first()
    if not db_label:
        raise HTTPException(status_code=404, detail="Label not found")
    db_label.name = label.name
    db.commit()
    db.refresh(db_label)
    return db_label


@router.delete(
    "/labels/{label_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)],
)
def delete_label(label_id: int, db: Session = Depends(get_db)):
    db_label = db.query(LabelModel).filter_by(id=label_id).first()
    if not db_label:
        raise HTTPException(status_code=404, detail="Label not found")
    db.delete(db_label)
    db.commit()
    return None


@router.get("/labels/", response_model=List[LabelSchema])
def list_labels(db: Session = Depends(get_db)):
    return db.query(LabelModel).all()
