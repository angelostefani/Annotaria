import os
from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import User as UserModel


class AppSettings(BaseSettings):
    allowed_origins: str = "*"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = AppSettings()

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Monta la cartella 'static' accessibile via /static
app.mount("/static", StaticFiles(directory="static"), name="static")

# Se usi template:
templates = Jinja2Templates(directory="templates")



app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.allowed_origins.split(",")],
    allow_methods=["*"],
    allow_headers=["*"],
)

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

from routers import (
    annotations,
    answers,
    expert_types,
    image_types,
    images,
    labels,
    questions,
    users,
    ui,
)
from routers.images import IMAGE_DIR

app.include_router(images.router)
app.include_router(image_types.router)
app.include_router(expert_types.router)
app.include_router(questions.router)
app.include_router(answers.router)
app.include_router(annotations.router)
app.include_router(labels.router)
app.include_router(users.router)
app.include_router(ui.router)

app.mount("/image_data", StaticFiles(directory=str(IMAGE_DIR)), name="image_data")

