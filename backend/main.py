from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from services.gemini.geminiService import ask_gemini
from services.canvas.canvasService import access_canvas


app = FastAPI()


# allow frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "CanvasAI backend is running"
    }


"""
Endpoints for prompting Gemini AI through geminiService
"""

class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    response = ask_gemini(request.message)

    return {
        "response": response
    }


"""
Endpoints for accessing Canvas API through canvasService
"""

class CanvasRequest(BaseModel):
    endpoint: str = ""
    cookies: dict[str, str] | None = None


class CanvasResponse(BaseModel):
    response: Any


@app.post("/canvas", response_model=CanvasResponse)
def canvas(request: CanvasRequest):
    endpoint = request.endpoint or ""
    response = access_canvas(endpoint, request.cookies)

    return {
        "response": response
    }