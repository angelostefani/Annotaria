from pathlib import Path
import shutil

from fastapi import APIRouter, Depends, Form, HTTPException, Request, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from models import (
    Image as ImageModel,
    Question as QuestionModel,
    Option as OptionModel,
    Answer as AnswerModel,
    Annotation as AnnotationModel,
)
from routers.images import IMAGE_DIR, register_image

templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="/ui", tags=["ui"], include_in_schema=False)


@router.get("/images", response_class=HTMLResponse)
def list_images(request: Request, db: Session = Depends(get_db)):
    for file in IMAGE_DIR.iterdir():
        if file.is_file():
            register_image(file, db)
    images = db.query(ImageModel).all()
    return templates.TemplateResponse("images.html", {"request": request, "images": images})


@router.get("/images/upload", response_class=HTMLResponse)
def upload_image_form(request: Request):
    return templates.TemplateResponse("image_form.html", {"request": request})


@router.post("/images/upload")
async def upload_image(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    file_path = IMAGE_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    register_image(file_path, db)
    return RedirectResponse(url="/ui/images", status_code=303)


@router.get("/images/{image_id}/edit", response_class=HTMLResponse)
def edit_image_form(image_id: int, request: Request, db: Session = Depends(get_db)):
    image = db.query(ImageModel).filter_by(id=image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return templates.TemplateResponse(
        "image_form.html", {"request": request, "image": image}
    )


@router.post("/images/{image_id}/edit")
def edit_image(image_id: int, filename: str = Form(...), db: Session = Depends(get_db)):
    image = db.query(ImageModel).filter_by(id=image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    image.filename = filename
    db.commit()
    return RedirectResponse(url="/ui/images", status_code=303)


@router.post("/images/{image_id}/delete")
def delete_image(image_id: int, db: Session = Depends(get_db)):
    image = db.query(ImageModel).filter_by(id=image_id).first()
    if image:
        file_path = Path(image.path)
        if file_path.exists():
            file_path.unlink()
        db.delete(image)
        db.commit()
    return RedirectResponse(url="/ui/images", status_code=303)


@router.get("/questions", response_class=HTMLResponse)
def list_questions(request: Request, db: Session = Depends(get_db)):
    questions = db.query(QuestionModel).all()
    return templates.TemplateResponse(
        "questions.html", {"request": request, "questions": questions}
    )


@router.get("/questions/create", response_class=HTMLResponse)
def create_question_form(request: Request):
    return templates.TemplateResponse("question_form.html", {"request": request})


@router.post("/questions/create")
def create_question(question_text: str = Form(...), db: Session = Depends(get_db)):
    question = QuestionModel(question_text=question_text)
    db.add(question)
    db.commit()
    return RedirectResponse(url="/ui/questions", status_code=303)


@router.get("/questions/{question_id}/edit", response_class=HTMLResponse)
def edit_question_form(question_id: int, request: Request, db: Session = Depends(get_db)):
    question = db.query(QuestionModel).filter_by(id=question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return templates.TemplateResponse(
        "question_form.html", {"request": request, "question": question}
    )


@router.post("/questions/{question_id}/edit")
def edit_question(
    question_id: int, question_text: str = Form(...), db: Session = Depends(get_db)
):
    question = db.query(QuestionModel).filter_by(id=question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    question.question_text = question_text
    db.commit()
    return RedirectResponse(url="/ui/questions", status_code=303)


@router.post("/questions/{question_id}/delete")
def delete_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(QuestionModel).filter_by(id=question_id).first()
    if question:
        db.delete(question)
        db.commit()
    return RedirectResponse(url="/ui/questions", status_code=303)


@router.get("/questions/{question_id}/options/create", response_class=HTMLResponse)
def create_option_form(question_id: int, request: Request):
    return templates.TemplateResponse(
        "option_form.html", {"request": request, "question_id": question_id}
    )


@router.post("/questions/{question_id}/options/create")
def create_option(
    question_id: int, option_text: str = Form(...), db: Session = Depends(get_db)
):
    option = OptionModel(question_id=question_id, option_text=option_text)
    db.add(option)
    db.commit()
    return RedirectResponse(url="/ui/questions", status_code=303)


@router.get("/options/{option_id}/edit", response_class=HTMLResponse)
def edit_option_form(option_id: int, request: Request, db: Session = Depends(get_db)):
    option = db.query(OptionModel).filter_by(id=option_id).first()
    if not option:
        raise HTTPException(status_code=404, detail="Option not found")
    return templates.TemplateResponse(
        "option_form.html", {"request": request, "option": option}
    )


@router.post("/options/{option_id}/edit")
def edit_option(option_id: int, option_text: str = Form(...), db: Session = Depends(get_db)):
    option = db.query(OptionModel).filter_by(id=option_id).first()
    if not option:
        raise HTTPException(status_code=404, detail="Option not found")
    option.option_text = option_text
    db.commit()
    return RedirectResponse(url="/ui/questions", status_code=303)


@router.post("/options/{option_id}/delete")
def delete_option(option_id: int, db: Session = Depends(get_db)):
    option = db.query(OptionModel).filter_by(id=option_id).first()
    if option:
        db.delete(option)
        db.commit()
    return RedirectResponse(url="/ui/questions", status_code=303)


@router.get("/answers", response_class=HTMLResponse)
def list_answers(request: Request, db: Session = Depends(get_db)):
    answers = db.query(AnswerModel).all()
    return templates.TemplateResponse(
        "answers.html", {"request": request, "answers": answers}
    )


@router.get("/answers/create", response_class=HTMLResponse)
def create_answer_form(request: Request):
    return templates.TemplateResponse("answer_form.html", {"request": request})


@router.post("/answers/create")
def create_answer(
    image_id: int = Form(...),
    question_id: int = Form(...),
    selected_option_id: int = Form(...),
    user_id: int = Form(...),
    db: Session = Depends(get_db),
):
    answer = AnswerModel(
        image_id=image_id,
        question_id=question_id,
        selected_option_id=selected_option_id,
        user_id=user_id,
    )
    db.add(answer)
    db.commit()
    return RedirectResponse(url="/ui/answers", status_code=303)


@router.get("/answers/{answer_id}/edit", response_class=HTMLResponse)
def edit_answer_form(answer_id: int, request: Request, db: Session = Depends(get_db)):
    answer = db.query(AnswerModel).filter_by(id=answer_id).first()
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    return templates.TemplateResponse(
        "answer_form.html", {"request": request, "answer": answer}
    )


@router.post("/answers/{answer_id}/edit")
def edit_answer(
    answer_id: int,
    image_id: int = Form(...),
    question_id: int = Form(...),
    selected_option_id: int = Form(...),
    user_id: int = Form(...),
    db: Session = Depends(get_db),
):
    answer = db.query(AnswerModel).filter_by(id=answer_id).first()
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    answer.image_id = image_id
    answer.question_id = question_id
    answer.selected_option_id = selected_option_id
    answer.user_id = user_id
    db.commit()
    return RedirectResponse(url="/ui/answers", status_code=303)


@router.post("/answers/{answer_id}/delete")
def delete_answer(answer_id: int, db: Session = Depends(get_db)):
    answer = db.query(AnswerModel).filter_by(id=answer_id).first()
    if answer:
        db.delete(answer)
        db.commit()
    return RedirectResponse(url="/ui/answers", status_code=303)


@router.get("/annotations", response_class=HTMLResponse)
def list_annotations(request: Request, db: Session = Depends(get_db)):
    annotations = db.query(AnnotationModel).all()
    return templates.TemplateResponse(
        "annotations.html", {"request": request, "annotations": annotations}
    )


@router.get("/annotations/create", response_class=HTMLResponse)
def create_annotation_form(request: Request):
    return templates.TemplateResponse("annotation_form.html", {"request": request})


@router.post("/annotations/create")
def create_annotation(
    image_id: int = Form(...),
    label: str = Form(...),
    x: float = Form(...),
    y: float = Form(...),
    width: float = Form(...),
    height: float = Form(...),
    user_id: int = Form(...),
    db: Session = Depends(get_db),
):
    annotation = AnnotationModel(
        image_id=image_id,
        label=label,
        x=x,
        y=y,
        width=width,
        height=height,
        user_id=user_id,
    )
    db.add(annotation)
    db.commit()
    return RedirectResponse(url="/ui/annotations", status_code=303)


@router.get("/annotations/{annotation_id}/edit", response_class=HTMLResponse)
def edit_annotation_form(
    annotation_id: int, request: Request, db: Session = Depends(get_db)
):
    annotation = db.query(AnnotationModel).filter_by(id=annotation_id).first()
    if not annotation:
        raise HTTPException(status_code=404, detail="Annotation not found")
    return templates.TemplateResponse(
        "annotation_form.html", {"request": request, "annotation": annotation}
    )


@router.post("/annotations/{annotation_id}/edit")
def edit_annotation(
    annotation_id: int,
    image_id: int = Form(...),
    label: str = Form(...),
    x: float = Form(...),
    y: float = Form(...),
    width: float = Form(...),
    height: float = Form(...),
    user_id: int = Form(...),
    db: Session = Depends(get_db),
):
    annotation = db.query(AnnotationModel).filter_by(id=annotation_id).first()
    if not annotation:
        raise HTTPException(status_code=404, detail="Annotation not found")
    annotation.image_id = image_id
    annotation.label = label
    annotation.x = x
    annotation.y = y
    annotation.width = width
    annotation.height = height
    annotation.user_id = user_id
    db.commit()
    return RedirectResponse(url="/ui/annotations", status_code=303)


@router.post("/annotations/{annotation_id}/delete")
def delete_annotation(annotation_id: int, db: Session = Depends(get_db)):
    annotation = db.query(AnnotationModel).filter_by(id=annotation_id).first()
    if annotation:
        db.delete(annotation)
        db.commit()
    return RedirectResponse(url="/ui/annotations", status_code=303)
