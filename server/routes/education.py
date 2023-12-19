"""Education routes."""

from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status
from loguru import logger

from models.resume import (
    ActivityDocument,
    EducationDocument,
    UpdateEducation,
)
from utils import pydantic_encoder

logger.add("resumeta.log", format="{time} {level} {message}", level="INFO")
router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=EducationDocument)
async def create_education(education: EducationDocument):
    """Create a new education."""
    await education.insert()
    return education


@router.get("/", response_model=List[EducationDocument])
async def get_educations():
    """Get all educations."""
    educations = await EducationDocument.find_all(fetch_links=True).to_list()
    return educations


@router.get("/{education_id}", response_model=EducationDocument)
async def get_education(education_id: PydanticObjectId):
    """Get an education by id."""
    education = await EducationDocument.get(education_id, fetch_links=True)
    if not education:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Education with id {education_id} not found",
        )

    return education


@router.put("/{education_id}", response_model=EducationDocument)
async def update_education(
    education_id: PydanticObjectId, education_data: UpdateEducation
):
    """Update an education by id."""
    education = await get_education(education_id)
    education_data = pydantic_encoder.encode_input(education_data)
    _ = await education.update({"$set": education_data})
    updated_education = await get_education(education_id)
    return updated_education


@router.post(
    "/{education_id}/activities/{activity_id}",
    response_model=EducationDocument,
)
async def add_activity(education_id: PydanticObjectId, activity_id: PydanticObjectId):
    """Add an activity to an education."""
    education = await get_education(education_id)
    activity = await ActivityDocument.get(activity_id)
    if activity not in education.activities:
        education.activities.append(activity)
    await education.save()
    return education


@router.delete(
    "/{education_id}/activities/{activity_id}",
    response_model=EducationDocument,
)
async def remove_activity(
    education_id: PydanticObjectId, activity_id: PydanticObjectId
):
    """Remove an activity from an education."""
    education = await get_education(education_id)
    activity = await ActivityDocument.get(activity_id)
    if activity in education.activities:
        education.activities.remove(activity)
    await education.save()
    return education


@router.delete("/{education_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_education(education_id: PydanticObjectId):
    """Delete an education by id."""
    education = await get_education(education_id)
    await education.delete()
    return status.HTTP_204_NO_CONTENT
