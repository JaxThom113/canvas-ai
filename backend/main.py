from datetime import datetime
from typing import Any

import mariadb
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from openai import APIStatusError
from pydantic import BaseModel

from services.navigator.navigatorService import ask_navigator
from services.canvas.canvasService import access_canvas
from app.auth import UsernameTakenError, create_account, create_token, verify_login, verify_token
from app.db import insert_login, insert_session, insert_chat
from db.chatStorage import create_session, get_sessions, save_chat, session_belongs_to


app = FastAPI()


# allow frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(mariadb.Error)
def mariadb_error_handler(request, exc: mariadb.Error):
    return JSONResponse(status_code=500, content={"detail": f"Database error: {exc}"})


@app.get("/")
def root():
    return {
        "message": "CanvasAI backend is running"
    }


"""
Endpoints for logging in / creating accounts
"""

class AuthRequest(BaseModel):
    username: str
    password: str


class AuthResponse(BaseModel):
    account_id: int
    username: str
    token: str


USERNAME_MAX_LENGTH = 50 # max username length
PASSWORD_MIN_LENGTH = 8 # minimum password length
PASSWORD_MAX_BYTES = 72 # encode() only allows passwords up to 72 bytes long


@app.post("/auth/signup", response_model=AuthResponse)
def signup(request: AuthRequest):
    username = request.username.strip()

    if not username:
        raise HTTPException(status_code=400, detail="Username is required.")
    if len(username) > USERNAME_MAX_LENGTH:
        raise HTTPException(status_code=400, detail=f"Username must be at most {USERNAME_MAX_LENGTH} characters.")
    if len(request.password) < PASSWORD_MIN_LENGTH:
        raise HTTPException(status_code=400, detail=f"Password must be at least {PASSWORD_MIN_LENGTH} characters.")
    if len(request.password.encode("utf-8")) > PASSWORD_MAX_BYTES:
        raise HTTPException(status_code=400, detail="Password is too long.")

    try:
        account_id = create_account(username, request.password)
    except UsernameTakenError:
        raise HTTPException(status_code=409, detail="That username is already taken.")

    return {
        "account_id": account_id,
        "username": username,
        "token": create_token(account_id)
    }


@app.post("/auth/login", response_model=AuthResponse)
def login(request: AuthRequest):
    result = None
    if len(request.password.encode("utf-8")) <= PASSWORD_MAX_BYTES:
        result = verify_login(request.username.strip(), request.password)

    if result is None:
        raise HTTPException(status_code=401, detail="Incorrect username or password.")

    account_id, username = result
    return {
        "account_id": account_id,
        "username": username,
        "token": create_token(account_id)
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
def chat(request: ChatRequest, authorization: str | None = Header(default=None)):
    # logged in users send "Authorization: Bearer <token>". Chats are only
    # saved when logged in; guests can still chat but nothing is stored
    account_id = None
    if authorization:
        account_id = verify_token(authorization.removeprefix("Bearer ").strip())
        if account_id is None:
            raise HTTPException(status_code=401, detail="Your login has expired. Please log in again.")

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

    if account_id is None:
        return {
            "response": response
        }

    # the first message sent after opening the extension creates the session,
    # later messages are added to it
    session_id = request.session_id
    try:
        if session_id is not None and not session_belongs_to(session_id, account_id):
            session_id = None
        if session_id is None:
            session_id = create_session(account_id=account_id, title=request.message[:255])
        save_chat(session_id, request.message, response)
    except Exception as e:
        print(f"Error saving chat: {e}")

    return {
        "response": response,
        "session_id": session_id
    }


"""
Endpoints for viewing the logged in user's chat history
"""

class HistoryChat(BaseModel):
    chat_id: int
    message: str
    response: str
    created_at: datetime | None = None


class HistorySession(BaseModel):
    session_id: int
    session_title: str
    created_at: datetime | None = None
    chats: list[HistoryChat]


@app.get("/sessions", response_model=list[HistorySession])
def sessions(authorization: str | None = Header(default=None)):
    # returns the user's sessions/chats, most recent first
    account_id = None
    if authorization:
        account_id = verify_token(authorization.removeprefix("Bearer ").strip())

    if account_id is None:
        raise HTTPException(status_code=401, detail="Your login has expired. Please log in again.")

    return get_sessions(account_id)


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