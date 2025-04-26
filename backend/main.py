from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from PyPDF2 import PdfReader
import docx

app = FastAPI()

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    return "\n".join([page.extract_text() or "" for page in reader.pages])

@app.post("/analyze/")
async def analyze_resume(resume: UploadFile = File(...), job_desc: str = Form(...)):
    try:
        content = await resume.read()
        filename = resume.filename.lower()

        if filename.endswith('.txt'):
            resume_text = content.decode("utf-8", errors="ignore")
        elif filename.endswith('.pdf'):
            with open("temp.pdf", "wb") as f:
                f.write(content)
            resume_text = extract_text_from_pdf("temp.pdf")
        elif filename.endswith('.docx'):
            with open("temp.docx", "wb") as f:
                f.write(content)
            resume_text = extract_text_from_docx("temp.docx")
        else:
            return JSONResponse(status_code=400, content={"error": "Unsupported file format"})

        # Dummy analysis
        overlap = set(resume_text.lower().split()) & set(job_desc.lower().split())
        score = len(overlap)

        return {"result": f"Matched words: {', '.join(overlap)}\nScore: {score}"}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
