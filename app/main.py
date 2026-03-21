from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from app.core.rate_limiter import is_allowed
from app.service import generate_response
from app.types import PromptRequest
from app.utils import read_html_file

app = FastAPI()


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
