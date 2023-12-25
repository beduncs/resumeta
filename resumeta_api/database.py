"""This module contains the database connection tools."""

import os

from beanie import init_beanie
from dotenv import load_dotenv
from motor import motor_asyncio

from resumeta_api.resumes.models import ResumeDocument
from resumeta_api.educations.models import EducationDocument
from resumeta_api.employments.models import EmploymentDocument

load_dotenv()  # take environment variables from .env.

DATABASE_URL = os.environ.get("DATABASE_URL")


async def init_db():
    """Initialize the database connection."""
    client = motor_asyncio.AsyncIOMotorClient(DATABASE_URL)

    await init_beanie(
        database=client.db_name,
        document_models=[ResumeDocument, EmploymentDocument, EducationDocument],
    )
