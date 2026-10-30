from typing import Any

import mariadb
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from openai import APIStatusError
from pydantic import BaseModel

from services.navigator.navigatorService import ask_navigator
from services.canvas.canvasService import access_canvas
from app.db import insert_login, insert_session, insert_chat

from db.chatStorage import create_session, save_chat


app = FastAPI()


# allow frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Unhandled DB errors (bad credentials, unreachable host, ...) would otherwise
# become a bare 500 without CORS headers, which the browser reports as
# "Failed to fetch". Return JSON so the real message shows up in the UI.
@app.exception_handler(mariadb.Error)
def mariadb_error_handler(request, exc: mariadb.Error):
    return JSONResponse(status_code=500, content={"detail": f"Database error: {exc}"})


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
    session_id: int | None = None


class ChatResponse(BaseModel):
    response: str
    session_id: int | None = None


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

    session_id = request.session_id
    try:
        if session_id is None:
            session_id = create_session(account_id=1, title=request.message[:255])
        save_chat(session_id, request.message, response)
    except Exception as e:
        print(f"Error saving chat: {e}")

    return {
        "response": response,
        "session_id": session_id
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