from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import ImageType as ImageTypeModel, User as UserModel
from schemas import ImageType as ImageTypeSchema, ImageTypeCreate
from main import get_current_user

router = APIRouter()


def require_admin(current_user: UserModel = Depends(get_current_user)):
    if current_user.role != "Amministratore":
        raise HTTPException(status_code=403, detail="Forbidden")
    return current_user


@router.post(
    "/image-types/",
    response_model=ImageTypeSchema,
    dependencies=[Depends(require_admin)],
)
def create_image_type(image_type: ImageTypeCreate, db: Session = Depends(get_db)):
    db_type = ImageTypeModel(name=image_type.name)
    db.add(db_type)
    db.commit()
    db.refresh(db_type)
    return db_type


@router.put(
    "/image-types/{type_id}",
    response_model=ImageTypeSchema,
    dependencies=[Depends(require_admin)],
)
def update_image_type(type_id: int, image_type: ImageTypeCreate, db: Session = Depends(get_db)):
    db_type = db.query(ImageTypeModel).filter_by(id=type_id).first()
    if not db_type:
        raise HTTPException(status_code=404, detail="Image type not found")
    db_type.name = image_type.name
    db.commit()
    db.refresh(db_type)
    return db_type


@router.delete(
    "/image-types/{type_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)],
)
def delete_image_type(type_id: int, db: Session = Depends(get_db)):
    db_type = db.query(ImageTypeModel).filter_by(id=type_id).first()
    if not db_type:
        raise HTTPException(status_code=404, detail="Image type not found")
    db.delete(db_type)
    db.commit()
    return None


@router.get("/image-types/", response_model=List[ImageTypeSchema])
def list_image_types(db: Session = Depends(get_db)):
    return db.query(ImageTypeModel).all()
