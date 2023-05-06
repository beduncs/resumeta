"""Schema definition for the backend database."""

import datetime

from typing import List, Optional

from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column


class Base(DeclarativeBase):
    """This class contains the Base class for the schema definition."""

    pass


class Employment(Base):
    """Employment class defining the Employment table."""

    __tablename__ = "employment"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    startdate: Mapped[datetime.date]
    enddate: Mapped[Optional[datetime.date]]
    institution_id: Mapped[int] = mapped_column(ForeignKey("institution.id"))
    activities: Mapped[List["Activity"]] = relationship()

    def __repr__(self) -> str:
        """Return formatted string.

        Returns:
            str: String formatted table return
        """
        return f'''
        Employment(id={self.id!r},
        title={self.title!r},
        startdate={self.startdate!r}),
        enddate={self.enddate!r})
        '''


class Activity(Base):
    """Activity class defining the Activity table."""

    __tablename__ = "activity"
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(500))
    employment_id: Mapped[int] = mapped_column(ForeignKey("employment.id"))

    def __repr__(self) -> str:
        """Return formatted string.

        Returns:
            str: String formatted table return
        """
        return f'''
        Activity(id={self.id!r},
        description={self.description!r}
        '''


class Location(Base):
    """Location class defining the Location table."""

    __tablename__ = "location"
    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[Optional[str]] = mapped_column(String(200))
    city: Mapped[Optional[str]] = mapped_column(String(100))
    state: Mapped[Optional[str]] = mapped_column(String(100))

    def __repr__(self) -> str:
        """Return formatted string.

        Returns:
            str: String formatted table return
        """
        return f'''
        Location(id={self.id!r},
        address={self.address!r},
        city={self.city!r},
        state={self.state!r}
        '''


class Institution(Base):
    """Institution class defining the Institution table."""

    __tablename__ = "institution"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    location: Mapped[Optional[int]] = mapped_column(ForeignKey("location.id"))

    def __repr__(self) -> str:
        """Return formatted string.

        Returns:
            str: String formatted table return
        """
        return f'''
        Institution(id={self.id!r},
        name={self.name!r}
        '''


class Education(Base):
    """Education class defining the Education table."""

    __tablename__ = "education"
    id: Mapped[int] = mapped_column(primary_key=True)
    degree: Mapped[str]
    gpa: Mapped[float]
    startdate: Mapped[datetime.date]
    enddate: Mapped[Optional[datetime.date]]
    institution_id: Mapped[int] = mapped_column(ForeignKey("institution.id"))

    def __repr__(self) -> str:
        """Return formatted string.

        Returns:
            str: String formatted table return
        """
        return f'''
        Education(id={self.id!r},
        degree={self.degree!r},
        gpa={self.gpa!r},
        startdate={self.startdate!r},
        enddate={self.enddate!r}
        '''


class User(Base):
    """User class defining the User table."""

    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    email_address: Mapped[Optional[str]]
    phone_number: Mapped[Optional[str]]
    location_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("location.id"))

    def __repr__(self) -> str:
        """Return formatted string.

        Returns:
            str: String formatted table return
        """
        return f'''
        User(id={self.id!r},
        name={self.name!r},
        email_address={self.email_address!r},
        phone_number={self.phone_number!r}
        '''


class Resume(Base):
    """Resume class defining the Resume table."""

    __tablename__ = "resume"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))


resume_employment = Table(
    "resume_employment",
    Base.metadata,
    Column("resume_id", ForeignKey("resume.id")),
    Column("employment_id", ForeignKey("employment.id"))
)

resume_education = Table(
    "resume_education",
    Base.metadata,
    Column("resume_id", ForeignKey("resume.id")),
    Column("education_id", ForeignKey("education.id"))
)
