from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

from database import engine, Base
import models
from routers import auth, properties, tasks, uploads
from utils.pdf_report import generate_property_report

# Initialize database
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="FixHub API",
    description="Backend API for FixHub project — property and repair management system",
    version="1.0.0"
)

# Include routers
app.include_router(auth.router)
app.include_router(properties.router)
app.include_router(tasks.router)
app.include_router(uploads.router)

# --- Static file handling ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Create /static folder automatically (prevents Render crash)
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# --- Root route ---
@app.get("/")
def root():
    return {"message": "FixHub backend is running successfully!"}
