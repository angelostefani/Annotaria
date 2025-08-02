import os
from pathlib import Path
from typing import List

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import Base, engine, get_db
import models
import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI()

IMAGE_DIR = Path(os.getenv("IMAGE_DIR", "./image_data"))
IMAGE_DIR.mkdir(parents=True, exist_ok=True)


@app.get("/images", response_model=List[schemas.Image])
def read_images(db: Session = Depends(get_db)):
    for file in IMAGE_DIR.iterdir():
        if file.is_file():
            existing = db.query(models.Image).filter_by(filename=file.name).first()
            if not existing:
                db_image = models.Image(filename=file.name, path=str(file))
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
