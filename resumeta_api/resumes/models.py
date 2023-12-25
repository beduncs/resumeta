from typing import List, Optional

from beanie import Document, Link
from pydantic import BaseModel

from resumeta_api.config import date_encoder
from resumeta_api.educations.models import EducationDocument
from resumeta_api.employments.models import EmploymentDocument
from resumeta_api.models import User


class Resume(BaseModel):
    """Resume class defining the Resume table."""

    name: str
    user: User
    employment: Optional[List[Link[EmploymentDocument]]] = []
    education: Optional[List[Link[EducationDocument]]] = []

    class Settings:
        """Pydantic configuration."""

        bson_encoders = date_encoder


class ResumeDocument(Resume, Document):
    """Resume class defining the Resume Document."""

    pass


class UpdateResume(BaseModel):
    """Resume class defining the Resume table."""

    name: Optional[str] = None
    user: Optional[User] = None
