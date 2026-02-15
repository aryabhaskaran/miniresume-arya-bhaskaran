from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from typing import Optional
import os
import shutil

app = FastAPI()

# In-memory storage
candidates = []
candidate_id = 1

UPLOAD_FOLDER = "uploads"

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
    resume: UploadFile = File(...)
):
    global candidate_id

    # Save file
    file_path = os.path.join(UPLOAD_FOLDER, resume.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)

    candidate = {
        "id": candidate_id,
        "name": name,
        "dob": dob,
        "phone": phone,
        "address": address,
        "education": education,
        "graduation_year": graduation_year,
        "experience": experience,
        "skills": skills.split(","),
        "resume_file": file_path
    }

    candidates.append(candidate)
    candidate_id += 1

    return {"message": "Resume uploaded successfully", "id": candidate["id"]}


# List candidates with filters
@app.get("/candidates")
def get_candidates(
    skill: Optional[str] = None,
    experience: Optional[int] = None,
    graduation_year: Optional[int] = None
):
    result = candidates

    if skill:
        result = [c for c in result if skill.lower() in [s.lower() for s in c["skills"]]]

    if experience is not None:
        result = [c for c in result if c["experience"] == experience]

    if graduation_year is not None:
        result = [c for c in result if c["graduation_year"] == graduation_year]

    return result


# Get candidate by ID
@app.get("/candidate/{id}")
def get_candidate(id: int):
    for c in candidates:
        if c["id"] == id:
            return c
    raise HTTPException(status_code=404, detail="Candidate not found")


# Delete candidate
@app.delete("/candidate/{id}")
def delete_candidate(id: int):
    global candidates
    candidates = [c for c in candidates if c["id"] != id]
    return {"message": "Candidate deleted"}
