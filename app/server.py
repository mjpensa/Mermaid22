from fastapi import FastAPI, UploadFile, File, Response, Query
from fastapi.responses import StreamingResponse
import tempfile
import os
import json
import io
from pdf_pipeline import process_pdf
from docx_pipeline import process_docx

app = FastAPI()

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.post("/render")
def render(file: UploadFile = File(...), log: bool = Query(False)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp:
        tmp.write(file.file.read())
        input_path = tmp.name
    output_path = tempfile.mktemp(suffix='.pdf')
    logs = []
    def log_callback(*args):
        logs.append(args)
    if file.filename.endswith('.pdf'):
        process_pdf(input_path, output_path, log_callback)
    elif file.filename.endswith('.docx'):
        process_docx(input_path, output_path, log_callback)
    else:
        raise ValueError("Unsupported file type")
    os.unlink(input_path)
    with open(output_path, 'rb') as f:
        pdf_data = f.read()
    os.unlink(output_path)
    headers = {}
    if log:
        headers['X-MermaidPaper-Log'] = json.dumps(logs)
    return StreamingResponse(io.BytesIO(pdf_data), media_type='application/pdf', headers=headers)