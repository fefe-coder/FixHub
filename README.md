# FixHub

Simple property maintenance & inspection manager.

## Stack

- Backend: FastAPI + SQLite + SQLAlchemy + JWT + ReportLab
- Frontend: React (Vite) + TailwindCSS + Axios
- Auth: Email/password (JWT)
- Features:
  - Manage properties
  - Manage maintenance tasks
  - Assign to workers
  - Upload before/after photos
  - Generate simple PDF report

## Dev

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.main:app --reload
