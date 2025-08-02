import os
import shutil
from pathlib import Path
from typing import List

from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from PIL import Image as PILImage, ExifTags

from database import Base, engine, get_db
import models
import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI()

IMAGE_DIR = Path(os.getenv("IMAGE_DIR", "./image_data"))
IMAGE_DIR.mkdir(parents=True, exist_ok=True)


def _ratio_to_float(value):
    return value[0] / value[1] if isinstance(value, tuple) else float(value)


def _convert_to_degrees(value, ref):
    d, m, s = value
    decimal = _ratio_to_float(d) + _ratio_to_float(m) / 60 + _ratio_to_float(s) / 3600
    return -decimal if ref in ["S", "W"] else decimal


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


def register_image(path: Path, db: Session):
    filename = path.name
    existing = db.query(models.Image).filter_by(filename=filename).first()
    exif_data = extract_exif(path)
    if existing:
        for key, value in exif_data.items():
            setattr(existing, key, value)
        existing.path = str(path)
        db.commit()
        db.refresh(existing)
        return existing
    db_image = models.Image(filename=filename, path=str(path), **exif_data)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


@app.get("/images", response_model=List[schemas.Image])
def read_images(db: Session = Depends(get_db)):
    for file in IMAGE_DIR.iterdir():
        if file.is_file():
            register_image(file, db)
    return db.query(models.Image).all()


@app.post(
    "/images/upload",
    response_model=schemas.ImageDetail,
    status_code=status.HTTP_201_CREATED,
)
async def upload_image(
    file: UploadFile = File(..., description="Immagine da caricare"),
    db: Session = Depends(get_db),
):
    """Carica un'immagine, salva il file ed estrae i metadati EXIF."""
    file_path = IMAGE_DIR / file.filename
    if file_path.exists():
        raise HTTPException(status_code=400, detail="File already exists")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return register_image(file_path, db)


@app.post("/questions/", response_model=schemas.Question)
def create_question(question: schemas.QuestionCreate, db: Session = Depends(get_db)):
    db_question = models.Question(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


@app.put("/questions/{question_id}", response_model=schemas.Question)
def update_question(question_id: int, question: schemas.QuestionCreate, db: Session = Depends(get_db)):
    db_question = db.query(models.Question).filter_by(id=question_id).first()
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")
    db_question.question_text = question.question_text
    db.commit()
    db.refresh(db_question)
    return db_question


@app.delete("/questions/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(question_id: int, db: Session = Depends(get_db)):
    db_question = db.query(models.Question).filter_by(id=question_id).first()
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")
    db.delete(db_question)
    db.commit()
    return None


@app.get("/questions/", response_model=List[schemas.Question])
def list_questions(db: Session = Depends(get_db)):
    return db.query(models.Question).all()


@app.post("/questions/{question_id}/options/", response_model=schemas.Option)
def create_option(question_id: int, option: schemas.OptionCreate, db: Session = Depends(get_db)):
    if not db.query(models.Question).filter_by(id=question_id).first():
        raise HTTPException(status_code=404, detail="Question not found")
    db_option = models.Option(question_id=question_id, option_text=option.option_text)
    db.add(db_option)
    db.commit()
    db.refresh(db_option)
    return db_option


@app.put("/options/{option_id}", response_model=schemas.Option)
def update_option(option_id: int, option: schemas.OptionCreate, db: Session = Depends(get_db)):
    db_option = db.query(models.Option).filter_by(id=option_id).first()
    if not db_option:
        raise HTTPException(status_code=404, detail="Option not found")
    db_option.option_text = option.option_text
    db.commit()
    db.refresh(db_option)
    return db_option


@app.delete("/options/{option_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_option(option_id: int, db: Session = Depends(get_db)):
    db_option = db.query(models.Option).filter_by(id=option_id).first()
    if not db_option:
        raise HTTPException(status_code=404, detail="Option not found")
    db.delete(db_option)
    db.commit()
    return None


@app.get("/questions/{question_id}/options/", response_model=List[schemas.Option])
def list_options(question_id: int, db: Session = Depends(get_db)):
    return db.query(models.Option).filter_by(question_id=question_id).all()


@app.post("/answers/", response_model=schemas.Answer)
def create_answer(answer: schemas.AnswerCreate, db: Session = Depends(get_db)):
    db_answer = models.Answer(**answer.dict())
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer


@app.get("/answers/{image_id}", response_model=List[schemas.Answer])
def list_answers(image_id: int, db: Session = Depends(get_db)):
    return db.query(models.Answer).filter_by(image_id=image_id).all()


@app.post("/annotations/", response_model=schemas.Annotation)
def create_annotation(annotation: schemas.AnnotationCreate, db: Session = Depends(get_db)):
    db_annotation = models.Annotation(**annotation.dict())
    db.add(db_annotation)
    db.commit()
    db.refresh(db_annotation)
    return db_annotation


@app.get("/annotations/{image_id}", response_model=List[schemas.Annotation])
def list_annotations(image_id: int, db: Session = Depends(get_db)):
    return db.query(models.Annotation).filter_by(image_id=image_id).all()


@app.put("/annotations/{annotation_id}", response_model=schemas.Annotation)
def update_annotation(annotation_id: int, annotation: schemas.AnnotationUpdate, db: Session = Depends(get_db)):
    db_annotation = db.query(models.Annotation).filter_by(id=annotation_id).first()
    if not db_annotation:
        raise HTTPException(status_code=404, detail="Annotation not found")
    for field, value in annotation.dict(exclude_unset=True).items():
        setattr(db_annotation, field, value)
    db.commit()
    db.refresh(db_annotation)
    return db_annotation


@app.delete("/annotations/{annotation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_annotation(annotation_id: int, db: Session = Depends(get_db)):
    db_annotation = db.query(models.Annotation).filter_by(id=annotation_id).first()
    if not db_annotation:
        raise HTTPException(status_code=404, detail="Annotation not found")
    db.delete(db_annotation)
    db.commit()
    return None
