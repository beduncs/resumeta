# Define the global models

from pydantic import BaseModel
from typing import Optional


class Location(BaseModel):
    """Location class defining the Location table."""

    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None


class User(BaseModel):
    """User class defining the user table."""

    first_name: str
    last_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    # links
