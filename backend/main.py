from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from routers import auth, properties, tasks, uploads
from utils.pdf_report import generate_property_report
from routers.auth import get_current_user
import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FixHub API")

# CORS (adjust for prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files (for uploaded photos & reports)
app.mount("/static", StaticFiles(directory="backend"), name="static")

app.include_router(auth.router)
app.include_router(properties.router)
app.include_router(tasks.router)
app.include_router(uploads.router)


@app.get("/")
def root():
    return {"message": "FixHub API running"}


@app.get("/reports/property/{property_id}")
def property_report(
    property_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    prop = db.query(models.Property).filter(
        models.Property.id == property_id,
        models.Property.manager_id == current_user.id,
    ).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")

    path = generate_property_report(property_id, db)
    return FileResponse(path, media_type="application/pdf", filename=path.split("/")[-1])
