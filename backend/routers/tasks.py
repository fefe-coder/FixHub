from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from .. import models
from ..database import get_db
from .auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    property_id: int
    assigned_to: Optional[str] = None
    due_date: Optional[datetime] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    assigned_to: Optional[str] = None
    due_date: Optional[datetime] = None


@router.get("/")
def list_tasks(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return (
        db.query(models.Task)
        .join(models.Property)
        .filter(models.Property.manager_id == current_user.id)
        .all()
    )


@router.get("/property/{property_id}")
def tasks_by_property(
    property_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return (
        db.query(models.Task)
        .join(models.Property)
        .filter(
            models.Task.property_id == property_id,
            models.Property.manager_id == current_user.id,
        )
        .all()
    )


@router.get("/{task_id}")
def get_task(
    task_id: int,
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
    return task


@router.post("/")
def create_task(
    data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    prop = db.query(models.Property).filter(
        models.Property.id == data.property_id,
        models.Property.manager_id == current_user.id,
    ).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")

    task = models.Task(
        title=data.title,
        description=data.description,
        property_id=data.property_id,
        assigned_to=data.assigned_to,
        due_date=data.due_date,
        status="Pending",
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.put("/{task_id}")
def update_task(
    task_id: int,
    data: TaskUpdate,
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

    for field, value in data.dict(exclude_unset=True).items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
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
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}
