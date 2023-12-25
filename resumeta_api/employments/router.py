"""Employment routes."""

from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status
from loguru import logger
from resumeta_api.employments.models import (
    EmploymentDocument,
    UpdateEmployment,
)

from resumeta_api.config import encode_input

logger.add("resumeta.log", format="{time} {level} {message}", level="INFO")
router = APIRouter()


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=EmploymentDocument
)
async def create_employment(employment: EmploymentDocument):
    """Create a new employment."""
    await employment.insert()
    return employment


@router.get("/", response_model=List[EmploymentDocument])
async def get_employments():
    """Get all employments."""
    employments = await EmploymentDocument.find_all(fetch_links=True).to_list()
    return employments


@router.get("/{employment_id}", response_model=EmploymentDocument)
async def get_employment(employment_id: PydanticObjectId):
    """Get an employment by id."""
    employment = await EmploymentDocument.get(employment_id, fetch_links=True)
    if not employment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employment with id {employment_id} not found",
        )

    return employment


@router.put("/{employment_id}", response_model=EmploymentDocument)
async def update_employment(
    employment_id: PydanticObjectId, employment_data: UpdateEmployment
):
    """Update an employment by id."""
    employment = await get_employment(employment_id)
    employment_data = encode_input(employment_data)
    _ = await employment.update({"$set": employment_data})
    updated_employment = await get_employment(employment_id)
    return updated_employment


@router.delete("/{employment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employment(employment_id: PydanticObjectId):
    """Delete an employment by id."""
    employment = await get_employment(employment_id)
    await employment.delete()
    return {"message": "Employment deleted"}
