import os
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
from .. import models
from ..database import get_db
from .auth import get_current_user

router = APIRouter(prefix="/uploads", tags=["Uploads"])

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/task-photo")
async def upload_task_photo(
    task_id: int = Form(...),
    photo_type: str = Form("before"),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    task = (
        db.query(models.Task)
        .join(models.Property)
        .filter(
            models.Task.id == task_id,
            models.Property.manager_id == current_user.id,
        )
        .first()
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid4().hex}{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as buffer:
        buffer.write(await file.read())

    rel_path = f"/static/uploads/{filename}"

    photo = models.TaskPhoto(
        task_id=task.id,
        url=rel_path,
        photo_type=photo_type,
    )
    db.add(photo)
    db.commit()
    db.refresh(photo)

    return {"url": rel_path, "photo": photo.id}
