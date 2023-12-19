"""Schema definition for the backend database."""

import datetime
from typing import List, Optional

from beanie import Document, Link
from pydantic import BaseModel

from server.utils.pydantic_encoder import date_encoder


class User(BaseModel):
    """User class defining the user table."""

    first_name: str
    last_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    # links


class Location(BaseModel):
    """Location class defining the Location table."""

    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None


# Activity Schemas


class Activity(BaseModel):
    """Activity class defining the Activity table."""

    description: str


class ActivityDocument(Activity, Document):
    """Activity class defining the Activity table."""

    pass


class UpdateActivity(BaseModel):
    """Activity class defining the Activity table."""

    description: Optional[str] = None


# Education Schemas


class Education(BaseModel):
    """Education class defining the education table."""

    degree: str
    major: str
    institution: Location
    start_date: Optional[datetime.date] = None
    end_date: Optional[datetime.date] = None
    minor: Optional[str] = None
    gpa: Optional[float] = None
    activities: Optional[List[Link[ActivityDocument]]] = []

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


# Employment Schemas


class Employment(BaseModel):
    """Employment class defining the employment table."""

    title: str
    location: Location
    start_date: Optional[datetime.date] = None
    end_date: Optional[datetime.date] = None
    activities: Optional[List[Link[ActivityDocument]]] = []

    class Settings:
        """Pydantic configuration."""

        bson_encoders = date_encoder


class EmploymentDocument(Employment, Document):
    """Employment class defining the employment table."""

    pass


class UpdateEmployment(BaseModel):
    """Resume class defining the Resume table."""

    title: Optional[str] = None
    location: Optional[Location] = None
    start_date: Optional[datetime.date] = None
    end_date: Optional[datetime.date] = None


# Resume Schemas


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
