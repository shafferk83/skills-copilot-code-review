"""
Endpoints for the Internship Directory
"""

from fastapi import APIRouter
from typing import Any, Dict, List, Optional

from ..database import internships_collection

router = APIRouter(
    prefix="/internships",
    tags=["internships"]
)


@router.get("", response_model=List[Dict[str, Any]])
@router.get("/", response_model=List[Dict[str, Any]])
def get_internships(branch: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Get all internship listings, with optional filtering by branch/department.

    - branch: Filter internships by this branch (e.g., 'Technology', 'Science')
    """
    query: Dict[str, Any] = {}
    if branch:
        query["branch"] = branch

    internships = []
    for internship in internships_collection.find(query):
        internship["id"] = str(internship.pop("_id"))
        internships.append(internship)

    return internships


@router.get("/branches", response_model=List[str])
def get_branches() -> List[str]:
    """Get a sorted list of all unique branches available in internship listings."""
    pipeline = [
        {"$group": {"_id": "$branch"}},
        {"$sort": {"_id": 1}}
    ]

    branches = []
    for doc in internships_collection.aggregate(pipeline):
        if doc["_id"]:
            branches.append(doc["_id"])

    return branches
