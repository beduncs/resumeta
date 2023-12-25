from pydantic import BaseModel
from typing import Optional, List
import datetime
from beanie import Document

from resumeta_api.models import Location
from resumeta_api.config import date_encoder


class Employment(BaseModel):
    """Employment class defining the employment table."""

    title: str
    location: Location
    start_date: Optional[datetime.date] = None
    end_date: Optional[datetime.date] = None
    activities: Optional[List[str]] = []

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
    activities: Optional[List[str]] = []
