from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import Annotation as AnnotationModel, User as UserModel
from schemas.annotation import (
    Annotation as AnnotationSchema,
    AnnotationCreate,
    AnnotationUpdate,
)
from main import get_current_user

router = APIRouter()


@router.post("/annotations/", response_model=AnnotationSchema)
def create_annotation(
    annotation: AnnotationCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    db_annotation = AnnotationModel(**annotation.dict(), user_id=current_user.id)
    db.add(db_annotation)
    db.commit()
    db.refresh(db_annotation)
    return db_annotation


@router.get("/annotations/{image_id}", response_model=List[AnnotationSchema])
def list_annotations(
    image_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return (
        db.query(AnnotationModel)
        .filter_by(image_id=image_id, user_id=current_user.id)
        .all()
    )


@router.put("/annotations/{annotation_id}", response_model=AnnotationSchema)
def update_annotation(annotation_id: int, annotation: AnnotationUpdate, db: Session = Depends(get_db)):
    db_annotation = db.query(AnnotationModel).filter_by(id=annotation_id).first()
    if not db_annotation:
        raise HTTPException(status_code=404, detail="Annotation not found")
    for field, value in annotation.dict(exclude_unset=True).items():
        setattr(db_annotation, field, value)
    db.commit()
    db.refresh(db_annotation)
    return db_annotation


@router.delete("/annotations/{annotation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_annotation(annotation_id: int, db: Session = Depends(get_db)):
    db_annotation = db.query(AnnotationModel).filter_by(id=annotation_id).first()
    if not db_annotation:
        raise HTTPException(status_code=404, detail="Annotation not found")
    db.delete(db_annotation)
    db.commit()
    return None
