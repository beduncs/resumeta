from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import init_db
from .routes.activity import router as ActivityRouter
from .routes.education import router as EducationRouter
from .routes.employment import router as EmploymentRouter
from .routes.resume import router as ResumeRouter


@asynccontextmanager
async def start_db(app: FastAPI):
    """Initialize the database connection."""
    await init_db()
    yield


app = FastAPI(lifespan=start_db)


app.include_router(ResumeRouter, tags=["Resumes"], prefix="/resumes")
app.include_router(EmploymentRouter, tags=["Employments"], prefix="/employment")
app.include_router(EducationRouter, tags=["Education"], prefix="/education")
app.include_router(ActivityRouter, tags=["Activities"], prefix="/activity")


@app.get("/", tags=["Root"])
async def read_root() -> dict:
    """Welcome message."""
    return {"message": "Welcome to your beanie powered app!"}
