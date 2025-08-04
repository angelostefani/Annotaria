import os
import shutil
from pathlib import Path
from typing import List

from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from PIL import Image as PILImage, ExifTags
from datetime import datetime, timedelta

from database import Base, engine, get_db
from models import (
    Image as ImageModel,
    Question as QuestionModel,
    Option as OptionModel,
    Answer as AnswerModel,
    Annotation as AnnotationModel,
    User as UserModel,
)
from schemas import (
    Image as ImageSchema,
    ImageDetail,
    Question as QuestionSchema,
    QuestionCreate,
    Option as OptionSchema,
    OptionCreate,
    Answer as AnswerSchema,
    AnswerCreate,
    Annotation as AnnotationSchema,
    AnnotationCreate,
    AnnotationUpdate,
)
from schemas.user import UserCreate, UserResponse, Token

Base.metadata.create_all(bind=engine)

app = FastAPI()

IMAGE_DIR = Path(os.getenv("IMAGE_DIR", "./image_data"))
IMAGE_DIR.mkdir(parents=True, exist_ok=True)

SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(UserModel).filter_by(username=username).first()
    if user is None:
        raise credentials_exception
    return user


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
    existing = db.query(ImageModel).filter_by(filename=filename).first()
    exif_data = extract_exif(path)
    if existing:
        for key, value in exif_data.items():
            setattr(existing, key, value)
        existing.path = str(path)
        db.commit()
        db.refresh(existing)
        return existing
    db_image = ImageModel(filename=filename, path=str(path), **exif_data)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter_by(username=user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user = UserModel(
        username=user.username, hashed_password=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(UserModel).filter_by(username=form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=UserResponse)
def read_users_me(current_user: UserModel = Depends(get_current_user)):
    return current_user


@app.get("/images", response_model=List[ImageSchema])
def read_images(db: Session = Depends(get_db)):
    for file in IMAGE_DIR.iterdir():
        if file.is_file():
            register_image(file, db)
    return db.query(ImageModel).all()


@app.post(
    "/images/upload",
    response_model=ImageDetail,
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


@app.post("/questions/", response_model=QuestionSchema)
def create_question(question: QuestionCreate, db: Session = Depends(get_db)):
    db_question = QuestionModel(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


@app.put("/questions/{question_id}", response_model=QuestionSchema)
def update_question(question_id: int, question: QuestionCreate, db: Session = Depends(get_db)):
    db_question = db.query(QuestionModel).filter_by(id=question_id).first()
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")
    db_question.question_text = question.question_text
    db.commit()
    db.refresh(db_question)
    return db_question


@app.delete("/questions/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(question_id: int, db: Session = Depends(get_db)):
    db_question = db.query(QuestionModel).filter_by(id=question_id).first()
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")
    db.delete(db_question)
    db.commit()
    return None


@app.get("/questions/", response_model=List[QuestionSchema])
def list_questions(db: Session = Depends(get_db)):
    return db.query(QuestionModel).all()


@app.post("/questions/{question_id}/options", response_model=OptionSchema)
def create_option(question_id: int, option: OptionCreate, db: Session = Depends(get_db)):
    if not db.query(QuestionModel).filter_by(id=question_id).first():
        raise HTTPException(status_code=404, detail="Question not found")
    db_option = OptionModel(question_id=question_id, option_text=option.option_text)
    db.add(db_option)
    db.commit()
    db.refresh(db_option)
    return db_option


@app.put("/options/{option_id}", response_model=OptionSchema)
def update_option(option_id: int, option: OptionCreate, db: Session = Depends(get_db)):
    db_option = db.query(OptionModel).filter_by(id=option_id).first()
    if not db_option:
        raise HTTPException(status_code=404, detail="Option not found")
    db_option.option_text = option.option_text
    db.commit()
    db.refresh(db_option)
    return db_option


@app.delete("/options/{option_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_option(option_id: int, db: Session = Depends(get_db)):
    db_option = db.query(OptionModel).filter_by(id=option_id).first()
    if not db_option:
        raise HTTPException(status_code=404, detail="Option not found")
    db.delete(db_option)
    db.commit()
    return None


@app.get("/questions/{question_id}/options", response_model=List[OptionSchema])
def list_options(question_id: int, db: Session = Depends(get_db)):
    return db.query(OptionModel).filter_by(question_id=question_id).all()


@app.post("/answers/", response_model=AnswerSchema)
def create_answer(answer: AnswerCreate, db: Session = Depends(get_db)):
    db_answer = AnswerModel(**answer.dict())
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer


@app.get("/answers/{image_id}", response_model=List[AnswerSchema])
def list_answers(image_id: int, db: Session = Depends(get_db)):
    return db.query(AnswerModel).filter_by(image_id=image_id).all()


@app.post("/annotations/", response_model=AnnotationSchema)
def create_annotation(annotation: AnnotationCreate, db: Session = Depends(get_db)):
    db_annotation = AnnotationModel(**annotation.dict())
    db.add(db_annotation)
    db.commit()
    db.refresh(db_annotation)
    return db_annotation


@app.get("/annotations/{image_id}", response_model=List[AnnotationSchema])
def list_annotations(image_id: int, db: Session = Depends(get_db)):
    return db.query(AnnotationModel).filter_by(image_id=image_id).all()


@app.put("/annotations/{annotation_id}", response_model=AnnotationSchema)
def update_annotation(annotation_id: int, annotation: AnnotationUpdate, db: Session = Depends(get_db)):
    db_annotation = db.query(AnnotationModel).filter_by(id=annotation_id).first()
    if not db_annotation:
        raise HTTPException(status_code=404, detail="Annotation not found")
    for field, value in annotation.dict(exclude_unset=True).items():
        setattr(db_annotation, field, value)
    db.commit()
    db.refresh(db_annotation)
    return db_annotation


@app.delete("/annotations/{annotation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_annotation(annotation_id: int, db: Session = Depends(get_db)):
    db_annotation = db.query(AnnotationModel).filter_by(id=annotation_id).first()
    if not db_annotation:
        raise HTTPException(status_code=404, detail="Annotation not found")
    db.delete(db_annotation)
    db.commit()
    return None
