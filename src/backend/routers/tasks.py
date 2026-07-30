"""
Task/To-Do endpoints for the High School Management System API
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId
from datetime import datetime

from ..database import tasks_collection

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)


class TaskCreate(BaseModel):
    title: str
    deadline: Optional[str] = None


def serialize_task(task: dict) -> dict:
    """Convert a MongoDB task document to a JSON-serializable dict."""
    return {
        "id": str(task["_id"]),
        "student_email": task["student_email"],
        "title": task["title"],
        "deadline": task.get("deadline"),
        "completed": task.get("completed", False),
        "created_at": task.get("created_at", ""),
    }


@router.get("", response_model=List[dict])
def get_tasks(student_email: str) -> List[dict]:
    """Get all tasks for a student by their email address."""
    if not student_email:
        raise HTTPException(status_code=400, detail="student_email is required")

    tasks = tasks_collection.find({"student_email": student_email})
    return [serialize_task(t) for t in tasks]


@router.post("", response_model=dict, status_code=201)
def create_task(student_email: str, task: TaskCreate) -> dict:
    """Create a new task for a student."""
    if not student_email:
        raise HTTPException(status_code=400, detail="student_email is required")

    if not task.title or not task.title.strip():
        raise HTTPException(status_code=400, detail="Task title cannot be empty")

    doc = {
        "student_email": student_email,
        "title": task.title.strip(),
        "deadline": task.deadline,
        "completed": False,
        "created_at": datetime.utcnow().isoformat(),
    }

    result = tasks_collection.insert_one(doc)
    doc["_id"] = result.inserted_id
    return serialize_task(doc)


@router.patch("/{task_id}/complete", response_model=dict)
def toggle_task_complete(task_id: str, student_email: str) -> dict:
    """Toggle the completed status of a task."""
    try:
        oid = ObjectId(task_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid task ID")

    task = tasks_collection.find_one({"_id": oid, "student_email": student_email})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    new_status = not task.get("completed", False)
    tasks_collection.update_one({"_id": oid}, {"$set": {"completed": new_status}})
    task["completed"] = new_status
    return serialize_task(task)


@router.delete("/{task_id}", status_code=200)
def delete_task(task_id: str, student_email: str) -> dict:
    """Delete a task belonging to a student."""
    try:
        oid = ObjectId(task_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid task ID")

    result = tasks_collection.delete_one({"_id": oid, "student_email": student_email})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task deleted"}
