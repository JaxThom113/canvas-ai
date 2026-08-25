from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from services.gemini.geminiService import ask_gemini


app = FastAPI()


# allow frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@app.get("/")
def root():
    return {
        "message": "CanvasAI backend is running"
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    response = ask_gemini(request.message)

    return {
        "response": response
    }