from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import APIStatusError
from pydantic import BaseModel

from services.navigator.navigatorService import ask_navigator
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
Endpoints for prompting NaviGator AI through navigatorService
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
        # prompt NaviGator and the desired model 
        # pass in message, base URL, and Canvas session cookies
        response = ask_navigator(
            request.message, 
            request.base_url, 
            request.cookies
        )

    except APIStatusError:
        return {
            "response": "NaviGator is busy right now. Please try again in a moment."
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