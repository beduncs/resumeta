"""Resume routes."""

from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status
from loguru import logger

from resumeta.models.resume import (
    EducationDocument,
    EmploymentDocument,
    ResumeDocument,
    UpdateResume,
)
from resumeta.utils import pydantic_encoder

logger.add("resumeta.log", format="{time} {level} {message}", level="INFO")
router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResumeDocument)
async def create_resume(resume: ResumeDocument):
    """Create a new resume."""
    await resume.insert()
    return resume


@router.get("/", response_model=List[ResumeDocument])
async def get_resumes():
    """Get all resumes."""
    books = await ResumeDocument.find_all(fetch_links=True).to_list()
    return books


@router.get("/{resume_id}", response_model=ResumeDocument)
async def get_resume(resume_id: PydanticObjectId):
    """Get a resume by id."""
    book = await ResumeDocument.get(resume_id, fetch_links=True)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resume with id {resume_id} not found",
        )

    return book


@router.put("/{resume_id}", response_model=ResumeDocument)
async def update_resume(resume_id: PydanticObjectId, resume_data: UpdateResume):
    """Update a resume by id."""
    resume = await get_resume(resume_id)
    resume_data = pydantic_encoder.encode_input(resume_data)
    _ = await resume.update({"$set": resume_data})
    updated_resume = await get_resume(resume_id)
    return updated_resume


@router.post("/{resume_id}/employment/{employment_id}", response_model=ResumeDocument)
async def add_employment(resume_id: PydanticObjectId, employment_id: PydanticObjectId):
    """Add employment to a resume."""
    resume = await ResumeDocument.get(resume_id)
    employment = await EmploymentDocument.get(employment_id)
    if employment not in resume.employment:
        resume.employment.append(employment)
    await resume.save()
    return resume


@router.delete("/{resume_id}/resume/{employment_id}", response_model=ResumeDocument)
async def remove_employment(
    resume_id: PydanticObjectId, employment_id: PydanticObjectId
):
    """Delete a employment from a resume by id."""
    resume = await get_resume(resume_id)
    employment = await EmploymentDocument.get(employment_id)
    if employment in resume.employment:
        resume.employment.remove(employment)
    await resume.save()
    return resume


@router.post("/{resume_id}/education/{education_id}", response_model=ResumeDocument)
async def add_education(resume_id: PydanticObjectId, education_id: PydanticObjectId):
    """Add education to a resume."""
    resume = await ResumeDocument.get(resume_id)
    education = await EducationDocument.get(education_id)
    if education not in resume.education:
        resume.education.append(education)
    await resume.save()
    return resume


@router.delete("/{resume_id}/education/{education_id}", response_model=ResumeDocument)
async def remove_education(resume_id: PydanticObjectId, education_id: PydanticObjectId):
    """Delete a education from a resume by id."""
    resume = await get_resume(resume_id)
    education = await EducationDocument.get(education_id)
    if education in resume.education:
        resume.education.remove(education)
    await resume.save()
    return resume


@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(resume_id: PydanticObjectId):
    """Delete a resume by id."""
    resume = await get_resume(resume_id)
    await resume.delete()
    return {"message": "Resume deleted successfully"}
