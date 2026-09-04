from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from google.genai import errors
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
    base_url: str | None = None
    cookies: dict[str, str] | None = None


class ChatResponse(BaseModel):
    response: str


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        # prompt Gemini, pass in message, base URL, and Canvas session cookies
        response = ask_gemini(
            request.message, 
            request.base_url, 
            request.cookies
        )

    except errors.ServerError:
        return {
            "response": "Gemini is busy right now. Please try again in a moment."
        }

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
    
    # call Canvas API, pass in desired  endpoint and Canvas session cookies 
    response = access_canvas(
        request.endpoint or "",
        request.cookies
    )

    return {
        "response": response
    }