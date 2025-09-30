from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from models import User as UserModel
from schemas.user import UserCreate, UserResponse, Token, PasswordChangeRequest
from main import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
)

router = APIRouter()

@router.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter_by(username=user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user = UserModel(
        username=user.username,
        hashed_password=get_password_hash(user.password),
        role=user.role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(UserModel).filter_by(username=form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=UserResponse)
def read_users_me(current_user: UserModel = Depends(get_current_user)):
    return current_user

@router.post("/users/me/password")
def change_password(
    payload: PasswordChangeRequest,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not verify_password(payload.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect current password")
    if payload.new_password != payload.new_password_confirm:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    if len(payload.new_password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")
    if verify_password(payload.new_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="New password must be different from the current password")

    current_user.hashed_password = get_password_hash(payload.new_password)
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return {"detail": "Password updated"}


