"""Education routes."""

from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status
from loguru import logger

from resumeta_api.educations.models import (
    EducationDocument,
    UpdateEducation,
)

from resumeta_api.config import encode_input

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
    education_data = encode_input(education_data)
    _ = await education.update({"$set": education_data})
    updated_education = await get_education(education_id)
    return updated_education


@router.delete("/{education_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_education(education_id: PydanticObjectId):
    """Delete an education by id."""
    education = await get_education(education_id)
    await education.delete()
    return status.HTTP_204_NO_CONTENT
