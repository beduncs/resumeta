from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.database import init_db
from server.routes.activity import router as ActivityRouter
from server.routes.education import router as EducationRouter
from server.routes.employment import router as EmploymentRouter
from server.routes.resume import router as ResumeRouter


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
app.include_router(EmploymentRouter, tags=["Employments"], prefix="/employment")
app.include_router(EducationRouter, tags=["Education"], prefix="/education")
app.include_router(ActivityRouter, tags=["Activities"], prefix="/activity")


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
