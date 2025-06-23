from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pydantic_settings import BaseSettings
import os
from typing import List
from .health import get_health_status


# Settings class to handle environment variables
class Settings(BaseSettings):
    app_name: str = "Mercedes-Benz Quiz API"
    app_version: str = "1.0.0"
    debug: bool = False
    secret_key: str
    allowed_hosts: str
    cors_origins: str
    database_url: str
    star_wars_api_url: str

    class Config:
        env_file = ".env"


# Initialize settings
settings = Settings()

# Create FastAPI app
app = FastAPI(
    title=settings.app_name, version=settings.app_version, debug=settings.debug
)

# Configure CORS
origins = settings.cors_origins.split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models
class QuizQuestion(BaseModel):
    id: int
    question: str
    options: List[str]
    correct_answer: int
    category: str


class QuizResponse(BaseModel):
    question_id: int
    selected_answer: int


# Sample data
sample_questions = [
    {
        "id": 1,
        "question": "What year was Mercedes-Benz founded?",
        "options": ["1886", "1900", "1926", "1950"],
        "correct_answer": 0,
        "category": "History",
    },
    {
        "id": 2,
        "question": "Which Mercedes-Benz model is known as the 'Silver Arrow'?",
        "options": ["300SL", "190E", "W196", "CLK-GTR"],
        "correct_answer": 2,
        "category": "Racing",
    },
]


@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "status": "running",
    }


@app.get("/health")
async def health_check(response: Response):
    """Get health status for all services"""
    health_status = await get_health_status(
        settings.app_name, settings.app_version, settings.star_wars_api_url
    )

    # Set HTTP status code based on health
    if health_status["status"] != "healthy":
        response.status_code = 400

    return health_status


@app.get("/questions", response_model=List[QuizQuestion])
async def get_questions():
    """Get all quiz questions"""
    return sample_questions


@app.get("/questions/{question_id}", response_model=QuizQuestion)
async def get_question(question_id: int):
    """Get a specific question by ID"""
    for question in sample_questions:
        if question["id"] == question_id:
            return question
    raise HTTPException(status_code=404, detail="Question not found")


@app.post("/submit-answer")
async def submit_answer(response: QuizResponse):
    """Submit an answer for a question"""
    # Find the question
    question = None
    for q in sample_questions:
        if q["id"] == response.question_id:
            question = q
            break

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Check if answer is correct
    is_correct = response.selected_answer == question["correct_answer"]

    return {
        "question_id": response.question_id,
        "selected_answer": response.selected_answer,
        "correct_answer": question["correct_answer"],
        "is_correct": is_correct,
        "message": "Correct!" if is_correct else "Incorrect. Try again!",
    }


@app.get("/categories")
async def get_categories():
    """Get all available question categories"""
    categories = list(set(q["category"] for q in sample_questions))
    return {"categories": categories}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
