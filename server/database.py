"""This module contains the database connection tools."""

import os

from dotenv import load_dotenv
from beanie import init_beanie
from motor import motor_asyncio
from server.models.resume import (
    ResumeDocument,
    EmploymentDocument,
    EducationDocument,
    ActivityDocument,
)

load_dotenv()  # take environment variables from .env.

DATABASE_URL = os.environ.get("DATABASE_URL")


async def init_db():
    """Initialize the database connection."""
    client = motor_asyncio.AsyncIOMotorClient(DATABASE_URL)

    # client = motor.motor_asyncio.AsyncIOMotorClient(
    #    "mongodb+srv://<username>:<password>@cluster0.zlhkso0.mongodb.net/?retryWrites=true&w=majority"
    # )

    await init_beanie(
        database=client.db_name,
        document_models=[
            ResumeDocument,
            EmploymentDocument,
            EducationDocument,
            ActivityDocument,
        ],
    )
