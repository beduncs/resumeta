"""Activity routes."""

from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status
from loguru import logger

from resumeta.models.resume import ActivityDocument, UpdateActivity
from resumeta.utils import pydantic_encoder

logger.add("resumeta.log", format="{time} {level} {message}", level="INFO")
router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ActivityDocument)
async def create_activity(activity: ActivityDocument):
    """Create a new education."""
    await activity.insert()
    return activity


@router.get("/", response_model=List[ActivityDocument])
async def get_activities():
    """Get all activities."""
    activities = await ActivityDocument.find_all().to_list()
    return activities


@router.get("/{activity_id}", response_model=ActivityDocument)
async def get_activity(activity_id: PydanticObjectId):
    """Get an activity by id."""
    activity = await ActivityDocument.get(activity_id)
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Activity with id {activity_id} not found",
        )

    return activity


@router.put("/{activity_id}", response_model=ActivityDocument)
async def update_activity(activity_id: PydanticObjectId, activity_data: UpdateActivity):
    """Update an activity by id."""
    activity = await get_activity(activity_id)
    activity_data = pydantic_encoder.encode_input(activity_data)
    _ = await activity.update({"$set": activity_data})
    updated_activity = await get_activity(activity_id)
    return updated_activity


@router.delete("/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_activity(activity_id: PydanticObjectId):
    """Delete an activity by id."""
    activity = await get_activity(activity_id)
    await activity.delete()
    return {"message": f"Activity with id {activity_id} deleted successfully"}
