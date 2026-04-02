import logging
import os
import shutil
import uuid

from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse

from app.core.rate_limiter import is_allowed
from app.core.redis_client import get_redis
from app.exceptions import SkillsParsingError
from app.observability.context import request_id_var
from app.observability.log import log_event
from app.services.extraction_service import extract_skills
from app.services.llm_service import generate_response
from app.services.resume_service import extract_text_from_pdf
from app.types import PromptRequest
from app.utils.file_parser import read_html_file
from app.utils.text_cleaner import clean_text

logging.basicConfig(level=logging.INFO, format="%(message)s")

app = FastAPI(title="AI Interview Simulator")


@app.get("/health")
async def health():
    payload = {"status": "ok", "redis": "disabled"}
    r = get_redis()
    if r:
        try:
            r.ping()
            payload["redis"] = "ok"
        except Exception as exc:
            payload["status"] = "degraded"
            payload["redis"] = "error"
            payload["redis_error"] = type(exc).__name__
    return payload


@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    token = request_id_var.set(str(uuid.uuid4()))
    try:
        response = await call_next(request)
        log_event(
            "http_request",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
        )
        return response
    finally:
        request_id_var.reset(token)


@app.get("/", response_class=HTMLResponse)
async def welcome():
    welcome_html = await read_html_file("./app/html/welcome.html")
    return welcome_html


@app.post("/ask")
async def ask(request: PromptRequest):
    system_prompt = "You are a technical interviewer. You should also be answering a few questions you are asked about."
    user_prompt = request.prompt
    try:
        user_id = "default_user"  # for now (we'll improve later)

        if not is_allowed(user_id):
            raise HTTPException(status_code=429, detail="Rate limit exceeded")

        response, latency = generate_response(request, system_prompt, user_prompt)

        return {
            "success": True,
            "provider": request.provider,
            "response": response,
            "latency": f"{latency:.2f}",
        }
    except Exception as e:
        print("Exception", e)
        return {
            "success": False,
            "error_type": type(e).__name__,
            "error_message": f"{e}",
        }
    finally:
        print("\nLLM Call Complete", end="\n\n")


@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    file_path = f"temp_{file.filename}"

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        text = extract_text_from_pdf(file_path)
        cleaned_text = clean_text(text)

        try:
            return extract_skills(resume_text=cleaned_text)
        except SkillsParsingError as exc:
            raise HTTPException(
                status_code=422,
                detail="Extraction failed: model output was not valid structured skills.",
            ) from exc
    finally:
        if os.path.isfile(file_path):
            os.remove(file_path)
