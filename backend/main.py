from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import os
from docx import Document
import fitz  # PyMuPDF

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Functions to read different file types
def read_txt(file_bytes):
    return file_bytes.decode('utf-8', errors='ignore')

def read_docx(file):
    doc = Document(file)
    return '\n'.join([para.text for para in doc.paragraphs])

def read_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as pdf:
        for page in pdf:
            text += page.get_text()
    return text

# Function to calculate match score
def calculate_match_score(resume_text, job_desc):
    resume_words = set(resume_text.lower().split())
    job_desc_words = set(job_desc.lower().split())
    matching_words = resume_words.intersection(job_desc_words)
    
    if not job_desc_words:
        return 0
    
    score = (len(matching_words) / len(job_desc_words)) * 100
    return round(score, 2)

# API Endpoint
@app.post("/analyze/")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_desc: str = Form(...)
):
    extension = os.path.splitext(resume.filename)[1].lower()

    if extension == ".txt":
        contents = await resume.read()
        resume_text = read_txt(contents)
    elif extension == ".pdf":
        resume.file.seek(0)
        resume_text = read_pdf(resume.file)
    elif extension == ".docx":
        resume.file.seek(0)
        resume_text = read_docx(resume.file)
    else:
        return {"error": "Unsupported file type"}

    score = calculate_match_score(resume_text, job_desc)

    return {
        "resume": resume.filename,
        "preview": resume_text[:7000],  # ✨ 7000 characters now
        "job_desc": job_desc[:7000],    # ✨ 7000 characters now
        "score": score                  # Match Score %
    }
