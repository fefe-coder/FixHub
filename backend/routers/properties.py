from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Property
from database import get_db

router = APIRouter(prefix="/properties", tags=["Properties"])


@router.get("/")
def get_properties(db: Session = Depends(get_db)):
    properties = db.query(Property).all()
    return properties


@router.get("/{property_id}")
def get_property(property_id: int, db: Session = Depends(get_db)):
    property = db.query(Property).filter(Property.id == property_id).first()
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    return property


@router.post("/")
def create_property(name: str, address: str, owner: str, db: Session = Depends(get_db)):
    new_property = Property(name=name, address=address, owner=owner)
    db.add(new_property)
    db.commit()
    db.refresh(new_property)
    return {"message": "Property created", "id": new_property.id}
