from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional
import os
import shutil

import models
from database import engine, SessionLocal

app = FastAPI()

# Create database tables
models.Base.metadata.create_all(bind=engine)

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Health check
@app.get("/health")
def health():
    return {"status": "API is running"}


# Upload Resume
@app.post("/upload")
async def upload_resume(
    name: str = Form(...),
    dob: str = Form(...),
    phone: str = Form(...),
    address: str = Form(...),
    education: str = Form(...),
    graduation_year: int = Form(...),
    experience: int = Form(...),
    skills: str = Form(...),
    resume: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # Save file
    file_path = os.path.join(UPLOAD_FOLDER, resume.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)

    # Save to database
    candidate = models.Candidate(
        name=name,
        dob=dob,
        phone=phone,
        address=address,
        education=education,
        graduation_year=graduation_year,
        experience=experience,
        skills=skills,
        resume_file=file_path
    )

    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    return {"message": "Resume uploaded successfully", "id": candidate.id}


# List candidates with filters
@app.get("/candidates")
def get_candidates(
    skill: Optional[str] = None,
    experience: Optional[int] = None,
    graduation_year: Optional[int] = None,
    db: Session = Depends(get_db)
):

    query = db.query(models.Candidate)

    if skill:
        query = query.filter(models.Candidate.skills.contains(skill))

    if experience is not None:
        query = query.filter(models.Candidate.experience == experience)

    if graduation_year is not None:
        query = query.filter(models.Candidate.graduation_year == graduation_year)

    return query.all()


# Get candidate by ID
@app.get("/candidate/{id}")
def get_candidate(id: int, db: Session = Depends(get_db)):

    candidate = db.query(models.Candidate).filter(models.Candidate.id == id).first()

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    return candidate


# Delete candidate
@app.delete("/candidate/{id}")
def delete_candidate(id: int, db: Session = Depends(get_db)):

    candidate = db.query(models.Candidate).filter(models.Candidate.id == id).first()

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    db.delete(candidate)
    db.commit()

    return {"message": "Candidate deleted"}