from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import os
from docx import Document
import fitz  # PyMuPDF

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        resume.file.seek(0)  # Reset file pointer!
        resume_text = read_pdf(resume.file)
    elif extension == ".docx":
        resume.file.seek(0)  # Reset file pointer!
        resume_text = read_docx(resume.file)
    else:
        return {"error": "Unsupported file type"}

    return {
        "resume": resume.filename,
        "preview": resume_text[:300],
        "job_desc": job_desc[:150]
    }
