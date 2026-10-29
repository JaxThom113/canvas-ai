from typing import Any

import mariadb
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google.genai import errors
from pydantic import BaseModel

from services.gemini.geminiService import ask_gemini
from services.canvas.canvasService import access_canvas
from app.db import insert_login, insert_session, insert_chat


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


"""
Endpoints for seeding test data directly into login/session/chat
"""

class LoginSeedRequest(BaseModel):
    account_id: int


@app.post("/db/login")
def seed_login(request: LoginSeedRequest):
    try:
        insert_login(request.account_id)
    except mariadb.IntegrityError:
        raise HTTPException(status_code=400, detail="account_id already exists")

    return {"success": True}


class SessionSeedRequest(BaseModel):
    account_id: int
    session_title: str
    session_id: int | None = None


@app.post("/db/session")
def seed_session(request: SessionSeedRequest):
    try:
        new_id = insert_session(request.account_id, request.session_title, request.session_id)
    except mariadb.IntegrityError as e:
        if e.errno == 1452:
            raise HTTPException(status_code=400, detail="account_id does not exist")
        raise HTTPException(status_code=400, detail="session_id already exists")

    return {"success": True, "session_id": new_id}


class ChatSeedRequest(BaseModel):
    session_id: int
    message: Any
    response: Any | None = None
    chat_id: int | None = None


@app.post("/db/chat")
def seed_chat(request: ChatSeedRequest):
    try:
        new_id = insert_chat(request.session_id, request.message, request.response, request.chat_id)
    except mariadb.IntegrityError as e:
        if e.errno == 1452:
            raise HTTPException(status_code=400, detail="session_id does not exist")
        raise HTTPException(status_code=400, detail="chat_id already exists")

    return {"success": True, "chat_id": new_id}