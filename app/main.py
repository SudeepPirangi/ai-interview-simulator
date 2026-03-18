import time

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.core.retry import call_with_retry
from app.llm.gemini_provider import GeminiProvider
from app.llm.openai_provider import OpenAIProvider
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
        if request.provider == "openai":
            provider = OpenAIProvider()
        else:
            provider = GeminiProvider()

        start = time.time()

        response = call_with_retry(
            lambda: provider.generate(system_prompt, user_prompt)
        )

        end = time.time()
        latency = end - start
        print(f"[Latency] {latency:.2f} seconds")

        return {
            "success": True,
            "provider": request.provider,
            "response": response,
            "latency": f"{latency:.2f} seconds",
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
