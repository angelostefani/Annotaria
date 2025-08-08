from pathlib import Path
from typing import List
import os
import shutil

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    UploadFile,
    File,
    Form,
    Response,
)
from sqlalchemy.orm import Session
from PIL import Image as PILImage, ExifTags

from database import get_db
from models import Image as ImageModel, ImageType as ImageTypeModel, User as UserModel
from schemas import Image as ImageSchema, ImageDetail, ImageUpdate
from main import get_current_user

router = APIRouter()

IMAGE_DIR = Path(os.getenv("IMAGE_DIR", "./image_data"))
IMAGE_DIR.mkdir(parents=True, exist_ok=True)


def _ratio_to_float(value):
    return value[0] / value[1] if isinstance(value, tuple) else float(value)


def _convert_to_degrees(value, ref):
    d, m, s = value
    decimal = _ratio_to_float(d) + _ratio_to_float(m) / 60 + _ratio_to_float(s) / 3600
    return -decimal if ref in ["S", "W"] else decimal


def require_admin(current_user: UserModel = Depends(get_current_user)):
    if current_user.role != "Amministratore":
        raise HTTPException(status_code=403, detail="Forbidden")
    return current_user


def extract_exif(path: Path):
    data = {}
    try:
        with PILImage.open(path) as img:
            exif = img._getexif() or {}
    except Exception:
        return data

    gps_info = {}
    for tag_id, value in exif.items():
        tag = ExifTags.TAGS.get(tag_id, tag_id)
        if tag == "DateTime":
            data["exif_datetime"] = value
        elif tag == "Make":
            data["exif_camera_make"] = value
        elif tag == "Model":
            data["exif_camera_model"] = value
        elif tag == "LensModel":
            data["exif_lens_model"] = value
        elif tag == "FocalLength":
            data["exif_focal_length"] = _ratio_to_float(value)
        elif tag in ("FNumber", "ApertureValue"):
            data["exif_aperture"] = _ratio_to_float(value)
        elif tag in ("ISOSpeedRatings", "PhotographicSensitivity"):
            data["exif_iso"] = int(_ratio_to_float(value))
        elif tag in ("ShutterSpeedValue", "ExposureTime"):
            data["exif_shutter_speed"] = str(value)
        elif tag == "Orientation":
            data["exif_orientation"] = str(value)
        elif tag == "ImageWidth":
            data["exif_image_width"] = int(value)
        elif tag == "ImageLength":
            data["exif_image_height"] = int(value)
        elif tag == "GPSInfo":
            for t in value:
                sub_tag = ExifTags.GPSTAGS.get(t, t)
                gps_info[sub_tag] = value[t]

    if gps_info:
        lat = gps_info.get("GPSLatitude")
        lat_ref = gps_info.get("GPSLatitudeRef")
        lon = gps_info.get("GPSLongitude")
        lon_ref = gps_info.get("GPSLongitudeRef")
        alt = gps_info.get("GPSAltitude")
        alt_ref = gps_info.get("GPSAltitudeRef")
        if lat and lat_ref:
            data["exif_gps_lat"] = _convert_to_degrees(lat, lat_ref)
        if lon and lon_ref:
            data["exif_gps_lon"] = _convert_to_degrees(lon, lon_ref)
        if alt:
            altitude = _ratio_to_float(alt)
            if alt_ref == 1:
                altitude = -altitude
            data["exif_gps_alt"] = altitude

    return data


def register_image(path: Path, db: Session, image_type_id: int | None = None):
    filename = path.name
    existing = db.query(ImageModel).filter_by(filename=filename).first()
    exif_data = extract_exif(path)
    if existing:
        for key, value in exif_data.items():
            setattr(existing, key, value)
        existing.path = str(path)
        if image_type_id is not None:
            existing.image_type_id = image_type_id
        db.commit()
        db.refresh(existing)
        return existing
    db_image = ImageModel(
        filename=filename,
        path=str(path),
        image_type_id=image_type_id,
        **exif_data,
    )
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


@router.get("/images", response_model=List[ImageSchema])
def read_images(db: Session = Depends(get_db)):
    for file in IMAGE_DIR.iterdir():
        if file.is_file():
            register_image(file, db)
    return db.query(ImageModel).all()


@router.get("/images/{image_id}", response_model=ImageDetail)
def read_image(image_id: int, db: Session = Depends(get_db)):
    image = db.query(ImageModel).filter(ImageModel.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return image


@router.post(
    "/images/upload",
    response_model=ImageDetail,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)],
)
async def upload_image(
    file: UploadFile = File(..., description="Immagine da caricare"),
    image_type_id: int | None = Form(None),
    db: Session = Depends(get_db),
):
    """Carica un'immagine, salva il file ed estrae i metadati EXIF."""
    file_path = IMAGE_DIR / file.filename
    if file_path.exists():
        raise HTTPException(status_code=400, detail="File already exists")
    if image_type_id is not None and not db.query(ImageTypeModel).filter_by(id=image_type_id).first():
        raise HTTPException(status_code=404, detail="Image type not found")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return register_image(file_path, db, image_type_id=image_type_id)


@router.put(
    "/images/{image_id}",
    response_model=ImageDetail,
    dependencies=[Depends(require_admin)],
)
def update_image(image_id: int, image_data: ImageUpdate, db: Session = Depends(get_db)):
    image = db.query(ImageModel).filter(ImageModel.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    data = image_data.dict(exclude_unset=True)
    if "image_type_id" in data and data["image_type_id"] is not None:
        if not db.query(ImageTypeModel).filter_by(id=data["image_type_id"]).first():
            raise HTTPException(status_code=404, detail="Image type not found")
    for key, value in data.items():
        setattr(image, key, value)
    db.commit()
    db.refresh(image)
    return image


@router.delete(
    "/images/{image_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)],
)
def delete_image(image_id: int, db: Session = Depends(get_db)):
    image = db.query(ImageModel).filter(ImageModel.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    file_path = Path(image.path)
    if file_path.exists():
        file_path.unlink()
    db.delete(image)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
