from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from resumeta_api.database import init_db
from resumeta_api.educations.router import router as EducationRouter
from resumeta_api.employments.router import router as EmploymentRouter
from resumeta_api.resumes.router import router as ResumeRouter


@asynccontextmanager
async def start_db(app: FastAPI):
    """Initialize the database connection."""
    await init_db()
    yield


app = FastAPI(lifespan=start_db)

origins = [
    "http://localhost",
    "http://localhost:8081",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(ResumeRouter, tags=["Resumes"], prefix="/resumes")
app.include_router(EmploymentRouter, tags=["Employments"], prefix="/employments")
app.include_router(EducationRouter, tags=["Educations"], prefix="/educations")


@app.get("/", tags=["Root"])
async def read_root() -> dict:
    """Welcome message."""
    return {"message": "Welcome to your beanie powered app!"}


if __name__ == "__main__":
    import uvicorn
    from dotenv import load_dotenv
    import os

    load_dotenv()  # take environment variables from .env.

    API_HOST = os.environ.get("API_HOST")
    API_PORT = os.environ.get("API_PORT")

    uvicorn.run("main:app", host=API_HOST, port=int(API_PORT), reload=True)
