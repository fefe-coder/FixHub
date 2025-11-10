from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Task
from database import get_db

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/")
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks


@router.get("/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/")
def create_task(title: str, description: str, property_id: int, db: Session = Depends(get_db)):
    new_task = Task(title=title, description=description, property_id=property_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"message": "Task created", "id": new_task.id}
