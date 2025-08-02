import os
from pathlib import Path
from typing import List

from fastapi import FastAPI, Depends, HTTPException, status
from PIL import Image as PILImage, ExifTags
from sqlalchemy.orm import Session

from database import Base, engine, get_db
import models
import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI()

IMAGE_DIR = Path(os.getenv("IMAGE_DIR", "./image_data"))
IMAGE_DIR.mkdir(parents=True, exist_ok=True)


def _convert_to_degrees(value):
    """Convert GPS coordinates stored as rationals to float degrees."""
    d, m, s = value
    return (
        d[0] / d[1]
        + (m[0] / m[1]) / 60
        + (s[0] / s[1]) / 3600
    )


@app.get("/images", response_model=List[schemas.Image])
def read_images(db: Session = Depends(get_db)):
    for file in IMAGE_DIR.iterdir():
        if file.is_file():
            existing = db.query(models.Image).filter_by(filename=file.name).first()
            if not existing:
                exif_data = {}
                try:
                    with PILImage.open(file) as img:
                        raw_exif = img._getexif() or {}
                        exif = {ExifTags.TAGS.get(k, k): v for k, v in raw_exif.items()}

                        exif_data["exif_datetime"] = exif.get("DateTimeOriginal") or exif.get("DateTime")
                        exif_data["exif_camera_make"] = exif.get("Make")
                        exif_data["exif_camera_model"] = exif.get("Model")
                        exif_data["exif_lens_model"] = exif.get("LensModel")

                        fl = exif.get("FocalLength")
                        if isinstance(fl, tuple) and fl[1]:
                            exif_data["exif_focal_length"] = fl[0] / fl[1]
                        else:
                            exif_data["exif_focal_length"] = fl

                        fnum = exif.get("FNumber")
                        if isinstance(fnum, tuple) and fnum[1]:
                            exif_data["exif_aperture"] = fnum[0] / fnum[1]
                        else:
                            exif_data["exif_aperture"] = fnum

                        iso = exif.get("ISOSpeedRatings") or exif.get("PhotographicSensitivity")
                        if isinstance(iso, (list, tuple)):
                            iso = iso[0]
                        exif_data["exif_iso"] = iso

                        shutter = exif.get("ExposureTime")
                        if isinstance(shutter, tuple) and shutter[1]:
                            exif_data["exif_shutter_speed"] = f"{shutter[0]}/{shutter[1]}"
                        else:
                            exif_data["exif_shutter_speed"] = str(shutter) if shutter else None

                        orientation = exif.get("Orientation")
                        exif_data["exif_orientation"] = str(orientation) if orientation else None

                        width = exif.get("ExifImageWidth") or img.width
                        height = exif.get("ExifImageHeight") or img.height
                        exif_data["exif_image_width"] = int(width) if width else None
                        exif_data["exif_image_height"] = int(height) if height else None

                        gps_info = exif.get("GPSInfo")
                        if isinstance(gps_info, dict):
                            gps = {ExifTags.GPSTAGS.get(k, k): v for k, v in gps_info.items()}
                            lat = gps.get("GPSLatitude")
                            lat_ref = gps.get("GPSLatitudeRef")
                            lon = gps.get("GPSLongitude")
                            lon_ref = gps.get("GPSLongitudeRef")
                            alt = gps.get("GPSAltitude")

                            if lat and lat_ref:
                                try:
                                    exif_data["exif_gps_lat"] = _convert_to_degrees(lat) * (
                                        1 if lat_ref == "N" else -1
                                    )
                                except Exception:
                                    pass
                            if lon and lon_ref:
                                try:
                                    exif_data["exif_gps_lon"] = _convert_to_degrees(lon) * (
                                        1 if lon_ref == "E" else -1
                                    )
                                except Exception:
                                    pass
                            if alt:
                                if isinstance(alt, tuple) and alt[1]:
                                    exif_data["exif_gps_alt"] = alt[0] / alt[1]
                                else:
                                    exif_data["exif_gps_alt"] = alt

                        exif_data["exif_drone_model"] = exif.get("CameraModelName") or exif.get("Make")
                        exif_data["exif_flight_id"] = exif.get("FlightID")
                        exif_data["exif_pitch"] = (
                            exif.get("GimbalPitchDegree") or exif.get("Pitch")
                        )
                        exif_data["exif_roll"] = exif.get("GimbalRollDegree") or exif.get("Roll")
                        exif_data["exif_yaw"] = exif.get("GimbalYawDegree") or exif.get("Yaw")
                except Exception:
                    exif_data = {}

                db_image = models.Image(
                    filename=file.name,
                    path=str(file),
                    **exif_data,
                )
                db.add(db_image)
    db.commit()
    return db.query(models.Image).all()


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
