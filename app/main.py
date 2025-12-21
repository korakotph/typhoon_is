from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import shutil, uuid, os

from app.ocr import extract_text
from app.typhoon_ai import analyze_finance
from app.text_cleaner import normalize_text

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def ui():
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()


@app.post("/analyze")
def analyze_document(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    file_path = f"{UPLOAD_DIR}/{file_id}_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    ocr_result = extract_text(file_path)
    ocr_result["text"] = normalize_text(ocr_result["text"])

    analysis = analyze_finance(ocr_result)

    return {
        "filename": file.filename,
        "ocr": ocr_result,
        "analysis": analysis
    }
