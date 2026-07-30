"""
Student endpoints for the High School Management System API
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List

from ..database import students_collection, activities_collection

router = APIRouter(
    prefix="/students",
    tags=["students"]
)


@router.get("/{email}", response_model=Dict[str, Any])
def get_student_profile(email: str) -> Dict[str, Any]:
    """Get a student's profile by email address"""
    student = students_collection.find_one({"_id": email})

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Find all activities the student is enrolled in
    enrolled_activities: List[str] = []
    for activity in activities_collection.find({"participants": email}):
        enrolled_activities.append(activity["_id"])

    return {
        "email": student["_id"],
        "name": student["name"],
        "grade": student["grade"],
        "branch": student["branch"],
        "enrolled_activities": enrolled_activities
    }
