from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .. import models
from ..database import get_db
from .auth import get_current_user

router = APIRouter(prefix="/properties", tags=["Properties"])


class PropertyCreate(BaseModel):
    name: str
    address: str


@router.get("/")
def list_properties(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return db.query(models.Property).filter(
        models.Property.manager_id == current_user.id
    ).all()


@router.post("/")
def create_property(
    prop: PropertyCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    new_p = models.Property(
        name=prop.name,
        address=prop.address,
        manager_id=current_user.id,
    )
    db.add(new_p)
    db.commit()
    db.refresh(new_p)
    return new_p


@router.get("/{property_id}")
def get_property(
    property_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    p = db.query(models.Property).filter(
        models.Property.id == property_id,
        models.Property.manager_id == current_user.id
    ).first()
    if not p:
        raise HTTPException(status_code=404, detail="Property not found")
    return p


@router.delete("/{property_id}")
def delete_property(
    property_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    p = db.query(models.Property).filter(
        models.Property.id == property_id,
        models.Property.manager_id == current_user.id
    ).first()
    if not p:
        raise HTTPException(status_code=404, detail="Property not found")
    db.delete(p)
    db.commit()
    return {"message": "Property deleted"}
