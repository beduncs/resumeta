import datetime
from typing import List, Optional

from beanie import Document
from pydantic import BaseModel

from resumeta_api.config import date_encoder
from resumeta_api.models import Location


class Education(BaseModel):
    """Education class defining the education table."""

    degree: str
    major: str
    institution: Location
    start_date: Optional[datetime.date] = None
    end_date: Optional[datetime.date] = None
    minor: Optional[str] = None
    gpa: Optional[float] = None
    activities: Optional[List[str]] = []

    class Settings:
        """Pydantic configuration."""

        bson_encoders = date_encoder


class EducationDocument(Education, Document):
    """Resume class defining the Resume Document."""

    pass


class UpdateEducation(BaseModel):
    """Resume class defining the Resume table."""

    name: Optional[str] = None
    degree: Optional[str] = None
    major: Optional[str] = None
    institution: Optional[Location] = None
    start_date: Optional[datetime.date] = None
    end_date: Optional[datetime.date] = None
    minor: Optional[str] = None
    gpa: Optional[float] = None
    activities: Optional[List[str]] = []
