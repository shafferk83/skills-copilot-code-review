"""
Endpoints for the High School Management System API
"""

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import RedirectResponse
from typing import Dict, Any, Optional, List

from ..database import activities_collection, teachers_collection

router = APIRouter(
    prefix="/activities",
    tags=["activities"]
)


@router.get("", response_model=Dict[str, Any])
@router.get("/", response_model=Dict[str, Any])
def get_activities(
    day: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get all activities with their details, with optional filtering by day and time

    - day: Filter activities occurring on this day (e.g., 'Monday', 'Tuesday')
    - start_time: Filter activities starting at or after this time (24-hour format, e.g., '14:30')
    - end_time: Filter activities ending at or before this time (24-hour format, e.g., '17:00')
    """
    # Build the query based on provided filters
    query = {}

    if day:
        query["schedule_details.days"] = {"$in": [day]}

    if start_time:
        query["schedule_details.start_time"] = {"$gte": start_time}

    if end_time:
        query["schedule_details.end_time"] = {"$lte": end_time}

    # Query the database
    activities = {}
    for activity in activities_collection.find(query):
        name = activity.pop('_id')
        activities[name] = activity

    return activities


@router.get("/days", response_model=List[str])
def get_available_days() -> List[str]:
    """Get a list of all days that have activities scheduled"""
    # Aggregate to get unique days across all activities
    pipeline = [
        {"$unwind": "$schedule_details.days"},
        {"$group": {"_id": "$schedule_details.days"}},
        {"$sort": {"_id": 1}}  # Sort days alphabetically
    ]

    days = []
    for day_doc in activities_collection.aggregate(pipeline):
        days.append(day_doc["_id"])

    return days


@router.get("/timetable", response_model=Dict[str, Any])
def get_timetable(branch: Optional[str] = None) -> Dict[str, Any]:
    """
    Get activities organized by day for timetable view.

    - branch: Filter activities by branch/department (sports, arts, academic, technology, community)

    Returns a dict with each day of the week mapped to a list of activities scheduled on that day,
    sorted by start time.
    """
    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    timetable: Dict[str, List[Any]] = {day: [] for day in days_order}

    # Branch-to-keyword mapping for server-side filtering
    branch_keywords: Dict[str, Dict[str, List[str]]] = {
        "sports": {
            "name": ["soccer", "basketball", "sport", "fitness"],
            "desc": ["team", "game", "athletic"]
        },
        "arts": {
            "name": ["art", "music", "theater", "drama"],
            "desc": ["creative", "paint"]
        },
        "academic": {
            "name": ["science", "math", "academic", "study", "olympiad", "debate", "chess"],
            "desc": ["learning", "education", "competition"]
        },
        "technology": {
            "name": ["computer", "coding", "tech", "robotics", "programming"],
            "desc": ["programming", "technology", "digital", "robot"]
        },
        "community": {
            "name": ["volunteer", "community"],
            "desc": ["service", "volunteer"]
        }
    }

    for activity in activities_collection.find({}):
        name = activity.pop('_id')
        activity_name_lower = name.lower()
        activity_desc_lower = activity.get("description", "").lower()

        # Apply branch filter when provided
        if branch and branch in branch_keywords:
            keywords = branch_keywords[branch]
            name_match = any(kw in activity_name_lower for kw in keywords["name"])
            desc_match = any(kw in activity_desc_lower for kw in keywords["desc"])
            if not name_match and not desc_match:
                continue

        schedule_days = activity.get("schedule_details", {}).get("days", [])
        for day in schedule_days:
            if day in timetable:
                timetable[day].append({"name": name, **activity})

    # Sort activities within each day by start time
    for day in timetable:
        timetable[day].sort(
            key=lambda x: x.get("schedule_details", {}).get("start_time", "")
        )

    return timetable


@router.post("/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str, teacher_username: Optional[str] = Query(None)):
    """Sign up a student for an activity - requires teacher authentication"""
    # Check teacher authentication
    if not teacher_username:
        raise HTTPException(
            status_code=401, detail="Authentication required for this action")

    teacher = teachers_collection.find_one({"_id": teacher_username})
    if not teacher:
        raise HTTPException(
            status_code=401, detail="Invalid teacher credentials")

    # Get the activity
    activity = activities_collection.find_one({"_id": activity_name})
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(
            status_code=400, detail="Already signed up for this activity")

    # Add student to participants
    result = activities_collection.update_one(
        {"_id": activity_name},
        {"$push": {"participants": email}}
    )

    if result.modified_count == 0:
        raise HTTPException(
            status_code=500, detail="Failed to update activity")

    return {"message": f"Signed up {email} for {activity_name}"}


@router.post("/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str, teacher_username: Optional[str] = Query(None)):
    """Remove a student from an activity - requires teacher authentication"""
    # Check teacher authentication
    if not teacher_username:
        raise HTTPException(
            status_code=401, detail="Authentication required for this action")

    teacher = teachers_collection.find_one({"_id": teacher_username})
    if not teacher:
        raise HTTPException(
            status_code=401, detail="Invalid teacher credentials")

    # Get the activity
    activity = activities_collection.find_one({"_id": activity_name})
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Validate student is signed up
    if email not in activity["participants"]:
        raise HTTPException(
            status_code=400, detail="Not registered for this activity")

    # Remove student from participants
    result = activities_collection.update_one(
        {"_id": activity_name},
        {"$pull": {"participants": email}}
    )

    if result.modified_count == 0:
        raise HTTPException(
            status_code=500, detail="Failed to update activity")

    return {"message": f"Unregistered {email} from {activity_name}"}
